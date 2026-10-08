# The stagnation scale — what size and density turn the free wave into a stagnant body

Jaden's order (2026-10-08, verbatim): the merger's 3 M☉ dump is "just displacement, not a
cavitating event" — it moved at lightspeed with no visible drag or bow shock, "so it was
under the cavitation limit"; the runaway black hole was "maxp at speed and did cause
cavitation". "There is a scale there where three suns worth of medium can be dropped and
move lightspeed without visible drag or cavitation, however max p can't — that's the thing
we have to figure out: the precise size and density that actually causes the stagnation."

Status: arithmetic on locked numbers, verified in `PWC/stagnation_scale.py`. Committed
2026-10-08 on Jaden's "in the git".

## 1. The condition: self-hold vs the yield

A chunk of medium at density ρ with radius R holds itself at that density iff its own
surface gravity meets the holding threshold (the yield a_max = 3.23×10¹¹ N/kg):

    g_surf = (4π/3)·G·ρ·R  ≥  a_max

    ⟹  ρ·R ≥ 3·a_max/(4πG) = 1.155×10²¹ kg/m²   (the stagnation column)

At the cap density ρ_max = 1.304×10¹⁵:

    R* = 3·a_max/(4πGρ_max) = 886 km
    M* = (4π/3)·ρ_max·R*³   = 1,910 M☉

The 886 km / 1,910 M☉ numbers are the session log's "a pure ρ_max sphere holds all the
mass" limit (black_holes_single_body_mechanics_2026-10-02.md) — previously a bookkeeping
limit of the shell rule, now the **stagnation boundary**: the size at which a dropped
chunk's own gravity equals the medium's holding yield.

## 2. The two regimes

| Case | ρ·R vs the column | Fate |
|---|---|---|
| Merger dump: 3 M☉ at ρ_max → R = 103 km | 0.116× (8.6× below) | **FREE** — cannot hold itself; decompresses at c₀; no drag, no bow shock, no cavitation — the gravity wave |
| RBH-1: core surface gravity 1.76×10¹⁴ (10⁷ M☉) | ~546× above (core-held) | **HELD** — the Max-P must displace the medium → stagnation at v_c = √(2Y/ρ_max) = 954 km/s → cavitation wake |

Equivalently: any confinement with pull ≥ a_max (a neutron core's surface gravity) holds
the chunk; below it the chunk is unheld and returns to the medium at the medium's own speed.
Jaden's reading in one number: the 3 M☉ dump sits at **0.116× the stagnation column** — under
the limit, so no bow shock, just the wave; the runaway sits ~550× over it, so it cavitates.

## 3. The scale, stated precisely

- **Density side:** the cap ρ_max is what makes a chunk a body at all (below it, it is
  decompressing medium).
- **Size side:** self-hold requires ρ·R ≥ 1.155×10²¹ kg/m² — at ρ_max, R ≥ 886 km
  (M ≥ 1,910 M☉); or any core-held Max-P whose holding pull exceeds the yield.
- **Speed side:** once held, stagnation engages at v_c = √(2Y/ρ) — at ρ_max, 954 km/s
  (the RBH-1 anchor). Below the column, there is no stagnation speed: the chunk rides c₀
  at every size.
- Consistency note: the k-rule held column Σ = 8.48×10²⁰ kg/m² = 0.73× the stagnation
  column — the same decade, different roles (surface capacity vs self-hold).

## 4. What this closes

The volume-to-mass friction scale (volume_mass_friction_rcp28.md) now has its boundary:
below the stagnation column the dropped medium is the wave (c₀, frictionless); at/above it
the same substance becomes a stagnant body (954 km/s cap, cavitation). The merger dump and
the runaway wake are the two sides of one scale, and the size/density that causes the
stagnation is **ρ·R = 1.155×10²¹ kg/m²**, i.e. 886 km / 1,910 M☉ at ρ_max.
