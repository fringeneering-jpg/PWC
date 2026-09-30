# PWC — Derivation Registry

One page. Every derivation: what it gives, where it lives, what reproduces it, and whether it is locked, open, or missing.
Start here before re-deriving anything. If a derivation isn't in this table, add it in the same commit that introduces it.

Status key: **LOCKED** = derived/tested and stands · **OPEN** = framework says what is needed, not yet derived ·
**NOT IN GIT** = stated as derived elsewhere (chat, notebook) but no text or script is in this repo yet.

**Read [`GR_TRAPS.md`](GR_TRAPS.md) first** — the standard-theory habits already cancelled, so they are not argued again.

Reproduce the merger chain in one command: `python PWC/derive_chain.py` (11/11 stated numbers of §0 Steps 1–7).

## Locked chain (PWC.md §0)

| # | Result | Where (PWC.md section) | Reproduce | Status |
|---|---|---|---|---|
| 1 | Hawking T = ħc³/(8πGMk_B), exact, zero free parameters, 18 orders of magnitude | §0 Step 1; §8 "Sonic-choke Hawking radiation" | `derive_chain.py` Step 1 | LOCKED |
| 2 | Merger = two neutron cores; mass **and** volume add; ρ_core ≈ 2.3×10¹⁷ constant | §0 Step 2 | `derive_chain.py` Step 2 | LOCKED |
| 3 | Medium has mass, held in 1/r²; reach ∝ M^½, core radius ∝ M^⅓, so two cores hold more than one | §0 Step 3 | `derive_chain.py` Step 3 | LOCKED |
| 4 | Max-P: ρ_max layer gets **thicker, not denser**, out to the radius where the pull drops below the yield | §0 Step 4; §3 | `derive_chain.py` Step 4/5 | LOCKED |
| 5 | GW150914 numbers: core 51 M☉ / 47.3 km; held 14 → 11 M☉; **3 M☉ released**; ρ_max = 1.304×10¹⁵; yield 3.23×10¹¹ N/kg; P = 4.21×10²⁶ Pa; γ = 3.36×10³¹ N/m | §0 Step 5 | `derive_chain.py` Step 5; **full derivation text: [`PWC/derivations/gw150914_shell.md`](PWC/derivations/gw150914_shell.md)** (source: AI Studio chat "Refining Black Hole Shell Density", 21–22 Sep 2026) | LOCKED |
| 6 | k-rule M_f = C + k·C^(2/3); k = 0.8524572447 (discovery), 0.868899 (GWTC-4); 89 events, mean −0.97%, std 2.02% | §8 "The core/gradient mass split"; "Single-source run" | `PWC/gwtc4_blind_tests.py`, `PWC/gwtc5_blind_test.py` | LOCKED |
| 7 | Surface-gravity deficit: release = κ[g(M₁)+g(M₂)−g(M₁+M₂)], g = GM/R² | §8 "The actual mechanism (2026-09-21)" | `PWC/gw_holdout_test.py`, `PWC/colab_gw_holdout_cell.py` | LOCKED |
| 8 | Merger 2^(−2/3) = 0.630 surface-pull ratio = SPARC 0.630 | §8 "Cross-domain confirmation (2026-09-22)" | `sparc/` — script not pinned, TODO | LOCKED |
| 9 | Rotation: g_obs = g_bar(1 + √(a₀/g_bar)); 149 SPARC galaxies, 0.1327 dex | §0 Step 7; §10 | `sparc/` — script not pinned, TODO | LOCKED |
| 10 | √(a₀·g_bar) from the tension rule: r_t = √(GM/a₀), 3D → 2D at r_t | §0 Step 7 "Deriving the √(a₀·g_bar) term" | `derive_chain.py` Step 7 | LOCKED (a₀ from tensioned-medium mass: next derivation) |

## Other derivations

| Result | Where | Status |
|---|---|---|
| a_hold = (c₀/√3)·√(Gρ₀/4) = 6.61×10⁻¹¹ (T1) | `PWC/knot_audit/eos_latent_heat.md` | LOCKED |
| H₀ from discrete unlocking; MOND–Hubble product invariant 0.02–0.06% (T7) | `PWC/knot_audit/t7_discrete_unlocking.md` | LOCKED |
| ρ₀ from bow-wave equilibrium, η ≈ 0.2488 (T2) | paper v1.9; `PWC.md` §8 bow wave | LOCKED to 0.5%; `t2_equilibrium.py` is cited but not in any branch — **NOT IN GIT** |
| Proton mass and charge radius from 720° topology + ρ_max | `PWC/predictions/proton_derivation_20260930.md` | LOCKED |
| RBH-1 wake, zero-fit | `rbh1/`, `PWC.md` §8 "RBH-1" | LOCKED (metallicity null in `rbh1/PREDICTION_metallicity.md`) |
| Tying expels L = c₀² per unit mass; untying absorbs it | `PWC.md` §4–§5 | LOCKED |

## Gaps: stated as derived, not reproducible from this repo

| Item | What is known | Where it should come from |
|---|---|---|
| **Shell on all black holes (Jaden: derived to 0.1%)** | `OPEN_WORK.md` still says "NEEDS DERIVATION"; the frozen `gwtc4_shell_vs_choke` test is recorded FAILED (R_max > r_sonic for 34 of 84, light holes). Only the GW150914 shell is reproduced (`derive_chain.py`). | AI Studio chat "Refining Black Hole Shell Density" / a Colab notebook — **paste the derivation here** |
| **Decompression rate after the merge → settling time τ** | `PWC.md` §8 "Bow wave vs. cavitation zone" (rebound passage): release of stored tension is clocked at c₀; §4: GW = the medium's own neighbour-reaction wave at c₀. τ measured: GW150914 4.68 ms (H1/L1 within 2%). No step connects the released medium to τ. The 26.3% light-BH number in `gwtc4_ringdown_mass.py` uses a borrowed radius and was withdrawn. | AI Studio chat / framework PDF — **paste here** |
| ρ_max at 2nd/3rd masses; ρ(r), P(r), c_s(r) and the stress law from core → max-P → decompression | `OPEN_WORK.md` | not derived |

## Already in the framework (pointers — do not re-add or re-derive)

| Topic | Where it already is | What is still open there |
|---|---|---|
| **Scale of passage** (light at the cap; ordinary matter a sieve, passes freely; an object at ρ_max cannot pass, so it ploughs a bow wave) | `PWC.md` Premise (line ~17); §2 sieve; §8 bow wave / cavitation zone | — |
| **Effective obstruction = core + ρ_max shell, not the bare core** (the medium can't flow through the crushed shell any more than the core) | `PWC.md` §8, line ~491 | "not yet turned into a number" — OPEN |
| **T2 creation law**, η = 1/4 (forward hemisphere ½ × cosine-average ½), ⟨v⟩ = c₀ (collapse-front speed, locked-phase sound speed), ρ₀ to 0.5% | `PWC/DERIVATION_BRIEF.md` T2; paper v1.9 | `t2_equilibrium.py` cited but not in any branch; gate that keeps Earth/Sun from heating (ungated law gives Earth ~1.4×10²¹ W) **exists only on branch `claude/pwc-engine-setup-ijmcxg`**: `sparc/domain_II_cavitation_wake_matter.py` — medium is blocked only above ρ > m_p/λ³ = 7.475×10¹⁶ kg/m³, so only compact cores impede the flow and stars/planets are transparent; `PWC/thermal_rate_criterion.py` (same branch) kills "nuclear detonation as inward heat absorption". Note Domain II's opening banner: its N = 4π/α = 1722 link is NOT Williamson's; the chain is kept as a record. Not merged to `main` |
| **Mass defect when knots combine (fusion)**: waves released, count drops, product weighs less | `PWC.md` §3/§4 "Binding energy" line (~133) | `OPEN_WORK.md` line ~49: intermediate scale (nucleon, nucleus, crust) — NEEDS DERIVATION |

## Not in the repo yet (stated 2026-10-01, untested — do not cite as results)

- **Nuclear-scale link (mine, from standard nuclear physics):** the liquid-drop mass formula has a surface term ∝ A^(2/3), the same scaling as the k-rule's M^(2/3); fusion gains by reducing surface.
- **Hydrogen is not an exception (Jaden):** every nucleus beyond H-1 holds neutrons at ~2.3×10¹⁷. Hydrogen is simply the **easiest knot to make** — the simplest bound state — which is why it is the most common matter and why cavitation recombination makes it first (`PWC.md` §8, "natural recombination product is hydrogen").

## Locked framing (Jaden's rulings — do not re-litigate)

- **The gravity wave is added medium, not a return to rest.** The merger adds ~3 M☉ of medium to the medium; there is **no return** — the extra medium stays — and it spreads at the medium's own speed c₀ **because it is the medium** (same as EM waves). **Contrast, a heavy planet passing by:** it tensions the medium and the medium **returns to rest tension** with nothing added — no wave. **One returns to rest; the other has no return.** No standard-theory mode/radius formalism anywhere in this work.
- The merger is not cavitation: the neutron cores simply join; the displaced medium is the wave.
- The medium has its own mass and sits in the 1/r² profile; reach uses total mass including the medium.
- **What the merger is, physically (Jaden, 2026-10-01):** the cores have to **push through the medium to join**. Each core sits in its own crushed ρ_max layer; as the cores close the two layers overlap, and medium cannot stay crushed twice, so the overlap is squeezed out of the crushed layer as free medium — about 3 M☉ of it added to the surrounding medium — and that medium spreading at c₀ is the gravity wave. It is geometry, not drag (matter is a sieve). GW150914 numbers (yield 3.23×10¹¹, total mass at the layer edge): layers 82.9 + 73.4 = 156.3 km thick separate, 112.6 km merged = **28% thinner**, ~44 km no longer crushed. How the added medium spreads out to give τ = 4.68 ms (c₀ across 44 km is only 0.15 ms; c₀·τ = 1403 km) is still to be supplied.
- The ρ_max layer's outer edge is where the pull from **everything inside it** (core + the layer itself, ≈ 62 M☉ at 159.6 km) drops below the yield 3.23×10¹¹; only mass inside counts. Compare layers by **thickness**, not by mass capacity (capacity grows with radius³ and misleads).
- The passage scale is continuous: photons at c₀, neutrinos just under, sieve matter ~99.99% empty, ~1000 km/s at ρ_max. Never binary.
- Merger-mass chain (rows 1–10) is validated data, not prediction.
- Nothing in git changes without his say-so; frozen predictions stay frozen.
