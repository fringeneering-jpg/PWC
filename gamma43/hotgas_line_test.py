"""43 GeV line vs hot gas (prediction frozen in PREDICTION_hotgas_line.md)."""
import numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from astroquery.vizier import Vizier
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.stats import mannwhitneyu
cl = pd.DataFrame([("Virgo",187.704,12.391,0.0038,18.358,1),("Fornax",54.669,-35.310,0.0046,17.906,1),("Ophiuchus",258.111,-23.363,0.0280,17.769,1),
  ("M49",187.444,7.997,0.0038,17.685,0),("A3526",192.200,-41.309,0.0103,17.600,0),("A1060",159.178,-27.521,0.0114,17.388,0),("Coma",194.947,27.939,0.0232,17.344,0),
  ("NGC4636",190.708,2.688,0.0037,17.313,0),("AWM7",43.623,41.578,0.0172,17.308,0),("A1367",176.190,19.703,0.0216,17.283,0),("NGC5813",225.299,1.698,0.0064,17.184,0),
  ("A2877",17.480,-45.922,0.0241,17.155,0),("S636",157.421,-35.326,0.0093,17.126,0)], columns=["name","ra","dec","z","logJ","det"])
m = Vizier(columns=["**"], row_limit=-1).get_catalogs("J/A+A/534/A109/mcxc")[0].to_pandas()
mc = SkyCoord([str(x) for x in m["RAJ2000"]], [str(x) for x in m["DEJ2000"]], unit=(u.hourangle, u.deg))
rows = []
for r in cl.itertuples():
    sep = SkyCoord(r.ra*u.deg, r.dec*u.deg).separation(mc).deg; i = int(np.argmin(sep))
    if sep[i] < 1.0:
        L = float(m["L500"].iloc[i]); d = r.z * 299792.458 / 70.0; rows.append((r.name, m["MCXC"].iloc[i], round(sep[i], 2), L, L / d**2, r.logJ, r.det))
    else: rows.append((r.name, None, round(sep[i], 2), np.nan, np.nan, r.logJ, r.det))
t = pd.DataFrame(rows, columns=["cluster","MCXC","sep_deg","L500","Xflux","logJ","detected"]).sort_values("Xflux", ascending=False)
t["Xflux_rank"] = t.Xflux.rank(ascending=False); print(t.to_string(index=False))
ok = t.dropna(subset=["Xflux"])
for col, lab in [("Xflux", "X-ray flux (hot gas)"), ("logJ", "dark-matter J-factor")]:
    p = mannwhitneyu(ok[ok.detected == 1][col], ok[ok.detected == 0][col], alternative="greater").pvalue
    print(f"{lab:22s}: detected rank above non-detected? one-sided Mann-Whitney p = {p:.3f}")
t.to_csv("hotgas_line_results.csv", index=False)
