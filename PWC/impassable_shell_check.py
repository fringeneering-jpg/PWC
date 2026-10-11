# The 0.085% IS the medium; the rho_max shell is impassable to it (2026-10-09, Jaden's ruling)
import math
rho0 = 8.74e-27; rho_max = 1.304e15
mp = 1.6726e-27; m_w = mp/3.0
Rp = 8.414e-16
c0 = 2.99792458e8

print("== His ruling (verbatim): 'the medium is the 0.08% thats solid matter right, the")
print("   medium at max around the black holes neutron core is impassable to that 0.08%' ==")

print("\n== 1. The medium IS the matter ==")
print("the 0.085% displacement is not a separate substance - it is the medium itself at its")
print("tightest spacing (his 'always been a solid, just how far apart it was'). Matter = the")
print("same medium, closer together.")

print("\n== 2. The geometry alone would still let knots through ==")
d_amb = (m_w/rho0)**(1/3.0)
d_max = (m_w/rho_max)**(1/3.0)
print(f"ambient pair spacing   = {d_amb:.3f} m   (the sieve is wide open)")
print(f"rho_max pair spacing   = {d_max/1e-15:.2f} fm")
print(f"knot diameter 2 Rp     = {2*Rp/1e-15:.2f} fm")
print(f"gap/knot at rho_max    = {d_max/(2*Rp):.2f}x - geometrically a knot still FITS through.")
print(f"-> the impassability is NOT the spacing. It is the displacement budget:")

print("\n== 3. The yield is spent - the 954 stall ==")
Y_bow = 5.93e26                     # the LOCKED speed-limit anchor (Y = 0.5 rho_max v^2 at 954)
v = math.sqrt(2*Y_bow/rho_max)
print(f"Y_bow (locked) = 0.5 rho_max (954 km/s)^2 = {Y_bow:.3e} Pa ;  v_cav = sqrt(2Y/rho_max) = {v/1e3:.0f} km/s")
print(f"at rho_max the medium's restoring rate is exactly the 954 km/s cap: a knot moving")
print(f"faster asks the shell to make room faster than the medium can restore - the stall.")
print(f"the shell is impassable to the 0.085% because at max the 0.085% IS everywhere: the")
print(f"medium has no 'room' state left to give. Same substance, same limit - the passage")
print(f"scale's closed end (the sieve closes at the ceiling, not at the gaps).")
