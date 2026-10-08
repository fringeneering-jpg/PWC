# The surface-area holding law (Jaden's ruling, 2026-10-08): thin skin, 1/r^2 dilution
import math
G = 6.6743e-11
rho_max = 1.304e15
rho_core = 2.3e17
a_max = 3.23e11
Msun = 1.989e30
Sigma_k = 8.48e20          # the k-rule held column (repo)

print("== 1. The inverse square = fixed tension diluted over 4 pi r^2 ==")
print("grip(r) = Grip_total / (4 pi r^2): a fixed amount of tension spread over the expanding")
print("sphere. The pull per unit area falls exactly as 1/r^2 - the geometric origin of the")
print("inverse-square law, no metric needed.")

print("\n== 2. The thin skin = the surface capacity ==")
t_skin = Sigma_k/rho_max
print(f"skin thickness = Sigma_k / rho_max = {Sigma_k:.2e} / {rho_max:.2e} = {t_skin/1e3:.0f} km")
print(f"(the session log's k-rule 20-hole run: absolute thickness 70 km -> a constant ~640 km;")
print(f" edge/core 4.69 -> 1.01. Small core: concentrated grip, proportionally thicker skin;")
print(f" supermassive core: grip diluted over the huge surface, razor-thin skin. RULED.)")

print("\n== 3. The r^-4 thick envelope is dead ==")
print("threshold-envelope tail was 35.6 Msun (rho ~ r^-4); the surface-area law replaces it:")
print("M_med = Sigma * 4 pi R_c^2  -  held mass bound strictly to the core's surface area.")
print(f"k-rule check: Sigma_k/(rho_max*t_skin) = {Sigma_k/(rho_max*t_skin):.4f} (identity by")
print(f"construction; the k = 0.868899 column is the fitted value).")

print("\n== 4. The sheet law (candidate for Sigma) vs the fitted column ==")
Sigma_sheet = a_max/(2.0*math.pi*G)      # flat-sheet self-pull balance: 2 pi G Sigma = a_max
print(f"candidate: 2 pi G Sigma = a_max -> Sigma = {Sigma_sheet:.3e} kg/m^2")
print(f"fitted k-rule Sigma = {Sigma_k:.3e} kg/m^2 -> residual {(Sigma_k/Sigma_sheet-1)*100:+.1f}%")
print(f"(the one open numerical thread between the surface-area law and the fitted column).")

print("\n== 5. Consistency with the stagnation scale ==")
col_ball = 3.0*a_max/(4.0*math.pi*G)
R_star = col_ball/rho_max
print(f"stagnation boundary (ball self-hold): R* = {R_star/1e3:.0f} km > skin {t_skin/1e3:.0f} km")
print(f"-> the thin skin is SUB-stagnation: it never self-holds, it is held by the core's grip")
print(f"through the 1/r^2 dilution - exactly the surface-area law. The ball column and the")
print(f"sheet column differ by 3/2 (geometry); the skin is the sheet regime.")
