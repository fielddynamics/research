import TetradScheme
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas

/-!
# Lean 4 / Mathlib formalisation of
#   S. Nelson, "The Gram Matrix of the Tetrad Equation"

Builds on `ForcedTetrahedralFrame` (`M₁ = Mmat`, `MᵀM`, `MMᵀ`), on `HalfSpaceTwoBoundedRegions`
(Route 1) and on `TetradScheme` (Route 2: `P`, `η`, `IsLorentz`, the quarter turn `Rq`).

## How to referee this file
A Lean proof can only be wrong in its *statements*. Check these definitions against the paper:
* `M1 = Mmat` (Eq. (2)), `M2 = −M1`; `gram U W = Uᵀ W`; `G = gram M1 M1`; `J` the all-ones matrix.
* `Hhat`: `M1` with a row of ones on top.
* `omega a b c M = det(v_a, v_b, v_c)`.
* `corner v`: every entry `±1`; `IsSymA L`, `IsSymS L`: orthogonal maps permuting the corners of
  TetA, of the compound `S`.
* `Idx = Fin 4 × Fin 4 × Fin 4` indexes `Γ^λ_{μν}` as `(λ, μ, ν)`; `tau Γ (λ,μ,ν) = Γ (λ,ν,μ)`;
  `Pplus = ½(1 + τ)`; `torsion Γ = Γ − τΓ`.
* `compat g D`: `g_{λσ} D^σ_{μν} + g_{νσ} D^σ_{μλ} = 0`, the pointwise condition on the
  difference of two `g`-compatible connections.
* `gammaOf e de ω`, `frameTorsion e de ω`: the connection and torsion of Propositions 2 and 3,
  with `de μ = ∂_μ e` and `ω μ = ω_μ` at a point.
-/

open Matrix

namespace GramMatrixTetradEquation

open ForcedTetrahedralFrame (Mmat Mcol MMt MtM MtM_apply J)
open TetradScheme (P eta etaR IsLorentz Rq)

/-! ## Part I: the three Gram products -/

abbrev M1 : Matrix (Fin 3) (Fin 4) ℝ := Mmat
abbrev M2 : Matrix (Fin 3) (Fin 4) ℝ := -Mmat

/-- The Gram product `G_{UW} = UᵀW`. -/
def gram (U W : Matrix (Fin 3) (Fin 4) ℝ) : Matrix (Fin 4) (Fin 4) ℝ := Uᵀ * W

abbrev G : Matrix (Fin 4) (Fin 4) ℝ := gram M1 M1

/-- **Lemma 1 (root-blindness).** -/
theorem lemma1 : gram M2 M2 = gram M1 M1 := by simp [gram]

/-- **Lemma 2 (cross-coupling).** Same-root pairs give `G`, cross-root pairs `−G`, and each value
is unchanged when the two roots are exchanged. -/
theorem lemma2 :
    gram M1 M2 = -G ∧ gram M2 M1 = -G ∧ gram M2 M1 = (gram M1 M2)ᵀ ∧
      (∀ U W : Matrix (Fin 3) (Fin 4) ℝ, (U = M1 ∨ U = M2) → (W = M1 ∨ W = M2) →
        gram U W = (if U = W then G else -G)) := by
  have hne : M1 ≠ M2 := by
    intro h; have := congrFun (congrFun h 0) 0; simp [Mmat] at this; norm_num at this
  refine ⟨by simp [gram], by simp [gram], by simp [gram, transpose_mul], ?_⟩
  rintro U W (rfl | rfl) (rfl | rfl)
  · simp [gram]
  · rw [ite_eq_right_of_eq_false _ _ (eq_false hne)]; simp [gram]
  · rw [ite_eq_right_of_eq_false _ _ (eq_false (Ne.symm hne))]; simp [gram]
  · simp [gram]

/-- `M1` bordered by a row of ones. -/
def Hhat : Matrix (Fin 4) (Fin 4) ℝ :=
  !![1, 1, 1, 1; 1, 1, -1, -1; 1, -1, 1, -1; 1, -1, -1, 1]

lemma Hhat_rows (i : Fin 3) (a : Fin 4) : Hhat i.succ a = Mmat i a := by
  fin_cases i <;> fin_cases a <;> rfl

/-- **Lemma 3 (explicit Gram matrix).** `ĤĤᵀ = 4I`, hence `ĤᵀĤ = 4I`, `M1·1 = 0`,
`G = 4I − J`, `M1M1ᵀ = 4I₃`. -/
theorem lemma3 :
    Hhat * Hhatᵀ = (4 : ℝ) • 1 ∧ Hhatᵀ * Hhat = (4 : ℝ) • 1 ∧ M1 *ᵥ (fun _ => 1) = 0 ∧
      G = (4 : ℝ) • 1 - J 4 ∧ M1 * M1ᵀ = (4 : ℝ) • 1 := by
  have h1 : Hhat * Hhatᵀ = (4 : ℝ) • 1 := by
    ext i j; fin_cases i <;> fin_cases j <;> simp [Hhat, Matrix.mul_apply, Fin.sum_univ_four] <;>
      norm_num
  have h2 : Hhatᵀ * Hhat = (4 : ℝ) • 1 := by
    -- a square matrix with `ĤĤᵀ = 4I` has `Ĥ⁻¹ = ¼Ĥᵀ`
    have : Hhat * ((1 / 4 : ℝ) • Hhatᵀ) = 1 := by
      rw [Matrix.mul_smul, h1, smul_smul]; norm_num
    have h := mul_eq_one_comm.mp this
    rw [Matrix.smul_mul] at h
    have := congrArg ((4 : ℝ) • ·) h
    simpa [smul_smul] using this
  refine ⟨h1, h2, ?_, ?_, MMt⟩
  · funext i; fin_cases i <;> simp [Mmat, mulVec, dotProduct, Fin.sum_univ_four]
  · show Mmatᵀ * Mmat = _
    rw [MtM]; ext a b; by_cases h : a = b
    · subst h; simp [J]; norm_num
    · simp [J, h]

lemma G_eq : G = (4 : ℝ) • 1 - J 4 := lemma3.2.2.2.1

lemma J_sq : J 4 * J 4 = (4 : ℝ) • J 4 := by
  ext i j; simp [J, Matrix.mul_apply]

lemma G_mulVec (x : Fin 4 → ℝ) : G *ᵥ x = (4 : ℝ) • x - (∑ i, x i) • (fun _ => 1) := by
  rw [G_eq, sub_mulVec, smul_mulVec, one_mulVec]
  congr 1
  funext i; simp [J, mulVec, dotProduct]

/-- **Lemma 4 (eigenstructure).** `¼G` and `¼J` are complementary orthogonal projections;
`G` has eigenvalue `0` exactly on the constants (closure) and `4` exactly on `1^⊥`, which the rows
of `M1` span (`G M1ᵀ = 4 M1ᵀ`, rows independent); the cross-coupling has `0` and `−4`. -/
theorem lemma4 :
    ((1 / 4 : ℝ) • G) * ((1 / 4 : ℝ) • G) = (1 / 4 : ℝ) • G ∧
      ((1 / 4 : ℝ) • J 4) * ((1 / 4 : ℝ) • J 4) = (1 / 4 : ℝ) • J 4 ∧
      (1 / 4 : ℝ) • G + (1 / 4 : ℝ) • J 4 = 1 ∧
      ((1 / 4 : ℝ) • G) * ((1 / 4 : ℝ) • J 4) = 0 ∧
      Gᵀ = G ∧ (J 4)ᵀ = J 4 ∧
      (∀ x : Fin 4 → ℝ, G *ᵥ x = 0 ↔ ∀ i j, x i = x j) ∧
      (∀ x : Fin 4 → ℝ, G *ᵥ x = (4 : ℝ) • x ↔ ∑ i, x i = 0) ∧
      G * M1ᵀ = (4 : ℝ) • M1ᵀ ∧
      (∀ c : Fin 3 → ℝ, M1ᵀ *ᵥ c = 0 → c = 0) ∧
      (∀ x : Fin 4 → ℝ, gram M1 M2 *ᵥ x = -(G *ᵥ x)) := by
  have hJ := J_sq
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, fun x => ?_, fun x => ?_, ?_, fun c hc => ?_, fun x => ?_⟩
  · rw [G_eq, smul_mul_smul_comm, sub_mul, mul_sub, mul_sub, hJ]
    simp only [Matrix.smul_mul, Matrix.mul_smul, Matrix.one_mul, Matrix.mul_one, smul_smul]
    module
  · rw [smul_mul_smul_comm, hJ, smul_smul]; norm_num
  · rw [G_eq]; module
  · rw [G_eq, smul_mul_smul_comm, sub_mul, hJ, Matrix.smul_mul, Matrix.one_mul]; simp
  · simp [gram, transpose_mul]
  · ext i j; simp [J]
  · rw [G_mulVec]
    constructor
    · intro h i j
      have hi := congrFun h i; have hj := congrFun h j
      simp at hi hj; linarith
    · intro h
      funext i
      simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul, mul_one, Pi.zero_apply,
        Fin.sum_univ_four]
      rw [h 1 i, h 2 i, h 3 i, h 0 i]; ring
  · rw [G_mulVec]
    constructor
    · intro h
      have := congrFun h 0
      simp at this; linarith
    · intro h; rw [h]; simp
  · show Mmatᵀ * Mmat * Mmatᵀ = _
    rw [Matrix.mul_assoc, MMt, Matrix.mul_smul, Matrix.mul_one]
  · have := congrArg (Mmat *ᵥ ·) hc
    simp only [mulVec_mulVec, MMt, mulVec_zero, smul_mulVec, one_mulVec] at this
    funext i; have := congrFun this i; simp at this; exact this
  · simp [gram, Matrix.neg_mulVec, Matrix.mul_neg]

/-- **Lemma 5 (invariance and rigidity).** Orthogonal `Q` leaves all Gram products unchanged;
conversely `WᵀW = G` forces `W = QM1` for a unique orthogonal `Q`, namely `Q = ¼WM1ᵀ`;
for `W = M2`, `Q = −I`. -/
theorem lemma5 :
    (∀ Q : Matrix (Fin 3) (Fin 3) ℝ, Qᵀ * Q = 1 → ∀ U W, gram (Q * U) (Q * W) = gram U W) ∧
      (∀ W : Matrix (Fin 3) (Fin 4) ℝ, Wᵀ * W = G →
        ∃! Q : Matrix (Fin 3) (Fin 3) ℝ, Qᵀ * Q = 1 ∧ W = Q * M1) ∧
      (∀ W : Matrix (Fin 3) (Fin 4) ℝ, ∀ Q, W = Q * M1 → Q = (1 / 4 : ℝ) • (W * M1ᵀ)) ∧
      (∃! Q : Matrix (Fin 3) (Fin 3) ℝ, Qᵀ * Q = 1 ∧ M2 = Q * M1) ∧ M2 = (-1 : Matrix (Fin 3) (Fin 3) ℝ) * M1 := by
  have hQ : ∀ W : Matrix (Fin 3) (Fin 4) ℝ, ∀ Q, W = Q * M1 → Q = (1 / 4 : ℝ) • (W * M1ᵀ) := by
    intro W Q h
    rw [h, Matrix.mul_assoc, MMt, Matrix.mul_smul, Matrix.mul_one, smul_smul]; norm_num
  have rig : ∀ W : Matrix (Fin 3) (Fin 4) ℝ, Wᵀ * W = G →
      ∃! Q : Matrix (Fin 3) (Fin 3) ℝ, Qᵀ * Q = 1 ∧ W = Q * M1 := by
    intro W hW
    have quad : ∀ x y : Fin 4 → ℝ, (W *ᵥ x) ⬝ᵥ (W *ᵥ y) = x ⬝ᵥ ((Wᵀ * W) *ᵥ y) := by
      intro x y
      rw [← mulVec_mulVec, Matrix.dotProduct_mulVec x Wᵀ (W *ᵥ y), vecMul_transpose]
    -- `W 1 = 0`: `|W1|² = 1ᵀ G 1 = 0`
    have hG1 : G *ᵥ (fun _ => (1 : ℝ)) = 0 := (lemma4.2.2.2.2.2.2.1 _).mpr fun _ _ => rfl
    have hW1 : W *ᵥ (fun _ => (1 : ℝ)) = 0 := by
      have h0 := quad (fun _ => 1) (fun _ => 1)
      rw [hW, hG1, dotProduct_zero] at h0
      exact dotProduct_self_eq_zero.mp h0
    have hWJ : W * J 4 = 0 := by
      ext i j
      have := congrFun hW1 i
      simpa [J, Matrix.mul_apply, mulVec, dotProduct] using this
    have hI : (1 : Matrix (Fin 4) (Fin 4) ℝ) = (1 / 4 : ℝ) • (M1ᵀ * M1) + (1 / 4 : ℝ) • J 4 :=
      lemma4.2.2.1.symm
    have hWeq : W = ((1 / 4 : ℝ) • (W * M1ᵀ)) * M1 := by
      calc W = W * 1 := (Matrix.mul_one W).symm
        _ = _ := by
          rw [hI, Matrix.mul_add, Matrix.mul_smul, Matrix.mul_smul, hWJ, smul_zero, add_zero,
            Matrix.smul_mul, Matrix.mul_assoc]
    refine ⟨(1 / 4 : ℝ) • (W * M1ᵀ), ⟨?_, hWeq⟩, fun Q ⟨_, hQW⟩ => hQ W Q hQW⟩
    rw [transpose_smul, smul_mul_smul_comm, transpose_mul, transpose_transpose,
      show M1 * Wᵀ * (W * M1ᵀ) = M1 * (Wᵀ * W) * M1ᵀ by simp only [Matrix.mul_assoc], hW,
      show M1 * G * M1ᵀ = (M1 * M1ᵀ) * (M1 * M1ᵀ) by simp only [gram, Matrix.mul_assoc], MMt,
      smul_mul_smul_comm, Matrix.one_mul, smul_smul]
    norm_num
  refine ⟨fun Q hQ U W => ?_, rig, hQ, ?_, by simp⟩
  · simp only [gram, transpose_mul]
    rw [show Uᵀ * Qᵀ * (Q * W) = Uᵀ * (Qᵀ * Q) * W by simp only [Matrix.mul_assoc], hQ,
      Matrix.mul_one]
  · exact rig M2 (by show (-Mmat)ᵀ * -Mmat = Mmatᵀ * Mmat; simp)

/-- The orientation of legs `a, b, c`: `det(v_a, v_b, v_c)`. -/
def omega (a b c : Fin 4) (M : Matrix (Fin 3) (Fin 4) ℝ) : ℝ :=
  (Matrix.of fun i k => M i (![a, b, c] k)).det

/-- **Proposition 1 (orientation).** `ω_abc` is nonzero on `M1` for distinct legs, transforms by
`det Q` (so is `SO(3)`-invariant), and reverses between the roots. -/
theorem prop1 :
    (∀ a b c : Fin 4, a ≠ b → b ≠ c → a ≠ c → omega a b c M1 ≠ 0) ∧
      (∀ (Q : Matrix (Fin 3) (Fin 3) ℝ) M a b c, omega a b c (Q * M) = Q.det * omega a b c M) ∧
      (∀ (Q : Matrix (Fin 3) (Fin 3) ℝ) M a b c, Q.det = 1 → omega a b c (Q * M) = omega a b c M) ∧
      (∀ a b c, omega a b c M2 = -omega a b c M1) := by
  have hmul : ∀ (Q : Matrix (Fin 3) (Fin 3) ℝ) M a b c,
      omega a b c (Q * M) = Q.det * omega a b c M := by
    intro Q M a b c
    unfold omega
    rw [← det_mul]; congr 1
  refine ⟨fun a b c hab hbc hac => ?_, hmul, fun Q M a b c hQ => by rw [hmul, hQ, one_mul],
    fun a b c => ?_⟩
  · fin_cases a <;> fin_cases b <;> fin_cases c <;> simp at hab hbc hac <;>
      simp [omega, det_fin_three, Mmat] <;> norm_num
  · have : (Matrix.of fun i k => M2 i (![a, b, c] k)) =
        -(Matrix.of fun i k => M1 i (![a, b, c] k)) := by ext i k; simp
    rw [omega, this, det_neg]; simp [omega]; norm_num

/-! ## Part II: geometric identification -/

/-- A corner of the cube `{±1}³`. -/
def corner (v : Fin 3 → ℝ) : Prop := ∀ i, v i = 1 ∨ v i = -1

lemma hdot (a b : Fin 4) : Mcol a ⬝ᵥ Mcol b = if a = b then 3 else -1 := by
  rw [← MtM_apply, Matrix.mul_apply]; simp [Mcol, dotProduct]

lemma hdot_self (a : Fin 4) : Mcol a ⬝ᵥ Mcol a = 3 := by rw [hdot]; simp

lemma hdot_ne {a b : Fin 4} (h : a ≠ b) : Mcol a ⬝ᵥ Mcol b = -1 := by rw [hdot]; simp [h]

/-- **Theorem 1 (tetrahedra in the cube).** The columns of `M1` are exactly the corners with
`xyz = +1`, those of `M2` exactly the corners with `xyz = −1`; edges have squared length 8; each set
is centred at the origin; the two sets are disjoint. -/
theorem theorem1 :
    (∀ v, corner v → (v 0 * v 1 * v 2 = 1 ↔ ∃ a, v = Mcol a)) ∧
      (∀ v, corner v → (v 0 * v 1 * v 2 = -1 ↔ ∃ a, v = -Mcol a)) ∧
      (∀ a, corner (Mcol a) ∧ corner (-Mcol a)) ∧
      (∀ a b, a ≠ b → (Mcol a - Mcol b) ⬝ᵥ (Mcol a - Mcol b) = 8) ∧
      ∑ a, Mcol a = 0 ∧ (∀ a b, Mcol a ≠ -Mcol b) := by
  refine ⟨fun v hv => ?_, fun v hv => ?_, fun a => ?_, fun a b hab => ?_, ?_, fun a b h => ?_⟩
  · constructor
    · intro h
      refine ⟨if v 0 = 1 then (if v 1 = 1 then 0 else 1) else (if v 1 = 1 then 2 else 3), ?_⟩
      rcases hv 0 with h0 | h0 <;> rcases hv 1 with h1 | h1 <;> rcases hv 2 with h2 | h2 <;>
        rw [h0, h1, h2] at h <;> norm_num at h <;>
        funext i <;> fin_cases i <;> simp [Mcol, Mmat, h0, h1, h2] <;> norm_num
    · rintro ⟨a, rfl⟩; fin_cases a <;> simp [Mcol, Mmat]
  · constructor
    · intro h
      refine ⟨if v 0 = -1 then (if v 1 = -1 then 0 else 1) else (if v 1 = -1 then 2 else 3), ?_⟩
      rcases hv 0 with h0 | h0 <;> rcases hv 1 with h1 | h1 <;> rcases hv 2 with h2 | h2 <;>
        rw [h0, h1, h2] at h <;> norm_num at h <;>
        funext i <;> fin_cases i <;> simp [Mcol, Mmat, h0, h1, h2] <;> norm_num
    · rintro ⟨a, rfl⟩; fin_cases a <;> simp [Mcol, Mmat]
  · constructor <;> intro i <;> fin_cases a <;> fin_cases i <;> simp [Mcol, Mmat]
  · rw [sub_dotProduct, dotProduct_sub, dotProduct_sub, hdot_self, hdot_self, hdot_ne hab,
      hdot_ne (Ne.symm hab)]; norm_num
  · funext i; fin_cases i <;> simp [Mcol, Mmat, Fin.sum_univ_four]
  · have := congrArg (Mcol b ⬝ᵥ ·) h
    simp only [dotProduct_neg, hdot_self] at this
    by_cases hab : b = a
    · subst hab; rw [hdot_self] at this; norm_num at this
    · rw [hdot_ne hab] at this; norm_num at this

/-- Orthogonal maps permuting the corners of TetA. -/
def IsSymA (L : Matrix (Fin 3) (Fin 3) ℝ) : Prop := Lᵀ * L = 1 ∧ ∀ a, ∃ b, L *ᵥ Mcol a = Mcol b

/-- Orthogonal maps permuting the eight corners of the compound `S = [M1 | M2]`. -/
def IsSymS (L : Matrix (Fin 3) (Fin 3) ℝ) : Prop :=
  Lᵀ * L = 1 ∧ ∀ a, ∃ b, L *ᵥ Mcol a = Mcol b ∨ L *ᵥ Mcol a = -Mcol b

lemma col_mul (L : Matrix (Fin 3) (Fin 3) ℝ) (a : Fin 4) (i : Fin 3) :
    (L * Mmat) i a = (L *ᵥ Mcol a) i := by
  simp [Matrix.mul_apply, mulVec, dotProduct, Mcol]

/-- A linear map is fixed by what it does to the four legs (they span `ℝ³`). -/
lemma ext_cols {L L' : Matrix (Fin 3) (Fin 3) ℝ} (h : ∀ a, L *ᵥ Mcol a = L' *ᵥ Mcol a) :
    L = L' := by
  have hM : L * Mmat = L' * Mmat := by ext i a; rw [col_mul, col_mul, h]
  have := congrArg (· * Mmatᵀ) hM
  simpa only [Matrix.mul_assoc, MMt, Matrix.mul_smul, Matrix.mul_one,
    smul_right_inj (by norm_num : (4 : ℝ) ≠ 0)] using this

lemma orth_dot {L : Matrix (Fin 3) (Fin 3) ℝ} (hL : Lᵀ * L = 1) (x y : Fin 3 → ℝ) :
    (L *ᵥ x) ⬝ᵥ (L *ᵥ y) = x ⬝ᵥ y := by
  rw [Matrix.dotProduct_mulVec (L *ᵥ x) L y, ← vecMul_transpose, vecMul_vecMul, hL]; simp

lemma Mcol_injective : Function.Injective Mcol := by
  intro a b h
  by_contra hne
  have := hdot_ne hne
  rw [h, hdot_self] at this; norm_num at this

/-- Every permutation of the legs is realised by exactly one orthogonal map. -/
theorem realise_perm (σ : Equiv.Perm (Fin 4)) :
    ∃! L : Matrix (Fin 3) (Fin 3) ℝ, Lᵀ * L = 1 ∧ ∀ a, L *ᵥ Mcol a = Mcol (σ a) := by
  set W : Matrix (Fin 3) (Fin 4) ℝ := Matrix.of fun i a => Mmat i (σ a) with hWdef
  have hW : Wᵀ * W = G := by
    ext a b
    have e1 : (Wᵀ * W) a b = (Mmatᵀ * Mmat) (σ a) (σ b) := by
      simp [hWdef, Matrix.mul_apply]
    rw [e1]
    show _ = (Mmatᵀ * Mmat) a b
    rw [MtM_apply, MtM_apply]
    simp only [σ.injective.eq_iff]
  obtain ⟨Q, ⟨hQ, hWQ⟩, -⟩ := lemma5.2.1 W hW
  refine ⟨Q, ⟨hQ, fun a => ?_⟩, fun L ⟨_, hL⟩ => ext_cols fun a => ?_⟩
  · funext i
    rw [← col_mul, ← hWQ]; simp [hWdef, Mcol]
  · rw [hL a]; funext i; rw [← col_mul, ← hWQ]; simp [hWdef, Mcol]

/-- The permutation induced by a symmetry of TetA. -/
theorem induced_perm {L : Matrix (Fin 3) (Fin 3) ℝ} (hL : IsSymA L) :
    ∃ σ : Equiv.Perm (Fin 4), ∀ a, L *ᵥ Mcol a = Mcol (σ a) := by
  choose f hf using hL.2
  have hinj : Function.Injective f := by
    intro a b hab
    have : L *ᵥ Mcol a = L *ᵥ Mcol b := by rw [hf, hf, hab]
    have h2 := congrArg (Lᵀ *ᵥ ·) this
    simp only [mulVec_mulVec, hL.1, one_mulVec] at h2
    exact Mcol_injective h2
  exact ⟨Equiv.ofBijective f (Finite.injective_iff_bijective.mp hinj), hf⟩

/-- **Theorem 2, first part.** `Sym(TetA)` has order 24, acting on the legs as all of `S₄`. -/
theorem symA_card : Nat.card {L : Matrix (Fin 3) (Fin 3) ℝ // IsSymA L} = 24 := by
  choose F hF using fun σ => (realise_perm σ).exists
  have hinj : Function.Injective F := by
    intro σ τ h
    ext a
    have := (hF σ).2 a
    rw [h, (hF τ).2 a] at this
    exact congrArg Fin.val (Mcol_injective this).symm
  have hset : {L | IsSymA L} = Set.range F := by
    ext L
    simp only [Set.mem_ofPred_eq, Set.mem_range]
    constructor
    · intro hL
      obtain ⟨σ, hσ⟩ := induced_perm hL
      exact ⟨σ, ext_cols fun a => by rw [(hF σ).2, hσ]⟩
    · rintro ⟨σ, rfl⟩; exact ⟨(hF σ).1, fun a => ⟨σ a, (hF σ).2 a⟩⟩
  rw [show Nat.card {L : Matrix (Fin 3) (Fin 3) ℝ // IsSymA L} = Nat.card (Set.range F) by
    rw [← hset]; rfl, Nat.card_range_of_injective hinj, Nat.card_perm]
  simp [Nat.factorial]

lemma dot_signs (b c : Fin 4) : Mcol c ⬝ᵥ Mcol b ≠ 1 ∧ Mcol c ⬝ᵥ Mcol b ≠ -3 := by
  rw [hdot]; split_ifs <;> norm_num

/-- **Theorem 2.** `Sym(S) = Sym(TetA) × {I, −I}`: every symmetry of the compound is a symmetry of
TetA or minus one, never both; it has order 48; and each element outside `Sym(TetA)` carries TetA
onto TetB. -/
theorem theorem2 :
    (∀ L, IsSymS L ↔ IsSymA L ∨ IsSymA (-L)) ∧ (∀ L, ¬ (IsSymA L ∧ IsSymA (-L))) ∧
      Nat.card {L : Matrix (Fin 3) (Fin 3) ℝ // IsSymS L} = 48 ∧
      (∀ L, IsSymS L → ¬ IsSymA L → ∀ a, ∃ b, L *ᵥ Mcol a = -Mcol b) ∧
      (∀ L : Matrix (Fin 3) (Fin 3) ℝ, (-1) * L = L * (-1)) := by
  have excl : ∀ L, ¬ (IsSymA L ∧ IsSymA (-L)) := by
    rintro L ⟨⟨-, h1⟩, ⟨-, h2⟩⟩
    obtain ⟨b, hb⟩ := h1 0; obtain ⟨c, hc⟩ := h2 0
    rw [neg_mulVec, hb] at hc
    have := congrArg (Mcol c ⬝ᵥ ·) hc
    simp only [dotProduct_neg] at this
    rw [hdot_self c] at this
    exact (dot_signs b c).2 (by linarith)
  have key : ∀ L, IsSymS L ↔ IsSymA L ∨ IsSymA (-L) := by
    intro L
    constructor
    · rintro ⟨hL, h⟩
      have hneg : (-L)ᵀ * (-L) = 1 := by simp [hL]
      obtain ⟨b, hb | hb⟩ := h 0
      · left
        refine ⟨hL, fun a => ?_⟩
        obtain ⟨c, hc | hc⟩ := h a
        · exact ⟨c, hc⟩
        · exfalso
          by_cases ha : a = 0
          · subst ha; rw [hb] at hc
            have := congrArg (Mcol c ⬝ᵥ ·) hc
            simp only [dotProduct_neg] at this
            rw [hdot_self c] at this
            exact (dot_signs b c).2 (by linarith)
          · have e := orth_dot hL (Mcol a) (Mcol 0)
            rw [hc, hb, hdot_ne ha, neg_dotProduct] at e
            exact (dot_signs b c).1 (by linarith)
      · right
        refine ⟨hneg, fun a => ?_⟩
        obtain ⟨c, hc | hc⟩ := h a
        · exfalso
          by_cases ha : a = 0
          · subst ha; rw [hb] at hc
            have := congrArg (Mcol c ⬝ᵥ ·) hc
            simp only [dotProduct_neg] at this
            rw [hdot_self c] at this
            exact (dot_signs b c).2 (by linarith)
          · have e := orth_dot hL (Mcol a) (Mcol 0)
            rw [hc, hb, hdot_ne ha, dotProduct_neg] at e
            exact (dot_signs b c).1 (by linarith)
        · exact ⟨c, by rw [neg_mulVec, hc, neg_neg]⟩
    · rintro (⟨hL, h⟩ | ⟨hL, h⟩)
      · exact ⟨hL, fun a => (h a).imp fun b hb => Or.inl hb⟩
      · refine ⟨by simpa using hL, fun a => ?_⟩
        obtain ⟨b, hb⟩ := h a
        exact ⟨b, Or.inr (by rw [neg_mulVec] at hb; rw [← hb, neg_neg])⟩
  refine ⟨key, excl, ?_, fun L hS hA a => ?_, fun L => by simp⟩
  · have hA : Set.Finite {L : Matrix (Fin 3) (Fin 3) ℝ | IsSymA L} := by
      have : Finite {L : Matrix (Fin 3) (Fin 3) ℝ // IsSymA L} :=
        Nat.finite_of_card_ne_zero (by rw [symA_card]; norm_num)
      exact Set.toFinite _
    have hset : {L | IsSymS L} = {L | IsSymA L} ∪ (fun L => -L) '' {L | IsSymA L} := by
      ext L
      simp only [Set.mem_ofPred_eq, Set.mem_union, Set.mem_image, key]
      constructor
      · rintro (h | h)
        · exact Or.inl h
        · exact Or.inr ⟨-L, h, neg_neg L⟩
      · rintro (h | ⟨L', h, rfl⟩)
        · exact Or.inl h
        · exact Or.inr (by simpa using h)
    have hdisj : Disjoint {L : Matrix (Fin 3) (Fin 3) ℝ | IsSymA L}
        ((fun L => -L) '' {L | IsSymA L}) := by
      rw [Set.disjoint_left]
      rintro L hL ⟨L', hL', rfl⟩
      exact excl L' ⟨hL', by simpa using hL⟩
    have h24 : Set.ncard {L : Matrix (Fin 3) (Fin 3) ℝ | IsSymA L} = 24 := symA_card
    show Set.ncard {L : Matrix (Fin 3) (Fin 3) ℝ | IsSymS L} = 48
    rw [hset, Set.ncard_union_eq hdisj hA (hA.image _),
      Set.ncard_image_of_injective _ neg_injective, h24]
  · rcases (key L).mp hS with h | h
    · exact absurd h hA
    · obtain ⟨b, hb⟩ := h.2 a
      exact ⟨b, by rw [neg_mulVec] at hb; rw [← hb, neg_neg]⟩

/-- **Half of the exchanging elements are rotations**: the quarter turn of `TetradScheme` is a
symmetry of the compound outside `Sym(TetA)` with determinant `+1`. -/
theorem quarter_turn_exchanges : IsSymS Rq ∧ ¬ IsSymA Rq ∧ Rq.det = 1 := by
  have hq := TetradScheme.same_shape
  have hcol : ∀ a, Rq *ᵥ Mcol a = -Mcol ((![1, 3, 0, 2] : Fin 4 → Fin 4) a) := by
    intro a; funext i
    fin_cases a <;> fin_cases i <;> simp [Rq, Mcol, Mmat, mulVec, dotProduct, Fin.sum_univ_three]
  have hA : IsSymA (-Rq) := ⟨by simpa using hq.1, fun a => ⟨_, by rw [neg_mulVec, hcol, neg_neg]⟩⟩
  have hS : IsSymS Rq := (theorem2.1 Rq).mpr (Or.inr hA)
  exact ⟨hS, fun h => theorem2.2.1 Rq ⟨h, hA⟩, hq.2.1⟩

/-! ## Part III: the index grid -/

/-- An index `(λ, μ, ν)` of `Γ^λ_{μν}`. -/
abbrev Idx := Fin 4 × Fin 4 × Fin 4

/-- Exchange of the lower indices. -/
def swapIdx (t : Idx) : Idx := (t.1, t.2.2, t.2.1)

/-- `τ`: `(τΓ)^λ_{μν} = Γ^λ_{νμ}`. -/
def tau : (Idx → ℝ) →ₗ[ℝ] (Idx → ℝ) := LinearMap.funLeft ℝ ℝ swapIdx

/-- `Π₊ = ½(1 + τ)`. -/
noncomputable def Pplus : (Idx → ℝ) →ₗ[ℝ] (Idx → ℝ) := (1 / 2 : ℝ) • (LinearMap.id + tau)

/-- The torsion `T^λ_{μν} = Γ^λ_{μν} − Γ^λ_{νμ}`. -/
def torsion : (Idx → ℝ) →ₗ[ℝ] (Idx → ℝ) := LinearMap.id - tau

/-- The `τ`-odd part. -/
def oddPart : Submodule ℝ (Idx → ℝ) := LinearMap.ker (LinearMap.id + tau)

lemma tau_apply (Γ : Idx → ℝ) (t : Idx) : tau Γ t = Γ (swapIdx t) := rfl

lemma swap_swap (t : Idx) : swapIdx (swapIdx t) = t := rfl

lemma mem_oddPart (Γ : Idx → ℝ) : Γ ∈ oddPart ↔ ∀ t, Γ (swapIdx t) = -Γ t := by
  simp only [oddPart, LinearMap.mem_ker, LinearMap.add_apply, LinearMap.id_apply]
  constructor
  · intro h t; have := congrFun h t; simp [tau_apply] at this; linarith
  · intro h; funext t; simp [tau_apply, h]

/-- **The grid (Eq. (6)).** `24 + 16 + 24 = 64`: per slice 6 strictly upper, 4 diagonal, 6 strictly
lower entries. -/
theorem grid :
    (Finset.univ.filter fun t : Idx => t.2.1 < t.2.2).card = 24 ∧
      (Finset.univ.filter fun t : Idx => t.2.1 = t.2.2).card = 16 ∧
      (Finset.univ.filter fun t : Idx => t.2.2 < t.2.1).card = 24 ∧
      Fintype.card Idx = 64 := by
  refine ⟨by decide, by decide, by decide, by simp⟩

/-- `τ`-odd tensors are determined by their strictly upper entries. -/
noncomputable def oddEquiv : oddPart ≃ₗ[ℝ] ({t : Idx // t.2.1 < t.2.2} → ℝ) := by
  refine LinearEquiv.ofBijective
    ((LinearMap.funLeft ℝ ℝ (Subtype.val : {t : Idx // t.2.1 < t.2.2} → Idx)).comp
      oddPart.subtype) ⟨?_, ?_⟩
  · intro x y hxy
    have hx := (mem_oddPart x).mp x.2
    have hy := (mem_oddPart y).mp y.2
    ext t
    have hU : ∀ u : {t : Idx // t.2.1 < t.2.2}, (x : Idx → ℝ) u = (y : Idx → ℝ) u :=
      fun u => congrFun hxy u
    rcases lt_trichotomy t.2.1 t.2.2 with h | h | h
    · exact hU ⟨t, h⟩
    · have e : swapIdx t = t := by
        obtain ⟨l, m, n⟩ := t; simp only at h; subst h; rfl
      have h1 := hx t; have h2 := hy t; rw [e] at h1 h2; linarith
    · have := hU ⟨swapIdx t, h⟩
      have h1 := hx t; have h2 := hy t
      simp only at this; linarith
  · intro f
    let Γ : Idx → ℝ := fun t =>
      if h : t.2.1 < t.2.2 then f ⟨t, h⟩ else if h' : t.2.2 < t.2.1 then -f ⟨swapIdx t, h'⟩ else 0
    have hΓ : Γ ∈ oddPart := by
      rw [mem_oddPart]
      intro t
      obtain ⟨l, m, n⟩ := t
      rcases lt_trichotomy m n with h | h | h
      · simp [Γ, swapIdx, h, not_lt.mpr h.le]
      · subst h; simp [Γ, swapIdx]
      · simp [Γ, swapIdx, h, not_lt.mpr h.le]
    refine ⟨⟨Γ, hΓ⟩, ?_⟩
    funext u
    simp [Γ, u.2]

/-- **Lemma 6 (the exchange split).** `τ² = 1`; `τ` fixes the diagonal and exchanges the triangles;
`Π₊` is a projection with range the `τ`-even tensors (rank 40) and kernel the `τ`-odd tensors
(dimension 24), which are exactly the torsions. -/
theorem lemma6 :
    tau ∘ₗ tau = LinearMap.id ∧
      (∀ Γ t, t.2.1 = t.2.2 → tau Γ t = Γ t) ∧
      (∀ t : Idx, t.2.1 < t.2.2 ↔ (swapIdx t).2.2 < (swapIdx t).2.1) ∧
      Pplus ∘ₗ Pplus = Pplus ∧
      (∀ Γ, Γ ∈ LinearMap.range Pplus ↔ tau Γ = Γ) ∧
      LinearMap.ker Pplus = oddPart ∧
      LinearMap.range torsion = oddPart ∧
      Module.finrank ℝ (LinearMap.ker Pplus) = 24 ∧
      Module.finrank ℝ (LinearMap.range Pplus) = 40 := by
  have htt : tau ∘ₗ tau = LinearMap.id := by ext Γ t; rfl
  have htt' : ∀ Γ, tau (tau Γ) = Γ := fun Γ => by funext t; rfl
  have hPP : Pplus ∘ₗ Pplus = Pplus := by
    ext Γ t
    simp only [Pplus, LinearMap.comp_apply, LinearMap.smul_apply, LinearMap.add_apply,
      LinearMap.id_apply, map_smul, map_add, htt', Pi.smul_apply, Pi.add_apply, smul_eq_mul]
    ring
  have hker : LinearMap.ker Pplus = oddPart := by
    ext Γ
    simp only [LinearMap.mem_ker, Pplus, oddPart, LinearMap.smul_apply]
    constructor
    · intro h; have := congrArg ((2 : ℝ) • ·) h; simpa [smul_smul] using this
    · intro h; rw [h]; simp
  have hdim : Module.finrank ℝ oddPart = 24 := by
    rw [oddEquiv.finrank_eq, Module.finrank_fintype_fun_eq_card]; decide
  refine ⟨htt, fun Γ t h => ?_, fun t => Iff.rfl, hPP, fun Γ => ?_, hker, ?_, ?_, ?_⟩
  · obtain ⟨l, m, n⟩ := t; simp only at h; subst h; rfl
  · constructor
    · rintro ⟨Δ, rfl⟩
      funext t
      simp only [Pplus, LinearMap.smul_apply, LinearMap.add_apply, LinearMap.id_apply, map_smul,
        map_add, htt', Pi.smul_apply, Pi.add_apply]
      ring
    · intro h
      exact ⟨Γ, by simp only [Pplus, LinearMap.smul_apply, LinearMap.add_apply,
        LinearMap.id_apply, h]; rw [← two_smul ℝ Γ, smul_smul]; norm_num⟩
  · ext Γ
    simp only [LinearMap.mem_range, oddPart, LinearMap.mem_ker, torsion]
    constructor
    · rintro ⟨Δ, rfl⟩; simp [htt']
    · intro h
      refine ⟨(1 / 2 : ℝ) • Γ, ?_⟩
      have : tau Γ = -Γ := by
        have := congrArg (fun x => x - Γ) h; simpa using this
      simp [this, smul_smul, ← two_smul ℝ Γ]
  · rw [hker, hdim]
  · have h := LinearMap.finrank_range_add_finrank_ker Pplus
    rw [hker, hdim, Module.finrank_fintype_fun_eq_card] at h
    simp at h; omega

/-- **Relabelling** the coordinates by `π` commutes with `τ`; reversing them carries every upper
entry into the lower triangle. The torsion of anything symmetric in the lower indices (such as the
inhomogeneous term in the transformation of `Γ`) vanishes. -/
theorem cautions :
    (∀ (π : Equiv.Perm (Fin 4)) (Γ : Idx → ℝ),
      tau (fun t => Γ (π t.1, π t.2.1, π t.2.2)) = fun t => tau Γ (π t.1, π t.2.1, π t.2.2)) ∧
      (∀ t : Idx, t.2.1 < t.2.2 → (Fin.rev t.2.2) < (Fin.rev t.2.1)) ∧
      (∀ Γ, tau Γ = Γ → torsion Γ = 0) := by
  refine ⟨fun π Γ => rfl, fun t h => Fin.rev_lt_rev.mpr h, fun Γ h => ?_⟩
  simp [torsion, h]

/-! ## Part IV: the torsion-free projection -/

/-- **Theorem 3 (i).** `T = 0` exactly on the image of `Π₊`; `Π₊` is not injective. -/
theorem theorem3_i :
    (∀ Γ, torsion Γ = 0 ↔ Γ ∈ LinearMap.range Pplus) ∧ ¬ Function.Injective Pplus ∧
      (16 + 24 = 40 ∧ (40 : ℕ) ≠ 64 ∧ 24 + 16 + 24 = 64) := by
  obtain ⟨-, -, -, -, hrange, hker, -, hk, -⟩ := lemma6
  refine ⟨fun Γ => ?_, fun hinj => ?_, by norm_num⟩
  · rw [hrange]
    simp only [torsion, LinearMap.sub_apply, LinearMap.id_apply, sub_eq_zero]
    exact eq_comm
  · have : LinearMap.ker Pplus = ⊥ := LinearMap.ker_eq_bot.mpr hinj
    rw [this, finrank_bot] at hk; norm_num at hk

/-- Lowering the first index with `g`. -/
def lower (g : Matrix (Fin 4) (Fin 4) ℝ) : (Idx → ℝ) →ₗ[ℝ] (Idx → ℝ) where
  toFun D t := ∑ s, g t.1 s * D (s, t.2.1, t.2.2)
  map_add' D E := by funext t; simp [mul_add, Finset.sum_add_distrib]
  map_smul' c D := by
    funext t
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply, Finset.mul_sum]
    exact Finset.sum_congr rfl fun x _ => by ring

lemma lower_lower (g h : Matrix (Fin 4) (Fin 4) ℝ) (D : Idx → ℝ) :
    lower g (lower h D) = lower (g * h) D := by
  funext t
  simp only [lower, LinearMap.coe_mk, AddHom.coe_mk, Matrix.mul_apply, Finset.mul_sum,
    Finset.sum_mul]
  rw [Finset.sum_comm]; congr 1; funext s; congr 1; funext r; ring

lemma lower_one (D : Idx → ℝ) : lower 1 D = D := by
  funext t; simp [lower, Matrix.one_apply]

lemma lower_torsion (g : Matrix (Fin 4) (Fin 4) ℝ) (D : Idx → ℝ) :
    lower g (torsion D) = torsion (lower g D) := by
  funext t; simp [lower, torsion, tau_apply, swapIdx, mul_sub, Finset.sum_sub_distrib]

/-- The pointwise condition on the difference `D` of two `g`-compatible connections:
`g_{λσ}D^σ_{μν} + g_{νσ}D^σ_{μλ} = 0`. -/
def compat (g : Matrix (Fin 4) (Fin 4) ℝ) : Submodule ℝ (Idx → ℝ) where
  carrier := {D | ∀ l m n, lower g D (l, m, n) + lower g D (n, m, l) = 0}
  add_mem' := by
    intro D E hD hE l m n
    simp only [Set.mem_ofPred_eq, map_add, Pi.add_apply] at *
    linarith [hD l m n, hE l m n]
  zero_mem' := by simp
  smul_mem' := by
    intro c D hD l m n
    simp only [Set.mem_ofPred_eq, map_smul, Pi.smul_apply, smul_eq_mul] at *
    rw [← mul_add, hD l m n, mul_zero]

/-- A tensor antisymmetric in slots 1, 3 and symmetric in slots 2, 3 vanishes. -/
lemma sym_antisym_zero (Δ : Idx → ℝ) (ha : ∀ l m n, Δ (l, m, n) = -Δ (n, m, l))
    (hs : ∀ l m n, Δ (l, m, n) = Δ (l, n, m)) : Δ = 0 := by
  funext ⟨l, m, n⟩
  have e1 := hs l m n; have e2 := ha l n m; have e3 := hs m n l
  have e4 := ha m l n; have e5 := hs n l m; have e6 := ha n m l
  simp only [Pi.zero_apply]
  linarith

/-- **Theorem 3 (ii).** For any invertible `g`, the torsion map is a bijection from the differences
of `g`-compatible connections onto the torsions (the `τ`-odd tensors); both spaces are
24-dimensional. The inverse is the contorsion. -/
theorem theorem3_ii (g gi : Matrix (Fin 4) (Fin 4) ℝ) (hg : g * gi = 1) (hg' : gi * g = 1) :
    (∀ D ∈ compat g, torsion D = 0 → D = 0) ∧
      (∀ T ∈ oddPart, ∃ D ∈ compat g, torsion D = T) ∧
      (∀ D, torsion D ∈ oddPart) ∧
      Module.finrank ℝ (compat g) = 24 := by
  have hlow : ∀ D, lower gi (lower g D) = D := fun D => by rw [lower_lower, hg', lower_one]
  have hlow' : ∀ D, lower g (lower gi D) = D := fun D => by rw [lower_lower, hg, lower_one]
  have hodd : ∀ D, torsion D ∈ oddPart := by
    intro D; rw [mem_oddPart]; intro t
    simp [torsion, tau_apply, swap_swap]
  have inj : ∀ D ∈ compat g, torsion D = 0 → D = 0 := by
    intro D hD hT
    have hL : lower g D = 0 := by
      apply sym_antisym_zero
      · intro l m n; have := hD l m n; linarith
      · intro l m n
        have := congrFun (congrArg (lower g) hT) (l, m, n)
        rw [lower_torsion, map_zero] at this
        simp [torsion, tau_apply, swapIdx] at this; linarith
    rw [← hlow D, hL, map_zero]
  have surj : ∀ T ∈ oddPart, ∃ D ∈ compat g, torsion D = T := by
    intro T hT
    set L := lower g T with hLdef
    have hLodd : ∀ l m n, L (l, m, n) = -L (l, n, m) := by
      intro l m n
      have := (mem_oddPart T).mp hT
      simp only [hLdef, lower, LinearMap.coe_mk, AddHom.coe_mk]
      rw [← Finset.sum_neg_distrib]; congr 1; funext s
      have := this (s, n, m); simp [swapIdx] at this; rw [this]; ring
    -- the contorsion
    let Δ : Idx → ℝ := fun t =>
      (1 / 2) * (L (t.1, t.2.1, t.2.2) + L (t.2.2, t.1, t.2.1) + L (t.2.1, t.1, t.2.2))
    refine ⟨lower gi Δ, ?_, ?_⟩
    · intro l m n
      rw [hlow']
      simp only [Δ]
      linarith [hLodd l m n, hLodd n l m, hLodd m l n, hLodd m n l, hLodd l n m, hLodd n m l]
    · have h1 : lower g (torsion (lower gi Δ)) = lower g T := by
        rw [lower_torsion, hlow']
        funext ⟨l, m, n⟩
        simp only [torsion, LinearMap.sub_apply, LinearMap.id_apply, tau_apply, swapIdx,
          Pi.sub_apply, Δ]
        linarith [hLodd l m n, hLodd n l m, hLodd m l n, hLodd m n l, hLodd l n m, hLodd n m l]
      have := congrArg (lower gi) h1
      rwa [hlow, hlow] at this
  refine ⟨inj, surj, hodd, ?_⟩
  -- `compat g ≃ oddPart` through the torsion map
  have e : compat g ≃ₗ[ℝ] oddPart := by
    refine LinearEquiv.ofBijective
      ((torsion.comp (compat g).subtype).codRestrict oddPart fun D => hodd D) ⟨?_, ?_⟩
    · intro x y hxy
      have h : torsion (x : Idx → ℝ) = torsion y := congrArg Subtype.val hxy
      have := inj (x - y) ((compat g).sub_mem x.2 y.2) (by rw [map_sub, h, sub_self])
      exact Subtype.ext (sub_eq_zero.mp this)
    · intro T
      obtain ⟨D, hD, hDT⟩ := surj T T.2
      exact ⟨⟨D, hD⟩, Subtype.ext hDT⟩
  rw [e.finrank_eq, ← lemma6.2.2.2.2.2.1, lemma6.2.2.2.2.2.2.2.1]

/-- **Theorem 3 (iii).** Two `g`-compatible connections with the same torsion are equal; a
torsion-free one is unique (the Levi-Civita connection), and `g` is the same on both roots. -/
theorem theorem3_iii (g gi : Matrix (Fin 4) (Fin 4) ℝ) (hg : g * gi = 1) (hg' : gi * g = 1)
    (Γ₁ Γ₂ : Idx → ℝ) (h : Γ₁ - Γ₂ ∈ compat g) (hT : torsion Γ₁ = torsion Γ₂) : Γ₁ = Γ₂ := by
  have := (theorem3_ii g gi hg hg').1 _ h (by rw [map_sub, hT, sub_self])
  exact sub_eq_zero.mp this

/-- The connection `Γ^λ_{μν} = (e⁻¹)^λ_a (∂_μ e^a_ν + ω^a_{μb} e^b_ν)` at a point. -/
noncomputable def gammaOf (e : Matrix (Fin 4) (Fin 4) ℝ) (de ω : Fin 4 → Matrix (Fin 4) (Fin 4) ℝ) :
    Idx → ℝ := fun t => (e⁻¹ * (de t.2.1 + ω t.2.1 * e)) t.1 t.2.2

/-- `ω` is a Lorentz connection: `η ω_μ` antisymmetric. -/
def IsLorentzConn (ω : Fin 4 → Matrix (Fin 4) (Fin 4) ℝ) : Prop :=
  ∀ m, (eta * ω m)ᵀ = -(eta * ω m)

lemma PP : P * P = 1 := by ext i j; fin_cases i <;> fin_cases j <;> simp [P]

lemma Peta : P * eta = eta * P := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [P, etaR]

lemma PT_eq : Pᵀ = P := by simp [P]

/-- **Proposition 2 (how a connection follows the root).** (a) Carrying `ω` with the frame,
`(e, ω) ↦ (Pe, PωP)`, keeps `ω` Lorentz and leaves `Γ` (hence its torsion) unchanged.
(b) With the same `ω` on both roots, the torsions can differ. -/
theorem prop2 :
    (∀ (e : Matrix (Fin 4) (Fin 4) ℝ) (de ω : Fin 4 → Matrix (Fin 4) (Fin 4) ℝ),
      IsUnit e.det → IsLorentzConn ω →
        IsLorentzConn (fun m => P * ω m * P) ∧
        gammaOf (P * e) (fun m => P * de m) (fun m => P * ω m * P) = gammaOf e de ω) ∧
      ∃ ω : Fin 4 → Matrix (Fin 4) (Fin 4) ℝ, IsLorentzConn ω ∧
        gammaOf 1 (fun _ => 0) ω ∈ compat eta ∧ gammaOf (P * 1) (fun _ => 0) ω ∈ compat eta ∧
        torsion (gammaOf (P * 1) (fun _ => 0) ω) ≠ torsion (gammaOf 1 (fun _ => 0) ω) := by
  refine ⟨fun e de ω he hω => ⟨fun m => ?_, ?_⟩, ?_⟩
  · have : eta * (P * ω m * P) = P * (eta * ω m) * P := by
      rw [← Matrix.mul_assoc, ← Matrix.mul_assoc, ← Peta, Matrix.mul_assoc P eta]
    rw [this, transpose_mul, transpose_mul, PT_eq, hω m]
    simp [Matrix.mul_assoc]
  · have hPinv : P⁻¹ = P := inv_eq_left_inv PP
    have hinv : (P * e)⁻¹ = e⁻¹ * P := by
      rw [Matrix.mul_inv_rev, hPinv]
    have key : ∀ m, e⁻¹ * P * (P * de m + P * ω m * P * (P * e)) = e⁻¹ * (de m + ω m * e) := by
      intro m
      have h1 : P * (P * de m) = de m := by rw [← Matrix.mul_assoc, PP, Matrix.one_mul]
      have h2 : P * (P * ω m * P * (P * e)) = ω m * e := by
        calc _ = (P * P) * ω m * (P * P) * e := by simp only [Matrix.mul_assoc]
          _ = _ := by rw [PP, Matrix.one_mul, Matrix.mul_one]
      rw [Matrix.mul_assoc, Matrix.mul_add, h1, h2]
    funext t
    simp only [gammaOf, hinv, key]
  · -- a boost generator in the 0–1 plane
    let B : Matrix (Fin 4) (Fin 4) ℝ := !![0, 1, 0, 0; 1, 0, 0, 0; 0, 0, 0, 0; 0, 0, 0, 0]
    have hP1 : (P * 1)⁻¹ = P := by rw [Matrix.mul_one]; exact inv_eq_left_inv PP
    refine ⟨fun m => if m = 1 then B else 0, fun m => ?_, ?_, ?_, fun h => ?_⟩
    · by_cases hm : m = 1
      · simp only [hm, ite_true]
        ext i j; fin_cases i <;> fin_cases j <;> simp [B, etaR, Matrix.mul_apply, Fin.sum_univ_four]
      · simp [hm]
    · intro l m n
      simp only [lower, LinearMap.coe_mk, AddHom.coe_mk, gammaOf, inv_one, Matrix.one_mul,
        zero_add, Matrix.mul_one, Fin.sum_univ_four]
      fin_cases l <;> fin_cases m <;> fin_cases n <;> simp [B, etaR]
    · intro l m n
      simp only [lower, LinearMap.coe_mk, AddHom.coe_mk, gammaOf, hP1, zero_add, Fin.sum_univ_four]
      fin_cases l <;> fin_cases m <;> fin_cases n <;>
        simp [B, P, etaR, Matrix.mul_apply, Fin.sum_univ_four, vecMul_diagonal]
    · have v1 : gammaOf (P * 1) (fun _ => 0) (fun m => if m = 1 then B else 0) (1, 1, 0) = -1 := by
        simp only [gammaOf, hP1]; simp [B, P, Matrix.mul_apply, Fin.sum_univ_four, vecMul_diagonal]
      have v2 : gammaOf (P * 1) (fun _ => 0) (fun m => if m = 1 then B else 0) (1, 0, 1) = 0 := by
        simp only [gammaOf, hP1]; simp [B, P, Matrix.mul_apply]
      have v3 : gammaOf 1 (fun _ => 0) (fun m => if m = 1 then B else 0) (1, 1, 0) = 1 := by
        simp only [gammaOf, inv_one]; simp [B, Matrix.mul_apply, Fin.sum_univ_four]
      have v4 : gammaOf 1 (fun _ => 0) (fun m => if m = 1 then B else 0) (1, 0, 1) = 0 := by
        simp only [gammaOf, inv_one]; simp [B, Matrix.mul_apply]
      have := congrFun h (1, 1, 0)
      simp only [torsion, LinearMap.sub_apply, LinearMap.id_apply, Pi.sub_apply, tau_apply,
        swapIdx] at this
      rw [v1, v2, v3, v4] at this
      norm_num at this

/-- The frame torsion `T^a_{μν} = ∂_μ e^a_ν − ∂_ν e^a_μ + ω^a_{μb} e^b_ν − ω^a_{νb} e^b_μ`. -/
def frameTorsion (e : Matrix (Fin 4) (Fin 4) ℝ) (de ω : Fin 4 → Matrix (Fin 4) (Fin 4) ℝ) :
    Idx → ℝ := fun t => (de t.2.1 + ω t.2.1 * e) t.1 t.2.2 - (de t.2.2 + ω t.2.2 * e) t.1 t.2.1

/-- The Levi-Civita symbol `ε_{abcd}`, as `∏_{i<j} sgn(x_j − x_i)`. -/
def levi (a b c d : Fin 4) : ℤ :=
  Int.sign (((b : ℤ) - a) * ((c : ℤ) - a) * ((d : ℤ) - a) * ((c : ℤ) - b) * ((d : ℤ) - b) *
    ((d : ℤ) - c))

/-- `levi` is the Levi-Civita symbol: normalised and totally antisymmetric. -/
theorem levi_spec :
    levi 0 1 2 3 = 1 ∧ (∀ a b c d, levi b a c d = -levi a b c d) ∧
      (∀ a b c d, levi a c b d = -levi a b c d) ∧ (∀ a b c d, levi a b d c = -levi a b c d) := by
  refine ⟨by decide, ?_, ?_, ?_⟩ <;> decide

/-- The dual `(⋆T)^λ_{αβ} = ½ ε_{αβ}{}^{μν} T^λ_{μν}`, with `ε = vol · levi`, indices raised by `gi`. -/
noncomputable def dualT (vol : ℝ) (gi : Matrix (Fin 4) (Fin 4) ℝ) (T : Idx → ℝ) : Idx → ℝ := fun t =>
  (1 / 2) * ∑ μ, ∑ ν, ∑ ρ, ∑ σ,
    vol * (levi t.2.1 t.2.2 ρ σ : ℝ) * gi ρ μ * gi σ ν * T (t.1, μ, ν)

/-- The axial vector `A^σ ∝ ε^{σλμν} T_{λμν}` (first index of `T` lowered by `g`). -/
noncomputable def axial (vol : ℝ) (gi g : Matrix (Fin 4) (Fin 4) ℝ) (T : Idx → ℝ) : Fin 4 → ℝ := fun s =>
  ∑ α, ∑ β, ∑ γ, ∑ δ, ∑ l, ∑ m, ∑ n,
    vol * (levi α β γ δ : ℝ) * gi s α * gi β l * gi γ m * gi δ n * lower g T (l, m, n)

/-- **Proposition 3 (how the torsion carries the root).**
(i) The frame torsion of `(Pe, P∂e, PωP)` is `P` times that of `(e, ∂e, ω)`, and its coordinate
form `e⁻¹T` is the same on both roots (and is the torsion of `Γ`).
(ii) The volume `det e` reverses, so the dual and the axial vector reverse; for `g = η` and
`vol ≠ 0`, the dual is injective on torsions.
(iii) The totally antisymmetric part of `Γ` is half that of `T`; the torsion-free part has none. -/
theorem prop3 :
    (∀ (e : Matrix (Fin 4) (Fin 4) ℝ) (de ω : Fin 4 → Matrix (Fin 4) (Fin 4) ℝ),
      (∀ t, frameTorsion (P * e) (fun m => P * de m) (fun m => P * ω m * P) t =
        ∑ b, P t.1 b * frameTorsion e de ω (b, t.2.1, t.2.2)) ∧
      (IsUnit e.det → lower (P * e)⁻¹ (frameTorsion (P * e) (fun m => P * de m)
          (fun m => P * ω m * P)) = lower e⁻¹ (frameTorsion e de ω)) ∧
      lower e⁻¹ (frameTorsion e de ω) = torsion (gammaOf e de ω)) ∧
      (∀ e : Matrix (Fin 4) (Fin 4) ℝ, (P * e).det = -e.det) ∧
      (∀ vol gi T, dualT (-vol) gi T = -dualT vol gi T) ∧
      (∀ vol gi g T, axial (-vol) gi g T = -axial vol gi g T) ∧
      (∀ vol T, vol ≠ 0 → T ∈ oddPart → dualT vol eta T = 0 → T = 0) ∧
      (∀ (g : Matrix (Fin 4) (Fin 4) ℝ) (Γ : Idx → ℝ) l m n,
        let alt := fun X : Idx → ℝ => X (l, m, n) + X (m, n, l) + X (n, l, m) - X (l, n, m) -
          X (m, l, n) - X (n, m, l)
        alt (lower g (torsion Γ)) = 2 * alt (lower g Γ) ∧ alt (lower g (Pplus Γ)) = 0) := by
  have key2 : ∀ (e : Matrix (Fin 4) (Fin 4) ℝ) (de ω : Fin 4 → Matrix (Fin 4) (Fin 4) ℝ) m,
      P * de m + P * ω m * P * (P * e) = P * (de m + ω m * e) := by
    intro e de ω m
    rw [Matrix.mul_add]; congr 1
    calc P * ω m * P * (P * e) = P * ω m * (P * P) * e := by simp only [Matrix.mul_assoc]
      _ = _ := by rw [PP, Matrix.mul_one, Matrix.mul_assoc]
  have hft : ∀ (e : Matrix (Fin 4) (Fin 4) ℝ) (de ω : Fin 4 → Matrix (Fin 4) (Fin 4) ℝ) t,
      frameTorsion (P * e) (fun m => P * de m) (fun m => P * ω m * P) t =
        ∑ b, P t.1 b * frameTorsion e de ω (b, t.2.1, t.2.2) := by
    intro e de ω t
    simp only [frameTorsion, key2, Matrix.mul_apply]
    rw [← Finset.sum_sub_distrib]
    exact Finset.sum_congr rfl fun b _ => by ring
  refine ⟨fun e de ω => ⟨fun t => hft e de ω t, fun he => ?_, ?_⟩, fun e => ?_, fun vol gi T => ?_,
    fun vol gi g T => ?_, fun vol T hvol hT hd => ?_, fun g Γ l m n => ?_⟩
  · have h1 : frameTorsion (P * e) (fun m => P * de m) (fun m => P * ω m * P) =
        lower P (frameTorsion e de ω) := by
      funext t; rw [hft e de ω t]; rfl
    have hinv : (P * e)⁻¹ = e⁻¹ * P := by rw [Matrix.mul_inv_rev, inv_eq_left_inv PP]
    rw [h1, lower_lower, hinv, Matrix.mul_assoc, PP, Matrix.mul_one]
  · funext ⟨l, m, n⟩
    simp only [lower, LinearMap.coe_mk, AddHom.coe_mk, torsion, LinearMap.sub_apply,
      LinearMap.id_apply, tau_apply, swapIdx, gammaOf, frameTorsion, Matrix.mul_apply, mul_sub,
      Finset.sum_sub_distrib, Pi.sub_apply]
  · rw [det_mul, TetradScheme.P_T.2.2.1]; ring
  · funext t; simp only [dualT, Pi.neg_apply]; simp [Finset.sum_neg_distrib, neg_mul]
  · funext s; simp only [axial, Pi.neg_apply]; simp [Finset.sum_neg_distrib, neg_mul]
  · funext ⟨l, γ, δ⟩
    have ho := (mem_oddPart T).mp hT
    have ho' : ∀ μ ν, vol * T (l, ν, μ) = -(vol * T (l, μ, ν)) := by
      intro μ ν; rw [show T (l, ν, μ) = -T (l, μ, ν) from ho (l, μ, ν)]; ring
    have hv : ∀ μ ν, vol * T (l, μ, ν) = 0 → T (l, μ, ν) = 0 :=
      fun μ ν h => (mul_eq_zero.mp h).resolve_left hvol
    have e01 := congrFun hd (l, 0, 1); have e02 := congrFun hd (l, 0, 2)
    have e03 := congrFun hd (l, 0, 3); have e12 := congrFun hd (l, 1, 2)
    have e13 := congrFun hd (l, 1, 3); have e23 := congrFun hd (l, 2, 3)
    simp only [dualT, Fin.sum_univ_four, Pi.zero_apply] at e01 e02 e03 e12 e13 e23
    norm_num [levi, etaR, diagonal_apply] at e01 e02 e03 e12 e13 e23
    have s12 : Int.sign 12 = 1 := by decide
    simp only [s12, Int.cast_one, mul_one] at e01 e02 e03 e12 e13 e23
    apply hv
    fin_cases γ <;> fin_cases δ <;> simp only [Fin.zero_eta, Fin.mk_one, Fin.reduceFinMk] <;>
      linarith [ho' 0 1, ho' 0 2, ho' 0 3, ho' 1 2, ho' 1 3, ho' 2 3, ho' 0 0, ho' 1 1, ho' 2 2,
        ho' 3 3]
  · have hP : lower g (Pplus Γ) = Pplus (lower g Γ) := by
      funext t
      simp [lower, Pplus, tau_apply, swapIdx, mul_add, Finset.sum_add_distrib, Finset.mul_sum]
      ring_nf
    simp only [lower_torsion, hP]
    simp only [torsion, Pplus, LinearMap.sub_apply, LinearMap.id_apply, LinearMap.smul_apply,
      LinearMap.add_apply, tau_apply, swapIdx, Pi.sub_apply, Pi.smul_apply, Pi.add_apply,
      smul_eq_mul]
    constructor <;> ring

#print axioms GramMatrixTetradEquation.lemma1
#print axioms GramMatrixTetradEquation.lemma2
#print axioms GramMatrixTetradEquation.lemma3
#print axioms GramMatrixTetradEquation.lemma4
#print axioms GramMatrixTetradEquation.lemma5
#print axioms GramMatrixTetradEquation.prop1
#print axioms GramMatrixTetradEquation.theorem1
#print axioms GramMatrixTetradEquation.realise_perm
#print axioms GramMatrixTetradEquation.induced_perm
#print axioms GramMatrixTetradEquation.symA_card
#print axioms GramMatrixTetradEquation.theorem2
#print axioms GramMatrixTetradEquation.quarter_turn_exchanges
#print axioms GramMatrixTetradEquation.grid
#print axioms GramMatrixTetradEquation.lemma6
#print axioms GramMatrixTetradEquation.cautions
#print axioms GramMatrixTetradEquation.theorem3_i
#print axioms GramMatrixTetradEquation.theorem3_ii
#print axioms GramMatrixTetradEquation.theorem3_iii
#print axioms GramMatrixTetradEquation.prop2
#print axioms GramMatrixTetradEquation.levi_spec
#print axioms GramMatrixTetradEquation.prop3

end GramMatrixTetradEquation
