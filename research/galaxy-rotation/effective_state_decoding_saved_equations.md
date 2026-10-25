# Effective State Decoding from Galaxy Rotation Curves

**Author:** Stephen Nelson — Gravity Field Dynamics  
**Status:** Working note — extracted from exploratory session, March 2026

---

## What this document is

This note collects the genuinely useful results from an extended derivation session on decoding the effective chamber-state coordinate from galaxy rotation curve data. Each section states what the object *actually is*, what it adds beyond existing GFD equations, and where it fits in the framework.

---

## 1. The Ontological Correction

**What it is:** A framework-level interpretive rule, not a new equation.

In observable 3+1 spacetime we do not directly access TetB. The Möbius state map applied to velocity data yields an *effective* state coordinate $s_{\text{eff}}(r)$, encoding how strongly the interior vortex drive contributes to the exterior TetA-side field response at radius $r$. Negative values of $s_{\text{eff}}$ do not mean we are "seeing into TetB." They mean the observed field response requires stronger interior drive to explain. This is exactly analogous to $M_{\text{dec}}(r)$ being an effective mass decode, not literal hidden mass.

**Why it matters:** Without this clarification, the state map is easily misread as a direct window into TetB geometry. It is a projection, not a sightline.

---

## 2. The Effective State Diagnostic

**What it is:** The existing Möbius state map $s(x) = (x-1)/(x+1)$ rewritten in directly observable variables and named as a standalone diagnostic quantity parallel to $M_{\text{dec}}(r)$.

$$s_{\text{eff}}(r) = \frac{v^2(r) - a_0 r}{v^2(r) + a_0 r}$$

This is not new mathematics — it is $s(x)$ with $x = v^2/(a_0 r)$ substituted. The value is in treating it as a named, computable observable extracted from rotation curve data at every measured radius.

---

## 3. The Throat Radius

**What it is:** The radius where the effective state crosses zero, i.e. the TetA/TetB balance point projected into observed space.

$$v^2(r_T) = a_0 \, r_T$$

Equivalently: $x(r_T) = 1$, $s_{\text{eff}}(r_T) = 0$, $g_t(r_T) = a_0$.

This gives a single concrete number per galaxy, locatable by interpolation on the rotation curve. No fitting required — just $a_0$ and the data.

---

## 4. Throat Sharpness (novel)

**What it is:** The rate at which the effective state coordinate crosses zero at the throat, expressed purely in terms of the observed logarithmic velocity slope.

Define the log-slope $m(r) \equiv d\ln v / d\ln r$ and the acceleration shape $A(r) = 2m(r) - 1 = d\ln g_t / d\ln r$.

The state derivative is:

$$\frac{ds}{d\ln r} = \frac{2x}{(1+x)^2} A(r)$$

At the throat ($x = 1$) this simplifies to:

$$\Sigma_T \equiv \left.\frac{ds}{d\ln r}\right|_{r_T} = \frac{1}{2}\,A(r_T) = \frac{1}{2}(2m(r_T) - 1)$$

**Why it matters:** This is the most genuinely new object in the session. It measures how *sharply* a galaxy's field crosses chamber-state space at the throat. Different galaxies may have sharp, broad, or weak throats even if they all cross $s = 0$. This diagnostic does not appear in the MOND/RAR literature.

---

## 5. The Throat Tuple

**What it is:** A four-parameter characterization of each galaxy's vortex throat structure.

$$\mathcal{T} = \bigl(r_T,\; m(r_T),\; \Sigma_T,\; \Delta_T\bigr)$$

where $\Delta_T = g_t(r_T)/g_b(r_T)$ is the drive ratio at the throat (how much the total field exceeds the baryonic source field at the balance point).

**Why it matters:** This replaces halo-parameter classification with throat-state classification. If $\mathcal{T}$ shows clean correlations across SPARC galaxies (e.g. with bulge fraction, morphological type, or total baryonic mass), that is a publishable result.

---

## 6. Chamber Weights

**What it is:** A decomposition of the effective state into fractional TetA/TetB projected contributions.

$$\mu_A(r) = \frac{1 + s_{\text{eff}}(r)}{2}, \qquad \mu_B(r) = \frac{1 - s_{\text{eff}}(r)}{2}, \qquad \mu_A + \mu_B = 1$$

Simple algebra from $s_{\text{eff}}$, but the notation is useful: it frames the observed field as a projected mixture of two chamber contributions required to produce the measured velocity.

---

## 7. The Full Local State Package

**What it is:** An explicit inventory confirming that at every observed radius, velocity alone determines a complete field-state vector.

$$r \;\mapsto\; \bigl(v,\; g_t,\; x,\; s_{\text{eff}},\; f,\; \mu,\; F,\; M_{\text{dec}}\bigr)$$

where $f(r) = 17 + 4\,s_{\text{eff}}(r)$, $\mu(r) = x/(x+1)$, $F(r) = x^2 - 2x + 2\ln(1+x)$ (note: verify the kinetic functional argument — this uses $y = x$, not $y = (\nabla\Phi)^2/a_0^2$; confirm whether the pointwise substitution is valid before publishing).

---

## 8. The Inverse Problem Framing

**What it is:** A statement of what velocity data can and cannot reconstruct, and what closes the gap.

- Velocity alone → full exterior effective state curve (Meaning A: solved).
- Full literal vortex (TetA + throat + TetB as unified object) → requires a throat closure rule plus baryonic mass (Meaning B: open problem).
- The missing piece is geometric, not observational: it is the mirror/continuation law at the throat, not more data.

The river analogy: measuring downstream velocities gives local field state exactly, but cannot reconstruct upstream bends and obstacles. Baryonic mass profiles provide the "upstream geology." Topology provides the channel geometry. All three together may overconstrain the inversion.

---

## Items intentionally discarded

- The "teaching note" draft (Sections 1–9): restates existing GFD equations with no new content.
- Repeated "analogy to effective mass" paragraphs: same point made four times.
- Kinetic channel energy decomposition ($E_{K^2}$, $E_{sK}$, $E_1$): needs argument verification before use.
- Three-regime descriptions ($s > 0$, $s = 0$, $s < 0$): obvious from the formula, not worth page space.
- All "if you want" hedges and "Version 2" offers: conversational filler.

---

*Copyright © 2025–2026 Stephen Nelson. Documentation: CC BY 4.0.*
