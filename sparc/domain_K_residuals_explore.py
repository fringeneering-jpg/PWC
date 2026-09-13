"""
DOMAIN K follow-up -- what falls out of the choke n=1/2 fit's residuals.

Not pre-registered, genuinely exploratory: domain_K_rar.py fits one global relation
across all 175 galaxies pooled together and reports the pooled scatter. This script
asks a question that fit never answered -- does the *leftover* (per-galaxy, per-point)
residual correlate with anything real: inclination, distance, rotation speed, data
quality, radius, or local environment (already-computed a0 wasn't tested against
residuals directly, only against per-galaxy a0 in domain_K_environment.py)?

Uses the same real SPARC data (vizier_t1.txt, vizier_t2.txt), same quality cuts, same
choke n=1/2 model already validated in domain_K_rar.py. No LCDM/dark-matter/dark-energy
content anywhere -- SPARC distances are independent (TRGB/Cepheid/group-median in the
catalog itself, not cosmological redshift), consistent with tonight's request to keep
this run clean of that.
"""
import numpy as np, json
from scipy.optimize import minimize_scalar
from scipy.stats import spearmanr, kruskal

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
KMS = 1.0e3
UPS_D, UPS_B = 0.5, 0.7

def hr(t): print("\n"+"="*78); print(t); print("="*78)

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

hr("1. LOAD (identical to domain_K_rar.py)")
t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name","i","Qual","Vflat","Dist"])
t2 = read_vizier_tsv(f"{D}/vizier_t2.txt", ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
inc  = {n:i for n,i in zip(t1["Name"], t1["i"])}
qual = {n:q for n,q in zip(t1["Name"], t1["Qual"])}
dist = {n:d for n,d in zip(t1["Name"], t1["Dist"])}
vflat= {n:v for n,v in zip(t1["Name"], t1["Vflat"])}

name = np.array(t2["Name"])
R    = np.array(t2["Rad"], float)
Vo   = np.array(t2["Vobs"], float)
eVo  = np.array(t2["e_Vobs"], float)
Vg   = np.where(np.isnan(np.array(t2["Vgas"], float)), 0.0, np.array(t2["Vgas"], float))
Vd   = np.array(t2["Vdisk"], float)
Vb   = np.where(np.isnan(np.array(t2["Vbulge"], float)), 0.0, np.array(t2["Vbulge"], float))

inc_a  = np.array([inc.get(n, np.nan)  for n in name], float)
qual_a = np.array([qual.get(n, np.nan) for n in name], float)
m = (R > 0) & (Vo > 0) & np.isfinite(eVo)
m &= (eVo/Vo <= 0.10)
m &= (inc_a >= 30.0)
m &= (qual_a <= 2)
R,Vo,eVo,Vg,Vd,Vb,name,inc_a = R[m],Vo[m],eVo[m],Vg[m],Vd[m],Vb[m],name[m],inc_a[m]

conv = (KMS**2)/KPC
g_obs = Vo**2 / R * conv
Vbar2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
g_bar = Vbar2 / R * conv
ok = (g_bar > 0) & (g_obs > 0)
g_obs,g_bar,Vo,R,name,inc_a = g_obs[ok],g_bar[ok],Vo[ok],R[ok],name[ok],inc_a[ok]
y = np.log10(g_obs)
print(f"  usable points: {len(g_obs)}, galaxies: {len(set(name))}")

hr("2. REFIT choke n=1/2 (same as domain_K_rar.py, confirming same a0)")
def choke(gb, a0, n=0.5): return gb*(1.0 + (a0/gb)**n)
def obj(la0): return np.mean((y - np.log10(choke(g_bar, 10**la0)))**2)
o = minimize_scalar(obj, bounds=(-12.0,-8.0), method="bounded")
a0 = 10**o.x
resid = y - np.log10(choke(g_bar, a0))   # per-point residual, dex
print(f"  a0 = {a0:.3e} m/s^2, pooled rms = {np.sqrt(np.mean(resid**2)):.4f} dex (sanity check vs domain_K_rar.py's 0.1382)")

hr("3. PER-GALAXY MEAN RESIDUAL vs INTRINSIC PROPERTIES")
galaxies = sorted(set(name))
g_resid, g_inc, g_dist, g_vflat, g_npts, g_rmax = [], [], [], [], [], []
for g in galaxies:
    sel = name == g
    g_resid.append(np.mean(resid[sel]))
    g_inc.append(inc.get(g, np.nan))
    g_dist.append(dist.get(g, np.nan))
    g_vflat.append(vflat.get(g, np.nan))
    g_npts.append(sel.sum())
    g_rmax.append(R[sel].max())
g_resid=np.array(g_resid); g_inc=np.array(g_inc); g_dist=np.array(g_dist)
g_vflat=np.array(g_vflat); g_npts=np.array(g_npts); g_rmax=np.array(g_rmax)

print(f"  {'property':<28}{'Spearman rho':>14}{'p':>12}{'n':>6}")
for lbl, arr in [("inclination (deg)", g_inc), ("distance (Mpc)", g_dist),
                  ("Vflat (km/s)", g_vflat), ("N rotation-curve points", g_npts),
                  ("max radius sampled (kpc)", g_rmax)]:
    ok2 = np.isfinite(arr) & np.isfinite(g_resid)
    rho, p = spearmanr(arr[ok2], g_resid[ok2])
    print(f"  {lbl:<28}{rho:>14.4f}{p:>12.4f}{ok2.sum():>6d}")

hr("4. RESIDUAL vs g_bar (is there curvature the n=1/2 form is missing?)")
rho, p = spearmanr(np.log10(g_bar), resid)
print(f"  per-point residual vs log10(g_bar): rho={rho:.4f}, p={p:.2e}, n={len(resid)}")
# bin into deciles of g_bar, look at mean residual per decile -- reveals systematic curvature
order = np.argsort(g_bar)
dec = np.array_split(order, 10)
print(f"  {'decile (low->high g_bar)':<28}{'mean resid (dex)':>18}{'n pts':>8}")
for i, d in enumerate(dec):
    print(f"  decile {i:<21d}{np.mean(resid[d]):>18.4f}{len(d):>8d}")

hr("5. SPLIT BY GALAXY TYPE PROXY -- high vs low Vflat (rough mass proxy, no per-galaxy free param used in the fit itself)")
med_v = np.nanmedian(g_vflat)
hi = g_vflat >= med_v
lo = g_vflat < med_v
stat, p = kruskal(g_resid[hi & np.isfinite(g_resid)], g_resid[lo & np.isfinite(g_resid)])
print(f"  median Vflat split: high-V mean resid={np.nanmean(g_resid[hi]):.4f}, low-V mean resid={np.nanmean(g_resid[lo]):.4f}")
print(f"  Kruskal-Wallis p={p:.4f}")

out = dict(
    a0=a0, pooled_rms=float(np.sqrt(np.mean(resid**2))),
    n_galaxies=len(galaxies), n_points=len(resid),
)
json.dump(out, open(f"{D}/domain_K_residuals_explore_results.json","w"), indent=2)
print(f"\n  summary -> {D}\\domain_K_residuals_explore_results.json")
