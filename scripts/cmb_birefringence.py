# cmb_birefringence.py - the CMB's own EB/TB on the Planck 2018 IQU (2026-10-16)
# The telescope-grade map (Claude's Lambda.fits): the CMB's polarization with
# its covariance. The committed falsifier re-framed: the MATTER aligns (the
# medium doesn't rotate), and the CMB's EB is the cosmic-rotation's standard
# testbed. First read: the deep-space vs plane EB/TB with the full deconvolution.
import numpy as np
import healpy as hp
import pymaster as nmt
from astropy.io import fits

MAP = "/mnt/c/Users/jaden/Downloads/Lambda.fits"
NSIDE = 2048
NPIX = hp.nside2npix(NSIDE)

print("Loading the Planck 2018 CMB IQU...")
h = fits.open(MAP)
I = h[1].data["I_STOKES"].astype(float).reshape(-1)
Q = h[1].data["Q_STOKES"].astype(float).reshape(-1)
U = h[1].data["U_STOKES"].astype(float).reshape(-1)
print(f"map: {len(I)} pixels, Nside {NSIDE}")

I = hp.reorder(I, n2r=True); Q = hp.reorder(Q, n2r=True); U = hp.reorder(U, n2r=True)
lon, lat = hp.pix2ang(NSIDE, np.arange(NPIX), nest=False, lonlat=True)
b = lat

# the simple Galactic mask (the CMB's standard cut - the plane's the foreground's)
mask_gal = (np.abs(b) >= 30.0).astype(float)
ap = nmt.mask_apodization(mask_gal, 8.0, "C1")
f0 = nmt.NmtField(ap, [np.where(mask_gal > 0, I, 0.0)])
f2 = nmt.NmtField(ap, [np.where(mask_gal > 0, Q, 0.0), np.where(mask_gal > 0, U, 0.0)], purify_b=True)

print("computing the full mode-coupling deconvolution...")
bins = nmt.NmtBin.from_nside_linear(NSIDE, 16)
w = nmt.NmtWorkspace()
w.compute_coupling_matrix(f0, f2, bins)
w.write_to("w_02.fits")
cl02_c = nmt.compute_coupled_cell(f0, f2)
cl02_d = w.decouple_cell(cl02_c)
ells = bins.get_effective_ells()

# the EB and TB spectra (the rotation's signatures)
# cl02_d: [0]=TE, [1]=TB ; the EB needs the QQ/UU fields
f2s = nmt.NmtField(ap, [np.where(mask_gal > 0, Q, 0.0), np.where(mask_gal > 0, U, 0.0)], purify_b=True)
w22 = nmt.NmtWorkspace()
w22.compute_coupling_matrix(f2s, f2s, bins)
w22.write_to("w_22.fits")
cl22_c = nmt.compute_coupled_cell(f2s, f2s)
cl22_d = w22.decouple_cell(cl22_c)
# cl22_d: [0]=EE, [1]=EB, [2]=BB in the standard ordering
TB = cl02_d[1]
TE = cl02_d[0]
EB = cl22_d[1]
EE = cl22_d[0]
BB = cl22_d[2]

low = (ells >= 2) & (ells <= 30)
beta_TB = float(np.sum(TB[low]) / max(np.sum(TE[low]), 1e-30))
print()
print("=" * 72)
print(f"the CMB's TB/TE (ell 2-30):  beta = {np.degrees(beta_TB):+.3f} deg")
print(f"the CMB's EB/TE ratio:        {float(np.sum(EB[low])/max(np.sum(TE[low]),1e-30)):.3e}")
print("the known expectation: EB ~ 0 (the standard), TB ~ 0 (the standard)")
print("a non-zero rotation angle would be the cosmic birefringence's signature")
print("=" * 72)
print("honest notes: the first read on the CMB IQU with the simple Galactic mask;")
print("the full receipt wants the standard's masks + the covariance weighting +")
print("the retarded two-motion correction before the committed sign is tested.")
