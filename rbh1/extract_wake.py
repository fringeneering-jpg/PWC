"""RBH-1 wake — model-neutral line maps and along-wake table from the re-reduced
JWST GO-3149 NIRSpec IFU mosaic (D:\\rbh1_reduction\\cube). No PWC quantity is used.
Predictions were frozen beforehand in PREDICTIONS_FROZEN.md (commit 472a9f4).

Per spaxel (after 2x2 binning for S/N), fits with a local linear continuum:
  Halpha + [N II]6548,6583 : shared v, sigma; [N II] 6583/6548 fixed 2.94
  [S II]6716,6731          : shared v, sigma; free amplitudes (density ratio)
  [O III]4959,5007         : shared v, sigma; 5007/4959 fixed 2.98
Instrumental resolution: 147 km/s FWHM at Halpha (van Dokkum et al. 2025, arXiv:2512.04166),
removed in quadrature as sigma_inst = 62.4 km/s. Density from [S II] 6716/6731 via Sanders et al. 2016 (T = 1e4 K).
"""
import glob, json, os, sys, warnings
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.cosmology import Planck18
from scipy.optimize import curve_fit
warnings.filterwarnings("ignore")

CUBE = sorted(glob.glob(r"D:\rbh1_reduction\cube\*_s3d.fits"))
OUT = r"C:\Users\jaden\cosmology\rbh1\out"; os.makedirs(OUT, exist_ok=True)
C = 299792.458
L = dict(Ha=0.656280, N2a=0.654805, N2b=0.658345, S2a=0.671644, S2b=0.673081, O3a=0.495891, O3b=0.500684)
SIG_INST = 147.0 / 2.3548  # van Dokkum et al. (arXiv:2512.04166): resolution 147 km/s at Halpha (FWHM)

f = fits.open(CUBE[0]); h = f["SCI"].header
sci, err, dq = f["SCI"].data.astype(float), f["ERR"].data.astype(float), f["DQ"].data
sci[(dq & 1) != 0] = np.nan
wl = h["CRVAL3"] + (np.arange(h["NAXIS3"]) + 1 - h["CRPIX3"]) * h["CDELT3"]
pix_as = abs(h["CDELT1"]) * 3600.0
# 2x2 spatial binning
ny, nx = sci.shape[1] // 2 * 2, sci.shape[2] // 2 * 2
B = lambda a, agg: agg(agg(a[:, :ny, :nx].reshape(len(wl), ny // 2, 2, nx // 2, 2), axis=4), axis=2)
sb = B(sci, np.nanmean); eb = np.sqrt(B(err**2, np.nanmean) / 4.0)
bin_as = 2 * pix_as

def g(x, a, mu, s): return a * np.exp(-0.5 * ((x - mu) / s) ** 2)

def fit_complex(spec, e, z0, lines, ratios, win_kms=3000):
    lo = min(L[k] for k in lines) * (1 + z0) * (1 - win_kms / C); hi = max(L[k] for k in lines) * (1 + z0) * (1 + win_kms / C)
    m = (wl > lo) & (wl < hi) & np.isfinite(spec) & np.isfinite(e) & (e > 0)
    if m.sum() < 15: return None
    x, y, s = wl[m], spec[m], e[m]
    lam0 = {k: L[k] * (1 + z0) for k in lines}
    def model(x, c0, c1, dv, sig, *amps):
        out = c0 + c1 * (x - x.mean())
        ai = 0
        for k in lines:
            mu = lam0[k] * (1 + dv / C); sg = mu * sig / C
            a = amps[ai] if k not in ratios else amps[lines.index(ratios[k][0])] / ratios[k][1]
            if k not in ratios: ai += 1
            out = out + g(x, a, mu, sg)
        return out
    nfree = sum(1 for k in lines if k not in ratios)
    p0 = [np.nanmedian(y), 0, 0, 150] + [max(np.nanmax(y) - np.nanmedian(y), 1e-6)] * nfree
    try:
        p, cov = curve_fit(model, x, y, p0=p0, sigma=s, absolute_sigma=True, maxfev=4000,
                           bounds=([-np.inf, -np.inf, -1500, 30] + [0] * nfree, [np.inf, np.inf, 1500, 800] + [np.inf] * nfree))
        pe = np.sqrt(np.diag(cov))
    except Exception:
        return None
    res = dict(v=p[2], ev=pe[2], sig=p[3], esig=pe[3])
    ai = 0
    for k in lines:
        if k in ratios: continue
        mu = lam0[k] * (1 + p[2] / C); sg = mu * p[3] / C
        res[k] = p[4 + ai] * sg * np.sqrt(2 * np.pi); res["e" + k] = pe[4 + ai] * sg * np.sqrt(2 * np.pi); ai += 1
    return res

# systemic redshift from the brightest-Halpha binned spaxels (search z = 0.95-0.98)
zgrid = np.linspace(0.95, 0.98, 601)
nb = ((np.abs(wl[:, None] - L["Ha"] * (1 + zgrid)[None, :]) < 0.0008))
flat = np.nan_to_num(sb.reshape(len(wl), -1)); cont = np.nanmedian(flat, axis=0)
score = np.array([np.nansum((flat[nb[:, i]] - cont), axis=0) for i in range(len(zgrid))])
best = np.unravel_index(np.nanargmax(score), score.shape); z0 = zgrid[best[0]]
print(f"systemic z (Halpha peak search) = {z0:.4f}")

H, W = sb.shape[1], sb.shape[2]
maps = {k: np.full((H, W), np.nan) for k in ["Ha", "eHa", "N2b", "S2a", "S2b", "eS2a", "eS2b", "O3b", "eO3b", "v", "sig", "esig"]}
for j in range(H):
    for i in range(W):
        sp, e = sb[:, j, i], eb[:, j, i]
        r = fit_complex(sp, e, z0, ["Ha", "N2a", "N2b"], {"N2a": ("N2b", 2.94)})
        if r and r["eHa"] > 0 and r["Ha"] / r["eHa"] > 5:
            maps["Ha"][j, i], maps["eHa"][j, i] = r["Ha"], r["eHa"]; maps["N2b"][j, i] = r.get("N2b", np.nan)
            maps["v"][j, i] = r["v"]; maps["sig"][j, i] = np.sqrt(max(r["sig"] ** 2 - SIG_INST ** 2, 0)); maps["esig"][j, i] = r["esig"]
            s2 = fit_complex(sp, e, z0, ["S2a", "S2b"], {})
            if s2: maps["S2a"][j, i], maps["S2b"][j, i], maps["eS2a"][j, i], maps["eS2b"][j, i] = s2["S2a"], s2["S2b"], s2["eS2a"], s2["eS2b"]
            o3 = fit_complex(sp, e, z0, ["O3a", "O3b"], {"O3a": ("O3b", 2.98)})
            if o3: maps["O3b"][j, i], maps["eO3b"][j, i] = o3["O3b"], o3["eO3b"]
print("spaxels with Halpha S/N > 5:", int(np.isfinite(maps["Ha"]).sum()))
wcs = WCS(h).celestial
np.savez(os.path.join(OUT, "wake_maps.npz"), z0=z0, bin_as=bin_as, **maps)
fits.writeto(os.path.join(OUT, "wake_Ha_map.fits"), maps["Ha"], wcs[::2, ::2].to_header() if hasattr(wcs, "__getitem__") else None, overwrite=True)
print("maps saved")
