#!/usr/bin/env bash
# run_heavy_parallel.sh - 8-core batch: threshold scan + DE sweep, all output to file
set -u

OUT="final_residuals_output.txt"
: > "$OUT"

echo "=== PWC 8-CORE BATCH ===" | tee -a "$OUT"
echo "start: $(date -u +%Y-%m-%dT%H:%M:%SZ)  cores: $(nproc)" | tee -a "$OUT"

echo "" | tee -a "$OUT"
echo "--- 8-core threshold scan (drho 0.40..0.47, one full integration per core) ---" | tee -a "$OUT"
python run_parallel_knots.py 2>&1 | tee -a "$OUT"
echo "exit code: ${PIPESTATUS[0]}" | tee -a "$OUT"

echo "" | tee -a "$OUT"
echo "--- domain_W_reformulated.py (differential_evolution workers=-1, 98 galaxies) ---" | tee -a "$OUT"
python domain_W_reformulated.py 2>&1 | tee -a "$OUT"
echo "exit code: ${PIPESTATUS[0]}" | tee -a "$OUT"

echo "" | tee -a "$OUT"
echo "=== batch complete: $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" | tee -a "$OUT"
echo "results: threshold_scan_results.json, domain_W_reformulated_results.json" | tee -a "$OUT"
