# THE FINAL BOSS: the 4pi torsion twist - measuring the topology's hold (2026-10-12)
import math
c0 = 2.99792458e8; hbar = 1.054571817e-34
me = 9.1093837e-31; e = 1.602176634e-19; eps0 = 8.8541878128e-12
alpha = e**2/(4*math.pi*eps0*hbar*c0)
s = 1.0/19.0
lam_bar = hbar/(me*c0); r_e = alpha*lam_bar
Y_bow = 5.93e26          # the 954 km/s yield wall
Y_cav = 1.378e-11        # the baseline tension
F_EM = e**2/(4*math.pi*eps0*r_e**2)
F_topology = (1.0-s)*F_EM
print(f"the target: F_topology = (1-s) F_EM = {F_topology:.4f} N  (18/19 of the squeeze {F_EM:.4f})\n")

print("== reading 1: the yield wall's plastic torsion (the capped shear) ==")
a = r_e; R = r_e
J = math.pi*a**4/2.0
tau_yield = Y_bow*J/a                       # the plastic torque at the yield
F_1 = tau_yield/R
print(f"  tau = Y_bow J/a = {tau_yield:.4e} Nm ; F = tau/R = {F_1:.4e} N   ({F_1/F_topology:.1e} of target)")

print("\n== reading 2: the elastic torsion, geometric strain gamma = 2a/R ==")
gam = 2.0*a/R
V = 2*math.pi**2*R*a**2
U = 0.5*Y_bow*gam**2*V
F_2 = 3.0*U/r_e
print(f"  U = 1/2 Y_bow gam^2 V = {U:.4e} J ; F = dU/dr = {F_2:.4f} N   ({F_2/F_topology:.1e} of target)")

print("\n== reading 3: the phase-lock spring (the footprint's k = me wC^2) ==")
wC = c0/lam_bar; k = me*wC**2
F_3 = k*r_e
print(f"  F = k r_e = {F_3:.4e} N   ({F_3/F_topology:.1e} of target)")

print("\n== the honest first blow ==")
print(f"the torsion with the geometric strain (2a/R = 2 at the fold) gives {F_2:.3f} N -")
print(f"{F_topology/F_2:.1f}x short of the needed {F_topology:.1f} N. The needed strain:")
gam_need = math.sqrt(F_topology/(1.5*math.pi**2*Y_bow*r_e**2))
print(f"  gamma = {gam_need:.4f} = 4pi x {gam_need/(4*math.pi):.4f}  (4pi x (sqrt5/2) = 14.049)")
print(f"the strain amplification over the geometry: {gam_need/2.0:.3f}x - the twist's effective")
print(f"strain at the fold. The named unknown: the fold's exact tube/loop geometry (the")
print(f"compressed tube's shape) - the ratio a/R at the fold that produces gamma = 4pi(sqrt5/2).")
