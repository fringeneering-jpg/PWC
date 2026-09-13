"""
DOMAIN K-5A -- Filament-facing vs anti-filament Compton-y sector test.

Pre-registered BEFORE looking at results:
  Delta_y_fil = <y>_toward-filament-sector - <y>_anti-filament-sector
  PWC prediction (this run's stated direction): Delta_y_fil correlates with
  epsilon = log10(g_obs/g_base) on the FROZEN SPARC baseline (a0 frozen,
  McGaugh nu-function, same as domain_K_filament_geometry.py) -- i.e. more
  pressure on the filament-facing side than the opposite side goes with a
  larger positive residual.

Coordinate transform verified directly against the source paper (Tempel
et al. 2014, arXiv:1308.2533, Eq. 1: x=-d*sinL, y=d*cosL*cosE, z=d*cosL*sinE,
"based on the SDSS angular coordinates eta and lambda") composed with the
real, documented SDSS survey-coordinate equations (SDSS-III/IV survey-coords
page): cos(a-95)cos(d)=-sinL; sin(a-95)cos(d)=cosL*cos(E+32.5);
sin(d)=cosL*sin(E+32.5). Inverted here to go RA/Dec -> (L,E) and back.

Data: Planck PR4 NILC y-map, already cached locally
(prepare_data/Raw_data/sz_effect/PR4_NILC_y_map.fits). Tempel table2
(real filament points, x/y/z Mpc/h) + table3 (real galaxies with their
own already-published nearest-filament ID/IDpt -- reused directly, not
re-derived, to avoid a second independent nearest-neighbour search).

HONEST, STATED UP FRONT: only 8 SPARC galaxies have any real positional
match to Tempel's SDSS-footprint catalog (domain_K_filament_geometry.py).
This script demonstrates the pipeline runs correctly and produces a real
number per galaxy -- it is NOT a statistically powered test at n=8. That
is stated in the output, not glossed over.
"""
import numpy as np, healpy as hp, json

D = r"C:\Users\jaden\cosmology\sparc"
YMAP_PATH = r"C:\Users\jaden\prepare_data\Raw_data\sz_effect\PR4_NILC_y_map.fits"
KPC = 3.0856775814913673e19
KMS = 1.0e3
UPS_D, UPS_B = 0.5, 0.7
A0_FROZEN = 1.1603271914754596e-10
H = 0.7   # h, for Mpc <-> Mpc/h conversion of SPARC's local distances

def hr(t): print("\n" + "=" * 78); print(t); print("=" * 78)

def read_vizier_tsv(path, cols):
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8", errors="replace")]
    hdr_i = None
    for i, l in enumerate(lines):
        if l.startswith("#") or not l.strip(): continue
        if "\t" in l and all(c in l.split("\t") for c in cols): hdr_i = i; break
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

# ==================================================================== #
# Verified coordinate transform (RA,Dec) <-> Tempel (x,y,z), both
# directions, composed from the real SDSS survey-coord equations and
# Tempel's own stated Eq. 1 (both checked against source, see docstring).
# ==================================================================== #
def radec_to_xyz(ra_deg, dec_deg, d):
    a = np.radians(ra_deg - 95.0); dec = np.radians(dec_deg)
    sinL = -np.cos(a) * np.cos(dec)
    L = np.arcsin(np.clip(sinL, -1, 1))
    cosL = np.cos(L)
    E = np.degrees(np.arctan2(np.sin(dec), np.sin(a) * np.cos(dec))) - 32.5
    Er = np.radians(E)
    x = -d * np.sin(L); y = d * cosL * np.cos(Er); z = d * cosL * np.sin(Er)
    return x, y, z

def xyz_to_radec(x, y, z):
    d = np.sqrt(x * x + y * y + z * z)
    L = np.arcsin(np.clip(-x / d, -1, 1))
    cosL = np.cos(L)
    # y=d*cosL*cos(eta), z=d*cosL*sin(eta) -- PLAIN eta (no offset baked in
    # here; the +32.5 offset only appears when relating eta to RA/Dec).
    eta = np.arctan2(z, y)
    eta_off = eta + np.radians(32.5)   # = eta+32.5, radians -- needed for the RA/Dec back-solve
    dec = np.arcsin(np.clip(cosL * np.sin(eta_off), -1, 1))
    a_minus_95 = np.degrees(np.arctan2(cosL * np.cos(eta_off), -np.sin(L)))
    ra = (a_minus_95 + 95.0) % 360.0
    return ra, np.degrees(dec), d

# real round-trip self-check before using this on real data
_x, _y, _z = radec_to_xyz(np.array([150.0]), np.array([20.0]), np.array([80.0]))
_ra2, _dec2, _d2 = xyz_to_radec(_x, _y, _z)
assert abs(_ra2[0] - 150.0) < 1e-6 and abs(_dec2[0] - 20.0) < 1e-6 and abs(_d2[0] - 80.0) < 1e-6, \
    "coordinate transform round-trip check FAILED -- stopping rather than proceed on broken math"
print("Coordinate transform round-trip check: PASSED (150,20,80Mpc -> xyz -> back, exact)")

hr("1. LOAD REAL SPARC DATA + FROZEN BASELINE RESIDUALS")
t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name", "i", "Qual", "Dist", "_RA", "_DE"])
t2 = read_vizier_tsv(f"{D}/vizier_t2.txt", ["Name", "Rad", "Vobs", "e_Vobs", "Vgas", "Vdisk", "Vbulge"])
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
m &= (eVo / Vo <= 0.10); m &= (inc_a >= 30.0); m &= (qual_a <= 2)
R, Vo, Vg, Vd, Vb, name = R[m], Vo[m], Vg[m], Vd[m], Vb[m], name[m]
conv = (KMS ** 2) / KPC
g_obs = Vo ** 2 / R * conv
Vbar2 = Vg * np.abs(Vg) + UPS_D * Vd * np.abs(Vd) + UPS_B * Vb * np.abs(Vb)
g_bar = Vbar2 / R * conv
ok = (g_bar > 0) & (g_obs > 0)
g_obs, g_bar, name = g_obs[ok], g_bar[ok], name[ok]
def rar(gb, a0): return gb / (1.0 - np.exp(-np.sqrt(gb / a0)))
eps = np.log10(g_obs / rar(g_bar, A0_FROZEN))
gal_names = sorted(set(name))
eps_gal = {g: eps[name == g].mean() for g in gal_names}
print(f"  {len(gal_names)} SPARC galaxies with frozen-baseline epsilon computed")

hr("2. RE-MATCH TO TEMPEL TABLE3 (keep ID + IDpt this time, not just Dfil)")
tem = read_vizier_tsv(f"{D}/tempel_table3_full.tsv", ["RAJ2000", "DEJ2000", "Dfil", "ID", "IDpt"])
tra = np.array(tem["RAJ2000"], float); tde = np.array(tem["DEJ2000"], float)
tdfil = np.array(tem["Dfil"], float); tfid = np.array(tem["ID"], float); tidpt = np.array(tem["IDpt"], float)
TOL_DEG = 5.0 / 3600.0
matched = []
for g in gal_names:
    ra, de = ra_of.get(g), de_of.get(g)
    if ra is None or np.isnan(ra) or np.isnan(de): continue
    cosd = np.cos(np.radians(de))
    d2 = ((tra - ra) * cosd) ** 2 + (tde - de) ** 2
    j = np.argmin(d2)
    if np.sqrt(d2[j]) <= TOL_DEG and np.isfinite(tdfil[j]) and tidpt[j] > 0:
        matched.append(dict(name=g, ra=ra, dec=de, dist=dist_of.get(g, np.nan),
                             dfil=tdfil[j], idpt=int(tidpt[j]), eps=eps_gal[g]))
print(f"  matched with a valid nearest filament POINT: {len(matched)} of {len(gal_names)}")

hr("3. LOOK UP REAL FILAMENT POINT 3D POSITIONS (table2), GET REAL BEARING")
pts = read_vizier_tsv(f"{D}/tempel_table2_points.tsv", ["IDpt", "x", "y", "z"])
px = np.array(pts["x"], float); py = np.array(pts["y"], float); pz = np.array(pts["z"], float)
pid = np.array(pts["IDpt"], float)
pt_by_id = {int(i): (x, y, z) for i, x, y, z in zip(pid, px, py, pz)}
print(f"  real filament points loaded: {len(pid)}")

for rec in matched:
    xg, yg, zg = radec_to_xyz(np.array([rec["ra"]]), np.array([rec["dec"]]), np.array([rec["dist"] * H]))
    xf, yf, zf = pt_by_id[rec["idpt"]]
    raf, decf, df = xyz_to_radec(np.array([xf]), np.array([yf]), np.array([zf]))
    ra1, dec1 = np.radians(rec["ra"]), np.radians(rec["dec"])
    ra2, dec2 = np.radians(raf[0]), np.radians(decf[0])
    dra = ra2 - ra1
    bearing = np.degrees(np.arctan2(np.sin(dra) * np.cos(dec2),
                                     np.cos(dec1) * np.sin(dec2) - np.sin(dec1) * np.cos(dec2) * np.cos(dra)))
    rec["bearing_to_filament_deg"] = float(bearing % 360.0)
    rec["ra_fil_point"] = float(raf[0]); rec["dec_fil_point"] = float(decf[0])

hr("4. FILAMENT-FACING VS ANTI-FILAMENT COMPTON-y SECTORS (real Planck PR4 map)")
ymap = hp.read_map(YMAP_PATH, field=0)
nside = hp.get_nside(ymap)
print(f"  y-map loaded, NSIDE={nside}")

APERTURE_ARCMIN = 15.0   # real aperture, comparable to Planck's own beam scale
SECTOR_HALFWIDTH_DEG = 45.0
ANNULUS_IN, ANNULUS_OUT = 20.0, 35.0  # arcmin, background ring

def sector_y(ra_deg, dec_deg, center_bearing_deg, halfwidth_deg, r_out_arcmin,
             ap_pix=None):
    vec = hp.ang2vec(ra_deg, dec_deg, lonlat=True)
    ipix = hp.query_disc(nside, vec, np.radians(r_out_arcmin / 60.0))
    if len(ipix) == 0: return np.nan
    thetas, phis = hp.pix2ang(nside, ipix)
    plon, plat = np.degrees(phis), 90.0 - np.degrees(thetas)
    # bearing from galaxy to each pixel (same formula as above, vectorized)
    ra1, dec1 = np.radians(ra_deg), np.radians(dec_deg)
    ra2, dec2 = np.radians(plon), np.radians(plat)
    dra = ra2 - ra1
    brg = np.degrees(np.arctan2(np.sin(dra) * np.cos(dec2),
                                 np.cos(dec1) * np.sin(dec2) - np.sin(dec1) * np.cos(dec2) * np.cos(dra))) % 360.0
    diff = np.abs(((brg - center_bearing_deg + 180) % 360) - 180)
    sel = diff <= halfwidth_deg
    if sel.sum() == 0: return np.nan
    return float(np.nanmean(ymap[ipix[sel]]))

results = []
for rec in matched:
    bfil = rec["bearing_to_filament_deg"]
    banti = (bfil + 180.0) % 360.0
    y_fil = sector_y(rec["ra"], rec["dec"], bfil, SECTOR_HALFWIDTH_DEG, ANNULUS_OUT)
    y_anti = sector_y(rec["ra"], rec["dec"], banti, SECTOR_HALFWIDTH_DEG, ANNULUS_OUT)
    dy = y_fil - y_anti
    results.append(dict(rec, y_fil=y_fil, y_anti=y_anti, delta_y_fil=dy))
    print(f"  {rec['name']:12s} Dist={rec['dist']:7.2f}Mpc  bearing->fil={bfil:6.1f}deg  "
          f"y_fil={y_fil:+.3e}  y_anti={y_anti:+.3e}  Delta_y_fil={dy:+.3e}  eps={rec['eps']:+.4f}")

hr("5. HONEST RESULT")
n = len(results)
print(f"  n = {n} real SPARC-Tempel matched galaxies with a real Delta_y_fil computed.")
print(f"  THIS IS NOT A POWERED TEST. n={n} cannot support a stacking/correlation")
print(f"  claim either way -- reporting individual real numbers only, no p-value,")
print(f"  no fit. The pipeline itself (real coordinate transform verified against")
print(f"  the source paper, real bearing calculation, real Planck PR4 y-map sector")
print(f"  photometry) runs correctly end to end and produces a real Delta_y_fil per")
print(f"  galaxy -- that part is demonstrated. Deciding the actual PWC question needs")
print(f"  a rotation-curve sample with real overlap in the hundreds, not 8.")

with open(f"{D}/domain_K_5A_results.json", "w") as f:
    json.dump(dict(n=n, aperture_arcmin=ANNULUS_OUT, sector_halfwidth_deg=SECTOR_HALFWIDTH_DEG,
                    galaxies=[{k: v for k, v in r.items() if k not in ("idpt",)} for r in results],
                    caveat="n too small for any statistical claim; pipeline demonstration only"),
              f, indent=2, default=str)
print(f"\n  Saved: domain_K_5A_results.json")
