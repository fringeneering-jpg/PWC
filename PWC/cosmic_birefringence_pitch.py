"""
PWC and cosmic birefringence: what survives, what was withdrawn, and the one
number that needs no wave size.

STATUS OF THE MEASUREMENT -- read this before quoting anything below.
---------------------------------------------------------------------
beta ~ 0.35 +/- 0.14 deg. Minami & Komatsu 2020 at 2.4 sigma; later
Planck+WMAP combined analyses tighten it toward ~3.6 sigma. This is NOT a
detection. The dominant systematic is the instrument's absolute
polarization-angle calibration. Nothing in this file may be quoted as
support for PWC until the measurement clears 5 sigma. It is a hook, not
evidence.

WHY IT IS INTERESTING FOR PWC AT ALL
------------------------------------
A pure vacuum cannot rotate the polarization plane; standard EM forbids it.
The standard explanations are an axion-like field or quintessence. NOTE,
because getting this wrong is how the argument gets dismissed: the axion
was NOT invented for this. Peccei-Quinn, 1977, for the strong CP problem,
forty years earlier. "Another ghost particle bolted on" is the weak form of
the argument and it is wrong on the history.

The strong form: standard vacuum has NO handedness available. PWC's medium
does -- Williamson's double-loop toroid carries a definite chirality (that
is where his spin hbar/2 comes from), and a paired EM(+)/EM(-) medium can
carry a global handedness in how the pairs lock. Neither is bolted on; both
predate the observation inside this framework. And a chiral medium has a
SIGN, so it can be wrong: beta is measured positive.

THREE ARGUMENTS WITHDRAWN ALONG THE WAY -- kept so they are not revived
-----------------------------------------------------------------------
W1. "Space is a structured lattice, lattices are birefringent, therefore
    rotation." NO. Calcite and stressed glass are LINEARLY birefringent --
    different index for two orthogonal LINEAR polarizations, which retards
    phase and makes linear light elliptical. It does NOT rotate the plane,
    and it is parity-EVEN. Calcite is birefringent and is not optically
    active. Structure is not enough. HANDEDNESS is what is required.

W2. "The resting medium has no inertial mass, so no dispersion, so the
    rotation is achromatic." NO, twice over.
    (a) It inverts. theta = pi*Lp*dn/lambda. Constant dn (no dispersion)
        gives theta ~ 1/lambda, which is STRONGLY chromatic -- the opposite
        of what the argument was invoked to supply. It predicts
        beta(353 GHz) = 3.53 * beta(100 GHz), and Eskilt 2022 measured
        beta band-by-band across exactly that range and found no frequency
        dependence. Excluded by data in hand.
    (b) It breaks PWC. c0^2 = K/rho (PWC.md 2, 4). rho = 0 gives infinite
        c0. The medium's density is what SETS c0, and PWC.md 4 says a
        photon has "the same molecular mass" at LOWER density, not zero.

W3. "Twist per lattice cell must be ~4e-44 rad, and topological quantities
    are O(1), so the topology argument fails." THIS WAS MY OWN ERROR and it
    is withdrawn for two independent reasons:
    (a) It used lambda = 2.818e-15 m as the cell size. That came from a
        DENSITY threshold; PWC has never fixed the wave size.
    (b) Deeper: decomposing a geometric phase into per-cell twists is the
        wrong operation. A Berry phase is a property of the PATH, not a sum
        of local rotations -- that is what makes it topological. Computing
        "radians per cell" reimported the circular-index-difference picture
        that W2 had just abandoned. There is no per-cell fine-tuning to
        answer because there are no cells in that description.

WHAT ACHROMATIC ACTUALLY REQUIRES
---------------------------------
theta independent of lambda  <=>  dn proportional to lambda. That is not a
refractive index difference; it is a phase accumulated along the path. It
is why the axion term (F F-dual) gives an achromatic angle. So the standing
requirement on PWC is specific and statable: the handedness must enter as a
geometric/topological phase, NOT as a circular index difference. There are
real precedents for achromatic geometric polarization rotation
(Rytov-Vladimirskii-Berry in helical fibres; Mauguin adiabatic following in
twisted nematics, which is why TN-LCDs work across the visible). The
category is legitimate. PWC has not done the calculation.
"""
import numpy as np
c = 2.99792458e8
L = lambda s='-': print(s*72)

beta_deg, beta_err = 0.35, 0.14
beta  = np.radians(beta_deg)
D     = 4.32e26          # comoving distance to last scattering, m
R_hor = 4.35e26          # comoving horizon radius, m
Gly   = 9.461e15*1e9

L('='); print("THE ONE NUMBER THAT NEEDS NO WAVE SIZE"); L('=')
rate = beta/D
print(f"\n   beta                  = {beta_deg} +/- {beta_err} deg ({beta_deg/beta_err:.1f} sigma, NOT a detection)")
print(f"   path                  = {D:.3e} m")
print(f"   rotation rate         = {rate:.4e} rad/m")
print("""
   That is beta divided by a path length. No lattice spacing, no wave
   size, no mean free path, no assumption about the medium's granularity.
   It is the observation and nothing else. It is the only quantity in this
   file that survived every withdrawal above.""")

l_rad, l_turn = 1.0/rate, 2*np.pi/rate
print(f"\n   length per radian     = {l_rad:.4e} m = {l_rad/Gly:.0f} Gly")
print(f"   length per full turn  = {l_turn:.4e} m = {l_turn/Gly:.0f} Gly")
print(f"   full turn / horizon   = {l_turn/R_hor:.0f}")

L(); print("   WHY THE PITCH EXCEEDING THE HORIZON IS STRUCTURALLY RIGHT")
L()
print("""   A geometric phase is not a free amplitude -- it is an angle set by the
   geometry, so the medium's handedness has a PITCH, and the observation
   fixes it. If that pitch were SHORTER than the horizon there would be
   DOMAINS: patches of sky with different beta, some with opposite sign.
   beta is measured uniform across the sky. A pitch far exceeding the
   horizon is exactly what a uniform beta requires.

   That is a real structural consistency and it costs nothing. It is not
   yet a prediction.""")

L(); print("   THE HYPOTHESIS -- NOT A RESULT, AND NOT TO BE QUOTED AS ONE")
L()
print(f"""   PWC's medium is BOUNDED. "Nothing is infinite": the boundary is what
   maintains P0, and P0 is the lam^+3 term that forbids R -> infinity in
   knot_existence_pressure_confinement.py. A bounded medium carrying one
   global handedness has exactly ONE natural pitch -- its own size.

   IF the chiral pitch is the boundary, beta measures it:

       full turn     {l_turn:.3e} m  = {l_turn/Gly:.0f} Gly
       one radian    {l_rad:.3e} m  = {l_rad/Gly:.0f} Gly

   WHAT THIS IS: a hypothesis that ties beta to a SECOND quantity, which
   is what makes it worth anything. If PWC ever pins the boundary another
   way -- from P0, from rho_min, from the knot functional -- the two
   numbers must agree or the picture is dead.

   WHAT THIS IS NOT: a measurement, a derivation, or support for PWC.
   Nothing derives the identification "pitch = boundary". It is named so
   it can be killed. The 'IF' is the whole content.""")

L(); print("   REJECTED: THE THERMAL JUSTIFICATION FOR THE TWIST")
L()
print("""   Proposed: the twist is the thermodynamic resting state of the paired
   EM(+)/EM(-) waves, maintained by heat returning as knots untie.

   REJECTED, on two counts that are both PWC's own:
   1. It makes chirality TEMPERATURE DEPENDENT, so beta would vary with
      the thermal history of each line of sight -- hotter through clusters
      and filaments, colder through voids. That predicts ANISOTROPIC beta
      correlated with large-scale structure. beta is measured isotropic.
      To survive, the coupling must be weak enough to hide -- which means
      it is doing no work, which means it is not the explanation. It
      converts a clean uniform prediction into one that must explain why
      it looks uniform.
   2. It leans on knot-untying returning heat to the medium, and PWC.md
      13 already killed untying against real Pantheon+ data: "no support
      -- dark-energy w stays flat while star-formation rate changes 4x
      over the same span."

   The bounded-medium pitch above supplies a number. The thermal story
   supplies none and costs an anisotropy prediction. Keep the first.""")

L(); print("   LOGGED, NOT CLAIMED")
L()
alpha = 7.2973525693e-3
print(f"   alpha in radians = {np.degrees(alpha):.4f} deg")
print(f"   beta             = {beta_deg} +/- {beta_err} deg")
print(f"   separation       = {abs(np.degrees(alpha)-beta_deg)/beta_err:.2f} sigma")
print(f"\n   and, if rotation DID accumulate per cell (it does not -- see W3),")
print(f"   a twist of alpha per cell implies a cell of {alpha/rate:.3e} m")
print(f"   = {alpha/rate/R_hor:.2f} horizon radii.")
print("""
   No mechanism behind either. Same bin as lambda coming out equal to the
   classical electron radius. If beta firms up at 5 sigma on 0.4181 deg it
   is a hit; at 0.25 deg it is dead. Not quotable until then.""")

L(); print("   WHAT WOULD KILL THIS FILE")
L()
print("""  - beta failing to reach 5 sigma, or landing far from 0.35 deg.
  - any measured frequency dependence of beta: that kills the geometric
    route and returns us to an index difference, which W2 already excluded.
  - measured ANISOTROPY of beta correlated with large-scale structure:
    kills the global-pitch picture (though it would revive the thermal one).
  - PWC pinning its boundary independently at a value that disagrees with
    the pitch above. That is the test this file exists to set up.
  - Nothing here is a calculation from PWC's own mechanics. The geometric
    phase has been named as the required category. It has not been derived
    from the pairing geometry, and until it is, this file records a
    constraint, not a prediction.""")
L('=')
