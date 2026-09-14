"""
Stage 2: given a relaxed near-equilibrium initial state, run the real
conservative dynamics for many crossing times and check whether the knot
is a genuine bounded, stable structure -- not just "still visible."

Pass criteria (declared before running, per the spec):
  - finite core radius 0<R(t)<inf for all t
  - never crosses rho_max
  - no secular spread to the full box
  - no collapse to grid scale
  - bounded oscillation: R(t) = Rbar + dR(t), dR/Rbar stays bounded
  - conserved mass/momentum/energy at stated tolerance
  - convergent under Nx=512,1024,2048
"""
import numpy as np
import dynamic_knot_solver as dks
import json, time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUTDIR = r"C:\Users\jaden\cosmology\PWC\knot_audit"

def relax_to_equilibrium(Nx, L=40.0, R0=3.0, delta_wall=1.0, gamma=2.0, T_relax=1000.0, cfl=0.3):
    dx = L/Nx
    x = (np.arange(Nx)+0.5)*dx
    x0 = L/2
    phi0 = 0.5*(1-np.tanh((np.abs(x-x0)-R0)/delta_wall))
    rho0 = dks.PARAMS['rho_bg'] + dks.PARAMS['drho']*phi0
    U = np.array([rho0, rho0*0.0, rho0*phi0])
    t = 0.0
    while t < T_relax:
        rho, u, phi = dks.primitives(U)
        c_s = np.sqrt(np.maximum(dks.eos_dPdrho(rho, phi), 1e-12))
        dt = cfl*dx/np.max(np.abs(u)+c_s+1e-12)
        dt = min(dt, T_relax-t)
        dUdt, *_ = dks.rhs(U, dx)
        dUdt[1] = dUdt[1] - gamma*U[1]
        U_new = U + dt*dUdt
        if np.any(U_new[0] >= dks.PARAMS['rho_max']*0.999) or np.any(U_new[0]<=0):
            dt *= 0.5
            U_new = U + dt*dUdt
        U = U_new
        t += dt
    return U, x, dx

def measure_R(phi, dx):
    idx = np.where(phi >= 0.5)[0]
    if len(idx) == 0:
        return 0.0
    return 0.5*dx*len(idx)

def run_conservative(U0, dx, T_end, cfl=0.3, save_every=20):
    U = U0.copy()
    t = 0.0
    hist = dict(t=[], M=[], Pnet=[], E=[], Rknot=[], rhomax=[])
    E0,_ = dks.total_energy(U, dx)
    step = 0
    while t < T_end:
        rho, u, phi = dks.primitives(U)
        c_s = np.sqrt(np.maximum(dks.eos_dPdrho(rho, phi), 1e-12))
        dt = cfl*dx/np.max(np.abs(u)+c_s+1e-12)
        dt = min(dt, T_end-t)
        ok = False
        for attempt in range(10):
            dUdt1, *_ = dks.rhs(U, dx)
            U1 = U + dt*dUdt1
            if np.any(U1[0] >= dks.PARAMS['rho_max']*0.999) or np.any(U1[0] <= 0):
                dt *= 0.5; continue
            dUdt2, *_ = dks.rhs(U1, dx)
            U2 = 0.5*U + 0.5*(U1 + dt*dUdt2)
            if np.any(U2[0] >= dks.PARAMS['rho_max']*0.999) or np.any(U2[0] <= 0) or np.any(~np.isfinite(U2[0])):
                dt *= 0.5; continue
            ok = True; break
        if not ok:
            print(f"  [FAIL] rho hit boundary repeatedly at t={t:.3f}")
            break
        U = U2; t += dt; step += 1
        if step % save_every == 0:
            rho, u, phi = dks.primitives(U)
            Et,_ = dks.total_energy(U, dx)
            hist['t'].append(t)
            hist['M'].append(np.sum(rho)*dx)
            hist['Pnet'].append(np.sum(rho*u)*dx)
            hist['E'].append(Et)
            hist['Rknot'].append(measure_R(phi, dx))
            hist['rhomax'].append(rho.max())
    for k in hist: hist[k] = np.array(hist[k])
    return U, hist, E0

if __name__ == "__main__":
    print("=== STAGE 2: long conservative run from relaxed state, Nx=512, T_end=200 ===")
    t0 = time.time()
    Nx = 512
    U_eq, x, dx = relax_to_equilibrium(Nx=Nx, T_relax=1000.0)
    print(f"relaxation done ({time.time()-t0:.1f}s)")
    U_final, hist, E0 = run_conservative(U_eq, dx, T_end=200.0, cfl=0.3)
    print(f"total wall time: {time.time()-t0:.1f}s")

    if len(hist['t']) > 0:
        E_drift = np.abs(hist['E']-E0)/E0
        M_drift = np.abs(hist['M']-hist['M'][0])/hist['M'][0]
        Rbar = np.mean(hist['Rknot'])
        dR = hist['Rknot'] - Rbar
        print(f"final t reached: {hist['t'][-1]:.2f} / 200.0")
        print(f"energy drift: max={E_drift.max():.4e}, final={E_drift[-1]:.4e}")
        print(f"mass drift: max={M_drift.max():.4e}")
        print(f"R_knot: mean={Rbar:.4f}, std={np.std(dR):.4f}, min={hist['Rknot'].min():.4f}, max={hist['Rknot'].max():.4f}")
        print(f"rho_max reached: {hist['rhomax'].max():.4f} (limit is {dks.PARAMS['rho_max']})")
        print(f"relative R oscillation (std/mean): {np.std(dR)/Rbar if Rbar>0 else float('nan'):.4f}")

        fig, axes = plt.subplots(2,2, figsize=(11,8))
        axes[0,0].plot(hist['t'], hist['Rknot']); axes[0,0].set_title('R_knot(t)'); axes[0,0].set_xlabel('t')
        axes[0,1].plot(hist['t'], E_drift); axes[0,1].set_title('|E(t)-E0|/E0'); axes[0,1].set_yscale('log')
        axes[1,0].plot(hist['t'], hist['rhomax']); axes[1,0].axhline(dks.PARAMS['rho_max'],ls=':',color='r')
        axes[1,0].set_title('max rho(t)')
        axes[1,1].plot(hist['t'], M_drift); axes[1,1].set_title('|M(t)-M0|/M0')
        plt.tight_layout()
        plt.savefig(f"{OUTDIR}/stage2_existence_Nx{Nx}.png", dpi=130)
        print(f"\nplot saved")
    else:
        print("NO DATA -- simulation failed immediately")
