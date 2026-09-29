# Two-phase EOS from latent heat: P(rho, s) built strictly on L = c0^2

Status: T3 progress note. Continuum mechanics only. No statistical alignment
parameter (Onsager, Maier-Saupe, S(rho,T)), no thermal-cancellation
fraction, no galaxy rotation input. All content here stays inside T1's
allowed inputs (P(rho,s), c, G, rho_max, 3.23e11 N/kg) and does not touch
the sealed a_0.

Tags follow the convention of `pwc_state_mapping.md` and
`hdf_stress_ldf_squeeze_foundations.md`.

## 1. Premise

The medium is EM(+)/EM(-) waves paired at a resting distance; heat holds
the pairs apart where neighbour attraction and repulsion balance
(DERIVATION_BRIEF Section 1). Matter is medium knotted at maximum
compression. The two phases are separated by a first-order transition with
specific latent heat L per unit mass.

- **[PWC premise]** compression of waves into a knot expels heat
  (exothermic press).
- **[PWC premise]** untying of a knot back to paired medium absorbs heat
  (endothermic expansion).
- **[PWC premise, already in CLOSURE_SHEET Section 4]**
  L = c0^2 per unit mass. This is the transition scale; the same c^2 =
  latent heat identity that already sits on the closure sheet.

## 2. Two-phase EOS

Two states of the same substance.

**Locked phase (matter, rho = rho_max):** all latent heat expelled during
compression. The paired waves are aligned along one axis; pressure carries
in that axis:

    P_k(rho) = rho * c0^2
    c_s,k^2 = dP_k/drho = c0^2
    c_s,k   = c0                                    [Zel'dovich stiff, w=1]

- **[trial numerical closure]** the linear form P = rho*c0^2 for the fully
  locked phase, matching the Zel'dovich 1962 stiff-limit reference used by
  DERIVATION_BRIEF Section 7.

**Untied phase (paired medium, rho = rho_0):** latent heat L = c0^2 per
unit mass is absorbed during untying, redistributed isotropically across
the 3 spatial degrees of freedom. Pressure per axis:

    P_g(rho) = rho * c0^2 / 3
    c_s,g^2 = dP_g/drho = c0^2 / 3
    c_s,g   = c0 / sqrt(3)                          [radiation-like, w=1/3]

- **[trial numerical closure]** the 1/3 factor comes from L equipartitioned
  across 3 spatial DOF at the ordered end; no alignment order parameter S
  is introduced.

**Latent-heat identity across the transition:**

    Enthalpy jump per unit mass = L = c0^2

That single number is the whole thermodynamic content of the transition
in this note.

## 3. c_s reproduction

The Round 1 c_s values (DERIVATION_BRIEF Section 7, "Kept"):

- ordered resting medium: c_s = c0 / sqrt(3), w = 1/3
- locked medium at rho_max: c_s = c0, w = 1

fall out of the latent-heat form above **without invoking the S alignment
order parameter or Onsager/Maier-Saupe statistics.** Same c_s numbers,
plain continuum-mechanics derivation: c_s^2 = dP/drho of each phase's
linear EOS.

- **[tested numerical result]** substituting into a_hold(rho) =
  c_s(rho) * sqrt(4*pi*G*rho) from the Jeans-scale route already logged
  in DERIVATION_BRIEF Round 1:
  - rho_max = 1.304e15 kg/m^3, c_s = c0:
    a_hold(rho_max) = c0 * sqrt(4*pi*G*rho_max) = 3.14e11 N/kg
    (2.9% below the sealed 3.23e11; DERIVATION_BRIEF Section 7 flags this
    as consistency, not a first-principles derivation, since the shell at
    0.87 r_s forces c*sqrt(G*rho) near c^4/GM automatically.)
  - rho_0 = 8.74e-27 kg/m^3, c_s = c0/sqrt(3):
    a_hold(rho_0) = (c0/sqrt(3)) * sqrt(4*pi*G*rho_0) = 4.69e-10 m/s^2

## 4. What is NOT closed

The **prefactor gap at rho_0** stands unchanged from Round 1: 4.69e-10 vs
sealed a_0 window 6.7e-11 to 7.6e-11, i.e. ~6.2x to 7.0x off. Nothing in
this note closes that gap.

- **[open derivation]** the ratio 4.69e-10 / a_0 ~ 7x is NOT recovered from
  the density difference and volume-release scales alone. Direct checks:
  - rho_max / rho_0 = 1.49e41 -> log ratio 41.17, no factor ~7 emerges
  - Volume released per unit mass, Delta_v = 1/rho_0 - 1/rho_max ~ 1/rho_0
    = 1.14e26 m^3/kg. Multiplied against every dimensioned scale checked
    (Hubble length c/H_0, Schwarzschild scales, c^2/(G*rho*length),
    sqrt(G*L*rho)) fails to land at ~7x.
  - Linear packing scale (rho_max/rho_0)^(1/3) = 5.3e13 also not ~7.

The prefactor must come from an input this note does not supply.

## 5. Where the remaining prefactor has to come from

Pegged to T5 as an explicit input requirement. Two channels, either of
which supplies a specific mechanical number:

### 5.1. Delta_V_wave and cosmic-web packing geometry (primary channel)

- **[open derivation, T5]** Delta_V_wave = volume debt per tied wave
  (CLOSURE_SHEET T5). Once T5 gives its numeric value, the wave number
  density per unit mass at each phase is fixed:
  - n_wave/kg at rho_max: waves packed at rho_max
  - n_wave/kg at rho_0: waves at their resting spacing, expanded by
    (rho_max/rho_0) in volume; linear spacing ratio (rho_max/rho_0)^(1/3).

- **[PWC premise]** released waves in the untied phase do not fill 3D
  space isotropically at cosmic scales -- matter and its untied surround
  track filaments, sheets and walls (the cosmic web). The Jeans-scale
  4*pi solid angle at rho_max (spherical shell geometry, DERIVATION_BRIEF
  Section 2) is not the effective solid angle at rho_0.

- **[open derivation]** the effective solid-angle rescaling at rho_0.
  In the Jeans-form a_hold = c_s * sqrt(Omega_eff * G * rho), replacing
  Omega_eff = 4*pi at rho_max with Omega_eff = 4*pi / N at rho_0 gives a
  factor 1/sqrt(N) suppression of a_hold. Numerically: N = 49 lands
  a_hold(rho_0) at 4.69e-10 / 7 = 6.7e-11 = a_0 (sealed target).

- **[what T5 must supply]** the number N as a mechanical consequence of
  Delta_V_wave and the cosmic-web packing geometry, without any galaxy
  rotation input. Success = deriving N (or the equivalent Omega_eff) from
  Delta_V_wave, rho_0, rho_max, c0, G alone. Not committed here; committing
  it here would be a fit.

### 5.2. Coherence length of released waves (alternative)

- **[open derivation]** if the released waves stay phase-correlated over
  a length L_coh before dispersing, the effective Jeans-scale for gravity
  hold at rho_0 changes. L_coh / lambda_J(rho_0) is a dimensionless
  factor; if it equals 1/7 (or 1/sqrt(49) inside the sqrt), same closure
  drops out. L_coh must come from the same latent-heat mechanism (heat
  redistribution time and free-streaming length of the released waves),
  not fitted to a_0.

Either channel closes T1 without touching sealed data.

## 6. What is explicitly NOT done

- **No** S(rho, T) alignment order parameter
- **No** Onsager isotropic-to-nematic rod-length parameter
- **No** Maier-Saupe pair alignment coefficient
- **No** thermal-cancellation fraction (previously proposed
  "w_th ~ 0.98 balance"; withdrawn per direction)
- **No** use of a_0 as an anchor (sealed under T1)
- **No** H_0 ~ a_0 closure assumption

## 7. Committed status

- **[tested numerical result]** locked-phase c_s = c0 and untied-phase
  c_s = c0/sqrt(3) reproduce Round 1 kept values from L = c0^2
  equipartition, no statistical-mechanics parameter used.
- **[tested numerical result]** a_hold(rho_max) = 3.14e11 N/kg (2.9%
  consistency echo of the sealed 3.23e11).
- **[open derivation]** a_hold(rho_0) prefactor. Pegged to T5 Delta_V_wave
  and cosmic-web packing geometry as the mechanical input required to
  close it. Not closed here.

T1 remains open. This note narrows the open question from "derive the
c_s form and the prefactor" to just "derive the prefactor from T5's
Delta_V_wave and the cosmic-web packing geometry."
