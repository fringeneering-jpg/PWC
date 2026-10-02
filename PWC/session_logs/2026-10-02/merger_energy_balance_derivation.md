# Merger mass drop as an energy balance (2026-10-02, Jaden's order: "derive it properly")

Status: candidate derivation; arithmetic checked on 89 events; NOT in git.

## Steps (his locked rules in bold)
1. **c0^2 = specific latent heat of the medium; untying absorbs m*c0^2, tying expels m*c0^2.** Releasing crushed (locked, Max-P) medium back into rest medium is an untying, so a released mass m_d absorbs the energy L = m_d*c0^2.
2. Energy source: the two bodies close under the 1/r^2 pull (r measured from the centres). The energy released while the separation shrinks from far apart to r is G*M1*M2/(2r) in a quasi-circular approach (half the potential energy released, the other half stays as orbital motion, which ends as the merged core's spin). In the Max-P medium the bodies are choked, so what is released goes into the medium as bow-wave heat: energy released = energy absorbed.
3. Contact: the merger starts where the two Max-P layers touch, because medium cannot stay crushed twice. Each layer's edge is the reach E_i = sqrt(G*M_i/a_max) (a_max = 3.23e11, the repo yield, total mass inside), so r = E1 + E2.
4. Result: m_d = G*M1*M2 / (2*c0^2*(E1+E2)) = [sqrt(G*a_max)/(2*c0^2)] * M1*M2/(sqrt(M1)+sqrt(M2)).

## Numbers (a_max not refit; rho_core does not enter)
GW150914: r = 230.8 km, predicted drop 3.34 Msun, catalog 3.00. GW190521: 11.78 vs 9.0. GW170104: 2.21 vs 1.9. GW170814: 2.66 vs 2.6. GW151226: 0.60 vs 0.9.
89 events: prediction/dump mean 1.15, median 1.09, sd 0.42 (range 0.58-3.17). Final-mass error with this dump: mean -0.51%, mean |err| 0.99%, sd 1.19%, 86/89 within 3%, 89/89 within 5%. Exponent in total mass: prediction 1.50, catalog dump 1.18; error vs ln M slope -1.5 %/lnM (heavy events over-drop).
The full potential (kinetic energy of a free fall from rest, G*M1*M2/r) gives 2.3 x the dump, so the data prefer the half.

## Assumptions / caveats
- The "half" is a virial assumption. The 1/r^2 energy is used at orbital speeds ~0.65c (Newtonian arithmetic). a_max = 3.23e11 was itself calibrated on GW150914's edge (but not on its dump). Catalog masses come from the GR pipeline.
- Same relation as before in different form: dump ~ (gamma-1)*mu at ~0.53c; here the speed is not assumed, it follows from the contact separation.
Script: capture/merger_energy_balance.py

## Jaden (2026-10-02): "i think its the heavier shit having less heat"
- Measured: catalog dump / energy-balance prediction by total-mass bin (median): 1.30 (14-27 Msun), 1.02, 0.94, 0.85, 0.89, 0.77 (97-238 Msun). Log-log slope -0.32 (dump ~ M^1.18 vs prediction M^1.50). A cut (65/Mt)^s on the predicted drop: s = 0 mean|err| 0.99%; s = 0.25 0.69%; best s = 0.29 0.68% (88/89 within 3%); s = 0.5 0.94%; s = 1 (heat ~ 1/M, Hawking-like) 2.19% (68/89 within 3%). One exponent fitted. Direction right; size M^-0.3, not 1/M.

## Jaden (2026-10-02): "or drawing the most, relatively after untying"
- Reading (mine): after untying, heat is drawn toward the untying site (his rule: heat is pulled to places where knots release), and the draw grows with how much was untied. Energy released P = G*M1*M2/(2 r) = drop d + draw. One fitted constant each, 89 events (energy balance alone: mean|err| 0.99%, 86/89 within 3%):
  - draw grows with the untied mass, P = d(1 + d/m*): m* = 28.6 Msun -> mean +0.05%, mean|err| 0.69%, sd 0.93%, ALL 89 within 3%, slope vs lnM -0.75.
  - draw grows with the energy released, d = P/(1 + P/m*): m* = 37.3 Msun -> mean|err| 0.70%, all 89 within 3%.
  - fixed fraction drawn, P = d(1 + f): f = 0.12 -> 0.82%, all 89 within 3%, slope -1.22.
  - fixed amount drawn, P = d + b: b -> 0 (no improvement; 0.99%).
- Not derived: the 28.6 Msun scale. Compare earlier fitted exponent form (65/Mt)^0.29: 0.68%, 88/89. Not in git.

## CORRECTION (Jaden, 2026-10-02, verbatim): "bro what dnt you realise about energy and mass being the same thinmg, heats the only different thing, and it wasnt involved in the merger"
- Energy and mass are the same thing (m = L/c0^2); heat is the only different thing and was NOT involved in the merger. So the merger derivation has no heat step: no latent heat absorbed, no bow-wave heat, no heat drawn after untying. WITHDRAWN: steps 1-2 wording above about absorbed energy / "untying absorbs m*c0^2" as the merger mechanism, and the whole "or drawing the most, relatively after untying" section (the P = d(1 + d/m*) fits, m* = 28.6 Msun etc.). Gemini's steps 2-3 (frictional heat, latent-heat exhaust) are wrong for the same reason.
- Clean version: dump = the cores' motion energy at contact, as mass. For a circular approach the motion (kinetic) energy is exactly half of G*M1*M2/r (the other half is potential), so dump = G*M1*M2 / (2*c0^2*(E1+E2)) with r = E1+E2. The "half" is not an assumption about how much goes into the medium; it is what the motion energy is. Numbers unchanged: GW150914 3.34 vs 3.00 Msun; 89 events final-mass mean |err| 0.99%, 86/89 within 3%; no fitted constant.
- Left over: heavy events over-drop (dump/prediction 1.30 -> 0.77 from the lightest to the heaviest bin). Not heat. Candidates: the contact separation, or the high-speed correction (at the contact speed ~0.65c the relativistic (gamma-1)*mu is 4.95 Msun for GW150914, i.e. larger, which goes the wrong way). Not in git.

## Jaden (2026-10-02), verbatim: "no, its just the volumetrically shrinking capability to store medium with volumetrically larger core"
- Test (89 events, no refit): two independent estimates of the drop. E = motion energy at contact as mass (G*M1*M2/(2*c0^2*(E1+E2))). S = storage capacity lost when the cores join = k*(C1^(2/3) + C2^(2/3) - Cf^(2/3)) (area law, k = 0.868899 from the repo, which was itself fitted to catalog masses). Named five (E, S, catalog): GW150914 3.34, 3.05, 3.0; GW190521 11.78, 5.56, 9.0; GW170104 2.21, 2.47, 1.9; GW170814 2.66, 2.73, 2.6; GW151226 0.60, 1.29, 0.9.
- Final-mass error vs catalog: E alone mean|err| 0.99%, slope -1.48 %/lnM (heavy over-drop); S alone 1.35%, slope +2.26 (heavy under-drop); THE SMALLER OF THE TWO (a bottleneck): mean +0.38%, mean|err| 0.89%, sd 1.09%, 88/89 within 3%, slope +0.11 (flat). Average 0.71%, geometric mean 0.67%, harmonic mean 0.66% (all 89 within 3%) but no physical reason for those. Light events are energy-limited, heavy ones storage-limited; GW150914 sits near the crossover.
- Caveat: S carries k, which was fitted on the catalog. Not in git.
