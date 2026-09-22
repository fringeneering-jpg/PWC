"""
DOMAIN CC4 -- the corrected tension proxy: real enclosed-mass asymmetry, not
a local slope. Directly encodes the chain-of-masses picture: at radius r,
compare mass enclosed inside r to mass remaining outside r (out to the last
measured point). Signed: +1 = all mass interior (edge of the disk, strong net
inward pull expected), -1 = all mass exterior (deep center, weak/opposite).

  M_enc(r) = g_bar(r) * r^2 / G          (from v_bar^2 = G*M_enc/r)
  M_tot    = M_enc at galaxy's own last (largest) measured radius
  asym(r)  = 2*M_enc(r)/M_tot - 1        (signed, in [-1, +1])

  g_pred = choke(g_bar, a0, n=1/2) * (1 + lam*asym(r))

Prediction under test: lam > 0 (extra pull where asym is positive, i.e. at
the edge) -- the opposite sign from the failed |gradient| proxy. One universal
lam, fit jointly with a0 on TRAIN galaxies, scored on HOLDOUT, galaxy-balanced
RMS throughout (not point-pooled), 10-seed stability check before any verdict.
"""
import numpy as np, json
from scipy.optimize import minimize, minimize_scalar

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
KMS = 1.0e3
UPS_D, UPS_B = 0.5, 0.7
G = 6.674e-11
MSUN = 1.989e30

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

t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name","i","Qual"])
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

# --- real enclosed-mass asymmetry per point ---
R_m = R * KPC
M_enc = g_bar * R_m**2 / G   # kg, from v_bar^2 = G*M_enc/r  =>  g_bar = G*M_enc/r^2

asym = np.zeros_like(g_bar)   # now: real tension MAGNITUDE, not net directional asymmetry
for gname in set(name):
    idx = np.where(name == gname)[0]
    order = idx[np.argsort(R[idx])]
    Menc_g = M_enc[order]
    Mtot = Menc_g[-1]   # enclosed mass at this galaxy's own last measured radius
    if Mtot <= 0 or not np.isfinite(Mtot):
        asym[order] = np.nan
        continue
    Mout_g = Mtot - Menc_g
    # sandwiched-ness: zero if nothing on one side (r=0 or r=r_max), peaks where
    # both interior and exterior mass are substantial -- matches "high tension
    # only where mass sits on BOTH sides", normalized to peak at 1.0
    asym[order] = 4.0*Menc_g*Mout_g/Mtot**2
valid = np.isfinite(asym)
print(f"usable points: {len(g_obs)}, with valid tension proxy: {valid.sum()}")
print(f"tension range: {np.nanmin(asym):.3f} to {np.nanmax(asym):.3f}, median {np.nanmedian(asym):.3f}")

galaxies = sorted(set(name))
def choke(gb, a0): return gb*(1.0 + np.sqrt(a0/gb))

def gal_balanced_rms(resid, names_sub):
    per_gal = [np.mean(resid[names_sub==g]) for g in set(names_sub)]
    return float(np.sqrt(np.mean(np.array(per_gal)**2)))

SEEDS = [7, 1, 2, 3, 4, 5, 6, 8, 9, 10]
stability = []
print(f"\n{'seed':>5} {'baseGal':>9} {'extGal':>9} {'delta':>9} {'lam':>10}  winner")
print("-"*58)
for seed in SEEDS:
    rng = np.random.default_rng(seed)
    shuffled = galaxies.copy(); rng.shuffle(shuffled)
    n_train = int(len(shuffled)*0.7)
    train_gal = set(shuffled[:n_train]); hold_gal = set(shuffled[n_train:])
    train_mask = np.array([n in train_gal for n in name]) & valid
    hold_mask  = np.array([n in hold_gal  for n in name]) & valid

    def obj_base(la0):
        return np.mean((y[train_mask]-np.log10(choke(g_bar[train_mask], 10**la0)))**2)
    ob = minimize_scalar(obj_base, bounds=(-12.0,-9.0), method="bounded")
    a0_base = 10**ob.x
    resid_base_hold = y[hold_mask]-np.log10(choke(g_bar[hold_mask], a0_base))
    base_gal = gal_balanced_rms(resid_base_hold, name[hold_mask])

    def obj_ext(p):
        la0, lam = p
        pred = choke(g_bar[train_mask], 10**la0) * (1.0 + lam*asym[train_mask])
        if np.any(pred <= 0): return 1e9
        return np.mean((y[train_mask]-np.log10(pred))**2)
    best = minimize(obj_ext, x0=[np.log10(a0_base), 0.05], method="Nelder-Mead",
                     options=dict(xatol=1e-9, fatol=1e-13, maxiter=6000))
    la0_e, lam_e = best.x
    a0_e = 10**la0_e
    pred_hold = choke(g_bar[hold_mask], a0_e)*(1.0+lam_e*asym[hold_mask])
    resid_ext_hold = y[hold_mask]-np.log10(np.maximum(pred_hold,1e-300))
    ext_gal = gal_balanced_rms(resid_ext_hold, name[hold_mask])

    winner = "ext" if ext_gal < base_gal else "base"
    stability.append(dict(seed=seed, base_gal=base_gal, ext_gal=ext_gal,
                           delta=ext_gal-base_gal, lam=lam_e, winner=winner))
    print(f"{seed:>5} {base_gal:>9.4f} {ext_gal:>9.4f} {ext_gal-base_gal:>+9.4f} {lam_e:>10.5f}  {winner}")

n_wins = sum(1 for s in stability if s["winner"]=="ext")
n_pos = sum(1 for s in stability if s["lam"]>0)
print(f"\nExtension beats baseline (galaxy-balanced holdout) in {n_wins}/{len(SEEDS)} seeds.")
print(f"lambda is POSITIVE in {n_pos}/{len(SEEDS)} seeds, NEGATIVE in {len(SEEDS)-n_pos}/{len(SEEDS)}.")
mean_delta = float(np.mean([s["delta"] for s in stability]))
mean_lam = float(np.mean([s["lam"] for s in stability]))
print(f"Mean holdout delta: {mean_delta:+.4f} dex. Mean lambda: {mean_lam:+.5f}")

json.dump(dict(stability=stability, n_wins=n_wins, n_seeds=len(SEEDS),
                n_lam_positive=n_pos, mean_delta=mean_delta, mean_lam=mean_lam),
          open(f"{D}/domain_CC4_results.json","w"), indent=2)
