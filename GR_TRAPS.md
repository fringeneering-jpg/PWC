# GR traps — standard-theory habits to cancel BEFORE they start an argument

Read this first. Every entry is a habit (Claude's, a reviewer's, another AI's) that imports standard-theory assumptions the framework has already rejected, what PWC says instead, and where it is stated.
Rule: if a sentence you are about to write uses the left column, rewrite it in the right column. If a mechanism is merely unfamiliar, that is not evidence it is wrong.

| Standard-theory habit | PWC instead | Where it is stated |
|---|---|---|
| Singularity / infinite density / zero-radius point | Solid neutron core (ρ ≈ 2.3×10¹⁷) inside a ρ_max shell (1.304×10¹⁵). Hard ceiling; past it the excess goes into **thickness, not density** | `PWC.md` §0 Steps 2, 4, 5; "No violations" paragraph; `PWC/derivations/gw150914_shell.md` |
| Event horizon at 2GM/c² as "the edge" | The edge is the **sonic choke**: where infall reaches the medium's own sound speed (c_s = c). This gives Hawking T exactly, zero free parameters. 2GM/c² radii are "space-weighs-nothing" values, not PWC values | `PWC.md` §0 Step 1, §8; `OPEN_WORK.md` (BH radial profile) |
| Free-fall v = √(2GM/r) from empty space | Space is not empty: v(r)² = 2∫G·M_enc(r′)/r′² dr′ with **the medium's own mass in M_enc**, against c_s(r) rising c₀/√3 → c₀ | `OPEN_WORK.md` (BH radial profile) |
| Space weighs nothing / is a mathematical zero | The medium has mass and its own gravitational pull. 1/r² is the geometric dilution/decompression profile of a finite medium response | `PWC.md` §0 Step 3; §2 |
| Gravity = spacetime curvature / geometry | Gravity = **tension of the medium**. A mass tensions the medium it pulls on; that is why 1/r² works outside a mass | `PWC.md` §0 Step 7 "Deriving the √(a₀·g_bar) term" |
| Ringdown, quasi-normal modes (2,2,0), photon sphere, 3GM/c² radius | **Forbidden vocabulary.** The gravity wave **is the medium itself returning to rest tension**. The settling time τ (GW150914 4.68 ms) is how long that takes | Jaden, 2026-10-01; `PWC.md` §4 |
| Gravitational waves as a separate thing radiated by the merging mass | GW = the medium's own **transverse neighbour-reaction wave at c₀**, same mode as light, hence the same speed (GW170817, 1 part in 10¹⁵). It is not a compression wave | `PWC.md` §4 "Why light moves at exactly c₀" |
| The 3 M☉ is mass converted to radiated energy (E = mc²) and "vaporized" | The 3 M☉ is **medium**: 14 M☉ held before, 11 M☉ after, 3 M☉ released. Core mass is conserved. Medium is conserved and released | `PWC.md` §0 Step 5; `PWC/derivations/gw150914_shell.md` |
| A merger is cavitation / water-hammer / Joukowsky slam | **The merger is not cavitation.** The neutron cores simply join; the displaced medium volume is the wave. Cavitation (bow wave, Rayleigh-collapse) is the *different* case: RBH-1 wake, SMBH-passage collision | `PWC.md` §8 "Bow wave vs. cavitation zone" |
| Reach/holding radius computed from the core's pull alone | Reach uses **total mass including the medium**: r_y = √(G·M_total/yield), yield 3.23×10¹¹ N/kg | `PWC.md` §0 Steps 3–5 |
| "No echoes" needs a horizon | No echoes: the shell is continuous, there is no wall to reflect off | `PWC.md` §8 "No gravitational-wave echoes" |
| Cosmic expansion = metric stretching driven by dark energy | Expansion = volume added to the medium by **untying knots** (radioactive-decay analog); matter-dense regions expand locally, voids stay static | `PWC.md` §5–§6; T7 |
| Galaxy rotation needs dark-matter halos (or modified inertia) | The zipper: tensioned medium keeps its mass and hold; g_obs = g_bar(1 + √(a₀/g_bar)); a₀ is the holding threshold for resting medium. One constant, 0.1327 dex | `PWC.md` §0 Steps 6–7 |
| Photons are massless because nothing is there | A photon is the **same substance** as the medium at lower local density; the denser medium squeezes it out (buoyancy) to ~zero measured rest mass. m = L/c₀² | `PWC.md` §4 |
| c is a spacetime constant | c₀ = 1/√(μ₀ε₀): restoring stiffness over inertia of the medium (Maxwell 1861–62) | `PWC.md` §4 |
| Matter moving through the medium feels drag / is a solid | Matter is a **sieve**, ~99.9–99.99% empty; passes through with no drag; the passage scale is **continuous** (photons c₀, neutrinos just under, sieve matter ~1000 km/s at ρ_max). Never binary | `PWC.md` §5; Jaden's rulings |
| Mass of a merger remnant comes from catalogue "final mass" | Caution recorded in `OPEN_WORK.md`: catalogue final masses are produced by the standard pipeline. The k-rule tests use them as-is (89 events, −0.97%); a native settling-time → mass relation is the independent version and is **not yet derived** | `OPEN_WORK.md` |

## Habits of argument (not physics, but they cause the same fight)

- **Do not demote the validated chain** (Hawking exact, k-rule 89 events, shell/ρ_max, 3 M☉, SPARC 0.1327 dex) to "prediction". Only things with no measurement behind them are labelled as predictions.
- **Do not import a formalism silently** (standard-theory mode analysis, shell theorem, Rayleigh-Plesset, photon gas). If one is needed, say which assumption it carries and whether the medium allows it, *first*.
- **Not understanding a mechanism ≠ wrong.** Don't object every turn while the model is being built; bank the objection, raise it rarely.
- **Same certainty on conservation laws as anywhere else.** No hand-waved infinities, no unaccounted mass or energy.
- **Find the existing derivation before asking.** `DERIVATIONS.md`, `PWC.md`, every branch, history. Only then ask him to paste it, and commit it the moment he does.
