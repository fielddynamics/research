import ForcedTetrahedralFrame
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Geometry.Euclidean.Angle.Unoriented.Basic

/-!
# The tetrahedral angle, in Mathlib's sense of the angle between vectors

Corollary 1 of "The Spatial Geometry of the Lorentz Tetrad" states that the angle between any two
legs is `arccos(−1/3)`. `ForcedTetrahedralFrame.cor1_geometry` proves the cosine form; this file
states the angle itself, using Mathlib's `InnerProductGeometry.angle` on Euclidean space
`EuclideanSpace ℝ (Fin 3)`, whose definition is `arccos (⟪x, y⟫ / (‖x‖ ‖y‖))`. Nothing about the
angle is defined here.
-/

open ForcedTetrahedralFrame

namespace ForcedTetrahedralFrame

/-- **Corollary 1 (angle).** In any realisation satisfying (R), (M), (N), (D), the angle between
any two distinct legs, as vectors of Euclidean `ℝ³`, is `arccos(−1/3)`. -/
theorem cor1_angle (v : Fin 4 → Fin 3 → ℝ) (c : ℝ) (h : Realisation 4 3 v c) (a b : Fin 4)
    (hab : a ≠ b) :
    InnerProductGeometry.angle (WithLp.toLp 2 (v a) : EuclideanSpace ℝ (Fin 3))
      (WithLp.toLp 2 (v b)) = Real.arccos (-1 / 3) := by
  have hi : ∀ x y : Fin 3 → ℝ,
      inner ℝ (WithLp.toLp 2 x : EuclideanSpace ℝ (Fin 3)) (WithLp.toLp 2 y) = x ⬝ᵥ y := by
    intro x y
    rw [EuclideanSpace.inner_toLp_toLp]
    simp [dotProduct_comm]
  have hn : ∀ x : Fin 3 → ℝ, ‖(WithLp.toLp 2 x : EuclideanSpace ℝ (Fin 3))‖ = Real.sqrt (x ⬝ᵥ x) := by
    intro x
    rw [← hi x x, real_inner_self_eq_norm_sq, Real.sqrt_sq (norm_nonneg _)]
  unfold InnerProductGeometry.angle
  rw [hi, hn, hn]
  exact congrArg Real.arccos ((cor1_geometry v c h).2.2.2.2 a b hab)

end ForcedTetrahedralFrame

#print axioms ForcedTetrahedralFrame.cor1_angle
