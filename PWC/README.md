# PWC folder

| File | What |
|---|---|
| [`PWC.md`](PWC.md) | The framework — premise, §0 derivation chain, mechanisms, results |
| [`DERIVATION_BRIEF.md`](DERIVATION_BRIEF.md) | One-page brief: what's derived, what's tested, ranked missing derivations (T1–T10), research prompts, Round 1 results |
| [`OPEN_WORK.md`](OPEN_WORK.md) | Everything still to derive or test, by section |
| [`CLOSURE_SHEET.md`](CLOSURE_SHEET.md) | Derivation order for the five values that close the framework |
| [`knot_audit/eos_latent_heat.md`](knot_audit/eos_latent_heat.md) | Two-phase latent-heat EOS + T1 (a_hold at 1% match to SPARC/PROBES a₀) |
| [`knot_audit/t7_discrete_unlocking.md`](knot_audit/t7_discrete_unlocking.md) | T7 discrete unlocking + H₀_wall at 1% match to SH0ES + product invariant at 0.06% |
| [`knot_audit/independence_audit.md`](knot_audit/independence_audit.md) | Independence audit of the 2026-09-30 closures (regenerate: `python audit_independence.py`) |
| [`t2_equilibrium.py`](t2_equilibrium.py) | T2 equilibrium closure for ρ₀ (as supplied 2026-09-30), reproducing the cell output; audited in `independence_audit.md` §7 |
| [`knot_audit/heat_spacer_results.md`](knot_audit/heat_spacer_results.md) | Heat-spacer free-energy scan output (regenerate: `python heat_spacer_free_energy.py`) — a code check, not evidence for PWC |
| [`../archive/tested_and_dropped.md`](../archive/tested_and_dropped.md) | Hypotheses tested and dropped, kept so they aren't re-run |

Frozen predictions and outcomes for the galaxy tests: [`../sparc/predictions/`](../sparc/predictions/). Project overview: [`../README.md`](../README.md).

The earlier "Proofs and Data Still Needed" status page that lived here is superseded by `DERIVATION_BRIEF.md` and `OPEN_WORK.md`; it remains in the git history.
