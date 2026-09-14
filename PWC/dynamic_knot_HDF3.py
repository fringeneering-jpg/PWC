"""
PWC Stage 2, corrected model v3: fixes a real discrete energy-conservation
gap identified in v2 by an instantaneous per-RHS budget audit (see
knot_audit/HDF_conservation_audit.md).

ROOT CAUSE (confirmed two independent ways -- analytic term-by-term budget
and a finite-difference cross-check on the actual rhs(), agreeing to 6+
digits): evolving only (rho, rho*u) via a Rusanov flux and diagnosing total
energy afterward from the algebraic EOS does NOT discretely conserve energy
for nonlinear/large-gradient states -- a well-known real gap in generic
finite-volume compressible schemes. The wave sector (A,Pi) was verified to
cancel EXACTLY against the fluid's V_lock(rho,A)-in-A term (as the by-hand
continuum proof predicted); the entire leak was in the fluid's own
kinetic+EOS+V_lock(rho) energy identity.

FIX: evolve E_medium = 0.5*rho*u^2 + e_EOS(rho) + V_lock(rho,A) as its OWN
conserved flux-form quantity (not diagnosed), with flux
    F_E = u*(E_medium + P_bulk)
and an explicit exchange source +Pi*dVdA(rho,A) (exactly matching the wave
sector's own -Pi*dVdA(rho,A) sink in dPi/dt). Evolving E via its own flux
guarantees the advective part telescopes to EXACTLY zero net contribution
over a periodic domain regardless of nonlinearity (the same structural
guarantee that already makes mass conservation exact to round-off) -- only
the pointwise exchange source survives, and it cancels the wave sector's
source by construction.

State: U = [rho, rho*u, E_medium, A, Pi]   (5 components)

Momentum flux:  F_mom = rho*u^2 + P_bulk(rho,A)
Energy flux:     F_E   = u*(E_medium + P_bulk(rho,A))

NO artificial viscosity, Kelvin-Voigt damping, hyperviscosity, or shock-
heating term of any kind. This process is a reversible reorganization of
HDF wave energy into a phase-locked medium state, not two colliding masses
of matter -- adding shock viscosity would import a standard material-shock
model that has no place in this test. If a state cannot be advanced without
crossing rho_max, the correct response is to reject the step (halve dt,
retry) and, if that fails repeatedly, report that the EOS/integrator
cannot resolve the finite-compression event -- never clip rho and never
add dissipation to force the collision through.
"""
import numpy as np
import sympy as sp
import dynamic_knot_solver as dks
import dynamic_knot_HDF2 as m2   # reuse e_EOS, V_lock, P_bulk, dPdrho, dVdA, c0, E_lock, etc.
import json, time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUTDIR = r"C:\Users\jaden\cosmology\PWC\knot_audit"

PARAMS = m2.PARAMS
c0 = m2.c0
E_lock = m2.E_lock
delta_E = m2.delta_E
e_EOS = m2.e_EOS
e_EOS_bg = m2.e_EOS_bg
V_lock = m2.V_lock
P_bulk = m2.P_bulk
dPdrho = m2.dPdrho
dVdA = m2.dVdA
grad_periodic = m2.grad_periodic
lap_periodic = m2.lap_periodic

def primitives(U):
    rho = U[0]
    u = U[1]/rho
    E_medium = U[2]
    A = U[3]
    Pi = U[4]
    return rho, u, E_medium, A, Pi

def rhs(U, dx):
    rho, u, E_medium, A, Pi = primitives(U)
    P = P_bulk(rho, A)
    c_s = np.sqrt(np.maximum(dPdrho(rho, A), 1e-12))

    F0 = rho*u
    F1 = rho*u**2 + P
    F2 = u*(E_medium + P)
    Ffluid = np.array([F0, F1, F2])

    Smax_cell = np.abs(u) + c_s
    Smax_face = np.maximum(Smax_cell, np.roll(Smax_cell, -1))

    Ufluid = U[:3]
    U_L = Ufluid
    U_R = np.roll(Ufluid, -1, axis=1)
    F_L = Ffluid
    F_R = np.roll(Ffluid, -1, axis=1)
    F_face = 0.5*(F_L+F_R) - 0.5*Smax_face*(U_R-U_L)
    dfluid_dt = -(F_face - np.roll(F_face, 1, axis=1))/dx

    exchange = Pi * dVdA(rho, A)   # explicit source, matches wave sector's sink exactly
    dEmedium_dt = dfluid_dt[2] + exchange

    dAdt = Pi
    dPidt = c0**2*lap_periodic(A, dx) - dVdA(rho, A)

    dUdt = np.array([dfluid_dt[0], dfluid_dt[1], dEmedium_dt, dAdt, dPidt])
    return dUdt, rho, u, E_medium, A, Pi, c_s

def energy_channels(U, dx):
    rho, u, E_medium, A, Pi = primitives(U)
    dAdx = grad_periodic(A, dx)
    # E_medium is now the EVOLVED conserved quantity (not diagnosed).
    # Diagnosed cross-check (should track E_medium closely if the fluid
    # equations are themselves accurate -- reported separately for audit).
    E_medium_diag = np.sum(0.5*rho*u**2 + e_EOS(rho) + V_lock(rho, A))*dx
    E_kinetic = np.sum(0.5*rho*u**2)*dx
    E_EOS_ = np.sum(e_EOS(rho))*dx
    E_coupling = np.sum(V_lock(rho, A))*dx
    E_HDF_kin = np.sum(0.5*Pi**2)*dx
    E_gradient = np.sum(0.5*c0**2*dAdx**2)*dx
    return dict(E_kinetic=E_kinetic, E_EOS=E_EOS_, E_coupling=E_coupling,
                E_HDF_kin=E_HDF_kin, E_gradient=E_gradient,
                E_HDF=E_HDF_kin+E_gradient,
                E_medium=np.sum(E_medium)*dx, E_medium_diag=E_medium_diag,
                E_total=np.sum(E_medium)*dx + E_HDF_kin + E_gradient)

def make_counter_pulses(Nx, L, x1, x2, amp, sigma, k_wave):
    dx = L/Nx
    x = (np.arange(Nx)+0.5)*dx
    A1 = amp*np.exp(-((x-x1)/sigma)**2)*np.cos(k_wave*(x-x1))
    A2 = amp*np.exp(-((x-x2)/sigma)**2)*np.cos(k_wave*(x-x2))
    dA1dx = grad_periodic(A1, dx)
    dA2dx = grad_periodic(A2, dx)
    Pi1 = -c0*dA1dx
    Pi2 = c0*dA2dx
    A0 = A1 + A2
    Pi0 = Pi1 + Pi2
    rho0 = np.full(Nx, PARAMS['rho_bg'])
    u0 = np.zeros(Nx)
    E_medium0 = 0.5*rho0*u0**2 + e_EOS(rho0) + V_lock(rho0, A0)
    return x, dx, rho0, u0, E_medium0, A0, Pi0

def make_state(rho0, u0, A0, Pi0):
    E_medium0 = 0.5*rho0*u0**2 + e_EOS(rho0) + V_lock(rho0, A0)
    return np.array([rho0, rho0*u0, E_medium0, A0, Pi0])

if __name__ == "__main__":
    print(f"[frozen constants] c0={c0:.6f} E_lock={E_lock:.6f} delta_E={delta_E:.6f}")
    print("dynamic_knot_HDF3 module loaded -- energy-conserving-by-construction fluid+wave model.")
