# PWC glitch check: pulsar glitches as hydrodynamic stall-and-recatch
# =====================================================================
# Hypothesis under test: the rotating rho_max core (the neutron body's shell)
# briefly re-locks with the medium when it hits a density variance, and the
# swept medium's angular momentum is transferred IN to the spin (glitches are
# spin-ups, dn/nu > 0).  Drag/catch law: F = 0.5*rho0*v^2 * f_solid * A_geo.
#
# Scratch-only test. Repo read-only. No git.
# Locked numbers (DERIVATIONS.md rows 5, 11, 15; task brief):
#   rho_max = 1.304e15, rho_core = 2.3e17, Y_bow = 5.93e26 Pa,
#   f_solid = 0.085%, rho0 = 8.74e-27, a_max = 3.23e11 N/kg
# Cap law: v_cap(rho) = sqrt(2Y/rho)  (row 15 / volume_mass_friction_rcp28.md)

import math

c0    = 2.99792458e8
G     = 6.67430e-11
Msun  = 1.98892e30
DAY   = 86400.0
YR    = 365.25 * DAY

rho_max   = 1.304e15
rho_core  = 2.3e17
Y_bow     = 5.93e26
f_solid   = 8.5e-4            # 0.085 %
rho_0     = 8.74e-27
a_max     = 3.23e11

def cap(rho):
    return math.sqrt(2.0 * Y_bow / rho)

V_RHOMAX  = cap(rho_max)
V_RHOCORE = cap(rho_core)
V_GAS     = c0 * math.sqrt(2.0 / (3.0 * 19.0))   # 0.187 c0 gas/electron branch

print("=" * 78)
print("0. CAPS FROM LOCKED NUMBERS   v_cap = sqrt(2*Y/rho)")
print("=" * 78)
print(f"  rho_max shell : {V_RHOMAX/1e3:9.1f} km/s  (locked 954)")
print(f"  rho_core      : {V_RHOCORE/1e3:9.1f} km/s  (locked 72)")
print(f"  gas branch    : {V_GAS/1e3:9.0f} km/s  = {V_GAS/c0:.4f} c0  (locked 56,156)")

def pulsar(name, M_msun, f_Hz, R_km):
    M = M_msun * Msun
    R = R_km * 1e3
    v = 2 * math.pi * R * f_Hz
    I = 0.4 * M * R * R
    return dict(name=name, M=M, R=R, f=f_Hz, v=v, I=I)

vela = pulsar("VELA", 1.4, 11.195, 11.0)
crab = pulsar("CRAB", 1.4, 29.947, 10.0)
msp  = pulsar("MSP (716 Hz, R=10 km)", 1.4, 716.0, 10.0)

print()
print("=" * 78)
print("1. SURFACE SPEED vs THE CAPS")
print("=" * 78)
for p in (vela, crab, msp):
    print(f"  {p['name']:24s} v_surf = 2*pi*R*f = {p['v']/1e3:9.0f} km/s")
    print(f"     vs rho_max cap {V_RHOMAX/1e3:.0f} km/s : {p['v']/V_RHOMAX:8.3f}x"
          + ("   --> ABOVE CAP (permanently stalled)" if p['v'] > V_RHOMAX else "   (below cap)"))
    print(f"     vs rho_core cap {V_RHOCORE/1e3:.0f} km/s: {p['v']/V_RHOCORE:8.3f}x"
          + ("   --> ABOVE CAP" if p['v'] > V_RHOCORE else ""))
    print(f"     vs gas-branch {V_GAS/1e3:.0f} km/s  : {p['v']/V_GAS:8.3f}x")
    # density the surface would have to be at for this speed to be the cap
    rho_at = 2.0 * Y_bow / p['v']**2
    print(f"     surface density needed for stall at this speed: {rho_at:.3e} = {rho_at/rho_max:.2f} x rho_max")

print()
print("  Vela R=10 km / 12 km band: "
      f"{2*math.pi*1e4*11.195/1e3:.0f} / {2*math.pi*1.2e4*11.195/1e3:.0f} km/s = "
      f"{2*math.pi*1e4*11.195/V_RHOMAX:.2f} / {2*math.pi*1.2e4*11.195/V_RHOMAX:.2f} of the 954 cap")

print()
print("=" * 78)
print("2. STALL TRIGGER: what density variance stalls Vela?")
print("=" * 78)
v = vela['v']
rho_stall = 2.0 * Y_bow / v**2
print(f"  cap(rho) = v_surf  ==>  rho = 2Y/v^2 = {rho_stall:.3e} kg/m^3")
print(f"  = {rho_stall/rho_max:.2f} x rho_max  ==>  the ambient/crust variance must")
print(f"  locally raise density by +{(rho_stall/rho_max - 1)*100:.0f}% to stall Vela.")
dv = (2e-6) * v
print(f"  A 2e-6 glitch changes v_surf by only {dv:.1f} m/s (cap margin is "
      f"{(V_RHOMAX - v)/1e3:.0f} km/s) - the spin-up itself never approaches the cap.")

print()
print("=" * 78)
print("3. RE-LOCK MOMENTUM TRANSFER: swept-medium catch  (drag law, f_solid = 0.085%)")
print("=" * 78)
print(f"{'psr':8s}{'A_geo':>12s}{'sweep T':>10s}{'m_swept kg':>13s}{'dL':>12s}{'dn/nu':>12s}{'vs obs':>10s}")

obs_vela = 2e-6
obs_crab = 1e-8
results = {}
for p, obs, Tlabel in ((vela, obs_vela, "100 d"), (crab, obs_crab, "100 d")):
    for Aname, A in (("4*pi*R^2", 4*math.pi*p['R']**2), ("pi*R^2", math.pi*p['R']**2)):
        for T in (100*DAY, 2.5*YR):
            m_sw = rho_0 * f_solid * A * p['v'] * T
            dL   = m_sw * p['v'] * p['R']
            dn   = dL / (2*math.pi * p['I'] * p['f'])
            tag  = f"{T/DAY:.0f} d" if T < YR else f"{T/YR:.1f} yr"
            print(f"{p['name'][:6]:8s}{Aname:>12s}{tag:>10s}{m_sw:13.3e}{dL:12.3e}{dn:12.3e}"
                  f"{obs/dn:10.1e}")
            if p['name'].startswith('VELA') and Aname == '4*pi*R^2' and T == 100*DAY:
                results['vela_100d'] = dn

print()
print("  ---- what the observed glitch DEMANDS ----")
for p, obs in ((vela, obs_vela), (crab, obs_crab)):
    m_req = obs * 2*math.pi * p['I'] * p['f'] / (p['v'] * p['R'])
    A = 4*math.pi*p['R']**2
    mdot = rho_0 * f_solid * A * p['v']
    t_req = m_req / mdot
    print(f"  {p['name'][:6]}: dn/nu = {obs:.1e} needs caught mass m = {m_req:.3e} kg "
          f"({m_req/Msun:.2e} Msun, {m_req/5.972e24:.2f} Earth masses)")
    print(f"         sweep time at the locked f_solid: {t_req/YR:.2e} yr"
          f"   (f_solid = 1: {t_req*f_solid/YR:.2e} yr)")
    # whole-lifetime supply, even catching 100% of the swept medium
    T_age = 1.13e4 * YR
    m_life = rho_0 * A * p['v'] * T_age
    dL_life = m_life * p['v'] * p['R']
    dn_life = dL_life / (2*math.pi * p['I'] * p['f'])
    print(f"         entire characteristic-age sweep, 100% catch: m = {m_life:.2f} kg "
          f"--> dn/nu = {dn_life:.2e}  (still {obs/dn_life:.1e}x short of {obs:.0e})")

print()
print("=" * 78)
print("4. TREND TEST (Vela vs Crab)")
print("=" * 78)
dn_v = results['vela_100d']
dn_c = crab_calc = None
m_sw_c = rho_0 * f_solid * 4*math.pi*crab['R']**2 * crab['v'] * 100*DAY
dn_c = m_sw_c * crab['v'] * crab['R'] / (2*math.pi * crab['I'] * crab['f'])
print(f"  predicted Crab/Vela glitch ratio = {dn_c/dn_v:.2f}  (model: dn/nu ~ nu)")
print(f"  observed  Crab/Vela ratio         = {obs_crab/obs_vela:.2e}")
print("  --> the model's trend is INVERTED vs observation by "
      f"{(dn_c/dn_v)/(obs_crab/obs_vela):.1e}x")

print()
print("=" * 78)
print("5. RECOVERY TIMESCALES vs observed days-months")
print("=" * 78)
r_edge = math.sqrt(G * vela['M'] / a_max)
print(f"  luminal response across the star : R/c0      = {vela['R']/c0*1e6:8.1f} us")
print(f"  luminal across the yield reach   : r_e/c0    = {r_edge/c0*1e6:8.1f} us  "
      f"(r_e = sqrt(GM/a_max) = {r_edge/1e3:.1f} km)")
T_drag = 0.5 * rho_0 * vela['v']**2 * f_solid * math.pi*vela['R']**2 * vela['R']
fdot_drag = T_drag / (2*math.pi * vela['I'])
fdot_obs  = 1.55e-11   # Vela observed spin-down rate, Hz/s
print(f"  framework drag torque            : {T_drag:.2e} N m  --> fdot = {fdot_drag:.2e} Hz/s")
print(f"  observed Vela fdot               : {fdot_obs:.2e} Hz/s   (drag is "
      f"{fdot_obs/fdot_drag:.1e}x too weak to even spin Vela down)")
t_relax = (obs_vela * vela['f']) / fdot_drag
print(f"  drag-only relaxation of one 2e-6 glitch: {t_relax/YR:.1e} yr")
print("  observed post-glitch recovery: days to months.")
print("  --> no locked framework number produces the observed recovery scale.")

print()
print("=" * 78)
print("6. SIGN CHECK (the locked framework says the medium does not move)")
print("=" * 78)
print("  The ambient medium is stationary (locked ruling). A shell re-catching")
print("  stationary medium absorbs its momentum, which in the rotating frame")
print("  points AGAINST the spin: the catch is a spin-DOWN of magnitude m*v*R,")
print("  not a spin-up.  For dn/nu > 0 the swept medium must already carry")
print("  specific angular momentum > v*R at the shell - no locked mechanism")
print("  gives the ambient any rotation.  Magnitude fails (sec. 3); sign also fails.")
