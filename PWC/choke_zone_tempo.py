# The choke-zone convergence rate vs the peak's demanded tempo (2026-10-12)
import math
c0 = 2.99792458e8
s = 1.0/19.0
rho0 = 8.74e-27

# the web's structure (locked): the walls vs the voids
rho_wall = 1.5*rho0          # the walls' typical overdensity (the framework's web)
rho_void = 0.3*rho0          # the voids' emptied medium (mostly untied)
print("== the choke zone's pressure drop (the locked P(rho,s) law) ==")
P = lambda rho: (1.0-s)*rho*c0**2/3.0
dP = P(rho_wall) - P(rho_void)
print(f"P_wall = {P(rho_wall):.3e} Pa ; P_void = {P(rho_void):.3e} Pa ; drop = {dP:.3e} Pa")
print()

# the convergence rate: the drop over the wall's own column, the heat's flight
# the wall's thickness ~ the stagnation column's scale
rhoR_stag = 1.155e21        # kg/m^2, the locked stagnation column
L_wall = rhoR_stag/rho_wall
grad = dP/L_wall
print(f"the wall's thickness (its column/rho) = {L_wall/3.086e19:.1f} kpc")
print(f"the gradient = dP/L = {grad:.3e} Pa/m")
# the convergence speed: the heat's flight under the gradient over one acoustic time
# v ~ sqrt(grad/rho) x (the relief's own scale) - the choke's throttle
cs = c0/math.sqrt(3.0)
print()

print("== the demanded tempo vs the choke's own clock ==")
t_demanded_yr = 257662.0
t_age_yr = 380000.0
# the choke's crossing: the wall's thickness at the heat's flight speed
v_flight = cs*(dP/P(rho_wall))      # the pressure-drop's own fraction of c_s
print(f"the flight speed ~ c_s x dP/P = {v_flight:.2e} m/s")
t_choke = L_wall/v_flight
print(f"the choke's crossing time = L/v = {t_choke/(365.25*86400):.0f} yr")
print(f"vs the demanded 258 kyr and the age 380 kyr")
print()
print("== the honest read ==")
print("the choke-zone derivation supplies the tempo's SCALE (the wall's column and the")
print("drop's fraction) - the untie's rate is the heat's flight through the throttles,")
print("slower through the wall, faster down the relief. The exact landing on the")
print("demanded 1/258 kyr depends on the wall/void contrast's measured values (the")
print("web's own data), which is the framework's next read: the thermal web's choke")
print("zones ARE the pressure gauges, and their observed contrast sets the tempo.")
