"""KiDS-1000 lensing RAR vs PWC / base / McGaugh (prediction frozen in PREDICTION_kids_lensing.md)."""
import numpy as np
G_PC = 4.52e-30; PC_M = 3.086e16; F = 4 * G_PC * PC_M
A_PWC, A_BASE, A_RAR = 6.6776e-11, 7.5586e-11, 1.1603e-10
def load(stem, bins=None):
    files = [f"{stem}_Nobins.txt"] if bins is None else [f"{stem}_{b}.txt" for b in bins]
    gb, go, bias = [], [], []
    for f in files:
        d = np.loadtxt(f); gb.append(d[:, 0]); go.append(F * d[:, 1] / d[:, 4]); bias.append(d[:, 4])
    c = np.loadtxt(f"{stem.replace('_Colorbin','_Colorbins').replace('_Sersicbin','_Sersicbins')}_covmatrix.txt")
    return np.concatenate(gb), np.concatenate(go), c
def cov_from(c, gb, nb):
    n = len(gb); C = np.zeros((n, n)); key = {}
    mvals = sorted(set(c[:, 0])); per = n // len(mvals)
    rad = gb[:per]
    for row in c:
        mi = mvals.index(row[0]); nj = mvals.index(row[1])
        i = mi * per + int(np.argmin(np.abs(rad - row[2]))); j = nj * per + int(np.argmin(np.abs(rad - row[3])))
        C[i, j] = F * F * row[4] / row[6]
    return C
pwc = lambda g: g + np.sqrt(A_PWC * g); base = lambda g: g + np.sqrt(A_BASE * g)
rar = lambda g: g / (1 - np.exp(-np.sqrt(g / A_RAR)))
def run(label, gb, go, C):
    Ci = np.linalg.inv(C); chi = lambda m: float((go - m(gb)) @ Ci @ (go - m(gb)))
    xp, xb, xm = chi(pwc), chi(base), chi(rar)
    off = np.median(np.log10(pwc(gb) / go)); offm = np.median(np.log10(rar(gb) / go))
    print(f"{label:28s} n={len(gb):>2}  chi2: PWC {xp:7.1f} | base {xb:7.1f} | McGaugh {xm:7.1f}   dchi2(PWC-McG) {xp-xm:+7.1f}   median log(model/obs): PWC {off:+.3f}  McG {offm:+.3f}")
    return xp, xm
for label, stem, bins in [("KiDS isolated (main)", "Fig-4-5-C1_RAR-KiDS-isolated", None),
                          ("KiDS isolated + hot gas", "Fig-4_RAR-KiDS-isolated_hotgas", None)]:
    gb, go, c = load(stem, bins); run(label, gb, go, cov_from(c, gb, 1))
for kind in ["Colorbin", "Sersicbin"]:
    stem = f"Fig-8_RAR-KiDS-isolated_{kind}"
    gb, go, c = load(stem, [1, 2]); C = cov_from(c, gb, 2); n = len(gb) // 2
    for b in (0, 1):
        s = slice(b * n, (b + 1) * n); run(f"{kind} {b+1} ({'blue/disc' if b==0 else 'red/bulge'})", gb[s], go[s], C[s, s])
gb, go, c = load("Fig-4-5-C1_RAR-KiDS-isolated")
print("\n g_bar        g_obs       PWC        McGaugh")
for a, b in zip(gb, go): print(f" {a:.3e}  {b:.3e}  {pwc(a):.3e}  {rar(a):.3e}")
