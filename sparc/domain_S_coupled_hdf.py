"""
DOMAIN S -- coupled HDF continuum calculation, per the corrected
specification: rho_gal (diffuse galactic HDF scale) is NOT rho_max
(compact-object saturation ceiling, 4.6e10 kg/m^3, kept separate and only
entering as the denominator scale in the stiffening term). ODE starts at
a positive r_min (first tabulated SPARC radius per galaxy), chi kept
strictly in (0,1) via a sigmoid/logit reparametrization (never clipped).
Pi(r)=1 (no-permeability baseline) for this run, per instruction.

DECLARED GAPS (not specified in the prompt, filled with the simplest
literal choice, flagged explicitly rather than silently assumed):
  f(chi) = chi            [simplest choice consistent with f[chi]->0 at
                            chi=0 and ->1 at chi=1; not otherwise specified]
  rho_bg = 0               [not listed among the 3 globally-fit parameters
                            (rho_gal, c_s0, chi0); treated as negligible
                            baseline rather than a 4th free parameter]

Equations (exactly as given):
  dM_HDF/dr = 4*pi*r^2*rho_gal*f(chi)*Pi(r)
  g_pred(r) = G*[M_bar(<r)+M_HDF(<r)]/r^2
  dchi/dr = -[rho_bg+rho_gal*f(chi)]*g_pred(r) / [(rho_max-rho_bg)*c_s0^2*F(chi)]
  F(chi) = 1/(1-chi)
"""
import numpy as np, json, time
from scipy.optimize import minimize
from scipy.integrate import solve_ivp
from scipy import stats

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19  # m
KMS = 1.0e3                  # m/s
UPS_D, UPS_B = 0.5, 0.7
G = 6.674e-11                # m^3 kg^-1 s^-2
RHO_MAX = 4.6e10             # kg/m^3, given -- compact-object ceiling, NOT galaxy-scale amplitude
RHO_BG = 0.0                 # declared gap, see docstring

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

t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name","i","Qual","Vflat","Dist","L3.6","SBdisk","MHI"])
t2 = read_vizier_tsv(f"{D}/vizier_t2.txt", ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
inc  = {n:i for n,i in zip(t1["Name"], t1["i"])}
qual = {n:q for n,q in zip(t1["Name"], t1["Qual"])}
L36  = {n:v for n,v in zip(t1["Name"], t1["L3.6"])}

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
g_obs_all = Vo**2 / R * conv
Vbar2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
g_bar_all = Vbar2 / R * conv
ok = (g_bar_all > 0) & (g_obs_all > 0)
g_obs_all, g_bar_all, name, R = g_obs_all[ok], g_bar_all[ok], name[ok], R[ok]

galaxies = sorted(set(name))
rng = np.random.default_rng(7)   # SAME seed/split as Domain M, N, R
shuffled = galaxies.copy(); rng.shuffle(shuffled)
n_train = int(len(shuffled)*0.7)
train_gal = set(shuffled[:n_train]); hold_gal = set(shuffled[n_train:])
print(f"train galaxies: {len(train_gal)}, holdout galaxies: {len(hold_gal)}")

# group per-galaxy arrays, sorted by radius, r in meters
gal_data = {}
for g in galaxies:
    gm = (name == g)
    r_kpc = R[gm]; gobs = g_obs_all[gm]; gbar = g_bar_all[gm]
    order = np.argsort(r_kpc)
    r_kpc, gobs, gbar = r_kpc[order], gobs[order], gbar[order]
    if len(r_kpc) < 3: continue
    r_m = r_kpc * KPC
    gal_data[g] = dict(r=r_m, gobs=gobs, gbar=gbar, L36=L36.get(g, np.nan))

def f_chi(chi): return chi
def sigmoid(y): return 1.0/(1.0+np.exp(-y))
def logit(chi): return np.log(chi/(1.0-chi))

def integrate_galaxy(gd, rho_gal, c_s0, chi0):
    r = gd["r"]; gbar = gd["gbar"]
    Mbar = gbar * r**2 / G
    def Mbar_of_r(rr):
        return np.interp(rr, r, Mbar)
    r_min, r_max = r[0], r[-1]
    y0 = logit(np.clip(chi0, 1e-9, 1-1e-9))

    def rhs(rr, state):
        MHDF, y = state
        chi = sigmoid(np.clip(y, -60, 60))
        Mb = Mbar_of_r(rr)
        gpred = G*(Mb+MHDF)/rr**2
        dMHDF = 4*np.pi*rr**2*rho_gal*f_chi(chi)
        dchi = -(RHO_BG+rho_gal*f_chi(chi))*gpred*(1-chi) / ((RHO_MAX-RHO_BG)*c_s0**2)
        dy = dchi/max(chi*(1-chi), 1e-300)
        return [dMHDF, dy]

    try:
        sol = solve_ivp(rhs, [r_min, r_max], [0.0, y0], t_eval=r, method="RK45",
                         rtol=1e-7, atol=1e-6, max_step=(r_max-r_min)/50)
    except Exception:
        return None
    if not sol.success:
        return None
    MHDF_arr = sol.y[0]
    chi_arr = sigmoid(np.clip(sol.y[1], -60, 60))
    gpred_arr = G*(Mbar+MHDF_arr)/r**2
    physical = bool(np.all((chi_arr > 0) & (chi_arr < 1)) and np.all(np.isfinite(MHDF_arr)))
    return dict(MHDF=MHDF_arr, chi=chi_arr, gpred=gpred_arr, Mbar=Mbar, r=r, physical=physical)

def train_objective(params):
    lrho_gal, lcs0, y0 = params
    rho_gal = 10**lrho_gal; c_s0 = 10**lcs0; chi0 = sigmoid(y0)
    if not (0 < chi0 < 1): return 1e9
    resid2 = []
    for g in train_gal:
        gd = gal_data.get(g)
        if gd is None: continue
        res = integrate_galaxy(gd, rho_gal, c_s0, chi0)
        if res is None or not res["physical"] or np.any(res["gpred"] <= 0):
            resid2.append(np.full(len(gd["r"]), 4.0))  # penalty ~ 2 dex^2 per point
            continue
        r = np.log10(gd["gobs"]) - np.log10(res["gpred"])
        resid2.append(r**2)
    if not resid2: return 1e9
    return float(np.mean(np.concatenate(resid2)))

print("=== fitting (rho_gal, c_s0, chi0) jointly on TRAIN only ===")
t0 = time.time()
x0 = [np.log10(1e-22), np.log10(3e4), logit(0.3)]
best = minimize(train_objective, x0=x0, method="Nelder-Mead",
                 options=dict(xatol=1e-4, fatol=1e-8, maxiter=400, maxfev=400))
lrho_gal, lcs0, y0 = best.x
rho_gal = 10**lrho_gal; c_s0 = 10**lcs0; chi0 = sigmoid(y0)
print(f"fit took {time.time()-t0:.1f}s, converged={best.success}, nit={best.nit}")
print(f"rho_gal = {rho_gal:.4e} kg/m^3")
print(f"c_s0    = {c_s0:.4e} m/s")
print(f"chi0    = {chi0:.6f}  (chi at r_min)")

def eval_set(gal_set):
    resid_list = []
    all_physical = True
    outer_MHDF = []
    outer_slope = []
    outer_vflat = []
    Mbar_last = []
    for g in gal_set:
        gd = gal_data.get(g)
        if gd is None: continue
        res = integrate_galaxy(gd, rho_gal, c_s0, chi0)
        if res is None or not res["physical"]:
            all_physical = False
            continue
        r = np.log10(gd["gobs"]) - np.log10(res["gpred"])
        resid_list.append(r)
        outer_MHDF.append(res["MHDF"][-1])
        Mbar_last.append(res["Mbar"][-1])
        # outer log-log slope of rho_excess ~ f(chi) between last two points
        if len(res["r"]) >= 2:
            rr = res["r"][-2:]; cc = f_chi(res["chi"][-2:])
            if cc[0] > 0 and cc[1] > 0:
                slope = np.log(cc[1]/cc[0])/np.log(rr[1]/rr[0])
                outer_slope.append(slope)
        vflat_pred = np.sqrt(res["gpred"][-1]*res["r"][-1])
        outer_vflat.append(vflat_pred)
    rms = np.sqrt(np.mean(np.concatenate(resid_list)**2)) if resid_list else float("nan")
    return dict(rms=rms, all_physical=all_physical, outer_MHDF=np.array(outer_MHDF),
                outer_slope=np.array(outer_slope), outer_vflat=np.array(outer_vflat),
                Mbar_last=np.array(Mbar_last))

print("\n=== TRAIN evaluation ===")
tr = eval_set(train_gal)
print(f"train rms = {tr['rms']:.4f} dex, all physical={tr['all_physical']}")
print(f"outer M_HDF: median={np.median(tr['outer_MHDF']):.4e} kg, "
      f"range=[{tr['outer_MHDF'].min():.2e}, {tr['outer_MHDF'].max():.2e}]")
print(f"outer log-log slope of rho_excess(r): median={np.median(tr['outer_slope']):.3f}")

print("\n=== HOLDOUT evaluation ===")
ho = eval_set(hold_gal)
print(f"holdout rms = {ho['rms']:.4f} dex, all physical={ho['all_physical']}")
print(f"outer M_HDF: median={np.median(ho['outer_MHDF']):.4e} kg, "
      f"range=[{ho['outer_MHDF'].min():.2e}, {ho['outer_MHDF'].max():.2e}]")
print(f"outer log-log slope of rho_excess(r): median={np.median(ho['outer_slope']):.3f}")

# BTFR slope from PREDICTED outer speeds (not observed Vflat), no a0 inserted anywhere
all_vflat = np.concatenate([tr["outer_vflat"], ho["outer_vflat"]])
all_Mbar  = np.concatenate([tr["Mbar_last"], ho["Mbar_last"]])
valid = (all_vflat > 0) & (all_Mbar > 0) & np.isfinite(all_vflat) & np.isfinite(all_Mbar)
if valid.sum() >= 10:
    slope_btfr, intercept_btfr, r_btfr, p_btfr, se_btfr = stats.linregress(
        np.log10(all_vflat[valid]), np.log10(all_Mbar[valid]))
    print(f"\n=== BTFR check (predicted v_flat vs M_bar, no a0 inserted) ===")
    print(f"log(M_bar) = {slope_btfr:.3f} * log(v_flat) + {intercept_btfr:.3f}  (r={r_btfr:.3f}, n={valid.sum()})")
else:
    slope_btfr = None
    print("insufficient valid points for BTFR check")

out = dict(
    rho_gal=rho_gal, c_s0=c_s0, chi0=chi0,
    rho_bg_assumed=RHO_BG, f_chi_form="identity: f(chi)=chi",
    train_rms=tr["rms"], train_all_physical=tr["all_physical"],
    holdout_rms=ho["rms"], holdout_all_physical=ho["all_physical"],
    train_outer_MHDF_median=float(np.median(tr["outer_MHDF"])),
    holdout_outer_MHDF_median=float(np.median(ho["outer_MHDF"])),
    train_outer_slope_median=float(np.median(tr["outer_slope"])) if len(tr["outer_slope"]) else None,
    holdout_outer_slope_median=float(np.median(ho["outer_slope"])) if len(ho["outer_slope"]) else None,
    btfr_slope=float(slope_btfr) if slope_btfr is not None else None,
)
json.dump(out, open(f"{D}/domain_S_results.json","w"), indent=2)
print(f"\nresults -> {D}\\domain_S_results.json")
