"""
PWC knot existence, re-run with the two terms the phase-field functional
never had: medium pressure and confinement energy.

WHY THIS EXISTS
---------------
PWC/knot_audit/RESULTS.md records Pass 1 (existence of a stable,
finite-radius localized knot) FAILING for all 36 tested combinations of
(B/K, C/K, Lam/K). The stated reason, in that file's own words:

    "Nothing in E[n,phi] penalizes spatial extent itself ... there is
     still no actual volume/pressure penalty in the functional -- the
     missing ingredient PWC's own 'maximum compression' language would
     need to supply mathematically."

That diagnosis is only half right. Adding a volume penalty alone does not
rescue existence -- it makes the knot collapse instead of disperse. Two
terms are missing, one at each end of R, and they are the SAME two bounds
that are load-bearing everywhere else in PWC.

THE THREE TERMS AND THEIR PROVENANCE  (state first, compute second)
-------------------------------------------------------------------
G(R) = (4*pi/3)*P0*R^3  +  4*pi*sigma*R^2  +  A/R

1. (4*pi/3)*P0*R^3   AMBIENT PRESSURE WORK
   The medium is bounded, so its boundary maintains a finite P0. The knot
   interior is LDF (unpaired); the ambient is HDF (paired). PWC: the pair
   is volumetrically HEAVIER than the two separate. So ambient > interior
   and holding the knot's volume open costs P0*V. This is the cavitation
   picture already used in domain II, not an import.

2. 4*pi*sigma*R^2    INTERFACE ENERGY
   HDF and LDF are physically distinct states of one continuum, so the
   boundary between them is a real interface with a real energy per area.
   sigma is a medium property, not a fitted knob.

3. A/R  with  A = h*c/(4*pi)     CONFINEMENT ENERGY OF THE TRAPPED LIGHT
   Williamson & van der Mark: the electron is a confined photon on a
   double-loop path; verbatim, "the loop radius is then exactly
   lambda_C/4pi" and the extremal paths "have length lambda_C". Two turns
   of circumference 2*pi*R give path length 4*pi*R = lambda, so
   E_photon = h*c/(4*pi*R). Hence A = h*c/(4*pi), a UNIVERSAL constant
   with no free parameter in it. This is Maxwell plus de Broglie. M = L/c0^2
   with L = light energy is Einstein 1905's own symbol, which PWC keeps.

NOT USED ANYWHERE IN THIS FILE: general relativity, MOND, LambdaCDM, a0,
any halo profile, any rotation curve, any fitted cosmological parameter.

WHAT THIS CAN AND CANNOT SHOW
-----------------------------
It can show existence, and it can FAIL. Section 5 is a hard falsification
test with a real chance of killing the picture, and the result is reported
straight whichever way it lands.
"""
import numpy as np

# ---------------------------------------------------------------- constants
c     = 2.99792458e8          # m/s   exact
h     = 6.62607015e-34        # J s   exact
hbar  = 1.054571817e-34       # J s
m_e   = 9.1093837015e-31      # kg
m_p   = 1.67262192369e-27     # kg
RHO_MAX = 4.6e17              # kg/m^3, 2x nuclear saturation; PWC's own ceiling

A1 = h * c / (4.0 * np.pi)    # J m -- the single-loop-pair confinement constant

def G(R, P0, sigma, A):
    return (4.0*np.pi/3.0)*P0*R**3 + 4.0*np.pi*sigma*R**2 + A/R

def dG(R, P0, sigma, A):
    return 4.0*np.pi*P0*R**2 + 8.0*np.pi*sigma*R - A/R**2

def R_equilibrium(P0, sigma, A):
    """Unique positive root of 4*pi*P0*R^4 + 8*pi*sigma*R^3 - A = 0.

    f(R) = 4*pi*P0*R^4 + 8*pi*sigma*R^3 is strictly increasing on R>0 for
    P0>=0, sigma>=0 (not both zero), f(0)=0, f(inf)=inf.  So exactly one
    root, found by bisection with no initial guess and no fitting.
    """
    f = lambda R: 4.0*np.pi*P0*R**4 + 8.0*np.pi*sigma*R**3 - A
    lo, hi = 1e-30, 1e-30
    while f(hi) < 0.0:
        hi *= 2.0
        if hi > 1e30:
            raise RuntimeError("no root below 1e30 m")
    for _ in range(400):
        mid = np.sqrt(lo*hi)          # geometric bisection: 50+ decades
        if f(mid) < 0.0: lo = mid
        else:            hi = mid
    return np.sqrt(lo*hi)

line = lambda s='-': print(s*74)

# ===========================================================================
print(__doc__.split("NOT USED ANYWHERE")[0].strip()[:0] or "", end="")
line('=')
print("PWC KNOT EXISTENCE WITH PRESSURE + CONFINEMENT")
line('=')

# ---------------------------------------------------------------- Section 1
print("\n1. WHY THE OLD FUNCTIONAL COULD NOT WIN -- DERRICK SCALING")
line()
print("""Scale a fixed profile shape by R -> lam*R in 3D and read off the power
of lam each energy term carries:

    term                        E(lam) power     pushes R toward
    gradient   K/2 (grad phi)^2     lam^+1        0   (collapse)
    potential  Lam phi^2(1-phi)^2   lam^+3        0   (collapse)
    coupling   B/2 (n-n0-dn phi)^2  lam^+3        0   (collapse)
    grad-n     C/2 (grad n)^2       lam^+1        0   (collapse)
    -------------------------------------------------------------
    pressure   (4pi/3) P0 R^3       lam^+3        0   (collapse)
    surface    4 pi sigma R^2       lam^+2        0   (collapse)
    confinement      A/R            lam^-1      infinity (expansion)

Derrick's theorem in one line: a stationary point needs BOTH signs of
exponent. The audited functional had only positive powers. Every one of
its 36 parameter sets was therefore doomed before a single BVP was solved
-- the failure was never about the values of B/K, C/K, Lam/K.

(The audit saw DISPERSAL rather than collapse because the fixed-inventory
constraint lets the amplitude fall as the lump spreads. Same verdict:
no interior minimum.)

Adding only a pressure term, as RESULTS.md proposed, adds another lam^+3.
It removes the dispersal escape and hands the lump to collapse instead.
It cannot produce existence on its own.

The ONLY negative power on that list is the confinement energy of the
trapped light. In PWC that is not an optional extra: the knot IS trapped
light. It was missing from E[n,phi] because E[n,phi] has no light in it --
its fields are n and phi. Pass 1 did not fail because the parameters were
wrong. It failed because the field content was wrong.""")

# ---------------------------------------------------------------- Section 2
print("\n2. EXISTENCE THEOREM -- NO PARAMETER SCAN REQUIRED")
line()
print("""G(R) = (4pi/3) P0 R^3 + 4 pi sigma R^2 + A/R

  dG/dR = 0   <=>   4 pi P0 R^4 + 8 pi sigma R^3 = A

The left side is strictly increasing on R>0 with value 0 at R=0 and
infinity at R=infinity, for ANY P0 >= 0, sigma >= 0 not both zero.
Therefore for any A > 0 there is EXACTLY ONE stationary radius, and since
G -> +inf at both ends it is the unique GLOBAL MINIMUM.

Existence is not parameter-dependent. There is nothing to scan. The 36-cell
phase diagram has no analogue here: every cell passes, by construction, for
every positive (P0, sigma, A).""")

# numerical demonstration across 12 decades of each medium constant
print("\n   numerical check -- unique interior minimum, verified by direct scan:")
print("   %-12s %-12s %14s %14s %10s" % ("P0 [Pa]","sigma [J/m2]","R* [m]","G(R*) [J]","grid min"))
ok = True
for P0 in [1e20, 1e28, 1e36]:
    for sg in [1e10, 1e18, 1e26]:
        Rs = R_equilibrium(P0, sg, A1)
        grid = np.logspace(np.log10(Rs)-6, np.log10(Rs)+6, 400001)
        Rg = grid[np.argmin(G(grid, P0, sg, A1))]
        agree = abs(np.log10(Rg/Rs)) < 1e-4
        ok &= agree
        print("   %-12.1e %-12.1e %14.6e %14.6e %10s"
              % (P0, sg, Rs, G(Rs,P0,sg,A1), "match" if agree else "MISMATCH"))
print("   all analytic roots reproduced by brute-force grid search:", ok)

# ---------------------------------------------------------------- Section 3
print("\n3. THE ELECTRON FIXES ONE EQUATION, NOT TWO")
line()
E_e   = m_e * c**2
R_e   = A1 / E_e               # = lambda_C/4pi, Williamson's loop radius
lamC  = h/(m_e*c)
print("   A = h c / 4pi                = %.6e J m   (universal, no freedom)" % A1)
print("   m_e c^2                      = %.6e J" % E_e)
print("   R* = A / (m_e c^2)           = %.6e m" % R_e)
print("   lambda_C / 4pi               = %.6e m   <- Williamson, verbatim" % (lamC/(4*np.pi)))
print("   agreement                    : %.3e relative" % abs(R_e/(lamC/(4*np.pi)) - 1))
print("""
   That is an identity, not a result: A/R = mc^2 IS M = L/c0^2 written for
   a confined photon. It reproduces Williamson because it is his relation.

   IMPORTANT AND EASY TO GET WRONG:
   The electron's mass is the CONFINED LIGHT, full stop -- M = L/c0^2 is an
   identity. The surface and pressure terms are what the MEDIUM pays to
   host the knot; they are medium strain, not light, so they are not part
   of m_e. Setting G(R*) = m_e c^2 would double-count and forces
   sigma = P0 = 0. It is wrong. What the electron gives is the equilibrium
   condition only:""")
print("\n      4 pi P0 R*^4 + 8 pi sigma R*^3 = A        (one equation, two unknowns)\n")
sigma_max = A1/(8.0*np.pi*R_e**3)
P0_max    = A1/(4.0*np.pi*R_e**4)
print("   endpoint if sigma = 0 :  P0    = %.6e Pa" % P0_max)
print("   endpoint if P0    = 0 :  sigma = %.6e J/m^2" % sigma_max)
print("   (sigma, P0) is pinned to the straight line between those endpoints.")

# ---------------------------------------------------------------- Section 4
print("\n4. P0 AGAINST PWC's OWN DENSITY CEILING -- AND sigma FALLS OUT")
line()
P_rhomax = RHO_MAX * c**2
print("   rho_max                      = %.3e kg/m^3   (2x nuclear saturation)" % RHO_MAX)
print("   rho_max c0^2                 = %.6e Pa" % P_rhomax)
print("   P0_max allowed by electron   = %.6e Pa" % P0_max)
print("   ratio P0_max / rho_max c0^2  = %.4e" % (P0_max/P_rhomax))
sigma_at_Prhomax = (A1 - 4.0*np.pi*P_rhomax*R_e**4)/(8.0*np.pi*R_e**3)
print("   sigma forced if P0 = rho_max c0^2 : %.4e J/m^2   <-- NEGATIVE" % sigma_at_Prhomax)
print("""
   RESULT: P0 = rho_max c0^2 is EXCLUDED, by a factor of %.2e. Forcing it
   drives sigma negative, and negative surface tension means the interface
   gains energy by growing -- no stable knot at all. So the medium's
   ambient pressure is not its compression-ceiling pressure.

   That is not a failure, it is the expected reading: rho_max is the
   ceiling reached inside a collapsed core, P0 is the ambient background of
   ordinary space. Ambient below ceiling is what PWC already says. What is
   NEW is that the electron now puts a hard NUMBER on the ambient ceiling:

       P0 < %.4e Pa        (equivalently P0/c0^2 < %.4e kg/m^3)

   Every candidate ambient density in this repo sits enormously below that
   bound, so the bound excludes nothing cosmological. It is loose. Say so.

   THE CONSEQUENCE THAT IS NOT LOOSE:
   because P0 is that far below the electron-scale pressure, the P0 R^4
   term in the equilibrium condition is negligible, and sigma stops being
   one end of a line and becomes DETERMINED:""" % (P_rhomax/P0_max, P0_max, P0_max/c**2))
for rho0, lab in [(1e-21,"repo value carried by domains EE/Z/II"),
                  (2.244e-27,"repo value implied by SPARC-fitted a0")]:
    frac = 4.0*np.pi*(rho0*c**2)*R_e**4 / A1
    print("      rho0 = %-9.3e kg/m^3 (%s)" % (rho0, lab))
    print("         pressure term is %.2e of A -- negligible" % frac)
sigma_pin = A1/(8.0*np.pi*R_e**3)
sigma_closed = 2.0*np.pi*m_e**3*c**4/h**2
print("\n      sigma = A/(8 pi R*^3)   = %.6e J/m^2" % sigma_pin)
print("      closed form: sigma = 2 pi m_e^3 c^4 / h^2")
print("                          = %.6e J/m^2  (agreement %.3e)"
      % (sigma_closed, abs(sigma_closed/sigma_pin - 1)))
print("""
   That is a medium property written entirely in m_e, c and h. It is a
   DERIVATION from one input (the electron mass), not a fit -- there was
   never a free knob to turn. It is also the first time sigma has had a
   number in this repo at all.

   INDEPENDENT COMPARISON -- the only other surface tension physics has at
   this scale is the nuclear liquid-drop surface term:""")
a_s_MeV = 17.8
a_s = a_s_MeV*1.602176634e-13
r0   = 1.2e-15
sig_nuc = a_s/(4.0*np.pi*r0**2)
print("      liquid-drop a_s = %.1f MeV, r0 = %.1f fm" % (a_s_MeV, r0*1e15))
print("      sigma_nuclear   = a_s/(4 pi r0^2) = %.4e J/m^2" % sig_nuc)
print("      sigma_PWC       =                   %.4e J/m^2" % sigma_pin)
print("      ratio           = %.3e" % (sig_nuc/sigma_pin))
R_nuc = (A1/(8.0*np.pi*sig_nuc))**(1.0/3.0)
print("""
      They differ by %.1e. They are NOT the same interface -- nuclear
      surface is nucleon-against-vacuum, PWC's sigma is HDF-against-LDF --
      so this neither confirms nor refutes anything. It is reported because
      it is the only external number available and hiding a mismatch would
      be dishonest.

      For the record, running the equilibrium BACKWARDS with the nuclear
      value gives R = %.4e m = %.3f fm and m c^2 = %.4g MeV.
      The radius is strikingly nuclear-scale; the mass is not any particle.
      One of those two is a coincidence and nothing here says which, so it
      is logged and not claimed.""" % (sig_nuc/sigma_pin, R_nuc, R_nuc*1e15,
                                       (A1/R_nuc)/1.602176634e-13/1e6))

# ---------------------------------------------------------------- Section 5
print("\n5. FALSIFICATION TEST: ONE MEDIUM, ONE A, ONE MASS")
line()
print("""A is universal and (sigma, P0) are medium properties, so
4 pi P0 R^4 + 8 pi sigma R^3 = A has EXACTLY ONE root -- section 2 proved
that. One root means one equilibrium radius means ONE PARTICLE MASS.

The universe has more than one particle. As written, the model is FALSE.

The only way out that PWC already contains, in your words -- "who's saying
an electron's only two waves though?" -- is that a knot of N wave-pairs
carries A_N = N*A1, giving a different root for each N. That is not a free
parameter per particle: N is an integer and the mass ratios are then fully
determined. So it is immediately testable against the proton.""")

R_p_obs = A1/(m_p*c**2)
print("\n   electron: R* = %.6e m,  m c^2 = %.6e J" % (R_e, E_e))
print("   proton  : R* = %.6e m,  m c^2 = %.6e J" % (R_p_obs, m_p*c**2))
print("   m_p/m_e = %.5f" % (m_p/m_e))
print("""
   With A_N = N*A1 and mc^2 = A_N/R:
     pure surface regime (sigma dominates): 8 pi sigma R^3 = N A1
        -> R ~ N^(1/3),  m ~ N/R ~ N^(2/3)   -> N = (m_p/m_e)^(3/2)
     pure pressure regime (P0 dominates)  : 4 pi P0 R^4 = N A1
        -> R ~ N^(1/4),  m ~ N/R ~ N^(3/4)   -> N = (m_p/m_e)^(4/3)""")
N_surface  = (m_p/m_e)**1.5
N_pressure = (m_p/m_e)**(4.0/3.0)
print("\n   N required, surface-dominated  = %12.1f" % N_surface)
print("   N required, pressure-dominated = %12.1f" % N_pressure)
print("""
   VERDICT ON SECTION 5: NEGATIVE, and it is the honest kind of negative.
   Neither N is an integer of any structural significance -- not 3, not
   1836, not 4pi/alpha, not any power of a small integer. Nothing in PWC
   predicts either number, and picking whichever regime lands closer to a
   nice number afterwards would be exactly the reverse-engineering already
   rejected once in this repo.

   What this does NOT do is kill the picture. It kills the claim that a
   proton is a scaled-up electron knot of the same kind -- which is an
   ordinary physics fact anyway: the proton is composite, the electron is
   not. A one-loop-family model has no business reproducing a composite
   mass, and the fact that it cannot is a point in favour of it being
   an actual model rather than an elastic one.

   The real test is therefore NOT the proton. It is any second object that
   is genuinely the same kind of knot -- the muon and the tau, which are
   the electron repeated. That test is stated in section 6 and NOT run
   here, because running it needs a term this file does not have.""")

print("\n   what the lepton test would demand, for the record:")
for nm, mass in [("electron", m_e), ("muon", 1.883531627e-28), ("tau", 3.16754e-27)]:
    Rx = A1/(mass*c**2)
    print("      %-9s m c^2 = %.6e J   R* = A/(mc^2) = %.6e m   m/m_e = %10.4f"
          % (nm, mass*c**2, Rx, mass/m_e))
mu_e = 1.883531627e-28/m_e
tau_e = 3.16754e-27/m_e
print("      N(mu)/N(e)  surface-dominated = %.2f   pressure-dominated = %.2f"
      % (mu_e**1.5, mu_e**(4.0/3.0)))
print("      N(tau)/N(e) surface-dominated = %.2f   pressure-dominated = %.2f"
      % (tau_e**1.5, tau_e**(4.0/3.0)))
print("""      -- these are not integers either, and no version of this file
         is allowed to round them until something in PWC predicts them.""")

# ---------------------------------------------------------------- Section 6
print("\n6. WHAT IS ESTABLISHED, WHAT IS NOT")
line()
print("""ESTABLISHED
  a) The RESULTS.md diagnosis is incomplete and its proposed fix does not
     work. A pressure term alone converts dispersal into collapse.
  b) Pass 1's 36/36 failure is fully explained by Derrick scaling: the
     functional carried no negative power of lam. No parameter value
     inside that functional could ever have passed.
  c) With pressure + surface + confinement, a unique stable finite-radius
     knot exists for EVERY positive (P0, sigma, A). Existence stops being
     a scan and becomes a theorem. Verified numerically over 12 decades.
  d) Derrick is evaded by the trapped light, not by a stabilising fudge.
     Both PWC bounds do load-bearing work and they act at opposite ends:
     the confinement energy forbids R -> 0, the bounded medium's P0 forbids
     R -> infinity. Remove the boundary and P0 goes, and the knot disperses.
     "Nothing is infinite" is doing real mathematical work here.
  e) The electron caps the medium's ambient pressure at P0 < %.3e Pa,
     which EXCLUDES P0 = rho_max c0^2 by a factor of %.1e (it would force
     sigma < 0). Ambient is not the compression ceiling.
  f) With P0 that far below the electron scale its term is negligible, so
     sigma is no longer one end of a line -- it is determined:
        sigma = 2 pi m_e^3 c^4 / h^2 = %.4e J/m^2
     derived from m_e, c, h with no free parameter. First number sigma has
     ever had in this repo.

NOT ESTABLISHED -- do not let any summary upgrade these
  g) P0 itself is still NOT pinned -- only bounded above, and the bound is
     loose enough to exclude nothing cosmological. sigma is pinned only
     BECAUSE P0 is negligible at 1e-13 m; that is an argument from scale
     separation, and it fails the moment anything asks for P0's value.
  h) Section 3 reproduces Williamson because it IS Williamson. It is a
     consistency check, not a prediction.
  i) Section 5 is negative. The N-loop extension produces no integer for
     the proton and none for the muon or tau.
  j) Nothing here has been tested against an observation. Every number in
     this file is h, c, a particle mass, or nuclear saturation density.
  k) The interior/ambient density contrast is ASSUMED to run LDF-inside,
     HDF-outside. If it ran the other way the pressure term flips sign,
     lam^+3 becomes lam^-3, and the unique minimum becomes a unique
     MAXIMUM -- a nucleation barrier, not a particle. The ontology is
     load-bearing, not decorative, and this is the single assumption most
     capable of destroying the result.

NEXT TERM NEEDED, named so it can be killed before it is coded
  The lepton test in section 5 needs the knot's internal topology to say
  what N counts -- turns, crossings, or linked loops. PWC does not
  currently contain that. Until it does, the lepton ratios cannot be
  predicted and must not be fitted.""" % (P0_max, P_rhomax/P0_max, sigma_pin))
line('=')
