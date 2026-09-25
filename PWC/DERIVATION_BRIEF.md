# PWC — Derivation Brief

*Fringeneering — Jaden Allison · 2026-09-25*

A single self-contained brief for outside research: what Phase Wave Cosmology has derived, what it has tested, and the derivations still missing, each stated as a precise target with its allowed inputs. Full framework: [`PWC.md`](https://raw.githubusercontent.com/fringeneering-jpg/PWC/main/PWC/PWC.md) · open list: [`OPEN_WORK.md`](https://raw.githubusercontent.com/fringeneering-jpg/PWC/main/PWC/OPEN_WORK.md) · derivation order: [`CLOSURE_SHEET.md`](https://raw.githubusercontent.com/fringeneering-jpg/PWC/main/PWC/CLOSURE_SHEET.md) · frozen predictions: [`sparc/predictions/`](https://github.com/fringeneering-jpg/PWC/tree/main/sparc/predictions)

---

## 1. The premise in five lines

1. Space is a real medium with a minute mass and a propagation limit c₀ = c — not a zero.
2. The medium is EM(+)/EM(−) waves paired at a resting distance; heat holds the pairs apart where neighbour attraction and repulsion balance.
3. Matter is medium knotted into a 720° toroidal loop (Williamson–van der Mark); m = L/c₀². Light, phonons and Hawking emission are unpaired (disordered) waves.
4. The medium has a hard density ceiling ρ_max: black holes are shells at ρ_max, not singularities. At ρ_max knots break back into medium.
5. Gravity is the medium's tension; the extra pull in galaxies is tensioned medium. No zeros, no infinities, no singularities; mass–energy and thermodynamics conserved throughout.

**The medium cycle:** matter → compressed to ρ_max in a black hole → knots break → most waves pair into ordered medium (heat sets their resting distance) → the unpaired remainder leaves as light/heat/Hawking emission → travelling, it reorders into pairs (that reordering is redshift) → ordered medium is tied into matter again at formation.

---

## 2. What is derived (equations written)

**Sonic-choke Hawking temperature** (horizon = where free-fall infall reaches c₀; surface gravity by Unruh's analog-gravity method):
```
v(r) = √(2GM/r);  v = c₀ at r_s = 2GM/c₀²;  κ = ½|d(c₀² − v²)/dr| = c₀⁴/4GM;  T = ħκ/(2πk_B c₀) = ħc³/(8πGMk_B)
```
Exact Hawking formula, no free parameter, Planck mass → M87*.

**Black-hole shell chain (GW150914, 36 + 29 → 62 M☉):** cores add by mass and volume (ρ_core ≈ 2.3×10¹⁷ kg/m³, conserved); medium held in 1/r² with reach ∝ M^½ vs core radius ∝ M^⅓; medium packs to a ceiling and thickens rather than densifies.

| Quantity | Value |
|---|---|
| Combined core | 51 M☉, radius 47.3 km |
| Medium held before / after | 14 M☉ / 11 M☉ → **3 M☉ released** (the "radiated" mass is medium) |
| ρ_max | **1.304×10¹⁵ kg/m³** (10.87 M☉ in the 47.3→159.6 km shell) |
| Holding yield at ρ_max | **3.23×10¹¹ N/kg** |
| ρ_max·g | 4.21×10²⁶ Pa/m (a pressure *gradient*) |
| "γ" = P·R/2 | 3.36×10³¹ Pa (a *pressure*, ≈ 0.29·ρ_max·c² — the sonic-point scale) |

Frozen merger rule (single-source k = 0.868899) on 89 GWTC binary-black-hole events: mean final-mass deviation −0.97%, std 2.02%.

**√(a₀·g_bar) from the tension rule:** pull falls as GM/r² until it reaches the holding threshold a₀ at r_t = √(GM/a₀); beyond, it spreads in 2D (the spinning disk vents heat through the poles), so g = a₀·r_t/r = √(a₀·g_bar). **a₀ is the holding threshold of resting medium** — the galaxy-scale counterpart of 3.23×10¹¹ N/kg at ρ_max.

**Cascade (independent second route to the same shape):** dM_med/dr = dM_bar/dr + M_med/r → M_med ∝ r far out (flat rotation), no a₀ used.

**Shared tension (galaxy rotation):**
```
g_obs = g_bar + √(a₀·g_bar) · [1 + s · shared · (1 − locked)]
shared = min(g_in, g_out)/g_in      (radial load from inside AND outside a radius; ring geometry of measured baryons)
locked = bulge share of the normal pull
```
Medium loaded from both sides is taut and gives extra pull; one-sided (edge) gives less; locked (bulge, at max) gives none. Bodies keep the medium they hold; only the overlap of weak tails is shared — so s is small.

**Photon:** same substance as the medium at lower density, squeezed out like a watermelon seed by the surrounding high-density phase; it moves at the high-density phase's speed c₀ = √(stiffness/density). Gravitational waves are the same medium, hence equal speed (GW170817: equal to 10⁻¹⁵).

---

## 3. What has been tested (all predictions frozen and timestamped before each run)

| Data | Constants | PWC | Base √(a₀g) | McGaugh RAR |
|---|---|---|---|---|
| SPARC 149, held-out mean, 10 splits | fitted on training galaxies | 0.1309 | 0.1326 | 0.1283 |
| LITTLE THINGS 16 dwarfs (not in SPARC) | locked from SPARC | 0.3374 | 0.3417 | 0.3464 |
| GHASP 81 spirals (not in SPARC) | locked | 0.2655 | 0.2661 | 0.2657 |
| **PROBES 1342 spirals** (not in SPARC/GHASP) | locked | **0.2931** | 0.2986 | 0.2982 |
| PROBES 331 with ALFALFA HI gas added | locked | **0.2452** | 0.2490 | 0.2511 |

Galaxy-balanced RMS scatter in log g (lower is better). Constants: a₀ = 6.68×10⁻¹¹ m/s², s = 0.226 — **two global constants, zero per galaxy** (dark-matter halos: 2–3 per galaxy). PROBES: beats McGaugh by 1.7% (bootstrap 95% 1.3–2.1%); holds at stellar M/L 0.4 / 0.5 / 0.6 (2.0% / 1.7% / 0.6%); adding gas *grew* the lead (1.8% → 2.3%), so the tension term is not standing in for missing gas.

**Status: survived, not proven.** a₀ and s are currently fitted on SPARC, not derived — closing that is the top target below.

---

## 4. Derivations still missing — ranked targets

Each target: what to derive · allowed inputs · forbidden inputs (sealed targets) · what success looks like.

### T1 — The holding-threshold law a_hold(ρ) → a₀ with nothing fitted  *(highest value)*
- **Derive:** one rule a_hold(ρ) that gives **3.23×10¹¹ N/kg at ρ_max = 1.304×10¹⁵ kg/m³** AND **a₀ ≈ 6.7–7.6×10⁻¹¹ m/s² at the resting density ρ₀**.
- **Route:** P(ρ, s) (the medium's equation of state, from the neighbour pull/push vs distance) → stiffness → a_hold = the pull at which the medium can no longer be held/tensioned (dP/dr = −ρ·g at threshold).
- **Known clue:** the dimensional form a ~ c·√(Gρ) needs a prefactor ≈ 3.65 at the black hole but ≈ 0.33 at galaxy density — an ~11× mismatch (needed ratio 10.9–11.8 for H₀ = 67–73). Candidate: sphere (black-hole shell) vs disk (galaxy) geometry — but 4π = 12.6 does not fit and 4πr²/2πr is not dimensionless. Resolve this ratio from mechanics.
- **Allowed:** ρ_max, 3.23×10¹¹, c, G, the EOS. **Forbidden:** any galaxy rotation data (a₀ is sealed).

### T2 — Resting density ρ₀
- **Derive** ρ₀ from the cosmological background / propagation (c² = K/ρ₀), not from galaxies. Jaden's working figure: ρ₀ ≈ 0.95 ρ_crit ≈ 8×10⁻²⁷ kg/m³.
- Feeds T1.

### T3 — The medium's equation of state P(ρ, s)
- From the paired-wave picture: neighbour attraction/repulsion vs separation, heat setting the equilibrium distance (liquid-water LDL/HDL two-phase behaviour is the physical analogy).
- **Hard conditions:** c_s ≤ c everywhere; ∂P/∂ρ > 0 where stable; finite energy density as ρ → ρ_max; defined yield/phase response at ρ_max; defined entropy production; weak-field limit recovers Newton.
- **Sealed targets:** other GW events, ringdowns, shell profile.

### T4 — The overlap share s ≈ 0.23
- **Derive** the fraction of medium that is contested (overlap of weak tails between neighbouring reaches) vs held, from the reach profile r_t = √(GM/a₀). **Forbidden:** SPARC/PROBES fits.

### T5 — G from volume debt per tied wave
- ΔV_wave (volume taken out of the medium per knot) × stiffness → G; also the normalisation of the sonic choke.

### T6 — Lorentz contraction of knots (Michelson–Morley)
- Light moves at c₀ relative to the medium; the medium streams through the lab. **Derive** that a 720° toroidal knot moving through the medium at v contracts by exactly √(1 − v²/c₀²) and its internal clock slows by the same factor (Lorentz–FitzGerald from propagation-limited binding; cf. Bell, "How to teach special relativity"). Must hold to 10⁻¹⁷ (modern cavity tests). Also reproduce stellar aberration and Fizeau's drag 1 − 1/n².

### T7 — Redshift as reordering
- **Derive** the rate at which unpaired waves reorder into pairs vs distance, giving (1+z). Must also give supernova light-curve stretch exactly (1+z) and Tolman surface-brightness dimming (1+z)⁻⁴ — the tests that killed classical tired light.

### T8 — Growth law and BAO
- ΔV_wave × untying rate → expansion history H(z); BAO 147 Mpc from the medium's sound speed and the formation-era travel time; CMB z ≈ 1100.

### T9 — Cluster scale
- Bullet Cluster: run PWC's own lensing-mass calculation on Zhang et al. 2026 (arXiv:2606.19454) baryonic budgets (baryons = 52–86% of GR's needed mass, 101–165% of MOND's in the cores). Clusters generally: MOND-type laws are short by ~2× — PWC must not be.

### T10 — Merger lag and formation
- Untie-to-rest relaxation time (heat available × tension gap) → the ~1.7 s GW–gamma lag of GW170817 as a source effect.

---

## 5. Rules for any derivation

- Write the equation first; fix each value **once** from its allowed inputs; never tune to a sealed target.
- Freeze predictions with a timestamp before looking at data; keep failures visible (`TESTED_AND_DROPPED.md`).
- No zeros, no infinities, no singularities, no placeholders; conserve mass–energy; respect thermodynamics.

---

## 6. Suggested prompts

**Deep Think (derivation):**
> Using only the PWC inputs in this brief (ρ_max = 1.304×10¹⁵ kg/m³, holding yield 3.23×10¹¹ N/kg at ρ_max, c, G, and a medium of paired EM waves held at a resting distance by heat), construct an equation of state P(ρ, s) satisfying the listed hard conditions, derive the holding threshold a_hold(ρ), and evaluate it at a resting density ρ₀ derived from the cosmological background. Do not use galaxy rotation data. Explain the ~11× prefactor mismatch between the black-hole and galaxy regimes of a ~ c√(Gρ). Report a₀ with uncertainty and state what would falsify the derivation.

**Deep Research (literature and methods):**
> Find existing physics that could supply each missing PWC derivation: (1) equations of state with a hard density ceiling and finite energy at the ceiling (e.g. stiff/causal EOS, maximum-compactness limits); (2) threshold or yield laws in self-gravitating media linking a microscopic yield to a macroscopic acceleration scale like a₀ ≈ cH₀/2π; (3) Lorentz contraction derived from propagation-limited binding in a medium (Lorentz ether theory, Bell, analog-gravity "emergent Lorentz invariance"); (4) two-phase (LDL/HDL) liquid models giving sound speed from phase pressure differences; (5) acoustic-metric (Unruh, Visser, Barceló–Liberati–Visser) results usable for surface gravity and horizon thermodynamics in a real medium; (6) superfluid-vacuum / Volovik emergent-gravity work with a massive medium. For each, give the key equation, the paper, and how it would plug into targets T1–T8.

---

## 7. Round 1 results (2026-09-25: AI Studio, Perplexity, Gemini Deep Research) — checked

**Kept:**
- **T3 endpoints specified (Jaden):** ordered resting medium = 3D radiation-like EM lattice, P = ε/3, c_s = c₀/√3; locked medium at ρ_max = 1D stiff EM lattice, P = ε, c_s = c₀ (Zel'dovich 1962, JETP 14, 1143). Still to derive: the transition w(η) from ⅓ to 1, and the anisotropic stress tensor.
- **Light and gravitational waves are neighbour-reaction (EM-yank) waves, not compression:** c₀ = 1/√(μ₀ε₀) (Maxwell 1861–62). Compression is the separate slower mode. New target: ε₀, μ₀ from the pairing.
- **T1 progress:** a_hold ~ c_s·√(4πGρ). Locked branch at ρ_max: c₀√(4πGρ_max) = 3.14×10¹¹ (2.9% from 3.23×10¹¹ — but the shell edge sits at 0.87 r_s, where any c√(Gρ) scale is forced near c⁴/GM, so this is a consistency check, not a derivation). Ordered branch at ρ₀ = 8.74×10⁻²⁷: (c₀/√3)√(4πGρ₀) = 4.69×10⁻¹⁰ — the gap to a₀ drops from ~11× to ~6.7×. The remaining factor is not derived.
- **T5 lead:** G from secondary Bjerknes forces between pulsating volume defects, G = ρ₀ω²(ΔV/m)²/4π (dimensionally correct; historical Bjerknes gravity analogy). Needs ΔV and ω of the 720° knot. Check the Guyer & McCall citation.
- **T6 lead:** Bell (1976) / FitzGerald round-trip: longitudinal 2Lc₀/(c₀²−v²) vs transverse → L = L₀√(1−v²/c₀²). Applies directly if the knot is EM waves. Still needs time dilation (Kennedy–Thorndike) and all binding forces sharing c₀.

**Rejected (do not reuse):**
- √(40/3) "from the Buchdahl limit" — Buchdahl is 2GM/Rc² ≤ 8/9; no such prefactor. √(40/3) ≈ 3.6515 vs required 3.652 is a numerical match only.
- 1/π disk factor giving a₀ = 7.29×10⁻¹¹ — chosen to land in the window (with H₀ = 70 chosen too); equals a₀ ≈ 0.107·cH₀, MOND's coincidence.
- "Exactly 10.6" as a target — depends on which fitted a₀ (10.6 for 7.55, 12.0 for 6.68). Use a range frozen in advance.
- "shared ≈ 4.5" for clusters — impossible, shared ≤ 1 by definition.
- BAO "830,000 years" — arithmetic error (4.53×10²⁴ m ÷ 1.73×10⁸ m/s = 830 million years; comoving/proper mixed).
- "P ≈ ρc²/3 is maximally stiff" — no, that is radiation; stiff is P = ρc².
- Energy loss stretching packet spacing (T7 variant) — the classic tired-light error.

**Round 2 focus:** T3 transition w(η) and stress tensor from EM-lattice mode counting; then the remaining T1 factor from that, target range frozen before derivation; ε₀ and μ₀ from the pairing.
