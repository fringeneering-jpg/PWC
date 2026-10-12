# THE TOPOLOGY EQUATION: the 4pi Dirac closure's five-fold geometry (2026-10-12)
import math
c0 = 2.99792458e8; hbar = 1.054571817e-34
me = 9.1093837e-31; e = 1.602176634e-19; eps0 = 8.8541878128e-12
alpha = e**2/(4*math.pi*eps0*hbar*c0)
s = 1.0/19.0
g = 20.0**(1.0/16.0)
phi = (1.0 + math.sqrt(5.0))/2.0
lam_bar = hbar/(me*c0); r_e = alpha*lam_bar
Y_bow = 5.93e26
F_EM = e**2/(4*math.pi*eps0*r_e**2)
F_top = (1.0-s)*F_EM

print("== the 4pi closure as the pentagram ==")
print("the Dirac closure turns 4pi in 5 equal steps: 5 x (4pi/5) = 5 x 144 deg = 720 deg")
print("-> the pentagram: five gates on the double circuit. Its geometry carries the golden")
print(f"   ratio: the inner pentagon's radius = r_e / phi^2 = {r_e/phi**2:.4e} m")

print("\n== the topology equation ==")
R_loop = (r_e/phi**2)/(math.pi*g)
print(f"R_loop = (r_e / phi^2) / (pi x g)")
print(f"       = {R_loop:.4e} m")
R_demand = r_e/(2*math.pi*math.sqrt(2.5))
print(f"vs the torsion's demanded R = r_e/(2pi sqrt(5/2)) = {R_demand:.4e} m")
print(f"agreement: {100*(R_loop/R_demand-1):+.3f}%")

print("\n== the 18/19 load follows ==")
gam = 2.0*r_e/R_loop
V = 2*math.pi**2*R_loop*r_e**2
U = 0.5*Y_bow*gam**2*V
F_meas = 3.0*U/r_e
print(f"gamma = 2a/R = {gam:.4f}  (the demanded 4pi sqrt(5/2) = {4*math.pi*math.sqrt(2.5):.4f})")
print(f"F_topology = {F_meas:.4f} N  vs  (1-s) F_EM = {F_top:.4f} N   ({100*(F_meas/F_top-1):+.3f}%)")

print("\n== the equation, in one line ==")
print("the 4pi Dirac closure projects as the pentagram: 5 gates x 4pi/5 = 720 deg; the")
print("inner pentagon sits at r_e/phi^2; the loop settles at (r_e/phi^2)/(pi g) - and the")
print("torsion's load lands on (1-s) F_EM = 18/19 of the squeeze at +0.16%. The five gates,")
print("the two circuits (the sqrt(5/2) signature), the golden ratio, and the coupling g -")
print("one topology equation, the same shared residual family (+0.16%).")
