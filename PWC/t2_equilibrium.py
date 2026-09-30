"""
t2_equilibrium.py

T2 equilibrium closure for the resting density rho_0, as supplied 2026-09-30
(session derivation; not previously in the repo), reconstructed so the cell
output can be reproduced and audited.

Balance of matter creation (mass sweeping the untied medium) against matter
decay (topological unspooling), per unit matter density rho_b:

    decay  :  Gamma * rho_b,          Gamma = rho_0 * c0 / (rho_max * R_p)
    create :  eta * rho_0 * (pi * G / a0) * <v> * rho_b     (swept volume pi*R_hold^2*v,
                                                              R_hold^2 = G*M/a0, M cancels)

rho_0 cancels from BOTH sides. It is fixed only after G is replaced by the
Friedmann expression G = 3*Gamma^2 / (8*pi*rho_0), which gives

    rho_0 = 8 * a0 * rho_max * R_p / (3 * eta * c0 * <v>)

Stdlib only. Run:  python PWC/t2_equilibrium.py
"""
import math

C0 = 2.998e8
A0 = 6.68e-11            # fitted on SPARC (galaxy rotation)
RHO_MAX = 1.304e15       # GW150914
RP = 0.8414e-15
RHO0_TARGET = 8.74e-27
G_MEAS = 6.6743e-11


def prefactor():
    """rho_0 * (eta * <v>/c0)"""
    return 8.0 * A0 * RHO_MAX * RP / (3.0 * C0 ** 2)


def untying_coefficient():
    """B = c0 / (rho_max * R_p), the specific rate Gamma / rho_0."""
    return C0 / (RHO_MAX * RP)


def rho0_closed_form(eta, v_over_c0):
    return prefactor() / (eta * v_over_c0)


def g_emergent(rho0):
    """G from Friedmann with H := Gamma_untie(rho_0)."""
    gamma = rho0 * untying_coefficient()
    return 3.0 * gamma ** 2 / (8.0 * math.pi * rho0)


def logistic(rho, rho_star, b):
    """The relaxation form that reproduces the printed cell output."""
    return b * rho * (1.0 - rho / rho_star)


def main():
    pre, b = prefactor(), untying_coefficient()
    required = pre / RHO0_TARGET
    print(f"Fixed-point prefactor = {pre!r} kg m^-3")
    print(f"Required eta*(<v>_M/c0) = {required!r}")
    print(f"Untying coefficient B = {b!r}")
    print()
    print(f"rho_star = {pre / required!r} kg m^-3")
    print(f"target rho0 = {RHO0_TARGET!r} kg m^-3")
    print(f"relative residual = {abs(pre / required - RHO0_TARGET) / RHO0_TARGET:.3e}")
    print(f"d rho/dt below equilibrium = {logistic(0.99 * RHO0_TARGET, RHO0_TARGET, b)!r}")
    print(f"d rho/dt above equilibrium = {logistic(1.01 * RHO0_TARGET, RHO0_TARGET, b)!r}")
    print(f"linearized derivative at equilibrium = {-b!r}")


if __name__ == "__main__":
    main()
