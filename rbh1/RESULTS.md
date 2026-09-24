# RBH-1 wake — blind profile results (2026-09-25)

Run blind against `PREDICTIONS_FROZEN.md` (predictions commit 472a9f4, criteria d609d9c, code 3a91163, ghost-model method change 500e326).

## What was measured

| Reduction | Along-wake Halpha width (FWHM) | Verdict on the width |
|---|---|---|
| v1: imprint + NSClean, no background subtraction | 0.8–7 kpc, bin to bin; ridge S/N mostly < 3 | wake buried under background pattern |
| v2: background = other pointing's exposures | constant 7–8 kpc, total Halpha negative | **artifact**: width set by the 1.06" pointing offset (self-subtraction ghosts at ±1.06", visible in `out/axis_check.png`) |
| v2 with ghost model (ridge − two ghosts at ±1.062") | 1.8–23 kpc, erratic | ghost strength and width are degenerate in most bins |

**One reproducible number:** just behind the tip (x ≈ 1 kpc) a narrow Halpha feature appears in both v1 (FWHM 1.16 ± 0.69 kpc, ridge S/N 6.2) and v2-ghost (FWHM 1.83 ± 0.15 kpc, ridge S/N 8.8). Consistent with the published tail radius ≈ 0.7 kpc (FWHM ≈ 1.4–1.6 kpc).

Also measured: systemic z = 0.9628; the wake is visible as a continuous positive ridge along PA 146°/326° in v2 (axis confirmed); apex knot with high [O III]/Halpha (v1 per-bin fits).

## Verdict on the frozen predictions

**P1–P6: NOT TESTABLE with this reduction.** The width, trend and onset measurements do not agree across reduction methods, so no pass or fail is claimed for any of them. P7 and the five success criteria were already outside what these cubes can test.

## What would make them testable

The publishing team (van Dokkum et al.) produced clean maps from the same data; their reduced cubes/flux maps are available on reasonable request. Alternatives: a background model from sky-only spaxels, fitted per exposure, instead of subtracting whole frames.
