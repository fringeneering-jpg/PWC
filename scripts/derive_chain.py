#!/usr/bin/env python3
"""
derive_chain.py -- PWC.md Section 0 (Steps 1-7) reproduced from inputs, in one place.

Nothing here is a new model. Every number is recomputed from the inputs below and
checked against the value PWC.md states. Run:  python derive_chain.py

Inputs (all stated in PWC.md):
  rho_core = 2.3e17 kg/m^3     Step 2   (constant through a merger)
  k        = 0.8524572447      Section 8, core/gradient split (GWTC-4 rerun: 0.868899)
  cores    = 28.118, 22.255 Msun   GW150914 (discovery-paper cores; final core 50.373)
  M_final  = 62 Msun           GW150914
  shell    = core surface -> 159.6 km, holding 10.87 Msun          Step 5
  a0       = 7.55e-11 m/s^2    Step 7

Everything else is derived below.
"""
import math

G = 6.674e-11
C0 = 2.99792458e8
MSUN = 1.989e30
HBAR = 1.054571817e-34
KB = 1.380649e-23

RHO_CORE = 2.3e17
K_RULE = 0.8524572447
CORE1, CORE2 = 28.118, 22.255          # Msun
M_FINAL = 62.0                          # Msun
A0 = 7.55e-11

checks = []


def check(name, got, stated, tol):
    ok = abs(got - stated) / abs(stated) <= tol
    checks.append(ok)
    print(f"  {'OK ' if ok else 'BAD'} {name:<52} {got:>12.4g}   (PWC.md: {stated:g}, tol {tol:.1%})")


def core_radius(m_msun):
    return (3 * m_msun * MSUN / (4 * math.pi * RHO_CORE)) ** (1 / 3)


print("STEP 1  Sonic choke -> Hawking temperature (zero free parameters)")
for m in (1.0, 62.0, 4.3e6):
    t = HBAR * C0**3 / (8 * math.pi * G * m * MSUN * KB)
    print(f"  M = {m:>8g} Msun   T_H = {t:.4e} K")

print("\nSTEP 2  Merger = two neutron-density cores; mass and volume add, density constant")
core_f = CORE1 + CORE2
print(f"  cores {CORE1} + {CORE2} = {core_f:.3f} Msun (conserved)")
v_sum = sum(core_radius(c) ** 3 for c in (CORE1, CORE2))
print(f"  V1 + V2 = {(4 / 3) * math.pi * v_sum:.4e} m^3   V_f = {(4 / 3) * math.pi * core_radius(core_f) ** 3:.4e} m^3  (equal at constant rho_core)")

print("\nSTEP 3  Medium held around each core (M^(1/2) reach vs M^(1/3) core)  -- k-rule")
held_before = K_RULE * (CORE1 ** (2 / 3) + CORE2 ** (2 / 3))
held_after = K_RULE * core_f ** (2 / 3)
print(f"  held before (two shells): {held_before:.3f} Msun")
print(f"  held after  (one shell):  {held_after:.3f} Msun    (M_final - core = {M_FINAL - core_f:.3f})")

print("\nSTEP 5  GW150914 numbers")
R_core = core_radius(51.0)
R_out = 159.6e3
shell_m = 10.87 * MSUN
V = (4 / 3) * math.pi * (R_out**3 - R_core**3)
rho_max = shell_m / V
g_yield = G * 62.0 * MSUN / R_out**2
P = rho_max * g_yield
gamma = P * R_out / 2
check("released medium (Msun)", held_before - held_after, 3.0, 0.03)
check("core radius of 51 Msun (km)", R_core / 1e3, 47.3, 0.005)
check("shell volume (m^3)", V, 1.658e16, 0.005)
check("rho_max (kg/m^3)", rho_max, 1.304e15, 0.005)
check("yield  G*M_total/r^2 at 159.6 km (N/kg)", g_yield, 3.23e11, 0.005)
check("boundary pressure rho_max*g (Pa)", P, 4.21e26, 0.01)
check("surface tension P*R/2 (N/m)", gamma, 3.36e31, 0.01)

print("\nSTEP 4/5  Reach r_y = sqrt(G*M_total/yield): shell grows with core mass at fixed rho_max")
print("  yield is calibrated on GW150914, so its own row is circular; GW151226 is the independent check.")
print("  Core comes from the published final mass through the k-rule  M_f = C + k*C^(2/3)  (no back-solving).")


def core_from_final(m_final):
    lo, hi = 1.0, m_final
    for _ in range(80):
        mid = (lo + hi) / 2
        if mid + K_RULE * mid ** (2 / 3) > m_final:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


for name, m_f, stated_core, stated_reach in (("GW151226 (M_f 20.8)", 20.8, 33.0, 94.0), ("GW150914 (M_f 62)", 62.0, 47.3, 160.0)):
    c = core_from_final(m_f)
    r_core = core_radius(c) / 1e3
    r_y = math.sqrt(G * m_f * MSUN / g_yield) / 1e3
    print(f"  {name}: core {c:5.2f} Msun, radius {r_core:5.1f} km, reach {r_y:6.1f} km, shell {r_y - r_core:6.1f} km")
    check(f"  {name} core radius (km)", r_core, stated_core, 0.05)
    check(f"  {name} reach (km)", r_y, stated_reach, 0.05)

print("\nSTEP 7  Holding threshold a0 and the sqrt(a0*g_bar) extension")
for m in (1e10, 1e11):
    r_t = math.sqrt(G * m * MSUN / A0) / 3.0857e19
    print(f"  M_bar = {m:.0e} Msun: r_t = sqrt(GM/a0) = {r_t:.1f} kpc;  g = a0*r_t/r = sqrt(a0*g_bar)")
print(f"  a0 / yield = {A0 / g_yield:.3e}   (galaxy-scale holding threshold vs the rho_max threshold)")

print(f"\n{sum(checks)}/{len(checks)} stated numbers reproduced.")
raise SystemExit(0 if all(checks) else 1)
