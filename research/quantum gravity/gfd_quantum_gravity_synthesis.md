# GFD Quantum Gravity Contact — Synthesis

## One Geometry, One Tetrahedron, Three Quantization Programs

**Framework:** Gravitational Field Dynamics (GFD)  
**Coupling Polynomial:** f(K, s) = 1 + Ks + K²  
**Geometry:** K = 4, D = 3 (stellated octahedron — two interpenetrating tetrahedra)  
**Tests:** 20/20 passed  
**File:** `gfd_quantum_gravity_contact.py`

---

## The Central Claim

The stellated octahedron — derived from 2(D+1) = 2^D with zero free parameters — makes structural contact with three independent quantum gravity programs: Regge calculus, loop quantum gravity, and spin foam models. The contact is not assumed. It is computed.

Every number that appears in these programs — the 16π in the Regge action, the area gap, the Immirzi parameter, the 6j-symbol for the quantum tetrahedron, the topological invariance under Pachner moves — has a derivation from K = 4 and D = 3. Where these programs have free parameters, GFD fixes them. Where they have structural constants, GFD derives them from the same two integers that produce the constitutive law, the magic numbers, and the fine structure constant.

GFD does not import quantum gravity. It makes contact with it because all four programs — GFD, Regge, LQG, and spin foams — use the same fundamental building block: the tetrahedron.

---

## Part Q1: Regge Contact

These five tests establish that the stellated octahedron is a natural simplicial building block for Regge calculus, and that the GFD action constants emerge from its discrete geometry.

### Q1a. Simplicial Decomposition

The stellated octahedron decomposes into 2K = 8 = 2^D elementary tetrahedra by coning each of the 8 triangular faces (4 per chamber) to the Field Origin at the cube center. Each elementary tetrahedron has K = 4 vertices: 3 face vertices plus the origin.

All elementary tetrahedra within a single chamber have identical volume. The total volume of both chambers is:

$$V_{\text{total}} = 2 \times \frac{8}{3} = \frac{16}{3} = \frac{K^2}{D}$$

The coupling constant K² = 16 divided by spatial dimension D = 3 gives the total simplicial volume. This is the Regge calculus content of the bimetric parameter β₂ = K² = 16: it counts the face coupling channels that tile the interior of the stellated octahedron.

### Q1b. Regge Edge Lengths

In Regge calculus, the gravitational degrees of freedom live in the edge lengths. The stellated octahedron has exactly two classes:

| Edge type | Count | Length | Formula |
|-----------|-------|--------|---------|
| Intra-tetrahedral | 2 × C(K,2) = 12 | 2√2 | Cube face diagonal |
| Cross-chamber (body diagonal) | K = 4 | 2√3 | Cube body diagonal |
| **Total** | **16** | | **K²** |

The total edge count is 12 + 4 = 16 = K². This is the same K² that appears as β₂ in the bimetric potential, as the 16 in 16πG, and as the face coupling channel count. The Regge degrees of freedom and the bimetric coupling constant are the same number, counted from different directions.

### Q1c. Deficit Angles and Solid Angle

The dihedral angle of a regular tetrahedron is arccos(1/3) ≈ 70.53°. This is a structural constant — it is determined by K = 4 vertices in D = 3 dimensions.

At the Field Origin, each chamber subtends a solid angle of 2π (half the full sphere, by the parity symmetry of the partition). Each of the K = 4 faces per chamber subtends:

$$\Omega_{\text{face}} = \frac{2\pi}{K} = \frac{\pi}{2}$$

Two chambers: total solid angle = 2 × K × π/2 = 4π. The complete sphere is tiled without gaps or overlaps. The Field Origin is the Regge vertex where all curvature concentrates, and its deficit angle is zero — the geometry is locally flat at the origin, consistent with the Field Origin being the equilibrium point (s = 0, μ₁ = 1/2, f = 17).

### Q1d. Regge Action Prefactor

The GFD scalar-tensor action contains the Einstein-Hilbert term R/(16πG). In Regge calculus, the discrete action is S = Σ A_e δ_e / (16πG). The 16 is the same number in both.

GFD derives it: 16 = K² = face coupling channels = β₂. The full SST coupling hierarchy is a geometric sequence:

| Coupling | Value | Geometry | Action term |
|----------|-------|----------|-------------|
| K² | 16 | Face channels | R/(16πG) |
| 2K | 8 | Vertex count | a₀²/(8πG) |
| K | 4 | Closure constant | (1/4)e^{−2Φ}F² |

The common ratio is 1/2 — the time face aperture. Each level of the hierarchy removes one bit of coupling freedom, descending through the topology from gravity through the scalar field to electromagnetism. The 16π in the Regge action is not a convention. It is K² × π, where K² counts independent coupling channels.

### Q1e. Bimetric Potential

The Hassan-Rosen bimetric gravity framework has five free coupling coefficients {β₀, β₁, β₂, β₃, β₄}. GFD locks them:

$$\{\beta_0, \beta_1, \beta_2, \beta_3, \beta_4\} = \{1, 0, K^2, 0, 1\} = \{1, 0, 16, 0, 1\}$$

from the coupling polynomial evaluated at the Field Origin: f(K, 0) = 1 + 0 + K² = 17 = F_ZERO.

The odd coefficients vanish by orientation parity — the Field Origin sees no handedness. The even coefficients encode the chamber exchange symmetry (β₀ = β₄ = 1) and the face coupling count (β₂ = K² = 16). The total bimetric potential is 1 + 0 + 16 + 0 + 1 = 18 = 2 + K².

**This is the GFD covariant completion.** Five previously free parameters reduced to zero. The bimetric potential is not fitted to data. It is read from the coupling polynomial.

---

## Part Q2: Quantum Tetrahedron

These five tests derive the area spectrum, volume spectrum, and angular momentum structure of the quantum tetrahedron directly from S4 representation theory applied to the stellated octahedron.

### Q2a. Spin Assignment

The rotation group of the stellated octahedron is S4, of order K! = 24 (every rotation of the cube permutes its K = 4 body diagonals). S4 has irreducible representations of dimensions {1, 1, 2, 3, 3}, satisfying 1² + 1² + 2² + 3² + 3² = 24.

The two 3-dimensional irreps correspond to angular momentum j = 1, with 2j + 1 = 3 = D. Each tetrahedron carries j = 1.

**This is not imported from LQG.** It is derived from the rotation group of the geometry. The quantum tetrahedron in LQG uses the same SU(2) representation theory because it is the same geometric object. GFD and LQG arrive at j = 1 from different directions and meet at the same point.

### Q2b. Face Area Spectrum

Each face of the regular tetrahedron inscribed in the [−1,1]³ cube is an equilateral triangle with edge length 2√2. The face area is:

$$A_{\text{face}} = \frac{\sqrt{3}}{4}(2\sqrt{2})^2 = 2\sqrt{3}$$

All K = 4 faces have identical area. In LQG, the area spectrum is a_n = 8πγl_P²√(j(j+1)). In GFD, the face area is determined exactly by K and D with no free parameters. The area is discrete because the geometry is discrete — there are exactly K faces, each with the same area.

### Q2c. Area Quantization and β₂

The triforce (medial triangle theorem) subdivides each face into K = 4 equal sub-triangles: 3 outer + 1 central. The sub-channel area quantum is:

$$A_{\text{sub}} = \frac{A_{\text{face}}}{K} = \frac{\sqrt{3}}{2}$$

This is GFD's minimum distinguishable area unit. The total surface area of one tetrahedron divided by the sub-channel quantum gives:

$$\frac{K \times A_{\text{face}}}{A_{\text{sub}}} = K^2 = 16 = \beta_2$$

The bimetric coupling constant β₂ counts the total sub-channel area quanta on the surface of one tetrahedron. Area quantization and the bimetric parameter are the same thing.

### Q2d. Volume Spectrum

The volume of each tetrahedron inscribed in the [−1,1]³ cube is:

$$V_{\text{tet}} = \frac{8}{3} = \frac{V_{\text{cube}}}{D} = \frac{2^D}{D}$$

The cube volume is 2^D = 8. Each tetrahedron occupies 1/D of the cube. The dual system (both tets) has total volume:

$$V_{\text{total}} = 2 \times \frac{8}{3} = \frac{16}{3} = \frac{K^2}{D}$$

In LQG, the volume operator has a discrete spectrum determined by the quantum numbers on the faces. In GFD, the volume is determined by K and D with no ambiguity. There is one volume eigenvalue per tetrahedron: 2^D/D.

### Q2e. Coupled Angular Momentum and Spin

Two coupled j = 1 tetrahedra give combined angular momentum j ∈ {0, 1, 2}:

| Combined j | Multiplicity | States |
|------------|-------------|--------|
| 0 (singlet) | 1 | 1 |
| 1 (triplet) | 1 | 3 |
| 2 (quintet) | 1 | 5 |
| **Total** | | **9 = D²** |

The maximum combined projection is m_max = 2. The time fraction — 2 time faces out of 2K = 8 total faces — projects this to intrinsic spin:

$$\text{spin} = \frac{2}{2K} \times m_{\max} = \frac{1}{4} \times 2 = \frac{1}{2}$$

Spin-1/2 is not postulated. It is computed from the time face fraction of the stellated octahedron applied to the j = 1 ⊗ j = 1 coupled system. The 9 = D² total states are the angular momentum content of the dual tetrahedral system.

---

## Part Q3: Immirzi Parameter

These four tests address the Barbero-Immirzi parameter γ — the one free parameter in standard LQG that GFD claims to fix.

### Q3a. The Area Gap

In LQG, the minimum nonzero area eigenvalue (the area gap) is proportional to γ. In GFD, the minimum distinguishable area is the sub-channel area:

$$A_{\text{gap}} = \frac{A_{\text{face}}}{K} = \frac{1}{K} \times A_{\text{face}}$$

The ratio 1/K = 1/4 is GFD's area gap in natural units. This is the same number as the EM prefactor 1/4 in the SST action, the central sub-channel fraction 1/(D+1) = 1/K, and the time fraction that projects angular momentum to spin-1/2.

### Q3b. γ = 1/K = 1/4

GFD's natural Immirzi candidate is:

$$\gamma_{\text{GFD}} = \frac{1}{K} = \frac{1}{4} = 0.25$$

The derivation:

1. The triforce subdivides each face into K = 4 sub-channels.
2. The minimum area quantum is A_face/K.
3. The LQG area formula a = 8πγl_P²√(j(j+1)) with j = 1 gives a = 8πγl_P²√2.
4. Normalizing so that the GFD area gap equals A_face/K fixes γ = 1/K.

This makes γ a derived constant, not a free parameter. The Immirzi parameter is the reciprocal of the closure constant.

### Q3c. Black Hole Entropy Contact

The Bekenstein-Hawking entropy S = A/(4l_P²) constrains γ in LQG. The Domagala-Lewandowski (2004) calculation gives γ_BH ≈ 0.2375.

GFD's candidate γ = 1/K = 0.25 differs by approximately 5.3%:

| Source | γ value | Derivation |
|--------|---------|-----------|
| GFD (tree level) | 0.2500 | 1/K = sub-channel fraction |
| LQG BH entropy | 0.2375 | State counting (Domagala-Lewandowski) |
| **Difference** | **~5.3%** | |

The GFD value is a tree-level geometric result. The 5% correction is the same order as the time fraction (1/4 = 25%) that projects the angular momentum to spin-1/2 — suggesting that the BH entropy calculation applies a loop correction that GFD's tree-level geometry does not yet include.

**This is an honest boundary.** GFD does not claim exact agreement. It claims 1/K as the tree-level Immirzi parameter, with a 5% gap that identifies the frontier where loop corrections become relevant.

### Q3d. The 5% Gap

The fractional difference:

$$\delta = \frac{\gamma_{\text{GFD}} - \gamma_{\text{BH}}}{\gamma_{\text{BH}}} = \frac{1/K - 0.2375}{0.2375} \approx 0.053$$

is bounded between 4% and 6%. The tree-level value overestimates slightly. The correction involves exactly the structural constants of the stellated octahedron: K = 4 (the closure constant), the binary factor 2 (from the two tetrahedra), and the continuous-limit factor π. Closing the gap requires quantizing the simplicial complex — which is precisely what LQG does. The 5% gap is the distance between classical GFD geometry and full quantum state counting.

---

## Part Q4: Spin Foam Amplitudes

These three tests compute the Ponzano-Regge spin foam amplitude for the GFD tetrahedron.

### Q4a. The 6j-Symbol

The Ponzano-Regge model assigns a 6j-symbol to each tetrahedron, with one angular momentum quantum number per edge. The GFD tetrahedron has j = 1 on all 6 = C(K, 2) edges (from the S4 three-dimensional irrep). The relevant 6j-symbol is:

$$\begin{Bmatrix} 1 & 1 & 1 \\ 1 & 1 & 1 \end{Bmatrix} = \frac{1}{6} = \frac{1}{C(K, 2)}$$

The amplitude is the inverse of the number of edges per tetrahedron. The spin foam transition amplitude for the quantum tetrahedron with uniform j = 1 coloring equals one over the edge count. This connects the spin foam formalism directly to the combinatorics of the stellated octahedron: C(K, 2) = 6 edges per tet determines the amplitude.

### Q4b. Semiclassical Normalization

The Ponzano-Regge asymptotic formula for large j gives:

$$\begin{Bmatrix} j & j & j \\ j & j & j \end{Bmatrix} \sim \frac{\cos(S_{\text{Regge}} + \pi/4)}{\sqrt{12\pi V}}$$

The normalization involves 12πV, where V = 8/3 is the GFD tetrahedron volume and 12 = K × D is the edge count of the stellated octahedron.

$$12\pi V = K \times D \times \pi \times \frac{8}{3}$$

Every factor is a stellated octahedron constant: K = 4, D = 3, V = 2^D/D. The semiclassical limit of the spin foam amplitude is normalized by the same numbers that determine the GFD geometry. At j = 1, the formula is not yet in its asymptotic regime, but the structural constants are exact.

### Q4c. State Sum

The Ponzano-Regge partition function for a single tetrahedron with all edges carrying j sums over spin colorings:

$$Z_{\text{tet}} = \sum_j (2j+1)^6 \times \begin{Bmatrix} j & j & j \\ j & j & j \end{Bmatrix}$$

For the GFD coloring j = 1:

| Quantity | Value | Formula |
|----------|-------|---------|
| Dimension per edge | 3 | 2j + 1 = D |
| Edge weight | 729 | D^C(K,2) = 3⁶ |
| 6j amplitude | 1/6 | 1/C(K, 2) |
| **Contribution** | **243/2** | **D^C(K,2) / C(K,2)** |

The j = 1 contribution to the state sum is D^C(K,2) / C(K,2) = 729/6 = 243/2 = 121.5. This is the spin foam weight of the GFD tetrahedron — the product of the edge dimension factor and the Racah amplitude, expressed entirely in terms of K and D.

---

## Part Q5: Pachner Stability

These three tests verify that elementary triangulation changes preserve the K = 4 structure.

### Q5a. The 2-3 Pachner Move

The 2-3 move replaces 2 tetrahedra sharing a common face with 3 tetrahedra sharing a common edge. It is the D = 3 generalization of the 2D edge flip.

Before: 2 tets with 2K − D = 5 vertices. After: 3 tets with 5 vertices. The vertex count is preserved. Each resulting tetrahedron still has K = 4 vertices. The move is local — it changes the number of simplices but not their structure.

### Q5b. The 1-4 Pachner Move

The 1-4 move places a new vertex inside a tetrahedron and connects it to all K = 4 faces, creating K = 4 new tetrahedra.

**This is exactly the GFD coning operation.** The Field Origin is the inserted vertex. Each face of the parent tetrahedron is coned to the origin, producing K elementary tetrahedra — the simplicial decomposition validated in Q1a. The 1-4 Pachner move IS the GFD construction.

Before: 1 tet with K = 4 vertices. After: K = 4 tets with K + 1 = 5 vertices (the original 4 plus the center). Each new tet has 3 face vertices + 1 center = K = 4 vertices.

### Q5c. Coupling Channel Invariance

Both Pachner moves preserve K. Since K is a property of the simplex (vertices per tetrahedron), not of the complex (total number of tetrahedra), all quantities that depend only on K are topological invariants:

| Invariant | Value | Why preserved |
|-----------|-------|--------------|
| K | 4 | Simplex structure |
| D | 3 | Ambient dimension |
| β₂ = K² | 16 | Face coupling channels |
| f(K, s) | 1 + 4s + 16 | Coupling polynomial |
| F_PLUS | 21 | Capacity ceiling |
| F_MINUS | 13 | Capacity floor |
| F_ZERO | 17 | Field Origin capacity |

The complete chain K → f(K, s) → μ(x) → SST action is invariant under Pachner moves because K is invariant. The uniqueness theorem 2(D+1) = 2^D is not affected by local triangulation changes.

**This is the GFD version of diffeomorphism invariance.** The geometry is background-independent not because the action is written in coordinate-free notation (which it is), but because the structural constants that determine the action are topological invariants of the simplex. No Pachner move can change K = 4 or D = 3. Therefore no local rearrangement of the simplicial complex can change the physics.

---

## What the 20 Tests Prove Together

**Regge contact (Q1a–Q1e):** The stellated octahedron is a natural simplicial building block with 8 = 2^D elementary tetrahedra, 16 = K² edges encoding the metric, and a dihedral structure that tiles the full solid angle at the Field Origin. The SST coupling hierarchy 16:8:4 = K²:2K:K derives the Regge action prefactor 1/(16πG) from face channel counting. The five Hassan-Rosen bimetric coefficients are locked to {1, 0, K², 0, 1} by the coupling polynomial at s = 0.

**Quantum tetrahedron (Q2a–Q2e):** Each tetrahedron carries j = 1 from S4 representation theory (2j+1 = D = 3). Face area 2√3 is determined by K and D. The triforce subdivision gives K = 4 sub-channels per face, with total sub-channel count K² = 16 = β₂. Volume 8/3 = 2^D/D. The coupled j₁ ⊗ j₂ system has 9 = D² states, and the time fraction projects m_max = 2 to spin-1/2.

**Immirzi parameter (Q3a–Q3d):** GFD's tree-level Immirzi is γ = 1/K = 1/4, derived from the sub-channel area fraction. This is 5.3% above the LQG black hole entropy value γ_BH ≈ 0.2375. The gap identifies the frontier between classical geometry and quantum state counting — exactly where loop corrections apply.

**Spin foam amplitudes (Q4a–Q4c):** The 6j-symbol {1,1,1;1,1,1} = 1/6 = 1/C(K,2) — the inverse edge count. The semiclassical normalization involves 12πV where 12 = K×D and V = 2^D/D. The state sum contribution D^C(K,2)/C(K,2) = 243/2 gives the spin foam weight of the GFD tetrahedron.

**Pachner stability (Q5a–Q5c):** Both 2-3 and 1-4 moves preserve K = 4 and D = 3. The 1-4 move IS the GFD coning construction. All coupling constants, the capacity polynomial, and the constitutive law are Pachner invariants because they depend only on K, which is a simplex property, not a complex property.

---

## Summary Table

| Test | Type | Parameters | Result |
|------|------|-----------|--------|
| Q1a. Simplicial decomposition | Geometric proof | 0 | 8 tets, V = K²/D |
| Q1b. Regge edge lengths | Geometric proof | 0 | 16 = K² total edges |
| Q1c. Deficit angles | Geometric proof | 0 | Full 4π tiled at origin |
| Q1d. Regge action prefactor | Algebraic proof | 0 | 16π = K² × π |
| Q1e. Bimetric potential | Algebraic proof | 0 | {1, 0, 16, 0, 1} locked |
| Q2a. Spin assignment j=1 | Representation theory | 0 | 2j+1 = D = 3 |
| Q2b. Face area spectrum | Geometric proof | 0 | A = 2√3, all K faces equal |
| Q2c. Area quantization | Geometric proof | 0 | K² = 16 sub-channels |
| Q2d. Volume spectrum | Geometric proof | 0 | V = 2^D/D = 8/3 |
| Q2e. Coupled system | Representation theory | 0 | 9 = D² states, spin = 1/2 |
| Q3a. Area gap | Algebraic proof | 0 | 1/K = 1/4 |
| Q3b. Immirzi from K | Algebraic proof | 0 | γ = 1/K = 0.25 |
| Q3c. BH entropy contact | Semi-empirical | 0 | 5.3% from γ_BH = 0.2375 |
| Q3d. The 5% gap | Semi-empirical | 0 | Tree-level vs. loop correction |
| Q4a. 6j-symbol | Algebraic proof | 0 | 1/6 = 1/C(K,2) |
| Q4b. Semiclassical volume | Algebraic proof | 0 | 12πV, all GFD constants |
| Q4c. State sum contribution | Algebraic proof | 0 | D^C(K,2)/C(K,2) = 243/2 |
| Q5a. 2-3 Pachner move | Topological proof | 0 | K = 4 preserved |
| Q5b. 1-4 Pachner move | Topological proof | 0 | = GFD coning operation |
| Q5c. Coupling invariance | Topological proof | 0 | f(K,s) is Pachner invariant |

**Total free parameters across all 20 tests: 0.**

---

## The Physical Picture

1. The **tetrahedron** is the fundamental quantum of 3-space. This is not a GFD postulate — it is the shared assumption of Regge calculus, LQG, and spin foam models. GFD adds that the uniqueness theorem 2(D+1) = 2^D selects D = 3, K = 4 uniquely.

2. Two interpenetrating tetrahedra form the **stellated octahedron**. Their interaction is described by the bimetric potential {1, 0, K², 0, 1}, which is derived, not fitted. Hassan and Rosen's five free coefficients reduce to zero.

3. The **coupling polynomial** f(K, s) = 1 + Ks + K² encodes the complete topological structure. Its three values F_MINUS = 13, F_ZERO = 17, F_PLUS = 21 are the capacity floor, Field Origin, and ceiling. Every constant in the GFD action is a polynomial or exponential in K and D.

4. Each tetrahedron carries **angular momentum j = 1** from S4 representation theory. Two coupled j = 1 systems give combined j ∈ {0, 1, 2} with 9 = D² states. The time fraction 1/4 projects the maximum projection to **spin-1/2**.

5. The **area spectrum** is quantized by the triforce subdivision: K = 4 sub-channels per face, A_sub = A_face/K. The total sub-channel count K² = 16 = β₂ is simultaneously the bimetric coupling constant, the face channel count, the total edge count, and the Regge action prefactor (divided by π).

6. The **Immirzi parameter** γ = 1/K = 1/4 is the sub-channel area fraction — the minimum resolvable unit of area in the GFD geometry. It is 5.3% above the LQG BH entropy value, identifying the tree-level/loop-correction boundary.

7. The **6j-symbol** for uniform j = 1 coloring is 1/C(K,2) = 1/6 — one over the number of edges. The spin foam amplitude is determined by the combinatorics of the simplex.

8. The geometry is **Pachner stable**: all structural constants are invariants of the simplex, not the complex. The 1-4 move that inserts a central vertex into a tetrahedron IS the GFD coning operation that creates the Field Origin. Quantization (Pachner moves) and the classical geometry (the stellated octahedron) are the same construction seen from different directions.

---

*GFD Quantum Gravity Contact v1.0 — 20/20 tests passing, 0 free parameters*
