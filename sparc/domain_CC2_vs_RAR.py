"""Domain CC2 vs McGaugh RAR on IDENTICAL splits.

Same data, cuts, gradient mask, 10 seeds and galaxy-balanced metric as
domain_CC2_surface_tension.py (its data-loading block is executed verbatim).
Adds McGaugh's empirical RAR, g_obs = g_bar / (1 - exp(-sqrt(g_bar/a0))),
with its one constant a0 fitted on the SAME training galaxies, scored on the
SAME held-out galaxies. Answers: does the PWC tension/gradient form beat the
best empirical relation out of sample?
"""
import numpy as np, json
from scipy.optimize import minimize, minimize_scalar

src = open(r"C:\Users\jaden\cosmology\sparc\domain_CC2_surface_tension.py", encoding="utf-8").read()
exec(src.split("SEEDS = [")[0])   # data loading + choke(), identical to CC2

def rar(gb, a0): return gb / (1.0 - np.exp(-np.sqrt(gb / a0)))
def gal_rms(resid, names_sub):
    return float(np.sqrt(np.mean([np.mean(resid[names_sub == g]) ** 2 for g in set(names_sub)])))

SEEDS = [7, 1, 2, 3, 4, 5, 6, 8, 9, 10]
rows = []
print(f"{'seed':>5} {'PWC base':>9} {'PWC+tension':>12} {'McGaugh RAR':>12}")
for seed in SEEDS:
    rng = np.random.default_rng(seed)
    sh = galaxies.copy(); rng.shuffle(sh); n_tr = int(len(sh) * 0.7)
    tr_g, ho_g = set(sh[:n_tr]), set(sh[n_tr:])
    tr = np.array([n in tr_g for n in name]) & valid_grad
    ho = np.array([n in ho_g for n in name]) & valid_grad
    # PWC base (one constant)
    a0b = 10 ** minimize_scalar(lambda la: np.mean((y[tr] - np.log10(choke(g_bar[tr], 10 ** la))) ** 2),
                                bounds=(-12, -9), method="bounded").x
    base = gal_rms(y[ho] - np.log10(choke(g_bar[ho], a0b)), name[ho])
    # PWC + tension/gradient term (two constants)
    def obj(p):
        pr = choke(g_bar[tr], 10 ** p[0]) * (1 + p[1] * np.abs(grad[tr]))
        return 1e9 if np.any(pr <= 0) else np.mean((y[tr] - np.log10(pr)) ** 2)
    b = minimize(obj, x0=[np.log10(a0b), 0.01], method="Nelder-Mead",
                 options=dict(xatol=1e-8, fatol=1e-12, maxiter=5000)).x
    ext = gal_rms(y[ho] - np.log10(np.maximum(choke(g_bar[ho], 10 ** b[0]) * (1 + b[1] * np.abs(grad[ho])), 1e-300)), name[ho])
    # McGaugh RAR (one constant)
    a0r = 10 ** minimize_scalar(lambda la: np.mean((y[tr] - np.log10(rar(g_bar[tr], 10 ** la))) ** 2),
                                bounds=(-11, -9), method="bounded").x
    mg = gal_rms(y[ho] - np.log10(rar(g_bar[ho], a0r)), name[ho])
    rows.append(dict(seed=seed, pwc_base=base, pwc_tension=ext, mcgaugh=mg))
    print(f"{seed:>5} {base:>9.4f} {ext:>12.4f} {mg:>12.4f}")
m = {k: float(np.mean([r[k] for r in rows])) for k in ("pwc_base", "pwc_tension", "mcgaugh")}
wins = sum(r["pwc_tension"] < r["mcgaugh"] for r in rows)
print(f"\nmean holdout galaxy-balanced RMS: PWC base {m['pwc_base']:.4f} | PWC+tension {m['pwc_tension']:.4f} | McGaugh {m['mcgaugh']:.4f}")
print(f"PWC+tension beats McGaugh on {wins}/{len(rows)} identical splits")
json.dump(dict(rows=rows, means=m, tension_beats_mcgaugh=wins), open("domain_CC2_vs_RAR_results.json", "w"), indent=1)
