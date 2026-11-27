import RecursiveTriforceClosure
import Mathlib

/-! # Proof 26: Gravity as the Response of Recursive Field Closure — finite theorems

This file machine-checks the exact, finite parts of Proof 26 (Revision 4). It imports
Proof 23 (`RecursiveTriforceClosure`) and reuses its labels, its 64 addresses, its
4 × 4 Hadamard matrix `H4` and its order-three label cycle, rather than restating them.

What is proved here is mathematics. The physical premises of the proof — that the native
action selects the collective determinant, that each direction carries |t|² = α, and the
long-wave source action — are not formalised and are not claimed. See `LEAN_AUDIT.md`.
-/

namespace RecursiveFieldClosureResponse

open RecursiveTriforceClosure Matrix
open scoped BigOperators Kronecker

set_option maxRecDepth 8192
set_option maxHeartbeats 0

/-! ## Theorem 1. Blind closure and sufficient information -/

/-- A blind (environment-independent) closure exists exactly when all feasible sets meet. -/
theorem blind_closure {X Y : Type*} (C : Y → Set X) :
    (∃ x, ∀ y, x ∈ C y) ↔ (⋂ y, C y).Nonempty := by
  simp [Set.Nonempty, Set.mem_iInter]

/-- A read `R` permits exact settlement `S = F ∘ R` exactly when equal reads force equal
settlements. -/
theorem read_factorization {X Y Z : Type*} [Nonempty X] (R : Y → Z) (S : Y → X) :
    (∃ F : Z → X, ∀ y, S y = F (R y)) ↔ ∀ y z, R y = R z → S y = S z := by
  classical
  constructor
  · rintro ⟨F, hF⟩ y z h
    rw [hF y, hF z, h]
  · intro H
    refine ⟨fun z => if h : ∃ y, R y = z then S h.choose else Classical.arbitrary X, ?_⟩
    intro y
    show S y = dite _ _ _
    split_ifs with h
    · exact H y h.choose h.choose_spec.symm
    · exact absurd ⟨y, rfl⟩ h

/-! ## Theorem 3. Three Walsh sweeps -/

/-- Proof 23's `H4`, as a matrix. -/
def Hm : Matrix Label Label ℤ := Matrix.of H4

/-- The 64-address Walsh–Hadamard matrix, one factor per Sierpiński level. -/
def H64 : Matrix Address Address ℤ := Hm ⊗ₖ (Hm ⊗ₖ Hm)

/-- The three radix-four sweeps, one per digit. -/
def sweep0 : Matrix Address Address ℤ := Hm ⊗ₖ ((1 : Matrix Label Label ℤ) ⊗ₖ 1)
def sweep1 : Matrix Address Address ℤ := (1 : Matrix Label Label ℤ) ⊗ₖ (Hm ⊗ₖ 1)
def sweep2 : Matrix Address Address ℤ := (1 : Matrix Label Label ℤ) ⊗ₖ (1 ⊗ₖ Hm)

theorem H4_symm (i j : Label) : H4 i j = H4 j i := by
  fin_cases i <;> fin_cases j <;> decide

theorem Hm_sq : Hm * Hm = (4 : ℤ) • (1 : Matrix Label Label ℤ) := by
  ext i j
  have h := local_walsh_orthogonal i j
  simp only [Hm, Matrix.mul_apply, Matrix.of_apply, Matrix.smul_apply, Matrix.one_apply,
    smul_eq_mul]
  rw [show (∑ k, H4 i k * H4 k j) = ∑ k, H4 i k * H4 j k from
    Finset.sum_congr rfl fun k _ => by rw [H4_symm k j], h]
  split_ifs <;> simp

/-- The full read is the product of the three sweeps. -/
theorem three_sweeps : sweep0 * sweep1 * sweep2 = H64 := by
  simp only [sweep0, sweep1, sweep2, H64, ← Matrix.mul_kronecker_mul, Matrix.mul_one,
    Matrix.one_mul]

/-- The sweeps commute, so their order is not fixed by the algebra. -/
theorem sweeps_commute :
    sweep0 * sweep1 = sweep1 * sweep0 ∧ sweep1 * sweep2 = sweep2 * sweep1 ∧
      sweep0 * sweep2 = sweep2 * sweep0 := by
  refine ⟨?_, ?_, ?_⟩ <;>
    simp only [sweep0, sweep1, sweep2, ← Matrix.mul_kronecker_mul, Matrix.mul_one,
      Matrix.one_mul]

/-- The read is reversible: `H64 * H64 = 64 • 1`, so `(H64/8)⁻¹ = H64/8`. -/
theorem H64_sq : H64 * H64 = (64 : ℤ) • (1 : Matrix Address Address ℤ) := by
  simp only [H64, ← Matrix.mul_kronecker_mul, Hm_sq, Matrix.smul_kronecker,
    Matrix.kronecker_smul, Matrix.one_kronecker_one, smul_smul]
  norm_num

/-- The label cycle is self-adjoint for the Walsh pairing. -/
theorem cycle_self_adjoint (i j : Label) : H4 (cycle i) j = H4 i (cycle j) := by
  fin_cases i <;> fin_cases j <;> decide

/-! ## Theorem 4. The Sierpiński factorization -/

/-- The subset (Sierpiński) matrix on two bits, in the same bit order as `H4`. -/
def S4 : Matrix Label Label ℤ := Matrix.of
  (![![1,0,0,0],![1,1,0,0],![1,0,1,0],![1,1,1,1]] : Label → Label → ℤ)

/-- The weight `(-2)^|c|`. -/
def D4 : Matrix Label Label ℤ := Matrix.of
  (![![1,0,0,0],![0,-2,0,0],![0,0,-2,0],![0,0,0,4]] : Label → Label → ℤ)

theorem sierpinski_four : S4 * D4 * S4ᵀ = Hm := by
  ext i j
  fin_cases i <;> fin_cases j <;> decide

/-- At size 64 the Hadamard matrix is Sierpiński · weight · Sierpiński-transpose. -/
theorem sierpinski_sixtyfour :
    (S4 ⊗ₖ (S4 ⊗ₖ S4)) * (D4 ⊗ₖ (D4 ⊗ₖ D4)) * (S4 ⊗ₖ (S4 ⊗ₖ S4))ᵀ = H64 := by
  have ht : (S4 ⊗ₖ (S4 ⊗ₖ S4))ᵀ = S4ᵀ ⊗ₖ (S4ᵀ ⊗ₖ S4ᵀ) := by
    ext ⟨a1, a2, a3⟩ ⟨b1, b2, b3⟩
    simp [Matrix.kroneckerMap_apply, Matrix.transpose_apply]
  rw [ht]
  simp only [← Matrix.mul_kronecker_mul]
  rw [sierpinski_four, H64]

/-- The lower shear on two bits. -/
def shear {R : Type*} [CommRing R] (z : R) : Matrix (Fin 2) (Fin 2) R := !![1, 0; z, 1]

/-- Same-direction sweeps only add: no attenuation. -/
theorem shear_add {R : Type*} [CommRing R] (a b : R) : shear a * shear b = shear (a + b) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [shear, Matrix.mul_apply, Fin.sum_univ_two, add_comm]

theorem shear_det {R : Type*} [CommRing R] (z : R) : (shear z).det = 1 := by
  simp [shear, Matrix.det_fin_two]

/-- Three alternating shears form a rotation (with `p = tan(θ/2)`). -/
theorem alternating_shears (p : ℝ) :
    !![1, -p; 0, 1] * !![1, 0; 2*p/(1+p^2), 1] * !![1, -p; 0, 1] =
      !![(1-p^2)/(1+p^2), -(2*p/(1+p^2)); 2*p/(1+p^2), (1-p^2)/(1+p^2)] := by
  have h : (1 + p^2) ≠ 0 := by positivity
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two] <;> field_simp <;> ring

/-! ## Theorem 5. The rotation is ω in F₄, and the 21 invariant directions -/

/-- Addition in F₄ (bitwise exclusive or of the two-bit labels). -/
def addF4 (x y : Label) : Label :=
  (![![0,1,2,3],![1,0,3,2],![2,3,0,1],![3,2,1,0]] : Label → Label → Label) x y

/-- Multiplication in F₄ = {0, 1, ω, ω²} encoded as 0, 1, 2, 3. -/
def mulF4 (x y : Label) : Label :=
  (![![0,0,0,0],![0,1,2,3],![0,2,3,1],![0,3,1,2]] : Label → Label → Label) x y

theorem F4_field :
    (∀ x y z : Label, mulF4 (mulF4 x y) z = mulF4 x (mulF4 y z)) ∧
    (∀ x y : Label, mulF4 x y = mulF4 y x) ∧
    (∀ x y z : Label, mulF4 x (addF4 y z) = addF4 (mulF4 x y) (mulF4 x z)) ∧
    (∀ x y z : Label, addF4 (addF4 x y) z = addF4 x (addF4 y z)) ∧
    (∀ x : Label, x ≠ 0 → ∃ y, mulF4 x y = 1) := by
  decide

/-- The order-three label cycle is multiplication by ω, and it is additive. -/
theorem cycle_is_omega (x : Label) : cycle x = mulF4 2 x := by
  fin_cases x <;> decide

theorem cycle_additive (x y : Label) : cycle (addF4 x y) = addF4 (cycle x) (cycle y) := by
  fin_cases x <;> fin_cases y <;> decide

/-- Away from the zero address the simultaneous cycle moves every address. -/
theorem cycle_free : ∀ x : Address, x ≠ (0,0,0) → cyAct x ≠ x ∧ cyAct (cyAct x) ≠ x := by
  decide

/-- Grade = position of the last nonzero digit (3 for the zero address). -/
def grade (x : Address) : ℕ :=
  if x.2.2 ≠ 0 then 2 else if x.2.1 ≠ 0 then 1 else if x.1 ≠ 0 then 0 else 3

theorem grade_counts :
    (Finset.univ.filter fun x : Address => grade x = 0).card = 3 ∧
    (Finset.univ.filter fun x : Address => grade x = 1).card = 12 ∧
    (Finset.univ.filter fun x : Address => grade x = 2).card = 48 := by
  decide

theorem cycle_preserves_grade : ∀ x : Address, grade (cyAct x) = grade x := by
  decide

/-- A numeric code to pick the least address of each orbit. -/
def code (x : Address) : ℕ := 16 * x.1.val + 4 * x.2.1.val + x.2.2.val

/-- An address is the representative of its (free) orbit when it has the least code. -/
def isRep (x : Address) : Bool :=
  decide (x ≠ (0,0,0)) && decide (code x < code (cyAct x)) &&
    decide (code x < code (cyAct (cyAct x)))

/-- The invariant directions per grade are 1, 4 and 16: the 21 points of PG(2,4). -/
theorem invariant_directions :
    (Finset.univ.filter fun x : Address => isRep x ∧ grade x = 0).card = 1 ∧
    (Finset.univ.filter fun x : Address => isRep x ∧ grade x = 1).card = 4 ∧
    (Finset.univ.filter fun x : Address => isRep x ∧ grade x = 2).card = 16 ∧
    (Finset.univ.filter fun x : Address => isRep x).card = 21 := by
  decide

/-- One entry of the 64-address Walsh matrix. -/
def H4e (a x : Address) : ℤ := H4 a.1 x.1 * H4 a.2.1 x.2.1 * H4 a.2.2 x.2.2

theorem H64_apply (a x : Address) : H64 a x = H4e a x := by
  simp [H64, Hm, H4e, Matrix.kroneckerMap_apply, mul_assoc]

/-- The orbit sum of three characters. -/
def orbitSum (a x : Address) : ℤ := H4e a x + H4e (cyAct a) x + H4e (cyAct (cyAct a)) x

/-- Each invariant mode is `4·𝟙[plane] − 1`: it takes only the values 3 and −1. -/
theorem orbit_sum_values :
    ∀ a : Address, a ≠ (0,0,0) → ∀ x : Address, orbitSum a x = 3 ∨ orbitSum a x = -1 := by
  decide

/-- … and the value 3 on exactly a 16-address plane. -/
theorem orbit_sum_plane :
    ∀ a : Address, a ≠ (0,0,0) →
      (Finset.univ.filter fun x : Address => orbitSum a x = 3).card = 16 := by
  decide

/-! ## Theorem 6. Completed-block accounting -/

theorem walsh_product (a : Address) (u v w : Label → ℤ) :
    (∑ x : Address, H4e a x * (u x.1 * v x.2.1 * w x.2.2)) =
      (∑ i, H4 a.1 i * u i) * (∑ j, H4 a.2.1 j * v j) * (∑ k, H4 a.2.2 k * w k) := by
  calc (∑ x : Address, H4e a x * (u x.1 * v x.2.1 * w x.2.2))
      = ∑ i, ∑ j, ∑ k, (H4 a.1 i * u i) * (H4 a.2.1 j * v j) * (H4 a.2.2 k * w k) := by
        simp only [Fintype.sum_prod_type, H4e]
        exact Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ =>
          Finset.sum_congr rfl fun k _ => by ring
    _ = ∑ i, ∑ j, (H4 a.1 i * u i) * (H4 a.2.1 j * v j) * ∑ k, (H4 a.2.2 k * w k) := by
        refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
        rw [Finset.mul_sum]
    _ = ∑ i, (H4 a.1 i * u i) * (∑ j, H4 a.2.1 j * v j) * ∑ k, (H4 a.2.2 k * w k) := by
        refine Finset.sum_congr rfl fun i _ => ?_
        rw [Finset.mul_sum, Finset.sum_mul]
    _ = (∑ i, H4 a.1 i * u i) * (∑ j, H4 a.2.1 j * v j) * (∑ k, H4 a.2.2 k * w k) := by
        rw [Finset.sum_mul, Finset.sum_mul]

theorem row_sum (i : Label) : (∑ j, H4 i j * 1) = if i = 0 then 4 else 0 := by
  fin_cases i <;> decide

/-- A completed face block (fixed first digit) has no Walsh detail below its level. -/
theorem face_block_detail (p : Label) (a : Address) (h : a.2.1 ≠ 0 ∨ a.2.2 ≠ 0) :
    (∑ x : Address, H4e a x * ((if x.1 = p then 1 else 0) * 1 * 1)) = 0 := by
  rw [walsh_product a (fun i => if i = p then 1 else 0) (fun _ => 1) (fun _ => 1),
    row_sum, row_sum]
  rcases h with h | h <;> simp [h]

/-- A completed channel block (fixed first two digits) has no finest-grade detail. -/
theorem channel_block_detail (p q : Label) (a : Address) (h : a.2.2 ≠ 0) :
    (∑ x : Address, H4e a x *
      ((if x.1 = p then 1 else 0) * (if x.2.1 = q then 1 else 0) * 1)) = 0 := by
  rw [walsh_product a (fun i => if i = p then 1 else 0) (fun j => if j = q then 1 else 0)
    (fun _ => 1), row_sum]
  simp [h]

/-- Walsh orthogonality on the 64 addresses. -/
theorem H4e_orthogonal (x y : Address) :
    (∑ a : Address, H4e a x * H4e a y) = if x = y then 64 else 0 := by
  have hs : ∀ a, H4e a x * H4e a y =
      H4e x a * ((H4 a.1 y.1) * (H4 a.2.1 y.2.1) * (H4 a.2.2 y.2.2)) := by
    intro a; simp only [H4e, H4_symm a.1 x.1, H4_symm a.2.1 x.2.1, H4_symm a.2.2 x.2.2]
  simp only [hs]
  rw [walsh_product x (fun i => H4 i y.1) (fun j => H4 j y.2.1) (fun k => H4 k y.2.2)]
  simp only [show ∀ r s : Label, (∑ i, H4 r i * H4 i s) = if r = s then 4 else 0 from
    fun r s => by rw [← local_walsh_orthogonal r s]; exact
      Finset.sum_congr rfl fun i _ => by rw [H4_symm i s]]
  obtain ⟨x1, x2, x3⟩ := x
  obtain ⟨y1, y2, y3⟩ := y
  by_cases h1 : x1 = y1 <;> by_cases h2 : x2 = y2 <;> by_cases h3 : x3 = y3 <;>
    simp [h1, h2, h3]

/-- For binary occupancy with total `A`: `c₀ = A` and `∑ c² = 64·A`, hence
`∑_{a≠0} c_a² = 64·A − A²`. -/
theorem binary_accounting (b : Address → ℤ) (hb : ∀ x, b x = 0 ∨ b x = 1) :
    (∑ x, H4e (0,0,0) x * b x) = ∑ x, b x ∧
    (∑ a, (∑ x, H4e a x * b x) ^ 2) = 64 * ∑ x, b x := by
  constructor
  · refine Finset.sum_congr rfl fun x _ => ?_
    have : H4e (0,0,0) x = 1 := by
      obtain ⟨i, j, k⟩ := x
      fin_cases i <;> fin_cases j <;> fin_cases k <;> decide
    rw [this, one_mul]
  · have hsq : ∀ x, b x * b x = b x := by
      intro x; rcases hb x with h | h <;> simp [h]
    calc (∑ a, (∑ x, H4e a x * b x) ^ 2)
        = ∑ a, ∑ x, ∑ y, (H4e a x * b x) * (H4e a y * b y) := by
          refine Finset.sum_congr rfl fun a _ => ?_
          rw [sq, Finset.sum_mul_sum]
      _ = ∑ x, ∑ y, b x * b y * ∑ a, H4e a x * H4e a y := by
          rw [Finset.sum_comm]
          refine Finset.sum_congr rfl fun x _ => ?_
          rw [Finset.sum_comm]
          refine Finset.sum_congr rfl fun y _ => ?_
          rw [Finset.mul_sum]
          exact Finset.sum_congr rfl fun a _ => by ring
      _ = ∑ x, b x * b x * 64 := by
          refine Finset.sum_congr rfl fun x _ => ?_
          simp only [H4e_orthogonal]
          simp
      _ = 64 * ∑ x, b x := by
          rw [Finset.mul_sum]
          refine Finset.sum_congr rfl fun x _ => ?_
          rw [hsq]; ring

theorem binary_detail_energy (b : Address → ℤ) (hb : ∀ x, b x = 0 ∨ b x = 1) :
    (∑ a ∈ Finset.univ.erase ((0,0,0) : Address), (∑ x, H4e a x * b x) ^ 2) =
      64 * (∑ x, b x) - (∑ x, b x) ^ 2 := by
  obtain ⟨h0, htot⟩ := binary_accounting b hb
  have := Finset.add_sum_erase (Finset.univ : Finset Address)
    (fun a => (∑ x, H4e a x * b x) ^ 2) (Finset.mem_univ (0,0,0))
  rw [htot, h0] at this
  linarith

/-! ## Theorem 7. Graded counts from the coupling polynomial -/

/-- The coupling polynomial and its capacity identity, for every `K`. -/
theorem coupling_capacity (K : ℤ) :
    (1 + K + K^2) * (1 - K + K^2) = 1 + K^2 + K^4 ∧
    1 + K^2 + K^4 = 1 + K^2 * (1 + K^2) := by
  constructor <;> ring

/-- The three grades of sizes 1, K, K² with K = 4. -/
abbrev Grade := Fin 1 ⊕ Fin 4 ⊕ Fin 16

/-- The abstract depth sign: +1, −1, +1 on the three grades. -/
def depthSign : Grade → ℤ
  | Sum.inl _ => 1
  | Sum.inr (Sum.inl _) => -1
  | Sum.inr (Sum.inr _) => 1

theorem graded_traces :
    (∑ _g : Grade, (1 : ℤ)) = 21 ∧
    (∑ g : Grade, (1 + depthSign g) / 2) = 17 ∧
    (∑ g : Grade, depthSign g) = 13 ∧
    Fintype.card ((Fin 1 × Fin 1) ⊕ (Fin 4 × Fin 4) ⊕ (Fin 16 × Fin 16)) = 273 := by
  refine ⟨by decide, by decide, by decide, by simp⟩

theorem coupling_values :
    (1 + 4 + 4^2 : ℤ) = 21 ∧ (1 + 4^2 : ℤ) = 17 ∧ (1 - 4 + 4^2 : ℤ) = 13 ∧
    (21 : ℤ) * 13 = 273 ∧ 1 + 16 * 17 = (273 : ℤ) ∧
    ((4 : ℤ)^3 - 1) / (4 - 1) = 21 ∧ ((16 : ℤ)^3 - 1) / (16 - 1) = 273 := by
  norm_num

/-! ## Theorem 8. Collective transmission -/

/-- The grade bridge restricted to the 21 invariant directions. -/
def bridge (t₁ t₂ t₃ : ℝ) : Matrix Grade Grade ℝ :=
  Matrix.diagonal fun g => match g with
    | Sum.inl _ => t₁
    | Sum.inr (Sum.inl _) => t₂
    | Sum.inr (Sum.inr _) => t₃

/-- `det(Tᵀ T) = t₁² t₂⁸ t₃³²`: each grade's gain is applied once, with its dimension. -/
theorem collective_determinant (t₁ t₂ t₃ : ℝ) :
    ((bridge t₁ t₂ t₃)ᵀ * bridge t₁ t₂ t₃).det = t₁^2 * t₂^8 * t₃^32 := by
  rw [bridge, Matrix.diagonal_transpose, Matrix.diagonal_mul_diagonal, Matrix.det_diagonal,
    Fintype.prod_sum_type, Fintype.prod_sum_type]
  simp only [Finset.prod_const, Finset.card_univ, Fintype.card_fin]
  ring

/-- With a common intensity `t² = α`, the collective response is `(17/13)·α²¹`. -/
theorem collective_response (t α : ℝ) (h : t^2 = α) :
    (17/13 : ℝ) * ((bridge t t t)ᵀ * bridge t t t).det = (17/13) * α^21 := by
  rw [collective_determinant, ← h]
  ring

/-- Symmetry does not select the determinant: the normalised trace is basis-invariant too,
equals 1 at the identity, and gives `t²`, not `t⁴²`. -/
theorem trace_versus_determinant (t : ℝ) :
    ((bridge t t t)ᵀ * bridge t t t).trace / 21 = t^2 ∧
    ((bridge t t t)ᵀ * bridge t t t).det = t^42 := by
  constructor
  · rw [bridge, Matrix.diagonal_transpose, Matrix.diagonal_mul_diagonal, Matrix.trace_diagonal,
      Fintype.sum_sum_type, Fintype.sum_sum_type]
    simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
    ring
  · rw [collective_determinant]; ring

/-! ## Theorems 9 and 10. Settlement witnesses -/

/-- Arithmetic certificate for the fixed-geometry vortex susceptibility
`u′ = 2k/(1 − hk)` at the inherited branch values (the matrices themselves are checked by
the Python verifier, not here). -/
theorem susceptibility_values :
    let k : ℚ := 42815 / 290521
    2 * k / (1 - (308/59) * k) = 5052170 / 3953719 ∧ 2 * k / (1 - 0 * k) = 85630 / 290521 := by
  norm_num

/-- Two children sharing one interface settle at the weighted mean, their fluxes balance,
and the registered energy is the parallel combination. -/
theorem two_child_registration (kA kB a b g : ℝ) (hA : 0 < kA) (hB : 0 < kB) :
    let gs := (kA*a + kB*b) / (kA + kB)
    kA * (gs - a) + kB * (gs - b) = 0 ∧
    kA * (g - a)^2 / 2 + kB * (g - b)^2 / 2 =
      kA * kB * (a - b)^2 / (2 * (kA + kB)) + (kA + kB) * (g - gs)^2 / 2 := by
  have h : kA + kB ≠ 0 := by positivity
  constructor
  · field_simp; ring
  · field_simp; ring

/-! ## Axiom audit -/

#print axioms blind_closure
#print axioms read_factorization
#print axioms Hm_sq
#print axioms three_sweeps
#print axioms sweeps_commute
#print axioms H64_sq
#print axioms cycle_self_adjoint
#print axioms sierpinski_four
#print axioms sierpinski_sixtyfour
#print axioms shear_add
#print axioms shear_det
#print axioms alternating_shears
#print axioms F4_field
#print axioms cycle_is_omega
#print axioms cycle_additive
#print axioms cycle_free
#print axioms grade_counts
#print axioms cycle_preserves_grade
#print axioms invariant_directions
#print axioms H64_apply
#print axioms orbit_sum_values
#print axioms orbit_sum_plane
#print axioms walsh_product
#print axioms face_block_detail
#print axioms channel_block_detail
#print axioms H4e_orthogonal
#print axioms binary_accounting
#print axioms binary_detail_energy
#print axioms coupling_capacity
#print axioms graded_traces
#print axioms coupling_values
#print axioms collective_determinant
#print axioms collective_response
#print axioms trace_versus_determinant
#print axioms susceptibility_values
#print axioms two_child_registration

end RecursiveFieldClosureResponse
