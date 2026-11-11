# The Two-Potential Energy of the Constitutive Law in Bimetric MOND

*How the constitutive law $\mu(x) = x/(x+1)$ fixes the free function of Milgrom's bimetric MOND, and why the second metric enters with the opposite sign · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`BIMOND` `QUMOND` `AQUAL` `MOND` `bimetric-gravity` `Legendre-duality` `proof`

---

This folder holds a short proof and a script that checks every step. It is the companion to the [AQUAL energy functional proof](../aqual-energy-functional/). That proof gives the energy of $\mu(x) = x/(x+1)$ when gravity has one potential. This one gives the energy when gravity has two, as in Milgrom's bimetric MOND. This page explains the argument for a reader with first-year calculus.

## The setting

In 2009 Milgrom proposed **bimetric MOND (BIMOND)**, a relativistic theory with two metrics. Ordinary matter feels one; a hypothetical "twin matter" feels the other. At low speeds there are two potentials: $\phi$, felt by matter, and $\hat\phi$, felt by twin matter. Their difference is $\phi^* = \phi - \hat\phi$.

The theory has two free choices:

- **The ratio of the two gravitational couplings**, $\alpha$ for the second metric and $\beta$ for the first.
- **An interaction function** $\mathcal{M}$. Milgrom calls it "an a priori unspecified function", to be fixed by phenomenology or by a deeper theory. Only its two limits are fixed: its derivative must vanish at high acceleration and grow like $z^{-1/4}$ at low acceleration.

Milgrom singles out $\alpha + \beta = 0$ because it makes the equations simple, and leaves $\mathcal{M}$ open. This proof shows that both choices are fixed.

## Result 1: why the couplings must be opposite

Combine the two field equations so that $\hat\phi$ drops out. What remains is an equation for $\phi^*$ whose coefficient is $\alpha\beta - (\alpha + \beta)\mathcal{M}'$. That coefficient is a constant, making $\phi^*$ an ordinary Newtonian potential, **if and only if $\alpha + \beta = 0$**.

Otherwise the interaction leaks into $\phi^*$ itself. In the special case the equations become Milgrom's quasilinear MOND (QUMOND): two Poisson equations, the second sourced by the first.

**Lemma 1** supplies the sign from geometry. Written with a tetrad (a frame of four vectors), the Einstein–Hilbert term is $\det(e)\,R$, not $|\det e|\,R$. The metric is unchanged when the frame is reflected, but the determinant flips sign. The tetrad equation has two roots, $\det e = \pm\sqrt{-g}$, exchanged by spatial parity (see the [two bounded regions proof](../tetrad-scheme-two-bounded-regions/)). So a second metric carried by a frame on the negative root, with the same coupling, enters with the opposite sign: $\beta = 1$, $\alpha = -1$.

## Result 2: the interaction function in closed form

Require BIMOND to reproduce the constitutive law: around any spherical mass its field should be the one AQUAL gives with $\mu(x) = x/(x+1)$. That fixes the derivative of $\mathcal{M}$. Requiring $\mathcal{M}(0) = 0$ then fixes $\mathcal{M}$ itself:

$$\mathcal{M} = 2x - 1 + 2b - b^2 + 2\ln b, \qquad b = \frac{1}{1+x},$$

where $x$ is the total field in units of $a_0$ and $b = 1 - \mu$. The same function written in the Newtonian field $y$ is

$$\mathcal{M} = \tfrac12\sqrt y\,(y+2)\sqrt{y+4} - \tfrac12 y^2 - 4\,\mathrm{arsinh}\big(\tfrac12\sqrt y\big).$$

The derivation mirrors the AQUAL proof. There, a long division turned the integrand into simple fractions. Here the key fact is that the total field splits as $x = y + \mu(x)$, so the slope of $\mathcal{M}$ is just $2\mu$. One partial-fraction step finishes the integral.

**Corollary 1** checks the limits:
- $\mathcal{M}' \to 0$ at high acceleration.
- $\mathcal{M}' = z^{-1/4} - \tfrac12 + \dots$ at low acceleration, with coefficient exactly 1 and nothing to tune.

These are Milgrom's two conditions, which he imposed by hand, met exactly.

## Result 3: the two energies are mirror images

The AQUAL energy $F$ (one potential) and the BIMOND energy $y^2 + \mathcal{M}$ (two potentials) are **Legendre transforms** of each other:

$$F(x^2) + y^2 + \mathcal{M} = 2xy .$$

This is the same relation that links energy and free energy in thermodynamics, or a Lagrangian and its Hamiltonian. Two details stand out:

- **The logarithm passes between them.** $F$ contains $-2\ln b$ and $\mathcal{M}$ contains $+2\ln b$, so the logarithms cancel in the sum.
- **The second field never exceeds $a_0$.** In spherical symmetry its strength is $a_0\,\mu(x)$.

**Corollary 2** shows the BIMOND energy is a strict bowl (strictly convex). Its curvature along the field and across it stand in the ratio $(x+1)/(x+2)$, exactly the reciprocal of the AQUAL ratio. A Legendre transform inverts curvature, and this is that inversion. The field equations have at most one solution for given boundary values.

## Why it matters

- **It removes BIMOND's free function.** For fifteen years $\mathcal{M}$ has been "a priori unspecified". Given $\mu(x) = x/(x+1)$, which the [exchange-symmetry proof](../constitutive-law-exchange-symmetry/) derives, there is exactly one $\mathcal{M}$, and it is written above.
- **It gives the sign of the second metric a reason.** Milgrom chose $\alpha + \beta = 0$ because it simplifies the equations. Here it is the only case in which the Newtonian potential stays Newtonian. In the tetrad form, it is what a frame on the second root contributes.
- **It connects GFD to an existing relativistic theory.** BIMOND has a covariant action, so this places GFD's constitutive law inside a relativistic two-metric framework that already exists in the literature.

In GFD terms, $\phi^*$ is the TetA field, $\hat\phi$ is the TetB field, and $\phi$ is the total. The research behind this reading, including where it works and where it does not, is in [`research/bimond-gfd/`](../../research/bimond-gfd/). The proof itself uses none of that interpretation.

## What it does not do

- It does not derive $\mu$; the [exchange-symmetry proof](../constitutive-law-exchange-symmetry/) does that.
- It treats only the low-speed (nonrelativistic) limit of BIMOND. It does not treat the full relativistic theory, its stability (the opposite-sign second metric raises the question of ghosts), gravitational waves, or BIMOND's second free function $f(\kappa)$.
- Lemma 1 rests on a stated premise. The second metric is carried by a frame on the negative root, with the same coupling, and the Einstein–Hilbert term is taken in its tetrad form $\det(e)\,R$. The metric form $\sqrt{-g}\,R$ would not see the sign.
- It makes no novelty claim for the Legendre duality as such. AQUAL and QUMOND are known to agree for spherical systems, and that is a standard convex duality. What is shown here is the closed form for this $\mu$, its derivation, and its properties.
- It proves uniqueness, not existence, and only on a bounded region.

## Contents

| File | Contents |
|---|---|
| [`bimetric_two_potential_energy.pdf`](bimetric_two_potential_energy.pdf) | The proof, three pages |
| [`bimetric_two_potential_energy.tex`](bimetric_two_potential_energy.tex) | LaTeX source (IOP journal class, included) |
| [`verify_bimetric_two_potential_energy.py`](verify_bimetric_two_potential_energy.py) | Checks of the Euler–Lagrange equations, the $\hat\phi$-free combination and its coefficient, the parity sign of the tetrad term, the inverse function $\nu$, the integral and both closed forms of $\mathcal{M}$, both limits, the Legendre identity and maximum, the cancelling logarithms, the Hessian and its reciprocal ratio, and monotonicity |
| [`iopjournal.cls`](iopjournal.cls) | Document class, so the source builds here |

```bash
pip install sympy numpy
python verify_bimetric_two_potential_energy.py      # 39/39
pdflatex -interaction=nonstopmode bimetric_two_potential_energy.tex
```

## Related

- [The energy functional of the constitutive law](../aqual-energy-functional/): the one-potential (AQUAL) energy, whose Legendre dual this is.
- [The constitutive law from exchange symmetry](../constitutive-law-exchange-symmetry/): the derivation of $\mu(x) = x/(x+1)$.
- [The tetrad scheme and the two bounded regions](../tetrad-scheme-two-bounded-regions/): the two roots of the tetrad equation, used in Lemma 1.
- [`research/bimond-gfd/`](../../research/bimond-gfd/): the research notes on BIMOND and GFD, including local systems and the brake/drive question.
- M. Milgrom, [Bimetric MOND gravity](https://arxiv.org/abs/0912.0790) (2009); [Quasi-linear formulation of MOND](https://arxiv.org/abs/0911.5464) (2010); [Matter and twin matter in bimetric MOND](https://arxiv.org/abs/1001.4444) (2010).

---

*The algebra is complete and machine-checked. Theorems 1–3 and the corollaries hold for any theory that adopts $\mu(x) = x/(x+1)$ in nonrelativistic BIMOND. Lemma 1 adds the tetrad premise stated above.*
