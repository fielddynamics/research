# The Spatial Geometry of the Lorentz Tetrad

*Why the frame of spacetime, drawn in space, has to be a regular tetrahedron · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`tetrad` `Gram-matrix` `regular-tetrahedron` `stellated-octahedron` `proof`

[![Lean proof](https://github.com/fielddynamics/research/actions/workflows/lean-forced-tetrahedral-frame.yml/badge.svg)](https://github.com/fielddynamics/research/actions/workflows/lean-forced-tetrahedral-frame.yml)

---

This folder holds a three-page proof, a script that checks every step, and a Lean 4 formalisation in which every statement of the proof is machine-checked. The proof shows that the geometry at the centre of Gravity Field Dynamics, the regular tetrahedron and its parity partner the stellated octahedron, is not chosen. It is read off the metric of special relativity. This page explains the argument for a reader with first-year linear algebra.

## The question

General relativity describes gravity with a *tetrad*: at every point of spacetime, four reference directions called legs. One leg points along time and three point along space, like a clock and three rulers. The legs are measured against the Minkowski metric

$$\eta = \mathrm{diag}(-1, +1, +1, +1) ,$$

which says three things: each leg has unit size, every pair of legs is perpendicular, and the time leg differs from the others by a minus sign.

GFD builds on a particular shape, the stellated octahedron: two interlocking regular tetrahedra. A fair question is where that shape comes from. Is it a choice, or is it forced? This proof shows that it is forced, and it identifies exactly what forces it.

## Drawing the legs in space

Try to draw the four legs as arrows in ordinary three-dimensional space. Two of the metric's three statements cannot be copied exactly:

- **Four mutually perpendicular arrows do not fit in three dimensions.** What can be kept is that *every pair of arrows bears the same relation*, because in the metric every pair, time with space and space with space, has the same entry, zero.
- **No arrow has a negative squared length.** So the minus sign of the time leg cannot be drawn. What can be kept is that *every arrow has the same length*, because every leg is a unit vector. The time leg's $-1$ is the same size, $1$, carrying the sign of a timelike vector: the sign says what kind of vector it is, not that there is less of it.

The drawing keeps the *pattern* of the metric's entries, which are all alike, and not their *values*, which three-dimensional space cannot hold.

## The four premises

**(R) Equal relation.** Every pair of arrows has the same dot product. This is the metric's off-diagonal entries, all zero, which carry no sign at all.

**(M) Equal magnitude.** Every arrow has the same length. Every leg of a tetrad is a unit vector, so the metric's diagonal entries all have size $1$; the time leg's $-1$ is that $1$ with a timelike sign. Equal magnitude keeps the $1$ and sets aside only the sign, which no length can carry.

**(N) Distinct legs.** The four arrows are not all the same arrow. The four legs of a tetrad form a basis, so they are certainly distinct; the premise asks for less.

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

For a tetrad, $K = 4$, so the spatial dimension must be $3$. Three is the one dimension in which four legs alike have exactly one shape. The count needs at least two legs; with a single leg, "not all the same" cannot hold.

The same argument covers a metric with one time direction and $n$ space directions, signature $(1, n)$: its $n + 1$ legs, drawn in the $n$ spatial dimensions, are forced to the regular $n$-simplex.

## What equal magnitude reads, and what it rules out

Three of the premises copy the tetrad as it stands. Equal relation copies entries that have no sign. Distinctness is the independence of the legs. The dimension is the spatial sector. Equal magnitude reads the size of each diagonal entry, and that size is not in doubt: a tetrad is a basis of unit vectors, the time leg included. Its $-1$ is $-(1)$, the same unit with the sign of a timelike vector, just as $1$ is not written $1/1$. The only thing set aside is the sign, because no squared length can be negative.

The proof shows what this rules out. Drop equal magnitude, and the other three premises admit an *observer's view* of the tetrad: the time leg shrinks to nothing, and the three spatial legs become three perpendicular rulers. That view does not merely drop a sign. It sends a unit vector to the zero vector. Keep every leg at its unit size, and the tetrahedron is forced.

The paper states this as a theorem about any tetrad, boosted or rotated. If the drawing gives each leg a length in proportion to its magnitude, and equal relations equal dot products, then the drawing is the regular tetrahedron. A second, independent route reaches the same premises from three requirements on how the metric is drawn: each entry drawn on its own, the same rule for every leg so that it does not matter where the time leg sits, and one picture for both sign conventions, $(-,+,+,+)$ and $(+,-,-,-)$. Since the time leg's entry changes sign between conventions, it must be drawn at the same size as the others. Each requirement is shown to be necessary.

So the theorem rests on one principle, stated openly: **the drawing keeps everything a squared length can carry.** That is the magnitudes and the relations, everything in the metric except the sign. From it, the four legs of spacetime, drawn in space, can only be a regular tetrahedron.

## The second tetrahedron

Spatial parity reflects all of space through the origin, so it sends every arrow drawn in space to its opposite, $v \to -v$. Dot products are unchanged, because $(-v)\cdot(-w) = v \cdot w$, so the table cannot tell the reflected arrows from the originals. The reflected set is a second regular tetrahedron that shares no corner with the first. Together their eight corners are the corners of a cube, and the two tetrahedra interlock as Kepler's *stella octangula*, the stellated octahedron. In GFD these are TetA and TetB.

## Each premise is necessary

For each premise, the proof gives a configuration that satisfies the other three and is not a regular tetrahedron:

| Premise removed | What becomes possible |
|---|---|
| Equal relation (R) | Four arrows $v, w, -v, -w$ with $v \perp w$: equal lengths, distinct, balanced, in three dimensions, and a flat square |
| Equal magnitude (M) | The observer's view: time leg zero, spatial legs perpendicular. Even with every arrow nonzero, unequal lengths are possible: the arrows $(-1,0,0)$, $(1,1,1)$, $(1,-1\pm\sqrt2,-1\mp\sqrt2)$ have squared lengths $1, 3, 7, 7$ and every dot product $-1$ |
| Distinctness (N) | All four arrows the same |
| Three dimensions (D) | In four dimensions, four mutually perpendicular arrows, unbalanced. In two dimensions, nothing at all |

## Machine-checked in Lean

The Python script checks each algebraic step. The [`lean/`](lean/) folder goes further: it states the whole proof in [Lean 4](https://lean-lang.org) with the [Mathlib](https://github.com/leanprover-community/mathlib4) library, and the Lean kernel checks every line of every argument. Nothing is taken on trust, not even the textbook lemmas.

What the formalisation establishes:

- **Every result of the paper**: the rigidity lemma, the forced Gram matrix with closure, all three corollaries with their uniqueness statements, and every row of the necessity table, including the rank of the $(1, 3, 7, 7)$ example.
- **The premises from the tetrad**: the legs form a basis, every leg is a unit vector, and a drawing that keeps magnitudes and relations is forced to the tetrahedron for any tetrad.
- **Every premise and requirement is needed, and none is vacuous**: each has a counterexample when dropped, and together they are satisfied by the tetrahedron itself.
- **Nothing tuned to four legs**: the general statement for signature $(1, n)$.

The build has no errors, no warnings and no gaps (`sorry`), and depends only on Lean's three standard axioms. GitHub re-checks the proof automatically whenever the Lean files change, and the badge at the top of this page shows the result of the latest run: it is green only if the proof builds with no warnings, no gaps and only the standard axioms. [`LEAN_AUDIT.md`](LEAN_AUDIT.md) is a referee's guide: the definitions to check against the paper, each claim mapped to its Lean theorem, anticipated objections, and the limits of the formalisation.

Four other formalisations import this one rather than restating it: the [Hadamard cube frame](../hadamard-cube-frame/), the [half-space regions](../half-space-two-bounded-regions/), the [tetrad scheme](../tetrad-scheme-two-bounded-regions/) and the [Gram matrix of the tetrad equation](../gram-matrix-tetrad-equation/). Their checks re-run whenever this proof changes.

## Why it matters

**A frame that was never given a shape has one, and only one.** General relativity uses the tetrad through the metric alone, which fixes how the legs relate and says nothing about a shape. No standard result assigns a Lorentz frame a geometry. That four equal arrows at equal angles form a regular tetrahedron is classical geometry; that the tetrad's own data *force* those conditions is the new result. Without it, the four directions on which [Letter 1](../../papers/letter-1-tetrad-frame-geometry/) builds TetA, TetB and the stellated octahedron would be a choice. With it, they are forced.

**The geometry is read, not chosen.** The regular tetrahedron, the cube and the stellated octahedron follow from the Minkowski metric: its legs are unit vectors, and every pair is alike. This is the foundation the rest of GFD stands on, so it matters that it carries no hidden choice. The one principle it rests on, that the drawing keeps everything a squared length can carry, is stated openly, its alternative is shown, and every step from it is machine-checked.

**It assumes less than the earlier version and derives more.** Balance used to be a premise; here it is a consequence of three dimensions. The step from "same table" to "same shape" used to be cited; here it is proved in a few lines. The symmetry condition used to be stated as invariance under all 24 shuffles, which invites the objection that the metric preserves only 6. Here it is replaced by two plain readings of the metric's entries, and the shuffle symmetry follows from them.

**It explains the three in 3 + 1.** Three is the unique dimension in which four legs alike have one and only one shape.

## What it does not do

The proof is about drawing the tetrad's legs as vectors in the spatial sector, at their unit magnitude. Lean verifies the mathematics, not the physical reading. That this drawing carries physical meaning, that TetA and TetB partition the gravitational field, is the framework's claim, developed in the letters and papers listed below. The proof also does not derive the coupling polynomial or the constitutive law; those build on this geometry.

## Earlier versions

Two earlier derivations reach the same tetrahedron by imposing conditions that this version derives.

- **Letter 1's null-cone route.** The [signature-to-frame supplement](../../papers/letter-1-tetrad-frame-geometry/Supplementary/supplementary_signature_to_frame.tex) takes four null directions on the sphere and assumes they have no net direction (zero centroid) and no preferred axis (isotropic second moment).
- **The RAR letter's supplement.** [Supplementary Proof A](../../papers/letter-radial-acceleration-relation-sparc/supplementary/supplementary_spatial_geometry_of_the_lorentz_tetrad.tex) proves the same theorem from three conditions: common norm, balanced closure and $S_4$-invariance of the Gram matrix. That proof is correct.

This version makes these changes:

- It derives closure instead of assuming it, using distinctness and three dimensions.
- It replaces $S_4$-invariance with two readings of $\eta$'s entries, equal relation and equal magnitude, and reads equal magnitude as the normalisation of the frame: every leg is a unit vector.
- It proves the rigidity step instead of citing it.
- It adds the dimension result and a necessity table, including the observer's view as the alternative to equal magnitude.
- It is machine-checked in Lean.

The routes agree. Letter 1's four null directions are the columns of $M$ divided by $\sqrt 3$. The [Hadamard cube proof](../hadamard-cube-frame/) shows that bordering $M$ with a row of ones gives a Hadamard matrix, whose columns satisfy this proof's forced Gram matrix and whose rows are exactly Letter 1's two conditions. The legs, read here, and the null directions, read there, are two readings of one geometry.

## Contents

| File | Contents |
|---|---|
| [`forced_tetrahedral_frame.pdf`](forced_tetrahedral_frame.pdf) | The proof, three pages |
| [`forced_tetrahedral_frame.tex`](forced_tetrahedral_frame.tex) | LaTeX source (IOP journal class, included); v2 edits are marked `% v2:` |
| [`verify_forced_tetrahedral_frame.py`](verify_forced_tetrahedral_frame.py) | Checks of the setting, the premises, the lemma, the theorem, all three corollaries, every row of the necessity table, and the v2 additions |
| [`iopjournal.cls`](iopjournal.cls) | Document class, so the source builds here |
| [`lean/ForcedTetrahedralFrame.lean`](lean/ForcedTetrahedralFrame.lean) | The Lean 4 formalisation of every statement |
| [`lean/TetrahedralAngle.lean`](lean/TetrahedralAngle.lean) | The angle $\arccos(-1/3)$ between any two legs, in Mathlib's own sense of the angle between vectors |
| [`lean/lakefile.toml`](lean/lakefile.toml), [`lean/lean-toolchain`](lean/lean-toolchain), [`lean/lake-manifest.json`](lean/lake-manifest.json) | Project files pinning Lean 4.36.0 and Mathlib v4.36.0 |
| [`LEAN_AUDIT.md`](LEAN_AUDIT.md) | Referee's guide to the formalisation |

```bash
pip install sympy numpy
python verify_forced_tetrahedral_frame.py      # 36/36
pdflatex -interaction=nonstopmode forced_tetrahedral_frame.tex

# Lean (needs elan: https://github.com/leanprover/elan)
cd lean
lake exe cache get    # downloads Mathlib, already compiled
lake build            # checks every theorem
```

## Related

- [The radial acceleration relation letter](../../papers/letter-radial-acceleration-relation-sparc/), whose supplement holds the earlier version.
- [Letter 1: The Coordinate-Space Geometry of the Tetrad Frame](../../papers/letter-1-tetrad-frame-geometry/), including the [signature-to-frame supplement](../../papers/letter-1-tetrad-frame-geometry/Supplementary/supplementary_signature_to_frame.tex), which reaches the same tetrahedron from isotropy of directions on the null cone.
- [The Gram Matrix of the Tetrad Equation](../../papers/gram-matrix-of-tetrad-equation/): the two roots of the tetrad equation and their Gram products.
- [The constitutive law from exchange symmetry](../constitutive-law-exchange-symmetry/): the partition of the field between the two tetrahedra.

---

*The algebra is complete and machine-checked, in Python step by step and in Lean in full. The one principle it rests on is stated, and its alternative is shown.*
