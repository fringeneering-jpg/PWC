"""
PWC Framework - Domain Z: disk-scale-length collapse test on the frozen
Domain Y density-inversion atlas.

Question (pre-registered, descriptive only -- see PROVENANCE_MANIFEST.md
Domain Y "next open test"): does rho_req(r) collapse onto one curve when
radius is measured in units of each galaxy's own disk scale length R_d
(x=r/R_d), instead of physical kpc? A collapse would suggest a self-similar
galaxy-associated structure; no collapse points to mass, surface density,
gas fraction, morphology, or environment as the organizing variable(s).

This does NOT modify the Domain Y inversion. Same 139-galaxy quality cuts,
same baryonic assumptions (Upsilon_disk=0.5, Upsilon_bulge=0.7), same
endpoint-exclusion rule, same galaxy-weighted stacking convention as
Domain Y. The only addition: R_d pulled from vizier_t1.txt (VizieR SPARC
Table 1 column "Rdisk", the 3.6um exponential stellar-disk scale length,
kpc) and used to build a second, parallel dimensionless stack alongside
the original physical-kpc one (which is preserved unchanged for reference).

Galaxies with missing/non-positive Rdisk are excluded from the normalized
stack only (not from the physical-kpc stack) -- reported explicitly, not
silently dropped.
"""
import numpy as np
import json

G = 6.6743e-11
KPC = 3.0856775814913673e19
KMS = 1.0e3
UPS_D, UPS_B = 0.5, 0.7

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
    t1 = read_vizier_tsv("vizier_t1.txt", ["Name","i","Qual","Rdisk"])
    t2 = read_vizier_tsv("vizier_t2.txt", ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
    inc  = {n:i for n,i in zip(t1["Name"], t1["i"])}
    qual = {n:q for n,q in zip(t1["Name"], t1["Qual"])}
    rdisk = {n:r for n,r in zip(t1["Name"], t1["Rdisk"])}
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
    n_missing_rdisk = 0
    for g in galaxies:
        gm = (name == g)
        r_kpc = R[gm]; gobs = g_obs_all[gm]; gbar = g_bar_all[gm]
        order = np.argsort(r_kpc)
        r_kpc, gobs, gbar = r_kpc[order], gobs[order], gbar[order]
        if len(r_kpc) < 4: continue
        rd = rdisk.get(g, np.nan)
        if not (np.isfinite(rd) and rd > 0):
            n_missing_rdisk += 1
        gal_data[g] = dict(r=r_kpc*KPC, gobs=gobs, gbar=gbar, Rdisk_kpc=rd)
    return gal_data, n_missing_rdisk

def invert_density(r, delta_g):
    f = r**2 * delta_g
    dfdr = np.gradient(f, r)
    return dfdr / (4*np.pi*G*r**2)

def main():
    gal_data, n_missing_rdisk = load()
    print(f"Domain Z: disk-scale-length collapse test, {len(gal_data)} galaxies")
    print(f"  ({n_missing_rdisk} galaxies missing/non-positive Rdisk -- excluded from the normalized stack only)\n")

    # -- physical-kpc stack (identical to Domain Y, preserved for reference) --
    phys_rho, phys_r_kpc = [], []
    # -- normalized x=r/Rdisk stack (galaxy-weighted, same endpoint-exclusion rule) --
    norm_rho, norm_x = [], []
    per_galaxy_norm_median = {}  # for galaxy-weighted binning

    bins_kpc = np.array([0,1,2,4,8,16,32,64])
    bins_x   = np.array([0,0.5,1,1.5,2,3,4,6,8,12,20])

    galaxy_bin_x_medians = {f"{lo}-{hi}": [] for lo,hi in zip(bins_x[:-1], bins_x[1:])}

    galaxy_bin_kpc_medians = {f"{lo}-{hi}": [] for lo,hi in zip(bins_kpc[:-1], bins_kpc[1:])}

    n_used_for_norm = 0
    for name, gd in gal_data.items():
        r, gobs, gbar, rd = gd["r"], gd["gobs"], gd["gbar"], gd["Rdisk_kpc"]
        delta_g = gobs - gbar
        rho_req = invert_density(r, delta_g)

        interior = np.zeros_like(rho_req, dtype=bool)
        if len(rho_req) > 2: interior[1:-1] = True
        valid = interior & np.isfinite(rho_req) & (rho_req > 0)

        r_kpc = r/KPC
        phys_rho.extend(rho_req[valid].tolist())
        phys_r_kpc.extend(r_kpc[valid].tolist())

        r_kpc_valid = r_kpc[valid]; rho_valid_phys = rho_req[valid]
        for lo, hi in zip(bins_kpc[:-1], bins_kpc[1:]):
            m_bin = (r_kpc_valid >= lo) & (r_kpc_valid < hi)
            if m_bin.sum() > 0:
                galaxy_bin_kpc_medians[f"{lo}-{hi}"].append(float(np.median(rho_valid_phys[m_bin])))

        if not (np.isfinite(rd) and rd > 0):
            continue
        n_used_for_norm += 1
        x = r_kpc / rd
        norm_rho.extend(rho_req[valid].tolist())
        norm_x.extend(x[valid].tolist())

        x_valid = x[valid]; rho_valid = rho_req[valid]
        for lo, hi in zip(bins_x[:-1], bins_x[1:]):
            m_bin = (x_valid >= lo) & (x_valid < hi)
            if m_bin.sum() > 0:
                galaxy_bin_x_medians[f"{lo}-{hi}"].append(float(np.median(rho_valid[m_bin])))

    phys_rho = np.array(phys_rho); phys_r_kpc = np.array(phys_r_kpc)
    norm_rho = np.array(norm_rho); norm_x = np.array(norm_x)

    print(f"galaxies with usable Rdisk: {n_used_for_norm} / {len(gal_data)}\n")

    print("=== Reference: physical-kpc stack (point-weighted median, unchanged from Domain Y) ===")
    for lo, hi in zip(bins_kpc[:-1], bins_kpc[1:]):
        m = (phys_r_kpc >= lo) & (phys_r_kpc < hi)
        if m.sum() < 3: continue
        print(f"  {lo:>3}-{hi:<3} kpc: n={m.sum():4d}  median rho_req = {np.median(phys_rho[m]):.3e} kg/m^3")

    print("\n=== Normalized x=r/Rdisk stack (point-weighted median) ===")
    point_medians = {}
    for lo, hi in zip(bins_x[:-1], bins_x[1:]):
        m = (norm_x >= lo) & (norm_x < hi)
        if m.sum() < 3: continue
        med = float(np.median(norm_rho[m]))
        point_medians[f"{lo}-{hi}"] = med
        print(f"  x={lo:>4}-{hi:<4} R_d: n={m.sum():4d}  median rho_req = {med:.3e} kg/m^3")

    print("\n=== Normalized x=r/Rdisk stack (galaxy-weighted median -- robustness check) ===")
    galaxy_medians = {}
    for label, vals in galaxy_bin_x_medians.items():
        if len(vals) == 0: continue
        gwm = float(np.median(vals))
        galaxy_medians[label] = dict(n_gal=len(vals), median=gwm)
        print(f"  x={label:>9} R_d: n_gal={len(vals):3d}  galaxy-weighted median rho_req = {gwm:.3e} kg/m^3")

    # quantify collapse: coefficient of variation across the bin medians
    # (compare the spread in normalized bins to the spread in physical-kpc bins,
    # both computed the same way, as a simple, honest diagnostic -- not a claim
    # of statistical significance)
    if len(point_medians) >= 3:
        vals = np.array(list(point_medians.values()))
        logvals = np.log10(vals)
        print(f"\nnormalized-stack bin medians: log10 range = {logvals.max()-logvals.min():.2f} dex across {len(vals)} bins")

    phys_bin_medians = []
    for lo, hi in zip(bins_kpc[:-1], bins_kpc[1:]):
        m = (phys_r_kpc >= lo) & (phys_r_kpc < hi)
        if m.sum() >= 3:
            phys_bin_medians.append(float(np.median(phys_rho[m])))
    if len(phys_bin_medians) >= 3:
        logvals_phys = np.log10(np.array(phys_bin_medians))
        print(f"physical-kpc stack bin medians:  log10 range = {logvals_phys.max()-logvals_phys.min():.2f} dex across {len(phys_bin_medians)} bins")

    # === the actual collapse test: galaxy-to-galaxy SCATTER at fixed radius, ===
    # === physical kpc vs normalized x=r/Rdisk, using the per-galaxy medians  ===
    # === already computed above (only bins with >=5 galaxies are compared,  ===
    # === so the scatter estimate isn't dominated by 1-2-galaxy bins)        ===
    print("\n=== Collapse test: per-bin galaxy-to-galaxy scatter (std of log10 rho_req across galaxies) ===")
    print("(lower scatter at fixed x than at fixed physical r would indicate real collapse)")
    kpc_scatter = {}
    for label, vals in galaxy_bin_kpc_medians.items():
        if len(vals) >= 5:
            s = float(np.std(np.log10(vals)))
            kpc_scatter[label] = dict(n_gal=len(vals), std_dex=s)
            print(f"  physical r={label:>7} kpc: n_gal={len(vals):3d}  scatter = {s:.3f} dex")
    x_scatter = {}
    for label, vals in galaxy_bin_x_medians.items():
        if len(vals) >= 5:
            s = float(np.std(np.log10(vals)))
            x_scatter[label] = dict(n_gal=len(vals), std_dex=s)
            print(f"  x={label:>10} R_d:   n_gal={len(vals):3d}  scatter = {s:.3f} dex")

    if kpc_scatter and x_scatter:
        mean_kpc_scatter = float(np.mean([v["std_dex"] for v in kpc_scatter.values()]))
        mean_x_scatter = float(np.mean([v["std_dex"] for v in x_scatter.values()]))
        print(f"\nmean scatter, physical-kpc bins (n_gal>=5): {mean_kpc_scatter:.3f} dex")
        print(f"mean scatter, x=r/Rdisk bins (n_gal>=5):    {mean_x_scatter:.3f} dex")
        if mean_x_scatter < mean_kpc_scatter:
            print(f"-> normalizing by Rdisk REDUCES scatter by {mean_kpc_scatter-mean_x_scatter:.3f} dex: modest support for self-similarity")
        else:
            print(f"-> normalizing by Rdisk does NOT reduce scatter (+{mean_x_scatter-mean_kpc_scatter:.3f} dex): no evidence of collapse")

    out = dict(
        n_galaxies=len(gal_data), n_missing_rdisk=n_missing_rdisk, n_used_for_norm=n_used_for_norm,
        physical_kpc_point_weighted_medians={f"{lo}-{hi}": float(np.median(phys_rho[(phys_r_kpc>=lo)&(phys_r_kpc<hi)]))
                                              for lo,hi in zip(bins_kpc[:-1],bins_kpc[1:])
                                              if ((phys_r_kpc>=lo)&(phys_r_kpc<hi)).sum()>=3},
        normalized_x_point_weighted_medians=point_medians,
        normalized_x_galaxy_weighted_medians=galaxy_medians,
        collapse_test_scatter_physical_kpc=kpc_scatter,
        collapse_test_scatter_normalized_x=x_scatter,
    )
    with open("domain_Z_disk_scale_collapse_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nresults -> domain_Z_disk_scale_collapse_results.json")

if __name__ == "__main__":
    main()
