# The Two Roots of the Tetrad Equation

*Why the equation of general relativity's frame has exactly two roots, and why keeping one is a convention · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`tetrad` `scheme` `algebraic-geometry` `Lorentz-group` `root-blindness` `spatial-parity` `stellated-octahedron` `proof`

---

This folder holds a two-page proof and a script that checks every step. The proof concerns the equation that defines the tetrad, the frame on which general relativity is built. Using the language of algebraic geometry founded by Grothendieck, it shows that the equation has exactly two roots, just as $x^2 = a$ does. Spatial parity carries one root to the other, nothing written in the metric can tell them apart, and in three dimensions they are the two tetrahedra of the stellated octahedron. The usual practice of keeping one root is therefore a convention, not something the equation demands. This page explains the argument for a reader with first-year linear algebra.

## The equation

General relativity can be written in terms of a *tetrad*: at every point of spacetime, four reference directions called legs, one along time and three along space. The tetrad $e$ is tied to the metric $g$, which measures lengths and angles, by

$$g = e^{T} \eta\, e, \qquad \eta = \mathrm{diag}(-1, +1, +1, +1).$$

This is the *tetrad equation*. The metric is built from the frame twice, so the tetrad is, in a precise sense, the square root of the metric. Square roots come in pairs, and the question is exactly what the pair is here.

## Where the two roots are

Take determinants of both sides. The determinant of a product is the product of the determinants, so

$$(\det e)^2 = \frac{\det g}{\det \eta} = c .$$

This is literally an equation of the form $y^2 = c$, with $c$ a positive number fixed by the metric. Its two roots are $\det e = +\sqrt c$ and $\det e = -\sqrt c$. Every tetrad has one of these two determinants, and no tetrad has both. The sign of $\det e$ is the frame's *orientation*: whether its legs are arranged right-handed or left-handed.

## What the proof shows

**1. The solutions fall into exactly two pieces, one per root.** Algebraic geometry treats the complete solution set of a system of equations as one object, called a *scheme*, with no root preferred. The proof shows the scheme of the tetrad equation has exactly two connected pieces, one over each root of $y^2 = c$. Neither piece splits further, even if complex numbers are allowed. So "two roots" is not a figure of speech: it is the exact number of pieces of the equation's solution set.

**2. Every solution comes from any other by a change of frame.** Rotations, boosts and reflections (the Lorentz group) turn any solution into any other, and there are no other solutions. A change of frame moves a tetrad to the other root exactly when it flips orientation.

**3. Parity is the map between the roots.** Time reversal and spatial parity both flip orientation, so both cross between the roots. To compare like with like, fix an observer and a direction of time. Then the changes of frame available are the rotations and reflections of that observer's space, and the ones that cross between the roots are exactly the reflections. Among those, only one treats every direction of space alike, in the sense that it commutes with every rotation and reflection: turning all three spatial directions around at once. That is spatial parity. It crosses between the roots because three is odd: flipping three directions flips the handedness. In two dimensions, flipping both directions is just a half turn, and parity would stay on the same root.

**4. The metric cannot tell the roots apart.** The metric fixes $(\det e)^2 = c$ and never the sign of $\det e$, just as $a$ fixes $x^2$ and never the sign of $x$. Every quantity built from the metric, including the curvature, Einstein's equations and the action they come from, takes exactly the same value on both roots. The textbook formulation restricts frames to the *proper orthochronous* Lorentz group, which stays on one root. That is a perfectly consistent choice, but no equation written in the metric can make it.

**5. In three dimensions the two roots are the two tetrahedra.** Letter 1 builds four directions from the three spatial legs of a frame. They point to the corners of a regular tetrahedron, TetA. Parity turns every one of them around, which gives TetA reflected through the origin: exactly the region Letter 1 calls TetB. Together they form the stellated octahedron. For frames whose time leg points to the future, the root of the frame decides which tetrahedron it carries. So Letter 1's second chamber is not added by hand; it is the equation's second root.

## Two honest caveats

**The tetrahedra have the same shape.** A regular tetrahedron is identical to its own mirror image, so as a shape TetB is just TetA turned: a quarter turn about one axis carries one set of corners onto the other. What the roots change is the order of the legs and the region of space the tetrahedron occupies, at one and the same observer. No rotation turns TetA into TetB leg by leg.

**Direction of time matters.** Turning every leg around, $e \to -e$, flips all four legs, time included. In four dimensions that leaves the determinant unchanged, $(-1)^4 = 1$, so $-e$ stays on the same root. Yet its spatial legs point the other way, so it carries TetB. The two statements are consistent because $-e$ also reverses the direction of time. That is why the proof states the root–tetrahedron match for future-pointing frames only. The map $e \to -e$ has a special status of its own, as the only change of frame that commutes with every other, but it is not the map between the roots.

## What each ingredient does

| Ingredient | What happens without it |
|---|---|
| A non-degenerate metric | $c = 0$, and $y^2 = 0$ has a single double root instead of two |
| An odd number of space dimensions | Parity stays on the same root; in two dimensions it is a half turn |
| Future-pointing frames | $-e$ carries TetB on the root of $e$ |
| Legs kept in order | As shapes, TetB is a rotation of TetA |

## Why it matters

**It is the algebraic foundation of the two chambers.** GFD's central structure is a pair of chambers, TetA and TetB. This proof shows that the pair is already present in the defining equation of general relativity's frame, as its two roots in the strict sense of algebraic geometry, before any physics is added.

**It locates the choice precisely.** General relativity keeps one root. The proof shows that the choice is consistent, that the metric cannot make it, and which convention makes it: restricting to the proper orthochronous Lorentz group. That is the starting point of [Einstein as the TetA partition](../../EINSTEIN_TETA_PARTITION.md) and of Letter 3.

**It ties the second chamber to three dimensions.** Parity is a new root only when the number of space dimensions is odd. Together with the [forced tetrahedral frame](../forced-tetrahedral-frame/), which shows that four legs have one shape only in three dimensions, both halves of the stellated octahedron are tied to $D = 3$.

## What it does not do

The proof is about the solutions of the tetrad equation at a point, and of tetrad fields pointwise. That the second root carries physical content, that TetB is a real sector of the gravitational field and torsion its carrier, is the framework's claim, developed in Letters 2 and 3. The proof shows that the second root exists, is reached by parity and is invisible to the metric; it does not by itself show that nature uses it.

## Earlier version

[*The Tetrad Scheme and the Two Bounded Regions*](../../papers/letter-1-tetrad-frame-geometry/Supplementary/supplementary_scheme_proof.tex), supplementary to Letter 1, makes the same argument in outline. Its central claim stands, and this version makes it unassailable:

- **It uses the scheme.** The earlier note named Grothendieck's schemes but argued with group theory alone. Here the scheme does the work: $(\det e)^2 = c$ splits it into exactly two pieces, and those pieces are the roots.
- **It proves "exactly two".** The earlier note reduced four pieces to two by restricting the Lorentz group to the spatial legs, which is not a well-defined step, since boosts mix time and space. Here the count follows from the determinant, and the four real pieces are explained as two roots times two directions of time.
- **It identifies parity as the canonical map.** The earlier note paired a frame with "the parity component", a whole continuum of frames. Here parity is singled out as the only reflection that commutes with every rotation and reflection of the observer's space.
- **It shows why three dimensions matter.** Parity crosses between the roots only for an odd number of space dimensions.
- **It names the right convention.** The earlier note attributed root selection to the choice between the sign conventions $(-,+,+,+)$ and $(+,-,-,-)$. That choice flips $\eta$ as a whole, leaves the Lorentz group unchanged and selects nothing. The convention that keeps one root is the restriction to the proper orthochronous group.
- **It sets aside the face-sign reading.** The earlier note read a $3 + 1$ split from the face normals' sign patterns. That split depends on the choice of axes, since all four faces of a regular tetrahedron are equivalent, so it is not part of a coordinate-free proof.

## Contents

| File | Contents |
|---|---|
| [`tetrad_equation_two_roots.pdf`](tetrad_equation_two_roots.pdf) | The proof, two pages |
| [`tetrad_equation_two_roots.tex`](tetrad_equation_two_roots.tex) | LaTeX source (IOP journal class, included) |
| [`verify_tetrad_equation_two_roots.py`](verify_tetrad_equation_two_roots.py) | Checks of the setting, both lemmas, all four theorems, the remark and every row of the scope table; exact where the statement is algebraic. One standard fact is cited rather than computed: the complex group $SO(4, \mathbb{C})$ is connected |
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

*Two roots of $(\det e)^2 = c$, exactly two pieces of the scheme, parity between them, and a metric that sees only $c$: each step proved and machine-checked.*
