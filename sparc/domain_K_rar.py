"""
DOMAIN K -- Radial Acceleration Relation from real SPARC data.

Pre-registered question (from results_for_readthrough.md Part 9):
  "Falsifies framework if the same functional form (no new free parameters per
   galaxy) can't match the RAR's tightness that MOND already achieves for free."

Key structural point established BEFORE fitting:
  Domain B's validated form is  choke = driving / ambient_resistance, a power
  ratio. Written as an acceleration relation that reduces to Newton at high
  acceleration, the only power-ratio family available is

      g_obs = g_bar * [ 1 + (a0/g_bar)^n ]

  n is the choke exponent. Domain D used n=1 (naive linear ratio) and found it
  outranked the textbook 1/6 power at n=6 -- but n=6 had no statistical power.
  Here n is fitted against 175 galaxies, which is the powered version of that
  same question.

Data: Lelli, McGaugh & Schombert 2016, AJ 152, 157 (SPARC).
      VizieR J/AJ/152/157 table1 (galaxies) + table2 (rotation curves).
      Downloaded live 2026-08-04. Nothing simulated.
"""
import numpy as np, re, json
from scipy.optimize import curve_fit, minimize_scalar

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
KMS = 1.0e3
A0_LIT = 1.2e-10          # MOND a0, m/s^2
UPS_D, UPS_B = 0.5, 0.7   # standard SPARC 3.6um mass-to-light ratios

def hr(t): print("\n"+"="*78); print(t); print("="*78)

def read_vizier_tsv(path, cols):
    """VizieR asu-tsv: header row, units row, dashes row, then data."""
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

hr("1. LOAD REAL SPARC DATA")
t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name","i","Qual","Vflat","Dist"])
t2 = read_vizier_tsv(f"{D}/vizier_t2.txt",
                     ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
print(f"  table1 galaxies      : {len(t1['Name'])}")
print(f"  table2 curve points  : {len(t2['Name'])}")
inc  = {n:i for n,i in zip(t1["Name"], t1["i"])}
qual = {n:q for n,q in zip(t1["Name"], t1["Qual"])}

name = np.array(t2["Name"])
R    = np.array(t2["Rad"], float)
Vo   = np.array(t2["Vobs"], float)
eVo  = np.array(t2["e_Vobs"], float)
Vg   = np.array(t2["Vgas"], float)
Vd   = np.array(t2["Vdisk"], float)
Vb   = np.array(t2["Vbulge"], float)
Vb   = np.where(np.isnan(Vb), 0.0, Vb)
Vg   = np.where(np.isnan(Vg), 0.0, Vg)

hr("2. QUALITY CUTS (McGaugh, Lelli & Schombert 2016 criteria)")
inc_a  = np.array([inc.get(n, np.nan)  for n in name], float)
qual_a = np.array([qual.get(n, np.nan) for n in name], float)
m = (R > 0) & (Vo > 0) & np.isfinite(eVo)
print(f"  finite R, Vobs, e_Vobs              : {m.sum():5d}")
m &= (eVo/Vo <= 0.10);   print(f"  + e_Vobs/Vobs <= 10%                : {m.sum():5d}")
m &= (inc_a >= 30.0);    print(f"  + inclination >= 30 deg             : {m.sum():5d}")
m &= (qual_a <= 2);      print(f"  + quality flag Q <= 2               : {m.sum():5d}")
print(f"  galaxies surviving                  : {len(set(name[m])):5d}")

R, Vo, eVo, Vg, Vd, Vb, name = R[m], Vo[m], eVo[m], Vg[m], Vd[m], Vb[m], name[m]

hr("3. BUILD THE ACCELERATIONS")
conv = (KMS**2)/KPC                      # (km/s)^2 / kpc  ->  m/s^2
g_obs = Vo**2 / R * conv
Vbar2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
g_bar = Vbar2 / R * conv
ok = (g_bar > 0) & (g_obs > 0)
g_obs, g_bar, Vo, eVo, R = g_obs[ok], g_bar[ok], Vo[ok], eVo[ok], R[ok]
print(f"  g_bar = [Vgas|Vgas| + {UPS_D}*Vdisk|Vdisk| + {UPS_B}*Vbul|Vbul|]/R")
print(f"  usable points        : {len(g_obs)}")
print(f"  log10 g_bar range    : {np.log10(g_bar).min():.2f} to {np.log10(g_bar).max():.2f}")
print(f"  log10 g_obs range    : {np.log10(g_obs).min():.2f} to {np.log10(g_obs).max():.2f}")

y = np.log10(g_obs)
def scatter(pred):
    r = y - np.log10(pred)
    return float(np.sqrt(np.mean(r**2))), float(np.std(r))

hr("4. BENCHMARKS")
res = {}

# (i) Newtonian baryons only -- the null: no dark matter, no medium
rms, sd = scatter(g_bar)
res["newton_baryons_only"] = dict(params=0, rms_dex=rms)
print(f"  Newtonian baryons only        (0 params) : rms {rms:.4f} dex")

# (ii) McGaugh RAR function, 1 universal parameter
def rar(gb, a0): return gb/(1.0 - np.exp(-np.sqrt(gb/a0)))
def obj_rar(la0):
    return np.mean((y - np.log10(rar(g_bar, 10**la0)))**2)
o = minimize_scalar(obj_rar, bounds=(-11.0, -9.0), method="bounded")
a0_fit = 10**o.x
rms, sd = scatter(rar(g_bar, a0_fit))
res["rar_mcgaugh"] = dict(params=1, a0=a0_fit, rms_dex=rms)
print(f"  RAR (McGaugh nu fn)           (1 param)  : rms {rms:.4f} dex, "
      f"a0 = {a0_fit:.3e} m/s^2")
rms_lit, _ = scatter(rar(g_bar, A0_LIT))
print(f"  RAR at literature a0=1.2e-10  (0 params) : rms {rms_lit:.4f} dex")
print(f"  published total scatter for reference     : ~0.13 dex")

hr("5. THE CHOKE FAMILY -- g_obs = g_bar * [1 + (a0/g_bar)^n]")
def choke(gb, a0, n): return gb*(1.0 + (a0/gb)**n)

print("  Structural constraint fixed BEFORE fitting: flat rotation curves")
print("  require g_obs ~ g_bar^(1/2) in the deep-field limit, and")
print("      g_obs -> a0^n * g_bar^(1-n)   =>   1-n = 1/2   =>   n = 1/2")
print("  So the choke structure is FORCED to n=1/2 by the existence of flat")
print("  rotation curves. Domain D's naive n=1 predicts g_obs -> a0 = const,")
print("  i.e. V ~ sqrt(R) RISING curves. Now test what the data picks.\n")

# fit n and a0 jointly (2 universal params, still zero per-galaxy freedom)
def obj2(p):
    la0, n = p
    if not (0.05 < n < 2.0): return 1e9
    return np.mean((y - np.log10(choke(g_bar, 10**la0, n)))**2)
from scipy.optimize import minimize
best = minimize(obj2, x0=[-10.0, 0.5], method="Nelder-Mead",
                options=dict(xatol=1e-6, fatol=1e-10, maxiter=4000))
la0_b, n_b = best.x
rms_b, _ = scatter(choke(g_bar, 10**la0_b, n_b))
res["choke_free_n"] = dict(params=2, a0=10**la0_b, n=n_b, rms_dex=rms_b)
print(f"  {'form':<44} {'params':>7} {'rms (dex)':>11}")
print(f"  {'-'*44} {'-'*7} {'-'*11}")
print(f"  {'choke, n and a0 both free':<44} {2:>7} {rms_b:>11.4f}"
      f"   -> n = {n_b:.4f}, a0 = {10**la0_b:.3e}")
for n_fix, lbl in ((0.5,"choke, n=1/2 fixed (flat-curve value)"),
                   (1.0,"choke, n=1 (Domain D naive linear ratio)"),
                   (1/6,"choke, n=1/6 (Chapman-Ferraro power)")):
    def objn(la0, nn=n_fix):
        return np.mean((y - np.log10(choke(g_bar, 10**la0, nn)))**2)
    oo = minimize_scalar(objn, bounds=(-12.0,-8.0), method="bounded")
    r_, _ = scatter(choke(g_bar, 10**oo.x, n_fix))
    res[f"choke_n_{n_fix:.4f}"] = dict(params=1, a0=10**oo.x, n=n_fix, rms_dex=r_)
    print(f"  {lbl:<44} {1:>7} {r_:>11.4f}   -> a0 = {10**oo.x:.3e}")

hr("6. VERDICT AGAINST THE PRE-REGISTERED RULE")
print(f"  {'model':<42} {'universal':>10} {'per-gal':>8} {'rms dex':>9}")
print(f"  {'-'*42} {'-'*10} {'-'*8} {'-'*9}")
rows = [("Newtonian baryons only (null)", 0, 0, res["newton_baryons_only"]["rms_dex"]),
        ("RAR / MOND nu function", 1, 0, res["rar_mcgaugh"]["rms_dex"]),
        ("choke n=1/2 (framework, forced)", 1, 0, res["choke_n_0.5000"]["rms_dex"]),
        ("choke n free", 2, 0, res["choke_free_n"]["rms_dex"]),
        ("choke n=1 (Domain D form)", 1, 0, res["choke_n_1.0000"]["rms_dex"])]
for lbl, u, pg, r in rows:
    print(f"  {lbl:<42} {u:>10} {pg:>8} {r:>9.4f}")

d_mond = res["rar_mcgaugh"]["rms_dex"]
d_chok = res["choke_n_0.5000"]["rms_dex"]
print(f"\n  MOND/RAR  : {d_mond:.4f} dex with 1 universal parameter")
print(f"  choke n=1/2: {d_chok:.4f} dex with 1 universal parameter")
print(f"  difference : {d_chok-d_mond:+.4f} dex ({100*(d_chok/d_mond-1):+.1f}%)")
verdict = ("MATCHES -- framework form is competitive with MOND"
           if d_chok <= d_mond*1.15 else
           "FAILS the pre-registered rule -- cannot match MOND's tightness")
print(f"\n  PRE-REGISTERED VERDICT: {verdict}")
print(f"  Fitted choke exponent n = {n_b:.4f}  (flat-curve requirement: 0.5;"
      f" Domain D used 1.0)")

json.dump(res, open(f"{D}/domain_K_results.json","w"), indent=2)
print(f"\n  results -> {D}\\domain_K_results.json")
