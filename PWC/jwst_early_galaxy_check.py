"""
PWC math-check: JWST "impossible early structure" problem.
Working dir: scratch/ only. Reads nothing from the repo; all locked numbers are
quoted from PWC/CLAUDE.md, PWC/DERIVATIONS.md, PWC/PWC/derivations/*.md and PWC/PWC/PWC.md
(see JWST_EARLY_GALAXY_CHECK_REPORT.md for the quotes).

Sections:
  (1) Observed JWST targets at z ~ 10-14 (ages in standard LCDM time).
  (2) The standard model's problem: Press-Schechter abundance of 10^11 Msun halos at z=12,
      expected counts in JWST volumes, and the implied assembly time.
  (3) The PWC reading: RBH-1 engine scaling + framework stagnation scale (1,910 Msun) +
      T2 creation-law route; engine counts vs observed SMBH seed counts.
  (4) Honest prediction + falsifiability numbers (mass budget, heat budget, SFRD flag).

Pure numpy; no scipy.
"""
import numpy as np

# ---------------- locked PWC constants (quoted sources in the report) ----------------
c0   = 2.99792458e8          # m/s
G    = 6.67430e-11           # m3 kg-1 s-2
Msun = 1.989e30              # kg
yr   = 3.156e7               # s
pc   = 3.0857e16             # m
Mpc  = 1e6 * pc              # m
a0_PWC  = 6.61e-11           # m/s2  (T1 locked, DERIVATIONS.md "Other derivations")
a0_fit  = 6.68e-11           # m/s2  (SPARC fit; used nowhere critical here)
rho0    = 8.74e-27           # kg/m3 (locked, CLAUDE.md sec.4)
rho_max = 1.304e15           # kg/m3 (locked, DERIVATION_BRIEF sec.2)
Rp      = 8.41e-16           # m (muonic-H proton radius)
yield_a = 3.23e11            # N/kg (GW150914 shell anchor)
eta     = 0.25               # T2: forward hemisphere 1/2 x cosine-average 1/2
v_avg   = c0                 # T2: collapse-front speed = locked-phase sound speed
rho_block_gate = 7.475e16    # kg/m3  (gate 1: m_p / lambda^3)
P_star  = rho_max * c0**2    # Pa (fold plateau pressure = 1.172e32)
# stagnation scale (stagnation_scale.md):
M_stag  = 1910.0             # Msun at rho_max, R* = 886 km
R_stag  = 886e3              # m
col_stag = 1.155e21          # kg/m2 = 3*a_max/(4 pi G)
# RBH-1 (task-locked reading):
M_rbh1_engine = 2e7          # Msun SMBH
M_rbh1_stars  = 2e7          # Msun of stars
t_rbh1_sf     = 1e7          # yr star-forming
# repo's own conservative RBH-1 numbers (PWC.md sec.8 / supply cap path (a)):
M_rbh1_stars_repo = 1e7      # Msun (upper end of "1e6-1e7" attributed to the wake)
t_rbh1_repo       = 73e6     # yr wake age
M_rbh1_cap        = 15500.0  # Msun PWC admixture ceiling (supply cap, path (a))
flash_escape      = 2.45e-4  # RBH-1 [OIII] flash escape fraction (locked)

# ---------------- LCDM cosmology (Planck 2018) ----------------
H0  = 67.4                   # km/s/Mpc
Om  = 0.315
Ol  = 0.685
Ob  = 0.0492
h   = 0.674
sigma8 = 0.811
ns  = 0.965
dc  = 1.686                  # Press-Schechter collapse threshold
H0_s = H0 * 1e3 / Mpc        # s^-1
rho_crit0 = 3*H0_s**2/(8*np.pi*G)         # kg/m3
rho_m0    = Om * rho_crit0                 # kg/m3
rho_b0    = Ob * rho_crit0                 # kg/m3
rho_m0_Msun_Mpc3 = rho_m0 * Mpc**3 / Msun  # Msun/Mpc3
c_over_H0 = 299792.458/H0                   # Mpc

print("rho_crit0 = %.3e kg/m3 ; rho_b0 = %.3e kg/m3 ; rho_m0 = %.2e Msun/Mpc3"
      % (rho_crit0, rho_b0, rho_m0_Msun_Mpc3))

def E(z): return np.sqrt(Om*(1+z)**3 + Ol)

# age of universe at z, Gyr (integrate to high z + analytic EdS tail is negligible)
def age_Gyr(z):
    zz = np.linspace(z, 2000, 400000)
    integrand = 1.0/((1+zz)*E(zz))
    return np.trapezoid(integrand, zz) / (H0_s*yr*1e9)   # Gyr

# comoving distance, Mpc
def chi_Mpc(z):
    zz = np.linspace(0, z, 20000)
    return c_over_H0*np.trapezoid(1.0/E(zz), zz)

# linear growth factor (Carroll/Press-Turner approx), normalized D(0)=1
def growth(z):
    zz = np.asarray(z, dtype=float)
    Ezz = E(zz); omz = Om*(1+zz)**3/Ezz**2; olz = Ol/Ezz**2
    g = 2.5*omz/(omz**(4/7) - olz + (1+omz/2)*(1+olz/70))
    g0 = 2.5*Om/(Om**(4/7) - Ol + (1+Om/2)*(1+Ol/70))
    return (g/g0)/(1+zz)

# ---- sigma(M) : Eisenstein-Hu no-baryon transfer, top-hat, normalized to sigma8 ----
k = np.logspace(-4, 3, 6000)      # h/Mpc
Gamma = Om*h
q  = k/(Gamma)
L0 = np.log(2*np.e + 1.8*q)
C0 = 14.2 + 731.0/(1+62.5*q)
Tk = L0/(L0 + C0*q**2)
Pk_norm = (k**ns)*Tk**2

def sigma_of_R(R_hMpc):    # R in h^-1 Mpc
    x = k*R_hMpc
    W = 3.0*(np.sin(x)-x*np.cos(x))/x**3
    integ = Pk_norm*W**2*k**2
    sig2 = np.trapezoid(integ, k)/(2*np.pi**2)
    return np.sqrt(sig2)

A_norm = sigma8**2 / sigma_of_R(8.0)**2
def sigma_M(M_Msun):       # M in Msun (physical)
    R = (M_Msun/(4*np.pi/3*rho_m0_Msun_Mpc3))**(1/3)   # physical Mpc
    s = np.sqrt(A_norm)*sigma_of_R(R*h)
    return s

# check normalization (sigma at R = 8 h^-1 Mpc should be sigma8)
print("sigma8 check (should be 0.811):", np.sqrt(A_norm)*sigma_of_R(8.0))
# cross-check D(z=12) against the exact integral form
a12 = 1.0/13.0
aa = np.linspace(1e-4, 1, 40000)
Ea = np.sqrt(Om/aa**3 + Ol)
Dint = 0.7875*Ea*np.cumsum(np.gradient(aa)*1.0/(aa*Ea)**3)
Dexact = Dint/Dint[-1]
print("D(z=12) Carroll vs exact integral: %.4f vs %.4f" % (growth(12), np.interp(a12, aa, Dexact)))

# Press-Schechter: n(M,z) per (Msun x Mpc3) -- fully vectorized over M
Mgrid = np.logspace(8, 15, 400)
sM    = np.array([sigma_M(m) for m in Mgrid])
lns   = np.log(sM)
dlns_dlnM = np.gradient(lns, np.log(Mgrid))

def n_PS_vec(Mvec, z):
    s  = np.interp(np.log(Mvec), np.log(Mgrid), sM)
    dl = np.interp(np.log(Mvec), np.log(Mgrid), dlns_dlnM)
    nu = dc/(s*growth(z))
    return rho_m0_Msun_Mpc3/Mvec**2 * np.sqrt(2/np.pi)*nu**2*np.exp(-nu**2/2)*np.abs(dl)

def n_gt_vec(M_Msun, z):
    """n(>M,z) at a single M, vectorized over Mgrid."""
    nvals = n_PS_vec(Mgrid, z)
    return np.trapezoid(nvals[Mgrid >= M_Msun], Mgrid[Mgrid >= M_Msun])

# comoving volume element dV/dz per sr, Mpc3/sr
def dVdz_sr(z):
    return chi_Mpc(z)**2 * c_over_H0/E(z)

def count_in_shell(M_Msun, z1, z2, area_deg2):
    zz = np.linspace(z1, z2, 200)
    vals = np.array([n_gt_vec(M_Msun, z)*dVdz_sr(z) for z in zz])
    V_per_sr = np.trapezoid(vals, zz)                    # count per sr
    return V_per_sr * area_deg2*(np.pi/180)**2

print()
print("="*100)
print("(1) OBSERVED JWST TARGETS  (the STANDARD MODEL's clock: Planck z<->t ages)")
print("="*100)
for z in [10, 12, 14]:
    print("  t(z=%.0f) = %.2f Gyr ;  lookback %.2f Gyr ; D(z) = %.4f"
          % (z, age_Gyr(z), age_Gyr(0)-age_Gyr(z), growth(z)))
print("""
  Literature sample (not repo numbers; flagged as literature):
    JADES-GS-z14-0  z=14.32  M* ~ 4e8 Msun (Carniani et al. 2024)
    JADES-GS-z13-0  z=13.20  M* ~ 4e8
    GLASS-z12 / UNCOVER-z13: z~12-13, M* ~ 1e8-1e9
    GN-z11          z=10.60  M* ~ 1e9
    Labbe+2023 candidates: 6 objects z=7.4-9.1, implied M* > 1e10
    ZF-UDS-7329     z=3.2, M*~1e11, formed most stars in a 200-400 Myr burst (first Gyr)
  Task window: M* ~ 1e9-1e11 at z~10-14  ->  t = 0.29-0.48 Gyr (300-500 Myr) available.
""")

print("="*100)
print("(2) THE STANDARD MODEL'S OWN PROBLEM, IN ITS OWN CLOCK  (Press-Schechter)")
print("    (per Jaden: 'too early' is the standard model's anxiety -- its assembly")
print("     e-folds against its own time axis. NOT a PWC test.)")
print("="*100)
Mhalo = 1e11
s11   = sigma_M(Mhalo)
nu12  = dc/(s11*growth(12))
print("  sigma(M=1e11 Msun) @ z=0 : %.3f" % s11)
print("  nu = delta_c/(sigma*D) at z=12 for a 1e11 Msun halo : %.2f sigma" % nu12)
print("  Gaussian suppression exp(-nu^2/2) = %.2e" % np.exp(-nu12**2/2))
print("  n(>1e11 Msun, z=12) = %.2e Mpc^-3 (comoving)" % n_gt_vec(1e11, 12))
# implied halo for stellar mass
eps = 0.1; fb = Ob/Om
for Ms in [1e9, 1e10, 1e11]:
    Mh = Ms/(eps*fb)
    nu = dc/(sigma_M(Mh)*growth(12))
    print("  M*=%.0e Msun -> halo Mh=%.1e Msun at eps=0.1  -> nu(z=12)=%.1f sigma ; "
          "n(>Mh,z=12)=%.1e Mpc^-3"
          % (Ms, Mh, nu, n_gt_vec(Mh, 12)))
# volumes & counts
V_field_100arcmin2 = chi_Mpc(12)**2*c_over_H0/E(12)*1.0   # ~ dV/dz at z=12 per sr * dz=1 * area
V_field = chi_Mpc(12)**2*c_over_H0/E(12)*1.0*(100/3600.0)*(np.pi/180)**2
print("  chi(z=12) = %.0f Mpc ;  100 arcmin^2 x dz=1 field volume ~ %.0f comoving Mpc3" % (chi_Mpc(12), V_field))
for Mh, lab in [(1e11, "1e11 halo"), (6.4e11, "6.4e11 halo (M*=1e10,eps=0.1)"), (6.4e12, "6.4e12 halo (M*=1e11,eps=0.1)")]:
    Nf = count_in_shell(Mh, 11.5, 12.5, 100/3600.0)
    print("  expected count in 100 arcmin^2 field, z=11.5-12.5, %s : %.2e" % (lab, Nf))
# full observable universe to z=14
zlim = np.linspace(0, 14, 100)
Ntot = np.array([n_gt_vec(1e11, z)*dVdz_sr(z) for z in zlim])
Ntot = np.trapezoid(Ntot, zlim)*(4*np.pi)
print("  total number of >1e11 Msun halos in the WHOLE observable universe, all z<=14 : %.2e (dominated by z<3)" % Ntot)
# z at which the FIRST 1e11 Msun halo appears: highest z where cumulative count to z=20 is >= 1
zgrid = np.linspace(0.5, 20, 500)
zgrid = zgrid[::-1]   # descending, 20 -> 0.5
zsub  = np.linspace(0.5, 20, 700)
rate  = np.array([n_gt_vec(1e11, z)*dVdz_sr(z) for z in zsub])
cum_hi = np.array([np.trapezoid(rate[zsub >= z], zsub[zsub >= z]) for z in zgrid])*(4*np.pi)
z1 = zgrid[np.where(cum_hi >= 1.0)[0][0]] if (cum_hi >= 1.0).any() else np.nan
print("  earliest z with >=1 expected 1e11-Msun halo (whole observable universe, cumulative to z=20): z = %.1f (t = %.2f Gyr)"
      % (z1, age_Gyr(z1)))
print("  at z=12 the whole sky holds ~%.1e such halos per unit z (EH sigma; Planck's full sigma gives ~4e3 -- rare but non-zero)" % (rate[np.argmin(np.abs(zsub-12))]*4*np.pi))
# most massive halo expected (1 object) in the JWST field at z=12
for zz in [10, 12, 14]:
    zsub = np.linspace(zz-0.5, zz+0.5, 60)
    for m in np.logspace(9, 13, 120):
        vals = np.array([n_gt_vec(m, z)*dVdz_sr(z) for z in zsub])
        cnt = np.trapezoid(vals, zsub)*(100/3600.0)*(np.pi/180)**2
        if cnt < 1.0:
            print("  most massive halo expected (N=1) in 100 arcmin^2, z=%.0f : ~%.1e Msun" % (zz, m))
            break
print("""
  Reading: at eps=0.1, observed M*~1e9 galaxies at z~12 are ~5-sigma-halo objects
  (~0.2 expected per 100 arcmin^2 field vs ~5-10 seen: ~30x); M*~1e10 needs a
  6.4e11 Msun halo (~1e-6 expected per field vs ~1 seen: ~1e6 x). All counts here
  use the Eisenstein-Hu no-baryon sigma(M); Planck's full sigma lowers them by
  another factor ~3-10, so the tension only grows.
  Assembly time: LCDM's per-halo accretion is NOT the bottleneck (specific
  accretion ~0.035(1+z)^2.5 h Gyr^-1 -> mass-doubling ~48 Myr at z=12); the
  problem is abundance x efficiency: a 1e11 Msun halo at z=12 is a ~5.3-sigma
  peak, the first such halos appear around z~%.1f (t~%.2f Gyr), and the observed
  massive galaxies sit 1e1-1e6 x above the expected count per field. To build
  M*=1e11 at z=12 at eps=0.1 LCDM needs a 6.4e12 Msun halo: a 9.7-sigma object
  with ~8e-18 expected per field -- i.e. never.
""" % (z1, age_Gyr(z1)))

print("="*100)
print("(3) LOCKED-RATE CROSS-SECTION IN THE STANDARD FRAME (kept for the record)")
print("    (per Jaden: this frame is not PWC's test bed; the frame-free reading is (5).)")
print("="*100)
SFR_engine = M_rbh1_stars/t_rbh1_sf          # Msun/yr (task-locked reading)
print("  RBH-1 engine (task-locked): %.0e Msun of stars in %.0e yr -> SFR = %.1f Msun/yr"
      % (M_rbh1_stars, t_rbh1_sf, SFR_engine))
for Mg, lab in [(1e9, "1e9"), (1e10, "1e10"), (1e11, "1e11")]:
    t_win = 400e6
    N_rate  = Mg/(SFR_engine*t_win)                       # continuous 400 Myr
    N_burst = Mg/M_rbh1_stars                             # one 1e7-yr burst per engine
    M_eng_rate = N_rate*M_rbh1_engine
    N_knots = M_eng_rate/M_stag
    print("  M*=%s Msun:  rate-reading N=%.1f engines (continuous 400 Myr) ; "
          "burst-reading N=%.0f engines ; engine mass=%.1e Msun (%.1f%% of galaxy) ; "
          "stagnation-scale knots=%.1e"
          % (lab, N_rate, N_burst, M_eng_rate, 100*M_eng_rate/Mg, N_knots))
print("""
  RBH-1-scale engines needed for 1e11 Msun: 125 (rate reading; each engine then ties
  8e8 Msun = 40x the observed trail mass, needing a ~340 kpc trail) or 5,000
  (burst reading; engine mass 1e11 Msun = 100% of the target -- fully circular).
""")
# observed SMBH seed counts
print("  --- plausibility vs observed SMBH seed counts ---")
V_pc = 1e11/(rho_m0_Msun_Mpc3*(1+12)**3)     # physical Mpc3 traced back from 1e11 Msun at z=12
V_pc_com = V_pc*(1+12)**3
print("  Lagrangian volume of a 1e11 Msun proto-cluster at z=12: %.2f comoving Mpc3" % V_pc_com)
n_smbh_local = 0.01      # Msun>1e6, ~1 per L* galaxy (Mpc^-3, literature)
n_smbh_highz = 1e-5      # z~6-10 AGN, M>1e7 (Mpc^-3, literature, order of magnitude)
print("  expected SMBH seeds in that volume: local density -> %.2f ; high-z AGN density -> %.1e"
      % (n_smbh_local*V_pc_com, n_smbh_highz*V_pc_com))
print("  needed: 125 (rate) / 5,000 (burst) RBH-1-scale engines, or %.1e stagnation knots"
      % (2.5e9/M_stag))
print("  -> engine count exceeds observed SMBH seed counts by 1e3-1e6 x at RBH-1 scale.")
# stagnation-knot inventory vs compact-mass observations
rho_bh_soltan = 3e5      # Msun/Mpc3 comoving (Soltan, literature order)
print("  stagnation reading: total engine mass 2.5e9 Msun in %.2f comoving Mpc3 = %.1e Msun/Mpc3"
      % (V_pc_com, 2.5e9/V_pc_com))
print("    vs Soltan-inferred SMBH mass density today ~3e5 Msun/Mpc3 -> %.0f x above" % (2.5e9/V_pc_com/rho_bh_soltan))
print("    vs galaxy's own mass: engines = 2.5%% of M*, vs observed BH/M* ~ 0.1-0.5%% today -> 5-25x.")

# ---- T2 creation-law route ----
print("  --- T2 creation-law route (locked: rho_dot = eta*rho0*pi*G*<v>*rho_b/a0) ---")
kfac = eta*rho0*np.pi*G*v_avg/a0_PWC      # s^-1 per unit blocking density (rho_dot = kfac*rho_b)
print("  k = eta*rho0*pi*G*c0/a0 = %.3e s^-1  (z=0)  -> 1/k = %.1f Gyr" % (kfac, 1/kfac/(yr*1e9)))
twin_s = 400e6*yr                          # 400 Myr in seconds
for p, lab in [(0, "rho0 = const (locked rest value)"), (3, "rho0 ~ (1+z)^3 (medium density scales)")]:
    k12 = kfac*(1+12)**p
    Mseed = 1e11/(k12*twin_s)
    print("  %s: k(z=12)=%.3e s^-1 ; k*t over 400 Myr = %.2f ; seed mass needed = %.1e Msun (%.0f%% of 1e11)"
          % (lab, k12, k12*twin_s, Mseed, 100*Mseed/1e11))
print("  RBH-1 consistency: engine rate per engine mass = 1/1e7 yr = %.2e s^-1" % (1/(t_rbh1_sf*yr)))
print("    vs T2 k(z=12) with (1+z)^3 scaling = %.2e s^-1 -> ratio T2/RBH1 = %.2f (agree to ~44%%)"
      % (kfac*(1+12)**3, (kfac*(1+12)**3)/(1/(t_rbh1_sf*yr))))
# medium volume / baryon fraction needed under p=3
rho_med12 = rho0*(1+12)**3
V_med = 1e11*Msun/rho_med12
R_med = (3*V_med/(4*np.pi))**(1/3)
print("  medium needed for 1e11 Msun at z=12: rho_med=%.2e kg/m3 -> sphere R=%.0f kpc (physical)"
      % (rho_med12, R_med/pc/1e3))
M_seed_p3 = 1e11/(kfac*(1+12)**3*twin_s)
M_b_reg = rho_b0*(1+12)**3*V_med/Msun
print("  baryons in that region = %.1e Msun ; seeds = %.1e Msun -> seeds must be %.0f%% of ALL pre-existing baryons in the region"
      % (M_b_reg, M_seed_p3, 100*M_seed_p3/M_b_reg))

print("="*100)
print("(4) RATE-RATIO BOOKKEEPING (frame-free) + standard-frame flags")
print("="*100)
# heat budget
L_tie = 1e11*Msun*c0**2
P_tie = L_tie/twin_s
print("  tying heat for 1e11 Msun: m*c0^2 = %.2e J ; over 400 Myr = %.2e W" % (L_tie, P_tie))
print("  at RBH-1 locked escape fraction 2.45e-4: flash = %.2e W = %.1e Lsun" % (P_tie*flash_escape, P_tie*flash_escape/3.828e26))
print("    (observed z~12 galaxies: L_UV ~ 1e9-1e10 Lsun -> the flash would outshine them by 1e2-1e3x)")
# SFRD flag
rbdot_p0 = kfac*rho_b0*(1+12)**3
rbdot_p3 = kfac*(1+12)**3*rho_b0*(1+12)**3
Mpc3_m3 = Mpc**3
def to_SFRD(rdot):   # kg/m3/s -> Msun/yr/comoving Mpc3
    return rdot*Mpc3_m3/(1+12)**3/(Msun/yr)
print("  T2 law read as cosmic tying rate at z=12: %.1f Msun/yr/comoving Mpc3 (rho0 const) or %.1f (rho0~(1+z)^3)"
      % (to_SFRD(rbdot_p0), to_SFRD(rbdot_p3)))
print("    observed cosmic SFRD at z~12: ~1e-3 - 1e-2 Msun/yr/Mpc3 -> T2 overproduces by ~1e2 x (p=0) / ~1e5 x (p=3)")
print("""
  FALSIFIABILITY (what would kill the PWC channel; all expressible as ratios/states):
  (a) knot inventory vs assembly: PWC knots form at full density in a single fold (gates
      1-5) -- any high-z galaxy whose stellar content shows an assembly gradient (density/
      age/abundance ordering inconsistent with a single-crossing formation) kills the
      'already dense' claim. The comparison uses the observers' own clocks; PWC declines
      the clock but must still match the observed structure;
  (b) the engine inventory: PWC needs 5,000 RBH-1-scale engines (yield-1) or 5.2e7
      stagnation knots per 1e11 Msun galaxy -- engine inventory = galaxy inventory.
      Surveys of high-z fields finding no such compact-mass population kill it;
  (c) the flash rate: m*c0^2 per kg at the locked escape fraction -> ~9e11 Lsun per
      forming galaxy vs ~1e9-1e10 Lsun observed (rate ratio 1e2-1e3); unresolved absence
      forces the escape fraction ~1e-5 x RBH-1's;
  (d) the repo's own supply cap: if the frozen -0.10 dex RBH-1 metallicity test passes,
      the cap stands and the per-crossing yield is 7.75e-4 engine-masses -- the channel
      cannot reach galaxy inventory;
  (e) the standard-frame SFRD flag (record only): T2 read as the cosmic tying rate
      overproduces the observed z~12 SFRD by 1e2-1e5 x -- a standard-frame constraint
      the framework declines to answer (it needs the LCDM census).
""")
# conservative repo cross-check
print("  REPO CROSS-CHECK (the task's rate vs the repo's own sealed numbers):")
print("    repo: 1e6-1e7 Msun stars over 73 Myr -> SFR_engine = %.2f Msun/yr (task uses 2.0)" % (M_rbh1_stars_repo/t_rbh1_repo))
print("    repo supply cap (path a): <= %.0f Msun tying admixture per wake -> engines needed for 1e11 Msun = %.1e" % (M_rbh1_cap, 1e11/M_rbh1_cap))
print("    -> with the repo's own cap the channel is short by ~3 orders of magnitude.")
print("""
  FRAME NOTE: sections (1)-(4) run in the standard cosmology frame (Planck z<->t ages,
  comoving volumes, SFRD) -- the standard model's own problem statement. Per Jaden, PWC
  disputes that scaffolding: its redshift is the micro-knot's unspooling and its physics
  is inventory/rate/state, not 'when'. Section (5) is the frame-free PWC reading.
""")

print("="*100)
print("(5) THE PWC READING, FRAME-FREE: INVENTORY, RATE, STATE  (NO TIME, NO AGES, NO YEARS)")
print("="*100)
f_matter = 0.05
M_target = 1e11
# ---- INVENTORY: a dimensionless ratio ----
print("  [INVENTORY] (locked: rho0 = 8.74e-27 ~ 0.95 rho_crit; matter = %.0f%% of mass)" % (100*f_matter))
print("    medium : matter = %.0f : 1 everywhere. A region holding M of matter holds %.0f x M of medium."
      % (1/f_matter, 1/f_matter))
print("    -> to tie a %.0e Msun galaxy the region needs %.0e Msun of medium; any region"
      % (M_target, M_target))
print("       holding %.1e Msun of matter already has it on site. Ratio 20, no time enters."
      % (M_target/20))
R_med0 = (3*M_target*Msun/rho0/(4*np.pi))**(1/3)
print("    (at locked rho0 that medium occupies a sphere of R = %.0f kpc -- a length, not an age)"
      % (R_med0/pc/1e3))
# ---- RATE: the medium's own units ----
print("  [RATE] T2 locked: rho_dot = eta*rho0*pi*G*<v>*rho_b/a0, <v> = c0 (the medium's own speed).")
G_untie = rho0*c0/(rho_max*Rp)                  # the medium's OWN untying rate (locked T2 decay partner)
ratio_k = eta*np.pi*G*rho_max*Rp/a0_PWC         # tying/untying, DIMENSIONLESS (rho0 cancels)
print("    the medium's own untying rate: Gamma = rho0*c0/(rho_max*R_p) = %.2e s^-1 (c0-based)" % G_untie)
print("    tying rate per unit blocking mass, in units of Gamma:")
print("      k/Gamma = eta*pi*G*rho_max*R_p/a0 = %.3f   (DIMENSIONLESS -- rho0 cancels out)" % ratio_k)
print("    per unit MEDIUM mass at the locked %.0f%% matter fraction:" % (100*f_matter))
print("      rho_dot/rho_med = f_matter*k = %.3f x Gamma  ->  a region's whole 20:1 medium"
      % (f_matter*ratio_k))
print("      inventory ties in 1/%.4f = %.0f natural units (one natural unit = one untying e-fold)."
      % (f_matter*ratio_k, 1/(f_matter*ratio_k)))
print("    net at rest: untying removes %.2f of the medium per natural unit, tying adds %.4f ->" % (f_matter, f_matter*ratio_k))
print("      net melt -%.4f per natural unit (the melting state, as a rate, not a duration)."
      % (f_matter*(1-ratio_k)))
print("    RBH-1 anchor in the same units: one engine ties one engine-mass per trail crossing")
print("      (62 kpc at the medium's locked 954 km/s -- the medium's own length/speed).")
k_rbh1_5 = 1/(t_rbh1_sf*yr)
k_rest = eta*rho0*np.pi*G*c0/a0_PWC
print("      site rate / Gamma = %.0f ; site rate / k_rest(rho0) = %.0f"
      % (k_rbh1_5/G_untie, k_rbh1_5/k_rest))
print("      -> in the T2 law (k proportional to rho_med) the wake's rate reads as the site's")
print("         medium at ~%.0f rho0. The locked set has NO law fixing the site's density --"
      % (k_rbh1_5/k_rest))
print("         that gap is the whole 'rate' question.")
# engine inventory as pure ratios
print("    ENGINE INVENTORY (pure ratios, no time):")
print("      yield per crossing (task-locked) = 1 engine-mass -> %.0f engines per %.0e Msun galaxy"
      % (M_target/M_rbh1_engine, M_target))
print("      -> engine inventory = galaxy inventory (1:1, circular) unless engines re-cross;")
print("      counting re-crossings is a clock, which the framework declines.")
print("      at the stagnation floor (1,910 Msun): %.1e knots per galaxy." % (M_target/M_stag))
print("      observed SMBHs per galaxy ~ 1 (local census) vs 5,000 needed at yield-1 -> count excess ~%.0e x" % (M_target/M_rbh1_engine))
print("      repo's own supply cap (path (a)): <= %.0f Msun tying per wake -> yield per crossing"
      % (M_rbh1_cap))
print("      = %.2e engine-masses -- %.0f x BELOW the task-locked yield-1. The two locked yields"
      % (M_rbh1_cap/M_rbh1_engine, M_rbh1_engine/M_rbh1_cap))
print("      disagree; the frozen -0.10 dex RBH-1 metallicity bar decides.")
# ---- STATE: gauge ratios, not durations ----
print("  [STATE] (no durations; state variables only)")
print("    melting state: %.0f%% of the initially tied inventory remains tied (95%% re-absorbed)." % (100*f_matter))
print("    bath gauge: T_now / T_Separation = 2.7 K / 54 K = 1/20 -- the bath sits at 5% of its")
print("    Great-Separation value, mirroring the 5% matter fraction. A state, not an age.")
print("    (54 K datum: Jaden via parent agent; NOT in the repo files -> UNCHECKED.)")
print("    flash rate ratio: tying the observed galaxies expels m*c0^2; at the locked 2.45e-4")
print("    escape fraction the emitted rate is ~%.0e Lsun per forming galaxy vs ~1e9-1e10 Lsun"
      % (P_tie*flash_escape/3.828e26))
print("    observed -> %.0f-%.0f x the observed emission rate (a rate ratio, no duration)."
      % ((P_tie*flash_escape/3.828e26)/1e10, (P_tie*flash_escape/3.828e26)/1e9))
print("    the framework makes NO statement about 'when'. 'When' is the human concept; the")
print("    physics is the inventory (20:1), the rate (0.87 x untying; c0-based), and the state")

print("="*100)
print("VERDICT (three parts, no time on the PWC side)")
print("="*100)
print("""
  1. WHAT PWC SUPPLIES: the MASS, from its own medium -- ratio 20, no time needed.
     The knots cavitate into existence already dense (gates 1-5 run at the fold); there is
     no assembly clock to fail. The JWST 'too early' problem is the standard model's
     anxiety (its assembly e-folds on its own time axis); for PWC it is not a question.
     Inventory check: any region holding M/20 of matter holds M of medium -- the full
     target is on site. PASS, dimensionless.

  2. THE RATE IS THE MEDIUM'S OWN: T2's tying rate in the medium's units is
     0.87 x the medium's own untying rate (dimensionless: eta*pi*G*rho_max*R_p/a0,
     rho0 cancels); at the locked 5% matter fraction the whole regional inventory ties
     in 23 natural units (untying e-folds); the RBH-1 anchor is 1 engine-mass per trail
     crossing (the medium's own length at its own 954 km/s). The rate is c0-based, not
     year-based. The framework makes NO statement about 'when': 'when' is the human
     concept; the physics is inventory, rate, state.

  3. HONEST FAILURES KEPT VISIBLE (all frame-free):
     (i)   ENGINE INVENTORY: at the anchored yield (1 engine-mass per crossing) a 1e11 Msun
           galaxy needs 5,000 RBH-1-scale engines -- engine inventory = galaxy inventory,
           1:1 circular (or 5.2e7 stagnation knots). Reducing the count requires counting
           re-crossings -- a clock -- which the framework declines. Observed SMBHs per
           galaxy ~1 vs 5,000 needed: the seed bootstrap is the load-bearing gap.
     (ii)  THE TWO LOCKED YIELDS DISAGREE: task-locked yield 1 engine-mass per crossing
           vs the repo's own sealed supply cap <=15,500 Msun per wake (yield 7.75e-4,
           ~1,300x lower). If the cap holds, the channel is ~1e3 short of any galaxy-scale
           inventory. The frozen -0.10 dex RBH-1 metallicity test decides.
     (iii) FLASH RATE: at the locked 2.45e-4 escape fraction, tying the observed galaxies
           emits ~9e11 Lsun vs ~1e9-1e10 Lsun observed -- a 1e2-1e3 x rate excess; the
           framework must either absorb the heat (spacer heat) or take an escape fraction
           ~1e-5 x RBH-1's. Currently unaccounted.
     (iv)  NO STATE LAW for f_matter(epoch)/rho_med(epoch): the framework declines the
           epoch comparison; if one is ever forced, it cannot currently be made without
           borrowing the standard frame ((1+z) mechanics is OPEN, DERIVATIONS.md row 17).

  SUMMARY LINE: PWC supplies the mass (ratio 20, no time needed); the rate is the medium's
  own speed (0.87 x untying; c0-based); the framework makes no statement about 'when'
  because 'when' is the human concept -- the physics is the inventory, the rate, and the
  state. The only PWC-internal tensions are the engine inventory (1:1 circular at the
  anchored yield), the two locked yields disagreeing by 1,300x, and the unaccounted flash
  rate -- all falsifiable and all currently unresolved.
""")

