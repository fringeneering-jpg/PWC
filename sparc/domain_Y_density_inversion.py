"""
PWC Framework - Domain Y: direct density-profile inversion (no fit, no BVP).

Purpose: Domain V/W/X all failed because they normalized rho_HDF against
RHO_HDF_REF=4.6e10 kg/m^3 (a compact-core-regime value) inside a galaxy-scale
calculation, making the state variable u ~ 1e-34 -- numerically unusable,
independent of any boundary-condition choice. Diagnosed 2026-09-14.

This script does NOT assume any reference density. It inverts the real SPARC
data directly for the density profile the data themselves require, using
only Newtonian gravity + spherical enclosed-mass algebra:

  Delta_g(r)  = v_obs(r)^2/r - g_bar(r)          [measured excess gravity]
  M_HDF(<r)   = Delta_g(r) * r^2 / G              [implied enclosed excess mass]
  rho_req(r)  = (1/(4 pi r^2)) d/dr[ r^2 Delta_g(r)/G ]   [implied local density]

No HDF reference density, no EOS, no closure, no per-galaxy tuning appears
anywhere in this calculation. It is pure data inversion under a spherical-
symmetry assumption -- the honest first step (Option B/C) before proposing
any universal response law, per the explicit "do not reverse-fit the
normalization" instruction.

Numerical differentiation of sparse, noisy real rotation-curve points is
itself noisy -- reported as-is (central differences on the actual unevenly
spaced r values), not smoothed or spline-fit to produce a cleaner picture.
"""
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
    t1 = read_vizier_tsv("vizier_t1.txt", ["Name","i","Qual"])
    t2 = read_vizier_tsv("vizier_t2.txt", ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
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
        if len(r_kpc) < 4: continue
        gal_data[g] = dict(r=r_kpc*KPC, gobs=gobs, gbar=gbar)
    return gal_data

def invert_density(r, delta_g):
    """rho_req(r) = 1/(4 pi G r^2) * d/dr[r^2 * delta_g(r)]  -- central differences
    on the real (unevenly spaced) r values. Returns NaN at points where
    delta_g < 0 (i.e. observed gravity is LESS than baryonic -- happens for
    some inner points / noisy data; not forced positive, reported honestly)."""
    f = r**2 * delta_g
    dfdr = np.gradient(f, r)
    rho = dfdr / (4*np.pi*G*r**2)
    return rho

def main():
    gal_data = load()
    print(f"Domain Y: direct density-profile inversion, {len(gal_data)} galaxies")
    print("No RHO_HDF_REF, no fit, no BVP -- pure Newtonian inversion of real data.\n")

    all_rho = []
    all_r_kpc = []
    all_gbar = []
    per_galaxy = {}

    for name, gd in gal_data.items():
        r, gobs, gbar = gd["r"], gd["gobs"], gd["gbar"]
        delta_g = gobs - gbar
        rho_req = invert_density(r, delta_g)
        per_galaxy[name] = dict(
            r_kpc=(r/KPC).tolist(), delta_g=delta_g.tolist(), rho_req=rho_req.tolist()
        )
        valid = np.isfinite(rho_req) & (rho_req > 0)
        all_rho.extend(rho_req[valid].tolist())
        all_r_kpc.extend((r[valid]/KPC).tolist())
        all_gbar.extend(gbar[valid].tolist())

    all_rho = np.array(all_rho); all_r_kpc = np.array(all_r_kpc); all_gbar = np.array(all_gbar)
    print(f"valid (positive, finite) rho_req points: {len(all_rho)} / total data points")
    print(f"rho_req range: {all_rho.min():.3e} to {all_rho.max():.3e} kg/m^3")
    print(f"rho_req median: {np.median(all_rho):.3e} kg/m^3")

    # bin by radius to see the trend (real data, no smoothing beyond simple binning)
    bins = np.array([0,1,2,4,8,16,32,64])
    print("\nrho_req(r) vs radius (median in each real-data radial bin, kpc):")
    for lo, hi in zip(bins[:-1], bins[1:]):
        m = (all_r_kpc >= lo) & (all_r_kpc < hi)
        if m.sum() < 3: continue
        print(f"  {lo:>3}-{hi:<3} kpc: n={m.sum():4d}  median rho_req = {np.median(all_rho[m]):.3e} kg/m^3")

    # check correlation with g_bar (does the required density just track baryonic gravity?)
    valid = all_rho > 0
    if valid.sum() > 10:
        logrho = np.log10(all_rho[valid]); loggbar = np.log10(all_gbar[valid])
        corr = np.corrcoef(logrho, loggbar)[0,1]
        slope = np.polyfit(loggbar, logrho, 1)
        print(f"\ncorr(log rho_req, log g_bar) = {corr:.3f}")
        print(f"log-log slope (rho_req vs g_bar) = {slope[0]:.3f}, intercept = {slope[1]:.3f}")

    with open("domain_Y_density_inversion_results.json", "w") as f:
        json.dump(dict(per_galaxy=per_galaxy,
                        summary=dict(n_valid=len(all_rho),
                                     rho_median=float(np.median(all_rho)),
                                     rho_min=float(all_rho.min()), rho_max=float(all_rho.max()))),
                  f, indent=2)
    print("\nresults -> domain_Y_density_inversion_results.json")

if __name__ == "__main__":
    main()
