# PWC Compact-Knot Dimensionless Existence/Stability/Scaling Audit — Results

## Task as specified
Conserved-inventory phase-field solver (fields n, φ), fixed dimensionless
parameters n0=Δn=K=Λ=1, B=10, C=0.1, sweep N_target={0.25,0.5,1,2,4,8,16},
four pass/fail tests (existence, conservation, stability, scaling), grid
convergence at 512/1024/2048.

## What actually happened, in order

1. **Built the solver** (`knot_solver.py`) as a proper two-point BVP using
   `scipy.integrate.solve_bvp`, with the inventory constraint enforced via
   an augmented state variable Q(r) (running integral of the excess
   inventory) and μ as an unknown parameter solved for by the BVP solver
   itself — not a hand-rolled shooting/outer-loop method.

2. **Single-case test (N_target=1.0) converged**, status 0, residual
   9.96e-9 — but to a **delocalized** solution: φ stayed at ~2.7e-5
   everywhere, n stayed within 3.3e-5 of n0 everywhere. The integral
   constraint Q(R_box)=1.0 was satisfied exactly. This is a real,
   mathematically valid stationary point, not a solver failure.

3. **Tried much sharper initial guesses** (φ_peak=0.95, localized) to see
   if a genuine localized branch also exists. The solver relaxed back to
   the same delocalized solution regardless of the initial guess.

4. **Directly computed the energy functional** on the found delocalized
   solution versus a family of explicit trial localized profiles (fixed
   core radius, φ amplitude solved to satisfy the exact same N_target).
   Result: the delocalized solution has *lower* energy than every trial
   localized profile tested, and the trend was monotonic — energy kept
   decreasing as the trial profile became more spread out, with no
   interior minimum, heading straight toward the delocalized value.
   **Pass 1 (existence) FAILS for the declared parameter set
   (K=1, B=10, C=0.1, Λ=1).**

5. **Ran the pre-authorized phase-diagram scan** over B/K∈{0.1,1,10,50},
   C/K∈{0.01,0.1,1}, Λ/K∈{0.1,1,5} (36 combinations), comparing a
   grid-search "best localized trial" (R_core up to 8) against an
   analytic delocalized-limit energy. **First pass showed 6/36 as
   "LOCALIZED."**

6. **Caught this as a likely artifact before reporting it**: every one of
   those 6 cases had `best_R_core` sitting exactly at the edge of the
   tested grid (R_core=8, the largest value scanned) — the same
   monotonic-improvement tell as step 4. Re-ran those 6 cases with the
   R_core grid widened to 50: **all 6 kept decreasing monotonically all
   the way to R_core=50, no interior minimum anywhere.** Confirmed false
   positives caused by a truncated search range, not real physics.

## Final result

**Pass 1 (existence of a stable, finite-radius localized knot) fails for
all 36 tested combinations of B/K, C/K, Λ/K**, at the declared reference
scale (N_target=1). No genuine energy minimum at any compact radius was
found anywhere in the tested space — the true minimum is always the
fully delocalized configuration.

Passes 2 (conservation), 3 (stability), and 4 (scaling) were not run,
because they require an actual localized solution to test the stability
and scaling of, which doesn't exist for any tested parameter set.

## Why, physically

Nothing in `E[n,φ] = ∫[K/2(∇φ)² + Λφ²(1-φ)² + B/2(n-n0-Δnφ)² + C/2(∇n)²]`
penalizes spatial extent itself:
- The gradient term penalizes steep profiles, favoring smooth/spread ones.
- The double-well penalizes sitting at intermediate φ, but φ=0 and φ=1
  are equally free — nothing favors concentrating at φ=1 over staying at φ=0.
- The B-coupling only penalizes n departing *locally* from n0+Δnφ.

None of these cost anything for occupying a large volume. The fixed
inventory constraint can always be satisfied by diluting the same total
excess over an arbitrarily large region at vanishing amplitude — cheaper
than concentrating it into a knot, which must pay the double-well barrier
crossing (V(½)=Λ/16, unavoidable) at its wall. The conserved-inventory
constraint alone is not sufficient stabilization; there is still no actual
volume/pressure penalty in the functional — the missing ingredient PWC's
own "maximum compression" language (§3) would need to supply mathematically.

## Files
- `knot_solver.py` — the BVP solver, single-case test
- `knot_audit/phase_scan.json` — raw phase-scan output (includes the 6
  since-corrected false-positive rows, left in for transparency, NOT to
  be read as a result — see corrected verdict above)
- `knot_audit/single_case_test.png` — plot of the delocalized solution
