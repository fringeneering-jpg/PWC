# =====================================================================
# CONTINUOUS, WALL-FREE HYDROSTATIC PROFILE -- REGULARIZED (w = sqrt(u))
# Removes the artificial excess_d floor entirely by substituting
# u = rho - rho_inf, w = sqrt(u). For n=1.5 this gives an exactly
# regular ODE dw/dr = -G*M_excess/(3*K*r^2), well-defined all the way
# to w=0 (rho=rho_inf), no clamping required.
# =====================================================================
import numpy as np
from scipy.integrate import solve_ivp

G = 6.6743e-11
Msun = 1.9884e30
km = 1000.0

rho_inf = 1e-15
rho_max = 4.6e17
n = 1.5          # this closed form is specific to n=1.5
K = 1.4778e7

r0 = 1.0
rho_c = rho_max * 0.99
u0 = rho_c - rho_inf
w0 = np.sqrt(u0)
M_start = (4/3) * np.pi * r0**3 * u0

def derivs(t, y):
    w, M_excess = y
    w = max(w, 0.0)              # w is physically non-negative; no lower floor needed beyond this
    dwdr = - (G * M_excess) / (3.0 * K * t**2)
    u = w * w
    dM_excess_dr = 4 * np.pi * (t**2) * u
    return [dwdr, dM_excess_dr]

def w_hits_zero(t, y):
    return y[0]
w_hits_zero.terminal = True
w_hits_zero.direction = -1

sol = solve_ivp(
    derivs,
    (r0, 10000.0 * km),
    [w0, M_start],
    method='RK45',
    events=w_hits_zero,
    dense_output=True,
    rtol=1e-10,
    atol=1e-12,
    max_step=50 * km
)

print("=== RAW SOLVER STATUS ===")
print("status:", sol.status, " message:", sol.message)
print("success:", sol.success)
print("event triggered at t_events:", sol.t_events)
print("number of accepted steps:", len(sol.t))
print("final r reached:", sol.t[-1]/km, "km")
print()

print("=== LAST 10 ACCEPTED STEPS (raw) ===")
print(f"{'r (km)':>12} {'w':>15} {'rho (kg/m3)':>15} {'M_excess/Msun':>15}")
for i in range(max(0, len(sol.t)-10), len(sol.t)):
    w_i = sol.y[0][i]
    rho_i = w_i*w_i + rho_inf
    print(f"{sol.t[i]/km:12.6f} {w_i:15.6e} {rho_i:15.6e} {sol.y[1][i]/Msun:15.6f}")
print()

steps_km = np.diff(sol.t)/km
print("min step (km):", steps_km.min())
print("max step (km):", steps_km.max())
print()

# resample for knee-finding and reporting
r_eval = np.logspace(np.log10(r0), np.log10(sol.t[-1]*0.9999), 3000)
w_curve = sol.sol(r_eval)[0]
w_curve = np.maximum(w_curve, 0.0)
rho_curve = w_curve**2 + rho_inf
M_curve = sol.sol(r_eval)[1] / Msun

excess = np.maximum(rho_curve - rho_inf, 1e-300)
d2lnrho = np.gradient(np.gradient(np.log(excess), np.log(r_eval)), np.log(r_eval))
knee_idx = np.argmax(np.abs(d2lnrho[10:-10])) + 10  # avoid edge artifacts

print("=== FEATURE SUMMARY ===")
mask90 = rho_curve >= 0.9*rho_max
if np.any(mask90):
    idx = np.where(mask90)[0][-1]
    print(f"rho >= 0.9 rho_max out to r = {r_eval[idx]/km:.3f} km, M_excess = {M_curve[idx]:.4f} Msun")
mask50 = rho_curve >= 0.5*rho_max
if np.any(mask50):
    idx = np.where(mask50)[0][-1]
    print(f"rho >= 0.5 rho_max out to r = {r_eval[idx]/km:.3f} km, M_excess = {M_curve[idx]:.4f} Msun")
print(f"knee (max |d2 ln rho / d ln r^2|) at r = {r_eval[knee_idx]/km:.3f} km, M_excess there = {M_curve[knee_idx]:.4f} Msun")
print(f"final enclosed excess mass at termination: {M_curve[-1]:.4f} Msun at r = {r_eval[-1]/km:.3f} km")
print()
print(f"COMPARISON -- calibration target from earlier tonight: M_grad = 7.876 Msun (walled model, R_core=30.73 km)")
