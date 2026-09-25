# Prediction frozen before scoring — GHASP spirals blind test (Jaden, 2026-09-25)

Data: sparc/ghasp/ghasp_accel.csv built by sparc/ghasp_build.py (no model scored during build).
81 GHASP galaxies not in SPARC (15 overlaps removed by 60" coordinate match), 1238 points, 69 with bulges.
Halpha rotation curves (Epinat+2008); stars only (no HI gas); Rc-band disc + Sersic bulge (Korsaga+2019);
M/L from B-V colour (Bell & de Jong), NOT SPARC's 3.6um 0.5/0.7. Sanity: median log(g_obs/g_bar) = 0.36;
11% of points have g_bar > g_obs.

Model: g_bar + sqrt(a0*g_bar)*[1 + s*shared*(1-locked)], shared = min(g_in,g_out)/g_in (same ring code),
locked = bulge share of V^2. ALL constants locked from SPARC: s = 0.2264, a0 = 6.6776e-11;
base a0 = 7.5586e-11; McGaugh a0 = 1.1603e-10. Nothing refitted on GHASP.
Metric: galaxy-balanced (mean of per-galaxy RMS in log g).

Predictions:
1. Beats base on all 81.
2. Beats base on the 69 bulge galaxies.
3. Gap to McGaugh no worse than SPARC (+1.3%).
4. Mechanism check: the tension term helps -- s = 0.2264 beats s = 0 at the same a0.
