"""RBH-1 metallicity dilution test — run blind against PREDICTION_metallicity.md (commit bc95fad).
Geometry and continuum subtraction copied from wake_profile.py. No PWC quantity used.
Usage: python metallicity_test.py <cube_s3d.fits>
"""
import json, os, sys, warnings
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.optimize import curve_fit
from numpy.lib.stride_tricks import sliding_window_view
warnings.filterwarnings("ignore")

CUBE = sys.argv[1]
C = 299792.458; Z = 0.9628
L = dict(Ha=0.656280, N2a=0.654805, N2b=0.658345, S2a=0.671644, S2b=0.673081)
P1 = SkyCoord(40.44051 * u.deg, -8.350361111111113 * u.deg); P2 = SkyCoord(40.44026166666667 * u.deg, -8.350525000000005 * u.deg)

f = fits.open(CUBE); h = f["SCI"].header
d = f["SCI"].data.astype(float); d[(f["DQ"].data & 1) != 0] = np.nan
wl = h["CRVAL3"] + (np.arange(h["NAXIS3"]) + 1 - h["CRPIX3"]) * h["CDELT3"]
W = 41; pad = np.pad(d, ((W // 2, W // 2), (0, 0), (0, 0)), mode="edge")
r = d - np.nanmedian(sliding_window_view(pad, W, axis=0), axis=-1)
mad = np.nanmedian(np.abs(r), axis=0, keepdims=True) * 1.4826; r[np.abs(r) > 6 * mad] = np.nan

# geometry (identical to wake_profile.py)
def win(l0, dv=250): return np.abs(wl / (l0 * (1 + Z)) - 1) * C < dv
Ha = np.nansum(r[win(L["Ha"])], 0)
wcs = WCS(h).celestial; ny, nx = Ha.shape
yy, xx = np.mgrid[0:ny, 0:nx]; sky = wcs.pixel_to_world(xx, yy)
mid = SkyCoord((P1.ra + P2.ra) / 2, (P1.dec + P2.dec) / 2)
dE = ((sky.ra - mid.ra) * np.cos(mid.dec.radian)).to(u.arcsec).value; dN = (sky.dec - mid.dec).to(u.arcsec).value
cE = ((P1.ra - P2.ra) * np.cos(mid.dec.radian)).to(u.arcsec).value; cN = (P1.dec - P2.dec).to(u.arcsec).value
pa_axis = np.degrees(np.arctan2(cE, cN)) + 90
ua = np.array([np.sin(np.radians(pa_axis)), np.cos(np.radians(pa_axis))])
proj = dE * ua[0] + dN * ua[1]; perp = dE * np.cos(np.radians(pa_axis)) - dN * np.sin(np.radians(pa_axis))
near = np.abs(perp) < 0.5
sgn = 1 if np.nansum(Ha[near & (proj > 0)]) >= np.nansum(Ha[near & (proj < 0)]) else -1
x = sgn * proj + 0.5; y = sgn * perp

REG = dict(apex=(-0.25, 0.25), tail=(0.5, 2.5))
lam0 = {k: v * (1 + Z) for k, v in L.items()}
lo, hi = 0.6500 * (1 + Z), 0.6780 * (1 + Z)
fw = (wl > lo) & (wl < hi)
linefree = fw.copy()
for k in L: linefree &= np.abs(wl / lam0[k] - 1) * C > 900

def model(xw, c0, c1, dv, s, aHa, aN2, aS2a, aS2b):
    out = c0 + c1 * (xw - xw.mean())
    for k, a in (("Ha", aHa), ("N2b", aN2), ("N2a", aN2 / 2.94), ("S2a", aS2a), ("S2b", aS2b)):
        mu = lam0[k] * (1 + dv / C); out = out + a * np.exp(-0.5 * ((xw - mu) / (mu * s / C)) ** 2)
    return out

def N2S2Ha(n2, s2, ha):
    yv = np.log10(n2 / s2) + 0.264 * np.log10(n2 / ha)
    return 8.77 + yv + 0.45 * (yv + 0.3) ** 5

rng = np.random.default_rng(7); res = {}
for name, (a, b) in REG.items():
    sel = (x >= a) & (x < b) & (np.abs(y) < 0.5) & np.isfinite(Ha)
    spec = np.nansum(r[:, sel], 1)
    sig = np.nanstd(spec[linefree])  # empirical, includes spatial correlation of the summed spaxels
    xw, yw = wl[fw], spec[fw]; ok = np.isfinite(yw); xw, yw = xw[ok], yw[ok]
    p0 = [0, 0, 0, 150, max(yw.max(), sig), sig, sig, sig]
    p, cov = curve_fit(model, xw, yw, p0=p0, sigma=np.full_like(yw, sig), absolute_sigma=True, maxfev=20000,
                       bounds=([-np.inf, -np.inf, -800, 40, 0, 0, 0, 0], [np.inf, np.inf, 800, 700] + [np.inf] * 4))
    pe = np.sqrt(np.diag(cov))
    wid = lambda k: lam0[k] * (1 + p[2] / C) * p[3] / C * np.sqrt(2 * np.pi)
    F = dict(Ha=p[4] * wid("Ha"), N2=p[5] * wid("N2b"), S2=p[6] * wid("S2a") + p[7] * wid("S2b"))
    snr = dict(Ha=p[4] / pe[4], N2=p[5] / pe[5], S2=(p[6] + p[7]) / np.sqrt(pe[6] ** 2 + pe[7] ** 2 + 2 * cov[6, 7]))
    draws = rng.multivariate_normal(p, cov, 20000)
    wHa, wN, wS1, wS2 = wid("Ha"), wid("N2b"), wid("S2a"), wid("S2b")
    ha_d, n2_d, s2_d = draws[:, 4] * wHa, draws[:, 5] * wN, draws[:, 6] * wS1 + draws[:, 7] * wS2
    good = (ha_d > 0) & (n2_d > 0) & (s2_d > 0)
    Zd = N2S2Ha(n2_d[good], s2_d[good], ha_d[good])
    res[name] = dict(nspax=int(sel.sum()), v=p[2], sigma=p[3], snr=snr, flux=F,
                     N2_Ha=F["N2"] / F["Ha"], S2_Ha=F["S2"] / F["Ha"],
                     OH=float(N2S2Ha(F["N2"], F["S2"], F["Ha"])), OH_draws=Zd, frac_valid=float(good.mean()))
    print(f"{name:5s} nspax={sel.sum():4d}  S/N Ha={snr['Ha']:.1f} N2={snr['N2']:.1f} S2={snr['S2']:.1f}  "
          f"[NII]/Ha={F['N2']/F['Ha']:.3f} [SII]/Ha={F['S2']/F['Ha']:.3f}  12+log(O/H)={res[name]['OH']:.3f} "
          f"(MC median {np.median(Zd):.3f}, 16-84% {np.percentile(Zd,16):.3f}-{np.percentile(Zd,84):.3f}, valid {good.mean():.2f})")

n = min(len(res["apex"]["OH_draws"]), len(res["tail"]["OH_draws"]))
dd = res["tail"]["OH_draws"][:n] - res["apex"]["OH_draws"][:n]
D = res["tail"]["OH"] - res["apex"]["OH"]; sD = 0.5 * (np.percentile(dd, 84) - np.percentile(dd, 16))
print(f"DELTA tail-apex = {D:+.3f} dex, sigma = {sD:.3f}, Delta/sigma = {D/sD:+.2f}; P(Delta<0) = {(dd<0).mean():.3f}")
out = dict(cube=os.path.basename(CUBE), delta=D, sigma=sD, p_neg=float((dd < 0).mean()),
           regions={k: {kk: (vv if not isinstance(vv, np.ndarray) else None) for kk, vv in v.items() if kk != "OH_draws"} for k, v in res.items()})
json.dump(out, open(os.path.join(r"C:\Users\jaden\cosmology\rbh1\out", "metallicity_" + os.path.basename(CUBE).replace(".fits", ".json")), "w"), indent=1, default=float)
