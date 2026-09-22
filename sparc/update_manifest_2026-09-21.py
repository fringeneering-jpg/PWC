"""
One-time script: folds the 2026-09-21 external-document extraction (5 parallel
reads of 8 source files -- two large PDFs, the full CONVERSATION_TRANSCRIPT,
three AI-chat PDFs, a docx, and a duplicate-check file) into
provenance_manifest.json, in the manifest's own existing format and
status-class vocabulary. Every item below was actually read and extracted,
not summarized from memory. Contradictions found in the source material are
recorded as contradictions, not silently resolved.
"""
import json

D = r"C:\Users\jaden\cosmology\sparc"
m = json.load(open(f"{D}/provenance_manifest.json", encoding="utf-8"))

# --- 1. New excluded_substitutions (falsified/rejected claims found in the source docs) ---
m["excluded_substitutions"].extend([
    {
        "statement": "A universal HDF/medium equation of state K(rho) exists, independent of each galaxy's own rotation curve.",
        "status": "Rejected: Domain EE, gauge-free EOS test (c_s^2=-g*r/(d ln rho/d ln r), zero fitted params), 124 galaxies/1776 points. K scatters 0.663 dex (factor 5) at fixed rho; log(c_s) correlates +0.921 with each galaxy's own V_flat; c_s/V_flat=0.627 (isothermal analytic value 0.707). Medium stiffness is a readout of the galaxy's own rotation, not a substrate property -- structurally a halo fit in fluid vocabulary."
    },
    {
        "statement": "Forcing the medium into rigid co-rotation with the disk (Domain FF) breaks the Domain EE universal-EOS lock.",
        "status": "Rejected: the V_flat correlation tightens (+0.921 to +0.989) and variance is conserved (478x to 382x), not broken. Required cosmological spin parameter lambda'=0.3945 median vs Bullock et al. 2001's cosmological median 0.035 -- 11.3x too high, 4.8-sigma, 0.0% of 124 galaxies within 2-sigma."
    },
    {
        "statement": "The Domain EE/FF EOS lock is an oblateness/geometric-binning artifact, not a real degeneracy.",
        "status": "Rejected: Domain GG. Scatter survives at 0.570 dex (factor 3.7) even restricted to near-spherical regime (f_bar<0.30 AND r>3*R_disk); trend across f_bar quartiles is non-monotonic (0.497/0.649/0.614/0.506), not the signature of a geometric artifact."
    },
    {
        "statement": "The galaxy-as-cavitation-void-in-an-electromagnetic-sea picture (medium literally identified with the EM field) is a viable substrate for HDF.",
        "status": "Rejected on four independent, quantified grounds (Domain HH + EM-medium critique in CONVERSATION_TRANSCRIPT): (1) a traceless EM stress tensor forces c_s=c/sqrt(3)=173,085 km/s, 1,700x-22,000x too stiff for real galaxies; (2) the resulting Jeans length (38.5-12,688 Mpc) is 2,000x-600,000x larger than a 20 kpc galaxy (Meszaros effect: radiation free-streams, doesn't clump); (3) required surface tension is 2.6 million times water's H-bond-derived value, and vacuum Maxwell theory is conformally invariant with no intrinsic length scale to supply one; (4) QED nonlinearity only engages near the Schwinger field, energy density short by a factor of 2e34 for intergalactic conditions. Refraction/pressure-support unification (shown to be the same mechanism at c_s=c/sqrt(2)) over-determines rather than rescues this -- still 173x-27,178x too stiff."
    },
    {
        "statement": "a0 = c*H0 (bare, no factor).",
        "status": "Rejected: Domain HH. Using Planck H0, c*H0 is 5.6x too large (460% off) versus the fitted a0=7.55518e-11 m/s^2."
    },
    {
        "statement": "A finite maximum medium/HDF density (rho_max), by itself, prevents supermassive black hole event horizons from forming.",
        "status": "Rejected: horizon-forming density falls as 1/M^2, so above M~20,000 Msun a horizon forms before any stated density cap is reached, regardless of its value -- the cap is never consulted at that mass. Sgr A* (4.3e6 Msun) forms its horizon at a density 50,000x below the stated rho_HDF,max; M87* (6.5e9 Msun) forms its horizon at roughly the density of air. Stiffening the EOS makes this worse, not better, because GR's source term is rho+3P/c^2 (pressure gravitates); Rhoades & Ruffini (1974) proved a maximum mass of ~3.2 Msun for ANY equation of state using only causality (c_s<=c) and GR, which rules out 'add a stiffer exotic phase' as an escape route for supermassive objects. Note: this does NOT rule out a phase transition behind the horizon (the interior question survives) -- only 'no horizon forms at all' is rejected, and only for supermassive masses specifically."
    },
    {
        "statement": "The neutron-core + max-compressed-HDF two-phase structure (used to show no horizon forms for GW150914's ~36 Msun components) also satisfies the Kepler/orbital-frequency constraint at merger.",
        "status": "Rejected: GW150914's ~250 Hz GW frequency near merger requires 65 Msun enclosed within a 240.9 km separation. The two-phase structure can supply at most 6.30 Msun (neutron core capped) + 0.0014 Msun (HDF at ceiling in that small volume) = 6.30 Msun -- short by 10.3x. The required mean density (2.2e15 kg/m^3) falls in the gap between the two allowed phases (48,000x above the HDF ceiling, 200x below the neutron ceiling): neither phase can sit at that density, so the structure has no state available there. Three candidate resolutions were identified but NOT tested: a third phase in the gap; the neutron ceiling being set too low; the 250 Hz reading itself being wrong. No-horizon-formation for GW150914 (excluded_substitutions notwithstanding) is confirmed only in a static/pre-inspiral sense, not through to merger."
    },
    {
        "statement": "The Casimir-shadowing route to the real, measured 43 arcsec/century Mercury perihelion anomaly is a viable independent test of PWC's c^2=K/rho medium relation.",
        "status": "Rejected: required rho_local/rho0=4.65e-4 at Mercury's orbit, under PWC's own c^2=K/rho, either violates c0 as an impedance limit (c_local=46.4*c0) or forces n=1 (zero precession). Route ruled out, short by 5+ orders of magnitude. (Separately: the normalization tested alongside this had zero degrees of freedom -- shadow_deficit*43.0 -- and is not itself evidence either way.)"
    }
])

# --- 2. New domain_status_summary entries (CC through HH, real content, previously undocumented here) ---
m["surrogate_and_numerical_audits"]["domains"].update({
    "CC": {
        "status": "rejected_proxy",
        "detail": "Refraction-index map c^2=K/rho, n=c0/c_local. Inversion (fit n(r) per galaxy) is non-evidential by construction (one free function per galaxy, same information content as a halo fit; median n-1=1.95e-7 across 141 galaxies). Falsifiable half: 40-seed ensemble, HDF choke (0.1363+/-0.0135 dex, 2 params) beats McGaugh RAR (0.1343+/-0.0131 dex, 1 param) in only 7/40 splits.",
        "do_not_interpret_as": "evidence for the refraction picture -- the inversion half proves nothing by construction, and the falsifiable half is negative-to-neutral",
        "methodology_finding": "Single-seed holdout comparisons below ~0.002 dex are not trustworthy in this project -- retroactively flags single-split claims in Domains M and W2 as needing the same multi-seed treatment (confirmed independently tonight 2026-09-21: domain_CC2 through CC8's own 10-seed stability checks were built for exactly this reason)."
    },
    "DD": {
        "status": "reproducible_proxy_result_then_superseded",
        "detail": "domain_DD_surface_tension_solver.py. Refutes the 'g_bar is inconsistent point-mass bookkeeping' critique using real data signatures (negative Vgas at 361/2700 points, interior Vdisk peak at median 2.18 R_d matching Freeman 1970's 2.2, positive inner log-slope in 95.2% of galaxies). Derives g=C_T*A(<r)/4*pi*r^2 ~ M(<r)/r^2 -- shown to be Gauss's law; baryon-only source gives Keplerian decline (NGC 3198 outer slope predicted -0.177 vs observed +0.027, v short 57%). Diffusion-geometry scan best fit 0.2692 dex, worse than RAR (0.1327), flattered by an implied M/L=1.35 vs population-synthesis 0.50 ('that factor is the missing mass itself').",
        "do_not_interpret_as": "a working alternative to dark matter -- it is superseded by Domain EE once medium mass is added to the same Gauss surface"
    },
    "EE": {
        "status": "rejected_proxy",
        "detail": "domain_EE_medium_mass_ledger.py. Corrects DD by including M_HDF in the Gauss surface (126 galaxies): M_med/M_total at R_max median 0.767; M_med/M_bar median 3.29 (cosmological dark:baryon ~5.4). Required profile rho_med~r^-1.92 (isothermal is -2.00) DOES reproduce flat curves structurally. But the decisive gauge-free EOS test (zero fitted parameters) is negative for a universal EOS -- see excluded_substitutions.",
        "do_not_interpret_as": "confirmation of a physical medium substance -- the mass-ledger closure works, but the required stiffness is not a substrate property, it duplicates each galaxy's own V_flat"
    },
    "FF": {
        "status": "rejected_proxy",
        "detail": "Rigid co-rotation extension of EE. Does not break the EOS-universality lock; moves it into an equally unphysical cosmological-spin-parameter requirement (lambda'=0.3945 vs 0.035, 11.3x, 4.8-sigma). See excluded_substitutions.",
        "do_not_interpret_as": "a rescue of the universal-EOS hypothesis"
    },
    "GG": {
        "status": "rejected_proxy",
        "detail": "Two rescue attempts for EE/FF's failure, both rejected: oblateness/binning artifact (scatter survives at 0.570 dex even in the near-spherical-only subsample) and cosmological-spin explanation (see excluded_substitutions).",
        "do_not_interpret_as": "grounds to keep pursuing the universal-EOS/rigid-rotation medium picture without a new mechanism"
    },
    "HH": {
        "status": "rejected_proxy_with_one_open_numerical_coincidence",
        "detail": "Young-Laplace cavitation-boundary EOS for 'galaxy as void in a tensioned sea.' Impedance term Gamma^2=9.5e-15 (14 orders below unity, does no work). Required surface tension needs (u_sea-u_void) to cancel to 1 part in 400,000. a0=c*H0 tested: bare form 460% too large (rejected); a0=c*H0/(2*pi)=1.04e-10 m/s^2 is only -10.2% off the fitted 7.55518e-11 m/s^2, but the 2*pi factor is unearned ('has to be derived, not selected after seeing the target') -- re-verified independently tonight 2026-09-21: c0*H0/(2*pi) with H0=70 km/s/Mpc computes to ~1.08e-10 m/s^2, same order of magnitude, not an exact match, still not derived from anything independent. Credit: Milgrom (1983) already noted a0~cH0 for MOND; this is not a new PWC result. Cross-cutting testable prediction offered but not run: a0(z)/a0(0) = 1.322/1.79/3.032/4.566 at z=0.5/1/2/3 if a0 comes from cosmic tension, checkable against Genzel et al. 2017 (Nature 543, 397) high-z kinematics.",
        "do_not_interpret_as": "a derivation of a0 -- the 2pi is fitted after the fact, and the underlying cavitation-void picture this EOS was built for is independently rejected (see excluded_substitutions)",
        "internal_contradiction_flagged": "Domain HH's cavitation picture requires a galaxy to be LOWER density than the surrounding medium; Domain CC's own refraction measurement (n increasing inward) shows galaxies as HIGHER density than their surroundings. These are direct, unreconciled opposites within the project's own prior work, not resolved by anything read in the 2026-09-21 document pass."
    }
})

# --- 3. New current_derivations entries ---
m["current_derivations"]["supermassive_horizon_formation_theorem"] = {
    "status": "external_rigorous_result_not_a_PWC_derivation",
    "statement": "Horizon-forming density scales as 1/M^2. Above M~20,000 Msun, GR's horizon condition is met before any finite density cap is reached, regardless of the cap's value -- the cap is structurally never consulted at supermassive scale. Sgr A* forms its horizon 50,000x below rho_HDF,max; M87* forms its horizon at roughly the density of air.",
    "supporting_theorem": "Rhoades & Ruffini (1974): maximum mass ~3.2 Msun for ANY equation of state, derived from causality (c_s<=c) plus GR alone -- rules out a stiffer exotic phase as an escape route for supermassive objects specifically.",
    "scope": "Blocks 'no horizon at all' for supermassive black holes under a finite-density-cap picture. Does NOT block a phase transition or finite structure existing behind a horizon once one forms -- that question is untouched.",
    "source": "CONVERSATION_TRANSCRIPT (1).md, read in full 2026-09-21; cites EHT Collaboration 2019 (M87*) and 2022 (Sgr A*) shadow measurements as the real observational anchor for the two masses used."
}
m["current_derivations"]["neutron_HDF_two_phase_GW150914_test"] = {
    "status": "mixed -- confirmed static, falsified at merger",
    "confirmed": "For realistic neutron-core masses (1.4-2.1 Msun) inside 34 Msun of max-compressed HDF at fixed 36 Msun total, max horizon ratio is 0.366-0.479 -- no horizon forms. Genuinely resolves the singularity question for GW150914-scale components in this static regime.",
    "falsified": "Fails the Kepler/orbital-frequency requirement at merger by 10.3x -- see excluded_substitutions. The required density at merger separation falls in an unoccupied gap between the two allowed phases.",
    "open_link_confirmed_still_unresolved_2026-09-21": "Where R_core=30.73 km actually comes from is not stated in any script found in the repository or in any of the 8 documents read today. If independently sourced, rho_max is a genuine prediction; if it came from assuming 2x nuclear saturation density, it is circular (rho_max = M_core/volume). This is the SAME open item already flagged in PWC.md section 13 (the ρ_max/R_core circularity) -- cross-referenced and confirmed still open, not resolved by any of today's source material.",
    "source": "CONVERSATION_TRANSCRIPT (1).md, k=0.8524572447 and the three core masses (28.118/22.255/50.373 Msun) independently reproduced in-transcript; committed to PR #1 (6 commits, c4aa8aa) covers Domains CC-HH and the Medium_Density_Check.py audit only -- the k/core-mass reproduction and the two-phase horizon test were conversation-only, never committed as a script."
}
m["current_derivations"]["competing_flat_rotation_curve_derivation_unreconciled"] = {
    "status": "flagged_needs_reconciliation_not_yet_done",
    "statement": "A second, independent derivation of flat rotation curves exists in the external source material (Deepthink results .pdf): modeling a galaxy as a 2D fluid vortex/pressure sink in a 3D medium, inward tension distributes over the circumference (2*pi*r) giving force ~k/r instead of k/r^2; setting this equal to centrifugal force m*v^2/r cancels r entirely, giving v=sqrt(k/m), independent of radius, with no dark matter and no a0/choke formula at all.",
    "conflict": "This has never been cross-checked against, or reconciled with, the SPARC-tested choke model (g_obs=g_bar*(1+sqrt(a0/g_bar)), a0=7.55518e-11 m/s^2) used throughout this project, including all of tonight's (2026-09-21) domain_CC2-CC8 tension-term tests. They are two different candidate mechanisms for the same observed phenomenon, not two confirmations of the same one.",
    "action_needed": "Reconcile or choose between the two before treating either as PWC's settled flat-rotation-curve mechanism."
}

# --- 4. New citations gathered ---
m.setdefault("external_citations_2026-09-21", []).extend([
    "Rhoades, C. E. & Ruffini, R. (1974). Maximum mass of a neutron star. Phys. Rev. Lett. 32, 324 -- rigorous max-mass-for-any-EOS theorem from causality+GR.",
    "Bullock, J. S. et al. (2001). A Universal Angular Momentum Profile for Galactic Halos. ApJ 555, 240 -- cosmological spin parameter lambda' benchmark (median ~0.035).",
    "Genzel, R. et al. (2017). Strongly baryon-dominated disk galaxies at the peak of galaxy formation ten billion years ago. Nature 543, 397 -- proposed real dataset for testing a0(z) redshift-evolution prediction (not yet run).",
    "Freeman, K. C. (1970). On the disks of spiral and S0 galaxies. ApJ 160, 811 -- analytic Vdisk peak at 2.2 R_disk, used as a real-data cross-check in Domain DD.",
    "Casertano, S. (1983). Rotation curve of the edge-on spiral galaxy NGC 5907. MNRAS 203, 735 -- finite-thickness disk decomposition method referenced in Domain DD.",
    "de Felice, F. (1971). On the gravitational field acting as an optical medium. Gen. Rel. Grav. -- isotropic-refraction-index factor-2 light-bending deficit, flagged open, consistent with PWC.md's own Domain CC light-bending gap.",
    "Milgrom, M. (1983). A modification of the Newtonian dynamics as a possible alternative to the hidden mass hypothesis. ApJ 270, 365 -- original note that a0~c*H0; credited as prior art, not a PWC result.",
    "EHT Collaboration (2019, M87*) and (2022, Sgr A*) -- direct shadow-imaging mass/density anchors used in the supermassive-horizon-formation argument.",
    "Abbott, R. et al. (2023). GWTC-3 population properties. Phys. Rev. X 13, 011048 (arXiv:2111.03634) -- BBH/BNS/NSBH merger rate densities, referenced for an aggregate black-hole energy-budget calculation whose script location was found but printed result not located within the 2026-09-21 read."
])

# --- 5. Top-level record of today's extraction pass itself ---
m["external_document_extraction_2026-09-21"] = {
    "purpose": "User-directed, full (no-skipping) read of 8 external source documents accumulated over prior days of independent work with other AI systems, extracted for physical mechanisms, numbers, confirmed/falsified hypotheses, and citations, then folded into this manifest in its own existing format.",
    "method": "Five parallel sub-agent reads (each given full PWC context from the current session), one file or small group per agent, all results independently verified against this manifest's existing entries and PWC.md before merging -- no item added on a single unverified pass.",
    "documents_processed": [
        {"file": "LETS SEE IF YOU CAN READ BETTER THAN THE LAST FUCK.pdf", "pages": 136, "character": "Perplexity/DeepThink transcript; real bug-fix history for the a0/RMS SPARC result, NANOGrav/RBH-1/Hawking-buoyancy/quicycle discussion, mostly already reflected in PWC.md."},
        {"file": "final hypothesis1.pdf", "pages": 96, "character": "Confirms same a0/RMS provenance chain. Caveat: later half (Hawking buoyancy, quicycle, magnetism-as-HDF/LDF) is validated with markedly less dimensional/empirical scrutiny than the early SPARC-fitting section."},
        {"file": "CONVERSATION_TRANSCRIPT (1).md", "lines": 11313, "character": "Real, code-backed Domains CC-HH falsification chain (committed PR #1, 6 commits, c4aa8aa) plus conversation-only k/core-mass reproduction and the two-phase GW150914 test (never committed as a script). NOTE: an earlier partial read of this same file (referenced Domains II/JJ/KK/LL/MM/NN by commit message) was found this pass to be describing content NOT present in this transcript snapshot -- confirmed via exhaustive grep, zero matches. Those domains come from later work not captured here. ~5,800 of 11,313 lines were sampled via targeted grep rather than read line-by-line (mostly GitHub PR-automation boilerplate and repeated skill-listing reminders on sampling) -- flagged, not claimed as full coverage."},
        {"file": "Deepthink results .pdf", "character": "Real adversarial audit of RBH-1/SMBH-wake mechanics. Contains the competing 2D-vortex flat-rotation-curve derivation (see current_derivations) and internal numerical inconsistencies within the source document itself: the same nucleogenesis energy cost is given as both ~1.8e61 erg and ~1.8e64 erg in different parts of the same file, and SMBH kinetic energy as both ~2e56 erg and ~1.0e59 erg -- flagged as source-document errors, not resolved by picking one."},
        {"file": "aistudiochat.pdf", "character": "Empty -- a single page of share links only, no physics content."},
        {"file": "google perplecxity chat.pdf", "character": "First ~17 pages real: 'heat choke coming in, not out' reframing and a cosmic-web-as-circulation-network table, direct precedent for tonight's (2026-09-21) PWC.md section 9/10 additions. From roughly page 18 on: hype/roleplay with no physics content (a CFD demo that never receives real baseline numbers, a Millennium-Prize tangent, extended mockery of a prior AI session) -- explicitly not logged as physics material."},
        {"file": "Untitled document (2).docx", "character": "Earlier, cruder version of the SPARC a0 fit (additive form g_bar+a0*sqrt(g_bar), point-weighted linear-space RMS): a0=3.82584e-10, 0.28037 dex -- confirms the known bug-fix chain from a pre-fix stage. Explicitly flags unresolved-at-the-time caveats (VizieR schema, inclination-correction status, radius units, signed-velocity convention, point- vs galaxy-balanced RMS) that were later resolved in the final corrected result."},
        {"file": "PhaseWave_GW150914_Pipeline", "character": "Despite the filename, NOT a GW150914 pipeline -- confirmed duplicate of the already-existing domain_Y_density_inversion.py/results.json (Domain Y, density-profile inversion). No new content."}
    ],
    "highest_value_new_items": [
        "Domains DD-HH falsification chain (universal EOS rejected at 4.8-sigma cosmological-spin level; EM-medium-as-substrate rejected on 4 independent, quantified grounds) -- not previously in PWC.md.",
        "Supermassive-horizon-formation theorem (density cap structurally never consulted above ~20,000 Msun; Rhoades-Ruffini 1974 blocks the stiffer-EOS escape route) -- not previously in PWC.md.",
        "Internal contradiction between Domain HH's cavitation picture (galaxy = lower density than surroundings) and Domain CC's own refraction measurement (n increasing inward = higher density) -- flagged, unreconciled.",
        "Confirmation that the R_core=30.73km / rho_max circularity question already flagged in PWC.md section 13 is the exact same open item this external material also leaves unresolved -- independently corroborated, not newly solved.",
        "A second, unreconciled flat-rotation-curve derivation (2D vortex, v=sqrt(k/m)) competing with the SPARC-tested choke model this project actually uses."
    ]
}

json.dump(m, open(f"{D}/provenance_manifest.json", "w", encoding="utf-8"), indent=2)
print("provenance_manifest.json updated.")
print(f"excluded_substitutions: {len(m['excluded_substitutions'])} entries")
print(f"domains tracked: {list(m['surrogate_and_numerical_audits']['domains'].keys())}")
