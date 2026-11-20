import HalfSpaceTwoBoundedRegions
import Mathlib.Topology.Instances.Matrix

/-!
# Lean 4 / Mathlib formalisation of
#   S. Nelson, "The Tetrad Scheme and the Two Bounded Regions"
#   (Route 2 of Letter 1, "The Coordinate-Space Geometry of the Tetrad Frame")

Builds on `ForcedTetrahedralFrame` (the four directions, columns of `M`) and on
`HalfSpaceTwoBoundedRegions` (Route 1: TetA, TetB, the projections `v_a`).

## How to referee this file
A Lean proof can only be wrong in its *statements*. Check these definitions against the paper:
* `etaR R = diag(−1, 1, 1, 1)` over any commutative ring `R`; `etaR ℝ` is the Minkowski metric.
* `IsTetrad g e : eᵀ η e = g`, the tetrad equation, Eq. (1). Row `a` of `e` is the leg `e^a`.
* `IsLorentz Λ : Λᵀ η Λ = η`, the Lorentz group `O(η)`.
* `kappa g = det g / det η`, Eq. (2). `Xplus g`, `Xminus g`: the solutions with `det e = ±√κ`.
* `P = diag(1, −1, −1, −1)` (spatial parity), `T = diag(−1, 1, 1, 1)` (time reversal).
* `obs Q`: the frame change `diag(1, Q)` that holds the time leg fixed.

## What is cited, not proved
That each root's piece does not split further *as a scheme*, because `SO(4, ℂ)` is connected
(Borel), and that `O(1,3)` has exactly four connected components (Wald). Mathlib has neither the
scheme `X_g` nor these connectedness results. Everything else in the note is proved here; the
split into two roots is proved as sets of real tetrads, each closed, and each open in the
solution set.
-/

open Matrix

namespace TetradScheme

open ForcedTetrahedralFrame (Mmat Mcol MMt MtM_apply)
open HalfSpaceTwoBoundedRegions (TetA TetB proj)

/-! ## The tetrad equation, over any commutative ring -/

section Ring

variable {R : Type*} [CommRing R]

/-- The Minkowski metric `η = diag(−1, 1, 1, 1)` with entries in `R`. -/
def etaR (R : Type*) [CommRing R] : Matrix (Fin 4) (Fin 4) R := diagonal ![-1, 1, 1, 1]

/-- The tetrad equation `g = eᵀ η e`. -/
def IsTetrad (g e : Matrix (Fin 4) (Fin 4) R) : Prop := eᵀ * etaR R * e = g

/-- `Λ` preserves `η`: `Λᵀ η Λ = η`. -/
def IsLorentz (Λ : Matrix (Fin 4) (Fin 4) R) : Prop := Λᵀ * etaR R * Λ = etaR R

lemma det_etaR : (etaR R).det = -1 := by
  simp [etaR, det_diagonal, Fin.prod_univ_four]

lemma etaR_transpose : (etaR R)ᵀ = etaR R := by simp [etaR]

/-- **Lorentz transformations act on solutions**: if `e` solves the equation, so does `Λ e`. -/
theorem lorentz_acts {g e Λ : Matrix (Fin 4) (Fin 4) R} (hΛ : IsLorentz Λ) (he : IsTetrad g e) :
    IsTetrad g (Λ * e) := by
  unfold IsTetrad IsLorentz at *
  rw [transpose_mul, show eᵀ * Λᵀ * etaR R * (Λ * e) = eᵀ * (Λᵀ * etaR R * Λ) * e by
    simp only [Matrix.mul_assoc], hΛ, he]

/-- Taking determinants: `(det e)² det η = det g`. -/
theorem det_sq {g e : Matrix (Fin 4) (Fin 4) R} (he : IsTetrad g e) :
    e.det ^ 2 * (etaR R).det = g.det := by
  rw [← he, det_mul, det_mul, det_transpose]; ring

/-- If `det g` is a unit, every solution is invertible. -/
theorem isUnit_det {g e : Matrix (Fin 4) (Fin 4) R} (hg : IsUnit g.det) (he : IsTetrad g e) :
    IsUnit e.det := by
  have h := det_sq he
  rw [det_etaR] at h
  have : e.det * (-e.det) = g.det := by rw [← h]; ring
  rw [← this] at hg
  exact isUnit_of_mul_isUnit_left hg

/-- **The orbit claim.** Any two solutions differ by exactly one Lorentz transformation. -/
theorem orbit {g e e' : Matrix (Fin 4) (Fin 4) R} (hg : IsUnit g.det) (he : IsTetrad g e)
    (he' : IsTetrad g e') : ∃! Λ, IsLorentz Λ ∧ e' = Λ * e := by
  have hu := isUnit_det hg he
  have hinv : e⁻¹ * e = 1 := nonsing_inv_mul e hu
  have hinv' : e * e⁻¹ = 1 := mul_nonsing_inv e hu
  refine ⟨e' * e⁻¹, ⟨?_, by rw [Matrix.mul_assoc, hinv, Matrix.mul_one]⟩, ?_⟩
  · unfold IsLorentz
    unfold IsTetrad at he he'
    calc (e' * e⁻¹)ᵀ * etaR R * (e' * e⁻¹) = (e⁻¹)ᵀ * (e'ᵀ * etaR R * e') * e⁻¹ := by
          rw [transpose_mul]; simp only [Matrix.mul_assoc]
      _ = (e⁻¹)ᵀ * (eᵀ * etaR R * e) * e⁻¹ := by rw [he', he]
      _ = (e * e⁻¹)ᵀ * etaR R * (e * e⁻¹) := by rw [transpose_mul]; simp only [Matrix.mul_assoc]
      _ = etaR R := by rw [hinv']; simp
  · rintro Λ ⟨-, hΛ⟩
    rw [hΛ, Matrix.mul_assoc, hinv', Matrix.mul_one]

/-- **The solution space is one Lorentz orbit, and distinct `Λ` give distinct solutions**:
`Λ ↦ Λ e₀` is a bijection from `O(η)` onto the solutions. -/
theorem solutions_eq_orbit {g e₀ : Matrix (Fin 4) (Fin 4) R} (hg : IsUnit g.det)
    (he₀ : IsTetrad g e₀) :
    (∀ e, IsTetrad g e ↔ ∃ Λ, IsLorentz Λ ∧ e = Λ * e₀) ∧
      ∀ Λ Λ' : Matrix (Fin 4) (Fin 4) R, Λ * e₀ = Λ' * e₀ → Λ = Λ' := by
  refine ⟨fun e => ⟨fun he => (orbit hg he₀ he).exists, ?_⟩, fun Λ Λ' h => ?_⟩
  · rintro ⟨Λ, hΛ, rfl⟩; exact lorentz_acts hΛ he₀
  · have hinv' : e₀ * e₀⁻¹ = 1 := mul_nonsing_inv e₀ (isUnit_det hg he₀)
    have := congrArg (· * e₀⁻¹) h
    simpa only [Matrix.mul_assoc, hinv', Matrix.mul_one] using this

/-- The signature convention `(+,−,−,−)` replaces `η` by `−η`: it leaves the Lorentz group and the
solution set unchanged (with `g` replaced by `−g`), so it selects no root. -/
theorem signature_convention (Λ e g : Matrix (Fin 4) (Fin 4) R) :
    (Λᵀ * (-etaR R) * Λ = -etaR R ↔ IsLorentz Λ) ∧
      (eᵀ * (-etaR R) * e = -g ↔ IsTetrad g e) := by
  constructor <;> simp [IsLorentz, IsTetrad]

end Ring

/-! ## The two roots, over ℝ -/

abbrev eta : Matrix (Fin 4) (Fin 4) ℝ := etaR ℝ

/-- `κ = det g / det η`. -/
noncomputable def kappa (g : Matrix (Fin 4) (Fin 4) ℝ) : ℝ := g.det / eta.det

/-- The solutions on the root `det e = +√κ`. -/
def Xplus (g : Matrix (Fin 4) (Fin 4) ℝ) : Set (Matrix (Fin 4) (Fin 4) ℝ) :=
  {e | IsTetrad g e ∧ e.det = Real.sqrt (kappa g)}

/-- The solutions on the root `det e = −√κ`. -/
def Xminus (g : Matrix (Fin 4) (Fin 4) ℝ) : Set (Matrix (Fin 4) (Fin 4) ℝ) :=
  {e | IsTetrad g e ∧ e.det = -Real.sqrt (kappa g)}

/-- **Eq. (2)**: `(det e)² = κ`, and `κ > 0` whenever `g` is non-degenerate and has a tetrad. -/
theorem det_sq_kappa {g e : Matrix (Fin 4) (Fin 4) ℝ} (he : IsTetrad g e) :
    e.det ^ 2 = kappa g := by
  have h := det_sq he
  rw [kappa, ← h, det_etaR]; field_simp

theorem kappa_pos {g e : Matrix (Fin 4) (Fin 4) ℝ} (hg : g.det ≠ 0) (he : IsTetrad g e) :
    0 < kappa g := by
  rw [← det_sq_kappa he]
  have h := det_sq he
  have : e.det ≠ 0 := by intro h0; rw [h0] at h; simp at h; exact hg h.symm
  positivity

/-- **The scheme is two schemes** (as sets of real tetrads): every solution lies on exactly one of
the two roots `±√κ`. -/
theorem two_roots {g : Matrix (Fin 4) (Fin 4) ℝ} (hg : g.det ≠ 0) :
    {e | IsTetrad g e} = Xplus g ∪ Xminus g ∧ Disjoint (Xplus g) (Xminus g) := by
  refine ⟨?_, ?_⟩
  · ext e
    simp only [Set.mem_ofPred_eq, Set.mem_union, Xplus, Xminus]
    constructor
    · intro he
      have h := det_sq_kappa he
      have hk := kappa_pos hg he
      have : e.det ^ 2 = Real.sqrt (kappa g) ^ 2 := by rw [Real.sq_sqrt hk.le, h]
      rcases sq_eq_sq_iff_eq_or_eq_neg.mp this with h' | h'
      · exact Or.inl ⟨he, h'⟩
      · exact Or.inr ⟨he, h'⟩
    · rintro (⟨he, -⟩ | ⟨he, -⟩) <;> exact he
  · rw [Set.disjoint_left]
    rintro e ⟨he, h1⟩ ⟨-, h2⟩
    have hk := Real.sqrt_pos.mpr (kappa_pos hg he)
    linarith

lemma continuous_metric : Continuous fun e : Matrix (Fin 4) (Fin 4) ℝ => eᵀ * eta * e :=
  ((continuous_id.matrix_transpose).matrix_mul continuous_const).matrix_mul continuous_id

/-- Each root's piece is closed, and is open in the solution set: it is the solution set cut by
the open condition `det e > 0` (respectively `< 0`). -/
theorem roots_clopen {g : Matrix (Fin 4) (Fin 4) ℝ} (hg : g.det ≠ 0) :
    IsClosed (Xplus g) ∧ IsClosed (Xminus g) ∧
      Xplus g = {e | IsTetrad g e} ∩ {e | 0 < e.det} ∧
      Xminus g = {e | IsTetrad g e} ∩ {e | e.det < 0} ∧
      IsOpen {e : Matrix (Fin 4) (Fin 4) ℝ | 0 < e.det} ∧
      IsOpen {e : Matrix (Fin 4) (Fin 4) ℝ | e.det < 0} := by
  have hdet : Continuous fun e : Matrix (Fin 4) (Fin 4) ℝ => e.det := continuous_id.matrix_det
  have hT : IsClosed {e : Matrix (Fin 4) (Fin 4) ℝ | IsTetrad g e} :=
    isClosed_eq continuous_metric continuous_const
  refine ⟨hT.inter (isClosed_eq hdet continuous_const),
    hT.inter (isClosed_eq hdet continuous_const), ?_, ?_,
    isOpen_lt continuous_const hdet, isOpen_lt hdet continuous_const⟩
  · ext e
    simp only [Xplus, Set.mem_ofPred_eq, Set.mem_inter_iff]
    constructor
    · rintro ⟨he, h⟩; exact ⟨he, by rw [h]; exact Real.sqrt_pos.mpr (kappa_pos hg he)⟩
    · rintro ⟨he, h⟩
      refine ⟨he, ?_⟩
      have h2 := det_sq_kappa he
      rw [← h2, Real.sqrt_sq h.le]
  · ext e
    simp only [Xminus, Set.mem_ofPred_eq, Set.mem_inter_iff]
    constructor
    · rintro ⟨he, h⟩
      exact ⟨he, by rw [h]; simpa using Real.sqrt_pos.mpr (kappa_pos hg he)⟩
    · rintro ⟨he, h⟩
      refine ⟨he, ?_⟩
      have h2 := det_sq_kappa he
      rw [← h2, show e.det ^ 2 = (-e.det) ^ 2 by ring, Real.sqrt_sq (by linarith)]; ring

/-! ## Frame changes and the four Lorentz classes -/

/-- Spatial parity `P = diag(1, −1, −1, −1)`. -/
def P : Matrix (Fin 4) (Fin 4) ℝ := diagonal ![1, -1, -1, -1]

/-- Time reversal `T = diag(−1, 1, 1, 1)`. -/
def T : Matrix (Fin 4) (Fin 4) ℝ := diagonal ![-1, 1, 1, 1]

lemma metric_apply (Λ : Matrix (Fin 4) (Fin 4) ℝ) (i j : Fin 4) :
    (Λᵀ * eta * Λ) i j = -(Λ 0 i * Λ 0 j) + Λ 1 i * Λ 1 j + Λ 2 i * Λ 2 j + Λ 3 i * Λ 3 j := by
  simp [Matrix.mul_apply, Fin.sum_univ_four, etaR, diagonal_apply]

/-- **A change of frame multiplies `det e` by `det Λ = ±1`**, so it exchanges the roots iff
`det Λ = −1`. -/
theorem frame_change {g e Λ : Matrix (Fin 4) (Fin 4) ℝ} (hg : g.det ≠ 0) (hΛ : IsLorentz Λ)
    (he : e ∈ Xplus g) :
    (Λ.det = 1 ∨ Λ.det = -1) ∧ (Λ * e ∈ Xminus g ↔ Λ.det = -1) ∧ (Λ * e ∈ Xplus g ↔ Λ.det = 1) := by
  have hd := det_sq (R := ℝ) hΛ
  rw [det_etaR] at hd
  have h1 : Λ.det ^ 2 = 1 := by linarith
  have hk := Real.sqrt_pos.mpr (kappa_pos hg he.1)
  have hs : Λ.det = 1 ∨ Λ.det = -1 := by
    have : (Λ.det - 1) * (Λ.det + 1) = 0 := by ring_nf; linarith
    rcases mul_eq_zero.mp this with h | h
    · left; linarith
    · right; linarith
  have hm := lorentz_acts hΛ he.1
  refine ⟨hs, ?_, ?_⟩
  · simp only [Xminus, Set.mem_ofPred_eq, det_mul, he.2, hm, true_and]
    constructor
    · intro h
      have : (Λ.det + 1) * Real.sqrt (kappa g) = 0 := by linarith
      rcases mul_eq_zero.mp this with h' | h' <;> [linarith; linarith]
    · intro h; rw [h]; ring
  · simp only [Xplus, Set.mem_ofPred_eq, det_mul, he.2, hm, true_and]
    constructor
    · intro h
      have : (Λ.det - 1) * Real.sqrt (kappa g) = 0 := by linarith
      rcases mul_eq_zero.mp this with h' | h' <;> [linarith; linarith]
    · intro h; rw [h]; ring

/-- `P` and `T` are Lorentz with determinant `−1`; `PT = −I` has determinant `+1`. -/
theorem P_T :
    IsLorentz P ∧ IsLorentz T ∧ P.det = -1 ∧ T.det = -1 ∧ P * T = -1 ∧
      (-1 : Matrix (Fin 4) (Fin 4) ℝ).det = 1 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · unfold IsLorentz; ext i j; rw [metric_apply]
    fin_cases i <;> fin_cases j <;> simp [P, etaR]
  · unfold IsLorentz; ext i j; rw [metric_apply]
    fin_cases i <;> fin_cases j <;> simp [T, etaR]
  · simp [P, det_diagonal, Fin.prod_univ_four]
  · simp [T, det_diagonal, Fin.prod_univ_four]
  · ext i j; fin_cases i <;> fin_cases j <;> simp [P, T]
  · rw [det_neg]; norm_num

/-- For a Lorentz `Λ`, `Λ₀₀² ≥ 1`: the time orientation `sign Λ₀₀` is well defined. -/
theorem time_component {Λ : Matrix (Fin 4) (Fin 4) ℝ} (hΛ : IsLorentz Λ) : 1 ≤ Λ 0 0 ^ 2 := by
  have := congrFun (congrFun hΛ 0) 0
  rw [metric_apply] at this
  simp [etaR] at this
  nlinarith [sq_nonneg (Λ 1 0), sq_nonneg (Λ 2 0), sq_nonneg (Λ 3 0)]

/-- **The four classes.** `I`, `P`, `T`, `PT` realise all four combinations of
`(det Λ, sign Λ₀₀)`, the labels of the four components of `O(1,3)`. -/
theorem four_classes :
    ((1 : Matrix (Fin 4) (Fin 4) ℝ).det = 1 ∧ (0 : ℝ) < (1 : Matrix (Fin 4) (Fin 4) ℝ) 0 0) ∧
      (P.det = -1 ∧ (0 : ℝ) < P 0 0) ∧ (T.det = -1 ∧ T 0 0 < 0) ∧
      ((P * T).det = 1 ∧ (P * T) 0 0 < 0) := by
  obtain ⟨-, -, hP, hT, hPT, hm⟩ := P_T
  refine ⟨by simp, ⟨hP, by simp [P]⟩, ⟨hT, by simp [T]⟩, ⟨by rw [hPT, hm], by rw [hPT]; simp⟩⟩

/-! ## One observer: the frame changes that hold the time leg fixed -/

/-- `diag(1, Q)`. -/
def obs (Q : Matrix (Fin 3) (Fin 3) ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![1, 0, 0, 0; 0, Q 0 0, Q 0 1, Q 0 2; 0, Q 1 0, Q 1 1, Q 1 2; 0, Q 2 0, Q 2 1, Q 2 2]

theorem det_obs (Q : Matrix (Fin 3) (Fin 3) ℝ) : (obs Q).det = Q.det := by
  rw [det_succ_row_zero, Fin.sum_univ_succ]
  simp [obs, det_fin_three, submatrix]

/-- `diag(1, Q)` is Lorentz iff `Q ∈ O(3)`. -/
theorem obs_lorentz (Q : Matrix (Fin 3) (Fin 3) ℝ) : IsLorentz (obs Q) ↔ Qᵀ * Q = 1 := by
  constructor
  · intro h
    ext i j
    have := congrFun (congrFun h i.succ) j.succ
    rw [metric_apply] at this
    rw [Matrix.mul_apply, Fin.sum_univ_three]
    fin_cases i <;> fin_cases j <;> simp [obs, etaR] at this ⊢ <;> linarith
  · intro h
    unfold IsLorentz
    ext i j
    rw [metric_apply]
    have E : ∀ i j, Q 0 i * Q 0 j + Q 1 i * Q 1 j + Q 2 i * Q 2 j = if i = j then 1 else 0 := by
      intro i j
      have := Matrix.ext_iff.mpr h i j
      simpa [Matrix.mul_apply, Fin.sum_univ_three, Matrix.one_apply] using this
    have e00 := E 0 0; have e01 := E 0 1; have e02 := E 0 2
    have e10 := E 1 0; have e11 := E 1 1; have e12 := E 1 2
    have e20 := E 2 0; have e21 := E 2 1; have e22 := E 2 2
    norm_num at e00 e01 e02 e10 e11 e12 e20 e21 e22
    fin_cases i <;> fin_cases j <;> simp [obs, etaR] <;> linarith

/-- **Holding the time leg fixed forces `Λ = diag(1, Q)`.** If a Lorentz `Λ` leaves the time leg
unchanged (`Λ e` has row 0 equal to that of `e`, for every `e`), its spatial block is in `O(3)`
and `det Λ = det Q`: for one observer the root is the orientation of the spatial legs. -/
theorem fixed_time_leg {Λ : Matrix (Fin 4) (Fin 4) ℝ} (hΛ : IsLorentz Λ)
    (h : ∀ (e : Matrix (Fin 4) (Fin 4) ℝ) (j : Fin 4), (Λ * e) 0 j = e 0 j) :
    ∃ Q : Matrix (Fin 3) (Fin 3) ℝ, Λ = obs Q ∧ Qᵀ * Q = 1 ∧ Λ.det = Q.det := by
  have hrow : ∀ j, Λ 0 j = if j = 0 then 1 else 0 := by
    intro j
    have := h 1 j
    rw [Matrix.mul_one, Matrix.one_apply] at this
    rw [this]; simp [eq_comm]
  have hc := congrFun (congrFun hΛ 0) 0
  rw [metric_apply] at hc
  simp [etaR, hrow] at hc
  have h10 : Λ 1 0 = 0 := by nlinarith [sq_nonneg (Λ 1 0), sq_nonneg (Λ 2 0), sq_nonneg (Λ 3 0)]
  have h20 : Λ 2 0 = 0 := by nlinarith [sq_nonneg (Λ 1 0), sq_nonneg (Λ 2 0), sq_nonneg (Λ 3 0)]
  have h30 : Λ 3 0 = 0 := by nlinarith [sq_nonneg (Λ 1 0), sq_nonneg (Λ 2 0), sq_nonneg (Λ 3 0)]
  set Q : Matrix (Fin 3) (Fin 3) ℝ := fun i j => Λ i.succ j.succ with hQ
  have hobs : Λ = obs Q := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [obs, hQ, hrow, h10, h20, h30]
  refine ⟨Q, hobs, (obs_lorentz Q).mp (hobs ▸ hΛ), by rw [hobs, det_obs]⟩

/-- `obs` keeps the time leg, and parity is `obs (−I)`. -/
theorem obs_time_leg (Q : Matrix (Fin 3) (Fin 3) ℝ) (e : Matrix (Fin 4) (Fin 4) ℝ) :
    (obs Q * e) 0 = e 0 ∧ obs (-1) = P := by
  refine ⟨?_, ?_⟩
  · funext j; simp [obs, Matrix.mul_apply, Fin.sum_univ_four]
  · ext i j; fin_cases i <;> fin_cases j <;> simp [obs, P]

/-! ## Parity is canonical, not a rotation, and needs odd dimension -/

/-- **Parity is canonical.** An orthogonal `Q` commuting with every element of `O(3)` is `±I`;
only `−I` has determinant `−1`. (The proof uses only sign and permutation matrices.) -/
theorem center_O3 {Q : Matrix (Fin 3) (Fin 3) ℝ} (hQ : Qᵀ * Q = 1)
    (hc : ∀ S : Matrix (Fin 3) (Fin 3) ℝ, Sᵀ * S = 1 → Q * S = S * Q) :
    (Q = 1 ∨ Q = -1) ∧ (Q.det = -1 → Q = -1) := by
  have orth : ∀ S : Matrix (Fin 3) (Fin 3) ℝ, Sᵀ * S = 1 → Q * S = S * Q := hc
  have sgn := fun (d : Fin 3 → ℝ) (hd : ∀ i, d i * d i = 1) => orth (diagonal d) (by
    ext i j; by_cases h : i = j
    · subst h; simp [hd]
    · simp [h])
  have s0 := sgn ![-1, 1, 1] (by intro i; fin_cases i <;> norm_num)
  have s1 := sgn ![1, -1, 1] (by intro i; fin_cases i <;> norm_num)
  have p01 := orth !![0, 1, 0; 1, 0, 0; 0, 0, 1] (by
    ext i j; fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_three])
  have p12 := orth !![1, 0, 0; 0, 0, 1; 0, 1, 0] (by
    ext i j; fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_three])
  have E := fun (A B : Matrix (Fin 3) (Fin 3) ℝ) (h : A = B) (i j : Fin 3) =>
    Matrix.ext_iff.mpr h i j
  have a1 := E _ _ s0 0 1; have a2 := E _ _ s0 0 2; have a3 := E _ _ s0 1 0
  have a4 := E _ _ s0 2 0; have a5 := E _ _ s1 1 2; have a6 := E _ _ s1 2 1
  simp at a1 a2 a3 a4 a5 a6
  have hdiag : ∀ i j, i ≠ j → Q i j = 0 := by
    intro i j hij
    fin_cases i <;> fin_cases j <;> simp at hij ⊢ <;> linarith
  have q01 := E _ _ p01 0 1
  have q12 := E _ _ p12 1 2
  simp [Matrix.mul_apply, Fin.sum_univ_three] at q01 q12
  have hQ' : Q = Q 0 0 • (1 : Matrix (Fin 3) (Fin 3) ℝ) := by
    ext i j
    by_cases h : i = j
    · subst h; fin_cases i <;> simp <;> linarith
    · rw [hdiag i j h]; simp [h]
  have hsq : Q 0 0 * Q 0 0 = 1 := by
    have := E _ _ hQ 0 0
    simp [Matrix.mul_apply, Fin.sum_univ_three, hdiag 1 0 (by decide),
      hdiag 2 0 (by decide)] at this
    linarith
  have hpm : Q 0 0 = 1 ∨ Q 0 0 = -1 := by
    have : (Q 0 0 - 1) * (Q 0 0 + 1) = 0 := by ring_nf; linarith
    rcases mul_eq_zero.mp this with h | h
    · left; linarith
    · right; linarith
  have hor : Q = 1 ∨ Q = -1 := by
    rcases hpm with h | h
    · left; rw [hQ', h, one_smul]
    · right; rw [hQ', h, neg_one_smul]
  refine ⟨hor, fun hd => ?_⟩
  rcases hor with h | h
  · rw [h, det_one] at hd; norm_num at hd
  · exact h

/-- **Parity is not a rotation in disguise.** The four directions span `ℝ³`, so `Q n_a = −n_a` for
every `a` forces `Q = −I`; no rotation carries TetA's frame to TetB's leg by leg. -/
theorem parity_not_rotation (Q : Matrix (Fin 3) (Fin 3) ℝ) (h : ∀ a, Q *ᵥ Mcol a = -Mcol a) :
    Q = -1 := by
  have hM : Q * Mmat = -Mmat := by
    ext i a
    have := congrFun (h a) i
    simpa [mulVec, dotProduct, Mcol, Matrix.mul_apply] using this
  have : Q * (Mmat * Mmatᵀ) = -(Mmat * Mmatᵀ) := by
    rw [← Matrix.mul_assoc, hM, Matrix.neg_mul]
  rw [MMt, Matrix.mul_smul, Matrix.mul_one, ← smul_neg] at this
  have := congrArg ((1 / 4 : ℝ) • ·) this
  simpa [smul_smul] using this

theorem no_rotation_is_parity (Q : Matrix (Fin 3) (Fin 3) ℝ) (hd : Q.det = 1) :
    ∃ a, Q *ᵥ Mcol a ≠ -Mcol a := by
  by_contra h
  push Not at h
  have := parity_not_rotation Q h
  rw [this, det_neg] at hd
  norm_num at hd

/-- **Odd dimension.** `det(−I) = (−1)^D`; in even `D`, `−I` is a rotation and parity would give no
new component. -/
theorem parity_odd_dimension (D : ℕ) :
    (-1 : Matrix (Fin D) (Fin D) ℝ).det = (-1) ^ D ∧
      (Even D → (-1 : Matrix (Fin D) (Fin D) ℝ).det = 1) ∧
      (Odd D → (-1 : Matrix (Fin D) (Fin D) ℝ).det = -1) := by
  have h : (-1 : Matrix (Fin D) (Fin D) ℝ).det = (-1) ^ D := by rw [det_neg]; simp
  exact ⟨h, fun he => by rw [h, he.neg_one_pow], fun ho => by rw [h, ho.neg_one_pow]⟩

/-! ## Parity maps TetA onto TetB, Route 1's second bounded region -/

/-- **The bridge to Route 1.** Parity's spatial block `−I` sends every `v_a → −v_a` and maps TetA
onto TetB, the all-flipped region; the parity directions `−n_a` keep the pairwise inner product
`−1/3` after normalisation. -/
theorem parity_TetA_TetB :
    (∀ a p, proj a (-p) = -proj a p) ∧
      (fun p : Fin 3 → ℝ => -p) '' TetA = TetB ∧
      (∀ a b, a ≠ b → ((-Mcol a) ⬝ᵥ (-Mcol b)) / 3 = -1 / 3) ∧
      (∀ a, ((-Mcol a) ⬝ᵥ (-Mcol a)) / 3 = 1) := by
  have hdot : ∀ a b, Mcol a ⬝ᵥ Mcol b = if a = b then 3 else -1 := by
    intro a b; rw [← MtM_apply, Matrix.mul_apply]; simp [Mcol, dotProduct]
  refine ⟨fun a p => HalfSpaceTwoBoundedRegions.proj_neg a p, ?_, fun a b hab => ?_, fun a => ?_⟩
  · rw [HalfSpaceTwoBoundedRegions.TetB_eq_neg_TetA]
    ext p
    simp only [Set.mem_image, Set.mem_ofPred_eq]
    exact ⟨fun ⟨q, hq, hqp⟩ => by rw [← hqp, neg_neg]; exact hq,
      fun hp => ⟨-p, hp, neg_neg p⟩⟩
  · rw [neg_dotProduct, dotProduct_neg, neg_neg, hdot, ite_eq_right_of_eq_false _ _ (eq_false hab)]
  · rw [neg_dotProduct, dotProduct_neg, neg_neg, hdot, ite_eq_left_of_eq_true _ _ (eq_true rfl)]; norm_num

/-- **Caution 1: same shape.** The quarter turn `R` about the third axis is a rotation that maps
TetA onto TetB as point sets, and the vertex set `{−n_a}` onto `{n_a}`; yet it is not parity, so it
does not carry the frame leg by leg. -/
def Rq : Matrix (Fin 3) (Fin 3) ℝ := !![0, -1, 0; 1, 0, 0; 0, 0, 1]

theorem same_shape :
    Rqᵀ * Rq = 1 ∧ Rq.det = 1 ∧
      (fun p => Rq *ᵥ p) '' TetA = TetB ∧
      (Finset.univ.image fun a => Rq *ᵥ (-Mcol a)) = Finset.univ.image Mcol ∧
      ∃ a, Rq *ᵥ Mcol a ≠ -Mcol a := by
  have horth : Rqᵀ * Rq = 1 := by
    ext i j; fin_cases i <;> fin_cases j <;> simp [Rq, Matrix.mul_apply, Fin.sum_univ_three]
  have horth' : Rq * Rqᵀ = 1 := by
    ext i j; fin_cases i <;> fin_cases j <;> simp [Rq, Matrix.mul_apply, Fin.sum_univ_three]
  have hdet : Rq.det = 1 := by simp [Rq, det_fin_three]
  -- `Rqᵀ n_a = −n_{σ a}` with `σ = (0 1 3 2)` read off the vertices
  have hproj : ∀ (q : Fin 3 → ℝ) a, proj a (Rqᵀ *ᵥ q) =
      -proj (![1, 3, 0, 2] a) q := by
    intro q a
    simp only [proj, Mcol, Mmat, dotProduct, mulVec, Fin.sum_univ_three, transpose_apply]
    fin_cases a <;> simp [Rq] <;> ring
  have hperm : Function.Bijective (![1, 3, 0, 2] : Fin 4 → Fin 4) := by decide
  refine ⟨horth, hdet, ?_, ?_, no_rotation_is_parity Rq hdet⟩
  · ext p
    simp only [Set.mem_image]
    rw [HalfSpaceTwoBoundedRegions.mem_TetB]
    constructor
    · rintro ⟨q, hq, rfl⟩ b
      obtain ⟨a, ha⟩ := hperm.2 b
      have := (HalfSpaceTwoBoundedRegions.mem_TetA q).mp hq a
      have e := hproj (Rq *ᵥ q) a
      rw [mulVec_mulVec, horth, one_mulVec, ha] at e
      linarith
    · intro hp
      refine ⟨Rqᵀ *ᵥ p, ?_, by rw [mulVec_mulVec, horth', one_mulVec]⟩
      rw [HalfSpaceTwoBoundedRegions.mem_TetA]
      intro a
      rw [hproj]
      linarith [hp (![1, 3, 0, 2] a)]
  · have hcomp : (fun a => Rq *ᵥ (-Mcol a)) = Mcol ∘ (![1, 3, 0, 2] : Fin 4 → Fin 4) := by
      funext a i
      fin_cases a <;> fin_cases i <;> simp [Rq, Mcol, Mmat, mulVec, dotProduct, Fin.sum_univ_three]
    rw [hcomp, ← Finset.image_image, Finset.image_univ_of_surjective hperm.2]

/-- **Caution 2: direction of time.** Reversing every leg, `−e = PT e`, keeps `det e`; its spatial
legs are those of `P e`, but its time leg is reversed. -/
theorem all_legs_reversed (e : Matrix (Fin 4) (Fin 4) ℝ) :
    -e = (P * T) * e ∧ (-e).det = e.det ∧
      (∀ i : Fin 4, i ≠ 0 → (-e) i = (P * e) i) ∧ (-e) 0 = -((P * e) 0) := by
  obtain ⟨-, -, -, -, hPT, -⟩ := P_T
  refine ⟨by rw [hPT]; simp, by rw [det_neg]; norm_num, fun i hi => ?_, ?_⟩
  · funext j
    fin_cases i
    · exact absurd rfl hi
    all_goals simp [P, Matrix.mul_apply, diagonal_apply]
  · funext j; simp [P, Matrix.mul_apply, diagonal_apply]

/-! ## Both schemes are present, and the metric cannot choose -/

/-- **Both roots occur.** If `e` solves the equation, so does `P e`, on the other root. -/
theorem both_present {g e : Matrix (Fin 4) (Fin 4) ℝ} (hg : g.det ≠ 0) (he : e ∈ Xplus g) :
    P * e ∈ Xminus g := by
  obtain ⟨hP, -, hdP, -⟩ := P_T
  exact ((frame_change hg hP he).2.1).mpr hdP

/-- **The metric is root-blind**: every quantity built from the metric takes the same value on
`e` and `Λ e`, for every Lorentz `Λ`, in particular on both roots. -/
theorem metric_blind {α : Type*} (F : Matrix (Fin 4) (Fin 4) ℝ → α) (e Λ : Matrix (Fin 4) (Fin 4) ℝ)
    (hΛ : IsLorentz Λ) : F ((Λ * e)ᵀ * eta * (Λ * e)) = F (eᵀ * eta * e) := by
  rw [lorentz_acts hΛ (rfl : IsTetrad (eᵀ * eta * e) e)]

/-- **The metric cannot choose**: no function of the metric returns `det e`. -/
theorem metric_cannot_choose :
    ¬ ∃ F : Matrix (Fin 4) (Fin 4) ℝ → ℝ, ∀ e : Matrix (Fin 4) (Fin 4) ℝ,
      F (eᵀ * eta * e) = e.det := by
  rintro ⟨F, hF⟩
  obtain ⟨hP, -, hdP, -⟩ := P_T
  have h1 := hF 1
  have h2 := hF (P * 1)
  rw [metric_blind F 1 P hP, h1, Matrix.mul_one, hdP, det_one] at h2
  norm_num at h2

/-- **Keeping one root is an extra equation.** The system `g = eᵀηe, det e = +√κ` has strictly
fewer solutions than the tetrad equation, and frame changes with `det Λ = 1` (such as
`SO⁺(1,3)`) stay on one root. -/
theorem one_root_is_a_restriction {g e : Matrix (Fin 4) (Fin 4) ℝ} (hg : g.det ≠ 0)
    (he : IsTetrad g e) :
    Xplus g ⊂ {e | IsTetrad g e} ∧
      ∀ Λ, IsLorentz Λ → Λ.det = 1 → ∀ e' ∈ Xplus g, Λ * e' ∈ Xplus g := by
  have hsplit := two_roots hg
  refine ⟨⟨fun e' he' => he'.1, fun hsub => ?_⟩, fun Λ hΛ hd e' he' =>
    ((frame_change hg hΛ he').2.2).mpr hd⟩
  have hmem : e ∈ Xplus g ∪ Xminus g := hsplit.1 ▸ he
  obtain ⟨hP, -, -, -⟩ := P_T
  rcases hmem with hp | hm
  · have := both_present hg hp
    exact Set.disjoint_left.mp hsplit.2 (hsub this.1) this
  · exact Set.disjoint_left.mp hsplit.2 (hsub hm.1) hm

/-! ## Each scheme carries a 3 + 1 decomposition, relative to the frame -/

/-- **The 3 + 1 pattern, relative to the legs.** TetA's normals: one `(+,+,+)`, three mixed;
TetB's: `(−,−,−)`. The tetrahedron's own rotations `diag(n_a)` (in `SO(3)`) permute the four
normals and send `n_0` to any `n_a`, so the pattern belongs to the tetrahedron relative to the
frame's axes, not to the tetrahedron alone. -/
theorem three_plus_one_relative :
    (∀ i, Mcol 0 i = 1) ∧ (∀ a, a ≠ 0 → ∃ i j, Mcol a i ≠ Mcol a j) ∧ (∀ i, (-Mcol 0) i = -1) ∧
      ∀ a, (diagonal (Mcol a))ᵀ * diagonal (Mcol a) = 1 ∧ (diagonal (Mcol a)).det = 1 ∧
        diagonal (Mcol a) *ᵥ Mcol 0 = Mcol a ∧ ∀ b, ∃ c, diagonal (Mcol a) *ᵥ Mcol b = Mcol c := by
  obtain ⟨h1, h2, h3⟩ := HalfSpaceTwoBoundedRegions.three_plus_one
  refine ⟨h1, h2, h3, fun a => ⟨?_, ?_, ?_, fun b => ?_⟩⟩
  · have hsq : ∀ i, Mcol a i * Mcol a i = 1 := by
      intro i; fin_cases a <;> fin_cases i <;> norm_num [Mcol, Mmat]
    rw [diagonal_transpose, diagonal_mul_diagonal]; simp only [hsq]; exact diagonal_one
  · fin_cases a <;> simp [Mcol, Mmat, det_diagonal, Fin.prod_univ_three]
  · funext i; fin_cases a <;> fin_cases i <;> simp [Mcol, Mmat, mulVec_diagonal]
  · refine ⟨(![![0, 1, 2, 3], ![1, 0, 3, 2], ![2, 3, 0, 1], ![3, 2, 1, 0]] : Fin 4 → Fin 4 → Fin 4)
      a b, ?_⟩
    funext i
    fin_cases a <;> fin_cases b <;> fin_cases i <;> simp [Mcol, Mmat, mulVec_diagonal]

#print axioms TetradScheme.lorentz_acts
#print axioms TetradScheme.det_sq
#print axioms TetradScheme.orbit
#print axioms TetradScheme.solutions_eq_orbit
#print axioms TetradScheme.signature_convention
#print axioms TetradScheme.kappa_pos
#print axioms TetradScheme.two_roots
#print axioms TetradScheme.roots_clopen
#print axioms TetradScheme.frame_change
#print axioms TetradScheme.P_T
#print axioms TetradScheme.four_classes
#print axioms TetradScheme.time_component
#print axioms TetradScheme.obs_lorentz
#print axioms TetradScheme.fixed_time_leg
#print axioms TetradScheme.center_O3
#print axioms TetradScheme.parity_not_rotation
#print axioms TetradScheme.no_rotation_is_parity
#print axioms TetradScheme.parity_odd_dimension
#print axioms TetradScheme.parity_TetA_TetB
#print axioms TetradScheme.same_shape
#print axioms TetradScheme.all_legs_reversed
#print axioms TetradScheme.both_present
#print axioms TetradScheme.metric_blind
#print axioms TetradScheme.metric_cannot_choose
#print axioms TetradScheme.one_root_is_a_restriction
#print axioms TetradScheme.three_plus_one_relative

end TetradScheme
