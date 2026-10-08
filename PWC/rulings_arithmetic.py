# Arithmetic consequences of Jaden's three rulings (2026-10-08 10:48)
import math
c0 = 2.99792458e8
c0sq = c0**2
rho0 = 8.74e-27
rhomax = 1.304e15
Msun = 1.989e30
kpc = 3.0857e19

print("== RULING 1 (path a): the locked dilution prediction ==")
# conventional swept-gas budget (Kaul & Oh, OPEN_WORK:93): 1e7-1e8 Msun; PWC admixture capped
for M_gas in (1e7, 1e8):
    for M_pwc, lab in ((1232.0, "zone inventory"), (15535.0, "inventory+swept ceiling")):
        d = M_pwc/M_gas
        ddex = math.log10(1.0 - d)
        print(f"  gas {M_gas:.0e} Msun, PWC cap {lab} {M_pwc:.0f} Msun: "
              f"dilution d={d:.2e} -> Delta(O/H) = {ddex:.2e} dex")
print("  frozen bar: -0.10 dex.  Cap prediction: 2-5 orders below the bar -> the bar is")
print("  unreachable under path (a); a -0.10 dex pass refutes the cap.")

print("\n== RULING 2a (chirality): q_w = e candidate for mu0 ==")
hbar = 1.05457e-34
mu0_real = 4*math.pi*1e-7
e = 1.602176634e-19
a0 = (hbar/(rho0*c0))**0.25
mw = rho0*a0**3/2.0
mu0_cand = mw*a0/e**2
print(f"  a = {a0:.3e} m, m_w = {mw:.3e} kg;  mu0 = m_w*a/e^2 = {mu0_cand:.3e} N/A^2")
print(f"  vs real mu0 = {mu0_real:.3e}: ratio {mu0_cand/mu0_real:.2f}x  (same order, not clean)")
print("  -> chirality settles WHAT the pair is, not the coupling magnitude; the yank law is")
print("     still open (needs the opposite-chirality coupling form).")

print("\n== RULING 2b (baseline T = 0; 2.7 K = matter's exhaust) ==")
a_rad = 7.5657e-16
T = 2.7255
u_cmb = a_rad*T**4
rho_m = (5.0/95.0)*rho0
print(f"  CMB energy density = {u_cmb:.3e} J/m^3")
print(f"  per kg of MEDIUM: {u_cmb/rho0:.3e} J/kg = {u_cmb/(rho0*c0sq):.3e} c0^2")
print(f"  per kg of MATTER: {u_cmb/rho_m:.3e} J/kg = {u_cmb/(rho_m*c0sq):.3e} c0^2")
print(f"  -> the 2.7 K bath holds {100*u_cmb/(rho_m*c0sq):.3f}% of ONE c0^2 per kg of matter")
print(f"     = {100*u_cmb/(rho_m*32.371*c0sq):.4f}% of the full 32.371 c0^2 ladder per kg")
print(f"  RBH-1 flash escape fraction (2.45e-4) sits in the same order band -> the bath is")
print(f"  the radiated sample of the tying exhaust; the bulk is the invisible spacer heat H0.")

print("\n  H0-floor reading: exhaust of an initially fully-tied inventory")
print(f"  today's matter (5/95) exhaust per kg of medium = 0.0526 * 32.371 c0^2 = "
      f"{0.0526*32.371:.3f} c0^2")
print(f"  100% initially tied -> {32.371:.3f} c0^2 per kg of present medium = the H0 floor exactly.")
print(f"  -> consistent reading: the spacer heat IS the great freeze's exhaust (everything")
print(f"     tied once, 95% melted since); baseline T = 0 means no primordial heat at all.")
print(f"     Today's matter alone can only refill {100*0.0526:.1f}% of the floor -> the heat")
print(f"     is mostly ancient, which is consistent with 'voids are the soup that already cooked'.")

print("\n== RULING 3 (no snap; energy field, not fluid) ==")
Y_coh = 0.061379*rhomax*c0sq
Y_bow = 5.93e26
print(f"  Y_coh = {Y_coh:.3e} Pa (high-pressure side, Max-P cohesion)")
print(f"  Y_bow = {Y_bow:.3e} Pa (low-pressure side, wake boundary) - ratio {Y_coh/Y_bow:.1e}x")
print(f"  -> no tear threshold: two points on ONE smooth pressure field; the passage limit")
print(f"     is where the field's local pressure gradient can no longer drive the body through.")
print(f"  The demand function's dP*dV is field-energy bookkeeping (energy density x volume),")
print(f"  valid in field language; water stays an ANALOG benchmark, not the ontology.")
