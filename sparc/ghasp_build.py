"""Build GHASP baryonic + observed accelerations (no model scoring here).

Sources (sparc/ghasp/):
  rotation curves  : Epinat+2008 J/MNRAS/388/500 & J/MNRAS/390/466 tablef (deprojected Vrot, kpc, both sides)
  photometry + M/L : Korsaga+2019 J/MNRAS/482/154 tablea1 (Rc disc h, LD, R25/h; Sersic bulge re, n, LB)
                     tablea2 M/L from B-V colour (Bell & de Jong 2001) -- NOT fitted to rotation curves
  coordinates      : Epinat+2008 J/MNRAS/390/466 tableb1 (for SPARC overlap removal)
Baryons = stars only (Halpha-only survey; no HI gas in these mass models).
Disc: thin exponential (Freeman), total L = LD / [1-(1+x)e^-x], x = R25/h.
Bulge: Sersic, M(<r) = Mb * P(2n, b_n (r/re)^(1/n)) (projected-light enclosed fraction, spherical approx).
One M/L (B-V) applied to disc and bulge.
"""
import numpy as np, pandas as pd, re
from scipy.special import i0, i1, k0, k1, gammainc
G = 4.30091e-6; CONV = 1e6 / 3.0856775814913673e19
num = lambda s: int(re.sub(r"\D", "", s)) if re.search(r"\d", s) else None

a1 = pd.read_fwf("ghasp/korsaga_a1.dat", colspecs=[(0,9),(10,11),(12,24),(25,29),(30,34),(35,39),(40,43),(44,48),(49,53),(54,57),(58,64),(65,70),(71,75),(76,80),(81,87),(88,89)],
                 names=["ID","fBV","Type","BMAG","BV","mu0obs","R25h","Rlasth","mu0","h","LD","mue","re","n","LB","flag"])
a2 = pd.read_fwf("ghasp/korsaga_a2.dat", colspecs=[(0,9),(80,84)], names=["ID","ML"])
ph = a1.merge(a2, on="ID"); ph["ugc"] = ph.ID.map(num)
rc = []
for f, cs in [("ghasp/rc_390.dat", [(0,8),(9,14),(31,34),(35,38),(39,41),(42,43)]), ("ghasp/rc_388.dat", [(0,9),(10,15),(32,35),(36,39),(40,42),(43,44)])]:
    t = pd.read_fwf(f, colspecs=cs, names=["Name","r","V","eV","nb","side"]); t["ugc"] = t.Name.map(num); t["src"] = f; rc.append(t)
rc = pd.concat(rc)
rc = rc[rc.groupby("ugc").src.transform(lambda s: s == s.iloc[0])]   # one source per galaxy (390 preferred)
co = pd.read_fwf("ghasp/obs_390.dat", colspecs=[(10,15),(23,25),(26,28),(29,33),(34,35),(35,37),(38,40),(41,43)], names=["ugc","h","m","s","sg","d","dm","ds"])
co["ra"] = 15 * (co.h + co.m / 60 + co.s / 3600); co["de"] = np.where(co.sg == "-", -1, 1) * (co.d + co.dm / 60 + co.ds / 3600)
t1 = pd.read_csv("vizier_t1.txt", sep=r'\t+', comment='#', engine='python', on_bad_lines='skip'); t1.columns = [c.strip() for c in t1.columns]
sra, sde = pd.to_numeric(t1["_RA"], errors="coerce").values, pd.to_numeric(t1["_DE"], errors="coerce").values

def in_sparc(u):
    c = co[co.ugc == u]
    if c.empty: return None
    d = np.hypot((sra - c.ra.values[0]) * np.cos(np.radians(c.de.values[0])), sde - c.de.values[0]) * 3600
    return np.nanmin(d) < 60

out, skipped = [], {}
for _, p in ph.iterrows():
    u = p.ugc; r = rc[rc.ugc == u]
    if r.empty: skipped[p.ID] = "no rotation curve"; continue
    ov = in_sparc(u)
    if ov is None: skipped[p.ID] = "no coordinates"; continue
    if ov: skipped[p.ID] = "in SPARC"; continue
    r = r[(r.r > 0) & (r.V > 0)]
    # merge both sides: radial bins of width max(5% Rmax, 0.3 kpc), weighted by number of velocity bins
    w = max(0.05 * r.r.max(), 0.3); r = r.assign(b=(r.r / w).astype(int))
    b = r.groupby("b").apply(lambda d: pd.Series(dict(R=np.average(d.r, weights=d.nb), V=np.average(d.V, weights=d.nb), n=d.nb.sum())), include_groups=False)
    b = b[b.n >= 2]
    R, V = b.R.values, b.V.values
    x = p.R25h; Ld = p.LD * 1e8 / (1 - (1 + x) * np.exp(-x)); Md = p.ML * Ld; hh = p.h
    y = R / (2 * hh); vd2 = 2 * G * Md / hh * y ** 2 * (i0(y) * k0(y) - i1(y) * k1(y))
    vb2 = np.zeros_like(R)
    if pd.notna(p.LB) and p.LB > 0 and pd.notna(p.re) and pd.notna(p.n):
        n = p.n; bn = 2 * n - 1 / 3 + 0.009876 / n
        vb2 = G * p.ML * p.LB * 1e8 * gammainc(2 * n, bn * (R / p.re) ** (1 / n)) / R
    for Ri, Vi, d2, b2 in zip(R, V, vd2, vb2):
        out.append(dict(Name=p.ID.strip(), Type=p.Type, Rad=Ri, g_obs=Vi ** 2 / Ri * CONV, g_bar=(d2 + b2) / Ri * CONV, locked=b2 / (d2 + b2), Vobs=Vi))
df = pd.DataFrame(out); df = df[(df.g_bar > 0) & (df.g_obs > 0)]
df = df[df.groupby("Name").Rad.transform("size") >= 3]
df.to_csv("ghasp/ghasp_accel.csv", index=False)
print(f"built {df.Name.nunique()} galaxies, {len(df)} points | skipped: " + ", ".join(f"{k}: {v}" for k, v in pd.Series(skipped).value_counts().items()))
print(f"with bulge: {df[df.locked > 0].Name.nunique()}")
