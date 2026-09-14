import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, curve_fit

# Real benchmark: the actual "extra dimming" data that founded dark energy is the
# distance-modulus RESIDUAL between (a) what's actually measured for real SNe Ia and
# (b) what a simple, non-accelerating, matter-only (Omega_m=1, decelerating) universe
# predicts for the same redshift. That residual is real, measured, grows with z,
# and peaks around 0.2-0.25 magnitudes near z~1 in the real data (Riess 1998,
# Perlmutter 1999, and it's essentially the mu(LCDM) - mu(matter-only) curve, since
# LCDM was fit specifically to match the real measured residual).

c = 299792.458
H0 = 67.4

def E_LCDM(z, Om=0.315, OL=0.685):
    return np.sqrt(Om*(1+z)**3 + OL)

def E_matter_only(z, Om=1.0):
    return np.sqrt(Om*(1+z)**3)

def D_C(z, E_func):
    val, _ = quad(lambda zp: c/(H0*E_func(zp)), 0, z)
    return val

def dist_mod(z, E_func):
    D_L = (1+z)*D_C(z, E_func)  # Mpc
    return 5*np.log10(D_L) + 25  # standard distance modulus, D_L in Mpc

z_vals = np.array([0.1, 0.3, 0.5, 0.8, 1.0, 1.5])

mu_LCDM = np.array([dist_mod(z, E_LCDM) for z in z_vals])
mu_matter = np.array([dist_mod(z, E_matter_only) for z in z_vals])
real_residual_mag = mu_LCDM - mu_matter   # THIS is the real "extra dimming" signature, in magnitudes

print("Real target: magnitude residual (extra dimming) that dark energy explains")
print(f"{'z':>6} {'residual (mag)':>16}")
for z, r in zip(z_vals, real_residual_mag):
    print(f"{z:6.2f} {r:16.4f}")

# Now: PWC boundary-decompression model.
# Compaction ~ D (void-crossing distance, use matter-only comoving distance as the
# "true" physical distance PWC would use, since it has no dark-energy acceleration term)
D_vals = np.array([D_C(z, E_matter_only) for z in z_vals])

# Flux loss factor from decompression: try compaction^p for a few plausible p,
# converted to magnitudes (mag = -2.5*log10(flux_ratio)), calibrated to match at z=1.0
# (the best-measured, most central point in the real historical data) so it gets the
# fairest possible shot, then check the whole curve shape.
print()
print("Testing decompression models: extra_mag = A * D^p, calibrated to match real residual at z=1.0")
for p in [0.5, 1.0, 1.5, 2.0]:
    # calibrate A at z=1.0 (index 4)
    idx_cal = 4
    A = real_residual_mag[idx_cal] / (D_vals[idx_cal]**p)
    predicted_mag = A * D_vals**p
    print(f"\n p={p}:")
    print(f"{'z':>6} {'real residual':>14} {'predicted':>12} {'ratio pred/real':>16}")
    for z, real, pred in zip(z_vals, real_residual_mag, predicted_mag):
        print(f"{z:6.2f} {real:14.4f} {pred:12.4f} {pred/real:16.4f}")
