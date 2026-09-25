# Prediction frozen before running — medium outside the choke vs ringdown (Jaden, 2026-09-25)

Profile (Jaden, §0 Step 4): core (k-rule, nuclear density) → max-P layer at ρ_max = 1.304×10¹⁵ out to the yield radius
r_y = √(GM_f / 3.23×10¹¹) → beyond r_y, ρ = ρ_max (r_y/r)² until the held medium M_f − C_f is used up.
Same 84 GWTC-4.0 BBHs, k = 0.868899.

Proxy (leading order, stated in advance): the ringdown is set by the mass enclosed within the potential peak,
r_pk = 3GM_rd/c² (solved self-consistently, M_rd = M(<r_pk)); the inspiral/total mass is M_f (everything).
Predicted inspiral-vs-ringdown mismatch: ΔM/M = (M_f − M_rd)/M_f. Also reported: mass outside the choke 2GM_f/c².

**Prediction (PWC):** ΔM/M stays within the approximate ±10% inspiral–ringdown consistency level (LVK GWTC-3 TGR, arXiv:2112.06861 — exact combined bound not re-checked) for the population (median) and for most events.
**Recorded before running (Claude):** rough hand estimate for a 15 M☉ black hole gives ΔM/M ≈ 25%; heavy black holes (all medium inside the choke) ≈ 0.

## Outcome — PASSED as written, with a sharp light-end prediction
Median ΔM/M = 0.0%; within 10%: 67/84 (80%).
By M_f: <25 M☉: median 26.3% (27% of the mass outside the choke; medium ends ~145 km vs choke ~54 km); 25–45: 3.9% (17% outside); 45–60: 0.0% (0.6%); 60–100 and >100: 0.0% (all medium inside the choke).
Above ~45 M☉ the held medium sits inside the choke, so inspiral and ringdown see the same mass — consistent with LVK's IMR tests, which are dominated by heavier, louder events.
Below ~25 M☉ the profile puts ~a quarter of the mass outside the choke and predicts the ringdown mass ~25% below the inspiral mass. Light systems have weak ringdowns and are mostly outside the LVK IMR sample, so this is not yet tested either way.
**Standing prediction:** a loud light binary black hole (M_f < 25 M☉) will show its ringdown-inferred final mass ~20–30% below its inspiral-inferred final mass. GR predicts agreement. Decisive once O4/O5 delivers one with a measurable ringdown.
Caveat: leading-order proxy (enclosed mass at the potential peak); a medium shell's redshift/reflection effects on the QNM not modelled.

## Correction after review (2026-09-25, Perplexity critique accepted)
This run is **not a PWC ringdown prediction**. It rested on three assumptions not derived in the framework:
(1) the k-rule's M_grad treated as literal mass at definite radii (the k-rule is apparent-mass bookkeeping);
(2) a 1/r² tail normalized to ρ_max at the yield radius (under which dM/dr is constant and M(r) ∝ r — the tail is not light by construction; its extent came from the budget, not from physics);
(3) GR's ringdown taken as set by the enclosed mass at 3GM/c², with the medium as ordinary exterior matter.
The "~25% light-BH ringdown deficit" is therefore withdrawn as a standing PWC prediction. A real test needs ρ(r), P(r), c_s(r), the stress law and PWC's own perturbation equation → ω_PWC(M, J, …).
Note: assumption (1) also underlies §3's ρ_max = M_grad / shell volume — if M_grad is not literal shell mass, the 1.304×10¹⁵ figure needs the same derivation.
