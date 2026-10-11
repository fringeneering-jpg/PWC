# Phase Wave Cosmology — Zenodo Upload

**Phase Wave Cosmology: The Complete Theory** — Jaden Allison, Fringe Engineering, 2026-10-12.

One medium, one yield, one formula, one ledger. Space is a continuous mass-bearing
electromagnetic medium; matter is the medium tied into 720° toroidal knots
(m = L/c₀², L = the light energy, Einstein 1905); black holes are shells at the
density ceiling terminating at a complete stop — not a singularity. Every constant
is derived or declared with its test record; the thermodynamic ledger closes at
1.000; the kinematic ladder admits zero violations; the coupling is
g = 20^(1/16) = 1.205909 (vs 16π³α/3 = 1.206740).

## Contents

- `PWC_COMPLETE_THEORY.tex` — the full submission-ready theory (compile with
  pdflatex; the precompiled PDF is `PWC_COMPLETE_THEORY.pdf` if attached).
- `scripts/` — the complete verification suite. **Run everything with one
  command:**
  ```
  python scripts/run_full_framework.py
  ```
  from inside `scripts/` (the runner resolves the scripts relative to its own
  folder). The scoreboard prints every verification — macro, micro, cosmic web,
  rulings — with honest statuses.

## Reproducing the headline numbers

| Result | Script |
|---|---|
| The zero-parameter galaxy suite (PROBES, derived a₀) | `scripts/probes_derived_a0.py` (needs the PROBES data; see the repo) |
| The universal speed ladder C(ρ) = min(c₀, √(2Y_bow/ρ)) | `scripts/universal_ladder_scaling.py` |
| The coupling g = 20^(1/16) | `scripts/sixteen_origin.py`, `scripts/g_from_fuel.py` |
| The s-closure (the mist's ram) | `scripts/s_mist_closure.py` |
| The knot equilibrium (H_trapped = s·c₀²) | `scripts/knot_equilibrium_eos.py` |
| The merger mass drop (min(E,S)) | `scripts/merger_energy_balance.py` |
| The Navier–Stokes regularization | `scripts/navier_stokes_answer.py` |
| The anomaly census (seven checks) | `scripts/gzk_uhcer_check.py`, `pwc_glitch_stall_check.py`, `frb_snap_check.py`, `oumuamua_gradient_check.py`, `thermostat_tension_check.py`, `pwc_bootes_birefringence.py`, `jwst_early_galaxy_check.py` |

## Methodology

Write the equation first. Freeze the prediction with a timestamp. Then look at
the data. Keep failures visible. Numerical near-misses without a mechanism are
reported, never claimed. The full derivation history — including every dead end
with its kill-numbers — is in the repository:
https://github.com/fringeneering-jpg/PWC

## Cite

J. Allison, *Phase Wave Cosmology: The Complete Theory*, Zenodo (2026).
DOI: 10.5281/zenodo.23304826 — https://doi.org/10.5281/zenodo.23304826
