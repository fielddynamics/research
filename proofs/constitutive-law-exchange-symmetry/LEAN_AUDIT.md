# Lean audit: The Constitutive Law from Exchange Symmetry

| | |
|---|---|
| **Formalisation** | [`lean/ConstitutiveLaw.lean`](lean/ConstitutiveLaw.lean), 439 lines, Lean 4.36.0 + Mathlib v4.36.0 |
| **Depends on** | Mathlib only. Premise (X) enters as a closure property of the realised states; the geometry behind it is the subject of the [tetrad scheme](../tetrad-scheme-two-bounded-regions/) and [half-space](../half-space-two-bounded-regions/) proofs |
| **Build** | 0 errors · 0 warnings · no `sorry` / `admit` / custom `axiom` / `native_decide` |
| **Axioms** | All 8 `#print axioms` checks report only `propext`, `Classical.choice`, `Quot.sound` |
| **Reproduce** | `cd lean && lake exe cache get && lake build` |
| **CI** | `.github/workflows/lean-constitutive-law.yml` |

**Verdict.** The Theorem, its Consequences, the parity form and every row of the necessity table are proved. Two standard facts are cited, as in the note: the field degrees in the Lemma (Gauss's lemma) and the irreducibility of the (A) alternatives (Eisenstein).

## 1. Definitions to check against the paper

| Lean | Paper |
|---|---|
| `rel a b c d x m : a x m + b x + c m + d = 0` | the relation of (A), `P = a x̃ μ + b x̃ + c μ + d` |
| hypothesis `a d − b c ≠ 0` | irreducibility of the bilinear `P` (Lemma) |
| `μ : ℝ → ℝ` with `rel` and `0 ≤ μ x ≤ 1` for `x ≥ 0` | `μ(x̃) ∈ [0, 1]`, a function of the acceleration |
| `states a b μ = {μ x : x ≥ 0} ∪ {m ∈ [0,1] : a m + b = 0}` | the partition states realised on `[0, ∞]`; at `x̃ = ∞` the relation's projective closure in `x̃`, `x̃(a μ + b) + (c μ + d) = 0`, reads `a μ + b = 0` |
| (E) `μ 0 = 0`; (X) `∀ m ∈ states, 1 − m ∈ states` | (E), (X) |
| `law x = x/(x + 1)` | Eq. (3) |
| `relA n m x y : xⁿ(1 − y)ᵐ = y` | the (A) row of the table |

## 2. Statements

| Paper | Lean | Notes |
|---|---|---|
| Lemma | `lemma_bilinear` | If `ad − bc = 0` (and the degrees are one), `P = (x + t)(a y + b)`; if `ad − bc ≠ 0`, each variable is fractional linear in the other, and `a x + c = 0` admits no `y`. The field degrees `[K(x,y):K(x)] = m` are cited |
| Theorem, Steps 1–3 | `unique_law` | Concludes `d = 0`, `a + b = 0` and `μ x = law (k x)` for a unique `k > 0` (so `a₀ = g_*/k` is unique). Step 2 is proved by `μ(1 − μ) ≥ 0`: `−b((a+b)x + c) ≥ 0` for all `x > 0` is impossible when the pole is at a positive `x₀` |
| Consequences | `consequences` | Screening identity; `μ(0) = 0`, `μ(1) = ½`; `μ → 1` (a `Tendsto` statement); `μ(x) + μ(1/x) = 1`; `(x, μ) → (1/x, 1 − μ)` preserves the relation; `μ` strictly increasing, so the exchanged state is at `1/x` and nowhere else; `ι ∘ ι = id`; fixed point `x = 1` |
| Parity form | `parity_form` | `s = (x − 1)/(x + 1)`, `x(1 − s) = 1 + s`, `s(1/x) = −s(x)`, and `(f(K,s) − f(K,−1))/2K = (1 + s)/2` |
| Necessity: (E) | `need_E` | `b = ½`: all other hypotheses hold, `μ(0) = 1/3` |
| Necessity: (X) | `need_X` | `μ = x/(2x + 1)`: all other hypotheses hold, the state `1` is never realised |
| Necessity: (A) | `need_A` | Every `n, m ≥ 1`: unique root in `[0, 1]` for each `x ≥ 0` (intermediate value theorem and monotonicity), `μ(0) = 0`, states `= [0, 1]` with `μ = 1` at `x = ∞`, and for `(n, m) ≠ (1, 1)` not `law (k x)` for any `k > 0` |
| "Without (A) the exchange carries no content" | `no_content_without_A` | Any continuous `μ` with `μ(0) = 0`, values in `[0, 1]` and `μ → 1` has states `[0, 1]` |

## 3. Notes for a referee

- **`x̃ = ∞`.** The note works on `[0, ∞]`. Lean keeps `x ≥ 0` real and reads the state at infinity off the projective closure of the relation, which is what "realised at `x̃ = ∞`" means for an algebraic relation. In Step 2 the case `γ = 0` is exactly the case where `μ = 1` is realised there.
- **Strict monotonicity** is the precise form of "μ is single-valued in x, so the exchanged state sits at 1/x".
- **Physics.** That TetA and TetB exist and are exchanged by parity, and that the unbound coupling is one-directional, are the framework's premises; the proof shows only that the law follows from them.
