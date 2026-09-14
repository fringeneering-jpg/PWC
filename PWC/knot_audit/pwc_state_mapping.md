# PWC state mapping v2: tri-state bedrock, tagged by evidentiary status

Supersedes the first version of this file. That version implied more than
is established -- it read as if the trial V_lock functional and its
double-well barrier were the derived PWC locking law. They are not. This
version tags every claim so premise, calibration setup, trial-model
mathematics, open derivation targets, and actually-tested numerical results
are never blurred together.

Tags used below:
- **[PWC premise]** -- part of the theory's stated ontology, asserted by
  the user, not something this code derives or tests.
- **[experiment/calibration context]** -- framing borrowed from real
  experimental reference material (e.g. pair production) to motivate a
  test, not itself a PWC derivation.
- **[trial numerical closure]** -- a specific mathematical form (V_lock,
  the EOS, the wave equation) chosen to build a runnable reduced model.
  It is A candidate closure, not THE physical law.
- **[open derivation]** -- a mechanism PWC claims exists but that this
  code has not derived or established. Listed explicitly so it is never
  accidentally treated as settled.
- **[tested numerical result]** -- an actual number this session measured
  by running code, with its own verified uncertainty.

## Bedrock definitions

| Term | Definition | Tag |
|---|---|---|
| **HDF** | The real, finite, nonzero background medium of space. Not a vacuum, not literal nothing. | [PWC premise] |
| **LDF** | Propagating energy-wave states within HDF: photon/light, gamma, RF, infrared, radiation, heat, and neutrino-like propagation. | [PWC premise] |
| **Sintot (matter)** | A finite local pressure-locked/knot state of the same medium. | [PWC premise] |
| **Cavitation** | Relative low pressure in the one medium. Never a zero-density, zero-pressure void. | [PWC premise] |
| **Physical bounds** | 0 < rho_min <= rho <= rho_max < infinity | [PWC premise] |

## Transition directions

| Direction | Reading | Tag |
|---|---|---|
| LDF + sintot -> HDF | The ordinary equalisation/material-transformation direction: light and matter both relax back toward the baseline medium state over time. | [PWC premise] |
| LDF + LDF -> sintot | The exceptional reverse event: two energy-wave configurations locking into a matter state under anchored energy-to-matter conditions. This is the PWC reading of the pair-production reference material -- an unusual local reversal/locking within the real HDF medium, NOT creation from literal nothing. | [PWC premise] + [experiment/calibration context] |

## What is explicitly NOT established (must not be stated as derived)

- HDF having a particular absolute "incredibly high expansive pressure" -- **[open derivation]**
- Every sintot region sitting at rho_max -- **[open derivation]**
- A sintot region being topologically stable -- **[open derivation]**
- V_lock (the trial double-well + B-registration functional) being THE physical PWC locking law -- it is **[trial numerical closure]** only
- The double-well barrier height (Lambda/16 in the trial functional) being THE E_lock condition -- **[trial numerical closure]**, not [PWC premise]
- A pressure-deficit / inward-HDF-flow / gravity mechanism -- **[open derivation]**, not yet attempted in this code

## Code variables used so far, tagged

| Code object | What it currently represents | Tag |
|---|---|---|
| rho, u (fluid sector) | A trial stand-in for local HDF medium density/flow, bounded above by rho_max in the EOS | [trial numerical closure] |
| A, Pi (wave sector) | A trial stand-in for an LDF propagating mode, given second-order wave dynamics | [trial numerical closure] |
| e_EOS(rho) = A_param*(-ln(1-rho/rho_max)-rho/rho_max) | A chosen finite-compression closure enforcing rho<rho_max; not derived from any deeper PWC compressibility law | [trial numerical closure] |
| V_lock(rho,A) = Lam*A^2*(1-A)^2 + (B/2)*(rho-rho_bg-drho*A)^2 | A chosen double-well + registration closure used to test whether SOME functional of this general shape can support locking; not asserted as the actual PWC mechanism | [trial numerical closure] |
| E_lock = rho_knot*c0^2 | A dimensional-bridge guess for a locking energy scale, used only to pick calibration amplitudes for a numerical test | [trial numerical closure] |
| The 3e-6 total-energy-conservation result (spherical solver, weak shell test) | An actual measured number confirming the CODE's flux-form E_medium construction conserves energy as built | [tested numerical result] |
| The linear/mass-like term found in dV_lock/dA at A=0 (m_eff^2 = 2*Lambda+B*drho^2, matching the measured ~1.66 vs c0=1.9 propagation speed at k_wave=2) | An actual measured/derived consequence of the CHOSEN trial V_lock closure -- a property of this specific trial functional, not a claim about real HDF/LDF physics | [tested numerical result] about a [trial numerical closure] |
| "Equalisation" as continuous small-amplitude energy exchange between the A,Pi sector and the rho,u+V_lock sector | Observed behavior of the trial closure at low amplitude; offered as a plausible READING consistent with the PWC premise (LDF+sintot->HDF direction being always-active at small perturbation), not a proof that this is how real equalisation works | [tested numerical result] interpreted against [PWC premise] |
| The Cartesian 1D packet-collision negative result (R_focus<=1 for all tested k_wave/sigma) | An actual measured result about THIS trial closure and THIS packet geometry only | [tested numerical result] |

## Status and next required step (per instruction)

No further solver sweep is authorized until the physical HDF/LDF/sintot
transition rule and the attraction/cavitation mechanism are specified in
plain mechanical terms. That specification is the next open item, and it
precedes any resumed numerical work -- including any leakage-rate scan,
the deferred radial-solver focusing/resolution checks, and any Test A/B
run.
