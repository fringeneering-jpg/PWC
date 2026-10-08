# Round-7 checks: caloric ladder vs the slam work; the wake selects the Y channel;
# the stale 0.207 m^3 bookkeeping flag.
import math
c0 = 2.99792458e8
c0sq = c0**2
rho0 = 8.74e-27
rhomax = 1.304e15
s = 1.0/19.0

print("== 1. Slam work vs the full compression ladder ==")
W_slam = c0sq/math.sqrt(3.0)        # resting-medium spike: dP*dv = rho0 c0^2/sqrt3 * (1/rho0)
Q_ladder = 32.371*c0sq
print(f"spike work per kg: (rho0 c0^2/sqrt3)*(1/rho0) = {W_slam/c0sq:.4f} c0^2")
print(f"full ladder per kg: 32.371 c0^2 -> the slam pays {100*W_slam/Q_ladder:.2f}% of the")
print(f"compression; the medium's own H0 >= 32.371 c0^2 finances the rest.")
print("-> my T2 'work-limited ceiling 1/sqrt3, T2 at 43% of ceiling' reading is superseded:")
print("   the 4/sqrt3 = 2.309 ratio stands as a geometric-prefactor comparison only;")
print("   T2's eta = 1/4 is geometric, not work-budget-limited. The spike is the trigger.")

print("\n== 2. The wake observation selects the Y channel ==")
v_coh = c0*math.sqrt(2*0.061379)    # locked-end cavitation speed from Y_coh = 0.061379 P_locked
Y_bow = 5.93e26
v_bow = math.sqrt(2*Y_bow/rhomax)
print(f"cohesion channel: v_cav(rho_max) = c0*sqrt(2*0.061379) = {v_coh/1e3:.0f} km/s")
print(f"bow-wave channel:  v_cav = sqrt(2*Y_bow/rho_max) = {v_bow/1e3:.0f} km/s (locked 954)")
print(f"RBH-1 moves at 954 km/s and the wake EXISTS -> the passage limit at rho_max is Y_bow,")
print(f"not Y_coh (a 110x difference). Proposal for the keystone's 6c tension: Y_bow is the")
print(f"DYNAMIC tear threshold, Y_coh the STATIC cohesion ceiling - two channels, no conflict;")
print(f"the wake observation is the evidence that the bow-wave boundary sits at 0.9021 of the")
print(f"heat ladder (the passage limit engages 9.8% short of full heat expulsion).")

print("\n== 3. The 0.207 m^3 bookkeeping flag (keystone A6) ==")
mn = 1.6749e-27
print(f"m_n/rho0 (rho0 = 8.74e-27): {mn/rho0:.5f} m^3  (keystone: locked 0.1916)")
print(f"m_n/8.1e-27 (stale rho0):  {mn/8.1e-27:.5f} m^3  (CLAUDE.md's '0.207 m^3')")
mp = 1.6726e-27
print(f"my T7 reach 3*m_p/rho0 = {3*mp/rho0:.4f} m^3 uses the correct rho0 - Identity 3 unaffected")
