# Frozen prediction — shared-tension sign (2026-09-25)

Model: g_pred = g_bar + sqrt(a0*g_bar) * [1 + s * min(g_in, g_out)/g_in]
- min(g_in, g_out)/g_in = how tight the medium already is where the body passes (pulled from both sides).
- Jaden's mechanism: a body only pulls the medium within its own reach; if that share is already tight,
  its pull is more effective.

PREDICTION (frozen before the run): s > 0, and galaxy-balanced scatter drops below the base formula's.
Failure: s <= 0, or no scatter improvement.
s and a0 fitted on training galaxies only; sign of s left free.

## Outcome (run after commit aa36854) — PASSED

- s = +0.188 on the full sample; positive on all 10 held-out splits (+0.09 to +0.27).
- Galaxy-balanced scatter (Jaden's metric): full 0.1309 vs base 0.1327; held-out mean 0.1311 vs base 0.1326; beats base on 10/10 splits.
- vs McGaugh RAR: full 0.1309 vs 0.1290; held-out 0.1311 vs 0.1283; beats McGaugh 2/10 splits.
- By type: beats McGaugh on irregular/BCD dwarfs (20/28) and Magellanic Sm (19/31); trails on early (9/27) and late spirals (19/63).
- On the 15 galaxies McGaugh fits worst, the shared-tension model fits 10 better.
Script: sparc/jaden_shared_tension.py; results: sparc/jaden_shared_tension_results.json.
