# =====================================================================
# PWC math check: FRB = re-tensioning snap ("micro GW150914 release")
# Hypothesis under test:
#   A structural mass crossing its kinematic yield cap (v > v_max(rho))
#   cavitates the medium; the FRB is the high-frequency snap as the
#   fluid collapses back to baseline.
#   Locked clocking: collapse timescale of a bubble of radius R = R/c0,
#   characteristic frequency ~ c0/R.
#
# Locked numbers (repo):
#   rho_max = 1.304e15 kg/m^3      (DERIVATIONS.md row 5)
#   Y_bow   = 5.93e26 Pa           (DERIVATIONS.md row 15)
#   c0      = 2.998e8 m/s
#   v_max(rho) = sqrt(2Y/rho)      (row 15: 1/2 rho v^2 = Y)
#   GW150914: 3 Msun released, tau = 4.68 ms, f = 150 Hz, h ~ 4e-21
#   Stagnation cross-check (row 56): R* = 886 km, M* = 1,910 Msun at rho_max
#   Energy = mass (row 13): released energy of mass m is m*c0^2
# =====================================================================

c0      = 2.998e8     # m/s
rho_max = 1.304e15    # kg/m^3
Y_bow   = 5.93e26     # Pa
Msun    = 1.989e30    # kg
G       = 6.674e-11

# observed FRB population targets
tau_obs  = (0.1e-3, 10e-3)          # s
f_obs    = (0.1e9, 8e9)             # Hz
E_obs    = (1e31, 1e33)             # J
DM_max   = 3000.0                   # pc/cm^3

def vol(R):  return 4.0/3.0*3.141592653589793*R**3
def R_of_V(V): return (3.0*V/(4.0*3.141592653589793))**(1.0/3.0)

print("="*72)
print("(0) Locked quantities")
v_max = (2*Y_bow/rho_max)**0.5
print(f"  v_max(rho_max) = sqrt(2Y/rho_max) = {v_max:.4g} m/s = {v_max/1e3:.1f} km/s  (repo: 954)")
# energy scales
print(f"  rho_max*c0^2     = {rho_max*c0**2:.4g} J/m^3   (mass-energy density)")
print(f"  Y_bow            = {Y_bow:.4g} J/m^3      (tension-energy density)")
print(f"  ratio m*c0^2 : Y*V  = {rho_max*c0**2/Y_bow:.3g}  -> mass-energy is "
      f"~2e5 x the tension energy of the same bubble")
# stagnation cross-check
V_stag = vol(886e3); M_stag = rho_max*V_stag
print(f"  cross-check (row 56): R=886 km, rho_max sphere -> M = {M_stag/Msun:.0f} Msun (repo: 1,910)")

print("="*72)
print("(1) OBSERVED FRB POPULATION (targets to match)")
print(f"  durations    tau ~ {tau_obs[0]*1e3:g}-{tau_obs[1]*1e3:g} ms")
print(f"  frequencies  f   ~ {f_obs[0]/1e9:g}-{f_obs[1]/1e9:g} GHz")
print(f"  energies     E   ~ {E_obs[0]:.0e}-{E_obs[1]:.0e} J (isotropic)")
print(f"  DM up to {DM_max:.0f} pc/cm^3 (extragalactic columns; "
      f"DM=3000 at <n_e>=2e-7/cm^3 -> ~15 Gpc)")
print(f"  observed f*tau product ~ {f_obs[0]*tau_obs[0]:.0e} to {f_obs[1]*tau_obs[1]:.0e}")

print("="*72)
print("(2) DURATION AXIS: tau = R/c0  ->  R, mass, f, energies")
print(f"{'tau':>8} {'R':>10} {'f=c0/R':>12} {'mass':>12} {'M/Msun':>12} "
      f"{'Y*V (J)':>12} {'m*c0^2 (J)':>14}")
for tau in (0.1e-3, 1e-3, 10e-3):
    R  = c0*tau
    m  = rho_max*vol(R)
    f  = c0/R
    YV = Y_bow*vol(R)
    mc2= m*c0**2
    print(f"{tau*1e3:6.1f}ms {R/1e3:9.1f}km {f:9.1f}Hz {m:12.4g} {m/Msun:11.4g} "
          f"{YV:12.3g} {mc2:14.3g}")
print("  -> the ms-duration bubble is 30-3,000 km and holds 0.07-74,000 Msun")
print("     of rho_max medium: a stellar-mass-to-supermassive chunk, NOT micro.")

print("="*72)
print("(3) FREQUENCY AXIS: f = c0/R  ->  R, tau, mass, energies")
print(f"{'f':>10} {'R':>12} {'tau=R/c0':>12} {'mass':>12} {'M/Msun':>12} "
      f"{'Y*V (J)':>12} {'m*c0^2 (J)':>14}")
for f in (0.1e9, 1e9, 8e9):
    R  = c0/f
    tau= R/c0
    m  = rho_max*vol(R)
    YV = Y_bow*vol(R)
    mc2= m*c0**2
    print(f"{f/1e9:6.1f}GHz {R:11.4g}m {tau:12.3g}s {m:12.4g} {m/Msun:11.4g} "
          f"{YV:12.3g} {mc2:14.3g}")
print("  -> the GHz bubble is 4 cm - 3 m and collapses in 0.1-10 ns, not ms.")
print(f"     its mass-energy {1.47e14*c0**2:.2g} J (1 GHz) is right in the FRB band.")

print("="*72)
print("(4) ENERGY AXIS: E_obs = 1e31-1e33 J  ->  required bubble")
print("    reading A: released ENERGY = TENSION ENERGY Y*V")
print(f"{'E (J)':>10} {'R':>10} {'tau':>12} {'f=c0/R':>12} {'mass':>12} {'M/Msun':>12}")
for E in (1e31, 1e32, 1e33):
    V  = E/Y_bow
    R  = R_of_V(V)
    tau= R/c0
    f  = c0/R
    m  = rho_max*V
    print(f"{E:.0e} {R:9.2f}m {tau:12.3g}s {f/1e6:9.1f}MHz {m:12.4g} {m/Msun:11.4g}")
print("    reading B: released ENERGY = MASS-ENERGY m*c0^2 (row 13: energy=mass)")
print(f"{'E (J)':>10} {'m (kg)':>12} {'M/Msun':>12} {'R':>10} {'tau':>12} {'f=c0/R':>12}")
for E in (1e31, 1e32, 1e33):
    m  = E/c0**2
    V  = m/rho_max
    R  = R_of_V(V)
    tau= R/c0
    f  = c0/R
    print(f"{E:.0e} {m:12.4g} {m/Msun:11.4g} {R:9.3f}m {tau:12.3g}s {f/1e9:9.3f}GHz")

print("="*72)
print("(5) MERGER COMPARISON (GW150914: 3 Msun, 4.68 ms, 150 Hz, h=4e-21)")
M_rel  = 3.0*Msun
E_gw   = M_rel*c0**2
print(f"  E_gw = 3 Msun * c0^2 = {E_gw:.3g} J")
print(f"  f*tau = {150*4.68e-3:.2f}  (merger obeys the single-bubble coherence!)")
print(f"  c0*tau = {c0*4.68e-3/1e3:.0f} km ; c0/f = {c0/150/1e3:.0f} km  (self-consistent)")
print(f"  FRB/merger energy ratio : {E_obs[0]/E_gw:.1g} - {E_obs[1]/E_gw:.1g}")
print(f"  FRB/merger freq. ratio  : {f_obs[0]/150:.1g} - {f_obs[1]/150:.1g}")
print("  -> energy scales DOWN by ~1e-15, frequency scales UP by ~1e6: the FRB")
print("     is NOT a self-similar scaled copy of the merger. At fixed strain")
print("     E ~ f, so the merger rescaled to 1 GHz would carry ~3.6e54 J,")
print("     21-23 orders above the FRB band.")
h_frb = 4e-21*((E_obs[0]/E_gw)**0.5)*(410/1000)   # same channel, ~1 Gpc vs 410 Mpc
print(f"  illustrative: FRB at 1 Gpc on the strain channel -> h ~ {h_frb:.0e}")

print("="*72)
print("(6) THE INCOHERENCE: single-bubble snap forces  f*tau = 1")
print(f"  hypothesis: f = c0/R and tau = R/c0  ->  f*tau = 1 exactly (any speed)")
print(f"  observed :  f*tau ~ {f_obs[0]*tau_obs[0]:.0e} to {f_obs[1]*tau_obs[1]:.0e}  "
      f"(5-8 orders too large)")
print("  -> the FRB's ms duration is ~1e6 collapse-times of the bubble whose")
print("     size makes its GHz frequency. One bubble cannot do both.")

print("="*72)
print("(7) ROBUSTNESS: clock the collapse at v_max(rho_max)=954 km/s instead of c0")
for tau in (1e-3,):
    R = v_max*tau
    m = rho_max*vol(R)
    print(f"  tau=1ms -> R={R/1e3:.2f} km, mass={m:.3g} kg = {m/Msun:.3g} Msun, "
          f"f=v/R={v_max/R:.0f} Hz, Y*V={Y_bow*vol(R):.2g} J, m*c0^2={m*c0**2:.2g} J")
print("  -> mass becomes plausible (2e-6 Msun), but f*tau = 1 still: 1 kHz,")
print("     and energies (1e36-1e41 J) stay far above the FRB band. f*tau=1 is")
print("     speed-independent, so no choice of restoring speed saves the triple.")
print("="*72)
