"""
Geometry sweep v2: separation scales with sigma (D=8*sigma) so every case
is genuinely separated at t=0 (overlap = exp[-(D/(2*sigma))^2] = exp(-16)
~= 1.1e-7, far below the declared 1e-4 tolerance, for ANY sigma -- this was
the bug in v1, where a FIXED box made wide-sigma packets overlap from the
start). Box: L_box=6*D, xC=L_box/2, xL=xC-D/2, xR=xC+D/2. Resolution scales
too: Nx chosen so dx <= sigma/30 for every case.

R_focus is now a descriptive diagnostic only, NOT a gate. The real
criterion is whether collision-region e_avail can cross E_lock while each
separated incoming packet stays below it.
"""
import numpy as np
import dynamic_knot_HDF3 as m3
import json

def geometry_for_sigma(sigma):
    D = 8.0*sigma
    L_box = 6.0*D
    xC = L_box/2.0
    xL = xC - D/2.0
    xR = xC + D/2.0
    Nx = int(np.ceil(L_box/(sigma/30.0)))
    return dict(D=D, L_box=L_box, xC=xC, xL=xL, xR=xR, Nx=Nx)

REF_ENERGY = None  # set from a reference case below

def single_packet_energy(amp, sigma, k_wave, xC, Nx, L_box):
    dx = L_box/Nx
    x = (np.arange(Nx)+0.5)*dx
    A = amp*np.exp(-((x-xC)/sigma)**2)*np.cos(k_wave*(x-xC))
    Ax = m3.grad_periodic(A, dx)
    Pi = -m3.c0*Ax
    return np.sum(0.5*Pi**2+0.5*m3.c0**2*Ax**2)*dx

def amp_for_energy(sigma, k_wave, xC, Nx, L_box, target_E):
    E_unit = single_packet_energy(1.0, sigma, k_wave, xC, Nx, L_box)
    if E_unit <= 0:
        return None
    return np.sqrt(target_E/E_unit)

def make_pulses(Nx, L_box, xL, xR, amp, sigma, k_wave, thetaL, thetaR):
    dx = L_box/Nx
    x = (np.arange(Nx)+0.5)*dx
    AL = amp*np.exp(-((x-xL)/sigma)**2)*np.cos(k_wave*(x-xL)+thetaL)
    AR = amp*np.exp(-((x-xR)/sigma)**2)*np.cos(k_wave*(x-xR)+thetaR)
    dALdx = m3.grad_periodic(AL, dx)
    dARdx = m3.grad_periodic(AR, dx)
    PiL = -m3.c0*dALdx
    PiR = m3.c0*dARdx
    A0 = AL+AR
    Pi0 = PiL+PiR
    rho0 = np.full(Nx, m3.PARAMS['rho_bg'])
    u0 = np.zeros(Nx)
    return x, dx, rho0, u0, A0, Pi0

def envelope_centroid_and_width(e_density, x, region_mask):
    w = e_density*region_mask
    tot = np.sum(w)
    if tot <= 1e-15:
        return None, None
    c = np.sum(w*x)/tot
    width = np.sqrt(np.sum(w*(x-c)**2)/tot)
    return c, width

def e_avail_field(rho,u,A,Pi,dx):
    Ax = m3.grad_periodic(A, dx)
    e_hdf = 0.5*Pi**2+0.5*m3.c0**2*Ax**2
    e_comp = m3.e_EOS(rho)-m3.e_EOS_bg
    e_flow = 0.5*rho*u**2
    e_lock = m3.V_lock(rho,A)
    return e_hdf+e_comp+e_flow+e_lock, e_hdf, e_comp, e_flow, e_lock

def run_geometry_case(sigma, k_wave, target_E, delta_theta=0.0, cfl=0.25):
    geo = geometry_for_sigma(sigma)
    Nx, L_box, xL, xR, xC, D = geo['Nx'], geo['L_box'], geo['xL'], geo['xR'], geo['xC'], geo['D']
    overlap = np.exp(-(D/(2*sigma))**2)

    amp = amp_for_energy(sigma, k_wave, xC, Nx, L_box, target_E)
    if amp is None or not np.isfinite(amp):
        return dict(sigma=sigma, k_wave=k_wave, note='degenerate shape', overlap=float(overlap))

    x, dx, rho0, u0, A0, Pi0 = make_pulses(Nx, L_box, xL, xR, amp, sigma, k_wave, 0.0, delta_theta)
    U = np.array([rho0, rho0*u0, 0.5*rho0*u0**2+m3.e_EOS(rho0)+m3.V_lock(rho0,A0), A0, Pi0])
    E0 = m3.energy_channels(U,dx)['E_total']
    M0 = np.sum(U[0])*dx
    P0 = np.sum(U[1])*dx

    T_end = 8.0*sigma/m3.c0
    left_mask = x < xC
    right_mask = x >= xC

    t=0.0; step=0
    trace=[]        # (t, max e_avail overall, loc)
    coll_trace=[]   # (t, E_coll integrated over |x-xC|<=2sigma)
    single_peak_pre_collision = 0.0
    centroidL_hist=[]; centroidR_hist=[]
    widthL_hist=[]; widthR_hist=[]
    coll_mask = np.abs(x-xC) <= 2*sigma
    E_one_packet_initial = np.sum((0.5*Pi0**2+0.5*m3.c0**2*m3.grad_periodic(A0,dx)**2)*left_mask)*dx

    while t < T_end:
        rho,u,Emed,A,Pi = m3.primitives(U)
        c_s = np.sqrt(np.maximum(m3.dPdrho(rho,A),1e-12))
        dt = cfl*dx/max(np.max(np.abs(u)+c_s), m3.c0)
        dt = min(dt, T_end-t)
        dUdt1,*_ = m3.rhs(U,dx); U1=U+dt*dUdt1
        if np.any(~np.isfinite(U1)) or np.any(U1[0]<=0):
            return dict(sigma=sigma,k_wave=k_wave,note='blowup',overlap=float(overlap))
        dUdt2,*_ = m3.rhs(U1,dx); U2=0.5*U+0.5*(U1+dt*dUdt2)
        U=U2; t+=dt; step+=1

        if step % 20 == 0:
            rho,u,Emed,A,Pi = m3.primitives(U)
            e_avail,e_hdf,e_comp,e_flow,e_lock = e_avail_field(rho,u,A,Pi,dx)
            cL,wL = envelope_centroid_and_width(e_hdf,x,left_mask)
            cR,wR = envelope_centroid_and_width(e_hdf,x,right_mask)
            centroidL_hist.append((t,cL)); centroidR_hist.append((t,cR))
            widthL_hist.append((t,wL)); widthR_hist.append((t,wR))
            trace.append((t,e_avail.max(),x[np.argmax(e_avail)]))
            E_coll = np.sum(e_avail*coll_mask)*dx
            coll_trace.append((t,E_coll))
            if cL is not None and cR is not None and (cR-cL) > 3*sigma:
                single_peak_pre_collision = max(single_peak_pre_collision, e_avail.max())

    diffs = [(tt,(cr-cl) if (cl is not None and cr is not None) else None) for (tt,cl),(_,cr) in zip(centroidL_hist,centroidR_hist)]
    valid = [(tt,d) for tt,d in diffs if d is not None]
    tC_meas = min(valid, key=lambda p: abs(p[1]))[0] if valid else T_end/2
    window = 2*sigma/m3.c0
    win_trace = [(tt,pk,loc) for tt,pk,loc in trace if abs(tt-tC_meas)<=window]
    collision_peak = max((pk for _,pk,_ in win_trace), default=0.0)
    R_focus = collision_peak/single_peak_pre_collision if single_peak_pre_collision>0 else float('nan')

    coll_peak_E = max((e for _,e in coll_trace), default=0.0)
    C_coll = coll_peak_E/E_one_packet_initial if E_one_packet_initial>0 else float('nan')

    rho,u,Emed,A,Pi = m3.primitives(U)
    ech = m3.energy_channels(U,dx)
    Mf = np.sum(rho)*dx; Pf = np.sum(rho*u)*dx

    return dict(sigma=sigma, k_wave=k_wave, amp=float(amp), overlap=float(overlap),
                Nx=Nx, L_box=float(L_box), D=float(D),
                tC_measured=float(tC_meas), single_peak_pre_collision=float(single_peak_pre_collision),
                collision_peak=float(collision_peak), R_focus=float(R_focus),
                C_coll=float(C_coll),
                E_drift=float(abs(ech['E_total']-E0)/E0), M_drift=float(abs(Mf-M0)/M0),
                P_drift=float(abs(Pf-P0)/(abs(P0)+1e-12)),
                rho_peak_frac=float(rho.max()/m3.PARAMS['rho_max']))

if __name__ == "__main__":
    REF_ENERGY = single_packet_energy(0.05, 3.0, 2.0, 0.0, 2000, 200.0)
    print(f"reference single-packet HDF energy: {REF_ENERGY:.6e}")
    print()
    results = []
    for k_wave in [0, 0.25, 0.5, 1, 2]:
        for sigma in [3, 6, 12]:
            geo = geometry_for_sigma(sigma)
            print(f"sigma={sigma}: D={geo['D']:.1f} L_box={geo['L_box']:.1f} Nx={geo['Nx']} overlap=exp(-16)={np.exp(-16):.3e}")
            r = run_geometry_case(sigma, k_wave, REF_ENERGY)
            results.append(r)
            print(f"  k_wave={k_wave:.2f} sigma={sigma:2.0f}: {r}")

    valid = [r for r in results if 'R_focus' in r]
    if valid:
        best = max(valid, key=lambda r: r['R_focus'])
        print()
        print(f"Best (descriptive) R_focus: k_wave={best['k_wave']}, sigma={best['sigma']}, R_focus={best['R_focus']:.4f}, C_coll={best['C_coll']:.4f}")
        for r in sorted(valid, key=lambda r: -r['C_coll']):
            print(f"  k={r['k_wave']:.2f} sigma={r['sigma']:2.0f}: R_focus={r['R_focus']:.4f} C_coll={r['C_coll']:.4f} E_drift={r['E_drift']:.2e}")

    with open(r"C:\Users\jaden\cosmology\PWC\knot_audit\geometry_sweep_v2.json","w") as f:
        json.dump(results, f, indent=2)
