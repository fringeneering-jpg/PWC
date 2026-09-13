"""
DOMAIN K-3 -- does a0 shift with ENVIRONMENT?

MOND               : a0 is a universal constant -> no environmental dependence.
Medium framework   : a0 is set by ambient resistance, which varies with local
                     medium density -> a0 SHOULD track environment.

This is the discriminator. K-2 already showed a0 has no dependence on INTERNAL
galaxy properties (0 of 4 trends). That is not the medium's prediction anyway --
the medium predicts dependence on what is OUTSIDE the galaxy.

Environment from 2MRS (Huchra et al. 2012, J/ApJS/199/26): all-sky K<11.75
redshift survey, ~44k galaxies. Real data, downloaded live.

CONFOUND HANDLED UP FRONT: 2MRS is flux-limited, so raw neighbour counts fall
with distance for purely observational reasons. Domain E was wrecked by exactly
this kind of confound (|GLAT| correlating r=-0.98 with the target). So the
neighbour sample here is VOLUME-LIMITED by absolute magnitude, and the
distance-residual check is reported whether it is flattering or not.
"""
import numpy as np, json
from scipy.optimize import minimize_scalar
from scipy import stats

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
UPS_D, UPS_B = 0.5, 0.7
H0 = 70.0
MK_LIM = -22.0            # volume-limited neighbour threshold
DV_WIN = 1000.0           # km/s association window
def hr(t): print("\n"+"="*78); print(t); print("="*78)

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

hr("1. LOAD")
sp = read_tsv(f"{D}/sparc_coords.txt",
              ["Name","_RA","_DE","Dist","i","Qual","Vflat","L3.6","Rdisk","SBdisk"])
mr = read_tsv(f"{D}/2mrs.txt", ["RAJ2000","DEJ2000","Ktmag","cz"])
t2 = read_tsv(f"{D}/vizier_t2.txt",
              ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
print(f"  SPARC galaxies      : {len(sp['Name'])}")
print(f"  2MRS galaxies       : {len(mr['cz'])}")
print(f"  SPARC curve points  : {len(t2['Name'])}")

# --- per-galaxy a0 (same pipeline as K-2)
meta={n.strip():dict(ra=ra,de=de,d=d,i=i,q=q,vf=vf,L=L,rd=rd,sb=sb)
      for n,ra,de,d,i,q,vf,L,rd,sb in zip(sp["Name"],sp["_RA"],sp["_DE"],sp["Dist"],
      sp["i"],sp["Qual"],sp["Vflat"],sp["L3.6"],sp["Rdisk"],sp["SBdisk"])}
name=np.array([n.strip() for n in t2["Name"]])
R=np.array(t2["Rad"],float); Vo=np.array(t2["Vobs"],float)
eVo=np.array(t2["e_Vobs"],float); Vg=np.nan_to_num(np.array(t2["Vgas"],float))
Vd=np.array(t2["Vdisk"],float); Vb=np.nan_to_num(np.array(t2["Vbulge"],float))
inc=np.array([meta.get(n,{}).get("i",np.nan) for n in name],float)
qa=np.array([meta.get(n,{}).get("q",np.nan) for n in name],float)
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

hr("2. VOLUME-LIMITED ENVIRONMENT (the confound-controlled part)")
mk_ok = -13.25 - 5*np.log10(np.maximum(1.0, np.array(mr["cz"],float)/H0))
Dmax = 10**((MK_LIM + 13.25)/-5.0)
print(f"  2MRS limit K<11.75 -> M_K = {MK_LIM} complete out to {Dmax:.1f} Mpc")
print(f"  So SPARC galaxies are restricted to Dist < {Dmax:.1f} Mpc, and only")
print(f"  neighbours with M_K < {MK_LIM} are counted. Both cuts, not one.")
ra_n=np.array(mr["RAJ2000"],float); de_n=np.array(mr["DEJ2000"],float)
cz_n=np.array(mr["cz"],float); kt=np.array(mr["Ktmag"],float)
MK_n = kt - 5*np.log10(np.maximum(1.0,cz_n/H0)) - 25.0
bright = np.isfinite(MK_n)&(MK_n<MK_LIM)&(cz_n>0)
print(f"  2MRS neighbours passing M_K cut : {bright.sum()} of {len(cz_n)}")
ra_b,de_b,cz_b = np.radians(ra_n[bright]),np.radians(de_n[bright]),cz_n[bright]

rows=[]
for gg in sorted(set(nm)):
    s=(nm==gg)
    if s.sum()<5: continue
    md=meta.get(gg)
    if md is None or not np.isfinite(md["ra"]) or not np.isfinite(md["d"]): continue
    if md["d"] >= Dmax: continue
    a0g=fit_a0(g_bar[s],y[s])
    ra0,de0,d0 = np.radians(md["ra"]),np.radians(md["de"]),md["d"]
    cz0 = H0*d0
    cosang=(np.sin(de0)*np.sin(de_b)+np.cos(de0)*np.cos(de_b)*np.cos(ra0-ra_b))
    ang=np.arccos(np.clip(cosang,-1,1))
    rproj=ang*d0                                   # Mpc, projected at target dist
    vsel=np.abs(cz_b-cz0)<DV_WIN
    self_ex = rproj>0.05                           # drop the galaxy itself
    n1=int(np.sum(vsel&self_ex&(rproj<1.0)))
    n3=int(np.sum(vsel&self_ex&(rproj<3.0)))
    n5=int(np.sum(vsel&self_ex&(rproj<5.0)))
    cand=rproj[vsel&self_ex]
    dnn=float(np.min(cand)) if cand.size else np.nan
    rows.append(dict(name=gg,a0=a0g,npts=int(s.sum()),dist=d0,
                     n1=n1,n3=n3,n5=n5,dnn=dnn,
                     L=md["L"],vf=md["vf"],sb=md["sb"]))
print(f"  SPARC galaxies in the volume-limited sample : {len(rows)}")

A=np.array([r["a0"] for r in rows]); DD=np.array([r["dist"] for r in rows])
N1=np.array([r["n1"] for r in rows],float); N3=np.array([r["n3"] for r in rows],float)
N5=np.array([r["n5"] for r in rows],float); DNN=np.array([r["dnn"] for r in rows],float)
lA=np.log10(A)
print(f"  a0: median {np.median(A):.3e}, log10 scatter {lA.std():.3f} dex")
print(f"  neighbours within 5 Mpc: median {np.median(N5):.0f}, "
      f"range {N5.min():.0f}-{N5.max():.0f}")
print(f"  isolated (0 within 3 Mpc): {int((N3==0).sum())} of {len(rows)}")

hr("3. CONFOUND CHECK -- does the environment measure track distance?")
for lbl,x in (("N within 1 Mpc",N1),("N within 3 Mpc",N3),("N within 5 Mpc",N5),
              ("dist to nearest bright neighbour",DNN)):
    f=np.isfinite(x)
    rho,p=stats.spearmanr(DD[f],x[f])
    print(f"  {lbl:<34} vs SPARC distance: rho={rho:+.3f}, p={p:.2e}"
          + ("   <-- CONFOUNDED" if p<0.01 else ""))
rho_ad,p_ad=stats.spearmanr(DD,lA)
print(f"  {'a0':<34} vs SPARC distance: rho={rho_ad:+.3f}, p={p_ad:.2e}")

hr("4. THE TEST -- a0 vs ENVIRONMENT")
print(f"  {'environment measure':<34} {'Spearman rho':>13} {'p':>11} {'partial(D)':>11} {'verdict':>10}")
print(f"  {'-'*34} {'-'*13} {'-'*11} {'-'*11} {'-'*10}")
res={}
hits=0
for lbl,x in (("N within 1 Mpc",N1),("N within 3 Mpc",N3),("N within 5 Mpc",N5),
              ("log dist to nearest neighbour",np.log10(np.where(DNN>0,DNN,np.nan)))):
    f=np.isfinite(x)&np.isfinite(lA)
    rho,p=stats.spearmanr(x[f],lA[f])
    # partial correlation controlling for SPARC distance, via rank residuals
    rx=stats.rankdata(x[f]); ry=stats.rankdata(lA[f]); rd=stats.rankdata(DD[f])
    bx=np.polyfit(rd,rx,1); by=np.polyfit(rd,ry,1)
    pr,pp=stats.pearsonr(rx-np.polyval(bx,rd), ry-np.polyval(by,rd))
    v="TREND" if (p<0.01 and pp<0.01) else ("marginal" if min(p,pp)<0.05 else "none")
    if v=="TREND": hits+=1
    res[lbl]=dict(rho=float(rho),p=float(p),partial_r=float(pr),partial_p=float(pp))
    print(f"  {lbl:<34} {rho:>13.3f} {p:>11.2e} {pr:>+11.3f} {v:>10}")

hr("5. TERCILE / ISOLATED-vs-GROUP CONTRAST")
q=np.nanpercentile(N5,[33.3,66.7])
lo_m,hi_m = N5<=q[0], N5>=q[1]
u,pu=stats.mannwhitneyu(A[lo_m],A[hi_m])
print(f"  lowest-density tercile  (N5<={q[0]:.0f}, n={lo_m.sum():3d}): "
      f"median a0 = {np.median(A[lo_m]):.3e}")
print(f"  highest-density tercile (N5>={q[1]:.0f}, n={hi_m.sum():3d}): "
      f"median a0 = {np.median(A[hi_m]):.3e}")
print(f"  ratio high/low = {np.median(A[hi_m])/np.median(A[lo_m]):.3f}, "
      f"Mann-Whitney p = {pu:.3f}")
iso,grp = N3==0, N3>=3
if iso.sum()>=8 and grp.sum()>=8:
    u2,pu2=stats.mannwhitneyu(A[iso],A[grp])
    print(f"  isolated (0 in 3 Mpc, n={iso.sum():3d}) median a0 = {np.median(A[iso]):.3e}")
    print(f"  group    (>=3 in 3 Mpc, n={grp.sum():3d}) median a0 = {np.median(A[grp]):.3e}")
    print(f"  ratio = {np.median(A[grp])/np.median(A[iso]):.3f}, "
          f"Mann-Whitney p = {pu2:.3f}")
else:
    pu2=np.nan; print(f"  isolated/group split too small (iso={iso.sum()}, grp={grp.sum()})")

hr("6. VERDICT")
print(f"  significant environment trends (p<0.01 raw AND partial): {hits} of 4")
if hits==0 and (np.isnan(pu2) or pu2>0.05) and pu>0.05:
    print("  -> NO environmental dependence of a0 detected.")
    print("     MOND's premise (a0 universal) survives. The medium reading")
    print("     predicted a trend and there isn't one, in either the continuous")
    print("     correlations or the tercile/isolated-vs-group contrasts.")
    print("     Combined with K-2 (0 of 4 internal trends), a0 shows no")
    print("     dependence on anything measured, internal or external.")
else:
    print("  -> Environmental dependence detected. That is a real discriminator")
    print("     in favour of an environment-set a0 over a universal constant.")
print(f"\n  Statistical power caveat, stated plainly: per-galaxy a0 scatter is")
print(f"  {lA.std():.3f} dex on n={len(rows)} galaxies, so the 2-sigma detectable")
print(f"  trend is roughly {2*lA.std()/np.sqrt(len(rows)):.3f} dex in the mean between")
print(f"  terciles. A weaker environmental effect than that would not show up")
print(f"  here and this null does not exclude it.")
json.dump(dict(n_gal=len(rows),a0_median=float(np.median(A)),
               log_scatter=float(lA.std()),trends=res,
               tercile_p=float(pu),iso_group_p=float(pu2) if not np.isnan(pu2) else None,
               hits=hits), open(f"{D}/domain_K_env_results.json","w"),indent=2)
print(f"\n  -> {D}\\domain_K_env_results.json")
