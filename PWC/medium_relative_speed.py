# The medium-relative speed: the Sun's 370 km/s through the medium is the varying factor
import math
rho0 = 8.74e-27
v_sun = 370.0e3          # the Sun through the bath (the CMB dipole)
v_oom = 26.0e3           # 'Oumuamua heliocentric (hyperbolic excess)
A = 8050.0               # the object's cross-section
f_pack = 5.02e-11        # its own capture (from its density 1e3)

print("== 'Oumuamua through the MEDIUM (not through the Sun's frame) ==")
for case, v_rel in [("heliocentric only (the old number)", v_oom),
                    ("anti-sunward leg (v_rel = 26 + 370)", v_oom + v_sun),
                    ("sunward leg (v_rel = 370 - 26)", v_sun - v_oom)]:
    F = 0.5*rho0*v_rel**2*f_pack*A
    a = F/3.0e8
    print(f"  {case:42s} v_rel = {v_rel/1e3:5.1f} km/s -> a = {a:.2e} m/s^2")
print(f"  observed non-gravitational acceleration = 4.92e-6 m/s^2, ANTI-sunward")
print(f"\n-> the 370 km/s boosts the drag 232x (26^2 -> 396^2), but the shortfall stays 1e21:")
print(f"   4.9e-6 / (4e-27) = 1e21. And the SIGN stays wrong: the drag with the medium-")
print(f"   relative velocity is SUNWARD (it opposes the relative motion), while the observed")
print(f"   residual is ANTI-sunward. The medium-relative speed cannot rescue the magnitude,")
print(f"   and it makes the direction worse. The v^2 IS the varying factor in the law; the")
print(f"   medium's thinness is the wall, not the speed bookkeeping.")
