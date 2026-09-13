"""
DOMAIN M -- the decisive, non-circular comparison requested: galaxy-level
train/holdout split (not pooled in-sample RMS) between McGaugh RAR and the
PWC choke n=1/2 form, PLUS residual-vs-galaxy-property structure test
(mass, surface brightness, gas fraction) -- same real SPARC data and
quality cuts as domain_K_rar.py, frozen unchanged.
"""
import numpy as np, json
from scipy.optimize import minimize_scalar
from scipy import stats

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

hr("1. LOAD REAL SPARC DATA (identical to domain_K_rar.py, frozen)")
t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name","i","Qual","Vflat","Dist","L3.6","SBdisk","MHI"])
t2 = read_vizier_tsv(f"{D}/vizier_t2.txt", ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])

inc  = {n:i for n,i in zip(t1["Name"], t1["i"])}
qual = {n:q for n,q in zip(t1["Name"], t1["Qual"])}
L36  = {n:v for n,v in zip(t1["Name"], t1["L3.6"])}
SBd  = {n:v for n,v in zip(t1["Name"], t1["SBdisk"])}
MHI  = {n:v for n,v in zip(t1["Name"], t1["MHI"])}

name = np.array(t2["Name"])
R    = np.array(t2["Rad"], float)
Vo   = np.array(t2["Vobs"], float)
eVo  = np.array(t2["e_Vobs"], float)
Vg   = np.array(t2["Vgas"], float)
Vd   = np.array(t2["Vdisk"], float)
Vb   = np.array(t2["Vbulge"], float)
Vb   = np.where(np.isnan(Vb), 0.0, Vb)
Vg   = np.where(np.isnan(Vg), 0.0, Vg)

inc_a  = np.array([inc.get(n, np.nan)  for n in name], float)
qual_a = np.array([qual.get(n, np.nan) for n in name], float)
m = (R > 0) & (Vo > 0) & np.isfinite(eVo)
m &= (eVo/Vo <= 0.10)
m &= (inc_a >= 30.0)
m &= (qual_a <= 2)
R, Vo, eVo, Vg, Vd, Vb, name = R[m], Vo[m], eVo[m], Vg[m], Vd[m], Vb[m], name[m]

conv = (KMS**2)/KPC
g_obs = Vo**2 / R * conv
Vbar2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
g_bar = Vbar2 / R * conv
ok = (g_bar > 0) & (g_obs > 0)
g_obs, g_bar, name = g_obs[ok], g_bar[ok], name[ok]
y = np.log10(g_obs)

galaxies = sorted(set(name))
print(f"  total galaxies available for split: {len(galaxies)}")

hr("2. GALAXY-LEVEL TRAIN/HOLDOUT SPLIT (70/30, fixed seed)")
rng = np.random.default_rng(7)
shuffled = galaxies.copy()
rng.shuffle(shuffled)
n_train = int(len(shuffled)*0.7)
train_gal = set(shuffled[:n_train])
hold_gal  = set(shuffled[n_train:])
print(f"  train galaxies: {len(train_gal)}, holdout galaxies: {len(hold_gal)}")

train_mask = np.array([n in train_gal for n in name])
hold_mask  = np.array([n in hold_gal  for n in name])
print(f"  train points: {train_mask.sum()}, holdout points: {hold_mask.sum()}")

def rar(gb, a0): return gb/(1.0 - np.exp(-np.sqrt(gb/a0)))
def choke_half(gb, a0): return gb*(1.0 + (a0/gb)**0.5)

hr("3. FIT BOTH MODELS ON TRAINING GALAXIES ONLY")
y_tr, gb_tr = y[train_mask], g_bar[train_mask]
y_ho, gb_ho = y[hold_mask], g_bar[hold_mask]

def fit_a0(model, y_fit, gb_fit):
    def obj(la0):
        return np.mean((y_fit - np.log10(model(gb_fit, 10**la0)))**2)
    o = minimize_scalar(obj, bounds=(-12.0, -9.0), method="bounded")
    return 10**o.x

a0_rar_train = fit_a0(rar, y_tr, gb_tr)
a0_choke_train = fit_a0(choke_half, y_tr, gb_tr)
print(f"  RAR a0 (fit on train only)        = {a0_rar_train:.4e}")
print(f"  choke n=1/2 a0 (fit on train only) = {a0_choke_train:.4e}")

def rms(y_true, pred):
    r = y_true - np.log10(pred)
    return float(np.sqrt(np.mean(r**2))), r

rms_rar_train, _ = rms(y_tr, rar(gb_tr, a0_rar_train))
rms_choke_train, _ = rms(y_tr, choke_half(gb_tr, a0_choke_train))
print(f"\n  IN-SAMPLE (train) RAR   rms: {rms_rar_train:.4f} dex")
print(f"  IN-SAMPLE (train) choke rms: {rms_choke_train:.4f} dex")

hr("4. BLIND PREDICTION ON HELD-OUT GALAXIES (never touched during fitting)")
rms_rar_hold, resid_rar_hold = rms(y_ho, rar(gb_ho, a0_rar_train))
rms_choke_hold, resid_choke_hold = rms(y_ho, choke_half(gb_ho, a0_choke_train))
print(f"  HOLDOUT RAR   rms: {rms_rar_hold:.4f} dex   (train->holdout change: {rms_rar_hold-rms_rar_train:+.4f})")
print(f"  HOLDOUT choke rms: {rms_choke_hold:.4f} dex   (train->holdout change: {rms_choke_hold-rms_choke_train:+.4f})")
print(f"\n  HOLDOUT difference (choke - RAR): {rms_choke_hold-rms_rar_hold:+.4f} dex "
      f"({100*(rms_choke_hold/rms_rar_hold-1):+.2f}%)")

hr("5. RESIDUAL STRUCTURE vs GALAXY PROPERTIES (mass, surface brightness, gas fraction)")
print("  Using ALL points (train+holdout) with each model's train-fit a0, per-galaxy mean residual")
resid_choke_all = y - np.log10(choke_half(g_bar, a0_choke_train))
resid_rar_all   = y - np.log10(rar(g_bar, a0_rar_train))

gal_mean_resid_choke, gal_mean_resid_rar, gal_L36, gal_SB, gal_gasfrac, gal_names_used = [],[],[],[],[],[]
for g in galaxies:
    gm = (name == g)
    if gm.sum() < 1: continue
    l36 = L36.get(g, np.nan)
    sb  = SBd.get(g, np.nan)
    mhi = MHI.get(g, np.nan)
    if not (np.isfinite(l36) and l36 > 0): continue
    gasfrac = (mhi/l36) if (np.isfinite(mhi) and mhi > 0) else np.nan
    gal_mean_resid_choke.append(np.mean(resid_choke_all[gm]))
    gal_mean_resid_rar.append(np.mean(resid_rar_all[gm]))
    gal_L36.append(l36)
    gal_SB.append(sb)
    gal_gasfrac.append(gasfrac)
    gal_names_used.append(g)

gal_mean_resid_choke = np.array(gal_mean_resid_choke)
gal_mean_resid_rar = np.array(gal_mean_resid_rar)
gal_L36 = np.array(gal_L36)
gal_SB = np.array(gal_SB)
gal_gasfrac = np.array(gal_gasfrac)

print(f"\n  galaxies with L3.6 available: {len(gal_L36)}")
for label, x in [("log10(L3.6) [mass proxy]", np.log10(gal_L36)),
                  ("SBdisk [surface brightness]", gal_SB),
                  ("log10(MHI/L3.6) [gas fraction]", np.log10(gal_gasfrac))]:
    valid = np.isfinite(x) & np.isfinite(gal_mean_resid_choke)
    if valid.sum() < 10:
        print(f"  {label}: insufficient data ({valid.sum()} galaxies)")
        continue
    rho_c, p_c = stats.spearmanr(x[valid], gal_mean_resid_choke[valid])
    rho_r, p_r = stats.spearmanr(x[valid], gal_mean_resid_rar[valid])
    print(f"\n  residual vs {label} (n={valid.sum()}):")
    print(f"    choke n=1/2 residual: rho={rho_c:+.3f}, p={p_c:.3f}")
    print(f"    RAR residual:         rho={rho_r:+.3f}, p={p_r:.3f}")

out = dict(
    n_train_gal=len(train_gal), n_hold_gal=len(hold_gal),
    a0_rar_train=a0_rar_train, a0_choke_train=a0_choke_train,
    rms_rar_train=rms_rar_train, rms_choke_train=rms_choke_train,
    rms_rar_hold=rms_rar_hold, rms_choke_hold=rms_choke_hold,
)
json.dump(out, open(f"{D}/domain_M_results.json","w"), indent=2)
print(f"\n\nresults -> {D}\\domain_M_results.json")
