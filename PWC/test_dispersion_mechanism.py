import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

# Test: does a FIXED (distance-proportional, not cosmic-history-dependent) dispersion
# between a fast "peak" component and a slow "tail" component reproduce (1+z) scaling
# for the arrival-time gap, across real supernova distances?
#
# Mechanism: Delta_t_arrival = D * (1/v_tail - 1/v_peak) = D * Delta_v / (v_peak*v_tail)
# i.e. arrival gap is LINEAR in distance D, with a FIXED dispersion coefficient
# (v_peak, v_tail treated as constants of the medium, not evolving with cosmic time).
#
# Real observed requirement: Delta_t_arrival / tau_rest = z  (so tau_obs = tau_rest*(1+z))
#
# Use the REAL measured luminosity-distance-vs-z relation (flat LCDM, Planck-like
# parameters) as the actual D(z) used to interpret real SN Ia data -- this is the
# real mapping between "how far away" and "what z gets measured" in the actual
# observations being explained, regardless of which theory is doing the explaining.

c = 299792.458  # km/s
H0 = 67.4  # km/s/Mpc
Om = 0.315
OL = 0.685

def E(z):
    return np.sqrt(Om*(1+z)**3 + OL)

def D_C(z):  # comoving distance, Mpc
    integrand = lambda zp: c/(H0*E(zp))
    val, _ = quad(integrand, 0, z)
    return val

def D_L(z):  # luminosity distance, Mpc
    return (1+z)*D_C(z)

z_vals = np.array([0.1, 0.3, 0.5, 0.8, 1.0, 1.5])
D_vals = np.array([D_C(z) for z in z_vals])  # use comoving/light-travel-proportional distance

# Calibrate the dispersion coefficient k (= Delta_v/(v_peak*v_tail)) so the LOW-z point
# matches exactly (giving the mechanism its best possible chance), then check if
# linear-in-D scaling tracks (1+z) at higher z or diverges.
k_calibrated = z_vals[0] / D_vals[0]   # forces exact match at z=0.1

predicted_ratio = k_calibrated * D_vals  # this stands in for "Delta_t/tau_rest", compare to z directly

print(f"{'z':>6} {'D (Mpc)':>12} {'required (z)':>14} {'predicted (k*D)':>16} {'ratio pred/req':>16}")
for z, D, p in zip(z_vals, D_vals, predicted_ratio):
    print(f"{z:6.2f} {D:12.1f} {z:14.3f} {p:16.3f} {p/z:16.4f}")
