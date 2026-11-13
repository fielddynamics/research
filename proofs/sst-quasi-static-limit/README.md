# The SST Covariant Completion in Its Quasi-Static Limit

*What the four-term covariant action gives where galaxies are observed · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`SST` `covariant-action` `AQUAL` `constitutive-law` `radial-acceleration-relation` `Tully-Fisher` `lensing` `proof`

---

This folder holds a three-page proof and a script that checks every step (26 checks, exact algebra). It was revised after an internal referee-style review ([`referee_review.md`](referee_review.md)). The SST (scalar-tensor transition) is GFD's four-term covariant action:

$$S = \int d^4x\,\sqrt{-g}\left[\frac{R}{16\pi G} - \frac{a_0^2}{8\pi G}F(y) - \frac14 e^{-2\Phi/c^2}F_{\mu\nu}F^{\mu\nu} + \mathcal L_{\rm matter}\right],\qquad F(y) = y - 2\sqrt y + 2\ln(1+\sqrt y).$$

The proof derives, exactly, what this action gives in the quasi-static weak field: the regime of rotation curves, the Tully–Fisher relation and galaxy lensing.

## How the action is read

The proof takes the SST as written, with the framework's own reading from Letter 3 and its covariant-completion supplement:
1. **Φ is gravity's own potential.** It is the Newtonian potential of the metric, not a new field. The constitutive law changes its response, and the TetB share 1 − μ is carried inside F.
2. **The terms divide the work.** The curvature term carries the tensor sector, so gravitational waves travel at c. Φ's response is carried by F.
3. **The static weak field.** Matter enters through −ρΦ, the weak-field form of minimal coupling when Φ is the metric potential, and e^{−2Φ/c²} → 1.
4. **μ applies to a galaxy's net field, not to each mass.** Bound systems such as the solar system are pure TetA, i.e. general relativity (Coles Notes §5.4).

**Lemma 1 states reading (2) exactly.** In the static weak field the curvature term's part is (1/8πG)[(∇Ψ)² − 2∇Φ·∇Ψ], which on Ψ = Φ is the Newtonian energy −(a₀²/8πG)y. So under reading (2) the static Lagrangian is that curvature part plus −(a₀²/8πG)[F(y) − y] − ρΦ: the curvature term supplies the y, and F supplies the rest. On Ψ = Φ this is −(a₀²/8πG)F(y) − ρΦ, the energy the archive varies. The −ρΦ source is minimal coupling, from −mc²√(−g₀₀).

**Naming.** "SST" names the action. The quadratic g_s = g_t²/(a₀ + g_t) is its spherical field equation. The documentation calls the capacity function f(x) = (21x+13)/(x+1) "the field equation"; Theorem 2 shows these are one equation.

## Results

| Theorem | Result |
|---|---|
| 1. The field equation | From Lemma 1: the Ψ-equation is ∇²(Φ − Ψ) = 0, so Ψ = Φ and γ = 1 at leading order. The Φ-equation is ∇·[μ(\|∇Φ\|/a₀)∇Φ] = 4πGρ, with μ = x/(x+1) |
| 2. The capacity form | f(x) = 17 + 4σ(x) = (21x+13)/(x+1) takes 13, 17, 21 at x = 0, 1, ∞, and μ = (f − 13)/8: the same field equation written through the coupling polynomial |
| 3. The spherical field equation | It integrates exactly to the conserved flux r²μg_t = GM, i.e. g_s = g_t²/(a₀ + g_t). The forward solver g_t = ½[g_s + √(g_s² + 4g_sa₀)] is the unique positive root, and the decoder M_dec = rv⁴/[G(a₀r + v²)] is its exact inverse |
| 4. Limits and scales | See the list below this table |
| 5. Well-posedness | The energy is strictly convex; the field equation is elliptic (anisotropy 1 + (1 − μ) ∈ [1, 2], the TetB share), and its solution is unique |
| 6. The single potential | Since Ψ = Φ, light is deflected by the same Φ that sets the dynamics (Born approximation). A point mass deflects light by 4GM/(bc²) and the deep field by 2π√(GMa₀)/c². Lensing mass equals dynamical mass. The EM factor differs from 1 by ~10⁻⁶ in a galaxy |

Theorem 4 in full:
- **Newtonian limit:** g_t = g_s + a₀ − a₀²/g_s + ….
- **Deep limit:** g_t = √(g_sa₀) + g_s/2 + ….
- **Baryonic Tully–Fisher:** v⁴ → GMa₀ exactly.
- **The TetB share is bounded:** it equals a₀μ, which is always less than a₀.
- **The transition ring:** μ = ½ at r = √(2GM/a₀).
- **The phantom density:** √(GMa₀)/(4πGr²) far out.

Theorems 3 and 4 are what the SPARC radial acceleration relation, the Tully–Fisher relation and the mass decoder test.

**A remark on reading (2).** The static weak-field part of R/16πG is the Newtonian energy of Φ. If it were counted for Φ as well as F, the equations would give ∇·[(1 + μ)∇Φ] = 4πGρ. So the SST's field equation is the one in which Φ's response is carried by F alone, which is what the archive states. The proof uses that reading throughout.

## What a referee would ask, and the answers

The internal review ([`referee_review.md`](referee_review.md)) raised four major points:
1. **"Reading (2)" is not a property of an action.** It is now Lemma 1, an exact identity for the static Lagrangian.
2. **γ = 1 was posited.** It is now derived at leading order from the curvature term's Ψ-equation.
3. **The matter coupling wasn't shown.** −ρΦ now follows from minimal coupling, −mc²√(−g₀₀).
4. **Prior work.** The standard AQUAL results are attributed. What's new is the derivation from the SST's own terms.

Minor points:
- the static frame is needed to define |∇Φ|²;
- the deflections use the Born approximation;
- Tully–Fisher holds for an isolated mass, with an external field effect otherwise;
- uniqueness needs boundary conditions;
- the remark on Paper I's processing boundary is rephrased neutrally.

## What it leaves open (as the Coles Notes record)

- **The metric field equations** beyond leading order, including the stress–energy of the F sector, have not been solved.
- **ℒ_matter** is specified here only in its weak-field form.
- **The covariant meaning of y.** The limit uses the static frame. As a spacetime scalar, y would need Φ to be a scalar field, and its covariant form for time-dependent and strong fields is open.
- **The fourth term has three descriptions in the documents:** disformal and needed for lensing; conformal with a cosmological role; an auxiliary vector field. The variation of α with the potential that it implies is not discussed.
- **The bimetric match.** The match from the locked bimetric theory to μ is open.
- **Paper I's processing boundary.** Paper I's √(GM/a₀) is where x = φ = (1+√5)/2, not where x = 1. The ring μ = ½ is at √(2GM/a₀).

## Contents

| File | Contents |
|---|---|
| [`sst_quasi_static.pdf`](sst_quasi_static.pdf) | The proof, three pages, Lemma 1, Theorems 1–6 and the Remark |
| [`referee_review.md`](referee_review.md) | The internal referee-style review and the response to each point |
| [`sst_quasi_static.tex`](sst_quasi_static.tex) | LaTeX source (IOP journal class, included) |
| [`verify_sst_quasi_static.py`](verify_sst_quasi_static.py) | Checks for every step: Lemma 1's identity, the Ψ- and Φ-equations, minimal coupling; F′ = μ; the Euler–Lagrange equation of the static action; the capacity form; the spherical divergence and flux; the quadratic, solver and decoder; both limits; Tully–Fisher; the TetB bound; the ring and φ; the phantom density; the Hessian; the deflections; lensing = dynamical mass; the EM factor; and the Remark |
| [`iopjournal.cls`](iopjournal.cls) | Document class, so the source builds here |

```bash
pip install sympy
python verify_sst_quasi_static.py      # 26/26
pdflatex -interaction=nonstopmode sst_quasi_static.tex
```

## Related

- [Letter 3](../../papers/letter-3-field-closure-of-tetrad-frame/) and its covariant-completion supplement: the action, the reading of Φ, γ = 1.
- [The energy functional of the constitutive law](../aqual-energy-functional/): F, convexity, uniqueness.
- [The constitutive law from exchange symmetry](../constitutive-law-exchange-symmetry/): μ = x/(x+1).
- [The RAR letter](../../papers/letter-radial-acceleration-relation-sparc/) and [the decoding-mass letter](../../papers/letter-decoding-mass-from-rotation-curves/): the spherical field equation on SPARC, and its inverse.
- [`docs/02-gravitation/`](../../docs/02-gravitation/): the field equation (capacity form) and the covariant completion.
