# Verify the numbers in scratch/demand_function_draft.md (arithmetic on stated numbers)
c0 = 2.998e8
c0sq = c0**2
rho_max = 1.304e15
Msun = 1.989e30

print("P_max = rho_max*c0^2 =", f"{rho_max*c0sq:.4e}", "Pa")
print("two-wall spike dP = rho_max*c0*c0 = P_max -> equal:",
      abs(rho_max*c0*c0 - rho_max*c0sq) < 1e-20)

# RBH-1 flash route
flash_W = 1.9e34            # 1.9e41 erg/s
mdot_light = flash_W / c0sq
print("mdot_light =", f"{mdot_light:.3e}", "kg/s")
years73 = 73e6 * 365.25 * 86400
print("73 Myr =", f"{years73:.3e}", "s")
M_light_kg = mdot_light * years73
M_light_Msun = M_light_kg / Msun
print("M_light =", f"{M_light_Msun:.1f}", "Msun (sec.8 says ~245)")

# star route
for M_stars in (1e6, 1e7):
    mdot = M_stars * Msun / years73
    Vdot = mdot / rho_max
    print(f"stars {M_stars:.0e} Msun: mdot={mdot:.3e} kg/s, Vdot={Vdot:.3e} m^3/s, "
          f"cube side={Vdot**(1/3):.1f} m, light fraction={M_light_Msun/M_stars:.3e}")

# water sanity
dw = 14.1
cw, rhow, Lv = 1500.0, 1000.0, 2.257e6
dPw = rhow * cw * dw
print("water dP =", f"{dPw:.2e}", "Pa; m/V =", f"{dPw/Lv:.2f}", "kg/m^3 =",
      f"{100*dPw/Lv/1000:.2f}", "% of the m^3")

# gamma per unit heat (null result check)
gamma_gw = 3.36e31
print("gamma/(rho_max*c0^2) =", f"{gamma_gw/(rho_max*c0sq):.4f}", "m")
print("vs 21 cm:", f"{0.2114:.4f}", "m, ratio", f"{gamma_gw/(rho_max*c0sq)/0.2114:.3f}")
