"""
PWC Stage 2 (corrected): does a propagating HDF (wave) energy pulse in the
baseline medium dynamically create and retain a bounded, rho_max-limited
matter knot when its local energy density crosses a declared locking
threshold -- and fail to do so when it doesn't?

phi is NOT a separately-advected/reacted field here. It is algebraically
slaved to the local, instantaneous energy density of the (rho,u) state:

    e_avail(x,t) = (1/2) rho u^2 + [e_EOS(rho) - e_EOS(rho_bg)]
    E_lock       = rho_knot * c_med^2
    phi_eq       = 0.5*(1 + tanh((e_avail - E_lock)/delta_E))

phi has no independent inertia/PDE of its own -- it is recomputed every
stage from the current (rho,u), then fed into the SAME pressure law and
Korteweg stress used throughout this project (P, e_bulk derived
symbolically in dynamic_knot_solver.py from the declared energy
functional). Only (rho, rho*u) are evolved/conserved fields.

No artificial relaxation, no damping, no thermal-channel bookkeeping, no
energy renormalization: E_total(t) is tracked and reported as a genuine
diagnostic, not forced to be constant.
"""
import numpy as np
import dynamic_knot_solver as dks
import json, time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUTDIR = r"C:\Users\jaden\cosmology\PWC\knot_audit"

PARAMS = dks.PARAMS
K = dks.K

def e_EOS(rho):
    A, rho_max = PARAMS['A'], PARAMS['rho_max']
    return A*(-np.log(1-rho/rho_max) - rho/rho_max)

# ---- declared, frozen constants (computed once from the existing PARAMS,
#      not tuned to produce any particular outcome) ----
_rho_bg_arr = np.array([PARAMS['rho_bg']])
c_med = float(np.sqrt(dks.eos_dPdrho(_rho_bg_arr, np.array([0.0]))[0]))
rho_knot = PARAMS['rho_bg'] + PARAMS['drho']
E_lock = rho_knot * c_med**2
delta_E = 0.05 * E_lock   # smoothing width, frozen fraction of E_lock
e_EOS_bg = e_EOS(PARAMS['rho_bg'])

print(f"[frozen constants] c_med={c_med:.6f}  rho_knot={rho_knot:.4f}  "
      f"E_lock={E_lock:.6f}  delta_E={delta_E:.6f}")

def e_avail_of(rho, u):
    return 0.5*rho*u**2 + (e_EOS(rho) - e_EOS_bg)

def phi_eq_of(rho, u):
    e_avail = e_avail_of(rho, u)
    return 0.5*(1.0 + np.tanh((e_avail - E_lock)/delta_E))

def grad_periodic(f, dx):
    return (np.roll(f,-1) - np.roll(f,1)) / (2*dx)

def primitives(U):
    rho = U[0]
    u = U[1]/rho
    return rho, u

def rhs(U, dx):
    rho, u = primitives(U)
    phi = phi_eq_of(rho, u)
    dphidx = grad_periodic(phi, dx)
    P = dks.eos_P(rho, phi)
    Txx = P + 0.5*K*dphidx**2

    F0 = rho*u
    F1 = rho*u**2 + Txx
    F = np.array([F0, F1])

    c_s = np.sqrt(np.maximum(dks.eos_dPdrho(rho, phi), 1e-12))
    Smax_cell = np.abs(u) + c_s
    Smax_face = np.maximum(Smax_cell, np.roll(Smax_cell,-1))

    U_L = U
    U_R = np.roll(U, -1, axis=1)
    F_L = F
    F_R = np.roll(F, -1, axis=1)

    F_face = 0.5*(F_L+F_R) - 0.5*Smax_face*(U_R-U_L)
    dUdt = -(F_face - np.roll(F_face,1,axis=1))/dx
    return dUdt, rho, u, phi

def energy_channels(U, dx):
    rho, u = primitives(U)
    phi = phi_eq_of(rho, u)
    dphidx = grad_periodic(phi, dx)
    e_kin = 0.5*rho*u**2
    e_eos = e_EOS(rho)
    e_coupling = PARAMS['Lam']*phi**2*(1-phi)**2 + 0.5*PARAMS['B']*(rho-PARAMS['rho_bg']-PARAMS['drho']*phi)**2
    e_grad = 0.5*K*dphidx**2
    return dict(
        E_kinetic=np.sum(e_kin)*dx,
        E_EOS=np.sum(e_eos)*dx,
        E_coupling=np.sum(e_coupling)*dx,
        E_gradient=np.sum(e_grad)*dx,
        E_total=np.sum(e_kin+e_eos+e_coupling+e_grad)*dx,
    )

def measure_R(phi, dx):
    idx = np.where(phi >= 0.5)[0]
    if len(idx) == 0:
        return 0.0
    return 0.5*dx*len(idx)

def make_pulse(Nx, L, x0, w, drho_pulse):
    dx = L/Nx
    x = (np.arange(Nx)+0.5)*dx
    rho0 = PARAMS['rho_bg'] + drho_pulse*np.exp(-((x-x0)/w)**2)
    u0 = c_med * (rho0 - PARAMS['rho_bg'])/PARAMS['rho_bg']   # simple-wave, right-moving
    return x, dx, rho0, u0

def peak_e_avail(rho0, u0):
    return np.max(e_avail_of(rho0, u0))

def run_case(label, Nx, L, x0, w, drho_pulse, T_end, cfl=0.3, save_every=20):
    x, dx, rho0, u0 = make_pulse(Nx, L, x0, w, drho_pulse)
    U = np.array([rho0, rho0*u0])
    peak_ea = peak_e_avail(rho0, u0)
    print(f"[{label}] peak e_avail={peak_ea:.6f} vs E_lock={E_lock:.6f}  "
          f"({'ABOVE' if peak_ea>=E_lock else 'below'} threshold)")

    t = 0.0
    step = 0
    hist = dict(t=[], E_total=[], E_kinetic=[], E_EOS=[], E_coupling=[], E_gradient=[],
                M=[], Rknot=[], rhomax=[], phimax=[])
    E0 = energy_channels(U, dx)['E_total']
    M0 = np.sum(U[0])*dx

    while t < T_end:
        rho, u = primitives(U)
        c_s = np.sqrt(np.maximum(dks.eos_dPdrho(rho, phi_eq_of(rho,u)), 1e-12))
        dt = cfl*dx/np.max(np.abs(u)+c_s+1e-12)
        dt = min(dt, T_end-t)
        ok = False
        for attempt in range(10):
            dUdt1, *_ = rhs(U, dx)
            U1 = U + dt*dUdt1
            if np.any(U1[0] >= PARAMS['rho_max']*0.999) or np.any(U1[0] <= 0) or np.any(~np.isfinite(U1[0])):
                dt *= 0.5; continue
            dUdt2, *_ = rhs(U1, dx)
            U2 = 0.5*U + 0.5*(U1 + dt*dUdt2)
            if np.any(U2[0] >= PARAMS['rho_max']*0.999) or np.any(U2[0] <= 0) or np.any(~np.isfinite(U2[0])):
                dt *= 0.5; continue
            ok = True; break
        if not ok:
            print(f"  [{label}] [FAIL] rho hit rho_max boundary repeatedly at t={t:.4f}")
            break
        U = U2; t += dt; step += 1

        if step % save_every == 0:
            rho, u = primitives(U)
            phi = phi_eq_of(rho, u)
            ech = energy_channels(U, dx)
            hist['t'].append(t)
            for k in ('E_total','E_kinetic','E_EOS','E_coupling','E_gradient'):
                hist[k].append(ech[k])
            hist['M'].append(np.sum(rho)*dx)
            hist['Rknot'].append(measure_R(phi, dx))
            hist['rhomax'].append(rho.max())
            hist['phimax'].append(phi.max())

    for k in hist: hist[k] = np.array(hist[k])
    return dict(label=label, x=x, dx=dx, U_final=U, hist=hist, E0=E0, M0=M0,
                peak_e_avail=peak_ea, final_t=t)

def summarize(res):
    hist = res['hist']
    if len(hist['t']) == 0:
        print(f"  [{res['label']}] NO DATA -- failed immediately")
        return
    E_drift = np.abs(hist['E_total']-res['E0'])/res['E0']
    M_drift = np.abs(hist['M']-res['M0'])/res['M0']
    print(f"  [{res['label']}] reached t={hist['t'][-1]:.2f}/{res['final_t']:.2f} target, "
          f"peak_e_avail/E_lock={res['peak_e_avail']/E_lock:.3f}")
    print(f"    E_total drift: max={E_drift.max():.4e}, final={E_drift[-1]:.4e}")
    print(f"    mass drift:   max={M_drift.max():.4e}")
    print(f"    rho_max reached: {hist['rhomax'].max():.4f} (limit {PARAMS['rho_max']})")
    print(f"    phi_max reached: {hist['phimax'].max():.4f}")
    print(f"    R_knot(t): mean={hist['Rknot'].mean():.4f}, std={hist['Rknot'].std():.4f}, "
          f"final={hist['Rknot'][-1]:.4f}, max={hist['Rknot'].max():.4f}")
    # retained knot at end of run = phi still >=0.5 somewhere at final time
    retained = hist['Rknot'][-1] > 0.0
    print(f"    RETAINED LOCKED REGION AT FINAL TIME: {retained}")

if __name__ == "__main__":
    t0 = time.time()
    Nx = 1024
    L = 60.0
    x0 = L/4
    w = 2.0
    T_end = 100.0

    print("=== calibrating pulse amplitudes against E_lock ===")
    candidates = np.linspace(0.02, 0.5, 25)
    for da in candidates:
        _, _, rho0, u0 = make_pulse(Nx, L, x0, w, da)
        pea = peak_e_avail(rho0, u0)
        flag = "ABOVE" if pea >= E_lock else "below"
        print(f"  drho_pulse={da:.4f}: peak_e_avail={pea:.6f} ({flag})")

    # frozen amplitudes, chosen only from the threshold-crossing scan above
    DRHO_A = 0.30   # sub-threshold (peak_e_avail/E_lock ~ 0.47)
    DRHO_B = 0.46   # super-threshold (peak_e_avail/E_lock ~ 1.33)

    print(f"\n=== TEST A (sub-threshold, drho_pulse={DRHO_A}) ===")
    resA = run_case("A-subthreshold", Nx, L, x0, w, DRHO_A, T_end)
    summarize(resA)

    print(f"\n=== TEST B (super-threshold, drho_pulse={DRHO_B}) ===")
    resB = run_case("B-superthreshold", Nx, L, x0, w, DRHO_B, T_end)
    summarize(resB)

    print(f"\ntotal wall time: {time.time()-t0:.1f}s")

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    for res, color in [(resA, 'tab:blue'), (resB, 'tab:red')]:
        h = res['hist']
        if len(h['t']) == 0: continue
        axes[0,0].plot(h['t'], h['Rknot'], color=color, label=res['label'])
        axes[0,1].plot(h['t'], np.abs(h['E_total']-res['E0'])/res['E0'], color=color, label=res['label'])
        axes[0,2].plot(h['t'], h['rhomax'], color=color, label=res['label'])
        axes[1,0].plot(h['t'], h['phimax'], color=color, label=res['label'])
        axes[1,1].plot(h['t'], h['E_kinetic'], color=color, linestyle='-', label=f"{res['label']} Ekin")
        axes[1,1].plot(h['t'], h['E_coupling'], color=color, linestyle='--', label=f"{res['label']} Ecoup")
        axes[1,2].plot(h['t'], np.abs(h['M']-res['M0'])/res['M0'], color=color, label=res['label'])
    axes[0,0].set_title('R_knot(t)'); axes[0,0].legend(fontsize=7)
    axes[0,1].set_title('|E_total(t)-E0|/E0'); axes[0,1].set_yscale('log')
    axes[0,2].set_title('max rho(t)'); axes[0,2].axhline(PARAMS['rho_max'], ls=':', color='k')
    axes[1,0].set_title('max phi(t)')
    axes[1,1].set_title('E_kinetic (solid) / E_coupling (dashed)'); axes[1,1].legend(fontsize=6)
    axes[1,2].set_title('|M(t)-M0|/M0')
    plt.tight_layout()
    plt.savefig(f"{OUTDIR}/stage2_HDF_existence.png", dpi=130)
    print("plot saved")

    with open(f"{OUTDIR}/stage2_HDF_results.json", "w") as f:
        json.dump(dict(
            E_lock=E_lock, c_med=c_med, rho_knot=rho_knot, delta_E=delta_E,
            A=dict(drho_pulse=DRHO_A, peak_e_avail=resA['peak_e_avail'],
                   final_t=float(resA['hist']['t'][-1]) if len(resA['hist']['t']) else None,
                   E_drift_max=float(np.abs(resA['hist']['E_total']-resA['E0']).max()/resA['E0']) if len(resA['hist']['t']) else None,
                   Rknot_final=float(resA['hist']['Rknot'][-1]) if len(resA['hist']['t']) else None,
                   rhomax_reached=float(resA['hist']['rhomax'].max()) if len(resA['hist']['t']) else None),
            B=dict(drho_pulse=DRHO_B, peak_e_avail=resB['peak_e_avail'],
                   final_t=float(resB['hist']['t'][-1]) if len(resB['hist']['t']) else None,
                   E_drift_max=float(np.abs(resB['hist']['E_total']-resB['E0']).max()/resB['E0']) if len(resB['hist']['t']) else None,
                   Rknot_final=float(resB['hist']['Rknot'][-1]) if len(resB['hist']['t']) else None,
                   rhomax_reached=float(resB['hist']['rhomax'].max()) if len(resB['hist']['t']) else None),
        ), f, indent=2)
    print("results saved to stage2_HDF_results.json")
