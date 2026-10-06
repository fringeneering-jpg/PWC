"""
Medium Density Check -- Phase Wave Cosmology (PWC)

PWC framing enforced throughout: one HDF/LDF substrate, master relation
`c^2 = Stiffness/Heaviness` (K/rho), mass baseline `M = L/c0^2`, gravity
as graded-index steering through density variation. No spacetime
curvature term, no non-baryonic dark matter parameter, no r=0 evaluation,
and no infinity is allowed to propagate: every derived quantity is guarded
and a failed guard halts and reports the substrate's own limit instead.

WHAT CHANGED IN THIS REVISION (2026-09-16), and why -- the previous
revision carried a banner reading "USER'S MODEL -- UNTOUCHED". Two parts
of what sat under that banner are changed here, because leaving them
intact would have meant reporting a number this file manufactures rather
than derives. Both originals are preserved verbatim in ORIGINAL_* strings
below, so nothing is lost:

  1. The Mercury "kill shot" ended with

         precession_arcseconds = shadow_deficit * 43.0  # Target normalization

     This multiplies by the answer. Its output is 43 * (a fraction), so it
     is bounded in [0, 43) and cannot land anywhere except near the target
     by construction, for ANY fit result. It is not a derivation of the 43
     arcsec anomaly and cannot be used as evidence about it. Removed, and
     replaced by Section 3, which instead asks what the shadowing model
     must demand of the substrate to reach the observed value, and then
     checks that demand against PWC's own master relation. It does not
     survive that check -- see the printed output.

  2. The `curve_fit` call ran against `rho_baseline = 1.0`, an admitted
     placeholder. With that value the model is bounded above by 1.0 while
     the data it is fitted to are galaxy counts per sky pixel of order
     1e0-1e2. The fit is structurally incapable of succeeding regardless
     of the data, so Section 1 now runs that feasibility check FIRST and
     halts with a diagnosis rather than reporting a meaningless
     coefficient. The model function itself is untouched.

Everything that was genuinely load-bearing and correct in the previous
revision -- the real Planck/DESI ingest, the ICRS->galactic transform,
the NSIDE=64 common grid -- is kept as written.

Data (external, not in this repository):
  CMB   : Planck 2018 SMICA full-sky map, NSIDE=2048, NESTED, GALACTIC.
  Density proxy : DESI DR1 ZCATALOG sample, ZWARN=0, native NSIDE=64.
Set PWC_PLANCK_FITS / PWC_DESI_TSV to point at them. Absent those files
this script runs every check that does not need them and says plainly
which ones it skipped.
"""

import os

import numpy as np

ORIGINAL_KILL_SHOT = """
    density_drop_ratio = local_density / baseline_density
    shadow_deficit = 1 - density_drop_ratio
    precession_arcseconds = shadow_deficit * 43.0  # Target normalization
    return precession_arcseconds
"""

ORIGINAL_BASELINE = "rho_baseline = 1.0  # Placeholder"

# --------------------------------------------------------------------- #
# Physical constants and PWC substrate parameters.
# --------------------------------------------------------------------- #
C0 = 2.99792458e8          # m/s, absolute propagation limit of the substrate
SUN_TEMP_EFFECTIVE = 5778  # K
MERCURY_DISTANCE = 57.9e9  # m
MERCURY_ANOMALY_OBS = 42.98      # arcsec/century, observed anomalous advance
MERCURY_ANOMALY_ERR = 0.04       # arcsec/century
NSIDE_COARSE = 64

PLANCK_FITS = os.environ.get("PWC_PLANCK_FITS", "")
DESI_TSV = os.environ.get("PWC_DESI_TSV", "")


def hr(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


def guard(value, label):
    """No-infinity guard. Returns the value, or halts this section."""
    a = np.asarray(value, float)
    if np.all(np.isfinite(a)):
        return value
    raise ArithmeticError(
        "HALT: %s produced a non-finite value. Under PWC premises no physical "
        "infinity exists, so this is a defect in the closure, not a result. "
        "Reporting the substrate's baseline tension limit instead." % label)


# ===================================================================== #
# THE MODEL -- unchanged from the original file.
# ===================================================================== #
def pwc_density_gradient(temp, baseline_density, expansion_coeff):
    """
    Calculates the fluid density drop based on thermal expansion.
    temp: Localized temperature of the High-Density Fluid.
    baseline_density: Resting density of the deep void (from LIGO merger delta-V).
    expansion_coeff: The hidden variable we are fitting for.
    """
    return baseline_density / (1 + (expansion_coeff * temp))


# `rho_baseline` still has no derived value. It requires the V_env(M)
# compression-envelope volume formula (steps 2-4 of the GW150914
# write-up), which does not exist anywhere in this repository. It is
# carried as an explicit unknown rather than silently set to 1.0.
rho_baseline = None


# ===================================================================== #
hr("1. CMB / DENSITY FIT -- feasibility check before any fitting")
# ===================================================================== #
have_data = bool(PLANCK_FITS) and bool(DESI_TSV) \
    and os.path.exists(PLANCK_FITS) and os.path.exists(DESI_TSV)

print("  Planck SMICA map : %s" % (PLANCK_FITS if PLANCK_FITS else "<unset: PWC_PLANCK_FITS>"))
print("  DESI DR1 sample  : %s" % (DESI_TSV if DESI_TSV else "<unset: PWC_DESI_TSV>"))
print("  both present     : %s" % have_data)

# This check does NOT need the data, and it is the one that matters.
# Model range, for baseline b and coefficient k > 0, temperature T > 0:
#     rho(T) = b / (1 + k*T)   ->   bounded in (0, b]
# Data: galaxy counts per NSIDE=64 pixel from a 2e5-row DESI sample.
npix = 12 * NSIDE_COARSE ** 2
print("\n  Structural feasibility of the curve_fit as originally written:")
print("    model  rho(T) = b/(1+k*T)  is bounded in (0, b]  for b,k,T > 0")
print("    with the placeholder b = 1.0, the model can never exceed 1.0")
print("    data   = galaxy counts per pixel, integers >= 1, over %d pixels" % npix)
print("    a 2e5-row DESI sample over the populated pixels gives counts of")
print("    order 1e0-1e2, i.e. the data exceed the model's supremum almost")
print("    everywhere.")
print("\n  HALT. The fit is structurally infeasible independently of the data.")
print("  curve_fit would not 'extract the universe's expansion coefficient';")
print("  it would drive k toward whatever least-squares value best absorbs a")
print("  units mismatch between a dimensionless bounded ratio and a raw")
print("  galaxy count. No coefficient is reported from this section.")
print("\n  What it would take to make this section meaningful:")
print("    (i)  rho_baseline as an actual density in kg/m^3, which needs the")
print("         V_env(M) envelope-volume formula. Not available.")
print("    (ii) a declared law converting galaxy counts per pixel into an HDF")
print("         density, with units. Counts are not densities.")
print("   (iii) the SMICA map is a temperature FLUCTUATION field (~1e-4 K")
print("         about 2.7255 K), not an absolute local HDF temperature, so")
print("         'temp' in the model is not the quantity the map supplies.")

if have_data:
    print("\n  Data files are present, but the three defects above are not data")
    print("  problems and are not fixed by loading them. Ingest is skipped.")

fit_status = "HALTED_STRUCTURALLY_INFEASIBLE"
pwc_expansion_coeff = None


# ===================================================================== #
hr("2. FLUID DENSITY AT MERCURY'S ORBIT")
# ===================================================================== #
print("  Requires rho_baseline (undefined) and the expansion coefficient")
print("  (not obtained in Section 1). Both inputs are missing, so no absolute")
print("  density at %.3e m is computed. Section 3 proceeds in RATIOS only,"
      % MERCURY_DISTANCE)
print("  which is legitimate: the shadowing model depends on the substrate")
print("  only through rho_local/rho_baseline, and that ratio is independent")
print("  of the unknown normalisation.")


# ===================================================================== #
hr("3. MERCURY PRECESSION -- what the shadowing model must demand")
# ===================================================================== #
# The original code multiplied the deficit by 43.0 and declared victory.
# Instead: invert. Ask what density ratio the shadowing picture REQUIRES
# to deliver the observed anomaly, then test that requirement against
# PWC's own master relation c^2 = K/rho.
#
# Retaining the original file's own normalisation assumption (deficit = 1
# corresponds to the full 43 arcsec/century), the requirement is:
#
#     shadow_deficit = 1 - rho_local/rho_baseline = 42.98/43.0

deficit_required = MERCURY_ANOMALY_OBS / 43.0
ratio_required = guard(1.0 - deficit_required, "required density ratio")
kT_required = guard(deficit_required / (1.0 - deficit_required), "required k*T")
k_required = kT_required / SUN_TEMP_EFFECTIVE

print("  Observed anomalous advance      : %.2f +/- %.2f arcsec/century"
      % (MERCURY_ANOMALY_OBS, MERCURY_ANOMALY_ERR))
print("  Required shadow deficit         : %.6f" % deficit_required)
print("  => required rho_local/rho_base  : %.6e" % ratio_required)
print("  => required k*T                 : %.1f" % kT_required)
print("  => required expansion coeff k   : %.4f per K  (at T = %d K)"
      % (k_required, SUN_TEMP_EFFECTIVE))
print("\n  In words: to produce Mercury's anomaly this way, the HDF at")
print("  Mercury's orbit must be rarefied to %.3f%% of deep-void baseline"
      % (100.0 * ratio_required))
print("  density -- a factor of %.0f depletion." % (1.0 / ratio_required))

print("\n  NOW TEST THAT AGAINST PWC'S OWN MASTER RELATION  c^2 = K/rho:")
c_local_over_c0 = guard(np.sqrt(1.0 / ratio_required), "c_local/c0")
print("    Branch A -- stiffness K held fixed, density drops by %.0f x:"
      % (1.0 / ratio_required))
print("      c_local/c0 = sqrt(rho_base/rho_local) = %.1f" % c_local_over_c0)
print("      i.e. light at Mercury's orbit would propagate at %.0f x c0."
      % c_local_over_c0)
print("      This violates c0 as the substrate's absolute impedance limit,")
print("      which is a PWC premise, not an imported relativistic one.")
print("      It also contradicts solar-system radar ranging and Cassini")
print("      timing, which bound any such variation below ~1e-5.")
print("\n    Branch B -- K co-varies with rho so that c_local = c0 exactly:")
print("      then K must fall by the same factor %.0f, and n = c0/c_local = 1"
      % (1.0 / ratio_required))
print("      everywhere. With no index gradient there is no graded-index")
print("      steering, so the gravitational mechanism this framework relies")
print("      on vanishes identically. Precession becomes 0, not 43.")
print("\n  Both branches fail. The shadowing route to Mercury's 43 arcsec is")
print("  RULED OUT in this form -- not by an external theory, but by PWC's")
print("  own master relation applied to the number the model itself needs.")

print("\n  BASELINE TENSION LIMIT (reported in place of the halted result):")
print("    The largest density contrast the substrate can carry at Mercury's")
print("    orbit without exceeding c0 is rho_local/rho_base -> 1 from below,")
print("    giving shadow_deficit -> 0 and precession -> 0 arcsec/century.")
print("    Admissible range under the c0 constraint: [0, ~1e-5 x 43] =")
print("    [0, ~4e-4] arcsec/century, against an observed %.2f."
      % MERCURY_ANOMALY_OBS)
print("    Shortfall: at least 5 orders of magnitude.")

print("\n  Degrees of freedom audit of the ORIGINAL formulation:")
print("    free parameters : 1 (the expansion coefficient)")
print("    data points     : 1 (Mercury's anomaly)")
print("    degrees of freedom : 0 -- it could not have failed, so its")
print("    agreement carried no evidential weight either way.")

# ===================================================================== #
hr("SUMMARY")
# ===================================================================== #
print("  Section 1 (CMB/density fit) : %s" % fit_status)
print("  Section 2 (Mercury density) : SKIPPED -- rho_baseline undefined")
print("  Section 3 (precession)      : COMPUTED -- model requirement RULED OUT")
print("                                by PWC's own c^2 = K/rho relation")
print("  Dark matter parameters used : 0")
print("  Infinities propagated       : 0")
print("  Claims of GR being overturned: 0 -- the previous revision's")
print("                                'GENERAL RELATIVITY DISMANTLED' branch")
print("                                was reachable for any input and has")
print("                                been removed.")
print("\n  See sparc/domain_CC_refraction_index_map.py for the galaxy-scale")
print("  test, which uses real SPARC data and does produce a usable result.")
