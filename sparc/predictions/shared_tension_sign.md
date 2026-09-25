# Frozen prediction — shared-tension sign (2026-09-25)

Model: g_pred = g_bar + sqrt(a0*g_bar) * [1 + s * min(g_in, g_out)/g_in]
- min(g_in, g_out)/g_in = how tight the medium already is where the body passes (pulled from both sides).
- Jaden's mechanism: a body only pulls the medium within its own reach; if that share is already tight,
  its pull is more effective.

PREDICTION (frozen before the run): s > 0, and galaxy-balanced scatter drops below the base formula's.
Failure: s <= 0, or no scatter improvement.
s and a0 fitted on training galaxies only; sign of s left free.
