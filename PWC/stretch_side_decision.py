# Stretch-side decision document + chirality coupling closure (round 9)
import math
c0 = 2.99792458e8
c0sq = c0**2
rho0 = 8.74e-27
rhomax = 1.304e15
s = 1.0/19.0
hbar = 1.05457e-34

print("== A. Three readings of the sealed 'negative pressure' language ==")
print("(1) STATIC under the tension-heat law Y = s rho c0^2/3:")
print(f"    P_net = (1-s) rho c0^2/3 = 0.9474 * rho c0^2/3 > 0 for ALL rho on the gas branch")
print(f"    -> no static sign change anywhere; the sealed 'net P negative beyond what Y holds'")
print(f"       (DERIVATION_BRIEF T3) is NOT reproducible under Y ~ rho.")
print("(2) DYNAMIC cavitation, 1/2 rho v^2 = Y (the cohesion-report's derived law):")
v_cav0 = c0*math.sqrt(2*s/3.0)
print(f"    v_cav(rho0) = c0 sqrt(2s/3) = {v_cav0/1e3:.0f} km/s on the gas branch (density-independent)")
print(f"    wake check: 1/2 rho_max (954 km/s)^2 = {0.5*rhomax*954e3**2:.3e} Pa = Y_bow = 5.93e26 EXACT")
print(f"    -> the wake is a rho_max phenomenon; the gas-branch threshold (56,000 km/s) is not")
print(f"       contradicted by anything observed (nothing moves that fast through the medium).")
print("(3) SEALED bookkeeping: the 1.053 stretch (5.3% volume, 95% of final volume) is cosmology")
print("    arithmetic (OPEN_WORK:124), not a local threshold - it never claimed a local sign change.")
print("RECONCILIATION PROPOSAL: 'negative pressure' = the dynamic pull exceeding Y (reading 2)")
print("plus Jaden's low-side reading; static P_net stays positive (reading 1); the 1.053 is")
print("bookkeeping (reading 3). All three coexist; nothing tears. A literal static P_net < 0")
print("baseline would require a new stretch-side Y(rho) law - Jaden's call, prepared either way.")

print("\n== B. Chirality: the kinematic confinement is NOT the yank ==")
a = (hbar/(rho0*c0))**0.25
mw = rho0*a**3/2.0
E_pair = math.pi*hbar*c0/a
k_zp = 2*math.pi*hbar*c0/a**3
k_eps = 1.0/(8.854187817e-12*a)
print(f"a = {a:.3e} m ; pair standing-wave energy E = pi*hbar*c0/a = {E_pair:.4e} J")
print(f"  = {E_pair/(mw*c0sq):.3f} x m_w c0^2  (the 2*pi is angular bookkeeping: m_w = hbar/(2 a c0))")
print(f"zero-point yank k_zp = 2 pi hbar c0/a^3 = {k_zp:.3e} N/m")
print(f"eps0-spring  k     = 1/(eps0 a)         = {k_eps:.3e} N/m  -> {k_eps/k_zp:.0e}x stronger")
print("-> the pair's confinement geometry (hbar) fixes the mass and spacing, but the YANK is a")
print("   separate, 3.6e28x stronger coupling datum = eps0 itself. The opposite-chirality")
print("   coupling law remains the single open input for eps0/mu0; chirality ruled WHAT the")
print("   pair is, not the coupling magnitude.")
