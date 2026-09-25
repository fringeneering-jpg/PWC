# Prediction frozen before running — red vs still: Lelli 2017 early-type galaxies (Jaden, 2026-09-25)

Learned on KiDS (red colour bin 2, isolated lenses, s = 0 form): a₀,red = 2.7286×10⁻¹⁰ (4.09× the spinning a₀), χ² 42.1 / 15 pts.
Test set: Lelli et al. 2017 ETGs with HI rotation curves (Rotmod_ETG, 16 galaxies; ATLAS3D: 14/15 fast rotators, NGC 3522 slow, UGC 6176 unclassified).
Models (full PWC form as on SPARC: g_bar + √(a₀ g_bar)[1 + s·shared·(1 − locked)], s = 0.2264, shared from ring geometry, locked = bulge share; Υ_disk 0.5, Υ_bulge 0.7):
- Spinning calibration: a₀ = 6.6776×10⁻¹¹ (SPARC)
- Red-learned: a₀ = 2.7286×10⁻¹⁰ (KiDS red)
Metric: galaxy-balanced RMS in log g_obs.
**Prediction (Jaden's mechanism — spin, not colour, takes weight off):** for the 15 spinning ETGs, the spinning calibration scores lower RMS than the red-learned a₀.
Reported separately (n = 1, not a test): NGC 3522 (slow) — mechanism expects it to prefer the red-learned a₀.

## Outcome — FAILED as frozen
Each galaxy has 2 points (inner and outer HI radius), 16 galaxies.
Spinning ETGs (15): galaxy-balanced RMS — spinning a₀ 0.207 vs KiDS-red a₀ 0.169; spinning calibration better in only 7/15. Median log(g_obs / PWC_spin) ≈ +0.15: these red-but-spinning galaxies show more pull than the spinning calibration predicts, closer to the red-learned value.
NGC 3522 (slow, n = 1): 0.204 (spinning) vs 0.192 (red) — slight preference for red a₀, not a test.
Reading: in this small sample, being red/early-type goes with extra pull even when the galaxy spins — spin alone does not remove it.
Caveat (stated after the run, not a rescue): stellar M/L was frozen at the late-type values (Υ_disk 0.5, Υ_bulge 0.7). Old early-type discs have higher 3.6 µm M/L; if the true values are higher, g_bar rises and the needed extra pull shrinks. A sensitivity rerun at higher Υ would show how much of the excess is stellar-mass bookkeeping.
