# -*- coding: utf-8 -*-
"""
PWC math-check: cosmic birefringence through the Bootes Void.
Scratch arithmetic ONLY on locked repo numbers (no repo files touched).

Locked (quoted from repo):
  DERIVATIONS.md row 17:
    "rotation rate 1.4e-20 rad/s = 0.0059 H0 for beta = 0.35 deg"
    "...a dipole check on 'we rotate' (a rigid rotation gives a zero-mean dipole
     across the sky; the repo treats beta as uniform)"
  PWC/derivations/lensing_redshift_mechanics.md line 37:
    "measured cosmic polarization rotation beta = 0.35 +- 0.14 degrees ... over the
     comoving distance to last scattering 4.32e26 m: rotation rate 1.414e-29 rad/m
     = 0.025 degrees per Gpc ... In the no-stretch picture (path = c x 13.8 Gyr =
     1.31e26 m) the rate would be 4.68e-29 rad/m."
  session_logs/2026-10-02/..._lensing_redshift_ldl_hdl.md line 95:
    "0.35 deg over 13.8 Gyr -> Omega = 1.40e-20 rad/s = 0.0059 H0 (0.0254 deg per Gyr)"
  session_logs/2026-10-08/2026-10-08_survival_triad_comet.md lines 105-111:
    "cosmic birefringence should be MAXIMAL in deep space / voids (no local light or
     heat sources) and SUPPRESSED near matter ... PWC predicts birefringence to
     anti-correlate with matter density. A positive matter correlation would falsify
     the reading."
"""
import math

# ---------- locked constants ----------
c0       = 2.99792458e8       # m/s
MLY      = 9.46073047e21      # metres per Mly (1 ly = 9.46073047e15 m)
GYR      = 3.15576e16         # s per Gyr (Julian year x 1e9)
RATE_S   = 1.40e-20           # rad/s  (locked, no-stretch "we rotate" calibration)
RATE_PER_M_COMOV = 1.414e-29  # rad/m  (repo's comoving-stretch calibration)
RATE_PER_M_NOSTR = 4.68e-29   # rad/m  (repo's no-stretch calibration)
BETA_GLOBAL_LOCKED = 0.35     # deg, repo's locked measured value (2.4 sigma)
BETA_GLOBAL_MEAS   = 0.30     # deg, Diego-Palazuelos et al. 2022, PR4 (68% CL err 0.11)
SIG_BETA_GLOBAL    = 0.11     # deg, current monopole uncertainty (PR4)
T_UNIV  = 13.8e9 * 365.25 * 86400   # 13.8 Gyr in s (travel time of CMB photons)

# ---------- Bootes geometry (task inputs) ----------
CHORD_BOOTES  = 330e6 * 365.25 * 86400 * c0   # path length through the void, 330 Mly -> m
DIST_BOOTES   = 700e6 * 365.25 * 86400 * c0   # distance to the void, 700 Mly -> m
CHORD_MLY     = 330.0
DIST_MLY      = 700.0

# ---------- (2) beta through the void at the locked rate ----------
t_void = CHORD_BOOTES / c0                    # light travel time across the void
beta_void_rad  = RATE_S * t_void              # locked-rate prediction
beta_void_deg  = math.degrees(beta_void_rad)
beta_void_arc  = beta_void_deg * 3600.0

# cross-checks: same number from the no-stretch per-metre rate; and 0.0254 deg/Gyr
beta_void_perm = RATE_PER_M_NOSTR * CHORD_BOOTES
beta_void_gyr  = 0.0254 * (CHORD_MLY / 1000.0)   # 0.0254 deg/Gyr x 0.33 Gyr
# repo's comoving-stretch alternative (3.30x smaller)
beta_void_comov = RATE_PER_M_COMOV * CHORD_BOOTES

# ---------- comparisons to the global value and path average ----------
path_frac = CHORD_MLY / 13800.0           # 330 Mly / 13.8 Gly (travel-time path)
beta_pathavg_meas   = BETA_GLOBAL_MEAS   * path_frac
beta_pathavg_locked = BETA_GLOBAL_LOCKED * path_frac
ratio_meas   = beta_void_deg / BETA_GLOBAL_MEAS
ratio_locked = beta_void_deg / BETA_GLOBAL_LOCKED

# H0 consistency of the locked "0.0059 H0"
H0_from_rate = RATE_S / 0.0059               # /s
H0_kms_mpc   = H0_from_rate * 3.0856776e19   # km/s/Mpc

# ---------- (3) the sharp prediction: void/wall contrast ----------
# S1 uniform (repo's only numeric treatment): contrast = 0 by construction.
# S2 maximal rest-state reading: ALL rotation accrues in rested deep space
# (voids), walls contribute zero; normalise so the global beta is reproduced.
f_rest = 0.60   # void volume fraction along random sightlines (Pan et al. 2012 catalog class)
for name, bglob in (("beta=0.30 measured", BETA_GLOBAL_MEAS),
                    ("beta=0.35 locked  ", BETA_GLOBAL_LOCKED)):
    rate_rest = bglob / (f_rest * 13.8)      # deg per Gyr in rested medium
    beta_B_max = rate_rest * (CHORD_MLY / 1000.0)  # void chord at rested rate
    ratio_rate = rate_rest / 0.0254
    print(f"S2 [{name}]: rested rate = {rate_rest:.4e} deg/Gyr "
          f"({ratio_rate:.2f}x locked 0.0254) -> beta_Bootes_max = {beta_B_max:.5f} deg "
          f"= {beta_B_max*3600:.1f} arcsec; contrast vs zero-wall = {beta_B_max:.5f} deg")

# S3 'all deep space rested' (walls are thin): rested rate ~ locked rate,
# void chord = neighbouring chords -> contrast ~ 0 again.
# => framework contrast is UNQUANTIFIED; bounded [0, ~0.012-0.014 deg].

# angular size of the void
theta_bootes = 2.0 * math.degrees(math.atan(0.5 * CHORD_MLY / DIST_MLY))

# ---------- (4) falsifier thresholds ----------
# S2 max excess values for the 3-sigma / 4-sigma falsifier statements
excess_max_meas   = BETA_GLOBAL_MEAS   / (f_rest * 13.8) * (CHORD_MLY / 1000.0)
excess_max_locked = BETA_GLOBAL_LOCKED / (f_rest * 13.8) * (CHORD_MLY / 1000.0)
# sensitivity needed to see the S2 excess at 4 sigma, and to kill it at 3 sigma
sig_4sigma = excess_max_meas / 4.0
sig_3sigma_null = excess_max_meas / 3.0
# current monopole error and what multiple is needed
print("\n=========== PWC BIRERRINGENCE THROUGH BOOTES: NUMBERS ===========")
print(f"c0                = {c0:.6e} m/s ; 1 Mly = {MLY:.6e} m")
print(f"path through void = 330 Mly = {CHORD_BOOTES:.4e} m ; travel time = {t_void:.4e} s = 330.0 Myr")
print(f"locked rate       = 1.40e-20 rad/s = 0.0059 H0  (H0 implied = {H0_kms_mpc:.1f} km/s/Mpc)")
print(f"beta_Bootes (locked rate)  = {beta_void_rad:.4e} rad = {beta_void_deg:.5f} deg = {beta_void_arc:.2f} arcsec")
print(f"  cross-check no-stretch/m = {math.degrees(beta_void_perm):.5f} deg ; 0.0254 deg/Gyr -> {beta_void_gyr:.5f} deg")
print(f"  repo comoving-stretch alt = {math.degrees(beta_void_comov):.5f} deg  (3.30x smaller; repo lists both)")
print(f"global beta        = {BETA_GLOBAL_MEAS} deg (PR4, sigma {SIG_BETA_GLOBAL}) ; repo locked {BETA_GLOBAL_LOCKED} +/- 0.14")
print(f"path fraction      = 330/13800 = {path_frac:.4f}  ({100*path_frac:.2f}% of the travel-time path)")
print(f"path-averaged beta = {beta_pathavg_meas:.5f} deg (at 0.30) ; {beta_pathavg_locked:.5f} deg (at 0.35)")
print(f"beta_Bootes / beta_global = {ratio_meas:.4f} (1/{1/ratio_meas:.1f}) ; vs path fraction 1/{1/path_frac:.1f}")
print(f"angular diameter of Bootes = {theta_bootes:.1f} deg")
print(f"S1 (repo uniform treatment): void/wall contrast = 0 exactly")
print(f"S2 (maximal all-void reading, f_rest=0.60): excess = {excess_max_meas:.5f} deg "
      f"(at 0.30) / {excess_max_locked:.5f} deg (at 0.35) = {excess_max_meas*3600:.1f} / {excess_max_locked*3600:.1f} arcsec")
print(f"measurability: need sigma_patch = {sig_4sigma:.4f} deg for 4 sigma on the S2 excess")
print(f"  -> {SIG_BETA_GLOBAL/sig_4sigma:.0f}x better than the current PR4 monopole error ({SIG_BETA_GLOBAL} deg)")
print(f"falsifier: positive matter correlation kills the void-maximal reading;")
print(f"           |Delta_beta| >= 0.005 deg at 3 sigma kills the uniform/'we rotate' zero-contrast accounts.")
