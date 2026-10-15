# helix_coupling_k.py - the k from the crushing geometry (Perplexity's helix step, applied) (2026-10-15)
# The helix unrolled:  l^2 = L^2 + R^2 phi^2
# More winding shortens the axis:  dL/dphi = -R^2 phi / L
# The crushing load drives the tightening:  tau_phi = F . dx/dphi = F . R^2 phi / L
# The contraction under the medium's shear gives the velocity slope k.
import numpy as np

c0   = 3.0e8
r_e  = 2.8179e-15            # the electron radius (the loop's scale)
phi  = 4.0 * np.pi           # the 720 deg winding
R_loop = r_e / (5.0 * np.pi**2)   # the locked loop radius
lam_C = 3.8616e-13
R_p   = 0.8414e-15

print("=" * 72)
print("THE k FROM THE CRUSHING GEOMETRY - the helix coupling")
print("=" * 72)
print()
print("1. THE HELIX (the geometry, not a fitted coefficient):")
print("      l^2 = L^2 + R^2 phi^2        (the winding unrolled)")
print("      dL/dphi = -R^2 phi / L        (more winding -> shorter axis)")
print("      tau_phi = F . dx/dphi = F . R^2 phi / L   (the crushing load's")
print("      torque, by virtual work - the sign follows the winding's own)")
print()
print("2. THE CRUSHING LOAD - the medium's shear on the exposed knot:")
print("      the surface tax: the flow presses the thread into its channel,")
print("      F(v) ~ the medium's dynamic pressure on the knot's cross-section,")
print("      linear in v at low speeds (the drag regime).")
print()
print("3. THE CHAIN TO k (the honest structure):")
print("      the torque's balanced by the lock's torsional stiffness kappa_phi:")
print("      tau_phi = kappa_phi . dphi   ->   dphi = F . R^2 phi / (L . kappa_phi)")
print("      the contraction:  dL/L = -(R^2 phi / L^2) . dphi")
print("      ->  dL/L = - F . R^4 phi^2 / (L^3 . kappa_phi)")
print("      ->  k = -(dL/L)/(v/c0) = F . R^4 phi^2 . c0 / (L^3 . kappa_phi . v)")
print()
print("4. WHAT THE LOCKED SET FIXES, AND WHAT IT LEAVES:")
print(f"      phi = 4pi,  R_loop = r_e/(5pi^2) = {R_loop:.2e} m  (locked)")
print("      the remaining scales: L (the axial length), kappa_phi (the")
print("      lock's torsional stiffness), and F/v (the drag's force per unit")
print("      speed) - the three quantities the medium's mechanics must supply.")
print()
print("5. THE HONEST CHECK - does the structure carry the right shape?")
print("      the contraction's form:  dL/L = -(F . R^4 phi^2 /(L^3 kappa_phi))")
print("      is LINEAR in F and hence in v - the linear stabilization falls")
print("      out of the helix itself, with the slope k set by the geometric")
print("      ratios and the two stiffnesses. The form is derived; the numbers")
print("      of L, kappa_phi and F/v are the remaining inputs.")
print()
print("=" * 72)
print("VERDICT: Perplexity's helix step is now the k's geometric basis - the")
print("crushing-to-torque coupling is DERIVED (no fitted twist-shortening),")
print("and the contraction's linear-in-v form is the helix's own. What the")
print("next step needs: the lock's torsional stiffness kappa_phi and the")
print("axial scale L from the cage's geometry - then k prints from the")
print("structure with nothing turned.")
print("=" * 72)
