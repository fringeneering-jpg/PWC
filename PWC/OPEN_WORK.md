# PWC — Open Work

What still needs doing, by section. **NEEDS DERIVATION** = no equation yet. **NEEDS TEST** = derived, not yet checked against data. **OPEN** = question not yet decided.

## The five values that close the framework

Fix each once, from one place — then it must predict what it was not set from.

| Value | Predicts once fixed |
|---|---|
| Resting density of the medium, ρ₀ | a₀'s value; the loose side of the zipper |
| Holding threshold vs density (one rule: 3.23×10¹¹ N/kg at ρ_max ↔ a₀ at ρ₀) | a₀ with zero fitted constants |
| Volume per tied wave | G; dump rate; supernova and cluster growth; Hubble tension |
| P(ρ) between ρ₀ and ρ_max | black-hole shell profile; bow wave; water-hammer spike |
| Growth-vs-time law | redshift = (1+z); CMB z ≈ 1100; BAO 147 Mpc |

## Core chain (§0, §3, §8)

- a₀'s value as a holding threshold: one threshold-vs-density rule must give 3.23×10¹¹ N/kg at ρ_max and a₀ at resting density. Dimensional form c·√(Gρ) needs factor ~3.65 (black hole) vs ~0.33 (galaxy) — an 11× mismatch; does sphere-vs-disk geometry account for it? (Needed ratio 10.9–11.8 across H₀ = 67–73; 4π = 12.6 does not fit, and 4πr²/2πr is not dimensionless.) — NEEDS DERIVATION
- Pole-venting prediction, spin vs extra gravity. Domain PV (2026-09-25, `sparc/domain_PV_pole_venting.py`): INCONCLUSIVE — rotation-curve spin proxies share velocities with g_obs; a no-spin-physics null mock (`domain_PV_null_mock.py`) reproduces the signal (Ω: real +0.42 vs mock +0.43). Only independent proxy, Hubble type: partial ρ = −0.20 (p = 0.036, ~0.11 after 3-proxy correction), predicted direction, not significant. Clean version: ATLAS3D fast vs slow rotators (λ_R, independent stellar kinematics) at fixed g_bar — NEEDS TEST
- Stationary medium, sweep effect: rotation-curve lopsidedness (~half of disks) should line up with each galaxy's direction of motion through the medium (rest frame: CMB, 370 km/s for us); strongest for fast-moving cluster galaxies — NEEDS TEST
- Preferred-frame limits in gravity (pulsars, solar spin: parts in 10⁹) are all at g ≫ a₀; state explicitly that the sweep effect lives below a₀ — NEEDS DERIVATION
- Web confinement for ellipticals: isolated field ellipticals (no filaments feeding them) should get less extra pull and fall below the relation vs node ellipticals — NEEDS TEST
- Pole-venting prediction: pressure-supported ellipticals with no disk fall below the relation — NEEDS TEST
- 2D step of the √(a₀·g_bar) derivation: early-type (non-disk) galaxies follow the same relation (Lelli et al. 2017) — does confinement come from the disk or from the web? — NEEDS TEST
- ρ_max at a second and third mass (GW151226, GW170814 ringdown extractions not yet clean) — NEEDS TEST
- G from volume debt per tied wave × the medium's stiffness (also the sonic-choke normalization) — NEEDS DERIVATION
- Volume debt per wave: the value, and why it is identical for every wave — NEEDS DERIVATION
- Merger rule vs trivial baseline (2026-09-25): on the 83 events in `gwtc_bh_core_deviation_data.json`, the frozen PWC rule gives RMS 1.73% (mean −0.73%); a fixed-fraction rule M_f = 0.952·(m1+m2), set once on GW150914, gives RMS 1.44% (mean −0.67%). The PWC rule does NOT yet beat a constant-loss baseline — it needs a prediction the constant fraction cannot make (e.g. the mass-ratio/spin dependence of the loss). Caveat: catalogue final masses are GR numerical-relativity inferences from the inspiral, not independent measurements, so both scores are against GR-derived values. Independent test: final masses from the ringdown frequency alone (GW150914 extraction gave 232 Hz vs 272 Hz predicted — unresolved) — NEEDS WORK
- Merger rule at joint-posterior level with k = 0.868899 (GW190412 rerun) — NEEDS TEST
- Residual that shrinks with core mass: locate the three regime thresholds relative to ρ_max — NEEDS DERIVATION
- GWTC-4.0 blind (84 events, 2026-09-25): merger rule −0.56% ± 1.62%, but the residual trend is the rule's radiated fraction ∝ M^(−1/3) (6.3% → 3.8% across mass) against data rising slightly (3.6% → 5.2%). Either derive a mass-scaling for M_grad that stays near-scale-free, or show the regime picture beats this simpler reading — NEEDS DERIVATION
- ρ_max universality FAILED with the shell edge at the horizon (GWTC-4.0: ρ_shell ∝ M^(−2.5), range ×1,300). Reformulate: fix ρ_max, let the shell thickness follow from M_grad ("thicker, not denser"), predict the shell edge vs the horizon for every event — NEEDS DERIVATION
- Surface-gravity deficit: all four residuals share one sign — second-order term — NEEDS DERIVATION
- 2^(−2/3) for extended galaxies from the same starting physics as compact cores — NEEDS DERIVATION
- ρ_max independently from nuclear/crust packing (Coulomb lattice) — NEEDS DERIVATION

## Knots and matter (§4, §5)

- Intermediate scale between the electron knot and the neutron core (nucleon, nucleus, crust) — NEEDS DERIVATION
- Stable-knot field equation needs a volume/pressure (max-compression) term — NEEDS DERIVATION
- Unordered state (charge, light): is "out of phase" the right description, and what pressure threshold joins it back into the order — OPEN
- Does knot handedness (chirality) decide matter vs antimatter — OPEN
- Can a knot be tight and not-tight at once, or always one or the other — OPEN
- Strong-force matter: what "L" locks nucleons if not EM light — NEEDS DERIVATION

## Galaxies (§10)

- Void rims too thin (burnt, not pushed aside): pushed-aside voids are compensated by their rims; burnt voids are not. Large voids are measured undercompensated (Hamaus, Sutter & Wandelt 2014, universal void profile; void lensing DES/KiDS). Derive PWC's deficit vs void size and compare with ΛCDM's environment-driven undercompensation — NEEDS DERIVATION
- Void shapes: evacuated voids round off with expansion (Icke 1984 "bubble theorem"); burnt voids keep the irregular footprint of their hot spots. Test: measured void ellipticity vs size/redshift against ΛCDM mock voids; PWC predicts no rounding trend. Hot-side check run 2026-09-25 (`voids/PREDICTION_thermal_edge.md`): FAILED as frozen, no signal (49%, p = 0.59; sensitivity ~5×10⁻⁸ in y). Rounding test blocked on a ΛCDM baseline: the matched mocks are 64 Horizon Run 4 SDSS DR7 mocks already run through VoidFinder by Douglass et al. 2023 — available on request only (HR4: Juhan Kim, KIAS; void team: Douglass & BenZvi, Rochester) — NEEDS TEST
- Dump-rate term: at fixed g_bar, do galaxies with higher untying rate (star formation, luminosity per mass) sit below the 0.1327 curve? Add the term and check whether scatter drops below 0.1327 — NEEDS TEST
- Dump rate bounds: Sun (GM☉ change from planetary ranging matches mass loss to ~10⁻¹⁴/yr) rules out a per-star 1/r² dump only — consistent with collective, cluster-scale growth; test the feeding-rate ladder Sgr A* → active nuclei → quasars for a rising gravity deficit in host centres — NEEDS TEST
- Collective cluster-scale growth: turnaround radii (Local Group ~1 Mpc, Virgo) smaller than gravity alone predicts? and the unusually cold local Hubble flow — NEEDS TEST
- Thick-wall growth: current void velocity profiles (Hamaus et al. 2014/2016) show thick-walled small voids collapsing and thin-walled large voids expanding. Test wall thickness vs void expansion at fixed void size for outward motion beyond what wall gravity allows — NEEDS TEST
- Growth profile through the tensioned web (not 1/r²): the equation — NEEDS DERIVATION
- Dump rate from untying rate: the equation (volume released per untied wave × untying rate) — NEEDS DERIVATION

- Shared-tension overlap share s ≈ 0.23: derive it from how far a body's reach runs before it is weak tail (currently measured on SPARC, not derived) — NEEDS DERIVATION
- Shared tension on interacting / merging galaxies: held medium changes hands only in catastrophically close orbits, so the 0.23 share should fail there, toward more pull — NEEDS TEST (no dataset with full mass models found yet; tidal dwarfs Lelli+2015 give Mdyn ≈ Mbar, known result, not blind)
- LITTLE THINGS rebuilt from HI maps + Spitzer 3.6 µm (adds DDO46, DDO47, F564-V3, Haro29; replaces noisy Vtot² − Vdm² baryons) — NEEDS TEST
- Rerun the GW190412 posterior-level merger test with the single-source k = 0.868899 — NEEDS TEST
- Dwarf-spheroidal transfer: ρ = 0.74 but 0.253 dex scatter — NEEDS WORK
- Cascade: why the coefficient is exactly 1; the residual ~8% outer decline — NEEDS DERIVATION
- Medium budget/closure: control volume, source term, boundary flux, EOS, gravity coupling — NEEDS DERIVATION
- Cluster lensing (Bullet Cluster) with PWC's own calculation on the Zhang et al. 2026 data — NEEDS TEST

## Heat and the thermal web (§9)

- Heat as the source of the medium's tension: tension per unit heat, linked to γ = 3.36×10³¹ N/m (§0) — NEEDS DERIVATION

- What sets the medium's chiral imbalance, and the heat-wave strength at galactic rotation rates — NEEDS DERIVATION
- **BH-merger thermal signature (corrected 2026-09-25):** one measured case — the disputed ZTF flare candidate for GW190521/S190521g (Graham et al. 2020, PRL 124, 251102): a brightening at roughly constant temperature (~10⁵¹ erg, ~80 d), not a cold deficit. Standard models ALSO predict post-merger cooling (horizon-region gas ~150 → ~10 MeV in GR simulations; disappearing thermal X-rays before SMBH-binary merger, arXiv:2304.02575), so 'cooling after merger' does not discriminate. PWC needs a quantitative prediction — amount, timing and location of any cooling beyond loss-of-heating — before AGN-flare follow-ups can test it — NEEDS DERIVATION
- **Decisive heat test:** cold expansion wakes (SN 1987A inner ejecta ~20 K dust, Cas A unshocked ejecta, kilonova cooling), hot bow-shock fronts and hot web nodes all fit PWC — but also fit standard adiabatic cooling + hot-to-cold heat flow, so they do not discriminate. The discriminator: an expanding/untying region that is already HOTTER than its surroundings yet still draws heat in (heat flowing up the temperature gradient). Standard thermodynamics forbids it without work; PWC's heat-to-untying rule predicts it — NEEDS TEST
- Heat seeking untying sources independently of the rotation axis — NEEDS TEST
- Heat choke vs real WHIM density/temperature data — NEEDS TEST
- Occupancy/band-filling equation for the EM-coupling heat choke — NEEDS DERIVATION

## Runaway black holes (§8, RBH-1)

- Conventional mass budget for RBH-1 (checked 2026-09-25): no upstream/sightline gas measurement exists. Kaul & Oh 2026 (arXiv:2604.13155) close the budget by cooling-induced entrainment of surrounding hot CGM along the whole tail, ASSUMING a typical halo density n_H ≈ 5×10⁻³ cm⁻³ at ~10⁶ K (from other galaxies' quasar-absorption surveys, not RBH-1). At that density the hot gas within 1–3 kpc of the 62 kpc tail holds ~10⁷–10⁸ M☉ — enough on paper. PWC criterion #1 wins if a direct measurement (background-quasar absorption; future X-ray) finds density well below that — NEEDS DATA
- Predicted star mass in the trail from the wake's volume debt — NEEDS DERIVATION
- Predicted trail width (no-scatter squeeze) vs measured RBH-1 trail width — NEEDS TEST
- Bow-wave compression profile and water-hammer pressure ΔP = ρ_max·c·Δv — NEEDS DERIVATION

## Cosmic scale (§6, §7)

- What makes the medium push apart at cosmic scale (dark energy): star-formation route failed; aggregate merger medium release not yet calculated — NEEDS DERIVATION
- Space holds excess heat: how that excess drives accelerated expansion, and whether it is a standing property of space (not tied to star-formation rate, so the Pantheon+ star-formation null does not apply) — NEEDS DERIVATION
- Excess heat vs the measured 2.7 K of space: what the medium's heat is, relative to measured radiation temperature — NEEDS DERIVATION
- BAO scale (147 Mpc, measured to ~1% by DESI, same ruler in the CMB): derive it from the medium's sound speed and the formation-era travel time before the wave froze — NEEDS DERIVATION
- Cosmic web from cavitation: reproduce the matter power spectrum and galaxy age spreads in filaments — NEEDS TEST
- Local growth around untying sites, from light echoes: V838 Mon polarization ring vs spectroscopic distance (agree ~10%); SN 1987A ring (51.4 kpc) vs LMC eclipsing-binary distance (49.6 kpc) (agree ~3.5%) — size of growth allowed around a star/supernova — NEEDS TEST
- Melting rate: early-universe baryon density (BBN deuterium, CMB) and today's census (incl. FRB missing-baryon count, Macquart et al. 2020) agree at ~5% of critical — how much matter has melted since formation, and whether that fits voids as "cooked soup" — NEEDS DERIVATION
- Stock-cube spin at the largest scale: whole-universe rotation is limited to < ~10⁻⁹ of the expansion rate (CMB uniformity) — spinning/breaking up must be piecewise, not global — NEEDS DERIVATION
- Early massive galaxies (JWST) from the bow-wave mechanism: mass vs redshift — NEEDS DERIVATION

## Light and gravitational waves

- Light bending factor of 2 (1.75″ at the solar limb, measured to ~10⁻⁴): the photon is squeezed in a channel between EM waves and cannot hop paths. Two equal terms: (1) **pressure** — the squeeze is stronger on the mass side, the gradient pushes the photon over (alone: κ = 1, 0.87″, the Newtonian/Soldner value); (2) **geometric** — the medium around the mass is compressed ("thicker, not denser"), so the channel itself is laid through more medium and curves; the confined photon follows it (another κ = 1). Total n = 1 + 2GM/(rc²) → α = 4GM/(bc²). Maps onto ε (squeeze/yank) and μ (density/inertia) each shifting by 2GM/(rc²), n = √(εμ); and onto GR's time + space halves. Confinement means both polarizations share the channel — no gravitational birefringence, as observed. Derive each term's GM/(rc²) from the medium's loading around mass (follows from the ε₀/μ₀ pairing derivation) — NEEDS DERIVATION
- Polarization-dependent lensing (birefringence) — NEEDS TEST
- Ringdown sandbox df/dt = κ·f^α fit to the real ridge — NEEDS TEST
- Medium tension from indirect probes: multi-messenger timing (SN 1987A), flyby anomaly — NEEDS TEST
- "Neutrino-to-neutron" ~1% resistance: the formula — NEEDS DERIVATION

## Underlies several items

- ε₀ and μ₀ from the medium's pairing: yank strength between neighbouring paired waves → 1/ε₀; density of paired waves → μ₀; must reproduce c₀ = 1/√(μ₀ε₀) — NEEDS DERIVATION
- EOS transition between the ordered branch (P = ε/3, c_s = c₀/√3) and the locked branch (P = ε, c_s = c₀): order parameter η and w(η), derived from EM-lattice mode counting / locking, not chosen — NEEDS DERIVATION
- Holding threshold: with c_s = c₀/√3 at rest the gap to a₀ drops from ~11× to ~6.7×; source of the remaining factor (√40 in the locked-branch coefficient √(40/3) ≈ 3.65 is a numerical match only) — NEEDS DERIVATION
- Volume released per untied mass: today's space is 95% of its final volume, matter is 5% of the mass → ΔV/m = (1/0.95 − 1)V ÷ 0.05M = 1.053/ρ_crit = 1/ρ₀ — **0.207 m³ per neutron, 112 cm³ per electron** (two routes agree). Growth factor per neutron ~10⁴⁴ — DERIVED (arithmetic), premise untested
- The 95%: remaining stretch 1/0.95 = 1.053 (5.3% volume) vs real cavitation stretch of clean water ≈ 6.4% (−140 MPa ÷ 2.2 GPa; Zheng et al., Science 1991). Derive the 95% from the medium's own tensile/cavitation limit via P(ρ) — NEEDS DERIVATION
- Does newly created space push adjacent matter apart? Decides everything below: if yes, neutron-lifetime traps (~10⁴ stored, 1% untying → ~20 m³ new space per fill) would already show it — OPEN
- Neutron lifetime gap: bottle ≈ 878 s vs beam ≈ 888 s (~1%, ~4σ) — ~1% of free neutrons vanishing without a proton = untying into medium? Predict the size — NEEDS DERIVATION
- Neutron lifetime inside an intense laser field (never measured): standard physics predicts no change; PWC with compounding untying predicts a shorter lifetime rising with laser power. Magnetic (~1 T) and material bottles already agree, so static field strength alone does not drive it — NEEDS TEST
- What caps compounding untying (heat → expansion → more untying)? PWC allows no runaway — NEEDS DERIVATION
- Prometheus laser cooling by neutron untying: heat drawn per untie at 350 K ≈ aT⁴·0.207 m³ ≈ 15 TeV (19 TeV isothermal) vs break-even ≈ 3.1 GeV (100 neutrons × 30 MeV spallation + 99 × 0.782 MeV decay heat, at 1% untying). If the premise holds: ~10¹⁸ unties/s, ~0.1 g free neutrons, ~0.5 GW to make, 2.5 TW removed, ~2×10¹⁷ m³/s new space. Fission is ruled out as the coolant (reactor calorimetry: net heater ≥100:1) — NEEDS TEST
- The medium's equation of state, P(ρ, s) — route: P_net = rigidity − cohesion; rigidity w = (1 + 2S)/3 from wave alignment S(ρ, T) (Onsager compression vs Maier–Saupe heat); cohesion Y = EM yank between pairs (same as ε₀). Gives c_s(ρ), ρ_max, the 1.053 stretch, a₀, and v_cav ≈ √(2Y/ρ) (see DERIVATION_BRIEF T3) — NEEDS DERIVATION
- Runaway-SMBH wake threshold v_cav: wakes only above it (RBH-1 ~950–1,000 km/s has one; central SMBHs don't); check recoil candidates (3C 186, CID-42); slowest wake bounds Y — NEEDS TEST
