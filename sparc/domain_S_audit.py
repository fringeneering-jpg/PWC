"""
Domain S audit (items 1, 2, 3 -- no new optimizer run, per instruction).
Uses the ALREADY-FITTED parameters from domain_S_coupled_hdf.py exactly as
they came out (rho_gal=6.8494e-22, c_s0=5.2940e4, chi0=0.300994) -- the
point here is to diagnose WHY that run produced a flat/uniform-density
branch, not to refit anything.
"""
import numpy as np, json
from scipy.integrate import solve_ivp
import domain_S_coupled_hdf as S

RHO_GAL = 6.8494e-22
C_S0 = 5.2940e4
CHI0 = 0.300994

def hr(t): print("\n"+"="*78); print(t); print("="*78)

hr("ITEM 2: UNITS / SCALE DIAGNOSTIC at a typical outer point")
# pick a representative galaxy and radius near 10 kpc
target_gal = None
for g, gd in S.gal_data.items():
    if gd["r"].max()/S.KPC > 8 and gd["r"].max()/S.KPC < 15:
        target_gal = g; break
if target_gal is None:
    target_gal = list(S.gal_data.keys())[0]
gd = S.gal_data[target_gal]
r_test = np.interp(10.0*S.KPC, gd["r"], gd["r"])  # nearest tabulated point to 10 kpc
idx = np.argmin(np.abs(gd["r"]-10.0*S.KPC))
r_test = gd["r"][idx]
gbar_test = gd["gbar"][idx]
Mbar_test = gbar_test*r_test**2/S.G

chi = CHI0
rho_HDF = S.RHO_BG + RHO_GAL*chi
g_pred_approx = S.G*Mbar_test/r_test**2  # approx, M_HDF small at this stage
term = rho_HDF*g_pred_approx*(1-chi) / ((S.RHO_MAX-S.RHO_BG)*C_S0**2)
print(f"galaxy used: {target_gal}, r = {r_test/S.KPC:.2f} kpc")
print(f"rho_HDF   = {rho_HDF:.4e} kg/m^3")
print(f"g_pred    = {g_pred_approx:.4e} m/s^2")
print(f"c_s0      = {C_S0:.4e} m/s")
print(f"term (=|dchi/dr|, units 1/m) = {term:.6e}")
print(f"1/term    = {1/term:.6e} m = {1/term/S.KPC:.6e} kpc")
print(f"  (this is the characteristic length scale over which chi actually")
print(f"   changes, given the rho_max-normalized denominator)")

hr("ITEM 3: CHI DEFINITION / SCALE MISMATCH CHECK")
chi_true_galaxy_scale = RHO_GAL*CHI0 / (S.RHO_MAX - S.RHO_BG)
print(f"If chi is genuinely a compact-saturation fraction (rho_max-normalized),")
print(f"a galaxy-scale excess of rho_gal*chi0 = {RHO_GAL*CHI0:.4e} kg/m^3")
print(f"corresponds to a TRUE saturation fraction of only:")
print(f"  (rho_gal*chi0)/(rho_max-rho_bg) = {chi_true_galaxy_scale:.4e}")
print(f"but the code initialized and evolved chi starting at chi0={CHI0} directly --")
print(f"a mismatch of {CHI0/chi_true_galaxy_scale:.4e}x between the value chi actually")
print(f"took and the value consistent with its own governing equation's normalization.")

hr("ITEM 1: ACTUAL RADIAL PROFILES for 10 representative galaxies")
# pick 10 galaxies spanning mass / gas fraction / surface brightness extremes
cands = []
for g, gd in S.gal_data.items():
    Mbar_out = gd["gbar"][-1]*gd["r"][-1]**2/S.G
    cands.append((g, Mbar_out, gd["r"][-1]))
cands.sort(key=lambda x: x[1])
n = len(cands)
picks = set()
for frac in [0.05, 0.15, 0.3, 0.5, 0.7, 0.85, 0.95]:
    picks.add(cands[int(frac*(n-1))][0])
# pad to 10 with a few more spread out
extra_idx = [1, n//4, 3*n//4]
for i in extra_idx:
    picks.add(cands[i][0])
picks = list(picks)[:10]

profile_records = {}
for gname in picks:
    gd = S.gal_data[gname]
    res = S.integrate_galaxy(gd, RHO_GAL, C_S0, CHI0)
    if res is None:
        print(f"{gname}: INTEGRATION FAILED"); continue
    r_kpc = res["r"]/S.KPC
    chi_arr = res["chi"]
    rho_excess = RHO_GAL*S.f_chi(chi_arr)
    MHDF = res["MHDF"]
    Mbar = res["Mbar"]
    gpred = res["gpred"]
    gbar = gd["gbar"]
    vpred = np.sqrt(gpred*res["r"])
    vobs = np.sqrt(gd["gobs"]*res["r"])

    # local log slopes over outer 3-5 points
    def logslope(y, x):
        ly, lx = np.log(np.maximum(y,1e-300)), np.log(x)
        n_pts = min(5, len(x))
        return np.polyfit(lx[-n_pts:], ly[-n_pts:], 1)[0]
    alpha_rho = logslope(rho_excess, res["r"]) if np.all(rho_excess[-5:]>0) else float("nan")
    alpha_M = logslope(np.maximum(MHDF,1e-10), res["r"])
    alpha_v = logslope(vpred, res["r"])

    print(f"\n--- {gname}  (Mbar_out={Mbar[-1]:.3e} kg, r_out={r_kpc[-1]:.2f} kpc) ---")
    print(f"  chi range: [{chi_arr.min():.6f}, {chi_arr.max():.6f}]  (delta={chi_arr.max()-chi_arr.min():.3e})")
    print(f"  outer alpha_rho={alpha_rho:.3f} (target -2)  alpha_M={alpha_M:.3f} (target +1)  alpha_v={alpha_v:.3f} (target 0)")
    print(f"  M_HDF/M_bar at r_out: {MHDF[-1]/Mbar[-1]:.3e}")

    profile_records[gname] = dict(r_kpc=r_kpc.tolist(), chi=chi_arr.tolist(),
        rho_excess=rho_excess.tolist(), MHDF=MHDF.tolist(), Mbar=Mbar.tolist(),
        gpred=gpred.tolist(), gbar=gbar.tolist(), vpred=vpred.tolist(), vobs=vobs.tolist(),
        alpha_rho=float(alpha_rho), alpha_M=float(alpha_M), alpha_v=float(alpha_v))

json.dump(profile_records, open(f"{S.D}/domain_S_audit_profiles.json","w"), indent=2)
print(f"\nprofiles saved -> {S.D}\\domain_S_audit_profiles.json")
