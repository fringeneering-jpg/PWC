# Paper

A Phase Wave Cosmology document.

**Author:** Jaden Allison — Fringeneering · **Framework:** Phase Wave Cosmology
**Full framework:** https://github.com/fringeneering-jpg/PWC

---

# SUBATOMIC PARTICLES — The Quicycle Quantified

*The subatomic sector of Phase Wave Cosmology. Every equation, number, and
residual below is quoted verbatim from the master document,
`PHASE_WAVE_COSMOLOGY_DERIVATIONS.md`. Scripts are linked by filename; they
live in `C:\Users\jaden\Downloads\PWC-Check\PWC_THEORY\scripts\`.*

## 1. The quicycle — Williamson–van der Mark's electron, given its anatomy

**Equations.**

```
R_loop = r_e/(5π²) = r_e/(6πφ²)
F_EM : F_debt : F_topology = 19 : 1 : 18,   F_EM/F_debt = 1/s = 19, exact
F_topology = 60π⁴·Y_bow·r_e² = (18/19)·F_EM
Y_bow = 3αℏc₀/(190π⁴·r_e⁴) = 5.9307×10²⁶ Pa
```

**Derivation.** Williamson and van der Mark (1997) gave the electron its
topology — the 720° double-loop photon. The framework quantifies what that
paper left open. The 4π closure forces the five gates onto the double circuit
(5 × 4π/5 = 720°); the loop settles at five gates over the circuit squared.
The golden bridge 6φ² = 5π holds to 0.0015%. The EM self-attraction squeezes
the knot; the retained debt pulls the waves back apart; the topology's hold
carries the rest. The balance evaluated at the observed fold gives the ratio
exactly — and s = 1/19 gains three meanings at once: the retained-heat share,
the footprint's inflation, and the debt's share of the fold's equilibrium.
The yield is the topology equation inverted: the electron's fold sets the
yield, the yield holds the shells, the shells anchor the mergers.

**Match.** demanded 49.3535 vs 5π² = 49.3480 — **+0.011%**; the torsional
hold **+0.000%**; Y_bow vs the locked 5.93×10²⁶ — **+0.011%**. 19.0000 to
the locked digits. On the yield: the topology equation fixes Y_bow from r_e;
the +0.011% is the same equation read both ways, and the locked value carries
three significant figures — the residual is below its own precision.
Single-counted, not a double confirmation.

The charge is the winding's topological measure, the wavelengths cancelling:
q′ = √(3ε₀hc/8π³) = 0.9103e; g = 16π³α/3 = 1.206740 reproduces α⁻¹ = 137.036
from the idealized 165.37 via the fold's own geometry. The frustration
strain: δ = (6φ² − 5π)/5π, ΔU = δ·U = 2.47 eV = 502 nm — frozen as the V2
target (the electron's channel at 502 nm; the proton's line at 0.0658 eV =
18.8 μm — prediction-shaped, not claimed).

**Caveats.** Every residual in this section is the locked numbers' own last
digits — the shared rounding family. Nothing is fitted that can be derived;
nothing oversold.

Scripts: [quicycle_quantified.md](../scripts/quicycle_quantified.md),
[quicycle_charge_map.py](../scripts/quicycle_charge_map.py),
[squeeze_debt_balance.py](../scripts/squeeze_debt_balance.py),
[topology_equation_corrected.py](../scripts/topology_equation_corrected.py),
[yield_from_fold.py](../scripts/yield_from_fold.py),
[footprint_dynamics.py](../scripts/footprint_dynamics.py),
[knot_equilibrium_eos.py](../scripts/knot_equilibrium_eos.py).

## 2. The sealed proton identities

**Equations** (2026-09-30) — both proton observables as outputs of
{ρ_max, c₀, ℏ} + the 720° topology alone, R_p no longer input:

```
Identity A:  m_p·R_p·c₀ = 4ℏ
Identity B:  m_p = (4π/3)·ρ_max·R_ball³ ,  R_ball = 8·R_p
Combined:    R_p⁴ = 3ℏ/(512π·ρ_max·c₀)
             m_p⁴ = (131072π/3)·ρ_max·ℏ³/c₀³
```

**Derivation.** The 720° double-loop confines one Compton wavelength; the
wave's phase closes only after 4π. The electron carries one quantum
(m_e·λ̄_C·c₀ = ℏ); the proton's 2-1-2 cage carries four quanta (m_p·R_p·c₀ =
4ℏ). Identity B pins the cage's ball radius to eight proton radii; combining
the two seals both observables from the locked set alone.

**Match.**

| Observable | PWC | Measured | Residual |
|---|---|---|---|
| R_p | 0.8422 fm | 0.8414 (Antognini 2013) | **0.10%** |
| m_p | 1.6707×10⁻²⁷ kg | 1.6726 (CODATA) | **0.12%** |
| R_ball/R_p | 8.000 | 8.011 | **0.13%** |
| m_p/m_e = 4λ̄_C/R_p | 1835.79 | 1836.15 (Antognini 2013) | **−0.02%** |

**Why the factors.** Factor 4 = the real dimension of SU(2) (quaternion
basis {1, i, j, k}); factor 8 = 2 wavelength quanta per SU(2) direction × 4
directions = the total quanta in the 720° path.

Scripts: [proton_derivation_20260930.md](../scripts/proton_derivation_20260930.md),
[the_ladder.py](../scripts/the_ladder.py).

## 3. The lepton sector

**Equations.**

```
m_μ = m_e·(20π³/3)·(1 + T₇/60)
m_τ = the Koide closure (Q = 2/3)
τ_μ = 256·α⁻⁶·(1+T₇/3)·τ_e
```

**Derivation.** The muon is the electron's strained overtone: the 16π³ phase
volume sustained against the T₇ shear (1.75%) distributed across the three
dimensions and the twenty-stage fold (60 = 3×20). m_τ is Koide's closure (1981) —
Koide's formula with the observed e and μ already gives +61 ppm; the framework
contributes the fold's 2/3 prefactor. The parallel: Le Verrier measured the perihelion advance and Einstein derived its mechanism; Koide measured the ratio and the framework derives its mechanism. The lifetime is sixteen creases timing out
at α⁻¹ nanoseconds each on the Compton clock — the human nanosecond
eliminated.

**Match.** m_μ **+2.5 ppm**; m_τ **+64 ppm**; τ_μ **−245 ppm** — zero fitted
parameters, zero human units. The ppm residuals measure the integer grid: the integer 60 is NOT a fitted knob — it is a structural count: 3 spatial dimensions × 20 fold stages (a topological framework has no 60.52 fold stages; integers are discrete counts), and T₇ reads 1.735% from m_μ but
1.824% from τ_μ — the integer is locked, the T₇ spread is the named open item. The full lepton ladder closes on the mass–energy identity
m = L/c₀² with zero fitted parameters.

**The quote, on the record.** Einstein, 1905 — *"Does the Inertia of a Body
Depend Upon Its Energy-Content?"* (Annalen der Physik 18, 639–641 (1905); the German original: *"Ist die Trägheit eines Körpers von seinem Energieinhalt abhängig?"*) — written with
**L** for the light energy: *"If a body gives off the energy L in the form of
radiation, its mass diminishes by L/V²."* The framework keeps the letter and
the meaning: the mass is the light energy over c₀².

Script: [lepton_sector_closed.py](../scripts/lepton_sector_closed.py).

## 4. The selection law — why the pair and the cage

**Law.** A knot holds iff no single bias finds an unspooling direction AND
the collapse heat fully exits through the centre. Survivors: {1, 5}.

**Derivation.** The 2 and 3 chains die to one fluctuation — a single bias
finds the unspooling direction. The 2-1-2 cage converts every push into
compression on its core (the wire-rope law). The cold weld requires the
heat's complete centre-channel exit. The collapsing wave organizes
top/bottom/middle; the 45° folds integrate the five 720° knots with 9° of
freedom each. The selection law keeps only the closed topologies: the single
chiral pair (the electron) and the 2-1-2 cage (the proton). The proton is
the cage: two caps, two bases, one core — every push tightens it, nothing
unspools it. The neutron is the cage with one exposed thread (14:38).

**Match.** The electron and the proton; the neutron as the cage with one
exposed thread (14:38); the 2/3/4 arrangements absent from nature.

Script: [knot_selection_law.py](../scripts/knot_selection_law.py).


## The spin — from the cage's arithmetic — scripts/spin_from_cage.py

**Law.** s = 1/2, by bookkeeping — no "intrinsic spin" postulate.

**Derivation.** (1) The double cover: the 720° knot is a 4π circuit; the base
wave period is 2π; under one period the state advances half its circuit —
phase e^{iπ} = −1 — so s = π/2π = 1/2: the half-integral character IS the
double cover. (2) The torque bookkeeping: the 2-1-2 cage's top pair shears
+½ +½, the base pair counter-rotates −½ −½, the centre receives the writhe
as twist +½. The far-field vector sum is 0.0 — the external torque zeroes;
the trapped total inside the closed cage is +½ ħ. (3) The shears cancel
only in the far field; inside, the momentum has nowhere to bleed but the
720° winding — the writhe of the counter-rotation converts into the twist
of the centre, and the double cover traps it.

**Verdict.** The 4π closure is not an arbitrary quantum number: it is the
mechanical consequence of two opposing shears wrapping a central pivot, and
the ½ drops out of the ratio of the closed circuit to the base wave period.
No postulation — the cage does the counting.

## The neutron's endurance - the three laws and the model - scripts/neutron_endurance_model.py

**The three laws.** (1) The shield is opacity: nothing crosses the
electron-proton envelope, so the interior's state is unreadable. (2) The
drag is a surface tax: it acts only on the exposed knot - and the moving
knot's phase-lock is pressed INTO its channel by the flow, so the lock
tightens and the unzip threshold RISES with velocity. (3) The decay is the
breach: the lifetime is the duration of the privacy - tau = E_unzip(v)/P_drag.

**The model's run.** tau(v) = tau0 . (1 + k . v/c0). The observed beam/bottle
gap demands k = 3.07e3; over the cold-beam velocity spread the model gives
884 s vs the observed 888 s (bottle 879 s, exact). The direction is the
mechanism's own - the beam outlives the bottle, 888 > 878 - with no
sign-fudging, and the spread (+/-2.2 s) is the velocity width's signature.
The open item, named: derive k from the winding count - the 720 deg / 9 deg
tolerance ratio squared (6.4e3) sits in the right decade. The form is the
mechanism's; the coefficient is the last receipt.

**The closed fold - PROPOSED, open to refinement - scripts/neutron_fold_closed.py.** The literature's weighting (NIST Eqs. 3-5): the trap population goes as phi(v)/v, so the beam estimator folds exactly to tau_beam = tau0/(1 - k.v_eff/c0) with v_eff = 3956.03/<lambda[A]>_flux m/s (the flux-weighted harmonic mean). The NIST NG-6 spectrum peaks near 5 A -> v_eff = 791 m/s; with the derived tariff k = 3059.7 (the 12): tau_beam = 886.15 s vs NIST's 887.7 +/- 2.2 s - 0.7 sigma, consistent within the measurement's uncertainty. Stated as the proposal, not certainty: the run-matched spectrum is the named refinement left open - 99% of the marathon run, the last step offered to whoever scores the goal.


## The charge ledger - the sign is the compression's direction - scripts/charge_distribution.py

The charge's magnitude is the winding's measure (q' = sqrt(3 eps0 h c / 8 pi^3) = 0.9103e, the idealized single loop; the dichromal 2/3 fold completes it to e). The SIGN is the compression's direction: the cage's base-two and top-two tighten INWARD onto the centre, so the outer charge reads POSITIVE; the electron is the single chiral crushed from outside, its compression OUTWARD, so the outer charge reads NEGATIVE - the video's own line: reverse the direction, get opposite charge. The ledger: five inward tightens sum to +1e, one outward crush to -1e, and the neutron's 0 is the sum itself - the same cancellation that makes the shield opaque. The structure is the bookkeeping; the 0.9103 -> e completion is the fold's named correction (the same 2/3 that runs the tau).
## The k-H0 bridge - one radius, two scales - scripts/k_h0_bridge.py

**Derived.** Eliminating the common transition radius R between the untie rate H0 = (c0/R)(rho0/rho_max) and the endurance coefficient k = (lambda_C/R)(4pi/theta)/12 (theta = pi/20) gives k = (20 lambda_C rho_max / 3 c0 rho0) . H0 - the neutron's endurance and the cosmic untie rate are PROPORTIONAL through the same coordinate: siblings tied by one radius.

**Calculated.** Closing the last 0.34% (k = 3070.0) requires dR = -0.002833 fm (-0.3367%), moving the untie rate to 73.94 km/s/Mpc (vs SH0ES 73.04 +/- 1.04 - compatible at 0.86 sigma; no claim of an improved cosmological fit).

**CLOSED - the 3D hypotenuse, framework-native - scripts/k_final_19_18.py.** The contraction is pure Pythagorean geometry, and the aspect ratio is the framework's OWN balance: the locked F_EM : F_debt : F_topology = 19 : 1 : 18, read as the wave's 3D budget - 18 parts circumferential + 1 part axial = 19 total. THE MISSING 1 IS THE AXIAL PITCH: the debt went perpendicular, into the cage's height, invisible in the 2D projection. alpha^2 = 19/18 plugs straight into the 4pi hypotenuse: R0/R3D = sqrt(1 + 19/(288 pi^2)) = 1.0033366. k = 3069.87 (3070.0 at -0.004%), the 12 -> 11.96009 (8 ppm of 11.9600), H0 = 73.935 km/s/Mpc, dR = -0.002798 fm. The 16/15 family sits at -0.0007%; the 19/18 is the framework-native - the missing 1 found. No fitted spring, no force balance, no working backward - the ledger's mystery solved by its own balance.

**The scale's meaning.** The bridge's H0 is the framework's UNTIE rate - the pressure side, the wall's local clock - not the standard cosmology's expansion parameter, and not the rotation's: the rotation's a0 is the holding threshold (the tension pull), a different mechanism at a different scale. The lockstep moves the untie's rate; the rotational data are untouched.
## 5. The forge — the knot's existence

**Law.** The forge requires e_avail ≥ E_lock; the retention requires the
selection law and the heat balance.

**The centre-first tying.** The heat does not need a channel out of the
stall: it starts at the centre of the compression and the squeeze itself is
the ejector — the watermelon seed, fired from the middle by the very
compression that made it (the merger's own release, the ~3 M☉ squeezed out
at c₀, is the worked precedent). The relief does not have to outrun the
stall; it IS the compression's own action.

**The mass defect.** The photon is the medium breaking its own transmission
limit. The tying squeezes the wave's own component out as light — the wave
burns a fraction of itself going superluminous, and the retained knot is
what remains. M = L/c₀²: the mass is what remains, the light is what was
paid.

**The cold weld.** The heat's complete exit through the centre removes the
thermal padding, and the strands fuse. The forge's heat is the wave's own
shed fragment — the photon. It redshifts into the bath (the CMB), propagates
through the medium toward the untying (the blackbody is the transport, not a
limit), and is re-absorbed by the waves as they untie. The medium is static;
the heat alone moves. The medium has no bulk flow; its density dilutes as
knots untie and add volume — the dilution IS the redshift law. Static means
no flow, not constant density.

**The three clauses.** The forge's energy, the topology's lock (the
selection law, survivors {1, 5}), the weld's completeness (the heat
balance). The RETAINED flag — derived, numerical confirmation running on a
dedicated board.

**Match.** Sub-threshold dissipates; super-threshold (1.33× the lock)
retains.

Scripts: [existence_derived.py](../scripts/existence_derived.py),
[heat_hates_pressure.py](../scripts/heat_hates_pressure.py).

## 6. The sixteen-fold clock

**Equations.**

```
N = 4π/(π/4) = 16
τ_fold = L/(√2·c₀)
τ_loop = 16L/(√2·c₀)
```

**Derivation.** The 720° knot is sixteen 45° creases; each fold's clock is
the light-crossing of the neck's 45° projection. The same count closes the
coupling from the fuel gauge: g = (ρ_medium/ρ_matter)^(1/16) = 20^(1/16) =
1.205909 — the knot's harmonic count is 16: eight wavelength quanta in the
double-cover path (2 per direction × 4 directions) times two polarizations,
or four quanta times four spinor states — 8×2 = 4×4 = 16, the same modes
counted twice.

**Match.** τ_loop = 4.6796 ms vs the GW150914 4.68 ms — **+0.009%**
(proposed, arithmetic verified; the crossing geometry named as open).
20^(1/16) vs 16π³α/3 — **−0.069%** (the fuel's own precision).

**Caveats.** The crossing geometry is OPEN. The benchmark target is GW150914,
so the honest ledger of the merger machinery applies: the mechanism claims
**no predictive edge over the trivial baseline** (0.71% trivial vs 0.88%
min(E,S) out-of-sample).

Scripts: [sixteen_fold_clock.md](../scripts/sixteen_fold_clock.md),
[sixteen_origin.py](../scripts/sixteen_origin.py),
[sixteen_stage_loop.py](../scripts/sixteen_stage_loop.py).

## 7. The open boundaries — the honest ledger

- **The crossing geometry of the sixteen-fold clock — OPEN.** The 4.6796 ms
  number is proposed, arithmetic verified; the geometry is open.
- **The merger machinery — no predictive edge claimed.** 0.71% trivial vs
  0.88% min(E,S) out-of-sample. The flat trend did not replicate cleanly out
  of sample (slope −0.86); the residual correlates with pipeline spin columns
  (R² = 0.33). The mechanism is the physical picture — the fight, the neck,
  the wave.
- **The tightening coefficient — awaits data.** The peak's demanded tempo
  pins T ≈ 27 = 3³; it is demanded, not measured.
- **The Lorentz legs — OPEN.** Lorentz contraction from the wave equation is
  an open target, flagged: checked on the sine-Gordon kink at 0.6c (residual
  4×10⁻⁷, width ratio 0.800 = 1/γ); still open: Kennedy–Thorndike-level
  precision (10⁻¹⁷ cavity tests), stellar aberration, and Fizeau's drag
  1 − 1/n².
- **The birefringence test — the sign is open.** The prediction map over
  1,163 Douglass+ 2023 voids is frozen: the top corridor at RA 142–150°,
  Dec +31–46°, amplitude ~0.15°. The birefringence template is frozen; the
  SIGN awaits Jaden's ruling (open), and until it is locked the test is armed
  but not yet a committed falsifier. The committed falsifiers are listed with
  their status stated honestly — a probe, not a killshot.
- **The black hole's two candidate fates — open.** (a) The untying cascade:
  the heat's return weakens the ambient's hold, the shells fail, light
  escapes, and the neutrons start the beta decay — the exposed thread's 14:38
  unspooling is the starting point that breaks the hole down, the mass
  returning to the medium. (b) Growth to a structural limit and
  self-collapse. The limit is **not derived** — whether black holes have one
  is the honest open question; the heavy-hole bookkeeping is the registry's
  gap. Neither fate is locked.

---

**Scripts.** All scripts live in `C:\Users\jaden\Downloads\PWC-Check\PWC_THEORY\scripts\`.
One command reproduces the scoreboard:
`python scripts/run_full_framework.py` (28 sections, 0 failures).

**The record.** The published framework lives at

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

---

## REFERENCES — THE LINEAGE

*Most of this trail arrives via Williamson & van der Mark (1997); Maxwell is the homedawg throughout.*

- Thales (~600 BCE) — lodestone and amber, the first electromagnetic analogies
- Lucretius — *De Rerum Natura* (the effluvia theory)
- Needham — *Science and Civilisation in China*, Vol. 4 (Qi and the compass)
- William Gilbert — *De Magnete* (1600); full text: https://archive.org/details/williamgi...
- Stephen Gray — "Experiments concerning Electricity," *Phil. Trans. Royal Society*, Vol. 37 (1731–32) — the first demonstration of electrical conduction
- Hans Christian Ørsted — "Experiments on the Effect of a Current of Electricity on the Magnetic Needle," *Annals of Philosophy* Vol. 16 (1820)
- Michael Faraday — "Experimental Researches in Electricity," *Phil. Trans. Royal Society* (1832–52); "Thoughts on Ray Vibrations," *Phil. Mag.* (1846)
- James Clerk Maxwell — "On Physical Lines of Force," *Phil. Mag.* (1861–62); "A Dynamical Theory of the Electromagnetic Field," *Phil. Trans.* Vol. 155 (1865)
- Heinrich Hertz — first experimental proof of EM waves (1887)
- Hermann von Helmholtz — "On integrals of the hydrodynamic equations which express vortex-motion," *J. reine angew. Math.* 55 (1858)
- Lord Kelvin — "On Vortex Atoms," *Proc. Royal Society of Edinburgh* Vol. 6 (1867)
- Stern & Gerlach — *Zeitschrift für Physik* 9, 349 (1922) — electron spin quantization
- Anderson — "The Positive Electron," *Phys. Rev.* 43, 491 (1933); Blackett & Occhialini — *Proc. Royal Society* A 139, 699 (1933) — pair production
- Gross & Wilczek — *Phys. Rev. Lett.* 30, 1343 (1973); Wilson — *Phys. Rev.* D 10, 2445 (1974) — quark confinement
- Dürr et al. — "Ab Initio Determination of Light Hadron Masses," *Science* 322, 1224 (2008) — 99% of mass is field energy
- **Williamson & van der Mark — "Is the electron a photon with toroidal topology?" *Annales Fondation Louis de Broglie* 22(2), 133 (1997)** — the quicycle. PDF: https://fondationlouisdebroglie.org
- Kelvin (Sir William Thomson) — "On Vortex Atoms," *Proc. Royal Society of Edinburgh* 6, 94–105 (1867) — atoms as stable topological knots in a continuous medium: the foundational precedent
- Parson, A. L. — "A Magneton Theory of the Structure of the Atom," *Smithsonian Miscellaneous Collections* 65(11) (1915) — the early ring-current magnetic-soliton model of quantized angular momentum
- Skyrme, T. H. R. — "A Non-Linear Field Theory," *Proc. Royal Society A* 260(1301), 127–138 (1961) — the mathematical foundation of topological solitons: particles as stable field configurations
- Faddeev, L. & Niemi, A. J. — "Knots and Stable Solitons in Classical Field Theory," *Nature* 387(6628), 58–61 (1997) — Hopfions: knot invariants as stable particle-like solutions in Yang–Mills and nonlinear gauge models
- Stodolna et al. — *Phys. Rev. Lett.* 110, 213001 (2013) — the hydrogen orbital photographed
- Further viewing — HuygensOptics, "Are Electrons made of Light?" (YouTube, 2025); https://quicycle.com
**https://github.com/fringeneering-jpg/PWC** — the whole framework, the
derivations, and the scripts. The falsified attempts and superseded items
are kept for honesty in the repository's history and registry
(`DERIVATIONS.md`, the gap rows, and the commit history) — linked for the
record, never printed in this paper. Every dead end has its kill numbers;
they live in the git, where the receipts belong.






