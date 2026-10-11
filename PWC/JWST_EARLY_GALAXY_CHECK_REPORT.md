# JWST Early-Galaxy Check — PWC Reading, Frame-Free (math-check, v2)

- **Script:** `scratch/jwst_early_galaxy_check.py` (pure numpy; nothing in the repo modified)
- **Full output:** `scratch/jwst_check_output.txt`
- **Frame discipline (Jaden's ruling, via parent):** the PWC side uses NO time, NO ages, NO years.
  The only PWC physics is INVENTORY, RATE (in the medium's own units), and STATE. The ΛCDM-frame
  numbers (sections 1–4) are kept solely as the standard model's own problem statement.

## Locked inputs (quotes)

| Locked number | Source |
|---|---|
| Five gates: blockage ρ > m_p/λ³ = 7.475×10¹⁶; fold ρ_max/2→ρ_max; plateau work m·c₀²/kg; quantization m·R·c₀ = 4ℏ; hold by topology | `PWC/PWC/derivations/transition_condition.md` L14–28, L32–37 |
| T2 creation law: ρ̇ = η·ρ₀·π·G·⟨v⟩·ρ_b/a₀, η = 1/4, ⟨v⟩ = c₀; T2 untying partner Γ = ρ₀c₀/(ρ_max·R_p) | `PWC/PWC/DERIVATION_BRIEF.md` L86–96 |
| Stagnation scale: ρ·R ≥ 3a_max/(4πG) = 1.155×10²¹ kg/m² → R* = 886 km, M* = 1,910 M☉ | `PWC/PWC/derivations/stagnation_scale.md` L20–27 |
| RBH-1: 2×10⁷ M☉ SMBH, 62-kpc trail, 10⁶–10⁷ M☉ new stars, wake at the locked 954 km/s | `PWC/PWC/PWC.md` L478, L495 |
| RBH-1 supply cap, path (a) LOCKED: tying admixture ≤ ~15,500 M☉ per wake; stars are swept ambient gas | `PWC/PWC/derivations/demand_function_pressure_conversion.md` L146–154 |
| ρ₀ ≈ 0.95 ρ_crit → medium ≈ 95% of mass (matter ≈ 5%) | `PWC/CLAUDE.md` L39 |
| Flash escape fraction 2.45×10⁻⁴ | demand file L107 |
| "(1+z) mechanics" OPEN, not derived | `PWC/DERIVATIONS.md` row 17 |

Task-locked engine yield: one RBH-1-scale tying site = 2×10⁷ M☉ / 10⁷ yr = **2 M☉/yr**.

## (1)–(2) The standard model's own problem, in its own clock (NOT a PWC test)

- t(z=10/12/14) = 0.47/0.37/0.30 Gyr (Planck). Observed: JADES-GS-z14-0 (M*~4×10⁸), GN-z11
  (M*~10⁹), Labbé+2023 six candidates (M*>10¹⁰), ZF-UDS-7329 (M*~10¹¹, z=3.2).
- σ₀(M=10¹¹ M☉) = 3.27 (Eisenstein–Hu no-baryon, σ₈-normalized); D(z=12) = 0.0977 (exact
  integral agrees). **A 10¹¹ M☉ halo at z=12 is a 5.28σ peak**; n = 2.2×10⁻⁷ Mpc⁻³.
- At ε = 0.1: M*=10⁹ → 6.4×10¹⁰ halo (5.0σ); M*=10¹⁰ → 6.4×10¹¹ (6.8σ); **M*=10¹¹ → 6.4×10¹² (9.7σ)**.
- Expected per 100 arcmin² JWST field (z=11.5–12.5): 3.9×10⁻² (10¹¹ halo) / 1.1×10⁻⁶ (6.4×10¹¹)
  / 8.1×10⁻¹⁸ (6.4×10¹²) vs ~5–10 M*~10⁹ galaxies and ~1 M*~10¹⁰ seen → **30× and ~10⁶× abundance
  shortfall** (Planck's full σ grows it 3–10× further).
- ΛCDM's accretion rate is NOT the bottleneck (doubling ~48 Myr at z=12); the exponential
  abundance tail is. First 10¹¹ M☉ halo anywhere: z≈15.8 (EH σ; Planck: z≈14–15). The "too
  early" problem is the standard model's own anxiety on its own time axis.

## (3) Standard-frame cross-section (kept for the record only)

- RBH-1 scaling in the standard frame: 125 engines (continuous 400 Myr) or 5,000 (one burst
  each) per 10¹¹ M☉ galaxy; engine mass 2.5×10⁹ M☉ (2.5%) or 10¹¹ M☉ (100%, circular).
- T2 with ρ₀∝(1+z)³ (borrowed scaling): k(z=12) = 4.57×10⁻¹⁵ s⁻¹, k·t = 57.6, seeds 1.7×10⁹ M☉
  (2%); RBH-1 rate/T2 ratio 1.44 — the two locked rates meet only via the standard frame.
  With ρ₀ constant: k·t = 0.026, seeds 3.8×10¹² M☉ (38× — no growth).

## (4) Rate-ratio bookkeeping (frame-free)

- Tying heat: m·c₀² = 1.79×10⁵⁸ J per 10¹¹ M☉. At the locked 2.45×10⁻⁴ escape fraction the
  emitted rate is ~9×10¹¹ L☉ per forming galaxy vs ~10⁹–10¹⁰ L☉ observed → **91–906× rate excess**
  (a rate ratio; no duration involved).
- Standard-frame flag (record only): T2 read as cosmic SFRD overproduces the observed z~12
  rate by 10²–10⁵× — a comparison the framework declines (needs the ΛCDM census).

## (5) THE PWC READING, FRAME-FREE — INVENTORY, RATE, STATE (no time anywhere)

**[INVENTORY]** medium:matter = **20:1** (locked 95/5). To tie a 10¹¹ M☉ galaxy the region needs
10¹¹ M☉ of medium — any region holding 5×10⁹ M☉ of matter already has it on site (a sphere of
R = 570 kpc at locked ρ₀ — a length, not an age). Ratio 20, no time enters. **PASS.**

**[RATE]** (the medium's own units, ⟨v⟩ = c₀):
- The medium's own untying rate Γ = ρ₀c₀/(ρ_max·R_p) = 2.39×10⁻¹⁸ s⁻¹ (c₀-based).
- T2 tying rate per unit blocking mass, in units of Γ: k/Γ = η·π·G·ρ_max·R_p/a₀ = **0.870** —
  dimensionless, ρ₀ cancels out. At the locked 5% matter fraction: ρ̇/ρ_med = 0.0435 Γ → a
  region's whole 20:1 medium inventory ties in **23 natural units** (untying e-folds). Net at
  rest: −0.0065 per natural unit (the melt, as a rate).
- RBH-1 anchor: **1 engine-mass per trail crossing** (62 kpc at the medium's own 954 km/s).
  Site rate = 1,326×Γ = 1,525× k_rest(ρ₀); in the T2 law (k ∝ ρ_med) that reads as the site's
  medium at ~1,525 ρ₀. The locked set has NO law fixing the site's density — that gap is the
  whole "rate" question.

**[STATE]** (gauge ratios, not durations): melting state = 5% of the initially tied inventory
remains tied (95% re-absorbed); bath gauge T_now/T_Separation = 2.7 K/54 K = **1/20** — the bath
sits at 5% of its Great-Separation value, mirroring the 5% matter fraction. (54 K datum: Jaden
via parent; not in repo files → UNCHECKED.) The framework makes no statement about "when".

## VERDICT (three parts)

1. **What PWC supplies: the MASS — ratio 20, no time needed.** The knots cavitate into
   existence already dense (gates 1–5 at the fold); there is no assembly clock to fail. The
   JWST "too early" problem is the standard model's anxiety on its own time axis; for PWC it is
   not a question. Inventory check passes, dimensionless.
2. **The RATE is the medium's own:** 0.87× the medium's untying rate (c₀-based); a region's
   inventory ties in 23 natural units; the RBH-1 anchor is 1 engine-mass per crossing. The
   framework makes NO statement about "when" — "when" is the human concept; the physics is
   inventory, rate, state.
3. **Honest failures, kept visible (all frame-free):**
   - (i) **Engine inventory:** at the anchored yield-1, a 10¹¹ M☉ galaxy needs **5,000 RBH-1-scale
     engines (or 5.2×10⁷ stagnation knots)** — engine inventory = galaxy inventory, 1:1 circular.
     Fewer engines require counting re-crossings — a clock, which the framework declines.
     Observed SMBHs per galaxy ~1 vs 5,000 needed: the seed bootstrap is the load-bearing gap.
   - (ii) **The two locked yields disagree:** task-locked yield 1 engine-mass/crossing vs the
     repo's own sealed cap ≤15,500 M☉/wake (yield 7.75×10⁻⁴, ~1,300× lower). If the cap holds the
     channel is ~10³ short of any galaxy-scale inventory. The frozen −0.10 dex RBH-1 metallicity
     test decides.
   - (iii) **Flash rate:** at the locked escape fraction the tying of the observed galaxies emits
     ~9×10¹¹ L☉ vs ~10⁹–10¹⁰ L☉ observed (91–906× rate excess) — currently unaccounted.
   - (iv) **No state law** for f_matter(epoch)/ρ_med(epoch): the framework declines the epoch
     comparison; any forced comparison currently borrows the standard frame ((1+z) OPEN).

**One-paragraph verdict:** The JWST "impossible early structure" problem is the standard model's
own: a 10¹¹ M☉ halo at z=12 is a 5.3σ Press–Schechter peak (9.7σ for M*=10¹¹ at ε=0.1), and the
observed z>10 galaxies sit 30×–10⁶× above the per-field expectation — that is ΛCDM's anxiety on
ΛCDM's clock, and it does not touch PWC. In PWC's own frame the reading works as far as it goes:
the mass is supplied by the medium itself (20:1 inventory, ratio only, no time), and the tying
rate is the medium's own speed — 0.87× its untying rate, a whole regional inventory per 23
natural units, with the RBH-1 wake anchoring one engine-mass per trail crossing. The framework
makes no statement about "when", because "when" is the human concept; its physics is inventory,
rate, and state. What remains unresolved inside the framework's own terms is the engine
inventory: at the only anchored yield the seeds equal the galaxy (5,000 RBH-1-scale engines,
1:1 circular, vs ~1 observed SMBH per galaxy), the repo's own sealed supply cap makes the yield
1,300× smaller still, and the locked escape fraction implies a 10²–10³× flash-rate excess that
no forming galaxy shows. Verdict: PWC's reading dissolves the mass-budget problem cleanly and
legitimately refuses the standard model's clock, but its own rate anchor still requires an
engine/seed inventory of galaxy scale that no observation supplies — falsifiable, and currently
unresolved.

## Falsifiability (ratios/states, no clock needed)

(a) Assembly-gradient test: any high-z galaxy whose stellar content shows an assembly gradient
inconsistent with single-fold, full-density knot formation kills the "already dense" claim.
(b) Engine-inventory test: surveys of high-z fields finding no compact-mass population of the
needed scale (5,000 SMBH-scale or 5.2×10⁷ stagnation knots per galaxy) kill the bootstrap.
(c) Flash-rate test: the locked m·c₀² bookkeeping + 2.45×10⁻⁴ escape fraction requires 10²–10³×
the observed emission rate; its absence forces the escape fraction ~10⁻⁵× RBH-1's.
(d) The frozen RBH-1 metallicity bar (−0.10 dex): a pass refutes the supply cap, forcing the
cap-vs-yield conflict to be resolved against the task-locked yield.
(e) Any future law fixing ρ_med at tying sites below ~10³ ρ₀ makes the T2 rate unable to supply
galaxy-scale inventory (the 23-natural-unit rate is only operative at the fold).
