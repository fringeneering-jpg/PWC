# The neck: after core-edge contact, the contact point becomes the highest pull (2026-10-08)
import math
G = 6.6743e-11
rho_core = 2.3e17
a_max = 3.23e11
Msun = 1.989e30

M1, M2 = 35.6, 30.6
R1 = (3*M1*Msun/(4*math.pi*rho_core))**(1/3)
R2 = (3*M2*Msun/(4*math.pi*rho_core))**(1/3)
g1 = G*M1*Msun/R1**2
g2 = G*M2*Msun/R2**2
g_contact = g1 + g2
print(f"surface pulls: g1 = {g1:.3e}, g2 = {g2:.3e} m/s^2")
print(f"combined pull at the contact point: {g_contact:.3e} = {g_contact/a_max:.1f}x the yield")

print("\n== The neck edge: where the combined pull along the axis drops to the yield ==")
def g_axis(d):
    return g1*(R1/(R1+d))**2 + g2*(R2/(R2+d))**2
lo, hi = 0.0, 5e5
for _ in range(60):
    mid = 0.5*(lo+hi)
    if g_axis(mid) > a_max: lo = mid
    else: hi = mid
d_neck = 0.5*(lo+hi)
print(f"axis edge beyond the contact point: d_neck = {d_neck/1e3:.1f} km")
print(f"-> the Max-P layer at the neck extends {d_neck/1e3:.1f} km past contact along the axis")

print("\n== Contrast with the merged system ==")
M_t = M1 + M2
R_c = (3*M_t*Msun/(4*math.pi*rho_core))**(1/3)
E_m = math.sqrt(G*M_t*Msun/a_max)
print(f"merged core: {M_t:.0f} Msun, R = {R_c/1e3:.1f} km; merged edge = {E_m/1e3:.1f} km;")
print(f"merged shell thickness = {E_m/1e3 - R_c/1e3:.1f} km")
print(f"at the neck the pull is {g_contact/a_max:.1f}x the yield vs the merged surface pull")
g_m = G*M_t*Msun/R_c**2
print(f"{g_m:.3e} = {g_m/a_max:.1f}x -> the contact point is the HIGHEST pull in the merger;")
print(f"the medium there is forced by both sides and stacks thickest at the neck (his ruling).")
