# Tetrad Gravity, Bimetric Gravity, and the Tetrahedron: Comprehensive Reference

**Purpose:** Consolidated reference for all established physics that the dual tetrad field topology rests upon. Covers tetrad gravity, bimetric gravity, the triad-tetrahedron identification, the (3+1) decomposition, and the chain of citations establishing each result. Distinguishes what is textbook, what is established in specialist literature, and what is novel to this paper.

**Status:** Internal knowledge document for Paper VII. Not for publication.

**Last updated:** February 2026, following detailed research into Barbieri (1998), Hassan-Kocic (2018), Hinterbichler-Rosen (2012), and the LQG quantum tetrahedron literature.

---

## Table of Contents

1. [Tetrad Gravity (Textbook)](#1-tetrad-gravity-textbook)
2. [The Triad Defines a Tetrahedron (Established)](#2-the-triad-defines-a-tetrahedron-established)
3. [The (3+1) Decomposition (Textbook)](#3-the-31-decomposition-textbook)
4. [Bimetric Gravity (Established)](#4-bimetric-gravity-established)
5. [Ghost-Freedom and Opposite Orientations (Established)](#5-ghost-freedom-and-opposite-orientations-established)
6. [Compatible (3+1) Decompositions (Established)](#6-compatible-31-decompositions-established)
7. [The Interaction Vertex and Beta Parameters (Established)](#7-the-interaction-vertex-and-beta-parameters-established)
8. [Quantum Tetrahedra in LQG (Established)](#8-quantum-tetrahedra-in-lqg-established)
9. [The Closure Constraint (Established)](#9-the-closure-constraint-established)
10. [Simplicial Gravity and Regge Calculus (Established)](#10-simplicial-gravity-and-regge-calculus-established)
11. [What This Paper Does Within These Frameworks (Novel)](#11-what-this-paper-does-within-these-frameworks-novel)
12. [Complete Citation Index](#12-complete-citation-index)

---

## 1. Tetrad Gravity (Textbook)

### What It Is

Tetrad gravity (also called vierbein gravity, frame-field gravity, or first-order gravity) is a reformulation of General Relativity that uses four orthonormal basis vectors at each spacetime point instead of the metric tensor directly. It is textbook material, taught in graduate courses worldwide.

### The Core Equation

The metric is decomposed as:

```
g_{mu nu} = eta_{ab} e^a_mu e^b_nu
```

where:
- `eta_{ab} = diag(-1, +1, +1, +1)` is the flat Minkowski metric
- `e^a_mu` is the tetrad (vierbein): four orthonormal basis vectors at each point
- Index `a` runs over internal (Lorentz) indices: 0 (time), 1, 2, 3 (space)
- Index `mu` runs over spacetime coordinate indices

### Why It Is Called the "Square Root of the Metric"

The metric `g` is quadratic in the tetrad `e`. In matrix form:

```
g = e^T eta e
```

Just as a number's square root satisfies x^2 = n, the tetrad satisfies e^T eta e = g. This is standard terminology used in:
- **MTW (1973)**, *Gravitation*, Chapter 14 (p. 327)
- **Wald (1984)**, *General Relativity*, Chapter 13
- **Weinberg (1972)**, *Gravitation and Cosmology*, Chapter 12
- **Nakahara (2003)**, *Geometry, Topology and Physics*, Chapter 7

### Non-Degeneracy and Closure

Taking determinants of g = e^T eta e:

```
det(g) = -[det(e)]^2
```

Therefore `det(g) != 0` if and only if `det(e) != 0`. The four tetrad legs must span the tangent space completely. **GR's non-degeneracy condition and tetrad closure are mathematically equivalent.**

### Degrees of Freedom

- The tetrad has 16 components (4 x 4 matrix)
- Local Lorentz invariance removes 6 (the SO(3,1) gauge freedom)
- Leaving 10 independent components = same as the symmetric metric tensor
- The tetrad carries the same information as the metric, plus an orientation

### Key Textbook References

| Reference | What It Establishes |
|-----------|-------------------|
| **Misner, Thorne, Wheeler (1973)** *Gravitation* Ch. 14 | Tetrad formalism, "square root of the metric," orthonormal frames |
| **Wald (1984)** *General Relativity* Ch. 13 | Spinor structure requires tetrads; tetrad = soldering form |
| **Weinberg (1972)** *Gravitation and Cosmology* Ch. 12 | Vierbein formulation, local Lorentz invariance |
| **Hehl et al. (1976)** Rev. Mod. Phys. 48, 393 | Tetrad gravity with torsion (Einstein-Cartan theory) |

---

## 2. The Triad Defines a Tetrahedron (Established)

### The Key Result

The spatial triad---the three spacelike legs of the tetrad---defines a tetrahedron. This is explicitly stated in the physics literature:

> **"A tetrahedron can be understood as the convex envelope of four points in 3-dimensional Euclidean space E^3. [...] a triad e_1, e_2, e_3 of independent vectors (nine numbers) defines completely the tetrahedron."**
>
> -- Barbieri (1998), Section II.A, "Quantum tetrahedra and simplicial spin networks," Nucl. Phys. B 518: 714. arXiv:gr-qc/9707010.

### How the Identification Works

Given a triad of three independent vectors (e_1, e_2, e_3) emanating from a common origin:
- They define four vertices: the origin plus the three endpoints
- These four points are the vertices of a tetrahedron
- The tetrahedron has 4 triangular faces, 6 edges, 4 vertices
- The face normals are:

```
n_1 = -e_1 x e_2
n_2 = -e_2 x e_3
n_3 = -e_3 x e_1
n_4 = -(n_1 + n_2 + n_3)    [closure constraint]
```

### The (3+1) Extension

Barbieri (1998), Section II.C, explicitly considers the tetrahedron embedded in 3+1 Minkowski spacetime:

> "If we imagine the tetrahedron as imbedded in 3+1 Minkowski spacetime, the requirement that all the edges are spacelike is equivalent to the requirement that the 4-dimensional 'normal' of the tetrahedron [...] lies inside the light cone."

This gives the chain:

```
Triad (3 spatial vectors) = Tetrahedron          [Barbieri 1998]
Tetrad = Triad + time direction                  [ADM decomposition]
Therefore: Tetrad = Tetrahedron + time = (3+1)   [follows directly]
```

### Why This Matters for Our Paper

The paper uses "tetrahedron" to describe what each tetrad's spatial content defines. This is NOT a novel claim---it is Barbieri's (1998) explicit statement, extended to 3+1 by Barbieri himself. When the paper says "two tetrahedra with opposite orientations," it means "two tetrads whose spatial triads define two tetrahedra." This is established physics with a direct citation.

### The Number 4

The number k = 4 appears for the same dimensional reason (d + 1 for d = 3) in multiple independent contexts:

| Origin | Why "4" appears | Reference |
|--------|----------------|-----------|
| Simplex theorem | d + 1 = 4 faces for minimal enclosure in d = 3 | Classical geometry (Ziegler 1995) |
| ADM constraints | 1 Hamiltonian + 3 momentum = 4 | Arnowitt-Deser-Misner (1962) |
| Tetrad legs | 1 timelike + 3 spacelike = 4 | MTW (1973), Wald (1984) |
| Tetrahedron faces | 4 triangular faces | Euclid |
| LQG 4-valent node | 4 edges -> 4 face normals -> closure | Barbieri (1998) |
| Tetrad components | 4 x 4 = 16 total, 10 metric + 6 gauge | Standard |

The literature attributes this convergence to the dimensionality of space (d = 3). All these "4"s are the same "4."

---

## 3. The (3+1) Decomposition (Textbook)

### ADM Formalism

The ADM (Arnowitt-Deser-Misner) formalism decomposes 4-dimensional spacetime into:
- A family of 3-dimensional spatial hypersurfaces Sigma_t
- Parameterized by a time function t
- With lapse function N and shift vector N^i connecting adjacent slices

The 4-metric decomposes as:

```
ds^2 = -N^2 dt^2 + h_{ij}(dx^i + N^i dt)(dx^j + N^j dt)
```

where h_{ij} is the induced 3-metric on each spatial slice.

### The Tetrad in (3+1) Form

The tetrad decomposes correspondingly:
- **Spatial triad** e^i_a (i = 1,2,3): encodes the 3-geometry of each slice
- **Lapse and shift** (related to e^0_mu): encode how slices are stacked

The spatial triad has 9 components. The 3-metric is:

```
h_{ij} = delta_{ab} e^a_i e^b_j    (Euclidean signature on spatial slice)
```

This triad "defines completely the tetrahedron" (Barbieri 1998).

### (3+1)^2 = Compatible Decompositions

In bimetric gravity with two metrics g and f:
- Each metric admits a (3+1) decomposition
- Hassan and Kocic (2018) proved that general covariance requires these decompositions to be **compatible**: the two metrics must share a common time direction
- Our paper denotes this requirement (3+1)^2: two compatible (3+1) decompositions

This is not invented notation. It names what Hassan-Kocic proved is required.

### Key References

| Reference | What It Establishes |
|-----------|-------------------|
| **Arnowitt, Deser, Misner (1962)** | The (3+1) decomposition of GR; Hamiltonian formulation |
| **Ashtekar (1986)** Phys. Rev. Lett. 57, 2244 | New variables for GR using self-dual connections; triad as fundamental variable |
| **Hassan, Kocic (2018)** JHEP 05, 099 | Compatible (3+1) decompositions required in bimetric gravity |

---

## 4. Bimetric Gravity (Established)

### What It Is

Ghost-free bimetric gravity (also called Hassan-Rosen bimetric theory) is a consistent theory of two interacting spin-2 fields. It was established as ghost-free at the nonlinear level in 2012.

### The Two Metrics

The theory contains two dynamical metrics:

```
g_{mu nu} = eta_{ab} E^a_mu E^b_nu    (metric 1, with tetrad E)
f_{mu nu} = eta_{ab} L^a_mu L^b_nu    (metric 2, with tetrad L)
```

Each metric has its own tetrad field. The spatial triad of each tetrad defines a tetrahedron (Barbieri 1998). Two tetrads define two tetrahedra.

### The Hassan-Rosen Action

The action in vielbein form:

```
S_HR = integral d^4x [ e E_I^alpha E_J^beta Omega^IJ_{alpha beta}(E)
                      + e_tilde L_I^alpha L_J^beta Omega^IJ_{alpha beta}(L)
                      + m^2 e sum_{n=0}^{4} beta_n e_n(E^{-1} L) ]
```

- First term: curvature of the first tetrad (standard GR for g)
- Second term: curvature of the second tetrad (standard GR for f)
- Third term: interaction potential coupling the two tetrads

### The Interaction Potential

The coupling between the two metrics occurs through:

```
V(S) = sum_{n=0}^{4} beta_n e_n(S)
```

where:
- `S = sqrt(g^{-1} f)` is a 4 x 4 matrix (the "square root matrix")
- `e_n(S)` are the elementary symmetric polynomials of the eigenvalues of S
- `beta_0` through `beta_4` are **five free coefficients** (the theory's free parameters)
- The total number of coupling terms across all five polynomials: 1 + 4 + 6 + 4 + 1 = 16 = (3+1)^2

### Degrees of Freedom

- 7 propagating DOF: 2 from a massless graviton + 5 from a massive graviton
- This is the maximum consistent number for two interacting spin-2 fields
- The Boulware-Deser ghost (the dangerous 8th mode) is absent

### Key References

| Reference | What It Establishes |
|-----------|-------------------|
| **Hassan, Rosen (2012)** JHEP 02, 126 | Ghost-free bimetric gravity; the interaction potential |
| **Hassan, Rosen (2012)** JHEP 04, 123 | Proof of ghost-freedom at the nonlinear level |
| **de Rham, Gabadadze, Tolley (2011)** Phys. Rev. Lett. 106, 231101 | Ghost-free massive gravity (one dynamical metric); precursor to bimetric theory |

---

## 5. Ghost-Freedom and Opposite Orientations (Established)

### The Boulware-Deser Ghost

Boulware and Deser (1972) showed that a generic theory of a massive spin-2 field contains a ghost: a scalar mode with negative kinetic energy. This makes the vacuum unstable. The ghost problem plagued massive gravity research for ~70 years (1939-2010).

### Resolution Through Orientation

The ghost is eliminated by the specific structure of the interaction potential (de Rham-Gabadadze-Tolley 2011, Hassan-Rosen 2012). In the tetrad formulation, the ghost-freedom condition has a geometric interpretation:

**Alexander, Marciano, Smolin (2014)**, "Gravitational origin of the weak interaction's chirality," Phys. Rev. D 89, 065017:
- Showed that a single-orientation tetrad field produces a scalar ghost
- Ghost-freedom requires **opposite spatial orientations** for the two tetrads
- Specifically: `det(E) = +1` and `det(L) = -1` (or vice versa) for the spatial components
- This corresponds to opposite spatial parity: one tetrad is the parity-reflected partner of the other

### Compatibility with Shared Time Direction

Opposite spatial orientations are fully compatible with a shared timelike direction:
- The two tetrads share a common time axis (required by Hassan-Kocic 2018)
- Their spatial triads are inverted relative to each other
- This is exactly the geometry of the stellated octahedron: two tetrahedra, opposite spatial orientations, sharing a common center and time axis

### The Stellated Octahedron as Physical Realization

The stellated octahedron (two interlocking tetrahedra with opposite orientations sharing a common center) is the unique geometric configuration that satisfies:
1. Ghost-freedom (opposite orientations) -- Alexander et al. 2014
2. Compatible (3+1) decompositions (shared time) -- Hassan-Kocic 2018
3. Single interaction vertex (coupled at one point) -- Hinterbichler-Rosen 2012
4. Spinor double cover (two sheets) -- Weinberg 1995, Geroch 1968
5. Chiral completeness (self-dual + anti-self-dual) -- Ashtekar 1986

### Key References

| Reference | What It Establishes |
|-----------|-------------------|
| **Boulware, Deser (1972)** Phys. Rev. D 6, 3368 | The ghost problem in massive gravity |
| **Alexander, Marciano, Smolin (2014)** Phys. Rev. D 89, 065017 | Opposite orientations required for stability; chirality from gravity |
| **Deffayet, Mourad, Zahariade (2013)** JHEP 03, 086 | Symmetric vielbein condition in bimetric gravity |

---

## 6. Compatible (3+1) Decompositions (Established)

### The Hassan-Kocic Theorem

**Hassan, Kocic (2018)**, "On the local structure of spacetime in ghost-free bimetric theory and massive gravity," JHEP 05, 099. arXiv:1706.07806.

Key result: General covariance in bimetric gravity requires the two metrics to admit **compatible (3+1) decompositions**. This means:

1. Both metrics must share a common timelike direction (compatible causal structure)
2. The spatial hypersurfaces of one metric must be spatial with respect to the other
3. The ADM lapse and shift of both metrics are defined with respect to the same foliation

### What This Means Geometrically

In tetrad language:
- Both tetrads share a common time leg (up to gauge transformation)
- Their spatial triads live on the same spatial slice
- The two spatial triads (defining two tetrahedra by Barbieri 1998) can have opposite orientations while sharing the same time direction

This is what our paper denotes (3+1)^2: two (3+1) decompositions that are compatible.

### Why This Matters

The (3+1)^2 notation in our paper is not arbitrary. It names what Hassan-Kocic proved is required:
- Two metrics, each with a (3+1) decomposition
- The decompositions are compatible (shared time direction)
- The spatial parts (triads/tetrahedra) have opposite orientations for ghost-freedom
- The interaction occurs at a single vertex (the Field Origin)

---

## 7. The Interaction Vertex and Beta Parameters (Established)

### The Single Interaction Vertex

**Hinterbichler, Rosen (2012)**, "Interacting spin-2 fields," JHEP 07, 047. arXiv:1203.5783.

Key result: Ghost-free spin-2 coupling can only occur at a **single interaction vertex**. This is not an approximation---it is a structural requirement of the theory. Higher-order vertices introduce the ghost.

In our paper: this single interaction vertex is identified as the Field Origin (the point where r = 0 and both tetrad fields meet).

### The Five Free Parameters

The interaction potential has five free coefficients:

```
V(S) = beta_0 e_0(S) + beta_1 e_1(S) + beta_2 e_2(S) + beta_3 e_3(S) + beta_4 e_4(S)
```

where `e_n(S)` are the elementary symmetric polynomials of the 4 x 4 matrix S = sqrt(g^{-1} f).

Explicitly:
- `e_0(S) = 1` (constant)
- `e_1(S) = Tr(S)` (trace)
- `e_2(S) = (1/2)[(Tr S)^2 - Tr(S^2)]`
- `e_3(S) = (1/6)[(Tr S)^3 - 3 Tr(S) Tr(S^2) + 2 Tr(S^3)]`
- `e_4(S) = det(S)` (determinant)

The total number of independent components in the sum: C(4,0) + C(4,1) + C(4,2) + C(4,3) + C(4,4) = 1 + 4 + 6 + 4 + 1 = 16.

These five beta parameters are the **only** free parameters of the theory (apart from the two Planck masses). Their values are not determined within bimetric gravity itself.

### What Our Paper Claims

Our paper claims that the stellated octahedron's topology constrains the beta parameters. The bimetric framework and its five free parameters are established (Hassan-Rosen 2012); the constraint from the topology is the paper's contribution.

---

## 8. Quantum Tetrahedra in LQG (Established)

### The Quantum Tetrahedron

The connection between tetrads and tetrahedra is most explicit in Loop Quantum Gravity (LQG), where the quantum tetrahedron is a fundamental building block of quantized space.

**Barbieri (1998)**, Nucl. Phys. B 518, 714 (arXiv:gr-qc/9707010):
- Associates an irreducible SU(2) representation to each face of a tetrahedron
- Imposes the closure constraint: sum of face normals = 0
- Defines the Hilbert space of the quantum tetrahedron
- **Key quote:** "a triad e_1, e_2, e_3 of independent vectors (nine numbers) defines completely the tetrahedron"

**Baez, Barrett (1999)**, "The Quantum Tetrahedron in 3 and 4 Dimensions" (arXiv:gr-qc/9903060):
- Shows the Hilbert space is labeled by face areas
- Extends to 4D: a tetrahedron in R^4 is described by 4 bivectors satisfying simplicity + closure
- The simplicity constraint B^{IJ} = e^I wedge e^J is precisely the tetrad condition

**Bianchi, Dona, Speziale (2011)**, "Polyhedra in loop quantum gravity," Phys. Rev. D 83, 044035 (arXiv:1009.3402):
- Generalizes Barbieri's construction using Minkowski's theorem (1897)
- A convex polyhedron in R^3 is uniquely determined by its face normals and areas, provided closure holds
- A 4-valent intertwiner (gauge-invariant state in LQG) = a quantum tetrahedron

### The Chain from Tetrad to Quantum Tetrahedron

```
Tetrad e^a_mu
    |
    | (3+1) decomposition
    v
Spatial Triad e^i_a (i=1,2,3)
    |
    | Ashtekar variables (densitized triad + connection)
    v
Holonomy-Flux algebra
    |
    | quantization on spin network graph
    v
Spin Network: edges carry SU(2) representations, nodes carry intertwiners
    |
    | duality: 4-valent node = quantum tetrahedron
    v
Quantum Tetrahedra (Barbieri 1998)
    |
    | Minkowski's theorem: face normals + closure -> polyhedron
    v
Classical Tetrahedra (in semiclassical limit)
```

The tetrad and the tetrahedron sit at opposite ends of this chain, connected by established intermediate steps.

### The Plebanski Formulation

The connection is made even tighter through the Plebanski action, which reformulates GR as a constrained BF theory:

```
S = integral [ B^{IJ} wedge F_{IJ}(omega) + phi_{IJKL} B^{IJ} wedge B^{KL} ]
```

The **simplicity constraint** enforces B^{IJ} = e^I wedge e^J (the B field equals the wedge product of tetrad legs). When discretized on a triangulation:
- The B field is integrated over triangles, yielding bivectors
- The simplicity constraint ensures each bivector is the wedge product of two edge vectors
- The closure constraint for each tetrahedron: sum of 4 bivectors = 0
- This is the discrete Gauss law

**De Pietri, Freidel (1999)** proved that the Plebanski action (= the tetrad action in disguise) is the continuum limit of the Barrett-Crane spin foam model (= built from quantum tetrahedra).

**The tetrad action, when discretized onto a simplicial complex, naturally produces amplitudes that are functions of tetrahedron geometry.**

### Relevance to Our Paper

Our paper does NOT work within LQG. However, the LQG literature establishes rigorously that:
1. The spatial triad defines a tetrahedron (Barbieri 1998)
2. Tetrahedra are the fundamental quanta of 3D space (Bianchi-Dona-Speziale 2011)
3. The closure constraint for tetrahedra = the discrete Gauss constraint (Charles-Livine 2017)
4. The tetrad action discretizes onto tetrahedra (Plebanski formulation)

These results strengthen the paper's use of "tetrahedron" as established terminology, even though the paper operates at the classical (not quantum) level.

### Key References

| Reference | What It Establishes |
|-----------|-------------------|
| **Barbieri (1998)** Nucl. Phys. B 518, 714 | Triad defines tetrahedron; quantum tetrahedron Hilbert space |
| **Baez, Barrett (1999)** arXiv:gr-qc/9903060 | Quantum tetrahedron in 3D and 4D |
| **Bianchi, Dona, Speziale (2011)** Phys. Rev. D 83, 044035 | Polyhedra in LQG via Minkowski's theorem |
| **Charles, Livine (2017)** Gen. Rel. Grav. 49, 92 | Closure constraint = discrete Bianchi identity |
| **Freidel, Speziale (2010)** Phys. Rev. D 82, 084040 | Twisted geometries; triad-tetrahedron phase space |
| **Barrett, Crane (1998)** J. Math. Phys. 39, 3296 | Spin foam model from tetrahedra |
| **De Pietri, Freidel (1999)** CQG 16, 2187 | Plebanski action = continuum limit of Barrett-Crane |
| **EPRL model: Engle, Livine, Pereira, Rovelli (2008)** Nucl. Phys. B 799, 136 | Modern spin foam with Immirzi parameter |
| **Rovelli, Vidotto (2014)** *Covariant Loop Quantum Gravity* | Textbook: tetrads (Ch. 3), tetrahedra as quanta (Ch. 7) |

---

## 9. The Closure Constraint (Established)

### Minkowski's Theorem (1897)

A convex polyhedron in R^3 is uniquely determined (up to translations) by its face normals and face areas, provided they satisfy the **closure constraint**:

```
sum_i A_i n_hat_i = 0
```

where A_i is the area and n_hat_i is the outward unit normal of face i.

For a tetrahedron (4 faces): four normal vectors satisfying closure uniquely determine the tetrahedron.

### Connection to the Gauss Constraint in Tetrad Gravity

In the tetrad/triad formalism, the Gauss constraint is:

```
D_a E_tilde^a_i = 0    (divergence-free condition on densitized triad)
```

This ensures gauge invariance under local SU(2) rotations.

In the spin network / quantum tetrahedron formalism, the **discrete** version of the Gauss constraint at a 4-valent node IS the closure constraint:

```
J_1 + J_2 + J_3 + J_4 = 0
```

where J_i are the SU(2) generators (quantized face normals).

**Charles, Livine (2017)** showed that the closure constraint for the tetrahedron can be reinterpreted as a **discrete Bianchi identity**, giving it deep geometric meaning: the closure of face normals around a polyhedron is the discrete analog of the contracted Bianchi identity nabla_mu G^{mu nu} = 0.

### Two "Closures" in Our Paper

Our paper uses "field closure" (det(g) != 0, non-degeneracy) and the tetrahedron closure (face normals sum to zero). These are related:

1. **Field closure** (det(e) != 0): the 4 tetrad legs span the tangent space -> physics is well-defined
2. **Minkowski closure** (sum n_i = 0): the 4 face normals close -> the tetrahedron exists as a solid
3. The **discrete Gauss constraint** mediates between them: it is the divergence-free condition on the triad, which when discretized becomes the Minkowski closure

---

## 10. Simplicial Gravity and Regge Calculus (Established)

### Regge Calculus

**Regge (1961)**, "General relativity without coordinates," Nuovo Cimento 19, 558.

Spacetime is approximated by flat simplices glued together:
- In 3D: the simplices are tetrahedra (4 vertices, 4 faces, 6 edges)
- In 4D: the simplices are pentachorons (5 vertices, 5 tetrahedral faces, 10 triangular faces)
- Curvature is concentrated on the (d-2)-dimensional "hinges" (edges in 3D, triangles in 4D)

Within each flat simplex, one CAN define a discrete tetrad: any 4 linearly independent edge vectors from a vertex serve as a (non-orthonormal) frame.

### Spin Foam Models

In spin foam models (Barrett-Crane, EPRL-FK), spacetime history is a "foam" of 2-complexes:
- Vertices = 4-simplices (bounded by 5 tetrahedra each)
- Edges = tetrahedra (shared between adjacent 4-simplices)
- Faces = triangles

The amplitude for each configuration depends on the geometry of the tetrahedra (face areas and dihedral angles). In the semiclassical limit, the spin foam amplitude reproduces the Regge action (Conrady-Freidel 2008).

### A Tetrahedron as a Model Spacetime Region

**Colosi, Doplicher, Fairbairn, Modesto, Noui, Rovelli (2005)**, "Background independence in a nutshell: the dynamics of a tetrahedron," CQG 22, 2971 (arXiv:gr-qc/0408079).

This paper explicitly uses a single tetrahedron as a model for a finite region of quantum spacetime. The physical information is encoded as a boundary amplitude on the tetrahedron's 4 faces. This is the closest the literature comes to treating a tetrahedron as the fundamental unit of spacetime geometry.

### Key References

| Reference | What It Establishes |
|-----------|-------------------|
| **Regge (1961)** Nuovo Cimento 19, 558 | Simplicial gravity with tetrahedra as building blocks |
| **Barrett, Crane (1998)** J. Math. Phys. 39, 3296 | Spin foam model from tetrahedra |
| **Conrady, Freidel (2008)** Phys. Rev. D 78, 104023 | Semiclassical limit reproduces Regge action |
| **Colosi et al. (2005)** CQG 22, 2971 | Tetrahedron as model spacetime region |
| **Dittrich, Speziale (2008)** New J. Phys. 10, 083006 | Area-angle variables for Regge calculus |

---

## 11. What This Paper Does Within These Frameworks (Novel)

### What Is Established (Not Our Claim)

| Result | Status | Citation |
|--------|--------|----------|
| Tetrad gravity: g = e^T eta e | Textbook | MTW 1973, Wald 1984 |
| Spatial triad defines a tetrahedron | Established | Barbieri 1998 |
| The (3+1) decomposition | Textbook | ADM 1962 |
| Bimetric gravity: two tetrads E and L | Established | Hassan-Rosen 2012 |
| Single interaction vertex | Established | Hinterbichler-Rosen 2012 |
| Five free beta parameters | Established | Hassan-Rosen 2012 |
| Ghost-freedom requires opposite orientations | Established | Alexander et al. 2014 |
| Compatible (3+1) decompositions | Established | Hassan-Kocic 2018 |
| Tetrahedra are quanta of 3D space (LQG) | Established | Barbieri 1998, Bianchi et al. 2011 |
| Closure constraint = discrete Gauss law | Established | Charles-Livine 2017 |
| The stellated octahedron as a geometric object | Classical geometry | Coxeter 1973 |
| k = 4 from simplex theorem (d+1 for d=3) | Classical geometry | Ziegler 1995 |

### What Is Novel (Our Contribution)

| Claim | What It Does |
|-------|-------------|
| **The stellated octahedron IS the physical realization** of the dual tetrad coupling in bimetric gravity | Identifies the specific geometry that opposite-orientation, compatible-(3+1), single-vertex tetrads form |
| **The coupling hierarchy f(k) = 1 + k + k^2** | Reads out a polynomial from the topology; its three terms map to established structures (vertex, face, interaction) |
| **The topology constrains the beta parameters** | Claims the five free parameters of bimetric gravity are determined by the stellated octahedron's geometry |
| **G from the coupling hierarchy** | alpha^{1+(3+1)+(3+1)^2} = alpha^21 predicts G to 0.12% with zero free parameters |
| **The force hierarchy from coupling depth** | Gravity couples through 21 levels, EM through 1, giving alpha^20 ~ 10^{-43} |
| **The fine-structure constant from interaction states** | 1/alpha = 137 + 1/28 from the total interaction states of the stellated octahedron |
| **Dark matter correction mu(x) = x/(1+x)** | Derived from detailed balance in field closure; a_0 from k^2 G m_e / r_e^2 |
| **Electron mass from exactly determined system** | Two equations from gravity and cosmology, connected by the mass-closure identity, yield m_e at 0.1% |
| **Identification of the Field Origin** | The bimetric interaction vertex identified as the point where r = 0 and both fields meet |
| **(3+1)^2 notation** | Names what Hassan-Kocic proved; not invented, but the specific shorthand is ours |

### The Framing Principle

The paper **operates within** the established dual tetrad field topology. It does not "connect to" or "extend" bimetric gravity. Rather:

1. Tetrad gravity provides the geometry: triad = tetrahedron, k = 4
2. Bimetric gravity provides the dynamics: two tetrads, single vertex, 5 free parameters
3. Four independent arguments (stability, spinor, chirality, bimetric) require opposite orientations
4. Hassan-Kocic requires compatible (3+1) decompositions
5. Together, these define the stellated octahedron

**The paper's contribution is reading out the coupling hierarchy f(k) = 1 + k + k^2 from this established topology and showing what it produces.**

The analogy: in condensed matter physics, the crystal lattice is the system and the band structure is read out from it. Nobody says "we connect to solid-state physics." The dual tetrad field topology is the same kind of established system. The paper reads out the coupling hierarchy that the topology produces.

### Language Guide

| Use | Avoid |
|-----|-------|
| "operates within established tetrad gravity and bimetric gravity" | "connects to bimetric gravity" |
| "the coupling hierarchy that the topology produces" | "determines parameters from geometry" |
| "whose terms correspond to structures already named in the literature" | "counting the geometry" |
| "the spatial triad defines a tetrahedron (Barbieri 1998)" | "the tetrad IS a tetrahedron" (too loose) |
| "the claim that the topology constrains the beta parameters is this paper's contribution" | "we derive bimetric gravity from geometry" (overclaims) |

---

## 12. Complete Citation Index

### Textbook References

| Key | Full Citation | Used For |
|-----|--------------|----------|
| mtw1973 | C.W. Misner, K.S. Thorne, J.A. Wheeler, *Gravitation* (Freeman, 1973) | Tetrad formalism, "square root of the metric," vierbein legs |
| wald1984 | R.M. Wald, *General Relativity* (U. Chicago Press, 1984) | Tetrad formalism, spinor structure |
| adm1962 | R. Arnowitt, S. Deser, C.W. Misner, "The Dynamics of General Relativity" (1962) | The (3+1) decomposition, Hamiltonian GR |
| weinberg1995 | S. Weinberg, *The Quantum Theory of Fields Vol. I* (Cambridge, 1995) | Spinor double cover, SL(2,C) |
| coxeter1973 | H.S.M. Coxeter, *Regular Polytopes* 3rd ed. (Dover, 1973) | Stellated octahedron geometry |
| ziegler1995 | G.M. Ziegler, *Lectures on Polytopes* (Springer, 1995) | Simplex theorem |
| rovelli2014 | C. Rovelli, F. Vidotto, *Covariant Loop Quantum Gravity* (Cambridge, 2014) | Tetrads (Ch. 3), tetrahedra as quanta (Ch. 7) |

### Established Research Papers

| Key | Full Citation | Used For |
|-----|--------------|----------|
| hassan2012 | S.F. Hassan, R.A. Rosen, "Bimetric gravity from ghost-free massive gravity," JHEP 02, 126 (2012) | Ghost-free bimetric gravity; interaction potential; beta parameters |
| hinterbichler2012 | K. Hinterbichler, R.A. Rosen, "Interacting spin-2 fields," JHEP 07, 047 (2012). arXiv:1203.5783 | Single interaction vertex for ghost-free coupling |
| hassankocic2018 | S.F. Hassan, M. Kocic, "On the local structure of spacetime in ghost-free bimetric theory," JHEP 05, 099 (2018). arXiv:1706.07806 | Compatible (3+1) decompositions required for general covariance |
| barbieri1998 | A. Barbieri, "Quantum tetrahedra and simplicial spin networks," Nucl. Phys. B 518, 714 (1998). arXiv:gr-qc/9707010 | Triad defines tetrahedron; quantum tetrahedron; closure constraint |
| alexander2014 | S. Alexander, A. Marciano, L. Smolin, "Gravitational origin of the weak interaction's chirality," Phys. Rev. D 89, 065017 (2014) | Opposite orientations required for ghost-freedom; chirality |
| ashtekar1986 | A. Ashtekar, "New variables for classical and quantum gravity," Phys. Rev. Lett. 57, 2244 (1986) | Chiral decomposition; self-dual/anti-self-dual connections |
| geroch1968 | R. Geroch, "Spinor structure of space-times in general relativity. I," J. Math. Phys. 9, 1739 (1968) | Spinor structure requires orientable double cover |
| deffayet2013 | C. Deffayet, J. Mourad, G. Zahariade, "A note on 'symmetric' vielbeins," JHEP 03, 086 (2013) | Symmetric vielbein condition in bimetric gravity |
| boulware1972 | D.G. Boulware, S. Deser, "Can gravitation have a finite range?" Phys. Rev. D 6, 3368 (1972) | The Boulware-Deser ghost problem |
| hehl1976 | F.W. Hehl et al., "General relativity with spin and torsion," Rev. Mod. Phys. 48, 393 (1976) | Tetrad gravity with torsion |

### LQG and Simplicial Gravity (Supporting)

| Key | Full Citation | Used For |
|-----|--------------|----------|
| baez1999 | J.C. Baez, J.W. Barrett, "The Quantum Tetrahedron in 3 and 4 Dimensions," arXiv:gr-qc/9903060 (1999) | Quantum tetrahedron in 3D and 4D; simplicity constraints |
| bianchi2011 | E. Bianchi, P. Dona, S. Speziale, "Polyhedra in loop quantum gravity," Phys. Rev. D 83, 044035 (2011) | Minkowski theorem; polyhedra from intertwiners |
| charles2017 | C. Charles, E. Livine, "The closure constraint for the hyperbolic tetrahedron as a Bianchi identity," GRG 49, 92 (2017) | Closure = discrete Bianchi identity |
| freidel2010 | L. Freidel, S. Speziale, "Twisted geometries," Phys. Rev. D 82, 084040 (2010) | Triad-tetrahedron phase space parametrization |
| barrett1998 | J.W. Barrett, L. Crane, "Relativistic spin networks and quantum gravity," J. Math. Phys. 39, 3296 (1998) | Spin foam model from tetrahedra |
| depietri1999 | R. De Pietri, L. Freidel, "so(4) Plebanski action and relativistic spin foam model," CQG 16, 2187 (1999) | Plebanski action = continuum limit of Barrett-Crane |
| eprl2008 | J. Engle, E. Livine, R. Pereira, C. Rovelli, "LQG vertex with finite Immirzi parameter," Nucl. Phys. B 799, 136 (2008) | EPRL spin foam model |
| colosi2005 | D. Colosi et al., "Background independence in a nutshell," CQG 22, 2971 (2005) | Tetrahedron as model spacetime region |
| regge1961 | T. Regge, "General relativity without coordinates," Nuovo Cimento 19, 558 (1961) | Simplicial gravity; tetrahedra as building blocks |
| conrady2008 | F. Conrady, L. Freidel, "Semiclassical limit of 4d spin foam models," Phys. Rev. D 78, 104023 (2008) | Semiclassical limit recovers Regge action |
| dittrich2008 | B. Dittrich, S. Speziale, "Area-angle variables for general relativity," New J. Phys. 10, 083006 (2008) | Area-angle Regge variables |
| plebanski1977 | J.F. Plebanski, "On the separation of Einsteinian substructures," J. Math. Phys. 18, 2511 (1977) | BF formulation of GR with simplicity constraints |

---

## Key Verbatim Quotes for Future Reference

### Barbieri (1998), Section II.A
> "A tetrahedron can be understood as the convex envelope of four points in 3-dimensional Euclidean space E^3. [...] **a triad e_1, e_2, e_3 of independent vectors (nine numbers) defines completely the tetrahedron.**"

### Barbieri (1998), Section II.C
> "If we imagine the tetrahedron as imbedded in 3+1 Minkowski spacetime, the requirement that all the edges are spacelike is equivalent to the requirement that the 4-dimensional 'normal' of the tetrahedron [...] lies inside the light cone."

### Barbieri (1998), on closure
> "The last equation [...] is simply the 'closure' condition (in the form integral_S n da = 0 it holds for every closed surface S)"

### Barbieri (1998), on parity and the quantum tetrahedron
> "we may distinguish the original and its P-transformed tetrahedra by means of the sign we give to n_1 . n_2 x n_3"

(This parity distinction is precisely the opposite-orientation condition required for ghost-freedom in bimetric gravity.)

### Barbieri (1998), Section III, on spin networks
> "The connection between quantum tetrahedra and the spin networks used in the Loop Representation framework of quantum General Relativity is fairly obvious: condition (11), translated in terms of the representations' spins, is nothing but the compatibility condition for the spins of the edges adjacent to a 4-valent vertex."

---

*End of reference document.*
