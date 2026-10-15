"""Light bending as push + pull (Jaden, 2026-10-02). Newtonian 1/r^2 only; no spacetime metric, no flowing medium, no index-of-refraction law.

PULL: a photon of energy L has mass L/c0^2 (locked rule m = L/c0^2). The 1/r^2 pull gives it a transverse impulse while it passes
      a mass M at impact parameter b along a straight path at c0: d_theta = (1/c0) * Integral g_perp dt = 2GM/(b*c0^2), independent of L.
PUSH: the medium around a mass is in equilibrium (its density fall is its own pull on itself): the pressure-gradient force per unit mass,
      (1/rho)*dP/dr, equals the gravitational pull g. The photon is the same substance as the medium (low-density phase), so it
      feels that push as well, in the same direction. Total inward acceleration 2g -> total bend = 2 * pull = 4GM/(b*c0^2).
Assumption: the photon responds to the pressure gradient with the medium's own density (same substance).
The two terms are the same two terms listed in OPEN_WORK.md ("Light bending factor of 2"); the equal size now follows from equilibrium.
"""
import numpy as np
from scipy.integrate import quad

G, C0, GM_SUN, R_SUN = 6.6743e-11, 299792458.0, 1.32712440018e20, 6.957e8
ARCSEC = 180 / np.pi * 3600


def pull_numeric(GM, b):
    # transverse pull along the straight path x = c0*t is g_perp = GM*b/(b^2+x^2)^1.5; put x = b*u so the integral is dimensionless
    shape, _ = quad(lambda u: 1.0 / (1.0 + u * u) ** 1.5, -np.inf, np.inf)   # = 2
    integral = (GM / b) * shape                                              # Integral g_perp dx
    return integral / C0 ** 2                                                # (1/c0) * Integral g dt = (1/c0^2) * Integral g dx


if __name__ == "__main__":
    pull = pull_numeric(GM_SUN, R_SUN)
    analytic = 2 * GM_SUN / (R_SUN * C0 ** 2)
    print("pull (photon mass L/c0^2, 1/r^2):  numeric %.5f arcsec, analytic 2GM/(b c0^2) %.5f arcsec" % (pull * ARCSEC, analytic * ARCSEC))
    push = pull                                                 # equilibrium: pressure-gradient push per unit mass = g
    total = pull + push
    print("push (hydrostatic balance, = pull): %.5f arcsec" % (push * ARCSEC))
    print("total at the solar limb:            %.4f arcsec  (4GM/(b c0^2) = %.4f)" % (total * ARCSEC, 4 * GM_SUN / (R_SUN * C0 ** 2) * ARCSEC))
    print("\nEnergy independence: L cancels, so every photon energy bends the same (observed: achromatic lensing).")
    # Test against the measured deflection, written as the ratio gamma = (measured / 1.7512 arcsec) * 2 - 1.
    # Literature value (Cassini radio link, Bertotti et al. 2003; NOT re-checked this session): gamma - 1 = (2.1 +- 2.3)e-5.
    gm1, err = 2.1e-5, 2.3e-5
    print("Model gives gamma = 1 exactly (push = pull). Cassini: gamma - 1 = %.1e +- %.1e -> model is %.1f sigma away." % (gm1, err, gm1 / err))
    print("\nWhat this does NOT show: that the photon feels the pressure gradient with the medium's own density (assumed); Sgr A*/M87* shadow sizes (undefined in PWC).")
