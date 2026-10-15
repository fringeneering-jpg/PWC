# The checker's algebra vs the framework's own melt: the R_lss fork (2026-10-12)
import math
ell_free = 179.5
ell_obs = 220.0

print("== 1. Verify the checker's closed form ==")
def R_from(ell1):
    target = ell1/ell_free
    # solve R/(2(sqrt(1+R)-1)) = target
    lo, hi = 1e-6, 10.0
    for _ in range(80):
        mid = (lo+hi)/2
        v = mid/(2*(math.sqrt(1+mid)-1))
        if v < target: lo = mid
        else: hi = mid
    return (lo+hi)/2
R_lss = R_from(ell_obs)
print(f"required R_lss = {R_lss:.4f}  (the checker's 1.106)")
print(f"-> the knots' fraction at the LSS: f = R/(R + 4/3) = {R_lss/(R_lss+4.0/3.0):.4f} ({100*R_lss/(R_lss+4.0/3.0):.1f}%)")
print()

print("== 2. The framework's own melt history ==")
H0 = 32.371
H_lss = H0 - math.log(1101.0)     # the caloric: H(z) = H0 - ln(1+z)
paid = 1.0 - H_lss/H0
f_lss_caloric = 0.05/(1.0-paid)
print(f"the caloric's repayment since the LSS: {100*paid:.1f}%")
print(f"-> the tied fraction at the LSS = 5%/(1-{100*paid:.0f}%) = {100*f_lss_caloric:.1f}%")
R_cal = 3.0*f_lss_caloric/(4.0*(1.0-f_lss_caloric))
ell_cal = ell_free*(R_cal/(2*(math.sqrt(1+R_cal)-1)))
print(f"R from the framework's history = {R_cal:.4f}  ->  ell_1 = {ell_cal:.1f}")
print()

print("== 3. The fork, stated honestly ==")
print(f"the peak's position demands R_lss = {R_lss:.3f} (a {100*R_lss/(R_lss+4/3):.0f}% tied")
print(f"fraction), while the framework's caloric history gives R = {R_cal:.3f} ({100*f_lss_caloric:.1f}%) -")
print("a factor ~20 in the drag ratio. The two resolutions:")
print("(a) the melt ran MUCH faster since the LSS (92% of the knots untied in the last")
print("    13.8 Gyr) - the caloric's 21.6% would need re-reading;")
print("(b) the knots drag STRONGER than their mass: the fold's grip (x7) and the hold")
print("    make each tied kg load the channel like ~20 kg of free medium - the")
print("    framework's own coupling law, quantified: the effective drag per knot.")
print("Both are framework-internal questions. The algebra is verified; the fork's")
print("numbers are on the table; neither resolution is chosen without a derivation.")
