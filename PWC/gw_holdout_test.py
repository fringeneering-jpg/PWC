import numpy as np
import h5py
from scipy import signal
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fs = 4096.0
trigger_gps = 1126259462.4
file_start_gps = 1126259447

with h5py.File('GW150914_H1_32s_4kHz.hdf5','r') as f:
    h1_raw = f['strain']['Strain'][:]

t_full = file_start_gps + np.arange(len(h1_raw))/fs
t_rel = t_full - trigger_gps   # seconds relative to trigger

# --- PSD from off-source portion of this same segment (away from merger) ---
off_mask = (t_rel < -2.0) | (t_rel > 5.0)
off_data = h1_raw[off_mask]
freqs_psd, psd = signal.welch(off_data, fs=fs, nperseg=int(fs*4), noverlap=int(fs*2))

# --- Whiten via FFT division by ASD, then bandpass ---
def whiten(strain, psd_freqs, psd_vals, fs):
    N = len(strain)
    freqs = np.fft.rfftfreq(N, d=1.0/fs)
    asd_interp = np.sqrt(np.interp(freqs, psd_freqs, psd_vals))
    strain_fft = np.fft.rfft(strain * signal.windows.tukey(N, 0.1))
    white_fft = strain_fft / asd_interp
    white_fft[0] = 0
    white = np.fft.irfft(white_fft, n=N) * np.sqrt(fs)/2
    return white

h1_white = whiten(h1_raw, freqs_psd, psd, fs)
sos = signal.butter(4, [20, 300], btype='bandpass', fs=fs, output='sos')
h1_clean = signal.sosfiltfilt(sos, h1_white)

# --- Spectrogram around merger ---
seg_mask = (t_rel >= -0.2) & (t_rel <= 0.15)
seg = h1_clean[seg_mask]
t_seg = t_rel[seg_mask]

nperseg = 128
noverlap = 124
f_spec, t_spec_rel, Sxx = signal.spectrogram(seg, fs=fs, nperseg=nperseg, noverlap=noverlap, window='hann')
t_spec = t_seg[0] + t_spec_rel

fband = (f_spec >= 20) & (f_spec <= 300)
f_spec_b = f_spec[fband]
Sxx_b = Sxx[fband, :]

# --- MAD-based robust ridge extraction ---
baseline_mask = (t_spec >= -0.2) & (t_spec < -0.08)
baseline_power = Sxx_b[:, baseline_mask]
noise_floor = np.median(baseline_power)
mad = np.median(np.abs(baseline_power - noise_floor))
thresh = noise_floor + 3.0*(1.4826*mad)

chirp_mask = (t_spec >= -0.06) & (t_spec <= 0.05)
c_times = t_spec[chirp_mask]
c_power = Sxx_b[:, chirp_mask]

ridge_idx = np.argmax(c_power, axis=0)
peak_power = np.max(c_power, axis=0)
f_ridge_raw = f_spec_b[ridge_idx]

valid = peak_power > thresh
rt = c_times[valid]
rf = f_ridge_raw[valid]

# enforce rough monotonic increase (strip obvious noise jumps)
keep = [0]
last_f = rf[0]
for i in range(1, len(rf)):
    if rf[i] >= last_f - 15:  # allow small negative jitter, reject big drops
        keep.append(i)
        last_f = max(last_f, rf[i])
keep = np.array(keep)
rt_clean, rf_clean = rt[keep], rf[keep]

print(f"Extracted ridge: {len(rt_clean)} nodes, {rf_clean.min():.1f}-{rf_clean.max():.1f} Hz, "
      f"t=[{rt_clean.min():.4f}, {rt_clean.max():.4f}] s relative to trigger")

# --- Train/holdout split: fit on first 65%, predict withheld last 35% ---
n_total = len(rt_clean)
n_train = int(n_total*0.65)
t_train, f_train = rt_clean[:n_train], rf_clean[:n_train]
t_hold, f_hold = rt_clean[n_train:], rf_clean[n_train:]
print(f"Train: {n_train} nodes (t up to {t_train[-1]:.4f}s), Holdout: {n_total-n_train} nodes")

# --- Bounded model: df/dt = kappa * f^alpha * [1 - (f/f_max)^beta] ---
def bounded_rhs(f, kappa, alpha, fmax, beta):
    ratio = np.clip(f/fmax, 0, 0.9999)
    return kappa * (f**alpha) * (1 - ratio**beta)

def integrate_model(params, t_eval, t0, f0):
    log_kappa, alpha, fmax, beta = params
    kappa = np.exp(log_kappa)
    from scipy.integrate import solve_ivp
    sol = solve_ivp(lambda t, y: bounded_rhs(y[0], kappa, alpha, fmax, beta),
                     (t0, t_eval[-1]), [f0], t_eval=t_eval, method='RK45', max_step=0.0005)
    return sol.y[0] if sol.success else np.full_like(t_eval, np.nan)

def residuals(params, t_train, f_train, t0, f0):
    pred = integrate_model(params, t_train, t0, f0)
    if np.any(np.isnan(pred)):
        return np.full_like(f_train, 1e3)
    return pred - f_train

t0, f0 = t_train[0], f_train[0]
x0 = [np.log(5e-4), 2.7, 260.0, 2.0]
res = least_squares(residuals, x0, args=(t_train, f_train, t0, f0),
                     bounds=([np.log(1e-8), 1.0, 200.0, 0.5], [np.log(1e2), 6.0, 400.0, 8.0]),
                     loss='soft_l1', f_scale=3.0)

kappa_fit = np.exp(res.x[0]); alpha_fit, fmax_fit, beta_fit = res.x[1], res.x[2], res.x[3]
print(f"\nFitted on TRAIN data only: kappa={kappa_fit:.4e}, alpha={alpha_fit:.3f}, "
      f"f_max={fmax_fit:.1f} Hz, beta={beta_fit:.3f}")

# --- Predict on full range (including withheld holdout) blind ---
t_all_eval = rt_clean
f_pred_all = integrate_model(res.x, t_all_eval, t0, f0)

train_rmse = np.sqrt(np.nanmean((f_pred_all[:n_train] - f_train)**2))
if len(f_hold) > 0 and not np.any(np.isnan(f_pred_all[n_train:])):
    hold_rmse = np.sqrt(np.mean((f_pred_all[n_train:] - f_hold)**2))
    hold_bias = np.mean(f_pred_all[n_train:] - f_hold)
else:
    hold_rmse, hold_bias = np.nan, np.nan

print(f"\nTRAIN RMSE: {train_rmse:.2f} Hz")
print(f"HOLDOUT RMSE (blind prediction vs withheld real data): {hold_rmse:.2f} Hz")
print(f"HOLDOUT bias (mean predicted - actual): {hold_bias:+.2f} Hz")

# unbounded comparison (alpha only, beta->0 effectively i.e. no f_max term) for reference
def unbounded_rhs(f, kappa, alpha):
    return kappa*(f**alpha)
def integrate_unbounded(params, t_eval, t0, f0):
    log_kappa, alpha = params
    kappa = np.exp(log_kappa)
    from scipy.integrate import solve_ivp
    sol = solve_ivp(lambda t,y: unbounded_rhs(y[0], kappa, alpha), (t0, t_eval[-1]), [f0],
                     t_eval=t_eval, method='RK45', max_step=0.0005)
    return sol.y[0] if sol.success else np.full_like(t_eval, np.nan)
def resid_unb(params, t_train, f_train, t0, f0):
    pred = integrate_unbounded(params, t_train, t0, f0)
    if np.any(np.isnan(pred)): return np.full_like(f_train, 1e3)
    return pred - f_train
res_unb = least_squares(resid_unb, [np.log(5e-4), 2.7], args=(t_train, f_train, t0, f0),
                         bounds=([np.log(1e-8),1.0],[np.log(1e2),6.0]), loss='soft_l1', f_scale=3.0)
f_pred_unb_all = integrate_unbounded(res_unb.x, t_all_eval, t0, f0)
if len(f_hold)>0 and not np.any(np.isnan(f_pred_unb_all[n_train:])):
    hold_rmse_unb = np.sqrt(np.mean((f_pred_unb_all[n_train:]-f_hold)**2))
else:
    hold_rmse_unb = np.nan
print(f"\n[Comparison] Unbounded power-law (no f_max term) HOLDOUT RMSE: {hold_rmse_unb:.2f} Hz")

# --- Plot ---
fig, ax = plt.subplots(figsize=(10,6))
ax.plot(rt_clean, rf_clean, 'o', color='gold', ms=5, mec='black', label='Real extracted ridge (H1, GW150914)')
ax.plot(t_train, f_train, 'o', color='green', ms=3, alpha=0.5, label='(training subset)')
ax.plot(t_all_eval, f_pred_all, '-', color='blue', lw=2, label=f'Bounded model prediction (fit on train only), f_max={fmax_fit:.0f}Hz')
ax.plot(t_all_eval, f_pred_unb_all, '--', color='red', lw=1.5, alpha=0.7, label='Unbounded power-law prediction (fit on train only)')
ax.axvline(t_train[-1], color='gray', ls=':', label='train/holdout boundary')
ax.set_xlabel('Time relative to trigger (s)')
ax.set_ylabel('Ridge frequency (Hz)')
ax.set_title('GW150914 Bounded-Model Holdout Test (real GWOSC H1 data)')
ax.legend(loc='upper left', fontsize=8)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('pwc_falsification_output/gw_holdout_test.png', dpi=130)
print("\nPlot saved to pwc_falsification_output/gw_holdout_test.png")
