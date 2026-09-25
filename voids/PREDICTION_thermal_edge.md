# Prediction frozen before touching Planck data — Thermal Edge Test (Jaden, 2026-09-25)

**PWC reasoning (Jaden):** void expansion is the endothermic melting of tied volume-debt, which demands heat, so melting proceeds fastest toward the greatest available heat.
**Prediction:** for asymmetric voids, the boundary at the ends of the true major axis (the stretched ends) shows a higher Compton-y (thermal pressure) than the boundary at the ends of the minor axis.
**Standard-physics caveat (acknowledged in advance):** ΛCDM tidal fields also stretch voids toward massive structures, which contain hot gas, so a positive result is expected to some degree in ΛCDM as well. This test alone does not discriminate; it establishes whether the signal exists and its size.

## Method (fixed before looking)
- **Voids:** VAST VoidFinder, SDSS DR7, Planck 2018 cosmology (Douglass et al. 2023, Zenodo 11043278 v1.3.1): `*_comoving_maximal.txt` + `*_comoving_holes.txt`. Keep edge == 0 only. (Switched from the V2/VIDE table because its catalogued ellipsoids are degenerate — two identical long axes in every void — and its galaxy list lacks coordinates.)
- **True shape:** Monte Carlo sample of points uniformly inside the union of each void's holes (spheres); centroid + covariance → principal axes. Major = largest eigenvalue, minor = smallest. Asymmetric = √(λmax/λmin) ≥ 1.3.
- **Boundary points:** from the centroid along ±major and ±minor, at the union's extent along that direction + 5 Mpc/h (just into the wall). Converted to RA/Dec with the catalogue's own cartesian convention (checked against its listed ra/dec).
- **y measurement:** Planck PR2 MILCA Compton-y map (Nside 2048). Mean y in a disc whose radius is 5 Mpc/h at the point's distance (minimum 0.5°). Discs >20% outside the usable map (masked/Galactic |b| < 20°) are dropped.
- **Statistic:** per void Δ = mean(y at the two major ends) − mean(y at the two minor ends).
- **PASS:** median Δ > 0 AND fraction(Δ > 0) > 50% with one-sided sign-test p < 0.05.
- **FAIL:** anything else. Also reported: bootstrap 95% range of mean Δ; same statistic with major replaced by the intermediate axis (control).

## Outcome — INCONCLUSIVE (exploratory hunch; no signal at Planck's sensitivity either way)
805 edge-free voids measured, 281 asymmetric (√(λmax/λmin) ≥ 1.3; median ratio 1.26). Cartesian convention verified.
Major ends − minor ends: median −1.2×10⁻⁸, mean +6.3×10⁻⁹, bootstrap 95% [−4.0, +5.5]×10⁻⁸; positive 139/281 (49%); sign-test p = 0.59.
Control (intermediate − minor): 143/281 (51%), p = 0.41.
No preference for hotter gas at the stretched ends. Sensitivity: differences below ~5×10⁻⁸ in y are not resolvable with single-void Planck discs — comparable to the size of stacked void SZ signals, so a small real effect (PWC's or ΛCDM's tidal one) cannot be excluded.
