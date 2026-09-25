"""One-material rebound test (prediction frozen in predictions/rebound.md).

available = shared * (1 - locked)
  shared = min(g_in, g_out)/g_in   (radial load from both sides; ring geometry as in jaden_tension_differential.py)
  locked = 0.7*Vbul^2/Vbar^2       (bulge share of normal pull = medium already maxed)
Main (1 constant a0): g_pred = g_bar + sqrt(a0*g_bar) * [1 + available]   -- s = 1, full rebound to rest state
Check (2 constants):  same with s fitted freely.
Jaden's verified pipeline and galaxy-balanced metric; same 10 seeds, 70/30.
"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, json
from scipy.optimize import minimize, minimize_scalar
exec(open("jaden_tension_differential.py", encoding="utf-8").read().split("model = lambda")[0])  # data + g_in/g_out rings
UPS_D, UPS_B = 0.5, 0.7
vb2 = UPS_B * data.Vbul * np.abs(data.Vbul)
vbar2 = data.Vgas * np.abs(data.Vgas) + UPS_D * data.Vdisk * np.abs(data.Vdisk) + vb2
data["locked"] = np.clip(vb2 / vbar2, 0, 1)
data["shared"] = np.minimum(data.gin, data.gout) / data.gin
data["avail"] = data.shared * (1 - data.locked)
bulge = set(data[data.Vbul > 0][mc].unique())

def reb(df, a0, s=1.0): return df.g_bar.values + np.sqrt(a0 * df.g_bar.values) * (1 + s * df.avail.values)
def shr(df, a0, s): return df.g_bar.values + np.sqrt(a0 * df.g_bar.values) * (1 + s * df.shared.values)
def base(df, a0): return df.g_bar.values * (1 + np.sqrt(a0 / df.g_bar.values))
def rar(df, a0): return df.g_bar.values / (1 - np.exp(-np.sqrt(df.g_bar.values / a0)))
def pts(df, pred): return np.sqrt(np.mean((np.log10(df.g_obs) - np.log10(np.maximum(pred, 1e-300))) ** 2))
def galm(df, f): return df.groupby(mc).apply(lambda d: pts(d, f(d)), include_groups=False).mean()
def fit1(df, f): return 10 ** minimize_scalar(lambda la: pts(df, f(df, 10 ** la)), bounds=(-13, -8), method="bounded", options={"xatol": 1e-12}).x
def fit2(df, f):
    r = minimize(lambda p: pts(df, f(df, 10 ** p[0], p[1])), x0=[np.log10(7.56e-11), 0.0], method="Nelder-Mead",
                 options=dict(xatol=1e-9, fatol=1e-12, maxiter=8000))
    return 10 ** r.x[0], r.x[1]

q = data.groupby(mc).Rad.transform(lambda x: (x.rank() - 1) / (len(x) - 1))
print("median available by radius (all | bulge galaxies):")
for lo, hi in [(0, .2), (.2, .4), (.4, .6), (.6, .8), (.8, 1.01)]:
    m = (q >= lo) & (q < hi); mb = m & data[mc].isin(bulge)
    print(f"   {lo:.1f}-{hi:.1f}: {data.avail[m].median():.2f} | {data.avail[mb].median():.2f}")

a1 = fit1(data, reb); aF, sF = fit2(data, reb); aS, sS = fit2(data, shr); ab, ar = fit1(data, base), fit1(data, rar)
print(f"\nFULL SAMPLE: rebound s=1 a0={a1:.4e} | free-s check s={sF:+.4f} a0={aF:.4e}")
print(f"   rebound(s=1) {galm(data, lambda d: reb(d, a1)):.5f} | free-s {galm(data, lambda d: reb(d, aF, sF)):.5f} | shared-only {galm(data, lambda d: shr(d, aS, sS)):.5f} | base {galm(data, lambda d: base(d, ab)):.5f} | McGaugh {galm(data, lambda d: rar(d, ar)):.5f}")

gals = np.array(sorted(data[mc].unique())); R = []
for sd in [7, 1, 2, 3, 4, 5, 6, 8, 9, 10]:
    g = gals.copy(); np.random.default_rng(sd).shuffle(g); n = int(len(g) * 0.7)
    tr, ho = data[data[mc].isin(g[:n])], data[data[mc].isin(g[n:])]
    r1 = fit1(tr, reb); rf = fit2(tr, reb); rs = fit2(tr, shr); b1 = fit1(tr, base); m1 = fit1(tr, rar)
    R.append([sd, rf[1], galm(ho, lambda d: reb(d, r1)), galm(ho, lambda d: reb(d, *rf)), galm(ho, lambda d: shr(d, *rs)),
              galm(ho, lambda d: base(d, b1)), galm(ho, lambda d: rar(d, m1))])
R = np.array(R)
print(f"\nHOLDOUT free s per split: {', '.join(f'{x:+.3f}' for x in R[:,1])}")
print(f"   mean: rebound(s=1) {R[:,2].mean():.4f} | free-s {R[:,3].mean():.4f} | shared-only {R[:,4].mean():.4f} | base {R[:,5].mean():.4f} | McGaugh {R[:,6].mean():.4f}")
print(f"   rebound(s=1) beats base {int((R[:,2]<R[:,5]).sum())}/10 | beats shared-only {int((R[:,2]<R[:,4]).sum())}/10 | beats McGaugh {int((R[:,2]<R[:,6]).sum())}/10")

t1 = pd.read_csv("vizier_t1.txt", sep=r'\t+', comment='#', engine='python', on_bad_lines='skip'); t1.columns = [c.strip() for c in t1.columns]
t1["Type"] = pd.to_numeric(t1["Type"], errors="coerce"); ty = dict(zip(t1["Name"].str.strip(), t1["Type"]))
lab = {**{t: "early spiral Sa-Sb" for t in [0,1,2,3]}, **{t: "late spiral Sbc-Sd" for t in [4,5,6,7]}, **{t: "Magellanic Sm" for t in [8,9]}, **{t: "irregular/BCD dwarfs" for t in [10,11]}}
rows = [dict(bul=n in bulge, cls=lab.get(ty.get(n.strip())), R1=pts(d, reb(d, a1)), RF=pts(d, reb(d, aF, sF)), S=pts(d, shr(d, aS, sS)),
             B=pts(d, base(d, ab)), M=pts(d, rar(d, ar))) for n, d in data.groupby(mc)]
df = pd.DataFrame(rows)
print("\nBY TYPE (full sample):")
for c, g in list(df.groupby("cls")) + [("BULGE galaxies", df[df.bul]), ("no-bulge galaxies", df[~df.bul])]:
    print(f"   {c:22s} n={len(g):>3}  rebound(s=1) {g.R1.mean():.4f}  free-s {g.RF.mean():.4f}  shared-only {g.S.mean():.4f}  base {g.B.mean():.4f}  McGaugh {g.M.mean():.4f}  | s=1 beats McGaugh {int((g.R1<g.M).sum())}/{len(g)}")
json.dump(dict(a0_s1=a1, free=[aF, sF], holdout_cols="seed,s_free,rebound_s1,free,shared,base,McGaugh", holdout=R.tolist()),
          open("jaden_rebound_results.json", "w"), indent=1)
