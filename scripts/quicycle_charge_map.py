# Williamson quicycle charge -> PWC mapping (2026-10-08, Jaden's directive)
import math
eps0 = 8.8541878128e-12
h = 6.62607015e-34
hbar = 1.054571817e-34
c0 = 2.99792458e8
e = 1.602176634e-19
me = 9.1093837e-31

print("== 1. The WvdM idealized charge (verified) ==")
qp = math.sqrt(3*eps0*h*c0/(8*math.pi**3))
print(f"q' = sqrt(3 eps0 h c / (8 pi^3)) = {qp:.6e} C = {qp/e:.4f} e   (paper: 1.4585e-19 = 0.91e)")
print(f"KEY: the wavelength cancels -> charge is TOPOLOGICAL, independent of the knot's mass")
print(f"and energy. q^2 = (3/8 pi^3) * eps0 * h * c - only eps0, h, c.")

print("\n== 2. The 9% gap = the geometric eigenmode factor ==")
g = (e/qp)**2
print(f"g = (e/q')^2 = {g:.4f} ;  16 pi^3 alpha / 3 = {16*math.pi**3*(e**2/(4*math.pi*eps0*hbar*c0))/3:.4f}")
print(f"-> the idealized geometry gives 0.91e; the exact harmonic eigenmode supplies g = 1.208")
print(f"(Quicycle claims 1 ppm on this number, forthcoming).")

print("\n== 3. The PWC mapping ==")
print("a) CHARGE = WINDING: the 720-degree double loop winds twice; the winding number is +-1")
print("   for EVERY knot -> protons and electrons carry exactly equal-opposite charge because")
print("   charge is topology, not mass. This closes the proton/electron charge identity.")
print("b) THE DATUM COLLAPSES: q^2 = (3/8 pi^3) eps0 h c -> the charge scale and eps0 are ONE")
print("   datum (the resting grip, the coupling-law ruling). {e, alpha} shrinks to eps0 alone,")
print("   and alpha = the geometric eigenfactor g = 16 pi^3 alpha / 3 = 1.208 - a derived number.")
print("c) THE 9% DEFICIT = THE LINEAR GRIP: the 0.91e result integrates the field energy with")
print("   the RESTING (linear) eps0. At the knot's core the heat is expelled - the grip stiffens")
print("   (the coupling-law ruling) - the same physics Lai 2026 calls 'vacuum saturation' via the")
print("   Born-Infeld/Schwinger limit. Same mechanism, his vocabulary: E_S = me^2 c^3/(e hbar) =")
print(f"   {me**2*c0**3/(e*hbar):.3e} V/m is where the medium's grip saturates.")
print(f"   Lai: linear vacuum alpha^-1 = 150 (0.91e); saturated = 135.9 (0.99e); observed 137.036")
print(f"   (1.00e) - the 'topology gap' between the cylindrical and toroidal limits.")
print("d) CHIRALITY RULING GETS ITS CHARGE: opposite chiralities = opposite windings = +- charge;")
print("   'opposites attract, likes repel' = the Coulomb signs from the winding orientation.")
print("e) WHAT REMAINS: derive g = 1.2069 in PWC's own terms - the exact harmonic eigenmode of")
print("   the double loop with the heat-function's core stiffening (the coupling law), not the")
print("   resting eps0. That is the last 9% of the charge.")
