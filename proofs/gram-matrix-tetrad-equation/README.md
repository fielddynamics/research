# The Gram Matrix of the Tetrad Equation

*What the metric can and cannot see of the two roots of the tetrad equation · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`tetrad` `Gram-matrix` `spatial-parity` `root-blindness` `Hadamard-matrix` `stellated-octahedron` `torsion` `proof`

---

This folder holds a five-page proof and a script that checks every step (66 checks, exact algebra, exhaustive where the cases are finite, and exact spot checks for the rigidity converse and Theorem 3(ii)). It was revised after an internal referee-style review ([`referee_review.md`](referee_review.md)). It is the revised version of the [Gram-matrix note](../../papers/gram-matrix-of-tetrad-equation/), which is unchanged in its own folder. This page explains the argument for a reader with first-year linear algebra.

## The question

The tetrad equation, $g = e^T\eta\,e$, builds the metric from the frame. It is quadratic in the frame, so flipping the spatial legs gives a second solution with the same metric: two roots, TetA and TetB. The note asks what can tell the two roots apart, using nothing but matrix multiplication. Its answer has three layers: the Gram matrices, the geometry, and the connection.

## Part I: the three Gram products

Realise the frame in space as four directions, each a combination of the three spatial legs, and write them as the columns of a $3 \times 4$ matrix $M$. Spatial parity flips every spatial leg, so it flips every direction: the second root is $-M$. From the two roots you can form three Gram products:

- **Self-coupling** $M^TM$ is the same for both roots. It is *root-blind*.
- **Cross-coupling** $M^T(-M)$ is minus the self-coupling.
- **The cross-coupling is unchanged by swapping the roots.** So Gram products tell you whether two factors come from the *same* root or from *opposite* roots, never which root is which.

For the tetrahedral frame, put a row of ones on top of $M$. The result is the $4 \times 4$ Hadamard matrix. That one fact gives everything at once: $M^TM = 4I - J$ (diagonal 3, off-diagonal −1), the rows of $M$ orthogonal with equal length, and the split $I = \tfrac14 G + \tfrac14 J$ of four dimensions into three spatial directions and one closure direction.

**What does tell the roots apart?** The Gram matrix fixes $M$ up to a unique rotation or reflection, and for the two roots that map is $-I$, a reflection. So no rotation-invariant quantity can distinguish them; only *orientation* can. The handedness of any three legs, $\det(v_a, v_b, v_c)$, flips sign between the roots, because $(-1)^3 = -1$. This is the spatial form of $\det(Pe) = -\det e$ in the [scheme proof](../tetrad-scheme-two-bounded-regions/): the roots differ only in orientation, and three being odd is why.

## Part II: the geometry

The legs of one root are the four corners of the cube with $xyz = +1$; those of the other are the four with $xyz = -1$. Each is a regular tetrahedron, together they are the whole cube, and their compound is the stellated octahedron.

The symmetry groups show exactly what the compound adds. One tetrahedron has 24 symmetries, all 24 rearrangements of its legs. The stellated octahedron has 48:

$$\mathrm{Sym}(S) = \mathrm{Sym}(\mathrm{TetA}) \times \{I, -I\}.$$

The extra factor is parity, the map that exchanges TetA and TetB. So a single tetrahedron is not the stellated octahedron, and the difference between them is precisely the parity exchange.

## Part III: the index grid

The affine connection has $4^3 = 64$ components. Each $4 \times 4$ slice has 4 diagonal entries and 6 in each triangle, so $64 = 24 + 16 + 24$. In the framework's reading the upper triangle is TetA, the lower TetB and the diagonal shared, and swapping the triangles is the TetB step (used in the [chiral holonomy](../chiral-holonomy-closed-frame/) proof).

Swapping the two lower indices splits the 64 components into 40 that are unchanged (symmetric) and 24 that flip sign (antisymmetric, the torsion). On one mirror pair with entries $u$ (upper) and $l$ (lower), the symmetric part is $\tfrac12(u + l)$ and the torsion is $u - l$.

The torsion-free condition of general relativity is $l = u$. Written in grid coordinates it keeps the diagonal and the upper triangle and makes the lower a copy. That is the sense in which it keeps shared plus TetA and discards TetB. Read without choosing coordinates, it keeps the combination that does not notice the triangles being swapped and discards the difference.

## Part IV: the torsion-free projection

The theorem has three parts:

1. **Torsion-free is a projection, not an equivalence.** It maps 64 components onto 40, with the 24 torsion components as its kernel: $16 + 24 = 40 \neq 64$.
2. **A metric connection is fixed by the metric and its torsion.** The ways two metric-compatible connections can differ form a 24-dimensional space, and the map to their torsion is one-to-one onto all 24 torsion components.
3. **So the torsion is the only place a connection can tell the roots apart.** The metric is the same on both roots, so a torsion-free metric connection, the Levi-Civita connection, is the same on both. Any metric connection that distinguishes them does so through its torsion and nowhere else.

Parts I and IV say the same thing at two levels. The metric cannot see the roots, so neither can anything built from the metric alone. General relativity sets the torsion to zero, and with it the only room left for the distinction.

**Necessary, not automatic.** Proposition 2 shows when the torsion actually carries the distinction. In the tetrad formalism a connection is built from the frame and a spin connection $\omega$:
- **Carried with the frame.** If $\omega$ is transformed by parity along with the frame, the connection comes out identical on both roots, torsion included.
- **Kept fixed.** If both roots keep the same $\omega$, the two connections share the metric but differ, and they differ exactly in their torsion.

So the torsion is the *necessary* carrier, Letter 2's word. Whether it carries the distinction depends on how the field assigns connections to the roots, which is physical input, not something the tetrad equation decides.

## Why it matters

- **It makes "root-blind" and "root-resolving" exact.** Gram data are blind to which root is which and resolve only the relative root; orientation is the absolute invariant.
- **It explains why three dimensions matter here too.** Orientation flips under parity because three is odd, the same fact behind the [scheme proof](../tetrad-scheme-two-bounded-regions/) and the cube filling of the [Hadamard proof](../hadamard-cube-frame/).
- **It locates TetB's room in the connection.** For metric connections, the torsion sector is not just *a* place the distinction could live; it is the *only* place. This is the algebraic ground under GFD's reading that the 24 torsion components carry the TetA/TetB distinction ([Letter 2](../../papers/letter-2-other-half-of-gravity-torsion/), [torsion as the regular representation](../torsion-regular-representation/)).

## What it does not do

- It does not prove that the field assigns the two roots connections that differ. It proves that if they differ, they differ in the torsion (Theorem 3), and that this happens exactly when the connection is not carried covariantly with the frame (Proposition 2).
- The split of each slice into upper and lower triangles depends on the order of the coordinates. The 40 + 24 split and the torsion do not.
- The tetrahedral frame is taken from the [forced tetrahedral frame](../forced-tetrahedral-frame/) proof, which rests on the magnitude reading of $\eta$.
- The labels upper = TetA, lower = TetB on the index grid are the framework's reading. The theorems hold whatever the labels.

## Earlier version

The original note, [`supplementary_gram_stellated_octahedron.tex`](../../papers/gram-matrix-of-tetrad-equation/supplementary_gram_stellated_octahedron.tex), is correct in its algebra. This version keeps its four-part structure and its lemmas, and:

- **corrects "root-resolving".** The original said the cross-coupling is "the only Gram product whose value distinguishes $M_1$ from $M_2$". But $M_2^TM_1 = M_1^TM_2$, so it is unchanged when the roots are swapped. It resolves the *relative* root of two factors, and the revision says so;
- **adds the absolute invariant.** Lemma 5 now proves the converse of orthogonal invariance (the Gram matrix fixes $M$ up to a unique element of $O(3)$, which is $-I$ for the two roots), and Proposition 1 shows orientation is what separates them, flipping because $D = 3$ is odd. This replaces the claim that the Gram products are "the complete orthogonal-invariant content", which is now proved, together with what it implies: that they cannot see which root is which;
- **derives the explicit Gram matrix from the Hadamard identity** rather than six entry-by-entry products, which gives the eigenstructure, the closure null vector and the rows of $M$ as eigenvectors in the same step;
- **proves the tetrahedron and cube facts directly** ($xyz = \pm 1$, edge length, disjointness, exhaustion) instead of citing Coxeter for "constant pairwise inner product implies a regular tetrahedron", which also needs equal lengths;
- **gives the non-isomorphism content.** "A tetrahedron is not a stellated octahedron" is now Theorem 2: $\mathrm{Sym}(S) = \mathrm{Sym}(\mathrm{TetA}) \times \{\pm I\}$, checked over all $8!$ relabellings, with the extra factor being the parity exchange;
- **repairs Theorem 1's proof.** The original concluded that the retained 24 are TetA and the discarded 24 TetB "by the Part II identification", but Part II identifies the *columns* of $M$ with the tetrahedra, not the *triangles* of the index grid. The revision keeps the framework's triangle reading as a reading, states the coordinate-free split (40 swap-even, 24 swap-odd), and proves what the conclusion needs: for metric connections, the discarded 24 are the only place the roots can differ;
- **drops the claim that the antisymmetric part "carries the root-resolving content of Lemma 2"** as a consequence of Part I. Lemma 2 is about Gram products, not connections; the revision proves instead that torsion is the *only possible* carrier, and states that its being nonzero is not shown;
- **sharpens the Levi-Civita sentence.** The original called torsion-freeness "a sufficient condition for the Levi-Civita theorem"; it is one of the theorem's two hypotheses, with metric compatibility.

## Contents

| File | Contents |
|---|---|
| [`gram_matrix_tetrad_equation.pdf`](gram_matrix_tetrad_equation.pdf) | The proof, five pages |
| [`gram_matrix_tetrad_equation.tex`](gram_matrix_tetrad_equation.tex) | LaTeX source (IOP journal class, included) |
| [`verify_gram_matrix_tetrad_equation.py`](verify_gram_matrix_tetrad_equation.py) | Exact checks of every lemma, proposition and theorem: the Hadamard identity, exact rational rotations and reflections for invariance and rigidity, orientation of all four leg triples, the symmetry groups over all $8!$ relabellings of the cube, the exchange split and its coordinate independence, the metric-connection bijection for $\eta$ and a generic Lorentzian metric, and both cases of Proposition 2 |
| [`referee_review.md`](referee_review.md) | Internal referee-style review and the change made for each point |
| [`iopjournal.cls`](iopjournal.cls) | Document class, so the source builds here |

```bash
pip install sympy
python verify_gram_matrix_tetrad_equation.py      # 66/66
pdflatex -interaction=nonstopmode gram_matrix_tetrad_equation.tex
```

## Related

- [The forced tetrahedral frame](../forced-tetrahedral-frame/): why the legs, drawn in space, form a regular tetrahedron; the rigidity lemma used here.
- [The stellated octahedron, the cube and the Hadamard matrix](../hadamard-cube-frame/): the bordered frame is the Hadamard matrix.
- [The tetrad scheme and the two bounded regions](../tetrad-scheme-two-bounded-regions/): the two roots, $\det(Pe) = -\det e$, and why keeping one is a convention.
- [The torsion sector as the regular representation of S₄](../torsion-regular-representation/): what the 24 torsion components contain.
- [Chiral holonomy of the closed tetrad frame](../chiral-holonomy-closed-frame/): the triangle exchange of the index grid as the TetB step.
- [The original Gram-matrix note](../../papers/gram-matrix-of-tetrad-equation/), with its own [verification script](../../papers/gram-matrix-of-tetrad-equation/verify_gram_theorems.py).

---

*The algebra is complete and exact. The script checks every step, exhaustively where the cases are finite and by exact spot checks for the rigidity converse and Theorem 3(ii). The physical reading of the roots and the index grid is GFD's, stated so that it can be tested.*
