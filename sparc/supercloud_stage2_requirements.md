# Supercloud Stage 2 requirements (not yet started)

Stage 2 is the actual pressure-regulation test:

```
rho_vol(mu),   A_perp(mu),   P_ext(mu)
```

i.e., does per-cloud volume density stay approximately constant while linear mass
(`mu = M/L`) varies by a factor of several, as Kormann et al. 2026's own aggregate
abstract claim states ("linear masses vary by about a factor of 4, volume densities
only vary by about 10%")?

## Exactly what is needed, and why each item is currently missing

1. **Per-cloud volume density, `rho_vol,i`, as numbers, not a figure.**
   K26's Fig. 6 (bottom panel, "Average density of the superclouds") shows this
   visually but the underlying values are not in any text table in the paper as
   checked this session (Table C.1/C.2/C.3, Appendix B/C/D/E all read directly —
   none contain a density column). Needed: either (a) the authors' own machine-
   readable data (contact, or a future VizieR/CDS submission — none exists as of
   this check, confirmed directly via vizier.cds.unistra.fr), or (b) a transparently
   documented digitization of Fig. 6 with stated pixel-to-value calibration and
   honest uncertainty bounds — not a casual eyeball estimate.

2. **Per-cloud cross-sectional area or an equivalent (width, height, or a
   volume estimate), `A_perp,i`.**
   K26 explicitly states their own width/height estimates are unreliable for most
   clouds due to irregular cloud shape ("leads to a large overestimation," Sect.
   3.2.3). This is not just missing data — the authors themselves distrust their
   own geometric estimate for this quantity. Using it anyway, even with a caveat,
   would reintroduce exactly the kind of untrustworthy number this project rejects
   elsewhere. A real Stage 2 needs either a better geometric reconstruction (not
   attempted by K26) or an independent volume estimate from a different method
   entirely (e.g. a dedicated 3D dust-map segmentation with density-weighted shape
   fitting, not PCA bounding-box extent).

3. **Per-cloud external/ambient pressure, `P_ext,i`.**
   Not supplied by K26, KF26, or B26 at the per-cloud level. Would need real
   ISM pressure tracers (e.g. thermal pressure from HI/CO temperature-density
   products, turbulent pressure from velocity dispersion, magnetic pressure from
   Zeeman/polarization data) matched spatially to each supercloud's location —
   a genuinely separate data-gathering effort, not derivable from anything already
   fetched this session.

4. **Formal per-cloud uncertainties on mass and length**, not reported by K26 at
   all (Table C.2 gives point estimates only). Any Stage 2 regression needs real
   error bars to weight the fit honestly; without them, any fit is unweighted and
   that limitation must stay explicit in the results, not silently assumed away.

## What would make Stage 2 legitimately runnable

Any ONE of the following, not invented or approximated:
- The K26 authors release Fig. 6's underlying data (direct request, or a future
  paper/erratum/VizieR submission).
- A follow-up paper (like KF26 was for fragmentation) that specifically tabulates
  per-cloud density and geometry with stated uncertainties.
- An independent re-derivation from the same underlying E24 dust map (Edenhofer et
  al. 2024c) using a density/volume estimator the original authors trust, run and
  documented transparently (not attempted here — would itself be a substantial new
  analysis, not a quick addition).

## What Stage 2 would test, once unblocked

```
H0 (null): rho_vol,i is uncorrelated with mu_i (no pressure regulation signature)
H1 (PWC-compatible, not PWC-confirming): rho_vol,i stays within a narrow range
    while mu_i varies substantially -- consistent with, but not proof of, an
    external confining pressure (HDF-mediated or ordinary ISM) setting cloud size.
```

Even a clean H1 result would only be "compatible with" HDF/LDF regulation, per the
same evidentiary standard held throughout this project — ordinary ISM pressure
balance is a live, un-falsified alternative explanation and must be checked against
real pressure tracers (item 3 above) before any HDF-specific claim could be made.

## Status

**Not started.** Logged as an open, specifically-scoped, data-blocked item — not a
failed test, a test that cannot yet be run honestly with data available in this
project.
