# The Spatial Geometry of the Lorentz Tetrad

*Why the frame of spacetime, drawn in space, has to be a regular tetrahedron · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`tetrad` `Gram-matrix` `regular-tetrahedron` `stellated-octahedron` `proof`

---

This folder holds a two-page proof and a script that checks every step. The proof shows that the geometry at the centre of Gravity Field Dynamics, the regular tetrahedron and its parity partner the stellated octahedron, is not chosen. It is read off the metric of special relativity. This page explains the argument for a reader with first-year linear algebra.

## The question

General relativity describes gravity with a *tetrad*: at every point of spacetime, four reference directions called legs. One leg points along time and three point along space, like a clock and three rulers. The legs are measured against the Minkowski metric

$$\eta = \mathrm{diag}(-1, +1, +1, +1) ,$$

which says three things: each leg has unit size, every pair of legs is perpendicular, and the time leg differs from the others by a minus sign.

GFD builds on a particular shape, the stellated octahedron: two interlocking regular tetrahedra. A fair question is where that shape comes from. Is it a choice, or is it forced? This proof shows that it is forced, and it identifies exactly what forces it.

## Drawing the legs in space

Try to draw the four legs as arrows in ordinary three-dimensional space. Two of the metric's three statements cannot be copied exactly:

- **Four mutually perpendicular arrows do not fit in three dimensions.** What can be kept is that *every pair of arrows bears the same relation*, because in the metric every pair, time with space and space with space, has the same entry, zero.
- **No arrow has a negative squared length.** So the minus sign of the time leg cannot be drawn. What can be kept is that *every arrow has the same length*, because every leg has unit size.

The drawing keeps the *pattern* of the metric's entries, which are all alike, and not their *values*, which three-dimensional space cannot hold.

## The four premises

**(R) Equal relation.** Every pair of arrows has the same dot product. This is the metric's off-diagonal entries, all zero, which carry no sign at all.

**(M) Equal magnitude.** Every arrow has the same length. This is the size of the metric's diagonal entries, with the time leg's minus sign set aside.

**(N) Distinct legs.** The four arrows are not all the same arrow, just as the four legs of a tetrad are independent.

**(D) Three dimensions.** The arrows live in the spatial part of spacetime, which has three dimensions, one for each $+1$ in the metric.

Notice what is *not* assumed: the proof does not assume that the arrows add up to zero. That comes out of the argument.

## How the proof works

**Step 1: two numbers.** Record the arrows in a table of dot products, the *Gram matrix* $G_{ab} = v_a \cdot v_b$. The diagonal holds the squared lengths and the off-diagonal entries hold the relations between pairs. Premises (M) and (R) say the diagonal is a single number and the off-diagonal is a single number. In matrix form, $G = \alpha I + \beta J$, where $J$ is the matrix of all ones. Equivalently, shuffling the four arrows in any of the 24 possible ways leaves the table unchanged.

**Step 2: three dimensions are not enough for four independent arrows.** A matrix of this form has two kinds of eigenvalue: $\alpha$, which appears three times, and $\alpha + 4\beta$, which appears once. The number of nonzero eigenvalues is the number of independent directions the arrows span. Distinct arrows make $\alpha$ positive, so at least three directions are needed. Three-dimensional space has only three. So the fourth eigenvalue must vanish, $\alpha + 4\beta = 0$. That one equation says the four arrows add up to zero: they balance.

**Step 3: read off the shape.** With the arrows balanced, the angle between any two is fixed. Its cosine is exactly $-1/3$, so the angle is about $109.47^\circ$. This is the tetrahedral angle, the same angle chemists find between the bonds of a methane molecule. Four arrows of equal length with this angle between every pair point to the corners of a regular tetrahedron.

**Step 4: nothing else is possible.** A short lemma shows that the table of lengths and angles determines the arrows completely, up to a rotation or reflection of the whole picture. So every configuration satisfying the premises is the same regular tetrahedron, turned some way in space.

## Why three dimensions

The argument works for any number of legs $K$ in any dimension $D$:

- If $D < K - 1$, there is no room: no configuration exists.
- If $D > K - 1$, there is too much room. The arrows no longer have to balance; for example, they can all be mutually perpendicular.
- Only when $D = K - 1$ does a configuration exist **and** have no freedom left.

For a tetrad, $K = 4$, so the spatial dimension must be $3$. Three is the one dimension in which four legs alike have exactly one shape.

## The one place a choice is made, and what it decides

Three of the premises copy the tetrad as it stands. Equal relation copies entries that have no sign. Distinctness is the independence of the legs. The dimension is the spatial sector. The only premise that involves a decision is equal magnitude, because it sets aside the minus sign of the time leg.

The proof does not hide that decision. It shows exactly what it decides. Drop equal magnitude, and the other three premises admit an *observer's view* of the tetrad: the time leg shrinks to nothing, and the three spatial legs become three perpendicular rulers. That is how a single observer sees the frame, with time not drawn in space at all. Keep equal magnitude, treating all four legs as units, and the tetrahedron is forced.

So the theorem states precisely what it rests on: **read by magnitude, the four legs of spacetime, drawn in space, can only be a regular tetrahedron.** Reading the frame by magnitude, so that all four legs count equally, is GFD's reading, and the necessity table shows it is the only premise that separates the tetrahedron from an observer's view.

## The second tetrahedron

Spatial parity reflects all of space through the origin, so it sends every arrow drawn in space to its opposite, $v \to -v$. Dot products are unchanged, because $(-v)\cdot(-w) = v \cdot w$, so the table cannot tell the reflected arrows from the originals. The reflected set is a second regular tetrahedron that shares no corner with the first. Together their eight corners are the corners of a cube, and the two tetrahedra interlock as Kepler's *stella octangula*, the stellated octahedron. In GFD these are TetA and TetB.

## Each premise is necessary

For each premise, the proof gives a configuration that satisfies the other three and is not a regular tetrahedron:

| Premise removed | What becomes possible |
|---|---|
| Equal relation (R) | Four arrows $v, w, -v, -w$ with $v \perp w$: equal lengths, distinct, balanced, in three dimensions, and a flat square |
| Equal magnitude (M) | The observer's view: time leg zero, spatial legs perpendicular. Even with every arrow nonzero, unequal lengths are possible: squared lengths $1, 3, 7, 7$ with every dot product $-1$ |
| Distinctness (N) | All four arrows the same |
| Three dimensions (D) | In four dimensions, four mutually perpendicular arrows, unbalanced. In two dimensions, nothing at all |

## Why it matters

**The geometry is read, not chosen.** The regular tetrahedron, the cube and the stellated octahedron follow from the pattern of the Minkowski metric, with no further input. This is the foundation the rest of GFD stands on, so it matters that it carries no hidden choice. The one reading it does make, by magnitude, is stated openly, and its alternative is shown.

**It assumes less than the earlier version and derives more.** Balance used to be a premise; here it is a consequence of three dimensions. The step from "same table" to "same shape" used to be cited; here it is proved in a few lines. The symmetry condition used to be stated as invariance under all 24 shuffles, which invites the objection that the metric preserves only 6. Here it is replaced by two plain readings of the metric's entries, and the shuffle symmetry follows from them.

**It explains the three in 3 + 1.** Three is the unique dimension in which four legs alike have one and only one shape.

## What it does not do

The proof is about drawing the tetrad's legs as vectors in the spatial sector, read by magnitude. That this drawing carries physical meaning, that TetA and TetB partition the gravitational field, is the framework's claim, developed in the letters and papers listed below. The proof also does not derive the coupling polynomial or the constitutive law; those build on this geometry.

## Earlier version

The [RAR letter's supplement](../../papers/letter-radial-acceleration-relation-sparc/supplementary/supplementary_spatial_geometry_of_the_lorentz_tetrad.tex) proves the same theorem from three conditions: common norm, balanced closure and $S_4$-invariance of the Gram matrix. That proof is correct. This version makes four changes:

- It derives closure instead of assuming it, using distinctness and three dimensions.
- It replaces $S_4$-invariance with two readings of $\eta$'s entries, equal relation and equal magnitude, and isolates the second as the one place where the sign is set aside.
- It proves the rigidity step instead of citing it.
- It adds the dimension result and a necessity table, including the observer's view as the alternative to equal magnitude.

## Contents

| File | Contents |
|---|---|
| [`forced_tetrahedral_frame.pdf`](forced_tetrahedral_frame.pdf) | The proof, two pages |
| [`forced_tetrahedral_frame.tex`](forced_tetrahedral_frame.tex) | LaTeX source (IOP journal class, included) |
| [`verify_forced_tetrahedral_frame.py`](verify_forced_tetrahedral_frame.py) | Checks of the setting, the premises, the lemma, the theorem, all three corollaries and every row of the necessity table |
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

*The algebra is complete and machine-checked. The one reading it makes, by magnitude, is stated, and its alternative is shown.*
