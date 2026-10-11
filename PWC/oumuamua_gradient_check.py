"""
PWC math-check: 'Oumuamua's non-gravitational acceleration vs the
Sun's held-medium pressure/tension gradient.

Hypothesis under test: the observed non-gravitational acceleration needs NO
outgassing -- it is the medium's pressure/tension gradient felt by the object
as it moves through the solar system's varying medium density.

LOCKED numbers, quoted before use (repo: PWC-Check/PWC):
  rho0 = 8.74e-27 kg/m^3
      CLAUDE.md: "rho_0 = 8.74e-27 kg/m^3 ~= 0.95 rho_crit (the medium is ~95% of mass)."
  c0 = 2.998e8 m/s
      CLAUDE.md: "c0 = 1/sqrt(mu0 eps0) is the medium's own speed"
  s = 1/19
      DERIVATIONS.md row 62: "The sealed stretch s = 1/19 IS the universal
      retained-heat fraction"
  Tension-heat law:  Y = s*rho*c0^2/3   ("on the gas branch")
      DERIVATIONS.md row 62 (the 720-degree pinch term s*rho*c0^2/3);
      PWC/derivations/demand_function_pressure_conversion.md line 251:
      "Tension-per-heat law: dY/d(Delta H) = -3Y/c0^2  ==>  Y = s rho c0^2/3
       on the gas branch (s = 1/19)"
  Caloric law:  H(rho) = H0 - (c0^2/3) ln(rho/rho0),  H0 = 32.371 c0^2
      README.md: "H(rho) = H0 - (c0^2/3)ln(rho/rho0)";
      session_logs/2026-10-08_2026-10-08_FULL_LEDGER.md line 76:
      "Caloric law: H(rho) = H0 - (c0^2/3)ln(rho/rho0); total drop 32.371 c0^2;
       H0 >= 32.371 c0^2."
  Solar held-medium compression (the exact locked form):
      DERIVATIONS.md row 23: "With the compression from the medium's own pull
      (c_s^2 = c0^2/3, d rho/rho = 3GM/(r c0^2)): dc/c = da/a = -GM/(r c0^2)"
      (task's light_bending rows 22/23; row 23 is the one carrying the profile)
  Push law (gradient force per unit mass):
      PWC/derivations/light_bending_push_pull.md line 8:
      "the pressure-gradient force per unit mass, (1/rho)*dP/dr, equals the pull g."
      and line 16: "the push is toward the mass"; DERIVATIONS.md row 14:
      "Push: the pressure-gradient force per unit mass equals the pull ... the
       photon, the same substance as the medium, feels it too."

OBSERVED (Micheli et al. 2018, Nature 559, 223-226): A1 = (4.92 +- 0.16)e-6 m/s^2
at r = 1 AU, best-fit radial dependence r^-2, directed AWAY from the Sun
(anti-solar; per arXiv:1904.02218 abstract: "a non-gravitational acceleration in
the anti-Solar direction").

Everything below is arithmetic on the locked numbers.  No repo files touched.
"""

import math

# ---- locked constants ----
RHO0   = 8.74e-27          # kg/m^3  (locked)
C0     = 2.998e8           # m/s     (locked)
S      = 1.0 / 19.0        #         (locked)
GM_SUN = 1.32712440018e20  # m^3/s^2, IAU standard GM_sun (standard value, not re-derived)
AU     = 1.495978707e11    # m       (standard value)

# observed non-gravitational acceleration (Micheli et al. 2018)
A_OBS  = 4.92e-6           # m/s^2 at 1 AU
A_OBS_ERR = 0.16e-6

def line(t):
    print("-" * 78)
    print(t)
    print("-" * 78)

line("(1) SOLAR HELD-MEDIUM DENSITY PROFILE  (locked form, row 23)")
# delta_rho/rho = 3GM/(r c0^2)
drr_1au = 3.0 * GM_SUN / (AU * C0**2)
print(f"delta_rho/rho (1 AU)   = 3*GM_sun/(r*c0^2) = {drr_1au:.4e}")
print(f"delta_rho/rho (0.255 AU perihelion) = {drr_1au/0.255:.4e}")
print(f"absolute delta_rho (1 AU) = rho0 * {drr_1au:.4e} = {RHO0*drr_1au:.4e} kg/m^3")
print(f"--> the Sun's compression changes the local medium density by ~3e-8 of rho0 at 1 AU.")

line("(2) PRESSURE/TENSION-GRADIENT FORCE PER UNIT MASS")
g_sun = GM_SUN / AU**2
print(f"g_sun = GM_sun/r^2 at 1 AU       = {g_sun:.4e} m/s^2")

# (a) framework's locked push law (row 14 / push-pull file line 8): push = pull
a_push = g_sun
print(f"(a) push law, (1/rho)dP/dr = g   : a_grad = {a_push:.4e} m/s^2  [toward the Sun]")

# (b) tension-heat law Y = s rho c0^2/3:  (1/rho) dY/dr = (s c0^2/3) d(ln rho)/dr
#     d(ln rho)/dr = -3GM/(c0^2 r^2)  from the row-23 profile
a_Y = S * g_sun
print(f"(b) tension-heat law Y=s rho c0^2/3: a_grad = s*g_sun = {a_Y:.4e} m/s^2  [toward the Sun]")
print(f"    (s = 1/19 = {S:.6f};  this is the framework's own 's-fraction' of the pull)")

# (c) volume (buoyancy-type) coupling on a low-density object: F = V*dY/dr,
#     a = (dY/dr)/rho_obj = s*(rho0/rho_obj)*g_sun
for robj in (1e-1, 1.0, 1e2):
    a_vol = S * (RHO0 / robj) * g_sun
    print(f"(c) volume route, rho_obj = {robj:6.1f} kg/m^3: a = s*(rho0/rho_obj)*g_sun = {a_vol:.3e} m/s^2")

# tension difference across a 230 m body (consistency of the volume route)
dYdr = S * RHO0 * g_sun
print(f"    |dY/dr| at 1 AU = s*rho0*g_sun = {dYdr:.3e} Pa/m; "
      f"across 230 m: {dYdr*230.0:.3e} Pa")

line("(3) COMPARISON WITH THE OBSERVED NON-GRAVITATIONAL ACCELERATION")
print(f"observed (Micheli et al. 2018):  {A_OBS:.3e} +- {A_OBS_ERR:.2e} m/s^2 at 1 AU, AWAY from the Sun")
print(f"                                 = {A_OBS/g_sun:.4e} of g_sun")
print()
print(f"(a) push law            : {a_push:9.3e} m/s^2  toward Sun   ratio = {a_push/A_OBS:8.1f}x   [too big, wrong sign]")
print(f"(b) tension-heat law    : {a_Y:9.3e} m/s^2  toward Sun   ratio = {a_Y/A_OBS:8.1f}x   [too big, wrong sign]")
for robj in (1e-1, 1e2):
    a_vol = S * (RHO0 / robj) * g_sun
    print(f"(c) volume, rho_obj={robj:6.1f}: {a_vol:9.3e} m/s^2              ratio = {a_vol/A_OBS:8.1e}x   [too small]")

line("(4) r-DEPENDENCE: PWC gradient vs observed")
print("PWC gradient:  d(ln rho)/dr = -3GM/(c0^2 r^2)  ==>  a_grad ~ r^-2  EXACTLY (pure r^-2)")
print("Observed best fit (Micheli 2018): n = -2   (r^-2-like; r^-1 and r^-3 also viable, worse)")
print("SHAPE: the r^-2 shape matches. SIGN: PWC gradient points toward the Sun; observed points")
print("away.  A sunward r^-2 extra force is degenerate with the GM_sun renormalization in the")
print("orbit fit and cannot produce an anti-sunward residual.")

line("(5) WHAT WOULD IT TAKE TO MATCH?")
# observed = 8.30e-4 of g_sun, anti-sunward.  volume route magnitude needs rho_obj:
rho_needed = S * RHO0 / (A_OBS / g_sun)
print(f"observed = {A_OBS/g_sun:.4e} of g_sun.  To get that magnitude by the volume route the")
print(f"object would need rho_obj = s*rho0/8.30e-4 = {rho_needed:.3e} kg/m^3  -- i.e. the object")
print("would have to BE the medium, not a 230 m, 1e-1..1e2 kg/m^3 body.  And the sign would")
print("still be wrong (observed anti-sunward, gradient sunward).")

line("VERDICT")
print("FAILS on magnitude (63x or 1205x too LARGE, sunward; or ~24 orders too SMALL on the")
print("volume route) and FAILS on direction (sunward vs observed anti-sunward).")
print("The only agreement is the r^-2 SHAPE, which radiation pressure also gives and which")
print("is not discriminating.  Per PWC methodology: near-miss (shape) reported, not claimed;")
print("the failure stays visible.")
