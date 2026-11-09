# The Tetrad Scheme and the Two Bounded Regions

*Why the tetrad equation has two roots, and why they are the two tetrahedra of the stellated octahedron · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`tetrad` `scheme` `algebraic-geometry` `Lorentz-group` `spatial-parity` `root-blindness` `stellated-octahedron` `proof`

---

This folder holds the revised scheme proof, supplementary to Letter 1, and a script that checks every claim in it. The proof gives the second of Letter 1's two routes to the stellated octahedron. Route 1, in the letter, classifies sixteen half-space regions and finds exactly two bounded. Route 2, here, starts from the equation that defines the tetrad: the equation is quadratic, so it has two roots, and the two roots are the two tetrahedra. This page explains the argument for a reader with first-year linear algebra.

## The equation is quadratic

General relativity can be written in terms of a *tetrad*: at every point of spacetime, four reference directions called legs, one along time and three along space. The tetrad $e$ is tied to the metric $g$, which measures lengths and angles, by

$$g = e^{T} \eta\, e, \qquad \eta = \mathrm{diag}(-1, +1, +1, +1).$$

The metric is built from the frame twice, so the tetrad is, in a precise sense, the square root of the metric. Any change of frame that preserves $\eta$, a Lorentz transformation, turns one solution into another, and the note shows there are no other solutions.

Algebraic geometry, the branch of mathematics founded on Grothendieck's work, treats the complete solution set of an equation as one object, called its *scheme*, with no root preferred. The proof works out what the scheme of the tetrad equation looks like.

## The two roots

Take determinants of both sides of the equation:

$$(\det e)^2 = \frac{\det g}{\det \eta} = \kappa .$$

This is literally an equation of the form $y^2 = \kappa$, with $\kappa$ a positive number fixed by the metric. Its two roots are $\det e = +\sqrt\kappa$ and $\det e = -\sqrt\kappa$. Every tetrad has one of these two determinants, and none has both. So the scheme falls into two pieces, one per root. The proof shows neither piece breaks up further, even if complex numbers are allowed. The tetrad equation has exactly two roots, in the strict sense of algebraic geometry.

## Parity carries one root to the other

A change of frame moves a tetrad to the other root exactly when it flips the frame's orientation, its handedness. Spatial parity, which turns all three spatial legs around, does this because three is odd. In two dimensions, turning both legs around is just a half turn and would stay on the same root.

Hold one observer and the direction of time fixed, as Letter 1 does. The remaining changes of frame are the rotations and reflections of that observer's space. Rotations keep the root. They turn the four tetrahedral directions rigidly and produce nothing new. Reflections cross to the other root, and among them parity is the canonical one: it is the only reflection that treats every direction of space alike, commuting with every rotation and reflection. Parity sends each of the four directions to its opposite, which turns TetA into exactly the region Letter 1 calls TetB. No rotation can do that leg by leg.

## The metric cannot choose

The metric fixes $(\det e)^2 = \kappa$ and never the sign of $\det e$, just as $a$ fixes $x^2$ and never the sign of $x$. Every quantity built from the metric, including the curvature, Einstein's equations and the action they come from, is identical on both roots. The textbook formulation keeps one root by restricting frames to the *proper orthochronous* Lorentz group. That is a consistent choice, but nothing in the metric makes it: it is a convention.

## Two honest caveats

**The two tetrahedra have the same shape.** A regular tetrahedron is identical to its mirror image, so as a shape TetB is TetA turned by a quarter turn. What the roots change is the order of the legs and the region of space the tetrahedron occupies, at one and the same observer.

**Direction of time matters.** Turning every leg around, time included, leaves the determinant unchanged in four dimensions, $(-1)^4 = 1$, so that frame stays on the same root while its spatial legs carry TetB. The reason is that it also reverses time. The match between root and tetrahedron is therefore stated for frames whose time leg points to the future, which is Letter 1's setting.

## The 3 + 1 pattern

In Letter 1's coordinates, whose axes are the frame's own spatial legs, one face normal of TetA has all signs equal, $(+,+,+)$, and three have mixed signs. Letter 1 reads this as one temporal face and three spatial ones. Parity sends the uniform normal to $(-,-,-)$, so TetB carries the same pattern. The note now says precisely what fixes the pattern: the frame's spatial legs. The tetrahedron's own rotations make all four faces equivalent, so the pattern belongs to the tetrahedron relative to the frame, not to the tetrahedron alone.

## What changed from the original

The original note is [`supplementary_scheme_proof.tex`](../../papers/letter-1-tetrad-frame-geometry/Supplementary/supplementary_scheme_proof.tex) in Letter 1's supplement, and it is unchanged there. This revision keeps its title, its sections, its argument, its Route 1 / Route 2 table and its wording wherever that wording is exact. The changes:

**The tetrad equation is quadratic**
- Proves the orbit claim. The original stated that the solution space is one Lorentz orbit; the revision adds the two lines that show every solution is invertible and every pair of solutions differs by a Lorentz transformation.
- Defines the scheme explicitly, as the affine scheme of the sixteen unknowns, and notes that it is isomorphic to the orthogonal group scheme.

**The scheme has two components** (titled "The Spatial Scheme Has Two Components" in the original)
- Adds the determinant equation $(\det e)^2 = \kappa$, which makes the scheme do the work: its two roots are the two components, and neither splits further over the complex numbers.
- Replaces the step from four Lorentz components to two. The original reduced them by saying time reversal acts trivially on the spatial legs, which is true but does not by itself define a restriction of the Lorentz group to the spatial sector, since boosts mix time and space. The revision counts the components by the determinant, and recovers the original's two spatial components, $SO(3)$ and $P \cdot SO(3)$, exactly, as the frame changes of one observer with the time leg held fixed.
- Adds why parity is the canonical member of its component, why no rotation can replace it, and why this needs an odd number of spatial dimensions.
- Adds the exact link to Route 1: parity maps TetA onto the all-flipped region, the second bounded region of the letter.
- Adds the two caveats above: same shape, and future-pointing frames.
- Tightens "four points with constant pairwise inner product" to "four unit vectors with common pairwise inner product $-1/3$", the hypothesis the regular-tetrahedron result actually needs.

**Both components are necessarily present**
- Adds the reason the metric cannot choose, $(\det e)^2 = \kappa$, and the list of quantities that agree on both components.
- Changes "there is no consistent way to retain one component and discard the other" to the exact statement: retaining one is consistent, but no equation in the metric can make the selection. The stronger wording could be refuted by pointing at general relativity itself, which does retain one.
- Corrects the convention. The original identified root selection with choosing the signature convention $(-,+,+,+)$ or $(+,-,-,-)$. That choice flips $\eta$ as a whole, leaves the Lorentz group unchanged and selects nothing. The convention that keeps one component is the restriction to the proper orthochronous group, and the revision says so, keeping the original's sentence that it is "a valid computational choice" and that "the scheme itself contains both".

**Each component carries a 3 + 1 decomposition**
- States that the sign patterns are read in the frame's own axes, and that the 3 + 1 split is relative to those legs.
- Removes the claim that TetA and TetB recover the $(-,+,+,+)$ and $(+,-,-,-)$ conventions, for the reason above; keeps that parity exchanges the uniform-sign normals.

**Summary**
- The table's key fact for Route 2 becomes "$(\det e)^2 = \kappa$ has two roots".
- "Neither route assumes the other" is made exact: Route 2 uses no half-space construction and Route 1 no quadratic structure, and both take the four tetrahedral directions from Letter 1's signature-to-frame supplement.

**References**
- Adds Borel (connectedness of the complex orthogonal group), Hehl et al. (the proper orthochronous convention) and Coxeter (the regular tetrahedron).

## Why it matters

**The second chamber is not added by hand.** GFD's central structure is a pair of chambers, TetA and TetB. The proof shows the pair is already present in the defining equation of general relativity's frame, as its two roots, before any physics is added.

**It locates the choice.** General relativity keeps one root. The proof shows that this is consistent, that the metric cannot make the choice, and which convention does. That is the starting point of [Einstein as the TetA partition](../../EINSTEIN_TETA_PARTITION.md) and of Letter 3.

**Two independent routes agree.** Route 1 finds the two tetrahedra by bounding half-spaces; Route 2 finds them as the roots of an equation. A reader who doubts one can check the other.

## What it does not do

The proof is about the solutions of the tetrad equation at a point. That the second root carries physical content, that TetB is a real sector of the gravitational field and torsion its carrier, is the framework's claim, developed in Letters 2 and 3.

## Contents

| File | Contents |
|---|---|
| [`tetrad_scheme_two_bounded_regions.pdf`](tetrad_scheme_two_bounded_regions.pdf) | The revised note |
| [`tetrad_scheme_two_bounded_regions.tex`](tetrad_scheme_two_bounded_regions.tex) | LaTeX source (IOP journal class, included) |
| [`verify_tetrad_scheme_two_bounded_regions.py`](verify_tetrad_scheme_two_bounded_regions.py) | Checks of every claim, labelled by section; exact where the claim is algebraic. One standard fact is cited rather than computed: the complex group $SO(4, \mathbb{C})$ is connected |
| [`iopjournal.cls`](iopjournal.cls) | Document class, so the source builds here |

```bash
pip install sympy numpy
python verify_tetrad_scheme_two_bounded_regions.py      # 39/39
pdflatex -interaction=nonstopmode tetrad_scheme_two_bounded_regions.tex
```

## Related

- [Letter 1: The Coordinate-Space Geometry of the Tetrad Frame](../../papers/letter-1-tetrad-frame-geometry/), Route 1, and the original of this note.
- [The forced tetrahedral frame](../forced-tetrahedral-frame/): why the four directions form a regular tetrahedron.
- [The Gram Matrix of the Tetrad Equation](../../papers/gram-matrix-of-tetrad-equation/): root-blindness and the cross-coupling of the two roots.
- [Einstein's equation as the TetA partition](../../EINSTEIN_TETA_PARTITION.md): what follows from keeping one root.

---

*Two roots of $(\det e)^2 = \kappa$, exactly two components of the scheme, parity between them, and a metric that sees only $\kappa$.*
