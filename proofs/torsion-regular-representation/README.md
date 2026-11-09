# The Torsion Sector as the Regular Representation of S₄

*What general relativity discards when it sets torsion to zero · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`torsion` `affine-connection` `representation-theory` `symmetric-group` `Einstein-Cartan` `proof`

---

This folder holds a two-page proof and a script that checks every step. The proof shows that the 24 torsion components of the tetrad connection, the part of the geometry that general relativity sets to zero, have a precise and very rich structure: they are one complete copy of the ways of rearranging the four legs of the tetrad. This page explains the argument for a reader who has met groups and matrices.

## Torsion in one paragraph

To compare directions at neighbouring points of spacetime, geometry uses a *connection*, written $\Gamma^a{}_{bc}$. With four legs, each of the three indices takes four values, so the connection has $4^3 = 64$ components. In a coordinate basis, swapping the two lower indices splits them into a symmetric part, 40 components, called the Christoffel part, and an antisymmetric part, 24 components, called the *torsion*. Einstein's general relativity sets the torsion to zero. Cartan showed in 1922 that geometry allows torsion, and the Einstein–Cartan theory keeps it. GFD reads the torsion as the place where the two tetrahedra of the stellated octahedron, TetA and TetB, are told apart. So it matters what the torsion actually contains.

## The symmetry

The four legs can be rearranged in $4! = 24$ ways. These rearrangements form the *symmetric group* $S_4$. Read by magnitude, as in the [forced tetrahedral frame](../forced-tetrahedral-frame/), all four legs are equivalent, so every rearrangement is a symmetry of the frame. A rearrangement of the legs relabels the indices of the connection, so it shuffles the 64 components among themselves, and it shuffles the 24 torsion components among themselves.

## The result

There are 24 torsion components and 24 rearrangements. The proof shows this is no coincidence. **The torsion sector is the regular representation of $S_4$**: it is exactly the group of rearrangements acting on itself.

Concretely, there is a single torsion tensor $\xi$ such that its 24 rearranged copies, one for each rearrangement, form a basis of all torsion. Every torsion configuration is a unique combination of the 24 copies, and rearranging the legs simply permutes the copies the way the group permutes its own elements. The tensor is

$$\xi = f_0 \otimes (f_0 \wedge f_1 + f_2 \wedge f_3),$$

that is, $T^0{}_{01} = T^0{}_{23} = 1$ and the components fixed by antisymmetry, with every other component zero.

The regular representation is the richest structure a 24-dimensional space can carry for this group. Every irreducible way that $S_4$ can act appears in it, each as many times as its own dimension. So when general relativity sets torsion to zero, it discards a complete copy of the group algebra of the legs.

## How the proof works

**Two kinds of torsion component.** A torsion component $T^a{}_{bc}$ has one upper index $a$ and an antisymmetric pair of lower indices $\{b, c\}$. Either the upper index is one of the pair, as in $T^0{}_{01}$, or it is not, as in $T^0{}_{23}$. Call these *incident* and *non-incident*. There are 12 of each, and rearranging the legs can carry any incident component to any other, and likewise for non-incident ones.

**What a swap does.** The only rearrangement that keeps $T^0{}_{01}$ in place is the swap of legs 2 and 3, and it leaves that component unchanged. The same swap also keeps $T^0{}_{23}$ in place, but it flips its sign, because swapping 2 and 3 reverses the antisymmetric pair.

**Putting them together.** Add the two: $\xi = t_{0;01} + t_{0;23}$. Applying the swap gives $t_{0;01} - t_{0;23}$. Adding and subtracting recovers each piece separately. Doing this for every rearrangement recovers every one of the 24 torsion components, so the 24 copies of $\xi$ span all of torsion, and since there are exactly 24 of them they form a basis. That is the theorem.

In the language of representation theory, the incident components carry the trivial character of the swap and the non-incident ones carry its sign character. Together, trivial plus sign is the regular representation of the two-element group, and building up from there gives the regular representation of $S_4$.

## The sign representation

Every rearrangement is either even or odd: built from an even or odd number of swaps. The *sign representation* is the simplest possible response to this: multiply by $+1$ for even rearrangements and $-1$ for odd ones. The proof shows:

- It occurs **exactly once** in the torsion.
- It occurs **not at all** in the 40 Christoffel components, the part general relativity keeps.
- In the torsion it is the totally antisymmetric tensor $\omega^a{}_{bc} = \sum_d \varepsilon_{abcd}$, whose components are nonzero only when all three indices differ.

So the only part of the whole connection that responds to odd rearrangements of the legs with a pure sign lives in the torsion, and setting torsion to zero removes it.

## The usual physics decomposition

Physicists split torsion under the Lorentz group into a *vector* part (4 components, from the trace), an *axial* part (4, the totally antisymmetric piece) and a *tensor* part (16, the rest). The proof shows how this sits inside the two kinds of component:

| | Incident (12) | Non-incident (12) |
|---|---|---|
| Vector part | all 4 | — |
| Axial part | — | all 4 |
| Tensor part | 8 | 8 |

The two halves of the tensor part turn out to be the same representation. This answers a question left open in earlier versions: how the permutation structure relates to the standard decomposition.

There is a condition, and the proof states it. The axial part is defined by lowering an index with the metric. Lowered with the magnitude pattern $|\eta| = I$, everything above holds. Lowered with $\eta$ itself, keeping the minus sign of the time leg, the axial part is no longer preserved by the rearrangements. So the clean picture needs the same reading by magnitude that forces the tetrahedral frame.

## Why four legs

The match between 24 torsion components and 24 rearrangements depends on the number of legs $K$. Torsion has $K \binom{K}{2}$ components and there are $K!$ rearrangements. These are equal only for $K = 2$ and $K = 4$. At $K = 3$ there are 9 torsion components but only 6 rearrangements, and at $K = 5$ there are 50 against 120. So the regular-representation structure belongs to four-legged frames, the frames of four-dimensional spacetime, with only the trivial case $K = 2$ beside it.

## What it does not claim

The sign representation responds to *odd rearrangements of the legs*. That is not the same as *spatial parity*, the reflection $e \to -e$ of the spatial legs. Both reverse orientation, since both have determinant $-1$, but spatial parity is not a rearrangement, and these theorems do not describe how it acts. Earlier versions linked the sign representation directly to the parity between TetA and TetB. This version does not make that link, because the algebra does not establish it. What the torsion means physically in GFD is the framework's claim, developed in the letters listed below.

## Why it matters

- **It shows what general relativity removes.** Setting torsion to zero does not just delete 24 numbers. It deletes one complete copy of the group algebra of the legs, including the only sign response of the connection to odd rearrangements.
- **It is pure algebra.** Apart from the vector–axial–tensor placement, which uses the magnitude reading, nothing depends on any physical assumption. Theorems 1 and 2 hold for any four-index frame, with or without a metric.
- **It is constructive.** The isomorphism is written down: one explicit tensor generates all of torsion.
- **It singles out four.** The structure exists only for frames with four legs, apart from the trivial case of two.

## Earlier versions

The theorem appears in the [RAR letter's supplement](../../papers/letter-radial-acceleration-relation-sparc/supplementary/torsion_regular_representation_S4.tex) and in [Paper B](../../papers/algebraic-papers-a-b-c/gfd_paper_b_torsion_S4.tex), both proved by computing characters. Both are correct. This version:

- proves the theorem by construction, with an explicit generator, and keeps the character table only as a check;
- gives the explicit isomorphism and the bridge to the vector–axial–tensor decomposition, both listed as open in Paper B;
- locates the sign representation exactly, as the totally antisymmetric torsion;
- tightens the proof that only $K = 2$ and $K = 4$ work;
- grounds the $S_4$ action in the magnitude reading of the forced tetrahedral frame;
- separates the permutation sign from spatial parity and drops the link to root-blindness that the algebra does not support.

## Contents

| File | Contents |
|---|---|
| [`torsion_regular_representation.pdf`](torsion_regular_representation.pdf) | The proof, two pages |
| [`torsion_regular_representation.tex`](torsion_regular_representation.tex) | LaTeX source (IOP journal class, included) |
| [`verify_torsion_regular_representation.py`](verify_torsion_regular_representation.py) | Checks of the setting, the lemma, all three theorems, the corollary, the proposition and the scope statements, in integer arithmetic with exact ranks |
| [`iopjournal.cls`](iopjournal.cls) | Document class, so the source builds here |

```bash
pip install sympy numpy
python verify_torsion_regular_representation.py      # 36/36
pdflatex -interaction=nonstopmode torsion_regular_representation.tex
```

## Related

- [The forced tetrahedral frame](../forced-tetrahedral-frame/): the magnitude reading that makes the four legs equivalent.
- [The constitutive law from exchange symmetry](../constitutive-law-exchange-symmetry/): how the field is shared between TetA and TetB.
- [Letter 2: The Other Half of Gravity](../../papers/letter-2-other-half-of-gravity-torsion/) and [Letter 3: Field Closure of the Tetrad Frame](../../papers/letter-3-field-closure-of-tetrad-frame/): the role of torsion in GFD.

---

*The algebra is complete and machine-checked. The physical meaning of the torsion sector is GFD's, stated so that it can be tested.*
