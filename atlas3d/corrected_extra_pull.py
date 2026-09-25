"""CORRECTION (2026-09-25): the spin and heat tests used logML_star from Paper XX, which is the JAM M/L times (1 - f_DM)
(dynamical, not from starlight). Correct extra-pull measure: C = log(M/L)_JAM - log(M/L)_Salp (dynamics vs stellar-population
M/L from the light, Salpeter IMF). Same frozen predictions (PREDICTION_fast_slow.md, PREDICTION_heat_age.md), same controls."""
import numpy as np, pandas as pd, re
from scipy import stats
d = pd.read_csv("fast_slow_merged.csv")
c20 = pd.read_csv("Cappellari2013b_Atlas3D_Paper20_Table1.txt", sep=r"\s+", comment="#", header=None)[[0, 4]]; c20.columns = ["gal", "logML_Salp"]
d = d.merge(c20, on="gal"); d["logML_Salp"] = pd.to_numeric(d.logML_Salp, errors="coerce")
d["C"] = d.logML_JAM - d.logML_Salp; d["logMs_pop"] = d.logML_Salp + d.logL
def pairs(f):
    out = {}
    for line in open(f):
        if line.startswith("#") or not line.strip(): continue
        p = re.findall(r"(\S+)\s*\+/-\s*(\S+)", line); out[line.split()[0]] = [v for v, e in p]
    return out
t3 = pairs("McDermid2015_Atlas3D_Paper30_Table3.txt"); t4 = pairs("McDermid2015_Atlas3D_Paper30_Table4.txt")
d["age_ssp"] = d.gal.map(lambda g: float(t3[g][4]) if g in t3 and len(t3[g]) > 4 and t3[g][4] != "--" else np.nan)
d["age_mw"] = d.gal.map(lambda g: float(t4[g][0]) if g in t4 and t4[g][0] != "--" else np.nan)
d = d.dropna(subset=["C"])
def ols(df, cols, y="C"):
    X = np.column_stack([np.ones(len(df))] + [df[c].values for c in cols]); b = np.linalg.lstsq(X, df[y].values, rcond=None)[0]
    r = df[y].values - X @ b; dof = len(df) - X.shape[1]; se = np.sqrt(np.diag(r @ r / dof * np.linalg.inv(X.T @ X))); return b, se, dof
print(f"n = {len(d)}  median C (dyn/pop): slow {d[d.slow==1].C.median():+.3f}  fast {d[d.slow==0].C.median():+.3f}")
b, se, dof = ols(d, ["logMs_pop", "logsig", "slow"]); t = b[3]/se[3]
print(f"SPIN  : slow coefficient {b[3]:+.4f} ± {se[3]:.4f}  t = {t:+.2f}  one-sided p(slow more) = {1-stats.t.cdf(t,dof):.3f}")
b, se, dof = ols(d, ["logMs_pop", "logsig", "lamR"]); t = b[3]/se[3]
print(f"        lambda_R coefficient {b[3]:+.4f} ± {se[3]:.4f}  t = {t:+.2f}  (more rotation -> {'more' if b[3]>0 else 'less'} extra pull)")
for col in ["age_ssp", "age_mw"]:
    x = d.dropna(subset=[col]).copy(); x["la"] = np.log10(x[col].clip(lower=0.1))
    b, se, dof = ols(x, ["logMs_pop", "logsig", "la"]); t = b[3]/se[3]
    print(f"HEAT  : {col}: age coefficient {b[3]:+.4f} ± {se[3]:.4f}  t = {t:+.2f}  one-sided p(older more) = {1-stats.t.cdf(t,dof):.3f}")
x = d.dropna(subset=["age_ssp"]); q = x.age_ssp.quantile([1/3, 2/3]).values
for lbl, s in [("young", x.age_ssp <= q[0]), ("middle", (x.age_ssp > q[0]) & (x.age_ssp <= q[1])), ("old", x.age_ssp > q[1])]:
    print(f"   {lbl:6s}: n={s.sum():>3}  median age {x[s].age_ssp.median():5.1f}  median C {x[s].C.median():+.3f}")
