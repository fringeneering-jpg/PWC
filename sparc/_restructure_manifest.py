import json, collections

d = json.load(open('provenance_manifest.json'))
old_domains = d.pop('domains')

new = collections.OrderedDict()
new['model_version'] = "PWC Universal HDF/LDF Framework v1"
new['model_scope'] = ("A finite, mass-bearing continuum framework in which matter/Sintot, HDF, "
    "LDF propagation, gravitational attraction, redshift, lensing, compact-object saturation, "
    "and gravitational-wave energy release are different regimes of one medium/state system.")
new['git_commit'] = d['git_commit']
new['git_status'] = d['git_status']
new['created_at_local'] = d['created_at_local']
new['environment'] = d['environment']

new['ontology'] = {
    "substrate": {"statement": "Space is not treated as physical nothing. The baseline is a finite, mass-bearing HDF/LDF medium with state-dependent density, stress, propagation geometry, and compressibility.", "status": "PWC premise"},
    "sintot": {"statement": "Sintot is organized/condensed medium inventory. Matter is a stable organized state of the same underlying medium, not an unrelated ontological substance.", "status": "PWC premise"},
    "conservation": {"statement": "Matter-energy is not created from nothing, destroyed at a singularity, or sent through a required separate universe. It reorganizes among condensed Sintot, bound/compressed HDF, baseline HDF, propagating LDF, and outward HDF/gravity-wave modes.", "status": "PWC premise"},
    "physical_limits": {"no_physical_zero": True, "no_physical_infinity": True, "no_singularity": True, "no_required_hard_reflecting_horizon": True, "status": "PWC premise"}
}

new['rules'] = {
    "mass_ledger": {"equation": "M_total = M_Sintot + M_HDF,bound + M_HDF,excess", "status": "PWC premise"},
    "gravity": {"statement": "More locally concentrated HDF medium corresponds to greater pull.", "exterior_constraint": "a(r) = -G*M_ledger/r^2", "status": "PWC premise / required exterior constraint, not yet independently derived from a medium functional"},
    "lensing": {"statement": "LDF/light follows locally straight available paths through curved or inhomogeneous HDF geometry. Bending is path guidance, not necessarily ordinary refractive drag or sub-local-limit photon slowing.", "status": "PWC premise, no ray-equation derivation performed in this session"},
    "redshift": {"statement": "HDF density state determines local process constraint. Emission from denser HDF observed in lower-density HDF/LDF is redshifted relative to the receiver's local process standard.", "status": "PWC premise, no explicit state-to-process mapping derived or tested in this session"},
    "compact_objects": {"statement": "A compact object is a finite high-density HDF/Sintot core plus a continuously descending compressed-HDF envelope.", "hdf_max_density": {"value": 4.6e10, "units": "kg m^-3", "provenance": "PWC compact-object constraint, distinct from neutron/nuclear matter density -- this distinction was itself the subject of a real correction earlier in this session"}, "status": "PWC premise"},
    "mergers": {"statement": "In a merger, compact-core inventory remains accounted for; the outgoing gravity-wave mass equivalent is released excess compressed/bound HDF field inventory.", "event_ledger": "M_1+M_2 = M_final + E_HDF_wave/c^2", "required_refinement": "The emitted fraction depends on the full radial density-envelope structure, relative sizes, overlap geometry, and spin/flow state -- NOT a universal one-constant mass-only fraction. A frozen one-constant version was tested (k~0.8525, and separately f~0.04594) and did not transfer to held-out events (GW190412) -- see excluded_substitutions.", "status": "PWC premise for the identity; the specific frozen-fraction proxy is REJECTED, not the premise itself"}
}

new['excluded_substitutions'] = [
    {"statement": "Finite HDF core means a rigid reflective surface.", "status": "Rejected: finite continuous gradient/trapping is not a mirror."},
    {"statement": "HDF maximum density equals neutron-core nuclear density.", "status": "Rejected: distinct regimes -- this exact conflation was made and corrected earlier in this session's own audit."},
    {"statement": "All compact-object density is uniform at rho_HDF,max.", "status": "Rejected: PWC specifies a finite high-density centre and descending envelope."},
    {"statement": "A local gas pull fraction g_gas/g_bar is identical to accessible HDF volume.", "status": "Rejected: tested directly as Domain R; q_ext converged to 0, no effect."},
    {"statement": "A frozen mass-only merger release coefficient is the PWC merger law.", "status": "Rejected: the true rule requires profile and overlap geometry; the frozen-fraction proxy failed a held-out test (GW190412) earlier this session."},
    {"statement": "PWC requires an empty exterior, singularity, dark-halo particle, or another universe.", "status": "Rejected: contradicts the stated finite-medium ledger."},
    {"statement": "A failed IVP or nonconverged BVP proxy falsifies the universal PWC framework.", "status": "Rejected: it constrains only the precise implemented EOS/boundary/proxy (Domains S/U/U2/V), not the ontology."}
]

new['current_derivations'] = {
    "diffuse_isothermal_HDF_branch": {
        "status": "derived_and_verified_this_session",
        "verification": "Derived analytically (this session) and independently confirmed numerically via Domain V's baryon-free control run (see surrogate_and_numerical_audits.domains.V), which reproduced the predicted asymptotic slope (-2.02 to -2.51 near the outer boundary, target -2) via an actual solve_bvp integration, not by assumption.",
        "assumptions": ["diffuse HDF excess approximately self-gravitating", "spherical outer-limit approximation", "low-density EOS becomes isothermal: P_excess ~ c_s^2*rho_excess"],
        "equations": {
            "hydrostatic": ["dP_excess/dr = -rho_excess*G*M(<r)/r^2", "dM/dr = 4*pi*r^2*rho_excess"],
            "asymptotic_density": "rho_HDF_excess(r) = c_s^2/(2*pi*G*r^2)",
            "asymptotic_mass": "M_HDF(<r) = 2*c_s^2*r/G",
            "asymptotic_speed": "v_c^2 = 2*c_s^2"
        },
        "important_scope": "Analytic existence/asymptotic derivation, numerically confirmed ONLY in the baryon-free control case. Whether the full baryon-coupled, finite-disk boundary problem selects this branch for real galaxies is UNRESOLVED -- Domain V's real-galaxy convergence test found multiple competing solution branches, not a clean selection of this one."
    },
    "compact_hdf_saturation_limit": {
        "status": "PWC fixed physical rule (premise), NOT independently derived",
        "rho_HDF_max": {"value": 4.6e10, "units": "kg m^-3"},
        "endpoint_statement": "Collapse terminates in a finite high-density HDF/Sintot core and a continuous descending HDF transition envelope; no physical zero-volume singularity is used.",
        "status_note": "This is asserted, not derived from a medium functional, in this session's record."
    },
    "unverified_claims_pending_source": {
        "status": "unverified_claim_pending_source",
        "note": "The following numbers were supplied in conversation with no matching script, results file, or raw output located anywhere in this repository. Sample sizes and specifics do not match any run actually performed and archived in this session (all SPARC fits in this repo used the 104-train/45-holdout, 149-galaxy split, seed=7). They are recorded here for the record, NOT as verified results, pending the actual source.",
        "claims": [
            {"label": "132-galaxy fixed n=1/2 SPARC fit", "claimed_rms_dex": 0.1382, "claimed_a0": 7.56e-11},
            {"label": "132-galaxy free-exponent SPARC fit", "claimed_n": 0.599, "claimed_rms_dex": 0.1339},
            {"label": "McGaugh RAR benchmark on the same 132-galaxy sample", "claimed_rms_dex": 0.1327},
            {"label": "41-galaxy dwarf-spheroidal transfer", "claimed_spearman_rho": 0.744, "claimed_p": 2.55e-8, "claimed_rms_dex": 0.253},
            {"label": "compact-object stiffness (K) scan", "claimed_scaling": "R ~ sqrt(K*G*rho_HDF_max)", "claimed_stability": "~1.5% across an eightfold scan in K"},
            {"label": "GW150914-specific bookkeeping", "claimed_masses": "36.2 + 29.1 -> 62.3 Msun", "claimed_release": "~3.0 Msun, ~5.4e47 J"}
        ]
    }
}
new['dataset'] = d['dataset']
new['constants'] = d['constants']
new['data_split'] = d['data_split']
new['quality_cuts'] = d['quality_cuts']
new['scoring_metric'] = d['scoring_metric']
new['comparison_baselines'] = d['comparison_baselines']

new['surrogate_and_numerical_audits'] = {
    "purpose": "Tests, approximations, and solver investigations performed during model development. These do NOT redefine the PWC ontology or replace its specified density-envelope and mass-ledger rules -- they test specific, narrow numerical proxies and closures, several of which were rejected or left unresolved.",
    "status_classes": ["reproducible_proxy_result", "rejected_proxy", "implementation_error", "numerical_nonconvergence", "unverified_external_claim"],
    "domain_status_summary": {
        "M": {"status": "reproducible_proxy_result", "do_not_interpret_as": "a complete PWC continuum derivation -- it is an algebraic phenomenological baseline"},
        "N": {"status": "rejected_proxy", "do_not_interpret_as": "a test of the HDF accessible-volume mechanism -- k_ext converged to ~0"},
        "R": {"status": "rejected_proxy", "do_not_interpret_as": "a test of physical gas permeability -- q_ext converged to 0"},
        "S": {"status": "implementation_error", "detail": "mixed compact-saturation (rho_max) and diffuse-galaxy (rho_gal) normalizations in the same equation"},
        "T_IVP": {"status": "numerical_nonconvergence", "detail": "boundary-independence check failed -- system stayed in a linear, non-attracting regime"},
        "U": {"status": "implementation_error", "detail": "u left unbounded, reached its physical ceiling (u=1); superseded"},
        "U2": {"status": "numerical_nonconvergence", "detail": "killed before completion once a genuine 2-sided BVP was required instead"},
        "V": {"status": "numerical_nonconvergence", "detail": "baryon-free control PASSED; baryon-coupled real-galaxy convergence test FAILED (multiple solution branches); no SPARC fit was attempted"},
        "T_claimed_unverified": {"status": "unverified_external_claim", "detail": "no script, results JSON, or raw per-galaxy output located anywhere in this repository"}
    },
    "domains": old_domains
}

json.dump(new, open('provenance_manifest.json', 'w'), indent=2)
print('rewritten OK')
print(json.dumps(list(new.keys()), indent=2))
