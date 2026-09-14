# Cartesian 1D counter-propagating HDF packet collision: negative result (closed)

## Statement (verbatim scope, as specified)

In the current 1D periodic effective-HDF/medium closure, genuinely separated
Gaussian-envelope counter-propagating packets show R_focus <= 1 for every
tested k_wave in {0, 0.25, 0.5, 1, 2} and sigma in {3, 6, 12}. The earlier
apparent focusing at sigma=12 (R_focus=5.86, in the first geometry sweep)
was an initial-overlap artifact caused by a fixed box (separation not
scaled with sigma) and is rejected -- confirmed by recomputing with genuine
separation enforced (D=8*sigma, giving overlap=exp(-16)~=1.1e-7 for every
case) in `geometry_sweep_v2.py` / `knot_audit/geometry_sweep_v2.json`.

## What this result IS

A negative result for the tested Cartesian-1D packet construction only:
simple counter-propagating Gaussian*cos wave packets, colliding head-on in
a 1D periodic domain, do not constructively concentrate local peak energy
density at the point of collision, for any tested carrier wavenumber or
envelope width. If anything, most configurations show mild-to-strong
defocusing (R_focus as low as 0.05-0.4 in several cases).

## What this result is NOT

Not a conclusion about PWC as a whole, not a statement about whether a
real baseline medium exists, and not a statement about whether converging
HDF energy can form a pressure-locked state in general. The tested setup
has no transverse geometric convergence -- two 1D plane-like packets
overlap and interfere, but they do not represent an inward 3D HDF energy
configuration with decreasing wavefront area (the geometric focusing a
real imploding spherical shell would have). This is why the investigation
moves to a spherically-symmetric radial solver next (see
`dynamic_knot_radial.py`), not to further Cartesian pulse-shape hunting.

## Supporting files
- `phase_geometry_audit.py` / `knot_audit/phase_geometry_audit.json` --
  8-phase sweep at fixed k_wave=2, sigma=3, all showing R_focus<1.
- `geometry_sweep_audit.py` -- FIRST geometry sweep, fixed box (XL=21,
  XR=39), invalidated by t=0 overlap at sigma=6/12 (kept for transparency,
  NOT to be read as a result).
- `geometry_sweep_v2.py` / `knot_audit/geometry_sweep_v2.json` -- the
  corrected sweep with separation scaled as D=8*sigma, resolution scaled
  to dx<=sigma/30, genuine overlap=1.1e-7 confirmed for every case. This
  is the authoritative version of the Cartesian result.

## Chain of self-corrections that led here (for transparency)
1. First existence draft (`dynamic_knot_HDF.py`/`HDF2.py`): phi
   algebraically slaved to instantaneous local energy, active in P and
   Korteweg stress -- rejected as not a passive label; could manufacture
   energy.
2. Real wave field (A,Pi) built (`dynamic_knot_HDF2.py`): found and fixed
   a genuine discrete energy-conservation bug (30-70% drift) via an
   instantaneous per-RHS budget audit -- root cause was diagnosing total
   energy from (rho,u,A) after evolving only (rho,rho*u), rather than
   evolving E_medium as its own conserved flux quantity
   (`dynamic_knot_HDF3.py`, fixed, verified to 1e-4-1e-5 drift, no
   artificial viscosity).
3. MUSCL-HLLC flux with Rusanov fallback built (`dynamic_knot_HDF4.py`)
   to address slow-converging numerical dissipation contaminating the
   local e_avail diagnostic; confirmed HLLC works (no fallback triggered,
   conservation intact) but showed the same evolved-vs-diagnosed gap size
   as Rusanov, revealing the gap is not primarily a flux-scheme artifact.
4. First geometry/calibration attempt used "global max e_avail over the
   whole run" to set pulse amplitude -- caught as measuring each packet's
   own standalone peak (near t=0) rather than the actual collision, since
   geometrically the packets meet around t~4.7-6.3 while the reported
   peak occurred at t~0.3-0.6.
5. First corrected geometry sweep (fixed box, sigma up to 12) appeared to
   show strong focusing (R_focus=5.86) -- caught as an artifact of
   insufficient packet separation at wide sigma in a fixed box (overlap
   check via exp(-(D/2/sigma)^2) showed 57% overlap at sigma=12).
6. Final corrected sweep (separation scaled with sigma) gives the
   authoritative negative result above.
