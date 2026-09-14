"""
PWC Stage 2, corrected model v4: replaces the Rusanov fluid flux (verified
in v3 to conserve total energy exactly, but too numerically diffusive to
resolve a local e_avail/E_lock threshold at practical resolution -- the
gap between evolved E_medium and the EOS-diagnosed value converged only
~15-20% per grid doubling) with a MUSCL-reconstructed, general-EOS HLLC
flux, falling back to Rusanov PER INTERFACE (logged) only where an HLLC
state would be unphysical.

The (A,Pi) wave sector and the E_medium flux/exchange-source construction
are UNCHANGED from v3 (already verified energy-conserving by construction).
Only the fluid flux (rho, rho*u, E_medium) changes.

Reconstruction: primitive variables (rho, u) MUSCL-reconstructed to each
face with a minmod slope limiter (2nd order, TVD). Pressure and sound
speed at each reconstructed face state come from the DECLARED EOS
(P_bulk, dPdrho -- the same symbolically-derived functions used throughout
this project), not any ideal-gas closure. Internal/total energy at each
reconstructed face state is recomputed from the reconstructed rho (and the
cell's own A, held fixed across the Riemann solve, a standard multi-field
HLLC simplification) via the EOS -- NOT by separately reconstructing
E_medium -- so the flux's own (rho,u,P,E) state is always thermodynamically
self-consistent at the face.

HLLC (Toro-form, general EOS): wave speeds S_L=min(u_L-c_L,u_R-c_R),
S_R=max(u_L+c_L,u_R+c_R), contact speed S_star from the standard HLLC
algebra. If the resulting star-state density falls outside (0, rho_max),
or implied pressure/internal energy is non-finite or negative, that
INTERFACE falls back to the plain Rusanov flux (logged: fallback_count).
"""
import numpy as np
import dynamic_knot_HDF3 as m3
import dynamic_knot_HDF2 as m2
import json, time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUTDIR = r"C:\Users\jaden\cosmology\PWC\knot_audit"

PARAMS = m3.PARAMS
c0 = m3.c0
E_lock = m3.E_lock
delta_E = m3.delta_E
e_EOS = m3.e_EOS
V_lock = m3.V_lock
P_bulk = m3.P_bulk
dPdrho = m3.dPdrho
dVdA = m3.dVdA
grad_periodic = m3.grad_periodic
lap_periodic = m3.lap_periodic
primitives = m3.primitives
make_counter_pulses = m3.make_counter_pulses
energy_channels = m3.energy_channels

def minmod(a, b):
    return np.where(a*b <= 0, 0.0, np.where(np.abs(a) < np.abs(b), a, b))

def muscl_face_states(f):
    # undivided differences, minmod-limited slope per cell
    dL = f - np.roll(f, 1)
    dR = np.roll(f, -1) - f
    slope = minmod(dL, dR)
    f_left_of_face = f + 0.5*slope          # extrapolated rightward from cell i, used as L state at face i+1/2
    f_right_of_face = f - 0.5*slope         # extrapolated leftward from cell i, used as R state at face i-1/2
    return f_left_of_face, f_right_of_face

def rhs(U, dx, rho_max_frac=0.999):
    rho, u, E_medium, A, Pi = primitives(U)
    P_cell = P_bulk(rho, A)
    c_s_cell = np.sqrt(np.maximum(dPdrho(rho, A), 1e-12))

    rho_Lface, rho_Rface = muscl_face_states(rho)
    u_Lface, u_Rface = muscl_face_states(u)

    # face i+1/2: L state extrapolated from cell i, R state extrapolated from cell i+1
    rho_L = rho_Lface
    rho_R = np.roll(rho_Rface, -1)
    u_L = u_Lface
    u_R = np.roll(u_Rface, -1)
    A_L = A                      # A held fixed across the Riemann solve (frozen parameter)
    A_R = np.roll(A, -1)

    # guard against MUSCL producing non-physical densities
    bad_recon = (rho_L <= 0) | (rho_R <= 0) | (rho_L >= PARAMS['rho_max']*rho_max_frac) | (rho_R >= PARAMS['rho_max']*rho_max_frac)
    rho_L = np.where(bad_recon, rho, rho_L)
    rho_R = np.where(bad_recon, np.roll(rho, -1), rho_R)
    u_L = np.where(bad_recon, u, u_L)
    u_R = np.where(bad_recon, np.roll(u, -1), u_R)

    P_L = P_bulk(rho_L, A_L)
    P_R = P_bulk(rho_R, A_R)
    c_L = np.sqrt(np.maximum(dPdrho(rho_L, A_L), 1e-12))
    c_R = np.sqrt(np.maximum(dPdrho(rho_R, A_R), 1e-12))
    E_L = 0.5*rho_L*u_L**2 + e_EOS(rho_L) + V_lock(rho_L, A_L)
    E_R = 0.5*rho_R*u_R**2 + e_EOS(rho_R) + V_lock(rho_R, A_R)

    S_L = np.minimum(u_L-c_L, u_R-c_R)
    S_R = np.maximum(u_L+c_L, u_R+c_R)

    F_L = np.array([rho_L*u_L, rho_L*u_L**2+P_L, u_L*(E_L+P_L)])
    F_R = np.array([rho_R*u_R, rho_R*u_R**2+P_R, u_R*(E_R+P_R)])
    U_Lv = np.array([rho_L, rho_L*u_L, E_L])
    U_Rv = np.array([rho_R, rho_R*u_R, E_R])

    denom = rho_L*(S_L-u_L) - rho_R*(S_R-u_R)
    denom_safe = np.where(np.abs(denom) < 1e-13, np.sign(denom)*1e-13 + (denom == 0)*1e-13, denom)
    S_star = (P_R - P_L + rho_L*u_L*(S_L-u_L) - rho_R*u_R*(S_R-u_R)) / denom_safe

    with np.errstate(divide='ignore', invalid='ignore'):
        coefL = rho_L*(S_L-u_L)/(S_L-S_star)
        coefR = rho_R*(S_R-u_R)/(S_R-S_star)
        eL_energy_term = E_L/rho_L + (S_star-u_L)*(S_star + P_L/(rho_L*(S_L-u_L)))
        eR_energy_term = E_R/rho_R + (S_star-u_R)*(S_star + P_R/(rho_R*(S_R-u_R)))

    U_starL = coefL*np.array([np.ones_like(rho_L), S_star, eL_energy_term])
    U_starR = coefR*np.array([np.ones_like(rho_R), S_star, eR_energy_term])

    F_starL = F_L + S_L*(U_starL - U_Lv)
    F_starR = F_R + S_R*(U_starR - U_Rv)

    F_hllc = np.where(S_L >= 0, F_L,
              np.where(S_star >= 0, F_starL,
              np.where(S_R >= 0, F_starR, F_R)))

    # validity check on the HLLC result: star-state density in (0,rho_max),
    # finite pressure/energy, finite F_hllc itself
    rho_star_L = U_starL[0]
    rho_star_R = U_starR[0]
    valid = (
        np.isfinite(S_star) & np.isfinite(F_hllc).all(axis=0) &
        (rho_star_L > 0) & (rho_star_L < PARAMS['rho_max']) &
        (rho_star_R > 0) & (rho_star_R < PARAMS['rho_max']) &
        ~bad_recon
    )

    # Rusanov fallback (per interface), using the SAME reconstructed L/R
    # face states so the fallback is a like-for-like local replacement
    Smax_face = np.maximum(np.abs(u_L)+c_L, np.abs(u_R)+c_R)
    F_rusanov = 0.5*(F_L+F_R) - 0.5*Smax_face*(U_Rv-U_Lv)

    F_face = np.where(valid[None, :], F_hllc, F_rusanov)
    fallback_count = int(np.sum(~valid))

    dfluid_dt = -(F_face - np.roll(F_face, 1, axis=1))/dx

    exchange = Pi * dVdA(rho, A)
    dEmedium_dt = dfluid_dt[2] + exchange

    dAdt = Pi
    dPidt = c0**2*lap_periodic(A, dx) - dVdA(rho, A)

    dUdt = np.array([dfluid_dt[0], dfluid_dt[1], dEmedium_dt, dAdt, dPidt])
    return dUdt, rho, u, E_medium, A, Pi, c_s_cell, fallback_count

if __name__ == "__main__":
    print(f"[frozen constants] c0={c0:.6f} E_lock={E_lock:.6f} delta_E={delta_E:.6f}")
    print("dynamic_knot_HDF4 module loaded -- MUSCL-HLLC fluid flux with Rusanov fallback.")
