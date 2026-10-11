# The merger trivial-baseline check: does "lose 4.5%" beat min(E,S)? (2026-10-12, audit item)
import pandas as pd, numpy as np, os
HERE = os.path.dirname(os.path.abspath(__file__))
def load(name):
    return pd.read_csv(os.path.join(HERE, name))[["event", "m1", "m2", "Mf"]]
OUT = load("gwtc5_blind_results.csv")
Mt = OUT.m1 + OUT.m2
dM_obs = Mt - OUT.Mf
print(f"GWTC-5 (n={len(OUT)}):  dM/Mt mean = {100*(dM_obs/Mt).mean():.2f}%  sd = {100*(dM_obs/Mt).std():.2f}%")
# the trivial model: dM = 4.5% of Mt
triv = 0.045*Mt
err_triv = 100*(triv - dM_obs)/Mt
print(f"trivial '4.5%' model: mean error = {err_triv.mean():+.2f}%  mean|error| = {np.abs(err_triv).mean():.2f}%")
# the E/S machinery, reproduced
k = 0.868899; a_max = 3.23e11; G = 6.6743e-11; c0 = 2.99792458e8; Msun = 1.989e30
def est(row):
    M1, M2, Mf = row.m1, row.m2, row.Mf
    C1, C2 = M1, M2                                 # the CSV is in solar masses
    E1 = np.sqrt(G*M1*Msun/a_max); E2 = np.sqrt(G*M2*Msun/a_max)
    E = G*M1*M2*Msun/(2*c0**2*(E1+E2))              # in solar masses
    S = k*(C1**(2/3)+C2**(2/3)-(Mf)**(2/3))
    return min(E, S)
est_vals = OUT.apply(est, axis=1)
err_es = 100*(est_vals - dM_obs)/Mt
print(f"min(E,S):            mean error = {err_es.mean():+.2f}%  mean|error| = {np.abs(err_es).mean():.2f}%")
print(f"\nverdict: the trivial baseline and min(E,S) on the SAME out-of-sample catalog.")
print(f"The audit's claim is testable here directly: if the trivial model's |error| is")
print(f"lower, the E/S machinery carries no predictive content beyond the regularity -")
print(f"and the honest paper must say so.")
