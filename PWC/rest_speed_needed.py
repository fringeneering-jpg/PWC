# The stationary medium: the drag is directionless, and what the rest speed WOULD need to be
import math
rho0 = 8.74e-27
A = 8050.0; m = 3.0e8
a_obs = 4.92e-6

print("== 1. The stationary-medium correction ==")
v_dipole = 370.0e3
a_drag = 0.5*rho0*v_dipole**2*A/m        # full capture, upper bound
print(f"the solar system moves through the STATIONARY medium at 370 km/s; the drag is")
print(f"~ 0.5 rho0 (370 km/s)^2 A / m = {a_drag:.2e} m/s^2 in EVERY direction (anti-dipole),")
print(f"no sunward/anti-sunward split. vs the observed 4.9e-6: short by {a_obs/a_drag:.0e}x.")

print("\n== 2. What would the rest speed have to be? ==")
v_need_full = math.sqrt(2*a_obs*m/(rho0*A))
print(f"at FULL capture: v_rest = sqrt(2 a m / rho0 A) = {v_need_full:.2e} m/s = {v_need_full/2.998e8:.0e} c0")
print(f"-> 20,000 times the speed of light. No rest speed fixes the magnitude.")

print("\n== 3. Or what density would the ambient need? ==")
rho_need = 2*a_obs*m/(v_dipole**2*A)
print(f"at 370 km/s, full capture: rho0_needed = {rho_need:.2e} kg/m^3 = {rho_need/rho0:.0e}x the locked rho0")
print(f"-> 1e15 times the locked ambient density (the near-Sun medium would have to be")
print(f"rho_max-grade: {rho_need/1.304e15:.2e} of rho_max). The medium's rest frame is fine;")
print(f"the drag's thinness is the density, not the frame. The observed 4.9e-6 anti-sunward")
print(f"r^-2 residual is not the medium's drag at ANY rest speed the framework allows - and")
print(f"the framework should say so plainly: 'Oumuamua's anomaly is not ours to explain yet.")
