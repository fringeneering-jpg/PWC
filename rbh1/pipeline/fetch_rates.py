"""Download all NIRSpec IFU science _rate.fits exposures for JWST GO-3149 (RBH-1 wake)."""
import os
from astroquery.mast import Observations

OUT = "/mnt/d/rbh1_reduction/rate"
os.makedirs(OUT, exist_ok=True)
obs = Observations.query_criteria(obs_collection="JWST", proposal_id="3149", calib_level=2)
print("level-2 observations:", len(obs))
prods = Observations.get_product_list(obs)
rate = Observations.filter_products(prods, productSubGroupDescription="RATE", productType="SCIENCE")
rate = rate[[("_rate.fits" in f) for f in rate["productFilename"]]]
print("rate files:", len(rate), "| total MB:", round(sum(rate["size"]) / 1e6))
Observations.download_products(rate, download_dir=OUT, flat=True)
print("done")
