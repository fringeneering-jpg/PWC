# Speed limit of a body in the medium; bow waves (Jaden, 2026-10-02)

Reproduced by [`../cavitation_speed_limit.py`](../cavitation_speed_limit.py). Registry: `DERIVATIONS.md` row 15. The formula is the repo's own (`DERIVATION_BRIEF.md` T3 / `OPEN_WORK.md` "Runaway-SMBH wake threshold v_cav"): v_cav ≈ √(2Y/ρ).

## Mechanism (his words in substance)
- **The medium does not move.** Matter is a sieve. A sieve swung fast enough through a cloud chokes: the medium cannot get through the gaps fast enough and a drag/bow wave forms. Every density has its own maximum speed before the sieve stops sieving through without drag.
- **The light and Max-P are the same thing at different densities.** A photon at c₀ (loose medium) and a ρ_max body at 954 km/s both sit at their density's limit and carry the full squeeze.
- **954 km/s is the medium's own limit at Max-P.** The RBH-1 bow wave is made by the outer shell (the ρ_max medium it carries) breaking that limit and forcing a new ρ_max front ahead of it; the neutron core would have beta-decayed if uncovered.
- **Cavitation is vapour returning to liquid; that needs the bow wave; that is water's limit.** Supernova ejecta and the merger are the same event at much higher speeds (10⁴ and 1.5×10⁵ km/s against 954 km/s).

## Numbers
- Combination: ½ρv² = Y (a straight line of slope −½ on log axes). RBH-1: ρ_max = 1.304×10¹⁵, 954 km/s → **Y = 5.93×10²⁶ Pa** (one anchor, so this fixes Y; it is not a test). Same Y gives c₀ for ρ ≲ 1.3×10¹⁰ kg/m³, 0.36 c₀ at 10¹¹, 0.036 c₀ at 10¹³, 954 km/s at ρ_max, 72 km/s at the neutron-core density.
- Water benchmark (Bernoulli, 1 atm): 14.1 m/s at 20 °C, rising as √pressure; for seven common liquids the cavitation limit is 0.95–1.46% of each liquid's sound speed (listed in the script), against 0.32% for the Max-P medium: same order, not exact. The liquids' "cohesion" there is only the ambient pressure.
- RBH-1 geometry: for 10⁷–2×10⁷ M☉ the derived core is 2,743–3,456 km and the ρ_max edge 64,109–90,664 km (reach picture). The bow wave of the shell is ≲ 10⁻⁹ pc, far below resolution; the observed ~1 kpc zone and 62 kpc wake are gas around it. Gas swept over 62 kpc at the repo's assumed n_H = 5×10⁻³ cm⁻³: 5×10⁵–10⁶ M☉ with the tension reach (144–204 pc), 10⁻¹⁶ M☉ with the shell edge. So the shell sets the speed; the gas wake scale comes from the outer reach.

## Tests
- Fastest pulsar B1508+55: 1,083 (+103/−90) km/s vs 954 → +1.3σ (neither passes nor fails; two other pulsars > 1,500 km/s have uncertain distances).
- Runaway SMBH candidates above 954 km/s must show a wake: 3C 186 (line of sight −1,310 ± 21 km/s; broad–narrow line offset 2,140 ± 390 km/s), CID-42 (≈1,300 km/s offset; kick models 1,428–2,470 km/s). Whether wakes were searched for or found: **not checked**. These are inferred speeds of candidates with alternative explanations.
- Applying c₀² = specific latent heat to water gives √L = 1,502–1,567 m/s against water's sound speed 1,482–1,543 m/s (3–6%), and liquid water stays within 0.98–1.06 from the triple point to T/T_c ≈ 0.75. It **fails** for the other liquids tried at low temperature (liquid N₂, Ar, CH₄ ≈ 0.5, He 0.68, ammonia 0.65 at T/T_c 0.55–0.65); simple liquids approach 1 only near the critical point where both quantities vanish.

## Honest limits
- One anchor for Y, so the law is untested apart from the order-of-magnitude liquid comparison and the open candidate checks. The law is a straight line in the combination ½ρv² (slope −½ in log–log), not in speed against density directly.
- Speeds of supernova ejecta and merger are typical/GR-derived values, not looked up for each event; the 954 km/s anchor is the JWST model value (arXiv 2512.04166).
