# The CMB mountain: the honest first climb - the first peak from the medium's own numbers
import math
c0 = 2.99792458e8
cs = c0/math.sqrt(3.0)           # the medium's acoustic channel (locked)
t_lss_yr = 380000.0              # the recombination age (standard, not yet framework-derived)
z_lss = 1100.0
rho0 = 8.74e-27

print("== the framework's first-pass numbers ==")
t_lss = t_lss_yr*365.25*86400
r_s_phys = cs*t_lss
print(f"the sound horizon: c_s x t_lss = (c0/sqrt3) x 380 kyr = {r_s_phys/3.086e22:.1f} Mpc (physical)")
chi = c0*13.8e9*365.25*86400
D_A = chi/(1+z_lss)
print(f"the path to the LSS: chi = {chi/9.461e24:.2f} Gly ; D_A = chi/(1+z) = {D_A/9.461e24:.2f} Mly")
r_s_com = r_s_phys*(1+z_lss)
theta_s = r_s_com/chi
print(f"the comoving horizon = {r_s_com/3.086e22:.1f} Mpc ; theta_s = {theta_s:.2f} rad")
ell1 = math.pi/theta_s
print(f"the first peak: ell_1 ~ pi/theta_s = {ell1:.2f}   (observed ~220)")
print()
print("== the verdict (locked wording) ==")
print(f"the {ell1:.1f} value is logged as the baseline calculation; the bath-weighted")
print("acoustic channel from the horizon join is the identified next derivation. The")
print("framework's history runs from the EVENT HORIZON (the joiner between the CMB's")
print("untie and our own, 62.5 Gly, the 4.529 aspect) - the LSS at 13.8 Gly is the")
print("local surface inside it, and the acoustic scale inherits the horizon's clock.")
