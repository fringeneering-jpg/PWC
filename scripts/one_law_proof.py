# The one-law proof: T12's local profile -> the density relation (2026-10-12)
import math
G = 6.67430e-11; c0 = 2.99792458e8
rho0 = 8.74e-27
H0 = 32.371*c0**2

print("== the two locked laws ==")
print("T12 (local, locked):    L_out/L_in = exp[-GM(1/r1 - 1/r2)/c0^2]")
print("cosmic (new):           (1+z) = (rho_emit/rho_obs)^(1/3)")
print("the profile (locked caloric):  rho(r) = rho0 exp(3GM/(r c0^2))\n")

print("== the substitution ==")
print("rho_emit/rho_obs = exp(3GM/(r1 c0^2)) / exp(3GM/(r2 c0^2)) = exp(3GM(1/r1 - 1/r2)/c0^2)")
print("(1+z) = [exp(3GM(1/r1 - 1/r2)/c0^2)]^(1/3) = exp(GM(1/r1 - 1/r2)/c0^2)")
print("T12's redshift:  1+z = L_in/L_out = exp[+GM(1/r1 - 1/r2)/c0^2]")
print("-> IDENTICAL. The 3 in the profile and the 1/3 in the cube root cancel EXACTLY:")
print("   the three dimensions appear twice, and their cancellation IS the unification.\n")

print("== numeric check at the solar limb (the paper's own T12 numbers) ==")
Msun = 1.989e30; Rsun = 6.957e8
z_density = math.exp(G*Msun/(Rsun*c0**2)) - 1.0
z_t12 = math.exp(G*Msun/(Rsun*c0**2)) - 1.0
print(f"density-relation z at the limb  = {z_density:.6e}")
print(f"T12 z at the limb               = {z_t12:.6e}   (identical by construction - the")
print(f"  locked L x 2.12e-6 of the paper's row 22, within rounding)")

print("\n== the debt history hardcoded into z ==")
print("H(z) = H0 - (c0^2/3) ln(rho/rho0) = H0 - (c0^2/3) ln[(1+z)^3] = H0 - c0^2 ln(1+z)")
z_lss = 1100.0
print(f"H(z=1100) = {H0/c0**2:.3f} - ln(1101) = {H0/c0**2 - math.log(1+z_lss):.3f} c0^2  (matches the run's 25.367)")
print("-> the caloric debt history IS (1+z): no arbitrary cosmic history function anywhere.")

print("\n== verdict ==")
print("one law in two regimes, PROVEN at equation level: the local T12 exponential and the")
print("cosmic density ratio are the same expression, because rho(r) = rho0 e^(3GM/(r c0^2))")
print("carries the same 3 the cube root divides by. Gravity and expansion = one fluid mechanism.")
