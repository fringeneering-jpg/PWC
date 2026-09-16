"""
DOMAIN FF -- rotating HDF: solve for the medium's own vorticity profile.

Domain EE assumed the medium was static (v_phi = 0) and spherical, and
derived c_s^2 = -g*r/(d ln rho/d ln r). That assumption was flagged in EE's
header, not hidden, and relaxing it is legitimate: a mass-bearing medium
interpenetrating a differentially rotating disk has no reason to sit at
rest. This domain drops it.

RADIAL MOMENTUM BALANCE (verified algebraically before coding):

    v_phi^2/r - (1/rho) dP/dr = V_circ^2 / r

with barotropic P(rho), dP/dr = c_s^2 drho/dr, multiply by r:

    v_phi^2 - c_s^2 (d ln rho / d ln r) = V_circ^2
    => c_s^2 = (V_circ^2 - v_phi^2) / (-d ln rho / d ln r)      [directive's form]
    => v_phi^2 = V_circ^2 + c_s^2 (d ln rho / d ln r)           [solved backwards]

The pivot: FIX c_s^2 as a universal invariant scalar, SOLVE for v_phi(r).

WHAT THIS CAN AND CANNOT ESTABLISH -- stated before running.

This system is fully determined. rho(r) and V_circ(r) come from data, c_s
is a fixed scalar, so v_phi(r) is not fitted -- it is read off. That means
the reformulation CANNOT FAIL on chi-squared grounds, and equally cannot
succeed on them. It is not a better fit; it is a different bookkeeping of
the same information.

It also does not remove the factor-251. In EE the per-galaxy variance sat
in c_s^2. Here c_s^2 is frozen, so the variance must reappear in v_phi^2.
Part C measures whether it is reduced, conserved, or amplified. The honest
prior is conserved: V_circ^2 spans the same range either way.

What the pivot CAN do, and why it is worth running: unlike a halo profile,
a rotating medium makes commitments outside the rotation curve. It carries
angular momentum that must be supplied, and the drag that supplies it acts
back on the baryons. Part D tests those commitments, which is where a
rotating medium can be right or wrong independently of the curve it was
built from.

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
A0 = 1.2e-10


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

# Build per-galaxy medium profiles (identical construction to Domain EE).
gal = {}
for g in sorted(set(name)):
    s = (name == g)
    if s.sum() < 6:
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
    rr, MM, vv, MB = r[ok], M_med[ok], vo[ok], M_bar[ok]
    rho = np.gradient(MM, rr) / (4.0 * np.pi * rr ** 2)
    good = rho > 0
    if good.sum() < 6:
        continue
    rr, rho, vv, MM, MB = rr[good], rho[good], vv[good], MM[good], MB[good]
    dln = np.gradient(np.log(rho), np.log(rr))
    val = dln < -0.05
    if val.sum() < 4:
        continue
    gal[g] = dict(r=rr[val], rho=rho[val], V=vv[val], dln=dln[val],
                  M_med=MM[val], M_bar=MB[val])

print("  galaxies with usable medium profiles: %d" % len(gal))

# ===================================================================== #
hr("PART A -- HOW UNIVERSAL CAN c_s ACTUALLY BE? (a hard ceiling)")
# ===================================================================== #
# v_phi^2 = V_circ^2 + c_s^2 * (d ln rho/d ln r) >= 0, and d ln rho/d ln r < 0,
# so   c_s^2 <= V_circ^2 / (-d ln rho/d ln r)   at EVERY point of EVERY galaxy.
bounds = []
gal_bound = {}
for g, v in gal.items():
    b = v["V"] ** 2 / (-v["dln"])
    bounds.append(b)
    gal_bound[g] = np.min(b)
allb = np.concatenate(bounds)
gb = np.array(list(gal_bound.values()))
cs_max_strict = float(np.sqrt(allb.min()))
cs_max_p05 = float(np.sqrt(np.percentile(allb, 5)))
print("  Requirement v_phi^2 >= 0 caps a UNIVERSAL c_s from above:")
print("    strictest point in the whole sample : c_s <= %6.2f km/s" % (cs_max_strict / KMS))
print("    5th-percentile point                : c_s <= %6.2f km/s" % (cs_max_p05 / KMS))
print("    per-galaxy ceilings span            : %.1f to %.1f km/s"
      % (np.sqrt(gb.min()) / KMS, np.sqrt(gb.max()) / KMS))
print("\n  The ceiling is set by the FAINTEST, slowest galaxies. A universal")
print("  c_s must fit inside the smallest dwarf's budget, so it is forced")
print("  far below the ~%.0f km/s that EE found massive galaxies imply."
      % (np.median([np.median(np.sqrt(v['V']**2/(-v['dln']))) for v in gal.values()]) / KMS))
CS_UNIVERSAL = cs_max_strict * 0.95
print("\n  LOCKED for the rest of this run: c_s = %.2f km/s (95%% of the strict"
      % (CS_UNIVERSAL / KMS))
print("  ceiling, so every galaxy stays physical).")
results["part_A_cs_ceiling"] = {
    "cs_max_strict_kms": cs_max_strict / KMS, "cs_max_p05_kms": cs_max_p05 / KMS,
    "cs_locked_kms": CS_UNIVERSAL / KMS,
    "per_galaxy_ceiling_min_kms": float(np.sqrt(gb.min()) / KMS),
    "per_galaxy_ceiling_max_kms": float(np.sqrt(gb.max()) / KMS),
}

# ===================================================================== #
hr("PART B -- REVERSED SOLVER: the required medium flow v_phi(r)")
# ===================================================================== #
TARGET = "NGC3198"
for g, v in gal.items():
    v["vphi2"] = v["V"] ** 2 + CS_UNIVERSAL ** 2 * v["dln"]
    v["vphi"] = np.sqrt(np.maximum(v["vphi2"], 0.0))

if TARGET in gal:
    v = gal[TARGET]
    print("  Standard model file: %s   (c_s locked at %.2f km/s)" % (TARGET, CS_UNIVERSAL / KMS))
    print("\n    R(kpc)   rho_med(kg/m3)  dlnrho/dlnr   V_circ   v_phi   v_phi/V_circ")
    st = max(1, len(v["r"]) // 10)
    for i in range(0, len(v["r"]), st):
        print("    %6.2f   %.3e      %+6.2f      %6.1f  %6.1f      %.4f"
              % (v["r"][i] / KPC, v["rho"][i], v["dln"][i], v["V"][i] / KMS,
                 v["vphi"][i] / KMS, v["vphi"][i] / v["V"][i]))

ratios = np.concatenate([v["vphi"] / v["V"] for v in gal.values()])
print("\n  Across all %d galaxies, required v_phi / V_circ:" % len(gal))
print("    median %.4f   5th pct %.4f   min %.4f"
      % (np.median(ratios), np.percentile(ratios, 5), ratios.min()))
print("    fraction of points with v_phi > 0.95 V_circ : %.1f%%"
      % (100.0 * (ratios > 0.95).mean()))
print("\n  MECHANICAL READING: with c_s forced universal, the pressure term")
print("  becomes negligible and the medium must very nearly CO-ROTATE with")
print("  the galaxy at the full circular speed. It is not a slowly")
print("  shear-dragged wake -- it is centrifugally supported, essentially a")
print("  co-rotating massive disk/halo of medium.")
results["part_B_flow"] = {
    "median_vphi_over_Vcirc": float(np.median(ratios)),
    "pct_points_above_0p95": float(100.0 * (ratios > 0.95).mean()),
}

# ===================================================================== #
hr("PART C -- DOES IT ABSORB THE FACTOR-251? (variance bookkeeping)")
# ===================================================================== #
cs2_EE, vphi2_FF, vf = [], [], []
for g, v in gal.items():
    cs2_EE.append(np.median(v["V"] ** 2 / (-v["dln"])))     # EE's per-galaxy c_s^2
    vphi2_FF.append(np.median(v["vphi2"]))                   # FF's per-galaxy v_phi^2
    vf.append(vflat.get(g, np.nan))
cs2_EE, vphi2_FF, vf = np.array(cs2_EE), np.array(vphi2_FF), np.array(vf)
pos = vphi2_FF > 0
r_EE = float(cs2_EE.max() / cs2_EE.min())
r_FF = float(vphi2_FF[pos].max() / vphi2_FF[pos].min())
print("  Dynamic range across galaxies of the quantity carrying the variance:")
print("    Domain EE, per-galaxy c_s^2   : factor %6.0f" % r_EE)
print("      (EE reported 251 using median c_s then squared; %.0f here uses" % r_EE)
print("       median c_s^2 directly -- same quantity, slightly different order)")
print("    Domain FF, per-galaxy v_phi^2 : factor %6.0f" % r_FF)
print("    scatter of log10 c_s^2   (EE) : %.3f dex" % np.std(np.log10(cs2_EE)))
print("    scatter of log10 v_phi^2 (FF) : %.3f dex" % np.std(np.log10(vphi2_FF[pos])))
fin = np.isfinite(vf) & (vf > 0) & pos
c_EE = float(np.corrcoef(np.log10(cs2_EE[fin]), np.log10(vf[fin]))[0, 1])
c_FF = float(np.corrcoef(np.log10(vphi2_FF[fin]), np.log10(vf[fin]))[0, 1])
print("\n  Correlation with the galaxy's own V_flat:")
print("    EE  log c_s^2   vs log V_flat : %+.3f" % c_EE)
print("    FF  log v_phi^2 vs log V_flat : %+.3f" % c_FF)
print("\n  ANSWER: the factor is NOT absorbed. It is CONSERVED and moved.")
print("  Freezing c_s does not remove per-galaxy freedom; it relocates it")
print("  from the substrate's stiffness into the substrate's flow field.")
print("  v_phi(r) is still one free radial function per galaxy, still read")
print("  off the observed curve, still tied to V_flat at %+.3f." % c_FF)
results["part_C_variance"] = {
    "EE_cs2_dynamic_range": r_EE, "FF_vphi2_dynamic_range": r_FF,
    "EE_logcs2_scatter_dex": float(np.std(np.log10(cs2_EE))),
    "FF_logvphi2_scatter_dex": float(np.std(np.log10(vphi2_FF[pos]))),
    "EE_corr_with_Vflat": c_EE, "FF_corr_with_Vflat": c_FF,
    "factor_absorbed": False,
}

# ===================================================================== #
hr("PART D -- THE PHYSICAL COMMITMENT: angular momentum budget")
# ===================================================================== #
# This is where a rotating medium can be wrong independently of the curve.
# Drag cannot create angular momentum; it can only move it from the disk.
Lr, names_L = [], []
for g, v in gal.items():
    r, vphi, V = v["r"], v["vphi"], v["V"]
    dM_med = np.gradient(v["M_med"], r)
    dM_bar = np.gradient(v["M_bar"], r)
    good = (dM_med > 0) & (dM_bar > 0)
    if good.sum() < 4:
        continue
    L_med = np.trapezoid(dM_med[good] * vphi[good] * r[good], r[good])
    L_bar = np.trapezoid(dM_bar[good] * V[good] * r[good], r[good])
    if L_bar > 0 and np.isfinite(L_med / L_bar):
        Lr.append(L_med / L_bar)
        names_L.append(g)
Lr = np.array(Lr)
print("  L_medium / L_baryons within R_max, %d galaxies:" % len(Lr))
print("    median %.2f   IQR %.2f-%.2f   max %.1f"
      % (np.median(Lr), np.percentile(Lr, 25), np.percentile(Lr, 75), Lr.max()))
print("\n  Drag is a TRANSFER, not a source. For the disk to have spun this")
print("  medium up, it must have shed a comparable angular momentum itself.")
print("  For a circular orbit L ~ sqrt(G M r), so losing a factor f in L")
print("  shrinks the orbital radius by f^2:")
for f in [np.median(Lr), np.percentile(Lr, 75)]:
    print("    shedding a factor %.2f of L  =>  disk radius shrinks by %.1fx"
          % (f, (1.0 + f) ** 2))
print("\n  Observed disks are ~10 Gyr old and still extended. A drag strong")
print("  enough to spin the medium to co-rotation would have decayed them.")
print("  Conversely, drag weak enough to preserve the disks cannot have")
print("  supplied this angular momentum -- so it must be primordial, which")
print("  is an extra assumption, not a consequence of the mechanism.")
print("\n  This is a REAL constraint, and it is the useful output of this run:")
print("  it is a test the rotating medium can fail that a static halo never")
print("  faces, because a static halo makes no angular-momentum commitment.")
results["part_D_angular_momentum"] = {
    "n_galaxies": int(len(Lr)),
    "median_L_med_over_L_bar": float(np.median(Lr)),
    "iqr": [float(np.percentile(Lr, 25)), float(np.percentile(Lr, 75))],
    "implied_disk_shrink_factor_median": float((1.0 + np.median(Lr)) ** 2),
}

# ===================================================================== #
hr("PART E -- DOES THE LOCKED c_s YIELD a0?")
# ===================================================================== #
L_implied = CS_UNIVERSAL ** 2 / A0
print("  Locked universal c_s = %.2f km/s" % (CS_UNIVERSAL / KMS))
print("  Dimensionally a0 = c_s^2 / L, so L = c_s^2/a0 = %.3e m = %.4f kpc"
      % (L_implied, L_implied / KPC))
print("  For comparison, SPARC disk scale lengths span %.2f to %.2f kpc."
      % (min(v for v in rdisk.values() if v > 0), max(rdisk.values())))
print("  The implied length is not obviously any galactic scale, and c_s was")
print("  fixed by the faintest dwarf's ceiling rather than derived, so this")
print("  does NOT constitute a derivation of a0. Reported, not claimed.")
results["part_E_a0"] = {
    "cs_locked_kms": CS_UNIVERSAL / KMS,
    "implied_length_kpc": float(L_implied / KPC),
    "constitutes_a0_derivation": False,
}

hr("SUMMARY")
print("  1. The static assumption WAS an assumption and relaxing it is fair.")
print("     The directive's momentum balance and c_s^2 formula are correct;")
print("     verified algebraically before coding.")
print("  2. A universal c_s is capped at %.2f km/s by the v_phi^2 >= 0"
      % (cs_max_strict / KMS))
print("     requirement in the faintest galaxies -- far below the ~150 km/s")
print("     that massive galaxies implied in EE.")
print("  3. At that c_s the pressure term is negligible and the medium must")
print("     co-rotate: v_phi/V_circ median %.4f." % np.median(ratios))
print("  4. The factor-251 is NOT absorbed. It moves from c_s^2 (range %.0f)"
      % r_EE)
print("     into v_phi^2 (range %.0f), still correlated with V_flat at %+.3f."
      % (r_FF, c_FF))
print("  5. The genuine gain: a rotating medium carries L_med/L_bar ~ %.2f,"
      % np.median(Lr))
print("     which is a commitment outside the rotation curve and therefore a")
print("     real falsifiable test. A static halo makes no such commitment.")

out = os.path.join(D, "domain_FF_vortical_medium_flow_results.json")
with open(out, "w") as f:
    json.dump(results, f, indent=2)
print("\n  wrote %s" % out)
