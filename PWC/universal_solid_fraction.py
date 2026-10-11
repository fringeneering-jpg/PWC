# The universal 0.085%: every knot has the same solid fraction (2026-10-09, Jaden's ruling)
# "the black hole made of neutrons and the medium at max p has the same 0.08% right,
#  everything does from our measurements, even electrons"
import math
G = 6.6743e-11; a0 = 6.6e-11
rho0 = 8.74e-27
hbar = 1.054571817e-34; c0 = 2.99792458e8; me = 9.1093837e-31
Msun = 1.989e30
f_solid = 0.00085

print(f"the universal solid fraction: f_solid = 0.085% = {f_solid}  (everything)")

print("\n== the drag with the universal fraction ==")
# electron
lamC_bar = hbar/(me*c0); r_t = 3.3023*lamC_bar
A_e = math.pi*r_t**2
F_e = 0.5*rho0*c0**2*f_solid*A_e
print(f"electron:  A_geo = {A_e:.2e} m^2 -> F = {F_e:.2e} N at c0")
# neutron star
R_ns = 1.2e4; v = 9.0e5
A_ns = math.pi*R_ns**2
F_ns = 0.5*rho0*v**2*f_solid*A_ns
print(f"neutron star: A_geo = {A_ns:.2e} m^2 -> F = {F_ns:.2e} N at 900 km/s")
# SMBH shell
M_bh = 2.0e7*Msun; a_max = 3.23e11
R_shell = math.sqrt(G*M_bh/a_max)
A_bh = math.pi*R_shell**2
F_bh = 0.5*rho0*(9.5e5)**2*f_solid*A_bh
print(f"SMBH shell:   A_geo = {A_bh:.2e} m^2 -> F = {F_bh:.2e} N at 950 km/s")

print("\n== what this settles ==")
print("every form of matter - the electron, the neutron core, the rho_max medium - carries")
print("the SAME 0.085% solid fraction. The drag is the same fraction of the frontal area for")
print("everything: universally negligible. Nobody drags because of solidity.")
print("The 954 wall is therefore NOT the solid fraction - it is the YIELD: the displacement")
print("budget spent, the medium unable to make room. The fraction is universal; the cap is")
print("the speed wall. The two rulings reconcile: same substance, same fraction, one cap.")
print("The earlier full-frontal drag computation is corrected: the shell is not 'more solid'")
print("than the electron - it is the same 0.085%, just at the yield.")
