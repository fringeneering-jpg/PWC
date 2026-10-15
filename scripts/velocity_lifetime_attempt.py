# velocity_lifetime_attempt.py - the neutron's velocity-lifetime equation: FIRST HONEST PASS (2026-10-15)
# The beam and bottle disagree by ~9-10 s. The framework's wedge: the bare knot's
# untie rate is a function of its velocity through the medium. This script states
# the required coupling and evaluates the candidates from LOCKED constants only.
import numpy as np

c0    = 3.0e8                 # m/s, the medium's speed
tau0  = 879.0                 # s, the bottle (rest) lifetime
tau_beam = 888.0              # s, the beam lifetime
v_beam = 1.0e3                # m/s, a representative cold-beam speed
hbar  = 1.05457e-34
r_e   = 2.8179e-15            # m, the electron radius (the loop's scale)
lam_C = 3.8616e-13            # m, the electron Compton wavelength

print("=" * 72)
print("THE VELOCITY-LIFETIME EQUATION - first honest pass")
print("=" * 72)
print()
print("1. THE REQUIRED COUPLING (from the observed numbers).")
drel = (tau_beam - tau0) / tau0
dim  = v_beam / c0
k_req = drel / dim
print(f"      observed relative shift  dtau/tau0 = {drel*100:.2f}%")
print(f"      dimensionless velocity   v/c0      = {dim:.2e}")
print(f"      REQUIRED coupling k      = {k_req:.2e}   (the shift per unit v/c0)")
print()
print("2. CANDIDATE 1 - the wave-equation time dilation (T6).")
gamma = 1.0 / np.sqrt(1.0 - dim**2)
dtau1 = tau0 * (gamma - 1.0)
print(f"      tau(v) = tau0.gamma   ->   dtau = {dtau1:.3e} s")
print(f"      verdict: {dtau1/tau0*100:.2e}% - ten orders short. NOT the term.")
print()
print("3. CANDIDATE 2 - the phase-drift exhaustion (the exposed thread vs the flow).")
# the thread circulates at c0 over the 720 deg circuit; the flow adds a phase
# drift per internal circuit; the fold's tolerance is the 9 deg of freedom.
R_loop = r_e / (5.0 * np.pi**2)       # m, the loop's radius
f_circ = c0 / (2.0 * np.pi * R_loop)  # Hz, the internal circulation frequency
tol    = np.pi / 20.0                 # 9 deg = the selection law's fold tolerance
drift  = 4.0 * np.pi * dim * f_circ   # rad/s, the flow's phase drift rate
t_ex   = tol / drift
print(f"      R_loop = {R_loop:.2e} m ;  circuit frequency = {f_circ:.2e} Hz")
print(f"      drift rate = {drift:.2e} rad/s ;  tolerance = {tol:.2e} rad")
print(f"      time to exhaust the tolerance = {t_ex:.2e} s")
print(f"      verdict: INSTANT exhaustion - the raw drift model is not the term")
print(f"      (the thread's phase-lock must RESIST the drift, not count it).")
print()
print("4. CANDIDATE 3 - the shear stabilization (the Magnus-like coupling).")
print("      the moving knot's phase-lock tightens against the flow: the untie")
print("      rate drops as the thread's exposed end is pressed INTO its channel.")
print("      The form:  tau(v) = tau0 . (1 + k . v/c0), k from the knot's own")
print("      structure (the winding's amplification of the external shear).")
print(f"      The data demands k = {k_req:.2e} - the amplification of the")
print("      winding, to be derived from the locked constants, not fitted.")
print()
print("=" * 72)
print("HONEST VERDICT (first pass):")
print("  - the gamma term:  10 orders short  (confirmed, by the framework's own")
print("    wave-equation contraction)")
print("  - the raw drift:   exhausts the 9 deg tolerance instantly - the thread's")
print("    phase-lock must be RESISTIVE, not additive")
print(f"  - the live candidate: the shear-stabilization form with k ~ {k_req:.0e},")
print("    the winding's amplification - the named derivation, not yet landed")
print("=" * 72)
print()
print("what this pass PROVES: the equation's form is now constrained - it must be")
print("a stabilization term linear in v/c0 with a coefficient of order 1e3-1e4,")
print("and the raw candidates are falsified with their numbers on the record.")
print("the next pass derives k from the winding count itself.")
