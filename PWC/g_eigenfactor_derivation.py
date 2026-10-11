# g = 16*pi^3*alpha/3 = 1.2067 -- the charge eigenfactor, all three routes (2026-10-08 session)
# Scratch work (session scratchpad, NOT in the clone). Pure stdlib.
# Locked PWC pieces used: coupling law (grip = f(heat expelled), flat at rest, x7 plateau),
# caloric law H(rho) = H0 - (c0^2/3)ln(rho/rho0) with plateau drop exactly c0^2/kg, H0 >= 32.371 c0^2,
# proton identity m R c0 = 4 hbar, Jaden's volumetric reframing (heat's VOLUME squeezed out).
# External: WvdM/Benn idealized q' = sqrt(3 eps0 h c / (8 pi^3)); Lai 2026 Born-Infeld route.
import math

# ---- locked / CODATA constants ----
eps0 = 8.8541878128e-12
mu0  = 4*math.pi*1e-7
h    = 6.62607015e-34
hbar = 1.054571817e-34
c0   = 2.99792458e8
e    = 1.602176634e-19
me   = 9.1093837e-31
mp   = 1.67262192e-27
Rp   = 0.8414e-15            # proton charge radius (Antognini 2013, repo value)
alpha= e*e/(4*math.pi*eps0*hbar*c0)
rho_max = 1.304e15           # locked (GW150914)
rho0    = 8.74e-27           # locked (T2)
s       = 1.0/19.0           # locked stretch share
kappa   = 3.49860            # locked cohesion channel factor (Y_coh = kappa s P_locked/3)
P_locked= rho_max*c0*c0
lamC    = h/(me*c0)
V_id    = math.pi*lamC**3/6.0      # WvdM rotational-horizon volume, r_hor = lamC/2
R_id    = lamC/(4*math.pi)         # WvdM transport radius
qprime  = math.sqrt(3*eps0*h*c0/(8*math.pi**3))
g       = (e/qprime)**2

print("="*92)
print("LOCKED INPUTS AND THE TARGET")
print("="*92)
print(f"q' = sqrt(3 eps0 h c /(8 pi^3)) = {qprime:.6e} C = {qprime/e:.4f} e   (idealized WvdM)")
print(f"g = (e/q')^2 = {g:.7f} ;  16 pi^3 alpha / 3 = {16*math.pi**3*alpha/3:.7f}  (alpha = {alpha:.10f})")
print(f"alpha^-1 (idealized geometry) = 16 pi^3 / 3 = {16*math.pi**3/3:.4f} ; observed = {1/alpha:.4f}")
print(f"g = (16 pi^3/3)/137.036 : the eigenmode must move alpha^-1 from 165.37 to 137.036, q^2 x g.")
print(f"[flag] Lai's chain 'linear 150 -> saturated 135.9' is HIS geometry: 0.91e <-> alpha^-1 = 165.4, NOT 150.")
print(f"[flag] q' = 0.9103e  =>  alpha^-1 = {1/(qprime*qprime/(4*math.pi*eps0*hbar*c0)):.2f}, not Lai's 150.")
print()
print(f"WvdM geometry: lamC = {lamC:.4e} m, R = lamC/4pi = {R_id:.4e} m ({R_id/lamC*1e3:.1f}e-3 lamC),")
print(f"r_hor = lamC/2 = {lamC/2:.4e} m, V = pi lamC^3/6 = {V_id:.4e} m^3")
print(f"electron mean field density: me/V_id = {me/V_id:.3e} kg/m^3  (vs fold rho_max/2 = {rho_max/2:.3e})")
print()

# ---------------------------------------------------------------
print("="*92)
print("GENERAL EIGENMODE CONDITION  (q = 4 pi eps0 R^2 <E>, <E>^2 = 2 U_E/(eps0 V), U_E = hc/2lam)")
print("="*92)
print("q^2 = 16 pi^2 eps0 h c R^4/(lam V)   [R = transport radius, V = field volume]")
print("exact eigenmode (q = e):  lam V / R^4 = 8 pi^2 / alpha")
print(f"  target lam V/R^4 = {8*math.pi**2/alpha:.3f}")
print(f"  idealized (R=lam/4pi, V=pi lam^3/6): lam V/R^4 = 128 pi^5/3 = {128*math.pi**5/3:.3f}")
print("  => the eigenmode is ONE dimensionless datum: the ratio  (R/R_id)^4 * (V_id/V) = g")
print(f"  if R is spin-locked at lam/4pi:  V_t/V_id = 1/g = {1/g:.6f}  -> linear squeeze {g**(1/3):.6f}")
print(f"  (the heat-expelled volume fraction = 1 - 1/g = {1-1/g:.6f} = {(1-1/g)*100:.4f}%)")
print()

# ---------------------------------------------------------------
print("="*92)
print("ROUTE 1 -- THE 4-QUANTUM EIGENMODE")
print("="*92)
print("Proton check (locked identity m R c0 = 4 hbar): 2 pi R_p = 4 lamC,p ?")
lamCp = h/(mp*c0)
print(f"  2 pi R_p = {2*math.pi*Rp:.5e} m ; 4 lamC,p = {4*lamCp:.5e} m ; ratio = {2*math.pi*Rp/(4*lamCp):.6f}")
print("  YES: the proton's 360-degree loop carries 4 full Compton wavelengths. R_p = 2 lamC,p/pi.")
print()
print("(a) Electron with the SAME 4-quantum structure (4 full Compton wavelengths per 360 deg):")
print("    2 pi R_e = 4 lamC  =>  R_e = 2 lamC/pi = 8 R_id ; OAM = p R = 4 hbar (spin via the shared cover)")
Re_a = 2*lamC/math.pi
print(f"    R_e = {Re_a:.6e} m = {Re_a/lamC:.4f} lamC = {Re_a/R_id:.2f} x R_id")
print(f"    q scales as R^2 V^-1/2: with R^2 = 64 R_id^2 the volume must grow 64/g = {64/g:.2f}x to keep q=e.")
def qgeom(R, V):
    return math.sqrt(16*math.pi**2*eps0*h*c0*R**4/(lamC*V))
V_hor_a = 4*math.pi*(2*lamC)**3/3.0   # each 4-lamC quantum's own horizon, r = lam_w/2 = 2 lamC
print(f"    natural volume (quantum horizon sphere r=2lamC): V = {V_hor_a:.4e} m^3 -> q = {qgeom(Re_a,V_hor_a)/e:.3f} e")
V_sweep_a = 4*math.pi*Re_a**3/3.0
print(f"    swept-loop sphere V = 4pi R^3/3: -> q = {qgeom(Re_a,V_sweep_a)/e:.3f} e")
V_ball8_a = 4*math.pi*(8*Re_a)**3/3.0   # proton B-identity analog R_ball = 8 R
print(f"    proton-analog B: V = 4pi(8R)^3/3: q = {qgeom(Re_a,V_ball8_a)/e:.3f} e  (reported, no mechanism)")
print(f"    -> the 4-quantum transport radius overproduces charge by 2-41x in every volume reading. FAIL.")
print()
print("(b) Quarter-wave reading (the ONE photon's lamC split into 4 quarter-wave quanta per 360 deg):")
print("    2 pi R_e = lamC  =>  R_e = lamC/2pi ; OAM = p R = hbar (photon spin, halved by the 720-deg cover)")
Re_b = lamC/(2*math.pi)
print(f"    R_e = {Re_b:.6e} m = {Re_b/lamC:.4f} lamC = {Re_b/R_id:.2f} x R_id")
print(f"    horizon sphere V = pi lamC^3/6: q = {qgeom(Re_b,V_id)/e:.3f} e")
V_ball8_b = 4*math.pi*(8*Re_b)**3/3.0   # proton B-identity analog R_ball = 8 R
print(f"    proton-analog B: V = 4pi(8R)^3/3: q = {qgeom(Re_b,V_ball8_b)/e:.4f} e  (= q' sqrt(pi^3/32): {math.sqrt(math.pi**3/32):.5f}, WRONG direction)")
print(f"    -> overshoots by 2x (horizon) or undershoots (B-analog); no reading gives q = e. FAIL.")
print()
print("(c) Spin-locked R = lamC/4pi (the idealized transport radius; p R = hbar/2):")
print("    then g must come ENTIRELY from the volume: V_t = V_id/g, r_hor = lam/2 g^-1/3 =",
      f"{lamC/2*g**(-1/3):.6e} m = {0.5*g**(-1/3):.4f} lamC")
print("    two-loop split (sphere reading): big loop l1/lam =",
      f"{g**(-1/3):.7f}, tiny loop l2/lam = {1-g**(-1/3):.7f}")
print(f"    needed tiny-loop fraction 1 - g^-1/3 = {1-g**(-1/3):.7f}")
print(f"    near-misses: 2/(19 sqrt3) = {2/(19*math.sqrt(3)):.7f} ({100*(2/(19*math.sqrt(3))/(1-g**(-1/3))-1):+.3f}%),")
print(f"    1/16 = {1/16:.7f} ({100*((1/16)/(1-g**(-1/3))-1):+.3f}%), Y_coh/P_locked = {kappa*s/3:.6f}",
      f"({100*(kappa*s/3/(1-g**(-1/3))-1):+.2f}%)")
print("    NONE is exact and NONE has a mechanism in the locked set (reported, not claimed).")
print("    -> Route 1 fails: the locked set contains no condition that fixes V_t/V_id = 1/g.")
print()

# ---------------------------------------------------------------
print("="*92)
print("ROUTE 2 -- FULL RADIAL-PROFILE SATURATION INTEGRAL")
print("="*92)
print("Coulomb profile E(r) = q/(4 pi eps0 r^2) inside the WvdM horizon r_hor = lamC/2;")
print("U_E(q) = int_0^r_hor u(E(r)) 4 pi r^2 dr = m_e c^2/2 ; solve for q.")
r_hor = lamC/2.0
Ue = me*c0*c0/2.0

def Efield(q, r): return q/(4*math.pi*eps0*r*r)

def integrand_u(q, r, uform):
    E = Efield(q, r)
    return uform(E, q)*4*math.pi*r*r

def integrate(q, uform, rmin=1e-22, n=40000):
    # log-spaced trapezoid, saturating u(E) makes r->0 converge
    s = 0.0
    lr = math.log(rmin); lR = math.log(r_hor)
    for i in range(n):
        l1 = lr + (lR-lr)*i/n; l2 = lr + (lR-lr)*(i+1)/n
        r1 = math.exp(l1); r2 = math.exp(l2)
        s += 0.5*(integrand_u(q, r1, uform) + integrand_u(q, r2, uform))*(r2-r1)
    return s

def solve_q(uform, q0=1e-19):
    lo, hi = 1e-21, 1e-17
    for _ in range(60):
        mid = math.sqrt(lo*hi)
        if integrate(mid, uform) > Ue: hi = mid
        else: lo = mid
    return math.sqrt(lo*hi)

# (i) Born-Infeld, fixed b = E_S (Lai):  u = b^2 (sqrt(1+eps0 E^2/b^2) - 1)
ES = me*me*c0**3/(e*hbar)
uBI = lambda E, q: ES*ES*(math.sqrt(1+eps0*E*E/(ES*ES)) - 1)
q_bi = solve_q(uBI)
print(f"(i)  BI fixed b = E_S = {ES:.3e} V/m  (Lai's functional, WvdM horizon + Coulomb profile):")
print(f"     q = {q_bi/e:.4f} e ; alpha^-1 = {4*math.pi*eps0*hbar*c0/q_bi**2:.1f}   (Lai cylindrical limit: 135.9)")
print(f"     U_BI(q=e) = {integrate(e, uBI):.3e} J = {integrate(e, uBI)/Ue:.1f} x m_e c^2/2  -> at q=e the field costs {integrate(e, uBI)/Ue:.0f}x the budget")
print(f"     [reason: the Coulomb profile keeps 1/r^2 all the way down; the BI crossover sits at")
print(f"      r_cross = {math.sqrt(e*math.sqrt(eps0)/(4*math.pi*eps0*ES)):.3e} m = 0.057 fm << r_e = 2.82 fm, so saturation")
print(f"      trims almost nothing. Lai's 135.9/0.996e uses HIS torus-tube geometry (E ~ bag-like inside")
print(f"      the tube, a natural fm cutoff from the geodesic constraint), not the WvdM horizon sphere.]")

# (ii) BI with the knot's own charge in the Schwinger scale: b(q) = m_e^2 c^3/(q hbar)
uBIq = lambda E, q: (me*me*c0**3/(q*hbar))**2*(math.sqrt(1+eps0*E*E/(me*me*c0**3/(q*hbar))**2) - 1)
q_biq = solve_q(uBIq)
print(f"(ii) BI with b = b(q) = m_e^2 c^3/(q hbar)  (the repo's self-consistent functional):")
print(f"     q = {q_biq/e:.4f} e ; alpha^-1 = {4*math.pi*eps0*hbar*c0/q_biq**2:.1f}")
print(f"     [b grows as q shrinks, so the saturation always runs away from the knot: no fixed point")
print(f"     near e. The repo's uniform-core (average-density) solve of this functional landed at 163.0;")
print(f"     the radial-profile solve lands at {4*math.pi*eps0*hbar*c0/q_biq**2:.0f}. Both wrong, differently.]")

# (iii) PWC heat-function saturation: grip flat below the fold, x7 across the plateau.
# u = (1/2) eps0 E^2 / f(rho)  with  f = 7^S , S = 2 - rho_max/rho (lever rule), rho = u/c^2.
# Below the fold u < rho_max c^2/2 the grip is at rest (f=1, linear).
def uPWC(E, q):
    u_lin = 0.5*eps0*E*E
    A = rho_max*c0*c0
    if u_lin <= A/2: return u_lin
    # implicit plateau: u * 7^(2 - A/u) = u_lin ; bisect u in [A/2, A]
    lo, hi = A/2, A
    for _ in range(80):
        mid = 0.5*(lo+hi)
        lhs = mid*(7.0**(2 - A/mid))
        if lhs > u_lin: hi = mid
        else: lo = mid
    return 0.5*(lo+hi)
q_pwc = solve_q(uPWC)
a_pwc = q_pwc*q_pwc/(4*math.pi*eps0*hbar*c0)
print(f"(iii) PWC coupling-law functional (flat grip below the fold rho_max/2, x7 by rho_max):")
print(f"      fold field E_fold = sqrt(rho_max c^2/eps0) = {math.sqrt(rho_max*c0*c0/eps0):.3e} V/m =",
      f"{math.sqrt(rho_max*c0*c0/eps0)/ES:.0f} x E_S")
print(f"      q = {q_pwc/e:.3f} e ; alpha^-1 = {1/a_pwc:.1f}   (needs 137.036)")
print(f"      U_PWC(q=e) = {integrate(e, uPWC):.3e} J = {integrate(e, uPWC)/Ue:.1f} x m_e c^2/2")
print(f"      [the PWC stiffening engages at the fold density {rho_max/2:.1e} kg/m^3, {rho_max/2/(ES*ES*eps0/(2*c0*c0)):.1e} x the")
print(f"      Schwinger density; its saturated core still costs {integrate(e,uPWC)/Ue:.1f}x the budget at q=e -> q collapses. FAIL.]")

# (iv) The bag-model form of the SAME circle: uniform core E0 = q/(4 pi eps0 r0^2) + Coulomb outside.
# Linear: U = (7/6) q^2/(8 pi eps0 r0) - q^2/(8 pi eps0 r_hor).  U = m_e c^2/2 with q = e forces r0:
r0_circle = (7.0/6.0)*e*e/(8*math.pi*eps0*(Ue + e*e/(8*math.pi*eps0*r_hor)))
re_cl = alpha*lamC/(2*math.pi)
print(f"(iv) Bag model (uniform core + Coulomb outside), linear grip: q = e <=> core radius")
print(f"     r0 = (7/6) r_e = {r0_circle:.4e} m = {r0_circle/re_cl:.4f} x r_e,  r_e = alpha lamC/2pi = {re_cl:.4e} m")
print(f"     -- the classical electron radius, which CONTAINS alpha. The cutoff is alpha in, alpha out:")
print(f"     every saturation functional only changes the prefactor (BI, b(q), PWC plateau all land on")
print(f"     'r0 ~ r_e' in their own variables). A derivation needs an INDEPENDENT electron-scale core")
print(f"     length, and the locked set {{rho_max, rho0, c0, s, 7, 32.371}} contains none.")
print(f"     Lai's 135.9 gets its core from his torus geodesic constraint (unpublished detail); the PWC")
print(f"     set has no electron-scale datum. FAIL with the missing input named.")
print()

# ---------------------------------------------------------------
print("="*92)
print("JADEN'S CHARGE STATEMENT FORMALIZED (his words: locked outward push = charge;")
print("the heat's volume squeeze concentrates it. capture/2026-10-09_0556_charge_locked_push.md)")
print("="*92)
print("charge = the net displacement flux through the transport surface:")
print("  q = D * 4 pi R^2,  D = eps0 <E> = sqrt(2 eps0 U_E / V)   ->   q = 4 pi R^2 sqrt(2 eps0 U_E/V)")
print("free photon: E alternates, net flux cancels -> q = 0.  720-degree knot: phase locked outward -> q.")
print()
print("The squeeze: same wave, same light energy U_E, same wavelength (R = lamC/4pi untouched by")
print("the heat), volume V_id -> V_t = V_id/g. Then <E> spikes by sqrt(g) and q' -> q' sqrt(g) = e.")
print("  q(V) / q' = sqrt(V_id/V):  at V_t/V_id = 1/g = 0.828679  ->  sqrt(g) =", f"{math.sqrt(g):.6f}")
print(f"  -> q = {qprime*math.sqrt(g)/e:.4f} e  (the 0.9103e -> 1.000e spike Jaden stated).")
print()
print("Direction check (locks the squeeze shape): a UNIFORM shrink (R -> R/g^(1/3) AND V -> V/g)")
print(f"  gives q -> q' sqrt(g) / g^(2/3) = q' g^(-1/6) = {qprime*g**(-1/6)/e:.4f} e  -- DOWN, wrong.")
print("  The correct squeeze is volume-only, transport radius untouched: the heat leaves, the")
print("  wavelength stays. Exactly his ruling (same EM wave, heat's volume squeezed out).")
print()
print("Engine now:  phase-lock (WvdM, 0.9103e)  ->  heat-expelled volume squeeze (17.13%)  ->  e.")
print("OPEN: the SOURCE of the 17.13% = 1 - 1/g = 0.171321 in the locked set (report section 6).")
print()

# ---------------------------------------------------------------
print("="*92)
print("THE PAIR EQUILIBRIA JADEN'S STATEMENT IMPLIES (capture/2026-10-09_0606_chiral_pair_movement.md)")
print("="*92)
print("his mechanism: the + and - parts, curled around each other = 1 wave, shrunken in the")
print("cavitation (denser -> more attractive), interacting via the movement. Two natural")
print("equilibrium readings of 'attracted via the movement' for the double loop, R = lamC/4pi,")
print("tube radius r0, circulating current I = q c / lamC:")
print()
print("(1) movement-mediated pinch: B = mu0 I/(2 pi r0), B^2/(2 mu0) = u/3, u = (m_e c^2/2)/V_tube")
qpinch2 = (8.0*math.pi/3.0)*h/(mu0*c0)
print(f"    r0 CANCELS in the equilibrium; q^2 = (8pi/3) h/(mu0 c) -> q = {math.sqrt(qpinch2)/e:.2f} e")
print("(2) +- ring attraction (line-charge limit, separation 2 r0) vs outward field pressure:")
print(f"    r0 CANCELS again; q^2 = (2/3) eps0 h c -> q = {math.sqrt(2.0/3.0*eps0*h*c0)/e:.2f} e")
print(f"    (q' for comparison = {qprime/e:.4f} e ; target = 1.0000 e)")
print("Both equilibria fix q, NOT the knot size, and both miss e. The stated mechanism supplies")
print("the grip's nature (density -> attraction, dynamical) but does not yet contain the 17.13%.")
print()
print("(3) THE SIZE-KEEPING BALANCE (Jaden 2026-10-09: waves chasing around the sphere's surface,")
print("    the middle = the heat that keeps the size; capture/2026-10-09_0644):")
print("    inward pinch of the chasing currents vs the interior heat pressure, at R = lamC/4pi:")
q_heat1 = math.sqrt(8*math.pi*eps0*h*c0)            # B = mu0 I/(2 pi R) loop form
q_heat2 = math.sqrt(4*math.pi*eps0*h*c0)            # B = mu0 K, K = I/(2R) surface form
print(f"    q = {q_heat1/e:.1f} e (loop-field form) / {q_heat2/e:.1f} e (surface-current form)  (needs 1.000)")
R_heat = lamC*lamC/(2*alpha*hbar/(me*c0))            # the balance's radius at q = e, loop form
R_spin_local = hbar/(2*me*c0)
print(f"    at q = e the balance puts the sphere at R = lamC^2/(2 r_e) = {R_heat*1e9:.2f} nm = {R_heat/R_spin_local:.0f} x the spin radius")
print(f"    -> the naive pinch is ~40-70x too strong: the love-hate net pull (likes repel, pairs")
print(f"    partially cancel the chase) is what the heat actually balances, and that net pull is")
print(f"    the eps0 grip datum in disguise. The freeze size still needs that one number.")
print()

# ---------------------------------------------------------------
print("="*92)
print("THE COMPARISON: the proton derivation's engine vs the electron charge")
print("(Jaden's order 2026-10-09: compare proton_derivation_20260930.md and see if it comes out)")
print("="*92)
# (1) the proton method's two identities intersect to R^4 = 3 hbar/(512 pi rho_max c0):
Rp_combined = (3*hbar/(512*math.pi*rho_max*c0))**0.25
print(f"(1) proton combined formula R^4 = 3 hbar/(512 pi rho_max c0) is MASS-INDEPENDENT:")
print(f"    applied to ANY mass it gives R = {Rp_combined*1e15:.4f} fm - the electron would be FORCED to")
print(f"    the proton's radius. Identity B (rho_max inventory) is proton-only; the electron's")
print(f"    inventory is the WvdM horizon, not locked medium. The method does not transplant as-is.")
print()
print("(2) the ONE clean output of comparing the two derivations:")
Re_spin = hbar/(2*me*c0)
print(f"    Identity A(e): m_e R_e c0 = hbar/2 (spin) and A(p): m_p R_p c0 = 4 hbar  =>")
print(f"    m_p/m_e = 8 R_e/R_p = {8*Re_spin/Rp:.2f} EXACTLY; observed m_p/m_e = {mp/me:.2f}  (0.02% = the")
print(f"    R_p rounding). The mass ratio falls out of the two quantizations - but it carries no alpha.")
print()
print("(3) the 4-quantum electron (gate 4 ruling: electron = 4 EM waves) + the proton's B-ball:")
Re4 = 2*lamC/math.pi
Vb8 = 4*math.pi*(8*Re4)**3/3.0
print(f"    R_e = 2 lamC/pi = {Re4:.4e} m ; V = 4pi(8 R_e)^3/3 = {Vb8:.4e} m^3")
print(f"    q = 4 pi eps0 R^2 sqrt(2 U_E/(eps0 V)) = {qgeom(Re4,Vb8)/e:.3f} e   (needs 1.000) - DOES NOT COME OUT.")
print()
# (4) THE CONVERGENCE: three independently-arrived electron-scale lengths
r0_exact = 1.0/(8*math.pi*eps0*Ue/e**2 + 1/r_hor)     # pure Coulomb cutoff giving q = e exactly
r0_bag   = (7.0/6.0)*e*e/(8*math.pi*eps0*(Ue + e*e/(8*math.pi*eps0*r_hor)))
lam_block = (mp/7.475e16)**(1/3.0)
lambar = hbar/(me*c0)
re_cl2 = alpha*lambar
print("(4) THE CONVERGENCE - electron-scale lengths arrived at independently:")
print(f"    core cutoff giving q = e exactly (pure Coulomb + horizon): {r0_exact*1e15:.5f} fm")
print(f"    bag-model cutoff (uniform core + Coulomb):                 {r0_bag*1e15:.5f} fm")
print(f"    classical radius r_e = alpha lam_bar_C:                    {re_cl2*1e15:.5f} fm")
print(f"    T2 blockage gate lam_block = (m_p/7.475e16)^(1/3):         {lam_block*1e15:.5f} fm  [transition_condition gate 1]")
print(f"    -> {r0_exact*1e15:.3f}, {re_cl2*1e15:.3f}, {lam_block*1e15:.3f} agree to +-0.12%; the bag one")
print(f"    (uniform-core profile) is the {r0_bag/re_cl2:.2f}x outlier - the profile shape matters at the 10% level.")
print()
print("(5) with the T2 gate as the electron's core datum (the previous alpha_knot script flagged")
print("    'r_e = 2.81794 fm [locked 2.818 fm]' - it treated them as the same locked number):")
ainv_block = lambar/lam_block
g_block = 16*math.pi**3/(3*ainv_block)
q_block = math.sqrt(4*math.pi*eps0*h*c0/(lamC/lam_block - 2))   # pure Coulomb + WvdM horizon
q_block_inf = math.sqrt(4*math.pi*eps0*h*c0*lam_block/lamC)     # no horizon term
q_block_bag = math.sqrt(8*math.pi*eps0*Ue/((7.0/6.0)/lam_block - 1/r_hor))
print(f"    lam_block/r_e = {lam_block/re_cl2:.7f}  ({100*(lam_block/re_cl2-1):+.4f}%)")
print(f"    alpha^-1 = lam_bar_C/lam_block = {ainv_block:.4f}   (observed 137.0360, dev {100*(ainv_block/(1/alpha)-1):+.4f}%)")
print(f"    g = 16 pi^3/(3 alpha) = {g_block:.6f}   (target 1.206740, dev {100*(g_block/g-1):+.4f}%)")
print(f"    q (Coulomb + horizon)  = {q_block/e:.5f} e ; q (no horizon) = {q_block_inf/e:.5f} e ;")
print(f"    q (bag profile) = {q_block_bag/e:.5f} e")
print(f"    -> with the Coulomb profile the charge comes out to 4-1200 ppm; with the bag profile")
print(f"    7.3% low. The profile shape inside the knot is the unpublished-eigenmode datum, so")
print(f"    'it comes out' only to the profile's precision - NOT closed. The T2 gate's exact")
print(f"    origin (7.475e16 kg/m^3) is NOT IN GIT (t2_equilibrium.py); if lam_block = r_e were")
print(f"    exact the chain would be circular. The last ~7 ppm is the one number left to derive.")
print()

# ---------------------------------------------------------------
print("="*92)
print("ROTATION SPEEDS AND THE WARMTH (Jaden's directive 2026-10-09:")
print("the ambient temperature is to be read off the rotation speeds)")
print("="*92)
kB = 1.380649e-23
omega = 2*me*c0*c0/hbar
print(f"circulation speed = c0 = {c0:.4e} m/s (the waves themselves)")
print(f"spin frequency omega = 2 m_e c0^2/hbar = 4 pi c0/lamC = {omega:.3e} s^-1 (zitterbewegung)")
print(f"warmth of the spin: hbar omega / kB = 2 m_e c0^2/kB = {hbar*omega/kB:.3e} K")
print(f"  (per m_e c0^2: the Compton temperature = {me*c0*c0/kB:.3e} K;")
print(f"   Euclidean-period convention hbar omega/(2 pi kB) = {hbar*omega/(2*math.pi*kB):.3e} K)")
print(f"kinetic warmth per kg of the circulation: c0^2/2 = {c0*c0/2:.3e} J/kg")
H_res = 32.371*c0*c0 - (c0*c0/3)*math.log((me*g/V_id)/rho0)   # residual at the squeezed density
print(f"knot heat-state residual (target-consistent): {H_res/c0/c0:.2f} c0^2/kg = {H_res:.3e} J/kg")
print(f"as a temperature with the pair mass m_w: T_H = H*m_w/kB =")
print(f"  m_w = m_p   : {H_res*mp/kB:.2e} K ;  m_w = m_p/3 : {H_res*mp/3/kB:.2e} K")
print(f"  vs T_rot = {hbar*omega/kB:.2e} K -> no match; the two warmth scales differ.")
print(f"  (PWC's T needs the heat capacity c_H - the repo's named open datum; the rotation")
print(f"  reading supplies the natural quantum mapping T = hbar omega/kB if Jaden rules it.)")
print()
print("c_H RULING (Jaden 2026-10-09, capture/2026-10-09_0703): 1 kg of medium reads 2.7 K ->")
cH = 32.371*c0*c0/2.7
print(f"  c_H = H0/2.7 K = {cH:.4e} J/(kg K) = {cH/(c0*c0):.3f} c0^2 per K  [his 1.0775e18 / 11.989]")
print(f"  frozen knot reads: 8.40 c0^2 / c_H = {8.40*c0*c0/cH:.2f} K  [his 0.70 K]  (2.7 K -> 0.70 K sink)")
print(f"  volumes: 1/rho0 = {1/rho0:.4e} m^3 ; 1/rho_max = {1/rho_max:.4e} m^3 ;")
print(f"  ratio = {1/rho0/(1/rho_max):.3e}  [his 1.49e41]")
print(f"  ambient heat density rho0 H0 = {rho0*32.371*c0*c0:.4e} J/m^3 ;")
print(f"  H0/(rho0 H0) = {32.371*c0*c0/(rho0*32.371*c0*c0):.4e} = 1/rho0  [his closed per-kg bookkeeping]")
print(f"  FLAG: 0.70 K is computed FROM the target-consistent 8.40 c0^2/kg (g still input);")
print(f"  the ruling closes the T-bridge, not yet the minimum-heat datum.")
print()

# ---------------------------------------------------------------
print("="*92)
print("ROUTE 3 -- THE HEAT-EXPELLED VOLUME AT THE FOLD")
print("="*92)
print("Jaden's reframing: frozen knot = same EM wave with the heat's VOLUME squeezed out.")
print("Needed: V_heat = V_id(1 - 1/g) =", f"{V_id*(1-1/g):.4e} m^3  (17.13% of V_id).")
print()
Qe = me*c0*c0   # tying heat of the electron: m c0^2 (CLAUDE.md: tying expels m c0^2)
Vheat_plateau = me/rho_max     # plateau reading: dv = 1/rho_max per kg (the fold-drop datum)
print(f"(a) plateau reading (dv = 1/rho_max per kg, the fold drop):")
print(f"    electron tying heat Q = m_e c0^2 = {Qe:.4e} J ; V_heat = m_e/rho_max = {Vheat_plateau:.4e} m^3")
print(f"    V_heat/V_id = {Vheat_plateau/V_id:.3e}  -- 10 orders too small. The plateau's volume per kg")
print(f"    is irrelevant at the electron's density (me/V_t = {me*g/V_id:.2e} kg/m^3 vs rho_max {rho_max:.1e}).")
print()
Vheat_gas = 3*me/(me*g/V_id)  # gas-branch reading: dQ = P dv with P = rho c0^2/3 => dv/dQ = 3/(rho c0^2), at rho = rho_e
print(f"(b) gas-branch reading at the knot's own state (dQ = P dv, P = rho c0^2/3):")
print(f"    dv/dQ = 3/(rho_e c0^2)  =>  V_heat = Q * 3/(rho_e c0^2) = 3 m_e/rho_e = 3 V_t")
print(f"    V_rest = V_t + 3 V_t = 4 V_t  =>  g = 4, not 1.2067. FAIL.")
print()
H0floor = 32.371*c0*c0
Vheat_rest = Qe/(rho0*H0floor)  # resting reading: heat's specific volume at rest = 1/(rho0 H0)
print(f"(c) resting-heat reading (heat's specific volume 1/(rho0 H0), H0 = 32.371 c0^2 floor):")
print(f"    V_heat = Q_e/(rho0 H0) = {Vheat_rest:.3e} m^3  -- {Vheat_rest/V_id:.1e} x the WHOLE knot volume: absurd.")
print()
print("(d) CAVITATION reading (Jaden: knot formation dumps heat = the cavitation;")
print("    capture/2026-10-09_0609_cavitation_heat_dump.md): the locked fold construction")
print("    P* dv = c0^2 (demand function) applied to the electron's own collapse, with the needed")
print("    dv = dV/m_e = 1.4066e-6 m^3/kg, FIXES the collapse pressure:")
P_cav = c0*c0/(V_id*(1-1/g)/me)
rho_cav = P_cav/(c0*c0)
uE = (me*c0*c0/2)/(V_id/g)
print(f"    P_cav = c0^2/dv = {P_cav:.4e} Pa = rho_cav c0^2, rho_cav = {rho_cav:.2e} kg/m^3")
print(f"    = {rho_cav/(me*g/V_id):.2f} x rho_e(knot) = {P_cav/uE:.2f} x u_E (the knot's field pressure).")
print(f"    That pressure is NOT in the locked ladder: the cavitation frame names the datum precisely --")
print(f"    the electron's collapse pressure (equivalently its dumped-heat fraction) is the one input")
print(f"    the locked set does not supply.")
print()
print("No locked reading of 'the heat's volume' produces 17.13%. The plateau datum (1/rho_max per kg)")
print("undershoots by 10 orders; the gas-branch law gives g = 4; the resting-heat reading is 10^29x too big.")
print("-> Route 3 fails: the heat-expelled volume ratio 1 - 1/g = 0.1713 has NO source in the locked set.")
print()

# ---------------------------------------------------------------
print("="*92)
print("NEAR-MISS TABLE (reported, not claimed -- no mechanism, none exact)")
print("="*92)
rows = [
 ("g^(1/3) vs sealed stretch 20/19", g**(1/3), 20/19),
 ("g vs 2 - 2^-1/3  (k-rule equal-core area deficit 1-2^-1/3)", g, 2-2**(-1/3)),
 ("g vs (33/31)^3", g, (33/31)**3),
 ("g^(1/2) vs ln 3", g**0.5, math.log(3)),
 ("1/(3g) vs (3/2) s kappa", 1/(3*g), 1.5*s*kappa),
 ("1 - g^-1/3 vs Y_coh/P_locked", 1-g**(-1/3), kappa*s/3),
 ("1 - g^-1/3 vs 2/(19 sqrt3)", 1-g**(-1/3), 2/(19*math.sqrt(3))),
 ("1 - g^-1/3 vs 1/16", 1-g**(-1/3), 1/16),
 ("g vs 1 + 2/(3pi)", g, 1+2/(3*math.pi)),
 ("g vs 4/3 (torus horizon r0=lam/2, degenerate tube)", g, 4/3),
]
for lab, a, b in rows:
    print(f"  {lab:52s} {a:.6f} vs {b:.6f}   dev {100*(a/b-1):+.3f}%")
print()
# tightest near-miss, checked precisely (reported, not claimed): the alpha^-1 gap itself
gap = 16*math.pi**3/3 - 1/alpha          # = 165.3668 - 137.0360
lnfold = math.log(rho_max/(2*rho0))
cand = lnfold*math.log10(2)
print(f"NEW: the alpha^-1 gap 16pi^3/3 - 137.036 = {gap:.5f}")
print(f"     ln(rho_max/2rho0)*log10(2) = ln({rho_max/(2*rho0):.4e})*log10(2) = {cand:.5f}")
print(f"     dev = {100*(cand/gap-1):+.5f}%  ({(cand-gap):+.4f} in alpha^-1)")
print(f"     CAVEAT: log10 is anthropic (no PWC structure counts in base 10), and the inputs")
print(f"     rho_max, rho0 carry 3-4 sig figs, so a ppm-level match cannot be exact by construction.")
print(f"     (7/8)*32.371 = {(7/8)*32.371:.5f}  dev {100*((7/8)*32.371/gap-1):+.3f}%  -- the nearest")
print(f"     ladder form, far looser than the log10 form. Both reported, neither claimed.")
print()
print("Best devs: 1/(3g) vs (3/2)s kappa +0.008%, g vs 2-2^-1/3 -0.036%, 2/(19 sqrt3) +0.003% (linear)")
print("-- all mechanism-free near-misses, per the framework's own rule (DERIVATION_BRIEF:188) reported not claimed.")

print()
print("="*92)
print("VERDICT")
print("="*92)
print("1. Eigenmode condition derived: lam V/R^4 = 8 pi^2/alpha = 10819.9 (idealized 128 pi^5/3 = 13056.8);")
print("   with R spin-locked at lam/4pi the whole 9% is ONE volume datum V_t/V_id = 1/g = 0.8287.")
print("2. Route 1 (4-quantum): R = 2lam/pi overproduces charge 7-41x in every volume reading;")
print("   R = lam/2pi overshoots 3.6x (horizon) or gives q' sqrt(pi^3/32) = 0.896e (proton-B analog, wrong")
print("   direction); the locked set contains no condition fixing V_t. FAIL.")
print("3. Route 2 (saturation, radial Coulomb profile, WvdM horizon): BI/E_S alpha^-1 = 8.3e4;")
print("   b(q) alpha^-1 = 2.1e6; PWC plateau functional alpha^-1 = 1665. All fail because the profile has")
print("   no fm core cutoff and every saturation functional only renormalizes the classical-radius circle:")
print("   q = e <=> core radius = (7/6) r_e = 3.29 fm (alpha in, alpha out). Lai's 135.9 works only through")
print("   HIS torus-tube cutoff from the geodesic constraint. The PWC set has no electron-scale length. FAIL.")
print("4. Route 3 (heat volume): plateau dv = 1/rho_max gives V_heat/V_id = 9.3e-11; the gas-branch law")
print("   gives g = 4; the resting-heat reading is 10^29x too large. No reading gives 0.1713. FAIL.")
print()
print("MISSING INPUT (named): an electron-scale knot datum -- the coupling-law heat-function's value at")
print("the electron's knot state (the locked set pins the grip only at rest [flat, g = 1] and at the")
print("plateau end [x7], and the electron's knot sits at ~1.5e5 kg/m^3, 9.6 decades of density below the")
print("fold, in the flat region), equivalently the exact two-loop harmonic eigenmode geometry (the")
print("unpublished Quicycle datum) or an independent electron-scale core length. Deriving g = 1.2067")
print("requires one of these; none is in the repo. The eigenmode condition lam V/R^4 = 8 pi^2/alpha is")
print("the precise form of the missing datum.")
