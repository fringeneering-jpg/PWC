# Refined: ridge significance + far-half width in the STScI drizzle
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from scipy.ndimage import map_coordinates

path = r"C:\Users\jaden\cosmology\data\rbh1_rcp28\hst_acs_GO16912\hst_16912_02_acs_wfc_total_jety02_drc.fits"
hdul = fits.open(path)
data = hdul[1].data.astype(np.float64)
wcs = WCS(hdul[1].header)
gal = SkyCoord("2h41m45.43s -8d20m55.4s", frame="icrs")
dec_rad = np.deg2rad(gal.dec.deg)
pa = np.deg2rad(147.0)
kpc_per_as = 8.05

# electron-count noise: DRZ is in electrons/s; get EXPTIME and assume Poisson-ish per-pixel sigma from local rms
h = hdul[1].header
print("EXPTIME:", h.get('EXPTIME'), " units:", h.get('BUNIT'))

def profile(d_lo, d_hi, n_cuts=40, across_lim=3.0, n_across=600):
    across = np.linspace(-across_lim, across_lim, n_across)
    profs = []
    for d in np.linspace(d_lo, d_hi, n_cuts):
        dra_cd = d*np.sin(pa) + across*np.cos(pa)
        ddec = d*np.cos(pa) - across*np.sin(pa)
        ra = gal.ra.deg + dra_cd/3600.0/np.cos(dec_rad)
        dec = gal.dec.deg + ddec/3600.0
        pts = np.array([wcs.world_to_pixel_values(r_, d_) for r_, d_ in zip(ra, dec)])
        vals = map_coordinates(data, [pts[:,1], pts[:,0]], order=1, mode='nearest')
        profs.append(vals)
    return across, np.array(profs)

across, P = profile(2.0, 7.0, n_cuts=80)
P = P - np.median(P, axis=1, keepdims=True)

# per-cut rms in the wings
wing = (np.abs(across) > 1.5)
rms_per_cut = np.std(P[:, wing], axis=1)
print(f"per-cut wing rms (data units): median {np.median(rms_per_cut):.4f}")

# un-normalized stack: mean of cuts
stack_mean = np.mean(P, axis=0)
core = np.abs(across) < 0.3
sig = stack_mean[core].mean() / (np.std(P[:, core]) / np.sqrt(P.shape[0]))
print(f"stacked ridge significance in |s|<0.3\": mean excess / SE = {sig:.1f}")

# far-half stack (narrow part), normalized per cut to unit max
P_far = P[40:] / np.max(np.abs(P[40:]), axis=1, keepdims=True)
stack_far = np.median(P_far, axis=0)
from scipy.optimize import curve_fit
def g(x, a, c, s):
    return a*np.exp(-0.5*((x-c)/s)**2)
w = np.abs(across) < 0.8
try:
    p, _ = curve_fit(g, across[w], stack_far[w], p0=[stack_far.max(), 0.0, 0.12],
                     bounds=([0, -0.2, 0.01], [np.inf, 0.2, 0.8]))
    fw = 2.3548*p[2]
    print(f"far-half (d=4.6-7.0\") stacked FWHM = {fw:.3f}\" = {fw*kpc_per_as:.2f} kpc "
          f"(deconvolved {np.sqrt(max(fw**2-0.075**2,0)):.3f}\" = "
          f"{np.sqrt(max(fw**2-0.075**2,0))*kpc_per_as:.2f} kpc)")
except Exception as e:
    print("fit failed:", e)

# HWHM crossings as a model-free width
half = 0.5*stack_far.max()
above = stack_far > half
idx = np.where(above)[0]
if len(idx):
    print(f"HWHM crossing width (model-free): {across[idx[-1]]-across[idx[0]]:.3f}\" = "
          f"{(across[idx[-1]]-across[idx[0]])*kpc_per_as:.2f} kpc")
