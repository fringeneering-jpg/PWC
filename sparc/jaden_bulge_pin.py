"""Bulge-pinned tension test (prediction frozen in predictions/bulge_pin.md).

pin = 0.7*Vbul^2/Vbar^2 (bulge share of normal pull), U = |g_in-g_out|/(g_in+g_out) (ring term).
A: T = max(pin, U)   B: T = pin
g_pred = g_bar + sqrt(a0*g_bar)*[1 + s*T]; a0, s fitted on training galaxies only.
Jaden's verified pipeline and galaxy-balanced metric; same 10 seeds, 70/30.
"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, json
from scipy.optimize import minimize, minimize_scalar
exec(open("jaden_tension_differential.py", encoding="utf-8").read().split("model = lambda")[0])  # data + g_in/g_out rings
UPS_D, UPS_B = 0.5, 0.7
vb2 = UPS_B * data.Vbul * np.abs(data.Vbul)
vbar2 = data.Vgas * np.abs(data.Vgas) + UPS_D * data.Vdisk * np.abs(data.Vdisk) + vb2
data["pin"] = np.clip(vb2 / vbar2, 0, 1)
data["U"] = np.abs(data.gin - data.gout) / (data.gin + data.gout)
data["tA"] = np.maximum(data.pin, data.U)
data["tB"] = data.pin
data["tS"] = np.minimum(data.gin, data.gout) / data.gin   # last night's static shared version
bulge = set(data[data.Vbul > 0][mc].unique())

def mk(col): return lambda df, a0, s: df.g_bar.values + np.sqrt(a0 * df.g_bar.values) * (1 + s * df[col].values)
A, B, S = mk("tA"), mk("tB"), mk("tS")
def base(df, a0): return df.g_bar.values * (1 + np.sqrt(a0 / df.g_bar.values))
def rar(df, a0): return df.g_bar.values / (1 - np.exp(-np.sqrt(df.g_bar.values / a0)))
def pts(df, pred): return np.sqrt(np.mean((np.log10(df.g_obs) - np.log10(np.maximum(pred, 1e-300))) ** 2))
def galm(df, f): return df.groupby(mc).apply(lambda d: pts(d, f(d)), include_groups=False).mean()
def fit1(df, f): return 10 ** minimize_scalar(lambda la: pts(df, f(df, 10 ** la)), bounds=(-13, -8), method="bounded", options={"xatol": 1e-12}).x
def fit2(df, f):
    r = minimize(lambda p: pts(df, f(df, 10 ** p[0], p[1])), x0=[np.log10(7.56e-11), 0.0], method="Nelder-Mead",
                 options=dict(xatol=1e-9, fatol=1e-12, maxiter=8000))
    return 10 ** r.x[0], r.x[1]

print(f"bulge galaxies: {len(bulge)} of {data[mc].nunique()}")
q = data.groupby(mc).Rad.transform(lambda x: (x.rank() - 1) / (len(x) - 1))
for lo, hi in [(0, .2), (.2, .4), (.4, .6), (.6, .8), (.8, 1.01)]:
    m = (q >= lo) & (q < hi); mb = m & data[mc].isin(bulge)
    print(f"   radius {lo:.1f}-{hi:.1f}: median T_A all {data.tA[m].median():.2f} | bulge gals T_A {data.tA[mb].median():.2f}  T_B {data.tB[mb].median():.2f}")

F = {}
for k, f in [("A", A), ("B", B), ("S", S)]: F[k] = fit2(data, f)
ab, ar = fit1(data, base), fit1(data, rar)
print(f"\nFULL SAMPLE: A s={F['A'][1]:+.4f} a0={F['A'][0]:.4e} | B s={F['B'][1]:+.4f} a0={F['B'][0]:.4e}")
print(f"   A {galm(data, lambda d: A(d, *F['A'])):.5f} | B {galm(data, lambda d: B(d, *F['B'])):.5f} | static shared {galm(data, lambda d: S(d, *F['S'])):.5f} | base {galm(data, lambda d: base(d, ab)):.5f} | McGaugh {galm(data, lambda d: rar(d, ar)):.5f}")

gals = np.array(sorted(data[mc].unique())); R = []
for sd in [7, 1, 2, 3, 4, 5, 6, 8, 9, 10]:
    g = gals.copy(); np.random.default_rng(sd).shuffle(g); n = int(len(g) * 0.7)
    tr, ho = data[data[mc].isin(g[:n])], data[data[mc].isin(g[n:])]
    fa, fb, fs = fit2(tr, A), fit2(tr, B), fit2(tr, S); b1, r1 = fit1(tr, base), fit1(tr, rar)
    R.append([sd, fa[1], fb[1], galm(ho, lambda d: A(d, *fa)), galm(ho, lambda d: B(d, *fb)),
              galm(ho, lambda d: S(d, *fs)), galm(ho, lambda d: base(d, b1)), galm(ho, lambda d: rar(d, r1))])
R = np.array(R)
print(f"\nHOLDOUT s_A per split: {', '.join(f'{x:+.3f}' for x in R[:,1])}")
print(f"HOLDOUT s_B per split: {', '.join(f'{x:+.3f}' for x in R[:,2])}")
print(f"   mean: A {R[:,3].mean():.4f} | B {R[:,4].mean():.4f} | static shared {R[:,5].mean():.4f} | base {R[:,6].mean():.4f} | McGaugh {R[:,7].mean():.4f}")
for i, k in [(3, "A"), (4, "B")]:
    print(f"   {k} beats base {int((R[:,i]<R[:,6]).sum())}/10 | beats static {int((R[:,i]<R[:,5]).sum())}/10 | beats McGaugh {int((R[:,i]<R[:,7]).sum())}/10")

t1 = pd.read_csv("vizier_t1.txt", sep=r'\t+', comment='#', engine='python', on_bad_lines='skip'); t1.columns = [c.strip() for c in t1.columns]
t1["Type"] = pd.to_numeric(t1["Type"], errors="coerce"); ty = dict(zip(t1["Name"].str.strip(), t1["Type"]))
lab = {**{t: "early spiral Sa-Sb" for t in [0,1,2,3]}, **{t: "late spiral Sbc-Sd" for t in [4,5,6,7]}, **{t: "Magellanic Sm" for t in [8,9]}, **{t: "irregular/BCD dwarfs" for t in [10,11]}}
rows = [dict(name=n.strip(), bul=n in bulge, cls=lab.get(ty.get(n.strip())), A=pts(d, A(d, *F["A"])), B=pts(d, B(d, *F["B"])),
             S=pts(d, S(d, *F["S"])), base=pts(d, base(d, ab)), M=pts(d, rar(d, ar))) for n, d in data.groupby(mc)]
df = pd.DataFrame(rows)
print("\nBY TYPE (full sample):")
for c, g in df.groupby("cls"): print(f"   {c:22s} n={len(g):>3}  A {g.A.mean():.4f}  B {g.B.mean():.4f}  static {g.S.mean():.4f}  base {g.base.mean():.4f}  McGaugh {g.M.mean():.4f}")
for lbl, g in [("BULGE galaxies", df[df.bul]), ("no-bulge galaxies", df[~df.bul])]:
    print(f"   {lbl:22s} n={len(g):>3}  A {g.A.mean():.4f}  B {g.B.mean():.4f}  static {g.S.mean():.4f}  base {g.base.mean():.4f}  McGaugh {g.M.mean():.4f}  | A beats base {int((g.A<g.base).sum())}/{len(g)}  B beats base {int((g.B<g.base).sum())}/{len(g)}")
json.dump(dict(full={k: list(v) for k, v in F.items()}, holdout_cols="seed,sA,sB,A,B,static,base,McGaugh", holdout=R.tolist()),
          open("jaden_bulge_pin_results.json", "w"), indent=1)
