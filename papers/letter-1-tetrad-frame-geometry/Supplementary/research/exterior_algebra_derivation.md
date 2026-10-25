# The Exterior Algebra of the Derived Tetrahedral Frame and the Stellated Octahedron

**A Companion Interpretation**

Stephen Nelson, Field Dynamics Research (2026)

---

## Statement

From the spatial sector of a Lorentzian tetrad, the companion supplementary derivation uniquely fixes an isotropic four-direction set with pairwise inner product $c = -1/3$. The present note studies the exterior algebra of that derived four-direction system and identifies its graded structure with the stellated octahedron.

The identification requires two independent ingredients: the combinatorial dimensions of the exterior algebra (which follow from the number of generators) and the equal-angle condition on the four derived directions (which follows from the Lorentz signature's isotropy via the supplementary derivation). Neither ingredient alone is sufficient. Together, they uniquely determine the graded geometric identification.

---

## Definitions

Let $\mathcal{M}$ be a 4-dimensional Lorentzian manifold with signature $(-,+,+,+)$. A **tetrad** (vierbein) $e^a{}_\mu$ at a point $p \in \mathcal{M}$ is a set of four one-forms satisfying:

$$\eta_{ab}\, e^a{}_\mu\, e^b{}_\nu = g_{\mu\nu}$$

where $\eta_{ab} = \text{diag}(-1,+1,+1,+1)$.

From the spatial sector of this tetrad, the companion supplementary material derives a unique isotropic four-direction set $v_1, v_2, v_3, v_4$ with pairwise inner product $c = -1/3$. These four derived tetrahedral directions are the generators of the exterior algebra studied here. They are not the three orthogonal spatial legs of the tetrad; they are four linear combinations of those legs, uniquely fixed by the isotropy of the $(-,+,+,+)$ signature's spatial sector.

Let $V$ be the 4-dimensional real vector space spanned by $v_1, v_2, v_3, v_4$, and let $\Lambda^k(V)$ denote its grade-$k$ exterior power.

A **stellated octahedron** (stella octangula) is the compound of two dual regular tetrahedra.

---

## Ingredient 1: The Combinatorial Dimensions

**Proposition 1.** *The exterior algebra of a vector space of dimension $n$ has dimension $\binom{n}{k}$ at grade $k$.*

The generators are $v_1, v_2, v_3, v_4$, so $n = 4$. This gives:

$$\dim(\Lambda^k) = \binom{4}{k} = \{1,\, 4,\, 6,\, 4,\, 1\}$$

This is a universal combinatorial fact. It holds for any four linearly independent generators, regardless of their geometric properties. It carries no information about angles or regularity.

---

## Ingredient 2: The Equal-Angle Condition

**Proposition 2.** *The four derived tetrahedral directions $v_1, v_2, v_3, v_4$ have equal pairwise angles, with $\cos\theta = -1/3$ for every pair.*

This is not a direct consequence of tetrad orthonormality in the textbook sense. It follows from the full derivation chain: the Lorentz signature gives $SO(3)$ isotropy in the spatial sector; in $D = 3$ dimensions, the minimal bounded enclosure requires $D + 1 = 4$ bounding planes; the isotropy condition on a four-point set uniquely fixes the pairwise inner product at $c = -1/3$. The derivation is given in the companion supplementary material.

**Proposition 3.** *Four unit vectors in $\mathbb{R}^3$ with equal pairwise angles and $\cos\theta = -1/3$ are the face normals of a regular tetrahedron, unique up to $O(3)$.*

**Proof.** The sum $S = \sum_{i=1}^{4} \hat{n}_i$ satisfies $|S|^2 = 4 + 12c = 0$ for $c = -1/3$, so $S = 0$. Four unit vectors in $\mathbb{R}^3$ that sum to zero with equal pairwise angles are the vertices of a regular tetrahedron inscribed on the unit sphere. $\square$

---

## The Identification

### Grade 1: The Primary Tetrahedron

The four generators $v_1, v_2, v_3, v_4$ are the face normals of a regular tetrahedron (Propositions 2 and 3). The half-space inequalities $v_i \leq 1$ bound the primary tetrahedron TetA:

$$\text{TetA}: \quad \max(v_1, v_2, v_3, v_4) \leq 1$$

Grade 1 of the exterior algebra is identified with TetA.

### Grade 3: The Dual Tetrahedron via the Hodge Star

The Hodge star in four dimensions maps grade-$k$ forms to grade-$(4-k)$ forms:

$$*: \Lambda^k \to \Lambda^{4-k}$$

On grade 1, it maps each generator $v_i$ to the grade-3 volume spanned by the remaining three:

$$*v_i = \epsilon_{ijkl}\, v^j \wedge v^k \wedge v^l$$

Under the natural orientation and metric duality, the grade-3 sector is identified with the orientation-reversed tetrahedral sector. The zero-sum identity $\sum v_i = 0$ means that the volume opposite to each face normal $v_i$ is spanned by the three directions whose sum is $-v_i$. The four grade-3 elements are therefore identified with the normals of the dual tetrahedron:

$$\text{TetB}: \quad \max(-v_1, -v_2, -v_3, -v_4) \leq 1$$

TetB is not introduced as an independent construction. It is the Hodge dual of TetA within the same exterior algebra.

### Grade 2: The Octahedral Core

Grade 2 has $\binom{4}{2} = 6$ basis elements: $v_i \wedge v_j$ for $i < j$. Each wedge product spans the plane defined by generators $i$ and $j$, which contains the edge where faces $i$ and $j$ of TetA meet. A regular tetrahedron has exactly $\binom{4}{2} = 6$ edges, so the six grade-2 elements are in one-to-one correspondence with the six edges.

The six edge midpoints of a regular tetrahedron are the six vertices of a regular octahedron (the rectification of the tetrahedron). The main letter proves directly that the intersection TetA $\cap$ TetB is a regular octahedron with these six vertices. Grade 2 is therefore identified with the octahedral core:

$$\text{Octahedron} = \text{TetA} \cap \text{TetB}$$

### Assembly

The compound of TetA (grade 1) and TetB (grade 3), with octahedral core (grade 2), is the stellated octahedron.

| Grade | $\dim = \binom{4}{k}$ | Geometric identification |
|---|---|---|
| 0 | 1 | Scalars |
| 1 | 4 | TetA (primary tetrahedron) |
| 2 | 6 | Octahedral core (TetA $\cap$ TetB) |
| 3 | 4 | TetB (dual tetrahedron) |
| 4 | 1 | Volume form |

---

## Why Both Ingredients Are Necessary

The combinatorial dimensions $\{1, 4, 6, 4, 1\}$ hold for any four linearly independent generators. Without the equal-angle condition forced by the Lorentz signature's isotropy, the four directions define an irregular tetrahedron and the compound is an irregular stella octangula. The isotropy derivation forces regularity. Without it, the structural constants do not reduce to $K = 4$ and $D = 3$.

---

## The Hodge Star as Exchange Symmetry

The Hodge star maps $\Lambda^1 \leftrightarrow \Lambda^3$, exchanging the TetA and TetB identifications. Grade 2, the octahedral core, is the fixed locus of this involution.

---

## Summary

1. **The Lorentz signature's isotropy**, via the companion supplementary derivation, uniquely fixes four tetrahedral directions with $\cos\theta = -1/3$.
2. **Equal pairwise angles** force these directions to be face normals of a regular tetrahedron (TetA, grade 1).
3. **The Hodge star** maps grade 1 to grade 3, and the grade-3 sector is identified with the orientation-reversed dual tetrahedron (TetB).
4. **Grade 2** contains six elements in one-to-one correspondence with the six edges, whose midpoints are the vertices of the octahedral core.
5. **The compound** of TetA and TetB is the stellated octahedron.

The boundedness classification in the main letter and the exterior algebra identification here arrive at the same stellated octahedron by complementary routes.
