# The Pixel Lattice: One Stellated Octahedron per Cube, and the Diamond Nets Its Legs Form

*Field Dynamics Research, research folder, 2026-11-14. Status: research, not a paper. Verification: `python verify_diamond_tetrad_lattice.py` (33 checks, exact).*

`lattice` `diamond` `photonic-crystal` `bond-reciprocity` `stellated-octahedron` `TetA` `TetB` `parity` `research`

---

## Question

The framework reads the vacuum as a lattice of photons ([The Pixel and the Lattice](../photonic/the-pixel-and-the-lattice.md)): as ice's pattern follows from water's bond angle, the lattice should follow from the pixel's geometry. Which lattice is it?

The tetrad equation $g = e^T\eta e$ has two roots ([Gram-matrix proof](../../proofs/gram-matrix-tetrad-equation/)):
- **TetA**, the legs $M$: the cube corners with $xyz = +1$, $(1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1)$.
- **TetB**, the parity root $-M$: the corners with $xyz = -1$.

Together they are the stellated octahedron in its cube. The lattice is cubic: pixels tile space as cubes, and each cube holds one whole stellated octahedron, its centre the pixel's Field Origin and its eight legs running to that cube's own corners. This note asks what that tiling looks like from the tetrad's side. It reads each root as the bond star of a site, its four bonds pointing along its legs, and finds the diamond lattice running through the cubic tiling (results 1–6), then shows how the two fit together (result 7).

## Results

**1. The legs are a tetrahedral bond star.** Their Gram matrix is $4I - J$: each leg has squared length 3, and each pair has inner product $-1$. So every bond angle is the tetrahedral angle, $\cos\theta = -1/3$ (checks 1.1–1.5).

**2. One root cannot make a lattice.** A bond must run both ways: if a site bonds to its neighbour along $v$, the neighbour bonds back along $-v$.
- No reversed TetA leg is a TetA leg: $M$ and $-M$ share no vector (checks 2.1, 2.2).
- So a lattice in which every site carries TetA has no bond that runs both ways.
- A neighbour that bonds back along every leg must carry $-M$, which is TetB (check 2.3).

In lattice terms, the tetrad equation needs both roots for its bonds to close.

**3. Alternating the roots builds the diamond lattice.** Start at one TetA site, and give each neighbour the other root. Then:
- No site is ever reached carrying both roots, so the alternation is consistent (3.1).
- The TetA sites are exactly a face-centred cubic (fcc) lattice, spanned by $(2,2,0), (2,0,2), (0,2,2)$ (3.2, 3.7).
- The TetB sites are the same fcc lattice shifted by $(1,1,1)$ (3.3).
- Two fcc lattices offset along a body diagonal form the diamond lattice (3.4).
- Every site has four neighbours, all carrying the other root, and every bond runs both ways (3.5, 3.6).

**4. Parity is the lattice's own inversion.** Inversion through the midpoint of any bond maps TetA sites onto TetB sites, and each site's bonds onto its image's bonds (4.1, 4.2).

**5. Edges and rings.**
- The six edges of the TetA tetrahedron are the twelve same-root (second-neighbour) vectors of the lattice (5.1).
- The smallest rings are hexagons, and twelve pass through every site (5.2, 5.3).

**6. What fixes diamond is the parity root, not reciprocity alone.**
- Turn the TetB star 60° about a shared bond. It still bonds back (6.1), but it is no longer $-M$ (6.2). A turn of this kind gives the eclipsed bond of hexagonal stacking, the lonsdaleite form of diamond.
- The turned star has the same Gram matrix (6.3), so the metric cannot tell the two stackings apart.
- The tetrad's own second root, the parity image $-M$, is what selects the diamond lattice. This is the root-blindness of the metric again, now at the level of the lattice: the frame decides, the metric does not.

**7. The cubic tiling of pixels, and the diamonds its legs form.** Tile space with cubes. Each cube holds one whole stellated octahedron: its eight vertices are that cube's corners (7.1), and its eight legs run from the centre to them. Neighbouring cubes share corners, never pixels.
- **Every corner is shared evenly.** It belongs to 8 cubes: it is a TetA vertex in 4 and a TetB vertex in the other 4 (7.2).
- **Neighbouring cubes swap.** Across every face, a shared corner that is TetA in one cube is TetB in the next (7.3). So on each shared face, one cube's TetA edge is the next cube's TetB edge (7.4).
- **The TetA legs meet at the corners in a TetB shape.** At each corner, the TetA legs of its 4 cubes arrive along the four TetB directions (7.5).
- **Joined at the corners, the TetA legs of all the cubes form diamond nets.** There are exactly two. One is the diamond lattice of results 3–4, moved by $(1,1,1)$, and the other is the same net moved by one cube (7.6, 7.7). Their nodes alternate between a cube centre, the Field Origin with its TetA star, and a shared corner, where the arriving legs form a TetB star (7.8). The TetB legs form two more diamond nets the same way (7.9).

So the picture is the cubic lattice with one whole stellated octahedron in each cube. Every leg lies inside its own cube. The diamond nets are what the legs make when they meet at the shared corners: each pixel's TetA legs hand on, at the corner, to the TetB shape of its neighbours. This is result 2 inside the tiling. A pixel's TetA legs cannot link it to another pixel directly; they close only through the reversed, TetB-shaped junction at the corners.

## What this adds to GFD

- **The structure inside the cubic lattice, named.** With one stellated octahedron in each cube, neighbouring cubes swap TetA and TetB across every face. The pixels' legs, joined at the shared corners, run through the tiling as diamond nets: two from the TetA legs and two from the TetB legs, each alternating Field Origin and corner.
- **TetB is required, not optional.** The usual reading of the tetrad equation keeps one root and drops the other by convention. As a lattice, one root cannot close; both are needed.
- **A photonic link.** The diamond structure is the landmark photonic crystal. Ho, Chan and Soukoulis (1990) showed that dielectric spheres on a diamond lattice have a complete photonic band gap, which simple fcc structures lack. The widest gap came from structures built from the bonds alone, the rods between sites, which are the TetA and TetB legs here.
- **The ice analogy made exact.** Water's tetrahedral bonding builds the same two nets: cubic ice is a diamond net of oxygen atoms, and ordinary hexagonal ice is the lonsdaleite-type net. Result 6 is the same choice for the tetrad, settled by the parity root. High-pressure ice VII is two interpenetrating diamond networks on a body-centred cubic lattice of oxygen atoms. That is the arrangement of the cube centres and corners in result 7, with the two TetA nets as its two networks.

## What is not established

- **That the vacuum is this lattice.** The algebra gives a lattice from the two roots once the legs are read as bonds of a spatial net. That reading, and the identification of the sites or bonds with photons, are the framework's, not consequences of the checks.
- **That "photonic" follows.** The diamond structure's band gap is a statement about light in a dielectric lattice. It is suggestive for the framework, not a derivation of it.
- **Any GFD observable.** Nothing here yet gives $\mu(x)$, $a_0$ or the 64 field-closure states. That is the next step.

## Next

1. **Coupling between the two sites.** Build the simplest wave model on this lattice (one mode per site, coupling along the bonds), and ask whether the share of a mode on TetA sites against TetB sites can give $\mu = x/(x+1)$ for some physically defined $x$. If it can, the lattice becomes the mechanism behind the constitutive law rather than a picture of it.
2. **The 64 states as lattice modes.** Ask whether the 64 field-closure states appear among the lattice's modes or symmetries (the cube's $8 \times 8$ Walsh–Hadamard structure is the natural candidate).
3. **Then a proof.** Once the statements here are settled, move the exact parts (results 1–4, 6 and 7) into `proofs/` as a short proof.

## Files

| File | What it does |
|---|---|
| [`verify_diamond_tetrad_lattice.py`](verify_diamond_tetrad_lattice.py) | 33 exact checks, labelled by the result numbers above |

## Reproduce

```
python verify_diamond_tetrad_lattice.py    # 33/33
```

## Related

- [Gram matrix of the tetrad equation](../../proofs/gram-matrix-tetrad-equation/): the two roots, their Gram matrix $4I - J$, and parity as the only difference.
- [The Pixel and the Lattice](../photonic/the-pixel-and-the-lattice.md) and [The Photonic Substrate](../photonic/the_photonic_substrate_enterprise_full_thinking.md): the framework's reading of the vacuum as a lattice of photons.
- [Two connections and the dual chamber](../two-connection-dual-chamber/): what distinguishes the roots is orientation.

## Reference

K. M. Ho, C. T. Chan and C. M. Soukoulis, "Existence of a photonic gap in periodic dielectric structures", Phys. Rev. Lett. **65**, 3152 (1990).
