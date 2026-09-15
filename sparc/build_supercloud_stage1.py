"""
Supercloud Stage 1 builder (2026-09-15).

Pure data-transcription and audit stage for a future HDF/LDF-constrained
Galactic morphology test. NOT a model fit, NOT a PWC validation. Every
number below is transcribed exactly from the cited table/page of a real,
verified source PDF (already fetched and read directly this session, not
taken on any other AI's word). Blocked quantities (volume density, cross-
section, external pressure) are explicitly null -- not approximated, not
digitized from a figure, not invented.

Sources (all fetched and read directly this session):
  [K26]  Kormann et al. 2026, A&A, "The superclouds of the local Milky Way"
         arXiv:2507.14883v3 -- Table C.2 (mass, length), Table C.3 (undulation fit)
  [B26]  Bobylev & Bajkova 2026, arXiv:2608.10884v2 -- Vela Ridge cross-check (not
         used for Stage 1 numbers directly; independent amplitude/wavelength
         already compared against video transcript in this session)
  [KF26] Kormann et al. 2026 (fragmentation follow-up), arXiv:2608.21028 --
         Table E.1 (characteristic superclump spacing, core/full range)

No per-cloud mass/length uncertainty is reported in [K26] Table C.2 (point
estimates from the HOP+PCA pipeline only) -- this is stated explicitly
below, not silently omitted.
"""
import csv, json

# ============================================================
# RAW, EXACTLY-TRANSCRIBED SOURCE VALUES -- do not modify without
# re-checking against the actual PDF text.
# ============================================================

# [K26] Table C.2 (p.11-12 of arXiv:2507.14883v3): Mass [Msun], Length [pc]
# No per-cloud uncertainty reported by the authors.
table_C2 = {
    "Radcliffe Wave":              dict(mass_Msun=3.58e6, length_pc=2468.67),
    "Split":                       dict(mass_Msun=1.85e6, length_pc=1399.60),
    "Natrix Cloud":                dict(mass_Msun=1.12e6, length_pc=1970.08),
    "Malpolon Cloud":              dict(mass_Msun=1.99e6, length_pc=1946.38),
    "Vela Ridge Cloud":            dict(mass_Msun=1.50e6, length_pc=2215.88),
    "Sagittarius Spur Extension":  dict(mass_Msun=2.39e6, length_pc=1487.87),
    "Anguis Cloud":                dict(mass_Msun=7.76e5, length_pc=981.80),
}

# [K26] Table C.3 (p.12): Amplitude a [pc], Wavelength lambda [pc], Phase phi [rad],
# Offset d [pc], damping eps_a [pc^-1], damping eps_omega [pc^-1].
# Vela Ridge Cloud fit with a SIMPLE (non-damped) sinusoid -- no damping params.
table_C3 = {
    "Malpolon Cloud":   dict(amplitude_pc=31.97,  wavelength_pc=1137.40, phase_rad=-3.10, offset_pc=58.15,  damp_eps_a=-1.18e-3, damp_eps_omega=-7.52e-5, fit_type="damped_sinusoid"),
    "Natrix Cloud":     dict(amplitude_pc=70.53,  wavelength_pc=1749.47, phase_rad=-0.58, offset_pc=-1.17,  damp_eps_a=1.59e-3,  damp_eps_omega=-1.12e-3, fit_type="damped_sinusoid"),
    "Radcliffe Wave":   dict(amplitude_pc=-87.95, wavelength_pc=1748.00, phase_rad=-3.09, offset_pc=-13.01, damp_eps_a=-1.10e-3, damp_eps_omega=2.88e-4, fit_type="damped_sinusoid"),
    "Vela Ridge Cloud": dict(amplitude_pc=56.90,  wavelength_pc=3078.95, phase_rad=0.41,  offset_pc=59.14,  damp_eps_a=None,     damp_eps_omega=None,    fit_type="simple_sinusoid"),
}

# [KF26] Table E.1 (p.8 of arXiv:2608.21028): characteristic superclump spacing,
# 800 pc cutoff applied. Core = 25th-75th percentile range, Full = min-max range.
# For Natrix Cloud the authors explicitly recommend the L1335-inclusive range
# as representative -- that is the value used here, per their own stated choice,
# not a selection made by this analysis.
table_E1 = {
    "Split":                       dict(core_lo_pc=160, core_hi_pc=190, full_lo_pc=148, full_hi_pc=192),
    "Radcliffe Wave":              dict(core_lo_pc=251, core_hi_pc=292, full_lo_pc=219, full_hi_pc=390),
    "Sagittarius Spur Extension":  dict(core_lo_pc=323, core_hi_pc=377, full_lo_pc=222, full_hi_pc=379),
    "Vela Ridge Cloud":            dict(core_lo_pc=248, core_hi_pc=248, full_lo_pc=244, full_hi_pc=254),
    "Malpolon Cloud":              dict(core_lo_pc=202, core_hi_pc=215, full_lo_pc=193, full_hi_pc=221),
    "Natrix Cloud":                dict(core_lo_pc=357, core_hi_pc=366, full_lo_pc=356, full_hi_pc=374),  # L1335-inclusive, authors' adopted value
    # Anguis Cloud explicitly excluded by [KF26]: only one superclump recovered, spacing not measurable.
}

ALL_CLOUDS = list(table_C2.keys())

def main():
    # ============================================================
    # supercloud_stage1_raw.csv
    # ============================================================
    with open("supercloud_stage1_raw.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["supercloud","mass_Msun","mass_uncertainty","length_pc","length_uncertainty",
                    "amplitude_pc","wavelength_pc","phase_rad","offset_pc","damp_eps_a_per_pc","damp_eps_omega_per_pc","fit_type",
                    "frag_core_lo_pc","frag_core_hi_pc","frag_full_lo_pc","frag_full_hi_pc",
                    "volume_density_status","cross_section_status","external_pressure_status",
                    "source_mass_length","source_undulation","source_fragmentation"])
        for c in ALL_CLOUDS:
            m = table_C2[c]
            u = table_C3.get(c, {})
            fr = table_E1.get(c, {})
            w.writerow([
                c, m["mass_Msun"], "not_reported", m["length_pc"], "not_reported",
                u.get("amplitude_pc",""), u.get("wavelength_pc",""), u.get("phase_rad",""), u.get("offset_pc",""),
                u.get("damp_eps_a",""), u.get("damp_eps_omega",""), u.get("fit_type","no_fit_reported"),
                fr.get("core_lo_pc",""), fr.get("core_hi_pc",""), fr.get("full_lo_pc",""), fr.get("full_hi_pc",""),
                "Not tabulated; displayed graphically in Fig. 6 of K26 only",
                "Not inferred; K26 authors state width/height estimates are unreliable",
                "Not supplied per cloud",
                "K26 Table C.2, p.11-12 (arXiv:2507.14883v3)",
                "K26 Table C.3, p.12 (arXiv:2507.14883v3)" if c in table_C3 else "no undulation fit reported for this cloud",
                "KF26 Table E.1, p.8 (arXiv:2608.21028)" if c in table_E1 else "excluded by KF26 -- only 1 superclump recovered, spacing not measurable",
            ])
    print("wrote supercloud_stage1_raw.csv")

    # ============================================================
    # supercloud_stage1_derived.csv -- transparent arithmetic only
    # ============================================================
    with open("supercloud_stage1_derived.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["supercloud","linear_mass_Msun_per_pc","amplitude_over_wavelength",
                    "frag_full_midpoint_pc","frag_over_wavelength"])
        derived_rows = []
        for c in ALL_CLOUDS:
            m = table_C2[c]
            mu = m["mass_Msun"] / m["length_pc"]
            u = table_C3.get(c)
            a_over_lambda = (abs(u["amplitude_pc"]) / u["wavelength_pc"]) if u else None
            fr = table_E1.get(c)
            frag_mid = ((fr["full_lo_pc"] + fr["full_hi_pc"]) / 2) if fr else None
            frag_over_lambda = (frag_mid / u["wavelength_pc"]) if (fr and u) else None
            row = [c, round(mu,2),
                   round(a_over_lambda,4) if a_over_lambda is not None else "",
                   round(frag_mid,1) if frag_mid is not None else "",
                   round(frag_over_lambda,4) if frag_over_lambda is not None else ""]
            w.writerow(row)
            derived_rows.append(dict(cloud=c, mu=mu, a_over_lambda=a_over_lambda,
                                      frag_mid=frag_mid, frag_over_lambda=frag_over_lambda))
    print("wrote supercloud_stage1_derived.csv")

    # print descriptive comparison, n=4 (or fewer) where undulation fit exists -- NO significance claims
    print("\n=== Descriptive comparison (n=4 wave-fit clouds; NOT a significance test) ===")
    fit_clouds = [r for r in derived_rows if r["a_over_lambda"] is not None]
    fit_clouds_sorted_by_mu = sorted(fit_clouds, key=lambda r: r["mu"])
    print("Rank by linear mass (mu, Msun/pc), with A/lambda and frag/lambda alongside:")
    for r in fit_clouds_sorted_by_mu:
        fol = f"{r['frag_over_lambda']:.4f}" if r["frag_over_lambda"] is not None else "n/a"
        print(f"  {r['cloud']:28s} mu={r['mu']:7.1f}  A/lambda={r['a_over_lambda']:.4f}  frag/lambda={fol}")

    return derived_rows

if __name__ == "__main__":
    main()
