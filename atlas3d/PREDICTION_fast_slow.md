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
