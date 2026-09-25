"""PROBES + ALFALFA gas test (prediction frozen in predictions/probes_gas.md, commit 2bb1108). Constants locked from SPARC."""
import numpy as np, pandas as pd, json
S, A = 0.2264, 6.6776e-11; A_BASE, A_RAR = 7.5586e-11, 1.1603e-10
pts = lambda go, gp: float(np.sqrt(np.mean((np.log10(go) - np.log10(gp)) ** 2)))
res = {}
for lbl, f in [("GAS, M/L 0.5 (predicted)", "probes/gas_ml05.csv"), ("no gas, M/L 0.5", "probes/nogas_ml05.csv"), ("GAS, M/L 0.6", "probes/gas_ml06.csv")]:
    d = pd.read_csv(f)
    r = pd.DataFrame([dict(PWC=pts(g.g_obs, g.g_bar + np.sqrt(A * g.g_bar) * (1 + S * g.shared)), s0=pts(g.g_obs, g.g_bar + np.sqrt(A * g.g_bar)),
                           base=pts(g.g_obs, g.g_bar * (1 + np.sqrt(A_BASE / g.g_bar))),
                           M=pts(g.g_obs, g.g_bar / (1 - np.exp(-np.sqrt(g.g_bar / A_RAR))))) for _, g in d.groupby("Name")])
    rng = np.random.default_rng(0); idx = [rng.integers(0, len(r), len(r)) for _ in range(2000)]
    bm = [r.PWC.values[i].mean() - r.M.values[i].mean() for i in idx]; bb = [r.PWC.values[i].mean() - r.base.values[i].mean() for i in idx]
    print(f"{lbl:26s} n={len(r)}  PWC {r.PWC.mean():.4f} | s=0 {r.s0.mean():.4f} | base {r.base.mean():.4f} | McGaugh {r.M.mean():.4f}\n"
          f"{'':28s}vs McGaugh {100*(r.PWC.mean()/r.M.mean()-1):+.1f}% 95%[{np.percentile(bm,2.5):+.4f},{np.percentile(bm,97.5):+.4f}] wins {int((r.PWC<r.M).sum())}"
          f" | vs base {100*(r.PWC.mean()/r.base.mean()-1):+.1f}% 95%[{np.percentile(bb,2.5):+.4f},{np.percentile(bb,97.5):+.4f}] wins {int((r.PWC<r.base).sum())} | tension helps {int((r.PWC<r.s0).sum())}")
    res[lbl] = dict(PWC=r.PWC.mean(), s0=r.s0.mean(), base=r.base.mean(), McGaugh=r.M.mean())
d = pd.read_csv("probes/gas_ml05.csv"); print(f"median shared with gas {d.shared.median():.2f} vs without {pd.read_csv('probes/nogas_ml05.csv').shared.median():.2f}")
json.dump(res, open("jaden_probes_gas_results.json", "w"), indent=1)
