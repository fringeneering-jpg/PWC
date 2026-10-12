# The sensitivity calculation: can the published PR4 map-space analysis constrain
# the 0.15-deg void template? (2026-10-12)
import math

print("== the published numbers (Douglas Scott, arXiv:2502.07654, Planck PR4 map-space) ==")
print("beta = 0.46 deg +/- 0.04 (stat) +/- 0.28 (syst); no evidence of a dipole")
print("-> the 0.04-deg statistical error is the GLOBAL mean over the whole peak stack\n")

print("== the sensitivity scaling ==")
# the template's corridor: RA 142-150, Dec +31-46 -> ~8 x 15 deg ~ 2.4% of the sky
# (with taper) -> call the effective template fraction f_template
f_template = 0.03        # the high-weight corridor's solid-angle share of the sky
sigma_global = 0.04      # deg, the published global statistical error
# per-region noise scales as sqrt(N_global / N_region) = sqrt(1 / f_template)
sigma_template = sigma_global * math.sqrt(1.0/f_template)
A_pred = 0.15            # deg, the frozen template amplitude
snr = A_pred / sigma_template
print(f"template sky fraction (corridor)      : {f_template:.2f}")
print(f"per-template noise  = 0.04 x sqrt(1/f): {sigma_template:.2f} deg")
print(f"predicted amplitude A               : {A_pred:.2f} deg")
print(f"signal-to-noise in the existing data: {snr:.2f}")
print()
print("== the verdict ==")
if snr < 1.0:
    print(f"SNR {snr:.2f} < 1: the published reconstruction CANNOT yet constrain the template -")
    print("the prediction sits below the existing sensitivity. The null has shelter.")
elif snr < 3.0:
    print(f"SNR {snr:.2f}: the prediction sits AT the existing sensitivity's edge - marginal,")
    print("neither a detection nor an exclusion is possible with the published map alone.")
else:
    print(f"SNR {snr:.2f}: the existing data would already exclude or detect - decisive.")
print("\nrefinements that change the number: the exact template sky fraction (the corridor")
print("vs the full void-weight map), the published map's per-pixel noise at 1-10 deg scales")
print("(the 0.04 deg is global; per-region errors may differ), and the systematic 0.28 deg")
print("(irrelevant for the DIRECTIONAL test - systematics are isotropic). The honest")
print("statement: the sensitivity margin is of order unity - the trap's shelter is ~1 sigma,")
print("and the next-generation instruments close it.")
