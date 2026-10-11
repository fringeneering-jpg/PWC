# Dislocation core geometry: what shape produces the 1.0213 volume multiplier? (2026-10-09)
import math
e = 1.602176634e-19; eps0 = 8.8541878128e-12; c0 = 2.99792458e8
hbar = 1.054571817e-34; me = 9.1093837e-31
alpha = e**2/(4*math.pi*eps0*hbar*c0)
r_e = e**2/(4*math.pi*eps0*me*c0**2)
lamC_bar = hbar/(me*c0)
R_p = 8.414e-16

target = 1.02132
print(f"target volume multiplier = {target:.5f}")

# 1. Elliptic core from the classic b/4 core displacement: semi-axis a = r0 + b/4
#    equal-area ellipse -> bounding multiplier = (1 + b/(4 r0))^(3/2)
b_over_r0_needed = 4.0*(target**(2.0/3.0) - 1.0)
b_needed = b_over_r0_needed*r_e
print(f"\n1. Elliptic core (classic b/4 displacement):")
print(f"   needed b/r0 = {b_over_r0_needed:.5f}  ->  b = {b_needed/1e-15:.4f} fm")
print(f"   b/lamC_bar = {b_needed/lamC_bar:.3e} ;  b/R_p = {b_needed/R_p:.4f} ;  b/r_e = {b_over_r0_needed/4:.4f}")

# 2. The core-constant reading: E_tot = (mu b^2/4pi)[ln(R/r0) + C]
ln_term = math.log(1/alpha)
C_target = (target - 1.0)*ln_term
print(f"\n2. Core-constant reading: ln(1/alpha) = {ln_term:.4f}")
print(f"   the 2.13% as a core constant: C = 0.02132 x 4.921 = {C_target:.4f}")
print(f"   standard uniform-core C ~ 0.5-1.0 -> the wave's core is {0.5/C_target:.1f}-{1.0/C_target:.1f}x")
print(f"   softer/more spread than a uniform core (the slip-knot's looseness, directionally right)")

# 3. Candidate Burgers vectors from the locked set vs b_needed
print(f"\n3. What is b = {b_needed/1e-15:.4f} fm?  Candidates:")
for name, b in [("r_e/17.67", r_e/17.67), ("8 alpha r_e (ad hoc 8)", 8*alpha*r_e),
                ("R_p/5.28", R_p/5.28), ("alpha^2 lamC_bar", alpha**2*lamC_bar),
                ("4 alpha r_e", 4*alpha*r_e), ("lamC_bar/2421", lamC_bar/2421)]:
    print(f"   {name:22s} = {b/1e-15:.4f} fm  ({100*(b/b_needed-1):+.2f}%)")
print(f"\n   nearest clean: 8 alpha r_e = 8 alpha^2 lamC_bar = {8*alpha*r_e/1e-15:.4f} fm ({100*(8*alpha*r_e/b_needed-1):+.2f}%)")
print(f"   - the '8' is not locked; reported, not claimed.")

print(f"\n4. The pinned equation:")
print(f"   core displacement b/4 model:  (1 + b/(4 r0))^(3/2) = 1.02132  ->  b = 0.0566 r0 = 0.1595 fm")
print(f"   OR the core profile whose core constant C = 0.1048.  Both are now computable targets")
print(f"   for the wave's own transverse profile - the next input is the standing wave's core shape.")
