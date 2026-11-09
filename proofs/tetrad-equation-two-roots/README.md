# The Two Roots of the Tetrad Equation

*Why the equation of general relativity's frame has two roots, and why keeping one is a convention · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`tetrad` `Lorentz-group` `root-blindness` `spatial-parity` `algebraic-geometry` `stellated-octahedron` `proof`

---

This folder holds a two-page proof and a script that checks every step. The proof concerns the equation that defines the tetrad, the frame on which general relativity is built. It shows that the equation has two roots, just as $x^2 = a$ does. It shows that the second root is genuinely different from the first because space has three dimensions, and that nothing written in the metric can tell the two apart. The usual practice of keeping one root is therefore a convention, not something the equation demands. This page explains the argument for a reader with first-year linear algebra.

## The equation

General relativity can be written in terms of a *tetrad*: at every point of spacetime, four reference directions called legs, one along time and three along space. The tetrad $e$ is tied to the metric $g$, which measures lengths and angles, by

$$g = e^{T} \eta\, e, \qquad \eta = \mathrm{diag}(-1, +1, +1, +1).$$

This is the *tetrad equation*. The metric is built from the frame twice, so the tetrad is, in a precise sense, the square root of the metric.

That has a consequence everyone knows from school algebra. The equation $x^2 = a$ has two roots, $+\sqrt a$ and $-\sqrt a$, because squaring hides the sign. The tetrad equation hides a sign in the same way: if $e$ solves it, so does $-e$, since $(-e)^T \eta (-e) = e^T \eta\, e$. Algebraic geometry, the branch of mathematics founded on Grothendieck's work, treats the complete solution set of an equation as one object, with no root preferred. This proof works out what that solution set looks like for the tetrad equation.

## What the proof shows

**1. All the solutions come from one.** Every solution is obtained from any other by a Lorentz transformation, a change of frame made of rotations, boosts and reflections. There are no other solutions. So the solution set looks exactly like the Lorentz group itself.

**2. The solutions split into exactly two classes.** The Lorentz group has four pieces that cannot be joined smoothly. A single sign, built from two simple numbers of each transformation (its determinant, and whether it keeps the future in the future), sorts those four pieces into two classes. Inside a class, frames can be turned into each other while keeping their spatial handedness. Between classes, the handedness flips. Time reversal stays inside a class, because it touches only the time leg. A mirror reflection crosses between them.

**3. The second root is in the other class because three is odd.** Flipping all three spatial directions multiplies the handedness by $(-1)^3 = -1$, so $-e$ lands in the opposite class from $e$. In a world with an even number of space dimensions, flipping every direction is just a rotation (in two dimensions it is a half turn), and $-e$ would be nothing new. In our three dimensions it is genuinely new.

**4. The second root is the canonical one.** Many transformations relate $e$ to frames in the other class, so why single out $-e$? Because it is the only partner of $e$ that every observer agrees on. Turning every leg around is the one operation that gives the same answer whatever change of frame you make first. In group language, $\pm I$ is the *centre* of the Lorentz group. Spatial parity, which flips the three space legs and leaves time alone, is not like this: a boost changes it. Parity is $-e$ with the time leg turned back, and it is how one particular observer sees the second root.

**5. The metric cannot tell the roots apart.** Every quantity built from the metric, including the curvature, Einstein's equations and the action they come from, takes exactly the same value on both roots. The textbook formulation restricts frames to the *proper orthochronous* Lorentz group, which keeps one piece and excludes $-e$. That is a perfectly consistent choice, but no equation written in the metric can make it. It is a convention laid on top.

**6. In three dimensions the two roots are the two tetrahedra.** Letter 1 builds four directions from the three spatial legs of a frame. They point to the corners of a regular tetrahedron, TetA. The second root turns every one of them around, which gives TetA reflected through the origin: exactly the region Letter 1 calls TetB. No rotation turns TetA into TetB leg by leg. Together they form the stellated octahedron. So Letter 1's second chamber is not added by hand; it is the equation's second root.

## An honest caveat

A regular tetrahedron is identical to its own mirror image, so as a shape TetB is just TetA turned. A quarter turn about one axis carries one set of corners onto the other. What the second root changes is not the shape but the order of the legs and the region of space the tetrahedron occupies, at one and the same observer. The proof states this explicitly, because a weaker claim stated precisely is stronger than a stronger claim that a referee can knock over. (An exploratory test in Letter 1's research folder claims that no rotation maps TetA onto TetB; as a statement about point sets that test is mistaken, and this proof replaces it with the correct statement about ordered legs.)

## What each ingredient does

| Ingredient | What happens without it |
|---|---|
| A non-degenerate metric | If the metric is degenerate the solutions need not come from one another; for $g = 0$ in two dimensions, both $e = 0$ and a non-zero frame solve the equation |
| An odd number of space dimensions | The second root falls in the same class as the first; in two dimensions it is a half turn |
| Legs kept in order | As shapes, TetB is a rotation of TetA |

## Why it matters

**It is the algebraic foundation of the two chambers.** GFD's central structure is a pair of chambers, TetA and TetB. This proof shows that the pair is already present in the defining equation of general relativity's frame, as its two roots, before any physics is added.

**It locates the choice precisely.** General relativity keeps one root. The proof shows that the choice is consistent, that the metric cannot make it, and exactly which convention makes it: restricting to the proper orthochronous Lorentz group. That is the starting point of [Einstein as the TetA partition](../../EINSTEIN_TETA_PARTITION.md) and of Letter 3.

**It explains the role of three dimensions.** The second root is new only when the number of space dimensions is odd. Combined with the [forced tetrahedral frame](../forced-tetrahedral-frame/), which shows that four legs have one shape only in three dimensions, both halves of the stellated octahedron are tied to $D = 3$.

## What it does not do

The proof is about the solutions of the tetrad equation at a point, and of tetrad fields pointwise. That the second root carries physical content, that TetB is a real sector of the gravitational field and torsion its carrier, is the framework's claim, developed in Letters 2 and 3. The proof shows the second root exists, is canonical and is invisible to the metric; it does not by itself show that nature uses it.

## Earlier version

[*The Tetrad Scheme and the Two Bounded Regions*](../../papers/letter-1-tetrad-frame-geometry/Supplementary/supplementary_scheme_proof.tex), supplementary to Letter 1, makes the same argument in outline. Its central claim stands, and this version makes it unassailable:

- **It proves "exactly two".** The earlier note reduced four components to two by restricting the Lorentz group to the spatial legs, which is not a well-defined step, since boosts mix time and space. Here a sign defined on the whole group does the job, with a short lemma.
- **It identifies the canonical root.** The earlier note paired a frame with "the parity component", which is a whole continuum of frames. Here the partner is $-e$, the one every observer agrees on, and parity is shown to be how one observer sees it.
- **It shows why three dimensions matter.** The second root is new only for an odd number of space dimensions, a fact the earlier note did not address.
- **It names the right convention.** The earlier note attributed root selection to the choice between the sign conventions $(-,+,+,+)$ and $(+,-,-,-)$. That choice flips $\eta$ as a whole, leaves the Lorentz group unchanged and selects nothing. The convention that keeps one root is the restriction to the proper orthochronous group, and this version says so.
- **It uses "scheme" exactly.** The equation defines a scheme; the proof works with its real points, the solution set, and claims nothing beyond them.
- **It sets aside the face-sign reading.** The earlier note read a $3 + 1$ split from the face normals' sign patterns. That split depends on the choice of axes, since all four faces of a regular tetrahedron are equivalent, so it is not part of a coordinate-free proof.

## Contents

| File | Contents |
|---|---|
| [`tetrad_equation_two_roots.pdf`](tetrad_equation_two_roots.pdf) | The proof, two pages |
| [`tetrad_equation_two_roots.tex`](tetrad_equation_two_roots.tex) | LaTeX source (IOP journal class, included) |
| [`verify_tetrad_equation_two_roots.py`](verify_tetrad_equation_two_roots.py) | Checks of the setting, both lemmas, all four theorems, the remark and every row of the scope table; exact where the statement is algebraic |
| [`iopjournal.cls`](iopjournal.cls) | Document class, so the source builds here |

```bash
pip install sympy numpy
python verify_tetrad_equation_two_roots.py      # 35/35
pdflatex -interaction=nonstopmode tetrad_equation_two_roots.tex
```

## Related

- [Letter 1: The Coordinate-Space Geometry of the Tetrad Frame](../../papers/letter-1-tetrad-frame-geometry/), which reaches the same two tetrahedra by half-spaces, and whose supplement holds the earlier version.
- [The forced tetrahedral frame](../forced-tetrahedral-frame/): why the four directions form a regular tetrahedron.
- [The Gram Matrix of the Tetrad Equation](../../papers/gram-matrix-of-tetrad-equation/): root-blindness and the cross-coupling of the two roots.
- [Einstein's equation as the TetA partition](../../EINSTEIN_TETA_PARTITION.md): what follows from keeping one root.

---

*Two roots, exactly two classes, one canonical partner, and a metric that cannot tell them apart: each step proved and machine-checked.*
