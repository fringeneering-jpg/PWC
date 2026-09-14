# HDF stress / LDF squeeze foundations audit (supersedes the vector-A ansatz)

Status: theory audit only, no code run. The 1D scalar A,Pi model
(`dynamic_knot_HDF*.py`) and the vector-A ansatz in
`ldf_polarization_foundations_audit.md` are both DEPRECATED as candidate
core equations -- kept only as historical toy models. Nothing here is
claimed as complete PWC electrodynamics, a derived EOS, or a proven
stable Sintot.

## 1. Field-and-units table

All units given in the same implicit code-unit convention used throughout
this project (no independent physical length/time/density scale has ever
been fixed here).

| Field | Meaning | Tag |
|---|---|---|
| rho(x,t) | Total HDF volumetric density/state, 0 < rho_min <= rho <= rho_max < infinity | [PWC premise] for the bound; [trial numerical closure] for the specific EOS realizing it |
| u_i(x,t) | HDF bulk flow velocity. Restricted here to POTENTIAL flow, u_i = d_i(phi_u), i=1,2 in 2D -- **[PWC ansatz]**: a frictionless/inviscid medium has no restoring force for bulk shear flow, so an unconstrained rotational u_i would carry a passive, non-propagating, arbitrary DOF. Restricting to potential flow removes that redundancy rather than silently carrying it. |
| sigma_ij(x,t) | HDF stress. **[PWC ansatz, NOT independently dynamical]**: taken as a Cauchy-elastic (Hooke's-law-type) function of the current state, sigma_ij = P_bulk(rho)*delta_ij + 2*mu_T*epsilon_ij(a), where epsilon_ij(a) = (1/2)(d_i a_j + d_j a_i) is the strain built from the LDF displacement field a_i. It is a CONSTITUTIVE/diagnostic quantity, not an independently integrated field with its own inertia -- this choice is explained in Section 7. |
| a_i(x,t) | LDF transverse displacement/shear state. Constrained to div(a)=0 (purely transverse) -- see Section 5 (constraint count) for why the longitudinal part is removed rather than silently retained. |
| pi_i(x,t) | Conjugate LDF momentum, pi_i = d(a_i)/dt, same transversality constraint as a_i |
| chi(x,t) | Sintot lock-progress order parameter, chi~0 baseline HDF, chi~1 inside a Sintot region | [PWC ansatz] |
| e_int(x,t) | HDF internal energy ledger -- an explicitly EVOLVED (not diagnosed) conserved bookkeeping field, exactly the E_medium construction already validated in the scalar model (needed again here for the same reason: diagnosing energy from rho,u after the fact does not discretely conserve it for nonlinear states -- this was the confirmed root cause of the earlier 30-70% Cartesian energy-conservation bug, and the fix carries over unchanged in structure). | [trial numerical closure], its CONSTRUCTION METHOD is [tested numerical result] from the earlier debugging |

Density-contribution bookkeeping (NOT independently conserved fluids,
per instruction):

    rho = rho_HDF + delta_rho_LDF + delta_rho_Sintot
    delta_rho_LDF < 0        [PWC premise]
    delta_rho_Sintot > 0     [PWC premise]

This decomposition is used only for interpretation/diagnostics (e.g.
identifying which part of a rho perturbation "is" LDF vs Sintot at a given
point); it is not a separate set of evolved variables.

## 2. Candidate energy functional

**[PWC ansatz]** throughout.

    e_total =
        (1/2) rho * u_i u_i                                  [HDF kinetic]
      + U_HDF(rho, chi, e_int)                                [bulk + registration + ledger]
      + (1/2) kappa_rho (d_i rho)(d_i rho)                    [HDF density-gradient/surface term]
      + (1/2) kappa_chi (d_i chi)(d_i chi)                    [lock-field gradient/surface term]
      + (1/2) Z(rho,chi) pi_i pi_i                            [LDF kinetic, state-dependent inertia]
      + (1/2) C_T(rho,chi) (curl a)^2                         [LDF/HDF-stress SHARED transverse mode -- see Section 4]
      + V_lock(rho, chi)                                      [same double-well+registration form as before, NOT re-derived, reused only as a provisional closure]

  where U_HDF(rho,chi,e_int) = e_EOS(rho) + V_lock(rho,chi) + e_int (the
  ledger term e_int enters additively, tracking whatever energy the
  exchange construction moves into/out of the medium beyond what the
  bare EOS+V_lock terms already carry).

  NO (div a)^2 term is included -- see Section 5: this term would
  duplicate the compressional mode already carried by (rho, u_i), so it
  is removed by the transversality constraint rather than assigned a
  free coefficient C_L and left to silently coexist with ordinary sound.

## 3. Constraint count: physical degrees of freedom (2D)

**[derived from ansatz]** -- this section directly addresses the
instruction not to silently leave extra observable propagation modes.

  - rho + potential flow (phi_u): ONE compressional/acoustic branch
    (exactly the existing scalar-model sound mode, unchanged in kind).
  - a_i constrained to div(a)=0: in 2D this leaves exactly ONE independent
    transverse component (a 2D transverse vector orthogonal to a given
    propagation direction has 1 remaining freedom, matching a single
    "polarization" state in 2D -- 3D would give 2, as in the earlier
    vector-ansatz audit). Paired with pi_i under the same constraint:
    ONE transverse propagating branch.
  - chi + its own conjugate momentum: ONE lock-progress branch.
  - sigma_ij: NOT an independent branch -- it is fully determined
    algebraically by the state of (rho, a_i) at each instant (Section 1).
    Counting it as dynamical would double-count the same physical
    information already carried by rho and a_i.

Total: THREE independent propagating branches in this 2D ansatz --
compressional (rho/u), transverse LDF/stress (a/pi), lock-progress
(chi/Pi_chi). No redundant or unaccounted mode is left over. This directly
resolves the instruction's specific concern about extra silent DOF: the
potential-flow restriction on u_i and the transversality constraint on a_i
are the two places redundancy was found and explicitly removed, not
carried forward unlabeled.

## 4. Derived PDEs, stress, and conserved currents

**[derived from ansatz]**

  Continuity:   d(rho)/dt + div(rho*u) = 0   (u_i = d_i phi_u)
  HDF momentum: d(rho*u_i)/dt + d_j(rho*u_i*u_j + P_bulk*delta_ij) = 0
                P_bulk = rho*d(e_EOS+V_lock)/d(rho)|_chi - (e_EOS+V_lock)
                (same Legendre construction as before; no extra stress
                term from a_i enters the FLUID momentum flux, for the
                same reason established in the earlier Cartesian
                debugging -- a_i is not advected with u_i, so no
                Korteweg-type addition is justified without a matching
                exchange term, which is instead handled explicitly below)
  LDF/stress wave equation (the SHARED branch):
                d(a_i)/dt = pi_i
                d(pi_i)/dt = C_T(rho,chi)*curl(curl(a))_i - dV_lock/da_i-equivalent-term
                (with V_lock built from chi, not a_i directly, per
                Section 1 -- so the only source term here is whatever
                dV/da the chosen functional supplies; with the functional
                in Section 2, dV/da = 0 identically, i.e. a_i propagates
                as a FREE transverse wave at speed sqrt(C_T), UNLESS a
                chi-a coupling term is explicitly added, which is left
                open here rather than inserted to force a particular
                interaction)
  Lock-progress equation:
                d(chi)/dt = Pi_chi   (no u.grad(chi) advective term
                included, since chi is not advected with the bulk flow in
                this ansatz -- consistent with how the scalar model's phi
                previously was NOT advected either, once it became a
                genuine wave-carrying field)
                d(Pi_chi)/dt = kappa_chi*grad^2(chi) - dV_lock/dchi
  Energy exchange (same construction validated in the scalar model):
                d(e_int)/dt + flux-divergence = +Pi_chi * d(V_lock)/d(rho)
                matching the corresponding sink in the momentum/EOS
                sector, by the same by-hand + finite-difference-verified
                method already established as reliable.

  Stress tensor: sigma_ij = P_bulk*delta_ij + 2*mu_T*epsilon_ij(a), with
  mu_T identified with C_T (the same coefficient sets both the transverse
  wave speed AND the shear-stress response -- this is what makes the
  "HDF stress/gravity branch" and "LDF transverse squeeze branch" the
  SAME propagating mode by construction, not two independently-tunable
  branches that happen to coincide. This is an honest simplification,
  flagged explicitly in Section 7, not oversold as two independently
  derived branches.

  Conserved linear momentum: by translational invariance of the
  (homogeneous-medium) functional, P_i = integral[rho*u_i + pi_j*d_i(a_j)] dV.

  Conserved angular momentum: in 2D, a_i's transversality constraint
  leaves only 1 component per point, so there is no internal component-
  mixing "spin" current the way a genuine >=2-component vector field
  would carry (unlike the earlier vector-A audit's 3D case) -- angular
  momentum here is purely ORBITAL, L = integral[epsilon_ij * x_i *
  (momentum density)_j] dV. This is an important, honest difference from
  the earlier vector-ansatz audit and should not be conflated with it.

## 5. Linear-mode dispersion calculation

**[derived from ansatz]**

Linearizing about rho=rho_bg, u=0, a=0, chi=0:

  Compressional branch: omega_sound(k) = c_s(rho_bg)*|k|, where
  c_s(rho_bg) = sqrt(dP_bulk/drho at rho_bg) -- exactly the same EOS
  sound-speed construction as the scalar model, unchanged.

  Transverse LDF/stress branch: omega_T(k) = sqrt(C_T(rho_bg,0)) * |k| --
  a genuinely LINEAR (non-dispersive) dispersion relation IF C_T is taken
  constant, in contrast to the earlier vector-A ansatz where a mass-like
  term from V_lock's curvature made the LDF branch dispersive. Here, since
  V_lock depends on chi (not a_i), a_i's own linearized equation has NO
  mass term at all -- dV/da=0 identically in this functional -- so this
  branch is exactly luminal at all k, with speed c_T = sqrt(C_T(rho_bg,0)).

  Lock-progress branch: omega_chi(k)^2 = kappa_chi*k^2 + m_chi^2, where
  m_chi^2 = d^2(V_lock)/d(chi)^2 at chi=0 (the SAME kind of linear/mass
  term found before, but now confined entirely to the chi branch, not
  contaminating the LDF/stress branch -- a genuinely different, cleaner
  separation than the vector-A ansatz achieved).

  Requirement "the same c must arise from the same baseline material
  coefficients": in this construction, c_s (compressional) and c_T
  (transverse) come from DIFFERENT coefficients (dP_bulk/drho vs C_T) --
  there is currently NO derived reason they should be numerically equal,
  let alone equal to a single universal c. Setting c_T = c_s = c would
  currently be an IMPOSED calibration choice, not a derived consequence.
  This is stated plainly as **[open]** rather than assumed.

## 6. Verdict on the three required checks

  (a) Does the functional produce an HDF stress/gravity branch? **Yes, by
      construction** -- but as literally the SAME mode as (b), not an
      independently-derived branch that happens to coincide with it. This
      is a real limitation, not a strength, and is flagged rather than
      oversold.

  (b) Does it produce a transverse LDF squeeze branch? **Yes** -- a_i's
      transverse wave equation, luminal at speed c_T = sqrt(C_T), with no
      dispersion in this functional (dV/da=0).

  (c) Does the SAME speed c arise from the same baseline material
      coefficients for both branches? **Not currently** -- c_s and c_T
      are set by independent coefficients (dP_bulk/drho vs C_T) with no
      derived relation between them. Imposing c_T=c_s=c right now would
      be a calibration, not a derivation. **[open]**.

## 7. Explicit list of every ansatz/premise/open item in this document

  [PWC premise]: HDF as the real finite background medium; LDF as a
    lower-volumetric propagating state advancing by sequential squeezing
    (not through nothing); Sintot as a localized pressure-locked state;
    the density bound 0<rho_min<=rho<=rho_max<infinity; c_HDF,stress =
    c_LDF,max = c as a stated causal constraint (NOT yet derived here --
    see Section 6c).

  [PWC ansatz]: potential-flow restriction on u_i; sigma_ij as a
    constitutive (non-dynamical) Cauchy-elastic function of (rho,a_i)
    rather than an independently evolved field; the specific energy
    functional in Section 2; identifying the "gravity/stress" branch with
    the "LDF transverse" branch as literally the same mode; reuse of the
    scalar model's V_lock/e_EOS FORMS as provisional placeholders (NOT
    claimed re-derived for this new ontology).

  [derived from ansatz]: the constraint-count/DOF argument (Section 3);
    the PDEs, stress tensor, and conserved currents (Section 4); the
    linear dispersion relations (Section 5).

  [open]: why c_T should equal c_s (no derivation yet); any dV/da(chi)
    coupling term connecting chi to a_i's dynamics (currently zero in
    this functional, meaning chi and a_i do not yet interact at all,
    which likely needs to change before any LDF-to-Sintot locking test
    is meaningful); the charge/antiparticle-label problem (carried over
    unresolved from the earlier vector-A audit); a genuine 3D extension
    (this document is 2D only, as instructed for the initial pass).

  [not supported]: any claim that this functional is a finished PWC
    electrodynamics, that HDF's EOS is established, that a stable
    topological Sintot has been shown, that zero drag is proved, or that
    this reproduces any specific experimental number (STAR, E-144, LUXE,
    E320 all remain untouched by this document).

## 8. Smallest grid-converged 2D simulation (specification only -- not built)

  - 2D, fields (rho, phi_u [or u_i with div/curl decomposition enforced],
    a_transverse, pi_transverse, chi, Pi_chi, e_int)
  - Baseline stability check (rho=rho_bg, u=0, a=0, chi=0): trivial, same
    kind of check already validated in the 1D radial model
  - Weak free-wave test for EACH of the three branches separately
    (compressional, transverse a, lock-progress chi), confirming: (i) the
    compressional branch reproduces the existing 1D sound speed, (ii) the
    transverse a branch propagates at a CONSTANT (non-dispersive) speed
    c_T for all tested k (a genuinely different, checkable prediction of
    THIS functional vs. the earlier vector-A ansatz's dispersive result),
    (iii) chi's branch shows the expected m_chi-based dispersion
  - Energy/mass/linear-momentum conservation verified via the SAME
    instantaneous per-RHS budget audit technique already established as
    reliable (this is not optional -- it is what caught the real 30-70%
    bug in the Cartesian model and must be run again before trusting any
    result from this new field content)
  - Only after all of the above: consider whether/how to add a chi-a
    coupling term (currently absent, per Section 7's [open] list) before
    attempting anything resembling an LDF-to-Sintot locking test

No such code has been written or run. This document is the specification
only, per instruction.
