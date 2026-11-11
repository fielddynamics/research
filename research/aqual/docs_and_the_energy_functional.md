# The Docs and the Energy Functional

*What the documentation derives from the AQUAL energy functional, read against the algebra of this folder · Field Dynamics Research · working note, November 2026*

---

## What was read

**Research repository.** These pages use $F(y) = y - 2\sqrt y + 2\ln(1+\sqrt y)$ or what follows from it:

| Page | What it contains |
|---|---|
| [`02-field-equation.md`](../../docs/02-gravitation/02-field-equation.md) | the capacity function $f(x)$ |
| [`03-constitutive-law-mu-x.md`](../../docs/02-gravitation/03-constitutive-law-mu-x.md) | the constitutive law, $v^4 = GM(g + a_0)$, the decode, the comparison with other interpolating functions |
| [`05-poisson-scale-invariance.md`](../../docs/02-gravitation/05-poisson-scale-invariance.md) | the modified Poisson equation |
| [`06-covariant-completion.md`](../../docs/02-gravitation/06-covariant-completion.md) | the action, $F$ and its three terms, the limits |
| [`04-galactic-dynamics/`](../../docs/04-galactic-dynamics/) | rotation curves, the decode, the RAR |
| [`07-characteristic-scale.md`](../../docs/01-foundations/07-characteristic-scale.md), [`05-h0-prediction.md`](../../docs/03-fundamental-constants/05-h0-prediction.md) | the scale $a_0$ and its relation to $H$ |

**The docs site** ([`fielddynamics/docs`](https://github.com/fielddynamics/docs)).

- Its covariant-completion page is identical to the research copy.
- What the site adds is tests: `covariant_completion/tests/validate.py` (22 checks) and `validate-extended.py` (41 checks). These carry the docs' claims about $F$: convexity, ghost freedom, subluminality, the Legendre transform, the Hamiltonian bound and uniqueness.
- Six gravitation items are placeholders, with both overview and test empty: `scalar_tensor_completion`, `weak_strong_field_limits`, `thermodynamic_relations`, `action_prefactor_dictionary`, `lensing_time_delay` and `bimetric_locking`.

Every statement below is checked by [`verify_docs_intersection.py`](verify_docs_intersection.py) (23 checks, all pass). Section numbers § refer to [`aqual_algebra_further.md`](aqual_algebra_further.md).

---

## A. Where the docs and this folder agree

| Docs | This folder |
|---|---|
| $dF/dy = \mu(\sqrt y)$, the round trip (docs 06, site tests) | Holds. The logarithm in $F$ is the screening identity integrated (§5) |
| $F(0) = 0$, $F \ge 0$, $F'' = 1/[2\sqrt y(1+\sqrt y)^2]$ | Hold. $F \ge 0$ because $F = \int_0^y \mu$ and $\mu \ge 0$ |
| $v^4 = GM(g + a_0)$ (docs 03, "the local field equation") | It is the spherical field equation $g_t^2 = g_s(g_t + a_0)$. In the hyperbolic variable of §9, $g + a_0 = a_0\coth^2(\psi/2)$ |
| The decode $M_{\text{dec}} = rv^4/[G(a_0r + v^2)]$ | Equivalently $M_{\text{dec}} = (r^2/G)\,(g_t - a_0\mu)$: **the decoded mass is the total field minus its TetB share**, from (1c). This is the quiet partition; the interior's active contribution is the separate quantity $\Delta M_{\text{eff}} = M_{\text{phot}} - M_{\text{dec}}$ |
| Deep field: $M = v^4/(Ga_0)$, slope 4 | Holds; it is the $\psi \to \infty$ limit of §9 |
| "The Legendre transform exists" (site test) | §7 gives it in closed form, $Q(z^2)$ |
| Complement symmetry $\mu(x) + \mu(1/x) = 1$ | Holds. It is why the mean coupling is 17 (§6) and what singles out the one-directional law (§11) |

## B. Docs statements the algebra does not support

1. **"In the deep field regime ($y \ll 1$), this [logarithmic] term dominates"** (docs 06). It does not. At $y = 10^{-6}$ the logarithm is 3000 times $F$ itself. $F \simeq \tfrac23 y^{3/2}$ arises because the orders $\sqrt y$ and $y$ cancel among all three terms. The [energy-functional proof](../../proofs/aqual-energy-functional/) says so explicitly, and so does the body of the [closed-form paper](../../papers/closed-form-aqual-energy-functional/) (§§5–6). That paper's abstract, however, says "the logarithm dominates at low acceleration and produces deep-MOND scaling" (line 29 of its source), contradicting its own §5.

2. **"No other proposed interpolation function gives an exact decode … Only the topological form is algebraic"** (docs 03). Both halves fail.
   - The decode needs only $\mu$ evaluated at the *observed* field, $M = r^2 g\,\mu(g/a_0)/G$. That is explicit for every interpolating function.
   - The standard $\mu = x/\sqrt{1+x^2}$ also has an algebraic forward inverse, $x = \sqrt{z\,(z + \sqrt{z^2+4})/2}$.

   What is distinctive about $x/(x+1)$ is narrower and still true:
   - its odds are linear, $\Omega = x$;
   - its forward inverse is a single quadratic root;
   - its energy functional is elementary (§7).

3. **The other interpolating functions are misstated** (docs 03, and the extended site test).
   - The "$n$ family" is written $x/(1+x)^{1/n}$. That exceeds 1 (at $x = 3$, $n = 2$ it is 1.5). The family is $x/(1+x^n)^{1/n}$.
   - The "RAR form $\mu = 1 - e^{-\sqrt x}$" is not McGaugh's function. The RAR fit is stated in the source variable, $g_{\text{obs}} = g_{\text{bar}}/(1 - e^{-\sqrt{g_{\text{bar}}/a_0}})$.
   - In `check_constitutive_law_uniqueness`, $x/\sqrt{1+x^2}$ is labelled "simple"; it is the *standard* function. The simple function is $x/(x+1)$ itself. The test's "McGaugh" function, $1 - e^{-x}$, is neither.

4. **The site's uniqueness test cannot fail a rival.** It rejects alternatives because $\mu(1) \ne 1/2$. But $\mu(1) = 1/2$ fixes only the unit of $a_0$: the standard function passes after $a_0 \to \sqrt3\,a_0$. The real uniqueness arguments are the exchange proof, the equilibrium route, and §11 here.

5. **The stability conditions tested are not the stability conditions.** The site tests use $F''(y) > 0$ as the ghost-free condition. For a scalar with kinetic function $F$, the conditions are:
   - no ghost: $F' > 0$;
   - gradient stability: $F' + 2yF'' > 0$.

   These are exactly the Hessian eigenvalues $\mu$ and $(x\mu)'$ of the energy-functional proof's Theorem 2. Both hold, so the conclusion stands, but the test checks a different quantity.

6. **Subluminality is not what the test measures.** `check_subluminal_scalar_propagation` checks $\mu \le 1$. If $y$ is read covariantly, $y = g^{\mu\nu}\partial_\mu\Phi\,\partial_\nu\Phi/a_0^2$, then perturbations of a static field travel at:

   $$c_\perp = c \ \text{(across the field)}, \qquad c_\parallel = c\sqrt{2 - \mu} \ \text{(along it)}.$$

   These are the two eigenvalues of §4, now as speeds. **Along the field the speed exceeds $c$ wherever $\mu < 1$, approaching $\sqrt2\,c$ as $x \to 0$ (the deep field).** It depends on $x$ through the partition, not on TetB's occupancy.

   This is the known behaviour of relativistic AQUAL (RAQUAL), noted by Bekenstein and Milgrom (1984). Whether it implies acausality is debated: Babichev, Mukhanov and Vikman (2008) argue that superluminal k-essence need not be paradoxical. The docs do not say whether GFD's $y$ is covariant in this sense. They also do not say what $F$ means for timelike gradients ($y < 0$), where $\sqrt y$ is not real.

7. **The scalar equation needs a source, and docs 06 removes it.** Docs 06 describes $\mathcal L_{\text{matter}}$ as "minimally coupled to the metric. There is no modification, no coupling to the scalar field."
   - In AQUAL the source enters through the term $-\rho\Phi$, which is in the energy-functional proof's Lagrangian.
   - With it, the Euler–Lagrange equation is $\nabla\cdot[\mu\nabla\Phi] = 4\pi G\rho$. Without any coupling between matter and $\Phi$, it is $\nabla\cdot[\mu\nabla\Phi] = 0$.

   Paper VII's action leaves $\mathcal L_{\text{matter}}$ unspecified, so the paper is not contradicted, only docs 06. One sentence would close this: say how matter couples to $\Phi$. In RAQUAL, matter couples to $\tilde g = e^{2\Phi/c^2}g$, which gives $-\rho\Phi$ at weak field.

8. **Naming.** The archive uses "the field equation" and "scalar-tensor transition" inconsistently.
   - Docs 02 calls the capacity function $f(x) = (21x+13)/(x+1)$ "the field equation".
   - Docs 02, docs 06, the rotation-curves page and Paper XIII call the quadratic $g_s = g_t^2/(a_0 + g_t)$ "the scalar-tensor transition".
   - Paper VII names the full action $S_{\text{ST}}$.

   The SST is the full covariant action; the quadratic is its spherical field equation and is never itself "the SST". The reader-facing Markdown (docs 02, docs 06, the rotation-curves page, the root README, the field-closure and Tully–Fisher READMEs and the research syntheses) has been corrected to say "spherical field equation" or "spherical-static quadratic". Paper titles and LaTeX sources (Papers X and XIII, the field-closure letter supplement, the Hassan–Rosen lock letter, GFD essentials) still use the old name and are left for the author.

   The same pages also label the regime $x \to 0$ "Deep field (TetB dominant)" (docs 02, docs 03). The deep field is a range of $x$ reached in the exterior, toward the rim, where the TetB share approaches 1. TetB itself is the throat interior at the centre, reached through the Field Origin (decoding-mass letter). The same conflation appears in the constitutive-law letter, lines 404–411 ("the deep-field limit … is itself the TetB sector"), and in the galaxy interior/exterior synthesis table ("TetB (deep field)").

9. **Two relations between $a_0$ and $H$.** At $H = 70.21$ km/s/Mpc:

| Relation | $a_0$ (m s⁻²) | Where |
|---|---|---|
| $a_0 = cH/2\pi$ | $1.086 \times 10^{-10}$ | [`what_is_gravity.md`](../g_from_topology/what_is_gravity.md) (citing Paper II), [`read_sweep_synthesis.md`](../g_from_topology/read_sweep_synthesis.md) |
| $a_0 = (cH/2\pi)\sqrt{K/\pi}$ | $1.225 \times 10^{-10}$ | the docs H₀ page |

   The second matches Paper VII's $a_0 = 16\,Gm_e/r_e^2$ to one part in $10^4$. The two relations differ by $\sqrt{4/\pi} = 1.128$, and one of them should be retired or the difference explained.

## C. What this folder adds to the docs

| Docs topic | Added here |
|---|---|
| Three terms of $F$ (docs 06) | The logarithm is $\int(1-\mu)\,dx = \int\mu\,d\ln x$; the deep field is a cancellation (§5) |
| Ghost freedom, subluminality (site tests) | The correct conditions are the Hessian eigenvalues; the along-field wave speed is $c\sqrt{2-\mu}$ (§4, C above) |
| Legendre existence | The closed form $Q$ (§7) |
| $v^4 = GM(g + a_0)$, the decode | The hyperbolic form (§9); $M_{\text{dec}} = (r^2/G)(g_t - a_0\mu)$ |
| Uniqueness of $\mu$ | Deep-field scaling plus exchange symmetry within the monomial family (§11) |
| The six placeholder items | `weak_strong_field_limits` can be filled from §7 and §9. `scalar_tensor_completion` needs B6 and B7 settled first. The others are outside this folder |

## D. Suggested edits, not made

None of these have been applied. Each needs your decision:

1. **Docs 06 and the closed-form paper's abstract:** correct the deep-field sentence about the logarithm (B1). In docs 06, also state how matter couples to $\Phi$ (B7).
2. **Docs 03:** correct the decode and algebraic-inverse claims (B2), and the interpolating functions (B3).
3. **Site tests:**
   - replace $F'' > 0$ with the two stability conditions (B5);
   - replace $\mu \le 1$ with the wave speeds, and decide what they mean for GFD (B6);
   - fix the labels in the uniqueness test and replace its midpoint criterion (B3, B4).
4. **Naming** across docs 02, docs 06 and the rotation-curves page (B8).
5. **One $a_0$–$H$ relation** for the archive (B9).

## References

- Babichev, E., Mukhanov, V. and Vikman, A. (2008). k-Essence, superluminal propagation, causality and emergent geometry. *J. High Energy Phys.* 2008(02), 101.
- Bekenstein, J. and Milgrom, M. (1984). Does the missing mass problem signal the breakdown of Newtonian gravity? *Astrophys. J.* 286, 7.
- Famaey, B. and McGaugh, S. S. (2012). Modified Newtonian Dynamics (MOND): observational phenomenology and relativistic extensions. *Living Rev. Relativ.* 15, 10.
- McGaugh, S. S., Lelli, F. and Schombert, J. M. (2016). Radial acceleration relation in rotationally supported galaxies. *Phys. Rev. Lett.* 117, 201101.

Run: `python verify_docs_intersection.py` (needs `sympy` and `mpmath`).
