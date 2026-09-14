# =====================================================================
# INJECTION-RECOVERY VALIDATION
# Inject KNOWN synthetic damped-sinusoid signals into REAL off-source
# detector noise (already whitened by the same validated pipeline), then
# run the exact same fit_ringdown() used on real events. If the pipeline
# can't recover a known tau reliably at a given SNR, it cannot be trusted
# to measure tau on real merger data at that SNR -- full stop, before any
# physical interpretation (PWC or otherwise).
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

with h5py.File('GW150914_H1_32s_4kHz.hdf5','r') as f:
    h1_raw = f['strain']['Strain'][:]
t_full = file_start_gps + np.arange(len(h1_raw))/fs
t_rel = t_full - trigger_gps

off_mask = (t_rel < -2.0) | (t_rel > 5.0)
off_data = h1_raw[off_mask]
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

h1_white = whiten(h1_raw, freqs_psd, psd, fs)
sos = signal.butter(4, [20, 300], btype='bandpass', fs=fs, output='sos')
h1_clean = signal.sosfiltfilt(sos, h1_white)

# real off-source noise RMS (same units the merger fits operate in)
off_source_noise = h1_clean[off_mask]
noise_rms = np.std(off_source_noise)
print(f"Real off-source whitened+bandpassed noise RMS: {noise_rms:.3f}")

def damped_sinusoid(t, A, tau, f0, phi, C):
    return A * np.exp(-t/tau) * np.cos(2*np.pi*f0*t + phi) + C

def fit_ringdown_on_segment(t_local, x_local, fit_window=0.030):
    env = np.abs(signal.hilbert(x_local))
    peak_idx = np.argmax(env[:int(0.02*fs)])  # look for peak in first 20ms (injection is near start)
    t_peak = t_local[peak_idx]
    fit_mask = (t_local >= t_peak) & (t_local <= t_peak + fit_window)
    t_fit = t_local[fit_mask] - t_peak
    x_fit = x_local[fit_mask]
    N = len(x_fit)
    freqs = np.fft.rfftfreq(N, d=1.0/fs)
    fft_mag = np.abs(np.fft.rfft(x_fit))
    band = (freqs >= 60) & (freqs <= 300)
    f0_guess = freqs[band][np.argmax(fft_mag[band])] if np.any(band) else 250.0
    try:
        popt, pcov = curve_fit(
            damped_sinusoid, t_fit, x_fit,
            p0=[np.max(np.abs(x_fit)), 0.006, f0_guess, 0.0, 0.0],
            bounds=([0, 0.0005, 40, -2*np.pi, -1e3], [1e5, 0.3, 350, 2*np.pi, 1e3]),
            maxfev=20000
        )
        return popt[1]  # tau
    except Exception:
        return np.nan

# --- injection setup ---
TAU_TRUE = 0.005   # 5 ms, known ground truth
F0_TRUE = 250.0    # Hz, known ground truth
rng = np.random.default_rng(42)

# candidate injection start points: many independent off-source windows
n_trials_per_snr = 30
window_len = int(0.1*fs)  # 100 ms segments
off_indices = np.where(off_mask)[0]
valid_starts = off_indices[(off_indices > 0) & (off_indices < len(h1_clean)-window_len-1)]

# real merger peak amplitudes observed tonight (whitened units), for comparison
real_peaks = {'GW150914': 327.2, 'GW151226': 120.3, 'GW170814': 40.0}

print("\n=== INJECTION-RECOVERY TEST ACROSS AMPLITUDES ===")
print(f"True tau = {TAU_TRUE*1000:.1f} ms, true f0 = {F0_TRUE:.0f} Hz\n")
print(f"{'Injected Amp':>14} {'SNR~Amp/RMS':>14} {'n_valid':>8} {'mean tau_rec(ms)':>18} {'std':>8} {'bias vs true(ms)':>18}")

test_amps = [20, 40, 80, 120, 200, 327, 500]
results = []
for amp in test_amps:
    recovered = []
    for trial in range(n_trials_per_snr):
        start_idx = rng.choice(valid_starts)
        seg = h1_clean[start_idx:start_idx+window_len].copy()
        t_local = np.arange(window_len)/fs
        phi_true = rng.uniform(0, 2*np.pi)
        injected_signal = amp * np.exp(-t_local/TAU_TRUE) * np.cos(2*np.pi*F0_TRUE*t_local + phi_true)
        seg_with_signal = seg + injected_signal
        tau_rec = fit_ringdown_on_segment(t_local, seg_with_signal)
        if not np.isnan(tau_rec):
            recovered.append(tau_rec)
    recovered = np.array(recovered)
    if len(recovered) > 0:
        mean_tau = np.mean(recovered)*1000
        std_tau = np.std(recovered)*1000
        bias = mean_tau - TAU_TRUE*1000
    else:
        mean_tau, std_tau, bias = np.nan, np.nan, np.nan
    print(f"{amp:14.0f} {amp/noise_rms:14.2f} {len(recovered):8d} {mean_tau:18.3f} {std_tau:8.3f} {bias:18.3f}")
    results.append((amp, amp/noise_rms, len(recovered), mean_tau, std_tau))

print()
print("=== COMPARISON TO REAL EVENT PEAK AMPLITUDES ===")
for name, peak in real_peaks.items():
    print(f"  {name}: peak whitened amplitude ~{peak:.1f} -> SNR-like ratio ~{peak/noise_rms:.2f}")
