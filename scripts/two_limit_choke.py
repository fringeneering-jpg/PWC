# two_limit_choke.py - the controlled-burn derivation, written and tested (2026-10-15)
# The untying's rate is the MIN of two coupled limits:
#   L1 - heat throughput:  the drag-steered flux can deliver heat at at most
#        the acoustic crossing rate; every kg untied owes L = c0^2.
#   L2 - volume accommodation: each untied kg releases ~1/rho_max of volume;
#        the region expands only as fast as the pressure opposition relaxes.
# The unrestricted sqrt(a0.g) overshoot is the un-choked process; the choke's
# the rate limiter, and the radial force follows the restricted rate.
import numpy as np, sys
sys.path.insert(0, r"C:\Users\jaden\Downloads\PWC-Check\scratch\rot\sparc_x")
from domain_K_rar import read_vizier_tsv, KPC, KMS, UPS_D, UPS_B
D = r"C:\Users\jaden\Downloads\PWC-Check\scratch\rot\sparc_x"
t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name","i","Qual","Vflat","Dist"])
t2 = read_vizier_tsv(f"{D}/vizier_t2.txt", ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
inc  = {n:i for n,i in zip(t1["Name"], t1["i"])}; qual = {n:q for n,q in zip(t1["Name"], t1["Qual"])}
name = np.array(t2["Name"]); R = np.array(t2["Rad"], float); Vo = np.array(t2["Vobs"], float)
eVo = np.array(t2["e_Vobs"], float); Vg = np.array(t2["Vgas"], float); Vd = np.array(t2["Vdisk"], float)
Vb = np.where(np.isnan(np.array(t2["Vbulge"], float)), 0.0, np.array(t2["Vbulge"], float)); Vg = np.where(np.isnan(Vg), 0.0, Vg)
inc_a = np.array([inc.get(n, np.nan) for n in name], float); qual_a = np.array([qual.get(n, np.nan) for n in name], float)
m = (R > 0) & (Vo > 0) & np.isfinite(eVo) & (eVo/Vo <= 0.10) & (inc_a >= 30.0) & (qual_a <= 2)
R, Vo, Vg, Vd, Vb, name = R[m], Vo[m], Vg[m], Vd[m], Vb[m], name[m]
conv = (KMS**2)/KPC; g_obs = Vo**2/R*conv
Vbar2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb); g_bar = Vbar2/R*conv
ok = (g_bar > 0) & (g_obs > 0); g_obs, g_bar, R, Vb, Vbar2, name = g_obs[ok], g_bar[ok], R[ok], Vb[ok], Vbar2[ok], name[ok]
locked = np.clip(UPS_B*Vb*np.abs(Vb)/np.maximum(Vbar2,1e-30), 0, 1)
shared = np.zeros_like(g_bar)
for n in set(name):
    sel = name == n; Mb = Vbar2[sel]*R[sel]; shared[sel] = np.clip(1.0 - Mb/Mb.max(), 0, 1)
a0 = 6.6110e-11; s = 0.22650
y = np.log10(g_obs)
def rms(pred): return float(np.sqrt(np.mean((y - np.log10(pred))**2)))
def rar(gb): return gb/(1.0-np.exp(-np.sqrt(gb/1.2e-10)))

print("THE TWO-LIMIT CHOKE, DERIVED STRUCTURE:")
print("  L1 (heat throughput):  untying rate <= (drag-steered flux) / L, L = c0^2")
print("      the flux caps at the acoustic crossing: m_dot_max = rho_ambient . c0 . A")
print("      ->  Gamma_1(g) = Gamma_0 . (1 + g/g_T)^-1       (the series supply)")
print("  L2 (volume accommodation): the expansion's rate <= the pressure relaxation")
print("      ->  Gamma_2(g) = Gamma_0 . (1 + (g/g_V)^2)^-1/2 (the quadrature loading)")
print("  the coupled rate: Gamma = Gamma_0 / (1 + x + x^2),  x = g_bar/g_c")
print("      (the two limits in series - the throughput AND the volume both gate)")
print("  g_c = 18.a0 (the planar budget, locked). NO fitted constants.")
g_c = 18.0*a0
x = g_bar/g_c
boost = 1.0 + s*shared*(1.0-locked)
print()
print("SPARC rms (dex), zero fitted parameters:")
print(f"  RAR (fitted a0):            {rms(rar(g_bar)):.4f}")
print(f"  unrestricted sqrt(a0 g):    {rms(g_bar + np.sqrt(a0*g_bar)*boost):.4f}")
fL1 = 1.0/(1.0+x)
fL2 = 1.0/np.sqrt(1.0+x**2)
f2  = 1.0/(1.0+x+x**2)
f3  = fL1*fL2
for lab, f in [("L1 only (throughput)", fL1), ("L2 only (volume)", fL2),
               ("coupled L1*L2", f3), ("coupled series 1/(1+x+x^2)", f2)]:
    print(f"  {lab}: {rms(g_bar + np.sqrt(a0*g_bar)*boost*f):.4f}")
