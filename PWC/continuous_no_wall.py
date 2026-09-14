import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

G = 6.674e-11
Msun = 1.989e30
km = 1000.0

rho_inf = 1.0
rho_max = 2 * 2.3e17  # theoretical ceiling, approached near center, not imposed as a wall

# n=1.5, K calibrated in the last run -- reuse those numbers to see how a
# TRULY continuous, wall-free version compares, not to force the same answer
n = 1.5
K = 1.4778e7

def rhs(r, y):
    rho, M = y
    rho = min(max(rho, rho_inf), rho_max)  # physical bounds only, not a wall
    excess = max(rho - rho_inf, 1e-30)
    dPdrho = K * n * excess**(n-1)
    dPdrho = max(dPdrho, 1e-30)
    dPdr = -G * M * rho / r**2
    drhodr = dPdr / dPdrho
    dMdr = 4*np.pi*r**2*rho
    return [drhodr, dMdr]

# Start deep in the interior -- small r0, density essentially at the ceiling
# there (no claim about exactly how deep this is, just "very near center,
# very near max compression" -- the physically motivated starting point)
r0 = 0.5 * km  # start at 0.5 km, well inside where a "core" would be
rho_c = rho_max * 0.999  # essentially at the compression ceiling near center
M0 = (4/3)*np.pi*r0**3*rho_c  # small enclosed mass right at the start, from geometry alone

sol = solve_ivp(rhs, (r0, 1e5*km), [rho_c, M0], max_step=km*2, dense_output=True,
                 method='RK45', rtol=1e-9, atol=1e-6)

r_plot = np.geomspace(r0, sol.t[-1]*0.999, 3000)
rho_plot = sol.sol(r_plot)[0]
M_plot = sol.sol(r_plot)[1]

print("=== CONTINUOUS, WALL-FREE PROFILE (starting near center, no imposed core radius) ===\n")
print(f"{'r (km)':>12} {'density (kg/m^3)':>18} {'enclosed M (Msun)':>18}")
for r_check_km in [1, 5, 10, 20, 30, 40, 50, 100, 200, 500, 1000, 5000, 20000]:
    idx = np.argmin(np.abs(r_plot/km - r_check_km))
    print(f"{r_plot[idx]/km:12.2f} {rho_plot[idx]:18.4e} {M_plot[idx]/Msun:18.4f}")

# where does density cross a "core-like" threshold, e.g. half of rho_max?
half_max_idx = np.argmin(np.abs(rho_plot - rho_max/2))
print(f"\nRadius where density naturally drops to half of max: {r_plot[half_max_idx]/km:.2f} km, "
      f"enclosed mass there: {M_plot[half_max_idx]/Msun:.3f} Msun")
print(f"(For comparison, the already-established core numbers from tonight: "
      f"R_core~30.73 km, M_core~28.118 Msun -- NOT imposed here, just a comparison point)")

plt.figure(figsize=(9,5))
plt.plot(r_plot/km, rho_plot)
plt.axhline(rho_max/2, color='gray', ls=':', label='half of max density')
plt.xscale('log'); plt.yscale('log')
plt.xlabel('r (km)'); plt.ylabel('density (kg/m^3)')
plt.title('Continuous, wall-free density profile from near-center outward')
plt.legend(); plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('pwc_falsification_output/continuous_no_wall.png', dpi=130)
print("\nPlot saved.")
