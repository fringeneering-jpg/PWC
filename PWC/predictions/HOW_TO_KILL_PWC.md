# How to Kill Phase Wave Cosmology — three falsification methods, ready to run

For observational-cosmology, radio-astronomy, and precision-metrology departments.
Every prediction below was frozen before publication (2026-10-12, commits on main).
A null on any of the three kills the framework's claim; the falsification condition
is stated with each test, so the kill is clean and citable either way.

---

## 1. The directional birefringence void-correlation (three sub-tests, frozen)

**The frozen prediction.** Cosmic birefringence accumulates preferentially along
low-density paths: β(n̂) = ∫ K(ρ,…) ds, ∂K/∂(ln ρ) < 0 (voids enhanced, walls
suppressed). The prediction template is in the record:
`PWC/birefringence_void_prediction.json`, built over 1,163 Douglass+ 2023
(Planck2018) SDSS DR7 voids. The highest-weight corridor lies at
**RA 142–150°, Dec +31–46°** (peak RA 149°, Dec +31°); the template's
fractional fluctuation is 43% — monopole-normalized, a characteristic
**~0.15°** amplitude. The spatial template and the positive sign are the
independently frozen targets; the amplitude normalization is stated before
fitting.

**Test 1a — amplitude exclusion.** Reconstruct a directional polarization-rotation
field and fit the frozen, mean-subtracted void template:
β_obs(n̂) = β₀ + A·T_void(n̂) + foreground/systematic terms, with the template
normalization and the predicted A specified before fitting, and the observational
mask, beam, and reconstruction response applied to the prediction. *Falsification:
a confidence interval excluding the predicted positive amplitude rejects the
fixed-amplitude version — an upper limit must fall below the predicted amplitude;
"no detection" alone is insufficient.*

**Test 1b — wrong-sign correlation.** Cross-correlate the reconstructed rotation
field with the frozen template over the shared footprint, using a predefined rank
statistic or angular cross-spectrum. *Falsification: a robust NEGATIVE correlation
rejects the voids-enhanced sign; a sufficiently precise null excludes the stated
amplitude, though not an arbitrarily weak sign-only hypothesis.*

**Test 1c — spatial-pattern failure.** Test the predicted high-weight corridor
against predefined lower-weight control regions, testing the entire template
rather than selecting favorable pixels afterward. *Falsification: with sensitivity
sufficient to recover the frozen signal in injection tests, the measured pattern
excluding the template — e.g. rotation preferring wall-dominated over
void-dominated sightlines.*

**Confounders, required for any of the three:** foreground EB checks,
polarization-angle calibration checks (instrument offsets and intrinsic
foreground EB correlations are recognized confounders), and end-to-end
simulations showing the analysis can recover or exclude the predicted signal.
Directional reconstruction uses the off-diagonal correlations between CMB
polarization modes — it is not a raw sky image of the ordinary EB spectrum.

**Hardware status (corrected):** published work has already reconstructed
anisotropic birefringence from Planck PR4 polarization data — whether that
reconstruction can constrain this template is a SENSITIVITY CALCULATION, not a
requirement for new telescopes. The Simons Observatory (Atacama, commissioning)
is the near-term instrument; **CMB-S4 is NOT a guaranteed platform** — DOE/NSF
withdrew support on 2025-07-09 and the project entered an orderly shutdown.
Do not advertise it as an assured test bed.

**Scope of a positive:** a replicated void-correlated signal supports the frozen
prediction and demands a physical explanation; it does not by itself establish
every part of PWC or collapse GR. The claim is the measurable one: here are the
template, normalization, sign, footprint, and exclusion criteria — test without
retuning.

**Sensitivity status (2026-10-12, preliminary):** area-scaled forecast from the
published PR4 map-space analysis (Scott, arXiv:2502.07654, σ_global = 0.04°):
per-template noise σ ≈ 0.23°, SNR ≈ 0.65 for the 0.15° target — the prediction
sits just below the existing sensitivity, and the published dipole null does not
test this template. Definitive sensitivity requires fitting the template with
the PR4 estimator response, mask, and simulation-derived covariance — named as
the next calculation.

**The literature is converging on this exact test:** cosmic birefringence
tomography via CMB × LSS cross-correlation (PRD, Oct 2023); anisotropic
birefringence as a model discriminator tied to LSS (arXiv:2610.09748, Oct 2026);
anisotropic birefringence estimators for forthcoming CMB surveys
(arXiv:2610.03876, Oct 2026); and void-based dark-sector probes. The
cross-correlation machinery is being built now — the frozen template predates
all of it.

---

## 2. The bare-proton frustration line (cryogenic Penning trap, BASE-style)

**The frozen prediction.** The proton's 720° fold carries a locked strain:
ΔU = δ·U = 2.47 eV for the electron; **0.0658 eV = 15.9 THz = 18.8 μm for the
proton**, from the same 5π² closure at the proton's scale. Absorbing one quantum
kicks the proton by Δp = E/c → **2.1 cm/s recoil**, visible as a discrete axial-
frequency step and temperature blip in a cryogenic Penning trap.

**The test.** Sweep a tunable mid-IR source across 15.9 THz on a trapped bare
proton; look for the recoil step, per-proton (not residual-gas) scaling.

**The falsification condition.** A clean exclusion of the 15.9 THz line kills
the proton's 5π² closure assumption — the second-scale extension of the
topology equation — in public, with the prediction dated before the run.

---

## 3. The next cap-runner (radio astronomy / proper-motion surveys)

**The frozen prediction.** A visible medium bow exists iff a body runs at
≥ ~0.9 of its own C(ρ) = min(c₀, √(2Y_bow/ρ)), with ρ read from the body's own
measured mass and radius. The law's only confirmed cap-runner is RBH-1 (0.996),
whose anchor was historically calibrated on it — so the next bow-shock object
is the independent test.

**The test.** For any newly identified bow-shock object (or the standing
candidates: B1508+55, 3C 186, CID-42, the Guitar pulsar), measure its speed,
mass, and radius; compare against its own C(ρ).

**The falsification condition.** A bow-shock object measured significantly
BELOW ~0.9 of its own C(ρ) — without the slammed (stripped-shell) signature —
falsifies the bow law and breaks the RBH-1 calibration circle.

---

The framework's own method applies to its killers: each falsifier is frozen,
dated, and in the git, so any null result is a clean, citable kill — and any
positive is the confirmation. The departments only need to run the hardware they
already have (or are building anyway).
