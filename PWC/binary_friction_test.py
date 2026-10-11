# Lock-it-down: binary pulsar friction vs the observed orbital decay (2026-10-09)
# The framework's own ruling: matter is a sieve (~99.99% empty). The drag = the knots'
# cross-sections only. Test: does the friction cover any of PSR B1913+16's observed decay?
import math
G = 6.6743e-11; c0 = 2.99792458e8
rho0 = 8.74e-27
mp = 1.6726e-27; Rp = 8.414e-16
rho_core = 2.3e17
Msun = 1.989e30

print("== PSR B1913+16 (Hulse-Taylor) ==")
M1, M2 = 1.4414, 1.3867          # Msun
a = 1.9501e9                      # m semi-major axis
e = 0.6171334
r_peri = a*(1-e)
M = (M1+M2)*Msun
v_peri = math.sqrt(G*M*(1+e)/r_peri)
print(f"periastron: r = {r_peri/1e9:.3f} Gm ; v = {v_peri/1e3:.0f} km/s  (cap = 954 km/s)")

print("\n== The sieve cross-section ==")
d_knot = (mp/rho_core)**(1/3.0)      # knot spacing at the core
pack = (Rp/d_knot)**2                # surface packing fraction (the first layer blocks)
R_ns = 1.2e4                         # 12 km neutron star
A_eff = pack*math.pi*R_ns**2
print(f"knot spacing {d_knot/1e-15:.2f} fm ; packing fraction {pack:.3f}")
print(f"effective frontal area of ONE neutron star = {A_eff:.3e} m^2  (the sieve)")

print("\n== The friction ==")
Cd = 1.0
F = 0.5*rho0*v_peri**2*Cd*A_eff
P_fric = F*v_peri
print(f"drag force F = 0.5 rho0 v^2 Cd A = {F:.3e} N")
print(f"friction power = F v = {P_fric:.3e} W")

print("\n== The observed decay ==")
Pdot_obs = -2.4025e-12              # s/s
P_orb = 27906.98                    # s
E_loss = (2.0/3.0)*G*M1*M2*Msun**2*math.pi/(P_orb*a)   # rough: dE/dt = -(32/5)... use scale
E_loss_obs = 7.35e24                # W (the literature value for B1913+16)
print(f"observed orbital decay power = {E_loss_obs:.3e} W (matches GR to ~0.2%)")
print(f"framework friction share = {P_fric/E_loss_obs:.2e} of the observed decay")

print("\n== Verdict ==")
print(f"the sieve-friction is 25 orders below the observed decay: the framework's own")
print(f"numbers say the decay CANNOT be drag. The energy leaves through the medium's")
print(f"tension cycles (the wave channel: each orbit re-tensions the medium, doing work).")
print(f"The falsifiable prediction: NO friction component in any orbital decay beyond the")
print(f"wave channel - standard physics says zero drag, PWC says 1e-25 of the wave rate,")
print(f"distinguishable in principle, both consistent with every measured decay. The")
print(f"'margin of error' is NOT covered by friction - it is covered by the wave.")
print(f"-> this also guards the 954 km/s cap: at periastron B1913+16 runs 902 km/s, just")
print(f"   under the cap, exactly where the framework's continuous passage scale puts it.")

print("\n== The finite-boundary mass sum (the pasted EOS claim) ==")
V_obs = 3.57e80
M_medium = rho0*V_obs
print(f"M_medium = rho0 V_obs = {M_medium:.3e} kg ; matter (5%) = {0.05*M_medium:.2e} kg")
print(f"the calculable sum, no infinity needed (the ambient tension + the volume).")
