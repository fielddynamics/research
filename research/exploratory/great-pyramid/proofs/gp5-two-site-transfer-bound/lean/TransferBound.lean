import Mathlib

/-!
# GP-5 · Two-site transfer bound and the mirror selector (Lean 4 / Mathlib formalisation)

Exploratory Great Pyramid core framework, Gravity Field Dynamics.
Companion to `../README.md` and `../verify_gp5_transfer_bound.py`.

What is formalised:

* `closed_form_norm` (Theorem 1): the closed-form amplitudes conserve probability,
  `cos² + (Δ/Ω)² sin² + (4|κ|²/Ω²) sin² = 1` when `Ω² = Δ² + 4|κ|²`.
* `peak_le_one`, `peak_eq_one_iff`, `peak_le_detuned` (Theorem 1): the peak transfer
  `4κ²/(Δ²+4κ²)` is at most 1, equals 1 iff `Δ = 0`, and is at most `4κ²/Δ²`.
* `detuning_tolerance` (Proposition 4): peak `≥ η` iff `Δ² ≤ 4κ²(1-η)/η`.
* `budget_mono` (Theorem 6, last item): a selector `M ∈ [0,1]` can only lower the bound
  `sin²(min(κ₀ M t, π/2))`.
* `selector_mem`, `selector_eq_one_iff` (Theorem 6): `M_xy ∈ [0,1]`, and `M_xy = 1` iff `d = 0`,
  `χ_x = -χ_y` and `cos²(Δθ/2) = 1`; `cos_sq_half_eq_one_iff`: the last means `Δθ ∈ 2πℤ`.
* `orbitDist_symm`, `orbitDist_triangle`, `orbitDist_self_smul` (Theorem 6): for a finite
  group acting by isometries, `d(x, y) = min_g dist(x, g • y)` is a pseudometric that vanishes on
  relabellings. With `S₃` acting on triad Gram matrices by `G ↦ PᵀGP`, this is `d_G`.

Not formalised (checked by the script): the coupling-budget inequality of Theorem 2 for
time-dependent drives, which needs the geodesic distance on `S³`; Corollary 3; Proposition 5.
-/

namespace GP5

open Real

/-- Theorem 1: the closed form conserves probability. -/
theorem closed_form_norm {Δ κ Ω θ : ℝ} (hΩ : Ω ^ 2 = Δ ^ 2 + 4 * κ ^ 2) (hΩ0 : Ω ≠ 0) :
    Real.cos θ ^ 2 + (Δ / Ω) ^ 2 * Real.sin θ ^ 2 + (4 * κ ^ 2 / Ω ^ 2) * Real.sin θ ^ 2 = 1 := by
  have h := Real.sin_sq_add_cos_sq θ
  have : (Δ / Ω) ^ 2 + 4 * κ ^ 2 / Ω ^ 2 = 1 := by
    rw [div_pow, div_add_div_same, ← hΩ, div_self (pow_ne_zero 2 hΩ0)]
  nlinarith [this]

/-- The peak transfer is at most one. -/
theorem peak_le_one {Δ κ : ℝ} (hκ : κ ≠ 0) : 4 * κ ^ 2 / (Δ ^ 2 + 4 * κ ^ 2) ≤ 1 := by
  have hpos : 0 < Δ ^ 2 + 4 * κ ^ 2 := by positivity
  rw [div_le_one hpos]; nlinarith [sq_nonneg Δ]

/-- Complete transfer happens iff the sites are in resonance. -/
theorem peak_eq_one_iff {Δ κ : ℝ} (hκ : κ ≠ 0) : 4 * κ ^ 2 / (Δ ^ 2 + 4 * κ ^ 2) = 1 ↔ Δ = 0 := by
  have hpos : 0 < Δ ^ 2 + 4 * κ ^ 2 := by positivity
  rw [div_eq_one_iff_eq hpos.ne']
  constructor
  · intro h; nlinarith [sq_nonneg Δ]
  · rintro rfl; ring

/-- Detuned peak is at most `4κ²/Δ²`. -/
theorem peak_le_detuned {Δ κ : ℝ} (hΔ : Δ ≠ 0) :
    4 * κ ^ 2 / (Δ ^ 2 + 4 * κ ^ 2) ≤ 4 * κ ^ 2 / Δ ^ 2 := by
  apply div_le_div_of_nonneg_left (by positivity) (by positivity)
  nlinarith [sq_nonneg κ]

/-- Proposition 4: detuning tolerance for a target efficiency `η`. -/
theorem detuning_tolerance {Δ κ η : ℝ} (hκ : κ ≠ 0) (hη : 0 < η) :
    η ≤ 4 * κ ^ 2 / (Δ ^ 2 + 4 * κ ^ 2) ↔ Δ ^ 2 ≤ 4 * κ ^ 2 * (1 - η) / η := by
  have hpos : 0 < Δ ^ 2 + 4 * κ ^ 2 := by positivity
  rw [le_div_iff₀ hpos, le_div_iff₀ hη]
  constructor <;> intro h <;> nlinarith

/-- A selector in `[0,1]` can only lower the coupling-budget bound. -/
theorem budget_mono {κ₀ M t : ℝ} (hκ : 0 ≤ κ₀) (ht : 0 ≤ t) (hM0 : 0 ≤ M) (hM1 : M ≤ 1) :
    Real.sin (min (κ₀ * M * t) (π / 2)) ^ 2 ≤ Real.sin (min (κ₀ * t) (π / 2)) ^ 2 := by
  have a0 : 0 ≤ min (κ₀ * M * t) (π / 2) := le_min (by positivity) (by positivity)
  have hle : min (κ₀ * M * t) (π / 2) ≤ min (κ₀ * t) (π / 2) := by
    apply min_le_min_right
    have : κ₀ * M * t ≤ κ₀ * 1 * t := by
      apply mul_le_mul_of_nonneg_right (mul_le_mul_of_nonneg_left hM1 hκ) ht
    linarith
  have b1 : min (κ₀ * t) (π / 2) ≤ π / 2 := min_le_right _ _
  have s0 : 0 ≤ Real.sin (min (κ₀ * M * t) (π / 2)) :=
    Real.sin_nonneg_of_nonneg_of_le_pi a0 (by linarith [Real.pi_pos])
  have mono : Real.sin (min (κ₀ * M * t) (π / 2)) ≤ Real.sin (min (κ₀ * t) (π / 2)) :=
    Real.sin_le_sin_of_le_of_le_pi_div_two (by linarith [Real.pi_pos]) b1 hle
  exact pow_le_pow_left₀ s0 mono 2

/-- The mirror-address selector of README §9 (with `χ = ±1`). -/
noncomputable def selector (d ε χx χy Δθ : ℝ) : ℝ :=
  Real.exp (-(d ^ 2) / (2 * ε ^ 2)) * ((1 - χx * χy) / 2) * Real.cos (Δθ / 2) ^ 2

lemma chirality_factor {χx χy : ℝ} (hx : χx = 1 ∨ χx = -1) (hy : χy = 1 ∨ χy = -1) :
    ((1 - χx * χy) / 2 = 0 ∨ (1 - χx * χy) / 2 = 1) ∧ ((1 - χx * χy) / 2 = 1 ↔ χx = -χy) := by
  rcases hx with rfl | rfl <;> rcases hy with rfl | rfl <;> norm_num

theorem selector_mem {d ε χx χy Δθ : ℝ} (hx : χx = 1 ∨ χx = -1) (hy : χy = 1 ∨ χy = -1) :
    0 ≤ selector d ε χx χy Δθ ∧ selector d ε χx χy Δθ ≤ 1 := by
  have he0 : 0 < Real.exp (-(d ^ 2) / (2 * ε ^ 2)) := Real.exp_pos _
  have he1 : Real.exp (-(d ^ 2) / (2 * ε ^ 2)) ≤ 1 := by
    rw [Real.exp_le_one_iff]
    apply div_nonpos_of_nonpos_of_nonneg (by nlinarith [sq_nonneg d]) (by positivity)
  have hc0 : 0 ≤ Real.cos (Δθ / 2) ^ 2 := sq_nonneg _
  have hc1 : Real.cos (Δθ / 2) ^ 2 ≤ 1 := by
    rw [sq_le_one_iff_abs_le_one]; exact Real.abs_cos_le_one _
  obtain ⟨h01, _⟩ := chirality_factor hx hy
  unfold selector
  rcases h01 with h | h <;> rw [h]
  · simp
  · constructor
    · positivity
    · rw [mul_one]; nlinarith

theorem selector_eq_one_iff {d ε χx χy Δθ : ℝ} (hε : ε ≠ 0)
    (hx : χx = 1 ∨ χx = -1) (hy : χy = 1 ∨ χy = -1) :
    selector d ε χx χy Δθ = 1 ↔ d = 0 ∧ χx = -χy ∧ Real.cos (Δθ / 2) ^ 2 = 1 := by
  obtain ⟨h01, hiff⟩ := chirality_factor hx hy
  have he1 : Real.exp (-(d ^ 2) / (2 * ε ^ 2)) ≤ 1 := by
    rw [Real.exp_le_one_iff]
    apply div_nonpos_of_nonpos_of_nonneg (by nlinarith [sq_nonneg d]) (by positivity)
  have he0 : 0 < Real.exp (-(d ^ 2) / (2 * ε ^ 2)) := Real.exp_pos _
  have hc1 : Real.cos (Δθ / 2) ^ 2 ≤ 1 := by
    rw [sq_le_one_iff_abs_le_one]; exact Real.abs_cos_le_one _
  have hc0 : 0 ≤ Real.cos (Δθ / 2) ^ 2 := sq_nonneg _
  unfold selector
  constructor
  · intro h
    rcases h01 with h0 | h0
    · rw [h0] at h; simp at h
    · rw [h0, mul_one] at h
      have hE : Real.exp (-(d ^ 2) / (2 * ε ^ 2)) = 1 := by nlinarith
      have hC : Real.cos (Δθ / 2) ^ 2 = 1 := by nlinarith
      refine ⟨?_, hiff.mp h0, hC⟩
      rw [Real.exp_eq_one_iff] at hE
      have h2 : (0 : ℝ) < 2 * ε ^ 2 := by positivity
      have : d ^ 2 = 0 := by
        field_simp at hE; nlinarith [sq_nonneg d]
      exact pow_eq_zero_iff (n := 2) (by norm_num) |>.mp this
  · rintro ⟨rfl, hχ, hC⟩
    rw [hiff.mpr hχ, hC]; simp

/-- `cos² (θ/2) = 1` iff `θ ∈ 2πℤ`. -/
theorem cos_sq_half_eq_one_iff (θ : ℝ) :
    Real.cos (θ / 2) ^ 2 = 1 ↔ ∃ n : ℤ, θ = n * (2 * π) := by
  have h := Real.sin_sq_add_cos_sq (θ / 2)
  constructor
  · intro hc
    have hs : Real.sin (θ / 2) = 0 := by
      have : Real.sin (θ / 2) ^ 2 = 0 := by linarith
      exact pow_eq_zero_iff (n := 2) (by norm_num) |>.mp this
    obtain ⟨n, hn⟩ := Real.sin_eq_zero_iff.mp hs
    exact ⟨n, by linarith⟩
  · rintro ⟨n, rfl⟩
    have : Real.sin (n * (2 * π) / 2) = 0 := by
      rw [show (n : ℝ) * (2 * π) / 2 = n * π by ring]
      exact Real.sin_int_mul_pi n
    nlinarith

section OrbitDist

variable {G X : Type*} [Group G] [Fintype G] [MulAction G X] [PseudoMetricSpace X]

/-- The relabelling-invariant mismatch `d(x, y) = min_g dist(x, g • y)`. -/
noncomputable def orbitDist (x y : X) : ℝ :=
  Finset.univ.inf' Finset.univ_nonempty (fun g : G => dist x (g • y))

variable (hiso : ∀ (g : G) (a b : X), dist (g • a) (g • b) = dist a b)
include hiso

lemma orbitDist_le_of (x y : X) (g : G) : orbitDist (G := G) x y ≤ dist x (g • y) :=
  Finset.inf'_le _ (Finset.mem_univ g)

lemma orbitDist_symm_le (x y : X) : orbitDist (G := G) y x ≤ orbitDist (G := G) x y := by
  apply Finset.le_inf'
  intro g _
  calc orbitDist (G := G) y x ≤ dist y (g⁻¹ • x) := orbitDist_le_of hiso y x g⁻¹
    _ = dist (g • y) (g • g⁻¹ • x) := (hiso g _ _).symm
    _ = dist x (g • y) := by rw [smul_inv_smul, dist_comm]

theorem orbitDist_symm (x y : X) : orbitDist (G := G) x y = orbitDist (G := G) y x :=
  le_antisymm (orbitDist_symm_le hiso y x) (orbitDist_symm_le hiso x y)

theorem orbitDist_triangle (x y z : X) :
    orbitDist (G := G) x z ≤ orbitDist (G := G) x y + orbitDist (G := G) y z := by
  obtain ⟨g, -, hg⟩ := Finset.exists_mem_eq_inf' Finset.univ_nonempty (fun g : G => dist x (g • y))
  obtain ⟨h, -, hh⟩ := Finset.exists_mem_eq_inf' Finset.univ_nonempty (fun h : G => dist y (h • z))
  have e1 : orbitDist (G := G) x y = dist x (g • y) := hg
  have e2 : orbitDist (G := G) y z = dist y (h • z) := hh
  calc orbitDist (G := G) x z ≤ dist x ((g * h) • z) := orbitDist_le_of hiso x z (g * h)
    _ ≤ dist x (g • y) + dist (g • y) ((g * h) • z) := dist_triangle _ _ _
    _ = dist x (g • y) + dist y (h • z) := by rw [mul_smul, hiso]
    _ = orbitDist (G := G) x y + orbitDist (G := G) y z := by rw [e1, e2]

theorem orbitDist_self_smul (x : X) (g : G) : orbitDist (G := G) x (g • x) = 0 := by
  apply le_antisymm
  · calc orbitDist (G := G) x (g • x) ≤ dist x (g⁻¹ • g • x) := orbitDist_le_of hiso x _ g⁻¹
      _ = 0 := by rw [inv_smul_smul, dist_self]
  · apply Finset.le_inf'
    intro g _
    exact dist_nonneg

end OrbitDist

end GP5

#print axioms GP5.closed_form_norm
#print axioms GP5.peak_le_one
#print axioms GP5.peak_eq_one_iff
#print axioms GP5.peak_le_detuned
#print axioms GP5.detuning_tolerance
#print axioms GP5.budget_mono
#print axioms GP5.selector_mem
#print axioms GP5.selector_eq_one_iff
#print axioms GP5.cos_sq_half_eq_one_iff
#print axioms GP5.orbitDist_symm
#print axioms GP5.orbitDist_triangle
#print axioms GP5.orbitDist_self_smul
