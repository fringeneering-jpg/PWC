# Phase Wave Cosmology (PWC)

*Fringeneering — Jaden Allison*

**Space is a medium with a minute mass and a propagation limit, not a zero.** Newton, GR and MOND work because they have been measuring this medium all along; PWC keeps their mathematics and adds the medium back in. Matter is medium tied into a 720° toroidal knot (m = L/c²). The resting medium is paired EM waves held apart by heat. Light is an unpaired wave. Black holes are shells at a maximum density, not singularities. The extra gravity in galaxies is the medium's tension.

**Start here → [`PWC/PWC.md`](PWC/PWC.md)** (the framework) · [`PWC/DERIVATION_BRIEF.md`](PWC/DERIVATION_BRIEF.md) (one-page summary for researchers)

---

## Headline result: galaxy rotation, blind

One formula, two global constants, **zero per galaxy**, carried unchanged from SPARC to galaxies it had never seen:

```
g_obs = g_bar + √(a₀·g_bar) · [1 + s · shared · (1 − locked)]
a₀ = 6.68×10⁻¹¹ m/s²,  s = 0.226
```

Medium loaded from both sides (between inner and outer mass) gives extra pull; medium pulled one way gives less; medium locked at maximum (bulges) gives none.

| Data | Galaxies | PWC | Base √(a₀g) | McGaugh RAR |
|---|---|---|---|---|
| SPARC, held-out, 10 splits | 149 | 0.1309 | 0.1326 | 0.1283 |
| LITTLE THINGS (not in SPARC) | 16 | **0.3374** | 0.3417 | 0.3464 |
| GHASP (not in SPARC) | 81 | **0.2655** | 0.2661 | 0.2657 |
| **PROBES** (not in SPARC/GHASP) | **1,342** | **0.2931** | 0.2986 | 0.2982 |
| PROBES + ALFALFA HI gas | 331 | **0.2452** | 0.2490 | 0.2511 |

Galaxy-balanced scatter in log g (lower is better). On PROBES, PWC beats McGaugh by 1.7% (bootstrap 95%: 1.3–2.1%), holds at stellar M/L 0.4–0.6, and the lead **grows** when gas is added. Dark-matter halos need 2–3 fitted numbers per galaxy. Every prediction was frozen and timestamped before its run: [`sparc/predictions/`](sparc/predictions/).

**Status: survived, not proven.** a₀ and s are measured on SPARC; deriving them from the medium is the top open target.

## What is derived

- **Hawking temperature from the sonic choke** — the horizon is where infalling medium reaches c; exact Hawking formula, no free parameter, 18 orders of magnitude in mass (§8).
- **Black-hole shells (GW150914)** — ρ_max = 1.304×10¹⁵ kg/m³, holding yield 3.23×10¹¹ N/kg; the "radiated" 3 M☉ is released medium. The frozen merger rule predicts the final masses of 89 GWTC mergers to a mean −0.97% (§0, §8).
- **√(a₀·g_bar) two ways** — from the holding threshold plus 2D spreading, and independently from the compounding cascade (§0, §10).
- **Shared tension** — loaded / one-sided / locked medium (§10).
- **The medium cycle** — knotted, paired, unpaired: matter breaks into medium at ρ_max, most waves pair, the unpaired remainder leaves as light and heat and reorders on the way (redshift) (§5).
- **Light and gravitational waves** — transverse neighbour-reaction waves driven by the EM yank, c₀ = 1/√(μ₀ε₀); compression is the slower longitudinal mode (§4). Equal speeds, as GW170817 measured.

## What is open

Ranked targets with allowed inputs and pass/fail rules: [`PWC/DERIVATION_BRIEF.md`](PWC/DERIVATION_BRIEF.md). The top three: the equation of state between the ordered (P = ε/3) and locked (P = ε) branches; a₀ from the holding threshold with nothing fitted; ε₀ and μ₀ from the medium's pairing. Full list: [`PWC/OPEN_WORK.md`](PWC/OPEN_WORK.md).

## Method

Write the equation first. Freeze the prediction with a timestamp. Then look at the data. Keep failures visible — they live in [`PWC/TESTED_AND_DROPPED.md`](PWC/TESTED_AND_DROPPED.md) and in the outcome notes under each frozen prediction.

## Repository map

| Path | What |
|---|---|
| `PWC/PWC.md` | The framework |
| `PWC/DERIVATION_BRIEF.md` | Derived results, tests, ranked missing derivations, research prompts |
| `PWC/OPEN_WORK.md` · `PWC/CLOSURE_SHEET.md` | Open items · derivation order for the five closing values |
| `PWC/TESTED_AND_DROPPED.md` | Everything tried and dropped |
| `sparc/predictions/` | Frozen predictions + outcomes for every galaxy test |
| `sparc/jaden_*.py`, `sparc/*_build.py` | Test and data-build scripts (SPARC, LITTLE THINGS, GHASP, PROBES, ALFALFA) |
| `sparc/littlethings/`, `sparc/ghasp/`, `sparc/probes/` | Catalogue data and built accelerations (raw PROBES: Zenodo 10456320) |
| `PWC/*.hdf5`, `PWC/cat_*.json` | GWOSC strain and catalogue data for the merger work |
| `rbh1/` | RBH-1 runaway black hole: JWST NIRSpec reduction and wake analysis |
| `PWC_Supersonic_Wake/` | OpenFOAM supersonic wake case (below) |
| `OLD/` | Archive of earlier versions |

Reproduce the biggest test: `cd sparc && python probes_build.py && python jaden_probes_blind.py` (needs the PROBES files from Zenodo record 10456320 in `D:/probes`, or edit the path).

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
