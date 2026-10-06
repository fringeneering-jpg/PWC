"""
DOMAIN JJ -- does the pairing redshift survive the arrival-rate test?

THE MECHANISM BEING TESTED, as stated by the author and not modified here:

  "Redshift is an expansion. Look up the fluid phases of liquid water, HDL
   and LDL ... It needs to find its exact opposite, the opposite charge,
   and phase into the medium. That's redshift. Not fucking time stretching.
   The reason it stretches is because the entropy enters the medium
   everywhere, not just one spot."

  "The mass is not wave count. I said HDL is volumetrically heavier ...
   It's a positive and a negative wave together."

Formalised from those two statements, with nothing added:

  - the medium is a lattice of PAIRED (+,-) electromagnetic waves
  - a photon is an UNPAIRED single chirality
  - a photon loses energy to the medium at a constant rate per unit PATH,
    every time it finds an available opposite and phases in
  - c is shared and constant (the shared-c postulate, c_s = c0)
  - geometry is static; a boundary maintains the pressure; space does not
    have to grow

That gives, with kappa the pairing rate per metre,

    dE/dx = -kappa*E      =>   1 + z = exp(kappa*D)
    small z:  z = kappa*D  =>   kappa = H0/c0     (Hubble law recovered)

Domain JJ does NOT test that. The Hubble law is recovered by construction --
any per-path energy loss recovers it, which is why it is not evidence. What
this domain tests is the one observable that per-path energy loss cannot
reach: the ARRIVAL RATE of successive photons.

WHY THAT IS THE DECISIVE TEST, AND WHY IT IS A THEOREM, NOT A FIT.

Two photons leave the same source dt apart. In a static geometry with a
single shared speed they traverse the SAME path at the SAME speed profile.
Identical travel time. They arrive dt apart. The arrival rate is unchanged
no matter how much energy each one loses on the way.

This holds even if c varies along the path, as long as c does not depend on
WHEN the photon was emitted: both photons see the same v(x) and integrate
to the same travel time. So no static medium of any density profile can
dilate arrival rates. It is a statement about the structure of the model,
not about any parameter in it.

Observation says arrival rates ARE dilated, by exactly (1+z).

EXTERNAL INPUTS. These are cited measurements. They are NOT re-derived from
data in this repository, and they are flagged as external everywhere below.

  [1] Goldhaber et al. 2001, ApJ 558, 359. Type Ia supernova light-curve
      width scales as (1+z)^b with b = 1.07 +/- 0.06.
  [2] Blondin et al. 2008, ApJ 682, 724. Spectral feature ageing rate of
      SNe Ia, independent of photometry, consistent with (1+z), no-dilation
      excluded.
  [3] Fujii et al. 2000 / Damour & Dyson 1996, Oklo natural reactor:
      |alpha_dot/alpha| <~ 1e-17 per year.
  [4] Lubin & Sandage 2001, AJ 122, 1084. Tolman surface-brightness test.

RULE FOLLOWED HERE: the conclusion text is written AFTER the numbers print.
Twice in this project it was written before, and both times it was wrong.
"""
import json
import os

import numpy as np

D_OUT = os.environ.get("PWC_SPARC_DIR", os.path.dirname(os.path.abspath(__file__)))

c0 = 2.99792458e8            # m/s
MPC = 3.0856775814913673e22  # m
YR = 3.155693e7              # s

H0_PLANCK = 67.4             # km/s/Mpc
H0_SH0ES = 73.0              # km/s/Mpc

# external, cited
B_OBS = 1.07
B_ERR = 0.06
ALPHA_DOT_BOUND = 1.0e-17    # per year

results = {}


def hr(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


def h0_si(h0_kms_mpc):
    return h0_kms_mpc * 1000.0 / MPC


# ---------------------------------------------------------------- 1
hr("1. THE PAIRING RATE kappa, FIXED BY THE HUBBLE LAW")

print("kappa = H0/c0 is not fitted here. It is forced: a constant per-path")
print("energy loss reproduces v = H0*D at small z for exactly one kappa.\n")
print(f"{'H0 source':<12} {'H0 [km/s/Mpc]':>14} {'H0 [1/s]':>12} "
      f"{'kappa [1/m]':>13} {'1/kappa [Gpc]':>14}")
kappa = {}
for name, h0 in (("Planck", H0_PLANCK), ("SH0ES", H0_SH0ES)):
    hs = h0_si(h0)
    k = hs / c0
    kappa[name] = k
    mfp_gpc = (1.0 / k) / (1000.0 * MPC)
    print(f"{name:<12} {h0:>14.1f} {hs:>12.4e} {k:>13.4e} {mfp_gpc:>14.3f}")

print("\nMean free path for one pairing event is of order the Hubble length.")
print("That is a consistency check, not a prediction: it is what kappa = H0/c0")
print("means. It buys the model nothing.")

results["kappa_planck_per_m"] = kappa["Planck"]
results["kappa_sh0es_per_m"] = kappa["SH0ES"]

# ---------------------------------------------------------------- 2
hr("2. ARRIVAL-RATE DILATION PREDICTED BY A STATIC MEDIUM")

print("Setup: source emits two photons dt apart. Static geometry, path D,")
print("speed profile v(x) that does not depend on emission epoch.\n")
print("  T = integral_0^D dx/v(x)   is the SAME for both photons")
print("  => dt_arrive = dt_emit   => width ratio W(z)/W(0) = 1 = (1+z)^0\n")
print("This is exact and holds for ANY v(x) and ANY kappa. It is not")
print("sensitive to a parameter choice, so there is nothing to tune.\n")

b_static = 0.0
n_sigma = abs(B_OBS - b_static) / B_ERR
print(f"  predicted exponent b_static = {b_static:.1f}")
print(f"  observed  exponent b_obs    = {B_OBS:.2f} +/- {B_ERR:.2f}   [ext. ref 1]")
print(f"  tension                     = {n_sigma:.1f} sigma")

# generosity check: even if the cited error bar were badly underestimated
for infl in (2, 3, 5):
    print(f"    if the quoted error were {infl}x larger: "
          f"{abs(B_OBS - b_static) / (B_ERR * infl):.1f} sigma")

results["b_static_prediction"] = b_static
results["b_observed"] = B_OBS
results["b_observed_err"] = B_ERR
results["static_tension_sigma"] = n_sigma

# ---------------------------------------------------------------- 3
hr("3. THE ONLY SALVAGE: c MUST DEPEND ON EMISSION EPOCH")

print("The theorem in section 2 has exactly one loophole. If v depends on")
print("cosmic TIME, the two photons no longer see the same profile, and the")
print("travel time becomes a function of emission epoch t_e:\n")
print("    dt_arrive/dt_emit = 1 + dT/dt_e\n")
print("Dilation by (1+z) therefore requires dT/dt_e = z. With T ~ D/c and")
print("D fixed by the static geometry,\n")
print("    dT/dt_e = -D * cdot / c^2 = z = kappa*D")
print("    =>  cdot/c = -kappa*c = -H0\n")
print("So c must DECAY as exp(-H0*t). There is no freedom in this: the")
print("required rate is fixed by the same kappa that fixed the Hubble law.\n")

print("Under the master relation c^2 = K/rho at constant stiffness K:")
print("    rho_medium ∝ exp(+2*H0*t)")
print("the medium must be DENSIFYING at 2*H0. That is at least the right")
print("direction for 'entropy enters the medium everywhere'.\n")

print("It is also the opposite of what pwc_redshift_timing_falsification.py")
print("assumed. That script tested v(rho) = c0*sqrt(rho0/rho) with a THINNING")
print("medium and found the dilation sign wrong. This says why: a thinning")
print("medium lets later photons catch up, which CONTRACTS arrival spacing.")

for name, k in kappa.items():
    hs = k * c0          # kappa = H0/c0, so kappa*c0 IS H0 in 1/s already
    print(f"\n  [{name}]  required -cdot/c = H0 = {hs:.4e} /s "
          f"= {hs * YR:.4e} /yr")
    print(f"           required d ln rho/dt = 2*H0 = {2 * hs * YR:.4e} /yr")

results["required_cdot_over_c_per_yr_planck"] = -h0_si(H0_PLANCK) * YR
results["required_dlnrho_dt_per_yr_planck"] = 2 * h0_si(H0_PLANCK) * YR

# ---------------------------------------------------------------- 4
hr("4. WHAT THAT SALVAGE COSTS: alpha = e^2/(4*pi*eps0*hbar*c)")

print("If c alone decays at H0 and e, eps0, hbar are held fixed, then")
print("alpha ∝ 1/c grows at +H0.\n")
adot_planck = h0_si(H0_PLANCK) * YR
adot_sh0es = h0_si(H0_SH0ES) * YR
print(f"{'H0 source':<12} {'alpha_dot/alpha [1/yr]':>24} "
      f"{'Oklo bound':>14} {'excess':>12}")
for name, ad in (("Planck", adot_planck), ("SH0ES", adot_sh0es)):
    print(f"{name:<12} {ad:>24.4e} {ALPHA_DOT_BOUND:>14.1e} "
          f"{ad / ALPHA_DOT_BOUND:>12.2e}x")

print("\n[ext. ref 3] Oklo constrains alpha_dot/alpha to ~1e-17 per year.")
print("The required rate overshoots it by about seven orders of magnitude.")
print("\nThe standard escape is real and must be stated: if e, eps0 and hbar")
print("co-vary so that alpha is exactly constant, nothing local changes and")
print("the Oklo bound says nothing. But then c(t) is unobservable by")
print("construction, and 'the medium densifies' and 'the metric expands'")
print("are the same statement in two gauges. The model would not have")
print("REPLACED expansion. It would have RENAMED it.")

results["alpha_dot_required_per_yr_planck"] = adot_planck
results["alpha_dot_oklo_bound_per_yr"] = ALPHA_DOT_BOUND
results["alpha_dot_excess_factor_planck"] = adot_planck / ALPHA_DOT_BOUND

# ---------------------------------------------------------------- 5
hr("5. TOLMAN SURFACE BRIGHTNESS, FOR THE RECORD")

print("Static Euclidean geometry, per-path energy loss only:")
print("  flux          ∝ (1+z)^-1   (energy per photon)")
print("  arrival rate  ∝ (1+z)^0    (section 2 theorem)")
print("  solid angle   ∝ (1+z)^0    (no metric, angular size = l/D)")
print("  => SB ∝ (1+z)^-1\n")
print("Metric expansion gives (1+z)^-4: two powers from flux, two from")
print("D_L = (1+z)^2 * D_A.\n")
zs = np.array([0.1, 0.3, 0.5, 1.0, 1.5, 2.0])
print(f"{'z':>6} {'SB static (1+z)^-1':>20} {'SB expansion (1+z)^-4':>24} "
      f"{'ratio':>10}")
for z in zs:
    s = (1 + z) ** -1.0
    e = (1 + z) ** -4.0
    print(f"{z:>6.1f} {s:>20.4f} {e:>24.6f} {s / e:>10.2f}")

print("\n[ext. ref 4] Lubin & Sandage report a raw R-band exponent near -2.3")
print("and attribute the remainder to luminosity evolution. That test needs")
print("an evolution correction, so it is WEAKER evidence than section 2 and")
print("is recorded here only for completeness. The light-curve width test")
print("needs no such correction: it measures a clock, not a brightness.")

results["sb_exponent_static"] = -1.0
results["sb_exponent_expansion"] = -4.0

# ---------------------------------------------------------------- 6
hr("6. VERDICT")

print("Written after the numbers above, not before.\n")
print(f"1. The static pairing mechanism predicts NO light-curve time")
print(f"   dilation. Observation says (1+z)^{B_OBS:.2f}+/-{B_ERR:.2f}. That is")
print(f"   {n_sigma:.0f} sigma, and it stays above 5 sigma even if the quoted")
print(f"   error bar is off by a factor of 3. As stated -- static medium,")
print(f"   shared constant c, per-path pairing -- the mechanism is dead.")
print()
print("2. It is dead for a structural reason, not a numerical one. Two")
print("   photons on one path in a static medium cannot arrive at a")
print("   different spacing than they left. No value of kappa, no density")
print("   profile, and no pairing cross-section changes that.")
print()
print("3. Exactly one loophole exists and it is fully determined, not free:")
print("   c must decay as exp(-H0*t), equivalently the medium must densify")
print("   as exp(+2*H0*t). Notably this is the OPPOSITE sign to the thinning")
print("   medium assumed in pwc_redshift_timing_falsification.py, which")
print("   explains that script's wrong-sign result rather than excusing it.")
print()
print(f"4. That loophole costs alpha_dot/alpha = {adot_planck:.2e} /yr against")
print(f"   an Oklo bound of {ALPHA_DOT_BOUND:.0e} /yr -- over by "
      f"{adot_planck / ALPHA_DOT_BOUND:.0e}x -- unless every other constant")
print("   co-varies to hide it. If they do co-vary, the mechanism is")
print("   observationally identical to metric expansion and is a relabelling.")
print()
print("5. WHAT THIS DOES NOT TOUCH. The pairing picture may still be the")
print("   right account of WHY the medium densifies, and the (+,-) pair")
print("   lattice is untested here either way. What is ruled out is the")
print("   specific claim that redshift is a static per-path process and")
print("   'not time stretching'. The data require a clock change. A medium")
print("   model has to produce one.")
print()
print("6. NOT FIXED, STILL OPEN: m_wave. Without the mass of a single")
print("   medium pair, rho0 cannot be turned into a pair number density,")
print("   and kappa = n_avail * sigma cannot be split into its two factors.")
print("   Domain II's two routes to that number disagree by ~1.5e6 and")
print("   neither is adopted here. Nothing in Domain JJ depends on it --")
print("   that is why this test could be run while that blocker stands.")

out = os.path.join(D_OUT, "domain_JJ_redshift_arrival_rate_results.json")
with open(out, "w") as f:
    json.dump(results, f, indent=2, sort_keys=True)
print(f"\nwrote {out}")
