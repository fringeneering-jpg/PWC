# Closure-rate reconciliation for the RBH-1 cavity (arithmetic on sealed numbers)
# Question: the sealed statement says the cavity walls close at c0 each (gap at 2c0).
# A 0.7 kpc-radius cavity closing at that rate lives ~2,000-5,000 yr. The wake is
# observed to persist ~73 Myr with continuous star formation. What reconciles the two?
import math

c0 = 2.998e8
rho_max = 1.304e15
rho0 = 8.74e-27
kpc = 3.0857e19
yr = 365.25*86400

r = 0.7*kpc          # trail radius
L = 62*kpc           # wake length
v_bh = 954e3         # m/s
age = 73e6*yr

print("== Naive closure rates ==")
t_2c0 = r/c0                          # each wall closes on the centre at c0
print(f"walls at c0 each: t_close = r/c0 = {t_2c0/yr:.0f} yr")
t_rayleigh = 0.915*r*math.sqrt(rho_max/(rho_max*c0**2))   # Rayleigh: R*sqrt(rho/Pmax)
print(f"Rayleigh collapse at P_max: t = 0.915*R*sqrt(rho/P) = {t_rayleigh/yr:.0f} yr")
# pressure-deficit refill: zone stretched 5% (1.053 stretch) -> P deficit ~ (1-0.95)*rho0 c0^2/3
dP = 0.05*rho0*c0**2/3.0
u_in = math.sqrt(2*dP/rho0)
print(f"5% stretch pressure deficit = {dP:.2e} Pa -> refill u = {u_in/c0:.3f} c0, "
      f"t_close = r/u = {r/u_in/yr:.0f} yr")
print(f"observed persistence = {age/yr:.0f} yr -> gap = {age/max(t_2c0,t_rayleigh):.0f}x")

print("\n== Steady-state reading: cavity maintained open, not closed by c0 ==")
# steady state: cavity opened at the bow at v_bh, closed behind; length L = v_bh * r / u_refill
u_refill = v_bh*r/L
print(f"implied side-refill speed u = v_bh*r/L = {u_refill/1e3:.1f} km/s "
      f"({u_refill/(c0/math.sqrt(3)):.2e} of c_s0)")

print("\n== Two degenerate readings of the conversion (same observed mdot) ==")
mdot = 1e6*1.989e30/age          # 1e6 Msun / 73 Myr
Vdot_full = 2*math.pi*r**2*c0    # full cross-section sweep at 2c0
rho_mist_full = mdot/Vdot_full
print(f"full 2c0 sweep: rho_mist = {rho_mist_full/rho0:.3f} rho0")
rho_stretched = 0.95*rho0        # just-stretched medium (1.053 stretch limit)
duty = mdot/(rho_stretched*Vdot_full)
print(f"mist at 0.95 rho0: collapse duty cycle = {duty:.3f} of the full sweep "
      f"(effective closure ~{duty*2:.2f} c0)")
print(f"sealed text: the zone is 'rarefied, vapor/mist-like' (PWC.md sec8 line 453) "
      f"-> favours rho_mist ~ 0.1 rho0, full sweep")

print("\n== What this pins on the missing bow-wave profile ==")
print("Any profile derivation must produce: (1) a cavity that persists 73 Myr against")
print("2,000-5,000 yr naive closure (gap ~1.5-3.5e4x) -> the cavity is re-opened at the bow")
print("as fast as it closes, length set by side-channel dynamics, NOT by the c0 closure;")
print("(2) the c0/2c0 closure applies per-pocket (the matter-formation slam), not to the")
print("whole cavity; (3) a zone mist at ~0.1 rho0 if the sweep is full.")
