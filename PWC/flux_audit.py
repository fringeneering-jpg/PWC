"""
Pre-registered flux audit: Rusanov (dynamic_knot_HDF3) vs MUSCL-HLLC+fallback
(dynamic_knot_HDF4), identical physical initial conditions, Nx=512/1024/2048.

Core declared metrics (full spectral/TV analysis deferred -- noted in output):
  E_total residual, mass residual, momentum residual, rho_peak/rho_max,
  max(e_avail)/E_lock, collision time (time of max e_avail), R_HDF, R_knot,
  HLLC fallback count.
"""
import numpy as np
import time
import dynamic_knot_HDF3 as m3
import dynamic_knot_HDF4 as m4

AMP = 0.25
SIGMA = 3.0
K_WAVE = 2.0
L = 60.0
X1, X2 = L*0.35, L*0.65
T_END = 12.0
CFL = 0.25

def e_avail_local(rho, u, A, dx):
    Ax = m3.grad_periodic(A, dx)
    # local energy density available: HDF-kinetic proxy (Pi provided
    # separately), compression excess, flow. Pi is passed in separately.
    return None  # placeholder, computed inline below with Pi available

def run_scheme(scheme, Nx):
    x, dx, rho0, u0, E0v, A0, Pi0 = m3.make_counter_pulses(Nx, L, X1, X2, AMP, SIGMA, K_WAVE)
    U = np.array([rho0, rho0*u0, E0v, A0, Pi0])
    E0 = m3.energy_channels(U, dx)['E_total']
    M0 = np.sum(U[0])*dx
    P0 = np.sum(U[1])*dx

    t = 0.0; step = 0
    max_fallback_total = 0
    peak_e_avail = 0.0
    peak_e_avail_t = 0.0
    peak_rho = rho0.max()

    while t < T_END:
        rho, u, Emed, A, Pi = m3.primitives(U)
        c_s = np.sqrt(np.maximum(m3.dPdrho(rho, A), 1e-12))
        speed = max(np.max(np.abs(u)+c_s), m3.c0)
        dt = CFL*dx/speed
        dt = min(dt, T_END-t)

        if scheme == 'rusanov':
            dUdt1, *_ = m3.rhs(U, dx)
        else:
            out1 = m4.rhs(U, dx)
            dUdt1 = out1[0]; max_fallback_total += out1[7]
        U1 = U + dt*dUdt1
        if np.any(~np.isfinite(U1)) or np.any(U1[0] <= 0):
            print(f'  [{scheme} Nx={Nx}] BLOWUP at t={t:.3f}')
            break

        if scheme == 'rusanov':
            dUdt2, *_ = m3.rhs(U1, dx)
        else:
            out2 = m4.rhs(U1, dx)
            dUdt2 = out2[0]; max_fallback_total += out2[7]
        U2 = 0.5*U + 0.5*(U1 + dt*dUdt2)
        U = U2; t += dt; step += 1

        rho, u, Emed, A, Pi = m3.primitives(U)
        Ax = m3.grad_periodic(A, dx)
        e_hdf_local = 0.5*Pi**2 + 0.5*m3.c0**2*Ax**2
        e_comp_excess = m3.e_EOS(rho) - m3.e_EOS_bg
        e_flow = 0.5*rho*u**2
        e_avail = e_hdf_local + e_comp_excess + e_flow
        cur_peak = e_avail.max()
        if cur_peak > peak_e_avail:
            peak_e_avail = cur_peak; peak_e_avail_t = t
        peak_rho = max(peak_rho, rho.max())

    rho, u, Emed, A, Pi = m3.primitives(U)
    ech = m3.energy_channels(U, dx)
    Mf = np.sum(rho)*dx
    Pf = np.sum(rho*u)*dx
    phi_diag = 0.5*(1.0+np.tanh((e_avail - m3.E_lock)/m3.delta_E))
    mask = phi_diag >= 0.5
    idxs = np.where(mask)[0]
    R_knot = 0.5*dx*len(idxs) if len(idxs) else 0.0
    Ax = m3.grad_periodic(A, dx)
    e_hdf_final = 0.5*Pi**2+0.5*m3.c0**2*Ax**2
    total_hdf = np.sum(e_hdf_final)*dx
    x_center = 0.5*(X1+X2)
    d = np.abs(x - x_center); d = np.minimum(d, L-d)
    order = np.argsort(d)
    cum = np.cumsum(e_hdf_final[order])*dx
    k = np.searchsorted(cum, 0.90*total_hdf) if total_hdf>0 else 0
    R_HDF = d[order[min(k, len(order)-1)]]

    return dict(
        scheme=scheme, Nx=Nx, final_t=t, steps=step,
        E_drift=abs(ech['E_total']-E0)/E0,
        M_drift=abs(Mf-M0)/M0,
        P_drift=abs(Pf-P0)/(abs(P0)+1e-12),
        rho_peak=peak_rho, rho_peak_frac=peak_rho/m3.PARAMS['rho_max'],
        peak_e_avail=peak_e_avail, peak_e_avail_ratio=peak_e_avail/m3.E_lock,
        collision_time=peak_e_avail_t,
        R_knot=R_knot, R_HDF=R_HDF,
        fallback_total=max_fallback_total if scheme=='hllc' else None,
    )

if __name__ == "__main__":
    results = []
    for Nx in [512, 1024, 2048]:
        for scheme in ['rusanov', 'hllc']:
            t0 = time.time()
            r = run_scheme(scheme, Nx)
            dt_wall = time.time()-t0
            results.append(r)
            print(f"[{scheme:8s} Nx={Nx:5d}] t={r['final_t']:.2f} steps={r['steps']} "
                  f"E_drift={r['E_drift']:.4e} M_drift={r['M_drift']:.4e} P_drift={r['P_drift']:.4e} "
                  f"rho_peak/rho_max={r['rho_peak_frac']:.4f} peak_e_avail/E_lock={r['peak_e_avail_ratio']:.4f} "
                  f"t_collision={r['collision_time']:.3f} R_knot={r['R_knot']:.3f} R_HDF={r['R_HDF']:.3f} "
                  f"fallback={r['fallback_total']}  [{dt_wall:.1f}s]")

    print()
    print("=== convergence of peak_e_avail_ratio across resolution, per scheme ===")
    for scheme in ['rusanov', 'hllc']:
        vals = [(r['Nx'], r['peak_e_avail_ratio']) for r in results if r['scheme']==scheme]
        print(f"  {scheme}: {vals}")
    print()
    print("NOTE: full total-variation and high-k spectral-fraction analysis deferred")
    print("(not computed in this pass given time constraints) -- core conservation")
    print("and threshold-relevant metrics only.")
