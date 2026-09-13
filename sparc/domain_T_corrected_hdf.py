"""
DOMAIN T -- corrected coupled HDF continuum, per the audit consensus
(Claude's Domain S audit + Gemini's cross-check):

  u(r) = rho_excess(r)/rho_gal,  0<=u<1   [galaxy-scale state variable]
  rho_HDF(r) = rho_bg + rho_gal*u(r)
  dM_HDF/dr = 4*pi*r^2*rho_gal*u(r)
  g_pred(r) = G*(M_bar(<r)+M_HDF(<r))/r^2
  du/dr = -(rho_bg+rho_gal*u)*g_pred*(1-u) / (rho_gal*c_s0^2)   [F(u)=1/(1-u),
      SAME functional form as the compact EOS, but applied to u -- NOT
      normalized by rho_max, which no longer appears in the ODE at all]

  chi_compact(r) = rho_gal*u(r) / (rho_max-rho_bg)   -- DIAGNOSTIC ONLY,
      reported to confirm it stays far below 1 (remote consistency bound),
      never fed back into the dynamics.

Boundary condition: NOT an arbitrary universal u0. u(r_min) = U0_TINY (a
fixed, non-fitted, near-zero value -- "starts from negligible diffuse
excess, let the coupled self-gravity build the profile"). Per the known
robustness of the isothermal-sphere problem, the OUTER/large-r attractor
solution should be largely independent of this choice as long as it is
small; this is checked explicitly below (three tiny starting values
compared) before trusting the result.

Only 2 free global parameters now: rho_gal, c_s0. u0 is fixed, not fit.
"""
import numpy as np, json, time
from scipy.optimize import minimize
from scipy.integrate import solve_ivp
from scipy import stats

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
KMS = 1.0e3
UPS_D, UPS_B = 0.5, 0.7
G = 6.674e-11
RHO_MAX = 4.6e10
RHO_BG = 0.0
U0_TINY = 1e-6   # fixed, not fitted

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

def sigmoid(y): return 1.0/(1.0+np.exp(-y))
def logit(u): return np.log(u/(1.0-u))

def load():
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
    gal_data = {}
    for g in galaxies:
        gm = (name == g)
        r_kpc = R[gm]; gobs = g_obs_all[gm]; gbar = g_bar_all[gm]
        order = np.argsort(r_kpc)
        r_kpc, gobs, gbar = r_kpc[order], gobs[order], gbar[order]
        if len(r_kpc) < 3: continue
        gal_data[g] = dict(r=r_kpc*KPC, gobs=gobs, gbar=gbar, L36=L36.get(g, np.nan))
    return gal_data, galaxies

gal_data, galaxies = load()
rng = np.random.default_rng(7)
shuffled = galaxies.copy(); rng.shuffle(shuffled)
n_train = int(len(shuffled)*0.7)
train_gal = set(shuffled[:n_train]); hold_gal = set(shuffled[n_train:])
print(f"train galaxies: {len(train_gal)}, holdout galaxies: {len(hold_gal)}")

def integrate_galaxy(gd, rho_gal, c_s0, u0=U0_TINY):
    r = gd["r"]; gbar = gd["gbar"]
    Mbar = gbar * r**2 / G
    def Mbar_of_r(rr): return np.interp(rr, r, Mbar)
    r_min, r_max = r[0], r[-1]
    y0 = logit(np.clip(u0, 1e-12, 1-1e-12))

    def rhs(rr, state):
        MHDF, y = state
        u = sigmoid(np.clip(y, -60, 60))
        Mb = Mbar_of_r(rr)
        gpred = G*(Mb+MHDF)/rr**2
        dMHDF = 4*np.pi*rr**2*rho_gal*u
        du = -(RHO_BG+rho_gal*u)*gpred*(1-u) / (rho_gal*c_s0**2)
        dy = du/max(u*(1-u), 1e-300)
        return [dMHDF, dy]

    try:
        sol = solve_ivp(rhs, [r_min, r_max], [0.0, y0], t_eval=r, method="RK45",
                         rtol=1e-8, atol=1e-6, max_step=(r_max-r_min)/100)
    except Exception:
        return None
    if not sol.success: return None
    MHDF_arr = sol.y[0]
    u_arr = sigmoid(np.clip(sol.y[1], -60, 60))
    gpred_arr = G*(Mbar+MHDF_arr)/r**2
    chi_compact = rho_gal*u_arr/(RHO_MAX-RHO_BG)
    physical = bool(np.all((u_arr > 0) & (u_arr < 1)) and np.all(np.isfinite(MHDF_arr)))
    return dict(MHDF=MHDF_arr, u=u_arr, gpred=gpred_arr, Mbar=Mbar, r=r,
                physical=physical, chi_compact=chi_compact)

# --- robustness check: does the outer solution depend on the tiny starting u0? ---
print("\n=== boundary-independence check (3 tiny u0 values, one galaxy) ===")
test_g = list(gal_data.keys())[0]
for u0_test in [1e-8, 1e-6, 1e-4]:
    res = integrate_galaxy(gal_data[test_g], rho_gal=1e-22, c_s0=5e4, u0=u0_test)
    if res:
        print(f"  u0={u0_test:.0e}: outer u={res['u'][-1]:.6f}, outer M_HDF={res['MHDF'][-1]:.4e} kg")

def train_objective(params):
    lrho_gal, lcs0 = params
    rho_gal = 10**lrho_gal; c_s0 = 10**lcs0
    resid2 = []
    for g in train_gal:
        gd = gal_data.get(g)
        if gd is None: continue
        res = integrate_galaxy(gd, rho_gal, c_s0)
        if res is None or not res["physical"] or np.any(res["gpred"] <= 0):
            resid2.append(np.full(len(gd["r"]), 4.0)); continue
        resid2.append((np.log10(gd["gobs"]) - np.log10(res["gpred"]))**2)
    if not resid2: return 1e9
    return float(np.mean(np.concatenate(resid2)))

print("\n=== fitting (rho_gal, c_s0) jointly on TRAIN only ===")
t0 = time.time()
best = minimize(train_objective, x0=[np.log10(1e-22), np.log10(5e4)], method="Nelder-Mead",
                 options=dict(xatol=1e-4, fatol=1e-8, maxiter=300, maxfev=300))
lrho_gal, lcs0 = best.x
rho_gal = 10**lrho_gal; c_s0 = 10**lcs0
print(f"fit took {time.time()-t0:.1f}s, converged={best.success}, nit={best.nit}")
print(f"rho_gal = {rho_gal:.4e} kg/m^3")
print(f"c_s0    = {c_s0:.4e} m/s  (predicts v_flat=sqrt(2)*c_s0={np.sqrt(2)*c_s0/1e3:.2f} km/s if SIS branch reached)")

def eval_set(gal_set):
    resid_list, outer_MHDF, outer_slope, outer_vflat, Mbar_last, chi_compact_max = [], [], [], [], [], []
    all_physical = True
    for g in gal_set:
        gd = gal_data.get(g)
        if gd is None: continue
        res = integrate_galaxy(gd, rho_gal, c_s0)
        if res is None or not res["physical"]:
            all_physical = False; continue
        resid_list.append(np.log10(gd["gobs"]) - np.log10(res["gpred"]))
        outer_MHDF.append(res["MHDF"][-1])
        Mbar_last.append(res["Mbar"][-1])
        chi_compact_max.append(res["chi_compact"].max())
        if len(res["r"]) >= 5:
            rr, uu = res["r"][-5:], res["u"][-5:]
            if np.all(uu > 0):
                slope = np.polyfit(np.log(rr), np.log(uu), 1)[0]
                outer_slope.append(slope)
        outer_vflat.append(np.sqrt(res["gpred"][-1]*res["r"][-1]))
    rms = np.sqrt(np.mean(np.concatenate(resid_list)**2)) if resid_list else float("nan")
    return dict(rms=rms, all_physical=all_physical, outer_MHDF=np.array(outer_MHDF),
                outer_slope=np.array(outer_slope), outer_vflat=np.array(outer_vflat),
                Mbar_last=np.array(Mbar_last), chi_compact_max=np.array(chi_compact_max))

print("\n=== TRAIN evaluation ===")
tr = eval_set(train_gal)
print(f"train rms = {tr['rms']:.4f} dex, all physical={tr['all_physical']}")
print(f"outer alpha_u (rho_excess slope): median={np.median(tr['outer_slope']):.3f} (target -2)")
print(f"max chi_compact (remote consistency check, should be <<1): {tr['chi_compact_max'].max():.4e}")

print("\n=== HOLDOUT evaluation ===")
ho = eval_set(hold_gal)
print(f"holdout rms = {ho['rms']:.4f} dex, all physical={ho['all_physical']}")
print(f"outer alpha_u (rho_excess slope): median={np.median(ho['outer_slope']):.3f} (target -2)")
print(f"max chi_compact (remote consistency check, should be <<1): {ho['chi_compact_max'].max():.4e}")

all_vflat = np.concatenate([tr["outer_vflat"], ho["outer_vflat"]])
all_Mbar  = np.concatenate([tr["Mbar_last"], ho["Mbar_last"]])
valid = (all_vflat > 0) & (all_Mbar > 0) & np.isfinite(all_vflat) & np.isfinite(all_Mbar)
slope_btfr = None
if valid.sum() >= 10:
    slope_btfr, intercept_btfr, r_btfr, p_btfr, se_btfr = stats.linregress(
        np.log10(all_vflat[valid]), np.log10(all_Mbar[valid]))
    print(f"\n=== BTFR check ===")
    print(f"log(M_bar) = {slope_btfr:.3f}*log(v_flat) + {intercept_btfr:.3f} (r={r_btfr:.3f}, n={valid.sum()})")

print(f"\n=== comparison to prior baselines ===")
print(f"  plain RAR:        train=0.1338, holdout=0.1298 dex")
print(f"  choke n=1/2:      train=0.1380, holdout=0.1387 dex")
print(f"  Domain S (buggy): train=0.2897, holdout=0.3293 dex")
print(f"  Domain T (fixed): train={tr['rms']:.4f}, holdout={ho['rms']:.4f} dex")

out = dict(rho_gal=rho_gal, c_s0=c_s0, u0_fixed=U0_TINY,
           train_rms=tr["rms"], holdout_rms=ho["rms"],
           train_all_physical=tr["all_physical"], holdout_all_physical=ho["all_physical"],
           train_outer_slope_median=float(np.median(tr["outer_slope"])) if len(tr["outer_slope"]) else None,
           holdout_outer_slope_median=float(np.median(ho["outer_slope"])) if len(ho["outer_slope"]) else None,
           btfr_slope=float(slope_btfr) if slope_btfr is not None else None,
           predicted_v_flat_kms=float(np.sqrt(2)*c_s0/1e3))
json.dump(out, open(f"{D}/domain_T_results.json","w"), indent=2)
print(f"\nresults -> {D}\\domain_T_results.json")
