# The untied wave's tension self-structure -> alpha_G = G mp^2/(hbar c0)? (2026-10-12)
import math
G = 6.67430e-11; c0 = 2.99792458e8; hbar = 1.054571817e-34
rho0 = 8.74e-27; rho_max = 1.304e15
mp = 1.67262192369e-27; Rp = 8.414e-16
s = 1.0/19.0
lamC = 2*math.pi*hbar/(mp*c0)      # the wave's full wavelength
lam_bar_p = hbar/(mp*c0)

alpha_G = G*mp**2/(hbar*c0)
print(f"the target: alpha_G = G mp^2/(hbar c0) = {alpha_G:.4e}\n")

print("== the untied wave's structure (the locked numbers) ==")
m_w = mp/3.0
V_pair = m_w/rho0
d_pair = V_pair**(1/3.0)
Y_cav = s*rho0*c0**2/3.0
E_tension = Y_cav*V_pair
print(f"wave mass m_w = mp/3 = {m_w:.3e} kg ; pair spacing d = {d_pair:.3f} m")
print(f"rest tension Y_cav = s rho0 c0^2/3 = {Y_cav:.3e} Pa")
print(f"tension energy per pair E = Y V = {E_tension:.3e} J")
print(f"tension mass fraction per pair = {E_tension/c0**2/m_w:.4f}  (= the T7 split 1.75%)")

print("\n== the wave's self-coupling ==")
U_G_proton = G*mp**2/Rp
E_quantum = hbar*c0/Rp
print(f"proton gravitational self-energy U_G = {U_G_proton:.3e} J")
print(f"quantum energy hbar c0/Rp        = {E_quantum:.3e} J")
print(f"alpha_G = U_G / E_quantum = {U_G_proton/E_quantum:.4e}  (the ratio reading)")
self_c = U_G_proton/E_tension
print(f"the tension's self-coupling  U_G / (Y V) = {self_c:.4e}")

print("\n== compositions from the wave's own ratios (the derivation attempt) ==")
ratios = {
  "the T7 tension share": s/3.0,
  "(R_p/lambda_C)^3": (Rp/lamC)**3,
  "(m_p/(rho_max lambda_bar^3))^7": (mp/(rho_max*lam_bar_p**3))**7,
  "rho0/rho_max x lambda_bar/Rp x s": (rho0/rho_max)*(lam_bar_p/Rp)*s,
  "(rho0/rho_max)^(3/2)": (rho0/rho_max)**1.5,
  "(rho0 lambda_C/(rho_max Rp)) x 27/256": (rho0*lamC/(rho_max*Rp))*27/256.0,
}
for name, val in ratios.items():
    print(f"  {name:44s} = {val:.4e}   (target 5.90e-39: {100*(val/alpha_G-1):+.1f}%)")

print("\n== honest verdict ==")
print("the tension self-structure supplies the wave's own ratios - the 1.75% tension")
print("share, the self-coupling 2.53e-37 - but no locked composition of them produces")
print("alpha_G = 5.90e-39. The definition-reading (U_G/E_quantum) is exact and circular")
print("(U_G contains G). The derivation's remaining piece: the dimensionless bridge")
print("between the tension's self-coupling (2.53e-37) and the gravity coupling (5.90e-39) -")
print("a ratio of 23.3 with no locked identity. Reported honestly: the wave's structure")
print("is fully written; its gravity number is the one composition still unnamed.")
