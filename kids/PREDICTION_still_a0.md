# Prediction frozen before scoring — still-galaxy a₀ from spin support (Jaden, 2026-09-25)
Mechanism: a₀ = 6.6776×10⁻¹¹ was calibrated on spinning galaxies, whose spin carries most of their weight; only the pressure-supported share p = σ²_3D/(v² + σ²_3D) loads the medium. Still galaxies: a₀,still = a₀ × p_still/p_spin.
Inputs (literature, not KiDS): spiral stellar discs, Bottema (1993): σ_R = 0.29 V, σ_z = 0.6σ_R, σ_φ = 0.7σ_R → p_spin = 0.135. Ellipticals: ATLAS3D (V/σ)_e for 260 ETGs, p = 3/((V/σ)² + 3), median 0.940.
Predicted ratio 6.98 → **a₀,still = 4.662×10⁻¹⁰**.
Test: KiDS isolated red lenses (colour bin 2), s = 0 form, full covariance. Pass if a₀,still lies within the 68% interval (Δχ² ≤ 1) of the KiDS-red best fit, and beats the spinning a₀ in χ².
(Known before freezing: KiDS-red best fit 2.73×10⁻¹⁰, ratio 4.09.)
