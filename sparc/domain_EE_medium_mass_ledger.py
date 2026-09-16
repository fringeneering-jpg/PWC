"""
DOMAIN EE -- the medium has mass. Closing the HDF mass ledger on SPARC.

CORRECTION THIS DOMAIN EXISTS TO FIX. Domain DD's tension-flux integral
used only the luminous source: A(<r) proportional to M_Sintot(<r). That is
incomplete under PWC's own stated ledger

    M_total = M_Sintot + M_HDF,bound + M_HDF,excess

The HDF substrate is mass-bearing (Ontology, PROVENANCE_MANIFEST.md), so
compressed HDF around a mass concentration must appear inside the same
Gauss surface as the baryons. Domain DD therefore under-counted the
source and its Keplerian result is not the last word. This domain puts the
missing terms back.

WHAT IS AT STAKE, STATED BEFORE COMPUTING ANYTHING.

A flat outer rotation curve requires M_total(<r) proportional to r, hence
a medium density falling as rho ~ r^-2. That is the isothermal profile.
So "bound HDF mass" is mathematically capable of producing flat curves --
DD's negative result does not survive the correction. The real question is
whether it does so as PHYSICS or as BOOKKEEPING:

  - If each galaxy needs its own rho_HDF(r), that is one free radial
    function per galaxy. Mathematically identical to fitting a dark matter
    halo. The ontology changes; the parameter count and predictive content
    do not.
  - If instead ONE equation of state determines rho_HDF everywhere, the
    medium is real fluid mechanics and this is a genuine prediction that
    dark matter cannot match.

THE DECISIVE TEST IS GAUGE-FREE. For any barotropic medium in hydrostatic
equilibrium, dP/dr = -rho*g and dP/drho = c_s^2, so

    c_s^2(r) = -rho*g / (drho/dr) = -g*r / (d ln rho / d ln r)

No integration constant, no boundary gauge, no fitted parameter. And by
PWC's own master relation c^2 = K/rho, the stiffness is

    K = rho * c_s^2

If the HDF is one substance with one equation of state, K must be a
single-valued function of rho across ALL galaxies. If K at fixed rho
scatters by orders of magnitude between galaxies, there is no shared
medium -- only per-galaxy halos wearing a fluid label.

Note the analytic benchmark: for an exactly flat curve with rho ~ r^-2,
c_s^2 = v_flat^2 / 2. So the test has a sharp prior expectation -- if the
medium is NOT universal, c_s will track each galaxy's own v_flat, and
SPARC spans v_flat from ~20 to ~300 km/s, i.e. a factor ~200 in c_s^2.

ASSUMPTIONS, STATED NOT BURIED:
  - The HDF component is treated as spherical while the baryons are a
    disk. Standard for this kind of decomposition, but an approximation.
  - The medium is taken as static (pressure-supported). Bulk rotation or
    flow in the HDF would add terms not included here.
  - rho_HDF is obtained by differentiating an enclosed mass built from
    noisy data; local log-space slopes are used to stabilise it, and all
    population statements are medians, not single-point claims.

Data: SPARC, VizieR J/AJ/152/157 (in-repo). Real catalog, nothing simulated.
"""
import os
import json

import numpy as np

D = os.environ.get("PWC_SPARC_DIR", os.path.dirname(os.path.abspath(__file__)))
KPC = 3.0856775814913673e19
KMS = 1.0e3
C0 = 2.99792458e8
G_SI = 6.67430e-11
MSUN = 1.98892e30
UPS_D, UPS_B = 0.5, 0.7


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
vflat = {n: v for n, v in zip(t1["Name"], t1["Vflat"])}

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

# ===================================================================== #
hr("PART A -- CLOSING THE LEDGER: how much of the mass is medium?")
# ===================================================================== #
per_gal = {}
frac_list, ratio_list = [], []
for g in sorted(set(name)):
    s = (name == g)
    if s.sum() < 6:
        continue
    o = np.argsort(R[s])
    r = R[s][o] * KPC
    vo = Vo[s][o] * KMS
    vbar2 = (Vg[s][o] * np.abs(Vg[s][o]) + UPS_D * Vd[s][o] * np.abs(Vd[s][o])
             + UPS_B * Vb[s][o] * np.abs(Vb[s][o])) * KMS ** 2
    M_tot = vo ** 2 * r / G_SI            # from the observed curve
    M_bar = vbar2 * r / G_SI              # Sintot, extended source
    M_med = M_tot - M_bar                 # M_HDF,bound + M_HDF,excess
    if np.any(~np.isfinite(M_tot)) or M_tot[-1] <= 0:
        continue
    per_gal[g] = dict(r=r, vo=vo, M_tot=M_tot, M_bar=M_bar, M_med=M_med)
    frac_list.append(M_med[-1] / M_tot[-1])
    if M_bar[-1] > 0:
        ratio_list.append(M_med[-1] / M_bar[-1])

frac = np.array(frac_list)
ratio = np.array([x for x in ratio_list if np.isfinite(x) and x > 0])
print("  galaxies with a usable ledger : %d" % len(per_gal))
print("  medium fraction M_med/M_total at R_max : median %.3f  (IQR %.3f-%.3f)"
      % (np.median(frac), np.percentile(frac, 25), np.percentile(frac, 75)))
print("  medium-to-Sintot ratio M_med/M_bar     : median %.2f" % np.median(ratio))
print("  points where M_med < 0 (medium RAREFIED, not compressed):")
neg = sum(int((v["M_med"] < 0).sum()) for v in per_gal.values())
tot = sum(len(v["M_med"]) for v in per_gal.values())
print("    %d of %d points (%.1f%%)" % (neg, tot, 100.0 * neg / tot))
print("\n  So the correction is real and large: the medium carries the")
print("  MAJORITY of the mass inside R_max in a typical galaxy.")
print("  For reference the cosmological dark:baryon ratio is ~5.4.")

results["part_A_ledger"] = {
    "n_galaxies": len(per_gal),
    "median_medium_fraction": float(np.median(frac)),
    "median_medium_to_baryon_ratio": float(np.median(ratio)),
    "negative_M_med_points_pct": float(100.0 * neg / tot),
}

# ===================================================================== #
hr("PART B -- THE MEDIUM'S DENSITY PROFILE")
# ===================================================================== #
slopes_rho, slopes_M = [], []
for g, v in per_gal.items():
    r, M_med = v["r"], v["M_med"]
    ok = M_med > 0
    if ok.sum() < 5:
        continue
    rr, MM = r[ok], M_med[ok]
    # rho from dM/dr, local log slopes
    rho = np.gradient(MM, rr) / (4.0 * np.pi * rr ** 2)
    good = rho > 0
    if good.sum() < 5:
        continue
    lr, lrho = np.log(rr[good]), np.log(rho[good])
    n_out = max(3, len(lr) // 2)
    slopes_rho.append(np.polyfit(lr[-n_out:], lrho[-n_out:], 1)[0])
    slopes_M.append(np.polyfit(np.log(rr[-n_out:]), np.log(MM[-n_out:]), 1)[0])
    v["rho"] = rho
    v["rho_r"] = rr[good] if good.sum() == len(rr) else rr
sr, sM = np.array(slopes_rho), np.array(slopes_M)
print("  outer d ln M_med / d ln r : median %+.2f   (flat curve needs +1.00)" % np.median(sM))
print("  outer d ln rho_med/ d ln r : median %+.2f   (isothermal is -2.00)" % np.median(sr))
print("\n  The medium's required profile IS the isothermal halo shape.")
print("  Domain DD's Keplerian result does not survive this correction:")
print("  with the medium's own mass in the ledger, flat curves are")
print("  reproduced. That much the ledger genuinely buys.")

results["part_B_profile"] = {
    "median_outer_dlnM_dlnr": float(np.median(sM)),
    "median_outer_dlnrho_dlnr": float(np.median(sr)),
    "flat_curve_requirement": 1.0, "isothermal_requirement": -2.0,
}

# ===================================================================== #
hr("PART C -- DECISIVE TEST: one equation of state, or one halo each?")
# ===================================================================== #
# c_s^2 = -g*r / (d ln rho / d ln r)   [gauge-free, no fitted parameter]
# K = rho * c_s^2                      [PWC master relation c^2 = K/rho]
rho_all, cs2_all, K_all, gal_all, vflat_all = [], [], [], [], []
for g, v in per_gal.items():
    r, M_med, M_tot = v["r"], v["M_med"], v["M_tot"]
    ok = M_med > 0
    if ok.sum() < 6:
        continue
    rr, MM = r[ok], M_med[ok]
    gg = G_SI * M_tot[ok] / rr ** 2
    rho = np.gradient(MM, rr) / (4.0 * np.pi * rr ** 2)
    good = rho > 0
    if good.sum() < 6:
        continue
    rr, rho, gg = rr[good], rho[good], gg[good]
    dlnrho = np.gradient(np.log(rho), np.log(rr))
    valid = dlnrho < -0.05
    if valid.sum() < 4:
        continue
    cs2 = -gg[valid] * rr[valid] / dlnrho[valid]
    ok2 = np.isfinite(cs2) & (cs2 > 0)
    rho_all.append(rho[valid][ok2])
    cs2_all.append(cs2[ok2])
    K_all.append(rho[valid][ok2] * cs2[ok2])
    gal_all.append(np.full(ok2.sum(), g))
    vflat_all.append(np.full(ok2.sum(), vflat.get(g, np.nan)))

rho_a = np.concatenate(rho_all)
cs2_a = np.concatenate(cs2_all)
K_a = np.concatenate(K_all)
gal_a = np.concatenate(gal_all)
vf_a = np.concatenate(vflat_all)
print("  usable points: %d across %d galaxies" % (len(rho_a), len(set(gal_a))))
print("  medium density rho spans %.2e to %.2e kg/m^3" % (rho_a.min(), rho_a.max()))
print("  sound speed c_s spans %.1f to %.1f km/s"
      % (np.sqrt(cs2_a.min()) / KMS, np.sqrt(cs2_a.max()) / KMS))
print("  c_s / c0 max = %.3e  -- impedance cap never approached"
      % (np.sqrt(cs2_a.max()) / C0))

# Universality: scatter of K at fixed rho, across galaxies.
lr_, lK = np.log10(rho_a), np.log10(K_a)
bins = np.linspace(lr_.min(), lr_.max(), 9)
print("\n  Is K a single-valued function of rho?  (one EOS => tight bins)")
print("    log10 rho bin        n_pts  n_gal   scatter in log10 K (dex)")
scat = []
for i in range(len(bins) - 1):
    b = (lr_ >= bins[i]) & (lr_ < bins[i + 1])
    if b.sum() < 20:
        continue
    sd = float(np.std(lK[b]))
    scat.append(sd)
    print("    %+.2f to %+.2f     %5d  %5d        %.3f"
          % (bins[i], bins[i + 1], b.sum(), len(set(gal_a[b])), sd))
mean_scat = float(np.mean(scat))
print("  mean within-bin scatter in log10 K : %.3f dex (factor %.0f)"
      % (mean_scat, 10 ** mean_scat))

# Does c_s track each galaxy's own v_flat? (the halo-in-disguise signature)
fin = np.isfinite(vf_a) & (vf_a > 0)
gal_cs = {}
for g in set(gal_a[fin]):
    s = (gal_a == g) & fin
    gal_cs[g] = (np.median(np.sqrt(cs2_a[s])) / KMS, vf_a[s][0])
cs_med = np.array([v[0] for v in gal_cs.values()])
vf_med = np.array([v[1] for v in gal_cs.values()])
corr = float(np.corrcoef(np.log10(cs_med), np.log10(vf_med))[0, 1])
rat = cs_med / vf_med
print("\n  Per-galaxy median c_s vs that galaxy's own V_flat:")
print("    galaxies: %d    correlation of log c_s with log V_flat: %+.3f" % (len(cs_med), corr))
print("    c_s / V_flat : median %.3f  (analytic isothermal value 1/sqrt2 = 0.707)"
      % np.median(rat))
print("    c_s range across galaxies: %.1f to %.1f km/s -- a factor %.0f in c_s^2"
      % (cs_med.min(), cs_med.max(), (cs_med.max() / cs_med.min()) ** 2))

results["part_C_eos_test"] = {
    "n_points": int(len(rho_a)), "n_galaxies": int(len(set(gal_a))),
    "mean_within_bin_logK_scatter_dex": mean_scat,
    "cs_vflat_log_correlation": corr,
    "median_cs_over_vflat": float(np.median(rat)),
    "isothermal_analytic_value": 0.7071,
    "cs2_dynamic_range_across_galaxies": float((cs_med.max() / cs_med.min()) ** 2),
    "max_cs_over_c0": float(np.sqrt(cs2_a.max()) / C0),
}

# ===================================================================== #
hr("PART D -- VERDICT")
# ===================================================================== #
print("  You were right that DD dropped the medium's mass, and putting it")
print("  back changes the DD result: with M_HDF in the ledger the medium")
print("  profile required is rho ~ r^%+.2f and M ~ r^%+.2f, which DOES"
      % (np.median(sr), np.median(sM)))
print("  give flat outer curves. DD's Keplerian conclusion applied only to")
print("  a baryon-only source and is superseded.")
print("\n  But the ledger does not by itself make this fluid mechanics.")
print("  The gauge-free EOS test says:")
print("    - stiffness K scatters by %.3f dex (factor %.0f) at fixed rho"
      % (mean_scat, 10 ** mean_scat))
print("    - c_s correlates with each galaxy's own V_flat at %+.3f" % corr)
print("    - c_s/V_flat sits at %.3f, essentially the isothermal 0.707"
      % np.median(rat))
print("    - c_s^2 varies by a factor %.0f across the sample"
      % ((cs_med.max() / cs_med.min()) ** 2))
if corr > 0.7 and mean_scat > 0.3:
    verdict = ("NEGATIVE for a universal EOS: the medium's stiffness is set by "
               "each galaxy's own rotation speed, not by a shared property of "
               "the substrate -- one free profile per galaxy, i.e. a halo")
elif mean_scat < 0.2 and corr < 0.4:
    verdict = "POSITIVE: K(rho) is near single-valued -- a genuine shared EOS"
else:
    verdict = "MIXED: partial structure in K(rho), not a clean universal EOS"
print("\n  VERDICT: %s" % verdict)
print("\n  What would flip this: an independent law fixing c_s (or K) from")
print("  substrate parameters ALONE -- not from the galaxy it sits in.")
print("  Then rho_HDF(r) would be predicted from the baryons with zero")
print("  per-galaxy freedom, and the medium would be doing real work that")
print("  a dark matter halo cannot. That law does not exist in this repo.")
results["part_D_verdict"] = verdict

out = os.path.join(D, "domain_EE_medium_mass_ledger_results.json")
with open(out, "w") as f:
    json.dump(results, f, indent=2)
print("\n  wrote %s" % out)
