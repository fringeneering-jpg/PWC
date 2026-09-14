# =====================================================================
# INDEPENDENT PROPAGATION/RELAXATION TIMESCALE FROM REAL GW150914 DATA
# Goal: extract a real post-merger decay timescale tau directly from the
# whitened strain envelope (Hilbert transform), completely independent
# of any mass fit, chirp-mass formula, or ridge-frequency tracking.
# This tau is the empirical input needed for c_relief = R / tau.
# Uses the SAME whitening pipeline already validated tonight (gw_holdout_test.py)
# so no new whitening bugs are introduced.
# =====================================================================
import numpy as np
import h5py
from scipy import signal
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fs = 4096.0
trigger_gps = 1126259462.4
file_start_gps = 1126259447

def load_and_whiten(fname):
    with h5py.File(fname, 'r') as f:
        raw = f['strain']['Strain'][:]
    t_full = file_start_gps + np.arange(len(raw))/fs
    t_rel = t_full - trigger_gps
    off_mask = (t_rel < -2.0) | (t_rel > 5.0)
    off_data = raw[off_mask]
    freqs_psd, psd = signal.welch(off_data, fs=fs, nperseg=int(fs*4), noverlap=int(fs*2))

    def whiten(strain, psd_freqs, psd_vals, fs):
        N = len(strain)
        freqs = np.fft.rfftfreq(N, d=1.0/fs)
        asd_interp = np.sqrt(np.interp(freqs, psd_freqs, psd_vals))
        strain_fft = np.fft.rfft(strain * signal.windows.tukey(N, 0.1))
        white_fft = strain_fft / asd_interp
        white_fft[0] = 0
        white = np.fft.irfft(white_fft, n=N) * np.sqrt(fs)/2
        return white

    white = whiten(raw, freqs_psd, psd, fs)
    sos = signal.butter(4, [20, 300], btype='bandpass', fs=fs, output='sos')
    clean = signal.sosfiltfilt(sos, white)
    return t_rel, clean

t_rel_h1, h1_clean = load_and_whiten('GW150914_H1_32s_4kHz.hdf5')
t_rel_l1, l1_clean = load_and_whiten('GW150914_L1_32s_4kHz.hdf5')

def envelope_and_peak(t_rel, clean, label):
    seg_mask = (t_rel >= -0.05) & (t_rel <= 0.10)
    t_seg = t_rel[seg_mask]
    x_seg = clean[seg_mask]
    analytic = signal.hilbert(x_seg)
    env = np.abs(analytic)
    peak_idx = np.argmax(env)
    t_peak = t_seg[peak_idx]
    print(f"{label}: peak envelope amplitude at t={t_peak:.5f} s relative to trigger, "
          f"amplitude={env[peak_idx]:.3f} (whitened units)")
    return t_seg, env, t_peak, peak_idx

t_seg_h1, env_h1, t_peak_h1, pidx_h1 = envelope_and_peak(t_rel_h1, h1_clean, "H1")
t_seg_l1, env_l1, t_peak_l1, pidx_l1 = envelope_and_peak(t_rel_l1, l1_clean, "L1")

def fit_decay(t_seg, env, peak_idx, label, fit_window=0.030):
    t_post = t_seg[peak_idx:]
    env_post = env[peak_idx:]
    mask = (t_post - t_post[0]) <= fit_window
    t_fit = t_post[mask] - t_post[0]
    e_fit = env_post[mask]
    e_fit = np.maximum(e_fit, 1e-6)

    def model(t, A, tau, C):
        return A * np.exp(-t/tau) + C

    try:
        popt, pcov = curve_fit(model, t_fit, e_fit,
                                p0=[e_fit[0], 0.004, np.median(e_fit[-5:])],
                                bounds=([0, 0.0002, 0], [1e4, 0.5, 1e4]))
        A, tau, C = popt
        perr = np.sqrt(np.diag(pcov))
        print(f"{label}: fitted decay tau = {tau*1000:.3f} +/- {perr[1]*1000:.3f} ms "
              f"(A={A:.3f}, C={C:.3f})")
        return t_fit, e_fit, model(t_fit, *popt), tau, perr[1]
    except Exception as ex:
        print(f"{label}: fit FAILED -- {ex}")
        return t_fit, e_fit, None, None, None

t_fit_h1, e_fit_h1, model_h1, tau_h1, tau_h1_err = fit_decay(t_seg_h1, env_h1, pidx_h1, "H1")
t_fit_l1, e_fit_l1, model_l1, tau_l1, tau_l1_err = fit_decay(t_seg_l1, env_l1, pidx_l1, "L1")

print()
if tau_h1 and tau_l1:
    tau_mean = 0.5*(tau_h1+tau_l1)
    print(f"=== REAL, DATA-DERIVED DECAY TIMESCALE (independent of any mass fit) ===")
    print(f"tau (H1) = {tau_h1*1000:.3f} ms, tau (L1) = {tau_l1*1000:.3f} ms")
    print(f"tau (mean) = {tau_mean*1000:.3f} ms")

    print()
    print("=== IMPLIED c_relief = R / tau FOR CANDIDATE RADII (from earlier K-scan family) ===")
    for R_km, K_val, M_val in [(38.1, 4.0e14, 15.37), (44.5, 6.0e14, 28.23), (50.5, 7.0e14, 35.58)]:
        R_m = R_km*1000
        c_relief = R_m / tau_mean
        K_implied = c_relief**2
        print(f"  R={R_km} km (K={K_val:.1e}, M={M_val} Msun) -> c_relief={c_relief:.4e} m/s, "
              f"implied K=c_relief^2={K_implied:.4e} m^2/s^2 (vs scan K={K_val:.1e})")

# --- Plot ---
fig, axes = plt.subplots(1, 2, figsize=(12,5))
for ax, t_seg, env, t_fit, e_fit, model, tau, label in [
    (axes[0], t_seg_h1, env_h1, t_fit_h1, e_fit_h1, model_h1, tau_h1, "H1"),
    (axes[1], t_seg_l1, env_l1, t_fit_l1, e_fit_l1, model, tau_l1, "L1") if False else (axes[1], t_seg_l1, env_l1, t_fit_l1, e_fit_l1, model_l1, tau_l1, "L1"),
]:
    ax.plot(t_seg, env, color='navy', lw=1, label='whitened envelope (Hilbert)')
    if model is not None:
        ax.plot(t_fit + (t_seg[np.argmax(env)]), model, color='orange', lw=2,
                label=f'exp decay fit, tau={tau*1000:.2f} ms')
    ax.axvline(t_seg[np.argmax(env)], color='gray', ls='--', alpha=0.5)
    ax.set_xlabel('t relative to trigger (s)')
    ax.set_ylabel('whitened envelope amplitude')
    ax.set_title(f'{label} post-merger envelope decay')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('pwc_falsification_output/ringdown_timescale.png', dpi=130)
print("\nPlot saved.")
