# FRB = re-tensioning snap — math check

**Script:** `scratch/frb_snap_check.py` (run with bundled Python; output verified by hand).
**Locked inputs:** ρ_max = 1.304×10¹⁵ kg/m³ · Y_bow = 5.93×10²⁶ Pa · c₀ = 2.998×10⁸ m/s ·
v_max(ρ)=√(2Y/ρ) (→ 954 km/s at ρ_max, repo ✓) · collapse clocked at c₀ (DERIVATIONS.md Gaps: "release of stored tension is clocked at c₀") ·
GW150914: 3 M☉ over 4.68 ms at 150 Hz, h ≈ 4×10⁻²¹.
**Framework consistency checks pass:** v_max(ρ_max) = 953.7 km/s; stagnation row reproduced exactly (R=886 km → 1910 M☉).

## Observed FRB targets
τ = 0.1–10 ms · f = 0.1–8 GHz · E = 10³¹–10³³ J · DM ≤ 3000 pc/cm³ (≈ 15 Gpc at ⟨n_e⟩=2×10⁻⁷ cm⁻³).
**Observed f·τ = 10⁴–8×10⁷.**

## The three axes, one bubble each
Hypothesis forces f = c₀/R AND τ = R/c₀ ⇒ **f·τ = 1 for any bubble radius and any speed.**

| Axis matched | Bubble radius R | Mass (at ρ_max) | What it predicts |
|---|---|---|---|
| Duration 0.1–10 ms | 30–3000 km | 0.074–74,000 M☉ | f = 100 Hz–10 kHz (GHz? **5–8 orders low**); Y·V = 10⁴⁰–10⁴⁶ J, m·c₀² = 10⁴⁶–10⁵² J (obs 10³¹–10³³: **7–19 orders high**) |
| Frequency 0.1–8 GHz | 4 cm–3 m | 3×10¹¹–1.5×10¹⁷ kg | τ = 0.1–10 ns (**5–7 orders short of ms**); m·c₀² = 2.6×10²⁸–1.3×10³⁴ J |
| Energy 10³¹–10³³ J (Y·V) | 16–74 m | 2.2×10¹⁹–2.2×10²¹ kg (10⁻¹¹–10⁻⁹ M☉) | τ = 53–250 ns; f = 4–19 MHz |
| Energy 10³¹–10³³ J (m·c₀²) | 0.27–1.27 m | 1.1×10¹⁴–1.1×10¹⁶ kg (5.6×10⁻¹⁷–5.6×10⁻¹⁵ M☉) | **f = 0.24–1.1 GHz ✓**; τ = 1–4 ns (**5–6 orders short**) |

## Merger comparison
E_gw = 3 M☉·c₀² = 5.36×10⁴⁷ J; merger f·τ = 0.70 (**obeys the snap coherence**), c₀τ = 1403 km ≈ c₀/f = 1999 km.
FRB/merger: energy ratio 10⁻¹⁷–10⁻¹⁵, frequency ratio 10⁶–5×10⁷ — the two scale factors disagree by ~22 orders, so the FRB is **not** a self-similar "micro" copy of the merger (fixed-strain rescaling: E ∝ f → merger at 1 GHz would carry ~3.6×10⁵⁴ J, 21–23 orders above the FRB band).
Energy-matched release (10¹⁴–10¹⁶ kg) is 10⁻¹⁵ of the merger's 3 M☉ and ~10⁻¹⁶ of a pulsar (1.4 M☉ = 2.8×10³⁰ kg): the mass axis is plausibly "micro". The 1-ms bubble (74 M☉) is not — it out-masses the merger's entire release.

## Robustness
Clocking the collapse at v_max(ρ_max) = 954 km/s instead of c₀: 1 ms → R = 0.95 km, 2.4×10⁻⁶ M☉ (plausible mass), but f = 1 kHz and energies 10³⁶–10⁴¹ J — still fails frequency and energy, because f·τ = 1 is speed-independent.

## Verdict (one paragraph)
The single-bubble re-tensioning snap **fails** to produce the observed FRB triple: with the locked clocking (τ = R/c₀, f = c₀/R), any snap has f·τ = 1, while FRBs have f·τ ≈ 10⁴–8×10⁷, so one collapse cannot be both millisecond-long and gigahertz-fast. Frequency and energy are jointly consistent only for a ~0.3–1.3 m bubble holding 10¹⁴–10¹⁶ kg of medium (5.6×10⁻¹⁷–5.6×10⁻¹⁵ M☉ — a comet/asteroid-scale release, genuinely "micro" next to the merger's 3 M☉), but that bubble collapses in 1–4 nanoseconds, ~10⁶× shorter than observed; conversely, the 0.1–10 ms durations require a 30–3000 km bubble holding 0.074–74,000 M☉ — a stellar-mass-to-supermassive chunk that out-masses the entire GW150914 release, radiates at 0.1–10 kHz, and carries 10⁷–10¹⁹× too much energy. The merger itself satisfies f·τ ≈ 0.7, so the analogy breaks exactly on the axis where it should hold. As stated, the hypothesis fails on the duration axis (and on the frequency axis whenever duration is honored); it survives only if the ms duration is a separate envelope (beam crossing, propagation, or many successive snaps), which is a new mechanism not contained in the R/c₀ collapse picture. (Naming note: the 2026-10-08 ruling "THE MEDIUM DOESNT SNAP" concerns Y_bow-vs-Y_coh tearing, not this collapse-back, but the word collision should be flagged when presenting.)
