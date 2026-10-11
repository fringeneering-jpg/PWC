# PWC math-check: cosmic birefringence through the Boötes Void

Script: `scratch/pwc_bootes_birefringence.py` (arithmetic on locked repo numbers only; repo untouched).
Sources: `PWC/DERIVATIONS.md` row 17; `PWC/PWC/derivations/lensing_redshift_mechanics.md` lines 19, 35–39;
`PWC/PWC/session_logs/2026-10-02/2026-10-02_0852_lensing_redshift_ldl_hdl.md` lines 82, 94–95;
`PWC/PWC/session_logs/2026-10-08/2026-10-08_survival_triad_comet.md` lines 92–111;
`PWC/PWC/session_logs/2026-10-08/2026-10-08_FULL_LEDGER.md` lines 231–235.

## Locked numbers (verbatim, from the repo)

- Registry row 17: *"rotation rate 1.4×10⁻²⁰ rad/s = 0.0059 H₀ for β = 0.35°"*; caveat:
  *"a dipole check on 'we rotate' (a rigid rotation gives a zero-mean dipole across the sky;
  the repo treats β as uniform)"*.
- Session log (2026-10-02): *"0.35 deg over 13.8 Gyr -> Omega = 1.40e-20 rad/s = 0.0059 H0 (0.0254 deg per Gyr)"*;
  the "we rotate" reading: *"the polarization of the light is fixed in the static medium; WE (matter) rotate,
  so the polarization angle we measure turns by how much we rotated relative to the medium during the flight:
  beta = Omega x T."* Jaden verbatim: *"we rotate moron do i need to constantly repeat myself"*.
- `lensing_redshift_mechanics.md` line 37: *"measured cosmic polarization rotation beta = 0.35 +- 0.14 degrees
  (2.4 sigma, NOT a detection; later combined analyses ~3.6 sigma), over the comoving distance to last scattering
  4.32e26 m: rotation rate 1.414e-29 rad/m = 0.025 degrees per Gpc ... In the no-stretch picture
  (path = c x 13.8 Gyr = 1.31e26 m) the rate would be 4.68e-29 rad/m."*
- Registry row 17, aberration (locked): *"aberration v_t/c, 20.5″ for Earth's orbit, 254″ at 370 km/s"*.
- H₀ ruling / void prediction (2026-10-08): *"cosmic birefringence should be MAXIMAL in deep space / voids
  (no local light or heat sources) and SUPPRESSED near matter. ... PWC predicts birefringence to anti-correlate
  with matter density. A positive matter correlation would falsify the reading."*

## The numbers

| Quantity | Value |
|---|---|
| Path length through Boötes | 330 Mly = 3.122×10²⁴ m (travel time 330 Myr = 1.041×10¹⁶ s) |
| Distance to Boötes | 700 Mly (z ≈ 0.05) |
| Angular diameter of Boötes | 26.5° |
| **β_Boötes = (1.4×10⁻²⁰ rad/s) × (330 Mly/c₀)** | **1.458×10⁻⁴ rad = 0.00835° = 30.1″** |
| Global β (measured, Planck PR4) | 0.30° ± 0.11° ([arXiv:2201.07682](https://arxiv.org/abs/2201.07682)); repo locks 0.35° ± 0.14° (2.4σ → ~3.6σ combined) |
| Path-averaged expectation (uniform rate) | 0.0072° (β=0.30°) / 0.0084° (β=0.35°) — **β_Boötes equals the path average by construction** |
| β_Boötes / β_global | 1/36 (path fraction is 330/13,800 = 1/42 = 2.39%) |
| Repo's own comoving-stretch alternative rate (1.414×10⁻²⁹ rad/m) | 0.00253° — **3.30× smaller; the repo lists two inconsistent rates** |
| **Void/wall contrast** | S1 (repo's uniform treatment): **exactly 0**. S2 (maximal reading, all rotation in rested voids, walls = 0, void path fraction 0.6): **+0.0120° = 43″ (β=0.30° calib) to +0.0140° = 50″ (β=0.35° calib)**, i.e. rate only 1.43–1.66× the locked rate. If "deep space" rather than only voids is rested, the contrast collapses to ~0 again. |
| Sensitivity needed for 4σ on the maximal excess | σ_patch ≈ 0.003° — ~37× better than the current PR4 monopole error (0.11°); 10–40× below the amplitudes (0.1–0.5°) and noise of the claimed anisotropy detections, and below the foreground (dust-EB) systematic floor the PR4 team itself flags |

## The falsifier, precisely

Define Δβ ≡ β̄(26.5° disc at Boötes) − β̄(equal-area annulus just outside).

- **Kills PWC (void-maximal reading):** a **positive matter correlation** — Δβ < 0 at ≥3σ (rotation measurably
  larger through walls/matter than through the void) — the repo's own falsification sentence. A sensitivity null
  (|Δβ| < 0.004° with σ ≤ 0.0013°) also kills the maximal reading by absence.
- **Kills it the OTHER way** (kills the uniform treatment, the rigid "we rotate" account, and the null
  interpretation of the contested 0.3°): a significant localized Δβ ≈ +0.008° to +0.012° centred on the void,
  suppressed behind walls. Any significant void-scale structure in β of either sign kills the repo's uniform
  treatment and the zero-mean-dipole "we rotate" account (the registry's own flagged check). The positive-void
  sign also discriminates PWC from standard axion/pseudoscalar-Chern-Simons models, whose rotation tracks the
  field around matter and correlates **with** density.

## Verdict

The locked rate is the global path average, so through Boötes PWC's own numbers give β ≈ 0.0084° (30″) —
1/36 of the contested global 0.3° — with **zero void/wall contrast by construction**; the qualitative
"maximal in voids, suppressed near matter" ruling is unquantified, and even its most generous calibrated
reading (all rotation in voids, none in walls) yields an excess of only +0.012° (43″) over a 26.5° patch.
That is ~40× below the current β-map sensitivity (the claimed anisotropy detections sit at 0.1–0.5° amplitudes,
2–3σ, themselves foreground-contested), so the prediction is **not testable now** — and worse, as it stands it
predicts nothing sharp: the same repo contains two inconsistent rates (no-stretch vs comoving, 3.30× apart) and
two unreconciled mechanisms ("we rotate" = zero-mean dipole; rested-lattice = void maxima). The clean falsifier
exists — a positive matter correlation of β kills the void-maximal reading, a localized +0.008–0.012° void excess
kills the uniform/rotation accounts — but at PWC's own magnitude it needs σ ≈ 0.003° per 26.5° patch, far beyond
current maps and near the limit of even next-generation instruments.
