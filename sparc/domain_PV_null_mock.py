"""DOMAIN PV null: does the PV analysis produce a 'spin signal' from mock galaxies
that obey the frozen formula exactly, with ONLY galaxy-level scatter (no spin physics)?
Vflat in the mock is shifted with the same galaxy offset as g_obs (g ~ V^2), i.e. the
circularity in the real test is reproduced. If mock partial rho ~ real, PV's PASS is an artifact."""
import json, numpy as np
from scipy.stats import rankdata
J = json.load(open("domain_PV_results.json"))
rows = J["galaxies"]; rng = np.random.default_rng(7)
r_real = np.array([x["r"] for x in rows]); sig = r_real.std()
ctrl = np.column_stack([[x["lgb"] for x in rows], [x["lL"] for x in rows]])
def pspear(x, y, Z):
    rx, ry = rankdata(x), rankdata(y); Zr = np.column_stack([rankdata(z) for z in Z.T]+[np.ones(len(x))])
    ex = rx-Zr@np.linalg.lstsq(Zr,rx,rcond=None)[0]; ey = ry-Zr@np.linalg.lstsq(Zr,ry,rcond=None)[0]
    return np.corrcoef(ex,ey)[0,1]
om_true = np.array([x["omega"] for x in rows]); vf_true = np.array([x["vflat"] for x in rows])
# remove the observed offset from the real Vflat to get a 'formula' Vflat, then re-add mock noise
vf_formula = vf_true/10**(r_real/2); om_formula = om_true/10**(r_real/2)
res = {"omega": [], "vflat": []}
for _ in range(2000):
    d = rng.normal(0, sig, len(rows))
    res["omega"].append(pspear(om_formula*10**(d/2), d, ctrl)); res["vflat"].append(pspear(vf_formula*10**(d/2), d, ctrl))
for k, real in [("omega", J["results"]["omega"]["partial_rho"]), ("vflat", J["results"]["vflat"]["partial_rho"])]:
    a = np.array(res[k]); print(f"{k:6s} real partial rho {real:+.3f} | mock (no spin physics) mean {a.mean():+.3f}, 95% range {np.percentile(a,2.5):+.3f}..{np.percentile(a,97.5):+.3f} | frac mock >= real: {(a>=real).mean():.3f}")
