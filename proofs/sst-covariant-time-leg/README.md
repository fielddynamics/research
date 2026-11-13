# The SST Covariant Completion: y From the Acceleration of the Time Leg

*The covariant definition of the SST's y, and what it settles · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`SST` `covariant-action` `tetrad` `time-leg` `acceleration` `khronometric` `preferred-foliation` `MOND` `proof`

---

This folder holds a four-page proof and a script that checks every step (16 checks, exact algebra). It is the companion to [`../sst-quasi-static-limit/`](../sst-quasi-static-limit/), whose Scope left three points open:

1. **The covariant form of y.** The archive writes y = |∇Φ|²/a₀², which is defined in the static frame.
2. **F for y < 0.** A scalar gradient ∇_μΦ∇^μΦ can be timelike.
3. **The metric field equations**, and the status of Φ's stress–energy.

One definition settles all three:

$$y \equiv \frac{c^4\,a_\mu a^\mu}{a_0^2},\qquad a^\mu = u^\nu\nabla_\nu u^\mu,\quad u = e_0 .$$

Here e₀ is the tetrad's time leg, taken normal to GFD's time foliation, and a is its acceleration: what an accelerometer at rest in that foliation reads.

## Results

| Theorem | Result | Open point |
|---|---|---|
| 1. Covariance and positivity | y is a spacetime scalar. a·u = 0, so a is spacelike or zero, and **y ≥ 0 for every configuration**. F needs no timelike branch | 2 |
| 2. The static reduction | For −N²c²dt² + h, a_i = ∂_i ln N exactly. With N = e^{Φ/c²}, **c²a_i = ∂_iΦ** and y = h^{ij}∂_iΦ∂_jΦ/a₀², which is \|∇Φ\|²/a₀² in the weak field. **Φ is the lapse potential of the metric**, not a separate field | 1 |
| 3. The covariant SST | **The SST is taken exactly as written.** Varied as the framework varies it (Lemma 1 of the quasi-static proof: the curvature term supplies the Newtonian part y of F), it has the field equations of Blanchet–Marsat's preferred-foliation theory with their function **f = a₀²[F(y) − y]**, and μ_total = 1 + f′/2a = **x/(x+1) exactly**. Its static weak field gives Ψ = Φ (γ = 1) and ∇·[μ∇Φ] = 4πGρ | 1, 3 |
| 4. The metric equations | Einstein's equation with the time-leg stress tensor as extra source, plus the foliation's equation. There is **no separate scalar stress tensor**, because Φ is the lapse. The 00-equation is ∇²Φ = 4πG(ρ + ρ_ph), the TetB share as phantom density. The time-leg energy is the gravitational field energy, v²/2c² times ρ_ph (about 2 × 10⁻⁷ at 200 km/s) | 3 |
| 5. The cosmological background | The comoving time leg of FLRW is geodesic, so a = 0, y = 0, F(0) = 0: **the background is exactly GR**, and the SST acts on perturbations | — |
| 6. The two limits of f | Deep field: f = −a² + 2a³/3a₀ + …, the MOND condition. Strong field: f = −2a₀a + 2a₀² ln(a/a₀) + …, which does **not** tend to a constant, so (1 − μ)g → a₀ | — |

## What Theorem 6 means for the solar system

The covariant form makes one point precise that the archive already states in words.

**On each mass's own time leg, the action leaves a TetB tail (1 − μ)g → a₀ around every star.** At Saturn (x ≈ 5 × 10⁵) the tail is a₀ to two parts in 10⁶. This is exactly the per-mass tail that the archive records as excluded:
- a constant extra pull ≈ a₀ at every planet, excluded by perihelia;
- a Sun-centred quadrupole, excluded by Cassini.

See Coles Notes §5.4 and [`research/bimetric-projection/`](../../research/bimetric-projection/) Part 3.

The archive therefore applies μ to the galaxy's net field, never to a star's own field. In covariant terms that rule says: **a is the acceleration of the coarse-grained time leg**, the frame of the galaxy's net field, and bound subsystems gravitate internally through R alone. The SST with a taken from each mass's own time leg does not implement this. An action that does (for example, one that defines the coarse-graining covariantly) is the open step. Nothing about galaxies changes: on galactic scales the coarse-grained field is the field the SPARC fits use, and Theorems 1–5 hold there.

## Prior work

The theory (1/16πG)√−g[R − 2f(a)], with a the acceleration of a unit timelike field normal to a preferred foliation, is due to:
- Blanchet & Marsat, *Modified gravity approach based on a preferred time foliation*, arXiv:1107.5264;
- Blanchet & Marsat, *Relativistic MOND theory based on the Khronon scalar field*, arXiv:1205.0400.

Related constructions:
- Sanders, Hořava-type MOND, arXiv:1105.3910;
- Zlosnik, Ferreira & Starkman, generalized Einstein-aether MOND;
- Blas, Pujolàs & Sibiryakov, khronometric theory.

What this note adds:
- the identification of the SST's y with the acceleration of the tetrad's time leg;
- the correspondence: the SST as written, varied as in Lemma 1, has that theory's field equations with f = a₀²[F(y) − y], which gives the archive's μ exactly;
- Φ as the lapse;
- the strong-field limit of this f and what it means for the net-field rule;
- machine checks of every step.

## What it leaves open

- **The net-field mechanism** (Theorem 6).
- **Preferred-frame effects.** A preferred foliation breaks local Lorentz invariance. PPN α₁, α₂ and the khronon's dynamics and stability are not computed for this f. In Blanchet–Marsat, GR is recovered above a₀ because f → constant there; this f does not, so these must be computed with the net-field rule in place.
- **Signal speeds.** The action has no (∇u)² shear or expansion terms, so the curvature term carries the tensor modes. The scalar-sector speed c√(2 − μ) found earlier assumed Φ is a covariant scalar, and it needs redoing with Φ as the lapse.
- **The fourth term.** With Φ = c² ln N, e^{−2Φ/c²} is defined relative to the foliation's normalized time. Its coefficient α remains open.
- **A general time leg.** If e₀ is not hypersurface-orthogonal, the theory is of generalized Einstein-aether type, with a vorticity sector not treated here.

## Contents

| File | What it is |
|---|---|
| [`sst_covariant_time_leg.pdf`](sst_covariant_time_leg.pdf) | The proof (4 pages) |
| [`sst_covariant_time_leg.tex`](sst_covariant_time_leg.tex) | LaTeX source (IOP class, [`iopjournal.cls`](iopjournal.cls)) |
| [`verify_sst_covariant_time_leg.py`](verify_sst_covariant_time_leg.py) | 16 checks: sympy exact algebra (Christoffel symbols and accelerations computed from the metric), plus one random-point positivity check on a time-dependent metric |
| [`referee_review.md`](referee_review.md) | Internal referee-style review and responses |

## Running the checks

```
python verify_sst_covariant_time_leg.py
```

It needs sympy and takes about a minute. It ends with `16/16 checks passed`.
