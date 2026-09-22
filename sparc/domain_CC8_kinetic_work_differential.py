"""
DOMAIN CC8 -- differential kinetic work: resistance asymmetry (inward vs
outward mass) multiplied by the orbital velocity of the mass moving through
it, not a static geometric snapshot.

  asym(R)  = 2*M_in(R)/M_tot - 1     (bounded -1..+1, + = interior-dominant)
  V_bar(R) = sqrt(Vbar2), baryonic-only orbital velocity (non-circular,
             doesn't use V_obs)
  work(R)  = asym(R) * V_bar(R)      -- the actual kinetic-work differential

  g_pred = choke(g_bar, a0, n=1/2) * (1 + lam*work)

Same discipline: real data, one universal lam, galaxy-balanced RMS,
10-seed stability, honest report either way.
"""
import numpy as np, json
from scipy.optimize import minimize, minimize_scalar

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
KMS = 1.0e3
UPS_D, UPS_B = 0.5, 0.7
G = 6.674e-11

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
ok = (g_bar > 0) & (g_obs > 0) & (Vbar2 > 0)
g_obs, g_bar, Vbar2, R, name = g_obs[ok], g_bar[ok], Vbar2[ok], R[ok], name[ok]
y = np.log10(g_obs)

R_m = R * KPC
M_enc = g_bar * R_m**2 / G
V_bar_kms = np.sqrt(Vbar2)   # baryonic-only orbital velocity, km/s

asym = np.zeros_like(g_bar)
for gname in set(name):
    idx = np.where(name == gname)[0]
    order = idx[np.argsort(R[idx])]
    Menc_g = M_enc[order]
    Mtot = Menc_g[-1]
    if Mtot <= 0 or not np.isfinite(Mtot):
        asym[order] = np.nan
        continue
    asym[order] = 2.0*Menc_g/Mtot - 1.0

work = asym * V_bar_kms   # the actual kinetic-work differential, km/s-scale
valid = np.isfinite(work)
print(f"usable points: {len(g_obs)}, valid: {valid.sum()}")
print(f"work range: {np.nanmin(work):.1f} to {np.nanmax(work):.1f} km/s, median {np.nanmedian(work):.1f}")

galaxies = sorted(set(name))
def choke(gb, a0): return gb*(1.0 + np.sqrt(a0/gb))
def gal_balanced_rms(resid, names_sub):
    per_gal = [np.mean(resid[names_sub==g]) for g in set(names_sub)]
    return float(np.sqrt(np.mean(np.array(per_gal)**2)))

# normalize work to O(1) scale for a well-conditioned fit (divide by its own std)
work_scale = np.nanstd(work[valid])
work_n = work / work_scale

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
        pred = choke(g_bar[train_mask], 10**la0) * (1.0 + lam*work_n[train_mask])
        if np.any(pred <= 0): return 1e9
        return np.mean((y[train_mask]-np.log10(pred))**2)
    best = minimize(obj_ext, x0=[np.log10(a0_base), 0.02], method="Nelder-Mead",
                     options=dict(xatol=1e-9, fatol=1e-13, maxiter=6000))
    la0_e, lam_e = best.x
    a0_e = 10**la0_e
    pred_hold = choke(g_bar[hold_mask], a0_e)*(1.0+lam_e*work_n[hold_mask])
    resid_ext_hold = y[hold_mask]-np.log10(np.maximum(pred_hold,1e-300))
    ext_gal = gal_balanced_rms(resid_ext_hold, name[hold_mask])

    winner = "ext" if ext_gal < base_gal else "base"
    stability.append(dict(seed=seed, base_gal=base_gal, ext_gal=ext_gal,
                           delta=ext_gal-base_gal, lam=lam_e, winner=winner))
    print(f"{seed:>5} {base_gal:>9.4f} {ext_gal:>9.4f} {ext_gal-base_gal:>+9.4f} {lam_e:>10.5f}  {winner}")

n_wins = sum(1 for s in stability if s["winner"]=="ext")
n_pos = sum(1 for s in stability if s["lam"]>0)
print(f"\nExtension beats baseline (galaxy-balanced holdout) in {n_wins}/{len(SEEDS)} seeds.")
print(f"lambda POSITIVE in {n_pos}/{len(SEEDS)}, NEGATIVE in {len(SEEDS)-n_pos}/{len(SEEDS)}.")
mean_delta = float(np.mean([s["delta"] for s in stability]))
mean_lam = float(np.mean([s["lam"] for s in stability]))
print(f"Mean holdout delta: {mean_delta:+.4f} dex. Mean lambda: {mean_lam:+.5f}")

json.dump(dict(stability=stability, n_wins=n_wins, n_seeds=len(SEEDS),
                n_lam_positive=n_pos, mean_delta=mean_delta, mean_lam=mean_lam,
                work_scale=float(work_scale)),
          open(f"{D}/domain_CC8_results.json","w"), indent=2)
