# PWC — Tested and Dropped

Hypotheses and model versions tested against real data and dropped or superseded. Kept so nobody re-runs them and so the reasoning that led to the current framework stays visible. Fuller per-domain records (Domains M–BB) live in `cosmology/sparc/` and the provenance manifest.

## Other dropped attempts (summary)

- **Medium decompresses at the same rate it compresses** — did not match real black-hole figures; replaced by the max-P "thicker, not denser" limit (PWC.md §0 Step 4).
- **Compounding self-gravity shell integration** — made the merged shell bigger instead of smaller (medium pulling on itself); dropped — the core pull comes from the centre of mass.
- **Galaxy medium budget `M_med = ξ·M_bar`**, HI point-mass lump, heat-proxy coupling coefficient — tested in `domain_M`–`domain_Q`; none survived holdout.
- **Grain-summed σ·Area at galaxy scale** — overshoots by 5–10 orders of magnitude; not coarse-graining invariant.
- **Ginzburg–Landau knot functional without a volume/pressure term** — no stable localized solution in a 36-case scan (`knot_audit/RESULTS.md`).
- **External-environment explanation for negative λ** (`domain_CC3`) — refuted; trend runs the opposite way.
- **Star-formation-driven expansion** (heat / knot-untying as dark energy) — no support in Pantheon+.
- **DF2/DF4 wake shadowing** — conflicts with c_s = c (Mach ~0.00024 at NGC1052's velocity).
- **Two-parameter cascade + tension fit** — 0.106 train / 0.1329 holdout: overfits; the one-constant form (0.1327) stands.

## Superseded merger-rule tests (discovery-paper calibration, since corrected — see PWC.md §8)

### Blind prediction: testing the frozen k against held-out mergers

Since k was fixed once from GW150914, the honest next step is a real prediction test: freeze k, apply the identical two-step rule (solve each initial mass for its core via `M = C + k·C^(2/3)`, add the cores, recompute a new gradient shell on the combined core via the same relation, read off the predicted final mass and radiated-energy fraction `ε_GW = 1 - M_f/(m1+m2)`) to real, independently-published masses for other mergers, and compare against their real, independently-measured remnant masses — no refitting per event.

Four real GWOSC/published events were tested this way, using real observational data (not simulated):

| Event | q = m2/m1 | Relative deviation in predicted ε_GW | Result |
|---|---|---|---|
| GW170814 | 0.83 | **−0.3%** | Strong hit |
| GW151226 | 0.53 | +41% | Miss |
| GW170608 | 0.69 | +48% | Miss |
| GW190412 | 0.28 | +47–50% (checked across two self-consistent parameter sets) | Miss |

**What this shows:** the frozen rule transfers with real precision near its own calibration regime (GW150914's mass ratio ≈0.86, GW170814's ≈0.83) and fails by a large, consistent margin (41–50%) everywhere else tested. That's a structured, repeatable pattern — not noise — and it rules out total mass as the organizing variable outright (GW190412 has high total mass, similar to the calibration event, and still misses badly). It does **not** yet establish that mass ratio itself is the missing variable: GW190412 also has a real, nonzero effective spin (χ_eff≈0.25, primary spin 0.22–0.60), so mass ratio and spin are confounded in this small sample and haven't been separated. That requires events that vary q and spin independently — not yet done.

**Known limitations of this specific test, to fix before treating the q-pattern as a real derivation target:**
- Every row must use source-frame m1, m2, and M_f from *one* self-consistent release/catalogue version — a first pass on GW190412 mixed the discovery-paper masses (30.1/8.3) with a later GWOSC-catalog remnant mass (35.6, measured against different progenitor masses, 27.7/9.0) and got a nonsense result (the deviation sign flipped depending on which mismatched pair was used). Caught and redone against the paper's own matched Table II value (M_f=37.3) before trusting it.
- ε_GW here is computed from published marginal median masses, not from posterior samples — subtracting independent marginal medians doesn't guarantee event-by-event mass conservation the way computing ε directly from posterior draws would. The current numbers are a legitimate first pass, not the fully rigorous version.
- Two catalogue versions for the same event (as used for GW190412) are a robustness check across analysis pipelines, not independent confirmation — they share the same underlying strain data and related waveform models.

**Not yet justified by this data, and not to be claimed until the posterior-level version below is done:** that mass ratio causes the failure; that spin causes the failure; that any specific PWC mechanism (e.g. an asymmetric-displacement/"wake" picture) is proven; that the rule predicts a hard equal-mass boundary; or that three first-pass misses independently establish a law. The sample is small and q/spin covary across it.

**The actual next validation layer** (not done tonight): pull one posterior-sample release per event, compute `ε_i = 1 - M_f,i/(m1,i+m2,i)` sample-by-sample from jointly-associated draws (not by subtracting independent marginal medians, which doesn't preserve event-by-event mass conservation), and report the frozen prediction's percentile within that posterior distribution — not just its distance from a central value. If GW170814 stays compatible while the other three stay materially high under that stricter test, the regime boundary is real and becomes a genuine derivation target.

**Stop-point summary:** the fixed GW150914-calibrated release rule transfers almost exactly to GW170814 but overpredicts first-pass central energy efficiencies by ~41–50% for GW151226, GW170608, and GW190412. These are internally consistent catalogue-level comparisons, not yet joint-posterior tests. No physical correction (q-dependence, spin term, or otherwise) should be added to the model until the posterior-level validation above is complete.

### First asymmetry-correction attempt — rejected as a universal rule

This is an **unfitted diagnostic calculation**, not a candidate law or partial confirmation. To test whether the frozen rule was missing a purely volumetric symmetry factor, one parameter-free candidate was evaluated: `S(q) = 2q/(1+q)`, `q = m2/m1`, derived from the ratio of the smaller core's volume to the combined volume of two equal-density cores. Applied without refitting, as `ε_corr = S(q)·ε_frozen`:

| Event | q | S(q) | ε_frozen deviation | ε_corrected deviation |
|---|---|---|---|---|
| GW170814 | 0.83 | 0.907 | −0.3% | **−9.6%** |
| GW151226 | 0.53 | 0.691 | +41.2% | −2.4% |
| GW170608 | 0.69 | 0.817 | +47.8% | +20.8% |
| GW190412 | 0.28 | 0.432 | +46.7% | **−36.6%** |

It improves the GW151226 comparison substantially, but fails as a universal correction: it degrades GW170814 from a near-exact match to a real deviation, leaves GW170608 still off, and overcorrects GW190412 hard enough to flip its sign. **A simple correction proportional to the smaller core's share of combined volume is rejected.**

Constraint this exposes: any future asymmetry function must satisfy `S(1)=1` and stay close to unity through the near-equal-mass regime GW150914/GW170814 occupy — it cannot be a direct global multiplier proportional to `2q/(1+q)`. Stated precisely: **if mass ratio is the dominant missing variable, the data disfavor `S(q)=2q/(1+q)` as a universal multiplicative factor** — not the stronger, unsupported claim that the correction must be flatter near q=1 and steeper toward q=0 in general, which assumes q is confirmed as the relevant variable when it isn't yet (spin is still confounded with it). Whether GW170814's −9.6% counts as a formal failure depends on a tolerance and posterior uncertainty that haven't been declared yet — it's a real degradation from near-perfect, not yet a declared miss.

No new symmetry function should be tried against these same four points until the posterior-sample audit above is done — doing so risks shaping a formula to pass exactly the data used to reject this one.


### GW190412 posterior-level stress test — frozen rule rejected for this event

This is the actual posterior-level validation the limitations above called for, completed for one event. Using all 23,984 released joint posterior samples from the real GW190412 source-properties release (`GW190412_posterior_samples_v3.h5`, `combined` group — downloaded from LIGO DCC, no resampling or subsampling), the observed radiated-energy efficiency was computed sample-by-sample as `ε_obs,i = 1 - M_f,i/(m1,i+m2,i)`, using each sample's own jointly-associated `mass_1_source`, `mass_2_source`, and `final_mass_source` — not independent marginal medians. The frozen GW150914-calibrated rule (k unchanged) was evaluated on the same joint mass draws.

| Quantity | Median | 90% credible interval |
|---|---|---|
| Observed ε_obs | 0.0293 | [0.0245, 0.0364] |
| Frozen prediction ε_pred | 0.0421 | [0.0372, 0.0486] |

The frozen prediction exceeds the observed efficiency in 100% of paired posterior samples. Its median lies at the 99.7th percentile of the observed efficiency distribution. The 90% credible intervals overlap only over a narrow numerical range — just 2.6% of predicted-efficiency samples fall within the observed 90% CI. **The one-constant GW150914-calibrated release rule is rejected for GW190412 under this posterior-level comparison** — strong posterior separation under the adopted event-inference model, not a frequentist p-value or an independent replicated detection, but no longer a weak table-median artifact either.

This result does not identify the missing physical variable — GW190412 has both a strongly unequal mass ratio and nonzero spin, so the miss may reflect mass ratio, spin, their coupling, or another missing merger-state variable. It does not validate any specific PWC mechanism (wake/drafting or otherwise), and it does not establish that the rule fails for all unequal-mass mergers — one event, rejected at the posterior level.

**Still incomplete:** the same test for GW151226, GW170608, and GW170814. The downloaded GWTC-1 posterior release for those three (`GW151226/170608/170814_GWTC-1.hdf5`, verified real files from LIGO DCC) contains detector-frame masses and spin parameters but no jointly-paired final-mass field. Completing this requires either a compatible remnant-property sample release or an independently verified numerical-relativity remnant-mass fit — no unverified formula has been substituted to fill the gap.

## Moved out of PWC.md (2026-09-25 cleanup)

Moved verbatim so PWC.md holds only the current framework. Frozen predictions and outcomes stay in `sparc/predictions/`.

### §8 merger: old 41–50% miss pattern

The prior "structured, repeatable 41–50% miss, worse at low q" finding does not survive: it tracks almost exactly with which events happened to be tested against catalog-sourced masses while GW150914 itself was calibrated against discovery-paper masses. This also means the rejected `S(q)=2q/(1+q)` asymmetry-correction attempt above was very likely chasing this same calibration artifact, not a real missing q/spin term — consistent with why it degraded the one event (GW170814) that happened to be least affected by the mismatch.

### §8 merger: old-k posterior test status

**What this does and doesn't establish:** it's a real, substantial correction to the blind-prediction result — same marginal-median method as the table above, properly source-consistent this time, not yet the deeper joint-posterior-sample version. The GW190412 posterior-level stress test below this section used the *old*, discovery-paper-calibrated k (0.8524572447) against posterior samples that are themselves catalog-sourced — the same mismatch this correction just found elsewhere. That test is flagged as needing to be rerun with k=0.868899 before its rejection can be trusted; it has not been rerun yet. Until then, treat the old posterior-level rejection below as itself suspect for the same reason the marginal-median table was, not as independent confirmation that k=0.8524572447 specifically fails.

### §8 merger: earlier merger attempts

— a substantial improvement over both the original 41–50% failure and this section's own earlier attempts tonight (compounding self-gravity, which was mathematically unstable; bare-core uniform-shell integration, which gave the wrong sign entirely by geometric necessity, r_boundary³∝M^1.5 always outpacing linear)

### §8/SPARC 0.630: within-galaxy slope comparison (retracted)

(Checked directly and explicitly ruled out as the wrong comparison: fitting the internal ρ_req-vs-g_bar slope separately *within* each of 107 individual galaxies gives a median of 1.527, std 1.186 — nothing like 0.63, and it shouldn't be expected to, since nobody derived a 2/3 prediction for radial structure at fixed total mass. That mismatch is not a contradiction; it's a different question that was mistakenly compared to this one and is retracted here.)

### §8 RBH-1: classical drag reading of the flash

**A rejected alternative, recorded for the same reason other rejected attempts are recorded in this document (§8's S(q) correction, the compounding-self-gravity merger attempt):** treating that same 1.9×10⁴¹ erg/s luminosity as the SMBH's own kinetic-energy loss via classical drag (`F=P/v`), then comparing the resulting deceleration to a claimed ~110 km/s velocity loss, was tested and **rejected**. The "110 km/s" in question is the measurement uncertainty on RBH-1's current velocity (954, +110/−126 km/s — a posterior credible interval, confirmed directly from the source paper), not an independent measurement of velocity lost to drag; no published deceleration measurement for RBH-1 currently exists to check any drag calculation against. Real CGM drag is separately acknowledged in the literature as a qualitative expectation (the same paper notes the BH "would have slowed down since merger due to drag," with no number attached) — a real, open item, just not one with a number yet, and not the one "confirmed" by the 110 km/s coincidence.

### §10: gradient-λ tension model (superseded by shared tension) and refuted environment story

- **Form tested:** `g_pred = choke(g_bar, a0, n=1/2) * (1 + λ·|d ln(g_bar)/d ln(R)|)` — one additional universal coefficient λ on the real, per-galaxy log-log slope of each galaxy's own baryonic acceleration profile (a genuine gradient computed from real Rad/Vgas/Vdisk/Vbulge points, not a free per-galaxy fit, same discipline as domain_K).
- **Result, full 141-galaxy sample:** galaxy-balanced RMS improves from 0.1292 dex (baseline choke) to 0.1266 dex (with the gradient term) — better than the ~0.127 dex reference figure this project already had, and closing further on the McGaugh RAR benchmark.
- **Robustness, properly checked (not just one split):** a 10-seed train/holdout stability check shows the extension beating baseline on galaxy-balanced holdout RMS in **10/10 seeds** — mean improvement −0.0028 dex, consistent in direction and magnitude across every seed, not a lucky split. (A first pass scored against point-pooled RMS instead of galaxy-balanced RMS showed a weaker, non-robust 7/10 — that was a metric error on the analysis side, not a property of the result; fixed before this was reported.)
- **λ's sign: real and robust, but not yet actually explained — a specific causal story for it was tested and failed.** λ comes out negative in all 10/10 seeds (−0.034 to −0.072), and the tension = negative pressure convention (already fixed earlier in this document) is consistent with a negative coefficient in principle. But a specific, falsifiable causal story built on top of that — that the tension comes from *external* competing masses, so galaxies in denser real environments should show a *more* negative λ — was tested directly (`domain_CC3_tension_vs_environment.py`) against real, confound-controlled 2MRS neighbour counts (same volume-limited method as the existing environment domain), using a properly balanced tercile split (43 vs 43 galaxies, not a lopsided isolated-vs-group cut). **Result: refuted, not just unconfirmed.** Low-density tercile λ = −0.077; high-density tercile λ = **+0.014** — the sign moves toward positive in denser environments, the opposite of the prediction. The error was scale, not the sign convention: the gradient term describes radial structure *inside* one galaxy's own disk (bulge/disk transitions, internal mass concentration), and the external-neighbor story tested a completely different scale (Mpc-scale galaxy clustering) that was never actually implied by the mechanism. Honest current state: negative λ is a real, robust empirical result; *why* it's negative remains genuinely open, and this specific external explanation for it is now closed off rather than left untested.

### §10: per-star independently-sourced medium mechanisms

Every mechanism tried this session where the medium's own extra mass/tension is sourced *independently* by each star (weighted by distance, by mass, by an individual per-star threshold, by mass-ratio extrapolation from §8's black-hole relation) failed the same way: any purely additive, pairwise-sourced quantity that tracks the visible mass distribution can only rescale the ordinary baryonic curve, never flatten it — confirmed by direct computation across five independent attempts, not asserted.

### §10 shared tension: failed variants (records in sparc/predictions/)

What failed on the way: full rebound (s = 1) overshoots; treating one-sided pull as tight (the U form) and a bulge pin on its own both came out with the wrong sign — consistent with one-sided and locked medium giving less, not more.

### OPEN_WORK: superseded gradient-λ item

- Blind holdout, identical splits (2026-09-25, `sparc/domain_CC2_vs_RAR.py`, 10 seeds, 70/30, galaxy-balanced): PWC base 0.1265 · PWC+tension 0.1237 (2 constants) · McGaugh RAR 0.1210 (1 constant). Tension term closes the gap to ~0.0027 dex (~2%) and beats McGaugh on 3/10 splits; not yet ahead on average. (Superseded single-split figure: 0.139 vs 0.130.) — NEEDS WORK

### OPEN_WORK: superseded gradient-λ item

- Negative λ on the gradient term: cause — OPEN
