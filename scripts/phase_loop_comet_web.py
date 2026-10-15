# The adiabatic phase loop, comet-scale and web-scale (2026-10-08, Jaden's extension)
import math
c0 = 2.99792458e8
rho0 = 8.74e-27
H0 = 32.371*c0**2

print("== 1. The loop in the framework's own variables (no invented T) ==")
print("knot (heat-void, suction) -> UNTIE: draws c0^2 per kg from the surroundings ->")
print("expanding parcel climbs the gas-branch adiabat H(rho) = H0 - (c0^2/3) ln(rho/rho0),")
print("absorbing heat all the way back to H0 at rho0 -> RE-PAIR: the medium takes it all.")
print("The untie's volumetric suction and the heat's draw are the SAME co-attraction - the")
print("knot is the heat sponge (T7), the heat is the pull (PWC.md sec 1).")

print("\n== 2. The loop's spatial footprint (the tail) ==")
mdot = 1e2                  # kg/s shallow-rung (sublimation)
V_per_s = mdot/rho0
R_per_s = (3*V_per_s/(4*math.pi))**(1/3)
print(f"released volume per second at 1e2 kg/s: V = mdot/rho0 = {V_per_s:.2e} m^3")
print(f"loop radius per second of untying: {R_per_s/1e6:,.0f} km")
for days in (1, 30, 100):
    m = mdot*days*86400
    R = (3*m/(4*math.pi*rho0))**(1/3)
    print(f"  after {days:3d} days at 1e2 kg/s: m = {m:.1e} kg -> loop radius = {R/1.496e11:.2f} AU")
print("the visible tail samples the UNPAIRED (entropic) fraction of this loop; most re-pairs")
print("invisibly (the sec-5 cycle). The tail is the loop's spatial footprint - 'the exposure")
print("of the highly entropic tail continues that phase loop until the medium takes it all'.")

print("\n== 3. The cold signature = the per-kg heat deficit along the adiabat ==")
rho_loop = 1e-18            # a parcel mid-loop (between the nucleus vapor and rho0)
H_parcel = H0 - (c0**2/3.0)*math.log(rho_loop/rho0)
deficit = H0 - H_parcel
print(f"at rho = 1e-18: H = {H_parcel/c0**2:.1f} c0^2 vs H0 = {H0/c0**2:.1f} c0^2 ->")
print(f"per-kg deficit H0 - H = {deficit/c0**2:.1f} c0^2 = 19% of H0: the parcel is HEAT-POOR")
print(f"per kg while compressed (rho > rho0), and the deficit IS the suction - it pulls the")
print(f"ambient heat in until the parcel reaches H0 at rho0 (re-paired). The icy wake is the")
print(f"deficit made visible; 'exponentially cold' = the deficit growing as ln(rho0/rho) down")
print(f"the ladder.")

print("\n== 4. Web-scale: the steam-cloud loop = the same adiabat ==")
print("baryonic gas heated by untying events -> overexpands along the same gas-branch")
print("adiabat -> cools (heat-poor, 'freezes') -> falls back toward the web -> re-pairs.")
print("Comet tail and thermal web are ONE loop at two scales: untie (endothermic) ->")
print("overexpansion (adiabatic cooling) -> re-pair (the medium takes it all).")
