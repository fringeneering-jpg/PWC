# RBH-1 demand-function test (Jaden OK'd new tests 2026-10-08; run locally, nothing in git)
# Demand function (corrected form): m = dP * dV_init / c0^2,  converted fraction
#   f = dP/(rho_local*c0^2) ; full conversion when dV/c0 >= rho_mist/rho_max.
# Mist-limited regime: m = rho_mist * V_swept ; the demand rule supplies the threshold.
import math

c0 = 2.998e8
c0sq = c0**2
rho_max = 1.304e15
rho0 = 8.74e-27
Msun = 1.989e30
kpc = 3.0857e19
yr = 365.25*86400

# --- RBH-1 measured context (PREDICTIONS_FROZEN.md, RESULTS.md, PWC.md sec 8) ---
r_trail_kpc = 0.7        # published tail radius (FWHM 1.4-1.6 kpc -> r = 0.7-0.8)
v_bh = 954e3              # m/s
age = 73e6*yr             # 73 Myr (van Dokkum 2025)
flash_erg_s = 1.9e41      # [O III] apex flash
stars = 1e6*Msun          # 1e6-1e7 Msun of new stars (sec 8)

print("== Geometry and collapse rate (sealed: walls close at c0 each, gap at 2c0) ==")
for r_kpc in (0.7, 0.75, 0.8):
    A = math.pi*(r_kpc*kpc)**2
    Vdot = 2*A*c0
    mdot = stars/age
    rho_mist = mdot/Vdot
    print(f"r={r_kpc} kpc: A={A:.3e} m^2, Vdot={Vdot:.3e} m^3/s, "
          f"rho_mist={rho_mist:.3e} kg/m^3 = {rho_mist/rho0:.3f} rho0")

print("\n== Threshold check: full conversion needs dv >= c0*rho_mist/rho_max ==")
rho_mist = (stars/age)/(2*math.pi*(0.7*kpc)**2*c0)
dv_min = c0*rho_mist/rho_max
dP_req = rho_mist*c0sq
P_max = rho_max*c0sq
print(f"rho_mist (r=0.7) = {rho_mist:.3e} kg/m^3 = {rho_mist/rho0:.3f} rho0")
print(f"dv_min = {dv_min:.3e} m/s   (vs 954 km/s wall speed: margin {954e3/dv_min:.1e}x)")
print(f"dP_req = rho_mist*c0^2 = {dP_req:.3e} Pa;  sealed spike at dv=c0 is P_max = {P_max:.3e} Pa")
print(f"pressure margin = {P_max/dP_req:.1e}x")

print("\n== Heat budget: expelled vs the observed flash ==")
mdot = stars/age
heat_rate = mdot*c0sq
print(f"mdot_stars = {mdot:.3e} kg/s -> expelled heat rate = {heat_rate:.3e} W = {heat_rate/1e7:.3e} erg/s")
print(f"flash = {flash_erg_s:.2e} erg/s -> escape fraction = {flash_erg_s/(heat_rate*1e7):.3e}")
mdot_light = (flash_erg_s/1e7)/c0sq
print(f"flash light-equivalent: mdot_light = {mdot_light:.3e} kg/s = {mdot_light*age/Msun:.1f} Msun over 73 Myr (sec 8 says ~245)")
for M in (1e6, 1e7):
    print(f"  stars {M:.0e} Msun: escape fraction = {245/M:.3e}")

print("\n== Demand function vs the proton inventory (R_ball = 8 R_p) ==")
mp = 1.6726e-27
Rp = 0.8414e-15
dV_p = mp/rho_max                    # demand function: collapse volume per proton at P_max
R_ball = (3*dV_p/(4*math.pi))**(1/3)
print(f"dV = m_p/rho_max = {dV_p:.4e} m^3 -> R_ball = {R_ball:.4e} m = {R_ball/Rp:.3f} R_p (identity B says 8)")

print("\n== eps0/mu0 from the pairing: spacing and wave mass from hbar+rho0+c0 ==")
hbar = 1.05457e-34
eps0 = 8.854187817e-12
mu0 = 4*math.pi*1e-7
a0 = (hbar/(rho0*c0))**0.25
mw = rho0*a0**3/2
k_link = 1/(eps0*a0)
qw = math.sqrt(mw*a0/mu0)
e = 1.602176634e-19
print(f"a(rho0) = (hbar/(rho0 c0))^(1/4) = {a0:.4e} m = {a0*1e6:.1f} um")
print(f"m_w = rho0*a^3/2 = {mw:.3e} kg;  lambda_w = 2a = {2*a0*1e6:.1f} um ({c0/(2*a0)/1e12:.2f} THz)")
print(f"link stiffness k = 1/(eps0*a) = {k_link:.3e} N/m")
print(f"pair charge candidate q_w = sqrt(m_w*a/mu0) = {qw:.3e} C = {qw/e:.2f} e  (muddy - needs coupling form)")
print(f"scaling check: a(rho_max)=(hbar/(rho_max c0))^(1/4) = {(hbar/(rho_max*c0))**0.25:.3e} m = {(hbar/(rho_max*c0))**0.25/1e-15:.2f} fm")

print("\n== gamma tension-per-heat, third cut ==")
g_yield = 3.23e11
gamma_shell = 3.36e31
print(f"gamma/(rho_max*c0^2) = {gamma_shell/(rho_max*c0sq):.4f} m (a length; nothing clean)")
print(f"tension per heat-density-column: gamma/(rho_max*c0^2*R_shell) = g_yield/(2*c0sq) = {g_yield/(2*c0sq):.3e}  (restates gamma = P*R/2, no new link)")
