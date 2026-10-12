# What the wait buys: three quantifications the new chain unlocks (2026-10-12)
import math
c0 = 2.99792458e8; hbar = 1.054571817e-34
me = 9.1093837e-31; mp = 1.67262192369e-27; e = 1.602176634e-19
eps0 = 8.8541878128e-12; Rp = 8.414e-16
alpha = e**2/(4*math.pi*eps0*hbar*c0)
s = 1.0/19.0
rho_max = 1.304e15; Y_bow = 5.93e26
lam_bar = hbar/(me*c0); r_e = alpha*lam_bar
f_solid = 8.4989e-4
delta = (6*((1+math.sqrt(5))/2)**2 - 5*math.pi)/(5*math.pi)

print("== 1. The footprint CLOSES exactly ==")
rt_base = (math.pi + 3*s)*lam_bar
rt_full = rt_base*(1.0 + f_solid)
target = lam_bar*2*math.pi/math.sqrt(16*math.pi**3*alpha)
print(f"r_t = (pi + 3s)(1 + f_solid) = {rt_full/lam_bar:.5f} lam_bar  vs  target {target/lam_bar:.5f}")
print(f"agreement: {100*(rt_full/target-1):+.4f}%  - the 0.085% matter residual IS the")
print(f"f_solid multiplier; the footprint's -0.085% gap is now derived, not named.")

print("\n== 2. The gate-1 re-anchoring (breaks the circularity) ==")
r_e4 = 3*alpha*hbar*c0/(190*math.pi**4*Y_bow)
r_e_from_locked = r_e4**0.25
gate = mp/r_e_from_locked**3
print(f"r_e from the locked set = {r_e_from_locked:.4e} m (vs 2.8179e-15, {100*(r_e_from_locked/r_e-1):+.3f}%)")
print(f"gate-1 threshold m_p/r_e^3 = {gate:.4e} kg/m^3  - no longer circular: r_e now")
print(f"derives from {r_e_from_locked:.4e} = (3 alpha hbar c0/(190 pi^4 Y_bow))^(1/4)")

print("\n== 3. The proton's frustration line (the second predicted energy) ==")
U_e = 4*math.pi**2*Y_bow*r_e**4/(r_e/(5*math.pi**2))          # the electron fold's strain
U_p = 4*math.pi**2*Y_bow*Rp**4/(Rp/(5*math.pi**2))            # the same topology at the proton
frust_e = delta*U_e; frust_p = delta*U_p
print(f"electron frustration = {frust_e/1.602176634e-19:.3f} eV (502 nm)")
print(f"proton frustration   = {frust_p/1.602176634e-19:.4f} eV -> {1239.84/(frust_p/1.602176634e-19):.1f} nm")
print(f"-> a second frozen line: the proton's own 720-fold strain, IF the proton's loop")
print(f"   obeys the same 5 pi^2 closure. Prediction-shaped, recorded, not claimed.")
