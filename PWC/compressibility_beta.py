"""Medium compressibility beta: M = C + K C^p, p = 2/3 + beta/3, K anchored on GW150914; beta fit on GWTC-4.0, blind on GWTC-5.0.
Prediction frozen in predictions/compressibility_beta.md."""
import numpy as np, pandas as pd
from scipy.optimize import brentq, minimize_scalar
a4 = pd.read_csv("gwtc4_blind_results.csv"); a5 = pd.read_csv("gwtc5_blind_results.csv")
def rule(beta):
    p = 2 / 3 + beta / 3
    core = lambda m, K: brentq(lambda C: C + K * C ** p - m, 1e-9, m)
    K = brentq(lambda K: (lambda Cf: Cf + K * Cf ** p)(core(35.6, K) + core(30.6, K)) - 63.1, 1e-6, 1e4)
    def pred(m1, m2): Cf = core(m1, K) + core(m2, K); return Cf + K * Cf ** p, Cf
    return K, p, pred
def score(t, beta):
    K, p, pred = rule(beta); P = np.array([pred(a, b) for a, b in zip(t.m1, t.m2)])
    dev = (P[:, 0] - t.Mf.values) / t.Mf.values
    return dev, P[:, 1], K, p
def rms4(b):
    try: return np.sqrt(np.mean(score(a4, b)[0] ** 2))
    except ValueError: return 1.0          # no K reproduces GW150914's 3.1 Msun release at this beta
fit = minimize_scalar(rms4, bounds=(-1, 0.9), method="bounded")   # p < 1 needed: at p = 1 a merger releases nothing
beta = fit.x; d4, _, K, p = score(a4, beta)
for b in [-0.5, 0, 0.3, 0.6]:
    print(f"   GWTC-4.0 rms at beta={b:+.1f}: {100*rms4(b):.2f}%")
print(f"fitted on GWTC-4.0: beta = {beta:.3f}  (p = {p:.3f}, K = {K:.4f});  GWTC-4.0 mean {100*d4.mean():+.2f}%  std {100*d4.std(ddof=1):.2f}%")
d5, C5, _, _ = score(a5, beta); d50, C50, _, _ = score(a5, 0.0)
print(f"GWTC-5.0 BLIND with beta: mean {100*d5.mean():+.2f}%  std {100*d5.std(ddof=1):.2f}%  corr(C_f,dev) {np.corrcoef(C5, d5)[0,1]:+.3f}  within 2%: {(np.abs(d5)<0.02).sum()}/{len(d5)}")
print(f"GWTC-5.0 k-rule (beta=0):  mean {100*d50.mean():+.2f}%  std {100*d50.std(ddof=1):.2f}%  corr {np.corrcoef(C50, d50)[0,1]:+.3f}")
Mt = a5.m1 + a5.m2
for lo, hi in [(0, 30), (30, 60), (60, 100), (100, 500)]:
    s = (Mt >= lo) & (Mt < hi); print(f"   M_total {lo}-{hi}: n={s.sum():>2}  median dev beta {100*np.median(d5[s]):+.2f}%   k-rule {100*np.median(d50[s]):+.2f}%")
