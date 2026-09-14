# PWC Stage 2, corrected: does HDF energy actually convert into a matter knot?

## Why the previous Stage 2 draft was the wrong test

`dynamic_knot_existence.py` (drafted, never run to a trusted conclusion)
initialized phi(x,0) directly as a tanh profile — i.e. it started from an
already-locked matter state and asked whether that state relaxes to
something bounded. That is a test of whether a knot, once posited to
already exist, is a stable fixed point of the conservative dynamics. It is
NOT a test of PWC's actual physical claim, which is that matter is HDF
(electromagnetic wave) energy of the baseline medium that has been
phase-locked and condensed by localized pressure (PWC.md line 81). A
legitimate existence test has to start from phi=0 everywhere (pure
baseline medium, no matter anywhere) and a propagating energy pulse, and
ask whether the pulse's own dynamics can convert some of itself into a
retained phi=1 knot.

## The physical picture being tested

An "HDF pulse" here means a localized traveling disturbance in the
baseline medium's own conserved fields (rho, u), at phi=0 everywhere, i.e.
pure kinetic + compressional (EOS) energy, no locked/potential energy
anywhere. This is the medium's own wave energy channel — no separate
electromagnetic field is being added to the model; rho/u already carry
that channel in this coarse-grained description.

**Local conversion criterion.** At each point, define the local energy
density available to drive locking as the EXCESS kinetic + compressional
energy above the quiescent baseline (rho=rho_bg, u=0, phi=0):

    e_avail(x,t) = (1/2) rho u^2 + [e_EOS(rho) - e_EOS(rho_bg)]

This excludes gradient and locked-state energy, which belong to
already-formed structure, not to the incoming wave.

**Locking threshold**, the dimensional bridge requested:

    E_lock = rho_knot * c_med^2

  - rho_knot = rho_bg + drho  (the target phi=1 locked density, from the
    already-declared B-coupling relation rho = rho_bg + drho*phi)
  - c_med = sqrt(dP/drho at rho=rho_bg, phi=0)  (linear sound speed of the
    undisturbed baseline medium — the medium's own characteristic speed,
    standing in for c in m = L/c^2 at this coarse-grained level)

Local phase-locking is only permitted where e_avail(x,t) >= E_lock.

## Reaction law (the new physical ingredient)

phi no longer just advects — it gets a conversion source, gated by the
threshold, growing toward the locked state at a declared fixed rate:

    D(phi)/Dt = R(rho,u,phi) = k_lock * S((e_avail - E_lock)/eps) * (1-phi)

  - S(y) = 1/(1+exp(-y)) is a smoothed Heaviside (width eps in e_avail
    units), used only for numerical well-posedness — S -> 0 essentially
    exactly below threshold, S -> 1 above it.
  - k_lock: FROZEN rate constant, declared before any run, chosen to be
    fast compared to the local sound-crossing time so locking (once
    triggered) completes within roughly one crossing time. NOT tuned
    per-case to force a particular outcome.
  - This is a threshold-gated conversion/nucleation process (like a
    combustion progress variable), explicitly NOT the dissipative
    relaxation the original spec ruled out — R is exactly zero below
    threshold, not a small drag acting everywhere.

This makes phi a genuinely reacting field: D(rho*phi)/Dt has a source
rho*R, on top of the existing conservative advective flux rho*u*phi.

## Restoring exact energy conservation: the thermal channel

Introducing D(phi)/Dt = R breaks the previously-verified conservative
identity that held for R=0 (passive advection), because the bulk energy
e_bulk(rho,phi) now changes locally due to reaction, not just advection.
By the standard reacting-flow chain rule, this adds exactly

    d/dt integral[ (1/2)rho u^2 + e_bulk + (K/2)(phi_x)^2 ] dx
        = integral[ rho * (d e_bulk/d phi) * R ] dx

with no compensating term elsewhere in the original 3-field model. Per
the explicit instruction to preserve energy through HDF, compression,
kinetic, gradient, thermal, and locked-state channels, a new explicit
thermal bookkeeping field theta (specific thermal energy, i.e. e_thermal
= rho*theta) is added, with source constructed to cancel that term
exactly, by declaration:

    D(theta)/Dt = -(d e_bulk/d phi) * R

so that d/dt integral[e_thermal] dx = - integral[rho (d e_bulk/d phi) R] dx,
and the two extra terms cancel identically. theta plays no other role
(does not feed back into pressure) — it is an explicit latent-heat ledger,
not a hidden energy sink. Total energy tracked is now:

    E_tot = integral[ (1/2)rho u^2 + e_EOS(rho) + e_pot(rho,phi)
                      + (K/2)(phi_x)^2 + rho*theta ] dx

State vector: U = [rho, rho*u, rho*phi, rho*theta] (4 components).
Conservative flux form is unchanged for all 4 components (theta and phi
both advect with u via the same Rusanov flux); the reaction adds source
terms (not fluxes) to components 3 and 4 only, applied as an operator-
split, sub-stepped explicit update within each SSP-RK2 stage so the
rho_max step-rejection logic still applies to the full update.

## Declared parameters (frozen before running)

  - k_lock = 5.0  (locking rate, in the same time units as the existing
    PARAMS; chosen only to be "fast vs. crossing time," not tuned per case)
  - eps = 0.05 * E_lock  (smoothing width for S(y), a small fraction of
    the threshold scale — sensitivity checked, not tuned to an outcome)
  - Existing PARAMS (A, rho_max, Lam, B, rho_bg, drho) and K unchanged
    from dynamic_knot_solver.py.

## Declared pass/fail criteria (before running)

In addition to the existing Stage 2 criteria (finite bounded R_knot(t),
no rho>=rho_max crossing, no secular spread to the full box, no collapse
to grid scale, |dM|/M(0) and |dE|/E(0) within the stated tolerances):

  - **Case A (above threshold):** an HDF pulse whose peak e_avail exceeds
    E_lock must nucleate phi -> locked state locally AND retain a finite,
    bounded knot after the pulse has passed/dispersed (not just transiently
    touch phi>0.5 then fully re-disperse back to phi~0 everywhere).
  - **Case B (below threshold):** an otherwise IDENTICAL pulse shape,
    scaled down so peak e_avail stays below E_lock, must NOT produce any
    retained locked region (phi stays ~0 everywhere for all t, up to the
    smoothing tail of S).
  - Both cases run from the same code path with only the pulse amplitude
    changed — no other parameter altered between A and B.

## Pulse initial condition

phi(x,0) = 0 everywhere (pure baseline medium — no matter is assumed to
pre-exist anywhere in the domain). rho(x,0) = rho_bg + drho_pulse *
exp(-((x-x0)/w)^2), a localized compression bump. u(x,0) set via the
linear acoustic (simple-wave) relation for the baseline medium so the
pulse is a genuinely right-moving disturbance rather than a static bump:
u0 = c_med * (rho0 - rho_bg)/rho_bg. Case A and Case B use the identical
w, x0, and functional form, differing only in drho_pulse amplitude,
chosen so peak e_avail brackets E_lock on either side.
