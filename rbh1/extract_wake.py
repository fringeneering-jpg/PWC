"""RBH-1 wake — model-neutral line maps from the re-reduced JWST GO-3149 NIRSpec IFU
mosaic (D:\\rbh1_reduction\\cube). No PWC quantity is used. Predictions were frozen
beforehand in PREDICTIONS_FROZEN.md (commit 472a9f4).

Input: continuum-subtracted, spike-clipped residual cube (out/mosaic_resid.npy; running
median continuum, 41 channels; |r| > 6 MAD clipped) and per-spaxel MAD noise.
Systemic z = 0.9628 from a data-driven Halpha-window scan (published: z = 0.96).
Binning 3x3 spaxels (0.3" ~ 2.5 kpc) for S/N. Noise per binned channel = MAD/3; drizzled
spaxels are correlated, so errors are UNDERESTIMATED (stated; bootstrap later).
Fits (shared v, sigma within each complex):
  Halpha + [N II]6548,6583 ([N II] 6583/6548 = 2.94 fixed)
  [S II]6716,6731 (free amplitudes)            [O III]4959,5007 (5007/4959 = 2.98)
Instrumental resolution 147 km/s FWHM at Halpha (van Dokkum et al., arXiv:2512.04166).
"""
import os, warnings
import numpy as np
from scipy.optimize import curve_fit
warnings.filterwarnings("ignore")
OUT = r"C:\Users\jaden\cosmology\rbh1\out"
C = 299792.458; Z0 = 0.9628; BIN = 3
L = dict(Ha=0.656280, N2a=0.654805, N2b=0.658345, S2a=0.671644, S2b=0.673081, O3a=0.495891, O3b=0.500684)
SIG_INST = 147.0 / 2.3548

r = np.load(os.path.join(OUT, "mosaic_resid.npy")).astype(float)
wl = np.load(os.path.join(OUT, "mosaic_wl.npy")); mad = np.load(os.path.join(OUT, "mosaic_mad.npy"))[0].astype(float)
nz, ny, nx = r.shape; ny, nx = ny // BIN * BIN, nx // BIN * BIN
rb = np.nanmean(r[:, :ny, :nx].reshape(nz, ny // BIN, BIN, nx // BIN, BIN), axis=(2, 4))
nb = np.sqrt(np.nanmean(mad[:ny, :nx].reshape(ny // BIN, BIN, nx // BIN, BIN) ** 2, axis=(1, 3))) / BIN

def g(x, a, mu, s): return a * np.exp(-0.5 * ((x - mu) / s) ** 2)

def fit(spec, sig, lines, ratios, win=2500):
    lo = min(L[k] for k in lines) * (1 + Z0) * (1 - win / C); hi = max(L[k] for k in lines) * (1 + Z0) * (1 + win / C)
    m = (wl > lo) & (wl < hi) & np.isfinite(spec)
    if m.sum() < 12 or not np.isfinite(sig) or sig <= 0: return None
    x, y = wl[m], spec[m]; lam0 = {k: L[k] * (1 + Z0) for k in lines}
    free = [k for k in lines if k not in ratios]
    def model(x, c0, dv, s, *a):
        out = np.full_like(x, c0); A = dict(zip(free, a))
        for k in lines:
            mu = lam0[k] * (1 + dv / C); amp = A[k] if k in A else A[ratios[k][0]] / ratios[k][1]
            out = out + g(x, amp, mu, mu * s / C)
        return out
    p0 = [0, 0, 150] + [max(np.nanmax(y), sig)] * len(free)
    try:
        p, cov = curve_fit(model, x, y, p0=p0, sigma=np.full_like(y, sig), absolute_sigma=True, maxfev=5000,
                           bounds=([-np.inf, -800, 40] + [0] * len(free), [np.inf, 800, 700] + [np.inf] * len(free)))
        pe = np.sqrt(np.diag(cov))
    except Exception:
        return None
    res = dict(v=p[1], ev=pe[1], sig=p[2], esig=pe[2])
    for i, k in enumerate(free):
        mu = lam0[k] * (1 + p[1] / C); w = mu * p[2] / C * np.sqrt(2 * np.pi)
        res[k], res["e" + k] = p[3 + i] * w, pe[3 + i] * w
    return res

H, W = rb.shape[1], rb.shape[2]
keys = ["Ha", "eHa", "N2b", "S2a", "S2b", "eS2a", "eS2b", "O3b", "eO3b", "v", "ev", "sig", "esig"]
M = {k: np.full((H, W), np.nan) for k in keys}
for j in range(H):
    for i in range(W):
        sp, s = rb[:, j, i], nb[j, i]
        a = fit(sp, s, ["Ha", "N2a", "N2b"], {"N2a": ("N2b", 2.94)})
        if not a or a["eHa"] <= 0 or a["Ha"] / a["eHa"] < 4: continue
        M["Ha"][j, i], M["eHa"][j, i], M["N2b"][j, i] = a["Ha"], a["eHa"], a.get("N2b", np.nan)
        M["v"][j, i], M["ev"][j, i], M["esig"][j, i] = a["v"], a["ev"], a["esig"]
        M["sig"][j, i] = np.sqrt(max(a["sig"] ** 2 - SIG_INST ** 2, 0))
        sII = fit(sp, s, ["S2a", "S2b"], {})
        if sII: M["S2a"][j, i], M["S2b"][j, i], M["eS2a"][j, i], M["eS2b"][j, i] = sII["S2a"], sII["S2b"], sII["eS2a"], sII["eS2b"]
        o = fit(sp, s, ["O3a", "O3b"], {"O3a": ("O3b", 2.98)})
        if o: M["O3b"][j, i], M["eO3b"][j, i] = o["O3b"], o["eO3b"]
n = int(np.isfinite(M["Ha"]).sum())
print(f"binned grid {H}x{W} ({BIN}x{BIN}); bins with Halpha S/N >= 4: {n}")
np.savez(os.path.join(OUT, "wake_maps.npz"), z0=Z0, bin=BIN, **M)
for k in ["Ha", "O3b", "v", "sig"]:
    f = M[k][np.isfinite(M[k])]
    if len(f): print(f"  {k:4s}: n={len(f)}  median={np.median(f):.3g}  range {np.min(f):.3g} .. {np.max(f):.3g}")
