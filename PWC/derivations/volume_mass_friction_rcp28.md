# The volume-to-mass friction scale (RCP 28 identity) — 2026-10-08

Jaden's order: the black hole's Max-P and the medium the RCP 28 runaway SMBH dropped are
essentially the same thing; build the volume-to-mass scale that affects the friction from
their sizes and masses — the wave moved at lightspeed, the Max-P around the runaway at 954 km/s.
Status: arithmetic on locked numbers, verified in `scratch/rcp28_volume_mass_friction.py`
(committed as `PWC/volume_mass_friction.py`). Committed 2026-10-08 on Jaden's "in the git".

## 0. The identity (verified)

- RCP 28 = the runaway SMBH RBH-1's host (`capture/2026-10-03...md` line 66: "the runaway
  SMBH (like RCP 28)").
- Black-hole Max-P and the runaway's dropped medium share one number: **V/M = 1/ρ_max =
  7.67×10⁻¹⁶ m³/kg**. The 10-05 chat's own "shed volume" of the 3 M☉ deficit —
  5.967×10³⁰/1.304×10¹⁵ = **4.57×10¹⁵ m³** — is the same ball as my 103-km sphere.

## 1. The friction law in volume-to-mass form

    v_cap² = 2Y·(V/M)   [HELD bodies; Y = 5.93×10²⁶ Pa, the RBH-1 anchor]

| ρ (kg/m³) | V/M (m³/kg) | v_cap | note |
|---|---|---|---|
| 1.32×10¹⁰ | 7.58×10⁻¹¹ | 0.9998 c₀ | crossover — above this, cap = c₀ |
| 1×10¹¹ | 1×10⁻¹¹ | 0.363 c₀ | white-dwarf class |
| 1×10¹³ | 1×10⁻¹³ | 0.0363 c₀ | |
| **1.304×10¹⁵ (Max-P)** | **7.67×10⁻¹⁶** | **954 km/s** | **the RCP 28 wall: cap ignition ½ρv² = Y** |
| 2.3×10¹⁷ (core) | 4.35×10⁻¹⁸ | 72 km/s | neutron idle speed |

## 2. One V/M, two fates

- **Held (the runaway's Max-P wall):** the medium cannot flow through itself at Max-P, so
  the hole advances by rebuilding the cap ahead and DROPPING it behind (the wake) — at
  exactly the cap-ignition speed 954 km/s (passage chart 2026-10-08: "the 954 anchor is
  now derived as cap ignition, not assumed"). The RCP 28 hole moves AT its friction cap.
- **Free (the merger's dumped medium — the wave):** no wall to rebuild, no displacement —
  it IS the medium spreading, so it rides c₀. The friction law does not apply to it.

## 3. The difference vs the ringdown — resolved as one object

Jaden's 10-05 ruling: "the ringdown was the start of it happening"; the ringdown is the
cores fighting through each other's Max-P to join, and the 3 M☉ release starts at, and is
clocked by, the join. So the dumped medium IS the difference (3 M☉ = 4.57×10¹⁵ m³ = a
103-km Max-P ball), and the ringdown is its release clock.

    V/M(t) = (1/ρ_max)(1 + c₀t/R₀)³ ,  R₀ = 103 km
    at t = τ = 4.68 ms: front = 1,403 km = 13.6×R₀ ; V/M = 1.94×10⁻¹² m³/kg (2,528× decompressed)
    (that V/M, if HELD, would cap at 0.16 c₀ — it rides c₀ because it is free)

## 4. Open

- The release profile between the ringdown start and the full spread — the capture's own
  words: "the release profile = the open decompression law, so a measured spike profile
  would measure it."
- Y has one anchor (RBH-1); the ladder above is a straight line in ½ρv² = Y, untested at
  other densities (pulsar census = the named test).
