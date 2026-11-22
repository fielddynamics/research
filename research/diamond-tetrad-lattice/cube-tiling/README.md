# The Cube Tiling: Two Labellings and What Each Builds

*Field Dynamics Research, research folder, 2026-11-22. Status: research, not a proof. Verification: `python3 verify_cube_tiling.py` (11 checks, exact integers).*

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

## What this settles and what it does not

Settled, exactly: the two labellings are different tilings, not two descriptions of one. They agree on the geometry (the same tetrahedral–octahedral honeycomb, since a star is unchanged by swapping its labels) and differ on every labelled structure: the symmetry group, the meaning of the global bit, the dual cube, and the net.

Not settled: which labelling the framework's tiling is. Each rests on a premise the framework states:
- **C** rests on Paper I's closure, "where parts meet they agree", read as one label per shared corner.
- **U** rests on every cube holding the same star, and on the lattice note's bond reciprocity: a TetA leg closes only through a TetB-shaped junction (lattice note, result 2). In U that junction is the dual cube's exchanged star.

The proof of the tiling cannot be written until this choice is made. Everything up to it (the honeycomb, the shared octahedra, result 1) is common to both and can go in either way.

## Next

- Choose the labelling, or state both as the two cases of the proof.
- Then the exact parts move to `proofs/`: the honeycomb and shared octahedra (already in the closure note), results 1–5 for the chosen labelling, and the lattice note's results 1–4 and 6 if U.

## Files

| File | What it does |
|---|---|
| [`verify_cube_tiling.py`](verify_cube_tiling.py) | 11 exact checks, labelled by the results above |

## Related

- [The pixel lattice](../README.md): the diamond nets (result 7) and bond reciprocity (result 2).
- [Pixel tiling and closure](../../stellated%20octahedron%20geometry/pixel_tiling_and_closure.md): the honeycomb, the shared octahedra and the closure labelling.
- [Hadamard cube frame](../../../proofs/hadamard-cube-frame/) and [Gram matrix](../../../proofs/gram-matrix-tetrad-equation/): the one-cube results the tiling builds on.
