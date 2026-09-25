# Prediction frozen before scoring — KiDS-1000 weak-lensing RAR (Jaden, 2026-09-25)

Data: Brouwer et al. 2021 (A&A 650, A113), KiDS public release `brouwer2021_rar.tar`: isolated KiDS-bright lenses
(Fig-4-5-C1 Nobins, 15 g_bar bins) with full covariance; also the hot-gas variant (Fig-4) and colour bins (Fig-8: early vs late).
g_obs = 4G·ESD_t/bias (B21 Eq. 7, as prescribed in the release README); covariance / bias, scaled the same way.
Models, all constants locked, nothing refitted:
- PWC: g = g_bar + √(a₀·g_bar), a₀ = 6.6776×10⁻¹¹, shared = 0 (isolated lenses — nothing outside loads the medium)
- Base: same form, a₀ = 7.5586×10⁻¹¹
- McGaugh RAR: a₀ = 1.1603×10⁻¹⁰
Score: χ² with the full covariance, 15 points, no free parameters.
**Prediction:** PWC χ² no worse than McGaugh's (Δχ² = χ²_PWC − χ²_McG ≤ 0).
**Recorded before scoring (arithmetic):** in the deep regime PWC sits √(6.68/11.6) → ~0.12 dex below McGaugh.
**Frozen caveat (Jaden):** B21 converts lensing to g_obs assuming GR lensing; PWC lensing is refraction (pressure term + geometric term, T11). If PWC sits systematically ~0.12 dex below McGaugh, that gap is logged as the derivation target for PWC's lensing rule. (T11's factor 2 matches GR's in the weak field, so the conversion is expected to carry over.)

## Outcome — FAILED on the main dataset
χ² (15 points, full covariance, no free parameters):
| Sample | PWC | Base | McGaugh | Δχ²(PWC−McG) | median log(model/obs) PWC / McG |
|---|---|---|---|---|---|
| KiDS isolated (main) | 304.1 | 257.6 | 125.7 | +178.4 | −0.234 / −0.127 |
| + hot gas (B21 estimate) | 317.4 | 315.4 | 405.0 | −87.6 | −0.127 / −0.030 |
| blue (colour) | 27.2 | 24.7 | 26.7 | +0.5 | −0.030 / +0.058 |
| red (colour) | 311.5 | 278.9 | 177.3 | +134.2 | −0.290 / −0.181 |
| disc (Sérsic) | 26.3 | 21.1 | 13.5 | +12.8 | −0.091 / +0.022 |
| bulge (Sérsic) | 240.2 | 212.9 | 129.9 | +110.3 | −0.312 / −0.197 |
Main-sample prediction (Δχ² ≤ 0) failed: PWC sits 0.23 dex below the lensing data (McGaugh 0.13 below) — ~0.11 dex worse than McGaugh, as the arithmetic expected.
Blue/disc galaxies: PWC ≈ McGaugh and both fit (χ² ~ 25 for 15 points). Red/bulge galaxies: every model falls well short (B21's own finding: early types show ~0.1–0.2 dex more lensing).
With B21's hot-gas estimate added to g_bar, PWC beats McGaugh (−87.6) but every model fits badly.
Reading (post-hoc, not a pass): the deficit is concentrated in red/bulge galaxies. PWC §0 says ellipticals are confined by the cosmic web — i.e. "isolated" lenses (no brighter neighbour within 3 Mpc) are still loaded from outside by the web, so shared = 0 is not their state. Test: derive the web loading for ellipticals before refitting anything.
