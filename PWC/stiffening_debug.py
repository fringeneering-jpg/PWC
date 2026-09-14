import numpy as np
from scipy.integrate import solve_ivp

G = 6.6743e-11
Msun = 1.9884e30
km = 1000.0
rho_inf = 1e-15
rho_max = 4.6e17
K = 1.0e7
r0 = 1.0

def derivs(t, y):
    rho, M_excess = y
    rho = min(max(rho, rho_inf), rho_max*(1-1e-14))
    u = rho - rho_inf
    dPdrho = K * rho_max * (rho_max - rho_inf) / (rho_max - rho)**2
    dPdr = - (G * M_excess * u) / (t**2)
    drhodr = dPdr / dPdrho
    dM_excess_dr = 4 * np.pi * (t**2) * u
    return [drhodr, dM_excess_dr]

frac = 0.99
rho_c = rho_max*frac
M_start = (4/3)*np.pi*r0**3*(rho_c-rho_inf)
print("M_start (kg):", M_start, " = ", M_start/Msun, "Msun")

y0 = [rho_c, M_start]
d0 = derivs(r0, y0)
print("initial derivs at r0=1m:", d0)
print("  drhodr:", d0[0], " dM_excess_dr:", d0[1])
dPdrho0 = K*rho_max*(rho_max-rho_inf)/(rho_max-rho_c)**2
print("dPdrho at rho_c:", dPdrho0)
dPdr0 = -(G*M_start*(rho_c-rho_inf))/r0**2
print("dPdr at r0:", dPdr0)

def event(t,y):
    return y[0]-rho_inf*1.0001
event.terminal=True
event.direction=-1

sol = solve_ivp(derivs, (r0, 20000*km), y0, method='RK45', events=event, dense_output=True, rtol=1e-9, atol=1e-9, max_step=100*km)
print("\nstatus:", sol.status, sol.message)
print("num steps:", len(sol.t))
print("\nfirst 15 raw steps:")
print(f"{'r(m)':>14} {'rho':>15} {'M_excess/Msun':>15}")
for i in range(min(15,len(sol.t))):
    print(f"{sol.t[i]:14.6f} {sol.y[0][i]:15.6e} {sol.y[1][i]/Msun:15.8e}")
print("\nlast 10 raw steps:")
for i in range(max(0,len(sol.t)-10), len(sol.t)):
    print(f"{sol.t[i]:14.6f} {sol.y[0][i]:15.6e} {sol.y[1][i]/Msun:15.8e}")
