"""
Geometry sweep (pre-registered): does ANY (k_wave, sigma) combination of
counter-propagating HDF wave packets produce genuine constructive
reinforcement (R_focus > 1) at collision? Fixed total initial HDF energy
per packet across the sweep (amplitude rescaled to match a reference
energy for each shape). Best phase from the prior audit (delta_theta=0,
R_focus=0.85, the least-defocusing of the 8 tested) used throughout.
"""
import numpy as np
import dynamic_knot_HDF3 as m3
import json

L = 60.0
XL, XR, XC = 21.0, 39.0, 30.0
DELTA_THETA = 0.0

def single_packet_energy(amp, sigma, k_wave, Nx=1024):
    dx = L/Nx
    x = (np.arange(Nx)+0.5)*dx
    A = amp*np.exp(-((x-XC)/sigma)**2)*np.cos(k_wave*(x-XC))
    Ax = m3.grad_periodic(A, dx)
    Pi = -m3.c0*Ax
    return np.sum(0.5*Pi**2+0.5*m3.c0**2*Ax**2)*dx

REF_ENERGY = single_packet_energy(0.05, 3.0, 2.0)
print(f"reference single-packet HDF energy (amp=0.05,sigma=3,k=2): {REF_ENERGY:.6e}")

def amp_for_energy(sigma, k_wave, target_E):
    E_unit = single_packet_energy(1.0, sigma, k_wave)
    if E_unit <= 0:
        return None
    return np.sqrt(target_E/E_unit)

def make_pulses(Nx, amp, sigma, k_wave, thetaL, thetaR):
    dx = L/Nx
    x = (np.arange(Nx)+0.5)*dx
    AL = amp*np.exp(-((x-XL)/sigma)**2)*np.cos(k_wave*(x-XL)+thetaL)
    AR = amp*np.exp(-((x-XR)/sigma)**2)*np.cos(k_wave*(x-XR)+thetaR)
    dALdx = m3.grad_periodic(AL, dx)
    dARdx = m3.grad_periodic(AR, dx)
    PiL = -m3.c0*dALdx
    PiR = m3.c0*dARdx
    A0 = AL+AR
    Pi0 = PiL+PiR
    rho0 = np.full(Nx, m3.PARAMS['rho_bg'])
    u0 = np.zeros(Nx)
    return x, dx, rho0, u0, A0, Pi0

def envelope_centroid(e_density, x, region_mask):
    w = e_density*region_mask
    tot = np.sum(w)
    if tot <= 1e-15:
        return None
    return np.sum(w*x)/tot

def e_avail_field(rho,u,A,Pi,dx):
    Ax = m3.grad_periodic(A, dx)
    e_hdf = 0.5*Pi**2+0.5*m3.c0**2*Ax**2
    e_comp = m3.e_EOS(rho)-m3.e_EOS_bg
    e_flow = 0.5*rho*u**2
    return e_hdf+e_comp+e_flow, e_hdf

def run_geometry_case(sigma, k_wave, Nx=1024, T_end=None, cfl=0.25):
    amp = amp_for_energy(sigma, k_wave, REF_ENERGY)
    if amp is None or not np.isfinite(amp):
        return dict(sigma=sigma, k_wave=k_wave, amp=None, R_focus=None, note='degenerate (k=0 zero-energy shape)')
    if T_end is None:
        T_end = (XR-XL)/m3.c0 + 6*sigma/m3.c0 + 3.0

    x, dx, rho0, u0, A0, Pi0 = make_pulses(Nx, amp, sigma, k_wave, 0.0, DELTA_THETA)
    U = np.array([rho0, rho0*u0, 0.5*rho0*u0**2+m3.e_EOS(rho0)+m3.V_lock(rho0,A0), A0, Pi0])

    left_mask = x < XC
    right_mask = x >= XC
    t=0.0; step=0
    trace=[]
    single_peak_pre_collision = 0.0
    centroidL_hist=[]; centroidR_hist=[]

    while t < T_end:
        rho,u,Emed,A,Pi = m3.primitives(U)
        c_s = np.sqrt(np.maximum(m3.dPdrho(rho,A),1e-12))
        dt = cfl*dx/max(np.max(np.abs(u)+c_s), m3.c0)
        dt = min(dt, T_end-t)
        dUdt1,*_ = m3.rhs(U,dx); U1=U+dt*dUdt1
        if np.any(~np.isfinite(U1)):
            return dict(sigma=sigma,k_wave=k_wave,amp=amp,R_focus=None,note='blowup')
        dUdt2,*_ = m3.rhs(U1,dx); U2=0.5*U+0.5*(U1+dt*dUdt2)
        U=U2; t+=dt; step+=1
        if step % 20 == 0:
            rho,u,Emed,A,Pi = m3.primitives(U)
            e_avail,e_hdf = e_avail_field(rho,u,A,Pi,dx)
            cL = envelope_centroid(e_hdf,x,left_mask)
            cR = envelope_centroid(e_hdf,x,right_mask)
            centroidL_hist.append((t,cL)); centroidR_hist.append((t,cR))
            trace.append((t,e_avail.max(),x[np.argmax(e_avail)]))
            if cL is not None and cR is not None and (cR-cL) > 3*sigma:
                single_peak_pre_collision = max(single_peak_pre_collision, e_avail.max())

    diffs = [(tt,(cr-cl) if (cl is not None and cr is not None) else None) for (tt,cl),(_,cr) in zip(centroidL_hist,centroidR_hist)]
    valid = [(tt,d) for tt,d in diffs if d is not None]
    tC = min(valid, key=lambda p: abs(p[1]))[0] if valid else T_end/2
    window = 2*sigma/m3.c0
    win_trace = [(tt,pk,loc) for tt,pk,loc in trace if abs(tt-tC)<=window]
    collision_peak = max((pk for _,pk,_ in win_trace), default=0.0)
    R_focus = collision_peak/single_peak_pre_collision if single_peak_pre_collision>0 else float('nan')
    return dict(sigma=sigma, k_wave=k_wave, amp=float(amp), tC=float(tC),
                single_peak=float(single_peak_pre_collision), collision_peak=float(collision_peak),
                R_focus=float(R_focus))

if __name__ == "__main__":
    results = []
    for k_wave in [0, 0.25, 0.5, 1, 2]:
        for sigma in [3, 6, 12]:
            r = run_geometry_case(sigma, k_wave)
            results.append(r)
            print(f"k_wave={k_wave:.2f} sigma={sigma:2.0f}: {r}")

    valid = [r for r in results if r.get('R_focus') is not None]
    if valid:
        best = max(valid, key=lambda r: r['R_focus'])
        print()
        print(f"BEST geometry: k_wave={best['k_wave']}, sigma={best['sigma']}, R_focus={best['R_focus']:.4f}")
        focusing = [r for r in valid if r['R_focus']>1]
        print(f"Number of geometries with R_focus>1: {len(focusing)} / {len(valid)}")
    else:
        print("NO valid results.")

    with open(r"C:\Users\jaden\cosmology\PWC\knot_audit\geometry_sweep_audit.json","w") as f:
        json.dump(results, f, indent=2)
