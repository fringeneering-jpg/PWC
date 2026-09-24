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
- Merger rule at joint-posterior level with k = 0.868899 (GW190412 rerun) — NEEDS TEST
- Residual that shrinks with core mass: locate the three regime thresholds relative to ρ_max — NEEDS DERIVATION
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

- Dump-rate term: at fixed g_bar, do galaxies with higher untying rate (star formation, luminosity per mass) sit below the 0.1327 curve? Add the term and check whether scatter drops below 0.1327 — NEEDS TEST
- Dump rate bounds: Sun (GM☉ change from planetary ranging matches mass loss to ~10⁻¹⁴/yr) rules out a per-star 1/r² dump only — consistent with collective, cluster-scale growth; test the feeding-rate ladder Sgr A* → active nuclei → quasars for a rising gravity deficit in host centres — NEEDS TEST
- Collective cluster-scale growth: turnaround radii (Local Group ~1 Mpc, Virgo) smaller than gravity alone predicts? and the unusually cold local Hubble flow — NEEDS TEST
- Thick-wall growth: current void velocity profiles (Hamaus et al. 2014/2016) show thick-walled small voids collapsing and thin-walled large voids expanding. Test wall thickness vs void expansion at fixed void size for outward motion beyond what wall gravity allows — NEEDS TEST
- Growth profile through the tensioned web (not 1/r²): the equation — NEEDS DERIVATION
- Dump rate from untying rate: the equation (volume released per untied wave × untying rate) — NEEDS DERIVATION

- Blind holdout, 104/45 split: PWC 0.139 vs McGaugh 0.130 dex — NEEDS WORK
- Dwarf-spheroidal transfer: ρ = 0.74 but 0.253 dex scatter — NEEDS WORK
- Cascade: why the coefficient is exactly 1; the residual ~8% outer decline — NEEDS DERIVATION
- Negative λ on the gradient term: cause — OPEN
- Medium budget/closure: control volume, source term, boundary flux, EOS, gravity coupling — NEEDS DERIVATION
- Cluster lensing (Bullet Cluster) with PWC's own calculation on the Zhang et al. 2026 data — NEEDS TEST

## Heat and the thermal web (§9)

- Heat as the source of the medium's tension: tension per unit heat, linked to γ = 3.36×10³¹ N/m (§0) — NEEDS DERIVATION

- What sets the medium's chiral imbalance, and the heat-wave strength at galactic rotation rates — NEEDS DERIVATION
- Heat seeking untying sources independently of the rotation axis — NEEDS TEST
- Heat choke vs real WHIM density/temperature data — NEEDS TEST
- Occupancy/band-filling equation for the EM-coupling heat choke — NEEDS DERIVATION

## Runaway black holes (§8, RBH-1)

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

- Light bending factor of 2: pressure term + geometric term as one equation — NEEDS DERIVATION
- Polarization-dependent lensing (birefringence) — NEEDS TEST
- Ringdown sandbox df/dt = κ·f^α fit to the real ridge — NEEDS TEST
- Medium tension from indirect probes: multi-messenger timing (SN 1987A), flyby anomaly — NEEDS TEST
- "Neutrino-to-neutron" ~1% resistance: the formula — NEEDS DERIVATION

## Underlies several items

- The medium's equation of state, P(ρ, s) — NEEDS DERIVATION
