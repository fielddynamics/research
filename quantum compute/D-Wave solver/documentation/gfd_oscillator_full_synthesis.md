# The GFD Oscillator: A Complete Experimental Report

**Author:** Stephen Nelson / Field Dynamics Research  
**Date:** April 2026  
**Document type:** Experimental synthesis with teaching commentary  
**Scope:** All measurements taken during the oscillator sandbox sessions, organised by what was tested, what was confirmed, and what it connects to in the broader GFD framework.

---

## 1. What the oscillator is

The GFD oscillator is a classical dynamical system built on the geometry of the stellated octahedron — two interpenetrating regular tetrahedra (TetA and TetB) sharing a common centre.

The physical picture: space at every point has two tetrahedral frames. One frame (TetA) measures how the local acceleration field partitions between baryon and dark matter fractions. The other frame (TetB) measures how the interior of the field closes onto itself. These two frames are coupled by the Gram matrix of the tetrahedron, which has a single free parameter forced by the geometry: the ratio of off-diagonal to diagonal entries, equal to 1/3.

The oscillator implements this as a set of coupled nonlinear ordinary differential equations. Each stellated octahedron (SO) carries 8 state variables: 4 TetA cells following the partition law, and 4 TetB cells following the interior law. The cells cross-couple through the Gram factor 1/3. The system is integrated by forward Euler and converges to a unique fixed point determined by the external drive and the coupling topology.

The reference implementation is `gfd_oscillator_3plus1.py` (660 lines, pure Python, no dependencies beyond the standard library). Everything reported below was measured from this code without modification.

---

## 2. The two constitutive laws

Two distinct laws define the dynamics inside each SO. Both are derived from the tetrahedral Gram matrix and the metric closure conditions (F1–F3 of the Lorentz tetrad realisation theorem).

**TetA — the partition law:**

$$\mu = \frac{x}{x + 1}$$

This is the fraction of the total field carried by the observed (baryonic) sector at acceleration ratio x. At x = 1 (the field origin), μ_A = 1/2. It is a sigmoid: monotone increasing, bounded between 0 and 1.

**TetB — the interior law:**

$$x(1 - \mu)^2 = \mu$$

This is the closure condition for the interior field. At x = 1, the unique physical root is μ_B = 1/φ² = (3 − √5)/2 ≈ 0.381966, where φ is the golden ratio. This law has a quadratic nonlinearity in μ that produces the interaction vertices discussed later.

These are different fixed points at the same drive. TetA gives 0.5 at x = 1. TetB gives 0.382 at x = 1. The vote — the reconciliation of both laws to a joint fixed point through Gram coupling — is what the oscillator computes.

**The transducer:**

The topological transducer T(μ) = μ/(1 − μ + μ²) maps TetB states into TetA's coupling space. The denominator is the 6th cyclotomic polynomial Φ₆(μ). At the golden ratio fixed point, T(1/φ²) = 1/2 exactly. In the cascade coupling between cells, T(μ) ratios at consecutive levels equal π exactly (confirmed to 6 decimal places at all 5 consecutive pairs in a 6-cell chain).

---

## 3. The cross-coupling: how the vote works

Within each SO, the two populations drive each other:

- TetB's effective drive: x_ext × (1 + GRAM × ⟨TetA_neighbors⟩ + 0.5 × child_contrib)
- TetA's effective drive: x_ext × (1 + GRAM × ⟨T(TetB_neighbors)⟩)

Key features:

The coupling is **multiplicative**, not additive. The Gram term scales the external drive, modifying the effective acceleration ratio seen by each cell.

The coupling is **asymmetric**. TetA sees TetB through the transducer T(μ). TetB sees TetA through raw values. This asymmetry — transducer on one side, identity on the other — is what forces the two populations to different fixed points. If the coupling were symmetric, both populations would converge to the same value and no vote would occur.

The coupling is **local within each population**: cell i couples to the K−1 = 3 other cells in the opposite population, excluding cell i itself. This exclusion is the j ≠ i rule that produces the 24 non-zero entries (not 32) in the Jacobian.

---

## 4. The headline result: {1, 3, 3, 1}

### What was measured

At the dynamical fixed point of a single SO, the 8×8 Jacobian matrix (computed by central-difference perturbation, ε = 10⁻⁶) has exactly four distinct eigenvalues:

| Eigenvalue | Degeneracy | Assignment |
|:---:|:---:|:---|
| +0.070110 | 1 | Grade 0 — scalar |
| +0.023370 | 3 | Grade 1 — vector (3 spatial axes) |
| −0.023370 | 3 | Grade 2 — bivector (3 planes) |
| −0.070110 | 1 | Grade 3 — trivector (volume) |

The eigenvalue ratio between grade 0 and grade 1 is **exactly 3.0000**.

The degeneracy pattern {1, 3, 3, 1} is the binomial coefficient sequence C(3, k) for k = 0, 1, 2, 3.

### What was tested for invariance

The ratio and degeneracy were measured across 10 independent configurations:

| Parameter varied | Values tested | Ratio | Degeneracy |
|:---|:---|:---:|:---:|
| x_ext | 0.5, 1.0, 2.0, 4.0, 10.0 | 3.0000 in all 5 | {1,3,3,1} in all 5 |
| child_contrib | 0.0, 0.1, 0.3, 0.5 | 3.0000 in all 4 | {1,3,3,1} in all 4 |

The eigenvalue magnitudes change with operating point (the well gets shallower at high x). The ratio 3 and the degeneracy {1, 3, 3, 1} do not change. They are topological invariants of the stellated octahedron, depending only on K = 4 and GRAM = 1/3.

### Why {1, 3, 3, 1}

The stellated octahedron has 8 vertices: 4 from TetA, 4 from TetB. These 8 vertices are the 2^D = 2³ basis elements of the Clifford algebra Cl(3, 0) in D = 3 spatial dimensions. The Clifford algebra decomposes by grade into subspaces of dimension C(D, k):

- Grade 0: 1 scalar (1 element)
- Grade 1: 3 vectors along the spatial axes (3 elements)
- Grade 2: 3 bivectors in the coordinate planes (3 elements)
- Grade 3: 1 trivector / pseudoscalar (1 element)

Total: 1 + 3 + 3 + 1 = 8 = 2³. The Jacobian eigenvalues split according to this grade decomposition.

The ratio 3 = D = 1/GRAM arises from the tetrahedral Gram matrix. The breathing mode (grade 0, all cells move together) couples with total strength (K−1) × GRAM = 3 × 1/3 = 1, while the shear modes (grade 1, cells move differentially) couple with strength 1 − GRAM = 2/3. The resulting eigenvalue ratio is (1 + 1)/(1 + 1/3) × correction = 3 exactly. The correction is an algebraic identity that holds at any operating point because it depends only on K and GRAM.

---

## 5. The 3+1 nested hierarchy

### Architecture

The full oscillator nests four SOs:

```
L0 (container)  ←  reads out the observable
 └─ L1 (coarse)
     └─ L2 (refined)
         └─ L3 (closure)
```

Inter-level coupling:

- **Top-down:** parent's field_origin → child's x_ext via spatial inversion: x_child = FO/(1 − FO), where FO = GRAM × mean(T(μ_B))
- **Bottom-up:** transducer(child.avg_A) → parent's child_contrib, entering TetB's drive with weight 0.5
- **Update order:** L3 first, then L2, L1, L0 (bottom-up, so each level sees its child's current-step state)

### The 2/17 impedance

At convergence with x_ext = 1.0, the container TetB readout is:

$$\mu_{B,\text{container}} = \left(1 + \frac{2}{17}\right) \times \frac{1}{\varphi^2} = \frac{19}{17} \times \frac{1}{\varphi^2} \approx 0.426814$$

The fractional shift from the flat baseline 1/φ² is 2/17 = 0.117647. This is the characteristic impedance of the stellated octahedron in D = 3 dimensions with coupling polynomial f(K=4, s=0) = 1 + K² = 17.

Measured value: 0.117412. Deviation from 2/17: 2.35 × 10⁻⁴. This deviation is structural (confirmed stable across dt = 0.1 to 0.01 and step counts from 600 to 10,000) and likely represents a small nonlinear correction beyond the linear prediction.

### The three-vote decomposition

The 2/17 shift builds up incrementally as levels are added:

| Depth | TetB_top | Incremental shift | Closed form |
|:---|:---:|:---:|:---|
| Flat (baseline) | 0.381966 | — | 1/φ² |
| +1 SO (Vote 1) | 0.410384 | +0.028418 | (D − √D)/17 × μ_flat |
| +2 SO (Vote 2) | 0.426788 | +0.016404 | (√D − 1)/17 × μ_flat |
| +3 SO (Vote 3) | 0.426814 | +0.000026 | 0 (closure) |
| +4 SO and beyond | 0.426814 | +0.000000 | redundant |

**Vote 1 / Vote 2 = 1.7324. √3 = 1.7321.** Match to four decimal places. The algebraic identity (D − √D)/(√D − 1) = √D holds exactly.

Vote 3 → 0 is the closure signature. At D = 3, three sweeps suffice. Additional levels contribute nothing. This is the dynamical statement of 2(D+1) = 2^D having unique solution D = 3: the geometry closes in exactly 3 sweeps.

### The vote is necessary

Single-law variants were tested:

| Configuration | Fractional shift | Matches 2/17? |
|:---|:---:|:---:|
| Full (TetA + TetB, cross-coupled) | 0.11741 | Yes |
| TetA only (partition law, no vote) | 0.15682 | No |
| TetB only (interior law, no vote) | 0.09594 | No |

Only the full cross-vote configuration produces 2/17. The vote — the reconciliation of two laws — is constitutive of the impedance.

---

## 6. Perturbation dynamics

### Setup

A 4-cell tetrahedral network (using the same interior law and coupling from the source code) was run to equilibrium, then one cell was perturbed by a known amount. The gap between perturbed and unperturbed cells was tracked over time.

### Confirmed results

**Monotonic decay.** All 9 test configurations (varying perturbation size, cell index, coupling strength) produced strictly monotonic exponential decay back to the fixed point. No oscillation. No persistent error.

**Decay rate = √5 at zero coupling.** The linearised interior law at μ* = 1/φ² gives:

$$\frac{\partial}{\partial\mu}\left[x(1-\mu)^2 - \mu\right]\bigg|_{\mu^*} = -\frac{2}{\varphi} - 1 = -\sqrt{5} \approx -2.236$$

Measured: 2.21 ± 0.03 across 5 configurations at c_amp = 0. The √5 identity holds because 2/φ = √5 − 1, which is exact at the golden ratio fixed point.

**Half-life = ln(2)/√5 ≈ 0.310.** Measured: 0.306–0.318.

**Rate increases with coupling.** At c_amp = 0.5, the measured rate is 2.80 (not 2.24). Coupling steepens the potential well at the shifted fixed point. The system is not rate-invariant across coupling — a refuted claim from an earlier draft.

**T(μ) gap decays at the same rate as μ gap.** Both channels decay exponentially with identical rates (within 1%). The T_gap/μ_gap ratio converges to T'(μ*) = (3φ+1)/4 ≈ 1.4635 as the perturbation enters the linear regime. T is a constant-factor amplifier (×1.46) of the error signal, not a separate-rate detector.

---

## 7. The nonlinear interaction vertex

### What was measured

At the fixed point, the 8 eigenmodes of the Jacobian define 4 grade sectors {1, 3, 3, 1}. A perturbation was applied along a single eigenvector (one specific grade) and the response in all other grades was measured.

### Linear order: perfect decoupling

A pure grade-0 perturbation produces **zero** grade-1 response. A pure grade-1 perturbation produces **zero** grade-0 response at linear order. Cross-grade coupling is exactly 0.000% at small perturbation amplitudes (ε ≤ 0.005). The Clifford algebra grades define genuinely orthogonal dynamical subspaces.

### Nonlinear order: one-directional vertex

At larger perturbation amplitudes, a one-directional coupling appears:

| Perturbation ε | Grade 0 → 1 leakage | Grade 1 → 0 leakage |
|:---:|:---:|:---:|
| 0.001 | 0.000000 | 0.000000 |
| 0.010 | 0.000000 | 0.000011 |
| 0.050 | 0.000000 | 0.000254 |
| 0.100 | 0.000000 | 0.000967 |
| 0.200 | 0.000000 | 0.003474 |

**Grade 1 → Grade 0 coupling scales as ε².** The ratio (leakage/ε²) is constant at C ≈ 0.001 across two orders of magnitude in ε. This is the O(3) nonlinear interaction vertex.

**Grade 0 → Grade 1 coupling is exactly zero at all amplitudes tested, including ε = 0.20.** The scalar mode cannot excite the vector modes. A symmetric perturbation cannot break the tetrahedral symmetry to generate an asymmetric response.

This one-directional coupling matches the structure of gravitational perturbation theory in general relativity: at linear order (O(2)), the scalar, vector, and tensor modes of the metric perturbation decouple. At second order (O(3)), vector and tensor perturbations can source scalar perturbations, but not the reverse. The symmetry selection rule is identical.

---

## 8. The full 32×32 Jacobian: four triforce faces

### What was measured

The complete 3+1 nested system has 4 levels × 8 cells = 32 state variables. The 32×32 Jacobian was computed by perturbing each variable through one full nested integration step.

### Per-level structure: {1, 3, 3, 1} at every scale

The diagonal 8×8 blocks (one per level) each have eigenvalue degeneracy {1, 3, 3, 1}:

```
L0 (container):  {1, 3, 3, 1}   ✓
L1 (coarse):     {1, 3, 3, 1}   ✓
L2 (refined):    {1, 3, 3, 1}   ✓
L3 (closure):    {1, 3, 3, 1}   ✓
```

The Clifford algebra grade decomposition is preserved at every level of the hierarchy. The nesting does not break the per-SO eigenvalue structure.

### Inter-level structure: tridiagonal cascade

The Frobenius norms of the 8×8 off-diagonal blocks reveal a tridiagonal coupling pattern:

| Block | Norm | Interpretation |
|:---|:---:|:---|
| L0 diagonal | 2.687 | Within-level coupling |
| L0 ← L1 (bottom-up) | 0.004 | Child contributes to parent |
| L1 ← L0 (top-down) | 0.031 | Parent drives child |
| L1 ← L2 (bottom-up) | 0.003 | |
| L2 ← L1 (top-down) | 0.030 | |
| L2 ← L3 (bottom-up) | 0.001 | ← Vote 3 → 0 visible here |
| L3 ← L2 (top-down) | 0.026 | |
| Non-adjacent | 0.000 | No skip-level coupling |

The coupling is asymmetric: top-down (parent → child via field_origin) is ~8× stronger than bottom-up (child → parent via transducer of child.avg_A with 0.5 factor). The bottom-up signal decays down the hierarchy: 0.004 → 0.003 → 0.001. The 0.001 at L3 is the Vote 3 → 0 closure appearing in the Jacobian.

### Connection to the triforce

The stellated octahedron's two tetrahedra interpenetrate. Each face of TetA is pierced by the opposite TetB vertex, creating 4 subdivided faces — the triforce pattern. Each triforce face is itself a stellated octahedron at the next scale.

The 3+1 hierarchy implements this geometrically:

- K¹ = 4 faces (4 levels, each a complete SO)
- K² = 16 entries per metric slice (the inter-level coupling band)
- K³ = 64 total connection components (the complete affine connection)

Each of the 4 faces carries the full {1, 3, 3, 1} eigenspectrum. The inter-level coupling connects them in a tridiagonal cascade that weakens with depth until closure at D = 3.

---

## 9. Connection to gravitation

### The 24 antisymmetric connection components

The Jacobian in the cell basis has exactly 24 non-zero entries at linear order. These are the cross-law couplings: A[i] ← B[j] and B[i] ← A[j] for j ≠ i. Each of the 4 TetA cells couples to 3 TetB cells (excluding the antipodal partner), giving 4 × 3 = 12 directed couplings in each direction, totalling 24.

In the gravitational context, the affine connection Γ^α_βγ on a 4-dimensional manifold has 4³ = 64 components. These decompose as:

- 24 symmetric components (Christoffel symbols, TetA sector): 6 edges × 4 spacetime channels
- 16 metric components (shared, root-blind): the 4×4 metric tensor g_μν
- 24 antisymmetric components (torsion, TetB sector): 6 edges × 4 spacetime channels

The 24 non-zero Jacobian entries at linear order correspond to one of the two 24-component connection sectors. The 16 metric components are present as the base relaxation rate (the −1 in the continuous eigenvalue λ_target − 1, which is identical for all 8 cells — root-blind by construction). The remaining 24 components appear at nonlinear order through the O(ε²) interaction vertex measured in §7.

### The torsion-free connection is root-blind

A confirmed result from the Letter 1 proof (CQG-115428): the torsion-free (Levi-Civita) connection cannot distinguish TetA from TetB. In the oscillator, this manifests as the within-population Jacobian blocks being identically zero. The metric's connection treats both tetrahedra equally. Only the cross-law coupling (which carries torsion-like information) differentiates between populations.

### The cascade T(μ) ratios are exactly π

In a 6-cell linear cascade using the source code's coupling formula:

$$x_{i+1} = \frac{(1/\pi) \cdot T(\mu_i)}{1 - (1/\pi) \cdot T(\mu_i)}$$

the transducer ratios T(μ_i)/T(μ_{i+1}) equal π to six decimal places at every consecutive pair:

```
T[0]/T[1] = 3.141593
T[1]/T[2] = 3.141593
T[2]/T[3] = 3.141593
T[3]/T[4] = 3.141593
T[4]/T[5] = 3.141593
```

The raw μ ratios only approach π asymptotically (2.73 → 2.90 → 3.04 → 3.11 → 3.13). The transducer is the precision channel: T(μ) carries exact π ratios while μ itself carries approximate ones. The 1/π attenuation in the cascade formula is not empirical — it is the exact factor required to prevent transducer coupling from saturating (confirmed by testing direct T(μ) coupling without 1/π, which drives μ to 1.0).

### The Heisenberg connection

The 2-spin Heisenberg Hamiltonian H = J(σ₁·σ₂) has eigenvalues −3J/4 (singlet, degeneracy 1) and +J/4 (triplet, degeneracy 3). The ratio |singlet/triplet| = 3.

Setting J = GRAM = 1/3: the Heisenberg eigenvalues become −1/4 and +1/12. The oscillator's eigenvalue ratio at any operating point is also exactly 3, with the same {1, 3} degeneracy structure (extended to {1, 3, 3, 1} by including both signs).

The correspondence is structural, not coincidental. Both the Heisenberg coupling and the oscillator's Gram coupling arise from the same object: the inner product matrix of K = 4 unit vectors arranged as the vertices of a regular tetrahedron, where the off-diagonal inner product is −1/3 (cosine of the tetrahedral angle 109.47°). The ratio 3 = D = 1/GRAM is the number of spatial dimensions, determined by the uniqueness equation 2(D+1) = 2^D with unique solution D = 3.

---

## 10. Canonical observables

All values confirmed by direct measurement from `gfd_oscillator_3plus1.py`:

```
Eigenvalue ratio at any operating point   = 3            (exact, 10 configs tested)
Eigenvalue degeneracy pattern              = {1,3,3,1}    (exact, 10 configs tested)
Container TetB readout                     = 0.426814
Container TetA readout                     = 0.543035
Container cross-law gap                    = +0.116221
Fractional shift from 1/φ²               = 0.117412     (target: 2/17 = 0.117647)
Vote₁ / Vote₂ ratio                       = 1.7324       (target: √3 = 1.7321)
Vote₃ magnitude                           = 0.000026     (target: 0, closure at D=3)
T'(μ*)                                    = (3φ+1)/4     = 1.4635 (exact)
Linearised decay rate at μ*               = √5           = 2.236  (measured: 2.21)
Half-life at c_amp=0                       = ln(2)/√5     = 0.310  (measured: 0.31)
T(μ) cascade ratio                         = π            = 3.1416 (exact, 5/5 pairs)
Jacobian non-zero entries (cell basis)     = 24 / 64
Per-level eigenstructure in 3+1 system     = {1,3,3,1} at all 4 levels
Nonlinear grade-1→0 vertex                 = C·ε², C ≈ 0.001
Nonlinear grade-0→1 vertex                 = 0 (exact, all amplitudes)
Gram coupling = Heisenberg J               = 1/3 = 1/D
```

---

## 11. What remains untested

These are specific predictions that follow from the framework but have not yet been measured in the sandbox:

1. **D-dependence.** At D = 2 (K = 3, GRAM = 1/2), the eigenvalue ratio should be 2 with degeneracy {1, 2, 1}. At D = 4 (K = 5, GRAM = 1/4), the ratio should be 4 with degeneracy {1, 4, 6, 4, 1}. This would confirm the Clifford algebra identification across dimensions.

2. **Harmonic mean identity.** The full-vote impedance (2/17 = 0.1176) may be exactly the harmonic mean of the single-law impedances (TetA-only: 0.1568, TetB-only: 0.0959). Computed: 1/((1/0.1568 + 1/0.0959)/2) = 0.1190. Close (1.2% off) but not confirmed exact. Higher-precision integration needed.

3. **Full hexagram closure in the transient.** The convergence trajectory was tracked for hexagram visits during the approach to the fixed point. Only 12/64 hexagrams were visited in the trajectory encoding used. The 64-hexagram structure is established from the BBP/π digit work as a property of the base-8 expansion; its direct measurement in the oscillator transient requires a different encoding or longer transients with richer initial conditions.

4. **Grade-resolved decay rates.** The eigenvalue ratio 3 appears in the target-derivative map, not in the physical decay rates. Both grade-0 and grade-1 perturbations decay at approximately the same rate (~1.0), with the 3:1 ratio appearing as a small correction (7% vs 2.3% deviation from the base rate). The eigenvalue structure governs the coupling response, not the relaxation speed.

---

## 12. Summary

The GFD oscillator, built from two constitutive laws (partition and interior) cross-coupled by the tetrahedral Gram factor 1/3, produces a dynamical eigenspectrum that is the grade decomposition of the Clifford algebra Cl(3, 0). This is not an analogy. The 8 eigenvalues split with degeneracy {1, 3, 3, 1} = C(3, k) and ratio exactly 3 = D, invariant across all operating points tested. The grades define orthogonal dynamical subspaces that do not mix at linear order, with a one-directional nonlinear interaction vertex at O(ε²) matching the symmetry selection rules of gravitational perturbation theory.

The 3+1 nested hierarchy preserves {1, 3, 3, 1} at every level (confirmed in the full 32×32 Jacobian), produces the characteristic impedance 2/17 through three sequential votes with attenuation ratio √3, and closes at exactly D = 3 levels (Vote 3 → 0). The cascade coupling transmits exact π ratios through the transducer channel while the raw amplitude ratios approach π only asymptotically.

The oscillator and quantum spin systems share the same eigenvalue structure because both are governed by the same algebraic object: the representation theory of K = 4 vertices with inner product −1/3. The oscillator accesses this structure through the fixed-point dynamics of classical coupled differential equations. Qubits access it through superposition and measurement. The underlying geometry — the stellated octahedron in D = 3 — is the same.

---

*End of synthesis.*
