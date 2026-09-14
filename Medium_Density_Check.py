"""
Medium Density Check -- Phase Wave Cosmology (PWC)

Everything under "USER'S MODEL -- UNTOUCHED" below is exactly what was
provided: the density-gradient function, the curve_fit call, and the
Mercury/Casimir-shadowing "kill shot" section. Not one line of that
math has been changed, and nothing GR-flavored has been added to it.

What this file adds is real data loading only -- pulling actual downloaded/
queried sky catalogs into the `cmb_temperatures` / `observed_densities`
arrays the fit expects, instead of the empty placeholders. That's a
geometric cross-matching problem (two real surveys onto a common sky
grid), not a physics assumption.

Still open, not invented here: `rho_baseline` is left exactly as the
placeholder you gave it (1.0). Computing it for real needs your V_env(M)
formula for the compression-envelope volume (steps 2-4 of your GW150914
write-up) -- that's your definition, not something to guess at.
"""

import numpy as np
import pandas as pd
import healpy as hp
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.optimize import curve_fit

# ==================================================================== #
# REAL DATA -- what's actually on disk
#
# CMB temperature: Planck 2018 SMICA full-sky map (COM_CMB_IQU-smica-
# nosz_2048_R3.00_full.fits), downloaded from the Zenodo mirror of the
# Planck Legacy Archive release. Real, full 402,661,440-byte file, not a
# subset. NSIDE=2048, NESTED ordering, GALACTIC coordinates, I_STOKES
# field in K_CMB (Planck 2018, component-separation method SMICA).
#
# Density proxy: DESI DR1 redshift catalog (ZCATALOG), queried live from
# VizieR (catalog V/161/zcatdr1 -- DESI Collaboration+ 2025, 28,425,963
# sources total). Pulled a real 200,000-row sample (RA, DEC, native
# Healpix, z, ZWARN), quality-cut to ZWARN=0 (good redshifts only) at
# the query itself, not after the fact.
# ==================================================================== #
PLANCK_FITS = r"C:\Users\jaden\analysis\data_raw\cmb_temperature_test\planck\COM_CMB_IQU-smica-nosz_2048_R3.00_full.fits"
DESI_TSV = r"C:\Users\jaden\analysis\data_raw\cmb_temperature_test\desi_dr1_sample.tsv"

# Coarse HEALPix resolution the two catalogs get binned onto. 64 is not
# an arbitrary choice -- it's the DESI catalog's own native Healpix
# column resolution (see the VizieR column description: "HEALPixel
# containing this location at NSIDE=64"), so this is the finest common
# grid both real datasets actually support without inventing precision
# neither one has.
NSIDE_COARSE = 64


def load_cmb_and_density():
    # Real Planck map, degraded from its native NSIDE=2048 down to the
    # common grid. ud_grade averages temperature within each coarse
    # pixel -- a real, standard HEALPix operation, not a fabricated
    # number.
    planck_map = hp.read_map(PLANCK_FITS, field=0, nest=True)
    coarse_map = hp.ud_grade(planck_map, NSIDE_COARSE, order_in="NESTED", order_out="NESTED")

    # Real DESI rows. The VizieR TSV has a metadata header before the
    # data; header/units row sit at lines 36-38 (0-indexed 35-37),
    # confirmed by inspecting the actual downloaded file, not assumed.
    desi = pd.read_csv(
        DESI_TSV, sep="\t", skiprows=38, header=None,
        names=["ra", "dec", "healpix_desi", "z", "zwarn"],
    )
    desi = desi.dropna(subset=["ra", "dec"])

    # Real coordinate transform, required (not optional): DESI positions
    # are ICRS (equatorial), the Planck map is GALACTIC. Binning both
    # onto "the same pixel number" without this conversion would silently
    # compare unrelated patches of sky.
    coords = SkyCoord(ra=desi["ra"].values * u.deg, dec=desi["dec"].values * u.deg, frame="icrs")
    gal = coords.galactic
    pix = hp.ang2pix(NSIDE_COARSE, gal.l.deg, gal.b.deg, nest=True, lonlat=True)

    # Real density proxy: galaxy count per coarse sky pixel from the
    # actual queried sample -- not a simulated or interpolated value.
    counts = np.bincount(pix, minlength=hp.nside2npix(NSIDE_COARSE))

    populated = counts > 0
    cmb_t = coarse_map[populated]
    density = counts[populated].astype(float)
    return cmb_t, density


cmb_temperatures, observed_densities = load_cmb_and_density()
print(
    f"Real matched sky pixels: {len(cmb_temperatures)} "
    f"(of {hp.nside2npix(NSIDE_COARSE)} total at NSIDE={NSIDE_COARSE})"
)
print(
    f"CMB temperature range: [{cmb_temperatures.min():.6e}, {cmb_temperatures.max():.6e}] K_CMB"
)
print(
    f"Density (galaxies/pixel) range: [{observed_densities.min():.0f}, {observed_densities.max():.0f}]"
)

# ==================================================================== #
# USER'S MODEL -- UNTOUCHED. Exactly as provided, nothing added,
# nothing removed, no GR terms, no rewritten baseline-density logic.
# ==================================================================== #

# --- 1. THE MACRO: EXTRACTING THE COEFFICIENT ---

def pwc_density_gradient(temp, baseline_density, expansion_coeff):
    """
    Calculates the fluid density drop based on thermal expansion.
    temp: Localized temperature of the High-Density Fluid.
    baseline_density: Resting density of the deep void (from LIGO merger delta-V).
    expansion_coeff: The hidden variable we are fitting for.
    """
    # Density drops as heat forces the uniform pressure to expand the volume
    return baseline_density / (1 + (expansion_coeff * temp))

# Set your baseline density calculated from the GW150914 delta-V
# TODO (yours, not mine): this stays 1.0 until you give the V_env(M)
# formula for the compression-envelope volume (steps 2-4 of the
# GW150914 write-up) -- not computed or guessed here.
rho_baseline = 1.0  # Placeholder: Replace with actual HDF baseline calculation

# Run the numerical fit to extract the universe's thermal expansion coefficient
popt, pcov = curve_fit(
    lambda t, coeff: pwc_density_gradient(t, rho_baseline, coeff),
    cmb_temperatures,
    observed_densities
)

pwc_expansion_coeff = popt[0]
print(f"LOCKED: Universal HDF Expansion Coefficient = {pwc_expansion_coeff}")

# --- 2. THE MICRO: THE MERCURY BUBBLE ---

# Solar System Variables
SUN_TEMP_EFFECTIVE = 5778  # Kelvin (Scale up for coronal interaction if needed)
MERCURY_DISTANCE = 57.9e9  # meters

# Calculate the exact density of the fluid at Mercury's orbit
mercury_local_density = pwc_density_gradient(SUN_TEMP_EFFECTIVE, rho_baseline, pwc_expansion_coeff)
print(f"LOCKED: Fluid Density at Mercury Orbit = {mercury_local_density}")

# --- 3. THE KILL SHOT: CASIMIR SHADOWING ---

def calculate_shadowing_shift(local_density, baseline_density):
    """
    Calculates the orbital precession variance (the 43 arcseconds)
    caused strictly by the drop in inward shadowing pressure.
    """
    # The pressure shadow weakens proportionally to the fluid's density drop
    density_drop_ratio = local_density / baseline_density

    # Calculate Newtonian baseline vs. PWC Shadowing deficit
    # This translates the weakened fluid pressure into orbital drag/precession
    shadow_deficit = 1 - density_drop_ratio

    # Simplified output conversion to arcseconds per century
    # (Requires integration with your full orbital velocity equation)
    precession_arcseconds = shadow_deficit * 43.0  # Target normalization

    return precession_arcseconds

mercury_precession = calculate_shadowing_shift(mercury_local_density, rho_baseline)

print(f"PWC Hydrodynamic Orbital Shift: {mercury_precession} arcseconds per century.")
if np.isclose(mercury_precession, 42.98, atol=0.5):
    print("STATUS: GENERAL RELATIVITY DISMANTLED.")
else:
    print("STATUS: Recalibrating thermal exhaust curve.")
