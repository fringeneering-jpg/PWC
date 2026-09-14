# Custom Prompt Library: Quantum Fluid Cosmology

Use these prompts in frontier models (like Gemini Pro or ChatGPT) to explore and develop specific mathematical details of the Quantum Fluid Medium framework. Copy and paste the text block under each section.

---

## 1. Analogue Gravity & Acoustic Metrics
**Goal**: Investigate the mathematics of wave propagation in compressible superfluids to derive standard relativistic spacetime metrics.

```text
System Directive: Adopt the role of a mathematical physicist specializing in analogue gravity, acoustic geometries, and superfluid vacuum theories.

Task:
Derive the line element for a sound wave propagating in a moving, barotropic, compressible, irrotational fluid. Show how this maps onto the acoustic metric:
ds^2 = (rho_0 / c_s) * [ -(c_s^2 - v^2)dt^2 - 2*v_i * dt * dx^i + delta_ij * dx^i * dx^j ]

Explain the physical meaning of each term in this metric:
1. Why does fluid density (rho_0) act as a conformal factor?
2. How does the speed of sound (c_s) play the role of the speed of light (c)?
3. How does this model explain gravitational lensing as a refractive index variation in the fluid, rather than warped space?
4. Address the Scharnhorst effect and how locally invariant light speeds (or sound speeds) are simulated inside a localized expansion bubble.

Present all derivations step-by-step with clear explanations. Do not default to standard general relativity arguments; work within the fluid-analog framework.
```

---

## 2. Pilot-Wave Hydrodynamics & Wave-Particle Localization
**Goal**: Model quantum mechanics deterministically using Couder’s bouncing droplets and pilot-wave hydrodynamics.

```text
System Directive: Adopt the role of a fluid physicist specializing in Pilot-Wave Hydrodynamics (PWH) and the mechanical interpretation of quantum phenomena (John Bush's framework).

Task:
Explain the classical mechanics of Yves Couder's walker experiments (millimetric oil droplets bouncing on a vibrating fluid bath). Address the following:
1. How does the droplet (particle) self-propel by interacting with its own wave field?
2. How does the "memory" (non-Markovian behavior) of the surface wave grid simulate quantum behaviors (e.g., diffraction, tunneling, and quantized orbits)?
3. Translate this to a 3D cosmological superfluid: How does a localized particle (like an electron) exist as a concentrated wave pocket ("heavy energy") that constantemente probes the surrounding environment via diffraction?
4. Explain how this fluid model resolves the double-slit experiment without using wave-function collapse or stochastic probability, showing that the wave goes through both slits and coordinates the particle's landing.

Avoid standard Copenhagen interpretation clichés. Ground the explanation strictly in hydrodynamics and deterministic wave fields.
```

---

## 3. Transactional Interpretation & "The Flush"
**Goal**: Detail the mechanics of the "Smear-Reflection-Standing Wave-Flush" sequence using advanced and retarded waves.

```text
System Directive: Adopt the role of an electrodynamics expert specializing in Cramer's Transactional Interpretation (TI) and Wheeler-Feynman absorber theory.

Task:
Describe the four-stage mechanical sequence of a transaction (a quantum collapse):
1. The Smear (Retarded Offer Wave, Psi)
2. The Reflection (Advanced Confirmation Wave, Psi*)
3. The Standing Wave (Constructive interference forming a zero-resistance low-pressure channel)
4. The Flush (The actual transfer of the quantized energy packet)

Address the primary mechanical hurdles:
1. How does the constructive interference Psi*Psi drop the local fluid resistance to zero along the path of least resistance?
2. Model the standing wave as a non-linear waveguide (dielectric breakdown analog). What equation of state would allow the fluid medium to collapse into a lossless pipe during the "Flush" without leaking energy radially?
3. Show how this transactional handshake resolves the Wheeler Delayed-Choice experiment without violating the speed of light for signal propagation.

Provide mathematical context using wave equations and energy densities.
```

---

## 4. Cosmological Cavitation & Rayleigh-Plesset Dynamics
**Goal**: Model the Big Bang and expansion of the universe as a cavitation bubble expanding in a hyper-dense bulk fluid.

```text
System Directive: Adopt the role of a fluid dynamics specialist in cavitation and multi-phase flows, applied to cyclic and cyclic-conformal cosmologies.

Task:
Model our universe as a spherical cavitation bubble of radius R(t) expanding in a cold, hyper-dense bulk fluid of density rho_L. Use the Rayleigh-Plesset equation:
R*d2R/dt2 + 3/2*(dR/dt)^2 = (1 / rho_L) * [ p_B(t) - p_inf(t) - 2*sigma/R - 4*mu*dR/dt ]

Address:
1. If the bulk has high density and pressure p_inf, what mechanism must keep p_B(t) high enough to sustain a 14-billion-year expansion? Model a continuous phase transition at the boundary converting dense bulk fluid into low-density interior space-time fluid.
2. Relate this expansion to the dilution of matter (dust, p = 0) and the transition to a pressure-dominated regime (Dark Energy analog) using the Schutz action principle for relativistic fluids.
3. Model the eventual bubble stall and collapse: Show how the supersonic collapse and sonoluminescence-like effect (compression heating) naturally trigger the next cycle (Big Bang).
4. Explain how time dilation between the low-density bubble and hyper-dense bulk translates a 0.6-second bulk process into a 14-billion-year internal timescale.

Provide numerical scenarios or Python code blocks to demonstrate bubble expansion and collapse curves.
```
