# Prediction frozen before scoring — PROBES blind test (Jaden, 2026-09-25)

Data: PROBES-I (Stone+2022, Zenodo 10456320; raw at D:/probes). Built by sparc/probes_build.py -> sparc/probes/probes_accel.csv
(no model scored during build). 1342 galaxies, ~23.7k binned points, after removing SPARC/GHASP overlaps (60" match + RC_survey tag "SPARC").
Stars from unWISE W1 profiles, M/L 0.5 (SPARC disc value), thin-disc ring gravity (h = 0.2 kpc). No gas; no bulge split -> locked = 0.
Inclination from r-band outer isophote (q0 = 0.2), 30-85 deg. Sanity: median log(g_obs/g_bar) = 0.50, 5% points g_bar > g_obs.

Model: g_bar + sqrt(a0*g_bar)*[1 + s*shared*(1-locked)]; shared = min(g_in,g_out)/g_in from the same rings.
ALL constants locked from SPARC: s = 0.2264, a0 = 6.6776e-11; base a0 = 7.5586e-11; McGaugh a0 = 1.1603e-10.
Metric: galaxy-balanced (mean of per-galaxy RMS in log g).

Predictions:
1. Beats base.
2. Tension term helps: s = 0.2264 beats s = 0 at the same a0.
3. Gap to McGaugh no worse than SPARC (+1.3%).

## Outcome — all three PASSED
ALL 1342: PWC 0.2931 | s=0 (same a0) 0.3050 | base 0.2986 | McGaugh 0.2982. Beats base 988/1342, McGaugh 821/1342, tension helps 1001/1342.
Gap to McGaugh -1.7%; bootstrap 95% (PWC - McGaugh) [-0.0063, -0.0039]; (PWC - s=0) [-0.0128, -0.0110].
By type: ahead of McGaugh in Sab, Sb, Sbc, Sc; level in Scd.
Fairer tension comparison is vs base (s=0 at its own SPARC a0): 0.2931 vs 0.2986 (-1.8%), 988/1342.
Caveats: no gas; stars only at fixed M/L 0.5; locked = 0 (no bulge split); scatter ~0.29 dex.
