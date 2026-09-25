"""Colder = denser = thicker: colour test (prediction frozen in PREDICTION_colour_cold.md)."""
import numpy as np, pandas as pd, re, warnings; warnings.filterwarnings("ignore")
from scipy import stats
from astroquery.vizier import Vizier
rc3 = Vizier(columns=["name", "altname", "B-VT", "B-VoT"], row_limit=-1).get_catalogs("VII/155/rc3")[0].to_pandas()
def key(s):
    m = re.match(r"\s*(NGC|IC|UGC|PGC)\s*0*(\d+)", str(s).upper()); return f"{m.group(1)}{int(m.group(2))}" if m else None
col = {}
for _, r in rc3.iterrows():
    v = r["B-VoT"] if pd.notna(r["B-VoT"]) else r["B-VT"]
    if pd.isna(v): continue
    for nm in (r["name"], r["altname"]):
        k = key(nm)
        if k and k not in col: col[k] = float(v)
d = pd.read_csv("fast_slow_merged.csv")
c20 = pd.read_csv("Cappellari2013b_Atlas3D_Paper20_Table1.txt", sep=r"\s+", comment="#", header=None)[[0, 4]]; c20.columns = ["gal", "logML_Salp"]
d = d.merge(c20, on="gal"); d["logML_Salp"] = pd.to_numeric(d.logML_Salp, errors="coerce")
d["C"] = d.logML_JAM - d.logML_Salp; d["logMs_pop"] = d.logML_Salp + d.logL; d["BV"] = d.gal.map(lambda g: col.get(key(g)))
x = d.dropna(subset=["C", "BV"])
print(f"galaxies with colour: {len(x)} of {len(d)}; B-V range {x.BV.min():.2f}-{x.BV.max():.2f}, median {x.BV.median():.2f}")
X = np.column_stack([np.ones(len(x)), x.logMs_pop, x.logsig, x.BV]); b = np.linalg.lstsq(X, x.C.values, rcond=None)[0]
r = x.C.values - X @ b; dof = len(x) - 4; se = np.sqrt(np.diag(r @ r / dof * np.linalg.inv(X.T @ X))); t = b[3] / se[3]
print(f"colour coefficient d = {b[3]:+.4f} ± {se[3]:.4f} per mag of B-V  (t = {t:+.2f}, one-sided p(redder more) = {1-stats.t.cdf(t, dof):.3f})")
print(f"   [log M* {b[1]:+.3f} ± {se[1]:.3f}, log sigma {b[2]:+.3f} ± {se[2]:.3f}]")
q = x.BV.quantile([1/3, 2/3]).values
for lbl, s in [("bluest (warmest)", x.BV <= q[0]), ("middle", (x.BV > q[0]) & (x.BV <= q[1])), ("reddest (coldest)", x.BV > q[1])]:
    print(f"   {lbl:18s}: n={s.sum():>3}  median B-V {x[s].BV.median():.2f}  median C {x[s].C.median():+.3f}  median logM* {x[s].logMs_pop.median():.2f}")
x.to_csv("colour_cold_results.csv", index=False)
