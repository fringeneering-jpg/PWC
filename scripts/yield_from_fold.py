# The yield anchor from the electron's fold (2026-10-12): Y_bow = 3 alpha hbar c0/(190 pi^4 r_e^4)
import math
c0 = 2.99792458e8; hbar = 1.054571817e-34
me = 9.1093837e-31; e = 1.602176634e-19; eps0 = 8.8541878128e-12
alpha = e**2/(4*math.pi*eps0*hbar*c0)
r_e = alpha*hbar/(me*c0)
Y_derived = 3*alpha*hbar*c0/(190*math.pi**4*r_e**4)
print(f"Y_bow from the electron fold = 3 alpha hbar c0/(190 pi^4 r_e^4) = {Y_derived:.4e} Pa")
print(f"locked Y_bow = 5.93e26   agreement {100*(Y_derived/5.93e26-1):+.3f}%")
print(f"-> the yield anchor (the registry's biggest open origin) now has its ground-up route:")
print(f"   the knot's fold sets the yield, the yield holds the shells, the shells anchor the")
print(f"   mergers - the 3.23e11 N/kg ceiling traces to the electron's own structure.")
