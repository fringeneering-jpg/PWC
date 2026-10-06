"""
DOMAIN LL -- is there a CORNER at the crossing acceleration, or a smooth blend?

WHY THIS DOMAIN EXISTS, STATED BLUNTLY. Every prior domain in this repository
scored PWC in another theory's units: rms in dex against McGaugh's RAR, a0
against Omega_m and rho_crit, medium spin against Bullock. The best possible
outcome of any of those runs was "ties with MOND", because MOND was the ruler.
That is not a test of this framework. This domain uses a discriminator that
MOND cannot express.

THE PHYSICAL DIFFERENCE BEING TESTED.

  MOND / RAR: an INTERPOLATING FUNCTION. Smooth by construction. There is no
  mechanism in it that can produce a discontinuity -- the whole point of the
  interpolation is that the two regimes blend.

  PWC: the galaxy's restorative phase-tension diffuses outward and weakens.
  The cosmic strain rate does not weaken -- it is a rate, not a position. They
  cross. At the crossing the outward-propagating mode meets an IMPEDANCE STEP
  and reflects. A reflection is an EDGE. It does not blend.

So the two pictures disagree about the SHAPE at the transition, not about
either asymptote. Both agree flat curves need slope 1/2 at low g_bar and
Newton needs slope 1 at high g_bar. Only one of them can put a corner between.

THE TEST IS DELIBERATELY HANDICAPPED AGAINST PWC.

  CORNER model, ZERO free parameters:
      g_obs = sqrt(g_bar * a0)   for g_bar <  a0
      g_obs = g_bar              for g_bar >= a0
    The two branches meet exactly at (a0, a0), so continuity fixes the
    normalisation with nothing left over. The exponent 1/2 is forced by flat
    rotation curves; the exponent 1 is forced by Newton. And a0 is NOT fitted
    here -- it is c0*H0/(2*pi), the crossing of a weakening tension against a
    constant strain rate, with 2*pi because one full topological cycle of a
    phase wave is 2*pi of phase.

  RAR model, ONE free parameter:
      g_obs = g_bar / (1 - exp(-sqrt(g_bar/a0))),  a0 FITTED to this data.

PWC gets zero parameters and an externally-fixed scale. MOND gets one
parameter fitted to the very data being scored. If the corner survives that,
it means something.

SECOND, SHARPER TEST. domain_K_residuals_explore.py found that the RAR-class
fit leaves a MONOTONIC residual trend across g_bar deciles (+0.037 dex in the
deep regime to -0.084 dex near-Newtonian, Spearman -0.27, p=1.5e-47 on 2700
points). That was logged as "transition shape slightly off". A real corner,
absorbed by a smooth function, produces exactly that signature. So the direct
question is: does the corner model REMOVE that trend, or leave it?

If the corner is real, the residual is not noise. It is the signal.

Data: SPARC (Lelli, McGaugh & Schombert 2016), VizieR J/AJ/152/157. Cuts
identical to Domains K and CC. Dark matter halo parameters: 0.

RULE: conclusion text written AFTER the numbers print. Not before.
"""
import json
import os

import numpy as np
from scipy import stats
from scipy.optimize import minimize_scalar

D = os.environ.get("PWC_SPARC_DIR", os.path.dirname(os.path.abspath(__file__)))

KPC = 3.0856775814913673e19
MPC = 3.0856775814913673e22
KMS = 1.0e3
c0 = 2.99792458e8
UPS_D, UPS_B = 0.5, 0.7

H0_PLANCK = 67.4 * KMS / MPC
H0_LOCAL = 73.0 * KMS / MPC

results = {}


def hr(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


def read_vizier_tsv(path, cols):
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8", errors="replace")]
    hdr_i = next(i for i, l in enumerate(lines)
                 if not l.startswith("#") and l.strip() and "\t" in l and "recno" in l)
    names = lines[hdr_i].split("\t")
    dash_i = max(i for i in range(hdr_i + 1, min(hdr_i + 6, len(lines)))
                 if set(lines[i].replace("\t", "").strip()) <= set("- "))
    idx = {c: names.index(c) for c in cols}
    out = {c: [] for c in cols}
    for l in lines[dash_i + 1:]:
        if not l.strip() or l.startswith("#"):
            continue
        f = l.split("\t")
        if len(f) < len(names):
            continue
        try:
            for c in cols:
                v = f[idx[c]].strip()
                out[c].append(v if c == "Name"
                              else (float(v) if v not in ("", "---") else np.nan))
        except ValueError:
            continue
    return out


# ---------------------------------------------------------------- 1
hr("1. DATA AND THE TWO CANDIDATE SHAPES")

t1 = read_vizier_tsv(os.path.join(D, "vizier_t1.txt"),
                     ["Name", "i", "Qual", "Vflat", "Dist", "Rdisk"])
t2 = read_vizier_tsv(os.path.join(D, "vizier_t2.txt"),
                     ["Name", "Rad", "Vobs", "e_Vobs", "Vgas", "Vdisk", "Vbulge"])
inc = dict(zip(t1["Name"], t1["i"]))
qual = dict(zip(t1["Name"], t1["Qual"]))

name = np.array(t2["Name"])
R = np.array(t2["Rad"], float)
Vo = np.array(t2["Vobs"], float)
eVo = np.array(t2["e_Vobs"], float)
Vg = np.nan_to_num(np.array(t2["Vgas"], float))
Vd = np.array(t2["Vdisk"], float)
Vb = np.nan_to_num(np.array(t2["Vbulge"], float))

inc_a = np.array([inc.get(n, np.nan) for n in name], float)
qual_a = np.array([qual.get(n, np.nan) for n in name], float)
m = (R > 0) & (Vo > 0) & np.isfinite(eVo) & (eVo / Vo <= 0.10) & (inc_a >= 30.0) & (qual_a <= 2)
R, Vo, Vg, Vd, Vb, name = R[m], Vo[m], Vg[m], Vd[m], Vb[m], name[m]

conv = (KMS ** 2) / KPC
g_obs = Vo ** 2 / R * conv
Vbar2 = Vg * np.abs(Vg) + UPS_D * Vd * np.abs(Vd) + UPS_B * Vb * np.abs(Vb)
g_bar = Vbar2 / R * conv
ok = (g_bar > 0) & (g_obs > 0)
g_obs, g_bar, name = g_obs[ok], g_bar[ok], name[ok]
y = np.log10(g_obs)
x = np.log10(g_bar)

print("  points: %d   galaxies: %d   halo parameters: 0" % (len(y), len(set(name))))

a0_planck = c0 * H0_PLANCK / (2 * np.pi)
a0_local = c0 * H0_LOCAL / (2 * np.pi)
print("\n  a0 from the crossing, NOT fitted:")
print("    c0*H0/(2pi), Planck H0 67.4 : %.4e m/s^2" % a0_planck)
print("    c0*H0/(2pi), local  H0 73.0 : %.4e m/s^2" % a0_local)


def corner(gb, a0):
    """Zero free parameters once a0 is given. Branches meet exactly at (a0,a0)."""
    return np.where(gb < a0, np.sqrt(gb * a0), gb)


def rar(gb, a0):
    return gb / (1.0 - np.exp(-np.sqrt(gb / a0)))


def rms(pred):
    return float(np.sqrt(np.mean((y - np.log10(pred)) ** 2)))


# ---------------------------------------------------------------- 2
hr("2. HEAD TO HEAD: 0 PARAMETERS vs 1 FITTED PARAMETER")

o = minimize_scalar(lambda la: np.mean((y - np.log10(rar(g_bar, 10 ** la))) ** 2),
                    bounds=(-11.5, -9.0), method="bounded")
a0_rar_fit = 10 ** o.x
rms_rar_fit = rms(rar(g_bar, a0_rar_fit))
rms_newton = rms(g_bar)

oc = minimize_scalar(lambda la: np.mean((y - np.log10(corner(g_bar, 10 ** la))) ** 2),
                     bounds=(-11.5, -9.0), method="bounded")
a0_corner_fit = 10 ** oc.x

rows = [
    ("Newton, baryons only", 0, np.nan, rms_newton),
    ("RAR (smooth), a0 FITTED to this data", 1, a0_rar_fit, rms_rar_fit),
    ("CORNER, a0 = c0*H0/2pi (Planck)", 0, a0_planck, rms(corner(g_bar, a0_planck))),
    ("CORNER, a0 = c0*H0/2pi (local H0)", 0, a0_local, rms(corner(g_bar, a0_local))),
    ("CORNER, a0 fitted (for reference only)", 1, a0_corner_fit, rms(corner(g_bar, a0_corner_fit))),
    ("RAR (smooth), a0 = c0*H0/2pi (local)", 0, a0_local, rms(rar(g_bar, a0_local))),
]
print(f"{'model':<42} {'free':>5} {'a0 [m/s^2]':>12} {'rms [dex]':>10}")
for lab, npar, a0v, r in rows:
    a0s = "--" if not np.isfinite(a0v) else f"{a0v:.4e}"
    print(f"{lab:<42} {npar:>5} {a0s:>12} {r:>10.4f}")
    results[lab] = {"n_free": npar, "a0": None if not np.isfinite(a0v) else float(a0v), "rms": r}

print("\n  Corner (0 params, external a0, local H0) minus RAR (1 fitted param):")
d = rms(corner(g_bar, a0_local)) - rms_rar_fit
print("    %+.4f dex" % d)
results["corner_minus_rar_dex"] = float(d)

# ---------------------------------------------------------------- 3
hr("3. THE DECISIVE TEST: DOES THE CORNER REMOVE DOMAIN K'S RESIDUAL TREND?")

print("domain_K_residuals_explore.py found a monotonic residual trend under a")
print("smooth fit: Spearman rho = -0.27, p = 1.5e-47. If a real corner is being")
print("absorbed by a smooth function, the corner model should REMOVE it.\n")


def trend(pred, label):
    res = y - np.log10(pred)
    rho, p = stats.spearmanr(x, res)
    dec = np.percentile(x, np.arange(0, 101, 10))
    means = []
    for i in range(10):
        s = (x >= dec[i]) & (x <= dec[i + 1] if i == 9 else x < dec[i + 1])
        means.append(float(np.mean(res[s])) if s.sum() else np.nan)
    swing = np.nanmax(means) - np.nanmin(means)
    print(f"  {label:<40} rho={rho:+.4f}  p={p:.2e}  decile swing={swing:.4f} dex")
    return {"spearman_rho": float(rho), "p": float(p), "decile_means": means,
            "decile_swing_dex": float(swing)}


tr = {}
tr["rar_fitted"] = trend(rar(g_bar, a0_rar_fit), "RAR (smooth), a0 fitted")
tr["corner_local"] = trend(corner(g_bar, a0_local), "CORNER, a0 = c0H0/2pi (local)")
tr["corner_fitted"] = trend(corner(g_bar, a0_corner_fit), "CORNER, a0 fitted")
tr["newton"] = trend(g_bar, "Newton (for scale)")
results["residual_trend"] = tr

print("\n  Decile means, low g_bar -> high g_bar:")
print(f"{'decile':>7} {'RAR smooth':>12} {'CORNER':>12}")
for i in range(10):
    print(f"{i:>7} {tr['rar_fitted']['decile_means'][i]:>12.4f} "
          f"{tr['corner_local']['decile_means'][i]:>12.4f}")

# ---------------------------------------------------------------- 4
hr("4. WHERE DOES THE DATA PUT THE CORNER, IF ALLOWED TO CHOOSE?")

print("Scanning the corner location over a wide range and reading off the")
print("minimum. If the data wants a corner at all, it should land near the")
print("predicted crossing rather than anywhere else.\n")
grid = np.linspace(-11.5, -9.0, 251)
curve = np.array([rms(corner(g_bar, 10 ** g)) for g in grid])
best = grid[np.argmin(curve)]
print("  best corner location : %.4e m/s^2  (log10 = %.3f)" % (10 ** best, best))
print("  predicted (local H0) : %.4e m/s^2  (log10 = %.3f)" % (a0_local, np.log10(a0_local)))
print("  ratio best/predicted : %.3f" % (10 ** best / a0_local))

lo = grid[curve <= curve.min() + 0.001]
print("  locations within 0.001 dex of best: %.3e to %.3e" % (10 ** lo.min(), 10 ** lo.max()))
results["corner_best_a0"] = float(10 ** best)
results["corner_best_over_predicted"] = float(10 ** best / a0_local)

# ---------------------------------------------------------------- 5
hr("5. GALAXY-LEVEL HOLDOUT, 40 RANDOM SPLITS (single splits are unreliable)")

gal = np.array(sorted(set(name)))
rng = np.random.default_rng(20260916)
sc = {"newton": [], "rar_fit": [], "corner_ext": []}
for _ in range(40):
    perm = rng.permutation(gal)
    ntr = int(round(0.70 * len(gal)))
    tr_g, te_g = set(perm[:ntr]), set(perm[ntr:])
    itr = np.array([n in tr_g for n in name])
    ite = ~itr
    ytr, xtr = y[itr], g_bar[itr]
    oo = minimize_scalar(lambda la: np.mean((ytr - np.log10(rar(xtr, 10 ** la))) ** 2),
                         bounds=(-11.5, -9.0), method="bounded")
    a0t = 10 ** oo.x
    yte, gte = y[ite], g_bar[ite]
    sc["newton"].append(np.sqrt(np.mean((yte - np.log10(gte)) ** 2)))
    sc["rar_fit"].append(np.sqrt(np.mean((yte - np.log10(rar(gte, a0t))) ** 2)))
    sc["corner_ext"].append(np.sqrt(np.mean((yte - np.log10(corner(gte, a0_local))) ** 2)))

print(f"{'model':<40} {'holdout rms [dex]':>20} {'free params':>12}")
for k, lab, npar in (("newton", "Newton, baryons only", 0),
                     ("rar_fit", "RAR smooth, a0 refit each split", 1),
                     ("corner_ext", "CORNER, a0 = c0H0/2pi, never fitted", 0)):
    a = np.array(sc[k])
    print(f"{lab:<40} {a.mean():>12.4f} +/- {a.std():.4f} {npar:>12}")
    results[f"holdout_{k}"] = {"mean": float(a.mean()), "std": float(a.std())}

wins = int(np.sum(np.array(sc["corner_ext"]) < np.array(sc["rar_fit"])))
print("\n  Corner beats fitted-RAR in %d of 40 splits." % wins)
results["corner_wins_of_40"] = wins

# ---------------------------------------------------------------- 6
hr("6. VERDICT -- written after the numbers, not before")

r_rar = tr["rar_fitted"]
r_cor = tr["corner_local"]
print("1. Pooled fit. Corner with ZERO free parameters and an externally fixed")
print("   a0 lands at %.4f dex; smooth RAR with a0 FITTED to this same data"
      % rms(corner(g_bar, a0_local)))
print("   lands at %.4f dex. Difference %+.4f dex."
      % (rms_rar_fit, d))
print()
print("2. Residual trend. RAR leaves Spearman %+.4f (p=%.1e, swing %.4f dex)."
      % (r_rar["spearman_rho"], r_rar["p"], r_rar["decile_swing_dex"]))
print("   Corner leaves Spearman %+.4f (p=%.1e, swing %.4f dex)."
      % (r_cor["spearman_rho"], r_cor["p"], r_cor["decile_swing_dex"]))
if abs(r_cor["spearman_rho"]) < abs(r_rar["spearman_rho"]):
    print("   The corner REDUCES the trend by %.1f%% in rho and %.1f%% in swing."
          % (100 * (1 - abs(r_cor["spearman_rho"]) / abs(r_rar["spearman_rho"])),
             100 * (1 - r_cor["decile_swing_dex"] / r_rar["decile_swing_dex"])))
else:
    print("   The corner does NOT reduce the trend. It is %.1f%% larger in rho."
          % (100 * (abs(r_cor["spearman_rho"]) / abs(r_rar["spearman_rho"]) - 1)))
print()
print("3. Free corner location. Data puts it at %.3e; prediction is %.3e;"
      % (10 ** best, a0_local))
print("   ratio %.3f." % (10 ** best / a0_local))
print()
print("4. Holdout, 40 splits. Corner (0 params, never fitted) %.4f +/- %.4f;"
      % (np.mean(sc["corner_ext"]), np.std(sc["corner_ext"])))
print("   RAR (1 param, refit every split) %.4f +/- %.4f. Corner wins %d/40."
      % (np.mean(sc["rar_fit"]), np.std(sc["rar_fit"]), wins))
print()
print("5. WHAT THIS DOMAIN DOES NOT CLAIM. rms is still a goodness-of-fit")
print("   number and both models are being scored on the same plane, which is")
print("   built from a Newtonian g_bar. The genuinely non-borrowed part is the")
print("   SHAPE question in section 3: a smooth interpolation cannot produce a")
print("   corner, so whichever model kills the residual trend is the one with")
print("   the right transition. That question does not need MOND as a ruler.")

out = os.path.join(D, "domain_LL_reflection_edge_results.json")
with open(out, "w") as f:
    json.dump(results, f, indent=2, sort_keys=True)
print(f"\nwrote {out}")
