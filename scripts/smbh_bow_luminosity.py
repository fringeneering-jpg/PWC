# smbh_bow_luminosity.py - the runaway's bow from the heat ledger (2026-10-16)
# L_bow = A_cross . v_smbh . Q_exp^max  - the 19:1:18 balance processed in
# real time. The bow is NOT gas friction; it is the medium's debt being paid.
import numpy as np

c0     = 2.9979e8
Q_CMB  = 4.175e-14
Q_exp  = 18.0 * Q_CMB                 # 7.515e-13 J/m^3 (the locked derived)
v_smbh = 0.996 * c0                   # the runaway's speed (RBH-1, locked)
kpc    = 3.0857e19

print("=" * 72)
print("THE RUNAWAY'S BOW - the ledger's luminosity receipt")
print("=" * 72)
print(f"  Q_exp^max = 18 . Q_CMB = {Q_exp:.3e} J/m^3   (the expelled debt)")
print(f"  v = 0.996 c0 = {v_smbh:.3e} m/s")
print()
print("the bow's cross-section: the swept area where the medium's compressed")
print("to the ceiling. The observed bow's radius is the MEASURED input (the")
print("framework's method: measure the geometry, derive the luminosity).")
for R_bow_kpc in [2.0, 5.0, 10.0]:
    R = R_bow_kpc * kpc
    A = np.pi * R**2
    L = A * v_smbh * Q_exp
    print(f"  R_bow = {R_bow_kpc:4.1f} kpc  ->  L_bow = {L:.2e} W  ({L/3.828e26:.2e} L_sun)")
print()
print("=" * 72)
print("the receipt: the derived L_bow is a PREDICTION - compare it against the")
print("observed bow's emission (the RBH-1 bow's ionized/stellar luminosity).")
print("If they meet, the 19:1:18 balance has been seen processing in real time;")
print("if not, the cross-section's geometry (or the debt's rate) is the named")
print("correction. Either way the number is on the board, derived before the")
print("check - the framework's discipline.")
print("=" * 72)
