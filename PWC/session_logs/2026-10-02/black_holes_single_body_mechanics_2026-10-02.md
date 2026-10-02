# Single black hole mechanics — Jaden's words (AI Studio chat "Data on Twenty Black Holes", 2026-10-01 4:00–4:57 AM)

Source: Drive file 1pVg6T77UYoYCAX21ENQp9-HvZxCAKSGr (full chat text: `ai_studio_data_on_twenty_black_holes.txt` beside this file).
STATUS: **MECHANICS ONLY. THE MATH HAS NOT BEEN DONE.** Jaden: "we haven't done the math yet, I was giving you the mechanics, the exact mechanics."
Every table Gemini produced in that chat (core radii, "decompressing size", density "fits", "flawless") is NOT a result and is not to be cited. See "Gemini's tables" at the bottom.

## The mechanics, as he stated them (his messages [6], [9], [12], [15], [21], [24], [27], [30], [33], [36], [39], [42])

1. **Core.** Every black hole has a neutron-density core, "just trying to not beta decay". It is very dense and has a large gravitational pull at 1/r² from its centre. (rho_core ~ 2.3e17 kg/m³)
2. **Shell.** The core cannot smash the medium down to its own density, because the medium has a maximum density, ρ_max = 1.304e15 kg/m³. So a shell of gravitationally attracted medium forms around the core. The shell has a thickness until the core's 1/r² centre point is far enough from the circumference to let the medium decompress to rest tension and mass again.
3. **Decompression envelope.** "The rest is just the medium's attraction to itself forming the decompressing." A larger neutron core probably means more layers of shell physically, but in ratio to the core the shell shrinks in thickness.
4. **Core size / "coremax".** Asked what happens when the core is extended larger than the centre being able to have quantitative effect -> "so we have a coremax derivation as well then."
5. **Neutrons stack.** "What if the density of the neutrons just does what ρ_max does and stacks." (Core density is a ceiling too; a bigger core adds layers, it does not collapse or beta-decay.)
6. **Finite surface pull.** A core 10x wider does NOT have 10x the pull at its surface: "what happens when the 1/r² rule has rendered the very centre ineffective outside the sphere anymore? meaning the surface's pull has a finite limit also. But still can stack."
7. **Order of work.** Fits to every individual black hole FIRST. "No mergers yet." Then check how accurately the fits match density, mass and size.
8. **Mergers (same framework).** Add the cores' volumes together, dump the excess medium. The gravity wave is "just a biggest 3 sun gravity wave of the medium looking for somewhere to go, because it's essentially just been reintroduced to space again." It is not instant: the two cores have max-P medium around them, the cores had to fight through it to unify, accounting for the build-up.
9. He considers the mechanics of black holes, mergers and the wave speed independently derived as mechanics; next topic was lensing.

(His message [3] also restates the intended test: for one observed black hole, the core size and the shell must mathematically add up to the observed mass, with one shared decompression law, no free variables per object, 20 or so holes of different masses.)

## What the math has to supply (not in the chat, not in the repo as of 2026-10-02)
- **The decompression law** ρ(r) from ρ_max down to ρ0, i.e. M_decompression. This is the same gap as `OPEN_WORK.md` / `DERIVATIONS.md` ("ρ(r), P(r), c_s(r) and the stress law from core -> max-P -> decompression").
- **The finite-surface-pull rule (point 6) as a stated law with a number.** Plain 1/r² with the shell theorem gives g_surface = (4/3)πGρR, linear in R, no cap. His point 6 needs a different rule (the deep interior stops contributing). Gemini simply agreed with it; no depth/length was ever derived.
- **What "size" the fit is against.** Gemini fitted to the Schwarzschild radius (2.95 km/Msun), which is a GR number (GR_TRAPS row 2). In PWC the edge is the sonic choke / the shell edge. Observed sizes exist only for Sgr A* and M87* (EHT shadow).

## What I verified (2026-10-02, python, G=6.6743e-11, Msun=1.989e30, a_max=3.23e11, rho_core=2.3e17)
Gemini's first pass (msg [5]) used: R_max = sqrt(G·M_obs/a_max); uniform ρ_max shell to R_max; core = the rest. That is the same rule as the repo's GW150914 shell (`PWC/derivations/gw150914_shell.md`) and it reproduces it: GW150914 core 47.3 km / 51.1 Msun, edge 159.6 km, shell 10.9 Msun. Other holes under the same rule:

| object | M (Msun) | edge km | core km | core Msun | shell Msun |
|---|---|---|---|---|---|
| GRO J1655-40 | 5.3 | 46.7 | 21.8 | 5.0 | 0.3 |
| V404 Cyg | 9.0 | 60.8 | 25.9 | 8.4 | 0.6 |
| Cyg X-1 | 21.2 | 93.3 | 34.0 | 19.1 | 2.1 |
| Gaia BH3 | 33 | 116.5 | 39.0 | 28.8 | 4.2 |
| GW150914 | 62 | 159.6 | 47.3 | 51.1 | 10.9 |
| GW190521 | 142 | 241.6 | 59.9 | 103.9 | 38.1 |

- Under that rule the core is largest at 83.8 km (285 Msun core, 849 Msun inside the edge at 591 km). Above that no terminating ρ_max shell exists (g(r) never falls back to a_max after the shell's own mass is added). At 1,910 Msun a pure ρ_max sphere (886 km) holds all the mass. So the rule as written runs out near 1e3 Msun: that is exactly where the envelope law (point 3) and the finite-surface-pull rule (point 6) have to take over. It is also where "shell on all black holes" was left open.
- The yield 3.23e11 is one point: G·62Msun/(159.6 km)². The 159.6 km edge was originally the Kerr horizon radius for GW150914 (banked note from the 2026-10-01 session).

## Gemini's tables (do not cite)
- "Stacked core radius" for Groups 2/3 (Omega Cen ... Phoenix A*) = (3M_obs/4πρ_core)^(1/3), i.e. ALL of M_obs as core. Contradicts M_obs = core + shell + envelope. Upper bounds only.
- "Total decompressing size" = the Schwarzschild radius copied from the first list. Not derived. (It is smaller than the core radius for GRO J1655-40: core 22.2 km vs "total ~15 km".)
- "Max thickness" shell for supermassive holes: a core of TON 618's size (51,500 km) has surface pull 3.3e15 m/s², 10^4 x a_max; with plain 1/r² the ρ_max shell would reach ~5e6 km and weigh ~4e14 Msun. The "thin skin" came from point 6 (finite surface pull), which was never given a number.
- "Density fits flawless": it is M/(4/3 π R_s³) with R_s = 2GM/c², which is ∝ 1/M² for any mass. The arithmetic is right (V404 2.27e17, Cyg X-1 4.1e16, GW150914 4.8e15, Sgr A* 1.0e6, TON 618 4.2e-3) but it is a GR identity, not a test. GW150914 at 4.8e15 is 3.7x ρ_max, not "almost exactly".
- Gemini's "70 km / 150 Msun core limit from beta decay" was invented (message [20]); his reply [21] discarded it.
- Merger text in the chat uses forbidden vocabulary in places (Gemini's "ringdown", "tsunami/shockwave"); his own rulings in DERIVATIONS.md stand.

## Addition (Jaden, 2026-10-02, after the above was saved)
- **The density fall (decompression law) is the medium's own gravitational pull on itself.** Outside the ρ_max shell, ρ(r) is set by the medium's pull on its own mass (M_enc includes the medium), not by a separate fitted law. This closes the "decompression law" item above as a mechanism; the equation form still needs his OK before any run.
- **Naming (Jaden):** "shell" = only the layer where max-P (ρ_max) applies. The decompressing medium is NOT shell; it falls off by the medium's own pull on itself. Use "shell" for the ρ_max layer and "decompression" / "envelope" for the rest.
- **Black hole = core + ρ_max shell (Jaden, 2026-10-02).** The black hole's size is set by the geometry of the medium's max-P sphere; otherwise the size is "too hard" to define. Outside the shell is just heavy medium, maybe called the **"black hole's starting attractor"** (name not final). So BH radius = the shell's outer edge (where max-P ends); the attractor is the medium around it, falling off by its own pull.
- Consequence to settle in the math: which mass the catalog number is. Repo convention (GW150914: 62 = core 51 + shell 11 inside 159.6 km) takes the catalog mass as the mass inside the BH edge, with the attractor on top. Default unless he says otherwise.

## Run of all 20 (2026-10-02, his OK; catalog mass = mass inside the edge; core + rho_max shell only; no decompression term). Full table: `bh_single_body_run_2026-10-02.csv`
- Solved (7): GRO J1655-40, V404 Cyg, Gaia BH1, Cyg X-1, Gaia BH3, GW150914, GW190521 (numbers in the table above; thickness/core 1.14 -> 3.04).
- NO SOLUTION (13): Omega Cen (8,200 Msun) and everything heavier. The rho_max shell out to sqrt(GM/a_max) alone outweighs the mass: 2.1x (Omega Cen) up to 7,200x (Phoenix A*). Under this rule a core+shell black hole cannot exceed ~1,910 Msun inside its edge.
- Shell thickness / core radius GROWS with core size (1.14 at 5 Msun, 2.38 at GW150914, up to 6.05 at the 83.8 km core limit). His stated expectation (ratio shrinks with a larger core) is the opposite under this rule. Gemini's "proof" (msg [11]) had the monotonic direction backwards: the bracket (rho_core-rho_max)/X^2 + X*rho_max is decreasing for X < 7.05, so a larger core gives a larger X.
- Not a size test: none of these edges is an observed size.

## CORRECTION to the "Run of all 20" above (2026-10-02, Jaden: "why do you always fuck up simple math... if you inserted GR fix it")
- The 13 "NO SOLUTION" rows are NOT a result of his mechanics. They come from using the point-mass pull g = G*M_enc/r^2 on large cores (shell-theorem pull, grows with core radius). His mechanic #6 says the opposite (finite surface pull, core still stacks). I left #6 out of the run. Retracted.
- GR in the constants (not added this session, but used without flagging): rho_max = 1.304e15 and yield a_max = 3.23e11 both come from 159.6 km, which is the Kerr outer horizon of GW150914 (M=62, a=0.67 -> 159.56 km). Quote, capture/ai_studio_refining_bh_shell_density.txt line 102: "the real Kerr horizon radius (159.6 km) computed from GW150914's actual published mass and spin — genuinely independent, standard GR formula". So GW150914 matches by construction, and every other hole inherits that calibration. The repo lists a native a_hold(rho_max) as the target (DERIVATION_BRIEF.md line 79), not derived. UNCHECKED arithmetic: (c0)*sqrt(G*rho_max/4) = 4.4e10, 7.3x below 3.23e11.
- The 7 stellar fits are arithmetically right under those constants only.

## CORRECTION 2 (Jaden, 2026-10-02): 2GM/c^2 is the sonic choke = the black hole's edge, with a medium reason
- My notes above call the Schwarzschild radius "a GR number, not an edge" / "not a size test". That was wrong as a blanket statement. PWC.md section 8 (line ~323-327): "A black hole's edge is where infalling medium reaches the medium's own maximum propagation speed — the sonic point ... v(r) = c0 exactly at r = r_s = 2GM/c0^2". It gives Hawking T exactly. So r_s = 2GM/c^2 IS the PWC edge (the choke), for a medium reason. The only trap is reading it as "space weighs nothing".
- Two radii per hole: sonic choke r_s = 2GM/c^2 and shell edge R_max = sqrt(GM/a_max). GW150914: 183 km vs 159.6 km. GRO J1655-40: 15.6 km vs 46.7 km (shell outside the choke; the repo records gwtc4_shell_vs_choke FAILED on this, OPEN_WORK line 37 asks what an exposed shell does).
- Same tension applies to the mechanics, not only to Gemini's table: a rho_core ball has mean density 2.27e17 at r_s for 9 Msun, so below ~9 Msun the core (e.g. 21.8 km for 5.3 Msun) is larger than its own choke (15.6 km).
- **Core stacks like the medium does (Jaden, 2026-10-02).** The core has a hard density ceiling (rho_core) and more mass adds layers/volume, not density; no beta-decay wall. Same behaviour as the rho_max shell ("thicker, not denser"). Core radius = (3M_core/(4*pi*rho_core))^(1/3), as in the run. This does not by itself give the pull law for the shell edge of very large cores (mechanic #6); that rule is still open.
- **Gravity rule, in his words (2026-10-02):** "gravity ... has a 1/r² rule, which means measure from the centre for r, once 1/r² runs out the centre isn't affecting no further, [and] the 1/r² growth is literally the same rate from the centre out of unused gravitational pull." Reading: r is always measured from the centre; the pull falls as 1/r² from there; where it runs out (reaches the yield) the centre has no further effect on the medium. Not yet turned into an equation for the shell edge of very large cores; asked him for one number (shell thickness of TON 618's 51,458 km core in his picture).
- **Reading B confirmed by Jaden (2026-10-02):** the live part of a stacked core is a skin of fixed thickness t, everything under it is dead, so surface pull = 4*pi*G*rho_core*t (finite) while the core keeps stacking. He says he already sent the answers (the Gemini colab tables: core radius from the whole mass at rho_core, choke 2GM/c^2 as total size).
- **Test of B on the core alone (my run, 2026-10-02):** with the core pull capped (t = 14, 28, 56 km) and the shell's own mass still pulling, no edge exists for cores above ~84-100 km: a rho_max shell's self-pull (4/3)*pi*G*rho_max*r reaches a_max at r = 886 km, so the shell never ends. Capping the core does not fix it; the shell (a stack of medium) needs the same live-skin rule. A shell skin t_s gives self-pull 4*pi*G*rho_max*t_s; it equals a_max at t_s = 295 km. The locked GW150914 shell (112 km thick) needs t_s >= 112 km to stay unchanged. So t_s must lie between ~112 and ~295 km. Not yet a number from Jaden.

## Run of all 20, capped-core rule as ordered by Jaden (2026-10-02). Full table: `bh_capped_core_20_2026-10-02.csv`
- Rule (his words): the core's surface pull hits a hard maximum because the centre's pull runs out of range, so it caps at a constant; the rho_max shell has NO pull of its own; shell edge = where the core's capped surface pull, falling 1/r² from the core surface, drops to the yield a_max = 3.23e11. No shell-skin variable.
- Constants used: rho_core 2.3e17, rho_max 1.304e15, a_max 3.23e11, g_cap = 5.38e12 (the surface pull of the 83.7 km core, the cap agreed under reading B; his own text gives no number for g_cap). Mass closure: M_catalog = core + rho_max shell (no attractor).
- Result: all 20 solve. Cores below 83.7 km are uncapped (GW190521 and lighter). Above, edge/core = sqrt(g_cap/a_max) = 4.08 and shell mass = 38% of core mass for every hole (shell = 27.5% of M). Absolute shell thickness still grows with the core (3.08 x core radius); only the RATIO is capped. If he means an absolute maximum thickness, the cap must fall with core size, which his text does not give.
- GW150914 moves off the locked values because the shell's self-pull is removed: core 47.9 km (locked 47.3), edge 148.1 km (locked 159.6), shell 8.6 Msun (locked 10.9). Sgr A* edge 7,591 km (message-8 scaling gave 42,040 km). TON 618 edge 1.89e5 km.
- Edge vs choke: shell edge inside the choke from ~50 Msun up (GW150914 0.81); outside for light holes (GRO J1655 2.9).

## RULING (Jaden, 2026-10-02, "the final order")
- The surface-gravity cap is absolute: the active pulling mass is a fixed-thickness layer riding the surface; the r² of the growing surface area cancels the r² of the gravity drop-off (g = 4*pi*G*rho_core*t, constant). The constant surface pull is physical law; the 4.08x structural lock (edge/core = sqrt(g_cap/a_max)) is correct; the engine is verified. (Implied: t = 27.9 km, g_cap = 5.38e12.)

## Shadows vs EHT (2026-10-02) — what the engine gives and what the data needs
- EHT: Sgr A* ring 51.8 +- 2.3 uas (shadow 48.7 uas; EHT mass ~4e6 Msun, distance 8.15 kpc UNCHECKED in the search extract); M87* ring 42 +- 3 uas, 6.5e9 +- 0.7e9 Msun, 16.8 Mpc. Sources: ADS 2022ApJ...930L..12E, ADS 2019ApJ...875L...1E.
- Engine radii as angular DIAMETERS: choke 2GM/c^2: Sgr A* 20.8 uas (4.3e6) / 19.4 (4.0e6), M87* 15.3 uas = 0.36-0.40 of the ring. Capped shell edge: Sgr A* 0.0125 uas, M87* 0.0001 uas (negligible).
- Observed ring RADIUS in choke units: Sgr A* 2.49 (4.3e6) / 2.67 (4.0e6) r_s, M87* 2.75 r_s (mass +-11%). Needed ring radius in km: Sgr A* 3.16e7, M87* 5.28e10. The engine has no radius at ~2.5-2.75 r_s; "decompression shadow" has no definition in the repo (lensing is the next topic, not derived).

## Mergers on the capped-core engine (2026-10-02; his merger script re-pasted: cores = all mass at rho_core, volumes add, surface-area loss ~20%, dump = (M1+M2) - M_final from the catalog)
- Engine merger (cores add as volumes, shell rebuilt around the fused core, uncapped regime for all five events): predicted dump comes out NEGATIVE (shell mass ~ M^1.5 is superadditive): GW150914 -2.94 (catalog +3.00), GW190521 -9.60 (+9.00), GW170104 -1.98 (+1.90), GW170814 -2.37 (+2.60), GW151226 -0.56 (+0.90). Magnitude within 2-38%, sign opposite. In the capped regime shell mass is linear in core mass (additive), so no regime gives a positive dump.
- His script's own route: dump = area loss (19.8-20.6%) x shell held before. That needs held shells of 14.6, 43.9, 9.4, 12.7, 4.6 Msun; the engine's separate shells total 6.9, 22.9, 4.8, 5.5, 1.4 Msun (about 2x too small). Repo bookkeeping: 14 = 65 - 51 (core total 51 from the k-rule); engine core total for GW150914 = 58.1.
- Script note: its "dump" is taken from the catalog final mass, so it is an input, not a prediction. Area loss is ~20% for every event.

## SUPERSEDES the capped-core runs above: the k-rule structure (repo `PWC/gwtc4_blind_tests.py`: core = brentq(C + k*C^(2/3) = m), k = 0.868899; pred = Cf + k*Cf^(2/3), Cf = C1 + C2)
- Each hole = core C + shell of mass k*C^(2/3) (proportional to the core's SURFACE AREA, Msun units) at rho_max around the core. Cores add as volumes in a merger; the shell is rebuilt on the fused core; the dump is the area loss.
- Mergers (k from the repo, not refitted): predicted final mass vs catalog: GW150914 61.95/62.0 (-0.08%), GW190521 145.4/142 (+2.4%), GW170104 48.1/48.7 (-1.2%), GW170814 53.1/53.2 (-0.25%), GW151226 20.4/20.8 (-1.9%). Dumps pred/cat: 3.05/3.00, 5.56/9.00, 2.47/1.90, 2.73/2.60, 1.29/0.90. Sign correct for all five.
- 20 holes (`bh_krule_20_2026-10-02.csv`): shell % of M falls from 37% (5.3 Msun) to 0.02% (TON 618); edge/core 4.69 -> 1.01; absolute shell thickness rises 70 km -> a constant ~640 km (his "maximum thickness" and "ratio shrinks"); core = (almost) all the mass for heavy holes, i.e. Gemini's all-mass core column. Sgr A*: core 2,067 km, edge 2,580 km. M87*: core 23,760 km, edge 24,390 km.
- The 4.08x lock and g_cap = 5.38e12 from the earlier run are NOT what this gives; do not use them.

## PUSHED (his order, 2026-10-02): f62df5c on GitHub main (DERIVATIONS.md row 11 + framing). He called the engine "officially locked and verified against the 89-event catalog".

## Shadows from the framework's own flow (2026-10-02; PWC.md section 8 premise: medium infalls at v(r)=sqrt(2GM/r), light moves at c0 relative to the medium)
- Ray in the moving medium: H = c|p| + u(r) p_r, u = -sqrt(r_s/r) c. Turning points where b^2 = r^3/(r - r_s) (r_s = 1): b(r) = r^(3/2)/sqrt(r-1) has its minimum 3*sqrt(3)/2 = 2.598 r_s at r = 1.5 r_s. Rays with b < 2.598 r_s cannot turn back (captured/escape depends on direction); b_c = 2.598 r_s. Ray-traced numerically: 2.5981 (after normalising b = L/omega).
- Escape cone at radius r (radial group velocity c*cos(beta) + u > 0): cos(beta_c) = sqrt(r_s/r): 0 deg at the choke r_s, 17.5 at 1.1 r_s, 35.3 at 1.5, 45 at 2, 60 at 4 r_s.
- Predicted ring diameter 2*b_c = 5.196 r_s: Sgr A* 54.1 uas (4.3e6 Msun) / 50.4 uas (4.0e6) vs EHT 51.8 +- 2.3 (+1.0 / -0.6 sigma); M87* 39.7 uas vs 42 +- 3 (-0.8 sigma). Mass implied by the ring: Sgr A* 4.11e6 +- 0.18e6; M87* 6.88e9 +- 0.49e9 Msun (adopted 6.5e9 +- 0.7e9). Sgr A* distance 8.15 kpc not confirmed in the search extract (UNCHECKED).
- Caveats: this is advection by the inflow, NOT refraction by a density gradient (no n(r) exists in the repo); shell/attractor/4.08x do not enter, only M and c0. It is mathematically the same capture number as GR's (3*sqrt(3)/2 r_s), so EHT agreement does not separate PWC from GR. Not in git.

## Pasted Sgr A* block (core 3.1e6 Msun, 930 km; edge 3795.5 km; shell 1.2e6 Msun; "8.32% yield", rho_max 1.058e16) — checked 2026-10-02, NOT a result
- Arithmetic is right (pull ratio 0.0833, shell volume 2.257e20 m3, rho 1.058e16), but rho_max is solved for, not used: it is 8.1x the locked 1.304e15. Core density implied 1.83e18 = 8x rho_core (at 2.3e17 the core would be 1,857 km). Pull at 3795.5 km is 3.96e13 = 123x the yield 3.23e11 (yield edge for 4.3e6 Msun: 42,039 km). "8.32%" is not a constant: same ratio for the locked GW150914 is 10.65%. Row 11 shell for a 3.1e6 Msun core is 1.85e4 Msun, not 1.2e6 (65x). Row 11 numbers for Sgr A*: core 2,067 km, edge 2,580 km, shell 2.3e4 Msun.

## WITHDRAWN (2026-10-02, Jaden: "you applied a euclidean mathematical fix to my physical framework")
- The "Shadows from the framework's own flow" section above is WITHDRAWN as a PWC result. It used a medium flowing inward (river model), but the medium does not flow or have a speed: it sits still; matter is what is pulled (feedback memory 2026-09-29). It is the GR capture number (3*sqrt(3)/2 r_s) reached through a GR-equivalent formalism, not a mechanism of his. PWC shadow remains UNDEFINED: needs his light-trapping mechanism.
- Also not his mechanics, and not to be reused: point-mass pull from the centre on large cores, rho*V mass-closure of the shell, the capped-core run (g_cap, 4.08x), the "mass inside the edge" bookkeeping. His description is the numbered list at the top of this file plus the 2026-10-02 rulings.

## CORRECTIONS to my mechanical write-up (Jaden, 2026-10-02, verbatim; these override anything above that disagrees)
1. WRONG (mine): "the centre's 1/r² runs out of range before it reaches the surface of a big core, so only a layer of fixed thickness riding the surface does the pulling, and the interior is dead weight."
   HIS: "THE INTERIOR DOESN'T STOP PULLING, IT JUST HAS NO EFFECT, MEANING IT SHOULD BE REMOVED FROM THE TOTAL PULLING CAPACITY OF THE CORE (THE SMALL BIT THAT DOESN'T PASS THE SPHERICAL BOUNDARY)." => core pulling capacity = core minus the interior bit whose pull does not pass the core's spherical boundary.
2. WRONG (mine): "the surface pull has a finite maximum while the core keeps stacking."
   HIS: "NOT REALLY, IT CAN PULL OVER PMAX IF IT WANTS, THAT CAN STACK IF NEEDED." => no cap on the pull; pull beyond what holds rho_max just stacks the shell thicker as needed. (g_cap / 4.08x cap are dead.)
3. WRONG (mine): "the joined core has about 20% less surface than the two separate ones, about 20% of the medium they held now has nothing holding it, so it's released."
   HIS: "IT HAS VOLUMETRICALLY LESS MAX GRAVITATIONAL PULL AND DROPS THE MASS." => the merged core has less maximum gravitational pull (more of its volume is dead interior, removed from its pulling capacity), so it can hold less medium, and the surplus medium is dropped.
- Note: DERIVATIONS.md row 11 (pushed, f62df5c) is worded in terms of surface area / a fixed-thickness pulling layer; his corrections state the mechanism as removed-interior pulling capacity. Same C^(2/3) scaling intended; wording not yet changed (he said no to a rewrite earlier).

## RUN under his corrected mechanics (2026-10-02, "NOW RUN THE NUMBERS")
- Implementation: core = whole mass at rho_core (as in his script); dead interior = the mass whose pull at the core boundary is below the yield, m_dead = a_max R²/G (= 0.39 C^(2/3) Msun for C in Msun; no new constant); pulling capacity P = C - m_dead; no cap; shell edge E = sqrt(G P / a_max) (pull falls 1/r² from the centre to the yield; shell has no pull of its own); held medium = rho_max * V(E - core).
- Max pull (surface pull of P) of the joined core vs the two separate cores, m/s²: GW150914 2.97e12 vs 4.57e12; GW190521 4.04e12 vs 6.26e12; GW170104 2.71e12 vs 4.13e12; GW170814 2.81e12 vs 4.32e12; GW151226 1.96e12 vs 2.94e12. Joined < separate in all five (about -35%), as he says.
- Held medium (rho_max x shell volume to the yield edge) goes UP on merging, not down: change -3.28 (cat +3.00), -11.74 (+9.00), -2.15 (+1.90), -2.61 (+2.60), -0.57 (+0.90) Msun. Magnitude within 0.4-30% of catalog dumps, sign opposite. A dump tied to the pull deficit instead (kappa fixed on GW150914) gives 3.0/4.2/2.7/2.8/1.8 vs 3.0/9.0/1.9/2.6/0.9.
- 20 holes: edges equal the message-8 numbers (Sgr A* 41,990 km, M87* 1.634e6 km, TON 618 5.21e6 km); dead interior 22.6% of the core at 5.3 Msun falling to 0.0085% at 1e11 Msun; held medium (rho_max to the edge) outweighs the hole by 47x for Sgr A* (2.0e8 vs 4.3e6 Msun). Table printed in the session only.

## RUN 2 (2026-10-02): the repo's own max-pull deficit (PWC.md section 8 line 398-407), frozen kappa = 3.1748e18 kg per (m/s²), no cap, no yield cutoff, nothing refitted
- His question: two neutron cores of the same weight, one half the size: the smaller pulls more medium in (surface pull GM/R², 4x at half the radius). Every part of the core counts, deeper mass counts less. I had invented a "below the yield" cutoff; dropped.
- Mechanism: deficit = kappa*[g(M1)+g(M2)-g(M1+M2)], g = GM/R², R from rho_core = 2.3e17. Joined core has 36-37% less max pull than the two separate in all five events.
- Results (pred vs catalog): GW150914 Mf 61.92/62.0 (-0.12%, the calibration event); GW190521 146.9/142 (+3.5%); GW170104 47.8/48.7 (-1.8%); GW170814 52.9/53.2 (-0.61%, repo table says -0.61%); GW151226 19.6/20.8 (-5.7%, repo table -5.75%). Dumps pred/cat: 3.08/3.00, 4.07/9.00, 2.79/1.90, 2.93/2.60, 2.08/0.90. Sign right in all five.
- The repo itself (PWC.md line 400) calls the C^(2/3) relation "a phenomenological stand-in" and this deficit "the mechanism going forward". DERIVATIONS.md row 11 (pushed) uses the surface-area wording; unchanged.
- His point (2026-10-02): the lighter the event, the bigger a fixed mistake looks in %. Catalog final-mass error bars (GWTC-1, from the GWOSC/arXiv search): GW151226 20.8 +6.1 -1.7; GW170104 48.9 +5.1 -4.0; GW170814 53.2 +3.2 -2.4 Msun. Run-2 predictions 19.6, 47.8, 52.9 all inside those ranges. The dump itself (0.9-3 Msun) is smaller than the error bar on the final mass for the light events.
- Pattern he noticed in the first table of Run 2 (2026-10-02): "the lower weight we went the more a mistake affected the % off". Final-mass error vs mass is monotonic, not scatter: 142 Msun +3.47%, 62 -0.12%, 53.2 -0.61%, 48.7 -1.83%, 20.8 -5.66%. In Msun: +4.93, -0.08, -0.33, -0.89, -1.18. The three lighter events sit near a fixed ~-1 Msun offset, which reads as a growing % at low mass. Model dump is nearly flat (3.08, 2.93, 2.79, 2.08, 4.07) vs catalog (3.0, 2.6, 1.9, 0.9, 9.0). Core-only masses (shell share removed, kappa recalibrated 3.3784e18 on GW150914) change it only a little (-5.66 -> -5.02% at 20.8): not the cause. The mistake itself is not yet named.

## SIZES BEFORE + 84 events (2026-10-02, "that's not enough data, I need sizes before everything"). Table: `maxpull_deficit_84events_2026-10-02.csv` (repo catalog gwtc4_blind_results.csv, frozen kappa 3.1748e18, whole-mass cores)
- Sizes (radii from the centre, km; whole mass as core at 2.3e17; reach = sqrt(GM/a_max)): GW150914 cores 42.0 + 39.1 -> joined 51.2 (catalog final-mass core 50.4); surface pulls 2.70e12 + 2.52e12 vs joined 3.29e12; reach 121.6 + 109.2 -> 163.4 (catalog final 159.6). GW190521 56.0 + 51.5 -> 67.8 (66.4); GW170104 40.1 + 34.2 -> 47.1 (46.5); GW170814 39.8 + 37.4 -> 48.7 (47.9); GW151226 30.8 + 24.9 -> 35.5 (35.0).
- 84 events binned by total mass: mean error % = -7.45, -3.03, -0.80, -0.23, +0.71, +2.11 (heaviest bin); mean error in Msun = -1.35, -1.07, -0.43, -0.16, +0.56, +2.82; within-bin sd ~1% (systematic, not scatter). error% vs ln(M): slope +5.1 %/ln-unit, corr 0.96.
- Dump scaling: catalog dump ~ M^1.18; model (g-deficit) dump ~ M^0.33. Dump as a share of total mass: catalog 3.3% (lightest bin) -> 5.0% (heaviest); model 10% -> 2.9%. The mismatch is the exponent, not a fixed offset.

## Error vs core VOLUME (2026-10-02; his reading: "volumes are the issue, we overestimate the neutrons' pulling power a tiny bit, perfect naturally at the ~50 km range")
- 89 events (5 named + 84 repo), frozen kappa, whole-mass cores. Error crosses zero at M1+M2 = 73 Msun = joined core radius 53.2 km, volume 6.3e5 km3. By joined radius: <40 km (n=18) -6.76%; 40-45 (7) -2.93%; 45-50 (16) -1.45%; 50-55 (24) -0.01%; 55-60 (13) +0.88%; 60-80 (11) +2.55%. Model over-drops mass for small cores, under-drops for large.
- Tiny trim (pull minus a_max, kappa recalibrated on GW150914): slope 5.1 -> 4.3 %/ln M, mean|err| 2.54 -> 2.19%. Small effect.
- Size-dependent pull g*(R/R0)^eps (R0 = 51.2 km, kappa calibrated once on GW150914): eps 0 -> mean|err| 2.46%, 64 within 3%; eps 0.5 -> 1.93%, 67; eps 1.0 -> 1.48%, 75 within 3%, all 89 within 5%. eps = 1 is pull proportional to R^2 (surface area, M^(2/3)): the row-11 scaling. Improvement is steady in eps; not a tiny correction.

## Sliding core density (Jaden, 2026-10-02: "we derived the core density and pmax from GW150914 alone, so we assumed the same density for every core; lighter cores lose more volume than expected, heavier denser cores pull more medium in to pmax")
- Test: rho_core(M) = rho_ref * (M/M_ref)^beta, each core's density from its own mass (joined core from M1+M2), kappa calibrated once on GW150914; 89 events (5 named + 84 repo). Normalisation does not matter (kappa absorbs it); only beta does.
- beta 0 (fixed density): mean|err| 2.46%, 64 within 3%. beta 0.5: 1.48%, 75. beta 0.8: 1.02%, 87. beta 0.9: 0.88%, 88. beta 0.95: 0.81%, 89/89 within 3%. Improves steadily as beta -> 1; the slope never reaches exactly zero before beta = 1 (at beta = 1 every core has the same radius and the pull is additive, deficit = 0).
- Limit model, one constant lam = 0.0671 calibrated on GW150914: dump = lam*[M1 ln(Mt/M1) + M2 ln(Mt/M2)] (the beta -> 1 limit; linear in total mass, matching the observed ~M^1.18 dump). 89 events: mean|err| 0.76%, sd 0.97%, all 89 within 3% (max 2.90%). Named five: GW150914 0.00, GW190521 +1.45, GW170104 -0.74, GW170814 +0.04, GW151226 -0.19 (%).
- Physical flag: beta near 0.95 means density roughly proportional to mass and core radius almost independent of mass; with the lightest core at nuclear saturation (2.3e17) the 140+ Msun cores sit at ~5e18, 20x saturation. Not "flatline to zero": residual sd ~1%.
