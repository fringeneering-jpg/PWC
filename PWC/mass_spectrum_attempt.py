# The particle mass spectrum: the honest attempt with the framework's anchors
import math
me = 0.510998950    # MeV
mmu = 105.6583755
mtau = 1776.86
mp = 938.27208816
s = 1.0/19.0
phi = (1+math.sqrt(5))/2

print("== the anchors already locked ==")
print(f"m_p/m_e = 1836.15 observed; the framework's 4 lam_C/R_p = 1835.79 (-0.02%)")
print(f"the electron: 1 quantum (m_e lam_C c0 = hbar); the proton: 4 quanta (m_p R_p c0 = 4 hbar)")
print()

print("== 1. The lepton ladder: candidates for m_mu/m_e = 206.7683 ==")
cands = {
    "(4pi)^3/ (206.77?)": (4*math.pi)**3/206.7683,
    "phi^11": phi**11,
    "16 x phi^8": 16*phi**8,
    "3 x 16 x phi^3": 3*16*phi**3,
    "(5 pi^2)^2 / 4.7": (5*math.pi**2)**2/4.7,
    "pi^3 x 16 / 2.4": math.pi**3*16/2.4,
    "1/(3s)^2": 1/(3*s)**2,
    "1/(s)^2 x 3/8": 1/(s**2)*3/8,
    "1/s^2 / 1.75": (1/s**2)/1.75,
}
for k, v in cands.items():
    print(f"  {k:26s} = {v:9.3f}   (target 206.768)")
print()

print("== 2. The tau: m_tau/m_e = 3477.2 ==")
cands2 = {
    "206.77^1.5": 206.7683**1.5,
    "(4pi)^5 / 36": (4*math.pi)**5/36,
    "(5 pi^2)^2": (5*math.pi**2)**2,
    "16^2 x phi^6": 16**2*phi**6,
    "1/s^3 / 7.8": (1/s**3)/7.8,
}
for k, v in cands2.items():
    print(f"  {k:26s} = {v:9.1f}   (target 3477.2)")
print()

print("== 3. The Koide relation with the framework's own (2/3) ==")
koide = (me+mmu+mtau) / ((math.sqrt(me)+math.sqrt(mmu)+math.sqrt(mtau))**2 * (2.0/3.0))
print(f"Koide: (m_e+m_mu+m_tau) / [(2/3)(sum sqrt m)^2] = {koide:.6f}  (exact = 1)")
print("the (2/3) = the dichromal fold's +2/3 - the framework's own fractional charge;")
print("the three generations = the three-fold... the relation holds to 5 decimal places,")
print("and the framework's charge geometry carries the exact prefactor. But the SPECTRUM")
print("(why 206.77 and 3477.2) is not produced by any locked composition tried above.")

print()
print("== the honest verdict ==")
print("the anchors hold (the proton/electron ratio at -0.02%, the quantizations); the")
print("Koide prefactor is the framework's own 2/3; but the mass LADDER's values are the")
print("same open question as the 16-mode eigenproblem - and they are ONE problem: the")
print("particle masses ARE the eigenvalues of L_PWC. Tonight's honest state: the spectrum")
print("is the eigenmode spectrum, the operator's structure is written, and the ladder's")
print("numbers remain the named target - no combination closes, nothing faked.")
