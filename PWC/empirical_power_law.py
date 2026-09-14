import warnings
import numpy as np
from gwpy.timeseries import TimeSeries
from scipy.optimize import curve_fit
warnings.filterwarnings('ignore')

trigger_time = 1126259462.4
duration, sample_rate = 4.0, 2048
f_min, f_max = 20.0, 300.0

# --- Use a WIDER pre-merger window than the final-sliver one that failed
# earlier -- go further back in the inspiral where the chirp is slower and
# smoother, giving a real, usable derivative instead of merger-edge noise ---
event_strain = TimeSeries.fetch_open_data('H1', trigger_time-duration/2, trigger_time+duration/2, cache=True).resample(sample_rate)
q_outseg = (trigger_time+0.15, trigger_time+0.45)
hq = event_strain.q_transform(frange=(f_min, f_max), qrange=(4,64), outseg=q_outseg)
hq_times, hq_freqs, hq_matrix = hq.times.value, hq.frequencies.value, hq.value

chirp_start, chirp_end = trigger_time+0.20, trigger_time+0.42
c_mask = (hq_times >= chirp_start) & (hq_times <= chirp_end)
c_times, c_power = hq_times[c_mask], hq_matrix[c_mask, :]
baseline_mask = (hq_times >= trigger_time+0.15) & (hq_times < trigger_time+0.20)
baseline = hq_matrix[baseline_mask, :]
noise_floor = np.median(baseline)
mad = np.median(np.abs(baseline - noise_floor))
thresh = noise_floor + 2.5*(1.4826*mad)
r_idx = np.argmax(c_power, axis=1)
peak_powers = np.max(c_power, axis=1)
v_mask = peak_powers > thresh
rt_clean = (c_times[v_mask] - trigger_time).astype(np.float64)
rf_clean = hq_freqs[r_idx[v_mask]].astype(np.float64)
order = np.argsort(rt_clean)
t_full, f_full = rt_clean[order], rf_clean[order]
print(f"Ridge: {len(t_full)} nodes, {f_full.min():.1f}-{f_full.max():.1f} Hz, "
      f"t=[{t_full.min():.4f},{t_full.max():.4f}]s over {t_full.max()-t_full.min():.4f}s\n")

# --- Bin onto a coarser grid to kill quantization jitter, wide enough window this time ---
n_bins = 25
bin_edges = np.linspace(t_full[0], t_full[-1], n_bins+1)
t_b, f_b = [], []
for i in range(n_bins):
    m = (t_full >= bin_edges[i]) & (t_full < bin_edges[i+1])
    if m.sum() > 0:
        t_b.append(np.mean(t_full[m])); f_b.append(np.mean(f_full[m]))
t_b, f_b = np.array(t_b), np.array(f_b)
dfdt = np.gradient(f_b, t_b)

valid = (dfdt > 0) & (f_b > 0)
print(f"Binned to {len(t_b)} points, {valid.sum()} with positive df/dt\n")

# --- PURE EMPIRICAL FIT: log(df/dt) = n*log(f) + log(kappa) ---
# No formula assumed for either side -- this is just "what power law does
# the real measured data itself show," full stop.
logf = np.log(f_b[valid])
logdfdt = np.log(dfdt[valid])
n_empirical, log_kappa = np.polyfit(logf, logdfdt, 1)
kappa_empirical = np.exp(log_kappa)

print(f"{'f (Hz)':>10} {'df/dt (Hz/s)':>14}")
for fi, di in zip(f_b[valid], dfdt[valid]):
    print(f"{fi:10.1f} {di:14.1f}")

print(f"\n=== PURE EMPIRICAL RESULT, NO THEORY ASSUMED ON EITHER SIDE ===")
print(f"Measured power-law exponent (df/dt proportional to f^n):  n = {n_empirical:.3f}")
print(f"Measured kappa (rate coefficient):                        kappa = {kappa_empirical:.4e}")
print(f"\nGR's prediction for this exponent (quadrupole formula):    n = 11/3 = {11/3:.3f}")
print(f"Difference from GR's predicted exponent:                   {n_empirical - 11/3:+.3f}")
if abs(n_empirical - 11/3) < 0.3:
    print("-> Measured exponent is CLOSE to GR's 11/3 prediction.")
else:
    print("-> Measured exponent DIFFERS meaningfully from GR's 11/3 prediction -- real signal, not assumed.")
