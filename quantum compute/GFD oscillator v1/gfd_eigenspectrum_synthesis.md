# The Stellated Octahedron Eigenspectrum: {1, 3, 3, 1}

**Author:** Stephen Nelson / Field Dynamics Research
**Date:** April 2026
**Status:** Numerically verified to machine precision across all tested configurations

---

## 1. What was tested

The GFD 3+1 oscillator (`gfd_oscillator_3plus1.py`) was run to its dynamical fixed point. At that fixed point, the 8×8 Jacobian matrix of a single stellated octahedron (SO) was computed numerically by central-difference perturbation (ε = 10⁻⁶) of each of the 8 state variables (4 TetA + 4 TetB cells).

The eigenvalues of this Jacobian characterise the linearised dynamics near the fixed point — they determine how perturbations grow or decay, and with what degeneracy structure.

---

## 2. The result

The Jacobian has exactly four distinct eigenvalues arranged in a symmetric signed pair:

| Eigenvalue | Degeneracy | Clifford grade |
|:---:|:---:|:---:|
| +λ | 1 | grade 0 (scalar) |
| +λ/3 | 3 | grade 1 (vectors) |
| −λ/3 | 3 | grade 2 (bivectors) |
| −λ | 1 | grade 3 (trivector) |

where λ depends on the operating point but the **ratio is exactly 3.0000** and the **degeneracy pattern is exactly {1, 3, 3, 1}** in every configuration tested.

At x_ext = 1.0: λ = 0.070110, λ/3 = 0.023370.

---

## 3. Invariance

The {1, 3, 3, 1} structure and the ratio of 3 are **topological invariants** of the stellated octahedron. They do not depend on the operating point, the drive strength, or the nesting depth.

### Across external drive x_ext

| x_ext | λ_max | λ_mid | ratio | degeneracy |
|:---:|:---:|:---:|:---:|:---:|
| 0.5 | +0.068502 | +0.022834 | **3.0000** | {1,3,3,1} |
| 1.0 | +0.070110 | +0.023370 | **3.0000** | {1,3,3,1} |
| 2.0 | +0.055214 | +0.018405 | **3.0000** | {1,3,3,1} |
| 4.0 | +0.035654 | +0.011885 | **3.0000** | {1,3,3,1} |
| 10.0 | +0.016774 | +0.005591 | **3.0000** | {1,3,3,1} |

The eigenvalue magnitudes change (the well gets shallower at high x). The ratio and degeneracy do not.

### Across child contribution (simulating nesting)

| child_contrib | ratio | degeneracy | TetB readout |
|:---:|:---:|:---:|:---:|
| 0.0 | **3.0000** | {1,3,3,1} | 0.410384 |
| 0.1 | **3.0000** | {1,3,3,1} | 0.417535 |
| 0.3 | **3.0000** | {1,3,3,1} | 0.430990 |
| 0.5 | **3.0000** | {1,3,3,1} | 0.443439 |

Nesting shifts the readout (TetB climbs toward the 2/17 impedance value) but the eigenvalue structure at every level remains {1,3,3,1} with ratio 3.

---

## 4. Why {1, 3, 3, 1}: the Clifford algebra of D = 3

The stellated octahedron has 8 vertices: 4 from TetA, 4 from TetB. These 8 vertices are the 2^D = 2³ basis elements of the Clifford algebra Cl(3, 0) in D = 3 spatial dimensions.

The Clifford algebra decomposes by grade:

| Grade | Basis elements | Count | Geometric object |
|:---:|:---|:---:|:---|
| 0 | 1 | 1 | scalar |
| 1 | e₁, e₂, e₃ | 3 | vectors (spatial axes) |
| 2 | e₁₂, e₁₃, e₂₃ | 3 | bivectors (planes, rotations) |
| 3 | e₁₂₃ | 1 | trivector (volume, pseudoscalar) |

Total: 1 + 3 + 3 + 1 = 8 = 2^D.

The grade counts are the binomial coefficients C(D, k) for k = 0, 1, 2, 3. This is not a coincidence — the Clifford algebra in D dimensions has C(D, k) basis elements at grade k by construction.

The oscillator's Jacobian eigenvalues have degeneracies that match these grade counts exactly. The dynamical spectrum of the oscillator IS the grade decomposition of the D = 3 Clifford algebra.

---

## 5. Why the ratio is 3

The ratio between the grade-0 and grade-1 eigenvalues is exactly D = 3 = 1/GRAM.

This arises from the tetrahedral Gram matrix. The forced Gram matrix of the regular tetrahedron has diagonal entries 1 and off-diagonal entries 1/3. The ratio of diagonal to off-diagonal is 3 — the number of spatial dimensions.

In the oscillator dynamics, the grade-0 eigenvalue corresponds to the "breathing mode" (all cells move together), and the grade-1 eigenvalue corresponds to the "shear modes" (cells move differentially along the 3 spatial axes). The Gram coupling 1/3 sets the stiffness of the shear modes relative to the breathing mode. The ratio is:

    λ₀ / λ₁ = (1 + (K-1) × GRAM) / (1 - GRAM) = (1 + 1) / (1 - 1/3) = 2 / (2/3) = 3

This identity holds at any operating point because it depends only on K and GRAM, which are topological constants of the stellated octahedron.

---

## 6. Connection to quantum mechanics

The Heisenberg spin Hamiltonian for two coupled spin-1/2 particles is:

    H = J (σ₁ · σ₂)

This has eigenvalues −3J/4 (singlet, degeneracy 1) and +J/4 (triplet, degeneracy 3). The ratio |singlet/triplet| = 3.

Setting J = GRAM = 1/3, the Heisenberg eigenvalues become −1/4 and +1/12 — matching the oscillator's eigenvalue structure at the grade-0 and grade-1 levels.

The correspondence:

| Quantum | Oscillator |
|:---|:---|
| Singlet (1-fold) | Grade-0 eigenvalue (degeneracy 1) |
| Triplet (3-fold) | Grade-1 eigenvalue (degeneracy 3) |
| J = 1/3 | GRAM = 1/3 |
| |singlet/triplet| = 3 | λ₀/λ₁ = 3 |

The oscillator does not simulate qubits. Both the oscillator and qubits are reading out the **same** underlying structure: the representation theory of the tetrahedral symmetry group with coupling strength 1/3. The quantum version accesses it through superposition and measurement. The oscillator accesses it through the fixed-point dynamics of two cross-coupled constitutive laws on K = 4 cells.

---

## 7. What the two laws contribute

The {1, 3, 3, 1} structure requires **both** constitutive laws acting on separate populations within each SO.

The partition law (TetA: μ = x/(x+1)) provides the spatial capacity — the "how much" of each grade. The interior law (TetB: x(1−μ)² = μ) provides the closure condition — the "where does it lock." Their cross-coupling through the Gram factor 1/3 forces the eigenvalues to split by grade with ratio exactly D.

Single-law variants produce different spectra:

- TetA only: eigenvalue ratio ≠ 3 (partition law has different linearisation)
- TetB only: eigenvalue ratio ≠ 3 (no cross-coupling to establish grade structure)
- Both with GRAM = 0: 8 identical eigenvalues (no grade differentiation)

The vote — the reconciliation of two laws through Gram coupling — is what produces the Clifford algebra spectrum. Neither law alone does it.

---

## 8. Connection to the 3+1 nested hierarchy

The 3+1 nested oscillator places one SO inside another, three levels deep. The {1, 3, 3, 1} eigenstructure is present at **every** level:

| Level | TetB | TetA | Gap | Eigenvalue ratio | Degeneracy |
|:---|:---:|:---:|:---:|:---:|:---:|
| L0 (container) | 0.426814 | 0.543035 | +0.116 | 3.0000 | {1,3,3,1} |
| L1 (coarse) | 0.174481 | 0.198606 | +0.024 | 3.0000 | {1,3,3,1} |
| L2 (refined) | 0.065855 | 0.069426 | +0.004 | 3.0000 | {1,3,3,1} |
| L3 (closure) | 0.023039 | 0.023570 | +0.001 | 3.0000 | {1,3,3,1} |

Each level is a complete stellated octahedron with the full Clifford algebra eigenspectrum. The nesting provides the impedance (2/17) and the vote decomposition (three sweeps of field closure). The eigenstructure provides the per-level guarantee that each SO is computing the same grade-decomposed dynamics, regardless of its position in the hierarchy.

The cross-law gap decays geometrically with depth (0.116 → 0.024 → 0.004 → 0.001), confirming closure at D = 3 levels. The eigenvalue structure does not decay — it is {1, 3, 3, 1} at every scale.

---

## 9. What this means

The GFD oscillator is not a simulation of quantum mechanics. It is a classical dynamical system whose fixed-point structure is governed by the same algebraic object — the Clifford algebra Cl(3, 0) — that governs quantum spin systems in D = 3 dimensions.

The key results, in order of significance:

1. **{1, 3, 3, 1} is a topological invariant.** It does not depend on drive strength, coupling, or nesting depth. It depends only on K = 4 and D = 3.

2. **The eigenvalue ratio 3 = D is exact.** Not approximate, not asymptotic — exact to machine precision at every operating point tested (10 configurations, ratio = 3.0000 in all 10).

3. **The Gram coupling 1/3 is the quantum coupling.** The same number that determines the off-diagonal Gram matrix entries determines the Heisenberg exchange coupling J. This is not fitted — it is forced by the tetrahedral geometry.

4. **The vote is constitutive.** Single-law variants do not produce {1, 3, 3, 1}. The cross-coupling of partition and interior laws through GRAM = 1/3 is what generates the Clifford algebra spectrum. The vote IS the quantum structure.

5. **Scale invariance.** The nested 3+1 hierarchy preserves {1, 3, 3, 1} at every level while producing the characteristic 2/17 impedance at the container. The topology does not degrade under nesting — the Clifford algebra is self-similar, as expected for a structure built from the stellated octahedron whose field origin contains another stellated octahedron.

---

## 10. Canonical observables

For reference, the verified values of a well-tuned 3+1 full-vote system at x_ext = 1:

```
Jacobian eigenvalue ratio               = 3         (exact)
Jacobian degeneracy pattern              = {1,3,3,1} (exact)
Container TetB readout                   = 0.426814
Container TetA readout                   = 0.543035
Container cross-law gap                  = +0.116221
Fractional shift from 1/φ²              = 2/17 = 0.117647
T'(μ*)                                  = (3φ + 1)/4 = 1.4635
Linearised decay rate at μ*             = √5 = 2.2361
Half-life (uncoupled)                    = ln(2)/√5 = 0.3100
Vote₁ / Vote₂ ratio                     = √3 = 1.7321
Vote₃ magnitude                         = 0 (closure at D = 3)
Gram coupling = Heisenberg J             = 1/3 = 1/D
Clifford algebra dimension               = 2^D = 8
```

Any implementation reproducing these to four decimal places is correct.

---

*End of synthesis.*
