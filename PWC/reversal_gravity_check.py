# Gravity = the EM pull re-tying the separated matter (the opposite of the untying) (2026-10-12)
import math
c0 = 2.99792458e8
rho0 = 8.74e-27
H0 = 32.371*c0**2
s = 1.0/19.0
alpha = 1.0/137.036
g_target = 16*math.pi**3*alpha/3.0

print("== 1. The two directions ==")
P_heat = rho0*H0/3.0          # the heat's separating pressure (the untying direction)
Y_pair = s*rho0*c0**2/3.0     # the pair tension (the EM re-pairing pull)
print(f"the untying push:  the heat's pressure   = {P_heat:.3e} Pa")
print(f"the tying pull:    the pairs' re-pairing  = {Y_pair:.3e} Pa")
print(f"heat wins by:      {P_heat/Y_pair:.0f}x  - the expansion runs today (95% re-absorbed)")
print(f"the reversal (the Great Rejoining): when the heat drains below the pull - the pull")
print(f"then re-ties everything and expels the heat again. Gravity = that pull, local.")

print("\n== 2. The g-S8 identity ==")
print(f"g = 16 pi^3 alpha/3 = {g_target:.6f}")
S8 = 1.0/g_target
print(f"1/g = {S8:.4f}  ->  g x S8 = 1 requires S8 = {S8:.4f}")
print(f"the observed S8: lensing 0.76-0.80 (DES Y3, KiDS) ; CMB-calibrated 0.834 +/- 0.016")
print(f"   -> 1/S8_CMB = {1/0.834:.4f}  (vs g = 1.2067: {100*(1/0.834/g_target-1):+.1f}%)")
print(f"   -> S8 = 0.8287 gives g exactly: the CMB-calibrated band contains it.")
print(f"\nreading: g = 1/S8 = the reciprocal of the tension fraction. The lensing 'low' (S8 < 1)")
print(f"= the medium's tension today, drained to ~83% of the formation calibration by the 95%")
print(f"re-absorption. The coupling g = the amplification that converts the drained tension")
print(f"into the grip - and the catastrophic reversal = the drain crossing the pull's threshold.")
print(f"gravity = the EM pull of the separated matter through the heat - the exact opposite of")
print(f"the untying, and g is its amplification from the observed low tension.")
