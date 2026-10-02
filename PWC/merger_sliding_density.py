"""Merger dump with a sliding core density (Jaden, 2026-10-02).

Reproduces the 89-event table: 5 named events + the 84 events of gwtc4_blind_results.csv.
Mechanism (PWC.md section 8, "surface-gravity deficit"): each core's max pull is g = G*M/R^2 with R from the core density;
two cores that join have less max pull than the two separate, and the lost pull drops mass:
    dump = kappa * [g(M1) + g(M2) - g(M1+M2)]
New here: the core density is not one fixed number. Heavier cores are squeezed harder (denser, smaller radius):
    rho_core(M) = rho_ref * (M/M_ref)^beta
kappa is calibrated ONCE, on GW150914 (dump = 3.0 Msun). Only beta matters (rho_ref and M_ref are absorbed by kappa).
The beta -> 1 limit (same radius for every core, pull additive, small non-additive remainder) is
    dump = lam * [M1*ln(Mt/M1) + M2*ln(Mt/M2)],   Mt = M1 + M2,   lam calibrated once on GW150914.
Valid range of the fit: total merger mass 14 - 238 Msun. NOT tested on supermassive black holes.
"""
import os
import numpy as np
import pandas as pd

G, MS, RHO0, M0 = 6.6743e-11, 1.989e30, 2.3e17, 62.0
HERE = os.path.dirname(os.path.abspath(__file__))

NAMED = pd.DataFrame([("GW150914", 36.0, 29.0, 62.0), ("GW190521", 85.0, 66.0, 142.0), ("GW170104", 31.2, 19.4, 48.7),
                      ("GW170814", 30.5, 25.3, 53.2), ("GW151226", 14.2, 7.5, 20.8)],
                     columns=["event", "m1", "m2", "Mf"])
ev = pd.concat([NAMED, pd.read_csv(os.path.join(HERE, "gwtc4_blind_results.csv"))[["event", "m1", "m2", "Mf"]]],
               ignore_index=True)
ev["Mt"] = ev.m1 + ev.m2


def pull_model(beta):
    rho = lambda m: RHO0 * (m / M0) ** beta
    R = lambda m: (3 * m * MS / (4 * np.pi * rho(m))) ** (1 / 3)
    g = lambda m: G * m * MS / R(m) ** 2
    D = lambda m1, m2: g(m1) + g(m2) - g(m1 + m2)
    kappa = 3.0 * MS / D(36.0, 29.0)                       # one calibration: GW150914
    return ev.Mt - kappa * D(ev.m1, ev.m2) / MS


H = lambda m1, m2: m1 * np.log((m1 + m2) / m1) + m2 * np.log((m1 + m2) / m2)


def limit_model():
    lam = 3.0 / H(36.0, 29.0)                              # one calibration: GW150914
    return ev.Mt - lam * H(ev.m1, ev.m2), lam


def stats(pred):
    err = (pred - ev.Mf) / ev.Mf * 100
    return err, dict(mean=err.mean(), mean_abs=err.abs().mean(), sd=err.std(), n3=int((err.abs() <= 3).sum()),
                     n5=int((err.abs() <= 5).sum()), worst=err.abs().max())


if __name__ == "__main__":
    print("events: %d" % len(ev))
    print("%-34s %8s %9s %6s %6s %6s" % ("model", "mean %", "mean|e| %", "sd %", "<=3%", "<=5%"))
    for beta in (0.0, 0.5, 0.8, 0.9, 0.95):
        _, s = stats(pull_model(beta))
        print("%-34s %8.2f %9.2f %6.2f %6d %6d" % ("pull deficit, rho ~ M^%.2f" % beta, s["mean"], s["mean_abs"], s["sd"], s["n3"], s["n5"]))
    pred, lam = limit_model()
    err, s = stats(pred)
    print("%-34s %8.2f %9.2f %6.2f %6d %6d   (lam = %.4f, worst %.2f%%)" % ("limit model (beta -> 1)", s["mean"], s["mean_abs"], s["sd"], s["n3"], s["n5"], lam, s["worst"]))
    out = ev.copy()
    out["V1_km3"] = out.m1 * MS / RHO0 / 1e9
    out["V2_km3"] = out.m2 * MS / RHO0 / 1e9
    out["Vjoin_km3"] = out.V1_km3 + out.V2_km3
    out["expected_Mf"] = pred
    out["actual_Mf"] = out.Mf
    out["diff_Msun"] = pred - out.Mf
    out["diff_pct"] = err
    out.drop(columns=["Mf"]).to_csv(os.path.join(HERE, "merger_sliding_density_results.csv"), index=False)
    print("wrote merger_sliding_density_results.csv (V1, V2 = core volumes at 2.3e17 kg/m3, expected vs actual final mass)")
