"""
PWC: heat as the slow channel, and the RATE criterion it forces on knot
formation.

WHAT THIS ADDS
--------------
Everything in this repo so far constrains a RESTING STATE. dG* is a barrier
height. G(R) = (4pi/3)P0 R^3 + 4 pi sigma R^2 + A/R has a unique minimum.
The tying/untying asymmetry is about barrier heights. None of it says how
FAST anything has to happen.

This file adds the first constraint on a PROCESS. It says the slam must
outrun heat, not just outweigh surface tension -- a velocity threshold
alongside the pressure threshold. Two conditions where there was one.

THE TERMS AND WHERE THEY CAME FROM  (stated before computing)
--------------------------------------------------------------
  t_diff = R^2/alpha, t_mech = R/v, Pe = t_diff/t_mech = vR/alpha
      Ratio of two timescales. Definitional. Nothing physical assumed.

  alpha = c0*lambda/3
      Kinetic theory for carriers moving at speed c0 with mean free path
      lambda. In PWC heat is not a second substance: it is already LDF
      (the unpaired propagating state -- photons, current, heat). LDF is
      light, so its carriers move at c0 and nothing else. Heat is slow
      because transport is DIFFUSIVE, not ballistic: short mean free path,
      random walk. Photons take ~1e5 years to leave the Sun while moving
      at c the entire way. One substance, one speed, slow transport.

  lambda = 2.818e-15 m
      NOT a new parameter. It is this repo's own blocking threshold,
      rho > m_p/lambda^3 = 7.475e16 kg/m^3 (domain II, PROVENANCE_MANIFEST
      line ~2526), solved for lambda.

  adiabatic T ~ V^(1-gamma)
      First law with Q = 0. Used ONLY in section 1, and its naive answer
      is reported as WRONG.

  v_freefall = sqrt(2GM/r)
      Newtonian. Used in section 3 as a PROXY for compression speed, and
      flagged as a proxy. Newtonian gravity is already used throughout this
      repo (g = GM/r^2 in the shell scaling). It is not the import that got
      domain NN retracted -- that was the FLRW scale factor, de Sitter, and
      Unruh/Gibbons-Hawking, none of which appear here.

NOT USED: general relativity, MOND, LambdaCDM, a0, any horizon, any
temperature of any horizon, any halo profile, any fitted parameter.
"""
import numpy as np

c0   = 2.99792458e8
G    = 6.67430e-11
m_p  = 1.67262192369e-27
M_sun = 1.98892e30
R_e   = 1.930796e-13          # electron knot radius, from knot_existence file

lam   = (m_p/7.475e16)**(1.0/3.0)
alpha = c0*lam/3.0

L = lambda s='-': print(s*72)
L('='); print("PWC THERMAL RATE CRITERION"); L('=')

# ===================================================================== 1
print("\n1. THE MECHANISM, CHECKED WHERE IT IS DIRECTLY OBSERVED")
L()
print("""Single-bubble sonoluminescence: argon in water, 26.5 kHz. The bubble
grows slowly and collapses in nanoseconds. If heat is a slow channel, growth
should be isothermal (heat has time to come IN) and collapse adiabatic (heat
cannot get OUT). That is a falsifiable statement about two Peclet numbers.

CORRECTION LOGGED: the first version of this check used argon's diffusivity
at STP for BOTH phases and got Pe = 4.2 for growth -- which would have meant
no isothermal phase and no asymmetry. That was wrong: alpha ~ 1/rho, and the
bubble at maximum radius is far more rarefied than ambient. Corrected below.""")

R0, R_max, R_min = 4.5e-6, 40e-6, 0.5e-6     # ambient, max, min radius
a_stp   = 2.0e-5                              # argon, ~STP
t_grow  = 0.5/26.5e3
v_coll  = 1000.0
R_mid   = 5e-6

a_grow = a_stp*(R_max/R0)**3                  # alpha ~ 1/rho ~ R^3
a_coll = a_stp*(R_mid/R0)**3
print(f"\n   rarefaction at R_max: rho/rho_0 = {(R0/R_max)**3:.2e}"
      f"  ->  alpha = {a_grow:.3e} m^2/s")
print(f"   at R_mid during collapse:        ->  alpha = {a_coll:.3e} m^2/s")

Pe_grow = (R_max**2/a_grow)/t_grow
Pe_coll = (R_mid**2/a_coll)/(R_mid/v_coll)
print(f"\n   {'phase':<10}{'t_mech':>12}{'t_diff':>14}{'Pe':>12}   regime")
print(f"   {'growth':<10}{t_grow*1e6:10.2f} us{R_max**2/a_grow*1e6:12.3f} us"
      f"{Pe_grow:12.4f}   isothermal, heat IN")
print(f"   {'collapse':<10}{R_mid/v_coll*1e9:10.2f} ns{R_mid**2/a_coll*1e9:12.1f} ns"
      f"{Pe_coll:12.1f}   adiabatic, heat TRAPPED")
print(f"\n   separation between regimes: {Pe_coll/Pe_grow:.3e}")
print("""
   Slow absorption, violent expulsion, separated by four orders of
   magnitude. The mechanical picture is confirmed.""")

gam, T0 = 5.0/3.0, 300.0
T_ad = T0*(R_max/R_min)**(3*(gam-1))
print(f"\n   NEGATIVE IN THE SAME CHECK:")
print(f"   naive adiabatic endpoint T = T0 (Rmax/Rmin)^(3(g-1)) = {T_ad:.3e} K")
print(f"   measured SBSL                                       ~ 1e4 - 1e5 K")
print(f"   overshoot ~{T_ad/3e4:.0f}x. Collapse is not perfectly adiabatic and the")
print( "   energy goes into dissociation and ionisation, not temperature.")
print( "   The MECHANISM survives; the ARITHMETIC does not. Do not quote it.")
print("""
   Also, and this matters: adiabatic bubble collapse is STANDARD physics.
   Reproducing it is a consistency check on PWC's picture, not evidence
   for PWC over anything else. It earns the right to use the criterion
   below. It is not a win.""")

# ===================================================================== 2
print("\n2. THE CRITERION IN THE MEDIUM -- ZERO FREE PARAMETERS")
L()
print(f"   lambda (from this repo's m_p/lambda^3 = 7.475e16) = {lam:.4e} m")
print(f"      for reference, the classical electron radius   = {2.8179403262e-15:.4e} m")
print(f"   alpha = c0*lambda/3                               = {alpha:.4e} m^2/s")
print(f"      scale check: water 1.4e-07, air 2.0e-05, copper 1.1e-04 m^2/s")
print(f"""
   Compression stores work only while heat cannot escape:

       v  >  alpha / R

   {'R [m]':>12}{'v_crit [m/s]':>16}{'v_crit/c0':>14}""")
for R in (1e-15, 3e-15, 1e-14, 1e-13, R_e, 1e-12, 1e-10, 1e-6):
    vc = alpha/R
    tag = "  IMPOSSIBLE (> c0)" if vc > c0 else ""
    print(f"   {R:12.2e}{vc:16.3e}{vc/c0:14.5f}{tag}")
print(f"""
   At the electron knot radius: v_crit = {alpha/R_e:.3e} m/s = {alpha/R_e/c0:.4f} c.

   The sign is the useful part. SMALL regions leak fastest, so below
   ~{alpha/c0:.2e} m the required speed exceeds c0 and NOTHING can be
   compressed adiabatically at any speed. That is a floor on knot size, and
   it is a different floor from the one in knot_existence_pressure_confinement
   (which came from A/R forbidding R -> 0). Two independent floors that do
   not contradict each other is worth something; they are not the same
   argument wearing a hat.""")

# ===================================================================== 3
print("\n3. DOES THE SLAM ACTUALLY CLEAR THE BAR? -- AND HOW RARE THAT IS")
L()
print("""PROXY WARNING, read it: what the criterion needs is the COMPRESSION
speed. What is computed here is Newtonian free-fall speed sqrt(2GM/r). Those
are not the same quantity. Free-fall is a reasonable scoping proxy for how
violently the medium is being driven near a compact object, and nothing more.
If the real compression speed is much below free-fall, everything in this
section moves. Treat it as scoping, not derivation.""")
v_crit_e = alpha/R_e
print(f"\n   bar to clear: v_crit = {v_crit_e:.3e} m/s")
print(f"\n   {'M [Msun]':>10}{'r where v_ff = v_crit [m]':>28}{'in R_sun':>12}")
for M in (1.0, 28.118, 1e6, 1e9):
    r_crit = 2*G*M*M_sun/v_crit_e**2
    print(f"   {M:10.4g}{r_crit:28.3e}{r_crit/6.957e8:12.3e}")
print("""
   So the criterion is CLEARED, easily, anywhere near a compact object --
   out to ~1e9 m around a stellar-mass core. It does not kill knot creation.

   But it is not vacuous either, and this is the point: it says creation can
   ONLY happen inside those regions, never in ordinary space. That turns
   "very rare though" from a word into a volume fraction.""")
n_star = 0.1/2.938e49        # ~0.1 stars per pc^3, in m^-3
r1 = 2*G*1.0*M_sun/v_crit_e**2
f_vol = n_star*(4.0/3.0*np.pi*r1**3)
print(f"   local stellar number density ~0.1 /pc^3 = {n_star:.3e} /m^3")
print(f"   r_crit for 1 Msun                        = {r1:.3e} m  ({r1/6.957e8:.3f} R_sun)")
print(f"   volume fraction of space above threshold = {f_vol:.2e}")
print(f"""
   ~1e{int(np.floor(np.log10(f_vol)))} of space. Note r_crit for one solar mass sits INSIDE
   the star, so for ordinary stars the region is buried and unavailable
   anyway -- the accessible cases are compact objects, which is where this
   framework already puts matter creation.

   This is a scoping number built on a proxy, not a measurement. It is
   quoted to show the criterion has teeth, not to claim a rate.""")

# ===================================================================== 4
print("\n4. CLAIMS THIS KILLS -- LOGGED SO THEY ARE NOT REVIVED")
L()
Y = 15.0*4.184e12
R_fb = 100.0
E_air = 1.2*(4/3*np.pi*R_fb**3)*718.0*300.0
print(f"""a) NUCLEAR DETONATION AS INWARD HEAT ABSORPTION -- FALSE.
   15 kt yield                                    = {Y:.3e} J
   ALL thermal energy in the whole fireball volume = {E_air:.3e} J
   ratio                                           = {E_air/Y*100:.2f} %
   Even drawing in every joule from its entire fireball, atmospheric heat
   supplies under 2% of the yield. And the yield already closes on the mass
   defect alone: fission of ~1 kg U-235 at ~200 MeV per event gives ~17 kt,
   which is the measured number. There is nothing for inward heat to do.
   The inward flow that IS observed -- the afterwind -- is buoyancy, occurs
   AFTER the fireball rises, and carries a negligible fraction of the yield.
   Right observation, wrong order, wrong magnitude.

b) VOLCANIC LIGHTNING AS ENERGY ARCING INTO EXPELLED HEAT -- FAILS AN
   EXISTING OBSERVATIONAL TEST. Lightning rate tracks ASH CONTENT, not heat:
   ash-poor phreatic plumes produce far less lightning than ash-rich ones.
   And the hottest point of an eruption is the vent, while the lightning
   concentrates up in the plume. If the mechanism were energy seeking
   expelled heat, it would be brightest and densest at the vent. It is not.

c) COSMIC EXPANSION AS A THERMAL CAVITATION CYCLE -- CONTRADICTS THIS REPO.
   PWC already says expansion is knot untying injecting volume into a
   pressurised medium. A thermal absorb/collapse cycle is a DIFFERENT
   mechanism for the same observable. One must go, or they must be shown to
   be the same process. Separately: expansion is observed monotonic and
   accelerating over ~13 Gyr with no collapse phase ever seen, so if the
   cycle's period exceeds the age of the universe the claim is not testable.
   NOT RESOLVED HERE. Flagged, not patched.""")

# ===================================================================== 5
print("\n5. WHAT WOULD KILL THIS FILE")
L()
print(f"""  - If the real compression speed at a creation site is below
    {v_crit_e:.2e} m/s, section 3 inverts and knot creation is forbidden
    where PWC says it happens. Section 3 uses a PROXY; replacing it with an
    actual compression speed is the single most valuable next calculation.
  - If the mean free path is not lambda, alpha is a free parameter and the
    zero-parameter claim in section 2 dies. lambda = 2.818e-15 m coming out
    equal to the classical electron radius is noted and NOT claimed as a
    result; nothing here derives it.
  - If heat is ever treated as a second substance rather than the kinetic
    content of LDF, this file is incoherent with the rest of the framework.
    One continuum. That constraint is load-bearing, not stylistic.
  - Nothing in this file has been tested against an observation that was not
    already explained by standard physics.""")
L('=')
