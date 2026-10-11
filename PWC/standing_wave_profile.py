# The standing wave's transverse profile: the last computation (2026-10-09)
import math
hbar = 1.054571817e-34; c0 = 2.99792458e8; me = 9.1093837e-31
e = 1.602176634e-19; eps0 = 8.8541878128e-12
lamC = 2*math.pi*hbar/(me*c0)
lamC_bar = hbar/(me*c0)
R = lamC/(4*math.pi)
alpha = e**2/(4*math.pi*eps0*hbar*c0)
g = 16*math.pi**3*alpha/3.0
r_t_target = lamC/math.sqrt(3*g)
print(f"target tube: r_t = {r_t_target/1e-12:.4f} pm = {r_t_target/lamC_bar:.4f} lamC_bar")

print("\n== 1. The coherent ring mode (Gaussian, 720-degree closure) ==")
w0_max = math.sqrt(lamC*R/(2*math.pi))
print(f"ring curvature R = lamC/4pi ; mode match needs R_phase = R at some z in [0,R]")
print(f"max solvable waist w0 = sqrt(lamC R / 2pi) = {w0_max/lamC_bar:.4f} lamC_bar")
print(f"-> the ring is too curved: the coherent mode CANNOT exceed 0.71 lamC_bar.")
print(f"   The target tube (3.30 lamC_bar) is 4.7x beyond the coherent limit.")
print(f"   KILL: the tube is NOT a coherent Gaussian mode.")

print("\n== 2. The transverse phase closure (2 pi r_t = n lamC) ==")
for n in (1,2,3,4):
    print(f"   n = {n}: r_t = {n} lamC_bar")
print(f"   target = 3.3020 lamC_bar - not an integer: the pure transverse closure")
print(f"   is OUT as the full story (the dynamic footprint carries the 0.30).")

print("\n== 3. The zitter amplitude ==")
a_z = lamC_bar/2.0
print(f"free zitter amplitude = lamC_bar/2 = 0.50 lamC_bar ; diameter = 1.00 lamC_bar")
print(f"target/pi = {r_t_target/(math.pi*lamC_bar):.4f} lamC_bar -> r_t sits at pi x (zitter diameter) x 1.051")

print("\n== 4. alpha-dressed compositions (reported, not claimed) ==")
print(f"pi sqrt(21/19) = {math.pi*math.sqrt(21/19):.4f}  vs 3.3020  ({100*(math.pi*math.sqrt(21/19)/3.3020-1):+.3f}%)")
print(f"10/3          = {10/3:.4f}  vs 3.3020  ({100*((10/3)/3.3020-1):+.3f}%)")
print(f"pi (20/19)    = {math.pi*20/19:.4f}  vs 3.3020  ({100*(math.pi*20/19/3.3020-1):+.3f}%)")

print("\n== verdict ==")
print(f"The coherent and quantized routes are dead with numbers. The tube (3.30 lamC_bar) is")
print(f"the DYNAMIC footprint: the zitter sweep (diameter lamC_bar) plus the self-spread, at")
print(f"~pi x the zitter diameter. The exact 1.051 dressing (pi sqrt(21/19) sits +0.025% away)")
print(f"is the last unknown - it is the equilibrium of the wave's self-field spreading the")
print(f"sweep against the phase-lock. That equilibrium is a dynamical computation, now fully")
print(f"specified: zitter diameter lamC_bar, self-repulsion of the loop charge, target 3.3020.")
