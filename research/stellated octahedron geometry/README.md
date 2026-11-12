# The 64-Tetrahedron Grid

*The 64-TG as exact geometry, read in the coupling algebra · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`stellated-octahedron` `64-tetrahedron-grid` `isotropic-vector-matrix` `association-scheme` `coupling-algebra`

*Research folder, 2026-11-12. Status: working notes with checks, not a paper. Run `python3 verify_64_tetrahedron_grid.py` (24 checks, exact: integers, fractions, sympy). Run `python3 export_64tg_model.py` to regenerate the 3D model files. Open `viewer.html` in a browser to explore the grid.*

---

This folder holds B. R. Galeffi's paper *On the 14-Octahedron Backbone of the Bimetric 64-Tetrahedron Grid Universe* (PDF). The 64-Tetrahedron Grid (64-TG) is the well-known structure of 64 tetrahedra built from 8 stellated octahedra. They sit inside a large stellated octahedron and a cube.

GFD reads the stellated octahedron as the photon, and field closure reads 64 states on it. This folder builds the 64-TG as exact coordinates, recomputes Galeffi's counts, and finds that the four coupling relations of [`coupling-algebra/`](../coupling-algebra/) ($A_0$ to $A_3$) sort the 64 tetrahedra into the grid's own anatomy.

## The model

- Take a $2\times2\times2$ block of unit cubes. The Field Origin is the centre $(1,1,1)$.
- Each small cube holds one stellated octahedron (a "star"). A star is a core octahedron plus 8 tetrahedral spikes, one tip at each corner of its cube.
- Label a star by the corner $c \in \{0,1\}^3$ of its cube nearest the block's origin. Label a spike by the corner $f \in \{0,1\}^3$ of that cube it points to.
- So **each of the 64 tetrahedra is an ordered pair of cube corners, (which star, which spike)**. The spike's tip sits at $c + f$. Its base is the three face centres of cube $c$ that meet at corner $f$.

In Galeffi's units, $a$ is the edge of the embedded cuboctahedron. Here $a = \sqrt2$, so the small tetrahedra have edge $a/2$ and the block is the cube of side $\sqrt2\,a$.

## Results

Tags follow [`certify_first_principles.py`](../coupling-algebra/certify_first_principles.py):
- **CLASSICAL**: known geometry, recomputed.
- **NEW**: a reading not found in the archive or in Galeffi.
- **CORRECTION**: a published number that the exact model changes.

### 1. The relation between star and spike fixes where the spike lands (NEW)

Write $d(c,f)$ for the Hamming distance, the number of coordinates where $c$ and $f$ differ. This is the coupling algebra's relation $A_d$. It alone decides where the tip lands:

| Relation | Tetrahedra | Tips land on | Distance from the Field Origin | Tips per point | In the coupling algebra |
|---|---|---|---|---|---|
| $A_0$ ($f = c$) | 8 | the 8 points of the large star (big-cube corners) | $\sqrt3$ | 1 | the corner itself |
| $A_1$ | 24 | the 12 vertices of the cuboctahedron (vector equilibrium) | $\sqrt2$ | 2 | vector links, **between** chambers |
| $A_2$ | 24 | the 6 vertices of the large star's core octahedron | $1$ | 4 | within a chamber |
| $A_3$ ($f = \bar c$) | 8 | the Field Origin | $0$ | 8 | parity, **between** chambers |

- The tips per point are $2^d$.
- The 27 tip points fill the block's $3\times3\times3$ lattice, with weights $1, 2, 1$ along each axis. So $64 = (1+2+1)^3$.
- The 48 symmetries of the grid act on star and spike together, and they sort the 64 tetrahedra into exactly **four kinds, one per relation** (8, 24, 24, 8). These are the cube's own $1, 3, 3, 1$ multiplied by the 8 stars.

### 2. The 64-TG is the large star plus the 24 vector links (NEW, checked by volume)

Test every vertex of every tetrahedron against the large stellated octahedron (tetrahedron edge $2a$). The result:

- **40 tetrahedra lie inside the large star**: all of $A_0$ (8), $A_2$ (24) and $A_3$ (8). Together with the 14 octahedral cavities they fill it exactly:

  $$40\cdot\tfrac{\sqrt2}{96}a^3 + 14\cdot\tfrac{\sqrt2}{24}a^3 = \sqrt2\,a^3 = V_{\text{large star}}.$$

- **The 24 $A_1$ spikes are the only tetrahedra outside it.** They are tipped two at each vertex of the cuboctahedron, which are the midpoints of the block cube's 12 edges. Adding them gives Galeffi's own total:

  $$\sqrt2\,a^3 + 24\cdot\tfrac{\sqrt2}{96}a^3 = \tfrac{5\sqrt2}{4}a^3 = V_{\text{64-TG}}.$$

So the grid splits along the coupling algebra. **64-TG = large star ($A_0 + A_2 + A_3$ and the 14 octahedra) + the 24 vector links ($A_1$).**

Two more inclusions, both CLASSICAL counts that Galeffi also gives:
- The 56 tetrahedra inside the cuboctahedron are everything except $A_0$.
- The 8 inside the central octahedron are exactly $A_3$, meeting at the Field Origin.

### 3. The 14 octahedra (CLASSICAL, with one reading)

The 14 cavities are the 8 star cores, one at each small-cube centre, and 6 more around the Field Origin.
- The 6 central octahedra point from the Field Origin to the 6 vertices of the large star's core octahedron. Those are exactly the $A_2$ tip points.
- The 14 cavities have $14\times8 = 112$ faces. Every one of them is a tetrahedron face.
- The 64 tetrahedra have 256 faces, and no face is shared between two tetrahedra. So $256 - 112 = 144$ faces are bare.
- Nodes: 63, which is 27 tips + 36 small-cube face centres. Segments: 240. Both agree with Galeffi.

### 4. Polarity and chamber depend on the scale (NEW)

- Galeffi's two polarities split the 64 into 32 + 32. In the model, a spike's polarity is the chamber (TetA or TetB) of its own corner $f$.
- The 8 points of the large star all sit at even positions of the fine lattice. So the fine chamber label cannot split the large star into its two tetrahedra.
- What does split them is the coarse label, the parity of "which star" $c$ (4 and 4).
- So the chamber of the composite is read from the star label, while the chamber of each photon is read from its spike label.
- The relations $A_1$ and $A_3$ (odd $d$) are exactly the ones whose star and spike lie in opposite chambers.

### 5. The grid's own coupling algebra is larger (computed, open)

The operators on the 64 tetrahedra that commute with the grid's 48 symmetries form an algebra of **dimension 120**. This number is computed, not predicted. Its structure (which part reduces to the cube's 4-dimensional coupling algebra on each label, and what the rest couples) is not analysed here.

## Correction to Galeffi's Table 3 (CORRECTION)

Galeffi's Table 3 lists the tetrahedra (edge $a/2$) inside each nested polyhedron. For the large stellated octahedron ($2a$) it gives **16** tetrahedra and a packing density of $1/6 \approx 0.166$. The exact model gives **40** and a density of **$5/12 \approx 0.417$**.

- Galeffi's own volumes settle it. His total volume of the 64-TG, $5\sqrt2a^3/4$, minus the 24 tetrahedra outside the large star leaves $\sqrt2a^3$.
- The large star's volume is $\sqrt2a^3$, which Galeffi also states.
- So 40 tetrahedra and 14 octahedra fill the large star exactly (check G7b). With 16 tetrahedra the volumes do not balance.

His other three columns are confirmed (check G11):
- the 64-TG, $8/15$;
- the cuboctahedron, 56 tetrahedra, $7/20$;
- the octahedron, 8 tetrahedra, $1/4$.

## Not checked

The following parts of Galeffi's paper are not assessed here:
- the Fibonacci assignments to radii and volumes (fits to curves);
- the jitterbug and construction-protocol sections;
- the cosmological readings.

## Drawing and sketching the 64-TG

| File | What it is | Opens in |
|---|---|---|
| `viewer.html` | Interactive 3D viewer. Toggle the relations $A_0$–$A_3$, the 14 octahedra and the outlines (large star, cuboctahedron, cube). Colour by relation, polarity or star. Explode the grid. Click a tetrahedron to read its (star, spike) label. | any browser (loads three.js from a CDN) |
| `64tg.obj` + `64tg.mtl` | The same exact geometry as a mesh. One group per relation, plus the two octahedron sets and a large-star reference. | Blender, FreeCAD, MeshLab, Windows 3D Viewer, most CAD and 3D tools |
| `64tg_geogebra.txt` | One `Execute` command that draws all 64 tetrahedra and 14 octahedra, coloured by relation. | [GeoGebra 3D](https://www.geogebra.org/3d): paste into the Input bar |

To sketch it by hand, GeoGebra 3D is the simplest tool. One tetrahedron is

```
Pyramid((0,0.5,0.5), (0.5,0,0.5), (0.5,0.5,0), (0,0,0))
```

This is the $A_0$ spike of star $000$: its base is three face centres and its tip is the corner. Every other spike follows the rule in "The model" above.

**Caveat:** the GeoGebra command file was generated, not tested in GeoGebra from here. The OBJ and the viewer were checked.

## Contents

| File | Purpose |
|---|---|
| `On the 14-Octahedron Backbone of the Bimetric.pdf` | Galeffi's paper (source) |
| `verify_64_tetrahedron_grid.py` | 24 exact checks: the anatomy and relations (1–9), Galeffi's counts and the Table 3 correction (G1–G11) |
| `export_64tg_model.py` | Writes `64tg.obj`, `64tg.mtl`, `64tg_geogebra.txt` from the same rules |
| `viewer.html` | Interactive viewer |

## Related

- [`coupling-algebra/`](../coupling-algebra/): the relations $A_0$–$A_3$ on the cube's 8 corners, the two TetA–TetB channels, parity as $A_3$.
- [`universe-is-pixelated/`](../universe-is-pixelated/): the cube's Walsh spectrum.
- [Paper VII, `GEOMETRIC_FOUNDATIONS.md`](../../papers/07-dual-tetrad-topology-field-origin/v5/GEOMETRIC_FOUNDATIONS.md): the isotropic vector matrix and the 64-tetrahedron grid in the archive.
- [`g_from_topology/`](../g_from_topology/): the 1, 4, 16, 64 counts.

## References

- B. R. Galeffi, *On the 14-Octahedron Backbone of the Bimetric 64-Tetrahedron Grid Universe* (PDF in this folder).
- R. B. Fuller, *Synergetics* (1975): the isotropic vector matrix and the vector equilibrium.
