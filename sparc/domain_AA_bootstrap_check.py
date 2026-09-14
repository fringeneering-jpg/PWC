"""
Domain AA follow-up: galaxy-level bootstrap significance check.

The raw result (mean scatter: rho_tilde 0.367 dex vs frozen physical-kpc
baseline 0.377 dex) is a 0.010 dex margin -- far smaller than the per-bin
scatter itself (0.22-0.51 dex range). Per the pre-registered discipline
("use per-galaxy medians and galaxy-level resampling, not pooled radial
points"), this bootstraps over GALAXIES (not radial points) to check
whether that margin is distinguishable from noise, before calling it a pass.

Method: resample the 139 galaxies with replacement (each resample keeps a
galaxy's full radial profile intact -- galaxy is the resampling unit, not
individual points), recompute both (a) the physical-kpc scatter (Domain Z's
statistic) and (b) the rho_tilde-in-x-bins scatter (Domain AA's statistic)
on each replicate, and report the fraction of replicates where AA's
statistic is actually lower than Domain Z's own recomputed baseline on the
SAME resample (a paired comparison, more powerful than comparing to the
single frozen 0.377 number).
"""
import numpy as np
import json

G = 6.6743e-11
KPC = 3.0856775814913673e19
KMS = 1.0e3
UPS_D, UPS_B = 0.5, 0.7
MSUN = 1.989e30
UNIT = 1.0e9
HE_CORRECTION = 1.33
N_BOOT = 2000
SEED = 7

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
    t1 = read_vizier_tsv("vizier_t1.txt", ["Name","i","Qual","Rdisk","L3.6","MHI"])
    t2 = read_vizier_tsv("vizier_t2.txt", ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
    inc  = {n:i for n,i in zip(t1["Name"], t1["i"])}
    qual = {n:q for n,q in zip(t1["Name"], t1["Qual"])}
    rdisk = {n:r for n,r in zip(t1["Name"], t1["Rdisk"])}
    l36 = {n:v for n,v in zip(t1["Name"], t1["L3.6"])}
    mhi = {n:v for n,v in zip(t1["Name"], t1["MHI"])}
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
        if len(r_kpc) < 4: continue
        rd = rdisk.get(g, np.nan); L = l36.get(g, np.nan); MHI_ = mhi.get(g, np.nan)
        rho_0 = np.nan
        if np.isfinite(rd) and rd > 0 and np.isfinite(L) and L > 0 and np.isfinite(MHI_) and MHI_ >= 0:
            M_star = UPS_D * L * UNIT * MSUN
            M_gas  = HE_CORRECTION * MHI_ * UNIT * MSUN
            Rd_m = rd * KPC
            Sigma_bar = (M_star + M_gas) / (2*np.pi*Rd_m**2)
            rho_0 = Sigma_bar / Rd_m
        gal_data[g] = dict(r=r_kpc*KPC, gobs=gobs, gbar=gbar, Rdisk_kpc=rd, rho_0=rho_0)
    return gal_data

def invert_density(r, delta_g):
    f = r**2 * delta_g
    dfdr = np.gradient(f, r)
    return dfdr / (4*np.pi*G*r**2)

def precompute(gal_data):
    """Precompute, per galaxy, the valid (r_kpc, x, rho_req, rho_tilde) arrays once."""
    pre = {}
    for name, gd in gal_data.items():
        r, gobs, gbar, rd, rho_0 = gd["r"], gd["gobs"], gd["gbar"], gd["Rdisk_kpc"], gd["rho_0"]
        delta_g = gobs - gbar
        rho_req = invert_density(r, delta_g)
        interior = np.zeros_like(rho_req, dtype=bool)
        if len(rho_req) > 2: interior[1:-1] = True
        valid = interior & np.isfinite(rho_req) & (rho_req > 0)
        if valid.sum() == 0: continue
        r_kpc = (r/KPC)[valid]; rho_req_v = rho_req[valid]
        entry = dict(r_kpc=r_kpc, rho_req=rho_req_v)
        if np.isfinite(rho_0) and rd > 0:
            entry["x"] = r_kpc/rd
            entry["rho_tilde"] = rho_req_v/rho_0
        pre[name] = entry
    return pre

def bin_scatter(names, pre, bins, key_r, key_rho, min_n=5):
    galaxy_bin_medians = {f"{lo}-{hi}": [] for lo,hi in zip(bins[:-1], bins[1:])}
    for name in names:
        entry = pre.get(name)
        if entry is None or key_r not in entry: continue
        rvals = entry[key_r]; rhovals = entry[key_rho]
        for lo, hi in zip(bins[:-1], bins[1:]):
            mbin = (rvals >= lo) & (rvals < hi)
            if mbin.sum() > 0:
                galaxy_bin_medians[f"{lo}-{hi}"].append(np.median(rhovals[mbin]))
    scatters = []
    for label, vals in galaxy_bin_medians.items():
        if len(vals) >= min_n:
            scatters.append(np.std(np.log10(vals)))
    return np.mean(scatters) if scatters else np.nan

def main():
    gal_data = load()
    pre = precompute(gal_data)
    all_names = [n for n in gal_data if n in pre]
    print(f"Domain AA bootstrap check: {len(all_names)} galaxies, {N_BOOT} galaxy-level resamples\n")

    bins_kpc = np.array([0,1,2,4,8,16,32,64])
    bins_x   = np.array([0,0.5,1,1.5,2,3,4,6,8,12,20])

    rng = np.random.default_rng(SEED)
    diffs = []  # physical_kpc_scatter - rho_tilde_scatter, per replicate; positive means AA wins
    n_valid_replicates = 0
    for b in range(N_BOOT):
        sample = rng.choice(all_names, size=len(all_names), replace=True)
        s_phys = bin_scatter(sample, pre, bins_kpc, "r_kpc", "rho_req", min_n=5)
        s_tilde = bin_scatter(sample, pre, bins_x, "x", "rho_tilde", min_n=5)
        if np.isfinite(s_phys) and np.isfinite(s_tilde):
            diffs.append(s_phys - s_tilde)
            n_valid_replicates += 1

    diffs = np.array(diffs)
    print(f"valid replicates: {n_valid_replicates}/{N_BOOT}")
    print(f"mean(physical_kpc_scatter - rho_tilde_scatter) = {diffs.mean():.4f} dex")
    print(f"std across replicates = {diffs.std():.4f} dex")
    print(f"95% CI on the difference: [{np.percentile(diffs,2.5):.4f}, {np.percentile(diffs,97.5):.4f}] dex")
    frac_positive = float((diffs > 0).mean())
    print(f"fraction of resamples where rho_tilde scatter < physical-kpc scatter: {frac_positive:.3f}")
    if frac_positive > 0.975 or frac_positive < 0.025:
        print("-> result is directionally consistent across resamples (outside the 95% null band)")
    else:
        print("-> NOT distinguishable from zero at 95% -- the point-estimate 'pass' does not survive resampling")

    # === paired, matched-bin comparison: rho_tilde vs raw rho_req, BOTH in the ===
    # === same x=r/Rdisk bins -- removes the bin-geometry confound entirely    ===
    print("\n=== Paired check: rho_tilde vs raw rho_req, same x=r/Rdisk bins (matched geometry) ===")
    diffs2 = []
    for b in range(N_BOOT):
        sample = rng.choice(all_names, size=len(all_names), replace=True)
        s_raw = bin_scatter(sample, pre, bins_x, "x", "rho_req", min_n=5)
        s_tilde = bin_scatter(sample, pre, bins_x, "x", "rho_tilde", min_n=5)
        if np.isfinite(s_raw) and np.isfinite(s_tilde):
            diffs2.append(s_raw - s_tilde)
    diffs2 = np.array(diffs2)
    print(f"valid replicates: {len(diffs2)}/{N_BOOT}")
    print(f"mean(raw_rho_req_scatter - rho_tilde_scatter), same x bins = {diffs2.mean():.4f} dex")
    print(f"95% CI: [{np.percentile(diffs2,2.5):.4f}, {np.percentile(diffs2,97.5):.4f}] dex")
    frac_positive2 = float((diffs2 > 0).mean())
    print(f"fraction of resamples where rho_tilde beats raw rho_req in the same bins: {frac_positive2:.3f}")
    if frac_positive2 > 0.975 or frac_positive2 < 0.025:
        print("-> distinguishable from zero at 95%: Sigma_bar normalization has a real effect on TOP of the x=r/Rdisk coordinate choice")
    else:
        print("-> NOT distinguishable from zero at 95%")

    out = dict(n_galaxies=len(all_names), n_boot=N_BOOT, n_valid_replicates=n_valid_replicates,
               vs_physical_kpc_baseline=dict(mean_diff_dex=float(diffs.mean()), std_diff_dex=float(diffs.std()),
                                              ci95_low=float(np.percentile(diffs,2.5)), ci95_high=float(np.percentile(diffs,97.5)),
                                              frac_resamples_tilde_lower=frac_positive),
               vs_raw_rho_req_same_x_bins=dict(mean_diff_dex=float(diffs2.mean()),
                                                ci95_low=float(np.percentile(diffs2,2.5)), ci95_high=float(np.percentile(diffs2,97.5)),
                                                frac_resamples_tilde_lower=frac_positive2))
    with open("domain_AA_bootstrap_results.json","w") as f:
        json.dump(out, f, indent=2)
    print("\nresults -> domain_AA_bootstrap_results.json")

if __name__ == "__main__":
    main()
