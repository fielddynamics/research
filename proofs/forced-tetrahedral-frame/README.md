# The Spatial Geometry of the Lorentz Tetrad

*Why the frame of spacetime, drawn in space, has to be a regular tetrahedron · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`tetrad` `Gram-matrix` `regular-tetrahedron` `stellated-octahedron` `representation-theory` `proof`

---

This folder holds a two-page proof and a script that checks every step. The proof shows that the geometry at the centre of Gravity Field Dynamics, the regular tetrahedron and its parity partner the stellated octahedron, is not chosen. It is read off the metric of special relativity. This page explains the argument for a reader with first-year linear algebra.

## The question

General relativity describes gravity with a *tetrad*: at every point of spacetime, four reference directions called legs. One leg points along time and three point along space, like a clock and three rulers. The legs are measured against the Minkowski metric

$$\eta = \mathrm{diag}(-1, +1, +1, +1) ,$$

which says that each leg has unit length, that every pair of legs is perpendicular, and that the time leg differs from the others by a sign.

GFD builds on a particular shape, the stellated octahedron: two interlocking regular tetrahedra. A fair question is where that shape comes from. Is it a choice, or is it forced? This proof answers that it is forced, and identifies exactly what forces it.

## The key observation

Look at the metric again, but ignore the signs and keep only the sizes of its entries:

$$|\eta_{ab}| = \delta_{ab} .$$

This is the identity matrix. It says every leg has the same magnitude and every pair of legs has the same relation, perpendicular. Shuffle the four legs in any of the 24 possible ways and this pattern does not change. The metric itself survives only the 6 shuffles that keep the time leg in place. **The only thing that singles out time is a minus sign.**

Now try to draw the four legs as arrows in ordinary three-dimensional space. In ordinary space every arrow has a positive squared length, so there is no way to draw a minus sign. What can be carried over from the metric is the part without signs: four arrows that are all alike.

## The three premises

**(S) The legs are equivalent.** Shuffling the four arrows does not change the table of their lengths and angles. This is the shuffle symmetry of $|\eta|$, carried into space.

**(N) The legs are distinct.** The four arrows are not all the same arrow, just as the four legs of a tetrad are independent.

**(D) The arrows live in three dimensions.** This is the spatial part of the metric, its three $+1$ entries.

Notice what is *not* assumed. The proof does not assume the arrows have equal length, and it does not assume they add up to zero. Both come out of the argument.

## How the proof works

**Step 1: two numbers.** Record the arrows in a table of dot products, the *Gram matrix* $G_{ab} = v_a \cdot v_b$. The diagonal holds the squared lengths, and the off-diagonal entries hold the angles between pairs. If shuffling the arrows leaves the table unchanged, every diagonal entry must be the same and every off-diagonal entry must be the same, because any entry can be shuffled into any other of its kind. So the whole table is fixed by two numbers. In matrix form, $G = \alpha I + \beta J$, where $J$ is the matrix of all ones.

**Step 2: three dimensions are not enough for four independent arrows.** A matrix of this form has two kinds of eigenvalue: $\alpha$, which appears three times, and $\alpha + 4\beta$, which appears once. The number of nonzero eigenvalues is the number of independent directions the arrows span. Distinct arrows make $\alpha$ positive, so at least three directions are needed. Three-dimensional space has only three. So the fourth eigenvalue must vanish, $\alpha + 4\beta = 0$. That one equation says the four arrows add up to zero: they balance.

**Step 3: read off the shape.** With the arrows balanced, the angle between any two is fixed. The cosine is exactly $-1/3$, so the angle is about $109.47^\circ$. This is the tetrahedral angle, the same angle chemists find between the bonds of a methane molecule. Four arrows of equal length with this angle between every pair point to the corners of a regular tetrahedron.

**Step 4: nothing else is possible.** A second lemma shows that the table of lengths and angles determines the arrows completely, up to a rotation or reflection of the whole picture. So every configuration satisfying the premises is the same regular tetrahedron, turned some way in space.

## Why three dimensions

The argument works for any number of legs $K$ in any dimension $D$:

- If $D < K - 1$, there is no room: no configuration exists.
- If $D > K - 1$, there is too much room. The arrows no longer have to balance; for example, they can all be mutually perpendicular.
- Only when $D = K - 1$ does a configuration exist **and** have no freedom left.

For a tetrad, $K = 4$, so the spatial dimension must be $3$. Three is the one dimension in which four equivalent legs have exactly one shape.

## A second route

A careful reader might object to the shuffle symmetry: the metric keeps only the 6 shuffles that fix the time leg, not all 24. The proof answers this with a second route. Grant only those 6 shuffles, together with equal lengths, and add the condition that the arrows balance. The same regular tetrahedron follows. The time leg, which the metric sets apart by its sign, ends up geometrically identical to the spatial legs. So whichever symmetry a reader accepts, the conclusion is the same.

## The second tetrahedron

Spatial parity flips every arrow, $v \to -v$. Dot products are unchanged, because $(-v)\cdot(-w) = v \cdot w$, so the table cannot tell the flipped arrows from the originals. The flipped set is a second regular tetrahedron that shares no corner with the first. Together their eight corners are the corners of a cube, and the two tetrahedra interlock as Kepler's *stella octangula*, the stellated octahedron. In GFD these are TetA and TetB.

## Each premise is necessary

For each premise, the proof gives a configuration that satisfies the others and is not a regular tetrahedron:

| Premise removed | What becomes possible |
|---|---|
| Equivalence (S) | Four arrows $v, w, -v, -w$ with $v \perp w$: distinct, equal in length, balanced, in three dimensions, and a flat square |
| Distinctness (N) | All four arrows the same |
| Three dimensions (D) | In four dimensions, four mutually perpendicular arrows: the pattern $|\eta|$ itself, unbalanced. In two dimensions, nothing at all |
| Balance, in the second route | Three perpendicular arrows plus a fourth pointing between their negatives: symmetric under the 6 shuffles, but unbalanced |

## Why it matters

**The geometry is read, not chosen.** Everything in the result comes from the Minkowski metric: equivalence of the legs from the sizes of its entries, and the dimension from its three positive entries. The regular tetrahedron, the cube and the stellated octahedron follow with no further input. This is the foundation the rest of GFD stands on, so it matters that it carries no hidden choice.

**It assumes less than earlier versions and derives more.** Equal lengths and balance used to be premises; here they are consequences. The step from "same table" to "same shape" used to be cited; here it is proved in a few lines.

**It answers the obvious objection in advance.** The second route shows that a reader who accepts only the symmetry the metric itself preserves reaches the same tetrahedron.

**It explains the three in 3 + 1.** Three is the unique dimension in which four equivalent legs have one and only one shape.

## What it does not do

The proof is about realising the tetrad's legs as vectors in the spatial sector. That this realisation carries physical meaning, that TetA and TetB partition the gravitational field, is the framework's claim, developed in the letters and papers listed below. The proof also does not derive the coupling polynomial or the constitutive law; those build on this geometry. Its job is to show that, once the legs are drawn in space, the shape cannot be anything else.

## Earlier version

The [RAR letter's supplement](../../papers/letter-radial-acceleration-relation-sparc/supplementary/supplementary_spatial_geometry_of_the_lorentz_tetrad.tex) proves the same theorem from three conditions: common norm, balanced closure and $S_4$-invariance of the Gram matrix. That proof is correct. This version makes four changes:

- It drops common norm and closure as premises and derives them, using only distinctness and three dimensions.
- It grounds $S_4$-invariance in the magnitude pattern $|\eta| = I$, where the earlier version noted only that the signature is preserved by $S_3$, which invited an objection.
- It proves the rigidity step instead of citing it.
- It adds the dimension result, the second route through $S_3$, and a necessity table.

## Contents

| File | Contents |
|---|---|
| [`forced_tetrahedral_frame.pdf`](forced_tetrahedral_frame.pdf) | The proof, two pages |
| [`forced_tetrahedral_frame.tex`](forced_tetrahedral_frame.tex) | LaTeX source (IOP journal class, included) |
| [`verify_forced_tetrahedral_frame.py`](verify_forced_tetrahedral_frame.py) | Checks of the setting, both lemmas, the theorem, all three corollaries, the second route and every row of the necessity table |
| [`iopjournal.cls`](iopjournal.cls) | Document class, so the source builds here |

```bash
pip install sympy numpy
python verify_forced_tetrahedral_frame.py      # 27/27
pdflatex -interaction=nonstopmode forced_tetrahedral_frame.tex
```

## Related

- [The radial acceleration relation letter](../../papers/letter-radial-acceleration-relation-sparc/), whose supplement holds the earlier version.
- [Letter 1: The Coordinate-Space Geometry of the Tetrad Frame](../../papers/letter-1-tetrad-frame-geometry/), including the [signature-to-frame supplement](../../papers/letter-1-tetrad-frame-geometry/Supplementary/supplementary_signature_to_frame.tex), which reaches the same tetrahedron from isotropy of directions on the null cone.
- [The Gram Matrix of the Tetrad Equation](../../papers/gram-matrix-of-tetrad-equation/): the two roots of the tetrad equation and their Gram products.
- [The constitutive law from exchange symmetry](../constitutive-law-exchange-symmetry/): the partition of the field between the two tetrahedra.

---

*The algebra is complete and machine-checked. The physical reading of the realisation is GFD's, stated so that it can be tested.*
