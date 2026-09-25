# Prediction frozen before running — medium viscosity set by heat: star formation / age (Jaden, 2026-09-25)

Mechanism: heat thins the medium; cool (quenched, old) galaxies leave it thick → more grip / extra pull.
Data: ATLAS3D. Heat proxy: SSP-equivalent age within R_e (McDermid+2015 Paper XXX Table 3; luminosity-weighted, most sensitive to recent star formation = heat output); secondary: mass-weighted age (Table 4).
Extra pull: (A) log(M/L)_JAM − log(M/L)_stars (Papers XV, XX); (B) f_DM(R_e). Controls: log M★, log σ_e. JAM quality > 0; SSP quality flag as given.
Test: OLS measure = a + b·logM★ + c·logσ_e + d·log(Age); one-sided d > 0.
**Prediction:** d > 0 at p < 0.05 for (A) with SSP age; same sign for (B) and for mass-weighted age.
Caveats: probes within ~1 R_e (where the ATLAS3D spin test was null); (M/L)_stars is itself age-dependent (A divides it out); IMF variation correlates with σ (controlled).

## Outcome — FAILED; the sign is reversed
187 ETGs (first parse misread rows with a missing Fe5270 index; fixed before reporting, no model change).
Age coefficient at fixed log M★ and log σ_e (prediction d > 0):
SSP age: A −0.052 ± 0.027 (t = −1.9), f_DM −0.066 ± 0.049 (t = −1.3); mass-weighted age: A −0.114 ± 0.048 (t = −2.4), f_DM −0.156 ± 0.086 (t = −1.8).
Terciles (SSP age 5.3 / 10.2 / 14.6 Gyr): median A +0.074 / +0.037 / +0.051; f_DM 0.140 / 0.080 / 0.095.
Within ~1 R_e, younger (hotter, more recently star-forming) early-types show MORE extra pull than older ones at the same mass and σ, at ~2σ — opposite to "cool = thicker = more grip".
Note (post-hoc, not a rescue): PWC §1 states heat is the pull; this result runs in that direction. Caveat: A divides by population-synthesis M/L, which is least certain for young populations.

## CORRECTION (2026-09-25) — wrong column (see PREDICTION_fast_slow.md); corrected result still opposite, but confounded
With C = log(M/L)_JAM − log(M/L)_Salp: SSP age coefficient −0.231 ± 0.045 (t = −5.1); mass-weighted −0.494 ± 0.076 (t = −6.5). Older → less extra pull, strongly.
Confound: the population M/L rises steeply with age by construction of the stellar models, so an age trend in C is dominated by how well those models (and the assumed IMF) weigh old vs young stars. This test cannot cleanly separate heat from stellar-model systematics; it does not support the "cool = more grip" prediction, and it cannot be read as a clean refutation either.
