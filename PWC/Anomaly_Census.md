# PWC Anomaly Census — the retroactive sweep (2026-10-09)

Seven anomalies, seven independent math checks (each with its script in `PWC/`), every
verdict honest: RESOLVED = the framework's numbers cover it; FAIL = the mechanism was
tested and died; NO NEW CONTENT = identical to the standard reading; UNTESTABLE =
the framework's own numbers don't yet support the claim.

## The scoreboard

| # | Anomaly | Check | Verdict |
|---|---|---|---|
| 1 | RBH-1 runaway SMBH (the star trail) | `rbh1_demand_test.py`, `rbh1_supply_cap.py`, `bow_and_merger_check.py` | **RESOLVED** — the bow fires AT the cap (ram = yield, 5.934×10²⁶ = Y_bow exactly); the trail is the medium cavitating, not gas (the supply cap: 65–810× short) |
| 2 | GW150914-style mergers | `bow_and_merger_check.py`, `merger_energy_balance.py` | **RESOLVED** — the 3 M☉ released as the medium: h = 4.0×10⁻²¹ at 410 Mpc vs the observed ~10⁻²¹; no shock, the wave |
| 3 | Fast objects vs their caps | `speed_census.py`, `density_speed_grid.py` | **RESOLVED as an instrument** — every object's speed reads back its effective density: B1508+55 = 0.775 ρ_max (at its own cap), the recoil SMBHs = 0.21–0.29 ρ_max (the slam), RBH-1 = 0.996 of the cap (the bow) |
| 4 | UHECR / GZK (Oh-My-God) | `gzk_uhcer_check.py` | **NO NEW CONTENT** — the bath is the standard 2.725 K blackbody; threshold, mean free path, and the anomaly are numerically identical in both frameworks. (Flag: the locked escape fraction 5.3×10⁻⁵ = Ω_γ — standard cosmology relabeled) |
| 5 | Pulsar glitches (Vela, Crab) | `pwc_glitch_stall_check.py` | **FAIL** — the stall-and-recatch misses Δν/ν by 31 orders, wrong sign (stationary medium → spin-down), inverted Vela/Crab trend, no recovery timescale, Crab/MSPs rotate permanently above the cap. The medium is too thin to carry a glitch, period |
| 6 | Fast Radio Bursts | `frb_snap_check.py` | **FAIL** — the single-bubble snap forces f·τ = 1; FRBs have f·τ ≈ 10⁴–8×10⁷. One collapse cannot be both ms and GHz. Survives only as ~10⁶ successive snaps — a mechanism not in the locked set |
| 7 | 'Oumuamua | `oumuamua_gradient_check.py`, `medium_relative_speed.py`, `rest_speed_needed.py`, `solid_content_audit.py`, `continuous_ramp_check.py` | **FAIL** — the gradient is 63–1205× too large (or 10²⁴× too small), wrong sign (sunward vs anti-sunward), the stationary-medium drag is directionless at ~10⁻²⁰ m/s², and no rest speed fixes it (needs 2×10⁴ c₀) or density (needs 3×10¹⁴ ρ₀). Only the r⁻² shape matches — reported, not claimed. **Not ours to explain yet** |
| 8 | Hubble tension | `thermostat_tension_check.py` | **SH0ES-side only** — H₀_wall = 73.8 (1.010) from four fundamentals; the Planck-side reading is qualitative (the 147 Mpc shell is adopted, not derived; the thermostat adds zero computed shift; the 54 K figure is not in the repo) |
| 9 | Boötes birefringence | `pwc_bootes_birefringence.py` | **UNTESTABLE as locked** — the locked rate IS the global average → zero void contrast by construction; the maximal reading gives +0.012°, ~40× below current sensitivity; two inconsistent rates sit in the repo. The sign test is the right falsifier, once the void-local rate is locked |
| 10 | JWST early galaxies | `jwst_early_galaxy_check.py` | **PARTIAL** — PWC dissolves the mass budget (the medium holds 20× the mass; knots form already dense; the "too early" panic is the standard clock's, not PWC's — time is the local clock rate, Jaden's ruling). BUT the engine inventory is 1:1 circular at the anchored yield (5,000 engines vs ~1 observed SMBH per galaxy), the repo's sealed supply cap is 1,300× lower still, and the flash-rate excess (91–906×) is unaccounted |

## What the sweep established

1. **The framework's claims survived only where its numbers actually cover them:** the bow (RBH-1), the merger wave, the speed grid. Those are the anchors.
2. **Four mechanisms died honestly:** the glitch stall, the FRB snap, the 'Oumuamua gradient/drag, and the GZK "resolution." Each with its kill-numbers in the record. That is the methodology working.
3. **Two of the framework's own gaps got named by the sweep:** the missing T(t)/state law (the epoch comparison is refused, and any forced one borrows the standard frame), and the engine-inventory/yield disagreement in the JWST channel (the sealed supply cap vs the task yield — the frozen RBH-1 metallicity bar decides).
4. **The time ontology is now written:** no universal clock; the clock rate = the medium's local speed; c_loc² + v² = c₀² (row 24b) makes the v → c and the horizon slowings ONE effect — the pushback at the limit. "When" is the human concept; the physics is inventory, rate, state.

## The hard stake (re-picked after the sweep)

The Boötes stake was untestable as locked. The first forward-looking falsifiable prediction is now:

> **Prediction #1 — the speed census.** Every body's speed must land on the grid at its
> own density: no gas-branch object above 0.1873 c₀, no ρ_max body above 954 km/s except
> the forced-passage slams. One future observation of a gas-branch body above 0.1873 c₀
> — or a ρ_max body above 954 that is NOT a stripped recoil — kills the law. No free
> parameters; the grid is the instrument.

> **Prediction #2 — the void reach law.** R_void = √(G·M_walls/a₀): log-log slope
> exactly 1/2 with a₀ frozen, against the void catalogs already on disk
> (`cosmology/voids/`). A slope ≠ 1/2 kills it. Testable now, no new instruments.
