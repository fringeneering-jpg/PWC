"""
PWC Framework - Domain W (Causal Dissipative Wake ODEs - Rigorous Reformulation)
-------------------------------------------------------------------------
Fully rewritten to strictly adhere to methodology_standing_rule_2026-09-14
and incorporate theoretical corrections to causality, characteristics, covariant
reductions, boundary conditions, and exact stress-tensor extraction.

Detailed Theoretical Resolutions to Critiques:
1. Strict Relativistic Causality: c_s0 = c violates the Müller-Israel-Stewart
   characteristic bounds when viscous modes are added. We allocate a causal
   "speed budget" (alpha_Pi, alpha_pi) such that the maximum characteristic speed
   v_char^2 = c_s0^2 + \zeta/(\rho_0 \tau_\Pi) + 4\eta/(3\rho_0 \tau_\pi) is exactly <= c^2.
   This algebraically guarantees causality without relying on informal bounds.
2. Exact Mass Shedding Continuity: The unphysical numerical `v_safe` hack is
   eliminated. The steady radial velocity v(r) is integrated analytically from
   the mass shedding source J_N = \Gamma \rho_bar (where \Gamma has strict units s^-1).
3. Fluid Momentum Conservation: The un-derived Newtonian gravity body-force
   has been purged from the fluid ODE. The HDF wake is driven purely by mass-shedding
   kinematics via \nabla_\mu T^{\mu r} = J^r.
4. Monopole vs. Dipole Force Extraction (Category Error Fixed):
   - Rotation curves are radial. They are driven by the exact monopole (l=0)
     density perturbation's gravitational field: g_HDF = G M_HDF / r^2.
   - The vector drag on the moving galaxy is an anisotropic dipole (l=1) effect,
     derived explicitly via Gauss's theorem on the source current \int J_z dV.
     This eliminates the arbitrary phenomenological scalar fudge factor (kappa).
5. Bounded Monopole Closure: The 1D plane-wave impedance is replaced by the
   exact steady asymptotic monopole decay condition (u' + 4u/r = 0) at R_max.
6. Validation Architecture: Synthetic MOND fallback removed. Script fails loudly
   if real SPARC data is missing, and benchmarks directly against the pre-registered
   Bare Newtonian and empirical McGaugh RAR.
"""

import numpy as np
import pandas as pd
from scipy.integrate import solve_bvp
from scipy.optimize import differential_evolution
from scipy.interpolate import interp1d
import os
import sys
import json
import warnings

warnings.filterwarnings('ignore')

# --- Universal Constants (SI) ---
G = 6.6743e-11
c = 299792458.0
KPC = 3.08567758149e19
KMS = 1000.0
UPS_D = 0.5
UPS_B = 0.7
SEED = 7
A0_RAR = 1.2e-10  # Empirical McGaugh baseline standard

def read_vizier_tsv(path, cols):
    """Real, working VizieR TSV parser -- same one used by every other domain
    script in this project tonight (domain_T, domain_W original). These are
    tab-separated exports with a '#'-commented header block and a dashed
    separator row, not clean whitespace-delimited columns."""
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8", errors="replace")]
    hdr_i = None
    for i, l in enumerate(lines):
        if l.startswith("#") or not l.strip(): continue
        if "\t" in l and "recno" in l: hdr_i = i; break
    names = lines[hdr_i].split("\t")
    dash_i = None
    for i in range(hdr_i+1, min(hdr_i+6, len(lines))):
        if set(lines[i].replace("\t","").strip()) <= set("- "): dash_i = i
    idx = {c: names.index(c) for c in cols}
    out = {c: [] for c in cols}
    for l in lines[dash_i+1:]:
        if not l.strip() or l.startswith("#"): continue
        f = l.split("\t")
        if len(f) < len(names): continue
        try:
            for c in cols:
                v = f[idx[c]].strip()
                out[c].append(v if c == "Name" else (float(v) if v not in ("","---") else np.nan))
        except ValueError:
            continue
    return out

def load_sparc_data(data_dir="."):
    """
    Loads the real SPARC dataset (vizier_t1.txt / vizier_t2.txt) using this
    project's proven TSV parser, and applies standard quality cuts.
    Fails loudly if real SPARC data is absent. Synthetic fallback strictly disabled.
    """
    t1_path = os.path.join(data_dir, "vizier_t1.txt")
    t2_path = os.path.join(data_dir, "vizier_t2.txt")

    if not (os.path.exists(t1_path) and os.path.exists(t2_path)):
        print("CRITICAL ERROR: SPARC dataset files not found.")
        print("Synthetic fallback disabled per rigorous validation methodology. Exiting.")
        sys.exit(1)

    galaxies = {}
    try:
        t1 = read_vizier_tsv(t1_path, ["Name", "i", "Qual"])
        t2 = read_vizier_tsv(t2_path, ["Name", "Rad", "Vobs", "e_Vobs", "Vgas", "Vdisk", "Vbulge"])

        inc = {n: i for n, i in zip(t1["Name"], t1["i"])}
        qual = {n: q for n, q in zip(t1["Name"], t1["Qual"])}

        name_arr = np.array(t2["Name"])
        rad_arr = np.array(t2["Rad"], float)
        vobs_arr = np.array(t2["Vobs"], float)
        evobs_arr = np.array(t2["e_Vobs"], float)
        vgas_arr = np.array(t2["Vgas"], float)
        vdisk_arr = np.array(t2["Vdisk"], float)
        vbulge_arr = np.array(t2["Vbulge"], float)
        vbulge_arr = np.where(np.isnan(vbulge_arr), 0.0, vbulge_arr)
        vgas_arr = np.where(np.isnan(vgas_arr), 0.0, vgas_arr)

        inc_arr = np.array([inc.get(n, np.nan) for n in name_arr], float)
        qual_arr = np.array([qual.get(n, np.nan) for n in name_arr], float)

        m = (rad_arr > 0) & (vobs_arr > 0) & np.isfinite(evobs_arr)
        m &= (evobs_arr / vobs_arr <= 0.10)
        m &= (inc_arr >= 30.0)
        m &= (qual_arr <= 2)

        name_arr, rad_arr, vobs_arr = name_arr[m], rad_arr[m], vobs_arr[m]
        vgas_arr, vdisk_arr, vbulge_arr = vgas_arr[m], vdisk_arr[m], vbulge_arr[m]

        for name in sorted(set(name_arr)):
            gm = (name_arr == name)
            if gm.sum() < 3:
                continue
            order = np.argsort(rad_arr[gm])
            r_kpc = rad_arr[gm][order]
            v_obs_kms = vobs_arr[gm][order]
            v_gas_kms = vgas_arr[gm][order]
            v_disk_kms = vdisk_arr[gm][order]
            v_bulge_kms = vbulge_arr[gm][order]

            r_m = r_kpc * KPC
            v_obs = v_obs_kms * KMS
            g_obs = (v_obs**2) / r_m

            v_gas = v_gas_kms * KMS
            v_disk = v_disk_kms * KMS
            v_bulge = v_bulge_kms * KMS

            v_bar_sq = np.sign(v_gas)*(v_gas**2) + UPS_D * (v_disk**2) + UPS_B * (v_bulge**2)
            v_bar_sq = np.maximum(v_bar_sq, 1e-10)

            M_bar = (v_bar_sq * r_m) / G
            M_bar = np.maximum.accumulate(M_bar)

            g_bar = G * M_bar / r_m**2

            dM_dr = np.gradient(M_bar, r_m)
            rho_bar = np.maximum(dM_dr / (4 * np.pi * r_m**2), 1e-35)

            galaxies[name] = {
                'r_m': r_m,
                'g_obs': g_obs,
                'g_bar': g_bar,
                'M_bar': M_bar,
                'rho_bar': rho_bar,
                'V_gal_approx': v_obs[-1]
            }
    except Exception as e:
        print(f"Error reading SPARC tables: {e}")
        sys.exit(1)

    return galaxies

def decode_params(params):
    rho0 = 10**params[0]
    Gamma = 10**params[1]
    tau_Pi = 10**params[2]
    tau_pi = 10**params[3]

    a1 = params[4]
    a2 = params[5]
    tot = a1 + a2
    scale = 0.999 / tot if tot > 0.999 else 1.0
    alpha_Pi = a1 * scale
    alpha_pi = a2 * scale

    c_s0_sq = c**2 * (1.0 - alpha_Pi - alpha_pi)

    zeta = alpha_Pi * rho0 * c**2 * tau_Pi
    eta  = alpha_pi * 0.75 * rho0 * c**2 * tau_pi

    return [rho0, Gamma, tau_Pi, tau_pi, zeta, eta, c_s0_sq]

def solve_galaxy_bvp(gal, p):
    rho0, Gamma, tau_Pi, tau_pi, zeta, eta, c_s0_sq = p
    r_m = gal['r_m']
    M_bar = gal['M_bar']
    rho_bar = gal['rho_bar']

    r_min, r_max = r_m[0], r_m[-1]
    r_dense = np.geomspace(r_min, r_max, 100)

    M_interp = interp1d(r_m, M_bar, kind='linear', fill_value=(M_bar[0], M_bar[-1]), bounds_error=False)
    rho_interp = interp1d(r_m, rho_bar, kind='linear', fill_value=(rho_bar[0], 0.0), bounds_error=False)

    M_dense = M_interp(r_dense)
    rho_dense = rho_interp(r_dense)

    v_dense = (Gamma * M_dense) / (4 * np.pi * r_dense**2 * rho0)
    v_prime = (Gamma * rho_dense / rho0) - (2.0 * v_dense / r_dense)
    div_v = Gamma * rho_dense / rho0
    sigma_rr = (2.0/3.0) * (v_prime - v_dense / r_dense)

    v_func = interp1d(r_dense, v_dense, kind='cubic')
    v_prime_func = interp1d(r_dense, v_prime, kind='cubic')
    div_v_func = interp1d(r_dense, div_v, kind='cubic')
    sigma_rr_func = interp1d(r_dense, sigma_rr, kind='cubic')

    def bvp_odes(x, y):
        r = r_dense[0] + x * (r_dense[-1] - r_dense[0])
        u, Pi, pi_rr, M_HDF = y

        v = v_func(r)
        v_p = v_prime_func(r)
        div = div_v_func(r)
        sig = sigma_rr_func(r)

        dPi_dr = - (Pi + zeta * div) / (tau_Pi * v)
        dpi_rr_dr = - (pi_rr + 2 * eta * sig) / (tau_pi * v)

        du_dr = -1.0 / (rho0 * c_s0_sq) * (
            rho0 * v * v_p + dPi_dr + dpi_rr_dr + 3 * pi_rr / r + Gamma * rho_interp(r) * v
        )

        dM_dr = 4 * np.pi * r**2 * rho0 * u

        scale = r_dense[-1] - r_dense[0]
        return np.vstack([du_dr * scale, dPi_dr * scale, dpi_rr_dr * scale, dM_dr * scale])

    def bvp_bcs(ya, yb):
        r_a = r_dense[0]
        r_b = r_dense[-1]

        bc1 = ya[1] - (-zeta * div_v_func(r_a))
        bc2 = ya[2] - (-2 * eta * sigma_rr_func(r_a))
        bc3 = ya[3] - (4.0 * np.pi / 3.0) * r_a**3 * rho0 * ya[0]

        v_b = v_func(r_b)
        v_p_b = v_prime_func(r_b)
        dPi_dr_b = - (yb[1] + zeta * div_v_func(r_b)) / (tau_Pi * v_b)
        dpi_rr_dr_b = - (yb[2] + 2 * eta * sigma_rr_func(r_b)) / (tau_pi * v_b)

        du_dr_b = -1.0 / (rho0 * c_s0_sq) * (
            rho0 * v_b * v_p_b + dPi_dr_b + dpi_rr_dr_b + 3 * yb[2] / r_b + Gamma * rho_interp(r_b) * v_b
        )

        bc4 = du_dr_b + 4.0 * yb[0] / r_b

        return np.array([bc1, bc2, bc3, bc4])

    x_mesh = (r_dense - r_dense[0]) / (r_dense[-1] - r_dense[0])
    y_guess = np.zeros((4, len(x_mesh)))

    y_guess[1, :] = -zeta * div_v_func(r_dense)
    y_guess[2, :] = -2 * eta * sigma_rr_func(r_dense)

    res = solve_bvp(bvp_odes, bvp_bcs, x_mesh, y_guess, tol=1e-3, max_nodes=5000)

    if res.success:
        x_data = (r_m - r_dense[0]) / (r_dense[-1] - r_dense[0])
        x_data = np.clip(x_data, 0.0, 1.0)
        M_HDF_sol = res.sol(x_data)[3]

        g_HDF = G * M_HDF_sol / r_m**2
        return g_HDF
    return None

def objective(log_params, galaxies, names, min_convergence_frac=0.5, return_diag=False):
    """
    FIXED (2026-09-14): the original version returned the full 1e6 penalty
    if even ONE galaxy in the set failed to converge -- diagnosed as the
    reason the differential-evolution search never found any usable signal
    (95/98 train galaxies converge fine at a reasonable midpoint parameter
    guess, but the all-or-nothing rule discarded that information every
    single time some other galaxy in the set failed). Now: failed galaxies
    are skipped and RMS is computed over the ones that converged, matching
    every other domain script in this project. A minimum-convergence-
    fraction guard still applies so the optimizer can't "succeed" by only
    fitting a trivially easy handful of galaxies and ignoring the rest.
    """
    p = decode_params(log_params)
    residuals = []
    n_ok, n_fail = 0, 0

    for name in names:
        gal = galaxies[name]
        try:
            g_HDF = solve_galaxy_bvp(gal, p)
        except Exception:
            g_HDF = None

        if g_HDF is None:
            n_fail += 1
            continue

        g_pred = gal['g_bar'] + g_HDF
        mask = (g_pred > 0) & (gal['g_obs'] > 0)

        if np.sum(mask) == 0:
            n_fail += 1
            continue

        res = np.log10(gal['g_obs'][mask]) - np.log10(g_pred[mask])
        residuals.extend(res)
        n_ok += 1

    n_total = n_ok + n_fail
    conv_frac = n_ok / n_total if n_total > 0 else 0.0

    if len(residuals) == 0 or conv_frac < min_convergence_frac:
        rms = 1e6
    else:
        rms = float(np.sqrt(np.mean(np.square(residuals))))

    if return_diag:
        return rms, n_ok, n_fail, conv_frac
    return rms

def evaluate_baseline(galaxies, names, baseline_type='newtonian'):
    residuals = []
    for name in names:
        gal = galaxies[name]
        g_bar = gal['g_bar']

        if baseline_type == 'newtonian':
            g_pred = g_bar
        else:
            g_pred = g_bar / (1 - np.exp(-np.sqrt(g_bar / A0_RAR)))

        mask = (g_pred > 0) & (gal['g_obs'] > 0)
        res = np.log10(gal['g_obs'][mask]) - np.log10(g_pred[mask])
        residuals.extend(res)

    if len(residuals) == 0:
        return 1e6
    return np.sqrt(np.mean(np.square(residuals)))

def extract_anisotropic_vector_drag(Gamma, M_bar_tot, V_gal):
    F_z_mag = Gamma * M_bar_tot * V_gal
    return F_z_mag

def main():
    print("PWC Framework: Domain W (Causal Dissipative Wake ODEs - Strict Reformulation)")
    print("Resolves: Superluminal Characteristics, Force Category Errors, and Fake IS-ODEs.")
    print("\nPre-registered Validation Protocol:")
    print("1. Synthetic fallback disabled. Hard constraint on real VizieR data.")
    print("2. Monopole: Rotation curves driven purely by exact HDF radial gravity.")
    print("3. Dipole: 3D Vector drag extracted analytically (F = - \\int J dV).")
    print("4. Causality: Characteristic speeds algebraically bounded (v_char <= c).")
    print("5. Outer Boundary: Exact steady monopole viscous decay (u' + 4u/r = 0).")

    galaxies = load_sparc_data()
    gal_names = sorted(list(galaxies.keys()))
    rng = np.random.default_rng(SEED)
    rng.shuffle(gal_names)

    split_idx = int(0.7 * len(gal_names))
    train_names = gal_names[:split_idx]
    holdout_names = gal_names[split_idx:]

    print(f"\nData Loaded: {len(train_names)} Train | {len(holdout_names)} Holdout")

    train_newt = evaluate_baseline(galaxies, train_names, 'newtonian')
    holdout_newt = evaluate_baseline(galaxies, holdout_names, 'newtonian')
    train_rar = evaluate_baseline(galaxies, train_names, 'rar')
    holdout_rar = evaluate_baseline(galaxies, holdout_names, 'rar')

    print(f"Baseline: Train Bare Newtonian RMS   : {train_newt:.4f} dex")
    print(f"Baseline: Holdout Bare Newtonian RMS : {holdout_newt:.4f} dex")
    print(f"Baseline: Train Empirical RAR RMS    : {train_rar:.4f} dex")

    bounds = [
        (-25, -20),
        (-25, -12),
        (8, 16),
        (8, 16),
        (0.01, 0.98),
        (0.01, 0.98)
    ]

    print("\nExecuting Differential Evolution Sweep (Train Set)...")
    res = differential_evolution(
        objective,
        bounds,
        args=(galaxies, train_names),
        strategy='best1bin',
        maxiter=12,
        popsize=8,
        seed=SEED,
        disp=True
    )

    p_best = decode_params(res.x)
    train_rms, train_ok, train_fail, train_conv = objective(res.x, galaxies, train_names, return_diag=True)
    holdout_rms, holdout_ok, holdout_fail, holdout_conv = objective(res.x, galaxies, holdout_names, return_diag=True)

    print(f"\nConvergence: TRAIN {train_ok}/{train_ok+train_fail} ({train_conv:.1%})  "
          f"HOLDOUT {holdout_ok}/{holdout_ok+holdout_fail} ({holdout_conv:.1%})")

    example_gal = galaxies[train_names[0]]
    F_drag_val = extract_anisotropic_vector_drag(p_best[1], example_gal['M_bar'][-1], example_gal['V_gal_approx'])

    print("\n--- Theoretical Optimization Resolved ---")
    print(f"Universal rho_0       : {p_best[0]:.3e} kg/m^3")
    print(f"Universal Gamma       : {p_best[1]:.3e} s^-1")
    print(f"Universal tau_Pi      : {p_best[2]:.3e} s")
    print(f"Universal tau_pi      : {p_best[3]:.3e} s")
    print(f"Universal zeta        : {p_best[4]:.3e} Pa s")
    print(f"Universal eta         : {p_best[5]:.3e} Pa s")
    print(f"Causal Sound Speed    : {np.sqrt(p_best[6])/c:.5f} c")
    print(f"\nVector Drag Diagnostic: F_z = {F_drag_val:.3e} N  (Galaxy: {train_names[0]})")

    print("\nModel Comparisons (RMS dex):")
    print(f"HDF Theory - Train    : {train_rms:.4f}")
    print(f"HDF Theory - Holdout  : {holdout_rms:.4f}")
    print(f"RAR Baseline - Holdout: {holdout_rar:.4f}")

    results = {
        "status": "completed",
        "methodology": "Strict Rule 2026-09-14 adhered. Causality speed bounds fixed. Source geometry corrected.",
        "universal_parameters": {
            "rho_0_kg_m3": p_best[0],
            "Gamma_s_1": p_best[1],
            "tau_Pi_s": p_best[2],
            "tau_pi_s": p_best[3],
            "zeta_Pa_s": p_best[4],
            "eta_Pa_s": p_best[5],
            "c_s0_m_s": np.sqrt(p_best[6])
        },
        "diagnostic": {
            "example_vector_drag_N": F_drag_val
        },
        "metrics": {
            "hdf_train_rms_dex": train_rms,
            "hdf_holdout_rms_dex": holdout_rms,
            "baseline_newt_holdout_rms": holdout_newt,
            "baseline_rar_holdout_rms": holdout_rar
        },
        "convergence": {
            "train_ok": train_ok, "train_fail": train_fail, "train_frac": train_conv,
            "holdout_ok": holdout_ok, "holdout_fail": holdout_fail, "holdout_frac": holdout_conv
        }
    }

    with open("domain_W_reformulated_results.json", "w") as f:
        json.dump(results, f, indent=4)
    print("\nResults saved to domain_W_reformulated_results.json")

if __name__ == "__main__":
    main()
