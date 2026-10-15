# k_h0_bridge.py - the k<->H0 bridge and the exact contraction target (2026-10-15)
# Perplexity eliminated the common radius: k and H0 are PROPORTIONAL through
# the same transition coordinate. The 0.34% gap is now mapped to an exact
# spatial target the slinky's torsion must derive: Delta R = -0.002833 fm.
import numpy as np

c0    = 2.9979e8
rho0  = 8.74e-27
rhomax= 1.304e15
lam_C = 3.8616e-13
R0    = 0.8414e-15            # fm-scale, the proton radius (the transition R)
theta = np.pi / 20.0

print("=" * 72)
print("THE k <-> H0 BRIDGE - one radius, two scales")
print("=" * 72)
print()
print("1. THE PROPORTIONALITY (eliminating the common R):")
print("      H0 = (c0/R) . (rho0/rhomax)")
print("      k  = (lambda_C/R) . (4pi/theta)/12 ,  theta = pi/20")
print("      ->  4pi/theta = 80 ,  k = 20 lambda_C / (3 R)")
print()
H0  = (c0 / R0) * (rho0 / rhomax)
k12 = 20.0 * lam_C / (3.0 * R0)
bridge = 20.0 * lam_C * rhomax / (3.0 * c0 * rho0)
print(f"      H0(R) = {H0:.6e} s^-1")
print(f"      k(R)  = {k12:.4f}")
print(f"      k = (20 lambda_C rho_max /(3 c0 rho0)) . H0   [factor {bridge:.3e}]")
print("      the neutron's endurance coefficient and the cosmic untie rate")
print("      are SIBLINGS - tied by one transition radius.")
print()
print("2. THE 3D PYTHAGOREAN CLOSURE (the 18:1:19 partition in 3D):")
print("      The 18 parts run the 2D circumference; the 1 is the perpendicular")
print("      axial stack height (L^2), invisible in a flat 2D projection.")
alpha_sq = 19.0 / 18.0
hyp_3d   = np.sqrt(1.0 + alpha_sq / (16.0 * np.pi**2))
R_3d     = R0 / hyp_3d
dR_3d    = R_3d - R0
N_3d     = 12.0 / hyp_3d
k_3d     = k12 * hyp_3d
H0_3d    = (c0 / R_3d) * (rho0 / rhomax)
print(f"      alpha^2 = 19/18          ->  hypotenuse = {hyp_3d:.7f}")
print(f"      12 -> 12 / hyp_3d        =  {N_3d:.5f}   (target 11.9600: {1e6*(N_3d/11.96-1):+.0f} ppm)")
print(f"      R_3D = R0 / hyp_3d       =  {R_3d*1e15:.7f} fm  (dR = {dR_3d*1e15:.6f} fm)")
print(f"      k_3D (forward derived)   =  {k_3d:.2f}      (vs 3070.0: {100*(k_3d-3070.0)/3070.0:+.4f}%)")
print(f"      H0_3D in lockstep        =  {H0_3d*3.0857e19:.3f} km/s/Mpc")
print()
print("3. THE SLINKY'S JOB - derive dR from the chiral torsion:")
print("      tau_phi = F . R^2 phi / L   (the virtual-work coupling)")
print("      the torsion's force F is the cage's OWN stress - the opposing")
print("      pairs clamping the centre - NOT Newtonian gravity (which is")
print("      1e-37 of the EM force at this scale and cannot supply 0.34%).")
print("      The displacement dR = -0.002833 fm is the spring's exact target:")
print("      the torsion must SHORTEN the effective radius by that fraction,")
print("      derived from the cage's stresses, not selected to close the gap.")
print()
print("=" * 72)
print("VERDICT: the bridge is the win - k and H0 move in lockstep through one")
print("radius, so the subatomic endurance and the cosmic expansion are the same")
print("coordinate's two readings. The 0.34% is now a DERIVATION TARGET with an")
print("exact size (dR = -0.002833 fm) and an exact driver named (the chiral")
print("torsion). The last step: the torsion's force scale from the fold's")
print("balance - then the final decimal locks without being selected.")
print("=" * 72)


