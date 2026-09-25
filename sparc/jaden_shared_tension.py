"""Shared-tension test (prediction frozen at commit aa36854: s > 0).

g_pred = g_bar + sqrt(a0*g_bar) * [1 + s * min(g_in, g_out)/g_in]
Ring geometry (g_in, g_out) from jaden_tension_differential.py; Jaden's verified pipeline and metric.
a0 and s fitted on training galaxies only; s sign free.
"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, json
from scipy.optimize import minimize, minimize_scalar
exec(open("jaden_tension_differential.py", encoding="utf-8").read().split("model = lambda")[0])  # data + g_in/g_out rings
data["tight"] = np.minimum(data.gin, data.gout) / data.gin

def shared(df, a0, s): return df.g_bar.values + np.sqrt(a0 * df.g_bar.values) * (1 + s * df.tight.values)
def base(df, a0): return df.g_bar.values * (1 + np.sqrt(a0 / df.g_bar.values))
def rar(df, a0): return df.g_bar.values / (1 - np.exp(-np.sqrt(df.g_bar.values / a0)))
def pts(df, pred): return np.sqrt(np.mean((np.log10(df.g_obs) - np.log10(np.maximum(pred, 1e-300))) ** 2))
def galm(df, f): return df.groupby(mc).apply(lambda d: pts(d, f(d)), include_groups=False).mean()
def fit1(df, f): return 10 ** minimize_scalar(lambda la: pts(df, f(df, 10 ** la)), bounds=(-13, -8), method="bounded", options={"xatol": 1e-12}).x
def fit2(df):
    r = minimize(lambda p: pts(df, shared(df, 10 ** p[0], p[1])), x0=[np.log10(7.56e-11), 0.0], method="Nelder-Mead",
                 options=dict(xatol=1e-9, fatol=1e-12, maxiter=8000))
    return 10 ** r.x[0], r.x[1]

a_s, s_all = fit2(data); a_b = fit1(data, base); a_r = fit1(data, rar)
print(f"FULL SAMPLE: s = {s_all:+.4f}  (a0={a_s:.4e})")
print(f"   shared-tension {galm(data, lambda d: shared(d, a_s, s_all)):.5f} | base {galm(data, lambda d: base(d, a_b)):.5f} | McGaugh {galm(data, lambda d: rar(d, a_r)):.5f}")

gals = np.array(sorted(data[mc].unique())); R = []
for sd in [7, 1, 2, 3, 4, 5, 6, 8, 9, 10]:
    g = gals.copy(); np.random.default_rng(sd).shuffle(g); n = int(len(g) * 0.7)
    tr, ho = data[data[mc].isin(g[:n])], data[data[mc].isin(g[n:])]
    a, s = fit2(tr); ab = fit1(tr, base); ar = fit1(tr, rar)
    R.append([sd, s, galm(ho, lambda d: shared(d, a, s)), galm(ho, lambda d: base(d, ab)), galm(ho, lambda d: rar(d, ar))])
R = np.array(R)
print(f"\nHOLDOUT: s per split = {', '.join(f'{x:+.3f}' for x in R[:,1])}")
print(f"   mean: shared-tension {R[:,2].mean():.4f} | base {R[:,3].mean():.4f} | McGaugh {R[:,4].mean():.4f}")
print(f"   shared beats base {int((R[:,2]<R[:,3]).sum())}/10 | shared beats McGaugh {int((R[:,2]<R[:,4]).sum())}/10")

t1 = pd.read_csv("vizier_t1.txt", sep=r'\t+', comment='#', engine='python', on_bad_lines='skip'); t1.columns = [c.strip() for c in t1.columns]
t1["Type"] = pd.to_numeric(t1["Type"], errors="coerce"); ty = dict(zip(t1["Name"].str.strip(), t1["Type"]))
lab = {**{t: "early spiral Sa-Sb" for t in [0,1,2,3]}, **{t: "late spiral Sbc-Sd" for t in [4,5,6,7]}, **{t: "Magellanic Sm" for t in [8,9]}, **{t: "irregular/BCD dwarfs" for t in [10,11]}}
rows = [dict(name=n.strip(), cls=lab.get(ty.get(n.strip())), S=pts(d, shared(d, a_s, s_all)), B=pts(d, base(d, a_b)), M=pts(d, rar(d, a_r))) for n, d in data.groupby(mc)]
df = pd.DataFrame(rows)
print("\nBY TYPE (full sample):")
for c, g in df.groupby("cls"): print(f"   {c:22s} n={len(g):>3}  shared {g.S.mean():.4f}  base {g.B.mean():.4f}  McGaugh {g.M.mean():.4f}  shared beats McGaugh {int((g.S<g.M).sum())}/{len(g)}")
print("\n15 galaxies McGaugh fits worst:")
for _, r in df.sort_values("M", ascending=False).head(15).iterrows():
    print(f"   {r['name']:10s} {r['cls']:22s} McGaugh {r.M:.3f}  shared {r.S:.3f}  base {r.B:.3f}")
json.dump(dict(s_full=s_all, a0_full=a_s, holdout=R.tolist()), open("jaden_shared_tension_results.json", "w"), indent=1)
