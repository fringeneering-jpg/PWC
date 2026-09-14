# PWC Universal HDF/LDF Framework v1 -- provenance manifest

The primary record leads with PWC's own stated ontology and rules,
clearly tagged as premises (not verified or derived by any script in this
repository). Claude's numerical surrogate tests and solver investigations
are preserved in full but demoted to an appendix
(`Surrogate and numerical audits`, below) -- they test specific, narrow
proxies and closures, several of which were rejected or left unresolved.
They do not define or redefine PWC's ontology.

## Ontology (PWC premise)

- **Substrate**: Space is not physical nothing. The baseline is a finite,
  mass-bearing HDF/LDF medium with state-dependent density, stress,
  propagation geometry, and compressibility.
- **Sintot**: organized/condensed medium inventory -- matter is a stable
  organized state of the same underlying medium, not an unrelated
  ontological substance.
- **Conservation**: matter-energy is not created from nothing, destroyed
  at a singularity, or sent through a required separate universe. It
  reorganizes among condensed Sintot, bound/compressed HDF, baseline HDF,
  propagating LDF, and outward HDF/gravity-wave modes.
- **Physical limits**: no physical zero, no physical infinity, no
  singularity, no required hard reflecting horizon.

## Rules (PWC premise, except where a specific proxy is separately rejected)

- **Mass ledger**: `M_total = M_Sintot + M_HDF,bound + M_HDF,excess`
- **Gravity**: more locally concentrated HDF corresponds to greater pull;
  exterior constraint `a(r) = -G*M_ledger/r^2` (required match, not yet
  independently derived from a medium functional in this session).
- **Lensing**: LDF/light follows locally straight available paths through
  curved/inhomogeneous HDF geometry -- path guidance, not ordinary
  refractive drag or sub-local-limit photon slowing. See dedicated
  section below (open derivation, not yet numerically complete).
- **Redshift**: HDF density state determines local process constraint;
  denser-HDF emission observed from lower-density HDF/LDF is redshifted.
  No explicit state-to-process mapping was derived or tested this session.
- **Compact objects**: a finite high-density HDF/Sintot core plus a
  continuously descending compressed-HDF envelope, `rho_HDF_max =
  4.6e10 kg/m^3` (distinct from neutron/nuclear matter density -- this
  exact conflation was made and corrected earlier in this session's audit).
- **Mergers**: `M_1+M_2 = M_final + E_HDF_wave/c^2` as an identity; the
  emitted fraction requires the full radial density-envelope structure,
  relative sizes, overlap geometry, and spin/flow state -- **a frozen
  one-constant version (k~0.8525, and separately f~0.04594) was tested
  and did NOT transfer to a held-out event (GW190412); the identity is
  retained as premise, the frozen-fraction proxy is rejected.**

## Mass baseline (PWC premise)

`M = L / c0^2` -- L is light (LDF) energy, c0 the speed of light in
vacuum. **Literal energy (light) is the baseline substance, not matter.**
HDF names that same baseline energy in its unlocked state; matter
(Sintot) is derived from it via locking -- energy is not a property
matter happens to contain, the direction runs the other way.

**Historical note (corrected):** this is Einstein's original 1905 form
and notation -- his paper is literally titled "Does the Inertia of a
Body Depend Upon Its Energy Content?", deriving m=L/c^2 for a body
emitting radiation of energy L. This is historically PRIOR to the
popularized E=mc^2 form, not a rearrangement of it -- an earlier note in
this manifest had that backwards and has been corrected. The original
derivation specifically analyzes EMISSION (a body radiating energy loses
mass, from the kinetic-energy mismatch seen in a boosted frame); that
directionality is why the sign convention below matters, not just a
formality.

**Entropy asymmetry (corrected from the earlier, vague "Planck" note):**
M=L/c0^2 is a mass-energy bookkeeping equation, algebraically symmetric
-- it does NOT assert that emission (mass->light) and locking/absorption
(light->mass) are thermodynamically symmetric processes. Emission (a
body radiating energy into the baseline medium) is entropy-favorable,
the same direction as any energy dispersing into a higher-entropy form.
Light spontaneously organizing into a locked, low-entropy Sintot state
is not the free mirror image of that -- it requires a specific,
non-generic driving/compression mechanism, exactly as PWC already
requires (the E_lock/barrier-crossing condition elsewhere in this
manifest was never claimed to be the automatic reverse of emission).
Analogy offered in conversation: multiplying by zero is reversible on
paper, but a real physical reset (e.g. erasing a bit, per Landauer's
principle) has a real minimum thermodynamic cost -- algebraic symmetry
of an equation does not imply the physical process is symmetric or free
in both directions. This reinforces, rather than contradicts, the
existing E_lock/exceptional-reverse-equalisation framing.

**Bookkeeping constraint, binding on all subsequent HDF/LDF/Sintot
mechanics:** any energy released or absorbed as light corresponds to a
mass change, `Delta_M = Delta_L / c0^2`. Sign: Delta_M > 0 when the
defined system absorbs light energy, Delta_M < 0 when it emits light
energy -- set by which the system is doing, not an independent
convention.

## Lensing (PWC premise + open derivation, historically anchored)

**Historical checkpoint -- three convergent half-answers, not one:**

1. *Newton/Soldner (1704 speculation, 1784/1801 calculation).* Newton's
   *Opticks* (Query 1) speculated gravity acts on light. The actual
   Newtonian-mechanics calculation -- light as an ordinary massive
   corpuscle on a hyperbolic trajectory under plain 1/r^2 gravity -- was
   done by Cavendish (1784, unpublished) and independently published by
   von Soldner (1801): `theta = 2GM/(b*c0^2)`. This is the ORIGINAL
   half-answer, over a century before Einstein, from literal particle
   mechanics -- nothing relativistic in it at all.
2. *Einstein, 1911.* Using only the equivalence principle (no spatial
   curvature yet), Einstein independently reproduced the *exact same*
   value, `2GM/(b*c0^2)`, via a wholly different argument (light losing
   energy/frequency climbing a gravitational potential -- the same
   reasoning as gravitational redshift/time dilation). Same number,
   different physics: Einstein did not originate the half-answer, he
   re-derived Newton/Soldner's value from an independent but still
   incomplete principle.
3. *Einstein, 1915.* Full general relativity added a second,
   independent contribution missing from both prior calculations --
   curvature of the *spatial* part of the metric, not just the time
   part. This doubles the result: `theta_GR = 4GM/(b*c0^2)`, confirmed
   by Eddington 1919.

**The domino this session must not repeat:** three historically
distinct calculations (Newton/Soldner's particle mechanics, Einstein
1911's equivalence principle, and any naive "photon slows down in
denser medium" refractive-index picture) all converge on the *same*
single-effect value, because each encodes only one potential
contribution to the light path. This is documented in the
gravity-as-refraction literature: an effective index built naively as
`n(r) = 1 + GM/(r*c0^2)` -- from the same potential that sets
gravitational redshift/time dilation alone -- reproduces only half the
true bending. Matching GR requires `n(r) = 1 + 2GM/(r*c0^2)`, i.e. two
independent contributions summed, not one.

**PWC candidate mechanism, as given in this session (2026-09-14):**
Light (LDF) propagates exactly as it always does. Near a mass, the
medium is a volumetrically heavier but singularly (spherically)
symmetric HDF concentration. This asymmetrically pressures the
surrounding LDF: the pressure on the near side of a photon's path grows
(from the HDF pull), and that gradient pulls the photon toward the
denser side. The resulting path is locally straight *from the photon's
own frame* even though it appears bent externally. Separately: "time"
bending is denied as a distinct entity -- there is no independently
curved time, only density; travelling at (or, for a neutrino, very
near) lightspeed through denser medium is what produces the effects GR
attributes to time dilation, as a direct density/kinematic consequence,
not a second geometric degree of freedom.

**Assessment (applying the same rigor as the mass-baseline corrections
above):**
- The transverse pressure-gradient piece is a real, correct mechanism
  as far as it goes -- mathematically a graded-index refraction /
  Fermat's-principle ray bend, exactly like light curving toward the
  dense side in a GRIN lens or a hot-road mirage. Nothing invented here.
- *Open problem:* by itself this is mechanically the same single-
  potential family flagged above. A photon path bent by one
  density-derived pressure/index field, sourced from the same `rho(r)`
  that also accounts for the redshift-like ("time") effect, reproduces
  only `2GM/(b*c0^2)` -- the historical half-answer -- for the identical
  structural reason all three prior attempts did.
- Denying "time bending" as a separate entity and reducing it to a
  density/speed consequence for the photon is a coherent ontological
  move (fewer primitives: density + motion, not density + motion + a
  separate curved-time substance) -- but it does not, by itself, supply
  the missing second contribution to the bending angle. It only
  relabels one of the two required pieces. If PWC has only one
  density-sourced effect doing all the work, the deflection still comes
  out at half value regardless of what that one effect is called.
- *What is actually required:* HDF compression must contribute to the
  photon's path in two mechanically distinct ways: (1) the pressure/
  index-gradient steering already described (supplies the
  "time-dilation-equivalent" half), and (2) an independent effect of the
  compression on the proper spatial path length through the compressed
  region itself (the "space" half) -- an equal, separate contribution.
  Collapsing both into a single `rho(r)`-sourced index law, however
  physically motivated the description, will not clear this bar without
  being checked quantitatively against the known `4GM/(b*c0^2)` target.

**Ontological refinement (2026-09-14): "HDF is the photon's path."** Not
a separate medium the photon crosses through a distinct background
space -- there is no space independent of HDF's own density/geometric
structure; the photon's path and the HDF structure are the same thing,
not two things in causal contact. This removes the need to invent a
*second, independent* physical mechanism for the missing contribution
above -- there is only ever one substrate. But it does not by itself
hand over the doubling factor. The correct reframed question: does
HDF's own compression response enter the photon's path in two distinct
*geometric roles* (an index/speed-like role and a proper-path-length
role), correctly weighted, rather than one role counted once? Real
precedent: de Felice (1971, *Gen. Rel. Grav.* 2:347) showed that
treating Schwarzschild lensing via a naive *isotropic* refractive index
built from the Newtonian potential alone under-predicts bending by
exactly a factor of 2 -- full GR bending is recovered only when the
effective medium's index is *anisotropic*, differing for radial vs
tangential propagation, because that is what encodes both metric
components (`g_tt` and `g_rr`) doing equal work from one field (see
also Evans & Nandy 2000 for the explicit refractive-index treatment of
exact Schwarzschild spacetime). Same substrate, two roles -- not two
fields. Reframed open question: does HDF's compression response to a
mass concentration act anisotropically -- steering a photon differently
along its direction of travel than transverse to it -- with the
specific relative weighting that reproduces `4GM/(b*c0^2)` rather than
`2GM/(b*c0^2)`? Not yet computed.

**Watermelon-seed analogy (2026-09-14), as a qualitative motivation for
that anisotropy:** a seed squeezed between fingers does not drift
sideways in proportion to a gentle pressure gradient (that is the mild,
linear picture -- the half-answer mechanism above); it shoots out,
because it is nearly incompressible -- confinement along the squeeze
axis has nowhere to go, so the stress relief is dumped almost entirely
into the transverse direction, out of proportion to the squeeze itself.
This is a genuinely nonlinear, anisotropic response of exactly the
shape de Felice's analysis requires. **This is qualitative motivation
only, not a derivation** -- it supplies a physical reason to expect
anisotropy of the right general shape, not a specific numerical factor;
it is explicitly not a claim that the analogy alone yields the factor
of 2. That must come from HDF's actual constitutive/EOS response
(bulk vs effective transverse stiffness) worked through quantitatively.

**Status: OPEN.** No numerical PWC bending-angle calculation exists yet.
No `rho(r)`-to-refractive-index law and no `rho(r)`-to-proper-path-
length law have been established anywhere in this project's files --
tonight's compressibility figures (`e_EOS(rho)`, `rho_HDF_max`, the
hydrostatic EOS machinery from the SPARC domains) describe the medium's
own *mechanical* compression response and can supply an input density
profile `rho(r)`, but do not by themselves constitute either of the two
optical laws above. Both must be derived (or the single mechanism shown
to genuinely contain two independent contributions when worked through
in full) before a bending angle can honestly be computed and compared
to the `2GM/(b*c0^2)` vs `4GM/(b*c0^2)` benchmark.

## Excluded substitutions (explicitly rejected, so they cannot re-enter quietly)

| Substitution | Status |
|---|---|
| Finite HDF core means a rigid reflective surface | Rejected -- finite continuous gradient/trapping is not a mirror |
| HDF maximum density equals neutron-core nuclear density | Rejected -- distinct regimes; this exact error was made and corrected in this session |
| All compact-object density is uniform at rho_HDF,max | Rejected -- PWC specifies a finite high-density centre and descending envelope |
| Local gas pull fraction g_gas/g_bar equals accessible HDF volume | Rejected -- tested directly as Domain R; q_ext converged to 0 |
| A frozen mass-only merger release coefficient is the PWC merger law | Rejected -- failed a held-out test (GW190412) |
| PWC requires an empty exterior, singularity, dark-halo particle, or another universe | Rejected -- contradicts the finite-medium ledger |
| A failed IVP or nonconverged BVP proxy falsifies the universal PWC framework | Rejected -- constrains only the specific implemented proxy (Domains S/U/U2/V) |

## Current derivations

**Diffuse isothermal HDF branch -- derived and verified this session.**
Derived analytically this session and independently confirmed numerically
via Domain V's baryon-free control run (an actual `solve_bvp` integration
reproducing the predicted asymptotic slope, -2.02 to -2.51 near the outer
boundary against a target of -2 -- not assumed, checked).
```
dP_excess/dr = -rho_excess*G*M(<r)/r^2,  dM/dr = 4*pi*r^2*rho_excess
=> rho_HDF_excess(r) = c_s^2/(2*pi*G*r^2),  M_HDF(<r) = 2*c_s^2*r/G,  v_c^2 = 2*c_s^2
```
**Scope, stated plainly**: this is confirmed ONLY in the baryon-free
control case. Whether the full baryon-coupled, finite-disk problem
selects this branch for real galaxies is UNRESOLVED -- Domain V's
real-galaxy convergence test found multiple competing solution branches,
not a clean selection of this one.

**Compact HDF saturation limit -- status: `external_session_derived_pending_archival`.**
`rho_HDF_max=4.6e10 kg/m^3` (finite core + descending envelope, no
singularity) is claimed to have been derived in a separate Perplexity
conversation on 2026-09-14, using a black-hole minimum-density/
maximum-density argument. That transcript is not accessible from this
Claude session and is not present anywhere in this repository. This
session's search establishes only that no transcript/derivation record
exists locally -- **not** that the derivation didn't happen elsewhere.
Explicitly NOT classified as: arbitrary, invented, a free parameter,
unsupported assertion, absent, or Domain-S-originated. It remains, as
before, a declared input value used by Domains S/T/U/V -- that use is
unchanged; only the description of its own origin changed. Upgrading
this to verified/derived-and-checked requires the original transcript
(or the black-hole objects/masses/radii, equations, and selection rule
it used) to be archived here. Until then it stays at this status.

This is a separate question from the K-scan parameter reconciliation
below, which was resolved independently (via script dates and vocabulary
absence, not via this value's own provenance) and is not being reopened.

**Correction (post-initial-draft):** the first version of this manifest
wrongly tagged the next two items as `unverified_claim_pending_source`.
They were sitting in this exact repository the whole time -- I failed to
cross-check pre-existing files (created before tonight's domain_M-V work)
against the claims before writing the first draft. Corrected below.

**132-galaxy SPARC transition-shape result -- Tier A, locally reproduced.**

| Field | Value |
|---|---|
| model_version_label | PWC-SPARC-domain-K (pre-existing, predates tonight's domain_M-V work) |
| script_path / sha256 | `sparc/domain_K_rar.py` / `EE0743EE18ACB95C49A96CB933EA9DA388D51DDD791C86448A095BDFB52BA567` |
| result_file_path / sha256 | `sparc/domain_K_results.json` / `2C0AB72EBF0DC23AB69652B104467D1EAF958233DC4DEF703F434BFA68C1F51D` |
| source_data | `sparc/vizier_t1.txt`, `sparc/vizier_t2.txt` (checksums as recorded above) |
| command_to_verify | `cd sparc && python domain_K_rar.py` |
| metric | RMS of (log10(g_obs)-log10(g_pred)), dex, n=132 usable galaxies |
| a0 provenance | fit via bounded scipy.optimize, not fixed a priori |
| n=0.5 provenance | forced by the flat-rotation-curve/low-acceleration requirement -- a genuine zero-choice constraint, not a fit |
| n=0.598849 provenance | fit jointly with a0, an empirical refinement, not forced |
| verified results | n=0.5: a0=7.5586e-11, rms=0.13824 dex; n=0.598849 (free): rms=0.13392 dex; McGaugh RAR: rms=0.13265 dex |
| cross_reference | `unified_framework_consolidated_2026-08-13.md`, lines 130, 356-358, 339-369 |

Source's own honest caveat retained: the transition-sharpness parameter
s=1.51 (a separate, related test) is fitted, not derived, unlike n=1/2
which is forced by the flat-rotation-curve requirement itself.

**41-galaxy dwarf-spheroidal transfer -- Tier A, locally reproduced.**

| Field | Value |
|---|---|
| model_version_label | PWC-SPARC-domain-L (pre-existing, predates tonight's domain_M-V work) |
| script_path / sha256 | `sparc/domain_L_dsph_test.py` / `700081CD1AE2046079369C80B79963D1D897C8DAEB876F67759C5E414DD0A087` |
| result_file_path / sha256 | `sparc/dsph/domain_L_results.json` / `33E696A2FD2E689AA43703A8AFCFB957C4D5AB80DAD0D464309D2A841D719736` |
| source_data | `sparc/dsph/dsph_data.tsv` (McConnachie 2012, VizieR J/AJ/144/4) / `BC08AF595A36BC3A7213CD4AA63413911C36B802C4C5A6E3CD48D7FE65B8CA64`; plus `dsph_raw.txt`, `dsph_fields.txt` |
| command_to_verify | `cd sparc && python domain_L_dsph_test.py` |
| metric | Spearman rho + RMS (dex), n=41 gas-free/gas-poor dwarfs (M_HI/M_star<0.05) |
| parameter provenance | (a0, s) carried unchanged from the globally-fitted free-shape SPARC relation -- no dwarf-specific refit; genuine out-of-sample transfer |
| verified results | n=41, rho=0.7436, p=2.5507e-08, rms=0.25302 dex |
| cross_reference | `unified_framework_consolidated_2026-08-13.md`, Part 8, line 411+ |

**Compact-object K-scan parameter reconciliation -- RESOLVED.**

Method: full read of both scripts, grep for `hdf|sintot|neutron|core`
(zero occurrences in either file), and a file-date comparison against
`dynamic_knot_solver.py` (where the HDF/LDF/Sintot vocabulary and
`rho_HDF_max=4.6e10` actually originate).

| Field | Value |
|---|---|
| local_artifacts | `PWC/stiffening_K_scan.py` (2026-09-10), `PWC/continuous_stiffening_limit.py` (2026-09-10) |
| reference_point | `PWC/dynamic_knot_solver.py` (2026-09-13) -- 3 days *after* the compact scripts |
| finding | Neither compact script contains "hdf", "sintot", "neutron", or "core" anywhere -- they predate that vocabulary entirely. Their own comments/setup ("real degenerate/incompressible matter", GW150914-relevant total mass ~28-36 Msun, radii checked in the tens-of-km range) unambiguously describe compact-object/nuclear-density-scale core material -- 4.6e17 kg/m^3 sits at the nuclear saturation density scale, a categorically different regime from the diffuse, kpc-scale galactic medium parameter used tonight |
| conclusion | Combination of explanations 1 and 3: a genuinely different density variable (compact/degenerate core density vs diffuse HDF medium density) from an earlier model version, not a transcription error and not a genuine parameter conflict -- neither script asserts these are the same quantity |
| remaining_action | Neither script gives its rho_max an explicit, disambiguated name (e.g. rho_Sintot_max / rho_core_max) -- recommended naming fix going forward, not a retroactive claim about what the scripts already say |

Independent of the naming question, running both scripts directly still
does not reproduce the specific claimed "~1.5% stable across an eightfold
K scan": `stiffening_K_scan.py` shows R_envelope varying from 0.006 km to
19,053.7 km (6+ orders of magnitude) across K=1e7 to 1e20. That finding
stands on its own, separate from the now-resolved naming question.

**GW150914-specific ledger (62.3 Msun final, ~5.4e47 J) -- partially
source-recorded.** The general interpretive framing ("the ~3 solar masses
conventionally described as radiated in GW150914 are interpreted as
involving space/the medium itself") is real, at `PWC.md` line 133. The
specific numbers (36.2+29.1->62.3 Msun, 5.4e47 J) do not appear in
`PWC.md` or `pwc_gw150914_pipeline.py`, and no matching results file was
located. Qualitative interpretation: Tier B. Specific quantitative ledger:
unverified pending its actual source.

An externally pasted, temporary AWS S3 pre-signed URL was offered as a
supporting source for some of the above. It was NOT fetched -- a
short-lived signed link cannot be authenticated or archived as a
provenance source, and pulling arbitrary external content into a
provenance document defeats the purpose of the document.

---

# Surrogate and numerical audits (appendix)

Tests, approximations, and solver investigations performed during model
development. These do NOT redefine the PWC ontology or replace its
specified density-envelope and mass-ledger rules above.

| Domain | Status | Do not interpret as |
|---|---|---|
| M | reproducible_proxy_result | a complete PWC continuum derivation -- it is an algebraic phenomenological baseline |
| N | rejected_proxy | a test of the HDF accessible-volume mechanism -- k_ext converged to ~0 |
| R | rejected_proxy | a test of physical gas permeability -- q_ext converged to 0 |
| S | implementation_error | mixed compact-saturation (rho_max) and diffuse-galaxy (rho_gal) normalizations in the same equation |
| T-IVP | numerical_nonconvergence | boundary-independence check failed -- linear, non-attracting regime |
| U | implementation_error | u left unbounded, reached its physical ceiling (u=1); superseded |
| U2 | numerical_nonconvergence | killed before completion once a genuine 2-sided BVP was required |
| V | numerical_nonconvergence | baryon-free control PASSED; real-galaxy convergence FAILED (multiple branches); no SPARC fit attempted |
| T (claimed) | unverified_external_claim | no script, results JSON, or raw output located anywhere in this repository |

The detailed per-domain equations, parameters, solver settings, and
results below are preserved in full from the original manifest.

## Environment

| Field | Value |
|---|---|
| git_commit | **N/A -- not a git repository.** `git rev-parse --show-toplevel` fails at both `C:\Users\jaden\cosmology\sparc` and `C:\Users\jaden\cosmology`. No commit hash exists to anchor this work. |
| python | 3.12.10 (MSC v.1943 64 bit AMD64) |
| scipy | 1.15.3 |
| numpy | 2.4.6 |
| host paths | All scripts/data under `C:\Users\jaden\cosmology\sparc\` |

## Dataset

| Field | Value |
|---|---|
| Source | Lelli, McGaugh & Schombert 2016, AJ 152, 157 ("Mass models for 175 disk galaxies with SPARC"), fetched via VizieR (J/AJ/152/157), tables 1 and 2 |
| dataset_checksum (vizier_t1.txt, SHA256) | `997D56A52580F78C762C1A146B6BE0FD9101E420146A5C9196BB9D1D53DB48A9` |
| dataset_checksum (vizier_t2.txt, SHA256) | `6E4B35B8F488B64AA5CA0E9D4B7B924FBB1BABCEEA50138E9AB17BB42A764093` |
| Retrieval date recorded in file header | 2026-08-04T15:14:14/16 (VizieR query timestamp in file) |

## Galaxy split

| Field | Value |
|---|---|
| galaxy_split_seed | `np.random.default_rng(7)` -- IDENTICAL across every domain (M, N, R, S, T, U, U2, V) |
| Split ratio | 70% train / 30% holdout, `n_train = int(0.7*len(shuffled))` |
| Resulting counts | 104 train galaxies, 45 holdout galaxies |
| Split method | Galaxy list sorted, then `rng.shuffle(shuffled)`, first 104 -> train, remaining 45 -> holdout (galaxy-level split, not point-level -- all radial points for a given galaxy stay in the same set) |

## Quality cuts (identical across all domains)

```
m  = (R > 0) & (Vobs > 0) & isfinite(e_Vobs)
m &= (e_Vobs/Vobs <= 0.10)      # <=10% velocity error
m &= (inclination >= 30.0)      # deg, avoids face-on projection error
m &= (Qual <= 2)                # SPARC quality flag: 1=high, 2=medium; excludes 3=low
```
Additional cut used ONLY in the ODE-based continuum domains (S, T, U, U2, V),
not in the algebraic domains (M, N, R): galaxies with fewer than 3 tabulated
radial points are dropped (`if len(r_kpc) < 3: continue`), since a 2-variable
coupled ODE integration is not meaningful over fewer points.

## SI unit conversions (identical across all domains)

| Symbol | Value | Meaning |
|---|---|---|
| KPC | 3.0856775814913673e19 m | 1 kpc in metres |
| KMS | 1.0e3 m/s | 1 km/s in m/s |
| conv | (KMS^2)/KPC = 3.24078e-14 | converts (km/s)^2 / kpc -> m/s^2 |
| G | 6.674e-11 m^3 kg^-1 s^-2 | Newton's constant -- **declared approximation**: CODATA recommended value is 6.67430e-11; the 4th significant figure differs. Not re-run with the more precise value. |
| UPS_D | 0.5 | disk mass-to-light ratio at 3.6um (standard SPARC literature convention) |
| UPS_B | 0.7 | bulge mass-to-light ratio at 3.6um (standard SPARC literature convention) |

g_bar and g_obs constructed as:
```
g_obs = Vobs^2 / R * conv
Vbar2 = Vgas*|Vgas| + UPS_D*Vdisk*|Vdisk| + UPS_B*Vbulge*|Vbulge|
g_bar = Vbar2 / R * conv
```

## Model versions, equations, parameters -- one row per domain actually run

### Domain M / N / R (algebraic, no ODE)
- **model_version**: `domain_M_heldout_comparison.py`, `domain_N_medium_in_gas.py`, `domain_R_accessible_volume.py`
- **Equations**:
  - RAR (empirical baseline): `g_obs = g_bar/(1-exp(-sqrt(g_bar/a0)))`
  - choke n=1/2 (PWC proxy): `g_obs = g_bar*(1+sqrt(a0/g_bar))`
  - Domain N extension: `g_bar_ext = g_bar + k*g_gas`, k fit jointly with a0
  - Domain R extension: `C = Pi_gas^q`, `Pi_gas = g_gas/g_bar`, applied as `g_obs = g_bar*(1+sqrt(a0/g_bar)*C)`
- **Parameters, bounds, provenance**:
  - a0: fit per-domain via `minimize_scalar`, bounds `10^[-12,-9]` (log-space), no fixed prior value
  - k (Domain N): fit via Nelder-Mead jointly with a0, bounds `0<=k<=20`
  - q (Domain R): fit via Nelder-Mead jointly with a0, bounds `-5<=q<=5`
- **Optimizer**: `scipy.optimize.minimize_scalar` (bounded, Brent) for a0-only fits; `scipy.optimize.minimize` (Nelder-Mead, `xatol=1e-8,fatol=1e-12,maxiter=6000-8000`) for joint fits
- **Scoring metric**: RMS of `log10(g_obs)-log10(g_pred)`, i.e. dex
- **Results** (holdout, dex): RAR 0.1298 (train 0.1338); choke 0.1387 (train 0.1380); Domain N extended 0.13873 (k_ext~1.7e-14, statistically zero, unchanged from baseline); Domain R extended: unchanged from baseline (q_ext=0.0000)
- **Residual-vs-gas-fraction**: rho=+0.166, p=0.0424 (Domain N/R, unchanged by either extension)

### Domain S (coupled ODE, IVP, OUTWARD integration) -- REJECTED, normalization bug
- **model_version**: `domain_S_coupled_hdf.py`
- **Equations**: `du/dr` normalized by `(rho_max-rho_bg)` in the denominator while `rho_excess=rho_gal*chi` used a SEPARATE, independently-fit `rho_gal` -- confirmed (not assumed) via direct diagnostic: 1/|dchi/dr| ~ 7.24e33 kpc at a typical point, chi range across the full radial span of every one of 10 tested galaxies was bit-identical `[0.300994, 0.300994]` (zero evolution)
- **Parameters/bounds**: rho_gal (fit, log10 search unconstrained via Nelder-Mead from x0=log10(1e-22)), c_s0 (fit, x0=log10(3e4)), chi0 (fit, x0=logit(0.3)) -- 3 free global parameters
- **Fitted values**: rho_gal=6.8494e-22 kg/m^3, c_s0=5.2940e4 m/s, chi0=0.300994
- **Initial condition**: M_HDF(r_min)=0, chi(r_min)=chi0 (fitted, universal across all galaxies)
- **Solver**: `scipy.integrate.solve_ivp`, RK45, rtol=1e-7, atol=1e-6, max_step=(r_max-r_min)/50
- **Optimizer**: Nelder-Mead, xatol=1e-4, fatol=1e-8, maxiter=maxfev=400
- **Results**: train RMS 0.2897 dex, holdout RMS 0.3293 dex, outer log-log slope of rho_excess: 0.000 (median, both sets) -- confirmed uniform-density branch, M_HDF~r^3
- **Per-galaxy raw profiles**: `domain_S_audit_profiles.json` -- 10 representative galaxies, full radial arrays (r, chi, rho_excess, M_HDF, M_bar, g_pred, g_bar, v_pred, v_obs) plus outer alpha_rho/alpha_M/alpha_v

### Domain T-IVP (coupled ODE, IVP, OUTWARD integration, corrected u normalization)
- **model_version**: `domain_T_corrected_hdf.py`
- **Equations**:
  ```
  u(r) = rho_excess(r)/rho_gal, 0<=u<1
  dM_HDF/dr = 4*pi*r^2*rho_gal*u
  g_pred = G*(M_bar(<r)+M_HDF(<r))/r^2
  du/dr = -(rho_bg+rho_gal*u)*g_pred*(1-u) / (rho_gal*c_s0^2)     [F(u)=1/(1-u), rho_max REMOVED from this equation entirely]
  chi_compact(r) = rho_gal*u(r)/(rho_max-rho_bg)                   [diagnostic-only, never fed back]
  ```
- **Parameters/bounds**: rho_gal, c_s0 (2 free global parameters; u0 FIXED, not fit, at U0_TINY=1e-6)
- **Fitted values**: rho_gal=3.1999e-16 kg/m^3, c_s0=3.5529e5 m/s (predicts v_flat=502.46 km/s)
- **Initial condition**: M_HDF(r_min)=0, u(r_min)=1e-6 (fixed, universal, not fitted -- chosen to remove the "arbitrary universal chi0" problem found in Domain S)
- **Boundary-independence check result**: FAILED -- outer M_HDF scaled exactly linearly with the choice of u0 (1e-8/1e-6/1e-4 -> M_HDF scaled 1x/100x/10000x), i.e. the system stayed in a linear (non-attracting) regime rather than reaching the claimed isothermal-sphere attractor
- **Solver**: solve_ivp, RK45, rtol=1e-8, atol=1e-6, max_step=(r_max-r_min)/100
- **Optimizer**: Nelder-Mead, xatol=1e-4, fatol=1e-8, maxiter=maxfev=300
- **Results**: train RMS 0.2745 dex, holdout RMS 0.2801 dex, outer alpha_u: -0.129 (train)/-0.136 (holdout) [target -2, not reached], BTFR slope 2.834 (r=0.934, n=141) [literature ~3.5-4]
- **rho_bg**: fixed at 0 (declared gap, not fit -- not among the listed globally-fit parameters)
- **f(chi)/f(u) form**: identity, f(u)=u (declared gap -- not otherwise specified in the request this domain was built from)

### Domain U / U2 (coupled ODE, IVP, INWARD shooting from analytic SIS boundary) -- INCOMPLETE, superseded
- **model_version**: `domain_U_shooting_bvp.py` (first attempt, R_FAR_MULT=50, KILLED after ~14 min for pathological slowness/CPU-bound stiffness); re-run with R_FAR_MULT=15 and bounded parameter search (`domain_U_shooting_bvp.py`, edited in place -- same filename, two different configs, see git_commit caveat above for why this isn't independently version-pinned)
- **Boundary condition**: u(r_far) = c_s0^2/(2*pi*G*rho_gal*r_far^2) (analytic SIS value, r_far=15x each galaxy's max tabulated radius), integrated INWARD to r_min; u NOT sigmoid-bounded in this version (bug, identified and only fixed in the next attempt)
- **Fitted values (R_FAR_MULT=15 run)**: rho_gal=3.2576e-20 kg/m^3, c_s0=2.6887e5 m/s (v_flat=380.24 km/s)
- **Results**: train RMS 1.1120 dex, holdout RMS 1.1211 dex, `all_physical=False` (u reached exactly 1.000 for the first sanity-check galaxy), BTFR slope -26.776 (nonsensical), residual-vs-gas-fraction rho=-0.822, p~0 -- **explicitly flagged as an invalid/pathological result, not a physics conclusion**, per direct instruction, since u was unbounded and hit its physical ceiling
- **Domain U2** (`domain_U2_audited.py`): rebuilt with sigmoid-bounded u and a saturation penalty in the optimizer objective; **launched but KILLED before completion** once the requirement to use a genuine two-sided BVP (not any IVP/shooting variant) was given. No completed results exist for U2. `domain_U2_per_galaxy.json` was NOT produced (job killed before that stage).

### Domain V (proper two-sided BVP, scipy.integrate.solve_bvp) -- convergence-tested only, NOT fit to SPARC
- **model_version**: `domain_V_bvp.py`
- **Equations** (identical physical content to Domain T-IVP/U, different solution method):
  ```
  du/dr     = -(rho_bg+rho_gal*u)*G*(M_bar(r)+M_HDF)/r^2*(1-u) / (rho_gal*c_s0^2)
  dM_HDF/dr = 4*pi*r^2*rho_gal*u
  ```
- **Boundary conditions** (2, matching the 2 first-order ODEs):
  1. `M_HDF(r_min) = 0`
  2. At r_far: `RHS_du/dr(u,M_HDF,r)|_{r_far} = -2*u(r_far)/r_far` (derivative-matching to the SIS asymptotic slope, NOT a fixed value for u(r_far) -- the amplitude is left to emerge from the full nonlinear solve)
- **u boundedness**: NOT sigmoid-transformed in this version; u clipped to (1e-12, 1-1e-12) only inside the RHS/bc evaluation, and any solution with u exiting (0,1) on the full mesh is meant to be flagged invalid (this flagging was implemented for the diagnostic prints but not yet wired into a full pass/fail gate across all 149 galaxies)
- **Solver**: `scipy.integrate.solve_bvp`, initial mesh `np.geomspace(r_min, r_far, n_mesh)` with n_mesh=60-100, initial guess = analytic SIS profile, `tol=1e-6`, `max_nodes=20000`
- **Mesh/r_far convergence settings tested**: R_FAR_MULT in {15, 25, 50, 100} x each galaxy's own max tabulated radius, on 3 representative galaxies (NGC2403, DDO154, NGC3198), with and without continuation (using the previous r_far's converged solution as the next initial guess)
- **Validation control** (Mbar=0 identically): PASSED -- local log-log slope of u(r), measured away from either boundary, transitions through -0.45 -> -2.17 -> -2.51 -> -2.14 -> -2.02 approaching r_far, confirming the solver correctly reproduces the known regular-isothermal-sphere asymptotic behavior
- **Real-galaxy r_far convergence result**: FAILED -- non-monotonic, non-convergent across r_far for 2 of 3 galaxies even with continuation; NGC2403 failed outright (mesh node limit exceeded) at mult=50; DDO154 jumped to a saturated branch (u_max=0.99996) at mult=50 then failed at mult=100; NGC3198 collapsed to a solution 4 orders of magnitude smaller at mult=50 then failed at mult=100. Only NGC3198's mult=15/25 pair (without continuation) showed values agreeing within ~20%.
- **Parameters used for the convergence test**: rho_gal=1e-21 kg/m^3, c_s0=1e5 m/s -- **arbitrary placeholder values, NOT fit to data** (the convergence test was run to check solver behavior before any fitting was attempted; per the explicit instruction, the SPARC fit was NOT run given this non-convergence)
- **No completed SPARC fit exists for Domain V.** No per-galaxy convergence table across all 149 galaxies exists. No raw radial output archive exists beyond the 3 manually-tested galaxies' console output (not saved to a JSON file).

## Comparison baselines (all on the same 104/45 split, same quality cuts)

| Model | Train RMS (dex) | Holdout RMS (dex) | Status |
|---|---|---|---|
| Empirical McGaugh RAR | 0.1338 | 0.1298 | baseline, a-theoretic |
| PWC choke n=1/2 | 0.1380 | 0.1387 | baseline, PWC algebraic proxy |
| Domain S (buggy normalization) | 0.2897 | 0.3293 | rejected -- confirmed normalization bug |
| Domain T-IVP (corrected normalization, IVP) | 0.2745 | 0.2801 | boundary-independence check failed |
| Domain U (IVP inward-shooting, unbounded u) | 1.1120 | 1.1211 | invalid -- u hit 1, flagged pathological |
| Domain U2 | -- | -- | incomplete, killed before results |
| Domain V (BVP) | -- | -- | convergence test failed before any fit attempted |
| "Domain T" pasted claim (source script not in this repo) | 0.1344 | 0.1368 | **not independently reproduced** -- no runnable script for this specific claim has been provided or located on disk |

## What this manifest does NOT contain (explicit gaps, not silently omitted)

- No git commit hash exists anywhere in this project tree.
- No completed per-galaxy convergence table exists for Domain U2 or Domain V.
- No raw radial-output archive exists for Domain T, U, U2, or V (only Domain S has `domain_S_audit_profiles.json`).
- The pasted "Domain T" result (RMS 0.1344/0.1368, alpha_rho=-1.986, BTFR=3.92) has no corresponding script, results JSON, or per-galaxy table on this disk -- it cannot currently be checksummed, re-run, or independently verified against this manifest's data/split/cuts.
