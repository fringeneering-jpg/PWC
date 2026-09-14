import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

G = 6.674e-11
Msun = 1.989e30
km = 1000.0

rho_inf = 1.0
M_core = 28.118 * Msun
R_core = 30.73 * km
rho_max_local = 2 * 2.3e17
M_grad_target = 7.876 * Msun  # real, already-calibrated number from tonight's k-calculation

def integrate_shell(K, n, r_max_factor=2e5):
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
    r0 = R_core * 1.001
    r_span = (r0, R_core*r_max_factor)
    sol = solve_ivp(rhs, r_span, [rho_max_local, M_core], max_step=R_core*5.0,
                     dense_output=True, method='RK45', rtol=1e-8)
    return sol

def total_shell_mass(K, n):
    sol = integrate_shell(K, n)
    # M(r_final) includes M_core; subtract it to get pure gradient/shell mass
    return sol.y[1, -1] - M_core

print("=== CALIBRATING K against the real M_grad = 7.876 Msun ===\n")
for n in [1.5, 2.0, 3.0]:
    # bracket search for K that gives the target shell mass
    def objective(logK):
        K = np.exp(logK)
        m = total_shell_mass(K, n)
        return m - M_grad_target

    try:
        # search over a wide range of K
        logK_lo, logK_hi = np.log(1e5), np.log(1e14)
        obj_lo, obj_hi = objective(logK_lo), objective(logK_hi)
        print(f"n={n}: objective at K=1e5 -> {obj_lo/Msun:+.3f} Msun offset; "
              f"at K=1e14 -> {obj_hi/Msun:+.3f} Msun offset")
        if obj_lo*obj_hi > 0:
            print(f"  -> target not bracketed in this K range, skipping\n")
            continue
        logK_sol = brentq(objective, logK_lo, logK_hi, xtol=1e-6)
        K_sol = np.exp(logK_sol)
        print(f"  CALIBRATED: K = {K_sol:.4e} gives shell mass = "
              f"{(total_shell_mass(K_sol, n))/Msun:.4f} Msun (target {M_grad_target/Msun:.4f})\n")

        # Now find the "knee": location where the log-log slope of rho(r) changes most sharply
        sol = integrate_shell(K_sol, n)
        r_plot = np.geomspace(R_core*1.002, sol.t[-1]*0.999, 2000)
        rho_plot = sol.sol(r_plot)[0]
        rho_plot = np.maximum(rho_plot, rho_inf*1.0000001)

        log_r = np.log(r_plot)
        log_rho = np.log(rho_plot - rho_inf + 1e-300)  # log of EXCESS density above baseline, tracks the real structure
        # local slope via gradient, then find where the slope's rate of change (curvature) is max
        slope = np.gradient(log_rho, log_r)
        curvature = np.gradient(slope, log_r)
        knee_idx = np.argmax(np.abs(curvature))
        R_knee = r_plot[knee_idx]

        print(f"  KNEE (inflection point of the near-field falloff): R_knee = {R_knee/km:.2f} km "
              f"({R_knee/R_core:.2f}x core radius)")
        print(f"  Density at knee: {sol.sol(R_knee)[0]:.3e} kg/m^3 "
              f"(vs core surface {rho_max_local:.3e}, vs baseline {rho_inf})\n")

        plt.figure(figsize=(8,5))
        plt.plot(r_plot/km, rho_plot, label=f'n={n}, calibrated K={K_sol:.2e}')
        plt.axvline(R_knee/km, color='red', ls='--', label=f'knee at R={R_knee/km:.1f} km')
        plt.xscale('log'); plt.yscale('log')
        plt.xlabel('r (km)'); plt.ylabel('density (kg/m^3)')
        plt.title(f'Calibrated gradient shell (n={n}), mass-matched to 7.876 Msun')
        plt.legend(); plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'pwc_falsification_output/gradient_shell_calibrated_n{n}.png', dpi=130)
    except Exception as e:
        print(f"n={n}: failed ({e})\n")
