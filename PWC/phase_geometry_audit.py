"""
Phase/geometry audit (pre-registered, no threshold interpretation): does a
pair of counter-propagating HDF wave packets actually focus (constructively
reinforce) at collision, or does it defocus? Run at LOW amplitude only.

xL=21, xR=39, xC=30, sigma=3, k_wave=2 (as declared). Sweep the relative
carrier phase delta_theta = thetaR-thetaL over 8 values, measure:
  - single-packet pre-collision peak e_avail (before envelopes overlap)
  - collision-window peak e_avail (|x-xC|<=2*sigma, t in [tC-2sigma/c0, tC+2sigma/c0])
  - R_focus = collision_peak / single_packet_peak
tC is measured from actual tracked envelope centroids, not assumed from c0.
"""
import numpy as np
import dynamic_knot_HDF3 as m3
import json

L = 60.0
XL, XR, XC = 21.0, 39.0, 30.0
SIGMA = 3.0
K_WAVE = 2.0
AMP_LOW = 0.05   # low amplitude, no threshold interpretation at this stage

def make_pulses_with_phase(Nx, amp, sigma, k_wave, thetaL, thetaR):
    dx = L/Nx
    x = (np.arange(Nx)+0.5)*dx
    AL = amp*np.exp(-((x-XL)/sigma)**2)*np.cos(k_wave*(x-XL)+thetaL)
    AR = amp*np.exp(-((x-XR)/sigma)**2)*np.cos(k_wave*(x-XR)+thetaR)
    dALdx = m3.grad_periodic(AL, dx)
    dARdx = m3.grad_periodic(AR, dx)
    PiL = -m3.c0*dALdx   # right-moving
    PiR = m3.c0*dARdx    # left-moving
    A0 = AL+AR
    Pi0 = PiL+PiR
    rho0 = np.full(Nx, m3.PARAMS['rho_bg'])
    u0 = np.zeros(Nx)
    return x, dx, rho0, u0, A0, Pi0

def envelope_centroid(e_density, x, region_mask):
    w = e_density * region_mask
    tot = np.sum(w)
    if tot <= 1e-15:
        return None
    return np.sum(w*x)/tot

def e_avail_field(rho, u, A, Pi, dx):
    Ax = m3.grad_periodic(A, dx)
    e_hdf = 0.5*Pi**2 + 0.5*m3.c0**2*Ax**2
    e_comp = m3.e_EOS(rho) - m3.e_EOS_bg
    e_flow = 0.5*rho*u**2
    return e_hdf + e_comp + e_flow, e_hdf

def run_phase_case(delta_theta, Nx=1024, T_end=14.0, cfl=0.25, print_trace=False):
    thetaL, thetaR = 0.0, delta_theta
    x, dx, rho0, u0, A0, Pi0 = make_pulses_with_phase(Nx, AMP_LOW, SIGMA, K_WAVE, thetaL, thetaR)
    U = np.array([rho0, rho0*u0, 0.5*rho0*u0**2+m3.e_EOS(rho0)+m3.V_lock(rho0,A0), A0, Pi0])

    left_mask = x < XC
    right_mask = x >= XC

    t = 0.0; step = 0
    trace = []
    single_peak_pre_collision = 0.0
    centroidL_hist = []
    centroidR_hist = []

    while t < T_end:
        rho, u, Emed, A, Pi = m3.primitives(U)
        c_s = np.sqrt(np.maximum(m3.dPdrho(rho,A),1e-12))
        dt = cfl*dx/max(np.max(np.abs(u)+c_s), m3.c0)
        dt = min(dt, T_end-t)
        dUdt1,*_ = m3.rhs(U,dx); U1=U+dt*dUdt1
        dUdt2,*_ = m3.rhs(U1,dx); U2=0.5*U+0.5*(U1+dt*dUdt2)
        U=U2; t+=dt; step+=1

        if step % 20 == 0:
            rho,u,Emed,A,Pi = m3.primitives(U)
            e_avail, e_hdf = e_avail_field(rho,u,A,Pi,dx)
            cL = envelope_centroid(e_hdf, x, left_mask)
            cR = envelope_centroid(e_hdf, x, right_mask)
            centroidL_hist.append((t,cL))
            centroidR_hist.append((t,cR))
            trace.append((t, e_avail.max(), x[np.argmax(e_avail)]))
            # pre-collision: while packets still resolved as separate (cL<XC<cR with margin)
            if cL is not None and cR is not None and (cR-cL) > 3*SIGMA:
                single_peak_pre_collision = max(single_peak_pre_collision, e_avail.max())

    # find tC: time when centroids cross (cR-cL minimal / crosses zero)
    diffs = [(tt, (cr-cl) if (cl is not None and cr is not None) else None) for (tt,cl),(_,cr) in zip(centroidL_hist,centroidR_hist)]
    valid = [(tt,d) for tt,d in diffs if d is not None]
    tC = min(valid, key=lambda p: abs(p[1]))[0] if valid else T_end/2

    # collision window peak
    window_mask_t = [(tt,pk,loc) for tt,pk,loc in trace if abs(tt-tC) <= 2*SIGMA/m3.c0]
    collision_peak = max((pk for _,pk,_ in window_mask_t), default=0.0)
    collision_peak_loc = None
    for tt,pk,loc in window_mask_t:
        if pk == collision_peak:
            collision_peak_loc = (tt,loc)

    R_focus = collision_peak / single_peak_pre_collision if single_peak_pre_collision>0 else float('nan')

    if print_trace:
        for tt,pk,loc in trace:
            print(f'    t={tt:.3f} peak_e_avail={pk:.5f} at x={loc:.2f}')

    return dict(delta_theta=delta_theta, tC=tC, single_peak_pre_collision=single_peak_pre_collision,
                collision_peak=collision_peak, collision_peak_loc=collision_peak_loc, R_focus=R_focus)

if __name__ == "__main__":
    print(f"[constants] c0={m3.c0:.4f}  XL={XL} XR={XR} XC={XC} sigma={SIGMA} k_wave={K_WAVE}")
    print(f"amplitude for this audit: {AMP_LOW} (low, no threshold interpretation)")
    print()
    phases = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi, 5*np.pi/4, 3*np.pi/2, 7*np.pi/4]
    results = []
    for dth in phases:
        r = run_phase_case(dth)
        results.append(r)
        print(f"delta_theta={dth:.4f} ({dth/np.pi:.2f}*pi): tC={r['tC']:.3f} "
              f"single_peak={r['single_peak_pre_collision']:.5f} "
              f"collision_peak={r['collision_peak']:.5f} "
              f"R_focus={r['R_focus']:.4f}  loc={r['collision_peak_loc']}")

    best = max(results, key=lambda r: r['R_focus'])
    print()
    print(f"BEST phase: delta_theta={best['delta_theta']:.4f} ({best['delta_theta']/np.pi:.2f}*pi), R_focus={best['R_focus']:.4f}")

    with open(r"C:\Users\jaden\cosmology\PWC\knot_audit\phase_geometry_audit.json","w") as f:
        json.dump([{k:(v if not isinstance(v,tuple) else list(v)) for k,v in r.items()} for r in results], f, indent=2)
