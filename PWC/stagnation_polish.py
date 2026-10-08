# Stagnation-scale polish: core-hold threshold, k-rule sheet relation, falsification
import math
G = 6.6743e-11
rho_max = 1.304e15
rho_core = 2.3e17
a_max = 3.23e11
Msun = 1.989e30

print("== 1. Core-hold threshold (a core holds Max-P iff its surface gravity >= yield) ==")
R_core_star = 3.0*a_max/(4.0*math.pi*G*rho_core)
M_core_star = (4.0*math.pi/3.0)*rho_core*R_core_star**3
print(f"R*_core = 3 a_max/(4 pi G rho_core) = {R_core_star/1e3:.2f} km ; M* = {M_core_star/Msun:.3f} Msun")
print("-> every neutron star / black hole core above ~0.06 Msun holds Max-P trivially.")
for M, R in [(1.4, 1.425e4), (5.3, 2.18e4)]:
    g = G*M*Msun/R**2
    print(f"   {M} Msun core at {R/1e3:.1f} km: g = {g:.2e} = {g/a_max:.1f}x a_max  (held)")

print("\n== 2. Sheet vs ball: the k-rule candidate column and the stagnation column ==")
Sigma_sheet = a_max/(2.0*math.pi*G)      # flat-sheet self-pull 2 pi G Sigma = a_max (OPEN_WORK candidate)
Sigma_ball = 3.0*a_max/(4.0*math.pi*G)   # ball self-pull (4pi/3) G rho R = a_max
print(f"sheet column  a_max/(2 pi G)  = {Sigma_sheet:.4e} kg/m^2  (k-rule candidate law)")
print(f"ball column   3 a_max/(4 pi G) = {Sigma_ball:.4e} kg/m^2  (stagnation scale)")
print(f"ratio = {Sigma_ball/Sigma_sheet:.3f} = 3/2 exactly (the geometry: g_sheet = 2pi G Sigma vs")
print(f"g_ball = (4pi/3) G rho R).  The two candidates are ONE balance in two geometries.")
print(f"k-rule measured Sigma = 8.48e20 = {8.48e20/Sigma_ball:.3f}x the ball column")

print("\n== 3. Falsification structure of the stagnation scale ==")
print("(i)  A sub-column chunk (rho*R < 1.155e21) showing a bow shock or drag would kill the")
print("     FREE regime. All merger dumps (<= ~10 Msun << 1,910) are sub-column -> every GW")
print("     event without a bow-shock counterpart is a pass; GW170817's GRB is ejected MATTER,")
print("     not a medium bow shock - consistent.")
print("(ii) A pure-Max-P object >= 886 km moving freely at c0 would kill the STAGNANT regime.")
print("     No such object is known; the 886 km / 1,910 Msun boundary is unpopulated in the")
print("     catalogue (the session log's 13 'NO SOLUTION' rows sit above it).")
print("(iii) The 954 km/s stagnation speed is anchored by RBH-1 alone; a second at-cap object")
print("     (recoil candidates at 1300-2470 km/s are ABOVE the cap - the slammed-bow regime,")
print("     not the wake regime) would test it. 'Slowest wake bounds Y' stays open.")
print("(iv) Neutron stars: rho*R = 2.3e17 x 1e4 = 2.3e21 = 2.0x the column -> stagnant bodies,")
print("     cap 72 km/s - the pulsar census tension (observed 75-1610 km/s) is unchanged: the")
print("     same open cell ('rho_max crust 954 vs bare rho_n 72').")
