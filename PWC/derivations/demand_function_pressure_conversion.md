# The pressure-to-phase-conversion demand function  m = ΔP·ΔV/c₀²

Status: **committed 2026-10-08 ("in the git"), with Jaden's blanket test OK and his three
rulings folded in (path (a), chirality, no-snap/energy-field — §3c, §5, §7).** All numbers
are arithmetic on Jaden's sealed numbers, labeled as such. Corrections from his keystone
files (TENSION_HEAT_LAW / COHESION_CHANNEL / HEAT_RAMP reports) are in §7. Reproduction
scripts: `PWC/rbh1_demand_test.py`, `PWC/wake_closure_rates.py`, `PWC/rbh1_supply_cap.py`,
`PWC/t2_crosscheck.py`, `PWC/baseline_cold_formal.py`, `PWC/literal_branch.py`,
`PWC/stretch_side_decision.py`, `PWC/rulings_arithmetic.py`, `PWC/reconcile_heat_ramp.py`,
`PWC/verify_demand_draft.py`, `PWC/round7_checks.py`, `PWC/volume_mass_friction.py`.

## 0. The sealed pieces it builds on (quotes)

- `PWC.md` §8 line 464: "what's still needed is the demand function that converts that
  pressure into how much of the medium crosses the phase boundary."
- `PWC.md` §8 line 454: the cavitation zone is "under genuine *negative pressure*", bounded by
  "two walls at ρ_max", and "each wall closes on the gap's center at c₀" (gap shrinks at 2c₀).
- `OPEN_WORK.md` line 96: "water-hammer pressure ΔP = ρ_max·c·Δv".
- `PWC.md` §8 line 462: the rejected heat is the flash; L = m·c₀² solved for L.
- `knot_audit/eos_latent_heat.md` §2: L = c₀² across the transition; locked P_k = ρc₀².
- PROVENANCE "EOS correction": ΔP(δ) = K₁δ + …, equilibrium ΔP(ρ₀) = 0, K₁ = ρ₀c_s0².

## 1. Proposed conversion rule

    m = ΔP · ΔV / c₀²,   with  ΔP = P_local − P_eq(ρ_local)   (excess over equilibrium)

where ΔV is the **pre-collapse (initial)** volume of the material that converts. ΔP is the
excess over equilibrium — at rest ΔP = 0 (PROVENANCE "EOS correction": ΔP(ρ₀) = 0, K₁ = ρ₀c_s0²).

Justification: the collapse delivers work W = ΔP·ΔV into the zone; the phase change consumes
latent heat m·c₀²; at the phase boundary the work is what pays for it, so m·c₀² = ΔP·ΔV.
Dimensionally unique, no fitted coefficient — §8 line 464 already forbids an efficiency factor.

Equivalent form: the converted fraction of the pre-collapse material is

    f = m / (ρ_local·ΔV) = ΔP / (ρ_local·c₀²)

i.e. the pressure excess measured in units of the medium's own stiffness-per-density.
"The zero is the pressure of the medium" — c₀² is the denominator that turns a pressure
excess into a mass fraction.

**Two regimes** (both follow from f):

- **Work-limited (ΔP/(ρ_local·c₀²) < 1):** only the fraction f converts. Convertible mass per
  unit initial volume = ΔP/c₀². For the Joukowsky spike ΔP = ρ_max·c₀·Δv this is
  **ρ_conv = ρ_max·Δv/c₀** — the maximum mist density a slam at Δv converts fully
  (4.15×10¹² kg/m³ at the 954 km/s bow-wave speed). Full conversion of material at density
  ρ_mist requires Δv ≥ c₀·ρ_mist/ρ_max.
- **Mist-limited (ΔP/(ρ_local·c₀²) ≥ 1):** everything in the swept volume converts,
  m = ρ_mist·ΔV — the demand rule then supplies only the threshold, and the mass follows from
  mass conservation.

## 2. Limit checks (arithmetic, checked 2026-10-08)

(a) **Rest:** ΔP = 0 → f = 0. No spontaneous tying in quiet medium. Matches the framework:
     matter forms only at slams / formation sites, never in the resting medium.

(b) **Two-wall slam at the sealed speeds:** Δv = c₀ (each wall closes on the gap center at
     c₀, §8 line 454) →

         ΔP = ρ_max·c₀·c₀ = ρ_max·c₀² = P_max = 1.172×10³² Pa   (exactly)

     → f = ρ_max/ρ_mist ≥ 1 for any mist at ρ_mist ≤ ρ_max: the sealed geometry converts
     EVERYTHING in the collapsing zone, whatever its density. The spike §8 says exists is
     exactly the pressure the conversion rule says suffices for full conversion; the converted
     mass is the mist inventory of the zone (mass conservation), not ρ_max × geometric volume.
     Heat expelled = m·c₀² = ΔP·ΔV_compressed (PV bookkeeping of the compressed side).

(c) **Water sanity check (same rule, real fluid):** Δv = 14.1 m/s, c = 1500 m/s, ρ = 1000
     kg/m³ → ΔP = ρcΔv = 2.1×10⁷ Pa → m/V = ΔP/L_vap = 2.1×10⁷ / 2.257×10⁶ ≈ 9.4 kg/m³,
     ≈0.9% of the m³ per slam. Right order for vapor-bubble condensation mass. The rule is
     the ordinary fluid-mechanics statement; PWC is the ρ_max, Δv = c₀ endpoint of it.

## 3. RBH-1 check — what it needs, what the current numbers give

Current numbers (`PWC.md` §8 line 478):

| Quantity | Value |
|---|---|
| [O III] flash | 1.9×10⁴¹ erg/s = 1.9×10³⁴ W |
| light-equivalent mass rate | ṁ_light = 1.9×10³⁴/c₀² = 2.11×10¹⁷ kg/s |
| over 73 Myr | 4.87×10³² kg = 245 M☉ (reproduces §8's figure) |
| stars formed | 10⁶–10⁷ M☉ → ṁ_stars ≈ 8.6×10²⁰ kg/s (10⁶ M☉ reading) |
| collapsing volume rate | V̇ = ṁ_stars/ρ_max ≈ 6.6×10⁵ m³/s (an 87 m cube per second) |
| light fraction | 245/10⁶ = 2.45×10⁻⁴ ≈ 10⁻⁴, matching §8's efficiency note (the flash samples the expelled heat, not the formed mass) |

What a full run needs and the repo does NOT have: the wake's collapsing volume per unit
time and the local ΔP — i.e. the bow-wave compression profile (`OPEN_WORK.md` line 96,
"NEEDS DERIVATION"). The demand function converts any stated V̇ correctly; it does not yet
predict V̇. That is the honest boundary of what this rule closes today.

Falsification form (proposed, for Jaden's OK): the SAME ΔP(ρ) rule must give (i) RBH-1's
formed mass, (ii) the great-freeze baryon fraction, with zero per-event tuning.

## 3b. RBH-1 run results (run 2026-10-08, Jaden's blanket OK; `scratch/rbh1_demand_test.py`)

Inputs: published tail radius 0.7–0.8 kpc (`rbh1/RESULTS.md`), 954 km/s, 73 Myr,
62 kpc (`rbh1/PREDICTIONS_FROZEN.md`), flash 1.9×10⁴¹ erg/s, stars 10⁶–10⁷ M☉ (§8).
Sealed collapse: each wall closes at c₀, gap shrinks at 2c₀ → V̇_swept = 2·πr²·c₀.

| Quantity | Result |
|---|---|
| Inferred wake mist density ρ_mist = ṁ_stars/(2πr²c₀) | **0.086–0.112 ρ₀** (r = 0.8–0.7 kpc) |
| Full-conversion threshold Δv ≥ c₀·ρ_mist/ρ_max | 2.3×10⁻³⁴ m/s — satisfied by 4×10³⁹× |
| Required spike ρ_mist·c₀² vs sealed P_max | 8.8×10⁻¹¹ Pa vs 1.17×10³² Pa — 10⁴²× margin |
| Expelled heat rate ṁ_stars·c₀² | 7.76×10³⁷ W = 7.76×10⁴⁴ erg/s |
| Flash escape fraction 1.9×10⁴¹ / 7.76×10⁴⁴ | **2.45×10⁻⁴** (10⁶ M☉) / 2.45×10⁻⁵ (10⁷ M☉) — §8's 10⁻⁴–10⁻⁵ order |
| Flash light-equivalent over 73 Myr | 244.8 M☉ — reproduces §8's ~245 |
| Proton check: collapse volume m_p/ρ_max → R_ball | 8.011 R_p (Identity B = 8) |

**Reading.** The conversion is deep in the mist-limited regime: the demand rule's quantitative
content at RBH-1 is the threshold (satisfied with enormous margin), so it predicts that
EVERYTHING the closing walls sweep converts, and the formed mass = the mist inventory of the
zone. Inverting the observed star rate + sealed closing speed pins the zone's mist density to
~0.1 ρ₀ — the rarefied medium phase, below the resting baseline, exactly the "vapor/mist-like
phase of the medium itself" §8 line 453 describes. That number is a NEW, checkable output:
a wake mist at ~0.1 ρ₀ could be falsified if a future trail-width/mass measurement pushes it
above ρ₀ (impossible for a rarefied zone) or forces r beyond the observed trail.

**Open (unchanged):** the rule does not yet predict ρ_mist from the medium's own P(ρ) — that
is the bow-wave compression profile (`OPEN_WORK.md` line 96). What this run gives: with the
measured geometry the profile must land at ρ_zone ≈ 0.1 ρ₀; that is now a target condition
for the still-missing profile derivation.

## 3c. Closure-rate and supply-cap checks (run 2026-10-08, `scratch/wake_closure_rates.py`,
## `scratch/rbh1_supply_cap.py`)

**Closure rates.** A 0.7 kpc cavity closes in 2,083 yr (Rayleigh collapse at P_max) or
2,283 yr (walls at c₀ each) — the 5% stretch pressure deficit gives 12,500 yr. The wake
persists 73 Myr with continuous, age-ordered star formation: **a 3.2×10⁴× gap.** The sealed
"walls close at c₀" therefore describes the per-pocket matter-formation slam, not the cavity
closure; the cavity is re-opened at the bow as fast as it closes, and its length is set by
side-channel dynamics. Implied steady-state side-refill speed: v_BH·r/L = 10.8 km/s —
deeply subsonic, so the choke ceiling is not what limits the refill.

**Supply cap.** Sealed: the zone is zero-flow and the displaced medium reroutes around the
core. The only in-zone supply is the mist inventory:

| Supply | Mass |
|---|---|
| zone inventory at the inferred 0.112 ρ₀ | 1,232 M☉ |
| zone inventory at the 1.053-stretch floor (0.95 ρ₀) | 11,700 M☉ |
| ambient cylinder swept by the trail cross-section (if fully captured) | 14,155 M☉ |
| combined ceiling | ≈15,500 M☉ |
| flash light-equivalent (§8) | 245 M☉ — **inside every cap** |
| stars §8 line 478 attributes to the wake | 10⁶–10⁷ M☉ — **65–810× above the cap** |

Steady star formation over 73 Myr requires refilling the zone at ~10²¹ kg/s; the sealed
zero-flow clause provides no supply route for that. **RULED 2026-10-08 (Jaden): PATH (a)
LOCKED** — the stars are swept ambient gas and the PWC admixture is the cap-sized hydrogen
fraction. Against the conventional 10⁷–10⁸ M☉ swept-gas budget the locked prediction is
**dilution d = 1.2×10⁻⁵ – 1.55×10⁻³ → Δ(O/H) = −5×10⁻⁶ to −6.7×10⁻⁴ dex** — 2–5 orders
below the frozen −0.10 dex bar of `rbh1/PREDICTION_metallicity.md`. The bar is unreachable
under path (a); a −0.10 dex pass refutes the cap. (Paths b and c closed by the ruling.)

## 4. What the rule does NOT supply (open items unchanged)

- ΔV(t) — the collapse dynamics (the §8 two-wall geometry is the boundary condition; the
  Rayleigh-Plesset-style evolution is still open).
- P_eq(ρ) between ρ₀ and ρ_max — the w(S) transition; decides ΔP everywhere.
- Cohesion Y (the tension side of the zero): anchored at RBH-1 only, Y = 5.93×10²⁶ Pa
  (`DERIVATIONS.md` row 15). **New two-anchor constraint (arithmetic on sealed premises):**
  light at c₀ is exactly at the resting medium's own cavitation limit (a photon threads a gap
  that opens and shuts in step with it — marginal, critical, no wake), so
  v_cav(ρ₀) = c₀ → Y(ρ₀) = ρ₀c₀²/2 = 3.93×10⁻¹⁰ Pa. Combined with Y(ρ_max) = 5.93×10²⁶ Pa:
  the cohesion per unit density Y/ρ falls from 4.49×10¹⁶ m²/s² at rest to 4.55×10¹¹ at full
  lock — **10⁵× weaker per unit density exactly where the medium is most compressed.** That
  is the hunch's tension side made quantitative: the yank per unit mass is largest in the
  heat-rich resting medium and nearly gone in the heat-expelled locked state (heat is the
  pull, §1) — a constraint any future Y(ρ)/cohesion law in T3 must satisfy.
- Untouched: the merger (not cavitation; no heat — locked rulings respected).

## 5. Tension-side and pairing explorations (2026-10-08)

- **Y(ρ) — SUPERSEDED (2026-10-08, by Jaden's tension-heat-law derivation).** My earlier
  "two-anchor power law" v = c₀(ρ/ρ₀)^(−0.0607) was built on a WRONG anchor
  (v_cav(ρ₀) = c₀). The locked set has Y_cav = s·ρ₀·c₀²/3 = 1.378×10⁻¹¹ Pa (s = 1/19), so
  v_cav(ρ₀) = c₀√(2s/3) = 0.1873 c₀ — my anchor was 28.5× too high. The tension-heat law
  (`TENSION_HEAT_LAW_REPORT.md`) gives Y = sρc₀²/3 on the gas branch (Y/ρ CONSTANT — my
  "10⁵ fall" claim was wrong), the plateau multiplying the yank by 7 (locked 6.9972) to
  Y_coh = 0.061379 P_locked, and γ = 0.2867 P_locked as the unreachable maximum tension at
  4.671 ρ_max (ladder {1, 7/2, 49/3}·sP_locked/3). See §7.

- **ε₀/μ₀ from the pairing — partial; chirality RULED (2026-10-08).** Jaden: EM(+) and
  EM(−) are opposite chirality. Numbers from ℏ+ρ₀+c₀: a(ρ₀) = 79.6 μm, m_w = 2.2×10⁻³⁹ kg,
  λ_w = 159 μm, link stiffness k = 1/(ε₀a) = 1.4×10¹⁵ N/m. With the charge quantum q_w = e,
  the candidate μ₀ = m_w·a/e² = 6.85×10⁻⁶ N/A² vs the real 1.257×10⁻⁶ — 5.45× off, same
  order, not clean. Chirality settles WHAT the pair members are; the coupling magnitude
  (the opposite-chirality yank law) is still open, and ε₀'s value cannot fall out of any
  pair-force model without circularity (the yank defines ε₀). Still partially open.

- **γ per unit heat — RESOLVED, superseding my four-cut null (2026-10-08).** Jaden's
  tension-heat-law derivation (`TENSION_HEAT_LAW_REPORT.md`) closes this item: the law is
  dY/d(ΔH) = −3Y/c₀², tension per unit heat = 3Y/c₀² = sρ (rises as the pairs close);
  γ = 0.2867 P_locked is the unreachable maximum tension at 4.671 ρ_max, and the cohesion
  actually carried at Max-P is Y_coh = 0.061379 P_locked. My earlier nulls (0.287 m,
  g_yield/2c₀²) were arithmetic restatements of γ = P·R/2, not the link — the link is the
  tension-per-heat law itself, now derived. See §7.

- **Path-(c) check for the RBH-1 supply cap:** the diffuse isothermal branch
  ρ_excess = c_s²/(2πGr²) gives 2.2×10⁹ ρ₀ at 62 kpc from the host and a 3.2×10¹³ M☉
  swept supply — unphysical, so path (c) cannot borrow that formula as written; the local
  galaxy-scale medium profile is the open Domain-V item (`OPEN_WORK.md`), not a number that
  exists yet. Paths (a) and (b) remain for Jaden's ruling.

## 6. Cross-checks against the sealed laws (run 2026-10-08, `scratch/t2_crosscheck.py`)

**(a) The demand function reproduces the sealed T2 creation law to a geometric prefactor.**
Same geometry (holding-reach cross-section πR_hold² = πGM/a₀), same clock (collapse front at
the locked-phase sound speed c₀), same inputs (ρ₀, G, a₀, c₀, ρ_b):

    demand route:  ρ̇ = ΔP·V̇/c₀² = (1/√3)·ρ₀·π·G·ρ_b·c₀/a₀        [ΔP = ρ₀·(c₀/√3)·c₀]
    T2 (sealed):   ρ̇ = η·ρ₀·π·G·c₀·ρ_b/a₀,  η = 1/4

    ratio = 1/(√3·η) = 4/√3 = 2.309

The work-limited ceiling fraction is 1/√3 = 0.577; T2's locked η = 1/4 runs at 43.3% of the
ceiling; the slack (32.7% of the swept medium) is what re-pairs into ordered medium —
`PWC.md` §5's "most of the released waves pair up". The ungated Earth heat is the same order
as the recorded 1.4×10²¹ W (3.2×10²¹ W on this route — the same gate applies).

**Interpretation REVISED (2026-10-08, after the keystone caloric law):** the "work-limited
ceiling" reading is withdrawn. The spike work per kg (ρ₀c₀²/√3)·(1/ρ₀) = 0.577 c₀² is only
**1.78%** of the full compression ladder (32.371 c₀² per kg, keystone). The slam cannot
finance the compression; the medium's own heat content H₀ ≥ 32.371 c₀² finances 98.2% of
it, and the spike is the TRIGGER, not the budget. T2's η = 1/4 is therefore purely
geometric, not work-budget-limited; the 4/√3 = 2.309 ratio stands as a geometric-prefactor
comparison only (the two rules count the same swept volume with different geometry).

**(b) Water confirms the two-regime structure.** Real cavitation bubbles convert
min(vapor available, work budget): the work-limited mass is ΔP/L_vap = 9.4 kg/m³ of bubble,
while saturated vapor at 20 °C is 0.017 kg/m³ — **water is 542× deep in the vapor-limited
regime**, exactly the mist-limited arm of the rule m/V = min(ρ_mist, ΔP/c₀²). The PWC wake
sits in the same arm; the work-limited arm is the ceiling both share.

**(c) T7 untying split — CORRECTED (2026-10-08).** My earlier "50/50 split" used a wrong
anchor. With the locked Y_cav = sρ₀c₀²/3 (s = 1/19), the marginal tension work per kg
untied is Y_cav/ρ₀ = s·c₀²/3 = c₀²/57 = **1.75%** of the latent heat; T7's heat draw pays
the other **98.25%** — untying is heat-dominated, exactly as T7's step 5 says.
(Arithmetic; the identification P_neg = Y_cav is the locked A1 anchor, not my invention.)

## 7. Integration with the 2026-10-08 caloric/tension-heat derivations (verified)

Jaden's parallel scratch derivations this morning (`PWC_HEAT_RAMP_REPORT.md`,
`COHESION_CHANNEL_HEAT_REPORT.md`, `TENSION_HEAT_LAW_REPORT.md`) close the very items this
draft left open, and confirm the demand function's reading of c₀².

**What they establish (independently re-verified in `scratch/reconcile_heat_ramp.py`):**
- Caloric law dH = P·dv: gas branch H(ρ) = H₀ − (c₀²/3)ln(ρ/ρ₀) (31.371 c₀² to the fold),
  plateau exactly c₀² (P*·dv = c₀²), total 32.371 c₀²; H₀ ≥ 32.371 c₀² (datum D1).
- Tension-per-heat law: dY/d(ΔH) = −3Y/c₀² ⟹ Y = sρc₀²/3 on the gas branch (s = 1/19;
  Y/ρ constant); plateau ×7 (locked 6.9972) → Y_coh = 0.061379 P_locked; γ = 0.2867 P_locked
  = the unreachable max tension at 4.671 ρ_max; ladder {1, 7/2, 49/3}·sP_locked/3.
- v_cav = √(2Y/ρ) = c₀√(2s/3) = 0.1873 c₀, density-independent on the gas branch; locked end
  0.3504 c₀. The 954 km/s bow-wave anchor (row 15) sits at 0.9021 of the heat ladder —
  Y_bow vs Y_coh is a documented unresolved cross-channel tension (their §6c), not resolved here.

**The demand function IS the plateau crossing.** At full conversion my rule reads
m = ΔP·ΔV/c₀² with ΔV per kg = dv = 1/ρ_max and ΔP = P* → 1 = P*·dv/c₀² — identical to
their fold construction. The c₀² in m = ΔP·ΔV/c₀² is the PLATEAU's phase-change heat
(their eq. (2)), which resolves the heat-ramp report's "failing datum L = c₀² as total
inventory": c₀² is the fold/plateau latent heat only; the 31.371 c₀² gas-branch squeeze is
the compression ladder paid by the medium's own heat content H₀ (their option 1). The
demand function never needed L = c₀² as a total inventory.

**What stands / what was corrected in this draft's earlier rounds:**
- Stands: Identity chain 1–4; the RBH-1 heat budget (slam pays only m·c₀²; escape fraction
  2.45×10⁻⁴); the T2 4/√3 cross-check; the water two-regime check; the supply cap; the
  closure-rate gap. Identity 2 (m_p·c₀² = P_max·V_p) is literally the plateau law per proton.
- Corrected: my v_cav(ρ₀) = c₀ anchor and Y(ρ) power law were wrong (28.5× high; §5
  superseded); my "Y/ρ falls 10⁵×" claim was wrong (Y/ρ is constant on the gas branch);
  my T7 "50/50 split" was wrong (correct: tension 1.75%, heat draw 98.25%; §6c).
- New consequence: u_h/P₀ ≥ 96.1 — with H₀ ≥ 32.371 c₀² the resting medium's heat energy
  density is ≥ 96× its pressure: the heat is mostly spacer heat, not pressurizing —
  consistent with "heat holds the pairs apart" and the excess-heat open item.

**Y_bow vs Y_coh — RULED (2026-10-08): nothing snaps.** Jaden: "THE MEDIUM DOESNT SNAP,
THERE IS SIMPLY A HIGH AND A LOW PRESSURE SIDE POSSIBLY TO EXTREMES, BUT NOTHING TEARS…
ITS THE ENERGY FIELD NOT FLUID." So there is no tear threshold: Y_coh = 7.19×10³⁰ Pa and
Y_bow = 5.93×10²⁶ Pa (1.2×10⁴× apart) are **two points on one smooth pressure field** — the
high side at Max-P cohesion, the low side at the wake boundary. The passage limit is where
the field's local pressure gradient can no longer drive the body through, not a rupture.
My earlier "dynamic tear threshold vs static ceiling" proposal is withdrawn in favor of
this reading. The demand function's ΔP·ΔV is **field-energy bookkeeping** (energy density
× volume) — valid in field language; water and its cavitation benchmarks remain ANALOGS
(the framework's own benchmark), not the ontology.

**Bookkeeping flag (keystone A6):** CLAUDE.md §4's "one neutron ↔ 0.207 m³" uses the stale
ρ₀ = 8.1×10⁻²⁷ (0.20678 m³); the correct value at ρ₀ = 8.74×10⁻²⁷ is 0.19164 m³. My T7
reach 3m_p/ρ₀ = 0.5741 m³ uses the correct ρ₀ — Identity 3 unaffected. Flagging, not fixing
(repo file; needs Jaden's say-so).

## 8. The baseline-cold ruling (2026-10-08): T₀ = 0, the 2.7 K bath is matter's exhaust

Jaden's mechanism: the baseline resting state of the field is **negative pressure** — it
naturally wants to stretch; that negative pressure is what we perceive as cold/vacuum, and
it IS the expansion (no Dark Energy). Tying a knot fights that negative pressure; the
friction vents heat = the 2.7 K CMB. **Baseline temperature = 0; the 2.7 K is the extra
heat in the medium because of the matter.** Untying: ambient heat loosens the lock, the
negative pressure rips it open, volume returns to baseline, the knot dissolves into a wave.

Arithmetic (`scratch/rulings_arithmetic.py`, verified):
- CMB energy density 4.175×10⁻¹⁴ J/m³ = 5.3×10⁻⁵ c₀² per kg of medium = **1.01×10⁻³ c₀²
  per kg of matter** — the bath holds 0.1% of one plateau latent heat per kg of matter,
  3.1×10⁻⁵ of the full 32.371 c₀² ladder.
- The RBH-1 flash escape fraction (2.45×10⁻⁴) sits in the same order band → the 2.7 K bath
  is the **radiated sample** of the tying exhaust; the bulk is the invisible spacer heat H₀
  (u_h/P₀ ≥ 96). Consistent with "most of the released waves pair up; the unpaired
  remainder leaves as light" (`PWC.md` §5).
- **H₀-floor reading:** today's matter exhaust = 0.0526 × 32.371 = 1.70 c₀² per kg of
  medium — only 5.3% of the H₀ ≥ 32.371 c₀² floor; an initially fully-tied inventory
  (everything tied at the great freeze, 95% melted since) deposits exactly 32.371 c₀² per
  kg of present medium = the floor. So the spacer heat is the freeze's exhaust, mostly
  ancient — matching "voids are the soup that already cooked" (`PWC.md` §6). Baseline
  T = 0 means no primordial heat; all medium heat is matter's exhaust.
- This answers `OPEN_WORK.md` line 102 ("excess heat vs the measured 2.7 K") in Jaden's
  own words: the medium's heat IS the matter exhaust; the 2.7 K is its radiated fraction;
  the bulk is spacer heat. Reconciliation with the resting-pressure sign: P_net =
  rigidity − Y with ΔP(ρ₀) = 0 (PROVENANCE) — the "negative-pressure baseline" is the
  tension side of that balance ("heat is the pull… the universe is always pulling
  outward", `PWC.md` §1), not a contradiction of the w = 1/3 positive gas-branch pressure.

## 9. The baseline-cold mechanism as equations (2026-10-08, `scratch/baseline_cold_formal.py`)

**The tug-of-war at rest.** Rigidity (push) P_g = ρc₀²/3 against tension (pull)
Y = sρc₀²/3, s = 1/19 (tension-heat law). Net: P_net(ρ) = (1−s)ρc₀²/3 > 0 for every
gas-branch density — so under the locked Y ∝ ρ law the baseline cannot be literal
P < 0; the "negative pressure" Jaden rules is the **pull side**, 5.26% of the push
(push:pull = **19:1** — the same 1/19 as the stretch datum), and "cold = the vacuum" is
the **low-pressure side**: P_net(ρ₀) = 2.48×10⁻¹⁰ Pa vs P_locked = 1.17×10³² Pa — a
41.7-decade high/low pair, "possibly to extremes, nothing tears." If a literal P < 0
baseline is wanted, the stretch-side Y(ρ) law must differ from Y ∝ ρ — Jaden's call.

**The pull's share.** Tension work per kg tied/untied = Y(ρ₀)/ρ₀ = s·c₀²/3 = 1.75% of the
latent heat; the heat draw pays 98.25%. "The negative pressure rips the knot open" reads:
heat loosens the lock (98.25% of the bill), the pull directs the rip (1.75%).

**The bath = the radiated exhaust.** u_bath = 4.175×10⁻¹⁴ J/m³ books as the tying exhaust's
radiated sample with cosmic escape fraction 5.3×10⁻⁵ (full-freeze inventory, 100% tied
once) or 1.01×10⁻³ (today's 5% matter) — the RBH-1 wake's measured 2.45×10⁻⁴ is straddled.
Baseline T = 0 needs no primordial bath: all 2.7 K is matter's exhaust; the bulk is the
spacer heat H₀ (≥ 32.371 c₀² per kg of medium, u_h/P₀ ≥ 96).

**Falsifiable prediction.** Fresh tying sites must show a local excess ABOVE the 2.725 K
bath — unthermalized exhaust (RBH-1's [O III] flash is the existing example); the bath
itself is smooth because it is accumulated, thermalized ancient exhaust — consistent with
CMB isotropy to 10⁻⁵. A measured local tying-region excess below the bath would fail it.

**Field, not fluid.** P_net is field stress (the aligned-wave push vs the chiral-pair pull),
not fluid pressure; the demand function's ΔP·ΔV is field-energy bookkeeping, valid in both
languages. Water remains an analog benchmark only.

**The stretch side — three readings reconciled (2026-10-08, `scratch/stretch_side_decision.py`,
awaiting Jaden's ruling on which to seal):**
1. *Static under Y = sρc₀²/3:* P_net = (1−s)ρc₀²/3 > 0 for every gas-branch ρ — no static
   sign change anywhere, so the sealed "net P negative beyond what Y holds"
   (DERIVATION_BRIEF T3) is not reproducible under Y ∝ ρ.
2. *Dynamic cavitation, ½ρv² = Y:* v_cav(ρ₀) = c₀√(2s/3) = 56,156 km/s (density-independent
   on the gas branch); the wake check closes exactly — ½ρ_max·(954 km/s)² = 5.93×10²⁶ Pa =
   Y_bow — so the wake is a ρ_max phenomenon and nothing observed contradicts the
   gas-branch threshold.
3. *Sealed bookkeeping:* the 1.053 stretch is cosmology arithmetic (95% of final volume,
   OPEN_WORK:124), never a claim of a local sign change.
Reconciliation proposal: "negative pressure" = the dynamic pull exceeding Y (2) plus the
low-side reading (§9's 41.7-decade pair); static P_net stays positive (1); the 1.053 stays
bookkeeping (3). A literal static P_net < 0 baseline would need a new stretch-side Y(ρ)
law — prepared either way, Jaden's call.

**The literal branch, fully prepared (2026-10-08, `scratch/literal_branch.py`, trial form):**
the vacuum's negative pressure = a constant pull term P_pull = (1−s)ρ₀c₀²/3 = 2.48×10⁻¹⁰ Pa
— the PROVENANCE "expansion pressure pushing out, balanced by something pushing back." Then
P_net(ρ) = (1−s)(ρ−ρ₀)c₀²/3: **zero at rest, negative below rest, positive above** — any
rarefaction tips the region negative and it "rips open" toward baseline: the mechanical
tug-of-war with no dark-energy term. At the sealed 5.3% stretch P_net = −0.906·Y_cav, and
the net tension reaches −Y_cav at a 5.556% stretch (1/18) — within 6% of the sealed 1/19
(5.263%) and in water's 6.4% cavitation class. The ONE assumption Jaden would be signing:
P_pull's density-independence (micro backing open — the caloric law H(ρ) does not make the
pull constant per unit volume by itself).

**Chirality coupling closure (2026-10-08):** the pair's confinement geometry (ℏ) fixes mass
and spacing (m_w = ħ/(2ac₀), E_pair = 2π·m_w·c₀²), but the zero-point yank
k_zp = 2πħc₀/a³ = 3.9×10⁻¹³ N/m is ~10²⁸× weaker than the ε₀-spring k = 1/(ε₀a) =
1.42×10¹⁵ N/m. The yank is therefore a separate coupling datum — ε₀ itself — and the
opposite-chirality coupling law remains the single open input for ε₀/μ₀. **Dead end
recorded (do not re-derive):** μ₀e²/(m_w·a) = 8πα to 7×10⁻¹¹, but m_w·a = ħ/(2c₀)
identically, so the "match" reduces to μ₀ = 1/(ε₀c₀²) — the μ₀ε₀c₀² = 1 identity, not a
result. No arithmetic closes the coupling datum.
