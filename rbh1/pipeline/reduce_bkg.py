"""Re-reduction v2: as reduce.py, plus pixel-level background subtraction.
Background for each science exposure = the 4 science exposures of the OTHER pointing
(same detector). The pointings sit on opposite sides of the wake, ~1" apart perpendicular
to it (van Dokkum et al., arXiv:2512.04166), so the narrow wake lands on different pixels
and is not self-subtracted; sky + detector pattern are removed. NRS1 only."""
import glob, json, os
from multiprocessing import Pool
os.environ.setdefault("CRDS_PATH", os.path.expanduser("~/crds_cache"))
os.environ.setdefault("CRDS_SERVER_URL", "https://jwst-crds.stsci.edu")
from astropy.io import fits
from jwst.pipeline import Spec2Pipeline, Spec3Pipeline

BASE = "/mnt/d/rbh1_reduction"
RATE, CAL, CUBE = f"{BASE}/rate", f"{BASE}/cal_bkg", f"{BASE}/cube_bkg"
for d in (CAL, CUBE): os.makedirs(d, exist_ok=True)

def key(f):
    h = fits.getheader(f, 0)
    return h.get("TARGPROP"), h.get("DETECTOR"), h.get("PATT_NUM"), bool(h.get("IS_IMPRT"))

def spec2(f):
    name = os.path.basename(f).replace("_rate.fits", "")
    out = os.path.join(CAL, name + "_cal.fits")
    if os.path.exists(out): return out
    t, det, dith, _ = key(f)
    rates = glob.glob(f"{RATE}/*_rate.fits")
    imp = [g for g in rates if key(g) == (t, det, dith, True)]
    bkg = [g for g in rates if key(g)[1] == det and key(g)[0] != t and not key(g)[3]]
    members = [{"expname": f, "exptype": "science"}]
    members += [{"expname": imp[0], "exptype": "imprint"}] if imp else []
    members += [{"expname": b, "exptype": "background"} for b in bkg]
    asn = {"asn_type": "spec2", "asn_rule": "manual", "program": "3149", "asn_pool": "manual",
           "products": [{"name": name, "members": members}]}
    ap = os.path.join(CAL, name + "_spec2_asn.json"); json.dump(asn, open(ap, "w"), indent=1)
    print(name, "| imprint", len(imp), "| background frames", len(bkg), flush=True)
    Spec2Pipeline.call(ap, output_dir=CAL, save_results=True, steps={
        "bkg_subtract": {"skip": False},
        "clean_flicker_noise": {"skip": False},
        "pixel_replace": {"skip": False},
        "cube_build": {"skip": True},
        "extract_1d": {"skip": True},
    })
    return out

if __name__ == "__main__":
    sci = sorted(g for g in glob.glob(f"{RATE}/*_nrs1_rate.fits") if not key(g)[3])
    print("science:", len(sci), flush=True)
    spec2(sci[0])
    with Pool(4) as p: p.map(spec2, sci)
    cals = sorted(glob.glob(f"{CAL}/*_cal.fits")); print("cal files:", len(cals), flush=True)
    asn = {"asn_type": "spec3", "asn_rule": "manual", "program": "3149", "asn_pool": "manual",
           "products": [{"name": "rbh1_wake_mosaic_bkg", "members": [{"expname": c, "exptype": "science"} for c in cals]}]}
    json.dump(asn, open(f"{CUBE}/asn.json", "w"), indent=1)
    Spec3Pipeline.call(f"{CUBE}/asn.json", output_dir=CUBE, save_results=True, steps={
        "master_background": {"skip": True}, "outlier_detection": {"skip": False},
        "pixel_replace": {"skip": False}, "cube_build": {"weighting": "drizzle", "coord_system": "skyalign"},
        "extract_1d": {"skip": True}, "spectral_leak": {"skip": True}})
    print("DONE", glob.glob(f"{CUBE}/*s3d.fits"), flush=True)
