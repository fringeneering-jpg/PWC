# The medium law P(rho, s) - assembled from the locked pieces (2026-10-12)
import math
c0 = 2.99792458e8
rho0 = 8.74e-27; rho_max = 1.304e15
H0 = 32.371*c0**2
s = 1.0/19.0

print("== the pieces, all locked ==")
print("the caloric law:      H(rho) = H0 - (c0^2/3) ln(rho/rho0)   (the debt's measure)")
print("the debt ontology:    heat = the waves' own squeezed-out portion; negative pressure")
print("the fold's balance:   F_EM = F_debt + F_topology,  F_EM/F_debt = 1/s = 19 exact")
print("the knot equilibrium: H_trapped = s c0^2  (the retained debt per kg)\n")

print("== the assembly ==")
print("the waves' own pressure at density rho:  P_wave = rho c0^2 / 3   (the 3 dimensions)")
print("the debt's tension (the pull-back):      P_debt = s rho c0^2 / 3   (the stretch's share)")
print("the medium's total pressure:  P(rho, s) = P_wave - P_debt = (1 - s) rho c0^2 / 3")
print()
print("check at rest:  P(rho0) = (1-s) rho0 c0^2/3 = %.3e Pa" % ((1-s)*rho0*c0**2/3))
print("the locked pull-side tension: Y = s rho0 c0^2/3 = 1.378e-11 Pa (the heat's draw, the")
print("SEPARATE pull channel - so the net pressure + the tension read as the two-sided book:")
print("  net pressure  (1-s) rho c0^2/3   (the waves' push, net of the debt)")
print("  tension       s rho c0^2/3       (the debt's draw, the pull-side, negative by sign)")
print("sum: rho c0^2/3 - the waves' full pressure, split (1-s) push and s pull - the same")
print("19:1:18 family: the fold's balance is the medium law read at the knot.")

print("\n== the full law ==")
print("P(rho, s) = (1-s) rho c0^2/3   +   the caloric floor H(rho) as the heat reservoir")
print("with the coupling's density dependence: the grip stiffens x7 across the plateau")
print("(locked 6.9972), and the fold drops the tension with the heat (T7: 1.75% pull,")
print("98.25% heat). The law's boundary conditions: P(rho0) at rest, P_max = rho_max c0^2")
print("at the fold, and the knot equilibrium H_trapped = s c0^2 as the retained share.")

print("\n== the honest status ==")
print("the pressure law is now WRITTEN in the debt ontology's own terms: the waves' push")
print("minus the debt's draw, split by the stretch - (1-s) vs s, the 19:1:18 balance's")
print("own ratio appearing at every density. The registry's 'medium law P(rho,s)' item")
print("has its form; the plateau/fold refinements (the x7 and the T7 split) are the")
print("locked couplings already in the record. This closes the EOS's last named piece.")
