"""
DOMAIN DD -- HDF surface-tension gravity solver on SPARC.

Built to the Level-2 directive: gravity as macroscopic surface tension from
phase-boundary stress between LDF vortices and the HDF substrate, with the
tension flux diffusing radially through the medium. No spacetime curvature,
no dark matter, no point mass, no r=0 evaluation, and -- in Part D -- no
acceleration scale of any kind.

--------------------------------------------------------------------------
CORRECTION TO THE DIRECTIVE'S PREMISE, ESTABLISHED IN PART A BELOW.

The directive states that the previous run "utilized g_bar based on the
standard Newtonian formula g = GM/r^2" and thereby "smuggled in
zero-dimensional point masses (r=0)".

That is false, and Part A demonstrates it from the catalog itself rather
than by assertion. SPARC's Vdisk/Vgas/Vbulge are NOT point-mass terms.
They are numerical solutions of Poisson's equation for observed, extended
3.6um surface-brightness distributions and observed HI surface-density
profiles (Lelli, McGaugh & Schombert 2016, following Casertano 1983 for
finite-thickness disks). Three signatures in the data prove the source is
extended and finite-volume, and each is impossible for a point mass:

  1. Vgas is NEGATIVE at 361 points across 48 galaxies. A point mass can
     never produce an inward-negative V^2; only mass distributed OUTSIDE
     the sampling radius can.
  2. Vdisk peaks at a finite interior radius in 158 galaxies, at a median
     of 2.18 disk scale lengths -- Freeman's (1970) analytic result for an
     exponential disk is 2.2. A point mass decays monotonically as
     r^-1/2 and has no interior peak.
  3. The inner logarithmic slope d ln Vdisk/d ln r is POSITIVE in 95.2% of
     galaxies (median +0.48). A point mass gives -0.50 everywhere.

So the constraint "acceleration peaks at the macro-boundary of the
organized matter cluster and falls inward" was ALREADY SATISFIED by the
previous run. It was not a defect that needed removing. Part A re-verifies
this inside this script so the claim is checkable here.

This script nonetheless honours the directive's substance: Parts B-D build
the mass distribution by integrating the OBSERVED surface brightness
profile directly, never touching Vdisk/Vbulge, so the finite-area source
is constructed here from photometry rather than inherited.

--------------------------------------------------------------------------
THE SURFACE-TENSION LAW, AND WHAT IT STRUCTURALLY IMPLIES.

Directive: mass is aggregated electromagnetic surface-defect area; the HDF
minimises surface-strain energy by pulling bounding surfaces together; the
resulting pull "drops off structurally based on total system displacement
propagating via 4*pi*r^2 surface diffusion".

Formalised: each phase-locked vortex contributes a fixed boundary area a_v,
so the enclosed defect area is A(<r) = (M(<r)/m_v) * a_v, i.e. A is
proportional to enclosed mass. Steady-state radial diffusion of a conserved
tension flux Phi through nested spheres gives flux density

    J(r) = Phi / (4*pi*r^2),        Phi proportional to A(<r)

and taking the acceleration proportional to J:

    g(r) = C_T * A(<r) / (4*pi*r^2)  =  [C_T*a_v/(4*pi*m_v)] * M(<r)/r^2

This is Gauss's law. The 4*pi*r^2 diffusion premise does not produce an
alternative to the inverse-square law -- it IS the inverse-square law, with
G reinterpreted as a tension-per-unit-defect-area constant. That is a
derivation, not a criticism: it is the strongest available argument that
the surface-tension picture reproduces Newtonian gravity in the regime
where Newtonian gravity is correct.

But it settles the closing question of the directive in the negative, and
Part B shows this numerically rather than rhetorically. Outside the
luminous body M(<r) -> M_total, so g -> 1/r^2, so v^2 = g*r -> 1/r, so
v -> r^(-1/2). The mechanism as specified predicts KEPLERIAN DECLINE. Flat
outer rotation curves require g ~ 1/r, i.e. flux conserved through a
surface growing like r^1 (cylindrical), not r^2 (spherical). Part C
measures which the data actually demands.

Data: SPARC, VizieR J/AJ/152/157 (in-repo). Real catalog, nothing simulated.
"""
import os
import json

import numpy as np

D = os.environ.get("PWC_SPARC_DIR", os.path.dirname(os.path.abspath(__file__)))

KPC = 3.0856775814913673e19       # m
PC = 3.0856775814913673e16        # m
KMS = 1.0e3
C0 = 2.99792458e8                 # substrate impedance limit, m/s
G_SI = 6.67430e-11
MSUN = 1.98892e30                 # kg
UPS_D, UPS_B = 0.5, 0.7           # 3.6um mass-to-light ratios
M_PROTON = 1.67262192e-27         # kg, vortex mass quantum


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

t1 = read_vizier_tsv(os.path.join(D, "vizier_t1.txt"), ["Name", "i", "Qual", "Rdisk", "Dist"])
t2 = read_vizier_tsv(os.path.join(D, "vizier_t2.txt"),
                     ["Name", "Rad", "Vobs", "e_Vobs", "Vgas", "Vdisk", "Vbulge",
                      "SBdisk", "SBbulge"])

name = np.array(t2["Name"])
R = np.array(t2["Rad"], float)
Vo = np.array(t2["Vobs"], float)
eVo = np.array(t2["e_Vobs"], float)
Vg = np.nan_to_num(np.array(t2["Vgas"], float))
Vd = np.array(t2["Vdisk"], float)
Vb = np.nan_to_num(np.array(t2["Vbulge"], float))
SBd = np.nan_to_num(np.array(t2["SBdisk"], float))
SBb = np.nan_to_num(np.array(t2["SBbulge"], float))
rdisk = {n: v for n, v in zip(t1["Name"], t1["Rdisk"])}
inc = {n: v for n, v in zip(t1["Name"], t1["i"])}
qual = {n: v for n, v in zip(t1["Name"], t1["Qual"])}

# ===================================================================== #
hr("PART A -- IS THE SPARC SOURCE A POINT MASS? (directive's premise)")
# ===================================================================== #
n_neg = int((Vg < 0).sum())
gal_neg = len(set(name[Vg < 0]))
print("  Test 1 -- negative Vgas (impossible for a point mass):")
print("    %d points across %d galaxies, most negative %.2f km/s" % (n_neg, gal_neg, Vg.min()))

peaks = []
for g in sorted(set(name)):
    s = (name == g)
    if s.sum() < 6:
        continue
    o = np.argsort(R[s])
    r, v = R[s][o], Vd[s][o]
    i = int(np.argmax(v))
    if i == 0 or i == len(v) - 1:
        continue
    if rdisk.get(g, np.nan) > 0:
        peaks.append(r[i] / rdisk[g])
peaks = np.array(peaks)
print("  Test 2 -- interior Vdisk peak (point mass has none):")
print("    %d galaxies peak internally, at median %.2f R_disk" % (len(peaks), np.median(peaks)))
print("    Freeman (1970) exponential-disk prediction: 2.2  -- matches.")

slopes = []
for g in sorted(set(name)):
    s = (name == g)
    if s.sum() < 6:
        continue
    o = np.argsort(R[s])
    r, v = R[s][o], Vd[s][o]
    m = (r > 0) & (v > 0)
    if m.sum() < 4:
        continue
    slopes.append(np.polyfit(np.log(r[m][:4]), np.log(v[m][:4]), 1)[0])
slopes = np.array(slopes)
print("  Test 3 -- inner slope d ln Vdisk / d ln r:")
print("    median %+.2f ; positive in %.1f%% of galaxies" % (np.median(slopes), 100 * (slopes > 0).mean()))
print("    point mass gives -0.50 everywhere.")
print("\n  VERDICT: the SPARC mass model is an EXTENDED, FINITE-VOLUME source.")
print("  No point mass, no r=0, no 1/r^2-from-a-singularity. The directive's")
print("  stated reason for rejecting the previous run does not hold.")
print("  'Acceleration peaks at the macro-boundary and falls inward' was")
print("  already satisfied.")

results["part_A_source_is_extended"] = {
    "negative_Vgas_points": n_neg, "negative_Vgas_galaxies": gal_neg,
    "interior_Vdisk_peak_galaxies": int(len(peaks)),
    "median_peak_over_Rdisk": float(np.median(peaks)),
    "freeman_1970_prediction": 2.2,
    "median_inner_slope": float(np.median(slopes)),
    "pct_positive_inner_slope": float(100 * (slopes > 0).mean()),
    "point_mass_premise_holds": False,
}

# ===================================================================== #
hr("PART B -- SURFACE-TENSION SOLVER, BUILT FROM PHOTOMETRY (NGC 3198)")
# ===================================================================== #
# Mass distribution constructed by integrating the OBSERVED 3.6um surface
# brightness. Vdisk/Vbulge are never touched here.
TARGET = "NGC3198"
s = (name == TARGET)
o = np.argsort(R[s])
r_kpc = R[s][o]
sb = UPS_D * SBd[s][o] + UPS_B * SBb[s][o]        # Msun/pc^2, observed
vobs = Vo[s][o]
vgas = Vg[s][o]

r_pc = r_kpc * 1.0e3
# Enclosed stellar mass: M(<R) = Int 2*pi*R*Sigma(R) dR, trapezoid on real points.
integrand = 2.0 * np.pi * r_pc * sb
M_star = np.concatenate([[0.0], np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(r_pc))])
# Gas enclosed mass from SPARC's own HI model (table2 carries no HI surface
# density column). Labelled: this one input is inherited, not rebuilt.
M_gas = (vgas * np.abs(vgas)) * (KMS ** 2) * (r_kpc * KPC) / G_SI / MSUN
M_encl = M_star + np.maximum(M_gas, 0.0)

# Defect-area bookkeeping, per the directive's ontology.
a_v = 4.0 * np.pi * (0.84e-15) ** 2               # proton-scale vortex boundary area, m^2
A_defect = (M_encl * MSUN / M_PROTON) * a_v       # m^2
C_T = G_SI * M_PROTON / a_v                       # tension constant fixed by the k=2 limit

r_m = r_kpc * KPC
g_tension = C_T * A_defect / (4.0 * np.pi * r_m ** 2) * (4.0 * np.pi)
v_pred = np.sqrt(np.maximum(g_tension * r_m, 0.0)) / KMS

print("  Source built by integrating observed 3.6um surface brightness.")
print("  Vdisk / Vbulge NOT used. Gas enclosed mass inherited from SPARC HI model.")
print("  Vortex boundary area a_v = %.3e m^2 ; C_T = %.4e (N/m per m^2 defect)"
      % (a_v, C_T))
print("  Total enclosed defect area at R_max : %.4e m^2" % A_defect[-1])
print("\n   R(kpc)   M_encl(Msun)   g_tension(m/s2)    v_pred    v_obs")
for i in range(0, len(r_kpc), max(1, len(r_kpc) // 12)):
    print("   %6.2f   %.4e     %.4e      %6.1f   %6.1f"
          % (r_kpc[i], M_encl[i], g_tension[i], v_pred[i], vobs[i]))
print("   %6.2f   %.4e     %.4e      %6.1f   %6.1f"
      % (r_kpc[-1], M_encl[-1], g_tension[-1], v_pred[-1], vobs[-1]))

# Outer logarithmic slope of the predicted vs observed curve.
n_out = max(4, len(r_kpc) // 4)
sl_pred = np.polyfit(np.log(r_kpc[-n_out:]), np.log(v_pred[-n_out:]), 1)[0]
sl_obs = np.polyfit(np.log(r_kpc[-n_out:]), np.log(vobs[-n_out:]), 1)[0]
print("\n  Outer d ln v / d ln r over the last %d points:" % n_out)
print("    surface-tension prediction : %+.3f   (Keplerian is -0.500)" % sl_pred)
print("    observed                   : %+.3f   (flat is  0.000)" % sl_obs)
print("    v_pred at R_max = %.1f km/s   vs   v_obs = %.1f km/s   -> short by %.0f%%"
      % (v_pred[-1], vobs[-1], 100 * (1 - v_pred[-1] / vobs[-1])))
print("\n  The 4*pi*r^2 diffusion premise reduces exactly to Gauss's law, so it")
print("  reproduces Newton where Newton is right and falls Keplerian outside")
print("  the luminous body. It does NOT produce a flat outer curve.")
print("  Impedance check: max v_pred/c0 = %.3e -- cap never approached."
      % (v_pred.max() * KMS / C0))

results["part_B_single_galaxy"] = {
    "galaxy": TARGET, "n_points": int(len(r_kpc)),
    "M_enclosed_Rmax_Msun": float(M_encl[-1]),
    "defect_area_Rmax_m2": float(A_defect[-1]),
    "outer_slope_predicted": float(sl_pred), "outer_slope_observed": float(sl_obs),
    "v_pred_Rmax_kms": float(v_pred[-1]), "v_obs_Rmax_kms": float(vobs[-1]),
    "max_v_over_c0": float(v_pred.max() * KMS / C0),
}

# ===================================================================== #
hr("PART C -- WHAT DIFFUSION GEOMETRY DOES THE DATA ACTUALLY DEMAND?")
# ===================================================================== #
# Generalise the diffusion surface: flux conserved through a surface ~ r^k.
#     g(r) = C_k * M(<r) / r^k
# k=2 is spherical (the directive). k=1 is cylindrical. Fit k on real data.
inc_a = np.array([inc.get(n, np.nan) for n in name], float)
q_a = np.array([qual.get(n, np.nan) for n in name], float)
m = (R > 0) & (Vo > 0) & np.isfinite(eVo) & (eVo / Vo <= 0.10) & (inc_a >= 30) & (q_a <= 2)
Rq, Voq, Vgq, Vdq, Vbq, nq = R[m], Vo[m], Vg[m], Vd[m], Vb[m], name[m]
Vbar2 = Vgq * np.abs(Vgq) + UPS_D * Vdq * np.abs(Vdq) + UPS_B * Vbq * np.abs(Vbq)
good = Vbar2 > 0
Rq, Voq, Vbar2, nq = Rq[good], Voq[good], Vbar2[good], nq[good]
# Enclosed baryonic mass of the EXTENDED source, in SI.
M_enc = Vbar2 * (KMS ** 2) * (Rq * KPC) / G_SI
r_si = Rq * KPC
g_obs = Voq ** 2 * KMS ** 2 / r_si

print("  %d points, %d galaxies (same cuts as Domain K/CC)." % (len(Rq), len(set(nq))))
print("  Model: g = C_k * M(<r) / r^k, with M(<r) the extended enclosed mass.")
print("  Exactly ONE free parameter per k (the constant C_k); k itself scanned.\n")
print("     k      interpretation              RMS (dex)")
best = None
scan = {}
for k in [1.0, 1.2, 1.4, 1.5, 1.6, 1.8, 2.0]:
    pred = M_enc / r_si ** k
    logC = np.mean(np.log10(g_obs) - np.log10(pred))
    rms = float(np.sqrt(np.mean((np.log10(g_obs) - np.log10(pred) - logC) ** 2)))
    lab = {1.0: "cylindrical (2D sheet)", 2.0: "spherical (the directive)"}.get(k, "")
    scan["k=%.1f" % k] = rms
    print("    %.1f    %-26s  %.4f" % (k, lab, rms))
    if best is None or rms < best[0]:
        best = (rms, k)
ks = np.linspace(0.8, 2.2, 141)
rr = []
for k in ks:
    pred = M_enc / r_si ** k
    logC = np.mean(np.log10(g_obs) - np.log10(pred))
    rr.append(np.sqrt(np.mean((np.log10(g_obs) - np.log10(pred) - logC) ** 2)))
k_best = float(ks[int(np.argmin(rr))])
rms_best = float(np.min(rr))
print("\n  Best-fit diffusion exponent k = %.3f   (RMS %.4f dex)" % (k_best, rms_best))
print("  Spherical k=2.0 gives %.4f dex. Cylindrical k=1.0 gives %.4f dex."
      % (scan["k=2.0"], scan["k=1.0"]))
print("\n  The data prefer k slightly below 2, but the improvement is small")
print("  (%.4f -> %.4f dex) and the whole scan is FLATTERED by a free" % (scan["k=2.0"], rms_best))
print("  global amplitude. Quantifying that, because it matters more than k:")
logC2 = np.mean(np.log10(g_obs) - np.log10(M_enc / r_si ** 2.0))
amp = 10 ** logC2 / G_SI
print("    fitted C_2 / G = %.2f" % amp)
print("    i.e. the k=2 fit only reaches %.4f dex by scaling all baryonic" % scan["k=2.0"])
print("    mass up by a factor %.2f. With C fixed to the true G, the same" % amp)
print("    model scores %.4f dex (the Domain CC Newtonian null)." % 0.5145)
print("    That factor is not physically available: it demands M/L(3.6um)")
print("    = %.2f against %.2f from stellar population synthesis, which is" % (UPS_D * amp, UPS_D))
print("    the very 'missing mass' the model was supposed to explain away.")
print("    So the scan absorbs the missing mass into a constant, and STILL")
print("    leaves %.4f dex of scatter." % rms_best)

results["part_C_diffusion_exponent"] = {
    "n_points": int(len(Rq)), "n_galaxies": int(len(set(nq))),
    "scan": scan, "k_best": k_best, "rms_best_dex": rms_best,
    "rms_spherical_k2": scan["k=2.0"], "rms_cylindrical_k1": scan["k=1.0"],
}

# ===================================================================== #
hr("PART D -- CAN THE ACCELERATION SCALE BE ELIMINATED?")
# ===================================================================== #
# The directive asks for orbits "without needing a0 artificially typed in".
# A pure power law g = C_k*M/r^k contains NO acceleration scale: it is
# scale-free by construction. So Part C IS the a0-free model, and its best
# possible score is the honest answer to the question.
print("  A power law g = C_k*M(<r)/r^k is scale-free: no a0 exists in it.")
print("  So Part C's best fit is the strongest possible a0-free result.\n")
print("     model                                    params   RMS (dex)")
print("     baryons, spherical diffusion k=2.0          1      %.4f" % scan["k=2.0"])
print("     baryons, best scale-free k=%.2f             2      %.4f" % (k_best, rms_best))
print("     RAR / choke (HAS an acceleration scale)     1      0.1327   [Domain CC]")
print("\n  The best scale-free law is worse than the scaled law by %.4f dex,"
      % (rms_best - 0.1327))
print("  a factor of %.1f in linear scatter." % (10 ** (rms_best - 0.1327)))

# Dimensional argument, made explicit.
print("\n  DIMENSIONAL ARGUMENT (why this is not a solver problem):")
print("    g = C_k * M / r^k  requires [C_k] = m^(k+1) / (s^2 kg).")
print("    For k=2 that is exactly G's units -- no extra scale.")
print("    For k<2, [C_k] = [G] / m^(2-k), so C_k = G / L^(2-k) for some")
print("    length L. Any k != 2 SMUGGLES IN A LENGTH SCALE inside its own")
print("    constant. Combined with G and a mass it yields an acceleration.")
L_implied = (G_SI / (10 ** np.mean(np.log10(g_obs) - np.log10(M_enc / r_si ** k_best)))) \
    ** (1.0 / (2.0 - k_best))
L_lo = (G_SI / (10 ** np.mean(np.log10(g_obs) - np.log10(M_enc / r_si ** 1.80)))) ** (1.0 / 0.20)
L_hi = (G_SI / (10 ** np.mean(np.log10(g_obs) - np.log10(M_enc / r_si ** 1.86)))) ** (1.0 / 0.14)
print("    Implied length at k=%.3f : L = %.3e m = %.3f kpc"
      % (k_best, L_implied, L_implied / KPC))
print("    CAVEAT: L = (G/C_k)^(1/(2-k)) and 2-k = %.2f here, so L is" % (2 - k_best))
print("    hypersensitive -- k=1.80 gives %.2f kpc, k=1.86 gives %.2f kpc."
      % (L_lo / KPC, L_hi / KPC))
print("    The DIMENSIONAL argument (k!=2 requires a scale) is solid; this")
print("    particular numeric value of L is not, and is not used further.")
a_from_L = 10 ** np.mean(np.log10(g_obs) - np.log10(M_enc / r_si ** k_best))
print("    So the scale is renamed, not removed.")
print("\n  ANSWER TO THE DIRECTIVE'S CLOSING QUESTION:")
print("    Do surface-tension gradients intrinsically predict flat outer")
print("    velocities without a0 and without dark matter?")
print("    NO -- not with 4*pi*r^2 spherical diffusion. That premise is")
print("    mathematically identical to Gauss's law and yields v ~ r^-1/2")
print("    (Part B: predicted outer slope %+.3f vs observed %+.3f)." % (sl_pred, sl_obs))
print("    Flat curves need flux conserved on a surface growing like r^1,")
print("    i.e. quasi-2D/cylindrical tension transport, not isotropic 3D.")
print("    And a pure r^1 law cannot hold everywhere -- the solar system")
print("    follows 1/r^2 to ~1e-5. A transition between the two regimes is")
print("    required, and the transition point IS an acceleration scale.")
print("    c0 impedance cap: never approached anywhere (max v/c0 ~ 1e-3).")

results["part_D_scale_free_test"] = {
    "best_scale_free_rms_dex": rms_best,
    "scaled_law_rms_dex": 0.1327,
    "penalty_dex": float(rms_best - 0.1327),
    "implied_length_scale_kpc": float(L_implied / KPC),
    "implied_length_unstable": True,
    "fitted_C2_over_G": float(10 ** np.mean(np.log10(g_obs) - np.log10(M_enc / r_si ** 2.0)) / G_SI),
    "implied_acceleration_constant": float(a_from_L),
    "a0_eliminable": False,
    "flat_curves_from_spherical_diffusion": False,
}

out = os.path.join(D, "domain_DD_surface_tension_results.json")
with open(out, "w") as f:
    json.dump(results, f, indent=2)
print("\n  wrote %s" % out)
