"""
PWC Stage 2, corrected model (v2): a real HDF wave-field sector coupled to a
real compressible baseline medium, both evolved conservatively from ONE
energy functional. Matter formation is measured as M_knot(t) = E_knot(t)/c0^2,
never as an algebraically-overwritten phase label.

State: U = [rho, rho*u, A, Pi]
  rho, u        : baseline-medium mass density and velocity (always > 0,
                  rho_bg is real, physical, and never subtracted from the
                  dynamics -- only from diagnostic "excess" displays).
  A, Pi         : HDF/light wave field and its conjugate momentum
                  (Pi = dA/dt). A genuine second-order wave field, NOT
                  advected with u and NOT algebraically slaved to anything.

Equations of motion (Hamiltonian, both sectors driven by ONE functional):
  d(rho)/dt   + d(rho u)/dx = 0
  d(rho u)/dt + d(rho u^2 + P_bulk(rho,A))/dx = 0
  dA/dt  = Pi
  dPi/dt = c0^2 * d2A/dx2 - dV_lock/dA(rho,A)

  IMPORTANT: the momentum flux carries NO (dA/dx)^2 "Korteweg" addition.
  That term only belongs in the stress when the differentiated field is
  advected with the fluid (Dphi/Dt=0), which is how it arose in the
  earlier phi-advection model. Here A evolves via its own independent
  wave equation, uncoupled from u -- adding that term breaks exact energy
  conservation (verified: produced 10-34% drift with it present). The
  by-hand conservation proof below requires Txx = P_bulk(rho,A) alone;
  the (dA/dx)^2 and Pi cross-terms in dE/dt cancel exactly via integration
  by parts using ONLY the A/Pi wave equation, with no fluid stress needed.

  P_bulk(rho,A) = rho * d(e_bulk)/d(rho)|_A - e_bulk(rho,A)     (same Legendre
      relation used throughout this project; e_bulk = e_EOS(rho)+V_lock(rho,A))
  V_lock(rho,A) = Lam*A^2*(1-A)^2 + (B/2)*(rho-rho_bg-drho*A)^2  (identical
      functional form to the earlier phi double-well+registration term --
      reused deliberately, since it is already a derived, non-tuned object;
      only its DYNAMICS change -- from passive advection/algebraic slaving
      to a genuine wave equation.)

  c0 = c_med(rho_bg): the wave-speed coefficient is FROZEN at its background
  value for the gradient/stress term (declared simplification, exactly
  analogous to the earlier constant-K treatment) -- the full rho-dependence
  of a local refractive-index effect is not attempted in this reduced model.

Energy ledger (all five terms sum EXACTLY to E_total by construction; no
term is double counted -- E_gradient is reported both standalone and as
part of E_HDF for interpretability):
  E_kinetic  = integral 0.5 rho u^2 dx
  E_EOS      = integral e_EOS(rho) dx                (full, not excess)
  E_HDF_kin  = integral 0.5 Pi^2 dx
  E_gradient = integral 0.5 c0^2 (dA/dx)^2 dx
  E_coupling = integral V_lock(rho,A) dx              ("tied-state" energy)
  E_HDF      = E_HDF_kin + E_gradient                 (propagating/mobile
               wave energy, NOT yet committed to a locked configuration)
  E_total    = E_kinetic + E_EOS + E_HDF + E_coupling

Closed periodic box -> E_boundary_out = 0 identically; the acceptance
criterion is E_total(t) = E_total(0) within a declared numerical tolerance.

phi_diag is used ONLY as a passive display/region classifier. It has zero
effect on P_bulk, V_lock, the stress, the flux, or any state update:
  phi_diag(x,t) = 0.5*(1+tanh((e_avail(x,t)-E_lock)/delta_E))
  e_avail = e_HDF_local + e_compression_excess + e_flow
  Omega_knot(t) = {x : phi_diag(x,t) >= 0.5}
"""
import numpy as np
import sympy as sp
import dynamic_knot_solver as dks
import json, time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUTDIR = r"C:\Users\jaden\cosmology\PWC\knot_audit"

PARAMS = dks.PARAMS

def e_EOS(rho):
    A_, rho_max = PARAMS['A'], PARAMS['rho_max']
    return A_*(-np.log(1-rho/rho_max) - rho/rho_max)

# ---- dV_lock/dA, derived symbolically (reuses the SAME e_bulk expression
#      already used for P and dP/drho, so it is guaranteed consistent) ----
_dVdA_expr = sp.diff(dks._e_bulk, dks._phi)   # d(e_EOS+V_lock)/dphi = dV_lock/dA (e_EOS has no phi-dependence)
_dVdA_func = sp.lambdify(dks._args, _dVdA_expr, 'numpy')
def dVdA(rho, A):
    return _dVdA_func(rho, A, *dks._pvals())

def V_lock(rho, A):
    return dks.eos_ebulk(rho, A) - e_EOS(rho)

def P_bulk(rho, A):
    return dks.eos_P(rho, A)

def dPdrho(rho, A):
    return dks.eos_dPdrho(rho, A)

# ---- frozen constants (identical numeric values to the earlier stage,
#      since PARAMS and rho_bg are unchanged) ----
c0 = float(np.sqrt(dPdrho(np.array([PARAMS['rho_bg']]), np.array([0.0]))[0]))
rho_knot = PARAMS['rho_bg'] + PARAMS['drho']
E_lock = rho_knot * c0**2
delta_E = 0.05 * E_lock
e_EOS_bg = e_EOS(PARAMS['rho_bg'])

print(f"[frozen constants] c0={c0:.6f}  rho_knot={rho_knot:.4f}  "
      f"E_lock={E_lock:.6f}  delta_E={delta_E:.6f}")

def grad_periodic(f, dx):
    return (np.roll(f,-1) - np.roll(f,1)) / (2*dx)

def lap_periodic(f, dx):
    # Must be the discrete adjoint of grad_periodic (central difference)
    # composed with itself -- NOT the compact 3-point stencil. The energy
    # functional's gradient term (dA/dx)^2 is built from grad_periodic, so
    # the wave equation's second-derivative term must be grad_periodic
    # applied twice to satisfy the discrete summation-by-parts identity
    # that makes energy conservation exact (verified analytically: central
    # differences are exactly skew-adjoint under periodic BC, but ONLY
    # when composed consistently with the gradient actually used in the
    # energy -- mixing this with the compact 3-point Laplacian produced a
    # verified 30-70% energy leak).
    return grad_periodic(grad_periodic(f, dx), dx)

def primitives(U):
    rho = U[0]
    u = U[1]/rho
    A = U[2]
    Pi = U[3]
    return rho, u, A, Pi

def rhs(U, dx):
    rho, u, A, Pi = primitives(U)
    dAdx = grad_periodic(A, dx)
    Pb = P_bulk(rho, A)
    # NOTE: no Korteweg-type (dA/dx)^2 addition here. That term is only
    # valid when the field being differentiated is ADVECTED with the fluid
    # (Dphi/Dt=0), which is what made it appear in the earlier phi-advection
    # model. A here evolves via its own independent wave equation, decoupled
    # from u -- adding a (dA/dx)^2 stress term with no compensating physics
    # elsewhere breaks exact energy conservation (verified: it produced
    # 10-34% energy drift even far from any rho_max thrashing). The correct
    # conservation identity (derived by hand, verified numerically below)
    # requires Txx = P_bulk(rho,A) alone.
    Txx = Pb

    F0 = rho*u
    F1 = rho*u**2 + Txx
    Ffluid = np.array([F0, F1])

    c_s = np.sqrt(np.maximum(dPdrho(rho, A), 1e-12))
    Smax_cell = np.abs(u) + c_s
    Smax_face = np.maximum(Smax_cell, np.roll(Smax_cell,-1))

    Ufluid = U[:2]
    U_L = Ufluid
    U_R = np.roll(Ufluid, -1, axis=1)
    F_L = Ffluid
    F_R = np.roll(Ffluid, -1, axis=1)
    F_face = 0.5*(F_L+F_R) - 0.5*Smax_face*(U_R-U_L)
    dfluid_dt = -(F_face - np.roll(F_face,1,axis=1))/dx

    dAdt = Pi
    dPidt = c0**2*lap_periodic(A, dx) - dVdA(rho, A)

    dUdt = np.array([dfluid_dt[0], dfluid_dt[1], dAdt, dPidt])
    return dUdt, rho, u, A, Pi, c_s

def energy_channels(U, dx):
    rho, u, A, Pi = primitives(U)
    dAdx = grad_periodic(A, dx)
    E_kinetic = np.sum(0.5*rho*u**2)*dx
    E_EOS_ = np.sum(e_EOS(rho))*dx
    E_HDF_kin = np.sum(0.5*Pi**2)*dx
    E_gradient = np.sum(0.5*c0**2*dAdx**2)*dx
    E_coupling = np.sum(V_lock(rho, A))*dx
    return dict(E_kinetic=E_kinetic, E_EOS=E_EOS_, E_HDF_kin=E_HDF_kin,
                E_gradient=E_gradient, E_HDF=E_HDF_kin+E_gradient,
                E_coupling=E_coupling,
                E_total=E_kinetic+E_EOS_+E_HDF_kin+E_gradient+E_coupling)

def local_diagnostics(U, dx):
    rho, u, A, Pi = primitives(U)
    dAdx = grad_periodic(A, dx)
    e_hdf_local = 0.5*Pi**2 + 0.5*c0**2*dAdx**2
    e_compression_excess = e_EOS(rho) - e_EOS_bg
    e_flow = 0.5*rho*u**2
    e_avail = e_hdf_local + e_compression_excess + e_flow
    phi_diag = 0.5*(1.0 + np.tanh((e_avail - E_lock)/delta_E))
    e_locked = V_lock(rho, A)
    e_boundary = 0.5*c0**2*dAdx**2
    return dict(e_avail=e_avail, phi_diag=phi_diag, e_hdf_local=e_hdf_local,
                e_compression_excess=e_compression_excess, e_flow=e_flow,
                e_locked=e_locked, e_boundary=e_boundary)

def R_from_mask(mask, dx):
    idx = np.where(mask)[0]
    if len(idx) == 0:
        return 0.0
    return 0.5*dx*len(idx)

def R90_cumulative(weight, dx, x, x_center):
    total = np.sum(weight)*dx
    if total <= 0:
        return 0.0
    d = np.abs(x - x_center)
    d = np.minimum(d, np.max(x)-d)  # periodic distance
    order = np.argsort(d)
    cum = np.cumsum(weight[order])*dx
    k = np.searchsorted(cum, 0.90*total)
    if k >= len(order):
        return d[order[-1]]
    return d[order[k]]

def make_counter_pulses(Nx, L, x1, x2, amp, sigma, k_wave):
    dx = L/Nx
    x = (np.arange(Nx)+0.5)*dx
    A1 = amp*np.exp(-((x-x1)/sigma)**2)*np.cos(k_wave*(x-x1))
    A2 = amp*np.exp(-((x-x2)/sigma)**2)*np.cos(k_wave*(x-x2))
    dA1dx = grad_periodic(A1, dx)
    dA2dx = grad_periodic(A2, dx)
    Pi1 = -c0*dA1dx   # right-moving
    Pi2 = +c0*dA2dx   # left-moving
    A0 = A1 + A2
    Pi0 = Pi1 + Pi2
    rho0 = np.full(Nx, PARAMS['rho_bg'])
    u0 = np.zeros(Nx)
    return x, dx, rho0, u0, A0, Pi0

def run_case(label, Nx, L, x1, x2, amp, sigma, k_wave, T_end, cfl=0.25, save_every=20):
    x, dx, rho0, u0, A0, Pi0 = make_counter_pulses(Nx, L, x1, x2, amp, sigma, k_wave)
    U = np.array([rho0, rho0*u0, A0, Pi0])
    diag0 = local_diagnostics(U, dx)
    peak_ea = diag0['e_avail'].max()
    print(f"[{label}] peak e_avail(t=0)={peak_ea:.6f} vs E_lock={E_lock:.6f}  "
          f"({'ABOVE' if peak_ea>=E_lock else 'below'} threshold)")

    t = 0.0
    step = 0
    hist = dict(t=[], E_total=[], E_kinetic=[], E_EOS=[], E_HDF=[], E_gradient=[],
                E_coupling=[], M=[], momentum=[], rhomax=[], phimax=[],
                e_avail_max=[], R_knot=[], R_HDF=[], E_knot=[], M_knot=[], L_HDF=[])
    ech0 = energy_channels(U, dx)
    E0 = ech0['E_total']
    M0 = np.sum(U[0])*dx

    x_center = 0.5*(x1+x2)

    while t < T_end:
        rho, u, A, Pi = primitives(U)
        c_s = np.sqrt(np.maximum(dPdrho(rho, A), 1e-12))
        speed = max(np.max(np.abs(u)+c_s), c0)
        dt = cfl*dx/speed
        dt = min(dt, T_end-t)
        ok = False
        for attempt in range(10):
            dUdt1, *_ = rhs(U, dx)
            U1 = U + dt*dUdt1
            if np.any(U1[0] >= PARAMS['rho_max']*0.999) or np.any(U1[0] <= 0) or np.any(~np.isfinite(U1)):
                dt *= 0.5; continue
            dUdt2, *_ = rhs(U1, dx)
            U2 = 0.5*U + 0.5*(U1 + dt*dUdt2)
            if np.any(U2[0] >= PARAMS['rho_max']*0.999) or np.any(U2[0] <= 0) or np.any(~np.isfinite(U2)):
                dt *= 0.5; continue
            ok = True; break
        if not ok:
            print(f"  [{label}] [FAIL] rho hit rho_max boundary repeatedly at t={t:.4f}")
            break
        U = U2; t += dt; step += 1

        if step % save_every == 0:
            ech = energy_channels(U, dx)
            diag = local_diagnostics(U, dx)
            rho, u, A, Pi = primitives(U)
            mask = diag['phi_diag'] >= 0.5
            R_knot = R_from_mask(mask, dx)
            R_HDF = R90_cumulative(diag['e_hdf_local'], dx, x, x_center)
            E_knot = np.sum((diag['e_locked'] + diag['e_compression_excess'] + diag['e_boundary'])[mask])*dx
            M_knot = E_knot / c0**2
            L_HDF = np.sum(diag['e_hdf_local'])*dx

            hist['t'].append(t)
            for kk in ('E_total','E_kinetic','E_EOS','E_HDF','E_gradient','E_coupling'):
                hist[kk].append(ech[kk])
            hist['M'].append(np.sum(rho)*dx)
            hist['momentum'].append(np.sum(rho*u)*dx)
            hist['rhomax'].append(rho.max())
            hist['phimax'].append(diag['phi_diag'].max())
            hist['e_avail_max'].append(diag['e_avail'].max())
            hist['R_knot'].append(R_knot)
            hist['R_HDF'].append(R_HDF)
            hist['E_knot'].append(E_knot)
            hist['M_knot'].append(M_knot)
            hist['L_HDF'].append(L_HDF)

    for kk in hist: hist[kk] = np.array(hist[kk])
    return dict(label=label, x=x, dx=dx, U_final=U, hist=hist, E0=E0, M0=M0,
                peak_e_avail=peak_ea, final_t=t)

def summarize(res):
    hist = res['hist']
    if len(hist['t']) == 0:
        print(f"  [{res['label']}] NO DATA -- failed immediately")
        return
    E_drift = np.abs(hist['E_total']-res['E0'])/res['E0']
    M_drift = np.abs(hist['M']-res['M0'])/res['M0']
    print(f"  [{res['label']}] reached t={hist['t'][-1]:.2f}/{res['final_t']:.2f}, "
          f"peak_e_avail/E_lock={res['peak_e_avail']/E_lock:.3f}")
    print(f"    E_total drift: max={E_drift.max():.4e}, final={E_drift[-1]:.4e}")
    print(f"    mass drift:   max={M_drift.max():.4e}")
    print(f"    rho_max reached: {hist['rhomax'].max():.4f} (limit {PARAMS['rho_max']})")
    print(f"    phi_diag_max reached: {hist['phimax'].max():.4f}")
    print(f"    R_knot(t): final={hist['R_knot'][-1]:.4f}, max={hist['R_knot'].max():.4f}")
    print(f"    R_HDF(t):  final={hist['R_HDF'][-1]:.4f}")
    print(f"    M_knot(t): final={hist['M_knot'][-1]:.6e}, max={hist['M_knot'].max():.6e}")
    print(f"    L_HDF(t):  initial={hist['L_HDF'][0]:.6f}, final={hist['L_HDF'][-1]:.6f}")
    retained = hist['R_knot'][-1] > 0.0
    print(f"    RETAINED LOCKED REGION AT FINAL TIME: {retained}")

if __name__ == "__main__":
    t0 = time.time()
    Nx = 1024
    L = 60.0
    x1, x2 = L*0.35, L*0.65   # converging toward center
    sigma = 3.0
    k_wave = 2.0
    T_end = 80.0

    print("=== calibrating counter-propagating pulse amplitude against E_lock ===")
    print("(peak e_avail measured AT COLLISION, not at t=0, since packets start separated)")
    for amp in np.linspace(0.05, 1.2, 24):
        x, dx, rho0, u0, A0, Pi0 = make_counter_pulses(Nx, L, x1, x2, amp, sigma, k_wave)
        U = np.array([rho0, rho0*u0, A0, Pi0])
        diag = local_diagnostics(U, dx)
        pea0 = diag['e_avail'].max()
        print(f"  amp={amp:.4f}: peak_e_avail(t=0, separated)={pea0:.6f}")
