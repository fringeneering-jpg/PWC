import warnings
import numpy as np
from gwpy.timeseries import TimeSeries
from scipy.interpolate import interp1d
warnings.filterwarnings('ignore')

trigger_time = 1126259462.4
duration, sample_rate = 4.0, 2048
f_min, f_max = 20.0, 300.0

def get_clean_strain(det, center_gps):
    event_strain = TimeSeries.fetch_open_data(det, center_gps-duration/2, center_gps+duration/2, cache=True).resample(sample_rate)
    bg_strain = TimeSeries.fetch_open_data(det, center_gps-duration/2-128.0, center_gps-duration/2, sample_rate=4096, cache=True).resample(sample_rate)
    psd_gwpy = bg_strain.psd(fftlength=duration, overlap=duration/2, method="median")
    asd_gwpy = psd_gwpy**0.5
    return event_strain.whiten(asd=asd_gwpy).bandpass(f_min, f_max)

def extract_ridge_from_strain(clean_strain, center_gps, chirp_start_off, chirp_end_off, baseline_start_off, baseline_end_off):
    q_outseg = (center_gps+0.25, center_gps+0.50)
    hq = clean_strain.q_transform(frange=(f_min, f_max), qrange=(4,64), outseg=q_outseg)
    hq_times, hq_freqs, hq_matrix = hq.times.value, hq.frequencies.value, hq.value
    chirp_start, chirp_end = center_gps+chirp_start_off, center_gps+chirp_end_off
    c_mask = (hq_times >= chirp_start) & (hq_times <= chirp_end)
    c_times, c_power = hq_times[c_mask], hq_matrix[c_mask, :]
    baseline_mask = (hq_times >= center_gps+baseline_start_off) & (hq_times < center_gps+baseline_end_off)
    baseline = hq_matrix[baseline_mask, :]
    noise_floor = np.median(baseline)
    mad = np.median(np.abs(baseline - noise_floor))
    thresh = noise_floor + 2.5*(1.4826*mad)
    r_idx = np.argmax(c_power, axis=1)
    peak_powers = np.max(c_power, axis=1)
    v_mask = peak_powers > thresh
    rt = (c_times[v_mask] - center_gps).astype(np.float64)
    rf = hq_freqs[r_idx[v_mask]].astype(np.float64)
    order = np.argsort(rt)
    return rt[order], rf[order]

def residual_from_smooth(t, f):
    smooth = np.maximum.accumulate(f)
    return f - smooth

def cross_corr(det1_strain, det2_strain, center_gps):
    t1, f1 = extract_ridge_from_strain(det1_strain, center_gps, 0.35, 0.43, 0.25, 0.34)
    t2, f2 = extract_ridge_from_strain(det2_strain, center_gps, 0.35, 0.43, 0.25, 0.34)
    if len(t1) < 5 or len(t2) < 5:
        return np.nan
    r1, r2 = residual_from_smooth(t1, f1), residual_from_smooth(t2, f2)
    common_t = np.linspace(max(t1.min(), t2.min()), min(t1.max(), t2.max()), 50)
    i1 = interp1d(t1, r1, bounds_error=False, fill_value=np.nan)
    i2 = interp1d(t2, r2, bounds_error=False, fill_value=np.nan)
    v1, v2 = i1(common_t), i2(common_t)
    valid = ~np.isnan(v1) & ~np.isnan(v2)
    if valid.sum() < 5:
        return np.nan
    return np.corrcoef(v1[valid], v2[valid])[0,1]

# Off-source windows: shift the "center" time by various offsets, well clear
# of the real event, reusing the same 4s +/- window fetches for PSD estimation each time
offsets = [-40, -30, -20, -10, 10, 20, 30, 40]  # seconds away from the real trigger
print("Computing off-source null correlations (same pipeline, non-event windows)...\n")
null_corrs = []
for off in offsets:
    fake_center = trigger_time + off
    try:
        h1_strain = get_clean_strain('H1', fake_center)
        l1_strain = get_clean_strain('L1', fake_center)
        r = cross_corr(h1_strain, l1_strain, fake_center)
        if not np.isnan(r):
            null_corrs.append(r)
            print(f"  offset {off:+4d}s: r = {r:+.3f}")
        else:
            print(f"  offset {off:+4d}s: insufficient ridge points, skipped")
    except Exception as e:
        print(f"  offset {off:+4d}s: failed ({e})")

null_corrs = np.array(null_corrs)
real_r = 0.625
print(f"\n=== NULL DISTRIBUTION RESULT ===")
print(f"Off-source correlations: {null_corrs}")
print(f"Null mean: {np.mean(np.abs(null_corrs)):.3f}, null std: {np.std(np.abs(null_corrs)):.3f}, n={len(null_corrs)}")
p_emp = (1 + np.sum(np.abs(null_corrs) >= abs(real_r))) / (1 + len(null_corrs))
print(f"Real event r={real_r}")
print(f"Empirical p-value (fraction of off-source windows with |r| >= 0.625): {p_emp:.3f}")
if p_emp < 0.05:
    print("-> Real event correlation is genuinely unusual compared to off-source noise.")
else:
    print("-> Real event correlation is NOT clearly distinguishable from what off-source")
    print("   noise windows commonly produce with this same pipeline -- 0.625 may not be special.")
