# Prediction frozen before scoring — still-galaxy a₀ from spin support (Jaden, 2026-09-25)
Mechanism: a₀ = 6.6776×10⁻¹¹ was calibrated on spinning galaxies, whose spin carries most of their weight; only the pressure-supported share p = σ²_3D/(v² + σ²_3D) loads the medium. Still galaxies: a₀,still = a₀ × p_still/p_spin.
Inputs (literature, not KiDS): spiral stellar discs, Bottema (1993): σ_R = 0.29 V, σ_z = 0.6σ_R, σ_φ = 0.7σ_R → p_spin = 0.135. Ellipticals: ATLAS3D (V/σ)_e for 260 ETGs, p = 3/((V/σ)² + 3), median 0.940.
Predicted ratio 6.98 → **a₀,still = 4.662×10⁻¹⁰**.
Test: KiDS isolated red lenses (colour bin 2), s = 0 form, full covariance. Pass if a₀,still lies within the 68% interval (Δχ² ≤ 1) of the KiDS-red best fit, and beats the spinning a₀ in χ².
(Known before freezing: KiDS-red best fit 2.73×10⁻¹⁰, ratio 4.09.)

## Outcome — FAILED as frozen: right direction, overshoots by 1.7×
KiDS red: best a₀ 2.73×10⁻¹⁰, 68% range 2.57–2.89×10⁻¹⁰. Predicted 4.66×10⁻¹⁰ is outside it. χ²: spinning a₀ 311.5 → predicted 141.6 (vs best 42.1).
KiDS blue: best 8.49×10⁻¹¹ (68% 7.48–9.52×10⁻¹¹); spinning a₀ 6.68×10⁻¹¹ χ² 27.2 — blue stays near the spinning calibration.
The spin-support mechanism moves red galaxies the right way and removes ~75% of their χ² excess, but the derived ratio (7.0) is larger than the data want (4.1).
