import warnings
import numpy as np
from gwpy.timeseries import TimeSeries
warnings.filterwarnings('ignore')

trigger_time = 1126259462.4
duration, sample_rate = 4.0, 2048
f_min, f_max = 20.0, 300.0

event_strain = TimeSeries.fetch_open_data('H1', trigger_time-duration/2, trigger_time+duration/2, cache=True).resample(sample_rate)
bg_strain = TimeSeries.fetch_open_data('H1', trigger_time-duration/2-128.0, trigger_time-duration/2, sample_rate=4096, cache=True).resample(sample_rate)
psd_gwpy = bg_strain.psd(fftlength=duration, overlap=duration/2, method="median")
asd_gwpy = psd_gwpy**0.5
clean_strain = event_strain.whiten(asd=asd_gwpy).bandpass(f_min, f_max)

q_outseg = (trigger_time+0.05, trigger_time+0.35)
hq = clean_strain.q_transform(frange=(f_min, 150.0), qrange=(8,64), outseg=q_outseg)
hq_times, hq_freqs, hq_matrix = hq.times.value, hq.frequencies.value, hq.value

chirp_start, chirp_end = trigger_time+0.10, trigger_time+0.32
c_mask = (hq_times >= chirp_start) & (hq_times <= chirp_end)
c_times, c_power = hq_times[c_mask], hq_matrix[c_mask, :]
baseline_mask = (hq_times >= trigger_time+0.05) & (hq_times < trigger_time+0.10)
baseline = hq_matrix[baseline_mask, :]
noise_floor = np.median(baseline)
mad = np.median(np.abs(baseline - noise_floor))
thresh = noise_floor + 3.0*(1.4826*mad)
r_idx = np.argmax(c_power, axis=1)
peak_powers = np.max(c_power, axis=1)
v_mask = peak_powers > thresh
rt_clean = (c_times[v_mask] - trigger_time).astype(np.float64)
rf_clean = hq_freqs[r_idx[v_mask]].astype(np.float64)
order = np.argsort(rt_clean)
t_full, f_full = rt_clean[order], rf_clean[order]
print(f"Calm early-inspiral ridge: {len(t_full)} nodes, {f_full.min():.1f}-{f_full.max():.1f} Hz, "
      f"over {t_full.max()-t_full.min():.4f}s\n")

keep = [0]
running_max = f_full[0]
for i in range(1, len(f_full)):
    if f_full[i] >= running_max:
        keep.append(i)
        running_max = f_full[i]
keep = np.array(keep)
t_m, f_m = t_full[keep], f_full[keep]
print(f"After removing physically-impossible frequency drops: {len(t_m)} points\n")

n_bins = 15
bin_edges = np.linspace(t_m[0], t_m[-1], n_bins+1)
t_b, f_b = [], []
for i in range(n_bins):
    m = (t_m >= bin_edges[i]) & (t_m < bin_edges[i+1])
    if m.sum() > 0:
        t_b.append(np.mean(t_m[m])); f_b.append(np.mean(f_m[m]))
t_b, f_b = np.array(t_b), np.array(f_b)
dfdt = np.gradient(f_b, t_b)
valid = (dfdt > 0) & (f_b > 0)
print(f"Binned to {len(t_b)} points, {valid.sum()} with positive df/dt\n")

print(f"{'f (Hz)':>10} {'df/dt (Hz/s)':>14}")
for fi, di in zip(f_b[valid], dfdt[valid]):
    print(f"{fi:10.1f} {di:14.1f}")

if valid.sum() >= 4:
    logf, logdfdt = np.log(f_b[valid]), np.log(dfdt[valid])
    n_emp, log_k = np.polyfit(logf, logdfdt, 1)
    resid = logdfdt - (n_emp*logf + log_k)
    ss_res, ss_tot = np.sum(resid**2), np.sum((logdfdt-np.mean(logdfdt))**2)
    r2 = 1 - ss_res/ss_tot if ss_tot > 0 else float('nan')
    print(f"\n=== EMPIRICAL RESULT ===")
    print(f"Measured exponent n = {n_emp:.3f}  (r^2 of log-log fit = {r2:.3f})")
    print(f"GR prediction: n = 11/3 = {11/3:.3f}")
    print(f"Difference: {n_emp - 11/3:+.3f}")
else:
    print("Still not enough clean points for a reliable fit.")
