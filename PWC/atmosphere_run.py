# The atmosphere run (2026-10-09): the electron's weather, in the framework's own units
import math
G = 6.6743e-11; a0 = 6.6e-11
me = 9.1093837e-31; e = 1.602176634e-19; eps0 = 8.8541878128e-12
c0 = 2.99792458e8; hbar = 1.054571817e-34
rho0 = 8.74e-27; rho_max = 1.304e15; s = 1.0/19.0
Y_cav = s*rho0*c0**2/3.0
mp = 1.6726e-27

r_reach = math.sqrt(G*me/a0)
r_e = e**2/(4*math.pi*eps0*me*c0**2)
lamC_bar = hbar/(me*c0)

print("== 1. The atmosphere's true extent, in the framework's own units ==")
# pair binding = the tension energy of the pair's own volume; tearing field = work over spacing
m_w = mp/3.0
V_pair = m_w/rho0
E_bind = Y_cav*V_pair
d_pair = V_pair**(1/3.0)
E_tear = E_bind/(e*d_pair)
r_tear = math.sqrt(e/(4*math.pi*eps0*E_tear))
print(f"pair binding E_bind = Y_cav*V_pair = {E_bind:.3e} J ; pair spacing d = {d_pair:.3f} m")
print(f"tearing field E_tear = {E_tear:.3e} V/m ; tearing radius r_tear = {r_tear:.3e} m = {r_tear/1e-9:.2f} nm")
print(f"the electron's field tears the AMBIENT pairs out to {r_tear/1e-9:.1f} nm - the weather's extent")

print("\n== 2. What the atmosphere actually holds ==")
M_atm = rho0*4*math.pi*r_reach**3/3.0
N_pairs = 4*math.pi*r_tear**3/3.0/V_pair
print(f"held mass inside the gravitational reach: {M_atm:.2e} kg = {M_atm/me:.1e} m_e - EMPTY")
print(f"torn pairs inside the 10-nm cloud: {N_pairs:.1e} pairs - EMPTY (less than one pair)")
print(f"-> the external atmosphere carries NOTHING. No screen, no pile. The electron's field")
print(f"   is naked in the ambient medium.")

print("\n== 3. So the atmosphere that matters is the knot's interior ==")
V_knot = me/rho_max
R_knot = (3*V_knot/(4*math.pi))**(1/3)
N_waves = me/m_w
print(f"knot volume at rho_max = {V_knot:.3e} m^3 -> tight-sphere radius R_knot = {R_knot/1e-15:.3f} fm")
print(f"me/m_w = {N_waves:.3e} (m_w = m_p/3) - the electron is FAR lighter than one matter wave:")
print(f"the electron IS one wave of its own mass scale (m_e R c0 = hbar, the 1-quantum knot).")
print(f"the ladder: knot {R_knot/1e-15:.2f} fm -> reach {r_reach/1e-15:.2f} fm -> fold {r_e/1e-15:.2f} fm")
print(f"ratios: reach/knot = {r_reach/R_knot:.3f} (vs sqrt3 = {math.sqrt(3):.3f}) ;")
print(f"        fold/reach = {r_e/r_reach:.3f} (vs 3)")
print(f"chained near-misses sqrt3 and 3 - reported, no mechanism")

print("\n== 4. Verdict ==")
print(f"The external atmosphere is empty - the 2.2% reach/fold near-miss has no medium to")
print(f"carry it, and dies as a mechanism. The interior holds ONE wave (the electron itself),")
print(f"so the 137.036 dilution cannot come from counting waves - it must come from the ONE")
print(f"wave's own structure: the 720-degree double-loop harmonic. The 'atmosphere' is the")
print(f"knot's own tight sphere; the screen is the single wave's self-interaction geometry.")
