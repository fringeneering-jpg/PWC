"""rho_max shell vs sonic choke on GWTC-4.0 (prediction frozen in predictions/gwtc4_shell_vs_choke.md)."""
import numpy as np, pandas as pd
G = 6.6743e-11; c = 299792458.0; Ms = 1.98892e30; RHO_MAX = 1.304e15; RHO_NUC = 2.3e17
t = pd.read_csv("gwtc4_blind_results.csv")
t["Mheld"] = t.Mf - t.Cf
Rc = (3 * t.Cf * Ms / (4 * np.pi * RHO_NUC)) ** (1 / 3)
t["Rmax_km"] = ((Rc ** 3 + 3 * t.Mheld.clip(lower=0) * Ms / (4 * np.pi * RHO_MAX)) ** (1 / 3)) / 1e3
t["rs_km"] = 2 * G * t.Mf * Ms / c ** 2 / 1e3
t["rplus_km"] = G * t.Mf * Ms / c ** 2 * (1 + np.sqrt(1 - t.chi_f.clip(upper=0.998) ** 2)) / 1e3
t["ratio"] = t.Rmax_km / t.rs_km; t["ratio_kerr"] = t.Rmax_km / t.rplus_km
inside = (t.ratio <= 1).sum()
print(f"R_max <= r_sonic: {inside}/{len(t)}   (prediction: all {len(t)})")
print(f"R_max <= Kerr r+: {(t.ratio_kerr <= 1).sum()}/{len(t)}")
s = t.sort_values("Mf")
cross = s[s.ratio <= 1].Mf.min()
print(f"lightest black hole with shell inside the choke: M_f = {cross:.1f} Msun; heaviest outside: {s[s.ratio > 1].Mf.max():.1f} Msun")
for lo, hi in [(0, 25), (25, 45), (45, 60), (60, 100), (100, 300)]:
    x = s[(s.Mf >= lo) & (s.Mf < hi)]
    if len(x): print(f"   M_f {lo:>3}-{hi:<3}: n={len(x):>2}  median R_max {x.Rmax_km.median():6.1f} km  r_sonic {x.rs_km.median():6.1f} km  ratio {x.ratio.median():.2f}  inside {int((x.ratio<=1).sum())}/{len(x)}")
print("fit: ratio ~ M^%.2f (expected ~ -0.78)" % np.polyfit(np.log10(s.Mf), np.log10(s.ratio), 1)[0])
t.to_csv("gwtc4_shell_vs_choke.csv", index=False)
