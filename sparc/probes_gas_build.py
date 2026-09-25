"""GAS VERSION (predictions/probes_gas.md): same build, ALFALFA-matched galaxies, exponential HI disc added.
Build PROBES baryonic + observed accelerations (no model scoring here).

Raw data: Stone et al. 2022 PROBES-I, Zenodo record 10456320, downloaded to D:/probes (not in repo; ~100 MB).
Choices fixed BEFORE any scoring:
- Stars from unWISE W1 surface-brightness profile (AB; M_sun,W1 = 5.92 per Willmer 2018 as used by PROBES),
  M/L = 0.5 (SPARC disc value at 3.6 um). Isophotes with SB_e > 0.3 mag dropped (PROBES' own truncation rule).
- Face-on correction mu_face = mu_obs - 2.5 log10(cos i) (W1 treated as transparent).
- Inclination from r-band outermost kept isophote ellipticity, intrinsic thickness q0 = 0.2; keep 30 <= i <= 85 deg.
- Thin-disc gravity from the actual surface-density profile summed as rings (thin-ring elliptic potential,
  h = 0.2 kpc, same ring_gr as the SPARC work). g_bar = net inward ring pull; g_in/g_out from the same rings.
- No gas (mostly Halpha curves), no bulge/disc split -> locked = 0 for every galaxy.
- Rotation curve: |V| / (sin i (1 + z_helio)), both sides merged in radial bins of width max(5% Rmax, 0.3 kpc);
  galaxies need >= 5 bins inside the photometric extent.
- Overlap with SPARC and GHASP removed by 60" coordinate match.
"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, os
exec(open("jaden_tension_differential.py", encoding="utf-8").read().split("src = open")[0])  # imports
from scipy.special import ellipk
G = 4.30091e-6; CONV = 1e6 / 3.0856775814913673e19; H = 0.2
def ring_pot(r, a, m):
    s = (a + r) ** 2 + H ** 2; return -(2 * G * m / np.pi) * ellipk(4 * a * r / s) / np.sqrt(s)
def ring_gr(r, a, m, dr=1e-3): return -(ring_pot(r + dr, a, m) - ring_pot(r - dr, a, m)) / (2 * dr)

P = "D:/probes"; PR = f"{P}/profiles/profiles"
mt = pd.read_csv(f"{P}/main_table.csv", skiprows=1)
t1 = pd.read_csv("vizier_t1.txt", sep=r'\t+', comment='#', engine='python', on_bad_lines='skip'); t1.columns = [c.strip() for c in t1.columns]
ex_ra = list(pd.to_numeric(t1["_RA"], errors="coerce")); ex_de = list(pd.to_numeric(t1["_DE"], errors="coerce"))
co = pd.read_fwf("ghasp/obs_390.dat", colspecs=[(23,25),(26,28),(29,33),(34,35),(35,37),(38,40),(41,43)], names=["h","m","s","sg","d","dm","ds"])
ex_ra += list(15 * (co.h + co.m / 60 + co.s / 3600)); ex_de += list(np.where(co.sg == "-", -1, 1) * (co.d + co.dm / 60 + co.ds / 3600))
ex_ra, ex_de = np.array(ex_ra, float), np.array(ex_de, float)

from scipy.optimize import brentq
import sys
ML, WITH_GAS, OUT = float(sys.argv[1]), sys.argv[2] == "gas", sys.argv[3]
h = pd.read_csv("probes/alfalfa_match.csv"); GAS = dict(zip(h.Name, h.MHI))
out, why = [], {}
def skip(n, r): why[r] = why.get(r, 0) + 1
for _, g in mt.iterrows():
    n = g["name"]
    if n not in GAS: continue
    if not (g["has_w1-band"] and g["has_r-band"]): skip(n, "no W1 or r photometry"); continue
    if np.nanmin(np.hypot((ex_ra - g.RA) * np.cos(np.radians(g.DEC)), ex_de - g.DEC)) * 3600 < 60: skip(n, "in SPARC/GHASP"); continue
    try:
        rc = pd.read_csv(f"{PR}/{n}_rc.prof", skiprows=1); w1 = pd.read_csv(f"{PR}/{n}_w1.prof", skiprows=1); rb = pd.read_csv(f"{PR}/{n}_r.prof", skiprows=1)
    except FileNotFoundError: skip(n, "missing profile file"); continue
    D = g.distance
    if not np.isfinite(D) or D <= 0: skip(n, "no distance"); continue
    rb = rb[rb.SB_e <= 0.3]; w1 = w1[(w1.SB_e <= 0.3) & (w1.R > 0)]
    if len(rb) < 3 or len(w1) < 5: skip(n, "photometry too short"); continue
    q = 1 - rb.ellip.values[-1]; c2 = (q ** 2 - 0.04) / 0.96
    inc = np.degrees(np.arccos(np.sqrt(np.clip(c2, 0, 1))))
    if not (30 <= inc <= 85): skip(n, "inclination outside 30-85"); continue
    k = D * 1e3 / 206265.0                                     # kpc per arcsec
    Rs = w1.R.values * k; mu = w1.SB.values - 2.5 * np.log10(np.cos(np.radians(inc)))
    Sig = ML * 10 ** (0.4 * (5.92 + 21.572 - mu)) * 1e6        # Msun/kpc^2
    edges = np.concatenate([[0], (Rs[1:] + Rs[:-1]) / 2, [Rs[-1] + (Rs[-1] - Rs[-2]) / 2]])
    mring = Sig * np.pi * (edges[1:] ** 2 - edges[:-1] ** 2)
    if WITH_GAS:
        Mh = GAS[n]; Rhi = 0.5 * 10 ** (0.506 * np.log10(Mh) - 3.293)
        f = lambda Rg: Mh / (2 * np.pi * Rg ** 2) * np.exp(-Rhi / Rg) - 1e6
        Rg = brentq(f, 1e-3 * Rhi, Rhi / 2) if f(Rhi / 2) > 0 else Rhi / 4
        ge = np.linspace(0, 2 * Rhi, 201); gm = 1.33 * Mh * np.diff(-(1 + ge / Rg) * np.exp(-ge / Rg))  # exact exp-disc mass per annulus
        Rs_all = np.concatenate([Rs, (ge[1:] + ge[:-1]) / 2]); m_all = np.concatenate([mring, gm])
    else:
        Rs_all, m_all = Rs, mring
    z = g.redshift_helio / 299792.458
    r = pd.DataFrame(dict(R=np.abs(rc.R.values) * k, V=np.abs(rc.V.values) / (np.sin(np.radians(inc)) * (1 + z))))
    r = r[(r.R > 0) & (r.R <= Rs[-1]) & np.isfinite(r.V)]
    if len(r) < 5: skip(n, "rotation curve too short"); continue
    w = max(0.05 * r.R.max(), 0.3); r["b"] = (r.R / w).astype(int)
    b = r.groupby("b").agg(R=("R", "mean"), V=("V", "mean"), n=("V", "size"))
    if len(b) < 5: skip(n, "fewer than 5 bins"); continue
    for Ri, Vi in zip(b.R.values, b.V.values):
        gr = ring_gr(Ri, Rs_all, m_all)
        gin = -gr[Rs_all < Ri].sum(); gout = gr[Rs_all > Ri].sum(); gnet = gin - gout
        if gnet <= 0 or Vi <= 0: continue
        out.append(dict(Name=n, Type=g.morphology, survey=g.RC_survey, inc=inc, Rad=Ri, g_obs=Vi ** 2 / Ri * CONV, g_bar=gnet * CONV,
                        shared=np.clip(min(gin, gout) / gin, 0, 1) if gin > 0 else 0.0, locked=0.0))
df = pd.DataFrame(out); df = df[df.groupby("Name").Rad.transform("size") >= 5]
df.to_csv(OUT, index=False)
print(f"built {df.Name.nunique()} galaxies, {len(df)} points"); print("skipped:", why)
