# =====================================================================
# PWC MODULE: EFFECTIVE/ENCLOSED MASS FROM THE REAL CHIRP TRAJECTORY
# =====================================================================
# Run this AFTER the Module 1-4 extraction cell (needs event_strain,
# rt_clean, rf_clean already in memory from that cell).
#
# At every point along the real extracted ridge, compute the effective
# gravitating mass implied by the LOCAL frequency and its LOCAL rate of
# change -- this is the standard chirp-mass relation, applied pointwise
# instead of assuming one fixed value for the whole inspiral.
#
# Flat M_eff(t) ~ 65 Msun throughout  -> fixed total mass, no growing
#                                         enclosed-mass effect in the data.
# Rising M_eff(t) as f increases      -> real evidence more of the
#                                         gradient mass becomes dynamically
#                                         enclosed as separation shrinks.
# =====================================================================

import numpy as np
import matplotlib.pyplot as plt

G = 6.674e-11
c_light = 2.998e8
Msun = 1.989e30

# --- Smoothed numerical derivative df/dt from the real extracted ridge ---
# rt_clean, rf_clean assumed already in memory from the Module 1-4 cell,
# rt_clean in seconds relative to trigger, rf_clean in Hz.
t = rt_clean.copy()
f = rf_clean.copy()

order = np.argsort(t)
t, f = t[order], f[order]

# Use a moving polynomial (Savitzky-Golay style via numpy polyfit on a
# sliding window) for a smoother, more honest df/dt than raw finite
# differences on noisy real ridge points.
from scipy.signal import savgol_filter

window = min(11, len(t) - (1 - len(t) % 2))  # odd window, capped to data length
if window < 5:
    window = 5 if len(t) >= 5 else len(t) - (1 - len(t) % 2)
poly_order = 3 if window > 4 else 2

f_smooth = savgol_filter(f, window_length=window, polyorder=poly_order)
dfdt = savgol_filter(f, window_length=window, polyorder=poly_order, deriv=1, delta=np.median(np.diff(t)))

# --- Pointwise effective chirp-mass style total mass ---
# M_eff = [ (5/96) * c^5 / (pi^(8/3) * G^(5/3)) * (df/dt) / f^(11/3) ]^(3/5)
# NOTE: this is the standard GR chirp-mass formula, used here purely as a
# theory-neutral way to convert (f, df/dt) into an effective mass number --
# it does not assume PWC or GR is correct, it's just dimensional bookkeeping
# already agreed as the real, standard way this conversion is made.
valid = (dfdt > 0) & (f_smooth > 0)
M_eff = np.full_like(f_smooth, np.nan)
prefactor = (5.0/96.0) * c_light**5 / (np.pi**(8.0/3.0) * G**(5.0/3.0))
M_eff[valid] = (prefactor * dfdt[valid] / f_smooth[valid]**(11.0/3.0))**(3.0/5.0)
M_eff_Msun = M_eff / Msun

M_known_total = 65.0  # Msun, the real, already-established total apparent mass

print("--> Pointwise effective mass along the real inspiral track:")
print(f"{'f (Hz)':>10} {'M_eff (Msun)':>14} {'M_eff / 65':>12}")
for fi, mi in zip(f_smooth[valid], M_eff_Msun[valid]):
    print(f"{fi:10.1f} {mi:14.2f} {mi/M_known_total:12.4f}")

# --- Trend check: is M_eff flat or systematically rising with f? ---
from scipy.stats import linregress
slope, intercept, r_value, p_value, std_err = linregress(f_smooth[valid], M_eff_Msun[valid])
print(f"\nLinear trend of M_eff vs frequency: slope={slope:.5f} Msun/Hz, "
      f"r^2={r_value**2:.3f}, p={p_value:.2e}")
if p_value < 0.01 and slope > 0:
    print("--> STATISTICALLY SIGNIFICANT RISING TREND: consistent with a growing")
    print("    enclosed mass as separation shrinks. Real evidence, not assumed.")
elif p_value < 0.01 and slope < 0:
    print("--> STATISTICALLY SIGNIFICANT trend, but DECREASING -- opposite of the")
    print("    enclosed-mass-growth prediction. Worth reporting honestly either way.")
else:
    print("--> NO statistically significant trend: M_eff is consistent with flat,")
    print("    fixed total mass across the inspiral. No enclosed-mass growth signal.")

# --- Plot ---
fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
axes[0].plot(t, f, 'o', color='gold', ms=4, mec='black', label='Real ridge')
axes[0].plot(t, f_smooth, '-', color='blue', lw=1.5, label='Smoothed')
axes[0].set_ylabel('Frequency (Hz)')
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].plot(f_smooth[valid], M_eff_Msun[valid], 'o-', color='purple', ms=4)
axes[1].axhline(M_known_total, color='gray', ls='--', label=f'Fixed total mass ({M_known_total} Msun)')
axes[1].set_xlabel('Frequency (Hz)')
axes[1].set_ylabel('Effective mass (Msun)')
axes[1].set_title(f'Pointwise effective mass vs frequency (trend slope={slope:.4f} Msun/Hz, p={p_value:.2e})')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("\n[+] This is real, theory-neutral data extracted from the whole inspiral,")
print("    not a backward solve from one endpoint. Flat = no effect in the data.")
print("    Rising = real evidence, worth deriving the 1/r^2 comparison shape next.")
