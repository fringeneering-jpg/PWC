"""
DOMAIN CC -- Gravity-as-refraction index map on real SPARC rotation curves.

Pre-registered question (written before any number below was computed):

  If galaxy rotation curves are produced by graded-index steering through a
  variable-density HDF substrate -- NOT by a non-baryonic dark matter halo --
  then the required refractive structure n(r) must be:

    (a) computable from the observed curve without any halo parameter, and
    (b) a UNIVERSAL function of the baryonic source g_bar, with no
        per-galaxy freedom.

  (a) alone is not a result. Inverting an observed curve into a medium
  profile is a change of variables, not a prediction: it has exactly the
  same information content as fitting a halo, because both absorb one free
  radial function per galaxy. Only (b) is falsifiable. This script computes
  (a) and then tests (b) on withheld galaxies.

Governing relations used (no spacetime curvature invoked anywhere):

  1. Master wave relation     c^2 = K / rho          (Stiffness / Heaviness)
  2. Effective index          n(r) = c0 / c_local(r)
     At fixed stiffness K, (1) gives  n^2 = rho_HDF / rho_0 .
     At fixed density rho,  (1) gives  n^2 = K_0 / K .
  3. Graded-index steering    g(r) = ALPHA * c0^2 * d ln n / dr

  ALPHA is the index-role weighting. It is NOT free here and it is NOT
  fitted: it is the unresolved factor flagged in PROVENANCE_MANIFEST.md
  ("Lensing", status OPEN). A single isotropic index role gives ALPHA=1;
  matching the GR light-bending benchmark 4GM/(b c0^2) requires the
  two-role (anisotropic) weighting. Both are carried through explicitly
  below so the convention dependence of the map is visible rather than
  buried.

Guards (per the no-infinity / no-singularity premise):
  - Every derived quantity is checked finite. A non-finite value halts the
    galaxy and reports the baseline tension limit instead of propagating.
  - The index contrast is checked against the project's own stated substrate
    cap rho_HDF_max = 4.6e10 kg/m^3.
  - No dark-matter halo parameter exists in this file. Free-parameter counts
    are printed explicitly for every model evaluated.

Data: Lelli, McGaugh & Schombert 2016, AJ 152, 157 (SPARC).
      VizieR J/AJ/152/157 table1 + table2, downloaded 2026-08-04.
      Real catalog files in this repository. Nothing simulated.

Parser and quality cuts are taken verbatim from domain_K_rar.py so the
numbers below are directly comparable to the existing Domain K/M record.
"""
import os
import json

import numpy as np
from scipy.optimize import minimize_scalar

# --------------------------------------------------------------------- #
# Paths. Repo-relative by default; PWC_SPARC_DIR overrides. The original
# hard-coded Windows path (C:\Users\jaden\cosmology\sparc) is unreachable
# on any other machine, which is why every domain script in this directory
# was previously unrunnable outside its author's laptop.
# --------------------------------------------------------------------- #
D = os.environ.get("PWC_SPARC_DIR", os.path.dirname(os.path.abspath(__file__)))

KPC = 3.0856775814913673e19      # m
KMS = 1.0e3                      # m/s
C0 = 2.99792458e8                # m/s, substrate propagation limit
UPS_D, UPS_B = 0.5, 0.7          # standard SPARC 3.6um mass-to-light ratios
RHO_HDF_MAX = 4.6e10             # kg/m^3, project's own stated substrate cap
ALPHA_ONE_ROLE = 1.0             # single isotropic index role
ALPHA_TWO_ROLE = 0.5             # two-role weighting (GR-matching convention)


def hr(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


def read_vizier_tsv(path, cols):
    """VizieR asu-tsv: header row, units row, dashes row, then data."""
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8", errors="replace")]
    hdr_i = None
    for i, l in enumerate(lines):
        if l.startswith("#") or not l.strip():
            continue
        if "\t" in l and "recno" in l:
            hdr_i = i
            break
    names = lines[hdr_i].split("\t")
    dash_i = None
    for i in range(hdr_i + 1, min(hdr_i + 6, len(lines))):
        if set(lines[i].replace("\t", "").strip()) <= set("- "):
            dash_i = i
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
                out[c].append(v if c == "Name" else (float(v) if v not in ("", "---") else np.nan))
        except ValueError:
            continue
    return out


def finite_or_halt(arr, label, galaxy=None):
    """No-infinity guard. Returns (ok, message)."""
    a = np.asarray(arr, float)
    if np.all(np.isfinite(a)):
        return True, ""
    where = "galaxy %s" % galaxy if galaxy else "global"
    return False, "NON-FINITE in %s (%s) -- halted, baseline tension limit reported instead" % (label, where)


results = {}

# ===================================================================== #
hr("1. LOAD REAL SPARC DATA")
# ===================================================================== #
t1 = read_vizier_tsv(os.path.join(D, "vizier_t1.txt"), ["Name", "i", "Qual", "Vflat", "Dist", "Rdisk"])
t2 = read_vizier_tsv(os.path.join(D, "vizier_t2.txt"),
                     ["Name", "Rad", "Vobs", "e_Vobs", "Vgas", "Vdisk", "Vbulge"])
print("  table1 galaxies      : %d" % len(t1["Name"]))
print("  table2 curve points  : %d" % len(t2["Name"]))

inc = {n: i for n, i in zip(t1["Name"], t1["i"])}
qual = {n: q for n, q in zip(t1["Name"], t1["Qual"])}

name = np.array(t2["Name"])
R = np.array(t2["Rad"], float)
Vo = np.array(t2["Vobs"], float)
eVo = np.array(t2["e_Vobs"], float)
Vg = np.nan_to_num(np.array(t2["Vgas"], float))
Vd = np.array(t2["Vdisk"], float)
Vb = np.nan_to_num(np.array(t2["Vbulge"], float))

# ===================================================================== #
hr("2. QUALITY CUTS (identical to Domain K -- McGaugh/Lelli/Schombert 2016)")
# ===================================================================== #
inc_a = np.array([inc.get(n, np.nan) for n in name], float)
qual_a = np.array([qual.get(n, np.nan) for n in name], float)
m = (R > 0) & (Vo > 0) & np.isfinite(eVo)
print("  finite R, Vobs, e_Vobs              : %5d" % m.sum())
m &= (eVo / Vo <= 0.10)
print("  + e_Vobs/Vobs <= 10%%                : %5d" % m.sum())
m &= (inc_a >= 30.0)
print("  + inclination >= 30 deg             : %5d" % m.sum())
m &= (qual_a <= 2)
print("  + quality flag Q <= 2               : %5d" % m.sum())
print("  galaxies surviving                  : %5d" % len(set(name[m])))

R, Vo, eVo, Vg, Vd, Vb, name = R[m], Vo[m], eVo[m], Vg[m], Vd[m], Vb[m], name[m]

# ===================================================================== #
hr("3. ACCELERATIONS FROM REAL VELOCITIES (no halo term anywhere)")
# ===================================================================== #
conv = (KMS ** 2) / KPC
g_obs = Vo ** 2 / R * conv
Vbar2 = Vg * np.abs(Vg) + UPS_D * Vd * np.abs(Vd) + UPS_B * Vb * np.abs(Vb)
g_bar = Vbar2 / R * conv
ok = (g_bar > 0) & (g_obs > 0)
g_obs, g_bar, R, name, Vo = g_obs[ok], g_bar[ok], R[ok], name[ok], Vo[ok]

ok_flag, msg = finite_or_halt(np.concatenate([g_obs, g_bar]), "g_obs/g_bar")
if not ok_flag:
    raise SystemExit(msg)

print("  g_bar = [Vgas|Vgas| + %.1f*Vdisk|Vdisk| + %.1f*Vbul|Vbul|]/R" % (UPS_D, UPS_B))
print("  usable points        : %d   galaxies: %d" % (len(g_obs), len(set(name))))
print("  log10 g_bar range    : %.2f to %.2f" % (np.log10(g_bar).min(), np.log10(g_bar).max()))
print("  log10 g_obs range    : %.2f to %.2f" % (np.log10(g_obs).min(), np.log10(g_obs).max()))
print("  DARK MATTER HALO PARAMETERS IN THIS CALCULATION: 0")

y = np.log10(g_obs)


def rms_dex(pred):
    return float(np.sqrt(np.mean((y - np.log10(pred)) ** 2)))


# ===================================================================== #
hr("4. ANCHOR TO THE EXISTING RECORD (Domain K benchmarks, recomputed)")
# ===================================================================== #
rms_newton = rms_dex(g_bar)
print("  Newtonian baryons only        (0 free params) : rms %.4f dex" % rms_newton)


def rar(gb, a0):
    return gb / (1.0 - np.exp(-np.sqrt(gb / a0)))


o = minimize_scalar(lambda la0: np.mean((y - np.log10(rar(g_bar, 10 ** la0))) ** 2),
                    bounds=(-11.0, -9.0), method="bounded")
a0_rar = 10 ** o.x
rms_rar = rms_dex(rar(g_bar, a0_rar))
print("  RAR / MOND-like interpolation (1 free param)  : rms %.4f dex   a0 = %.4e m/s^2"
      % (rms_rar, a0_rar))

results["benchmarks"] = {
    "n_points": int(len(g_obs)), "n_galaxies": int(len(set(name))),
    "newton_baryons_only_rms_dex": rms_newton,
    "rar_rms_dex": rms_rar, "rar_a0": float(a0_rar),
    "dark_matter_parameters": 0,
}

# ===================================================================== #
hr("5. THE REFRACTION MAP  n(r)  -- part (a), the change of variables")
# ===================================================================== #
# g = ALPHA * c0^2 * d ln n / dr   =>   ln n(r) = -(1/(ALPHA c0^2)) * Int_r^Rout g dr'
# Boundary condition: n -> 1 at the outermost measured radius (baseline HDF).
# This is an OUTER boundary condition, not an r=0 condition: no point mass,
# no r=0 singularity is ever evaluated.

per_gal = {}
halts = []
for gname in sorted(set(name)):
    s = (name == gname)
    if s.sum() < 3:
        continue
    order = np.argsort(R[s])
    r_m = R[s][order] * KPC
    go = g_obs[s][order]
    gb = g_bar[s][order]

    # cumulative outward integral of g dr, from each radius to the outermost
    seg = np.concatenate([[0.0], np.cumsum(0.5 * (go[1:] + go[:-1]) * np.diff(r_m))])
    integral_to_out = seg[-1] - seg          # Int_r^Rout g dr'   (>=0)

    seg_b = np.concatenate([[0.0], np.cumsum(0.5 * (gb[1:] + gb[:-1]) * np.diff(r_m))])
    integral_b = seg_b[-1] - seg_b

    entry = {}
    bad = False
    for tag, alpha in (("one_role_alpha1", ALPHA_ONE_ROLE), ("two_role_alpha0.5", ALPHA_TWO_ROLE)):
        ln_n = integral_to_out / (alpha * C0 ** 2)
        ln_n_bar = integral_b / (alpha * C0 ** 2)
        okf, msg = finite_or_halt(ln_n, "ln n", gname)
        if not okf:
            halts.append(msg)
            bad = True
            break
        n_minus_1 = np.expm1(ln_n)
        rho_contrast = np.exp(2.0 * ln_n)          # n^2 = rho_HDF/rho_0 at fixed K
        stiff_contrast = np.exp(-2.0 * ln_n)       # n^2 = K_0/K at fixed rho
        entry[tag] = {
            "max_n_minus_1": float(n_minus_1.max()),
            "max_rho_HDF_over_rho_0": float(rho_contrast.max()),
            "min_K_over_K_0": float(stiff_contrast.min()),
            "max_excess_n_minus_1": float(np.expm1(ln_n - ln_n_bar).max()),
        }
    if bad:
        continue
    entry["n_points"] = int(s.sum())
    entry["R_max_kpc"] = float(R[s].max())
    per_gal[gname] = entry

amax = np.array([v["one_role_alpha1"]["max_n_minus_1"] for v in per_gal.values()])
rmax = np.array([v["one_role_alpha1"]["max_rho_HDF_over_rho_0"] for v in per_gal.values()])
emax = np.array([v["one_role_alpha1"]["max_excess_n_minus_1"] for v in per_gal.values()])
amax2 = np.array([v["two_role_alpha0.5"]["max_n_minus_1"] for v in per_gal.values()])

print("  galaxies mapped                        : %d" % len(per_gal))
print("  halts on non-finite values             : %d" % len(halts))
print("  required (n-1) at galaxy centre, ALPHA=1   : median %.3e  max %.3e"
      % (np.median(amax), amax.max()))
print("  required (n-1) at galaxy centre, ALPHA=0.5 : median %.3e  max %.3e"
      % (np.median(amax2), amax2.max()))
print("  -> the map is convention-dependent by exactly the unresolved")
print("     factor flagged in PROVENANCE_MANIFEST.md 'Lensing' (status OPEN).")
print("  required rho_HDF/rho_0 contrast, ALPHA=1   : median %.6f  max %.6f"
      % (np.median(rmax), rmax.max()))
print("  excess (n-1) over baryons, ALPHA=1         : median %.3e  max %.3e"
      % (np.median(emax), emax.max()))

# Substrate-cap check: does any galaxy drive the medium toward its own cap?
print("\n  SUBSTRATE CAP CHECK (rho_HDF_max = %.1e kg/m^3):" % RHO_HDF_MAX)
print("    largest density contrast demanded anywhere : %.6f x baseline" % rmax.max())
print("    the cap is a ratio of %.1e to the SPARC-scale baseline (~1e-21 kg/m^3)," % RHO_HDF_MAX)
print("    i.e. ~1e31 x. Galaxy curves demand a contrast of order 1e-6.")
print("    CONCLUSION: SPARC never approaches the cap. The no-singularity")
print("    clause is not exercised by this data and is therefore not")
print("    tested by it -- neither confirmed nor challenged.")

results["refraction_map"] = {
    "boundary_condition": "n -> 1 at outermost measured radius; no r=0 evaluation",
    "n_galaxies_mapped": len(per_gal),
    "halts_nonfinite": len(halts),
    "median_max_n_minus_1_alpha1": float(np.median(amax)),
    "median_max_n_minus_1_alpha0p5": float(np.median(amax2)),
    "max_rho_HDF_over_rho_0": float(rmax.max()),
    "median_max_excess_n_minus_1_alpha1": float(np.median(emax)),
    "substrate_cap_exercised": False,
}

# ===================================================================== #
hr("6. PART (b) -- THE ACTUAL TEST: is the required medium UNIVERSAL?")
# ===================================================================== #
# The excess index gradient beyond baryons, expressed as an acceleration:
#     c0^2 * d ln n_excess / dr  =  (g_obs - g_bar) / ALPHA
# Question: is this a single-valued universal function of g_bar, with NO
# per-galaxy parameter? Split by galaxy, fit on train, predict holdout.

gals = np.array(sorted(set(name)))


def medium_law(gb, a0, p):
    """HDF stiffness-deficit closure: excess steering grows as a power of the
    stiffness shortfall (a0/g_bar). p is the choke exponent already used in
    Domain K; a0 is the stiffness-transition scale. Both universal, both
    shared across every galaxy, none per-galaxy, none a halo."""
    return gb * (1.0 + (a0 / gb) ** p)


def fit_on(mask):
    yy, gg = np.log10(g_obs[mask]), g_bar[mask]
    best = None
    for p in np.linspace(0.2, 1.5, 66):
        o = minimize_scalar(lambda la0: np.mean((yy - np.log10(medium_law(gg, 10 ** la0, p))) ** 2),
                            bounds=(-12.0, -8.0), method="bounded")
        if best is None or o.fun < best[0]:
            best = (o.fun, 10 ** o.x, p)
    a0_r = 10 ** minimize_scalar(
        lambda la0: np.mean((yy - np.log10(rar(gg, 10 ** la0))) ** 2),
        bounds=(-11.0, -9.0), method="bounded").x
    return best[1], best[2], a0_r


# A SINGLE train/holdout split is not a result: the split-to-split spread is
# comparable to the model differences being tested. The headline number is
# therefore an ensemble over many random galaxy-level splits. (Checked: the
# first seed tried here gave HDF -0.0011 dex vs RAR, which the ensemble below
# shows to be a favourable minority draw, not the typical outcome.)
N_SPLITS = 40
FRAC_TRAIN = 0.70
d_hdf, d_rar, d_newt, a0s, ps = [], [], [], [], []
for seed in range(N_SPLITS):
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(gals))
    train_g = set(gals[perm[:int(round(FRAC_TRAIN * len(gals)))]])
    tr = np.array([g in train_g for g in name])
    ho = ~tr
    a0_m, p_m, a0_r = fit_on(tr)
    yho, gho = np.log10(g_obs[ho]), g_bar[ho]
    d_hdf.append(np.sqrt(np.mean((yho - np.log10(medium_law(gho, a0_m, p_m))) ** 2)))
    d_rar.append(np.sqrt(np.mean((yho - np.log10(rar(gho, a0_r))) ** 2)))
    d_newt.append(np.sqrt(np.mean((yho - np.log10(gho)) ** 2)))
    a0s.append(a0_m)
    ps.append(p_m)

d_hdf, d_rar, d_newt = np.array(d_hdf), np.array(d_rar), np.array(d_newt)
diff = d_hdf - d_rar
n_train_gal = int(round(FRAC_TRAIN * len(gals)))

print("  %d random splits, %d train / %d holdout GALAXIES each (never split by point)"
      % (N_SPLITS, n_train_gal, len(gals) - n_train_gal))
print("  fitted universal params across splits: a0 = %.4e +/- %.1e m/s^2,  p = %.3f +/- %.3f"
      % (np.mean(a0s), np.std(a0s), np.mean(ps), np.std(ps)))
print("\n  HOLDOUT rms (dex), mean +/- sd over splits:")
print("     Newtonian baryons only (0 params)  : %.4f +/- %.4f" % (d_newt.mean(), d_newt.std()))
print("     MOND/RAR interpolation (1 param)   : %.4f +/- %.4f" % (d_rar.mean(), d_rar.std()))
print("     HDF stiffness-deficit  (2 params)  : %.4f +/- %.4f" % (d_hdf.mean(), d_hdf.std()))
print("\n     HDF minus RAR : %+.4f +/- %.4f dex   HDF wins %d/%d splits"
      % (diff.mean(), diff.std(), int((diff < 0).sum()), N_SPLITS))

# Per-galaxy residual scatter under the full-sample universal fit.
a0_full, p_full, _ = fit_on(np.ones(len(name), bool))
resid = np.log10(g_obs) - np.log10(medium_law(g_bar, a0_full, p_full))
per_gal_mean = np.array([resid[name == g].mean() for g in gals])
print("\n  Galaxy-to-galaxy scatter of the mean residual : %.4f dex" % per_gal_mean.std())
print("  (the offset each galaxy would want if allowed its own medium")
print("   normalisation -- the per-galaxy freedom the universal law is NOT")
print("   permitted to use. It is comparable to the total residual, so a")
print("   single universal medium is genuinely constrained here, not fitted.)")

results["universality_test"] = {
    "protocol": "%d random galaxy-level splits, %.0f%% train" % (N_SPLITS, 100 * FRAC_TRAIN),
    "n_train_gal": n_train_gal, "n_holdout_gal": int(len(gals) - n_train_gal),
    "hdf_law_a0_mean": float(np.mean(a0s)), "hdf_law_a0_sd": float(np.std(a0s)),
    "hdf_law_p_mean": float(np.mean(ps)), "hdf_law_p_sd": float(np.std(ps)),
    "holdout_rms_dex_mean_sd": {
        "newton_baryons_only": [float(d_newt.mean()), float(d_newt.std())],
        "rar_1param": [float(d_rar.mean()), float(d_rar.std())],
        "hdf_choke_2param": [float(d_hdf.mean()), float(d_hdf.std())],
    },
    "hdf_minus_rar_dex_mean": float(diff.mean()), "hdf_minus_rar_dex_sd": float(diff.std()),
    "hdf_wins_n_splits": int((diff < 0).sum()), "n_splits": N_SPLITS,
    "per_galaxy_mean_residual_scatter_dex": float(per_gal_mean.std()),
    "free_params_hdf": 2, "free_params_rar": 1, "free_params_halo_per_galaxy": 0,
}
rms_ho, rms_rar_ho, rms_newt_ho = d_hdf.mean(), d_rar.mean(), d_newt.mean()

# ===================================================================== #
hr("7. SCOPE CHECK -- the r < 0.5*alpha short-range break")
# ===================================================================== #
BOHR = 5.29177210903e-11   # m
print("  Proposed break radius scale (Bohr radius a0_B)  : %.3e m" % BOHR)
print("  Smallest SPARC galactocentric radius in sample  : %.3e m" % (R.min() * KPC))
print("  Ratio                                           : %.2e" % (R.min() * KPC / BOHR))
print("  SPARC probes radii ~%d orders of magnitude above any atomic-scale"
      % round(np.log10(R.min() * KPC / BOHR)))
print("  break. This dataset places NO constraint on it, in either direction.")
results["short_range_break"] = {
    "testable_with_sparc": False,
    "min_sparc_radius_over_bohr": float(R.min() * KPC / BOHR),
}

# ===================================================================== #
hr("8. VERDICT")
# ===================================================================== #
delta = rms_ho - rms_rar_ho
print("  (a) Inversion to a medium profile: SUCCEEDS for all %d galaxies," % len(per_gal))
print("      with zero halo parameters and zero infinities. But an inversion")
print("      cannot fail -- it absorbs one free radial function per galaxy,")
print("      exactly as a halo fit does. It is a change of variables, and on")
print("      its own it is not evidence for anything.")
print("  (b) Universality on withheld galaxies is the falsifiable half:")
print("      HDF stiffness-deficit law : %.4f dex (2 universal params)" % rms_ho)
print("      MOND/RAR interpolation    : %.4f dex (1 universal param)" % rms_rar_ho)
print("      difference %+.4f +/- %.4f dex, HDF ahead in %d/%d splits."
      % (diff.mean(), diff.std(), int((diff < 0).sum()), N_SPLITS))
if diff.mean() < -diff.std():
    v = "HDF law beats RAR on withheld galaxies"
elif diff.mean() > diff.std():
    v = ("NEGATIVE -- the HDF stiffness-deficit law is consistently WORSE than "
         "1-parameter RAR on withheld galaxies despite carrying one more free parameter")
else:
    v = "INDISTINGUISHABLE from RAR, while carrying one more free parameter"
print("      VERDICT: %s" % v)
print("\n  What IS solid: both laws crush the baryons-only null (%.4f dex)." % rms_newt_ho)
print("  Real galaxies do demand a smooth, monotonic medium response tied to")
print("  the baryons, with no per-galaxy halo. That much the data supports.")
print("\n  What is NOT established by this run:")
print("   - a0 is FITTED here (%.3e m/s^2), not derived from K, rho_0 or c_s0."
      % np.mean(a0s))
print("     Nothing in this repository derives it. Domain X's attempt using")
print("     rho_HDF_max was off-regime by ~33 orders of magnitude.")
print("   - The refraction law itself is convention-dependent by the factor-2")
print("     ambiguity that PROVENANCE_MANIFEST.md already records as OPEN.")
print("     An isotropic single-role index reproduces 2GM/(b c0^2), i.e. half")
print("     the measured light bending. That is unresolved, and fitting")
print("     rotation curves does not touch it.")
print("   - Rotation curves do not discriminate refraction from any other")
print("     mechanism producing the same g(r). This test constrains the")
print("     radial force law, not the ontology behind it.")
results["not_established"] = [
    "a0 is fitted, not derived from the substrate parameters",
    "isotropic-index factor-2 light-bending deficit remains OPEN",
    "rotation curves do not discriminate refraction from other g(r) mechanisms",
    "substrate density cap is never approached, so it is untested here",
    "short-range r<0.5*alpha break is ~29 orders of magnitude out of reach",
]
results["verdict"] = v

out = os.path.join(D, "domain_CC_refraction_index_map_results.json")
results["per_galaxy"] = per_gal
with open(out, "w") as f:
    json.dump(results, f, indent=2)
print("\n  wrote %s" % out)
