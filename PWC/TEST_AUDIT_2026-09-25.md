# PWC test audit — 2026-09-25 (for independent checking)

Every test run today: data source, script, frozen prediction (timestamped git commit before the run), outcome, and what a checker should verify. Repo: https://github.com/fringeneering-jpg/PWC (all paths relative to repo root).

**Known error already found and corrected:** the ATLAS3D spin and heat tests first used Cappellari+2013b `logML_star` as "stellar-population M/L", but that column is the JAM M/L × (1 − f_DM) (dynamical). Corrected measure: log(M/L)_JAM − log(M/L)_Salp. See `atlas3d/corrected_extra_pull.py`.

| # | Test | Script | Frozen prediction | Outcome |
|---|---|---|---|---|
| 1 | SPARC shared tension (10 splits) | `sparc/jaden_shared_tension.py` | `sparc/predictions/shared_tension_sign.md` | s > 0 on all splits — passed |
| 2 | LITTLE THINGS blind (16) | `sparc/jaden_littlethings_blind.py` | `sparc/predictions/littlethings_blind.md` | passed (noisy) |
| 3 | GHASP blind (81) | `sparc/jaden_ghasp_blind.py` | `sparc/predictions/ghasp_blind.md` | passed narrowly |
| 4 | PROBES blind (1342) | `sparc/jaden_probes_blind.py` | `sparc/predictions/probes_blind.md` | passed (beats McGaugh 1.7%) |
| 5 | PROBES M/L 0.4/0.6 | `sparc/jaden_probes_ml_robustness.py` | `sparc/predictions/probes_ml_robustness.md` | passed at both |
| 6 | PROBES + ALFALFA gas (331) | `sparc/jaden_probes_gas.py` | `sparc/predictions/probes_gas.md` | passed |
| 7 | Void thermal edge | `voids/thermal_edge_test.py` | `voids/PREDICTION_thermal_edge.md` | failed (no signal) |
| 8 | GWTC-4.0 merger rule (84) | `PWC/gwtc4_blind_tests.py` | `PWC/predictions/gwtc4_blind.md` | A passed; B (ρ_max universal) failed |
| 9 | Shell vs choke | `PWC/gwtc4_shell_vs_choke.py` | `PWC/predictions/gwtc4_shell_vs_choke.md` | failed |
| 10 | Ringdown mass (assumed profile) | `PWC/gwtc4_ringdown_mass.py` | `PWC/predictions/gwtc4_ringdown_mass.md` | withdrawn (un-derived profile) |
| 11 | BH flow profile | `PWC/bh_flow_profile.py` | `PWC/predictions/bh_flow_profile.md` | withdrawn (medium does not inflow) |
| 12 | GWTC-5.0 merger rule (104) | `PWC/gwtc5_blind_test.py` | `PWC/predictions/gwtc5_blind.md` | passed |
| 13 | Compressibility β | `PWC/compressibility_beta.py` | `PWC/predictions/compressibility_beta.md` | numbers passed, core driven to ~0 — not a measurement |
| 14 | KiDS lensing RAR | `kids/kids_lensing_test.py` | `kids/PREDICTION_kids_lensing.md` | failed on main sample; blue ≈ McGaugh, red excess |
| 15 | Fast vs slow (ATLAS3D) | `atlas3d/corrected_extra_pull.py` | `atlas3d/PREDICTION_fast_slow.md` | corrected: passed (still > spinning, p = 0.022) |
| 16 | Red vs still (Lelli ETGs) | `lelli_etg/red_vs_still_test.py` | `lelli_etg/PREDICTION_red_vs_still.md` | failed; stellar M/L caveat |
| 17 | Heat / age (ATLAS3D) | `atlas3d/corrected_extra_pull.py` | `atlas3d/PREDICTION_heat_age.md` | opposite; confounded by population M/L |
| 18 | Colour / cold (ATLAS3D) | `atlas3d/colour_cold_test.py` | `atlas3d/PREDICTION_colour_cold.md` | flat (−0.12 ± 0.20, no control); ambiguous in all-red sample |

## What a checker should verify
1. **Column meanings** in every catalogue read (the ATLAS3D error was exactly this). Check each against the source ReadMe/table header.
2. **Sign conventions:** deviation = (model − observed)/observed in the merger tests; "median log(model/obs)" in KiDS (negative = model too low); C and f_DM higher = more extra pull in ATLAS3D.
3. **Units:** SPARC/PROBES/GHASP g in m/s²; KiDS g_obs = 4G·ESD/bias (Brouwer 2021 README); rotation curves km/s, kpc.
4. **Frozen before run:** compare each prediction file's commit time with the results commit (`git log`).
5. **Ring geometry** (`sparc/jaden_tension_differential.py`): shared = min(g_in, g_out)/g_in from each galaxy's own baryons.
6. **Controls in ATLAS3D regressions** (mass, σ) — whether they remove the effect being tested (raised by Jaden for the colour test).
7. **Merger catalogue final masses** come from GR remnant formulas, not independent measurements.
