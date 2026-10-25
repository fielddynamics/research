# Supplementary Note: From 24 = D × 2K to Vortical Closure

*S. Nelson · Field Dynamics Research · March 2026*

---

## Starting Point

The companion letter [2] proved the following results, which are used here without re-derivation:

**From [2], Section 5, Theorem.** The 24 torsion components of the K = 4 tetrad connection admit the factorisation 24 = D × 2K = 3 × 8. This factorisation holds exclusively at K = 4.

**From [2], Supplementary Note.** The torsion sector is the necessary carrier of the TetA/TetB distinction. The exchange-symmetric partition is μ(x) = x/(x+1) for TetA and 1/(x+1) for TetB.

**From [1].** The closed tetrad frame Tet_A ∪ Tet_B forms the stellated octahedron with 2K = 8 vertices. K = 4 is forced by the uniqueness equation 2(D+1) = 2^D.

This note identifies the two factors in 24 = D × 2K with specific geometric objects of the closed frame, and proves that their interaction is vortical.

---

## Identification of the Two Factors

### The factor 2K = 8: the null directions of the closed frame

The stellated octahedron [1] has 2K = 8 vertices. In Cartesian coordinates, these are (±1/√3, ±1/√3, ±1/√3) — the 8 vertices of the cube dual to the octahedral core. The 4 odd-popcount vertices {1, 2, 4, 7} belong to Tet_A; the 4 even-popcount vertices {0, 3, 5, 6} belong to Tet_B.

Each vertex lies on the celestial sphere S² and defines a null direction of the frame. The factor 2K in the torsion factorisation is therefore the count of null directions of the closed frame: 4 from Tet_A + 4 from Tet_B = 8.

### The factor D = 3: transverse rotation planes per null direction

The cube has 4 body diagonals (antipodal pairs). Each vertex belongs to exactly 1 diagonal. Each vertex is therefore transverse to the other 3 diagonals. Three transverse axes = 3 independent rotation planes, one per spatial dimension.

The factor D in the torsion factorisation is the count of transverse rotation planes per null direction.

### The factorisation

Each torsion component corresponds to one (null direction, rotation plane) pair. There are 8 null directions and 3 rotation planes per direction:

```
24 = 8 null directions × 3 rotation planes = 2K × D
```

This is the factorisation proven algebraically in [2], now identified geometrically with the closed-frame structure of [1].

> **Note.** Letter [2] proved the factorisation as an algebraic identity of K. This note does not re-prove it. It identifies what the factors refer to in the geometry of the closed frame.

---

## The Chirality Split

### Orientation of the two sub-frames

Tet_A and Tet_B are dual tetrahedra: identical vertex geometry, opposite face-normal orientations [1]. At the connection level, [2] proved that Tet_A is the identity component and Tet_B is the parity component under P: e^i → −e^i.

For each null direction, the 3 torsion components form a spatial rotation vector obtained by dualising the antisymmetric pair:

```
τ^I_a = (1/2) ε_abc T^I_bc
```

Under the orientation reversal that exchanges Tet_A and Tet_B, the Levi-Civita symbol flips sign: ε^B = −ε^A. Therefore:

```
τ (Tet_B) = −τ (Tet_A)
```

The 4 Tet_A null directions carry rotation vectors with chirality (+).
The 4 Tet_B null directions carry rotation vectors with chirality (−).

This is the parity distinction of [2], now resolved to the level of individual torsion components: opposite parity means opposite chirality.

---

## The Holonomy Computation

### The question

The 8 null directions form a bipartite graph: every cube edge connects a Tet_A vertex to a Tet_B vertex. A closed transport path through all 8 directions alternates between sub-frames: A → B → A → B → A → B → A → B.

At each step, the frame rotates by angle θ = arccos(1/3) ≈ 70.53° (the angular separation between adjacent cube vertices on S²). The chirality of the source vertex determines the sign: +θ from Tet_A, −θ from Tet_B.

Question: does the total rotation cancel after one complete cycle through all 8?

### The answer

This is a finite computation. There are exactly 12 Hamiltonian cycles on the cube graph. Each can be evaluated by composing 8 rotation matrices via Rodrigues' formula.

**Without chirality (uniform +θ at every step):**
All 12 cycles give identity holonomy. The cube's octahedral symmetry enforces exact cancellation.

**With chirality (+θ from Tet_A, −θ from Tet_B):**
No cycle gives identity. 6 cycles give net rotation 135° (= 3π/4). 6 cycles give net rotation 155.8° (≈ 7π/8).

The chirality distinction — the parity-resolved content that [2] proved is carried by torsion — breaks the exact cancellation that the directional scaffold alone would enforce.

### Explicit example

Cycle: v₁(A) → v₆(B) → v₃(A) → v₅(B) → v₄(A) → v₇(B) → v₂(A) → v₈(B) → v₁(A)

```
Step 1: v₁(A) → v₆(B):  +θ about (0, −0.707, +0.707)
Step 2: v₆(B) → v₃(A):  −θ about (−0.707, −0.707, 0)
Step 3: v₃(A) → v₅(B):  +θ about (−0.707, 0, +0.707)
Step 4: v₅(B) → v₄(A):  −θ about (0, +0.707, +0.707)
Step 5: v₄(A) → v₇(B):  +θ about (+0.707, 0, +0.707)
Step 6: v₇(B) → v₂(A):  −θ about (0, −0.707, +0.707)
Step 7: v₂(A) → v₈(B):  +θ about (+0.707, +0.707, 0)
Step 8: v₈(B) → v₁(A):  −θ about (0, +0.707, −0.707)
```

Uniform composition (all +θ): net rotation = 0°. Identity.
Chiral composition (alternating ±θ): net rotation = 135°.

The sign alternation — which is the physical content of the Tet_A/Tet_B parity distinction — breaks the cancellation completely. The positive and negative rotations act about different axes (each axis depends on both endpoints). Reversing the sign at alternating steps does not invert those steps; it produces a qualitatively different composition.

> **Note.** The computation is reproducible in approximately 40 lines of Python using NumPy and Rodrigues' formula. All 12 cycles have been verified for both uniform and chiral transport. The code is available as supplementary material.

---

## Why a Vortex

### The winding is helical

The holonomy per cycle is a rotation by a fixed angle Θ ≠ 0 about a fixed axis. The path passes through the field origin O at every Tet_A ↔ Tet_B transition. A path that advances through a common point while rotating by a constant angle per cycle is helical.

### The helix has a plane

The rotation axis of the holonomy defines a preferred direction. The field closure is therefore not spherically symmetric — it is planar, perpendicular to the holonomy axis. This is why the vortex forms a disk, not a sphere.

> **Note.** Cold dark matter models predict spherical halos because structureless mass has no preferred direction. The closed tetrad frame predicts disk geometry because the chiral holonomy has an axis. Observed galaxies are disks. This is a qualitative prediction that distinguishes the two frameworks.

### The constitutive law is the vortex profile

Letter [2] derived μ(x) = x/(x+1) from the exchange symmetry of the closed frame, independently of the present vortex result. That same partition, when plotted radially and revolved about the holonomy axis, produces the spatial profile of the vortex:

- Inner throat (x >> 1): μ → 1, Christoffel-dominated, the galactic core.
- Outer disk (x << 1): μ → 0, torsion-dominated, what standard cosmology calls dark matter.
- Transition ring (x = 1): μ = 1/2, the MOND crossover.

The constitutive law and the vortex are the same object viewed from two sides. The exchange symmetry determines the algebraic partition. The chiral holonomy determines the spatial geometry. Together they give the complete gravitational field.

---

## Summary

| Result | Source | What it establishes |
|--------|--------|-------------------|
| 24 = D × 2K at K = 4 | Letter [2], Theorem | Algebraic factorisation |
| 2K = 8 null directions | This note | Geometric identification |
| D = 3 transverse planes | This note | Geometric identification |
| Chirality ± from parity | This note + [2] | Torsion sign from frame orientation |
| Uniform transport → identity | This note (computation) | The scaffold alone is inert |
| Chiral transport → 135° | This note (computation) | The parity distinction generates winding |
| Winding + axis → disk | This note | Vortex, not sphere |

The 24 torsion components that Letter [2] identified as the carrier of TetB organise into 8 null directions × 3 rotation planes. Their parity-resolved chirality breaks the exact holonomy cancellation of the directional scaffold, forcing the field to close as a vortex. The constitutive law μ(x) = x/(x+1), already derived in [2], is the radial profile of this vortex.

---

## References

[1] S. Nelson, "The Coordinate-Space Geometry of the Tetrad Frame," submitted to Class. Quantum Grav. (CQG-115428), 2025.

[2] S. Nelson, "The Other Half of Gravity: Torsion and the Two-Chamber Structure of the Tetrad Frame," submitted to Class. Quantum Grav. (CQG-115447), 2025.

---

*Field Dynamics Research · docs.fielddynamics.org*
*Attribution: Stephen Nelson · CC BY 4.0*
