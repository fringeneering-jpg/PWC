# What aspect ratio does the saturated fixed point NEED to hit alpha^-1 = 137.036?
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

eps0 = 8.8541878128e-12
hbar = 1.054571817e-34
c0 = 2.99792458e8
me = 9.1093837e-31
e = 1.602176634e-19
lamC = hbar/(me*c0)
R_maj = lamC/2.0            # WvdM major radius = lamC/4pi
L = 2*2*np.pi*R_maj         # double-loop path = lamC
U_target = me*c0**2/2.0

def alpha_inv_for_tube(r0, n=0.02):
    # uniform-core (n->0) Born-Infeld fixed point over the cylindrical tube of radius r0
    def resid(qe):
        q = qe*e
        b = me**2*c0**3/(q*hbar)
        E0 = q/(2*np.pi*eps0*L*r0)          # cylindrical Gauss at the tube edge
        u_core = b**2*(np.sqrt(1+eps0*E0**2/b**2)-1)
        U = u_core*np.pi*r0**2*L            # uniform core approximation
        return U - U_target
    try:
        qe = brentq(resid, 0.2, 3.0, xtol=1e-13, maxiter=200)
    except ValueError:
        return None, None
    a_inv = 4*np.pi*eps0*hbar*c0/((qe*e)**2)
    return qe, a_inv

print("tube radius r0  |  R/r0  |  q/e  |  alpha^-1")
print("-"*52)
for r0 in (R_maj, 5e-14, 3e-14, 2.81794e-15, 1e-15, 5e-16):
    qe, a_inv = alpha_inv_for_tube(r0)
    if qe is None:
        print(f"{r0:.3e}  no root")
        continue
    print(f"{r0:.3e} | {R_maj/r0:7.1f} | {qe:5.3f} | {a_inv:9.3f}")

print("\n== The question ==")
print("target alpha^-1 = 137.036. What R/r0 lands there?  Solve numerically:")
def ratio_for_target():
    def f(log_r0):
        qe, a = alpha_inv_for_tube(np.exp(log_r0))
        return a - 137.036 if a is not None else 1e9
    from scipy.optimize import brentq as br
    lo, hi = np.log(1e-16), np.log(5e-14)
    try:
        log_r0 = br(f, lo, hi, xtol=1e-10, maxiter=200)
        r0 = np.exp(log_r0)
        qe, a = alpha_inv_for_tube(r0)
        return r0, R_maj/r0, qe, a
    except ValueError as ex:
        return None, None, None, str(ex)
r0, ratio, qe, a = ratio_for_target()
if r0:
    print(f"r0 = {r0:.4e} m ;  R/r0 = {ratio:.3f} ;  q/e = {qe:.5f} ;  alpha^-1 = {a:.3f}")
    print(f"compare: 1/alpha = {1/7.2973525693e-3:.1f} ;  (1/alpha)/2 = {1/(2*7.2973525693e-3):.1f}")
    print(f"        lambdaC_bar/r_e = {lamC/2.81794e-15:.1f}")
else:
    print("no solution in range:", a)
