# cycle_stability.py - the D/U system's repeating solution (2026-10-17)
# dD/dt = dv . M_tie(D,U) - R(D,U)      (the volume deficit)
# dU/dt = eta . q_cav . M_tie(D,U) - L(U)   (the brake's heat)
# The conversion fires when the tension's recovered (U below the trigger) and
# the field's stressed (D above the prime); it pauses when the heat's over-
# pressure exceeds the brake (U above the suppression). The question: does a
# STABLE limit cycle exist, and what sets its period?
import numpy as np

# the framework's honest ratios (dimensionless toy - the structure's test)
dv   = 1.0        # the volume reduction per unit mass (the f_solid's order)
q    = 1.0        # q_cav's scale (18 c0^2 in the real units - absorbed here)
eta  = 0.5        # the brake's deposition fraction (the open coupling)
tau_fill = 1.0    # the inflow's crossing (the c0 fill)
tau_diss = 3.0    # the heat's dissipation (the radiative bleed - the probe)
U_trig = 0.2      # the reset threshold (the conversion resumes below this)
U_supp = 1.0      # the brake's threshold (the conversion pauses above this)
D_prime = 0.05    # the prime (the field must be stressed to fire)

def M_tie(D, U):
    # the conversion law: fires when the heat's recovered AND the field's stressed
    fire = (U < U_trig) & (D > D_prime)
    return np.where(fire, 1.0, 0.0)

def step(state, dt):
    D, U = state
    dD = dv * M_tie(D, U) - D / tau_fill
    dU = eta * q * M_tie(D, U) - U / tau_diss
    return D + dt * dD, U + dt * dU

# the run: the long integration, hunting the cycle
D, U = 0.0, 0.0
hist = []
dt = 0.005
for i in range(200000):
    D, U = step((D, U), dt)
    hist.append((D, U))
hist = np.array(hist)

# the cycle's signature: the periodic structure in the settled tail
tail = hist[100000:]
# find the conversion events (the M_tie's fires) in the tail
fires = []
for k in range(1, len(tail)):
    if M_tie(tail[k][0], tail[k][1]) == 1.0 and M_tie(tail[k-1][0], tail[k-1][1]) == 0.0:
        fires.append(k)
print("THE D/U SYSTEM - does the cycle repeat?")
print(f"  conversion events in the tail: {len(fires)}")
if len(fires) >= 4:
    gaps = np.diff(fires) * dt
    print(f"  the inter-event gaps (the cycle's period, toy units): mean {gaps.mean():.2f}, std {gaps.std():.2f}")
    print(f"  the regularity: std/mean = {gaps.std()/gaps.mean():.3f}")
    if gaps.std() / gaps.mean() < 0.2:
        print("  VERDICT: a STABLE limit cycle exists - the brake and the reset hold")
        print("  a regular rhythm; the period's the thermal-recovery's own.")
    else:
        print("  VERDICT: the events repeat but irregularly - the cycle's marginal")
        print("  at these couplings; the eta/thresholds need the sharper forms.")
elif len(fires) > 0:
    print("  too few events - the system settled without a repeating cycle at")
    print("  these parameters")
else:
    print("  NO events - the system settled to the quiescent state (the fire's")
    print("  conditions never re-armed)")
print()
print("honest note: the toy's the STRUCTURE's test (the framework's ratios in")
print("dimensionless form) - the physical period needs the real tau_diss/tau_fill")
print("and the eta. The stable cycle's existence is the question; the 106 kpc")
print("stays the comparison, not the target.")
