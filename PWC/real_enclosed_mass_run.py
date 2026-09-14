import logging, warnings
import numpy as np
from gwpy.timeseries import TimeSeries
from scipy.signal import savgol_filter
from scipy.stats import linregress
warnings.filterwarnings('ignore')

trigger_time = 1126259462.4
duration = 4.0
sample_rate = 2048
f_min, f_max = 20.0, 300.0
psd_duration = 128.0

print("--> Fetching real H1 data + off-source PSD...")
event_strain = TimeSeries.fetch_open_data('H1', trigger_time-duration/2, trigger_time+duration/2, cache=True).resample(sample_rate)
bg_strain = TimeSeries.fetch_open_data('H1', trigger_time-duration/2-psd_duration, trigger_time-duration/2, sample_rate=4096, cache=True).resample(sample_rate)
psd_gwpy = bg_strain.psd(fftlength=duration, overlap=duration/2, method="median")
asd_gwpy = psd_gwpy**0.5
clean_strain = event_strain.whiten(asd=asd_gwpy).bandpass(f_min, f_max)

print("--> Q-transform + MAD-threshold ridge extraction (no hand-tuned filter)...")
q_outseg = (trigger_time+0.25, trigger_time+0.50)
hq = event_strain.q_transform(frange=(f_min, f_max), qrange=(4,64), outseg=q_outseg)
hq_times, hq_freqs, hq_matrix = hq.times.value, hq.frequencies.value, hq.value

chirp_start, chirp_end = trigger_time+0.35, trigger_time+0.43
c_mask = (hq_times >= chirp_start) & (hq_times <= chirp_end)
c_times, c_power = hq_times[c_mask], hq_matrix[c_mask, :]

baseline_mask = (hq_times >= trigger_time+0.25) & (hq_times < trigger_time+0.34)
baseline = hq_matrix[baseline_mask, :]
noise_floor = np.median(baseline)
mad = np.median(np.abs(baseline - noise_floor))
thresh = noise_floor + 2.5*(1.4826*mad)

r_idx = np.argmax(c_power, axis=1)
peak_powers = np.max(c_power, axis=1)
v_mask = peak_powers > thresh
rt_clean = c_times[v_mask] - trigger_time
rf_clean = hq_freqs[r_idx[v_mask]]

order = np.argsort(rt_clean)
t, f = rt_clean[order], rf_clean[order]
print(f"    Ridge: {len(t)} nodes, {f.min():.1f}-{f.max():.1f} Hz, t=[{t.min():.4f},{t.max():.4f}]s\n")

window = min(11, len(t) - (1 - len(t)%2))
if window < 5: window = 5
poly_order = 3
f_smooth = savgol_filter(f, window_length=window, polyorder=poly_order)
dfdt = savgol_filter(f, window_length=window, polyorder=poly_order, deriv=1, delta=np.median(np.diff(t)))

G, c_light, Msun = 6.674e-11, 2.998e8, 1.989e30
prefactor = (5.0/96.0) * c_light**5 / (np.pi**(8.0/3.0) * G**(5.0/3.0))
valid = (dfdt > 0) & (f_smooth > 0)
M_eff = np.full_like(f_smooth, np.nan)
M_eff[valid] = (prefactor * dfdt[valid] / f_smooth[valid]**(11.0/3.0))**(3.0/5.0)
M_eff_Msun = M_eff / Msun

print(f"{'f (Hz)':>10} {'M_eff (Msun)':>14} {'M_eff/65':>10}")
for fi, mi in zip(f_smooth[valid], M_eff_Msun[valid]):
    print(f"{fi:10.1f} {mi:14.2f} {mi/65.0:10.3f}")

slope, intercept, r_value, p_value, std_err = linregress(f_smooth[valid], M_eff_Msun[valid])
print(f"\nTrend: slope={slope:.5f} Msun/Hz, r^2={r_value**2:.3f}, p={p_value:.4f}, n={valid.sum()}")
if p_value < 0.05 and slope > 0:
    print("-> REAL, SIGNIFICANT RISING TREND: consistent with growing enclosed mass.")
elif p_value < 0.05 and slope < 0:
    print("-> REAL, SIGNIFICANT FALLING TREND: opposite of the enclosed-mass-growth prediction.")
else:
    print("-> No significant trend: consistent with a flat, fixed total mass.")
print(f"\nMedian M_eff across track: {np.nanmedian(M_eff_Msun):.2f} Msun (compare to known 65 Msun total)")
