# two_border_test.py - the traffic-jam vs the easy-going border (2026-10-16)
# The framework's own web data: the choke should be HIGH where the heat's fed
# (the galaxy-adjacent traffic jam) and LOW where the medium just settles
# (the void-adjacent easy-going border). The falsifier's first read.
import pandas as pd
import numpy as np

d = pd.read_csv(r"C:\Users\jaden\Downloads\PWC-Check\scratch\rot\filaments_intergalactic.csv")
print(f"web segments: {len(d)}")
print()
print("THE TWO-BORDER READ - the choke vs the feed:")
feed = d["feed_proxy"].values
choke = d["choke_F2"].values

# the split: the high-feed (the galaxy-fed traffic jam) vs the low-feed (the
# void-adjacent easy-going) quartiles
lo = feed <= np.percentile(feed, 25)
hi = feed >= np.percentile(feed, 75)
print(f"  low-feed segments (the void-adjacent):  n={lo.sum():5d}  mean choke = {choke[lo].mean():.3f}")
print(f"  high-feed segments (the galaxy-fed):    n={hi.sum():5d}  mean choke = {choke[hi].mean():.3f}")
print()
# the correlation: does the jam scale with the feed?
r = float(np.corrcoef(feed, choke)[0, 1])
print(f"  choke-vs-feed correlation: r = {r:+.3f}")
print()
print("=" * 72)
if choke[hi].mean() > 1.5 * choke[lo].mean() and r > 0.2:
    print("VERDICT: the jam is where the heat is - the galaxy borders choke, the")
    print("void borders settle. The two-border prediction's first read AGREES.")
elif abs(r) < 0.1:
    print("VERDICT: no feed-dependence in this proxy - the prediction's not visible")
    print("in these columns; the sharper test needs the border-normalized gradients.")
else:
    print(f"VERDICT: partial - the choke's feed-dependence is there (r={r:+.3f}) but")
    print("the quartile split's weak; the border-normalized gradients are the next read.")
print("=" * 72)
print("honest note: these are the framework's own proxy columns (the choke_F2, the")
print("feed_proxy) - the run is the first read of the two-border question on the")
print("existing data, not the telescope-grade receipt.")
