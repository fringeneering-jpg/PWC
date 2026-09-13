"""
DOMAIN U -- genuine outer-boundary shooting method, per the audit's own
"option B" (outer boundary integration, start near the diffuse baseline
and integrate inward), implemented WITHOUT any new free shooting
parameter: the analytic SIS asymptote

    u_far = c_s0^2 / (2*pi*G*rho_gal*r_far^2)

is fully determined by the SAME two global parameters (rho_gal, c_s0)
already being fit -- imposed at r_far = 50x each galaxy's own maximum
tabulated radius (genuinely remote from the real data, not close to it),
then integrated INWARD through the real baryonic mass profile down to
r_min. The slope is measured at the ACTUAL SPARC radii, not at r_far,
specifically to check whether Domain U's claimed alpha_rho~-2 is a real
emergent result there or an artifact of being close to the imposed
boundary.
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
R_FAR_MULT = 15.0   # remote boundary = 15x the galaxy's own max tabulated radius
                     # (reduced from 50x: still genuinely remote from the data,
                     # but avoids the enormous dynamic range that made the
                     # RK45 integration pathologically slow/stiff during the
                     # optimizer's wide initial exploration)

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

def load():
    t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name","i","Qual","Vflat","Dist","L3.6","SBdisk","MHI"])
    t2 = read_vizier_tsv(f"{D}/vizier_t2.txt", ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
    inc  = {n:i for n,i in zip(t1["Name"], t1["i"])}
    qual = {n:q for n,q in zip(t1["Name"], t1["Qual"])}
    L36  = {n:v for n,v in zip(t1["Name"], t1["L3.6"])}
    MHI  = {n:v for n,v in zip(t1["Name"], t1["MHI"])}
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
        gal_data[g] = dict(r=r_kpc*KPC, gobs=gobs, gbar=gbar, L36=L36.get(g, np.nan), MHI=MHI.get(g, np.nan))
    return gal_data, galaxies

gal_data, galaxies = load()
rng = np.random.default_rng(7)
shuffled = galaxies.copy(); rng.shuffle(shuffled)
n_train = int(len(shuffled)*0.7)
train_gal = set(shuffled[:n_train]); hold_gal = set(shuffled[n_train:])
print(f"train galaxies: {len(train_gal)}, holdout galaxies: {len(hold_gal)}")

def integrate_inward(gd, rho_gal, c_s0):
    r = gd["r"]; gbar = gd["gbar"]
    Mbar = gbar * r**2 / G
    Mbar_total = Mbar[-1]   # plateaus beyond the last tabulated radius
    def Mbar_of_r(rr):
        return np.where(rr <= r[-1], np.interp(rr, r, Mbar), Mbar_total)

    r_far = R_FAR_MULT * r[-1]
    u_far = c_s0**2 / (2*np.pi*G*rho_gal*r_far**2)
    if u_far <= 0 or u_far >= 1:
        return None
    MHDF_far_analytic = 4*np.pi*rho_gal*(c_s0**2/(2*np.pi*G*rho_gal))*r_far  # 2*c_s0^2/G * r_far, standard SIS enclosed mass

    def rhs(rr, state):
        MHDF, u = state
        u = np.clip(u, 1e-15, 1-1e-15)
        Mb = Mbar_of_r(rr)
        gpred = G*(Mb+MHDF)/rr**2
        dMHDF_dr = 4*np.pi*rr**2*rho_gal*u
        du_dr = -(RHO_BG+rho_gal*u)*gpred*(1-u) / (rho_gal*c_s0**2)
        return [dMHDF_dr, du_dr]

    r_min = r[0]
    state_far = [MHDF_far_analytic, u_far]
    t_eval = np.sort(r)[::-1]  # decreasing, matching integration direction
    try:
        sol = solve_ivp(rhs, [r_far, r_min], state_far, t_eval=t_eval, method="RK45",
                         rtol=1e-6, atol=1e-10, max_step=(r_far-r_min)/100)
    except Exception:
        return None
    if not sol.success:
        return None
    # re-sort back to increasing r to match gd["r"] order
    order = np.argsort(sol.t)
    r_out = sol.t[order]
    MHDF_out = sol.y[0][order]
    u_out = sol.y[1][order]
    if not np.allclose(r_out, r, rtol=1e-6):
        # t_eval ordering mismatch guard
        MHDF_out = np.interp(r, r_out, MHDF_out)
        u_out = np.interp(r, r_out, u_out)
    gpred = G*(Mbar+MHDF_out)/r**2
    physical = bool(np.all((u_out > 0) & (u_out < 1)) & np.all(np.isfinite(MHDF_out)) & np.all(gpred>0))
    return dict(MHDF=MHDF_out, u=u_out, gpred=gpred, Mbar=Mbar, r=r, physical=physical, u_far=u_far, r_far=r_far)

print("\n=== sanity check: does integrating inward from the analytic SIS boundary")
print("    reproduce a sensible profile for one galaxy, before any fitting? ===")
test_g = list(gal_data.keys())[0]
res_test = integrate_inward(gal_data[test_g], rho_gal=1e-21, c_s0=1e5)
if res_test:
    print(f"galaxy={test_g}, physical={res_test['physical']}, u range=[{res_test['u'].min():.3e},{res_test['u'].max():.3e}]")
else:
    print("integration failed for sanity check")

def train_objective(params):
    lrho_gal, lcs0 = params
    if not (-25 <= lrho_gal <= -18) or not (3.5 <= lcs0 <= 6.0):
        return 1e9  # keep the optimizer out of pathologically stiff/invalid regions
    rho_gal = 10**lrho_gal; c_s0 = 10**lcs0
    resid2 = []
    for g in train_gal:
        gd = gal_data.get(g)
        if gd is None: continue
        res = integrate_inward(gd, rho_gal, c_s0)
        if res is None or not res["physical"]:
            resid2.append(np.full(len(gd["r"]), 4.0)); continue
        resid2.append((np.log10(gd["gobs"]) - np.log10(res["gpred"]))**2)
    if not resid2: return 1e9
    return float(np.mean(np.concatenate(resid2)))

print("\n=== fitting (rho_gal, c_s0) jointly on TRAIN, inward-shooting method ===")
t0 = time.time()
best = minimize(train_objective, x0=[np.log10(1e-21), np.log10(1e5)], method="Nelder-Mead",
                 options=dict(xatol=1e-4, fatol=1e-8, maxiter=300, maxfev=300))
lrho_gal, lcs0 = best.x
rho_gal = 10**lrho_gal; c_s0 = 10**lcs0
print(f"fit took {time.time()-t0:.1f}s, converged={best.success}, nit={best.nit}")
print(f"rho_gal = {rho_gal:.4e} kg/m^3, c_s0 = {c_s0:.4e} m/s (v_flat=sqrt(2)*c_s0={np.sqrt(2)*c_s0/1e3:.2f} km/s)")

def eval_set(gal_set):
    resid_list, outer_slope, outer_vflat, Mbar_last, gal_resid_mean, gal_gasfrac = [], [], [], [], [], []
    all_physical = True
    for g in gal_set:
        gd = gal_data.get(g)
        if gd is None: continue
        res = integrate_inward(gd, rho_gal, c_s0)
        if res is None or not res["physical"]:
            all_physical = False; continue
        r_res = np.log10(gd["gobs"]) - np.log10(res["gpred"])
        resid_list.append(r_res)
        gal_resid_mean.append(np.mean(r_res))
        l36 = gd.get("L36", np.nan); mhi = gd.get("MHI", np.nan)
        gal_gasfrac.append((mhi/l36) if (np.isfinite(l36) and l36>0 and np.isfinite(mhi) and mhi>0) else np.nan)
        Mbar_last.append(res["Mbar"][-1])
        if len(res["r"]) >= 5:
            rr, uu = res["r"][-5:], res["u"][-5:]
            if np.all(uu>0):
                outer_slope.append(np.polyfit(np.log(rr), np.log(uu), 1)[0])
        outer_vflat.append(np.sqrt(res["gpred"][-1]*res["r"][-1]))
    rms = np.sqrt(np.mean(np.concatenate(resid_list)**2)) if resid_list else float("nan")
    return dict(rms=rms, all_physical=all_physical, outer_slope=np.array(outer_slope),
                outer_vflat=np.array(outer_vflat), Mbar_last=np.array(Mbar_last),
                gal_resid_mean=np.array(gal_resid_mean), gal_gasfrac=np.array(gal_gasfrac))

print("\n=== TRAIN evaluation ===")
tr = eval_set(train_gal)
print(f"train rms = {tr['rms']:.4f} dex, all physical={tr['all_physical']}")
print(f"outer alpha (rho_excess slope, at REAL data radii, NOT at r_far): median={np.median(tr['outer_slope']):.3f} (target -2)")

print("\n=== HOLDOUT evaluation ===")
ho = eval_set(hold_gal)
print(f"holdout rms = {ho['rms']:.4f} dex, all physical={ho['all_physical']}")
print(f"outer alpha (rho_excess slope, at REAL data radii, NOT at r_far): median={np.median(ho['outer_slope']):.3f} (target -2)")

all_vflat = np.concatenate([tr["outer_vflat"], ho["outer_vflat"]])
all_Mbar  = np.concatenate([tr["Mbar_last"], ho["Mbar_last"]])
valid = (all_vflat>0)&(all_Mbar>0)&np.isfinite(all_vflat)&np.isfinite(all_Mbar)
if valid.sum()>=10:
    slope_btfr, intercept, rb, pb, seb = stats.linregress(np.log10(all_vflat[valid]), np.log10(all_Mbar[valid]))
    print(f"\nBTFR: slope={slope_btfr:.3f} (literature ~3.5-4), r={rb:.3f}, n={valid.sum()}")
else:
    slope_btfr = None

all_resid = np.concatenate([tr["gal_resid_mean"], ho["gal_resid_mean"]])
all_gf = np.concatenate([tr["gal_gasfrac"], ho["gal_gasfrac"]])
vgf = np.isfinite(all_gf) & np.isfinite(all_resid)
if vgf.sum()>=10:
    rho_gf, p_gf = stats.spearmanr(np.log10(all_gf[vgf]), all_resid[vgf])
    print(f"residual vs log10(gas fraction): rho={rho_gf:+.3f}, p={p_gf:.4f}  (Domain M/N/R found rho=0.166,p=0.042)")

print(f"\n=== comparison ===")
print(f"  plain RAR:        holdout=0.1298 dex")
print(f"  choke n=1/2:      holdout=0.1387 dex")
print(f"  Domain S (buggy): holdout=0.3293 dex")
print(f"  Domain T (IVP):   holdout=0.2801 dex")
print(f"  Domain U (this):  holdout={ho['rms']:.4f} dex")

out = dict(rho_gal=rho_gal, c_s0=c_s0, train_rms=tr["rms"], holdout_rms=ho["rms"],
           train_outer_slope=float(np.median(tr["outer_slope"])) if len(tr["outer_slope"]) else None,
           holdout_outer_slope=float(np.median(ho["outer_slope"])) if len(ho["outer_slope"]) else None,
           btfr_slope=float(slope_btfr) if slope_btfr else None,
           v_flat_pred_kms=float(np.sqrt(2)*c_s0/1e3))
json.dump(out, open(f"{D}/domain_U_results.json","w"), indent=2)
print(f"\nresults -> {D}\\domain_U_results.json")
