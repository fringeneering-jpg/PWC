"""
DOMAIN R -- tests the "accessible-volume/permeability" idea from tonight's
proposal, in the most honest form buildable from REAL SPARC public columns
(no scale-height data is published, so a literal 3D volume-filling factor
is not directly measurable; Pi_gas here is declared explicitly as a proxy:
the LOCAL fraction of Newtonian pull contributed by gas vs total baryons,
bounded [0,1] by construction -- a genuinely different functional shape
from Domain N's failed additive k*g_gas term, not a rescaling of it).

C(r) = Pi_gas(r)^q,  Pi_gas(r) = g_gas(r) / g_bar(r)
g_obs_pred = g_bar * (1 + (a0/g_bar)^0.5 * C(r))

ONE new global parameter (q) fit on the SAME 104 training galaxies as
Domain M/N (identical seed=7 split). Reported on the SAME 45 holdout
galaxies. a0 refit jointly with q on train only (frozen split, not frozen
a0 -- Domain N did the same for its k parameter).
"""
import numpy as np, json
from scipy.optimize import minimize, minimize_scalar
from scipy import stats

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
KMS = 1.0e3
UPS_D, UPS_B = 0.5, 0.7

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
g_obs = Vo**2 / R * conv
Vbar2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
g_bar = Vbar2 / R * conv
g_gas = Vg*np.abs(Vg) / R * conv
ok = (g_bar > 0) & (g_obs > 0)
g_obs, g_bar, g_gas, name = g_obs[ok], g_bar[ok], g_gas[ok], name[ok]
y = np.log10(g_obs)

# Pi_gas: local gas-dominance fraction, bounded [0,1] by construction
pi_gas = np.clip(g_gas / g_bar, 0.0, 1.0)

galaxies = sorted(set(name))
rng = np.random.default_rng(7)   # SAME seed/split as Domain M and N
shuffled = galaxies.copy(); rng.shuffle(shuffled)
n_train = int(len(shuffled)*0.7)
train_gal = set(shuffled[:n_train]); hold_gal = set(shuffled[n_train:])
train_mask = np.array([n in train_gal for n in name])
hold_mask  = np.array([n in hold_gal  for n in name])
print(f"train galaxies: {len(train_gal)}, holdout galaxies: {len(hold_gal)}")

def choke_pi(gb, pig, a0, q):
    return gb*(1.0 + (a0/gb)**0.5 * pig**q)

y_tr, gb_tr, pig_tr = y[train_mask], g_bar[train_mask], pi_gas[train_mask]
y_ho, gb_ho, pig_ho = y[hold_mask], g_bar[hold_mask], pi_gas[hold_mask]

print("=== BASELINE (Domain M choke n=1/2, no Pi_gas factor, for reference) ===")
def obj_base(la0):
    return np.mean((y_tr - np.log10(gb_tr*(1.0+(10**la0/gb_tr)**0.5)))**2)
o0 = minimize_scalar(obj_base, bounds=(-12.0,-9.0), method="bounded")
a0_base = 10**o0.x
rms_base_tr = np.sqrt(np.mean((y_tr - np.log10(gb_tr*(1.0+(a0_base/gb_tr)**0.5)))**2))
rms_base_ho = np.sqrt(np.mean((y_ho - np.log10(gb_ho*(1.0+(a0_base/gb_ho)**0.5)))**2))
print(f"  a0={a0_base:.4e}  train rms={rms_base_tr:.4f}  holdout rms={rms_base_ho:.4f}")

print("\n=== EXTENDED: C = Pi_gas^q, fit (a0,q) jointly on TRAIN only ===")
def obj_ext(p):
    la0, q = p
    if q < -5 or q > 5: return 1e9
    pred = choke_pi(gb_tr, pig_tr, 10**la0, q)
    if np.any(~np.isfinite(pred)) or np.any(pred<=0): return 1e9
    return np.mean((y_tr - np.log10(pred))**2)
best = minimize(obj_ext, x0=[-10.0, 0.0], method="Nelder-Mead",
                 options=dict(xatol=1e-8, fatol=1e-12, maxiter=8000))
la0_ext, q_ext = best.x
a0_ext = 10**la0_ext
rms_ext_tr = np.sqrt(np.mean((y_tr - np.log10(choke_pi(gb_tr, pig_tr, a0_ext, q_ext)))**2))
rms_ext_ho = np.sqrt(np.mean((y_ho - np.log10(choke_pi(gb_ho, pig_ho, a0_ext, q_ext)))**2))
print(f"  fitted: a0={a0_ext:.4e}, q={q_ext:.4f}")
print(f"  train rms={rms_ext_tr:.4f} (baseline {rms_base_tr:.4f})")
print(f"  holdout rms={rms_ext_ho:.4f} (baseline {rms_base_ho:.4f})   change: {rms_ext_ho-rms_base_ho:+.4f}")

print("\n=== DOES THE GAS-FRACTION RESIDUAL (Domain N: rho=0.166, p=0.042) CHANGE? ===")
resid_ext_all  = y - np.log10(choke_pi(g_bar, pi_gas, a0_ext, q_ext))
resid_base_all = y - np.log10(g_bar*(1.0+(a0_base/g_bar)**0.5))

gal_resid_ext, gal_resid_base, gal_gasfrac = [], [], []
for g in galaxies:
    gm = (name == g)
    if gm.sum() < 1: continue
    l36 = L36.get(g, np.nan); mhi = MHI.get(g, np.nan)
    if not (np.isfinite(l36) and l36 > 0): continue
    gf = (mhi/l36) if (np.isfinite(mhi) and mhi > 0) else np.nan
    gal_resid_ext.append(np.mean(resid_ext_all[gm]))
    gal_resid_base.append(np.mean(resid_base_all[gm]))
    gal_gasfrac.append(gf)

gal_resid_ext = np.array(gal_resid_ext); gal_resid_base = np.array(gal_resid_base)
gal_gasfrac = np.array(gal_gasfrac)
valid = np.isfinite(gal_gasfrac) & np.isfinite(gal_resid_ext)
x = np.log10(gal_gasfrac[valid])
rho_base, p_base = stats.spearmanr(x, gal_resid_base[valid])
rho_ext, p_ext = stats.spearmanr(x, gal_resid_ext[valid])
print(f"  BASELINE residual vs log10(gas fraction): rho={rho_base:+.3f}, p={p_base:.4f}")
print(f"  EXTENDED residual vs log10(gas fraction): rho={rho_ext:+.3f}, p={p_ext:.4f}")

out = dict(a0_base=a0_base, rms_base_train=float(rms_base_tr), rms_base_holdout=float(rms_base_ho),
           a0_ext=a0_ext, q_ext=float(q_ext), rms_ext_train=float(rms_ext_tr), rms_ext_holdout=float(rms_ext_ho),
           rho_base=float(rho_base), p_base=float(p_base), rho_ext=float(rho_ext), p_ext=float(p_ext))
json.dump(out, open(f"{D}/domain_R_results.json","w"), indent=2)
print(f"\nresults -> {D}\\domain_R_results.json")
