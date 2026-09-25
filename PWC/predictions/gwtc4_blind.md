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
