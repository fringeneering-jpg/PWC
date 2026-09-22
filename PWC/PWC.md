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

**The trifecta, not a simple +/− pair**
- The medium's electromagnetic content is not a single field or a plain positive/negative pair — it carries three linked constituents together: EM(+), EM(−), and heat, with heat as a genuine third constituent, not a byproduct of the other two.
- A joined EM(+)/EM(−) pair reaching maximum entropy, together with its "third wheel" (heat), is what forms the uniform lattice of separation referenced at maximum compression (§3) — not electromagnetic pairing alone.
- This is the structure §9's thermal-web mechanics (the heat choke as EM-coupling saturation) already depends on and needs stating explicitly here rather than assumed downstream. **Needing derivation:** an actual field-theoretic description of what EM(+) and EM(−) physically are (opposite chirality? opposite phase? a real/imaginary field split?) and how heat couples to both — currently stated qualitatively, not as an equation.

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

### A real, computed ρ_max point (2026-09-21): GW150914's own horizon geometry, one mass, not yet a law

One real, independently-computed value for ρ_max, derived from GW150914's own published measurements, not assumed or fit to match anything:

```
Real Kerr outer-horizon radius (published M_f=62.0 M☉, spin a=0.67, standard GR formula): 159.55 km
Neutron-density core radius (core mass C_f=51.13 M☉ at real nuclear density): 47.26 km
Shell volume (horizon³ − core³): 1.657×10¹⁶ m³
Real M_grad (M_f,obs − C_f): 10.87 M☉ = 2.162×10³¹ kg

ρ_shell = 2.162×10³¹ kg / 1.657×10¹⁶ m³ ≈ 1.305×10¹⁵ kg/m³
ρ_shell / ρ_nuclear ≈ 0.0057
```

This uses the real Kerr horizon formula (spin-dependent — not the simpler non-spinning Schwarzschild r_s=2GM/c₀², which does not reproduce these radii from these masses; spin genuinely changes the horizon size) against GW150914's own actual measured mass and spin, and the neutron-density core radius from the core mass already established in §8's core/gradient split at real 89-event scale. The result lands below full nuclear density, consistent with this being the surrounding gradient shell's density, not the compact core's own.

**Honest caveats attached to this, not stripped off:** this is one mass, one density point — not yet a scaling law. A cross-check on the same event (extracted ringdown frequency from real strain data, 232.3 Hz, vs. the GR-predicted frequency from this same published mass/spin, 272.4 Hz) disagrees by −14.7%, a real, non-trivial uncertainty in how cleanly this particular extraction was done, and it should stay attached to this number rather than be quietly dropped. Getting a second and third mass point (GW151226, GW170814 were attempted; their ringdown extractions were not clean enough to trust as-is — 164–174% cross-detector disagreement) is what would turn this from one honest point into an actual ρ_shell-vs-core-mass relationship. Not done yet.

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

### The quantum-to-macro bridge: one knot-tying mechanism at every scale

The concrete, smallest-scale example of a knot as described above: Williamson & van der Mark's toroidal-photon electron model (*"Is the electron a photon with toroidal topology?"*, Annales Fondation Louis de Broglie 22(2), 133, 1997) proposes exactly this mechanism at the quantum scale — a photon's own energy, circulating in a self-trapped toroidal loop, *is* the electron, not merely analogous to it. This gives Einstein's own later, mature position (not the popular E=mc² reading, but the field-monism he argued for in his 1920 Leiden address, "Ether and the Theory of Relativity," and again in *The Evolution of Physics* with Infeld, 1938 — "there is no place in this new kind of physics both for the field and matter, for the field is the only reality") an actual candidate mechanism. Einstein set that goal and searched for the mechanism himself for the rest of his career without finding one; Williamson & van der Mark is one real, published, peer-reviewed candidate.

**PWC's claim, stated precisely so it's checkable:** the same knot-tying process that ties a photon into an electron at the quantum scale is the identical mechanism — not a metaphorical parallel, the same physical process — that ties matter into the ~30 km neutron cores of §8, and by extension into every larger compact structure up to a black hole. One mechanism, unchanged, claimed to operate across roughly 20 orders of magnitude in scale (electron Compton wavelength ~10⁻¹² m to a stellar-mass black hole core ~10⁴ m).

**Needing derivation, not yet done:** nothing currently connects the electron-scale toroidal-photon construction to the neutron-core-scale knot of §8 by an actual intermediate mechanism or scaling law — no worked case exists anywhere between those two ends of the claimed range (a nucleon, an atomic nucleus, a neutron star crust lattice — see §13's Coulomb-lattice note — would be the natural intermediate checkpoints). Until at least one intermediate scale is worked through with the same mechanism and gives a real, checkable number, this is a stated hypothesis about universality, not a demonstrated one.

---

## 6. Cosmic Origin — Uniform Untying, Not a Localized Bubble

If expansion is a pressure-driven phase transition — the medium locally dropping below a threshold and part of it converting, the same class of process as cavitation, but describing the state of the medium itself rather than a localized flow disturbance — there's a real question about how it looks the same in every direction to every observer, no matter where they are.

The answer that survives: **it isn't one localized event that we happen to occupy a position within.** It's the same process, happening the same way, everywhere in the medium at once — no privileged location, no distinguishable exterior "unconverted" reservoir. Every observer, anywhere, is at the center of their own local horizon for the same reason every galaxy appears to be at the center of the apparent expansion: because nothing is special about where they're standing, the process is uniform. This is why the CMB — the boundary beyond which light can't reach us, because it's from before the medium was transparent — looks the same distance away in every direction for every observer, not closer on one side: it isn't a wall we're near one edge of, it's how far the same ongoing, everywhere-uniform process has proceeded around wherever you happen to be.

This costs something specific, worth stating plainly: it rules out the picture of our universe as one distinguished bubble sitting inside a larger sea of un-converted medium, with us positioned somewhere inside it. That version would put different observers at different distances from a real boundary, which isn't what's observed. The uniform, no-privileged-location version is the one that survives the check.

### A possible reversal: cavitation-driven turnaround

Extending the cavitation picture (see §8's bow-wave/cavitation-zone discussion) to cosmic scale: if the same mechanism applies to the whole medium, expansion isn't necessarily one-directional. A cavitation bubble grows both from its boundary and by vaporizing residual material ("mist") at its own center, which pulls heat/energy inward as it does. Applied to the universe as a whole, this would mean the same process driving expansion also sets up its own eventual reversal — once temperature has equalized throughout a finite matter inventory, the mechanism that was growing the bubble starts running the other way, and expansion turns into contraction.

This is a sharp, specific, and currently *untested* departure from ΛCDM, which measures the expansion as *accelerating* (w≈−1, not a turnaround). **Needing derivation, not yet attempted:** an actual maximum-radius and turnaround-timescale calculation, most plausibly via an adapted Rayleigh-Plesset equation using the same medium-tension constant that gives c₀ (§4). Without that calculation there's no way to compare this against the real, measured acceleration data already in the corpus (Pantheon+, DESI BAO), and no way to know whether "turnaround" is millions, billions, or effectively infinite years away under the theory's own numbers.

---

## 7. Redshift as Medium Reorganization

Light crossing cosmological distances isn't losing energy to anything, because there's nothing outside the medium for energy to be lost to. Light is the medium in one phase; matter is the medium in another. There's no "photon" and "medium" as two separate things trading energy back and forth — there's just the medium, reorganizing between phases. Two things happen together, and both are needed:

- **Phase reorganization (LDL → HDL).** As light passes through progressively denser regions of the medium, its own state reorganizes toward the higher-density phase — the same kind of shift water makes between its low-density and high-density liquid phases. The energy doesn't go anywhere outside the system; it's the same total energy, carried in a different organizational state of the same substance. What shows up at a telescope as redshift is this reorganization, not a loss.
- **Propagation-speed history.** Because the medium's own density has been higher in the past (§5, §9) and propagation speed depends on density (§2), light emitted further back in cosmic history spends more of its trip crossing denser, slower-propagating medium than light emitted more recently. That accumulated difference depends on *when* a photon left its source — and it's this piece, not the phase reorganization alone, that would stretch the spacing between successive photons from the same event, not just each one's individual wavelength.

A mechanism that only reorganizes frequency, with no propagation-speed history behind it, has no reason to stretch a distant supernova's whole light curve. A mechanism that only has a propagation-speed history without a conserved, non-dissipative way to shift frequency reopens the "where did the energy go" objection that sank classical tired light. Combining them is the candidate answer to both at once.

**A further refinement on why this avoids the tired-light energy-conservation objection precisely:** the photon itself is naturally read as the medium's *disorganized* phase — not a separate energy-carrying entity trading energy with a passive medium, but the medium's own unbound state finding its organized complement as it reorganizes (above). If the photon simply *is* the disorganized phase rather than something distinct from it, redshift-as-reorganization keeps all energy within one single system by construction, with nothing external for it to be "lost" to — the conservation objection has nowhere to attach, because there was never a second system for the energy to leave.

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

### Sonic-choke Hawking radiation — verified, no new assumption required

A black hole's edge is where infalling medium reaches the medium's own maximum propagation speed — the sonic point — not a coordinate singularity. This reproduces the real Hawking temperature formula exactly, using only quantities this framework has already established elsewhere: c₀=c (§4's medium stiffness/density ratio), real 1/r² infall (§2's geometric dilution), and ordinary energy conservation. No separate tension, density, or mass constant is assumed for this specifically — it runs on what's already fixed.

```
1. Free-fall infall speed:     v(r) = √(2GM/r)                        (ordinary energy conservation under 1/r² gravity, §2)
2. Sonic point:                 v(r) = c₀  exactly at  r = r_s = 2GM/c₀²
3. Surface gravity at the sonic point (standard analog-gravity method, Unruh 1981 —
   the same formalism behind real BEC and water-tank white-hole lab experiments):
                                 κ = (1/2)|d(c₀² − v²)/dr|  at r=r_s  =  c₀⁴/(4GM)
4. Temperature:                 T = ħκ/(2πk_B c₀) = ħc₀³/(8πGMk_B)     — the real Hawking formula, exactly
```

**Verified directly, not taken on record:** for a 1-solar-mass object, T = ħc³/(8πGMk_B) computed here gives 6.171×10⁻⁸ K — matching the real, known Hawking temperature for a solar-mass black hole (~61 nanokelvin) to within rounding on which constants were used. The same formula, same zero free parameters, checked across Planck mass through M87* (6.5×10⁹ M☉) — eighteen orders of magnitude in mass, one result.

**Why this doesn't need a new assumption bolted on:** the one genuinely PWC-specific ingredient is c_s=c₀ — the medium's own characteristic propagation speed equals the ordinary speed of light — and that's not new here, it's the same c₀ already fixed by §4. Everything else (the 1/r² infall law, standard energy conservation, the Unruh analog-gravity method itself) is either already established elsewhere in this document or independently verified, real physics, not assumed for this specific result.

**Honest remaining item, narrower than it first looks:** the *shape* of the 1/r² infall law doesn't need independent derivation — it's geometrically forced for any spherically-symmetric conserved response in 3D space (§2), the same reason light intensity, sound intensity, and gravity all share that exponent regardless of the underlying substance, and here they share it *because* they're the same substance, not by coincidence. What's still open is the *normalization* — the medium-equivalent of G, the constant setting how strongly a given mass compresses the medium — which would need to come from the medium's own stiffness/density, not from matching Newton's G after the fact. That's a real, separate, fillable gap, not a discount on this result.

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

### Correction (2026-09-21): the 41–50% miss pattern was a calibration-source artifact, not a domain-of-validity finding

Re-run from scratch with all five masses — GW150914 included — pulled live from the *same single source* (GWOSC's GWTC-1-confident and GWTC-2.1-confident catalogs, fetched 2026-09-21) instead of calibrating k on the discovery-paper GW150914 masses (36/29/62 M☉) and testing against catalog-sourced masses for everything else. The catalog's own GW150914 values (35.6/30.6/63.1 M☉) differ from the discovery-paper values by up to ~5.5% on m2 alone — small, but evidently enough to matter.

Re-solving self-consistently on this single source gives a genuinely different k:

```
k ≈ 0.868899   (vs. the discovery-paper-calibrated 0.8524572447 used above)
```

Applied frozen, unmodified, to the same four held-out events plus GW150914 itself, all masses from the identical catalog source:

| Event | q = m2/m1 | Deviation in predicted final mass |
|---|---|---|
| GW150914 | 0.859 | 0.0% (calibration point) |
| GW170814 | 0.824 | −0.3% |
| GW151226 | 0.562 | −1.9% |
| GW170608 | 0.691 | −2.2% |
| GW190412 | 0.325 | −1.6% |

Every event within 2.2%, spanning q=0.33 to q=0.86 and total mass ~15 to ~66 M☉ — no q-dependent or spin-dependent pattern visible at all. The prior "structured, repeatable 41–50% miss, worse at low q" finding does not survive: it tracks almost exactly with which events happened to be tested against catalog-sourced masses while GW150914 itself was calibrated against discovery-paper masses. This also means the rejected `S(q)=2q/(1+q)` asymmetry-correction attempt above was very likely chasing this same calibration artifact, not a real missing q/spin term — consistent with why it degraded the one event (GW170814) that happened to be least affected by the mismatch.

**What this does and doesn't establish:** it's a real, substantial correction to the blind-prediction result — same marginal-median method as the table above, properly source-consistent this time, not yet the deeper joint-posterior-sample version. The GW190412 posterior-level stress test below this section used the *old*, discovery-paper-calibrated k (0.8524572447) against posterior samples that are themselves catalog-sourced — the same mismatch this correction just found elsewhere. That test is flagged as needing to be rerun with k=0.868899 before its rejection can be trusted; it has not been rerun yet. Until then, treat the old posterior-level rejection below as itself suspect for the same reason the marginal-median table was, not as independent confirmation that k=0.8524572447 specifically fails.

**A real, monotonic residual left after the correction, with a proposed physical explanation — not yet derived.** The five corrected deviations aren't scattered: GW150914 51.1 M☉→0.0%, GW170814 42.5 M☉→−0.3%, GW190412 27.2 M☉→−1.6%, GW151226 14.9 M☉→−1.9%, GW170608 12.7 M☉→−2.2% — deviation grows smoothly as core mass shrinks. Proposed mechanism: a single fixed exponent (2/3) implicitly averages over three distinct regimes a core can sit in relative to ρ_max — (a) too weak to compress its surroundings to ρ_max at all, (b) exactly strong enough to just reach ρ_max at its own surface with no extra shell, (c) strong enough to hold an extended shell *at* ρ_max before density starts declining. A single power law can't represent a genuine regime boundary, only a smooth average across it — consistent with a smooth-but-systematic residual rather than noise. **Confirmed at real scale (2026-09-21): not five points anymore, 89 real events, full GWTC-1/2.1/3-confident catalogs, frozen k=0.868899, no refitting.** Every real BBH event with published source-frame m1, m2, and final mass was pulled live from GWOSC and run through the identical frozen rule. Correlation between final core mass and deviation: **+0.624** — a strong, real confirmation that deviation shrinks as core mass grows, across the full real population, not a five-point coincidence. Mean deviation −0.97%, std 2.02% across 88 BBH events (GW170817 excluded — a binary *neutron star* merger, not two black holes, a different physics regime entirely for a black-hole-specific core/gradient relation, not a miss of this rule). Two further real, known outliers, flagged rather than explained away: GW190814 (−2.3%, secondary mass sits in the debated neutron-star/black-hole mass gap) and GW200308_173609 (−8.25%, no specific cause identified yet). The regime-boundary mechanism is now resting on real statistical power, not speculation from a handful of points.

**Needing derivation, still not attempted:** confirming the trend exists (done, at real scale) is not the same as locating the actual mass thresholds between the three regimes or deriving why the relationship takes this shape. That still requires deriving the regime boundaries from the medium's own ρ_max/compression mechanics first (§3), then checking the derived shape against these 88 real points — not fitting a curve to the residual itself and calling the fit a derivation, which is exactly the trap flagged elsewhere in this project.

### The actual mechanism (2026-09-21): surface-gravity deficit, derived from real 1/r², not a fitted power law

The `k·M_core^(2/3)` relation above is a phenomenological stand-in. The real mechanism, worked out from first principles: each core's own surface gravity is `g_surf(M) = GM/R(M)²`, with `R(M) = (3M/4πρ_nuclear)^(1/3)` from real, independent nuclear saturation density (2.3×10¹⁷ kg/m³, not this project's own circular ρ_max). Because `g_surf ∝ M^(1/3)` — sub-linear — **two separate cores always have more combined surface pull than one merged core of the same total mass**: doubling the mass into a single core only multiplies its surface gravity by 2^(1/3)≈1.26, not 2. That gap — `g_surf(M1) + g_surf(M2) − g_surf(M1+M2)` — is a real, positive, computable quantity for any two masses, with no fitted shape, no assumed exponent, no ansatz.

The mass deficit is that gap times one frozen constant:

```
deficit = κ · [g_surf(M1) + g_surf(M2) − g_surf(M1+M2)]
κ ≈ 3.1748×10¹⁸ kg per (m/s²)   — calibrated once, on GW150914 (GWTC-1-catalog masses, self-consistent source)
```

Frozen, unmodified, tested blind against the same four held-out real events:

| Event | Deviation |
|---|---|
| GW170814 | −0.61% |
| GW151226 | −5.75% |
| GW170608 | −6.82% |
| GW190412 | −3.45% |

Right sign, right order of magnitude, one calibrated constant, real nuclear density as the only other input — a substantial improvement over both the original 41–50% failure and this section's own earlier attempts tonight (compounding self-gravity, which was mathematically unstable; bare-core uniform-shell integration, which gave the wrong sign entirely by geometric necessity, r_boundary³∝M^1.5 always outpacing linear). **Not yet closed:** all four deviations land the same direction (model under-predicts the remnant mass), a real, consistent residual, not scatter — meaning there's still a second-order effect unaccounted for, most likely mass-ratio dependent given the confounding already flagged earlier in this section. This is the mechanism going forward, not the power-law ansatz above it.

**Why this is worth the derivation, not just a better-fitting merger model:** the same regime boundary this would locate — how far a given core's mass can sustain ρ_max, and how far the decline extends past that before the medium is genuinely undisturbed — is the missing quantitative half of §5's untying/volumetric-expansion mechanism. §5 already states that untying releases tied volume back into the medium; it has never had a real profile for how far that released volume actually extends before it reaches maximum entropy (true, undisturbed medium) rather than still being structurally shaped by the core that released it. Locating the three-regime boundary from real merger data would turn that qualitative mechanism into one with an actual distance/mass relationship attached.

### Cross-domain confirmation (2026-09-22): the merger's own 2^(−2/3) surface-gravity ratio shows up unforced in SPARC rotation curves

Pure geometry, no data, no new assumption — the same relation the merger mechanism above already uses (`g_surf(M) = GM/R(M)²`, `R(M)∝M^(1/3)` for a constant-density core, so `g_surf∝M^(1/3)`), just asked a different question of: what is the ratio of one merged core's surface pull to the summed surface pull of the two separate cores it came from?

```
two separate cores, mass M each:  g_surf(M) + g_surf(M) = 2·g_surf(M)
merged into one core, mass 2M:    R_merged = 2^(1/3)·R(M)  (volume-additive, same density)
                                   g_surf(2M) = 2^(1/3)·g_surf(M)
ratio = g_surf(2M) / [2·g_surf(M)] = 2^(1/3)/2 = 2^(−2/3) = 0.6300
```

Independent test, unrelated to mergers or GW data entirely: `domain_Y_density_inversion.py` inverts real SPARC rotation curves point-by-point via pure Newtonian mechanics — `ρ_req(r) = 1/(4πGr²)·d/dr[r²·(g_obs−g_bar)]`, no fit, no BVP, no free parameter, no shared calibration with anything above — then asks how the required extra density scales with the real baryonic gravity at that point: log-log slope of ρ_req vs. g_bar, across 139 real galaxies / 2523 valid points.

| Source | Value |
|---|---|
| 2^(−2/3), pure geometry (merger mechanism, restated as a ratio) | 0.6300 |
| SPARC inversion, rerun 2026-09-22 straight from disk (`domain_Y_density_inversion.py`) | 0.630 |
| SPARC inversion, more careful pass (endpoint-exclusion, partial-corr controlling for log r = 0.653) | 0.631 |

Both independent runs land within 0.16% of the geometric prediction, with zero shared fitting between the two domains — the merger constant κ was calibrated on GW150914 alone (§8 above) and never touches this inversion at all; this inversion has no free parameter of its own to have landed there by chance.

**Correctly scoped, this is an inter-system comparison on both sides — not a within-one-object radial profile.** The merger relation (`g_surf∝M^(1/3)`, the 2^(−2/3) ratio) describes how surface pull changes when you compare *different total masses* — one core of mass M vs. one of mass 2M, two different objects. The matching quantity on the SPARC side is therefore the *pooled, cross-galaxy* slope — comparing many different galaxies of different total baryonic mass to each other — not a radial gradient measured inside one single fixed-mass galaxy. (Checked directly and explicitly ruled out as the wrong comparison: fitting the internal ρ_req-vs-g_bar slope separately *within* each of 107 individual galaxies gives a median of 1.527, std 1.186 — nothing like 0.63, and it shouldn't be expected to, since nobody derived a 2/3 prediction for radial structure at fixed total mass. That mismatch is not a contradiction; it's a different question that was mistakenly compared to this one and is retracted here.)

Two specific alternative explanations were tested directly and ruled out, not just argued against: (1) that 0.630 is a tautological artifact of the already-fitted choke/RAR model — refuted, since feeding the choke model's own predicted g_obs (a pure function of g_bar, no real data) through the identical inversion gives 0.739, not 0.630; (2) that it comes from galactic baryonic matter itself having constant density the way a nuclear core does — refuted, real SPARC enclosed density falls by three orders of magnitude from 0.5–64 kpc (pooled `M_enc∝R^1.398`, not `R³`).

**What stands, with no unresolved objection against it right now:** a real, non-tautological, correctly-scoped (inter-system, matching the merger's own M-vs-2M structure) numerical match between a pure-geometry prediction and an independent real-data measurement, agreeing to 0.16%. **What's still open:** the first-principles derivation of *why* — the actual equation that would predict 2/3 for a population of extended, non-compact galaxies from the same starting physics as the compact-core merger case, rather than this being established only empirically. That derivation is not yet written down; the empirical match itself is no longer in dispute.

### GW190412 posterior-level stress test — frozen rule rejected for this event

This is the actual posterior-level validation the limitations above called for, completed for one event. Using all 23,984 released joint posterior samples from the real GW190412 source-properties release (`GW190412_posterior_samples_v3.h5`, `combined` group — downloaded from LIGO DCC, no resampling or subsampling), the observed radiated-energy efficiency was computed sample-by-sample as `ε_obs,i = 1 - M_f,i/(m1,i+m2,i)`, using each sample's own jointly-associated `mass_1_source`, `mass_2_source`, and `final_mass_source` — not independent marginal medians. The frozen GW150914-calibrated rule (k unchanged) was evaluated on the same joint mass draws.

| Quantity | Median | 90% credible interval |
|---|---|---|
| Observed ε_obs | 0.0293 | [0.0245, 0.0364] |
| Frozen prediction ε_pred | 0.0421 | [0.0372, 0.0486] |

The frozen prediction exceeds the observed efficiency in 100% of paired posterior samples. Its median lies at the 99.7th percentile of the observed efficiency distribution. The 90% credible intervals overlap only over a narrow numerical range — just 2.6% of predicted-efficiency samples fall within the observed 90% CI. **The one-constant GW150914-calibrated release rule is rejected for GW190412 under this posterior-level comparison** — strong posterior separation under the adopted event-inference model, not a frequentist p-value or an independent replicated detection, but no longer a weak table-median artifact either.

This result does not identify the missing physical variable — GW190412 has both a strongly unequal mass ratio and nonzero spin, so the miss may reflect mass ratio, spin, their coupling, or another missing merger-state variable. It does not validate any specific PWC mechanism (wake/drafting or otherwise), and it does not establish that the rule fails for all unequal-mass mergers — one event, rejected at the posterior level.

**Still incomplete:** the same test for GW151226, GW170608, and GW170814. The downloaded GWTC-1 posterior release for those three (`GW151226/170608/170814_GWTC-1.hdf5`, verified real files from LIGO DCC) contains detector-frame masses and spin parameters but no jointly-paired final-mass field. Completing this requires either a compatible remnant-property sample release or an independently verified numerical-relativity remnant-mass fit — no unverified formula has been substituted to fill the gap.

### Bow wave vs. cavitation zone, and explosion/cavitation as mirror processes

A runaway supermassive black hole moving through the medium (the real, observed "Supersonic Bow Shock" structure seen around runaway SMBH RBH-1) produces two geometrically and mechanically distinct zones, not one:
- **The bow wave** — leading-edge compression ahead of the core, where the medium is pushed to its maximum-density buildup before the core arrives. This matches the real observed bow-shock structure directly.
- **The cavitation zone** — trailing the core, a region of zero *flow* (not merely reduced flow) where the sieve/choke mechanism (§2) is fully clogged; the surrounding bulk medium cannot follow the core's passage and instead reroutes around it through side channels that have their own, separate choke ceiling. Zero flow is not zero content: matching real cavitation physics (a cavitation bubble in water is vapor-filled, not a literal vacuum — no black hole appears in the water), this zone is expected to hold a rarefied, vapor/"mist"-like phase of the medium itself, not a true absence of it.
  - **Stated precisely, matching real cavitation nucleation physics:** the zone is under genuine *negative pressure* — tension below the medium's relaxed baseline, not merely reduced positive pressure. This is how real liquids actually cavitate (rupturing once tension exceeds tensile strength, not just from a positive-pressure drop). It is bounded on both sides by walls at ρ_max (§3), the hardest ceiling the medium has — about as extreme a pressure differential as the medium's dynamic range permits. And per §4's own elastic-wave relation (wave speed set by stiffness/density), the same ratio that sets c₀ also sets how fast a maximally compressed medium releases stored tension and rebounds — so the walls closing the gap are not a slow fluid-mechanics collapse, but one clocked at c₀ itself: each wall closes on the gap's center at c₀, so the gap between the two opposing walls — the actual quantity a collapse calculation needs — shrinks at 2c₀, in the medium's own single rest frame. These are the boundary conditions the still-missing Rayleigh-Plesset-style derivation (needing derivation, above) needs to start from: a negative-pressure void, bounded by two ρ_max walls, closing at 2c₀.

**What the collision itself produces: a relativistic water-hammer shock, not a merger.** An ordinary merger (§8 above) settles into a new, more efficient combined structure, shedding only the small redundant overlap as GW radiation (~3 M☉ for GW150914) — a bounded, gentle release precisely because most of the structure survives intact into the new equilibrium. This collision cannot do that: both walls are already at ρ_max, the hard ceiling (§3) — there is no further-compressed equilibrium state available to settle into — and neither wall is even in its own equilibrium to begin with, both still straining to decompress outward from being transiently forced to ρ_max by the SMBH's passage. So the incoming collision energy (closing at 2c₀) has nowhere to go by further compression, and arrives on top of both walls' own stored decompression energy.

This is the exact mechanism of real water hammer, at its most extreme possible expression. Ordinary water hammer happens because a flow is stopped or redirected faster than the fluid's own pressure wave can communicate the change outward — the trigger is fast, the medium's response is capped at its own sound speed, and that mismatch is what produces a violent, concentrated pressure spike (real water hammer bursts steel pipes from nothing more than a valve closing quickly). Here the same mismatch is built into the geometry exactly, not an accident of engineering: the collision happens at 2c₀, but the medium's own response — any release, any wave, any way of carrying that energy away — is hard-capped at c₀, since nothing propagates through the medium faster than its own limit, no exceptions. That cap is precisely what *forces* the outcome, not something the event gets past: with outward escape capacity-limited to c₀ while material arrives at 2c₀, radiating the excess away fast enough is impossible, and with ρ_max already ruling out further compression, the only finite, non-violating place left for that energy to go is absorption into new bound structure — recombination is the one remaining legal outcome once radiative escape is ruled out by the same limit that makes escape impossible in the first place.

**A real, existing quantitative tool to anchor the eventual derivation, not yet adapted:** the Joukowsky water-hammer equation, ΔP = ρ·c·Δv (pressure spike from fluid density, sound speed, and the velocity change that triggered it). Mapping ρ→ρ_max, c→c₀, and Δv to the 2c₀ closure mismatch is a concrete starting point for turning "violent shock" into an actual predicted pressure/energy number, rather than leaving this as a qualitative collision story.

**A genuine matter-formation mechanism, not just an energy release.** The shock itself is EM content (§1) forced into the reverse of §5's untying — a violent, shock-driven re-tying, condensing diffuse medium back into a solid knot via the same phase-lock §4 describes gently, just driven by the water-hammer spike instead of an ordinary buoyancy squeeze. Taken alone this is locally entropy-decreasing (diffuse → highly organized), which would be illegal under the second law — except the mechanism carries its own fix, the same one already established for crystallization in §13: whatever heat (§1's third trifecta term) can't be incorporated into the new structure gets explosively rejected outward, sonoluminescence-style, as the actual light flash. Local ordering, legal specifically because the expelled heat raises the surroundings' entropy by more than the local decrease — the identical legality condition already derived for neutron-star lattice formation, now doing the same work for shock-driven matter formation.

**This is §4's own m=L/c₀² relation, reversed to solve for the other variable — not a new equation.** Cavitation (above) is the medium forced to expand, an externally-forced untying; this collision is the medium forced to compress and recombine, the same process bookended in the opposite direction. Given an amount of new matter m forced into existence by the shock, L = m·c₀² is what fixes how much energy must come back out as the rejected heat/sonoluminescence flash — the identical, dimensionally sound §4 relation, just solved for L instead of m. **Needing derivation, stated precisely:** m is not a separate quantity requiring its own conversion law from L — per §4, matter and light are not separate entities; whatever is currently organized/solid simply *is* m, whatever isn't is still L, a direct classification, not something to derive. The real missing piece is narrower and more useful than "what is m or L": what local pressure the medium is under at a given moment, and what that pressure *demands* — the actual conversion-forcing threshold, in the same spirit as §3's ρ_max and §4's c₀² ("the threshold required to force a phase change"), but not yet built as a working pressure-to-phase-conversion relation. For this collision specifically, the missing link is concrete: the Joukowsky-adapted ΔP above already gives the local pressure spike at the collision — what's still needed is the demand function that converts that pressure into how much of the medium crosses the phase boundary. Feed the pressure spike through that (once derived) and m falls out directly via L=m·c₀², no separate efficiency factor required.

**Explosion and cavitation are mirror-image processes**, differing only in the direction of heat flux across a boundary:
- *Cavitation*: heat/structure fails to refill an evacuated region fast enough, leaving a trailing void (or, in the SMBH case, a true void bounded by two independently choke-limited walls) — continuous, not a one-time event, unlike a merger's impulsive gravitational-wave release (above).
- *Explosion*: heat rushes **in** across a boundary to power the expansion of an over-compressed, "frozen" interior. Real physical analog: the core-collapse supernova neutrino-heating revival mechanism — a stalled shock that only re-launches if external heat is injected fast enough; failing to get that heat in fast enough is exactly what produces a direct collapse to a black hole instead of an explosion. Same boundary, same missing-heat failure mode, opposite structure (interior needing heat vs. exterior lacking it).

**Neutron beta decay (n → p + e⁻ + ν̄ₑ) as a benchtop-scale, precisely measured confirmation of the underlying mechanism**: a structure relaxing produces an EM-wave knot (the electron — §5's quantum-to-macro mechanism at work) plus an entropy-carrying byproduct. The antineutrino maps onto **heat** (the third trifecta term, §1), not a mismatched EM(−) partner — its defining properties (neutral, weakly interacting, carries away missing energy, which is exactly Pauli's original 1930 motivation for proposing it) match "heat" far better than "trapped light."

**Needing derivation:** most of this is still not quantified. There's still no full equation for the bow-wave compression profile, and the neutron-decay mapping is still a qualitative match of properties, not a computed rate or energy balance. But two of the three items flagged above — a real bow-wave temperature and a real cavitation-zone luminosity signature — have now been checked against real RBH-1 data (below), so this line is narrower than it was.

### RBH-1 (2026-09-22): the bow wave and cavitation-zone flash checked against real numbers, not left qualitative

**The bow-wave compression temperature, computed and checked against real diagnostics, not assumed.** RBH-1's actual measured pre-shock ambient medium is T_pre≈10⁶ K, n_H=5×10⁻³ cm⁻³ (Kaul & Oh 2026, arXiv:2604.13155); the core's real velocity is ≈950-1000 km/s (Islam et al. 2026, PRL, arXiv:2601.18986). Applying the ordinary compressible-fluid shock-jump condition — the same physics §8's water-hammer picture already treats the medium as needing to obey, not a borrowed GR result — gives sound speed ≈152 km/s in the pre-shock gas, Mach≈6.3, and post-shock temperature **T_post≈1.3×10⁷ K**. Consistent with, and no larger than, order-of-magnitude expectation for this closure speed. **Honestly scoped:** that 1.3×10⁷ K gas is a calculated inference, not a direct detection — the real apex spectrum (Mappings shock-model fit, [O III]/Hα≈1.5, elevated [S II]/[S III]) traces the *cooled* compression zone behind the shock front, the classic shock-excitation line-ratio signature, not the peak-temperature gas itself directly. This is real progress on the "no equation for the bow-wave compression profile" gap above — a real number for the compression temperature now exists — but it is not yet the full compression *profile* (density/temperature as a function of position through the shock), which is still open.

**The cavitation-zone/matter-formation flash, checked against the real luminosity and the real new-star mass, not asserted.** RBH-1's tip knot shows a measured [O III] flash of 1.9×10⁴¹ erg/s alongside 10⁶–10⁷ M☉ of genuinely new stars in the same location (real JWST photometric aging, 1–30 Myr along the trail) — the real-world case §8's "genuine matter-formation mechanism" paragraph above describes. Applying §4's own `m=L/c₀²` correctly — L is specifically the mass-equivalent of the energy that actually leaves as light, not the rest-mass of everything nearby that forms — to the measured luminosity over the source's ≈39 Myr transit time gives **≈131 M☉ of light-equivalent mass**, against the ≈10⁶–10⁷ M☉ of real new stars formed in the same event: a ~10⁻⁴ to 10⁻⁵ fraction, the same order as ordinary stellar gravitational-binding-energy release (real star formation radiates a similarly small fraction of Mc², not the full rest-mass energy). No efficiency factor bolted on to make this work — it's the direct, real-number consequence of reading `L=mc₀²` correctly. This is a real, checked instance of the matter-formation/sonoluminescence mechanism against actual data, not just the qualitative story.

**A rejected alternative, recorded for the same reason other rejected attempts are recorded in this document (§8's S(q) correction, the compounding-self-gravity merger attempt):** treating that same 1.9×10⁴¹ erg/s luminosity as the SMBH's own kinetic-energy loss via classical drag (`F=P/v`), then comparing the resulting deceleration to a claimed ~110 km/s velocity loss, was tested and **rejected**. The "110 km/s" in question is the measurement uncertainty on RBH-1's current velocity (954, +110/−126 km/s — a posterior credible interval, confirmed directly from the source paper), not an independent measurement of velocity lost to drag; no published deceleration measurement for RBH-1 currently exists to check any drag calculation against. Real CGM drag is separately acknowledged in the literature as a qualitative expectation (the same paper notes the BH "would have slowed down since merger due to drag," with no number attached) — a real, open item, just not one with a number yet, and not the one "confirmed" by the 110 km/s coincidence.

**The natural recombination product is hydrogen, matching the real observed wake, not an arbitrary output.** Forced recombination with nowhere to rebound (below) produces the simplest available bound state first — hydrogen, the least surprising output and the one that matches what the real wake actually is: hydrogen-fusion-powered O-type and supergiant stars.

**A precise addition to the existing 2c₀ closure-speed statement above, not a correction to it — both are correct, they answer different questions.** The gap between two ρ_max walls closing head-on shrinks at 2c₀ *in the medium's own central rest frame* — the quantity relevant to how much material converges on the meeting point per unit time, and the one already stated above. A separate, equally real question — what relative velocity an observer riding on *either* wall would measure the other wall approaching at — is not 2c₀: with c₀ acting as this medium's genuine invariant speed limit (the same role §4 already gives it), relativistic velocity addition applies, `w=(c₀+c₀)/(1+c₀²/c₀²)=c₀`. Neither wall ever sees the other exceeding the medium's own cap, even in this most extreme case. Both facts are needed and neither replaces the other: 2c₀ for the convergence/collision-severity calculation, c₀ for what either wall's own frame measures.

**The effective obstruction is core-plus-ρ_max-shell, not the bare core — not yet turned into a number.** The medium can't flow through the ρ_max-compressed shell around the core any more than it can flow through the core itself (§2's sieve, fully saturated), so the real cross-section for any drag/ram-pressure treatment of this system is larger than the bare neutron-core radius. **Still needing derivation:** the actual shell radius as a function of core mass (the same three-regime boundary already flagged as open in the surface-gravity-deficit section above), and, once that exists, the Joukowsky-adapted pressure number (ΔP=ρ_max·c₀·Δv, §8 above) computed with a specific, justified ρ_max value rather than a placeholder guess — not done tonight, genuinely open.

**Extended to blackbody radiation as the same single mechanism.** Conventional blackbody theory treats a hot object as passively emitting radiation outward, sourced from its own stored thermal energy. PWC's reframing: heat (the third trifecta term, §1) is drawn *toward*, not radiated from, an untying/matter-release site — the same heat-seeking-untying process as above and as §9's thermal web — while the EM waves themselves, not heat, are what's actually released outward as light. If this holds, it unifies four things under one mechanism instead of four: SMBH-wake cavitation, supernova-revival explosions, the thermal web's cosmic-scale heat inflow, and ordinary blackbody emission — a real theoretical economy, if it survives the check below.

**The concrete, unforgiving check this owes:** real blackbody radiators match the Stefan-Boltzmann law (P=σAT⁴) and the Planck spectral shape to extremely high precision, using only the object's own temperature — no measured "extra" inflow is needed to explain the emitted power. Whatever heat is being drawn in under this picture has to net out to exactly that already-measured, already-accounted energy budget, not add to it, or this becomes a real, testable first-order conservation violation of exactly the kind §1 forbids. The direction of the causal story can flip (heat seeking the release, rather than heat becoming the release) without changing the accounting at all — that would be a real, permitted result. Reproducing σT⁴ and the actual Planck curve from this mechanism, not just a coherent qualitative direction-of-flow story, is what would make this a derivation rather than a reframing.

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

### Cosmic web as the thermal-web mechanism's real physical anchor

The real, well-mapped large-scale structure of the universe — galaxy clusters connected by filaments, with vast voids between — gives the thermal-web mechanism above a genuine physical substrate to run on, rather than leaving it a generic "heat rises, cools, falls" description with no scale attached. Mainstream astrophysics already has a name for warm gas sitting in those filaments, and a live open problem attached to it: the **missing baryon problem** (BBN/CMB predict more ordinary matter than is ever accounted for in stars and cold gas), whose leading resolution is that the missing baryons are diffuse, warm-to-hot gas threading the filaments themselves — the **WHIM** (warm-hot intergalactic medium) — now getting real observational support (FRB dispersion-measure censuses, e.g. Macquart et al. 2020, *Nature* 581, 391; stacked Sunyaev-Zel'dovich and X-ray absorption studies). If the thermal-web mechanism is right, it predicts something specific about that gas: it should look under-dense for its local pressure, specifically at filament/node boundaries, not uniformly — see the heat-choke restatement below. This is a genuinely checkable claim against real WHIM density/temperature/pressure data, **not yet fetched into the corpus** (unlike SPARC/Pantheon+/Planck/DESI — see `physics_engine`) or tested against any domain script.

### Heat choke restated: pressure and density decouple at the medium boundary

Sharper version of the "thermal-web heat choke" bullet above: at the boundary between the organized medium and hot baryonic gas at the *same temperature*, the gas sits at a much lower density than the local pressure alone would predict, because the heat choke rate-limits how fast heat crosses the border and equilibrates the two sides into the density an ordinary equation of state would give. Ordinary gas physics ties pressure and density together tightly (p ∝ ρT); this claims the boundary layer breaks that tie. The gas, being hot, is buoyant and rises — but because it can never match the medium's much steeper density gradient, it overshoots past where it would otherwise settle, then loses thermal buoyancy abruptly (shock-freezes/stiffens, per the existing cycle above) and falls back. Real physical analog for the overshoot-then-fallback step: convective overshoot at a stellar convection-zone boundary, independently measured via helioseismology (~0.3–0.5 pressure scale heights in the Sun) — a genuine, confirmed mechanism for exactly this "rise past equilibrium, lose buoyancy, fall back" behavior, not a borrowed word.

**Resolved as a genuinely separate mechanism from the mass choke, not the same function reapplied.** §2's mass choke blocks on *throughput* — a density/relative-velocity clogging limit, geometric in character. This heat choke blocks on *coupling*: heat transfer is fundamentally electromagnetic, and the medium's EM(+)/EM(−) content, once locked into its maximally-paired trifecta lattice (§3), has no unbonded EM modes left for incoming heat to couple into. The pairing is the cause, not incidental to it — the more completely separated/organized that EM(+)/EM(−) structure becomes, the fewer open channels remain, so the medium's capacity to *absorb* incoming heat gets weaker precisely as its internal order increases. Order and EM-coupling capacity move in opposite directions. Real physical analog, not a borrowed word: Pauli blocking / filled-band non-absorption in solids — an insulator is transparent to a given photon energy because every accessible electronic state is already occupied, so there's nowhere for an absorbed photon's energy to go. Same logic on a different substrate: a maximally-paired medium has no empty state for an EM-mediated heat transfer to land in, so it doesn't absorb, it reflects/excludes — which is why baryonic gas at the boundary can't equilibrate despite sitting against high pressure. It's an absence of an available transition, not a throughput bottleneck. This means the two chokes are independent mechanisms with independent parameters — not a saving of one free parameter, but it does mean each is separately falsifiable: the mass choke against SPARC/rotation-curve data as already tested, this heat choke against WHIM absorption/emission spectra (does the WHIM show suppressed coupling specifically at filament/medium boundaries, the way a filled-band material shows a real, measurable absorption edge) once that data is in the corpus.

---

## 10. Galaxy-Scale Gravity

High gravity draws in and compresses more of the cosmic lattice/energy medium. The galaxy then behaves as if it has more effective gravitational weight, producing lensing and cohesion effects without a separate unseen dark-matter particle inventory.

```
galactic mass/energy → medium compression and density increase → pressure shadowing and altered propagation → enhanced effective cohesion/lensing
```

"Pressure shadowing" and a denser, cold medium are proposed as mechanical contributors to galactic cohesion, treated as Casimir-like effects dependent on the medium's local temperature and density. (This connects to the separate, more detailed galaxy-rotation-curve mechanisms — shadowing/pressure-asymmetry, no-shadowing-at-the-outer-edge, and the temperature-density mechanism — worked through in the companion medium-mechanics debate; those remain quantitatively unresolved against ordinary hydrostatic-equilibrium compression.)

A live, directly relevant citation for this section's cluster-lensing claim: Zhang et al. 2026 (arXiv:2606.19454) find baryonic mass alone accounts for 52–86% of GR's required Bullet Cluster lensing mass and 101–165% of MOND's, in its central regions — real evidence that a non-dark-matter mechanism can do genuine work at cluster scale. **Needing derivation:** PWC has not yet run its own version of this calculation against that same real data; this is a citation for context, not a PWC result.

### The push/pull unification: one self-gravitating mechanism, not two

Since the medium is mass (§1, §4 — matter is condensed medium, not a separate category), it is self-gravitating: every region of it with any density at all is *also* a source of attraction on everything around it, not merely a passive substance sitting between "real" masses. There is no separate "outer pressure" mechanism and "inner tension" mechanism — there is one rule (gravity is medium compression/attraction around mass, §2) applied consistently at every scale simultaneously, not collapsed down to a single point-source:

- **A cluster or galaxy as a whole** pulls in its surrounding medium — from an outside vantage point this reads as pressure pushing in on the structure's outer edge. Same rule as §2, applied to the whole structure as one source.
- **Every individual mass concentration inside it** (star, core, clump) pulls on the more finely distributed medium around it too — the same rule, applied to the full distributed mass structure rather than one point. Medium caught between multiple simultaneous pulls is under tension, not compression.

Push and pull are not two mechanisms — they are the same single self-gravitating rule, described from two different vantage points inside one self-consistent field. And this is a real, named fluid-dynamics effect at the boundary, not just an analogy: ordinary surface tension arises from exactly this asymmetry — a molecule deep inside a fluid is pulled roughly equally in every direction by its neighbors and feels no net force, while a molecule near the boundary has neighbors on one side and comparatively little on the other, producing a net inward pull (the "skin" that lets water bead up or support a water strider). A self-gravitating medium at a galaxy's edge sits in the identical position, gravity standing in for intermolecular attraction — pulled inward by everything behind it, with little pulling back from outside, producing the same membrane-like boundary tension.

**This is what makes testing a0 (§13's SPARC-fit constant) against the SMBH-wake tension term (§8) a genuinely motivated hypothesis, not cross-domain borrowing:** both are the same underlying self-gravitating tension mechanism, expressed at wildly different density scales — a galaxy's edge and a runaway SMBH's cavitation wake. If it is truly one mechanism, the same frozen constant surviving a blind test across that scale gap would be a real, falsifiable result, in the same spirit as §8's frozen-k merger test. **Needing derivation:** the actual dimensional bridge (a0 is an acceleration; the wake tension term needs a pressure) is not yet built. The galaxy-scale half of the test, though, has now actually been run (`domain_CC2_surface_tension.py`, 2026-09-21) against real SPARC data, and it's a real, positive result:

- **Form tested:** `g_pred = choke(g_bar, a0, n=1/2) * (1 + λ·|d ln(g_bar)/d ln(R)|)` — one additional universal coefficient λ on the real, per-galaxy log-log slope of each galaxy's own baryonic acceleration profile (a genuine gradient computed from real Rad/Vgas/Vdisk/Vbulge points, not a free per-galaxy fit, same discipline as domain_K).
- **Result, full 141-galaxy sample:** galaxy-balanced RMS improves from 0.1292 dex (baseline choke) to 0.1266 dex (with the gradient term) — better than the ~0.127 dex reference figure this project already had, and closing further on the McGaugh RAR benchmark.
- **Robustness, properly checked (not just one split):** a 10-seed train/holdout stability check shows the extension beating baseline on galaxy-balanced holdout RMS in **10/10 seeds** — mean improvement −0.0028 dex, consistent in direction and magnitude across every seed, not a lucky split. (A first pass scored against point-pooled RMS instead of galaxy-balanced RMS showed a weaker, non-robust 7/10 — that was a metric error on the analysis side, not a property of the result; fixed before this was reported.)
- **λ's sign: real and robust, but not yet actually explained — a specific causal story for it was tested and failed.** λ comes out negative in all 10/10 seeds (−0.034 to −0.072), and the tension = negative pressure convention (already fixed earlier in this document) is consistent with a negative coefficient in principle. But a specific, falsifiable causal story built on top of that — that the tension comes from *external* competing masses, so galaxies in denser real environments should show a *more* negative λ — was tested directly (`domain_CC3_tension_vs_environment.py`) against real, confound-controlled 2MRS neighbour counts (same volume-limited method as the existing environment domain), using a properly balanced tercile split (43 vs 43 galaxies, not a lopsided isolated-vs-group cut). **Result: refuted, not just unconfirmed.** Low-density tercile λ = −0.077; high-density tercile λ = **+0.014** — the sign moves toward positive in denser environments, the opposite of the prediction. The error was scale, not the sign convention: the gradient term describes radial structure *inside* one galaxy's own disk (bulge/disk transitions, internal mass concentration), and the external-neighbor story tested a completely different scale (Mpc-scale galaxy clustering) that was never actually implied by the mechanism. Honest current state: negative λ is a real, robust empirical result; *why* it's negative remains genuinely open, and this specific external explanation for it is now closed off rather than left untested.

### The cascade equation (2026-09-22): a compounding-shadow mechanism, not a pairwise sum, tested directly against real disk data

Every mechanism tried this session where the medium's own extra mass/tension is sourced *independently* by each star (weighted by distance, by mass, by an individual per-star threshold, by mass-ratio extrapolation from §8's black-hole relation) failed the same way: any purely additive, pairwise-sourced quantity that tracks the visible mass distribution can only rescale the ordinary baryonic curve, never flatten it — confirmed by direct computation across five independent attempts, not asserted.

**What works instead: each shell of medium responds to the state already built up by the shells inside it, not to the local baryonic source alone** — a compounding-shadow (Casimir-type) mechanism rather than direct action-at-a-distance, consistent with the Casimir-like pressure-shadowing already proposed for galactic cohesion above. Stated as an ODE for the enclosed medium mass:

```
dM_med/dr = dM_bar/dr + M_med(r)/r
```

The first term is the ordinary local baryonic source; the second is the compounding term — the medium already organized by everything inside radius r also draws in the next shell, with no free coefficient (the "1" is the simplest possible choice, not fit). Far outside the visible disk, where dM_bar/dr→0, this reduces exactly to `dM_med/dr = M_med/r`, which solves to **M_med(r) ∝ r** — the identical linear-growth, isothermal-type profile independently derived earlier from converting the already-validated √(g_bar·a0) relation into an equivalent density. Two separate routes — one backward from the fitted SPARC result, one forward from this compounding mechanism — landing on the same shape is a real convergence, not a forced match.

**Run against a real exponential disk (M_bar=9×10¹⁰ M☉, Rd=3 kpc, no dark matter, no a0 assumed anywhere in this calculation):**

| R (kpc) | M_bar (M☉) | M_med, cascade (M☉) | v_baryonic (km/s) | v_total (km/s) |
|---|---|---|---|---|
| 5 | 4.47×10¹⁰ | 1.21×10¹¹ | 196.0 | 377.7 |
| 10 | 7.61×10¹⁰ | 2.88×10¹¹ | 180.9 | 395.9 |
| 20 | 8.91×10¹⁰ | 5.97×10¹¹ | 138.4 | 384.2 |
| 30 | 9.00×10¹⁰ | 8.97×10¹¹ | 113.6 | 376.1 |
| 50 | 9.00×10¹⁰ | 1.50×10¹² | 88.0 | 369.2 |
| 100 | 9.00×10¹⁰ | 2.99×10¹² | 62.2 | 364.0 |

Baryonic-only velocity declines by a factor of 3.2 over this range (196→62 km/s), the standard missing-mass problem. With the cascade term, velocity stays within a narrow band (364–396 km/s) across a 20× range in radius — not perfectly flat (a real, honest ~8% decline from 10 to 100 kpc remains, since the baryonic source term still dominates the equation's behavior near the disk before the compounding term takes over), but categorically different from every prior attempt tonight, with zero parameters tuned to produce this result.

**Needing derivation, not yet done:** why the coefficient on the compounding term is exactly 1 rather than some other value derived from K₁/ρ_max/c₀ specifically; whether the residual ~8% decline closes with a proper treatment of the transition region near the visible disk rather than the unit coefficient used here; and the connection to a0 itself — this derivation didn't need a0 as an input anywhere, so if it's right, a0's specific value should be recoverable as an *output* of this equation applied self-consistently across many real galaxies, not assumed. That cross-check has not been run.

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
- **`k ≈ 0.8524572447` is a calibration, not an independent prediction — and the original blind-test "41–50% miss, domain-of-validity" finding has since been corrected (§8, 2026-09-21).** The apparent q-dependent failure pattern turned out to track calibration-source inconsistency (GW150914 calibrated against discovery-paper masses, held-out events tested against catalog-sourced masses), not a real domain-of-validity boundary. Re-solved self-consistently on a single source (live GWOSC catalog pull), the frozen rule (k≈0.868899 under this consistent sourcing) predicts all five events — GW150914 through GW190412, q=0.33 to 0.86 — within 2.2%, with no visible q or spin pattern. This is still marginal-median-level, not yet re-verified at the joint-posterior-sample level (the existing GW190412 posterior-level rejection below used the old, inconsistently-calibrated k and is itself flagged as needing a rerun before being trusted). See §8 for the full corrected table and the exact source-mismatch mechanism.
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
- **The cosmic-web / heat-choke restatement (§9) is a proposed mechanical picture, not yet tested against data.** It gives the existing thermal-web rules a real observational anchor (the WHIM and the missing-baryon problem) and two real physical analogs — stellar convective overshoot (helioseismology-constrained) for the rise/overshoot/fallback cycle, and Pauli blocking / filled-band non-absorption for why the heat choke is a genuinely separate mechanism from §2's mass choke (coupling-limited, not throughput-limited). What's still missing before this is a quantitative test in the style of §8 or `domain_O_thermal_web.py`: no WHIM density/temperature/pressure or absorption-spectrum data has been fetched or compared against it — SPARC/Pantheon+/Planck/DESI are in the corpus, WHIM data is not — and the EM-coupling picture has no equation yet (an actual available-state/occupancy function for the trifecta lattice, analogous to a real band-filling factor, not just the qualitative Pauli-blocking analogy).
- **The "neutrino-to-neutron" density/resistance scaling claim (Earth sitting at ~1% resistance) is stated but not yet reproduced from any formula.** Direct attempts to derive it from raw density ratio, compactness (GM/Rc²), escape-velocity fraction, and surface gravity all failed to reproduce ~1%, and gravity/attraction was separately ruled out as the right normalization — attraction and throughput-resistance are distinct axes in this framework (attraction exists even at rest; resistance/clogging only matters near ρ_max). The actual formula behind "1%" is unresolved.
- **A real empirical test program for the medium's tension constant has been proposed but not executed.** The constant can't be measured by direct contact — the same epistemic situation historically faced by dark matter and the neutrino, both eventually pinned down via indirect/kinematic inference, not direct contact either. Four candidate cross-checks, none yet run against real data: (a) Casimir-shadowing; (b) multi-messenger propagation-speed timing across light/gamma/neutrino/GW — GW170817 already constrains light vs. gravity to 1 part in 10¹⁵, and SN 1987A's ~3-hour neutrino-lead time is a real, existing third-messenger dataset, not yet pulled into the corpus; (c) using a merger's actual near-source nonlinear ringdown waveform, not just its asymptotic propagation speed, as a medium stress-response probe; (d) real spacecraft tracking anomalies — the Pioneer anomaly (8.74×10⁻¹⁰ m/s², now mostly attributed to anisotropic RTG thermal recoil per Turyshev et al. 2012, an attribution not independently re-verified here) and the still-unresolved Flyby Anomaly (Anderson et al.'s geometry-dependent formula) — both suggestively close in order of magnitude to a0, which is itself only a suggestive coincidence until checked.
- **Neutron-star-crust physics (Coulomb/Wigner crystallization — a real, existing "nuclei in a lattice plus degenerate electron sea" literature) is the most directly relevant existing physics for deriving ρ_max from first principles, as a packing limit, instead of fitting or assuming it — proposed, not yet worked through.** This bears directly on the ρ_max/R_core=30.73 km circularity already flagged above (§8): if R_core can be derived independently via a crystallization/packing argument, ρ_max becomes a genuine prediction rather than a restated input. Worth carrying forward precisely, since it's easy to overstate: crystallization is entropy-*decreasing* for the ordering subsystem itself; it's only legal under the second law because the heat expelled during ordering raises the surroundings' entropy by more. The correct claim is "maximum packing forms the lattice, and expelled heat keeps the total entropy budget non-negative," not "maximum entropy forms the lattice."
- **A candidate resolution for Domain CC's factor-of-2 light-bending gap, proposed but not derived.** Real GR light deflection splits into two roughly equal contributions: a Newtonian-like redirection term and a separate spatial-curvature term (space itself warped, so "straight" traces a curve) — Eddington's 1919 measurement confirmed the full, doubled value specifically because both terms are present. Domain CC's isotropic single-role refraction-index treatment only reproduces the first term (2GM/(bc₀²), half the measured bending), which is consistent with this diagnosis. The proposed fix — combining a pressure-differential term (light riding a density gradient) with a separate geometric-curvature term (the medium itself bending the path) — has not been formulated as an actual equation or tested against Domain CC's own numbers.
- **Birefringence is a sharp, currently untested falsifiable PWC-vs-GR discriminant.** GR lensing is measured to be polarization-independent. If the medium's EM(+)/EM(−) structure (§1) is genuinely chiral/directional, PWC predicts polarization-*dependent* lensing — something GR cannot produce at all, structurally, not just as an unmeasured effect. No polarization-resolved lensing data has been checked against this yet.
- **A proposed but unquantified connection between the SMBH bow-wave mechanism (§8) and JWST's early/"impossible" massive galaxies** — a real, currently open tension for ΛCDM structure-formation timelines. The idea: the same compression-front/bow-wave mechanism already used for RBH-1 could accelerate structure formation around it, which would show up as excess galaxy mass at high redshift. This needs an actual mass-vs-redshift prediction derived from the bow-wave mechanics before it's a real test rather than a suggestive parallel.
- **The buoyancy/squeeze mechanism in §4 is not a separate assumption needing its own justification.** Same substance, same mass, different density by phase — exactly like liquid water and water vapor — is ordinary phase behavior, not a special case that needs proving before it's allowed. The actual open item is the same one already listed for the GW150914 model layer above: nobody has yet written down the medium's real equation of state, P(ρ,s), that this phase behavior (and the rest of the theory) would run on. That's one open item, not a new one specific to §4.
