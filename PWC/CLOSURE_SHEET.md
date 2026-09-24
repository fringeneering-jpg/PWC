# PWC — Medium Closure Sheet

The five values that close the framework, as one derivation order. Each is fixed **once**, from its allowed inputs only, then must predict its sealed targets without retuning. (Protocol adapted 2026-09-25; matches the repo's standing methodology rule.)

**Order:** P(ρ, s) → a_hold(ρ) → ρ₀ → ΔV_wave → growth law

## Variables

| Variable | Units | Definition | First equation containing it | Already fixed in PWC | Allowed inputs | Sealed prediction targets |
|---|---|---|---|---|---|---|
| P(ρ, s) | Pa | Medium equation of state | c_s² = (∂P/∂ρ)_s | c_s = c at rest (§4); c² = latent heat (§4); shell pressure ≈ 0.29·ρ_max·c² at the sonic point (§0, see note) | compact-object stability; one GW event | other GW events; ringdowns; shell profile |
| ρ_max | kg/m³ | Compression ceiling | yield law at the shell | **1.304×10¹⁵** (GW150914, §0 Step 5) | GW150914 | shell radius vs mass; 89-event merger rule |
| a_hold(ρ) | m/s² | Holding threshold: pull at which the medium can no longer be held/tensioned at density ρ | dP/dr = −ρ·g at the threshold | **3.23×10¹¹ N/kg at ρ_max** (§0) | EOS + compact-object boundary | **a₀ (sealed)**; SPARC relation |
| ρ₀ | kg/m³ | Resting medium density | c² = K/ρ₀ | — | expansion / propagation / cosmological background (NOT galaxy rotation) | a₀ via a_hold(ρ₀) |
| K | Pa | Medium stiffness | c_s² = ∂P/∂ρ | K = ρ₀c² at rest (§4) | EOS | c; threshold law |
| ΔV_wave | m³ per wave | Volume taken out of the medium per tied wave (volume debt) | E_knot = ∫P dV + E_phase + E_surface + E_gradient; m = E/c² | mass = wave count; equal debt per wave (§2) | one microscopic or compact-state transition | **G**; merger release; dump rate; growth |
| Γ_untie | s⁻¹ | Untying rate | V̇ = ΔV_wave·Γ_untie | untying = volume release (§5) | a defined physical process | H(z); redshift (1+z) |
| Growth law | s⁻¹ | Coarse-grained expansion Θ = V̇_released/V − V̇_retied/V; H_PWC = Θ/3 | Θ = ∇·u | growth concentrated at untying sites and thick walls (§2, §6) | one time-domain redshift dataset | BAO 147 Mpc; CMB z ≈ 1100; independent supernova sample |

## Arrows (✔ = equation written, ☐ = derivation target)

- ✔ sonic choke + c_s = c → Hawking temperature (§8)
- ✔ additive cores + 1/r² hold → ρ_max, 3 M☉ release (§0)
- ✔ tension rule + holding threshold + 2D spreading → √(a₀·g_bar) shape (§0)
- ☐ P(ρ, s) → a_hold(ρ) — the single rule linking 3.23×10¹¹ at ρ_max to a₀ at ρ₀
- ☐ cosmological background → ρ₀
- ☐ knot energy functional → ΔV_wave → G
- ☐ ΔV_wave × Γ_untie → growth law → (1+z), BAO

## Hard conditions on P(ρ, s)

| Requirement | Prevents |
|---|---|
| c_s ≤ c in every state | superluminal propagation |
| ∂P/∂ρ > 0 where stable | mechanical instability |
| finite energy density as ρ → ρ_max | a hidden infinity |
| defined phase/yield response at ρ_max | "no singularity" as bare assertion |
| defined entropy production | heat/untying as an unaccounted source |
| weak-field limit recovers Newton | failing solar-system tests |

## Note on the §0 Step 5 units

"P = ρ_max·g = 4.21×10²⁶" is a pressure **gradient** (Pa/m), and "γ = P·R/2 = 3.36×10³¹" is therefore a **pressure** (Pa), not a surface tension in N/m. As a pressure it is ≈ 0.29·ρ_max·c² — the scale expected at a sonic point, a consistency check on Step 1. Relabel in §0 pending Jaden's OK.

## Sealed notebook template (one per value)

Definition · Allowed inputs · Forbidden inputs (blinded targets) · Equation · Fixed value ± uncertainty · Predictions (no adjustment) · Failure condition
