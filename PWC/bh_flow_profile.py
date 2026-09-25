"""Held medium as steady transonic inflow of the resting medium (prediction frozen in predictions/bh_flow_profile.md).
Isothermal Bondi flow, c_s = c0/sqrt(3), outer density rho0; Newtonian (order of magnitude; relativistic Michel/Babichev
accretion of a P = w*eps fluid changes the near-horizon density by O(1-10), not orders of magnitude)."""
import numpy as np
from scipy.optimize import brentq
G = 6.6743e-11; c = 299792458.0; Ms = 1.98892e30; RN = 2.3e17; RM = 1.304e15; RHO0 = 8.1e-27; k = 0.868899
cs = c / np.sqrt(3)
def bondi(M):                      # isothermal Bondi: Mach number x(r) on the accreting branch, lambda = e^{3/2}/4
    rsn = G * M / (2 * cs ** 2)
    def rho(r):                    # s = r/r_sonic, x = v/cs: x^2/2 - ln x = 2 ln s + 2/s - 3/2 ; rho/rho0 = e^{3/2}/(x s^2)
        s = r / rsn; R = 2 * np.log(s) + 2 / s - 1.5
        if abs(s - 1) < 1e-9: x = 1.0
        else:
            f = lambda x: 0.5 * x * x - np.log(x) - R
            x = brentq(f, 1.0, 2 * np.sqrt(2 * R) + 10, maxiter=500) if s < 1 else brentq(f, 1e-300, 1.0, maxiter=500)
        return RHO0 * np.exp(1.5) / (x * s * s)
    return rsn, rho
rows = []
for C in [10, 50, 1e3, 4.3e6]:
    Cm = C * Ms; Mf = C + k * C ** (2 / 3); M = Mf * Ms
    Rc = (3 * Cm / (4 * np.pi * RN)) ** (1 / 3); rch = 2 * G * M / c ** 2
    rsn, rho = bondi(M)
    r = np.geomspace(Rc, max(rch, 10 * rsn), 4000); d = np.array([rho(x) for x in r])
    Mmed = np.trapezoid(4 * np.pi * r ** 2 * d, r)
    rows.append((C, Rc / 1e3, rch / 1e3, rsn / 1e3, d[0], d.max(), Mmed / Ms, k * C ** (2 / 3)))
    print(f"C={C:>9.0f}  R_c={Rc/1e3:7.1f} km  choke={rch/1e3:9.1f} km  sonic pt={rsn/1e3:9.1f} km  rho at core {d[0]:.2e} (rho_max {RM:.1e})  held medium {Mmed/Ms:.2e} Msun  vs k-rule {k*C**(2/3):.1f}")
C = np.array([x[0] for x in rows]); m = np.array([x[6] for x in rows])
print(f"held-medium scaling from flow: C^{np.polyfit(np.log10(C), np.log10(m), 1)[0]:.2f}  (target 0.67)")
print(f"accretion rate onto GW150914-size BH: {4*np.pi*(G*62*Ms)**2*RHO0/cs**3*np.exp(1.5)/4:.2e} kg/s")
