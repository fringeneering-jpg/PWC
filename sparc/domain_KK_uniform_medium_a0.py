"""
DOMAIN KK -- a0 from a UNIFORM medium, with the free parameter actually removed.

WHY THIS DOMAIN EXISTS. Domain EE tried to explain flat rotation curves with a
medium whose density varies per galaxy and with radius. The author's ontology
forbids that -- "constant even pressure and tension everywhere" -- and EE's
headline numbers are therefore artifacts (see the banner on that file). This
domain takes the uniform medium seriously instead and asks what a medium that
never varies can still predict.

A uniform medium has exactly one number in it: rho0. The only acceleration
scale that can be built from rho0, G and the shared speed c0 without inserting
a dimensionless factor by hand is

    a0 = c0 * sqrt(G * rho0)

That is dimensionally forced, not chosen: [G*rho] = 1/s^2, so sqrt(G*rho) is a
frequency and c*frequency is an acceleration. There is no other combination of
those three that gives m/s^2 without a free exponent.

WHAT IS BEING TESTED, AND WHAT WOULD FALSIFY IT.
  - PASS would mean: fixing a0 to c0*sqrt(G*rho0), with rho0 taken from
    somewhere OTHER than this rotation-curve data, reproduces the RAR scatter
    that a freely fitted a0 achieves. Zero fitted parameters, same scatter.
  - FAIL would mean: it needs a fudge factor, in which case the fudge factor
    is the free parameter and nothing has been derived.

THE TRAP THIS DOMAIN MUST NOT FALL INTO. a0 ~ c*H0/(2*pi) is a sixty-year-old
numerical coincidence. Since rho_crit ∝ H0^2, ANY a0 = c*sqrt(G*rho0) with
rho0 tied to rho_crit is that same coincidence rewritten. Section 5 checks
explicitly whether this is a derivation or a relabelling, and reports which.

Data: SPARC (Lelli, McGaugh & Schombert 2016), VizieR J/AJ/152/157, local
copies vizier_t1.txt / vizier_t2.txt. Cuts identical to Domains K and CC.
No dark matter halo parameter appears anywhere in this file.
"""
import json
import os

import numpy as np
from scipy.optimize import minimize_scalar

D = os.environ.get("PWC_SPARC_DIR", os.path.dirname(os.path.abspath(__file__)))

KPC = 3.0856775814913673e19
MPC = 3.0856775814913673e22
KMS = 1.0e3
c0 = 2.99792458e8
G = 6.67430e-11
UPS_D, UPS_B = 0.5, 0.7

# external cosmology inputs, flagged as external everywhere they are used
H0_PLANCK = 67.4 * KMS / MPC
OMEGA_M = 0.315
RHO_CRIT = 3 * H0_PLANCK ** 2 / (8 * np.pi * G)
RHO_HDF_REPO = 1e-21            # the value Domains EE/Z/II carry internally

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
hr("1. REAL SPARC, IDENTICAL CUTS TO DOMAINS K AND CC")

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
m = (R > 0) & (Vo > 0) & np.isfinite(eVo)
m &= (eVo / Vo <= 0.10)
m &= (inc_a >= 30.0)
m &= (qual_a <= 2)
R, Vo, Vg, Vd, Vb, name = R[m], Vo[m], Vg[m], Vd[m], Vb[m], name[m]

conv = (KMS ** 2) / KPC
g_obs = Vo ** 2 / R * conv
Vbar2 = Vg * np.abs(Vg) + UPS_D * Vd * np.abs(Vd) + UPS_B * Vb * np.abs(Vb)
g_bar = Vbar2 / R * conv
ok = (g_bar > 0) & (g_obs > 0)
g_obs, g_bar, name = g_obs[ok], g_bar[ok], name[ok]
y = np.log10(g_obs)

print("  usable points : %d      galaxies : %d" % (len(g_obs), len(set(name))))
print("  dark matter halo parameters in this file : 0")
results["n_points"] = int(len(g_obs))
results["n_galaxies"] = int(len(set(name)))


def rar(gb, a0):
    return gb / (1.0 - np.exp(-np.sqrt(gb / a0)))


def rms_dex(pred):
    return float(np.sqrt(np.mean((y - np.log10(pred)) ** 2)))


# ---------------------------------------------------------------- 2
hr("2. BENCHMARK: a0 FITTED FREELY (one parameter, the thing to beat)")

o = minimize_scalar(lambda la: np.mean((y - np.log10(rar(g_bar, 10 ** la))) ** 2),
                    bounds=(-11.5, -9.0), method="bounded")
a0_fit = 10 ** o.x
rms_fit = rms_dex(rar(g_bar, a0_fit))
rms_newton = rms_dex(g_bar)
print("  Newton, baryons only      (0 params) : rms %.4f dex" % rms_newton)
print("  RAR, a0 fitted            (1 param)  : rms %.4f dex   a0 = %.4e m/s^2"
      % (rms_fit, a0_fit))
results["a0_fitted"] = float(a0_fit)
results["rms_fitted"] = rms_fit
results["rms_newton"] = rms_newton

# ---------------------------------------------------------------- 3
hr("3. a0 PREDICTED FROM A UNIFORM MEDIUM -- NOTHING FITTED TO THIS DATA")

cands = [
    ("Omega_m * rho_crit  [Planck 2018, EXTERNAL]", OMEGA_M * RHO_CRIT),
    ("rho_crit            [Planck 2018, EXTERNAL]", RHO_CRIT),
    ("rho_HDF = 1e-21     [this repo, Domains EE/Z/II]", RHO_HDF_REPO),
]
print("  a0_pred = c0 * sqrt(G * rho0)\n")
print(f"{'rho0 source':<46} {'rho0 [kg/m^3]':>13} {'a0_pred':>12} "
      f"{'a0_pred/a0_fit':>15} {'rms [dex]':>10}")
for label, r0 in cands:
    a0p = c0 * np.sqrt(G * r0)
    rp = rms_dex(rar(g_bar, a0p))
    print(f"{label:<46} {r0:>13.4e} {a0p:>12.4e} {a0p / a0_fit:>15.4f} {rp:>10.4f}")
    results[f"a0_pred_{label.split()[0]}"] = float(a0p)
    results[f"rms_pred_{label.split()[0]}"] = rp

a0_om = c0 * np.sqrt(G * OMEGA_M * RHO_CRIT)
rms_om = rms_dex(rar(g_bar, a0_om))
print("\n  Penalty for using the Omega_m*rho_crit prediction instead of the fit:")
print("    %.4f - %.4f = %+.4f dex  (linear factor %.3f)"
      % (rms_om, rms_fit, rms_om - rms_fit, 10 ** (rms_om - rms_fit)))
print("    and it still beats Newton by %.4f dex." % (rms_newton - rms_om))
results["penalty_dex_vs_fitted"] = float(rms_om - rms_fit)

# ---------------------------------------------------------------- 4
hr("4. INVERSION: WHAT rho0 DOES SPARC ITSELF DEMAND?")

rho0_sparc = a0_fit ** 2 / (c0 ** 2 * G)
print("  rho0 = a0^2 / (c0^2 * G)")
print("    from the SPARC-fitted a0 : %.4e kg/m^3" % rho0_sparc)
print("    as a fraction of rho_crit: %.4f" % (rho0_sparc / RHO_CRIT))
print("    Planck Omega_m for compare: %.4f   [EXTERNAL]" % OMEGA_M)
print("    ratio                     : %.3f" % (rho0_sparc / (OMEGA_M * RHO_CRIT)))
print()
print("  against the value this repository already carries for rho_HDF:")
print("    rho_HDF (repo)            : %.4e kg/m^3" % RHO_HDF_REPO)
print("    rho0 (SPARC inversion)    : %.4e kg/m^3" % rho0_sparc)
print("    discrepancy               : %.3e x" % (RHO_HDF_REPO / rho0_sparc))
results["rho0_from_sparc"] = float(rho0_sparc)
results["rho0_over_rho_crit"] = float(rho0_sparc / RHO_CRIT)
results["repo_rho_hdf_discrepancy"] = float(RHO_HDF_REPO / rho0_sparc)

# ---------------------------------------------------------------- 5
hr("5. IS THIS A DERIVATION OR IS IT c*H0 IN A DIFFERENT COSTUME?")

print("  rho_crit = 3*H0^2/(8*pi*G), so for rho0 = f * rho_crit:")
print("      c0*sqrt(G*rho0) = c0*H0 * sqrt(3f/(8*pi))\n")
print("  The medium formula therefore CANNOT be independent of c*H0. The only")
print("  question is whether it predicts the O(1) factor or absorbs it.\n")
cH0 = c0 * H0_PLANCK
print(f"{'quantity':<40} {'value':>13} {'/(c0*H0)':>12}")
print(f"{'c0*H0  [Planck, EXTERNAL]':<40} {cH0:>13.4e} {1.0:>12.4f}")
print(f"{'a0 fitted to SPARC':<40} {a0_fit:>13.4e} {a0_fit / cH0:>12.4f}")
print(f"{'c0*sqrt(G*Omega_m*rho_crit)':<40} {a0_om:>13.4e} {a0_om / cH0:>12.4f}")
print(f"{'c0*H0/(2*pi)  [the old coincidence]':<40} "
      f"{cH0 / (2 * np.pi):>13.4e} {1 / (2 * np.pi):>12.4f}")
print()
print("  sqrt(3*Omega_m/(8*pi)) = %.4f   is the factor the medium formula"
      % np.sqrt(3 * OMEGA_M / (8 * np.pi)))
print("  supplies. It is not free -- it comes from Omega_m -- but Omega_m is")
print("  itself a Planck/LCDM fit, so the O(1) factor has been IMPORTED, not")
print("  derived. The author's own objection applies here in full:")
print('      "is fitted assuming LCDM ... Its fitted in acdm."')
print("  That objection is correct about this step and is not waved away.")
results["a0_fit_over_cH0"] = float(a0_fit / cH0)
results["a0_pred_over_cH0"] = float(a0_om / cH0)
results["sqrt_3om_8pi"] = float(np.sqrt(3 * OMEGA_M / (8 * np.pi)))

# ---------------------------------------------------------------- 6
hr("6. THE ONE THING A UNIFORM MEDIUM PREDICTS THAT A HALO CANNOT")

print("  A uniform medium has ONE rho0 for the whole universe. So a0 must be")
print("  strictly universal: no dependence on galaxy mass, size or surface")
print("  density. Per-galaxy a0, fitted independently:")
gal = np.array(sorted(set(name)))
a0_gal, n_gal = [], []
for gname in gal:
    sel = name == gname
    if sel.sum() < 4:
        continue
    yy, gg = y[sel], g_bar[sel]
    oo = minimize_scalar(
        lambda la: np.mean((yy - np.log10(rar(gg, 10 ** la))) ** 2),
        bounds=(-12.0, -8.0), method="bounded")
    a0_gal.append(10 ** oo.x)
    n_gal.append(gname)
a0_gal = np.array(a0_gal)
la = np.log10(a0_gal)
print("    galaxies with >=4 points : %d" % len(a0_gal))
print("    median a0                : %.4e m/s^2" % np.median(a0_gal))
print("    scatter in log10 a0      : %.4f dex" % np.std(la))
print("    16th-84th percentile     : %.4e to %.4e"
      % (np.percentile(a0_gal, 16), np.percentile(a0_gal, 84)))
print()
print("  NOTE, stated plainly: this scatter is an UPPER bound on any real")
print("  variation. Per-galaxy fits absorb distance errors, inclination")
print("  errors and mass-to-light scatter, all of which inflate it. This")
print("  domain does NOT claim the spread is physical. It records it so a")
print("  later domain with proper error propagation can test universality.")
results["a0_per_galaxy_median"] = float(np.median(a0_gal))
results["a0_per_galaxy_scatter_dex"] = float(np.std(la))
results["n_galaxies_per_galaxy_fit"] = int(len(a0_gal))

# ---------------------------------------------------------------- 7
hr("7. VERDICT -- written after the numbers above, not before")

print("1. a0 = c0*sqrt(G*rho0) is dimensionally forced for a uniform medium.")
print("   That much is real and needs no apology.\n")
print("2. With rho0 = Omega_m*rho_crit taken from Planck and NOTHING fitted to")
print("   SPARC, the RAR scatter is %.4f dex against %.4f dex for a freely"
      % (rms_om, rms_fit))
print("   fitted a0 -- a penalty of %+.4f dex, and still %.4f dex better than"
      % (rms_om - rms_fit, rms_newton - rms_om))
print("   Newton. Calling that 'zero free parameters' is fair ONLY if the")
print("   Planck input is counted honestly, which section 5 does.\n")
print("3. Section 5 is the load-bearing caveat. Because rho_crit ∝ H0^2, this")
print("   formula is c*H0 times sqrt(3*Omega_m/(8*pi)) = %.4f. It reproduces"
      % np.sqrt(3 * OMEGA_M / (8 * np.pi)))
print("   the a0/(c*H0) = %.4f that SPARC wants, to within %.1f%%. That is a"
      % (a0_fit / cH0, 100 * abs(a0_om / a0_fit - 1)))
print("   genuinely good number, and it is ALSO an LCDM-sourced number. Both")
print("   are true at once and neither cancels the other.\n")
print("4. INTERNAL INCONSISTENCY FOUND, and it is this repository's problem,")
print("   not an external one. SPARC demands rho0 = %.3e kg/m^3. Domains EE,"
      % rho0_sparc)
print("   Z and II carry rho_HDF = %.0e kg/m^3. Those differ by a factor of"
      % RHO_HDF_REPO)
print("   %.2e, i.e. %.1f orders of magnitude."
      % (RHO_HDF_REPO / rho0_sparc, np.log10(RHO_HDF_REPO / rho0_sparc)))
print("   The medium cannot be uniform AND carry two densities that far")
print("   apart. One of the two is wrong and this domain does not settle")
print("   which -- it records that they cannot both stand.\n")
print("5. What would make this a real derivation rather than a repackaging:")
print("   an independent route to rho0 that does not pass through H0 or")
print("   Omega_m. m_wave -- the mass of one (+,-) medium pair -- is exactly")
print("   such a route, and it is still unknown. That is the same blocker")
print("   Domain JJ ends on.")

out = os.path.join(D, "domain_KK_uniform_medium_a0_results.json")
with open(out, "w") as f:
    json.dump(results, f, indent=2, sort_keys=True)
print(f"\nwrote {out}")
