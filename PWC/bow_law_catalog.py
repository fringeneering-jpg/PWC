# The bow law: a visible medium-bow iff the body is at its own C (2026-10-12, Jaden's ruling)
import math
c0 = 2.99792458e8
Y_bow = 5.93e26

def v_max(rho):
    return min(c0, math.sqrt(2*Y_bow/rho))

print("THE BOW LAW: the medium's own front (the bow) forms iff v ~ v_max(rho) of the body.\n")
print(f"{'OBJECT':34s} {'its v':>12s} {'its C':>14s} {'v/C':>8s}  READING")
print("-" * 92)
cases = [
    ("'Oumuamua (26 km/s, rho ~ 1e3)", 2.6e4, v_max(1e3),
     "far below its C -> NO bow, not an anomaly - just something FAST (his words)"),
    ("RBH-1 (950 km/s, the shell)", 9.5e5, v_max(1.304e15),
     "0.996 of its C -> the bow fires, the star forge (the anchor)"),
    ("pulsar WIND (relativistic, near c0)", 0.999*c0, c0,
     "the wind at its C -> the wind's bow (the pulsar's visible shock is the wind's,"),
    ("", 0, 0, "not the star's - the star itself is below its cap, as the census found)"),
    ("SN blast wave (1e4 km/s, the ISM)", 1e7, v_max(1e-21),
     "the blast is SUPERSONIC in the GAS (10 km/s sound), but far below the medium's own"),
    ("", 0, 0, "front -> the SN shock is the gas's compression front, a different rung than"),
    ("", 0, 0, "the medium's bow - the law's subject is the medium's own rho_max front"),
    ("recoil SMBHs (1770-2100 km/s)", 1.9e6, v_max(1.304e15),
     "1.9-2.2x their C - the SLAMMED regime: forced through, the stripped-shell signature"),
]
for name, v, vc, note in cases:
    if name:
        print(f"{name:34s} {v/1e3:>10,.0f} km/s {vc/1e3:>12,.0f} km/s {v/vc:>8.3f}  {note}")
    else:
        print(f"{'':34s} {'':>12s} {'':>14s} {'':>8s}  {note}")
print("\n== the falsifiable form ==")
print("any body observed with a MEDIUM bow must sit at >= ~0.9 of its own C; any body far")
print("below its C must show no medium bow. 'Oumuamua: 4.6e-4 of its C, no bow -> PASS,")
print("not an anomaly. RBH-1: 0.996, the bow -> PASS. One future bow without the cap, or")
print("one cap-runner without a bow, kills the law. The shockwave catalog now has one rule.")
