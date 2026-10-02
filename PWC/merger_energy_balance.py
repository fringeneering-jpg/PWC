"""Merger mass drop: energy balance and storage bottleneck (Jaden, 2026-10-02). Newtonian 1/r^2 only; no GR formula is used.

Energy and mass are the same thing (m = L/c0^2). Heat is a separate thing and is not involved in the merger.

E  (energy limit): the cores' motion energy at contact, as mass.
    r = E1 + E2 is where the two Max-P layers touch (medium cannot stay crushed twice); E_i = sqrt(G*M_i/a_max) is the reach
    where the pull of everything inside falls to the yield a_max = 3.23e11 N/kg (PWC.md section 0 step 5).
    In a circular approach the motion (kinetic) energy is half of G*M1*M2/r, so
        E = G*M1*M2 / (2*c0^2*(E1+E2))                      -- no fitted constant here.
S  (storage limit): a bigger core stores relatively less medium (area, not volume): the loss when the cores join is
        S = k*(C1^(2/3) + C2^(2/3) - Cf^(2/3)),  C from  C + k*C^(2/3) = M,  k = 0.868899 (frozen repo constant, fitted on catalog).
Dropped mass = min(E, S): light events are energy-limited, heavy ones storage-limited.

Honest limits: the reach scale uses a_max from the GW150914 shell numbers (origin: see the yield-anchor row under Gaps in
DERIVATIONS.md; Jaden's position is a pure PWC ceiling from rho_max, derivation not in git). Catalog masses come from the
standard (GR) pipeline.
Datasets: DEV = 5 named events + gwtc4_blind_results.csv (89 events; used while the formulas were being explored);
OUT = gwtc5_blind_results.csv (104 events, no overlap with DEV, never used in any step here).
"""
import os
import numpy as np
import pandas as pd
from scipy.optimize import brentq

G, C0, MS, A_MAX, K = 6.6743e-11, 299792458.0, 1.989e30, 3.23e11, 0.868899
HERE = os.path.dirname(os.path.abspath(__file__))
NAMED = pd.DataFrame([("GW150914", 36.0, 29.0, 62.0), ("GW190521", 85.0, 66.0, 142.0), ("GW170104", 31.2, 19.4, 48.7),
                      ("GW170814", 30.5, 25.3, 53.2), ("GW151226", 14.2, 7.5, 20.8)], columns=["event", "m1", "m2", "Mf"])


def load(name):
    return pd.read_csv(os.path.join(HERE, name))[["event", "m1", "m2", "Mf"]]


DEV = pd.concat([NAMED, load("gwtc4_blind_results.csv")], ignore_index=True)
OUT = load("gwtc5_blind_results.csv")
core = lambda m: brentq(lambda c: c + K * c ** (2 / 3) - m, 1e-6, m)


def estimates(ev):
    ev = ev.copy()
    ev["Mt"] = ev.m1 + ev.m2
    edge = lambda m: np.sqrt(G * m * MS / A_MAX)
    ev["E"] = G * (ev.m1 * MS) * (ev.m2 * MS) / (2 * (edge(ev.m1) + edge(ev.m2)) * C0 ** 2) / MS
    c1, c2 = ev.m1.apply(core), ev.m2.apply(core)
    ev["S"] = K * (c1 ** (2 / 3) + c2 ** (2 / 3) - (c1 + c2) ** (2 / 3))
    ev["dump_cat"] = ev.Mt - ev.Mf
    ev["dump_min"] = np.minimum(ev.E, ev.S)
    # sliding-density limit form (PWC/merger_sliding_density.py): one constant, calibrated on GW150914 only
    H = lambda a, b: a * np.log((a + b) / a) + b * np.log((a + b) / b)
    ev["dump_limit"] = 3.0 / H(36.0, 29.0) * H(ev.m1, ev.m2)
    return ev


def report(name, ev):
    print("\n%s: %d events" % (name, len(ev)))
    print("  %-34s %8s %10s %7s %6s %6s %9s" % ("model", "mean %", "mean|e| %", "sd %", "<=3%", "<=5%", "slope/lnM"))
    for lab, col in (("energy limit E (no fitted constant)", "E"), ("storage limit S (k frozen)", "S"),
                     ("min(E, S)", "dump_min"), ("sliding-density limit form (1 const)", "dump_limit")):
        err = (ev.Mt - ev[col] - ev.Mf) / ev.Mf * 100
        print("  %-34s %8.2f %10.2f %7.2f %6d %6d %9.2f" % (lab, err.mean(), err.abs().mean(), err.std(), (err.abs() <= 3).sum(),
                                                         (err.abs() <= 5).sum(), np.polyfit(np.log(ev.Mt), err, 1)[0]))


if __name__ == "__main__":
    dev, out = estimates(DEV), estimates(OUT)
    report("DEV (explored on)", dev)
    report("OUT (GWTC-5, out of sample)", out)
    both = pd.concat([dev.assign(set="DEV"), out.assign(set="OUT")], ignore_index=True)
    both["expected_Mf"] = both.Mt - both.dump_min
    both["actual_Mf"] = both.Mf
    both["diff_pct"] = (both.expected_Mf - both.actual_Mf) / both.actual_Mf * 100
    both[["set", "event", "m1", "m2", "Mt", "E", "S", "dump_cat", "dump_min", "expected_Mf", "actual_Mf", "diff_pct"]].to_csv(
        os.path.join(HERE, "merger_energy_balance_results.csv"), index=False)
    print("\nwrote merger_energy_balance_results.csv")
