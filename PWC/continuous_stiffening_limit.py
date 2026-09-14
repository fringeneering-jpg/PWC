# =====================================================================
# CONTINUOUS PROFILE WITH A REAL INCOMPRESSIBILITY LIMIT
# EOS: P_excess(rho) = K * rho_max * u / (rho_max - rho),  u = rho - rho_inf
# This diverges ONLY as rho -> rho_max (stiffness -> infinity at the ceiling,
# so the medium resists further compression instead of the density just
# tapering off). It is smooth and finite everywhere down to rho = rho_inf --
# no separate regularization trick needed, no wall, no discontinuity.
#
# Physical picture being tested: once you hit the compression ceiling, the
# object doesn't get denser -- it grows in radius to carry more mass, same
# way real degenerate/incompressible matter behaves.
# =====================================================================
import numpy as np
from scipy.integrate import solve_ivp

G = 6.6743e-11
Msun = 1.9884e30
km = 1000.0

rho_inf = 1e-15
rho_max = 4.6e17

K = 1.0e7   # UNCALIBRATED -- illustrative stiffness scale, flagged explicitly below

r0 = 1.0

def make_derivs(K):
    def derivs(t, y):
        rho, M_excess = y
        rho = min(max(rho, rho_inf), rho_max * (1 - 1e-14))  # stay strictly below ceiling
        u = rho - rho_inf
        dPdrho = K * rho_max * (rho_max - rho_inf) / (rho_max - rho)**2
        dPdr = - (G * M_excess * u) / (t**2) if M_excess > 0 else 0.0
        drhodr = dPdr / dPdrho
        dM_excess_dr = 4 * np.pi * (t**2) * u
        return [drhodr, dM_excess_dr]
    return derivs

def make_event():
    def reach_ambient(t, y):
        return y[0] - rho_inf * 1.0001
    reach_ambient.terminal = True
    reach_ambient.direction = -1
    return reach_ambient

print("=== SCANNING CENTRAL DENSITY (fixed K, testing 'hits limit and grows') ===")
print(f"K = {K:.3e} (uncalibrated illustrative stiffness -- flagged as free parameter)")
print(f"rho_max = {rho_max:.3e} kg/m^3, rho_inf = {rho_inf:.3e} kg/m^3\n")

print(f"{'rho_c/rho_max':>15} {'R_envelope (km)':>18} {'M_excess (Msun)':>18} {'R(rho>0.99rho_max) km':>24}")

results = []
for frac in [0.9, 0.99, 0.999, 0.9999, 0.99999, 0.999999]:
    rho_c = rho_max * frac
    M_start = (4/3) * np.pi * r0**3 * (rho_c - rho_inf)
    sol = solve_ivp(
        make_derivs(K),
        (r0, 20000.0 * km),
        [rho_c, M_start],
        method='RK45',
        events=make_event(),
        dense_output=True,
        rtol=1e-9,
        atol=1e-9,
        max_step=100 * km
    )
    if sol.status != 1:
        print(f"{frac:>15.6f}  DID NOT TERMINATE CLEANLY -- status={sol.status}, msg={sol.message}")
        continue
    r_env = sol.t[-1]
    M_final = sol.y[1][-1] / Msun

    r_dense = np.logspace(np.log10(r0), np.log10(r_env*0.9999), 2000)
    rho_dense = sol.sol(r_dense)[0]
    mask99 = rho_dense >= 0.99 * rho_max
    r99 = r_dense[np.where(mask99)[0][-1]]/km if np.any(mask99) else 0.0

    print(f"{frac:>15.6f} {r_env/km:>18.3f} {M_final:>18.4f} {r99:>24.4f}")
    results.append((frac, r_env/km, M_final, r99))

print()
print("=== INTERPRETATION ===")
if len(results) >= 2:
    m0 = results[0][2]
    m1 = results[-1][2]
    r0_ = results[0][1]
    r1 = results[-1][1]
    print(f"As central density pushes from {results[0][0]} to {results[-1][0]} of rho_max:")
    print(f"  envelope radius went {r0_:.2f} km -> {r1:.2f} km")
    print(f"  enclosed mass went {m0:.3f} Msun -> {m1:.3f} Msun")
    if m1 > m0 and r1 > r0_:
        print("  -> CONFIRMED: mass and radius both grow together as the interior")
        print("     saturates closer to the compression ceiling. This IS the")
        print("     'hits a limit and grows' behavior, not a fixed-mass cutoff.")
    else:
        print("  -> Did NOT show clear growth -- needs investigation before trusting the mechanism.")
print()
print("COMPARISON: does any of these reach GW150914-relevant mass (~28-36 Msun total system)")
print("at a radius in the tens-of-km range, WITHOUT retuning K to force it?")
