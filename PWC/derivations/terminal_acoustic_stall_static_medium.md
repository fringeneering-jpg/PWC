# Terminal Acoustic Fluid Stall and the static-medium Hawking/Schwarzschild correspondence (Jaden, 2026-10-06)

Registry: `DERIVATIONS.md` rows 24 and 24b. Reproduced by [`../static_medium_check.py`](../static_medium_check.py).
Status words follow the registry: the mechanism is Jaden's (locked); the two higher-order forms in section 2 are **not** derived from the medium's equation of state and are marked as such.

## 1. The compounding law (row 24)
The photon is the medium's own wave at its speed limit, so it already carries maximum drag (row 15: light and the Max-P bow wave are one law at two densities). Extra squeeze from the pull/pressure gradient therefore compounds on a photon already slowed. With x = GM/(r c0^2):

- registry first order (row 22): dn/dx = 2, n = 1 + 2x (bending 4GM/(b c0^2), gamma = 1, Shapiro);
- single compounding: dn/dx = 2n, n = e^(2x) (never stalls);
- the law adopted: **dn/dx = 2 n^2, n = 1/(1 - 2x), v = c0 (1 - 2x)** (a slower photon spends longer in the gradient and the squeeze acts on it harder: two compounding factors). The first order equals row 22. The photon stalls at x = 1/2, r = 2GM/c0^2, the sonic choke, for every mass: the event horizon is a Terminal Acoustic Fluid Stall (two limits meeting; no flowing medium; the medium does not move).

| x | linear 1 + 2x | e^(2x) | adopted 1/(1 - 2x) |
|---|---|---|---|
| 0.2 | 1.40 | 1.49 | 1.67 |
| 0.4 | 1.80 | 2.23 | 5.00 |
| 0.5 | 2.00 | 2.72 | stall |

Companion (not derived): the work term compounds with the same factor, dL/L = -n dx, so L ~ (1 - 2x)^(1/2) and z = (1 - 2x)^(-1/2) - 1: 0.291 at x = 0.2 (supersedes row 21's e^x - 1 = 0.221 in the strong field; first order unchanged). Consequence recorded by the author: PWC's strong-field redshift equals GR's; the neutron-star discriminator of row 21 no longer separates them.

## 2. Static-medium reconciliation (row 24b)
Why: the September Hawking derivation (PWC.md section 8, commit e9f95df) says "infalling medium reaches c_s"; the October ruling is that the medium does not flow. Static-medium form, no flow anywhere (f = 1 - 2x = 1 - r_s/r):

- **Push (speed budget).** The matter driven to v_ff = sqrt(2GM/r) uses up part of the medium's capacity: c_loc^2 + v_ff^2 = c0^2, so c_loc = c0 sqrt(f). First order c0(1 - x): the row-22 push slowing. The same quantity c0^2 - v^2 is the one in the registry's Hawking surface gravity.
- **Pull.** Radial paths are lengthened by 1/sqrt(f). First order 1 + x: the row-22 channel lengthening.
- Radial coordinate speed = c_loc / (1/sqrt f) = c0 f (stalls at x = 1/2: row 24, n_r = 1/f, dn/dx = 2n^2). Transverse coordinate speed = c0 sqrt(f) (n_t = 1/sqrt f, dn/dx = n^3). n_r = n_t^2.
- These are exactly the null cone of g_tt = -f c0^2, g_rr = 1/f: bending 4GM/(b c0^2) at first order, redshift z = 1/sqrt(f) - 1, static clocks ticking as sqrt(f).
- **Hawking.** kappa = (1/2) c0^2 f'(r_s) = c0^4/(4GM), identical to the registry's (1/2)|d(c0^2 - v^2)/dr|, so T = hbar kappa/(2 pi k_B c0) = hbar c0^3/(8 pi G M k_B) with no flowing medium (symbolic check in the script). With a flat proper radial length (no lengthening) the same method gives twice this T, so the lengthening is load-bearing.

| x | f | c_loc/c0 | n_r = 1/f | n_t = 1/sqrt f | z = 1/sqrt f - 1 |
|---|---|---|---|---|---|
| 0.05 | 0.90 | 0.949 | 1.11 | 1.054 | 0.054 |
| 0.10 | 0.80 | 0.894 | 1.25 | 1.118 | 0.118 |
| 0.20 | 0.60 | 0.775 | 1.67 | 1.291 | 0.291 |
| 0.30 | 0.40 | 0.632 | 2.50 | 1.581 | 0.581 |
| 0.40 | 0.20 | 0.447 | 5.00 | 2.236 | 1.236 |
| 0.45 | 0.10 | 0.316 | 10.0 | 3.162 | 2.162 |
| 0.50 | 0 (exterior law) | 0 | capped | capped | capped |

## 3. Finite cap (no infinities)
The exterior law (section 2) is an asymptotic form valid for r > r_h. At the choke the strain reaches mechanical yield and is capped by the finite Max-P state, so the physical wave speed does not reach exactly zero. The size of the floor is **not derived**: row 23's lattice law c ~ rho^(-1/3) extrapolated to rho_max gives 1.9e-14 c0 (5.7e-6 m/s); row 15's speed-limit law gives 954 km/s at rho_max.

## 4. What is and is not shown
Shown: light propagation (radial and transverse null speeds), static redshift, the Hawking temperature, the first-order tests (V5 of the master framework), all in a stationary medium. Not shown: second-order light deflection (the 15 pi/4 term) and the black-hole shadow; timelike orbits (perihelion precession), frame dragging, gravitational-wave polarization content; why the push is sqrt(f) and the pull 1/sqrt(f) from the medium's equation of state (the speed-budget reading c_loc^2 + v_ff^2 = c0^2 is the proposed reason; a critical-exponent reading of 1/sqrt(f) as the mean-field correlation-length exponent nu = 1/2 is a further hypothesis). Tension: for M >~ 50 Msun the rho_max shell edge lies inside the choke (edge/choke 0.87 at GW150914, 2.7e-5 at TON 618), so the medium at the choke is only moderately compressed there; a claim that the choke is the Max-P phase boundary for every mass is not supported by the shell geometry.
