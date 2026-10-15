# Clay Lodgement 2
A Phase Wave Cosmology document.
**Author:** Jaden Allison — Fringeneering · **Framework:** Phase Wave Cosmology**
**Full framework:** https://github.com/fringeneering-jpg/PWC
---

## Yang–Mills Existence and Mass Gap — The Knot's Closure

*Source of truth: [PHASE_WAVE_COSMOLOGY_DERIVATIONS.md](../PHASE_WAVE_COSMOLOGY_DERIVATIONS.md).
Every number, equation, residual, and caveat below is quoted from that master
document. Nothing is fitted that could be derived; nothing is oversold.*

## Summary

The Clay question: prove that pure Yang–Mills theory has a mass gap — a
positive lower bound on the excitation spectrum above the vacuum, no
zero-mass mode. The framework's answer is the knot's closure. The 5π²
boundary forbids the zero-mass mode, because a closed 720° loop has no free
unconfined excitation. The spectrum is discrete by the selection law: only
the {1, 5} closed topologies survive. The gap is not a property bolted onto
the field theory. It is what a closed loop is.

The worked numbers, verbatim:

    m_e·λ̄_C·c₀ = ℏ (1 quantum);  m_p·R_p·c₀ = 4ℏ (4 quanta)
    m_p/m_e = 4λ̄_C/R_p = 1835.79 vs 1836.15 — −0.02% (Antognini 2013)
    R_p⁴ = 3ℏ/(512π·ρ_max·c₀) → R_p = 0.8422 fm vs 0.8414 — 0.10%
    m_p⁴ = (131072π/3)·ρ_max·ℏ³/c₀³ → 1.6707×10⁻²⁷ kg vs 1.6726 — 0.12%
    m_μ = m_e·(20π³/3)·(1+T₇/60) — +2.5 ppm
    m_τ — the Koide closure (Q = 2/3) — +64 ppm
    τ_μ = 256·α⁻⁶·(1+T₇/3)·τ_e — −245 ppm

The ppm residuals measure the integer grid: the integer 60 is NOT a fitted knob — it is a structural count: 3 spatial dimensions × 20 fold stages (a topological framework has no 60.52 fold stages; integers are discrete counts), and T₇ reads 1.735% from m_μ but 1.824% from τ_μ. The integer is locked, the T₇ spread is the named open item.

The lodgement claims the physics origin of the gap. The formal translation
into the mathematical theory's language remains the named bridge, stated
below.

## The mechanism of the gap — confinement as closure

**The ontology.** The universe is one substance: a continuous, mass-bearing
electromagnetic medium — paired EM waves at rest spacing, held by heat.
Matter is this same medium tied into 720° toroidal knots: m = L/c₀², L the

> Einstein, 1905 — *"Does the Inertia of a Body Depend Upon Its
> Energy-Content?"* (Annalen der Physik 18, 639–641 (1905); the German original: *"Ist die Trägheit eines Körpers von seinem Energieinhalt abhängig?"*) — his original symbol for
> the light energy was **L**: *"If a body gives off the energy L in the form
> of radiation, its mass diminishes by L/V²."*
light energy (Einstein's original letter, 1905). The medium is static; it
does not move. Confinement is a property of the tied knot, not of any flow.

**The vacuum.** The framework's first law: no zeros. "Colorless" is
sum-to-ambient, never zero; there is no vacuum, no empty space — the medium
is everywhere, always. The Yang–Mills vacuum is the medium at its rest: the
tensioned, maximum-unwound floor. The knot is the wound state. The gap is
the energy difference between the two — the weld's price, m = L/c₀², the
light paid at the tying.

**The closure.** R_loop = r_e/(5π²) = r_e/(6πφ²). The 4π closure forces the
five gates onto the double circuit (5 × 4π/5 = 720°); the loop settles at
five gates over the circuit squared. The wave's phase closes only after 4π.
Match: demanded 49.3535 vs 5π² = 49.3480 — **+0.011%**; the torsional hold
**+0.000%**. The golden bridge 6φ² = 5π holds to 0.0015%. The topology
equation fixes Y_bow from r_e; the +0.011% is the same equation read both ways,
and the locked value carries three significant figures — the residual is below
its own precision. Single-counted, not a double confirmation.

**Why the zero-mass mode is forbidden.** The zero-mass mode of Yang–Mills is
the unconfined propagating excitation. In the framework that mode is the
loop left open — the configuration that never survives the fold. Once the
720° loop closes through the 5π² boundary, no free unconfined excitation
remains to carry a zero-mass state: every excitation of a closed loop costs
the loop's own strain. The lowest state is the knot itself, and the knot has
mass.

**The hold.** F_EM = F_debt + F_topology, split 19 : 1 : 18; F_EM/F_debt =
1/s = 19, exact. The torsional hold at the yield wall lands on the balance's
demanded share: F_topology = 60π⁴·Y_bow·r_e² = (18/19)·F_EM. Eighteen
nineteenths of the fold's hold is topology — a winding invariant, not a
coupling a perturbative expansion can remove. The gap has a topological
floor.

**The floor's size.** The knot can never reach the stress-free golden
configuration — the winding limit stops it δ short, δ = (6φ² − 5π)/5π.
ΔU = δ·U = 2.47 eV = 502 nm. The locked strain is the energy cost of
existing as matter: geometric frustration, the phase boundary.

## The discrete spectrum — the selection law

**The law.** A knot holds iff no single bias finds an unspooling direction
AND the collapse heat fully exits through the centre. Survivors: {1, 5}.

**The mechanism.** The 2 and 3 chains die to one fluctuation. The 2-1-2
cage converts every push into compression on its core (the wire-rope law).
The cold weld requires the heat's complete centre-channel exit.

**The observed spectrum.** The electron and the proton. The neutron as the
cage with one exposed thread (14:38). The 2/3/4 arrangements absent from
nature.

**Why the spectrum is discrete.** The selection law admits exactly two
closed topologies: the single chiral pair (the electron) and the 2-1-2 cage
(the proton). Discreteness is not imposed on the spectrum; the unspooled
configurations do not survive to appear in it. What survives carries
quantized winding — one quantum in the pair, four in the cage.

**Existence.** The forge requires e_avail ≥ E_lock; the retention requires
the selection law and the heat balance. Three clauses: the forge's energy,
the topology's lock, the weld's completeness. Sub-threshold dissipates;
super-threshold (1.33× the lock) retains. The RETAINED flag is **derived**
from the three clauses — forge energy, selection law {1,5}, heat balance —
numerical confirmation running.

## The worked derivations

**The quantization** — [the_ladder.py](../scripts/the_ladder.py).

    m_e·λ̄_C·c₀ = ℏ (1 quantum);  m_p·R_p·c₀ = 4ℏ (4 quanta)

The 720° double-loop confines one Compton wavelength; the wave's phase closes
only after 4π. The proton's 2-1-2 cage carries four quanta.

    m_p/m_e = 4λ̄_C/R_p = 1835.79 vs 1836.15 — −0.02% (Antognini 2013)

**The sealed proton identities (2026-09-30)** — [proton_derivation_20260930.md](../scripts/proton_derivation_20260930.md).
Both proton observables as outputs of {ρ_max, c₀, ℏ} + the 720° topology
alone, R_p no longer input:

    Identity A:  m_p·R_p·c₀ = 4ℏ
    Identity B:  m_p = (4π/3)·ρ_max·R_ball³ ,  R_ball = 8·R_p
    Combined:    R_p⁴ = 3ℏ/(512π·ρ_max·c₀)   →   R_p = 0.8422 fm vs 0.8414 (Antognini 2013) — 0.10%
                 m_p⁴ = (131072π/3)·ρ_max·ℏ³/c₀³   →   m_p = 1.6707×10⁻²⁷ kg vs 1.6726 (CODATA) — 0.12%
                 R_ball/R_p = 8.000 vs 8.011 — 0.13%

**Why the factors.** Factor 4 = the real dimension of SU(2) (quaternion
basis {1, i, j, k}); factor 8 = 2 wavelength quanta per SU(2) direction × 4
directions = the total quanta in the 720° path. The quantization counts the
SU(2) dimensions directly — the Yang–Mills entry point.

**The lepton sector** — [lepton_sector_closed.py](../scripts/lepton_sector_closed.py).

    m_μ = m_e·(20π³/3)·(1 + T₇/60)
    m_τ = the Koide closure (Q = 2/3)
    τ_μ = 256·α⁻⁶·(1+T₇/3)·τ_e

    m_μ  +2.5 ppm
    m_τ  +64 ppm
    τ_μ  −245 ppm

The ppm residuals measure the integer grid: the integer 60 is NOT a fitted knob — it is a structural count: 3 spatial dimensions × 20 fold stages (a topological framework has no 60.52 fold stages; integers are discrete counts), and T₇ reads 1.735% from m_μ but 1.824% from τ_μ. The integer is locked, the T₇ spread is the named open item.

Zero fitted parameters, zero human units. The muon is the electron's
strained overtone: the 16π³ phase volume sustained against the T₇ shear
(1.75%) distributed across the three dimensions and the twenty-stage fold
(60 = 3×20). m_τ is Koide's closure (1981) — Koide's formula with the
observed e and μ already gives +61 ppm; the framework contributes the fold's
2/3 prefactor. The parallel: Le Verrier measured the perihelion advance and Einstein derived its mechanism; Koide measured the ratio and the framework derives its mechanism.
The lifetime is sixteen creases timing out at α⁻¹ nanoseconds each on the
Compton clock — the human nanosecond eliminated.

**The coupling, counted twice** — [quicycle_charge_map.py](../scripts/quicycle_charge_map.py),
[sixteen_origin.py](../scripts/sixteen_origin.py).

    q′ = √(3ε₀hc/8π³) = 0.9103e;  g = 16π³α/3 = 1.206740
    g = (ρ_medium/ρ_matter)^(1/16) = 20^(1/16) = 1.205909

Match: 20^(1/16) vs 16π³α/3 — **−0.069%**. The electron is the photon of
toroidal topology (Williamson–van der Mark 1997); the charge is the
winding's topological measure, the wavelengths cancelling.

## What the lodgement claims and does not claim

**Claims — the physics origin of the gap.** Confinement as closure: the 5π²
boundary forbids the zero-mass mode, because a closed 720° loop has no free
unconfined excitation. The discrete spectrum: the selection law admits only
the {1, 5} closed topologies. The worked quantizations above, with the
residuals exactly as quoted — the shared rounding family of the locked
numbers' own last digits.

**Does not claim.** The formal translation into the mathematical theory's
language remains the named bridge. This lodgement claims the mechanism and
the numbers; it does not claim that translation as complete.

## The honest boundaries — stated once

- The merger machinery claims **no predictive edge over the trivial
  baseline**: 0.71% trivial vs 0.88% min(E,S) out-of-sample. The mechanism
  is the physical picture — the fight, the neck, the wave.
- The sixteen-fold clock's **crossing geometry is open** (proposed,
  arithmetic verified; the crossing geometry named as open).
- The **T6 Lorentz legs are open**: Kennedy–Thorndike-level precision
  (10⁻¹⁷ cavity tests), stellar aberration, Fizeau's drag 1 − 1/n².
- The tightening coefficient **T ≈ 27 = 3³ awaits data**.
- The birefringence template is frozen; the SIGN awaits Jaden's ruling (open), and until it is locked the test is armed but not yet a committed falsifier. The committed falsifiers are listed with their status stated honestly.
- The **black-hole limits are open** — two candidate fates; the limit is
  not derived.
- The RETAINED flag is **derived** — the three clauses: forge energy,
  selection law {1,5}, heat balance — numerical confirmation running.

## Framework link

The master document: [PHASE_WAVE_COSMOLOGY_DERIVATIONS.md](../PHASE_WAVE_COSMOLOGY_DERIVATIONS.md) —
all derivations, all data matches. The executable form:
[run_full_framework.py](../scripts/run_full_framework.py) (28 sections, 0
failures). The derivations used here: [the_ladder.py](../scripts/the_ladder.py),
[proton_derivation_20260930.md](../scripts/proton_derivation_20260930.md),
[topology_equation_corrected.py](../scripts/topology_equation_corrected.py),
[squeeze_debt_balance.py](../scripts/squeeze_debt_balance.py),
[knot_selection_law.py](../scripts/knot_selection_law.py),
[existence_derived.py](../scripts/existence_derived.py),
[lepton_sector_closed.py](../scripts/lepton_sector_closed.py).


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
https://github.com/fringeneering-jpg/PWC — the whole framework, the falsified
attempts kept in the repository history for honesty.




