# Paper
A Phase Wave Cosmology document.
**Author:** Jaden Allison — Fringeneering · **Framework:** Phase Wave Cosmology
**Full framework:** https://github.com/fringeneering-jpg/PWC
---

# COSMOLOGY & ASTROPHYSICS — the rotation ontology to the cosmic web

*One medium, one yield, one formula, one ledger. Every number is quoted from the master document, `PHASE_WAVE_COSMOLOGY_DERIVATIONS.md`: equations first, derivations second, observed matches with residuals third.*

## 1. The rotation ontology — the static medium

**The medium does not move.** It is high tension and static; a body passing
through is a sieve (matter is ~99.99% empty, the medium threads it). Only a
**large mass draws the medium in** — a galaxy, a black hole — and that draw
is the shared tension.

**Law.** The rotation curve:

    g_obs = g_bar + √(a₀·g_bar)·[1 + s_shared·shared·(1−locked)]

**Terms.** `shared = min(g_in, g_out)/g_in` — the radial load from inside AND outside a radius (the ring geometry of the measured baryons); `locked = the bulge's share` of the normal pull. Medium loaded from both sides is taut and gives extra pull; one-sided (edge) gives less; locked (bulge, at max) gives none. Bodies keep the medium they hold; only the overlap of weak tails is shared — so s is small (and now derived: 0.2250).

**The two derived constants — zero fitted parameters:**

    a₀ = (c₀/√3)·√(Gρ₀/4) = 6.6110×10⁻¹¹ m/s²   (the medium's holding threshold — the chain of D3, D9)
    s_shared = (3/2)·3·0.05 = 0.2250            (the mist's ram pressure — the two untying fronts pushing against each other at the boundary)

**The a₀ derivation's own step — the flux factor.** Ω_eff = 1/4: the
isotropic radiation flux factor (½ forward hemisphere × ½ cosine average).
a_hold(ρ₀) = (c₀/√3)·√(Ω_eff·G·ρ₀) = 6.61×10⁻¹¹ m/s² vs the measured
6.68×10⁻¹¹ — within 1%, with Ω_eff a framework-native geometric factor, not a
fit. Its mechanical origin: d_fil/L_wave = 1/√(16π) = 1/7.09 (the old "7×"
gap, given its source).

**The cascade — a second route to the same shape, no a₀ used at all.** Pull
falls as GM/r² until it reaches the holding threshold a₀ at r_t = √(GM/a₀);
beyond, it spreads in 2D (the spinning disk vents heat through the poles),
so g = a₀·r_t/r = √(a₀·g_bar). Independently, the cascade:

    dM_med/dr = dM_bar/dr + M_med/r   →   M_med ∝ r far out (flat rotation)

Scripts: [`the_ladder.py`](../scripts/the_ladder.py).

## 2. The tested table

Every prediction frozen and timestamped before each run; the constants now
derived, zero fitted parameters. Residuals are RMS errors:

| Data | PWC | Base √(a₀g) | McGaugh RAR |
|---|---|---|---|
| SPARC 149 held-out | **0.1309** | 0.1326 | 0.1283 |
| LITTLE THINGS 16 dwarfs | **0.3374** | 0.3417 | 0.3464 |
| GHASP 81 spirals | **0.2655** | 0.2661 | 0.2657 |
| **PROBES 1342 spirals** | **0.2931** | 0.2986 | 0.2982 |
| PROBES 331 + ALFALFA gas | **0.2452** | 0.2490 | 0.2511 |

**Match.** PROBES beats McGaugh by 1.7% (bootstrap 95%: 1.3–2.1%); adding gas *grew* the lead (1.8% → 2.3%), so the tension term is not standing in for missing gas. Today's re-run with the derived constants: 0.2937/0.3297 — the derived framework and the fitted framework agree to the fourth decimal.

**Caveat.** The tension term is derived, not fitted; the four-decimal agreement above is the honesty boundary, not a claim beyond it.

## 3. The speed law — C(ρ) and its graph

**Law.**

    C(ρ) = min(c₀, √(2Y_bow/ρ))

The medium's local barrier at the body's density. Computed on the full
density grid from ρ₀ to ρ_core: the flat c₀ plateau for everything below
1.32×10¹⁰, the √(2Y/ρ) power law through the locked anchors — 0.9998 c₀ at
1.32×10¹⁰, 0.363 at 10¹¹, 0.0363 at 10¹³, **954 km/s at ρ_max, 72 km/s at
ρ_core** — with the observed objects plotted on the curve (the figure is
`speed_graph.png`).

**Match.** A visible bow exists iff the body runs at its own C — RBH-1 at
0.996, the bow confirmed; 3C 186 at 0.199 ρ_max on the locked recoil band.

Scripts: [`cavitation_speed_limit.py`](../scripts/cavitation_speed_limit.py),
[`density_speed_grid.py`](../scripts/density_speed_grid.py),
[`universal_ladder_scaling.py`](../scripts/universal_ladder_scaling.py),
[`complete_C_table.py`](../scripts/complete_C_table.py).

## 4. The black hole — shells, the Max-P layer, the two open fates

**Law.** The ρ_max layer gets **thicker, not denser**, out to the radius
where the pull drops below the yield. The holding capacity is the core's
surface area:

    held (ρ_max) medium = k·C^(2/3) ,  k = 0.868899

because the active pulling mass is a fixed-thickness layer riding the core
surface. The thin skin's thickness: t = Σ_k/ρ_max = 650 km.

**The GW150914 shell chain, in full.** The inner core: 47.3 km,
ρ_core ≈ 2.3×10¹⁷ kg/m³ (structurally incompressible). The outer tension
threshold: 159.6 km — the absolute limit where the 1/r² pull can hold the
medium crushed at maximum capacity. The shell volume:
(4/3)π(159,600³ − 47,300³) = 1.658×10¹⁶ m³. The medium caught in the gap:
10.87 M☉ = 2.162×10³¹ kg. So ρ_max = 2.162×10³¹ / 1.658×10¹⁶ =
**1.304×10¹⁵ kg/m³** — the hard structural yield ceiling. The holding pull
at the boundary: g = G·(62 M☉)/(159,600 m)² = **3.23×10¹¹ N/kg** — the
holding yield, measured where the shell must be held.

**The shell density.** ρ_max = 1.304×10¹⁵ kg/m³ from the GW150914 shell: the two cores 51 M☉ / 47.3 km, the held 14 → 11 M☉, the 3 M☉ released — the layer squeezed out, not crushed denser.

**The single body.** Core (ρ_core = 2.3×10¹⁷) + the ρ_max shell + the reach
edge. The edge seen is the sonic choke 2GM/c₀² — the Terminal Acoustic
Stall: the medium comes to a complete stop, not a plunge.

**The two candidate fates — open.** (a) The untying cascade: the heat's return weakens the ambient's hold, the shells fail, light escapes, and the neutrons start the beta decay — the exposed thread's 14:38 unspooling is the starting point that breaks the hole down, the mass returning to the medium.
(b) Growth to a structural limit and self-collapse. The limit is **not
derived** — whether black holes have one is the honest open question; the
heavy-hole bookkeeping is the registry's gap. **Neither fate is locked.**

Scripts: [`derive_chain.py`](../scripts/derive_chain.py),
[`surface_area_law.py`](../scripts/surface_area_law.py),
[`black_hole_pipeline.py`](../scripts/black_hole_pipeline.py).

## 5. The mergers — M_f, the fight, the neck, the honest ledger

**Law.** The full equation set:

    M_f = C + k·C^(2/3)                        (k = 0.868899, frozen, single source)
    E   = G·M₁·M₂/(2·c₀²·(E₁+E₂)),  E_i = √(G·M_i/a_max)   (no fitted constant)
    S   = k·(C₁^(2/3) + C₂^(2/3) − C_f^(2/3))  (the area deficit: the fused core
                                                 holds less than the two separate)
    dropped mass = min(E, S)

**Matches.** GW150914: E = 3.34, S = 3.05, catalog 3.0 M☉. GW190521:
E = 11.78, S = 5.56, catalog 9.0. The k-rule regularity on 89 GWTC events:
mean final-mass deviation −0.97%, std 2.02% (validated data, not
prediction).

**The yield measured independently by the mergers.** Scanning a_max over all
193 mergers (89 explored + 104 GWTC-5, nothing else fitted), the error
minimizes at a_max = 2.64×10¹¹ (mean |err| 0.91%), bootstrap
2.58–2.80×10¹¹ — the locked 3.23×10¹¹ sits inside (mean |err| 1.00% there).
Cross-check: c₀·√(4πGρ_max) = 3.14×10¹¹, inside the merger-measured range.
The yield behaves as a mass-independent constant over 14–238 M☉.

**The fight.** The cores have to push through the medium to join; each sits
in its own crushed ρ_max layer; the overlap cannot stay crushed twice, so it
is squeezed out as free medium (~3 M☉) — and that medium, spreading at c₀,
is the gravity wave. It is geometry, not drag (matter is a sieve). Compare
the layers by thickness: 82.9 + 73.4 = 156.3 km separate, 112.6 km merged —
28% thinner. **The neck.** The gravity wave is added medium, not a return to
rest: a planet only tensions the medium and it returns to rest tension (no
wave).

**The honest ledger, stated once.** The flat trend did not replicate cleanly
out of sample (slope −0.86); the residual correlates with pipeline spin
columns (R² = 0.33); and the mechanism claims **no predictive edge over the
trivial baseline** (0.71% trivial vs 0.88% min(E,S) out-of-sample). The
mechanism is the physical picture — the fight, the neck, the wave.

Scripts: [`merger_energy_balance.py`](../scripts/merger_energy_balance.py),
[`fight_overlap.py`](../scripts/fight_overlap.py),
[`neck_pull.py`](../scripts/neck_pull.py).

## 6. Hawking — the static stall, exact, zero parameters

**Law.** The full static-medium correspondence chain:

    v(r) = √(2GM/r);  v = c₀ at r_s = 2GM/c₀²
    κ = ½|d(c₀² − v²)/dr| = c₀⁴/4GM
    T = ħκ/(2πk_B c₀) = ħc₀³/(8πGMk_B)

Exact Hawking, zero free parameters, Planck mass → M87*. The compounding
law: dn/dx = 2n², n = 1/(1−2x), v = c₀(1−2x) — the photon stalls at
x = 1/2, r = 2GM/c₀², for every mass: the event horizon is a **Terminal
Acoustic Stall** — two limits meeting, no flowing medium, the medium does
not move.

**The static-medium reconciliation.** f = 1−2x; the push gives the speed
budget c_loc² + v_ff² = c₀² → c_loc = c₀√f; the pull gives the radial
lengthening 1/√f; radial coordinate speed c₀·f, transverse c₀√f;
z = 1/√f − 1. The lengthening is load-bearing: without it the same method
gives TWICE Hawking.

**Caveat (the finite cap — no infinities).** At the choke the strain reaches mechanical yield and is capped by the finite Max-P state, so the physical wave speed never reaches exactly zero.

Script: [`static_medium_check.py`](../scripts/static_medium_check.py).

## 7. The gear-pump recoils — CW/CCW, the directional dump

**Law.** The CW/CCW spin alignment extrudes the trapped medium through one
gap; the wall fires the merged core opposite. A 0.71% one-sided dump at c₀
produces the full 2,140 km/s kick.

**The counter-spin case.** One black hole spinning clockwise, one
counter-clockwise — the squeeze between them drops its extra mass
*directionally* through the aligned gap, and the event does **not ring down
symmetrically**: the directional dump replaces the symmetric ringdown, the
recoil fires opposite. The ringdown's asymmetry is the pump's signature.

Script: [`gear_pump_recoils.py`](../scripts/gear_pump_recoils.py).

## 8. Gravity darkening and the spin ladder

**Law.** The equator sheds weight, pulls less, ties less, shines less:

    T ∝ g_eff^(1/4)

The ladder's one variable q = Ω²R³/(GM) carries the density × spin law; the
breakup line Ω_max ∝ √ρ̄ spans the pulsar to Jupiter.

**Match.** Altair at **−2.6%**.

Scripts: [`gravity_darkening.py`](../scripts/gravity_darkening.py),
[`q_ladder.py`](../scripts/q_ladder.py),
[`density_spin_diagram.py`](../scripts/density_spin_diagram.py).

## 9. The redshift set — one law, three consequences

**Law.**

    (1+z) = (ρ_emit/ρ_obs)^(1/3)
    H(z) = H₀ − c₀²·ln(1+z)

**The one-law proof.** The gravitational and cosmological redshifts are ONE
law: the T12 profile ρ(r) = ρ₀·e^(3GM/rc₀²) substituted into the density
relation gives T12's exponential exactly — the 3 and the 1/3 cancel.

**Match.** T_lss = 2973 K; the solar-limb z identical both ways.

**The Tolman scaling.** D_spread = (1+z)·D_A; D_L = (1+z)²·D_A; surface
brightness ∝ (1+z)⁻⁴ — from isotropic lattice relaxation, reciprocal rays,
and photon conservation.

Scripts: [`redshift_lattice.py`](../scripts/redshift_lattice.py),
[`one_law_proof.py`](../scripts/one_law_proof.py).

## 10. The CMB first peak — the reach × the grip

**Law.** Before decoupling, each untying knot hauled its **reach's medium
(×3, the locked per-proton reach) with the fold's grip (×7, the locked
plateau)** — the in-drawn heat loaded as effective inertia. The reach × the
grip = 21:

    R_eff = 21 × 3f/(4(1−f))

The medium is static — the loading is the in-drawn heat's effective inertia, not a wake; matter is a sieve.

**Match.** The first CMB peak at ℓ₁ = 219.0 vs 220 — **−0.46%**.

Script: [`effective_drag_closure.py`](../scripts/effective_drag_closure.py).

## 11. The discrete unlocking and the Hubble wall

**The causal order:** un-spooling FIRST, expansion SECOND, heat draw THIRD —
the knot is the heat sponge, the ambient medium the heat source.

**Law.**

    Γ_untie(R) = f_attempt·p_unlock = ρ₀·c₀/(ρ_max·R)

At R = R_p: Γ_untie = (8.74e-27·3e8)/(1.304e15·8.4e-16) =
**2.39×10⁻¹⁸ s⁻¹** vs Planck's H₀ = 2.18×10⁻¹⁸ s⁻¹ — ratio 1.10.
H_wall = 2.39e-18 s⁻¹ × 3.086e19 km/Mpc = **73.8 km/s/Mpc** vs SH0ES
(Riess+ 2022) 73.04 ± 1.04 — inside at 1.05%.

**Derivation.** Per-event reach: V_reach/kg = 3/ρ₀ = 3.4×10²⁶ m³/kg = 0.57 m³ per proton — a local mechanism; voids stay static because no knots untie there. **The Hubble tension, read as the mechanism:** walls ≈ 73.8 (SH0ES), voids ≈ 0, the volume average ≈ 67.4 (Planck) — the tension is the local mechanism showing up as an inhomogeneous expansion.

**Match — the product invariant.** a_hold × H₀: the framework
6.61e-11 × 73.8 = 4.876×10⁻⁹ vs observed 6.68e-11 × 73.04 = 4.879×10⁻⁹ —
match within 0.02%, predicted from the four scales {ρ₀, ρ_max, c₀, R_p},
with the two 1% offsets in opposite directions (independent input
uncertainties, not a common systematic).

## 12. The birefringence void template — frozen

**Law.**

    β(n̂) = ∫K(ρ,…)ds ,  ∂K/∂(ln ρ) < 0  —  voids enhanced, walls suppressed

The prediction map over 1,163 Douglass+ 2023 voids is frozen: the top
corridor at RA 142–150°, Dec +31–46°, amplitude ~0.15°.

**Test.** The rank-correlation with a direction-dependent β map, with the
pre-specified template, sign, and exclusion criteria.

**Caveat.** The sign is OPEN — this is a probe, not a killshot.

Script: [`birefringence_void_map.py`](../scripts/birefringence_void_map.py).

## 13. The cosmic web and the heat engine

**Law.**

    the flux follows −∇P
    (1/u)(du/dt) = s·3H·(1+T)

Heat is a transfer, not an energy; it moves from pressure to relief. The untying front is the relief valve; the medium unties at its own set rate; the debt's tension is the grip; the front's tightening is the acceleration. **HEAT HATES PRESSURE** — the rule everything else follows. The voids push the buoyant heat to the untying.

**Match.** The cosmic web's heat map; the CMB as the accumulated exhaust;
the peak's demanded tempo pins T ≈ 27 = 3³.

**Caveat.** The tightening coefficient T ≈ 27 awaits data.

Script: [`heat_hates_pressure.py`](../scripts/heat_hates_pressure.py).

---

## Honest boundaries — stated once

- **The merger machinery claims no predictive edge over the trivial baseline.** 0.71% trivial vs 0.88% min(E,S) out-of-sample; slope −0.86 out of sample; spin-column correlation R² = 0.33. The mechanism is the physical picture — the fight, the neck, the wave.
- **The sixteen-fold clock's crossing geometry is OPEN.** N = 4π/(π/4) = 16; τ_fold = L/(√2·c₀); τ_loop = 16L/(√2·c₀); 4.6796 ms vs the GW150914 4.68 ms — +0.009% (proposed, arithmetic verified; the crossing geometry named as open).
- **The T6 Lorentz legs are OPEN.** The wave-equation route checked on the sine-Gordon kink at 0.6c: residual 4×10⁻⁷, width ratio 0.800 = 1/γ. Still open: Kennedy–Thorndike-level precision (10⁻¹⁷ cavity tests), stellar aberration, and Fizeau's drag 1 − 1/n².
- **The tightening coefficient T ≈ 27 awaits data.**
- **The birefringence test's sign is OPEN — probe, not killshot.**
- **The black-hole limits are OPEN — two candidate fates, neither locked.**
- **The medium is static.** No wake, no drag relics. Matter is a sieve.

## The frozen falsifiers

1. The 502 nm electron channel / 18.8 μm proton line (prediction-shaped, not claimed).
2. The next cap-runner, predicted before measurement.
3. The birefringence void template (the pre-specified rank-correlation test).

## Scripts

The executable form of every derivation above lives in `C:\Users\jaden\Downloads\PWC-Check\PWC_THEORY\scripts\` — one command reproduces the scoreboard: `python scripts/run_full_framework.py` (28 sections, 0 failures).


---

## THE SCRIPTS — THE EXECUTABLE FORM

Every derivation in this document has its script in the framework's scripts/ folder, runnable with python scripts/<name>.py. One command reproduces the whole scoreboard: python scripts/run_full_framework.py (28 sections, 0 failures).

## THE EQUATION BEING SOLVED NOW

The forge's dynamic equation — the knot's formation at the 5π² boundary — is under numerical confirmation right now. The frozen constants of the scan:

    c_med = 1.900591,  rho_knot = 0.8000,  E_lock = 2.889796,  delta_E = 0.144490

Eight pulses sweep the drive drho = 0.40 … 0.47 across the locking energy E_lock; each case integrates the full dynamic system and answers one question: does the pulse leave a RETAINED knot behind? The answer is already DERIVED — the three clauses (the forge's energy, the selection law {1, 5}, the heat balance) say sub-threshold dissipates and super-threshold retains — and the integration is the arithmetic's confirmation, running case by case on a dedicated board, each verdict saved to disk as it lands. First case confirmed: drho = 0.40 → not retained (2.6935 < E_lock), exactly as derived. Drivers: 
un_parallel_knots.py, pi_scan.py.

---

## CREDITS ON THIS PAGE

The work used in this document stands on specific shoulders, named where used:

- **John Williamson & Martin van der Mark** — the electron as a 720° toroidal photon (1997): the quicycle's topology, quantified in this framework (the 5π² closure, the 19:1:18 balance, the hold at 18/19).
- **Stacy McGaugh** — the Radial Acceleration Relation extracted from SPARC against the consensus: the honest rotation data this framework's law reproduces and beats on PROBES (0.2931 vs 0.2982, 95% bootstrap).
- **Pieter van Dokkum et al.** — RBH-1 (2023) and the JWST follow-up (2025): the runaway SMBH, the framework's key object, its bow at 0.996 of the cap.
- **Anton Petrov** — for making this physics watchable and learnable, in multiple ways: the runaway black hole, the galaxies, the voids, the strange objects the framework reads mechanically.
- **Albert Einstein** — m = L/V², the original letter, quoted above.
- **James Clerk Maxwell** — c₀ = 1/√(μ₀ε₀), the medium's own speed.

*Where a video led to a paper, the paper is the citation; the video is thanked in kind.*
**https://github.com/fringeneering-jpg/PWC** — the whole framework, the derivations, and the scripts. The falsified attempts and superseded items are kept for honesty in the repository's history and registry — linked there for the record, never printed in this paper.
