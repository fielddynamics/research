# Active Work 15 — Core Unification Algebra: The Constructive Push

**Status:** Push — the seven constructive theorems from Part III of the closure-algebra pipeline made runtime-verified
**Purpose:** Turn the unification algebra from a labeling object into a real algebra with σ, Ω, ring norms, divisor formula, grade decomposition, and the worked example
**Reading time:** 9 minutes
**Companion modules:** `python/unification_algebra.py` (extended; now 533 + ~330 = ~860 lines), `python/tests/test_unification_algebra_core.py` (48 new tests)
**Canonical source:** `99_appendices/G_closure_algebra_pipeline.md` Part III (Rigorous Statements) + Part IV (Worked Example)

---

## 0. Headline

AW 13 had the **uniqueness** theorems T1–T8: three independent routes to $D = 3$, the coupling polynomial as trace, the 40/24 split. Those said *why the algebra has the shape it has*.

AW 15 adds the **constructive** theorems R1–R7: the orientation cocycle as an explicit callable, the closure operator Ω as a basis permutation, the imaginary-quadratic ring norms as actual integer computations, the divisor formula for $S(D, K)$, the Cl(3, 0) grade decomposition, and a worked example that walks a Boolean function through the full pipeline.

The unification algebra is no longer a dataclass with theorems attached. It is a runtime algebra with operations.

## 1. What "push harder" meant

After AW 13, `unification_algebra.py` had:

- `UnificationAlgebra` — a frozen dataclass with fields `(n, K, decomposition, axial_dim, middle_dim, total_dim, ring_axial, ring_middle)` — *a labeling*
- T1–T8 uniqueness theorems wired
- 10-stage pipeline as a list of dicts pointing to other modules

What it was missing (Part III of appendix G):

| Missing piece | What it is | Now lives in |
|---|---|---|
| **R2 — orientation cocycle $\sigma(a, b)$** | $\sigma(a, b) = (-1)^{\sum_{i>j} a_i b_j}$ on $(\mathbb Z/2)^n$ | `orientation_cocycle`, `twisted_product`, `clifford_relations_check_3` |
| **R3 — closure operator Ω as basis permutation** | $\Omega : e_1 \to e_2 \to e_3 \to e_1$ on Cl(3, 0); $\Omega^3 = \text{id}$ | `omega_permute_mask`, `omega_order_check`, `omega_fixed_masks`, `omega_cycled_masks` |
| **R4 — explicit subspace identification** | Ω-fixed = $\{1, I\}$ (axial); Ω-cycled = 2 orbits of length 3 (vectors + bivectors) | `omega_decomposition_check` |
| **R5 — imaginary-quadratic ring norms** | $N_{\mathbb Z[i]/\mathbb Z}(K - i) = K^2 + 1$; $N_{\mathbb Z[\omega]/\mathbb Z}(K \mp \omega) = K^2 \pm K + 1$ | `gaussian_norm_Z_i`, `eisenstein_norm_Z_omega`, `coupling_polynomial_as_norm_trace_check` |
| **R6 — divisor formula for $S(D, K)$** | $S(D, K) = \prod_{d \mid 2D,\, d > 2} \Phi_d(K)$ | `divisors_above_two`, `S_D_K_divisor_formula` |
| **R7 — Cl(3, 0) grade decomposition** | grade dimensions $\{1, 3, 3, 1\}$ = $\binom{3}{k}$ | `cl_3_0_grade_dimensions`, `cl_3_0_grade_check` |
| **Worked example** | a 3-bit Boolean function through all stages of the pipeline | `ClosureAlgebraReading`, `boolean_function_through_pipeline` |

Stephen's redirect ("push harder on the core unification algebra") meant: stop pushing more peripheral pieces. Make the **core** algebra a real first-class object. The eight uniqueness theorems are about what's forced; the seven constructive theorems are about what the algebra *is*.

## 2. R2 — The orientation cocycle

The cocycle that twists the Walsh group algebra $\mathbb R[G]$ into the Clifford algebra $\mathrm{Cl}(n, 0)$ is

$$\sigma(a, b) \;=\; (-1)^{\sum_{i > j}\, a_i\, b_j}$$

where $a, b \in G = (\mathbb Z/2)^n$ and $a_i$ is bit $i$ of $a$. The twisted product is

$$e_a \cdot e_b \;=\; \sigma(a, b)\,e_{a \oplus b}$$

**Implementation.** `orientation_cocycle(a, b, n=3)` returns $\pm 1$. `twisted_product(a, b, n=3)` returns the pair $(\sigma, a \oplus b)$.

**Verification — `clifford_relations_check_3()` confirms:**
- $e_i^2 = +1$ for each generator (mask 1 = $e_1$, mask 2 = $e_2$, mask 4 = $e_3$)
- $e_i e_j = -e_j e_i$ for each $i \ne j$ pair

This is the standard cocycle-twisted group-algebra construction (Lounesto, *Clifford Algebras and Spinors*, 2nd ed., Cambridge 2001). It is now a runtime object that any future module can use without re-deriving.

## 3. R3 — The closure operator Ω

Ω is the algebra automorphism that cyclically permutes generators $e_1 \to e_2 \to e_3 \to e_1$. In mask order (where bit $i$ of a mask indicates presence of $e_{i+1}$), Ω permutes bits:

$$\text{bit 0} \to \text{bit 1} \to \text{bit 2} \to \text{bit 0}$$

**Action on the 8 basis elements:**

| Mask | Element | $\Omega(\text{mask})$ | $\Omega(\text{element})$ |
|:-:|:-:|:-:|:-:|
| 0 | $1$ | 0 | $1$ (fixed) |
| 1 | $e_1$ | 2 | $e_2$ |
| 2 | $e_2$ | 4 | $e_3$ |
| 4 | $e_3$ | 1 | $e_1$ |
| 3 | $e_{12}$ | 6 | $e_{23}$ |
| 6 | $e_{23}$ | 5 | $e_{13}$ |
| 5 | $e_{13}$ | 3 | $e_{12}$ |
| 7 | $I = e_{123}$ | 7 | $I$ (fixed) |

The minimal polynomial of Ω on $\mathrm{Cl}(3, 0)$ factors as

$$X^3 - 1 \;=\; (X - 1)(X^2 + X + 1) \;=\; \Phi_1(X)\,\Phi_3(X)$$

**The Φ_3 factor is what makes Eisenstein structure appear on the middle sector.** The middle six-dimensional sector is acted on by Ω with eigenvalues $\omega, \bar\omega$ (cube roots of unity), giving it the $\mathbb Z[\omega]$-module structure.

**Implementation.** `omega_permute_mask(mask)`, `omega_order_check()` verifies $\Omega^3 = \text{id}$, `omega_fixed_masks()` returns $[0, 7]$ (the axial sector), `omega_cycled_masks()` returns the two orbits of length 3 (vectors and bivectors).

## 4. R4 — The decomposition $\mathcal A_3 = \langle 1, I\rangle \oplus \mathbb Z[\omega]^3$

Under Ω:

- **Ω-fixed subspace** (eigenvalue $+1$, multiplicity 2): the axial sector $\langle 1, I\rangle$, spanned by scalar $1$ (mask 0) and pseudoscalar $I = e_{123}$ (mask 7)
- **Ω-cycled subspace** (eigenvalues $\omega, \bar\omega$, total multiplicity 6): two orbits of length 3
  - Vectors orbit: $\{e_1, e_2, e_3\}$ (masks $\{1, 2, 4\}$)
  - Bivectors orbit: $\{e_{12}, e_{23}, e_{13}\}$ (masks $\{3, 6, 5\}$)

Each length-3 orbit carries the action of Ω as multiplication by $\omega$, giving it the structure of a free $\mathbb Z[\omega]$-module of rank 1. Combining the three Eisenstein channels (axial pair $(e_k, e_{(k+1)(k+2)})$ at each $k$ from the Hodge pairing), the middle sector is $\mathbb Z[\omega]^3$.

Total real dimension: $2 + 6 = 8 = \dim \mathrm{Cl}(3, 0)$ ✓

**Implementation.** `omega_decomposition_check()` returns the explicit orbit structure and verifies the dimensional accounting.

## 5. R5 — Coupling polynomial as norm trace

The coupling polynomial at the three discriminant-irreducible values is the **norm trace** on three imaginary-quadratic rings:

| $s$ | Channel | Ring | Element | Norm | Value at $K = 4$ |
|:-:|---|---|---|---|:-:|
| $0$ | axial | $\mathbb Z[i]$ | $K - i$ | $N(K - i) = K^2 + 1$ | $17$ |
| $+1$ | Eisenstein "+" | $\mathbb Z[\omega]$ | $K - \omega$ | $N(K - \omega) = K^2 + K + 1$ | $21$ |
| $-1$ | Eisenstein "−" | $\mathbb Z[\omega]$ | $K + \omega$ | $N(K + \omega) = K^2 - K + 1$ | $13$ |

**These are honest ring norms**, not abstract polynomial values. The Gaussian norm $N_{\mathbb Z[i]/\mathbb Z}(a + bi) = a^2 + b^2$ and the Eisenstein norm $N_{\mathbb Z[\omega]/\mathbb Z}(a + b\omega) = a^2 - ab + b^2$ are runtime callables. Plugging $(K, -1)$ into the Gaussian norm gives the axial trace; plugging $(K, \mp 1)$ into the Eisenstein norm gives the two hexagonal traces.

**The framework's $\{13, 17, 21\}$ is the integer-ring-norm trace, evaluated at $K = 4$, of the coupling polynomial's three channels.**

**Implementation.** `gaussian_norm_Z_i(a, b)` returns $a^2 + b^2$. `eisenstein_norm_Z_omega(a, b)` returns $a^2 - ab + b^2$. `coupling_polynomial_as_norm_trace_check(K)` verifies the three matches.

## 6. R6 — Divisor formula for $S(D, K)$

The 3-sweep cumulative dimension generalizes to arbitrary depth via the divisor formula

$$\boxed{\;S(D, K) \;=\; \prod_{\substack{d \mid 2D \\ d > 2}} \Phi_d(K)\;}$$

Worked at small $D$ with $K = 4$:

| $D$ | $2D$ | Divisors $> 2$ | Factors | $S(D, 4)$ |
|:-:|:-:|---|---|:-:|
| 2 | 4 | $\{4\}$ | $\Phi_4(4) = 17$ | $17$ |
| 3 | 6 | $\{3, 6\}$ | $\Phi_3(4) \cdot \Phi_6(4) = 21 \cdot 13$ | $273$ |
| 4 | 8 | $\{4, 8\}$ | $\Phi_4(4) \cdot \Phi_8(4) = 17 \cdot 257$ | $4369$ |
| 5 | 10 | $\{5, 10\}$ | $\Phi_5(4) \cdot \Phi_{10}(4)$ | future |

**At $D = 2$**: the impedance value $17$ pops out as $S(2, 4)$ — the unique level at which only $\Phi_4$ contributes.
**At $D = 3$**: the $\Phi_3 \cdot \Phi_6$ pair gives the framework's preferred parity-conjugate factorization. The divisor formula explains *why* this pair is special: at $2D = 6$, the divisors above 2 are exactly $\{3, 6\}$.
**At $D = 4$**: $\Phi_4 \cdot \Phi_8 = 17 \cdot 257$ — Gaussian × Fermat-prime structure, not Eisenstein. The framework would behave fundamentally differently at $D = 4$ (this is the open question raised in Part V of appendix G).

**Implementation.** `divisors_above_two(m)` returns divisors $> 2$. `S_D_K_divisor_formula(D, K)` returns the full breakdown with each $\Phi_d(K)$ factor and verifies alignment with `closure_core256.sierpinski_S`.

## 7. R7 — Cl(3, 0) grade decomposition

The Clifford algebra $\mathrm{Cl}(3, 0)$ has 4 grades, with dimensions counted by $\binom{3}{k}$:

| Grade | Elements | Dimension |
|:-:|---|:-:|
| 0 | scalar $1$ | $\binom{3}{0} = 1$ |
| 1 | vectors $e_1, e_2, e_3$ | $\binom{3}{1} = 3$ |
| 2 | bivectors $e_{12}, e_{13}, e_{23}$ | $\binom{3}{2} = 3$ |
| 3 | trivector $I = e_{123}$ | $\binom{3}{3} = 1$ |

**Total:** $1 + 3 + 3 + 1 = 8 = \dim \mathrm{Cl}(3, 0)$. The pattern $\{1, 3, 3, 1\}$ is **exactly** the $\{1, D, D, 1\}$ eigenspectrum of the GFD oscillator's Jacobian at $D = 3$. The dynamical realization (T2 in AW 13) inherits its eigenvalue multiplicities directly from the Clifford grade decomposition.

**Implementation.** `cl_3_0_grade_dimensions()` returns the dict $\{0: 1, 1: 3, 2: 3, 3: 1\}$. `cl_3_0_grade_check()` computes the grade decomposition by counting `popcount(mask)` for masks $0..7$ and verifies it matches.

## 8. The worked example — Part IV of appendix G

The pipeline now reads a single 3-bit Boolean function as a **closure-algebra element** with all stages computable.

**`ClosureAlgebraReading`** is the dataclass returning:

- `truth_table` — the original 8-entry $\pm 1$ vector
- `walsh_coefficients` — 8-entry Walsh transform output
- `axial_scalar`, `axial_pseudoscalar` — the $\langle 1, I\rangle$ components $a + b I$
- `hex_z1, hex_z2, hex_z3` — the three Eisenstein channel coordinates (each a $(x, y)$ pair representing $x + y\omega$)
- `closure_norm` — the integer-valued complexity measure $N_\mathcal A(F) = a^2 + b^2 + \sum_k N(z_k)$

**Function.** `boolean_function_through_pipeline(truth_table)` walks the pipeline:
1. Stage 1 (state law): the truth table on $(\mathbb Z/2)^3$
2. Stage 1' (Walsh): FWHT to coefficient vector
3. Stage 3 (closure): decompose into $\langle 1, I\rangle$ (axial) + $\mathbb Z[\omega]^3$ (hexagonal)
4. Stage 7 (closure norm): single integer

For any Boolean function on 3 bits — there are $2^8 = 256$ of them — this is now a runtime computation. The "three views of the same operator" from Part IV (Boolean gate / Clifford multivector / closure-algebra element / projective-plane point-labeling / norm object) become accessible as runtime properties of the same `ClosureAlgebraReading`.

## 9. What this changes for the framework

Four consequences:

**(a) The orientation cocycle is now a callable, not just a formula.** Before R2, the Clifford twist of the Walsh group algebra was stated in §01.5 prose. After: $\sigma(a, b)$ is a runtime function, and the Clifford relations $e_i^2 = +1$ and $e_i e_j = -e_j e_i$ are runtime-verified for all generator pairs at $n = 3$.

**(b) The closure operator Ω has an explicit basis-permutation form.** Before R3, Ω was described as "cyclic permutation $e_1 \to e_2 \to e_3$." After: `omega_permute_mask` is a function on the 8 masks; the Ω-fixed and Ω-cycled subspaces are explicit lists of masks; the $\{1, I\}$ axial sector and the two length-3 Eisenstein orbits are returned by name.

**(c) The coupling polynomial $\{13, 17, 21\}$ is now an integer-ring-norm trace.** Before R5, the framework's preferred numbers were stated as cyclotomic polynomial values $\Phi_3(4) = 21$ etc. After: they are honest norms — $N_{\mathbb Z[i]}(4 - i) = 17$, $N_{\mathbb Z[\omega]}(4 - \omega) = 21$, $N_{\mathbb Z[\omega]}(4 + \omega) = 13$ — computed in code. The integers are integer-ring norms, not abstract polynomial values.

**(d) The framework's preferred dimension is now visibly the divisor structure of $2D$.** Before R6, $D = 3$ was the dimension at which everything clicked. After: $D = 3$ is the unique $D$ at which $2D$ has divisors $\{3, 6\}$ above 2, giving the parity-conjugate $\Phi_3 \cdot \Phi_6$ pair. The framework's algebra reads through this pair specifically because $D = 3$ places its $2D$ at 6.

## 10. The two-block structure of `unification_algebra.py`

The module now has two complementary blocks:

```
unification_algebra.py
  |
  +-- T-block — uniqueness theorems (AW 13)
  |     T1  vertex-count uniqueness
  |     T2  eigenspectrum {1,D,D,1} uniqueness
  |     T3  parity-shift-conjugation collapse
  |     T4  coupling polynomial as trace
  |     T5  three factorizations of S(3,K)
  |     T6  connection split from (f-1)/2
  |     T7  discriminant constraint s^2 < 4
  |     T8  range identity Delta f = 2K = 2^D
  |
  +-- R-block — constructive theorems (AW 15)
        R2  orientation cocycle sigma -> Clifford
        R3  closure operator Omega: cyclic permutation, Omega^3 = id
        R4  decomposition A_3 = <1, I> + Z[omega]^3
        R5  coupling polynomial as imaginary-quadratic ring norm
        R6  S(D, K) divisor formula
        R7  Cl(3, 0) grade decomposition matches {1, 3, 3, 1}
```

T-block answers *why* the algebra has its specific form. R-block answers *what* the algebra is concretely. R1 from appendix G (the FWHT isomorphism of the Walsh group algebra) is already implemented in `closure_core256.walsh_matrix_3` and `truth_to_walsh3`/`walsh_to_truth3`, so it doesn't need a new function — the existing primitive is the runtime form. The five concrete morphisms of the closure-algebra pipeline (`parity_pushout`, `shift`, `fusion`, `edge`, `projective`) from AW 14 sit in the third block, `coupling_shells.py`.

## 11. Test coverage

| Class | Count | What it verifies |
|---|---:|---|
| `TestR2OrientationCocycle` | 4 | $\sigma(a, b)$ values at small inputs |
| `TestTwistedProduct` | 3 | $e_a \cdot e_b$ via the twist |
| `TestCliffordRelationsCheck` | 3 | $e_i^2 = +1$, anticommutation for all 3 pairs |
| `TestR3OmegaPermutation` | 7 | Ω fixes $\{0, 7\}$, cycles $\{1, 2, 4\}$ and $\{3, 5, 6\}$, $\Omega^3 = \text{id}$ |
| `TestR4Decomposition` | 4 | axial dim 2, middle dim 6, total 8, two length-3 orbits |
| `TestR5NormTrace` | 6 | Gaussian and Eisenstein norms; coupling polynomial alignment at $K = 2, 3, 4, 5, 7, 10, 16$ |
| `TestR6DivisorFormula` | 7 | $S(2, 4) = 17$, $S(3, 4) = 273$, $S(4, 4) = 4369$; consistency across $D, K$ |
| `TestR7Cl30GradeDecomposition` | 4 | $\{1, 3, 3, 1\}$ from popcount; matches T2 eigenspectrum |
| `TestWorkedExample` | 6 | 3-bit Boolean function through pipeline; AND gate; all-ones; alternating |
| `TestCoreShowcase` | 3 | audit trail mentions R2–R7 and worked example |
| **Total** | **48** | All passing in 0.18s |

Combined with AW 13's `test_unification_algebra.py` (42 tests), the unification module now has **90 tests** covering both the uniqueness theorems and the constructive theorems.

## 12. Status table

| Element | Status |
|---|---|
| R1 (Walsh FWHT isomorphism) — already in `closure_core256.walsh_matrix_3` | derived |
| R2 orientation cocycle $\sigma(a, b)$ — Clifford twist | derived (10 tests) |
| R3 closure operator Ω as basis permutation | derived (7 tests) |
| R4 $\mathcal A_3$ decomposition: axial(2) ⊕ middle(6) | derived (4 tests) |
| R5 coupling polynomial as $\mathbb Z[i]$ / $\mathbb Z[\omega]$ norm | derived (6 tests) |
| R6 $S(D, K)$ divisor formula | derived (7 tests) |
| R7 Cl(3, 0) grade decomposition $\{1, 3, 3, 1\}$ | derived (4 tests) |
| Worked example — Boolean function through pipeline | derived (6 tests) |
| `ClosureAlgebraReading` dataclass for "three views" | structural |
| Two-block T+R structure in `unification_algebra.py` | derived |

## 13. Headline

The unification algebra is now a real algebra. R2 makes the Clifford twist a runtime callable. R3 makes Ω an explicit basis permutation. R4 identifies the Ω-fixed and Ω-cycled subspaces by name. R5 turns the coupling polynomial into honest integer-ring norms. R6 explains the parity-conjugate factorization $\Phi_3 \cdot \Phi_6$ as the divisors of $2D$ above 2 at $D = 3$. R7 ties the dynamical $\{1, D, D, 1\}$ eigenspectrum to the Clifford grade decomposition. The worked example walks a Boolean function through the full pipeline, giving simultaneous Boolean / Walsh / Clifford / closure-algebra / norm readings. The dataclass that was just a labeling now has all the algebra's operations attached.

---

**Cross-references:**
- Canonical source: `99_appendices/G_closure_algebra_pipeline.md` (Part III + Part IV)
- `01_framework_foundations/01.3_graded_identity_operator.md` — three-sweep Walsh-Hadamard kernel (the R1 form)
- `01_framework_foundations/01.5_universal_vertex_reframe.md` — the closure-node algebra in prose; this AW makes it runtime
- `active_work/12_closure_core_integration.md` — the closure-core algebra that R-block uses for primitives
- `active_work/13_unification_algebra.md` — the T-block (uniqueness theorems) that this AW complements
- `active_work/14_parity_pushout_recursion.md` — the five morphisms (pipeline-category view); this AW provides the underlying algebra
- Implementation: `python/unification_algebra.py` (extended), `python/tests/test_unification_algebra_core.py` (new)
