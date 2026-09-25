"""Heat / viscosity test (prediction frozen in PREDICTION_heat_age.md)."""
import numpy as np, pandas as pd, re
from scipy import stats
d = pd.read_csv("fast_slow_merged.csv")
def mcd(f, col):
    rows = []
    for line in open(f):
        if line.startswith("#") or not line.strip(): continue
        pairs = re.findall(r"(\S+)\s*\+/-\s*(\S+)", line); rows.append((line.split()[0], [v for v, e in pairs]))
    return rows
t3 = mcd("McDermid2015_Atlas3D_Paper30_Table3.txt", None); t4 = mcd("McDermid2015_Atlas3D_Paper30_Table4.txt", None)
age_ssp = {g: float(n[4]) for g, n in t3 if len(n) >= 5 and n[4] != "--"}   # pairs: Hb, Fe5015, Mgb, Fe5270, Age -> index 4
age_mw = {g: float(n[0]) for g, n in t4 if len(n) >= 1 and n[0] != "--"}
d["age_ssp"] = d.gal.map(age_ssp); d["age_mw"] = d.gal.map(age_mw)
print(f"with SSP age: {d.age_ssp.notna().sum()}  with mass-weighted age: {d.age_mw.notna().sum()}  (of {len(d)})")
print(f"age range SSP {d.age_ssp.min():.1f}-{d.age_ssp.max():.1f} Gyr, median {d.age_ssp.median():.1f}")
def ols(df, y, cols):
    X = np.column_stack([np.ones(len(df))] + [df[c].values for c in cols]); b = np.linalg.lstsq(X, df[y].values, rcond=None)[0]
    r = df[y].values - X @ b; dof = len(df) - X.shape[1]; se = np.sqrt(np.diag(r @ r / dof * np.linalg.inv(X.T @ X)))
    return b, se, dof
for agecol in ["age_ssp", "age_mw"]:
    x = d.dropna(subset=[agecol]).copy(); x["logage"] = np.log10(x[agecol].clip(lower=0.1))
    for y in ["A", "fDM"]:
        b, se, dof = ols(x, y, ["logMs", "logsig", "logage"]); t = b[3] / se[3]; p = 1 - stats.t.cdf(t, dof)
        print(f"{agecol:7s} {y:4s}: age coefficient d = {b[3]:+.4f} ± {se[3]:.4f}  (t = {t:+.2f}, one-sided p(d>0) = {p:.3f})  n={len(x)}")
x = d.dropna(subset=["age_ssp"]); q = x.age_ssp.quantile([1/3, 2/3]).values
for lbl, s in [("young third", x.age_ssp <= q[0]), ("middle", (x.age_ssp > q[0]) & (x.age_ssp <= q[1])), ("old third", x.age_ssp > q[1])]:
    print(f"   {lbl:11s}: n={s.sum():>3}  median age {x[s].age_ssp.median():5.1f} Gyr  median A {x[s].A.median():+.3f}  median f_DM {x[s].fDM.median():.3f}  median logM* {x[s].logMs.median():.2f}")
