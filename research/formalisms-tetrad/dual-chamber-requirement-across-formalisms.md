# The Dual-Chamber Structure Across Gravitational Formalisms

### Tetrad gravity, bimetric gravity, loop quantum gravity, spinor theory and stability analysis, read against the GFD stellated octahedron

*Field Dynamics Research, working note, October 2026.*

---

## Abstract

Gravity Field Dynamics (GFD) holds that the local unit of the gravitational field is not one tetrahedral chamber but two interpenetrating chambers of opposite orientation, TetA and TetB. Together they form the stellated octahedron, coupled at a single central Field Origin.

This note surveys five established formalisms in which a twofold structure appears:

- the two chiralities of spinor matter coupled through the tetrad;
- the two metrics of any consistent theory of a massive graviton;
- the self-dual and anti-self-dual halves of the Lorentz algebra;
- the double cover $SL(2,\mathbb C)$ of the Lorentz group;
- the stability conditions of massive gravity.

For each, it states what the formalism establishes and how GFD connects it to the stellated octahedron. It then sets out what GFD derives that the formalisms assume, the open questions the comparison raises, and the predictions that distinguish the dual-chamber reading.

The formalisms are consistent with the dual-chamber picture and motivate it. GFD's distinctive claim is stronger: that the twofold structure each formalism exhibits in its own language is one geometric object, derived from a single tetrad.

## 1. The premise

A single regular tetrahedron has a definite orientation; its apex points one way. A field built from one such chamber would distinguish orientations at the most local level, whereas gravity couples to mass-energy without regard to spatial orientation. GFD therefore takes the local frame to carry a second chamber of opposite orientation, which restores inversion symmetry ([`04-dual-tetrahedron-field-origin.md`](../../docs/01-foundations/04-dual-tetrahedron-field-origin.md)).

## 2. Five formalisms with a twofold structure

### 2.1 Tetrad gravity and spinor matter

In metric general relativity the basic variable is $g_{\mu\nu}$. Spinor fields cannot be coupled to the metric alone, because they transform under the local Lorentz group rather than under general coordinate transformations. Coupling them requires two things:
- the tetrad (vierbein) $e^a{}_\mu$, four orthonormal vector fields relating the curved manifold to a local Minkowski frame;
- the spin connection $\omega^{ab}{}_\mu$ built from it.

This construction is due to Weyl (1929) and Fock (1929); the spin connection is also known as the Fock–Ivanenko coefficients. The surrounding history:
- **Cartan (1922)** had introduced torsion, the antisymmetric part of the connection.
- **Einstein (1928)** used tetrads in his teleparallel (*Fernparallelismus*) programme for a unified field theory.

The Dirac field carries both chiralities, separated by the projectors $\tfrac12(1 \pm \gamma^5)$. The tetrad itself is a single frame. Its role is to make the coupling of both chiral halves of matter possible.

**In GFD.** The two chiralities correspond to the two oppositely oriented chambers. Letter 2 makes this concrete. The tetrad equation $g_{\mu\nu} = \eta_{ab}\, e^a{}_\mu e^b{}_\nu$ is quadratic in the frame, so it admits two roots related by spatial parity. These are TetA and TetB, and the metric cannot distinguish them.

### 2.2 Bimetric gravity

- **The ghost.** Boulware and Deser (1972) showed that generic nonlinear theories of a massive graviton propagate a sixth degree of freedom with negative energy, the Boulware–Deser (BD) ghost.
- **Ghost-free massive gravity.** de Rham, Gabadadze and Tolley (2011) constructed a nonlinear massive gravity whose potential removes it. Any Lorentz-invariant graviton mass term requires a second metric. In this theory, dRGT, that metric is a fixed reference metric.
- **Bimetric gravity.** Hassan and Rosen (2012) proved the absence of the ghost and extended the theory to one in which the second metric $f_{\mu\nu}$ is itself dynamical. The interaction is built from the matrix square root $\sqrt{g^{-1}f}$, through five coefficients $\beta_0, \dots, \beta_4$.
- **The vielbein form.** Hinterbichler and Rosen (2012) gave the vielbein formulation, in which the two metrics become two interacting tetrads.

The bimetric theory propagates seven degrees of freedom: two of a massless and five of a massive spin-2 field.

**In GFD.** The two interacting tetrads are the two chambers. Paper XII ([`12-dual-tetrad-covariance-hassan-rosen/`](../../papers/12-dual-tetrad-covariance-hassan-rosen/)) develops a term-by-term correspondence between the GFD action and the Hassan–Rosen potential. It fixes the coefficients as $\beta = \{1, 0, 16, 0, 1\}$, which are palindromic under the exchange TetA ↔ TetB and determined by $K = 4$ alone.

### 2.3 Loop quantum gravity and the Ashtekar variables

**The connection and its two halves.** Ashtekar (1986) reformulated canonical general relativity in terms of a connection $A^i{}_a$ and a conjugate densitised triad $E^a{}_i$. This brought the constraints into polynomial form and the theory close to a Yang–Mills phase space. The connection is the self-dual part of the spin connection. Over the complex numbers, the Lorentz algebra splits into self-dual and anti-self-dual halves:

$$\mathfrak{so}(3,1)_{\mathbb C} \cong \mathfrak{su}(2)_{\mathbb C} \oplus \mathfrak{su}(2)_{\mathbb C}.$$

The original formulation works with one half, and reality conditions recover real general relativity. Modern loop quantum gravity uses the real Ashtekar–Barbero connection (Barbero 1995) with the Barbero–Immirzi parameter (Immirzi 1997).

**Discreteness and the quantum tetrahedron.**
- Rovelli and Smolin (1995) showed that area and volume operators have discrete spectra: spin-network nodes carry quanta of volume and links carry quanta of area.
- A four-valent node corresponds semiclassically to a quantum tetrahedron (Barbieri 1998; Baez and Barrett 1999).
- Gauge invariance at the node imposes the closure constraint: the area vectors of the faces sum to zero.
- More generally, an $n$-valent node describes a polyhedron with $n$ faces, by Minkowski's theorem (Bianchi, Doná and Speziale 2011).

**In GFD.** The four-valent node with its closure constraint is the single chamber. Letter 1's four tetrad-derived directions satisfy the same condition, $\sum_i v_i = 0$, and bound the regular tetrahedron. In GFD the valence is not a free choice: four is the minimum number of faces that encloses a volume in three dimensions ($K = D + 1$).

The chiral split connects through the exterior algebra (§3.2).

### 2.4 Spinor theory and the double cover

The group acting on spinors is $SL(2,\mathbb C)$, the double cover of the proper orthochronous Lorentz group (Penrose and Rindler 1984). A spinor returns to itself only after a rotation of $720^\circ$. Two-component spinors come in two inequivalent kinds, unprimed and primed (left- and right-handed). A real four-vector is built from one of each, and a null tetrad is built from a spinor dyad.

**In GFD.** Each chamber realises one sheet of the double cover. A $360^\circ$ rotation realigns TetA but leaves TetB out of phase, and a second turn realigns both. The same face structure gives the intrinsic spin $\hbar/2$ ([`08-face-structure-and-spin.md`](../../docs/01-foundations/08-face-structure-and-spin.md)).

### 2.5 Stability

The stability argument is the Boulware–Deser result of §2.2. A stable, Lorentz-invariant theory of a massive graviton needs two metrics together with a potential of the special dRGT–Hassan–Rosen form. Massless general relativity, with one metric, is stable.

**In GFD.** The seven propagating modes of the bimetric theory, each coupling through the four faces of a chamber, give $7 \times 4 = 28$ mode–face couplings. This equals the number of geometric elements of the stellated octahedron, $V + E + F = 8 + 12 + 8$ ([`09-twenty-eight-geometric-elements.md`](../../docs/01-foundations/09-twenty-eight-geometric-elements.md)).

## 3. The geometry

### 3.1 The parity partition

Label the eight vertices of a cube by three-bit addresses, $000$ to $111$, and divide them by the parity of their bit count:
- even: $000, 011, 101, 110$;
- odd: $001, 010, 100, 111$.

Within each group every pair of addresses differs in exactly two bits, so all six pairwise distances are equal. Each group is therefore a regular tetrahedron. The two are vertex-, edge- and face-disjoint. Each tetrahedron's six edges are face diagonals of the cube, and the twelve edges of the pair are exactly the cube's twelve face diagonals.

These are the only two regular tetrahedra with vertices among the cube's vertices. Their compound is the stellated octahedron, which Kepler named *stella octangula* in *De Nive Sexangula* (1611); it had been drawn earlier by Pacioli (1509) and Jamnitzer (1568).

The four body diagonals join each vertex to its complement ($000$–$111$ and so on) and cross at the centre of the cube, where the position vectors of all eight vertices sum to zero. GFD names this point the **Field Origin**: the single point at which the two chambers couple.

### 3.2 The exterior algebra and self-duality

The exterior algebra of four generators has graded dimensions $\binom{4}{k} = \{1, 4, 6, 4, 1\}$. The GFD exterior-algebra note ([`exterior_algebra_derivation.md`](../../papers/letter-1-tetrad-frame-geometry/Supplementary/research/exterior_algebra_derivation.md)) assigns the grades as follows:
- **grade 1:** TetA;
- **grade 3:** TetB, its Hodge dual;
- **grade 2:** six elements, one for each edge, whose midpoints are the vertices of the octahedral region shared by the two tetrahedra.

The Hodge star exchanges grades 1 and 3, so the exchange of the chambers is the Hodge involution.

The same operator defines chirality in gravity. Grade 2 is the space of bivectors, and the Lorentz algebra $\mathfrak{so}(3,1)$ is exactly this six-dimensional space. On it the Hodge star squares to $-1$, and its eigenspaces (over $\mathbb C$) are the self-dual and anti-self-dual halves on which the Ashtekar variables are built.

**In GFD**, one operator therefore does two jobs: it exchanges the two chambers (grades 1 ↔ 3), and it splits the six Lorentz generators (grade 2) into the two chiral halves.

### 3.3 The structural inventory

| Quantity | Expression | Value | Reading |
|---|---|---|---|
| Faces per tetrahedron | $K$ | 4 | minimal enclosure in $D = 3$ |
| Vertices of the compound | $2^D$ | 8 | the binary address space $\{0,1\}^3$ |
| Edges of the compound | $K \cdot D = 2\binom{K}{2}$ | 12 | the cube's face diagonals |
| Edges + Field Origin | $K \cdot D + 1$ | 13 | the GFD structural floor; $f(K, -1) = 13$ |
| Face-to-face coupling channels | $K^2$ | 16 | four faces × four sub-channels |

**The sixteen components of the tetrad** divide in the standard way as $16 = 10 + 6$. Ten fix the metric. The other six are local Lorentz freedom, the dimension of the Lorentz group, and GFD pairs them with the six edges of one tetrahedron. In the ADM decomposition (Arnowitt, Deser and Misner 1962) the ten metric components divide further into lapse (1), shift (3) and spatial metric (6).

**In discrete gravity**, curvature in Regge calculus is concentrated on the codimension-2 simplices: edges in three dimensions and triangles in four (Regge 1961).

## 4. What GFD derives that the formalisms assume

The formalisms of §2 each contain a twofold structure, but most of them introduce it by hand:
- bimetric gravity postulates the second metric;
- the Ashtekar formulation chooses one chiral half;
- the BD analysis shows what a theory needs, not why nature supplies it.

GFD's programme is to derive the twofold structure from a single tetrad:

| Result | Statement | Source |
|---|---|---|
| Two chambers from one frame | The sixteen sign combinations of the four half-spaces of a single tetrad give exactly two bounded regions, TetA and TetB, whose compound is the stellated octahedron. No second frame is assumed. | Letter 1, [`letter-1-tetrad-frame-geometry/`](../../papers/letter-1-tetrad-frame-geometry/) |
| Two roots of one equation | The tetrad equation is quadratic. Its solution space (scheme) has exactly two spatial components, $SO(3)$ and $P \cdot SO(3)$, related by parity. Both satisfy the same equation with the same metric. | [`supplementary_scheme_proof.tex`](../../papers/letter-1-tetrad-frame-geometry/Supplementary/supplementary_scheme_proof.tex) |
| The geometry is forced | Under common norm, balanced closure and $S_4$ symmetry, the Gram matrix of the spatial tetrad is fixed. The regular tetrahedron, and hence the stellated octahedron, is the unique realisation. | [`supplementary_spatial_geometry_of_the_lorentz_tetrad.tex`](../../papers/letter-radial-acceleration-relation-sparc/supplementary/supplementary_spatial_geometry_of_the_lorentz_tetrad.tex); [`verify_gram_theorems.py`](../../papers/gram-matrix-of-tetrad-equation/verify_gram_theorems.py) |
| Torsion carries the distinction | A torsion-free connection depends only on the metric and so cannot tell the two roots apart. The 24 torsion components carry the TetA/TetB distinction. At $K = 4$ the torsion sector carries the regular representation of $S_4$, which contains the parity representation. | Letter 2, [`letter-2-other-half-of-gravity-torsion/`](../../papers/letter-2-other-half-of-gravity-torsion/); Paper B, [`algebraic-papers-a-b-c/`](../../papers/algebraic-papers-a-b-c/) |
| The exchange fixes the law | Exchange symmetry between the two chambers forces the constitutive law $\mu(x) = x/(x+1)$. | [`letter-constitutive-law-tetrad-geometry/`](../../papers/letter-constitutive-law-tetrad-geometry/) |
| The split is polynomial | The torsion-free condition keeps 40 and discards 24 of the 64 connection components: the coupling polynomial at its two opposite states. | Letter 3, [`EINSTEIN_TETA_PARTITION.md`](../../EINSTEIN_TETA_PARTITION.md) |

On this reading, the twofold structures of §2 are not five separate facts. They are five views of the two roots of the tetrad equation.

## 5. Open questions

The comparison also raises questions that a complete account must answer.

1. **Torsion in Einstein–Cartan theory.** In Einstein–Cartan–Sciama–Kibble theory (Kibble 1961; Sciama 1964; Hehl et al. 1976), torsion is algebraic rather than propagating, and it is sourced only by spin density. GFD assigns the torsion sector the TetB share of the field, $1 - \mu(x)$, which is largest at galactic radii. GFD must say how its torsion sector differs from the Einstein–Cartan one, and why it is not suppressed in the same way.
2. **Teleparallel gravity.** The teleparallel equivalent of general relativity (Aldrovandi and Pereira 2013) is built entirely on torsion, with the curvature of the Weitzenböck connection set to zero, yet it is dynamically equivalent to general relativity. GFD's restored torsion sector must be distinguished from that reformulation.
3. **A fixed or a dynamical second chamber.** dRGT achieves ghost-freedom with a fixed reference metric; Hassan–Rosen with a dynamical one. In GFD both chambers arise from the same tetrad. The relation between that structure and the fixed-versus-dynamical distinction should be stated explicitly.
4. **One chiral half or two.** The Ashtekar formulation works with one chiral half plus reality conditions. Whether GFD's two chambers correspond to two independent dynamical sectors, or to one sector and its conjugate, should be made precise.
5. **Valence.** Loop quantum gravity admits nodes of any valence. GFD selects four. The argument from minimal enclosure ($K = D + 1$) should be connected to the quantum dynamics, for instance to whether four-valent nodes dominate the semiclassical limit.

## 6. What the dual-chamber reading predicts

None of the five formalisms on its own yields the following results, which follow in GFD from the two-chamber structure:

| Prediction | Result | Source |
|---|---|---|
| The interpolating function | $\mu(x) = x/(x+1)$, derived rather than fitted | constitutive-law letter |
| The radial acceleration relation | 164 SPARC galaxies, 3284 points, scatter 0.181 dex, with no parameter fitted to the galaxies | [`letter-radial-acceleration-relation-sparc/`](../../papers/letter-radial-acceleration-relation-sparc/) |
| Mass from rotation | Enclosed mass decoded from observed velocity for the Milky Way and M33, with no dark-matter halo | [`letter-decoding-mass-from-rotation-curves/`](../../papers/letter-decoding-mass-from-rotation-curves/) |
| Tully–Fisher evolution | $v(z)/v(0) = [H(z)/H_0]^{0.17}$; all nine IFU measurements to $z = 3$ within the predicted band | [`tully-fisher-velocity-evolution/`](../../papers/tully-fisher-velocity-evolution/) |
| The torsion split | 40 retained and 24 discarded connection components, from $f(K, \pm 1)$ | Letter 3 |

## 7. Conclusion

Each of the five formalisms carries a genuine and central twofold structure:
- the two chiralities of spinor matter;
- the two metrics of a massive graviton;
- the self-dual and anti-self-dual halves of the Lorentz algebra;
- the double cover $SL(2,\mathbb C)$;
- the stability conditions that require both a second metric and a special potential.

The parity partition of the cube produces two disjoint regular tetrahedra about a common centre. The Hodge star of the exterior algebra both exchanges them and splits the Lorentz algebra into its chiral halves.

GFD's claim is that these are one structure: the two roots of the tetrad equation, realised as the two chambers of the stellated octahedron. The formalisms make that claim consistent and well motivated. Letters 1–3 and their supplements derive it, and the galactic predictions of §6 test it. The open questions of §5 mark where the account must still be completed.

---

## References

- Aldrovandi, R. and Pereira, J. G. (2013). *Teleparallel Gravity: An Introduction*. Springer.
- Arnowitt, R., Deser, S. and Misner, C. W. (1962). The dynamics of general relativity. In L. Witten (ed.), *Gravitation: An Introduction to Current Research*. Wiley. Reprinted as [arXiv:gr-qc/0405109](https://arxiv.org/abs/gr-qc/0405109).
- Ashtekar, A. (1986). New variables for classical and quantum gravity. *Phys. Rev. Lett.* 57, 2244.
- Baez, J. C. and Barrett, J. W. (1999). The quantum tetrahedron in 3 and 4 dimensions. *Adv. Theor. Math. Phys.* 3, 815. [arXiv:gr-qc/9903060](https://arxiv.org/abs/gr-qc/9903060).
- Barbero, J. F. (1995). Real Ashtekar variables for Lorentzian signature space-times. *Phys. Rev. D* 51, 5507. [arXiv:gr-qc/9410014](https://arxiv.org/abs/gr-qc/9410014).
- Barbieri, A. (1998). Quantum tetrahedra and simplicial spin networks. *Nucl. Phys. B* 518, 714. [arXiv:gr-qc/9707010](https://arxiv.org/abs/gr-qc/9707010).
- Bianchi, E., Doná, P. and Speziale, S. (2011). Polyhedra in loop quantum gravity. *Phys. Rev. D* 83, 044035. [arXiv:1009.3402](https://arxiv.org/abs/1009.3402).
- Boulware, D. G. and Deser, S. (1972). Can gravitation have a finite range? *Phys. Rev. D* 6, 3368.
- Cartan, É. (1922). Sur une généralisation de la notion de courbure de Riemann et les espaces à torsion. *C. R. Acad. Sci. Paris* 174, 593.
- de Rham, C., Gabadadze, G. and Tolley, A. J. (2011). Resummation of massive gravity. *Phys. Rev. Lett.* 106, 231101. [arXiv:1011.1232](https://arxiv.org/abs/1011.1232).
- Einstein, A. (1928). Riemann-Geometrie mit Aufrechterhaltung des Begriffes des Fernparallelismus. *Sitzungsber. Preuss. Akad. Wiss., Phys.-Math. Kl.*, 217. See [Sauer, arXiv:physics/0405142](https://arxiv.org/abs/physics/0405142) for the programme.
- Fock, V. (1929). Geometrisierung der Diracschen Theorie des Elektrons. *Z. Phys.* 57, 261.
- Hassan, S. F. and Rosen, R. A. (2012). Resolving the ghost problem in nonlinear massive gravity. *Phys. Rev. Lett.* 108, 041101. [arXiv:1106.3344](https://arxiv.org/abs/1106.3344).
- Hassan, S. F. and Rosen, R. A. (2012). Bimetric gravity from ghost-free massive gravity. *JHEP* 02, 126. [arXiv:1109.3515](https://arxiv.org/abs/1109.3515).
- Hehl, F. W., von der Heyde, P., Kerlick, G. D. and Nester, J. M. (1976). General relativity with spin and torsion: foundations and prospects. *Rev. Mod. Phys.* 48, 393.
- Hinterbichler, K. and Rosen, R. A. (2012). Interacting spin-2 fields. *JHEP* 07, 047. [arXiv:1203.5783](https://arxiv.org/abs/1203.5783).
- Immirzi, G. (1997). Real and complex connections for canonical gravity. *Class. Quantum Grav.* 14, L177. [arXiv:gr-qc/9612030](https://arxiv.org/abs/gr-qc/9612030).
- Kepler, J. (1611). *Strena seu de nive sexangula*. Frankfurt.
- Kibble, T. W. B. (1961). Lorentz invariance and the gravitational field. *J. Math. Phys.* 2, 212.
- Penrose, R. and Rindler, W. (1984). *Spinors and Space-Time, Vol. 1: Two-Spinor Calculus and Relativistic Fields*. Cambridge University Press.
- Regge, T. (1961). General relativity without coordinates. *Nuovo Cimento* 19, 558.
- Rovelli, C. and Smolin, L. (1995). Discreteness of area and volume in quantum gravity. *Nucl. Phys. B* 442, 593. [arXiv:gr-qc/9411005](https://arxiv.org/abs/gr-qc/9411005).
- Sciama, D. W. (1964). The physical structure of general relativity. *Rev. Mod. Phys.* 36, 463.
- Weyl, H. (1929). Elektron und Gravitation. I. *Z. Phys.* 56, 330.

**GFD documentation:** [`04-dual-tetrahedron-field-origin.md`](../../docs/01-foundations/04-dual-tetrahedron-field-origin.md), [`08-face-structure-and-spin.md`](../../docs/01-foundations/08-face-structure-and-spin.md), [`09-twenty-eight-geometric-elements.md`](../../docs/01-foundations/09-twenty-eight-geometric-elements.md), [`10-stellated-octahedron.md`](../../docs/01-foundations/10-stellated-octahedron.md).
