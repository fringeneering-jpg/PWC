# rcp28_field_ring.py - the wake's spatial spectrum: the field's recoil (2026-10-17)
# NOT fluid dynamics - field tension. The clumps are the tensioned field
# snapping back and ringing after the SMBH's passage. The FFT of the 1D
# profile extracts the ring's spatial wavelength = the substrate's stiffness.
import numpy as np
from astropy.io import fits
from scipy.ndimage import gaussian_filter

P = r"C:\Users\jaden\Downloads\PWC-Check\scratch\hst_jets\MAST_2026-09-19T0854\HST\jety02010\jety02010_drz.fits"
h = fits.open(P)
img = h[1].data if len(h) > 1 and h[1].data is not None else h[0].data
img = img.astype(float)

thr = np.nanpercentile(img, 99.0)
yy, xx = np.where(img > thr)
if len(xx) < 100:
    thr = np.nanpercentile(img, 97.0)
    yy, xx = np.where(img > thr)
c = np.column_stack([xx - xx.mean(), yy - yy.mean()])
cov = (c.T @ c) / len(c)
w, v = np.linalg.eigh(cov)
axis = v[:, np.argmax(w)]

t = (xx - xx.mean()) * axis[0] + (yy - yy.mean()) * axis[1]
tmin, tmax = np.nanpercentile(t, 1), np.nanpercentile(t, 99)
bins = np.linspace(tmin, tmax, 4000)
prof = np.zeros(len(bins) - 1)
for i in range(len(bins) - 1):
    sel = (t >= bins[i]) & (t < bins[i + 1])
    if sel.any():
        prof[i] = np.nanmean(img[yy[sel], xx[sel]])
prof = gaussian_filter(prof, 2)
prof = prof - np.nanmean(prof)

# the spatial spectrum (the field's ring)
dx = (tmax - tmin) / (len(bins) - 1)          # px per the bin
n = len(prof)
spec = np.abs(np.fft.rfft(prof))[1:]
freqs = np.fft.rfftfreq(n, d=dx)[1:]
wavelengths = 1.0 / np.maximum(freqs, 1e-12)  # px

# the dominant peaks of the spectrum (the ring's harmonics)
order = np.argsort(spec)[::-1]
print("THE FIELD'S RING - the wake's spatial spectrum (the finer read):")
print(f"  profile bins: {n}, the bin width {dx:.2f} px, the Nyquist ~{2*dx:.1f} px")
print("  dominant wavelengths (px):")
seen = []
for k in order[:20]:
    lam = wavelengths[k]
    if lam > 3000 or any(abs(lam - s) / max(lam, 1) < 0.12 for s in seen):
        continue
    seen.append(lam)
    print(f"    {lam:8.1f} px   (the spectral power {spec[k]:.2e})")
    if len(seen) >= 6:
        break
print()
print("the physical: ~0.4 kpc/px -> the knot-scale rings are the sub-500 px")
print("family. The finest resolvable spacing ~ the Nyquist ~2.6 px ~ 1 kpc.")
print()
print("honest notes: the pixel wavelengths convert to the physical kpc via the")
print("plate scale (ACS WFC ~0.05 arcsec/px) and RCP 28's distance (z=0.964,")
print("~8 kpc/arcsec) -> 1 px ~ 0.4 kpc. The dominant ring's the FIELD's")
print("recoil wavelength; the clock's prediction is the framework's side to")
print("state against it. No fluid analogies - the tension's the only actor.")
