# PWC Session 2026-10-08 — Complete Ledger
## Every figure, its derivation, and the tests still to be worked

Status: consolidated by the working agent from this session's verified scripts; every
number below was computed and checked in `scratch/` (committed copies under `PWC/`).
Committed 2026-10-08 on Jaden's "in the git". Where a number is his ruling or a locked
datum, it is marked.

---

## 1. The identity chain — M = L/c₀² as the medium's pressure

| Identity | Value | Status |
|---|---|---|
| c₀² = 1/(μ₀ε₀) = P_max/ρ_max = L | 8.988×10¹⁶ (all four) | LOCKED (PWC.md §4 + EOS) |
| Tying heat = PV work of the collapse | m_p·c₀² = P_max·(m_p/ρ_max) = 1.5033×10⁻¹⁰ J, exact | verified |
| Tying heat ÷ knot's reach volume = resting pressure | m_p·c₀²/(3m_p/ρ₀) = ρ₀c₀²/3 = 2.6185×10⁻¹⁰ Pa = P₀, exact | verified (mirror of T7 §3) |
| Direction: pressure ↔ tension | P_net = rigidity − cohesion; P > 0 ties (heat OUT), P < 0 unties (heat IN) | LOCKED (pull-side ruling) |

## 2. The demand function — m = ΔP·ΔV/c₀² (the §8 line 464 missing link)

- m = ΔP·ΔV/c₀², ΔV = PRE-collapse volume; converted fraction f = ΔP/(ρ_local·c₀²);
  two regimes: m/V = min(ρ_mist, ΔP/c₀²).
- Full conversion at the sealed two-wall slam (Δv = c₀): ΔP = ρ_max·c₀² = P_max exactly —
  the rule is identical to the keystone's fold construction P*·dv = c₀².
- The c₀² in the rule is the PLATEAU latent heat only — resolves the heat-ramp report's
  "failing datum L = c₀² as total inventory" (option 1).
- Cross-checks: T2 creation law reproduced to 4/√3 = 2.309 (geometric prefactor; the
  spike's 0.577 c₀²/kg is 1.78% of the 32.371 c₀² ladder — the slam is the trigger, H₀
  finances); water 542× deep in the vapor-limited arm (the two-regime structure, anchored
  at both ends); proton R_ball = 8.011 R_p.

## 3. RBH-1 (RCP 28) — all figures

| Quantity | Value | Note |
|---|---|---|
| Wake mist density (published 0.7 kpc) | 0.086–0.112 ρ₀ | "rarefied, vapor/mist-like" ✓ |
| Wake mist density (HST 0.61 kpc, 7.5σ) | 0.13–0.15 ρ₀ | first independent measurement |
| Expelled heat rate, escape fraction | 7.76×10³⁷ W; 2.45×10⁻⁴ | matches §8's 10⁻⁴–10⁻⁵ |
| Flash light-equivalent over 73 Myr | 244.8 M☉ | reproduces §8's ~245 exactly |
| Supply cap (path (a) LOCKED) | 1,232–15,500 M☉ vs 10⁶–10⁷ M☉ stars (65–810×) | zero-flow zone |
| Dilution prediction vs frozen −0.10 dex bar | Δ(O/H) = −5×10⁻⁶ to −6.7×10⁻⁴ dex | the bar is unreachable; a pass refutes the cap |
| Closure-rate gap | 2,100–2,300 yr naive vs 73 Myr = 3.2×10⁴× | sealed 2c₀ closure is per-pocket, not cavity |

## 4. The volume-to-mass friction scale

- v_cap² = 2Y·(V/M) for HELD bodies: 0.9998 c₀ (ρ = 1.32×10¹⁰) → 0.363 c₀ (10¹¹) →
  0.0363 c₀ (10¹³) → **954 km/s (ρ_max, cap ignition)** → 72 km/s (ρ_core).
- One V/M = 1/ρ_max, two fates: held → 954 (RCP 28's wall), free → c₀ (the wave).
- The timeline: 3 M☉ at ρ_max = 103 km → 1,403 km at τ = 4.68 ms (2,528× decompressed) →
  52,200 km at 0.17 s (the chat's dropped ambient floor 10⁷) = Jaden's 0.2 s pulse width.

## 5. The stagnation scale (the size/density that causes stagnation)

- Self-hold condition: g_surf ≥ a_max → **ρ·R ≥ 3a_max/(4πG) = 1.155×10²¹ kg/m²**.
- At ρ_max: **R* = 886 km, M* = 1,910 M☉** — the session log's "pure ρ_max sphere" limit,
  now the stagnation boundary. The 3 M☉ dump sits 0.116× below (free); RBH-1 ~546× above
  (stagnant). Core-hold threshold: R ≥ 5.02 km (0.06 M☉) — every NS/BH core qualifies.
- Sheet vs ball: a_max/(2πG) and 3a_max/(4πG) differ by exactly 3/2 (geometry).
- Falsification: sub-column bow shock kills FREE; ≥886-km Max-P at c₀ kills STAGNANT.

## 6. The five-gate medium→matter transition (with kill conditions)

1. BLOCKAGE: ρ > m_p/λ³ = 7.475×10¹⁶ (λ = 2.82 fm = 3.3 R_p). Killed by tying without
   obstruction (Earth-heat gate guards).
2. FOLD: ρ_max/2 → ρ_max at P* = 1.172×10³² Pa; squeeze 31.371 c₀²/kg, self-financed by
   H ≥ 32.371 c₀²/kg. Killed by sub-fold tying.
3. PLATEAU WORK: m·c₀² per kg (P*·dv = c₀² exact). Killed by tying heat ≠ m·c₀².
4. QUANTIZATION: m·R·c₀ = 4ℏ (proton 4.001ℏ); S = 1 = the heat-void state. Killed by a
   stable knot violating it (neutron 2.5% off, isospin-recorded; Δ open).
5. HOLD: topology, not gravity (knot column 8.79 kg/m² vs 1.155×10²¹). Killed by a knot
   untying with no heat draw.
- The wave never reaches gate 2; the Max-P shell runs 1–2; the RSMBH wake runs 1–4 → H.

## 7. Keystone integration (Jaden's 5:5x AM files, integrated and corrected)

- Caloric law: H(ρ) = H₀ − (c₀²/3)ln(ρ/ρ₀); total drop 32.371 c₀²; H₀ ≥ 32.371 c₀².
- Tension-heat law: dY/d(ΔH) = −3Y/c₀² → Y = sρc₀²/3 on the gas branch (s = 1/19);
  Y_cav = 1.378×10⁻¹¹ Pa; plateau ×7 (locked 6.9972) → Y_coh = 0.061379 P_locked;
  γ = 0.2867 P_locked (unreachable max at 4.671 ρ_max); v_cav = c₀√(2s/3) = 0.1873 c₀.
- Corrections owned: my v_cav(ρ₀) = c₀ anchor (28.5× high) withdrawn; "Y/ρ falls 10⁵"
  wrong (constant); T7 split 1.75% tension / 98.25% heat (not 50/50).

## 8. The rulings (verbatim in `PWC/session_logs/2026-10-08/`)

- RBH-1 supply path (a) LOCKED · chirality (EM(+) / EM(−)) · no-snap (energy field, not
  fluid; high/low pressure sides, nothing tears) · baseline T = 0, the 2.7 K = matter's
  exhaust · **the Great Separation** (heat expelled, NOT gone; medium is the baseline) ·
  pull-side sealed (the "negative pressure" = the heat's draw; matter = the suction) ·
  coupling law (grip = f(heat expelled); vacuum ε₀/μ₀ = resting values; the heat-function
  is flat at rest → row 23's "why the links are harmonic" ANSWERED).
- Consequences: u_h/P₀ ≥ 96 (spacer heat ≫ pressure); T7's untying split 1.75/98.25.

## 9. The charge — Williamson's quicycle (Jaden's directive)

- q' = √(3ε₀hc/8π³) = 1.4585×10⁻¹⁹ C = 0.9103e — "the wavelengths cancel: charge is
  topological." Only ε₀, h, c enter.
- The 9% gap = the linear (resting) grip; Lai 2026's vacuum saturation (Born-Infeld at the
  Schwinger limit) = PWC's heat-dependent coupling law. α⁻¹: 150 (linear) → 135.9
  (saturated) → 137.036 (observed, the topology gap).
- Charge = winding ±1 → proton/electron equal-opposite charge; {e, α} collapses to ε₀
  alone; chirality = winding = ± charge.
- **OPEN: g = 16π³α/3 = 1.2067** — my two attempts failed honestly (uniform-core 163.0 vs
  their 135.9; frozen-grip √k goes the wrong way). The volumetric route (the heat-expelled
  volume, f = g^(1/3) = 1.0646 vs the stretch 1.0526, +1.14%) is named, not closed.

## 10. The surface-area holding law (thin skin)

- Inverse square = fixed tension diluted over 4πr² (the geometric origin).
- Thin skin: t = Σ_k/ρ_max = 650 km (the 20-hole run: 70 → ~640 km; edge/core 4.69 → 1.01).
  The r⁻⁴ thick envelope (35.6 M☉ tail) is DEAD; M_med = Σ·4πR_c².
- Σ_k = 8.48233×10²⁰ vs the sheet law 2πGΣ = a_max → 7.702×10²⁰ (+10.1%);
  near-misses (11/10)·sheet = (11/15)·ball at +0.117%, no mechanism — reported, not
  claimed. Skin 650 km < stagnation 886 km (sub-stagnation, core-held).

## 11. The fight and the neck (merger mechanics)

- Push-out: overlap at core-edge contact = 2.72×10¹⁵ m³ = **1.78 M☉** of Max-P forced out
  of the way (the shells cannot interpenetrate).
- Budget: full potential 6.90 = displacement 1.78 + capacity dump 3.05 (k-rule S) +
  2.07 spin/ringdown.
- Stack-up: after edge contact the contact point is the HIGHEST pull — g₁+g₂ = 5.25×10¹²
  = 16.3× the yield (vs 10.3× at the merged surface) — and the neck's Max-P layer extends
  **124 km past contact, thicker than the merged shell's 113 km**: the thickest part.

## 12. The survival triad, the comet, and the adiabatic phase loop

- Three modes: MICRO (knot topology + speed), MACRO (collective well — a 10-pc cloud's own
  pull is 1.44×10⁻¹¹ < a₀: clouds hold via the host well/Jeans), and dense-at-speed
  (Max-P cap). The comet is the failed in-between.
- Comet heat budget (honest bounds): observed 10² kg/s sublimation costs 2.6×10⁸ W of the
  Sun's 10¹⁰ W ✓; full c₀²-untying of the same flux = 9×10¹⁸ W = 10⁹× the Sun;
  ambient-medium flux supports 8.5×10⁻⁹ kg/s; T7 rate 2.4×10⁻⁵ kg/s → the tail is ~100%
  SHALLOW untying (sublimation = the low rung of the continuous ladder).
- The phase loop (comet tail = thermal web at two scales): untie (draws c₀²/kg) → the
  parcel climbs the adiabat H(ρ) = H₀ − (c₀²/3)ln(ρ/ρ₀) → re-pairs at H₀. The tail = the
  loop's footprint: 1,398 km/s of untying → 0.41 AU in a day → 1.28 AU in 30 days. The
  icy wake = the per-kg deficit (19% of H₀ mid-loop); the suction and the heat are ONE
  co-attraction. The gas is 10⁶× volumetrically heavier than the medium — the traffic jam —
  cycling (rise/expand/freeze/fall/heat) "until it is."

## 13. The Great Separation (H₀ and the 2.7 K bath)

- H₀ ≥ 32.371 c₀² = 2.909×10¹⁸ J/kg (the floor); **one ruling away from pinned**: "everything
  was tied once at the Great Separation" → H₀ = 32.371 c₀² exactly (an initially fully-tied
  inventory deposits exactly the floor; today's 5% can refill only 5.3% — the spacer heat
  is ancient exhaust).
- The 2.7 K bath = the radiated sample: 5.3×10⁻⁵ (freeze inventory) or 1.01×10⁻³ (today's
  matter) escape fraction, straddling RBH-1's measured 2.45×10⁻⁴. Baseline T = 0 needs no
  primordial bath.

## 14. Data tests run

- Pulsar bow census (BR14): the flux-fold needs 10⁴³–10⁴⁵ m/s — never fires in the ISM;
  5/6 bow pulsars sit BELOW 954 (the ridge doesn't separate neutron bodies — the
  "ρ_max crust vs ρ_n" cell stands); dense-ISM→slower direction present in n = 6,
  selection-dominated (not evidence).
- Recoil candidates: CID-42 1428–2470 km/s, 3C 186 ~2100 km/s — above-cap (slammed regime),
  no wakes reported — consistent, not evidence; "slowest wake bounds Y" stays open.
- 43 GeV line: Profumo 2609.16425 recalibrates to 2.7σ conditional; broad/uniform morphology
  fits the hot-gas-tracking prediction better than NFW; fluctuation most likely; VLAST
  decisive.
- HST RCP 28: far-half FWHM 1.36 kpc, deconvolved radius 0.61 kpc at 7.5σ vs published 0.7
  — the supply-cap input survives.

---

## TESTS STILL TO BE WORKED (my list, in priority order)

1. **g = 1.2067 (the charge eigenfactor)** — the holy grail. The volumetric route: the
   heat-expelled volume of the knot from the caloric ladder's fold drop, not a uniform
   stiffening. Needs either the exact double-loop eigenmode (the 4-quantum SU(2)
   quantization) or the full radial-profile saturation integral with PWC's EOS.
2. **The Σ +10.1%** — a mechanism for (11/10)·sheet or the acceptance that k = 0.868899's
   last 10% is catalogue systematics.
3. **H₀** — Jaden's one-word ruling (Great Separation inventory) pins it to 32.371 c₀².
4. **The τ = 4.68 ms release profile** — the decompression law connecting the 3 M☉ dump to
   the settling time (103 km → 1403 km = 13.6×; the profile is the open decompression law).
5. **Pulsar "crust vs bare ρ_n" cell** — needs the frontal-area law (the repo's escape is
   "minimal drag") stated as an equation, then re-score the census.
6. **A second Y anchor** — "slowest wake bounds Y": recoil candidates are above-cap; an
   at-cap object (or a bow-shock census at higher S/N) is needed.
7. **VLAST** — the 43 GeV line, decisive (~1–2 yr).
8. **Cosmology predictions** — BAO 147 Mpc, CMB z ≈ 1100, the growth law, DESI DR3 — the
   sealed targets, untested.
9. **Housekeeping sweep** — PWC.md still says "the great freezing"; DERIVATIONS.md's Gaps
   table still lists items this session closed (demand function, envelope shape); the
   registry rows are committed but the master docs need reconciliation.
10. **Smaller open cells** — the muon and Δ-baryons (proton-derivation extensions); the
    EHT shadow (undefined until the light-trapping mechanism is stated); m_w unpinned
    (m_p/3–m_p); the bow sheath profile ρ_bow(r) (passage-chart open cell); the 2.7 K
    bath-anisotropy test (local tying-region excesses above the bath).

*Every figure above has a verification script in the repo (`PWC/*.py`) and a derivation
document in `PWC/derivations/`; every ruling is verbatim in `PWC/session_logs/2026-10-08/`.*
