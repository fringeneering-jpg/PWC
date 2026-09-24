"""Re-reduce JWST GO-3149 (RBH-1 wake) NIRSpec IFU G140M/F100LP from _rate.fits.
Differences from the archive Level-3 product: NSClean flicker-noise cleaning ON,
bad-pixel self-calibration across dithers ON, pixel replacement ON, outlier
detection across all dithers, both pointings combined into one mosaic cube.
Background is removed later per spaxel from line-free continuum (no dedicated
background exposures exist for this programme)."""
import glob, json, os, sys
from multiprocessing import Pool
os.environ.setdefault("CRDS_PATH", os.path.expanduser("~/crds_cache"))
os.environ.setdefault("CRDS_SERVER_URL", "https://jwst-crds.stsci.edu")
from jwst.pipeline import Spec2Pipeline, Spec3Pipeline

BASE = "/mnt/d/rbh1_reduction"
RATE, CAL, CUBE = f"{BASE}/rate", f"{BASE}/cal", f"{BASE}/cube"
for d in (CAL, CUBE): os.makedirs(d, exist_ok=True)

from astropy.io import fits

def key(f):
    h = fits.getheader(f, 0)
    return h.get("TARGPROP"), h.get("DETECTOR"), h.get("PATT_NUM"), bool(h.get("IS_IMPRT"))

def spec2(f):
    out = os.path.join(CAL, os.path.basename(f).replace("_rate.fits", "_cal.fits"))
    if os.path.exists(out): return out
    t, det, dith, _ = key(f)
    imps = [g for g in glob.glob(f"{RATE}/*_rate.fits") if key(g) == (t, det, dith, True)]
    members = [{"expname": f, "exptype": "science"}] + [{"expname": imps[0], "exptype": "imprint"}] if imps else [{"expname": f, "exptype": "science"}]
    name = os.path.basename(f).replace("_rate.fits", "")
    asn = {"asn_type": "spec2", "asn_rule": "manual", "program": "3149", "asn_pool": "manual",
           "products": [{"name": name, "members": members}]}
    ap = os.path.join(CAL, name + "_spec2_asn.json"); json.dump(asn, open(ap, "w"), indent=1)
    print(name, "imprint:", os.path.basename(imps[0]) if imps else "NONE", flush=True)
    Spec2Pipeline.call(ap, output_dir=CAL, save_results=True, steps={
        "clean_flicker_noise": {"skip": False},
        "pixel_replace": {"skip": False},
        "cube_build": {"skip": True},
        "extract_1d": {"skip": True},
    })
    return out

if __name__ == "__main__":
    # NRS2 holds no G140M/F100LP IFU spectrum for this programme (NoDataOnDetector) -> NRS1 only
    rates = sorted(g for g in glob.glob(f"{RATE}/*_nrs1_rate.fits") if not key(g)[3])
    print("science rate files:", len(rates), flush=True)
    if not rates: sys.exit("no rate files")
    # fetch reference files once, serially, so parallel workers don't race on the CRDS cache
    spec2(rates[0])
    with Pool(4) as p:
        cals = p.map(spec2, rates)
    cals = sorted(glob.glob(f"{CAL}/*_cal.fits"))
    print("cal files:", len(cals), flush=True)
    asn = {"asn_type": "spec3", "asn_rule": "manual", "program": "3149", "asn_pool": "manual",
           "products": [{"name": "rbh1_wake_mosaic",
                         "members": [{"expname": c, "exptype": "science"} for c in cals]}]}
    json.dump(asn, open(f"{CUBE}/rbh1_spec3_asn.json", "w"), indent=1)
    Spec3Pipeline.call(f"{CUBE}/rbh1_spec3_asn.json", output_dir=CUBE, save_results=True, steps={
        "master_background": {"skip": True},
        "outlier_detection": {"skip": False},
        "pixel_replace": {"skip": False},
        "cube_build": {"weighting": "drizzle", "coord_system": "skyalign"},
        "extract_1d": {"skip": True},
        "spectral_leak": {"skip": True},
    })
    print("DONE", glob.glob(f"{CUBE}/*s3d.fits"), flush=True)
