# The stagnation scale: what size and density turn the free wave into a stagnant body
import math
G = 6.6743e-11
rho_max = 1.304e15
rho_core = 2.3e17
a_max = 3.23e11          # the yield (holding threshold at rho_max)
Y = 5.93e26              # the bow-wave anchor pressure
Msun = 1.989e30
c0 = 2.998e8

print("== The condition: a chunk holds itself at density rho iff surface gravity >= yield ==")
g_surf = lambda rho, R: (4.0*math.pi/3.0)*G*rho*R
R_star = 3.0*a_max/(4.0*math.pi*G*rho_max)
M_star = (4.0*math.pi/3.0)*rho_max*R_star**3
col = 3.0*a_max/(4.0*math.pi*G)
print(f"column scale rho*R >= 3 a_max/(4 pi G) = {col:.4e} kg/m^2")
print(f"at rho_max: R* = {R_star/1e3:,.0f} km ;  M* = {M_star/Msun:,.0f} Msun")
print(f"  (the session log's 'pure rho_max sphere holds all the mass' limit = 1,910 Msun -")
print(f"   now it is the STAGNATION BOUNDARY)")

print("\n== The two cases ==")
# the merger dump: 3 Msun released at rho_max
M3 = 3*Msun
R3 = (3*M3/(4*math.pi*rho_max))**(1/3)
g3 = g_surf(rho_max, R3)
print(f"merger dump: M = 3 Msun at rho_max -> R = {R3/1e3:.0f} km, g_surf = {g3:.3e}")
print(f"  g/a_max = {g3/a_max:.3f} (8.6x BELOW the yield) -> cannot hold itself -> unheld ->")
print(f"  free decompression at c0: the wave. No drag, no bow shock, under the cavitation")
print(f"  limit.  [Jaden's reading, now as a number]")

# the runaway: core-held Max-P
for Mbh, lab in [(1e7, "RBH-1 (1e7 Msun)"), (1e8, "RBH-1 (1e8 Msun)")]:
    Rc = (3*Mbh*Msun/(4*math.pi*rho_core))**(1/3)
    gc = G*Mbh*Msun/Rc**2
    print(f"{lab}: core R = {Rc/1e3:,.0f} km, g_surf = {gc:.3e} = {gc/a_max:.0f}x the yield "
          f"-> HELD at Max-P -> displaces the medium -> stagnation at "
          f"v_c = sqrt(2Y/rho_max) = {math.sqrt(2*Y/rho_max)/1e3:.0f} km/s -> cavitation.")

print("\n== The scale, stated precisely ==")
print("STAGNATION if rho*R >= 3 a_max/(4 pi G) = 1.155e21 kg/m^2 (self-hold >= yield),")
print("  equivalently any confinement with pull >= a_max (a core's surface gravity).")
print("At rho_max: R >= 886 km / M >= 1,910 Msun self-held.")
print("Below: FREE - decompresses at c0, no visible drag, no cavitation (the gravity wave).")
print("At/above: STAGNANT BODY - displacement, drag, cavitation at v_c = sqrt(2Y/rho).")
print("The 3-Msun wave sits at 0.116x the boundary; the runaway at ~550x above it.")
print("(k-rule held column Sigma = 8.48e20 kg/m^2 = 0.73x the stagnation column - same decade)")
