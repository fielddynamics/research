# The Energy Functional of the Constitutive Law

*The energy behind $\mu(x) = x/(x+1)$, its two limits, and why its field equation is well behaved · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`AQUAL` `MOND` `energy-functional` `convexity` `ellipticity` `proof`

---

This folder holds a two-page proof and a script that checks every step. The proof concerns the energy from which the constitutive law's field equation is derived. It gives that energy in closed form, shows exactly how it reduces to Newton's gravity and to the deep-MOND regime, and proves that the resulting field equation is well posed: for given conditions on the boundary, the field is unique. This page explains the argument for a reader with first-year calculus.

## The setting

In Newtonian gravity the potential $\Phi$ obeys Poisson's equation, $\nabla^2\Phi = 4\pi G\rho$. That equation comes from minimising an energy whose density is proportional to $|\nabla\Phi|^2$, the square of the field strength.

The AQUAL theory of Bekenstein and Milgrom (1984) keeps this structure but replaces the square by a more general function. The energy density becomes proportional to $F(y)$, where $y = |\nabla\Phi|^2/a_0^2$ measures the field strength against the scale $a_0$. Minimising the energy gives the modified Poisson equation

$$\nabla\cdot\big[\mu(|\nabla\Phi|/a_0)\,\nabla\Phi\big] = 4\pi G\rho ,$$

and the constitutive law is the derivative of the energy function, $\mu(\sqrt{y}) = F'(y)$. Newton is the special case $F(y) = y$, $\mu = 1$.

GFD derives the constitutive law $\mu(x) = x/(x+1)$ (see the [exchange-symmetry proof](../constitutive-law-exchange-symmetry/)). This proof turns to the energy that goes with it.

## Result 1: the energy in closed form

Integrating $F'(y) = \sqrt{y}/(1+\sqrt{y})$ with the substitution $u = \sqrt{y}$ gives

$$F(y) = y - 2\sqrt{y} + 2\ln\big(1 + \sqrt{y}\big) .$$

This is the only possibility. An added constant would not change the field equation, and it is fixed by requiring $F(0) = 0$.

## Result 2: the two limits

**Strong fields.** For $y > 1$,

$$F(y) = y - 2\sqrt{y} + \ln y + \frac{2}{\sqrt{y}} - \frac{1}{y} + \cdots$$

The leading term is Newton's $y$, and $\mu \to 1$, so the field equation becomes Poisson's equation.

**Weak fields.** For $y \le 1$,

$$F(y) = \tfrac{2}{3}\,y^{3/2} - \tfrac{1}{2}\,y^2 + \tfrac{2}{5}\,y^{5/2} - \cdots$$

The leading term $\tfrac23 y^{3/2}$ is the deep-MOND energy, which gives flat rotation curves and the baryonic Tully–Fisher relation. No single term of the closed form produces it. Expanding the logarithm, the $\sqrt{y}$ pieces cancel and the $y$ pieces cancel among all three terms, and $\tfrac23 y^{3/2}$ is what survives. Both expansions are given in full, as convergent series, not only to leading order.

## Result 3: the field equation is well behaved

A natural question about any modified gravity is whether its field equation behaves as well as Poisson's: does matter determine the field uniquely? The proof answers yes for this constitutive law, in three steps.

**The energy is a bowl.** As a function of the field gradient, the energy density has curvature (its Hessian matrix) with two kinds of eigenvalue: $2\mu$ across the field direction and $2(x\mu)'$ along it. For $\mu(x) = x/(x+1)$ these are $2x/(1+x)$ and $2x(x+2)/(x+1)^2$, both positive wherever the field is nonzero. A function whose curvature is positive in every direction is *strictly convex*: shaped like a bowl, with no flat stretches and no second dip.

**The field equation is elliptic.** The same two numbers govern the field equation itself. Because both are positive, the equation is *elliptic*, the class to which Poisson's equation belongs, and the two never differ by more than a factor of two. Both vanish only where the field itself vanishes, where the equation degenerates in the same way as the deep-MOND equation.

**The field is unique.** Strict convexity makes the field equation's flux strictly monotone: stronger gradients always give more flux, in every direction. If two potentials solved the equation in a region with the same values on its boundary, subtracting the two equations and integrating would give the integral of a quantity that is positive wherever their gradients differ, and the integral would have to be zero. So their gradients are equal everywhere and the potentials coincide. On all of space, Bekenstein and Milgrom showed that the same condition, $(x\mu)' > 0$, gives a unique solution that falls off at infinity.

## Why it matters

- **It is the action-level form of the constitutive law.** The energy is what enters the GFD action and its covariant completion, so having it in closed form, with exact expansions, makes calculations explicit rather than numerical.
- **It answers a referee's first question about a modified field equation.** The field equation is elliptic and its solutions are unique. Not every interpolating function gives this so cleanly; here the two governing quantities stay within a factor of two of each other at every field strength.
- **It is pure mathematics.** Given the AQUAL action and the constitutive law, nothing in the proof depends on any further assumption.

## What it does not do

The proof does not derive the constitutive law; the [exchange-symmetry proof](../constitutive-law-exchange-symmetry/) does that. It does not treat the covariant (relativistic) theory, only the field equation of the weak-field limit. It proves uniqueness on a bounded region with given boundary values, and cites Bekenstein and Milgrom for all of space. It does not prove that a solution exists.

## Earlier versions

The closed form appears in the [RAR letter's supplement](../../papers/letter-radial-acceleration-relation-sparc/supplementary/supplementary_energy_functional_gravitational_constitutive_law.tex) and in the [closed-form energy functional paper](../../papers/closed-form-aqual-energy-functional/). Its integration is correct. This version changes four things:

- **The sign of the source term.** Both earlier versions write the Lagrangian with $+\rho\Phi$. That gives $\nabla\cdot(\mu\nabla\Phi) = -4\pi G\rho$, the wrong sign. Bekenstein and Milgrom's action has $-\rho\Phi$, used here, and the script checks both.
- **The low-acceleration limit.** The earlier abstract says the logarithm "dominates at low acceleration". It does not: the deep-MOND term arises from a cancellation among all three terms. The earlier body text describes this correctly; the abstract did not.
- **No novelty claim.** The earlier versions state that no closed form appears in the published literature. That is a claim about the literature for an elementary integral, easy to dispute and unnecessary, so it is dropped.
- **New results.** The full convergent expansions, convexity, ellipticity with the factor-of-two bound, and uniqueness are added.

## Contents

| File | Contents |
|---|---|
| [`aqual_energy_functional.pdf`](aqual_energy_functional.pdf) | The proof, two pages |
| [`aqual_energy_functional.tex`](aqual_energy_functional.tex) | LaTeX source (IOP journal class, included) |
| [`verify_aqual_energy_functional.py`](verify_aqual_energy_functional.py) | Checks of the Euler–Lagrange equation and its sign, the closed form, both series, the Hessian, the eigenvalue bound, monotonicity and the regularity used in the uniqueness proof |
| [`iopjournal.cls`](iopjournal.cls) | Document class, so the source builds here |

```bash
pip install sympy numpy
python verify_aqual_energy_functional.py      # 24/24
pdflatex -interaction=nonstopmode aqual_energy_functional.tex
```

## Related

- [The constitutive law from exchange symmetry](../constitutive-law-exchange-symmetry/): the derivation of $\mu(x) = x/(x+1)$.
- [The radial acceleration relation letter](../../papers/letter-radial-acceleration-relation-sparc/): the action tested on 164 SPARC galaxies.
- [Letter 3 supplement: covariant completion](../../papers/letter-3-field-closure-of-tetrad-frame/Supplementary/supplementary_covariant_completion.tex): the energy in the covariant action.

---

*The algebra is complete and machine-checked. The result holds for any theory that adopts $\mu(x) = x/(x+1)$ in the AQUAL framework.*
