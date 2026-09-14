"""
PWC conservative 1D phase-field hydrodynamics existence test.
Conserved variables U = [rho, rho*u, rho*phi]. Rusanov (local Lax-Friedrichs)
finite-volume scheme, periodic BC, SSP-RK2 time stepping, adaptive dt with
explicit rejection (not clipping) of any step that would cross rho_max.

Pressure and bulk energy are derived symbolically from the SAME energy
functional (see pwc_eos.py) -- not chosen independently.
"""
import numpy as np
import sympy as sp
import json, os, time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUTDIR = r"C:\Users\jaden\cosmology\PWC\knot_audit"
os.makedirs(OUTDIR, exist_ok=True)

# ---------- symbolic EOS, derived once, lambdified for speed ----------
_rho, _phi, _A, _rho_max, _Lam, _B, _rho_bg, _drho = sp.symbols(
    'rho phi A rho_max Lambda B rho_bg drho', positive=True)
_e_EOS = _A*(-sp.log(1-_rho/_rho_max) - _rho/_rho_max)
_e_bulk = _e_EOS + _Lam*_phi**2*(1-_phi)**2 + sp.Rational(1,2)*_B*(_rho - _rho_bg - _drho*_phi)**2
_de_drho = sp.diff(_e_bulk, _rho)
_P = sp.simplify(_rho*_de_drho - _e_bulk)
_dPdrho = sp.diff(_P, _rho)

_args = (_rho, _phi, _A, _rho_max, _Lam, _B, _rho_bg, _drho)
P_func = sp.lambdify(_args, _P, 'numpy')
ebulk_func = sp.lambdify(_args, _e_bulk, 'numpy')
dPdrho_func = sp.lambdify(_args, _dPdrho, 'numpy')

# ---------- dimensionless parameters (declared, not tuned) ----------
# order must match _args = (rho, phi, A, rho_max, Lam, B, rho_bg, drho)
PARAMS = dict(A=1.0, rho_max=1.0, Lam=1.0, B=10.0, rho_bg=0.3, drho=0.5)
_PARAM_ORDER = ['A', 'rho_max', 'Lam', 'B', 'rho_bg', 'drho']
K = 1.0   # gradient/Korteweg stiffness

def _pvals():
    return [PARAMS[k] for k in _PARAM_ORDER]

def eos_P(rho, phi):
    return P_func(rho, phi, *_pvals())
def eos_ebulk(rho, phi):
    return ebulk_func(rho, phi, *_pvals())
def eos_dPdrho(rho, phi):
    return dPdrho_func(rho, phi, *_pvals())

def grad_periodic(f, dx):
    return (np.roll(f,-1) - np.roll(f,1)) / (2*dx)

def primitives(U):
    rho = U[0]
    u = U[1]/rho
    phi = U[2]/rho
    return rho, u, phi

def rhs(U, dx):
    rho, u, phi = primitives(U)
    dphidx = grad_periodic(phi, dx)
    P = eos_P(rho, phi)
    Txx = P + 0.5*K*dphidx**2

    F0 = rho*u
    F1 = rho*u**2 + Txx
    F2 = rho*u*phi
    F = np.array([F0, F1, F2])

    c_s = np.sqrt(np.maximum(eos_dPdrho(rho, phi), 1e-12))
    Smax_cell = np.abs(u) + c_s
    # face wave speed = max of neighboring cells (Rusanov)
    Smax_face = np.maximum(Smax_cell, np.roll(Smax_cell,-1))

    U_L = U
    U_R = np.roll(U, -1, axis=1)
    F_L = F
    F_R = np.roll(F, -1, axis=1)

    F_face = 0.5*(F_L+F_R) - 0.5*Smax_face*(U_R-U_L)
    # dU/dt = -(F_{i+1/2} - F_{i-1/2})/dx
    dUdt = -(F_face - np.roll(F_face,1,axis=1))/dx
    return dUdt, rho, u, phi, dphidx, c_s

def total_energy(U, dx):
    rho, u, phi = primitives(U)
    dphidx = grad_periodic(phi, dx)
    e_tot = 0.5*rho*u**2 + eos_ebulk(rho, phi) + 0.5*K*dphidx**2
    return np.sum(e_tot)*dx, e_tot

def run_sim(Nx, L=40.0, R0=3.0, x0=None, T_end=60.0, cfl=0.3,
            rho_amp=0.4, delta_wall=1.0, verbose=True, save_prefix=None):
    dx = L/Nx
    x = (np.arange(Nx)+0.5)*dx
    if x0 is None: x0 = L/2

    phi0 = 0.5*(1-np.tanh((np.abs(x-x0)-R0)/delta_wall))
    # rho0 consistent with the B-coupling's own preferred relation rho=rho_bg+drho*phi,
    # so the initial state doesn't start with an artificial rho-phi mismatch that the
    # solver then just relaxes (that mismatch, not instability, was the real bug).
    # rho_amp now perturbs AROUND that consistent state, not away from it.
    rho0 = PARAMS['rho_bg'] + PARAMS['drho']*phi0 + rho_amp*np.exp(-((x-x0)/R0)**2)
    u0 = np.zeros(Nx)
    U = np.array([rho0, rho0*u0, rho0*phi0])

    t = 0.0
    M0, _ = None, None
    M_t, Pnet_t, E_t, t_hist, Rknot_t, rhomax_t = [], [], [], [], [], []
    step = 0
    rejected_steps = 0
    max_steps = 2_000_000

    while t < T_end and step < max_steps:
        rho, u, phi = primitives(U)
        if np.any(rho <= 0) or np.any(~np.isfinite(rho)):
            if verbose: print(f"  [FAIL] non-physical density at t={t:.4f}, step={step}")
            break
        c_s = np.sqrt(np.maximum(eos_dPdrho(rho, phi), 1e-12))
        dt = cfl*dx/np.max(np.abs(u)+c_s+1e-12)
        dt = min(dt, T_end-t)

        # try step, reject (halve dt) if rho_max would be crossed
        accepted = False
        for attempt in range(8):
            dUdt1, *_ = rhs(U, dx)
            U1 = U + dt*dUdt1
            rho1 = U1[0]
            if np.any(rho1 >= PARAMS['rho_max']*0.999) or np.any(rho1 <= 0):
                dt *= 0.5
                rejected_steps += 1
                continue
            dUdt2, *_ = rhs(U1, dx)
            U2 = 0.5*U + 0.5*(U1 + dt*dUdt2)
            rho2 = U2[0]
            if np.any(rho2 >= PARAMS['rho_max']*0.999) or np.any(rho2 <= 0) or np.any(~np.isfinite(rho2)):
                dt *= 0.5
                rejected_steps += 1
                continue
            accepted = True
            break
        if not accepted:
            if verbose: print(f"  [FAIL] could not find stable dt at t={t:.4f} after 8 halvings -- rho hit boundary repeatedly")
            break

        U = U2
        t += dt
        step += 1

        if step % max(1,int(50)) == 0 or step==1:
            Etot, e_tot_arr = total_energy(U, dx)
            rho_c, u_c, phi_c = primitives(U)
            M = np.sum(rho_c)*dx
            Pnet = np.sum(rho_c*u_c)*dx
            # knot radius: where phi crosses 0.5, measured from x0
            idx = np.where(phi_c>=0.5)[0]
            if len(idx)>0:
                Rknot = 0.5*dx*len(idx)  # crude: half-width of phi>=0.5 region
            else:
                Rknot = 0.0
            M_t.append(M); Pnet_t.append(Pnet); E_t.append(Etot)
            t_hist.append(t); Rknot_t.append(Rknot); rhomax_t.append(rho_c.max())

    result = dict(Nx=Nx, t=np.array(t_hist), M=np.array(M_t), Pnet=np.array(Pnet_t),
                  E=np.array(E_t), Rknot=np.array(Rknot_t), rhomax=np.array(rhomax_t),
                  rejected_steps=rejected_steps, final_step=step, final_t=t,
                  x=x, U_final=U, completed=(t>=T_end))
    if verbose:
        print(f"Nx={Nx}: steps={step}, rejected={rejected_steps}, final_t={t:.3f}/{T_end}, completed={result['completed']}")
        if len(M_t)>1:
            print(f"  mass drift: {abs(M_t[-1]-M_t[0])/M_t[0]:.3e}")
            print(f"  energy drift: {abs(E_t[-1]-E_t[0])/E_t[0]:.3e}")
    return result

if __name__ == "__main__":
    print("=== SINGLE RESOLUTION TEST FIRST (Nx=256, short run) ===")
    t0=time.time()
    res = run_sim(Nx=256, T_end=10.0, verbose=True)
    print(f"wall time: {time.time()-t0:.1f}s")
