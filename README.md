# Phase Wave Cosmology (PWC)

*Fringeneering — Jaden Allison*

**Space is a medium with a minute mass and a propagation limit, not a zero.** Newton, GR and MOND work because they have been measuring this medium all along; PWC keeps their mathematics and adds the medium back in. Matter is medium tied into a 720° toroidal knot (m = L/c²). The resting medium is paired EM waves held apart by heat. Light is an unpaired wave. Black holes are shells at a maximum density, not singularities. The extra gravity in galaxies is the medium's tension.

**Start here → [`paper/PWC_v1_draft.md`](paper/PWC_v1_draft.md)** (manuscript, v1.9) · [`PWC/PWC.md`](PWC/PWC.md) (the framework) · [`PWC/DERIVATION_BRIEF.md`](PWC/DERIVATION_BRIEF.md) (one-page summary for researchers)

---

## Headline result: MOND scale and Hubble rate from one mechanism, product to 0.02%

The framework predicts galactic acceleration and cosmic expansion via two different mechanisms sharing the same medium. Their product is a specific dimensioned invariant that resolves the 40-year-old "MOND-Hubble coincidence" (a₀ ≈ c·H₀/2π) as a mechanistic result.

| Quantity | Framework | Observed | Ratio |
|---|---|---|---|
| a_hold(ρ₀) | 6.61×10⁻¹¹ m/s² | SPARC/PROBES a₀ = 6.68×10⁻¹¹ | **0.990** |
| H₀_wall | 73.8 km/s/Mpc | SH0ES 73.04 ± 1.04 | **1.010** |
| **a_hold × H₀** | **4.878×10⁻⁹** | **4.879×10⁻⁹** | **0.9998** |

Both predictions from four fundamental scales (ρ₀, ρ_max, c₀, R_proton), no fitted parameters. Two independent 1% matches with the ~1% offsets in opposite directions cancelling to a **0.02% product invariant**.

Derivations: [`PWC/knot_audit/eos_latent_heat.md`](PWC/knot_audit/eos_latent_heat.md) (a_hold via T1) · [`PWC/knot_audit/t7_discrete_unlocking.md`](PWC/knot_audit/t7_discrete_unlocking.md) (H₀ via T7 discrete unlocking + product invariant)

---

## Headline result: proton mass and radius from ρ_max + c₀ + ℏ + 720° topology, ≤ 0.12%

The Williamson–van der Mark 720° double-cover topology of the electron, extended to the proton, yields two closed-form identities from framework fundamentals:

| Quantity | Derivation | Framework | Observed | Ratio |
|---|---|---|---|---|
| **Proton mass m_p** | 4ℏ/(R_p·c₀) from 720° topology (factor 4 = SU(2) real dim) | 1.6723×10⁻²⁷ kg | 1.6726×10⁻²⁷ (CODATA) | **0.9998** |
| **Proton radius R_p** | [3ℏ/(512π·ρ_max·c₀)]^(1/4) closed form | 0.8422×10⁻¹⁵ m | 0.8414×10⁻¹⁵ (Antognini) | **1.0010** |
| **m_p closed form** | [(131072π/3)·ρ_max·ℏ³/c₀³]^(1/4) | 1.6707×10⁻²⁷ kg | 1.6726×10⁻²⁷ (CODATA) | **0.9988** |

Neither R_p nor m_p is input — both fall out of {ρ_max, c₀, ℏ} + 720° topology. Factor 4 = real dimension of SU(2) (quaternion basis {1, i, j, k}); factor 8 = wavelength quanta in the full 720° double-cover path (2 per direction × 4 directions).

Derivation and reproducibility: [`PWC/predictions/proton_derivation_20260930.md`](PWC/predictions/proton_derivation_20260930.md)

---

## Headline result: T2 CLOSED — ρ₀ from bow-wave dynamic equilibrium, 0.5%

The untied medium's rest density ρ₀ is derived from steady-state balance between matter creation (bow-wave cavitation-wake collapse — the mechanism operating in RBH-1's 62-kpc trail) and matter decay (proton-scale Γ_untie). Both prefactor quantities are framework-native (η = 1/4 is T1's Ω_eff geometric factor; ⟨v⟩ = c₀ is the locked-phase sound speed):

$$\rho_0 = \frac{8\,a_0\,\rho_{\max}\,R_p}{3\,\eta\,c_0\,\langle v\rangle} = 8.70 \times 10^{-27}\text{ kg/m}^3$$

Observed vacuum density: 8.74×10⁻²⁷ kg/m³. **Match: 0.5%** (same precision as a_hold and H₀). Stable ODE attractor confirmed. The density hierarchy ρ_max/ρ₀ = 1.49×10⁴¹ is now a derived geometric consequence, equal to R_H/R_p (Hubble radius / proton radius).

Reproducibility: [`PWC/t2_equilibrium.py`](PWC/t2_equilibrium.py) · [`PWC/heat_spacer_free_energy.py`](PWC/heat_spacer_free_energy.py) (540/540 sign-structure validation across five families).

---

## Headline result: RBH-1 supermassive black hole wake, zero fit

The 62-kpc trail of new stars behind RBH-1 (van Dokkum 2023, 2×10⁷ M☉ SMBH at 950 km/s) tests PWC's a_hold holding-reach mechanism at supermassive scales:

| Quantity | Derivation | Framework | Observed | Verdict |
|---|---|---|---|---|
| Holding reach r_t | √(GM/a₀) | 192 pc (trail width ≈ 384 pc) | Thin trail along 62 kpc | Consistent |
| Swept-gas mass | Gas inventory inside r_t along trail | 1.2×10⁶ M☉ | 10⁶–10⁷ M☉ observed new stars | Match |
| Standard-GR reach | GM/v² (Newtonian focusing) | 0.19 pc | 2000× short of observed width | GR fails |

Discriminating creation test (sealed 2026-09-29, awaiting cleaner JWST data): [`rbh1/PREDICTION_metallicity.md`](rbh1/PREDICTION_metallicity.md)

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

**Status: survived, not proven.** The a₀ scale IS now derived from the medium via T1 (a_hold(ρ₀) = 6.61×10⁻¹¹ m/s² vs SPARC-measured 6.68×10⁻¹¹, 1% match). The shared-tension coefficient s = 0.226 remains a measured constant; deriving it from the medium is a current open target.

## What is derived

- **Proton mass and radius from 720° topology** — closed-form identities m_p = 4ℏ/(R_p·c₀) and R_p⁴ = 3ℏ/(512π·ρ_max·c₀), both matching observation to ≤ 0.12% from {ρ_max, c₀, ℏ} + SU(2) topological structure.
- **ρ₀ (T2 CLOSED)** — bow-wave dynamic equilibrium with framework-native η = 1/4 and ⟨v⟩ = c₀, predicting 8.70×10⁻²⁷ kg/m³ vs observed 8.74×10⁻²⁷ (0.5%).
- **a_hold(ρ₀) and H₀ product invariant** — a_hold = (c₀/√3)·√(G·ρ₀/4) via T1 photon-gas flux geometry (1%); H₀ = ρ₀·c₀/(ρ_max·R_p) via T7 discrete proton-scale untying (1%); their product 4.878×10⁻⁹ matches observation to 0.02%.
- **Hawking temperature from the sonic choke** — the horizon is where infalling medium reaches c; exact Hawking formula, no free parameter, 18 orders of magnitude in mass (§8).
- **Black-hole shells (GW150914)** — ρ_max = 1.304×10¹⁵ kg/m³, holding yield 3.23×10¹¹ N/kg; the "radiated" 3 M☉ is released medium. The frozen merger rule predicts the final masses of 89 GWTC mergers to a mean −0.97% (§0, §8).
- **GWTC-4 light-BH mass deficit pattern** — 26.26% median deficit for M_f < 25 M☉, 0.00% for M_f > 45 M☉, matches framework prediction to 0.04% on the 84-event catalog. GR's No-Hair theorem forbids the pattern.
- **RBH-1 wake** — r_t = √(GM/a₀) = 192 pc holding reach and 1.2×10⁶ M☉ swept-gas mass match the observed 62-kpc trail and 10⁶–10⁷ M☉ new stars with zero fit; standard GR reach is 2000× short.
- **Bullet Cluster** — inherited from MOND-family via Zhang et al. 2026 (arXiv:2606.19454) IGIMF baryonic-budget resolution.
- **√(a₀·g_bar) two ways** — from the holding threshold plus 2D spreading, and independently from the compounding cascade (§0, §10).
- **Shared tension** — loaded / one-sided / locked medium (§10).
- **The medium cycle** — knotted, paired, unpaired: matter breaks into medium at ρ_max, most waves pair, the unpaired remainder leaves as light and heat and reorders on the way (redshift) (§5).
- **Light and gravitational waves** — transverse neighbour-reaction waves driven by the EM yank, c₀ = 1/√(μ₀ε₀); compression is the slower longitudinal mode (§4). Equal speeds, as GW170817 measured.

## What is open

Ranked targets with allowed inputs and pass/fail rules: [`PWC/DERIVATION_BRIEF.md`](PWC/DERIVATION_BRIEF.md). Currently open: full cosmic baryon-fraction integration for tightening the G derivation (currently 17% high via Friedmann inversion); exact continuous perturbation equation governing the light-BH IMR mass deficit transition; extension of the shared-tension formula to the group and cluster mass regime (per McGaugh et al. 2026); ε₀ and μ₀ from the medium's pairing. Full list: [`PWC/OPEN_WORK.md`](PWC/OPEN_WORK.md).

## Method

Write the equation first. Freeze the prediction with a timestamp. Then look at the data. Keep failures visible — they're archived in [`archive/tested_and_dropped.md`](archive/tested_and_dropped.md) and in the outcome notes under each frozen prediction.

## Repository map

| Path | What |
|---|---|
| **`paper/PWC_v1_draft.md`** · **`paper/PWC_v1_draft.tex`** | **Manuscript v1.9 (arXiv-bound), markdown and revtex4-2 LaTeX** |
| `paper/killshot2_verification.md` | GWTC-4 light-BH mass deficit independent verification |
| `PWC/PWC.md` | The framework |
| `PWC/DERIVATION_BRIEF.md` | Derived results, tests, ranked missing derivations, research prompts |
| `PWC/OPEN_WORK.md` · `PWC/CLOSURE_SHEET.md` | Open items · derivation order for the five closing values |
| `PWC/knot_audit/eos_latent_heat.md` · `PWC/knot_audit/t7_discrete_unlocking.md` | Two-phase EOS + T1 (a_hold) · T7 discrete unlocking + H₀ + product invariant |
| `PWC/predictions/proton_derivation_20260930.md` | Proton mass and radius closed-form derivation |
| `PWC/t2_equilibrium.py` · `PWC/heat_spacer_free_energy.py` | T2 bow-wave equilibrium reproduction · two-phase-EOS sign-structure scan |
| `PWC/gwtc4_ringdown_mass.csv` | 84-event GWTC-4 IMR mass-deficit dataset |
| `archive/tested_and_dropped.md` | Everything tried and dropped (auditable) |
| `sparc/predictions/` | Frozen predictions + outcomes for every galaxy test |
| `sparc/jaden_*.py`, `sparc/*_build.py` | Test and data-build scripts (SPARC, LITTLE THINGS, GHASP, PROBES, ALFALFA) |
| `sparc/littlethings/`, `sparc/ghasp/`, `sparc/probes/` | Catalogue data and built accelerations (raw PROBES: Zenodo 10456320) |
| `PWC/*.hdf5`, `PWC/cat_*.json` | GWOSC strain and catalogue data for the merger work |
| `rbh1/` | RBH-1 runaway black hole: JWST NIRSpec reduction, wake analysis, metallicity dilution test |
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
