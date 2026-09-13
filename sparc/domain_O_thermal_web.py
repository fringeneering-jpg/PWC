"""
DOMAIN O -- Thermal-web constitutive test, pre-registered exactly as specified:

  T_med(r) = T_bg + A_T * I_3.6(r)          (I_3.6(r) = local stellar heat proxy,
                                              radially resolved via Vdisk/Vbulge,
                                              NOT the single aggregate SBdisk number)
  rho_med(r) = rho_ref * [T_ref / T_med(r)]^beta
             = rho0 / (1 + A*I_3.6(r))^beta      (reparametrized, same physics,
                                                    fewer degenerate constants)
  M_med(<r) = 4*pi * INTEGRAL rho_med(r') r'^2 dr'   (real shell integration,
                                                        per galaxy, over its own
                                                        measured radii)
  g_med(r) = G*M_med(<r)/r^2

  g_bar_ext = g_bar + g_med(r), fed into the SAME choke n=1/2 formula.

  Fit (a0, rho0, A, beta) jointly on TRAINING galaxies only, all shape params
  constrained >= 0 (beta>0 required for "hotter -> lower density" as specified).
  Same 70/30 galaxy-level split, seed=7, as every other domain tonight.

PRE-REGISTERED SUCCESS CRITERIA (all three required, checked honestly either way):
  1. holdout rms < 0.1298 dex  (beats McGaugh RAR holdout)
  2. p(residual vs gas fraction) > 0.05  (residual no longer significant)
  3. p(residual vs surface brightness) > 0.05  (residual no longer significant)
"""
import numpy as np, json
from scipy.optimize import minimize, minimize_scalar
from scipy import stats
from scipy.integrate import cumulative_trapezoid

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
gasfrac_gal = {n: (MHI_d[n]/L36[n]) if (n in L36 and L36[n]>0 and n in MHI_d and np.isfinite(MHI_d[n])) else np.nan for n in t1["Name"]}

name = np.array(t2["Name"]); R = np.array(t2["Rad"], float)
Vo = np.array(t2["Vobs"], float); eVo = np.array(t2["e_Vobs"], float)
Vg = np.array(t2["Vgas"], float); Vd = np.array(t2["Vdisk"], float); Vb = np.array(t2["Vbulge"], float)
Vb = np.where(np.isnan(Vb), 0.0, Vb); Vg = np.where(np.isnan(Vg), 0.0, Vg)

inc_a  = np.array([inc.get(n, np.nan)  for n in name], float)
qual_a = np.array([qual.get(n, np.nan) for n in name], float)
m = (R > 0) & (Vo > 0) & np.isfinite(eVo)
m &= (eVo/Vo <= 0.10); m &= (inc_a >= 30.0); m &= (qual_a <= 2)
R, Vo, eVo, Vg, Vd, Vb, name = R[m], Vo[m], eVo[m], Vg[m], Vd[m], Vb[m], name[m]

conv = (KMS**2)/KPC
g_obs = Vo**2 / R * conv
Vbar2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
g_bar = Vbar2 / R * conv
# LOCAL stellar heat proxy I_3.6(r): stars only (disk+bulge), radially resolved,
# NOT gas -- this is the actual "heat source" term, distinct from gas geometry
Vstar2 = UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
I_local = Vstar2 / R * conv   # same units as g_bar, a real local stellar-field proxy
ok = (g_bar > 0) & (g_obs > 0)
g_obs, g_bar, R, name, I_local = g_obs[ok], g_bar[ok], R[ok], name[ok], I_local[ok]
y = np.log10(g_obs)

galaxies = sorted(set(name))
rng = np.random.default_rng(7)
shuffled = galaxies.copy(); rng.shuffle(shuffled)
n_train = int(len(shuffled)*0.7)
train_gal = set(shuffled[:n_train]); hold_gal = set(shuffled[n_train:])
train_mask = np.array([n in train_gal for n in name])
hold_mask  = np.array([n in hold_gal  for n in name])

def choke_half(gb, a0): return gb*(1.0 + (a0/gb)**0.5)

# per-galaxy shell integration of rho_med(r) = rho0/(1+A*I_local(r))^beta
def g_medium_all(R_all, I_all, name_all, rho0, A, beta):
    g_med = np.zeros_like(R_all)
    for g in set(name_all):
        gm = (name_all == g)
        r_g = R_all[gm]; I_g = I_local_lookup(I_all, gm)
        order = np.argsort(r_g)
        r_sorted = r_g[order]
        I_sorted = I_g[order]
        rho_sorted = rho0 / (1.0 + A*I_sorted)**beta
        integrand = rho_sorted * (r_sorted*KPC)**2
        r_m = r_sorted*KPC
        # cumulative shell mass, starting M(0)=0
        if len(r_m) > 1:
            Menc = np.concatenate([[0.0], cumulative_trapezoid(integrand, r_m)])
        else:
            Menc = np.array([integrand[0]*r_m[0]])  # crude single-point fallback
        Menc = 4*np.pi*Menc
        g_med_sorted = G*Menc/np.maximum(r_m,1e-10)**2
        g_med[np.where(gm)[0][order]] = g_med_sorted
    return g_med

def I_local_lookup(I_all, mask):
    return I_all[mask]

print("=== BASELINE ===")
def obj_base(la0):
    return np.mean((y[train_mask] - np.log10(choke_half(g_bar[train_mask], 10**la0)))**2)
o0 = minimize_scalar(obj_base, bounds=(-12.0,-9.0), method="bounded")
a0_base = 10**o0.x
rms_base_ho = np.sqrt(np.mean((y[hold_mask] - np.log10(choke_half(g_bar[hold_mask], a0_base)))**2))
print(f"a0={a0_base:.4e}, holdout rms={rms_base_ho:.4f}")

print("\n=== THERMAL-WEB MEDIUM (pre-registered form, fit on TRAIN only) ===")

def obj_ext(p):
    la0, lrho0, lA, lbeta = p
    a0, rho0, A, beta = 10**la0, 10**lrho0, 10**lA, 10**lbeta
    if beta > 5 or A > 1e5: return 1e9
    gm_tr = g_medium_all(R[train_mask], I_local[train_mask], name[train_mask], rho0, A, beta)
    gb_ext = g_bar[train_mask] + gm_tr
    if np.any(~np.isfinite(gb_ext)) or np.any(gb_ext<=0): return 1e9
    return np.mean((y[train_mask] - np.log10(choke_half(gb_ext, a0)))**2)

best = minimize(obj_ext, x0=[-10.0, -24.0, 0.0, -0.3], method="Nelder-Mead",
                 options=dict(xatol=1e-7, fatol=1e-11, maxiter=4000))
la0_e, lrho0_e, lA_e, lbeta_e = best.x
a0_e, rho0_e, A_e, beta_e = 10**la0_e, 10**lrho0_e, 10**lA_e, 10**lbeta_e
print(f"fitted: a0={a0_e:.4e}, rho0={rho0_e:.4e} kg/m^3, A={A_e:.4e}, beta={beta_e:.4f}")

gm_ho = g_medium_all(R[hold_mask], I_local[hold_mask], name[hold_mask], rho0_e, A_e, beta_e)
gb_ho_ext = g_bar[hold_mask] + gm_ho
rms_ext_ho = np.sqrt(np.mean((y[hold_mask] - np.log10(choke_half(gb_ho_ext, a0_e)))**2))
print(f"\nHOLDOUT rms (thermal-web) = {rms_ext_ho:.4f}  (baseline {rms_base_ho:.4f}, RAR benchmark 0.1298)")

gm_all = g_medium_all(R, I_local, name, rho0_e, A_e, beta_e)
resid_all = y - np.log10(choke_half(g_bar+gm_all, a0_e))
gal_resid, gal_gf, gal_sb = [], [], []
SBd  = {n:v for n,v in zip(t1["Name"], t1["SBdisk"])}
for g in galaxies:
    gm_ = (name == g)
    if gm_.sum() < 1: continue
    gf = gasfrac_gal.get(g, np.nan); sb = SBd.get(g, np.nan)
    if not np.isfinite(gf): continue
    gal_resid.append(np.mean(resid_all[gm_])); gal_gf.append(gf); gal_sb.append(sb)
gal_resid = np.array(gal_resid); gal_gf = np.array(gal_gf); gal_sb = np.array(gal_sb)
valid_sb = np.isfinite(gal_sb)
rho_gas, p_gas = stats.spearmanr(np.log10(gal_gf), gal_resid)
rho_sb, p_sb = stats.spearmanr(gal_sb[valid_sb], gal_resid[valid_sb])

print(f"\nresidual vs gas fraction: rho={rho_gas:+.3f}, p={p_gas:.4f}  (need p>0.05 to pass)")
print(f"residual vs surface brightness: rho={rho_sb:+.3f}, p={p_sb:.4f}  (need p>0.05 to pass)")

print("\n=== PRE-REGISTERED VERDICT ===")
c1 = rms_ext_ho < 0.1298
c2 = p_gas > 0.05
c3 = p_sb > 0.05
print(f"1. holdout < 0.1298 dex: {'PASS' if c1 else 'FAIL'} ({rms_ext_ho:.4f})")
print(f"2. gas residual p>0.05:  {'PASS' if c2 else 'FAIL'} (p={p_gas:.4f})")
print(f"3. SB residual p>0.05:   {'PASS' if c3 else 'FAIL'} (p={p_sb:.4f})")
print(f"\nALL THREE: {'PASS' if (c1 and c2 and c3) else 'FAIL'}")
