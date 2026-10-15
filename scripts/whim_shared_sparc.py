# whim_shared_sparc.py - the WHIM's surrounding load, from the 2MRS, then the choke (2026-10-15)
# The deep field was missing the ENVIRONMENT: the web's heat pressing on the
# galaxy's reach. The 2MRS catalogue supplies the surroundings; the framework's
# both-sides loading gives each galaxy its WHIM shared floor.
import numpy as np, sys
sys.path.insert(0, r"C:\Users\jaden\Downloads\PWC-Check\scratch\rot\sparc_x")
from domain_K_rar import read_vizier_tsv, KPC, KMS, UPS_D, UPS_B
D = r"C:\Users\jaden\Downloads\PWC-Check\scratch\rot\sparc_x"

# --- the SPARC galaxies with coordinates ---
t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name","i","Qual","Vflat","Dist","_RA","_DE"])
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

# --- the WHIM's surrounding load from the 2MRS ---
def parse_2mrs(path):
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8", errors="replace")]
    hdr_i = None
    for i, l in enumerate(lines):
        if l.startswith("RAJ2000"): hdr_i = i; break
    names = lines[hdr_i].split("\t")
    idx = {c: names.index(c) for c in ["RAJ2000","DEJ2000","cz"]}
    ra, de, cz = [], [], []
    for l in lines[hdr_i+1:]:
        if not l.strip() or l.startswith("#"): continue
        f = l.split("\t")
        if len(f) < len(names): continue
        try:
            v = f[idx["cz"]].strip()
            if v in ("","---"): continue
            ra.append(float(f[idx["RAJ2000"]].strip())); de.append(float(f[idx["DEJ2000"]].strip())); cz.append(float(v))
        except ValueError: continue
    return np.array(ra), np.array(de), np.array(cz)
ra2, de2, cz2 = parse_2mrs(f"{D}/2mrs.txt")
H0k = 73.0
d2 = cz2 / H0k   # Mpc

gal_names = sorted(set(name))
ra1 = np.array([t1["_RA"][t1["Name"].index(n)] if n in t1["Name"] else np.nan for n in gal_names], float)
de1 = np.array([t1["_DE"][t1["Name"].index(n)] if n in t1["Name"] else np.nan for n in gal_names], float)
d1  = np.array([t1["Dist"][t1["Name"].index(n)] if n in t1["Name"] else np.nan for n in gal_names], float)
print(f"SPARC galaxies with coords: {np.isfinite(ra1).sum()}/{len(gal_names)};  2MRS entries: {len(ra2)}")

# angular separation (radians)
ra1r, de1r = np.deg2rad(ra1), np.deg2rad(de1)
ra2r, de2r = np.deg2rad(ra2), np.deg2rad(de2)
shared_env = {}
APERT = 5.0   # Mpc, the web's loading scale
for k, n in enumerate(gal_names):
    if not (np.isfinite(ra1[k]) and np.isfinite(d1[k])): shared_env[n] = 0.0; continue
    ca = np.sin(de1r[k])*np.sin(de2r) + np.cos(de1r[k])*np.cos(de2r)*np.cos(ra1r[k]-ra2r)
    ca = np.clip(ca, -1, 1); sep = np.arccos(ca) * d1[k]   # projected Mpc at the galaxy's distance
    nn = int(((sep < APERT) & (np.abs(d2 - d1[k]) < 6.0)).sum())
    shared_env[n] = nn
vals = np.array([shared_env[n] for n in gal_names], float)
n_scale = 2.0*np.median(vals[vals > 0]) if (vals > 0).any() else 1.0
shared_env = {n: min(1.0, v/n_scale) for n, v in zip(gal_names, vals)}
print(f"env shared: median neighbour count {np.median(vals[vals>0]):.0f}, scale {n_scale:.0f}, "
      f"range of shared_env {min(shared_env.values()):.2f}-{max(shared_env.values()):.2f}")

# --- merge: the WHIM floor + the galaxy's own outer mass ---
shared = np.zeros_like(g_bar)
for n in set(name):
    sel = name == n
    Mb = Vbar2[sel]*R[sel]
    own = np.clip(1.0 - Mb/Mb.max(), 0, 1)
    shared[sel] = np.clip(own + shared_env.get(n, 0.0)*(1.0-own), 0, 1)

# --- the choke, with the WHIM ---
a0 = 6.6110e-11; s = 0.22650
y = np.log10(g_obs)
def rms(pred): return float(np.sqrt(np.mean((y - np.log10(pred))**2)))
def rar(gb): return gb/(1.0-np.exp(-np.sqrt(gb/1.2e-10)))
x = g_bar/(18.0*a0); boost = 1.0 + s*shared*(1.0-locked)
f_coupled = 1.0/(1.0+x+x**2)
print()
print("SPARC rms (dex):")
print(f"  RAR (fitted a0):                    {rms(rar(g_bar)):.4f}")
print(f"  two-limit choke, NO WHIM:           {rms(g_bar + np.sqrt(a0*g_bar)*(1.0+s*np.clip(1.0-np.zeros_like(g_bar),0,1)*(1.0-locked))*f_coupled):.4f}")
print(f"  two-limit choke + WHIM shared:      {rms(g_bar + np.sqrt(a0*g_bar)*boost*f_coupled):.4f}")
# the deep-field check
rat = g_bar/a0; sel = (rat < 0.2)
res_w = np.log10((g_bar + np.sqrt(a0*g_bar)*boost*f_coupled)/g_obs)
print(f"  deep-field mean residual (with WHIM): {res_w[sel].mean():+.4f}  (was -0.0295)")
