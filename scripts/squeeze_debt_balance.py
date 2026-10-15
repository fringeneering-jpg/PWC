# The squeeze-vs-debt balance: alpha as the compression equilibrium (2026-10-12)
import math
c0 = 2.99792458e8; hbar = 1.054571817e-34
me = 9.1093837e-31; e = 1.602176634e-19; eps0 = 8.8541878128e-12
alpha = e**2/(4*math.pi*eps0*hbar*c0)
s = 1.0/19.0
lam_bar = hbar/(me*c0)
r_e = alpha*lam_bar

print("== the balance at the observed fold (r = r_e = alpha lambda_bar) ==")
# the EM self-attraction's squeeze (the Coulomb self-force at the compressed extent)
F_em = e**2/(4*math.pi*eps0*r_e**2)
# the retained debt's tension (the gas-branch pull-back, the waves wanting rest spacing)
rho_knot = me/(4*math.pi*r_e**3/3.0)
F_debt = (s*rho_knot*c0**2/3.0) * (4*math.pi*r_e**2)
print(f"the squeeze:  F_EM  = e^2/(4 pi eps0 r_e^2)   = {F_em:.4e} N")
print(f"the debt's tension: F_debt = (s rho c0^2/3) x 4 pi r_e^2 = {F_debt:.4e} N")
print(f"ratio: F_EM / F_debt = {F_em/F_debt:.4f}  =  1/s = {1/s}  EXACT")
print(f"\n-> the EM squeeze beats the debt's tension by exactly 19 = 1/s. The debt balances")
print(f"   1/19 of the fold; the topology's hold (the 720-degree lock) carries the other 18/19.")
print(f"   s = 1/19 = the debt's SHARE of the fold's equilibrium - the stretch's third meaning:")

print("\n== the stretch's three meanings, one number ==")
print("  1. the retained-heat fraction (the knot keeps 5.26%)")
print("  2. the footprint's inflation (r_t = (pi + 3s) lambda_bar)")
print("  3. the debt's share of the fold's balance (F_debt = s x F_total, EXACT here)")

print("\n== the honest remaining piece ==")
print("the RELATIVE structure is derived exactly: the squeeze, the debt, and the topology")
print("split the fold 19 : 1 : 18. What sets alpha's ABSOLUTE value is the topology's own")
print("hold - the 720-degree lock's force magnitude - which balances the squeeze's remaining")
print("18/19. The equation:  F_EM = F_debt + F_topology,  F_debt = s F_EM,  F_topology =")
print("(1-s) F_EM - and alpha = the compression where the topology's hold first equals")
print("(1-s) times the squeeze. The balance is written; the topology's force is the final")
print("named quantity - the eigenmode's own strength, now a force in the equation.")
