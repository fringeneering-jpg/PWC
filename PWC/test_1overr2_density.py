import numpy as np

# Test: density history follows 1/r^2 (n=2), matching the same falloff as gravity (SS2).
# r stands in for cosmic scale factor a(t): a = 1/(1+z), so rho/rho0 = (1/a)^2 = (1+z)^2  -> n=2
# Keep v(rho) = c0 * sqrt(rho0/rho) EXACTLY as already in the doc (denser = slower, the sound-speed form from S2/S4).

z_vals = np.array([0.1, 0.5, 1.0, 1.5])
n = 2.0  # 1/r^2 density history

# timing stretch formula already derived & cross-validated by the redshift agent:
# dt_arrival/dt_emit = v(t_emit)/v(t_today) = sqrt(rho0/rho(t_emit)) = (1+z)^(-n/2)
timing_stretch_n2 = (1+z_vals)**(-n/2)

print("Testing n=2 (1/r^2) density history, WITH the existing (denser=slower) v(rho):")
print(f"{'z':>5} {'required(1+z)':>15} {'predicted stretch':>20} {'ratio pred/req':>16}")
for z, ts in zip(z_vals, timing_stretch_n2):
    req = 1+z
    print(f"{z:5.1f} {req:15.3f} {ts:20.4f} {ts/req:16.4f}")

print()
print("Now test WITH the sign flipped (denser = FASTER, v = c0*sqrt(rho/rho0)) + n=2:")
# if v(rho) = c0*sqrt(rho/rho0) instead (opposite sign), then
# dt_arrival/dt_emit = v(t_emit)/v(t_today) = sqrt(rho(t_emit)/rho0) = (1+z)^(n/2)
timing_stretch_flipped_n2 = (1+z_vals)**(n/2)
print(f"{'z':>5} {'required(1+z)':>15} {'predicted stretch':>20} {'ratio pred/req':>16}")
for z, ts in zip(z_vals, timing_stretch_flipped_n2):
    req = 1+z
    print(f"{z:5.1f} {req:15.3f} {ts:20.4f} {ts/req:16.4f}")
