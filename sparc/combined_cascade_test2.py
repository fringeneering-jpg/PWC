import numpy as np, time
from scipy.integrate import solve_ivp
from scipy.optimize import minimize, minimize_scalar
import cascade_universal_test as ct

G = 6.674e-11

def combined_predict(r, vb, c, a0):
    Mbar = r * vb**2 / G
    dMbar_dr = np.gradient(Mbar, r)
    gbar_curve = vb**2 / r
    def rhs(rr, Mmed):
        dmb = np.interp(rr, r, dMbar_dr)
        gb = np.interp(rr, r, gbar_curve)
        tension = 1.0 + (gb/a0)**(2/3)
        return (dmb + c*Mmed[0]/rr) / tension
    sol = solve_ivp(rhs, (r[0], r[-1]), [0.0], t_eval=r, method="RK23",
                     rtol=1e-4, max_step=(r[-1]-r[0])/40)
    Mmed = np.clip(sol.y[0], 0, None)
    return np.sqrt(G*(Mbar+Mmed)/r)

def combined_rms(gal_data, galaxies, c, a0):
    logs = []
    for g in galaxies:
        r, vb, vo = gal_data[g]
        try:
            vp = combined_predict(r, vb, c, a0)
        except Exception:
            continue
        resid = np.log10(vo) - np.log10(np.clip(vp, 1e-3, None))
        logs.append(np.sqrt(np.mean(resid**2)))
    return float(np.mean(logs)) if logs else np.inf

if __name__ == "__main__":
    t0 = time.time()
    gal_data = ct.load_sparc(".")
    galaxies = list(gal_data.keys())
    print(f"Galaxies: {len(galaxies)}  (load took {time.time()-t0:.1f}s)", flush=True)

    N_SEEDS = 5
    results = []
    for seed in range(N_SEEDS):
        ts = time.time()
        rng = np.random.default_rng(seed)
        idx = rng.permutation(len(galaxies))
        n_train = int(0.7*len(galaxies))
        train = [galaxies[i] for i in idx[:n_train]]
        holdout = [galaxies[i] for i in idx[n_train:]]

        obj = lambda p: combined_rms(gal_data, train, p[0], 10**p[1])
        res = minimize(obj, [0.7, -10.0], method="Nelder-Mead",
                        bounds=[(0.01,5.0),(-12.0,-8.0)],
                        options={"xatol":1e-2,"fatol":1e-4,"maxiter":80})
        c_fit, a0_fit = res.x[0], 10**res.x[1]
        rms_train = combined_rms(gal_data, train, c_fit, a0_fit)
        rms_hold  = combined_rms(gal_data, holdout, c_fit, a0_fit)
        res1 = minimize_scalar(lambda c: ct.galaxy_balanced_rms(gal_data, train, c),
                                bounds=(0.01,5.0), method="bounded", options={"xatol":1e-2})
        rms_hold_simple = ct.galaxy_balanced_rms(gal_data, holdout, res1.x)

        results.append((seed, c_fit, a0_fit, rms_train, rms_hold, rms_hold_simple))
        print(f"seed={seed}: c={c_fit:.3f} a0={a0_fit:.3e}  train={rms_train:.4f}  "
              f"holdout_combined={rms_hold:.4f}  holdout_simple={rms_hold_simple:.4f}  "
              f"[{time.time()-ts:.1f}s]", flush=True)

    hc = [r[4] for r in results]; hs = [r[5] for r in results]
    print()
    print(f"mean holdout combined (c+a0, 2-param): {np.mean(hc):.4f} +/- {np.std(hc):.4f}")
    print(f"mean holdout simple cascade (c only):   {np.mean(hs):.4f} +/- {np.std(hs):.4f}")
    print(f"combined beats simple cascade in {sum(h1<h2 for h1,h2 in zip(hc,hs))}/{N_SEEDS} seeds")
