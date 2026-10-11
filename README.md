# Phase Wave Cosmology (PWC)

*Fringeneering — Jaden Allison*

**Space is a medium with a minute mass and a propagation limit, not a zero.** Newton, GR and MOND work because they have been measuring this medium all along; PWC keeps their mathematics and adds the medium back in. Matter is medium tied into a 720° toroidal knot (m = L/c₀²). The resting medium is paired EM waves held apart by heat. Light is an unpaired wave. Black holes are shells at a maximum density, not singularities. The extra gravity in galaxies is the medium's tension. It's always been a solid — it was just how far apart it was.

## Run the whole framework — one command

```
python PWC/run_full_framework.py
```

Fires every active verification — macro, micro, cosmic web, rulings — and prints one scoreboard (22 sections, statuses honest). Per-script output: `PWC/run_full_framework_last.log`.

**Start here →** [`paper/PWC_v1_draft.md`](paper/PWC_v1_draft.md) (manuscript v1.9) · [`PWC/PWC.md`](PWC/PWC.md) (the framework) · [`PWC/DERIVATION_BRIEF.md`](PWC/DERIVATION_BRIEF.md) (one-page summary) · [`DERIVATIONS.md`](DERIVATIONS.md) (**registry: every derivation, where it lives, what reproduces it**) · [`PWC/session_logs/`](PWC/session_logs/) (every session, Jaden's rulings verbatim)

---

# The framework by scale

## MACRO — black holes, mergers, lensing, rotation

- **Black-hole pipeline** (one-command rebuild): the core (ρ_core = 2.3×10¹⁷) + ρ_max shell (1.304×10¹⁵, 954 km/s cap) + the reach edge — [`PWC/black_hole_pipeline.py`](PWC/black_hole_pipeline.py).
- **Merger mass drop**: the smaller of (a) the cores' motion energy at contact and (b) the lost storage capacity — **−0.97% mean on 89 GWTC events; 0.81% out-of-sample on 104 GWTC-5**. [`PWC/merger_energy_balance.py`](PWC/merger_energy_balance.py)
- **The fight and the neck** (2026-10-08): the shells cannot interpenetrate — the cores plow **1.78 M☉** of overlap medium out of the way, then the contact point becomes the highest pull (**16.3× the yield**) and the neck stacks 124 km — thicker than the merged shell. [`PWC/fight_overlap.py`](PWC/fight_overlap.py), [`PWC/neck_pull.py`](PWC/neck_pull.py)
- **Light bending = pull + push**: 4GM/(b·c₀²) = **1.7512″** at the solar limb, γ = 1 exact. [`PWC/light_bending_push_pull.py`](PWC/light_bending_push_pull.py)
- **Hawking from the static-medium stall**: T = ℏc₀³/(8πGMk_B) exact, no flowing medium. [`PWC/static_medium_check.py`](PWC/static_medium_check.py)
- **Thin skin** (surface-area law): M_med = Σ_k·4πR_c², skin 650 km thick, the r⁻⁴ envelope dead. [`PWC/surface_area_law.py`](PWC/surface_area_law.py)
- **Galaxy rotation, blind**: one formula, two global constants, zero per galaxy — SPARC 0.1309, PROBES 0.2931 (beats McGaugh by 1.7%), predictions frozen before every run: [`sparc/predictions/`](sparc/predictions/).

## MICRO — the knot, the charge, the quarks

- **Proton from topology**: m_p = 4ℏ/(R_p·c₀) and R_p⁴ = 3ℏ/(512π·ρ_max·c₀), both ≤ 0.12% from {ρ_max, c₀, ℏ} + the 720° double-cover. [`PWC/predictions/proton_derivation_20260930.md`](PWC/predictions/proton_derivation_20260930.md)
- **The stretch unlocked** (2026-10-09): the trapped heat's pressure balances the 720° pinch → **H_trapped = s·c₀²** — the sealed stretch s = 1/19 IS the universal retained-heat fraction (5.26% kept, 94.74% expelled, re-absorbed on untying). The mass ratio: m_p/m_e = 4λ̄_C/R_p = 1835.79 (−0.02%), the ratio of the two quantizations. [`PWC/knot_equilibrium_eos.py`](PWC/knot_equilibrium_eos.py)
- **The footprint**: the trapped heat inflates the zitter horizon against the phase-lock → **r_t = (π + 3s)λ̄_C = 3.2995 vs the target 3.3023 (−0.085%)** — the target bracketed; the residual IS the matter (Jaden's ruling: the gap is the displacement, not a defect). [`PWC/footprint_dynamics.py`](PWC/footprint_dynamics.py), [`PWC/residual_is_matter.py`](PWC/residual_is_matter.py)
- **Charge as winding**: q′ = √(3ε₀hc/8π³) = 0.9103e — the wavelengths cancel, charge is topological; the electron = an edge dislocation in the birefringent lattice (Burgers = charge, the double circuit = 720°). g = 16π³α/3 = 1.2067 remains the one open value; every dead route is on the record with kill-numbers. [`PWC/quicycle_charge_map.py`](PWC/quicycle_charge_map.py), [`PWC/dislocation_core_geometry.py`](PWC/dislocation_core_geometry.py)
- **Quarks = directional untying vectors** (2026-10-09): the dichromal fold — +2/3 = the compression crest across two axes, −1/3 = the rarefaction anchoring the third; the 2:1 is dimensional. Three folds + the neutral 4th strand = the proton's +1. "Colorless" = sum-to-ambient, never zero. [`PWC/dichromal_knot_check.py`](PWC/dichromal_knot_check.py)
- **The five gates** (medium→matter): blockage, fold, plateau work, quantization (m·R·c₀ = 4ℏ), topology hold. [`PWC/transition_condition.py`](PWC/transition_condition.py)

## WEB — stagnation, RBH-1, the comet, the thermal web

- **Stagnation scale**: self-hold needs ρ·R ≥ 3a_max/(4πG) = 1.155×10²¹ kg/m² → **R\* = 886 km, M\* = 1,910 M☉** at ρ_max. [`PWC/stagnation_scale.py`](PWC/stagnation_scale.py)
- **Demand function**: m = ΔP·ΔV/c₀² (PWC.md §8 line 464's missing link, now derived). [`PWC/derivations/demand_function_pressure_conversion.md`](PWC/derivations/demand_function_pressure_conversion.md)
- **RBH-1 (RCP 28)**: the 62-kpc star trail — mist density 0.086–0.112 ρ₀, escape fraction 2.45×10⁻⁴, supply cap 65–810× short, dilution prediction Δ(O/H) = −5×10⁻⁶ to −6.7×10⁻⁴ dex. [`PWC/rbh1_demand_test.py`](PWC/rbh1_demand_test.py), [`PWC/rbh1_supply_cap.py`](PWC/rbh1_supply_cap.py)
- **Survival triad + the comet**: macro (collective well), micro (knot topology), speed (the cap) — and the comet as the failed in-between: its tail is ~100% shallow untying (the c₀² channel bounded to 10⁻¹⁰–10⁻¹² by the heat budget). [`PWC/comet_survival_map.py`](PWC/comet_survival_map.py)
- **The adiabatic phase loop**: untie → climb the adiabat H(ρ) = H₀ − (c₀²/3)ln(ρ/ρ₀) → re-pair; the tail = the loop's footprint (1.28 AU in 30 days at 10² kg/s); the steam clouds of the thermal web are the same loop at cosmic scale. [`PWC/phase_loop_comet_web.py`](PWC/phase_loop_comet_web.py)
- **The void reach law**: R_void = √(G·M_walls/a₀) — a 10¹⁵ M☉ cluster → 1.45 Mpc; the 150 Mpc BAO void needs 10¹⁹ M☉ of walls: the reach law lands on the BAO scale itself.

## RULINGS — the sealed decisions (verbatim in `PWC/session_logs/`)

- **The Great Separation** (the heat expelled, not gone; the medium is the baseline — "the great freezing" retired).
- **The heat-capacity datum**: 1 kg of medium reads 2.7 K → c_H = H₀/2.7 K = 1.0775×10¹⁸ J/(kg·K); H₀ = 32.371 c₀² is the rest state at absolute zero; 2.7 K is the real zero, ours is arbitrary.
- **The coupling law**: the grip between chiralities = f(heat expelled), flat at rest — ε₀/μ₀ are the resting values.
- **Pull-side sealed**: the "negative pressure" is the heat's draw; matter is the suction.
- **Nothing snaps**: an energy field, not a fluid; high/low pressure sides, nothing tears.
- **Chirality**: EM(+) and EM(−) are opposite chiralities.
- **No zeros**: "colorless" is sum-to-ambient; every balance is a match between non-zero terms.

---

# The locked numbers

| Constant | Value | Origin |
|---|---|---|
| c₀² = 1/(μ₀ε₀) = P_max/ρ_max | 8.988×10¹⁶ | the medium's stiffness/inertia = the latent heat |
| ρ₀ | 8.74×10⁻²⁷ kg/m³ | T2 bow-wave equilibrium, 0.5% |
| ρ_max | 1.304×10¹⁵ kg/m³ | the tied state (P_max = 1.172×10³² Pa) |
| ρ_core | 2.3×10¹⁷ kg/m³ | the stacked core |
| a_max (yield) | 3.23×10¹¹ N/kg | the ρ_max layer's holding edge |
| s = 1/19 | 5.26% | **the retained-heat fraction** (2026-10-09: H_trapped = s·c₀²) |
| k = 0.868899 | storage capacity | calibrated on GW150914, 89-event tested |
| H₀ | 32.371 c₀² | the Great Separation inventory |
| α = 1/137.036 | the fold | r_e/λ̄_C — the structure derived to −0.085%, the value open |

---

# What is open

Ranked targets with pass/fail rules: [`PWC/DERIVATION_BRIEF.md`](PWC/DERIVATION_BRIEF.md), [`PWC/OPEN_WORK.md`](PWC/OPEN_WORK.md), and the live list in [`PWC/session_logs/2026-10-08/2026-10-08_FULL_LEDGER.md`](PWC/session_logs/2026-10-08/2026-10-08_FULL_LEDGER.md). The one-line version: **g = 1.2067** (the charge eigenfactor — the 0.085% profile term, the only step between the framework and a fully derived α); the τ = 4.68 ms decompression profile; the yield-anchor's origin text; the PWC shadow (undefined until light-trapping is stated); the path-growth/(1+z) mechanics; a second Y anchor ("slowest wake bounds Y"); VLAST on the 43 GeV line; the BAO 147 Mpc steam-loop stall radius.

## Method

Write the equation first. Freeze the prediction with a timestamp. Then look at the data. Keep failures visible — they're archived in [`archive/tested_and_dropped.md`](archive/tested_and_dropped.md) and in the outcome notes under each frozen prediction. Numerical near-misses without a mechanism are reported, never claimed.

## Repository map

| Path | What |
|---|---|
| **`paper/PWC_v1_draft.md`** · **`paper/PWC_v1_draft.tex`** | **Manuscript v1.9 (arXiv-bound), markdown and revtex4-2 LaTeX** |
| `PWC/PWC.md` | The framework |
| `DERIVATIONS.md` | Derivation registry — every result, script, status, gap. Check before re-deriving |
| `PWC/DERIVATION_BRIEF.md` | One-page summary: derived results, tests, ranked missing derivations |
| `PWC/OPEN_WORK.md` · `PWC/CLOSURE_SHEET.md` | Open items · derivation order for the closing values |
| **`PWC/run_full_framework.py`** | **The front door: one command, every verification, one scoreboard** |
| `PWC/black_hole_pipeline.py` | One-command rebuild of the black-hole chain |
| `PWC/session_logs/2026-10-08/` · `2026-10-09/` | The October sessions: every ruling verbatim, the full ledger |
| `PWC/derivations/` | One derivation document per result |
| `PWC/predictions/proton_derivation_20260930.md` | Proton mass and radius closed-form derivation |
| `PWC/knot_audit/` | The two-phase EOS, T1 (a_hold), T7 discrete unlocking |
| `rbh1/` | RBH-1 runaway black hole: JWST NIRSpec reduction, wake analysis, metallicity test |
| `sparc/` | Galaxy-rotation catalogue data, builds, frozen predictions (SPARC, LITTLE THINGS, GHASP, PROBES, ALFALFA) |
| `archive/tested_and_dropped.md` | Everything tried and dropped (auditable) |
| `OLD/` | Archive of earlier versions |

Reproduce the biggest external test: `cd sparc && python probes_build.py && python jaden_probes_blind.py` (needs the PROBES files from Zenodo record 10456320 in `D:/probes`, or edit the path).

## In gratitude

To **James Clerk Maxwell**, for listening to the intuition guys, and to **Albert Einstein**, for going back to correct what he'd started when nobody listened — *"If a body gives off the energy L in the form of radiation, its mass diminishes by L/c²."* ("Does the Inertia of a Body Depend Upon Its Energy Content?", 1905). See the top of [`PWC/PWC.md`](PWC/PWC.md).

---

<details>
<summary><b>Fluid dynamics: OpenFOAM supersonic wake simulation (<code>PWC_Supersonic_Wake/</code>)</b></summary>

OpenFOAM case files modelling supersonic flow: velocity (U), pressure (p), temperature (T) and density (ρ) across transient time steps.

- `system/` — `blockMeshDict`, `controlDict`, `fvSchemes`, `fvSolution`, `topoSetDict`, `changeDictionaryDict`, `setFieldsDict`
- `0/` and time directories (`0.501437` … `4.99922797784`) — U, p, T, rho, `uniform/time`, `functionObjects/`
- `constant/` — `thermophysicalProperties`, `turbulenceProperties`, `polyMesh/` (incl. `obstacleCells`)

```bash
blockMesh        # generate mesh
# run solver, or inspect the pre-calculated time directories; log: log.pwc_case_c
```

</details>
