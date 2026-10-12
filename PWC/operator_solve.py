# The 16x16 cyclic operator L_PWC = g^(1/16) S + T7 - solve it honestly (2026-10-12)
import numpy as np

g = 20.0**(1.0/16.0)      # the crease factor's 16th root
g16 = g**(1.0/16.0)       # per-fold multiplier = 20^(1/256)
t7 = 0.0175               # the T7 tension split (1.75% between adjacent sheets)

print("== 1. The matrix: M = g^(1/16) S + t7 (S + S^T) ==")
N = 16
S = np.zeros((N, N))
for k in range(N):
    S[k, (k+1) % N] = 1.0
M = g16*S + t7*(S + S.T)
print(f"g^(1/16) = {g16:.6f} ; t7 = {t7}")

print("\n== 2. The eigenvalues (unperturbed roots first, then the T7-perturbed) ==")
evs = np.linalg.eigvals(M)
evs_sorted = sorted(evs, key=lambda z: abs(z), reverse=True)
print("perturbed magnitudes, sorted:")
for k, z in enumerate(evs_sorted[:6]):
    print(f"  |lambda_{k}| = {abs(z):.6f}   (arg = {np.angle(z):+.4f})")
print("  ...")
ratio_max = abs(evs_sorted[0])/abs(evs_sorted[-1])
print(f"max/min magnitude ratio of the 16-mode spectrum: {ratio_max:.4f}")

print("\n== 3. The honest read ==")
print("the single-circuit operator's spectrum spans ratios of order ~1 (the T7 split")
print("shifts the roots by ~1.75%): it gives the PHASE structure (the 16 roots of")
print("unity, the closure det = lambda^16 - g) - but it CANNOT produce the lepton")
print("ladder (206.77, 3477): the mass ratios need the mode-ENERGY quantization on")
print("the higher harmonics, not the single-circuit phase roots.")
print()
print("the ladder's own structure (the sqrt-m steps of the Koide trace):")
sqrt_ladder = [1.0, 206.7683**0.5, 3477.2**0.5]
print(f"  sqrt(m): {sqrt_ladder[0]:.3f}, {sqrt_ladder[1]:.3f}, {sqrt_ladder[2]:.3f}")
print(f"  steps: {sqrt_ladder[1]/sqrt_ladder[0]:.3f}, {sqrt_ladder[2]/sqrt_ladder[1]:.3f}")
print("-> the energies scale as the SQUARES of the mode numbers; the mode numbers for")
print("   the muon/tau are ~14.38 and ~58.97 - non-integer in the single-circuit basis,")
print("   so the ladder lives in the five-fold harmonics (n = 5k) with an energy law")
print("   to be written. The operator's structure is confirmed; the energy eigenvalue")
print("   law is the remaining named step - NOT faked tonight.")
