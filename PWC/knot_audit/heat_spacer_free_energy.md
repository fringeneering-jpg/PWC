# Heat-Spacer Free-Energy Model

**Status:** Hypothesis specification and reproducible computational scan. Generated numerical artifacts are pending execution of the accompanying script in a Python environment with NumPy and SciPy.

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
