# AQUAL

*The scalar sector of the covariant action: the constitutive law, its energy functional, the field equation and the bound law · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`aqual` `mond` `constitutive-law` `interpolating-function` `energy-functional` `qumond` `modified-poisson-equation` `gravity`

---

The GFD covariant action carries a scalar sector, $-(a_0^2/8\pi G)\,F(y)$ with $y = |\nabla\Phi|^2/a_0^2$, in the form of Bekenstein and Milgrom's AQUAL (1984). The AQUAL identity $\mu(\sqrt y) = dF/dy$ ties the energy functional $F$ to the constitutive law $\mu$. Varying the action gives the modified Poisson equation:

$$\nabla\cdot\big[\mu(|\nabla\Phi|/a_0)\,\nabla\Phi\big] = 4\pi G\rho, \qquad \mu(x) = \frac{x}{x+1}, \qquad F(y) = y - 2\sqrt y + 2\ln(1+\sqrt y).$$

Two statements must be kept apart:

- **The constitutive law** $\mu(x)$ is kinematic: the TetA share of the field at acceleration $x = g/a_0$.
- **The spherical-static limit of the field equation**, $g_s = g_t^2/(a_0 + g_t)$, is dynamic: it comes from varying the action.

They are algebraically identical and connected by $\mu = dF/dy$. They are not the same statement.

The AQUAL material in the archive is spread across proofs, letters, papers and research notes. This folder gathers it in one place:

- a map of where each piece already lives;
- the work that carries the algebra further, connecting the unbound law, its inverse, the bound law of the nuclear papers and the energy functional;
- two verification scripts.

## Terms

| Term | Meaning | Source |
|---|---|---|
| TetA | The exterior: the observable disk, our spacetime, in which the baryons orbit as tracers of the flow | [Decoding-mass letter](../../papers/letter-decoding-mass-from-rotation-curves/) |
| Deep field | The low-acceleration regime $x \ll 1$, where $\mu \to x$. A range of $x$, reached toward a galaxy's rim, in the exterior; not TetB | Paper VII; Letter 2 |
| TetB | The interior: the subspace reached only through the Field Origin. In a galaxy it lies beyond the throat at the centre, and matter spiralling inward through the throat passes into it, so a galaxy's TetB is occupied. Only an individual unbound envelope, a tile of the long-range mesh, has an empty TetB | [Decoding-mass letter](../../papers/letter-decoding-mass-from-rotation-curves/); Paper VII; [`bound-gravity-and-packing/`](../bound-gravity-and-packing/) |
| Unbound law | The one-directional law $x(1-\mu) = \mu$. It governs a galaxy's exterior field; the name refers to the law, not to the state of the galaxy's interior | [`bound-gravity-and-packing/`](../bound-gravity-and-packing/) |
| TetB share | $1 - \mu$, the fraction of the coupling capacity resolved through TetB; part of the quiet prediction | Paper VII, the constitutive law from detailed balance |
| $s$ and $\sigma(x)$ | $s$ is the coupling polynomial's state label: $+1$ TetA, $0$ Field Origin, $-1$ TetB. $\sigma(x) = \mu - (1-\mu)$ is the share difference at acceleration $x$. $\sigma(x)$ takes the label values without being those states: $\sigma = 0$ on the ring $x = 1$, which is not the Field Origin, and $\sigma \to -1$ in the deep field, which is not TetB | This folder |
| Interior's active contribution | $\Delta M_{\text{eff}} = M_{\text{phot}} - M_{\text{dec}}$: zero when the interior is quiet, otherwise drive or brake. Not the TetB share | Decoding-mass letter; [`what_is_gravity.md`](../g_from_topology/what_is_gravity.md) §7 |

Some archive texts equate the deep field with TetB ("the deep-field limit … is itself the TetB sector", constitutive-law letter, lines 404–411; "TetB (deep field)", galaxy interior/exterior synthesis; "Deep field (TetB dominant)", docs 02 and 03). This folder keeps the three terms separate.

## Reading order

1. **The archive's foundations** (see the map below). Start with the three derivations of $\mu$, then the [energy-functional proof](../../proofs/aqual-energy-functional/): closed form, convexity, ellipticity and uniqueness.
2. [`aqual_algebra_further.md`](aqual_algebra_further.md), *The AQUAL Algebra, Taken Further*. Its sections:

| § | Result |
|---|---|
| 1 | The constitutive law and the field equation as one algebra in three forms; the TetB share of the field is $a_0\mu$ |
| 2 | The bound law is the exchange image of the source form |
| 3 | The logistic family |
| 4 | The field equation's anisotropy equals the TetB share |
| 5 | The logarithm in $F$ is the screening identity integrated |
| 6 | The mean coupling of 17 follows from exchange symmetry |
| 7 | Closed forms: the Legendre dual of the energy density (QUMOND's kinetic function), the bound kinetic function, the point-mass potential |
| 8 | A check on the central density inferred from the TetB share |
| 9–10 | The point mass and the bound law in one hyperbolic variable |
| 11 | Two operations generate the laws; uniqueness within the family |
| 12 | The partition composes like rapidities |
| 13 | Why general relativity never meets 13, 17 and 21: the coupling polynomial is a trace over $\mathrm{Sym}^2 \oplus \Lambda^2$, the constitutive law weights the two sectors, and GR sits at the endpoint $\mu = 1$ |

3. [`docs_and_the_energy_functional.md`](docs_and_the_energy_functional.md), *The Docs and the Energy Functional*. What the documentation and the docs-site tests derive from $F$, read against this folder: what agrees, nine statements the algebra does not support, and suggested edits (not made).

## Map: where the AQUAL material lives

| Topic | Where | What it establishes |
|---|---|---|
| $\mu$ from exchange symmetry | [`proofs/constitutive-law-exchange-symmetry/`](../../proofs/constitutive-law-exchange-symmetry/) | Endpoint, exchange closure and degree one force $x(1-\mu) = \mu$ |
| $\mu$ by three routes | [`papers/letter-constitutive-law-tetrad-geometry/`](../../papers/letter-constitutive-law-tetrad-geometry/) | The metric read, exchange symmetry, and equilibrium closure ([detailed balance](../../papers/letter-constitutive-law-tetrad-geometry/Supplementary/supplementary_equilibrium_route.tex)) |
| $F(y)$, convexity, uniqueness | [`proofs/aqual-energy-functional/`](../../proofs/aqual-energy-functional/) | Closed form; Hessian eigenvalues $2\mu$, $2(x\mu)'$; ellipticity; uniqueness on bounded domains |
| $F(y)$ as a standalone result | [`papers/closed-form-aqual-energy-functional/`](../../papers/closed-form-aqual-energy-functional/) | The closed form for any AQUAL theory using this $\mu$ |
| The action and the field equation | [Paper VII](../../papers/07-dual-tetrad-topology-field-origin/v7/), [`docs/02-gravitation/06-covariant-completion.md`](../../docs/02-gravitation/06-covariant-completion.md), [`05-poisson-scale-invariance.md`](../../docs/02-gravitation/05-poisson-scale-invariance.md) | The four-term action; the modified Poisson equation |
| Einstein's equation as the TetA partition | [`EINSTEIN_TETA_PARTITION.md`](../../EINSTEIN_TETA_PARTITION.md), [Letter 3](../../papers/letter-3-field-closure-of-tetrad-frame/) | $\mu = 1$ recovers GR; the TetB share as the discrepancy |
| The radial acceleration relation | [`papers/letter-radial-acceleration-relation-sparc/`](../../papers/letter-radial-acceleration-relation-sparc/) | 3,284 points in 164 SPARC galaxies, no free parameter |
| The inverse pipeline | [`papers/letter-decoding-mass-from-rotation-curves/`](../../papers/letter-decoding-mass-from-rotation-curves/) | $M_{\text{dec}} = rv^4/[G(a_0r + v^2)]$ |
| The bound law $x(1-\mu)^2 = \mu$ | [Paper XIII](../../papers/13-nuclear-binding-bidirectional-sst/), [Paper XI](../../papers/11-nuclear-shells-tetrahedral-packing/), [`bound-gravity-and-packing/`](../bound-gravity-and-packing/) | Nuclear binding; the golden ratio at the gate |
| The bound law as bimetric screening | [Paper VIII](../../papers/08-gfd-and-bimetric-gravity/) | The $N = 2$ law, $\mu = (\sqrt{1+4x}-1)/(\sqrt{1+4x}+1)$; equal to $\tanh^2(\psi/2)$ of §10 here |
| The algebraic chain to $F$ | [`algebraic_pipeline_of_reality.md`](../../papers/algebraic-papers-a-b-c/algebraic_pipeline_of_reality.md) | $D = 3$ through the partition law to $F$ and the logistic equation |
| Suites and visualisations | [`constitutive-law-u(x)/`](<../constitutive-law-u(x)/>) | Test suites and the TetA/TetB roulette |
| The documentation | [`docs/02-gravitation/`](../../docs/02-gravitation/), [`docs/04-galactic-dynamics/`](../../docs/04-galactic-dynamics/); site tests in [`fielddynamics/docs`](https://github.com/fielddynamics/docs) | The reader-facing account of $F$ and its consequences; read against this folder in `docs_and_the_energy_functional.md` |

## What is established, and what is open

| Result | Status |
|---|---|
| $\mu(x) = x/(x+1)$ | Derived by three routes in the archive |
| $F(y)$, convexity, ellipticity, uniqueness | Proved in the archive |
| The forms and identities of `aqual_algebra_further.md` | Exact; checked twice (below) |
| Pointwise forms (1a)–(1c) beyond spherical, cylindrical and planar symmetry | Approximate in GFD's field equation, which has the AQUAL form (the curl term); exact only in QUMOND, which is a separate action |
| The bound law as the exchange of the source form | Exact identity; its physical reading is open |
| Letter 3's "bounded central density" | The acceleration bound holds; the density has a cusp (§8) |
| How nested closures compose (§12) | Open; the algebra does not decide it |
| How matter couples to $\Phi$ in the action | Not stated in the docs; needed for the scalar equation to have a source |
| Whether $y$ is covariant, and $F$ for timelike gradients | Open; if covariant, waves along a static field travel at $c\sqrt{2-\mu}$ |
| One relation between $a_0$ and $H$ | Two are in use, differing by $\sqrt{4/\pi}$ |

## Running

```bash
pip install sympy mpmath
python verify_aqual_algebra.py     # 50/50, each claim by its own algebra
python verify_independent.py       # 48/48, by routes that do not reuse the closed forms
python verify_docs_intersection.py # 23/23, the docs read against this folder
```

The independent script evaluates every identity at random points to 60 digits. It also:

- solves the field by root-finding and quadrature;
- computes the Legendre dual as a numerical supremum;
- takes the Hessian by finite differences in three dimensions;
- tests the QUMOND vector form on random non-spherical fields;
- checks the law family for irreducibility and root counts.

## Contents

| File | Contents |
|---|---|
| [`aqual_algebra_further.md`](aqual_algebra_further.md) | The AQUAL algebra carried further: twelve sections, with status and verification |
| [`verify_aqual_algebra.py`](verify_aqual_algebra.py) | Direct verification, symbolic and exact |
| [`verify_independent.py`](verify_independent.py) | Independent verification, numerical and symbolic by separate routes |
| [`docs_and_the_energy_functional.md`](docs_and_the_energy_functional.md) | The documentation's account of $F$ and its consequences, read against this folder |
| [`verify_docs_intersection.py`](verify_docs_intersection.py) | Verification for the docs note |

## References

- Bekenstein, J. and Milgrom, M. (1984). Does the missing mass problem signal the breakdown of Newtonian gravity? *Astrophys. J.* 286, 7.
- Milgrom, M. (2010). Quasi-linear formulation of MOND. *Mon. Not. R. Astron. Soc.* 403, 886.
- Babichev, E., Mukhanov, V. and Vikman, A. (2008). k-Essence, superluminal propagation, causality and emergent geometry. *J. High Energy Phys.* 2008(02), 101.
