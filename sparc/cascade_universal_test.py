"""
Cascade equation, tested for real universality across the full SPARC sample.

Question: does ONE coefficient c in
    dM_med/dr = dM_bar/dr + c * M_med(r) / r
(the compounding-shadow "every bit that pulls, pulls a bit" mechanism,
independently derived 2026-09-22 -- see PWC.md section 10) reproduce real
observed rotation curves across MANY real galaxies simultaneously, not just
one toy disk -- with c fit ONCE, globally, not per galaxy.

Data: Lelli, McGaugh & Schombert 2016, AJ 152, 157 (SPARC), same
vizier_t1.txt / vizier_t2.txt already used elsewhere in this project.
Upload both files alongside this script to run in Colab.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar

KPC = 3.0856775814913673e19
KMS = 1.0e3
G = 6.674e-11
UPS_D, UPS_B = 0.5, 0.7   # standard SPARC 3.6um mass-to-light ratios

def read_vizier_tsv(path, cols):
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8", errors="replace")]
    hdr_i = None
    for i, l in enumerate(lines):
        if l.startswith("#") or not l.strip(): continue
        if "\t" in l and "recno" in l: hdr_i = i; break
    names = lines[hdr_i].split("\t")
    dash_i = None
    for i in range(hdr_i+1, min(hdr_i+6, len(lines))):
        if set(lines[i].replace("\t","").strip()) <= set("- "): dash_i = i
    idx = {c: names.index(c) for c in cols}
    out = {c: [] for c in cols}
    for l in lines[dash_i+1:]:
        if not l.strip() or l.startswith("#"): continue
        f = l.split("\t")
        if len(f) < len(names): continue
        try:
            for c in cols:
                v = f[idx[c]].strip()
                out[c].append(v if c == "Name" else (float(v) if v not in ("","---") else np.nan))
        except ValueError:
            continue
    return out

def load_sparc(D="."):
    t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name","i","Qual","Vflat","Dist"])
    t2 = read_vizier_tsv(f"{D}/vizier_t2.txt",
                         ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
    inc  = {n:i for n,i in zip(t1["Name"], t1["i"])}
    qual = {n:q for n,q in zip(t1["Name"], t1["Qual"])}
    name = np.array(t2["Name"]); R = np.array(t2["Rad"], float); Vo = np.array(t2["Vobs"], float)
    eVo  = np.array(t2["e_Vobs"], float); Vg = np.array(t2["Vgas"], float)
    Vd   = np.array(t2["Vdisk"], float); Vb = np.array(t2["Vbulge"], float)
    Vb = np.where(np.isnan(Vb), 0.0, Vb); Vg = np.where(np.isnan(Vg), 0.0, Vg)
    inc_a  = np.array([inc.get(n, np.nan)  for n in name], float)
    qual_a = np.array([qual.get(n, np.nan) for n in name], float)
    m = (R > 0) & (Vo > 0) & np.isfinite(eVo)
    m &= (eVo/Vo <= 0.10)
    m &= (inc_a >= 30.0)
    m &= (qual_a <= 2)
    R, Vo, Vg, Vd, Vb, name = R[m], Vo[m], Vg[m], Vd[m], Vb[m], name[m]
    Vbar2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
    Vbar = np.where(Vbar2 > 0, np.sqrt(Vbar2), 0.0)

    gal_data = {}
    for g in sorted(set(name)):
        mm = (name == g)
        r  = R[mm]*KPC; vb = Vbar[mm]*KMS; vo = Vo[mm]*KMS
        order = np.argsort(r)
        r, vb, vo = r[order], vb[order], vo[order]
        if len(r) >= 5:
            gal_data[g] = (r, vb, vo)
    return gal_data

def cascade_predict(r, vb, c):
    """Solve dM_med/dr = dM_bar/dr + c*M_med/r along this galaxy's own
    real radius grid, using its own real baryonic velocity curve as the
    source term. Returns predicted total velocity at each real data point."""
    Mbar = r * vb**2 / G                      # implied enclosed baryonic mass, real data
    dMbar_dr = np.gradient(Mbar, r)
    def rhs(rr, Mmed):
        dmb = np.interp(rr, r, dMbar_dr)
        return dmb + c*Mmed[0]/rr
    sol = solve_ivp(rhs, (r[0], r[-1]), [0.0], t_eval=r, method="RK45",
                     rtol=1e-6, max_step=(r[-1]-r[0])/200)
    Mmed = np.clip(sol.y[0], 0, None)
    Mtot = Mbar + Mmed
    return np.sqrt(G*Mtot/r)

def galaxy_balanced_rms(gal_data, galaxies, c):
    logs = []
    for g in galaxies:
        r, vb, vo = gal_data[g]
        try:
            vp = cascade_predict(r, vb, c)
        except Exception:
            continue
        resid = np.log10(vo) - np.log10(np.clip(vp, 1e-3, None))
        logs.append(np.sqrt(np.mean(resid**2)))
    return float(np.mean(logs)) if logs else np.inf

if __name__ == "__main__":
    gal_data = load_sparc(".")
    galaxies = list(gal_data.keys())
    print(f"Galaxies loaded: {len(galaxies)}")

    rng = np.random.default_rng(0)
    idx = rng.permutation(len(galaxies))
    n_train = int(0.7*len(galaxies))
    train = [galaxies[i] for i in idx[:n_train]]
    holdout = [galaxies[i] for i in idx[n_train:]]
    print(f"Train: {len(train)}  Holdout: {len(holdout)}")

    print("\nFitting ONE universal coefficient c on the train set...")
    obj = lambda c: galaxy_balanced_rms(gal_data, train, c)
    res = minimize_scalar(obj, bounds=(0.01, 5.0), method="bounded",
                           options={"xatol":1e-3})
    c_fit = res.x
    print(f"Best-fit universal c = {c_fit:.4f}")

    rms_train_baseline = galaxy_balanced_rms(gal_data, train, 0.0)   # c=0 -> baryons only
    rms_train_cascade  = galaxy_balanced_rms(gal_data, train, c_fit)
    rms_hold_baseline  = galaxy_balanced_rms(gal_data, holdout, 0.0)
    rms_hold_cascade   = galaxy_balanced_rms(gal_data, holdout, c_fit)

    print(f"\nTRAIN   baryons-only (c=0): {rms_train_baseline:.4f} dex")
    print(f"TRAIN   cascade (c={c_fit:.3f}):     {rms_train_cascade:.4f} dex")
    print(f"HOLDOUT baryons-only (c=0): {rms_hold_baseline:.4f} dex")
    print(f"HOLDOUT cascade (c={c_fit:.3f}):     {rms_hold_cascade:.4f} dex")
    print(f"\nReference: this project's existing choke/a0 fit ~0.138 dex,")
    print(f"McGaugh published RAR benchmark ~0.130-0.133 dex.")
