# Heat-Spacer Free-Energy Model

**Status:** Hypothesis specification and reproducible computational scan. Executed 2026-09-30 (Colab, Python 3.13 / NumPy 2.1; re-run in a second environment, Python 3.11 / NumPy 2.4, with identical results). Outputs: [`heat_spacer_scan.csv`](heat_spacer_scan.csv), [`heat_spacer_results.md`](heat_spacer_results.md). 540/540 rows behave as encoded (432/432 outward families positive, 108/108 control negative).

**What that pass is:** a check that the optimiser and bookkeeping are correct. It is not evidence for PWC. By the implicit-function theorem, `dd₀/dT = −(∂²f/∂d∂T)/f''(d₀)`, so with `f'' > 0` the sign of the response is fixed by the sign of the thermal term that was written into each family; the sign of every row can be stated from the input alone, without minimising (`PWC/audit_independence.py` §6 does exactly this and agrees in 540/540 rows). A test that could fail on the physics needs a thermal term whose d-dependence is derived from the medium rather than chosen to point outward.

## Purpose

This note records a conditional thermodynamic requirement for the PWC framework: an outward thermal-support term should increase the finite, stable equilibrium separation \(d_0\) of a paired medium.

\[
\frac{\partial d_0}{\partial T}>0.
\]

Here \(T\) is a dimensionless thermal-support control variable. This document does not derive the trial-potential coefficients from microscopic PWC dynamics, does not select a unique potential, and does not claim experimental confirmation.

## Acceptance conditions

For every parameter tuple and sampled thermal value, an accepted state must meet all of:

\[
d_0>0,
\qquad
\left.\frac{\partial^2 f}{\partial d^2}\right|_{d_0}>0,
\]

and \(d_0\) must lie outside a numerical boundary margin. The trial families contain a short-distance barrier and a large-distance restoring term, so they remain bounded below as \(d\to0\) and \(d\to\infty\).

A parameter tuple passes the heat-spacer test only when the fitted slope satisfies:

\[
\frac{d d_0}{dT}>10^{-7}.
\]

## Trial free-energy families

All quantities are dimensionless.

### A. Linear outward thermal support

\[
f_A(d,T)=\frac{A}{d^{12}}-\frac{B}{d^6}+\frac{K}{2}(d-d_{\rm ref})^2-\alpha Td.
\]

### B. Thermally shifted preferred separation

\[
f_B(d,T)=\frac{A}{d^{12}}-\frac{B}{d^6}+\frac{K}{2}\left[d-(d_{\rm ref}+\beta T)\right]^2.
\]

### C. Saturating outward thermal support

\[
f_C(d,T)=\frac{A}{d^{12}}-\frac{B}{d^6}+\frac{K}{2}(d-d_{\rm ref})^2-\alpha T\frac{d}{d+1}.
\]

### D. Logarithmic thermal term

\[
f_D(d,T)=\frac{A}{d^{12}}-\frac{B}{d^6}+\frac{K}{2}(d-d_{\rm ref})^2-\alpha T\ln d.
\]

### E. Negative control

\[
f_E(d,T)=\frac{A}{d^{12}}-\frac{B}{d^6}+\frac{K}{2}(d-d_{\rm ref})^2+\alpha Td.
\]

Families A-D encode outward thermal support and are expected to produce positive fitted slope. Family E deliberately encodes inward thermal forcing and is expected to produce a negative fitted slope. It checks that the numerical procedure can distinguish the direction of the thermal term.

## Reproducible scan

The script `PWC/heat_spacer_free_energy.py` uses:

\[
A\in\{0.5,1,2\},\quad
B\in\{2,4,8\},\quad
K\in\{2,8\},
\]

\[
d_{\rm ref}\in\{1.0,1.4\},\quad
\alpha\text{ or }\beta\in\{0.1,0.35,0.75\},
\]

and nine equally spaced points on \(T\in[0,4]\). It minimizes over \(d\in[0.35,8]\), rejects boundary or nonpositive-curvature minima, fits \(d_0(T)\), and writes two generated artifacts:

```text
PWC/knot_audit/heat_spacer_scan.csv
PWC/knot_audit/heat_spacer_results.md
```

Run it from the repository root:

```bash
python PWC/heat_spacer_free_energy.py
```

## Interpretation boundary

A passing scan supports only this conditional statement:

> Within the specified finite trial-potential families and parameter grid, the encoded outward thermal-support terms produce increasing stable equilibrium separation.

It does not establish a first-principles PWC microscopic potential, determine physical coefficient values, calculate a matter-locking transition, or experimentally validate PWC.
