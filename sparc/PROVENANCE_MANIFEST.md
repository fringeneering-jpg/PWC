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
  **Regime-dependence resolution (2026-09-14):** "light limited to light
  speed, neutrinos to neutrino speed" -- different things have their own
  characteristic behavior within one medium, resolving the apparent
  contradiction between "HDF gravity is plain 1/r²" (asserted earlier
  this session) and "HDF tension can also behave MOND-like at low
  acceleration" (needed for the Bullet Cluster punch-through
  translation below). MOND's own math is built this way -- its
  interpolating function collapses to plain Newtonian 1/r² at high
  acceleration (solar-system/dense regime) and only departs (boosts) at
  low acceleration; not boosted everywhere. Same shape as PWC's own
  already-logged Bogoliubov dispersion for the (ρ,θ,u) continuum:
  phonon-like at low momentum, free-particle-like at high momentum, one
  medium, two genuinely different regimes, no contradiction. "1/r²
  works" and "a separate low-acceleration regime behaves differently"
  are not competing claims. **What remains open:** this resolves the
  logical tension, not the derivation -- knowing the split is permitted
  is not the same as showing HDF tension actually reproduces it, in the
  boosting direction, at the correct scale (`a0 ~ 1.2e-10 m/s²`). No
  such derivation exists anywhere in this project; the Bogoliubov
  phonon/free-particle split is the template for how one could arise.
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

**Entropy ironing mechanism (2026-09-14):** the medium (HDF) is a fluid,
tension-bearing superfluid (see Lensing section below). It "irons
itself into the medium" via matter (Sintot/locked structures) acting as
the iron: matter falling into / merging with mass concentrations,
radiating energy back into HDF (`M1+M2 = M_final + E_HDF_wave/c0^2`,
already on record), consumed/used up irreversibly in the process --
"kamikaze pilots," one-way, no return trip. Same entropy-favorable
direction as the emission side of the entropy asymmetry above.

**Refinement:** a single large merger/kamikaze event (the "scraper")
only reaches gross-scale tension features in the medium. Effective
ironing/smoothing requires the energy broken down to fine grain,
distributed throughout the medium (the "water pick"), reaching
irregularities a single macro-scale event cannot. Real grounding: this
matches the established physics of turbulent energy cascade (Kolmogorov,
1941) -- a large-scale disturbance cannot dissipate into heat directly
at the scale it is injected; it cascades down through progressively
smaller eddies until reaching the scale where viscosity actually
converts motion into heat. The large event is the correct *direction*
(entropy-favorable, one-way, consumes the matter involved) but not by
itself the correct *grain* -- the released energy must cascade to fine,
widely distributed interactions before the medium's tension actually
relaxes.

**Honest caveat:** qualitative and structurally coherent, not a
derivation. No cascade rate, dissipation scale, or fine-vs-macro
efficiency ratio has been computed or measured for HDF anywhere in
this project. Refines, does not replace, the Mergers rule and entropy-
asymmetry note above; may eventually bear on how HDF's tension actually
relaxes near a mass concentration (relevant to the open lensing
derivation below), but supplies no number yet.

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

**Root-cause domino chain (2026-09-14), fixing the historical hand-wave
at its source:** the standard telling of Newton/Soldner's calculation
treats "assume light has a tiny mass, then let it vanish as m→0" as a
delicate limit needing justification. It is not. Impulse approximation
for a particle of mass `m`, speed `v`, passing mass `M` at impact
parameter `b`: perpendicular impulse `Δp⊥ = 2GMm/(bv)`; deflection angle
`θ ≈ Δp⊥/p = Δp⊥/(mv) = 2GM/(bv²)`. The test mass `m` appears in both
the force (∝m) and the momentum being divided into (`p=mv`, also ∝m)
and cancels by plain algebra at the *first* step -- before any
statement about what light is made of is needed. Setting `v=c` gives
`θ=2GM/(bc²)` directly, no limit, no hand-wave. **This is the fixed
"bullshit workaround for a zero doing nothing":** the cancellation was
never delicate work, it was a trivial structural fact about the force
law (`a=GM/r²` is already mass-independent) misrepresented as a special
trick.

**The dominoes this fix knocks forward:**
1. Because `a=GM/r²` never depended on the moving object's mass,
   Newtonian gravity was already quietly equivalence-principle-like,
   over a century before the equivalence principle was named (1907) --
   unnoticed, because the cancellation was treated as a magic trick
   rather than a plain structural fact.
2. But `a=GM/r²` only ever describes a path bending through
   *unchanged, rigid* Newtonian space -- the ontology has no concept of
   space itself being reshaped, so there is nothing in the law for a
   second effect to attach to. Newton/Soldner's half-answer is not
   half-right by bad luck; it is structurally incapable of being more,
   because the framework only has room for one effect.
3. Einstein 1911 reaches the identical number via a wholly different
   argument (equivalence principle / redshift-time-dilation, not
   particle mechanics) -- but is still confined to the same single
   degree of freedom: how time runs differently near mass. Still no
   reshaped space. Same domino, knocked over twice by independent
   routes, landing in the same place for the same reason.
4. Only in 1915, once space is allowed to curve as a genuinely separate
   degree of freedom from time, does the second, equal contribution
   appear, doubling the result to `4GM/(bc²)`, confirmed by Eddington
   1919.
5. **PWC application:** if HDF's compression is modeled as *only* a
   pressure/index gradient kinematically steering a photon (however
   physically motivated), it is mechanically the same shape as
   `a=GM/r²` -- one law, one effect, one half-answer, for the identical
   structural reason, in new vocabulary. The missing piece is not "a
   better steering mechanism" -- it is the medium's own proper-length/
   geometric role, entirely separate from how it steers direction.
6. **Why surface tension is the leading candidate, not just one
   option among several:** interfacial tension inherently supplies two
   distinct geometric roles (tangential steering, normal/curvature
   length-changing) from *one* parameter, rather than one role counted
   once -- the correct shape to escape this trap, traced back to its
   root, not a preference among equals.

**Status: still no computed bending angle.** The missing input remains
an actual HDF tension/anisotropy figure, not yet derived or measured
anywhere in this project.

**The 115-year confirmation chain (2026-09-14; 1911 to 2026 is exactly
115 years):** the fix above lands on 1915's doubled value, but the
real target for any eventual PWC derivation is not that round number --
it is everything the following century did to it. Eddington's 1919
eclipse expedition confirmed the doubled value over the half-value, but
only to ~30% precision. The 1960s-70s parametrized post-Newtonian (PPN)
formalism (Robertson, then Nordtvedt and Will) named the exact quantity
this whole chain circles: `γ`, the ratio of the spatial-curvature
contribution to the time-dilation contribution -- Newton/Soldner and
Einstein 1911 are `γ=0` (half answer), full GR is `γ=1` (full
doubling). 1970s-90s VLBI tracking of quasar deflection pinned `γ` to
~1%. The 2003 Cassini Shapiro-delay experiment measured `γ−1 = (2.1 ±
2.3)×10⁻⁵` -- confirmed to roughly 1 part in 100,000, not merely
"roughly doubled." Since 2015, LIGO/Virgo ringdown observations and the
Event Horizon Telescope's photon-ring imaging (M87*, Sagittarius A*)
extend the same test into the strong-field regime near an actual
horizon. **The real target: not 4GM/(bc²) as a round figure, but `γ=1`
to about five decimal places in the weak field, holding unmodified into
the strong-field regime.** That is the bar any HDF tension/anisotropy
mechanism will eventually need to clear.

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

**Tension and surface-tension mechanism (2026-09-14):** HDF is under
high tension -- expansion pressure pushing out, balanced by something
pushing back. A photon feels no resistance because its speed equals
the rate the medium is parting ahead of it and closing behind it -- it
threads a gap that opens and shuts in step with its own motion.
Separately, HDF is still attracted to heavier knots via a
surface-tension-like effect, the way two water drops on a wet flat
surface pull together through the connecting film.

The frictionless-propagation piece is a clean plain-language restatement
of the existing frictionless-superfluid picture already on record -- it
explains why light loses no energy moving through HDF, but is not
itself a bending mechanism and does not bear on the missing factor of 2.

The surface-tension piece is structurally promising: if HDF's pull
toward a knot is genuinely an interfacial-tension effect rather than an
ordinary isotropic pressure gradient, real established physics
(Young-Laplace capillarity) already splits interfacial tension into two
distinct geometric roles from *one* quantity (the tension itself, `γ`):
a tangential role (resists stretching *along* the surface) and a
normal/curvature role (drives a pressure jump *across* the surface,
`ΔP = γ(1/R1 + 1/R2)`). Two genuinely different effects from one
parameter -- not two mechanisms bolted together. If HDF's attraction is
tension-driven in this sense, the two-roles-from-one-substrate
requirement may be structurally built in automatically.

**Status, honestly:** strongest qualitative lead identified so far, but
not a computed answer. No HDF surface-tension coefficient (an analog of
`γ`) has been established, derived, or measured anywhere in this
project. No Young-Laplace-style pressure-jump profile around a mass
concentration has been computed. A bending angle cannot be produced
from this until such a coefficient exists and is worked through
quantitatively against the `4GM/(b*c0^2)` benchmark.

**Correction (2026-09-14): LDF/HDF are two phases of one substance, not
a frictionless pass-through.** The frictionless-propagation claim above
is REJECTED by the user: light does feel drag. LDF is HDF -- same
weight, same speed -- just a different phase of the one substance, not
a separate thing passing through an inert background; gravity waves are
also HDF. Real grounding identified: liquid water is now understood,
with real experimental support, to have TWO distinct liquid phases -- a
high-density liquid (HDL) and a low-density liquid (LDL) -- separated
by a genuine phase transition, most clearly studied in supercooled
water. This was a long-standing hypothesis (Poole, Sciortino, Stanley
and others, from the early 1990s, the "liquid-liquid critical point"
hypothesis) and received direct experimental support from X-ray
scattering on supercooled water microdroplets (Kim et al., *Science*,
2020). Same molecule, two distinct liquid phases, genuinely different
density and structure -- the physical grounding for HDF/LDF as two
phases of one substance rather than a background-plus-wave picture.

If LDF and HDF are genuinely distinct phases rather than a uniform
medium a wave passes through unchanged, a photon (LDF) interacting with
HDF is a real phase-boundary interaction -- real drag is physically
expected, the same way sound or heat transport differ measurably
between water's two liquid phases. The earlier "no resistance" framing
incorrectly treated LDF and HDF as the same phase encountering itself;
they are not. **Honest caveat:** water's liquid-liquid transition
remains an active, still-debated research area (the hypothesized second
critical point is contested and experimentally hard to reach) --
treated as well-evidenced grounding for a two-phase picture, not as an
exactly-solved system to import numbers from. No HDF/LDF drag
coefficient or phase-boundary condition has been derived anywhere in
this project. This correction concerns real drag/energy exchange during
propagation -- a separate question from the surface-tension anisotropy
lead above; whether that drag is itself directionally asymmetric (and
could also contribute to bending) is a new, not-yet-examined question.

**Shared-c mechanism (2026-09-14):** each individual fundamental unit of
the substrate weighs the same whether currently arranged as HDF or
LDF. The two phases differ purely in volumetric packing density: HDF
packs units tightly (the source of pressure/squeeze/pull toward mass);
LDF spreads them so thin it is "almost massless" in bulk despite being
built from identical individual units. Because both phases are
ultimately the same fundamental stuff, the maximum speed a disturbance
can propagate at is set by that shared per-unit property, not by which
macroscopic-density phase carries it -- hence light (an LDF disturbance)
and gravitational waves (an HDF disturbance) share the same speed
ceiling, `c`.

This is not speculative: GW170817 (2017 binary neutron star merger) was
observed in both gravitational waves (LIGO/Virgo) and a gamma-ray burst
(Fermi/INTEGRAL) arriving within ~1.7 seconds of each other after a
~130-million-light-year journey, constraining the fractional difference
between gravitational-wave speed and light speed to roughly 1 part in
10^15 -- effectively identical. The shared-fundamental-unit picture
supplies an actual physical reason for this near-exact match, rather
than leaving `c_GW = c_light` as an unexplained empirical coincidence.

This also reconciles cleanly with the drag correction above: "almost
massless" in bulk is a genuine qualitative reason LDF's coupling to HDF
is normally weak enough to look frictionless over most of light's
travel (consistent with light crossing cosmological distances with no
measurable exotic dispersion) -- but weak coupling is not zero coupling,
which does not contradict the prior correction that real drag exists.
The residual coupling is exactly where real drag AND the surface-tension
pull toward mass concentrations both plausibly live -- concentrated
where HDF is dense, negligible where it is not.

**Honest caveats:** this is a qualitative, structurally coherent account,
not a derivation. No scaling law has been established anywhere in this
project relating volumetric packing density to propagation-speed cap,
drag magnitude, or the surface-tension coefficient needed for the
still-open bending-angle question above. The GW170817 evidence directly
supports the shared-speed-ceiling claim specifically; it does not by
itself derive drag magnitude or resolve the anisotropy/factor-of-2
question.

**HDF is the more fluid phase (2026-09-14):** confirmed by the actual
water research, and non-obvious -- density and fluidity are separate
axes in the two-liquid-phase picture. The "fragile-to-strong dynamical
crossover" seen in supercooled-water studies (Xu, Kumar, Stanley and
others, mid-2000s onward) associates HDL (the denser phase) with
FASTER, more disordered, more fluid dynamics -- a "fragile" liquid in
the technical sense, relaxing/flowing readily. LDL (the less dense
phase) is the more rigidly structured one -- a tetrahedral, ice-like
hydrogen-bond network that relaxes slowly, behaving like a "strong"
liquid, closer to solid-like character despite being less dense.
Denser is not sluggish here; it is the reverse.

Mapped onto PWC: HDF being the more fluid phase fits it doing the
flowing, squeezing, tension-exerting work around a mass concentration
(tension and flow belong to the same kind of substance -- this
strengthens, rather than sits apart from, the surface-tension mechanism
above). LDF being the more rigid, structurally ordered phase fits
light's fixed, coherent, steady-speed wave propagation, rather than
light being the "loose"/flowing one -- the naive intuition (light=fluid,
mass=rigid) runs backwards from what the real research supports, and
HDF/LDF's roles line up with the correct, non-naive direction.

**Honest caveat:** a real, correctly-directioned qualitative match,
strengthening internal consistency of the two-phase picture -- not a
viscosity value, flow law, or quantitative fluidity ratio, none of
which exist anywhere in this project. Supports, does not yet compute,
the surface-tension bending lead and shared-c/drag entries above.

**LDF generalization (2026-09-14):** LDF is not limited to visible-
spectrum photons -- it is the general category of genuine energy-wave/
radiation phenomena: the full EM spectrum (radio, infrared, visible,
UV, X-ray, gamma) plus neutrinos, all sharing the rigid/structured
(LDL-like) character above. Plasma is explicitly excluded, correctly:
plasma is ionized MATTER -- charged particles, still bound mass
carriers -- not a pure energy-wave. It carries its own collective wave
phenomena (plasma/Langmuir oscillations), but that is a matter-wave in
a charged fluid, categorically different from a photon or a
free-streaming neutrino; plasma stays on the Sintot/matter side of the
ledger.

**Honest caveat:** neutrinos are not exactly massless and do not travel
at exactly `c` -- they carry a small, confirmed nonzero rest mass
(neutrino oscillation experiments, Super-Kamiokande/SNO, 2015 Nobel
Prize), traveling very close to but not exactly at `c`. Consistent with
the user's own earlier framing this session ("99.99% to a neutrino"),
not a contradiction of it.

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

## Bullet Cluster JWST 2026 fact-check (2026-09-14)

**Claim as given:** "JWST 2026 result, MOND 100% accounts for the Bullet
Cluster, dark matter is dead." Web-searched and checked against actual
sources -- **not** a clean "resolved, dark matter dead" result; a real,
live, three-way scientific debate as of mid-2026.

**What is real:** a new JWST-based Bullet Cluster lens model (NIRCam
imaging + NIRSpec spectroscopy, 135 secure multiple images across 27
background galaxies with spectroscopic redshifts -- *Mapping dark
matter in the Bullet Cluster using JWST imaging and spectroscopy*, A&A
2026) produced a materially better stellar-population count and
confirmed significant iron/oxygen abundance, implying more massive-star
remnants (neutron stars, black holes) than previously counted.
Recalculating lensing contributions with this improved remnant
inventory made a MOND (no dark matter) explanation "much more
plausible" without the previously assumed dark matter quantity.

**What is not established:** community response as of mid-2026 splits
three ways -- full MOND (baryons + remnants alone), standard dark
matter reduced by roughly half (not eliminated), or a hybrid. Benoit
Famaey -- a leading pro-MOND researcher, not a skeptic -- published a
paper (arXiv:2605.10022, "On the residual missing mass of the Bullet
Cluster") using this *same* updated JWST lens model and concludes MOND
still leaves a residual missing-mass problem in the Bullet Cluster, of
the same collisionless, galaxy-centered character it leaves in other
clusters generally -- not fully closed even with the improved
remnant-counting.

**Honest verdict:** real, significant update -- the dark-matter
fraction required to fit the Bullet Cluster dropped substantially on
the new JWST data. Not verified: "MOND 100% accounts for it" or "dark
matter is dead." Logged as a genuine partial dent in the dark-matter
case, not a resolution.

Sources: [A&A 2026](https://www.aanda.org/articles/aa/full_html/2026/06/aa59214-26/aa59214-26.html),
[phys.org summary](https://phys.org/news/2026-06-bullet-cluster-reopen-dark-debate.html),
[Famaey, arXiv:2605.10022](https://arxiv.org/abs/2605.10022),
[arXiv:2601.22245](https://arxiv.org/pdf/2601.22245)

**Update -- full text read directly (2026-09-14):** the IGIMF/MOND core
paper above was re-read in full from the local PDF (arXiv:2606.19454v3,
Zhang, Haghi, Asencio, Banik et al., dated 2026-07-06/07), superseding
the earlier summary-only pass. The mechanism is real and non-arbitrary:
Blackwell, Bregman & Snowden (2022) showed the *visible* stellar
populations in cluster galaxies can't account for the metals actually
measured in the intracluster gas, requiring an earlier, now-dead
massive-star population -- leaving far more neutron-star/black-hole
remnant mass than standard IMF accounting credits. IGIMF (developed
independently of any dark-matter question, gauged on globular clusters
and star counts since Kroupa & Weidner 2003) quantifies how much.
Metallicity is a real, independent evidentiary anchor, not a free
parameter tuned to fit lensing.

**Quantitative result:** for the three BCG cores, IGIMF-corrected
baryonic mass (stars + remnants + ICL + gas) as a fraction of the MOND
lensing requirement at 250 kpc: 101-136% (southern), 117-165%
(northern), 120-163% (subclump) -- brackets or *exceeds* the MOND
requirement in most cases.

**Three honest limits, stated by the authors themselves, not imposed
externally:**
1. Scope: three central BCG cores only, not the full cluster's
   weak-lensing offset map (Clowe et al. 2006's original "direct
   empirical proof" claim covers the whole cluster).
2. Against plain GR/ΛCDM (not MOND), the same generous baryonic
   estimate is still only 52-86% of the required lensing mass -- a real
   gap remains; the paper's conclusion is dark matter models must
   "revise their parameters to reduce the required dark matter mass,"
   not eliminate it.
3. Self-flagged unresolved tension: this much extra remnant mass in
   BCGs should push their velocity-dispersion profiles toward
   declining/Keplerian, but observed BCG profiles are flat. Testing
   whether natal kicks spread remnants out enough to avoid this
   conflict is explicitly "beyond the scope of this work" and "remains
   to be explored" -- an open problem in the paper's *own* scenario.

**Additional context:** a companion paper in prep (Cho, Jee, Joo, Cha,
HyeongHan, arXiv:2512.03150) reportedly finds the Bullet Cluster is a
*minor* merger, not the extreme high-velocity major collision the
original ΛCDM-tension claims were built on -- a separate, not-yet-fully-
absorbed crack in the standard picture.

**PWC translation (2026-09-14):** weakly-locked Sintot (X-ray gas,
large surface area) shocks and bogs down on collision; neutron-
degenerate matter (the strongest knot, near-zero cross-section) punches
straight through ballistically; HDF tension gradients track the real
mass concentration (the neutron stars), not the gas -- producing the
observed offset without an invented dark matter species. This is a
legitimate, earned translation, not relabeling: the punch-through logic
is the same physics that makes dark matter collisionless in the
standard picture (negligible collision cross-section, same reason stars
almost never collide during full galaxy mergers), correctly reassigned
to neutron-degenerate matter -- already established here as the
strongest, most radiation-resistant tier-knot. The collision dynamics
(shock heating, gas lag) are real, independent astrophysics (Markevitch
et al. 2002), not invented. It inherits three open dependencies rather
than closing the case: (1) the gravity regime-dependence question above
-- "no MOND math required" presumes HDF tension reproduces a MOND-like
low-acceleration boost, shown permissible, not yet derived; (2) the
three limits already logged for the IGIMF paper (core-only scope,
residual GR-side gap, unresolved BCG velocity-dispersion tension); (3)
the paper's own hedge that neutron-star dominance of the remnant
population (vs. black holes) is plausible, not certain. Real, earned
mechanism translation -- not a closed result.

**Authors' own conclusion language:** "the notion that the Bullet
Cluster provides definitive evidence for dark matter needs to be
questioned... alternative frameworks... offer explanations that
deserve further exploration." Explicitly hedged -- not "falsified," not
"dead." Strongest of the Bullet Cluster results checked in this
project so far, still short of "dead."

## Frontier 2 -- low-acceleration boost (a₀) -- split status (2026-09-14)

Product of an extended, adversarial derivation process: multiple
proposed closures for the galactic-scale prefactor were checked by
independent hand calculation in this session and rejected when they
did not survive verification. The surviving result below is real
specifically because it was independently reproduced three separate
ways using standard, checkable physics, not because it was asserted
persuasively.

**Cosmic acceleration scale -- NOT DERIVED, IMPOSED SCALAR-MATCHING
ASSUMPTION** (downgraded a second, deeper time, 2026-09-14): every
version of this calculation attempted in this session (SHM scaling,
Unruh=GH temperature matching, Stefan-Boltzmann pressure matching,
ideal-gas pressure matching) shares the same underlying structural
flaw -- each sets two *scalar* reference quantities equal (a local
temperature/pressure value vs a global one) and treats that equality
as if it generates a force. That is not how fluids produce
acceleration: force comes from a pressure *gradient*, integrated over
a surface (`f=-∇P`, `F=-∮P·n̂dA`), not from an equality condition
between two separately-computed scalars. `a_cosmic=c₀H₀` was never
actually a force calculation -- it was an equality condition dressed
as one. This is a deeper correction than the earlier "conditional
model result" framing: even the cosmic-scale number rests on an
imposed matching assumption with no demonstrated connection to an
actual force-generating mechanism. Retained below purely as the
arithmetic record of what each attempted equality condition produces,
not as a derived physical result.

The three numerically-convergent routes, all built on the same
now-rejected scalar-matching structure:
1. Simple harmonic restoring acceleration `a=ω₀²R_cosmic` with
   `ω₀=H₀`, `R_cosmic=c₀/H₀`.
2. Unruh local wake temperature (`T=ħa/(2πk_Bc₀)`) equated to
   Gibbons-Hawking de Sitter horizon temperature (`T=ħH₀/(2πk_B)`) --
   the `2π` cancels identically between the two, leaving `a₀=c₀H₀`
   exactly.
3. Stefan-Boltzmann radiation pressure equality (`P=u(T)/3`, isotropic
   both sides) between the local Unruh wake and the global adiabatic
   background -- independently re-derived here, confirmed to give the
   same `a₀=c₀H₀`, no free parameter.

**Refinement:** treating Unruh temperature (an accelerating detector's
perception of vacuum) and Gibbons-Hawking temperature (a cosmological
horizon's associated temperature) as two sides of one real, locally-
equilibrating radiation-fluid pressure that can be set in direct
contact is an *extra model assumption*, not something standard QFT/
thermodynamics hands over for free just because both formulas share
the same `ħκ/(2πk_B)` form. Routes 2 and 3 above therefore share this
same underlying assumption and are not as mutually independent as
first logged. `a_cosmic=c₀H₀` remains the correctly-computed algebraic
consequence of that stated model, real and checkable, but conditional
on this assumption rather than an unconditional derivation from
standard thermodynamics alone.

**Hemispheric projection -- DERIVED STANDARD RADIATIVE-TRANSFER
RESULT:** `P_hemi = u/6` (one-sided isotropic hemispheric radiation on
a surface: `P=(u/4π)∫_hemisphere cos²θ dΩ = u/6`). Correct on its own.
**Does not imply `a=c₀H₀/6`** -- confirmed by direct calculation below.

**Pressure matching with the hemispheric correction -- ALGEBRAIC
CONSEQUENCE OF THE STATED MODEL:** `u(T_Unruh)/6 = u(T_GH)/3` gives
`a = 2^(1/4)·c₀H₀ ≈ 8.1×10⁻¹⁰ m/s²` -- *further* from the `1.2×10⁻¹⁰`
target, not closer. The hemispheric coefficient shifts the derived
scale upward; it cannot produce the MOND-like `c₀H₀/(2π)` suppression.
Confirms directly: using `u/6` to naively divide `c₀H₀` by 6 is the
wrong operation; the correct pressure-level substitution yields
`2^(1/4)·c₀H₀`, not the galactic `a₀`.

**Galactic acceleration scale -- OPEN DERIVATION / EMPIRICAL
CORRESPONDENCE:** empirical target `1.20×10⁻¹⁰ m/s²`. The ratio
`a_cosmic/a₀ ~ 5.7` sits close to `2π` (`c₀H₀/2π ~ 1.08×10⁻¹⁰`, ~10%
agreement) -- a known, real coincidence Milgrom himself noted decades
ago, not something derived here first. Four attempted mechanistic
derivations of this specific projection factor were checked in this
session and each failed independent verification:
- (a) an unexplained dimensional-analysis combination `c₀ν₀` that does
  not match the standard SHM acceleration formula (which instead gives
  `c₀H₀`, no `2π`);
- (b) a closed-cavity eigenmode/impedance-matching argument with no
  worked calculation shown;
- (c) an Unruh-adiabatic-floor argument that, worked correctly with
  the real Gibbons-Hawking formula, also gives `c₀H₀`, no `2π`;
- (d) a Stefan-Boltzmann hemispheric-vs-isotropic radiation pressure
  argument (`P_hemisphere=u/6`, itself a correctly verified textbook
  radiative-transfer result) that, properly substituted into the
  actual temperature-matching equation rather than applied as a
  post-hoc divisor on the final answer, gives `a₀=2^(1/4)·c₀H₀`
  (`~8.1×10⁻¹⁰`, *further* from the target) -- because temperature
  enters the Stefan-Boltzmann relation to the 4th power, a factor-of-6
  pressure correction only produces a `6^(1/4)~1.57×` change in the
  resulting acceleration, not `6×`.

The exact field-theoretic derivation of the `1/(2π)` (or any other)
geometric projection factor from HDF's own wake dynamics remains
genuinely open. No derivation attempted in this session produces the
real, approximately `1/(2π)` suppression from pressure geometry or
standard Unruh/Gibbons-Hawking thermodynamics. This is the jointly-
confirmed, converged status after an extended adversarial derivation
process -- both parties independently arrived at the same conclusion
via separate calculations.

**What a real derivation actually requires (2026-09-14), replacing
"find the right prefactor" as the framing entirely:**

| Required element | Form | Status |
|---|---|---|
| Local equation of state | `P=P(ρ,T,s)` | Not yet specified -- determines whether the wake is classical, radiation-like, barotropic, or something else |
| Adiabatic closure | `Pρ⁻ᵞ=const`, if applicable | Not yet specified -- relates local compression/rarefaction to temperature and pressure |
| Wake solution | `δρ(x), δT(x), δP(x)` | Not yet solved -- an actual SOLVED anisotropic wake profile, not an assumed hemisphere |
| Geometry/boundary condition | Surface, trailing cone, cavity wall, or mode distribution | Not yet specified -- determines the angular factor as an OUTPUT, not an input |
| Force coupling | `F=-∮_∂V P(x)n̂dA` | Not yet carried out -- converts the actual pressure distribution into a real acceleration |
| Cosmological coupling | How `H₀` actually sets `P_background(x)` or a gradient | Not yet specified -- not merely a background temperature asserted by analogy |

**Status summary:** neither `a₀=c₀H₀` nor any hemispheric variant
(`c₀H₀/6`, `2^(1/4)c₀H₀`, `2c₀H₀`) is derived. All rest on an imposed
scalar-matching assumption that was never physically justified as a
force-generating mechanism. A real derivation requires solving the six
elements above, not finding the right prefactor to apply to a scalar
equality.

**Deep-MOND-limit interpolation -- EMPIRICAL PHENOMENOLOGICAL LAW:**
`g_obs=√(a₀·g_bar)` is a real target formula, supported by SPARC-132
Tier A data, but not derived from the wake mechanism. The proposed
physical picture (entropic wake pressure asymmetry breaking
d'Alembert's symmetry -- itself a real, legitimate classical-fluids
starting point) has no worked calculation connecting it specifically
to the square-root/geometric-mean form, as opposed to any other
interpolating shape. The complete non-linear transition function
(continuum stress-tensor closure) remains an open derivation.

## JWST early-galaxy LCDM tension fact-check (2026-09-14)

**Claim as given:** Labbé et al. (Nature, Feb 2023), Boylan-Kolchin
(Nature Astronomy 2023), and Glazebrook et al. ZF-UDS-7329 (Nature,
Feb 2024) together mean ΛCDM is falsified. Web-searched against
primary sources -- real papers, real initial tension, but the current
(2026) state splits into two threads with two different outcomes, more
nuanced than "falsified."

**Thread 1 (Labbé, walked back):** six candidate massive galaxies
(z=7.4-9.1, implied stellar mass >10¹⁰ M☉) seemed too massive too
early. Boylan-Kolchin showed that *if* the photometric mass estimates
held, some sat at or beyond ΛCDM's star-formation-efficiency limit for
that epoch -- a genuine flag at the time. A direct spectroscopic
follow-up, *"Confirmation of the standard cosmological model from red
massive galaxies ~600 Myr after the Big Bang"* (arXiv:2304.11911),
found several original candidates sit at *lower* redshift than the
photometric estimate implied -- largely dissolving the tension for
those objects. Substantially walked back toward the standard model,
not confirmed against it.

**Thread 2 (ZF-UDS-7329, still live):** spectroscopically confirmed
(not photometry-only) -- a ~10¹¹ M☉ quiescent galaxy at z≈3.2 that
appears to have formed most of its stars in a fast 200-400 Myr burst
within the universe's first billion years, already quiescent by
observation. A real, still-standing challenge to ΛCDM halo assembly/
quenching timescales. Follow-up work (Carnall et al. 2024, Turner et
al. 2024) shows the tension can be substantially mitigated depending on
star-formation-history priors and whether a major-merger channel is
allowed -- reduced, not eliminated, not confirmed away either.

**Honest verdict:** not "ΛCDM falsified." One thread was significantly
walked back by better data in the standard model's favor; the other is
real and still an open, active tension as of 2026, with plausible but
unsettled mitigations. A genuine open question, not a resolved
falsification -- same discipline as the Bullet Cluster entry above.

Sources: [Boylan-Kolchin, arXiv:2208.01611](https://arxiv.org/abs/2208.01611),
[arXiv:2304.11911](https://arxiv.org/pdf/2304.11911),
[ZF-UDS-7329 (A&A)](https://www.aanda.org/articles/aa/full_html/2025/02/aa52781-24/aa52781-24.html),
[Age-dating early quiescent galaxies (MNRAS)](https://academic.oup.com/mnras/article/537/2/1826/7973012)

## Sonic-choke Hawking derivation -- VERIFIED (2026-09-14)

**Correction of an earlier rejection this session:** a Hawking-radiation
derivation was rejected earlier tonight as a relabeling of standard GR
surface gravity (`κ=GM/R_s²` plugged directly from `R_s`, no
independent HDF input) -- correct for that specific presentation. But a
real, pre-existing, more sophisticated derivation exists in this
project's own files (`Downloads/claude chat.txt` §II G, cross-
referenced in `unified_framework_consolidated_2026-08-13.md`), found
only after being told to search for it -- same mistake pattern as the
earlier SPARC-132/dwarf-41 error this session: should have checked
project files before ruling.

**The real derivation, independently re-verified in this session, not
taken on either document's word:**
1. Free-fall inflow speed: `v(r) = √(2GM/r) = c√(r_s/r)` -- standard
   mechanics, energy conservation for infall under inverse-square
   gravity.
2. Sonic condition: inflow reaches the medium's own characteristic
   speed (`c_s = c`, the shared-c postulate already established
   elsewhere in this framework) exactly at `r = r_s = 2GM/c²`.
3. Run through the real, general analog-gravity method (Unruh 1981 --
   the same formalism underlying the actual BEC and water-tank
   white-hole experiments, *not* GR's own Hawking derivation): surface
   gravity from the flow profile at the sonic point,
   `κ = (1/2)|d(c_s²−v²)/dr|` at `r=r_s`. Independently computed here:
   `κ = c²/(2r_s) = c⁴/(4GM)` -- exactly the real value.
4. `T = ħκ/(2πk_Bc) = ħc³/(8πGMk_B)` -- the real Hawking formula,
   exactly.

**Numerical verification:** the source gives `T_sonic = 6.1686778×10⁻⁸ K`
for a 1-solar-mass object, ratio 1.000000000000 against `T_Hawking`,
checked across Planck mass, 1 M☉, Sgr A* (4.3×10⁶ M☉), and M87*
(6.5×10⁹ M☉) -- eighteen orders of magnitude in mass, zero free
parameters. Independently cross-checked here against the known real
value for a solar-mass black hole (~60 nanokelvin) -- consistent.

**Why this is different from the rejected version:** that version
plugged `R_s` directly into `GM/r²` -- purely circular, no independent
physics. This version runs an actual flow profile through the actual
general method used in real, independent, peer-reviewed analog-gravity
physics. That this specific combination reproduces Hawking's formula
exactly, over eighteen orders of magnitude, is not guaranteed by the
method itself -- a genuine, non-trivial result.

**Honest remaining caveat, a separate open item, not a discount on
this result:** `v=√(2GM/r)` is standard inverse-square-gravity
mechanics -- it assumes ordinary `1/r²` gravity rather than
independently deriving it from HDF's own equation of state (same open
item already on record: PWC's gravity law is a required match, not
yet derived from a medium functional). The genuinely new, PWC-specific
ingredient doing the real work is `c_s=c`, combined with ordinary
mechanics, run through a real independent method, to get an exact
match -- a legitimate, largely non-circular result built on one real
postulate, not zero, though not yet built from a fully independent HDF
equation of state either.

**Also resolves, consistently, from the same source:** no `r=0`
singularity (density floor `ρ₀>0` and ceiling `ρ_max<∞` bound both
extremes), and the finite-redshift-boundary/emitting-surface objection
(self-flagged in the source) -- resolved because inflow exceeds the
medium's own signal speed at the boundary, making it "optically black
by kinematics, not by geometry," independently matching the answer
already given earlier tonight to "does PWC's black hole have flow."

**Status:** strongest single verified result in this project to date,
per the source's own characterization and this session's independent
re-derivation.

## Quantization / vacuum-cutoff unification (2026-09-14)

**Correction of an earlier claim this session:** an earlier entry
claimed mainstream QFT already explains `E=hf` cleanly via canonical
quantization, independent of any medium, undercutting the case for
HDF. That claim was too generous to the standard picture.

**The real technical point:** a single isolated field oscillator's
energy levels, `E=(n+1/2)hf`, are well-defined regardless of medium --
that part genuinely doesn't need a substrate. But getting an actual
*finite* total (a real vacuum energy density/cosmological-constant
prediction) requires summing `hf/2` over every mode of the field, and
in truly unbounded, structureless empty space there is no natural
scale to stop that sum at. The standard technique -- impose a finite
box to get countable modes, take the box to infinity, or equivalently
impose an energy cutoff (commonly the Planck scale) by hand -- is not
a natural, physically motivated regularization. It is arbitrary, and
it is exactly where the ~10¹²⁰-order vacuum energy discrepancy (see
Bullet Cluster/dark-energy section above) comes from: no natural
stopping point, so the "answer" depends entirely on where the sum is
artificially cut off.

**Why a real medium is structurally different:** HDF would supply a
natural, non-arbitrary cutoff -- its own physical grain or resonant
scale -- rather than an imposed one. This ties `E=hf`'s quantization
requirement to the same root cause as the vacuum catastrophe: an
abstract geometric zero has no scale of its own to pixelate with, so
any attempt (single-photon quantization or vacuum-energy summation)
either diverges or needs an arbitrary, unmotivated cutoff.

**Honest status:** the structural argument is sound -- a real medium
naturally resolves the cutoff-arbitrariness problem an abstract void
cannot. This is not yet a derivation: PWC has not derived what HDF's
actual cutoff/grain scale *is* anywhere in this project. Same
open-number category as the lensing tension coefficient and the
low-acceleration gravity boost -- the shape of the fix is right, the
number is still missing.

**Also refines** (not retracts) the earlier "pixels" framing: Planck's
quantum `hf` is not a fixed minimum size -- a real medium's phonon-
style fixed lattice grain would predict a hard maximum frequency
(a Debye-style cutoff), which doesn't match reality (no upper limit on
real photon frequency exists). The quantum scales *with* frequency.
Any HDF grain-based account of `E=hf` needs to reproduce a
frequency-*dependent* grain, not a fixed one -- more specific, and
currently undelivered.

## Neutron/knot entropy capstone (2026-09-14)

"Neutrons decay in the open, still the strongest knot, entropy's a
bitch, deal with it." Not a contradiction -- the same entropy-asymmetry
rule already logged under Mass baseline, demonstrated at the particle
level. A free neutron sits in the high-entropy, spontaneous-decay
direction with no cost and no special condition required: it decays
via `n -> p + e- + antineutrino` with a mean lifetime of ~879 seconds
(~15 minutes), a precisely measured fact. Packed into sufficient
density with degeneracy pressure (Pauli blocking suppressing the
reverse reaction) and gravitational confinement holding the bulk state
together, that same particle becomes part of the most tightly bound,
radiation-resistant configuration in this framework -- more resistant
than even iron-56, the peak of the nuclear binding curve. Nothing about
the neutron itself changes between these two cases; only whether the
surrounding conditions have paid the entropy cost of confinement
determines whether it is the weakest or the strongest thing in the
framework. Capstone synthesis of three already-logged points (free
neutron lifetime, neutron-degenerate matter as the strongest tier-knot,
and the general locking/unlocking entropy-asymmetry rule) -- no new
numerical claim.

## Excluded substitutions (explicitly rejected, so they cannot re-enter quietly)

| Substitution | Status |
|---|---|
| Finite HDF core means a rigid reflective surface | Rejected -- finite continuous gradient/trapping is not a mirror |
| HDF maximum density equals neutron-core nuclear density | Rejected -- distinct regimes; this exact error was made and corrected in this session |
| All compact-object density is uniform at rho_HDF,max | Rejected -- PWC specifies a finite high-density centre and descending envelope |
| Local gas pull fraction g_gas/g_bar equals accessible HDF volume | Rejected -- tested directly as Domain R; q_ext converged to 0 |
| A frozen mass-only merger release coefficient is the PWC merger law | Rejected -- failed a held-out test (GW190412) |
| PWC requires an empty exterior, singularity, dark-halo particle, or another universe | Rejected -- contradicts the finite-medium ledger |
| GR's r=0 collapse endpoint is a real, physical infinite-density point | Rejected -- mainstream physics already treats this as a signal classical GR breaks down there (the motivation for quantum gravity), not a confirmed prediction; consistent with PWC's own no-physical-infinity premise |
| Dark matter is a real, invisible particle species | Rejected as a substance -- but the phenomena it explained remain real and NOT discharged by the rejection: (1) flat rotation curves -- Tier A traction exists (132-galaxy SPARC fit); (2) Bullet Cluster lensing offset from visible gas -- not addressed anywhere in this project, and per a 2026-09-14 web-sourced check (below), the observational picture itself is a live, unresolved three-way debate, not a closed case either direction; (3) CMB acoustic peak heights needing a specific matter/baryon ratio -- not addressed anywhere in this project. Rejection transfers the burden to HDF mechanics, it does not discharge it -- three obligations remain open, one of them (Bullet Cluster) now genuinely narrower on the mainstream side too |
| The cosmological constant / dark energy is literal vacuum energy generated from empty space | Rejected as a mechanism -- but the observation it explained (accelerating cosmic expansion, Type Ia supernovae, Perlmutter/Riess/Schmidt 1998) remains real and is not addressed anywhere in this project; fully open |
| The FLRW scale factor `a(t)` reaching `a=0` at the Big Bang is a real, physical zero-volume singular starting point | Rejected -- same category as GR's `r=0` collapse endpoint above: a classical-theory extrapolation to a point the theory itself doesn't understand, not a confirmed physical state. Does NOT extend to the Friedmann equations' evolution of `a(t)` generally, which are explicitly sourced by real measured energy density/pressure -- structurally the same as mass sourcing the Schwarzschild metric, not empty geometry doing unsourced work. The valid target is the singular endpoint only |
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

### Domain W (shock-freeze/multiphase-pressure-balance outer BC, full SPARC run) -- 2026-09-14

- **model_version**: `domain_W_shock_freeze_bvp.py`
- **Proposal:** replace Domain V's arbitrary-r_far derivative-matching outer
  condition with a physically motivated one: `R_freeze`, a multiphase
  pressure-equilibrium/shock-freeze radius where hot, buoyant baryonic gas
  meets the ambient HDF pressure ceiling and precipitates into cold, dense
  clumps -- real physical grounding matching the established multiphase ISM
  model (Field 1965; McKee & Ostriker 1977).
- **Interpretive choices made explicit** (spec under-determined in three
  places, none silently assumed): (1) `R_freeze` proxied as each galaxy's own
  last measured HI radius (no real gas-pressure/temperature profile exists in
  the loaded SPARC data to compute it from first principles); (2) `u`
  redefined as `rho_HDF_local/rho_HDF_max` (not `rho_excess/rho_gal`),
  removing `rho_gal` as a free parameter -- `c_s0` is the only free global
  parameter; (3) of the two given outer conditions (a value and a derivative
  constraint), only the value condition is used as an independent equation --
  the derivative condition was verified redundant with it for the same SIS
  profile, confirmed algebraically, not a third independent equation for a
  2-state system.
- **Equations:**
  ```
  du/dr     = -(rho_bg+rho_HDF_max*u)*G*(M_bar(r)+M_HDF)/r^2*(1-u) / (rho_HDF_max*c_s0^2)
  dM_HDF/dr = 4*pi*r^2*rho_HDF_max*u
  ```
- **Boundary conditions:** inner `M_HDF(r_min)=(4/3)*pi*r_min^3*rho_HDF_max*u(r_min)`;
  outer `u(R_freeze) = c_s0^2/(2*pi*G*rho_HDF_max*R_freeze^2)`.
- **Run: full 104/45 train/holdout split, all 149 usable galaxies, same rng
  seed 7 as every other domain.**
- **Result: NEGATIVE, clean.** 0 of 144 attempted galaxies converged (0/99
  train, 0/42 holdout) -- not one physical solution found anywhere in the
  tested parameter range. The single-galaxy sanity check failed at four
  different `c_s0` values before the full run was even attempted. The
  reported "fit" (`c_s0=9.99e5 m/s`, implying an absurd ~1413 km/s flat
  velocity) is not a real fit -- every `solve_bvp` call failed uniformly
  across the entire search range, so the scalar optimizer searched a flat,
  uninformative penalty surface and landed arbitrarily.
- **Diagnosis:** pinning `u` to an exact Dirichlet value at `R_freeze`
  (stricter than Domain V's derivative-matching condition) forces the solver
  to find a trajectory from the inner boundary landing on one exact
  prescribed value at the outer edge, for every galaxy's specific real
  baryon profile. scipy's Newton-based BVP collocation solver fails to find
  any such path for any tested galaxy or `c_s0` -- not converging to a wrong
  answer, simply not converging.
- **Status:** Domain V's branch-degeneracy problem is NOT closed by this
  proposal -- replaced by a stricter formulation that fails to converge at
  all. The physical grounding (multiphase pressure balance) remains
  legitimate; this specific mathematical implementation of it does not work
  as specified.

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
| Domain W (BVP, shock-freeze outer BC) | nan (0/99) | nan (0/42) | full run attempted, 0 of 144 galaxies converged |
| "Domain T" pasted claim (source script not in this repo) | 0.1344 | 0.1368 | **not independently reproduced** -- no runnable script for this specific claim has been provided or located on disk |

## What this manifest does NOT contain (explicit gaps, not silently omitted)

- No git commit hash exists anywhere in this project tree.
- No completed per-galaxy convergence table exists for Domain U2 or Domain V.
- No raw radial-output archive exists for Domain T, U, U2, or V (only Domain S has `domain_S_audit_profiles.json`).
- The pasted "Domain T" result (RMS 0.1344/0.1368, alpha_rho=-1.986, BTFR=3.92) has no corresponding script, results JSON, or per-galaxy table on this disk -- it cannot currently be checksummed, re-run, or independently verified against this manifest's data/split/cuts.
