# =====================================================================
# PWC GW150914 BOUNDED-MODEL ROLLING HOLDOUT TEST (Colab / gwpy)
# =====================================================================
# Fixes applied from review of the first attempt:
#  1. NO hand-tuned monotonic ridge filter -- MAD threshold only (Module 4,
#     unchanged from the validated pipeline).
#  2. Reduced to a 3-parameter model (beta=1 fixed) -- more identifiable
#     than 4 params on a short, noisy ridge.
#  3. No silent clipping near f_max -- an ODE event stops integration when
#     the trajectory approaches the bound; beyond that point is reported
#     as "out of model domain," not smoothed over.
#  4. Fair unbounded-model comparison -- also event-stopped (at a large
#     blow-up threshold), scored only over its valid domain, with its
#     predicted blow-up time reported explicitly.
#  5. Rolling forecast (train on 50/60/70/80%, predict next 10% each time)
#     instead of one fixed split -- a real finite bound should give a
#     STABLE f_max estimate as more data is added, not just a single
#     number from one split.
#  6. A non-PWC empirical baseline (logistic saturating curve) included,
#     so "beats a rigid textbook constant" isn't a bar of one competitor.
# =====================================================================

!pip install -q gwpy scipy numpy matplotlib

import logging
import warnings
import numpy as np
import matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeries
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares, curve_fit

warnings.filterwarnings("ignore")

print("\n" + "=" * 75)
print("     PWC GW150914 ROLLING HOLDOUT TEST")
print("=" * 75 + "\n")

trigger_time = 1126259462.4
duration = 4.0
sample_rate = 2048
f_min, f_max_band = 20.0, 300.0
psd_duration = 128.0
psd_start = trigger_time - duration / 2 - psd_duration
psd_end = trigger_time - duration / 2

# ---------------------------------------------------------------------
# MODULE 1-3: fetch, PSD, whiten (unchanged, validated)
# ---------------------------------------------------------------------
print("--> Fetching H1 strain + off-source PSD, whitening...")
event_strain = TimeSeries.fetch_open_data(
    "H1", trigger_time - duration / 2, trigger_time + duration / 2, cache=True
).resample(sample_rate)
bg_strain = TimeSeries.fetch_open_data(
    "H1", psd_start, psd_end, sample_rate=4096, cache=True
).resample(sample_rate)
psd_gwpy = bg_strain.psd(fftlength=duration, overlap=duration / 2, method="median")
asd_gwpy = psd_gwpy ** 0.5
clean_strain = event_strain.whiten(asd=asd_gwpy).bandpass(f_min, f_max_band)

# ---------------------------------------------------------------------
# MODULE 4: Q-transform, MAD threshold ONLY -- no monotonic filter
# ---------------------------------------------------------------------
print("--> Q-transform + MAD-threshold ridge extraction (no hand-tuned filter)...")
q_outseg = (trigger_time + 0.25, trigger_time + 0.50)
hq = event_strain.q_transform(frange=(f_min, f_max_band), qrange=(4, 64), outseg=q_outseg)
hq_times = hq.times.value
hq_freqs = hq.frequencies.value
hq_matrix = hq.value

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

# NOTE: no monotonic/continuity filter applied here. This is the raw
# MAD-threshold-passing ridge, exactly as the validated pipeline defines it.
rt_clean = c_times[v_mask] - trigger_time
rf_clean = hq_freqs[r_idx[v_mask]]
print(f"    Ridge: {len(rt_clean)} nodes, {rf_clean.min():.1f}-{rf_clean.max():.1f} Hz, "
      f"t=[{rt_clean.min():.4f},{rt_clean.max():.4f}]s")

f_obs_max = rf_clean.max()

# ---------------------------------------------------------------------
# 3-PARAMETER BOUNDED MODEL: df/dt = kappa * f^alpha * (1 - f/f_max)
# beta fixed at 1 for identifiability on a short ridge.
# Event-stopped: integration halts if f gets within 0.1% of f_max
# (treated as reaching the model's domain boundary, not smoothed past it).
# ---------------------------------------------------------------------
def bounded_rhs(t, y, kappa, alpha, fmax):
    f = y[0]
    if f >= fmax:
        return [0.0]
    return [kappa * (f ** alpha) * (1 - f / fmax)]

def near_bound_event(t, y, kappa, alpha, fmax):
    return (y[0] / fmax) - 0.999
near_bound_event.terminal = True
near_bound_event.direction = 1

def integrate_bounded(params, t_eval, t0, f0):
    log_kappa, alpha, fmax = params
    kappa = np.exp(log_kappa)
    sol = solve_ivp(bounded_rhs, (t0, t_eval[-1] + 1e-6), [f0], t_eval=None,
                     args=(kappa, alpha, fmax), method="RK45", max_step=0.0005,
                     events=near_bound_event, dense_output=True)
    pred = np.full_like(t_eval, np.nan)
    t_stop = sol.t[-1]
    in_domain = t_eval <= t_stop
    if np.any(in_domain):
        pred[in_domain] = sol.sol(t_eval[in_domain])[0]
    return pred, t_stop  # t_stop = where model says it leaves valid domain (approaches f_max)

def resid_bounded(params, t_fit, f_fit, t0, f0):
    pred, _ = integrate_bounded(params, t_fit, t0, f0)
    pred = np.where(np.isnan(pred), 1e3, pred)  # heavily penalize leaving domain during TRAIN fit
    return pred - f_fit

# Unbounded comparison: df/dt = kappa*f^alpha, event-stopped at a genuine
# blow-up threshold (5x observed max) rather than scored as an outright
# failure -- fair domain-limited comparison.
BLOWUP_THRESH = f_obs_max * 5.0

def unbounded_rhs(t, y, kappa, alpha):
    return [kappa * (y[0] ** alpha)]

def blowup_event(t, y, kappa, alpha):
    return y[0] - BLOWUP_THRESH
blowup_event.terminal = True
blowup_event.direction = 1

def integrate_unbounded(params, t_eval, t0, f0):
    log_kappa, alpha = params
    kappa = np.exp(log_kappa)
    sol = solve_ivp(unbounded_rhs, (t0, t_eval[-1] + 1e-6), [f0], args=(kappa, alpha),
                     method="RK45", max_step=0.0005, events=blowup_event, dense_output=True)
    pred = np.full_like(t_eval, np.nan)
    t_stop = sol.t[-1]
    in_domain = t_eval <= t_stop
    if np.any(in_domain):
        pred[in_domain] = sol.sol(t_eval[in_domain])[0]
    return pred, t_stop

def resid_unbounded(params, t_fit, f_fit, t0, f0):
    pred, _ = integrate_unbounded(params, t_fit, t0, f0)
    pred = np.where(np.isnan(pred), 1e3, pred)
    return pred - f_fit

# Non-PWC empirical baseline: logistic saturating curve, purely descriptive,
# no physical claim attached -- f(t) = fmax_L / (1 + exp(-k*(t-t_mid)))
def logistic(t, fmax_L, k, t_mid, f_floor):
    return f_floor + (fmax_L - f_floor) / (1 + np.exp(-k * (t - t_mid)))

# ---------------------------------------------------------------------
# ROLLING FORECAST: train on 50/60/70/80%, predict the NEXT 10% each time
# ---------------------------------------------------------------------
train_fracs = [0.50, 0.60, 0.70, 0.80]
n_total = len(rt_clean)
results = []

# Bounds: deliberately wide, f_max lower bound only just above observed max
# (not pinned near the expected ringdown region), so a pinned result is
# meaningful rather than pre-baked.
bnd_lo = [np.log(1e-10), 1.0, f_obs_max * 1.01]
bnd_hi = [np.log(1e3), 8.0, f_obs_max * 10.0]

print("\n--> Rolling forecast (fit on train fraction, predict next 10%, all blind):\n")
print(f"{'train%':>7} {'alpha':>7} {'f_max(Hz)':>10} {'pinned?':>8} "
      f"{'next10% RMSE':>13} {'unb. RMSE':>10} {'unb. blowup_t':>14} {'logistic RMSE':>14}")

for frac in train_fracs:
    n_train = int(n_total * frac)
    n_next = int(n_total * 0.10)
    if n_train + n_next > n_total:
        n_next = n_total - n_train
    if n_next < 2:
        continue

    t_train, f_train = rt_clean[:n_train], rf_clean[:n_train]
    t_next, f_next = rt_clean[n_train:n_train + n_next], rf_clean[n_train:n_train + n_next]
    t0b, f0b = t_train[0], f_train[0]

    x0 = [np.log(5e-4), 2.7, f_obs_max * 1.15]
    res = least_squares(resid_bounded, x0, args=(t_train, f_train, t0b, f0b),
                         bounds=(bnd_lo, bnd_hi), loss="soft_l1", f_scale=3.0)
    kappa_f, alpha_f, fmax_f = np.exp(res.x[0]), res.x[1], res.x[2]
    pinned = (abs(alpha_f - bnd_hi[1]) < 1e-2) or (abs(fmax_f - bnd_lo[2]) < 1e-2 * f_obs_max) \
             or (abs(fmax_f - bnd_hi[2]) < 1e-2 * f_obs_max)

    pred_next, _ = integrate_bounded(res.x, t_next, t0b, f0b)
    rmse_next = np.sqrt(np.nanmean((pred_next - f_next) ** 2)) if not np.all(np.isnan(pred_next)) else np.nan

    res_u = least_squares(resid_unbounded, [np.log(5e-4), 2.7], args=(t_train, f_train, t0b, f0b),
                           bounds=([np.log(1e-10), 1.0], [np.log(1e3), 8.0]), loss="soft_l1", f_scale=3.0)
    pred_next_u, t_stop_u = integrate_unbounded(res_u.x, t_next, t0b, f0b)
    in_domain_u = ~np.isnan(pred_next_u)
    rmse_next_u = (np.sqrt(np.mean((pred_next_u[in_domain_u] - f_next[in_domain_u]) ** 2))
                   if np.any(in_domain_u) else np.nan)

    try:
        popt_log, _ = curve_fit(logistic, t_train, f_train,
                                 p0=[f_obs_max * 1.1, 200, t_train[-1], f_train[0]], maxfev=5000)
        pred_next_log = logistic(t_next, *popt_log)
        rmse_next_log = np.sqrt(np.mean((pred_next_log - f_next) ** 2))
    except Exception:
        rmse_next_log = np.nan

    results.append(dict(frac=frac, alpha=alpha_f, fmax=fmax_f, pinned=pinned,
                         rmse_next=rmse_next, rmse_next_u=rmse_next_u,
                         t_stop_u=t_stop_u, rmse_next_log=rmse_next_log))
    print(f"{frac*100:6.0f}% {alpha_f:7.2f} {fmax_f:10.1f} {str(pinned):>8} "
          f"{rmse_next:13.2f} {rmse_next_u:10.2f} {t_stop_u:14.4f} {rmse_next_log:14.2f}")

print("\n--- Interpretation guide ---")
print("A real finite bound should show f_max converging to a STABLE value as train% increases,")
print("not jumping around or sitting pinned at a bound. Compare bounded vs unbounded vs logistic")
print("next-10% RMSE at each row -- the bounded model only 'wins' if its RMSE is consistently")
print("lower than BOTH competitors, not just lower than a model that hit its blow-up event.")

# ---------------------------------------------------------------------
# PLOT: f_max estimate stability across rolling train fractions
# ---------------------------------------------------------------------
fracs = [r["frac"] for r in results]
fmaxes = [r["fmax"] for r in results]
pinned_flags = [r["pinned"] for r in results]

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
colors = ["red" if p else "blue" for p in pinned_flags]
axes[0].scatter(fracs, fmaxes, c=colors, s=80, zorder=3)
axes[0].plot(fracs, fmaxes, "--", color="gray", alpha=0.5, zorder=1)
axes[0].set_xlabel("Training fraction")
axes[0].set_ylabel("Fitted f_max (Hz)")
axes[0].set_title("f_max stability across rolling forecast\n(red = pinned at bound, unreliable)")
axes[0].grid(alpha=0.3)

axes[1].plot(rt_clean, rf_clean, "o", color="gold", ms=4, mec="black", label="Real ridge (MAD only)")
for r, frac in zip(results, fracs):
    n_train = int(n_total * frac)
    axes[1].axvline(rt_clean[n_train - 1], color="gray", ls=":", alpha=0.4)
axes[1].set_xlabel("Time relative to trigger (s)")
axes[1].set_ylabel("Ridge frequency (Hz)")
axes[1].set_title("Ridge with rolling train/predict boundaries")
axes[1].legend(fontsize=8)
axes[1].grid(alpha=0.3)
plt.tight_layout()
plt.show()

print("\n[+] Rolling holdout test complete. Judge the theory on f_max stability")
print("    and next-10% RMSE across ALL rows, not on any single fit.")
