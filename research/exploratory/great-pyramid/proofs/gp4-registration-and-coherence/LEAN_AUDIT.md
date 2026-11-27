# Lean audit: gp4-registration-and-coherence

| | |
|---|---|
| **File** | [`lean/RegistrationCoherence.lean`](lean/RegistrationCoherence.lean) |
| **Imports** | `Mathlib` (v4.36.0, the same version as the root `proofs/` chain) |
| **Theorems** | 9 |
| **Axioms** | every `#print axioms` reports only `propext`, `Classical.choice`, `Quot.sound` (some fewer); no `sorry` |
| **CI** | [`.github/workflows/lean-great-pyramid-gp4.yml`](../../../../../.github/workflows/lean-great-pyramid-gp4.yml): builds, then fails on any warning, error, `sorry` or non-standard axiom |

## Statements formalised

| README | Lean | Statement |
|---|---|---|
| Theorem 3 (lemma) | `abs_sin_nat_mul_le` | `|sin(n x)| ≤ n |sin x|` |
| Theorem 3 (lemma) | `one_sub_cos_eq` | `1 - cos y = 2 sin²(y/2)` |
| Theorem 3 | `one_sub_cos_nat_mul_le` | `1 - cos(n x) ≤ n² (1 - cos x)` |
| Theorem 3 | `ensemble_bound` | finite ensembles: `Σ pᵢ(1 - cos n(θᵢ-φ)) ≤ n² Σ pᵢ(1 - cos(θᵢ-φ))` |
| Theorem 4 | `coprime_registration` | any field: `z³ = w³`, `z⁷ = w⁷`, `w ≠ 0` ⇒ `z = w` |
| Theorems 1, 5 | `uniform_gon_harmonic` | `Σ_{k<N} ζ^(dk) = N` if `N ∣ d`, else 0 (exact selector) |
| Theorem 1 | `uniform_gon_registered` | `(ζⁿ)^N = 1` |
| Theorem 2 | `mixture_coherence` | the mixture `(1-t)·uniform + t·δ₀` has first harmonic `t` |
| Proposition 6 | `lock_minima` | `cos(21 · 2πn/21) = 1` |

## Checked by script, not formalised

- Theorem 1's 'only if' (|E e^{iNθ}| = 1 forces a coset): script.
- Theorem 5's Parseval sidelobe bound and the 14-character sum: script, 50-digit numerics.
- The step from the finite-ensemble bound to `C_N ≥ 1 - N²(1 - C₁)` (choosing φ = arg m₁) is one line in the README.

A Lean proof can be wrong only in its statements; a referee should check the statements above against the README, not the proofs.
