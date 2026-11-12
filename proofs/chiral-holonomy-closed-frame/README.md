# Chiral Holonomy of the Closed Tetrad Frame

*Why carrying a frame round the stellated octahedron's directions returns it unchanged only if TetB is ignored, and why the two directions of travel differ · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`holonomy` `parallel-transport` `chirality` `spinor` `double-cover` `Berry-phase` `cube` `stellated-octahedron` `tetrad` `proof`

---

This folder holds a short proof and a script that checks every step, exactly and over every case. It is the revised version of the chiral-holonomy computation in Letter 3's supplement, whose cited script is not in the repository. The original's numbers are reproduced, three exact results are added, and one erratum is corrected. This page explains the argument for a reader with first-year linear algebra.

## The setting

The closed tetrad frame has eight null directions, the corners of a cube: four belong to TetA and four to TetB. Every edge of the cube joins a TetA corner to a TetB corner. A route that visits all eight corners once and returns, along edges, is a *Hamiltonian cycle*. The cube has six of them, each of which can be travelled in two directions.

To carry a frame along an edge from one corner to the next, use the rotation R that turns the first corner's direction onto the second's. Do this around a whole cycle and see how the frame comes back. That final turn is the *holonomy*.

There are two ways to carry the frame:
- **Uniform:** use R at every step.
- **Chiral:** use R on steps leaving a TetA corner and its transpose Rᵀ on steps leaving a TetB corner.

The transpose of a rotation keeps its diagonal and swaps its upper and lower triangles. That is the same exchange GFD's [Gram index grid](../../papers/gram-matrix-of-tetrad-equation/) uses to tell TetA from TetB. There each 4 × 4 slice of the connection is 6 upper (TetA) + 4 diagonal (shared) + 6 lower (TetB), 64 = 24 + 16 + 24 in total. Uniform transport reads every step as TetA. That matches the torsion-free connection, which Letter 2 shows cannot tell the two apart. These readings motivate the two transports; the proofs themselves don't depend on them.

## Result 1: TetA alone returns vectors but not spinors

Uniform transport is ordinary parallel transport on a sphere. On a sphere, carrying a frame round a closed loop turns it by the area the loop encloses. Every Hamiltonian cycle of the cube makes four left turns and four right turns of 60°, so it encloses exactly half the sphere, an area of 2π.

So the frame comes back turned by a full 360°:
- **Vectors return unchanged.** The holonomy is the identity.
- **Spinors return with a minus sign.** They need two full turns, 720°, to come back. This is the same −1 a spin-½ particle picks up when carried round half the sphere (Berry's phase).

The double cover that Paper VII assigns to the two tetrahedra appears here directly. One circuit of the frame directions, read root-blind, is exactly a full turn.

## Result 2: keeping TetB, the frame never closes

With TetB's steps transposed, no cycle returns the frame to where it started. The turn is exactly one of two angles:

$$\cos\Theta = -\frac{4639}{6561} \quad\text{or}\quad -\frac{5983}{6561}, \qquad 6561 = 3^8,$$

that is 134.996° or 155.770°. The 3⁸ comes from eight steps, each with cos θ = 1/3. **The two angles are the two directions of travel.** Each cycle gives one value going one way and the other going back. Going round clockwise and going round anticlockwise are genuinely different: the closure has a handedness, a chirality. The spinor versions are exactly 31/81 and −17/81.

## Result 3: swapping TetA and TetB is the same as reversing direction

Relabel the chambers, calling TetA's corners TetB and vice versa. The holonomy of each cycle becomes exactly the transpose of the holonomy of the reversed cycle. So swapping the two chambers and reversing the direction of travel are the same operation. The reason is simple: the two directions use the same eight steps in opposite orders. For uniform transport the two orders give the same rotation. For chiral transport they don't, and that difference is the chirality.

## Result 4: weighting by the constitutive law

GFD divides the field between the chambers in the shares μ and 1 − μ, with μ(x) = x/(x + 1). Weight each step the same way: μR + (1 − μ)Rᵀ from a TetA corner, and the mirror from a TetB corner. Then:
- **Each step is an exact rotation plus a shrink.** The rotation is by φ with tan φ = σ tan θ, where σ = (x − 1)/(x + 1) is the difference between the two shares.
- **Exchange symmetry acts as reversal.** x → 1/x turns σ into −σ, and that is the same as reversing the direction of travel.
- **On the transition ring x = 1 the chirality vanishes.** There σ = 0, every step is symmetric, and the two directions agree. The chirality has opposite signs inside and outside the ring.
- **Fully TetA or fully TetB** (σ = ±1) recovers Result 2.

## Why it matters

- **It makes the vortex's handedness exact.** The supplement's claim that the closed frame's closure is chiral now rests on exact angles and a theorem: relabelling the chambers is the same as reversing the direction. No numerical fit is involved.
- **The double cover falls out.** The root-blind reading gives the spinor sign −1 for one circuit, with no assumption added.
- **It connects to the constitutive law.** Weighted by μ, each step's rotation is governed by σ(x) = (x − 1)/(x + 1), and exchange symmetry x → 1/x acts on the holonomy as reversal of direction.

## What it does not do

- **It is about transport through eight discrete directions, not a continuous connection on spacetime.** It does not compute a field, solve equations of motion or show that galaxies form disks.
- **The readings are the framework's, grounded in other results.** That the transpose is the TetB step comes from the Gram index grid and Letter 2, and that uniform transport is the root-blind reading likewise. The theorems are pure linear algebra and hold whatever the reading.
- **The share-weighting is a construction.** It applies the constitutive law to the transport; it is not derived from an action. The weighted products also shrink as well as rotate, so only their rotational parts are compared.
- **It treats rotations of frames only.** In Riemann–Cartan geometry torsion also produces a translational effect around a loop, the failure of a small loop to close. That is not addressed here.

## Earlier version

The original is [`supplementary_chiral_holonomy.tex`](../../papers/letter-3-field-closure-of-tetrad-frame/Supplementary/supplementary_chiral_holonomy.tex) in Letter 3's supplement, with a markdown version in [`supplementary_vortex_closure.md`](../../papers/letter-3-field-closure-of-tetrad-frame/Supplementary/supplementary_vortex_closure.md). Its computation is correct and reproduces. This version:
- **gives the angles exactly**, as arccos(−4639/6561) and arccos(−5983/6561). The original's "135° (= 3π/4)" is close but not exact: cos(3π/4) = −0.70711 against −0.70706;
- **identifies the original's "two orientation classes"** as the two directions of travel round each cycle;
- **explains why uniform transport closes** (Gauss–Bonnet, enclosed area 2π) and adds that it gives −1 on spinors;
- **states the chiral step as a transpose** and ties it to the Gram index grid, where the original assigned "+θ from TetA, −θ from TetB" without that link;
- **proves that relabelling equals reversal**, and adds the share-weighted steps;
- **ships the verification script** the original cites.

The vortex and disk discussion of the original is not carried over. It is interpretation rather than a consequence of the holonomy theorems.

## Contents

| File | Contents |
|---|---|
| [`chiral_holonomy_closed_frame.pdf`](chiral_holonomy_closed_frame.pdf) | The proof, three pages |
| [`chiral_holonomy_closed_frame.tex`](chiral_holonomy_closed_frame.tex) | LaTeX source (IOP journal class, included) |
| [`verify_chiral_holonomy_closed_frame.py`](verify_chiral_holonomy_closed_frame.py) | Checks of every step. Exact (sympy) for the edge rotations, both transports on all 12 directed cycles, the spinor lift, the exact angles and the relabelling theorem. Symbolic for the weighted step. Numerical for the turning count and for the weighted holonomies. |
| [`iopjournal.cls`](iopjournal.cls) | Document class, so the source builds here |

```bash
pip install sympy numpy
python verify_chiral_holonomy_closed_frame.py      # 32/32
pdflatex -interaction=nonstopmode chiral_holonomy_closed_frame.tex
```

## Related

- [The tetrad scheme and the two bounded regions](../tetrad-scheme-two-bounded-regions/): the two roots, TetA and TetB.
- [The stellated octahedron, the cube and the Hadamard matrix](../hadamard-cube-frame/): the cube corners as the two parity classes.
- [The torsion sector as the regular representation of S₄](../torsion-regular-representation/): the structure of the 24.
- [The constitutive law from exchange symmetry](../constitutive-law-exchange-symmetry/): μ(x) = x/(x + 1) and the exchange x → 1/x.
- [The Gram matrix of the tetrad equation](../../papers/gram-matrix-of-tetrad-equation/): the 24 + 16 + 24 index grid.
- [`research/bimond-gfd/`](../../research/bimond-gfd/), scripts 10–12: the research that led here.

---

*The algebra is exact and machine-checked over every Hamiltonian cycle. The physical reading of the two transports is GFD's, stated so that it can be tested.*
