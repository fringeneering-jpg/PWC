# Eigenmode program, first pass: the standing wave's effective volume vs the WvdM uniform
# Target: g = alpha/alpha_lin = 1.2067, i.e. q^2 ~ 1/V_eff -> V_eff = V_horizon/g.
import numpy as np

hbar = 1.054571817e-34; c0 = 2.99792458e8; me = 9.1093837e-31
e = 1.602176634e-19; eps0 = 8.8541878128e-12
lamC = 2*np.pi*hbar/(me*c0)      # one Compton wavelength (full)
lamC_bar = hbar/(me*c0)
R = lamC/(4*np.pi)               # WvdM major radius
L = 2*2*np.pi*R                  # double-loop path = lamC
V_hor = np.pi*lamC**3/6.0        # the rotational horizon sphere (WvdM uniform fill)
alpha = e**2/(4*np.pi*eps0*hbar*c0)
g_target = 16*np.pi**3*alpha/3.0

print(f"V_horizon = {V_hor:.3e} m^3 ;  alpha = {alpha:.6f} ;  g_target = {g_target:.6f}")

V_eff = V_hor/g_target
print(f"\nthe eigenmode needs V_eff = V_horizon/g = {V_eff:.3e} m^3")
print("tube volume = 2 pi^2 R r_t^2  ->  r_t = sqrt(V_eff/(2 pi^2 R))")
r_t = np.sqrt(V_eff/(2*np.pi**2*R))
print(f"r_t = {r_t:.4e} m = {r_t/lamC_bar:.3f} lamC_bar = lamC/{lamC/r_t:.3f}")

print("\n== Bounding geometries ==")
# horizon fill (uniform, the WvdM limit): r_t -> r_hor = lamC/2
print(f"uniform fill (WvdM):  g = 1.0000")
# diffraction-limited waist: r_t = lamC/(2 pi) = lamC_bar
V_w = 2*np.pi**2*R*lamC_bar**2
print(f"diffraction waist r_t = lamC_bar:  g = V_horizon/V_tube = {V_hor/V_w:.2f}  (overshoots)")
# the needed scale vs framework lengths
print(f"\nneeded r_t/lamC_bar = {r_t/lamC_bar:.3f}")
print(f"compare: lamC_bar = 1.000 ; R = lamC_bar/2 = 0.500 ; r_e/lamC_bar = alpha = {alpha:.5f}")
print(f"         sqrt(3g) = lamC/r_t = {lamC/r_t:.4f}  -> r_t = lamC/sqrt(3g) = lamC/sqrt(16 pi^3 alpha)")
print(f"NOTE: sqrt(3g) = sqrt(16 pi^3 alpha) contains alpha - the effective-volume shortcut")
print(f"is CIRCULAR. The real eigenmode must fix r_t from the phase-lock structure itself,")
print(f"not from the volume shortcut. The two bounding geometries bracket the target:")
print(f"horizon fill (g=1) ... target r_t = 1.27 pm ... diffraction waist (g=13.2).")
print(f"\nthe next step: the transverse profile of the 1-quantum standing wave on the double")
print(f"loop (the phase-locked waist), integrated properly - no alpha input.")
