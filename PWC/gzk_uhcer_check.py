# -*- coding: utf-8 -*-
"""
PWC math check: GZK cutoff / Oh-My-God particle vs the 2.725 K bath.
Agent check, 2026-11. Scratch only — does not touch the repo.

Locked numbers (task brief):
  c0 = 2.998e8 m/s
  m_p = 1.6726e-27 kg
  bath photon energy E_gamma = k_B*2.725 K = 3.76e-4 eV  (LOCKED as given)
  OMG particle: E = 3.2e20 eV, gamma ~ 3.2e11, v = (1 - 5e-24) c0

Questions:
 (1) E_GZK = (m_Delta^2 - m_p^2)/(4 E_gamma), m_Delta = 1232 MeV, vs standard ~5e19 eV.
 (2) Does the PWC bath (same 2.725 K photon) give the same threshold?
 (3) OMG vs threshold; does the PWC sieve reading change the mean free path?
 (4) Does PWC add anything beyond standard GZK?
"""

# ---------------- constants ----------------
C0       = 2.998e8            # m/s (locked)
M_P_KG   = 1.6726e-27         # kg  (locked)
M_P      = 938.272            # MeV (PDG proton mass; task's kg value is the same)
M_DELTA  = 1232.0             # MeV, Delta+(1232)
M_PI0    = 134.9768           # MeV, pi0 (the actual GZK threshold partner)
M_PI_C   = 139.5704           # MeV, pi+ (n pi+ channel)
E_GAMMA  = 3.76e-4            # eV, locked bath photon energy (task calls it k_B*2.725 K)
T_CMB    = 2.725              # K
KB       = 8.617333e-5        # eV/K
E_KT     = KB * T_CMB         # = true k_B*2.725 K
E_MEAN   = 2.701 * E_KT       # mean blackbody photon energy <E> = 2.701 kT
OMG_E    = 3.2e20             # eV, Oh-My-God particle
STD_GZK  = 5.0e19             # eV, the standard "GZK cutoff energy" quoted

print("=" * 78)
print("0) SANITY: the locked photon energy vs k_B * 2.725 K")
print(f"   k_B = {KB:.6e} eV/K ;  k_B*2.725 K = {E_KT:.4e} eV")
print(f"   locked E_gamma        = {E_GAMMA:.4e} eV")
print(f"   ratio locked/k_B*T    = {E_GAMMA/E_KT:.4f}   (locked value is 1.6x kT)")
print(f"   -> locked 3.76e-4 eV equals the MODAL photon energy (~1.59 kT), not kT.")
print(f"      mean blackbody photon energy <E> = 2.701 kT = {E_MEAN:.4e} eV")
print()

print("=" * 78)
print("1) E_GZK from the locked formula  (m_D^2 - m_p^2)/(4 E_gamma), head-on")
print("=" * 78)

def e_threshold(mX_mev, eg_ev):
    """head-on threshold energy (eV) for p + gamma -> X: (mX^2 - mp^2)/(4 E_gamma)."""
    mX2 = mX_mev**2
    mp2 = M_P**2
    num_mev2 = mX2 - mp2
    num_ev2 = num_mev2 * 1e12          # 1 MeV^2 = 1e12 eV^2
    return num_ev2 / (4.0 * eg_ev), num_mev2

E_delta_locked, num_delta = e_threshold(M_DELTA, E_GAMMA)
E_delta_mean,   _          = e_threshold(M_DELTA, E_MEAN)
E_delta_kt,     _          = e_threshold(M_DELTA, E_KT)
E_pi0_locked,   num_pi0    = e_threshold(M_P + M_PI0, E_GAMMA)
E_pi0_mean,     _          = e_threshold(M_P + M_PI0, E_MEAN)

print(f"   m_Delta = {M_DELTA} MeV ; m_p = {M_P} MeV ; m_p + m_pi0 = {M_P+M_PI0:.2f} MeV")
print(f"   numerator m_D^2 - m_p^2 = {num_delta:.1f} MeV^2 = {num_delta*1e12:.4e} eV^2")
print(f"   E_GZK(Delta, E_gamma locked)  = {E_delta_locked:.4e} eV  = {E_delta_locked/1e19:.2f} x 1e19 eV")
print(f"   E_GZK(Delta, <E>=2.701 kT)    = {E_delta_mean:.4e} eV   = {E_delta_mean/1e19:.2f} x 1e19 eV")
print(f"   E_GZK(Delta, kT only)         = {E_delta_kt:.4e} eV     = {E_delta_kt/1e19:.2f} x 1e19 eV")
print(f"   vs standard quoted            = {STD_GZK:.1e} eV")
print(f"   ratio locked/std  = {E_delta_locked/STD_GZK:.2f}x")
print()
print("   BUT the Delta is a RESONANCE, not the threshold. Photopion production")
print(f"   p + gamma -> p + pi0 (or n + pi+) opens at s = (m_p + m_pi)^2 = "
      f"{(M_P+M_PI0)**2:.1f} MeV^2 < m_D^2 = {M_DELTA**2:.1f} MeV^2.")
print(f"   TRUE threshold, locked E_gamma:  E_th(pion) = {E_pi0_locked:.4e} eV")
print(f"   TRUE threshold, mean <E>:        E_th(pion) = {E_pi0_mean:.4e} eV")
print()

print("=" * 78)
print("2) Does the PWC bath reproduce the SAME threshold?")
print("=" * 78)
# CMB energy density from PWC's own bookkeeping = a T^4
import math
A_RAD = 7.5657e-16   # J m^-3 K^-4
u_cmb = A_RAD * T_CMB**4
print(f"   a*T^4 (T=2.725 K) = {u_cmb:.4e} J/m^3  (PWC bookkeeping: 4.175e-14 J/m^3 -> match)")
# photon number density
HBAR_C = 1.97327e-7   # eV m
N_GAM = 2.0 * 1.2020569 / math.pi**2 * (E_KT / HBAR_C)**3
print(f"   n_gamma = 2 zeta(3)/pi^2 (kT/hbar c)^3 = {N_GAM/1e6:.2f} x 1e6 m^-3 = {N_GAM*1e-6:.1f} cm^-3")
print()
print("   The PWC bath IS the standard 2.725 K blackbody (same photon energies, same")
print("   spectrum, same number density). The threshold is a statement about the")
print("   invariant s = (p_p + p_gamma)^2 >= m_X^2, so with the same E_gamma the")
print("   threshold is IDENTICAL by construction: yes, same number, trivially.")
print()

print("=" * 78)
print("3) Oh-My-God particle vs threshold; sieve reading and the mean free path")
print("=" * 78)
gamma_omg = OMG_E / (M_P * 1e6)   # MeV -> eV
# 1 - beta via series, not via 1 - sqrt(1 - 1/g^2), to avoid double-precision
# cancellation (1 - 1/g^2 rounds to 1.0 in float64)
one_minus_beta = 1.0 / (2.0 * gamma_omg**2)
print(f"   E = {OMG_E:.2e} eV -> gamma = E/m_p c^2 = {gamma_omg:.4e}   (locked: ~3.2e11)")
print(f"   1 - v/c = 1/(2 gamma^2) = {one_minus_beta:.3e}   (locked: 5e-24 -> consistent, ~17% off")
print(f"   because gamma=3.2e11 exactly corresponds to E = 3.00e20 eV; either way same order)")
print()
print(f"   Is it above threshold?  E = 3.2e20 eV")
print(f"     vs true pion threshold (locked E_gamma)  {E_pi0_locked/1e19:.1f} x 1e19  -> ABOVE by {OMG_E/E_pi0_locked:.2f}x")
print(f"     vs true pion threshold (mean <E>)        {E_pi0_mean/1e19:.1f} x 1e19  -> ABOVE by {OMG_E/E_pi0_mean:.2f}x")
print(f"     vs standard effective GZK energy         {STD_GZK/1e19:.1f} x 1e19  -> ABOVE by {OMG_E/STD_GZK:.1f}x")
print(f"     vs locked Delta-formula number           {E_delta_locked/1e19:.1f} x 1e19  -> (below only because the")
print(f"     Delta-formula overstates the threshold; Delta is a resonance above m_p + m_pi)")
print()
# mean free path at the Delta peak (both frameworks share n_gamma and sigma)
SIGMA_DELTA = 5.0e-28   # cm^2 ~ 0.5 mb at the Delta peak
n_gamma_cm3 = N_GAM * 1e-6
lam_cm = 1.0 / (n_gamma_cm3 * SIGMA_DELTA)
MPC_CM = 3.0857e24     # cm per Mpc
lam_mpc = lam_cm / MPC_CM
print(f"   Mean free path at the Delta peak: 1/(n sigma) with n = {n_gamma_cm3:.1f} cm^-3,")
print(f"   sigma = {SIGMA_DELTA:.1e} cm^2:  lambda = {lam_cm:.3e} cm = {lam_mpc:.2f} Mpc")
print(f"   (standard attenuation length at 3e20 eV ~ 10 Mpc; either way << cosmological)")
print()
print("   Sieve reading: a lone knot threads the medium 'at any speed up to c0'.")
print("   Threading describes PROPAGATION, not the p+gamma coupling. The bath photons")
print("   still exist at 411 cm^-3 with the same energies; the knot still scatters on")
print("   them with the same sigma. No new channel is removed or added, so the mean")
print("   free path is UNCHANGED: PWC predicts the SAME propagation length, not longer.")
print("   (A LONGER length would require the knot to decouple from the bath photons,")
print("   i.e. abandoning the EM interaction - which PWC keeps.)")
print()

print("=" * 78)
print("4) Cross-check of the locked 'escape fraction 5.3e-5'")
print("=" * 78)
H0 = 67.4e3 / 3.0857e22          # 67.4 km/s/Mpc in s^-1
G  = 6.6743e-11
rho_crit_c2 = 3.0 * H0**2 * C0**2 / (8.0 * math.pi * G)   # J/m^3
OMEGA_GAM = u_cmb / rho_crit_c2
print(f"   rho_crit c^2 = 3 H0^2 c0^2/(8 pi G) = {rho_crit_c2:.3e} J/m^3")
print(f"   Omega_gamma = u_CMB / rho_crit c^2 = {OMEGA_GAM:.4e}")
print(f"   -> PWC's 'cosmic escape fraction 5.3e-5' = the standard Omega_gamma = {OMEGA_GAM:.2e}.")
print("      The bath bookkeeping is standard cosmology relabelled as tying exhaust.")
print()

print("=" * 78)
print("VERDICT NUMBERS")
print("=" * 78)
print(f"   E_GZK(Delta, locked)   = {E_delta_locked:.2e} eV   (task formula, 8.5x the quoted 5e19)")
print(f"   E_th(pion, locked)     = {E_pi0_locked:.2e} eV   (the real threshold, correct channel)")
print(f"   E_th(pion, mean <E>)   = {E_pi0_mean:.2e} eV")
print(f"   standard effective     = {STD_GZK:.1e} eV   (full-spectrum convolution incl. Wien tail)")
print(f"   OMG energy             = {OMG_E:.2e} eV, above threshold by {OMG_E/E_pi0_mean:.1f}x")
print(f"   bath = standard CMB    : n_gamma = {n_gamma_cm3:.0f} cm^-3, u = {u_cmb:.3e} J/m^3")
print(f"   MFP at Delta peak      = {lam_mpc:.2f} Mpc   (identical in both frameworks)")
print(f"   PWC escape fraction    = {OMEGA_GAM:.2e} = Omega_gamma (relabel)")
