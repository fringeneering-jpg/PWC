# PWC Gap-Fill Report — M = L/c₀² as medium pressure/tension (2026-10-08)

Agent work product, run with Jaden's blanket OK ("RUN ANY NEW TESTS YOU WANT"), committed
2026-10-08 on his "in the git". All numbers are arithmetic on Jaden's sealed numbers,
verified by the scripts listed in
`PWC/derivations/demand_function_pressure_conversion.md` (committed under `PWC/`).
His three rulings (path (a), chirality, no-snap/energy-field) and his verbatim statements
are in the session_logs capture files beside this one.

## 1. The hunch, already sealed

Jaden's words: "M = L/C²₀ is the key where the zero is the pressure of the medium, or the
tension depending which way it's pulling, and the heat is what's escaping the medium when it
cavitates to form the knots."

The framework already says it — `PWC.md` §4 line 196: "**c₀²** = the specific latent heat of
the universe — the medium's own pressure/stiffness, the threshold required to force a phase
change." Line 197: "Mass is light energy that has been phase-locked and condensed by the
localized pressure of the superfluid. Relief of that pressure evaporates it." §6 line 271:
"the freeze and the release of latent heat are the same moment … m = L/c² counts the heat
each piece of frozen matter gave up."

## 2. What the hunch adds, as four exact identities (verified)

1. c₀² = 1/(μ₀ε₀) = P_max/ρ_max = L = 8.988×10¹⁶ — the "0" IS the medium's own
   pressure-density ratio at lock (P_max = ρ_max·c₀² = 1.172×10³² Pa).
2. Tying heat = PV work of the collapse: m_p·c₀² = P_max·(m_p/ρ_max) = 1.5033×10⁻¹⁰ J (exact).
3. Tying heat ÷ the knot's T7 reach volume = resting pressure, exactly:
   m_p·c₀²/(3m_p/ρ₀) = ρ₀c₀²/3 = 2.6185×10⁻¹⁰ Pa = P₀ (the mirror of T7 §3's
   V_reach = c₀²/(ρ₀c₀²/3) = 3/ρ₀).
4. Direction: P_net = rigidity − cohesion; P > 0 (compression) → tying, heat OUT; P < 0
   (tension, past the 1.053 stretch) → cavitation, heat IN. Same c₀² slope both ways —
   "the zero is the pressure or the tension depending which way it's pulling."

## 3. The demand function (the missing link PWC.md §8 line 464 names)

    m = ΔP·ΔV / c₀²,   ΔP = P_local − P_eq(ρ_local),   ΔV = pre-collapse volume
    f = ΔP/(ρ_local·c₀²)   [converted fraction]
    m/V = min(ρ_mist, ΔP/c₀²)   [two regimes: mist-limited vs work-limited]

- Rest: ΔP = 0 → nothing converts (matter forms only at slams).
- Sealed two-wall slam at Δv = c₀: ΔP = ρ_max·c₀² = P_max exactly → converts everything.
- Water (real cavitation): work-limited 9.4 kg/m³ vs vapor 0.017 kg/m³ → 542× deep in the
  vapor/mist-limited arm — the same arm the PWC wake sits in.

## 4. RBH-1 results

- Wake mist density implied by the star rate + sealed 2c₀ closure: **0.086–0.112 ρ₀** — the
  rarefied medium phase, matching §8 line 453's "vapor/mist-like phase".
- Expelled heat 7.76×10³⁷ W; flash escape fraction 2.45×10⁻⁴ (matches §8's 10⁻⁴–10⁻⁵);
  flash light-equivalent 244.8 M☉ over 73 Myr (reproduces §8's ~245 exactly).
- Proton check: collapse volume m_p/ρ_max → R_ball = 8.011 R_p (Identity B).
- **Closure-rate gap:** 0.7 kpc cavity closes in ~2,100–2,300 yr (Rayleigh at P_max; walls
  at c₀) vs 73 Myr observed → 3.2×10⁴×. The sealed c₀ closure is the per-pocket
  matter-formation slam; the cavity is maintained by side-channel dynamics (implied
  side-refill 10.8 km/s, subsonic).
- **Supply cap (new tension, needs Jaden's ruling):** the zero-flow zone holds only
  1,232–11,700 M☉ of mist; the swept cylinder adds ≤14,155 M☉ if captured; combined ceiling
  ≈15,500 M☉. The 245 M☉ flash fits inside every cap; the 10⁶–10⁷ M☉ of stars §8 line 478
  attributes to the wake exceed the cap 65–810×. Steady star formation needs zone refill
  ~10²¹ kg/s, which the sealed zero-flow clause provides no route for. Paths:
  (a) stars = swept ambient gas, PWC share = cap-sized dilution (Δ ≈ −0.0005 to −0.007 dex,
  far below the frozen −0.10 dex bar — a −0.10 pass refutes the cap);
  (b) the zone is refilled at 380–3,400 km/s (needs a mechanism);
  (c) local medium ~10³ ρ₀ (the isothermal branch gives 2.2×10⁹ ρ₀ at 62 kpc → 3.2×10¹³ M☉
  swept, unphysical — so (c) needs the real galaxy-scale profile, the open Domain-V item).

## 5. Cohesion Y and the passage scale — SUPERSEDED/CORRECTED by Jaden's keystone files

My earlier two-anchor constraint (v_cav(ρ₀) = c₀) and the Y(ρ) power law were built on a
WRONG anchor and are withdrawn. Jaden's `TENSION_HEAT_LAW_REPORT.md` /
`COHESION_CHANNEL_HEAT_REPORT.md` (workspace root, 2026-10-08 5:5x AM) derive the correct law:

- Y_cav = s·ρ₀·c₀²/3 = 1.378×10⁻¹¹ Pa (s = 1/19); v_cav = c₀√(2s/3) = 0.1873 c₀,
  density-independent on the gas branch.
- Tension-per-heat law dY/d(ΔH) = −3Y/c₀² ⟹ Y = sρc₀²/3 on the gas branch (Y/ρ CONSTANT —
  my "10⁵ fall" was wrong); plateau ×7 (locked 6.9972) → Y_coh = 0.061379 P_locked.
- γ = 0.2867 P_locked = the unreachable max tension at 4.671 ρ_max; ladder {1, 7/2, 49/3}.
- The 954 km/s bow-wave anchor (row 15) vs Y_coh is a documented unresolved cross-channel
  tension (their §6c), not resolved here.

## 6. Cross-checks against sealed laws

- **T2 creation law reproduced to 4/√3 = 2.309:** demand route gives
  (1/√3)·ρ₀·πGρ_b c₀/a₀ vs T2's η·(same), η = 1/4. Interpretation revised after the
  keystone caloric law: the spike work (0.577 c₀²/kg) is only 1.78% of the 32.371 c₀²/kg
  ladder — the slam is the trigger, the medium's H₀ finances the compression; η = 1/4 is
  purely geometric. The 4/√3 ratio stands as a geometric comparison only.
- **T7 untying split — CORRECTED:** with the locked Y_cav, tension pays s·c₀²/3 = 1.75% of
  the latent heat; T7's heat draw pays 98.25% (my earlier "50/50" used the wrong anchor).
- **Water:** 542× vapor-limited — confirms the min(ρ_vapor, ΔP/c₀²) two-regime structure.
- **Y_bow vs Y_coh — the wake observation selects the channel:** cohesion channel gives
  v_cav(ρ_max) = 105,000 km/s, bow-wave channel 954 km/s. RBH-1 moves at 954 km/s and the
  wake exists → the passage limit at ρ_max is Y_bow. Proposal for the keystone's §6c:
  Y_bow = dynamic tear threshold, Y_coh = static cohesion ceiling — two channels, no
  conflict; the bow-wave boundary sits at 0.9021 of the heat ladder. For Jaden's ruling.
- **Bookkeeping flag (keystone A6):** CLAUDE.md §4's "0.207 m³ per neutron" uses the stale
  ρ₀ = 8.1×10⁻²⁷; correct is 0.19164 m³ at 8.74×10⁻²⁷. My per-proton 0.5741 m³ (T7 reach)
  uses the correct ρ₀ — unaffected. Flagging, not fixing.

## 7. Open items — status after integrating Jaden's keystone files

- **Heat→tension γ link — CLOSED by Jaden's tension-heat law** (dY/dΔH = −3Y/c₀²;
  tension per unit heat = 3Y/c₀² = sρ). My four-cut null is retired.
- **ε₀/μ₀ from the pairing:** partial — a(ρ₀) = 79.6 μm, m_w = 2.2×10⁻³⁹ kg,
  k = 1.4×10¹⁵ N/m from ℏ+ρ₀+c₀. Blocked structurally: the pair yank defines ε₀, so no
  pair-force model can output ε₀'s value without circularity; μ₀ needs the charge quantum
  (candidate 2.34e), which needs Jaden's ruling on what EM(+) and EM(−) physically are
  (PWC.md line 118). STILL OPEN.
- **The demand function IS the plateau crossing:** m = ΔP·ΔV/c₀² at full conversion is
  identical to the keystone fold construction P*·dv = c₀² — the c₀² in the rule is the
  plateau latent heat only, which resolves the heat-ramp report's "failing datum L = c₀²"
  (their option 1). The demand function never needed L = c₀² as a total inventory.
- New consequence: u_h/P₀ ≥ 96.1 (H₀ ≥ 32.371 c₀² ⇒ the resting heat density ≥ 96× the
  pressure — spacer heat, consistent with "heat holds the pairs apart").

## 8. Jaden's rulings (2026-10-08 10:48) — recorded verbatim in capture

1. **RBH-1 supply path: (a) LOCKED** — stars = swept ambient gas; PWC admixture = the
   cap-sized hydrogen fraction. Locked prediction: dilution d = 1.2×10⁻⁵ – 1.55×10⁻³ →
   Δ(O/H) = −5×10⁻⁶ to −6.7×10⁻⁴ dex against the conventional 10⁷–10⁸ M☉ budget — 2–5
   orders below the frozen −0.10 dex bar; the bar is unreachable under (a), and a pass
   refutes the cap.
2. **Pair ontology: CHIRALITY** (EM(+) / EM(−) opposite chirality). Baseline = negative
   pressure that drives expansion (no Dark Energy); **baseline T = 0**, the 2.7 K CMB = the
   extra heat from matter (the tying exhaust vented out). Tying fights the negative
   pressure (friction → heat); untying = heat loosens the lock, the negative pressure rips
   it open. Arithmetic: the bath = 1.01×10⁻³ c₀² per kg of matter (0.1% of the plateau
   latent heat) — the same order band as the RBH-1 flash fraction (2.45×10⁻⁴); the bulk of
   the exhaust is the spacer heat H₀. H₀-floor reading: an initially fully-tied inventory
   deposits exactly 32.371 c₀² per kg of present medium — the freeze's exhaust is the
   spacer heat ("voids are the soup that already cooked"). ε₀/μ₀: with q_w = e,
   μ₀ = m_w·a/e² = 6.85×10⁻⁶ vs real 1.257×10⁻⁶ (5.45×, same order, not clean) — the
   coupling law is still open; chirality settles the WHAT.
3. **Y_bow vs Y_coh: nothing snaps** — high/low pressure sides, possibly to extremes, no
   tear; **the medium is an energy field, not a fluid**. Y_coh and Y_bow are two points on
   one smooth pressure field (high side Max-P, low side wake boundary); the passage limit
   is where the local pressure gradient can no longer drive the body through. The demand
   function's ΔP·ΔV is field-energy bookkeeping; water stays an analog benchmark.

Files: `scratch/demand_function_draft.md` (full derivation), `scratch/rbh1_demand_test.py`,
`scratch/wake_closure_rates.py`, `scratch/rbh1_supply_cap.py`, `scratch/y_powerlaw_and_iso.py`,
`scratch/t2_crosscheck.py`, `scratch/verify_demand_draft.py`, `scratch/hunch_arithmetic.py`;
capture: `capture/2026-10-08_0756_c0sq_pressure_tension.md`. Git untouched throughout.
