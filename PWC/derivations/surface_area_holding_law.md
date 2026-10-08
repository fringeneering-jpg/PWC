# The surface-area holding law: thin skin, 1/r² dilution (2026-10-08)

Jaden's ruling (verbatim): "Gravity drops off at 1/r² precisely because it is spreading out
over the surface area of a sphere (4πr²). The holding force is a fixed amount of tension
being diluted across a rapidly expanding surface... the bigger it gets, the thinner its skin
gets stretched... The holding equation is strictly bound to the surface area and the 1/r²
dilution of gravity."

Status: arithmetic on locked numbers, verified in `PWC/surface_area_law.py`. Committed
2026-10-08 on Jaden's "in the git".

## 1. The inverse square as geometric dilution

The core's grip is a fixed total; at radius r it is spread over the sphere 4πr², so the
pull per unit area falls as exactly 1/r². The inverse-square law is the dilution of a fixed
tension across an expanding surface — the mechanical origin, no metric needed (the same
statement as GR_TRAPS' "1/r² is the geometric dilution").

## 2. The thin skin

The skin thickness is the surface capacity divided by the ceiling:

    t = Σ_k / ρ_max = 8.48×10²⁰ / 1.304×10¹⁵ = 650 km

The k-rule 20-hole run (session log 2026-10-02): absolute thickness 70 km → ~640 km;
edge/core 4.69 → 1.01. Small core: the grip is concentrated over a small surface and holds
a proportionally thicker skin; supermassive core: the grip is diluted over the huge surface
and holds a razor-thin skin. **RULED: the r⁻⁴ thick threshold envelope (35.6 M☉ tail) is
dead; M_med = Σ·4πR_c², bound strictly to the surface.**

## 3. The sheet law vs the fitted column

Candidate: the flat-sheet self-pull balance 2πGΣ = a_max → Σ = 7.70×10²⁰ kg/m², vs the
fitted k-rule Σ = 8.48×10²⁰ — a +10.1% residual. The surface-area law is now the structure;
closing that 10% would make k = 0.868899 a derived number instead of a fitted one. (The
ball-column stagnation scale differs from the sheet column by exactly 3/2 — geometry; the
skin is the sheet regime.)

## 4. Stagnation consistency

The thin skin (650 km) sits inside the stagnation boundary (886 km): the skin is
SUB-stagnation — it never self-holds; it is held by the core's grip through the 1/r²
dilution. Two independent derivations, one picture.

## 5. What this closes

The third open item — the decompression-envelope shape — is now ruled: the thin skin by
the surface-area law. Remaining numerical threads: the +10.1% Σ residual (above) and the
charge eigenfactor g = 1.2067 (charge_winding_quicycle.md).
