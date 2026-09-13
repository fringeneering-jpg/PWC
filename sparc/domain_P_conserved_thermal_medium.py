"""
DOMAIN P -- the fully-synthesized, correctly-specified model:

1. MASS-BASED, not a coupling multiplier: rho_med(r) -> M_med(<r) via real
   shell integration -> g_med(r) = G*M_med(<r)/r^2. Rotation is sourced by
   enclosed mass, not by density directly.

2. CONSERVED total budget, not a free-floating amplitude: total integrated
   medium mass per galaxy is fixed to M_med_total = xi * M_baryonic(galaxy),
   consistent with the already-established PWC principle from tonight's
   black-hole work ("bigger mass pulls in more medium"). xi is ONE
   universal constant, fit once, same for every galaxy.

3. Shape set by local heat state, not amplitude: the FIXED total mass is
   redistributed radially according to w(r) = 1/(T_bg + A*I_local(r))^beta
   (shared-pressure, ideal-gas-style local density-temperature response),
   normalized so the shape integrates to 1 -- heat spreads the SAME mass
   into more volume, it does not create or destroy medium.

4. Checked for seed stability from the start (10 splits), not as an
   afterthought.

Pre-registered criteria, same as before, now evaluated on the MEAN across
10 seeds (not one cherry-pickable split):
  1. mean holdout rms < 0.1298 dex
  2. mean p(residual vs gas fraction) > 0.05
  3. mean p(residual vs surface brightness) > 0.05
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
SBd  = {n:v for n,v in zip(t1["Name"], t1["SBdisk"])}
gasfrac_gal = {n: (MHI_d[n]/L36[n]) if (n in L36 and L36[n]>0 and n in MHI_d and np.isfinite(MHI_d[n])) else np.nan for n in t1["Name"]}
# real baryonic mass per galaxy: stars (L3.6*upsilon) + gas (1.33*MHI for He correction)
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
y = np.log10(g_obs)
Mbar_point = np.array([Mbar_gal[n] for n in name])

galaxies = sorted(set(name))

def choke_half(gb, a0): return gb*(1.0 + (a0/gb)**0.5)

def g_medium_conserved(R_all, I_all, Mbar_all, name_all, xi, A, beta):
    """Mass-conserved, heat-redistributed medium: fixed total xi*Mbar per
    galaxy, shape set by w(r) = 1/(1+A*I(r))^beta, normalized to integrate
    to that fixed total (not a free amplitude)."""
    g_med = np.zeros_like(R_all)
    for gname in set(name_all):
        gm = (name_all == gname)
        idxs = np.where(gm)[0]
        r_g = R_all[gm]; I_g = I_all[gm]; Mtot = xi*Mbar_all[gm][0]
        order = np.argsort(r_g)
        r_sorted = r_g[order]; I_sorted = I_g[order]
        w = 1.0/(1.0+A*I_sorted)**beta
        r_m = r_sorted*KPC
        integrand = w*r_m**2
        if len(r_m) > 1:
            cum = np.concatenate([[0.0], cumulative_trapezoid(integrand, r_m)])
        else:
            cum = np.array([integrand[0]*r_m[0]])
        total = cum[-1] if cum[-1] > 0 else 1.0
        Menc = Mtot * cum/total   # normalized shape * FIXED conserved total mass
        g_med_sorted = G*Menc/np.maximum(r_m,1e-10)**2
        g_med[idxs[order]] = g_med_sorted
    return g_med

rng0 = np.random.default_rng(0)
seeds = list(range(1,11))
results = []
for seed in seeds:
    rng = np.random.default_rng(seed)
    shuffled = galaxies.copy(); rng.shuffle(shuffled)
    n_train = int(len(shuffled)*0.7)
    train_gal = set(shuffled[:n_train]); hold_gal = set(shuffled[n_train:])
    train_mask = np.array([n in train_gal for n in name])
    hold_mask  = np.array([n in hold_gal  for n in name])

    def obj_base(la0):
        return np.mean((y[train_mask] - np.log10(choke_half(g_bar[train_mask], 10**la0)))**2)
    o0 = minimize_scalar(obj_base, bounds=(-12.0,-9.0), method="bounded")
    a0_base = 10**o0.x
    rms_base_ho = np.sqrt(np.mean((y[hold_mask] - np.log10(choke_half(g_bar[hold_mask], a0_base)))**2))

    def obj_ext(p):
        la0, lxi, lA, lbeta = p
        a0, xi, A, beta = 10**la0, 10**lxi, 10**lA, 10**lbeta
        if lA > 15 or lA < 5 or lbeta > 2 or xi > 50: return 1e3
        gm_tr = g_medium_conserved(R[train_mask], I_local[train_mask], Mbar_point[train_mask],
                                    name[train_mask], xi, A, beta)
        gb_ext = g_bar[train_mask] + gm_tr
        if np.any(~np.isfinite(gb_ext)) or np.any(gb_ext<=0): return 1e3
        return np.mean((y[train_mask] - np.log10(choke_half(gb_ext, a0)))**2)

    best = minimize(obj_ext, x0=[-10.0, -1.0, 10.0, -0.1], method="Nelder-Mead",
                     options=dict(xatol=1e-8, fatol=1e-12, maxiter=6000))
    la0_e, lxi_e, lA_e, lbeta_e = best.x
    a0_e, xi_e, A_e, beta_e = 10**la0_e, 10**lxi_e, 10**lA_e, 10**lbeta_e

    gm_ho = g_medium_conserved(R[hold_mask], I_local[hold_mask], Mbar_point[hold_mask],
                                name[hold_mask], xi_e, A_e, beta_e)
    gb_ho_ext = g_bar[hold_mask] + gm_ho
    rms_ext_ho = np.sqrt(np.mean((y[hold_mask] - np.log10(choke_half(gb_ho_ext, a0_e)))**2))

    gm_all = g_medium_conserved(R, I_local, Mbar_point, name, xi_e, A_e, beta_e)
    resid_all = y - np.log10(choke_half(g_bar+gm_all, a0_e))
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

    results.append(dict(seed=seed, a0=a0_e, xi=xi_e, A=A_e, beta=beta_e,
                         rms_base=rms_base_ho, rms_ext=rms_ext_ho, p_gas=p_gas, p_sb=p_sb))
    print(f"seed={seed:2d} a0={a0_e:.3e} xi={xi_e:.4f} A={A_e:.3e} beta={beta_e:+.4f} "
          f"base_ho={rms_base_ho:.4f} ext_ho={rms_ext_ho:.4f} p_gas={p_gas:.3f} p_sb={p_sb:.3f}")

print()
rms_ext_all = np.array([r["rms_ext"] for r in results])
rms_base_all = np.array([r["rms_base"] for r in results])
p_gas_all = np.array([r["p_gas"] for r in results])
p_sb_all = np.array([r["p_sb"] for r in results])
beats_base = np.sum(rms_ext_all < rms_base_all)
print(f"mean base holdout: {rms_base_all.mean():.4f}")
print(f"mean ext holdout:  {rms_ext_all.mean():.4f}  (beats baseline in {beats_base}/10 seeds)")
print(f"mean p_gas: {p_gas_all.mean():.4f}  (>0.05 in {np.sum(p_gas_all>0.05)}/10 seeds)")
print(f"mean p_sb:  {p_sb_all.mean():.4f}  (>0.05 in {np.sum(p_sb_all>0.05)}/10 seeds)")
print()
c1 = rms_ext_all.mean() < 0.1298
c2 = p_gas_all.mean() > 0.05
c3 = p_sb_all.mean() > 0.05
print(f"PRE-REGISTERED (mean across 10 seeds): 1={'PASS' if c1 else 'FAIL'} 2={'PASS' if c2 else 'FAIL'} 3={'PASS' if c3 else 'FAIL'} ALL={'PASS' if c1 and c2 and c3 else 'FAIL'}")
