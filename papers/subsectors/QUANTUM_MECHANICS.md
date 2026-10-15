# Paper
A Phase Wave Cosmology document.
**Author:** Jaden Allison — Fringeneering · **Framework:** Phase Wave Cosmology
**Full framework:** https://github.com/fringeneering-jpg/PWC
---

# Quantum Mechanics — The Subatomic Sector

*One medium, one yield, one formula, one ledger. The subsector paper for the
physics department: the ontology, the mass–energy identity, the quantization,
the charge, the coupling, the frustration, the photon, and the heat — every
equation first, every derivation second, every observed match with its
residual third. Every number is quoted from
`PHASE_WAVE_COSMOLOGY_DERIVATIONS.md`, the master document; every script is
linked by filename from `scripts/`.*

---

## 1. The ontology — one medium, three rules

The universe is **one substance**: a continuous, mass-bearing electromagnetic
medium — paired EM waves at rest spacing, held by heat. The heat is not a
separate energy and not mass: it is the waves' own component, squeezed out
when they compress — **the debt**. Matter is this same medium tied into
**720° toroidal knots**: m = L/c₀², with L the **light energy** (Einstein's
original letter, 1905). Light is the medium's own wave — the photon is the
medium breaking its own transmission limit. Black holes are shells at the
density ceiling, ending at a **complete stop** — not a singularity. The
medium is static. Everything in this document follows from exactly three
quantities: **pressure, density, geometry.** No dark matter, no dark energy,
no singularities, no placeholders.

## 2. The mass–energy identity — m = L/c₀²

**The quote, first.** Einstein, 1905 — *"Does the Inertia of a Body Depend
Upon Its Energy-Content?"* (Annalen der Physik 18, 639–641 (1905); the German original: *"Ist die Trägheit eines Körpers von seinem Energieinhalt abhängig?"*). His original symbol
for the light energy was **L**, not E: *"If a body gives off the energy L in
the form of radiation, its mass diminishes by L/V²."* The framework restores
the letter: the mass is the light energy over c₀², and c₀² is the specific
latent heat of the universe.

**Law.** m = L/c₀², L the light energy; c₀² the specific latent heat of the
universe.

**Derivation.** Einstein's 1905 identity, restored to its original letter — L,
not E. The tying squeezes the wave's own component out as light; the retained
knot is what remains. The mass is the wave-structure that survives the weld;
the light is the portion shed. The confinement chain: the confined light
carries Maxwell's momentum p = L/c₀, and the 720° double-loop confines one
Compton wavelength — the wave's phase closes only after 4π, so the loop
stores the momentum as rest inertia, not transport: m = L/c₀².

**Match.** The full lepton ladder (D11) and the merger catalog (D13) close on
this identity with zero fitted parameters. Script: [`the_ladder.py`](../scripts/the_ladder.py).

## 3. The quantization pair

**Law.** m_e·λ̄_C·c₀ = ℏ (1 quantum); m_p·R_p·c₀ = 4ℏ (4 quanta).

**Derivation.** The 720° double-loop confines one Compton wavelength; the
wave's phase closes only after 4π. The proton's 2-1-2 cage carries four
quanta. Factor 4 = the real dimension of SU(2) (quaternion basis
{1, i, j, k}); factor 8 = 2 wavelength quanta per SU(2) direction × 4
directions = the total quanta in the 720° path.

**Match.** m_p/m_e = 4λ̄_C/R_p = 1835.79 vs 1836.15 — **−0.02%** (Antognini
2013).

**The sealed proton identities** (2026-09-30) — both proton observables as
outputs of {ρ_max, c₀, ℏ} + the 720° topology alone, R_p no longer input:

    Identity A:  m_p·R_p·c₀ = 4ℏ
    Identity B:  m_p = (4π/3)·ρ_max·R_ball³ ,  R_ball = 8·R_p
    Combined:    R_p⁴ = 3ℏ/(512π·ρ_max·c₀)   →   R_p = 0.8422 fm vs 0.8414 (Antognini 2013) — 0.10%
                 m_p⁴ = (131072π/3)·ρ_max·ℏ³/c₀³   →   m_p = 1.6707×10⁻²⁷ kg vs 1.6726 (CODATA) — 0.12%
                 R_ball/R_p = 8.000 vs 8.011 — 0.13%

Script: [`proton_derivation_20260930.md`](../scripts/proton_derivation_20260930.md); the ladder:
[`the_ladder.py`](../scripts/the_ladder.py).

## 4. The charge and the dichromal fold

**Law.** q′ = √(3ε₀hc/8π³) = 0.9103e; g = 16π³α/3 = 1.206740.

**Derivation.** The electron is the photon of toroidal topology
(Williamson–van der Mark 1997); the charge is the winding's topological
measure, the wavelengths cancelling. g is the charge geometry's eigenfactor.

**Match.** g = 16π³α/3 reproduces α⁻¹ = 137.036 from the idealized 165.37 via
the fold's own geometry (D7). Script: [`quicycle_charge_map.py`](../scripts/quicycle_charge_map.py).

## 5. The coupling from the fuel gauge

**Law.** g = (ρ_medium/ρ_matter)^(1/16) = 20^(1/16) = 1.205909.

**Derivation.** The tension declines as the fuel burns; the remaining fraction
is the sixteenth root of the fuel fraction, because the knot's harmonic count
is 16 — eight wavelength quanta in the double-cover path (2 per direction × 4
directions) times two polarizations, or four quanta times four spinor states:
8×2 = 4×4 = 16, the same modes counted twice.

**Match.** 20^(1/16) vs 16π³α/3 — **−0.069%** (the fuel's own precision).
Scripts: [`sixteen_origin.py`](../scripts/sixteen_origin.py), [`sixteen_stage_loop.py`](../scripts/sixteen_stage_loop.py).

## 6. The frustration energy

**Law.** ΔU = δ·U = 2.47 eV = 502 nm, δ = (6φ² − 5π)/5π.

**Derivation.** The knot can never reach the stress-free golden configuration
— the winding limit stops it δ short. The locked strain is the energy cost of
existing as matter: geometric frustration, the phase boundary.

**Match.** frozen as the V2 target: the electron's channel at 502 nm; the
proton's line at 0.0658 eV = 18.8 μm (prediction-shaped, not claimed).
Script: [`topology_equation_corrected.py`](../scripts/topology_equation_corrected.py).

## 7. The photon's identity

The photon is the same substance as the medium at lower density — squeezed out
like a watermelon seed by the surrounding high-density phase — and it moves at
the high-density phase's own speed: c₀ = √(stiffness/density) = 1/√(μ₀ε₀)
(Maxwell 1861–62). Light and gravitational waves are neighbour-reaction
(EM-yank) waves, not compression — hence equal speed (GW170817: equal to
10⁻¹⁵).

## 8. The photon's round trip — the loop's balance

The forge's heat is the wave's own shed fragment — the photon. The untying's
orphan wave absorbs heat, becomes luminous, redshifts into the bath (the CMB),
propagates through the medium toward the untying (the blackbody is the
transport, not a limit), and is pulled back to the untying, where it is
re-absorbed by the waves as they untie. The cold weld: the heat's complete
exit through the centre removes the thermal padding, and the strands fuse.
M = L/c₀² — the mass is what remains, the light is what was paid. The ledger
closes at 1.000 — expelled 94.74% + retained 5.26% = c₀² exactly; the bath is
the accumulated exhaust; the heat returns to the untying. The loop is the
balance. Script: [`heat_hates_pressure.py`](../scripts/heat_hates_pressure.py).

## 9. The heat ontology — HEAT HATES PRESSURE

**Law.** the flux follows −∇P; (1/u)(du/dt) = s·3H·(1+T).

**Derivation.** Heat is a transfer, not an energy; it moves from pressure to
relief. The untying front is the relief valve; the medium unties at its own
set rate; the debt's tension is the grip; the front's tightening is the
acceleration. **HEAT HATES PRESSURE** — the rule everything else follows.

**Match.** the cosmic web's heat map; the CMB as the accumulated exhaust; the
peak's demanded tempo pins T ≈ 27 = 3³ — the tightening coefficient awaits
data. Script: [`heat_hates_pressure.py`](../scripts/heat_hates_pressure.py).

## 10. The selection law and the knot's existence

**Law.** a knot holds iff no single bias finds an unspooling direction AND the
collapse heat fully exits through the centre. Survivors: {1, 5}.

**Derivation.** The 2 and 3 chains die to one fluctuation; the 2-1-2 cage
converts every push into compression on its core (the wire-rope law); the cold
weld requires the heat's complete centre-channel exit.

**Match.** the electron and the proton; the neutron as the cage with one
exposed thread (14:38); the 2/3/4 arrangements absent from nature. Script:
[`knot_selection_law.py`](../scripts/knot_selection_law.py).

**Existence.** the forge requires e_avail ≥ E_lock; the retention requires the
selection law and the heat balance. Three clauses: the forge's energy, the
topology's lock, the weld's completeness — the RETAINED flag is **derived**
analytically from these three clauses (forge energy, selection law {1,5},
heat balance); numerical confirmation running. Sub-threshold dissipates;
super-threshold (1.33× the lock) retains. Script:
[`existence_derived.py`](../scripts/existence_derived.py).

## 11. The sixteen-fold clock — the crossing geometry named open

**Law.** N = 4π/(π/4) = 16; τ_fold = L/(√2·c₀); τ_loop = 16L/(√2·c₀).

**Derivation.** The 720° knot is sixteen 45° creases; each fold's clock is the
light-crossing of the neck's 45° projection.

**Match.** 4.6796 ms vs the GW150914 4.68 ms — +0.009% (proposed, arithmetic
verified; the crossing geometry named as open). Script:
[`sixteen_fold_clock.md`](../scripts/sixteen_fold_clock.md).

## 12. The honest boundaries — carried from the master, stated once

- The merger machinery claims **no predictive edge over the trivial
  baseline**: 0.71% trivial vs 0.88% min(E,S) out-of-sample.
- The sixteen-fold clock's crossing geometry is **OPEN** (arithmetic
  verified only).
- The T6 Lorentz legs are **OPEN** — Kennedy–Thorndike-level precision
  (10⁻¹⁷ cavity tests), stellar aberration, and Fizeau's drag 1 − 1/n².
- The tightening coefficient T ≈ 27 = 3³ awaits data.
- The birefringence test's sign is **OPEN** — a probe, not a killshot.
- The black-hole limits are **OPEN** — two candidate fates, neither locked.
- The RETAINED flag is **DERIVED** (forge energy, selection law {1,5}, heat
  balance); numerical confirmation running.

---

## The scripts and the record

Every derivation above has its executable form in
`C:\Users\jaden\Downloads\PWC-Check\PWC_THEORY\scripts\`. The department is
invited to check any derivation against its script: one command reproduces
the scoreboard, `python scripts/run_full_framework.py` (28 sections, 0
failures).

The published framework lives at

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
- Stodolna et al. — *Phys. Rev. Lett.* 110, 213001 (2013) — the hydrogen orbital photographed
- Further viewing — HuygensOptics, "Are Electrons made of Light?" (YouTube, 2025); https://quicycle.com
**https://github.com/fringeneering-jpg/PWC** — the theory, the derivations,
and the scripts. The falsified attempts and superseded items are kept for
honesty in the repository's history, never printed in this paper.

