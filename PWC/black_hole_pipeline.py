"""ONE command that rebuilds the whole black-hole pipeline from the repo (Jaden, 2026-10-02): python black_hole_pipeline.py
Run it from anywhere; it imports the scripts that sit beside it in PWC/.
 1. Single black holes (20): neutron core, Max-P edge (reach), sonic choke; plus the area-law split (core + k*C^(2/3) shell).
 2. Mergers: energy limit E, storage limit S, min(E,S), sliding-density limit, on the explored set and on GWTC-5 (never used).
 3. Light bending (pull + push), speed limit (water benchmark, Y from RBH-1).
Constants: rho_core 2.3e17, rho_max 1.304e15, a_max 3.23e11 (origin of a_max: see DERIVATIONS.md Gaps row), k 0.868899.
"""
import os, sys, subprocess
import numpy as np
from scipy.optimize import brentq

REPO = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, REPO)
G, C0, MS = 6.6743e-11, 299792458.0, 1.989e30
RHO_CORE, RHO_MAX, A_MAX, K = 2.3e17, 1.304e15, 3.23e11, 0.868899
CAT = [("GRO J1655-40", 5.3), ("V404 Cygni", 9.0), ("Gaia BH1", 9.6), ("Cygnus X-1", 21.2), ("Gaia BH3", 33), ("GW150914", 62),
       ("GW190521", 142), ("Omega Cen", 8200), ("HLX-1", 2e4), ("Sgr A*", 4.3e6), ("Cen A", 5.5e7), ("M31", 1.4e8), ("Sombrero", 1e9),
       ("M87*", 6.5e9), ("OJ 287", 1.83e10), ("Holmberg 15A", 4e10), ("S5 0014+81", 4e10), ("TON 618", 6.6e10), ("IC 1101", 1e11),
       ("Phoenix A*", 1e11)]
V = lambda r: 4 / 3 * np.pi * r ** 3

print("=" * 100, "\n1. SINGLE BLACK HOLES  (radii from the centre, km)\n" + "=" * 100)
print("%-13s %10s | %10s %12s | %10s %11s | %12s" % ("object", "M Msun", "core(all)", "edge(reach)", "core(area)", "edge(area)", "choke 2GM/c2"))
for n, m in CAT:
    M = m * MS
    rc = (3 * M / (4 * np.pi * RHO_CORE)) ** (1 / 3); edge = np.sqrt(G * M / A_MAX)
    c = brentq(lambda x: x + K * x ** (2 / 3) - m, 1e-6, m); rc2 = (3 * c * MS / (4 * np.pi * RHO_CORE)) ** (1 / 3)
    e2 = (rc2 ** 3 + K * c ** (2 / 3) * MS / RHO_MAX / (4 / 3 * np.pi)) ** (1 / 3)
    print("%-13s %10.4g | %10.4g %12.4g | %10.4g %11.4g | %12.4g" % (n, m, rc / 1e3, edge / 1e3, rc2 / 1e3, e2 / 1e3, 2 * G * M / C0 ** 2 / 1e3))
print("core(all)/edge(reach): message-8 derivation, whole mass as core, edge where the pull falls to the yield. core(area)/edge(area): row 11 split.")
print("The two shell pictures disagree for heavy holes (open item, DERIVATIONS.md row 16).")

print("\n" + "=" * 100, "\n2. MERGERS (explored set vs GWTC-5 out of sample)\n" + "=" * 100)
import merger_energy_balance as m
dev, out = m.estimates(m.DEV), m.estimates(m.OUT)
m.report("DEV", dev); m.report("OUT (GWTC-5)", out)

print("\n" + "=" * 100, "\n3. LIGHT BENDING and SPEED LIMIT\n" + "=" * 100)
for s in ("light_bending_push_pull.py", "cavitation_speed_limit.py"):
    print(subprocess.run([sys.executable, os.path.join(REPO, s)], capture_output=True, text=True).stdout)

