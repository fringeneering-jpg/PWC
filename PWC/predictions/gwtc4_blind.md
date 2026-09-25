# Predictions frozen before touching GWTC-4.0 data (Jaden, 2026-09-25)

Recipe exactly as in PWC.md §3/§8, k = 0.868899 NOT refitted; GWTC-4.0 masses used as published (single source, source frame).
Events: GWTC-4.0 events not in GWTC-1/2.1/3 (the 89 already used); binary black holes only (m2 ≥ 3 M☉, as before).
- Cores: C + k·C^(2/3) = m_i → C1, C2; C_f = C1 + C2 (cores conserved).

## Test A — blind merger rule
Predicted M_f = C_f + k·C_f^(2/3); deviation = (pred − obs)/obs.
Predictions: (1) mean deviation within ±2%; (2) std ≤ 2.5% (89-event run: −0.97% ± 2.02%);
(3) deviation shrinks with core mass: corr(C_f, deviation) > 0 (89-event run: +0.624).

## Test B — ρ_max universality
ρ_shell = (M_f,obs − C_f) / [4/3 π (r₊³ − r_core³)], r₊ = (GM_f/c²)(1 + √(1 − χ_f²)), r_core = (3C_f / 4πρ_nuc)^(1/3), ρ_nuc = 2.3×10¹⁷ kg/m³.
Prediction (Jaden): ρ_shell is the same for every event — no trend with mass; scatter consistent with mass/spin uncertainties.
Pass: |log-log slope of ρ_shell vs M_f| < 0.3 and median within a factor 2 of 1.304×10¹⁵ kg/m³.

**Recorded before running (Claude):** with this recipe M_grad ∝ C^(2/3) while the shell volume ∝ r₊³ ∝ M³, so at similar spins ρ_shell is expected to scale roughly as M^(−7/3) — i.e. the recipe as written is structurally expected to FAIL universality. The run measures whether that holds in the data; the prediction is not changed.

## Outcome
84 GWTC-4.0 binary black holes (all O4a, none in the earlier 89). Final spin for B from Rezzolla et al. 2008 fit (not published in GWOSC summaries).

**Test A — all three predictions PASSED as written:** mean deviation −0.56% (±2% ✓), std 1.62% (≤2.5% ✓), corr(C_f, dev) = +0.829 (>0 ✓); 61/84 within ±2%; worst GW231123 +3.8%, GW230630 −3.7%, GW230712 −3.5%.
**Mechanism check on the trend (added after the run):** radiated fraction (m1+m2−M_f)/(m1+m2) by total mass —
observed 3.6% / 4.3% / 4.7% / 5.2% (M_tot <30 / 30–60 / 60–100 / >100), log-slope +0.18;
PWC rule 6.3% / 5.0% / 4.4% / 3.8%, log-slope −0.27 (the rule's deficit ∝ C^(2/3), so its fraction falls as M^(−1/3)).
The positive deviation–mass correlation is the rule's radiated fraction falling with mass while the data's does not: calibrated near GW150914 (~65 M☉) the rule over-radiates light systems and under-radiates heavy ones. So prediction 3 passed, but it reads as the rule's mass scaling missing the data, not as a separate physical regime.

**Test B — FAILED:** ρ_shell median 1.59×10¹⁵ kg/m³ but range 6.7×10¹³ – 8.7×10¹⁶ (×1,300); log-log slope vs M_f = −2.52 (pass needed |slope| < 0.3), Spearman −1.00; medians by M_f bin: 3.4×10¹⁶ (<25), 7.4×10¹⁵ (25–45), 1.6×10¹⁵ (45–70), 6.4×10¹⁴ (>70). As expected from the recipe (≈ M^(−7/3)): with the shell's outer edge set at the horizon, ρ_max cannot be universal. A universal ceiling needs the shell edge set by ρ_max itself ("thicker, not denser"), not by the horizon.
