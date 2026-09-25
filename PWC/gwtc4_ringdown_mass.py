"""Medium outside the choke vs ringdown (prediction frozen in predictions/gwtc4_ringdown_mass.md)."""
import numpy as np, pandas as pd
G = 6.6743e-11; c = 299792458.0; Ms = 1.98892e30; RM = 1.304e15; RN = 2.3e17; YIELD = 3.23e11
t = pd.read_csv("gwtc4_blind_results.csv")
def profile(Mf, Cf):
    Mf, Cf = Mf * Ms, Cf * Ms; Mmed = max(Mf - Cf, 0.0)
    Rc = (3 * Cf / (4 * np.pi * RN)) ** (1 / 3); ry = np.sqrt(G * Mf / YIELD)
    m_maxp_full = RM * 4 / 3 * np.pi * max(ry ** 3 - Rc ** 3, 0.0)
    if m_maxp_full >= Mmed:                       # all medium fits in the max-P layer
        Rend = (Rc ** 3 + 3 * Mmed / (4 * np.pi * RM)) ** (1 / 3); ry_eff = Rend; Rout = Rend
    else:
        ry_eff = max(ry, Rc); Rout = ry_eff + (Mmed - m_maxp_full) / (4 * np.pi * RM * ry_eff ** 2)
    def Menc(r):
        if r <= Rc: return Cf * (r / Rc) ** 3
        m = Cf + RM * 4 / 3 * np.pi * (min(r, ry_eff) ** 3 - Rc ** 3)
        if r > ry_eff: m += 4 * np.pi * RM * ry_eff ** 2 * (min(r, Rout) - ry_eff)
        return min(m, Mf)
    Mrd = Mf
    for _ in range(200): Mrd = Menc(3 * G * Mrd / c ** 2)
    rs = 2 * G * Mf / c ** 2
    return Mrd / Ms, (Mf - Menc(rs)) / Ms, Rout / 1e3, rs / 1e3
out = [profile(r.Mf, r.Cf) for r in t.itertuples()]
t["M_rd"], t["M_outside_choke"], t["R_out_km"], t["rs_km"] = zip(*out)
t["dM"] = (t.Mf - t.M_rd) / t.Mf; t["frac_out"] = t.M_outside_choke / t.Mf
print(f"events: {len(t)}   median inspiral-ringdown mismatch dM/M = {100*t.dM.median():.1f}%   within 10%: {(t.dM<=0.10).sum()}/{len(t)}")
for lo, hi in [(0, 25), (25, 45), (45, 60), (60, 100), (100, 300)]:
    s = t[(t.Mf >= lo) & (t.Mf < hi)]
    if len(s): print(f"   M_f {lo:>3}-{hi:<3}: n={len(s):>2}  median dM/M {100*s.dM.median():5.1f}%   mass outside choke {100*s.frac_out.median():5.1f}%   medium ends at {s.R_out_km.median():6.1f} km vs choke {s.rs_km.median():6.1f} km")
t.to_csv("gwtc4_ringdown_mass.csv", index=False)
