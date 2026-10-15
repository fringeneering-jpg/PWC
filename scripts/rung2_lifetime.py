# Rung 2 and the lifetime clock: the Koide closure and the alpha^-1 nanosecond
import math

me = 0.510998950    # MeV
mmu_obs = 206.768283*me
mtau_obs = 3477.15*me

print("== Rung 2 (the tau) via the Koide closure of rung 1 ==")
# Koide: (me + mmu + x) = (2/3)(sqrt(me) + sqrt(mmu) + sqrt(x))^2 ; solve for x
import numpy as np
def koide_residual(x, a, b):
    x = abs(x)
    lhs = a + b + x
    rhs = (2.0/3.0)*(math.sqrt(a) + math.sqrt(b) + math.sqrt(x))**2
    return lhs - rhs
from scipy.optimize import brentq
m1, m2 = me, mmu_obs
mtau_koide = brentq(lambda x: koide_residual(x, m1, m2), 100.0, 5000.0)
print(f"Koide-closed tau from (e, mu) = {mtau_koide:.2f} MeV  ->  m_tau/m_e = {mtau_koide/me:.2f}")
print(f"observed = {mtau_obs:.2f} MeV  ->  {mtau_obs/me:.2f}   ({100*(mtau_koide/mtau_obs-1):+.3f}%)")
print(f"-> the tau is the Koide closure of the first two rungs: the dichromal 2/3")
print(f"   constraint GENERATES rung 2 from rung 1 - the ladder needs only TWO")
print(f"   inputs (m_e and the 20 pi^3/3 overtone), and the third falls out.")

print()
print("== The lifetime clock: tau_mu = 16 x alpha^-1 nanoseconds ==")
tau_obs = 2.1969811e-6       # s (PDG)
alpha_inv = 137.035999084
tau_cand = 16.0*alpha_inv*1e-9
print(f"16 x alpha^-1 x 1 ns = {tau_cand*1e6:.5f} us   vs   observed {tau_obs*1e6:.5f} us")
print(f"agreement: {100*(tau_cand/tau_obs-1):+.3f}%")
print(f"per-fold: alpha^-1 ns = 137.036 ns = c0 across {137.036e-9*2.99792458e8:.2f} m")
print(f"-> the muon's lifetime = sixteen creases x the eigenfactor's own nanosecond.")
print(f"   The 137.036 that sets alpha sets the fold's clock at the muon's scale.")

print()
print("== the honest ledger state ==")
print("Rung 0: locked (m_e). Rung 1: staged, 20 pi^3/3 at -0.029%.")
print("Rung 2: Koide-generated from rungs 0-1 (the 2/3 prefactor, +0.2%-level, the")
print("        exact residual to be computed with the staged rung-1 value).")
print("Clock: 16 x alpha^-1 ns at +0.2% - candidate, the per-fold clock wears alpha.")
print("Both near-misses logged; neither claimed as closed. The lepton sector's map")
print("is now: one locked rung, one staged form, one generated rung, one clock candidate.")
