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
