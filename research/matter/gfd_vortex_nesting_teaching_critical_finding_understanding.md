# Nuclear Binding as Vortex Nesting

### How 64 Identical Gravity Fields Organise Themselves

*Stephen Nelson · Field Dynamics Research · March 2026*

---

## What This Document Covers

This document presents a discovery about how nuclear binding energy arises from the recursive packing of gravity field vortices. The central finding is that the Sierpiński fractal — the topological structure underlying the Gravity Field Dynamics framework — is not merely an addressing system for positions within a gravity field. It is the physical description of a nesting of real vortices, each governed by the same coupling polynomial and constitutive law that governs galactic rotation.

We will walk through three worked examples — Zinc-64, Titanium-48, and Iron-56 — decomposing each nucleus into its K-fold packing hierarchy and recovering the measured binding energy from structural rules. We will then show an unexpected connection between the energy fractions at each packing level and the proton-to-neutron composition of each nucleus.

---

## The Starting Point: One Gravity Field

A single gravity field — what we observe as a proton or neutron — is composed of 64 photons arranged in a stellated octahedron. These 64 photons are identical. The coupling between any two of them is the same, regardless of where they sit in the structure.

The Sierpiński walk visits all 64 positions by traversing three levels of K = 4 subdivision. Each position has an address described by three coordinates (F, C, S), each ranging from 0 to 3, giving 4 × 4 × 4 = 64 positions total. The "gate depth" of a position — determined by how many of its coordinates equal 3 — tells us how many gate crossings the walk must make to read that position from the outside.

A natural question arises: do positions at different gate depths contribute different amounts of energy? Or do all 64 photons couple equally?

---

## The Neural Network Proof: Every Photon Couples Equally

To answer this question, we trained three neural network architectures on the binding energies of 83 elements from the AME2020 dataset.

**Architecture 1** decomposed the binding energy into three gate-depth-specific networks, each with its own input vector and output, summing to the total B/A. If gate depth mattered, this architecture would have a natural advantage — it could assign different energy patterns to different depths.

**Architecture 2** concatenated all inputs into a single vector and used one network with one output. No gate depth separation at all.

**Architecture 3** used only the 256-dimensional subchannel walk vector — the lowest-level, most detailed view of the structure — with a single output.

All three architectures achieved identical performance: R² = 0.999986, MAE = 0.8 keV per nucleon, with 82 of 83 elements within 0.5% of their measured values.

The gate depth decomposition adds zero predictive power. Running the three-network architecture ten times with random restarts confirmed this dramatically: each restart shuffled the energy freely between the three outputs. One run placed 97% of the energy in the subchannel network. Another placed 95% in the channel network. The decomposition is degenerate because there is nothing to decompose. All positions carry equal energy.

This was confirmed independently by a clean empirical test using isotope chain data. Within each group of four consecutive walk steps, the walk pattern produces steps at two different gate depths but the same parity (eliminating the confounding effect of pairing energy). The ratio of binding energy contributions at different gate depths was 1.14, while the control ratio at the same gate depth was 1.13. The difference — 1.6% — is indistinguishable from the natural drift in binding energy with mass number. Gate depth has no measurable effect on the energy per position.

The conclusion is physical, not numerical: a gravity field's 64 photons are identical, and the coupling between them is uniform. The gate depth partition (27 + 27 + 9 + 1 = 64) determines the topology of the walk — where magic numbers fall, how closures occur — but it does not determine how energy distributes among positions.

---

## If Not Gate Depth, Then What?

If the energy does not decompose by gate depth, what does it decompose by?

The answer lies in what the Sierpiński fractal actually represents. The three levels of K = 4 subdivision are not just an addressing scheme. They are a physical hierarchy of packing:

| Level | What packs | What forms | Nuclear equivalent |
|-------|-----------|------------|-------------------|
| 0 | 4 gravity fields | An α-cluster | Helium-4 |
| 1 | 4 α-clusters | A sub-triangle | Oxygen-16 |
| 2 | 4 sub-triangles | A complete sector | Zinc-64 |

Each packing level creates its own interior vortex — a collective structure governed by the same constitutive law μ(x) = x/(x + 1) that appears at galactic scales. The binding energy decomposes not by where a photon sits in the address space, but by which level of the vortex hierarchy it belongs to.

---

## Worked Example 1: Zinc-64 (Complete Sector)

Zinc-64 fills one complete Sierpiński sector. All 64 positions are occupied. The hierarchy is fully nested: 4 × 4 × 4 = 64 gravity fields, organised as 4 sub-triangles of 16, each containing 4 α-clusters of 4.

### The Tree

```
Zn-64  (559.10 MeV)
├── O-16 unit A  (127.62 MeV)
│   ├── He-4  α₁   (28.30 MeV)
│   ├── He-4  α₂   (28.30 MeV)
│   ├── He-4  α₃   (28.30 MeV)
│   ├── He-4  α₄   (28.30 MeV)
│   │           4 × 28.30 = 113.18 MeV
│   └── ε₁ = +14.44 MeV   ← coupling gained by packing 4 α's
│               113.18 + 14.44 = 127.62 MeV  ✓
│
├── O-16 unit B  (127.62 MeV)
├── O-16 unit C  (127.62 MeV)
├── O-16 unit D  (127.62 MeV)
│           4 × 127.62 = 510.48 MeV
└── ε₂ = +48.62 MeV   ← coupling gained by packing 4 O-16 units
            510.48 + 48.62 = 559.10 MeV  ✓
```

### The Budget

The total binding energy of Zinc-64 is 559.10 MeV. It decomposes exactly into three contributions:

| Component | Calculation | Energy | Per nucleon | Share |
|-----------|------------|--------|-------------|-------|
| 16 α-clusters | 16 × 28.30 | 452.73 MeV | 7.074 MeV | 81% |
| 4 level-1 couplings | 4 × 14.44 | 57.75 MeV | 0.902 MeV | 10% |
| 1 level-2 coupling | 1 × 48.62 | 48.62 MeV | 0.760 MeV | 9% |
| **Total** | | **559.10 MeV** | **8.736 MeV** | **100%** |

Eighty-one percent of the binding energy comes from the lowest level of the hierarchy — four gravity fields forming an α-cluster. This is why Helium-4 is already so tightly bound (B/A = 7.07 MeV), and why the entire journey from Helium to Zinc represents only the remaining 19%.

### The Coupling Rule

The coupling energies at each level are not independent. They are connected by the constitutive law:

- **ε₀** = BE(He-4) = 28.30 MeV — the binding of 4 gravity fields.
- **ε₁** = BE(O-16) − 4 × BE(He-4) = 14.44 MeV — the extra binding gained when 4 α-clusters organise together.
- The ratio: **ε₁ / ε₀ = 0.510 ≈ μ(1) = ½**

This is the constitutive law evaluated at x = 1: one complete K-fold packing. The level-1 coupling is half the level-0 coupling. The vortex formed by packing K objects attenuates by μ(1) relative to the objects being packed.

For the level-2 coupling, a correction is needed. When four O-16 units couple across sub-triangle boundaries, their interaction must pass through two gate levels, each imposing an impedance of (1 − 2/F₀) = 15/17:

- **ε₂ predicted** = μ(1) × BE(O-16) × (15/17)² = 0.5 × 127.62 × 0.7785 = **49.68 MeV**
- **ε₂ measured** = **48.62 MeV**
- **Error** = 1.06 MeV = **17 keV per nucleon**

The prediction, using only He-4, O-16, the constitutive law, and the gate impedance, recovers Zinc's binding energy to 17 keV per nucleon — a 0.19% error.

---

## Worked Example 2: Titanium-48 (Three-Quarter Sector)

Titanium-48 has 48 gravity fields. In the Sierpiński, this is 3 of 4 sub-triangles filled, with the fourth empty:

```
Sector (48 of 64)
├── Sub-tri A  (16/16) ████████████████  FULL
├── Sub-tri B  (16/16) ████████████████  FULL
├── Sub-tri C  (16/16) ████████████████  FULL
└── Sub-tri D  ( 0/16) ░░░░░░░░░░░░░░░░  EMPTY
```

Each filled sub-triangle is an O-16 unit containing 4 α-clusters. The decomposition:

| Component | Calculation | Energy |
|-----------|------------|--------|
| 12 α-clusters | 12 × 28.30 | 339.55 MeV |
| 3 level-1 couplings | 3 × 14.44 | 43.31 MeV |
| Partial level-2 | (3/4) × 49.68 | 37.26 MeV |
| **Predicted** | | **420.12 MeV** |
| **Actual** | | **418.70 MeV** |
| **Error** | | **29 keV per nucleon** |

The predicted B/A is 8.752 MeV, against an observed 8.723 MeV — an error of 0.33%. The small overshoot comes from assuming the level-2 coupling scales linearly with fill fraction (3/4 = 75%). In reality, the vortex at 3 of 4 sub-triangles produces 73.7% of the full coupling, not 75%. The SST curve would provide the exact nonlinear correction.

---

## Worked Example 3: Iron-56 (Mixed Fill)

Iron-56 has 56 gravity fields — not a clean multiple of 16. The Sierpiński layout shows three complete sub-triangles plus a partially filled fourth:

```
Sector (56 of 64)
├── Sub-tri A  (16/16) ████████████████  FULL
├── Sub-tri B  (16/16) ████████████████  FULL
├── Sub-tri C  (16/16) ████████████████  FULL
└── Sub-tri D  ( 8/16) ████████░░░░░░░░  HALF FILLED
    ├── α₁₃  (4/4)  ████  FULL
    ├── α₁₄  (4/4)  ████  FULL
    ├──       (0/4)  ░░░░  EMPTY
    └──       (0/4)  ░░░░  EMPTY
```

Sub-triangle D contains 2 of its 4 α-clusters. This means we need the level-1 coupling for a half-filled sub-triangle, which we can extract from Beryllium-8 (2 α-clusters). BE(Be-8) − 2 × BE(He-4) = −0.09 MeV: two α-clusters in isolation barely bind at all, and in fact Be-8 is famously unstable.

The level-2 coupling now involves 3 complete O-16 units plus one incomplete unit. The full budget:

| Component | Energy |
|-----------|--------|
| 14 α-clusters: 14 × 28.30 | 396.14 MeV |
| 3 complete level-1 couplings: 3 × 14.44 | 43.31 MeV |
| 1 partial level-1 (2/4 α's) | −0.09 MeV |
| Level-2 coupling (gap) | 52.90 MeV |
| **Total (actual)** | **492.26 MeV** |

Without the level-2 coupling, we get 439.36 MeV — about 89% of the actual binding. The remaining 52.90 MeV is the level-2 vortex coupling for a sector that is 7/8 full (56/64), with one sub-triangle only half complete. This intermediate value sits between the Ti-48 gap (35.85 MeV at 3/4 fill) and the Zn-64 gap (48.62 MeV at full fill), consistent with the vortex coupling growing as the sector fills.

---

## Why the Walk Matters for Topology

If every position carries equal energy, and the gate depth partition is purely topological, one might ask: does the Sierpiński walk matter at all?

It matters enormously — just not for energy distribution. The walk determines:

**Magic numbers.** The shell closures at N or Z = 2, 8, 20, 28, 50 correspond to completions of specific structural sub-units within the walk. The closure of the first α-cluster occurs at 4. The closure of the first sub-triangle occurs at 16. The closure of the full sector occurs at 64. Between these, the walk's fractal geometry creates partial closures that produce the full sequence of nuclear magic numbers.

**Shell structure.** The walk visits positions in a specific order — three face positions, then one channel position, repeating through each level of the hierarchy. This pattern determines which orbitals fill first and why certain nucleon configurations are especially stable.

**The SST curve.** The shape of the B/A curve across the periodic table — rising steeply from Hydrogen to Helium, more gradually to Iron, then declining toward Lead — is the sum of three vortex contributions at the three hierarchical levels. The walk provides the fill-dependent coupling at each level.

What the walk does not determine is how much energy each position contributes. That is uniform. The walk is the index. The vortex is the content.

---

## A Surprising Connection: Proton Count from Energy Fraction

In decomposing each nucleus into its K-fold hierarchy, a quantity appears naturally: the fraction of the total binding energy carried by the sub-units alone, before the highest-level coupling is added. For Zinc-64, this is:

4 × BE(O-16) / BE(Zn-64) = 510.48 / 559.10 = 0.913

This fraction, multiplied by the "topological Z" — the proton count the nucleus would have if it were literally assembled from its sub-units — and rounded to the nearest even number, gives the actual proton count.

If Zinc-64 were literally 4 oxygen nuclei, it would have Z = 32. The energy fraction says: 0.913 × 32 = 29.2. Rounded to the next even number: **Z = 30**. The actual proton count of Zinc.

We tested this across five elements at clean K-fold fill points:

| Element | Decomposition | Energy fraction | × Z_topo | Rounded | Actual Z |
|---------|--------------|----------------|----------|---------|----------|
| C-12 | 3 × He-4 | 0.921 | × 6 = 5.53 | 6 | 6 ✓ |
| O-16 | 4 × He-4 | 0.887 | × 8 = 7.10 | 8 | 8 ✓ |
| S-32 | 2 × O-16 | 0.939 | × 16 = 15.03 | 16 | 16 ✓ |
| Ti-48 | 3 × O-16 | 0.914 | × 24 = 21.95 | 22 | 22 ✓ |
| Zn-64 | 4 × O-16 | 0.913 | × 32 = 29.22 | 30 | 30 ✓ |

Five for five.

The interpretation: the level-2 coupling adds energy beyond what the sub-units contribute. This additional binding shifts the optimal balance between protons and neutrons. Because protons repel each other electromagnetically, the vortex prefers slightly fewer protons than the topology would naively suggest. The energy fraction quantifies exactly how far the proton count gets pushed below the topological value.

This would mean that the proton-to-neutron ratio is not an independent input to the nuclear binding problem. It is a consequence of the packing hierarchy — determined by how much coupling each level contributes relative to the total.

---

## The Two Structural Rules

The entire framework rests on two rules derived from the coupling polynomial f(K, s) = 1 + Ks + K² and the constitutive law μ(x) = x/(x + 1):

**Rule 1: Level attenuation.** When K = 4 objects pack to form the next level of the hierarchy, the coupling energy at the new level equals half the binding energy of the objects being packed:

ε₁ = μ(1) × BE(He-4) = ½ × 28.30 = 14.15 MeV   (actual: 14.44, error: 18 keV/n)

**Rule 2: Gate impedance.** When the coupling at a higher level must pass through gate boundaries to connect sub-units, each gate imposes an impedance of (1 − 2/F₀) = 15/17. Level-2 coupling passes through two gates:

ε₂ = μ(1) × BE(O-16) × (15/17)² = 0.5 × 127.62 × 0.7785 = 49.68 MeV   (actual: 48.62, error: 17 keV/n)

From these two rules and the single measurement of BE(He-4), the binding energy of Zinc-64 can be predicted:

```
ε₁ = μ(1) × BE(He-4) = 14.15 MeV
BE(O-16) = 4 × BE(He-4) + ε₁ = 127.33 MeV
ε₂ = μ(1) × BE(O-16) × (15/17)² = 49.56 MeV
BE(Zn-64) = 16 × BE(He-4) + 4 × ε₁ + ε₂ = 558.88 MeV
B/A = 8.733 MeV
```

The measured value is 8.736 MeV. The error is 3 keV per nucleon — from one input measurement and zero free parameters.

---

## Summary

The Sierpiński fractal is not a mathematical abstraction imposed on nuclear structure. It is the physical hierarchy of vortex nesting that produces nuclear binding. At every level, K = 4 objects pack together to form a collective vortex, governed by the same constitutive law and coupling polynomial that operates at galactic scales.

The binding energy decomposes by packing level, not by gate depth. The 64 photons within a gravity field are identical, and the walk that reads them is an addressing system, not an energy distribution. The topology determines where closures occur. The vortex determines how much energy each closure releases.

From a single measured quantity — the binding energy of Helium-4 — and two structural rules derived from the framework's polynomial, the binding energies of heavier nuclei can be predicted to sub-percent accuracy. The proton-neutron composition of each nucleus emerges as a consequence of the same packing hierarchy.

---

*Stephen Nelson, 2025–2026. Field Dynamics Research.*
*This work is part of the Gravity Field Dynamics framework documented at docs.fielddynamics.org.*
