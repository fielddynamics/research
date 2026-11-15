# The Walsh Eigenmodes of the Pixel, and What Closure Reads

*Which Walsh standing waves the stellated octahedron holds, how they make its vortices, and why closure must read them in two sectors · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`Walsh-functions` `Hadamard` `eigenmodes` `standing-wave` `tetrahedral-symmetry` `closure` `stellated-octahedron` `proof`

---

This folder holds a three-page proof ([PDF](walsh_eigenmodes_of_the_pixel.pdf), [LaTeX](walsh_eigenmodes_of_the_pixel.tex)) and a script that checks every step ([`verify_walsh_eigenmodes.py`](verify_walsh_eigenmodes.py), 34 checks, [output](verify_output.txt)). It builds on two earlier proofs:
- [the Hadamard cube frame](../hadamard-cube-frame/): the Walsh matrix is parity times frame;
- [the vortices of the stellated octahedron](../vortices-of-the-stellated-octahedron/).

It also runs the archive's [oscillator node](../../research/universe-is-pixelated/) directly.

## The question

The eight Walsh functions on the cube's corners are already known to be the cube's eigenmodes, its standing waves. The rows of the Hadamard matrix are these functions:

| Name | Functions |
|---|---|
| uniform mode | 1 |
| direction modes | x, y, z (grade 1) and yz, xz, xy (grade 2) |
| parity mode | xyz |

Two questions follow for GFD:
- Does the pixel, the stellated octahedron with TetA and TetB, actually hold these modes?
- Must closure read them, and if so, which ones?

## The answers

**1. The pixel holds the Walsh modes exactly when TetA and TetB are alike.** Under the pixel's symmetry, the eight modes fall into two sectors:
- **the uniform and parity sector:** 1 and xyz;
- **the direction sector:** the six direction modes.

For any coupling with that symmetry, all eight Walsh functions are exact eigenmodes if and only if TetA and TetB have equal energies and equal internal couplings, which is the cube's full symmetry. When they differ, the modes pair up and rotate:
- 1 with xyz;
- x with yz, y with xz, z with xy.

Each rotation angle is given in closed form by a 2×2 matrix.

**2. The vortices are made of direction modes.** The pixel's winding states lie entirely in the direction sector, so the uniform and parity modes never circulate. On the plain cube, two degenerate Walsh standing waves combine into a vortex: x + iy carries a circulating current, while x and y alone carry none.

**3. Closure must read the two sectors separately.** Schur's lemma restricts what any readout of the pixel can do, provided it is linear and respects the symmetry:
- **Directions.** Any such readout that gives a direction from one tetrahedron is Letter 1's frame readout, the sum Σψᵢvᵢ over the legs. Closure, v₁+v₂+v₃+v₄ = 0, is exactly what makes that readout blind to the uniform mode. It reads exactly the direction modes.
- **Scalars.** Any such readout that gives a scalar reads only 1 and xyz.
- **Nothing else.** No symmetric linear readout does anything beyond these two.

**4. The oscillator node's closure obeys this split.** In `octahedral_node.py`:
- **The node's μ is the TetA share.** μ = (1 + c_xyz/c₁)/2 equals S_A/(S_A + S_B). It depends only on 1 and xyz, so it is blind to every vortex.
- **The amplitude closure sees only total Walsh power.** By Parseval, that is all the energy contains. Every corner gets the same target, so the spread between corners shrinks by exactly 2% per step. At equal amplitudes, each step scales the whole spectrum by one factor.

**5. A precise test for μ = x/(1+x).** For an eigenmode of the uniform/parity block with mixing angle θ, the node's μ equals 1/(1 + tan θ). So μ = x/(1+x) holds exactly when tan θ = 1/x, which is a₀/g.

## What it does not claim

- That the physical field is this node, or closes this way.
- That its readouts are linear.
- That the field's mixing angle satisfies tan θ = a₀/g. Result 5 turns that into a test; it does not prove it.

## Contents

| File | Contents |
|---|---|
| [`walsh_eigenmodes_of_the_pixel.pdf`](walsh_eigenmodes_of_the_pixel.pdf) | The proof, 3 pages |
| [`walsh_eigenmodes_of_the_pixel.tex`](walsh_eigenmodes_of_the_pixel.tex) | LaTeX source |
| [`verify_walsh_eigenmodes.py`](verify_walsh_eigenmodes.py) | 34 checks, in five parts: (A) the cube's eigenmodes; (B) the pairing under the pixel's symmetry, in all parameters; (C) the vortices and the cube vortex x + iy; (D) the readouts, solved from their equivariance equations; (E) the node, symbolically and on its own code |
| [`verify_output.txt`](verify_output.txt) | Output of the script |

## Reproduce

```
python verify_walsh_eigenmodes.py      # 34/34 (needs sympy; imports research/universe-is-pixelated/octahedral_node.py)
pdflatex -jobname=walsh_eigenmodes_of_the_pixel '\providecommand\ead[1]{\email{#1}}\input{walsh_eigenmodes_of_the_pixel.tex}'
```

## Related

- [The Hadamard cube frame](../hadamard-cube-frame/): the Walsh matrix as parity times frame, and the collapse of the eight functions to four on one tetrahedron.
- [Vortices of the stellated octahedron](../vortices-of-the-stellated-octahedron/): the pixel's vortices, which this proof places in the direction sector.
- [The universe is pixelated](../../research/universe-is-pixelated/): the oscillator node and its Walsh readout.
