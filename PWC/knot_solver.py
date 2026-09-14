"""
PWC compact-knot dimensionless existence/stability/scaling audit.
Conserved-inventory phase-field solver, spherically symmetric, step 1 only.

State vector y = [phi, phi', n, n', Q], unknown parameter p = [mu].
Q tracks the running excess-inventory integral so the N_exc=N_target
constraint becomes a normal boundary condition instead of an outer loop.

ODEs (from the given Euler-Lagrange equations):
  phi'' = [V'(phi) - B*dn*(n - n0 - dn*phi)]/K - (2/r)*phi'
  n''   = [B*(n - n0 - dn*phi) - mu]/C - (2/r)*n'
  Q'    = 4*pi*r^2*(n - n0)

Boundary conditions (6, for 5 states + 1 parameter):
  phi'(r_min) = 0
  n'(r_min)   = 0
  Q(r_min)    = 0
  phi(R_box)  = 0
  n(R_box)    = n0
  Q(R_box)    = N_target
"""
import numpy as np
from scipy.integrate import solve_bvp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json, os, time

OUTDIR = r"C:\Users\jaden\cosmology\PWC\knot_audit"
os.makedirs(OUTDIR, exist_ok=True)

# dimensionless parameters, exactly as specified -- not fitted
n0 = 1.0
dn = 1.0
K = 1.0
B = 10.0
C = 0.1
Lam = 1.0

def Vprime(phi):
    # V(phi) = Lam*phi^2*(1-phi)^2
    # V'(phi) = 2*Lam*phi*(1-phi)*(1-2*phi)
    return 2*Lam*phi*(1-phi)*(1-2*phi)

def make_ode(r_min):
    def ode(r, y, p):
        mu = p[0]
        phi, dphi, n, dn_, Q = y
        r_safe = np.maximum(r, r_min)
        ddphi = (Vprime(phi) - B*dn*(n - n0 - dn*phi))/K - (2.0/r_safe)*dphi
        ddn   = (B*(n - n0 - dn*phi) - mu)/C - (2.0/r_safe)*dn_
        dQ    = 4*np.pi*r_safe**2*(n - n0)
        return np.vstack([dphi, ddphi, dn_, ddn, dQ])
    return ode

def make_bc(N_target, n0):
    def bc(ya, yb, p):
        # ya = values at r_min, yb = values at R_box
        return np.array([
            ya[1],            # phi'(r_min) = 0
            ya[3],             # n'(r_min) = 0
            ya[4],             # Q(r_min) = 0
            yb[0],             # phi(R_box) = 0
            yb[2] - n0,        # n(R_box) = n0
            yb[4] - N_target,  # Q(R_box) = N_target
        ])
    return bc

def initial_guess(r, N_target, R_guess_knot):
    # localized bump for phi, matching excess-inventory bump for n
    phi0 = 1.0/(1.0+np.exp((r-R_guess_knot)/max(R_guess_knot*0.15,0.05)))
    n_ = n0 + dn*phi0
    dphi0 = np.gradient(phi0, r)
    dn0 = np.gradient(n_, r)
    # crude running integral for Q
    integrand = 4*np.pi*r**2*(n_-n0)
    Q0 = np.concatenate([[0], np.cumsum(0.5*(integrand[1:]+integrand[:-1])*np.diff(r))])
    return np.vstack([phi0, dphi0, n_, dn0, Q0])

def solve_knot(N_target, R_box, n_points, R_guess_knot=None, r_min=1e-4, verbose=True):
    if R_guess_knot is None:
        R_guess_knot = max(0.5, N_target**(1/3))  # rough volumetric guess, just for initial mesh
    r = np.linspace(r_min, R_box, n_points)
    y_guess = initial_guess(r, N_target, R_guess_knot)
    mu_guess = np.array([B*dn*0.5])  # rough guess

    ode = make_ode(r_min)
    bc = make_bc(N_target, n0)

    sol = solve_bvp(ode, bc, r, y_guess, p=mu_guess, max_nodes=200000, tol=1e-8, verbose=0)
    if verbose:
        print(f"  N_target={N_target}: status={sol.status}, message={sol.message}, mu={sol.p[0]:.6f}, max_res={np.max(sol.rms_residuals):.3e}")
    return sol, r

if __name__ == "__main__":
    print("=== SINGLE-CASE TEST: N_target=1.0 ===")
    t0 = time.time()
    sol, r = solve_knot(N_target=1.0, R_box=20.0, n_points=2000, R_guess_knot=1.2)
    print(f"wall time: {time.time()-t0:.1f}s")

    if sol.status != 0:
        print("SOLVER DID NOT CONVERGE -- stopping here, no further steps until this is fixed")
    else:
        r_fine = np.linspace(sol.x[0], sol.x[-1], 4000)
        y_fine = sol.sol(r_fine)
        phi, n_ = y_fine[0], y_fine[2]
        print(f"phi(0)={phi[0]:.4f}, n(0)={n_[0]:.4f}, phi(R_box)={phi[-1]:.4e}, n(R_box)={n_[-1]:.4f}")
        print(f"mu = {sol.p[0]:.6f}")
        # find R_knot where phi=0.5
        idx = np.where(phi <= 0.5)[0]
        if len(idx) > 0:
            i = idx[0]
            if i > 0:
                r_knot = np.interp(0.5, [phi[i], phi[i-1]], [r_fine[i], r_fine[i-1]])
            else:
                r_knot = r_fine[0]
            print(f"R_knot (phi=0.5) = {r_knot:.4f}")
        else:
            print("phi never drops to 0.5 within domain -- profile too broad or R_box too small")

        fig, axes = plt.subplots(1,2, figsize=(11,4.5))
        axes[0].plot(r_fine, phi, label='phi(r)')
        axes[0].axhline(0.5, ls=':', color='gray')
        axes[0].set_xlabel('r'); axes[0].set_title('phase field phi'); axes[0].legend()
        axes[1].plot(r_fine, n_, label='n(r)', color='orange')
        axes[1].axhline(n0, ls=':', color='gray')
        axes[1].set_xlabel('r'); axes[1].set_title('inventory field n'); axes[1].legend()
        plt.tight_layout()
        plt.savefig(f"{OUTDIR}/single_case_test.png", dpi=130)
        print(f"\nplot saved to {OUTDIR}/single_case_test.png")
