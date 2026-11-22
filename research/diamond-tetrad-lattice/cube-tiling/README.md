# The Cube Tiling: Two Labellings and What Each Builds

*Field Dynamics Research, research folder, 2026-11-22. Status: research, not a proof. Verification: `python3 verify_cube_tiling.py` (19 checks, exact integers and fractions).*

`tiling` `cube` `stellated-octahedron` `TetA` `TetB` `closure` `diamond` `fluorite` `research`

---

## Question

The proofs so far work on one cube: the forced frame, the Hadamard and Gram matrices, the Walsh eigenmodes and the vortices. The next proof is the tiling: cubes fill space, each holding one whole stellated octahedron, and neighbouring cubes share corners. Before writing it, the algebra has to say which tiling.

Two research notes already treat it, and they label it differently:
- **U (uniform).** Every cube carries the same star: corner $p$ of cube $n$ has the local label $\chi_n(p) = \prod_i (p_i - 2n_i)$. This is [result 7 of the lattice note](../README.md).
- **C (closure).** Each cube may swap its two tetrahedra, $\sigma_n \chi_n(p)$, and every shared corner must get one label from all eight cubes. This is [pixel tiling and closure](../../stellated%20octahedron%20geometry/pixel_tiling_and_closure.md).

Neither note mentions the other. This note puts them side by side. Coordinates: cube centres $2n$, $n \in \mathbb Z^3$; corners $p \in (2\mathbb Z + 1)^3$; TetA is local sign $+1$ (the Gram-matrix convention, $xyz = +1$).

## Results

**1. The local label flips across faces and through corners, not across edges.** For neighbours $n$ and $n + d$, a shared corner's local label changes by $(-1)^{|d|}$ (check 1). This one sign drives everything below.

**2. Closure turns the corner label into a character of the lattice.** Closure forces $\sigma_n = \sigma_0(-1)^{n_1+n_2+n_3}$, and then every corner carries
$$\lambda(p) = -\sigma_0\,(-1)^{(p_1+p_2+p_3+3)/2},$$
the same in all eight cubes (check 2). The corners split into two fcc lattices, one TetA and one TetB, in the rock-salt pattern.

**3. In both labellings the root exchange is a translation.**
- **U** is invariant under every cube translation (3a). Exchanging TetA and TetB everywhere is translation by half a body diagonal, which sends cube centres to corners (7a).
- **C** is invariant only under the translations with $t_1 + t_2 + t_3$ even, the fcc sublattice; an odd translation, one cube, is the exchange (3b). This is why a periodic box closes only with an even number of cubes per side (7b).

So the "one global bit" of the closure note is the choice of origin in C, and the choice of which sublattice (centres or corners) is called a centre in U.

**4. The corner, seen as the centre of the dual cube.** The eight cube centres around a corner are the corners of a dual cube centred there.
- **U:** of the eight legs meeting at a corner, four are TetA and four TetB, and the TetA ones arrive in TetB's shape. The dual cube holds a stellated octahedron with the roots exchanged (4a).
- **C:** all eight legs meeting at a corner carry that corner's one label. The dual cube holds one chamber only (4b).

**5. The nets the TetA legs form.**
- **U:** every node has four legs, cube centres and corners alternate, and the legs form two interpenetrating diamond nets, one through the cubes with $n_1+n_2+n_3$ even and one through the odd ones (5a, 6). This is the lattice note's result 7.
- **C:** cube centres have four legs, TetA corners eight, TetB corners none. The legs form one fluorite (CaF$_2$) net: the TetA corners on an fcc lattice, the cube centres on the simple cubic lattice in its tetrahedral holes (5b).

**6. Where a TetA meets a TetB of another cube** (checks 8a, 8b). A cube's big tetrahedra touch the neighbouring cubes only on the shared boundary.
- **C:** a TetA of one cube and a TetB of a face neighbour meet at one point, the face centre, which is a vertex of both cubes' Field Origins. Across edges and corners they do not meet. So TetA and TetB touch nowhere outside the cubes' Field Origins.
- **U:** across every face a TetA and the neighbour's TetB share a whole edge, a face diagonal from corner to corner; across a corner they share that corner. These contacts lie outside the cubes' own Field Origins. They lie on the edges and vertices of the shared octahedra.

**7. The shared octahedra** (checks 9a, 9b). Each has eight faces, two from each of the four cubes around its edge, and a face belongs to the chamber of the spike it bounds.
- **U:** the faces alternate TetA/TetB, as on a cube's own Field Origin. The shared octahedron and its eight spikes make a complete stellated octahedron, centred on the cube edge and straddling four cubes.
- **C:** the four faces at one end of the edge are TetA and the four at the other end TetB. The shared octahedron is a TetA square pyramid and a TetB square pyramid meeting at a square. It is not a Field Origin.

**8. The root in each cube** (check 10). The orientation of a cube's TetA legs, $M_1$ or $-M_1$, is the root of the tetrad equation in that cube (Gram-matrix proof, Proposition 1).
- **U:** the root is the same in every cube.
- **C:** the root alternates across every face. Each cube's TetA legs are the parity image of its neighbour's.

**9. What the label is read from** (checks 11a–11c). The honeycomb's tetrahedra come in two orientations, each the inversion of the other.
- **U:** TetA is every tetrahedron of one orientation and TetB every one of the other. The label is the honeycomb's own 2-colouring, read from shape alone.
- **C:** each orientation carries both labels. The label is read from the corner's position.

## The two side by side

| | U (uniform) | C (closure) |
|---|---|---|
| stellated octahedra | in every cube, on every cube edge (7), at every corner (4a) | in the cubes only |
| TetA meets TetB | along cube-face diagonals and at corners (6) | only at the Field Origins (6) |
| a shared corner | 4 TetA + 4 TetB legs (4a) | one chamber (2, 4b) |
| the root, cube to cube | constant (8) | alternates (8) |
| the label is | the tetrahedron's orientation (9) | the corner's position (2, 9) |
| the TetA legs form | two diamond nets (5a) | one fluorite net (5b) |
| the root exchange | half a body diagonal (3) | one cube (3) |

## What this settles and what it does not

Settled, exactly: the two labellings are different tilings, not two descriptions of one. They agree on the geometry (the same tetrahedral–octahedral honeycomb, since a star is unchanged by swapping its labels) and differ on every labelled structure.

Not settled: which labelling the framework's tiling is. The framework's stated positions bear on it as follows.
- **For C.** Paper I's closure, "where parts meet they agree", read as one label per shared corner. The position that each cube holds one whole stellated octahedron, never one straddling cubes or centred on a corner: C has stars in the cubes only, while U has them on every cube edge and at every corner as well (results 4, 7). Rule 3, that TetB is reached only through the Field Origin: C keeps every TetA–TetB contact at the cubes' Field Origins (result 6).
- **For U.** The root is the same in every cube, as a frame field keeps its orientation wherever $\det e \neq 0$ (result 8). The lattice note's bond reciprocity: a TetA leg closes only through a TetB-shaped junction (lattice note, result 2), and the diamond nets. The label is a property of the shape, not of position (result 9).

The proof of the tiling cannot be written until this choice is made. Everything common to both (the honeycomb, the shared octahedra as regions, result 1) can go in either way.

## Next

- Choose the labelling, or state both as the two cases of the proof.
- If C: say what the alternating root means. In C the parity image of one cube's frame sits in the next cube, so the two roots alternate in space, one cube to the next.
- If U: say what the stars on the cube edges and at the corners are, since they straddle cubes.
- Then the exact parts move to `proofs/`: the honeycomb and shared octahedra (already in the closure note) and the results above for the chosen labelling.

## Files

| File | What it does |
|---|---|
| [`verify_cube_tiling.py`](verify_cube_tiling.py) | 19 exact checks: parts 1–7 for results 1–5, parts 8–11 for results 6–9 |

## Related

- [The pixel lattice](../README.md): the diamond nets (result 7) and bond reciprocity (result 2).
- [Pixel tiling and closure](../../stellated%20octahedron%20geometry/pixel_tiling_and_closure.md): the honeycomb, the shared octahedra and the closure labelling.
- [Hadamard cube frame](../../../proofs/hadamard-cube-frame/) and [Gram matrix](../../../proofs/gram-matrix-tetrad-equation/): the one-cube results the tiling builds on.
