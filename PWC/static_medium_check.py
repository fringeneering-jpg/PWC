"""Static-medium check for rows 24 / 24b (DERIVATIONS.md).
Speed budget c_loc^2 + v_ff^2 = c0^2, radial lengthening 1/sqrt(f): radial coordinate speed c0 f, transverse c0 sqrt(f);
surface gravity and Hawking temperature identical to the registry's (1/2)|d(c0^2 - v^2)/dr| form. Needs sympy."""
import math
import sympy as sp

r, rs, c, G, M, hbar, kB = sp.symbols('r r_s c G M hbar k_B', positive=True)
f = 1 - rs / r
c_loc = c * sp.sqrt(f)            # push: speed budget
L = 1 / sp.sqrt(f)                # pull: radial path lengthening
print('radial coordinate speed  =', sp.simplify(c_loc / L))
print('transverse coord. speed  =', sp.simplify(c_loc))

rs_val = 2 * G * M / c**2
kappa = sp.simplify((sp.Rational(1, 2) * c**2 * sp.diff(f, r)).subs(r, rs).subs(rs, rs_val))
print('kappa (static medium)    =', kappa)
T = sp.simplify(hbar * kappa / (2 * sp.pi * kB * c))
print('T                        =', T)

v2 = 2 * G * M / r
kappa_reg = sp.simplify((sp.Rational(1, 2) * sp.diff(c**2 - v2, r)).subs(r, rs_val))
print('registry kappa           =', kappa_reg, '  equal:', sp.simplify(kappa_reg - kappa) == 0)
print('c0^2 - v_ff^2 - c0^2 f   =', sp.simplify(c**2 - v2 - (c**2 * f).subs(rs, rs_val)))

# flat proper radial length (no lengthening): metric -c0^2 f^2 dt^2 + dr^2, kappa_flat = c0 f'(r_s) (1/s), T_flat = hbar kappa_flat/(2 pi k_B)
T_flat = sp.simplify(hbar * (c * sp.diff(f, r)).subs(r, rs).subs(rs, rs_val) / (2 * sp.pi * kB))
print('T_flat / T_Hawking       =', sp.simplify(T_flat / T), ' (without the lengthening: twice Hawking)')

print()
print('x     f     c_loc/c  n_radial  n_transverse  z=1/sqrt(f)-1')
for x in (0.05, 0.1, 0.2, 0.3, 0.4, 0.45):
    ff = 1 - 2 * x
    print('%.2f  %.2f  %.3f    %.2f      %.3f         %.3f' % (x, ff, math.sqrt(ff), 1 / ff, 1 / math.sqrt(ff), 1 / math.sqrt(ff) - 1))
print('x=0.50: exterior law -> stall (capped at the finite Max-P state; floor not derived)')

