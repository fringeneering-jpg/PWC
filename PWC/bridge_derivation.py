# The bridge: the two-regime ratio derived - 9/(4s) from the stretch and the quantization
import math
G = 6.67430e-11; c0 = 2.99792458e8; hbar = 1.054571817e-34
rho0 = 8.74e-27; mp = 1.67262192369e-27; Rp = 8.414e-16
s = 1.0/19.0

alpha_G = G*mp**2/(hbar*c0)
m_w = mp/3.0
V_pair = m_w/rho0
Y_cav = s*rho0*c0**2/3.0
U_G = G*mp**2/Rp
self_c = U_G/(Y_cav*V_pair)

print("== the bridge, measured from the run ==")
bridge_num = self_c/alpha_G
print(f"self-coupling / alpha_G = {self_c:.4e} / {alpha_G:.4e} = {bridge_num:.4f}")

print("\n== the bridge, DERIVED (G cancels exactly) ==")
print("self-coupling / alpha_G = [G mp^2/Rp / (Y V)] / [G mp^2/(hbar c0)] = hbar c0/(Rp Y V)")
bridge = hbar*c0/(Rp*Y_cav*V_pair)
print(f"  = hbar c0 / (Rp * Y_cav * V_pair) = {bridge:.4f}   - NO G anywhere")
print("\nsubstitute the locked identities:")
print("  Y_cav = s rho0 c0^2/3 ;  V_pair = m_w/rho0 = m_p/(3 rho0)")
print("  -> bridge = hbar c0 / (Rp * s rho0 c0^2/3 * m_p/(3 rho0)) = 9 hbar/(s c0 m_p Rp)")
print("  the quantization: m_p Rp c0 = 4 hbar  ->  m_p Rp = 4 hbar/c0")
print(f"  -> bridge = 9 hbar/(s c0 * 4 hbar/c0) = 9/(4s) = {9/(4*s):.4f}")
print(f"\nthe measured bridge {bridge_num:.4f} vs the derived 9/(4s) = {9/(4*s):.4f}  "
      f"({100*(bridge_num/(9/(4*s))-1):+.4f}%)")

print("\n== the full chain now ==")
print(f"alpha_G = (the tension self-coupling) / (9/(4s))")
print(f"        = {self_c:.4e} / {9/(4*s):.4f} = {self_c/(9/(4*s)):.4e}   (target {alpha_G:.4e})")
print("\nthe bridge is DERIVED - exact, G-free, from the stretch s = 1/19 and the")
print("quantization m_p R_p c0 = 4 hbar. The one remaining piece: the tension's own")
print(f"self-coupling {self_c:.4e} = U_G/(Y V) - the wave's gravitational self-interaction")
print("composed from its own structure. With the bridge closed, alpha_G = self-coupling x 4s/9,")
print("and the derivation reduces to that single wave-structure ratio.")
