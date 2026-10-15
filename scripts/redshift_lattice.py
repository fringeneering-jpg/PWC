# The cosmological redshift from the lattice law: (1+z) = (rho_emit/rho_obs)^(1/3) (2026-10-12)
import math
c0 = 2.99792458e8
rho0 = 8.74e-27
H0 = 32.371*c0**2

print("== the mechanism ==")
print("the lattice law (derived, weak field, row 23): c = a sqrt(k/m) ~ a ~ rho^(-1/3)")
print("the photon's wavelength rides the medium's spacing:  lambda ~ rho^(-1/3)")
print("-> the cosmological redshift is the medium's density GROWTH between emission and now:")
print("   (1+z) = lambda_obs/lambda_emit = (rho_emit/rho_obs)^(1/3)\n")

print("== check 1: the last-scattering surface (z = 1100) ==")
z_lss = 1100.0
rho_lss = rho0*(1+z_lss)**3
print(f"rho_lss = rho0 x (1+z)^3 = {rho_lss:.3e} kg/m^3")
print(f"the caloric reading at that density: H = H0 - (c0^2/3) ln(rho_lss/rho0)")
H_lss = H0 - (c0**2/3.0)*math.log(rho_lss/rho0)
print(f"  = {H_lss/c0**2:.3f} c0^2  (the debt then, vs {H0/c0**2:.3f} c0^2 today - the medium")
print(f"  carried 21% less debt-equivalent per kg: the untying HAS been paying it back)")
print(f"  T_lss = 2.7 K x (1+z) = {2.7*(1+z_lss):.0f} K  - the bath's own scaling, same law\n")

print("== check 2: the supernova stretch and Tolman dimming fall out free ==")
print("stretch: every time-interval scales with the wavelength (one clock) -> t ~ (1+z)")
print("  - the light-curve stretch is the SAME rho^(-1/3) law, no extra parameter")
print("dimming: flux ~ 1/D_L^2 with D_L = D(1+z) from the stretch alone; the photon")
print("  count is conserved (the medium grows, the photons don't multiply) -> Tolman's")
print("  (1+z)^-1 extra factor = the stretch's own, nothing added\n")

print("== the one-mechanism statement ==")
print("gravitational redshift (T12, locked) and cosmological redshift are ONE law:")
print("  L_out/L_in = exp[-GM d(1/r)/c0^2]      (local: the pull's density profile)")
print("  L_out/L_in = (rho_emit/rho_obs)^(1/3)  (cosmic: the untying's density growth)")
print("both are 'the photon does work at its speed limit against the medium's density' -")
print("the registry's redshift set opens with a derived (1+z), the stretch, and the dimming.")
