# The tension shadow balance: gravity = the push of the medium? Does g = 1.2067 fall out? (2026-10-12)
import math
c0 = 2.99792458e8
rho0 = 8.74e-27
H0 = 32.371*c0**2
P_amb = rho0*H0              # the baseline tension's pressure scale (the ambient push)
f_solid = 0.00085            # the universal 0.085% displacement fraction
G = 6.6743e-11
mp = 1.6726e-27; Rp = 8.414e-16
rho_p = mp/(4*math.pi*Rp**3/3.0)

print(f"P_ambient = rho0 H0 = {P_amb:.3e} Pa ;  f_solid = {f_solid}")
print(f"proton: rho = {rho_p:.2e} kg/m^3, R = {Rp:.3e} m\n")

print("== the shadow force ==")
# each knot's effective shadow cross-section = f_solid x pi R^2
# F = P x A_eff x (A_eff / 4 pi d^2)  - the shielded solid angle of the other knot
A_eff = f_solid*math.pi*Rp**2
F_over_d2 = P_amb*A_eff**2/(4*math.pi)      # F = (F_over_d2)/d^2
print(f"A_eff = {A_eff:.3e} m^2 ;  F = {F_over_d2:.3e} / d^2  N")
F_newton_d2 = G*mp**2
print(f"Newton: F = {F_newton_d2:.3e} / d^2  N")
print(f"ratio shadow/Newton = {F_over_d2/F_newton_d2:.3e}  ->  the ambient push is")
print(f"{F_newton_d2/F_over_d2:.1e}x too thin to be the force. The shadow mechanism at the")
print(f"AMBIENT tension fails the magnitude by 10 orders.")

print("\n== what ambient pressure WOULD make the shadow = Newton? ==")
P_need = G*mp**2*4*math.pi/A_eff**2
print(f"P_needed = {P_need:.3e} Pa  =  {P_need/P_amb:.1e} x the ambient  =  {P_need/(rho_max:=1.304e15*c0**2):.2e} of P_max")
print(f"-> the push must be the tension at the KNOT's own scale (the held shell), not the")
print(f"   ambient - the mechanism's magnitude lives at rho_max-grade, 26 billion x the baseline.")

print("\n== the geometric conversion factor: does any clean factor give 1.2067? ==")
g_target = 1.2067
cands = {
  "the shadow's solid-angle factor 1/(4 pi)": 1.0/(4*math.pi),
  "the 3D/2D sphere conversion (4/3)/(1)": 4.0/3.0,
  "9/(64 pi) (the full shadow-Newton prefactor)": 9.0/(64*math.pi),
  "16 pi^3 / 3 (the framework's g definition)": 16*math.pi**3/3.0,
  "4 pi^3 / 3": 4*math.pi**3/3.0,
}
for name, val in cands.items():
    print(f"  {name:46s} = {val:.4f}   (g_target/val = {g_target/val:.4f})")
print(f"\n-> none of the shadow's natural geometric factors is 1.2067. The target g =")
print(f"16 pi^3 alpha/3 = the alpha-dressed WvdM geometry, NOT the pressure-shadow")
print(f"conversion. The shadow balance gives gravity's SHAPE (F ~ 1/d^2, the push not the")
print(f"pull) but not its magnitude (26 billion x short at the ambient) and not g.")
print(f"\nhonest verdict: the mechanism is Jaden's ruling and the 1/d^2 shape is right - but")
print(f"the numbers say the push that makes gravity is the tension AT the knots' held")
print(f"shells (the compressed medium), not the baseline; and g = 1.2067 is the charge")
print(f"eigenfactor, not the shadow conversion. The stake remains unclaimed; the vampire's")
print(f"heart is the held-shell tension balance, a different equation than the one run.")
