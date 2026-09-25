"""Red-but-spinning Lelli 2017 ETGs: spinning calibration vs KiDS-red a0 (prediction frozen in PREDICTION_red_vs_still.md)."""
import numpy as np, pandas as pd, glob, os
from scipy.special import ellipk
G = 4.30091e-6; CONV = 1e6 / 3.0856775814913673e19; H = 0.2
S = 0.2264; A_SPIN = 6.6776e-11; A_RED = 2.7286e-10
def ring_gr(r, a, m, dr=1e-3):
    pot = lambda rr: -(2 * G * m / np.pi) * ellipk(4 * a * rr / ((a + rr) ** 2 + H ** 2)) / np.sqrt((a + rr) ** 2 + H ** 2)
    return -(pot(r + dr) - pot(r - dr)) / (2 * dr)
import sys; UPS = float(sys.argv[1]); slow = {"NGC3522"}; rows = []
for f in sorted(glob.glob("rm/*_rotmod.dat")):
    name = os.path.basename(f).split("_")[0]
    d = np.loadtxt(f); R, V, eV, Vg, Vd, Vb = d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 4], d[:, 5]
    vb2 = UPS * Vb * np.abs(Vb); vbar2 = Vg * np.abs(Vg) + UPS * Vd * np.abs(Vd) + vb2
    ok = (R > 0) & (vbar2 > 0) & (V > 0); R, V, vbar2, vb2 = R[ok], V[ok], vbar2[ok], vb2[ok]
    gb = vbar2 / R; go = V ** 2 / R
    M = np.maximum(gb * R ** 2 / G, 0); dm = np.clip(np.diff(np.concatenate([[0.0], M])), 0, None)
    a = np.concatenate([[R[0] / 2], (R[1:] + R[:-1]) / 2])
    gin = np.array([-ring_gr(r, a, dm)[a < r].sum() for r in R]); gout = np.array([ring_gr(r, a, dm)[a > r].sum() for r in R])
    shared = np.clip(np.minimum(gin, gout) / np.where(gin > 0, gin, np.nan), 0, 1); shared = np.nan_to_num(shared)
    locked = np.clip(vb2 / vbar2, 0, 1)
    gbs, gos = gb * CONV, go * CONV
    pwc = lambda A: gbs + np.sqrt(A * gbs) * (1 + S * shared * (1 - locked))
    rms = lambda p: np.sqrt(np.mean((np.log10(gos) - np.log10(p)) ** 2))
    rows.append(dict(gal=name, n=len(R), slow=name in slow, spin=rms(pwc(A_SPIN)), red=rms(pwc(A_RED)),
                     medlog=np.median(np.log10(gos / pwc(A_SPIN))), outer_gbar=np.log10(gbs[-1])))
t = pd.DataFrame(rows)
sp = t[~t.slow]
print(f"\nSPINNING ETGs (n={len(sp)}): galaxy-balanced RMS  spinning a0 {sp.spin.mean():.4f}  |  KiDS-red a0 {sp.red.mean():.4f}   -> spinning better in {int((sp.spin<sp.red).sum())}/{len(sp)}")
s1 = t[t.slow]
print(f"NGC3522 (slow): spinning a0 {s1.spin.iloc[0]:.3f}  |  red a0 {s1.red.iloc[0]:.3f}")
t.to_csv(f"red_vs_still_ups{UPS}.csv", index=False)
