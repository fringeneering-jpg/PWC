# The directional comparison, honestly runnable: predicted anisotropy vs published isotropy
import json, math
import numpy as np

pred = json.load(open(r"C:\Users\jaden\Downloads\PWC-Check\birefringence_void_prediction.json"))
top = pred['top10']

# rebuild the full map stats
import importlib.util
spec = importlib.util.spec_from_file_location("bvm", r"C:\Users\jaden\Downloads\PWC-Check\scratch\birefringence_void_map.py")
# the map script prints and writes JSON; recompute the stats inline instead:
rows = []
with open(r"C:\Users\jaden\Downloads\PWC-Check\PWC\sparc\voids_vf.txt") as f:
    started = False
    for line in f:
        if line.startswith("recno"):
            started = True; continue
        if not started or not line.strip() or line.startswith("#"): continue
        if "h-1.Mpc" in line: continue
        p = line.split()
        if len(p) < 12: continue
        try:
            if p[1] == "Planck2018":
                rows.append((float(p[9]), float(p[10]), float(p[8]), float(p[11])))
        except (ValueError, IndexError): continue

def sep(ra1, de1, ra2, de2):
    d1, d2 = math.radians(de1), math.radians(de2)
    return math.degrees(math.acos(max(-1.0, min(1.0,
        math.sin(d1)*math.sin(d2)+math.cos(d1)*math.cos(d2)*math.cos(math.radians(ra1-ra2))))))

weights = []
for ra0 in range(114, 258, 2):
    for de0 in range(-1, 66, 2):
        w = 0.0
        for (ra, de, s, reff) in rows:
            th = sep(ra0, de0, ra, de); thv = math.degrees(reff/s)
            if th <= thv: w += reff*(1.0-th/thv)
        weights.append(w)
w = np.array(weights)
mean_w, std_w = w.mean(), w.std()
print(f"void-weight map over the footprint: mean {mean_w:.1f}, std {std_w:.1f}, max {w.max():.1f}")
frac = std_w/mean_w if mean_w > 0 else 0
print(f"predicted fractional beta fluctuation: std/mean = {frac:.2f}")

BETA = 0.342       # deg, Eskilt-Komatsu 2022 joint WMAP+Planck monopole
sig_beta_pred = BETA*frac
print(f"predicted beta fluctuation amplitude: {sig_beta_pred:.2f} deg on the void angular scale")
print(f"(the top directions: RA {top[0]['ra']:.0f} Dec {top[0]['dec']:.0f} etc. carry the spikes)")

print("\n== the measured side, correctly scoped ==")
print("the published birefringence results (Eskilt & Komatsu 2205.13962: beta = 0.342")
print("+/- 0.094 deg, 3.6 sigma) are ISOTROPIC-monopole measurements - they say nothing")
print("about direction dependence, so they are NOT yet usable against the voids-maximal")
print("prediction. Jaden's ruling: leave it at the frozen prediction; do not use the")
print("isotropic study for the directional test.")
print("\n== the state ==")
print("PREDICTION FROZEN (2026-10-12): beta fluctuations ~0.15 deg, 43% fractional,")
print("spiked in the deep-void corridor (top: RA 149, Dec +31); rank-correlation with a")
print("future per-direction beta map is the test. No applicable measurement exists yet.")
