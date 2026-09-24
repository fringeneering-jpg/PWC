"""
DOMAIN PV -- Pole-venting rotation test on real SPARC data.

PWC mechanism (PWC.md §0, "Why the disk is 2D: the poles vent the heat"):
  a spinning galaxy vents heat along its rotation axis (§9), leaving the disk as
  pure 2D tension; beyond the holding threshold the pull falls as 1/r, giving
  the extra term sqrt(a0*g_bar). If spin drives the venting, faster-spinning
  disks should confine more strongly.

PRE-REGISTERED (written before any number below was computed):
  Model is FROZEN: g_pred = g_bar * (1 + sqrt(a0/g_bar)), a0 = 7.556e-11 m/s^2
  (the 0.1327-dex Void Push run). No refitting.
  Residual per point: r = log10(g_obs) - log10(g_pred).
  Only the low-acceleration region counts (g_bar < a0), where the zipper term
  dominates. Per galaxy: mean residual over its low-g points (need >= 3).
  PRIMARY spin proxy: outer angular speed Omega_out = Vflat / R_last.
  SECONDARY proxies: Vflat; Hubble type T (0=S0 ... 11=BCD).
  PREDICTION: residual rises with spin (positive correlation with Omega_out),
  surviving control for the galaxy's own mean log g_bar (low-g region) and
  log L[3.6] (total light ~ mass), via partial Spearman correlation.
  PASS  : partial rho > 0 with permutation p < 0.05.
  FAIL  : partial rho <= 0, or p >= 0.05 (no detectable spin dependence --
          what MOND-type laws with no spin term predict).

Data: Lelli, McGaugh & Schombert 2016 (SPARC), VizieR J/AJ/152/157 tables 1+2,
      same files and quality cuts as domain_K_rar.py.
"""
import numpy as np, json
from scipy.stats import spearmanr, rankdata

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19; KMS = 1.0e3
UPS_D, UPS_B = 0.5, 0.7
A0 = 7.556e-11
rng = np.random.default_rng(20260925)

def read_vizier_tsv(path, cols):
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8", errors="replace")]
    hdr_i = next(i for i, l in enumerate(lines) if not l.startswith("#") and "\t" in l and "recno" in l)
    names = lines[hdr_i].split("\t")
    dash_i = max(i for i in range(hdr_i+1, min(hdr_i+6, len(lines)))
                 if set(lines[i].replace("\t", "").strip()) <= set("- "))
    idx = {c: names.index(c) for c in cols}; out = {c: [] for c in cols}
    for l in lines[dash_i+1:]:
        if not l.strip() or l.startswith("#"): continue
        f = l.split("\t")
        if len(f) < len(names): continue
        try:
            row = {c: (f[idx[c]].strip() if c == "Name" else
                       (float(f[idx[c]]) if f[idx[c]].strip() not in ("", "---") else np.nan)) for c in cols}
        except ValueError:
            continue
        for c in cols: out[c].append(row[c])
    return out

t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name", "i", "Qual", "Vflat", "Type", "L3.6"])
t2 = read_vizier_tsv(f"{D}/vizier_t2.txt", ["Name", "Rad", "Vobs", "e_Vobs", "Vgas", "Vdisk", "Vbulge"])
G1 = {n: dict(i=i, q=q, vf=v, T=t, L=L) for n, i, q, v, t, L in
      zip(t1["Name"], t1["i"], t1["Qual"], t1["Vflat"], t1["Type"], t1["L3.6"])}

name = np.array(t2["Name"]); R = np.array(t2["Rad"]); Vo = np.array(t2["Vobs"]); eVo = np.array(t2["e_Vobs"])
Vg = np.nan_to_num(np.array(t2["Vgas"])); Vd = np.array(t2["Vdisk"]); Vb = np.nan_to_num(np.array(t2["Vbulge"]))
inc = np.array([G1.get(n, {}).get("i", np.nan) for n in name]); qual = np.array([G1.get(n, {}).get("q", np.nan) for n in name])
m = (R > 0) & (Vo > 0) & np.isfinite(eVo) & (eVo/Vo <= 0.10) & (inc >= 30) & (qual <= 2)
name, R, Vo, Vg, Vd, Vb = name[m], R[m], Vo[m], Vg[m], Vd[m], Vb[m]
conv = KMS**2/KPC
g_obs = Vo**2/R*conv
g_bar = (Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb))/R*conv
ok = (g_bar > 0) & (g_obs > 0)
name, R, g_obs, g_bar = name[ok], R[ok], g_obs[ok], g_bar[ok]
res = np.log10(g_obs) - np.log10(g_bar*(1+np.sqrt(A0/g_bar)))
print(f"points after cuts: {len(res)}   galaxies: {len(set(name))}")
print(f"frozen-model scatter, all points: {np.sqrt(np.mean(res**2)):.4f} dex")

rows = []
for n in sorted(set(name)):
    s = name == n; lo = s & (g_bar < A0)
    g = G1[n]
    if lo.sum() < 3 or not np.isfinite(g["vf"]) or g["vf"] <= 0: continue
    Rlast = R[s].max()
    rows.append(dict(name=n, r=float(res[lo].mean()), n_lo=int(lo.sum()),
                     omega=float(g["vf"]/Rlast), vflat=float(g["vf"]), T=float(g["T"]),
                     lgb=float(np.log10(g_bar[lo]).mean()), lL=float(np.log10(g["L"]))))
print(f"galaxies with >=3 low-g points and a Vflat: {len(rows)}")
r = np.array([x["r"] for x in rows]); ctrl = np.column_stack([[x["lgb"] for x in rows], [x["lL"] for x in rows]])

def partial_spearman(x, y, Z):
    rx, ry = rankdata(x), rankdata(y); Zr = np.column_stack([rankdata(z) for z in Z.T] + [np.ones(len(x))])
    ex = rx - Zr @ np.linalg.lstsq(Zr, rx, rcond=None)[0]; ey = ry - Zr @ np.linalg.lstsq(Zr, ry, rcond=None)[0]
    return float(np.corrcoef(ex, ey)[0, 1])

out = {}
for key, label in [("omega", "PRIMARY  Omega_out = Vflat/R_last"), ("vflat", "secondary Vflat"), ("T", "secondary Hubble type T")]:
    x = np.array([v[key] for v in rows])
    rho_raw, p_raw = spearmanr(x, r)
    rho_p = partial_spearman(x, r, ctrl)
    null = np.array([partial_spearman(rng.permutation(x), r, ctrl) for _ in range(5000)])
    p_perm = float((np.abs(null) >= abs(rho_p)).mean())
    out[key] = dict(raw_rho=float(rho_raw), raw_p=float(p_raw), partial_rho=rho_p, perm_p_two_sided=p_perm)
    print(f"{label:38s} raw rho={rho_raw:+.3f} (p={p_raw:.3g})   partial rho={rho_p:+.3f} (perm p={p_perm:.3g})")

prim = out["omega"]
verdict = "PASS" if (prim["partial_rho"] > 0 and prim["perm_p_two_sided"] < 0.05) else "FAIL"
print(f"\nPRE-REGISTERED VERDICT (primary proxy): {verdict}")
json.dump(dict(a0=A0, n_galaxies=len(rows), results=out, verdict=verdict,
               galaxies=rows), open(f"{D}/domain_PV_results.json", "w"), indent=1)
