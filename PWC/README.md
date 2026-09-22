# PWC: Proofs and Data Still Needed

Status document, not a pitch. Separates what's actually verified from what's a good hypothesis, and flags places where an outside "defense" writeup overclaimed or presented a live scientific dispute as settled. Rule for this file: nothing goes in the "verified" column without a real computed number or a checked primary source behind it.

## Verified — real, computed, checked

- **ρ_max (black hole density floor):** 1.304×10¹⁵ kg/m³, derived from GW150914's own Kerr horizon geometry (real published masses/spin), not assumed. Dated 2026-09-21 in PWC.md §3.
- **Cascade equation vs. MOND, honest holdout split (92 train / 40 holdout, real SPARC data):** MOND ties or edges out the cascade model on unseen data (MOND holdout ≈0.130 dex vs. combined cascade+tension holdout ≈0.133 dex). The 2-parameter version that scores better on training data (0.106 dex) does not hold that advantage on holdout — textbook overfitting signature, not yet resolved in PWC's favor.
- **Zero-parameter geometric version (C_GEO=1/√2, no fitting):** 0.144 dex — worse than MOND, confirmed by running the actual script, not just reading it.
- **GW170817 constrains |v_GW − v_light|/c to ≈4×10⁻¹⁶** (using the raw 1.7s delay over ~130 Mly, no assumption about source-side emission delay). Real, and this is the correct bound to cite — GW150914 (no EM counterpart) does not constrain this at all and should not be conflated with GW170817 in any future write-up.
- **TeVeS and similar bimetric relativistic-MOND variants are ruled out** by the GW170817/GRB170817A speed match — real, solid, not in dispute.

## Good next steps (from the outside "defense" doc's roadmap — legitimate, not yet done)

1. Run the actual PWC ODE on a Gaia-DR3-scale wide-binary configuration (2–30 kAU separation) and check computationally whether the cascade term genuinely fails to accumulate at that scale (the claimed advantage over MOND here is currently asserted, not demonstrated).
2. Define how the cascade handles an External Field Effect analog — does a dwarf satellite's cascade integral get suppressed by its host galaxy's background g_bar? Untested.
3. Test the ODE against SPARC's dwarf spheroidal subsample specifically (heavily dark-matter-dominated in ΛCDM — a real stress test).
4. Extend to pressure-supported systems (ellipticals, ultra-diffuse galaxies) — the cascade has only been tested on rotationally-supported disks so far.
5. A genuine covariant/relativistic formulation that guarantees c_g = c without importing TeVeS-style auxiliary fields — currently just asserted as a future goal, not derived.

## Checked and confirmed (moved out of "flagged" after independent verification)

- **The MOND MCMC claim is accurate.** Confirmed directly from arXiv:1803.00022's abstract: it marginalizes stellar mass-to-light ratio, distance, and inclination per galaxy across the SPARC sample and gets 0.057 dex scatter. Worth adding: even with that per-galaxy freedom, the paper reports "no credible indication of variation in the critical acceleration scale" — a0 stays universal regardless. Safe to cite.

## Flagged — genuinely live, unresolved dispute (checked, and it's real)

- **Gaia DR3 wide binaries: this is an actual, ongoing fight in the literature, not a settled 16-19σ verdict against MOND.** Same catalogue, opposite conclusions from independent groups:
  - Chae (2023): γ = 1.43 ± 0.06 — MOND-consistent boost detected
  - Chae (2024a): γ = 1.49 ± 0.2 — boost detected
  - Hernandez et al. (2024): γ = 1.5 ± 0.2 — boost detected, consistent with AQUAL's predicted ~1.4
  - Banik et al. (2024): 19σ preference for pure Newtonian (γ = 1) — no boost
  - A recent forensic paper (arXiv:2608.24556) investigating *why* they disagree finds undetected triple-star contamination can manufacture a pseudo-signal recovering γ = 1.08-1.13 from purely Newtonian simulated data — about halfway to the claimed anomaly. This suggests part of the disagreement may be a data-contamination artifact, but doesn't settle which side is ultimately right.

  Do not cite "Gaia disproves MOND" as a stable foundation for anything until this dispute actually resolves — right now it's a real, active, three-vs-one-groups fight with a known contamination confound still being worked out.

- **The 0.13 dex "noise floor" claim** (that observational error alone accounts for essentially all of the RAR's scatter) still needs its own source check before being used to argue PWC's holdout result is "exactly at the floor, therefore not overfit." Not yet verified against a primary source.

## The honest one-line summary

ρ_max and the GW170817 speed bound are real, checked, and stand on their own. The cascade equation currently ties MOND, it doesn't beat it, on the only test that matters (holdout). Everything else — the quantum-to-matter chain, the density-to-speed law, the wide-binary/EFE claims — is a real, coherent hypothesis, not yet a result.
