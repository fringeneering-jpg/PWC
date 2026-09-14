# One-continuum HDF/LDF/Sintot foundations (supersedes ALL prior field-split constructions)

Status: theory audit only, no code run. This document supersedes and
corrects `hdf_stress_ldf_squeeze_foundations.md` and
`ldf_polarization_foundations_audit.md` in full -- both split the medium
into two inventories (HDF fields + a separately-invented LDF field
needing a coupling term), which is the same category error regardless of
whether the second inventory was a scalar (chi) or a vector (a_i). The
1D scalar (rho,u,phi) toy model remains deprecated as a candidate core
equation set, kept only as historical scaffolding.

## The correction, stated plainly

There is ONE mass-bearing continuum, not two things needing to be joined:

    rho(x,t)     -- mass density of the one real space-medium
    theta(x,t)   -- phase/organization state of the SAME medium
    u(x,t)       -- transport velocity of the SAME medium

P(x,t) is NOT an independently evolved field -- it is a constitutive
(equation-of-state) quantity, P(rho,theta), consistent with how pressure
has been derived throughout this project's earlier (now-superseded) work.

  HDF    = the regime rho ~= rho_base, theta slowly varying              [PWC premise]
  LDF    = a propagating phase differential in theta and/or a density
           deficit (delta_rho<0) relative to local HDF -- NOT a separate
           substance, field, or inventory                                 [PWC premise]
  Sintot = a localized regime where theta=theta_lock, rho=rho_lock (a
           locked/organized state of the SAME field, not an additional
           order parameter appended to it)                                [PWC premise]

`rho_space > 0` everywhere (no physical volume has zero mass), and gravity
sources from the TOTAL density:

    rho = rho_HDF + rho_Sintot_excess     [PWC premise]

NOT rho = rho_matter + rho_mysterious_external_halo. There is no separate
dark-matter-like inventory in this ontology -- the "extra" gravitational
pull attributed elsewhere to dark matter is, in PWC, simply the
gravitational contribution of the real, nonzero mass of HDF space itself.

## Base equations

    d(rho)/dt + div(rho*u) = 0
    d(rho*u)/dt + div(sigma) = -rho*grad(Phi)
    grad^2(Phi) = 4*pi*G*rho

    sigma = -P(rho,theta)*I + tau(rho,theta, grad(rho), grad(theta))

**[PWC premise]** for the structural form; **[PWC ansatz]** for any
specific P and tau realizing it (not yet specified beyond this section).

## Closing u to theta -- the one closure this ontology needs

The field table lists u and theta as separate roles, but if they were
independently free, "phase/organization state" and "transport velocity"
would again be two things needing a relation between them -- the same
kind of gap that produced the earlier category error. The natural,
minimal closure, consistent with "LDF = a phase differential" and with
the "frictionless superfluid" language used throughout this project, is:

    u = (hbar_eff/m_eff) * grad(theta)      **[PWC ansatz]**

i.e. theta plays the role of a SUPERFLUID PHASE, and flow is literally
its gradient -- not a separate independently-specifiable field. This is
not an arbitrary invention: it is the standard closure of real superfluid
(Bose-Einstein condensate) hydrodynamics, and adopting it explicitly lets
the rest of this document borrow ALREADY-ESTABLISHED, real physics rather
than inventing new closures from scratch.

## Realizing "one equation of state and one organization energy" with real physics

The task requires specifying one P(rho,theta) and one e(rho,theta,
grad(theta)). Rather than inventing another ad hoc double-well (as the
deprecated chi/A constructions did), the closure above makes the
Gross-Pitaevskii / Madelung framework a directly available, well-
established candidate -- **[PWC ansatz]**, but grounded in real,
independently-verified physics, not fabricated for this project:

  Write psi(x,t) = sqrt(rho) * exp(i*theta). If psi obeys the standard
  Gross-Pitaevskii equation

    i*hbar_eff*d(psi)/dt = -(hbar_eff^2/2m_eff)*grad^2(psi) + g*|psi|^2*psi + m_eff*Phi*psi

  then the Madelung transformation gives EXACTLY the base equations above,
  with:

    P(rho) = (g/2)*rho^2                              [the GPE's own bulk/EOS term]
    Q_quantum(rho) = -(hbar_eff^2/2m_eff^2) * grad^2(sqrt(rho))/sqrt(rho)
                     ["quantum pressure" / Bohm potential -- a REAL,
                      DERIVED gradient-energy term, not an arbitrary
                      kappa_rho*|grad(rho)|^2 guess]

  This is offered as the recommended concrete realization of the required
  P(rho,theta) and e(rho,theta,grad(theta)) -- not yet adopted as final,
  but strongly preferable to inventing another closure, since its
  consequences below are independently checkable against known superfluid
  physics rather than freely tunable.

## LDF as a regime of this one field (linearized/Bogoliubov branch)

**[derived from ansatz, borrowing established results]**

Linearizing rho=rho_base+delta_rho, theta small, around the homogeneous
GPE state gives the standard Bogoliubov dispersion relation:

    omega(k)^2 = c_s^2*k^2 + (hbar_eff*k^2 / 2*m_eff)^2

  where c_s = sqrt(g*rho_base/m_eff) is the ordinary (phonon-like)
  sound speed at low k. This is a REAL, derivable prediction (not an
  inserted mass term): LDF propagates as an ordinary sound-like phonon
  at low k, crossing over to free-particle-like dispersion at high k,
  with the crossover scale set by the SAME g, rho_base, m_eff that also
  set P(rho) -- directly satisfying the earlier-flagged requirement that
  different propagation branches share the same baseline material
  coefficients rather than being independently assigned.

## Sintot as a regime of this one field -- the real stabilization question

**[open, with a concrete, well-grounded candidate]**

A repulsive-interaction (g>0) superfluid's stable localized nonlinear
structures are DENSITY DEFICITS (dark solitons, vortices) -- not density
ENHANCEMENTS. This directly reproduces the earlier Derrick's-theorem
finding from this project's much earlier scalar-model work: a simple
gradient+potential functional cannot support a stable, localized,
elevated-density lump in 3D without an additional stabilizing
ingredient. The GPE/Madelung framing does not evade that theorem; it
reframes it precisely, in an already well-studied setting.

The physically real candidate mechanism that DOES stabilize a localized
density ENHANCEMENT in a repulsive superfluid is a **quantum droplet**:
a self-bound state stabilized by competition between mean-field
attraction (requiring g<0 in some regime, or a two-component/dipolar
system) and a beyond-mean-field repulsive correction (the Lee-Huang-Yang
term), giving an effective energy density with BOTH signs of nonlinearity
and a genuine, non-Derrick-obstructed stable minimum at finite size. This
is the same real experimental phenomenon referenced earlier in this
project's own reference material (Monash quantum droplets, arXiv:
2507.19324) -- flagged here as the natural next candidate for how Sintot
could be genuinely stabilized, rather than by an invented double-well.
This is NOT yet shown to work for this specific system -- it is named
explicitly as the concrete next thing to check, replacing the deprecated
chi-double-well machinery.

## What is deprecated by this document

  - The independent LDF vector field a_i and its transversality/coupling
    machinery (`hdf_stress_ldf_squeeze_foundations.md`) -- deprecated in
    full, kept only as historical record of the category error and its
    correction.
  - The independent lock-progress scalar chi and its double-well
    V_lock(rho,chi) -- deprecated for the same reason: it was a second
    inventory appended to rho, needing its own coupling back to rho. It
    is replaced by treating "locked" as a REGIME of (rho,theta) itself
    (Sintot: theta=theta_lock, rho=rho_lock), with quantum droplets as
    the candidate real mechanism for why such a regime can be stable.
  - Any specific numerical claim about STAR/E-144/LUXE/E320 (already
    withdrawn in `star_a4_correction.md`, and untouched by this
    ontological correction).

## What remains open before any simulation

  1. Fix g, m_eff, rho_base (or their PWC-labeled equivalents) as the
     ONE set of baseline material coefficients from which BOTH c_s (LDF
     sound speed) and the gravitational sourcing scale are derived --
     not assigned independently.
  2. Decide whether a genuine quantum-droplet-type two-term nonlinearity
     (not a single g*rho^2 term) is needed for Sintot stability, and if
     so specify it explicitly rather than assuming the single-term GPE
     suffices.
  3. Only then: specify the smallest 1D or 2D grid-converged simulation
     of this ONE-FIELD (rho,theta) system -- baseline stability, a weak
     LDF (Bogoliubov) propagation test matching the derived dispersion
     relation, and (if step 2 supplies a stabilizing nonlinearity) a
     genuine existence test for a stable, localized, elevated-density
     Sintot region -- verified via the same energy/mass/momentum
     conservation audit method already established as reliable in this
     project.
  4. Gravity (grad^2(Phi)=4*pi*G*rho) has not yet been added to any
     simulation in this project -- it is part of the base equations here
     but remains unimplemented and untested.

No code has been written or run against this document.
