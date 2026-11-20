# Lean audit: The Stellated Octahedron, the Cube and the Hadamard Matrix

| | |
|---|---|
| **Formalisation** | [`lean/HadamardCubeFrame.lean`](lean/HadamardCubeFrame.lean), 786 lines, Lean 4.36.0 + Mathlib v4.36.0 |
| **Depends on** | [`../forced-tetrahedral-frame/lean/`](../forced-tetrahedral-frame/lean/) (imported, not copied) |
| **Build** | 0 errors · 0 warnings · no `sorry` / `admit` / custom `axiom` / `native_decide` |
| **Axioms** | All 19 `#print axioms` checks report only `propext`, `Classical.choice`, `Quot.sound` |
| **Reproduce** | `cd lean && lake exe cache get && lake build` |
| **CI** | `.github/workflows/lean-hadamard-cube-frame.yml`, on every change to this proof or the one it imports |

**Verdict.** Every statement of the paper is proved, and several in more generality than the verification script checks them.

## 1. Definitions to check against the paper

| Lean | Paper |
|---|---|
| `IsSign A`: every entry is `±1` | sign matrix |
| `col M a` | the column `v_a`, a point of `Q_D` |
| `IsCubeSimplex M`: sign matrix, distinct columns, one common squared distance | cube simplex: `D + 1` distinct, pairwise equidistant points of `Q_D` |
| `Hhat M`: a row of ones on top of `M` | `Ĥ` |
| `IsHadamard H`: sign matrix with `HᵀH = nI` | Hadamard matrix |
| `cubeQ D`, `simplexAndImage M` | `Q_D` and `V ∪ (−V)` as finite sets of points |
| `chi S x = ∏_{i∈S} x_i`; `evenS`, `oddS`; `walsh M` | Walsh functions, their stated order, and `W` with columns `v₀…v₃, −v₀…−v₃` |
| `Matrix.fromBlocks Ĥ Ĥ Ĥ (−Ĥ)` | `H₂ ⊗ Ĥ` |
| `splitOf S = {S, Sᶜ}`; `allSplits K`; `plusSet M i`; `rowSplits M` | a split into two halves; all such splits; the `+1` set of a row; the splits given by the rows |

## 2. Statements

| Paper | Lean | Scope compared with the script |
|---|---|---|
| Theorem 1, (a)⇔(b)⇔(c)⇔(d) | `theorem1` | Every `D ≥ 1` (the script: all matrices `D ≤ 3`, samples at `D = 7`). (a)⇒(b) is `ForcedTetrahedralFrame.general_forced` |
| Remark: normalised Hadamard matrices = cube simplices | `normalise_hadamard` | General |
| Lemma (Hadamard) | `hadamard_four_dvd` | Every order `n > 2` (the script: orders 3 and 5 by search). Proved by the equivalent count `Σ_c (1 + r₂)(1 + r₃) = n`, each term `0` or `4` |
| Corollary 1 | `corollary1`, `no_cube_simplex_two`, `cube_simplex_three` | General |
| Theorem 2 | `theorem2` | Every `D ≥ 2`: `−V` a cube simplex, disjoint, `|V ∪ −V| = 2(D+1)`, `V ∪ −V = Q_D ⇔ D = 3` (`two_succ_eq_pow_iff`, `card_cubeQ`) |
| Theorem 2, `D = 3` parity classes | `theorem2_parity_classes` | Any cube simplex in `Q₃` |
| Theorem 3, `W = H₂ ⊗ Ĥ` | `theorem3`, `theorem3_M` | Any ordering of the parity class `+1`; `chi_neg` for `χ_S(−x)` |
| Remark: each Walsh function equals its complement up to a common sign | `chi_compl` | Every point of `Q₃` |
| Corollary 2 | `corollary2`: `rowSplits ⊆ allSplits`, `|rowSplits| = K − 1`, `2·|allSplits| = C(K, K/2)`, and **`rowSplits = allSplits ⇔ K = 2 ∨ K = 4`**; parts `corollary2_balanced`, `corollary2_distinct_splits`, `corollary2_halves`, `corollary2_count`, `corollary2_pairs` | Every cube simplex; `K` even is derived from Corollary 1, not assumed |

## 3. Notes for a referee

- **Corollary 2 is stated as the paper states it.** The splits are defined as objects (`allSplits`, `rowSplits`), and the theorem `corollary2` proves the sentence "the rows are all such splits iff `K = 2` or `K = 4`" itself, with the counting (each split is exactly two halves) proved rather than assumed.
- **"Stella octangula".** A name. Lean proves the eight vertices are the two parity classes of `Q₃`.
- **Not paper claims.** The script also checks that `W` is a Hadamard matrix of order 8; the paper does not claim this, so it is not formalised.
