"""Void thermal edge test (prediction frozen in PREDICTION_thermal_edge.md, commit 5def3f2).
VAST VoidFinder SDSS DR7 (Planck2018) voids; true shapes from Monte Carlo over the union of holes;
Planck PR2 MILCA Compton-y (D:/planck_milca_y_2048.fits)."""
import numpy as np, pandas as pd, healpy as hp, json, sys
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
rng = np.random.default_rng(42)
mx = pd.read_csv("VoidFinder-nsa_v1_0_1_Planck2018_comoving_maximal.txt", sep=r"\s+", comment=None, skiprows=1,
                 names="x y z radius void edge r ra dec Reff".split())
ho = pd.read_csv("VoidFinder-nsa_v1_0_1_Planck2018_comoving_holes.txt", sep=r"\s+", skiprows=1, names="x y z radius void".split())
# check cartesian convention against listed ra/dec
r0 = mx.iloc[0]; ra = np.degrees(np.arctan2(r0.y, r0.x)) % 360; dec = np.degrees(np.arcsin(r0.z / np.linalg.norm([r0.x, r0.y, r0.z])))
print(f"convention check: computed ra/dec {ra:.3f},{dec:.3f} vs listed {r0.ra:.3f},{r0.dec:.3f}")
h = fits.open("D:/planck_milca_y_2048.fits"); hdr = h[1].header
print("map columns:", h[1].columns.names, "ORDERING:", hdr.get("ORDERING"), "COORDSYS:", hdr.get("COORDSYS"))
y = np.asarray(h[1].data.field(0), float).ravel(); nest = hdr.get("ORDERING", "RING").upper().startswith("NEST")
nside = hp.npix2nside(y.size)
pix_b = hp.pix2ang(nside, np.arange(y.size), nest=nest, lonlat=True)[1]
usable = np.isfinite(y) & (np.abs(pix_b) >= 20) & (y > -1e30)

def ymean(xyz):
    d = np.linalg.norm(xyz); sc = SkyCoord(ra=np.degrees(np.arctan2(xyz[1], xyz[0])) % 360 * u.deg, dec=np.degrees(np.arcsin(xyz[2] / d)) * u.deg).galactic
    rad = max(np.radians(0.5), 5.0 / d)
    vec = hp.ang2vec(sc.l.deg, sc.b.deg, lonlat=True); pix = hp.query_disc(nside, vec, rad, nest=nest)
    ok = usable[pix]
    return np.nan if ok.mean() < 0.8 else y[pix[ok]].mean()

rows = []
for v, m in mx[mx.edge == 0].groupby("void"):
    hs = ho[ho.void == v][["x", "y", "z", "radius"]].values
    lo, hi = (hs[:, :3] - hs[:, 3:]).min(0), (hs[:, :3] + hs[:, 3:]).max(0)
    P = rng.uniform(lo, hi, size=(20000, 3))
    inside = np.zeros(len(P), bool)
    for c in hs: inside |= ((P - c[:3]) ** 2).sum(1) <= c[3] ** 2
    P = P[inside]
    if len(P) < 500: continue
    cen = P.mean(0); w, V = np.linalg.eigh(np.cov((P - cen).T))       # ascending
    ratio = np.sqrt(w[2] / w[0])
    ends = {}
    for name, k in [("major", 2), ("inter", 1), ("minor", 0)]:
        a = V[:, k]; proj = (P - cen) @ a
        ends[name] = [ymean(cen + a * (proj.max() + 5)), ymean(cen - a * (-proj.min() + 5))]
    rows.append(dict(void=int(v), Reff=float(m.Reff.iloc[0]), ratio=ratio, dist=float(np.linalg.norm(cen)),
                     y_major=np.nanmean(ends["major"]), y_inter=np.nanmean(ends["inter"]), y_minor=np.nanmean(ends["minor"])))
d = pd.DataFrame(rows).dropna(); a = d[d.ratio >= 1.3].copy()
a["D"] = a.y_major - a.y_minor; a["Dc"] = a.y_inter - a.y_minor
from scipy.stats import binomtest
def report(lbl, x):
    n = len(x); k = int((x > 0).sum()); p = binomtest(k, n, 0.5, alternative="greater").pvalue
    bs = [rng.choice(x.values, n).mean() for _ in range(5000)]
    print(f"{lbl:34s} n={n}  median {x.median():+.3e}  mean {x.mean():+.3e}  95% [{np.percentile(bs,2.5):+.2e},{np.percentile(bs,97.5):+.2e}]  positive {k}/{n} ({100*k/n:.0f}%)  sign-test p={p:.3g}")
    return x.median() > 0 and p < 0.05
print(f"\nvoids measured: {len(d)} (edge==0, discs usable); asymmetric (ratio>=1.3): {len(a)}; median ratio {d.ratio.median():.2f}")
passed = report("MAJOR ends - MINOR ends (test)", a.D)
report("INTERMEDIATE - MINOR (control)", a.Dc)
print("\nRESULT:", "PASS" if passed else "FAIL")
a.to_csv("thermal_edge_results.csv", index=False)
