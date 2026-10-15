# The volume-to-mass friction scale: black-hole Max-P = RCP 28's dropped medium
import math
c0 = 2.998e8
rho_max = 1.304e15
rho_core = 2.3e17
rho0 = 8.74e-27
Y = 5.93e26
Msun = 1.989e30

print("== The identity ==")
Vm_max = 1.0/rho_max
print(f"black-hole Max-P and the RCP 28 runaway's dropped medium: same V/M = 1/rho_max = "
      f"{Vm_max:.4e} m^3/kg  (the 10-05 chat's own 'shed volume' 4.57e15 m^3 for 3 Msun = "
      f"{3*Msun/rho_max:.3e} m^3 - identical)")

print("\n== The friction law: v_cap^2 = 2Y * (V/M)  [held bodies] ==")
for rho, lab in [(1.32e10, "crossover to c0"), (1e11, "white-dwarf class"),
                 (1e13, ""), (rho_max, "Max-P (RCP 28 wall)"), (rho_core, "neutron core")]:
    v = math.sqrt(2*Y/rho)
    print(f"  rho = {rho:.3e} ({lab}): v_cap = {v/1e3:,.0f} km/s = {v/c0:.4f} c0")

print("\n== The wave (free): V/M grows at c0, no friction ==")
M3 = 3*Msun
R0 = (3*M3/(4*math.pi*rho_max))**(1/3)
tau = 4.68e-3
n = c0*tau/R0
Vm_tau = (n**3)/rho_max
v_held = math.sqrt(2*Y*Vm_tau)
print(f"the difference (3 Msun) at Max-P = a {R0/1e3:.0f} km ball; the ringdown starts the release")
print(f"at c0 for tau = 4.68 ms: front = {c0*tau/1e3:.0f} km = {n:.1f}x R0; V/M grows to "
      f"{Vm_tau:.3e} m^3/kg ({n**3:,.0f}x decompressed)")
print(f"if that V/M were HELD, its friction cap would be {v_held/1e3:,.0f} km/s = {v_held/c0:.3f} c0")
print(f"-> it rides c0 anyway because it is FREE: the wave is the medium's own mode; friction")
print(f"only bites the HELD state.  Same substance, same V/M at release, two modes, two speeds.")

print("\n== The runaway's cap ignition (passage chart 2026-10-08) ==")
print(f"1/2 rho_max v^2 = Y at v = sqrt(2Y/rho_max) = {math.sqrt(2*Y/rho_max)/1e3:.0f} km/s:")
print(f"the RCP 28 hole moves AT its friction cap - the Max-P cannot flow through itself, so the")
print(f"cap is rebuilt ahead and DROPPED behind (the wake) at that speed. The wave (merger dump)")
print(f"has no wall to rebuild, so c0.  One V/M, two fates: held -> 954, free -> c0.")
