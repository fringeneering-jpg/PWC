# LDF polarization/stress foundations audit (provisional next layer)

Status: theory audit only. No simulation run. No experiment fitting
attempted. Nothing here is claimed as a completed PWC electrodynamics.

Labels used throughout: [PWC premise], [AI Studio candidate], [PWC ansatz],
[derived from ansatz], [open], [not supported].

## 1. Can an isotropic HDF medium support a transverse mode without contradiction?

**[derived from ansatz], with a flagged tension against prior framing.**

A medium supports a propagating TRANSVERSE (shear) mode only if it has some
restoring response to shear strain -- an ordinary inviscid, zero-shear-
rigidity fluid (the literal reading of "frictionless, zero-viscosity
superfluid" used elsewhere in this project) supports ONLY longitudinal
(compressional) sound-like excitations. A single SCALAR order parameter
(the existing A(x,t)) has no internal structure that could rotate into a
transverse mode -- it is compressional by construction.

Two honest routes exist:
1. Give the medium genuine elastic shear rigidity -- this contradicts the
   "frictionless/zero-viscosity" language used earlier in this project and
   is not adopted here.
2. Give the LDF field an INTERNAL vector degree of freedom (additional
   components beyond a single scalar) that can rotate into itself under
   spatial rotation, without requiring the BULK medium itself to resist
   shear (analogous to how superfluid He-3's vector/tensor order parameter
   carries internal orientation without the fluid having ordinary elastic
   rigidity, or how the electromagnetic field's transverse polarization
   comes from gauge structure, not material shear). Route 2 is adopted
   below as the candidate extension. **[PWC ansatz]**

## 2. Minimum field content for a 2D/3D HDF-LDF extension

**[PWC ansatz]** -- explicitly not claimed to equal standard
electrodynamics.

  rho(x,t)         -- HDF baseline density (unchanged)
  u_i(x,t)         -- HDF medium's own (longitudinal) flow velocity (unchanged)
  A_i(x,t)         -- LDF vector field, i=1..d (d=2 or 3); decomposes as
                       A_i = d_i(A_long) + A_trans,i  (Helmholtz split),
                       with the transverse part A_trans,i carrying the
                       candidate polarization information. The longitudinal
                       part reduces to the scalar A already used in the 1D
                       model.
  Pi_i(x,t)        -- conjugate momentum, Pi_i = dA_i/dt
  chi(x,t)         -- a NEW scalar lock-progress order parameter, distinct
                       from A_i itself. chi, not A_i directly, plays the
                       role the old scalar A played in V_lock. This
                       decouples "how much LDF energy is passing through a
                       point" (A_i, Pi_i -- oscillatory, sign-changing)
                       from "how locked is this point" (chi -- a slower,
                       double-well order parameter driven by local LDF
                       stress invariants). Its own conjugate momentum
                       Pi_chi is included so it retains genuine (not purely
                       relaxational) dynamics, consistent with how A was
                       treated in the 1D model.

All units below are expressed in the SAME implicit code-unit convention
already used throughout this project (PARAMS are dimensionless "code
units"; no independent physical scale for length/time/density has ever
been fixed in this project). This is stated plainly rather than implying a
false precision.

## 3. Most general lowest-order rotationally invariant energy functional

**[PWC ansatz]**

    e_total =
        (1/2) rho * u_i u_i                                    [kinetic, existing]
      + e_EOS(rho)                                              [bulk EOS, existing]
      + (1/2) Pi_i Pi_i                                         [LDF kinetic]
      + (c_L^2/2) (d_i A_i)^2                                   [LDF longitudinal gradient]
      + (c_T^2/4) (d_i A_j - d_j A_i)(d_i A_j - d_j A_i)         [LDF transverse/shear gradient]
      + (1/2) m_A^2 * A_i A_i                                   [LDF "mass"/dispersion term]
      + Lam * chi^2 (1-chi)^2                                   [double well in chi, existing form]
      + (B/2) (rho - rho_bg - drho*chi)^2                       [chi-rho registration, existing form]
      + (kappa_g/2) (d_i chi)(d_i chi)                          [chi's own gradient/surface term]
      + g_1 * chi * A_i A_i                                     [NEW: lowest-order coupling of chi to the LDF invariant |A|^2]

  Coefficients (code-unit dimensions only, given no fixed physical scale exists):
    c_L^2, c_T^2 : [length^2/time^2]  -- independent longitudinal/transverse LDF speeds
    m_A^2        : [1/time^2]
    Lam, B       : as in the existing scalar model
    kappa_g      : [length^2] x [existing chi-energy-density units]
    g_1          : [existing chi-energy-density units] / [A_i A_i units]

  Higher-order terms (e.g. lambda_A*(A_i A_i)^2, a g_2*chi*Pi_iPi_i kinetic
  coupling) are allowed by symmetry but omitted here for tractability --
  the g_2-type coupling in particular would give chi a field-dependent
  "mass matrix" for Pi_i, complicating the canonical structure, and is
  explicitly deferred, not silently assumed away.

## 4. Derived equations of motion, stress, and conserved quantities

**[derived from ansatz]**

  Continuity:      d(rho)/dt + d_i(rho u_i) = 0
  Momentum:         d(rho u_i)/dt + d_j(rho u_i u_j + P_bulk delta_ij) = 0
                     P_bulk = rho*d(e_EOS+V_lock)/d(rho)|_chi - (e_EOS+V_lock)
                     (SAME Legendre construction as the scalar model; the
                     LDF vector sector does NOT inject an extra stress term
                     into the fluid momentum flux, for the same reason
                     established in the Cartesian debugging: A_i is not
                     advected with u_i, so no Korteweg-type addition is
                     justified here either -- confirmed by the same kind
                     of by-hand + exchange-source construction used before).
  LDF wave eq:       dA_i/dt = Pi_i
                     dPi_i/dt = c_L^2 * d_i(d_j A_j) + c_T^2*[grad^2 A_i - d_i(d_j A_j)]
                                - m_A^2*A_i - 2*g_1*chi*A_i
  Lock-progress eq:  dchi/dt = Pi_chi
                     dPi_chi/dt = kappa_g*grad^2(chi)
                                - [2*Lam*chi(1-chi)(1-2chi) - B*drho*(rho-rho_bg-drho*chi) + g_1*A_iA_i]
  Medium energy exchange (same construction as the scalar model):
                     dE_medium/dt + flux-divergence = +Pi_chi * dV/d(chi)_from_rho-coupling term
                     (i.e. the SAME kind of exchange source as before, now
                     attached to chi rather than directly to A)

  Symmetric LDF stress tensor (standard elastic-medium form, relabeled --
  NOT claimed to be the Maxwell stress tensor):
    T_LDF,ij = c_L^2*(d_k A_k)*delta_ij + c_T^2*[(d_iA_j+d_jA_i) - (d_kA_k)*delta_ij]

  Conserved energy: E_total = integral[e_total] dV -- conserved by the same
    time-translation-invariance argument used throughout this project
    (verified numerically in the scalar case to ~1e-4-1e-5; not yet
    verified numerically for this vector extension since no code exists
    for it yet).

  Conserved linear momentum (translational invariance, homogeneous medium):
    P_i = integral[rho*u_i + (LDF field-momentum density)_i] dV,
    field-momentum density_i = -Pi_j * d_i A_j (standard Noether current
    for a vector field under spatial translation).

  Angular momentum current -- **this is the key new object**: because
  A_i has >=2 independent components that can rotate INTO EACH OTHER
  under a spatial rotation, the field carries, in addition to ordinary
  ORBITAL angular momentum (r x momentum-density), an INTRINSIC ("spin")
  angular momentum density:
    S_k = epsilon_kij * Pi_i * A_j
  This is the standard Noether construction for the internal (component-
  mixing) part of a rotation acting on a vector field, directly analogous
  to the E x A spin-density construction for the electromagnetic field --
  it is DERIVED from the ansatz's having >=2 field components, not
  assumed or borrowed from electrodynamics.

## 5. Operational definitions

  Linear LDF polarization **[PWC ansatz, operational]**: A_i(x,t) =
    e_i * a(k.x - c_T*t) for a fixed real unit vector e_i transverse to
    the propagation direction k_hat.

  Circular LDF polarization **[PWC ansatz, operational]**: A_i(x,t) =
    a*[e1_i*cos(phase) + e2_i*sin(phase)] for two orthonormal transverse
    vectors e1, e2 -- exists because 3D (or the in-plane 2D case) admits
    2 independent transverse directions per propagation axis.

  LDF helicity/spin analog **[derived from ansatz]**: YES, present --
    the spin density S_k above is generically nonzero for circular
    polarization and time-averages to zero for linear polarization,
    matching the standard photon-spin analogy structurally.

  Sintot pair's opposite charge/state label **[open]**: NOT present in
    this ansatz. Nothing in the current field content (rho, A_i, chi) has
    a conserved U(1)-like "charge" quantum number. Producing genuinely
    oppositely-"charged" Sintot_e- / Sintot_e+ analogs would require
    promoting chi (or an additional field) to a COMPLEX order parameter
    with its own phase symmetry, giving a Noether-conserved charge via the
    standard complex-scalar-field construction. This is not part of the
    current ansatz and is stated plainly as missing, not assumed solvable.

## 6. Symmetry check: allowed harmonic structure, before fitting any data

**[derived from ansatz]**

Every term in the Section 3 energy functional is manifestly EVEN in A_i
(built from A_iA_i, gradient-squared combinations, and chi*A_iA_i -- no
term linear or cubic in A_i appears). This means the ansatz's "linear
polarization" direction e_i has the same 2-fold (director, not true
vector) ambiguity that a real photon's linear polarization has: A_i and
-A_i describe the same physical oscillation. Any physical rate or cross
section built from this functional can therefore only depend on the
relative-polarization angle through EVEN functions of it -- structurally
permitting a Fourier expansion in cos(2*Delta_phi), cos(4*Delta_phi), ...
and FORBIDDING cos(Delta_phi), cos(3*Delta_phi), ... by this symmetry
alone, independent of any specific Gamma_lock kernel.

This is as far as symmetry alone can go. It does NOT determine whether
A_2 is zero, what value A_4 takes, or the relative size of the two
harmonics -- those require an actual dynamical Gamma_lock derivation,
which has not been attempted.

## 7. Assessment of AI Studio's specific claims

| Claim | Verdict | Reasoning |
|---|---|---|
| A_2,PWC = 0 exactly | **[underdetermined]** | No Gamma_lock kernel has been derived to check this against; nothing in Section 6's symmetry argument forces A_2=0 specifically (it only shows A_2 is *allowed*, on the same footing as A_4) |
| \|A_4,PWC\| = 1/6 | **[underdetermined]** | Same reason -- no dynamical calculation exists yet. Flagged concern: 1/6 ~= 0.167 is the well-known closed-form leading-order QED coefficient for this exact process. A "PWC-derived" value landing on the standard QED number without an independent derivation chain is a real red flag for copying/pattern-matching rather than derivation, and should be treated with suspicion until a genuinely independent PWC-side calculation is shown |
| STAR acceptance shifts it to ~0.168 | **[underdetermined]** | Depends on the (undone) dynamical calculation plus a real detector-acceptance convolution, neither of which has been attempted here |
| P_perp ~= 38.1 MeV follows from a 2-3 fm knot scale | **[underdetermined]** | No relation between a Sintot knot's spatial scale and outgoing transverse momentum has been derived anywhere in this project; this would require an actual dynamical calculation connecting knot size to final-state kinematics, not yet attempted |

None of these four claims are treated as inputs, targets, or PWC results.

## 8. Smallest simulation that could test this ansatz (specification only -- not run)

  - 2D (not 1D): fields rho, u_i (i=1,2), A_i (i=1,2), Pi_i (i=1,2), chi, Pi_chi
  - Domain: doubly-periodic (consistent with prior Cartesian work) for the
    first pass; an absorbing/open boundary variant as a follow-up
  - Initial condition: two transverse (or mixed longitudinal+transverse)
    wave packets with specified linear polarization directions e_1, e_2 at
    a controlled relative angle, converging toward a common region --
    genuinely 2D, so an actual impact-parameter/Delta_phi observable can
    be defined for the first time
  - Finite-density HDF background (rho_bg > 0), as before
  - chi as the explicitly-labeled provisional lock variable (never
    asserted to BE Sintot without qualification)
  - Event-by-event checks: total energy, total 2D linear momentum, AND
    total angular momentum (S_k above plus orbital contribution) --
    verified via the same instantaneous per-RHS budget audit already
    established as reliable for the scalar model
  - Grid-refinement tests (Nx, Ny at multiple resolutions) before trusting
    any output, exactly as required for the scalar model

## 9. Decision gate -- what must happen before ANY experiment comparison

Not yet done, and required before Section 1 of the benchmark protocol
(defining theta_PWC, I_1, I_2, etc.) can be attempted honestly:

  1. Derive an actual Gamma_lock kernel from the Section 3-4 functional
     (currently only symmetry-ALLOWABILITY of cos(2*Delta_phi)/cos(4*Delta_phi)
     is established -- no coefficient values).
  2. Resolve the [open] charge/antiparticle-label problem (needs a
     complex/U(1)-carrying field extension not present in this ansatz).
  3. Build and verify a working 2D implementation with confirmed energy,
     linear-momentum, AND angular-momentum conservation (none of this
     exists in code yet -- Section 8 is a specification, not a build).
  4. Confirm grid-convergence of any candidate Gamma_lock-driven
     observable in that 2D code.
  5. Only then begin the benchmark protocol's own Stage 1 (fit a minimal
     theta_PWC to ONE calibration subset, freeze it, predict the rest).

No STAR, E-144, LUXE, or E320 comparison is attempted in this document.
