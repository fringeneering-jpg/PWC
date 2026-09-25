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
