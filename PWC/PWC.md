# Phase Wave Cosmology (PWC)

*Fringeneering — Jaden Allison*

Compiled from the working session that built and ran the GW150914 diagnostic pipeline (`pwc_gw150914_pipeline.py`, same folder). This file holds the theory's rules and reasoning as written during that session; the companion script holds the corrected code that tests it against real detector data.

---

## 1. Core Ontology

PWC treats the universe as a continuous, physically real energy medium — the **birefringent cosmic lattice**, also described as an **electromagnetic ocean**. It is not an empty, zero-content vacuum. Matter, photons, neutrinos, gravity, heat, pressure, and wave phenomena are finite states, modes, stresses, or flows within that medium.

**No physical zero**
- Space is nonzero. Energy is nonzero.
- A photon is not "nothing" because its invariant/rest mass is zero — it is a nonzero energy/momentum mode of the medium.
- Matter is not separate from the medium in the sense of being placed into an otherwise literal void.

**No physical infinity**
- No infinite density, infinite compression, infinite temperature, zero-volume endpoint, or undefined singularity is permitted as a real physical state.
- An infinity is a warning that an idealized equation has passed the finite-state boundary of the physical medium, not a description of what actually happens there.

**No placeholders**
- The theory cannot say "then a singularity happens," "space is zero," "energy disappears," or "an undefined point resolves it somehow."
- Every apparent endpoint must have a finite mechanism: state transition, structural response, propagation, thermal redistribution, phase change, expansion, or rebound.

**Conservation stays real**
- Energy cannot be discarded merely because a mathematical coordinate or limiting expression breaks down.
- The framework aims to preserve mass–energy accounting using standard ADM-style conservation language, while giving energy a physical medium-based route to propagate, compress, redistribute, and reappear as observable behavior.

---

## 2. Medium Mechanics

The medium is effectively **frictionless/superfluid** in its propagation behavior. It is not a static, timeless abstraction — it evolves, transmits stress, and has density, tension, wave speed, and a finite response range.

- Energy moves through the medium as **phase-wave structure**, not through literal nothing.
- Gravity is the medium being pulled, compressed, or made locally denser around high-energy/mass regions. More gravity means more of the underlying medium is attracted/compressed, changing local propagation and effective gravitational behavior.
- Photons and neutrinos are phase-wave/mode-like excitations of the medium.
- The medium is **birefringent**: its response and propagation can depend on phase, density, temperature, or orientation/state.

**The 1/r² reinterpretation** — the key replacement for a bare inverse-square "nothing between bodies" reading:

```
source energy/mass → medium stress / density gradient → spherically distributed response → 1/r²-like weakening
```

1/r² is read as the geometric dilution/decompression profile of a *finite* medium response, not evidence that the region between bodies has no physical structure. Newton's calculation (treating space as a mathematical zero) happened to land on the same functional form a spherically-weakening finite medium would produce — which is PWC's explanation for why the inverse-square law works at all without space actually being empty.

---

## 3. Maximum Compression

The decisive rule: energy concentration has a finite upper compression limit.

```
0 < ρ ≤ ρ_max < ∞
```

A collapse can increase density, tension, phase concentration, and wave frequency, but it cannot proceed to a literal zero radius or infinite density. At the maximum, the medium yields structurally or changes state:

```
compression → maximum finite density/tension → geometric snap, release, redistribution, or phase transition
```

This is the meaning of **"no solution is itself the solution"** in the Navier–Stokes discussion. The formal continuum result may permit a finite-time unbounded limit, but the physical universe does not contain an infinite state for that solution to reach — the missing piece is the finite material rule that stops the idealized continuation before it gets there. The position is not that convergence, vortexing, collapse, or rapidly rising frequency can't occur — it's that the final step, r→0, ρ→∞, is not physical. A real medium reaches a bound and responds.

Stated as the standalone "Time-Independence" law elsewhere in this project: stripping the time derivative out and relying on steady-state spatial pressure/density/geometry is the claimed mechanism that keeps both Navier–Stokes and GR from ever reaching that unbounded step — the fluid hits a maximum localized pressure threshold instead of blowing up.

**Matter is soliton knots, not turbulent vortices — a real, different mathematical class.** Ordinary Navier–Stokes vortices are inherently unstable: they stretch and tangle, cascading down to smaller scales, and that stretching is exactly the mechanism that lets a singularity develop. Solitons are the opposite kind of structure by definition — stable, self-reinforcing, holding their shape rather than cascading apart, because nonlinear and dispersive effects exactly balance instead of one overwhelming the other. If matter is soliton-knotted rather than vortex-structured, there's a real, structural reason it wouldn't inherit ordinary turbulent blow-up: it isn't the same class of object the blow-up mechanism acts on.

**On the 2026 proof that a Navier–Stokes singularity can occur:** that result is real and it does not need to be argued away — it's a rigorous, formally checked construction. Two things about it, though, keep it from closing this section: (1) it's for a *forced* system — an external push applied to the fluid — and the universe has no "outside" pushing on it, so the physically relevant comparison is the *unforced* case, which remains open for the viscous equations; the one related result on record (the unforced, frictionless/Euler case) found regularity — no blow-up — not the other way around. (2) It's a statement about the idealized continuum PDE as pure mathematics, not a claim about what any real substance does — the same gap this section already depends on (§1, "no physical infinity": the math can diverge without physical reality following it there). Both of those are real, precise reasons this framework isn't in tension with that result, not a dismissal of it.

---

## 4. Mass as a Phase Change — m = L/c₀²

Matter and light are not separate entities; they sit on a continuous thermodynamic spectrum, and the medium — not matter — is the baseline, fundamental substance. Matter is a localized, condensed phase of the medium; it is not that matter is fundamental and "contains" energy.

- **L** = light energy — a real, physical quantity of the medium's own substance, not a bookkeeping abstraction. This isn't a borrowed or coincidental symbol: Einstein's own 1905 paper, *"Does the Inertia of a Body Depend Upon Its Energy Content?"*, uses L for exactly this — the energy of light radiated by a body — not a generic energy symbol. His own conclusion there was "the mass of a body is a measure of its energy content." `m = L/c₀²` uses Einstein's own notation for his own specific quantity, applied consistently rather than flattened into the later textbook shorthand E=mc².
- **c₀²** = the specific latent heat of the universe — the medium's own pressure/stiffness, the threshold required to force a phase change. It is a physical property of the medium, not a conversion constant relating two otherwise-separate things.
- Mass is light energy that has been phase-locked and condensed by the localized pressure of the superfluid. Relief of that pressure evaporates it back into propagating light.

**Why light has no rest mass (the buoyancy mechanism):** light is not "made of nothing" and it is not a separate, genuinely massless category of thing. A photon is composed of the same underlying substance as the medium it moves through — same molecular mass — but at a lower local volumetric density than the surrounding medium. Because of that density mismatch, the higher-density medium around it squeezes it — the way a watermelon seed squeezed between two fingers shoots out — expelling it and holding it at effectively zero measured rest mass while it propagates. It isn't that the photon has no mass; it's that the surrounding medium's own pressure keeps forcing it out to a de-facto-massless propagating state. Matter is what happens when that same substance gets condensed past the point where this buoyancy-squeeze can expel it — it stays put as a stable, dense knot instead of getting shot back out.

**Why light moves at exactly c₀, and not some other speed:** light's speed isn't set by how hard any particular squeeze event is — it's a fixed property of the medium itself, the same way the speed of sound through water is set by water's own stiffness and density, not by how loud the sound was. Wave speed in any real elastic medium comes from the ratio of the medium's stiffness to its density; c₀ is that same ratio for the medium as a whole. That's why c₀ comes out to the same fixed number everywhere the medium's bulk stiffness/density ratio is the same, instead of varying with the size or force of whatever squeezed a given photon out.

**HDL flows easier than LDL.** Real water shows this directly: compressing water breaks apart its more rigid, low-density hydrogen-bonded structure into a denser, more loosely-packed one — and the denser state actually flows *more* easily, not less, despite being more compressed. The same ordering applies here: matter, condensed into a knot (§5), sits in the denser, more mobile HDL-like state near where it forms and where the medium is hot and active; the colder, less-compressed medium farther out behaves more like the less-mobile, more rigidly structured LDL state.

---

## 5. Knots and Volumetric Expansion

Matter isn't just "condensed medium" in the abstract — it's a **soliton knot**: a stable, self-tied structure in the frictionless, zero-viscosity medium. A knot is what the phase-lock from §4 actually looks like structurally — energy tied into a compact, self-sustaining shape instead of propagating freely.

- **Tying a knot** is the phase change described in §4: free-propagating energy gets caught and condensed into a stable, self-tensioned structure — that structure is matter.
- **Untying a knot** is the reverse: the tied structure releases back into diffuse, propagating energy — the phase change running the other way.
- **Untying is volumetric expansion.** A tied knot holds energy in a compact, self-tensioned form; when it unties, that same energy is no longer bound into a small structure — it spreads back out into the medium, occupying more volume than the knot did. Every untying event is a small, local release of volume into the medium.

Across the universe, matter is constantly tying and untying — fusion, decay, any reaction that converts mass to radiated energy is a knot untying. Each one is a small local expansion. The claim is that the *aggregate* of all these untying events across all the matter in the universe is what expansion actually is: not space stretching from nothing, but the medium's own volume growing because a continuous background rate of knots are releasing their tied-up volume back into it.

---

## 6. Cosmic Origin — Uniform Untying, Not a Localized Bubble

If expansion is a pressure-driven phase transition — the medium locally dropping below a threshold and part of it converting, the same class of process as cavitation, but describing the state of the medium itself rather than a localized flow disturbance — there's a real question about how it looks the same in every direction to every observer, no matter where they are.

The answer that survives: **it isn't one localized event that we happen to occupy a position within.** It's the same process, happening the same way, everywhere in the medium at once — no privileged location, no distinguishable exterior "unconverted" reservoir. Every observer, anywhere, is at the center of their own local horizon for the same reason every galaxy appears to be at the center of the apparent expansion: because nothing is special about where they're standing, the process is uniform. This is why the CMB — the boundary beyond which light can't reach us, because it's from before the medium was transparent — looks the same distance away in every direction for every observer, not closer on one side: it isn't a wall we're near one edge of, it's how far the same ongoing, everywhere-uniform process has proceeded around wherever you happen to be.

This costs something specific, worth stating plainly: it rules out the picture of our universe as one distinguished bubble sitting inside a larger sea of un-converted medium, with us positioned somewhere inside it. That version would put different observers at different distances from a real boundary, which isn't what's observed. The uniform, no-privileged-location version is the one that survives the check.

---

## 7. Redshift as Medium Reorganization

Light crossing cosmological distances isn't losing energy to anything, because there's nothing outside the medium for energy to be lost to. Light is the medium in one phase; matter is the medium in another. There's no "photon" and "medium" as two separate things trading energy back and forth — there's just the medium, reorganizing between phases. Two things happen together, and both are needed:

- **Phase reorganization (LDL → HDL).** As light passes through progressively denser regions of the medium, its own state reorganizes toward the higher-density phase — the same kind of shift water makes between its low-density and high-density liquid phases. The energy doesn't go anywhere outside the system; it's the same total energy, carried in a different organizational state of the same substance. What shows up at a telescope as redshift is this reorganization, not a loss.
- **Propagation-speed history.** Because the medium's own density has been higher in the past (§5, §9) and propagation speed depends on density (§2), light emitted further back in cosmic history spends more of its trip crossing denser, slower-propagating medium than light emitted more recently. That accumulated difference depends on *when* a photon left its source — and it's this piece, not the phase reorganization alone, that would stretch the spacing between successive photons from the same event, not just each one's individual wavelength.

A mechanism that only reorganizes frequency, with no propagation-speed history behind it, has no reason to stretch a distant supernova's whole light curve. A mechanism that only has a propagation-speed history without a conserved, non-dissipative way to shift frequency reopens the "where did the energy go" objection that sank classical tired light. Combining them is the candidate answer to both at once.

**Open item, not yet closed:** whether the specific density-to-speed relationship (§2) and the specific density-over-cosmic-time history (§5, §9) combine to reproduce the *exact* observed (1+z) stretching factor for both wavelength and timing together — not just stretching in the right direction. That calculation is what would turn this from a coherent picture into a real, checked prediction.

---

## 8. Black Holes and GW150914

A black hole does not contain a singularity or an "infinite hole leading nowhere." It is a finite, compact, high-compression structure governed by the medium's maximum-compression response.

- Black holes are finite neutron/matter core structures rather than infinite-density points.
- The cores are described as approximately 30 km-scale neutron clumps.
- The neutron cores account for the gravitating mass; the two merging cores together are treated as carrying 100% of the black-hole mass in the model.
- The ≈3 solar masses conventionally described as radiated in GW150914 are interpreted as involving space/the medium itself, rather than additional disappearing core mass.
- A black hole is not a one-way sink with unaccounted energy loss — the model's principle is that it outputs as much as it takes in through finite medium-state processes.

The gravitational-wave mechanism is not ordinary fluid friction or generic bulk turbulence. It is a **structural geometric snap**: tension relaxes between merging stress points, producing a quadrupolar wave pattern. The hourglass-like stretch-and-snap geometry is meant to account for the observed quadrupole structure, propagation near light speed, energy loss, and waveform behavior.

**Once released, the wave doesn't dissipate.** A real ocean wave loses energy over distance because real water has viscosity and turbulence — friction converting wave energy into heat. The medium here is frictionless (§2), so once a gravitational wave leaves the merger, nothing in the medium absorbs it; it only weakens the way any wave spreading out from a point does — geometric dilution as the wavefront covers more area, not damping. That matches what's actually been measured: for the 2017 neutron-star merger (GW170817), the distance calculated purely from how much the gravitational wave's amplitude had dropped off matched the distance measured independently from the host galaxy, across 130 million light-years, with no extra loss beyond that geometric spreading. A real friction-based medium would show extra attenuation on top of that; this one doesn't, which is what zero viscosity predicts.

```
pre-threshold chirp progression → increasing concentration/frequency → finite boundary → turnover and structural release
```

The GW150914 pipeline is the observational side of this claim: it extracts the H1/L1 ridge, fits the early rising section with an unbounded power-law projection, and plots the later observed departure from that projection. In this framework, that departure is read as the geometric boundary/yield signal — the system transitions before a mathematical crash, rather than physically completing an infinity.

### The core/gradient mass split

The apparent mass measured from outside a merging pair is split into two physical zones:

```
M_app = M_core + M_grad
```

- `M_core` — the highly compressed physical wave-clump (the actual core).
- `M_grad` — the surrounding high-entropy medium stressed/compressed into a 1/r² gradient to support that core.

Cores are conserved through a merger (`M_core,final = M_core,1 + M_core,2`); the ≈3 M☉ apparent deficit is attributed entirely to redundant gradient-sphere overlap being shed when two separate spheres merge into one more efficient geometry:

```
M_grad,1 + M_grad,2 − M_grad,final = 3 M☉
```

Modeling `M_grad = k · M_core^(2/3)` (a surface/volume-scaling exponent) and solving for the single ratio `k` that makes this partition consistent for GW150914's reported masses (36, 29, 62 M☉) gives:

```
k ≈ 0.8524572447
M_core,1 ≈ 28.118 M☉   M_core,2 ≈ 22.255 M☉   M_core,final ≈ 50.373 M☉
```

**This k is a calibration, not an independent prediction** — see §13.

### Blind prediction: testing the frozen k against held-out mergers

Since k was fixed once from GW150914, the honest next step is a real prediction test: freeze k, apply the identical two-step rule (solve each initial mass for its core via `M = C + k·C^(2/3)`, add the cores, recompute a new gradient shell on the combined core via the same relation, read off the predicted final mass and radiated-energy fraction `ε_GW = 1 - M_f/(m1+m2)`) to real, independently-published masses for other mergers, and compare against their real, independently-measured remnant masses — no refitting per event.

Four real GWOSC/published events were tested this way, using real observational data (not simulated):

| Event | q = m2/m1 | Relative deviation in predicted ε_GW | Result |
|---|---|---|---|
| GW170814 | 0.83 | **−0.3%** | Strong hit |
| GW151226 | 0.53 | +41% | Miss |
| GW170608 | 0.69 | +48% | Miss |
| GW190412 | 0.28 | +47–50% (checked across two self-consistent parameter sets) | Miss |

**What this shows:** the frozen rule transfers with real precision near its own calibration regime (GW150914's mass ratio ≈0.86, GW170814's ≈0.83) and fails by a large, consistent margin (41–50%) everywhere else tested. That's a structured, repeatable pattern — not noise — and it rules out total mass as the organizing variable outright (GW190412 has high total mass, similar to the calibration event, and still misses badly). It does **not** yet establish that mass ratio itself is the missing variable: GW190412 also has a real, nonzero effective spin (χ_eff≈0.25, primary spin 0.22–0.60), so mass ratio and spin are confounded in this small sample and haven't been separated. That requires events that vary q and spin independently — not yet done.

**Known limitations of this specific test, to fix before treating the q-pattern as a real derivation target:**
- Every row must use source-frame m1, m2, and M_f from *one* self-consistent release/catalogue version — a first pass on GW190412 mixed the discovery-paper masses (30.1/8.3) with a later GWOSC-catalog remnant mass (35.6, measured against different progenitor masses, 27.7/9.0) and got a nonsense result (the deviation sign flipped depending on which mismatched pair was used). Caught and redone against the paper's own matched Table II value (M_f=37.3) before trusting it.
- ε_GW here is computed from published marginal median masses, not from posterior samples — subtracting independent marginal medians doesn't guarantee event-by-event mass conservation the way computing ε directly from posterior draws would. The current numbers are a legitimate first pass, not the fully rigorous version.
- Two catalogue versions for the same event (as used for GW190412) are a robustness check across analysis pipelines, not independent confirmation — they share the same underlying strain data and related waveform models.

**Not yet justified by this data, and not to be claimed until the posterior-level version below is done:** that mass ratio causes the failure; that spin causes the failure; that any specific PWC mechanism (e.g. an asymmetric-displacement/"wake" picture) is proven; that the rule predicts a hard equal-mass boundary; or that three first-pass misses independently establish a law. The sample is small and q/spin covary across it.

**The actual next validation layer** (not done tonight): pull one posterior-sample release per event, compute `ε_i = 1 - M_f,i/(m1,i+m2,i)` sample-by-sample from jointly-associated draws (not by subtracting independent marginal medians, which doesn't preserve event-by-event mass conservation), and report the frozen prediction's percentile within that posterior distribution — not just its distance from a central value. If GW170814 stays compatible while the other three stay materially high under that stricter test, the regime boundary is real and becomes a genuine derivation target.

**Stop-point summary:** the fixed GW150914-calibrated release rule transfers almost exactly to GW170814 but overpredicts first-pass central energy efficiencies by ~41–50% for GW151226, GW170608, and GW190412. These are internally consistent catalogue-level comparisons, not yet joint-posterior tests. No physical correction (q-dependence, spin term, or otherwise) should be added to the model until the posterior-level validation above is complete.

### First asymmetry-correction attempt — rejected as a universal rule

This is an **unfitted diagnostic calculation**, not a candidate law or partial confirmation. To test whether the frozen rule was missing a purely volumetric symmetry factor, one parameter-free candidate was evaluated: `S(q) = 2q/(1+q)`, `q = m2/m1`, derived from the ratio of the smaller core's volume to the combined volume of two equal-density cores. Applied without refitting, as `ε_corr = S(q)·ε_frozen`:

| Event | q | S(q) | ε_frozen deviation | ε_corrected deviation |
|---|---|---|---|---|
| GW170814 | 0.83 | 0.907 | −0.3% | **−9.6%** |
| GW151226 | 0.53 | 0.691 | +41.2% | −2.4% |
| GW170608 | 0.69 | 0.817 | +47.8% | +20.8% |
| GW190412 | 0.28 | 0.432 | +46.7% | **−36.6%** |

It improves the GW151226 comparison substantially, but fails as a universal correction: it degrades GW170814 from a near-exact match to a real deviation, leaves GW170608 still off, and overcorrects GW190412 hard enough to flip its sign. **A simple correction proportional to the smaller core's share of combined volume is rejected.**

Constraint this exposes: any future asymmetry function must satisfy `S(1)=1` and stay close to unity through the near-equal-mass regime GW150914/GW170814 occupy — it cannot be a direct global multiplier proportional to `2q/(1+q)`. Stated precisely: **if mass ratio is the dominant missing variable, the data disfavor `S(q)=2q/(1+q)` as a universal multiplicative factor** — not the stronger, unsupported claim that the correction must be flatter near q=1 and steeper toward q=0 in general, which assumes q is confirmed as the relevant variable when it isn't yet (spin is still confounded with it). Whether GW170814's −9.6% counts as a formal failure depends on a tolerance and posterior uncertainty that haven't been declared yet — it's a real degradation from near-perfect, not yet a declared miss.

No new symmetry function should be tried against these same four points until the posterior-sample audit above is done — doing so risks shaping a formula to pass exactly the data used to reject this one.

### GW190412 posterior-level stress test — frozen rule rejected for this event

This is the actual posterior-level validation the limitations above called for, completed for one event. Using all 23,984 released joint posterior samples from the real GW190412 source-properties release (`GW190412_posterior_samples_v3.h5`, `combined` group — downloaded from LIGO DCC, no resampling or subsampling), the observed radiated-energy efficiency was computed sample-by-sample as `ε_obs,i = 1 - M_f,i/(m1,i+m2,i)`, using each sample's own jointly-associated `mass_1_source`, `mass_2_source`, and `final_mass_source` — not independent marginal medians. The frozen GW150914-calibrated rule (k unchanged) was evaluated on the same joint mass draws.

| Quantity | Median | 90% credible interval |
|---|---|---|
| Observed ε_obs | 0.0293 | [0.0245, 0.0364] |
| Frozen prediction ε_pred | 0.0421 | [0.0372, 0.0486] |

The frozen prediction exceeds the observed efficiency in 100% of paired posterior samples. Its median lies at the 99.7th percentile of the observed efficiency distribution. The 90% credible intervals overlap only over a narrow numerical range — just 2.6% of predicted-efficiency samples fall within the observed 90% CI. **The one-constant GW150914-calibrated release rule is rejected for GW190412 under this posterior-level comparison** — strong posterior separation under the adopted event-inference model, not a frequentist p-value or an independent replicated detection, but no longer a weak table-median artifact either.

This result does not identify the missing physical variable — GW190412 has both a strongly unequal mass ratio and nonzero spin, so the miss may reflect mass ratio, spin, their coupling, or another missing merger-state variable. It does not validate any specific PWC mechanism (wake/drafting or otherwise), and it does not establish that the rule fails for all unequal-mass mergers — one event, rejected at the posterior level.

**Still incomplete:** the same test for GW151226, GW170608, and GW170814. The downloaded GWTC-1 posterior release for those three (`GW151226/170608/170814_GWTC-1.hdf5`, verified real files from LIGO DCC) contains detector-frame masses and spin parameters but no jointly-paired final-mass field. Completing this requires either a compatible remnant-property sample release or an independently verified numerical-relativity remnant-mass fit — no unverified formula has been substituted to fill the gap.

---

## 9. Thermal-Web Rules

Temperature matters because the universe is a real medium — heat is not an incidental label applied to matter in a void, it's part of the state and dynamics of the medium.

- **Reactions and matter transfer energy outward** — where reactions occur, energy and heat are carried outward into the medium; entropy pushes energy from matter into the entropic medium.
- **Expansion requires room** — energy needs physical room to spread; making that room is itself thermally active, not instantaneous.
- **Heat drives expansion** — heated regions expand into progressively less-dense layers, spread over more area, lose concentration, and cool.
- **Cooling stiffens the medium** — as energy spreads farther it super-cools and stiffens, eventually constraining further outward progress.
- **Thermal-web heat chokes** — a heat choke is a high-pressure, low-density region produced when expanded heated flow rises into denser, cooler medium; penetration and spreading are rate-limited, the flow cools, may freeze/stiffen, and falls back down.
- **Recurring cycle**: `reaction/heat → expansion → spreading → cooling → stiffening/freezing → fallback → reheating/rising`.
- **Confinement expands rather than simply fails** — rising thermal pressure doesn't necessarily rupture a container; the system can expand into a wider thermal web until enough surface area exists to act as a heat sink.
- **Matter and entropy spread differently** — higher-entropy material spreads farther through the medium; matter can sink, reboil, rise, and cycle until incorporated into the medium.

Described via analogies to water-vapor/hydrogen-vapor phase behavior, while remaining a proposed medium-level mechanism rather than ordinary weather physics.

---

## 10. Galaxy-Scale Gravity

High gravity draws in and compresses more of the cosmic lattice/energy medium. The galaxy then behaves as if it has more effective gravitational weight, producing lensing and cohesion effects without a separate unseen dark-matter particle inventory.

```
galactic mass/energy → medium compression and density increase → pressure shadowing and altered propagation → enhanced effective cohesion/lensing
```

"Pressure shadowing" and a denser, cold medium are proposed as mechanical contributors to galactic cohesion, treated as Casimir-like effects dependent on the medium's local temperature and density. (This connects to the separate, more detailed galaxy-rotation-curve mechanisms — shadowing/pressure-asymmetry, no-shadowing-at-the-outer-edge, and the temperature-density mechanism — worked through in the companion medium-mechanics debate; those remain quantitatively unresolved against ordinary hydrostatic-equilibrium compression.)

---

## 11. The Unified Rule Set

1. The universe is a physically real, continuous birefringent energy medium.
2. Space is never physically zero-content.
3. Matter, photons, neutrinos, radiation, pressure, heat, and gravity are finite nonzero states or modes of that medium.
4. A photon's zero invariant/rest mass does not mean zero energy, zero momentum, zero gravitational role, or nonexistence.
5. No real physical system reaches literal zero size, infinite density, infinite velocity, infinite temperature, or an undefined singular state.
6. Energy is conserved and must remain physically accounted for through propagation, compression, phase/state change, expansion, waves, radiation, or thermal transfer.
7. Gravity is medium compression/stress/density response around energy and matter, with spherical geometric spreading yielding inverse-square-like weakening.
8. The medium propagates gravitational waves as phase/tension disturbances; merger radiation is a geometric structural snap between merging stress points.
9. Maximum compression is finite; collapse reaches a yield boundary and transitions rather than becoming singular.
10. Black holes are finite compact medium/matter structures, not infinite holes or zero-radius points.
11. Heat and entropy change the medium's state; thermal gradients drive expansion, spreading, cooling, stiffening, heat chokes, and fallback cycles.
12. Temperature- and density-dependent medium behavior influences propagation, pressure shadowing, Casimir/shadow effects, galaxy cohesion, and lensing.
13. The theory must not solve a gap with timelessness, literal void, infinite continuation, or an undefined placeholder transition.
14. The physical test is whether one fixed finite-medium rule set reproduces known gravitational-wave, lensing, galaxy, thermal, and conservation observations while making predictions that standard models do not.

---

## 12. The GW150914 Diagnostic Program

`pwc_gw150914_pipeline.py` (companion file) runs a theory-neutral extraction pass on the real H1/L1 GWOSC strain data, then overlays a PWC-parametrized model on top. It deliberately keeps two things separate:

**Empirical / theory-neutral extraction** (no GR waveform template used anywhere in this stage):
- H1–L1 causal cross-correlation lag, capped at ±10 ms (the light-travel-time bound between the two sites) — confirms a coherent structure crossed the Earth at ≤c.
- A local background z-score for that lag peak, built from off-source 100 ms windows that explicitly exclude the event itself.
- A Q-transform ridge trace `f_ridge(t)` — the loudest time-frequency track — extracted with a **MAD-based robust noise floor**, not a hand-tuned frequency-sweep filter (see §13 on why that distinction matters).
- A normalized excess-power envelope `P_d(t) = Σ_f power(f,t) · Δf`, an energy-shape proxy, explicitly *not* a calibrated physical energy.

**PWC-specific model layer**, fit on top of those empirical targets:
- The `M_core`/`M_grad` conservation solve from §8 giving `k ≈ 0.8524572447`.
- A toy radiation-loss sandbox, `df/dt = κ·f^α`, integrated with `scipy.integrate.solve_ivp` and compared against the empirical ridge and `P_d(t)` — this is where a real PWC equation of state `P(ρ,s)` would eventually have to plug in, replacing the placeholder κ/α values.

---

## 13. Status — What's Confirmed vs. What's Still Fitted

Kept honest and short, in the same style as the rest of this project's tracking (see `cosmology/unified_framework_consolidated_2026-08-13.md`):

- **The single biggest open item: what makes the medium push at cosmic scale when it pulls everywhere else.** Galaxy-scale gravity (§10) and the SPARC result both depend on the medium compressing/attracting around mass. Cosmic acceleration needs the opposite — something pushing space apart. Two candidate mechanisms have been proposed and checked: heat/reaction-driven expansion (§9) and knot-untying (§5) both ultimately run through stellar fusion, whose rate is tracked by cosmic star-formation history — tested directly against real Pantheon+ data, no support (dark-energy w stays flat while star-formation rate changes 4× over the same span). A third candidate — black holes absorbing/redistributing the medium itself — is real and measurable (the GW150914 merger mass deficit is exactly this, measured), but whether the *aggregate* total across all mergers in cosmic history is large enough, and has its own rate-history distinct from star formation, hasn't been calculated. Until one of these (or a new one) survives a real check, this is the one thing standing between "replaces dark matter" (done — see the SPARC note below) and "replaces dark matter and dark energy" (not done).
- **Whether "tight/not-tight" is ever genuinely undetermined, or always definitely one or the other.** The knot's binary state is real discreteness (§5) — that's settled. What's still open is whether a knot can be in a genuine superposition of tight and not-tight simultaneously (the way real quantum systems can be), or whether it's always definitely one or the other, like a classical switch. That distinction is what would separate this from an ordinary classical discrete system — untested either way.
- **The uniform-untying picture (§6) trades a simpler story for a working one.** It rules out a single localized "our universe" bubble sitting in a larger reservoir — that version doesn't match the isotropy of what's observed. The everywhere-at-once version does, but it means there's no literal "outside" left to ask about.
- **`k ≈ 0.8524572447` is a calibration, not an independent prediction — but it has now been blind-tested on four held-out mergers (§8), with a real, structured result.** Frozen, unmodified, applied to real published masses for GW170814, GW151226, GW170608, and GW190412: it predicts GW170814's radiated-energy fraction to within 0.3% (relative), and misses GW151226, GW170608, and GW190412 by a consistent 41–50%. That's a genuine domain-of-validity finding — the rule works near its own calibration mass ratio (q≈0.83–0.86) and fails elsewhere — not proof the mechanism is right or wrong. Mass ratio and spin are confounded in this small sample (GW190412 has both low q and real spin) and haven't been separated; the ε_GW numbers used are first-pass marginal-median calculations, not the more rigorous posterior-sample version. See §8 for the full table and the version-mismatch bug that was caught and fixed before trusting the GW190412 row.
- **The `df/dt = κ·f^α` sandbox has not been fit to the real ridge data.** In the working session it was only run with placeholder test values (κ=120, α=2.0) to prove the plumbing works, not to test the theory. Fitting α/κ against `clean_ridge_t`/`clean_ridge_f` is the actual next step, not something already done.
- **Use the MAD-based ridge threshold, not a hand-tuned monotonic sweep filter.** An earlier script variant (`phase_wave_master_compiler_v3.py`) replaced the MAD/robust-noise-floor threshold with a manually bounded frequency-sweep heuristic (`0.85× ≤ f ≤ 280 Hz` step acceptance). That's a regression against this project's own "no placeholders" rule — a hand-tuned acceptance window can shape the ridge toward whatever curve looks right, rather than letting the noise floor decide what's signal. `pwc_gw150914_pipeline.py` uses the MAD version.
- **The 1/r² "reinterpretation" (§2) is currently a re-reading of the existing inverse-square law, not a distinguishing prediction.** It explains why Newtonian gravity still works under PWC, but by design it reproduces the same functional form GR/Newton already give — the place to look for a genuine PWC-vs-GR difference is where the finite-medium mechanics predict something inverse-square gravity doesn't (e.g., the maximum-compression yield behavior in §3, or the core/gradient split in §8). `cosmology/sparc/` fit a galaxy-scale phenomenological response law motivated by this mechanism against 132 real SPARC rotation curves, with the key exponent (n=1/2) *forced* by the flat-rotation-curve requirement itself, not chosen — the **pooled, in-sample** scatter (0.138 dex) lands within 0.0055 dex of the best published empirical relation (McGaugh RAR, 0.133 dex). That specific pooled number is not the right one to quote as "PWC's performance," though: a proper galaxy-level 70/30 train/holdout test (fit on 104 galaxies, blind-scored on the other 45, never touched during fitting) put McGaugh's holdout scatter at 0.130 dex against PWC's 0.139 dex — a real, if modest, ~7% deficit on genuinely blind data, not the ~4% the pooled number suggests. The dwarf-spheroidal out-of-sample test (41 real Local Group dSphs, zero new tuning) is real and significant (Spearman ρ=0.74, p=2.5×10⁻⁸) but with substantial scatter (0.253 dex) and several individual galaxies off by a factor of several. Net: the empirical response law is real and competitive, not yet decisively better than the empirical benchmark it's compared against — that's a claim about the fitted law, not about the PWC mechanism itself, which (see next item) still lacks the derived closure needed to call this a physical medium implementation rather than a phenomenological stand-in for one.
- **The galaxy-scale medium has mass and volume, but no derived budget law — this is the single largest open item under §10.** A long series of same-night tests (`domain_M` through `domain_Q` in `cosmology/sparc/`) tried to give the medium implied by §10's galaxy mechanism an actual physical accounting, in order of increasing rigor: (1) a point-mass lump from a galaxy's total HI gas mass — properly null-tested (constrained non-negative, loss-surface-scanned to rule out an optimizer-stuck artifact) and genuinely rejected, any positive amount makes the fit worse; (2) a universal, ungrounded diffuse halo profile — gives a small real holdout improvement (0.139→0.134 dex) but isn't tied to any galaxy's actual gas/heat state, so it's an existence proof, not a mechanism test; (3) a multiplicative "coupling coefficient" rescaling the existing prediction by a local heat proxy — the best holdout result found (0.134 dex, closing most of the gap to RAR) but it doesn't correspond to any real mass distribution, so it isn't physically grounded, and a 10-seed stability check showed the improvement itself isn't robust (beats baseline in 7/10 splits, loses in 3/10); (4) two independently-built, properly mass-conserved versions (spherical shell, then real disk-geometry via a validated exponential-disk basis solver) that tie the total medium mass to `ξ·M_baryonic` — both came back *worse than baseline*, not better, once the free-floating-amplitude loophole was closed. **The honest reading is narrower than either "conservation kills the mechanism" or "the mechanism is confirmed": all that's shown is that the one specific closure law tested (`M_med = ξ·M_bar`) doesn't work, not that no closure works.**
  - What's still missing, precisely, is PWC's own version of a continuity/closure system — not a proxy, not an invented proportionality:
    ```
    ∂ρ_med/∂t + ∇·(ρ_med·u_med) = S_phase
    ```
    with five pieces PWC has not yet specified: (a) the **control volume** — what physical boundary encloses a galaxy's medium (not just "the HI radius" unless PWC derives that identification); (b) the **source/phase term** `S_phase` — does stellar heat convert compact medium to expanded medium, or just redistribute it at fixed mass; (c) the **boundary flux** `J_med` — does medium flow in along cold web paths and expanded medium flow back out, and what sets the net time-averaged rate; (d) an actual **equation of state** `P_med(ρ_med, T_med, ...)` — "hot regions are locally less dense" is a direction, not yet a usable equation; (e) the **gravity/tension coupling** `g_med = 𝒢[ρ_med, P_med, u_med]` that turns a solved medium state into an actual radial acceleration. Until these five are written down from PWC's own mechanics, any galaxy-scale medium-mass test is fitting an external closure on top of PWC, not testing PWC itself.
  - Also worth being precise about: every "heat" or "brightness" proxy used in these tests (`V_disk(R)`, 3.6μm surface brightness) is a **nonlocal stellar-gravity or stellar-light signature**, not a local thermal/pressure measurement. None of tonight's tests actually tested "local heat → local medium state" as literally stated in §9 — real resolved local ISM thermal-pressure data (a real, different observable from what SPARC provides) would be needed for that, and hasn't been used here.
  - **A corrected two-component source architecture, proposed but not yet tested.** Trying to extract a real physical constant from the already-calibrated `M_grad = k·M_core^(2/3)` (§8) — treating it as a literal phase-boundary/surface-tension energy, σ·Area/c² — gives a real, computed number (σ≈1.19×10³⁸ J/m²) that fails badly at *both* reference scales tested: ~10²⁰× too large versus real nuclear surface tension, and, applied directly at a galaxy's own radius (R~5-50 kpc), it overshoots the entire observable universe's total mass-energy content by 10-11 orders of magnitude — nowhere near the ~10¹¹-10¹² M☉ actually needed to explain a flat rotation curve. Neither direction works using that literal number. The actual error this exposed wasn't the number, though — it was the architecture: forcing one boundary-area term to reproduce *all* of gravity, including the ordinary far-field 1/r² part that a ordinary mass term already handles. The corrected structure is two additive source terms:
    ```
    ∇²ψ = -(λ_vol·ρ_lock + λ_grad·a_lock)
    ```
    where `ρ_lock` (volumetric locked/condensed-medium density) sources the ordinary mass-proportional far field, and `a_lock` (a coarse-grained phase-boundary-area density) sources an additional, separate "gradient" response that may supply SPARC's low-acceleration excess. This resolves the false either/or — the volume term already gives ordinary M/r² gravity, so the boundary term doesn't have to.
  - **Before this can be fit to anything, four physical definitions have to be fixed — none of them are yet:** (1) what real baryonic quantity `ρ_lock` maps to (stellar mass, gas mass, some phase-dependent split); (2) what physically counts as `a_lock` at galaxy scale (there's no meaningful way to just count every atom's surface); (3) the coherence length `ℓ_PWC` that turns a raw density into an effective boundary-area density (`a_lock = ρ_lock/(ρ*·ℓ_PWC)`) — critically, if `ℓ_PWC` is constant, `a_lock` just duplicates the mass term and adds nothing new; it only produces a genuine SPARC-relevant effect if `ℓ_PWC` itself depends on local medium state (density, temperature, field strength), which is the real physics claim needing its own derivation, not a per-galaxy fit knob; (4) how `λ_grad/λ_vol` is fixed independently (from the medium's own EOS or an existing calibration), not tuned to make SPARC agree. Same discipline that already burned the `ξ·M_bar` tests in the item above: a floating coherence length would be exactly the same mistake in new notation.
  - **Real, computed check on whether the compact-object σ can just be reused at galaxy scale, with a real, quantified result: no.** Since Area∝ρ^(-2/3) for a fixed mass, using each star's own real physical density (~1410 kg/m³, verified by reproducing the actual solar radius to 0.01%) rather than ρ_max gives ~4.74×10⁹ times more implied boundary area than treating stars as ρ_max cores — confirmed by direct computation. Applying the compact-merger σ≈1.19×10³⁸ J/m² (from §8's already-calibrated k) to a typical spiral's real baryonic mass (5×10¹⁰ M☉), divided into realistic star-sized grains at their real density, gives M_grad≈2×10²⁰ M☉ — 9-10 orders of magnitude larger than the ~10¹¹-10¹² M☉ actually needed. Coarser grains reduce the overshoot but never remove it: even treating the whole galaxy as one solid lump at stellar density still gives ~5.5×10¹⁶ M☉, still 5 orders of magnitude too large. (Using the *wrong*, unphysical ρ_max density for the star grains would have coincidentally landed near the right ballpark, ~4×10¹⁰ M☉ — a real, tempting trap, and exactly why the number must not be tuned by picking whichever density assumption makes it look right.) **The conclusion this actually supports: `M_grad=k·M_core^(2/3)`, calibrated at compact-object (nuclear) density, cannot be validly summed over arbitrary galaxy-scale grains using that same fixed coefficient — the regime mismatch is real, not just under-refined.** What's missing is the state-dependent stress law itself (σ, or its equivalent, as a function of local density/phase) — not a better grain-size guess.
  - **The real reason grain-counting was the wrong kind of object, stated precisely:** a legitimate replacement isn't a better grain size, it's a genuine local field-theoretic energy density `u_grad(φ, ∇φ, ρ_med, T_med, ...)` integrated over the actual continuous field configuration — that construction is automatically coarse-graining invariant, because it's a real functional of a smooth field, not a sum over an arbitrarily-chosen discretization. "Divide the matter into N grains and sum each one's boundary area" is not such an object — it has no physical referent for what counts as one grain, which is exactly why the answer swung by four orders of magnitude on grain-size choice alone in the test above. That swing isn't a numerical-resolution artifact to be refined away; it's the signature of an unphysical prescription. **Concrete test any future candidate must pass before touching SPARC data at all:** halving the resolution of whatever grid represents a galaxy's mass distribution must leave the predicted total `M_grad` unchanged. If it doesn't converge as the grid is refined, it's disqualified before it's ever compared to real data.
  - **The candidate that gives §3's "soliton knot" language an actual mathematical realization:** a phase-field (Ginzburg-Landau-type) functional, `E[φ] = ∫d³x[(K/2)|∇φ|² + (λ/4)(φ²-φ₀²)² - J(x)φ]`, field equation `-K∇²φ + λφ(φ²-φ₀²) = J(x)`. This is automatically coarse-graining invariant (it's a genuine integral over a continuous field, not a grain sum), and for a thin spherical domain wall of thickness δ and phase contrast Δφ, the gradient energy works out to `E_grad ≈ 2πK(Δφ)²R²/δ` — **verified correct**, and R∝M_core^(1/3) at fixed core density makes this ∝M_core^(2/3), the same exponent already calibrated in §8. Precise about what this does and doesn't establish: **it derives the 2/3 scaling conditionally (if K, Δφ, δ, ρ_core are fixed), not the calibrated coefficient k=0.8524572447 itself.** The coefficient works out to `k_theory = [2πK(Δφ)²/(δc₀²)]·(3/4πρ_core)^(2/3)`, which must emerge from independently specified PWC quantities — it has not been shown to equal 0.8524572447 from anything but the already-known GW150914 calibration. `K=c₀²` isn't dimensionally complete on its own; a valid closure for dimensionless φ is `K=ρ_ref·c₀²·ℓ₀²`, illustrative dimensional closure, not yet a derived PWC value.
  - **A real physics gap in the functional as stated, not a minor omission: it has no stabilization mechanism.** A pure gradient+double-well functional gives E_wall∝R² with dE/dR monotonically increasing from R=0 — no stationary point except collapse to a point. This is the standard content of Derrick's theorem: static, finite-radius solitons don't exist from gradient+potential terms alone in 3+1 dimensions. Something has to be added to get an actual stable knot rather than a wall that either collapses or expands without bound — a conserved phase charge/medium inventory, a pressure difference between phases, a volume term, rotation/vorticity, or a fixed source J(x). This is exactly where §3's "maximum compression" and finite medium-inventory language has to enter mathematically, not an optional add-on.
  - **Required order of operations, all parameters frozen at each step, no refitting to make later steps agree — and step 1 is four binary pass/fail tests, not a search for values that reproduce k:**
    | Test | Pass condition |
    |---|---|
    | Existence | The functional (with its stabilizing term) admits a finite, nonsingular radial configuration at all |
    | Stability | That configuration is a genuine energy minimum (dE/dR=0, d²E/dR²>0) — not a wall that shrinks or expands |
    | Scaling | A controlled range of source/inventory values yields E_grad∝R² in the saturated-wall regime |
    | Resolution | E_grad, R, and wall width converge under grid refinement (Δr, Δr/2, Δr/4) |

    Only after all four pass should the question of whether a PWC-derived parameter set predicts k_theory=0.8524572447 even be asked. After that: (5) build a real galaxy disk source J(R,z) from actual SPARC Σ_baryon(R); (6) derive the actual stress-to-acceleration map g_R(R)=𝒢[φ,∇φ] from the same field equation; (7) only then compare to SPARC, with every parameter fixed from the earlier steps, none refit to make step 7 look good.
  - **Step 1 executed (full record: `knot_audit/RESULTS.md`, `knot_solver.py`) — Pass 1 (existence) fails for the entire declared parameter space.** Built as a proper two-point BVP (`scipy.solve_bvp`, inventory constraint enforced via an augmented state variable, not a hand-rolled shooting method). The reference case (K=1, B=10, C=0.1, Λ=1, N_target=1) converged, but to a delocalized solution — direct energy comparison against explicit localized trial profiles confirmed the delocalized state is genuinely lower-energy, not a solver artifact. A follow-up 36-case phase scan over B/K∈{0.1,1,10,50}, C/K∈{0.01,0.1,1}, Λ/K∈{0.1,1,5} first showed 6 "localized" cases — self-caught as a truncated-search-range artifact (all 6 had their best radius sitting at the edge of the tested grid) and corrected: widening the range confirmed all 6 also keep improving with more spread, no interior minimum anywhere. **No combination in this scan supports a stable localized knot.** Diagnosed why: nothing in `E[n,φ] = ∫[K/2(∇φ)² + Λφ²(1-φ)² + B/2(n-n0-Δnφ)² + C/2(∇n)²]` penalizes spatial extent itself — the fixed inventory can always be diluted over an arbitrarily large region at vanishing amplitude more cheaply than concentrating it into a knot, which must pay the double-well barrier crossing. The conserved-inventory constraint alone is not sufficient stabilization — a genuine volume/pressure penalty term is still missing, which is what §3's "maximum compression" language would need to supply mathematically before this functional can support a real knot. Passes 2-4 were not run — they require an actual localized solution to test, which none of the 36 tested parameter combinations produced.
- **(Detail on the top item)** knot-untying and heat-driven expansion collapse to the same claim because both run through stellar fusion — see the top item above for the full reasoning and the specific decoupling condition that would save it.
- **The GW150914 pipeline's z-score is a local diagnostic, not a detection significance.** With only a handful of 100 ms off-source chunks in a 4-second window, treat it as "is the lag peak locally distinguishable from nearby noise," not as a rigorous multi-sigma detection claim.
- **The buoyancy/squeeze mechanism in §4 is not a separate assumption needing its own justification.** Same substance, same mass, different density by phase — exactly like liquid water and water vapor — is ordinary phase behavior, not a special case that needs proving before it's allowed. The actual open item is the same one already listed for the GW150914 model layer above: nobody has yet written down the medium's real equation of state, P(ρ,s), that this phase behavior (and the rest of the theory) would run on. That's one open item, not a new one specific to §4.
