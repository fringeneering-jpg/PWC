# Comet heat budget vs the untying claim + the survival map (2026-10-08)
import math
c0 = 2.99792458e8
c0sq = c0**2
rho0 = 8.74e-27
u_h = 32.371*rho0*c0sq          # medium heat density at the H0 floor
mp = 1.6726e-27
Gamma = 2.39e-18                 # T7 untying rate per proton (s^-1)

print("== 1. The comet's observed budget ==")
mdot_obs = 1e2                    # kg/s near perihelion (67P-scale; Halley up to 1e4)
L_sub = 2.6e6                     # J/kg sublimation enthalpy
Q_sun = 1e10                      # W solar input on the nucleus (rough, 1e10-1e11)
print(f"observed mass loss ~ {mdot_obs:.0e} kg/s")
print(f"sublimation enthalpy demand: mdot*L_sub = {mdot_obs*L_sub:.1e} W - fits the solar")
print(f"input ({Q_sun:.0e} W). The STANDARD model already has an endothermic phase change.")

print("\n== 2. If the same loss were c0^2-untying ==")
print(f"heat draw needed: mdot*c0^2 = {mdot_obs*c0sq:.1e} W = {mdot_obs*c0sq/Q_sun:.0e}x the")
print(f"solar input. IMPOSSIBLE from the Sun.")

print("\n== 3. What the ambient medium can supply ==")
flux_h = u_h*c0                    # the medium's heat streaming in at c0 (upper bound)
print(f"medium heat flux u_h*c0 = {flux_h:.2f} W/m^2  (H0 = 32.371 c0^2 floor)")
A = 1e8                            # m^2 nucleus surface (upper)
mdot_untie_max = flux_h*A/c0sq
print(f"over A = 1e8 m^2: max full-untying rate = {mdot_untie_max:.1e} kg/s = "
      f"{mdot_untie_max/mdot_obs:.0e}x the observed")
print(f"T7 rate for a 1e13 kg comet: {1e13*Gamma:.1e} kg/s = "
      f"{1e13*Gamma/mdot_obs:.0e}x the observed")

print("\n== 4. The honest reading ==")
print("The comet's ablation is ~100% SHALLOW untying - sublimation, the low rung of the")
print("continuous phase ladder (latent heat 2.6e6 J/kg vs the full c0^2 = 9e16 J/kg). The")
print("deep (c0^2) untying is bounded to 1e-10-1e-12 of the observed flux by the heat budget.")
print("The icy wake = the endothermic signature (both standard sublimation AND the framework's")
print("heat-draw agree on the sign); the tail's expansion = the released volume at the SHALLOW")
print("rate + gas dynamics. The comet is the in-between failing at the shallow end; RBH-1's")
print("slam runs the deep end. The framework's claim survives as the CONTINUOUS ladder, not as")
print("full untying of the tail.")

print("\n== 5. The survival map (the pressure ladder with the three modes) ==")
print("survives if: knot grip (topology, m R c0 = 4 hbar) OR collective well (Jeans/self-pull")
print("> the ambient untying pressure OR Max-P cap at speed (the stagnation column).")
print("comet: below all three - the in-between, shredded from the surface inward.")
print("cloud self-pull check: (4pi/3) G rho R for n=1e2 cm^-3, R=10 pc =")
rho_cl = 1e2*1e6*1.67e-27
R_cl = 10*3.0857e16
print(f"  {4.19*6.6743e-11*rho_cl*R_cl:.2e} m/s^2 vs a0 = 6.6e-11 - clouds hold via the HOST")
print(f"well and Jeans mass, not their own column - consistent with the triad.")

print("\n== 6. Charge reframing (volumetric squeeze, not shell hardening) ==")
g = 16*math.pi**3*(1/137.036)/3.0
f = g**(1/3)
print(f"g = {g:.4f}; if g is a VOLUME ratio of the heat squeeze: f = g^(1/3) = {f:.4f}")
print(f"vs the sealed stretch 20/19 = {20/19:.4f} ({(f/(20/19)-1)*100:+.2f}%) - not clean;")
print(f"the volumetric route needs the knot's heat-expelled volume from the caloric ladder")
print(f"(H(rho) drop at the fold), not a uniform factor. Route named, not closed.")
