# Prediction frozen before scoring — PROBES with HI gas added (Jaden, 2026-09-25)

Subset: 331 PROBES galaxies matched to ALFALFA a.100 (Haynes+2018, J/ApJ/861/49): optical counterpart within 30",
|Vhel - cz| < 300 km/s, HI code 1. Match file sparc/probes/alfalfa_match.csv (median sep 1.6", median dV 0).
Gas: M_HI = 2.356e5 * D_PROBES^2 * S_HI; M_gas = 1.33 M_HI (helium, as SPARC).
R_HI from HI mass-size relation (Wang+2016): log D_HI[kpc] = 0.506 log M_HI - 3.293, R_HI = D_HI/2.
Profile: exponential gas disc, scale length Rg = the root of Sigma_HI(R_HI) = 1 Msun/pc^2 with Rg < R_HI/2.
Gas rings added to the W1 star rings (M/L 0.5); g_bar AND shared recomputed from stars+gas. locked = 0.
Constants locked from SPARC: s = 0.2264, a0 = 6.6776e-11; base 7.5586e-11; McGaugh 1.1603e-10.

Predictions (M/L 0.5, gas included, galaxy-balanced mean over the 331):
1. PWC beats McGaugh.
2. PWC beats base.
Also reported (not predicted): same 331 without gas; gas + M/L 0.6.
Wording rule: a pass means "survived", not "proven".

## Outcome — both predictions SURVIVED
Gas, M/L 0.5 (predicted): PWC 0.2452 | base 0.2490 | McGaugh 0.2511. vs McGaugh -2.3% (95% [-0.0084,-0.0033]), wins 207/331; vs base -1.5% (95% [-0.0044,-0.0031]), wins 242/331.
Same 331 without gas: vs McGaugh -1.8%, vs base -1.5%. Adding gas did not erode the lead; it grew vs McGaugh. Gas adds outer mass, median shared 0.36 -> 0.39.
Gas + M/L 0.6 (reported): PWC 0.2426 vs McGaugh 0.2427 -- tie (95% [-0.0028,+0.0028]); still beats base -1.1% (95% excludes 0).
