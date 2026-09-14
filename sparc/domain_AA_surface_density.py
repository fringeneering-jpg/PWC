"""
PWC Framework - Domain AA: baryonic-surface-density amplitude normalization
test on the Domain Y atlas. Single pre-registered test, per the discipline
established for Domain Z (define the predictor before inspecting results;
preserve Domain Y's sample/inversion/assumptions/endpoint handling; state
the pass criterion in advance; preserve a negative result exactly as found).

Question: does normalizing rho_req by a characteristic density scale built
from baryonic surface density (Sigma_bar) reduce cross-galaxy scatter,
relative to the frozen Domain Z physical-kpc baseline of 0.377 dex?

Predictor, declared before running (not searched over):
  M_star  = Upsilon_disk * L[3.6]                 (Upsilon_disk=0.5, project standard;
                                                     L[3.6] is TOTAL luminosity, not
                                                     disk-only -- see limitations)
  M_gas   = 1.33 * M_HI                            (standard He-correction factor,
                                                     Lelli/McGaugh/Schombert convention,
                                                     not invented for this test)
  Sigma_bar = (M_star + M_gas) / (2*pi*Rdisk^2)    (mean baryonic surface density
                                                     within one disk scale length)
  rho_0     = Sigma_bar / Rdisk                    (one characteristic density scale,
                                                     dimensionally exact: [M/L^2]/[L]=[M/L^3],
                                                     no fitted exponent)
  rho_tilde = rho_req / rho_0                      (dimensionless, one-parameter
                                                     amplitude normalization -- this is
                                                     the ONLY new choice; radius coordinate
                                                     stays x=r/Rdisk, as pre-registered
                                                     for Domain Z)

Pass criterion, declared before running: rho_tilde's cross-galaxy scatter
(std of log10(rho_tilde) across per-galaxy medians, same bins/n_gal>=5 rule
as Domain Z) must be LOWER than the frozen 0.377 dex physical-kpc baseline
to count as support for Sigma_bar as an organizing variable. No exponent or
functional form was tuned to hit this criterion -- rho_0's definition was
fixed above before this script was run.

L[3.6] and M_HI units confirmed against known catalog values before running
this script (NGC3198: MHI=10.869 -> 1.089e10 Msun, matches catalog; NGC2403:
MHI=3.199 -> 3.199e9 Msun, matches catalog) -- both columns are in units of
1e9 (Lsun or Msun), standard SPARC/VizieR convention.
"""
import numpy as np
import json

G = 6.6743e-11
KPC = 3.0856775814913673e19
KMS = 1.0e3
UPS_D, UPS_B = 0.5, 0.7
MSUN = 1.989e30
LSUN_TO_MSUN_UNIT = 1.0e9   # L3.6 and MHI columns are both in units of 1e9 (Lsun/Msun)
HE_CORRECTION = 1.33        # M_gas = 1.33*M_HI, standard convention

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
    n_missing = 0
    for g in galaxies:
        gm = (name == g)
        r_kpc = R[gm]; gobs = g_obs_all[gm]; gbar = g_bar_all[gm]
        order = np.argsort(r_kpc)
        r_kpc, gobs, gbar = r_kpc[order], gobs[order], gbar[order]
        if len(r_kpc) < 4: continue
        rd = rdisk.get(g, np.nan); L = l36.get(g, np.nan); MHI_ = mhi.get(g, np.nan)
        if not (np.isfinite(rd) and rd > 0 and np.isfinite(L) and L > 0 and np.isfinite(MHI_) and MHI_ >= 0):
            n_missing += 1
            gal_data[g] = dict(r=r_kpc*KPC, gobs=gobs, gbar=gbar, Rdisk_kpc=rd, rho_0=np.nan)
            continue
        M_star = UPS_D * L * LSUN_TO_MSUN_UNIT * MSUN
        M_gas  = HE_CORRECTION * MHI_ * LSUN_TO_MSUN_UNIT * MSUN
        Rd_m = rd * KPC
        Sigma_bar = (M_star + M_gas) / (2*np.pi*Rd_m**2)
        rho_0 = Sigma_bar / Rd_m
        gal_data[g] = dict(r=r_kpc*KPC, gobs=gobs, gbar=gbar, Rdisk_kpc=rd,
                            Sigma_bar=Sigma_bar, rho_0=rho_0)
    return gal_data, n_missing

def invert_density(r, delta_g):
    f = r**2 * delta_g
    dfdr = np.gradient(f, r)
    return dfdr / (4*np.pi*G*r**2)

def main():
    gal_data, n_missing = load()
    print(f"Domain AA: baryonic-surface-density amplitude normalization test, {len(gal_data)} galaxies")
    print(f"  ({n_missing} galaxies missing L3.6/MHI/Rdisk -- excluded from rho_0 normalization)\n")
    print("Pre-registered pass criterion: mean scatter of log10(rho_tilde) across x=r/Rdisk")
    print("bins (n_gal>=5) must be LOWER than the frozen 0.377 dex physical-kpc baseline.\n")

    bins_x = np.array([0,0.5,1,1.5,2,3,4,6,8,12,20])
    galaxy_bin_tilde_medians = {f"{lo}-{hi}": [] for lo,hi in zip(bins_x[:-1], bins_x[1:])}
    galaxy_bin_raw_medians   = {f"{lo}-{hi}": [] for lo,hi in zip(bins_x[:-1], bins_x[1:])}  # rho_req in x bins, cross-check vs Domain Z

    amplitude_check = []  # (Sigma_bar, per-galaxy characteristic rho_req at x=1-2) for a direct correlation check

    n_used = 0
    for name, gd in gal_data.items():
        r, gobs, gbar, rd, rho_0 = gd["r"], gd["gobs"], gd["gbar"], gd["Rdisk_kpc"], gd["rho_0"]
        if not np.isfinite(rho_0):
            continue
        delta_g = gobs - gbar
        rho_req = invert_density(r, delta_g)
        interior = np.zeros_like(rho_req, dtype=bool)
        if len(rho_req) > 2: interior[1:-1] = True
        valid = interior & np.isfinite(rho_req) & (rho_req > 0)
        if valid.sum() == 0:
            continue
        n_used += 1
        r_kpc = r/KPC
        x = r_kpc/rd
        rho_tilde = rho_req/rho_0

        x_valid = x[valid]; rho_req_valid = rho_req[valid]; rho_tilde_valid = rho_tilde[valid]
        for lo, hi in zip(bins_x[:-1], bins_x[1:]):
            m_bin = (x_valid >= lo) & (x_valid < hi)
            if m_bin.sum() > 0:
                galaxy_bin_tilde_medians[f"{lo}-{hi}"].append(float(np.median(rho_tilde_valid[m_bin])))
                galaxy_bin_raw_medians[f"{lo}-{hi}"].append(float(np.median(rho_req_valid[m_bin])))

        m12 = (x_valid >= 1.0) & (x_valid < 2.0)
        if m12.sum() > 0:
            amplitude_check.append((gd["Sigma_bar"], float(np.median(rho_req_valid[m12]))))

    print(f"galaxies used (finite rho_0): {n_used} / {len(gal_data)}\n")

    print("=== Direct check: does per-galaxy amplitude (rho_req at x=1-2 Rd) correlate with Sigma_bar? ===")
    if len(amplitude_check) > 10:
        sb, amp = zip(*amplitude_check)
        sb = np.array(sb); amp = np.array(amp)
        ok = (sb > 0) & (amp > 0)
        corr = np.corrcoef(np.log10(sb[ok]), np.log10(amp[ok]))[0,1]
        print(f"n={ok.sum()}, corr(log Sigma_bar, log rho_req[x=1-2]) = {corr:.3f}")

    print("\n=== Scatter, rho_tilde = rho_req/rho_0(Sigma_bar), in x=r/Rdisk bins (galaxy-weighted) ===")
    tilde_scatter = {}
    for label, vals in galaxy_bin_tilde_medians.items():
        if len(vals) >= 5:
            s = float(np.std(np.log10(vals)))
            tilde_scatter[label] = dict(n_gal=len(vals), std_dex=s)
            print(f"  x={label:>10} R_d: n_gal={len(vals):3d}  scatter(rho_tilde) = {s:.3f} dex")

    print("\n=== Cross-check: raw rho_req scatter in x bins, this sample (should match Domain Z closely) ===")
    raw_scatter = {}
    for label, vals in galaxy_bin_raw_medians.items():
        if len(vals) >= 5:
            s = float(np.std(np.log10(vals)))
            raw_scatter[label] = dict(n_gal=len(vals), std_dex=s)
            print(f"  x={label:>10} R_d: n_gal={len(vals):3d}  scatter(rho_req) = {s:.3f} dex")

    DOMAIN_Z_PHYSICAL_KPC_BASELINE = 0.377
    if tilde_scatter:
        mean_tilde = float(np.mean([v["std_dex"] for v in tilde_scatter.values()]))
        print(f"\nmean scatter, rho_tilde in x=r/Rdisk bins (n_gal>=5): {mean_tilde:.3f} dex")
        print(f"frozen Domain Z physical-kpc baseline: {DOMAIN_Z_PHYSICAL_KPC_BASELINE:.3f} dex")
        if mean_tilde < DOMAIN_Z_PHYSICAL_KPC_BASELINE:
            print(f"-> PASSES pre-registered criterion: Sigma_bar-based normalization reduces scatter by {DOMAIN_Z_PHYSICAL_KPC_BASELINE-mean_tilde:.3f} dex")
        else:
            print(f"-> FAILS pre-registered criterion: scatter is {mean_tilde-DOMAIN_Z_PHYSICAL_KPC_BASELINE:.3f} dex WORSE than the physical-kpc baseline")

    if raw_scatter:
        mean_raw = float(np.mean([v["std_dex"] for v in raw_scatter.values()]))
        print(f"\n(cross-check) mean scatter, raw rho_req in x=r/Rdisk bins, this sample: {mean_raw:.3f} dex (Domain Z reported 0.447 dex on the full 139-galaxy sample)")

    out = dict(
        n_galaxies=len(gal_data), n_missing_predictor=n_missing, n_used=n_used,
        pass_criterion_dex=DOMAIN_Z_PHYSICAL_KPC_BASELINE,
        rho_tilde_scatter_dex=tilde_scatter,
        raw_rho_req_scatter_dex_this_sample=raw_scatter,
        amplitude_vs_sigma_bar_n=len(amplitude_check),
    )
    with open("domain_AA_surface_density_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nresults -> domain_AA_surface_density_results.json")

if __name__ == "__main__":
    main()
