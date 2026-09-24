# RBH-1 wake — PWC predictions, frozen before any line map was made

Frozen 2026-09-25, before the JWST GO-3149 NIRSpec IFU cubes (`data/`) were mapped. Committed to git before the extraction script ran; the commit timestamp is the record. Mechanism: PWC.md §8 "The full wake sequence" (front compression → ooze around the sides → cavitating wake → volume-debt squeeze → heat drains → clean line of suns).

| # | PWC expectation | Measurable signature in the cubes | Would count against it |
|---|---|---|---|
| P1 | Leading compression boundary | [O III]/Hα, Hα line width and a velocity jump all peak at the apex end | excitation/width peak mid-wake or at the far end |
| P2 | Cavitation / closure wake | a narrow axial Hα ridge, symmetric across the trajectory | broad, lopsided or fragmented emission with no ridge |
| P3 | Pressure-guided closure (volume-debt squeeze) | ridge width stays bounded or **contracts** over at least part of the wake | width grows steadily with distance like a free turbulent plume |
| P4 | Axial ordering | velocity, dispersion, excitation and [S II] density change systematically (monotonically) with distance from the apex | no trend, or random scatter along the axis |
| P5 | Closure delay | a distinct offset from the apex to the onset of low-excitation / compact knots; t_close = x_onset / v_trail | knots start right at the apex, or appear at random positions |
| P6 | Heat drains from new hydrogen | line width (σ) highest at the apex and **decreasing** downstream (cooling) | σ flat or rising downstream |
| P7 | New-matter branch (NOT testable with these cubes alone) | wake mass/composition exceeds a conservative swept-up + entrained ambient gas budget; needs gas mass, CGM density, metallicity, HST stellar ages | — deferred |

## Rules for the extraction

- Model-neutral: maps and the axial table are produced without any PWC quantity.
- The apex end is identified from the published geometry (black hole at the bright tip, van Dokkum et al. 2023/2025), not from which end looks most "PWC".
- All numbers reported with uncertainties; the two clocks (projected 62 kpc / 954 km/s ≈ 64 Myr vs §8's ~39 Myr) are kept separate until the geometry is sourced.
- Original cubes in `data/` are never modified.

## Addendum (2026-09-25, before any wake profile was measured): success criteria for the new-matter branch

These are the conditions under which RBH-1 would count as support for PWC's matter-formation mechanism. They are criteria, not results; none had been measured when this was committed.

1. **Mass:** the observed wake mass exceeds any credible conventional supply (swept-up + entrained ambient gas).
2. **Energy:** the residual energy after conventional terms has the right sign and magnitude to account for the inferred newly tied mass.
3. **Composition:** the metallicity/abundance pattern points to a non-entrained origin (primitive, hydrogen-dominated gas).
4. **Profiles:** axial width, density, velocity and age profiles agree with a cavitation-closure calculation written down before the comparison.
5. **Universality:** the same c₀, equation of state and holding-threshold law work in other systems without retuning.

## Measured context at time of freezing

Wake 62 kpc; v_BH = 954 (+110/−126) km/s; inclination 29° (+6/−3) out of the sky plane; wake age ≈ 73 Myr (van Dokkum et al., arXiv:2512.04166). Our re-reduction of GO-3149 (NRS1, 8 × 3,501 s): systemic z = 0.9628; apex knot Hα S/N 7–8, σ ≈ 80–110 km/s, [O III]/Hα ≈ 1.2–2.8 (first-pass cube, errors underestimated).
