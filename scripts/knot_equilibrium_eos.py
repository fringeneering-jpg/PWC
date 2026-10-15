# The knot equilibrium: outward trapped heat vs the inward 720-degree pinch (2026-10-09)
# PWC's own EOS: pressure = rho*H/3 (gas branch); tension Y = s*rho*c0^2/3 (tension-heat law)
import math
c0 = 2.99792458e8; c0sq = c0**2
s = 1.0/19.0
H0 = 32.371*c0sq
cH = H0/2.7

print("== The equilibrium ==")
print("outward: trapped heat's pressure  P_out = rho_knot * H_trapped / 3")
print("inward:  the 720-degree pinch    P_in  = Y = s * rho_knot * c0^2 / 3   (tension-heat law)")
print("balance:  rho H_trapped / 3 = s rho c0^2 / 3  ->  H_trapped = s c0^2")
H_trap = s*c0sq
print(f"\nH_trapped = s * c0^2 = {H_trap:.4e} J/kg = {100*s:.2f}% of the tying heat")
print(f"-> the sealed stretch s = 1/19 IS the retained-heat fraction. The knot keeps 5.26%,")
print(f"   expels 94.74% as the radiation. 'Expelling most of the heat, but not all' - exact.")
print(f"\nresidual-heat reading on the ruled c_H: T = H_trapped/c_H = {H_trap/cH:.4f} K")
print(f"   -> the knot sits at 4.4 mK against the 2.7 K bath: the heat sink, the suction, with")
print(f"      the equilibrium's own number. (vs the earlier 0.70 K from 8.40 c0^2 - superseded.)")

print("\n== Universal across knots: the electron and the proton ==")
print("the balance is rho-independent (both sides scale with rho_knot): the SAME equilibrium")
print("holds for every knot -> H_trapped = s c0^2 for the electron AND the proton.")
print("the EOS sets the universal retained FRACTION (s); the topology sets the SCALE.")
print("electron: 1 quantum  m_e R_e c0 = hbar   -> R_e = lamC_bar")
print("proton:    4 quanta  m_p R_p c0 = 4 hbar -> R_p")
print(f"mass ratio from the quantization: m_p/m_e = 4 lamC_bar/R_p = "
      f"{4*1.054571817e-34/(9.1093837e-31*2.99792458e8)/8.414e-16:.2f}  vs 1836.15")
print("\n-> division of labor: the EOS gives the fraction (s, universal), the phase-lock gives")
print("   the size (lambda_C vs R_p), and the ratio 1836 is the ratio of the two quantizations.")
print("   The 3.302-lamC-bar tube target remains the dynamic footprint (r-independent balance).")
