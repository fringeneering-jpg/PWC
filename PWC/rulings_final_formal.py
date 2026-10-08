# Formalization of the final two rulings (2026-10-08)
import math
c0 = 2.99792458e8
c0sq = c0**2
rho0 = 8.74e-27
rhomax = 1.304e15
s = 1.0/19.0

print("== RULING 1: pull-side sealed ==")
P_g = rho0*c0sq/3.0
Y_0 = s*rho0*c0sq/3.0
P_net = P_g - Y_0
print(f"resting net P_net = (1-s) rho0 c0^2/3 = {P_net:.4e} Pa (positive - the literal-negative")
print(f"branch is NOT selected; the pull side Y = s rho0 c0^2/3 = {Y_0:.4e} Pa IS the")
print(f"'negative pressure' = the draw of the heat (19:1 tug-of-war, the stretch datum).")
print(f"matter = the suction: each knot's heat deficit = m*c0^2 (the plateau heat); the drive")
print(f"for expansion = the knots untying back to the tensile web (T7: tension 1.75% trigger +")
print(f"heat draw 98.25%).")

print("\n== RULING 2: coupling law = grip as a function of the heat expelled ==")
print("chiral pair: opposites attract, likes repel -> stable tensioned distance; heat gives")
print("fluidity (weak grip), freezing gives stiff clumps (strong grip).")
print("Vacuum eps0/mu0 = the RESTING grip (the measured datum, like G).")
print("Heat-function shape: the keystone ramp's flat start (the m-family: dS/dln rho -> 0 at")
print("rest) - so the grip is FLAT through the gas branch to first order, and the stiffening")
print("engages on the ramp toward the fold, x7 across the plateau (locked 6.9972).")

print("\n== Reconciliation with row 23 (weak-field light-speed law assumed fixed k) ==")
# row 23: c = a*sqrt(k/m_w), k fixed -> c ~ rho^-1/3
# coupling ruling: k stiffens as heat leaves -> flat at rest (ramp flat start), so first order
# delta_k = 0 and row 23 survives; the stiffening is second order / ramp region only.
d_rho_rho = 2.12e-6                     # solar-limb compression (row 22)
# ramp correction at weak field: S ~ (rho/rho_g*)^m with rho_g* = rhomax/2 -> ~1e-41
print(f"at the solar limb (drho/rho = {d_rho_rho:.1e}), the ramp correction (rho/rho_g*)^m ~ "
      f"{(rho0*(1+d_rho_rho)/rhomax):.1e} -> the grip shift is ZERO to first order:")
print(f"  row 23's fixed-k stands (dc/c = -GM/(r c0^2) unchanged); the coupling ruling answers")
print(f"  row 23's open caveat 'why the links are harmonic' - the heat-function is flat at rest.")
print(f"At the fold/locked: the grip is maximal - the stiff clumps: P = rho_max c0^2, c_s = c0,")
print(f"x7 the fold grip (the keystone plateau factor) - the frozen state.")

print("\n== mu0 side ==")
hbar = 1.05457e-34
a0 = (hbar/(rho0*c0))**0.25
mw = rho0*a0**3/2.0
print(f"mu0 = the pair's inertia per link m_w/a: at rest {mw/a0:.3e} kg/m; under compression")
print(f"a shrinks as rho^-1/3 so mu0(rho) ~ rho^+1/3 - more inertia per length. With the flat")
print(f"grip, the local product gives c_loc/c0 = a/a0 = (rho/rho0)^-1/3 - exactly row 23.")
print(f"The vacuum eps0/mu0 remain the resting values of the heat-function; the charge scale")
print(f"(e, alpha) is the single numeric datum (the charge-dimension proof stands: the ruling")
print(f"supplies the FUNCTION, the vacuum value is the measured anchor).")
