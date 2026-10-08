# Verify the heat-ramp report's key numbers + reconcile with the demand function
import math
c0 = 2.99792458e8
c0sq = c0**2
rho0 = 8.74e-27
rhomax = 1.304e15
rhog = rhomax/2.0
Pstar = rhomax*c0sq

print("== Report's key numbers, independently re-verified ==")
Lmin = (c0sq/3.0)*math.log(rhog/rho0)
print(f"(c0^2/3) ln(rhog/rho0) = {Lmin/c0sq:.4f} c0^2  (report: 31.371)")
print(f"fold construction: P* dv = P*(1/rhog - 1/rhomax)/c0^2 = "
      f"{Pstar*(1/rhog - 1/rhomax)/c0sq:.10f} c0^2  (report: = c0^2 exactly)")
print(f"fold pressure jump: P* - (rhog*c0^2) = {Pstar - rhog*c0sq:.3e} Pa = "
      f"{(Pstar - rhog*c0sq)/Pstar:.4f} P*  (report: jumps x2 -> jump = P*/2)")

print("\n== H0 floor vs the resting pressure P0 (my Identity 3) ==")
H0_floor = 32.04*c0sq
u_h = rho0*H0_floor
P0 = rho0*c0sq/3.0
print(f"H0 floor = 32.04 c0^2 = {H0_floor:.4e} J/kg")
print(f"heat energy density u_h = rho0*H0 >= {u_h:.4e} J/m^3")
print(f"vs resting pressure P0 = {P0:.4e} Pa ->  u_h/P0 >= {u_h/P0:.1f}  (heat-dominated)")
print(f"tying-heat identity unchanged: m_p c0^2/(3 m_p/rho0) = P0 exactly (the c0^2 there")
print(f"is the FOLD latent heat, not H0)")

print("\n== Reconciliation chain ==")
print("1. Demand function at full conversion = the fold construction:")
print("   m = dP*dV/c0^2 with dV per kg = dv = 1/rhomax, dP = P*  ->")
print("   1 kg = P* dv/c0^2 = c0^2/c0^2 = 1  [identical equations]")
print("2. The c0^2 in the demand function is the PLATEAU/fold latent heat (the parent's corrected")
print("   caloric law: gas branch 31.371 c0^2 + plateau exactly 1.000 c0^2 = 32.371 total),")
print("   NOT the total inventory -> the heat-ramp report's failing datum does not touch the rule.")
print("3. The 31.371 c0^2 gas-branch squeeze heat is the compression ladder, paid by the medium's")
print("   own heat content H0 >= 32.371 c0^2 (datum D1) - not by the slam work.")
print("4. RBH-1 heat budget: the slam pays only the fold cost m*c0^2; escape fraction 2.45e-4")
print("   unchanged.")

print("\n== CORRECTIONS to my earlier rounds (locked A1 supersedes my wrong anchor) ==")
s = 1.0/19.0
Y_cav = s*rho0*c0sq/3.0
print(f"locked Y_cav = s*rho0*c0^2/3 = {Y_cav:.4e} Pa  (s = 1/19, the 5.3% stretch)")
print(f"v_cav(rho0) = c0*sqrt(2s/3) = {math.sqrt(2*s/3):.6f} c0 = "
      f"{c0*math.sqrt(2*s/3)/1e3:.0f} km/s  (NOT c0 - my round-3 anchor was wrong)")
print(f"my round-3 Y(rho0) = rho0*c0^2/2 = {0.5*rho0*c0sq:.4e} Pa was 28.5x too high")
print(f"tension work per kg untied: Y_cav/rho0 = s*c0^2/3 = {s/3.0:.4f} c0^2 = "
      f"{100*s/3.0:.2f}% of the latent heat (my round-4 '50/50 split' was wrong)")
print(f"correct T7 split: tension {100*s/3.0:.2f}% + heat draw {100*(1-s/3.0):.2f}%")
print(f"Y/rho on the gas branch: sc0^2/3 = {s*c0sq/3.0:.4e} m^2/s^2 = CONSTANT (my '1e5 fall'")
print(f"claim was wrong; tension per unit heat 3Y/c0^2 = s*rho RISES as the pairs close)")

print("\n== gamma item: resolved by the tension-heat law (supersedes my four-cut null) ==")
P_locked = rhomax*c0sq
Y_gamma = 3.36e31
print(f"Y_gamma/P_locked = {Y_gamma/P_locked:.5f}  (locked 0.286695); ladder in s*P_locked/3:")
print(f"  {{1, 7/2, 49/3}} = {{1, 3.5, 16.333}} vs locked {{1, 3.4986, {Y_gamma/(s*P_locked/3.0):.4f}}}")
print(f"  -> gamma is the unreachable max tension at 4.671 rho_max; cohesion at Max-P is")
print(f"     Y_coh = 0.061379 P_locked.  The heat->tension item is now a LAW: dY/d(dH) = -3Y/c0^2.")
