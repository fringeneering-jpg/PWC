# The interior tension profile: does G fall out of the collective shell? (2026-10-12)
import math
G = 6.6743e-11; c0 = 2.99792458e8
rho0 = 8.74e-27; rho_max = 1.304e15
H0 = 32.371*c0**2
s = 1.0/19.0
a_max = 3.23e11
mp = 1.6726e-27

print("== 1. The profile: rho(r) = rho0 exp(3GM/(r c0^2)) - the pull compressing the medium ==")
print("compression factor 3GM/(r c0^2) at each scale:\n")
for name, M, r in [("lone proton (the unphysical case)", mp, 8.4e-16),
                   ("an iron nucleus (A=56)", 9.4e-26, 4.0e-15),
                   ("a carbon atom", 2.0e-26, 7.0e-11),
                   ("a person-scale body", 70.0, 0.5),
                   ("the Earth", 5.97e24, 6.37e6),
                   ("a galaxy's inner region", 1e41, 3.0e19)]:
    f = 3*G*M/(r*c0**2)
    print(f"  {name:32s} M = {M:.2e} kg, r = {r:.2e} m  ->  3GM/(rc0^2) = {f:.2e}")

print("\n-> the gravitational compression is EMPTY (1e-38 to 1e-9) at every scale below")
print("   the astronomical. The knots' own pull compresses nothing - Jaden's survival-triad")
print("   point, made arithmetic: the lone knot has no shell, and even the atom's collective")
print("   pull is 1e-37-level. The interior tension from gravity does not exist sub-")
print("   astronomically.")

print("\n== 2. Where the profile is NON-trivial ==")
# the astronomical scale: the galaxy / the BH - the framework's actual gravity carrier
M_bh = 2.0e7*1.989e30
r_skin = math.sqrt(G*M_bh/a_max)
f_skin = 3*G*M_bh/(r_skin*c0**2)
print(f"RBH-1: r_skin = {r_skin/1e3:.0f} km ; compression at the skin = {f_skin:.2e}")
print(f"-> the held medium is REAL only at the BH/galaxy scale - where the framework's")
print(f"   gravity lives (the shared tension, the thin skin, the surface-area law).")

print("\n== 3. The consequence for the G-derivation ==")
print("the particle-scale G cannot come from the knots' own held medium - the profile is")
print("empty (1e-38). The particle-scale gravity must BE the coupling itself:")
print("  g = 20^(1/16) = 1.2059  (the 16-stage loop's stage factor, derived)")
print("  G = g x (the dimension-carrying constants)  =  c0^2/(rho_max R_p lamC) x f")
print(f"  -> the needed dimensionless factor f = {G*rho_max*8.4e-16*2.426e-12/c0**2:.2e}")
print(f"  candidates: (m_p/M_Pl)^2 = {(mp/2.176e-8)**2:.2e}  (3x off - reported, not claimed)")
print("  -> the coupling route's dimensional completion is the NAMED remaining piece:")
print("     f = 1.97e-39 must come from the framework's locked set, and no combination")
print("     has produced it yet. The profile run confirms: gravity is the coupling,")
print("     not the compression - and the last dimensionless factor is the grail's")
print("     final named gap.")
