"""
DOMAIN U2 -- forensic-audited rebuild of Domain U, per the requested review.

Fixes vs Domain U:
  - u is bounded via sigmoid(y) (as in Domain S/T-IVP), so the SOLVER STATE
    itself can never reach or exceed 1 -- not just an in-RHS clip.
  - Optimizer penalty added if too many training galaxies saturate
    (max(u) >= 0.99) for a given parameter trial -- keeps the search out
    of the pathological near-saturation regime rather than silently
    reporting it as a valid rotation-curve prediction.
  - Full per-galaxy diagnostics exported: name, r_out, M_bar_total, u_min,
    u_max, M_HDF(r_out), v_pred(r_out), v_obs(r_out), valid flag, failure
    reason.
  - Holdout RMS and BTFR reported TWICE: (A) all attempted galaxies,
    (B) valid, non-saturated (max(u)<0.99) galaxies only.
  - Raw log10(M_bar), log10(v_flat) arrays printed (min/max + 10 sample
    rows) before any BTFR regression is trusted.

Note on the du/dr=-2u/r question: this implementation does NOT impose that
slope directly as a constraint. It sets u(r_far) to the analytic SIS value
(u_far = c_s0^2/(2*pi*G*rho_gal*r_far^2)) and lets the ODE's own RHS
determine du/dr from there -- at r_far specifically, that RHS numerically
evaluates close to -2u/r ONLY if the local solution is genuinely on/near
the pure-HDF SIS branch (M_bar negligible relative to M_HDF there). This
is checked explicitly below (is M_bar/M_HDF small at r_far?), rather than
assumed.
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
RHO_BG = 0.0
R_FAR_MULT = 15.0
SATURATION_THRESH = 0.99

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

def sigmoid(y): return 1.0/(1.0+np.exp(-y))
def logit(u): return np.log(u/(1.0-u))

def integrate_inward(gd, rho_gal, c_s0):
    r = gd["r"]; gbar = gd["gbar"]
    Mbar = gbar * r**2 / G
    Mbar_total = Mbar[-1]
    def Mbar_of_r(rr):
        return np.where(rr <= r[-1], np.interp(rr, r, Mbar), Mbar_total)

    r_far = R_FAR_MULT * r[-1]
    u_far = c_s0**2 / (2*np.pi*G*rho_gal*r_far**2)
    if not (0 < u_far < 0.5):   # keep the STARTING point itself well inside the bounded regime
        return dict(valid=False, reason=f"u_far out of range ({u_far:.3e})")
    MHDF_far = 2*c_s0**2/G * r_far   # SIS enclosed mass at r_far
    Mb_far = Mbar_of_r(r_far)
    y0 = logit(u_far)

    def rhs(rr, state):
        MHDF, y = state
        u = sigmoid(np.clip(y, -60, 60))
        Mb = Mbar_of_r(rr)
        gpred = G*(Mb+MHDF)/rr**2
        dMHDF_dr = 4*np.pi*rr**2*rho_gal*u
        du_dr = -(RHO_BG+rho_gal*u)*gpred*(1-u) / (rho_gal*c_s0**2)
        dy_dr = du_dr/max(u*(1-u), 1e-300)
        return [dMHDF_dr, dy_dr]

    r_min = r[0]
    t_eval = np.sort(r)[::-1]
    try:
        sol = solve_ivp(rhs, [r_far, r_min], [MHDF_far, y0], t_eval=t_eval, method="RK45",
                         rtol=1e-6, atol=1e-10, max_step=(r_far-r_min)/100)
    except Exception as e:
        return dict(valid=False, reason=f"exception: {e}")
    if not sol.success:
        return dict(valid=False, reason=f"solve_ivp failed: {sol.message}")

    order = np.argsort(sol.t)
    r_out = sol.t[order]
    if not np.allclose(r_out, r, rtol=1e-6):
        MHDF_out = np.interp(r, r_out, sol.y[0][order])
        y_out = np.interp(r, r_out, sol.y[1][order])
    else:
        MHDF_out = sol.y[0][order]; y_out = sol.y[1][order]
    u_out = sigmoid(np.clip(y_out, -60, 60))
    gpred = G*(Mbar+MHDF_out)/r**2

    reasons = []
    if not np.all(np.isfinite(MHDF_out)): reasons.append("non-finite M_HDF")
    if not np.all(np.isfinite(gpred)) or np.any(gpred<=0): reasons.append("non-finite/non-positive g_pred")
    if u_out.max() >= SATURATION_THRESH: reasons.append(f"saturated (max u={u_out.max():.4f})")
    if not np.all(np.diff(r)>0): reasons.append("radius not monotonic")

    valid = (len(reasons)==0)
    m_b_over_hdf_at_far = Mb_far/MHDF_far if MHDF_far>0 else float("nan")
    return dict(valid=valid, reason="; ".join(reasons) if reasons else "ok",
                MHDF=MHDF_out, u=u_out, gpred=gpred, Mbar=Mbar, r=r,
                u_far=u_far, r_far=r_far, m_b_over_hdf_at_far=m_b_over_hdf_at_far)

print("\n=== boundary-condition check: is M_bar/M_HDF small at r_far (i.e. genuinely on pure-SIS branch there)? ===")
res0 = integrate_inward(gal_data[list(gal_data.keys())[0]], rho_gal=1e-21, c_s0=1e5)
print(f"  sample galaxy: valid={res0.get('valid')}, M_bar/M_HDF at r_far = {res0.get('m_b_over_hdf_at_far'):.3e}")

def train_objective(params):
    lrho_gal, lcs0 = params
    if not (-25 <= lrho_gal <= -18) or not (3.5 <= lcs0 <= 6.0):
        return 1e9
    rho_gal = 10**lrho_gal; c_s0 = 10**lcs0
    resid2 = []
    n_saturated = 0
    n_total = 0
    for g in train_gal:
        gd = gal_data.get(g)
        if gd is None: continue
        res = integrate_inward(gd, rho_gal, c_s0)
        n_total += 1
        if not res["valid"]:
            resid2.append(np.full(len(gd["r"]), 4.0))
            if "saturated" in res["reason"]: n_saturated += 1
            continue
        resid2.append((np.log10(gd["gobs"]) - np.log10(res["gpred"]))**2)
    if not resid2: return 1e9
    penalty = 5.0 * (n_saturated/max(n_total,1))**2  # discourage saturation-heavy regions
    return float(np.mean(np.concatenate(resid2))) + penalty

print("\n=== fitting (rho_gal, c_s0) jointly on TRAIN, with saturation penalty ===")
t0 = time.time()
best = minimize(train_objective, x0=[np.log10(1e-21), np.log10(1e5)], method="Nelder-Mead",
                 options=dict(xatol=1e-4, fatol=1e-8, maxiter=250, maxfev=250))
lrho_gal, lcs0 = best.x
rho_gal = 10**lrho_gal; c_s0 = 10**lcs0
print(f"fit took {time.time()-t0:.1f}s, converged={best.success}, nit={best.nit}")
print(f"rho_gal = {rho_gal:.4e} kg/m^3, c_s0 = {c_s0:.4e} m/s (v_flat=sqrt(2)*c_s0={np.sqrt(2)*c_s0/1e3:.2f} km/s)")

def full_eval(gal_set, label):
    rows = []
    for g in gal_set:
        gd = gal_data.get(g)
        if gd is None: continue
        res = integrate_inward(gd, rho_gal, c_s0)
        l36 = gd.get("L36", np.nan); mhi = gd.get("MHI", np.nan)
        gasfrac = (mhi/l36) if (np.isfinite(l36) and l36>0 and np.isfinite(mhi) and mhi>0) else np.nan
        if not res["valid"]:
            rows.append(dict(name=g, valid=False, reason=res["reason"],
                              r_out=gd["r"][-1]/KPC, Mbar_total=gd["gbar"][-1]*gd["r"][-1]**2/G,
                              u_min=None, u_max=None, MHDF_out=None, v_pred=None,
                              v_obs=np.sqrt(gd["gobs"][-1]*gd["r"][-1]), gasfrac=gasfrac))
            continue
        v_pred = np.sqrt(res["gpred"][-1]*res["r"][-1])
        v_obs = np.sqrt(gd["gobs"][-1]*gd["r"][-1])
        rows.append(dict(name=g, valid=True, reason="ok",
                          r_out=res["r"][-1]/KPC, Mbar_total=res["Mbar"][-1],
                          u_min=float(res["u"].min()), u_max=float(res["u"].max()),
                          MHDF_out=float(res["MHDF"][-1]), v_pred=float(v_pred), v_obs=float(v_obs),
                          resid_log_g=(np.log10(gd["gobs"])-np.log10(res["gpred"])).tolist(),
                          gasfrac=gasfrac))
    return rows

print("\n=== full per-galaxy diagnostic export ===")
rows_train = full_eval(train_gal, "train")
rows_hold = full_eval(hold_gal, "holdout")
all_rows = rows_train + rows_hold
n_valid = sum(1 for r_ in all_rows if r_["valid"])
print(f"total galaxies attempted: {len(all_rows)}, valid (non-saturated, finite): {n_valid}")
for r_ in all_rows:
    if not r_["valid"]:
        print(f"  INVALID: {r_['name']}: {r_['reason']}")

json.dump(dict(train=rows_train, holdout=rows_hold), open(f"{D}/domain_U2_per_galaxy.json","w"), indent=2)

def rms_and_btfr(rows, only_valid):
    use = [r_ for r_ in rows if (r_["valid"] or not only_valid)]
    resid_all = []
    vflat, mbar = [], []
    for r_ in use:
        if r_["valid"]:
            resid_all.extend(r_["resid_log_g"])
            vflat.append(r_["v_pred"]); mbar.append(r_["Mbar_total"])
        elif not only_valid:
            resid_all.append(4.0)  # penalty residual for invalid, counted in the "all attempted" version
    rms = np.sqrt(np.mean(np.array(resid_all)**2)) if resid_all else float("nan")
    return rms, np.array(vflat), np.array(mbar)

print("\n=== (A) ALL ATTEMPTED GALAXIES ===")
rms_tr_all, vf_tr_all, mb_tr_all = rms_and_btfr(rows_train, only_valid=False)
rms_ho_all, vf_ho_all, mb_ho_all = rms_and_btfr(rows_hold, only_valid=False)
print(f"train rms (all) = {rms_tr_all:.4f} dex, holdout rms (all) = {rms_ho_all:.4f} dex")

print("\n=== (B) VALID (NON-SATURATED) GALAXIES ONLY ===")
rms_tr_v, vf_tr_v, mb_tr_v = rms_and_btfr(rows_train, only_valid=True)
rms_ho_v, vf_ho_v, mb_ho_v = rms_and_btfr(rows_hold, only_valid=True)
print(f"train rms (valid only) = {rms_tr_v:.4f} dex, holdout rms (valid only) = {rms_ho_v:.4f} dex")
print(f"n valid: train={len(vf_tr_v)}/{len(rows_train)}, holdout={len(vf_ho_v)}/{len(rows_hold)}")

all_vf = np.concatenate([vf_tr_v, vf_ho_v])
all_mb = np.concatenate([mb_tr_v, mb_ho_v])
valid_btfr = (all_vf>0)&(all_mb>0)&np.isfinite(all_vf)&np.isfinite(all_mb)
print(f"\n=== BTFR audit (valid-only galaxies) ===")
lv = np.log10(all_vf[valid_btfr]); lm = np.log10(all_mb[valid_btfr])
print(f"log10(v_flat[m/s]) range: [{lv.min():.3f}, {lv.max():.3f}]")
print(f"log10(M_bar[kg])   range: [{lm.min():.3f}, {lm.max():.3f}]")
print("sample 10 points (log10 v_flat, log10 M_bar):")
idxs = np.linspace(0, valid_btfr.sum()-1, min(10,valid_btfr.sum())).astype(int)
for i in idxs:
    print(f"  {lv[i]:.4f}, {lm[i]:.4f}")
if valid_btfr.sum() >= 10:
    slope, intercept, rr, pp, se = stats.linregress(lv, lm)
    print(f"\nfit: log10(M_bar) = {slope:.3f}*log10(v_flat) + {intercept:.3f}  (r={rr:.3f}, n={valid_btfr.sum()})")

out = dict(rho_gal=rho_gal, c_s0=c_s0,
           rms_train_all=rms_tr_all, rms_holdout_all=rms_ho_all,
           rms_train_valid=rms_tr_v, rms_holdout_valid=rms_ho_v,
           n_valid_train=len(vf_tr_v), n_total_train=len(rows_train),
           n_valid_holdout=len(vf_ho_v), n_total_holdout=len(rows_hold))
json.dump(out, open(f"{D}/domain_U2_results.json","w"), indent=2)
print(f"\nresults -> {D}\\domain_U2_results.json, per-galaxy -> {D}\\domain_U2_per_galaxy.json")
