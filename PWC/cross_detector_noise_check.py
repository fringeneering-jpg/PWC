import warnings
import numpy as np
from gwpy.timeseries import TimeSeries
warnings.filterwarnings('ignore')

trigger_time = 1126259462.4
duration, sample_rate = 4.0, 2048
f_min, f_max = 20.0, 300.0

def extract_ridge(det, chirp_start_off, chirp_end_off, baseline_start_off, baseline_end_off):
    event_strain = TimeSeries.fetch_open_data(det, trigger_time-duration/2, trigger_time+duration/2, cache=True).resample(sample_rate)
    bg_strain = TimeSeries.fetch_open_data(det, trigger_time-duration/2-128.0, trigger_time-duration/2, sample_rate=4096, cache=True).resample(sample_rate)
    psd_gwpy = bg_strain.psd(fftlength=duration, overlap=duration/2, method="median")
    asd_gwpy = psd_gwpy**0.5
    clean_strain = event_strain.whiten(asd=asd_gwpy).bandpass(f_min, f_max)

    q_outseg = (trigger_time+0.25, trigger_time+0.50)
    hq = clean_strain.q_transform(frange=(f_min, f_max), qrange=(4,64), outseg=q_outseg)
    hq_times, hq_freqs, hq_matrix = hq.times.value, hq.frequencies.value, hq.value

    chirp_start, chirp_end = trigger_time+chirp_start_off, trigger_time+chirp_end_off
    c_mask = (hq_times >= chirp_start) & (hq_times <= chirp_end)
    c_times, c_power = hq_times[c_mask], hq_matrix[c_mask, :]
    baseline_mask = (hq_times >= trigger_time+baseline_start_off) & (hq_times < trigger_time+baseline_end_off)
    baseline = hq_matrix[baseline_mask, :]
    noise_floor = np.median(baseline)
    mad = np.median(np.abs(baseline - noise_floor))
    thresh = noise_floor + 2.5*(1.4826*mad)
    r_idx = np.argmax(c_power, axis=1)
    peak_powers = np.max(c_power, axis=1)
    v_mask = peak_powers > thresh
    rt = (c_times[v_mask] - trigger_time).astype(np.float64)
    rf = hq_freqs[r_idx[v_mask]].astype(np.float64)
    order = np.argsort(rt)
    return rt[order], rf[order]

print("--> Extracting H1 near-merger ridge (same region as the noisy n=0.95 measurement)...")
t_h1, f_h1 = extract_ridge('H1', 0.35, 0.43, 0.25, 0.34)
print(f"    H1: {len(t_h1)} nodes, {f_h1.min():.1f}-{f_h1.max():.1f} Hz")

print("--> Extracting L1 near-merger ridge (same region, same event)...")
t_l1, f_l1 = extract_ridge('L1', 0.35, 0.43, 0.25, 0.34)
print(f"    L1: {len(t_l1)} nodes, {f_l1.min():.1f}-{f_l1.max():.1f} Hz")

# Compute residuals from a smooth monotonic trend in EACH detector separately
def residual_from_smooth(t, f):
    # simple monotonic running-max as the "smooth expected" trend, residual = actual - smooth
    smooth = np.maximum.accumulate(f)
    return f - smooth

resid_h1 = residual_from_smooth(t_h1, f_h1)
resid_l1 = residual_from_smooth(t_l1, f_l1)

print(f"\nH1 residual (jumpiness) stats: mean={np.mean(np.abs(resid_h1)):.2f} Hz, std={np.std(resid_h1):.2f} Hz")
print(f"L1 residual (jumpiness) stats: mean={np.mean(np.abs(resid_l1)):.2f} Hz, std={np.std(resid_l1):.2f} Hz")

# Interpolate both onto a common time grid (accounting for ~7ms light travel offset
# doesn't matter much for this correlation check at this resolution) and correlate
from scipy.interpolate import interp1d
common_t = np.linspace(max(t_h1.min(), t_l1.min()), min(t_h1.max(), t_l1.max()), 50)
interp_h1 = interp1d(t_h1, resid_h1, bounds_error=False, fill_value=np.nan)
interp_l1 = interp1d(t_l1, resid_l1, bounds_error=False, fill_value=np.nan)
r_h1_common = interp_h1(common_t)
r_l1_common = interp_l1(common_t)
valid = ~np.isnan(r_h1_common) & ~np.isnan(r_l1_common)

if valid.sum() >= 5:
    corr = np.corrcoef(r_h1_common[valid], r_l1_common[valid])[0,1]
    print(f"\n=== CROSS-DETECTOR CORRELATION OF THE 'JUMPINESS' ===")
    print(f"Correlation coefficient between H1 and L1 residual noise: {corr:.3f}")
    print(f"(n={valid.sum()} common time points)")
    if abs(corr) > 0.5:
        print("-> STRONG correlation: the jumpiness matches between independent detectors.")
        print("   Consistent with a REAL physical feature of the event, not instrument noise.")
    elif abs(corr) > 0.25:
        print("-> WEAK/moderate correlation: ambiguous, not a clean answer either way.")
    else:
        print("-> NO meaningful correlation: H1 and L1 jumpiness don't match each other.")
        print("   Consistent with each detector's own independent measurement noise,")
        print("   NOT a real shared physical feature of the merger.")
else:
    print("Not enough overlapping valid points for a correlation test.")
