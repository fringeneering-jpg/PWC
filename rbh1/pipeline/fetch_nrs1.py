"""Download the NRS1 science _rate.fits exposures for GO-3149 that the first query missed."""
import os
from astroquery.mast import Observations
OUT = "/mnt/d/rbh1_reduction/rate"
obs = Observations.query_criteria(obs_collection="JWST", proposal_id="3149")
p = Observations.get_product_list(obs)
keep = [i for i, f in enumerate(p["productFilename"])
        if f.endswith("_nrs1_rate.fits") and ("_02101_" in f or "_04101_" in f)]
sel = p[keep]
# de-duplicate by filename
_, idx = __import__("numpy").unique(sel["productFilename"], return_index=True)
sel = sel[sorted(idx)]
print("NRS1 science rate files:", len(sel))
Observations.download_products(sel, download_dir=OUT, flat=True)
print("done")
