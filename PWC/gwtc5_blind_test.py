"""GWTC-5.0 blind test (predictions frozen in predictions/gwtc5_blind.md).
Recipe from PWC.md §3/§8, k = 0.868899 frozen. Source: gw_allevents.json (GWOSC eventapi, fetched 2026-09-25).
Final spin not published in GWOSC summaries: computed from m1, m2, chi_eff (a1 = a2 = chi_eff) with the
Rezzolla et al. 2008 (ApJ 674, L29) aligned-spin fit — used only for the Kerr horizon in Test B."""
import json, numpy as np, pandas as pd
from scipy.optimize import brentq
from scipy.stats import pearsonr, spearmanr
k = 0.868899; G = 6.6743e-11; c = 299792458.0; Ms = 1.98892e30; RHO_NUC = 2.3e17
core = lambda m: brentq(lambda C: C + k * C ** (2 / 3) - m, 1e-6, m)
def chi_f(m1, m2, a):
    q = min(m1, m2) / max(m1, m2); nu = q / (1 + q) ** 2; at = (a + a * q * q) / (1 + q * q)
    return at + nu * (-0.1229 * at * at * nu + 0.4537 * at * nu - 2.8904 * at + 2 * np.sqrt(3) - 3.5171 * nu + 2.5763 * nu * nu)
d = json.load(open("gw_allevents.json"))["events"]
rows = []
for v in d.values():
    if v["catalog.shortName"] != "GWTC-5.0": continue
    m1, m2, Mf, ce = v.get("mass_1_source"), v.get("mass_2_source"), v.get("final_mass_source"), v.get("chi_eff")
    if None in (m1, m2, Mf) or m2 < 3: continue
    ce = 0.0 if ce is None else ce
    C1, C2 = core(m1), core(m2); Cf = C1 + C2; pred = Cf + k * Cf ** (2 / 3)
    x = chi_f(m1, m2, ce); rp = G * Mf * Ms / c ** 2 * (1 + np.sqrt(1 - min(x, 0.998) ** 2)); rc = (3 * Cf * Ms / (4 * np.pi * RHO_NUC)) ** (1 / 3)
    rho = (Mf - Cf) * Ms / (4 / 3 * np.pi * (rp ** 3 - rc ** 3)) if Mf > Cf and rp > rc else np.nan
    rows.append(dict(event=v["commonName"], m1=m1, m2=m2, Mf=Mf, chi_eff=ce, chi_f=x, Cf=Cf, pred=pred, dev=(pred - Mf) / Mf, rho=rho))
t = pd.DataFrame(rows).sort_values("Mf")
print(f"GWTC-5.0 BBH events: {len(t)} (GWTC-5.0; none in earlier catalogues)  names: {t.event.str[:4].unique()}")
print(f"\nTEST A: mean deviation {100*t.dev.mean():+.2f}%  std {100*t.dev.std():.2f}%  corr(C_f, dev) = {pearsonr(t.Cf, t.dev)[0]:+.3f}  (89-event run: -0.97% ± 2.02%, +0.624)")
print(f"   within ±2%: {int((t.dev.abs()<0.02).sum())}/{len(t)}; worst: " + ", ".join(f"{r.event} {100*r.dev:+.1f}%" for r in t.reindex(t.dev.abs().sort_values(ascending=False).index).head(3).itertuples()))
g = t.dropna(subset=["rho"]); sl = np.polyfit(np.log10(g.Mf), np.log10(g.rho), 1)[0]
print(f"\nTEST B: rho_shell median {g.rho.median():.3e} kg/m3 (GW150914: 1.304e15), range {g.rho.min():.2e} – {g.rho.max():.2e}")
print(f"   log-log slope vs M_f = {sl:+.2f} (pass needs |slope| < 0.3; recipe expectation ~ -7/3 = -2.33); Spearman rho = {spearmanr(g.Mf, g.rho)[0]:+.2f}")
for lo, hi in [(0, 25), (25, 45), (45, 70), (70, 300)]:
    s = g[(g.Mf >= lo) & (g.Mf < hi)]
    if len(s): print(f"   M_f {lo}-{hi} Msun: n={len(s):>2}  median rho {s.rho.median():.2e}")
t.to_csv("gwtc5_blind_results.csv", index=False)
