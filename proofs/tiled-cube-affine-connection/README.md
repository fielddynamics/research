# The Affine Connection of the Tiled Cube

The affine connection Γ^λ_μν is what tells a field how to change from one place to the next. General relativity gives it 64 components, keeps 40 of them, and sets the other 24, the torsion, to zero by convention. It never says why each index runs over four values, or what the discarded 24 are. **This proof shows that tiling space with GFD's cube builds the connection by itself, each index a piece of geometry, and that the 24 are the handedness of how cubes couple: a swirl around each face and a flow toward TetB, one vortex through each Field Origin.**

This folder holds a four-page proof, a script that checks every statement (44 exact checks, numbered by theorem), and its output. A Lean formalisation is to follow.

## Why this matters

Earlier proofs established what the 24 torsion components *do*: they are the only place a connection can tell TetA from TetB ([Letter 2](../../papers/letter-2-other-half-of-gravity-torsion/), [Gram matrix](../gram-matrix-tetrad-equation/)), and they form the regular representation, the one home of the parity detector ([torsion proof](../torsion-regular-representation/)). What was missing is a picture of what they *are*, in space, and of why the connection has the shape 4 × 4 × 4 at all.

GFD's cube supplies the picture. Each cube holds one whole stellated octahedron (TetA and TetB meeting in the Field Origin), and cubes tile space. Nothing else is added. Counting how a cube's faces are shared with its neighbours gives exactly the connection, and the part general relativity discards is the part of that sharing with a handedness. General relativity is then the tiling with the handedness removed.

## The picture

Look at one face of the cube's TetA.

- **Four channels.** The TetB corner behind the face pierces it and cuts it into a small central triangle, the *core*, which is a face of the Field Origin, and three corner triangles: Letter 1's channels.
- **Four cubes per channel.** In the tiling, each corner channel faces one of the octahedra that fill the space between stars, and each of those is held jointly by the four cubes around a cube edge. The core faces the three neighbouring cubes whose Field Origins touch its corners. So every channel is shared by exactly four cubes.
- **16 per face, 64 in all.** Four channels times four cubes is 16 couplings per face, and four faces give 64: the number of components of the connection.
- **Three indices.** Each coupling is a *face* (λ), a *channel* of that face (μ), and a neighbouring cube that lies along one *leg* of the tetrad (ν). Each runs over four values. That is Γ^λ_μν.

## What is proved

1. **The honeycomb (Theorem 1).** The star fills half its cube; the other half is twelve edge wedges, and the four wedges around each cube edge close into one octahedron held by the four cubes. Space is half stars, half shared octahedra.
2. **Every channel is shared by four cubes (Theorem 2).** The core by the cube and three face neighbours; each corner channel by the four cubes around one cube edge. Every channel of a face leads to the one TetB corner that pierces it.
3. **The dictionary (Theorem 3).** With v₁…v₄ the tetrad's legs (Σv = 0, v_a·v_b = 4δ − 1), the four cubes sharing channel μ of face λ sit at

   c = −v_λ + ε v_ν, with ε = +1 when ν is λ or μ, and −1 otherwise,

   one cube along each leg, measured from the TetB corner that pierces the face. This is a one-to-one match between the 64 couplings and the 64 index triples, and it respects every symmetry of the cube. **It is forced, not chosen:** the symmetry alone allows 1,152 such matches, but fixing the roles (face, channel, leg) leaves exactly one, and of 32 possible sign rules only this one works. TetB follows the same formula with its own legs.
4. **The sectors (Theorem 4).** The couplings carry the connection's full symmetry content. Exchanging μ and ν splits them into a mirror-symmetric 40, exactly the Christoffel sector, and a handed 24, exactly the torsion sector, with the parity detector only in the 24. The Field Origin is the row μ = λ of each slice. This is the Gram proof's 6 + 4 + 6 index grid per slice, now with each entry identified.
5. **Torsion is the couplings' handedness (Theorem 5).** On the couplings from corner channels to neighbouring cubes, exchanging μ and ν is exactly a mirror reflection, so torsion-free means mirror-symmetric. Torsion has two kinds of part:
   - **a swirl:** the totally antisymmetric torsion is +1 for one direction of circulation around each face and −1 for the other, and it behaves like a circulation (unchanged by rotations, reversed by reflections);
   - **a flow:** the vector torsion along each leg is a net shift toward that leg's TetB corner.

   They never overlap.
6. **One vortex through the Field Origin (Theorem 6).** Each face's swirl is a vortex about its leg. The four balance, as the legs close. TetA's vortex sits on one side of the cube along each axis and TetB's on the other, with the same spin: one swirl through the Field Origin, TetA at one end and TetB at the other.
7. **With closure, TetA couples to TetA (Theorem 7).** When every shared corner carries one chamber in all the cubes around it, the couplings close TetA to TetA across the tiling. Without closure they cross chambers.

## In vortex terms

A drained vortex is a swirl about an axis plus a flow into its drain (the Burgers vortex of the [tug-of-war proof](../constitutive-law-tug-of-war/)). On the tiled cube, torsion has exactly those two kinds of part, and TetA's and TetB's swirls join into one vortex through the Field Origin: spiral, throat, spiral. The Christoffel 40 is the part with no handedness. This reading is the framework's; the algebra under it is exact.

## Premises

- **(T) Tiling.** Cubes tile space, each holding one whole stellated octahedron.
- **(S) Sharing.** A channel couples to the cubes that share it, and to nothing at a distance (the Laplacian's neighbour comparison).
- **(C) Closure.** Every shared corner carries one chamber in all the cubes around it (Paper I's "where parts meet they agree"). Only Theorem 7 uses it.

Each is shown necessary in the proof: an isolated cube gives 16 couplings, not 64; without fixing the roles, 1,152 matches are possible; any other sign rule misses the couplings; without closure, the couplings cross chambers.

## What it leaves open

- **Dynamics.** This is the connection's index structure, which is the level at which Γ is built, the same in general relativity. Its transformation law and parallel transport need a field on the tiling whose coupling coefficients are Γ. There, torsion would be the net circulation through the corner channels. That is the next step.
- **Letter 2's reading of the 24 as TetB.** The handed couplings are TetA's, and they run toward the TetB corner piercing each face. That fits the reading but does not prove it.
- **The K² of a₀ = K²Gm_e/r_e².** Each face carries K² = 16 couplings; that this is the K² in a₀ is not shown.
- **Lean.** Every statement is finite and integer, so a formalisation importing the forced-frame and Gram chain is straightforward; it is not yet written.

## Contents

| File | What it is |
|---|---|
| [`tiled_cube_affine_connection.tex`](tiled_cube_affine_connection.tex), [`.pdf`](tiled_cube_affine_connection.pdf) | The proof |
| [`verify_tiled_cube_affine_connection.py`](verify_tiled_cube_affine_connection.py) | 44 exact checks; check i.j belongs to Theorem i |
| [`verify_output.txt`](verify_output.txt) | Its output |

## Reproduce

```
python3 verify_tiled_cube_affine_connection.py    # 44/44, with a per-theorem summary
```

## Related

- Working notes, with the two labellings of the tiling compared and the 3 × 3 × 3 ladder: [`research/diamond-tetrad-lattice/cube-tiling/`](../../research/diamond-tetrad-lattice/cube-tiling/).
- [Half-space regions](../half-space-two-bounded-regions/) (the channels), [forced frame](../forced-tetrahedral-frame/) (the legs), [Gram matrix](../gram-matrix-tetrad-equation/) (the index grid), [torsion as the regular representation](../torsion-regular-representation/) (the sectors), [chiral holonomy](../chiral-holonomy-closed-frame/) and [vortices](../vortices-of-the-stellated-octahedron/) (circulation on the cube).
