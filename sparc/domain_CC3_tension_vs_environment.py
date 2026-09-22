"""
DOMAIN CC3 -- independent, falsifiable check on the lambda sign story from
domain_CC2: if steep-gradient regions are under tension specifically because
they're contested by MULTIPLE nearby masses (the "competing pulls" picture),
then galaxies sitting in denser real environments (more massive neighbours)
should show a MORE NEGATIVE lambda than isolated galaxies. If lambda doesn't
differ between isolated and grouped galaxies, the "competing external masses"
explanation is not supported by this test, and that gets reported plainly.

Reuses domain_K_environment.py's real, confound-controlled 2MRS neighbour
count (volume-limited, same M_K cut, same distance-confound check) rather
than inventing a new environment measure.
"""
import numpy as np, json
from scipy.optimize import minimize, minimize_scalar
from scipy import stats

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
KMS = 1.0e3
UPS_D, UPS_B = 0.5, 0.7
H0 = 70.0
MK_LIM = -22.0
DV_WIN = 1000.0

def read_tsv(path, cols):
    lines=[l.rstrip("\n") for l in open(path,encoding="utf-8",errors="replace")]
    hdr=next(i for i,l in enumerate(lines) if not l.startswith("#") and "\t" in l
             and any(c in l.split("\t") for c in cols))
    names=lines[hdr].split("\t")
    dash=max(i for i in range(hdr+1,hdr+6)
             if set(lines[i].replace("\t","").strip())<=set("- "))
    idx={c:names.index(c) for c in cols}
    out={c:[] for c in cols}
    for l in lines[dash+1:]:
        if not l.strip() or l.startswith("#"): continue
        f=l.split("\t")
        if len(f)<len(names): continue
        try:
            for c in cols:
                v=f[idx[c]].strip()
                out[c].append(v if c=="Name" else (float(v) if v not in("","---") else np.nan))
        except ValueError: continue
    return out

# --- rotation curve data + real per-galaxy gradient (same as domain_CC2) ---
def read_vizier_tsv(path, cols):
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8", errors="replace")]
    hdr_i = None
    for i, l in enumerate(lines):
        if l.startswith("#") or not l.strip(): continue
        if "\t" in l and "recno" in l: hdr_i = i; break
    names = lines[hdr_i].split("\t")
    dash_i = None
    for i in range(hdr_i+1, min(hdr_i+6, len(lines))):
        if set(lines[i].replace("\t","").strip()) <= set("- "): dash_i = i
    idx = {c: names.index(c) for c in cols}
    out = {c: [] for c in cols}
    for l in lines[dash_i+1:]:
        if not l.strip() or l.startswith("#"): continue
        f = l.split("\t")
        if len(f) < len(names): continue
        try:
            for c in cols:
                v = f[idx[c]].strip()
                out[c].append(v if c == "Name" else (float(v) if v not in ("","---") else np.nan))
        except ValueError:
            continue
    return out

t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name","i","Qual"])
t2 = read_vizier_tsv(f"{D}/vizier_t2.txt", ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
inc  = {n:i for n,i in zip(t1["Name"], t1["i"])}
qual = {n:q for n,q in zip(t1["Name"], t1["Qual"])}
name = np.array(t2["Name"]); R = np.array(t2["Rad"], float)
Vo = np.array(t2["Vobs"], float); eVo = np.array(t2["e_Vobs"], float)
Vg = np.array(t2["Vgas"], float); Vd = np.array(t2["Vdisk"], float); Vb = np.array(t2["Vbulge"], float)
Vb = np.where(np.isnan(Vb), 0.0, Vb); Vg = np.where(np.isnan(Vg), 0.0, Vg)
inc_a  = np.array([inc.get(n, np.nan)  for n in name], float)
qual_a = np.array([qual.get(n, np.nan) for n in name], float)
m = (R > 0) & (Vo > 0) & np.isfinite(eVo)
m &= (eVo/Vo <= 0.10); m &= (inc_a >= 30.0); m &= (qual_a <= 2)
R, Vo, eVo, Vg, Vd, Vb, name = R[m], Vo[m], eVo[m], Vg[m], Vd[m], Vb[m], name[m]
conv = (KMS**2)/KPC
g_obs = Vo**2 / R * conv
Vbar2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
g_bar = Vbar2 / R * conv
ok = (g_bar > 0) & (g_obs > 0)
g_obs, g_bar, R, name = g_obs[ok], g_bar[ok], R[ok], name[ok]
y = np.log10(g_obs)

grad = np.zeros_like(g_bar)
for gname in set(name):
    idx = np.where(name == gname)[0]
    order = idx[np.argsort(R[idx])]
    r_g = R[order]; gb_g = g_bar[order]
    lr = np.log(r_g); lg = np.log(np.maximum(gb_g, 1e-300))
    d = np.gradient(lg, lr) if len(r_g) >= 3 else np.full_like(lr, np.nan)
    grad[order] = d
valid_grad = np.isfinite(grad)

def choke(gb, a0): return gb*(1.0 + np.sqrt(a0/gb))

# --- real, confound-controlled 2MRS neighbour counts, same method as domain_K_environment ---
sp = read_tsv(f"{D}/sparc_coords.txt", ["Name","_RA","_DE","Dist","i","Qual"])
mr = read_tsv(f"{D}/2mrs.txt", ["RAJ2000","DEJ2000","Ktmag","cz"])
meta={n.strip():dict(ra=ra,de=de,d=d) for n,ra,de,d in zip(sp["Name"],sp["_RA"],sp["_DE"],sp["Dist"])}
Dmax = 10**((MK_LIM + 13.25)/-5.0)
ra_n=np.array(mr["RAJ2000"],float); de_n=np.array(mr["DEJ2000"],float)
cz_n=np.array(mr["cz"],float); kt=np.array(mr["Ktmag"],float)
MK_n = kt - 5*np.log10(np.maximum(1.0,cz_n/H0)) - 25.0
bright = np.isfinite(MK_n)&(MK_n<MK_LIM)&(cz_n>0)
ra_b,de_b,cz_b = np.radians(ra_n[bright]),np.radians(de_n[bright]),cz_n[bright]

n5_by_gal = {}
for gg in sorted(set(name)):
    md = meta.get(gg.strip())
    if md is None or not np.isfinite(md["ra"]) or not np.isfinite(md["d"]) or md["d"]>=Dmax:
        continue
    ra0,de0,d0 = np.radians(md["ra"]),np.radians(md["de"]),md["d"]
    cz0 = H0*d0
    cosang=(np.sin(de0)*np.sin(de_b)+np.cos(de0)*np.cos(de_b)*np.cos(ra0-ra_b))
    ang=np.arccos(np.clip(cosang,-1,1))
    rproj=ang*d0
    vsel=np.abs(cz_b-cz0)<DV_WIN
    self_ex = rproj>0.05
    n5_by_gal[gg] = int(np.sum(vsel&self_ex&(rproj<5.0)))

print(f"Galaxies with valid volume-limited environment measure: {len(n5_by_gal)}")
# balanced terciles on N5 (continuous neighbour count), matching domain_K_environment's
# own approach -- avoids the tiny-isolated-bucket problem of a strict N3=0 cut
gal_list = sorted(n5_by_gal.keys())
n5_vals = np.array([n5_by_gal[g] for g in gal_list], float)
q = np.percentile(n5_vals, [33.3, 66.7])
iso_gal = {g for g,v in zip(gal_list, n5_vals) if v <= q[0]}
grp_gal = {g for g,v in zip(gal_list, n5_vals) if v >= q[1]}
print(f"N5 terciles: low <= {q[0]:.0f}, high >= {q[1]:.0f}")
print(f"Low-density tercile: {len(iso_gal)} galaxies | High-density tercile: {len(grp_gal)} galaxies")

def fit_lambda(mask):
    sub = mask & valid_grad
    def obj(p):
        la0, lam = p
        pred = choke(g_bar[sub], 10**la0) * (1.0 + lam*np.abs(grad[sub]))
        if np.any(pred<=0): return 1e9
        return np.mean((y[sub]-np.log10(pred))**2)
    best = minimize(obj, x0=[-10.0, -0.05], method="Nelder-Mead",
                     options=dict(xatol=1e-8, fatol=1e-12, maxiter=5000))
    la0, lam = best.x
    n_gal = len(set(name[sub]))
    return 10**la0, lam, n_gal, int(sub.sum())

iso_mask = np.array([n in iso_gal for n in name])
grp_mask = np.array([n in grp_gal for n in name])

a0_iso, lam_iso, ng_iso, np_iso = fit_lambda(iso_mask)
a0_grp, lam_grp, ng_grp, np_grp = fit_lambda(grp_mask)

print(f"\nLOW-density tercile  (n_gal={ng_iso}, n_pts={np_iso}): a0={a0_iso:.3e}, lambda={lam_iso:+.5f}")
print(f"HIGH-density tercile (n_gal={ng_grp}, n_pts={np_grp}): a0={a0_grp:.3e}, lambda={lam_grp:+.5f}")
print(f"\nPrediction being tested: lambda should be MORE NEGATIVE for HIGH-density than LOW-density")
print(f"lambda_high - lambda_low = {lam_grp-lam_iso:+.5f}")
if lam_grp < lam_iso:
    print("RESULT: consistent with the competing-external-masses prediction.")
else:
    print("RESULT: NOT consistent -- high-density lambda is not more negative than low-density. Prediction not supported by this test.")

json.dump(dict(split="N5 terciles", n5_low_cut=float(q[0]), n5_high_cut=float(q[1]),
               a0_low=a0_iso, lam_low=lam_iso, n_gal_low=ng_iso, n_pts_low=np_iso,
               a0_high=a0_grp, lam_high=lam_grp, n_gal_high=ng_grp, n_pts_high=np_grp),
          open(f"{D}/domain_CC3_results.json","w"), indent=2)
