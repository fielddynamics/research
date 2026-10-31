# Field Closure

*A bubble, not a film · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`field-closure` `tetrad` `coupling-polynomial` `stellated-octahedron` `general-relativity` `bbp-formula` `pi`

---

Dip a wire loop in soapy water and lift it out. A film stretches across the loop, shimmering and perfectly real, but it holds nothing. It has no inside and no outside. Blow gently and it bellies outward. Then, at one particular instant, it pinches off, seals itself, and becomes a bubble.

Nothing new was added at that instant. The soap is the same soap, and the film is the same thickness. What changed is that the surface **closed**. A closed surface is a different kind of object. It encloses a volume, holds a pressure and keeps its shape. It also keeps strict books: every bit of the film is accounted for, and none of it runs off the edge, because there is no edge.

This folder begins from one idea: **a gravitational field must close, like a bubble.** A field that does not close is a soap film. It can be described locally, but it has no identity of its own. Everything else in this archive grew out of asking what closure demands.

## Where this started

I am a tech engineer with an interest in theoretical physics. My working life has been spent building enterprise systems, including encryption systems for government, where structure has to close: data must reconcile, transactions must settle, state must return to a valid configuration, and every transform must invert without loss. In that world, a system that leaves something unaccounted for is a broken system, however good each part looks on its own.

Field closure is what launched this work. The first paper, [*Distributed Field Processing: The Gravitational Constitutive Law*](../../papers/01-gravitational-constitutive-law/2026-01_28_Nelson_DFP_Gravitational_Constitutive_Law.pdf) (January 2026), reads gravity the way an engineer reads a distributed system. A field that carries waves from one place to another, as gravitational waves do, cannot be monolithic: it must have parts, and the Laplacian at the heart of every field equation is literally a comparison between neighbours. Parts that couple must reconcile. Where one field meets another, each side must read what the other is doing, and the coupling must settle into one consistent state across every interface at once. Settlement is atomic: either all the coupling channels agree, or the configuration has not settled. That settlement is field closure. Requiring it to be lossless (no wakes, drag or hysteresis) and locally evaluable (causality forbids global computation), formalised as Postulates A1–A3, leaves one constitutive law within the minimal single-channel saturating closure class, $\mu(x) = x/(1+x)$: a conditional theorem, not a fit. In three dimensions the smallest closed coupling has four channels, the tetrahedron.

The papers that followed carried the idea further: [*Topological Field Closure*](../../papers/2026-01-26-Topological_Field_Closure_A_Bidirectional_Derivation_of_the_Hubble_Constant_and_the_Electron_Mass.pdf) and [*Field Closure and the Topology of Gravity*](../../papers/05-field-closure-and-topology-of-gravity/2026-01_29_Nelson_DFPV_Field_Closure_And_The_Topology_Of_Gravity.pdf), then the tetrad letters, the galaxy results and the nuclear work, each an attempt to follow closure one step further.

What follows is an introduction to the idea, written for anyone curious enough to follow it.

— Stephen Nelson

## What closure demands

### The smallest closed thing

In three dimensions, the smallest number of flat walls that can enclose a volume is four. Three walls make at best an open trough. Four make a tetrahedron, the simplest possible bubble. This is the **simplex theorem**: in $d$ dimensions, closure needs $d + 1$ faces. For our space, $K = D + 1 = 4$.

General relativity already contains this number. Its most fundamental form uses the **tetrad**, a frame of four directions at every point of spacetime. Fermions such as electrons cannot be coupled to gravity without it. Letter 1 asks a question that, as far as we know, had not been asked: *what shape do the tetrad's four directions make in space?*

### Two bubbles from one frame

Each of the tetrad's four spatial directions defines a wall with two sides. Choosing one side of each wall gives $2^4 = 16$ possible regions. Fourteen of them are open: they leak to infinity, like films with an edge. Exactly two of them close.

The reason is the closure condition itself. A region is sealed when the inward normals of its walls cancel, so that the walls surround the centre from every direction. For the tetrad's directions,

$$v_1 + v_2 + v_3 + v_4 = 0 .$$

The four directions cancel, and so do their four negatives. The first sealed region is the tetrahedron **TetA**. The second is a mirror-image tetrahedron, **TetB**, which nobody put in: it emerges from the same four walls. The two interpenetrate to form the stellated octahedron, Kepler's *stella octangula*, and they share a single central point, the **Field Origin** (Letter 1).

There is an algebraic reason the second bubble must be there. The metric is built from the tetrad by squaring, $g_{\mu\nu} = \eta_{ab}\,e^a{}_\mu e^b{}_\nu$, and a square has two roots. TetA and TetB are those two roots. They produce the same metric, so a theory built on the metric alone cannot tell them apart.

## The accounting

Closure is bookkeeping. A sealed bubble has no edge for anything to slip off, so every quantity has to balance. Seen this way, the core results of GFD are a set of ledgers. Each must balance exactly, and each does.

| Ledger | The books | What balances |
|---|---|---|
| **Regions** | 16 ways to choose sides of four walls | 2 sealed regions, 14 open. Closure picks out the pair (Letter 1). |
| **Vertices** | Two tetrahedra, each with $D+1$ corners, against the $2^D$ corners of a cube | $2(D+1) = 2^D$, which holds only at $D = 3$: 8 corners, all used, none left over, none missing. |
| **Connection** | The gravitational connection has $K^3 = 64$ components | 40 retained plus 24 removed by the torsion-free condition. Per face, $16 = 10 + 6$, which is the coupling polynomial at its two opposite states, $(f(K,\pm1) - 1)/2$ (Letter 3). |
| **Field** | The field response, shared between the two chambers | $\mu + (1 - \mu) = 1$ at every radius, with TetA carrying $\mu(x) = x/(x+1)$ and TetB carrying $1/(x+1)$ (Letter 2). |
| **Coupling** | The polynomial $f(K,s) = 1 + sK + K^2$ at its three states | $21$, $17$, $13$: equally spaced, with the Field Origin value 17 exactly the mean of the other two. The range is $2K = 8$, the vertex count. |
| **Walk** | One orbit of the closure walk around the eight vertices | Signed contributions $+4 - 2 - 1 - 1 = 0$: one orbit deposits nothing net. |

**When the books do not balance.** In 1915 general relativity made the connection torsion-free. That choice keeps 40 of the 64 components and removes 24. Letters 2 and 3 show that the 24 removed components are exactly the ones that carry the TetB root. A torsion-free theory therefore books the whole field to TetA, setting $\mu = 1$.

Where the field is strong, as in the solar system, this costs almost nothing. TetB's share there is less than one part in a million, which is why general relativity passes every local test. Where the field is weak, at the edges of galaxies, TetB carries most of the field, and a theory that does not book it finds a shortfall.

The shortfall is $1/(x+1)$, and its ratio to what was booked is $1/x$. That is precisely the ratio conventionally attributed to dark matter. In the language of this folder, dark matter is the unbooked half of a closed field: a film mistaken for a bubble.

## The field closure pipeline

Closure is not only a principle. It runs as a pipeline, from the demand that the field seal to numbers that can be compared with telescopes. Every stage is forced by the one before it, and no stage introduces a free parameter.

**Forward: from closure to the field equations.**

1. **Closure in three dimensions** needs four faces: $K = D + 1 = 4$.
2. **Exact partition** of the coordinate cell by two closed tetrahedra: $2(D+1) = 2^D$, so $D = 3$.
3. **Two roots of the tetrad equation**: TetA and TetB, the stellated octahedron, coupled at the Field Origin (Letter 1).
4. **The coupling polynomial**: the tetrad equation has a scalar, a vector and a tensor part. These scale as $K^0$, $K^1$ and $K^2$, and only the vector part changes sign between the chambers. So $f(K,s) = 1 + sK + K^2$ (Letter 2; [`derivation_chain_coupling_polynomial.md`](derivation_chain_coupling_polynomial.md)).
5. **The partition**: exchange symmetry between the two chambers allows exactly one split of the field, $\mu(x) = x/(x+1)$ (Letter 2).
6. **The energy functional**: integrating $\mu$ gives $F(y) = y - 2\sqrt y + 2\ln(1 + \sqrt y)$. Its three terms are the three levels of the polynomial (Letter 3).
7. **The action**: Einstein–Hilbert plus the scalar sector built on $F$, with electromagnetic and matter terms (Letter 3).
8. **The field equations**: in the spherical, static limit, the action gives the Poisson equation and the scalar-tensor transition (SST), $g_s = g_t^2/(a_0 + g_t)$.

**Inverse: from what we observe back to what is there.** Because both field equations are algebraic in the spherical case, the pipeline also runs backwards ([*GFD Essentials*](../../papers/gfd-essentials-tetrads-field-closure-inverse-pipeline/)):

$$v(r) \;\longrightarrow\; g_t = \frac{v^2}{r} \;\longrightarrow\; g_s = \frac{g_t^2}{a_0 + g_t} \;\longrightarrow\; M(r) = \frac{r\,v^4}{G\,(a_0 r + v^2)} .$$

Measure how fast stars orbit, and the closed field returns the mass that must be there, with no dark-matter halo and no fitted profile. Applied to 164 galaxies, the same chain reproduces the radial acceleration relation. Applied to the Milky Way and M33, it decodes their enclosed mass directly from the rotation curve.

## The closure walk

The rest of this folder explores a more unusual question. If the field must close, how does it *traverse* its own structure to do so?

Give the eight corners of the cube their three-bit addresses, 0 to 7, and walk among them. A face of the stellated octahedron closes when all three of its corners have been visited. The whole structure closes when every one of the $8 \times 8 = 64$ ordered transitions between corners has occurred.

- **Driven by π.** Driven by the digits of π in base 8, stepping by cumulative sum, the walk closes all eight faces in its first 16 steps and all 64 transitions at step 332. It stays almost perfectly balanced between the two chambers along the way.
- **The six constraints.** The notes in this folder go further. Reading the face normals of the tetrahedron through the three spatial axes, they assemble a series with base $16 = K^2$, four terms per orbit (one per face), and signed numerators that cancel over each orbit. That series is term-for-term the Bailey–Borwein–Plouffe formula for π (1995). [*Why π*](why_pi_formal_derivation.md) argues that each coefficient is fixed by the geometry.

The BBP formula and the digits of π are established mathematics. The reading of BBP as the stellated octahedron's own closure walk is GFD's interpretation, set out with verification scripts so that every step can be checked.

## Contents

| File | Contents |
|---|---|
| [`derivation_chain_coupling_polynomial.md`](derivation_chain_coupling_polynomial.md) | **Start here.** From the 3+1 structure of spacetime to the coupling polynomial in nine steps: the simplex theorem, the uniqueness equation, the parity partition, and the three structural ranks of the tetrad equation |
| [`why_pi_formal_derivation.md`](why_pi_formal_derivation.md) | Why the closure walk yields π: six geometric constraints that assemble the BBP series |
| [`why_pi_verification.py`](why_pi_verification.py) | Checks each of the six constraints and the term-by-term match with BBP (20 checks) |
| [`closure_walk_proof.py`](closure_walk_proof.py) | Two-source check: π in base 8 from arbitrary-precision arithmetic and from the three-axis reading, matched digit for digit across 401 digits, with the walk closing all 64 transitions at step 332 |
| [`pi_base8_field_closure_walk_full_synthesis.docx`](pi_base8_field_closure_walk_full_synthesis.docx) | A technical synthesis of the walk: face addressing, macro-cycles, the canonical and π walks compared, and the balance between chambers |
| [`so_sierpinski_walk.html`](so_sierpinski_walk.html) | Interactive 3D view: the π walk lighting the 64 transition triangles on the stellated octahedron |
| [`tetb_64_walk_of_field_closure.html`](tetb_64_walk_of_field_closure.html) | Interactive view of the 64-channel closure walk through the TetB chamber: faces, channels and sub-channels |

```bash
pip install mpmath
python why_pi_verification.py     # 20/20
python closure_walk_proof.py      # closure at step 332
```

## Related papers

- **Letter 1**, [*The Coordinate-Space Geometry of the Tetrad Frame*](../../papers/letter-1-tetrad-frame-geometry/): the two closed regions of a single tetrad.
- **Letter 2**, [*The Other Half of Gravity*](../../papers/letter-2-other-half-of-gravity-torsion/): torsion as the carrier of TetB, the partition $\mu + (1-\mu) = 1$, and the dark-to-baryon ratio $1/x$.
- **Letter 3**, [*Field Closure of the Tetrad Frame*](../../papers/letter-3-field-closure-of-tetrad-frame/): the 40/24 split as the coupling polynomial at its opposite states, the full 64-component connection, and the action. Summarised in [`EINSTEIN_TETA_PARTITION.md`](../../EINSTEIN_TETA_PARTITION.md).
- **Paper IX**, [*Complete Field Closure from Stellated Octahedron Topology*](../../papers/09-complete-field-closure/): the closure condition as an output rather than an input.
- [*GFD Essentials: Tetrads, Field Closure, and the Inverse Pipeline*](../../papers/gfd-essentials-tetrads-field-closure-inverse-pipeline/): the pipeline from tetrads to decoded mass.

---

*A soap film can be described point by point and still never be a bubble. The question this archive keeps asking is what changes, in the mathematics of gravity, at the moment the film seals.*
