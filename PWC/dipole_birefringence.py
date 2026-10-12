# The two remaining redshift-set items: the "we rotate" dipole check and the
# birefringence-redshift link (2026-10-12)
import math

print("== 1. The 'we rotate' dipole check ==")
# the framework's reading: the measured polarization angle is turned by our rotation
# relative to the static medium. A rigid rotation turns EVERY direction equally.
print("a rigid rotation relative to a static medium rotates every polarization angle by")
print("the SAME amount -> the sky signature is a MONOPOLE (a uniform angular offset),")
print("NOT a dipole. The registry's flag ('a rigid rotation gives a zero-mean dipole')")
print("resolves: the effect is a uniform offset, invisible against a global calibration.")
print("what IS observable: the offset DRIFTS as we rotate.")
rot = 1.4e-20          # rad/s, the repo's rotation rate (0.0059 H0)
drift_per_yr = rot*365.25*86400
print(f"secular drift = {drift_per_yr:.2e} rad/yr = {drift_per_yr*180/math.pi*3600*1000:.3f} mas/yr")
print(f"over a decade: {10*drift_per_yr*180/math.pi*3600*1000:.3f} mas  - far below current")
print(f"polarization precision (~100 mas). Verdict: the 'we rotate' effect is currently")
print(f"unobservable; it predicts a secular monopole drift, not a sky dipole. The repo's")
print(f"uniform-beta treatment is the monopole reading, consistent.")

print("\n== 2. The birefringence-redshift link ==")
print("the registry's own note stands: birefringence changes POLARIZATION PHASE, not energy.")
print("-> it does not contribute to redshift. The LINK is a shared path integral:")
print("   z        = the density ratio along the path (the wavelength's work)")
print("   beta     = the accumulated phase between the two polarizations along the SAME path")
print("   the anisotropy that drives beta is the cooler medium's own structure; the")
print("   framework's sign (locked, Bootes): beta anti-correlates with matter density")
print("   -> the frozen form: d(beta)/d(ln rho) < 0, i.e. beta accumulates preferentially")
print("   in LOW-density regions (voids), while z integrates the density itself.")
print("the test: the CMB's beta = 0.35 deg (+/-0.14) should map to the void-weighted")
print("path, not the wall-weighted one - the same 'voids maximal' signature already")
print("frozen in the Bootes check. The link is directional, not energetic: phase vs energy,")
print("same path, opposite density weighting.")
