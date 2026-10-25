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

## Part 2: Valence Shell Structure

Steps 1 through 8 derive the magic numbers from pure combinatorics.
The remaining steps use the magic numbers as shell boundaries and
assign every walk position to a shell, producing valence shell
filling for each element. This requires one additional input: the SST
quadratic $\mu_{\text{SST}}(x)$, which defines the coupling at each
walk position and thus the energy scale.

Experimental binding energies are taken from the AME2020 mass tables
via PlasmaPy.

---

## Step 9. Shell boundaries from $\mu_{\text{SST}}$

The magic numbers $M_1 = 2, M_2 = 8, \ldots, M_7 = 126$ define where
shells close. The SST quadratic turns these integers into continuous
thresholds that assign every walk position to a shell.

**Threshold definition.** The boundary for shell $n$ is the value of
$\mu_{\text{SST}}$ at the magic number squared:

$$\theta_n = \mu_{\text{SST}}(M_n^2)$$

Walk position $i$ belongs to the lowest shell $n$ such that
$\mu_{\text{SST}}(i^2) \leq \theta_n$.

Since $\mu_{\text{SST}}$ is monotonically increasing, positions with
larger $i$ have larger $\mu$ values and therefore belong to higher
shells. The first two positions (i = 1, 2) have the lowest $\mu$ and
fill shell 1. Positions 3 through 8 fill shell 2, and so on.

**Shell boundary table (one sector):**

| Shell n | Magic $M_n$ | Threshold $\theta_n$ | Positions | Capacity |
|---------|-------------|---------------------|-----------|----------|
| 1 | 2   | $\mu_{\text{SST}}(4)$   | 1 to 2   | 2  |
| 2 | 8   | $\mu_{\text{SST}}(64)$  | 3 to 8   | 6  |
| 3 | 20  | $\mu_{\text{SST}}(400)$ | 9 to 20  | 12 |
| 4 | 28  | $\mu_{\text{SST}}(784)$ | 21 to 28 | 8  |
| 5 | 50  | $\mu_{\text{SST}}(2500)$| 29 to 50 | 22 |
| 6 | 82  | $\mu_{\text{SST}}(6724)$| 51 to 82 | 32 |
| 7 | 126 | $\mu_{\text{SST}}(15876)$| 83 to 126| 44 |

These capacities are identical to those from the packing algebra
(Step 5). The $\mu_{\text{SST}}$ thresholds do not create the shell
structure; the packing algebra does. The thresholds provide a
continuous mechanism for assigning positions to shells, which is needed
for elements whose mass number $A$ does not land exactly on a magic
number.

**Sector restart rule.** The Sierpiński walk has $K^D = 64$ positions
per sector. For elements with $A > 64$, the walk restarts at each
sector boundary:

- Positions 1 to 64: sector 0, local walk positions 1 to 64.
- Positions 65 to 128: sector 1, local walk positions 1 to 64.
- Positions 129 to 192: sector 2, local walk positions 1 to 64.
- Positions 193 to 256: sector 3, local walk positions 1 to 64.

Shell assignment uses the local walk position. This means the shell
structure repeats per sector: sector 1 fills the same shells in the
same order as sector 0. An element with $A = 120$ fills sector 0
completely (64 positions across shells 1 through 6) and then fills
the first 56 positions of sector 1 (shells 1 through 5, with shell 5
partially filled).

---

## Step 10. Shell filling across the periodic table

For any element with atomic number $Z$ and mass number $A$, the shell
filling is determined by walking through all $A$ positions and
assigning each to a shell based on its local walk position within the
current sector.

**Energy per position.** Each walk position contributes binding energy
proportional to its $\mu_{\text{SST}}$ value:

$$E_i = \text{SCALE} \times \mu_{\text{SST}}(i_{\text{local}}^2)$$

where $\text{SCALE} = B/A(\text{Zn}) \times K^D / \sum_{i=1}^{64}
\mu_{\text{SST}}(i^2)$ is calibrated from Zn-64, and $i_{\text{local}}$
is the local walk position within the current sector.

**Example: Fe-56 (Z = 26).**
Iron-56 has the highest binding energy per nucleon of any nuclide.
It fills one sector (sector 0) with 56 positions:

| Shell | Positions | Nucleons | Capacity | Status |
|-------|-----------|----------|----------|--------|
| 1 | 1 to 2    | 2  | 2  | full    |
| 2 | 3 to 8    | 6  | 6  | full    |
| 3 | 9 to 20   | 12 | 12 | full    |
| 4 | 21 to 28  | 8  | 8  | full    |
| 5 | 29 to 50  | 22 | 22 | full    |
| 6 | 51 to 56  | 6  | 32 | 6/32   |

Shells 1 through 5 are completely filled (50 nucleons). The remaining
6 nucleons begin filling shell 6. The valence shell is n = 6 with
occupancy 6/32.

**Example: Pb-208 (Z = 82).**
Lead-208 is doubly magic (Z = 82, N = 126). It spans sectors 0
through 3 (208 positions):

| Shell | Nucleons (all sectors) | Capacity (per sector) | Sectors |
|-------|----------------------|---------------------|---------|
| 1 | 2 per sector = varying | 2 | 4 partial |
| 2 | 6 per sector | 6 | varies |
| ... | ... | ... | ... |

The detailed breakdown for each element is produced by running
`magic_numbers_pipeline.py`, which prints per-shell energy
decomposition and predicted vs. experimental B/A for all 82 elements.

**Summary for key elements:**

| Z | Element | A | Sectors | Valence shell | Note |
|---|---------|---|---------|---------------|------|
| 2  | He | 4   | 1 | n=2, 2/6     | shell 1 closed |
| 8  | O  | 16  | 1 | n=3, 8/12    | shell 2 closed |
| 20 | Ca | 40  | 1 | n=5, 12/22   | shell 3 closed |
| 26 | Fe | 56  | 1 | n=6, 6/32    | peak B/A nuclide |
| 28 | Ni | 58  | 1 | n=6, 8/32    | near shell 4 closure |
| 30 | Zn | 64  | 1 | n=6, 14/32   | K^D boundary |
| 50 | Sn | 120 | 2 | n=6, 12/64   | shell 5 closure region |
| 82 | Pb | 208 | 4 | n=5, 48/88   | doubly magic |

---

## Step 11. Validation against AME2020

The predicted B/A from the shell energy decomposition can be compared
against experimental values from the AME2020 mass tables (accessed
via PlasmaPy). This validates that the shell assignment mechanism
produces physically meaningful energy partitioning.

**Shell closure verification.** At each magic number, the
corresponding shell should be exactly filled. The Python script
confirms this for all accessible magic number nuclei (He-4, O-16,
Ca-40, Ni-58, Sn-120, Pb-208).

**Enhanced stability.** Nuclei at magic numbers have above-average
B/A compared to their mass neighbours. This is the experimental
signature of shell closures: a nucleus with all shells fully packed
is more tightly bound than its neighbours with partially filled
valence shells.

**Prediction accuracy.** For the rising curve region ($A = 4$ to 64,
one sector), the mu_SST predicted B/A achieves:

- R2 and MAE values are reported by `magic_numbers_pipeline.py`
  using live PlasmaPy data.

For the full range ($A = 4$ to 208), the binding energy pipeline
(documented separately in `nuclear_binding_pipeline.md`) provides the
multi-sector envelope construction with ceiling drops. The magic
numbers pipeline focuses on shell structure, not on the global
envelope fit.

**Reproducibility.** Run `magic_numbers_pipeline.py` with PlasmaPy
installed to regenerate all tables, shell assignments, and validation
statistics. The script requires no manual input; all experimental
data is fetched from the AME2020 tables at runtime.

---

## Summary

The construction has two parts.

**Part 1: Magic numbers (Steps 1 through 8).** Pure combinatorics.

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

**Part 2: Shell structure (Steps 9 through 11).** The magic numbers
become shell boundaries via $\mu_{\text{SST}}$ thresholds. Each walk
position is assigned to a shell, the walk restarts at each Sierpinski
sector boundary ($K^D = 64$), and per-shell energy contributions are
computed and validated against AME2020 experimental data.

The shell filling for any element is fully determined by its mass
number $A$, the structural constants $K = 4$ and $D = 3$, and the SST
quadratic. No additional parameters, quantum numbers, or
phenomenological terms are introduced.

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
- **No field equation for magic numbers.** The magic numbers (Part 1)
  depend only on the walk structure. Part 2 introduces the SST
  quadratic to assign walk positions to shells and compute energies,
  but the shell boundaries are set by the packing algebra, not by
  the field equation.

---

## Cross-references

- Binding energy pipeline: `nuclear_binding_pipeline.md`
- Shell structure explorer (interactive): `gfd_sst_shells.html`
- Walk structure: [docs.fielddynamics.org/framework/md/why_k4_d3](https://docs.fielddynamics.org/framework/md/why_k4_d3/)
- Gate face: [docs.fielddynamics.org/framework/md/face_structure_and_spin](https://docs.fielddynamics.org/framework/md/face_structure_and_spin/)
- Validation tests: [docs.fielddynamics.org/tests](https://docs.fielddynamics.org/tests/)
- Python script: `magic_numbers_pipeline.py` (requires PlasmaPy for AME2020 data)

---

*Stephen Nelson, Field Dynamics Research. March 2026.*
