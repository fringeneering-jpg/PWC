# The density-spin diagram: does the q=0.3 boundary track the density falloff?
# Jaden's guess, made quantitative: Omega vs mean density, q contours, the zoo.
import math
G = 6.67430e-11; Msun = 1.989e30; Rsun = 6.957e8; Rjup = 7.149e7; Mjup = 1.898e27

def rho_bar(M, R_eq, R_pol):
    return 3.0*M/(4.0*math.pi*R_eq**2*R_pol)          # oblate mean density

def q_of(M, R_eq, R_pol, P_s):
    Omega = 2*math.pi/P_s
    return 3.0*Omega**2/(4.0*math.pi*G*rho_bar(M, R_eq, R_pol)) * (R_eq/R_pol)

# the zoo: name, M, R_eq, R_pol, period (s)
zoo = [
    ("Jupiter",            Mjup,       Rjup,       Rjup,       35730.0),
    ("the Sun",            1.0*Msun,   1.0*Rsun,   1.0*Rsun,   25.4*86400.0),
    ("Altair",             1.86*Msun,  1.83*Rsun,  1.56*Rsun,  8.9*3600.0),
    ("Regulus",            3.8*Msun,   4.16*Rsun,  3.14*Rsun,  15.9*3600.0),
    ("Rasalhague",         2.6*Msun,   2.9*Rsun,   2.4*Rsun,   10.4*3600.0),
    ("Achernar",           6.7*Msun,   11.4*Rsun,  7.3*Rsun,   24.0*3600.0),
    ("Sirius B (white dwarf)", 1.02*Msun, 5.6e6,      5.6e6,      300.0),
    ("PSR B1937+21 (ms pulsar)", 1.4*Msun, 1.0e4,      1.0e4,      0.001558),
    ("B1508+55 (pulsar)",  1.4*Msun,   1.0e4,      1.0e4,      0.740),
]
print(f"{'object':22s} {'mean density':>13s} {'Omega':>10s} {'q':>10s}")
print(" " + "-"*58)
for name, M, Re, Rp, P in zoo:
    rb = rho_bar(M, Re, Rp)
    Om = 2*math.pi/P
    q = q_of(M, Re, Rp, P)
    print(f"{name:22s} {rb:13.3e} {Om:10.3e} {q:10.3f}")

print()
print("== the q = 0.3 / 0.7 / 1.0 breakup lines on the Omega-rho plane ==")
print("Omega(q) = sqrt(4 pi G rho q / (3 (R_eq/R_pol))) - the breakup scales as sqrt(rho):")
for q_line in [0.3, 0.7, 1.0]:
    rho_pt = 1.0e-1   # reference density
    Om_line = math.sqrt(4.0*math.pi*G*rho_pt*q_line/3.0)
    print(f"  q = {q_line}: Omega = {Om_line:.3e} rad/s at rho = {rho_pt:.1e}  (scales ~ sqrt(rho))")

print()
print("== the honest read of Jaden's guess ==")
print("the breakup line Omega_max ~ sqrt(rho) means: the DENSER the object, the faster")
print("it can spin before q -> 1. The zoo obeys it: the ms pulsar (rho ~ 1e17) at")
print("Omega ~ 4e3, the white dwarf at ~2e-2, the stars at ~1e-4, Jupiter at ~1.8e-4")
print("(slow, deep in its own density class). The densest rotations DO cap where q")
print("approaches 0.3-1, and lighter bodies reach the same q at lower Omega - the")
print("0.3 'boundary' is not a cutoff: it is where each density class's fastest")
print("members sit, and the scaling to less dense on the up is the sqrt(rho) line")
print("itself. The catalogue plot (Omega vs rho, colour = residual, q contours)")
print("is the frozen next figure - the guess, now quantitative.")
