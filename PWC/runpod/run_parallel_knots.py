# run_parallel_knots.py - the 8-core threshold scan around E_lock (headless pod batch)
# Each case = one full dynamic integration, one core. No physics touched:
# run_case is the script's own function, imported under its __main__ guard.
import importlib.util, json, multiprocessing as mp

spec = importlib.util.spec_from_file_location("dkh", "dynamic_knot_HDF.py")
dkh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dkh)

Nx, L, x0, w, T_end = 1024, 60.0, 15.0, 2.0, 100.0
# the fine scan across the threshold crossing (0.40 below -> 0.42 above E_lock)
CASES = [0.40, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47]

def worker(drho):
    import numpy as np
    res = dkh.run_case(f"scan-{drho:.2f}", Nx, L, x0, w, drho, T_end)
    h = res['hist']
    if len(h['t']) == 0:
        return dict(drho=drho, failed=True)
    retained = h['Rknot'][-1] > 0.0
    return dict(
        drho=drho,
        peak_e_avail=res['peak_e_avail'],
        E_lock=dkh.E_lock,
        final_t=float(h['t'][-1]),
        E_drift_max=float(np.abs(h['E_total']-res['E0']).max()/res['E0']),
        M_drift_max=float(np.abs(h['M']-res['M0']).max()/res['M0']),
        rhomax_reached=float(h['rhomax'].max()),
        Rknot_final=float(h['Rknot'][-1]),
        Rknot_max=float(h['Rknot'].max()),
        RETAINED=bool(retained),
    )

if __name__ == "__main__":
    with mp.Pool(8) as p:
        out = p.map(worker, CASES)
    with open("threshold_scan_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\n=== 8-CORE THRESHOLD SCAN COMPLETE ===")
    for row in out:
        flag = "RETAINED" if row.get("RETAINED") else ("failed" if row.get("failed") else "not retained")
        print(f"  drho={row['drho']:.2f}  e_avail={row.get('peak_e_avail', float('nan')):.4f} "
              f" rho_max={row.get('rhomax_reached', float('nan')):.3f}  Rknot_final={row.get('Rknot_final', float('nan')):.4f}  -> {flag}")
    print("results -> threshold_scan_results.json")
