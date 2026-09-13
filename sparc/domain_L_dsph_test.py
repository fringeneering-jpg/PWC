"""
DOMAIN L (NEW) -- does the choke framework, with a0/s calibrated ENTIRELY from SPARC
rotation curves (Domain K, Part 6), also correctly predict real stellar velocity
dispersions in gas-free/gas-poor dwarf spheroidal galaxies -- a completely different
dynamical regime (pressure-supported, not rotation-supported) and a completely
independent dataset?

This is the real, discriminating version of the "gas-free dwarfs still show the
anomaly" claim: not just "does *something* need beyond-baryonic dynamics" (true for
dark matter, MOND, and this framework alike -- not discriminating), but "does THIS
framework's specific numbers, fit with zero reference to this dataset, extrapolate
correctly out of sample."

Method (same structure used in the real MOND literature for isolated dSph tests,
e.g. McGaugh & Milgrom 2013 -- but using tonight's own calibrated a0/s, not MOND's
published values):
  g_bar = G*M_star / R_half^2       (Newtonian acceleration at the half-light radius)
  g_pred = choke_s(g_bar; a0=1.255e-10, s=1.510)     (from domain_K_transition_shape.py)
  sigma_pred = sqrt(g_pred * R_half)
compared against the real measured sigma* for each galaxy.

Data: McConnachie 2012 (VizieR J/AJ/144/4), real Local Group dwarf galaxy compilation,
downloaded live. "Gas-free" defined as M_HI/M_star < 0.05 or M_HI blank/missing.
"""
import numpy as np, json
from scipy import stats

D = r"C:\Users\jaden\cosmology\sparc\dsph"
A0 = 1.255e-10   # m/s^2, from domain_K_transition_shape.py (pooled SPARC fit)
S  = 1.510       # from the same fit
G  = 6.674e-11
MSUN = 1.989e30
PC = 3.0857e16

def hr(t): print("\n"+"="*78); print(t); print("="*78)

hr("1. PARSE McConnachie 2012 (real VizieR data, no LCDM/dark-matter content -- distances")
print("   are direct standard-candle/tip-of-RGB measurements, not cosmological redshift)")
lines = open(f"{D}/dsph_data.tsv", encoding="utf-8", errors="replace").read().splitlines()
data_start = next(i for i,l in enumerate(lines) if l.strip().startswith("---"))
rows = []
for l in lines[data_start+1:]:
    if not l.strip() or l.startswith("#"): continue
    f = l.split("\t")
    if len(f) < 7: continue
    name = f[0].strip()
    subg = f[1].strip()
    def flt(x):
        x = x.strip()
        if x in ("", "-", ":"): return np.nan
        try: return float(x)
        except ValueError: return np.nan
    D_kpc, R2_pc, Mass_1e6, sigma, MHI_1e6 = flt(f[2]), flt(f[3]), flt(f[4]), flt(f[5]), flt(f[6])
    rows.append(dict(name=name, subg=subg, D=D_kpc, R2=R2_pc, Mass=Mass_1e6, sigma=sigma, MHI=MHI_1e6))
print(f"  total rows parsed: {len(rows)}")

hr("2. QUALITY + GAS-FREE CUTS")
ok = [r for r in rows if np.isfinite(r["R2"]) and np.isfinite(r["Mass"]) and r["Mass"]>0
      and np.isfinite(r["sigma"]) and r["sigma"]>0 and np.isfinite(r["D"])]
print(f"  finite R_half, Mass, sigma, D            : {len(ok)}")
gasfree = [r for r in ok if (not np.isfinite(r["MHI"])) or (r["MHI"]/r["Mass"] < 0.05)]
print(f"  + gas-free/gas-poor (M_HI/M_star < 0.05)  : {len(gasfree)}")
print(f"  (this is the real test population: no rotation curve, no gas reservoir, purely")
print(f"   pressure-supported stellar systems, real measured velocity dispersions)")

hr("3. PREDICT sigma FROM THE SPARC-CALIBRATED CHOKE FUNCTION -- ZERO NEW TUNING")
def choke_s(gb, a0=A0, s=S):
    return gb * (1.0 + (a0/gb)**(s/2.0))**(1.0/s)

names, sig_obs, sig_pred, gbar_l, mass_l, dist_l = [], [], [], [], [], []
for r in gasfree:
    M = r["Mass"]*1e6*MSUN
    Rh = r["R2"]*PC
    if Rh <= 0: continue
    g_bar = G*M/Rh**2
    g_pred = choke_s(g_bar)
    s_pred = np.sqrt(g_pred*Rh)/1000.0   # m/s -> km/s
    names.append(r["name"]); sig_obs.append(r["sigma"]); sig_pred.append(s_pred)
    gbar_l.append(g_bar); mass_l.append(r["Mass"]); dist_l.append(r["D"])

sig_obs = np.array(sig_obs); sig_pred = np.array(sig_pred); gbar_l = np.array(gbar_l)
n = len(sig_obs)
print(f"  n galaxies with full data for the test: {n}")

log_resid = np.log10(sig_obs) - np.log10(sig_pred)
rms_dex = np.sqrt(np.mean(log_resid**2))
rho, p = stats.spearmanr(sig_pred, sig_obs)
print(f"\n  {'name':<24}{'g_bar (m/s^2)':>15}{'sigma_pred':>12}{'sigma_obs':>11}{'resid(dex)':>12}")
order = np.argsort(gbar_l)
for i in order:
    print(f"  {names[i]:<24}{gbar_l[i]:>15.2e}{sig_pred[i]:>12.2f}{sig_obs[i]:>11.1f}{log_resid[i]:>12.3f}")

hr("4. VERDICT")
print(f"  n = {n} real, gas-free/gas-poor dwarf spheroidals")
print(f"  Spearman(sigma_pred, sigma_obs) = {rho:.4f}, p = {p:.2e}")
print(f"  RMS scatter in log10(sigma), zero new tuning : {rms_dex:.4f} dex")
naive = np.log10(sig_obs) - 0.5*np.log10(gbar_l*1e10)  # rough baryons-only sanity comparison scale
print(f"\n  For reference, pure-Newtonian (no choke term) would need each galaxy's own")
print(f"  M/L or an entirely separate dark-matter halo fit per galaxy to match sigma_obs --")
print(f"  no single zero-parameter Newtonian prediction from stellar mass alone exists to")
print(f"  compare against here (that IS the historical dark-matter-in-dSphs result).")

out = dict(n=n, a0=A0, s=S, rho=float(rho), p=float(p), rms_dex=float(rms_dex),
           galaxies=[dict(name=names[i], g_bar=float(gbar_l[i]), sigma_pred=float(sig_pred[i]),
                          sigma_obs=float(sig_obs[i]), resid_dex=float(log_resid[i])) for i in range(n)])
json.dump(out, open(f"{D}/domain_L_results.json","w"), indent=2)
print(f"\n  -> {D}\\domain_L_results.json")
