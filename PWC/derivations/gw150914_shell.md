# GW150914 black hole shell — the physical derivation (Jaden)

Source: working session "Refining Black Hole Shell Density" (AI Studio, 21–22 Sep 2026); text pasted by Jaden 2026-10-01 and stored here verbatim in substance so it cannot be lost again.
Reproduced numerically by [`../derive_chain.py`](../derive_chain.py) (Step 5). Registry entry: [`../../DERIVATIONS.md`](../../DERIVATIONS.md) row 5. Framework statement: `PWC.md` §0 Steps 2–5.

This is tactile structural geometry. No spacetime-geometry formalism is used or needed anywhere.

## 1. The physical boundaries

The black hole is not an infinitely small dot. It is a solid core surrounded by a crushed layer of the medium.

- **Inner solid neutron core:** radius 47.3 km.
- **Core density:** ≈ 2.3×10¹⁷ kg/m³ (structurally incompressible).
- **Outer tension threshold:** 159.6 km — the absolute limit where the 1/r² pull can hold the medium crushed at maximum capacity.

## 2. The volume of the shell (the macroscopic Casimir gap)

The space holding the highly compressed medium is the shell between the solid core and the outer threshold.

```
Volume = (4/3)·π·(r_outer³ − r_inner³)
       = (4/3)·π·(159,600³ − 47,300³)  m³
       = 1.658×10¹⁶ m³
```

## 3. The maximum medium density ρ_max

The medium mass caught in that gap is 10.87 M☉ = 2.162×10³¹ kg.

```
ρ_max = Mass / Volume = 2.162×10³¹ kg / 1.658×10¹⁶ m³ = 1.304×10¹⁵ kg/m³
```

This is the hard structural yield ceiling of the medium. It cannot be compressed tighter than this.

## 4. The exact inward force required to hold it

To keep that volume packed at exactly ρ_max, the pull from the knot must output a specific structural force at the 159.6 km boundary:

```
g = G·M / r² = 6.674×10⁻¹¹ · (62 M☉) / (159,600 m)²
Structural holding tension (yield) = 3.23×10¹¹ N/kg
```

(M = 62 M☉ is the total mass, **including the medium's own mass** in the 1/r² profile.)

## 5. The M^(2/3) merger mass deficit (the 3 solar masses)

Because ρ_max is a hard structural wall and volume dictates capacity, merging two objects physically reduces their holding footprint relative to their additive cores.

- **Pre-merger:** core 1 and core 2 have an additive incompressible solid core mass of 51 M☉. Out of the 65 M☉ entering the crash, their separate individual shells were holding **14 M☉** of medium at ρ_max.
- **Post-merger:** they merge into a single solid 51 M☉ core. A single sphere's volume-to-area scaling decays at the M^(2/3) limit, so the new single shell only has the capacity to hold **11 M☉** at ρ_max.
- **Result:** 14 M☉ − 11 M☉ = **3 M☉**.

## Conclusion

The 3 solar masses were not "vaporized" from an infinite singularity. They are the exact volumetric overlap capacity squeezed out when the two fields combined. It is a strictly fluid-mechanical decompression.

---

## What this file does NOT contain (still to be added when Jaden supplies it)

- The same shell worked for **every** black hole (Jaden: derived to 0.1%).
- The **decompression rate** that turns the released medium into the measured settling time (τ = 4.68 ms for GW150914).

Both are listed under "Gaps" in `DERIVATIONS.md`.
