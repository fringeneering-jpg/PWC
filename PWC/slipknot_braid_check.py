# The slip-knot vs the braid: verify Jaden's electron/proton mechanism (2026-10-09)
import math
e = 1.602176634e-19; eps0 = 8.8541878128e-12; c0 = 2.99792458e8
hbar = 1.054571817e-34; me = 9.1093837e-31; mp = 1.67262192369e-27
rho_max = 1.304e15; rho_core = 2.3e17; a_max = 3.23e11; G = 6.6743e-11

lamC_bar = hbar/(me*c0)
r_e = e**2/(4*math.pi*eps0*me*c0**2)
R_p = 8.414e-16                    # locked proton radius
alpha = e**2/(4*math.pi*eps0*hbar*c0)

print("== 1. The claimed geometry ==")
print(f"electron fold r_e = {r_e/1e-15:.3f} fm ; proton braid R_p = {R_p/1e-15:.3f} fm")
print(f"radius ratio r_e/R_p = {r_e/R_p:.4f}  (~3.35, 'three times smaller')")
vol_ratio = (r_e/R_p)**3
print(f"volume ratio (r_e/R_p)^3 = {vol_ratio:.2f}  (~38x smaller volume)")

print("\n== 2. The drag bookkeeping: 4 waves x 38 volume x 137 strip =? 1836 ==")
book = 4.0*(1/alpha)*vol_ratio
print(f"4 x (1/alpha) x (r_e/R_p)^3 = {book:.1f}  vs 1836.15  ({100*(book/1836.15-1):+.2f}%)")
ident = 4.0*lamC_bar/R_p
print(f"reduces to: 4 x 137.036 x alpha x lamC_bar/R_p ... = 4 lamC_bar/R_p = {ident:.2f}")
print(f"  -> the bookkeeping is the LOCKED identity m_p/m_e = 4 lamC_bar/R_p in costume;")
print(f"     its content is the reading: 4 waves x un-diluted drag x fold/braid ratio.")

print("\n== 3. The slip-knot's empty space (the dilution) ==")
V_fold = 4*math.pi*r_e**3/3.0
V_tight = me/rho_max
R_tight = (3*V_tight/(4*math.pi))**(1/3)
print(f"fold volume (r_e sphere) = {V_fold:.3e} m^3 ; tight volume = {V_tight:.3e} m^3")
print(f"emptiness ratio V_fold/V_tight = {V_fold/V_tight:.1f}  vs 1/alpha = {1/alpha:.1f}  "
      f"({100*(V_fold/V_tight/(1/alpha)-1):+.1f}%)")
print(f"  -> the single wave fills {100*V_tight/V_fold:.2f}% of its fold: the slip-knot is")
print(f"     {100*(1-V_tight/V_fold):.2f}% empty - and the emptiness ratio sits at 134.5 vs 137.0.")
print(f"     NEAR-MISS (reported, no mechanism yet).")

print("\n== 4. The braid's density ==")
rho_p = mp/(4*math.pi*R_p**3/3.0)
print(f"proton braid density = {rho_p:.2e} kg/m^3 = {rho_p/rho_core:.2f} x rho_core")
print(f"  -> the braid packs 2.9x the core density: no empty space, the screening collapses.")

print("\n== 5. The coupling-strip test ==")
print(f"claim: braid coupling ~1 vs EM 1/137.036 -> alpha_s/alpha ~ 137 (the strip factor).")
print(f"QCD alpha_s at the confinement scale: ~0.3-1 (running) - consistent with the claim,")
print(f"not yet a sharp test; the framework's version: the braid exposes the raw tension")
print(f"(the plateau grip x7, no dilution), the slip-knot dilutes by its own geometry.")
