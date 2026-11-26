import RecursiveTriforceClosure
import Mathlib

/-! # The intrinsic tetrahedral geometry of the collective flywheel

Finite incidence identities, their real consequences, and the actual core
parity split. No dynamical or gravitational axiom is introduced. The upstream
half-space theorem is reached through RecursiveTriforceClosure. Finite matrix
identities are proved entry by entry with `fin_cases` and `norm_num`; see
LEAN_AUDIT.md for the kernel build and axiom audit.
-/
namespace FlywheelTetradGeometry

open scoped BigOperators
open Matrix
set_option maxRecDepth 4096
set_option maxHeartbeats 0
-- The generic simp sets below list structural lemmas some identities do not need.
set_option linter.unusedSimpArgs false

abbrev Label := Fin 4
abbrev Edge := Fin 6
abbrev Tile := Fin 12
abbrev CoreNode := Fin 8

/-! ## 1. Abstract incidence: no spatial coordinates are used in these definitions. -/
def B {K : Type*} [Ring K] : Matrix Label Edge K :=
  !![-1, -1, -1, 0, 0, 0;
    1, 0, 0, -1, -1, 0;
    0, 1, 0, 1, 0, -1;
    0, 0, 1, 0, 1, 1]

def D {K : Type*} [Ring K] : Matrix Edge Label K :=
  !![0, 0, 1, -1;
    0, -1, 0, 1;
    0, 1, -1, 0;
    1, 0, 0, -1;
    -1, 0, 1, 0;
    1, -1, 0, 0]

def R {K : Type*} [Ring K] : Matrix Label Tile K :=
  !![1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0;
    0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0;
    0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0;
    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]

def Q {K : Type*} [Ring K] : Matrix Label Tile K :=
  !![0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0;
    1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0;
    0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1;
    0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]

def G {K : Type*} [Ring K] : Matrix Label Label K :=
  !![3, -1, -1, -1;
    -1, 3, -1, -1;
    -1, -1, 3, -1;
    -1, -1, -1, 3]

def A {K : Type*} [Ring K] : Matrix Tile Edge K :=
  !![1, 0, 0, 0, 0, 0;
    0, 1, 0, 0, 0, 0;
    0, 0, 1, 0, 0, 0;
    -1, 0, 0, 0, 0, 0;
    0, 0, 0, 1, 0, 0;
    0, 0, 0, 0, 1, 0;
    0, -1, 0, 0, 0, 0;
    0, 0, 0, -1, 0, 0;
    0, 0, 0, 0, 0, 1;
    0, 0, -1, 0, 0, 0;
    0, 0, 0, 0, -1, 0;
    0, 0, 0, 0, 0, -1]

def N {K : Type*} [Ring K] : Matrix CoreNode Tile K :=
  !![-1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0;
    0, 0, 0, -1, -1, -1, 0, 0, 0, 0, 0, 0;
    0, 0, 0, 0, 0, 0, -1, -1, -1, 0, 0, 0;
    0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1;
    0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0;
    1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0;
    0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1;
    0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]

def invCore {K : Type*} [Ring K] : Matrix Tile Tile K :=
  !![0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0;
    0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0;
    0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0;
    -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0;
    0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0;
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0;
    0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0;
    0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0;
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1;
    0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0;
    0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0;
    0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0]

def ones {K : Type*} [Ring K] : Label → K := fun _ => 1

def rowProjector : Matrix Tile Tile ℚ :=
  1 - (1/3 : ℚ) • ((R : Matrix Label Tile ℚ)ᵀ * (R : Matrix Label Tile ℚ))

def C : Matrix Label Tile ℚ := (Q : Matrix Label Tile ℚ) * rowProjector

def P : Matrix Label Label ℚ := (1/4 : ℚ) • G

def Z : Matrix Tile Label ℚ := (3/8 : ℚ) • Cᵀ

/-- Rescaled isometry: L₀ Cᵀ = D. Its normalized real form is described below. -/
def L0 : Matrix Edge Tile ℚ := (3/8 : ℚ) • ((D : Matrix Edge Label ℚ) * C)

/-! Explicit rational forms. Each is proved equal to its definition below, so the
    later identities are checked on the defined matrices, not on assumed tables. -/
def PrX : Matrix Tile Tile ℚ :=
  !![2/3, -1/3, -1/3, 0, 0, 0, 0, 0, 0, 0, 0, 0;
    -1/3, 2/3, -1/3, 0, 0, 0, 0, 0, 0, 0, 0, 0;
    -1/3, -1/3, 2/3, 0, 0, 0, 0, 0, 0, 0, 0, 0;
    0, 0, 0, 2/3, -1/3, -1/3, 0, 0, 0, 0, 0, 0;
    0, 0, 0, -1/3, 2/3, -1/3, 0, 0, 0, 0, 0, 0;
    0, 0, 0, -1/3, -1/3, 2/3, 0, 0, 0, 0, 0, 0;
    0, 0, 0, 0, 0, 0, 2/3, -1/3, -1/3, 0, 0, 0;
    0, 0, 0, 0, 0, 0, -1/3, 2/3, -1/3, 0, 0, 0;
    0, 0, 0, 0, 0, 0, -1/3, -1/3, 2/3, 0, 0, 0;
    0, 0, 0, 0, 0, 0, 0, 0, 0, 2/3, -1/3, -1/3;
    0, 0, 0, 0, 0, 0, 0, 0, 0, -1/3, 2/3, -1/3;
    0, 0, 0, 0, 0, 0, 0, 0, 0, -1/3, -1/3, 2/3]

def CX : Matrix Label Tile ℚ :=
  !![0, 0, 0, 2/3, -1/3, -1/3, 2/3, -1/3, -1/3, 2/3, -1/3, -1/3;
    2/3, -1/3, -1/3, 0, 0, 0, -1/3, 2/3, -1/3, -1/3, 2/3, -1/3;
    -1/3, 2/3, -1/3, -1/3, 2/3, -1/3, 0, 0, 0, -1/3, -1/3, 2/3;
    -1/3, -1/3, 2/3, -1/3, -1/3, 2/3, -1/3, -1/3, 2/3, 0, 0, 0]

def ZX : Matrix Tile Label ℚ :=
  !![0, 1/4, -1/8, -1/8;
    0, -1/8, 1/4, -1/8;
    0, -1/8, -1/8, 1/4;
    1/4, 0, -1/8, -1/8;
    -1/8, 0, 1/4, -1/8;
    -1/8, 0, -1/8, 1/4;
    1/4, -1/8, 0, -1/8;
    -1/8, 1/4, 0, -1/8;
    -1/8, -1/8, 0, 1/4;
    1/4, -1/8, -1/8, 0;
    -1/8, 1/4, -1/8, 0;
    -1/8, -1/8, 1/4, 0]

def L0X : Matrix Edge Tile ℚ :=
  !![0, 3/8, -3/8, 0, 3/8, -3/8, 1/8, 1/8, -1/4, -1/8, -1/8, 1/4;
    -3/8, 0, 3/8, -1/8, -1/8, 1/4, 0, -3/8, 3/8, 1/8, -1/4, 1/8;
    3/8, -3/8, 0, 1/8, -1/4, 1/8, -1/8, 1/4, -1/8, 0, 3/8, -3/8;
    1/8, 1/8, -1/4, 3/8, 0, -3/8, 3/8, 0, -3/8, 1/4, -1/8, -1/8;
    -1/8, 1/4, -1/8, -3/8, 3/8, 0, -1/4, 1/8, 1/8, -3/8, 0, 3/8;
    -1/4, 1/8, 1/8, 1/4, -1/8, -1/8, 3/8, -3/8, 0, 3/8, -3/8, 0]

theorem rowProjector_eq : rowProjector = PrX := by
  ext i j
  simp only [rowProjector, Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [PrX, R, Matrix.one_apply, nsmul_eq_mul]

theorem C_eq : C = CX := by
  ext i j
  simp only [C, rowProjector_eq, Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [PrX, CX, Q, Matrix.one_apply, nsmul_eq_mul]

theorem Z_eq : Z = ZX := by
  ext i j
  simp only [Z, C_eq, Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [CX, ZX, Matrix.one_apply, nsmul_eq_mul]

theorem L0_eq : L0 = L0X := by
  ext i j
  simp only [L0, C_eq, Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [CX, L0X, D, Matrix.one_apply, nsmul_eq_mul]

/-! Closed finite equalities are proved entrywise by kernel `decide`. -/
theorem incidence_gram : (B : Matrix Label Edge ℚ) * (B : Matrix Label Edge ℚ)ᵀ = (G : Matrix Label Label ℚ) := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [B, G, Matrix.one_apply, nsmul_eq_mul]

theorem cycle_gram : (D : Matrix Edge Label ℚ)ᵀ * (D : Matrix Edge Label ℚ) = (G : Matrix Label Label ℚ) := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [D, G, Matrix.one_apply, nsmul_eq_mul]

theorem boundary_boundary : (B : Matrix Label Edge ℚ) * (D : Matrix Edge Label ℚ) = 0 := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [B, D, Matrix.one_apply, nsmul_eq_mul]

theorem cycle_projector : (D : Matrix Edge Label ℚ) * (D : Matrix Edge Label ℚ)ᵀ +
    (B : Matrix Label Edge ℚ)ᵀ * (B : Matrix Label Edge ℚ) = 4 • (1 : Matrix Edge Edge ℚ) := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [D, B, Matrix.add_apply, Matrix.one_apply, nsmul_eq_mul, Matrix.one_apply, nsmul_eq_mul]

theorem gram_projector : P * P = P := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [P, G, Matrix.one_apply, nsmul_eq_mul]

theorem cycle_zero_sum : (D : Matrix Edge Label ℚ).mulVec ones = 0 := by
  funext i
  fin_cases i <;> norm_num [D, ones, mulVec, dotProduct, Fin.sum_univ_succ]

/-- Real cycle reconstruction, including the converse to boundary-of-boundary.
    This is the pointwise projector identity used to deduce image/kernel equality. -/
theorem real_cycle_projector (a b : Edge) :
    ((D : Matrix Edge Label ℝ) * (D : Matrix Edge Label ℝ)ᵀ +
      (B : Matrix Label Edge ℝ)ᵀ * (B : Matrix Label Edge ℝ)) a b =
      (4 • (1 : Matrix Edge Edge ℝ)) a b := by
  simp only [Matrix.add_apply, Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply,
    Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases a <;> fin_cases b <;> norm_num [D, B, Matrix.one_apply, nsmul_eq_mul]

/-- Gram equality with the existing real tetrad, not an independent frame axiom. -/
theorem real_cycle_tetrad_gram (a b : Label) :
    ((D : Matrix Edge Label ℝ)ᵀ * (D : Matrix Edge Label ℝ)) a b =
      (ForcedTetrahedralFrame.Mmatᵀ * ForcedTetrahedralFrame.Mmat) a b := by
  rw [ForcedTetrahedralFrame.MtM_apply]
  fin_cases a <;> fin_cases b <;>
    norm_num [D, Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_succ]

/-! ## 2. The independent row-closed column read and exact right inverse -/
theorem row_gram : (R : Matrix Label Tile ℚ) * (R : Matrix Label Tile ℚ)ᵀ = 3 • (1 : Matrix Label Label ℚ) := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [R, Matrix.one_apply, nsmul_eq_mul, Matrix.one_apply, nsmul_eq_mul]

theorem row_projector_idempotent : rowProjector * rowProjector = rowProjector := by
  rw [rowProjector_eq]
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [PrX, Matrix.one_apply, nsmul_eq_mul]

theorem row_projector_symmetric : rowProjectorᵀ = rowProjector := by
  rw [rowProjector_eq]
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [PrX, Matrix.one_apply, nsmul_eq_mul]

theorem row_projector_closed : (R : Matrix Label Tile ℚ) * rowProjector = 0 := by
  rw [rowProjector_eq]
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [R, PrX, Matrix.one_apply, nsmul_eq_mul]

theorem column_gram : C * Cᵀ = (2/3 : ℚ) • (G : Matrix Label Label ℚ) := by
  rw [C_eq]
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [CX, G, Matrix.one_apply, nsmul_eq_mul]

theorem read_right_inverse : (Q : Matrix Label Tile ℚ) * Z = P := by
  rw [Z_eq]
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [Q, ZX, P, G, Matrix.one_apply, nsmul_eq_mul]

theorem read_row_closed : (R : Matrix Label Tile ℚ) * Z = 0 := by
  rw [Z_eq]
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [R, ZX, Matrix.one_apply, nsmul_eq_mul]

theorem read_norm : Zᵀ * Z = (3/8 : ℚ) • P := by
  rw [Z_eq]
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [ZX, P, G, Matrix.one_apply, nsmul_eq_mul]

theorem read_orthogonality : Zᵀ = (3/8 : ℚ) • ((Q : Matrix Label Tile ℚ) - (1/3 : ℚ) •
    ((Q : Matrix Label Tile ℚ) * (R : Matrix Label Tile ℚ)ᵀ * (R : Matrix Label Tile ℚ))) := by
  rw [Z_eq]
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [ZX, Q, R, Matrix.sub_apply, Matrix.one_apply, nsmul_eq_mul]

theorem isometry_maps_frame : L0 * Cᵀ = (D : Matrix Edge Label ℚ) := by
  rw [L0_eq, C_eq]
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [L0X, CX, D, Matrix.one_apply, nsmul_eq_mul]

theorem isometry_source_projector : L0ᵀ * L0 = (9/16 : ℚ) • (Cᵀ * C) := by
  rw [L0_eq, C_eq]
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [L0X, CX, Matrix.one_apply, nsmul_eq_mul]

theorem isometry_target_projector : L0 * L0ᵀ = (3/8 : ℚ) • ((D : Matrix Edge Label ℚ) * (D : Matrix Edge Label ℚ)ᵀ) := by
  rw [L0_eq]
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [L0X, D, Matrix.one_apply, nsmul_eq_mul]

/-- For a real zero-sum read q, the analytic Gram normalization is 3/2.
    The rational Gram above is exact; this lemma verifies the square-root factor. -/
theorem normalizing_factor : (Real.sqrt (3/2 : ℝ))^2 * (2/3 : ℝ) = 1 := by
  rw [Real.sq_sqrt (by norm_num : 0 ≤ (3/2 : ℝ))]
  norm_num

/-- The real column read, written out in the same twelve-tile order. -/
noncomputable def CReal : Matrix Label Tile ℝ :=
  !![0, 0, 0, (2/3), (-1/3), (-1/3), (2/3), (-1/3), (-1/3), (2/3), (-1/3), (-1/3);
    (2/3), (-1/3), (-1/3), 0, 0, 0, (-1/3), (2/3), (-1/3), (-1/3), (2/3), (-1/3);
    (-1/3), (2/3), (-1/3), (-1/3), (2/3), (-1/3), 0, 0, 0, (-1/3), (-1/3), (2/3);
    (-1/3), (-1/3), (2/3), (-1/3), (-1/3), (2/3), (-1/3), (-1/3), (2/3), 0, 0, 0]

noncomputable def rowProjectorReal : Matrix Tile Tile ℝ :=
  1 - (1/3 : ℝ) • ((R : Matrix Label Tile ℝ)ᵀ * (R : Matrix Label Tile ℝ))

/-- The explicit entries are the actual projected column read. -/
theorem real_column_definition (i : Label) (t : Tile) :
    CReal i t = ((Q : Matrix Label Tile ℝ) * rowProjectorReal) i t := by
  simp only [rowProjectorReal, Matrix.mul_apply, Matrix.sub_apply, Matrix.smul_apply, smul_eq_mul,
    Matrix.transpose_apply, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases t <;> norm_num [CReal, Q, R, Matrix.one_apply]

theorem real_column_gram (i j : Label) :
    (CReal * CRealᵀ) i j = (2/3 : ℝ) * (G : Matrix Label Label ℝ) i j := by
  fin_cases i <;> fin_cases j <;>
    norm_num [CReal, G, Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_succ]

noncomputable def FReal : Matrix Tile Label ℝ :=
  Matrix.of fun t i => Real.sqrt (3/2 : ℝ) * CReal i t

/-- The actual normalized real flywheel and cycle frames have the same Gram. -/
theorem common_real_gram (i j : Label) :
    (FRealᵀ * FReal) i j = ((D : Matrix Edge Label ℝ)ᵀ * (D : Matrix Edge Label ℝ)) i j := by
  have hC := real_column_gram i j
  rw [Matrix.mul_apply] at hC
  simp only [Matrix.transpose_apply] at hC
  have hD : ((D : Matrix Edge Label ℝ)ᵀ * (D : Matrix Edge Label ℝ)) i j =
      (G : Matrix Label Label ℝ) i j := by
    fin_cases i <;> fin_cases j <;>
      norm_num [D, G, Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_succ]
  rw [hD, Matrix.mul_apply]
  simp only [Matrix.transpose_apply, FReal, Matrix.of_apply]
  calc
    (∑ t : Tile, (Real.sqrt (3/2 : ℝ) * CReal i t) *
        (Real.sqrt (3/2 : ℝ) * CReal j t)) =
      (Real.sqrt (3/2 : ℝ))^2 * ∑ t : Tile, CReal i t * CReal j t := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro t _
        ring
    _ = (G : Matrix Label Label ℝ) i j := by
      rw [hC, Real.sq_sqrt (by norm_num : 0 ≤ (3/2 : ℝ))]
      ring

/-- Both independently constructed frames recover the previously proved tetrad Gram. -/
theorem flywheel_tetrad_gram (i j : Label) :
    (FRealᵀ * FReal) i j =
      (ForcedTetrahedralFrame.Mmatᵀ * ForcedTetrahedralFrame.Mmat) i j :=
  (common_real_gram i j).trans (real_cycle_tetrad_gram i j)

/-! ## 3. Full label symmetry, with the orientation sign -/
def edgeLabel : Edge → Label × Label := ![(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]

def tileLabel : Tile → Label × Label := ![(0,1), (0,2), (0,3), (1,0), (1,2), (1,3), (2,0), (2,1), (2,3), (3,0), (3,1), (3,2)]

def edgeCoeff (a b i : Label) : ℚ :=
  ∑ e : Edge, if edgeLabel e = (a,b) then (D : Matrix Edge Label ℚ) e i
    else if edgeLabel e = (b,a) then -(D : Matrix Edge Label ℚ) e i else 0

def tileCoeff (i a b : Label) : ℚ :=
  ∑ t : Tile, if tileLabel t = (a,b) then C i t else 0

abbrev permTable := RecursiveTriforceClosure.permTable
abbrev permEven := RecursiveTriforceClosure.permEven

def parity (p : Fin 24) : ℚ := if permEven p then 1 else -1

/-- Closed value of a tile coefficient, times three: the column read of tile (a,b)
    is 2/3 when b = i, 0 when a = i, and −1/3 otherwise; there is no tile (a,a). -/
def tc3 (i a b : Label) : ℤ :=
  if a = b then 0 else (if b = i then 3 else 0) - (if a = i then 0 else 1)

theorem tileCoeff_eq (i a b : Label) : tileCoeff i a b = (tc3 i a b : ℚ) / 3 := by
  rw [tileCoeff, C_eq]
  fin_cases i <;> fin_cases a <;> fin_cases b <;>
    norm_num [tc3, CX, tileLabel, Fin.sum_univ_succ]

/-- Closed table of oriented cycle coefficients, indexed (a, b, i). -/
def epsT : Label → Label → Label → ℤ :=
  ![![![0, 0, 0, 0], ![0, 0, 1, -1], ![0, -1, 0, 1], ![0, 1, -1, 0]],
    ![![0, 0, -1, 1], ![0, 0, 0, 0], ![1, 0, 0, -1], ![-1, 0, 1, 0]],
    ![![0, 1, 0, -1], ![-1, 0, 0, 1], ![0, 0, 0, 0], ![1, -1, 0, 0]],
    ![![0, -1, 1, 0], ![1, 0, -1, 0], ![-1, 1, 0, 0], ![0, 0, 0, 0]]]

theorem edgeCoeff_eq (a b i : Label) : edgeCoeff a b i = (epsT a b i : ℚ) := by
  fin_cases a <;> fin_cases b <;> fin_cases i <;>
    norm_num [edgeCoeff, epsT, D, edgeLabel, Fin.sum_univ_succ]

/-- The closed table changes by the permutation sign under all 24 relabelings. -/
theorem epsT_covariant (p : Fin 24) : ∀ a b i : Label,
    epsT (permTable p a) (permTable p b) (permTable p i) =
      (if permEven p then 1 else -1) * epsT a b i := by
  fin_cases p <;> decide

/-- All 24 relabelings act without a sign on the column frame. -/
theorem column_covariant (p : Fin 24) (i a b : Label) :
    tileCoeff (permTable p i) (permTable p a) (permTable p b) = tileCoeff i a b := by
  have hinj : Function.Injective (permTable p) := fun a b h =>
    RecursiveTriforceClosure.table_injective p a b h
  rw [tileCoeff_eq, tileCoeff_eq]
  simp only [tc3, hinj.eq_iff]

/-- Oriented cycle coefficients acquire the permutation sign. -/
theorem cycle_covariant (p : Fin 24) (i a b : Label) :
    edgeCoeff (permTable p a) (permTable p b) (permTable p i) =
      parity p * edgeCoeff a b i := by
  rw [edgeCoeff_eq, edgeCoeff_eq, epsT_covariant p a b i, parity]
  split_ifs <;> simp

/-- Completeness of the permutation test is inherited, not assumed. -/
theorem all_relabelings (q : Label → Label) (h : Function.Injective q) :
    ∃ p : Fin 24, ∀ i : Label, permTable p i = q i :=
  RecursiveTriforceClosure.table_complete q h

/-! ## 4. The actual twelve-edge octahedral core -/
theorem inversion_squared : (invCore : Matrix Tile Tile ℚ) * (invCore : Matrix Tile Tile ℚ) = 1 := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [invCore, Matrix.one_apply, Matrix.one_apply, nsmul_eq_mul]

theorem even_embedding : (invCore : Matrix Tile Tile ℚ) * (A : Matrix Tile Edge ℚ) = (A : Matrix Tile Edge ℚ) := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [invCore, A, Matrix.one_apply, nsmul_eq_mul]

theorem even_embedding_norm : (A : Matrix Tile Edge ℚ)ᵀ * (A : Matrix Tile Edge ℚ) = 2 • (1 : Matrix Edge Edge ℚ) := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [A, Matrix.one_apply, nsmul_eq_mul, Matrix.one_apply, nsmul_eq_mul]

theorem even_cycles_are_core_cycles :
    (N : Matrix CoreNode Tile ℚ) * (A : Matrix Tile Edge ℚ) * (D : Matrix Edge Label ℚ) = 0 := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;>
    norm_num [N, A, D, Matrix.one_apply, nsmul_eq_mul]

/-- The core current has zero diagonal; row sums express conservation.
    In either transpose sector the column sums then vanish as well. -/
def RowClosed (I : Matrix Label Label ℝ) : Prop := ∀ i, ∑ j, I i j = 0

def ZeroDiag (I : Matrix Label Label ℝ) : Prop := ∀ i, I i i = 0

def evenArray (a b c : ℝ) : Matrix Label Label ℝ :=
  !![0,a,b,-a-b; -a,0,c,a-c; -b,-c,0,b+c; a+b,c-a,-b-c,0]

def oddArray (a b : ℝ) : Matrix Label Label ℝ :=
  !![0,a,b,-a-b; a,0,-a-b,b; b,-a-b,0,a; -a-b,b,a,0]

/-- Every even divergence-free core array is uniquely determined by three entries.
    Even refers to signed transpose inversion, not to ordinary transpose. -/
theorem even_parametrization (I : Matrix Label Label ℝ)
    (hz : ZeroDiag I) (hr : RowClosed I) (ha : ∀ i j, I i j = -I j i) :
    I = evenArray (I 0 1) (I 0 2) (I 1 2) := by
  have h0 := hr 0
  have h1 := hr 1
  have h2 := hr 2
  simp only [Fin.sum_univ_four] at h0 h1 h2
  have d0 := hz 0
  have d1 := hz 1
  have d2 := hz 2
  have d3 := hz 3
  have a10 := ha 1 0
  have a20 := ha 2 0
  have a30 := ha 3 0
  have a21 := ha 2 1
  have a31 := ha 3 1
  have a32 := ha 3 2
  ext i j
  fin_cases i <;> fin_cases j <;> simp [evenArray] <;> linarith

/-- Every odd divergence-free core array is uniquely determined by two entries. -/
theorem odd_parametrization (I : Matrix Label Label ℝ)
    (hz : ZeroDiag I) (hr : RowClosed I) (ha : ∀ i j, I i j = I j i) :
    I = oddArray (I 0 1) (I 0 2) := by
  have h0 := hr 0
  have h1 := hr 1
  have h2 := hr 2
  have h3 := hr 3
  simp only [Fin.sum_univ_four] at h0 h1 h2 h3
  have d0 := hz 0
  have d1 := hz 1
  have d2 := hz 2
  have d3 := hz 3
  have a10 := ha 1 0
  have a20 := ha 2 0
  have a30 := ha 3 0
  have a21 := ha 2 1
  have a31 := ha 3 1
  have a32 := ha 3 2
  ext i j
  fin_cases i <;> fin_cases j <;> simp [oddArray] <;> linarith

theorem even_family (a b c : ℝ) :
    ZeroDiag (evenArray a b c) ∧ RowClosed (evenArray a b c) ∧
    (∀ i j, evenArray a b c i j = -evenArray a b c j i) := by
  refine ⟨?_, ?_, ?_⟩
  · intro i; fin_cases i <;> simp [evenArray]
  · intro i; fin_cases i <;> simp [evenArray, Fin.sum_univ_succ]; ring
  · intro i j; fin_cases i <;> fin_cases j <;> simp [evenArray] <;> ring

theorem odd_family (a b : ℝ) :
    ZeroDiag (oddArray a b) ∧ RowClosed (oddArray a b) ∧
    (∀ i j, oddArray a b i j = oddArray a b j i) := by
  refine ⟨?_, ?_, ?_⟩
  · intro i; fin_cases i <;> simp [oddArray]
  · intro i; fin_cases i <;> simp [oddArray, Fin.sum_univ_succ] <;> ring
  · intro i j; fin_cases i <;> fin_cases j <;> simp [oddArray]

theorem even_parameters_unique (a b c a' b' c' : ℝ)
    (h : evenArray a b c = evenArray a' b' c') : a=a' ∧ b=b' ∧ c=c' := by
  have h1 := congrFun (congrFun h 0) 1
  have h2 := congrFun (congrFun h 0) 2
  have h3 := congrFun (congrFun h 1) 2
  simpa [evenArray] using And.intro h1 (And.intro h2 h3)

theorem odd_parameters_unique (a b a' b' : ℝ)
    (h : oddArray a b = oddArray a' b') : a=a' ∧ b=b' := by
  have h1 := congrFun (congrFun h 0) 1
  have h2 := congrFun (congrFun h 0) 2
  simpa [oddArray] using And.intro h1 h2

/-- Every zero-diagonal core with both row and column conservation splits
    into the antisymmetric and symmetric families (the 3+2 decomposition). -/
theorem core_decomposition (I : Matrix Label Label ℝ) (hz : ZeroDiag I)
    (hr : RowClosed I) (hc : ∀ j, ∑ i, I i j = 0) :
    ∃ a b c d e : ℝ, I = evenArray a b c + oddArray d e := by
  let E : Matrix Label Label ℝ := Matrix.of fun i j => (I i j-I j i)/2
  let S : Matrix Label Label ℝ := Matrix.of fun i j => (I i j+I j i)/2
  have ez : ZeroDiag E := by intro i; simp [E]
  have sz : ZeroDiag S := by intro i; simp [S, hz i]
  have er : RowClosed E := by
    intro i
    simp only [E, Matrix.of_apply, div_eq_mul_inv, ← Finset.sum_mul,
      Finset.sum_sub_distrib, hr i, hc i, sub_self, zero_mul]
  have sr : RowClosed S := by
    intro i
    simp only [S, Matrix.of_apply, div_eq_mul_inv, ← Finset.sum_mul,
      Finset.sum_add_distrib, hr i, hc i, add_zero, zero_mul]
  have ea : ∀ i j, E i j = -E j i := by
    intro i j; simp [E]; ring
  have sa : ∀ i j, S i j = S j i := by
    intro i j; simp [S]; ring
  refine ⟨E 0 1,E 0 2,E 1 2,S 0 1,S 0 2,?_⟩
  rw [← even_parametrization E ez er ea, ← odd_parametrization S sz sr sa]
  apply Matrix.ext
  intro i j
  simp [E,S]; ring

/-! ## 5. Common phase wedge and current reconstruction -/

def wedge (x y : Label → ℝ) (i j : Label) : ℝ := x i * y j - y i * x j

theorem wedge_row_closed (x y : Label → ℝ)
    (hx : ∑ i, x i = 0) (hy : ∑ i, y i = 0) (i : Label) :
    ∑ j, wedge x y i j = 0 := by
  simp only [wedge, Finset.sum_sub_distrib, ← Finset.mul_sum, hx, hy, mul_zero, sub_zero]

/-- Explicit three-coordinate reconstruction of the six oriented edge currents. -/
def edgeCycle (a b c : ℝ) : Edge → ℝ := ![a,b,-a-b,c,a-c,b+c]

theorem cycle_reconstruction (a b c : ℝ) (e : Edge) :
    (∑ i : Label, (D : Matrix Edge Label ℝ) e i *
      (∑ f : Edge, (D : Matrix Edge Label ℝ) f i * edgeCycle a b c f)) =
      4 * edgeCycle a b c e := by
  fin_cases e <;> simp [D, edgeCycle, Fin.sum_univ_succ] <;> ring

/-- All six pairwise wedge entries of a zero-sum phase obey the core parametrization. -/
theorem wedge_core (x y : Label → ℝ) (hx : ∑ i, x i = 0) (hy : ∑ i, y i = 0) :
    (fun i j => wedge x y i j : Matrix Label Label ℝ) =
      evenArray (wedge x y 0 1) (wedge x y 0 2) (wedge x y 1 2) := by
  apply even_parametrization
  · intro i; simp [wedge]; ring
  · intro i; exact wedge_row_closed x y hx hy i
  · intro i j; simp [wedge]; ring

/-- Real and imaginary parts of Im(conj(a)*b); the row shift cancels. -/
def alt (a b : ℝ × ℝ) : ℝ := a.1*b.2-a.2*b.1

def addP (a b : ℝ × ℝ) : ℝ × ℝ := (a.1+b.1,a.2+b.2)

def mulP (a b : ℝ × ℝ) : ℝ × ℝ := (a.1*b.1-a.2*b.2,a.1*b.2+a.2*b.1)

def cyc (a b c : ℝ × ℝ) : ℝ := alt a b + alt b c + alt c a

theorem common_shift_cancels (m v a b c : ℝ × ℝ) :
    cyc (addP m (mulP v a)) (addP m (mulP v b)) (addP m (mulP v c)) =
      (v.1^2+v.2^2) * cyc a b c := by
  simp [cyc, alt, addP, mulP]
  ring

theorem common_core_gain (w a b : ℝ × ℝ) :
    alt (mulP w a) (mulP w b) = (w.1^2+w.2^2) * alt a b := by
  simp [alt, mulP]
  ring

/-- Undivided current relation, valid at zero winding as well. -/
theorem physical_current_identity (rho v2 w2 a b c : ℝ) (e : Edge) :
    v2 * (2*rho^2*w2*edgeCycle a b c e) =
      (3/4 : ℝ)*w2 * (∑ i : Label, (D : Matrix Edge Label ℝ) e i *
        ((2*rho^2*v2/3) * ∑ f : Edge, (D : Matrix Edge Label ℝ) f i * edgeCycle a b c f)) := by
  fin_cases e <;> simp [D, edgeCycle, Fin.sum_univ_succ] <;> ring

/-! ## 6. The inherited spatial realization -/

theorem positive_hull :
    HalfSpaceTwoBoundedRegions.TetB = {p | ∃ w : Fin 4 → ℝ,
      (∀ a, 0 ≤ w a) ∧ ∑ a, w a = 1 ∧
      p = ∑ a, w a • ForcedTetrahedralFrame.Mcol a} :=
  HalfSpaceTwoBoundedRegions.TetB_eq_hull

theorem negative_hull :
    HalfSpaceTwoBoundedRegions.TetA = {p | ∃ w : Fin 4 → ℝ,
      (∀ a, 0 ≤ w a) ∧ ∑ a, w a = 1 ∧
      p = ∑ a, w a • (-ForcedTetrahedralFrame.Mcol a)} :=
  HalfSpaceTwoBoundedRegions.TetA_eq_hull

theorem shared_octahedron :
    HalfSpaceTwoBoundedRegions.TetA ∩ HalfSpaceTwoBoundedRegions.TetB =
      {p | |p 0| + |p 1| + |p 2| ≤ 1} :=
  HalfSpaceTwoBoundedRegions.inter_eq_octahedron.2

/-- The six off-diagonal entries determine the six diagonal edge weights. -/
def weightedGram (w : Edge → ℝ) (i j : Label) : ℝ :=
  ∑ e : Edge, (D : Matrix Edge Label ℝ) e i * w e * D e j

theorem weighted_gram_entries (w : Edge → ℝ) :
    weightedGram w 0 1 = -w 5 ∧ weightedGram w 0 2 = -w 4 ∧
    weightedGram w 0 3 = -w 3 ∧ weightedGram w 1 2 = -w 2 ∧
    weightedGram w 1 3 = -w 1 ∧ weightedGram w 2 3 = -w 0 := by
  simp [weightedGram, D, Fin.sum_univ_succ]

/-- The six midpoint vectors are the three signed coordinate axes. Here the
    table uses twice the midpoint, so there is no division in the certificate. -/
def twiceMidpoint : Edge → Fin 3 → ℝ :=
  ![![2,0,0],![0,2,0],![0,0,2],![0,0,-2],![0,-2,0],![-2,0,0]]

theorem inherited_midpoints (e : Edge) (d : Fin 3) :
    ForcedTetrahedralFrame.Mmat d (edgeLabel e).1 +
      ForcedTetrahedralFrame.Mmat d (edgeLabel e).2 = twiceMidpoint e d := by
  fin_cases e <;> fin_cases d <;>
    norm_num [ForcedTetrahedralFrame.Mmat, edgeLabel, twiceMidpoint]

/-! ## Axiom reports -/
#print axioms incidence_gram
#print axioms cycle_gram
#print axioms boundary_boundary
#print axioms cycle_projector
#print axioms gram_projector
#print axioms cycle_zero_sum
#print axioms real_cycle_projector
#print axioms real_cycle_tetrad_gram
#print axioms row_gram
#print axioms row_projector_idempotent
#print axioms row_projector_symmetric
#print axioms row_projector_closed
#print axioms column_gram
#print axioms read_right_inverse
#print axioms read_row_closed
#print axioms read_norm
#print axioms read_orthogonality
#print axioms isometry_maps_frame
#print axioms isometry_source_projector
#print axioms isometry_target_projector
#print axioms normalizing_factor
#print axioms column_covariant
#print axioms cycle_covariant
#print axioms all_relabelings
#print axioms inversion_squared
#print axioms even_embedding
#print axioms even_embedding_norm
#print axioms even_cycles_are_core_cycles
#print axioms even_parametrization
#print axioms odd_parametrization
#print axioms even_family
#print axioms odd_family
#print axioms even_parameters_unique
#print axioms odd_parameters_unique
#print axioms wedge_row_closed
#print axioms cycle_reconstruction
#print axioms wedge_core
#print axioms common_shift_cancels
#print axioms common_core_gain
#print axioms physical_current_identity
#print axioms positive_hull
#print axioms negative_hull
#print axioms shared_octahedron
#print axioms weighted_gram_entries

#print axioms rowProjector_eq
#print axioms C_eq
#print axioms Z_eq
#print axioms L0_eq
#print axioms tileCoeff_eq
#print axioms edgeCoeff_eq
#print axioms epsT_covariant
#print axioms real_column_definition
#print axioms real_column_gram
#print axioms common_real_gram
#print axioms flywheel_tetrad_gram
#print axioms core_decomposition
#print axioms inherited_midpoints

end FlywheelTetradGeometry
