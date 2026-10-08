# RBH-1 supply-cap check (arithmetic on sealed numbers; new-test OK from Jaden)
# Sealed: the cavitation zone is ZERO FLOW (PWC.md sec8 line 449-453: "fully clogged",
# medium "cannot follow... reroutes around it"); walls at rho_max; ambient medium at rho0.
# Question: how much new matter can the sealed mechanism actually supply to the wake?
import math

c0 = 2.998e8
rho_max = 1.304e15
rho0 = 8.74e-27
kpc = 3.0857e19
yr = 365.25*86400
Msun = 1.989e30

r = 0.7*kpc
L = 62*kpc
v_bh = 954e3
age = 73e6*yr

print("== Supply routes under the sealed zero-flow zone ==")
# 1. The zone's own mist inventory (rarefied medium in the cavity)
for f in (0.112, 0.95):
    M_zone = f*rho0*math.pi*r**2*L
    print(f"zone inventory at {f:.3f} rho0: {M_zone/Msun:.0f} Msun")
# 2. The cylinder swept by the hole through ambient rho0 medium
M_swept = rho0*math.pi*r**2*v_bh*age
print(f"ambient medium swept through the trail cross-section: {M_swept/Msun:.0f} Msun")
print(f"combined cap (inventory at 0.112 rho0 + swept): "
      f"{(0.112*rho0*math.pi*r**2*L + M_swept)/Msun:.0f} Msun")

print("\n== What the wake is observed to have formed ==")
for M in (1e6, 1e7):
    print(f"stars claimed (sec8 line 478): {M:.0e} Msun -> cap/supply ratio "
          f"{M_swept/Msun/M:.1e}-{M_swept/Msun/M/8:.1e} of what is needed")

print("\n== The flash is fine ==")
M_light = 245.0
print(f"flash light-equivalent 245 Msun vs zone inventory 1,232 Msun: inside the cap")

print("\n== What refill would need (if the zone is NOT zero-flow) ==")
mdot_stars = 1e6*Msun/age
A_side = 2*math.pi*r*L
for f in (0.112, 1.0):
    u = mdot_stars/(f*rho0*A_side)
    print(f"side inflow at {f:.3f} rho0: u = {u/1e3:.0f} km/s = {u/c0:.2e} c0 "
          f"(subsonic? {u < c0/math.sqrt(3)})")

print("\n== Dilution prediction for the frozen metallicity test ==")
for M in (1e6, 1e7):
    share = (0.112*rho0*math.pi*r**2*L + M_swept)/Msun / M
    print(f"new-hydrogen share of the stars at {M:.0e} Msun: {share:.2e} "
          f"(the frozen pass bar was |dilution| >= 0.10 dex = 20%)")

print("\n== Reading (corrected) ==")
print("Sealed: the swept ambient reroutes AROUND the core (side channels), so it does not enter the")
print("zone. The only in-zone supply is the mist inventory: ~1,232 Msun at 0.112 rho0, up to")
print("~11,700 Msun at 0.95 rho0. Even granting full capture of the swept cylinder (~14,155 Msun),")
print("the combined ceiling is ~15,500 Msun.")
print("The ~245 Msun flash sits inside any of these caps. The 1e6-1e7 Msun of stars exceed the")
print("zone-inventory cap by ~85-810x (or 65-650x with the swept cylinder granted).")
print("Steady star formation over 73 Myr requires refilling the zone at ~1e21 kg/s; under the sealed")
print("'zero flow' clause there is no supply route for that. Resolution paths (Jaden's ruling):")
print("(a) the stars are swept ambient gas and the PWC admixture is the cap-sized hydrogen fraction")
print("(dilution between ~1e-4 and ~1.5e-2 of the stars, far below the frozen -0.10 dex pass bar);")
print("(b) the zone is refilled at 380-3,400 km/s (contradicts 'zero flow', needs a mechanism);")
print("(c) the local medium around RBH-1 is ~1e3 rho0 (needs the galaxy-scale medium profile).")
