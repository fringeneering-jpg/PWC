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

## Outcome — FAILED as frozen; model as described NOT tested

- s = -0.1115 full sample (a0 8.6986e-11); negative on all 10 splits (-0.05 to -0.17). Prediction 1 failed.
- Spirals (n=90): U 0.1192 vs static shared 0.1185 vs McGaugh 0.1090. Prediction 2 failed.
- Full: U 0.13145 | static 0.13089 | base 0.13273 | McGaugh 0.12895. Held-out: U 0.1317 | static 0.1311 | base 0.1326 | McGaugh 0.1283; U beats static 2/10.

NOTE: the formula did not produce the U shape. Median T by radius (inner->outer fifths):
0.38, 0.49, 0.58, 0.68, 0.95 -- a monotonic ramp, loosest at centre. Ring geometry alone does not
make the centre one-sided, so the pinned centre never appeared. This run tests "extra boost where the
edge is tight" (disfavoured), not Jaden's U. Next: pin the bulge explicitly (approved by Jaden).
