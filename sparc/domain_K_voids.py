"""
DOMAIN K-4 -- a0 for SPARC galaxies INSIDE cosmic voids vs outside.

Void catalogue: Douglass et al. 2023, ApJS 265, 7 (VizieR J/ApJS/265/7 table1)
  VoidFinder maximal spheres from SDSS DR7, real, downloaded live.
Rotation curves: SPARC (Lelli+ 2016), the same validated pipeline that
  reproduced the published RAR to 3% in a0 and 0.133 dex scatter.

Why this beats the 2MRS neighbour-count version: a void membership flag from a
proper void-finding algorithm is a far cleaner low-density selection than
"few bright neighbours within 3 Mpc", which only found 2 isolated galaxies.

Honest expectation stated BEFORE running: SDSS DR7 covers ~1/4 of sky and the
void sample sits at larger distances than most of SPARC, so the overlap may be
too small to test anything. If so, that is the result and it gets reported as
"insufficient overlap", not stretched.
"""
import numpy as np, json
from scipy.optimize import minimize_scalar
from scipy import stats

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
UPS_D, UPS_B = 0.5, 0.7
H_LITTLE = 0.7
def hr(t): print("\n"+"="*78); print(t); print("="*78)

def read_tsv(path, cols):
    lines=[l.rstrip("\n") for l in open(path,encoding="utf-8",errors="replace")]
    hdr=next(i for i,l in enumerate(lines) if not l.startswith("#") and "\t" in l
             and all(c in l.split("\t") for c in cols[:2]))
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
                out[c].append(v if c in ("Name","Cosmo") else
                              (float(v) if v not in("","---") else np.nan))
        except ValueError: continue
    return out

hr("1. LOAD VOIDS AND SPARC")
vd = read_tsv(f"{D}/voids_vf.txt",
              ["recno","Cosmo","x","y","z","Rad","void","edge","s","RAJ2000","DEJ2000"])
cos_a=np.array(vd["Cosmo"]); sel=(cos_a=="Planck2018")
vx=np.array(vd["x"],float)[sel]; vy=np.array(vd["y"],float)[sel]
vz=np.array(vd["z"],float)[sel]; vR=np.array(vd["Rad"],float)[sel]
vs=np.array(vd["s"],float)[sel]; vedge=np.array(vd["edge"],float)[sel]
print(f"  void maximal spheres (Planck2018) : {sel.sum()} of {len(cos_a)}")
print(f"  void centre distance s  : {vs.min():.1f} to {vs.max():.1f} h-1 Mpc")
print(f"  void radius Rad         : {vR.min():.1f} to {vR.max():.1f} h-1 Mpc")
print(f"  nearest void inner edge : {(vs-vR).min():.1f} h-1 Mpc"
      f"  = {(vs-vR).min()/H_LITTLE:.1f} Mpc")

sp = read_tsv(f"{D}/sparc_coords.txt",
              ["Name","_RA","_DE","Dist","i","Qual","Vflat","L3.6","Rdisk","SBdisk"])
t2 = read_tsv(f"{D}/vizier_t2.txt",
              ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
meta={n.strip():dict(ra=ra,de=de,d=dd,i=i,q=q) for n,ra,de,dd,i,q in
      zip(sp["Name"],sp["_RA"],sp["_DE"],sp["Dist"],sp["i"],sp["Qual"])}
name=np.array([n.strip() for n in t2["Name"]])
R=np.array(t2["Rad"],float); Vo=np.array(t2["Vobs"],float)
eVo=np.array(t2["e_Vobs"],float); Vg=np.nan_to_num(np.array(t2["Vgas"],float))
Vd=np.array(t2["Vdisk"],float); Vb=np.nan_to_num(np.array(t2["Vbulge"],float))
inc=np.array([meta.get(n,{}).get("i",np.nan) for n in name],float)
qa =np.array([meta.get(n,{}).get("q",np.nan) for n in name],float)
m=(R>0)&(Vo>0)&np.isfinite(eVo)&(eVo/np.where(Vo>0,Vo,1)<=0.10)&(inc>=30)&(qa<=2)
conv=(1.0e3**2)/KPC
g_obs=(Vo**2/R*conv)[m]
g_bar=((Vg*np.abs(Vg)+UPS_D*Vd*np.abs(Vd)+UPS_B*Vb*np.abs(Vb))/R*conv)[m]
nm=name[m]; ok=(g_bar>0)&(g_obs>0)
g_obs,g_bar,nm=g_obs[ok],g_bar[ok],nm[ok]; y=np.log10(g_obs)
rar=lambda gb,a0: gb/(1.0-np.exp(-np.sqrt(gb/a0)))
def fit_a0(gb,yy):
    o=minimize_scalar(lambda la: np.mean((yy-np.log10(rar(gb,10**la)))**2),
                      bounds=(-12,-8),method="bounded")
    return 10**o.x

hr("2. RADIAL OVERLAP CHECK (before any classification)")
gals=[g for g in sorted(set(nm)) if (nm==g).sum()>=5
      and g in meta and np.isfinite(meta[g]["d"]) and np.isfinite(meta[g]["ra"])]
dists=np.array([meta[g]["d"] for g in gals])
print(f"  SPARC galaxies with >=5 points : {len(gals)}")
print(f"  SPARC distance range           : {dists.min():.1f} to {dists.max():.1f} Mpc")
print(f"                                 = {dists.min()*H_LITTLE:.1f} to "
      f"{dists.max()*H_LITTLE:.1f} h-1 Mpc")
lo,hi=(vs-vR).min(),(vs+vR).max()
n_in_shell=int(((dists*H_LITTLE>=lo)&(dists*H_LITTLE<=hi)).sum())
print(f"  void survey radial span        : {lo:.1f} to {hi:.1f} h-1 Mpc")
print(f"  SPARC galaxies inside that span: {n_in_shell}")
if n_in_shell==0:
    print("\n  >>> ZERO radial overlap. The SDSS DR7 void catalogue does not reach")
    print("      in to SPARC's distances. This test cannot be run with these two")
    print("      datasets. Reported as insufficient overlap, not stretched.")

hr("3. VOID MEMBERSHIP")
rows=[]
for g in gals:
    md=meta[g]
    s=md["d"]*H_LITTLE
    ra,de=np.radians(md["ra"]),np.radians(md["de"])
    gx=s*np.cos(de)*np.cos(ra); gy=s*np.cos(de)*np.sin(ra); gz=s*np.sin(de)
    dd=np.sqrt((gx-vx)**2+(gy-vy)**2+(gz-vz)**2)
    inside=dd<vR
    j=int(np.argmin(dd-vR))
    a0g=fit_a0(g_bar[nm==g],y[nm==g])
    rows.append(dict(name=g,a0=a0g,dist=md["d"],s=s,
                     in_void=bool(inside.any()),
                     n_void=int(inside.sum()),
                     frac_to_edge=float((dd[j]/vR[j])),
                     nearest_void_gap=float((dd-vR).min())))
A=np.array([r["a0"] for r in rows]); IN=np.array([r["in_void"] for r in rows])
GAP=np.array([r["nearest_void_gap"] for r in rows])
print(f"  SPARC galaxies classified      : {len(rows)}")
print(f"  inside a VoidFinder sphere     : {int(IN.sum())}")
print(f"  outside                        : {int((~IN).sum())}")
print(f"  nearest-void gap (h-1 Mpc): min {GAP.min():.1f}, median {np.median(GAP):.1f}")

hr("4. RESULT")
if IN.sum()>=8 and (~IN).sum()>=8:
    u,p=stats.mannwhitneyu(A[IN],A[~IN])
    print(f"  void   (n={int(IN.sum()):3d}) median a0 = {np.median(A[IN]):.4e}")
    print(f"  非void (n={int((~IN).sum()):3d}) median a0 = {np.median(A[~IN]):.4e}")
    print(f"  ratio void/non-void = {np.median(A[IN])/np.median(A[~IN]):.3f}, "
          f"Mann-Whitney p = {p:.4f}")
    res=dict(n_void=int(IN.sum()),n_non=int((~IN).sum()),
             a0_void=float(np.median(A[IN])),a0_non=float(np.median(A[~IN])),p=float(p))
else:
    print(f"  INSUFFICIENT SAMPLE: {int(IN.sum())} in-void vs "
          f"{int((~IN).sum())} outside.")
    print("  A Mann-Whitney needs roughly >=8 per side to mean anything, so no")
    print("  statistic is quoted. This is a data-availability failure, not a")
    print("  null result about physics -- the two must not be conflated.")
    res=dict(n_void=int(IN.sum()),n_non=int((~IN).sum()),verdict="insufficient overlap")
    # continuous fallback: does a0 track distance-to-nearest-void-edge at all?
    f=np.isfinite(GAP)&np.isfinite(A)
    rho,pp=stats.spearmanr(GAP[f],np.log10(A[f]))
    print(f"\n  Continuous fallback (uses every galaxy, no membership cut):")
    print(f"  a0 vs gap-to-nearest-void-edge: Spearman rho={rho:+.3f}, p={pp:.3f}")
    print(f"  n={int(f.sum())}. Weaker than a membership test but it is what the")
    print(f"  overlap supports.")
    res["fallback_rho"]=float(rho); res["fallback_p"]=float(pp)

json.dump(res, open(f"{D}/domain_K_voids_results.json","w"), indent=2)
print(f"\n  -> {D}\\domain_K_voids_results.json")
