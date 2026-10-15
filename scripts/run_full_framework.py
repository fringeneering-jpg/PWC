# run_full_framework.py - one command, every active verification, one scoreboard.
# python PWC/run_full_framework.py
# Each entry: (label, script, key-output lines to surface, optional status note)
import subprocess, sys, os, textwrap

ROOT = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(ROOT, "run_full_framework_last.log")

SECTIONS = [
("MACRO - black holes, mergers, lensing, speed limit", [
  ("BH pipeline (the 62 Msun chain, one-command rebuild)", "black_hole_pipeline.py",
   ["edge", "core", "954", "159.6", "62"], None),
  ("Merger mass drop E/S (89-event fit, out-of-sample GWTC-5)", "merger_energy_balance.py",
   ["mean", "0.89", "0.81", "out of sample"], None),
  ("Light bending push+pull (1.7512 arcsec)", "light_bending_push_pull.py",
   ["1.75", "gamma"], None),
  ("Speed limit / bow wave (954 km/s ladder)", "cavitation_speed_limit.py",
   ["954", "sound speed", "km/s"], None),
  ("Static-medium Hawking choke (T = hbar c0^3/8piGMkB)", "static_medium_check.py",
   ["kappa", "T", "0.291"], None),
  ("The fight + the neck (1.78 Msun displaced, 16.3x yield)", "fight_overlap.py",
   ["1.78", "6.90"], None),
]),
("MICRO - the knot, the charge, the footprint", [
  ("Knot equilibrium (H_trapped = s c0^2, the stretch unlocked)", "knot_equilibrium_eos.py",
   ["5.26", "1835.79", "4.4 mK"], None),
  ("Footprint dynamics ((pi+3s) lamC_bar, -0.085%)", "footprint_dynamics.py",
   ["3.2995", "-0.084", "bracket"], None),
  ("Charge as winding (q' = 0.9103e)", "quicycle_charge_map.py",
   ["0.9103", "1.2067"], None),
  ("Five gates (medium -> matter)", "transition_condition.py",
   ["7.475", "fold", "4.001"], None),
  ("Dislocation core geometry (b = 0.0566 r0)", "dislocation_core_geometry.py",
   ["0.0566", "0.1049"], None),
  ("Slip-knot vs braid (1836 = 4 x 137.036 x 3.349)", "slipknot_braid_check.py",
   ["1835.7", "134.2", "2.91"], None),
  ("The 0.085% is the matter (residual volume)", "residual_is_matter.py",
   ["0.2525", "4.15e+07"], None),
  ("Standing-wave kills (coherent 0.707, closure integers)", "standing_wave_profile.py",
   ["0.707", "3.302"], None),
]),
("WEB - stagnation, demand, supply, surface area, comet", [
  ("Stagnation scale (886 km / 1,910 Msun)", "stagnation_scale.py",
   ["886", "1910", "1.155"], None),
  ("Volume-to-mass friction (the V/M ladder)", "volume_mass_friction.py",
   ["954", "72"], None),
  ("RBH-1 demand function (m = dP dV / c0^2)", "rbh1_demand_test.py",
   ["244.8", "escape", "2.45e-04"], None),
  ("RBH-1 supply cap (stars swept gas)", "rbh1_supply_cap.py",
   ["cap", "810"], None),
  ("Surface-area thin skin (650 km)", "surface_area_law.py",
   ["650", "8.48e+20"], None),
  ("Comet survival map (the shallow rung)", "comet_survival_map.py",
   ["1e+18", "8.5e-09"], None),
]),
("RULINGS - the sealed arithmetic", [
  ("Rulings formal (pull-side, coupling, row 23)", "rulings_final_formal.py",
   ["1.75", "98.25", "0.2867"], None),
  ("Baseline cold (T = 0, the 2.7 K exhaust)", "baseline_cold_formal.py",
   ["2.7", "5.3e-05"], None),
]),
("THE MICRO LADDER - fold, bridge, G-chain, topology (2026-10-12)", [
   ("Fold force balance (19:1:18, F_EM/F_debt = 1/s exact)", "squeeze_debt_balance.py",
    ["19.0000", "18/19", "1.5291"], None),
   ("The two-regime bridge (9/(4s) = 42.75)", "bridge_derivation.py",
    ["42.7500", "42.7416", "9/(4s)"], None),
   ("The G-chain closure (f_solid^12 x 4s/81)", "final_G_lock.py",
    ["8.4989", "6.6769", "0.0850"], None),
   ("The topology equation (R_loop = r_e/(5 pi^2))", "topology_equation_corrected.py",
    ["49.3480", "27.5244", "18/19", "5 pi^2"], None),
   ("The yield anchor from the fold (Y_bow = 3 alpha hbar c0/(190 pi^4 r_e^4))", "yield_from_fold.py",
    ["5.9307", "5.93e26", "+0.011"], None),
   ("The ladder (4pi closure -> 1,342 galaxies)", "the_ladder.py",
    ["0.3297", "6.6110"], None),
]),
]

def run_one(script):
    path = os.path.join(ROOT, script)
    if not os.path.exists(path):
        return "MISSING", ""
    try:
        with open(LOG, "w", encoding="utf-8", errors="replace") as fh:
            r = subprocess.run([sys.executable, path], stdout=fh, stderr=subprocess.STDOUT,
                               cwd=ROOT, timeout=300)
        with open(LOG, "r", encoding="utf-8", errors="replace") as fh:
            out = fh.read()
        if r.returncode != 0:
            return "FAILED", out
        return "OK", out
    except subprocess.TimeoutExpired:
        return "TIMEOUT", ""
    except Exception as ex:
        return f"ERROR {ex}", ""

print("PWC FULL-FRAMEWORK RUN - one command, every active verification\n")
n_ok = n_fail = 0
for section, items in SECTIONS:
    print("=" * 74)
    print(section)
    print("=" * 74)
    for label, script, patterns, note in items:
        status, out = run_one(script)
        if status == "OK":
            hits = []
            for p in patterns:
                for line in out.splitlines():
                    if p in line and line.strip()[:90] not in hits:
                        hits.append(line.strip()[:90])
            if hits:
                print(f"\n[OK]   {label}")
                for h in hits[:3]:
                    print(f"       {h}")
                n_ok += 1
            else:
                print(f"\n[UNVERIFIED] {label} - ran, but no key number matched."
                      f" Counted as a FAILURE. Fix {script}.")
                n_fail += 1
        elif status == "MISSING":
            print(f"\n[FAIL] {label} - script missing ({script})")
            n_fail += 1
        else:
            print(f"\n[{status}] {label} - {script}")
            n_fail += 1

print("\n" + "=" * 74)
print(f"SCOREBOARD: {n_ok} sections verified, {n_fail} failed/skipped")
print("Full output per script: run it directly. Combined log tail: run_full_framework_last.log")
