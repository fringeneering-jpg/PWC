# The spin branch: does rotation change the cap? (2026-10-12, Jaden's new question)
import math
G = 6.67430e-11; c0 = 2.99792458e8
Y_bow = 5.93e26; rho_max = 1.304e15
Msun = 1.989e30

print("== the two competing effects ==")
print("(1) centrifugal relief: the equatorial support drops by Omega^2 R, so the")
print("    cap-setting density relaxes:  C_spin/C_nonspin = sqrt(rho_non/rho_spin)")
print("(2) surface-speed loading: the co-rotating side adds Omega R to v_rel - an")
print("    asymmetric cap, the leading side loads first")
print()

def spin_correction(M, R, period_s):
    Omega = 2*math.pi/period_s
    q = Omega**2 * R**3 / (G*M)              # the rotation quadrupole parameter
    relief = Omega**2 * R / (G*M/R**2)       # centrifugal / surface gravity
    v_surf = Omega*R                         # the surface speed
    C_nonspin = math.sqrt(2*Y_bow/(0.2*rho_max))/1e3 if M > 1e3*Msun else math.sqrt(2*Y_bow/(rho_max))/1e3
    return q, relief, v_surf, C_nonspin

print("== the cases ==")
cases = [
    ("B1508+55 (fast pulsar)", 1.4*Msun, 1.0e4, 0.010),
    ("B1508+55 (slow end)",    1.4*Msun, 1.0e4, 0.100),
    ("3C 186 remnant (BH)",    1.0e9*Msun, 3.0e9, 3600.0),   # slow remnant spin guess
    ("3C 186 remnant (fast)",  1.0e9*Msun, 3.0e9, 300.0),    # fast remnant spin guess
]
for name, M, R, P in cases:
    q, relief, v_surf, C_non = spin_correction(M, R, P)
    C_spin = C_non / math.sqrt(1.0 - min(relief, 0.9))
    print(f"{name:22s} q = {q:.2e}  relief = {relief:.2e}  v_surf = {v_surf/1e3:6.1f} km/s")
    print(f"    C_nonspin = {C_non:6.0f} km/s -> C_spin = {C_spin:6.0f} km/s  (+{100*(C_spin/C_non-1):.3f}%)")

print()
print("== the honest read ==")
print("the pulsar's quadrupole parameter is ~5e-4: spin's density relief is sub-0.1%,")
print("so its cap barely moves - the 0.775 rho_max reading stands. The correction only")
print("matters where Omega^2 R approaches the surface gravity: the fast remnant's")
print("equatorial belt. The two effects compete: relief RAISES the cap (lower density),")
print("surface loading LOWERS it on the leading side (higher local v_rel). The frozen")
print("prediction: the recoil band's spread (0.21-0.29 rho_max) should correlate with")
print("remnant spin - the faster spinners at the band's low-density edge, and the")
print("co-rotating side showing the bow/cavitation asymmetry first. A candidate spin")
print("correction, not yet a derived one - the datum: the remnants' measured spins.")
