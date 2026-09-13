"""
DOMAIN K-2 -- can a0 be DERIVED rather than fitted?

Three separate questions, kept apart on purpose:
  (1) What is a0 from real SPARC, with a proper bootstrap error bar?
  (2) Which dimensional combinations of the framework's own quantities land on
      it, and which of those contain a free numerical factor (i.e. are fits in
      disguise)?
  (3) Is a0 actually UNIVERSAL? MOND says yes by construction. A medium-based
      framework says ambient resistance depends on the local medium, which
      varies -- so a per-galaxy trend would DISCRIMINATE between them.
      Question (3) needs no derivation at all and is the strongest test here.
"""
import numpy as np, json
from scipy.optimize import minimize_scalar
from scipy import stats

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
MPC = 3.0856775814913673e22
c_l, G = 2.99792458e8, 6.67430e-11
UPS_D, UPS_B = 0.5, 0.7
A0_LIT = 1.2e-10
H0_70 = 70.0*1e3/MPC
RHO_CRIT = 3*H0_70**2/(8*np.pi*G)
NU_BULK = 0.34454                 # from the S8 fit
TAU = 1.0/(NU_BULK*H0_70)         # 40.5 Gyr

def hr(t): print("\n"+"="*78); print(t); print("="*78)

def read_vizier_tsv(path, cols):
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8", errors="replace")]
    hdr_i = next(i for i,l in enumerate(lines)
                 if not l.startswith("#") and l.strip() and "\t" in l and "recno" in l)
    names = lines[hdr_i].split("\t")
    dash_i = max(i for i in range(hdr_i+1, hdr_i+6)
                 if set(lines[i].replace("\t","").strip()) <= set("- "))
    idx = {c: names.index(c) for c in cols}
    out = {c: [] for c in cols}
    for l in lines[dash_i+1:]:
        if not l.strip() or l.startswith("#"): continue
        f = l.split("\t")
        if len(f) < len(names): continue
        try:
            for c in cols:
                v = f[idx[c]].strip()
                out[c].append(v if c=="Name" else (float(v) if v not in ("","---") else np.nan))
        except ValueError: continue
    return out

t1 = read_vizier_tsv(f"{D}/vizier_t1.txt",
                     ["Name","i","Qual","Vflat","L3.6","Rdisk","MHI","SBdisk"])
t2 = read_vizier_tsv(f"{D}/vizier_t2.txt",
                     ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
meta = {n:dict(i=i,q=q,vf=vf,L=L,rd=rd,mhi=mh,sb=sb) for n,i,q,vf,L,rd,mh,sb in
        zip(t1["Name"],t1["i"],t1["Qual"],t1["Vflat"],t1["L3.6"],t1["Rdisk"],
            t1["MHI"],t1["SBdisk"])}

name = np.array(t2["Name"]); R=np.array(t2["Rad"],float)
Vo=np.array(t2["Vobs"],float); eVo=np.array(t2["e_Vobs"],float)
Vg=np.nan_to_num(np.array(t2["Vgas"],float)); Vd=np.array(t2["Vdisk"],float)
Vb=np.nan_to_num(np.array(t2["Vbulge"],float))
inc=np.array([meta.get(n,{}).get("i",np.nan) for n in name],float)
qa =np.array([meta.get(n,{}).get("q",np.nan) for n in name],float)

m = (R>0)&(Vo>0)&np.isfinite(eVo)&(eVo/np.where(Vo>0,Vo,1)<=0.10)&(inc>=30)&(qa<=2)
conv=(1.0e3**2)/KPC
g_obs=(Vo**2/R*conv)[m]
g_bar=((Vg*np.abs(Vg)+UPS_D*Vd*np.abs(Vd)+UPS_B*Vb*np.abs(Vb))/R*conv)[m]
nm=name[m]; ok=(g_bar>0)&(g_obs>0)
g_obs,g_bar,nm=g_obs[ok],g_bar[ok],nm[ok]
y=np.log10(g_obs)
rar=lambda gb,a0: gb/(1.0-np.exp(-np.sqrt(gb/a0)))

def fit_a0(gb,yy):
    o=minimize_scalar(lambda la: np.mean((yy-np.log10(rar(gb,10**la)))**2),
                      bounds=(-12,-8), method="bounded")
    return 10**o.x, float(np.sqrt(o.fun))

hr("1. a0 FROM REAL SPARC, WITH BOOTSTRAP ERROR BAR")
a0_best, rms = fit_a0(g_bar,y)
print(f"  points {len(y)}, galaxies {len(set(nm))}")
print(f"  a0 (point-weighted) : {a0_best:.4e} m/s^2,  rms {rms:.4f} dex")
gals=np.array(sorted(set(nm)))
rng=np.random.default_rng(12345)
boot=[]
for _ in range(400):
    pick=rng.choice(gals,size=len(gals),replace=True)
    sel=np.concatenate([np.where(nm==gg)[0] for gg in pick])
    boot.append(fit_a0(g_bar[sel],y[sel])[0])
boot=np.array(boot)
lo,hi=np.percentile(boot,[16,84])
print(f"  galaxy-bootstrap 68% CI: {lo:.4e} to {hi:.4e}  (+/- {(hi-lo)/2:.3e})")
print(f"  literature (McGaugh 2016): {A0_LIT:.3e}   -> "
      f"{'CONSISTENT' if lo<=A0_LIT<=hi else 'inconsistent'}")
sig=(hi-lo)/2

hr("2. CANDIDATE DERIVATIONS -- and which are fits in disguise")
cH0=c_l*H0_70
cands=[
 ("c*H0",                              cH0,                          "none"),
 ("c*H0 / 2pi",                        cH0/(2*np.pi),                "2pi chosen"),
 ("c*H0 / 6",                          cH0/6.0,                      "6 chosen"),
 ("c*sqrt(G*rho_crit)",                c_l*np.sqrt(G*RHO_CRIT),      "none"),
 ("c*sqrt(G*rho_crit) / 2",            c_l*np.sqrt(G*RHO_CRIT)/2,    "2 chosen"),
 ("c*sqrt(G*rho_med), rho=7.5e-27",    c_l*np.sqrt(G*7.5e-27),       "none"),
 ("c*sqrt(G*rho_med) / 2",             c_l*np.sqrt(G*7.5e-27)/2,     "2 chosen"),
 ("(c^2/2pi)*sqrt(Lambda/3), OmL=0.7", (c_l**2/(2*np.pi))*(H0_70*np.sqrt(0.7)/c_l), "2pi chosen"),
 ("c / tau   [tau from S8 fit]",       c_l/TAU,                      "none, but tau is FITTED"),
 ("c / (2*tau)",                       c_l/(2*TAU),                  "2 chosen AND tau fitted"),
 ("c*H0*Om_heatleak (0.4093)",         cH0*0.4093,                   "none"),
]
print(f"  measured a0 = {a0_best:.4e} +/- {sig:.3e}  (68% galaxy bootstrap)\n")
print(f"  {'candidate':<38} {'value':>12} {'ratio':>8} {'sigma off':>10} {'free factor':<24}")
print(f"  {'-'*38} {'-'*12} {'-'*8} {'-'*10} {'-'*24}")
scored=[]
for lbl,v,note in cands:
    z=(v-a0_best)/sig
    scored.append((abs(z),lbl,v,z,note))
    print(f"  {lbl:<38} {v:12.4e} {v/a0_best:8.3f} {z:+10.1f} {note:<24}")
print(f"\n  tau = {TAU:.4e} s = {TAU/3.156e16:.1f} Gyr,  H0=70 convention throughout")

hr("3. THE HONEST READING OF THE c/(2*tau) HIT")
v=c_l/(2*TAU)
print(f"  c/(2*tau) = {v:.4e} vs measured {a0_best:.4e}  -> {100*(v/a0_best-1):+.1f}%")
print("  That is the closest candidate. But unpack it before believing it:")
print(f"      tau  = 1/(nu_bulk*H0),  nu_bulk = {NU_BULK} was FITTED to the S8 deficit")
print(f"      so c/(2*tau) = (nu_bulk/2)*c*H0 = {NU_BULK/2:.4f} * c*H0")
print(f"      and measured a0/(c*H0) = {a0_best/cH0:.4f}")
print(f"  i.e. the 'derivation' says nu_bulk/2 = a0/(c*H0), which is")
print(f"      {NU_BULK/2:.4f} vs {a0_best/cH0:.4f}  -- agreement {100*abs(NU_BULK/2/(a0_best/cH0)-1):.1f}%")
print("\n  Two independently FITTED numbers agreeing to ~1%. That is exactly the")
print("  shape of the 0.01 claim I pushed back on, and it deserves the same")
print("  treatment: interesting, not evidence. The difference -- and it IS a")
print("  real difference -- is that both quantities here are independently")
print("  MEASURABLE, so 'a0 = c/(2 tau)' is a falsifiable prediction rather")
print("  than a coincidence between a residual and a state variable.")
print("  To promote it you need the mechanism that puts the 2 there. Without")
print("  that, it is a fit with two steps.")

hr("4. IS a0 UNIVERSAL? -- the test that needs no derivation at all")
print("  MOND: a0 is a universal constant, so per-galaxy a0 must show NO trend.")
print("  Medium framework: ambient resistance depends on the local medium,")
print("  which varies galaxy to galaxy -- so a trend IS predicted.")
print("  This discriminates between them using only real data.\n")
rows=[]
for gg in gals:
    s=(nm==gg)
    if s.sum()<5: continue
    a0g,rg=fit_a0(g_bar[s],y[s])
    md=meta.get(gg,{})
    rows.append((gg,a0g,rg,int(s.sum()),md.get("L",np.nan),md.get("vf",np.nan),
                 md.get("rd",np.nan),md.get("sb",np.nan)))
A=np.array([r[1] for r in rows]); L=np.array([r[4] for r in rows],float)
VF=np.array([r[5] for r in rows],float); RD=np.array([r[6] for r in rows],float)
SB=np.array([r[7] for r in rows],float)
print(f"  galaxies with >=5 usable points : {len(rows)}")
print(f"  per-galaxy a0: median {np.median(A):.3e}, "
      f"16-84% {np.percentile(A,16):.3e} to {np.percentile(A,84):.3e}")
print(f"  scatter in log10(a0)            : {np.std(np.log10(A)):.3f} dex\n")
print(f"  {'a0 correlated against':<34} {'Spearman rho':>13} {'p':>12} {'verdict':>12}")
print(f"  {'-'*34} {'-'*13} {'-'*12} {'-'*12}")
trend_hits=0
for lbl,x in (("L_3.6 (stellar luminosity)",L),("Vflat (rotation speed)",VF),
              ("Rdisk (disk scale length)",RD),("SBdisk (surface brightness)",SB)):
    f=np.isfinite(x)&np.isfinite(A)&(x>0)
    if f.sum()<20: continue
    rho,p=stats.spearmanr(np.log10(x[f]),np.log10(A[f]))
    v="TREND" if p<0.01 else ("marginal" if p<0.05 else "no trend")
    if p<0.01: trend_hits+=1
    print(f"  {lbl:<34} {rho:>13.3f} {p:>12.2e} {v:>12}")
print(f"\n  significant trends (p<0.01): {trend_hits} of 4")
if trend_hits==0:
    print("  -> a0 behaves as a UNIVERSAL constant. This SUPPORTS MOND's premise")
    print("     and is a problem for a medium whose local density varies: if")
    print("     ambient resistance sets a0, a0 should track something. It does not.")
else:
    print("  -> a0 varies systematically. That is a genuine discriminator IN")
    print("     FAVOUR of an environment-dependent medium over universal MOND,")
    print("     and it is the strongest result available in this domain.")

json.dump(dict(a0=a0_best,a0_lo=lo,a0_hi=hi,rms=rms,
               per_galaxy_log_scatter=float(np.std(np.log10(A))),
               n_gal=len(rows),trend_hits=trend_hits),
          open(f"{D}/domain_K_a0_results.json","w"),indent=2)
print(f"\n  -> {D}\\domain_K_a0_results.json")
