# The -2.1% dilution gap: what deformation does the slip-knot need? (2026-10-09)
import math
e = 1.602176634e-19; eps0 = 8.8541878128e-12; c0 = 2.99792458e8
hbar = 1.054571817e-34; me = 9.1093837e-31
rho_max = 1.304e15
lamC = 2*math.pi*hbar/(me*c0); lamC_bar = hbar/(me*c0)
r_e = e**2/(4*math.pi*eps0*me*c0**2)
alpha = e**2/(4*math.pi*eps0*hbar*c0)

V_fold = 4*math.pi*r_e**3/3.0
V_tight = me/rho_max
print(f"V_fold = (4pi/3) r_e^3 = {V_fold:.4e} ;  V_tight = m_e/rho_max = {V_tight:.4e}")
print(f"idealized dilution = {V_fold/V_tight:.3f}  vs  1/alpha = {1/alpha:.3f}  "
      f"({100*(V_fold/V_tight/(1/alpha)-1):+.2f}%)")
V_needed = V_fold/ (1/alpha)
print(f"\nthe exact-1/alpha fold needs V_tight = {V_needed:.4e} -> interior packing "
      f"{V_tight/V_needed:.4f} x rho_max")
print(f"OR the fold radius must be {100*((V_tight*(1/alpha))/V_fold)**(1/3)-100:+.3f}% larger than r_e")
print(f"   -> r_fold = r_e x {((V_tight*(1/alpha))/V_fold)**(1/3):.5f} = "
      f"{r_e*((V_tight*(1/alpha))/V_fold)**(1/3)/1e-15:.4f} fm")
print(f"OR the shape factor is 4pi/(3 x {V_tight/V_needed:.4f})")

print("\n== candidate deformations ==")
# (2,1) torus knot: L = lamC with a tube r -> major radius shrinks -> LESS dilution
for r_t_fm in (1.0, 2.8, 10.0):
    r_t = r_t_fm*1e-15
    R_k = math.sqrt(lamC**2 - 4*math.pi**2*r_t**2)/(4*math.pi)
    V_k = 4*math.pi*R_k**3/3.0
    print(f"(2,1) knot with tube r_t = {r_t_fm:4.1f} fm: R = {R_k/1e-15:.1f} fm, "
          f"V/V_fold = {V_k/V_fold:.4f}  (dilution {V_k/V_tight:.1f})")
print("  -> the (2,1) knot SHRINKS the fold: wrong direction for MORE give. The twist is")
print("     not the answer unless it adds volume some other way (the Hopf twist's sweep).")

print("\n== the numbers near the 2.13% ==")
target = V_tight/V_needed
for name, val in [("sqrt(25/24)", math.sqrt(25/24.0)), ("neutron 2.5% (1.025)", 1.025),
                  ("20/19 stretch (1.0526)", 20/19.0), ("1 + s/2.47", 1+1/19/2.47)]:
    print(f"{name:24s} = {val:.5f}  vs {target:.5f}  ({100*(val/target-1):+.2f}%)")
print("\nverdict: the -2.1% is a SHAPE deformation: the fold must enclose 2.13% more volume")
print("than the perfect r_e-sphere. Candidates: the zitter sweep, the Hopf twist's pitch,")
print("the double-cover's overlap. None verified yet - the target is now a shape, not a number.")
