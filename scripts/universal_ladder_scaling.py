# The universal speed ladder, corrected: ONE formula, no branches (2026-10-09)
# v_max(rho) = min(c0, sqrt(2 Y_bow / rho))  - the single 1/sqrt(rho) law capped at c0
import math
c0 = 2.99792458e8
rho0 = 8.74e-27; rho_max = 1.304e15; rho_core = 2.3e17
Y_bow = 5.93e26          # the ONE yield: 0.5 rho_max (954 km/s)^2

def v_max(rho):
    return min(c0, math.sqrt(2*Y_bow/rho))

rho_crit = 2*Y_bow/c0**2
print(f"the single law: v_max(rho) = min(c0, sqrt(2 Y_bow / rho)),  Y_bow = 5.93e26 Pa\n")
print(f"the c0 cap engages below rho = 2 Y_bow/c0^2 = {rho_crit:.3e} kg/m^3 "
      f"(the locked ladder's first anchor 1.32e10)\n")
print(f"{'STATE':42s} {'density':>16s} {'its C':>18s}")
print("-" * 80)
print(f"{'PHOTON / the wave (the medium itself)':42s} {'~ rho0':>16s} {'c0 = 299,792 km/s':>18s}")
print(f"{'NEUTRINO (minimal knot)':42s} {'< 1.32e10':>16s} {'c0(1 - 1e-9)':>18s}")
print(f"{'the c0 cap (ladder anchor)':42s} {'1.32e10':>16s} {'0.9998 c0':>18s}")
for rho, name, lab in [(1e11, "ladder anchor", "0.363 c0"), (1e13, "ladder anchor", "0.0363 c0"),
                       (rho_max, "MAX-P (the shell)", "954 km/s"), (rho_core, "BARE NEUTRON (the core)", "72 km/s")]:
    v = v_max(rho)
    print(f"{name:42s} {rho:>16.3e} {v/1e3:>12,.0f} km/s = {v/c0:.5f} c0  (locked: {lab})")
print("\n== the runaway SMBH's rung ==")
print(f"RBH-1 at 950 km/s on the rho_max rung: {950/954:.3f} of its C - the fastest SMBH")
print(f"observed sits at 99.6% of its own maximum.")
print("\n== the reading ==")
print("EVERYTHING has a max speed - its own C - and every C is ONE formula: the 1/sqrt(rho)")
print("power law with the single yield Y_bow, capped at c0 for anything lighter than 1.32e10.")
print("The photon tops it because it IS the medium; the neutrino threads at the cap; the")
print("ladder falls 1/sqrt(rho) through the gas branch, 954 at Max-P, 72 at the core -")
print("and the runaway SMBH sits at 0.996 of its rung. ONE medium, ONE yield, every object's")
print("C - the scaling is perfect by construction, and the anchors all sit on it.")
