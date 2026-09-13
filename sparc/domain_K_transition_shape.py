"""
DOMAIN K follow-up #2 -- does a smoother transition shape close the residual gap found
in domain_K_residuals_explore.py (real, p=1.5e-47 systematic trend vs g_bar)?

The choke n=1/2 form g_obs = g_bar*(1+(a0/g_bar)^0.5) already has the two asymptotic
limits forced by the framework itself: Newtonian at high g_bar, g_obs -> sqrt(a0*g_bar)
at low g_bar (required for flat rotation curves). What's NOT forced is the sharpness of
the transition between those two limits -- the pure power law is one specific choice, not
the only one consistent with the framework's own constraints.

Generalization tested here (both asymptotic limits preserved for ANY s):

    g_obs = g_bar * (1 + (a0/g_bar)^(s/2))^(1/s)

s=1 reproduces the original choke n=1/2 form exactly. s != 1 changes only the sharpness
of the transition. Fit (a0, s) jointly -- same parameter count (2) as domain_K_rar.py's
"choke_free_n" fit -- and see what the data actually wants, honestly reported either way.

Same real SPARC data/cuts as domain_K_rar.py and domain_K_residuals_explore.py. No
LCDM/dark-matter content (independent SPARC distances).
"""
import numpy as np, json
from scipy.optimize import minimize, minimize_scalar
from scipy.stats import spearmanr

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

hr("1. LOAD (identical cuts to domain_K_rar.py)")
t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name","i","Qual","Vflat","Dist"])
t2 = read_vizier_tsv(f"{D}/vizier_t2.txt", ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
inc  = {n:i for n,i in zip(t1["Name"], t1["i"])}
qual = {n:q for n,q in zip(t1["Name"], t1["Qual"])}
name = np.array(t2["Name"]); R = np.array(t2["Rad"], float)
Vo = np.array(t2["Vobs"], float); eVo = np.array(t2["e_Vobs"], float)
Vg = np.where(np.isnan(np.array(t2["Vgas"], float)), 0.0, np.array(t2["Vgas"], float))
Vd = np.array(t2["Vdisk"], float)
Vb = np.where(np.isnan(np.array(t2["Vbulge"], float)), 0.0, np.array(t2["Vbulge"], float))
inc_a  = np.array([inc.get(n, np.nan)  for n in name], float)
qual_a = np.array([qual.get(n, np.nan) for n in name], float)
m = (R > 0) & (Vo > 0) & np.isfinite(eVo)
m &= (eVo/Vo <= 0.10); m &= (inc_a >= 30.0); m &= (qual_a <= 2)
R,Vo,Vg,Vd,Vb = R[m],Vo[m],Vg[m],Vd[m],Vb[m]
conv = (KMS**2)/KPC
g_obs = Vo**2/R*conv
g_bar = (Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb))/R*conv
ok = (g_bar>0)&(g_obs>0)
g_obs, g_bar = g_obs[ok], g_bar[ok]
y = np.log10(g_obs)
print(f"  usable points: {len(g_obs)}")

def scatter(pred):
    r = y - np.log10(pred)
    return float(np.sqrt(np.mean(r**2)))

hr("2. BASELINES (from domain_K_rar.py, for comparison)")
def rar_mcgaugh(gb, a0): return gb/(1.0-np.exp(-np.sqrt(gb/a0)))
o = minimize_scalar(lambda la0: np.mean((y-np.log10(rar_mcgaugh(g_bar,10**la0)))**2), bounds=(-11,-9), method="bounded")
rms_mcgaugh = scatter(rar_mcgaugh(g_bar, 10**o.x))
print(f"  McGaugh RAR (1 param)          : {rms_mcgaugh:.4f} dex")

def choke_s1(gb, a0): return gb*(1.0+(a0/gb)**0.5)
o1 = minimize_scalar(lambda la0: np.mean((y-np.log10(choke_s1(g_bar,10**la0)))**2), bounds=(-12,-8), method="bounded")
rms_s1 = scatter(choke_s1(g_bar, 10**o1.x))
print(f"  choke n=1/2, s=1 fixed (1 param): {rms_s1:.4f} dex  (matches domain_K_rar.py's 0.1382)")

hr("3. GENERALIZED TRANSITION SHAPE: g_obs = g_bar*(1+(a0/g_bar)^(s/2))^(1/s)")
print("  Both forced asymptotic limits (Newtonian at high g_bar, sqrt(a0*g_bar) at low")
print("  g_bar) hold for ANY s -- s is purely a transition-sharpness parameter, not")
print("  something that could break the framework's own forced boundary conditions.\n")

def choke_s(gb, a0, s):
    return gb * (1.0 + (a0/gb)**(s/2.0))**(1.0/s)

def obj(p):
    la0, s = p
    if not (0.05 < s < 20.0): return 1e9
    try:
        pred = choke_s(g_bar, 10**la0, s)
        if not np.all(np.isfinite(pred)) or np.any(pred<=0): return 1e9
        return np.mean((y - np.log10(pred))**2)
    except (OverflowError, FloatingPointError):
        return 1e9

best = minimize(obj, x0=[-10.0, 1.0], method="Nelder-Mead",
                 options=dict(xatol=1e-7, fatol=1e-12, maxiter=6000))
la0_b, s_b = best.x
rms_b = scatter(choke_s(g_bar, 10**la0_b, s_b))
print(f"  fitted: a0={10**la0_b:.3e} m/s^2, s={s_b:.4f}, rms={rms_b:.4f} dex")
print(f"  (s=1.0 is the original pure power-law choke form)")

hr("4. VERDICT")
print(f"  {'model':<40}{'params':>8}{'rms dex':>10}")
print(f"  {'-'*40}{'-'*8}{'-'*10}")
print(f"  {'choke, s=1 fixed (original)':<40}{1:>8}{rms_s1:>10.4f}")
print(f"  {'choke, s free (this test)':<40}{2:>8}{rms_b:>10.4f}")
print(f"  {'McGaugh RAR (exponential form)':<40}{1:>8}{rms_mcgaugh:>10.4f}")
print(f"\n  improvement over s=1: {rms_s1-rms_b:+.4f} dex")
print(f"  remaining gap to McGaugh: {rms_b-rms_mcgaugh:+.4f} dex")

hr("5. DOES THE RESIDUAL-VS-g_bar TREND FROM PART 5 GO AWAY?")
resid_b = y - np.log10(choke_s(g_bar, 10**la0_b, s_b))
rho, p = spearmanr(np.log10(g_bar), resid_b)
print(f"  residual vs log10(g_bar), s free : rho={rho:.4f}, p={p:.2e}  (was rho=-0.2735, p=1.5e-47 at s=1)")

out = dict(a0=10**la0_b, s=s_b, rms_s_free=rms_b, rms_s1=rms_s1, rms_mcgaugh=rms_mcgaugh,
           resid_trend_rho=rho, resid_trend_p=p)
json.dump(out, open(f"{D}/domain_K_transition_shape_results.json","w"), indent=2)
print(f"\n  -> {D}\\domain_K_transition_shape_results.json")
