#!/usr/bin/env bash
# run_heavy.sh - run the two heavy PWC scripts headless, all output -> final_residuals_output.txt
set -u

OUT="final_residuals_output.txt"
: > "$OUT"   # fresh file

echo "=== PWC heavy batch: dynamic_knot_HDF.py -> domain_W_reformulated.py ===" | tee -a "$OUT"
echo "start: $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$OUT"

# 1) the knot pulse integration (writes stage2_HDF_*.png/json into its own outdir)
echo "" | tee -a "$OUT"
echo "--- dynamic_knot_HDF.py ---" | tee -a "$OUT"
python dynamic_knot_HDF.py 2>&1 | tee -a "$OUT"
echo "exit code: ${PIPESTATUS[0]}" | tee -a "$OUT"

# 2) the 98-galaxy differential-evolution BVP sweep
echo "" | tee -a "$OUT"
echo "--- domain_W_reformulated.py (98-galaxy DE sweep) ---" | tee -a "$OUT"
python domain_W_reformulated.py 2>&1 | tee -a "$OUT"
echo "exit code: ${PIPESTATUS[0]}" | tee -a "$OUT"

echo "" | tee -a "$OUT"
echo "=== batch complete: $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" | tee -a "$OUT"
echo "results JSON files (if written): stage2_HDF_results.json, domain_W_reformulated_results.json" | tee -a "$OUT"
