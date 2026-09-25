# Prediction frozen before run — one-material rebound (Jaden, 2026-09-25)

available = shared * (1 - locked);  shared = min(g_in,g_out)/g_in;  locked = 0.7*Vbul^2/Vbar^2
Main (1 constant): g_pred = g_bar + sqrt(a0*g_bar) * [1 + available]   (s = 1: full rebound to rest state)
Check (2 constants): same with s fitted freely.
Jaden's pipeline + galaxy-balanced metric, same 10 seeds, 70/30.

Predictions:
1. s=1 version beats base on held-out galaxies (mean over 10 splits).
2. Freely fitted s lands in [0.5, 1.5] on held-out splits.
