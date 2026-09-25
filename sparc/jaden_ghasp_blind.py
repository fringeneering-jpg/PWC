"""GHASP spirals blind test (prediction frozen in predictions/ghasp_blind.md, commit 99f5812).
All constants locked from SPARC; nothing refitted. Data from ghasp_build.py.
"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, json
exec(open("jaden_tension_differential.py", encoding="utf-8").read().split("parts = []")[0])  # ring_gr, G, CONV (no SPARC data needed)
S, A = 0.2264, 6.6776e-11; A_BASE, A_RAR = 7.5586e-11, 1.1603e-10
d = pd.read_csv("ghasp/ghasp_accel.csv")
parts = []
for n, g in d.groupby("Name"):
    g = g.sort_values("Rad").copy(); R = g.Rad.values; gb = g.g_bar.values / CONV
    M = np.maximum(gb * R ** 2 / G, 0); dm = np.clip(np.diff(np.concatenate([[0.0], M])), 0, None)
    a = np.concatenate([[R[0] / 2], (R[1:] + R[:-1]) / 2])
    gin = np.array([-ring_gr(r, a, dm)[a < r].sum() for r in R]); gout = np.array([ring_gr(r, a, dm)[a > r].sum() for r in R])
    g["shared"] = np.clip(np.minimum(gin, gout) / np.where(gin > 0, gin, np.nan), 0, 1); g["shared"] = g.shared.fillna(0)
    parts.append(g)
d = pd.concat(parts)
pts = lambda go, gp: np.sqrt(np.mean((np.log10(go) - np.log10(gp)) ** 2))
pwc = lambda g, s: g.g_bar + np.sqrt(A * g.g_bar) * (1 + s * g.shared * (1 - g.locked))
rows = []
for n, g in d.groupby("Name"):
    rows.append(dict(name=n, type=g.Type.iloc[0], bulge=bool(g.locked.max() > 0), npts=len(g),
                     PWC=pts(g.g_obs, pwc(g, S)), PWC_s0=pts(g.g_obs, pwc(g, 0.0)),
                     base=pts(g.g_obs, g.g_bar * (1 + np.sqrt(A_BASE / g.g_bar))),
                     McGaugh=pts(g.g_obs, g.g_bar / (1 - np.exp(-np.sqrt(g.g_bar / A_RAR))))))
r = pd.DataFrame(rows)
def line(lbl, x):
    print(f"   {lbl:18s} n={len(x):>2}  PWC {x.PWC.mean():.4f} | PWC s=0 {x.PWC_s0.mean():.4f} | base {x.base.mean():.4f} | McGaugh {x.McGaugh.mean():.4f}"
          f"  || PWC beats base {int((x.PWC<x.base).sum())}/{len(x)}, beats McGaugh {int((x.PWC<x.McGaugh).sum())}/{len(x)}, tension helps {int((x.PWC<x.PWC_s0).sum())}/{len(x)}")
print("GHASP blind (galaxy-balanced RMS, lower = better):")
line("ALL", r); line("bulge galaxies", r[r.bulge]); line("no bulge", r[~r.bulge])
print(f"   gap to McGaugh (all): {100*(r.PWC.mean()/r.McGaugh.mean()-1):+.1f}%  (SPARC +1.3%)")
print(f"   median shared {d.shared.median():.2f}, median locked {d.locked.median():.2f}")
json.dump(dict(locked=dict(s=S, a0=A, a0_base=A_BASE, a0_rar=A_RAR), galaxies=rows), open("jaden_ghasp_blind_results.json", "w"), indent=1)
