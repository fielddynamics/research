# The Walsh Eigenmodes of the Cube, and What Field Closure Reads

*Which Walsh standing waves the cube holds when TetA and TetB are kept distinct, how they make the cube's vortices, and why field closure is what reads all of them · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`Walsh-functions` `Hadamard` `eigenmodes` `standing-wave` `tetrahedral-symmetry` `field-closure` `stellated-octahedron` `proof`

---

This folder holds:
- a proof of four pages plus references ([PDF](walsh_eigenmodes_of_the_cube.pdf), [LaTeX](walsh_eigenmodes_of_the_cube.tex));
- a script that checks every step ([`verify_walsh_eigenmodes.py`](verify_walsh_eigenmodes.py), 47 checks, [output](verify_output.txt));
- an internal referee review with a response to each point ([`referee_review.md`](referee_review.md)).

It builds on:
- [the coupling algebra](../../research/coupling-algebra/), which already treats the cube under its full symmetry: the four distance relations, diagonalised by the Walsh grades, and the null-cone reading of the grades;
- [the Hadamard cube frame](../hadamard-cube-frame/);
- [the vortices of the stellated octahedron](../vortices-of-the-stellated-octahedron/).

The new step here is to keep TetA and TetB distinct. The proof also runs the archive's [oscillator node](../../research/universe-is-pixelated/) directly.

## The vocabulary

**The eight corner modes.** These are the archive's names, from the coupling algebra:

| Mode | Name | Reading |
|---|---|---|
| 1 | the constant mode | time, on the null cone |
| x, y, z | the vector modes | space |
| yz, xz, xy | the bivector modes | the rotation generators |
| xyz | the chamber sign | +1 on TetA, −1 on TetB |

As angular shapes the four grades are s, p, d and f. Under the stellated octahedron's symmetry (T_d), they fall into two sectors:
- 1 and xyz;
- the six T₂ modes: the vector and bivector modes.

**The Field Origin.** It is the central octahedron in which the chambers intersect, with centre O.

**Closure.** Letter 1's closure condition, v₁+v₂+v₃+v₄ = 0, seals TetA, and the same four walls seal TetB. The forced-tetrahedral-frame proof derives it rather than assuming it. Field closure (Letter 3) keeps both roots active, with nothing held at zero.

**The node's closure rule.** The oscillator node's update rule is a separate thing.

## The answers

**1. The cube's corners hold the Walsh modes exactly when TetA and TetB are alike.** For any coupling on the corners with T_d symmetry:
- **Alike.** If TetA and TetB have equal energies and internal couplings, all eight functions are exact eigenmodes. This is the coupling algebra's case.
- **Different.** If they differ, the modes pair up and rotate: 1 with xyz, x with yz, y with xz, z with xy. The angles are in closed form.

This is the cube's version of the standard s–f and p–d mixing of tetrahedral chemistry. In the whole cube, with its Field Origin, the pairing holds mode by mode, each mode with its own angle.

**2. The vortices are made of T₂ modes.** The constant mode and the chamber sign never circulate. On the plain cube, x + iy circulates, while x and y alone don't.

**3. Field closure is what reads all of them.** This holds among linear readouts of the eight corner states that respect the symmetry.

| Roots used | What it reads |
|---|---|
| one (TetA alone) | four modes, 1 and x, y, z: on the null cone, time and the three directions of space, TetA's 3+1 |
| both (field closure) | all eight modes |

The four modes one root confuses with these are the bivector modes and the chamber sign. They are also the four the metric cannot see.

Under field closure the work splits cleanly:
- **Scalars:** the two chamber sums read 1 and xyz, and give μ.
- **Frames:** the two frames read the six T₂ modes.
- **Nothing else:** every other symmetric linear readout is built from these four.

Closure, Σv = 0, is the same equation as the frame ignoring the constant mode.

**4. The oscillator node's closure rule.**
- **μ is the TetA share,** a function of 1 and xyz only.
- **The amplitude and outward-coupling updates see only the total Walsh weight** (Parseval).
- **The inward-coupling update is corner-local.** It is inert only because it starts at its fixed point.

**5. μ fixes the bonding A₁ mode.** Read the corner values as field values. Then μ = x/(1+x) makes the mode proportional to (g_t, a₀), and its TetA part is the TetA partition g_s = μ g_t of Letter 3. The exchange x → 1/x swaps the chambers.

Written out, μ g_t = g_t²/(g_t + a₀), which is also the right-hand side of the spherical field equation. The two are different statements:
- **the partition:** kinematic;
- **the spherical field equation:** dynamic.

They are linked by the AQUAL identity μ = dF/dy, and the proof uses only the partition.

The linear reading matches four things in the archive:
- Letter 3's division of the field;
- the measured share g_bar/g_obs from the hourglass work;
- the coupling algebra's flow share;
- every readout in this proof.

If the field is a wave's intensity instead, the mode is proportional to (√g_t, √a₀). That is the diamond lattice's bond-orbital dictionary.

## What it does not claim

- That the physical field is this node, or reads linearly.
- Anything about the 64 ordered transitions between corners. In GFD those are what field closure reads; this proof treats only the eight corner states.
- That any lattice model's bonding mode satisfies tan θ = a₀/g_t. Result 5 makes that the test.

The models here are linear, while GFD's Field Origin is nonlinear.

## Contents

| File | Contents |
|---|---|
| [`walsh_eigenmodes_of_the_cube.pdf`](walsh_eigenmodes_of_the_cube.pdf) | The proof |
| [`walsh_eigenmodes_of_the_cube.tex`](walsh_eigenmodes_of_the_cube.tex) | LaTeX source |
| [`verify_walsh_eigenmodes.py`](verify_walsh_eigenmodes.py) | 47 checks, in six parts: (A) the cube's eigenmodes; (B) the pairing, on the cube's corners in all parameters and in the whole cube; (C) the vortices and x + iy; (D) closure and field closure, with the metric's view of the grades; (E) the node, symbolically and on its own code; (F) the two readings of μ, with the exchange |
| [`verify_output.txt`](verify_output.txt) | Output of the script |
| [`referee_review.md`](referee_review.md) | Internal referee review and the response to each point |

## Reproduce

```
python verify_walsh_eigenmodes.py      # 47/47 (needs sympy and numpy; imports research/universe-is-pixelated/octahedral_node.py)
pdflatex -jobname=walsh_eigenmodes_of_the_cube '\providecommand\ead[1]{\email{#1}}\input{walsh_eigenmodes_of_the_cube.tex}'
```

## Related

- [The coupling algebra](../../research/coupling-algebra/): the cube's couplings under full symmetry, the Walsh and Clifford names, the null-cone reading (Result 9) and μ as a flow share (Result 7).
- [The Hadamard cube frame](../hadamard-cube-frame/): the Walsh matrix as parity times frame, and the collapse on one tetrahedron.
- [The forced tetrahedral frame](../forced-tetrahedral-frame/): closure derived rather than assumed.
- [Field closure](../../research/field-closure/) and [Letter 3](../../FIELD_CLOSURE_OF_THE_TETRAD_FRAME.md): closure, both roots, and the 64 transitions.
- [Vortices of the stellated octahedron](../vortices-of-the-stellated-octahedron/): the vortices, here placed in the T₂ sector.
- [The universe is pixelated](../../research/universe-is-pixelated/): the oscillator node.
