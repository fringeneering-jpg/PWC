# HST wake-width measurement: RCP 28 / RBH-1 trail FWHM vs the published 0.7 kpc radius
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import astropy.units as u

path = r"C:\Users\jaden\cosmology\data\rbh1_rcp28\hst_acs_GO16912\hst_16912_02_acs_wfc_total_jety02_drc.fits"
print("opening", path)
hdul = fits.open(path)
data = hdul[1].data.astype(np.float64)
wcs = WCS(hdul[1].header)
print("image shape:", data.shape)

gal = SkyCoord("2h41m45.43s -8d20m55.4s", frame="icrs")
x0, y0 = wcs.world_to_pixel(gal)
print(f"galaxy at pixel ({x0:.1f}, {y0:.1f})")

# plate scale (arcsec/pix) from the WCS
cd = np.array([[hdul[1].header.get('CD1_1', 1), hdul[1].header.get('CD1_2', 0)],
               [hdul[1].header.get('CD2_1', 0), hdul[1].header.get('CD2_2', 1)]])
scale = np.sqrt(abs(np.linalg.det(cd))) * 3600.0
print(f"pixel scale: {scale:.4f} arcsec/pix")

# kpc per arcsec at z = 0.964 (LambdaCDM D_A ~ 1.66 Gpc)
kpc_per_as = 1660.0e6 * (np.pi/180.0/3600.0) / 1e3
print(f"plate scale: {kpc_per_as:.2f} kpc/arcsec")

# trail: from galaxy to tip at PA 147 deg (tip is 7.7" away), then a margin
pa_deg = 147.0
d_tip = 7.7          # arcsec to the tip
half = 6.0           # cross-axis half-width in arcsec for the profile

pa = np.deg2rad(pa_deg)
dec_rad = np.deg2rad(gal.dec.deg)
n_along = 400
along = np.linspace(-1.0, d_tip + 2.0, n_along)         # arcsec from galaxy outward
n_across = 400
across = np.linspace(-half, half, n_across)

# perpendicular sampling (fixed):  dRA*cos(dec) = d*sin(PA) + s*cos(PA)
#                                  dDec         = d*cos(PA) - s*sin(PA)
profiles = []
for d in np.linspace(0.0, d_tip, 60):
    dra_cd = d*np.sin(pa) + across*np.cos(pa)
    ddec = d*np.cos(pa) - across*np.sin(pa)
    ra = gal.ra.deg + dra_cd/3600.0/np.cos(dec_rad)
    dec = gal.dec.deg + ddec/3600.0
    from scipy.ndimage import map_coordinates
    pts = np.array([wcs.world_to_pixel_values(ra_, de_) for ra_, de_ in zip(ra, dec)])
    vals = map_coordinates(data, [pts[:,1], pts[:,0]], order=1, mode='nearest')
    vals = vals - np.median(vals)
    m = np.nanmax(np.abs(vals))
    profiles.append(vals/m if m > 0 else vals)

profiles = np.array(profiles)
stack = np.nanmedian(profiles[8:52], axis=0)     # avoid galaxy (d<~2") and the tip knot
stack = stack - np.median(stack)

# gaussian fit on the stacked profile
w = np.abs(across) < 1.0
from scipy.optimize import curve_fit
def g(x, a, c, s):
    return a*np.exp(-0.5*((x-c)/s)**2)
try:
    p, _ = curve_fit(g, across[w], stack[w], p0=[stack.max(), 0.0, 0.15],
                     bounds=([0, -0.3, 0.01], [np.inf, 0.3, 1.5]))
    fw_stack = 2.3548*p[2]
    print(f"\nstacked cross-axis profile (d = 2.1-6.7\", median of 44 cuts):")
    print(f"  fitted FWHM = {fw_stack:.3f} arcsec = {fw_stack*kpc_per_as:.2f} kpc")
    print(f"  PSF ~0.075\" -> deconvolved = {np.sqrt(max(fw_stack**2-0.075**2,0)):.3f}\" = "
          f"{np.sqrt(max(fw_stack**2-0.075**2,0))*kpc_per_as:.2f} kpc")
    print(f"  published: tail radius 0.7 kpc (FWHM 1.4-1.6 kpc)")
except Exception as e:
    print("fit failed:", e)
    fw_stack = np.nan

# save a cutout PNG for a visual check
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8, 3))
# cutout in pixels: 10" x 8" box around the trail
from scipy.ndimage import map_coordinates as mc
# make a rotated cutout: sample a grid in (along, across) and imshow it
grid_d, grid_s = np.meshgrid(np.linspace(2.0, 9.5, 700), np.linspace(-4, 4, 500))
dra_cd = grid_d*np.sin(pa) + grid_s*np.cos(pa)
ddec = grid_d*np.cos(pa) - grid_s*np.sin(pa)
ra_g = gal.ra.deg + dra_cd/3600.0/np.cos(dec_rad)
dec_g = gal.dec.deg + ddec/3600.0
pts = np.array([wcs.world_to_pixel_values(r_, d_) for r_, d_ in zip(ra_g.ravel(), dec_g.ravel())])
cut = mc(data, [pts[:,1].reshape(grid_d.shape), pts[:,0].reshape(grid_d.shape)], order=1)
vmin, vmax = np.nanpercentile(cut, [20, 99.5])
ax.imshow(cut, origin='lower', aspect='auto', cmap='gray_r', vmin=vmin, vmax=vmax,
          extent=[2.0, 9.5, -4, 4])
ax.set_xlabel("distance from galaxy (arcsec)")
ax.set_ylabel("cross-axis (arcsec)")
ax.set_title("RCP 28 streak, HST total (F606W+F814W) - PA 147")
fig.savefig(r"C:\Users\jaden\Downloads\PWC-Check\scratch\rcp28_streak_cutout.png", dpi=100)
print("cutout saved: scratch/rcp28_streak_cutout.png")
