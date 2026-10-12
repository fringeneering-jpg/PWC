"""
DOMAIN HH -- cavitation boundary: impedance mismatch EOS, and the a0 ~ c*H0 claim.

This domain does two things:
  (1) writes the boundary equation of state for a phase void held open by
      radiation pressure against an impedance mismatch, with no kinetic
      rotation and no mechanical shear anywhere -- as requested;
  (2) tests the one falsifiable claim in the framing, a0 = c*H0.

PROVENANCE OF THE a0 ~ c*H0 RELATION -- stated up front so it is not
mis-attributed. This coincidence is not a PWC result. Milgrom noted it in
his original 1983 papers, and it has been discussed continuously since
(it is why MOND is often said to "smell cosmological"). Writing it into a
phase-wave framework is a reinterpretation of a known numerical
coincidence, not a new derivation. That does not make it worthless -- it
is the first proposal in this project to fix a0 from OUTSIDE the galaxy
rather than fitting it per-sample -- but the credit belongs where it
belongs.

THE MATHEMATICS BEING IMPLEMENTED.

1. Impedance of the EM sea.  Z = sqrt(mu/eps). With mu = mu_0 and
   n = c0/c_local = sqrt(eps_m/eps_0), the void-to-sea impedance ratio is
       Z_m / Z_0 = 1/n
   so the amplitude reflection coefficient at the phase boundary is
       Gamma = (Z_m - Z_0)/(Z_m + Z_0) = (1 - n)/(1 + n)
   and the reflected power fraction is Gamma^2.

2. Radiation pressure from an isotropic sea. An isotropic EM field of
   energy density u exerts P = u/3. A boundary that reflects a fraction
   Gamma^2 transfers extra momentum, so the net inward traction is
       Delta_P = [(u_sea - u_void)/3] * (1 + Gamma^2)

3. Boundary equation of state (Young-Laplace). For a quasi-static void of
   radius R with boundary tension sigma:
       Delta_P = 2*sigma/R
   Combining:
       2*sigma/R = [(u_sea - u_void)/3] * (1 + Gamma^2)          [EOS]
   This is the requested boundary EOS. It contains no velocity, no
   vorticity, no viscosity and no shear -- purely a normal-traction
   balance, which is what the framing asked for.

4. Cavitation threshold as an acceleration. The boundary layer accelerates
   material at
       a_boundary ~ (1/rho) dP/dr ~ (2*sigma)/(rho * R^2)
   Setting a_boundary = a0 fixes sigma given rho and R. That is the link
   between the boundary EOS and the acceleration scale.

WHAT THIS DOMAIN DOES NOT CLAIM. Writing a consistent EOS is not evidence
that it is realised. Section D records two structural problems that the
numerics below cannot fix and that the framing does not address.
"""
import os
import json

import numpy as np

D = os.environ.get("PWC_SPARC_DIR", os.path.dirname(os.path.abspath(__file__)))
C0 = 2.99792458e8
KPC = 3.0856775814913673e19
MPC = 3.0856775814913673e22
G_SI = 6.67430e-11

# Fitted a0 values from this repository's own runs.
A0_RAR = 1.1603288113586142e-10      # domain_K_results.json / Domain CC
A0_CHOKE = 5.5536e-11                # Domain CC HDF stiffness-deficit law
A0_LIT = 1.2e-10                     # MOND literature value

H0_PLANCK = 67.4       # km/s/Mpc, Planck 2018
H0_SHOES = 73.0        # km/s/Mpc, SH0ES


def hr(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


results = {}

# ===================================================================== #
hr("A -- IS a0 = c*H0? THE ACTUAL NUMBERS")
# ===================================================================== #
print("   H0 source        H0(SI)        c*H0 (m/s^2)   a0_RAR/cH0   cH0/a0_RAR")
rows = {}
for lab, h in (("Planck 2018", H0_PLANCK), ("SH0ES", H0_SHOES)):
    H_si = h * 1000.0 / MPC
    cH = C0 * H_si
    rows[lab] = dict(H0_kms_Mpc=h, H0_si=H_si, cH0=cH,
                     ratio=A0_RAR / cH, inv=cH / A0_RAR)
    print("   %-14s  %.4e   %.4e     %.4f       %.2f"
          % (lab, H_si, cH, A0_RAR / cH, cH / A0_RAR))

cH_p = rows["Planck 2018"]["cH0"]
print("\n  So the bare claim a0 = c*H0 is WRONG by a factor of %.1f." % (cH_p / A0_RAR))
print("  The relation that actually works is a0 = c*H0 / 2*pi:")
for lab in rows:
    pred = rows[lab]["cH0"] / (2.0 * np.pi)
    err = 100.0 * (pred - A0_RAR) / A0_RAR
    print("    %-14s  cH0/2pi = %.4e   vs fitted a0 = %.4e   (%+.1f%%)"
          % (lab, pred, A0_RAR, err))
    rows[lab]["cH0_over_2pi"] = pred
    rows[lab]["pct_err_vs_a0_RAR"] = err

print("\n  Other common forms, for completeness:")
for nm, div in (("cH0/(2pi)", 2 * np.pi), ("cH0/6", 6.0), ("cH0/(2pi) w/ SH0ES", None)):
    if div is None:
        continue
    print("    a0 = %-12s = %.4e   ratio to fitted a0: %.3f"
          % (nm, cH_p / div, (cH_p / div) / A0_RAR))
print("\n  VERDICT: the ORDER OF MAGNITUDE is right and that is genuinely")
print("  striking. The specific claim 'a0 = c*H0' is not -- it overshoots by")
print("  %.1fx. A framework that predicts cH0 exactly is falsified at %.0f%%;" % (cH_p / A0_RAR, 100 * (cH_p / A0_RAR - 1)))
print("  one that predicts cH0/2pi matches to %+.1f%%, but the 2pi must be" % rows["Planck 2018"]["pct_err_vs_a0_RAR"])
print("  DERIVED, not chosen after seeing the answer. Nothing in this")
print("  framing derives it.")
results["A_a0_vs_cH0"] = rows
results["A_verdict"] = "order of magnitude correct; bare a0=cH0 wrong by %.1fx" % (cH_p / A0_RAR)

# ===================================================================== #
hr("B -- THE BOUNDARY EOS, EVALUATED")
# ===================================================================== #
# Sea energy density: identify with the cosmological critical density.
for lab in rows:
    H_si = rows[lab]["H0_si"]
    rho_crit = 3.0 * H_si ** 2 / (8.0 * np.pi * G_SI)
    u_sea = rho_crit * C0 ** 2
    rows[lab]["rho_crit"] = rho_crit
    rows[lab]["u_sea"] = u_sea
    print("  %-14s rho_crit = %.4e kg/m^3   u_sea = rho c^2 = %.4e J/m^3"
          % (lab, rho_crit, u_sea))

rho_crit = rows["Planck 2018"]["rho_crit"]
u_sea = rows["Planck 2018"]["u_sea"]

# Impedance mismatch implied by Domain CC's measured index contrast.
N_MINUS_1_CC = 1.95e-07          # Domain CC median required (n-1)
n = 1.0 + N_MINUS_1_CC
Gamma = (1.0 - n) / (1.0 + n)
print("\n  Using Domain CC's own measured index contrast (n-1 = %.2e):" % N_MINUS_1_CC)
print("    Gamma = (1-n)/(1+n) = %.4e" % Gamma)
print("    reflected power fraction Gamma^2 = %.4e" % Gamma ** 2)
print("    => (1 + Gamma^2) = %.12f" % (1 + Gamma ** 2))
print("\n  The impedance mismatch is %.0e. The reflection term is" % abs(Gamma))
print("  %.0e below unity, so it contributes NOTHING to the traction" % Gamma ** 2)
print("  balance at any level this data can register. The boundary EOS")
print("  degenerates to plain Delta_P = (u_sea - u_void)/3.")

# Required boundary tension to put a0 at a galaxy edge.
R_GAL = 20.0 * KPC
sigma_req = A0_RAR * rho_crit * R_GAL ** 2 / 2.0
dP_req = 2.0 * sigma_req / R_GAL
print("\n  Boundary tension needed to set a = a0 at R = 20 kpc:")
print("    sigma = a0 * rho * R^2 / 2 = %.4e N/m" % sigma_req)
print("    => Delta_P = 2 sigma/R = %.4e Pa" % dP_req)
print("    compare u_sea/3 = %.4e Pa   ratio = %.3e"
      % (u_sea / 3.0, dP_req / (u_sea / 3.0)))
print("\n  FINE-TUNING PROBLEM: the required traction is %.0e times the"
      % (dP_req / (u_sea / 3.0)))
print("  pressure the sea actually has. So (u_sea - u_void) must cancel to")
print("  roughly 1 part in %.0e for the balance to land at a0. Nothing in"
      % ((u_sea / 3.0) / dP_req))
print("  the framing supplies that cancellation; it has to be assumed.")
results["B_boundary_eos"] = {
    "n_minus_1": N_MINUS_1_CC, "Gamma": float(Gamma), "Gamma_squared": float(Gamma ** 2),
    "rho_crit": float(rho_crit), "u_sea": float(u_sea),
    "sigma_required_N_per_m": float(sigma_req), "delta_P_Pa": float(dP_req),
    "delta_P_over_u_sea_third": float(dP_req / (u_sea / 3.0)),
    "impedance_term_negligible": True,
}

# ===================================================================== #
hr("C -- THE SHARPEST FALSIFIABLE PREDICTION: a0 MUST EVOLVE")
# ===================================================================== #
print("  If a0 is set by cosmic tension, a0 = c*H(z)/2pi is NOT a constant.")
print("  H(z) = H0*sqrt(Om*(1+z)^3 + OL), so a0 grows with redshift:")
Om, OL = 0.315, 0.685
H0_si = rows["Planck 2018"]["H0_si"]
print("\n     z       H(z)/H0    a0(z)/a0(0)")
eva = {}
for z in [0.0, 0.5, 1.0, 2.0, 3.0]:
    f = np.sqrt(Om * (1 + z) ** 3 + OL)
    print("    %.1f      %6.3f       %6.3f" % (z, f, f))
    eva["z=%.1f" % z] = float(f)
print("\n  This is a REAL, testable prediction and it is the best thing in")
print("  the proposal. High-z rotation curves (e.g. Genzel+ 2017, Nature 543,")
print("  397) already probe z~1-2 kinematics. A framework committed to")
print("  a0 ~ c*H(z) predicts a0 roughly %.1fx larger at z=2." % eva["z=2.0"])
print("  That is a genuine falsification target that no fit to SPARC can")
print("  reach, and it is worth pursuing. Note it cuts both ways: if a0 is")
print("  measured constant with z, the cosmic-tension origin is dead.")
results["C_a0_evolution"] = eva

# ===================================================================== #
hr("D -- TWO STRUCTURAL PROBLEMS THE NUMERICS CANNOT FIX")
# ===================================================================== #
print("  PROBLEM 1 -- SIGN. The framing says a galaxy IS a void: LOWER")
print("  energy density than the background sea. Domain CC measured the")
print("  required index profile from the same data and found n INCREASING")
print("  inward (n-1 = %.2e at centre, -> 1 at large r). Since n^2 =" % N_MINUS_1_CC)
print("  rho/rho_0 at fixed stiffness, that is HIGHER density toward the")
print("  galaxy -- compression, not cavitation. The cavitation picture and")
print("  the refraction picture in this same repository require OPPOSITE")
print("  density gradients. Both cannot be right.")
print("    Possible escape: the void is in one component (LDF/EM sea) while")
print("    the other (HDF) compresses. But then the framework must say")
print("    WHICH ONE refracts light and which one carries the mass, and")
print("    the manifest does not.")
print("\n  PROBLEM 2 -- STATIC SUPPORT IS ALREADY TESTED. Removing rotation")
print("  (correctly, after FF) leaves a normal-traction balance. That is")
print("  exactly the static case Domain EE tested: pressure support with no")
print("  bulk flow. EE's gauge-free result stands unchanged --")
print("  c_s = -g*r/(dln rho/dln r) gave 0.663 dex scatter in K and c_s")
print("  correlated with each galaxy's own V_flat at +0.921. A 'stabilized")
print("  phase boundary' supported by normal traction is subject to that")
print("  same test, and a0 = cH0/2pi does not change the answer: a global")
print("  constant cannot supply per-galaxy variation that scales with")
print("  V_flat. Domain GG then showed the scatter is not a binning")
print("  artifact (0.570 dex in the near-spherical regime).")
print("\n  So the cavitation reframing inherits EE's failure rather than")
print("  escaping it -- UNLESS the boundary is genuinely a discontinuity")
print("  (a phase transition at a specific radius) rather than a smooth")
print("  profile. That WOULD be a different model, and it makes a sharp")
print("  prediction: a detectable kink in rotation curves at the boundary.")
print("  SPARC can test that. It is the natural next domain.")
results["D_structural"] = {
    "sign_contradiction_with_domain_CC": True,
    "CC_required_n_increases_inward": True,
    "static_support_already_tested_by_EE": True,
    "EE_K_scatter_dex": 0.663, "GG_near_spherical_scatter_dex": 0.570,
    "suggested_next_test": "discontinuity/kink in rotation curves at a boundary radius",
}

hr("SUMMARY")
print("  a0 = c*H0            : wrong by %.1fx" % (cH_p / A0_RAR))
print("  a0 = c*H0/(2pi)      : matches fitted a0 to %+.1f%% -- but 2pi undrived"
      % rows["Planck 2018"]["pct_err_vs_a0_RAR"])
print("  attribution          : Milgrom 1983, not a PWC result")
print("  boundary EOS         : writable and self-consistent (Section B),")
print("                         but the impedance term is %.0e and does" % Gamma ** 2)
print("                         no work")
print("  best idea in it      : a0 must evolve as H(z) -- genuinely")
print("                         falsifiable, testable at z~1-2, worth doing")
print("  unresolved           : sign contradiction with Domain CC; static")
print("                         support already failed in EE/GG")

out = os.path.join(D, "domain_HH_cavitation_boundary_results.json")
with open(out, "w") as f:
    json.dump(results, f, indent=2)
print("\n  wrote %s" % out)
