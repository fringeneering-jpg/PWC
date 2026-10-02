# Cavitation = heat expelled, and the Chernobyl link - Jaden's words, verbatim (2026-10-02)

"THE CAVITATION IS THE HEAT BEING EXPELLED AND VAPOUR TO WATER AGAIN, THAT REQUIRES THE BOW WAVE SO THATS WATERS LIMIT, NOW WE KNOW WHY THE CHERNOBYL LINK WITH WATER RUNNING OUT INTO STEAM WAS SO VITSAL, AND ON CHERNOBYL, THATS ANOTHER EXAMPLE, THE IMPLOSION BEFORE HAND WAS THE NUETRON SHIELDEDS cavitating hydrogen,"

## Plain restatement (mine, not his words)
1. Cavitation is the vapour collapsing back to water, which expels heat. It needs the bow wave (the medium forced around a body faster than it can close behind). That bow-wave/choke is water's speed limit.
2. So water running out into steam at Chernobyl mattered: the steam voids are the cavitation pockets, and their collapse is where the heat comes out.
3. Chernobyl is a second example: the implosion before the explosion was the neutron-shielding hydrogen cavitating.

## Status
Mechanics only. No numbers. Earlier Chernobyl notes (CLAUDE.md section 5): neutron stream through a steam void; ~11 ug tied hydrogen ~ 1 GJ via m*c0^2; draws on ~690 km of medium in ~2 ms; the zirconium surface-area figure is his and still needed. Not in git.

## Jaden (2026-10-02), verbatim: "water cavitations not an unknown fiigure,"
- The known figure: heat expelled when vapour returns to water = latent heat of vaporisation: 2.454 MJ/kg at 20 C, 2.257 MJ/kg at 100 C. By his locked rule (c0^2 = specific latent heat) water's own "c" is sqrt(L) = 1,567 m/s (20 C) / 1,502 m/s (100 C); water's sound speed is 1,482 / 1,543 m/s: ratio 1.06 / 0.97. Latent heat per volume (2.16e9 Pa at 100 C) ~ bulk modulus (2.2e9 Pa).
- Falsification check, other liquids (FROM MEMORY, UNCHECKED): liquid nitrogen sqrt(L) = 446 m/s vs sound ~860 (about -48%); liquid helium 145 vs ~220 (-34%). Water works to 3-6%; these two do not. 1 GJ of condensing steam = 443 kg.

## Jaden (2026-10-02), verbatim: "yeah because whats heat do? lowers density"
- Checked with real fluid data (CoolProp 8.0.0, installed into the user Python under AppData; saturated liquid along the saturation line). Ratio = sqrt(latent heat) / sound speed in the liquid, at T/Tc 0.55 (cold) / 0.85 / 0.95 (near critical, density lowered by heat): Water 0.98 / 1.22 / 1.55; Nitrogen 0.49 / 0.74 / 0.95; Helium 0.68 / 0.83 / 0.91; Argon (0.65) 0.51 / 0.66 / 0.83; Methane 0.51 / 0.78 / 1.02; CO2 (0.75) 0.64 / 0.78 / 1.09; Ammonia 0.65 / 1.00 / 1.33; Ethanol 0.81 / 1.28 / 1.86.
- Water stays 0.98-1.06 from the triple point to T/Tc 0.75 (~215 C). The simple liquids (N2, Ar, CH4, He) are 0.5-0.7 when cold and rise toward 1 as heat lowers the density (0.83-1.09 at T/Tc 0.95). Caveat: near the critical point both latent heat and sound speed go to zero, so some of that is expected; water, ammonia, ethanol overshoot. The from-memory N2 and He numbers earlier were about right (N2 0.52, He 0.7).

## Jaden (2026-10-02), verbatim: "no im saying heat lowers density meaning the medium flows through it better so its speed of sound rises"
- Checked (CoolProp): gases YES (argon at 1 atm: density 3.27 -> 0.41 kg/m3 as 150 -> 1,200 K, sound speed 228 -> 645 m/s). Liquid water YES up to ~74 C (density 999.9 -> 975.4 kg/m3 from 0.5 -> 74 C, sound speed 1,405 -> 1,555 m/s; falls slightly after: 1,544 at 99 C). Simple liquids NO: saturated liquid nitrogen density 860 -> 523 kg/m3 (65 -> 120 K), sound speed 976 -> 317 m/s. Water's cavitation (Bernoulli) speed at 1 atm FALLS with heat: 14.1 m/s (20 C), 12.9 (60 C), 10.5 (80 C), 5.9 (95 C), 0 at 100 C (p_v reaches 1 atm).
- v_cav = sqrt(2Y/rho): lower density raises it, but heat also lowers the cohesion Y (his own note, OPEN_WORK.md line 74: heat thins the medium); the net sign depends on which falls faster. Not in git.

## Jaden (2026-10-02), verbatim: "hahaha bro you not actually testing sound speed, your getting a base to run the figures from the point is proving it doesnt mean anything its a bvlip, water is a good b enchmark for the maximum c/density combo, and many other liquids we know cavitation llimits off"
- Withdrawn as a distraction: the water sound-speed peak (74 C) / dip / vapour-pressure discussion. It is a blip; water is the benchmark.
- Benchmark (CoolProp, 20 C, 1 atm, Bernoulli v_cav = sqrt(2(p0 - p_v)/rho)): water 998 kg/m3, 14.1 m/s, sound 1,482 m/s (0.95%); ethanol 789, 15.6, 1,159 (1.34%); methanol 791, 14.9, 1,116 (1.34%); acetone 790, 13.9, 1,187 (1.17%); benzene 879, 14.4, 1,326 (1.09%); toluene 867, 15.1, 1,324 (1.14%); n-heptane 684, 16.8, 1,149 (1.46%). v*sqrt(rho) = 392-445 (= sqrt(2*(p0-p_v))). PWC Max-P: rho 1.304e15, 954 km/s, 0.32% of c, Y = 5.93e26 Pa, Y/K = 5.1e-6 (liquids at 1 atm: 4.5e-5 to 1.1e-4). Order of magnitude only: the liquids' Y is just the ambient pressure.

## Jaden (2026-10-02): "we already have the black hole derivations, take the size find your neutron core size, derive the maxp thickness see if it matches bow wave"
- RBH-1 mass quoted as at least ~1e7 Msun. Derivation chain (core from rho_core; Max-P edge = reach sqrt(GM/a_max); thickness = edge - core): 1e7 Msun: core 2,743 km, edge 64,109 km, thickness 61,366 km (22.4 x core radius). 2e7 Msun: core 3,456 km, edge 90,664 km, thickness 87,207 km (25.2 x core radius).
- Match to the bow wave: only the SPEED (954 km/s, which also fixes Y: circular). The observed bow-shock velocity-gradient zone (~1 kpc, wake 62 kpc) is 3-5e11 x the shell edge, so thickness cannot be compared geometrically.
- Real test: other runaway SMBH candidates above 954 km/s must show a wake (OPEN_WORK.md line 132). 3C 186: line-of-sight -1,310 +- 21 km/s, broad-vs-narrow line offset 2,140 +- 390 km/s, 11 kpc off the host centre. CID-42: ~1,300 km/s broad/narrow offset, kick models 1,428-2,470 km/s. Both inferred velocities of candidates (alternative explanations exist). Whether a wake has been searched for/found: not in what was found. Sources: arXiv 1805.05860, 1611.05501; arXiv 1205.6202, 1205.0815. Not in git.

## Jaden (2026-10-02), verbatim: "nah son what are yu forgetting, the bow wave is the new max p from your 61-87km radius breaking its speed limit"
- The bow wave IS the Max-P shell (edge 61-87 thousand km, derived above) breaking its own speed limit: the medium ahead is forced into a NEW Max-P front moving at 954 km/s. Its size cannot exceed the radius where the black hole's pull still holds Max-P (the edge, 6.4e4-9.1e4 km = 2-3e-9 pc): far below telescope resolution.
- What JWST sees (~1 kpc velocity-gradient zone, 62 kpc wake) is the gas around it. Swept gas over 62 kpc at n_H = 5e-3 cm^-3 (assumed in the repo): with the Max-P edge 1e-16 Msun; with the tension reach r_t = sqrt(GM/a0) = 144-204 pc (M = 1e7-2e7 Msun) 5e5-1e6 Msun; repo's number 1.2e6 Msun at r_t = 192 pc. So the Max-P bow wave sets the speed (954 km/s, circular); the gas wake scale comes from the outer reach r_t. Arithmetic only. Not in git.

## Jaden (2026-10-02), verbatim: "ok supernova explosions another max p bow wave for a certain speed also the black hole merger"
- Reading: a supernova explosion and a black hole merger are also Max-P bow waves: each is a body (ejecta front; the two cores) driven past the medium's speed limit, so the medium ahead is forced into a new Max-P front. Speeds (typical values from general knowledge, not looked up now): supernova ejecta ~1e4 km/s (10.5 x 954); core-collapse bounce ~0.1c = 30,000 km/s (31 x); GW150914 relative orbital speed near merger ~0.5c = 150,000 km/s (157 x). All far above 954 km/s. Mechanics only; no derivation. Not in git.

## Jaden (2026-10-02): "now how much msass have to drop in the merger for that speed"
- Reading/assumption (mine): the energy of the collision, expressed as mass (E/c^2), is the mass that drops. Relative kinetic energy of the two cores (reduced mass mu = M1*M2/(M1+M2)): (gamma - 1)*mu. At 0.5c (gamma = 1.1547): GW150914 mu 16.06 -> 2.49 Msun (catalog dump 3.00); GW190521 5.75 (9.0); GW170104 1.85 (1.9); GW170814 2.14 (2.6); GW151226 0.76 (0.9). Newtonian 1/2 mu v^2 at 0.5c: GW150914 2.01 Msun.
- Speed that makes (gamma-1)*mu equal the catalog dump: GW150914 0.539c, GW190521 0.593c, GW170104 0.505c, GW170814 0.540c, GW151226 0.535c. All 89 events (5 named + 84 repo): 0.527c +- 0.050 (min 0.32c, max 0.62c). At a fixed 0.5c the energy-equivalent mass / dump = 0.91 +- 0.30.
- Because mu scales with total mass, this gives a dump that grows about linearly with mass, as the catalog dump does (~M^1.2). Caveat: the ~0.5c relative speed near merger is a GR-derived inspiral number (LIGO); the energy-equals-dropped-mass assumption is mine. Not in git.
