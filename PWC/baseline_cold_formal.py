# Baseline-cold formalization (Jaden's 2026-10-08 ruling) - arithmetic on locked numbers
import math
c0 = 2.99792458e8
c0sq = c0**2
rho0 = 8.74e-27
rhomax = 1.304e15
s = 1.0/19.0

print("== 1. The tug-of-war at rest: push vs pull ==")
P_g = rho0*c0sq/3.0
Y_0 = s*rho0*c0sq/3.0
P_net = P_g - Y_0
print(f"push (rigidity) P_g(rho0) = rho0 c0^2/3 = {P_g:.4e} Pa")
print(f"pull (tension)   Y(rho0)   = s rho0 c0^2/3 = {Y_0:.4e} Pa   (s = 1/19)")
print(f"net P_net(rho0) = (1-s) rho0 c0^2/3 = {P_net:.4e} Pa  (> 0: the gas branch never")
print(f"goes negative under Y = s*rho*c0^2/3 - the 'negative pressure' is the PULL side,")
print(f"5.26% of the push; push:pull = 19:1, the same 1/19 as the stretch datum")
print(f"high/low sides: P_locked = {rhomax*c0sq:.3e} Pa vs P_net(rho0) = {P_net:.3e} Pa -")
print(f"a {math.log10(rhomax*c0sq/P_net):.1f}-decade pair, 'possibly to extremes', no tear")

print("\n== 2. Cold = the pull: the tension share of tying/untying ==")
print(f"tension work per kg: Y(rho0)/rho0 = s c0^2/3 = {s/3.0:.4f} c0^2 = "
      f"{100*s/3.0:.2f}% of the latent heat")
print(f"-> the pull supplies the DIRECTION (1.75% of the bill); the heat draw pays 98.25%.")
print(f"   'the negative pressure rips the knot open' = heat loosens, pull directs.")

print("\n== 3. The bath = the radiated exhaust (baseline T = 0) ==")
a_rad = 7.5657e-16
u_cmb = a_rad*2.7255**4
f_rad_freeze = u_cmb/(rho0*c0sq)          # bath per kg medium in plateau-c0^2 units
rho_m = (5.0/95.0)*rho0
f_rad_today  = u_cmb/(rho_m*c0sq)         # bath per kg of TODAY's matter
print(f"u_bath = {u_cmb:.4e} J/m^3")
print(f"cosmic escape fraction, freeze inventory (100% tied once): {f_rad_freeze:.3e}")
print(f"cosmic escape fraction, today's matter (5% tied):          {f_rad_today:.3e}")
print(f"RBH-1 wake measured escape fraction: 2.45e-4  (straddled by the two)")
print(f"-> all the 2.7 K can be booked as the RADIATED sample of tying exhaust;")
print(f"   the bulk is the spacer heat H0.  Baseline T = 0 needs no primordial bath.")

print("\n== 4. Local-exhaust prediction (falsifiable) ==")
print("Fresh tying sites (wakes, formation knots) must show a local excess ABOVE the")
print("2.725 K bath - unthermalized exhaust (RBH-1's [O III] flash is exactly this);")
print("the bath itself is smooth because it is the accumulated, thermalized ancient")
print("exhaust - consistent with CMB isotropy to 1e-5.")
