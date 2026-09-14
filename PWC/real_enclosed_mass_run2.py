import warnings
import numpy as np
from gwpy.timeseries import TimeSeries
from scipy.stats import linregress
warnings.filterwarnings('ignore')

trigger_time = 1126259462.4
duration, sample_rate = 4.0, 2048
f_min, f_max = 20.0, 300.0

event_strain = TimeSeries.fetch_open_data('H1', trigger_time-duration/2, trigger_time+duration/2, cache=True).resample(sample_rate)
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
t_full, f_full = rt_clean[order], rf_clean[order]
print(f"Full ridge: {len(t_full)} nodes over {t_full[-1]-t_full[0]:.4f}s "
      f"(native dt ~{np.median(np.diff(t_full))*1000:.3f} ms)")

# --- Bin onto a coarser, physically meaningful time grid to kill bin-jitter ---
n_bins = 20  # ~2.75 ms per bin across the 0.055s window -- enough points for a trend, coarse enough to average out 0.5 Hz quantization jitter
bin_edges = np.linspace(t_full[0], t_full[-1], n_bins+1)
t_binned, f_binned = [], []
for i in range(n_bins):
    m = (t_full >= bin_edges[i]) & (t_full < bin_edges[i+1])
    if m.sum() > 0:
        t_binned.append(np.mean(t_full[m]))
        f_binned.append(np.mean(f_full[m]))
t_binned, f_binned = np.array(t_binned), np.array(f_binned)
print(f"Binned to {len(t_binned)} points, dt ~{np.median(np.diff(t_binned))*1000:.2f} ms\n")

# Simple, robust centered finite difference on the binned (smoothed) series
f_binned = f_binned.astype(np.float64); t_binned = t_binned.astype(np.float64)
dfdt = np.gradient(f_binned, t_binned)

G, c_light, Msun = 6.674e-11, 2.998e8, 1.989e30
prefactor = (5.0/96.0) * c_light**5 / (np.pi**(8.0/3.0) * G**(5.0/3.0))
valid = (dfdt > 0) & (f_binned > 0)
M_eff = np.full_like(f_binned, np.nan)
M_eff[valid] = (prefactor * dfdt[valid] / f_binned[valid]**(11.0/3.0))**(3.0/5.0)
M_eff_Msun = M_eff / Msun

print(f"{'t(s)':>8} {'f (Hz)':>9} {'df/dt (Hz/s)':>13} {'M_eff (Msun)':>14} {'M_eff/65':>10}")
for ti, fi, di, mi in zip(t_binned[valid], f_binned[valid], dfdt[valid], M_eff_Msun[valid]):
    print(f"{ti:8.4f} {fi:9.1f} {di:13.1f} {mi:14.2f} {mi/65.0:10.3f}")

if valid.sum() >= 3:
    slope, intercept, r_value, p_value, std_err = linregress(f_binned[valid], M_eff_Msun[valid])
    print(f"\nTrend: slope={slope:.5f} Msun/Hz, r^2={r_value**2:.3f}, p={p_value:.4f}, n={valid.sum()}")
    if p_value < 0.05 and slope > 0:
        print("-> REAL, SIGNIFICANT RISING TREND: consistent with growing enclosed mass.")
    elif p_value < 0.05 and slope < 0:
        print("-> REAL, SIGNIFICANT FALLING TREND: opposite of enclosed-mass-growth prediction.")
    else:
        print("-> No significant trend: consistent with a flat, fixed total mass.")
    print(f"\nMedian M_eff: {np.nanmedian(M_eff_Msun):.2f} Msun (compare to known 65 Msun total)")
else:
    print("Not enough valid points after binning for a trend test.")
