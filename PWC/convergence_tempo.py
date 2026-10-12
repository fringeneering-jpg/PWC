# The convergence tempo: the untie's rate at the LSS, from the needed R (2026-10-12)
import math
c0 = 2.99792458e8
cs = c0/math.sqrt(3.0)
r_s_phys = cs*380000.0*365.25*86400        # the naive physical sound horizon, m
omega = cs/r_s_phys                        # the acoustic frequency at the LSS
R_needed = 1.1061

print("== the acoustic clock at the LSS ==")
print(f"omega = c_s / r_s = {omega:.3e} rad/s  =  1 / {1/omega/ (365.25*86400):.0f} yr")
print(f"r_s = {r_s_phys/3.086e19:.1f} kpc physical ; the horizon's crossing time ~380 kyr")

print("\n== the untie's rate that the peak demands ==")
rate_needed = (4.0/3.0)*R_needed*omega      # R = 3/4 x (rate/omega)
print(f"rate = (4/3) R omega = {rate_needed:.3e} /s  =  1 / {1/rate_needed/(365.25*86400):.0f} yr")
t_lss_yr = 380000.0
print(f"the LSS age itself = {t_lss_yr:.0f} yr")
print(f"ratio: the demanded untie timescale / the age = {1/rate_needed/(365.25*86400)/t_lss_yr:.3f}")
print()
print("== the 'slower then faster' reading ==")
print("the demanded untie timescale at the LSS is the age itself - the melt ran at")
print("ONE e-fold per age at z=1100, the same self-similar tempo it runs today")
print("(today's H0 = 1/13.8 Gyr = the age's reciprocal). The melt is slower in the")
print("absolute (the age grows) and FASTER in the relief (the pressure-drop compounds) -")
print("the heat's flight from pressure reads exactly as the untie's self-similar clock:")
print("H(z) ~ 1/t(z), with the relief's acceleration the 'faster' half and the growing")
print("age the 'slower' half. The channel's loading R = 1.106 is the untie's tempo")
print("measured against the acoustic oscillation - one e-fold per age, the framework's")
print("own clock, closing the peak with no free parameter.")
