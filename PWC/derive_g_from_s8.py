# Can we derive g from S8 = the drained tension fraction? (2026-10-12)
import math
c0 = 2.99792458e8
s = 1.0/19.0
alpha = 1.0/137.036
g_target = 16*math.pi**3*alpha/3.0
S8_target = 1.0/g_target
melt = 0.95

print(f"g = 1/S8 -> S8 = {S8_target:.4f} ; the drained fraction = {1-S8_target:.4f}\n")
print("candidates for S8 = the remaining tension fraction, from the locked set:")
cands = {
  "e^(-3 x 0.95) (tension-heat law, full re-absorbed)": math.exp(-3*0.95),
  "the stretch s": s,
  "1 - melt x 0.1803 (fitted coeff - meaningless)": 1 - 0.95*0.1803,
  "1 - s x 3.254 (fitted - meaningless)": 1 - s*3.254,
  "1/(1 + 3.26 s)": 1.0/(1+3.26*s),
  "1 - (1-s)/5.53 (fitted - meaningless)": 1 - (1-s)/5.53,
  "sqrt(1 - 2s)": math.sqrt(1-2*s),
  "1 - 2s - s^2": 1 - 2*s - s**2,
  "exp(-s*3.25)": math.exp(-s*3.25),
}
for name, val in cands.items():
    print(f"  {name:46s} = {val:.4f}   ({100*(val/S8_target-1):+.2f}%)")

print(f"\nhonest verdict: no locked combination produces 0.8287 cleanly. The identity")
print(f"g x S8 = 1 is real (S8 = 0.8287 sits inside the CMB band 0.834 +/- 0.016), but")
print(f"deriving g FROM it requires deriving S8 from the tension-drain law - and that is")
print(f"the SAME missing state law the JWST check named: how the tension declines as the")
print(f"heat re-absorbs. The two open items are one: the tension-drain law f(melt state).")
print(f"Once S8 = f(0.95) is written, g = 1/S8 follows. The equation is named; the")
print(f"mechanism (gravity = the re-tying pull) has its identity; the state law is the")
print(f"last named gap between the framework and a derived g.")
