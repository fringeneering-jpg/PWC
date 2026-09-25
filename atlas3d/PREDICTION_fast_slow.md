# Prediction frozen before running — still vs moving ellipticals (Jaden, 2026-09-25)

Mechanism (Jaden): a moving (rotating) galaxy's medium keeps letting go and grabbing the next mass, never at full tension; a still galaxy's medium stays at peak tension → more extra pull.
Data: ATLAS3D 260 early-type galaxies — Emsellem+2011 Table B1 (λ_Re, fast/slow class F/S_e), Cappellari+2013a Paper XV Table 1
(log(M/L)_JAM r-band, log L_r, log σ_e, quality), Cappellari+2013b Paper XX Table 1 (log(M/L)_stars r-band, f_DM(R_e)).
Extra-pull measures: (A) log(M/L)_JAM − log(M/L)_stars (dynamical over stellar, within ~R_e); (B) f_DM(R_e).
Controls: log M★ = log(M/L)_stars + log L_r, and log σ_e (σ tracks the known IMF/M-L trend). JAM quality > 0 only.
Test: OLS  measure = a + b·logM★ + c·logσ_e + d·[slow]; one-sided test d > 0.
**Prediction:** d > 0 at p < 0.05 for measure (A); same sign for (B).
Also reported: raw medians slow vs fast, and λ_Re as a continuous variable (prediction: coefficient < 0).
Caveats: extra pull inside ~1 R_e is small (g ≫ a₀ in many cores); JAM assumes mass follows light; stellar M/L from population synthesis.

## Outcome — FAILED as frozen
187 galaxies with JAM quality > 0 (21 slow, 166 fast).
Controlled for stellar mass and σ_e: slow-rotator coefficient d = +0.009 ± 0.018 (A: log M/L dyn/stellar; p = 0.31) and +0.010 ± 0.032 (B: f_DM; p = 0.38) — no detectable extra pull for still galaxies.
λ_Re (continuous) runs the other way for (A): +0.059 ± 0.029 (t = +2.1) — more rotation, slightly more extra pull.
Raw f_DM is higher for slow rotators (0.140 vs 0.105) but they are ~3.6× more massive (median log M★ 11.13 vs 10.57); at matched mass the difference disappears (A: +0.054 vs +0.048).
Scope: this probes within ~1 R_e (a few kpc), not the 100 kpc–Mpc scales where KiDS found the red-galaxy excess. The KiDS red/blue gap is therefore not explained by stillness at the R_e scale; environment (web loading) or scale remain open.

## CORRECTION (2026-09-25) — the first outcome used the wrong column; corrected result PASSES
The "stellar M/L" column (Paper XX logML_star) is the JAM M/L × (1 − f_DM) — dynamical, not from starlight (verified to 0.009 dex). So measures A and B were both the dynamical model's own halo fraction. Corrected measure C = log(M/L)_JAM − log(M/L)_Salp (dynamics vs stellar-population M/L from the light), same controls (log M★ from the population M/L, log σ_e):
slow coefficient +0.061 ± 0.030, t = +2.04, one-sided p = 0.022 → **prediction met (d > 0 at p < 0.05)**. Still galaxies show more extra pull than rotating ones at the same mass and σ. λ_R continuous: +0.035 ± 0.050 (not significant). Script: corrected_extra_pull.py.


## Audit status: corrected pass is meaningful but not decisive — inner-R_e dynamics, 21 slow rotators; not a large-radius test.
