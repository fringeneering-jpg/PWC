# Prediction frozen before run — PROBES M/L robustness (Jaden, 2026-09-25)

Same data/model/constants as probes_blind.md (s = 0.2264, a0 = 6.6776e-11; base 7.5586e-11; McGaugh 1.1603e-10, all locked from SPARC).
Only change: stellar M/L 0.4 and 0.6 instead of 0.5. Stars are the whole baryon budget here, so g_bar scales by M/L/0.5;
shared = min(g_in,g_out)/g_in is a ratio and does not change.

Prediction: PWC beats McGaugh (galaxy-balanced mean) at BOTH M/L = 0.4 and M/L = 0.6.
(Also reported, not predicted: beats base, tension helps, bootstrap ranges.)

## Outcome — PASSED at both, lead shrinks as M/L rises
M/L 0.4: PWC 0.3194 vs McGaugh 0.3258 (-2.0%, 95% [-0.0075,-0.0053]); beats McGaugh 848/1342.
M/L 0.5: PWC 0.2931 vs McGaugh 0.2982 (-1.7%, 95% [-0.0063,-0.0039]); 821/1342.
M/L 0.6: PWC 0.2812 vs McGaugh 0.2828 (-0.6%, 95% [-0.0029,-0.0003]); 759/1342.
Every model fits better at 0.6 (baryons likely under-counted: no gas). Lead holds at all three but narrows with more baryons.
