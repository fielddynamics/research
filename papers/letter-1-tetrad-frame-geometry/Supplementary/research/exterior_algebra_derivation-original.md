# The Exterior Algebra of the Tetrad Frame and the Stellated Octahedron

**A Derivation**

Stephen Nelson, Field Dynamics Research (2026)

---

## Statement

We prove that the exterior algebra of a regular orthonormal tetrad in four-dimensional spacetime, restricted to its spatial components, has the geometric structure of a stellated octahedron. The proof requires two independent ingredients: the combinatorial dimensions of the exterior algebra (which follow from the number of one-forms) and the equal-angle condition on the spatial projections (which follows from the orthonormality of the frame). Neither ingredient alone is sufficient. Together, they force the identification uniquely.

---

## Definitions

Let $\mathcal{M}$ be a 4-dimensional Lorentzian manifold with signature $(-,+,+,+)$. A **tetrad** (vierbein) $e^a{}_\mu$ at a point $p \in \mathcal{M}$ is a set of four one-forms satisfying the orthonormality condition:

$$\eta_{ab}\, e^a{}_\mu\, e^b{}_\nu = g_{\mu\nu}$$

where $\eta_{ab} = \text{diag}(-1,+1,+1,+1)$ is the Minkowski metric.

The **spatial projection** of the tetrad is the restriction of the three spatial one-forms $(e^1, e^2, e^3)$ to the local spatial frame. In flat space, or at any point in Riemann normal coordinates, these project the four tetrad legs onto $\mathbb{R}^3$.

A **regular tetrahedron** in $\mathbb{R}^3$ is a set of four vectors with equal pairwise angles.

A **stellated octahedron** (stella octangula) is the compound of two dual regular tetrahedra — a regular tetrahedron and its orientation-reversed image under spatial inversion.

---

## Ingredient 1: The Combinatorial Dimensions

**Proposition 1.** *The exterior algebra of $n$ one-forms has dimension $\binom{n}{k}$ at grade $k$, for $k = 0, 1, \ldots, n$.*

This is standard linear algebra. Given one-forms $\omega^1, \ldots, \omega^n$, the grade-$k$ component $\Lambda^k$ is spanned by all $k$-fold wedge products $\omega^{i_1} \wedge \cdots \wedge \omega^{i_k}$ with $i_1 < \cdots < i_k$. The number of such products is $\binom{n}{k}$.

For $n = 4$ (the tetrad), this gives:

$$\dim(\Lambda^k) = \binom{4}{k} = \{1,\, 4,\, 6,\, 4,\, 1\}$$

**This is a universal combinatorial fact.** It holds for any four linearly independent one-forms, regardless of their geometric properties. It carries no information about angles, regularity, or the specific structure of the tetrad.

---

## Ingredient 2: The Equal-Angle Condition

**Proposition 2.** *The spatial projections of a regular orthonormal tetrad in $\mathbb{R}^{3,1}$ have equal pairwise angles, with $\cos\theta = -1/3$ for every pair.*

**Proof.** In flat space, the canonical orthonormal tetrad has spatial legs pointing along the four directions:

$$\hat{n}_1 = \frac{1}{\sqrt{3}}(1,1,1), \quad \hat{n}_2 = \frac{1}{\sqrt{3}}(1,-1,-1), \quad \hat{n}_3 = \frac{1}{\sqrt{3}}(-1,1,-1), \quad \hat{n}_4 = \frac{1}{\sqrt{3}}(-1,-1,1)$$

Each vector has unit length: $|\hat{n}_i|^2 = (1+1+1)/3 = 1$. The dot product between any two distinct vectors is:

$$\hat{n}_i \cdot \hat{n}_j = \frac{1}{3}(1 - 1 - 1) = -\frac{1}{3} \quad \text{for all } i \neq j$$

This gives $\cos\theta = -1/3$, or $\theta \approx 109.47°$, for every pair. The calculation is the same for all six pairs by the symmetry of the sign pattern: each pair of vectors agrees on exactly one coordinate and disagrees on two.

A local Lorentz rotation $\Lambda \in SO(3,1)$ transforms the tetrad as $e'^a = \Lambda^a{}_b\, e^b$. The pairwise angles between the spatial projections are preserved under spatial rotations $R \in SO(3)$ (which rotate all four vectors rigidly) and are independent of the boost components (which affect only the time leg). The equal-angle property is therefore gauge-invariant within the spatial rotation subgroup.  $\square$

**Proposition 3.** *Four unit vectors in $\mathbb{R}^3$ with equal pairwise angles form the face normals of a regular tetrahedron. This configuration is unique up to rotation.*

**Proof.** Let $\hat{n}_1, \ldots, \hat{n}_4$ be unit vectors in $\mathbb{R}^3$ with $\hat{n}_i \cdot \hat{n}_j = c$ for all $i \neq j$, where $c$ is a constant. The sum $S = \sum_{i=1}^{4} \hat{n}_i$ satisfies:

$$|S|^2 = \sum_i |\hat{n}_i|^2 + 2\sum_{i < j} \hat{n}_i \cdot \hat{n}_j = 4 + 2 \cdot 6 \cdot c = 4 + 12c$$

For $c = -1/3$, this gives $|S|^2 = 0$, so $S = 0$: the four vectors sum to zero. A set of four unit vectors in $\mathbb{R}^3$ that sum to zero and have equal pairwise angles are the outward face normals of a regular tetrahedron centred at the origin. This is a standard result in Euclidean geometry; the proof follows from the fact that the four vectors are the vertices of a regular tetrahedron inscribed on the unit sphere, and the convex hull of such vertices is the unique regular simplex in three dimensions.  $\square$

---

## The Derivation

We now combine the two ingredients to derive the stellated octahedron from the exterior algebra of the tetrad.

### Grade 1: The Primary Tetrahedron

By Proposition 2, the four spatial tetrad one-forms $v_1, v_2, v_3, v_4$ have equal pairwise angles with $\cos\theta = -1/3$. By Proposition 3, they are the face normals of a regular tetrahedron. We label this tetrahedron TetA.

The half-space inequalities $v_i \leq 1$ bound TetA as a convex region:

$$\text{TetA}: \quad \max(v_1, v_2, v_3, v_4) \leq 1$$

Grade 1 of the exterior algebra is TetA.

### Grade 3: The Dual Tetrahedron

The Hodge star operator in four dimensions maps grade-$k$ forms to grade-$(4-k)$ forms:

$$*: \Lambda^k \to \Lambda^{4-k}$$

On grade 1, it acts as:

$$*v_i = \epsilon_{ijkl}\, v^j \wedge v^k \wedge v^l$$

where $\epsilon_{ijkl}$ is the Levi-Civita symbol. Each grade-1 element $v_i$ maps to a grade-3 element that spans the three-dimensional volume defined by the remaining three one-forms $\{v_j, v_k, v_l\}$.

The spatial content of this map is: $*v_i$ is the volume *opposite* to the face with normal $v_i$. In three spatial dimensions, this is equivalent to the direction $-v_i$ (the inward normal becomes the outward normal of the opposite face in the dual tetrahedron). The four grade-3 elements therefore point along:

$$-\hat{n}_1, \quad -\hat{n}_2, \quad -\hat{n}_3, \quad -\hat{n}_4$$

These are the face normals of the **orientation-reversed dual tetrahedron**, obtained by negating all four spatial directions. We label this TetB:

$$\text{TetB}: \quad \max(-v_1, -v_2, -v_3, -v_4) \leq 1$$

Grade 3 of the exterior algebra is TetB.

### Grade 2: The Octahedral Intersection

Grade 2 has $\binom{4}{2} = 6$ basis elements: $v_i \wedge v_j$ for $i < j$. Each wedge product $v_i \wedge v_j$ defines the plane spanned by face normals $i$ and $j$, which is the plane containing the **edge** where faces $i$ and $j$ of TetA meet.

A regular tetrahedron has exactly $\binom{4}{2} = 6$ edges. The six grade-2 elements are in one-to-one correspondence with the six edges of TetA (equivalently, the six edges of TetB, since the edge skeleton is the same under the sign flip).

The six edge midpoints of a regular tetrahedron are the six vertices of a regular octahedron. This is a classical result: the octahedron is the rectification of the tetrahedron. The region enclosed by these six vertices — equivalently, the intersection of TetA and TetB — is the regular octahedral core:

$$\text{Octahedron} = \text{TetA} \cap \text{TetB}$$

Grade 2 of the exterior algebra is the octahedral intersection of the two tetrahedra.

### Grades 0 and 4: Existence and Closure

Grade 0, $\Lambda^0$, is the one-dimensional space of scalar functions. It represents pure existence — a point with no directional content. This is the precondition for the geometry to be defined at all.

Grade 4, $\Lambda^4$, is the one-dimensional space of volume forms. The single element $v_1 \wedge v_2 \wedge v_3 \wedge v_4$ is the oriented volume of the full four-dimensional frame. It represents closure — the body of the compound taken as a whole.

### Assembly

The compound of TetA (grade 1) and TetB (grade 3) is, by definition, the **stellated octahedron** — the polyhedron first described by Kepler (1619) as the compound of two dual regular tetrahedra, with the octahedral core (grade 2) as their intersection.

The exterior algebra of the tetrad frame therefore has the following geometric identification:

| Grade | $\dim = \binom{4}{k}$ | Exterior algebra | Stellated octahedron |
|---|---|---|---|
| 0 | 1 | Scalars | Existence |
| 1 | 4 | One-forms $v_i$ | TetA (primary tetrahedron) |
| 2 | 6 | Two-forms $v_i \wedge v_j$ | Octahedral core (TetA $\cap$ TetB) |
| 3 | 4 | Three-forms $*v_i$ | TetB (dual tetrahedron) |
| 4 | 1 | Volume form | Closure |

---

## Why Both Ingredients Are Necessary

The combinatorial dimensions $\{1, 4, 6, 4, 1\}$ are necessary but not sufficient. Any four linearly independent one-forms produce these dimensions. To identify the resulting geometry as a *stellated octahedron* rather than a generic 4-dimensional exterior algebra requires the additional geometric content provided by the equal-angle condition.

Without equal pairwise angles, the four one-forms at grade 1 define an *irregular* tetrahedron. The Hodge dual at grade 3 defines the corresponding irregular dual. The compound is an irregular stella octangula — a valid geometric object, but not the regular stellated octahedron whose structural constants reduce to $K = 4$ and $D = 3$.

The orthonormality of the tetrad forces $\cos\theta = -1/3$ for all pairs, which forces regularity. Without orthonormality, the proof fails at Proposition 2. With it, every subsequent step is uniquely determined.

---

## The Hodge Star as the Exchange Symmetry

The Hodge star $*$ maps $\Lambda^1 \to \Lambda^3$ and $\Lambda^3 \to \Lambda^1$ (up to sign). On the stellated octahedron, this is the involution $\sigma$ that swaps TetA and TetB:

$$* : \text{Grade 1 (TetA)} \longleftrightarrow \text{Grade 3 (TetB)}$$

The fixed locus of this involution — grade 2 — is the octahedral core. This is consistent with the Lefschetz analysis: the involution has no fixed simplices on the two tetrahedra, but the geometric intersection (the octahedron) is the fixed subspace in the ambient algebra.

In the context of Maxwell's electrodynamics, the Hodge star maps the electromagnetic field tensor $F$ (a 2-form) to its dual $*F$. The self-dual and anti-self-dual decomposition of $F$ corresponds to the electric and magnetic components. This decomposition occurs at grade 2 — at the octahedral core, the field origin, the intersection of the two frames.

Electric-magnetic duality is TetA-TetB exchange. The electromagnetic field lives at the fixed point of that exchange.

---

## Conformal Invariance and Scale

Maxwell's equations in four-dimensional vacuum are conformally invariant. They contain no intrinsic length scale, no mass parameter, no preferred distance. The equations are identical under arbitrary rescaling of the metric:

$$g_{\mu\nu} \to \Omega^2(x)\, g_{\mu\nu}$$

This conformal invariance is the field-theoretic expression of the motivic fixed-point condition $T([M]) = [M]$ established in the companion analysis. The exterior algebra of the tetrad has the same structure $\{1, 4, 6, 4, 1\}$ at every scale because the algebra depends only on the number of one-forms (four) and their pairwise angle condition ($\cos\theta = -1/3$), neither of which carries a length dimension.

The stellated octahedron is therefore the scale-invariant geometric structure of the electromagnetic field. It is not a model of the photon — it is the algebraic skeleton on which any theory of the photon must be built, because the exterior algebra of any regular orthonormal tetrad in four-dimensional spacetime produces it, and no other regular structure is consistent with the Hodge star and the equal-angle condition.

---

## Summary

The derivation proceeds in five steps, each of which is forced:

1. **Orthonormality of the tetrad** forces equal pairwise angles $\cos\theta = -1/3$ between all four spatial one-forms (Proposition 2).

2. **Equal pairwise angles** force the four one-forms to be the face normals of a regular tetrahedron, unique up to rotation (Proposition 3).

3. **The Hodge star** maps grade 1 to grade 3, sending each face normal to the volume opposite it, which is the face normal of the orientation-reversed dual tetrahedron.

4. **The compound** of a regular tetrahedron and its dual is the stellated octahedron, by definition (Kepler, 1619).

5. **Grade 2** contains the six pairwise wedge products, in one-to-one correspondence with the six edges of the tetrahedron, whose midpoints are the six vertices of the octahedral core.

No choices are made at any step. The only input is the orthonormal tetrad in four-dimensional Lorentzian spacetime. The stellated octahedron is the output.
