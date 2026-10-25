# Mathematical Foundations of Tetrad Gravity (Vierbein Formalism)

## Overview

The tetrad (vierbein) formalism provides a bridge between coordinate-dependent descriptions of spacetime and local Lorentz-invariant physics. This framework is essential for understanding how gravity can be discretized and computed, making it particularly relevant for computational gravity field models.

---

## 1. Tetrad/Vierbein Definition

### Basic Structure

The tetrad field **e^a_μ** creates a mapping between two different index types:

- **Coordinate indices** (μ, ν, ρ, σ): Greek indices running 0-3, referring to spacetime coordinates
- **Local Lorentz indices** (a, b, c, d): Latin indices running 0-3, referring to an orthonormal frame at each point

### Metric Reconstruction

The spacetime metric **g_μν** is reconstructed from the tetrad:

```
g_μν = η_ab e^a_μ e^b_ν
```

where **η_ab** is the Minkowski metric diag(-1, +1, +1, +1).

**Physical meaning**: At each point, the tetrad provides four orthonormal basis vectors (one timelike e^0, three spacelike e^1, e^2, e^3) that span the tangent space. The metric encodes how these local frames relate to the global coordinate system.

### Inverse Tetrad

The inverse tetrad **E_a^μ** satisfies:

```
E_a^μ e^a_ν = δ^μ_ν
e^a_μ E_b^μ = δ^a_b
```

This allows conversion between coordinate and frame indices.

---

## 2. Key Mathematical Structure

### Component Counting

- **Total components**: The tetrad e^a_μ has 4 × 4 = 16 components
- **Physical degrees of freedom**: Only 10 are physical (matching the 10 independent components of the symmetric metric tensor g_μν)
- **Gauge degrees of freedom**: The remaining 6 represent local Lorentz transformations (rotations and boosts in the local frame)

**Physical meaning**: The 6 extra degrees of freedom reflect the freedom to choose different orthonormal frames at each point without changing the physical geometry. This gauge symmetry is crucial for the equivalence principle.

### Orthonormality Conditions

The tetrad satisfies:

```
η_ab e^a_μ e^b_ν = g_μν    (metric reconstruction)
g_μν E_a^μ E_b^ν = η_ab    (inverse orthonormality)
```

---

## 3. Connection Forms

### Weitzenböck Connection

The Weitzenböck connection is defined as:

```
Γ^λ_μν = E_a^λ ∂_μ e^a_ν
```

**Key properties**:
- **Curvature-free**: R^λ_ρμν = 0 (vanishing Riemann tensor)
- **Torsionful**: T^λ_μν ≠ 0 (non-zero torsion tensor)
- **Flat spacetime**: The connection describes gravity through torsion rather than curvature

**Physical meaning**: This connection represents a "teleparallel" geometry where parallel transport is path-independent (no curvature), but frames rotate relative to each other (torsion encodes gravitational effects).

### Spin Connection

The spin connection **ω^a_b_μ** encodes how local Lorentz frames rotate as you move through spacetime:

```
D_μ e^a_ν = ∂_μ e^a_ν + ω^a_b_μ e^b_ν - Γ^λ_μν e^a_λ = 0
```

This covariant derivative condition ensures the tetrad remains orthonormal under parallel transport.

**Physical meaning**: The spin connection describes the "rotation" of local frames, which is how gravitational effects manifest in the tetrad formalism. In TEGR, this can be set to zero (Weitzenböck gauge), making torsion the sole carrier of gravitational information.

### Torsion Tensor

The torsion tensor measures the antisymmetric part of the connection:

```
T^λ_μν = Γ^λ_μν - Γ^λ_νμ = E_a^λ (∂_μ e^a_ν - ∂_ν e^a_μ)
```

**Physical meaning**: Torsion represents the failure of parallelograms to close. In TEGR, this torsion encodes all gravitational dynamics, replacing the role of curvature in standard GR.

### Torsion Scalar

The torsion scalar **T** is constructed from contractions of the torsion tensor:

```
T = (1/4) T^λ_μν T_λ^μν + (1/2) T^λ_μν T^νμ_λ - T^λ_μλ T^ν_ν^μ
```

This scalar plays the role analogous to the Ricci scalar R in standard GR.

---

## 4. Teleparallel Equivalent of GR (TEGR)

### Action Principle

The TEGR action is:

```
S = (1/16πG) ∫ e T d⁴x
```

where:
- **e = det(e^a_μ)** is the determinant of the tetrad (volume element)
- **T** is the torsion scalar
- **G** is Newton's gravitational constant

### Field Equations

Variation with respect to the tetrad yields field equations equivalent to Einstein's equations:

```
E_a^μ (∂_ν(e S_a^μν)) - e S_b^νμ T^b_νμ E_a^μ = 8πG e T_a^μ
```

where **S_a^μν** is the superpotential and **T_a^μ** is the energy-momentum tensor.

**Key result**: These equations are dynamically equivalent to Einstein's field equations, proving TEGR is a reformulation of GR, not a modification.

### Advantages of TEGR

1. **Gravitational energy**: Energy-momentum can be defined as surface integrals (not possible in standard GR)
2. **Flat background**: Spacetime is flat (zero curvature), with gravity encoded in torsion
3. **Computational simplicity**: Torsion is first-order in derivatives, while curvature is second-order
4. **Discrete compatibility**: Flat geometry is more natural for lattice/discrete approaches

---

## 5. Fiber Bundle Perspective

### Principal Bundle Structure

The tetrad formalism has a natural fiber bundle interpretation:

- **Base manifold**: Spacetime M (4-dimensional)
- **Fiber**: SO(3,1) Lorentz group (6-dimensional)
- **Principal bundle**: P(M, SO(3,1)) over spacetime
- **Frame bundle**: The bundle of all orthonormal frames at each point

### Tetrad as Section

The tetrad **e^a_μ(x)** is a section of the frame bundle, selecting a specific orthonormal frame at each spacetime point.

### Connection 1-Form

The spin connection **ω^a_b_μ** is a connection 1-form on the principal bundle:

```
ω = ω^a_b_μ dx^μ
```

This connection determines how frames are parallel-transported along curves in spacetime.

**Physical meaning**: The fiber bundle structure makes explicit the gauge symmetry (local Lorentz transformations) and provides the mathematical framework for understanding how gravitational dynamics emerge from the geometry of frame rotations.

---

## 6. Discrete/Computational Approaches

### Why Tetrad Formalism Enables Discretization

1. **Flat background**: TEGR's flat spacetime is naturally compatible with discrete lattices, as there's no intrinsic curvature to approximate

2. **First-order dynamics**: Torsion involves only first derivatives of the tetrad, making it easier to discretize than curvature (which requires second derivatives)

3. **Local frames**: The tetrad provides a natural local structure at each point, matching the discrete nature of computational grids

4. **k=4 structure**: The four tetrad legs (one timelike + three spacelike) naturally map to tetrahedral structures:
   - 4 vertices of a tetrahedron
   - 4 faces of a tetrahedron  
   - 4 ADM constraints (1 Hamiltonian + 3 momentum)

### Computational Advantages

- **Finite difference**: First derivatives are more stable and accurate than second derivatives
- **Lattice gauge theory**: The SO(3,1) gauge structure parallels QCD lattice methods
- **Parallel transport**: Torsion-based parallel transport is simpler to compute than curvature-based transport
- **Energy localization**: Gravitational energy can be computed locally (not possible in standard GR)

### Discrete Tetrad Implementation

In a discrete setting:

1. **Tetrad assignment**: Assign tetrad components e^a_μ to lattice sites
2. **Torsion computation**: Calculate T^λ_μν from finite differences of tetrad components
3. **Action evaluation**: Sum torsion scalar over lattice volume
4. **Field equations**: Solve discrete versions of TEGR field equations

The tetrahedral structure (k=4) naturally emerges from the requirement that 4 orthonormal vectors span the 4-dimensional tangent space at each point.

---

## Key Equations Summary

### Fundamental Relations

```
g_μν = η_ab e^a_μ e^b_ν                    (metric reconstruction)
E_a^μ e^a_ν = δ^μ_ν                        (inverse tetrad)
```

### Connection and Torsion

```
Γ^λ_μν = E_a^λ ∂_μ e^a_ν                   (Weitzenböck connection)
T^λ_μν = E_a^λ (∂_μ e^a_ν - ∂_ν e^a_μ)     (torsion tensor)
```

### Action and Field Equations

```
S = (1/16πG) ∫ e T d⁴x                     (TEGR action)
```

### Physical Interpretation

- **16 components** → **10 physical** + **6 gauge** (local Lorentz symmetry)
- **4 tetrad legs** → **1 timelike** + **3 spacelike** (spans tangent space)
- **Torsion** → encodes gravitational dynamics (replaces curvature)
- **Flat spacetime** → enables discrete/computational approaches

---

## Connection to Gravity Field Models

The tetrad formalism's k=4 structure (four orthonormal basis vectors) directly connects to:

1. **Tetrahedral geometry**: 4 vertices/faces required for 3D closure
2. **ADM constraints**: 4 constraints (1 Hamiltonian + 3 momentum)
3. **LQG quantum tetrahedra**: 4 faces per quantum tetrahedron
4. **Stellated octahedron**: Two interpenetrating tetrahedra (8 vertices total)

This geometric structure provides the foundation for discrete field processing models where gravitational dynamics emerge from tetrahedral coupling topologies.

---

## References

- Cartan, É. (1922). Sur une généralisation de la notion de courbure de Riemann et les espaces à torsion.
- Misner, C. W., Thorne, K. S., & Wheeler, J. A. (1973). Gravitation. W. H. Freeman.
- Aldrovandi, R., & Pereira, J. G. (2013). Teleparallel Gravity: An Introduction. Springer.
- Hehl, F. W., et al. (1995). Metric-affine gauge theory of gravity. Reviews of Modern Physics, 48(3), 393.
- Hayashi, K., & Shirafuji, T. (1979). New general relativity. Physical Review D, 19(12), 3524.
