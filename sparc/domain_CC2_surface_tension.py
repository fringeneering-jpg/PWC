"""
DOMAIN CC2 -- testing tonight's surface-tension mechanism against real SPARC
data, on top of the existing domain_K choke model.

Physical claim being tested (from tonight's PWC.md addition, section 10):
  the medium is self-gravitating; a galaxy's outer boundary sits under a
  real surface-tension-like state (net inward pull from density asymmetry
  at the edge), same mechanism as ordinary liquid surface tension.

Honest, non-arbitrary way to encode "surface tension" from real data: surface
tension in real physics (Cahn-Hilliard / van der Waals theory) comes from the
GRADIENT of density, not density itself -- sigma ~ integral (d(rho)/dr)^2 dr.
So the added term uses the local slope of g_bar's own radial profile, computed
directly from each galaxy's real Rad/Vgas/Vdisk/Vbulge points -- not a free
per-galaxy fit, one single universal coefficient, same discipline as domain_K.

  g_pred = choke(g_bar, a0, n=0.5) * (1 + lam * |d ln(g_bar)/d ln(R)|)

lam and a0 fit jointly on TRAIN galaxies only (70/30 split, seed=7, matching
domain_M's convention), scored blind on HOLDOUT. Reported honestly either way.
"""
import numpy as np, json
from scipy.optimize import minimize

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

t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name","i","Qual","Vflat","Dist"])
t2 = read_vizier_tsv(f"{D}/vizier_t2.txt", ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
inc  = {n:i for n,i in zip(t1["Name"], t1["i"])}
qual = {n:q for n,q in zip(t1["Name"], t1["Qual"])}

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
ok = (g_bar > 0) & (g_obs > 0)
g_obs, g_bar, R, name = g_obs[ok], g_bar[ok], R[ok], name[ok]
y = np.log10(g_obs)

# --- real per-galaxy log-log slope of g_bar(R): the actual gradient term ---
grad = np.zeros_like(g_bar)
for gname in set(name):
    idx = np.where(name == gname)[0]
    order = idx[np.argsort(R[idx])]
    r_g = R[order]; gb_g = g_bar[order]
    lr = np.log(r_g); lg = np.log(np.maximum(gb_g, 1e-300))
    if len(r_g) >= 3:
        d = np.gradient(lg, lr)
    else:
        d = np.full_like(lr, np.nan)
    grad[order] = d
valid_grad = np.isfinite(grad)
print(f"usable points total: {len(g_obs)}, with valid local gradient: {valid_grad.sum()}")

galaxies = sorted(set(name))

def choke(gb, a0): return gb*(1.0 + np.sqrt(a0/gb))

SEEDS = [7, 1, 2, 3, 4, 5, 6, 8, 9, 10]
stability = []

from scipy.optimize import minimize_scalar

def gal_balanced_rms(resid, names_sub):
    """average residual within each galaxy first, then RMS across galaxy means."""
    per_gal = []
    for g in set(names_sub):
        gm = names_sub == g
        per_gal.append(np.mean(resid[gm]))
    per_gal = np.array(per_gal)
    return float(np.sqrt(np.mean(per_gal**2)))

print(f"\n{'seed':>5} {'basePt':>8} {'extPt':>8} {'baseGal':>8} {'extGal':>8} {'lam':>10}  gal_winner")
print("-"*76)
for seed in SEEDS:
    rng = np.random.default_rng(seed)
    shuffled = galaxies.copy(); rng.shuffle(shuffled)
    n_train = int(len(shuffled)*0.7)
    train_gal = set(shuffled[:n_train]); hold_gal = set(shuffled[n_train:])
    train_mask = np.array([n in train_gal for n in name]) & valid_grad
    hold_mask  = np.array([n in hold_gal  for n in name]) & valid_grad

    def obj_base(la0):
        pred = np.log10(choke(g_bar[train_mask], 10**la0))
        return np.mean((y[train_mask]-pred)**2)
    ob = minimize_scalar(obj_base, bounds=(-12.0,-9.0), method="bounded")
    a0_base = 10**ob.x
    resid_base_hold = y[hold_mask]-np.log10(choke(g_bar[hold_mask], a0_base))
    base_pt  = float(np.sqrt(np.mean(resid_base_hold**2)))
    base_gal = gal_balanced_rms(resid_base_hold, name[hold_mask])

    def obj_ext(p):
        la0, lam = p
        pred = choke(g_bar[train_mask], 10**la0) * (1.0 + lam*np.abs(grad[train_mask]))
        if np.any(pred <= 0): return 1e9
        return np.mean((y[train_mask]-np.log10(pred))**2)
    best = minimize(obj_ext, x0=[np.log10(a0_base), 0.01], method="Nelder-Mead",
                     options=dict(xatol=1e-8, fatol=1e-12, maxiter=5000))
    la0_e, lam_e = best.x
    a0_e = 10**la0_e
    pred_hold = choke(g_bar[hold_mask], a0_e)*(1.0+lam_e*np.abs(grad[hold_mask]))
    resid_ext_hold = y[hold_mask]-np.log10(np.maximum(pred_hold,1e-300))
    ext_pt  = float(np.sqrt(np.mean(resid_ext_hold**2)))
    ext_gal = gal_balanced_rms(resid_ext_hold, name[hold_mask])

    winner = "ext" if ext_gal < base_gal else "base"
    stability.append(dict(seed=seed, base_pt=base_pt, ext_pt=ext_pt,
                           base_gal=base_gal, ext_gal=ext_gal, lam=lam_e, winner=winner))
    print(f"{seed:>5} {base_pt:>8.4f} {ext_pt:>8.4f} {base_gal:>8.4f} {ext_gal:>8.4f} {lam_e:>10.5f}  {winner}")

n_ext_wins = sum(1 for s in stability if s["winner"]=="ext")
print(f"\nExtension beats baseline on GALAXY-BALANCED holdout in {n_ext_wins}/{len(SEEDS)} seeds.")
mean_delta_gal = float(np.mean([s["ext_gal"]-s["base_gal"] for s in stability]))
print(f"Mean galaxy-balanced holdout delta across seeds: {mean_delta_gal:+.4f} dex")

json.dump(dict(stability=stability, n_ext_wins=n_ext_wins, n_seeds=len(SEEDS),
                mean_delta_gal=mean_delta_gal),
          open(f"{D}/domain_CC2_results.json","w"), indent=2)
