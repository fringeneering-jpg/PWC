"""Still (slow) vs moving (fast) rotators — prediction frozen in PREDICTION_fast_slow.md."""
import numpy as np, pandas as pd
from scipy import stats
rd = lambda f: pd.read_csv(f, sep=r"\s+", comment="#", header=None)
e = rd("Emsellem2011_Atlas3D_Paper3_TableB1.txt"); e = e[[0, 7, 9]]; e.columns = ["gal", "lamR", "FS"]
c15 = rd("Cappellari2013a_Atlas3D_Paper15_Table1.txt"); c15 = c15[[0, 1, 5, 7, 14]]; c15.columns = ["gal", "logsig", "logML_JAM", "q", "logL"]
c20 = rd("Cappellari2013b_Atlas3D_Paper20_Table1.txt"); c20 = c20[[0, 2, 3]]; c20.columns = ["gal", "fDM", "logML_star"]
d = e.merge(c15, on="gal").merge(c20, on="gal")
for col in ["lamR", "logsig", "logML_JAM", "q", "logL", "fDM", "logML_star"]: d[col] = pd.to_numeric(d[col], errors="coerce")
d = d.dropna(); d = d[d.q > 0]
d["A"] = d.logML_JAM - d.logML_star; d["logMs"] = d.logML_star + d.logL; d["slow"] = (d.FS.str.upper() == "S").astype(float)
print(f"galaxies: {len(d)}  slow: {int(d.slow.sum())}  fast: {int((1-d.slow).sum())}")
print(f"raw medians  A (log M/L dyn/stellar): slow {d[d.slow==1].A.median():+.3f}  fast {d[d.slow==0].A.median():+.3f} | f_DM: slow {d[d.slow==1].fDM.median():.3f}  fast {d[d.slow==0].fDM.median():.3f}")
print(f"median log M*: slow {d[d.slow==1].logMs.median():.2f}  fast {d[d.slow==0].logMs.median():.2f} | median log sigma: slow {d[d.slow==1].logsig.median():.2f}  fast {d[d.slow==0].logsig.median():.2f}")
def ols(y, cols):
    X = np.column_stack([np.ones(len(d))] + [d[c].values for c in cols]); b, res, *_ = np.linalg.lstsq(X, d[y].values, rcond=None)
    r = d[y].values - X @ b; s2 = r @ r / (len(d) - X.shape[1]); se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    return b, se, len(d) - X.shape[1]
for y in ["A", "fDM"]:
    b, se, dof = ols(y, ["logMs", "logsig", "slow"]); t = b[3] / se[3]; p = 1 - stats.t.cdf(t, dof)
    print(f"{y:4s}: slow coefficient d = {b[3]:+.4f} ± {se[3]:.4f}  (t = {t:+.2f}, one-sided p(d>0) = {p:.3f})   [logM* {b[1]:+.3f}, logsig {b[2]:+.3f}]")
    b, se, dof = ols(y, ["logMs", "logsig", "lamR"]); t = b[3] / se[3]; p = stats.t.cdf(t, dof)
    print(f"      lambda_R coefficient = {b[3]:+.4f} ± {se[3]:.4f}  (t = {t:+.2f}, one-sided p(<0) = {p:.3f})")
# matched-mass comparison: slow rotators vs fast rotators within the slow rotators' mass range
lo, hi = d[d.slow == 1].logMs.quantile([0.1, 0.9]); m = d[(d.logMs >= lo) & (d.logMs <= hi)]
print(f"mass-matched (log M* {lo:.2f}-{hi:.2f}): n slow {int(m.slow.sum())}, fast {int((1-m.slow).sum())}; median A slow {m[m.slow==1].A.median():+.3f} fast {m[m.slow==0].A.median():+.3f}")
d.to_csv("fast_slow_merged.csv", index=False)
