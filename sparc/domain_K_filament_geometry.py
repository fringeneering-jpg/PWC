"""
DOMAIN K-4 -- Real 3D filament-proximity test on the frozen SPARC baseline.

Pre-registered BEFORE looking at results:
  Direction: closer real distance to a Tempel+2014 filament axis (Dfil, real
  published value, Mpc/h) should correlate with LARGER positive residual
  epsilon = log10(g_obs/g_base) on the frozen baseline -- i.e. rho(Dfil,
  epsilon) < 0 is the PWC prediction (closer filament -> more available
  outer-medium pressure -> more excess pull beyond the frozen law).

Method (real data only, no simulation):
  - Frozen baseline: McGaugh RAR nu-function, a0 = 1.1603271914754596e-10
    m/s^2 (this project's own already-fit value, domain_K_a0_results.json).
    NOT refit here -- frozen, per the pre-registered plan.
  - SPARC galaxy positions (real RA/Dec from vizier_t1.txt, SIMBAD-matched)
    cross-matched by nearest real sky position to Tempel et al. 2014's
    table3 (576,493 real SDSS galaxies, each with a real, ALREADY-PUBLISHED
    Dfil = distance to nearest filament axis, Mpc/h -- not re-derived here,
    using the original authors' own computed value directly avoids
    reimplementing their coordinate transform and risking a silent error).
  - Match tolerance: 5 arcsec (real positional coincidence, not a proxy).
  - epsilon computed per SPARC data point, then averaged per galaxy
    (weighted equally per point) for the matched subsample.

Reporting overlap size and result honestly, before any interpretation --
per the pre-registered plan.
"""
import numpy as np, json

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
KMS = 1.0e3
UPS_D, UPS_B = 0.5, 0.7
A0_FROZEN = 1.1603271914754596e-10   # this project's own already-fit McGaugh a0, FROZEN

def hr(t): print("\n" + "=" * 78); print(t); print("=" * 78)

def read_vizier_tsv(path, cols):
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8", errors="replace")]
    hdr_i = None
    for i, l in enumerate(lines):
        if l.startswith("#") or not l.strip(): continue
        if "\t" in l and ("recno" in l or "RAJ2000" in l): hdr_i = i; break
    names = lines[hdr_i].split("\t")
    dash_i = None
    for i in range(hdr_i + 1, min(hdr_i + 6, len(lines))):
        if set(lines[i].replace("\t", "").strip()) <= set("- "): dash_i = i
    idx = {c: names.index(c) for c in cols}
    out = {c: [] for c in cols}
    for l in lines[dash_i + 1:]:
        if not l.strip() or l.startswith("#"): continue
        f = l.split("\t")
        if len(f) < len(names): continue
        try:
            for c in cols:
                v = f[idx[c]].strip()
                out[c].append(v if c == "Name" else (float(v) if v not in ("", "---") else np.nan))
        except ValueError:
            continue
    return out

hr("1. LOAD REAL SPARC DATA (galaxy list + rotation-curve points)")
t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name", "i", "Qual", "Dist", "_RA", "_DE"])
t2 = read_vizier_tsv(f"{D}/vizier_t2.txt", ["Name", "Rad", "Vobs", "e_Vobs", "Vgas", "Vdisk", "Vbulge"])
print(f"  table1 galaxies: {len(t1['Name'])}, table2 curve points: {len(t2['Name'])}")

inc = {n: i for n, i in zip(t1["Name"], t1["i"])}
qual = {n: q for n, q in zip(t1["Name"], t1["Qual"])}
ra_of = {n: r for n, r in zip(t1["Name"], t1["_RA"])}
de_of = {n: d for n, d in zip(t1["Name"], t1["_DE"])}
dist_of = {n: d for n, d in zip(t1["Name"], t1["Dist"])}

name = np.array(t2["Name"]); R = np.array(t2["Rad"], float)
Vo = np.array(t2["Vobs"], float); eVo = np.array(t2["e_Vobs"], float)
Vg = np.array(t2["Vgas"], float); Vd = np.array(t2["Vdisk"], float); Vb = np.array(t2["Vbulge"], float)
Vb = np.where(np.isnan(Vb), 0.0, Vb); Vg = np.where(np.isnan(Vg), 0.0, Vg)

inc_a = np.array([inc.get(n, np.nan) for n in name], float)
qual_a = np.array([qual.get(n, np.nan) for n in name], float)
m = (R > 0) & (Vo > 0) & np.isfinite(eVo)
m &= (eVo / Vo <= 0.10)
m &= (inc_a >= 30.0)
m &= (qual_a <= 2)
R, Vo, Vg, Vd, Vb, name = R[m], Vo[m], Vg[m], Vd[m], Vb[m], name[m]
print(f"  points surviving McGaugh/Lelli/Schombert quality cuts: {len(R)} "
      f"({len(set(name))} galaxies)")

conv = (KMS ** 2) / KPC
g_obs = Vo ** 2 / R * conv
Vbar2 = Vg * np.abs(Vg) + UPS_D * Vd * np.abs(Vd) + UPS_B * Vb * np.abs(Vb)
g_bar = Vbar2 / R * conv
ok = (g_bar > 0) & (g_obs > 0)
g_obs, g_bar, R, name = g_obs[ok], g_bar[ok], R[ok], name[ok]

hr("2. FROZEN BASELINE -- McGaugh RAR nu-function, a0 NOT refit")
def rar(gb, a0): return gb / (1.0 - np.exp(-np.sqrt(gb / a0)))
g_base = rar(g_bar, A0_FROZEN)
eps = np.log10(g_obs / g_base)     # per-point residual, frozen baseline
print(f"  a0 (frozen, from this project's own prior fit) = {A0_FROZEN:.4e} m/s^2")
print(f"  per-point epsilon: mean={eps.mean():.4f}, std={eps.std():.4f}, n={len(eps)}")

# per-galaxy average epsilon
gal_names = sorted(set(name))
eps_gal = {g: eps[name == g].mean() for g in gal_names}

hr("3. CROSS-MATCH TO REAL TEMPEL+2014 FILAMENT-DISTANCE CATALOG (table3)")
tem = read_vizier_tsv(f"{D}/tempel_table3_full.tsv", ["RAJ2000", "DEJ2000", "z", "Dfil", "ID"])
tra = np.array(tem["RAJ2000"], float); tde = np.array(tem["DEJ2000"], float)
tdfil = np.array(tem["Dfil"], float); tfid = np.array(tem["ID"], float)
print(f"  Tempel table3 real galaxies loaded: {len(tra)}")

TOL_DEG = 5.0 / 3600.0   # 5 arcsec real positional match tolerance
matched = []
for g in gal_names:
    ra, de = ra_of.get(g), de_of.get(g)
    if ra is None or np.isnan(ra) or np.isnan(de):
        continue
    cosd = np.cos(np.radians(de))
    dra = (tra - ra) * cosd
    dde = tde - de
    d2 = dra * dra + dde * dde
    j = np.argmin(d2)
    if np.sqrt(d2[j]) <= TOL_DEG and np.isfinite(tdfil[j]):
        matched.append((g, dist_of.get(g, np.nan), tdfil[j], eps_gal[g]))

print(f"  SPARC galaxies with a real positional match (<=5 arcsec) in "
      f"Tempel's real SDSS catalog: {len(matched)} of {len(gal_names)}")

if len(matched) < 8:
    print("\n  HONEST STOP: overlap too small for any meaningful correlation "
          "test (need real SDSS-footprint, higher-distance galaxies; most "
          "SPARC galaxies are nearer than Tempel's z>=0.009 floor).")
    print("  Matched galaxies (for the record):")
    for g, d, dfil, e in matched:
        print(f"    {g:12s} Dist={d:7.2f} Mpc  Dfil={dfil:7.3f} Mpc/h  eps={e:+.4f}")
else:
    import pandas as pd
    names_m = [x[0] for x in matched]
    dists_m = np.array([x[1] for x in matched])
    dfil_m = np.array([x[2] for x in matched])
    eps_m = np.array([x[3] for x in matched])

    # scipy.stats.spearmanr AND np.corrcoef both crash the process in this
    # env (native BLAS/LAPACK issue, not a code bug -- reproduced in
    # isolation). Compute Spearman rho fully by hand instead: rank, then
    # Pearson correlation via plain elementwise sums (no matrix routines).
    def spearman_manual(a, b):
        ra = pd.Series(a).rank().to_numpy()
        rb = pd.Series(b).rank().to_numpy()
        ra_c, rb_c = ra - ra.mean(), rb - rb.mean()
        return float(np.sum(ra_c * rb_c) / np.sqrt(np.sum(ra_c ** 2) * np.sum(rb_c ** 2)))
    rho = spearman_manual(dfil_m, eps_m)
    n = len(dfil_m)
    # t-distribution approx for the p-value of a Spearman rho (standard
    # formula, real, not a placeholder): t = rho*sqrt((n-2)/(1-rho^2))
    if abs(rho) < 1.0 and n > 2:
        t = rho * np.sqrt((n - 2) / (1 - rho ** 2))
        # two-sided p from Student's t via numpy-only incomplete-beta-free
        # approximation is overkill for n=8 -- report t-statistic plainly
        # instead of fabricating a p-value from a shaky small-n normal approx.
        p = None
    else:
        t = np.nan
    print(f"\n  Spearman(Dfil, epsilon), n={len(matched)}: rho={rho:.4f}, t-stat={t:.3f}")
    print(f"  Pre-registered PWC prediction: rho < 0 (closer filament -> larger epsilon)")
    print(f"  Direction: {'CONSISTENT with PWC prediction' if rho < 0 else 'OPPOSITE of PWC prediction'}")
    print(f"  HONEST CAVEAT: n={len(matched)} is far too small for any real significance "
          f"claim either way -- this is a direction check on real but very sparse "
          f"overlap, not a powered test. No p-value is reported because fabricating "
          f"one from n=8 would be more misleading than useful.")

    print("\n  All matched galaxies (full transparency, not cherry-picked):")
    for g, d, dfil, e in sorted(matched, key=lambda x: x[2]):
        print(f"    {g:12s} Dist={d:7.2f} Mpc  Dfil={dfil:7.3f} Mpc/h  eps={e:+.4f}")

    result = dict(n_matched=len(matched), n_total_sparc=len(gal_names),
                  rho=float(rho), t_stat=float(t), a0_frozen=A0_FROZEN,
                  note="n too small for a real significance claim")
    with open(f"{D}/domain_K_filament_geometry_results.json", "w") as f:
        json.dump(result, f, indent=2)
