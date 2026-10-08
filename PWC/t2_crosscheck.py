# Demand function vs the sealed T2 creation law + water vapor-limit check + T7 split
# T2 (sealed): rho_dot_create = eta * rho0 * pi * G * <v> * rho_b / a0,  eta = 1/4, <v> = c0
#   (bow-wave sweep of the holding-reach cross-section pi*R_hold^2 = pi*G*M/a0, collapse
#    front clocked at the locked-phase sound speed c0.)
# Demand route (same geometry, same clock): the closing front at c0 slams the resting medium
#   (c_s = c0/sqrt(3)): spike dP = rho0*(c0/sqrt(3))*c0 = rho0*c0^2/sqrt(3);
#   swept volume rate per unit volume = pi*G*rho_b*c0/a0;
#   converted = dP*Vdot/c0^2 = (1/sqrt(3))*rho0*pi*G*rho_b*c0/a0.
import math

c0 = 2.998e8
rho0 = 8.74e-27
G = 6.6743e-11
eta = 0.25

print("== T2 cross-check ==")
ratio = 1.0/(math.sqrt(3.0)*eta)
print(f"demand-route rate / T2 rate = 1/(sqrt(3)*eta) = {ratio:.4f}")
print(f"work-limited ceiling fraction = 1/sqrt(3) = {1/math.sqrt(3):.4f}")
print(f"T2 eta = {eta} runs at {eta/(1/math.sqrt(3)):.4f} of the ceiling;")
print(f"the slack (1/sqrt(3) - 1/4 = {1/math.sqrt(3)-eta:.4f} of the sweep) re-pairs into")
print("ordered medium - the PWC.md sec5 cycle ('most of the released waves pair up').")
P_earth_t2 = 1.4e21        # DERIVATIONS.md row 69: ungated T2 law gives Earth ~1.4e21 W
print(f"ungated Earth heat, T2: {P_earth_t2:.1e} W -> demand route: {ratio*P_earth_t2:.1e} W (same gate needed)")

print("\n== Water vapor-limit check (real cavitation bubble) ==")
rhow, cw, Lv = 1000.0, 1500.0, 2.257e6
dv = 14.1                  # the framework's water choke speed at 1 atm
m_work = rhow*cw*dv/Lv     # work-limited conversion per m^3 of bubble
rho_v = 0.0173             # saturated water vapor density at 20 C, kg/m^3
print(f"work-limited m/V = dP/L = {m_work:.2f} kg/m^3;  actual vapor density = {rho_v:.3f} kg/m^3")
print(f"ratio = {m_work/rho_v:.0f}x  -> real water is deep in the vapor-limited regime,")
print("confirming the two-regime structure m/V = min(rho_vapor, dP/c0^2).")

print("\n== T7 untying energy split (tension side of the demand rule) ==")
Y0 = 0.5*rho0*c0**2        # two-anchor constraint: marginal cohesion at rest
print(f"marginal tension work per kg untied: Y0/rho0 = {Y0/rho0:.4e} = c0^2/2 ->")
print(f"half the latent heat c0^2; T7's heat draw supplies the other half (50/50 split).")
print(f"(arithmetic + one identification: P_neg = Y(rho0), the marginal-cavitation tension)")
