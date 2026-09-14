"""
Domain W2 residual/convergence audit (2026-09-14).

Pure diagnostic pass on the ALREADY-fitted Domain W2 parameters (from
domain_W_reformulated_results.json) -- no re-optimization, no parameter
changes. Reuses domain_W_reformulated.py's exact data loader, train/holdout
split (same SEED=7), and solve_galaxy_bvp function unmodified.

Goal: characterize where the 101 converged solutions have their residual
error, and characterize the 40 non-convergent galaxies (26 train + 14
holdout) -- looking for whether either group clusters by galaxy mass, size,
radius range, or is broadly/randomly distributed instead.
"""
import numpy as np
import json
import sys

sys.path.insert(0, ".")
from domain_W_reformulated import (
    load_sparc_data, solve_galaxy_bvp, G, KPC, SEED
)

def main():
    with open("domain_W_reformulated_results.json") as f:
        res = json.load(f)
    up = res["universal_parameters"]
    rho0 = up["rho_0_kg_m3"]
    Gamma = up["Gamma_s_1"]
    tau_Pi = up["tau_Pi_s"]
    tau_pi = up["tau_pi_s"]
    zeta = up["zeta_Pa_s"]
    eta = up["eta_Pa_s"]
    c_s0_sq = up["c_s0_m_s"]**2
    p = [rho0, Gamma, tau_Pi, tau_pi, zeta, eta, c_s0_sq]
    print("Auditing FIXED, already-fitted W2 parameters (no re-optimization):")
    print(f"  rho_0={rho0:.3e} Gamma={Gamma:.3e} tau_Pi={tau_Pi:.3e} tau_pi={tau_pi:.3e}")
    print(f"  zeta={zeta:.3e} eta={eta:.3e} c_s0={np.sqrt(c_s0_sq):.3e}\n")

    galaxies = load_sparc_data()
    gal_names = sorted(list(galaxies.keys()))
    rng = np.random.default_rng(SEED)
    rng.shuffle(gal_names)
    split_idx = int(0.7 * len(gal_names))
    train_names = gal_names[:split_idx]
    holdout_names = gal_names[split_idx:]
    all_names = [(n, "train") for n in train_names] + [(n, "holdout") for n in holdout_names]

    converged = []
    failed = []

    for name, split in all_names:
        gal = galaxies[name]
        r_kpc = gal['r_m'] / KPC
        M_bar_tot = gal['M_bar'][-1] / 1.989e30  # Msun
        n_pts = len(r_kpc)
        try:
            g_HDF = solve_galaxy_bvp(gal, p)
        except Exception as e:
            g_HDF = None

        record = dict(name=name, split=split, r_min_kpc=float(r_kpc[0]), r_max_kpc=float(r_kpc[-1]),
                      n_pts=int(n_pts), M_bar_Msun=float(M_bar_tot), V_gal_kms=float(gal['V_gal_approx']/1000))

        if g_HDF is None:
            failed.append(record)
            continue
        g_pred = gal['g_bar'] + g_HDF
        mask = (g_pred > 0) & (gal['g_obs'] > 0)
        if mask.sum() == 0:
            failed.append(record)
            continue
        res_dex = np.log10(gal['g_obs'][mask]) - np.log10(g_pred[mask])
        rms = float(np.sqrt(np.mean(res_dex**2)))
        bias = float(np.mean(res_dex))  # signed: + means model under-predicts g_obs
        record.update(rms_dex=rms, bias_dex=bias)
        converged.append(record)

    print(f"Converged: {len(converged)}   Failed: {len(failed)}   Total: {len(converged)+len(failed)}\n")

    conv_rms = np.array([c["rms_dex"] for c in converged])
    conv_Mbar = np.array([c["M_bar_Msun"] for c in converged])
    conv_rmax = np.array([c["r_max_kpc"] for c in converged])
    conv_rmin = np.array([c["r_min_kpc"] for c in converged])
    conv_bias = np.array([c["bias_dex"] for c in converged])

    print("=== Converged-galaxy residual RMS vs galaxy properties ===")
    print(f"RMS range: {conv_rms.min():.3f} to {conv_rms.max():.3f} dex, median {np.median(conv_rms):.3f}")
    print(f"corr(rms, log10 M_bar)   = {np.corrcoef(conv_rms, np.log10(conv_Mbar))[0,1]:.3f}")
    print(f"corr(rms, r_max_kpc)     = {np.corrcoef(conv_rms, conv_rmax)[0,1]:.3f}")
    print(f"corr(rms, r_min_kpc)     = {np.corrcoef(conv_rms, conv_rmin)[0,1]:.3f}")
    print(f"mean signed bias (dex)   = {conv_bias.mean():.3f}  (+ = model under-predicts g_obs, i.e. not enough HDF gravity)")

    # worst 10 converged galaxies by RMS
    worst = sorted(converged, key=lambda c: -c["rms_dex"])[:10]
    print("\nWorst 10 converged galaxies by RMS:")
    for c in worst:
        print(f"  {c['name']:12s} split={c['split']:7s} rms={c['rms_dex']:.3f} bias={c['bias_dex']:+.3f} "
              f"M_bar={c['M_bar_Msun']:.2e} Msun  r=[{c['r_min_kpc']:.2f},{c['r_max_kpc']:.2f}] kpc  n_pts={c['n_pts']}")

    best = sorted(converged, key=lambda c: c["rms_dex"])[:10]
    print("\nBest 10 converged galaxies by RMS:")
    for c in best:
        print(f"  {c['name']:12s} split={c['split']:7s} rms={c['rms_dex']:.3f} bias={c['bias_dex']:+.3f} "
              f"M_bar={c['M_bar_Msun']:.2e} Msun  r=[{c['r_min_kpc']:.2f},{c['r_max_kpc']:.2f}] kpc  n_pts={c['n_pts']}")

    print("\n=== Failed galaxies: do they cluster by any property? ===")
    if failed:
        fail_Mbar = np.array([f["M_bar_Msun"] for f in failed])
        fail_rmax = np.array([f["r_max_kpc"] for f in failed])
        fail_rmin = np.array([f["r_min_kpc"] for f in failed])
        fail_npts = np.array([f["n_pts"] for f in failed])
        print(f"Failed M_bar range: {fail_Mbar.min():.2e} to {fail_Mbar.max():.2e} Msun, median {np.median(fail_Mbar):.2e}")
        print(f"Converged M_bar range: {conv_Mbar.min():.2e} to {conv_Mbar.max():.2e} Msun, median {np.median(conv_Mbar):.2e}")
        print(f"Failed r_max range: {fail_rmax.min():.2f} to {fail_rmax.max():.2f} kpc, median {np.median(fail_rmax):.2f}")
        print(f"Converged r_max range: {conv_rmax.min():.2f} to {conv_rmax.max():.2f} kpc, median {np.median(conv_rmax):.2f}")
        print(f"Failed r_min range: {fail_rmin.min():.3f} to {fail_rmin.max():.3f} kpc, median {np.median(fail_rmin):.3f}")
        print(f"Converged r_min range: {conv_rmin.min():.3f} to {conv_rmin.max():.3f} kpc, median {np.median(conv_rmin):.3f}")
        print(f"Failed n_pts range: {fail_npts.min()} to {fail_npts.max()}, median {np.median(fail_npts):.1f}")
        print(f"Converged n_pts range: {conv_Mbar.min():.0f}...")  # placeholder avoided below
        conv_npts = np.array([c["n_pts"] for c in converged])
        print(f"Converged n_pts range: {conv_npts.min()} to {conv_npts.max()}, median {np.median(conv_npts):.1f}")

        # Mann-Whitney-style simple check: what fraction of failed galaxies are below/above converged median?
        for label, farr, carr in [("M_bar", fail_Mbar, conv_Mbar), ("r_max", fail_rmax, conv_rmax),
                                    ("r_min", fail_rmin, conv_rmin), ("n_pts", fail_npts, conv_npts)]:
            frac_below = float((farr < np.median(carr)).mean())
            print(f"  fraction of FAILED galaxies below converged median {label}: {frac_below:.1%}")

        print("\nAll failed galaxy names, split, and properties:")
        for f in sorted(failed, key=lambda x: x["M_bar_Msun"]):
            print(f"  {f['name']:12s} split={f['split']:7s} M_bar={f['M_bar_Msun']:.2e} Msun  "
                  f"r=[{f['r_min_kpc']:.2f},{f['r_max_kpc']:.2f}] kpc  n_pts={f['n_pts']}")
    else:
        print("No failed galaxies.")

    out = dict(
        n_converged=len(converged), n_failed=len(failed),
        converged=converged, failed=failed,
        summary=dict(
            rms_median=float(np.median(conv_rms)), rms_min=float(conv_rms.min()), rms_max=float(conv_rms.max()),
            corr_rms_vs_logMbar=float(np.corrcoef(conv_rms, np.log10(conv_Mbar))[0,1]),
            corr_rms_vs_rmax=float(np.corrcoef(conv_rms, conv_rmax)[0,1]),
            corr_rms_vs_rmin=float(np.corrcoef(conv_rms, conv_rmin)[0,1]),
            mean_signed_bias=float(conv_bias.mean()),
        )
    )
    with open("domain_W2_residual_audit_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nresults -> domain_W2_residual_audit_results.json")

if __name__ == "__main__":
    main()
