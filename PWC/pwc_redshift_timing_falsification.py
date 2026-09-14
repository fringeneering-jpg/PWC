"""
pwc_redshift_timing_falsification.py

A real, computed falsification test of the PWC §7 claim ("Redshift as Medium
Reorganization"): that combining (a) phase reorganization toward a denser
phase, tuned so wavelength stretches by the standard cosmological factor
(1+z), with (b) a density-dependent propagation-speed history, should ALSO,
for free, reproduce the independently-measured Type Ia supernova light-curve
time-dilation stretch, which real observations (Goldhaber et al. 1997/2001,
Blondin et al. 2008) show also scales as (1+z).

WHAT THIS SCRIPT DOES
----------------------
1. Fixes the wave-speed/density relation exactly as specified as the
   starting point in the task:

        v(rho) = c0 * sqrt(rho0 / rho)          (sound-speed-style scaling)

   i.e. denser medium -> slower propagation, today's density rho0 gives
   today's light speed c0.

2. Builds a REAL flat-LambdaCDM cosmic time <-> redshift map (Planck-like
   parameters: H0=67.4 km/s/Mpc, Om=0.315, Or=9.4e-5, OL=0.685) via
   numerical integration of the real Friedmann equation. This supplies
   actual lookback times in Gyr -- not a toy clock -- as the "real
   reference for cosmic history" requested.

3. Tries THREE separately-motivated density-history laws rho(z)/rho0:
      (A) matter-dominated scaling      rho/rho0 = (1+z)^3   [textbook]
      (B) radiation-dominated scaling   rho/rho0 = (1+z)^4   [textbook]
      (C) a third, functionally different guess: exponential decay in real
          cosmic lookback time with an e-folding of one Hubble time,
          rho/rho0 = exp(lookback_time / t_Hubble)
   All three share the one thing every real cosmological history agrees
   on: the medium (matter+radiation content) was denser in the past.

4. For a homogeneous medium (density is a function of cosmic time only,
   not of position along the line of sight -- the natural reading of
   "the medium's average density has been higher in the past"), and a
   FIXED proper path length L (this mechanism is explicitly NOT metric
   expansion -- PWC ties the whole redshift to phase reorganization +
   propagation-speed history, not to space stretching), the light-travel
   equation for a photon leaving at cosmic time t_e and arriving at t_a is

        integral_{t_e}^{t_a(t_e)} v(t) dt = L        (constant L)

   Differentiating with respect to t_e (Leibniz rule) gives the EXACT,
   closed-form prediction for how an emitted time-interval (e.g. the
   spacing between two wavecrests, or between two features of a light
   curve) maps onto an observed time interval:

        dt_a/dt_e = v(t_e) / v(t_a)

   This ratio is the model's predicted "timing stretch factor" -- directly
   analogous to the observed (1+z) supernova light-curve stretch. It is
   forced purely by mechanism (b) (propagation-speed history), exactly as
   PWC's own text says timing dilation must come from that piece alone.

5. Cross-checks the closed-form derivative against a genuine numerical
   integration + root-find (two real, closely-spaced photon trajectories,
   solved via scipy.integrate.quad + scipy.optimize.brentq) to make sure
   the analytic shortcut is not hiding a mistake.

6. Compares the predicted timing stretch to the REQUIRED (1+z) over
   z = 0.1 .. 1.5 (the real SN Ia time-dilation survey range) for all
   three density histories, and reports whether the gap grows or shrinks.

7. Saves plots + a results CSV to pwc_falsification_output/.

This is a genuine test that can fail -- and the code below does not adjust
anything post-hoc to make it pass.
"""

import os
import numpy as np
from scipy import integrate, optimize
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "pwc_falsification_output")
os.makedirs(OUTDIR, exist_ok=True)

# ---------------------------------------------------------------------
# 1. Real background cosmology (Planck-like flat LambdaCDM) -- used only
#    to get a REAL cosmic time <-> redshift map (lookback time in Gyr).
#    This grounds "cosmic history" in an actual, standard reference
#    rather than an arbitrary clock.
# ---------------------------------------------------------------------
H0_KMSMPC = 67.4                     # km/s/Mpc
OMEGA_M = 0.315
OMEGA_R = 9.4e-5
OMEGA_L = 1.0 - OMEGA_M - OMEGA_R

KM_PER_MPC = 3.0856775814913673e19
SEC_PER_GYR = 3.1556952e16
H0 = H0_KMSMPC * SEC_PER_GYR / KM_PER_MPC     # H0 in 1/Gyr
T_HUBBLE = 1.0 / H0                            # Hubble time, Gyr

def E(z):
    """Dimensionless Friedmann expansion rate H(z)/H0, real LambdaCDM."""
    return np.sqrt(OMEGA_M * (1 + z) ** 3 + OMEGA_R * (1 + z) ** 4 + OMEGA_L)

def lookback_time_gyr(z):
    """Real lookback time to redshift z, in Gyr, from the Friedmann eqn."""
    if z <= 0:
        return 0.0
    integrand = lambda zp: 1.0 / ((1 + zp) * H0 * E(zp))
    val, _ = integrate.quad(integrand, 0.0, z, limit=200)
    return val

print("=" * 72)
print("Real background cosmology check (Planck-like flat LambdaCDM):")
for zz in [0.1, 0.3, 0.7, 1.0, 1.5]:
    print(f"  z={zz:4.2f}  lookback={lookback_time_gyr(zz):6.3f} Gyr "
          f"(Hubble time = {T_HUBBLE:5.2f} Gyr)")
print("=" * 72)

# ---------------------------------------------------------------------
# 2. Wave-speed / density relation -- FIXED, as specified by the task:
#       v(rho) = c0 * sqrt(rho0 / rho)
#    All quantities below are worked in units where c0 = 1 and rho0 = 1
#    (only ratios matter for the stretch factors).
# ---------------------------------------------------------------------
def v_ratio_from_density_ratio(rho_over_rho0):
    """v(rho)/c0 given rho/rho0, for v(rho) = c0 sqrt(rho0/rho)."""
    return np.sqrt(1.0 / rho_over_rho0)

# ---------------------------------------------------------------------
# 3. Three density-history laws, rho(z)/rho0.
# ---------------------------------------------------------------------
def rho_ratio_matter(z):
    """Standard matter-dominated dilution: rho ~ a^-3 = (1+z)^3."""
    return (1.0 + z) ** 3

def rho_ratio_radiation(z):
    """Standard radiation-dominated dilution: rho ~ a^-4 = (1+z)^4."""
    return (1.0 + z) ** 4

def rho_ratio_expdecay(z):
    """Own guess: exponential decay in real cosmic lookback time, with an
    e-folding time of one Hubble time. Functionally different shape from
    a pure power law in (1+z), used to check whether the *shape* of the
    density history (not just its power-law index) can rescue the model."""
    tau = lookback_time_gyr(z)
    return np.exp(tau / T_HUBBLE)

DENSITY_MODELS = {
    "matter (1+z)^3":      rho_ratio_matter,
    "radiation (1+z)^4":   rho_ratio_radiation,
    "exp(lookback/t_H)":   rho_ratio_expdecay,
}

# ---------------------------------------------------------------------
# 4. Closed-form timing-stretch prediction:
#       dt_a/dt_e = v(t_e)/v(t_a=today) = v_ratio(z) / v_ratio(0)
#    v_ratio(0) = 1 by construction (rho(0)=rho0 -> v=c0).
# ---------------------------------------------------------------------
def predicted_timing_stretch(z, rho_ratio_fn):
    rho_e = rho_ratio_fn(z)
    return v_ratio_from_density_ratio(rho_e)   # divided by v_ratio(0)=1

# ---------------------------------------------------------------------
# 5. Numerical cross-check: actually integrate two nearby photon
#    trajectories through the SAME evolving-speed medium and root-find
#    their arrival times, rather than trusting the closed form blindly.
# ---------------------------------------------------------------------
def build_v_of_t(rho_ratio_fn, z_grid_max=3.0, n=4000):
    """Return an interpolating function v(t)/c0 of cosmic time t (Gyr),
    with t=0 today and t<0 in the past, valid over the grid range, built
    from the real lookback-time map and the chosen density history."""
    zs = np.linspace(0.0, z_grid_max, n)
    t_lookbacks = np.array([lookback_time_gyr(z) for z in zs])   # >=0
    t_vals = -t_lookbacks                                        # t<=0
    rho_ratios = np.array([rho_ratio_fn(z) for z in zs])
    v_ratios = v_ratio_from_density_ratio(rho_ratios)
    # t_vals is decreasing (0 down to -lookback_max); sort ascending for interp
    order = np.argsort(t_vals)
    t_sorted = t_vals[order]
    v_sorted = v_ratios[order]

    def v_of_t(t):
        # flat extrapolation just past t=0 (near-today / near-future),
        # only ever needed for a tiny perturbation during the finite-
        # difference check below.
        return np.interp(t, t_sorted, v_sorted)
    return v_of_t, t_sorted, v_sorted

def numeric_timing_stretch(z_target, rho_ratio_fn, delta_t=1e-4):
    """Integrate the fixed-L light-travel condition for a photon emitted
    at the cosmic time corresponding to z_target and arriving today, then
    perturb the emission time by delta_t (Gyr) and re-solve for the new
    arrival time via root-finding. Returns the numerically measured
    dt_a/dt_e, to be compared against the closed-form prediction."""
    v_of_t, t_grid, v_grid = build_v_of_t(rho_ratio_fn, z_grid_max=max(3.0, z_target * 2 + 1))
    t_e = -lookback_time_gyr(z_target)
    t0 = 0.0

    # L implied by this model for a photon emitted at t_e arriving today
    L, _ = integrate.quad(v_of_t, t_e, t0, limit=200)

    def path(t_start, t_end):
        val, _ = integrate.quad(v_of_t, t_start, t_end, limit=200)
        return val

    def arrival_time(t_start):
        # solve for t_end such that path(t_start, t_end) == L
        f = lambda t_end: path(t_start, t_end) - L
        # bracket around t0
        lo, hi = t0 - 5.0, t0 + 5.0
        return optimize.brentq(f, lo, hi, xtol=1e-10)

    t_a1 = arrival_time(t_e)
    t_a2 = arrival_time(t_e + delta_t)
    dt_a = t_a2 - t_a1
    return dt_a / delta_t, t_a1

# ---------------------------------------------------------------------
# 6. Run the comparison over z = 0.1 .. 1.5 (real SN Ia time-dilation
#    survey range) for all three density histories.
# ---------------------------------------------------------------------
z_range = np.linspace(0.1, 1.5, 15)
z_checkpoints = [0.3, 0.7, 1.2]   # for the numeric cross-check (slower)

results = {name: {"z": z_range, "S_timing": None} for name in DENSITY_MODELS}

print("\nClosed-form vs numerically-integrated timing stretch "
      "(sanity cross-check at 3 redshifts per model):")
for name, fn in DENSITY_MODELS.items():
    S = np.array([predicted_timing_stretch(z, fn) for z in z_range])
    results[name]["S_timing"] = S
    print(f"\n  Model: {name}")
    for zc in z_checkpoints:
        analytic = predicted_timing_stretch(zc, fn)
        numeric, _ = numeric_timing_stretch(zc, fn)
        print(f"    z={zc:4.2f}  analytic dt_a/dt_e={analytic:8.5f}   "
              f"numeric dt_a/dt_e={numeric:8.5f}   "
              f"(match to {abs(analytic-numeric):.2e})")

# ---------------------------------------------------------------------
# 7. Report: does S_timing(z) match the required (1+z)?
# ---------------------------------------------------------------------
target = 1.0 + z_range

print("\n" + "=" * 72)
print("RESULT TABLE: predicted timing stretch vs required (1+z)")
print("=" * 72)
header = f"{'z':>5} {'target(1+z)':>12}"
for name in DENSITY_MODELS:
    header += f" {name[:18]:>20}"
print(header)
for i, z in enumerate(z_range):
    row = f"{z:5.2f} {target[i]:12.4f}"
    for name in DENSITY_MODELS:
        row += f" {results[name]['S_timing'][i]:20.5f}"
    print(row)

# ratio S_timing/target, and whether the gap grows with z
print("\nRatio (predicted timing stretch) / (required 1+z):")
header = f"{'z':>5}"
for name in DENSITY_MODELS:
    header += f" {name[:18]:>20}"
print(header)
ratios = {}
for name in DENSITY_MODELS:
    ratios[name] = results[name]["S_timing"] / target
for i, z in enumerate(z_range):
    row = f"{z:5.2f}"
    for name in DENSITY_MODELS:
        row += f" {ratios[name][i]:20.5f}"
    print(row)

# ---------------------------------------------------------------------
# 8. Diagnostic: what power-law index WOULD reproduce (1+z), and under
#    which (unstated, contradictory) sign of the v-rho relation.
# ---------------------------------------------------------------------
print("\n" + "-" * 72)
print("Diagnostic: solving directly for what would be needed to close the gap")
print("-" * 72)
print("""
With v(rho) = c0*sqrt(rho0/rho) and rho/rho0 = (1+z)^n (n>0, denser in the
past, as required by every real cosmological history), the closed-form
timing stretch is:

    dt_a/dt_e = sqrt(rho0/rho(z)) = (1+z)^(-n/2)

This is LESS than 1 for any n>0 -- i.e. observed intervals are predicted
to be COMPRESSED (blueshifted timing), not stretched, for ANY positive
power-law index. No value of n>0 can make (1+z)^(-n/2) equal (1+z)>1.
The sign itself is wrong, not just the magnitude -- increasing n makes the
mismatch WORSE, not better, because it drives the exponent further
negative.

The only way to get a timing STRETCH (factor >1) out of this framework is
to flip the sign of the v-rho relation itself, to v(rho) = c0*sqrt(rho/rho0)
(denser medium propagates FASTER) -- the opposite of the sound-speed
analogy stated in PWC and the opposite of the relation this test was asked
to check. Even granting that flip, matching (1+z) exactly requires solving
(1+z)^(n/2) = (1+z), i.e. n=2 -- not the matter (n=3) or radiation (n=4)
scaling this framework's own text (S5, S9) invokes for "the medium's
density has been higher in the past." That n=2 value has no independent
motivation here; it would be reverse-engineered solely to force a match.
""")

# ---------------------------------------------------------------------
# 9. Plots
# ---------------------------------------------------------------------
colors = {"matter (1+z)^3": "#c0392b", "radiation (1+z)^4": "#8e44ad",
          "exp(lookback/t_H)": "#16a085"}

fig, ax = plt.subplots(figsize=(7.5, 5.5))
ax.plot(z_range, target, "k--", lw=2, label="required: (1+z)  [SN Ia timing + wavelength]")
for name in DENSITY_MODELS:
    ax.plot(z_range, results[name]["S_timing"], "-o", ms=4,
            color=colors[name], label=f"predicted timing stretch: {name}")
ax.axhline(1.0, color="gray", lw=0.8)
ax.set_xlabel("emission redshift z")
ax.set_ylabel("stretch factor  dt_observed / dt_emitted")
ax.set_title("PWC §7 timing-stretch prediction vs required (1+z)\n"
             "v(ρ) = c₀√(ρ₀/ρ), three density-history laws")
ax.legend(fontsize=8, loc="upper left")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUTDIR, "timing_stretch_vs_required.png"), dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(7.5, 5.5))
for name in DENSITY_MODELS:
    ax.plot(z_range, ratios[name], "-o", ms=4, color=colors[name], label=name)
ax.axhline(1.0, color="k", lw=1.5, ls="--", label="perfect match (ratio=1)")
ax.set_xlabel("emission redshift z")
ax.set_ylabel("predicted timing stretch / required (1+z)")
ax.set_title("Fractional match to observed SN Ia light-curve time dilation\n"
             "(1.0 = exact match; falling further below 1.0 = growing failure)")
ax.legend(fontsize=8)
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUTDIR, "ratio_to_required_1plusz.png"), dpi=150)
plt.close(fig)

# sign-flip diagnostic plot: show power-law n needed under each convention
fig, ax = plt.subplots(figsize=(7.5, 5.5))
n_scan = np.linspace(0, 6, 200)
z_demo = 1.0
stretch_as_specified = (1 + z_demo) ** (-n_scan / 2)   # v = c0 sqrt(rho0/rho)
stretch_flipped = (1 + z_demo) ** (n_scan / 2)          # v = c0 sqrt(rho/rho0), unphysical per task spec
ax.plot(n_scan, stretch_as_specified, color="#c0392b",
        label="v(ρ)=c₀√(ρ₀/ρ)  (as specified)")
ax.plot(n_scan, stretch_flipped, color="#2980b9",
        label="v(ρ)=c₀√(ρ/ρ₀)  (sign flipped, not what was specified)")
ax.axhline(1 + z_demo, color="k", ls="--", label=f"required (1+z) at z={z_demo}")
ax.axvline(3, color="gray", ls=":", lw=1, label="n=3 (matter)")
ax.axvline(4, color="gray", ls="-.", lw=1, label="n=4 (radiation)")
ax.set_xlabel("density-history power-law index n  [ρ/ρ0=(1+z)^n]")
ax.set_ylabel(f"predicted timing stretch at z={z_demo}")
ax.set_title("No positive n under the specified v-ρ relation reaches (1+z);\n"
             "reaching it requires flipping the v-ρ sign AND picking n=2")
ax.legend(fontsize=7.5, loc="upper left")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUTDIR, "sign_flip_diagnostic.png"), dpi=150)
plt.close(fig)

# ---------------------------------------------------------------------
# 10. Save results table as CSV
# ---------------------------------------------------------------------
csv_path = os.path.join(OUTDIR, "results_table.csv")
with open(csv_path, "w") as f:
    cols = ["z", "target_1plusz"] + [f"S_timing__{n}" for n in DENSITY_MODELS] + \
           [f"ratio__{n}" for n in DENSITY_MODELS]
    f.write(",".join(cols) + "\n")
    for i, z in enumerate(z_range):
        row = [f"{z:.4f}", f"{target[i]:.6f}"]
        for name in DENSITY_MODELS:
            row.append(f"{results[name]['S_timing'][i]:.6f}")
        for name in DENSITY_MODELS:
            row.append(f"{ratios[name][i]:.6f}")
        f.write(",".join(row) + "\n")

print(f"\nSaved plots and results table to: {OUTDIR}")
print("  - timing_stretch_vs_required.png")
print("  - ratio_to_required_1plusz.png")
print("  - sign_flip_diagnostic.png")
print("  - results_table.csv")
