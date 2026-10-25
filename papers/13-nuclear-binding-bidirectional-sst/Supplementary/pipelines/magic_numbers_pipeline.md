# Nuclear Magic Numbers from the Sierpiński Walk

## Pipeline: Deriving the seven magic numbers from packing algebra

This document describes the complete derivation of the nuclear magic
numbers 2, 8, 20, 28, 50, 82, 126 from the structural constants K = 4
and D = 3. Every number is exact and algebraic. No fitting, no
spin-orbit coupling, no phenomenological terms.

---

## Inputs

**Two structural constants.** K = 4 (branching factor) and D = 3 (depth).
These are the unique integer solution of the closure condition
$2(D+1) = 2^D$, which requires that the number of linear degrees of
freedom in the structure equals the number of states it can encode.

**One structure.** The Sierpiński walk: an equilateral triangle subdivided
D = 3 times at branching factor K = 4, producing $K^D = 64$ sub-triangles.
Each sub-triangle is one position in the walk.

**One equation.** The SST quadratic $\mu_{\text{SST}}(x)$ defines the
coupling at each walk position, but the magic numbers themselves do not
depend on it. They follow entirely from K, D, and the packing geometry.
The magic numbers are a property of the walk, not the field equation.

---

## Step 1. The walk hierarchy

The 64 positions are organized in a three-level hierarchy set by
K = 4 and D = 3:

- **Level 1 (faces):** The triangle has K = 4 faces, indexed 0, 1, 2, 3.
- **Level 2 (channels):** Each face contains K = 4 channels.
- **Level 3 (sub-channels):** Each channel contains K = 4 sub-channels.

Total positions: $4 \times 4 \times 4 = K^D = 64$.

Every position has a three-digit address in base K: (face, channel,
sub-channel). For example, position (2, 1, 3) is face 2, channel 1,
sub-channel 3. There are $4^3 = 64$ such addresses.

These 64 positions constitute one face of the parent Sierpiński triangle,
which itself has K = 4 faces for a total capacity of $4 \times 64 = 256$.
The shell structure described here operates within a single face.

---

## Step 2. The gate face

At each level of the hierarchy, three of the four faces are ordinary
and one is special. The fourth face at each level (index 3) is the
**gate face**: the boundary where the structure folds back on itself.

The gate face is physically distinct because it sits at the interface
between the current level and the next. Positions that fall on the gate
face are excluded from the shell count because they belong to the
boundary, not the interior.

The gate face has index K - 1 = 3 (zero-indexed), or equivalently, it
is the K-th face (one-indexed). This means the gate first contributes
positions at shell level n = K. For shells below n = K, the packing
has not yet reached the gate boundary and no exclusion occurs.

> **Key point.** The gate face is not an added rule. It is a property of
> the Sierpiński geometry: any K-fold branching structure with D levels
> has a boundary face at each level. The exclusion is structural.

---

## Step 3. Concentric shell layers

Nucleons fill the walk sequentially, and the positions pack into
concentric layers indexed by $n = 1, 2, 3, \ldots$. Each layer n adds
positions at the n-th level of the packing. The cumulative count of
positions through layer n is given by the tetrahedral number:

$$T(n) = \frac{n(n+1)(n+2)}{6}$$

This is the standard formula for the cumulative count in a structure
that branches K-fold at each level. It is called "tetrahedral" because
it counts the number of objects in a tetrahedron of side n, which is the
natural packing geometry for a K = 4 branching structure.

The first several values:

| n | T(n) | Layer size T(n) - T(n-1) |
|---|------|--------------------------|
| 1 |    1 | 1 |
| 2 |    4 | 3 |
| 3 |   10 | 6 |
| 4 |   20 | 10 |
| 5 |   35 | 15 |
| 6 |   56 | 21 |
| 7 |   84 | 28 |

Each layer n adds $n(n+1)/2$ new positions (the triangular number).
This is the number of positions in one triangular slice of the
tetrahedral packing.

> **Note.** The layer sizes 1, 3, 6, 10, 15, 21, 28 are the triangular
> numbers. At n = 7, the layer size is 28, the geometric element count
> of the stellated octahedron (8 vertices + 12 edges + 8 faces).

---

## Step 4. Gate exclusion

Not all positions counted by T(n) are available for shell filling.
Positions that fall on the gate face are excluded. The number of
excluded positions at shell level n is:

$$G(n) = \begin{cases} 0 & n < K \\ \frac{(n-1)\,n}{2} & n \geq K \end{cases}$$

**Why this formula.** The gate face is a triangular boundary surface.
At shell level n, the gate boundary has $(n-1)n/2$ positions on it,
which is the triangular number for side $(n-1)$. These positions lie
on the boundary between the interior and the gate face, and they are
excluded from the interior shell count.

**Why activation at n = K.** The gate face is the K-th face at each
level of the hierarchy. For shells $n < K$, the packing has not yet
reached the K-th face, so the gate boundary has no positions to exclude.
At $n = K = 4$, the packing first reaches the gate face, and exclusion
begins. This is not a threshold that is chosen or adjusted. It is a
geometric consequence of K = 4.

The gate exclusion values:

| n | G(n) | Why |
|---|------|-----|
| 1 | 0 | n < K, gate inactive |
| 2 | 0 | n < K, gate inactive |
| 3 | 0 | n < K, gate inactive |
| 4 | 6 | n = K, gate activates. G(4) = 3 x 4 / 2 = 6 |
| 5 | 10 | G(5) = 4 x 5 / 2 = 10 |
| 6 | 15 | G(6) = 5 x 6 / 2 = 15 |
| 7 | 21 | G(7) = 6 x 7 / 2 = 21 |

> **Note.** G(7) = 21 = 1 + K + K² = the coupling polynomial evaluated
> at s = +1. The number of positions excluded at the final shell equals
> the full coupling depth of the stellated octahedron.

---

## Step 5. Shell closures and magic numbers

The cumulative number of nucleons that can occupy the walk through
shell level n is:

$$M(n) = 2\big[T(n) - G(n)\big]$$

**The factor of 2.** Each walk position can hold two nucleons: one
proton and one neutron (or equivalently, the two tetrahedra of the
dual structure contribute independently). This is the same isospin
degeneracy that appears in the standard nuclear shell model.

**The available positions** at each shell are $T(n) - G(n)$: the
tetrahedral count minus the gate exclusion. The factor of 2 doubles
this for the two orientations.

**The shell capacity** (how many nucleons each new shell adds) is
$M(n) - M(n-1)$.

The complete table:

| n | T(n) | G(n) | T(n) - G(n) | M(n) | Capacity | Observed magic? |
|---|------|------|-------------|------|----------|-----------------|
| 1 |    1 |    0 |           1 |    2 |        2 | 2 ✓ |
| 2 |    4 |    0 |           4 |    8 |        6 | 8 ✓ |
| 3 |   10 |    0 |          10 |   20 |       12 | 20 ✓ |
| 4 |   20 |    6 |          14 |   28 |        8 | 28 ✓ |
| 5 |   35 |   10 |          25 |   50 |       22 | 50 ✓ |
| 6 |   56 |   15 |          41 |   82 |       32 | 82 ✓ |
| 7 |   84 |   21 |          63 |  126 |       44 | 126 ✓ |

All seven nuclear magic numbers are reproduced exactly.

---

## Step 6. The 20 → 28 anomaly

This is the central result. In the standard nuclear shell model, the
naive shell capacities follow from harmonic oscillator degeneracies
and grow as 2, 6, 12, 20, 30, 42, 56. The fourth shell has capacity 20,
giving a cumulative closure at 40, not 28. The observed magic number
sequence (20, 28) has a gap of only 8, not 20.

Mayer and Jensen (1949) resolved this by adding a phenomenological
spin-orbit coupling term to the nuclear potential. The strength of
this term is adjusted to reproduce the correct shell sequence.

In the Sierpiński walk, the resolution is structural. At $n = 4 = K$,
the gate face activates and excludes $G(4) = 6$ positions from the
shell count. The raw tetrahedral count at n = 4 is T(4) = 20. After
gate exclusion, the available positions are $T(4) - G(4) = 20 - 6 = 14$.
After doubling for proton-neutron orientations:

$$M(4) = 2 \times 14 = 28$$

The shell capacity at n = 4 is $M(4) - M(3) = 28 - 20 = 8$. This is
exactly the observed anomaly. No spin-orbit term is introduced. The
gate face, which is a geometric property of the K = 4 branching
structure, does the work.

> **What to verify.** The gate exclusion at n = 4 removes exactly 6
> positions. This is not a parameter. It is G(4) = (4-1)(4)/2 = 6,
> computed from K alone. A different value of K would give a different
> gate threshold and different magic numbers. K = 4 is the only value
> that reproduces the observed sequence.

---

## Step 7. Shell capacities vs. standard model

The shell capacities from the Sierpiński walk and from the standard
nuclear shell model (with spin-orbit coupling) are:

| Shell | Sierpiński capacity | Standard model capacity | Match? |
|-------|--------------------|-----------------------|--------|
| 1     | 2                  | 2                     | ✓ |
| 2     | 6                  | 6                     | ✓ |
| 3     | 12                 | 12                    | ✓ |
| 4     | 8                  | 8 (with spin-orbit)   | ✓ |
| 5     | 22                 | 22                    | ✓ |
| 6     | 32                 | 32                    | ✓ |
| 7     | 44                 | 44                    | ✓ |

Both approaches reproduce the same capacities. The difference is that
the standard model requires spin-orbit coupling (a phenomenological
term with adjustable strength) to achieve this, while the Sierpiński
walk produces it from the gate face threshold at n = K = 4.

---

## Step 8. Connection to the binding energy curve

The shell closures and the binding energy curve share the same walk
structure. The positions that pack into shells (this pipeline) are the
same positions that contribute coupling $\mu_{\text{SST}}(i^2)$ to
the binding sum (the binding energy pipeline).

The magic numbers mark the mass numbers where shells close. On the
binding energy curve, these correspond to nuclei with enhanced stability:
the binding energy per nucleon is locally higher at magic numbers than
at neighbouring mass numbers. This is visible as fine structure
(small oscillations) on top of the smooth envelope curve.

The two pipelines are independent computations on the same structure:

- **Magic numbers** use only K, D, and the packing geometry (T, G, M).
  They are exact integers. No field equation is involved.
- **Binding energy** uses $\mu_{\text{SST}}(i^2)$ evaluated at each
  walk position. It is a continuous curve calibrated from one element.

Both are outputs of the 64-position Sierpiński walk defined by K = 4
and D = 3.

---

## Summary

The construction has three parts:

1. **One packing formula.** $T(n) = n(n+1)(n+2)/6$ counts cumulative
   positions in the K-fold branching structure.

2. **One exclusion rule.** $G(n) = (n-1)n/2$ for $n \geq K$, zero
   otherwise. The gate face excludes boundary positions starting at
   the shell level where the packing reaches the K-th face.

3. **One doubling.** $M(n) = 2[T(n) - G(n)]$ accounts for
   proton-neutron orientations.

The seven magic numbers 2, 8, 20, 28, 50, 82, 126 follow from
K = 4 alone. The anomalous $20 \to 28$ gap (capacity 8 instead of 18)
emerges from gate exclusion at n = K = 4, without spin-orbit coupling.

---

## What is NOT in this pipeline

- **No spin-orbit coupling.** The $20 \to 28$ gap is structural, not
  dynamical. No potential term is added or adjusted.
- **No angular momentum quantum numbers.** The standard shell model
  derives capacities from l and j values. This pipeline derives
  them from the gate face geometry.
- **No fitted parameters.** K = 4 and D = 3 are fixed by the closure
  condition. The gate threshold n = K is a geometric consequence, not
  a choice.
- **No field equation.** The magic numbers depend only on the walk
  structure. The SST quadratic is not used. This is pure combinatorics.

---

## Cross-references

- Binding energy pipeline: `nuclear_binding_pipeline.md`
- Walk structure: [docs.fielddynamics.org/framework/md/why_k4_d3](https://docs.fielddynamics.org/framework/md/why_k4_d3/)
- Gate face: [docs.fielddynamics.org/framework/md/face_structure_and_spin](https://docs.fielddynamics.org/framework/md/face_structure_and_spin/)
- Validation tests: [docs.fielddynamics.org/tests](https://docs.fielddynamics.org/tests/)
- Python script: `magic_numbers_pipeline.py`

---

*Stephen Nelson, Field Dynamics Research. March 2026.*
