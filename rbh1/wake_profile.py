"""RBH-1 along-wake profile — model-neutral, run blind against PREDICTIONS_FROZEN.md.

Geometry (published, van Dokkum et al. arXiv:2512.04166): the two IFU pointings sit on
opposite sides of the wake, 0.5" downstream of the tip. From the headers, WAKEPOS1/2 centres
give the cross-wake direction; the wake axis is perpendicular to it; the tip is 0.5" upstream
of the pointing midpoint. The downstream sign is the side holding more Halpha flux within
|y| < 0.5" (geometry only; both choices are reported).
Noise: empirical, from the same-width sums in many line-free windows (captures drizzle
correlation). Profiles: axial bins of 0.25" (~2.1 kpc); cross-axis Halpha profile fitted
with Gaussian + constant -> FWHM; bootstrap over line-free windows for errors.
"""
import glob, json, os, sys, warnings
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.optimize import curve_fit
from numpy.lib.stride_tricks import sliding_window_view
warnings.filterwarnings("ignore")

CUBE = sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob(r"D:\rbh1_reduction\cube_bkg\*_s3d.fits"))[0]
OUT = r"C:\Users\jaden\cosmology\rbh1\out"; os.makedirs(OUT, exist_ok=True)
C = 299792.458; Z = 0.9628; KPC_AS = 8.272
LINES = dict(Ha=0.656280, O3=0.500684, N2=0.658345, S2a=0.671644, S2b=0.673081)
P1 = SkyCoord(40.44051 * u.deg, -8.350361111111113 * u.deg); P2 = SkyCoord(40.44026166666667 * u.deg, -8.350525000000005 * u.deg)

f = fits.open(CUBE); h = f["SCI"].header
d = f["SCI"].data.astype(float); d[(f["DQ"].data & 1) != 0] = np.nan
wl = h["CRVAL3"] + (np.arange(h["NAXIS3"]) + 1 - h["CRPIX3"]) * h["CDELT3"]
W = 41; pad = np.pad(d, ((W // 2, W // 2), (0, 0), (0, 0)), mode="edge")
r = d - np.nanmedian(sliding_window_view(pad, W, axis=0), axis=-1)
mad = np.nanmedian(np.abs(r), axis=0, keepdims=True) * 1.4826; r[np.abs(r) > 6 * mad] = np.nan

def win(l0, dv=250): return np.abs(wl / (l0 * (1 + Z)) - 1) * C < dv
def nb(mask): return np.nansum(r[mask], 0)
# empirical noise maps: same-width windows in line-free regions near Halpha and [O III]
def noise_windows(l0, n=40):
    base = win(l0); w = base.sum(); centre = np.argmax(base)
    offs = [o for o in range(-300, 300, w + 2) if abs(o) > 3 * w]
    stacks = []
    for o in offs:
        m = np.zeros_like(base); lo = centre - w // 2 + o
        if lo < 0 or lo + w >= len(wl): continue
        m[lo:lo + w] = True
        if any(np.any(win(v, 600) & m) for v in LINES.values()): continue
        stacks.append(nb(m))
    return np.array(stacks)
NHa, NO3 = noise_windows(LINES["Ha"]), noise_windows(LINES["O3"])
Ha, O3 = nb(win(LINES["Ha"])), nb(win(LINES["O3"]))
sHa = np.nanstd(NHa, 0); sO3 = np.nanstd(NO3, 0)
print(f"cube {os.path.basename(CUBE)}; noise windows Ha={len(NHa)} O3={len(NO3)}")

wcs = WCS(h).celestial; ny, nx = Ha.shape
yy, xx = np.mgrid[0:ny, 0:nx]; sky = wcs.pixel_to_world(xx, yy)
mid = SkyCoord((P1.ra + P2.ra) / 2, (P1.dec + P2.dec) / 2)
dE = ((sky.ra - mid.ra) * np.cos(mid.dec.radian)).to(u.arcsec).value; dN = (sky.dec - mid.dec).to(u.arcsec).value
cE = ((P1.ra - P2.ra) * np.cos(mid.dec.radian)).to(u.arcsec).value; cN = (P1.dec - P2.dec).to(u.arcsec).value
pa_cross = np.degrees(np.arctan2(cE, cN)); pa_axis = pa_cross + 90
ua = np.array([np.sin(np.radians(pa_axis)), np.cos(np.radians(pa_axis))])
proj = dE * ua[0] + dN * ua[1]; perp = dE * np.cos(np.radians(pa_axis)) - dN * np.sin(np.radians(pa_axis))
near = np.abs(perp) < 0.5
fp, fm = np.nansum(Ha[near & (proj > 0)]), np.nansum(Ha[near & (proj < 0)])
sgn = 1 if fp >= fm else -1
x = sgn * proj + 0.5; y = sgn * perp  # x: arcsec downstream from tip
print(f"cross-wake PA {pa_cross:.1f} deg; axis PA {pa_axis:.1f}/{pa_axis+180:.1f}; Halpha near axis: +side {fp:.3g}, -side {fm:.3g} -> downstream sign {sgn:+d}")

GHOST = float(os.environ.get("GHOST_AS", "0"))  # >0: model background self-subtraction ghosts at +/-GHOST arcsec
def gauss(yv, a, y0, s, c, b=0.0):
    G = lambda m: np.exp(-0.5 * ((yv - m) / s) ** 2)
    return a * G(y0) - (b * (G(y0 + GHOST) + G(y0 - GHOST)) if GHOST > 0 else 0) + c
rows = []; edges = np.arange(-1.0, x[np.isfinite(Ha)].max() + 0.25, 0.25)
rng = np.random.default_rng(1)
for lo in edges[:-1]:
    sel = (x >= lo) & (x < lo + 0.25) & (np.abs(y) < 1.5) & np.isfinite(Ha)
    if sel.sum() < 15: continue
    yb = np.arange(-1.5, 1.5001, 0.1); prof = []; perr = []
    for yc in yb:
        s = sel & (np.abs(y - yc) < 0.05)
        prof.append(np.nansum(Ha[s])); perr.append(np.sqrt(np.nansum(sHa[s] ** 2)))
    prof, perr = np.array(prof), np.array(perr); perr[perr <= 0] = np.nanmedian(perr[perr > 0])
    row = dict(x_as=lo + 0.125, x_kpc=(lo + 0.125) * KPC_AS, n_spax=int(sel.sum()),
               Ha_sum=float(np.nansum(Ha[sel])), Ha_err=float(np.sqrt(np.nansum(sHa[sel] ** 2))),
               O3_sum=float(np.nansum(O3[sel])), O3_err=float(np.sqrt(np.nansum(sO3[sel] ** 2))))
    try:
        p, cov = curve_fit(gauss, yb, prof, p0=[max(prof.max(), 1e-3), 0, 0.2, 0] + ([0.5 * max(prof.max(), 1e-3)] if GHOST > 0 else []), sigma=perr, absolute_sigma=True,
                           bounds=([0, -1.2, 0.04, -np.inf] + ([0] if GHOST > 0 else []), [np.inf, 1.2, 1.2, np.inf] + ([np.inf] if GHOST > 0 else [])), maxfev=5000)
        fw = []
        for _ in range(200):
            try:
                pb, _ = curve_fit(gauss, yb, prof + rng.normal(0, perr), p0=p, sigma=perr,
                                  bounds=([0, -1.2, 0.04, -np.inf] + ([0] if GHOST > 0 else []), [np.inf, 1.2, 1.2, np.inf] + ([np.inf] if GHOST > 0 else [])), maxfev=3000)
                fw.append(2.3548 * pb[2])
            except Exception: pass
        row.update(ghost_ratio=float(p[4] / p[0]) if GHOST > 0 and p[0] > 0 else np.nan, ridge_amp_snr=float(p[0] / np.sqrt(cov[0, 0])), y0_as=float(p[1]),
                   fwhm_as=float(2.3548 * p[2]), fwhm_err=float(np.std(fw)) if fw else np.nan,
                   fwhm_kpc=float(2.3548 * p[2] * KPC_AS))
    except Exception:
        row.update(ridge_amp_snr=np.nan, y0_as=np.nan, fwhm_as=np.nan, fwhm_err=np.nan, fwhm_kpc=np.nan)
    row["Ha_snr"] = row["Ha_sum"] / row["Ha_err"] if row["Ha_err"] > 0 else np.nan
    row["O3_Ha"] = row["O3_sum"] / row["Ha_sum"] if row["Ha_sum"] > 0 else np.nan
    rows.append(row)

json.dump(dict(cube=os.path.basename(CUBE), z=Z, kpc_per_arcsec=KPC_AS, axis_pa=float(pa_axis),
               downstream_sign=sgn, rows=rows), open(os.path.join(OUT, "wake_profile.json"), "w"), indent=1)
print(f"ghost model: {GHOST} arcsec"); print(f"{'x(kpc)':>7} {'Ha S/N':>7} {'ridge S/N':>9} {'FWHM(kpc)':>12} {'y0(as)':>7} {'[OIII]/Ha':>9}")
for rw in rows:
    print(f"{rw['x_kpc']:7.1f} {rw['Ha_snr']:7.1f} {rw['ridge_amp_snr']:9.1f} {rw['fwhm_kpc']:7.2f}±{rw['fwhm_err']*KPC_AS:4.2f} {rw['y0_as']:7.2f} {rw['O3_Ha']:9.2f}")
