import Mathlib.Analysis.Real.Sqrt
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.LinearAlgebra.UnitaryGroup
import Mathlib.Tactic.LinearCombination

/-!
# Lean 4 / Mathlib formalisation of
#   S. Nelson, "The Spatial Geometry of the Lorentz Tetrad" (Field Dynamics Research, preprint)

Checked with Lean 4.36.0 and Mathlib v4.36.0: Lean reports no errors or warnings for this file,
there is no `sorry`, and there are no custom axioms. Every theorem depends only on `propext`,
`Classical.choice`, `Quot.sound` (see the `#print axioms` lines). GitHub Actions re-checks all of
this whenever the file changes.

## How to referee this file
A Lean proof can only be wrong in its *statements*: the proofs are machine-checked. A referee
therefore needs to check only the following definitions and theorem statements against the paper.

Definitions (the trusted base):
* `gram v a b = v a ⬝ᵥ v b` (Euclidean Gram matrix); `J` all-ones; `Vmat` legs as columns.
* `PremR`, `PremM`, `PremN`: premises (R), (M), (N); (D) is the ambient type `Fin D → ℝ`.
  `premM_iff_norm` shows `PremM` is exactly `|v_a| = c > 0`.
* `Realisation K D v c := PremR v ∧ PremM v c ∧ PremN v`.
* `Exists' K D`, `Forced K D`: existence of a realisation / every realisation is the closed simplex.
* `eta = diag(−1, 1, 1, 1)`, `mink x y = −x₀y₀ + x₁y₁ + x₂y₂ + x₃y₃`: the Minkowski metric.
* `IsTetrad e := ∀ a b, mink (e a) (e b) = eta a b`: `e` is a tetrad (any frame with this Gram
  matrix, i.e. any Lorentz transform of the standard frame, reflections included).
* `PreservesMagnitude e v c := 0 < c ∧ ∀ a, |v_a|² = c²·|η(e_a, e_a)|`;
  `PreservesRelation e v`: equal `η(e_a, e_b)` (`a ≠ b`) give equal `v_a · v_b`.
* `etaG n s = diag(−s, s, …, s)`: tetrad metric of signature `(1,n)`, convention `s = ±1`.
* `Transcribes f g M v`: `G_aa = f(M_aa)`, `G_ab = g(M_ab)` with the same `f, g` for every leg
  (rules *Local* + *Covariant*, the paper's "label-blind").

Headline results (in the order of the paper):
* `forced_gram`, `rigidity`, `cor1_*`, `cor2_*`, `cor3_*`, `nec_*`: the paper's results as stated.
* `tetrad_basis`, `eta_sign_times_magnitude`, `tetrad_unit_magnitude`: the legs are a basis of unit
  vectors, each `η_aa` a sign times the common magnitude `1`.
* `normalisation_forces_tetrahedron`: for any tetrad, a magnitude- and relation-preserving
  realisation is the closed regular tetrahedron, unique up to `O(3)` (the primary derivation);
  `observer_breaks_normalisation`, `observer_violates_only_time_leg`, `normalisation_satisfiable`.
* `rules_force_simplex` / `tetrahedron_from_rules`: the independent route, for any signature
  `(1,n)`; `rules_satisfiable(_general)` (not vacuous); `need_convention_independence`,
  `need_covariance`, `need_locality`, `need_faithfulness`, `need_dimension` (each rule necessary).
* `aut_eta`, `extension_forces_S4`: the symmetry view (`S₃` is maximal in `S₄`).
-/

open Matrix Finset

namespace ForcedTetrahedralFrame

/-! ## Definitions -/

/-- Gram matrix `G_ab = v_a · v_b`. -/
def gram {K D : ℕ} (v : Fin K → Fin D → ℝ) : Matrix (Fin K) (Fin K) ℝ :=
  Matrix.of fun a b => v a ⬝ᵥ v b

/-- The all-ones matrix `J`. -/
def J (K : ℕ) : Matrix (Fin K) (Fin K) ℝ := Matrix.of fun _ _ => 1

def PremR {K D : ℕ} (v : Fin K → Fin D → ℝ) : Prop := ∃ β : ℝ, ∀ a b, a ≠ b → v a ⬝ᵥ v b = β
def PremM {K D : ℕ} (v : Fin K → Fin D → ℝ) (c : ℝ) : Prop := 0 < c ∧ ∀ a, v a ⬝ᵥ v a = c ^ 2
def PremN {K D : ℕ} (v : Fin K → Fin D → ℝ) : Prop := ∃ a b, v a ≠ v b

/-- (R), (M), (N) for `K` legs in `ℝ^D`; (D) is the choice `D = 3`. -/
def Realisation (K D : ℕ) (v : Fin K → Fin D → ℝ) (c : ℝ) : Prop :=
  PremR v ∧ PremM v c ∧ PremN v

/-- The matrix `V ∈ ℝ^{D×K}` whose columns are the legs. -/
def Vmat {K D : ℕ} (v : Fin K → Fin D → ℝ) : Matrix (Fin D) (Fin K) ℝ := Matrix.of fun i a => v a i

lemma Vmat_gram {K D : ℕ} (v : Fin K → Fin D → ℝ) : (Vmat v)ᵀ * Vmat v = gram v := by
  ext a b; rw [Matrix.mul_apply]; simp [Vmat, gram, dotProduct]

/-- (M) in the paper's form `|v_a| = c > 0`, with `|x| = √(x·x)`. -/
lemma premM_iff_norm {K D : ℕ} (v : Fin K → Fin D → ℝ) (c : ℝ) :
    PremM v c ↔ 0 < c ∧ ∀ a, Real.sqrt (v a ⬝ᵥ v a) = c := by
  constructor
  · rintro ⟨hc, h⟩; exact ⟨hc, fun a => by rw [h a, Real.sqrt_sq hc.le]⟩
  · rintro ⟨hc, h⟩
    refine ⟨hc, fun a => ?_⟩
    have h0 : 0 ≤ v a ⬝ᵥ v a := by
      unfold dotProduct; exact Finset.sum_nonneg (fun i _ => mul_self_nonneg (v a i))
    rw [← h a, Real.sq_sqrt h0]

/-! ## Basic lemmas -/

lemma dot_self_nonneg {n : ℕ} (w : Fin n → ℝ) : 0 ≤ w ⬝ᵥ w := by
  unfold dotProduct; exact Finset.sum_nonneg (fun i _ => mul_self_nonneg (w i))

lemma dot_self_pos {n : ℕ} {w : Fin n → ℝ} (h : w ≠ 0) : 0 < w ⬝ᵥ w :=
  lt_of_le_of_ne (dot_self_nonneg w) (fun h' => h (dotProduct_self_eq_zero.mp h'.symm))

/-- "(M) and (R) say that G is invariant under every permutation of the legs." -/
theorem gram_perm_invariant {K D : ℕ} (v : Fin K → Fin D → ℝ) (c β : ℝ)
    (hM : ∀ a, v a ⬝ᵥ v a = c ^ 2) (hR : ∀ a b, a ≠ b → v a ⬝ᵥ v b = β)
    (σ : Equiv.Perm (Fin K)) (a b : Fin K) : gram v (σ a) (σ b) = gram v a b := by
  simp only [gram, of_apply]
  by_cases h : a = b
  · subst h; rw [hM, hM]
  · rw [hR _ _ (σ.injective.ne h), hR _ _ h]

/-- `|v_a - v_b|² = 2α` with `α = c² - β`, and (N) forces `α > 0`. -/
lemma dist_sq {K D : ℕ} (v : Fin K → Fin D → ℝ) (c β : ℝ)
    (hM : ∀ a, v a ⬝ᵥ v a = c ^ 2) (hR : ∀ a b, a ≠ b → v a ⬝ᵥ v b = β)
    {a b : Fin K} (hab : a ≠ b) : (v a - v b) ⬝ᵥ (v a - v b) = 2 * (c ^ 2 - β) := by
  rw [sub_dotProduct, dotProduct_sub, dotProduct_sub, hM, hM, hR a b hab, hR b a (Ne.symm hab)]
  ring

lemma alpha_pos {K D : ℕ} (v : Fin K → Fin D → ℝ) (c β : ℝ)
    (hM : ∀ a, v a ⬝ᵥ v a = c ^ 2) (hR : ∀ a b, a ≠ b → v a ⬝ᵥ v b = β)
    (hN : PremN v) : 0 < c ^ 2 - β := by
  obtain ⟨a, b, hab⟩ := hN
  have hne : a ≠ b := fun h => hab (by rw [h])
  have := dot_self_pos (sub_ne_zero.mpr hab)
  rw [dist_sq v c β hM hR hne] at this
  linarith

lemma two_le_K {K D : ℕ} {v : Fin K → Fin D → ℝ} (hN : PremN v) : 2 ≤ K := by
  obtain ⟨a, b, hab⟩ := hN
  have hne : a ≠ b := fun h => hab (by rw [h])
  have : a.val ≠ b.val := fun h => hne (Fin.ext h)
  omega

/-- Row `b` of `G g`: `(Σ_a g_a v_a)·v_b = α g_b + β Σ_a g_a`. -/
lemma comb_dot {K D : ℕ} (v : Fin K → Fin D → ℝ) (c β : ℝ)
    (hM : ∀ a, v a ⬝ᵥ v a = c ^ 2) (hR : ∀ a b, a ≠ b → v a ⬝ᵥ v b = β)
    (g : Fin K → ℝ) (b : Fin K) :
    (∑ a, g a • v a) ⬝ᵥ v b = (c ^ 2 - β) * g b + β * ∑ a, g a := by
  rw [sum_dotProduct]
  have h : ∀ a, (g a • v a) ⬝ᵥ v b = β * g a + if a = b then (c ^ 2 - β) * g a else 0 := by
    intro a
    rw [smul_dotProduct, smul_eq_mul]
    by_cases hab : a = b
    · subst hab; rw [hM, ite_eq_left rfl]; ring
    · rw [hR a b hab, ite_eq_right hab]; ring
  rw [Finset.sum_congr rfl (fun a _ => h a), Finset.sum_add_distrib, ← Finset.mul_sum,
    Finset.sum_ite_eq']
  simp only [Finset.mem_univ, ite_true]
  ring

/-- Any linear dependency among the legs has all coefficients equal. -/
lemma dep_const {K D : ℕ} (v : Fin K → Fin D → ℝ) (c β : ℝ)
    (hM : ∀ a, v a ⬝ᵥ v a = c ^ 2) (hR : ∀ a b, a ≠ b → v a ⬝ᵥ v b = β)
    (hα : 0 < c ^ 2 - β) (g : Fin K → ℝ) (hg : ∑ a, g a • v a = 0) (a b : Fin K) :
    g a = g b := by
  have h : ∀ b, (c ^ 2 - β) * g b + β * ∑ a, g a = 0 := fun b => by
    rw [← comb_dot v c β hM hR g b, hg, zero_dotProduct]
  have ha := h a
  have hb := h b
  have : (c ^ 2 - β) * g a = (c ^ 2 - β) * g b := by linarith
  exact mul_left_cancel₀ hα.ne' this

/-- More legs than dimensions ⇒ a nontrivial dependency. -/
lemma exists_dep {K D : ℕ} (hDK : D < K) (v : Fin K → Fin D → ℝ) :
    ∃ g : Fin K → ℝ, ∑ a, g a • v a = 0 ∧ ∃ i, g i ≠ 0 := by
  have : ¬ LinearIndependent ℝ v := by
    intro hli
    have := hli.fintype_card_le_finrank
    rw [Module.finrank_fin_fun, Fintype.card_fin] at this
    omega
  exact Fintype.not_linearIndependent_iff.mp this

/-- Core: if `D < K`, (R),(M),(N) force `α + Kβ = 0` and closure `Σ v_a = 0`. -/
theorem core_forced {K D : ℕ} (hDK : D < K) (v : Fin K → Fin D → ℝ) (c β : ℝ)
    (hM : ∀ a, v a ⬝ᵥ v a = c ^ 2) (hR : ∀ a b, a ≠ b → v a ⬝ᵥ v b = β) (hN : PremN v) :
    (c ^ 2 - β) + (K : ℝ) * β = 0 ∧ ∑ a, v a = 0 := by
  have hα := alpha_pos v c β hM hR hN
  obtain ⟨g, hg, i, hi⟩ := exists_dep hDK v
  have hconst := dep_const v c β hM hR hα g hg
  have hgμ : ∀ a, g a = g i := fun a => hconst a i
  -- Σ g_a v_a = g_i Σ v_a
  have hsum : ∑ a, v a = 0 := by
    have : g i • ∑ a, v a = 0 := by
      rw [Finset.smul_sum, ← hg]; exact Finset.sum_congr rfl (fun a _ => by rw [hgμ a])
    exact (smul_eq_zero.mp this).resolve_left hi
  have hrow := comb_dot v c β hM hR g i
  rw [hg, zero_dotProduct] at hrow
  have hS : ∑ a, g a = (K : ℝ) * g i := by
    rw [Finset.sum_congr rfl (fun a _ => hgμ a), Finset.sum_const, Finset.card_univ,
      Fintype.card_fin, nsmul_eq_mul]
  rw [hS] at hrow
  have : g i * ((c ^ 2 - β) + (K : ℝ) * β) = 0 := by linarith
  exact ⟨(mul_eq_zero.mp this).resolve_left hi, hsum⟩

/-- General form: `K` legs in `ℝ^D` with `D < K` ⇒ closed, with `G_ab = -c²/(K-1)` off the diagonal. -/
theorem general_forced {K D : ℕ} (hDK : D < K) (v : Fin K → Fin D → ℝ) (c : ℝ)
    (h : Realisation K D v c) :
    ∑ a, v a = 0 ∧ ∀ a b, a ≠ b → v a ⬝ᵥ v b = -c ^ 2 / ((K : ℝ) - 1) := by
  obtain ⟨⟨β, hR⟩, ⟨hc, hM⟩, hN⟩ := h
  obtain ⟨h1, h2⟩ := core_forced hDK v c β hM hR hN
  have hK : (2 : ℝ) ≤ K := by exact_mod_cast two_le_K hN
  refine ⟨h2, fun a b hab => ?_⟩
  rw [hR a b hab, eq_div_iff (by linarith)]
  linarith

/-! ## Rigidity Lemma -/

lemma isUnit_of_rank_eq {n : ℕ} (A : Matrix (Fin n) (Fin n) ℝ) (h : A.rank = n) : IsUnit A := by
  rw [← mulVec_surjective_iff_isUnit]
  have htop : LinearMap.range A.mulVecLin = ⊤ := by
    apply Submodule.eq_top_of_finrank_eq
    rw [Module.finrank_fin_fun]; exact h
  intro y
  have : y ∈ LinearMap.range A.mulVecLin := htop ▸ Submodule.mem_top
  obtain ⟨x, hx⟩ := this
  exact ⟨x, hx⟩

/-- Over `ℝ`, `XᵀX = 0 → X = 0`. -/
lemma transpose_mul_self_eq_zero {m n : ℕ} {X : Matrix (Fin m) (Fin n) ℝ} (h : Xᵀ * X = 0) :
    X = 0 := by
  ext i j
  have hj := congrFun (congrFun h j) j
  rw [Matrix.mul_apply, Matrix.zero_apply] at hj
  simp only [transpose_apply] at hj
  have := (Finset.sum_eq_zero_iff_of_nonneg (fun k _ => mul_self_nonneg (X k j))).mp hj i
    (Finset.mem_univ _)
  simpa using mul_self_eq_zero.mp this

/-- **Lemma (Rigidity).** If `UᵀU = WᵀW` has rank `D`, then `W = QU` for a unique `Q ∈ O(D)`.
(Stated for any number `N` of columns; the paper uses `N = 4`.) -/
theorem rigidity {D N : ℕ} (U W : Matrix (Fin D) (Fin N) ℝ) (hG : Uᵀ * U = Wᵀ * W)
    (hr : (Uᵀ * U).rank = D) :
    ∃! Q : Matrix (Fin D) (Fin D) ℝ, Q ∈ Matrix.orthogonalGroup (Fin D) ℝ ∧ W = Q * U := by
  have hrU : U.rank = D := by rw [← rank_transpose_mul_self]; exact hr
  obtain ⟨A, hA⟩ : ∃ A, A = U * Uᵀ := ⟨_, rfl⟩
  have hAu : IsUnit A := isUnit_of_rank_eq A (by rw [hA, rank_self_mul_transpose, hrU])
  have hAd : IsUnit A.det := (isUnit_iff_isUnit_det A).mp hAu
  obtain ⟨Q, hQ⟩ : ∃ Q, Q = W * Uᵀ * A⁻¹ := ⟨_, rfl⟩
  obtain ⟨P, hP⟩ : ∃ P, P = Uᵀ * A⁻¹ * U := ⟨_, rfl⟩
  have hUP : U * (1 - P) = 0 := by
    rw [hP, Matrix.mul_sub, Matrix.mul_one, ← Matrix.mul_assoc, ← Matrix.mul_assoc, ← hA,
      mul_nonsing_inv A hAd, Matrix.one_mul, sub_self]
  have hE : W - Q * U = W * (1 - P) := by
    rw [hQ, hP, Matrix.mul_sub, Matrix.mul_one]; simp only [Matrix.mul_assoc]
  have hEE : (W * (1 - P))ᵀ * (W * (1 - P)) = 0 := by
    calc (W * (1 - P))ᵀ * (W * (1 - P)) = (1 - P)ᵀ * (Wᵀ * W) * (1 - P) := by
          rw [transpose_mul]; simp only [Matrix.mul_assoc]
      _ = (1 - P)ᵀ * (Uᵀ * U) * (1 - P) := by rw [hG]
      _ = (U * (1 - P))ᵀ * (U * (1 - P)) := by rw [transpose_mul]; simp only [Matrix.mul_assoc]
      _ = 0 := by rw [hUP]; simp
  have hW0 : W * (1 - P) = 0 := transpose_mul_self_eq_zero hEE
  have hQU : Q * U = W := (sub_eq_zero.mp (hE.trans hW0)).symm
  have cancel : ∀ X, A⁻¹ * (A * X * A) * A⁻¹ = X := by
    intro X
    rw [Matrix.mul_assoc, Matrix.mul_assoc, mul_nonsing_inv A hAd, Matrix.mul_one,
      ← Matrix.mul_assoc, nonsing_inv_mul A hAd, Matrix.one_mul]
  have hQorth : Qᵀ * Q = 1 := by
    have h1 : Uᵀ * (Qᵀ * Q) * U = Uᵀ * U := by
      rw [hG, ← hQU, transpose_mul]; simp only [Matrix.mul_assoc]
    have h2 : A * (Qᵀ * Q) * A = A * 1 * A := by
      calc A * (Qᵀ * Q) * A = U * (Uᵀ * (Qᵀ * Q) * U) * Uᵀ := by
            rw [hA]; simp only [Matrix.mul_assoc]
        _ = U * (Uᵀ * U) * Uᵀ := by rw [h1]
        _ = A * 1 * A := by rw [hA]; simp only [Matrix.mul_one, Matrix.mul_assoc]
    rw [← cancel (Qᵀ * Q), h2, cancel]
  refine ⟨Q, ⟨(mem_orthogonalGroup_iff' (Fin D) ℝ).mpr hQorth, hQU.symm⟩, ?_⟩
  rintro Q' ⟨_, hQ'⟩
  have h3 : Q' * A = Q * A := by
    rw [hA, ← Matrix.mul_assoc, ← Matrix.mul_assoc, ← hQ', hQU]
  have h4 := congrArg (· * A⁻¹) h3
  simp only [Matrix.mul_assoc, mul_nonsing_inv A hAd, Matrix.mul_one] at h4
  exact h4

/-! ## Theorem (the forced Gram matrix), K = 4, D = 3 -/

/-- **Theorem.** Under (R), (M), (N), (D): the legs close and
`G = c² I − (c²/3)(J − I)`. -/
theorem forced_gram (v : Fin 4 → Fin 3 → ℝ) (c : ℝ) (h : Realisation 4 3 v c) :
    ∑ a, v a = 0 ∧ gram v = c ^ 2 • (1 : Matrix (Fin 4) (Fin 4) ℝ) - (c ^ 2 / 3) • (J 4 - 1) := by
  have hM := h.2.1.2
  obtain ⟨hsum, hoff⟩ := general_forced (by norm_num) v c h
  refine ⟨hsum, ?_⟩
  ext a b
  by_cases hab : a = b
  · subst hab; simp [gram, J, hM]
  · simp only [gram, J, of_apply, Matrix.sub_apply, Matrix.smul_apply, Matrix.one_apply_ne hab,
      smul_eq_mul]
    rw [hoff a b hab]; norm_num; ring

/-- Entrywise form: `G_aa = c²`, `G_ab = −c²/3`. -/
theorem forced_gram_entries (v : Fin 4 → Fin 3 → ℝ) (c : ℝ) (h : Realisation 4 3 v c)
    (a b : Fin 4) : v a ⬝ᵥ v b = if a = b then c ^ 2 else -c ^ 2 / 3 := by
  by_cases hab : a = b
  · subst hab; simp [h.2.1.2]
  · rw [ite_eq_right hab, (general_forced (by norm_num) v c h).2 a b hab]; norm_num

/-- The abstract's remark: the common value `0` of (R) cannot be kept in `ℝ³`. -/
theorem no_orthogonal_tetrad (v : Fin 4 → Fin 3 → ℝ) (c : ℝ) (hM : PremM v c) :
    ¬ ∀ a b, a ≠ b → v a ⬝ᵥ v b = 0 := by
  intro h0
  have hN : PremN v := by
    refine ⟨0, 1, fun h => ?_⟩
    have := h0 0 1 (by decide); rw [h, hM.2] at this
    exact absurd this (pow_ne_zero 2 hM.1.ne')
  have := forced_gram_entries v c ⟨⟨0, h0⟩, hM, hN⟩ 0 1
  rw [h0 0 1 (by decide), ite_eq_right (by decide)] at this
  have hc := hM.1; nlinarith

/-! ## Corollary 1 (the regular tetrahedron) -/

theorem cor1_geometry (v : Fin 4 → Fin 3 → ℝ) (c : ℝ) (h : Realisation 4 3 v c) :
    (∀ a b, a ≠ b → (v a - v b) ⬝ᵥ (v a - v b) = 8 * c ^ 2 / 3) ∧
    (∀ a b, a ≠ b → Real.sqrt ((v a - v b) ⬝ᵥ (v a - v b)) = c * Real.sqrt (8 / 3)) ∧
    (∑ a, v a = 0) ∧
    (∀ a, Real.sqrt (v a ⬝ᵥ v a) = c) ∧
    (∀ a b, a ≠ b →
      v a ⬝ᵥ v b / (Real.sqrt (v a ⬝ᵥ v a) * Real.sqrt (v b ⬝ᵥ v b)) = -1 / 3) := by
  have hc := h.2.1.1
  have hM := h.2.1.2
  have hE := forced_gram_entries v c h
  have hd : ∀ a b, a ≠ b → (v a - v b) ⬝ᵥ (v a - v b) = 8 * c ^ 2 / 3 := by
    intro a b hab
    rw [sub_dotProduct, dotProduct_sub, dotProduct_sub, hE a a, hE a b, hE b a, hE b b,
      ite_eq_left rfl, ite_eq_left rfl, ite_eq_right hab, ite_eq_right (Ne.symm hab)]
    ring
  have hn : ∀ a, Real.sqrt (v a ⬝ᵥ v a) = c := ((premM_iff_norm v c).mp h.2.1).2
  refine ⟨hd, fun a b hab => ?_, (core_forced (by norm_num) v c _ hM (h.1.choose_spec) h.2.2).2,
    hn, fun a b hab => ?_⟩
  · rw [hd a b hab, show 8 * c ^ 2 / 3 = c ^ 2 * (8 / 3) by ring,
      Real.sqrt_mul' _ (by norm_num), Real.sqrt_sq hc.le]
  · rw [hn, hn, hE a b, ite_eq_right hab]
    field_simp

/-- The matrix `M` of Eq. (2). -/
def Mmat : Matrix (Fin 3) (Fin 4) ℝ := !![1, 1, -1, -1; 1, -1, 1, -1; 1, -1, -1, 1]

def Mcol (a : Fin 4) : Fin 3 → ℝ := fun i => Mmat i a

lemma MtM_apply (a b : Fin 4) : (Mmatᵀ * Mmat) a b = if a = b then 3 else -1 := by
  rw [Matrix.mul_apply]; fin_cases a <;> fin_cases b <;> simp [Mmat, Fin.sum_univ_succ] <;> norm_num

/-- `MᵀM = 3I − (J − I)`. -/
lemma MtM : Mmatᵀ * Mmat = (3 : ℝ) • (1 : Matrix (Fin 4) (Fin 4) ℝ) - (J 4 - 1) := by
  ext a b; rw [MtM_apply]
  by_cases h : a = b
  · subst h; norm_num [J]
  · simp [J, h, Matrix.one_apply_ne h]

lemma MMt : Mmat * Mmatᵀ = (4 : ℝ) • (1 : Matrix (Fin 3) (Fin 3) ℝ) := by
  ext i j; rw [Matrix.mul_apply]; fin_cases i <;> fin_cases j <;> simp [Mmat, Fin.sum_univ_succ] <;> norm_num

/-- With `c = √3`, the columns of `M` realise Eq. (1) and satisfy all premises. -/
theorem cor1_M_realises : Realisation 4 3 Mcol (Real.sqrt 3) ∧
    ∀ a b, Mcol a ⬝ᵥ Mcol b = if a = b then (Real.sqrt 3) ^ 2 else -(Real.sqrt 3) ^ 2 / 3 := by
  have h3 : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hdot : ∀ a b, Mcol a ⬝ᵥ Mcol b = (Mmatᵀ * Mmat) a b := by
    intro a b; rw [Matrix.mul_apply]; simp [Mcol, dotProduct]
  refine ⟨⟨⟨-1, fun a b hab => ?_⟩, ⟨by positivity, fun a => ?_⟩, ⟨0, 1, fun h => ?_⟩⟩,
    fun a b => ?_⟩
  · rw [hdot, MtM_apply, ite_eq_right hab]
  · rw [hdot, MtM_apply, ite_eq_left rfl, h3]
  · have := congrFun h 1; simp [Mcol, Mmat] at this; norm_num at this
  · rw [hdot, MtM_apply, h3]; split_ifs <;> norm_num

/-- **Corollary 1 (uniqueness).** Every realisation is `V = Q · ((c/√3) M)` for a unique
`Q ∈ O(3)`. -/
theorem cor1_unique (v : Fin 4 → Fin 3 → ℝ) (c : ℝ) (h : Realisation 4 3 v c) :
    ∃! Q : Matrix (Fin 3) (Fin 3) ℝ,
      Q ∈ Matrix.orthogonalGroup (Fin 3) ℝ ∧ Vmat v = Q * ((c / Real.sqrt 3) • Mmat) := by
  have h3 : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hc := h.2.1.1
  have hk : (c / Real.sqrt 3) ^ 2 = c ^ 2 / 3 := by rw [div_pow, h3]
  apply rigidity
  · rw [Vmat_gram]
    ext a b
    rw [transpose_smul, Matrix.smul_mul, Matrix.mul_smul, smul_smul, Matrix.smul_apply,
      MtM_apply, smul_eq_mul, ← pow_two, hk]
    simp only [gram, of_apply]
    rw [forced_gram_entries v c h]
    split_ifs <;> ring
  · rw [rank_transpose_mul_self, ← rank_self_mul_transpose, transpose_smul, Matrix.smul_mul,
      Matrix.mul_smul, smul_smul, MMt, smul_smul]
    have hne : (c / Real.sqrt 3 * (c / Real.sqrt 3) * 4) ≠ 0 := by positivity
    have hu : IsUnit ((c / Real.sqrt 3 * (c / Real.sqrt 3) * 4) • (1 : Matrix (Fin 3) (Fin 3) ℝ)) := by
      rw [isUnit_iff_isUnit_det, det_smul, det_one, mul_one, isUnit_iff_ne_zero]
      exact pow_ne_zero _ hne
    rw [rank_of_isUnit _ hu, Fintype.card_fin]

/-! ## Corollary 2 (why three dimensions) -/

def Exists' (K D : ℕ) : Prop := ∃ v : Fin K → Fin D → ℝ, ∃ c, Realisation K D v c

/-- "Forced to the closed regular simplex": every realisation is closed with
`G_ab = −c²/(K−1)` for `a ≠ b`. -/
def Forced (K D : ℕ) : Prop :=
  ∀ (v : Fin K → Fin D → ℝ) (c : ℝ), Realisation K D v c →
    ∑ a, v a = 0 ∧ ∀ a b, a ≠ b → v a ⬝ᵥ v b = -c ^ 2 / ((K : ℝ) - 1)

/-- No realisation when `D < K − 1`. -/
theorem no_realisation {K D : ℕ} (hD : D + 1 < K) (v : Fin K → Fin D → ℝ) (c : ℝ) :
    ¬ Realisation K D v c := by
  rintro ⟨⟨β, hR⟩, ⟨_, hM⟩, hN⟩
  have hα := alpha_pos v c β hM hR hN
  let a₀ : Fin K := ⟨0, by omega⟩
  -- augmented vectors (v_a, [a = a₀]) ∈ ℝ^(D+1)
  let w : Fin K → Fin (D + 1) → ℝ := fun a => Fin.snoc (v a) (if a = a₀ then 1 else 0)
  obtain ⟨g, hg, i, hi⟩ := exists_dep hD w
  have h1 : ∑ a, g a • v a = 0 := by
    funext j
    have := congrFun hg (Fin.castSucc j)
    simpa [w, Finset.sum_apply, Fin.snoc_castSucc] using this
  have h2 : g a₀ = 0 := by
    have := congrFun hg (Fin.last D)
    simpa [w, Finset.sum_apply, Fin.snoc_last] using this
  exact hi (by rw [dep_const v c β hM hR hα g h1 i a₀, h2])

theorem K_one_no_realisation (D : ℕ) : ¬ Exists' 1 D := by
  rintro ⟨v, c, _, _, a, b, hab⟩
  exact hab (by rw [Subsingleton.elim a b])

/-- If `D ≥ K − 1` (i.e. `K < D + 2`) every realisation with `D < K` is forced. -/
theorem forced_of_lt {K D : ℕ} (hDK : D < K) : Forced K D :=
  fun v c h => general_forced hDK v c h

/-- Wording caveat: for `D < K − 1`, `Forced` holds *vacuously* (no realisations at all). -/
theorem forced_vacuous {K D : ℕ} (hD : D + 1 < K) : Forced K D :=
  fun v c h => absurd h (no_realisation hD v c)

/-- Sufficient criterion for (N). -/
lemma premN_of {K D : ℕ} (hK : 2 ≤ K) (v : Fin K → Fin D → ℝ) (c β : ℝ)
    (hM : ∀ a, v a ⬝ᵥ v a = c ^ 2) (hR : ∀ a b, a ≠ b → v a ⬝ᵥ v b = β) (hβ : β ≠ c ^ 2) :
    PremN v := by
  refine ⟨⟨0, by omega⟩, ⟨1, by omega⟩, fun h => hβ ?_⟩
  rw [← hR ⟨0, by omega⟩ ⟨1, by omega⟩ (by simp [Fin.ext_iff]), h, hM]

/-- Orthogonal legs `c·e_a` (`β = 0`) in `ℝ^D` for `K ≤ D`: a realisation that is not closed. -/
theorem orthogonal_realisation {K D : ℕ} (hK : 2 ≤ K) (hKD : K ≤ D) :
    ∃ v : Fin K → Fin D → ℝ, Realisation K D v 1 ∧ ∑ a, v a ≠ 0 ∧
      ∀ a b, a ≠ b → v a ⬝ᵥ v b = 0 := by
  let v : Fin K → Fin D → ℝ := fun a => Pi.single (Fin.castLE hKD a) 1
  have hdot : ∀ a b, v a ⬝ᵥ v b = if a = b then 1 else 0 := by
    intro a b
    simp only [v, single_dotProduct, one_mul, Pi.single_apply]
    by_cases h : a = b
    · simp [h]
    · rw [ite_eq_right h, ite_eq_right]; intro h'; exact h (Fin.castLE_injective hKD h')
  have hR : ∀ a b, a ≠ b → v a ⬝ᵥ v b = 0 := fun a b h => by rw [hdot, ite_eq_right h]
  have hM : ∀ a, v a ⬝ᵥ v a = 1 ^ 2 := fun a => by rw [hdot, ite_eq_left rfl]; norm_num
  refine ⟨v, ⟨⟨0, hR⟩, ⟨one_pos, hM⟩, premN_of hK v 1 0 hM hR (by norm_num)⟩, ?_, hR⟩
  intro hs
  have := congrArg (· ⬝ᵥ v ⟨0, by omega⟩) hs
  simp only [sum_dotProduct, zero_dotProduct, hdot] at this
  simp at this

theorem not_forced_of_le {K D : ℕ} (hK : 2 ≤ K) (hKD : K ≤ D) : ¬ Forced K D := by
  intro hF
  obtain ⟨v, hv, hs, _⟩ := orthogonal_realisation hK hKD
  exact hs (hF v 1 hv).1

/-! ### Explicit closed regular simplex in `ℝ^n`, `n ≥ 1`, with `n + 1` vertices -/

section Simplex

variable (n : ℕ)

noncomputable def rr : ℝ := Real.sqrt ((n : ℝ) + 1)
noncomputable def ss : ℝ := 1 / (rr n * (rr n + 1))
def onev : Fin n → ℝ := fun _ => 1

@[simp] lemma onev_apply (i : Fin n) : onev n i = 1 := rfl

/-- Vertices `e_i − s·1` (`i < n`) and `−(1/r)·1`. -/
noncomputable def simplexVec : Fin (n + 1) → Fin n → ℝ :=
  Fin.lastCases (-(1 / rr n) • onev n) (fun i => Pi.single i 1 - ss n • onev n)

lemma rr_pos : 0 < rr n := Real.sqrt_pos.mpr (by positivity)
lemma rr_sq : (n : ℝ) = rr n ^ 2 - 1 := by
  rw [rr, Real.sq_sqrt (by positivity)]; ring

lemma onev_dot : onev n ⬝ᵥ onev n = n := by simp [onev, dotProduct]
lemma single_onev (i : Fin n) : Pi.single i (1 : ℝ) ⬝ᵥ onev n = 1 := by
  simp [single_dotProduct, onev]
lemma onev_single (i : Fin n) : onev n ⬝ᵥ Pi.single i (1 : ℝ) = 1 := by
  simp [dotProduct_single, onev]

/-- Gram matrix of the explicit simplex: `c² = 1 − 1/r²`, `β = −1/r²`. -/
lemma simplex_dot (a b : Fin (n + 1)) :
    simplexVec n a ⬝ᵥ simplexVec n b =
      if a = b then 1 - 1 / rr n ^ 2 else -(1 / rr n ^ 2) := by
  have hr := rr_pos n
  have hn := rr_sq n
  have hs : ss n = 1 / (rr n * (rr n + 1)) := rfl
  induction a using Fin.lastCases with
  | last =>
    induction b using Fin.lastCases with
    | last =>
      rw [ite_eq_left rfl]
      simp only [simplexVec, Fin.lastCases_last, smul_dotProduct, dotProduct_smul,
        onev_dot, smul_eq_mul, hn]
      field_simp
    | cast j =>
      rw [ite_eq_right (Fin.castSucc_ne_last j).symm]
      simp only [simplexVec, Fin.lastCases_last, Fin.lastCases_castSucc, smul_dotProduct,
        dotProduct_sub, dotProduct_smul, onev_dot, onev_single, smul_eq_mul, hs, hn]
      field_simp; ring
  | cast i =>
    induction b using Fin.lastCases with
    | last =>
      rw [ite_eq_right (Fin.castSucc_ne_last i)]
      simp only [simplexVec, Fin.lastCases_last, Fin.lastCases_castSucc, dotProduct_smul,
        sub_dotProduct, smul_dotProduct, onev_dot, single_onev, smul_eq_mul, hs, hn]
      field_simp; ring
    | cast j =>
      simp only [simplexVec, Fin.lastCases_castSucc, sub_dotProduct, dotProduct_sub,
        smul_dotProduct, dotProduct_smul, onev_dot, single_onev, onev_single, smul_eq_mul,
        Fin.castSucc_inj, hs, hn]
      rw [single_dotProduct, Pi.single_apply]
      by_cases hij : i = j
      · subst hij; rw [ite_eq_left rfl, ite_eq_left rfl]; field_simp; ring
      · rw [ite_eq_right hij, ite_eq_right hij]; field_simp; ring

end Simplex

/-- Zero-padding `ℝ^n ↪ ℝ^(n+m)` preserves dot products. -/
def pad {n m : ℕ} (x : Fin n → ℝ) : Fin (n + m) → ℝ := Fin.append x 0

lemma pad_dot {n m : ℕ} (x y : Fin n → ℝ) : (pad (m := m) x) ⬝ᵥ (pad y) = x ⬝ᵥ y := by
  simp [pad, dotProduct, Fin.sum_univ_add, Fin.append_left, Fin.append_right]

/-- Existence of the closed regular simplex with `K = n+1` legs in any `ℝ^(n+m)`, `n ≥ 1`. -/
theorem simplex_realisation (n m : ℕ) (hn : 1 ≤ n) :
    ∃ c, Realisation (n + 1) (n + m) (fun a => pad (simplexVec n a)) c := by
  have hr := rr_pos n
  have hr2 : 2 ≤ rr n ^ 2 := by
    have := rr_sq n; have : (1 : ℝ) ≤ n := by exact_mod_cast hn
    linarith
  have hc2 : 0 < 1 - 1 / rr n ^ 2 := by
    rw [sub_pos, div_lt_one (by positivity)]; linarith
  refine ⟨Real.sqrt (1 - 1 / rr n ^ 2), ?_⟩
  have hM : ∀ a, pad (m := m) (simplexVec n a) ⬝ᵥ pad (simplexVec n a) =
      Real.sqrt (1 - 1 / rr n ^ 2) ^ 2 := by
    intro a; rw [pad_dot, simplex_dot, ite_eq_left rfl, Real.sq_sqrt hc2.le]
  have hR : ∀ a b, a ≠ b → pad (m := m) (simplexVec n a) ⬝ᵥ pad (simplexVec n b) =
      -(1 / rr n ^ 2) := by
    intro a b hab; rw [pad_dot, simplex_dot, ite_eq_right hab]
  refine ⟨⟨_, hR⟩, ⟨Real.sqrt_pos.mpr hc2, hM⟩, premN_of (by omega) _ _ _ hM hR ?_⟩
  rw [Real.sq_sqrt hc2.le]; intro h; linarith

/-- **Corollary 2 (existence).** For `K ≥ 2` legs, a realisation in `ℝ^D` exists iff `D ≥ K − 1`. -/
theorem cor2_exists_iff (K D : ℕ) (hK : 2 ≤ K) : Exists' K D ↔ K - 1 ≤ D := by
  constructor
  · rintro ⟨v, c, h⟩
    by_contra hlt
    exact no_realisation (by omega) v c h
  · intro hD
    obtain ⟨n, rfl⟩ : ∃ n, K = n + 1 := ⟨K - 1, by omega⟩
    obtain ⟨m, rfl⟩ : ∃ m, D = n + m := ⟨D - n, by omega⟩
    obtain ⟨c, hc⟩ := simplex_realisation n m (by omega)
    exact ⟨_, c, hc⟩

/-- **Corollary 2 (forcing).** For `K ≥ 2`, a realisation exists *and* is forced to the
closed regular simplex iff `D = K − 1`. -/
theorem cor2_forced_iff (K D : ℕ) (hK : 2 ≤ K) : (Exists' K D ∧ Forced K D) ↔ D = K - 1 := by
  constructor
  · rintro ⟨hE, hF⟩
    have := (cor2_exists_iff K D hK).mp hE
    by_contra hne
    exact not_forced_of_le hK (by omega) hF
  · intro hD
    exact ⟨(cor2_exists_iff K D hK).mpr (by omega), forced_of_lt (by omega)⟩

/-- For the tetrad: three is the only dimension where a realisation exists and is forced. -/
theorem three_is_unique (D : ℕ) : (Exists' 4 D ∧ Forced 4 D) ↔ D = 3 := by
  rw [cor2_forced_iff 4 D (by norm_num)]

/-- "If D ≥ K, any α + Kβ > 0 is also realisable": every `α > 0, α + Kβ ≥ 0` is realised in `ℝ^K`
by `v_a = √α e_a + y·1`. (Strengthens the paper's single example `β = 0`.) -/
theorem cor2_all_gram_realisable (K : ℕ) (α β : ℝ) (hα : 0 < α) (hαβ : 0 ≤ α + K * β)
    (hK : 1 ≤ K) :
    ∃ v : Fin K → Fin K → ℝ, ∀ a b, v a ⬝ᵥ v b = if a = b then α + β else β := by
  have hKr : (K : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr (by omega)
  obtain ⟨x, hxdef⟩ : ∃ x, x = Real.sqrt α := ⟨_, rfl⟩
  obtain ⟨z, hzdef⟩ : ∃ z, z = Real.sqrt (α + K * β) := ⟨_, rfl⟩
  obtain ⟨y, hy⟩ : ∃ y, y = (z - x) / K := ⟨_, rfl⟩
  have hx : x ^ 2 = α := by rw [hxdef]; exact Real.sq_sqrt hα.le
  have hz : z ^ 2 = α + K * β := by rw [hzdef]; exact Real.sq_sqrt hαβ
  have key : (K : ℝ) * y ^ 2 + 2 * x * y = β := by
    have e : (K : ℝ) * y ^ 2 + 2 * x * y = (z ^ 2 - x ^ 2) / K := by
      rw [hy]; field_simp; ring
    rw [e, hz, hx]; field_simp; ring
  refine ⟨fun a => x • Pi.single a 1 + y • onev K, fun a b => ?_⟩
  simp only [add_dotProduct, dotProduct_add, smul_dotProduct, dotProduct_smul, single_dotProduct,
    onev_single, onev_dot, onev_apply, Pi.single_apply, smul_eq_mul]
  split_ifs
  · linear_combination hx + key
  · linear_combination key

/-! ## Corollary 3 (parity completion) -/

theorem cor3_parity (v : Fin 4 → Fin 3 → ℝ) (c : ℝ) (h : Realisation 4 3 v c) :
    Realisation 4 3 (fun a => -v a) c ∧ gram (fun a => -v a) = gram v ∧
      ∀ a b, v a ≠ -v b := by
  obtain ⟨⟨β, hR⟩, ⟨hc, hM⟩, ⟨a₀, b₀, hab₀⟩⟩ := h
  have hneg : ∀ a b, (-v a) ⬝ᵥ (-v b) = v a ⬝ᵥ v b := fun a b => by
    rw [neg_dotProduct, dotProduct_neg, neg_neg]
  refine ⟨⟨⟨β, fun a b hab => by rw [hneg, hR a b hab]⟩, ⟨hc, fun a => by rw [hneg, hM]⟩,
    ⟨a₀, b₀, fun h => hab₀ (neg_injective h)⟩⟩, by ext a b; simp [gram, hneg], ?_⟩
  intro a b hab
  have hE := forced_gram_entries v c ⟨⟨β, hR⟩, ⟨hc, hM⟩, ⟨a₀, b₀, hab₀⟩⟩ a b
  have : v a ⬝ᵥ v b = -c ^ 2 := by rw [hab, neg_dotProduct, hM]
  rw [this] at hE
  split_ifs at hE <;> nlinarith

/-- The 8 columns of `M` and `−M` are distinct and are exactly the cube `{−1,+1}³`. -/
theorem cor3_cube :
    Function.Injective (Sum.elim Mcol (fun a => -Mcol a)) ∧
    (∀ a i, Mcol a i = 1 ∨ Mcol a i = -1) ∧
    (∀ s : Fin 3 → ℝ, (∀ i, s i = 1 ∨ s i = -1) → ∃ a, s = Mcol a ∨ s = -Mcol a) := by
  refine ⟨?_, ?_, ?_⟩
  · rintro (a | a) (b | b) h <;>
    · have h0 := congrFun h 0; have h1 := congrFun h 1; have h2 := congrFun h 2
      fin_cases a <;> fin_cases b <;> simp [Mcol, Mmat] at h0 h1 h2 ⊢ <;>
        linarith
  · intro a i; fin_cases a <;> fin_cases i <;> simp [Mcol, Mmat]
  · intro s hs
    have hs' : s = ![s 0, s 1, s 2] := by ext i; fin_cases i <;> rfl
    rcases hs 0 with h0 | h0 <;> rcases hs 1 with h1 | h1 <;> rcases hs 2 with h2 | h2 <;>
      rw [hs', h0, h1, h2]
    · exact ⟨0, Or.inl (by ext i; fin_cases i <;> simp [Mcol, Mmat])⟩
    · exact ⟨3, Or.inr (by ext i; fin_cases i <;> simp [Mcol, Mmat])⟩
    · exact ⟨2, Or.inr (by ext i; fin_cases i <;> simp [Mcol, Mmat])⟩
    · exact ⟨1, Or.inl (by ext i; fin_cases i <;> simp [Mcol, Mmat])⟩
    · exact ⟨1, Or.inr (by ext i; fin_cases i <;> simp [Mcol, Mmat])⟩
    · exact ⟨2, Or.inl (by ext i; fin_cases i <;> simp [Mcol, Mmat])⟩
    · exact ⟨3, Or.inl (by ext i; fin_cases i <;> simp [Mcol, Mmat])⟩
    · exact ⟨0, Or.inr (by ext i; fin_cases i <;> simp [Mcol, Mmat])⟩

/-! ## Necessity of the premises (the table) -/

def e3 (i : Fin 3) : Fin 3 → ℝ := Pi.single i 1

lemma e3_dot (i j : Fin 3) : e3 i ⬝ᵥ e3 j = if i = j then 1 else 0 := by
  fin_cases i <;> fin_cases j <;> simp [e3, dotProduct, Fin.sum_univ_succ]

/-- (R) removed: `(v, w, −v, −w)`, `|v| = |w| = c`, `v ⊥ w` — satisfies (M),(N),(D), not (R);
closed; consecutive sides `2c²`, diagonals `4c²` (a square). -/
theorem nec_R (c : ℝ) (hc : 0 < c) :
    let v : Fin 4 → Fin 3 → ℝ := ![c • e3 0, c • e3 1, -(c • e3 0), -(c • e3 1)]
    PremM v c ∧ PremN v ∧ ¬ PremR v ∧ ∑ a, v a = 0 ∧
      (∀ a : Fin 4, (v a - v (a + 1)) ⬝ᵥ (v a - v (a + 1)) = 2 * c ^ 2) ∧
      (v 0 - v 2) ⬝ᵥ (v 0 - v 2) = 4 * c ^ 2 ∧ (v 1 - v 3) ⬝ᵥ (v 1 - v 3) = 4 * c ^ 2 := by
  intro v
  have hd : ∀ i j, (c • e3 i) ⬝ᵥ (c • e3 j) = c ^ 2 * (if i = j then 1 else 0) := by
    intro i j; rw [smul_dotProduct, dotProduct_smul, e3_dot]; simp [smul_eq_mul]; ring
  refine ⟨⟨hc, fun a => ?_⟩, ⟨0, 1, fun h => ?_⟩, ?_, ?_, fun a => ?_, ?_, ?_⟩
  · fin_cases a <;> simp [v, hd, smul_dotProduct, dotProduct_smul, e3_dot, neg_dotProduct, dotProduct_neg] <;> ring
  · have := congrFun h 0; simp [v, e3] at this; exact hc.ne' this
  · rintro ⟨β, hR⟩
    have h1 := hR 0 1 (by decide); have h2 := hR 0 2 (by decide)
    simp [v, hd, dotProduct_neg] at h1 h2
    nlinarith
  · simp [v, Fin.sum_univ_succ]
  · fin_cases a <;>
      simp [v, sub_dotProduct, dotProduct_sub, smul_dotProduct, dotProduct_smul, e3_dot, neg_dotProduct, dotProduct_neg] <;> ring
  · simp [v, smul_dotProduct, dotProduct_smul, e3_dot]; ring
  · simp [v, smul_dotProduct, dotProduct_smul, e3_dot]; ring

/-- (M) removed, first row: `v₀ = 0`, `vᵢ = c êᵢ` (observer's projection). -/
theorem nec_M1 (c : ℝ) (hc : 0 < c) :
    let v : Fin 4 → Fin 3 → ℝ := ![0, c • e3 0, c • e3 1, c • e3 2]
    PremR v ∧ PremN v ∧ (∀ c', ¬ PremM v c') ∧ (∀ a b, a ≠ b → v a ⬝ᵥ v b = 0) := by
  intro v
  have hd : ∀ i j, (c • e3 i) ⬝ᵥ (c • e3 j) = c ^ 2 * (if i = j then 1 else 0) := by
    intro i j; rw [smul_dotProduct, dotProduct_smul, e3_dot]; simp [smul_eq_mul]; ring
  have hR : ∀ a b, a ≠ b → v a ⬝ᵥ v b = 0 := by
    intro a b hab; fin_cases a <;> fin_cases b <;> simp_all [v, smul_dotProduct, dotProduct_smul, e3_dot]
  refine ⟨⟨0, hR⟩, ⟨0, 1, fun h => ?_⟩, fun c' ⟨hc', hM⟩ => ?_, hR⟩
  · have := congrFun h 0; simp [v, e3] at this; exact hc.ne' this.symm
  · have := hM 0; simp [v] at this; exact hc'.ne' (by nlinarith)

/-- (M) removed, second row: every leg non-zero, `G_aa = (1,3,7,7)c²`, `G_ab = −c²`,
realised in `ℝ³` (so rank ≤ 3). Explicit vectors (c = 1):
`(−1,0,0), (1,1,1), (1,−1+√2,−1−√2), (1,−1−√2,−1+√2)`. -/
noncomputable def vM2 (c : ℝ) : Fin 4 → Fin 3 → ℝ :=
  fun a => c • (![![-1, 0, 0], ![1, 1, 1], ![1, -1 + Real.sqrt 2, -1 - Real.sqrt 2],
    ![1, -1 - Real.sqrt 2, -1 + Real.sqrt 2]] a)

theorem nec_M2 (c : ℝ) (hc : 0 < c) :
    PremR (vM2 c) ∧ PremN (vM2 c) ∧ (∀ c', ¬ PremM (vM2 c) c') ∧
    (∀ a b, a ≠ b → vM2 c a ⬝ᵥ vM2 c b = -c ^ 2) ∧
    vM2 c 0 ⬝ᵥ vM2 c 0 = 1 * c ^ 2 ∧ vM2 c 1 ⬝ᵥ vM2 c 1 = 3 * c ^ 2 ∧
    vM2 c 2 ⬝ᵥ vM2 c 2 = 7 * c ^ 2 ∧ vM2 c 3 ⬝ᵥ vM2 c 3 = 7 * c ^ 2 := by
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hdot : ∀ a b, vM2 c a ⬝ᵥ vM2 c b =
      c ^ 2 * (if a = b then ![1, 3, 7, 7] a else -1) := by
    intro a b
    fin_cases a <;> fin_cases b <;>
      simp [vM2, dotProduct, Fin.sum_univ_succ] <;> ring_nf <;> rw [h2] <;> ring
  have hR : ∀ a b, a ≠ b → vM2 c a ⬝ᵥ vM2 c b = -c ^ 2 := by
    intro a b hab; rw [hdot, ite_eq_right hab]; ring
  refine ⟨⟨_, hR⟩, ⟨0, 1, fun h => ?_⟩, fun c' ⟨_, hM⟩ => ?_, hR, ?_, ?_, ?_, ?_⟩
  · have := congrFun h 0; simp [vM2] at this; linarith
  · have h0 := hM 0; have h1 := hM 1
    rw [hdot, ite_eq_left rfl] at h0 h1; simp at h0 h1
    nlinarith
  all_goals (rw [hdot, ite_eq_left rfl]; simp [mul_comm])

/-- (N) removed: `v_a = v` for all `a`, `G = c² J`. -/
theorem nec_N (c : ℝ) (hc : 0 < c) :
    let v : Fin 4 → Fin 3 → ℝ := fun _ => c • e3 0
    PremR v ∧ PremM v c ∧ ¬ PremN v ∧ gram v = c ^ 2 • J 4 := by
  intro v
  have hd : v 0 ⬝ᵥ v 0 = c ^ 2 := by
    simp only [v, smul_dotProduct, dotProduct_smul, e3_dot, smul_eq_mul]; simp; ring
  refine ⟨⟨c ^ 2, fun a b _ => hd⟩, ⟨hc, fun a => hd⟩, fun ⟨a, b, h⟩ => h rfl, ?_⟩
  ext a b; simp only [gram, J, of_apply, Matrix.smul_apply, smul_eq_mul, mul_one]; exact hd

/-- (D) removed: in `ℝ⁴`, `v_a = c ê_a`, `G = c² I`, not closed; in `ℝ²` no realisation. -/
theorem nec_D :
    (∃ v : Fin 4 → Fin 4 → ℝ, Realisation 4 4 v 1 ∧ ∑ a, v a ≠ 0 ∧
      ∀ a b, a ≠ b → v a ⬝ᵥ v b = 0) ∧
    (∀ (v : Fin 4 → Fin 2 → ℝ) c, ¬ Realisation 4 2 v c) :=
  ⟨orthogonal_realisation (by norm_num) le_rfl, fun v c => no_realisation (by norm_num) v c⟩

/-! ## The tetrad's data, and the symmetry view

Data of a Lorentz tetrad: legs `e_a ∈ ℝ^{1,3}` with `η(e_a, e_b) = η_ab = diag(−1,1,1,1)`.
This section defines `η` and the Minkowski form, proves the tetrad facts used for (N) and (D), and
gives the symmetry view of the premises: a realisation is required to be
* (Faithful)  legs not all equal (the paper's (N));
* (Symmetric) every permutation of legs that is a symmetry of the chosen metric data is a
  symmetry of the realisation's Gram matrix;
* (Dimension) `D` = positive index of `η`.
With `η` itself the symmetry group is `S₃` and the tetrahedron is not forced; with `|η| = I` it is
`S₄` and the tetrahedron is forced; `S₃` is maximal in `S₄`, so there is nothing in between.
-/

def eta : Matrix (Fin 4) (Fin 4) ℝ := Matrix.diagonal ![-1, 1, 1, 1]

/-- Minkowski form on `ℝ^{1,3}`. -/
def mink (x y : Fin 4 → ℝ) : ℝ := -(x 0 * y 0) + x 1 * y 1 + x 2 * y 2 + x 3 * y 3

/-- `σ` is a symmetry of the leg-indexed matrix `M`. -/
def IsSymOf (M : Matrix (Fin 4) (Fin 4) ℝ) (σ : Equiv.Perm (Fin 4)) : Prop :=
  ∀ a b, M (σ a) (σ b) = M a b

lemma eta_diag (a : Fin 4) : eta a a = if a = 0 then -1 else 1 := by
  fin_cases a <;> simp [eta]

lemma eta_off {a b : Fin 4} (h : a ≠ b) : eta a b = 0 := by
  simp [eta, Matrix.diagonal_apply_ne _ h]

/-- The symmetries of `η` itself are exactly the permutations fixing the time leg (`S₃`). -/
theorem aut_eta (σ : Equiv.Perm (Fin 4)) : IsSymOf eta σ ↔ σ 0 = 0 := by
  constructor
  · intro h
    have := h 0 0
    rw [eta_diag, eta_diag, ite_eq_left rfl] at this
    by_contra hne
    rw [ite_eq_right hne] at this; norm_num at this
  · intro h0 a b
    by_cases hab : a = b
    · subst hab
      have hiff : σ a = 0 ↔ a = 0 :=
        ⟨fun h => σ.injective (h.trans h0.symm), fun h => by rw [h, h0]⟩
      rw [eta_diag, eta_diag]; simp only [hiff]
    · rw [eta_off hab, eta_off (σ.injective.ne hab)]

/-- The sign-stripped metric `|η|` (entrywise absolute value) is the identity … -/
def absEta : Matrix (Fin 4) (Fin 4) ℝ := Matrix.of fun a b => |eta a b|

lemma absEta_eq_one : absEta = 1 := by
  ext a b
  by_cases h : a = b
  · subst h; simp only [absEta, of_apply, eta_diag, Matrix.one_apply_eq]; split_ifs <;> norm_num
  · simp [absEta, eta_off h, Matrix.one_apply_ne h]

/-- … so every permutation of legs is a symmetry of `|η|` (`S₄`). -/
theorem aut_absEta (σ : Equiv.Perm (Fin 4)) : IsSymOf absEta σ := by
  intro a b; rw [absEta_eq_one]; simp [Matrix.one_apply, σ.injective.eq_iff]

/-- (N) from the tetrad: legs with `η(e_a,e_b) = η_ab` are pairwise distinct. -/
theorem tetrad_legs_distinct (e : Fin 4 → Fin 4 → ℝ) (he : ∀ a b, mink (e a) (e b) = eta a b) :
    Function.Injective e := by
  intro a b hab
  by_contra hne
  have h1 := he a b
  rw [hab, he b b, eta_off hne, eta_diag] at h1
  split_ifs at h1 <;> norm_num at h1

/-- (D) from the tetrad: the positive index of `η` is 3. -/
theorem positive_index : (Finset.univ.filter fun a : Fin 4 => 0 < eta a a).card = 3 := by
  rw [show (Finset.univ.filter fun a : Fin 4 => 0 < eta a a) = ({1, 2, 3} : Finset (Fin 4)) by
    ext a; fin_cases a <;> simp [eta_diag]]
  rfl

lemma gram_symm {K D : ℕ} (v : Fin K → Fin D → ℝ) (a b : Fin K) : gram v a b = gram v b a := by
  simp [gram, dotProduct_comm]

/-- Structure forced by `S₃` (symmetries of `η`): `G₀₀ = p`, `G₀ᵢ = q`, `Gᵢᵢ = r`, `Gᵢⱼ = s`. -/
lemma S3_structure (G : Matrix (Fin 4) (Fin 4) ℝ) (hsym : ∀ a b, G a b = G b a)
    (h : ∀ σ : Equiv.Perm (Fin 4), σ 0 = 0 → IsSymOf G σ) :
    (∀ i, i ≠ 0 → G i i = G 1 1) ∧ (∀ i, i ≠ 0 → G 0 i = G 0 1) ∧
    (∀ i j, i ≠ 0 → j ≠ 0 → i ≠ j → G i j = G 1 2) := by
  have hsw : ∀ i : Fin 4, i ≠ 0 → (Equiv.swap 1 i) 0 = 0 := fun i hi =>
    Equiv.swap_apply_of_ne_of_ne (by decide) (Ne.symm hi)
  refine ⟨fun i hi => ?_, fun i hi => ?_, ?_⟩
  · have := h _ (hsw i hi) 1 1
    rwa [Equiv.swap_apply_left] at this
  · have := h _ (hsw i hi) 0 1
    rwa [hsw i hi, Equiv.swap_apply_left] at this
  · have h13 : G 1 3 = G 1 2 := by
      have := h (Equiv.swap 2 3) (by decide) 1 2
      rwa [Equiv.swap_apply_of_ne_of_ne (by decide) (by decide), Equiv.swap_apply_left] at this
    have h32 : G 3 2 = G 1 2 := by
      have := h (Equiv.swap 1 3) (by decide) 1 2
      rwa [Equiv.swap_apply_left, Equiv.swap_apply_of_ne_of_ne (by decide) (by decide)] at this
    intro i j hi hj hij
    fin_cases i <;> fin_cases j <;> simp at hi hj hij ⊢ <;>
      linarith [hsym 2 1, hsym 3 1, hsym 2 3, h13, h32]

/-- **Maximality.** Any symmetry requirement containing `Aut(η) = S₃` plus *one* permutation that
moves the time leg forces full `S₄` structure: equal diagonal and equal off-diagonal (= (M),(R)). -/
theorem extension_forces_S4 (G : Matrix (Fin 4) (Fin 4) ℝ) (hsym : ∀ a b, G a b = G b a)
    (hS3 : ∀ σ : Equiv.Perm (Fin 4), σ 0 = 0 → IsSymOf G σ)
    (σ₁ : Equiv.Perm (Fin 4)) (h1 : σ₁ 0 ≠ 0) (hσ₁ : IsSymOf G σ₁) :
    (∀ a, G a a = G 0 0) ∧ (∀ a b, a ≠ b → G a b = G 0 1) := by
  obtain ⟨hd, h0, hs⟩ := S3_structure G hsym hS3
  have hp : G 1 1 = G 0 0 := by have := hσ₁ 0 0; rwa [hd _ h1] at this
  -- pick a space leg j with σ₁ j ≠ 0
  obtain ⟨j, hj0, hjσ⟩ : ∃ j : Fin 4, j ≠ 0 ∧ σ₁ j ≠ 0 := by
    by_cases hm : σ₁ 1 = 0
    · refine ⟨2, by decide, fun h2 => ?_⟩
      exact absurd (σ₁.injective (h2.trans hm.symm)) (by decide)
    · exact ⟨1, by decide, hm⟩
  have hqs : G 0 1 = G 1 2 := by
    have := hσ₁ 0 j
    rw [hs _ _ h1 hjσ (σ₁.injective.ne (Ne.symm hj0)), h0 j hj0] at this
    exact this.symm
  refine ⟨fun a => ?_, fun a b hab => ?_⟩
  · by_cases ha : a = 0
    · rw [ha]
    · rw [hd a ha, hp]
  · by_cases ha : a = 0
    · subst ha; exact h0 b (Ne.symm hab)
    · by_cases hb : b = 0
      · subst hb; rw [hsym, h0 a ha]
      · rw [hs a b ha hb hab, hqs]

/-- Equal diagonal + equal off-diagonal + (N) ⇒ premises (R),(M),(N) hold, any `K`, `D`. -/
lemma realisation_of_const {K D : ℕ} (v : Fin K → Fin D → ℝ) (hN : PremN v) (a₀ : Fin K)
    (d o : ℝ) (hd : ∀ a, gram v a a = d) (ho : ∀ a b, a ≠ b → gram v a b = o) :
    ∃ c, Realisation K D v c := by
  have hpos : 0 < d := by
    rcases (dot_self_nonneg (v a₀)).lt_or_eq with h | h
    · have := hd a₀; simp only [gram, of_apply] at this; linarith
    · exfalso
      obtain ⟨a, b, hab⟩ := hN
      have hz : ∀ x, v x = 0 := fun x => by
        have h1 := hd x; have h2 := hd a₀; simp only [gram, of_apply] at h1 h2
        exact dotProduct_self_eq_zero.mp (by linarith)
      exact hab ((hz a).trans (hz b).symm)
  refine ⟨Real.sqrt d, ⟨o, fun a b hab => ?_⟩, ⟨Real.sqrt_pos.mpr hpos, fun a => ?_⟩, hN⟩
  · have := ho a b hab; simpa [gram] using this
  · rw [Real.sq_sqrt hpos.le]; have := hd a; simpa [gram] using this

lemma realisation_of_S4 (v : Fin 4 → Fin 3 → ℝ) (hN : PremN v)
    (hd : ∀ a, gram v a a = gram v 0 0) (ho : ∀ a b, a ≠ b → gram v a b = gram v 0 1) :
    ∃ c, Realisation 4 3 v c :=
  realisation_of_const v hN 0 _ _ hd ho

/-- **Transcription theorem.** Rules: (Faithful) legs not all equal; (Symmetric) every symmetry of
`|η|` is a symmetry of `G`; (Dimension) `ℝ^3`, the positive index of `η`. Then the legs close and
`G = c²I − (c²/3)(J − I)`: the regular tetrahedron. -/
theorem transcription_forces_tetrahedron (v : Fin 4 → Fin 3 → ℝ) (hN : PremN v)
    (hsym : ∀ σ, IsSymOf absEta σ → IsSymOf (gram v) σ) :
    ∃ c : ℝ, 0 < c ∧ ∑ a, v a = 0 ∧
      gram v = c ^ 2 • (1 : Matrix (Fin 4) (Fin 4) ℝ) - (c ^ 2 / 3) • (J 4 - 1) := by
  have hall : ∀ σ, IsSymOf (gram v) σ := fun σ => hsym σ (aut_absEta σ)
  obtain ⟨hd, ho⟩ := extension_forces_S4 (gram v) (gram_symm v) (fun σ _ => hall σ)
    (Equiv.swap 0 1) (by decide) (hall _)
  obtain ⟨c, hc⟩ := realisation_of_S4 v hN hd ho
  exact ⟨c, hc.2.1.1, forced_gram v c hc⟩

/-- **Dichotomy, part 1.** Using `η`'s own symmetries (`S₃`) the tetrahedron is *not* forced:
the observer's projection `(0, ê₁, ê₂, ê₃)` is faithful, `Aut(η)`-symmetric, and not closed. -/
theorem lorentz_symmetry_alone_not_forced :
    ∃ v : Fin 4 → Fin 3 → ℝ, Function.Injective v ∧
      (∀ σ, IsSymOf eta σ → IsSymOf (gram v) σ) ∧ ∑ a, v a ≠ 0 := by
  let v : Fin 4 → Fin 3 → ℝ := ![0, e3 0, e3 1, e3 2]
  have hg : ∀ a b, gram v a b = if a = b then (if a = 0 then 0 else 1) else 0 := by
    intro a b; fin_cases a <;> fin_cases b <;> simp [gram, v, e3_dot]
  refine ⟨v, ?_, fun σ hσ a b => ?_, fun h => ?_⟩
  · intro a b h
    have h0 := congrFun h 0; have h1 := congrFun h 1; have h2 := congrFun h 2
    fin_cases a <;> fin_cases b <;> simp [v, e3] at h0 h1 h2 ⊢
  · have h0 := (aut_eta σ).mp hσ
    have hiff : σ a = 0 ↔ a = 0 :=
        ⟨fun h => σ.injective (h.trans h0.symm), fun h => by rw [h, h0]⟩
    rw [hg, hg]; simp only [σ.injective.eq_iff, hiff]
  · have := congrFun h 0; simp [v, Fin.sum_univ_succ, e3] at this

/-- **Dichotomy, part 2.** As soon as the symmetry requirement contains `Aut(η)` and *any*
permutation moving the time leg, the tetrahedron is forced. -/
theorem any_extension_beyond_lorentz_forces (v : Fin 4 → Fin 3 → ℝ) (hN : PremN v)
    (hS3 : ∀ σ, IsSymOf eta σ → IsSymOf (gram v) σ)
    (σ₁ : Equiv.Perm (Fin 4)) (h1 : ¬ IsSymOf eta σ₁) (hσ₁ : IsSymOf (gram v) σ₁) :
    ∃ c : ℝ, 0 < c ∧ ∑ a, v a = 0 ∧
      gram v = c ^ 2 • (1 : Matrix (Fin 4) (Fin 4) ℝ) - (c ^ 2 / 3) • (J 4 - 1) := by
  obtain ⟨hd, ho⟩ := extension_forces_S4 (gram v) (gram_symm v)
    (fun σ h => hS3 σ ((aut_eta σ).mpr h)) σ₁ (fun h => h1 ((aut_eta σ₁).mpr h)) hσ₁
  obtain ⟨c, hc⟩ := realisation_of_S4 v hN hd ho
  exact ⟨c, hc.2.1.1, forced_gram v c hc⟩

#print axioms ForcedTetrahedralFrame.transcription_forces_tetrahedron
#print axioms ForcedTetrahedralFrame.lorentz_symmetry_alone_not_forced
#print axioms ForcedTetrahedralFrame.any_extension_beyond_lorentz_forces
#print axioms ForcedTetrahedralFrame.tetrad_legs_distinct
#print axioms ForcedTetrahedralFrame.positive_index

/-! ## Independent route: the transcription rules, for any signature `(1, n)`

The tetrad's metric in convention `s` is `etaG n s = diag(−s, s, …, s)` on `n + 1` legs
(`s = 1`: (−,+,…,+); `s = −1`: (+,−,…,−)). A realisation `v : legs → ℝ^D` is constrained by:

* **Local** — each Gram entry is a function of the matching metric entry only:
  `G_aa = f(η_aa)`, `G_ab = g(η_ab)` (`a ≠ b`).
* **Covariant** (the paper's "label-blind") — the same `f`, `g` for every leg: the rule ignores
  leg labels, so it does not matter where the time leg sits (`transcribes_relabel`,
  `time_leg_anywhere`).
* **Convention-independent** — one realisation transcribes both `s = 1` and `s = −1`.
* **Faithful** — the legs are not all equal (the paper's (N); the tetrad's legs are distinct,
  `tetrad_legs_distinct`).
* **Dimension** — `D = n`, the positive index of the metric (`etaG_positive_index`).

`Transcribes f g M v` packages *Local + Covariant*.
-/

def etaG (n : ℕ) (s : ℝ) : Matrix (Fin (n + 1)) (Fin (n + 1)) ℝ :=
  Matrix.of fun a b => if a = b then (if a = 0 then -s else s) else 0

/-- Local + covariant transcription of the metric `M` by `f` (diagonal) and `g` (off-diagonal). -/
def Transcribes {K D : ℕ} (f g : ℝ → ℝ) (M : Matrix (Fin K) (Fin K) ℝ)
    (v : Fin K → Fin D → ℝ) : Prop :=
  ∀ a b, gram v a b = if a = b then f (M a a) else g (M a b)

lemma etaG_diag (n : ℕ) (s : ℝ) (a : Fin (n + 1)) : etaG n s a a = if a = 0 then -s else s := by
  simp [etaG]

lemma etaG_off (n : ℕ) (s : ℝ) {a b : Fin (n + 1)} (h : a ≠ b) : etaG n s a b = 0 := by
  simp [etaG, h]

/-- (D) The positive index of `etaG n 1` is `n`. -/
theorem etaG_positive_index (n : ℕ) :
    (Finset.univ.filter fun a : Fin (n + 1) => 0 < etaG n 1 a a).card = n := by
  have : (Finset.univ.filter fun a : Fin (n + 1) => 0 < etaG n 1 a a) = Finset.univ.erase 0 := by
    ext a; by_cases ha : a = 0 <;> simp [etaG_diag, ha]
  rw [this, Finset.card_erase_of_mem (Finset.mem_univ _), Finset.card_univ, Fintype.card_fin]
  simp

/-- Covariance made explicit: relabelling the legs of the metric relabels the realisation. -/
lemma transcribes_relabel {K D : ℕ} (f g : ℝ → ℝ) (M : Matrix (Fin K) (Fin K) ℝ)
    (v : Fin K → Fin D → ℝ) (σ : Equiv.Perm (Fin K))
    (h : Transcribes f g (M.submatrix σ σ) v) : Transcribes f g M (v ∘ σ.symm) := by
  intro a b
  have := h (σ.symm a) (σ.symm b)
  simp only [submatrix_apply, Equiv.apply_symm_apply, σ.symm.injective.eq_iff] at this
  simpa [gram, Function.comp] using this

/-- **Main theorem (any signature `(1,n)`).** Local + covariant + convention-independent +
faithful transcription into `ℝⁿ` (the positive index) forces the closed regular `n`-simplex:
(R), (M), (N) hold, `Σ v_a = 0`, and `G_ab = −c²/n` for `a ≠ b`. -/
theorem rules_force_simplex (n : ℕ) (f g : ℝ → ℝ) (v : Fin (n + 1) → Fin n → ℝ) (hN : PremN v)
    (hplus : Transcribes f g (etaG n 1) v) (hminus : Transcribes f g (etaG n (-1)) v) :
    ∃ c : ℝ, Realisation (n + 1) n v c ∧ ∑ a, v a = 0 ∧
      ∀ a b, a ≠ b → v a ⬝ᵥ v b = -c ^ 2 / n := by
  have hd : ∀ a, gram v a a = f 1 := by
    intro a
    by_cases ha : a = 0
    · rw [hminus a a, ite_eq_left rfl, etaG_diag, ite_eq_left ha]; norm_num
    · rw [hplus a a, ite_eq_left rfl, etaG_diag, ite_eq_right ha]
  have ho : ∀ a b, a ≠ b → gram v a b = g 0 := by
    intro a b hab; rw [hplus a b, ite_eq_right hab, etaG_off _ _ hab]
  obtain ⟨c, hc⟩ := realisation_of_const v hN 0 _ _ hd ho
  obtain ⟨hs, hoff⟩ := general_forced (by omega) v c hc
  refine ⟨c, hc, hs, fun a b hab => ?_⟩
  rw [hoff a b hab, show ((n + 1 : ℕ) : ℝ) - 1 = n by push_cast; ring]

/-- **Headline (the tetrad, `n = 3`).** The rules force the closed regular tetrahedron, Eq. (1),
unique up to a unique `Q ∈ O(3)`. -/
theorem tetrahedron_from_rules (f g : ℝ → ℝ) (v : Fin 4 → Fin 3 → ℝ) (hN : PremN v)
    (hplus : Transcribes f g (etaG 3 1) v) (hminus : Transcribes f g (etaG 3 (-1)) v) :
    ∃ c : ℝ, 0 < c ∧ ∑ a, v a = 0 ∧
      gram v = c ^ 2 • (1 : Matrix (Fin 4) (Fin 4) ℝ) - (c ^ 2 / 3) • (J 4 - 1) ∧
      ∃! Q : Matrix (Fin 3) (Fin 3) ℝ,
        Q ∈ Matrix.orthogonalGroup (Fin 3) ℝ ∧ Vmat v = Q * ((c / Real.sqrt 3) • Mmat) := by
  obtain ⟨c, hc, -, -⟩ := rules_force_simplex 3 f g v hN hplus hminus
  exact ⟨c, hc.2.1.1, (forced_gram v c hc).1, (forced_gram v c hc).2, cor1_unique v c hc⟩

/-- **Time leg anywhere.** Put the time leg at any position (relabel by any `σ`): the same rules
still force the same geometry. -/
theorem time_leg_anywhere (f g : ℝ → ℝ) (σ : Equiv.Perm (Fin 4)) (v : Fin 4 → Fin 3 → ℝ)
    (hN : PremN v)
    (hplus : Transcribes f g ((etaG 3 1).submatrix σ σ) v)
    (hminus : Transcribes f g ((etaG 3 (-1)).submatrix σ σ) v) :
    ∃ c : ℝ, 0 < c ∧ ∑ a, v a = 0 ∧
      gram v = c ^ 2 • (1 : Matrix (Fin 4) (Fin 4) ℝ) - (c ^ 2 / 3) • (J 4 - 1) := by
  set w := v ∘ σ.symm with hw
  have hNw : PremN w := by
    obtain ⟨a, b, hab⟩ := hN
    exact ⟨σ a, σ b, by simpa [hw] using hab⟩
  obtain ⟨c, hc, hsum, hG, -⟩ := tetrahedron_from_rules f g w hNw
    (transcribes_relabel f g _ v σ hplus) (transcribes_relabel f g _ v σ hminus)
  refine ⟨c, hc, ?_, ?_⟩
  · rw [← hsum, hw]; exact (Equiv.sum_comp σ.symm v).symm
  · ext a b
    have h1 : gram v a b = gram w (σ a) (σ b) := by simp [gram, hw]
    rw [h1, hG]
    simp only [Matrix.sub_apply, Matrix.smul_apply, Matrix.one_apply, J, of_apply,
      σ.injective.eq_iff]

/-- **Non-vacuity (tetrad).** The rules are satisfiable: the columns of `M` transcribe both
conventions with `f ≡ 3`, `g ≡ −1`. -/
theorem rules_satisfiable :
    Transcribes (fun _ => 3) (fun _ => -1) (etaG 3 1) Mcol ∧
      Transcribes (fun _ => 3) (fun _ => -1) (etaG 3 (-1)) Mcol ∧ PremN Mcol := by
  have hg : ∀ a b, gram Mcol a b = if a = b then 3 else -1 := fun a b => by
    rw [← MtM_apply]; simp only [gram, of_apply]; rw [Matrix.mul_apply]; simp [Mcol, dotProduct]
  exact ⟨fun a b => by rw [hg], fun a b => by rw [hg], cor1_M_realises.1.2.2⟩

/-- **Non-vacuity (any `n ≥ 1`).** The explicit regular simplex satisfies the rules in `ℝⁿ`. -/
theorem rules_satisfiable_general (n : ℕ) (hn : 1 ≤ n) :
    ∃ (f g : ℝ → ℝ) (v : Fin (n + 1) → Fin n → ℝ),
      Transcribes f g (etaG n 1) v ∧ Transcribes f g (etaG n (-1)) v ∧ PremN v := by
  obtain ⟨c, hc⟩ := simplex_realisation n 0 hn
  refine ⟨fun _ => 1 - 1 / rr n ^ 2, fun _ => -(1 / rr n ^ 2), simplexVec n, ?_, ?_, ?_⟩
  · intro a b; simp only [gram, of_apply]; rw [simplex_dot]
  · intro a b; simp only [gram, of_apply]; rw [simplex_dot]
  · obtain ⟨a, b, hab⟩ := hc.2.2
    exact ⟨a, b, fun h => hab (by simp [h])⟩

#print axioms ForcedTetrahedralFrame.rules_satisfiable
#print axioms ForcedTetrahedralFrame.rules_satisfiable_general

/-! ### Every rule is necessary

Each theorem below drops exactly one rule, keeps all the others, and exhibits a realisation
that is not the regular tetrahedron (it is not closed). -/

/-- The observer's projection `(0, ê₁, ê₂, ê₃)`. -/
def observer : Fin 4 → Fin 3 → ℝ := ![0, e3 0, e3 1, e3 2]

lemma observer_gram (a b : Fin 4) :
    gram observer a b = if a = b then (if a = 0 then 0 else 1) else 0 := by
  fin_cases a <;> fin_cases b <;> simp [gram, observer, e3_dot]

lemma observer_premN : PremN observer := by
  refine ⟨0, 1, fun h => ?_⟩
  have := congrFun h 0; simp [observer, e3] at this

lemma observer_not_closed : ∑ a, observer a ≠ 0 := by
  intro h; have := congrFun h 0; simp [observer, Fin.sum_univ_succ, e3] at this

/-- **Drop convention independence.** A local, covariant rule in one convention admits the
observer's projection (`f x = [x > 0]`, `g = 0`). -/
theorem need_convention_independence :
    ∃ f g : ℝ → ℝ, Transcribes f g (etaG 3 1) observer ∧ PremN observer ∧
      ∑ a, observer a ≠ 0 := by
  refine ⟨fun x => if 0 < x then 1 else 0, fun _ => 0, fun a b => ?_, observer_premN,
    observer_not_closed⟩
  rw [observer_gram]
  by_cases hab : a = b
  · subst hab; rw [ite_eq_left rfl, ite_eq_left rfl, etaG_diag]
    by_cases ha : a = 0 <;> simp [ha]
  · rw [ite_eq_right hab, ite_eq_right hab]

/-- **Drop covariance.** A local, convention-independent rule whose `f` depends on the leg label
(`f₀ ≡ 0`, `fᵢ ≡ 1`) admits the observer's projection in both conventions. -/
theorem need_covariance :
    ∃ (f : Fin 4 → ℝ → ℝ) (g : ℝ → ℝ),
      (∀ s : ℝ, ∀ a b, gram observer a b =
        if a = b then f a (etaG 3 s a a) else g (etaG 3 s a b)) ∧
      PremN observer ∧ ∑ a, observer a ≠ 0 := by
  refine ⟨fun a _ => if a = 0 then 0 else 1, fun _ => 0, fun s a b => ?_, observer_premN,
    observer_not_closed⟩
  rw [observer_gram]

/-- A *non-local* rule: leg `a` is kept iff its diagonal sign agrees with the trace's sign. -/
noncomputable def traceRule (M : Matrix (Fin 4) (Fin 4) ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  Matrix.of fun a b => if a = b then (if 0 < M a a * M.trace then 1 else 0) else 0

lemma traceRule_covariant (M : Matrix (Fin 4) (Fin 4) ℝ) (σ : Equiv.Perm (Fin 4)) :
    traceRule (M.submatrix σ σ) = (traceRule M).submatrix σ σ := by
  have ht : (M.submatrix σ σ).trace = M.trace := by
    simp only [Matrix.trace, Matrix.diag, submatrix_apply]
    exact Equiv.sum_comp σ (fun i => M i i)
  ext a b
  simp only [traceRule, of_apply, submatrix_apply, ht, σ.injective.eq_iff]

lemma etaG3_trace (s : ℝ) : (etaG 3 s).trace = 2 * s := by
  simp [Matrix.trace, Fin.sum_univ_succ, etaG]; ring

/-- **Drop locality.** A covariant, convention-independent, non-local rule (`traceRule`) admits
the observer's projection. -/
theorem need_locality :
    (∀ (M : Matrix (Fin 4) (Fin 4) ℝ) (σ : Equiv.Perm (Fin 4)),
      traceRule (M.submatrix σ σ) = (traceRule M).submatrix σ σ) ∧
    traceRule (etaG 3 1) = traceRule (etaG 3 (-1)) ∧
    gram observer = traceRule (etaG 3 1) ∧ PremN observer ∧ ∑ a, observer a ≠ 0 := by
  refine ⟨traceRule_covariant, ?_, ?_, observer_premN, observer_not_closed⟩
  · ext a b
    simp only [traceRule, of_apply, etaG3_trace, etaG_diag]
    split_ifs <;> norm_num at *
  · ext a b
    rw [observer_gram]
    simp only [traceRule, of_apply, etaG3_trace, etaG_diag]
    split_ifs <;> norm_num at *

/-- **Drop faithfulness.** Equal legs transcribe both conventions locally and covariantly
(`f ≡ g ≡ 1`), giving `G = J`. -/
theorem need_faithfulness :
    let v : Fin 4 → Fin 3 → ℝ := fun _ => e3 0
    Transcribes (fun _ => 1) (fun _ => 1) (etaG 3 1) v ∧
      Transcribes (fun _ => 1) (fun _ => 1) (etaG 3 (-1)) v ∧ ¬ PremN v ∧ ∑ a, v a ≠ 0 := by
  intro v
  have hg : ∀ a b, gram v a b = 1 := fun a b => by simp [gram, v, e3_dot]
  refine ⟨fun a b => ?_, fun a b => ?_, fun ⟨a, b, h⟩ => h rfl, fun h => ?_⟩
  · rw [hg]; split_ifs <;> rfl
  · rw [hg]; split_ifs <;> rfl
  · have := congrFun h 0; simp [v, e3] at this

/-- **Drop the dimension rule.** In `ℝ⁴` the orthonormal legs transcribe both conventions locally
and covariantly (`f ≡ 1`, `g ≡ 0`), faithfully, and are not closed. (In `ℝ²` there is no
realisation at all: `nec_D`.) -/
theorem need_dimension :
    let v : Fin 4 → Fin 4 → ℝ := fun a => Pi.single a 1
    Transcribes (fun _ => 1) (fun _ => 0) (etaG 3 1) v ∧
      Transcribes (fun _ => 1) (fun _ => 0) (etaG 3 (-1)) v ∧ PremN v ∧ ∑ a, v a ≠ 0 := by
  intro v
  have hg : ∀ a b, gram v a b = if a = b then 1 else 0 := by
    intro a b
    simp only [gram, of_apply, v, single_dotProduct, one_mul, Pi.single_apply]
  refine ⟨fun a b => by rw [hg], fun a b => by rw [hg], ⟨0, 1, fun h => ?_⟩, fun h => ?_⟩
  · have := congrFun h 0; simp [v] at this
  · have := congrFun h 0; simp [v] at this

/-- The (M)-row Gram matrix `G_aa = (1,3,7,7)c²`, `G_ab = −c²` has rank exactly 3. -/
theorem nec_M2_rank (c : ℝ) (hc : c ≠ 0) : (gram (vM2 c)).rank = 3 := by
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  rw [← Vmat_gram, rank_transpose_mul_self, ← rank_self_mul_transpose]
  have hVV : Vmat (vM2 c) * (Vmat (vM2 c))ᵀ =
      c ^ 2 • !![(4 : ℝ), -1, -1; -1, 7, -1; -1, -1, 7] := by
    ext i j
    rw [Matrix.mul_apply]
    fin_cases i <;> fin_cases j <;>
      simp [Vmat, vM2, Fin.sum_univ_succ] <;> ring_nf <;> rw [h2] <;> ring
  have hu : IsUnit (c ^ 2 • !![(4 : ℝ), -1, -1; -1, 7, -1; -1, -1, 7]) := by
    rw [isUnit_iff_isUnit_det, det_smul, det_fin_three, isUnit_iff_ne_zero]
    simp; norm_num
    exact hc
  rw [hVV, rank_of_isUnit _ hu, Fintype.card_fin]

#print axioms ForcedTetrahedralFrame.rules_force_simplex
#print axioms ForcedTetrahedralFrame.tetrahedron_from_rules
#print axioms ForcedTetrahedralFrame.time_leg_anywhere
#print axioms ForcedTetrahedralFrame.etaG_positive_index
#print axioms ForcedTetrahedralFrame.need_convention_independence
#print axioms ForcedTetrahedralFrame.need_covariance
#print axioms ForcedTetrahedralFrame.need_locality
#print axioms ForcedTetrahedralFrame.need_faithfulness
#print axioms ForcedTetrahedralFrame.need_dimension
#print axioms ForcedTetrahedralFrame.nec_M2_rank

/-! ## Normalisation: the primary derivation of (M) and (R)

A tetrad is an *orthonormal* frame: `η(e_a, e_b) = η_ab`, so every leg has unit magnitude
`|η(e_a, e_a)| = 1`. The time leg's `−1` is that unit magnitude carrying the sign of a timelike
vector; the sign records the vector's type, not a smaller size. A frame with diagonal
`(−0.9, 0.4, 1, 1)` is not a tetrad. The realisation must preserve what the tetrad fixes:
* **Magnitude-preserving:** `|v_a|² = c² · |η(e_a, e_a)|` for one scale `c > 0`
  (a squared length carries the magnitude; it cannot carry the sign).
* **Relation-preserving:** pairs with equal `η(e_a, e_b)` have equal `v_a · v_b`.
These are stated for an *arbitrary* tetrad `e` (any Lorentz transform of the standard frame,
reflections included).
-/

/-- `e` is a tetrad: `η(e_a, e_b) = η_ab`. -/
def IsTetrad (e : Fin 4 → Fin 4 → ℝ) : Prop := ∀ a b, mink (e a) (e b) = eta a b

def PreservesMagnitude (e : Fin 4 → Fin 4 → ℝ) (v : Fin 4 → Fin 3 → ℝ) (c : ℝ) : Prop :=
  0 < c ∧ ∀ a, v a ⬝ᵥ v a = c ^ 2 * |mink (e a) (e a)|

def PreservesRelation (e : Fin 4 → Fin 4 → ℝ) (v : Fin 4 → Fin 3 → ℝ) : Prop :=
  ∀ a b a' b', a ≠ b → a' ≠ b' → mink (e a) (e b) = mink (e a') (e b') →
    v a ⬝ᵥ v b = v a' ⬝ᵥ v b'

/-- Every leg of a tetrad has unit magnitude (time leg included). -/
theorem tetrad_unit_magnitude (e : Fin 4 → Fin 4 → ℝ) (he : IsTetrad e) (a : Fin 4) :
    |mink (e a) (e a)| = 1 := by
  rw [he a a, eta_diag]; split_ifs <;> norm_num

/-- **Sign × magnitude.** Each diagonal entry of `η` is its sign times its magnitude, and the
magnitude is the same `1` on every leg: `η = diag(−1,1,1,1) = diag(−,+,+,+) · 1`. -/
theorem eta_sign_times_magnitude :
    (∀ a, eta a a = (if a = 0 then -1 else 1) * |eta a a|) ∧ (∀ a, |eta a a| = 1) ∧
      (∀ a b, |eta a a| = |eta b b|) := by
  have h1 : ∀ a, |eta a a| = 1 := fun a => by rw [eta_diag]; split_ifs <;> norm_num
  refine ⟨fun a => ?_, h1, fun a b => by rw [h1, h1]⟩
  rw [h1, mul_one, eta_diag]

#print axioms ForcedTetrahedralFrame.eta_sign_times_magnitude

/-- The Minkowski form is linear in its first argument. -/
lemma mink_sum (g : Fin 4 → ℝ) (x : Fin 4 → Fin 4 → ℝ) (y : Fin 4 → ℝ) :
    mink (∑ a, g a • x a) y = ∑ a, g a * mink (x a) y := by
  simp only [mink, Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Fin.sum_univ_four]; ring

/-- **The legs are vectors, and they form a basis.** A tetrad's legs are linearly independent;
in particular every leg, the time leg included, is a non-zero vector. This is the paper's
reason for (N). -/
theorem tetrad_basis (e : Fin 4 → Fin 4 → ℝ) (he : IsTetrad e) :
    LinearIndependent ℝ e ∧ ∀ a, e a ≠ 0 := by
  have hli : LinearIndependent ℝ e := by
    rw [Fintype.linearIndependent_iff]
    intro g hg b
    have h := mink_sum g e (e b)
    rw [hg, show mink 0 (e b) = 0 by simp [mink]] at h
    simp only [show ∀ a, mink (e a) (e b) = eta a b from fun a => he a b] at h
    have : ∑ a, g a * eta a b = g b * eta b b := by
      rw [Finset.sum_eq_single b (fun a _ hab => by rw [eta_off hab, mul_zero])
        (fun h => absurd (Finset.mem_univ b) h)]
    rw [this] at h
    have hb : eta b b ≠ 0 := by rw [eta_diag]; split_ifs <;> norm_num
    exact (mul_eq_zero.mp h.symm).resolve_right hb
  exact ⟨hli, fun a => hli.ne_zero a⟩

#print axioms ForcedTetrahedralFrame.tetrad_basis

/-- **Normalisation theorem.** For any tetrad, a magnitude- and relation-preserving realisation
in `ℝ³` with legs not all equal is the closed regular tetrahedron, Eq. (1), unique up to `O(3)`. -/
theorem normalisation_forces_tetrahedron (e : Fin 4 → Fin 4 → ℝ) (he : IsTetrad e)
    (v : Fin 4 → Fin 3 → ℝ) (c : ℝ) (hmag : PreservesMagnitude e v c)
    (hrel : PreservesRelation e v) (hN : PremN v) :
    ∑ a, v a = 0 ∧
      gram v = c ^ 2 • (1 : Matrix (Fin 4) (Fin 4) ℝ) - (c ^ 2 / 3) • (J 4 - 1) ∧
      ∃! Q : Matrix (Fin 3) (Fin 3) ℝ,
        Q ∈ Matrix.orthogonalGroup (Fin 3) ℝ ∧ Vmat v = Q * ((c / Real.sqrt 3) • Mmat) := by
  have hM : PremM v c := ⟨hmag.1, fun a => by rw [hmag.2 a, tetrad_unit_magnitude e he a, mul_one]⟩
  have hR : PremR v := ⟨v 0 ⬝ᵥ v 1, fun a b hab =>
    hrel a b 0 1 hab (by decide) (by rw [he, he, eta_off hab, eta_off (by decide)])⟩
  have h : Realisation 4 3 v c := ⟨hR, hM, hN⟩
  exact ⟨(forced_gram v c h).1, (forced_gram v c h).2, cor1_unique v c h⟩

/-- The standard tetrad `e_a = ê_a` is a tetrad. -/
theorem standard_isTetrad : IsTetrad (fun a => Pi.single a 1) := by
  intro a b
  fin_cases a <;> fin_cases b <;> simp [mink, eta]

/-- The observer's projection does not preserve magnitude: it gives the unit-magnitude time leg
zero length. -/
theorem observer_breaks_normalisation (c : ℝ) :
    ¬ PreservesMagnitude (fun a => Pi.single a 1) observer c := by
  rintro ⟨hc, h⟩
  have := h 0
  rw [tetrad_unit_magnitude _ standard_isTetrad 0] at this
  simp [observer] at this
  exact (pow_ne_zero 2 hc.ne') this.symm

/-- The observer's projection violates the hypothesis **exactly once**: for the standard tetrad
with `c = 1` it preserves every relation and every spatial leg's magnitude, and fails only on the
time leg, which it sends to the zero vector. -/
theorem observer_violates_only_time_leg :
    PreservesRelation (fun a => Pi.single a 1) observer ∧
      (∀ a, a ≠ 0 → observer a ⬝ᵥ observer a =
        1 ^ 2 * |mink (Pi.single a 1) (Pi.single a 1)|) ∧
      observer 0 ⬝ᵥ observer 0 ≠ 1 ^ 2 * |mink (Pi.single 0 1) (Pi.single 0 1)| := by
  have hu := tetrad_unit_magnitude _ standard_isTetrad
  refine ⟨fun a b a' b' hab hab' _ => ?_, fun a ha => ?_, ?_⟩
  · have h1 := observer_gram a b; have h2 := observer_gram a' b'
    simp only [gram, of_apply, ite_eq_right hab, ite_eq_right hab'] at h1 h2
    rw [h1, h2]
  · have h := observer_gram a a
    simp only [gram, of_apply, ite_eq_right ha] at h
    rw [h, hu a]; norm_num
  · have h := observer_gram 0 0
    simp only [gram, of_apply] at h
    rw [h, hu 0]; norm_num

#print axioms ForcedTetrahedralFrame.observer_violates_only_time_leg

/-- The rules are satisfiable: the columns of `M` preserve magnitude (`c = √3`) and relation for
the standard tetrad. -/
theorem normalisation_satisfiable :
    PreservesMagnitude (fun a => Pi.single a 1) Mcol (Real.sqrt 3) ∧
      PreservesRelation (fun a => Pi.single a 1) Mcol ∧ PremN Mcol := by
  obtain ⟨⟨⟨β, hR⟩, ⟨hc, hM⟩, hN⟩, -⟩ := cor1_M_realises
  refine ⟨⟨hc, fun a => ?_⟩, fun a b a' b' hab hab' _ => by rw [hR a b hab, hR a' b' hab'], hN⟩
  rw [hM a, tetrad_unit_magnitude _ standard_isTetrad a, mul_one]

#print axioms ForcedTetrahedralFrame.normalisation_forces_tetrahedron
#print axioms ForcedTetrahedralFrame.observer_breaks_normalisation
#print axioms ForcedTetrahedralFrame.normalisation_satisfiable

end ForcedTetrahedralFrame

/-! ## Axiom audit -/
#print axioms ForcedTetrahedralFrame.rigidity
#print axioms ForcedTetrahedralFrame.forced_gram
#print axioms ForcedTetrahedralFrame.cor1_geometry
#print axioms ForcedTetrahedralFrame.cor1_M_realises
#print axioms ForcedTetrahedralFrame.cor1_unique
#print axioms ForcedTetrahedralFrame.cor2_exists_iff
#print axioms ForcedTetrahedralFrame.cor2_forced_iff
#print axioms ForcedTetrahedralFrame.three_is_unique
#print axioms ForcedTetrahedralFrame.cor2_all_gram_realisable
#print axioms ForcedTetrahedralFrame.K_one_no_realisation
#print axioms ForcedTetrahedralFrame.forced_vacuous
#print axioms ForcedTetrahedralFrame.cor3_parity
#print axioms ForcedTetrahedralFrame.cor3_cube
#print axioms ForcedTetrahedralFrame.nec_R
#print axioms ForcedTetrahedralFrame.nec_M1
#print axioms ForcedTetrahedralFrame.nec_M2
#print axioms ForcedTetrahedralFrame.nec_N
#print axioms ForcedTetrahedralFrame.nec_D
#print axioms ForcedTetrahedralFrame.gram_perm_invariant
#print axioms ForcedTetrahedralFrame.no_orthogonal_tetrad
