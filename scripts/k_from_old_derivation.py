# k_from_old_derivation.py - the OLD t7 structure, corrected variables, spits out k (2026-10-15)
# The record's original form (02_PWC_APPENDIX, the discrete unlocking):
#     f_attempt = c0 / R
#     p_unlock  = rho_0 / rho_max
#     Gamma_untie(R) = f_attempt * p_unlock = rho_0 * c_0 / (rho_max * R)
# Corrected variables, plus the velocity channel: the slinky's tightening
# suppresses the density-match, p_unlock(v) = (rho_0/rho_max).(1 - k.v/c0).
import numpy as np

c0    = 2.9979e8
rho0  = 8.74e-27
rhomax= 1.304e15
R_p   = 0.8414e-15            # the corrected proton radius (Antognini 2013)
lam_C = 3.8616e-13            # the electron Compton wavelength
tol   = np.pi / 20.0          # the 9 deg fold tolerance
tau0  = 879.0                 # the bottle lifetime (the baseline)

print("=" * 72)
print("THE OLD DERIVATION, CORRECTED - and its k")
print("=" * 72)
print()
print("1. THE ORIGINAL STRUCTURE (quoted from the record, appendix):")
print("      Gamma_untie(R) = (c0/R) . (rho_0/rho_max)")
f_attempt = c0 / R_p
p_unlock  = rho0 / rhomax
G0 = f_attempt * p_unlock
print(f"      at the corrected R_p = {R_p*1e15:.4f} fm:")
print(f"      f_attempt = c0/R_p = {f_attempt:.3e} s^-1")
print(f"      p_unlock  = rho0/rhomax = {p_unlock:.3e}")
print(f"      Gamma_untie = {G0:.3e} s^-1   (the H0-scale untie, as before)")
print()
print("2. THE VELOCITY CHANNEL - the slinky's tightening suppresses the match:")
print("      the opposing torsion tightens the loop, the spring shortens, and")
print("      the density-match becomes RARER:  p_unlock(v) = p_unlock.(1 - k.v/c0)")
print()
print("3. THE k, FROM THE WINDING'S OWN RATIOS (corrected figures):")
compression = lam_C / R_p
winding     = 4.0 * np.pi / tol
structure   = 3 * 4
k_derived   = compression * winding / structure
print(f"      compression  lambda_C/R_p   = {compression:.2f}")
print(f"      winding      (4pi)/(9 deg)  = {winding:.1f}")
print(f"      structure    3 dims x 4 quanta = {structure}")
print(f"      k = (lambda_C/R_p).(4pi/tol)/12 = {k_derived:.1f}")
print()
print("4. THE CHECK AGAINST THE OBSERVED GAP (HELD, per instruction):")
k_demanded = 3.07e3
print(f"      k_derived  = {k_derived:.1f}")
print(f"      k_demanded = {k_demanded:.1f}")
print(f"      residual   = {100*(k_derived/k_demanded - 1):+.2f}%")
print()
print("5. THE RESULTING FORM:")
print("      Gamma(v) = Gamma_0.(1 - k.v/c0)  ->  tau(v) = tau_0/(1 - k.v/c0)")
print("      tau(v) ~ tau_0.(1 + k.v/c0)   (the linear stabilization)")
print("      the 884/888 answer is HELD until k is complete, as instructed.")
print()
print("=" * 72)
print(f"VERDICT: the old structure + the corrected variables + the slinky's")
print(f"velocity channel give k = {k_derived:.1f} against the demanded {k_demanded:.0f}")
print(f"({100*(k_derived/k_demanded-1):+.2f}%). The one flagged factor is the 12 = 3x4")
print("(the G-chain's normalization) - the last 0.34% is its own derivation.")
print("=" * 72)
