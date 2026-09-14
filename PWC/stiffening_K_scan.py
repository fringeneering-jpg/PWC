import numpy as np
from scipy.integrate import solve_ivp

G = 6.6743e-11
Msun = 1.9884e30
km = 1000.0
c = 2.998e8
rho_inf = 1e-15
rho_max = 4.6e17
r0 = 1.0

def make_derivs(K):
    def derivs(t, y):
        rho, M_excess = y
        rho = min(max(rho, rho_inf), rho_max*(1-1e-14))
        u = rho - rho_inf
        dPdrho = K * rho_max * (rho_max - rho_inf) / (rho_max - rho)**2
        dPdr = - (G * M_excess * u) / (t**2) if M_excess > 0 else 0.0
        drhodr = dPdr / dPdrho
        dM_excess_dr = 4 * np.pi * (t**2) * u
        return [drhodr, dM_excess_dr]
    return derivs

def event(t, y):
    return y[0] - rho_inf*1.0001
event.terminal = True
event.direction = -1

frac = 0.99
rho_c = rho_max*frac
M_start = (4/3)*np.pi*r0**3*(rho_c-rho_inf)

print("=== SCANNING K (stiffness) AT FIXED rho_c = 0.99 rho_max ===")
print(f"{'K (m^2/s^2)':>14} {'K/c^2':>10} {'R_env (km)':>14} {'M_excess (Msun)':>18} {'status':>10}")

for K in [1e7, 1e10, 1e13, 1e15, 1e16, 3e16, 1e17, 3e17, 1e18, 1e19, 1e20]:
    sol = solve_ivp(
        make_derivs(K), (r0, 2_000_000.0*km), [rho_c, M_start],
        method='RK45', events=event, dense_output=True,
        rtol=1e-9, atol=1e-9, max_step=1000*km
    )
    r_env = sol.t[-1]/km
    M_final = sol.y[1][-1]/Msun
    print(f"{K:14.3e} {K/c**2:10.3e} {r_env:14.4f} {M_final:18.6e} {sol.status:>10}")
