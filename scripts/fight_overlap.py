# The fight: cores plow the overlap Max-P medium out of the way (2026-10-08)
import math
G = 6.6743e-11
c0 = 2.99792458e8
c0sq = c0**2
rho_core = 2.3e17
rho_max = 1.304e15
a_max = 3.23e11
Msun = 1.989e30
k = 0.868899

M1, M2 = 35.6, 30.6
R1 = (3*M1*Msun/(4*math.pi*rho_core))**(1/3)
R2 = (3*M2*Msun/(4*math.pi*rho_core))**(1/3)
E1 = math.sqrt(G*M1*Msun/a_max)        # reach edge (the shell outer radius)
E2 = math.sqrt(G*M2*Msun/a_max)
t1 = E1 - R1
t2 = E2 - R2
print(f"R1 = {R1/1e3:.1f} km, R2 = {R2/1e3:.1f} km; edges = {E1/1e3:.1f}/{E2/1e3:.1f} km; "
      f"t = {t1/1e3:.0f}/{t2/1e3:.0f} km")

def Vcap(r, R, s):
    if s >= r + R: return 0.0
    if s <= abs(r - R): return 4*math.pi*min(r, R)**3/3.0
    return math.pi*(r + R - s)**2*(s**2 + 2*s*(r+R) - 3*(r-R)**2)/(12.0*s)

def V_overlap(t1, t2, s):
    return (Vcap(R1+t1, R2+t2, s) - Vcap(R1+t1, R2, s)
            - Vcap(R1, R2+t2, s) + Vcap(R1, R2, s))

s0 = R1 + R2 + t1 + t2          # first shell-shell touch
s1 = R1 + R2                    # core-core contact (cores cannot overlap: volume additive)
V_ov0 = V_overlap(t1, t2, s0)
V_ov1 = V_overlap(t1, t2, s1)
m_ov = V_ov1*rho_max
E_motion = G*M1*M2*Msun**2/(2.0*c0sq*(E1+E2))
print(f"\noverlap volume at first touch: {V_ov0:.3e} m^3 (zero: tangent shells)")
print(f"overlap volume at CORE CONTACT (the displaced medium): {V_ov1:.3e} m^3")
print(f"displaced mass m_ov = rho_max*V_ov = {m_ov/Msun:.2f} Msun")
print(f"motion energy at contact as mass: {E_motion/Msun:.2f} Msun  (dump prediction)")
print(f"FULL potential as mass: {2*E_motion/Msun:.2f} Msun")
print(f"-> full potential / displaced = {2*E_motion/m_ov:.3f}")

print("\n== The fight reading ==")
print("P_max*dV work: W = rho_max c0^2 * V_ov = m_ov*c0^2 - displacing the overlap costs its")
print("own rest energy. The cores' full potential budget (2x the circular motion energy) pays")
print("for pushing the ENTIRE overlap out of the way. The observed dump (3.0-3.34 Msun) is the")
print("half that leaves as the wave; the other half ends as the merged spin (the session log's")
print("virial half). The fight = the displacement; the dump = the wave; the sum = the overlap.")
