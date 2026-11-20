# Lean audit: The Spatial Geometry of the Lorentz Tetrad

| | |
|---|---|
| **Formalisation** | [`lean/ForcedTetrahedralFrame.lean`](lean/ForcedTetrahedralFrame.lean), 1,316 lines, Lean 4.36.0 + Mathlib v4.36.0 (pinned in `lean/lakefile.toml` and `lean/lake-manifest.json`) |
| **Build** | 0 errors · 0 warnings · no `sorry` / `admit` / custom `axiom` / `native_decide` / `unsafe` |
| **Axioms** | All 43 `#print axioms` checks report only `propext`, `Classical.choice`, `Quot.sound` |
| **Reproduce** | `cd lean && lake exe cache get && lake build` |
| **Paper** | Revised as v2 ([`forced_tetrahedral_frame.tex`](forced_tetrahedral_frame.tex) / [`.pdf`](forced_tetrahedral_frame.pdf)). Every statement in it maps to a theorem below. |

**Verdict.** Every mathematical claim of v1 is correct. Two wording defects in Corollary 2 are fixed in v2. The premises are derived from the tetrad's own structure (basis, unit magnitudes, orthogonality), and each one is shown to be necessary. The single input that is not mathematics is the transcription principle: *the spatial picture keeps what a squared length can carry.* It is stated as a definition, and everything downstream of it is machine-checked.

---

## 1. How to referee the formalisation

Lean checks every proof. A referee needs to check only that the **definitions and statements** mean what the paper says. That trusted base is listed here in full.

| Lean definition | Paper meaning |
|---|---|
| `gram v a b = v a ⬝ᵥ v b` | Gram matrix G |
| `PremR v := ∃ β, ∀ a ≠ b, v a·v b = β` | (R) equal relation |
| `PremM v c := 0 < c ∧ ∀ a, v a·v a = c²` | (M) equal magnitude; `premM_iff_norm` proves this is exactly \|vₐ\| = c > 0 |
| `PremN v := ∃ a b, v a ≠ v b` | (N) not all equal |
| ambient type `Fin D → ℝ` | (D); `positive_index` / `etaG_positive_index` prove D = positive index of η |
| `Realisation K D v c` | (R) ∧ (M) ∧ (N) |
| `Forced K D` | every realisation is closed with G_ab = −c²/(K−1) |
| `eta = diag(−1,1,1,1)`, `mink x y = −x₀y₀ + x₁y₁ + x₂y₂ + x₃y₃` | Minkowski metric |
| `IsTetrad e := ∀ a b, mink (e a) (e b) = eta a b` | e is a tetrad (any boost or rotation of the standard frame) |
| `PreservesMagnitude e v c := 0 < c ∧ ∀ a, \|vₐ\|² = c²·\|η(eₐ,eₐ)\|` | lengths carry the legs' magnitudes |
| `PreservesRelation e v` | equal η(eₐ,e_b) ⇒ equal vₐ·v_b (a ≠ b) |
| `etaG n s = diag(−s, s, …, s)`, `Transcribes f g M v` | signature (1,n), convention s = ±1; local, label-blind transcription |

---

## 2. The paper's results

| Paper (v2) | Lean | Remark |
|---|---|---|
| Legs form a basis; each η_aa = sign × 1 | `tetrad_basis`, `eta_sign_times_magnitude`, `tetrad_unit_magnitude` | new in v2 |
| (M) + (R) ⇔ S₄-invariance of G | `gram_perm_invariant` | |
| Rigidity Lemma | `rigidity` | proved for any number of columns |
| Theorem: closure and Eq. (1) | `forced_gram`, `forced_gram_entries` | via linear dependence; the paper's eigenvalue route is also sound |
| The value 0 of (R) cannot be kept in ℝ³ | `no_orthogonal_tetrad` | |
| Corollary 1 | `cor1_geometry`, `cor1_M_realises`, `MtM`, `cor1_unique` | angle stated as cos θ = −1/3 |
| Corollary 2 | `cor2_exists_iff`, `cor2_forced_iff`, `three_is_unique` | K ≥ 2 required (`K_one_no_realisation`); "exists **and** forced" (`forced_vacuous`) |
| Corollary 2, D ≥ K | `cor2_all_gram_realisable` | every α > 0, α + Kβ ≥ 0, not only β = 0 |
| Corollary 3 | `cor3_parity`, `cor3_cube` | |
| Necessity table | `nec_R`, `nec_M1`, `nec_M2`, `nec_M2_rank`, `nec_N`, `nec_D` | (M)-row vectors are explicit; rank 3 proved |

---

## 3. The premises from the tetrad (primary derivation)

A tetrad is a **basis of unit vectors**. e₀ is a unit *timelike* vector: η₀₀ = −(1) is the same magnitude 1 as every other leg, and the sign records the vector's type, not its size. (A frame with diagonal (−0.9, 0.4, 1, 1) is not a tetrad.)

| Result | Lean |
|---|---|
| The legs are linearly independent; each is non-zero | `tetrad_basis` |
| η_aa = (sign)·\|η_aa\| with \|η_aa\| = 1 on every leg | `eta_sign_times_magnitude` |
| **For any tetrad**: magnitude- and relation-preserving, (N), ℝ³ ⇒ closed regular tetrahedron, Eq. (1), unique Q ∈ O(3) | `normalisation_forces_tetrahedron` |
| The observer's projection sends a unit vector to the zero vector, and violates the hypothesis on that leg only | `observer_breaks_normalisation`, `observer_violates_only_time_leg` |
| The hypotheses are satisfiable (M's columns, c = √3) | `normalisation_satisfiable` |

(M) is the normalisation of the frame, (R) is its orthogonality pattern, and (N) is its independence. Only the sign is set aside, because no squared length can be negative.

## 4. Independent route: local, label-blind, convention-independent

Rules: **Local** (G_aa = f(η_aa), G_ab = g(η_ab)); **Label-blind** (the same f, g for every leg); **Convention-independent** (one picture for (−,+,+,+) and (+,−,−,−)); **Faithful** (N); **Dimension** (D = positive index).

| Result | Lean |
|---|---|
| Rules ⇒ closed regular **n-simplex** for any signature (1,n) | `rules_force_simplex` |
| n = 3: tetrahedron, Eq. (1), unique Q ∈ O(3) | `tetrahedron_from_rules` |
| The time leg can sit at any position | `time_leg_anywhere`, `transcribes_relabel` |
| Satisfiable | `rules_satisfiable`, `rules_satisfiable_general` |
| Each rule is necessary | `need_convention_independence`, `need_covariance`, `need_locality`, `need_faithfulness`, `need_dimension` |

The locality counterexample (`traceRule`) is itself proved label-blind and convention-independent (`traceRule_covariant`), so it violates locality alone.

## 5. The symmetry view

η's own symmetry group is S₃, the permutations fixing the time leg (`aut_eta`). It does not force the tetrahedron (`lorentz_symmetry_alone_not_forced`). Because S₃ is maximal in S₄, adding any single permutation that moves the time leg forces the full S₄ structure and hence the tetrahedron (`extension_forces_S4`, `any_extension_beyond_lorentz_forces`). Sign-stripping gives |η| = I, whose symmetry group is all of S₄ (`aut_absEta`, `transcription_forces_tetrahedron`).

---

## 6. Anticipated referee objections

**"(M) is assumed."** It is the normalisation of the frame (`tetrad_unit_magnitude`). Two independent routes derive it: §3 and §4.

**"The premises are tailored."** Each premise and each rule is necessary, by an explicit machine-checked counterexample. The result holds for every signature (1,n), not only for four legs.

**"The theorem might be vacuous."** The hypotheses are satisfiable (`normalisation_satisfiable`, `rules_satisfiable_general`).

**"Why keep magnitudes?"** They are what the tetrad fixes; dropping them is exactly what the observer's projection does (`observer_breaks_normalisation`). The principle itself is physics, stated as a definition. Lean shows what follows from it and what fails without it.

**"The proof route differs from the paper."** The formal proof uses linear dependence. v2 records this route in a Remark after the Theorem. The two routes are equivalent.

---

## 7. Changes made in the paper (v2)

| Location | Change | Backed by |
|---|---|---|
| Abstract | Premises read off the tetrad; −1 described as a unit magnitude with a timelike sign; (1,n) result; Lean verification | §3, §4 |
| Setting | Legs form a basis; each η_aa is a sign × 1 | `tetrad_basis`, `eta_sign_times_magnitude` |
| (M), (N) | (M) justified by normalisation; (N) tied to independence and noted as weaker | `tetrad_unit_magnitude`, `tetrad_basis` |
| After the Theorem | Remark: the linear-dependence route | `core_forced` |
| Corollary 2 | K ≥ 2; "exists and is forced"; every admissible Gram matrix realised for D ≥ K | `cor2_*`, `K_one_no_realisation`, `forced_vacuous` |
| Necessity table, (M) row | Explicit vectors; rank 3; projection described as sending a unit vector to zero | `nec_M2`, `nec_M2_rank`, `observer_breaks_normalisation` |
| New section: the premises from the tetrad | Normalisation theorem; independent route; (1,n) simplex | `normalisation_forces_tetrahedron`, `rules_force_simplex`, `need_*` |
| New section: formal verification | Statement-to-theorem table; Lean 4 and Mathlib citations | the whole file |
| Summary | Aligned with the normalisation reading | |

Nothing else was changed. Every edit is marked `% v2:` in the source. The Python verifier gained eight matching checks (35/35).

---

## 8. Review log (issues found in the formalisation and fixed)

1. **Hidden rule:** a single f for all legs was implicit. Label-blindness is now an explicit rule and proved necessary.
2. **Unfair counterexample:** the old non-local rule referenced leg 1. It is replaced by the label-blind `traceRule`.
3. **Over-strong hypothesis:** injectivity is weakened to (N).
4. **Missing uniqueness:** the headline theorems now include the unique Q ∈ O(3).
5. **Hard-wired K = 4:** generalised to signature (1,n).
6. **Numeric-only claim:** rank 3 of the (M) row is now proved.
7. **Vacuity:** satisfiability is now proved.
8. **Hygiene:** a deprecated import, deprecated names and 73 warnings, now 0.

## 9. Limits

- **Angle:** stated as cos θ = −1/3. `Real.arccos` would need a much heavier build.
- **"Stella octangula":** a name. Lean proves the eight vertices are {−1,+1}³ split into the two tetrahedra.
- **Physics:** the transcription principle is the paper's to argue; everything that follows from it is verified.
