import FlywheelTetradGeometry
import Mathlib

/-! Proof 25: common closure-space transport and the pair-incidence core.
The real matrix lemmas are dimension-parametric. Finite matrix identities
are proved entry by entry with `fin_cases` and `norm_num`. No physical
axiom is supplied; see LEAN_AUDIT.md for the build and axiom audit. -/
namespace TetradFlywheelConvergence
open Matrix
open scoped BigOperators
open FlywheelTetradGeometry
set_option maxRecDepth 4096
set_option maxHeartbeats 0
-- The generic simp sets below list structural lemmas some identities do not need.
set_option linter.unusedSimpArgs false

/-! 1. The key combinatorial step in the incidence recognition theorem.
After naming the reference triangle, an edge common to the first two
attached triangles requires a common vertex other than their shared
reference vertex. The full graph-to-this-reduction argument is in the paper. -/
theorem shared_outside_vertex {α : Type*} (b c x y : α)
    (hbc : b ≠ c) (hby : b ≠ y) (hxc : x ≠ c)
    (h : ∃ t, (t = b ∨ t = x) ∧ (t = c ∨ t = y)) : x = y := by
  rcases h with ⟨t, ht, hu⟩
  rcases ht with h₁ | h₁ <;> rcases hu with h₂ | h₂
  · exact False.elim (hbc (h₁.symm.trans h₂))
  · exact False.elim (hby (h₁.symm.trans h₂))
  · exact False.elim (hxc (h₁.symm.trans h₂))
  · exact h₁.symm.trans h₂

theorem attached_triangles {α : Type*} (a b c x y z : α)
    (hbc : b ≠ c) (hac : a ≠ c) (hby : b ≠ y) (hxc : x ≠ c)
    (haz : a ≠ z)
    (hxy : ∃ t, (t = b ∨ t = x) ∧ (t = c ∨ t = y))
    (hxz : ∃ t, (t = a ∨ t = x) ∧ (t = c ∨ t = z)) :
    x = y ∧ x = z := by
  exact ⟨shared_outside_vertex b c x y hbc hby hxc hxy,
    shared_outside_vertex a c x z hac haz hxc hxz⟩

/-! 2. Signed complementary-edge involution and intrinsic projector. -/
def dualEdge : Matrix Edge Edge ℚ :=
  !![0,0,0,0,0,-1; 0,0,0,0,1,0; 0,0,0,-1,0,0;
     0,0,-1,0,0,0; 0,1,0,0,0,0; -1,0,0,0,0,0]

theorem dual_symmetric : dualEdgeᵀ = dualEdge := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;> norm_num [dualEdge, Matrix.one_apply, nsmul_eq_mul]

theorem dual_involutive : dualEdge * dualEdge = 1 := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;> norm_num [dualEdge, Matrix.one_apply, nsmul_eq_mul]

theorem dual_cut_cycle : dualEdge * (B : Matrix Label Edge ℚ)ᵀ = (D : Matrix Edge Label ℚ) := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;> norm_num [dualEdge, B, D, Matrix.one_apply, nsmul_eq_mul]

theorem dual_projectors :
    dualEdge * ((B : Matrix Label Edge ℚ)ᵀ * (B : Matrix Label Edge ℚ)) * dualEdge =
      (D : Matrix Edge Label ℚ) * (D : Matrix Edge Label ℚ)ᵀ := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;> norm_num [dualEdge, B, D, Matrix.one_apply, nsmul_eq_mul]

noncomputable def closureP : Matrix Label Label ℝ := (1/4 : ℝ) • (G : Matrix Label Label ℝ)

theorem closureP_symm : closurePᵀ = closureP := by
  ext i j; fin_cases i <;> fin_cases j <;> norm_num [closureP, G]

theorem closureP_idem : closureP * closureP = closureP := by
  ext i j; fin_cases i <;> fin_cases j <;>
    norm_num [closureP, G, Matrix.mul_apply, Fin.sum_univ_succ]

theorem intrinsic_frame_gram :
    ((2 : ℝ) • closureP)ᵀ * ((2 : ℝ) • closureP) = (G : Matrix Label Label ℝ) := by
  ext i j; fin_cases i <;> fin_cases j <;>
    norm_num [closureP, G, Matrix.mul_apply, Fin.sum_univ_succ]

/-- Reuse the actual frame and column read from Proof 24, not independent axioms. -/
theorem inherited_cycle_gram :
    (D : Matrix Edge Label ℝ)ᵀ * (D : Matrix Edge Label ℝ) = (G : Matrix Label Label ℝ) := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;> norm_num [D, G, Matrix.one_apply, nsmul_eq_mul]

theorem inherited_cut_gram :
    (B : Matrix Label Edge ℝ) * (B : Matrix Label Edge ℝ)ᵀ = (G : Matrix Label Label ℝ) := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;> norm_num [B, G, Matrix.one_apply, nsmul_eq_mul]

theorem inherited_spatial_gram : ForcedTetrahedralFrame.Mmatᵀ * ForcedTetrahedralFrame.Mmat = (G : Matrix Label Label ℝ) := by
  ext i j
  exact (real_cycle_tetrad_gram i j).symm.trans
    (congrArg (fun M : Matrix Label Label ℝ => M i j) inherited_cycle_gram)

theorem inherited_flywheel_gram : FRealᵀ * FReal = (G : Matrix Label Label ℝ) := by
  ext i j
  exact (common_real_gram i j).trans
    (congrArg (fun M : Matrix Label Label ℝ => M i j) inherited_cycle_gram)

/-! 3. Universal transport theorem. Use A=X/2, B=Y/2, C=Z/2,
so the Gram is the projector itself and transport is B Aᵀ. -/
section Transport
variable {n m k : Type*} [Fintype n] [Fintype m] [Fintype k]

/-- A real Gram equal to zero forces the matrix to be zero. -/
theorem zero_gram (X : Matrix n Label ℝ) (h : Xᵀ * X = 0) : X = 0 := by
  classical
  ext i j
  have hs : (∑ l : n, X l j * X l j) = 0 := by
    have hh := congrArg (fun T : Matrix Label Label ℝ => T j j) h
    simpa [Matrix.mul_apply] using hh
  have hi : X i j * X i j ≤ ∑ l : n, X l j * X l j :=
    Finset.single_le_sum (f := fun l : n => X l j * X l j)
      (fun l _ => mul_self_nonneg (X l j)) (Finset.mem_univ i)
  rw [hs] at hi
  simp only [Matrix.zero_apply]
  nlinarith

/-- Crucial point: support on the closure space follows from the Gram;
it is not an additional hypothesis of the transport theorem. -/
theorem support_of_gram (X : Matrix n Label ℝ)
    (h : Xᵀ * X = closureP) : X * closureP = X := by
  have h₁ : Xᵀ * (X * closureP) = closureP := by
    rw [← Matrix.mul_assoc, h, closureP_idem]
  have h₂ : (X * closureP)ᵀ * X = closureP := by
    rw [Matrix.transpose_mul, closureP_symm, Matrix.mul_assoc, h, closureP_idem]
  have h₃ : (X * closureP)ᵀ * (X * closureP) = closureP := by
    rw [Matrix.transpose_mul, closureP_symm, Matrix.mul_assoc, h₁, closureP_idem]
  have hz : (X - X * closureP)ᵀ * (X - X * closureP) = 0 := by
    rw [Matrix.transpose_sub, Matrix.sub_mul, Matrix.mul_sub, Matrix.mul_sub, h, h₁, h₂, h₃]
    abel
  exact (sub_eq_zero.mp (zero_gram _ hz)).symm

def transport (X : Matrix n Label ℝ) (Y : Matrix m Label ℝ) : Matrix m n ℝ := Y * Xᵀ

theorem transport_apply (X : Matrix n Label ℝ) (Y : Matrix m Label ℝ)
    (hX : Xᵀ * X = closureP) (hY : Yᵀ * Y = closureP) :
    transport X Y * X = Y := by
  rw [transport, Matrix.mul_assoc, hX, support_of_gram Y hY]

omit [Fintype n] in
theorem transport_composition (X : Matrix n Label ℝ) (Y : Matrix m Label ℝ)
    (Z : Matrix k Label ℝ) (hY : Yᵀ * Y = closureP) (hZ : Zᵀ * Z = closureP) :
    transport Y Z * transport X Y = transport X Z := by
  unfold transport
  calc
    (Z * Yᵀ) * (Y * Xᵀ) = Z * ((Yᵀ * Y) * Xᵀ) := by simp only [Matrix.mul_assoc]
    _ = Z * (closureP * Xᵀ) := by rw [hY]
    _ = Z * Xᵀ := by rw [← Matrix.mul_assoc, support_of_gram Z hZ]

theorem transport_source_projector (X : Matrix n Label ℝ) (Y : Matrix m Label ℝ)
    (hX : Xᵀ * X = closureP) (hY : Yᵀ * Y = closureP) :
    (transport X Y)ᵀ * transport X Y = X * Xᵀ := by
  unfold transport
  rw [Matrix.transpose_mul, Matrix.transpose_transpose]
  exact transport_composition X Y X hY hX

theorem transport_target_projector (X : Matrix n Label ℝ) (Y : Matrix m Label ℝ)
    (hX : Xᵀ * X = closureP) (hY : Yᵀ * Y = closureP) :
    transport X Y * (transport X Y)ᵀ = Y * Yᵀ := by
  unfold transport
  rw [Matrix.transpose_mul, Matrix.transpose_transpose]
  exact transport_composition Y X Y hX hY

theorem image_projector_idempotent (X : Matrix n Label ℝ) (hX : Xᵀ * X = closureP) :
    (X * Xᵀ) * (X * Xᵀ) = X * Xᵀ := by
  exact transport_composition X X X hX hX

/-- Uniqueness on the frame image: every vector represented by Xq has
the same image under every linear matrix map that sends X to Y. -/
theorem transport_unique_on_image (X : Matrix n Label ℝ) (Y : Matrix m Label ℝ)
    (T : Matrix m n ℝ) (q : Matrix Label (Fin 1) ℝ)
    (hX : Xᵀ * X = closureP) (hY : Yᵀ * Y = closureP)
    (hT : T * X = Y) : T * (X * q) = transport X Y * (X * q) := by
  rw [← Matrix.mul_assoc, hT, ← Matrix.mul_assoc, transport_apply X Y hX hY]
end Transport

/-! 4. Intrinsic reconstruction: analytic barycentric inverse and recession ray. -/
theorem barycentric_inverse (q : Label → ℝ) (h : ∑ i, q i = 0) (i : Label) :
    (∑ j : Label, (G : Matrix Label Label ℝ) i j * ((q j + 1)/4)) = q i := by
  rw [Fin.sum_univ_four] at h
  fin_cases i <;> simp [G, Fin.sum_univ_four] <;> linarith

theorem barycentric_sum (q : Label → ℝ) (h : ∑ i, q i = 0) :
    (∑ j : Label, (q j + 1)/4) = 1 := by
  rw [Fin.sum_univ_four] at h ⊢
  linarith

theorem upper_bound_forces_lower (a b c d : ℝ) (hs : a+b+c+d=0)
    (hb : b ≤ 1) (hc : c ≤ 1) (hd : d ≤ 1) : -3 ≤ a := by linarith

theorem unique_outer_spike (a b c d : ℝ) (hs : a+b+c+d=0)
    (hc : -1 ≤ c) (hd : -1 ≤ d) : ¬ (1 < a ∧ 1 < b) := by
  rintro ⟨ha,hb⟩; linarith

theorem fourth_saturation (a b c d : ℝ) (hs : a+b+c+d=0)
    (ha : a=1 ∨ a= -1) (hb : b=1 ∨ b= -1) (hc : c=1 ∨ c= -1)
    (hd : -1 ≤ d ∧ d ≤ 1) : d=1 ∨ d= -1 := by
  rcases ha with ha|ha <;> rcases hb with hb|hb <;> rcases hc with hc|hc <;>
    first | (left; linarith) | (right; linarith)

theorem inherited_core : HalfSpaceTwoBoundedRegions.TetA ∩ HalfSpaceTwoBoundedRegions.TetB =
    {p | |p 0| + |p 1| + |p 2| ≤ 1} := shared_octahedron

/-! 5. The unsigned pair incidence and its intrinsic octahedral Gram. -/
def pairInc : Matrix Label Edge ℚ :=
  !![1,1,1,0,0,0;1,0,0,1,1,0;0,1,0,1,0,1;0,0,1,0,1,1]

def coreAdj : Matrix Edge Edge ℚ := pairIncᵀ * pairInc - 2 • (1 : Matrix Edge Edge ℚ)
def J₆ : Matrix Edge Edge ℚ := Matrix.of (fun _ _ => 1)
def Mq : Matrix (Fin 3) Label ℚ := !![1,1,-1,-1;1,-1,1,-1;1,-1,-1,1]
def coreV : Matrix (Fin 3) Edge ℚ := (1/2 : ℚ) • (Mq * pairInc)

theorem pair_row_gram :
    pairInc * pairIncᵀ = (2 : ℚ) • (1 : Matrix Label Label ℚ) + Matrix.of (fun _ _ => 1) := by
  ext i j
  simp only [Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;> norm_num [pairInc, Matrix.one_apply, nsmul_eq_mul]

theorem core_vertex_gram : coreVᵀ * coreV = 2 • (1 : Matrix Edge Edge ℚ) + coreAdj - J₆ := by
  ext i j
  simp only [coreV, coreAdj, J₆, Matrix.of_apply, Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;> norm_num [Mq, pairInc, Matrix.one_apply, nsmul_eq_mul]

theorem core_tight_frame : coreV * coreVᵀ = 2 • (1 : Matrix (Fin 3) (Fin 3) ℚ) := by
  ext i j
  simp only [coreV, Matrix.mul_apply, Matrix.transpose_apply, Matrix.smul_apply, Matrix.sub_apply, Matrix.add_apply, smul_eq_mul, Fin.sum_univ_succ, Fin.sum_univ_zero]
  fin_cases i <;> fin_cases j <;> norm_num [Mq, pairInc, Matrix.one_apply, nsmul_eq_mul]

theorem core_spatial_bridge (i : Fin 3) (j : Label) : (Mq i j : ℝ) = ForcedTetrahedralFrame.Mmat i j := by
  fin_cases i <;> fin_cases j <;> norm_num [Mq, ForcedTetrahedralFrame.Mmat]

/-- The positive face contains pair vertices with label i; the negative
face contains pairs avoiding j. Count their common vertices. -/
def commonFaceVertices (i j : Label) : Finset Edge := Finset.univ.filter fun e =>
  ((edgeLabel e).1 = i ∨ (edgeLabel e).2 = i) ∧ (edgeLabel e).1 ≠ j ∧ (edgeLabel e).2 ≠ j

theorem core_face_adjacency (i j : Label) :
    (commonFaceVertices i j).card = if i=j then 0 else 2 := by
  revert i j; decide

/-! 6. Diagonal metric rigidity and the exact squared anisotropy identity. -/
theorem diagonal_metric_rigidity (w : Edge → ℝ) (c : ℝ)
    (h : ∀ i j : Label, i ≠ j → weightedGram w i j = -c) : ∀ e, w e = c := by
  obtain ⟨h01,h02,h03,h12,h13,h23⟩ := weighted_gram_entries w
  have a01 := h 0 1 (by decide)
  have a02 := h 0 2 (by decide)
  have a03 := h 0 3 (by decide)
  have a12 := h 1 2 (by decide)
  have a13 := h 1 3 (by decide)
  have a23 := h 2 3 (by decide)
  intro e
  fin_cases e
  · show w 0 = c; linarith
  · show w 1 = c; linarith
  · show w 2 = c; linarith
  · show w 3 = c; linarith
  · show w 4 = c; linarith
  · show w 5 = c; linarith

theorem constant_weights_gram (c : ℝ) (i j : Label) :
    weightedGram (fun _ => c) i j = c * (G : Matrix Label Label ℝ) i j := by
  fin_cases i <;> fin_cases j <;> simp [weightedGram, D, G, Fin.sum_univ_succ] <;> ring

/-- For six deviations in the fixed edge order, the four diagonal
entries are the sums on the complementary incidence. -/
theorem anisotropy_square (a b c d e f : ℝ) :
    (∑ i : Label, ∑ j : Label, (weightedGram (![a,b,c,d,e,f]) i j)^2) =
    2*(a^2+b^2+c^2+d^2+e^2+f^2) +
      (d+e+f)^2+(b+c+f)^2+(a+c+e)^2+(a+b+d)^2 := by
  simp [weightedGram, D, Fin.sum_univ_succ]; ring

/-! Axiom reports -/
#print axioms shared_outside_vertex
#print axioms attached_triangles
#print axioms dual_symmetric
#print axioms dual_involutive
#print axioms dual_cut_cycle
#print axioms dual_projectors
#print axioms closureP_symm
#print axioms closureP_idem
#print axioms intrinsic_frame_gram
#print axioms inherited_cycle_gram
#print axioms inherited_cut_gram
#print axioms inherited_spatial_gram
#print axioms inherited_flywheel_gram
#print axioms zero_gram
#print axioms support_of_gram
#print axioms transport_apply
#print axioms transport_composition
#print axioms transport_source_projector
#print axioms transport_target_projector
#print axioms image_projector_idempotent
#print axioms transport_unique_on_image
#print axioms barycentric_inverse
#print axioms barycentric_sum
#print axioms upper_bound_forces_lower
#print axioms unique_outer_spike
#print axioms fourth_saturation
#print axioms inherited_core
#print axioms pair_row_gram
#print axioms core_vertex_gram
#print axioms core_tight_frame
#print axioms core_spatial_bridge
#print axioms core_face_adjacency
#print axioms diagonal_metric_rigidity
#print axioms constant_weights_gram
#print axioms anisotropy_square

end TetradFlywheelConvergence
