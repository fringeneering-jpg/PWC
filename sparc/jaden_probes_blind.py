"""PROBES blind test (prediction frozen in predictions/probes_blind.md, commit 1a92e41).
All constants locked from SPARC; nothing refitted. Data from probes_build.py.
"""
import numpy as np, pandas as pd, json
S, A = 0.2264, 6.6776e-11; A_BASE, A_RAR = 7.5586e-11, 1.1603e-10
d = pd.read_csv("probes/probes_accel.csv")
pts = lambda go, gp: float(np.sqrt(np.mean((np.log10(go) - np.log10(gp)) ** 2)))
pwc = lambda g, s: g.g_bar + np.sqrt(A * g.g_bar) * (1 + s * g.shared * (1 - g.locked))
rows = [dict(name=n, type=g.Type.iloc[0], survey=g.survey.iloc[0], npts=len(g),
             PWC=pts(g.g_obs, pwc(g, S)), PWC_s0=pts(g.g_obs, pwc(g, 0.0)),
             base=pts(g.g_obs, g.g_bar * (1 + np.sqrt(A_BASE / g.g_bar))),
             McGaugh=pts(g.g_obs, g.g_bar / (1 - np.exp(-np.sqrt(g.g_bar / A_RAR))))) for n, g in d.groupby("Name")]
r = pd.DataFrame(rows)
def line(lbl, x):
    print(f"   {lbl:14s} n={len(x):>4}  PWC {x.PWC.mean():.4f} | s=0 {x.PWC_s0.mean():.4f} | base {x.base.mean():.4f} | McGaugh {x.McGaugh.mean():.4f}"
          f"  || beats base {int((x.PWC<x.base).sum())}, beats McGaugh {int((x.PWC<x.McGaugh).sum())}, tension helps {int((x.PWC<x.PWC_s0).sum())}")
print("PROBES blind (galaxy-balanced RMS, lower = better):"); line("ALL", r)
for t in ["Sa", "Sab", "Sb", "Sbc", "Sc", "Scd", "Sd", "Sm", "Irr"]:
    x = r[r.type.astype(str).str.strip() == t]
    if len(x) >= 15: line(t, x)
print(f"   gap to McGaugh: {100*(r.PWC.mean()/r.McGaugh.mean()-1):+.1f}%  (SPARC +1.3%)")
rng = np.random.default_rng(0); bs = [(lambda i: r.PWC.values[i].mean() - r.McGaugh.values[i].mean())(rng.integers(0, len(r), len(r))) for _ in range(2000)]
bt = [(lambda i: r.PWC.values[i].mean() - r.PWC_s0.values[i].mean())(rng.integers(0, len(r), len(r))) for _ in range(2000)]
print(f"   bootstrap 95% (PWC - McGaugh): [{np.percentile(bs,2.5):+.4f}, {np.percentile(bs,97.5):+.4f}] | (PWC - s=0): [{np.percentile(bt,2.5):+.4f}, {np.percentile(bt,97.5):+.4f}]")
json.dump(dict(locked=dict(s=S, a0=A, a0_base=A_BASE, a0_rar=A_RAR), galaxies=rows), open("jaden_probes_blind_results.json", "w"), indent=1)
