# RBH-1 — metallicity dilution test (frozen 2026-09-29, before any metallicity was measured)

**Mechanism (PWC.md §8, RBH-1 "creation test"):** the bow wave slams ambient gas (ambient metallicity). Behind the black hole the cavitation pocket collapses and makes new matter from the medium, which forms as pure hydrogen. New hydrogen mixed into the swept gas must **dilute** it.

**Question:** gathered gas only (standard) vs gathered gas + new hydrogen (PWC).

## Measurement (model-neutral, no PWC quantity used)

- Data: JWST GO-3149 NIRSpec IFU G140M/F100LP, both re-reductions: v1 `D:\rbh1_reduction\cube` and v2 `D:\rbh1_reduction\cube_bkg`.
- Geometry: unchanged from `wake_profile.py` (published pointing geometry; x = arcsec downstream from the tip).
- Regions, fixed now:
  - **Apex (bow, swept ambient gas):** −0.25″ ≤ x < 0.25″, |y| < 0.5″
  - **Tail (downstream wake):** 0.5″ ≤ x < 2.5″, |y| < 0.5″
- Stack the continuum-subtracted spectra in each region; fit Hα + [N II]6548,6583 (6583/6548 = 2.94) + [S II]6716,6731 with shared velocity and width.
- Metallicity index: **Dopita et al. 2016 N2S2Hα**, y = log([N II]6583/[S II]6716+6731) + 0.264·log([N II]6583/Hα); 12+log(O/H) = 8.77 + y + 0.45(y+0.3)⁵. Chosen because all three lines are in G140M's range at z = 0.9628, are close in wavelength (dust-insensitive), and the index depends weakly on ionization.
- Errors: empirical, from line-free windows of the same width (captures drizzle correlation), propagated by Monte Carlo.

## Prediction

| Outcome | Criterion (Δ = tail − apex, dex) |
|---|---|
| **PWC pass** | Δ ≤ −0.10 **and** Δ/σ_Δ ≤ −2 in **both** reductions |
| **Against PWC** | Δ ≥ 0 with Δ/σ_Δ ≥ +1 in both reductions (tail as metal-rich as or richer than the apex) |
| Not testable | [N II]6583 or [S II] below S/N 3 in either region, or the two reductions disagree in sign |

## Known bias, stated before running

The apex is shock-excited (high [O III]/Hα, elevated [S II]). Shocks raise [S II] relative to [N II], which lowers N2S2Hα at the apex. That biases the apex **low**, and so works **against** a PWC pass. Reported regardless, with [S II]/Hα per region so the excitation difference is visible.

## Result (2026-09-29, run after commit bc95fad; code `metallicity_test.py`)

| Reduction | Region | S/N Hα / [N II] / [S II] | [N II]/Hα | [S II]/Hα | 12+log(O/H) N2S2Hα |
|---|---|---|---|---|---|
| v1 (no bkg) | apex | 5.1 / 0.4 / 0.0 | — | — | undetected |
| v1 (no bkg) | tail | 4.3 / 0.0 / 1.6 | — | — | undetected |
| v2 (bkg = other pointing) | apex | 6.4 / 3.3 / 6.0 | 0.48 | 1.42 | 8.21 (8.00–8.38) |
| v2 (bkg = other pointing) | tail | 11.6 / 10.9 / 15.9 | 0.91 | 2.17 | 8.38 (8.32–8.43) |

v2: Δ = tail − apex = **+0.17 ± 0.19 dex** (0.9σ; P(Δ<0) = 0.17).

**Verdict by the frozen rule: NOT TESTABLE.** [N II] and [S II] are undetected in v1, so the two reductions cannot be compared.

- v2 alone leans against dilution (tail slightly richer), but at 0.9σ, below the ≥1σ-in-both bar for "against".
- v2's [S II]/Hα of 1.4–2.2 is far outside the H II-region range the N2S2Hα calibration was built on (typically < 0.4; shocks ~0.5–1). This gas is shock/mixing-excited, so the index is not a reliable metallicity here, and v2's background method is already known to distort fluxes (RESULTS.md, ghosts). The v2 number is recorded, not claimed.

**What would make it testable:** the publishing team's clean cubes (van Dokkum et al., on request), or deeper spectra further down the 62 kpc tail, beyond this IFU's first ~20 kpc, where the gas has cooled out of the shock regime. A temperature-based (direct) metallicity would also need [O III]4363 or [N II]5755, which this setup does not reach cleanly.

## Method addendum (2026-09-29, declared BEFORE running; prediction and criteria unchanged)

v1 lacks [N II]/[S II] detections and v2's cross-pointing background is known to distort ratios. Adding **v3**: the v1 cube (no cross-pointing subtraction) with a **sky-spaxel background** removed per channel — median of spaxels at |y| > 1.0″ from the wake axis, after the same running-median continuum subtraction. The "both reductions" rule now means **v2 and v3**. If v3 also fails S/N 3 on [N II] or [S II], the verdict stays NOT TESTABLE.

## v3 result (sky-spaxel background, 2072 sky spaxels)

| Region | S/N Hα / [N II] / [S II] |
|---|---|
| apex | 5.3 / 0.5 / 0.0 |
| tail | 3.9 / 0.0 / 1.7 |

[N II] and [S II] are undetected again, the same as v1. **Verdict: NOT TESTABLE** (unchanged).

Two cleaner reductions agree that these lines are below the noise, so v2's strong [N II] and [S II] (and its implausible [S II]/Hα ≈ 2) are most likely produced by the cross-pointing subtraction, not real emission. **The v2 numbers should not be used.** This IFU data cannot measure the tail's metallicity. A test needs deeper or further-downstream spectra.
