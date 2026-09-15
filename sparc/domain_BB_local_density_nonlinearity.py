"""
PWC Framework - Domain BB: local-density nonlinearity test ("boosted core").

Mechanism, as stated (2026-09-15): the force law itself stays ordinary
1/r^2, but the effective SOURCE feeding it is boosted specifically where
baryonic matter is concentrated -- tapering back toward ordinary baryonic
sourcing in diffuse regions. This is NOT the same claim as Domain Y's
original corr(rho_req, g_bar)=0.617 result (that used g_bar, the ENCLOSED-
mass-sourced gravity, not local density) and NOT the same as Domain AA's
Sigma_bar amplitude test (a galaxy-averaged surface density, not a local,
radius-by-radius quantity). This tests something new: does rho_req(r)
track a NON-LINEAR function of LOCAL baryonic volume density rho_bar(r)
better than it tracks rho_bar(r) linearly?

Why this is a real, falsifiable claim and not just re-deriving gravity:
ordinary Newtonian gravity only ever cares about enclosed mass M(<r), not
how densely that mass is packed locally. Two galaxies with identical
M(<r) profiles but different local density structure (one compact, one
diffuse) are indistinguishable to ordinary gravity. If rho_req(r) tracks
a non-linear (e.g. quadratic) function of LOCAL rho_bar(r) better than a
linear one, that is evidence for exactly the kind of density-concentration
-sensitive mechanism described, which ordinary gravity cannot produce.

Predeclared, before running:
  rho_bar(r): local baryonic volume density, via the SAME method already
    validated in domain_W_reformulated.py: rho_bar = dM_bar/dr / (4*pi*r^2)
    (spherically-averaged local density from the mass profile's own
    derivative -- not a new/invented estimator).
  rho_req(r): the SAME inversion already frozen in Domain Y
    (rho_req = 1/(4*pi*G*r^2) * d/dr[r^2*(g_obs-g_bar)]), reused unchanged.
  Test forms, declared before checking which wins:
    (a) linear:    log(rho_req) ~ log(rho_bar)
    (b) quadratic: log(rho_req) ~ log(rho_bar^2) = 2*log(rho_bar)
        -- i.e. does rho_req scale closer to rho_bar^1 or rho_bar^2?
  Fit ONE free exponent p via log(rho_req) = a + p*log(rho_bar) (a single
  linear regression, not a search over many forms) and report where p
  actually lands, rather than picking (a) or (b) to match a target.
Same 139-galaxy sample, same quality cuts, same endpoint-exclusion rule,
same galaxy-weighted robustness check as every other domain in this
branch. Does not modify the frozen Domain Y inversion.
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
    galaxies = sorted(set(name))
    gal_data = {}
    for g in galaxies:
        gm = (name == g)
        r_kpc = R[gm]
        order = np.argsort(r_kpc)
        r_kpc = r_kpc[order]
        Vo_g, Vg_g, Vd_g, Vb_g = Vo[gm][order], Vg[gm][order], Vd[gm][order], Vb[gm][order]
        if len(r_kpc) < 4: continue

        r_m = r_kpc * KPC
        v_obs = Vo_g * KMS
        g_obs = v_obs**2 / r_m

        v_bar_sq = np.sign(Vg_g)*(Vg_g*KMS)**2 + UPS_D*(Vd_g*KMS)**2 + UPS_B*(Vb_g*KMS)**2
        v_bar_sq = np.maximum(v_bar_sq, 1e-10)
        M_bar = (v_bar_sq * r_m) / G
        M_bar = np.maximum.accumulate(M_bar)  # monotonic enclosed mass, same convention as domain_W_reformulated.py
        g_bar = G * M_bar / r_m**2

        dM_dr = np.gradient(M_bar, r_m)
        rho_bar = np.maximum(dM_dr / (4*np.pi*r_m**2), 1e-35)  # SAME estimator as domain_W_reformulated.py

        ok = (g_bar > 0) & (g_obs > 0)
        if ok.sum() < 4: continue
        gal_data[g] = dict(r=r_m[ok], gobs=g_obs[ok], gbar=g_bar[ok], rho_bar=rho_bar[ok])
    return gal_data

def invert_density(r, delta_g):
    f = r**2 * delta_g
    dfdr = np.gradient(f, r)
    return dfdr / (4*np.pi*G*r**2)

def main():
    gal_data = load()
    print(f"Domain BB: local-density nonlinearity test, {len(gal_data)} galaxies")
    print("Testing: does rho_req(r) track LOCAL rho_bar(r) linearly, or non-linearly (boosted core)?\n")

    all_rho_req, all_rho_bar, all_r_kpc = [], [], []
    galaxy_records = {}

    for name, gd in gal_data.items():
        r, gobs, gbar, rho_bar = gd["r"], gd["gobs"], gd["gbar"], gd["rho_bar"]
        delta_g = gobs - gbar
        rho_req = invert_density(r, delta_g)

        interior = np.zeros_like(rho_req, dtype=bool)
        if len(rho_req) > 2: interior[1:-1] = True
        valid = interior & np.isfinite(rho_req) & (rho_req > 0) & (rho_bar > 1e-30)

        if valid.sum() < 2: continue
        galaxy_records[name] = dict(r_kpc=(r[valid]/KPC).tolist(), rho_req=rho_req[valid].tolist(),
                                     rho_bar=rho_bar[valid].tolist())
        all_rho_req.extend(rho_req[valid].tolist())
        all_rho_bar.extend(rho_bar[valid].tolist())
        all_r_kpc.extend((r[valid]/KPC).tolist())

    all_rho_req = np.array(all_rho_req); all_rho_bar = np.array(all_rho_bar); all_r_kpc = np.array(all_r_kpc)
    print(f"valid points: {len(all_rho_req)} across {len(galaxy_records)} galaxies")
    print(f"rho_bar range: {all_rho_bar.min():.3e} to {all_rho_bar.max():.3e} kg/m^3")

    logreq = np.log10(all_rho_req)
    logbar = np.log10(all_rho_bar)

    # single free exponent p: log(rho_req) = a + p*log(rho_bar)
    A = np.column_stack([np.ones_like(logbar), logbar])
    coef, *_ = np.linalg.lstsq(A, logreq, rcond=None)
    a_fit, p_fit = coef
    pred = A @ coef
    resid = logreq - pred
    r2 = 1 - np.sum(resid**2)/np.sum((logreq-logreq.mean())**2)
    corr_pooled = np.corrcoef(logreq, logbar)[0,1]

    print(f"\nPooled fit: log10(rho_req) = {a_fit:.3f} + {p_fit:.3f} * log10(rho_bar)")
    print(f"Fitted exponent p = {p_fit:.3f}  (p=1 -> linear/ordinary gravity-like; p>1 -> boosted-core, concentration-sensitive)")
    print(f"corr(log rho_req, log rho_bar) = {corr_pooled:.3f}, R^2 = {r2:.3f}")

    # compare linear (p=1, fixed) vs the fitted-p model on RMS in log space -- galaxy-weighted, not pooled
    print("\n=== Galaxy-weighted comparison: residual scatter, linear (p=1) vs fitted p ===")
    lin_resid_all, fitp_resid_all = [], []
    per_gal_p1_rms, per_gal_fitp_rms = [], []
    for name, rec in galaxy_records.items():
        rb = np.array(rec["rho_bar"]); rq = np.array(rec["rho_req"])
        if len(rb) < 2: continue
        logrb, logrq = np.log10(rb), np.log10(rq)
        # linear model: assume rho_req = C * rho_bar (p=1), fit only the constant per galaxy via median offset
        offset1 = np.median(logrq - logrb)
        pred1 = logrb + offset1
        rms1 = np.sqrt(np.mean((logrq-pred1)**2))
        # fitted-p model (global p_fit), fit only the constant per galaxy
        offsetp = np.median(logrq - p_fit*logrb)
        predp = p_fit*logrb + offsetp
        rmsp = np.sqrt(np.mean((logrq-predp)**2))
        per_gal_p1_rms.append(rms1); per_gal_fitp_rms.append(rmsp)

    per_gal_p1_rms = np.array(per_gal_p1_rms); per_gal_fitp_rms = np.array(per_gal_fitp_rms)
    print(f"mean per-galaxy RMS, p=1 (linear):      {per_gal_p1_rms.mean():.4f} dex")
    print(f"mean per-galaxy RMS, p={p_fit:.3f} (fitted): {per_gal_fitp_rms.mean():.4f} dex")
    if per_gal_fitp_rms.mean() < per_gal_p1_rms.mean():
        print(f"-> fitted exponent p={p_fit:.3f} reduces within-galaxy scatter vs strict linear (p=1)")
    else:
        print(f"-> fitted exponent does NOT improve on strict linear -- no evidence of boosted-core nonlinearity")

    out = dict(
        n_galaxies=len(galaxy_records), n_points=len(all_rho_req),
        fitted_exponent_p=float(p_fit), fitted_intercept_a=float(a_fit),
        corr_pooled=float(corr_pooled), r2_pooled=float(r2),
        mean_per_galaxy_rms_linear_p1=float(per_gal_p1_rms.mean()),
        mean_per_galaxy_rms_fitted_p=float(per_gal_fitp_rms.mean()),
    )
    with open("domain_BB_local_density_nonlinearity_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nresults -> domain_BB_local_density_nonlinearity_results.json")

if __name__ == "__main__":
    main()
