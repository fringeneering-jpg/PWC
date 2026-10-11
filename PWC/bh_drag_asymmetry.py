# Black holes drag, we don't: run the asymmetry (2026-10-09, Jaden's mechanism)
import math
G = 6.6743e-11; a0 = 6.6e-11
rho0 = 8.74e-27; rho_max = 1.304e15
mp = 1.6726e-27; Rp = 8.414e-16; rho_core = 2.3e17
Msun = 1.989e30

print("== 1. Ordinary matter: the medium passes through (the sieve) ==")
R_ns = 1.2e4
d_knot = (mp/rho_core)**(1/3.0); pack = (Rp/d_knot)**2
A_sieve = pack*math.pi*R_ns**2
v = 9.0e5
F_ns = 0.5*rho0*v**2*A_sieve
print(f"neutron star frontal area (the knots only): {A_sieve:.2e} m^2")
print(f"drag force = {F_ns:.2e} N  ->  friction power = {F_ns*v:.2e} W  (the 0.27 W: nothing)")

print("\n== 2. The black hole: the shell is impassable - the full reach captures the flux ==")
M_bh = 2.0e7*Msun                          # RBH-1
r_reach = math.sqrt(G*M_bh/a0)             # the holding reach (192 pc)
A_bh = math.pi*r_reach**2
F_bh = 0.5*rho0*(9.5e5)**2*A_bh
a_drag = F_bh/M_bh
print(f"reach = {r_reach/3.0857e16:.0f} pc ; frontal area = {A_bh:.2e} m^2")
print(f"drag force = {F_bh:.2e} N ; deceleration = {a_drag:.2e} m/s^2")
dt = 3.15e14                              # 10 Myr
print(f"speed lost in 10 Myr: {a_drag*dt:.2f} m/s  ->  the drag is real but glacial")
print(f"damping time at 950 km/s: {9.5e5/a_drag/3.15e16:.1f} Gyr  (vs the universe's 13.8)")

print("\n== 3. What actually rests the SMBHs ==")
print("the hole sits INSIDE its own held medium - no relative flow, no drag (the shell and")
print("the medium co-move). The kicked ones (CID-42, 3C 186) leave the held shell behind,")
print("hit the ambient at 1000-2500 km/s - ABOVE the cap - the slammed regime (the recoil")
print("check's finding). The rest = the co-moving shell; the kicked = the slam.")

print("\n== verdict ==")
print("his asymmetry is right in kind: the shell is impassable (drag), the sieve is not")
print("(none). But the drag's size (1e-14 m/s^2) cannot be what rests the SMBHs - it is the")
print("held-medium co-motion. The drag ramps toward the yield as v -> 954: the near-cap")
print("brake is where RBH-1 (950 km/s) and the recoil candidates live - the two regimes")
print("of the same law.")
