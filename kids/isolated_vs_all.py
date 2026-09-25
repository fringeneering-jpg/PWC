"""Isolated vs all lenses inside 0.3 Mpc (prediction frozen in PREDICTION_isolated_vs_all.md)."""
import numpy as np
F = 4 * 4.52e-30 * 3.086e16; G = 6.6743e-11; MSUN = 1.989e30; R = 0.3 * 3.0857e22
edges_up = [10.3, 10.6, 10.8, 11.0]
L, W, rows = [], [], []
for b, lu in enumerate(edges_up, 1):
    iso = np.loadtxt(f"Fig-9_RAR-KiDS-isolated_Massbin-{b}.txt"); al = np.loadtxt(f"Fig-A4_RAR-KiDS-all_Massbin-{b}.txt")
    gb = iso[:, 0]; gi = F * iso[:, 1] / iso[:, 4]; ei = F * iso[:, 3] / iso[:, 4]; ga = F * al[:, 1] / al[:, 4]; ea = F * al[:, 3] / al[:, 4]
    gcut = G * 10 ** lu * MSUN / R ** 2
    for x, a, sa, c, sc in zip(gb, gi, ei, ga, ea):
        if x <= gcut or a <= 0 or c <= 0: continue
        lr = np.log10(a / c); s = np.sqrt((sa / a) ** 2 + (sc / c) ** 2) / np.log(10)
        L.append(lr); W.append(1 / s ** 2); rows.append((b, x, lr, s))
L, W = np.array(L), np.array(W); m = (L * W).sum() / W.sum(); e = 1 / np.sqrt(W.sum())
for b, x, lr, s in rows: print(f"  mass bin {b}  g_bar {x:.2e}  log(iso/all) {lr:+.3f} ± {s:.3f}")
print(f"\n{len(L)} points inside 0.3 Mpc:  weighted mean log(isolated/all) = {m:+.4f} ± {e:.4f}  ({m/e:+.1f} sigma)  -> isolated pull {'harder' if m>0 else 'less'} by {100*(10**m-1):+.1f}%")
