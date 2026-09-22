import numpy as np
import json

G = 6.6743e-11
KPC = 3.0856775814913673e19
KMS = 1.0e3
UPS_D, UPS_B = 0.5, 0.7
Msun = 1.989e30

def read_vizier_tsv(path, cols):
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8", errors="replace")]
    hdr_i = None
    for i, l in enumerate(lines):
        if l.startswith("#") or not l.strip(): continue
        if "\t" in l and "recno" in l: hdr_i = i; break
    names = lines[hdr_i].split("\t")
    dash_i = None
    for i in range(hdr_i+1, min(hdr_i+6, len(lines))):
        if set(lines[i].replace("\t"," ").strip()) <= set("- "): dash_i = i
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
    t1 = read_vizier_tsv("vizier_t1.txt", ["Name","i","Qual"])
    t2 = read_vizier_tsv("vizier_t2.txt", ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
    inc  = {n:i for n,i in zip(t1["Name"], t1["i"])}
    qual = {n:q for n,q in zip(t1["Name"], t1["Qual"])}

    name_orig = np.array(t2["Name"])
    R_orig = np.array(t2["Rad"], float)
    Vo_orig = np.array(t2["Vobs"], float)
    eVo_orig = np.array(t2["e_Vobs"], float)
    Vg_orig = np.array(t2["Vgas"], float)
    Vd_orig = np.array(t2["Vdisk"], float)
    Vb_orig = np.array(t2["Vbulge"], float)

    Vb_orig = np.where(np.isnan(Vb_orig), 0.0, Vb_orig)
    Vg_orig = np.where(np.isnan(Vg_orig), 0.0, Vg_orig)

    inc_a  = np.array([inc.get(n, np.nan)  for n in name_orig], float)
    qual_a = np.array([qual.get(n, np.nan) for n in name_orig], float)

    m = (R_orig > 0) & (Vo_orig > 0) & np.isfinite(eVo_orig)
    m &= (eVo_orig/Vo_orig <= 0.10); m &= (inc_a >= 30.0); m &= (qual_a <= 2)

    R_filtered, Vo_filtered, eVo_filtered, Vg_filtered, Vd_filtered, Vb_filtered, name_filtered = \
        R_orig[m], Vo_orig[m], eVo_orig[m], Vg_orig[m], Vd_orig[m], Vb_orig[m], name_orig[m]

    conv = (KMS**2)/KPC
    g_obs_all = Vo_filtered**2 / R_filtered * conv
    Vbar2 = Vg_filtered*np.abs(Vg_filtered) + UPS_D*Vd_filtered*np.abs(Vd_filtered) + UPS_B*Vb_filtered*np.abs(Vb_filtered)
    g_bar_all = Vbar2 / R_filtered * conv

    ok = (g_bar_all > 0) & (g_obs_all > 0)
    g_obs_all, g_bar_all, name_filtered, R_filtered = g_obs_all[ok], g_bar_all[ok], name_filtered[ok], R_filtered[ok]

    Vo_filtered = Vo_filtered[ok]
    eVo_filtered = eVo_filtered[ok]


    galaxies = sorted(set(name_filtered))
    gal_data = {}
    for g in galaxies:
        gm = (name_filtered == g)
        r_kpc = R_filtered[gm]; gobs = g_obs_all[gm]; gbar = g_bar_all[gm]
        Vo_gal = Vo_filtered[gm]; eVo_gal = eVo_filtered[gm]

        order = np.argsort(r_kpc)
        r_kpc, gobs, gbar = r_kpc[order], gobs[order], gbar[order]
        Vo_gal, eVo_gal = Vo_gal[order], eVo_gal[order]

        if len(r_kpc) < 4: continue

        gal_data[g] = dict(r=r_kpc*KPC,
                           vobs=Vo_gal * KMS,
                           evobs=eVo_gal * KMS,
                           gobs=gobs,
                           gbar=gbar)
    return gal_data

def invert_density(r, delta_g):
    f = r**2 * delta_g
    dfdr = np.gradient(f, r)
    rho = dfdr / (4*np.pi*G*r**2)
    return rho

def residualize(y, x):
    x = np.asarray(x).ravel()
    X = np.column_stack([np.ones_like(x), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return y - X @ beta

def main():
    gal_data = load()
    print(f"Domain Y v2 (Colab pass 1): direct density-profile inversion, {len(gal_data)} galaxies")
    print("No RHO_HDF_REF, no fit, no BVP -- pure Newtonian inversion of real data.\n")

    all_rho = []
    all_r_kpc = []
    all_gbar = []
    per_galaxy = {}

    for name, gd in gal_data.items():
        r, gobs, gbar = gd["r"], gd["gobs"], gd["gbar"]
        delta_g = gobs - gbar

        M_req_check = r**2 * delta_g / G
        try:
            np.testing.assert_allclose(delta_g, G * M_req_check / r**2, rtol=1e-12, atol=0.0)
        except AssertionError as e:
            print(f"Consistency check FAILED for galaxy {name}: {e}")

        rho_req = invert_density(r, delta_g)

        interior = np.zeros_like(rho_req, dtype=bool)
        if len(rho_req) > 2:
            interior[1:-1] = True

        valid_for_stats = (
            interior
            & np.isfinite(rho_req)
            & (rho_req > 0)
        )

        per_galaxy[name] = dict(
            r_kpc=(r/KPC).tolist(),
            vobs=(gd["vobs"]).tolist(),
            evobs=(gd["evobs"]).tolist(),
            delta_g=delta_g.tolist(),
            rho_req=rho_req.tolist()
        )

        all_rho.extend(rho_req[valid_for_stats].tolist())
        all_r_kpc.extend((r[valid_for_stats]/KPC).tolist())
        all_gbar.extend(gbar[valid_for_stats].tolist())

    all_rho = np.array(all_rho)
    all_r_kpc = np.array(all_r_kpc)
    all_gbar = np.array(all_gbar)

    all_rho_full = []
    for name, gd in per_galaxy.items():
        all_rho_full.extend(gd['rho_req'])
    all_rho_full = np.array(all_rho_full)

    finite = np.isfinite(all_rho_full)
    positive = finite & (all_rho_full > 0)
    negative = finite & (all_rho_full < 0)
    zero_or_nan_inf = ~finite | (all_rho_full == 0)

    n_total = len(all_rho_full)
    n_finite = finite.sum()
    n_positive = positive.sum()
    n_negative = negative.sum()
    n_zero_or_nan_inf = zero_or_nan_inf.sum()

    print(f"\n--- rho_req diagnostic ---")
    print(f"Total rho_req points: {n_total}")
    print(f"Finite rho_req points: {n_finite}")
    if n_finite > 0:
        print(f"  Positive: {n_positive} ({n_positive/n_finite:.1%})")
        print(f"  Negative: {n_negative} ({n_negative/n_finite:.1%})")
    print(f"Zero/NaN/Inf points: {n_zero_or_nan_inf}")
    print(f"--------------------------")

    print(f"valid (positive, finite, non-endpoint) rho_req points used for stats: {len(all_rho)} / {n_total} total points")
    if len(all_rho) > 0:
        print(f"rho_req range: {all_rho.min():.3e} to {all_rho.max():.3e} kg/m^3")
        print(f"rho_req median: {np.median(all_rho):.3e} kg/m^3")
    else:
        print(f"No valid rho_req points to calculate range or median.")

    bins = np.array([0,1,2,4,8,16,32,64])
    print("\nrho_req(r) vs radius (median in each real-data radial bin, kpc):")
    for lo, hi in zip(bins[:-1], bins[1:]):
        m = (all_r_kpc >= lo) & (all_r_kpc < hi)
        if m.sum() < 3: continue
        print(f"  {lo:>3}-{hi:<3} kpc: n={m.sum():4d}  median rho_req = {np.median(all_rho[m]):.3e} kg/m^3")

    if len(all_rho) > 10:
        logrho = np.log10(all_rho)
        loggbar = np.log10(all_gbar)

        corr = np.corrcoef(logrho, loggbar)[0,1]
        slope = np.polyfit(loggbar, logrho, 1)
        print(f"\ncorr(log rho_req, log g_bar) = {corr:.3f}")
        print(f"log-log slope (rho_req vs g_bar) = {slope[0]:.3f}, intercept = {slope[1]:.3f}")

        if len(all_r_kpc) >= 2:
            logr = np.log10(all_r_kpc)
            rho_resid = residualize(logrho, logr)
            gbar_resid = residualize(loggbar, logr)

            if len(rho_resid) > 1 and len(gbar_resid) > 1:
                try:
                    partial_corr = np.corrcoef(rho_resid, gbar_resid)[0, 1]
                    print(f"partial corr(log rho_req, log g_bar | log r) = {partial_corr:.3f}")
                except RuntimeWarning:
                    print(f"Warning: Not enough variation in residuals to compute partial correlation.")
            else:
                print(f"Not enough data points after residualizing for partial correlation.")
        else:
            print(f"Not enough data points for partial correlation calculation.")
    else:
        print(f"Not enough valid data points for correlation calculations.")

    with open("domain_Y_v2_results.json", "w") as f:
        json.dump(dict(per_galaxy=per_galaxy,
                        summary=dict(n_valid=len(all_rho),
                                     rho_spherical_equivalent_required_kg_m3_median=float(np.median(all_rho)) if len(all_rho) > 0 else np.nan,
                                     rho_spherical_equivalent_required_kg_m3_min=float(all_rho.min()) if len(all_rho) > 0 else np.nan,
                                     rho_spherical_equivalent_required_kg_m3_max=float(all_rho.max()) if len(all_rho) > 0 else np.nan)),
                  f, indent=2)
    print("\nresults -> domain_Y_v2_results.json")

if __name__ == "__main__":
    main()
