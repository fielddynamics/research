# CMB Gravitational Enhancement — Structural Extensions and Future Directions

**Status:** Internal working document — results verified but not yet placed in the docs framework  
**Source:** Extended derivation session, March 2026  
**Author:** Stephen Nelson — Gravity Field Dynamics

---

## Overview

During the construction of the CMB Gravitational Enhancement overview and derivation pages, several structural results emerged that are mathematically verified but were excluded from the published pages to maintain fortress discipline. This document collects them for future use — as follow-up pages, journal paper sections, or validation suite targets.

Each item is labeled by its logical status:
- **Level A:** Algebraically proven from the framework
- **Level B:** Numerically verified, structural interpretation
- **Level C:** Observation, not yet derived

---

## 1. Closed-Form Analytic Enhancement (Level A)

The recombination enhancement can be expressed as a single exact function of redshift, eliminating the step-by-step numerical chain.

Starting from $\mathcal{E} = 1 + 1/x$, substituting $x = \sqrt{g_s/a_0(z)}$, and applying $a_0(z) = a_0(0)(H(z)/H_0)^{1-1/\pi}$:

$$\mathcal{E}(z) = 1 + \sqrt{\frac{a_0(0)}{g_s(z)}} \left(\frac{H(z)}{H_0}\right)^{\frac{\pi - 1}{2\pi}}$$

The exponent $(\pi - 1)/(2\pi)$ is half the cosmological scaling exponent, entering through the square root in $x = \sqrt{g_s/a_0}$. At $z = 1100$ this returns $\mathcal{E} = 6.46$ continuously.

**Why it was excluded:** Adds a proposition without adding new physics. The step-by-step chain is more pedagogically transparent.

**Future use:** Journal paper, as the compact form of the main result.

---

## 2. Energy Functional Cancellation at the Field Origin (Level A)

At the deep-field limit governing the CMB epoch, the face-coupling and flow-coupling energy densities of the scalar sector exactly cancel, leaving the Field Origin term alone to drive the acoustic oscillations.

The scalar kinetic functional is $F(y) = y - 2\sqrt{y} + 2\ln(1+\sqrt{y})$ with $y = x^2$. Expanding for $x < 1$:

$$F(x^2) = x^2 - 2x + \left(2x - x^2 + \frac{2}{3}x^3 - \mathcal{O}(x^4)\right) = \frac{2}{3}x^3 + \mathcal{O}(x^4)$$

The $x^2$ term ($K^2 = 16$ face coupling) and the $-2x$ term ($sK = 4$ flow) cancel exactly. The CMB-epoch scalar energy density is driven entirely by the Taylor remainder of the $2\ln(1+x)$ term — the $K^0 = 1$ Field Origin contribution.

**Why it was excluded:** Beautiful structural result but expands the derivation attack surface. The derivation page proves the enhancement without needing the energy functional decomposition.

**Future use:** Covariant Completion deep-dive page, or dedicated "Field Origin Isolation" result.

---

## 3. The Acoustic Tully-Fisher Theorem (Level A)

The CMB acoustic peaks are mathematically identical to galactic rotation curves — the same kinematic law operating on different tracers.

In the deep-field limit, $g_s = g_t^2/a_0$. Let $c_s$ be the plasma sound speed and $r_s$ the sound horizon. Then $g_t = c_s^2/r_s$ and $g_s = GM_{ac}/r_s^2$. Substituting:

$$\frac{GM_{ac}}{r_s^2} = \frac{c_s^4}{r_s^2 \cdot a_0(z_{\text{rec}})}$$

$$c_s^4 = GM_{ac} \cdot a_0(z_{\text{rec}})$$

This is the baryonic Tully-Fisher relation $v^4 = GMa_0$ with the sound speed $c_s$ replacing the rotation velocity $v$. The acoustic peaks and galactic rotation curves are the same equation — one operating on the plasma sound horizon, the other on a stellar disk, both mediated by the topologically scaled saturation scale.

**Why it was excluded:** Powerful unification result but requires careful framing to avoid overreach. The CMB page already connects to Tully-Fisher through the velocity evolution exponent.

**Future use:** Standalone page or journal paper Section V. This is a theorem, not an approximation.

---

## 4. The Screening Identity Lock: $\Omega_b/\Omega_c \equiv x$ (Level A + Level B)

The $\Lambda$CDM ratio of baryonic to dark matter density is not an independent initial condition. It is the screening equation of the stellated octahedron.

The screening identity $x(1-\mu) = \mu$ rearranges to:

$$\frac{\mu}{1-\mu} = x$$

The TetA fraction $\mu$ maps to $\Omega_b$ and the TetB fraction $(1-\mu)$ maps to $\Omega_c$ in the $\Lambda$CDM parameterization. Therefore:

$$\frac{\Omega_b}{\Omega_c} \longleftrightarrow x$$

**Numerical verification:**
- GFD at $z = 1100$: $x = 0.183$
- Planck 2018: $\Omega_b h^2 / \Omega_c h^2 = 0.0224/0.1200 = 0.187$
- Agreement: $\sim 2\%$

If this identification holds, $\Lambda$CDM's six parameters reduce by one — $\Omega_c h^2$ is not independent of $\Omega_b h^2$ but locked to it by the screening equation. The ratio of ordinary matter to "dark matter" is the acceleration ratio $x$, computed from the constitutive law with zero free parameters.

**Why it was excluded:** The most powerful single result in the session, but requires careful defense of the $\mu \leftrightarrow \Omega_b$ mapping at the Boltzmann hierarchy level. The derivation page correctly labels the $\mathcal{E} \leftrightarrow \Omega_m/\Omega_b$ correspondence as Level B. This result inherits that caveat.

**Future use:** Publish first. If $\Omega_b/\Omega_c \equiv x$ is falsifiable, novel, and strips a free parameter from the standard model. This forces a response.

---

## 5. The Galactic-Cosmological Equivalence Lock (Level A)

The global gravitational enhancement $\mathcal{E}_{\text{CMB}}$ driving the acoustic peaks at $z = 1100$ is mathematically identical to the local ratio of inferred dark matter to baryonic matter at any radius in a $z = 0$ galaxy. Both are exact evaluations of $1/\mu(x)$.

**Proof.** In the analysis of galactic rotation curves, the total inferred dynamical mass (typically parameterized as baryonic mass plus an NFW dark matter halo) is $M_{\text{total}} = rv^2/G$. The GFD decoded baryonic mass, derived from the scalar-tensor transition, is $M_{\text{dec}} = rv^4/[G(a_0 r + v^2)]$.

The ratio at any radius:

$$\frac{M_{\text{total}}}{M_{\text{dec}}} = \frac{rv^2/G}{rv^4/[G(a_0 r + v^2)]} = \frac{a_0 r + v^2}{v^2} = 1 + \frac{1}{x} = \frac{1}{\mu(x)}$$

This algebraic identity holds at every radius in every galaxy, verified to machine precision ($< 10^{-16}$) across the CDM translation suite.

At recombination, the global ratio of total gravitating mass to baryonic mass is $\Omega_m/\Omega_b$. As derived on the CMB page, this cosmic enhancement is identically $1/\mu(x_{\text{rec}}) = 6.46$.

Therefore, the "dark matter" in the early universe and the "dark matter" in late-universe galaxies are not two separate phenomena linked by structure formation. They are the exact same partition function — $1/\mu(x)$ — evaluated at different acceleration states. $\Lambda$CDM requires billions of years of N-body simulations to connect the cosmic dark matter density at $z = 1100$ to the dark matter halos of galaxies at $z = 0$. GFD connects them with a single algebraic identity.

The NGC2998 rotation curve makes this visible. The bar chart shows GFD and MOND hovering at 1× the decoded mass (they agree on the baryonic content), while CDM climbs from 1× at the center to 3–4× at the outer radii. Those purple bars growing with radius ARE $1/\mu(x)$ evaluated at each point — the same function that, evaluated globally at $z = 1100$, returns 6.46. The halo is the constitutive law, fitted with parameters instead of derived from topology.

**Structural consequence:** If a referee accepts the SPARC galaxy rotation curve results (verified without free parameters to machine precision), this identity forces acceptance of the CMB enhancement, because the mathematics is algebraically identical. The dark matter illusion is completely scale-invariant: same equation at $z = 0$ per galaxy, same equation at $z = 1100$ globally.

**Why it was excluded from the derivation page:** It connects two results from different pages (CDM Translation and CMB Enhancement) and its full force requires the galactic verification to be independently established first. The derivation page proves the CMB enhancement from its own chain. This result proves the CMB and galactic results are the same chain.

**Future use:** This is the master key. It belongs as the bridge between the galactic and cosmological sections of the framework — either as a standalone page or as the opening theorem of a unified cosmology paper. It should be published after the SPARC-wide verification is complete across all 175 galaxies.

---

## 6. The Complement Symmetry Inversion (Level A)

The CMB enhancement and a galactic Newtonian core are exact topological duals through the Field Origin.

The complement symmetry $\mu(x) + \mu(1/x) = 1$ gives:

$$1 - \mu(0.183) \approx 0.845 = \mu(5.46)$$

The 84.5% TetB fraction driving the CMB "dark matter" enhancement is identically the 84.5% TetA fraction of a system at the reciprocal acceleration $x = 5.46$ — the strong-field interior of a galactic vortex. The early universe's deep-field condition and a galaxy's Newtonian core are mirror images, mapped through the Field Origin via $x \to 1/x$.

**Why it was excluded:** Elegant but interpretive. The derivation page stays at Level A/B; this is a Level B structural statement.

**Future use:** Constitutive Law page extension, or the complement symmetry section of a unified cosmology paper.

---

## 7. The Möbius State Map at the CMB (Level A)

The effective state coordinate $s(x) = (x-1)/(x+1)$ evaluated at the CMB epoch reveals the structural position of recombination in the stellated octahedron's state space.

| Quantity | $x$ | $s(x)$ | $f(x)$ | Regime |
|:---|:---:|:---:|:---:|:---|
| TetB floor | $0$ | $-1$ | $13$ | Deep field ceiling |
| Naive CMB | $0.037$ | $-0.929$ | $13.28$ | Pinned to floor |
| **Corrected CMB** | **$0.183$** | **$-0.690$** | **$14.24$** | Interior TetB |
| Field Origin | $1$ | $0$ | $17$ | 50/50 partition |
| CMB complement | $5.46$ | $+0.690$ | $19.76$ | Interior TetA |
| TetA ceiling | $\infty$ | $+1$ | $21$ | Full Newtonian |

Key observations:
- The tiling correction moves the CMB from $s = -0.929$ (92.9% toward the floor) to $s = -0.690$ (69.0%) — a quarter of the way back toward the Field Origin.
- The enhancement is $\mathcal{E} = 1 + 1/x = 1 + 5.46 = 6.46$. The enhancement IS one plus the complement point.
- The CMB complement at $s = +0.690$ is the mirror image — the same $|s|$, opposite sign.

**Future use:** Effective State Decoding page, or a Möbius visualization of cosmic evolution.

---

## 8. The Naive Enhancement and the 28 Geometric Elements (Level C)

The naive enhancement before tiling correction is $\sim 28$. The stellated octahedron has $K(K+D) = 4 \times 7 = 28$ geometric elements (8 vertices + 12 edges + 8 faces). The same 28 that gives the fractional correction $1/28$ in the fine structure constant $1/\alpha = 137 + 1/28$.

Without the tiling correction, the constitutive law responds with the full geometric element count — all 28 elements "active." The $1/\pi$ correction brings the response down from the full scaffold count to the actual coupled fraction at that epoch.

**Status:** Numerical coincidence or structural connection — not yet determined. The naive $x \approx 0.037 \approx 1/27$ is close to $1/28$ but not exact. If the link between $x_{\text{naive}}$ and $1/K(K+D)$ can be shown algebraically, this becomes a Level A result.

**Future use:** Track. Do not claim until the algebra is locked.

---

## 9. Pascal's Row 4,6,4 and the Enhancement 6.46 (Level C)

The inner entries of the $K = 4$ Pascal row are $4, 6, 4$. The CMB enhancement is $6.46$. Same three digits, palindromic.

The enhancement derives entirely from $K = 4$: the $1/\pi$ from spheres in $D = 3$, the constitutive law from the coupling polynomial, the 28 from the row's geometry. Every number in the derivation traces to this row.

**Status:** Striking numerical pattern. Not yet shown to be algebraically forced (i.e., that $(x+1)/x$ evaluated at the tiling-corrected deep-field limit reduces to a function of $\binom{4}{1}$, $\binom{4}{2}$, $\binom{4}{3}$). Coincidence until proven otherwise.

**Future use:** Track. If someone finds the short algebraic path, this becomes extraordinary.

---

## 10. The Nucleation Story: CMB Packing and First-Generation Hydrogen (Level B)

The dense packing at the CMB epoch is the same physics that enables hydrogen creation without stellar compression.

In the gravity field packing picture, creating hydrogen requires pushing an unbound field through the Field Origin ($f = 17$, $x = 1$) from TetA onto TetB. At late times, stellar interiors provide this compression (the "bicycle pump"). At the CMB epoch, no stars exist. But the ocean is packed a billion times denser than today, and every perturbation is amplified 6.4× by the TetB fraction. The dense packing itself provides the compression that forces the first unbound fields through the gate.

The CMB enhancement (what Planck measures) and hydrogen nucleation (what first-generation stars are made of) are two consequences of the same dense-packing physics at the same epoch.

**Why it was excluded:** Opens the bound-state nuclear physics channel, which the CMB page deliberately firewalls. The overview page is entirely unbound ocean physics.

**Future use:** Nucleosynthesis page, or a "Cosmological Origins" page connecting the CMB, hydrogen creation, and first-generation stars through the packing density at recombination.

---

## 11. The K=1 Big Bang: Pascal's Ladder (Level C)

Pascal's triangle is the structural ladder of cosmic evolution:

| Row | Sum | Geometry | Gravity? |
|:---:|:---:|:---|:---:|
| $K=1$ | $2$ | No faces, no enclosure, no volume | No |
| $K=2$ | $4$ | Line segment, 1D enclosure only | No |
| $K=3$ | $8$ | Triangle, 2D enclosure, $K^2 \neq 2^K$ | No |
| $K=4$ | $16$ | Tetrahedron, self-dual, $K^2 = 2^K$ | **Yes** |

At maximum compression (Big Bang), the substrate is at $K = 1$ — no topology, no gravity, just existence and its mirror. As the universe expands, the packing thins until there is room for $K = 4$ to organize. Gravity emerges. The coupling polynomial starts operating. The constitutive law exists.

The $1/\pi$ at $z = 1100$ measures position on this ladder: $K = 4$ exists and gravity is operating, but the dense packing suppresses coupling efficiency. The exponent $1 - 1/\pi$ is the cost of running $K = 4$ topology in a universe that hasn't fully expanded into it yet.

The photonic substrate has 28 (the scaffold, the geometry) but not 137 (the coupling strength). The 137 requires the coupling polynomial, which requires $K = 4$, which requires gravity. Shape exists before coupling. Geometry before interaction. The substrate before its own self-interaction constant.

**Status:** Interpretive framework for the Big Bang within GFD. Not derivation. Not for the CMB page.

**Future use:** Cosmological origins page, or the opening section of a Paper III on quantum origins.

---

## 12. Screening Directionality (Level A — for Constitutive Law page)

The following paragraph is ready to insert at the end of "The Screening Equation" section on the Constitutive Law page:

> When this partition accumulates across the field — from one radius to the next in a galaxy, from one boundary to the next in a cosmological tiling — the remaining fraction $(1 - \mu)$ compounds. Compounding fractions produce power laws. This is what the partition function does when applied across a lattice: the TetA fraction $\mu$ and the TetB fraction $(1 - \mu)$ are both active at every point, the screening equation holds them in balance at each step, and the cumulative effect of that balance across many steps is a power-law scaling relationship. The exponent encodes the geometry of the accumulation. This property is what allows the constitutive law to govern not only the radial profile of a single galaxy but also the cosmological evolution of the saturation scale across epochs of different packing density.

**Status:** Ready to deploy. Bridges the Constitutive Law page to the CMB page.

---

*Copyright © 2025–2026 Stephen Nelson. Documentation: CC BY 4.0.*
