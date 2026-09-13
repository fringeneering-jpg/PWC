"""
DOMAIN K follow-up #3 -- does the transition-sharpness parameter s vary per galaxy
with local environment ("each galaxy has its own pressure bubble"), rather than being
one universal number?

Part 6 found a single pooled s=1.51 closes the RAR gap. Tonight's claim: the underlying
force law doesn't change galaxy to galaxy, but each galaxy sits in its own local ambient
medium ("pressure bubble"), so the drag/transition shape it experiences should differ
per system -- s should vary with each galaxy's own environment, not be one fixed number.

This reuses the exact volume-limited, confound-checked environment pipeline from
domain_K_environment.py (2MRS neighbour counts within 1/3/5 Mpc, distance to nearest
neighbour, distance-confound already verified there) but tests it against per-galaxy s
instead of per-galaxy a0 (which K-3 already tested and found null).

a0 held FIXED at the global pooled value from domain_K_transition_shape.py (1.255e-10
m/s^2) so each galaxy's fit has exactly one free parameter (s) -- keeps per-galaxy fits
stable even for galaxies with few rotation-curve points.
"""
import numpy as np, json
from scipy.optimize import minimize_scalar
from scipy import stats

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
UPS_D, UPS_B = 0.5, 0.7
H0 = 70.0
MK_LIM = -22.0
DV_WIN = 1000.0
A0_GLOBAL = 1.255e-10   # from domain_K_transition_shape.py, s-free pooled fit

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

hr("1. LOAD (same as domain_K_environment.py)")
sp = read_tsv(f"{D}/sparc_coords.txt",
              ["Name","_RA","_DE","Dist","i","Qual","Vflat","L3.6","Rdisk","SBdisk"])
mr = read_tsv(f"{D}/2mrs.txt", ["RAJ2000","DEJ2000","Ktmag","cz"])
t2 = read_tsv(f"{D}/vizier_t2.txt", ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])

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

def choke_s(gb, s, a0=A0_GLOBAL):
    return gb * (1.0 + (a0/gb)**(s/2.0))**(1.0/s)

def fit_s(gb, yy):
    def obj(s):
        if not (0.1 < s < 20.0): return 1e9
        try:
            pred = choke_s(gb, s)
            if not np.all(np.isfinite(pred)) or np.any(pred<=0): return 1e9
            return np.mean((yy-np.log10(pred))**2)
        except (OverflowError, FloatingPointError):
            return 1e9
    o = minimize_scalar(obj, bounds=(0.1, 20.0), method="bounded")
    return o.x

hr("2. VOLUME-LIMITED ENVIRONMENT (identical method to domain_K_environment.py)")
Dmax = 10**((MK_LIM + 13.25)/-5.0)
ra_n=np.array(mr["RAJ2000"],float); de_n=np.array(mr["DEJ2000"],float)
cz_n=np.array(mr["cz"],float); kt=np.array(mr["Ktmag"],float)
MK_n = kt - 5*np.log10(np.maximum(1.0,cz_n/H0)) - 25.0
bright = np.isfinite(MK_n)&(MK_n<MK_LIM)&(cz_n>0)
ra_b,de_b,cz_b = np.radians(ra_n[bright]),np.radians(de_n[bright]),cz_n[bright]

rows=[]
for gg in sorted(set(nm)):
    s_mask=(nm==gg)
    if s_mask.sum()<5: continue
    md=meta.get(gg)
    if md is None or not np.isfinite(md["ra"]) or not np.isfinite(md["d"]): continue
    if md["d"] >= Dmax: continue
    s_fit = fit_s(g_bar[s_mask], y[s_mask])
    ra0,de0,d0 = np.radians(md["ra"]),np.radians(md["de"]),md["d"]
    cz0 = H0*d0
    cosang=(np.sin(de0)*np.sin(de_b)+np.cos(de0)*np.cos(de_b)*np.cos(ra0-ra_b))
    ang=np.arccos(np.clip(cosang,-1,1))
    rproj=ang*d0
    vsel=np.abs(cz_b-cz0)<DV_WIN
    self_ex = rproj>0.05
    n1=int(np.sum(vsel&self_ex&(rproj<1.0)))
    n3=int(np.sum(vsel&self_ex&(rproj<3.0)))
    n5=int(np.sum(vsel&self_ex&(rproj<5.0)))
    cand=rproj[vsel&self_ex]
    dnn=float(np.min(cand)) if cand.size else np.nan
    rows.append(dict(name=gg,s=s_fit,npts=int(s_mask.sum()),dist=d0,
                     n1=n1,n3=n3,n5=n5,dnn=dnn,vf=md["vf"],L=md["L"]))
print(f"  SPARC galaxies in volume-limited sample: {len(rows)}")

S=np.array([r["s"] for r in rows]); DD=np.array([r["dist"] for r in rows])
N1=np.array([r["n1"] for r in rows],float); N3=np.array([r["n3"] for r in rows],float)
N5=np.array([r["n5"] for r in rows],float); DNN=np.array([r["dnn"] for r in rows],float)
VF=np.array([r["vf"] for r in rows],float)
print(f"  per-galaxy s: median {np.median(S):.3f}, scatter {S.std():.3f}, "
      f"range {S.min():.3f}-{S.max():.3f}")

hr("3. CONFOUND CHECK -- environment measures vs distance (must already be clean, reused from K-3)")
for lbl,x in (("N within 1 Mpc",N1),("N within 3 Mpc",N3),("N within 5 Mpc",N5)):
    rho,p=stats.spearmanr(DD,x)
    print(f"  {lbl:<20} vs distance: rho={rho:+.3f}, p={p:.2e}" + ("  <-- CONFOUNDED" if p<0.01 else ""))

hr("4. THE TEST -- per-galaxy s vs ENVIRONMENT ('pressure bubble' claim)")
print(f"  {'environment measure':<32}{'Spearman rho':>13}{'p':>11}{'partial(D)':>11}{'verdict':>10}")
print(f"  {'-'*32}{'-'*13}{'-'*11}{'-'*11}{'-'*10}")
res={}; hits=0
for lbl,x in (("N within 1 Mpc",N1),("N within 3 Mpc",N3),("N within 5 Mpc",N5),
              ("log dist to nearest neighbour",np.log10(np.where(DNN>0,DNN,np.nan)))):
    f=np.isfinite(x)&np.isfinite(S)
    rho,p=stats.spearmanr(x[f],S[f])
    rx=stats.rankdata(x[f]); ry=stats.rankdata(S[f]); rd=stats.rankdata(DD[f])
    bx=np.polyfit(rd,rx,1); by=np.polyfit(rd,ry,1)
    pr,pp=stats.pearsonr(rx-np.polyval(bx,rd), ry-np.polyval(by,rd))
    v="TREND" if (p<0.01 and pp<0.01) else ("marginal" if min(p,pp)<0.05 else "none")
    if v=="TREND": hits+=1
    res[lbl]=dict(rho=float(rho),p=float(p),partial_r=float(pr),partial_p=float(pp))
    print(f"  {lbl:<32}{rho:>13.3f}{p:>11.2e}{pr:>+11.3f}{v:>10}")

hr("5. TERCILE CONTRAST + intrinsic-property check (mirrors K-2/K-3 structure)")
q=np.nanpercentile(N5,[33.3,66.7])
lo_m,hi_m = N5<=q[0], N5>=q[1]
u,pu=stats.mannwhitneyu(S[lo_m],S[hi_m])
print(f"  lowest-density tercile  (N5<={q[0]:.0f}, n={lo_m.sum():3d}): median s = {np.median(S[lo_m]):.3f}")
print(f"  highest-density tercile (N5>={q[1]:.0f}, n={hi_m.sum():3d}): median s = {np.median(S[hi_m]):.3f}")
print(f"  Mann-Whitney p = {pu:.3f}")
f=np.isfinite(VF)&np.isfinite(S)
rho_vf,p_vf = stats.spearmanr(VF[f], S[f])
print(f"  s vs Vflat (intrinsic mass proxy, not environment): rho={rho_vf:+.3f}, p={p_vf:.3f}")

hr("6. VERDICT")
print(f"  significant environment trends on s (p<0.01 raw AND partial): {hits} of 4")
if hits==0 and pu>0.05:
    print("  -> NO environmental dependence of s detected in this sample.")
    print("     The 'every galaxy has its own pressure-bubble drag' claim predicts a")
    print("     trend here and none was found -- same outcome K-3 already found for a0.")
else:
    print("  -> Environmental dependence on s detected -- real support for the")
    print("     per-galaxy pressure-bubble claim, a genuine discriminator MOND doesn't predict.")
print(f"\n  Power caveat: per-galaxy s scatter is {S.std():.3f} on n={len(rows)} galaxies,")
print(f"  so a weaker effect than roughly {2*S.std()/np.sqrt(len(rows)):.3f} (2-sigma, mean")
print(f"  difference between terciles) would not be detectable here.")

json.dump(dict(n_gal=len(rows), s_median=float(np.median(S)), s_scatter=float(S.std()),
               trends=res, tercile_p=float(pu), vflat_rho=float(rho_vf), vflat_p=float(p_vf),
               hits=hits), open(f"{D}/domain_K_s_environment_results.json","w"), indent=2)
print(f"\n  -> {D}\\domain_K_s_environment_results.json")
