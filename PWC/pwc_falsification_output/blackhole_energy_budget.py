"""
PWC falsification test: aggregate black-hole-merger energy vs. the dark-energy budget.

Context (see PWC.md §13, top bullet of "Status", and §8 "Black Holes and GW150914"):
PWC proposes that black holes absorbing/redistributing the cosmic medium during mergers
is a candidate mechanism for cosmic acceleration (mainstream "dark energy"). GW150914's
~3 solar-mass apparent deficit is real, measured energy release. The open question the
theory document flags but has NOT calculated: is the AGGREGATE of this effect, summed
over every black hole merger in the observable universe across cosmic history, anywhere
near the energy scale of dark energy? Or is it negligible by many orders of magnitude?

This script does that order-of-magnitude calculation with real numbers and cites sources
inline. It is a falsification test, not an advocacy piece: the numbers land where they
land.

Run: python blackhole_energy_budget.py
"""

import math

# ---------------------------------------------------------------------------
# 0. Physical constants and unit conversions (textbook / CODATA values, own
#    confident general knowledge — these are not in dispute).
# ---------------------------------------------------------------------------
c = 2.998e8            # speed of light, m/s
Msun = 1.989e30         # solar mass, kg
Mpc = 3.086e22           # megaparsec, m
Gpc = 3.086e25           # gigaparsec, m
yr = 3.156e7              # Julian year, s
Gyr = yr * 1e9

Msun_c2 = Msun * c**2   # rest-mass energy of one solar mass, J

print("=" * 78)
print("STEP 0: constants")
print("=" * 78)
print(f"  1 Msun c^2                = {Msun_c2:.4e} J")
print()

# ---------------------------------------------------------------------------
# 1. Black hole merger rate density.
#    Source: LIGO-Virgo-KAGRA GWTC-3 population paper, Abbott et al. 2023,
#    "The population of merging compact binaries inferred using GWTC-3",
#    Phys. Rev. X 13, 011048 (arXiv:2111.03634). Verified via web search
#    2026-09-10.
#      - Binary black hole (BBH) merger rate: 17.9-44 Gpc^-3 yr^-1 at a
#        fiducial redshift z=0.2 (90% credible range).
#      - Binary neutron star (BNS): 10-1700 Gpc^-3 yr^-1.
#      - NS-black hole (NSBH): 7.8-140 Gpc^-3 yr^-1.
#      - The BBH rate increases with redshift as (1+z)^kappa, kappa ~ 2.9,
#        for z <~ 1, meaning the LOCAL (z~0.2) rate used below systematically
#        UNDERESTIMATES the historical average rate at z~0.5-1.5 by a factor
#        of a few to ~10 (the specific star-formation-tracking peak). This
#        makes the total below conservative (an underestimate), which only
#        strengthens a "too small" verdict and is noted, not corrected for,
#        since we only need an order of magnitude.
#    We restrict to BBH mergers because, despite BNS having a much higher/
#    more uncertain rate, per-event energy for BNS/NSBH is ~30-100x smaller
#    (typically ~0.025-0.1 Msun c^2 radiated, vs a few Msun c^2 for BBH), so
#    BBH dominates the aggregate ENERGY budget even though it's not the most
#    numerous merger type. We take this into account by working with BBH
#    only, which is the dominant energy channel.
# ---------------------------------------------------------------------------
print("=" * 78)
print("STEP 1: BBH merger rate density (GWTC-3, Abbott et al. 2023, arXiv:2111.03634)")
print("=" * 78)
R_low, R_high = 17.9, 44.0   # Gpc^-3 yr^-1
R_fiducial = math.sqrt(R_low * R_high)  # geometric mean as a representative point estimate
print(f"  Reported 90% range: {R_low}-{R_high} Gpc^-3 yr^-1 (at z=0.2)")
print(f"  Fiducial point estimate (geometric mean): {R_fiducial:.1f} Gpc^-3 yr^-1")
print()

# ---------------------------------------------------------------------------
# 2. Energy released per merger.
#    Source: GW150914 discovery paper, Abbott et al. 2016, PRL 116, 061102 —
#    ~3 Msun c^2 radiated as gravitational waves, the number PWC's own §8
#    explicitly anchors to. We use this as the representative per-event
#    value, per the task's own framing ("a few solar masses x c^2").
#    Caveat stated plainly: GW150914 (total mass ~65 Msun) was an unusually
#    massive, energetic event; the GWTC-3 catalog's typical BBH total mass
#    is lower (~20-40 Msun), so a "typical" event likely radiates somewhat
#    less than 3 Msun c^2 (order 1-2 Msun c^2). We keep 3 Msun c^2 as the
#    stated reasonable assumption; the conclusion below does not hinge on
#    this factor of ~2.
# ---------------------------------------------------------------------------
print("=" * 78)
print("STEP 2: energy radiated per merger")
print("=" * 78)
E_per_merger_Msun = 3.0
E_per_merger = E_per_merger_Msun * Msun_c2
print(f"  Assumed {E_per_merger_Msun} Msun c^2 per merger (GW150914-like, Abbott et al. 2016)")
print(f"  = {E_per_merger:.4e} J per merger")
print()

# ---------------------------------------------------------------------------
# 3. Aggregate GW energy across the observable universe and cosmic history.
#    Observable universe comoving radius: ~46.5 billion light-years
#    (standard Planck-cosmology LambdaCDM figure, own confident general
#    knowledge / standard cosmology textbook value) ~= 14.3 Gpc.
#    Age of universe: 13.8 Gyr (Planck 2018).
#
#    Simplifying assumption (stated explicitly): treat the merger rate
#    density as constant at today's local value over the full 13.8 Gyr
#    history and across the full present-day comoving volume. This is a
#    genuine simplification — real BBH merger rate density rises with
#    redshift (per GWTC-3, (1+z)^2.9-ish) before turning over around
#    z~1-2 tracking cosmic star formation, then declines toward z=0. Using
#    the flat, LOCAL rate for the whole history and volume underestimates
#    the true integral by something like a factor of 3-10 (it misses the
#    star-formation-era enhancement), so this is a conservative (i.e.
#    favorable to the PWC mechanism) approximation for order-of-magnitude
#    purposes.
# ---------------------------------------------------------------------------
print("=" * 78)
print("STEP 3: aggregate BBH merger energy over cosmic history")
print("=" * 78)

R_obs_Gly = 46.5  # observable universe comoving radius, billion light-years
ly = c * yr
R_obs_m = R_obs_Gly * 1e9 * ly
R_obs_Gpc = R_obs_m / Gpc
print(f"  Observable universe comoving radius: {R_obs_Gly} Gly = {R_obs_Gpc:.2f} Gpc")

V_obs_Gpc3 = (4.0 / 3.0) * math.pi * R_obs_Gpc**3
V_obs_m3 = (4.0 / 3.0) * math.pi * R_obs_m**3
print(f"  Observable universe comoving volume: {V_obs_Gpc3:.3e} Gpc^3 = {V_obs_m3:.3e} m^3")

age_universe_Gyr = 13.8
age_universe_yr = age_universe_Gyr * 1e9

N_mergers_total = R_fiducial * V_obs_Gpc3 * age_universe_yr
print(f"  Assumed constant rate x volume x age (13.8 Gyr):")
print(f"  N_total mergers ~ {R_fiducial:.1f} Gpc^-3 yr^-1 x {V_obs_Gpc3:.3e} Gpc^3 x {age_universe_yr:.3e} yr")
print(f"                  ~ {N_mergers_total:.3e} mergers over cosmic history")

E_BH_total = N_mergers_total * E_per_merger
print(f"  Total aggregate BH-merger GW energy:")
print(f"    E_BH_total = N_total x E_per_merger = {E_BH_total:.3e} J")

# Sensitivity: low/high ends of the published rate range
N_low = R_low * V_obs_Gpc3 * age_universe_yr
N_high = R_high * V_obs_Gpc3 * age_universe_yr
E_BH_low = N_low * E_per_merger
E_BH_high = N_high * E_per_merger
print(f"  Sensitivity range (using published 17.9-44 Gpc^-3 yr^-1 bounds):")
print(f"    E_BH_total in [{E_BH_low:.3e}, {E_BH_high:.3e}] J")
print()

# ---------------------------------------------------------------------------
# 4. Dark energy budget: total dark-energy content of the observable
#    universe, using the given dark-energy density (~6e-10 J/m^3, ~68-70%
#    of critical density) times the observable universe's volume computed
#    above. Source: standard Planck-cosmology value, consistent with
#    Omega_Lambda ~ 0.68-0.70 and rho_crit ~ 8.6e-27 kg/m^3 (own confident
#    general knowledge / standard cosmology textbook figure, as given in
#    the task).
# ---------------------------------------------------------------------------
print("=" * 78)
print("STEP 4: total dark-energy content of the observable universe (benchmark)")
print("=" * 78)
rho_DE = 6e-10  # J/m^3
E_DE_total = rho_DE * V_obs_m3
print(f"  rho_DE = {rho_DE:.1e} J/m^3")
print(f"  V_obs  = {V_obs_m3:.3e} m^3")
print(f"  E_DE_total = rho_DE x V_obs = {E_DE_total:.3e} J")
print()

# ---------------------------------------------------------------------------
# 5. Sanity-check benchmark #2: cumulative stellar fusion energy output
#    across cosmic history, order of magnitude only.
#    Source for stellar mass density: Fukugita & Peebles 2004 (ApJ 616, 643)
#    / Madau & Dickinson 2014 review-level figure — present-day cosmic
#    stellar mass density is order a few x 10^8 Msun/Mpc^3; we use
#    5e8 Msun/Mpc^3 as a round order-of-magnitude figure (own confident
#    general knowledge of the standard value, not a specific new lookup).
#    Fusion efficiency: hydrogen -> helium mass defect is ~0.7% of rest
#    mass (standard nuclear-physics textbook value, Delta_m/m for
#    4p -> He4 = 0.0071).
#    We use total present-day stellar mass as a proxy for total mass ever
#    processed through fusion (an order-of-magnitude simplification -
#    ignores stellar remnants/recycling, correct to within a factor of a
#    few for this purpose).
# ---------------------------------------------------------------------------
print("=" * 78)
print("STEP 5: sanity-check benchmark - cumulative stellar fusion energy")
print("=" * 78)
rho_star_Msun_per_Mpc3 = 5e8   # Fukugita & Peebles 2004 / Madau & Dickinson 2014, order-of-magnitude
V_obs_Mpc3 = V_obs_m3 / Mpc**3
M_star_total_Msun = rho_star_Msun_per_Mpc3 * V_obs_Mpc3
print(f"  Cosmic stellar mass density: {rho_star_Msun_per_Mpc3:.1e} Msun/Mpc^3")
print(f"  V_obs = {V_obs_Mpc3:.3e} Mpc^3")
print(f"  Total stellar mass ever formed (proxy): {M_star_total_Msun:.3e} Msun")

fusion_efficiency = 0.007  # H -> He mass defect fraction, standard nuclear physics value
E_fusion_total = fusion_efficiency * M_star_total_Msun * Msun_c2
print(f"  H->He fusion efficiency: {fusion_efficiency} (mass defect fraction)")
print(f"  E_fusion_total = eff x M_star_total x c^2 = {E_fusion_total:.3e} J")
print()

# ---------------------------------------------------------------------------
# 6. Verdict.
# ---------------------------------------------------------------------------
print("=" * 78)
print("STEP 6: COMPARISON AND VERDICT")
print("=" * 78)
ratio_BH_to_DE = E_BH_total / E_DE_total
ratio_fusion_to_DE = E_fusion_total / E_DE_total
ratio_BH_to_fusion = E_BH_total / E_fusion_total

print(f"  E_BH_total (aggregate BBH merger energy, all history) = {E_BH_total:.3e} J")
print(f"  E_fusion_total (cumulative stellar fusion, sanity check) = {E_fusion_total:.3e} J")
print(f"  E_DE_total (total dark energy content, observable universe) = {E_DE_total:.3e} J")
print()
print(f"  E_BH_total / E_DE_total      = {ratio_BH_to_DE:.3e}  "
      f"({math.log10(1/ratio_BH_to_DE):.1f} orders of magnitude too small)")
print(f"  E_fusion_total / E_DE_total  = {ratio_fusion_to_DE:.3e}  "
      f"({math.log10(1/ratio_fusion_to_DE):.1f} orders of magnitude too small)")
print(f"  E_BH_total / E_fusion_total  = {ratio_BH_to_fusion:.3e}  "
      f"(BH aggregate is ~{1/ratio_BH_to_fusion:.0f}x smaller than cumulative fusion output)")
print()
print("  VERDICT:")
print("  Even using generous/conservative-in-PWC's-favor assumptions (flat local")
print("  merger rate applied across all history and volume, full 3 Msun c^2 per")
print("  event, BBH-only restriction to maximize energy per merger), the aggregate")
print("  black-hole-merger gravitational-wave energy output across the entire")
print("  observable universe's history falls short of the total dark-energy")
print(f"  budget by roughly {math.log10(1/ratio_BH_to_DE):.0f} orders of magnitude. It is also ~3-4 orders of")
print("  magnitude smaller than cumulative stellar fusion output -- which itself")
print("  was already checked elsewhere in this project (PWC.md SS13) and found to")
print("  be ~4-5 orders of magnitude short of the dark-energy scale, with no")
print("  redshift-dependence match to Pantheon+ data. Black hole mergers are an")
print("  even smaller energy channel than fusion, not a larger one.")
print()
print("  This mechanism is QUANTITATIVELY IMPLAUSIBLE as an explanation for dark")
print("  energy: not close, not 'needs a better model', but off by many orders of")
print("  magnitude, independent of any of the model's other assumptions about how")
print("  the released energy would even push space apart. The redshift-evolution")
print("  concern about the merger rate (a factor of ~3-10 undercount above) is")
print("  utterly dwarfed by an ~8-order-of-magnitude gap, so it cannot rescue this.")
