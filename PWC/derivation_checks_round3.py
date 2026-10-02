"""Checks for DERIVATIONS.md rows 19-22 (2026-10-02). Newtonian 1/r^2 and wave-equation algebra only; no GR formula.
 1. yield a_max measured by the merger energy balance over 193 events (89 explored + 104 GWTC-5), nothing else fitted
 2. Lorentz contraction of a moving solution of a wave equation (sine-Gordon kink, c = 1)
 3. gravitational redshift from the photon doing work at its speed limit: dL = -V dP, V = L/(rho c^2), dP = rho g dr
 4. Shapiro-delay requirement against the medium's compression (c_s^2 = c^2/3) and light-speed exponent
"""
import numpy as np
import pandas as pd
import merger_energy_balance as m

G, C0, MS = m.G, m.C0, m.MS
ev = pd.concat([m.DEV, m.OUT], ignore_index=True)
ev["Mt"] = ev.m1 + ev.m2


def err(a):
    edge = lambda x: np.sqrt(G * x * MS / a)
    e = G * (ev.m1 * MS) * (ev.m2 * MS) / (2 * (edge(ev.m1) + edge(ev.m2)) * C0 ** 2) / MS
    return (ev.Mt - e - ev.Mf) / ev.Mf * 100


print("1. yield from the mergers (E alone, a_max scanned):")
A = np.logspace(np.log10(5e10), np.log10(3e12), 400)
mae = np.array([err(a).abs().mean() for a in A])
print("   best a_max = %.3e (mean|err| %.2f%%); repo 3.23e11 gives %.2f%%" % (A[mae.argmin()], mae.min(), err(3.23e11).abs().mean()))
for M in (14., 62., 238.):
    print("   M = %5.0f Msun: sqrt(GM/a_max)/(GM/c^2) = %.3f (a Kerr horizon is between 1 and 2)" % (M, np.sqrt(G * M * MS / 3.23e11) / (G * M * MS / C0 ** 2)))

print("2. Lorentz contraction: sine-Gordon kink moving at 0.6 c")
v = 0.6
gam = 1 / np.sqrt(1 - v * v)
f = lambda x, t: 4 * np.arctan(np.exp(gam * (x - v * t)))
h, X0, T0 = 1e-3, 0.3, 0.2
utt = (f(X0, T0 + h) - 2 * f(X0, T0) + f(X0, T0 - h)) / h ** 2
uxx = (f(X0 + h, T0) - 2 * f(X0, T0) + f(X0 - h, T0)) / h ** 2
print("   u_tt - u_xx + sin(u) = %.1e (0 expected); width ratio moving/static = 1/gamma = %.3f" % (utt - uxx + np.sin(f(X0, T0)), 1 / gam))

print("3. gravitational redshift: L(r2)/L(r1) = exp(-GM(1/r1 - 1/r2)/c^2); the lost energy becomes medium")
print("   Pound-Rebka h = 22.5 m: gh/c^2 = %.3e (measured 2.5e-15)" % (9.80665 * 22.5 / C0 ** 2))
for x in (0.1, 0.2, 0.3):
    print("   x = %.1f: PWC z = %.3f ; GR z = %.3f ; fraction converted to medium (point mass only: a LOWER BOUND, the medium's own pull adds) = %.3f"
          % (x, np.exp(x) - 1, (1 - 2 * x) ** -0.5 - 1, 1 - np.exp(-x)))

print("4. Shapiro: need n - 1 = 2GM/(r c^2); medium compression with c_s^2 = c^2/3 is d_rho/rho = 3GM/(r c^2)")
for p in (0.5, 2 / 3):
    print("   light speed ~ rho^-%.3f: delay = %.0f%% of the measured value" % (p, 3 * p / 2 * 100))
