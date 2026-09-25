# Prediction frozen before running — held medium as a steady transonic flow (Jaden, 2026-09-25)

First pass (hydrostatic, 4 trial stiff EOS; script bh_profile_trial_hydrostatic.py) FAILED to give C^(2/3): exponents −1.5 to +0.2, several unbound. Reason: a nuclear-density core above ~9 M☉ lies inside its own choke, so the medium there cannot be static.
Finding kept: the k-rule is exactly a universal held column density Σ = M_med / 4πR_c² = 8.48×10²⁰ kg/m².

Flow setup: steady spherical inflow of the resting medium onto the core (Bondi/Michel accretion, the river picture):
Ṁ = 4πr²ρv (constant); v dv/dr = −(1/ρ) dP/dr − GM(r)/r²; dM/dr = 4πr²ρ; resting sound speed c₀/√3 (P = ε/3 branch), ρ ≤ ρ_max; outer boundary ρ → ρ₀ = 8.1×10⁻²⁷ kg/m³; smooth passage through the sonic point.
Targets (frozen): M_med(C) ∝ C^(2/3) with k ≈ 0.87 (Σ = 8.48×10²⁰ kg/m², mass-independent); GW150914 release ≈ 3 M☉; Sgr A* held medium inside ~120 AU; no reflecting wall outside the light horizon.
