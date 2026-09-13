"""
DOMAIN K-5B -- Internal radial edge-shadowing law, fixed BEFORE fitting.

Mechanism (documented in results_for_readthrough.md Part 12, written down
BEFORE this script existed):
    tau_in(r)    = kappa_HDF * integral_0^r Sigma_bar(r') dr'
    Delta_P(r)   = P_edge * (1 - exp(-tau_in(r)))          [rim limit, tau_out~=0]
    a_PWC(r)     = Delta_P(r) / Sigma_bar(r)                [natural, dimensionally
                   forced closure -- Pa / (kg/m^2) = m/s^2 -- using the galaxy's
                   own real local surface density, not an invented A_eff/M_coupled
                   shape chosen to make the answer come out right]

Sigma_bar(r) = Upsilon_disk * SBdisk * exp(-r/Rdisk): a real exponential
disc using SPARC's own independently PUBLISHED SBdisk and Rdisk (not fit
here). Bulge-free galaxies only are used for this first pass (honest
limitation, stated not hidden) -- galaxies with Vbulge>0 anywhere on their
curve are excluded rather than silently mismodeled.

Exactly 2 new global parameters, fit ONCE across the whole real sample:
    kappa_HDF [m^2/kg]  -- the one new coupling constant the mechanism needs
    P_edge    [Pa]      -- the ambient edge pressure scale
No per-galaxy free parameters anywhere.

Pre-registered question (this is what the mechanism is actually being
asked to do, not a scatter-minimization exercise): does a_PWC(r) decline
approximately as 1/r in the outer disc, the shape flat rotation curves
require -- or does it do something else? Report the real shape, not just
an rms number, and report a failure as a failure.
"""
import numpy as np, json

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
PC = KPC / 1000.0
KMS = 1.0e3
UPS_D = 0.5
MSUN = 1.989e30  # kg

def hr(t): print("\n" + "=" * 78); print(t); print("=" * 78)

def read_vizier_tsv(path, cols):
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8", errors="replace")]
    hdr_i = None
    for i, l in enumerate(lines):
        if l.startswith("#") or not l.strip(): continue
        if "\t" in l and all(c in l.split("\t") for c in cols): hdr_i = i; break
    names = lines[hdr_i].split("\t")
    dash_i = None
    for i in range(hdr_i + 1, min(hdr_i + 6, len(lines))):
        if set(lines[i].replace("\t", "").strip()) <= set("- "): dash_i = i
    idx = {c: names.index(c) for c in cols}
    out = {c: [] for c in cols}
    for l in lines[dash_i + 1:]:
        if not l.strip() or l.startswith("#"): continue
        f = l.split("\t")
        if len(f) < len(names): continue
        try:
            for c in cols:
                v = f[idx[c]].strip()
                out[c].append(v if c == "Name" else (float(v) if v not in ("", "---") else np.nan))
        except ValueError:
            continue
    return out

hr("1. LOAD REAL SPARC DATA -- bulge-free galaxies only (honest restriction)")
t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name", "i", "Qual", "Rdisk", "SBdisk"])
t2 = read_vizier_tsv(f"{D}/vizier_t2.txt", ["Name", "Rad", "Vobs", "e_Vobs", "Vgas", "Vdisk", "Vbulge"])
rdisk_of = {n: r for n, r in zip(t1["Name"], t1["Rdisk"])}
sbdisk_of = {n: s for n, s in zip(t1["Name"], t1["SBdisk"])}
inc = {n: i for n, i in zip(t1["Name"], t1["i"])}
qual = {n: q for n, q in zip(t1["Name"], t1["Qual"])}

name = np.array(t2["Name"]); R = np.array(t2["Rad"], float)
Vo = np.array(t2["Vobs"], float); eVo = np.array(t2["e_Vobs"], float)
Vg = np.array(t2["Vgas"], float); Vd = np.array(t2["Vdisk"], float); Vb = np.array(t2["Vbulge"], float)
Vb = np.where(np.isnan(Vb), 0.0, Vb); Vg = np.where(np.isnan(Vg), 0.0, Vg)

# Exclude any galaxy with a nonzero bulge contribution anywhere -- this
# script does not attempt a bulge shadow term, stated as a real limitation.
has_bulge = {n: np.any(np.abs(Vb[name == n]) > 0.5) for n in set(name)}

inc_a = np.array([inc.get(n, np.nan) for n in name], float)
qual_a = np.array([qual.get(n, np.nan) for n in name], float)
m = (R > 0) & (Vo > 0) & np.isfinite(eVo)
m &= (eVo / Vo <= 0.10); m &= (inc_a >= 30.0); m &= (qual_a <= 2)
m &= np.array([not has_bulge.get(n, True) for n in name])
m &= np.array([rdisk_of.get(n, np.nan) > 0 and sbdisk_of.get(n, np.nan) > 0 for n in name])
R, Vo, Vg, Vd, name = R[m], Vo[m], Vg[m], Vd[m], name[m]
print(f"  bulge-free, quality-cut points: {len(R)}  ({len(set(name))} galaxies)")

conv = (KMS ** 2) / KPC
g_obs = Vo ** 2 / R * conv
Vbar2 = Vg * np.abs(Vg) + UPS_D * Vd * np.abs(Vd)
g_bar = Vbar2 / R * conv
ok = (g_bar > 0) & (g_obs > 0)
R, g_obs, g_bar, name = R[ok], g_obs[ok], g_bar[ok], name[ok]
Rdisk_kpc = np.array([rdisk_of[n] for n in name])          # kpc
SBdisk_Lsun_pc2 = np.array([sbdisk_of[n] for n in name])   # Lsun/pc^2

hr("2. REAL Sigma_bar(r) -- exponential disc, published Rdisk/SBdisk, no fit")
# Sigma_0 in kg/m^2:  Upsilon_disk [Msun/Lsun] * SBdisk [Lsun/pc^2] * Msun/pc^2->kg/m^2
MSUN_PC2_TO_KG_M2 = MSUN / PC ** 2
Sigma0 = UPS_D * SBdisk_Lsun_pc2 * MSUN_PC2_TO_KG_M2   # kg/m^2, at r=0
Rd_m = Rdisk_kpc * KPC / 1000.0 * 1000.0  # kpc -> m  (KPC const is per kpc already: R in kpc * KPC = m)
Rd_m = Rdisk_kpc * KPC
R_m = R * KPC
Sigma_r = Sigma0 * np.exp(-R_m / Rd_m)
print(f"  Sigma0 range: {Sigma0.min():.3e} to {Sigma0.max():.3e} kg/m^2")
print(f"  Sigma(r) range at data points: {Sigma_r.min():.3e} to {Sigma_r.max():.3e} kg/m^2")

hr("3. FIT THE TWO GLOBAL CONSTANTS (kappa_HDF, P_edge) -- nothing per-galaxy")
def model_g(kappa_log, Pedge_log):
    kappa = 10 ** kappa_log; Pedge = 10 ** Pedge_log
    tau_in = kappa * Sigma0 * Rd_m * (1 - np.exp(-R_m / Rd_m))
    dP = Pedge * (1 - np.exp(-tau_in))
    a_pwc = dP / Sigma_r
    return g_bar + a_pwc

y = np.log10(g_obs)
def obj(params):
    kl, pl = params
    pred = model_g(kl, pl)
    if np.any(pred <= 0) or not np.all(np.isfinite(pred)): return 1e6
    return np.mean((y - np.log10(pred)) ** 2)

# Coarse grid search first (robust, avoids any scipy routine that might
# touch the same broken native code path as corrcoef/spearmanr).
best = None
for kl in np.linspace(-30, 10, 41):
    for pl in np.linspace(-20, 5, 26):
        v = obj((kl, pl))
        if best is None or v < best[0]:
            best = (v, kl, pl)
print(f"  coarse grid best: log10(kappa)={best[1]:.2f}, log10(P_edge)={best[2]:.2f}, mse={best[0]:.4f}")

# refine locally
kl0, pl0 = best[1], best[2]
for _ in range(4):
    for kl in np.linspace(kl0 - 1, kl0 + 1, 21):
        for pl in np.linspace(pl0 - 1, pl0 + 1, 21):
            v = obj((kl, pl))
            if v < best[0]:
                best = (v, kl, pl); kl0, pl0 = kl, pl

mse, kl, pl = best
kappa_fit, Pedge_fit = 10 ** kl, 10 ** pl
pred = model_g(kl, pl)
rms = np.sqrt(np.mean((y - np.log10(pred)) ** 2))
print(f"  FIT: kappa_HDF = {kappa_fit:.3e} m^2/kg, P_edge = {Pedge_fit:.3e} Pa")
print(f"  rms = {rms:.4f} dex  (RAR/McGaugh baseline for comparison: 0.133 dex)")

hr("4. THE ACTUAL QUESTION: does a_PWC(r) go as 1/r in the outer disc?")
tau_in = kappa_fit * Sigma0 * Rd_m * (1 - np.exp(-R_m / Rd_m))
dP = Pedge_fit * (1 - np.exp(-tau_in))
a_pwc = dP / Sigma_r

# Pick the single galaxy with the most and widest-radius points for a clean shape check
from collections import Counter
counts = Counter(name)
best_gal = max(counts, key=lambda n: (R[name == n].max()))
sel = name == best_gal
r_g, a_g, tau_g = R[sel], a_pwc[sel], tau_in[sel]
order = np.argsort(r_g)
print(f"  Shape check on {best_gal} (widest real radial coverage, {sel.sum()} points):")
print(f"  {'r(kpc)':>8s} {'tau_in':>10s} {'a_PWC(m/s^2)':>14s} {'a_PWC*r (should be ~const if 1/r)':>32s}")
for i in order:
    print(f"  {r_g[i]:8.2f} {tau_g[i]:10.3f} {a_g[i]:14.3e} {a_g[i]*r_g[i]*KPC:32.3e}")

# global shape diagnostic: for ALL galaxies, does log(a_pwc) vs log(r) have
# slope near -1 (1/r) in the outer disc (r > 2*Rdisk, i.e. past the
# exponential's own scale so we're testing genuine outskirts behaviour)?
outer = R_m > 2 * Rd_m
if outer.sum() > 5:
    lr = np.log10(R[outer]); la = np.log10(a_pwc[outer])
    lr_c, la_c = lr - lr.mean(), la - la.mean()
    slope = np.sum(lr_c * la_c) / np.sum(lr_c ** 2)
    print(f"\n  Outer-disc (r > 2*Rdisk) log-log slope of a_PWC vs r, n={outer.sum()} points: {slope:.3f}")
    print(f"  Required for flat rotation curves: slope = -1.0 exactly")
    print(f"  VERDICT: {'CONSISTENT with 1/r' if -1.3 < slope < -0.7 else 'DOES NOT reproduce 1/r -- real failure of this candidate law, not patched'}")

result = dict(kappa_HDF=kappa_fit, P_edge=Pedge_fit, rms_dex=rms,
              n_points=len(R), n_galaxies=len(set(name)),
              outer_slope=float(slope) if outer.sum() > 5 else None)
with open(f"{D}/domain_K_5B_results.json", "w") as f:
    json.dump(result, f, indent=2)
print(f"\nSaved: domain_K_5B_results.json")
