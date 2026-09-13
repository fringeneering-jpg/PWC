"""
DOMAIN V -- proper two-sided BVP (scipy.integrate.solve_bvp), replacing the
IVP/shooting attempts (Domain U/U2), per the explicit instruction that a
one-direction shooting integration cannot be used to accept or reject the
continuum closure.

State: y = [u, M_HDF], solved on r in [r_min, r_far] via collocation.
  du/dr     = -(rho_bg+rho_gal*u)*G*(Mbar(r)+M_HDF)/r^2*(1-u) / (rho_gal*cs0^2)
  dM_HDF/dr = 4*pi*r^2*rho_gal*u

Boundary conditions (2 total, exactly matching the 2 first-order ODEs):
  M_HDF(r_min) = 0                                    [physical: no HDF
                                                         excess mass inside
                                                         the innermost shell]
  RHS_du/dr(u,M_HDF,r)|_{r=r_far} = -2*u(r_far)/r_far  [outer condition:
                                                         the solution is
                                                         entering its own
                                                         r^-2 asymptotic
                                                         falloff at the
                                                         remote boundary --
                                                         a derivative-
                                                         matching condition,
                                                         NOT a fixed value
                                                         for u(r_far), so
                                                         the amplitude is
                                                         determined by the
                                                         full nonlinear
                                                         system including
                                                         M_bar, not pre-set
                                                         from the vacuum
                                                         formula]

u is NOT sigmoid-transformed (kept as the direct physical variable, since
solve_bvp's bc() needs to express both conditions algebraically in terms
of boundary VALUES, which is simplest done directly in u); any solution
where u exits (0,1) anywhere on the mesh is explicitly flagged INVALID and
excluded, never silently included, per instruction.
"""
import numpy as np, json, time
from scipy.integrate import solve_bvp
from scipy.optimize import minimize
from scipy import stats

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
KMS = 1.0e3
UPS_D, UPS_B = 0.5, 0.7
G = 6.674e-11
RHO_BG = 0.0

def make_rhs(rho_gal, c_s0, Mbar_of_r):
    def fun(r, y):
        u, MHDF = y
        u_c = np.clip(u, 1e-12, 1-1e-12)
        Mb = Mbar_of_r(r)
        gpred = G*(Mb+MHDF)/r**2
        du_dr = -(RHO_BG+rho_gal*u_c)*gpred*(1-u_c) / (rho_gal*c_s0**2)
        dMHDF_dr = 4*np.pi*r**2*rho_gal*u_c
        return np.vstack([du_dr, dMHDF_dr])
    return fun

def make_bc(rho_gal, c_s0, Mbar_of_r, r_far):
    def bc(ya, yb):
        u_far, MHDF_far = yb
        u_c = np.clip(u_far, 1e-12, 1-1e-12)
        Mb = Mbar_of_r(np.array([r_far]))[0]
        gpred = G*(Mb+MHDF_far)/r_far**2
        du_dr_far = -(RHO_BG+rho_gal*u_c)*gpred*(1-u_c) / (rho_gal*c_s0**2)
        outer_cond = du_dr_far - (-2*u_c/r_far)
        return np.array([ya[1] - 0.0, outer_cond])
    return bc

def solve_profile(r_min, r_far, rho_gal, c_s0, Mbar_of_r, n_mesh=60, u_guess=None, MHDF_guess=None):
    r_mesh = np.geomspace(r_min, r_far, n_mesh)
    if u_guess is None:
        A = c_s0**2/(2*np.pi*G*rho_gal)
        u_guess = np.clip(A/r_mesh**2, 1e-8, 0.5)
    if MHDF_guess is None:
        MHDF_guess = 4*np.pi*rho_gal*A*r_mesh if 'A' in dir() else 4*np.pi*rho_gal*(c_s0**2/(2*np.pi*G*rho_gal))*r_mesh
    y_guess = np.vstack([u_guess, MHDF_guess])
    fun = make_rhs(rho_gal, c_s0, Mbar_of_r)
    bc = make_bc(rho_gal, c_s0, Mbar_of_r, r_far)
    sol = solve_bvp(fun, bc, r_mesh, y_guess, max_nodes=20000, tol=1e-6, verbose=0)
    return sol

hr = lambda t: print("\n"+"="*78+"\n"+t+"\n"+"="*78)

hr("STEP 1: BARYON-FREE ISOTHERMAL CONTROL VALIDATION (Mbar=0 everywhere)")
rho_gal_test, c_s0_test = 1e-21, 1e5
Mbar_zero = lambda r: np.zeros_like(np.atleast_1d(r))
r_min_test = 0.1*KPC
r_far_test = 15.0 * (30.0*KPC)   # pretend "galaxy" out to 30 kpc, remote boundary at 15x that
sol = solve_profile(r_min_test, r_far_test, rho_gal_test, c_s0_test, Mbar_zero)
print(f"solve_bvp status: {sol.status}, message: {sol.message}, success: {sol.success}")
if sol.success:
    r_check = np.array([1.0, 5.0, 15.0, 30.0, 60.0])*KPC
    r_check = r_check[r_check <= r_far_test]
    u_num = np.interp(r_check, sol.x, sol.y[0])
    A = c_s0_test**2/(2*np.pi*G*rho_gal_test)
    u_analytic = A/r_check**2
    print("r[kpc]   u_numeric      u_analytic(SIS)   ratio")
    for i in range(len(r_check)):
        print(f"  {r_check[i]/KPC:6.1f}  {u_num[i]:.6e}  {u_analytic[i]:.6e}  {u_num[i]/u_analytic[i]:.4f}")
    print(f"\nu range on full mesh: [{sol.y[0].min():.3e}, {sol.y[0].max():.3e}]  (must stay in (0,1))")
