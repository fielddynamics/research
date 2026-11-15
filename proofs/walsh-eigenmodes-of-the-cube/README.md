# The Walsh Eigenmodes of the Cube, and What Field Closure Reads

*Which Walsh standing waves the cube holds under the stellated octahedron's symmetry, how they make its vortices, and why field closure is what reads all of them · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`Walsh-functions` `Hadamard` `eigenmodes` `standing-wave` `tetrahedral-symmetry` `field-closure` `stellated-octahedron` `proof`

---

This folder holds:
- a four-page proof ([PDF](walsh_eigenmodes_of_the_cube.pdf), [LaTeX](walsh_eigenmodes_of_the_cube.tex));
- a script that checks every step ([`verify_walsh_eigenmodes.py`](verify_walsh_eigenmodes.py), 45 checks, [output](verify_output.txt));
- an internal referee review with the response to each point ([`referee_review.md`](referee_review.md)).

It builds on two earlier proofs, [the Hadamard cube frame](../hadamard-cube-frame/) and [the vortices of the stellated octahedron](../vortices-of-the-stellated-octahedron/), and it runs the archive's [oscillator node](../../research/universe-is-pixelated/) directly.

## The question

The eight Walsh functions on the cube's corners are the rows of the Hadamard matrix. They are already known to be the cube's eigenmodes, its standing waves. Two questions follow for GFD:
- Which of them does the cube hold under the stellated octahedron's symmetry?
- Must field closure read them, and if so, how?

## The vocabulary

**The two sectors.** Under the stellated octahedron's symmetry (T_d), the eight functions fall into two sectors:

| Sector | Modes | Kind |
|---|---|---|
| uniform and parity | 1, xyz | scalars |
| the six T₂ modes, grade 1 | x, y, z | vectors |
| the six T₂ modes, grade 2 | yz, xz, xy | quadrupoles |

As angular shapes, the eight are the s, p, d and f characters familiar from chemistry. The symmetry treats the quadrupoles like directions only because it has no inversion.

**The two closures.** The archive uses "closure" for two different things:
- **Frame closure** is Letter 1's v₁+v₂+v₃+v₄ = 0.
- **Field closure** is Letter 3's: both roots of the tetrad, TetA and TetB, active, with nothing held at zero.

The oscillator node's update rule is a third thing, called here its closure rule.

## The answers

**1. The cube holds the Walsh modes exactly when TetA and TetB are alike.** For any coupling on the cube with the stellated octahedron's symmetry:
- **Alike.** If TetA and TetB have equal energies and equal internal couplings, all eight functions are exact eigenmodes. This is the cube's full symmetry.
- **Different.** If they differ, the modes pair up and rotate together: 1 with xyz, and x with yz, y with xz, z with xy. Each angle is given in closed form.

This is the cube's version of the standard s–f and p–d mixing in tetrahedral chemistry.

**In the full pixel** (the cube with the octahedron and the Field Origin):
- **Alike.** The Walsh modes survive.
- **Different.** The same pairing holds, but each mode has its own angle, set by an energy-dependent coupling.

**2. The vortices are made of T₂ modes.** The pixel's winding states lie entirely in the T₂ sector, so the uniform and parity modes never circulate. On the plain cube, two of the Walsh standing waves combine into a vortex: x + iy circulates, while x and y alone don't.

**3. Field closure is what reads all of them.** This holds for every readout that is linear and respects the symmetry.

| Roots used | What it can read |
|---|---|
| one (TetA alone) | half the spectrum: it can't tell a Walsh function from its complement, the collapse in the Hadamard proof |
| both (field closure) | all eight modes |

Under field closure, the work splits cleanly:
- **Scalars:** the two chamber sums read 1 and xyz.
- **Frames:** the two frames read the six T₂ modes.
- **Nothing else:** every other symmetric linear readout is built from these four.

μ = S_A/(S_A + S_B) needs TetB's sum, so it can't be formed from TetA alone.

Frame closure is not an extra assumption. The symmetry forces it, and it is the same equation as the frame ignoring the uniform mode.

**4. The oscillator node's closure rule.** In `octahedral_node.py`:
- **μ is the TetA share,** which depends only on 1 and xyz.
- **The amplitude and outward-coupling updates see only total Walsh power,** by Parseval. Each has one target for every corner.
- **The inward-coupling update is corner-local.** It is inert only because it starts at its fixed point of 1.

**5. μ fixes the bonding A₁ mode.** If the corner values are field values (the linear reading), μ = x/(1+x) means the mode is proportional to (g, a₀). Its two chamber parts are then g_N and g − g_N, which is exactly the field equation g_N = g²/(g + a₀). This matches Letter 3, which divides the field g itself between TetA and TetB.

If instead the field is a wave's intensity (the quadratic reading), the mode is proportional to (√g, √a₀). That is the diamond lattice's bond-orbital dictionary.

The two readings agree only at x = 1. Which one applies is a question of what the mode's amplitude represents, not of μ. For the cube, the linear reading is the consistent one.

## What it does not claim

- That the physical field is this node, or reads linearly.
- That any lattice model's bonding mode satisfies tan θ = a₀/g. Result 5 makes that the test: compute the mode, then compare its angle with a₀/g.

## Contents

| File | Contents |
|---|---|
| [`walsh_eigenmodes_of_the_cube.pdf`](walsh_eigenmodes_of_the_cube.pdf) | The proof, 4 pages |
| [`walsh_eigenmodes_of_the_cube.tex`](walsh_eigenmodes_of_the_cube.tex) | LaTeX source |
| [`verify_walsh_eigenmodes.py`](verify_walsh_eigenmodes.py) | 45 checks, in six parts: (A) the cube's eigenmodes; (B) the pairing, on the cube in all parameters and in the pixel; (C) the vortices and x + iy; (D) frame closure and field closure, solved from the symmetry equations; (E) the node, symbolically and on its own code; (F) the two readings of μ |
| [`verify_output.txt`](verify_output.txt) | Output of the script |
| [`referee_review.md`](referee_review.md) | Internal referee review and the response to each point |

## Reproduce

```
python verify_walsh_eigenmodes.py      # 45/45 (needs sympy and numpy; imports research/universe-is-pixelated/octahedral_node.py)
pdflatex -jobname=walsh_eigenmodes_of_the_cube '\providecommand\ead[1]{\email{#1}}\input{walsh_eigenmodes_of_the_cube.tex}'
```

## Related

- [The Hadamard cube frame](../hadamard-cube-frame/): the Walsh matrix as parity times frame, and the collapse on one tetrahedron.
- [Vortices of the stellated octahedron](../vortices-of-the-stellated-octahedron/): the vortices, here placed in the T₂ sector.
- [Field closure of the tetrad frame](../../FIELD_CLOSURE_OF_THE_TETRAD_FRAME.md): Letter 3, where field closure is defined.
- [The universe is pixelated](../../research/universe-is-pixelated/): the oscillator node.
