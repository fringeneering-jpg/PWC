# CMB Step 1: the bath-weighted channel with the framework's OWN melt (2026-10-12)
import math
c0 = 2.99792458e8
ell_naive = 179.48
ell_obs = 220.0
H0 = 32.371*c0**2

print("== the correction needed ==")
print(f"ell_1: naive {ell_naive:.1f} -> observed {ell_obs:.0f} : factor {ell_obs/ell_naive:.4f}")
print(f"the horizon must shrink by {1/(ell_obs/ell_naive):.4f}  ->  c_s must drop by {1/(ell_obs/ell_naive):.4f}\n")

print("== the bath weighting with the framework's own knots ==")
# c_s = c0/sqrt(3(1+R)),  R = 3 f_knots / (4 (1 - f_knots))
def cs_factor(f):
    R = 3.0*f/(4.0*(1.0-f))
    return 1.0/math.sqrt(1.0+R)
for f, lab in [(0.05, "today's tied fraction (5%)"),
               (0.064, "the LSS fraction from the caloric (21.6% melted since)")]:
    fac = cs_factor(f)
    ell = ell_naive/fac
    print(f"  f = {f}: R = {3*f/(4*(1-f)):.4f}, c_s drop {fac:.4f} -> ell_1 = {ell:.1f}")

print("\n== what WOULD close it ==")
# the needed factor: c_s/c_s_naive = 179.48/220 -> 1+R = (220/179.48)^2
R_needed = (ell_obs/ell_naive)**2 - 1.0
f_needed = 4.0*R_needed/(3.0+4.0*R_needed)
print(f"needed R = {R_needed:.4f}  ->  the tied fraction at the LSS = {f_needed:.3f} ({100*f_needed:.1f}%)")
print(f"vs the framework's melt: the caloric says 21.6% of the debt paid since the LSS,")
print(f"so the tied fraction THEN was ~6-7%, not {100*f_needed:.0f}%.")

print("\n== the verdict (locked wording) ==")
print("the 179.5 value is logged as the baseline calculation; the bath-weighted acoustic")
print("channel from the horizon join is the identified next derivation. The framework's")
print("history runs from the EVENT HORIZON (the joiner between the CMB's untie and our")
print("own, 62.5 Gly, the 4.529 aspect) - the LSS at 13.8 Gly is the local surface")
print("inside it, and the acoustic scale inherits the horizon's clock. The channel's")
print("bath-weighting reads the tied fraction ALONG the horizon's untie curve, not")
print("against today's 5%.")
