# =====================================================================
# ROBUST RINGDOWN EXTRACTION: damped sinusoid fit to whitened strain
# (not just its envelope) -- A*exp(-t/tau)*cos(2*pi*f0*t+phi).
# Uses phase information, far less prone to being fooled by broadband
# noise sitting in the same time window than a raw envelope fit.
# Frozen across all three events -- same code, only file/GPS change.
# =====================================================================
import numpy as np
import h5py
from scipy import signal
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fs = 4096.0

EVENTS = {
    'GW150914': dict(trigger=1126259462.4,
                      h1='GW150914_H1_32s_4kHz.hdf5', l1='GW150914_L1_32s_4kHz.hdf5'),
    'GW151226': dict(trigger=1135136350.6,
                      h1='GW151226_H1_32s_4kHz.hdf5', l1='GW151226_L1_32s_4kHz.hdf5'),
    'GW170814': dict(trigger=1186741861.0,
                      h1='GW170814_H1_32s_4kHz.hdf5', l1='GW170814_L1_32s_4kHz.hdf5'),
}

def get_key_and_data(fname):
    with h5py.File(fname, 'r') as f:
        keys = list(f.keys())
        if 'strain' in keys:
            raw = f['strain']['Strain'][:]
            x0 = None  # GW150914 files use file_start_gps convention instead
        else:
            key = keys[0]
            raw = f[key][:]
            x0 = f[key].attrs['x0']
    return raw, x0

FILE_START_GPS = {
    'GW150914_H1_32s_4kHz.hdf5': 1126259447,
    'GW150914_L1_32s_4kHz.hdf5': 1126259447,
}

def load_and_whiten(fname, trigger_gps):
    raw, x0 = get_key_and_data(fname)
    file_start_gps = x0 if x0 is not None else FILE_START_GPS[fname]
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

def damped_sinusoid(t, A, tau, f0, phi, C):
    return A * np.exp(-t/tau) * np.cos(2*np.pi*f0*t + phi) + C

def fit_ringdown(t_rel, clean, label, fit_window=0.030, search_start=-0.01, search_end=0.03):
    # locate peak via envelope (just for the start-time anchor, not for tau itself)
    seg_mask = (t_rel >= search_start) & (t_rel <= search_end)
    t_seg = t_rel[seg_mask]
    x_seg = clean[seg_mask]
    env = np.abs(signal.hilbert(x_seg))
    peak_idx = np.argmax(env)
    t_peak = t_seg[peak_idx]

    fit_mask = (t_rel >= t_peak) & (t_rel <= t_peak + fit_window)
    t_fit_raw = t_rel[fit_mask]
    x_fit = clean[fit_mask]
    t_fit = t_fit_raw - t_peak

    # initial frequency guess from FFT peak in this window
    N = len(x_fit)
    freqs = np.fft.rfftfreq(N, d=1.0/fs)
    fft_mag = np.abs(np.fft.rfft(x_fit))
    band = (freqs >= 60) & (freqs <= 300)
    f0_guess = freqs[band][np.argmax(fft_mag[band])] if np.any(band) else 150.0

    try:
        popt, pcov = curve_fit(
            damped_sinusoid, t_fit, x_fit,
            p0=[np.max(np.abs(x_fit)), 0.006, f0_guess, 0.0, 0.0],
            bounds=([0, 0.0005, 40, -2*np.pi, -1e3], [1e5, 0.3, 350, 2*np.pi, 1e3]),
            maxfev=20000
        )
        A, tau, f0, phi, C = popt
        perr = np.sqrt(np.diag(pcov))
        print(f"{label}: tau={tau*1000:.3f}+/-{perr[1]*1000:.3f} ms, f0={f0:.1f}+/-{perr[2]:.1f} Hz, "
              f"t_peak={t_peak:.5f}s")
        return t_fit, x_fit, damped_sinusoid(t_fit, *popt), tau, perr[1], f0, perr[2], t_peak
    except Exception as ex:
        print(f"{label}: fit FAILED -- {ex}")
        return t_fit, x_fit, None, None, None, None, None, t_peak

print("=== DAMPED-SINUSOID RINGDOWN FIT, ALL THREE EVENTS, FROZEN PIPELINE ===\n")
results = {}
fig, axes = plt.subplots(3, 2, figsize=(12, 12))
for i, (name, info) in enumerate(EVENTS.items()):
    print(f"--- {name} ---")
    t_rel_h1, h1_clean = load_and_whiten(info['h1'], info['trigger'])
    t_rel_l1, l1_clean = load_and_whiten(info['l1'], info['trigger'])
    t_fit_h1, x_fit_h1, model_h1, tau_h1, tau_h1_err, f0_h1, f0_h1_err, tpk_h1 = fit_ringdown(t_rel_h1, h1_clean, f"{name} H1")
    t_fit_l1, x_fit_l1, model_l1, tau_l1, tau_l1_err, f0_l1, f0_l1_err, tpk_l1 = fit_ringdown(t_rel_l1, l1_clean, f"{name} L1")
    if tau_h1 and tau_l1:
        rel_diff = abs(tau_h1-tau_l1)/(0.5*(tau_h1+tau_l1))*100
        print(f"  cross-detector tau diff: {rel_diff:.1f}%\n")
        results[name] = dict(tau_h1=tau_h1, tau_l1=tau_l1, rel_diff=rel_diff,
                              tau_h1_err=tau_h1_err, tau_l1_err=tau_l1_err,
                              f0_h1=f0_h1, f0_l1=f0_l1)
    else:
        print()

    for j, (t_fit, x_fit, model, tau, label) in enumerate([
        (t_fit_h1, x_fit_h1, model_h1, tau_h1, f"{name} H1"),
        (t_fit_l1, x_fit_l1, model_l1, tau_l1, f"{name} L1"),
    ]):
        ax = axes[i, j]
        ax.plot(t_fit*1000, x_fit, color='navy', lw=0.8, label='whitened strain')
        if model is not None:
            ax.plot(t_fit*1000, model, color='orange', lw=1.5, label=f'damped-sinusoid fit, tau={tau*1000:.2f}ms')
        ax.set_title(label, fontsize=9)
        ax.set_xlabel('ms after peak')
        ax.legend(fontsize=7)
        ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('pwc_falsification_output/damped_sinusoid_ringdown.png', dpi=130)
print("Plot saved.")

print("\n=== SUMMARY ===")
for name, r in results.items():
    print(f"{name}: tau_H1={r['tau_h1']*1000:.2f}+/-{r['tau_h1_err']*1000:.2f}ms, "
          f"tau_L1={r['tau_l1']*1000:.2f}+/-{r['tau_l1_err']*1000:.2f}ms, "
          f"diff={r['rel_diff']:.1f}%, f0_H1={r['f0_h1']:.0f}Hz, f0_L1={r['f0_l1']:.0f}Hz")
