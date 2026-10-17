# heat_ledger.py - the universe-sized cavitation's account (2026-10-16)
# The framework's numbers: the heat expelled = the cosmic thermal web's heat
# x 19 (the 19:1 balance); the matter's the knots' locked remainder at the
# median density. The account, precisely.
import numpy as np

c0   = 2.9979e8
rho0 = 8.74e-27               # the median density (locked)
a_rad = 7.5657e-16            # J/m^3/K^4 (the radiation constant)
T_cmb = 2.7255                # K (the CMB, the web's baseline)
f_solid = 8.4989e-4           # the locked solid fraction (the matter's share)

u_cmb = a_rad * T_cmb**4      # the web's heat, J/m^3
u_squeezed = 19.0 * u_cmb     # the total heat squeezed out of the medium
E_medium = rho0 * c0**2 / f_solid   # the medium's total energy budget (the knots' share defines the whole)
E_matter = rho0 * c0**2       # the matter's energy, J/m^3 (E = m c^2 at the median)

print("=" * 72)
print("THE UNIVERSE-SIZED CAVITATION - THE HEAT LEDGER")
print("=" * 72)
print()
print(f"  the cosmic thermal web's heat (the CMB):  {u_cmb:.3e} J/m^3")
print(f"  x 19 (the balance's ratio)               = {u_squeezed:.3e} J/m^3")
print(f"  that is the total heat SQUEEZED OUT of the universal medium")
print()
print(f"  the matter's remainder (E = rho0 c0^2):  {E_matter:.3e} J/m^3")
print(f"  the medium's total budget (via f_solid): {E_medium:.3e} J/m^3")
print()
print("THE REMAINDER, PRECISELY:")
print(f"  matter / total budget = f_solid = {f_solid:.6f}  ({100*f_solid:.4f}%)")
print(f"  the expelled heat's share of the total = {u_squeezed/E_medium:.6e}")
print(f"  heat : matter = 1 : {E_matter/u_squeezed:.3e}")
print()
print("=" * 72)
print("THE ACCOUNT: the heat expelled is the web's heat x 19 - the medium's")
print(f"whole squeezed-out total, {u_squeezed:.3e} J/m^3. What remains in the")
print(f"matter is the small fraction {100*f_solid:.4f}% - the knots locked at the")
print("median density, holding the 19:1's remainder. The rest of the universe")
print("is the field itself and the heat it once squeezed out.")
print("=" * 72)
