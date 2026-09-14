# =====================================================================
# PWC GW150914 DIAGNOSTIC PIPELINE (consolidated, corrected)
# =====================================================================
# Companion script to PWC.md in this folder.
#
# Built from phase_wave_master_compiler_v2.py (the most-corrected of three
# prior attempts in ~/Downloads), plus two additions that no prior version
# had: the core/gradient mass-conservation solver (Module 0) and the
# df/dt = kappa*f^alpha radiation-loss sandbox (Module 6).
#
# Requires: gwpy, bilby, lalsuite, scipy, numpy, matplotlib
#   pip install gwpy bilby lalsuite scipy numpy matplotlib
# Requires live network access to GWOSC (https://gwosc.org) to fetch H1/L1
# strain. This script has NOT been executed here — run it yourself.
#
# Discipline kept throughout: Modules 0-4 are theory-neutral empirical
# extraction (no GR waveform template, no PWC assumption baked into the
# math). Modules 5-6 are the PWC-specific model layer applied ON TOP of
# those empirical targets. Don't blur the two — see PWC.md section 9-10.
# =====================================================================

import logging
import warnings

import numpy as np
import matplotlib.pyplot as plt
import bilby
from gwpy.timeseries import TimeSeries
from bilby.gw.detector import PowerSpectralDensity
from scipy.signal import correlate, correlation_lags
from scipy.optimize import least_squares, root_scalar
from scipy.integrate import solve_ivp

warnings.filterwarnings("ignore")
bilby.core.utils.logger.setLevel(logging.WARNING)

print("\n" + "=" * 75)
print("     PWC GW150914 PIPELINE: EMPIRICAL EXTRACTION + PWC MODEL LAYER")
print("=" * 75 + "\n")

# --- INITIALIZATION PARAMETERS ---
trigger_time = 1126259462.4
duration = 4.0
sample_rate = 2048
f_min, f_max = 20.0, 300.0

psd_duration = 128.0
psd_start = trigger_time - duration / 2 - psd_duration
psd_end = trigger_time - duration / 2

# =====================================================================
print("--> [0/6] PWC MODEL LAYER: Core/Gradient Mass-Conservation Solve...")
# =====================================================================
# THEORY LAYER, not empirical extraction. See PWC.md section 5.
# M_app = M_core + M_grad, with M_grad = k * M_core**(2/3).
# Solve for the single k that makes core mass conserved across the
# merger (M_core1 + M_core2 = M_core_final) given GW150914's reported
# apparent masses. This k is a CALIBRATION to the known ~3 Msun deficit,
# not an independent prediction -- see PWC.md section 10.

M_app1, M_app2, M_app_final = 36.0, 29.0, 62.0
GRAD_EXP = 2.0 / 3.0


def M_grad(M_core, k, gamma=GRAD_EXP):
    return k * (M_core ** gamma)


def _core_for(M_app, k):
    func = lambda Mc: Mc + M_grad(Mc, k) - M_app
    return root_scalar(func, bracket=[0.1, M_app]).root


def _conservation_residual(k):
    Mc1 = _core_for(M_app1, k)
    Mc2 = _core_for(M_app2, k)
    Mcf = _core_for(M_app_final, k)
    return (Mc1 + Mc2) - Mcf


k_calibrated = root_scalar(_conservation_residual, bracket=[0.01, 10.0]).root
C1_fixed = _core_for(M_app1, k_calibrated)
C2_fixed = _core_for(M_app2, k_calibrated)
Cf_fixed = _core_for(M_app_final, k_calibrated)
G1_fixed = M_grad(C1_fixed, k_calibrated)
G2_fixed = M_grad(C2_fixed, k_calibrated)
Gf_fixed = M_grad(Cf_fixed, k_calibrated)

print(f"      Calibrated k                : {k_calibrated:.10f}")
print(f"      Core masses (1, 2, final)   : {C1_fixed:.3f}, {C2_fixed:.3f}, {Cf_fixed:.3f} Msun")
print(f"      Gradient masses (1,2,final) : {G1_fixed:.3f}, {G2_fixed:.3f}, {Gf_fixed:.3f} Msun")
print(f"      Shed gradient mass          : {(G1_fixed + G2_fixed - Gf_fixed):.3f} Msun (target: 3.000)")

# =====================================================================
print("\n--> [1/6] EMPIRICAL: Calibrating Detectors against Off-Source Data...")
# =====================================================================
ifos = bilby.gw.detector.InterferometerList([])
clean_strains = {}
raw_strains = {}

for det in ("H1", "L1"):
    event_strain = TimeSeries.fetch_open_data(
        det, trigger_time - duration / 2, trigger_time + duration / 2, cache=True
    ).resample(sample_rate)
    raw_strains[det] = event_strain

    ifo = bilby.gw.detector.get_empty_interferometer(det)
    ifo.set_strain_data_from_gwpy_timeseries(event_strain)
    ifo.minimum_frequency = f_min
    ifo.maximum_frequency = f_max
    ifos.append(ifo)
    short_strain_2k = ifo.strain_data.to_gwpy_timeseries()

    bg_strain = TimeSeries.fetch_open_data(
        det, psd_start, psd_end, sample_rate=4096, cache=True
    ).resample(sample_rate)
    psd_gwpy = bg_strain.psd(fftlength=duration, overlap=duration / 2, method="median")
    asd_gwpy = psd_gwpy ** 0.5

    ifo.power_spectral_density = PowerSpectralDensity(
        frequency_array=psd_gwpy.frequencies.value,
        psd_array=psd_gwpy.value,
    )
    # NOTE: whiten() takes an ASD, not a PSD. Passing psd_gwpy here silently
    # over-whitens the strain -- this was one of the bugs caught mid-session.
    clean_strains[det] = short_strain_2k.whiten(asd=asd_gwpy).bandpass(f_min, f_max)

# =====================================================================
print("--> [2/6] EMPIRICAL: Model-Agnostic H1-L1 Causal Correlation...")
# =====================================================================
crop_start = trigger_time + 0.35
crop_end = trigger_time + 0.45

h_raw = clean_strains["H1"].crop(crop_start, crop_end).value
l_raw = clean_strains["L1"].crop(crop_start, crop_end).value

h_norm = (h_raw - np.mean(h_raw)) / np.std(h_raw)
l_norm = (l_raw - np.mean(l_raw)) / np.std(l_raw)

corr = correlate(h_norm, l_norm, mode="full", method="fft")
lags = correlation_lags(len(h_norm), len(l_norm), mode="full") / sample_rate

physical = np.abs(lags) <= 0.010  # Speed-of-light causal cap between H1/L1
best_index = np.argmax(np.abs(corr[physical]))
peak_corr = corr[physical][best_index] / len(h_norm)
lag_seconds = lags[physical][best_index]

print(f"      Inter-site transit lag: {lag_seconds * 1000:+.3f} ms (peak corr = {peak_corr:.3f})")

# =====================================================================
print("--> [3/6] EMPIRICAL: Local Background Z-Score (Null Windows)...")
# =====================================================================
# NOTE: the exclusion window below must fully cover the visible chirp
# (crop_start/crop_end above, ~+0.35 to +0.45) plus padding. Leaving any
# part of the event inside the "null" pool inflates the background
# statistic and makes the z-score meaningless -- this was the second bug
# caught mid-session.
full_h1 = clean_strains["H1"].value
full_l1 = clean_strains["L1"].value
full_times = clean_strains["H1"].times.value
win_samps = int(0.100 * sample_rate)

event_pad_start = trigger_time + 0.32
event_pad_end = trigger_time + 0.46
null_corrs = []

for i in range(len(full_h1) // win_samps):
    lo = i * win_samps
    hi = lo + win_samps
    t_lo = full_times[lo]
    t_hi = full_times[min(hi - 1, len(full_times) - 1)]

    # Reject any chunk that so much as touches the padded event window.
    if t_lo < event_pad_end and t_hi > event_pad_start:
        continue

    h_chunk = full_h1[lo:hi]
    l_chunk = full_l1[lo:hi]
    if len(h_chunk) != win_samps or np.std(h_chunk) == 0 or np.std(l_chunk) == 0:
        continue

    c_null = correlate(
        (h_chunk - np.mean(h_chunk)) / np.std(h_chunk),
        (l_chunk - np.mean(l_chunk)) / np.std(l_chunk),
        mode="full", method="fft",
    )
    lag_idx = correlation_lags(len(h_chunk), len(l_chunk), mode="full")
    val_null = np.abs(lag_idx / sample_rate) <= 0.010
    if np.any(val_null):
        null_corrs.append(np.max(np.abs(c_null[val_null])) / len(h_chunk))

z_score = 0.0
if len(null_corrs) > 0 and np.std(null_corrs) > 0:
    z_score = (abs(peak_corr) - np.mean(null_corrs)) / np.std(null_corrs)

print(f"      Local null z-score: {z_score:.2f} sigma above nearby background")
print("      (diagnostic only -- too few 100ms chunks in 4s for a rigorous detection claim)")

# =====================================================================
print("--> [4/6] EMPIRICAL: Q-Transform Ridge Extraction (MAD threshold)...")
# =====================================================================
# NOTE: uses a MAD-based robust noise floor, deliberately NOT a hand-tuned
# monotonic frequency-sweep filter. An earlier script variant swapped this
# for a manually bounded acceptance window, which can shape the ridge
# toward whatever curve looks right rather than letting the noise floor
# decide what's signal -- see PWC.md section 10.
q_outseg = (trigger_time + 0.25, trigger_time + 0.50)
hq = raw_strains["H1"].q_transform(frange=(f_min, f_max), qrange=(4, 64), outseg=q_outseg)

hq_times = hq.times.value
hq_freqs = hq.frequencies.value
hq_matrix = hq.value  # shape: (n_times, n_freqs)

chirp_start = trigger_time + 0.35
chirp_end = trigger_time + 0.43

c_mask = (hq_times >= chirp_start) & (hq_times <= chirp_end)
c_times = hq_times[c_mask]
c_power_matrix = hq_matrix[c_mask, :]

baseline_mask = (hq_times >= trigger_time + 0.25) & (hq_times < trigger_time + 0.34)
baseline_matrix = hq_matrix[baseline_mask, :]
noise_floor = np.median(baseline_matrix)
mad = np.median(np.abs(baseline_matrix - noise_floor))
thresh = noise_floor + 2.5 * (1.4826 * mad)

r_idx = np.argmax(c_power_matrix, axis=1)
peak_powers = np.max(c_power_matrix, axis=1)
v_mask = peak_powers > thresh

clean_ridge_t = c_times[v_mask]
clean_ridge_f = hq_freqs[r_idx[v_mask]]

df_q = np.median(np.diff(hq_freqs))
P_d_proxy = np.sum(c_power_matrix, axis=1) * df_q  # excess-power proxy, NOT a calibrated energy
P_d_norm = P_d_proxy / np.max(P_d_proxy)

print(f"      Ridge nodes retained: {len(clean_ridge_t)} spanning "
      f"{clean_ridge_f.min():.1f}-{clean_ridge_f.max():.1f} Hz")

# =====================================================================
print("--> [5/6] PWC MODEL LAYER: Power-Law Ridge Fit (empirical exponent)...")
# =====================================================================
# This is a bare power-law fit to the extracted ridge, used only to get a
# first-look exponent estimate. It is NOT yet a derivation from a PWC
# equation of state -- that derivation is the actual open item (see
# Module 6 and PWC.md section 10).
f_mask = (clean_ridge_t >= clean_ridge_t[0]) & (clean_ridge_t <= clean_ridge_t[-1] - 0.008)
t_f, f_f = clean_ridge_t[f_mask], clean_ridge_f[f_mask]
t0, f0 = t_f[0], f_f[0]


def pw_func(p, t):
    log_k, alpha = p
    base = f0 ** (1.0 - alpha) - (alpha - 1.0) * np.exp(log_k) * (t - t0)
    out = np.full_like(t, 1e12, dtype=float)
    valid = base > 0
    out[valid] = base[valid] ** (-1.0 / (alpha - 1.0))
    return out


fit_result = least_squares(
    lambda p: pw_func(p, t_f) - f_f,
    x0=[np.log(1e-5), 3.513],
    bounds=([np.log(1e-12), 0.25], [np.log(1e2), 8.0]),
    loss="soft_l1", f_scale=5.0,
)
b_k, b_alpha = np.exp(fit_result.x[0]), fit_result.x[1]
rmse_hz = np.sqrt(np.mean((pw_func(fit_result.x, t_f) - f_f) ** 2))

print(f"      Fitted exponent alpha: {b_alpha:.3f}   kappa: {b_k:.4e}   RMSE: {rmse_hz:.3f} Hz")

f_mapped_eval = pw_func(fit_result.x, clean_ridge_t)
f_mapped_vis = f_mapped_eval.copy()
f_mapped_vis[f_mapped_vis >= 1e10] = np.nan

# =====================================================================
print("--> [6/6] PWC MODEL LAYER: df/dt = kappa*f^alpha Radiation Sandbox...")
# =====================================================================
# NEW relative to prior script versions -- this stage did not exist before.
# This is an explicit, honest SANDBOX, not a validated result: kappa/alpha
# below are placeholder test values, not values fit to clean_ridge_f. The
# actual next step is fitting this ODE (or replacing it with a derived
# dE_orbit^PW/df and P_wave^PW(f) from a real PWC equation of state) against
# clean_ridge_t/clean_ridge_f and P_d_proxy -- see PWC.md section 9-10.

def phase_wave_derivatives(t, f, kappa, alpha):
    return kappa * (f ** alpha)


test_kappa = 120.0   # PLACEHOLDER -- not fit to data
test_alpha = 2.0      # PLACEHOLDER -- not fit to data

f_initial = clean_ridge_f[0]
t_span = (clean_ridge_t[0], clean_ridge_t[-1])

sol = solve_ivp(
    phase_wave_derivatives,
    t_span,
    [f_initial],
    args=(test_kappa, test_alpha),
    t_eval=clean_ridge_t,
    method="RK45",
)

if sol.success:
    f_PW_model = sol.y[0]
    p_snap_PW = (f_PW_model ** (-1.0 / 3.0)) * phase_wave_derivatives(
        clean_ridge_t, f_PW_model, test_kappa, test_alpha
    )
    p_snap_norm = p_snap_PW / np.max(p_snap_PW)
    print("      Sandbox integration succeeded (placeholder kappa/alpha -- unfit).")
else:
    f_PW_model = np.full_like(clean_ridge_t, np.nan)
    p_snap_norm = np.full_like(clean_ridge_t, np.nan)
    print("      Sandbox integration FAILED -- kappa/alpha combination left the physical domain.")

# =====================================================================
# DASHBOARD
# =====================================================================
fig = plt.figure(figsize=(16, 14))
gs = fig.add_gridspec(4, 2, height_ratios=[1.2, 1, 0.8, 0.8], hspace=0.4, wspace=0.25)
plt.suptitle("PWC GW150914 DIAGNOSTIC: EMPIRICAL TARGETS + PWC MODEL LAYER",
             fontsize=15, weight="bold", y=0.98)

ax1 = fig.add_subplot(gs[0, 0])
t_plot_h = clean_strains["H1"].times.value
t_plot_l = clean_strains["L1"].times.value - lag_seconds
mask_plot_h = (t_plot_h >= trigger_time + 0.35) & (t_plot_h <= trigger_time + 0.45)
mask_plot_l = (t_plot_l >= trigger_time + 0.35) & (t_plot_l <= trigger_time + 0.45)
ax1.plot(t_plot_h[mask_plot_h] - trigger_time, clean_strains["H1"].value[mask_plot_h],
          color="cyan", lw=1.5, label="H1 Strain")
ax1.plot(t_plot_l[mask_plot_l] - trigger_time, clean_strains["L1"].value[mask_plot_l],
          color="orange", lw=1.2, alpha=0.85, label=f"L1 (shifted {lag_seconds * 1000:+.2f} ms)")
ax1.set_title("Empirical: H1 vs L1 Strain Coherence", fontsize=11, weight="bold")
ax1.set_xlabel(f"Seconds from trigger [{trigger_time:.1f} GPS]")
ax1.set_ylabel("Whitened strain")
ax1.grid(alpha=0.3)
ax1.legend(loc="upper left")

ax2 = fig.add_subplot(gs[0, 1])
mesh = ax2.pcolormesh(hq_times - trigger_time, hq_freqs, hq_matrix.T, shading="auto", cmap="viridis")
ax2.plot(clean_ridge_t - trigger_time, clean_ridge_f, "o", color="gold", ms=4,
          markeredgecolor="black", label="Extracted ridge (MAD threshold)")
ax2.set_xlim(0.25, 0.48)
ax2.set_ylim(f_min, f_max)
ax2.set_yscale("log")
ax2.set_title("Empirical: Q-Transform & Extracted Ridge", fontsize=11, weight="bold")
ax2.set_xlabel(f"Seconds from trigger [{trigger_time:.1f} GPS]")
ax2.set_ylabel("Frequency (Hz)")
fig.colorbar(mesh, ax=ax2, label="Normalized power")
ax2.legend(loc="upper left")

ax3 = fig.add_subplot(gs[1, 0])
ax3.plot(clean_ridge_t - trigger_time, clean_ridge_f, "o", color="gold", ms=5,
          markeredgecolor="black", label="Empirical ridge")
ax3.plot(t_f - trigger_time, f_mapped_vis[f_mask], "-", color="red", lw=2.5,
          label=rf"Power-law fit ($\alpha$={b_alpha:.3f})")
ax3.plot(clean_ridge_t[~f_mask] - trigger_time, f_mapped_vis[~f_mask], "--", color="red",
          lw=1.8, alpha=0.6, label="Unbounded projection")
ax3.set_ylim(30, 260)
ax3.set_title("PWC model: Ridge Fit vs Projection", fontsize=11, weight="bold")
ax3.set_ylabel("Frequency (Hz)")
ax3.set_xlabel(f"Seconds from trigger [{trigger_time:.1f} GPS]")
ax3.grid(alpha=0.3)
ax3.legend(loc="upper left")

ax4 = fig.add_subplot(gs[1, 1])
resids = clean_ridge_f - f_mapped_vis
ax4.axhline(0, color="black", lw=1)
ax4.plot(clean_ridge_t - trigger_time, resids, "o-", color="slateblue", lw=1.2, ms=4)
ax4.fill_between(clean_ridge_t - trigger_time, resids, 0, where=(resids < 0), color="blue", alpha=0.15)
ax4.set_ylim(-150, 20)
ax4.set_title("Residuals / Turnover", fontsize=11, weight="bold")
ax4.set_xlabel(f"Seconds from trigger [{trigger_time:.1f} GPS]")
ax4.set_ylabel("Deviance (Hz)")
ax4.grid(alpha=0.3)

ax5 = fig.add_subplot(gs[2, :])
ax5.plot(c_times - trigger_time, P_d_norm, color="darkorange", lw=2.0, label="Empirical P_d(t) (excess-power proxy)")
ax5.set_title("Empirical: Normalized Excess-Power Envelope", fontsize=11, weight="bold")
ax5.set_xlabel(f"Seconds from trigger [{trigger_time:.1f} GPS]")
ax5.set_ylabel("Normalized power")
ax5.grid(alpha=0.3)
ax5.legend(loc="upper left")

ax6 = fig.add_subplot(gs[3, :])
ax6.plot(clean_ridge_t - trigger_time, clean_ridge_f, "o", color="gold", ms=4,
          markeredgecolor="black", label="Empirical ridge")
ax6.plot(clean_ridge_t - trigger_time, f_PW_model, "-", color="blue", lw=2,
          label=f"df/dt=kappa*f^alpha sandbox (UNFIT: kappa={test_kappa}, alpha={test_alpha})")
ax6.set_title("PWC model layer: Unfit ODE Sandbox vs Empirical Ridge (Module 6)", fontsize=11, weight="bold")
ax6.set_xlabel(f"Seconds from trigger [{trigger_time:.1f} GPS]")
ax6.set_ylabel("Frequency (Hz)")
ax6.grid(alpha=0.3)
ax6.legend(loc="upper left")

plt.tight_layout()
plt.show()

print("\n[+] Pipeline complete. Modules 0-4 are empirical/theory-neutral; "
      "modules 5-6 are the PWC model layer -- module 6 is an unfit sandbox, "
      "not a validated result. See PWC.md section 10 for the honest status list.\n")
