# Prediction frozen before running — colder is denser is thicker: colour test (Jaden, 2026-09-25)

Mechanism (Jaden): colder medium is denser and thicker → more grip / extra pull. Cold measured directly by colour: redder light = cooler stars.
Data: ATLAS3D 187 ETGs (JAM quality > 0) × RC3 (de Vaucouleurs+1991, VizieR VII/155) corrected total colour (B−V)_T⁰ (fallback (B−V)_T).
Extra pull: C = log(M/L)_JAM − log(M/L)_Salp (dynamics vs stellar-population M/L from the light — the corrected measure).
Controls: log M★ (population), log σ_e.
Test: OLS C = a + b·logM★ + c·logσ_e + d·(B−V); one-sided d > 0.
**Prediction:** redder (colder) → more extra pull: d > 0 at p < 0.05.
Caveat stated in advance: colour also enters the stellar-population M/L (redder → higher model M/L), the same kind of confound that hit the age test. A positive d survives that confound (the model M/L works against it); a negative d would be ambiguous.

## Outcome — not met; ambiguous by the pre-stated rule
128 ETGs with RC3 colours (B−V 0.60–0.99, median 0.90).
Raw terciles by colour: bluest C −0.073, middle −0.085, reddest −0.032 — the coldest third shows the most extra pull (raw direction as predicted).
Controlled for log M★ and log σ_e: d = −0.44 ± 0.22 per mag (t = −2.0) — negative, which the frozen caveat already classed as ambiguous (redder colour raises the model M/L in the denominator).
Why this sample can't decide it: ATLAS3D is all early-types — every galaxy is already red (most within 0.85–0.95), and within the red sequence colour tracks mass and metallicity, not temperature. Controlling for mass removes most of the colour spread. The real cold-vs-warm comparison is red vs blue galaxies (KiDS), where the cold ones show more lensing.
