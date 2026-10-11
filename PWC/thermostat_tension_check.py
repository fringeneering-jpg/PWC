"""
PWC "thermostat" reading of the Hubble tension - math check.
Math-check agent, 2026-10 (session delegate).

Reads ONLY the repo (PWC/...) and computes in scratch/. Repo untouched.
All framework numbers are quoted from the files listed; arithmetic on
stated numbers is labelled ARITHMETIC.

Repo sources used (quoted in the report):
  PWC/PWC/knot_audit/t7_discrete_unlocking.md  (T7, H0_wall, sec 9)
  PWC/PWC/PWC.md line 138                      (BAO 147 Mpc reading)
  PWC/PWC/derivations/demand_function_pressure_conversion.md sec 8
  PWC/PWC/session_logs/2026-10-08/2026-10-08_FULL_LEDGER.md sec 13
  PWC/PWC/session_logs/2026-10-09/2026-10-09_0703_cH_ruling_2.7K.md
  PWC/PWC/OPEN_WORK.md line 103 (BAO NEEDS DERIVATION), line 124 (95%)
  PWC/DERIVATIONS.md line 63 (heat-capacity datum)
  PWC/README.md (locked numbers table)
  PWC/paper/PWC_v1_draft.md line 161, 218 (H0_wall 73.8, ratio 1.010)
"""

# ---------------- constants ----------------
C0     = 2.99792458e8          # m/s
C0SQ   = C0 * C0               # J/kg  (specific latent heat)
G      = 6.67430e-11           # m3/(kg s2)
MPC_KM = 3.0857e19             # km per Mpc (repo uses 3.086e19)
A_RAD  = 7.565733e-16          # J/(m3 K4) radiation constant
T_CMB  = 2.7255                # K  (FIRAS/Planck monopole)

# framework locked inputs
RHO0   = 8.74e-27              # kg/m3
RHOMAX = 1.304e15              # kg/m3
RP     = 0.84e-15              # m  proton radius used by T7 for 73.8
RP_HI  = 0.88e-15              # m  upper end of measured span (t7 cites 0.84-0.88 fm)
S      = 1.0 / 19.0            # the stretch / retained-heat fraction (5.26%)
H0_HEAT= 32.371                # H0 = 32.371 c0^2 (J/kg) heat floor (NOT a rate)

# observations
SH0ES  = 73.04                 # km/s/Mpc, Riess+ 2022 (repo's number)
PLANCK = 67.4                  # km/s/Mpc, CMB-inferred (repo's number)
RD_DESI= 147.09                # Mpc, comoving sound horizon at drag (DESI DR1/Planck18)

print("=" * 78)
print("PWC thermostat / Hubble-tension math check")
print("=" * 78)

# ---------------- (1) the two H0 anchors ----------------
print("\n(1) THE FRAMEWORK'S TWO H0 ANCHORS")
print("-" * 78)

# H0_wall from T7: Gamma_untie(R_p) = rho0*c0/(rhomax*R_p)
Gamma = RHO0 * C0 / (RHOMAX * RP)
H0_wall = Gamma * MPC_KM
print(f"Gamma_untie(R_p) = rho0*c0/(rho_max*R_p)")
print(f"  = {RHO0:.3e}*{C0:.5e}/({RHOMAX:.4e}*{RP:.2e}) = {Gamma:.4e} s^-1")
print(f"H0_wall = Gamma * 3.0857e19 = {H0_wall:.2f} km/s/Mpc   (repo: 73.8; uses 3.086e19 conv -> {Gamma*3.086e19:.2f})")
print(f"SH0ES match: {H0_wall:.1f}/{SH0ES:.2f} = {H0_wall/SH0ES:.4f}  (paper v1.9 line 190: ratio 1.010)")

# spread from the measured proton-radius span (t7 line 363-364: R_p spans 0.84-0.88 fm)
H0_wall_hi = RHO0 * C0 / (RHOMAX * RP_HI) * MPC_KM
print(f"R_p span check (t7 cites 0.84-0.88 fm): H0_wall = {H0_wall:.1f} (0.84 fm) to {H0_wall_hi:.1f} (0.88 fm) km/s/Mpc")
print("  -> the headline 73.8 uses the LOW end of the measured proton-radius span")

# Planck-side claim: quote + arithmetic of the claimed volume average
print()
print("Planck-side account (t7 sec 9, quoted):")
print('  "The CMB inference integrates over full observable volume including the')
print('   dominant void space at rho_0 with no knots. Void interiors contribute')
print('   essentially zero to volume creation... Volume-weighted average of')
print('   ~73.8 km/s/Mpc in matter-dense regions and ~0 km/s/Mpc in voids')
print('   produces the observed CMB H_0 = 67.4 km/s/Mpc."')
f_wall = PLANCK / H0_wall
f_wall2 = PLANCK / SH0ES
print(f"ARITHMETIC on that claim: 67.4 = f_wall*73.8 + (1-f_wall)*0")
print(f"  => required wall volume fraction f_wall = {PLANCK}/{H0_wall:.1f} = {f_wall:.4f}  ({f_wall*100:.1f}% of ALL volume)")
print(f"  (using 73.04 instead: f_wall = {f_wall2:.4f})")
print("  -> the framework never computes f_wall; t7 line 207 marks")
print('     "Quantitative void-vs-wall H_0 prediction" as [open derivation].')

print()
print("BAO 147 Mpc in PWC terms (PWC.md line 138, quoted):")
print('  "The thickest rings sit at a preferred spacing - the BAO scale, ~147 Mpc -')
print('   read in PWC as the shells where a sound wave in the medium, launched at')
print('   the formation event (the Great Separation), froze in place."')
print("OPEN_WORK.md line 103: derive 147 Mpc from the medium's sound speed and the")
print("formation-era travel time - NEEDS DERIVATION (the number is adopted from")
print("measurement, not derived).")

# ---------------- (2) the thermostat bookkeeping ----------------
print()
print("(2) THERMOSTAT BOOKKEEPING (Great Separation / 2.7 K bath)")
print("-" * 78)

H0_J   = H0_HEAT * C0SQ            # J/kg
cH     = H0_J / 2.7                # J/(kg K)
cH_c0  = H0_HEAT / 2.7             # in c0^2 per K
print(f"H0 (heat floor, J/kg) = 32.371 c0^2 = {H0_J:.4e} J/kg   (NOT a Hubble rate)")
print(f"c_H datum = H0/2.7 K = {cH:.4e} J/(kg K) = {cH_c0:.4f} c0^2 per K  (repo: 11.989)")
T_knot = S / cH_c0
print(f"knot retained heat s*c0^2 reads {T_knot*1000:.2f} mK on the c_H ladder (repo: 4.4 mK heat sink)")
today5 = 0.0526 * H0_HEAT
print(f"today's 5% matter exhaust: 0.0526*32.371 = {today5:.3f} c0^2 per kg medium = {today5/H0_HEAT*100:.2f}% of the floor")
print("  (95% melted since the Great Separation; the spacer heat is ancient exhaust)")

u_cmb = A_RAD * T_CMB**4
esc_med  = u_cmb / RHO0 / C0SQ      # c0^2 per kg of medium
rho_mat  = S * RHO0                 # today's tied matter as 1/19 of mass
esc_mat  = u_cmb / rho_mat / C0SQ   # c0^2 per kg of matter
print(f"u_bath = a*T^4 = {u_cmb:.4e} J/m^3 (repo: 4.175e-14)")
print(f"escape fraction per kg MEDIUM   = {esc_med:.4e} c0^2/kg  (repo: 5.3e-5, freeze inventory)")
print(f"escape fraction per kg MATTER   = {esc_mat:.4e} c0^2/kg  (repo: 1.01e-3, today's 5%)")
print(f"ratio = {esc_mat/esc_med:.2f} = 1/s (s = 1/19 = {S:.5f})  -> internally consistent")

# the 54 K "formation-time ambient" (given in the task; NOT found in repo)
T54  = 2.7 / 0.05
T54s = 2.7 / S
print()
print("'54 K formation ambient' = 2.7/0.05 =", f"{T54:.0f} K  (task's framing; NOT in the repo -")
print(f"  2.7/0.0526 = {T54s:.1f} K with the repo's own s = 1/19.  grep found no 54 K figure anywhere.)")
T_rec = T_CMB * (1 + 1100)
z54 = T54 / T_CMB - 1
print(f"Cross-check: the framework's own CMB epoch is z ~ 1100 (CLOSURE_SHEET); the standard")
print(f"bath there is 2.7255*(1+1100) = {T_rec:.0f} K, while 54 K is the standard bath at z = {z54:.0f}.")
print("  -> 54 K mixes the tied fraction (5%) with a redshift; the repo has no T(t) law for the bath.")

# ---------------- (3) does the shell read through the standard calibration shift H0? ----------------
print()
print("(3) TENSION DIRECTION: 147 Mpc shell through the standard calibration")
print("-" * 78)
print("Standard CMB chain: theta* = r_s(z_drag)/D_M(z_rec), r_s ~ 147.09 Mpc (DESI r_d).")
print(f"PWC's formation shell is pinned at the SAME length, {RD_DESI:.2f} Mpc (adopted from BAO).")
print("A calibration uses the LENGTH, not the label: 147 Mpc in -> H0 = 67.4 out. Shift = 0.")
r_s_req = RD_DESI * PLANCK / H0_wall
dr_s    = r_s_req - RD_DESI
print(f"To close 67.4 -> 73.8 by recalibration (H0 ~ 1/r_s at fixed theta*):")
print(f"  r_s needed = 147.09*67.4/73.8 = {r_s_req:.2f} Mpc  (Delta = {dr_s:+.2f} Mpc = {dr_s/RD_DESI*100:+.2f}%)")
print(f"  DIRECTION: a SHORTER ruler raises H0; 73.8 needs the shell at {r_s_req:.0f} Mpc.")
print(f"  vs DESI's measured r_d = 147.09 +- 0.26 Mpc: the shift is {abs(dr_s)/0.26:.0f} sigma from the")
print("  measured BAO ruler - and it contradicts the framework's own pinned 147 Mpc reading.")

# thermostat channel: does the bath temperature enter the Planck H0 chain?
print()
print("Does the 54 K -> 2.7 K bath evolution bias the Planck calibration?")
print("  Planck's H0 is anchored on theta* and the recombination physics, not on the")
print("  bath temperature; T0 enters only as the blackbody-monopole calibration and")
print("  via Omega_gamma*h^2 ~ T0^4 (FIRAS-fixed at 2.7255 K, 0.02% precision).")
print("  The past bath temperature is not an input at all (Planck measures today's CMB).")
print("  The repo derives NO bath cooling law T(t); the bath is 'accumulated, thermalized")
print("  ancient exhaust' (demand_function sec 8), and the c_H datum is a definition, not")
print("  an evolution equation. So the thermostat channel gives a calibration shift of ~0.")
print("  The framework's own claimed Planck-side mechanism is the INHOMOGENEITY route")
print("  (73.8 in walls / ~0 in voids), not a cooling-bath calibration bias.")

# ---------------- (4) verdict numbers ----------------
print()
print("(4) HONEST VERDICT - THE NUMBERS")
print("-" * 78)
print(f"H0_wall (computed, SH0ES side)          = 73.8 km/s/Mpc  (ratio to 73.04: 1.010)")
print(f"  spread from R_p 0.84-0.88 fm         = 73.8 -> {H0_wall_hi:.1f} km/s/Mpc")
print(f"Planck-side 67.4 (asserted, not derived)= volume avg of 73.8 (walls) and ~0 (voids)")
print(f"  wall volume fraction that requires    = {f_wall*100:.1f}%  [OPEN: t7 'quantitative void-vs-wall' row]")
print(f"Calibration-shift route would need      = r_s {r_s_req:.2f} Mpc ({dr_s/RD_DESI*100:+.1f}%)  [not computed, contradicts 147 Mpc]")
print(f"Thermostat 54 K = 2.7/0.05              = {T54:.0f} K  [parent framing; not in repo; no T(t) law]")
print(f"Tension itself: 73.8-67.4 = {H0_wall-PLANCK:.1f} km/s/Mpc; ratio {H0_wall/PLANCK:.4f} ({ (H0_wall/PLANCK-1)*100:.1f}%)")
print(f"54/2.7 = 20.0 has no entry in theta* or in the {H0_wall/PLANCK:.3f} ratio.")
print()
print("VERDICT: QUANTITATIVE on the SH0ES side only (73.8 is computed from four")
print("fundamentals + R_p). QUALITATIVE for the tension's SIZE on the Planck side:")
print("the 67.4 average is asserted with the needed 91.3% wall fraction uncomputed,")
print("the calibration-shift route would need r_s = 134.3 Mpc (never computed, and")
print("49 sigma off DESI's measured ruler), and the thermostat (54 -> 2.7 K) carries")
print("no equation that enters the CMB H0 chain at all.")
