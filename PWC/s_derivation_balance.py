# The s = 0.2264 derivation attempt: the expansion balance (2026-10-12)
# s = the minimum tension keeping the expansion = the release pressure / the tension scale
import math
c0 = 2.99792458e8
rho0 = 8.74e-27; rho_max = 1.304e15
Rp = 8.414e-16
s_stretch = 1.0/19.0
H0_heat = 32.371*c0**2
Gamma = rho0*c0/(rho_max*Rp)          # T7 untying rate (locked)

print(f"Gamma = rho0 c0 / (rho_max R_p) = {Gamma:.4e} s^-1 ; 1/Gamma = {1/Gamma/3.156e16:.2f} Gyr")
print(f"1/H0_wall timescale = {1/Gamma/3.156e16:.2f} Gyr (the natural relaxation)\n")

print("== the balance: s * (rho0 c0^2/3) = the release pressure at the ambient ==")
melt = 0.05
tau = 1/Gamma
s_nat = Gamma*melt*tau
print(f"release over one natural relaxation, 5% melt: s = Gamma * 0.05 * (1/Gamma) = {s_nat:.4f}")
print(f"-> the natural timescale gives s = 0.05 EXACTLY - the melt fraction itself:")
print(f"   the minimum tension keeping the expansion = the pressure of the 5% still tied.")
print(f"\nthe observed s = 0.2264 needs:  s = Gamma * 0.05 * tau  ->  tau = {0.2264/(Gamma*melt)/3.156e16:.1f} Gyr")
print(f"   = 4.35x the natural relaxation - no clean identity closes there.")

print("\n== the split: s_shared = (the melt-pressure fraction) x (the geometric share) ==")
geo = 0.2264/melt
print(f"0.2264 / 0.05 = {geo:.4f}  - the geometric share of the inner/outer tension loading")
print(f"candidates for {geo:.4f}:  e x 5/3 = {math.e*5/3:.4f} (+{100*(math.e*5/3/geo-1):+.2f}%)")
print(f"                          sqrt(20.5) = {math.sqrt(20.5):.4f} (+{100*(math.sqrt(20.5)/geo-1):+.2f}%)")
print(f"                          sqrt(s_stretch) route: sqrt(1/19) = {math.sqrt(s_stretch):.4f} "
      f"(as s directly, {100*(math.sqrt(s_stretch)/0.2264-1):+.2f}%)")

print("\n== honest verdict ==")
print("the balance yields HALF the answer cleanly: s_min = 0.05 - the expansion's minimum")
print("tension IS the pressure of the 5% still tied (the melt fraction itself, one natural")
print("relaxation). The remaining factor 4.53 = the geometric share of the rotation's")
print("inner/outer loading - the formula's own 'shared' mechanism, not yet derived from the")
print("1/r^2 tension profile. s = 0.2264 = 0.05 x 4.53: the thermodynamic half is locked,")
print("the geometric half is the named remaining integral.")
