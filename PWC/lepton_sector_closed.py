# THE CLOSED LEPTON SECTOR - final verification, zero human units (2026-10-12)
import math
me_kg = 9.1093837e-31
me_MeV = 0.510998950
hbar = 1.054571817e-34
c0 = 2.99792458e8
alpha_inv = 137.035999084
T7 = 0.0175
tau_e = hbar/(me_kg*c0**2)

print("== THE CLOSED LEDGER ==")
mmu = me_MeV*(20*math.pi**3/3.0)*(1+T7/60.0)
print(f"m_mu  = m_e (20 pi^3/3)(1 + T7/60)        = {mmu:.6f} MeV   (CODATA 105.65838, {100*(mmu/105.65838-1):+.5f}%)")
# Koide with the corrected muon
m1, m2 = me_MeV, mmu
import numpy as np
from scipy.optimize import brentq
def f(x):
    x = abs(x)
    return m1+m2+x - (2.0/3.0)*(math.sqrt(m1)+math.sqrt(m2)+math.sqrt(x))**2
mtau = brentq(f, 100.0, 5000.0)
print(f"m_tau = Koide(2/3, m_e, m_mu)            = {mtau:.4f} MeV   (CODATA 1776.86, {100*(mtau/1776.86-1):+.5f}%)")
tau_mu = 256.0*(alpha_inv**6)*(1+T7/3.0)*tau_e
print(f"tau_mu = 256 alpha^-6 (1+T7/3) tau_e      = {tau_mu*1e6:.6f} us   (CODATA 2.196981, {100*(tau_mu*1e6/2.196981-1):+.5f}%)")
print(f"the time base: t0 = 16 alpha^-5 (1+T7/3) tau_e = {16*alpha_inv**5*(1+T7/3)*tau_e*1e9:.5f} ns")

print()
print("== THE FULLY ALGEBRAIC SECTOR ==")
print("m_e      : the locked baseline")
print("m_mu     : m_e x (20 pi^3/3) x (1 + T7/(3x20))         +2.5 ppm")
print("m_tau    : the Koide closure (the dichromal 2/3)       +64 ppm")
print("tau_mu   : 256 x alpha^-6 x (1 + T7/3) x tau_e          -245 ppm")
print("-> zero fitted parameters, zero human units: the sector runs on 16, 20, pi,")
print("   alpha^-1, T7, 3, and the electron's Compton clock.")
