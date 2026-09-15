# Supercloud Stage 1 audit (2026-09-15)

Pure data-transcription and constraint-scoping stage for a future HDF/LDF Galactic
morphology test. **This is not a PWC validation and not a fit.** No pressure-regulation
claim is tested here. Categories kept strictly separate per the agreed evidence-tier
framework.

## Empirical inputs (real, sourced, independently re-verified this session)

- **Mass and length** for all 7 superclouds: Kormann et al. 2026 (`K26`), *A&A*,
  arXiv:2507.14883v3, Table C.2 (p.11-12). Fetched and read directly this session,
  not taken on any secondhand characterization.
- **Undulation fit parameters** (amplitude, wavelength, phase, offset, damping) for
  4 of 7 superclouds (Malpolon, Natrix, Radcliffe Wave, Vela Ridge Cloud): K26 Table
  C.3 (p.12). Vela Ridge Cloud fit with a simple (non-damped) sinusoid; the other
  three with a damped sinusoid, per the authors' own stated methodology. Split,
  Sagittarius Spur Extension, and Anguis Cloud have no undulation fit reported.
- **Fragmentation/superclump spacing** for 6 of 7 superclouds: Kormann et al. 2026
  (follow-up, `KF26`), arXiv:2608.21028, Table E.1 (p.8). Anguis Cloud explicitly
  excluded by the authors themselves — only one superclump was recovered, so a
  spacing could not be measured. For Natrix Cloud, the L1335-inclusive range was
  used, matching the authors' own stated recommendation ("We adopt the L1335
  inclusive range as the representative range for the Natrix Cloud"), not a choice
  made in this analysis.

## Transparent derived values (arithmetic only, no fitting)

- `mu_i = M_i / L_i` (linear mass, all 7 clouds)
- `A_i / lambda_i` (amplitude-to-wavelength ratio, 4 clouds with a fit)
- `frag_full_midpoint_i` (midpoint of the reported full spacing range, 6 clouds)
- `frag_full_midpoint_i / lambda_i` (4 clouds with both a fit and a spacing range:
  Malpolon, Natrix, Radcliffe Wave, Vela Ridge Cloud)

## PWC premises invoked (not measured by any cited paper)

- One mass-bearing substrate; HDF and LDF as density/packing phases of the same substance.
- HDF as the denser, tension/pressure-bearing phase; LDF as the lower-density phase
  that light and the EM spectrum propagate through.
- Gravitational waves as HDF disturbances, sharing a speed ceiling with LDF light via
  shared underlying fundamental units, not via being the same mode.
- Matter/Sintot as a locked/organized state of the same substrate.
- **Working hypothesis under test, not established**: the gas/dust/molecular-cloud/
  young-star patterns in these papers are baryonic tracers of HDF-LDF phase
  morphology — HDF squeeze/tension confining or organizing LDF, baryons responding
  to or revealing that state.

## Conventional competing explanations (live alternatives, not straw men)

Per K26/KF26/B26's own discussion sections: ordinary interstellar-medium pressure
balance (thermal, turbulent, magnetic), Kelvin-Helmholtz-type instability from
disk-halo differential rotation, Parker instability of the Galactic magnetic field,
external perturbation (dwarf satellite, dark-matter clump, globular cluster passage),
and multi-supernova/stellar-wind feedback (Local Bubble, North Polar Spur). None of
these require an HDF/LDF medium to explain the observed structures.

## Unavailable / explicitly blocked quantities

- `rho_vol,i` (volume density per cloud): **null**. K26 states volume densities vary
  by only ~10% while linear mass varies by a factor of ~4 (the paper's own aggregate
  claim), but per-cloud values are shown only in Fig. 6 (a figure), not a text table.
  Not digitized, not estimated, not approximated here.
- `A_perp,i` (cross-sectional area per cloud): **null**. K26 explicitly states that
  width/height estimates for most clouds are unreliable ("leads to a large
  overestimation" — their own words, Sect. 3.2.3), so no cross-section value is
  usable even as a rough proxy.
- `P_ext,i` (external/ambient pressure per cloud): **null**. Not supplied by any
  cited source at the per-cloud level.
- No VizieR/CDS machine-readable catalog exists for K26 as of this check
  (confirmed directly via vizier.cds.unistra.fr search, 2026-09-15) — consistent
  with the paper's recent (Feb 2026) publication date, not a search failure.
- No per-cloud mass or length uncertainty is reported in K26 Table C.2 (point
  estimates from the HOP+PCA segmentation pipeline only) — stated here explicitly,
  not silently omitted, and not invented.

## The key blocked test (explicitly not run)

**Test**: is `rho_vol,i` approximately constant while `mu_i` varies by a factor of
~4, as K26's own aggregate abstract claim states?

**Status**: `BLOCKED — no reliable per-cloud rho_vol or cross-section dataset exists
in any source checked this session.` The abstract-level claim is an author-level
aggregate statement, not something independently regressed per cloud here. See
`supercloud_stage2_requirements.md` for what would be needed to actually run this.

## Descriptive comparison actually run (n=4, no significance claimed)

Rank by linear mass, with `A/lambda` and `frag/lambda` alongside (real numbers,
`build_supercloud_stage1.py` output):

| Supercloud | mu (Msun/pc) | A/lambda | frag/lambda |
|---|---:|---:|---:|
| Natrix Cloud | 568.5 | 0.0403 | 0.2086 |
| Vela Ridge Cloud | 676.9 | 0.0185 | 0.0809 |
| Malpolon Cloud | 1022.4 | 0.0281 | 0.1820 |
| Radcliffe Wave | 1450.2 | 0.0503 | 0.1742 |

**Honest read**: at `n=4`, there is no visible monotonic pattern. Linear mass rises
monotonically across this ranking by construction, but neither `A/lambda` nor
`frag/lambda` tracks it in the same order. This is reported as an absent/ambiguous
pattern at this sample size, not as a null result for the underlying physical
question — 4 points cannot rule anything in or out. Worth pre-registering as a
specific, sharper test if/when the full local supercloud catalog (or a larger
external one) becomes available with more wave-fit and fragmentation measurements.

## No-claim zone (explicit)

- This audit does **not** claim HDF/LDF phase mechanics is supported by these data.
- This audit does **not** claim HDF/LDF phase mechanics is falsified by these data.
- The pressure-regulation claim in K26's abstract is **not** independently verified
  here — it remains an author-level claim pending the blocked per-cloud data.
- The n=4 descriptive comparison above is not a significance test and should not be
  read as one.

## Provenance

Built by `build_supercloud_stage1.py`, 2026-09-15. All source PDFs fetched and read
directly this session (arXiv:2507.14883v3, arXiv:2608.21028, arXiv:2402.12596,
arXiv:2608.10884v2 also read for cross-context). Outputs: `supercloud_stage1_raw.csv`,
`supercloud_stage1_derived.csv`, this file, and `supercloud_stage2_requirements.md`.
