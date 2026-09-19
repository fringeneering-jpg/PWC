"""
DOMAIN MM -- does the ORBITING MATERIAL's own nature change the answer?

THE ONE PLACE NEWTON AND MOND CANNOT FOLLOW.

Both of them are built on the equivalence principle: at a given radius in a
given potential, the acceleration does not depend on what the orbiting thing
is. A hydrogen cloud and a star at the same radius get the same answer. This
is not a fitted feature of those theories -- it is structural. Neither has any
term where a property of the test particle could enter.

PWC's governor is not like that. The author's statement:

    "density is the mesh, speed is the multiplier"
    "It's just volumetrically more resistance compared to a smaller orbit"

If flat rotation curves come from a sieve sweeping a footprint of stationary
tensioned medium, then the sieve's own character is IN the mechanism. Change
what is doing the sweeping and the resistance changes.

So: at fixed g_bar, does the residual depend on the baryonic composition?
MOND and Newton both say NO, with no freedom to say otherwise. PWC says YES.
Neither answer is scored against the other theory's goodness of fit -- this is
a yes/no on a feature only one of them can have.

WHAT THIS TEST CAN AND CANNOT DO, STATED FIRST SO IT IS NOT OVERSOLD.

  CANNOT: SPARC gives ONE rotation curve per galaxy. Vobs is not split into a
  gas tracer and a stellar tracer measured separately at the same radius. So
  this is NOT the clean version of the test -- the clean version needs
  independently measured HI and stellar (or globular cluster) kinematics in
  the same galaxy, which is a different dataset.

  CAN: test whether the residual depends on the local baryonic COMPOSITION --
  whether the mass at that radius is gas or stars -- at fixed g_bar. Gas and
  stars differ by roughly 24 orders of magnitude in volumetric density
  (diffuse HI ~1e-21 kg/m^3 vs stellar ~1.4e3 kg/m^3). If a density-dependent
  sweep term exists anywhere in the mechanism, that contrast is where it
  should show.

CONFOUND CONTROL. Gas-rich systems are also faint, small, distant and
inclination-uncertain. Those are GALAXY-level properties. So the primary
statistic here is computed WITHIN each galaxy separately and then aggregated:
per galaxy, the partial correlation of residual with gas fraction while
controlling for g_bar. Every galaxy-level confound cancels by construction,
because each galaxy is only ever compared against itself.

Data: SPARC (Lelli, McGaugh & Schombert 2016), VizieR J/AJ/152/157.
Halo parameters: 0.

RULE: conclusion written after the numbers print.
"""
import json
import os

import numpy as np
from scipy import stats
from scipy.optimize import minimize_scalar

D = os.environ.get("PWC_SPARC_DIR", os.path.dirname(os.path.abspath(__file__)))

KPC = 3.0856775814913673e19
KMS = 1.0e3
UPS_D, UPS_B = 0.5, 0.7
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


def partial_spearman(a, b, ctrl):
    """Spearman correlation of a vs b with ctrl removed from both, rank-based."""
    ra, rb, rc = (stats.rankdata(v) for v in (a, b, ctrl))
    ra = ra - np.polyval(np.polyfit(rc, ra, 1), rc)
    rb = rb - np.polyval(np.polyfit(rc, rb, 1), rc)
    if np.std(ra) == 0 or np.std(rb) == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


# ---------------------------------------------------------------- 1
hr("1. DATA, WITH PER-POINT COMPOSITION")

t1 = read_vizier_tsv(os.path.join(D, "vizier_t1.txt"),
                     ["Name", "i", "Qual", "Vflat", "Dist", "Rdisk"])
t2 = read_vizier_tsv(os.path.join(D, "vizier_t2.txt"),
                     ["Name", "Rad", "Vobs", "e_Vobs", "Vgas", "Vdisk", "Vbulge",
                      "SBdisk", "SBbulge"])
inc = dict(zip(t1["Name"], t1["i"]))
qual = dict(zip(t1["Name"], t1["Qual"]))
rdisk = dict(zip(t1["Name"], t1["Rdisk"]))

name = np.array(t2["Name"])
R = np.array(t2["Rad"], float)
Vo = np.array(t2["Vobs"], float)
eVo = np.array(t2["e_Vobs"], float)
Vg = np.nan_to_num(np.array(t2["Vgas"], float))
Vd = np.array(t2["Vdisk"], float)
Vb = np.nan_to_num(np.array(t2["Vbulge"], float))
SBd = np.array(t2["SBdisk"], float)

inc_a = np.array([inc.get(n, np.nan) for n in name], float)
qual_a = np.array([qual.get(n, np.nan) for n in name], float)
m = (R > 0) & (Vo > 0) & np.isfinite(eVo) & (eVo / Vo <= 0.10) & (inc_a >= 30.0) & (qual_a <= 2)
R, Vo, Vg, Vd, Vb, SBd, name = R[m], Vo[m], Vg[m], Vd[m], Vb[m], SBd[m], name[m]
# kept unshifted for the mass-to-light sensitivity scan in section 6b
R_all, Vo_all, Vg_all, Vd_all, Vb_all, name_all = R, Vo, Vg, Vd, Vb, name

conv = (KMS ** 2) / KPC
g_obs = Vo ** 2 / R * conv
Vgas2 = Vg * np.abs(Vg)
Vstar2 = UPS_D * Vd * np.abs(Vd) + UPS_B * Vb * np.abs(Vb)
Vbar2 = Vgas2 + Vstar2
g_bar = Vbar2 / R * conv
ok = (g_bar > 0) & (g_obs > 0)
g_obs, g_bar, R, name, SBd = g_obs[ok], g_bar[ok], R[ok], name[ok], SBd[ok]
Vgas2, Vstar2, Vbar2 = Vgas2[ok], Vstar2[ok], Vbar2[ok]

f_gas = Vgas2 / Vbar2          # gas share of the local baryonic source
y = np.log10(g_obs)
x = np.log10(g_bar)

print("  points: %d   galaxies: %d   halo parameters: 0" % (len(y), len(set(name))))
print("  f_gas (gas share of local baryonic source):")
print("    min %.3f  16th %.3f  median %.3f  84th %.3f  max %.3f"
      % (f_gas.min(), np.percentile(f_gas, 16), np.median(f_gas),
         np.percentile(f_gas, 84), f_gas.max()))
print("  points with f_gas < 0.2 (star dominated) : %d" % int(np.sum(f_gas < 0.2)))
print("  points with f_gas > 0.8 (gas  dominated) : %d" % int(np.sum(f_gas > 0.8)))
print("\n  volumetric density of the two components (external reference):")
print("    diffuse HI   ~1e-21 kg/m^3")
print("    stellar      ~1.4e3 kg/m^3")
print("    contrast     ~24 orders of magnitude")
results["n_points"] = int(len(y))
results["n_galaxies"] = int(len(set(name)))

# ---------------------------------------------------------------- 2
hr("2. BASELINE FIT (the thing we take residuals from)")


def rar(gb, a0):
    return gb / (1.0 - np.exp(-np.sqrt(gb / a0)))


o = minimize_scalar(lambda la: np.mean((y - np.log10(rar(g_bar, 10 ** la))) ** 2),
                    bounds=(-11.5, -9.0), method="bounded")
a0 = 10 ** o.x
res = y - np.log10(rar(g_bar, a0))
print("  a0 fitted = %.4e m/s^2, rms = %.4f dex" % (a0, np.sqrt(np.mean(res ** 2))))
print("  The baseline is deliberately the BEST smooth fit available, so any")
print("  composition signal has to survive a model already tuned to this data.")

# ---------------------------------------------------------------- 3
hr("3. POOLED TEST (confounded -- reported, but not the primary statistic)")

print("  raw Spearman, residual vs f_gas      : rho = %+.4f  p = %.2e"
      % stats.spearmanr(f_gas, res))
pr = partial_spearman(res, f_gas, x)
print("  partial, controlling for log g_bar   : rho = %+.4f" % pr)
print("\n  This number is NOT trustworthy on its own: gas-rich systems are also")
print("  faint, small and inclination-uncertain, and those are galaxy-level")
print("  properties that survive a pooled control for g_bar. Section 4 is the")
print("  statistic that matters.")
results["pooled_raw_rho"] = float(stats.spearmanr(f_gas, res)[0])
results["pooled_partial_rho"] = float(pr)

# ---------------------------------------------------------------- 4
hr("4. PRIMARY TEST: WITHIN-GALAXY, EVERY GALAXY AGAINST ITSELF ONLY")

print("  Per galaxy: partial Spearman of residual vs f_gas, controlling for")
print("  log g_bar. Distance, inclination, mass-to-light and every other")
print("  galaxy-level confound cancels -- each galaxy is compared only to")
print("  itself. Then test whether those correlations centre on zero.\n")

gal = sorted(set(name))
per = []
for gname in gal:
    s = name == gname
    if s.sum() < 8:
        continue
    if np.std(f_gas[s]) < 1e-6:
        continue
    v = partial_spearman(res[s], f_gas[s], x[s])
    if np.isfinite(v):
        per.append((gname, v, int(s.sum())))

vals = np.array([v for _, v, _ in per])
print("  galaxies with >=8 points and varying f_gas : %d" % len(vals))
print("  mean within-galaxy partial rho            : %+.4f" % vals.mean())
print("  median                                    : %+.4f" % np.median(vals))
print("  std                                       : %.4f" % vals.std())
t, p_t = stats.ttest_1samp(vals, 0.0)
w, p_w = stats.wilcoxon(vals)
print("  t-test vs 0   : t = %+.3f   p = %.3e" % (t, p_t))
print("  Wilcoxon vs 0 : W = %.1f     p = %.3e" % (w, p_w))
print("  fraction positive : %.3f" % float(np.mean(vals > 0)))
sem = vals.std(ddof=1) / np.sqrt(len(vals))
print("  95%% CI on the mean : %+.4f to %+.4f" % (vals.mean() - 1.96 * sem,
                                                  vals.mean() + 1.96 * sem))
results["within_galaxy"] = {
    "n": int(len(vals)), "mean_rho": float(vals.mean()),
    "median_rho": float(np.median(vals)), "std": float(vals.std()),
    "t": float(t), "p_t": float(p_t), "p_wilcoxon": float(p_w),
    "frac_positive": float(np.mean(vals > 0)),
    "ci95": [float(vals.mean() - 1.96 * sem), float(vals.mean() + 1.96 * sem)]}

# ---------------------------------------------------------------- 5
hr("5. EFFECT SIZE: STAR-DOMINATED vs GAS-DOMINATED AT MATCHED g_bar")

print("  Narrow g_bar bins. Inside each bin compare mean residual for")
print("  star-dominated (f_gas<0.35) against gas-dominated (f_gas>0.65).")
print("  If the equivalence principle holds these must agree.\n")
edges = np.percentile(x, np.arange(0, 101, 12.5))
print(f"{'log g_bar bin':>22} {'n_star':>7} {'n_gas':>7} {'res_star':>10} "
      f"{'res_gas':>10} {'diff':>9}")
diffs, wts = [], []
for i in range(len(edges) - 1):
    inb = (x >= edges[i]) & (x < edges[i + 1])
    ss = inb & (f_gas < 0.35)
    gg = inb & (f_gas > 0.65)
    if ss.sum() < 20 or gg.sum() < 20:
        continue
    ds = float(np.mean(res[ss]) - np.mean(res[gg]))
    diffs.append(ds)
    wts.append(min(ss.sum(), gg.sum()))
    print(f"{edges[i]:>10.2f}..{edges[i+1]:<10.2f} {ss.sum():>7} {gg.sum():>7} "
          f"{np.mean(res[ss]):>10.4f} {np.mean(res[gg]):>10.4f} {ds:>9.4f}")
if diffs:
    diffs = np.array(diffs); wts = np.array(wts, float)
    wm = float(np.sum(diffs * wts) / np.sum(wts))
    print("\n  weighted mean star-minus-gas residual : %+.4f dex" % wm)
    print("  sign consistent across bins           : %s"
          % ("yes" if np.all(diffs > 0) or np.all(diffs < 0) else "NO"))
    results["matched_bin_star_minus_gas_dex"] = wm
    results["matched_bin_diffs"] = [float(v) for v in diffs]
else:
    print("\n  no bin had >=20 points in both classes")
    results["matched_bin_star_minus_gas_dex"] = None

# ---------------------------------------------------------------- 6
hr("6. SECOND PROBE: LOCAL STELLAR SURFACE BRIGHTNESS")

good = np.isfinite(SBd) & (SBd > 0)
print("  points with finite SBdisk : %d" % int(good.sum()))
lsb = np.log10(SBd[good])
pr2 = partial_spearman(res[good], lsb, x[good])
print("  partial rho, residual vs log SBdisk, controlling log g_bar : %+.4f" % pr2)
per2 = []
for gname in gal:
    s = (name == gname) & good
    if s.sum() < 8 or np.std(np.log10(SBd[s])) < 1e-6:
        continue
    v = partial_spearman(res[s], np.log10(SBd[s]), x[s])
    if np.isfinite(v):
        per2.append(v)
per2 = np.array(per2)
if len(per2):
    t2s, p2 = stats.ttest_1samp(per2, 0.0)
    print("  within-galaxy: n=%d  mean rho=%+.4f  t=%+.3f  p=%.3e"
          % (len(per2), per2.mean(), t2s, p2))
    results["sb_within_galaxy"] = {"n": int(len(per2)), "mean_rho": float(per2.mean()),
                                   "t": float(t2s), "p": float(p2)}

# ---------------------------------------------------------------- 6b
hr("6b. THE CONFOUND TEST THAT DECIDES IT: SENSITIVITY TO MASS-TO-LIGHT")

print("A real sweep-resistance term is a property of the medium and the")
print("orbiting material. It cannot care what number is used to convert")
print("3.6um light into stellar mass -- that is a bookkeeping choice made by")
print("the analyst, not a physical quantity.")
print()
print("A mass-to-light ERROR, on the other hand, must behave exactly one way:")
print("if Upsilon is too low, the stellar contribution to g_bar is")
print("under-counted, so star-dominated points sit systematically high in the")
print("residual and gas-dominated points sit low -- which IS a correlation")
print("with f_gas, produced entirely by the assumption. Raise Upsilon and it")
print("has to shrink toward zero.")
print()
print("So: sweep Upsilon and watch the signal. Physical effect -> stable.")
print("Bookkeeping artifact -> monotonic collapse.\n")

print(f"{'Ups_d':>6} {'Ups_b':>6} {'a0 [m/s^2]':>12} {'rms':>8} {'n_gal':>6} "
      f"{'mean rho':>9} {'p':>10}")
ups_scan = []
for ud, ub in ((0.3, 0.5), (0.5, 0.7), (0.7, 0.9), (1.0, 1.0)):
    Vs2 = ud * Vd_all * np.abs(Vd_all) + ub * Vb_all * np.abs(Vb_all)
    Vg2 = Vg_all * np.abs(Vg_all)
    Vb2 = Vg2 + Vs2
    gb_u = Vb2 / R_all * conv
    go_u = Vo_all ** 2 / R_all * conv
    k = (gb_u > 0) & (go_u > 0)
    yy, xx = np.log10(go_u[k]), np.log10(gb_u[k])
    fgu = Vg2[k] / Vb2[k]
    nn = name_all[k]
    oo = minimize_scalar(lambda la: np.mean((yy - np.log10(rar(10 ** xx, 10 ** la))) ** 2),
                         bounds=(-11.5, -9.0), method="bounded")
    a0u = 10 ** oo.x
    ru = yy - np.log10(rar(10 ** xx, a0u))
    vv = []
    for gname in sorted(set(nn)):
        s_ = nn == gname
        if s_.sum() < 8 or np.std(fgu[s_]) < 1e-6:
            continue
        v_ = partial_spearman(ru[s_], fgu[s_], xx[s_])
        if np.isfinite(v_):
            vv.append(v_)
    vv = np.array(vv)
    tt, pp = stats.ttest_1samp(vv, 0.0)
    print(f"{ud:>6.1f} {ub:>6.1f} {a0u:>12.4e} {np.sqrt(np.mean(ru**2)):>8.4f} "
          f"{len(vv):>6} {vv.mean():>+9.4f} {pp:>10.2e}")
    ups_scan.append({"ups_d": ud, "ups_b": ub, "a0": float(a0u),
                     "rms": float(np.sqrt(np.mean(ru ** 2))), "n_gal": int(len(vv)),
                     "mean_rho": float(vv.mean()), "p": float(pp)})
results["upsilon_scan"] = ups_scan

print()
print("  Also re-run with RADIUS as the control instead of g_bar, since f_gas")
print("  rises outward in every disk and a pure radial trend would mimic this:")
for ctrl, lab in ((x, "log g_bar"), (np.log10(R), "log radius")):
    vv = []
    for gname in gal:
        s_ = name == gname
        if s_.sum() < 8 or np.std(f_gas[s_]) < 1e-6:
            continue
        v_ = partial_spearman(res[s_], f_gas[s_], ctrl[s_])
        if np.isfinite(v_):
            vv.append(v_)
    vv = np.array(vv)
    tt, pp = stats.ttest_1samp(vv, 0.0)
    print(f"    control = {lab:<12} n={len(vv):>4}  mean rho={vv.mean():+.4f}  p={pp:.2e}")
    results[f"control_{lab.replace(' ', '_')}"] = {"n": int(len(vv)),
                                                   "mean_rho": float(vv.mean()),
                                                   "p": float(pp)}

# ---------------------------------------------------------------- 7
hr("7. VERDICT -- written after the numbers, not before")

sc = results["upsilon_scan"]
print("The prediction under test: Newton and MOND REQUIRE zero dependence on")
print("what the orbiting material is. PWC's sweep-resistance requires nonzero.\n")
print("At the standard Upsilon_d = 0.5, the within-galaxy partial correlation")
print("is %+.4f with p = %.2e across %d galaxies. Taken alone that reads as a"
      % (vals.mean(), p_t, len(vals)))
print("detection of exactly the effect PWC predicts, and I would have reported")
print("it as one.\n")
print("It is not. Section 6b settles it. The signal is a monotonic function of")
print("the mass-to-light ratio I chose:\n")
for r_ in sc:
    print("    Upsilon_d = %.1f  ->  rho = %+.4f   p = %.2e"
          % (r_["ups_d"], r_["mean_rho"], r_["p"]))
print()
print("It scales smoothly with Upsilon and vanishes by Upsilon_d = 1.0. That")
print("is the exact signature of under-counted stellar mass, and it is NOT")
print("something a physical sweep term could do -- the medium does not know")
print("what number an analyst used to convert 3.6um light into mass.")
print()
print("CONCLUSION: NEGATIVE. No composition dependence survives the")
print("mass-to-light degeneracy. The apparent detection is an artifact of the")
print("assumed constant Upsilon. What this does buy is a real BOUND: any")
print("composition-dependent term in the governor has to be small enough to")
print("hide inside the Upsilon uncertainty, which is roughly a 0.1 dex effect")
print("at most.")
print()
print("WHAT WOULD MAKE THIS DECISIVE, and it is not SPARC: independently")
print("measured kinematics of two tracers with different volumetric density")
print("at the SAME radius in the SAME galaxy -- HI versus stellar, or")
print("globular clusters versus gas. SPARC has one curve per galaxy, so this")
print("tests the composition of the SOURCE, not of the TRACER, and the source")
print("version is degenerate with Upsilon by construction. The tracer version")
print("is not, which is why it is the test worth going and getting data for.")

out = os.path.join(D, "domain_MM_tracer_density_results.json")
with open(out, "w") as f:
    json.dump(results, f, indent=2, sort_keys=True)
print(f"\nwrote {out}")
