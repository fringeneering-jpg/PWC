# sparc_ldlhdl_test.py - the LDL/HDL candidate forms vs the RAR on SPARC (2026-10-15)
# The framework's own SPARC loader + the candidate saturation forms, all
# parameter-free. locked = the bulge's share of the pull; shared = the outer
# mass's share (the framework's both-sides loading, proxied by 1 - M(<r)/M_tot).
import numpy as np, sys
sys.path.insert(0, r"C:\Users\jaden\Downloads\PWC-Check\scratch\rot\sparc_x")
from domain_K_rar import read_vizier_tsv, KPC, KMS, UPS_D, UPS_B

D = r"C:\Users\jaden\Downloads\PWC-Check\scratch\rot\sparc_x"
t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name","i","Qual","Vflat","Dist"])
t2 = read_vizier_tsv(f"{D}/vizier_t2.txt", ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
inc  = {n:i for n,i in zip(t1["Name"], t1["i"])}
qual = {n:q for n,q in zip(t1["Name"], t1["Qual"])}

name = np.array(t2["Name"]); R = np.array(t2["Rad"], float); Vo = np.array(t2["Vobs"], float)
eVo = np.array(t2["e_Vobs"], float); Vg = np.array(t2["Vgas"], float); Vd = np.array(t2["Vdisk"], float)
Vb = np.where(np.isnan(np.array(t2["Vbulge"], float)), 0.0, np.array(t2["Vbulge"], float))
Vg = np.where(np.isnan(Vg), 0.0, Vg)
inc_a = np.array([inc.get(n, np.nan) for n in name], float)
qual_a = np.array([qual.get(n, np.nan) for n in name], float)
m = (R > 0) & (Vo > 0) & np.isfinite(eVo) & (eVo/Vo <= 0.10) & (inc_a >= 30.0) & (qual_a <= 2)
R, Vo, Vg, Vd, Vb, name = R[m], Vo[m], Vg[m], Vd[m], Vb[m], name[m]

conv = (KMS**2)/KPC
g_obs = Vo**2 / R * conv
Vbar2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
g_bar = Vbar2 / R * conv
ok = (g_bar > 0) & (g_obs > 0)
g_obs, g_bar, R, Vb, Vbar2, name = g_obs[ok], g_bar[ok], R[ok], Vb[ok], Vbar2[ok], name[ok]

locked = np.clip(UPS_B * Vb*np.abs(Vb) / np.maximum(Vbar2, 1e-30), 0, 1)

# shared: the outer mass's share (1 - enclosed/total), per galaxy
shared = np.zeros_like(g_bar)
for n in set(name):
    sel = name == n
    Mbar = Vbar2[sel] * R[sel]              # proportional to enclosed mass (V^2 R/G ~ M)
    Mtot = Mbar.max()
    shared[sel] = np.clip(1.0 - Mbar/Mtot, 0, 1)

a0 = 6.6110e-11
s  = 0.22650
y  = np.log10(g_obs)

def score(pred):
    r = y - np.log10(pred)
    return float(np.sqrt(np.mean(r**2))), float(np.sqrt(np.mean(np.clip(r, None, 0)**2))), float(np.sqrt(np.mean(np.clip(r, 0, None)**2)))

def rar(gb): return gb/(1.0 - np.exp(-np.sqrt(gb/1.2e-10)))

def candidates(gb, sh, lk):
    boost = 1.0 + s*sh*(1.0-lk)
    x = gb/(18.0*a0)
    A = gb + np.sqrt(a0*gb*(1.0-lk))*boost
    C = gb + np.sqrt(a0*gb/np.sqrt(1.0+x**2))*boost
    D = gb + np.sqrt(a0*gb*(1.0-lk)/np.sqrt(1.0+(gb*(1.0-lk)/(18.0*a0))**2))*boost
    E = gb + np.sqrt(a0*gb)*boost/(1.0+x**2)
    F = gb + np.sqrt(a0*gb*(1.0-lk))*boost/(1.0+x**2)
    return A, C, D, E, F

print("SPARC (175 galaxies, the quality cuts) - RMS dex [total / under / over]:")
r, u, o = score(rar(g_bar))
print(f"  RAR (McGaugh, a0=1.2e-10):    {r:.4f}  [u {u:.4f} / o {o:.4f}]")
for label, f in [("Form A bulge chimney", 0), ("Form C Pythagorean", 1), ("Form D combined", 2), ("Form E LDL/HDL switch", 3), ("Form F D+switch", 4)]:
    A, C, Dd, E, F = candidates(g_bar, shared, locked)
    pred = [A, C, Dd, E, F][f]
    r, u, o = score(pred)
    print(f"  {label}: {r:.4f}  [u {u:.4f} / o {o:.4f}]")
