# The Pixel Lattice: One Stellated Octahedron per Cube, and the Diamond Nets Its Legs Form

*Field Dynamics Research, research folder, 2026-11-14. Status: research, not a paper. Verification: `python verify_diamond_tetrad_lattice.py` (52 checks, exact).*

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

**8. Carbon's sp³ orbitals are the Gram-matrix proof's Hadamard matrix.** The four tetrahedral sp³ hybrids of a diamond-lattice atom have the coefficient matrix $\tfrac12[1;\,M]$, rows $s, p_x, p_y, p_z$. This is the bordered matrix $[1;\,M]$ of the Gram-matrix proof, a Hadamard matrix, divided by 2 (8.1, 8.2).
- Each hybrid is $\tfrac14$ $s$ and $\tfrac34$ $p$, and its $p$-part points along its TetA leg (8.3).
- The $p$-parts meet at the tetrahedral angle (8.4).
- A TetB site's hybrids are $\tfrac12[1;\,-M]$ (8.5). Along every bond, the TetA and TetB hybrids point at each other (8.6).

**9. The bond between a TetA site and a TetB site gives $\mu(x)$ exactly.** In the bond-orbital model of chemistry (Harrison), a bond joins two hybrids. A covalent energy $V_2$ couples them, and a polar energy $V_3$ puts the TetA hybrid at $-V_3$ and the TetB hybrid at $+V_3$. The bonding orbital is the lower state of this two-level problem (9.0, 9.1). Then:
- **Its shares are $\mu$ and $1-\mu$.** The bonding electron sits on the TetA end with weight $\mu = x/(1+x)$, where $x$ is its odds between the two ends (9.2), and $x = (u + \sqrt{1+u^2})^2$ with $u = V_3/V_2$ (9.3).
- **Polarity is $2\mu - 1 = (x-1)/(x+1)$,** the share difference the framework already uses (9.4).
- **Covalency squared is $4\mu(1-\mu)$,** four times the logistic term $x\,d\mu/dx$ (9.5, 9.6).
- **Exchange is polarity reversal.** Swapping the two ends, $u \to -u$, sends $x \to 1/x$ (9.7).
- **The equal-share point $x = 1$ is the nonpolar bond,** both ends alike, which is diamond itself (9.8). Polar compounds on the same lattice, such as GaAs, have $x \ne 1$.

So any given $x$ needs $V_3/V_2 = (x-1)/(2\sqrt x)$ (9.9). For $x = g/a_0$, that is a polar energy $(g - a_0)/2$ and a covalent coupling $\sqrt{g a_0}$. With those, the bonding orbital has amplitudes $(\sqrt g,\ \sqrt{a_0})$ and TetA share $g/(g+a_0)$, and the bond gap is $g + a_0$ (9.10, 9.11). Shifted by $(g+a_0)/2$, the bond matrix has rank one: a single coupled channel (9.12).

## What this adds to GFD

- **The structure inside the cubic lattice, named.** With one stellated octahedron in each cube, neighbouring cubes swap TetA and TetB across every face. The pixels' legs, joined at the shared corners, run through the tiling as diamond nets: two from the TetA legs and two from the TetB legs, each alternating Field Origin and corner.
- **TetB is required, not optional.** The usual reading of the tetrad equation keeps one root and drops the other by convention. As a lattice, one root cannot close; both are needed.
- **A photonic link.** The diamond structure is the landmark photonic crystal. Ho, Chan and Soukoulis (1990) showed that dielectric spheres on a diamond lattice have a complete photonic band gap, which simple fcc structures lack. The widest gap came from structures built from the bonds alone, the rods between sites, which are the TetA and TetB legs here.
- **A mechanism-shaped reading of $\mu(x)$.** The constitutive law has exactly the algebra of the chemical bond between a TetA site and a TetB site: $\mu$ is the bonding electron's share on the TetA end, exchange is swapping the ends, and the equal-share ring is the nonpolar bond. The question "why $\mu(x)$?" becomes one precise question: why would the polar energy scale as $g - a_0$ and the coupling as $\sqrt{g a_0}$? The coupling $\sqrt{g a_0}$ is the familiar deep-field scale.
- **The ice analogy made exact.** Water's tetrahedral bonding builds the same two nets: cubic ice is a diamond net of oxygen atoms, and ordinary hexagonal ice is the lonsdaleite-type net. Result 6 is the same choice for the tetrad, settled by the parity root. High-pressure ice VII is two interpenetrating diamond networks on a body-centred cubic lattice of oxygen atoms. That is the arrangement of the cube centres and corners in result 7, with the two TetA nets as its two networks.

## What is not established

- **That the vacuum is this lattice.** The algebra gives a lattice from the two roots once the legs are read as bonds of a spatial net. That reading, and the identification of the sites or bonds with photons, are the framework's, not consequences of the checks.
- **That "photonic" follows.** The diamond structure's band gap is a statement about light in a dielectric lattice. It is suggestive for the framework, not a derivation of it.
- **That the bond picture is the mechanism.** Any two-state system gives a share $x/(1+x)$; that algebra alone is generic. What is specific here is the identification: the two states are the TetA and TetB ends of a lattice bond, and parity is polarity reversal. Result 9 shows what the energies would have to be, not that they are.
- **Any GFD observable.** Nothing here derives $a_0$, the scaling of the bond energies with $g$, or the 64 field-closure states. [`TEST_PLAN.md`](TEST_PLAN.md) sets out 20 tests aimed at these.

## Next

[`TEST_PLAN.md`](TEST_PLAN.md) sets out 20 Python tests, each with its question, method and pass criterion fixed in advance. Once the statements here are settled, the exact parts (results 1–4 and 6–9) can move into `proofs/` as a short proof.

## Files

| File | What it does |
|---|---|
| [`verify_diamond_tetrad_lattice.py`](verify_diamond_tetrad_lattice.py) | 52 exact checks, labelled by the result numbers above |
| [`TEST_PLAN.md`](TEST_PLAN.md) | 20 planned tests to take the lattice and the bond reading further |

## Reproduce

```
python verify_diamond_tetrad_lattice.py    # 52/52
```

## Related

- [Gram matrix of the tetrad equation](../../proofs/gram-matrix-tetrad-equation/): the two roots, their Gram matrix $4I - J$, and parity as the only difference.
- [The Pixel and the Lattice](../photonic/the-pixel-and-the-lattice.md) and [The Photonic Substrate](../photonic/the_photonic_substrate_enterprise_full_thinking.md): the framework's reading of the vacuum as a lattice of photons.
- [Two connections and the dual chamber](../two-connection-dual-chamber/): what distinguishes the roots is orientation.

## References

W. A. Harrison, *Electronic Structure and the Properties of Solids* (Freeman, 1980): the bond-orbital model, polarity and covalency.

K. M. Ho, C. T. Chan and C. M. Soukoulis, "Existence of a photonic gap in periodic dielectric structures", Phys. Rev. Lett. **65**, 3152 (1990).
