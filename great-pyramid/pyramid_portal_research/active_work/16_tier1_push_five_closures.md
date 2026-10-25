# AW 16 — Tier 1 Push: Five Closures

**Active work item:** 16
**Date:** May 12, 2026
**Status:** all five Tier 1 items addressed; four full closures + one partial closure (mass-from-associator, calibration step acknowledged as open)
**Modules added:** `cyclotomic_12.py`, `gfd_oscillator_jacobian.py`, `fine_structure_hierarchy.py`, `mirror_match_distribution.py`, `mass_from_associator.py`
**Appendix added:** `J_closure_algebra_advancement.md` (canonical source for §1)
**Tests:** 129 new (768 total, up from 639)

## Headline

Five Tier 1 gaps tackled in one push:

| # | Gap | Module | Status |
|:-:|---|---|---|
| 1 | Mass from associator | `mass_from_associator.py` | partial: formalism explicit, m_e calibration open |
| 2 | α in closure-algebra hierarchy via ord_{137}(4) | `fine_structure_hierarchy.py` | closed: 137 placed in Gaussian-axial sector at level Φ_{34} |
| 3 | Cyclotomic-12 unification (A_3^Ω ≅ Z[ζ_{12}]) | `cyclotomic_12.py` | closed: full ring + Galois + Cl(3,0) embedding |
| 4 | Theorem 7 GFD oscillator explicit Jacobian | `gfd_oscillator_jacobian.py` | closed: 8×8 matrix, S_4×Z_2-invariant, spectrum (1,3,3,1) |
| 5 | Mirror match as distribution | `mirror_match_distribution.py` | closed: bimodal structure characterized |

The single redirect from Stephen (sweep is the Hadamard operator; my earlier "sweep-multiplication algebra structure" framing was wrong) sharpened Tier 1 #3 from "build a multiplication table" to "make the cyclotomic-12 unification runtime-verified" — which is the deeper and correct gap.

---

## §1 Cyclotomic-12 unification: A_3^Ω ≅ Z[ζ_{12}]

**Canonical source:** appendix J.

The Ω-fixed subalgebra of Cl(3, 0) is the 12th cyclotomic integer ring with explicit generator

$$\zeta_{12} = \frac{T_1 + I}{2}, \qquad T_1 = e_1 + e_2 + e_3, \qquad T_2 = e_{12} + e_{23} - e_{13}, \qquad I = e_{123}$$

The four-element basis {1, T_1, T_2, I} of A_3^Ω satisfies the multiplication table

$$T_1^2 = 3, \quad T_2^2 = -3, \quad T_1 T_2 = 3I, \quad I T_1 = T_2, \quad I^2 = -1$$

and the minimal polynomial Φ_{12}(ζ) = ζ⁴ - ζ² + 1 = 0 is verified in Cl(3, 0) by direct computation.

**Eight advances delivered:**

1. The Ω-fixed subalgebra is exactly Z[ζ_{12}] — unifying Gaussian Z[i] and Eisenstein Z[ω] as the two quadratic subfields of Q(ζ_{12})
2. Full Z/3-grading of Cl(3, 0) (the +1, ω, ω̄ eigenspaces of Ω, multiplicities 2, 3, 3)
3. Galois group V_4 = (Z/12)* = {1, 5, 7, 11} with three non-trivial elements fixing three quadratic subfields
4. **Parity exhaustion**: there can be no fourth parity tag because Q(ζ_{12}) has exactly three quadratic subfields (sharper than the s² < 4 discriminant constraint)
5. Spinor lift Ω̃ ∈ SU(2) has order 6 (generates the binary tetrahedral group 2T of order 24)
6. McKay correspondence: 2T ↔ Ê_6 Dynkin, with irrep dimensions (1, 1, 1, 2, 2, 2, 3) matching the Cl(3, 0) closure structure
7. **Sweep multiplication ⋆ on A_3^Ω = ordinary multiplication in Z[ζ_{12}]** — the deepest unification statement
8. Compositum-12 closure tower at D = 6: S(6, 4) = 21 · 17 · 13 · 257 · 241 (primary trio {13, 17, 21} + Fermat-prime extension {257} + top cyclotomic level {241})

**Runtime artifacts:** 42 tests passing in 0.25s. The cyclotomic ring is implemented as a 4-tuple with exact rational coefficients; Cl(3, 0) embedding uses numpy with the orientation cocycle from `unification_algebra`.

**What this changes:** the framework's Gaussian-axial channel and Eisenstein-hexagonal channels were previously separate. Cyclotomic-12 shows they are two quadratic subfields of one number ring. The "axial vs. hexagonal" framing is the projection of the V_4 Galois action onto its three non-trivial subgroups.

## §2 Fine structure: 137 in the closure-algebra hierarchy

**Result:** 137 lives in the **Gaussian axial sector** of the closure-algebra hierarchy, with cyclotomic depth 34.

Three sharp number-theoretic facts about 137:

- 137 ≡ 1 (mod 4) → **splits in Z[i]** (Gaussian axial channel): 137 = 4² + 11² = (4 + 11i)(4 − 11i)
- 137 ≡ 2 (mod 3) → **inert in Z[ω]** (does NOT split in the Eisenstein hexagonal channels)
- 137 ≡ 5 (mod 12) → **does not split completely in Z[ζ_{12}]** — sits at the Gaussian-half of the cyclotomic-12 splitting

The multiplicative order ord_{137}(4) = 34 places 137 at the cyclotomic level Φ_{34}, not at any of the primary trio {Φ_3, Φ_4, Φ_6} = {21, 17, 13}. 137 is a *deeper* prime than the framework's primary harmonics.

**Empirical observation:** 1/α = 137 + 1/28 gives 137.035714 vs CODATA 137.035999 (residual −2.08 ppm). The denominator 28 has three structural readings: 4 + 24 (pentachoron + torsion), 7 · 4 (Fano shell × tetrahedral cells), C(8, 2) (pair count of Cl(3, 0) basis). Not derived — flagged as observation, not closure.

**What's closed:** the structural location of 137 (Gaussian, level 34) and the splitting-behavior diagnostic.
**What's open:** the 1/28 derivation. The relationship 1/α = 137 + 1/28 holds within 2 ppm but the framework does not yet derive it from first principles.

24 tests, 0.11s.

## §3 GFD oscillator Jacobian: Theorem 7 made runtime

**Result:** the 8×8 Jacobian at the dynamical fixed point of the K = 4 GFD oscillator is constructed explicitly, S_4 × Z_2-invariant, with eigenspectrum (+λ, +λ/D, −λ/D, −λ) of multiplicities (1, D, D, 1).

**Construction (four projectors):** decompose R^4 ⊕ R^4 = R^8 into S_4-irreps via P_{triv,4} = (1/4) **1 1**^T and P_{std,4} = I_4 − P_{triv,4}. Then cross with Z_2 (TetA ↔ TetB) symmetry:

$$J = \lambda\, P_{\text{triv}}^{+} \;+\; \frac{\lambda}{D}\, P_{\text{std}}^{+} \;-\; \frac{\lambda}{D}\, P_{\text{std}}^{-} \;-\; \lambda\, P_{\text{triv}}^{-}$$

where the four projectors are rank (1, 3, 3, 1) respectively, summing to identity on R^8.

**Verified:**

- [J, S_4-cyclic] = 0 (commutes with the diagonal S_4 4-cycle on TetA ⊕ TetB)
- [J, S_4-transposition] = 0 (commutes with any S_4 element)
- [J, Z_2-swap] = 0 (commutes with the TetA ↔ TetB exchange)
- Eigenspectrum: {+λ, +λ/3, −λ/3, −λ} at D = 3, with multiplicities exactly (1, 3, 3, 1)
- Multiplicities match Cl(3, 0) grade dimensions (1, 3, 3, 1)
- HJH has the same spectrum (Walsh-block-diagonal form)
- Eigenvalue ratio λ_max / λ_mid = D (so the dimensional control parameter sets the spectral gap)
- At D = 4 the ratio is 4, multiplicities still (1, 3, 3, 1) because the standard rep of S_4 is always 3-dim

22 tests, 0.12s.

**What this changes:** Theorem 7 had been an abstract assertion ("the Jacobian commutes with S_4 × Z_2 and has spectrum (1, D, D, 1)"). It is now a concrete numpy matrix any consumer of the framework can verify.

## §4 Mirror-match distribution

**Result:** M(U, V) is **bimodal** — concentrated at 0 for random pairs, at 1 for designed mirror pairs.

**Gate decomposition.** M(U, V) factors into three gates:

- Chirality gate: (1 − χ_U χ_V) / 2, fires only when chiralities oppose
- Phase gate: 1 if phases close mod 2π (measure-zero for random pairs)
- Gram gate: Σ_P exp(−‖G_U − P^T G_V P‖² / ε²), peaks at 6 when Gram matrices match

**Empirical fire rates** (n = 200, ε = 10^{-3}):

| Gate | Random pairs | Designed mirror pairs |
|---|:-:|:-:|
| chirality | 0.490 | 1.000 |
| phase | 0.000 | 1.000 |
| Gram | 0.000 | 1.000 |
| all three | 0.000 | 1.000 |

**Designed pair construction.** V = mirror(U) constructs the mirror partner by reflecting U's triad through origin (negates each vector). This:

- Preserves G (reflection is orthogonal: G(−v_i, −v_j) = G(v_i, v_j))
- Flips chirality (det(−A) = −det(A) for 3×3)
- Preserves phase (designed assignment)

All 50 designed pairs give M ≈ 1.000. All 200 random pairs give M = 0.000.

**Tolerance sweep.** For designed pairs, M = 1 across ε ∈ [10^{-6}, 10^{-1}]. The match is exact, so widening tolerance doesn't change it. For random pairs, M stays near 0 until ε ~ 0.1 or higher, when the Gaussian kernel becomes wide enough to bridge generic Gram differences.

20 tests, 0.72s.

**What this characterizes:** the mirror-match functional is a strict three-gate AND. Generic triad pairs almost never match because each gate is individually rare (½, 0, 0). Designed pairs that satisfy all three gates pass the AND.

## §5 Mass from associator (partial closure)

**Status:** formalism explicit; calibration to m_e remains the Generation-1 open piece.

**The formalism.** For the sweep product ⋆ = closure_projection ∘ Clifford_product, the associator

$$[a, b, c]_\star = (a \star b) \star c \;-\; a \star (b \star c)$$

is non-zero in general because closure_projection is not a ring homomorphism (the Clifford product is associative, but the Ω-projection step destroys this structure for the symmetrized version).

**Computed residue.** For the structured triple

- a = α·1 + β·T_1 (TetA-axial seed)
- b = γ·1 + δ·T_2 (TetB-axial seed)
- c = ε·I (bridge seed)

at default amplitudes (α = γ = ε = 1, β = δ = ½), the sweep-associator has axial component −0.75 in the scalar sector, axial-norm exactly 0.75.

**Scaling.** The associator is trilinear, so doubling all seed amplitudes multiplies the residue by 8.

**What this is.** A dimensionless axial scalar from a runtime computation, depending on five real seed amplitudes. The framework predicts that this scalar — appropriately calibrated by the Generation-1 scale — gives the electron mass m_e. The calibration step is not in this module.

**What's closed.** The associator-axial-projection pipeline is explicit and verified. Tests cover the trilinear scaling, the axial-projection mechanics, the structural seed construction, and the partial-closure status flag.

**What's open.** The Generation-1 calibration that maps the dimensionless residue to m_e in eV. This is the framework-level open piece (irreducible Generation-1 mass), not a missing computation.

21 tests, 0.16s.

## Cross-cutting observations

**The Hadamard architecture stands.** Stephen's correction settled what was conceptual confusion on my part: there is no "sweep multiplication algebra structure" to build because the sweep IS the three-pass Hadamard kernel. `sweep_product3` in `closure_core256` is the canonical implementation. The cyclotomic-12 work is the real gap that sat in the same conceptual neighborhood and was the deeper thing pointing-toward.

**The framework's three primary primes and their cyclotomic levels:**

- 13 = Φ_6(4): Eisenstein '−' (TetB floor), splits in Z[ω]
- 17 = Φ_4(4): Gaussian axial (Field Origin), splits in Z[i]
- 21 = Φ_3(4): Eisenstein '+' (TetA ceiling), 3 · 7 (composite)

The framework's fourth deep prime 137 sits at Φ_{34}, splitting in Z[i] only — the Gaussian-axial channel taken to a much higher cyclotomic level.

**Tier 1 closure summary:**

- Cyclotomic-12 unification: ✓ closed
- α via ord_{137}(4) structural location: ✓ closed; numerical fit (1/α = 137 + 1/28): open
- Explicit Jacobian: ✓ closed
- Mirror match distribution: ✓ closed
- Mass from associator: formalism ✓ closed; calibration ✗ open

Four of five fully closed. The fifth has the formalism made concrete with an explicit dimensionless residue but flags the m_e mapping as the Generation-1 step.

## Test counts (after this push)

| Suite | Tests |
|---|:-:|
| Pre-push baseline | 639 |
| `test_cyclotomic_12` | +42 |
| `test_gfd_oscillator_jacobian` | +22 |
| `test_fine_structure_hierarchy` | +24 |
| `test_mirror_match_distribution` | +20 |
| `test_mass_from_associator` | +21 |
| **Total** | **768** |

All 768 pass in 1.44s. The package now exposes 5 new module surfaces; appendix J is the canonical source for the cyclotomic-12 work.

## What's next

Items deferred to a possible Tier 2 push:

- 3-cocycle of ⋆ in H³(Z/3, Z[ζ_{12}]) on the full Cl(3, 0) — structured non-associativity off the Ω-fixed subalgebra
- Generation-1 calibration step that closes mass-from-associator to m_e in physical units
- Derivation of the 1/28 denominator in 1/α = 137 + 1/28 (currently 2 ppm empirical)
- McKay Ê_6 — pin down where the seven irreducible reps of 2T show up as framework observables
- Tensor-product cyclotomic-12 structure: A_3^⊗2 fixed subalgebra

These are listed in appendix J §9.
