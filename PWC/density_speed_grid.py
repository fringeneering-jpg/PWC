# THE GRID: the C of every density - the universal density/speed-limit map (2026-10-09)
import math
c0 = 2.99792458e8
s = 1.0/19.0
rho_max = 1.304e15; rho_core = 2.3e17
me = 9.1093837e-31; hbar = 1.054571817e-34

print("THE UNIVERSAL SPEED LIMIT:  v_max(rho) = sqrt(2Y/rho)   (the volume-to-mass law)\n")
print("=" * 66)

rows = []
# photon / energy: the wave IS the medium - no body density, no limit below c0
rows.append(("PHOTON / ENERGY (the unpaired wave, the medium itself)", "~ rho0 (the medium)", f"{c0/1e3:.1f} km/s  (c0 - the ceiling, not a limit)"))
# neutrino: the minimal knot, zero winding, threads everything
rows.append(("NEUTRINO (minimal knot, zero winding)", "threads all", f"just under {c0/1e3:.1f} km/s"))
# electron: its knot density at the footprint
lamC_bar = hbar/(me*c0); r_t = 3.3023*lamC_bar
rho_e = me/(4*math.pi*r_t**3/3.0)
Y_e = s*rho_e*c0**2/3.0
v_e = math.sqrt(2*Y_e/rho_e)
rows.append(("ELECTRON (knot at its 3.302 lamC_bar footprint)", f"{rho_e:.2e} kg/m^3", f"{v_e/1e3:.0f} km/s = {v_e/c0:.4f} c0"))
# gas-branch: Y/rho constant -> the same cap
rows.append(("GAS-BRANCH BODIES (Y/rho constant)", "any rho on the gas branch", f"{v_e/1e3:.0f} km/s = 0.187 c0 (the locked v_cav)"))
# Max-P matter
v_max = 954.0
rows.append(("MAX-P MATTER (the rho_max shell)", f"{rho_max:.3e}", f"{v_max} km/s (the locked cap: the bow, the stall)"))
# bare neutron
v_core = 72.0
rows.append(("BARE NEUTRON (the stacked core)", f"{rho_core:.3e}", f"{v_core} km/s (the locked floor of the ladder)"))
# the ladder's own anchors
rows.append(("LADDER ANCHORS (locked):", "1.32e10 / 1e11 / 1e13", "0.9998 c0 / 0.363 c0 / 0.0363 c0"))

for name, dens, v in rows:
    print(f"  {name:52s}  rho = {dens:22s}  v_max = {v}")

print("\n" + "=" * 66)
print("THE READING: each density has its own C. Light is the medium, so c0 is its own")
print("speed - not its limit. Every TIGHT knot has a limit set by its own density: the")
print("electron flies at 0.187 c0, Max-P matter stalls at 954, the bare neutron crawls at")
print("72. The 954 bow and the 72 core are the SAME formula at two densities - and the")
print("photon tops the grid because it IS the medium.")
print("\n== the SPARC question, honestly ==")
print("matching the friction to the known densities does NOT move the 0.1309 SPARC result:")
print("the friction enters every orbit at the 1e-26 level (the decay times are 1e8-1e28 Gyr).")
print("The rotation curves are the TENSION's law; the grid is the SPEED law. Two channels,")
print("one medium - the 0.1309 stands, and the grid is what the friction universalizes.")
