# Prediction frozen before running — held medium as a steady transonic flow (Jaden, 2026-09-25)

First pass (hydrostatic, 4 trial stiff EOS; script bh_profile_trial_hydrostatic.py) FAILED to give C^(2/3): exponents −1.5 to +0.2, several unbound. Reason: a nuclear-density core above ~9 M☉ lies inside its own choke, so the medium there cannot be static.
Finding kept: the k-rule is exactly a universal held column density Σ = M_med / 4πR_c² = 8.48×10²⁰ kg/m².

Flow setup: steady spherical inflow of the resting medium onto the core (Bondi/Michel accretion, the river picture):
Ṁ = 4πr²ρv (constant); v dv/dr = −(1/ρ) dP/dr − GM(r)/r²; dM/dr = 4πr²ρ; resting sound speed c₀/√3 (P = ε/3 branch), ρ ≤ ρ_max; outer boundary ρ → ρ₀ = 8.1×10⁻²⁷ kg/m³; smooth passage through the sonic point.
Targets (frozen): M_med(C) ∝ C^(2/3) with k ≈ 0.87 (Σ = 8.48×10²⁰ kg/m², mass-independent); GW150914 release ≈ 3 M☉; Sgr A* held medium inside ~120 AU; no reflecting wall outside the light horizon.

## Outcome — FAILED by ~39 orders of magnitude
Isothermal Bondi inflow of the resting medium (c_s = c₀/√3, ρ₀ = 8.1×10⁻²⁷), Newtonian order of magnitude:
density at the core surface 4×10⁻²⁶ – 6×10⁻²¹ kg/m³ (ρ_max = 1.3×10¹⁵); held medium 7×10⁻⁴⁰ (C=10) … 2×10⁻²³ M☉ (Sgr A*) vs k-rule 4.0 … 23,000 M☉; scaling C^2.93 (target 0.67). Accretion rate onto a GW150914-size BH ≈ 1.5×10⁻⁶ kg/s.
Relativistic corrections change the near-horizon density by O(1–10), not 40 orders.
**Reading:** the held medium cannot be resting medium flowing in from outside — the resting medium is far too thin. It must be produced at the black hole itself (shredded / untied matter — the medium cycle), from formation onward. The universal column Σ = 8.48×10²⁰ kg/m² then looks like a *surface* property of the core: equivalent to a ~3.7 km skin at nuclear density, or ~650 km at ρ_max.

## Withdrawn as a PWC model (2026-09-25)
The premise was wrong for PWC: the medium does not inflow. PWC's medium is stationary (§0 "the medium does not move"), and a black hole, once set, does not keep drawing medium in (Jaden). Steady inflow (Bondi / GR river picture) was imported, not derived. The ~39-order failure is a failure of that imported premise, not a PWC result.
