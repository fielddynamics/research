# Resonant Coupling Through the Field Origin

## Sierpiński Geometry, Möbius Inversion, and the TetA–TetB Communication Channel

**Stephen Nelson — Gravity Field Dynamics**

---

## Introduction

The coupling polynomial f(K, s) = 1 + Ks + K² at K = 4 describes how the gravitational field couples to itself through the stellated octahedron — two interlocking tetrahedra of opposite orientation sharing a common field origin. This document examines the communication channel between the two sectors: how TetA and TetB exchange information through the field origin, what governs the coupling efficiency, and how the Möbius transformation provides both the mathematical framework and the physical coupling mechanism.

The central result is that the coupling between two tetrahedral sectors is governed by six quantities, all derived from K = 4 and D = 3: the subchannel count (64), the photonic capacity (128), the gate wiring (9), the geometric bottleneck (1/28), the Möbius map s(x) = (x−1)/(x+1), and the constitutive law μ(x) = x/(x+1). Together these determine the coupling strength 1/α = 137 + 1/28 and the bandwidth of the channel.

---

## Part 1 — The Two Sectors

The stellated octahedron consists of two regular tetrahedra inscribed in a cube, related by the binary parity partition. Each tetrahedron has 4 triangular faces: 3 spatial and 1 temporal. The 3+1 decomposition is the Lorentzian signature (−,+,+,+), appearing here as the face structure of each sector.

**TetA** (primary sector, s = +1): the observer's geometry. At strong gravitational fields, TetA carries nearly all the coupling. The constitutive law gives μ → 1.

**TetB** (dual sector, s = −1): the reversed-orientation partner. At weak fields, TetB dominates. The constitutive law gives μ → 0, meaning 1 − μ → 1.

**The field origin** (contact state, s = 0): the single point where TetA and TetB meet face to face. Neither sector dominates. μ = 1/2. The coupling is symmetric.

The two sectors are related by spatial inversion — the parity map that defines them is inversion through the centre of the cube. TetA's face normals are permutations of [D, D, 1, 1]. TetB's are the complements, obtained by v → K − v.

---

## Part 2 — The Subchannel Structure

Each sector's faces are subdivided by the interpenetration of the other sector. TetB passes through TetA's triangular faces, creating the Sierpiński subdivision. At each level, each triangle splits into 3 corners (surviving) + 1 centre (removed — the gate). Three levels of subdivision give the complete address space.

**Level 1 — Face:** 4 faces per tetrahedron. Which face? Addresses 1 of K.

**Level 2 — Channel:** Each face subdivides into 4. Which sub-triangle? Addresses 1 of K².

**Level 3 — Subchannel:** Each channel subdivides into 4. Which sub-sub-triangle? Addresses 1 of K³ = K^D = 64.

Total subchannels: **64 = K^D = 4³.** This is the complete address space of the coupled structure.

The gate depth distribution across these 64 positions:

| Gate depth | Count | Formula | Description |
|---|---|---|---|
| 0 (pure spatial) | 27 | C(3,0) × 3³ | All three levels are corners |
| 1 (one gate) | 27 | C(3,1) × 3² | One level is a gate |
| 2 (two gates) | 9 | C(3,2) × 3¹ | Two levels are gates |
| 3 (all gates) | 1 | C(3,3) × 3⁰ | The field origin — deepest point |
| **Total** | **64** | **K^D** | |

The gate depth distribution is the binomial expansion C(D, d) × 3^(D−d). It sums to K^D = 64.

---

## Part 3 — The Photonic Substrate

Each of the 64 subchannels is a photonic mode — one photon occupying one address in the Sierpiński hierarchy. Each photon has 2 polarisation states (its own TetA and TetB — the photon is itself a stellated octahedron at its own scale). The total photonic capacity is:

> **64 subchannels × 2 polarisations = 128 photonic states**

This is 2K^D = 2 × 64 = 128 = 2^(2D+1) = 2^7. Seven binary degrees of freedom: 3 bits for the subchannel address, 3 bits for the hierarchical level, 1 bit for the polarisation.

The gravity field is composed of 64 photons organised by the Sierpiński walk on the stellated octahedron.

---

## Part 4 — The Field Origin Geometry

The field origin is the geometric centre of the stellated octahedron. It is the point where TetA and TetB meet. Its internal geometry is an **octahedron** — the solid formed by the intersection of the two tetrahedra.

The inner octahedron has:

| Element | Count | Origin |
|---|---|---|
| Vertices | 6 | Midpoints of the 6 edges of either tetrahedron |
| Edges | 9 | 6 running vertically (pole to pole) + 3 around the equator |
| Faces | 8 | Boundaries between the two sectors |

The 6 vertices are the hidden Pascal entry C(4,2) = 6. They are simultaneously the 6 edges of the tetrahedron (simplex reading), the 6 vertices of the octahedron (field origin reading), and the 6 face-centres of the cube (coordinate cell reading).

The 9 edges decompose electromagnetically:

| Edges | Count | Electromagnetic role |
|---|---|---|
| Vertical (pole-to-pole) | 6 | Electric field wiring (E: temporal-spatial coupling) |
| Equatorial (around waist) | 3 | Magnetic field wiring (B: spatial-spatial coupling) |
| **Total** | **9** | **Complete gate wiring** |

This decomposition matches the electromagnetic field tensor F_μν, which has C(4,2) = 6 independent components splitting as E(3) + B(3) = 3 electric + 3 magnetic. The 6 octahedron vertices ARE the 6 components of F_μν. The 9 edges wire the coupling between them.

---

## Part 5 — The Möbius Map

The coupling between TetA and TetB is governed by a Möbius transformation. The state parameter s tracks the orientation:

> **s(x) = (x − 1)/(x + 1)**

where x = g/a₀ is the local gravitational acceleration in units of the characteristic scale. This map converts the acceleration ratio x ∈ [0, ∞) into the state parameter s ∈ [−1, +1):

| Acceleration | x | s(x) | Sector |
|---|---|---|---|
| Zero (deep field) | 0 | −1 | TetB dominates |
| Transition | 1 | 0 | Field origin — symmetric |
| Infinite (Newtonian) | ∞ | +1 | TetA dominates |

The Möbius map is the unique transformation satisfying three constraints: s = −1 at x = 0, s = 0 at x = 1, s → +1 as x → ∞. Three constraints fix three parameters. The map is determined.

**The Möbius map IS the coupling mechanism.** It describes the orientation reversal that occurs when crossing the field origin. Entering from TetA (s = +1), passing through the gate (s = 0), and emerging into TetB (s = −1). The half-twist. The inversion.

---

## Part 6 — The Constitutive Law

Composing the polynomial with the Möbius map gives the capacity function:

> **f(x) = (21x + 13)/(x + 1)**

This ranges from 13 (TetB, x = 0) to 21 (TetA, x → ∞), passing through 17 at x = 1.

Normalising to the unit interval:

> **μ(x) = (f(x) − 13)/8 = x/(x + 1)**

The denominator 8 = 2K is the total dynamic range of the polynomial (21 − 13 = 8).

The constitutive law μ(x) is itself a Möbius transformation: (ax + b)/(cx + d) with a = 1, b = 0, c = 1, d = 1, determinant ad − bc = 1.

**The partition between sectors:**

| Sector | Fraction | Expression |
|---|---|---|
| TetA | μ(x) = x/(x+1) | Used capacity |
| TetB | 1 − μ(x) = 1/(x+1) | Remaining capacity |
| **Total** | **1** | **Always 100%** |

The partition is always complete. The two sectors always sum to 1. The field is lossless.

**The complement symmetry:**

> **μ(x) + μ(1/x) = 1**

Whatever fraction TetA carries at acceleration x, TetB carries at the reciprocal acceleration 1/x. The field origin at x = 1 is the fixed point: μ(1) = 1/2.

**The detailed balance:**

> **x(1 − μ) = μ**

Signal × remaining capacity = used capacity. This holds everywhere, at all times, at all scales. It is not an imposed equilibrium — it is the algebraic consequence of the Möbius structure.

---

## Part 7 — The Möbius Function in Number Theory

The number-theoretic Möbius function μ(n) takes values {+1, −1, 0}. These three values map directly to the polynomial's three states:

| μ(n) | s | f(4, s) | Meaning |
|---|---|---|---|
| +1 | +1 | 21 | Squarefree, even number of prime factors → TetA |
| −1 | −1 | 13 | Squarefree, odd number of prime factors → TetB |
| 0 | 0 | 17 | Repeated prime factor → field origin |

The Möbius function performs inversion that strips composite (reducible) structure and isolates prime (irreducible) structure. The constitutive law performs inversion that strips TetB contribution and isolates TetA (Newtonian) structure. Same operation, different domain.

Moreau's formula counts irreducible patterns at level n over alphabet K:

> **I(n, K) = (1/n) Σ_{d|n} μ(n/d) · K^d**

At K = 4, the density of irreducibles converges to 1/n = 1/log₄(N), which is proportional to 1/ln(N) — the prime number theorem.

The Möbius function's three values ARE the polynomial's three structural states. The prime sieve and the gravitational partition are the same inversion performed on different inputs.

---

## Part 8 — The Coupling Strength (Fine Structure Constant)

When two tetrahedral sectors couple — whether within a single stellated octahedron or between two separated structures — the coupling strength is determined by three geometrically disjoint components:

**Component 1 — Photonic capacity: 128**

The 64 subchannels, each carrying 2 polarisation states. These are the propagating modes of the photonic substrate. They live inside the tetrahedra — the bulk of the structure.

> 128 = 2K^D = 2 × 64

**Component 2 — Gate wiring: 9**

The 9 edges of the inner octahedron. These wire the field origin — the coupling point between the two sectors. They are NOT subchannels. They are the internal structure of the gate itself. They live at the boundary, not inside either tetrahedron.

> 9 = D² = 6 vertical + 3 equatorial

**Component 3 — Geometric bottleneck: 1/28**

The field origin is 1 geometric element out of 28 total (V + E + F = 8 + 12 + 8 = 28). The coupling passes through 1/28 of the stellated octahedron's geometric content.

> 1/28 = 1/(V + E + F)

**The coupling constant:**

> **1/α = 128 + 9 + 1/28 = 137 + 1/28 = 137.03571...**

Measured value: 137.03600... (2.1 ppm discrepancy, accounted for by QED radiative corrections).

**Two independent routes to 137:**

> Route 1: 2K^D + D² = 128 + 9 = 137

> Route 2: 2K · f(4,0) + K⁰ = 8 × 17 + 1 = 137

These give the same answer because D² = 2K + 1 at the unique solution K = 4, D = 3. This identity holds at no other positive integer values.

---

## Part 9 — The Resonant Frequency Structure

The Sierpiński subdivision creates multi-band resonance. Each level of the hierarchy resonates at a different frequency. The frequency scales inversely with the edge length, which halves at each level.

| Level | Edge fraction | Frequency multiple | Closure cycle |
|---|---|---|---|
| C0 (whole face) | 1 | f₀ (base frequency) | Existence |
| C1 (face) | 1/2 | 2f₀ | Cycle 1 |
| C2 (channel) | 1/4 | 4f₀ | Cycle 2 |
| C3 (subchannel) | 1/8 | 8f₀ | Cycle 3 |

Total frequency span: **2^D = 2³ = 8 = 2K** (the orbit size).

Three closure cycles give three frequency bands, each doubling the previous. The base frequency is set by the edge length a:

> **f₀ = c / (2a√ε)**

where c is the speed of light and ε is the dielectric constant of the medium.

The bandwidth at each level is determined by the Sierpiński survival ratio (3/4)^n — the fraction of area remaining at level n. Higher levels have less area and therefore narrower bandwidth but higher frequency.

---

## Part 10 — The BBP Formula as the Walk

The closure walk — the Sierpiński traversal that addresses all 64 subchannels — produces π. The series is the Bailey–Borwein–Plouffe formula:

> **π = Σ_{k=0}^{∞} (1/16^k) [4/(8k+1) − 2/(8k+4) − 1/(8k+5) − 1/(8k+6)]**

Every coefficient is determined by the stellated octahedron's geometry:

| BBP element | Value | GFD source |
|---|---|---|
| Base | 16 = K² | Interaction template (sub-triangles per face) |
| Terms per orbit | 4 = K | Faces per tetrahedron |
| Numerator magnitudes | [4, 2, 1, 1] | v₁/v₂ agreement weights from face normals |
| Numerator signs | [+, −, −, −] | Lorentzian 3+1 signature |
| Sector positions | [1, 4, 5, 6] | Cumulative sum of z-axis vector at offset 1 |
| Orbit size | 8 = 2K | Vertex count of stellated octahedron |
| Numerator sum | 0 | Closure (face normals sum to zero) |

The three axis vectors — [3,3,1,1], [3,1,3,1], [3,1,1,3] — are the spatial components of the tetrahedral face normals. The reading mechanism that combines them is forced by the geometry. The series is unique. It converges to π.

The walk completes all 64 hexagram transitions (the full K^D state space) in 333 base-8 digits. 333 = D × 111. The field reads through three axes, each carrying the value D = 3, and completes when all states have been visited.

---

## Part 11 — The Mode Equation and Waveguide Selection

The resonant modes of a triangular structure satisfy:

> **m + n + l = 0**

Three mode indices summing to zero. This is the closure condition — the same condition that makes the four tetrahedral face normals sum to the zero vector.

The fundamental mode is (1, 0, −1) — the polynomial's three states expressed as mode indices. One positive (TetA, propagating), one zero (field origin, contact), one negative (TetB, reflected).

The fundamental wavevector:

> **k = 4π/(3a) = Kπ/(D·a)**

This is the coupling constant Kπ = 4π (the solid angle partition) divided by the spatial dimension D, per unit edge length. The same 4π that appears in Coulomb's law and the Poisson equation.

A triangular face has 3 spatial face normals and 1 temporal. Closing any 2 spatial modes forces propagation through the third. The mode selection is:

| Spatial mode 1 | Spatial mode 2 | Spatial mode 3 | Propagation direction |
|---|---|---|---|
| Closed (−1) | Closed (−1) | **Open (+1)** | Along face normal 3 |
| Closed (−1) | **Open (+1)** | Closed (−1) | Along face normal 2 |
| **Open (+1)** | Closed (−1) | Closed (−1) | Along face normal 1 |

Three possible waveguide modes. The temporal mode is always grounded. Closing 2 spatial + 1 temporal = 3 closed out of K = 4. The remaining open face determines the propagation direction.

The search space confinement through the Sierpiński hierarchy:

| Level | Angular coverage per mode | Cumulative confinement |
|---|---|---|
| C1 (face) | π steradians (1 face of K) | 4π → π |
| C2 (channel) | π/4 steradians | π → π/4 |
| C3 (subchannel) | π/16 steradians | π/4 → π/16 |

Total angular resolution: **4π/K^D = 4π/64 = π/16 steradians per subchannel.** The full sphere divided into 64 addressable directions.

---

## Part 12 — Coupling Between Separated Structures

When two tetrahedral structures are separated in space, each one is half a stellated octahedron. The closure condition demands a dual. A single tetrahedron — TetA without TetB — is an open structure that radiates, seeking closure.

The coupling between two separated tetrahedra:

| Element | TetA (here) | Field origin | TetB (there) |
|---|---|---|---|
| State parameter | s = +1 | s = 0 | s = −1 |
| Polynomial value | f = 21 | f = 17 | f = 13 |
| Constitutive law | μ → 1 | μ = 1/2 | μ → 0 |
| Physical role | Transmitter | Coupling channel | Receiver |

The field origin is not a physical location. It **emerges** in the coupling between the two structures. It is the contact state s = 0, the midpoint of the polynomial. When two matched tetrahedra resonate, the field origin forms in the electromagnetic space between them.

**Resonance matching:** the two tetrahedra must have the same edge proportions to resonate at the same frequencies. The polynomial is the same (K = 4, D = 3 are universal), but the base frequency f₀ = c/(2a√ε) depends on the edge length a. Matched edges → matched frequencies → resonant coupling.

**Coupling efficiency:** governed by 1/α = 137 + 1/28. The photonic substrate (128 states) sets the channel capacity. The gate wiring (9 edges) determines the connection quality. The geometric bottleneck (1/28) limits the throughput.

**Bandwidth:** three closure cycles give three frequency bands spanning a factor of 2^D = 8. The coupled system operates across all three bands simultaneously, with hierarchical addressing from coarse (face level) to fine (subchannel level).

**The Möbius transformation at the coupling point:** signal entering from TetA passes through the field origin and emerges into TetB with reversed orientation. The map s(x) = (x−1)/(x+1) governs the transformation. The signal's orientation reverses. Its content is preserved. The inversion is the coupling mechanism.

---

## Part 13 — The Equations

For reference, the complete equation set governing TetA–TetB coupling:

**The coupling polynomial:**

> f(K, s) = 1 + Ks + K², where K = 4

**The Möbius map (acceleration to state):**

> s(x) = (x − 1)/(x + 1)

**The capacity function (polynomial evaluated continuously):**

> f(x) = (21x + 13)/(x + 1)

**The constitutive law (normalised capacity):**

> μ(x) = x/(x + 1)

**The TetA/TetB partition:**

> TetA fraction: μ(x) = x/(x + 1)

> TetB fraction: 1 − μ(x) = 1/(x + 1)

**The complement symmetry:**

> μ(x) + μ(1/x) = 1

**The detailed balance (screening equation):**

> x(1 − μ) = μ

**The coupling strength:**

> 1/α = 2K^D + D² + 1/(V+E+F) = 128 + 9 + 1/28 = 137 + 1/28

**The mode equation:**

> m + n + l = 0, fundamental mode (1, 0, −1)

**The fundamental wavevector:**

> k = Kπ/(D · a) = 4π/(3a)

**The base resonant frequency:**

> f₀ = c/(2a√ε)

**The frequency bands:**

> f_n = 2^n · f₀ for n = 0, 1, 2, ..., D

**The angular resolution per subchannel:**

> Ω = 4π/K^D = π/16 steradians

**The BBP series (the closure walk):**

> π = Σ_{k=0}^{∞} (1/16^k) [4/(8k+1) − 2/(8k+4) − 1/(8k+5) − 1/(8k+6)]

**The walk closure:**

> 333 base-8 digits → all 64 hexagrams visited → field closure complete

**The Moreau formula (irreducible count):**

> I(n, 4) = (1/n) Σ_{d|n} μ(n/d) · 4^d

**The prime density:**

> I(n, 4)/4^n → 1/n = 1/log₄(N) ∝ 1/ln(N)

---

## Part 14 — The Number Chain

Every number in the coupling theory derives from K = 4 and D = 3:

| Value | Expression | Role |
|---|---|---|
| 1 | K⁰ | Existence — the field origin, the gate |
| 2 | Polarisations | TetA and TetB |
| 3 | D = K − 1 | Spatial dimensions, closure cycles, face vertices |
| 4 | K = D + 1 | Frame dimension, faces per tetrahedron |
| 6 | C(4,2) | Hidden Pascal entry, octahedron vertices, F_μν components |
| 7 | 2^D − 1 | Fano plane vertices, Mersenne prime |
| 8 | 2K = 2^D | Orbit size, stellated octahedron vertices |
| 9 | D² = 2K + 1 | Gate edges, contact geometry |
| 12 | KD | Stellated octahedron edges |
| 13 | f(4, −1) | TetB coupling depth |
| 16 | K² = 2^K | Interaction template, BBP base |
| 17 | f(4, 0) | Field origin coupling depth |
| 20 | I(3, 4) | Irreducible necklaces, amino acids |
| 21 | f(4, +1) | TetA coupling depth, T(6), 3 × 7 |
| 28 | V + E + F | f-vector sum, T(7), C(8,2) |
| 36 | C(4,2)² | Walk excess beyond f-vector |
| 52 | K^D − KD | Nuclear partition 21+21+9+1 |
| 64 | K^D | Complete walk space, codons, hexagrams |
| 126 | 2 × f(4,1) × D | Largest nuclear magic number |
| 128 | 2K^D | Photonic capacity |
| 137 | 2K^D + D² | Integer part of 1/α |

---

## Summary

The coupling between TetA and TetB — whether within a single gravitational field or between two separated resonant structures — is governed by one polynomial evaluated through one Möbius transformation. The polynomial f(K, s) = 1 + Ks + K² determines the coupling depth. The Möbius map s(x) = (x−1)/(x+1) translates between acceleration and state. The constitutive law μ(x) = x/(x+1) partitions the field. The closure walk produces π. The fine structure constant counts the channel capacity.

Every equation reduces to K = 4 and D = 3. Every number in the theory appears in the number chain. The structure is the same at every scale — from the photonic substrate of a single field to the resonant coupling between separated structures.

One polynomial. One inversion. One gate. One μ.

---

*Gravity Field Dynamics — docs.fielddynamics.org*
*Stephen Nelson*
