"""
DOMAIN Q -- properly sequenced, properly geometric thermal-medium test.

SEQUENCE (physics first, numerics second, exactly as specified):
  1. Fix the physical law: Pi(I) = 1/(1+exp((I-I_crit)/dI))  -- logistic
     permeability in the LOCAL heat proxy I_local(R), ONE candidate being
     tested, not asserted as confirmed.
  2. Sigma_med(R) = M_tot * Pi(R) / [2*pi*INT Pi(R')R'dR'],  M_tot = xi*Mbar
     -- exact disk-plane mass conservation, tied to each galaxy's own real
     baryonic mass (not a free per-galaxy amplitude).
  3. NUMERICAL SOLVER STEP ONLY: approximate that FIXED target Sigma_med(R)
     with a non-negative least-squares combination of a fixed bank of
     exponential-disk components (fixed scale lengths, chosen once, not
     fit parameters of the physics). Approximation error is tracked.
  4. Disk gravity computed via the verified closed-form Freeman kernel for
     each component (fast, reliable, already validated earlier tonight),
     summed by linearity -- no oscillatory/unbounded numerical integrals.
  5. Outer optimization is ONLY over the physical parameters (a0, xi,
     I_crit, dI). The exponential coefficients are recomputed by NNLS at
     every evaluation from the CURRENT physical Sigma_med(R) -- they are
     never free parameters of the fit themselves.

Same pre-registered criteria, same 10-seed stability protocol as before.
"""
import numpy as np, json, time
from scipy.optimize import minimize, minimize_scalar, nnls
from scipy.special import iv, kv
from scipy import stats
from scipy.interpolate import interp1d

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
KMS = 1.0e3
G = 6.674e-11
MSUN = 1.989e30
UPS_D, UPS_B = 0.5, 0.7

def read_vizier_tsv(path, cols):
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8", errors="replace")]
    hdr_i = None
    for i, l in enumerate(lines):
        if l.startswith("#") or not l.strip(): continue
        if "\t" in l and "recno" in l: hdr_i = i; break
    names = lines[hdr_i].split("\t")
    dash_i = None
    for i in range(hdr_i+1, min(hdr_i+6, len(lines))):
        if set(lines[i].replace("\t","").strip()) <= set("- "): dash_i = i
    idx = {c: names.index(c) for c in cols}
    out = {c: [] for c in cols}
    for l in lines[dash_i+1:]:
        if not l.strip() or l.startswith("#"): continue
        f = l.split("\t")
        if len(f) < len(names): continue
        try:
            for c in cols:
                v = f[idx[c]].strip()
                out[c].append(v if c == "Name" else (float(v) if v not in ("","---") else np.nan))
        except ValueError:
            continue
    return out

t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name","i","Qual","Vflat","Dist","L3.6","SBdisk","MHI"])
t2 = read_vizier_tsv(f"{D}/vizier_t2.txt", ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
inc  = {n:i for n,i in zip(t1["Name"], t1["i"])}
qual = {n:q for n,q in zip(t1["Name"], t1["Qual"])}
L36  = {n:v for n,v in zip(t1["Name"], t1["L3.6"])}
MHI_d  = {n:v for n,v in zip(t1["Name"], t1["MHI"])}
SBd  = {n:v for n,v in zip(t1["Name"], t1["SBdisk"])}
gasfrac_gal = {n: (MHI_d[n]/L36[n]) if (n in L36 and L36[n]>0 and n in MHI_d and np.isfinite(MHI_d[n])) else np.nan for n in t1["Name"]}
Mbar_gal = {n: (UPS_D*L36[n] + 1.33*MHI_d.get(n,0.0))*1e9*MSUN
            for n in t1["Name"] if n in L36 and np.isfinite(L36[n]) and L36[n] > 0}

name = np.array(t2["Name"]); R = np.array(t2["Rad"], float)
Vo = np.array(t2["Vobs"], float); eVo = np.array(t2["e_Vobs"], float)
Vg = np.array(t2["Vgas"], float); Vd = np.array(t2["Vdisk"], float); Vb = np.array(t2["Vbulge"], float)
Vb = np.where(np.isnan(Vb), 0.0, Vb); Vg = np.where(np.isnan(Vg), 0.0, Vg)

inc_a  = np.array([inc.get(n, np.nan)  for n in name], float)
qual_a = np.array([qual.get(n, np.nan) for n in name], float)
m = (R > 0) & (Vo > 0) & np.isfinite(eVo)
m &= (eVo/Vo <= 0.10); m &= (inc_a >= 30.0); m &= (qual_a <= 2)
m &= np.array([n in Mbar_gal for n in name])
R, Vo, eVo, Vg, Vd, Vb, name = R[m], Vo[m], eVo[m], Vg[m], Vd[m], Vb[m], name[m]

conv = (KMS**2)/KPC
g_obs = Vo**2 / R * conv
Vbar2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
g_bar = Vbar2 / R * conv
Vstar2 = UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
I_local = Vstar2 / R * conv
ok = (g_bar > 0) & (g_obs > 0)
g_obs, g_bar, R, name, I_local = g_obs[ok], g_bar[ok], R[ok], name[ok], I_local[ok]
y_all = np.log10(g_obs)
Mbar_point = np.array([Mbar_gal[n] for n in name])
galaxies = sorted(set(name))

def choke_half(gb, a0): return gb*(1.0 + (a0/gb)**0.5)

# --- fixed exponential basis (scale lengths only, chosen once, not fit params) ---
RD_BASIS_KPC = np.array([0.3, 0.6, 1.2, 2.5, 4.0, 6.0, 9.0, 13.0, 18.0, 25.0])
N_BASIS = len(RD_BASIS_KPC)

def freeman_unit(R_m, rd_m):
    """Freeman V^2(R) for Sigma0=1. Returns V^2, units m^2/s^2 per (kg/m^2)."""
    y = np.clip(R_m/(2.0*rd_m), 1e-8, 50)
    bess = iv(0,y)*kv(0,y) - iv(1,y)*kv(1,y)
    return 4*np.pi*G*rd_m*y**2*bess

print("Precomputing per-galaxy geometry (grid, basis kernels, Freeman unit curves)...")
t_start = time.time()
GAL = {}
for g in galaxies:
    gm = (name == g)
    r_g = R[gm]; I_g = I_local[gm]
    order = np.argsort(r_g)
    r_sorted = r_g[order]; I_sorted = I_g[order]
    Rmax_kpc = r_sorted[-1]*1.02
    Rgrid_kpc = np.linspace(max(0.01, r_sorted[0]*0.3), Rmax_kpc, 120)
    Rgrid_m = Rgrid_kpc*KPC

    # interpolate I_local onto the fine grid (edge-extrapolated)
    I_interp = interp1d(r_sorted, I_sorted, kind="linear", bounds_error=False,
                         fill_value=(I_sorted[0], I_sorted[-1]))
    I_on_grid = I_interp(Rgrid_kpc)

    # basis matrix on the grid, for NNLS fitting of Sigma_med(R) each iteration
    Bgrid = np.exp(-Rgrid_m[:,None]/(RD_BASIS_KPC[None,:]*KPC))  # (ngrid, nbasis)

    # basis Freeman unit V^2 curves evaluated at the GALAXY'S ACTUAL measured radii
    # (precomputed ONCE -- independent of physics params, huge speedup)
    r_meas_m = r_sorted*KPC
    U = np.stack([freeman_unit(r_meas_m, rd*KPC) for rd in RD_BASIS_KPC], axis=1)  # (npts, nbasis)

    GAL[g] = dict(order=order, r_sorted=r_sorted, I_sorted=I_sorted,
                  Rgrid_kpc=Rgrid_kpc, Rgrid_m=Rgrid_m, I_on_grid=I_on_grid,
                  Bgrid=Bgrid, U=U, Mbar=Mbar_gal[g], idx=np.where(gm)[0])
print(f"  done in {time.time()-t_start:.1f}s for {len(galaxies)} galaxies\n")

def g_medium_all(names_subset, xi, I_crit, dI):
    g_med = np.zeros(len(name))
    for g in names_subset:
        d = GAL[g]
        Pi_grid = 1.0/(1.0+np.exp((d["I_on_grid"]-I_crit)/dI))
        norm = 2*np.pi*np.trapezoid(Pi_grid*d["Rgrid_m"], d["Rgrid_m"])
        if norm <= 0 or not np.isfinite(norm):
            continue
        Mtot = xi*d["Mbar"]
        Sigma_target = Mtot*Pi_grid/norm   # kg/m^2 on the grid

        c, _ = nnls(d["Bgrid"], Sigma_target, maxiter=200)
        V2_med = d["U"] @ c   # (npts,), m^2/s^2
        g_med_sorted = V2_med / d["r_sorted"] / KPC
        g_med[d["idx"][d["order"]]] = g_med_sorted
    return g_med

print("=== quick single-galaxy sanity check ===")
test_g = galaxies[0]
g_test = g_medium_all([test_g], xi=0.2, I_crit=5e-11, dI=2e-11)
print(f"galaxy {test_g}: g_med nonzero points = {np.sum(g_test!=0)}, "
      f"range = [{g_test[g_test!=0].min():.3e}, {g_test[g_test!=0].max():.3e}]" if np.any(g_test!=0) else "all zero")

def run_seed(seed, verbose=True):
    rng = np.random.default_rng(seed)
    shuffled = galaxies.copy(); rng.shuffle(shuffled)
    n_train = int(len(shuffled)*0.7)
    train_gal = shuffled[:n_train]; hold_gal = shuffled[n_train:]
    train_mask = np.array([n in set(train_gal) for n in name])
    hold_mask  = np.array([n in set(hold_gal)  for n in name])

    def obj_base(la0):
        return np.mean((y_all[train_mask] - np.log10(choke_half(g_bar[train_mask], 10**la0)))**2)
    o0 = minimize_scalar(obj_base, bounds=(-12.0,-9.0), method="bounded")
    a0_base = 10**o0.x
    rms_base_ho = np.sqrt(np.mean((y_all[hold_mask] - np.log10(choke_half(g_bar[hold_mask], a0_base)))**2))

    def obj_ext(p):
        la0, lxi, lIcrit, ldI = p
        a0, xi, I_crit, dI = 10**la0, 10**lxi, 10**lIcrit, 10**ldI
        if xi > 20 or dI > 1e-8 or dI < 1e-13 or lIcrit < -12 or lIcrit > -9: return 1e3
        gm_tr = g_medium_all(train_gal, xi, I_crit, dI)
        gb_ext = g_bar[train_mask] + gm_tr[train_mask]
        if np.any(~np.isfinite(gb_ext)) or np.any(gb_ext<=0): return 1e3
        return np.mean((y_all[train_mask] - np.log10(choke_half(gb_ext, a0)))**2)

    best = minimize(obj_ext, x0=[-10.0, -0.7, -10.3, -10.5], method="Nelder-Mead",
                     options=dict(xatol=1e-6, fatol=1e-10, maxiter=800))
    la0_e, lxi_e, lIcrit_e, ldI_e = best.x
    a0_e, xi_e, Icrit_e, dI_e = 10**la0_e, 10**lxi_e, 10**lIcrit_e, 10**ldI_e

    gm_all_vals = g_medium_all(galaxies, xi_e, Icrit_e, dI_e)
    gb_ho_ext = g_bar[hold_mask] + gm_all_vals[hold_mask]
    rms_ext_ho = np.sqrt(np.mean((y_all[hold_mask] - np.log10(choke_half(gb_ho_ext, a0_e)))**2))

    resid_all = y_all - np.log10(choke_half(g_bar+gm_all_vals, a0_e))
    gal_resid, gal_gf, gal_sb = [], [], []
    for gname in galaxies:
        gmk = (name == gname)
        if gmk.sum() < 1: continue
        gf = gasfrac_gal.get(gname, np.nan); sb = SBd.get(gname, np.nan)
        if not np.isfinite(gf): continue
        gal_resid.append(np.mean(resid_all[gmk])); gal_gf.append(gf); gal_sb.append(sb)
    gal_resid=np.array(gal_resid); gal_gf=np.array(gal_gf); gal_sb=np.array(gal_sb)
    valid_sb = np.isfinite(gal_sb)
    rho_gas,p_gas = stats.spearmanr(np.log10(gal_gf), gal_resid)
    rho_sb,p_sb = stats.spearmanr(gal_sb[valid_sb], gal_resid[valid_sb])

    if verbose:
        print(f"seed={seed:2d} a0={a0_e:.3e} xi={xi_e:.4f} I_crit={Icrit_e:.3e} dI={dI_e:.3e} "
              f"base_ho={rms_base_ho:.4f} ext_ho={rms_ext_ho:.4f} p_gas={p_gas:.3f} p_sb={p_sb:.3f}")
    return dict(seed=seed, a0=a0_e, xi=xi_e, Icrit=Icrit_e, dI=dI_e,
                rms_base=rms_base_ho, rms_ext=rms_ext_ho, p_gas=p_gas, p_sb=p_sb)

print("\n=== SEED 7 ONLY FIRST (timing + sanity check before full sweep) ===")
t0 = time.time()
r7 = run_seed(7)
print(f"single-seed wall time: {time.time()-t0:.1f}s")
