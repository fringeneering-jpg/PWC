"""PROBES M/L robustness (prediction frozen in predictions/probes_ml_robustness.md).
g_bar scaled by ML/0.5 (stars only); shared unchanged; all constants locked from SPARC."""
import numpy as np, pandas as pd, json
S, A = 0.2264, 6.6776e-11; A_BASE, A_RAR = 7.5586e-11, 1.1603e-10
d0 = pd.read_csv("probes/probes_accel.csv")
pts = lambda go, gp: float(np.sqrt(np.mean((np.log10(go) - np.log10(gp)) ** 2)))
res = {}
for ML in [0.4, 0.5, 0.6]:
    d = d0.assign(g_bar=d0.g_bar * ML / 0.5)
    r = pd.DataFrame([dict(PWC=pts(g.g_obs, g.g_bar + np.sqrt(A * g.g_bar) * (1 + S * g.shared)),
                           s0=pts(g.g_obs, g.g_bar + np.sqrt(A * g.g_bar)),
                           base=pts(g.g_obs, g.g_bar * (1 + np.sqrt(A_BASE / g.g_bar))),
                           M=pts(g.g_obs, g.g_bar / (1 - np.exp(-np.sqrt(g.g_bar / A_RAR))))) for _, g in d.groupby("Name")])
    rng = np.random.default_rng(0); idx = [rng.integers(0, len(r), len(r)) for _ in range(2000)]
    bm = [r.PWC.values[i].mean() - r.M.values[i].mean() for i in idx]
    print(f"M/L {ML}: PWC {r.PWC.mean():.4f} | s=0 {r.s0.mean():.4f} | base {r.base.mean():.4f} | McGaugh {r.M.mean():.4f}"
          f" | gap {100*(r.PWC.mean()/r.M.mean()-1):+.1f}% (95% [{np.percentile(bm,2.5):+.4f},{np.percentile(bm,97.5):+.4f}])"
          f" | beats McGaugh {int((r.PWC<r.M).sum())}/{len(r)}, base {int((r.PWC<r.base).sum())}, tension helps {int((r.PWC<r.s0).sum())}")
    res[ML] = dict(PWC=r.PWC.mean(), s0=r.s0.mean(), base=r.base.mean(), McGaugh=r.M.mean(), ci=[np.percentile(bm,2.5), np.percentile(bm,97.5)])
json.dump(res, open("jaden_probes_ml_robustness_results.json", "w"), indent=1)
