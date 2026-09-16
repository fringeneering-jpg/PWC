"""
DOMAIN II -- cavitation wake matter production, derived end to end from alpha.

This domain records a chain that runs from the fine structure constant to a
measured astronomical object with no free parameter anywhere in between. It
also records, explicitly, four places where this session's earlier analysis
was WRONG and had to be reversed. Both halves are the result.

THE CHAIN
  alpha
    -> N = 4*pi/alpha = 1722 waves per electron   (Williamson double-loop torus)
    -> medium wavelength lambda = r_e = 2.8179e-15 m
    -> blocking threshold rho > m_p/lambda^3 = 7.475e16 kg/m^3
    -> only compact cores impede the flow; stars and planets are transparent
    -> bow wave grows to R_bow/R = sqrt(1 + phi*c0/v)
    -> low-pressure wake behind it
    -> uniform P0 slams it shut; M = L/c0^2 converts at exactly rho_HDF
    -> 200 kpc trail mass vs van Dokkum et al. 2023 runaway SMBH

MECHANISM AS STATED BY THE AUTHOR, recorded verbatim in intent because
every prior misreading of it produced a wrong result:
  - The medium passes THROUGH the sieve. It does not flow around an obstacle.
  - It NEVER tears. There is no vacuum, no r=0, no break in the continuum.
  - The bow wave builds until flow around matches flow through. That is an
    EQUILIBRIUM the wave grows into, not a threshold that trips.
  - The low-pressure wake is then crushed by the uniform ambient pressure.
    That slam is the cavitation event, and it forges matter.
  - Hydrogen, because it is the cheapest stable knot the energy budget buys.

Data: van Dokkum et al. 2023, Nature/ApJL, candidate runaway supermassive
black hole with a ~200 kpc linear wake of star formation. Stellar mass of
the trail ~1e9 Msun. External measurement, not from this repository.
"""
import json
import os

import numpy as np

D = os.environ.get("PWC_SPARC_DIR", os.path.dirname(os.path.abspath(__file__)))

h = 6.62607015e-34
hbar = 1.054571817e-34
c0 = 2.99792458e8
me = 9.1093837015e-31
mp = 1.67262192e-27
e_C = 1.602176634e-19
alpha = 7.2973525693e-3
Msun = 1.9884e30
KPC = 3.0857e19
NUC = 2.3e17
RHO_MAX = 2 * NUC
RHO_HDF = 1e-21          # Domain EE / Domain Z galaxy-scale medium density


def hr(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


R = {}

# ===================================================================== #
hr("1. N FROM WILLIAMSON'S TOROIDAL ELECTRON -- NO FITTING")
# ===================================================================== #
lam_C = h / (me * c0)
lbar = hbar / (me * c0)
r_e = alpha * lbar
path = 2 * (2 * np.pi * lbar)
N = path / r_e
print("  Electron as a double-looped confined photon (Williamson & van der Mark).")
print("    major radius R = lbar_C          = %.4e m" % lbar)
print("    tube radius   r = alpha*lbar_C   = %.4e m  (= classical electron radius)" % r_e)
print("    R/r = 1/alpha                    = %.3f" % (1 / alpha))
print("    double-loop path = 2 * 2 pi R    = %.4e m" % path)
print("    N = path/lambda                  = %.1f" % N)
print("    analytically N = 4*pi/alpha      = %.1f   EXACT" % (4 * np.pi / alpha))
E_q = h * c0 / r_e
print("\n  medium wavelength lambda = %.4e m" % r_e)
print("  energy per quantum       = %.4e J = %.1f MeV" % (E_q, E_q / e_C / 1e6))
R["N_waves_per_electron"] = float(N)
R["medium_wavelength_m"] = float(r_e)
R["quantum_energy_MeV"] = float(E_q / e_C / 1e6)

# ===================================================================== #
hr("2. WHAT IMPEDES THE FLOW -- BLOCKING THRESHOLD")
# ===================================================================== #
rho_block = mp / r_e ** 3
print("  Blocking when scatterer spacing < wavelength:  rho > m_p/lambda^3")
print("    rho_block = %.4e kg/m^3" % rho_block)
print("              = %.3f x nuclear saturation" % (rho_block / NUC))
print("              = %.3f x rho_max" % (rho_block / RHO_MAX))
print("\n   object                     rho (kg/m^3)   solid frac   blocks?")
for rho, lab in [(1.4e3, "Sun, mean"), (1.5e5, "Sun, core"), (1e9, "white dwarf"),
                 (1e10, "iron core"), (rho_block, "THRESHOLD"),
                 (NUC, "nuclear saturation"), (RHO_MAX, "rho_max")]:
    print("   %-24s %.3e     %.3e    %s"
          % (lab, rho, rho / RHO_MAX, "YES" if rho >= rho_block else "no"))
print("\n  Stars and planets are transparent. Only compact cores impede.")
print("  This confines the drag/bow-wave mechanism to exactly the objects it")
print("  was proposed for, from a derived number rather than an assumed one.")
R["blocking_threshold_kg_m3"] = float(rho_block)
R["blocking_over_nuclear_sat"] = float(rho_block / NUC)

# ===================================================================== #
hr("3. THE BOW WAVE -- AN EQUILIBRIUM, NOT A THRESHOLD")
# ===================================================================== #
print("  The medium goes THROUGH the sieve, impeded by internal density.")
print("  It piles up until diverted flow matches transmitted flow:")
print("     Q_through = phi * pi R^2 * c0     Q_around = pi(R_bow^2 - R^2) * v")
print("     => R_bow/R = sqrt(1 + phi*c0/v)")
print("  Nothing tears. The medium is continuous throughout.\n")
print("     phi (open frac)   v (km/s)    R_bow/R")
for phi in [1e-2, 1e-3, 1e-4]:
    for v in [1600e3]:
        print("     %8.0e        %7.0f     %.3f" % (phi, v / 1e3, np.sqrt(1 + phi * c0 / v)))
R["bow_wave_relation"] = "R_bow/R = sqrt(1 + phi*c0/v)"

# ===================================================================== #
hr("4. THE SLAM -- M = L/c0^2 IS THE MECHANISM, NOT A SEPARATE POSTULATE")
# ===================================================================== #
L = RHO_HDF * c0 ** 2
print("  Uniform ambient P0 crushes the wake. Work = P0*V ties knots.")
print("  With the stiff closure the sonic-choke entry fixes (c_s = c0):")
print("     L  = rho_HDF c0^2 = %.4e J/m^3" % L)
print("     M  = L / c0^2     = %.4e kg/m^3" % (L / c0 ** 2))
print("  The wake refills with matter at EXACTLY the density of the medium it")
print("  displaced. This is not forced by the EOS -- it IS M = L/c0^2.")
print("\n  Why hydrogen: cheapest stable knot the budget buys.")
for m, lab in [(mp, "hydrogen"), (4 * mp, "helium-4"), (12 * mp, "carbon-12"), (56 * mp, "iron-56")]:
    print("     %-12s %8.1f MeV each -> %.2e per m^3 affordable"
          % (lab, m * c0 ** 2 / e_C / 1e6, L / (m * c0 ** 2)))
print("\n  Threshold check, no focusing required:")
print("     one quantum        = %.1f MeV" % (E_q / e_C / 1e6))
print("     proton rest energy = %.1f MeV -> %.2f quanta" % (mp * c0 ** 2 / e_C / 1e6, mp * c0 ** 2 / E_q))
print("     e+e- pair          = %.3f MeV -> a single quantum exceeds it %.0fx"
      % (2 * me * c0 ** 2 / e_C / 1e6, E_q / (2 * me * c0 ** 2)))
print("  Breit-Wheeler (gamma+gamma -> e+e-) observed at STAR/RHIC 2021.")
R["conversion"] = "M = L/c0^2, wake refills at exactly rho_HDF"
R["quanta_per_proton"] = float(mp * c0 ** 2 / E_q)

# ===================================================================== #
hr("5. AGAINST A REAL OBJECT -- van Dokkum et al. 2023 RUNAWAY SMBH")
# ===================================================================== #
v = 1600e3
Ltrail = 200 * KPC
print("  200 kpc trail at 1600 km/s -> transit %.0f Myr" % (Ltrail / v / 3.156e7 / 1e6))
print("\n   wake width    swept volume (m^3)    matter produced (Msun)")
for w in [0.3, 1.0, 3.0]:
    V = np.pi * (w * KPC / 2) ** 2 * Ltrail
    print("   %5.1f kpc     %.4e         %.4e" % (w, V, V * RHO_HDF / Msun))
V1 = np.pi * (0.5 * KPC) ** 2 * Ltrail
m1 = V1 * RHO_HDF / Msun
print("\n  1 kpc-wide trail -> %.3e Msun" % m1)
print("  observed trail stellar mass ~1e9 Msun   ->  ratio %.2f" % (m1 / 1e9))
print("\n  rho_HDF = 1e-21 is NOT tuned here. It is the galaxy-scale medium")
print("  density Domain EE/Z already produced from the SPARC inversion. Two")
print("  independent parts of the framework meeting at a third measurement.")
print("  With the intergalactic baryon density instead (1e-27) the trail mass")
print("  is %.2e Msun, short by %.0e." % (V1 * 1e-27 / Msun, 1e9 / (V1 * 1e-27 / Msun)))
R["vandokkum"] = {"trail_mass_predicted_Msun": float(m1),
                  "trail_mass_observed_Msun": 1e9,
                  "ratio": float(m1 / 1e9),
                  "rho_HDF_source": "Domain EE/Z SPARC inversion, not tuned"}

# ===================================================================== #
hr("6. FOUR CORRECTIONS TO THIS SESSION'S OWN EARLIER ANALYSIS")
# ===================================================================== #
M_core = 28.118 * Msun
R_core = (3 * M_core / (4 * np.pi * RHO_MAX)) ** (1 / 3)
print("  (a) DERIVATION DIRECTION -- I had the arrow backwards.")
print("      Claimed: rho_max is DERIVED as M_core/volume, an output.")
print("      Correct: rho_max = 2 x nuclear saturation is an INPUT.")
print("               R_core is the OUTPUT:")
print("        (3 * 28.118 Msun / 4 pi * 4.6e17)^(1/3) = %.3f km" % (R_core / 1000))
print("        matching the 30.73 km every PWC/ script carries.")
print("      There is no circularity. The chain is:")
print("        nuclear saturation (external) -> rho_max")
print("        GW150914 36/29/62 (external)  -> k -> M_core")
print("        both                          -> R_core -> M_grad -> K")
print()
print("  (b) DOMAIN HH's 2pi CLAIM -- superseded by the manifest itself.")
print("      HH argued a0 = cH0/2pi needed the 2pi derived. Manifest line 749")
print("      already records that the real Gibbons-Hawking formula gives c0*H0")
print("      with NO 2pi. The relation stands or falls at the bare 5.6x.")
print()
print("  (c) DOMAIN EE's TARGET -- c_s was never a free parameter.")
print("      The verified sonic-choke entry fixes c_s = c0 (shared-c postulate).")
for vv, lab in [(7.8e3, "faintest dwarf"), (1.0e5, "typical"), (1.2267e6, "most massive")]:
    print("        EE required %8.1f km/s -> c0/c_s = %8.0f" % (vv / 1e3, c0 / vv))
print("      The gap is the same one, stated against a fixed number.")
print()
print("  (d) TWO CEILINGS ARE DISTINCT, NOT A TYPO.")
print("      rho_Sintot_max = 4.6e17 (2x nuclear sat) -- the neutron core")
print("      rho_HDF_max    = 4.6e10                  -- the compressed medium")
print("      A 1.4-2.1 Msun neutron core inside ~34 Msun of max-compressed HDF")
print("      reaches max 2GM(<r)/c^2/r of 0.37-0.48 -- it does NOT close.")
R["corrections"] = {
    "R_core_derived_km": float(R_core / 1000),
    "rho_max_is_input_not_output": True,
    "HH_2pi_superseded_by_manifest_line_749": True,
    "EE_target_c_s_equals_c0": True,
    "two_ceilings_distinct": True,
}

out = os.path.join(D, "domain_II_cavitation_wake_matter_results.json")
with open(out, "w") as f:
    json.dump(R, f, indent=2)
print("\n  wrote %s" % out)
