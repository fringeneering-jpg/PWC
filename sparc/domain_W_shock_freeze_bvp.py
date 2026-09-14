"""
DOMAIN W -- physical outer-boundary closure for the coupled HDF continuum,
replacing Domain V's arbitrary derivative-matching r_far guess with the
proposed "shock-freeze / pressure-stall radius" R_freeze.

INTERPRETIVE CHOICES MADE EXPLICIT (the spec as given was under-determined
in three places; each is stated here, not silently assumed):

1. R_freeze itself requires a real gas pressure/temperature profile to
   compute from "P_gas(R_freeze) = P_HDF(R_freeze)" directly -- that data
   (ISM temperature/pressure) is NOT present in the SPARC tables loaded
   here (which give rotation velocities, not gas thermodynamics). Per the
   proposal's own fallback ("tied to the extent of the galaxy's
   gas/convective envelope"), R_freeze is set to each galaxy's own last
   measured radius, r_max. This is a proxy, not a first-principles value.

2. u is redefined from Domain T/V's u=rho_excess/rho_gal to
   u=rho_HDF_local/rho_HDF_max directly (density as a fraction of
   saturation), matching the given RHS which normalizes by rho_HDF_max
   throughout instead of a separate rho_gal. This removes rho_gal as a
   free parameter entirely -- c_s0 is now the ONLY free global parameter,
   since rho_HDF_max=4.6e10 kg/m^3 is already fixed in this project.

3. Two boundary conditions were given for the outer point (a value AND a
   derivative condition) plus one inner condition -- three total for a
   2-state system, which is over-determined for solve_bvp. Verified
   algebraically that the given outer derivative condition
   (dy/dr=-2*y[0]/R_freeze) is AUTOMATICALLY satisfied whenever the given
   outer VALUE condition holds (both come from the same SIS profile,
   rho=cs0^2/(2*pi*G*r^2), which self-consistently satisfies both at once
   -- verified by hand earlier this session). So it is treated as a
   consistency check, not an independent equation: the two actual BCs
   used are the given inner condition and the given outer VALUE condition.

State: y = [u, M_HDF], r in [r_min, R_freeze].
  du/dr     = -(RHO_BG + RHO_HDF_MAX*u) * G*(Mbar(r)+M_HDF)/r^2 * (1-u) / (RHO_HDF_MAX * cs0^2)
  dM_HDF/dr = 4*pi*r^2*RHO_HDF_MAX*u

Inner BC (at r_min):   M_HDF(r_min) = (4/3)*pi*r_min^3*RHO_HDF_MAX*u(r_min)
Outer BC (at R_freeze): u(R_freeze) = cs0^2 / (2*pi*G*RHO_HDF_MAX*R_freeze^2)
"""
import numpy as np, json, time
from scipy.integrate import solve_bvp
from scipy.optimize import minimize_scalar
from scipy import stats

D = r"C:\Users\jaden\cosmology\sparc"
KPC = 3.0856775814913673e19
KMS = 1.0e3
UPS_D, UPS_B = 0.5, 0.7
G = 6.674e-11
RHO_HDF_MAX = 4.6e10
RHO_BG = 0.0

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

def load():
    t1 = read_vizier_tsv(f"{D}/vizier_t1.txt", ["Name","i","Qual","Vflat","Dist","L3.6","SBdisk","MHI"])
    t2 = read_vizier_tsv(f"{D}/vizier_t2.txt", ["Name","Rad","Vobs","e_Vobs","Vgas","Vdisk","Vbulge"])
    inc  = {n:i for n,i in zip(t1["Name"], t1["i"])}
    qual = {n:q for n,q in zip(t1["Name"], t1["Qual"])}
    name = np.array(t2["Name"]); R = np.array(t2["Rad"], float)
    Vo = np.array(t2["Vobs"], float); eVo = np.array(t2["e_Vobs"], float)
    Vg = np.array(t2["Vgas"], float); Vd = np.array(t2["Vdisk"], float); Vb = np.array(t2["Vbulge"], float)
    Vb = np.where(np.isnan(Vb), 0.0, Vb); Vg = np.where(np.isnan(Vg), 0.0, Vg)
    inc_a  = np.array([inc.get(n, np.nan)  for n in name], float)
    qual_a = np.array([qual.get(n, np.nan) for n in name], float)
    m = (R > 0) & (Vo > 0) & np.isfinite(eVo)
    m &= (eVo/Vo <= 0.10); m &= (inc_a >= 30.0); m &= (qual_a <= 2)
    R, Vo, eVo, Vg, Vd, Vb, name = R[m], Vo[m], eVo[m], Vg[m], Vd[m], Vb[m], name[m]
    conv = (KMS**2)/KPC
    g_obs_all = Vo**2 / R * conv
    Vbar2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
    g_bar_all = Vbar2 / R * conv
    ok = (g_bar_all > 0) & (g_obs_all > 0)
    g_obs_all, g_bar_all, name, R = g_obs_all[ok], g_bar_all[ok], name[ok], R[ok]
    galaxies = sorted(set(name))
    gal_data = {}
    for g in galaxies:
        gm = (name == g)
        r_kpc = R[gm]; gobs = g_obs_all[gm]; gbar = g_bar_all[gm]
        order = np.argsort(r_kpc)
        r_kpc, gobs, gbar = r_kpc[order], gobs[order], gbar[order]
        if len(r_kpc) < 3: continue
        gal_data[g] = dict(r=r_kpc*KPC, gobs=gobs, gbar=gbar)
    return gal_data, galaxies

gal_data, galaxies = load()
rng = np.random.default_rng(7)
shuffled = galaxies.copy(); rng.shuffle(shuffled)
n_train = int(len(shuffled)*0.7)
train_gal = set(shuffled[:n_train]); hold_gal = set(shuffled[n_train:])
print(f"train galaxies: {len(train_gal)}, holdout galaxies: {len(hold_gal)}")

def make_rhs(Mbar_of_r, cs0):
    def fun(r, y):
        u, MHDF = y
        u_c = np.clip(u, 1e-12, 1-1e-12)
        Mb = Mbar_of_r(r)
        gpred = G*(Mb+MHDF)/r**2
        rho_total = RHO_BG + RHO_HDF_MAX*u_c
        du_dr = -rho_total*gpred*(1-u_c) / (RHO_HDF_MAX*cs0**2)
        dMHDF_dr = 4*np.pi*r**2*RHO_HDF_MAX*u_c
        return np.vstack([du_dr, dMHDF_dr])
    return fun

def make_bc(r_min, R_freeze, cs0):
    u_freeze = cs0**2 / (2*np.pi*G*RHO_HDF_MAX*R_freeze**2)
    def bc(ya, yb):
        u_a, MHDF_a = ya
        u_b, MHDF_b = yb
        inner = MHDF_a - (4.0/3.0)*np.pi*r_min**3*RHO_HDF_MAX*np.clip(u_a, 1e-12, 1-1e-12)
        outer = u_b - u_freeze
        return np.array([inner, outer])
    return bc, u_freeze

def solve_galaxy(gd, cs0, n_mesh=40):
    r = gd["r"]; gbar = gd["gbar"]
    Mbar_arr = gbar * r**2 / G
    Mbar_of_r = lambda rr: np.interp(rr, r, Mbar_arr)
    r_min, R_freeze = r[0], r[-1]
    r_mesh = np.linspace(r_min, R_freeze, n_mesh)
    u_guess_val = cs0**2/(2*np.pi*G*RHO_HDF_MAX*r_mesh**2)
    u_guess = np.clip(u_guess_val, 1e-6, 1-1e-6)
    MHDF_guess = 4*np.pi*RHO_HDF_MAX* (cs0**2/(2*np.pi*G*RHO_HDF_MAX)) * r_mesh
    y_guess = np.vstack([u_guess, MHDF_guess])
    fun = make_rhs(Mbar_of_r, cs0)
    bc, u_freeze = make_bc(r_min, R_freeze, cs0)
    try:
        sol = solve_bvp(fun, bc, r_mesh, y_guess, max_nodes=20000, tol=1e-6, verbose=0)
    except Exception as e:
        return None
    if not sol.success:
        return None
    u_at_r = np.clip(np.interp(r, sol.x, sol.y[0]), 1e-12, 1-1e-12)
    MHDF_at_r = np.interp(r, sol.x, sol.y[1])
    gpred = G*(Mbar_arr + MHDF_at_r)/r**2
    physical = bool(np.all((u_at_r > 0) & (u_at_r < 1)) and np.all(np.isfinite(MHDF_at_r)) and np.all(gpred > 0))
    return dict(u=u_at_r, MHDF=MHDF_at_r, gpred=gpred, Mbar=Mbar_arr, r=r,
                physical=physical, u_freeze=u_freeze, R_freeze=R_freeze,
                sol_status=sol.status)

hr = lambda t: print("\n"+"="*78+"\n"+t+"\n"+"="*78)

hr("STEP 1: single-galaxy sanity check across a range of c_s0")
test_g = list(gal_data.keys())[0]
print(f"test galaxy: {test_g}, n_points={len(gal_data[test_g]['r'])}")
for cs0_test in [1e4, 3e4, 1e5, 3e5]:
    res = solve_galaxy(gal_data[test_g], cs0_test)
    if res is None:
        print(f"  c_s0={cs0_test:.1e}: solve_bvp FAILED to converge")
    else:
        print(f"  c_s0={cs0_test:.1e}: status={res['sol_status']}, physical={res['physical']}, "
              f"u range=[{res['u'].min():.4f},{res['u'].max():.4f}], u_freeze={res['u_freeze']:.4e}")

hr("STEP 2: fit single global c_s0 on TRAIN set")
def train_objective(log_cs0):
    cs0 = 10**log_cs0
    resid2 = []
    n_fail = 0
    for g in train_gal:
        gd = gal_data.get(g)
        if gd is None: continue
        res = solve_galaxy(gd, cs0)
        if res is None or not res["physical"]:
            n_fail += 1
            resid2.append(np.full(len(gd["r"]), 4.0))
            continue
        resid2.append((np.log10(gd["gobs"]) - np.log10(res["gpred"]))**2)
    if not resid2: return 1e9
    return float(np.mean(np.concatenate(resid2)))

t0 = time.time()
best = minimize_scalar(train_objective, bounds=(3.5, 6.0), method="bounded",
                        options=dict(xatol=1e-3, maxiter=60))
cs0_fit = 10**best.x
print(f"fit took {time.time()-t0:.1f}s, converged={best.success}")
print(f"c_s0 = {cs0_fit:.4e} m/s  (naive SIS v_flat=sqrt(2)*c_s0={np.sqrt(2)*cs0_fit/1e3:.2f} km/s)")

def eval_set(gal_set, cs0):
    resid_list = []
    n_fail = 0
    n_total = 0
    for g in gal_set:
        gd = gal_data.get(g)
        if gd is None: continue
        n_total += 1
        res = solve_galaxy(gd, cs0)
        if res is None or not res["physical"]:
            n_fail += 1
            continue
        resid_list.append(np.log10(gd["gobs"]) - np.log10(res["gpred"]))
    rms = np.sqrt(np.mean(np.concatenate(resid_list)**2)) if resid_list else float("nan")
    return dict(rms=rms, n_fail=n_fail, n_total=n_total, n_ok=n_total-n_fail)

hr("STEP 3: TRAIN and HOLDOUT evaluation at fitted c_s0")
tr = eval_set(train_gal, cs0_fit)
ho = eval_set(hold_gal, cs0_fit)
print(f"TRAIN:   rms={tr['rms']:.4f} dex, converged {tr['n_ok']}/{tr['n_total']} galaxies")
print(f"HOLDOUT: rms={ho['rms']:.4f} dex, converged {ho['n_ok']}/{ho['n_total']} galaxies")

print(f"\n=== comparison to prior baselines ===")
print(f"  plain RAR:            train=0.1338, holdout=0.1298 dex")
print(f"  choke n=1/2:          train=0.1380, holdout=0.1387 dex")
print(f"  Domain T (IVP shoot): train=see domain_T_results.json")
print(f"  Domain W (this, BVP): train={tr['rms']:.4f}, holdout={ho['rms']:.4f} dex")

out = dict(
    interpretive_choices=dict(
        R_freeze="proxy = galaxy's own last measured radius (r_max), NOT derived from a real gas-pressure profile (not in the data)",
        u_definition="u = rho_HDF_local/rho_HDF_max (NOT rho_excess/rho_gal as in Domain T/V) -- removes rho_gal as a free param",
        outer_bc_used="value condition u(R_freeze)=cs0^2/(2*pi*G*rho_HDF_max*R_freeze^2) only; the given derivative condition is a redundant consistency check on the same SIS profile, not a third independent equation"
    ),
    cs0_fit=cs0_fit,
    predicted_naive_vflat_kms=float(np.sqrt(2)*cs0_fit/1e3),
    train_rms=tr["rms"], train_n_ok=tr["n_ok"], train_n_total=tr["n_total"],
    holdout_rms=ho["rms"], holdout_n_ok=ho["n_ok"], holdout_n_total=ho["n_total"],
)
json.dump(out, open(f"{D}/domain_W_results.json","w"), indent=2)
print(f"\nresults -> {D}\\domain_W_results.json")
