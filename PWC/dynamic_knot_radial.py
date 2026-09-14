"""
PWC Stage 2, spherical-radial model: replaces the 1D Cartesian collision
test (closed out as a negative result for that geometry family --
see knot_audit/cartesian_1D_negative_result.md) with a genuinely
convergent geometry: an inward-moving HDF shell in spherical symmetry,
where wavefront area shrinks as r^2 -> 0, unlike two 1D plane packets.

State per radial cell: U = [rho, rho*u, E_medium, A, Pi]  (same physical
content as the Cartesian model, same declared EOS/V_lock/exchange
structure -- only the geometry changes).

Continuity:  d(rho)/dt   + (1/r^2) d[r^2 rho u]/dr = 0
Momentum:    d(rho u)/dt + (1/r^2) d[r^2(rho u^2+P_eff)]/dr = 2*P_eff/r
Energy:      dE_medium/dt+ (1/r^2) d[r^2 u(E_medium+P_eff)]/dr = +Pi*dVdA(rho,A)
Wave field:  dA/dt = Pi
             dPi/dt = c0^2*(1/r^2) d/dr[r^2 dA/dr] - dVdA(rho,A)

Boundary conditions:
  r=0 (inner ghost cell): mirror -- rho,E_medium,A,Pi even; u odd (u(0,t)=0
      and dA/dr(0,t)=0 enforced by this parity choice).
  r=R_max (outer ghost cell): zero-gradient (outflow) -- lets energy leave
      and be tracked as a measured boundary flux, per the open-box
      accounting rule (E_total(t)+E_boundary_out(t)=E_total(0)).

No artificial viscosity, no clipping, no damping. Step rejection (halve
dt, retry) on any rho crossing rho_max, exactly as in the Cartesian model.
"""
import numpy as np
import dynamic_knot_HDF3 as m3
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
e_EOS_bg = m3.e_EOS_bg
V_lock = m3.V_lock
P_bulk = m3.P_bulk
dPdrho = m3.dPdrho
dVdA = m3.dVdA

def make_grid(Nr, R_max):
    dr = R_max/Nr
    r = (np.arange(Nr)+0.5)*dr
    r_face = np.arange(1, Nr)*dr   # interior faces, index i+1/2 for i=0..Nr-2 (Nr-1 faces)
    return dr, r, r_face

def apply_ghosts(field, parity):
    # parity: +1 even (mirror) at inner boundary, -1 odd (mirror-antisymmetric) at inner boundary
    inner_ghost = parity*field[0]
    outer_ghost = field[-1]   # zero-gradient outflow
    return np.concatenate([[inner_ghost], field, [outer_ghost]])

def primitives(U):
    rho = U[0]; u = U[1]/rho; E_medium = U[2]; A = U[3]; Pi = U[4]
    return rho, u, E_medium, A, Pi

def rhs(U, dr, r, boundary_flux_tracker=None):
    Nr = len(r)
    rho, u, E_medium, A, Pi = primitives(U)
    P = P_bulk(rho, A)
    c_s = np.sqrt(np.maximum(dPdrho(rho, A), 1e-12))

    rho_g = apply_ghosts(rho, +1)
    u_g = apply_ghosts(u, -1)
    P_g = apply_ghosts(P, +1)
    E_g = apply_ghosts(E_medium, +1)
    A_g = apply_ghosts(A, +1)
    c_s_g = apply_ghosts(c_s, +1)

    F0_g = rho_g*u_g
    F1_g = rho_g*u_g**2 + P_g
    F2_g = u_g*(E_g+P_g)
    U0_g = rho_g; U1_g = rho_g*u_g; U2_g = E_g

    Smax_g = np.abs(u_g)+c_s_g
    # faces: Nr+1 faces total (index 0..Nr), face j is between ghost-extended cell j and j+1
    Smax_face = np.maximum(Smax_g[:-1], Smax_g[1:])
    F0_face = 0.5*(F0_g[:-1]+F0_g[1:]) - 0.5*Smax_face*(U0_g[1:]-U0_g[:-1])
    F1_face = 0.5*(F1_g[:-1]+F1_g[1:]) - 0.5*Smax_face*(U1_g[1:]-U1_g[:-1])
    F2_face = 0.5*(F2_g[:-1]+F2_g[1:]) - 0.5*Smax_face*(U2_g[1:]-U2_g[:-1])

    r_face_all = np.concatenate([[0.0], (np.arange(1,Nr))*dr, [Nr*dr]])  # Nr+1 face radii, r=0 .. r=R_max
    r2_face = r_face_all**2

    d0 = -(r2_face[1:]*F0_face[1:] - r2_face[:-1]*F0_face[:-1]) / (r**2 * dr)
    d1 = -(r2_face[1:]*F1_face[1:] - r2_face[:-1]*F1_face[:-1]) / (r**2 * dr) + 2*P/r
    d2 = -(r2_face[1:]*F2_face[1:] - r2_face[:-1]*F2_face[:-1]) / (r**2 * dr)

    exchange = Pi*dVdA(rho, A)
    d2 = d2 + exchange

    # wave field: dPi/dt = c0^2*(1/r^2) d/dr[r^2 dA/dr] - dVdA
    dAdr_face = (A_g[1:]-A_g[:-1])/dr
    G_face = r2_face * dAdr_face
    dPidt = c0**2*(G_face[1:]-G_face[:-1])/(r**2*dr) - dVdA(rho, A)
    dAdt = Pi

    if boundary_flux_tracker is not None:
        # energy flux leaving through the outer face (r=R_max): 4*pi*r^2*F2 there
        boundary_flux_tracker[0] = 4*np.pi*r2_face[-1]*F2_face[-1]

    dUdt = np.array([d0, d1, d2, dAdt, dPidt])
    return dUdt, rho, u, E_medium, A, Pi, c_s

def energy_channels(U, dr, r):
    rho, u, E_medium, A, Pi = primitives(U)
    A_g = apply_ghosts(A, +1)
    dAdr = (A_g[2:]-A_g[:-2])/(2*dr)   # centered, using ghosts at both ends
    vol = 4*np.pi*r**2*dr
    E_kinetic = np.sum(0.5*rho*u**2*vol)
    E_EOS_ = np.sum(e_EOS(rho)*vol)
    E_coupling = np.sum(V_lock(rho,A)*vol)
    E_HDF_kin = np.sum(0.5*Pi**2*vol)
    E_gradient = np.sum(0.5*c0**2*dAdr**2*vol)
    E_medium_evolved = np.sum(E_medium*vol)
    E_medium_diag = np.sum((0.5*rho*u**2+e_EOS(rho)+V_lock(rho,A))*vol)
    return dict(E_kinetic=E_kinetic, E_EOS=E_EOS_, E_coupling=E_coupling,
                E_HDF_kin=E_HDF_kin, E_gradient=E_gradient, E_HDF=E_HDF_kin+E_gradient,
                E_medium=E_medium_evolved, E_medium_diag=E_medium_diag,
                E_total=E_medium_evolved+E_HDF_kin+E_gradient)

def mass_total(U, dr, r):
    rho = U[0]
    return np.sum(rho*4*np.pi*r**2*dr)

def make_state(rho0, u0, A0, Pi0):
    E_medium0 = 0.5*rho0*u0**2+e_EOS(rho0)+V_lock(rho0,A0)
    return np.array([rho0, rho0*u0, E_medium0, A0, Pi0])

def make_inward_shell(Nr, R_max, R0, sigma_r, k_wave, amp, theta=0.0):
    dr, r, r_face = make_grid(Nr, R_max)
    A0 = amp*np.exp(-((r-R0)/sigma_r)**2)*np.cos(k_wave*(r-R0)+theta)
    dAdr = np.gradient(A0, dr)
    Pi0 = c0*dAdr    # INWARD moving: dA/dt=Pi, want packet moving toward r=0 (decreasing r)
    rho0 = np.full(Nr, PARAMS['rho_bg'])
    u0 = np.zeros(Nr)
    return dr, r, rho0, u0, A0, Pi0

if __name__ == "__main__":
    print(f"[frozen constants] c0={c0:.6f} E_lock={E_lock:.6f} delta_E={delta_E:.6f}")
    print("dynamic_knot_radial module loaded -- spherical HDF+medium solver.")
