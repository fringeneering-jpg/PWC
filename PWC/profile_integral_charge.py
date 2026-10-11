# Corrected spherical profile-integral fixed point (WvdM horizon + Lai ansatz + stable u)
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

eps0 = 8.8541878128e-12
hbar = 1.054571817e-34
c0 = 2.99792458e8
me = 9.1093837e-31
e = 1.602176634e-19
lamC = hbar/(me*c0)
r_hor = lamC/2.0              # rotational horizon radius = lamC_bar
R_tr  = lamC/(4.0*np.pi)      # transport radius (WvdM)
V = np.pi*lamC**3/6.0
U_target = me*c0**2/2.0

def fixed_point(n):
    def resid(qe):
        q = qe*e
        b = me**2*c0**3/(q*hbar)
        shape = lambda r: (r/r_hor)*np.exp((1-(r/r_hor)**n)/n)
        A = (q/(4*np.pi*eps0*R_tr**2))/shape(R_tr)
        Efn = lambda r: A*shape(r)
        u = lambda r: eps0*Efn(r)**2/(np.sqrt(1+eps0*Efn(r)**2/b**2)+1)
        U, _ = quad(lambda r: u(r)*4*np.pi*r**2, 1e-20, r_hor, limit=400)
        return U - U_target
    try:
        qe = brentq(resid, 0.5, 3.0, xtol=1e-14, maxiter=200)
    except ValueError as ex:
        # find where the sign changes
        vals = [(x, resid(x)) for x in np.linspace(0.5, 3.0, 8)]
        return None, vals
    a_inv = 4*np.pi*eps0*hbar*c0/((qe*e)**2)
    return qe, a_inv

print("n (profile) -> q/e, alpha^-1    [target 137.036]")
for n in (0.001, 0.05, 0.2, 0.5, 1.0, 2.0):
    res = fixed_point(n)
    if res[0] is None:
        print(f"n={n}: no sign change in [0.5,3]; resid:", [f'{v:+.1e}' for _,v in res[1]])
    else:
        print(f"n={n:5.3f} : q = {res[0]:.4f} e ;  alpha^-1 = {res[1]:.3f}")
