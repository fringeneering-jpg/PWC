# PWC glitch check — pulsar glitches as hydrodynamic stall-and-recatch

**Hypothesis tested:** the rotating ρ_max core (neutron body's shell) briefly re-locks with
the medium when it hits a density variance, and the swept medium's angular momentum is
transferred IN to the spin (glitches are spin-ups, Δν/ν > 0).

**Script:** `scratch/pwc_glitch_stall_check.py` · **output:** `scratch/pwc_glitch_stall_output.txt`
Locked numbers used: ρ_max = 1.304×10¹⁵, ρ_core = 2.3×10¹⁷, Y_bow = 5.93×10²⁶ Pa,
f_solid = 0.085%, ρ₀ = 8.74×10⁻²⁷, a_max = 3.23×10¹¹; cap law v_cap = √(2Y/ρ);
catch law F = ½ρ₀v²·f_solid·A_geo. Repo untouched.

## 1. Surface speed vs caps

| Object | v_surf = 2πRf | vs ρ_max cap 954 km/s | vs ρ_core cap 72 km/s | vs gas 56,156 km/s |
|---|---|---|---|---|
| Vela (R = 11 km, 11.195 Hz) | 774 km/s (703–844 for R = 10–12) | **0.81×** (below) | **10.8× over** | 0.014× |
| Crab (R = 10 km, 29.95 Hz) | 1,882 km/s | **1.97× over — permanently stalled** | 26× over | 0.034× |
| MSP (716 Hz) | 44,988 km/s | **47× over** | 626× over | 0.80× |

Stall trigger: Vela needs a local density ≥ 2Y/v² = 1.98×10¹⁵ = **1.52 ρ_max (a +52%
density variance)** to stall at 774 km/s. A 2×10⁻⁶ glitch changes v_surf by 1.5 m/s —
the spin-up never approaches the cap. Crab/MSPs sit permanently above the cap: under the
stall law they could not rotate at all, yet they rotate and glitch.

## 2. Re-lock momentum transfer (swept ambient, drag law)

Δν/ν = m_swept·v·R / (2π I ν), m_swept = ρ₀·f_solid·A_geo·v·T

| Case | m_swept | Δν/ν predicted | observed | shortfall |
|---|---|---|---|---|
| Vela, 100 d, 4πR² | 7.6×10⁻⁸ kg | **6.8×10⁻³⁸** | 2×10⁻⁶ | **2.9×10³¹** |
| Vela, 2.5 yr (interglitch) | 6.9×10⁻⁷ kg | 6.2×10⁻³⁷ | 2×10⁻⁶ | 3.2×10³⁰ |
| Crab, 100 d, 4πR² | 1.5×10⁻⁷ kg | **1.4×10⁻³⁷** | 10⁻⁸ | 7.3×10²⁸ |

One Vela glitch demands **2.23×10²⁴ kg caught (1.1×10⁻⁶ M☉, 0.37 Earth masses)**. Sweep
time at the locked f_solid: **8×10³⁰ yr**; even at f_solid = 1 (100% catch): 6.9×10²⁷ yr.
The medium swept in Vela's entire ~11,000-yr characteristic age, at 100% catch, is
**3.7 kg** → Δν/ν = 3.3×10⁻³⁰, still **6×10²³ short**.

## 3. Trend test

Model predicts glitch size ∝ ν → Crab glitches 2× **bigger** than Vela's.
Observed: Crab 10⁻⁸–10⁻⁹ vs Vela 2×10⁻⁶ → 200–2000× **smaller**. Trend inverted by ~400×.

## 4. Recovery timescale (observed: days–months)

- Luminal response across star / yield reach: R/c₀ = 37 μs, r_e/c₀ = 80 μs (r_e = 24 km).
- Framework drag torque 9.3×10⁻⁶ N·m → ν̇ = 1.1×10⁻⁴⁴ Hz/s vs Vela's observed
  ν̇ = 1.55×10⁻¹¹ Hz/s: the drag law is **1.4×10³³× too weak to even spin Vela down**.
- Drag-only relaxation of one glitch: 6.5×10³¹ yr.
No locked number produces days–months.

## 5. Sign

The locked framework's medium is stationary. Catching stationary ambient in the rotating
frame is a **spin-down** (−m·v·R), not a spin-up. Δν > 0 requires the swept medium to
already carry specific AM > v·R at the shell — no locked mechanism rotates the ambient.

## Verdict

**FAIL.** The stall-and-recatch gives Δν/ν ≈ 6.8×10⁻³⁸ for Vela vs the observed 2×10⁻⁶
— **31 orders of magnitude short**; a single Vela glitch would need the shell to catch
0.37 Earth masses of medium, while even a 100%-efficient catch of everything the shell
sweeps in the pulsar's entire lifetime totals 3.7 kg (still 6×10²³× short). The same
mismatch (≈29 orders) holds for the Crab, the model's glitch-size trend with spin rate is
inverted ~400× versus observation, and no locked framework number produces the observed
days–months recovery (candidates: 37–80 μs luminal, or 10³¹–10³³ yr drag). The mechanism
also fails on sign (a stationary medium transfers angular momentum out, not in) and on
self-consistency: Vela sits 19% below the 954 km/s cap and would need a +52% density
variance to stall, while the Crab (1.97×) and all millisecond pulsars (up to 47×) are
permanently above the cap and could not rotate at all under the stall law — yet they
rotate and glitch. Hydrodynamic stall-and-recatch of the ambient medium is not the
mechanism of pulsar glitches at the locked PWC numbers.
