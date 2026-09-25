"""Jaden's tension-differential model (approved 2026-09-25).

g_pred = g_bar + sqrt(a0 * Delta),   Delta = g_bar * (g_in - g_out)/g_in  (clipped at 0)

- g_bar : normal Newtonian baryonic pull, untouched (SPARC, fixed M/L 0.5/0.7 as in Jaden's pipeline).
- The medium has mass. The star pulls on the medium on both sides; the outer side gives freely,
  the inner side is also pulled by the inner masses -> tension. Net one-sided tension = Delta.
- g_in  : in-plane pull at R from all mass rings inside R.
- g_out : in-plane outward pull at R from all mass rings outside R (spiral edge -> ~0; centre -> large).
- Rings: from each galaxy's measured profile, M(<R_i) = Vbar^2 R / G, ring mass = difference
  (negative increments clipped to 0), each ring placed at the midpoint between radii; thin-ring
  potential via complete elliptic integral, fixed disk thickness h = 0.2 kpc (not fitted).
- Scoring: Jaden's verified pipeline (reproduces 0.13273) and his galaxy-balanced metric.
  One fitted constant a0 (training galaxies only on splits), same as McGaugh.
"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, json
from scipy.optimize import minimize_scalar
from scipy.special import ellipk

src = open("void_push_zero_param_pipeline.py", encoding="utf-8").read()
head = src.split("# Execute with local files")[0]; exec(head[head.rfind("def load_and_filter_sparc"):])
data, _, mc = load_and_filter_sparc("vizier_t1.txt", "vizier_t2.txt")
G = 4.30091e-6                      # kpc (km/s)^2 / Msun
CONV = 1e6 / 3.0856775814913673e19  # (km/s)^2/kpc -> m/s^2
H = 0.2                             # kpc, fixed disk thickness

def ring_pot(r, a, m):
    s = (a + r) ** 2 + H ** 2; k2 = 4 * a * r / s
    return -(2 * G * m / np.pi) * ellipk(k2) / np.sqrt(s)

def ring_gr(r, a, m, dr=1e-3):     # radial accel (km/s)^2/kpc, + = outward
    return -(ring_pot(r + dr, a, m) - ring_pot(r - dr, a, m)) / (2 * dr)

parts = []
for name, d in data.groupby(mc):
    d = d.sort_values("Rad").copy()
    R = d["Rad"].values; gb = d["g_bar"].values / CONV
    M = np.maximum(gb * R ** 2 / G, 0)
    dm = np.clip(np.diff(np.concatenate([[0.0], M])), 0, None)
    a = np.concatenate([[R[0] / 2], (R[1:] + R[:-1]) / 2])
    gin = np.zeros_like(R); gout = np.zeros_like(R)
    for j, r in enumerate(R):
        gr = ring_gr(r, a, dm)
        gin[j] = -gr[a < r].sum()          # inner rings pull inward
        gout[j] = gr[a > r].sum()          # outer rings pull outward
    # magnitude from measured g_bar; ring geometry supplies only the one-sidedness fraction
    # (fix: spherical->ring mass reconstruction inflated g_in by 30-65%, so absolute ring pulls are not used)
    d["Delta"] = d["g_bar"].values * np.clip((gin - gout) / gin, 0, None)
    d["gin"] = gin * CONV; d["gout"] = gout * CONV
    parts.append(d)
data = pd.concat(parts)

model = lambda df, a0: df.g_bar.values + np.sqrt(a0 * df.Delta.values)
rar = lambda df, a0: df.g_bar.values / (1 - np.exp(-np.sqrt(df.g_bar.values / a0)))
def pts(df, f, a0): return np.sqrt(np.mean((np.log10(df.g_obs) - np.log10(f(df, a0))) ** 2))
def galm(df, f, a0): return df.groupby(mc).apply(lambda d: pts(d, f, a0), include_groups=False).mean()
def fit(df, f): return 10 ** minimize_scalar(lambda la: pts(df, f, 10 ** la), bounds=(-13, -8), method="bounded", options={"xatol": 1e-12}).x

a_m, a_r = fit(data, model), fit(data, rar)
print(f"sanity: median g_out/g_in in outer third of disks = {np.median((data.gout/data.gin)[data.groupby(mc).Rad.transform(lambda x: x >= x.quantile(0.67))]):.3f}, inner third = {np.median((data.gout/data.gin)[data.groupby(mc).Rad.transform(lambda x: x <= x.quantile(0.33))]):.3f}")
print(f"FULL SAMPLE: tension-differential a0={a_m:.4e} -> {galm(data, model, a_m):.5f} | McGaugh a0={a_r:.4e} -> {galm(data, rar, a_r):.5f}")

gals = np.array(sorted(data[mc].unique())); Rr = []
for s in [7, 1, 2, 3, 4, 5, 6, 8, 9, 10]:
    g = gals.copy(); np.random.default_rng(s).shuffle(g); n = int(len(g) * 0.7)
    tr, ho = data[data[mc].isin(g[:n])], data[data[mc].isin(g[n:])]
    Rr.append([s, galm(ho, model, fit(tr, model)), galm(ho, rar, fit(tr, rar))])
Rr = np.array(Rr)
print(f"HOLDOUT (10 splits): tension-differential {Rr[:,1].mean():.4f} | McGaugh {Rr[:,2].mean():.4f} | wins {int((Rr[:,1] < Rr[:,2]).sum())}/10")
for r in Rr: print(f"   seed {int(r[0]):>2}: tension-diff {r[1]:.4f}  McGaugh {r[2]:.4f}")

t1 = pd.read_csv("vizier_t1.txt", sep=r'\t+', comment='#', engine='python', on_bad_lines='skip'); t1.columns = [c.strip() for c in t1.columns]
t1["Type"] = pd.to_numeric(t1["Type"], errors="coerce"); ty = dict(zip(t1["Name"].str.strip(), t1["Type"]))
lab = {**{t: "early spiral Sa-Sb" for t in [0,1,2,3]}, **{t: "late spiral Sbc-Sd" for t in [4,5,6,7]}, **{t: "Magellanic Sm" for t in [8,9]}, **{t: "irregular/BCD dwarfs" for t in [10,11]}}
rows = [dict(cls=lab.get(ty.get(n.strip())), T=pts(d, model, a_m), M=pts(d, rar, a_r)) for n, d in data.groupby(mc)]
df = pd.DataFrame(rows)
print("BY TYPE (full sample):")
for c, g in df.groupby("cls"): print(f"   {c:22s} n={len(g):>3}  tension-diff {g['T'].mean():.4f}  McGaugh {g.M.mean():.4f}  wins {int((g['T'] < g.M).sum())}/{len(g)}")
json.dump(dict(a0=a_m, full=float(galm(data, model, a_m)), holdout=Rr.tolist()), open("jaden_tension_differential_results.json", "w"), indent=1)
