# RBH-1 re-reduction pipeline (JWST GO-3149, NIRSpec IFU G140M/F100LP)

Run inside WSL Ubuntu (the JWST pipeline does not build on Windows). Working data lives on `D:\rbh1_reduction` (not in git).

1. `setup_env.sh` — installs uv + Python 3.12 venv at `~/rbh1/.venv` with `jwst` 3.0.0 and `astroquery`.
2. `fetch_rates.py`, `fetch_nrs1.py` — download all `_rate.fits` exposures from MAST (science + imprint; NRS1 science needed a second query).
3. `reduce.py` — v1: Spec2 with imprint subtraction, NSClean (`clean_flicker_noise`), pixel replacement; Spec3 outlier detection + drizzled mosaic cube. NRS1 only (NRS2 holds no spectrum for this setup).
4. `reduce_bkg.py` — v2: as v1 plus pixel-level background subtraction, using the other pointing's 4 exposures as background (pointings sit on opposite sides of the wake, ~1" apart).

Why re-reduce: the archive Level-3 cubes skipped background subtraction and NSClean, and showed no emission lines.

Analysis (Windows Python, in `rbh1/`): `extract_wake.py` (per-bin line fits), `wake_profile.py` (along-wake table, blind against `PREDICTIONS_FROZEN.md`).
