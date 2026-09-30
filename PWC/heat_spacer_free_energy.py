import csv
import itertools
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar

T_VALUES = np.linspace(0.0, 4.0, 9)
D_LO = 0.35
D_HI = 8.0
BOUNDARY_MARGIN = 0.02
SLOPE_TOL = 1e-7

A_VALUES = [0.5, 1.0, 2.0]
B_VALUES = [2.0, 4.0, 8.0]
K_VALUES = [2.0, 8.0]
DREF_VALUES = [1.0, 1.4]
THERMAL_VALUES = [0.1, 0.35, 0.75]


def common_energy(d, A, B, K, d_ref):
    return A / d**12 - B / d**6 + 0.5 * K * (d - d_ref) ** 2


def common_curvature(d, A, B, K):
    return 156.0 * A / d**14 - 42.0 * B / d**8 + K


def f_a(d, A, B, K, d_ref, coefficient, temperature):
    return common_energy(d, A, B, K, d_ref) - coefficient * temperature * d


def c_a(d, A, B, K, d_ref, coefficient, temperature):
    return common_curvature(d, A, B, K)


def f_b(d, A, B, K, d_ref, coefficient, temperature):
    return A / d**12 - B / d**6 + 0.5 * K * (d - (d_ref + coefficient * temperature)) ** 2


def c_b(d, A, B, K, d_ref, coefficient, temperature):
    return common_curvature(d, A, B, K)


def f_c(d, A, B, K, d_ref, coefficient, temperature):
    return common_energy(d, A, B, K, d_ref) - coefficient * temperature * d / (d + 1.0)


def c_c(d, A, B, K, d_ref, coefficient, temperature):
    return common_curvature(d, A, B, K) + 2.0 * coefficient * temperature / (d + 1.0) ** 3


def f_d(d, A, B, K, d_ref, coefficient, temperature):
    return common_energy(d, A, B, K, d_ref) - coefficient * temperature * np.log(d)


def c_d(d, A, B, K, d_ref, coefficient, temperature):
    return common_curvature(d, A, B, K) + coefficient * temperature / d**2


def f_e(d, A, B, K, d_ref, coefficient, temperature):
    return common_energy(d, A, B, K, d_ref) + coefficient * temperature * d


def c_e(d, A, B, K, d_ref, coefficient, temperature):
    return common_curvature(d, A, B, K)


FAMILIES = {
    "A": {"energy": f_a, "curvature": c_a, "expected_sign": "positive"},
    "B": {"energy": f_b, "curvature": c_b, "expected_sign": "positive"},
    "C": {"energy": f_c, "curvature": c_c, "expected_sign": "positive"},
    "D": {"energy": f_d, "curvature": c_d, "expected_sign": "positive"},
    "E_control": {"energy": f_e, "curvature": c_e, "expected_sign": "negative"},
}


def observed_sign(slope):
    if slope > SLOPE_TOL:
        return "positive"
    if slope < -SLOPE_TOL:
        return "negative"
    return "near_zero"


def run_scan():
    results = []
    parameter_grid = itertools.product(
        A_VALUES, B_VALUES, K_VALUES, DREF_VALUES, THERMAL_VALUES
    )
    parameter_grid = list(parameter_grid)

    for family_name, family in FAMILIES.items():
        for A, B, K, d_ref, coefficient in parameter_grid:
            d0_values = []
            energy_values = []
            curvature_values = []
            boundary_hit = False
            all_stable = True

            for temperature in T_VALUES:
                minimization = minimize_scalar(
                    family["energy"],
                    bounds=(D_LO, D_HI),
                    args=(A, B, K, d_ref, coefficient, temperature),
                    method="bounded",
                )
                d0 = minimization.x
                curvature = family["curvature"](
                    d0, A, B, K, d_ref, coefficient, temperature
                )

                d0_values.append(d0)
                energy_values.append(minimization.fun)
                curvature_values.append(curvature)

                if d0 <= D_LO + BOUNDARY_MARGIN or d0 >= D_HI - BOUNDARY_MARGIN:
                    boundary_hit = True
                if curvature <= 0.0:
                    all_stable = False

            slope, intercept = np.polyfit(T_VALUES, d0_values, 1)
            sign = observed_sign(slope)
            expected_sign = family["expected_sign"]
            sign_test_pass = sign == expected_sign
            all_pass = (not boundary_hit) and all_stable and sign_test_pass

            results.append(
                {
                    "family": family_name,
                    "expected_sign": expected_sign,
                    "A": A,
                    "B": B,
                    "K": K,
                    "d_ref": d_ref,
                    "thermal_coeff": coefficient,
                    "T_min": T_VALUES[0],
                    "T_max": T_VALUES[-1],
                    "d0_Tmin": d0_values[0],
                    "d0_Tmax": d0_values[-1],
                    "energy_Tmin": energy_values[0],
                    "energy_Tmax": energy_values[-1],
                    "slope": slope,
                    "intercept": intercept,
                    "min_curvature": min(curvature_values),
                    "boundary_hit": boundary_hit,
                    "all_stable": all_stable,
                    "observed_sign": sign,
                    "sign_test_pass": sign_test_pass,
                    "all_pass": all_pass,
                }
            )

    return results


def build_summary(results):
    summary = {}
    for family_name in FAMILIES:
        rows = [row for row in results if row["family"] == family_name]
        stable_rows = [
            row for row in rows if not row["boundary_hit"] and row["all_stable"]
        ]
        passing_rows = [row for row in stable_rows if row["sign_test_pass"]]
        slopes = [row["slope"] for row in stable_rows]
        summary[family_name] = {
            "total": len(rows),
            "stable": len(stable_rows),
            "expected_sign_pass": len(passing_rows),
            "expected_sign_fail": len(stable_rows) - len(passing_rows),
            "rejected": len(rows) - len(stable_rows),
            "min_slope": min(slopes) if slopes else None,
            "max_slope": max(slopes) if slopes else None,
        }
    return summary


def write_csv(path, results):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)


def write_report(path, summary):
    lines = [
        "# Heat-Spacer Free-Energy Scan Results",
        "",
        "This report is generated by `PWC/heat_spacer_free_energy.py`.",
        "",
        "## Environment",
        "",
        f"- Python: {sys.version.split()[0]}",
        f"- NumPy: {np.__version__}",
        "",
        "## Per-family results",
        "",
        "| Family | Expected sign | Total | Stable interior | Sign pass | Sign fail | Rejected | Minimum slope | Maximum slope |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for family_name, values in summary.items():
        expected = FAMILIES[family_name]["expected_sign"]
        minimum = "n/a" if values["min_slope"] is None else f"{values['min_slope']:.6e}"
        maximum = "n/a" if values["max_slope"] is None else f"{values['max_slope']:.6e}"
        lines.append(
            f"| {family_name} | {expected} | {values['total']} | {values['stable']} | "
            f"{values['expected_sign_pass']} | {values['expected_sign_fail']} | "
            f"{values['rejected']} | {minimum} | {maximum} |"
        )

    lines.extend(
        [
            "",
            "## Caveat",
            "",
            "This scan tests consequences of assumed finite trial potentials. It does not derive a microscopic PWC interaction, fix physical coefficients, or constitute experimental confirmation.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    results = run_scan()
    output_dir = Path(__file__).resolve().parent / "knot_audit"
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "heat_spacer_scan.csv"
    report_path = output_dir / "heat_spacer_results.md"
    write_csv(csv_path, results)

    summary = build_summary(results)
    write_report(report_path, summary)

    print("Heat-Spacer Free-Energy Scan")
    for family_name, values in summary.items():
        print(
            f"{family_name}: total={values['total']}, stable={values['stable']}, "
            f"sign_pass={values['expected_sign_pass']}, sign_fail={values['expected_sign_fail']}, "
            f"rejected={values['rejected']}, min_slope={values['min_slope']}, "
            f"max_slope={values['max_slope']}"
        )
    print(f"CSV: {csv_path.relative_to(output_dir.parent.parent)}")
    print(f"Report: {report_path.relative_to(output_dir.parent.parent)}")


if __name__ == "__main__":
    main()
