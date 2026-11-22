# The Cube Tiling: Two Labellings, and the Ladder of Tiles

*Field Dynamics Research, research folder, 2026-11-22. Status: research, not a proof. Verification: `python3 verify_cube_tiling.py` (19 checks) `python3 verify_scale_ladder.py` (11) and `python3 verify_sixteen_channels.py` (17), exact integers and fractions.*

`tiling` `cube` `stellated-octahedron` `TetA` `TetB` `closure` `scale-ladder` `Field-Origin` `affine-connection` `torsion` `diamond` `fluorite` `research`

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
- **C:** written from each cube's own centre, the TetA legs of neighbouring cubes are mirror images. Nothing in the cube differs: every cube holds the same star, and its TetA is whichever of its corners are TetA on the one global board of corners (result 2). A shared corner is TetA for both cubes; they reach it from opposite sides, (+,+,+) from one centre and (−,+,+) from the other.

**9. What the label is read from** (checks 11a–11c). The honeycomb's tetrahedra come in two orientations, each the inversion of the other.
- **U:** TetA is every tetrahedron of one orientation and TetB every one of the other. The label is the honeycomb's own 2-colouring, read from shape alone.
- **C:** each orientation carries both labels. The label is read from the corner's position.

## The two side by side

| | U (uniform) | C (closure) |
|---|---|---|
| stellated octahedra | in every cube, on every cube edge (7), at every corner (4a) | in the cubes only |
| TetA meets TetB | along cube-face diagonals and at corners (6) | only at the Field Origins (6) |
| a shared corner | 4 TetA + 4 TetB legs (4a) | one chamber (2, 4b) |
| TetA legs from each centre | the same directions (8) | mirror images in neighbours, one board of corners (8) |
| the label is | the tetrahedron's orientation (9) | the corner's position (2, 9) |
| the TetA legs form | two diamond nets (5a) | one fluorite net (5b) |
| the root exchange | half a body diagonal (3) | one cube (3) |

**10. Dilation** (`verify_scale_ladder.py`, 10a–10b). Scaling the tiling by an integer $k$ about a cube centre sends corners to corners exactly when $k$ is odd; even $k$ sends them onto cube centres. The closure labels obey
$$\lambda(kp) = (-1)^{(k-1)/2}\,\lambda(p):$$
$k \equiv 1 \pmod 4$ keeps every label, $k \equiv 3 \pmod 4$ exchanges TetA and TetB.

**11. Blocks of tiles are tiles at odd sizes only** (11a–11d). An $n \times n \times n$ block's eight corners form a labelled star, four TetA corners making a tetrahedron, exactly when $n$ is odd. For even $n$ all eight carry one chamber. This is the 64-grid note's observation for its $2 \times 2 \times 2$ block (its section 4: the fine labels cannot split the large star), and the reason that note needs a separate coarse label.
- The $3 \times 3 \times 3$ blocks obey the closure rule again, as tiles (11b): the closure tiling reproduces itself one level up, with nothing added.
- The block centred on a tile has its TetA in the directions of the centre tile's TetB (11c), and so on up a ladder of tiles of side $2 \times 3^L$, every level a labelled star (11d).

**12. A star inside the Field Origin** (12a–12e). Take the $3 \times 3 \times 3$ block centred on a tile. Its Field Origin, the core octahedron $|x|+|y|+|z| \le 3$, holds the centre tile, and nothing else whole (12b). The centre tile's eight corners are exactly the centroids of the Field Origin's eight faces (12a).
- **C:** the centre tile's TetA corners sit on the faces of the composite's TetA, and its TetB corners on the composite's TetB (12d). Across the two levels, TetA meets TetA and TetB meets TetB. The mirror orientation of 11c is what makes this so.
- **U:** the composite has the tile's orientation, so the centre tile's TetA corners sit on the composite's TetB faces: the chambers cross between the levels (12e).

So the framework's statement that the stellated octahedron scales, with another stellated octahedron inside its Field Origin, is exact in the tiling: inscribed corner to face centroid, one level down at a factor of 3, with each chamber continuing into the same chamber.

**13. The 16 channels of a face, in the tiling** (`verify_sixteen_channels.py`, 13a–13d). Each face of TetA is cut by the TetB corner that pierces it into a core triangle, a face of the Field Origin, and three corner triangles, faces of TetA's spikes: Letter 1's channels. In the tiling every channel is shared by exactly four tiles.
- A corner channel is a face of one shared octahedron, so it is shared by the four tiles around that cube edge: the tile, two face neighbours and one edge neighbour.
- The core channel bounds the tile's Field Origin, and its three vertices, cube face centres, are vertices of three face neighbours' Field Origins.

So each face carries 4 channels × 4 tiles = **16 couplings, and the tetrahedron 4 × 16 = 64**, the number of components of the affine connection. Every channel of the face opposite $a$ leads to the TetB corner $-a$ that pierces it: the core channel is the base of TetB's spike at $-a$, and each corner channel's shared octahedron runs from its TetA corner to $-a$. A face reaches 7 of the 8 tiles around that TetB corner.

**14. The 64 couplings are the affine connection, as a representation** (14a–14e). The symmetries keeping TetA ($T_d$, acting on its corners as $S_4$) permute the 64 couplings in orbits of sizes 4, 12, 12, 12 and 24, exactly as they permute the connection's index triples $(\lambda, \mu, \nu)$. The characters on the classes $(e, (12), (123), (1234), (12)(34))$ are:

| | character | as in |
|---|---|---|
| all 64 couplings | $(64, 8, 1, 0, 0)$ | the connection $V \otimes V \otimes V$ |
| the 40 in the four smaller orbits | $(40, 8, 1, 0, 0)$ | the Christoffel sector $V \otimes \mathrm{Sym}^2 V$ |
| the 24 in the free orbit | $(24, 0, 0, 0, 0)$ | the torsion sector $V \otimes \Lambda^2 V$, the regular representation (torsion proof, Theorem 1) |

The sign representation, the one scalar detector of orientation, occurs once in the 24 and never in the 40, as it does in torsion and the Christoffel sector (torsion proof, Theorem 2). The free 24 are exactly the corner channels' couplings to face neighbours.

**15. The connection is the 16 channels × 4, algebraically** (15a–15h). The dictionary is not chosen: it is a formula in the forced frame's legs $v_1, \dots, v_4$ (the columns of $M$, with $\sum_a v_a = 0$ and $v_a \cdot v_b = 4\delta_{ab} - 1$), and each index of $\Gamma^\lambda{}_{\mu\nu}$ has one role.
- **$\lambda$ is the face**, the face of TetA opposite $v_\lambda$, and with it the TetB corner $-v_\lambda$ that pierces it.
- **$\mu$ is the channel**, in the half-space proof's own labels: $\mu = \lambda$ is the core, the face of the Field Origin; $\mu \neq \lambda$ is the corner channel at $v_\mu$.
- **$\nu$ is the leg.** The four tiles sharing channel $\mu$ are centred at
$$c_{\lambda\mu\nu} = -v_\lambda + \varepsilon_{\lambda\mu\nu}\, v_\nu, \qquad \varepsilon_{\lambda\mu\nu} = \begin{cases} +1 & \nu \in \{\lambda, \mu\} \\ -1 & \text{otherwise,}\end{cases}$$
one tile along each leg from the piercing TetB corner.

The proof uses only the frame. The core channel's vertices are cube face centres $(v_q + v_r)/2$, which closure rewrites as $-(v_\lambda + v_p)/2$, and a face centre $f$ is shared by the tiles at $0$ and $2f$ (15b). A corner channel $\mu \neq \lambda$ lies on the shared octahedron at the cube-edge midpoint $(v_\mu - v_\lambda)/2$, because $v_\mu \cdot v_\lambda = -1$ makes $(v_\mu + v_\lambda)/2$ a unit vector, and the four tiles holding that edge are exactly $c_{\lambda\mu\nu}$ (15c). So $(\lambda, \mu, \nu) \mapsto$ (channel $\mu$ of face $\lambda$, tile $c_{\lambda\mu\nu}$) is a bijection from the 64 index triples onto the 64 couplings, and it commutes with $T_d$ because it is built from the legs alone (15d). Each channel couples along all four legs of the tetrad, so a face is a $4 \times 4$, channels by legs, and the connection is these 16 per face times the 4 faces.

In this dictionary (15e–15h):
- **The Field Origin is the row $\mu = \lambda$** of each slice: the core channel, coupling the tile to itself and to the three face neighbours whose Field Origins it touches.
- **The diagonal $\mu = \nu$** is each channel's coupling straight through, along its own leg: the core to its own tile, and a corner channel through its shared octahedron to the tile diagonally across.
- **One face's 16** fall, under the face's own symmetry, into the orbits of one slice's ordered index pairs, and the corner channels' couplings to face neighbours are chiral: the face's rotations separate each channel's left and right neighbour, and its reflections exchange them.
- **Exchanging the lower indices** $\mu \leftrightarrow \nu$ swaps a channel with a leg. Its even part is 40-dimensional (Christoffel) and its odd part 24 (torsion), and on the corner channels' couplings to face neighbours it exchanges the two senses of circulation around the face, as the [chiral-holonomy proof](../../../proofs/chiral-holonomy-closed-frame/)'s TetB step is the transpose of its TetA step.

The slice structure is the Gram paper's index grid: 6 upper + 4 diagonal (shared) + 6 lower per slice, $24 + 16 + 24 = 64$ ([Gram-matrix proof](../../../proofs/gram-matrix-tetrad-equation/), Part III; the GRAM manuscript; Letter 3). What the tiling adds is the geometric source of each index, and which coupling is which entry.

*Correction.* An earlier version of this note used a table chosen so that $\mu \leftrightarrow \nu$ paired couplings reaching the same tile, and under it the core channel was the diagonal. The formula above replaces that table: under it the core channel is the row $\mu = \lambda$, and the diagonal is the straight-through coupling.

The sharing in 13–15 is geometric, so these results hold for either labelling.

**What 13–15 do and do not say.**
- They say the tile's 16 channels per face, read in the tiling, are a copy of one slice of the connection, and the four faces the whole connection, with its Christoffel and torsion sectors, as representations of the tetrahedral group, and with an explicit equivariant dictionary.
- The 40 + 24 split as representations is canonical, and the dictionary is the formula of result 15, built from the legs: no choice is made.
- This is the level at which the connection itself is built. $\Gamma^\lambda{}_{\mu\nu}$ has 64 components because each of its three indices runs over 4: one slice per value of $\lambda$, times the $4 \times 4$ of $(\mu, \nu)$. Its 40 + 24 split is the symmetric and antisymmetric parts in $(\mu, \nu)$, an index symmetry. Results 13–15 reproduce exactly that: the count, the slices and the split under the same symmetry. In general relativity each factor of 4 is the number of coordinates; in the tiling each has a geometric source: the face ($\lambda$, with the TetB corner piercing it), the four channels of the face, and the four tiles sharing each channel. The four slices are the four coupled faces, each carrying one $4 \times 4$ copy.
- What the index structure does not supply, in either case, is the dynamics: the transformation law and parallel transport. On the tiles that is a field whose coupling coefficients are $\Gamma$, the continuum step, where torsion would be read as the net circulation through the corner channels.
- The 24 here are TetA's couplings, which run toward the TetB corner piercing each face (13c). How that bears on Letter 2's reading of the 24 torsion components as TetB is a question, not a result.
- The per-face 16 is $K^2$. Whether it is the $K^2$ of $a_0 = K^2 G m_e / r_e^2$ is not shown.

## What this settles and what it does not

Settled, exactly: the two labellings are different tilings, not two descriptions of one. They agree on the geometry (the same tetrahedral–octahedral honeycomb, since a star is unchanged by swapping its labels) and differ on every labelled structure.

Which labelling is the framework's is a choice the framework makes, not one the algebra makes. Its stated positions bear on it as follows.
- **For C.** Paper I's closure, "where parts meet they agree", read as one label per shared corner. The position that each cube holds one whole stellated octahedron, never one straddling cubes or centred on a corner: C has stars in the cubes only, while U has them on every cube edge and at every corner as well (results 4, 7). Rule 3, that TetB is reached only through the Field Origin: C keeps every TetA–TetB contact at the cubes' Field Origins (result 6).
- **For C, from the scale ladder.** The closure tiling reproduces itself at $3 \times 3 \times 3$ (result 11), and the star nested in a Field Origin continues TetA into TetA and TetB into TetB only in C (result 12).
- **For U.** The TetA legs point the same way from every centre (result 8). The lattice note's bond reciprocity: a TetA leg closes only through a TetB-shaped junction (lattice note, result 2), and the diamond nets. The label is a property of the shape, not of position (result 9).

The framework's positions now point one way, to C. Everything common to both (the honeycomb, the shared octahedra as regions, result 1) can go into the proof either way.

## What the scale ladder does not say

- **Not a physical size ladder.** Results 10–12 are about the tiling's labels. Physical closure surfaces sit at each object's Jacobi radius (`proofs/closure-surface/`), which the factor 3 does not set. Compositional scale invariance (llms.txt, Rule 15) is the same rule at every level, not geometric self-similarity of objects.
- **Not a reason for 3 from $D$.** The factor 3 is the smallest odd $k > 1$; result 10 holds in any dimension. It is not derived from $D = 3$ and should not be read as $D$.
- **The 16.** See results 13–15: each face's 16 channels are one slice of the connection; whether that is the $K^2$ of $a_0$ is not shown.

## Next

- Build the tiling proof on C: the honeycomb and shared octahedra (closure note), the global board of corners (results 1–2), the contacts (6), and the ladder and the nested star (10–12).
- A field on the tiling with the couplings of results 13–15 as its coefficients: the step from this representation to the connection itself, and the continuum limit.

## Files

| File | What it does |
|---|---|
| [`verify_cube_tiling.py`](verify_cube_tiling.py) | 19 exact checks: parts 1–7 for results 1–5, parts 8–11 for results 6–9 |
| [`verify_scale_ladder.py`](verify_scale_ladder.py) | 11 exact checks for results 10–12 |
| [`verify_sixteen_channels.py`](verify_sixteen_channels.py) | 17 exact checks for results 13–15 |

## Related

- [The pixel lattice](../README.md): the diamond nets (result 7) and bond reciprocity (result 2).
- [The 64-tetrahedron grid](../../stellated%20octahedron%20geometry/README.md): the $2 \times 2 \times 2$ block and its coarse label (section 4).
- [Pixel tiling and closure](../../stellated%20octahedron%20geometry/pixel_tiling_and_closure.md): the honeycomb, the shared octahedra and the closure labelling.
- [Hadamard cube frame](../../../proofs/hadamard-cube-frame/) and [Gram matrix](../../../proofs/gram-matrix-tetrad-equation/): the one-cube results the tiling builds on.
