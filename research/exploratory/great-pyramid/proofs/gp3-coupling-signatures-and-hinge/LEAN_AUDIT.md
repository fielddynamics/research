# Lean audit: gp3-coupling-signatures-and-hinge

| | |
|---|---|
| **File** | [`lean/SignaturesHinge.lean`](lean/SignaturesHinge.lean) |
| **Imports** | `Mathlib` (v4.36.0, the same version as the root `proofs/` chain) |
| **Theorems** | 24 |
| **Axioms** | every `#print axioms` reports only `propext`, `Classical.choice`, `Quot.sound` (some fewer); no `sorry` |
| **CI** | [`.github/workflows/lean-great-pyramid-gp3.yml`](../../../../../.github/workflows/lean-great-pyramid-gp3.yml): builds, then fails on any warning, error, `sorry` or non-standard axiom |

## Statements formalised

| README | Lean | Statement |
|---|---|---|
| Theorem 1 | `sig_plus_eq_cyclotomic` | `(cyclotomic 3 ℤ).eval K = f K 1` |
| Theorem 1 | `sig_zero_eq_cyclotomic` | `(cyclotomic 4 ℤ).eval K = f K 0` |
| Theorem 1 | `sig_minus_eq_cyclotomic` | `(cyclotomic 6 ℤ).eval K = f K (-1)` |
| Theorem 1 | `integer_s_in_open_interval` | `|s| < 2 ↔ s ∈ {-1,0,1}` |
| Theorem 1 | `f_two, f_neg_two` | `f K (±2) = (K ± 1)²` |
| Theorem 2 | `hinge` | `f K 1 = f (K+1) (-1)` |
| Theorem 2 | `hinge_unique` | every coincidence `f K s = f K' s'` (`K,K' ≥ 1`, `s,s' ∈ {-1,0,1}`) is trivial or a hinge |
| Theorem 2 | `seventeen_unique` | `f K s = 17` only at `(4, 0)` |
| Theorem 3 | `coprime_plus_minus, coprime_zero_plus, coprime_zero_minus, gcd_one` | pairwise coprime for every `K : ℤ` |
| Theorem 3 | `midpoint` | `f K 1 + f K (-1) = 2 f K 0` |
| Theorem 4 | `fusion, fusion'` | `f K 1 · f K (-1) = f (K²) 1 = 1 + K² f K 0` |
| Theorem 4 | `tower` | `f(K^(2^n),1) = f(K,1) ∏_{j<n} f(K^(2^j),-1)` |
| Theorem 4b | `tower_factor_dvd, tower_head_dvd` | every earlier tower factor divides `A_n = f(K^(2^n), 1)` |
| Theorem 4b | `tower_pairwise_coprime, tower_head_coprime` | `A_0, B_0, B_1, …` pairwise coprime, for every `K : ℤ` (referee's induction) |
| Theorem 4 | `tower_at_four` | the K = 4 values 21, 13, 17, 273, 241, 65793, … |
| Theorem 6 | `graded_trace, involution_multiplicities` | trace form; multiplicities (17, 4) forced |

## Checked by script, not formalised

- Theorem 1's converse via `φ(n) = 2 ↔ n ∈ {3,4,6}` and Niven's theorem: cited; script checks the bound and cases.
- Theorem 5 (finite-geometry counts over GF(3), GF(4), GF(16); the ovoid of PG(3,4)): script, exact enumeration.

A Lean proof can be wrong only in its statements; a referee should check the statements above against the README, not the proofs.
