# Is the 0.085% residual the matter itself? Test the displacement reading (2026-10-09)
import math
hbar = 1.054571817e-34; c0 = 2.99792458e8; me = 9.1093837e-31
e = 1.602176634e-19; eps0 = 8.8541878128e-12
rho_max = 1.304e15
lamC_bar = hbar/(me*c0); lamC = 2*math.pi*lamC_bar
alpha = e**2/(4*math.pi*eps0*hbar*c0)
g = 16*math.pi**3*alpha/3.0
r_t_target = lamC/math.sqrt(3*g)
r_t_model = (math.pi + 3.0/19.0)*lamC_bar
s = 1.0/19.0

print(f"linear residual: {100*(r_t_target/r_t_model-1):+.4f}%")
V_target = 4*math.pi*r_t_target**3/3.0
V_model  = 4*math.pi*r_t_model**3/3.0
V_res = V_target - V_model
print(f"volume residual: {100*(V_res/V_target):+.4f}% of the fold = {V_res:.3e} m^3")

print("\n== candidate 'matter volumes' vs the residual ==")
cands = {
  "m_e/rho_max (the tight sphere at the plateau)": me/rho_max,
  "the wave tube pi r_e^2 lamC": math.pi*(alpha*lamC_bar)**2*lamC,
  "the hairpin sphere 4pi/3 r_e^3": 4*math.pi*(alpha*lamC_bar)**3/3.0,
  "the tight sphere at rho_core (2.3e17)": me/2.3e17,
  "residual volume (itself)": V_res,
}
for name, v in cands.items():
    print(f"  {name:44s} = {v:.3e} m^3   ({100*v/V_res:.4f}% of the residual)")

print("\n== the implied density if the residual IS the matter ==")
rho_implied = me/V_res
print(f"rho = m_e/V_res = {rho_implied:.3e} kg/m^3")
print(f"vs rho_max = {rho_max:.3e} ; rho_core = {2.3e17:.3e} ; gate 7.475e16 ; rho0 = 8.74e-27")
print(f"rho_implied/rho_max = {rho_implied/rho_max:.4e}")
print(f"-> the residual volume is 3.2e7x the tight sphere: the displacement is NOT matter at")
print(f"   rho_max. The implied density (4.1e7) has no locked match. The ONTOLOGY stands")
print(f"   (the gap = the matter; a perfect hit = the empty fluid) - the quantitative")
print(f"   measure of 'the matter's own volume in the footprint' remains open.")
print(f"\nnote: s^2 = {s**2*100:.3f}% sits near the volume residual {100*V_res/V_target:.3f}%"
      f" (-7.6%) - reported, no mechanism.")
