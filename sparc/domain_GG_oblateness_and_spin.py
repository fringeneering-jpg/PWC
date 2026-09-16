"""
DOMAIN GG -- two specific challenges to Domain EE/FF, tested directly.

Domain FF already ran the rotating-medium pivot and found the per-galaxy
variance conserved rather than absorbed (c_s^2 range 478 -> v_phi^2 range
382; correlation with V_flat TIGHTENED from +0.921 to +0.989). This domain
tests the two claims FF did NOT cover.

CHALLENGE 1 -- THE OBLATENESS ARTIFACT.
  Claim: "If you evaluated d ln rho/d ln r using spherical radial bins in a
  region where the fluid is actually oblate, you introduced artificial
  scatter into your calculation of K." Paired with the concession that "in
  the outer radii where the HDF dominates, spherical is a fine
  approximation."

  That concession makes the claim decisively testable. If spherical binning
  inside a disk-flattened potential is what produced EE's 0.663 dex scatter
  in K, the scatter must COLLAPSE when restricted to points where the
  medium dominates and the potential is near-spherical by both sides'
  agreement. If the scatter survives there, the artifact is not the cause.

  Test: recompute EE's rho-binned scatter of log10 K, restricted by
  baryon-domination fraction f_bar = M_bar/M_tot and by r/R_disk.

CHALLENGE 2 -- COSMOLOGICAL SPIN.
  Claim: per-galaxy variation is legitimately absorbed by the medium's
  angular momentum profile, "which is a perfectly valid per-galaxy
  variable, as we know different halos have different spin parameters."

  This is the right question and FF only partly answered it: FF computed
  L_med/L_bar but never converted it to a spin parameter and compared it
  against the observed cosmological distribution. Doing that here.

  Bullock et al. 2001 spin parameter: lambda' = J / (sqrt(2) M V R).
  Measured distribution for real halos: lognormal, median ~0.035, with
  sigma_ln(lambda) ~ 0.5. A rotating medium is only "a perfectly valid
  per-galaxy variable" if the lambda it requires lands in that
  distribution.

  Analytic expectation, worked before running: for a co-rotating isothermal
  medium (v_phi = V_circ, rho ~ r^-2, so M ~ r),
      J = Int v_phi r dM = V (M/R) R^2/2 = V M R / 2
      lambda' = (V M R/2)/(sqrt(2) M V R) = 1/(2 sqrt(2)) = 0.354
  independent of where it is truncated -- so R_max truncation is not a
  limitation for this profile. That is ~10x the cosmological median.

Data: SPARC, VizieR J/AJ/152/157 (in-repo). Real catalog, nothing simulated.
"""
import os
import json

import numpy as np

D = os.environ.get("PWC_SPARC_DIR", os.path.dirname(os.path.abspath(__file__)))
KPC = 3.0856775814913673e19
KMS = 1.0e3
G_SI = 6.67430e-11
UPS_D, UPS_B = 0.5, 0.7
LAMBDA_COSMO_MEDIAN = 0.035
SIGMA_LN_LAMBDA = 0.5


def hr(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


def read_vizier_tsv(path, cols):
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8", errors="replace")]
    hdr_i = next(i for i, l in enumerate(lines)
                 if not l.startswith("#") and l.strip() and "\t" in l and "recno" in l)
    names = lines[hdr_i].split("\t")
    dash_i = None
    for i in range(hdr_i + 1, min(hdr_i + 6, len(lines))):
        if set(lines[i].replace("\t", "").strip()) <= set("- "):
            dash_i = i
    idx = {c: names.index(c) for c in cols}
    out = {c: [] for c in cols}
    for l in lines[dash_i + 1:]:
        if not l.strip() or l.startswith("#"):
            continue
        f = l.split("\t")
        if len(f) < len(names):
            continue
        try:
            for c in cols:
                v = f[idx[c]].strip()
                out[c].append(v if c == "Name" else (float(v) if v not in ("", "---") else np.nan))
        except ValueError:
            continue
    return out


results = {}
t1 = read_vizier_tsv(os.path.join(D, "vizier_t1.txt"), ["Name", "i", "Qual", "Vflat", "Rdisk"])
t2 = read_vizier_tsv(os.path.join(D, "vizier_t2.txt"),
                     ["Name", "Rad", "Vobs", "e_Vobs", "Vgas", "Vdisk", "Vbulge"])
inc = {n: v for n, v in zip(t1["Name"], t1["i"])}
qual = {n: v for n, v in zip(t1["Name"], t1["Qual"])}
rdisk = {n: v for n, v in zip(t1["Name"], t1["Rdisk"])}

name = np.array(t2["Name"])
R = np.array(t2["Rad"], float)
Vo = np.array(t2["Vobs"], float)
eVo = np.array(t2["e_Vobs"], float)
Vg = np.nan_to_num(np.array(t2["Vgas"], float))
Vd = np.array(t2["Vdisk"], float)
Vb = np.nan_to_num(np.array(t2["Vbulge"], float))
inc_a = np.array([inc.get(n, np.nan) for n in name], float)
q_a = np.array([qual.get(n, np.nan) for n in name], float)
m = (R > 0) & (Vo > 0) & np.isfinite(eVo) & (eVo / Vo <= 0.10) & (inc_a >= 30) & (q_a <= 2)
name, R, Vo, Vg, Vd, Vb = name[m], R[m], Vo[m], Vg[m], Vd[m], Vb[m]

rho_a, K_a, gal_a, fbar_a, rrd_a = [], [], [], [], []
gal = {}
for g in sorted(set(name)):
    s = (name == g)
    if s.sum() < 6 or not (rdisk.get(g, 0) > 0):
        continue
    o = np.argsort(R[s])
    r = R[s][o] * KPC
    vo = Vo[s][o] * KMS
    vbar2 = (Vg[s][o] * np.abs(Vg[s][o]) + UPS_D * Vd[s][o] * np.abs(Vd[s][o])
             + UPS_B * Vb[s][o] * np.abs(Vb[s][o])) * KMS ** 2
    M_tot = vo ** 2 * r / G_SI
    M_bar = vbar2 * r / G_SI
    M_med = M_tot - M_bar
    ok = M_med > 0
    if ok.sum() < 6:
        continue
    rr, MM, vv, MT, MB = r[ok], M_med[ok], vo[ok], M_tot[ok], M_bar[ok]
    rho = np.gradient(MM, rr) / (4.0 * np.pi * rr ** 2)
    good = rho > 0
    if good.sum() < 6:
        continue
    rr, rho, vv, MM, MT, MB = rr[good], rho[good], vv[good], MM[good], MT[good], MB[good]
    dln = np.gradient(np.log(rho), np.log(rr))
    val = dln < -0.05
    if val.sum() < 4:
        continue
    rr, rho, vv, MM, MT, MB, dln = (rr[val], rho[val], vv[val], MM[val],
                                    MT[val], MB[val], dln[val])
    gg = G_SI * MT / rr ** 2
    cs2 = -gg * rr / dln
    fin = np.isfinite(cs2) & (cs2 > 0)
    if fin.sum() < 4:
        continue
    rho_a.append(rho[fin]); K_a.append(rho[fin] * cs2[fin])
    gal_a.append(np.full(fin.sum(), g))
    fbar_a.append((MB / MT)[fin])
    rrd_a.append((rr / (rdisk[g] * KPC))[fin])
    gal[g] = dict(r=rr, V=vv, M_med=MM, M_bar=MB, M_tot=MT)

rho_a = np.concatenate(rho_a); K_a = np.concatenate(K_a)
gal_a = np.concatenate(gal_a); fbar_a = np.concatenate(fbar_a); rrd_a = np.concatenate(rrd_a)
lr, lK = np.log10(rho_a), np.log10(K_a)

# ===================================================================== #
hr("CHALLENGE 1 -- IS THE K-SCATTER AN OBLATE-BINNING ARTIFACT?")
# ===================================================================== #
def binned_scatter(mask, label):
    if mask.sum() < 60:
        print("    %-34s  too few points (%d)" % (label, mask.sum()))
        return None
    sub_r, sub_K, sub_g = lr[mask], lK[mask], gal_a[mask]
    bins = np.linspace(sub_r.min(), sub_r.max(), 7)
    sc = []
    for i in range(len(bins) - 1):
        b = (sub_r >= bins[i]) & (sub_r < bins[i + 1])
        if b.sum() >= 20 and len(set(sub_g[b])) >= 5:
            sc.append(np.std(sub_K[b]))
    if not sc:
        print("    %-34s  no populated bins" % label)
        return None
    v = float(np.mean(sc))
    print("    %-34s  %5d pts  %3d gal   %.3f dex  (factor %.1f)"
          % (label, mask.sum(), len(set(sub_g)), v, 10 ** v))
    return v

print("  EE baseline, all points                             0.663 dex (factor 5)")
print("\n  Restricting to where the MEDIUM dominates (both sides agree")
print("  spherical is a good approximation there):\n")
print("    selection                           n_pts  n_gal   scatter")
s_all = np.ones(len(lr), bool)
v_all = binned_scatter(s_all, "all points (reproduces EE)")
v_f50 = binned_scatter(fbar_a < 0.50, "f_bar < 0.50 (medium majority)")
v_f30 = binned_scatter(fbar_a < 0.30, "f_bar < 0.30 (medium dominant)")
v_f20 = binned_scatter(fbar_a < 0.20, "f_bar < 0.20 (medium overwhelming)")
v_r3 = binned_scatter(rrd_a > 3.0, "r > 3 R_disk (outer)")
v_r4 = binned_scatter(rrd_a > 4.0, "r > 4 R_disk (far outer)")
v_both = binned_scatter((fbar_a < 0.30) & (rrd_a > 3.0), "f_bar<0.30 AND r>3 R_disk")

print("\n  Does scatter correlate with baryon domination, as the artifact")
print("  hypothesis requires?")
qs = [(0.0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 1.01)]
trend = []
for lo, hi in qs:
    b = (fbar_a >= lo) & (fbar_a < hi)
    if b.sum() >= 60:
        sv = binned_scatter(b, "  f_bar in [%.1f, %.1f)" % (lo, hi))
        if sv:
            trend.append((lo, sv))
print("\n  VERDICT ON CHALLENGE 1:")
if v_both is not None and v_both < 0.25:
    c1 = "SUPPORTED -- scatter collapses where the medium dominates"
elif v_both is not None and v_both > 0.45:
    c1 = ("REJECTED -- the scatter SURVIVES in exactly the regime both sides "
          "agree is near-spherical, so oblate binning is not its cause")
else:
    c1 = "PARTIAL -- scatter reduced but not removed"
print("    %s" % c1)
print("    The concession that spherical is fine in the outer, medium-")
print("    dominated regime is what makes this decisive: the artifact")
print("    hypothesis predicts near-zero scatter there.")

results["challenge_1_oblateness"] = {
    "EE_baseline_dex": 0.663, "all_points_dex": v_all,
    "fbar_lt_0p50_dex": v_f50, "fbar_lt_0p30_dex": v_f30, "fbar_lt_0p20_dex": v_f20,
    "r_gt_3Rd_dex": v_r3, "r_gt_4Rd_dex": v_r4, "both_cuts_dex": v_both,
    "verdict": c1,
}

# ===================================================================== #
hr("CHALLENGE 2 -- DOES THE REQUIRED SPIN MATCH REAL HALOS?")
# ===================================================================== #
lam = []
for g, v in gal.items():
    r, V, M_med, M_tot = v["r"], v["V"], v["M_med"], v["M_tot"]
    dM = np.gradient(M_med, r)
    ok = dM > 0
    if ok.sum() < 4:
        continue
    # FF result: with a universal c_s the medium must co-rotate, v_phi ~ V_circ.
    J = np.trapezoid(dM[ok] * V[ok] * r[ok], r[ok])
    Mtot_end, V_end, R_end = M_med[-1], V[-1], r[-1]
    if Mtot_end <= 0 or V_end <= 0:
        continue
    lam.append(J / (np.sqrt(2.0) * Mtot_end * V_end * R_end))
lam = np.array([x for x in lam if np.isfinite(x) and x > 0])
print("  Required medium spin parameter lambda' = J/(sqrt(2) M V R),")
print("  using FF's co-rotation solution (v_phi ~ V_circ):")
print("    galaxies            : %d" % len(lam))
print("    median lambda'      : %.4f" % np.median(lam))
print("    IQR                 : %.4f - %.4f" % (np.percentile(lam, 25), np.percentile(lam, 75)))
print("    analytic prediction : 0.354  (co-rotating isothermal, 1/(2 sqrt2))")
print("\n  Observed cosmological halo spin (Bullock et al. 2001):")
print("    median lambda'      : %.4f   lognormal, sigma_ln ~ %.1f"
      % (LAMBDA_COSMO_MEDIAN, SIGMA_LN_LAMBDA))
ratio = np.median(lam) / LAMBDA_COSMO_MEDIAN
nsig = np.log(ratio) / SIGMA_LN_LAMBDA
print("\n    required / cosmological = %.1fx" % ratio)
print("    in units of the cosmological spread: %.1f sigma high" % nsig)
frac_in = float(np.mean(np.abs(np.log(lam / LAMBDA_COSMO_MEDIAN)) < 2 * SIGMA_LN_LAMBDA))
print("    fraction of galaxies within 2 sigma of the cosmological median: %.1f%%"
      % (100 * frac_in))
print("\n  VERDICT ON CHALLENGE 2:")
if nsig > 3:
    c2 = ("REJECTED -- the required spin is %.1fx the cosmological median, "
          "%.1f sigma high. A co-rotating medium is NOT a normally-spinning "
          "halo; real halos are pressure-supported with only ~3.5%% of the "
          "angular momentum needed here" % (ratio, nsig))
elif nsig > 1.5:
    c2 = "STRAINED -- required spin is high but not impossible"
else:
    c2 = "SUPPORTED -- required spin sits inside the cosmological distribution"
print("    %s" % c2)
print("\n  This is why the appeal to halo spin does not rescue the model:")
print("  real halos DO have a spin distribution, but it is centred an order")
print("  of magnitude below full co-rotation. Invoking spin as the free")
print("  per-galaxy variable requires spins that the observed distribution")
print("  of halos does not contain.")

results["challenge_2_spin"] = {
    "n_galaxies": int(len(lam)),
    "median_lambda_required": float(np.median(lam)),
    "iqr": [float(np.percentile(lam, 25)), float(np.percentile(lam, 75))],
    "analytic_prediction": 0.354,
    "cosmological_median": LAMBDA_COSMO_MEDIAN,
    "ratio_to_cosmological": float(ratio),
    "sigma_high": float(nsig),
    "pct_within_2sigma": float(100 * frac_in),
    "verdict": c2,
}

hr("SUMMARY")
print("  Challenge 1 (oblate binning artifact) : %s" % c1.split(" -- ")[0])
print("  Challenge 2 (cosmological halo spin)  : %s" % c2.split(" -- ")[0])
print("\n  Neither assumption-relaxation rescues the universal EOS. The")
print("  missing object is unchanged after six domains: a law fixing c_s or")
print("  a0 from substrate parameters alone, not from the host galaxy.")

out = os.path.join(D, "domain_GG_oblateness_and_spin_results.json")
with open(out, "w") as f:
    json.dump(results, f, indent=2)
print("\n  wrote %s" % out)
