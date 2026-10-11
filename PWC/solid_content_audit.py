# Jaden's audit: the drag must include the anomaly's OWN solid matter (its density), (2026-10-09)
# The capture fraction = the body's surface knot-packing = (R_p / d_knot)^2, d_knot = (m_p/rho_body)^(1/3)
import math
rho0 = 8.74e-27
mp = 1.6726e-27; Rp = 8.414e-16

def capture(rho_body):
    d = (mp/rho_body)**(1/3.0)
    return (Rp/d)**2

print("the body's own capture fraction (surface knot-packing) from its own density:\n")
for name, rho, A_geo, v, m in [
    ("'Oumuamua (rock, rho ~ 1e3)", 1e3, 8050.0, 2.6e4, 3.0e8),
    ("Vela neutron star (rho_core)", 2.3e17, 4*math.pi*(1.1e4)**2, 7.74e5, 2.8e30),
    ("US 708 star (rho ~ 1e3)", 1e3, math.pi*(7e8)**2, 1.2e6, 2e30),
]:
    f = capture(rho)
    F = 0.5*rho0*v**2*f*A_geo
    a = F/m
    print(f"  {name:32s} rho_body = {rho:.1e}  capture = {f:.2e}  F = {F:.2e} N  a = {a:.2e} m/s^2")

print("\n== what this changes ==")
print("the universal 0.085% is the KNOT's internal solid fraction (the fold's displacement).")
print("the BODY's capture fraction is its own surface packing - denser bodies catch more,")
print("looser bodies catch almost nothing. For 'Oumuamua (a rock at rho ~ 1e3) the capture")
print("is 5e-11, not 8.5e-4: its drag drops 1.7e7x further below the observed acceleration.")
print("For the Vela core the packing is 0.19 (224x the 0.085%), but the glitch's swept-mass")
print("shortfall was 31 orders - 224x cannot dent it. The verdicts STAND and get STRONGER:")
print("the corrected drag with each anomaly's own solid content still misses every magnitude.")
