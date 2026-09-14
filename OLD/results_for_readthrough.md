# Results for read-through

All numbers below are either freshly computed this session (Part 1) or read directly from
already-executed scripts in `C:\Users\jaden\analysis\` and `C:\Users\jaden\analysis_verified_rerun\`
(Part 2), which pull real catalogs from VizieR/CDS (access date 2026-07-20). Nothing here is
simulated. Numbers are reported as computed; no framing added either direction.

---

## PART 1 — Quick tests run this session

### Test 1: CMB pressure-variance mapping (Planck 143 GHz, `HFI_SkyMap_143_2048_R3.01_full.fits`)
- Mean-subtracted, top/bottom 5% pixel maps generated (`dense_mud.png`, `cavitation_voids.png`,
  now in `C:\Users\jaden\Pictures\`).
- Follow-up check: largest contiguous hot/cold region outside the galactic plane (|b|>20 deg).
  Top-1% hot pixels: centroid l=339.9, b=-4.9, angular spread up to 164.8 deg from centroid
  (out of a max possible ~180 deg). Bottom-1% cold pixels: centroid l=215.2, b=-2.2, spread up
  to 160.3 deg. Both extremes are scattered across most of the unmasked sky, not concentrated
  into one localized region.

### Test 2: Bow-shock thermal-exhaust arithmetic
- Fixed constants (galaxy velocity 600 km/s, fluid density 0.0147 atoms/cm^3) plugged into
  0.5*rho*v^2 = 2646.0 "units of thermal friction." Formula only; no measured data compared.

### Test 3: Satellite flyby drafting-anomaly check
| Probe | Predicted wake surge (area/mass x1000) | Actual measured boost (mm/s) | Ratio |
|---|---|---|---|
| Rosetta | 22.07 | 1.80 | 12.3x |
| Cassini | 4.35 | 0.11 | 39.5x |
| NEAR | 17.39 | 13.46 | 1.3x |
Ratio spans 12.3x-39.5x across the three probes (not constant).

### Test 4: tSZ pressure profile, hypothesis curves vs. real GNFW
Two hand-specified curves (smooth exponential vacuum decay; hard cliff at 1.5 Mpc) plotted
against the Arnaud et al. universal GNFW pressure profile (real fit form used for stacked
Planck cluster data, c500=1.18, alpha=1.05, beta=5.49, gamma=0.31, R500~1.3 Mpc for Coma).
GNFW falls off smoothly and faster than both hand-specified curves; no discontinuity at 1.5 Mpc
or anywhere else. `coma_profile.csv` (a specific local overlay file) was not found in
`data_raw/tsz_pressure/`, so no local/real Coma-specific profile was overlaid — only the
general GNFW fit form.

### Test 5: Expansion-mechanics vector field (illustrative, not fit to data)
Two panels plotted: radial expansion from origin (0,0), and radial expansion from an
arbitrary "observer" point (-5,-5). Both panels use the identical formula v=position-origin;
they are the same math evaluated from two vantage points, not two different physical models.

### PSZ2 3D macro-current map
1094 SZ-detected clusters (Planck PSZ2, z>0 subset) converted to 3D Cartesian via
GLON/GLAT/redshift (dist = z*4280 Mpc proxy) and plotted, sized by mass (MSZ), colored by
thermal signature (Y5R500). Figure saved, no clustering/void statistic computed on it.

### Framework-native heat-leak vs. constant-term expansion fit
Standard Domain-D test (below) infers w(z) via a flat-wCDM fit (vacuum-shaped dark-energy
term) and checks if w correlates with SFRD(z) — found flat, p=0.71 (see Part 2, Domain D
cosmic-expansion note). Redone with zero vacuum/w term: built E(z)^2 = Om(1+z)^3 + (1-Om)*g(z),
where g(z) is the cumulative Madau & Dickinson SFRD history (normalized 1 today, 0 at high z,
using a matter-only Einstein-de Sitter time-weighting, not a dark-energy one), fit directly to
all 1701 real Pantheon+ magnitudes with the same 2 free parameters (Om, offset) as the standard
model:

| Model | Om | chi^2 | dof | chi^2/dof |
|---|---|---|---|---|
| Heat-leak (g(z) from cumulative SFRD) | 0.409+/-0.011 | 759.80 | 1699 | 0.4472 |
| Standard constant-vacuum-term (w=-1) | 0.351+/-0.012 | 758.79 | 1699 | 0.4466 |

Delta chi^2 = 1.01, same parameter count -- statistically indistinguishable fit quality on
real Pantheon+ data.

---

## PART 2 — Full statistical pipeline (real archival data)

### A1 — Interstellar filaments (Ge & Wang 2022, n=137)
Target: aspect ratio (fA). choke_F2 R^2=0.011; mass_only R^2=0.025 (p=0.06, not significant).
No proxy or baseline clears ~3% of variance. Threshold/decile test: Kruskal-Wallis p=0.012 but
non-monotonic (single-decile spike), top-decile-vs-rest not significant (p=0.58).

### A2 — Intergalactic/cosmic-web filaments (Tempel et al. 2014, n=15,421)
Target: thickness_proxy (construction-independent). choke_F1 R^2=0.0052 (r=-0.07, p=4e-19);
choke_F2 R^2=0.00005 (p=0.39, n.s.); length_only R^2=0.0077; richness_only R^2=0.0035.
All R^2<0.01. Separately, choke_F2 vs. concentration_Ng shows r=0.77, but this is 96%-explained
by algebra shared between the two definitions (verified: log(choke_F2) vs. log[x/(1-x)]
r=0.962) -- not independent signal.
Threshold test: top-decile thickness 5% lower than rest (p=0.003), bottom-decile 4% higher
(p=0.03), Kruskal-Wallis p=2e-4 -- small (~5%) but correctly-signed and statistically solid
given n=15,421.

### B — Galactic HII-region bubbles (Anderson et al. 2014, n=826)
Target: R_pc (physical radius). driving_only R^2=0.0083 (r=-0.09, p=0.009, wrong-signed --
larger line width -> smaller radius); ambient_only R^2=0.1113 (r=-0.33, p=6e-23); choke_B1
R^2=0.0689; choke_B2 R^2=0.0983; driving+ambient additive R^2=0.1218 (best of all forms tested).
Ambient-resistance partial correlation holds within all 3 driving terciles (r=-0.44,-0.27,-0.34,
all p<1e-4).
Threshold test: top-decile choke_B1 median R=6.8 pc vs. 3.7 pc for the rest (83% larger),
Mann-Whitney p=8e-10, Kruskal-Wallis p=9e-11.

### C — Cluster lensing, richness x WL-mass forecast (redMaPPer x Sereno & Ettori, n=26,111)
MWLc (mass forecast) vs. richness alone: r=0.978, R^2=0.973 (i.e. MWLc carries almost no
information beyond richness+z). Regression: lambda+z baseline R^2=0.9728, +neighbor_density_knn
extended R^2=0.9748 (delta=0.0020). Classification (structured vs. unstructured environment,
held-out AUC): lambda-only 0.618, MWLc-only 0.576, lambda x MWLc combined 0.700.

### C2 — Cluster lensing, richness x tSZ Y-parameter (PSZ2, n=300)
Y5R500 vs. richness+z: R^2=0.220 (much less degenerate with richness than MWLc was).
Regression: lambda+z baseline R^2=0.2202, +neighbor extended R^2=0.2225 (delta=0.0023,
neighbor coefficient p=0.354, not significant). Classification (n_labeled=200, held-out AUC):
lambda-only 0.670, Y5R500-only 0.596, combined 0.698.

### D — Planetary magnetospheres, PILOT n=6 (Mercury, Earth, Jupiter, Saturn, Uranus, Neptune)
Spearman rho vs. real measured magnetopause standoff distance (planetary radii):
- naive choke_D1 (dipole moment / solar-wind pressure, power=1): rho=0.943
- Chapman-Ferraro predictor (dipole^2/P_sw)^(1/6) -- the actual textbook-correct physics for
  this system: rho=0.829
- driving_proxy (dipole moment) alone: rho=0.829
At n=6 this is a pilot, not a powered test -- but as computed, the naive linear ratio ranks
higher than the known-correct 1/6-power law.

### D2 — Force-balance check, planets only (n=6, the one domain with real calibrated units)
Ratio of magnetic pressure at the *measured* standoff distance to solar-wind dynamic pressure
(should be ~1, within a factor of ~2, if real geometry matches simple dipole balance):
Mercury 0.142, Earth 0.199, Jupiter 0.0133, Saturn 0.0709, Uranus 0.509, Neptune 0.138.
All are below the naive-balance value; Uranus is the closest to the expected 0.5-2.0 range.
Not run for HII bubbles or galaxy clusters -- those catalogs have no calibrated local pressure
in physical units, only relative/integrated proxies, so the check would not be genuine there.

### E — FRB-cluster proximity, naive (CHIME/FRB Catalog 1 x Planck PSZ2, n=600)
Spearman(separation, DM excess) r=0.470, p=2.7e-34. Close-to-cluster (<2 deg, n=221) median
DM excess=39.1; far-from-cluster (>10 deg, n=47) median=323.3, Mann-Whitney p=6.1e-27 --
i.e. FRBs *far* from clusters show *higher* DM excess than those close, in the raw comparison.

### E2 — FRB-cluster proximity, galactic-latitude-controlled (n=600)
Raw result above is confounded: |GLAT| correlates r=-0.98 with the naive DM-excess variable
and rho=-0.54 with distance to nearest cluster. Three methods to control for it:
- Method A (decile-binned residuals): Spearman r=0.121, p=0.003
- Method B (degree-2 polynomial regression residuals): Spearman r=0.496, p=1.55e-38;
  GLAT alone explains R^2=0.851 of DM-excess variance
- Method C (stratified, same-latitude-decile pairs): returned no result (empty)
Methods A and B disagree substantially (0.12 vs. 0.50) even though both are meant to control
for the same confound; this is reported as-is, not resolved.

### F — Cross-scale pressure/density, 3 phases
- Phase 1 (planetary, Earth only clean case): magnetosheath/interior density ratio = 50.0x.
  Jupiter/Saturn have real but non-comparable numbers (internal plasma sources: Io torus,
  icy-moon sources) -- not reported as clean confirmations.
- Phase 2 (HII bubbles, n=826): R_pc vs. ambient pressure model r=-0.353 (p=1.3e-25); R_pc vs.
  driving r=-0.090 (p=0.0096). (ambient_resistance_proxy is a pressure model, not a measured
  density -- this catalog has no per-object density data.)
- Phase 3 (clusters, n=300): log(Y5R500) vs. log(neighbor_density_knn), Spearman r=0.242
  (p=2.3e-5), OLS R^2=0.061, slope=0.120 (p=1.5e-5) -- weak but statistically solid positive
  relationship between local environment density and tSZ pressure signal.

### G — Cluster entropy profile shape (ACCEPT archive, Chandra X-ray, n=240)
Entropy power-law fits K(r)=K0+K100*(r/100kpc)^alpha. alpha>0 (entropy rising with radius,
implying density falling with radius) in 240/240 clusters (100%). Median alpha=1.245; median
entropy ratio at 500 kpc vs. core = 19.6x. Real X-ray density structure is smoothly
centrally-concentrated in every cluster in the sample -- no case shows a dense compressed
shell piling up at the boundary the way a wind-blown stellar-bubble shell does.

---

## PART 3 — De-Lambda'd rerun: separating framework-native results from GR/vacuum-contaminated ones

Both Domain C (`03_lensing.py`) and Domain C2 (`07_lensing_tsz_pressure.py`) built their
"ambient/environment" term (`neighbor_density_knn`) using `astropy.cosmology.Planck18` --
a LCDM/vacuum-energy cosmology mixed into what was supposed to be an independent structure
measurement. Rebuilt using the heat-leak E(z) from Part 1 (Om=0.4093, zero vacuum/w term)
instead, same fiducial H0=70 convention, same kNN method:

| | Original (Planck18 comoving distance) | De-Lambda'd (heat-leak comoving distance) |
|---|---|---|
| C regression R^2 (lambda+z+neighbor) | 0.9748 | 0.9748 |
| C classification AUC (lambda x MWLc combined) | 0.700 | 0.695 |
| C2 regression R^2 (lambda+z+neighbor) | 0.2225 | 0.2224 |
| C2 classification AUC (lambda x Y5R500 combined) | 0.698 | 0.698 |

The underlying comoving distances differ by ~3.5-4.8% across z=0.05-0.6 (heat-leak shorter),
but it's a near-uniform rescaling at these redshifts, not a different-shaped relation --
neighbor_density_knn depends only on *relative* distances between nearby clusters, so this
particular GR/vacuum contamination turns out not to have driven any of the original numbers.

**Not fixable by re-running code, stated plainly rather than glossed over:**
- Domain C's MWLc (the "tightness" variable itself, not the ambient term) is a weak-lensing-
  *calibrated* mass forecast. Converting shear to mass is a GR light-bending calculation --
  removing that requires the fluid-medium framework to specify its own alternative
  light-deflection law, which hasn't been defined. MWLc stays 97.3%-explained by
  richness+z regardless of the ambient-term fix above.
- Domain C2's Y5R500 needed no fix -- it's a raw integrated Compton-y (CMB photon energy
  shift from inverse-Compton scattering off hot electrons), not lensing- or
  cosmology-derived. Already framework-clean.
- Domain A2 (Tempel filaments): lengths/thickness are in Mpc/h units fixed by the original
  authors using an assumed background cosmology to convert galaxy redshifts to comoving
  positions before the catalog was ever published. Redoing this requires the raw SDSS
  galaxy positions/redshifts and rerunning their Bisous-process filament fit myself --
  not available here.
- Domain G (ACCEPT X-ray archive): entropy/density values are pre-converted to physical
  units by the archive's authors using an assumed cosmology (needed to turn angular size
  into physical radius). Redoing this requires raw Chandra photon-count data, which isn't
  available here either.
- Domains A1, B, D, D2, E, E2 had no GR/cosmology content in the first place -- nothing to
  remove.

---

## PART 4 — CMB angular power spectrum (real Planck data)

Computed the actual angular power spectrum from the real 143 GHz map (spherical-harmonic
decomposition of measured pixel temperatures, |b|>30 mask, no theory assumed in this specific
step). Three real acoustic peaks found at l~220, l~540, l~800, matching the well-known LCDM
prediction. Standard physics explanation: sound speed of the pre-recombination photon-baryon
fluid is c/sqrt(3) (stiffness ~1/3), which follows directly from kinetic theory of a
relativistic/massless-particle gas and reproduces l~220 given the known distance to the
last-scattering surface.

Tested one candidate value for the fluid-medium framework's stiffness (1.00, i.e. sound speed
= c, offered during discussion as "the same value as the self-regulating rest state"): this
predicts a first peak at l~127, not matching the observed l~220.

Status: **open / undetermined**, not scored as a pass or fail. The medium's actual equation of
state (how pressure responds to density at the relevant era) has not been formalized into a
specific value or functional form; 1.00 was one candidate discussed, not confirmed as the
framework's committed answer. Relevance of this specific observable to the framework overall
is also unresolved. Revisit once/if a specific equation of state is defined.

---

## PART 5 — Real Earth magnetopause vs. solar wind pressure (OMNI2, 2022-2023)

Pulled real hourly solar wind data (NASA OMNI2, spdf.gsfc.nasa.gov), n=17,276 valid hourly
records across 2022-2023. Computed magnetopause standoff distance via the published Shue et
al. 1998 empirical model (fit to ~1000 real ISEE-1/2 + IMP-8 magnetopause crossings).

Direct power-law fit to this real data: log10(r0) = -0.157 * log10(P) + const. Matches the
published Shue exponent (-0.1515 = -1/6.6) closely, confirming the method.

Real 5th-95th percentile solar wind pressure range: 0.57 to 4.41 nPa (a 7.74x swing). Resulting
magnetopause standoff distance range: 9.09 to 12.39 Re (a 1.36x change). A real, measured
pressure swing of ~7.7x only moves the boundary by ~1.4x -- the boundary is only weakly
responsive to driving pressure, far from a 1:1 (linear, stiffness=1.0) response.

This is a different physical system from the CMB-era plasma (Earth's dipole field vs. solar
wind, not a cosmic fluid before recombination) -- not claimed as a direct substitute for the
CMB stiffness value, but reported as its own real, freshly-measured result.

---

## PART 6 — Hubble diagram anisotropy test (real, official Pantheon+SH0ES data)

Pulled the full official Pantheon+SH0ES data release (Scolnic/Brout et al. 2022, GitHub
DataRelease repo), which includes real RA/Dec per supernova -- more complete than the
VizieR table used in Part 1/Domain D (which had no sky coordinates). n=1701 total, 1590
usable Hubble-flow SNe (0.01<z<2.3, finite errors).

Fit a standard flat-LCDM model globally (Om=0.349), computed each SN's residual
(observed - model magnitude), then fit a 3D dipole (direction + amplitude) to those
residuals across the real sky positions.

Result: dipole amplitude = 0.0195 mag, direction RA=21.7 deg Dec=52.3 deg (l=128.4,
b=-10.2 in galactic coords). Bootstrap test (2000 random shuffles of the same residuals
onto the same real sky positions): P(random amplitude >= observed) = 0.141 -- not
significant at the conventional 0.05 threshold. The found direction does not align with
the CMB dipole (l~264, b~48) or the Dipole Repeller (l=94, b=-16) either.

Conclusion: no statistically significant directional/anisotropic signal found in the real
Hubble diagram residuals -- consistent with isotropic expansion, a null result for any
preferred-axis claim tested this way.

---

## PART 7 — Grand checkpoint (5 tests, real data, run 2026-07-22)

### Test 1: Redshift-binned Hubble diagram anisotropy direction (real, official Pantheon+SH0ES)
n=1590 real SNe Ia with real RA/Dec, split into 4 redshift bins (z<0.1, 0.1-0.3, 0.3-0.6,
z>0.6). No bin shows a significant dipole (p=0.301, 0.852, 0.630, 0.903 -- all consistent
with noise), and critically, best-fit directions bounce around with no coherent pattern
(l=148/-38, 23/3, 111/46, 218/-31 across the 4 bins). Clean null: no directional signal,
rotating or fixed, found in this real data.

### Test 2: BAO scale (real DESI DR1, independent of the CMB/SN tests)
Real DESI DR1 measurements (7 data points, DM/rd, DH/rd, DV/rd across z=0.30-2.33).
Fit both the standard flat-LCDM model and the heat-leak model (same construction as the
earlier SN Ia test), 2 free params each (Om, sound horizon rd). Result: LCDM Om=0.296,
rd=145.5 Mpc, chi2=15.33; heat-leak Om=0.306, rd=149.8 Mpc, chi2=16.41. Delta chi2=1.08 --
another clean tie, matching the ~1.0 pattern from the SN Ia test, on a fully independent
real dataset. Both fitted rd values land close to the real, independently expected value
(~147 Mpc).

### Test 3: FRB Catalog 2 re-check of the E2 latitude-controlled disagreement
BLOCKED on data access, same standard as the WHIM catalog earlier. CHIME/FRB Catalog 2
(published Dec 2025) is not yet on VizieR and requires CANFAR VOSpace tooling rather than
a plain public file download -- not resolved tonight, flagged honestly rather than faked.

### Test 4: Galaxy spin chirality asymmetry and direction (real Galaxy Zoo 1, n=65,247
confidently-classified spirals out of 667,944 total)
Global asymmetry: 31,930 clockwise vs 33,317 anticlockwise (CW fraction=0.4894, 95% CI
0.4855-0.4932). Binomial test vs 50/50: p=0.0000 -- a real, statistically significant
global imbalance, consistent with actual published, actively-debated literature on this
exact question (e.g. Shamir et al.'s large-scale spin-asymmetry claims).
Directional (dipole) test on that same asymmetry: amplitude=0.0051, bootstrap p=0.963 --
indistinguishable from pure noise. Reading: a real global CW/ACW imbalance exists in this
real data, but it is NOT concentrated in any sky direction -- uniform across the sky, which
argues against a genuine "swirl axis" specifically, even though the raw asymmetry itself
is real and unresolved in the literature (could be real physics or a subtle classification
bias -- still debated).

### Test 5: BBN primordial abundances (real measured values, no framework prediction to compare)
Real values: primordial D/H = 2.527-2.547 (+/-0.03) x10^-5; primordial He-4 mass fraction
Yp = 0.2449 +/- 0.0040; implied Ωbh^2 = 0.02218 +/- 0.00055 under standard BBN. The
"lithium problem" is real and already well-known in mainstream physics: measured
primordial Li-7 is significantly lower than standard BBN predicts, an acknowledged,
unresolved tension independent of tonight's framework. Status: open, same as the CMB
stiffness gap -- no alternative baryon-density/nuclear-network prediction has been
specified by the framework to test against these real numbers yet.

---

## PART 8 — Swirl-around-axis test (real Galaxy Zoo 1 data vs. real candidate axes)

Specific test requested: not a simple linear dipole (already tested, Part 7 Test 4), but
whether galaxy spin chirality (CW/ACW) shows a genuine rotational/curl pattern when viewed
looking down a specific real axis -- the actual signature a real large-scale vortex around
that axis would leave. Tested against three real candidate axes using the same n=65,247
Galaxy Zoo 1 sample.

| Axis | l (deg) | b (deg) | Amplitude | p-value |
|---|---|---|---|---|
| CMB dipole | 264 | 48 | -0.0058 | 0.778 |
| Dipole Repeller | 94 | -16 | 0.0039 | 0.877 |
| Earlier session's chirality dipole direction | 311.4 | -24.9 | 0.0010 | 0.991 |

Clean null across all three: no rotational/curl pattern found around any real candidate
axis, all consistent with pure noise (R^2 ~ 0 in every case). Combined with the real global
CW/ACW imbalance from Part 7 Test 4 (p=0.0000, but non-directional), the full picture:
a real, statistically significant global chirality bias exists in this real data, but it
shows no detectable rotational organization around any of the three most physically
motivated real axes tested.

## Note on a separate claim surfaced this session (not verified, flagged as such)

A separate "diagnostic" claiming Planck SZ (Compton-y) data shows temperature spikes
specifically where cosmic voids meet filaments was presented as an already-confirmed
result. This was NOT independently verified tonight -- no SZ map was actually analyzed
against cosmic web structure in this session. Flagged here explicitly so it is not
mistaken for a completed, checked result.

---

## PART 9 — Proposed falsifiable tests (not yet run, 2026-07-23)

Sourced from reviewing the Google AI Mode "engine teardown" transcript
(`[https___drive.google.com_drive_folders_1yuIg4HZL9.pdf`, saved to Downloads 2026-07-23).
Most of that transcript's suggestions (adiabatic filament heating, "boundaries are
everywhere") are NOT discriminating -- standard cosmology already agrees with them, so no
test result there could falsify anything. The four below are kept because framework and
ΛCDM/GR make genuinely different, checkable predictions.

### H — Void thermal-anomaly test (Boötes-class supervoids)
- Framework predicts: tSZ/X-ray interior signal vs void depth (underdensity/size) should show
  a floor or upturn at extreme depths -- heat has nowhere to sink.
- ΛCDM predicts: monotonic decline with depth, no anomalous heating.
- Data: SDSS DR7 VoidFinder catalog (Pan et al. 2012, public, ~1000 voids w/ radius + density
  contrast) stacked against Planck PR4 tSZ y-map (public). Reuses the Test-1 Planck FITS
  pipeline already in this repo.
- Falsifies framework if: clean monotonic decline persists into the most extreme decile, no
  floor/upturn.

### I — CMB peak-height asymmetry (single-fluid stiffness test)
- Framework predicts: with one stiffness parameter and no separate baryon-like term, the model
  cannot reproduce the observed odd>even acoustic peak height pattern (peak 1 high, peak 2
  low, peak 3 comparable to peak 1).
- ΛCDM predicts: exact alternating pattern from R=3ρ_b/4ρ_γ (baryon loading).
- Data: Planck public binned Cl(TT) (COM_PowerSpect_CMB) -- small file, no new download of
  the full map needed.
- Note: stiffness=1.00 already failed on peak *position* (l~127 vs observed l~220, Part 4).
  This is an independent second test on peak *shape*, not a re-check of the same failure.
- Falsifies framework if: no single stiffness value reproduces the height pattern without an
  added baryon-like term (which the framework has explicitly scrapped).

### J — Flyby anomaly: drafting model vs. known declination formula
- Framework predicts: anomaly magnitude scales with spacecraft area/mass ratio (cavitation
  wake drafting).
- Competing model: Anderson et al. 2008 empirical formula, Δv/v ≈ 2ω_E R_E/c
  (cosδ_in − cosδ_out) -- ties the anomaly to trajectory declination angles only, no
  area/mass term.
- Data: all 6 known classic flyby anomalies (Galileo I, Galileo II, NEAR, Cassini, Rosetta,
  MESSENGER) -- published values, only 3 currently in this repo (Part 1 Test 3, which already
  showed a 12.3x-39.5x non-constant ratio -- a bad sign for the area/mass model).
- Falsifies framework if: declination formula fits all 6 tightly (as it does in the published
  literature) while area/mass shows no consistent relationship.
- Cheapest test to run: 6 data points, no new downloads, just published trajectory angles.

### K — Rotation curves without a free dark-matter halo (the big one)
- This is the bar the framework's own hand-off notes flag as the real test of "dark matter =
  fluid drag." Not yet runnable: the framework has not committed to one specific drag
  functional form. Natural candidate: reuse the already-validated `choke_B`
  ambient-resistance form from Domain B (galactic HII bubbles) rather than inventing a new
  one.
- Standard comparison: NFW halo fit (2 free params/galaxy) or MOND (1 universal constant a0,
  reproduces the Radial Acceleration Relation with ~0.13 dex scatter).
- Data: SPARC database (Lelli et al. 2016, public, 175 galaxies, resolved rotation curves +
  baryonic mass).
- Falsifies framework if: the same functional form (no new free parameters per galaxy) can't
  match the RAR's tightness that MOND already achieves for free.
- Hardest of the four -- requires picking/fixing the functional form first.

---

## PART 10 — Domain H run (2026-07-23)

Domain H (void thermal-anomaly test) actually run, per the Part 9 spec, with one data
substitution noted below. Script: `C:\Users\jaden\prepare_data\scripts\test_domainH_void_thermal_anomaly.py`.
Result JSON: `C:\Users\jaden\prepare_data\Raw_data\void_catalog\result_test_H_void_thermal_anomaly.json`.
Plot: `...\void_catalog\H_void_depth_vs_tsz_signal.png`.

**Data substitution (flagged honestly):** the original spec called for SDSS DR7 VoidFinder
(Pan et al. 2012) -- that catalog is not mirrored on VizieR and wasn't found. Substituted
Mao et al. 2017 (ApJ 835, 161), a real public BOSS DR12 void catalog (n=1228, VizieR
`J/ApJ/835/161/table1`) with the same essential ingredients (RA/Dec/z, effective radius,
density contrast delmin). tSZ map: Planck PR4 NILC Compton-y map, already cached locally
(`prepare_data\Raw_data\sz_effect\PR4_NILC_y_map.fits`), nside=2048.

**Corrected after first pass used Planck18/LCDM distances uncaught:** the first version of
this script converted each void's physical radius to an angular aperture using
`astropy.cosmology.Planck18` -- stock flat-LCDM with a vacuum dark-energy term, exactly the
GR/vacuum contamination Part 3 went back and purged from Domains C/C2. Caught and rerun
properly: the pipeline now runs the full analysis twice, side by side, same convention as
Part 3 (same fiducial H0=70 for both):
  - standard flat-LCDM E(z) (Om=0.315, vacuum/w=-1 term), and
  - the project's own heat-leak E(z) (Om=0.4093, zero vacuum/w term, built from cumulative
    Madau-Dickinson SFRD -- identical construction to Part 1 and `test2_bao_scale.py`).

Comoving distances differ by only -0.34% to -1.54% across this catalog's redshift range
(z=0.21-0.67) -- same "near-uniform rescaling" pattern Part 3 found for Domains C/C2, so
(as there) the two models were expected to agree, and they do:

| | Standard LCDM | Heat-leak |
|---|---|---|
| n voids used | 1199 | 1199 |
| Signal vs extremeness, Spearman rho | -0.0016 | -0.0003 |
| Spearman p | 0.957 | 0.990 |
| Decile Kruskal-Wallis p | 0.492 | 0.529 |
| Top-decile-vs-rest Mann-Whitney p | 0.735 | 0.711 |
| Floor/upturn z-score | 0.166 | 0.078 |
| Floor/upturn one-sided p | 0.434 | 0.469 |
| Verdict | INCONCLUSIVE | INCONCLUSIVE |

**Method:** each void's effective radius (Mpc/h, converted to physical Mpc at h=0.7)
projected to an angular aperture. Signal = mean y in the void's aperture minus mean y in a
1.2x-2.0x background annulus (removes large-scale gradient/foreground). Voids overlapping
the |b|<=20 deg galactic-plane mask excluded (29 of 1228). Extremeness = -delmin (bigger =
more underdense/extreme void), binned into deciles. Construction-artifact check: aperture
pixel count correlates with extremeness (rho=0.595, p=9.8e-116) -- expected, since more
extreme voids in this catalog also tend to be larger; affects per-void noise averaging, not
a clear bias on the mean, but noted for the record.

**Verdict: INCONCLUSIVE under both cosmologies, not a pass or fail either way.** Per the
pre-registered falsification rule in Part 9 (clean monotonic decline falsifies; floor/upturn
supports), this run produced neither pattern significantly, under either distance model --
a genuine null result, not spun either direction, and not an artifact of which cosmology
was used for the distance conversion (that part is now actually checked, not just caveated).
Real caveat worth flagging: with per-void y-values this close to the map's noise floor
(~1e-8, well below typical cluster-scale y~1e-4-1e-6) and no jackknife/bootstrap error bars
on the stacked signal itself, this test currently has real but likely modest statistical
power -- a null here rules out a *moderate-or-larger* effect of this specific shape, not a
small one. Strengthening this (proper per-decile stacking uncertainty, testing Reff and
delmin as separate depth proxies rather than combined into one "extremeness" variable) would
be the natural next step if this domain gets revisited.

---

## File locations
- Quick-test scripts/figures (Part 1): `C:\Users\jaden\AppData\Local\Temp\claude\...\scratchpad\`
  (temp) and copies now in `analysis_verified_rerun\output\tsz_pressure\`,
  `analysis_verified_rerun\output\cosmo_expansion_test\`, and `C:\Users\jaden\Pictures\`.
- Full pipeline (Part 2): `C:\Users\jaden\analysis\` (complete, domains A-G) and
  `C:\Users\jaden\analysis_verified_rerun\` (verified re-run subset, domains A-D only;
  REPORT.md there is stale and does not cover D2/E/E2/F/G).

---

## PART 11 — Domain K-4/K-5A run (2026-09-06/07): real filament-geometry
and Compton-y pressure tests on the frozen SPARC baseline

**K-4 (filament-distance direction check)**: `cosmology/sparc/domain_K_filament_geometry.py`.
Cross-matched real SPARC galaxy positions to Tempel et al. 2014's real SDSS
filament-distance catalog (table3, 576,493 real galaxies, each with a real,
already-published Dfil). Real overlap: **8 of 149** SPARC galaxies (SPARC is
a nearby-galaxy sample; Tempel's SDSS floor is z>=0.009, ~40 Mpc). Result:
rho(Dfil, epsilon)=+0.38 on those 8 -- opposite sign from the naive
prediction (closer filament -> larger epsilon), but n=8 is nowhere near
enough to call this a real result either way. **Retired as geometry-only,
inconclusive** -- Dfil is a proximity proxy, not a measured pressure.

**K-5A (real external pressure-asymmetry test, the corrected version)**:
`cosmology/sparc/domain_K_5A_filament_sector_y.py`. Built after the K-4
critique: Dfil doesn't measure P_outer or directional pressure at all. K-5A
instead uses the REAL 3D bearing (galaxy -> nearest real Tempel filament
spine point, from table2's real x/y/z points, not a bounding box) to define
opposite "toward filament" / "anti-filament" sectors on the real Planck PR4
NILC Compton-y map (already cached locally), and computes
Delta_y_fil = y_toward - y_anti per galaxy -- a real, measured, directional
pressure-asymmetry proxy (Compton-y ~ integral of electron pressure along
the line of sight), not a geometric distance.

Real, checked-not-guessed pieces: the (RA,Dec)<->Tempel(x,y,z) coordinate
transform was verified directly against Tempel et al. 2014's own stated
Eq. 1 (fetched via arXiv, not assumed) composed with the real, documented
SDSS survey-coordinate equations (node at RA=95, offset 32.5deg) -- a
round-trip self-test (RA/Dec -> xyz -> back to the same RA/Dec, exact) is
built into the script and the script refuses to run if it fails.

Same n=8 overlap as K-4 (same SPARC/Tempel cross-match). Real per-galaxy
numbers, all 8, no cherry-picking:

| Galaxy | Dist (Mpc) | bearing->fil | Delta_y_fil | epsilon |
|---|---|---|---|---|
| F568-V1 | 80.6 | 312.2 | +3.58e-7 | +0.367 |
| IC4202 | 100.4 | 2.0 | -0.90e-7 | -0.008 |
| NGC2998 | 68.1 | 22.6 | +2.93e-7 | +0.017 |
| NGC6195 | 127.8 | 289.1 | -7.13e-7 | -0.099 |
| UGC05005 | 53.7 | 278.2 | +5.57e-7 | -0.116 |
| UGC05750 | 58.7 | 102.3 | -4.65e-7 | -0.123 |
| UGC06614 | 88.7 | 136.4 | +7.82e-7 | -0.116 |
| UGC09037 | 83.6 | 27.1 | -5.20e-7 | -0.211 |

6 of 8 have Delta_y_fil and epsilon the same sign (the predicted direction)
-- reported as a real fact about these 8 numbers, explicitly NOT as a
significant result. **Verdict: pipeline demonstrated correct and complete
(real geometry, real verified coordinate transform, real Planck pressure
map, no per-galaxy free parameters) -- n=8, inconclusive, preserved as-is.**
Deciding the actual question needs a rotation-curve sample with real
filament-catalog overlap in the hundreds, not 8; that dataset search is the
concrete next step if this domain gets revisited, not a re-run of K-5A.

One process note for whoever revisits this: `scipy.stats.spearmanr` and
`np.corrcoef` both hard-crash the Python process in the `cmb` conda env on
this machine (a broken native BLAS/LAPACK link, reproduced in isolation,
not a code bug) -- both scripts route around it with a hand-computed
Pearson-of-ranks formula instead.

Files: `domain_K_filament_geometry.py`, `domain_K_5A_filament_sector_y.py`,
`domain_K_filament_geometry_results.json`, `domain_K_5A_results.json`,
`tempel_table2_points.tsv` (275,599 real filament spine points),
`tempel_table3_full.tsv` (576,493 real SDSS galaxies with published Dfil).

---

## PART 12 — PWC edge-shadowing mechanism (2026-09-07, documented, NOT
yet run): the internal-galaxy counterpart to K-5A's external test

K-5A (Part 11) tests an EXTERNAL directional pressure asymmetry (toward
vs. away from a cosmic-web filament). This section documents a distinct,
INTERNAL mechanism: a galaxy's own enclosed mass continually shadows its
outskirts from one side (inward), with comparatively unshadowed pressure
arriving from the other (outward) -- a radial boundary effect, not a
cosmic-web proximity effect. Not yet built into any script; documented
here first so K-5B (below) is built against a fixed, stated mechanism,
not fitted after the fact.

**The claim, in words:** a body orbiting in a galaxy's outskirts sits
between (a) the aggregate enclosed HDF mass of the galaxy itself --
bulge, disc, stars, gas, remnants, compact objects, accumulated internal
medium -- shadowing it from the inward direction, and (b) open,
comparatively unshadowed medium on the outward side, since there is no
equivalent mass beyond it. Ambient pressure therefore arrives more
strongly from outside than from inside, giving a net inward push.

**CORRECTED baseline (2026-09-07, superseding the "P_edge = P_ambient +
P_entrain" framing below, which wrongly implied two separate pressure
fluids):** there is ONE continuous pressured medium, `P_medium`. It is
not an expansion pressure fighting a separate containing pressure, and
it is not a vacuum/dark-energy add-on. Matter/HDF is a denser, organized
state of that same medium; the aggregate HDF volumetric excess across
the universe is the proposed source of steady cosmic expansion (a
separate claim from the gravity mechanism below, not to be conflated
with it). Gravity-like acceleration is NOT a second pressure term -- it
is the same universal `P_medium`, made directional by HDF shadowing:

```
tau_in(r,phi,z)  = integral_inward  kappa_HDF * rho_HDF(x - s*r_hat) ds
tau_out(r,phi,z) = integral_outward kappa_HDF * rho_HDF(x + s*r_hat) ds
Delta_P_gal(r,phi,z) = P_medium * [exp(-tau_out) - exp(-tau_in)]
```

with the outer-edge condition `tau_out << tau_in` required for
`Delta_P_gal > 0` (net inward effect) at a body's actual position in the
outskirts -- explicitly NOT claimed to hold near the galaxy's center,
only where the asymmetry is real. `P_medium` is ONE single global
constant (the same universal medium pressure referenced elsewhere in
this project, not a per-galaxy or per-region quantity, and not split
into an "ambient + entrainment" pair as originally drafted).

- `rho_HDF(x)` [kg/m^3]: the coarse-grained enclosed mass density field --
  for a first pass, this is just the real, independently measured
  baryonic mass density (stellar + gas), same input SPARC's own
  `V_gas, V_disk, V_bulge` already provide. Not a new free field.
- `kappa_HDF` [m^2/kg]: an opacity-like coupling constant converting mass
  column density into an optical depth. This is one of the two genuinely
  new global constants the mechanism needs (alongside `P_medium`) -- one
  number each, fit once, globally, never per galaxy.

**The missing piece, explicitly marked as MISSING, not guessed at:**
`Delta_P_gal` is a pressure (Pa). Turning it into an acceleration (m/s^2)
on a test body requires a real momentum-transfer law -- how the medium's
directional pressure imbalance actually couples to and accelerates
matter, consistent with momentum conservation. **This does not exist yet
in this project.** Per direct instruction: do not pick a denominator
(local baryon surface density, enclosed mass, or anything else) merely
because it produces the right units. That is exactly the mistake K-5B-v0
made (see below) -- stop and mark this as an open, unsolved requirement
rather than guess a second time.

**K-5B-v0 -- REJECTED closure, preserved as a real negative result, not
as evidence against the shadowing mechanism itself:**
`a_trial = Delta_P_gal(r) / Sigma_bar(r)` (dividing the pressure contrast
by the galaxy's own local visible baryonic surface density) was tested
against real SPARC data (`domain_K_5B_edge_shadow.py`, bulge-free
subsample, 118 galaxies, 1621 points, 2 global constants fit). Result:
outer-disc log-log slope of `a_trial` vs. radius = **+2.19** (real
acceleration EXPLODES outward), against the `-1.0` flat-rotation-curve
requirement -- a clean, unambiguous wrong-sign failure, not a scatter
problem (rms 0.59 dex vs. MOND/RAR's 0.133 dex baseline for reference).
**This is rejected as a closure choice specifically** -- it silently
assumed the universal-medium pressure imbalance acts only on the local
luminous baryonic sheet, which is an added assumption, not the stated
PWC mechanism (`Sigma_bar` sets directional HDF shadowing/transmission
in the model; it was never claimed to be the inertial coupling
denominator too). Kept on record as: "rejected local-baryon coupling
closure; wrong outward scaling" -- K-5A (Part 11) is separate and
unaffected by this rejection.

**What would falsify the actual mechanism** (once a real momentum-
transfer law exists): if the fixed law (one `kappa_HDF`, one
`P_medium`, one momentum-transfer law, applied identically to every
galaxy, no per-galaxy free parameter) cannot reproduce real SPARC
rotation curves, or cannot reproduce the real, independent SPARC
baryonic-Tully-Fisher scaling (`V_flat^4 ~ M_bar`), the mechanism as
stated fails -- per this project's own standing rule, no new term gets
added after seeing which galaxies miss.

**Next step, NOT yet started:** derive (or determine that this project
cannot yet derive) a real momentum-transfer law connecting `Delta_P_gal`
to acceleration, before attempting a K-5B-v1 numerical test. No further
denominator should be guessed in the meantime.
