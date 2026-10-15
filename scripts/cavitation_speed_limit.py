"""Speed limit of a body in a medium: v_cav = sqrt(2*Y/rho) (DERIVATION_BRIEF T3), tested on liquids and anchored on RBH-1.
Jaden, 2026-10-02. The medium does not move; matter is a sieve; a sieve swung through a cloud fast enough chokes and drags.
Light at c0 and the Max-P bow wave at 954 km/s are the same mechanism at two densities (loose medium, medium crushed to rho_max).

1. Water and other liquids (known cavitation limits, Bernoulli): v = sqrt(2*(p0 - p_vap)/rho) at 20 C, 1 atm.
   Property values are hard-coded from CoolProp 8.0.0 (saturated liquid at 293.15 K) so this script needs only numpy.
2. PWC anchor: RBH-1 bow wave 954 km/s at rho_max = 1.304e15 -> Y = 0.5*rho*v^2. ONE point: it fixes Y, so it is not a test.
3. Tests that can fail: fastest pulsars (carrying a Max-P layer would put the wake threshold at 954 km/s); other runaway SMBHs above 954 km/s
   must show a wake (3C 186, CID-42: NOT yet checked for wakes).
Honest limits: for the liquids the 'cohesion' used is just the ambient pressure (real liquids hold more tension); the match to PWC is order of
magnitude only. n_H, masses etc. are not used here.
"""
import numpy as np

C0 = 299792458.0
P0 = 101325.0
# name: (density kg/m3, vapour pressure Pa, sound speed m/s) at 20 C, from CoolProp 8.0.0
LIQUIDS = {"water": (998.2, 2339.0, 1482.0), "ethanol": (789.4, 5876.0, 1159.0), "methanol": (791.0, 13032.0, 1116.0),
           "acetone": (790.3, 24662.0, 1187.0), "benzene": (878.8, 10030.0, 1326.0), "toluene": (866.9, 2919.0, 1324.0),
           "n-heptane": (683.8, 4722.0, 1149.0)}
RHO_MAX, V_RBH1 = 1.304e15, 954e3                          # RBH-1 bow-wave speed (arXiv 2512.04166)
PULSAR = (1083.0, 103.0, 90.0)                              # PSR B1508+55 transverse speed km/s (+ / -) (VLBA parallax)

if __name__ == "__main__":
    print("%-10s %9s %11s %10s %9s %9s" % ("liquid", "rho", "p_vap Pa", "v_cav m/s", "sound", "v/c_s %"))
    for n, (rho, pv, cs) in LIQUIDS.items():
        v = np.sqrt(2 * (P0 - pv) / rho)
        print("%-10s %9.1f %11.0f %10.2f %9.0f %9.2f" % (n, rho, pv, v, cs, v / cs * 100))
    Y = 0.5 * RHO_MAX * V_RBH1 ** 2
    print("\nPWC Max-P medium: rho %.3e, v_cav %.0f km/s = %.2f%% of c0 ; Y = 0.5*rho*v^2 = %.3e Pa (one anchor, not a test)" % (RHO_MAX, V_RBH1 / 1e3, V_RBH1 / C0 * 100, Y))
    print("Same Y at other densities, limit sqrt(2Y/rho) (capped at c0):")
    for lab, rho in (("white dwarf 1e9", 1e9), ("1e11", 1e11), ("1e13", 1e13), ("rho_max", RHO_MAX), ("neutron core 2.3e17", 2.3e17)):
        v = np.sqrt(2 * Y / rho)
        print("   %-20s %s" % (lab, "c0 (formula %.2g c0)" % (v / C0) if v > C0 else "%.4g km/s (%.4f c0)" % (v / 1e3, v / C0)))
    print("   crossover with c0 at rho = 2Y/c0^2 = %.3e kg/m3" % (2 * Y / C0 ** 2))
    v, up, dn = PULSAR
    print("\nTest (not failed, not passed): fastest pulsar B1508+55 %.0f +%.0f/-%.0f km/s vs 954 -> %+.1f sigma (upper error)" % (v, up, dn, (v - 954) / up))
    print("Test (open): runaway SMBH candidates above 954 km/s must show a wake: 3C 186 (-1,310 km/s line of sight), CID-42 (~1,300 km/s): wake search NOT checked.")
    print("Falsification seen: sqrt(latent heat) = water's sound speed to 3-6% (c0^2 = specific latent heat applied to water) but liquid N2 / He are 34-48% low (CoolProp, not in this script).")
