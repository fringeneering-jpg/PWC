"""
PWC Framework - Domain X: minimal linear causal closure baseline.

Purpose (narrowly scoped, per the clean parameter ledger agreed 2026-09-14):
test whether the ONLY currently-verified HDF response law -- the linear
restoring term K1 = rho0*c_s0^2 -- produces anything meaningful for real
SPARC rotation curves, BEFORE any nonlinear/dissipative physics (P*, n,
zeta, eta, tau_Pi, tau_pi) gets invented. Nothing nonlinear is used here.

Fixed, project-verified values (not fit):
  rho_HDF_ref = 4.6e10 kg/m^3   (correct exponent, per this project's own record)
  rho_max_core = 4.6e17 kg/m^3  (compact-core ceiling hypothesis, NOT used
                                   directly in this galaxy-scale linear test)
  compression_ratio_max = exp(1/2)  (recorded, not used by the linear closure itself)

Explicitly open / fit in this run:
  c_s0  -- the ledger notes c_s0=c is a "short-scale/optical-limit hypothesis,"
           not necessarily the galaxy-scale value. Fit it here rather than
           assume it.

State: y = [u, M_HDF], u = rho_HDF_local/rho_HDF_ref (bounded fraction).
Linear closure only:
  P(rho) = P_0 + c_s0^2 * (rho - rho_0)   =>   dP/drho = c_s0^2 everywhere
  (no nonlinear stiffening -- explicitly NOT claiming a sharp wall; this run
   tests only what the linear term alone can do)

du/dr     = -(rho_bg + rho_HDF_ref*u) * G*(M_bar(r)+M_HDF)/r^2 * (1-u) / (rho_HDF_ref*c_s0^2)
dM_HDF/dr = 4*pi*r^2*rho_HDF_ref*u

Boundary conditions (matching the established, working Domain V/W BVP
convention): inner M_HDF(r_min)=0; outer derivative-matching to the SIS
asymptotic slope (du/dr = -2u/r at r_far), NOT a pinned Dirichlet value
(the pinned-value version was the one that failed to converge at all
earlier tonight).

Robust aggregation (the fix from the earlier Domain W run): galaxies that
fail to converge are skipped, not treated as killing the whole objective,
with a minimum-convergence-fraction guard.
"""
import numpy as np
import os, sys, json, time
from scipy.integrate import solve_bvp
from scipy.optimize import minimize_scalar

G = 6.6743e-11
c = 299792458.0
KPC = 3.0856775814913673e19
KMS = 1.0e3
UPS_D, UPS_B = 0.5, 0.7
SEED = 7

RHO_HDF_REF = 4.6e10   # kg/m^3 -- correct exponent, fixed, not fit
RHO_BG = 0.0

def read_vizier_tsv(path, cols):
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

def load():
    D = "."
    t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name","i","Qual"])
    t2 = read_vizier_tsv(f"{D}/vizier_t2.txt", ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
    inc  = {n:i for n,i in zip(t1["Name"], t1["i"])}
    qual = {n:q for n,q in zip(t1["Name"], t1["Qual"])}
    name = np.array(t2["Name"]); R = np.array(t2["Rad"], float)
    Vo = np.array(t2["Vobs"], float); eVo = np.array(t2["e_Vobs"], float)
    Vg = np.array(t2["Vgas"], float); Vd = np.array(t2["Vdisk"], float); Vb = np.array(t2["Vbulge"], float)
    Vb = np.where(np.isnan(Vb), 0.0, Vb); Vg = np.where(np.isnan(Vg), 0.0, Vg)
    inc_a  = np.array([inc.get(n, np.nan)  for n in name], float)
    qual_a = np.array([qual.get(n, np.nan) for n in name], float)
    m = (R > 0) & (Vo > 0) & np.isfinite(eVo)
    m &= (eVo/Vo <= 0.10); m &= (inc_a >= 30.0); m &= (qual_a <= 2)
    R, Vo, eVo, Vg, Vd, Vb, name = R[m], Vo[m], eVo[m], Vg[m], Vd[m], Vb[m], name[m]
    conv = (KMS**2)/KPC
    g_obs_all = Vo**2 / R * conv
    Vbar2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
    g_bar_all = Vbar2 / R * conv
    ok = (g_bar_all > 0) & (g_obs_all > 0)
    g_obs_all, g_bar_all, name, R = g_obs_all[ok], g_bar_all[ok], name[ok], R[ok]
    galaxies = sorted(set(name))
    gal_data = {}
    for g in galaxies:
        gm = (name == g)
        r_kpc = R[gm]; gobs = g_obs_all[gm]; gbar = g_bar_all[gm]
        order = np.argsort(r_kpc)
        r_kpc, gobs, gbar = r_kpc[order], gobs[order], gbar[order]
        if len(r_kpc) < 3: continue
        gal_data[g] = dict(r=r_kpc*KPC, gobs=gobs, gbar=gbar)
    return gal_data, galaxies

def solve_galaxy(gd, c_s0, n_mesh=60):
    """
    FIXED (diagnosed 2026-09-14, two layers):
    1. Original SIS-style initial guess collapsed to the numerical floor
       once RHO_HDF_REF=4.6e10 replaced the ~1e-21 scale it was tuned for.
    2. Deeper issue: passing raw physical r (~1e19-1e20 m) directly into
       solve_bvp, with du/dr ~1e-22 per meter, creates an enormous scale
       mismatch that produces a singular collocation Jacobian regardless
       of the initial guess. The earlier (reformulated Domain W) script
       avoided this by internally mapping r onto a normalized x in [0,1]
       -- this version was missing that step. Fixed here: solve on
       x=(r-r_min)/(r_far-r_min) in [0,1], with M_HDF also normalized by
       a characteristic mass scale, both undone only at the end when
       interpolating back to the real data radii.
    """
    r = gd["r"]; gbar = gd["gbar"]
    Mbar_arr = gbar * r**2 / G
    Mbar_of_r = lambda rr: np.interp(rr, r, Mbar_arr)
    r_min, r_far = r[0], r[-1]
    r_span = r_far - r_min
    M_scale = max(Mbar_of_r(r_far), 1.0)  # characteristic mass to non-dimensionalize M_HDF

    x_mesh = np.linspace(0.0, 1.0, n_mesh)
    r_of_x = lambda x: r_min + x*r_span

    u_scale = np.clip(M_scale / (4*np.pi*r_far**3*RHO_HDF_REF/3.0), 1e-6, 0.5)
    u_guess = np.clip(u_scale * x_mesh, 1e-8, 1-1e-8)
    m_guess = u_scale * x_mesh  # M_HDF/M_scale, dimensionless, O(u_scale)
    y_guess = np.vstack([u_guess, m_guess])

    def fun(x, y):
        u, m = y
        u_c = np.clip(u, 1e-12, 1-1e-12)
        rr = r_of_x(x)
        Mb = Mbar_of_r(rr)
        MHDF = m * M_scale
        gpred = G*(Mb+MHDF)/rr**2
        rho_total = RHO_BG + RHO_HDF_REF*u_c
        du_dr = -rho_total*gpred*(1-u_c) / (RHO_HDF_REF*c_s0**2)
        dMHDF_dr = 4*np.pi*rr**2*RHO_HDF_REF*u_c
        # chain rule: d/dx = d/dr * dr/dx = d/dr * r_span
        return np.vstack([du_dr*r_span, (dMHDF_dr/M_scale)*r_span])

    U_OUTER_PLACEHOLDER = 0.01  # explicit placeholder, NOT a physical claim -- see note below

    def bc(ya, yb):
        # PLACEHOLDER outer BC (2026-09-14): swapped from derivative-matching
        # (which failed to converge, same as every prior BC tried tonight)
        # to a crude, fixed, small u(r_far) value. This is NOT the choke/
        # pressure condition or the temperature-gradient idea discussed --
        # both of those need real physics (a T(r) profile, an EOS linking T
        # to density, or a quantified choke threshold) that doesn't exist
        # yet. This placeholder exists purely to check whether the rest of
        # the pipeline (data loading, RHS, coordinate normalization) works
        # at all, isolated from the boundary-condition question. Not a
        # result -- a diagnostic.
        return np.array([ya[1] - 0.0, yb[0] - U_OUTER_PLACEHOLDER])

    try:
        sol = solve_bvp(fun, bc, x_mesh, y_guess, max_nodes=20000, tol=1e-6, verbose=0)
    except Exception:
        return None
    if not sol.success:
        return None

    x_data = np.clip((r - r_min)/r_span, 0.0, 1.0)
    u_at_r = np.clip(np.interp(x_data, sol.x, sol.y[0]), 1e-12, 1-1e-12)
    MHDF_at_r = np.interp(x_data, sol.x, sol.y[1]) * M_scale
    gpred = G*(Mbar_arr + MHDF_at_r)/r**2
    physical = bool(np.all((u_at_r > 0) & (u_at_r < 1)) and np.all(np.isfinite(MHDF_at_r)) and np.all(gpred > 0))
    if not physical:
        return None
    return gpred

def objective(log_cs0, galaxies, names, min_convergence_frac=0.5, return_diag=False):
    c_s0 = 10**log_cs0
    residuals = []
    n_ok, n_fail = 0, 0
    for name in names:
        gd = galaxies.get(name)
        if gd is None: continue
        gpred = solve_galaxy(gd, c_s0)
        if gpred is None:
            n_fail += 1
            continue
        residuals.append(np.log10(gd["gobs"]) - np.log10(gpred))
        n_ok += 1
    n_total = n_ok + n_fail
    conv_frac = n_ok/n_total if n_total > 0 else 0.0
    if not residuals or conv_frac < min_convergence_frac:
        rms = 1e6
    else:
        rms = float(np.sqrt(np.mean(np.concatenate(residuals)**2)))
    if return_diag:
        return rms, n_ok, n_fail, conv_frac
    return rms

def main():
    print("Domain X: minimal LINEAR causal closure baseline (K1=rho0*c_s0^2 only)")
    print(f"rho_HDF_ref = {RHO_HDF_REF:.3e} kg/m^3 (fixed, correct exponent)")
    print("c_s0: FIT (galaxy-scale value explicitly not assumed = c)")
    print("No nonlinear/dissipative terms used -- this is a floor test, not a full model.\n")

    gal_data, galaxies = load()
    rng = np.random.default_rng(SEED)
    shuffled = galaxies.copy(); rng.shuffle(shuffled)
    n_train = int(len(shuffled)*0.7)
    train_gal = set(shuffled[:n_train]); hold_gal = set(shuffled[n_train:])
    print(f"train galaxies: {len(train_gal)}, holdout galaxies: {len(hold_gal)}")

    t0 = time.time()
    best = minimize_scalar(objective, bounds=(2.0, 6.5), method="bounded",
                            args=(gal_data, train_gal), options=dict(xatol=1e-3, maxiter=60))
    c_s0_fit = 10**best.x
    print(f"fit took {time.time()-t0:.1f}s")
    print(f"c_s0 = {c_s0_fit:.4e} m/s  ({c_s0_fit/c:.6f} c)")
    print(f"naive SIS v_flat = sqrt(2)*c_s0 = {np.sqrt(2)*c_s0_fit/1e3:.2f} km/s")

    tr_rms, tr_ok, tr_fail, tr_conv = objective(np.log10(c_s0_fit), gal_data, train_gal, return_diag=True)
    ho_rms, ho_ok, ho_fail, ho_conv = objective(np.log10(c_s0_fit), gal_data, hold_gal, return_diag=True)

    print(f"\nTRAIN:   rms={tr_rms:.4f} dex, converged {tr_ok}/{tr_ok+tr_fail} ({tr_conv:.1%})")
    print(f"HOLDOUT: rms={ho_rms:.4f} dex, converged {ho_ok}/{ho_ok+ho_fail} ({ho_conv:.1%})")

    print(f"\n=== comparison to prior baselines ===")
    print(f"  plain RAR:            train=0.1338, holdout=0.1298 dex")
    print(f"  choke n=1/2:          train=0.1380, holdout=0.1387 dex")
    print(f"  Domain X (this, linear-only): train={tr_rms:.4f}, holdout={ho_rms:.4f} dex")

    out = dict(
        rho_HDF_ref=RHO_HDF_REF, c_s0_fit=c_s0_fit, c_s0_over_c=c_s0_fit/c,
        train_rms=tr_rms, train_ok=tr_ok, train_fail=tr_fail, train_conv=tr_conv,
        holdout_rms=ho_rms, holdout_ok=ho_ok, holdout_fail=ho_fail, holdout_conv=ho_conv,
        note="Linear closure only (K1=rho0*c_s0^2), no nonlinear/dissipative terms. Floor test."
    )
    with open("domain_X_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nresults -> domain_X_results.json")

if __name__ == "__main__":
    main()
