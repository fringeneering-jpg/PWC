# Prediction frozen before run — bulge-pinned tension (Jaden, 2026-09-25)

pin(R) = 0.7*Vbul^2 / Vbar^2  (bulge share of the normal pull at R; 0 where no bulge; UPS_B = 0.7 as in pipeline)
U(R)   = |g_in - g_out| / (g_in + g_out)   (ring term, as in jaden_u_tension.py)
A (full U):      T = max(pin, U)
B (pin alone):   T = pin
g_pred = g_bar + sqrt(a0*g_bar) * [1 + s*T];  a0, s fitted on training galaxies only.
Jaden's pipeline + galaxy-balanced metric, same 10 seeds, 70/30. 31 of 149 galaxies have a bulge.

Predictions (both A and B):
1. s > 0 (full sample and held-out splits).
2. Beats base on the 31 bulge galaxies (full-sample mean galaxy RMS).
