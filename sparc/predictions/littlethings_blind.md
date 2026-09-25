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
