# threshold_crossing_prediction.py - the geometric cheat predicts the crossing (2026-10-15)
# The forge holds iff the pulse's energy clears E_lock (the 5pi^2 boundary's
# barrier). The pulse's energy scales acoustically as drho^2. ONE confirmed
# datum (drho 0.40 -> e_avail 2.6935) pins the scaling, and the crossing
# falls out closed-form - the same Bolyai move, applied to the scan itself.
import numpy as np

E_lock = 2.889795918367347
drho_ref = 0.40
e_ref    = 2.6934768876741297   # the confirmed case-1 datum (not retained)

print("=" * 72)
print("THE CROSSING, FROM THE GEOMETRIC CHEAT - no 25-hour grid")
print("=" * 72)
print()
print("1. THE THREE CLAUSES (the existence derivation, already on the record):")
print("   forge iff e_avail >= E_lock;  the selection law keeps {1, 5};")
print("   the heat balance welds. The flag's DERIVED; the grid only confirms.")
print()
print("2. THE ACOUSTIC SCALING:  e_avail ~ drho^2  (the pulse's energy density).")
drho_star = drho_ref * np.sqrt(E_lock / e_ref)
print(f"   pin the scaling with the one confirmed datum (drho {drho_ref} -> {e_ref:.4f}):")
print(f"   drho* = {drho_ref} . sqrt(E_lock/e_ref)")
print(f"         = {drho_star:.4f}")
print()
print("3. THE PREDICTED MAP (each of the scan's eight cases):")
print(f"   {'drho':>6s} {'e_avail pred':>12s} {'predicted flag':>16s}")
for drho in [0.40, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47]:
    e_pred = e_ref * (drho / drho_ref) ** 2
    flag = "RETAINED" if e_pred >= E_lock else "not retained"
    print(f"   {drho:>6.2f} {e_pred:>12.4f} {flag:>16s}")
print()
print("=" * 72)
print(f"PREDICTION: the RETAINED flag flips between drho 0.41 and 0.42,")
print(f"with the exact crossing at drho* = {drho_star:.4f}. The scan's own")
print(f"eight cases will confirm or break this - and the crossing's now")
print(f"a DERIVED number, waiting on the grid's arithmetic to check it.")
print("=" * 72)
