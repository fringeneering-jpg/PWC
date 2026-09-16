"""
DOMAIN NN -- derive the coefficient in a0 = (coefficient) * c0 * H0, or fail.

THE DEBT BEING CALLED IN. Domain HH and the PR both carry a0 = c0*H0/(2*pi).
The 2*pi has never been derived anywhere in this repository. It was asserted
as "one full topological cycle is 2*pi of phase". It is also, precisely, the
factor that turns a 5.64x miss into a 2.8% hit. A factor introduced at the one
step that needs a calculation, which happens to be the factor that makes the
answer work, is the same shape as the `* 43.0` this project already caught in
Medium_Density_Check.py. It is less bad, because 2*pi is the most natural
number in wave physics. It is still unearned.

THE RULE FOR THIS FILE. No coefficient is typed in anywhere. Each route below
computes its own, from its own stated physics, and whatever falls out is what
gets reported -- 1, pi, 2*pi, 4*pi, sqrt(2), or something that is not a
constant at all.

THE THREE ROUTES, each stated before it is run:

  ROUTE 1 -- THE CROSSING, DONE WITH A REAL STRAIN FIELD.
    This is the argument the framework actually makes: an inward pull that
    weakens with distance against an outward cosmic strain that does not, so
    they must cross, and the crossing is at a fixed ACCELERATION rather than a
    fixed distance. The step that has never been checked is what acceleration
    a uniform expansion actually exerts on a body at distance r. It is NOT a
    constant. Route 1 computes it and follows the consequence wherever it goes.

  ROUTE 2 -- THE HORIZON.
    c0*H0 is the surface gravity of the de Sitter horizon, and the standard
    way to reach it is to equate the Unruh temperature of an accelerated
    observer with the Gibbons-Hawking temperature of the cosmic horizon. Both
    of those formulas carry a 2*pi. Route 2 does the algebra and reports
    whether the 2*pi survives or cancels.

  ROUTE 3 -- WHAT THE DATA ACTUALLY DEMANDS.
    Read the coefficient straight off SPARC with no theory at all, with a
    galaxy-level bootstrap interval, and compare it to whatever routes 1 and 2
    produced.

Conclusion text is written after the numbers print. Not before.
"""
import json
import os

import numpy as np
from scipy.optimize import minimize_scalar

D = os.environ.get("PWC_SPARC_DIR", os.path.dirname(os.path.abspath(__file__)))

c0 = 2.99792458e8
G = 6.67430e-11
hbar = 1.054571817e-34
kB = 1.380649e-23
MPC = 3.0856775814913673e22
KPC = 3.0856775814913673e19
KMS = 1.0e3
Msun = 1.98892e30

H0_P = 67.4 * KMS / MPC
H0_L = 73.0 * KMS / MPC

results = {}


def hr(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


# ================================================================= ROUTE 1
hr("ROUTE 1 -- THE CROSSING, WITH A REAL STRAIN FIELD")

print("The inward term. Spherical diffusion of tension flux through 4*pi*r^2")
print("surfaces gives a 1/r^2 law. IMPORTANT BOOKKEEPING: that 4*pi is already")
print("inside G. Poisson's equation is div^2(Phi) = 4*pi*G*rho precisely so")
print("that g = G*M/r^2 comes out with no loose 4*pi. Multiplying by another")
print("4*pi here would be double counting the same geometry.\n")
print("    g_in(r) = G*M / r^2          [no free coefficient available]\n")

print("The outward term. This is the step never checked. What acceleration")
print("does a uniform expansion exert on a body at distance r?\n")
print("  A comoving separation obeys r(t) = a(t)*x, so")
print("      r_dot    = (a_dot/a) * r  = H * r        <- a VELOCITY, not an accel")
print("      r_dotdot = (a_dotdot/a) * r")
print("  For a de Sitter-like medium a_dotdot/a = H^2, so\n")
print("    g_out(r) = H0^2 * r          [linear in r, NOT constant]\n")
print("  The expansion does not push with a constant acceleration. It pushes")
print("  with a TIDAL acceleration that GROWS with distance. A uniform")
print("  velocity field cannot exert a uniform acceleration -- that is the")
print("  whole content of Hubble's law being a velocity law.\n")

print("Crossing condition g_in = g_out:")
print("    G*M/r^2 = H0^2*r   ->   r_cross = (G*M/H0^2)^(1/3)")
print("    a_cross = G*M/r_cross^2 = (G*M)^(1/3) * H0^(4/3)\n")
print("  The coefficient is exactly 1. No pi appears anywhere -- the only")
print("  geometric factor in the problem was absorbed into G before we began.")
print("  But a_cross depends on M^(1/3). It is NOT a universal acceleration.\n")

print(f"{'galaxy mass [Msun]':>20} {'r_cross':>14} {'a_cross [m/s^2]':>18} "
      f"{'r(g=a0_emp)':>14}")
a0_emp_placeholder = None
masses = [1e9, 1e10, 1e11, 1e12, 1e13]
r1 = []
for Mx in masses:
    M = Mx * Msun
    rc = (G * M / H0_P ** 2) ** (1.0 / 3.0)
    ac = G * M / rc ** 2
    r1.append((Mx, rc, ac))
    print(f"{Mx:>20.0e} {rc/MPC:>11.3f} Mpc {ac:>18.3e} {'':>14}")

spread = r1[-1][2] / r1[0][2]
print(f"\n  a_cross varies by {spread:.1f}x across 1e9 to 1e13 Msun.")
print("  A universal a0 cannot vary at all. This is already fatal for the")
print("  crossing as a source of a0, independent of any coefficient.")
results["route1"] = {
    "coefficient": 1.0,
    "form": "(G*M)^(1/3) * H0^(4/3)",
    "mass_dependent": True,
    "a_cross_1e12Msun": float(r1[3][2]),
    "r_cross_1e12Msun_Mpc": float(r1[3][1] / MPC),
    "spread_1e9_to_1e13": float(spread)}

# ================================================================= ROUTE 2
hr("ROUTE 2 -- THE HORIZON, AND WHETHER THE 2*pi SURVIVES")

print("Unruh: an observer with proper acceleration a sees a thermal bath")
print("    T_Unruh = hbar*a / (2*pi*c0*kB)\n")
print("Gibbons-Hawking: the de Sitter cosmic horizon has")
print("    T_dS = hbar*H0 / (2*pi*kB)\n")
print("The horizon argument sets the acceleration scale by equating them:\n")
print("    hbar*a/(2*pi*c0*kB) = hbar*H0/(2*pi*kB)\n")
print("The 2*pi appears on BOTH sides and cancels identically. So:\n")
print("    a = c0 * H0        coefficient EXACTLY 1\n")


def T_unruh(a):
    return hbar * a / (2 * np.pi * c0 * kB)


def T_ds(H):
    return hbar * H / (2 * np.pi * kB)


for lab, H in (("Planck 67.4", H0_P), ("local 73.0", H0_L)):
    a_h = c0 * H
    print(f"  [{lab}]  a = c0*H0 = {a_h:.4e} m/s^2")
    print(f"           check: T_Unruh(a) = {T_unruh(a_h):.6e} K, "
          f"T_dS(H0) = {T_ds(H):.6e} K, ratio {T_unruh(a_h)/T_ds(H):.12f}")
results["route2"] = {"coefficient": 1.0, "form": "c0*H0",
                     "a_planck": float(c0 * H0_P), "a_local": float(c0 * H0_L)}

print("\n  This independently confirms PROVENANCE_MANIFEST.md line 749. The")
print("  real Gibbons-Hawking derivation gives c0*H0 with NO 2*pi, because")
print("  the 2*pi is in both temperatures and divides out.")
print("\n  To KEEP a 2*pi you would have to equate T_Unruh(a) with something")
print("  other than T_dS. Solving T_Unruh(a) = X for the a the data wants:")
a0_for_check = 1.1603e-10
print(f"    T_Unruh({a0_for_check:.3e}) = {T_unruh(a0_for_check):.4e} K")
print(f"    T_dS(H0 local)             = {T_ds(H0_L):.4e} K")
print(f"    ratio                      = {T_unruh(a0_for_check)/T_ds(H0_L):.4f}")
print("  Nothing in the thermodynamics picks that ratio out.")

# ================================================================= ROUTE 3
hr("ROUTE 3 -- WHAT THE DATA DEMANDS, WITH NO THEORY AT ALL")


def read_vizier_tsv(path, cols):
    L = [l.rstrip("\n") for l in open(path, encoding="utf-8", errors="replace")]
    h = next(i for i, l in enumerate(L)
             if not l.startswith("#") and l.strip() and "\t" in l and "recno" in l)
    nm = L[h].split("\t")
    d = max(i for i in range(h + 1, min(h + 6, len(L)))
            if set(L[i].replace("\t", "").strip()) <= set("- "))
    ix = {c: nm.index(c) for c in cols}
    o = {c: [] for c in cols}
    for l in L[d + 1:]:
        if not l.strip() or l.startswith("#"):
            continue
        f = l.split("\t")
        if len(f) < len(nm):
            continue
        try:
            for c in cols:
                v = f[ix[c]].strip()
                o[c].append(v if c == "Name"
                            else (float(v) if v not in ("", "---") else np.nan))
        except ValueError:
            continue
    return o


t1 = read_vizier_tsv(os.path.join(D, "vizier_t1.txt"), ["Name", "i", "Qual"])
t2 = read_vizier_tsv(os.path.join(D, "vizier_t2.txt"),
                     ["Name", "Rad", "Vobs", "e_Vobs", "Vgas", "Vdisk", "Vbulge"])
inc = dict(zip(t1["Name"], t1["i"]))
qual = dict(zip(t1["Name"], t1["Qual"]))
nm = np.array(t2["Name"])
R = np.array(t2["Rad"], float)
Vo = np.array(t2["Vobs"], float)
e = np.array(t2["e_Vobs"], float)
Vg = np.nan_to_num(np.array(t2["Vgas"], float))
Vd = np.array(t2["Vdisk"], float)
Vb = np.nan_to_num(np.array(t2["Vbulge"], float))
ia = np.array([inc.get(x, np.nan) for x in nm], float)
qa = np.array([qual.get(x, np.nan) for x in nm], float)
m = (R > 0) & (Vo > 0) & np.isfinite(e) & (e / Vo <= .10) & (ia >= 30) & (qa <= 2)
R, Vo, Vg, Vd, Vb, nm = R[m], Vo[m], Vg[m], Vd[m], Vb[m], nm[m]
cv = (KMS ** 2) / KPC
go = Vo ** 2 / R * cv
gb = (Vg * np.abs(Vg) + 0.5 * Vd * np.abs(Vd) + 0.7 * Vb * np.abs(Vb)) / R * cv
k = (gb > 0) & (go > 0)
go, gb, nm, R = go[k], gb[k], nm[k], R[k]
y = np.log10(go)


def rar(g, a):
    return g / (1 - np.exp(-np.sqrt(g / a)))


o = minimize_scalar(lambda l: np.mean((y - np.log10(rar(gb, 10 ** l))) ** 2),
                    bounds=(-11.5, -9), method="bounded")
a0_emp = 10 ** o.x
gal = np.array(sorted(set(nm)))
rng = np.random.default_rng(11)
bs = []
for _ in range(400):
    pick = rng.choice(gal, len(gal), replace=True)
    idx = np.concatenate([np.where(nm == g)[0] for g in pick])
    yy, gg = y[idx], gb[idx]
    oo = minimize_scalar(lambda l: np.mean((yy - np.log10(rar(gg, 10 ** l))) ** 2),
                         bounds=(-11.5, -9), method="bounded")
    bs.append(10 ** oo.x)
bs = np.array(bs)

print("  a0 measured from SPARC, no theory input:")
print("    best fit %.4e m/s^2" % a0_emp)
print("    68%% interval %.4e to %.4e" % (np.percentile(bs, 16), np.percentile(bs, 84)))
print("\n  The coefficient the data demands, k = a0 / (c0*H0):\n")
print(f"{'H0 source':<14} {'c0*H0':>12} {'k best':>9} {'k 68% interval':>24}")
kk = {}
for lab, H in (("Planck 67.4", H0_P), ("local 73.0", H0_L)):
    cH = c0 * H
    kb = a0_emp / cH
    klo, khi = np.percentile(bs, 16) / cH, np.percentile(bs, 84) / cH
    kk[lab] = (kb, klo, khi)
    print(f"{lab:<14} {cH:>12.4e} {kb:>9.4f} {klo:>11.4f} to {khi:.4f}")

print("\n  Candidate closed forms, and whether the data's interval contains them:")
cands = [("1", 1.0), ("1/2", 0.5), ("1/pi", 1 / np.pi), ("1/4", 0.25),
         ("1/(2*pi)", 1 / (2 * np.pi)), ("1/(sqrt(2)*pi)", 1 / (np.sqrt(2) * np.pi)),
         ("1/(4*pi)", 1 / (4 * np.pi)), ("1/6", 1 / 6), ("sqrt(3*0.315/(8*pi))", np.sqrt(3 * 0.315 / (8 * np.pi)))]
print(f"{'form':<22} {'value':>8} {'in Planck 68%?':>16} {'in local 68%?':>16}")
for nmk, v in cands:
    ip = kk["Planck 67.4"][1] <= v <= kk["Planck 67.4"][2]
    il = kk["local 73.0"][1] <= v <= kk["local 73.0"][2]
    print(f"{nmk:<22} {v:>8.4f} {str(ip):>16} {str(il):>16}")
results["route3"] = {
    "a0_empirical": float(a0_emp),
    "a0_68": [float(np.percentile(bs, 16)), float(np.percentile(bs, 84))],
    "k_planck": list(map(float, kk["Planck 67.4"])),
    "k_local": list(map(float, kk["local 73.0"])),
    "candidates": {n: float(v) for n, v in cands}}

# ================================================================= ROUTE 1 vs a0
hr("ROUTE 1 CHECKED DIRECTLY AGAINST a0 -- IS THE CROSSING EVEN IN THE GALAXY?")

print("For each mass: the radius where g = a0 (the rotation-curve transition)")
print("versus the radius where gravity crosses the cosmic strain.\n")
print(f"{'M [Msun]':>10} {'r(g=a0) [kpc]':>15} {'r_cross [kpc]':>15} {'ratio':>9} "
      f"{'a_cross/a0':>12}")
for Mx, rc, ac in r1:
    M = Mx * Msun
    r_a0 = np.sqrt(G * M / a0_emp)
    print(f"{Mx:>10.0e} {r_a0/KPC:>15.2f} {rc/KPC:>15.2f} {rc/r_a0:>9.1f} "
          f"{ac/a0_emp:>12.3e}")
results["route1_vs_a0"] = {
    "a_cross_over_a0_1e12": float(r1[3][2] / a0_emp),
    "r_ratio_1e12": float(r1[3][1] / np.sqrt(G * 1e12 * Msun / a0_emp))}

# ================================================================= VERDICT
hr("VERDICT -- written after the numbers, not before")

kp, kpl, kph = kk["Planck 67.4"]
kl, kll, klh = kk["local 73.0"]
inv2pi = 1 / (2 * np.pi)

print("THE 2*pi IS NOT DISCHARGED. It is worse than that.\n")
print("1. ROUTE 2 settles the coefficient cleanly and the answer is 1, not")
print("   1/(2*pi). The 2*pi appears in the Unruh temperature AND in the")
print("   Gibbons-Hawking temperature and cancels identically when they are")
print("   equated. This independently reproduces manifest line 749. There is")
print("   no version of the horizon argument that leaves a 2*pi behind.\n")
print("2. ROUTE 1 does not fail on its coefficient -- it fails on its FORM.")
print("   A uniform expansion exerts g_out = H0^2 * r, which is linear in r,")
print("   not constant. Hubble's law is a velocity law; a uniform velocity")
print("   field cannot produce a uniform acceleration. So the crossing gives")
print("     a_cross = (G*M)^(1/3) * H0^(4/3),  coefficient exactly 1,")
print("   which is MASS DEPENDENT -- it varies by %.0fx from 1e9 to 1e13 Msun."
      % spread)
print("   A universal a0 cannot vary at all.\n")
print("3. And the crossing is not even in the right place. For a 1e12 Msun")
print("   galaxy the rotation-curve transition g = a0 sits at %.0f kpc, while"
      % (np.sqrt(G * 1e12 * Msun / a0_emp) / KPC))
print("   gravity crosses the cosmic strain at %.0f kpc -- %.0fx further out,"
      % (r1[3][1] / KPC, r1[3][1] / np.sqrt(G * 1e12 * Msun / a0_emp)))
print("   at an acceleration %.0fx SMALLER than a0. That radius is the known"
      % (a0_emp / r1[3][2]))
print("   turnaround / zero-velocity surface of a galaxy group. It is a real")
print("   boundary, and it is a Local-Group-scale boundary, not a galaxy-edge")
print("   one. It is not where rotation curves go flat.\n")
print("4. What the data demands, read off with no theory:")
print("     k = a0/(c0*H0) = %.4f  [68%%: %.4f to %.4f]  using Planck H0"
      % (kp, kpl, kph))
print("     k = a0/(c0*H0) = %.4f  [68%%: %.4f to %.4f]  using local  H0"
      % (kl, kll, klh))
print("   1/(2*pi) = %.4f. It sits %s the local interval and %s the Planck one."
      % (inv2pi,
         "inside" if kll <= inv2pi <= klh else "OUTSIDE",
         "inside" if kpl <= inv2pi <= kph else "OUTSIDE"))
print("   But being inside an interval is not a derivation. Several other")
print("   simple forms sit in there too, as the candidate table shows.\n")
print("5. WHAT THIS COSTS THE FRAMEWORK, STATED PLAINLY. The claim I endorsed")
print("   two messages ago -- that PWC supplies a MECHANISM for why a0 is an")
print("   acceleration scale, via a crossing -- does not survive this")
print("   calculation. Done with a real strain field the crossing produces a")
print("   mass-dependent acceleration at a Local-Group radius. The mechanism")
print("   I called 'rock solid' is wrong, and I should not have called it")
print("   that before doing the integral.\n")
print("6. WHAT SURVIVES. a0 ~ c0*H0 is still a real numerical coincidence,")
print("   and the horizon route gives coefficient 1 from actual")
print("   thermodynamics -- which lands %.2fx off the measured value. That is"
      % (1.0 / kl))
print("   a genuine, unexplained factor of about %.1f, and it is exactly where"
      % (1.0 / kl))
print("   the unearned 2*pi was being used to paper over the gap.")

out = os.path.join(D, "domain_NN_a0_coefficient_results.json")
with open(out, "w") as f:
    json.dump(results, f, indent=2, sort_keys=True)
print(f"\nwrote {out}")
