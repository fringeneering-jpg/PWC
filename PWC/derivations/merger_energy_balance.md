# Merger mass drop — energy balance and storage bottleneck (Jaden, 2026-10-02)

Reproduced by [`../merger_energy_balance.py`](../merger_energy_balance.py) (per-event table: `../merger_energy_balance_results.csv`). Registry: `DERIVATIONS.md` row 13. No GR formula is used; Newtonian 1/r² only.

## The mechanism (his rulings)
- **Energy and mass are the same thing** (m = L/c₀²). **Heat is a different thing and is not involved in the merger.** No latent heat, no friction heat, no heat drawn after untying, no relaxation back to rest. The wave is the dropped medium; it stays.
- Each core sits in its own ρ_max layer. The cores push through each other's layers; their incompressible volumes add (V = V₁ + V₂).
- The joined core has volumetrically less max gravitational pull and a smaller capacity to store medium than the two separate cores, and the surplus medium drops.

## Two limits on the dropped mass
**E — energy limit.** The merger starts where the two ρ_max layers touch (medium cannot stay crushed twice): r = E₁ + E₂, with E_i = √(G·M_i/a_max) the reach where the pull of everything inside falls to the yield a_max = 3.23×10¹¹ N/kg. In a circular approach the cores' motion energy is half of G·M₁·M₂/r (the other half is potential), and energy is mass:

    E = G·M₁·M₂ / ( 2·c₀²·(E₁ + E₂) )        no fitted constant

**S — storage limit.** A bigger core stores relatively less medium (its capacity goes with area, not volume): S = k·(C₁^(2/3) + C₂^(2/3) − C_f^(2/3)), C from C + k·C^(2/3) = M, k = 0.868899 (frozen repo constant, fitted on catalog masses).

**Dropped mass = min(E, S).** Light events are energy-limited (the energy cannot fill the storage that was lost); heavy ones are storage-limited. GW150914: E = 3.34, S = 3.05, catalog 3.0 M☉. GW190521: E = 11.78, S = 5.56, catalog 9.0.

## Results (final-mass error, mean % / mean |err| % / events within 3%)
| model | DEV, 89 events (explored on) | OUT, 104 GWTC-5 events (never used) |
|---|---|---|
| E, no fitted constant | −0.51 / 0.99 / 86 | −0.17 / 1.01 / 101 |
| S, k frozen | −0.54 / 1.35 / 82 | −0.86 / 1.24 / 94 |
| min(E, S) | +0.38 / 0.89 / 88 | +0.35 / 0.81 / 102 |
| sliding-density limit form (row 12, one constant) | −0.18 / 0.76 / 89 | −0.26 / 0.66 / 102 |

The out-of-sample set has no event in common with the explored set. Trend of error with mass (slope %/ln M): E −1.48 (dev), −1.74 (out) — heavy events over-drop; S +2.26, +1.80 — heavy events under-drop; min(E, S) +0.11 (dev) but −0.86 (out): the flat trend did **not** replicate cleanly out of sample.

## Residual check (falsification, 188 events GWTC-4 + GWTC-5)
The leftover final-mass error of min(E, S) is not noise: it correlates with the catalogue's final-spin column (+0.49), effective spin (+0.37), mass ratio (+0.29) and ln total mass (−0.24); together they explain R² = 0.33 of the residual (sd 1.06%, mean +0.36%). The mechanism is missing a spin / mass-ratio term. (Spin and mass-ratio columns are the catalogue's own, so they are GR-pipeline quantities; the final-spin column is itself computed from the others.) Sensitivity: a_max +10% changes E by −4.7% (E ∝ a_max^(−1/2)).

## Honest limits
- a_max = 3.23×10¹¹ was calibrated on GW150914's edge (159.6 km), a number first computed from that event's Kerr horizon (a GR quantity). The reach scale therefore carries one GR-derived calibration, though not GW150914's dump.
- k is fitted on catalog masses; the S and min(E, S) rows inherit it. Catalog masses come from the standard (GR) pipeline.
- The merger's contact separation (E₁ + E₂) and the "half" (circular-orbit motion energy) are mechanism choices; the data prefer them to the full potential energy (2.3× too high), but they are not independently measured.
- At the contact speed implied (≈0.65 c for GW150914) the Newtonian 1/r² energy is used; a relativistic correction would raise the E estimate (4.95 M☉ for GW150914), the wrong way.

## Withdrawn along the way (do not revive)
Heat-based versions (latent heat absorbed; "heat drawn after untying", P = d(1 + d/m*), m* = 28.6 M☉); the speed-solved form (γ−1)·μ with v ≈ 0.53 c (that speed was solved from the same dumps — circular); Gemini's friction-heat / viscoelastic-relaxation account.
