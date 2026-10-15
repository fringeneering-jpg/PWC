# The void-weighted birefringence prediction map (2026-10-12)
# beta(n) = sum over voids: K(rho) ds,  dK/d(ln rho) < 0  -> voids maximal.
# With the repo's void catalog (Douglass+ 2023, SDSS DR7, 1184 voids) we freeze
# the PREDICTION side: the directions where beta must spike. The correlation side
# needs a direction-dependent measured beta map (named at the end).
import math, json
import numpy as np

# --- parse the catalog ---
rows = []
with open(r"C:\Users\jaden\Downloads\PWC-Check\PWC\sparc\voids_vf.txt") as f:
    started = False
    for line in f:
        if line.startswith("recno"):
            started = True
            continue
        if not started or not line.strip() or line.startswith("#"):
            continue
        if line.startswith(" ") and ("h-1.Mpc" in line):
            continue
        parts = line.split()
        if len(parts) < 12:
            continue
        try:
            cosmo, s, ra, dec, reff = parts[1], float(parts[8]), float(parts[9]), float(parts[10]), float(parts[11])
            if cosmo != "Planck2018":
                continue
            rows.append(dict(ra=ra, dec=dec, s=s, reff=reff))
        except (ValueError, IndexError):
            continue
print(f"voids loaded: {len(rows)} (Planck2018, SDSS footprint)")

# --- the kernel: each void's angular radius theta = Reff/s; linear taper ---
def angular_sep(ra1, dec1, ra2, dec2):
    d1, d2 = math.radians(dec1), math.radians(dec2)
    dra = math.radians(ra1 - ra2)
    return math.degrees(math.acos(max(-1.0, min(1.0,
        math.sin(d1)*math.sin(d2) + math.cos(d1)*math.cos(d2)*math.cos(dra)))))

grid_ra = np.arange(114, 258, 1.0)
grid_dec = np.arange(-1, 66, 1.0)
beta_map = np.zeros((len(grid_dec), len(grid_ra)))
for i, dec0 in enumerate(grid_dec):
    for j, ra0 in enumerate(grid_ra):
        wsum = 0.0
        for v in rows:
            theta = angular_sep(ra0, dec0, v['ra'], v['dec'])
            th_v = math.degrees(v['reff']/v['s'])
            if theta <= th_v:
                wsum += v['reff'] * (1.0 - theta/th_v)
        beta_map[i, j] = wsum

# --- the frozen prediction: the top directions ---
flat = [(beta_map[i, j], grid_dec[i], grid_ra[j])
        for i in range(len(grid_dec)) for j in range(len(grid_ra))]
flat.sort(reverse=True)
print("\nbeta_pred anisotropy: max = %.1f, min = %.1f, ratio = %.2f" % (
    flat[0][0], flat[-1][0], flat[0][0]/max(flat[-1][0], 1e-9)))
print("\nTOP 10 FROZEN beta-maximal directions (void-weighted lines of sight):")
for k in range(10):
    v, dec, ra = flat[k]
    print(f"  {k+1:2d}. RA {ra:6.1f}  Dec {dec:+5.1f}   beta_pred weight {v:.1f}")
print("\nBOTTOM 3 (beta-minimal, wall-dominated):")
for k in range(3):
    v, dec, ra = flat[-1-k]
    print(f"     RA {ra:6.1f}  Dec {dec:+5.1f}   weight {v:.1f}")

print("\n== what the correlation test needs (named, not faked) ==")
print("a direction-dependent measured beta map over the same footprint - e.g. the")
print("Diego-Palazuelos et al. 2022 PR4 per-region values, or an ACT DR6 birefringence")
print("map. The repo holds only the monopole (0.35 +/- 0.14 Planck; 0.30 +/- 0.11 PR4).")
print("Test form, frozen: rank-correlate measured beta(direction) with the predicted")
print("void-weight map above; the framework's sign demands a POSITIVE rank correlation,")
print("with the top predicted directions carrying the largest measured rotation.")
json.dump(dict(top10=[dict(ra=flat[k][2], dec=flat[k][1], w=flat[k][0]) for k in range(10)],
               bottom3=[dict(ra=flat[-1-k][2], dec=flat[-1-k][1], w=flat[-1-k][0]) for k in range(3)]),
          open("birefringence_void_prediction.json", "w"), indent=2)
print("prediction map saved: birefringence_void_prediction.json")
