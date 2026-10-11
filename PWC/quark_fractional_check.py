# Do the fractional charges map onto the framework's own thirds? (2026-10-09)
import math
s = 1.0/19.0

print("== 1. The thirds are the framework's own ==")
print("P = rho H / 3        - the EOS carries the 1/3 (the three spatial dimensions)")
print("dY/d(dH) = -3Y/c0^2  - the tension-heat law carries the 3 (same three axes)")
print("the medium is 3-dimensional: every knot's tension projects onto three orthogonal axes.")

print("\n== 2. The colorless condition = the equilibrium ==")
v = [0.0, 120.0, 240.0]
sx = sum(math.cos(math.radians(a)) for a in v)
sy = sum(math.sin(math.radians(a)) for a in v)
print(f"three unit vectors at 120 degrees: sum = ({sx:.1e}, {sy:.1e}) = ZERO")
print(f"-> 'colorless' is the three cross-locks summing to zero: the knot holds. Same")
print(f"statement as the knot equilibrium (the pressures balance). The 120-degree")
print(f"separation = the three axes of P = rho H/3.")

print("\n== 3. The fractional charges = the winding over the three axes ==")
q = [2.0/3.0, 2.0/3.0, -1.0/3.0]   # uud
print(f"uud:  2/3 + 2/3 - 1/3 = {sum(q)}  (the proton's winding +1)")
q2 = [2.0/3.0, -1.0/3.0, -1.0/3.0]  # udd -> neutron
print(f"udd:  2/3 - 1/3 - 1/3 = {sum(q2)}  (the neutron's winding 0)")
print(f"-> the thirds ARE the framework's 1/3; two axes wind WITH the total, one winds")
print(f"   AGAINST. The 2/3 = 1 - 1/3: the winding minus one axis's counter-share.")

print("\n== 4. Confinement = you cannot extract a direction from a knot ==")
print("isolating one vector leaves an open wave - the fluid caps the open ends with a new")
print("slip-knot (the meson). The meson's own knot: the two broken ends re-tied at the")
print("caps, exactly the framework's slip-knot, not a 'new particle from the vacuum'.")

print("\n== 5. Honest gap ==")
print("the thirds are derived (the EOS); the DISTRIBUTION - why +2/3 on two axes and -1/3")
print("on the third - needs the braid's actual fold structure (the 4-wave crossing angles).")
print("That is the open braid-geometry question; the framework supplies the denominators,")
print("the numerators wait on the braid's crossing map.")
