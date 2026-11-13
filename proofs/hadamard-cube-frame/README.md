# The Stellated Octahedron, the Cube and the Hadamard Matrix

*Why the tetrad frame is a Hadamard matrix, and why only three dimensions fill the cube · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`Hadamard-matrix` `Walsh-functions` `cube` `stellated-octahedron` `tetrad` `proof`

---

This folder holds a two-page proof and a script that checks every step, exhaustively wherever the cases can be listed. The proof connects three objects that grew up in separate fields: the tetrahedral frame of the tetrad (geometry and gravity), the Hadamard matrix (combinatorics and signal processing) and the Walsh functions on a cube (digital transforms). It shows they are one object, and it gives the equation $2(D+1) = 2^D$, used throughout GFD, a precise geometric meaning. This page explains the argument for a reader with first-year linear algebra.

## The objects

**The cube.** In $D$ dimensions the cube has $2^D$ corners, the points whose coordinates are all $+1$ or $-1$. In three dimensions these are the 8 corners $(\pm1, \pm1, \pm1)$.

**A cube simplex.** Pick $D + 1$ corners of the cube that are all the same distance from each other. In three dimensions, four corners with every pair the same distance apart form a regular tetrahedron sitting inside the cube. Write the chosen corners as the columns of a matrix $M$, with $D$ rows and $D + 1$ columns of $\pm1$ entries.

**A Hadamard matrix.** A square matrix of $\pm1$ entries whose rows are mutually perpendicular. The smallest interesting one is $4 \times 4$:

$$H_4 = \begin{pmatrix} +1 & +1 & +1 & +1 \\ +1 & +1 & -1 & -1 \\ +1 & -1 & +1 & -1 \\ +1 & -1 & -1 & +1 \end{pmatrix}.$$

Hadamard matrices drive the Walsh–Hadamard transform used in signal processing and coding.

## Result 1: the frame is a Hadamard matrix

Put a row of ones on top of $M$. The proof shows that the result is a Hadamard matrix **exactly when** the columns of $M$ form a cube simplex. It also shows two more equivalent ways of saying the same thing:

- **The columns** satisfy $M^TM = (D+1)I - J$, the forced Gram matrix of the tetrad frame from the [forced tetrahedral frame](../forced-tetrahedral-frame/) proof.
- **The rows** satisfy two conditions: the corners add up to zero, and the spread of the corners is the same in every direction. These are exactly the conditions Letter 1 imposes on the four directions of the frame: no net direction and no preferred axis.

So "the tetrad's frame is a regular tetrahedron", "its directions are balanced and isotropic" and "its sign pattern is a Hadamard matrix" are three readings of one fact. In three dimensions the bordered matrix is exactly $H_4$ above. Its last three rows are the tetrahedron's corners, read coordinate by coordinate.

## Result 2: where such frames can exist

A classical argument due to Hadamard shows that a Hadamard matrix bigger than $2 \times 2$ must have a size divisible by 4. The proof includes it in three lines. So a regular simplex can sit on the corners of a cube only when $D + 1$ is 2 or a multiple of 4. The first interesting case is $D = 3$.

## Result 3: only three dimensions fill the cube

Spatial parity sends every point to its opposite, $x \to -x$. It maps a cube simplex to a second one, and the two never share a corner. Together they have $2(D+1)$ corners, and the cube has $2^D$. They fill the cube exactly when

$$2(D+1) = 2^D ,$$

which happens only at $D = 3$. In three dimensions the two tetrahedra are forced to be the two *parity classes*: the four corners with $xyz = +1$ and the four with $xyz = -1$. Their compound is the stellated octahedron.

This is what the equation $2(D+1) = 2^D$ counts: the corners of a tetrahedron and its mirror image on the left, the corners of the cube on the right. In three dimensions, and only there, TetA and TetB use up the cube exactly.

## Result 4: the Walsh functions split as parity times frame

On the three-cube there are eight Walsh functions, the products of coordinates: $1, x, y, z, yz, xz, xy, xyz$. Their values on the eight corners form the $8 \times 8$ Walsh matrix. The proof shows that, with the corners ordered TetA then TetB, and the functions ordered even then odd,

$$W = H_2 \otimes \hat H ,$$

exactly. Here $H_2$ is the $2 \times 2$ Hadamard matrix and $\hat H$ is the bordered frame. The $H_2$ factor is spatial parity itself: reflecting every coordinate leaves even functions unchanged and flips the sign of odd ones. The $\hat H$ factor is the frame. On each tetrahedron the eight Walsh functions collapse to four, because there each one equals its complement: on TetA, $xyz = 1$, so $yz = x$, $xz = y$ and $xy = z$.

## Why four legs, again

Every row of $M$ splits the $K = D + 1$ legs into two equal halves. With four legs there are exactly three ways to split them into two pairs, and the three rows of $M$ are those three ways. With eight legs there would be 7 rows but 35 possible splits. Only for four legs, apart from the trivial case of two, does the frame use every possible split.

## Why it matters

- **It gives $2(D+1) = 2^D$ a meaning.** In earlier GFD documents this equation appears as arithmetic. Here it is a theorem about geometry: it is the condition for a tetrahedron and its parity image to fill the cube.
- **It ties the frame to the Hadamard–Walsh world.** The tetrad's frame, the Hadamard matrix and the Walsh functions on the cube are one object, and the split into TetA and TetB is the even–odd split of the Walsh functions.
- **It connects the existing proofs.** The forced Gram matrix of the [forced tetrahedral frame](../forced-tetrahedral-frame/) and the balance-and-isotropy conditions of Letter 1 are the two halves of one Hadamard condition, on the columns and on the rows.
- **It is pure mathematics.** Every result is exact and checked, most of them exhaustively.

## What it does not do

The proof is about points on a cube. That the tetrad's legs are realised as such points is the content of the [forced tetrahedral frame](../forced-tetrahedral-frame/) proof, which rests on the magnitude reading of the metric. This proof also makes no claim about how gravity uses the Walsh transform; it shows only that the frame and the Walsh matrix share their structure exactly.

## Earlier version

[Paper C](../../papers/algebraic-papers-a-b-c/gfd_paper_c_hadamard_tetrad.tex) observes that the stellated octahedron's axes form $H_4$ and that the Walsh characters collapse on one tetrahedron. Those observations are correct. This version:

- proves the identification as an equivalence, with the forced Gram matrix and the isotropy conditions as the column and row readings;
- proves Hadamard's divisibility condition, and proves the uniqueness of $D = 3$, which Paper C states as a proposition without proof;
- states the Sylvester factorisation exactly, with the ordering that makes it an equality and with $H_2$ identified as spatial parity, where Paper C writes $H_8 \cong H_2 \otimes H_4$ loosely;
- reads the bordering row of ones as closure, not as the temporal leg;
- drops the claims that the $S_4$ action permutes the Hadamard rows (it permutes the columns, the legs) and that the Walsh transform is "the transform gravity uses to read its frame".

## Contents

| File | Contents |
|---|---|
| [`hadamard_cube_frame.pdf`](hadamard_cube_frame.pdf) | The proof, two pages |
| [`hadamard_cube_frame.tex`](hadamard_cube_frame.tex) | LaTeX source (IOP journal class, included) |
| [`verify_hadamard_cube_frame.py`](verify_hadamard_cube_frame.py) | Checks of every theorem, lemma and corollary: Theorem 1 over all sign matrices for $D \le 3$ and sampled at $D = 7$, Hadamard's condition exhaustively at orders 3 and 5, both cube simplices of the three-cube, the exact Walsh factorisation, and the split count |
| [`iopjournal.cls`](iopjournal.cls) | Document class, so the source builds here |

```bash
pip install sympy numpy
python verify_hadamard_cube_frame.py      # 25/25
pdflatex -interaction=nonstopmode hadamard_cube_frame.tex
```

## Related

- [The forced tetrahedral frame](../forced-tetrahedral-frame/): why the tetrad's legs, drawn in space, form a regular tetrahedron.
- [Letter 1 supplement: from the Lorentz signature to the tetrahedral frame](../../papers/letter-1-tetrad-frame-geometry/Supplementary/supplementary_signature_to_frame.tex): the balance and isotropy conditions.
- [The torsion sector as the regular representation of S₄](../torsion-regular-representation/): the permutation structure of the four legs.
- [G's graded operator is a null rotation](../g-null-rotation/), Theorems 7–8: this frame is the Walsh–Hadamard read on G's 4-block, it factors through a null rotation, and with its two bits read as spinor indices its legs are a Newman–Penrose null tetrad.

---

*The algebra is complete and machine-checked, exhaustively where the cases are finite. The physical reading of the frame is GFD's, stated so that it can be tested.*
