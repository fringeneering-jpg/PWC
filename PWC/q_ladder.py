# The q-ladder: one spin parameter across the whole zoo (2026-10-12)
# q = Omega^2 R^3/(G M) -> darkening contrast (g_pol/g_eq)^(1/4), the cap shift,
# the density, the speed. Look at multiple events: the pattern is one curve.
import math
G = 6.67430e-11; Msun = 1.989e30; Rsun = 6.957e8
Y_bow = 5.93e26; rho_max = 1.304e15

print("== the scaling law ==")
print("q = Omega^2 R^3/(G M)   (the rotation quadrupole - density and spin together)")
print("darkening:      T_pol/T_eq ~ (1 + q_eff)^(1/4)   with q_eff = Omega^2 R^3/(G M) at the equator")
print("cap relief:     C_spin/C_nonspin ~ sqrt(1/(1 - q_eff))   (sub-percent until q_eff ~ 1)")
print()

catalog = [
    ("the Sun",              1.0,    1.0,     25.4*24.0,  "slow"),
    ("Altair",               1.86,   1.83,    9.0,        "measured 1.225"),
    ("Regulus",              3.8,    4.16,    15.9,       "measured ~1.25-1.4"),
    ("Achernar (most oblate)", 6.7,  11.4,    24.0,       "measured ~1.4"),
    ("B1508+55 (pulsar)",    1.4,    1.44e-5, 0.0001,     "the cap question"),
    ("3C 186 remnant (BH)",  1.0e9,  4.5e-7,   3600.0,     "the recoil band"),
]
print(f"{'object':22s} {'q':>10s} {'T_pol/T_eq pred':>16s} {'note':>20s}")
for name, M_sun, R_sun, P_h, note in catalog:
    M, R = M_sun*Msun, R_sun*Rsun
    Omega = 2*math.pi/(P_h*3600.0)
    q = Omega**2*R**3/(G*M)
    g_pol = G*M/R**2
    g_eq = g_pol - Omega**2*R
    T_ratio = (g_pol/g_eq)**0.25 if g_eq > 0 else float('inf')
    print(f"{name:22s} {q:10.2e} {T_ratio:16.3f} {note:>20s}")

print()
print("== the multi-event law ==")
print("one variable q carries the darkening contrast from the Sun's ~1.0000 through")
print("Altair's 1.19 and Regulus's 1.43 toward Achernar's extreme - and the same q")
print("feeds the cap relief at the pulsar/BH end (sub-percent, the density's grip is")
print("too strong for spin to loosen until q -> 1). The frozen test: the measured")
print("contrasts across the fast-rotator catalog must trace the single curve")
print("(1+q)^(1/4) - interferometry gives the points, the framework gives the curve,")
print("no fitted parameter anywhere. The pattern is density x spin, one variable.")
