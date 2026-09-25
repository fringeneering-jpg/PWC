# Prediction frozen before run — LITTLE THINGS blind test (Jaden, 2026-09-25)

Data: Oh et al. 2015 (J/AJ/149/180), sparc/littlethings/. 20 galaxies NOT in SPARC
(excluded: DDO50, DDO87, DDO126, DDO154, DDO168, NGC2366).
g_obs = Vtot^2/R (rotdmbar "Data"), g_bar = (Vtot^2 - Vdm^2)/R (rotdm "Data" = DM-only), both
de-scaled by R0.3, V0.3. Points with Vbar^2 <= 0 dropped. No bulges -> locked = 0.
NOTE: their stellar M/L from colours (not SPARC 0.5/0.7); no gas/star split; asymmetric-drift corrected.

Model: g_bar + sqrt(a0*g_bar)*[1 + s*shared*(1-locked)], shared = min(g_in,g_out)/g_in (same ring code).
ALL constants locked from SPARC full-sample fits (jaden_rebound.py free-s): s = 0.2264, a0 = 6.6776e-11.
Base and McGaugh: a0 = their SPARC full-sample fits. Nothing refitted on LITTLE THINGS.
Metric: Jaden's galaxy-balanced (mean over galaxies of per-galaxy RMS in log g).

Predictions:
1. Beats base on the 20 galaxies.
2. Gap to McGaugh no worse than on SPARC overall (SPARC full: 0.13062 vs 0.12895, +1.3%) -- i.e. within +1.3% of McGaugh or better.

## Outcome — both predictions PASSED (on noisy data)
First run had a data-read bug (DM-only file de-scaled with the total-curve factors); fixed, no model/constant change.
16 of 20 usable (DDO46, DDO47, F564-V3, Haro29 have no DM-only curve), 425 points.
Galaxy-balanced: PWC 0.3374 | base 0.3417 | McGaugh 0.3464. PWC beats base 10/16, beats McGaugh 10/16; gap -2.6%.
Caveats: scatter ~0.34 dex vs 0.13 on SPARC (baryon curve reconstructed as Vtot^2 - Vdm^2; DDO101, NGC3738, IC1613 fit badly under every model).
Diagnostic: same a0 with s=0 gives 0.3383 -> most of the gain over base is the SPARC-locked a0; shared term adds 0.3383 -> 0.3374.
