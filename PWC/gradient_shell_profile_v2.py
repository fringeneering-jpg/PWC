import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

G = 6.674e-11
Msun = 1.989e30
km = 1000.0

rho_inf = 1.0
Lambda = 1e-9

M_core = 28.118 * Msun
R_core = 30.73 * km
rho_max_local = 2 * 2.3e17

def solve_shell(K, n, M_core, R_core, r_max_factor):
    def rhs(r, y):
        rho, M = y
        rho = max(rho, rho_inf)
        excess = max(rho - rho_inf, 1e-30)
        dPdrho = K * n * excess**(n-1) if n != 1.0 else K
        dPdrho = max(dPdrho, 1e-30)
        dPdr = -G * M * rho / r**2
        drhodr = dPdr / dPdrho
        dMdr = 4*np.pi*r**2*rho
        return [drhodr, dMdr]

    def hit_baseline(r, y):
        return y[0] - rho_inf*1.0001
    hit_baseline.terminal = True
    hit_baseline.direction = -1

    # Start integration slightly OUTSIDE the core surface to avoid the
    # n=1 degenerate startup case, and use adaptive max_step scaled to
    # distance so large-radius searches don't take forever
    r0 = R_core * 1.001
    r_span = (r0, R_core*r_max_factor)
    sol = solve_ivp(rhs, r_span, [rho_max_local, M_core], max_step=R_core*2.0,
                     events=hit_baseline, dense_output=True, method='RK45', rtol=1e-8)
    return sol

print("=== FIXED: proper startup + much larger search range ===\n")
print(f"Core: M={M_core/Msun:.3f} Msun, R={R_core/km:.2f} km\n")

fig, ax = plt.subplots(figsize=(8,5))
K = 1e10
for n in [1.0, 1.5, 2.0, 3.0]:
    sol = solve_shell(K, n, M_core, R_core, r_max_factor=1e6)  # much larger ceiling
    reached_baseline = len(sol.t_events[0]) > 0
    R_boundary = sol.t[-1]
    print(f"n={n}: {'REACHED baseline' if reached_baseline else 'DID NOT reach baseline (still hit search ceiling)'}"
          f" at R={R_boundary/km:.2f} km ({R_boundary/R_core:.2f}x core radius)")
    if len(sol.t) > 1:
        ax.plot(sol.t/km, sol.y[0], label=f'n={n} ({"reached" if reached_baseline else "did not reach"} baseline)')

ax.set_xlabel('r (km)'); ax.set_ylabel('density (kg/m^3)'); ax.set_yscale('log'); ax.set_xscale('log')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('pwc_falsification_output/gradient_shell_profile_v2.png', dpi=130)
print("\nPlot saved.")
