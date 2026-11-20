import ForcedTetrahedralFrame

/-!
# Lean 4 / Mathlib formalisation of
#   S. Nelson, "The Stellated Octahedron, the Cube and the Hadamard Matrix"
#   (Field Dynamics Research, supplementary material)

Builds on `ForcedTetrahedralFrame` (the forced Gram matrix), which the paper cites in the proof of
Theorem 1 (a) ⇒ (b): that step is the theorem `ForcedTetrahedralFrame.general_forced` itself.

## How to referee this file
A Lean proof can only be wrong in its *statements*: the proofs are machine-checked. Check these
definitions against the paper:
* `IsSign A`: every entry of `A` is `+1` or `−1`.
* `col M a`: the `a`-th column of `M`, a point of the cube `Q_D = {−1,+1}^D`.
* `IsCubeSimplex M`: `M` is a sign matrix whose `D + 1` columns are distinct and pairwise
  equidistant (squared distance `d` for every pair).
* `Hhat M`: `M` bordered by a row of ones on top.
* `IsHadamard H`: `H` is a sign matrix with `Hᵀ H = n I`.
* `cubeQ D`, `simplexAndImage M`: the cube's vertices and `V ∪ (−V)` as finite sets of points.
* `chi S x = ∏_{i ∈ S} x_i`: the Walsh function of `S ⊆ {1,2,3}`.

Headline results, in the order of the paper:
* `theorem1`: (a) cube simplex ⇔ (b) `MᵀM = KI − J` ⇔ (c) `Ĥ` Hadamard ⇔ (d) `M𝟏 = 0, MMᵀ = KI`,
  for every `D ≥ 1`; (a) ⇒ (b) is `ForcedTetrahedralFrame.general_forced`.
* `normalise_hadamard`: cube simplices and normalised Hadamard matrices are the same objects.
* `hadamard_four_dvd` (Lemma): order `n > 2` ⇒ `4 ∣ n`; `corollary1`, `no_cube_simplex_two`,
  `cube_simplex_three`.
* `theorem2`: `−V` is a cube simplex, disjoint from `V`, `|V ∪ −V| = 2(D+1)`, and `V ∪ −V = Q_D`
  iff `D = 3`; `theorem2_parity_classes`: for `D = 3`, `V` and `−V` are `x₁x₂x₃ = ±p`.
* `theorem3`: `W = [[Ĥ, Ĥ], [Ĥ, −Ĥ]] = H₂ ⊗ Ĥ` for any ordering of the parity class `+1`;
  `theorem3_M` for the paper's `M`; `chi_neg`, `chi_compl`.
* `corollary2_balanced`, `corollary2_distinct_splits`, `corollary2_halves`, `corollary2_count`,
  `corollary2_pairs`.
-/

open Matrix Finset

namespace HadamardCubeFrame

open ForcedTetrahedralFrame (J Realisation general_forced dot_self_nonneg Mmat Mcol MMt)

/-! ## Definitions -/

def IsSign {m n : ℕ} (A : Matrix (Fin m) (Fin n) ℝ) : Prop := ∀ i j, A i j = 1 ∨ A i j = -1

/-- Column `a` of `M`. -/
def col {D K : ℕ} (M : Matrix (Fin D) (Fin K) ℝ) (a : Fin K) : Fin D → ℝ := fun i => M i a

/-- A cube simplex: `D + 1` distinct, pairwise equidistant points of `{−1,+1}^D`. -/
def IsCubeSimplex {D : ℕ} (M : Matrix (Fin D) (Fin (D + 1)) ℝ) : Prop :=
  IsSign M ∧ (∀ a b, a ≠ b → col M a ≠ col M b) ∧
    ∃ d : ℝ, ∀ a b, a ≠ b → (col M a - col M b) ⬝ᵥ (col M a - col M b) = d

/-- `M` bordered by a row of ones. -/
def Hhat {D : ℕ} (M : Matrix (Fin D) (Fin (D + 1)) ℝ) : Matrix (Fin (D + 1)) (Fin (D + 1)) ℝ :=
  Matrix.of fun r c => Fin.cases (1 : ℝ) (fun i => M i c) r

def IsHadamard {n : ℕ} (H : Matrix (Fin n) (Fin n) ℝ) : Prop :=
  IsSign H ∧ Hᵀ * H = (n : ℝ) • (1 : Matrix (Fin n) (Fin n) ℝ)

/-! ## Basic lemmas -/

lemma sign_sq {x : ℝ} (h : x = 1 ∨ x = -1) : x * x = 1 := by
  rcases h with h | h <;> rw [h] <;> norm_num

lemma sign_dot_self {D : ℕ} (v : Fin D → ℝ) (hv : ∀ i, v i = 1 ∨ v i = -1) : v ⬝ᵥ v = D := by
  simp [dotProduct, fun i => sign_sq (hv i)]

lemma gram_apply {D K : ℕ} (M : Matrix (Fin D) (Fin K) ℝ) (a b : Fin K) :
    (Mᵀ * M) a b = col M a ⬝ᵥ col M b := by
  rw [Matrix.mul_apply]; simp [col, dotProduct]

lemma Hhat_sign {D : ℕ} (M : Matrix (Fin D) (Fin (D + 1)) ℝ) (hM : IsSign M) : IsSign (Hhat M) := by
  intro r c
  refine Fin.cases ?_ (fun i => ?_) r
  · simp [Hhat]
  · simpa [Hhat] using hM i c

/-- `Ĥᵀ Ĥ = J + Mᵀ M`. -/
lemma HhatT_Hhat {D : ℕ} (M : Matrix (Fin D) (Fin (D + 1)) ℝ) :
    (Hhat M)ᵀ * Hhat M = J (D + 1) + Mᵀ * M := by
  ext a b
  rw [Matrix.mul_apply, Matrix.add_apply, Matrix.mul_apply, Fin.sum_univ_succ]
  simp [Hhat, J]

/-- Entries of `Ĥ Ĥᵀ`. -/
lemma Hhat_HhatT_zero_zero {D : ℕ} (M : Matrix (Fin D) (Fin (D + 1)) ℝ) :
    (Hhat M * (Hhat M)ᵀ) 0 0 = (D + 1 : ℕ) := by
  rw [Matrix.mul_apply]; simp [Hhat]

lemma Hhat_HhatT_zero_succ {D : ℕ} (M : Matrix (Fin D) (Fin (D + 1)) ℝ) (i : Fin D) :
    (Hhat M * (Hhat M)ᵀ) 0 i.succ = (M *ᵥ fun _ => 1) i := by
  rw [Matrix.mul_apply]; simp [Hhat, mulVec, dotProduct]

lemma Hhat_HhatT_succ_zero {D : ℕ} (M : Matrix (Fin D) (Fin (D + 1)) ℝ) (i : Fin D) :
    (Hhat M * (Hhat M)ᵀ) i.succ 0 = (M *ᵥ fun _ => 1) i := by
  rw [Matrix.mul_apply]; simp [Hhat, mulVec, dotProduct]

lemma Hhat_HhatT_succ_succ {D : ℕ} (M : Matrix (Fin D) (Fin (D + 1)) ℝ) (i j : Fin D) :
    (Hhat M * (Hhat M)ᵀ) i.succ j.succ = (M * Mᵀ) i j := by
  rw [Matrix.mul_apply, Matrix.mul_apply]; simp [Hhat]

/-- For a square matrix, `Hᵀ H = n I ↔ H Hᵀ = n I` (`n ≠ 0`). -/
lemma transpose_mul_eq_iff {n : ℕ} (hn : n ≠ 0) (H : Matrix (Fin n) (Fin n) ℝ) :
    Hᵀ * H = (n : ℝ) • (1 : Matrix (Fin n) (Fin n) ℝ) ↔
      H * Hᵀ = (n : ℝ) • (1 : Matrix (Fin n) (Fin n) ℝ) := by
  have hn' : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hn
  have key : ∀ A B : Matrix (Fin n) (Fin n) ℝ, A * B = (n : ℝ) • 1 ↔ ((n : ℝ)⁻¹ • A) * B = 1 := by
    intro A B
    rw [Matrix.smul_mul]
    constructor
    · intro h; rw [h, smul_smul, inv_mul_cancel₀ hn', one_smul]
    · intro h
      have := congrArg (fun X => (n : ℝ) • X) h
      simp only [smul_smul, mul_inv_cancel₀ hn', one_smul] at this
      exact this
  rw [key, key]
  constructor
  · intro h
    have := mul_eq_one_comm.mp h
    rw [Matrix.mul_smul, ← Matrix.smul_mul] at this
    exact this
  · intro h
    have := mul_eq_one_comm.mp h
    rw [Matrix.mul_smul, ← Matrix.smul_mul] at this
    exact this

/-! ## Theorem 1: the frame is a Hadamard matrix -/

/-- (a) ⇒ (b), via the forced Gram matrix of the tetrad frame (`general_forced`). -/
theorem a_imp_b {D : ℕ} (hD : 1 ≤ D) (M : Matrix (Fin D) (Fin (D + 1)) ℝ) (h : IsCubeSimplex M) :
    Mᵀ * M = ((D + 1 : ℕ) : ℝ) • (1 : Matrix (Fin (D + 1)) (Fin (D + 1)) ℝ) - J (D + 1) := by
  obtain ⟨hs, hdist, d, hd⟩ := h
  have hnorm : ∀ a, col M a ⬝ᵥ col M a = D := fun a => sign_dot_self _ (fun i => hs i a)
  have hDpos : (0 : ℝ) < D := by exact_mod_cast hD
  have hD0 : D ≠ 0 := by omega
  have hR : ∀ a b, a ≠ b → col M a ⬝ᵥ col M b = (2 * D - d) / 2 := by
    intro a b hab
    have := hd a b hab
    rw [sub_dotProduct, dotProduct_sub, dotProduct_sub, hnorm, hnorm,
      dotProduct_comm (col M b) (col M a)] at this
    linarith
  have hreal : Realisation (D + 1) D (col M) (Real.sqrt D) := by
    refine ⟨⟨_, hR⟩, ⟨Real.sqrt_pos.mpr hDpos, fun a => by rw [hnorm, Real.sq_sqrt hDpos.le]⟩,
      ⟨0, 1, hdist 0 1 (by simpa [Fin.ext_iff] using hD0)⟩⟩
  have hoff := (general_forced (Nat.lt_succ_self D) (col M) _ hreal).2
  ext a b
  rw [gram_apply]
  by_cases hab : a = b
  · subst hab; simp [hnorm, J]
  · rw [hoff a b hab, Real.sq_sqrt hDpos.le]
    simp [J, Matrix.one_apply_ne hab]
    field_simp

/-- (b) ⇒ (a). -/
theorem b_imp_a {D : ℕ} (M : Matrix (Fin D) (Fin (D + 1)) ℝ) (hs : IsSign M)
    (hb : Mᵀ * M = ((D + 1 : ℕ) : ℝ) • (1 : Matrix (Fin (D + 1)) (Fin (D + 1)) ℝ) - J (D + 1)) :
    IsCubeSimplex M := by
  have hG : ∀ a b, col M a ⬝ᵥ col M b = if a = b then (D : ℝ) else -1 := by
    intro a b
    rw [← gram_apply, hb]
    by_cases hab : a = b
    · subst hab; simp [J]
    · simp [J, Matrix.one_apply_ne hab, hab]
  have hdist : ∀ a b, a ≠ b → (col M a - col M b) ⬝ᵥ (col M a - col M b) = 2 * (D + 1) := by
    intro a b hab
    rw [sub_dotProduct, dotProduct_sub, dotProduct_sub, hG, hG, hG, hG, ite_eq_left rfl, ite_eq_left rfl,
      ite_eq_right hab, ite_eq_right (Ne.symm hab)]
    ring
  refine ⟨hs, fun a b hab h => ?_, _, hdist⟩
  have := hdist a b hab
  rw [h, sub_self, zero_dotProduct] at this
  have : (0 : ℝ) ≤ D := by positivity
  linarith

/-- **Theorem 1.** For a `D × (D+1)` sign matrix `M` (`D ≥ 1`) the following are equivalent:
(a) its columns form a cube simplex; (b) `MᵀM = KI − J`; (c) `Ĥ` is a Hadamard matrix;
(d) `M𝟏 = 0` and `MMᵀ = K I_D`. -/
theorem theorem1 {D : ℕ} (hD : 1 ≤ D) (M : Matrix (Fin D) (Fin (D + 1)) ℝ) (hs : IsSign M) :
    List.TFAE [IsCubeSimplex M,
      Mᵀ * M = ((D + 1 : ℕ) : ℝ) • (1 : Matrix (Fin (D + 1)) (Fin (D + 1)) ℝ) - J (D + 1),
      IsHadamard (Hhat M),
      (M *ᵥ fun _ => (1 : ℝ)) = 0 ∧ M * Mᵀ = ((D + 1 : ℕ) : ℝ) • (1 : Matrix (Fin D) (Fin D) ℝ)] := by
  have hbc : Mᵀ * M = ((D + 1 : ℕ) : ℝ) • (1 : Matrix (Fin (D + 1)) (Fin (D + 1)) ℝ) - J (D + 1) ↔
      (Hhat M)ᵀ * Hhat M = ((D + 1 : ℕ) : ℝ) • (1 : Matrix (Fin (D + 1)) (Fin (D + 1)) ℝ) := by
    rw [HhatT_Hhat]
    constructor
    · intro h; rw [h]; abel
    · intro h; rw [← h]; abel
  have hcd : (Hhat M) * (Hhat M)ᵀ = ((D + 1 : ℕ) : ℝ) • (1 : Matrix (Fin (D + 1)) (Fin (D + 1)) ℝ) ↔
      ((M *ᵥ fun _ => (1 : ℝ)) = 0 ∧ M * Mᵀ = ((D + 1 : ℕ) : ℝ) • (1 : Matrix (Fin D) (Fin D) ℝ)) := by
    constructor
    · intro h
      refine ⟨funext fun i => ?_, ?_⟩
      · have := congrFun (congrFun h 0) i.succ
        rw [Hhat_HhatT_zero_succ] at this
        simpa [Matrix.one_apply_ne (Fin.succ_ne_zero i).symm] using this
      · ext i j
        have := congrFun (congrFun h i.succ) j.succ
        rw [Hhat_HhatT_succ_succ] at this
        simpa [Matrix.one_apply, Fin.succ_inj] using this
    · rintro ⟨h1, h2⟩
      ext r c
      refine Fin.cases ?_ (fun i => ?_) r <;> refine Fin.cases ?_ (fun j => ?_) c
      · rw [Hhat_HhatT_zero_zero]; simp
      · rw [Hhat_HhatT_zero_succ, h1]; simp [Matrix.one_apply_ne (Fin.succ_ne_zero j).symm]
      · rw [Hhat_HhatT_succ_zero, h1]; simp [Matrix.one_apply_ne (Fin.succ_ne_zero i)]
      · rw [Hhat_HhatT_succ_succ, h2]; simp [Matrix.one_apply, Fin.succ_inj]
  tfae_have 1 → 2 := a_imp_b hD M
  tfae_have 2 → 1 := b_imp_a M hs
  tfae_have 2 ↔ 3 := by
    rw [hbc]; exact ⟨fun h => ⟨Hhat_sign M hs, h⟩, fun h => h.2⟩
  tfae_have 3 ↔ 4 := by
    rw [← hcd, ← transpose_mul_eq_iff (Nat.succ_ne_zero D)]
    exact ⟨fun h => h.2, fun h => ⟨Hhat_sign M hs, h⟩⟩
  tfae_finish

/-! ## Remark: normalising a Hadamard matrix -/

/-- Negating columns turns any Hadamard matrix into one with first row `𝟏ᵀ`, whose remaining rows
form a cube simplex: cube simplices and normalised Hadamard matrices are the same objects. -/
theorem normalise_hadamard {D : ℕ} (hD : 1 ≤ D) (H : Matrix (Fin (D + 1)) (Fin (D + 1)) ℝ)
    (hH : IsHadamard H) :
    ∃ M : Matrix (Fin D) (Fin (D + 1)) ℝ, IsHadamard (Hhat M) ∧ IsCubeSimplex M ∧
      ∀ r c, Hhat M r c = H r c * H 0 c := by
  obtain ⟨hs, hHH⟩ := hH
  let H' : Matrix (Fin (D + 1)) (Fin (D + 1)) ℝ := Matrix.of fun r c => H r c * H 0 c
  let M : Matrix (Fin D) (Fin (D + 1)) ℝ := Matrix.of fun i c => H i.succ c * H 0 c
  have hHM : Hhat M = H' := by
    ext r c; refine Fin.cases ?_ (fun i => ?_) r
    · simp [Hhat, H', sign_sq (hs 0 c)]
    · simp [Hhat, H', M]
  have hMs : IsSign M := by
    intro i c
    simp only [M, of_apply]
    rcases hs i.succ c with h1 | h1 <;> rcases hs 0 c with h2 | h2 <;> rw [h1, h2] <;> norm_num
  have hH' : H'ᵀ * H' = ((D + 1 : ℕ) : ℝ) • (1 : Matrix (Fin (D + 1)) (Fin (D + 1)) ℝ) := by
    ext a b
    have h := congrFun (congrFun hHH a) b
    rw [Matrix.mul_apply] at h ⊢
    simp only [H', transpose_apply, of_apply]
    have : ∀ r, H r a * H 0 a * (H r b * H 0 b) = (H r a * H r b) * (H 0 a * H 0 b) :=
      fun r => by ring
    simp only [this, ← Finset.sum_mul]
    simp only [transpose_apply] at h
    rw [h]
    by_cases hab : a = b
    · subst hab; simp [sign_sq (hs 0 a)]
    · simp [Matrix.one_apply_ne hab]
  have hHad : IsHadamard (Hhat M) := ⟨Hhat_sign M hMs, by rw [hHM]; exact hH'⟩
  refine ⟨M, hHad, ?_, fun r c => by rw [hHM]; rfl⟩
  exact ((theorem1 hD M hMs).out 3 1).mp hHad

/-! ## Lemma (Hadamard) and Corollary 1 -/

/-- **Lemma (Hadamard).** A Hadamard matrix of order `n > 2` has `4 ∣ n`.
Normalise the first row to ones; then `Σ_c (1 + r₁)(1 + r₂) = n`, and each term is `0` or `4`. -/
theorem hadamard_four_dvd {n : ℕ} (hn : 2 < n) (H : Matrix (Fin n) (Fin n) ℝ) (hH : IsHadamard H) :
    4 ∣ n := by
  obtain ⟨m, rfl⟩ : ∃ m, n = m + 1 := ⟨n - 1, by omega⟩
  obtain ⟨M, hHad, -, -⟩ := normalise_hadamard (by omega) H hH
  obtain ⟨hs, hHH⟩ := hHad
  have hrows := (transpose_mul_eq_iff (Nat.succ_ne_zero m) _).mp hHH
  have e : ∀ r s : Fin (m + 1), ∑ c, Hhat M r c * Hhat M s c = if r = s then ((m + 1 : ℕ) : ℝ) else 0 := by
    intro r s
    have := congrFun (congrFun hrows r) s
    rw [Matrix.mul_apply] at this
    simp only [transpose_apply] at this
    rw [this]; by_cases h : r = s <;> simp [h]
  let r1 : Fin (m + 1) := ⟨1, by omega⟩
  let r2 : Fin (m + 1) := ⟨2, by omega⟩
  have h01 := e 0 r1; have h02 := e 0 r2; have h12 := e r1 r2
  rw [ite_eq_right (by simp [r1, Fin.ext_iff])] at h01
  rw [ite_eq_right (by simp [r2, Fin.ext_iff])] at h02
  rw [ite_eq_right (by simp [r1, r2, Fin.ext_iff])] at h12
  have hrow0 : ∀ c, Hhat M 0 c = 1 := fun c => by simp [Hhat]
  simp only [hrow0, one_mul] at h01 h02
  -- the counting identity
  have hterm : ∀ c, (1 + Hhat M r1 c) * (1 + Hhat M r2 c) =
      if Hhat M r1 c = 1 ∧ Hhat M r2 c = 1 then 4 else 0 := by
    intro c
    rcases hs r1 c with h1 | h1 <;> rcases hs r2 c with h2 | h2 <;> simp [h1, h2] <;> norm_num
  have hsum : ∑ c, (1 + Hhat M r1 c) * (1 + Hhat M r2 c) = ((m + 1 : ℕ) : ℝ) := by
    have : ∀ c, (1 + Hhat M r1 c) * (1 + Hhat M r2 c) =
        1 + Hhat M r1 c + Hhat M r2 c + Hhat M r1 c * Hhat M r2 c := fun c => by ring
    simp only [this, Finset.sum_add_distrib, h01, h02, h12]
    simp
  simp only [hterm, Finset.sum_ite, Finset.sum_const_zero, add_zero, Finset.sum_const,
    nsmul_eq_mul] at hsum
  set N := (Finset.univ.filter fun c => Hhat M r1 c = 1 ∧ Hhat M r2 c = 1).card with hN
  refine ⟨N, ?_⟩
  have hc : ((m + 1 : ℕ) : ℝ) = 4 * (N : ℝ) := by linarith
  exact_mod_cast hc

/-- **Corollary 1.** A cube simplex in `Q_D` exists only if `D = 1` or `4 ∣ D + 1`; the first case
beyond the segment is `D = 3` (`no_cube_simplex_two`, `cube_simplex_three`). -/
theorem corollary1 {D : ℕ} (hD : 1 ≤ D) (M : Matrix (Fin D) (Fin (D + 1)) ℝ) (h : IsCubeSimplex M) :
    D = 1 ∨ 4 ∣ D + 1 := by
  rcases Nat.lt_or_ge D 2 with h2 | h2
  · left; omega
  · right
    exact hadamard_four_dvd (by omega) _ (((theorem1 hD M h.1).out 1 3).mp h)

theorem no_cube_simplex_two (M : Matrix (Fin 2) (Fin 3) ℝ) : ¬ IsCubeSimplex M := by
  intro h
  rcases corollary1 (by norm_num) M h with h | h <;> omega

theorem cube_simplex_three : IsCubeSimplex Mmat := by
  have hs : IsSign Mmat := by
    intro i j; fin_cases i <;> fin_cases j <;> simp [Mmat]
  refine b_imp_a Mmat hs ?_
  rw [ForcedTetrahedralFrame.MtM]
  ext a b; by_cases h : a = b
  · subst h; simp [J]; norm_num
  · simp [J, Matrix.one_apply_ne h]

#print axioms HadamardCubeFrame.theorem1
#print axioms HadamardCubeFrame.normalise_hadamard
#print axioms HadamardCubeFrame.hadamard_four_dvd
#print axioms HadamardCubeFrame.corollary1
#print axioms HadamardCubeFrame.no_cube_simplex_two
#print axioms HadamardCubeFrame.cube_simplex_three

/-! ## Theorem 2: only three dimensions fill the cube -/

section Cube

open Classical

/-- The sign vector of a Boolean vector. -/
noncomputable def signVec {D : ℕ} (b : Fin D → Bool) : Fin D → ℝ := fun i => if b i then 1 else -1

lemma signVec_injective {D : ℕ} : Function.Injective (signVec (D := D)) := by
  intro b b' h
  funext i
  have := congrFun h i
  simp only [signVec] at this
  cases hb : b i <;> cases hb' : b' i <;> simp [hb, hb'] at this ⊢ <;> norm_num at this

/-- The vertices of the cube `Q_D = {−1,+1}^D`. -/
noncomputable def cubeQ (D : ℕ) : Finset (Fin D → ℝ) := Finset.univ.image signVec

lemma card_cubeQ (D : ℕ) : (cubeQ D).card = 2 ^ D := by
  rw [cubeQ, Finset.card_image_of_injective _ signVec_injective, Finset.card_univ,
    Fintype.card_fun, Fintype.card_bool, Fintype.card_fin]

lemma mem_cubeQ {D : ℕ} (x : Fin D → ℝ) : x ∈ cubeQ D ↔ ∀ i, x i = 1 ∨ x i = -1 := by
  constructor
  · intro hx i
    obtain ⟨b, -, rfl⟩ := Finset.mem_image.mp hx
    simp only [signVec]; split_ifs <;> simp
  · intro hx
    refine Finset.mem_image.mpr ⟨fun i => decide (x i = 1), Finset.mem_univ _, funext fun i => ?_⟩
    simp only [signVec]
    rcases hx i with h | h <;> simp [h]; norm_num

/-- `V ∪ (−V)`: a cube simplex and its parity image. -/
noncomputable def simplexAndImage {D : ℕ} (M : Matrix (Fin D) (Fin (D + 1)) ℝ) :
    Finset (Fin D → ℝ) :=
  Finset.univ.image (col M) ∪ Finset.univ.image (fun a => -col M a)

lemma lt_two_pow_of_four_le (n : ℕ) (h : 4 ≤ n) : 2 * (n + 1) < 2 ^ n := by
  induction n, h using Nat.le_induction with
  | base => norm_num
  | succ n hn ih => rw [pow_succ]; omega

/-- `2(D+1) = 2^D` exactly when `D = 3`. -/
lemma two_succ_eq_pow_iff (D : ℕ) : 2 * (D + 1) = 2 ^ D ↔ D = 3 := by
  constructor
  · intro h
    by_contra hne
    rcases Nat.lt_or_ge D 4 with h4 | h4
    · interval_cases D <;> simp_all
    · have := lt_two_pow_of_four_le D h4
      omega
  · rintro rfl; norm_num

/-- Gram entries of a cube simplex: `D` on the diagonal, `−1` off it. -/
lemma cube_simplex_gram {D : ℕ} (hD : 1 ≤ D) (M : Matrix (Fin D) (Fin (D + 1)) ℝ)
    (h : IsCubeSimplex M) (a b : Fin (D + 1)) :
    col M a ⬝ᵥ col M b = if a = b then (D : ℝ) else -1 := by
  rw [← gram_apply, a_imp_b hD M h]
  by_cases hab : a = b
  · subst hab; simp [J]
  · simp [J, Matrix.one_apply_ne hab, hab]

/-- **Theorem 2.** For a cube simplex `V` in `Q_D`, `D ≥ 2`: `−V` is a cube simplex, `V` and `−V`
are disjoint, `V ∪ (−V)` has `2(D+1)` points of the cube, and `V ∪ (−V) = Q_D` iff `D = 3`. -/
theorem theorem2 {D : ℕ} (hD : 2 ≤ D) (M : Matrix (Fin D) (Fin (D + 1)) ℝ) (h : IsCubeSimplex M) :
    IsCubeSimplex (-M) ∧ (∀ a b, col M a ≠ -col M b) ∧
      (simplexAndImage M).card = 2 * (D + 1) ∧ simplexAndImage M ⊆ cubeQ D ∧
      (simplexAndImage M = cubeQ D ↔ D = 3) := by
  have hD1 : 1 ≤ D := by omega
  have hG := cube_simplex_gram hD1 M h
  have hneg : IsCubeSimplex (-M) := by
    refine b_imp_a (-M) (fun i j => ?_) ?_
    · rcases h.1 i j with h' | h' <;> simp [h']
    · rw [transpose_neg, Matrix.neg_mul, Matrix.mul_neg, neg_neg]; exact a_imp_b hD1 M h
  have hdisj : ∀ a b, col M a ≠ -col M b := by
    intro a b hab
    have := hG a b
    rw [hab, neg_dotProduct, hG b b, ite_eq_left rfl] at this
    have hDr : (2 : ℝ) ≤ D := by exact_mod_cast hD
    split_ifs at this <;> linarith
  have hinj : Function.Injective (col M) := by
    intro a b hab; by_contra hne; exact h.2.1 a b hne hab
  have hinj' : Function.Injective (fun a => -col M a) := by
    intro a b hab; exact hinj (neg_injective hab)
  have hcard : (simplexAndImage M).card = 2 * (D + 1) := by
    rw [simplexAndImage, Finset.card_union_of_disjoint, Finset.card_image_of_injective _ hinj,
      Finset.card_image_of_injective _ hinj', Finset.card_univ, Fintype.card_fin]
    · ring
    · rw [Finset.disjoint_left]
      intro x hx hx'
      obtain ⟨a, -, rfl⟩ := Finset.mem_image.mp hx
      obtain ⟨b, -, hb⟩ := Finset.mem_image.mp hx'
      exact hdisj a b hb.symm
  have hsub : simplexAndImage M ⊆ cubeQ D := by
    intro x hx
    rw [mem_cubeQ]
    intro i
    rcases Finset.mem_union.mp hx with hx | hx
    · obtain ⟨a, -, rfl⟩ := Finset.mem_image.mp hx
      exact h.1 i a
    · obtain ⟨a, -, rfl⟩ := Finset.mem_image.mp hx
      rcases h.1 i a with h' | h' <;> simp [col, h']
  refine ⟨hneg, hdisj, hcard, hsub, ?_⟩
  rw [← two_succ_eq_pow_iff, ← hcard, ← card_cubeQ]
  constructor
  · intro heq; rw [heq]
  · intro hc; exact Finset.eq_of_subset_of_card_le hsub (by rw [hc])

/-- In `Q_3`, inner product `−1` means the points differ in exactly two coordinates, so they have
the same product `x₁x₂x₃`. -/
lemma prod_eq_of_dot_neg_one (u v : Fin 3 → ℝ) (hu : ∀ i, u i = 1 ∨ u i = -1)
    (hv : ∀ i, v i = 1 ∨ v i = -1) (h : u ⬝ᵥ v = -1) : u 0 * u 1 * u 2 = v 0 * v 1 * v 2 := by
  simp only [dotProduct, Fin.sum_univ_three] at h
  rcases hu 0 with a0 | a0 <;> rcases hu 1 with a1 | a1 <;> rcases hu 2 with a2 | a2 <;>
    rcases hv 0 with b0 | b0 <;> rcases hv 1 with b1 | b1 <;> rcases hv 2 with b2 | b2 <;>
    simp only [a0, a1, a2, b0, b1, b2] at h ⊢ <;> revert h <;> norm_num

/-- **Theorem 2 (D = 3).** A cube simplex `V` in `Q_3` and its image `−V` are the two parity classes
`x₁x₂x₃ = p` and `x₁x₂x₃ = −p`, `p = ±1`. -/
theorem theorem2_parity_classes (M : Matrix (Fin 3) (Fin 4) ℝ) (h : IsCubeSimplex M) :
    ∃ p : ℝ, (p = 1 ∨ p = -1) ∧ ∀ x ∈ cubeQ 3,
      ((∃ a, x = col M a) ↔ x 0 * x 1 * x 2 = p) ∧ ((∃ a, x = -col M a) ↔ x 0 * x 1 * x 2 = -p) := by
  have hG := cube_simplex_gram (by norm_num) M h
  have hs : ∀ a i, col M a i = 1 ∨ col M a i = -1 := fun a i => h.1 i a
  set p := col M 0 0 * col M 0 1 * col M 0 2 with hp
  have hcol : ∀ a, col M a 0 * col M a 1 * col M a 2 = p := by
    intro a
    by_cases ha : a = 0
    · rw [ha]
    · have := hG a 0; rw [ite_eq_right ha] at this
      exact prod_eq_of_dot_neg_one _ _ (hs a) (hs 0) this
  have hnegcol : ∀ a, (-col M a) 0 * (-col M a) 1 * (-col M a) 2 = -p := by
    intro a; simp only [Pi.neg_apply]; rw [← hcol a]; ring
  have hp1 : p = 1 ∨ p = -1 := by
    rcases hs 0 0 with a | a <;> rcases hs 0 1 with b | b <;> rcases hs 0 2 with c | c <;>
      simp [hp, a, b, c]
  have hpne : p ≠ -p := by rcases hp1 with h1 | h1 <;> rw [h1] <;> norm_num
  obtain ⟨-, -, -, -, hfill⟩ := theorem2 (by norm_num) M h
  have hall : simplexAndImage M = cubeQ 3 := hfill.mpr rfl
  refine ⟨p, hp1, fun x hx => ?_⟩
  rw [← hall] at hx
  rcases Finset.mem_union.mp hx with hx | hx
  · obtain ⟨a, -, rfl⟩ := Finset.mem_image.mp hx
    refine ⟨⟨fun _ => hcol a, fun _ => ⟨a, rfl⟩⟩, ⟨?_, ?_⟩⟩
    · rintro ⟨b, hb⟩
      have h1 := hcol a
      rw [hb, hnegcol b] at h1
      exact absurd h1.symm hpne
    · intro h'
      rw [hcol a] at h'
      exact absurd h' hpne
  · obtain ⟨a, -, rfl⟩ := Finset.mem_image.mp hx
    refine ⟨⟨?_, ?_⟩, ⟨fun _ => hnegcol a, fun _ => ⟨a, rfl⟩⟩⟩
    · rintro ⟨b, hb⟩
      have h1 := hnegcol a
      rw [hb, hcol b] at h1
      exact absurd h1 hpne
    · intro h'
      rw [hnegcol a] at h'
      exact absurd h'.symm hpne

end Cube

/-! ## Theorem 3: the Walsh factorisation -/

/-- The Walsh function `χ_S(x) = ∏_{i ∈ S} x_i`. -/
def chi (S : Finset (Fin 3)) (x : Fin 3 → ℝ) : ℝ := ∏ i ∈ S, x i

/-- Even-degree Walsh functions `1, x₂x₃, x₁x₃, x₁x₂` and odd `x₁x₂x₃, x₁, x₂, x₃`. -/
def evenS : Fin 4 → Finset (Fin 3) := ![∅, {1, 2}, {0, 2}, {0, 1}]
def oddS : Fin 4 → Finset (Fin 3) := ![{0, 1, 2}, {0}, {1}, {2}]

/-- The Walsh matrix: rows even then odd functions, columns `v₀,…,v₃, −v₀,…,−v₃`. -/
def walsh (M : Matrix (Fin 3) (Fin 4) ℝ) : Matrix (Fin 4 ⊕ Fin 4) (Fin 4 ⊕ Fin 4) ℝ :=
  Matrix.of fun r c => chi (Sum.elim evenS oddS r) (Sum.elim (col M) (fun a => -col M a) c)

/-- `χ_S(−x) = (−1)^{|S|} χ_S(x)`. -/
lemma chi_neg (S : Finset (Fin 3)) (x : Fin 3 → ℝ) : chi S (-x) = (-1) ^ S.card * chi S x := by
  simp [chi, Finset.prod_neg]

/-- **Theorem 3.** If the columns of the sign matrix `M` form the parity class `x₁x₂x₃ = +1`, then
in the stated ordering `W = H₂ ⊗ Ĥ = [[Ĥ, Ĥ], [Ĥ, −Ĥ]]`. -/
theorem theorem3 (M : Matrix (Fin 3) (Fin 4) ℝ) (hs : IsSign M)
    (hp : ∀ a, M 0 a * M 1 a * M 2 a = 1) :
    walsh M = Matrix.fromBlocks (Hhat M) (Hhat M) (Hhat M) (-Hhat M) := by
  have hsq : ∀ i a, M i a * M i a = 1 := fun i a => sign_sq (hs i a)
  have e0 : ∀ a, M 1 a * M 2 a = M 0 a := fun a => by
    linear_combination (M 0 a) * hp a - (M 1 a * M 2 a) * hsq 0 a
  have e1 : ∀ a, M 0 a * M 2 a = M 1 a := fun a => by
    linear_combination (M 1 a) * hp a - (M 0 a * M 2 a) * hsq 1 a
  have e2 : ∀ a, M 0 a * M 1 a = M 2 a := fun a => by
    linear_combination (M 2 a) * hp a - (M 0 a * M 1 a) * hsq 2 a
  have hH0 : ∀ a, Hhat M 0 a = 1 := fun a => rfl
  have hH1 : ∀ a, Hhat M 1 a = M 0 a := fun a => rfl
  have hH2 : ∀ a, Hhat M 2 a = M 1 a := fun a => rfl
  have hH3 : ∀ a, Hhat M 3 a = M 2 a := fun a => rfl
  have hev : ∀ s a, chi (evenS s) (col M a) = Hhat M s a := by
    intro s a
    fin_cases s
    · simp [chi, evenS, hH0]
    · simp [chi, evenS, col, hH1, e0]
    · simp [chi, evenS, col, hH2, e1]
    · simp [chi, evenS, col, hH3, e2]
  have hod : ∀ s a, chi (oddS s) (col M a) = Hhat M s a := by
    intro s a
    fin_cases s
    · show chi (oddS 0) (col M a) = Hhat M 0 a
      have hu : oddS 0 = Finset.univ := by decide
      rw [chi, hu, Fin.prod_univ_three, hH0]
      exact hp a
    · simp [chi, oddS, col, hH1]
    · simp [chi, oddS, col, hH2]
    · simp [chi, oddS, col, hH3]
  ext r c
  rcases r with s | s <;> rcases c with a | a
  · simp [walsh, hev]
  · simp only [walsh, of_apply, Sum.elim_inl, Sum.elim_inr, fromBlocks_apply₁₂]
    rw [chi_neg, hev]; fin_cases s <;> simp [evenS]
  · simp [walsh, hod]
  · simp only [walsh, of_apply, Sum.elim_inr, fromBlocks_apply₂₂, Matrix.neg_apply]
    rw [chi_neg, hod]; fin_cases s <;> simp [oddS]; norm_num

/-- The paper's frame `M` satisfies the hypotheses of Theorem 3. -/
theorem theorem3_M : walsh Mmat = Matrix.fromBlocks (Hhat Mmat) (Hhat Mmat) (Hhat Mmat) (-Hhat Mmat) :=
  theorem3 Mmat cube_simplex_three.1 (fun a => by fin_cases a <;> simp [Mmat])

/-- On a parity class with product `p`, every Walsh function equals `p` times its complement. -/
lemma chi_compl (x : Fin 3 → ℝ) (hx : ∀ i, x i = 1 ∨ x i = -1) (S : Finset (Fin 3)) :
    chi S x = (x 0 * x 1 * x 2) * chi Sᶜ x := by
  have hall : chi S x * chi Sᶜ x = x 0 * x 1 * x 2 := by
    simp only [chi]; rw [Finset.prod_mul_prod_compl, Fin.prod_univ_three]
  have hc : chi Sᶜ x * chi Sᶜ x = 1 := by
    simp only [chi, ← Finset.prod_mul_distrib]
    exact Finset.prod_eq_one (fun i _ => sign_sq (hx i))
  calc chi S x = chi S x * (chi Sᶜ x * chi Sᶜ x) := by rw [hc, mul_one]
    _ = (chi S x * chi Sᶜ x) * chi Sᶜ x := by ring
    _ = (x 0 * x 1 * x 2) * chi Sᶜ x := by rw [hall]

/-! ## Corollary 2: why four legs -/

/-- Each row of a cube simplex is balanced: it has as many `+1` as `−1` entries. -/
theorem corollary2_balanced {D : ℕ} (hD : 1 ≤ D) (M : Matrix (Fin D) (Fin (D + 1)) ℝ)
    (h : IsCubeSimplex M) (i : Fin D) :
    2 * (Finset.univ.filter fun a => M i a = 1).card = D + 1 := by
  obtain ⟨hrow, -⟩ := ((theorem1 hD M h.1).out 1 4).mp h
  have h0 := congrFun hrow i
  simp only [mulVec, dotProduct, mul_one, Pi.zero_apply] at h0
  have hsplit : ∀ a, M i a = 2 * (if M i a = 1 then 1 else 0) - 1 := by
    intro a; rcases h.1 i a with h' | h' <;> simp [h'] <;> norm_num
  rw [Finset.sum_congr rfl (fun a _ => hsplit a), Finset.sum_sub_distrib, ← Finset.mul_sum,
    Finset.sum_boole, Finset.sum_const, Finset.card_univ, Fintype.card_fin] at h0
  simp only [nsmul_eq_mul, mul_one] at h0
  push_cast at h0
  exact_mod_cast (show (2 * (Finset.univ.filter fun a => M i a = 1).card : ℝ) = D + 1 by
    linarith)

/-- A sign row is determined by its `+1` set. -/
lemma row_eq_of_split {K : ℕ} (u v : Fin K → ℝ) (hu : ∀ a, u a = 1 ∨ u a = -1)
    (hv : ∀ a, v a = 1 ∨ v a = -1)
    (h : (Finset.univ.filter fun a => u a = 1) = Finset.univ.filter fun a => v a = 1) : u = v := by
  funext a
  have := congrArg (a ∈ ·) h
  simp only [Finset.mem_filter, Finset.mem_univ, true_and, eq_iff_iff] at this
  rcases hu a with h1 | h1 <;> rcases hv a with h2 | h2 <;> simp_all

/-- Different rows of a cube simplex give different splits of the `K` points into halves:
neither the same `+1` set nor complementary ones. -/
theorem corollary2_distinct_splits {D : ℕ} (hD : 1 ≤ D) (M : Matrix (Fin D) (Fin (D + 1)) ℝ)
    (h : IsCubeSimplex M) (i j : Fin D) (hij : i ≠ j) :
    (Finset.univ.filter fun a => M j a = 1) ≠ Finset.univ.filter (fun a => M i a = 1) ∧
      (Finset.univ.filter fun a => M j a = 1) ≠ (Finset.univ.filter fun a => M i a = 1)ᶜ := by
  obtain ⟨-, hMM⟩ := ((theorem1 hD M h.1).out 1 4).mp h
  have hdot : ∀ r s : Fin D, ∑ a, M r a * M s a = if r = s then ((D + 1 : ℕ) : ℝ) else 0 := by
    intro r s
    have := congrFun (congrFun hMM r) s
    rw [Matrix.mul_apply] at this; simp only [transpose_apply] at this
    rw [this]; by_cases hrs : r = s <;> simp [hrs]
  have hK : ((D + 1 : ℕ) : ℝ) ≠ 0 := by positivity
  constructor
  · intro heq
    have := row_eq_of_split _ _ (fun a => h.1 j a) (fun a => h.1 i a) heq
    have h1 := hdot i j; have h2 := hdot i i
    rw [ite_eq_right hij] at h1; rw [ite_eq_left rfl] at h2
    have hji : ∀ a, M j a = M i a := fun a => congrFun this a
    simp only [hji] at h1
    exact hK (h2.symm.trans h1)
  · intro heq
    have hneg : (fun a => M j a) = fun a => -M i a := by
      apply row_eq_of_split _ _ (fun a => h.1 j a)
        (fun a => by rcases h.1 i a with h' | h' <;> simp [h'])
      rw [heq]; ext a
      simp only [Finset.mem_compl, Finset.mem_filter, Finset.mem_univ, true_and]
      rcases h.1 i a with h' | h' <;> simp [h'] <;> norm_num
    have h1 := hdot i j; have h2 := hdot i i
    rw [ite_eq_right hij] at h1; rw [ite_eq_left rfl] at h2
    have h3 : ∑ a, M i a * M j a = -∑ a, M i a * M i a := by
      rw [← Finset.sum_neg_distrib]
      exact Finset.sum_congr rfl (fun a _ => by rw [congrFun hneg a]; ring)
    rw [h1, h2] at h3
    exact hK (by linarith)

/-- There are `C(K, K/2)` halves, i.e. `C(K, K/2)/2` splits; this equals `K − 1`, the number of
rows, exactly for `K = 2` and `K = 4`. -/
theorem corollary2_count (K : ℕ) (hK : 2 ≤ K) (heven : Even K) :
    K.choose (K / 2) = 2 * (K - 1) ↔ K = 2 ∨ K = 4 := by
  obtain ⟨m, rfl⟩ := heven
  have hm : (m + m) / 2 = m := by omega
  rw [hm]
  constructor
  · intro h
    by_contra hne
    have hm3 : 3 ≤ m := by omega
    have h1 : (m + m).choose 2 ≤ (m + m).choose m := by
      have := Nat.choose_le_middle 2 (m + m); rwa [hm] at this
    have h2 : 2 * (m + m).choose 2 = (m + m) * (m + m - 1) := by
      rw [Nat.choose_two_right]
      exact Nat.mul_div_cancel' (Nat.even_mul_pred_self _).two_dvd
    obtain ⟨n, hn⟩ : ∃ n, m + m = n + 1 := ⟨m + m - 1, by omega⟩
    rw [hn, Nat.add_sub_cancel] at h2 h
    rw [hn] at h1
    nlinarith
  · rintro (h | h)
    · obtain rfl : m = 1 := by omega
      decide
    · obtain rfl : m = 2 := by omega
      decide

/-- The halves of `K` points number `C(K, K/2)`; each split into two halves is a half and its
complement, so there are `C(K, K/2)/2` splits. -/
theorem corollary2_halves (K : ℕ) :
    ((Finset.univ : Finset (Fin K)).powersetCard (K / 2)).card = K.choose (K / 2) := by
  rw [Finset.card_powersetCard, Finset.card_univ, Fintype.card_fin]

/-- At `K = 4` the three rows of `M` are the three ways of splitting the four legs into pairs. -/
theorem corollary2_pairs :
    (Finset.univ.filter fun a => Mmat 0 a = 1) = {0, 1} ∧
      (Finset.univ.filter fun a => Mmat 1 a = 1) = {0, 2} ∧
      (Finset.univ.filter fun a => Mmat 2 a = 1) = {0, 3} := by
  refine ⟨?_, ?_, ?_⟩ <;> ext a <;> fin_cases a <;> simp [Mmat] <;> norm_num

#print axioms HadamardCubeFrame.card_cubeQ
#print axioms HadamardCubeFrame.two_succ_eq_pow_iff
#print axioms HadamardCubeFrame.theorem2
#print axioms HadamardCubeFrame.theorem2_parity_classes
#print axioms HadamardCubeFrame.theorem3
#print axioms HadamardCubeFrame.theorem3_M
#print axioms HadamardCubeFrame.chi_compl
#print axioms HadamardCubeFrame.corollary2_balanced
#print axioms HadamardCubeFrame.corollary2_distinct_splits
#print axioms HadamardCubeFrame.corollary2_count
#print axioms HadamardCubeFrame.corollary2_halves
#print axioms HadamardCubeFrame.corollary2_pairs

end HadamardCubeFrame
