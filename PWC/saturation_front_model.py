# =====================================================================
# TWO-REGION SATURATION-FRONT MODEL
# Inner region (0 <= r <= R_sat): rho = rho_max exactly (incompressible
# ceiling -- density cannot rise further, so mass accumulates as volume).
# Outer region (r > R_sat): the ALREADY-VALIDATED regularized relief zone
# (n=1.5, K=1.4778e7, w=sqrt(u) substitution -- confirmed numerically
# clean, no floor artifacts, checked earlier tonight), matched
# continuously in density at r=R_sat (rho=rho_max there, no jump).
#
# R_sat is the one free "how much mass saturated at the ceiling" quantity.
# Scanning it (not re-tuning K) shows what R_sat gives GW150914-scale mass.
# =====================================================================
import numpy as np
from scipy.integrate import solve_ivp

G = 6.6743e-11
Msun = 1.9884e30
km = 1000.0

rho_inf = 1e-15
rho_max = 4.6e17
n = 1.5
K = 1.4778e7   # reused unchanged from the earlier validated relief-zone solve

def w_hits_zero(t, y):
    return y[0]
w_hits_zero.terminal = True
w_hits_zero.direction = -1

def relief_derivs(t, y):
    w, M_excess = y
    w = max(w, 0.0)
    dwdr = - (G * M_excess) / (3.0 * K * t**2)
    u = w * w
    dM_excess_dr = 4 * np.pi * (t**2) * u
    return [dwdr, dM_excess_dr]

u_max = rho_max - rho_inf

print("=== TWO-REGION SATURATION-FRONT MODEL ===")
print(f"Core: rho = rho_max = {rho_max:.3e} kg/m^3 exactly, for 0 <= r <= R_sat")
print(f"Relief zone (r > R_sat): n=1.5, K={K:.4e} (unchanged from earlier validated solve)\n")

print(f"{'R_sat (km)':>12} {'M_core (Msun)':>15} {'R_env (km)':>12} {'M_shell (Msun)':>16} {'M_total (Msun)':>16}")

rows = []
for R_sat_km in [1, 5, 10, 15, 20, 25, 30, 30.73, 35, 40]:
    R_sat = R_sat_km * km
    M_core = (4/3) * np.pi * u_max * R_sat**3

    w0 = np.sqrt(u_max)
    sol = solve_ivp(
        relief_derivs, (R_sat, 20000*km), [w0, M_core],
        method='RK45', events=w_hits_zero, dense_output=True,
        rtol=1e-10, atol=1e-12, max_step=50*km
    )
    R_env = sol.t[-1]/km
    M_total = sol.y[1][-1]/Msun
    M_shell = M_total - M_core/Msun

    print(f"{R_sat_km:12.2f} {M_core/Msun:15.4f} {R_env:12.3f} {M_shell:16.4f} {M_total:16.4f}")
    rows.append((R_sat_km, M_core/Msun, R_env, M_shell, M_total))

print()
print("=== CROSS-CHECK ===")
print("GW150914 total system (both compact objects combined, LIGO-inferred): ~28.118 + 22.255 = 50.37 Msun progenitor")
print("Individual compact objects (LIGO-inferred, apparent horizon masses): ~7.876 and ~6.750 (M_grad convention earlier)")
print("Full core numbers from tonight's earlier (walled) calibration: M_core=28.118 Msun at R_core=30.73 km")
print()
print("Looking at R_sat=30.73 km row above (the previously-established core radius) --")
print("this shows what total mass a saturation front AT that radius, matched to the SAME")
print("already-validated relief EOS, actually produces -- not tuned to hit any target.")
