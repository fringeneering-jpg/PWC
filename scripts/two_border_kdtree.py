# two_border_kdtree.py - the bubbles vs the void shells: the D_ratio wall (2026-10-17)
# The prediction: the 334,163 HII bubbles (the thaw zones paying the 19-part
# debt) should hug the VoidFinder shells' 20-part geometric boundaries - the
# nearest-distance distribution should pile up at D_ratio ~ 1.0 (the wall),
# not spread randomly. The honest read: both populations on disk, two frames,
# one conversion.
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

# --- the bubbles (the master_data.json's 334k HII regions) ---
bub = pd.read_json(r"C:\Users\jaden\cosmology\OLD\master_data.json")
print(f"bubbles: {len(bub)}")
glon = np.radians(bub["GLON"].values.astype(float))
glat = np.radians(bub["GLAT"].values.astype(float))
dist = pd.to_numeric(bub["Dist"].replace("", np.nan), errors="coerce").values.astype(float)
ok = np.isfinite(dist) & (dist > 0)
glon, glat, dist = glon[ok], glat[ok], dist[ok]
print(f"bubbles with distances: {ok.sum()}")
# the Galactic frame -> the local cartesian (the sun at the origin, the simple conversion)
x_b = dist * np.cos(glat) * np.cos(glon)
y_b = dist * np.cos(glat) * np.sin(glon)
z_b = dist * np.sin(glat)

# --- the voids (the VoidFinder shells, comoving Mpc/h) ---
vv = pd.read_csv(r"C:\Users\jaden\Downloads\VoidFinder-nsa_v1_0_1_Planck2018_comoving_holes.txt", sep=r"\s+", skiprows=1,
                 names=["x","y","z","radius","void"])
print(f"void shell points: {len(vv)}")
# the comoving Mpc/h -> kpc: h ~ 0.7, so 1 Mpc/h = 1428.57 kpc... the bubbles' Dist
# is the kpc; use the ratio-free approach: the D_ratio = distance_to_shell / shell_radius
# (dimensionless), so the units cancel if both sides use the SAME unit. Convert the
# voids to kpc with h=0.7 for the absolute comparison.
h = 0.7
kpc_per = 1000.0 / h
xv = vv["x"].values.astype(float) * kpc_per
yv = vv["y"].values.astype(float) * kpc_per
zv = vv["z"].values.astype(float) * kpc_per
rv = vv["radius"].values.astype(float) * kpc_per

# the bubble positions in the SAME comoving frame: the approximate - the bubbles'
# Dist is the line-of-sight distance; the radial-velocity part's ignored in this
# first read (the honest label: the local-frame vs the comoving-frame mismatch is
# the named caveat - this is the order-of-magnitude first read).
tree = cKDTree(np.column_stack([xv, yv, zv]))
# the distance to the nearest shell POINT for a sample of bubbles
idx = np.random.default_rng(42).choice(len(x_b), size=min(20000, len(x_b)), replace=False)
d, _ = tree.query(np.column_stack([x_b[idx], y_b[idx], z_b[idx]]), k=1)
# the D_ratio: the distance to the shell divided by the shell's radius
# (the shell radius at the matched point's void - use the mean void radius for the
# first read)
r_mean = rv.mean()
D_ratio = d / r_mean
print()
print("THE D_RATIO WALL - the bubbles vs the void shells (first read):")
print(f"  bubbles sampled: {len(d)}")
print(f"  D_ratio: median {np.median(D_ratio):.3f}, mean {D_ratio.mean():.3f}")
print(f"  fraction within D_ratio < 0.5: {float((D_ratio < 0.5).mean()):.3f}")
print(f"  fraction within D_ratio < 1.0: {float((D_ratio < 1.0).mean()):.3f}")
print()
print("  the prediction: the distribution piles up at D_ratio ~ 1.0 (the hard")
print("  wall at the shells) - a sharp excess over the random expectation.")
print("  the honest caveats: the bubbles are the LOCAL (Galactic) HII regions,")
print("  the voids are the COSMOLOGICAL shells - the frames are mismatched in this")
print("  first read (the bubbles are our galaxy's own, not the cosmic web's).")
print("  The real test wants the EXTRAGALACTIC bubble census; this is the plumbing's")
print("  proof, not the receipt.")
