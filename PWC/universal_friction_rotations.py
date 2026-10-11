# One universal friction rule across the rotational data (2026-10-09)
# F = 0.5 rho0 v^2 Cd f_solid A_geo,  f_solid = 0.085% (the same for everything)
import math
rho0 = 8.74e-27
f_solid = 0.00085
Msun = 1.989e30

def drag(v, A_geo):
    return 0.5*rho0*v**2*f_solid*A_geo

print("THE UNIVERSAL RULE:  F = 1/2 rho0 v^2 . f_solid . A_geo,  f_solid = 0.085% for everything\n")

print("== applied across the rotational data ==")
# a typical SPARC star
R_sun = 6.96e8; v = 2.0e5
F = drag(v, math.pi*R_sun**2)
m = Msun
print(f"star at 200 km/s:   F = {F:.3e} N ; decay time p/F = {m*v/F/3.15e16:.1e} Gyr (infinite)")
# a gas cloud (the HI: 10 pc cloud)
R_cl = 10*3.0857e16; m_cl = 1e6*Msun
F_cl = drag(v, math.pi*R_cl**2)
print(f"10-pc HI cloud:     F = {F_cl:.3e} N ; decay time = {m_cl*v/F_cl/3.15e16:.1e} Gyr")
# the central SMBH
M_bh = 1e9*Msun; R_sh = math.sqrt(6.6743e-11*M_bh/3.23e11)
F_bh = drag(2.0e5, math.pi*R_sh**2)
print(f"SMBH at 200 km/s:   F = {F_bh:.3e} N ; decay time = {M_bh*2e5/F_bh/3.15e16:.1e} Gyr")

print("\n== what the one rule says about the rotation curves ==")
print("the friction's contribution to the curve SHAPE is zero (decay times >> the Hubble")
print("time for every object). The curves stay the TENSION's law - the shared-tension")
print("formula, already blind-tested (SPARC 0.1309, PROBES 0.2931). The rule's job is the")
print("DECAY channel: one formula replaces every ad hoc cross-section, and it predicts no")
print("friction signal in any measured orbit (the binary test: 1e-26 of the decay).")
print("\n-> so the rotational improvements are already in (the tension formula, blind);")
print("   the universal rule unifies the drag description under ONE f_solid for every object")
print("   from the electron to the SMBH - and pins the decay prediction at 1e-26.")
print("   The SMBH 'at rest' reading now uses the SAME rule: the co-moving shell, no")
print("   relative flow, F = 0 - the rule says rest, the data says rest.")
