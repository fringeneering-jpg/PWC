# The chart backwards: the bubble's aspect = the medium's own C vs the join's C (2026-10-12)
import math
c0 = 2.99792458e8
Y_bow = 5.93e26
rho_cap = 2*Y_bow/c0**2          # the speed-cap density (the chart's knee)
aspect = 4.528

print("the medium against a medium of itself: C(ambient) = c0 (it IS the medium, no limit)")
print(f"the aspect {aspect} = c0 / C(join)  ->  the join's C = c0/{aspect} = {c0/aspect/1e3:,.0f} km/s\n")
v_join = c0/aspect
rho_join = 2*Y_bow/v_join**2
print(f"the chart inverted: rho_join = 2 Y_bow / v_join^2 = {rho_join:.4e} kg/m^3")
print(f"= {rho_join/rho_cap:.2f} x the speed-cap density {rho_cap:.3e}")
print(f"\nthe identity:  aspect = sqrt(rho_join / rho_cap)  =  sqrt({rho_join/rho_cap:.3f}) = {math.sqrt(rho_join/rho_cap):.4f}")
print(f"   R_wall / R_CMB = sqrt(rho_join / rho_cap) = c0 / C(rho_join)")
print(f"\n-> the bubble's aspect is the square root of the JOIN's density over the speed-cap")
print(f"   density. The join (the CMB - where the untying matter meets the medium) has a")
print(f"   structural density {rho_join:.3e} kg/m^3 = 20.5x the cap threshold.")
print(f"   The prediction: the untying join's density is {rho_join:.3e} - and the wall's")
print(f"   distance is the aspect x the join's. The chart reads the universe's shape back.")
print(f"   (honest note: no locked framework density equals {rho_join:.3e} yet - the join's")
print(f"   density is now a named prediction, checkable against the CMB's own structure.)")
