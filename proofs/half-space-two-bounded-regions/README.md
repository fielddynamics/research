# The Sixteen Half-Space Regions of the Tetrad Frame

*Route 1 of Letter 1: four planes, sixteen sign choices, exactly two closed solids · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`tetrad` `half-spaces` `stellated-octahedron` `octahedron` `spatial-parity` `boundary-channels` `proof` `Lean`

[![Lean proof](https://github.com/fielddynamics/research/actions/workflows/lean-half-space-two-bounded-regions.yml/badge.svg)](https://github.com/fielddynamics/research/actions/workflows/lean-half-space-two-bounded-regions.yml)

---

This folder holds Letter 1's first route to the stellated octahedron as a standalone proof, a script that checks every claim, and a Lean formalisation that proves every claim. Letter 1 reaches the two tetrahedra by two independent routes. Route 2, the [tetrad scheme](../tetrad-scheme-two-bounded-regions/), finds them as the two roots of the tetrad equation. Route 1, here, finds them by bounding half-spaces: of the sixteen regions that four planes cut out, exactly two close into finite solids. This page explains the argument for a reader with first-year linear algebra.

## Four planes

The [forced tetrahedral frame](../forced-tetrahedral-frame/) shows that the spatial legs of a tetrad, drawn in space, are forced to four directions $\mathbf n_a$ at equal angles: the face normals of a regular tetrahedron. Measuring a point $\mathbf p = (x, y, z)$ along each direction gives four numbers,

$$v_1 = x + y + z,\quad v_2 = x - y - z,\quad v_3 = -x + y - z,\quad v_4 = -x - y + z .$$

Each $v_a$ defines a plane, and each plane offers two sides: $v_a \le 1$ or $-v_a \le 1$. Choosing one side per plane gives $2^4 = 16$ regions.

## Exactly two are bounded

The four numbers always add to zero: $v_1 + v_2 + v_3 + v_4 = 0$, at every point, and this is the only relation among them.

**All four kept, or all four flipped: bounded.** If every $v_a \le 1$, then each $v_a$, being minus the sum of the other three, is at least $-3$, and the coordinates, $x = (v_1 + v_2)/2$ and so on, stay between $-3$ and $1$. The region is a closed solid: TetA. Flipping all four gives the second solid, TetB, which nobody defined. It is the mirror image of TetA through the origin.

**Anything mixed: unbounded.** Keep the directions in a set $S$ and flip the rest, with $S$ neither empty nor everything. Walk along $\mathbf d = -\sum_{b \in S} \mathbf n_b$. Every constraint gets *easier* the further you go, so the walk never leaves the region and the region reaches infinity. This works for all fourteen mixed choices with one formula.

So exactly two of the sixteen are bounded, and they are TetA and TetB.

## What the two solids make

- **They are tetrahedra.** TetA has corners $-\mathbf n_a$, TetB has corners $\mathbf n_a$, the forced frame itself.
- **They pass through each other.** Each corner of one pokes through exactly one face of the other.
- **Their overlap is a regular octahedron**, $|x| + |y| + |z| \le 1$, with six corners $\pm\hat{\mathbf e}_j$ and twelve edges of length $\sqrt2$.
- **Their union is the stellated octahedron**, Kepler's *stella octangula*.
- **Sixteen channels.** On each face of TetA, the poking corner of TetB carves the face into four pieces: a central core inside TetB and three exposed corners. Four faces times four pieces gives sixteen boundary channels.
- **The inventory** depends only on $K = 4$ faces and $D = 3$ dimensions: $2^D = 8$ corners, $K \times D = 12$ edges, $2K = 8$ faces, $K^2 = 16$ channels, $V + E + F = K(K + D) = 28$, and $V - E + F = 4$.

## Machine-checked in Lean

The [`lean/`](lean/) folder proves every mathematical statement in [Lean 4](https://lean-lang.org) with the [Mathlib](https://github.com/leanprover-community/mathlib4) library, and the Lean kernel checks every step.

- **The four directions are not re-entered.** Lean imports them from the [forced tetrahedral frame](../forced-tetrahedral-frame/)'s formalisation, as the columns of its matrix $M$, so the two proofs are checked as one chain.
- **"Bounded" is Mathlib's definition** (`Bornology.IsBounded`), not one written for this proof.
- **The classification is an "if and only if".** A region is bounded exactly when its four signs agree, and the set of bounded regions among the sixteen is exactly $\{\text{TetA}, \text{TetB}\}$.
- **All fourteen mixed cases at once.** The letter argues the one-flip case in words and says the rest follow the same way; Lean proves every case with the explicit escape direction above.
- **The shapes are identified, not just sampled.** TetA and TetB are proved equal to the solid tetrahedra on their corners, the overlap equal to the solid octahedron on $\pm\hat{\mathbf e}_j$, and each channel non-empty and convex, with the four channels of a face disjoint and covering it.

GitHub re-checks the proof automatically whenever it, or the proof it builds on, changes; the badge at the top of this page shows the latest result. It is green only if the proof builds with no warnings, no gaps (`sorry`) and only Lean's three standard axioms. [`LEAN_AUDIT.md`](LEAN_AUDIT.md) is a referee's guide to the formalisation.

## Why it matters

- **The second tetrahedron is not added by hand.** TetB appears as the only other closed region of the same four planes. GFD's pair of chambers is already present in a single tetrad's spatial frame.
- **It is the shape, not only the frame.** The [forced tetrahedral frame](../forced-tetrahedral-frame/) forces the four directions; this proof shows what those directions build: the stellated octahedron, its octahedral core and its sixteen channels.
- **Two independent routes agree.** Route 1 uses no quadratic structure and Route 2 no half-spaces; both arrive at TetA and TetB.

## What it does not do

The proof is about the regions four planes cut out of space. That the four planes come from the tetrad is the content of the forced tetrahedral frame. That the channels and the two chambers carry physical content is the framework's claim, developed in Letters 2 and 3. Whether deeper levels of the Sierpiński subdivision matter is not addressed.

## Relation to Letter 1

The note keeps Letter 1's sections *Four Planes*, *The Emergent Geometry* and *Structural Inventory* word for word, and its figures. The letter itself, in [`papers/letter-1-tetrad-frame-geometry/`](../../papers/letter-1-tetrad-frame-geometry/), is unchanged. Additions are marked `% Lean:` in the source:

- an abstract and title for the standalone note, and a *Formal Verification* section;
- the explicit bound on TetA, $|x|, |y|, |z| \le 3$;
- the explicit escape ray for every mixed selection, which makes the letter's "the same reasoning applies" exact;
- TetA and TetB as the tetrahedra on $-\mathbf n_a$ and $\mathbf n_a$, related by parity;
- the octahedron in coordinates, $|x| + |y| + |z| \le 1$, as the hull of $\pm\hat{\mathbf e}_j$;
- the channels defined as sets, with why they are disjoint and cover each face;
- the reference for the frame updated to the forced tetrahedral frame;
- the $3 + 1$ sign pattern sentence moved from the letter's Discussion to the end of the inventory.

## Contents

| File | Contents |
|---|---|
| [`half_space_two_bounded_regions.pdf`](half_space_two_bounded_regions.pdf) | The proof, three pages |
| [`half_space_two_bounded_regions.tex`](half_space_two_bounded_regions.tex) | LaTeX source (IOP journal class, included) |
| [`fig1_tetrad_frame.png`](fig1_tetrad_frame.png) | Letter 1's Figure 1: the rendering at four million points |
| [`verify_half_space_two_bounded_regions.py`](verify_half_space_two_bounded_regions.py) | Letter 1's validation script, unchanged apart from its header: the sum rule, all sixteen regions by linear programming and by convex hulls, all fourteen mixed cases, the octahedron, the face subdivision, the channels and the inventory |
| [`iopjournal.cls`](iopjournal.cls) | Document class, so the source builds here |
| [`lean/HalfSpaceTwoBoundedRegions.lean`](lean/HalfSpaceTwoBoundedRegions.lean) | The Lean 4 formalisation of every mathematical statement |
| [`lean/lakefile.toml`](lean/lakefile.toml), [`lean/lean-toolchain`](lean/lean-toolchain), [`lean/lake-manifest.json`](lean/lake-manifest.json) | Project files: Lean 4.36.0, Mathlib v4.36.0, and the forced tetrahedral frame's formalisation as a dependency |
| [`LEAN_AUDIT.md`](LEAN_AUDIT.md) | Referee's guide to the formalisation |

```bash
pip install numpy scipy
python verify_half_space_two_bounded_regions.py      # 29/29
pdflatex -interaction=nonstopmode half_space_two_bounded_regions.tex

# Lean (needs elan: https://github.com/leanprover/elan)
cd lean
lake exe cache get    # downloads Mathlib, already compiled
lake build            # checks every theorem, and the forced-frame proof it imports
```

## Related

- [Letter 1: The Coordinate-Space Geometry of the Tetrad Frame](../../papers/letter-1-tetrad-frame-geometry/), where this route first appears.
- [The tetrad scheme and the two bounded regions](../tetrad-scheme-two-bounded-regions/): Route 2, the same two tetrahedra as the two roots of the tetrad equation.
- [The forced tetrahedral frame](../forced-tetrahedral-frame/): why the four directions form a regular tetrahedron.
- [The stellated octahedron, the cube and the Hadamard matrix](../hadamard-cube-frame/): the same eight corners as the two parity classes of the cube.

---

*Four planes, sixteen choices, two solids: proved for every case by the Lean kernel, and seen at four million points.*
