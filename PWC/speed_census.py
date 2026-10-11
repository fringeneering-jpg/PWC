# THE CENSUS: every fast object against its density/speed cap; outliers and anomalies (2026-10-09)
import math
c0 = 2.99792458e8; s = 1.0/19.0
rho_max = 1.304e15
Y_bow = 5.93e26
v_cap_max = 954.0                      # km/s, the rho_max cap
v_cap_gas = c0*math.sqrt(2*s/3.0)/1e3  # km/s, the gas-branch cap (constant)

print("THE TWO REGIMES:")
print(f"  gas-branch bodies (the sieve, Y = s rho c0^2/3):  v_cap = {v_cap_gas:,.0f} km/s = 0.1873 c0")
print(f"  rho_max bodies (the plateau, Y_bow locked):       v_cap = {v_cap_max} km/s\n")
print(f"{'OBJECT':34s} {'SPEED km/s':>10s}  {'REGIME':16s}  READING")
print("-" * 92)

def row(name, v, regime, note):
    print(f"{name:34s} {v:>10,.0f}  {regime:16s}  {note}")

row("Photon / light", 299792, "the medium", "c0 - the ceiling, not a limit")
row("Neutrino (minimal knot)", 299792*0.999, "zero winding", "just under c0 (threads everything)")
row("US 708 (fastest unbound star)", 1200, "gas-branch", f"47x BELOW its {v_cap_gas:,.0f} km/s cap - not an anomaly")
row("B1913+16 periastron", 902, "orbital", "at the rho_max cap scale - orbital, not passage")
row("RBH-1 (the runaway SMBH)", 950, "rho_max at cap", "AT the cap (954): the bow, the star forge")
row("B1508+55 (fastest pulsar)", 1083, "neutron body", "+1.3 sigma ABOVE 954 - the flagged cell (crust vs rho_n)")
row("CID-42 (recoil candidate)", 1770, "rho_max kicked", "1.9x above cap - the SLAMMED regime")
row("3C 186 (recoil candidate)", 2100, "rho_max kicked", "2.2x above cap - the SLAMMED regime")
row("M87 / Sgr A* (central SMBHs)", 30, "co-moving shell", "F = 0 - the rule says rest, the data says rest")

print("\n" + "-" * 92)
print("THE MAP:")
print("  - every GAS-BRANCH object (stars, planets, you) caps at 56,156 km/s: the sieve")
print("    threads the medium, so 1200 km/s stars are 47x inside their limit - not outliers.")
print("  - every rho_max BODY caps at 954: RBH-1 sits exactly on it (the bow).")
print("  - the GENUINE outliers: the recoil SMBHs (1.9-2.6x above 954) - the kicked shells,")
print("    forced through by the merger recoil = the SLAM; and B1508+55 at +1.3 sigma - the")
print("    neutron-body cell the census was built to resolve (crust vs bare rho_n).")
print("  - the prediction: no gas-branch object above 0.1873 c0, no rho_max body above 954")
print("    except the forced-passage slams - and every future fast object must land on the")
print("    grid at its own density.")
print("\n  effective density of the outliers (v -> rho_eff = 2 Y_bow / v^2):")
for name, v in [("B1508+55", 1083e3), ("CID-42", 1770e3), ("3C 186", 2100e3)]:
    print(f"    {name:10s} -> rho_eff = {2*Y_bow/v**2:.2e} kg/m^3 = {2*Y_bow/v**2/rho_max:.3f} rho_max")
