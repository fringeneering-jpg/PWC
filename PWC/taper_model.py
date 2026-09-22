import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

G = 6.674e-11; MSUN = 1.989e30
rho_core = 2.3e17       # real nuclear saturation density
rho_shell_max = 1.305e15  # real, ringdown-derived tonight, density right at the core surface

def R_of_M(Mc): return (3*Mc/(4*np.pi*rho_core))**(1/3)

def shell_mass(Mc, c_s):
    """Hydrostatic taper: d(ln rho)/dr = -g(r)/c_s^2, rho(Rc)=rho_shell_max.
    Compounding self-gravity included (M_enc grows as shell mass accumulates),
    but since rho strictly decays, this is well-behaved -- no runaway."""
    Rc = R_of_M(Mc)
    def rhs(r, y):
        M, lnrho = y
        rho = np.exp(lnrho)
        g = G*M/r**2
        dM = 4*np.pi*r**2*rho
        dlnrho = -g/c_s**2
        return [dM, dlnrho]
    def ev_tiny(r, y):
        return y[1] - np.log(rho_shell_max*1e-8)  # stop once density has fallen to ~1e-8 of its starting value
    ev_tiny.terminal = True
    ev_tiny.direction = -1
    r_scale = c_s**2 * Rc**2 / (G*Mc)  # rough scale-height estimate to set integration span
    rmax = Rc + max(r_scale*50, Rc*5)
    sol = solve_ivp(rhs, (Rc, rmax), [Mc, np.log(rho_shell_max)], events=ev_tiny,
                     max_step=(rmax-Rc)/2000, rtol=1e-9, atol=1e-6)
    Mfinal = sol.y[0,-1]
    return Mfinal - Mc

def core_from_apparent(Mapp, c_s):
    def f(Mc):
        return Mc + shell_mass(Mc, c_s) - Mapp
    return brentq(f, Mapp*0.05, Mapp, xtol=Mapp*1e-9)

m1, m2, Mf_obs = 35.6*MSUN, 30.6*MSUN, 63.1*MSUN

def calib_residual(log_cs):
    cs = 10**log_cs
    c1 = core_from_apparent(m1, cs)
    c2 = core_from_apparent(m2, cs)
    cf = c1+c2
    mf_pred = cf + shell_mass(cf, cs)
    return (mf_pred-Mf_obs)/MSUN

print("scanning c_s...")
for lg in np.arange(3, 8, 0.5):
    try:
        r = calib_residual(lg)
        print(f"  log10(c_s)={lg:.1f}  c_s={10**lg:.2e} m/s  residual={r:+.4f} Msun")
    except Exception as e:
        print(f"  log10(c_s)={lg:.1f}  FAILED: {e}")

print("\nextending scan toward c0...")
for lg in np.arange(7.5, 8.48, 0.1):
    try:
        r = calib_residual(lg)
        print(f"  log10(c_s)={lg:.2f}  c_s={10**lg:.3e} m/s  (c_s/c={10**lg/2.998e8:.4f})  residual={r:+.5f} Msun")
    except Exception as e:
        print(f"  log10(c_s)={lg:.2f}  FAILED: {e}")
