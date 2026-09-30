"""
audit_independence.py

Independence audit of the 2026-09-30 closures (T1 a_hold, T2 rho_0, T7 H_0,
product invariant, proton identities, heat-spacer scan).

For each claimed match it asks one question: is the "observed" number
independent of the inputs that produced the "predicted" number, and would
the check have failed if the physics were wrong?

Stdlib + the heat-spacer module only. Deterministic. No data files.
Run from anywhere:   python PWC/audit_independence.py
Writes:              PWC/knot_audit/independence_audit.md
"""
import io
import math
import sys
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

G = 6.6743e-11
C0 = 2.998e8
MPC_KM = 3.0856775814913673e19
MPC_M = MPC_KM * 1e3
HBAR = 1.054572e-34
RHO0 = 8.74e-27          # kg/m^3, as used in t7_discrete_unlocking.md
RHO_MAX = 1.304e15       # kg/m^3, GW150914 calibration
RP_TXT = 8.4e-16         # m, value used in the T7 arithmetic
MP = 1.6726e-27          # kg, value used in proton_derivation_20260930.md
RP_OBS = 0.8414e-15      # m, value used in proton_derivation_20260930.md


def rho_crit(h0_kms_mpc):
    h = h0_kms_mpc * 1e3 / MPC_M
    return 3.0 * h * h / (8.0 * math.pi * G)


def solve_h0_for(rho_target, factor):
    lo, hi = 50.0, 90.0
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if factor * rho_crit(mid) < rho_target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def a_hold(rho, omega_eff, c0=C0):
    return (c0 / math.sqrt(3.0)) * math.sqrt(omega_eff * G * rho)


def h_wall(rho0, c0=C0, rho_max=RHO_MAX, rp=RP_TXT):
    gamma = rho0 * c0 / (rho_max * rp)
    return gamma, gamma * MPC_KM


def section_rho0():
    print("## 1. Where rho_0 comes from (T2)")
    print()
    h_impl = solve_h0_for(RHO0, 0.95)
    print(f"rho_0 = {RHO0:.2e} kg/m^3 equals 0.95 * rho_crit at H0 = {h_impl:.3f} km/s/Mpc.")
    print(f"  0.95 * rho_crit(70.0) = {0.95 * rho_crit(70.0):.4e}")
    print("So rho_0 is not independent of the Hubble constant: a measured H0 = 70 is")
    print("already inside it (paper/PWC_v1_draft.md: 'rho_0 ~ 0.95 rho_crit').")
    print("T2 is therefore an INPUT (DERIVATION_BRIEF: 'Option C accepted'), not a derivation.")
    print()


def section_h0():
    print("## 2. H0_wall (T7) is not independent of the H0 inside rho_0")
    print()
    gamma, h_out = h_wall(RHO0)
    print(f"Gamma_untie = rho0*c0/(rho_max*R_p) = {gamma:.3e} 1/s  ->  {h_out:.2f} km/s/Mpc")
    print("Because rho_0 = 0.95*rho_crit(H_in) and Gamma is linear in rho_0, H_out ~ H_in^2.")
    print()
    print("| H0 baked into rho_0 | H0_wall out | out/in |")
    print("|---:|---:|---:|")
    for h_in in (67.4, 70.0, 73.04):
        _, h_o = h_wall(0.95 * rho_crit(h_in))
        print(f"| {h_in:.2f} | {h_o:.2f} | {h_o / h_in:.3f} |")
    print()
    print("The output tracks whichever H0 was fed in: a Planck-valued input gives 68.5 (a 'match'")
    print("to Planck within 2%), a SH0ES-valued input gives 80.4. The input actually used, 70,")
    print("sits between them, so 73.8 landing within 1% of SH0ES does not discriminate anything.")
    print()


def section_omega():
    print("## 3. The geometric factor in a_hold was chosen after seeing the target")
    print()
    a0_fit = 6.68e-11
    print("a_hold = (c0/sqrt(3)) * sqrt(Omega_eff * G * rho_0)")
    print()
    print("| Omega_eff | a_hold (m/s^2) | / a0(6.68e-11) |")
    print("|---|---:|---:|")
    for label, om in (("1/pi   (first closure)", 1 / math.pi),
                      ("1/4    (adopted 'tightening')", 0.25),
                      ("4pi/49 (N=49 needed to hit a0)", 4 * math.pi / 49)):
        a = a_hold(RHO0, om)
        print(f"| {label} | {a:.3e} | {a / a0_fit:.3f} |")
    om_req = (a0_fit / (C0 / math.sqrt(3))) ** 2 / (G * RHO0)
    print()
    print(f"Omega_eff required to hit a0 exactly: {om_req:.4f}  (1/4 is {abs(0.25 / om_req - 1) * 100:.1f}% away).")
    print("Per the PR #2 description, 1/pi was replaced by 1/4 after it overshot a0 by 12%; the")
    print("replacement came with a textbook rationale, but it was chosen with the target in view")
    print("and the ~7x prefactor gap already known (eos_latent_heat.md s4-5). That is selection")
    print("among O(1) factors, not a forecast, and a 1% match after selection is not a 1% test.")
    print()


def section_product():
    print("## 4. The 'product invariant' and its stated precision")
    print()
    a_fw = a_hold(RHO0, 0.25)
    _, h_fw = h_wall(RHO0)
    print(f"Unrounded framework product: {a_fw:.4e} * {h_fw:.3f} = {a_fw * h_fw:.4e}")
    print(f"Rounded inputs as printed in the docs: 6.61e-11 * 73.8 = {6.61e-11 * 73.8:.4e}")
    print("Repo states 4.876e-9 (README, t7 doc) and 4.878e-9 (paper, proton doc), and the")
    print("match as 0.06% and 0.02%. The two 'precisions' differ by rounding of the same numbers.")
    print()
    print("| 'observed' pairing | product | framework / observed |")
    print("|---|---:|---:|")
    for label, a0, h0 in (("a0=6.68e-11 (this repo's sqrt law), SH0ES 73.04", 6.68e-11, 73.04),
                          ("a0=6.68e-11, Planck 67.4", 6.68e-11, 67.4),
                          ("a0=1.2e-10 (McGaugh+2016 RAR form), SH0ES 73.04", 1.2e-10, 73.04),
                          ("a0=1.2e-10 (McGaugh+2016 RAR form), Planck 67.4", 1.2e-10, 67.4)):
        p = a0 * h0
        print(f"| {label} | {p:.3e} | {a_fw * h_fw / p:.3f} |")
    print()
    print("The 0.06% figure holds for exactly one pairing. The observed H0 alone has a")
    print("~8% spread between SH0ES and Planck, and a0 is a fitted, functional-form-dependent")
    print("number, so 0.06% is not a measure of accuracy. Supportable claim: agreement at the")
    print("~10% level, with rho_0 (which embeds H0 = 70) and two chosen factors as inputs.")
    print()


def section_proton():
    print("## 5. Proton identities")
    print()
    ident_a = MP * RP_OBS * C0 / HBAR
    print(f"Identity A: m_p * R_p * c0 / hbar = {ident_a:.4f}   (claimed 4)")
    rp = (3 * HBAR / (512 * math.pi * RHO_MAX * C0)) ** 0.25
    mp = ((131072 * math.pi / 3) * RHO_MAX * HBAR ** 3 / C0 ** 3) ** 0.25
    print(f"Combined:   R_p = {rp * 1e15:.4f} fm, m_p = {mp * 1e27:.4f}e-27 kg")
    rho_implied = 3 * MP / (2048 * math.pi * RP_OBS ** 3)
    print(f"rho_max implied by CODATA m_p and R_p through Identity B: {rho_implied:.4e} kg/m^3")
    print(f"  vs GW150914 calibration {RHO_MAX:.3e}  (ratio {rho_implied / RHO_MAX:.4f})")
    print(f"Equivalent: (mean proton density / rho_max)^(1/3) = "
          f"{((MP / (4 / 3 * math.pi * RP_OBS ** 3)) / RHO_MAX) ** (1 / 3):.4f}   (claimed 8)")
    print()
    print("This is the strongest item in the batch: rho_max comes from GW150914 and the target is")
    print("proton data, so the inputs really are independent, and two dimensionless combinations")
    print("land within ~0.1% of the integers 4 and 8. Worth keeping and pursuing.")
    print("Limits: (i) the integers were attached by a topological story written after the numbers")
    print("were known, and the repo's own text says R_p spans 0.84-0.88 fm across methods (at")
    print(f"0.88 fm Identity A reads {MP * 0.88e-15 * C0 / HBAR:.3f}); (ii) which combinations to test was")
    print("also chosen after the fact (look-elsewhere); (iii) the same mechanism applied to the")
    print("neutron misses by ~2.5% (proton_derivation_20260930.md), over 20x worse than the proton")
    print("match, and is explained by 'isospin' only afterwards. Status: coincidence with a")
    print("proposed mechanism, not a derivation, until 4 and 8 are forced independently and a")
    print("second particle is predicted before its number is looked up.")
    print()


def section_heat():
    print("## 6. Heat-spacer scan: can it fail?")
    print()
    import numpy as np
    import heat_spacer_free_energy as hs

    def mixed(family, d0, args, dt=1e-4):
        A, B, K, dref, coeff = args
        f = hs.FAMILIES[family]["energy"]
        h = 1e-5

        def dfd(T):
            return (f(d0 + h, A, B, K, dref, coeff, T) - f(d0 - h, A, B, K, dref, coeff, T)) / (2 * h)
        return (dfd(dt) - dfd(-dt)) / (2 * dt)

    results = hs.run_scan()
    agree = 0
    for row in results:
        args = (row["A"], row["B"], row["K"], row["d_ref"], row["thermal_coeff"])
        mixed_d = mixed(row["family"], row["d0_Tmin"], args)
        predicted = "positive" if -mixed_d > 0 else "negative"
        if predicted == row["observed_sign"] and row["all_stable"]:
            agree += 1
    print(f"Sign predicted from the input alone (-d2f/dd dT at d0, given f''>0) matches the")
    print(f"scan outcome in {agree}/{len(results)} rows, with no minimization needed to state it.")
    print("Implicit-function theorem: dd0/dT = -(d2f/dd dT) / f''(d0). Families A-D were written")
    print("with a negative mixed derivative and E with a positive one, so once f'' > 0 the sign")
    print("is fixed. The scan verifies the optimiser and the bookkeeping; it cannot fail on the")
    print("physics, and 432/432 + 108/108 is not evidence about PWC. A test that can fail needs a")
    print("thermal term whose d-dependence is derived from the medium, not chosen to point outward.")
    print()


def section_t2_notebook():
    print("## 7. T2 fixed-point cell (values printed by the Colab run; the cell is not in the repo)")
    print()
    prefactor, required, b, target = 2.1745131423320837e-27, 0.2488001307016114, 2.7324456318055946e+08, 8.74e-27
    print(f"prefactor / required = {prefactor / required:.6e}  vs target {target:.2e}  "
          f"(rel. diff {abs(prefactor / required / target - 1):.1e})")
    print("'required eta*(Delta_M/c0)' is the number that makes the fixed point equal the target,")
    print("so 'reproduced exactly' and 'residual 0.000' are identities, not confirmations.")
    below, above = 2.3642759073761120e-20, -2.4120390570200742e-20
    mean_resp = 0.5 * (below - above)
    print(f"Printed responses at +-1% of rho*: mean magnitude {mean_resp:.5e}; B*0.01*rho* = {b * 0.01 * target:.5e}.")
    print("The response and the linearised derivative are one calculation seen twice. Any")
    print("d(rho)/dt = source - sink(rho) with an increasing sink has a stable fixed point, so")
    print("'pushes toward the fixed point' holds for any B > 0 and cannot fail. The ODE itself is")
    print("not in the repo, so nothing beyond these relations can be audited here.")
    print("The real content is one number: eta*(Delta_M/c0) = 0.2488 must be <= 1 (v/c0 >= 0.2488).")
    print("That is a constraint on unknown microphysics, not a confirmation of it.")
    print()


def main():
    print("# Independence audit of the 2026-09-30 closures")
    print()
    print("Generated by `PWC/audit_independence.py`. Each section states what the check")
    print("does and does not establish.")
    print()
    for fn in (section_rho0, section_h0, section_omega, section_product,
               section_proton, section_heat, section_t2_notebook):
        fn()


if __name__ == "__main__":
    buf = io.StringIO()
    with redirect_stdout(buf):
        main()
    text = buf.getvalue()
    print(text)
    out = Path(__file__).resolve().parent / "knot_audit" / "independence_audit.md"
    out.write_text(text, encoding="utf-8")
    print(f"[written] {out}")
