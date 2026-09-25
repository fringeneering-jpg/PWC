"""LITTLE THINGS blind test (prediction frozen in predictions/littlethings_blind.md, commit 3e50156).
Fix after first run: DM-only file uses its own R0.3/V0.3 scaling (first run wrongly used the total-curve scaling).

All constants locked from SPARC; nothing refitted on LITTLE THINGS.
g_obs = Vtot^2/R, g_bar = (Vtot^2 - Vdm^2)/R from Oh+2015 rotdmbar/rotdm "Data" rows (de-scaled).
Model: g_bar + sqrt(a0*g_bar)*[1 + s*shared*(1-locked)], locked = 0 (no bulges), shared from same ring code.
"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, json
from scipy.optimize import minimize_scalar
exec(open("jaden_tension_differential.py", encoding="utf-8").read().split("model = lambda")[0])  # SPARC data, ring_gr, G, CONV
S_LOCK, A_LOCK = 0.2264, 6.6776e-11
def rar(gb, a0): return gb / (1 - np.exp(-np.sqrt(gb / a0)))
def pts(go, gp): return np.sqrt(np.mean((np.log10(go) - np.log10(gp)) ** 2))
fit = lambda f: 10 ** minimize_scalar(lambda la: pts(data.g_obs.values, f(data.g_bar.values, 10 ** la)), bounds=(-13, -8), method="bounded", options={"xatol": 1e-12}).x
A_BASE = fit(lambda gb, a: gb * (1 + np.sqrt(a / gb))); A_RAR = fit(rar)
print(f"locked from SPARC: s={S_LOCK} a0={A_LOCK:.4e} | base a0={A_BASE:.4e} | McGaugh a0={A_RAR:.4e}")

cols = [(0, 8), (9, 14), (15, 23), (24, 34), (35, 44), (45, 54), (55, 63)]
names = ["Name", "Type", "R03", "V03", "R", "V", "eV"]
tot = pd.read_fwf("littlethings/lt_rotdmbar.dat", colspecs=cols, names=names)
dm = pd.read_fwf("littlethings/lt_rotdm.dat", colspecs=cols, names=names)
tot, dm = tot[tot.Type == "Data"], dm[dm.Type == "Data"]
EXCL = {"DDO_50", "DDO_87", "DDO_126", "DDO_154", "DDO_168", "NGC_2366"}
rows = []; dropped = {}
for n, t in tot.groupby("Name"):
    if n in EXCL: continue
    d = dm[dm.Name == n]
    # each file is scaled by its OWN R0.3, V0.3 -> de-scale separately, then put DM on the total-curve radii
    if d.empty: print(f"   skip {n}: no DM-only curve in catalogue"); continue
    t = t.sort_values("R"); d = d.sort_values("R")
    R = t.R.values * t.R03.values; Vt = t.V.values * t.V03.values
    Rd = d.R.values * d.R03.values; Vdd = d.V.values * d.V03.values
    Vd = np.interp(R, Rd, Vdd, left=np.nan, right=np.nan)
    vb2 = Vt ** 2 - Vd ** 2; ok = np.isfinite(vb2) & (vb2 > 0) & (R > 0) & (Vt > 0)
    dropped[n] = int((~ok).sum()); R, Vt, vb2 = R[ok], Vt[ok], vb2[ok]
    if len(R) < 3: print(f"   skip {n}: {len(R)} usable points"); continue
    gb = vb2 / R                                  # (km/s)^2/kpc
    M = np.maximum(gb * R ** 2 / G, 0); dmr = np.clip(np.diff(np.concatenate([[0.0], M])), 0, None)
    a = np.concatenate([[R[0] / 2], (R[1:] + R[:-1]) / 2])
    gin = np.array([-ring_gr(r, a, dmr)[a < r].sum() for r in R]); gout = np.array([ring_gr(r, a, dmr)[a > r].sum() for r in R])
    shared = np.clip(np.minimum(gin, gout) / gin, 0, 1)
    go, gbs = Vt ** 2 / R * CONV, gb * CONV
    P = gbs + np.sqrt(A_LOCK * gbs) * (1 + S_LOCK * shared)
    B = gbs * (1 + np.sqrt(A_BASE / gbs)); Mg = rar(gbs, A_RAR)
    rows.append(dict(name=n, npts=len(R), dropped=dropped[n], PWC=pts(go, P), base=pts(go, B), McGaugh=pts(go, Mg),
                     med_shared=float(np.median(shared)), med_logratio=float(np.median(np.log10(go / gbs)))))
df = pd.DataFrame(rows)
pd.set_option("display.width", 200); print(df.round(3).to_string(index=False))
print(f"\n{len(df)} galaxies, {df.npts.sum()} points")
print(f"galaxy-balanced: PWC {df.PWC.mean():.4f} | base {df.base.mean():.4f} | McGaugh {df.McGaugh.mean():.4f}")
print(f"PWC beats base {int((df.PWC<df.base).sum())}/{len(df)} | PWC beats McGaugh {int((df.PWC<df.McGaugh).sum())}/{len(df)}")
print(f"gap to McGaugh: {100*(df.PWC.mean()/df.McGaugh.mean()-1):+.1f}%  (SPARC: +1.3%)")
json.dump(dict(locked=dict(s=S_LOCK, a0=A_LOCK, a0_base=A_BASE, a0_rar=A_RAR), galaxies=rows), open("jaden_littlethings_blind_results.json", "w"), indent=1)
