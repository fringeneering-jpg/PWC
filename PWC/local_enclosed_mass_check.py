import numpy as np
import h5py
from scipy import signal
from scipy.signal import savgol_filter
from scipy.stats import linregress

fs = 4096.0
trigger_gps = 1126259462.4
file_start_gps = 1126259447

with h5py.File('GW150914_H1_32s_4kHz.hdf5','r') as f:
    h1_raw = f['strain']['Strain'][:]
t_full = file_start_gps + np.arange(len(h1_raw))/fs
t_rel = t_full - trigger_gps

off_mask = (t_rel < -2.0) | (t_rel > 5.0)
freqs_psd, psd = signal.welch(h1_raw[off_mask], fs=fs, nperseg=int(fs*4), noverlap=int(fs*2))

def whiten(strain, psd_freqs, psd_vals, fs):
    N = len(strain)
    freqs = np.fft.rfftfreq(N, d=1.0/fs)
    asd_interp = np.sqrt(np.interp(freqs, psd_freqs, psd_vals))
    strain_fft = np.fft.rfft(strain * signal.windows.tukey(N, 0.1))
    white_fft = strain_fft / asd_interp
    white_fft[0] = 0
    return np.fft.irfft(white_fft, n=N) * np.sqrt(fs)/2

h1_white = whiten(h1_raw, freqs_psd, psd, fs)
sos = signal.butter(4, [20, 300], btype='bandpass', fs=fs, output='sos')
h1_clean = signal.sosfiltfilt(sos, h1_white)

seg_mask = (t_rel >= -0.2) & (t_rel <= 0.15)
seg, t_seg = h1_clean[seg_mask], t_rel[seg_mask]
f_spec, t_spec_rel, Sxx = signal.spectrogram(seg, fs=fs, nperseg=128, noverlap=124, window='hann')
t_spec = t_seg[0] + t_spec_rel
fband = (f_spec >= 20) & (f_spec <= 300)
f_spec_b, Sxx_b = f_spec[fband], Sxx[fband, :]

baseline_mask = (t_spec >= -0.2) & (t_spec < -0.08)
noise_floor = np.median(Sxx_b[:, baseline_mask])
mad = np.median(np.abs(Sxx_b[:, baseline_mask] - noise_floor))
thresh = noise_floor + 3.0*(1.4826*mad)

chirp_mask = (t_spec >= -0.06) & (t_spec <= 0.05)
c_times, c_power = t_spec[chirp_mask], Sxx_b[:, chirp_mask]
ridge_idx = np.argmax(c_power, axis=0)
peak_power = np.max(c_power, axis=0)
valid = peak_power > thresh
rt, rf = c_times[valid], f_spec_b[ridge_idx][valid]

order = np.argsort(rt)
t, f = rt[order], rf[order]
print(f"Local (coarse) ridge: {len(t)} points, {f.min():.1f}-{f.max():.1f} Hz")
print("CAVEAT: this is the same coarse fixed-window spectrogram flagged earlier tonight")
print("(~32 Hz native resolution), NOT the proper gwpy Q-transform. Treat as preliminary only.\n")

window = min(11, len(t) - (1 - len(t) % 2))
if window < 5: window = 5
poly_order = 3
f_smooth = savgol_filter(f, window_length=window, polyorder=poly_order)
dfdt = savgol_filter(f, window_length=window, polyorder=poly_order, deriv=1, delta=np.median(np.diff(t)))

G, c_light, Msun = 6.674e-11, 2.998e8, 1.989e30
prefactor = (5.0/96.0) * c_light**5 / (np.pi**(8.0/3.0) * G**(5.0/3.0))
valid2 = (dfdt > 0) & (f_smooth > 0)
M_eff = np.full_like(f_smooth, np.nan)
M_eff[valid2] = (prefactor * dfdt[valid2] / f_smooth[valid2]**(11.0/3.0))**(3.0/5.0)
M_eff_Msun = M_eff / Msun

print(f"{'f (Hz)':>10} {'M_eff (Msun)':>14} {'M_eff/65':>10}")
for fi, mi in zip(f_smooth[valid2], M_eff_Msun[valid2]):
    print(f"{fi:10.1f} {mi:14.2f} {mi/65.0:10.3f}")

slope, intercept, r_value, p_value, std_err = linregress(f_smooth[valid2], M_eff_Msun[valid2])
print(f"\nTrend: slope={slope:.5f} Msun/Hz, r^2={r_value**2:.3f}, p={p_value:.4f}, n={valid2.sum()}")
if p_value < 0.05 and slope > 0:
    print("-> Rising trend, statistically real at p<0.05 (but LOCAL/coarse data -- confirm in Colab)")
elif p_value < 0.05 and slope < 0:
    print("-> Falling trend, statistically real at p<0.05 (opposite of enclosed-mass-growth prediction)")
else:
    print("-> No significant trend detected in this coarse local extraction.")
