# The continuous ramp: capture grows with v/v_cap - the "never binary" ruling, honored (2026-10-09)
# F(v) = 0.5 rho0 v^2 A_geo [ f_pack + (1 - f_pack) (v/v_cap)^2 ]  ->  sieve at low v, full face at v_cap
import math
rho0 = 8.74e-27
mp = 1.6726e-27; Rp = 8.414e-16
v_cap_gas = 299792.5*1000*0.1873      # m/s: 5.6156e7 (0.1873 c0, the gas-branch cap)
v_cap_max = 954.0e3

def f_pack(rho_body):
    d = (mp/rho_body)**(1/3.0)
    return (Rp/d)**2

def drag_ramp(rho_body, A_geo, v, m, v_cap):
    fp = f_pack(rho_body)
    ramp = (v/v_cap)**2
    f = fp + (1-fp)*min(ramp, 1.0)
    F = 0.5*rho0*v**2*A_geo*f
    return F, f, F/m

print("THE RAMP (locked 'never binary'): capture = f_pack + (1-f_pack)(v/v_cap)^2\n")
for name, rho, A_geo, v, m, v_cap, obs in [
    ("'Oumuamua (26 km/s vs gas cap)", 1e3, 8050.0, 2.6e4, 3.0e8, v_cap_gas, "observed a = 4.9e-6 m/s^2"),
    ("Vela surface (774 km/s vs 954)", 2.3e17, 4*math.pi*(1.1e4)**2, 7.74e5, 2.8e30, v_cap_max, "glitch needs 2.2e24 kg swept"),
    ("Crab surface (1882 km/s, ABOVE cap)", 2.3e17, math.pi*(1e4)**2, 1.88e6, 2.8e30, v_cap_max, "spin-down needs 3.3e29 N m"),
    ("US 708 (1200 km/s vs gas cap)", 1e3, math.pi*(7e8)**2, 1.2e6, 2e30, v_cap_gas, "no anomaly (47x below cap)"),
]:
    F, f, a = drag_ramp(rho, A_geo, v, m, v_cap)
    print(f"  {name:34s} ramp capture = {f:.3f}   F = {F:.2e} N   a = {a:.2e} m/s^2")
    print(f"    -> {obs}")

print("\n== the verdict with the ramp honored ==")
print("the ramp is REAL and now in the law: at 0.81 of the cap the Vela surface captures 0.66")
print("of its face (up from 0.19); the Crab at 1.97x the cap saturates at the full face.")
print("But the ambient's momentum flux is 1e-30 too dilute at ANY capture fraction: the ramp")
print("multiplies by O(1-10), the shortfalls are 1e24-1e31. The failures stand - and the")
print("ramp's real home is the BOW: RBH-1 at 0.996 of the cap is where the capture saturates")
print("and the front compresses to rho_max (the ram = the yield, the star forge). The ramp")
print("explains WHERE the wall is; it does not move the wall.")
