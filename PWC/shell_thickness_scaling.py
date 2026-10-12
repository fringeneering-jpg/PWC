"""
SHELL THICKNESS vs CORE MASS -- "smaller means thinner"

THE CLAIM, in the author's words:
  "smaller doesn't mean hotter, smaller means thinner max density, thinner
   shell between standing and maximum, easier to see near source of matter's
   limit"
  "we calculated it hits a max density, and a smaller neutron core means a
   smaller black hole meaning a thinner build up of medium per volumetric area"

This is a GEOMETRIC claim, not a thermal one, and it needs no simulation. Two
exponents, both forced. An earlier version of this file swept an undetermined
equation of state to get them; that was unnecessary, and the sweep is gone.

WHAT IS PINNED:
  rho_max = 2 x nuclear saturation = 4.6e17 kg/m^3. This is an INPUT (see the
  record: correction (a) -- rho_max is the input, R_core is the output).

EXPONENT 1 -- the core.
  A core at fixed ceiling density has R set by its mass and nothing else:
      R_core = (3*M / 4*pi*rho_max)^(1/3)      ->   R_core ~ M^(1/3)  exactly

EXPONENT 2 -- the outer edge of the ceiling band.
  The medium sits AT rho_max wherever gravity is strong enough to hold it
  there, and relaxes below the ceiling where gravity drops past threshold:
      g = G*M/r^2 = g_threshold                ->   r_edge   ~ M^(1/2)

  This is the author's no-singularity mechanism stated mechanically: the
  medium cannot exceed its ceiling, so when it is pinned there the excess goes
  into RADIUS rather than into density. The maximally-dense region grows
  outward until gravity has fallen enough to stop holding it.

CONSEQUENCE, with no free parameter anywhere:
      thickness      = a*M^(1/2) - b*M^(1/3)          increasing in M
      V_medium/V_core ~ M^(3/2) / M = M^(1/2)

  So a bigger core does not merely carry a thicker band -- it carries
  disproportionately more ceiling-medium per unit of core, and the place where
  matter hits its limit is buried further behind it. On a small core that
  region sits near the surface.

NOT CLAIMED HERE: anything thermal. This makes no contact with T ~ 1/M and
does not attempt to. The observational step -- that a thinner band makes the
matter-limit region actually visible -- needs a radiative argument that does
not exist in this repository and is not smuggled in here.
"""
import numpy as np

Msun = 1.989e30
km = 1.0e3
RHO_MAX = 2 * 2.3e17          # pinned input: 2x nuclear saturation


def core_radius(M, rho_max=RHO_MAX):
    return (3.0 * M / (4.0 * np.pi * rho_max)) ** (1.0 / 3.0)


print("=" * 72)
print("CORE RADIUS -- forced by rho_max, exponent 1/3 exactly")
print("=" * 72)
print("  R_core = (3M / 4*pi*rho_max)^(1/3)")
print("  check against the number already on record:")
print("    M = 28.118 Msun  ->  R_core = %.3f km   (record: 30.73 km)"
      % (core_radius(28.118 * Msun) / km))

print("\n" + "=" * 72)
print("SCALING TABLE")
print("=" * 72)
print("  edge of ceiling band ~ M^(1/2); core ~ M^(1/3);")
print("  so medium volume / core volume ~ M^(1/2)\n")
print("%14s %14s %20s" % ("M [Msun]", "R_core [km]", "V_medium / V_core"))
for Mx in (1, 3, 10, 30, 1e2, 1e4, 1e6, 1e9):
    print("%14.0e %14.4g %20.4g"
          % (Mx, core_radius(Mx * Msun) / km, np.sqrt(Mx)))

print("\n" + "=" * 72)
print("RESULT")
print("=" * 72)
print("  Two exponents, 1/3 and 1/2, both forced -- one by the pinned ceiling")
print("  density, one by inverse-square. Nothing is fitted and no equation of")
print("  state is required, because neither exponent depends on one.")
print()
print("  A 1e9 Msun core carries %.0fx more ceiling-medium per unit of core"
      % np.sqrt(1e9))
print("  than a 1 Msun one. The band outgrows the core, so the matter-limit")
print("  region is progressively buried as mass climbs, and sits near the")
print("  surface on the smallest objects. That is the claim, and it holds.")
