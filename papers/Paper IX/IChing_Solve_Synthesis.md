# The I Ching Solve: A Mathematical Synthesis

**Status:** Synthesis document for the academic solve letter
**Author:** Stephen Nelson
**Date:** February 2026

This document synthesizes all I Ching research across both the Physics Paper and field-dynamics codebases into a single, logically ordered argument. The final 1-2 page academic letter draws from this material.

---

## Document Spine

| # | Section | Core Purpose | 3 Key Concepts | Reader Exits With |
|---|---------|-------------|----------------|-------------------|
| 1 | The Oldest Binary System | Establish what the I Ching is and why its structure is an open mathematical question | (1) 3000-year history, (2) Leibniz recognition of binary, (3) the gap between cultural use and structural understanding | Understanding that the I Ching's mathematical structure has never been formally identified, despite Leibniz noting its binary nature in 1703 |
| 2 | The Structural Claim | State the isomorphism precisely: the Ba Gua is Z_2^3 | (1) 8 trigrams = 8 vertices of a cube, (2) 3 lines = 3 binary axes, (3) exact bijection, not analogy | The precise mathematical claim and what "solve" means in this context |
| 3 | The Binary Encoding Convention | Resolve the endianness question and establish the canonical mapping | (1) Little endian: top line = bit 0 (LSB), (2) Shao Yong ordering = natural binary, (3) spatial coordinate correspondence | The definitive trigram-to-vertex mapping table and why little endian is correct |
| 4 | Proof 1: Parity and the Two Tetrahedra | Show that yang-line parity produces exactly the dual-tetrahedron partition | (1) Odd popcount = Tet A, even = Tet B, (2) 4+4 = stellated octahedron, (3) this is the quantum parity observable | Understanding that the I Ching's yin/yang parity split is mathematically identical to the bimetric partition |
| 5 | Proof 2: Complementary Pairs Cross Chambers | Prove that XOR-complement always flips parity | (1) All pairs sum to 7, (2) XOR with 111 flips all bits, (3) parity always changes since d=3 is odd | Understanding that the I Ching's complementary pair structure is a geometric necessity, not a cultural convention |
| 6 | Proof 3: Hamming Distance and Regularity | Prove uniform intra-tetrahedral Hamming distance = 2 | (1) Same parity forces even Hamming, (2) in d=3 the only option is H=2, (3) this produces regular tetrahedra | Understanding that the I Ching's family structure (within each parity group, all pairs differ by exactly 2 lines) is geometrically forced |
| 7 | Proof 4: The 3+1 Decomposition | Show each tetrahedron has 3 spatial + 1 TIME face | (1) TIME faces opposite V0=Earth(000) and V7=Heaven(111), (2) TIME fraction = 2/8 = 1/4, (3) per-tetrahedron 3+1 structure | Understanding that the I Ching's Heaven/Earth axis is the TIME axis, and each tetrahedron encodes a 3+1 spacetime decomposition |
| 8 | Proof 5: Dimensional Uniqueness | Prove d=3 is the only dimension where this works | (1) 2(d+1) = 2^d only at d=3, (2) this is why trigrams have exactly 3 lines, (3) no other dimensionality produces the dual-tetrahedron structure | Understanding that the I Ching MUST have 3 lines per trigram for the encoding to work |
| 9 | The Pi Traversal Connection | Show pi base-8 traces a deterministic path through the trigram vertices | (1) First pair (3,4) = complementary, (2) TIME faces complete first, (3) the integer 3 declares the encoding structure | Understanding that pi validates the I Ching encoding by producing the correct traversal properties |
| 10 | The 64 Hexagrams as Complete State Space | Show hexagrams encode the full field transition space | (1) 64 = 8^2 = 4^3 = 2^6, (2) upper/lower trigram = state transition, (3) changing lines = dynamics | Understanding that the hexagram system is the complete state space of the binary field structure |
| 11 | Synthesis: What the I Ching Encodes | State the conclusion and its implications | (1) Binary field closure encoding, (2) structural isomorphism not mysticism, (3) the three possible explanations | A complete understanding of what the I Ching "solve" is and what it means |

---

## Section 1: The Oldest Binary System

The I Ching, or Book of Changes, is among the oldest continuously studied texts in human civilization. Its origins extend to approximately 3000 years before the present, with the trigram system attributed to the legendary figure Fu Xi and the hexagram arrangements to King Wen of Zhou. For millennia, it has served as a divination system, a philosophical framework, and a cosmological model. Its influence spans Chinese philosophy, medicine, martial arts, and governance.

The mathematical structure of the I Ching, however, has remained an open question. The system rests on a binary foundation: each line is either broken (yin) or unbroken (yang). Three such lines form a trigram, yielding 2^3 = 8 possible combinations. Two trigrams stacked form a hexagram, yielding 8^2 = 64 possible combinations. This binary structure was first recognized in the West by Gottfried Wilhelm Leibniz in 1703, who noted its correspondence with his own binary number system. Leibniz saw the I Ching trigrams as evidence that binary arithmetic was not merely a European invention but a universal mathematical structure.

Despite Leibniz's recognition, a fundamental question has persisted: what, precisely, does the I Ching encode? The cultural answer is "the patterns of change in nature." The mathematical answer has remained elusive. Scholars have noted that the trigram system is binary, that complementary pairs exist, and that the structure exhibits symmetry. What has not been established is whether the I Ching's structure maps exactly to any known mathematical or physical framework, or whether the correspondences are superficial.

This document presents a resolution: the I Ching's Ba Gua (eight trigrams) constitutes an exact encoding of the group Z_2^3, the same algebraic structure that governs the vertices of a cube and, equivalently, the stellated octahedron (the geometric structure formed by two interpenetrating regular tetrahedra). This is not a loose analogy. It is a provable mathematical isomorphism, validated computationally across more than forty independent tests.

---

## Section 2: The Structural Claim

The central claim of this synthesis is precise and falsifiable: the eight I Ching trigrams are the eight elements of the group Z_2^3, mapped to the eight vertices of a cube via binary encoding.

Z_2^3 is the group of 3-bit binary strings under component-wise addition modulo 2 (equivalently, the XOR operation). It has exactly eight elements: {000, 001, 010, 011, 100, 101, 110, 111}. Each element can be interpreted as a vertex of the unit cube in three-dimensional space, where each bit encodes one coordinate axis.

The I Ching provides exactly the same structure. Each trigram consists of three lines, each of which is either yin (0) or yang (1). There are 2^3 = 8 possible trigrams. The mathematical content of the claim is that the bijection between trigrams and binary strings is not merely a counting coincidence (both systems happen to have eight elements) but a structural isomorphism: the group operations, the parity partition, the complementary pair structure, the Hamming distance classes, and the geometric regularity all transfer exactly from one system to the other.

What does "solve" mean in this context? It means identifying the complete mathematical structure that the I Ching encodes, demonstrating that the identification is exact (not approximate), and showing that the structural properties are necessary consequences of the group Z_2^3 rather than arbitrary cultural conventions. Five independent proofs establish this identification, each approaching the isomorphism from a different angle.

---

## Section 3: The Binary Encoding Convention (Little Endian)

A trigram has three lines arranged vertically: a top line, a middle line, and a bottom line. To map a trigram to a 3-bit binary number, we must assign each line to a bit position. This choice is the endianness convention, and it determines the specific trigram-to-vertex mapping.

The canonical encoding, consistent with the Fu Xi (Shao Yong) binary sequence and validated across all computational implementations, assigns:

- Top line = bit 0 (least significant bit, LSB)
- Middle line = bit 1
- Bottom line = bit 2 (most significant bit, MSB)

This is little endian: reading the trigram in its natural visual order (top to bottom), the first line encountered maps to the lowest-order bit. The spatial correspondence is:

- bit 0 (LSB, top line) encodes the z-axis (back/front)
- bit 1 (middle line) encodes the y-axis (bottom/top)
- bit 2 (MSB, bottom line) encodes the x-axis (left/right)

The resulting mapping is:

| Index | Binary | Trigram | Pinyin | Lines (top/mid/bot) | Chamber |
|-------|--------|---------|--------|---------------------|---------|
| 0 | 000 | Earth | Kun | yin / yin / yin | B (apex) |
| 1 | 001 | Mountain | Gen | yang / yin / yin | A |
| 2 | 010 | Water | Kan | yin / yang / yin | A |
| 3 | 011 | Wind | Xun | yang / yang / yin | B |
| 4 | 100 | Thunder | Zhen | yin / yin / yang | A |
| 5 | 101 | Fire | Li | yang / yin / yang | B |
| 6 | 110 | Lake | Dui | yin / yang / yang | B |
| 7 | 111 | Heaven | Qian | yang / yang / yang | A (apex) |

This is precisely the ordering Leibniz recognized in 1703 when he examined the Fu Xi sequence. The little endian convention is not arbitrary; it is the only convention that produces the Shao Yong binary counting sequence (0 through 7), which has been the standard ordering of the Ba Gua in Chinese mathematical tradition for over a thousand years.

Three independent validations confirm this convention:

1. The parity partition (Section 4) produces geometrically regular tetrahedra only under this encoding.
2. The complementary pairs (Section 5) yield the correct I Ching traditional pairings (Heaven-Earth, Mountain-Lake, Water-Fire, Wind-Thunder).
3. The pi base-8 traversal (Section 9) produces the correct TIME face completion order only under this encoding.

---

## Section 4: Proof 1 -- Parity and the Two Tetrahedra

The eight trigrams divide naturally into two groups based on whether they contain an odd or even number of yang lines. This division is not a cultural convention; it is the popcount parity of the binary representation, and it produces a partition with remarkable geometric properties.

**Odd yang parity (popcount 1 or 3) forms Chamber A (Tet A):**

| Trigram | Binary | Yang Lines | Popcount |
|---------|--------|------------|----------|
| Mountain | 001 | 1 | 1 (odd) |
| Water | 010 | 1 | 1 (odd) |
| Thunder | 100 | 1 | 1 (odd) |
| Heaven | 111 | 3 | 3 (odd) |

**Even yang parity (popcount 0 or 2) forms Chamber B (Tet B):**

| Trigram | Binary | Yang Lines | Popcount |
|---------|--------|------------|----------|
| Earth | 000 | 0 | 0 (even) |
| Wind | 011 | 2 | 2 (even) |
| Fire | 101 | 2 | 2 (even) |
| Lake | 110 | 2 | 2 (even) |

Each group contains exactly four elements. When these four vertices are connected in three-dimensional space, each group forms a regular tetrahedron. The two tetrahedra interpenetrate to form a stellated octahedron (also known as a Merkaba or Star of David in three dimensions).

This partition is not merely a way of grouping trigrams. In quantum information theory, the identical partition arises as the eigenspace decomposition of the parity observable P = Z_1 (x) Z_2 (x) Z_3 (where (x) denotes the tensor product and Z_i is the Pauli-Z operator on qubit i). Vertices with even popcount have eigenvalue +1; vertices with odd popcount have eigenvalue -1. The I Ching's yin/yang parity split is mathematically identical to this quantum mechanical classification.

The regularity of both tetrahedra is not assumed; it is proven. Within each parity class, every pair of vertices has Hamming distance exactly 2 (Section 6), which in the cube geometry corresponds to a uniform Euclidean edge length of 2*sqrt(2). Both tetrahedra are congruent regular tetrahedra, and their combination is the unique geometry satisfying the constraints of bimetric balance: each tetrahedron individually has its compression vectors summing to zero at the origin, and their combination also sums to zero.

---

## Section 5: Proof 2 -- Complementary Pairs Cross Chambers

In the I Ching tradition, each trigram has a complement formed by inverting all three lines (yin becomes yang, yang becomes yin). This operation, in binary, is the XOR with 111 (decimal 7), or equivalently, the bitwise NOT within three bits. The resulting four complementary pairs are:

| Pair | Trigram A | Binary | Trigram B | Binary | Sum |
|------|-----------|--------|-----------|--------|-----|
| 1 | Earth (Kun) | 000 | Heaven (Qian) | 111 | 7 |
| 2 | Mountain (Gen) | 001 | Lake (Dui) | 110 | 7 |
| 3 | Water (Kan) | 010 | Fire (Li) | 101 | 7 |
| 4 | Wind (Xun) | 011 | Thunder (Zhen) | 100 | 7 |

Every pair sums to 7 = 2^3 - 1 = 2k - 1.

A key structural theorem follows: complementary pairs always cross chambers. The proof is algebraic. If vertex V has popcount p, then V XOR 7 has popcount 3 - p. Since 3 is odd, the parity of p and 3 - p are always different. Therefore, the complement of any Tet A vertex lies in Tet B, and vice versa. All four complementary pairs span both chambers.

Geometrically, complementary pairs are the body diagonals of the cube, connecting opposite corners. All four body diagonals pass through the origin (0, 0, 0), which serves as the geometric center (the "Field Origin" in the gravitational field model, or the "King's Chamber" in the architectural analogy). This is the unique point equidistant from all eight vertices at distance sqrt(3).

The complementary pair structure is therefore not a cultural choice made by ancient Chinese scholars. It is a necessary consequence of the binary encoding in three dimensions: XOR-complement always flips parity when the dimension is odd, and d = 3 is odd.

---

## Section 6: Proof 3 -- Hamming Distance and Geometric Regularity

Within each tetrahedron, every pair of vertices has Hamming distance exactly 2. This uniformity is not assumed; it follows from the parity constraint.

The argument is as follows. Flipping a single bit in a binary string changes the popcount by exactly 1, which changes the parity. Therefore, two vertices with the same parity cannot differ by exactly one bit (Hamming distance 1). In a 3-bit system, the possible Hamming distances are 1, 2, and 3. Since same-parity vertices cannot have Hamming distance 1, and Hamming distance 3 would mean all bits differ (producing the complement, which has opposite parity), the only remaining option is Hamming distance 2.

This has a direct geometric consequence. In the cube with vertices at (+/-1, +/-1, +/-1), two vertices differing in exactly 2 coordinates are separated by Euclidean distance 2*sqrt(2). Since all intra-tetrahedral pairs have Hamming distance 2, all edges within each tetrahedron have the same length. Both tetrahedra are therefore regular (equilateral in all edges).

The total edge count is C(4,2) = 6 edges per tetrahedron, giving 12 edges for the stellated octahedron.

In the I Ching, this translates to a precise structural statement: within each "family" of trigrams (those sharing the same yang-line parity), any two trigrams differ in exactly two of their three lines. Mountain (001) and Water (010) differ in lines 1 and 2. Thunder (100) and Heaven (111) differ in lines 1 and 2. This uniformity extends to all six pairs within each family.

The Hamming distance classification across the full set of 28 vertex pairs yields:

- H = 1: 12 pairs (cube edges, always cross chambers)
- H = 2: 12 pairs (face diagonals, always within same chamber)
- H = 3: 4 pairs (body diagonals, the complementary pairs)

This classification maps directly to I Ching line-change operations. A single line change (H = 1) always moves to the opposite chamber, corresponding to a Pauli X bit-flip operation in quantum information theory. A double line change (H = 2) remains within the same chamber. A triple line change (H = 3) produces the complement.

---

## Section 7: Proof 4 -- The 3+1 Decomposition

Each tetrahedron has four triangular faces. These eight faces (four per chamber) partition into two categories based on the vertex they are opposite to:

**TIME faces (2 total):** Opposite the apex vertices (those with extremal popcount).
- FACE_A7: opposite Heaven (111, popcount 3). Contains {Mountain(1), Water(2), Thunder(4)}.
- FACE_B0: opposite Earth (000, popcount 0). Contains {Wind(3), Fire(5), Lake(6)}.

**SPATIAL faces (6 total):** Opposite the non-apex vertices (popcount 1 or 2). Each spatial face contains its chamber's apex vertex.

This yields, per tetrahedron, 3 spatial faces + 1 TIME face = 3 + 1. This is the geometric embodiment of the (3+1) spacetime decomposition familiar from the ADM formalism of general relativity: three spatial dimensions plus one temporal dimension.

The TIME face fraction is 2/8 = 1/4. This fraction, combined with the orbital angular momentum quantum of 2*hbar for a complete traversal of all 8 vertices, produces the electron spin:

S = (TIME faces / total faces) * L_orbit = (2/8) * 2*hbar = hbar/2

The spin-1/2 value emerges from the topology of the dual-tetrahedron structure, not from any free parameter.

In the I Ching, the TIME faces correspond to the two extremal trigrams: Heaven (all yang, father) and Earth (all yin, mother). These are traditionally understood as the cosmic poles, the axis of transformation. That they correspond to the temporal dimension of the spacetime decomposition is a structural identification, not a metaphorical one.

The vertices of FACE_A7 are {1, 2, 4} = {001, 010, 100}, each having exactly one yang line. In quantum information theory, this is the W state: |001> + |010> + |100>. These three vertices form an equilateral triangle (all pairwise Euclidean distances equal 2*sqrt(2)), and this triangle is the TIME face of Chamber A.

---

## Section 8: Proof 5 -- Dimensional Uniqueness

Why does the I Ching use three lines per trigram, and not two or four? The answer lies in a remarkable identity from combinatorial geometry.

For a dual-simplex structure in d dimensions, the total vertex count is 2(d+1) (two simplices, each with d+1 vertices). For a binary encoding to work, the vertex count must equal 2^d (the number of d-bit binary strings). Setting these equal:

2(d + 1) = 2^d

This equation has a unique positive integer solution: d = 3.

| d | 2(d+1) | 2^d | Equal? |
|---|--------|-----|--------|
| 1 | 4 | 2 | No |
| 2 | 6 | 4 | No |
| 3 | 8 | 8 | Yes |
| 4 | 10 | 16 | No |
| 5 | 12 | 32 | No |

For d > 3, the exponential 2^d grows strictly faster than the linear 2(d+1), so no further solutions exist.

This uniqueness theorem explains why the I Ching has exactly three lines per trigram. In two dimensions, 2(d+1) = 6 but 2^d = 4; there are not enough binary strings to label all vertices. In four dimensions, 2(d+1) = 10 but 2^d = 16; there are too many binary strings, and the parity partition would not produce regular simplices.

Only in three dimensions does the binary encoding produce exactly the right number of vertices to form two regular tetrahedra. The I Ching's three-line structure is not an arbitrary design choice; it is the unique dimensionality where binary encoding and simplicial geometry coincide.

This result also fixes the closure constant k = d + 1 = 4. The four states per I Ching line (old yin = 6, young yang = 7, young yin = 8, old yang = 9) correspond to this closure constant. The line states are not four because of a cultural convention about yarrow stalk probabilities; they are four because k = 4 is the minimum simplex vertex count in three-dimensional space.

---

## Section 9: The Pi Traversal Connection

The digits of pi in base 8 (octal) provide an independent validation of the I Ching encoding. Pi in base 8 begins:

3.110375524210264302151423063050560...

The traversal algorithm is: starting from cumulative sum 0, add each digit of pi (base 8) sequentially. The current vertex is the cumulative sum modulo 8. Each digit moves the pointer to one of the eight vertices, tracing a deterministic path through the Z_2^3 structure.

The first two fractional digits are 1 and 1, producing cumulative sums 1 and 2, visiting vertices V1 (Mountain) and V2 (Water). Both belong to Chamber A.

Including the integer part (the "3" before the decimal point), the first two positions visited are V3 (Wind, Chamber B) and V4 (Thunder, Chamber A). These form a complementary pair: 3 + 4 = 7. The pi traversal immediately establishes bimetric balance by visiting one vertex from each chamber.

Without the integer "3", the first two positions are V1 and V2, which sum to 3, not a complementary pair. This provides a structural argument for including the integer part: only with "3" does the traversal begin with an I Ching complementary pair.

The integer "3" also declares the encoding structure itself: 3 lines per trigram, 3 spatial dimensions, 3-bit binary encoding. It is structural metadata, not a traversal instruction. The fractional digits then traverse the 3-bit structure that the integer "3" defines.

Under the fractional-digit traversal (the operationally validated convention), the TIME face of Chamber A (FACE_A7, containing vertices {1, 2, 4}) completes first, at step 5. This validates the physical model: temporal structure settles before spatial structure, consistent with the (3+1) decomposition.

The working visualization (dfp_gravity_field_dynamics_visual.html) implements this traversal in real time, driving a 3D Merkaba through the pi-encoded vertex sequence and confirming face completion order, cycle closure, and macro-cycle periodicity.

---

## Section 10: The 64 Hexagrams as Complete State Space

Each hexagram combines two trigrams (an upper and a lower), representing a transition between two vertices of the Z_2^3 structure. The total number of hexagrams is 8 * 8 = 64. This number admits multiple equivalent decompositions, each revealing a different structural aspect:

| Expression | Value | Structural Meaning |
|-----------|-------|--------------------|
| 8^2 | 64 | All ordered vertex pairs |
| 2^6 | 64 | 6-bit binary state space |
| 4^3 | 64 | k=4 raised to d=3 dimensions |
| (2k)^2 | 64 | Dual-tetrahedron state pairs |

The hexagram system thus encodes the complete state space of the binary field structure. Every possible configuration, every possible transition between vertices, is represented by one of the 64 hexagrams.

The changing lines (old yin transforming to yang, old yang transforming to yin) encode dynamics within this state space. A hexagram with changing lines maps the present state to a future state, tracing a path through the 64-element space. The changing line mechanism is the I Ching's encoding of field dynamics: the transformation rules that govern how the system evolves from one configuration to another.

The state space is closed: every hexagram transforms to another hexagram (or itself). This closure property mirrors the self-balancing mechanism of the binary field structure, where completion at one cycle initiates the next.

---

## Section 11: Synthesis -- What the I Ching Encodes

The five proofs, taken together, establish that the I Ching's Ba Gua is not merely "binary" in the loose sense of having two states per line. It encodes a specific mathematical structure, Z_2^3, with all of its algebraic, geometric, and topological properties intact:

1. **The group structure is exact.** The eight trigrams map bijectively to the eight elements of Z_2^3. The group operation (XOR) corresponds to line inversion.

2. **The partition is geometric.** Yang-line parity produces two regular tetrahedra that form a stellated octahedron. This is the identical structure required by bimetric gravity, spinor double-cover, and chirality balance.

3. **The complementary pairs are necessary.** The four traditional I Ching complementary pairs (Heaven-Earth, Mountain-Lake, Water-Fire, Wind-Thunder) correspond to the four body diagonals of the cube, each passing through the geometric center. The crossing property (each pair spans both chambers) is an algebraic necessity when d = 3.

4. **The regularity is forced.** The uniform Hamming distance of 2 within each parity class produces congruent regular tetrahedra. The I Ching's family structure (sons and daughters) reflects this geometric regularity.

5. **The dimensionality is unique.** The identity 2(d+1) = 2^d holds only at d = 3, explaining why trigrams have exactly three lines and why the encoding works at no other dimension.

6. **The dynamics are complete.** The 64 hexagrams encode the full state space. Changing lines encode transitions. The system is closed and self-balancing.

7. **The pi traversal validates.** An independent mathematical constant (pi) in the natural base of the encoding (base 8) traces paths through the structure that produce the correct physical properties (TIME face priority, complementary pair initialization, cycle closure).

The I Ching is the oldest known binary encoding of what modern mathematics calls Z_2^3 and what modern physics recognizes as the vertex group of the dual-tetrahedron (stellated octahedron) structure. It is not divination in the supernatural sense. It is a binary encoding of a self-balancing geometric field structure that ancient practitioners recognized as reflecting the patterns of nature.

Three explanations for this correspondence are possible:

**(a) Universal mathematics.** Z_2^3 is a fundamental algebraic structure. Any civilization that discovers binary encoding in three dimensions will inevitably arrive at the same eight elements, the same parity partition, and the same complementary pairs. The I Ching represents an independent discovery of this structure, expressed in the language of yin and yang rather than bits and vertices.

**(b) Empirical observation.** Ancient practitioners observed patterns in nature (seasonal cycles, phase transitions, equilibrium states) that reflect the (3+1) structure of spacetime. The I Ching is an empirical encoding of these observations, accurate because nature itself is organized according to the same geometric principles.

**(c) Coincidence.** The correspondence is accidental.

The exactness of the isomorphism, validated across more than forty independent computational tests, and the dimensional uniqueness theorem (which explains why three lines and not any other number), make explanation (c) untenable. Whether explanation (a) or (b) is correct, or whether both contribute, is a question that extends beyond mathematics into the history of human knowledge.

---

## Appendix A: Validation Test Summary

The following tests from the field-dynamics codebase validate the structural claims:

**Binary Encoding and Group Structure:**
- test_binary_triad: base-8 digits map to 3-bit triads
- test_geometric_quantum_correspondence (ThreeQubitBijection): 8 vertices = 8 basis states
- test_dimensional_uniqueness: 2(d+1) = 2^d only at d=3

**Parity and Tetrahedra:**
- test_geometric_quantum_correspondence (ParityEqualsParityObservable): parity = quantum observable eigenspaces
- test_hamming_distance_tetrahedra: uniform H=2 within each parity class
- test_historical_tetrahedral_regularity: both tetrahedra are regular
- test_historical_intra_tetrahedral_hamming: parity forces H=2

**Complementary Pairs:**
- test_complementary_pairs: all 4 pairs cross chambers, pass through origin
- test_complement_crosses_tetrahedra: XOR with 7 always flips parity
- test_complement_pairs_cross_tetrahedra: all pairs span both chambers
- test_body_diagonal_convergence: all diagonals intersect at (0,0,0)

**Face Structure and 3+1:**
- test_face_structure_3plus1: 6 spatial + 2 TIME = 3+1 per tetrahedron
- test_face_classification: TIME faces opposite V0 and V7
- test_historical_time_face_classification: extremal popcount identifies TIME faces

**Field Origin Geometry:**
- test_field_origin_geometry: centroid, equidistance, vector cancellation
- test_field_origin_equidistance: all vertices at sqrt(3) from origin
- test_origin_centrality: body diagonals, graph eccentricity, symmetry

**Quantum Correspondences:**
- test_geometric_quantum_correspondence (GHZState): |000>+|111> = body diagonal
- test_geometric_quantum_correspondence (WState): |001>+|010>+|100> = TIME face triangle
- test_geometric_quantum_correspondence (PauliAsReflections): bit flip = coordinate reflection

---

## Appendix B: Source File Index

**Physics Paper workspace (c:\Code\Physics Paper):**
- Research/field closure/IChing_Field_Closure_Encoding.md
- Research/IChing_G_Constant_Connection.md
- Research/field closure/Understanding_Pi_Field_Closure.md
- Research/field closure/Field_Closure_Encoding.md
- Research/field closure/Field_Closure_Complete_Read_Sequence_Proof.md
- Published/Paper VII/v7/md plans/Internal_Reference_IChing.md
- Published/Paper VI/dfp_gravity_field_dynamics_visual.html
- Published/Finding Pi/iching_trigram_triforce_validation.py
- Published/Paper VI/Other/investigate_iching_3_connection.py
- Textbook/Gravity_Field_Dynamics_Textbook.md (Chapter 12)

**field-dynamics workspace (c:\Code\field-dynamics):**
- dfp-gravity-field-model/gravity_field_model/common/geometry_constants.py
- historical_systems/field_origin_geometry/test_geometric_quantum_correspondence.py
- historical_systems/field_origin_geometry/test_field_origin_geometry.py
- historical_systems/field_origin_geometry/test_advanced_field_origin.py
- historical_systems/field_origin_geometry/test_origin_centrality.py
- dfp-gravity-field-model/gravity_field_model/engine_core/geometry/test_binary_triad.py
- dfp-gravity-field-model/gravity_field_model/engine_core/geometry/test_complementary_pairs.py
- dfp-gravity-field-model/gravity_field_model/engine_core/geometry/test_hamming_distance_tetrahedra.py
- dfp-gravity-field-model/gravity_field_model/engine_core/geometry/test_face_structure_3plus1.py
- dfp-gravity-field-model/gravity_field_model/engine_core/geometry/test_dimensional_uniqueness.py
