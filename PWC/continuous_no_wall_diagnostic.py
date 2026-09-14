# =====================================================================
# DIAGNOSTIC RE-RUN of the pasted "continuous hydrostatic phase gradient"
# script, unmodified physics, but with real solver introspection instead
# of trusting the printed summary. Checking: did solve_ivp actually reach
# the event cleanly, or stall/underflow near the reported "knee"?
# =====================================================================
import numpy as np
from scipy.integrate import solve_ivp

G = 6.6743e-11
Msun = 1.9884e30
km = 1000.0

rho_inf = 1e-15
rho_max = 4.6e17
n = 1.5
K = 1.4778e7

r0 = 1.0
rho_c = rho_max * 0.99
M_start = (4/3) * np.pi * r0**3 * (rho_c - rho_inf)

floor_hits = {"count": 0, "first_r": None, "last_r": None}

def eos_outward_yield(t, y):
    rho, M_excess = y
    rho = max(rho, rho_inf)
    raw_excess = rho - rho_inf
    excess_d = max(raw_excess, 1e-10)

    if raw_excess < 1e-10:
        floor_hits["count"] += 1
        if floor_hits["first_r"] is None:
            floor_hits["first_r"] = t
        floor_hits["last_r"] = t

    dPdrho = K * n * excess_d**(n-1)
    if dPdrho < 1e-15:
        return [0.0, 0.0]
    dPdr = - (G * M_excess * excess_d) / (t**2)
    drhodr = dPdr / dPdrho
    dM_excess_dr = 4 * np.pi * (t**2) * excess_d
    return [drhodr, dM_excess_dr]

def reach_ambient_density(t, y):
    return y[0] - (rho_inf * 1.01)
reach_ambient_density.terminal = True

sol = solve_ivp(
    eos_outward_yield,
    (r0, 10000.0 * km),
    [rho_c, M_start],
    method='RK45',
    events=reach_ambient_density,
    dense_output=True,
    rtol=1e-8,
    atol=1e-6
)

print("=== RAW SOLVER STATUS ===")
print("status:", sol.status, " message:", sol.message)
print("success:", sol.success)
print("event triggered at t_events:", sol.t_events)
print("number of accepted steps (len sol.t):", len(sol.t))
print("final integrator t reached:", sol.t[-1]/km, "km")
print("t span requested: up to", 10000.0, "km")
print()

print("=== EXCESS-DENSITY FLOOR (1e-10) HIT DIAGNOSTIC ===")
print("floor hit count during derivative evals:", floor_hits["count"])
print("first r where raw_excess < 1e-10 floor kicked in:",
      None if floor_hits["first_r"] is None else floor_hits["first_r"]/km, "km")
print("last r where floor active:",
      None if floor_hits["last_r"] is None else floor_hits["last_r"]/km, "km")
print()

print("=== LAST 15 ACCEPTED SOLVER STEPS (raw, not interpolated) ===")
print(f"{'r (km)':>12} {'rho (kg/m3)':>15} {'M_excess/Msun':>15} {'dr_step (km)':>14}")
rs = sol.t
for i in range(max(0, len(rs)-15), len(rs)):
    dr = (rs[i]-rs[i-1])/km if i > 0 else float('nan')
    print(f"{rs[i]/km:12.4f} {sol.y[0][i]:15.4e} {sol.y[1][i]/Msun:15.4f} {dr:14.6f}")
print()

print("=== STEP SIZE COLLAPSE CHECK ===")
steps_km = np.diff(rs)/km
print("min step (km):", steps_km.min() if len(steps_km) else None)
print("max step (km):", steps_km.max() if len(steps_km) else None)
print("median step over last 20 steps (km):", np.median(steps_km[-20:]) if len(steps_km) >= 20 else steps_km)

print()
print("=== FINAL VALUES ===")
print("final rho:", sol.y[0][-1], " rho_inf*1.01 target:", rho_inf*1.01)
print("final M_excess (Msun):", sol.y[1][-1]/Msun)
