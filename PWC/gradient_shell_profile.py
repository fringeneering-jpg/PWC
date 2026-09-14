import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# =====================================================================
# GRADIENT-SHELL DENSITY/PRESSURE PROFILE
# Pure compressible-fluid hydrostatic equilibrium. No GR, no spacetime
# curvature -- this is the same math used for stellar atmospheres and
# planetary interiors for over a century.
# =====================================================================

G = 6.674e-11
Msun = 1.989e30
km = 1000.0

# --- SETUP, exactly as specified ---
rho_inf = 1.0          # baseline density far from any core (normalized units)
Lambda = 1e-9          # baseline hydrostatic pressure far away (real, nonzero, not 0)
rho_max = 2 * 2.3e17 / (2.3e17)  # placeholder normalization -- see note below

# --- THE TWO EQUATIONS THAT GOVERN THIS, DERIVED, NOT ASSERTED ---
#
# 1. Hydrostatic equilibrium (the fluid doesn't accelerate, pressure
#    gradient exactly balances gravitational pull inward):
#       dP/dr = -G * M(r) * rho(r) / r^2
#
# 2. Mass continuity (how much fluid mass is enclosed within radius r
#    grows as you integrate outward through denser/thinner shells):
#       dM/dr = 4*pi*r^2*rho(r)
#
# These two are forced by basic mechanics (force balance + geometry) --
# not assumptions, not GR. To close the system (2 equations, 3 unknowns:
# P, rho, M) we need ONE more relation: an equation of state connecting
# P and rho. THIS is the genuinely open, undetermined piece -- the
# "equation of state" flagged as missing since the very first audit
# tonight. Building the equations honestly means showing that gap
# explicitly, not hiding it.
#
# Physically reasonable choice, consistent with "baseline pressure
# Lambda at baseline density 1, stiffening as compression increases":
#       P(rho) = Lambda + K * (rho - rho_inf)^n      for rho >= rho_inf
#
# K sets how strongly pressure resists compression; n sets how sharply
# that resistance ramps up (n=1 linear/"soft", higher n = stiffer,
# resists more violently as density climbs -- like the pressure laws
# used for real neutron-star matter).

def solve_shell(K, n, M_core, R_core, r_max_factor=50):
    """Integrate hydrostatic equilibrium OUTWARD from the core surface."""
    def rhs(r, y):
        rho, M = y
        if rho <= rho_inf:
            rho = rho_inf
        # dP/drho from the equation of state (chain rule to get drho/dr)
        dPdrho = K * n * max(rho - rho_inf, 1e-30)**(n-1) if n != 1 else K
        if dPdrho <= 0:
            dPdrho = 1e-30
        dPdr = -G * M * rho / r**2
        drhodr = dPdr / dPdrho
        dMdr = 4*np.pi*r**2*rho
        return [drhodr, dMdr]

    def hit_baseline(r, y):
        return y[0] - rho_inf*1.0001
    hit_baseline.terminal = True
    hit_baseline.direction = -1

    r_span = (R_core, R_core*r_max_factor)
    sol = solve_ivp(rhs, r_span, [rho_max_local, M_core], max_step=R_core*0.05,
                     events=hit_baseline, dense_output=True, method='RK45')
    return sol

# Real core numbers already established tonight (C1 from k-calibration)
M_core = 28.118 * Msun
R_core = 30.73 * km  # from the 2x-nuclear-saturation estimate used earlier

rho_max_local = 2 * 2.3e17  # core surface density, continuous with core's own density (2x nuclear sat, same as before)

print("=== GRADIENT-SHELL PROFILE: testing polytropic stiffness index n ===\n")
print(f"Core: M={M_core/Msun:.3f} Msun, R={R_core/km:.2f} km, surface density={rho_max_local:.3e} kg/m^3\n")

fig, axes = plt.subplots(1, 2, figsize=(13,5))
results = {}
for n in [1.0, 1.5, 2.0, 3.0]:
    K = 1e10  # illustrative stiffness constant -- UNDETERMINED free parameter, see note
    sol = solve_shell(K, n, M_core, R_core)
    if sol.t.size > 1:
        r_vals = sol.t
        rho_vals = sol.y[0]
        R_grad_boundary = r_vals[-1]
        results[n] = (r_vals, rho_vals, R_grad_boundary)
        print(f"n={n}: gradient shell extends to R={R_grad_boundary/km:.2f} km "
              f"({R_grad_boundary/R_core:.2f}x core radius) before reaching baseline density")
        axes[0].plot(r_vals/km, rho_vals, label=f'n={n}')
    else:
        print(f"n={n}: integration failed to reach baseline within {50}x core radius")

axes[0].set_xlabel('r (km)')
axes[0].set_ylabel('density (kg/m^3)')
axes[0].set_yscale('log')
axes[0].set_title('rho(r): gradient shell density profile')
axes[0].legend()
axes[0].grid(alpha=0.3)

for n, (r_vals, rho_vals, _) in results.items():
    P_vals = Lambda + 1e10*(rho_vals - rho_inf)**n
    axes[1].plot(r_vals/km, P_vals, label=f'n={n}')
axes[1].set_xlabel('r (km)')
axes[1].set_ylabel('pressure (Pa, illustrative units)')
axes[1].set_yscale('log')
axes[1].set_title('P(r): pressure profile')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('pwc_falsification_output/gradient_shell_profile.png', dpi=130)
print("\nPlot saved.")
print("\n=== HONEST STATUS ===")
print("The two governing equations (hydrostatic equilibrium + mass continuity) are")
print("real, derived, standard physics -- no GR, no assumption beyond basic mechanics.")
print("The equation of state P(rho) = Lambda + K*(rho-1)^n is the genuinely open piece:")
print("K and n are NOT yet derived from anything -- they were picked illustratively")
print("here to show the SHAPE of the family of solutions. Pinning K and n down from")
print("an independent physical principle (or fitting them against the real gradient")
print("mass M_grad already calibrated tonight) is the actual next step to make this")
print("a prediction instead of a demonstration.")
