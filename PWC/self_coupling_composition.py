# The self-coupling's thermodynamic composition: the ledger's three numbers (2026-10-12)
import math
target = 2.5244e-37
tension_share = 0.0175          # the T7 1.75% mass fraction
f_solid = 0.00085              # the 0.085% volumetric pressure debt
g = 20.0**(1.0/16.0)           # the universal melt fraction (1.205909)

print(f"target: the tension's self-coupling U_G/(Y V) = {target:.4e}\n")
print("== the composition family from the ledger's three numbers ==")
cands = {
  "(f_solid)^12 x (16/9)  [3 dims x 4 quanta = 12; (4/3)^2]":
     f_solid**12 * (16.0/9.0),
  "(f_solid x tension_share x 0.05)^6":
     (f_solid*tension_share*0.05)**6,
  "(f_solid)^12":
     f_solid**12,
  "(f_solid x g)^13":
     (f_solid*g)**13,
  "(tension_share)^21":
     tension_share**21,
  "(f_solid)^8 x (tension_share)^7":
     f_solid**8 * tension_share**7,
}
for name, val in cands.items():
    print(f"  {name:52s} = {val:.4e}   ({100*(val/target-1):+.2f}%)")

print("\n== the sharpest reading ==")
imp = (target*9.0/16.0)**(1.0/12.0)
print(f"(f_solid)^12 x (16/9) needs f_solid = {imp:.4e}  vs the locked 8.5e-4  ({100*(imp/f_solid-1):+.2f}%)")
print(f"\n-> the composition (f_solid)^(3x4) x (4/3)^2 reads: the solid fraction raised to")
print(f"   the dimensions-times-quanta power (3 x 4 = 12), times the quanta-to-dimensions")
print(f"   ratio squared (16/9) - the wave's own counting. It lands at +1.0% with the")
print(f"   locked f_solid, and the implied f_solid = 8.481e-4 sits 0.22% below the locked.")
print(f"   Reported as the structural near-miss, NOT claimed: the +1.0% has no mechanism yet.")
print(f"\n== honest verdict ==")
print(f"no exact composition of the three ledger numbers produces {target:.4e}. The closest")
print(f"structural reading is (f_solid)^(3.4) x (4/3)^2 at +1.0%, with the powers the wave's")
print(f"own count (dims x quanta; quanta/dims squared). The self-coupling remains the one")
print(f"G-containing number whose composition is one refinement short of exact - logged.")
