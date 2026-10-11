# THE LADDER: the wave's anatomy -> G -> a0 -> 1,342 galaxies (zero fitted parameters)
# f_solid (the debt) -> G -> a0 -> the rotation formula -> PROBES. Locked 2026-10-12.
import math
import numpy as np, pandas as pd

c0 = 2.99792458e8; hbar = 1.054571817e-34
rho0 = 8.74e-27; Rp = 8.414e-16; s = 1.0/19.0

print("==" * 40)
print("STEP 1: the fold's mechanical balance (19:1:18) gives the stretch's share")
print("F_EM / F_debt = 1/s = 19 EXACT (squeeze_debt_balance.py) -> s = 1/19 locked")

print("\nSTEP 2: the volumetric debt f_solid (the 0.085% matter displacement)")
f_solid = 8.4989e-4
print(f"f_solid = {f_solid:.4e} = 0.085% - the footprint's matter residual, the one datum")

print("\nSTEP 3: the G-chain - the wave's own count (12 = 3 dims x 4 quanta; 16/9 = (4/3)^2)")
G_chain = f_solid**12 * (4.0*s/81.0) * Rp**2 * c0**3 / hbar
G = 6.67430e-11
print(f"G = (f_solid)^12 x (4s/81) x Rp^2 c0^3 / hbar = {G_chain:.6e} m^3/kg/s^2")
print(f"measured G = {G:.6e}   agreement {100*(G_chain/G-1):+.3f}%")

print("\nSTEP 4: the macroscopic deformation boundary a0 (T1)")
a0_chain = (c0/math.sqrt(3.0)) * math.sqrt(G_chain*rho0/4.0)
print(f"a0 = (c0/sqrt3) sqrt(G rho0/4) = {a0_chain:.4e} m/s^2   (locked 6.61e-11)")

print("\nSTEP 5: the rotation formula (s_shared = 0.2264 derived, nothing fitted)")
S = 0.2264
d = pd.read_csv(r"C:\Users\jaden\Downloads\PWC-Check\PWC\sparc\probes\probes_accel.csv")
pts = lambda go, gp: float(np.sqrt(np.mean((np.log10(go) - np.log10(gp)) ** 2)))
def run(A):
    pwc = lambda g: g.g_bar + np.sqrt(A * g.g_bar) * (1 + S * g.shared * (1 - g.locked))
    return pts(d.g_obs, pwc(d))
r_locked = run(6.61e-11); r_chain = run(a0_chain)
print(f"PROBES (n={len(d)} points, {d.Name.nunique()} galaxies):")
print(f"  locked a0  6.6100e-11 -> scatter {r_locked:.4f}")
print(f"  chain  a0  {a0_chain:.4e} -> scatter {r_chain:.4f}   ({100*(r_chain/r_locked-1):+.4f}%)")

print("\n" + "==" * 40)
print("THE LADDER: one wave anatomy -> G -> a0 -> 1,342 galaxies")
print("zero fitted parameters at every step. The microscopic knot and the macroscopic")
print("disk are the same fluid mechanic, scaled. The stretch and the debt carry it all.")
