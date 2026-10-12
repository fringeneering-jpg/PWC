# PWC heavy batch - headless RunPod deployment

The two scripts that timed out locally (numeric slowness, not breaks):
`dynamic_knot_HDF.py` (super-threshold pulse integration near rho_max)
and `domain_W_reformulated.py` (differential-evolution BVP sweep over 98 SPARC galaxies).

## Headless status (already safe - verified)

- `dynamic_knot_HDF.py`: already calls `matplotlib.use('Agg')` before pyplot
  and saves PNGs via `plt.savefig(...)` - NO `plt.show()` anywhere.
- `dynamic_knot_solver.py`: imports matplotlib but only for saving figures
  inside functions gated by the Agg call in the parent.
- `domain_W_reformulated.py`: imports NO matplotlib at all (pure
  numpy/scipy compute) - nothing to patch.

Belt-and-braces shim (only if you ever see a display error on the pod):
add this before any `import matplotlib.pyplot`:

```python
import matplotlib
matplotlib.use('Agg')
```

## Run on the pod

```bash
pip install -r requirements.txt
bash run_heavy.sh
```

All stdout/stderr of both scripts lands in `final_residuals_output.txt`.
The scripts also write their JSON results to their working directory:
`stage2_HDF_results.json` and `domain_W_reformulated_results.json`.

## Files in this package

- dynamic_knot_HDF.py
- dynamic_knot_solver.py   (local module the knot script imports - MUST ship)
- domain_W_reformulated.py
- vizier_t1.txt, vizier_t2.txt   (the SPARC data domain_W loads from its cwd)
- requirements.txt
- run_heavy.sh

Note: run the batch from THIS directory (both scripts resolve data/solver
relative to the working directory).
