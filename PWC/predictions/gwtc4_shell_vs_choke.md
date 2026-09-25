# Prediction frozen before running — ρ_max shell vs sonic choke (Jaden, 2026-09-25)

ρ_max = 1.304×10¹⁵ kg/m³ locked (GW150914). Same 84 GWTC-4.0 BBHs, same cores (k = 0.868899), M_held = M_f,obs − C_f.
R_max = (R_c³ + 3M_held / 4πρ_max)^(1/3), R_c = (3C_f / 4πρ_nuc)^(1/3), ρ_nuc = 2.3×10¹⁷.
r_sonic = 2GM_f/c₀² (Jaden's specification). Also reported: Kerr r₊ (spin from Rezzolla 2008 fit).

**Prediction (Jaden):** R_max ≤ r_sonic for every one of the 84 — the shell stays behind the choke across the mass spectrum (required for no echoes).
**Recorded before running (Claude):** M_held ∝ C^(2/3) ⇒ R_max ∝ ~M^(2/9) while r_sonic ∝ M, so R_max/r_sonic ∝ ~M^(−7/9); anchored at GW150914 (0.87) the recipe expects R_max > r_sonic below M_f ≈ 52 M☉. Prediction unchanged.

## Outcome — FAILED as frozen
R_max ≤ r_sonic for 50/84 (all needed). Every black hole above M_f ≈ 55 M☉ passes; every one below ≈ 54 M☉ fails (crossover as expected, ~52 M☉).
By M_f: <25: 0/13 inside (R_max 125 km vs r_sonic 54 km, ratio 2.3); 25–45: 0/12 (1.5); 45–60: 8/17 (1.0); 60–100: 32/32 (0.80); >100: 10/10 (0.54). Against Kerr r₊: 37/84.
With ρ_max fixed and M_held from the k-rule, light black holes' shells extend 1.5–2.3× beyond the choke — i.e. would sit outside the horizon and predict echoes/surface effects for exactly the systems LIGO sees most. Echo searches (null) include such systems. The failure traces to M_held ∝ M^(2/3): too much held medium for light black holes (same root as the Test A radiated-fraction trend). A held-medium law scaling closer to M³ (shell ∝ horizon volume) — or a mass-dependent ρ_max — is needed for both.
