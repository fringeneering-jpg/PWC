# Literal-negative-baseline branch, fully prepared (trial form, awaiting Jaden's ruling)
import math
c0 = 2.99792458e8
c0sq = c0**2
rho0 = 8.74e-27
s = 1.0/19.0

print("== Literal branch: the vacuum's negative pressure = the constant pull term ==")
P_pull = (1-s)*rho0*c0sq/3.0
print(f"P_pull = (1-s) rho0 c0^2/3 = {P_pull:.4e} Pa   (the 'expansion pressure pushing out,"
      f" balanced by something pushing back' - PROVENANCE)")
print(f"P_net(rho) = (1-s)(rho - rho0) c0^2/3  ->  0 at rest; NEGATIVE below rest (stretch);")
print(f"positive above (compression).  The baseline 'wants to stretch' because any rarefaction")
print(f"tips P_net negative.")
stretch5 = rho0/1.053
P_net_s5 = (1-s)*(stretch5-rho0)*c0sq/3.0
Y_cav = s*rho0*c0sq/3.0
print(f"at the sealed 5.3% stretch (rho = rho0/1.053): P_net = {P_net_s5:.3e} Pa = "
      f"{P_net_s5/Y_cav:.3f} x Y_cav   (Y_cav = {Y_cav:.3e} Pa)")

# crossing: P_net = -Y_cav at what stretch?
x_cross = s/(1.0-s)                    # solve (1-s)(rho-rho0) c0^2/3 = -s rho0 c0^2/3 -> (rho0-rho)/rho0 = s/(1-s)
print(f"P_net = -Y_cav at stretch fraction (rho0-rho)/rho0 = s/(1-s) = 1/18 = "
      f"{100*x_cross:.3f}%")
print(f"  sealed stretch: 1/19 = {100*s:.3f}% ;  water: 6.4% ;  crossing: 5.56%")
print(f"  -> the net tension reaches -Y_cav within 6% of the sealed 5.3% stretch, and water's")
print(f"     6.4% cavitation stretch sits in the same class (cohesion report A6).")

print("\n== Dark-energy reading of the literal branch ==")
print(f"the vacuum's pressure datum is P_pull = {P_pull:.3e} Pa (negative, measured against the")
print(f"rigidity); net zero at rest.  Expansion = untying drops rho locally below rho0 ->")
print(f"P_net < 0 -> the region 'rips open' toward baseline - the mechanical tug-of-war,")
print(f"no dark energy term.  Trial form; the constancy of P_pull is the assumption Jaden")
print(f"would be signing (micro backing open).")

print("\n== Coupling-law candidate check (honest dead end) ==")
hbar = 1.05457e-34
e = 1.602176634e-19
mu0 = 4*math.pi*1e-7
a = (hbar/(rho0*c0))**0.25
mw = rho0*a**3/2.0
alpha = e**2/(4*math.pi*8.854187817e-12*hbar*c0)
lhs = mu0*e**2/(mw*a)
rhs = 8*math.pi*alpha
print(f"mu0 e^2/(m_w a) = {lhs:.5f} ;  8 pi alpha = {rhs:.5f}  -> match to {abs(lhs/rhs-1):.1e}")
print(f"BUT m_w*a = hbar/(2c0) exactly, so mu0 = 8 pi alpha * m_w a / e^2 reduces to")
print(f"mu0 = 1/(eps0 c0^2): the match is the identity mu0*eps0*c0^2 = 1, NOT a new result.")
print(f"-> the coupling datum stays eps0 itself; nothing closes it by arithmetic.")
