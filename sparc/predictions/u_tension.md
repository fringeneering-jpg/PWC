# Prediction frozen before run — U-shaped tension (Jaden, 2026-09-25)

Model: g_pred = g_bar + sqrt(a0*g_bar) * [1 + s * T],  T = |g_in - g_out| / (g_in + g_out)
- Centre: pinned (maxed BH/bulge side) -> one-sided -> tight.
- Middle: inner and outer pulls balance -> loosest.
- Edge: only normal gravity pulling on the medium as mass moves through -> one-sided -> tight.
Rings/g_in/g_out as in jaden_tension_differential.py. a0, s fitted on training galaxies only.
Jaden's pipeline + galaxy-balanced metric, same 10 seeds, 70/30.

Predictions:
1. s > 0 (full sample and held-out splits).
2. Beats the static shared-tension version (jaden_shared_tension.py) on spirals (early + late, full-sample mean).
