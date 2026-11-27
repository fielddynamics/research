import Mathlib

/-!
# GP-2 · Robustness of the balance plane (Lean 4 / Mathlib formalisation)

Exploratory Great Pyramid core framework, Gravity Field Dynamics.
Companion to `../README.md` and `../verify_gp2_robustness.py`.

What is formalised:

* `affine_share_strictAntiOn` (Theorem 3, the monotone range `-1 < b ≤ 2`):
  `g(u) = (1-u)^2 (1+bu)` is strictly decreasing on `[0,1]`, so its balance level is unique.
* `affine_share_diff` : the exact factorisation `g(u) - g(v) = (v-u) Q(u,v,b)` used above.
* `shift_coefficient` (Theorem 4): `(1-u₀) u₀ / 2 = (√2 - 1)/4` at `u₀ = 1 - 1/√2`,
  i.e. `du*/db = -(∂g/∂b)/(∂g/∂u)` at `b = 0`.
* `interval_sq`, `interval_sqrt` (Theorem 5): if the mean axial density ratio `r` lies in
  `[1-ε, 1+ε]` and `(1-u)^2 r = 1/2`, then `1/(2(1+ε)) ≤ (1-u)^2 ≤ 1/(2(1-ε))`, hence
  `1 - 1/√(2(1-ε)) ≤ u ≤ 1 - 1/√(2(1+ε))`.
* `interval_sharp` : the bounds are attained by constant ratios `1 ± ε`.
* `constitutive_half_iff` and `structural_ne_constitutive` (Theorem 8): `x/(x+1) = 1/2 ↔ x = 1`,
  and the net-field value `μ = 1` differs from `μ_B = 1/2` by `1/2`.

Not formalised (checked by the script): the centroid identity and flux balance (Theorems 1–2,
measure theory), the case `b > 2` of Theorem 3, the Earth and self-gravity numerics (6–7).
-/

namespace GP2

open Real

/-- The affine-background share `g(u) = (1-u)^2 (1 + b u)`. -/
def g (b u : ℝ) : ℝ := (1 - u) ^ 2 * (1 + b * u)

/-- Exact difference factorisation. -/
theorem affine_share_diff (b u v : ℝ) :
    g b u - g b v =
      (v - u) * ((2 - u - v) + b * (-u ^ 2 - u * v - v ^ 2 + 2 * u + 2 * v - 1)) := by
  simp only [g]; ring

/-- For `-1 < b ≤ 2` the share is strictly decreasing on `[0,1]` (Theorem 3). -/
theorem affine_share_strictAntiOn {b : ℝ} (hb1 : -1 < b) (hb2 : b ≤ 2) :
    StrictAntiOn (g b) (Set.Icc (0 : ℝ) 1) := by
  intro u hu v hv huv
  obtain ⟨hu0, hu1⟩ := hu
  obtain ⟨hv0, hv1⟩ := hv
  -- Q is affine in b: 3 Q(b) = (2 - b) Q(-1) + (b + 1) Q(2)
  have qm1 : 0 ≤ (1 - u) ^ 2 + (1 - v) ^ 2 + (1 - u) * (1 - v) := by
    have : 0 ≤ (1 - u) * (1 - v) := mul_nonneg (by linarith) (by linarith)
    positivity
  have q2 : 0 < u * (3 - 2 * u - v) + v * (3 - u - 2 * v) := by
    have a : 0 ≤ u * (3 - 2 * u - v) := mul_nonneg hu0 (by linarith)
    have c : 0 < v * (3 - u - 2 * v) := mul_pos (by linarith) (by linarith)
    linarith
  have hQ : 0 < (2 - u - v) + b * (-u ^ 2 - u * v - v ^ 2 + 2 * u + 2 * v - 1) := by
    have e : 3 * ((2 - u - v) + b * (-u ^ 2 - u * v - v ^ 2 + 2 * u + 2 * v - 1)) =
        (2 - b) * ((1 - u) ^ 2 + (1 - v) ^ 2 + (1 - u) * (1 - v)) +
          (b + 1) * (u * (3 - 2 * u - v) + v * (3 - u - 2 * v)) := by ring
    have t1 : 0 ≤ (2 - b) * ((1 - u) ^ 2 + (1 - v) ^ 2 + (1 - u) * (1 - v)) :=
      mul_nonneg (by linarith) qm1
    have t2 : 0 < (b + 1) * (u * (3 - 2 * u - v) + v * (3 - u - 2 * v)) :=
      mul_pos (by linarith) q2
    linarith
  have := affine_share_diff b u v
  have hpos : 0 < (v - u) * ((2 - u - v) + b * (-u ^ 2 - u * v - v ^ 2 + 2 * u + 2 * v - 1)) :=
    mul_pos (by linarith) hQ
  linarith

/-- Uniqueness of the balance level for `-1 < b ≤ 2`. -/
theorem affine_balance_unique {b u v : ℝ} (hb1 : -1 < b) (hb2 : b ≤ 2)
    (hu : u ∈ Set.Icc (0 : ℝ) 1) (hv : v ∈ Set.Icc (0 : ℝ) 1)
    (h1 : g b u = 1 / 2) (h2 : g b v = 1 / 2) : u = v :=
  (affine_share_strictAntiOn hb1 hb2).injOn hu hv (h1.trans h2.symm)

/-- The partial derivatives of `g` (Theorem 3 uses the first; Theorem 4 both). -/
theorem partials (b u : ℝ) :
    HasDerivAt (fun w => g b w) (-(1 - u) * (2 - b + 3 * b * u)) u ∧
      HasDerivAt (fun c => g c u) ((1 - u) ^ 2 * u) b := by
  constructor
  · have h1 : HasDerivAt (fun w : ℝ => 1 - w) (-1) u := by
      simpa using (hasDerivAt_id u).const_sub 1
    have h2 : HasDerivAt (fun w : ℝ => 1 + b * w) b u := by
      simpa using ((hasDerivAt_id u).const_mul b).const_add 1
    have h4 := (h1.mul h1).mul h2
    have e : (fun w => g b w) = fun w => (1 - w) * (1 - w) * (1 + b * w) := by
      funext w; unfold g; ring
    rw [e]
    exact h4.congr_deriv (by ring)
  · have h2 : HasDerivAt (fun c : ℝ => 1 + c * u) u b := by
      simpa using ((hasDerivAt_id b).mul_const u).const_add 1
    exact (h2.const_mul ((1 - u) ^ 2)).congr_deriv (by ring)

/-- Theorem 4: `du*/db` at `b = 0`. Implicit differentiation of `g(u*(b), b) = 1/2` with
`∂g/∂b = (1-u)^2 u` and `∂g/∂u = -2(1-u)` at `b = 0` (`partials`) gives `(1-u₀) u₀ / 2`;
at `u₀ = 1 - 1/√2` this is `(√2 - 1)/4`. -/
theorem shift_coefficient {u₀ : ℝ} (hu : u₀ = 1 - 1 / Real.sqrt 2) :
    (1 - u₀) ^ 2 * u₀ / (2 * (1 - u₀)) = (Real.sqrt 2 - 1) / 4 := by
  have hs : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hspos : 0 < Real.sqrt 2 := by positivity
  have hinv : 1 / Real.sqrt 2 = Real.sqrt 2 / 2 := by
    rw [div_eq_div_iff hspos.ne' (by norm_num), one_mul]
    exact (Real.mul_self_sqrt (by norm_num)).symm
  rw [hinv] at hu
  subst hu
  have h1 : 1 - (1 - Real.sqrt 2 / 2) = Real.sqrt 2 / 2 := by ring
  rw [h1, div_eq_iff (by positivity)]
  linear_combination (-(Real.sqrt 2) / 8) * hs

/-- Theorem 5, squared form. -/
theorem interval_sq {ε r u : ℝ} (he1 : ε < 1)
    (hr1 : 1 - ε ≤ r) (hr2 : r ≤ 1 + ε) (h : (1 - u) ^ 2 * r = 1 / 2) :
    1 / (2 * (1 + ε)) ≤ (1 - u) ^ 2 ∧ (1 - u) ^ 2 ≤ 1 / (2 * (1 - ε)) := by
  have rpos : 0 < r := by linarith
  have hq : (1 - u) ^ 2 = 1 / (2 * r) := by
    field_simp; linarith
  rw [hq]
  constructor
  · apply one_div_le_one_div_of_le (by positivity); linarith
  · apply one_div_le_one_div_of_le (by nlinarith); linarith

/-- Theorem 5, the interval for the level itself. -/
theorem interval_sqrt {ε r u : ℝ} (he0 : 0 ≤ ε) (he1 : ε < 1)
    (hr1 : 1 - ε ≤ r) (hr2 : r ≤ 1 + ε) (hu : u ≤ 1) (h : (1 - u) ^ 2 * r = 1 / 2) :
    1 - 1 / Real.sqrt (2 * (1 - ε)) ≤ u ∧ u ≤ 1 - 1 / Real.sqrt (2 * (1 + ε)) := by
  obtain ⟨hlo, hhi⟩ := interval_sq he1 hr1 hr2 h
  have ht : 0 ≤ 1 - u := by linarith
  have hsq : Real.sqrt ((1 - u) ^ 2) = 1 - u := Real.sqrt_sq ht
  have a : Real.sqrt (1 / (2 * (1 + ε))) ≤ 1 - u := by
    rw [← hsq]; exact Real.sqrt_le_sqrt hlo
  have c : 1 - u ≤ Real.sqrt (1 / (2 * (1 - ε))) := by
    rw [← hsq]; exact Real.sqrt_le_sqrt hhi
  rw [Real.sqrt_div' _ (by positivity : (0 : ℝ) ≤ 2 * (1 + ε)), Real.sqrt_one] at a
  rw [Real.sqrt_div' _ (by nlinarith : (0 : ℝ) ≤ 2 * (1 - ε)), Real.sqrt_one] at c
  constructor <;> linarith

/-- The interval is sharp: the constant ratios `1 + ε` and `1 - ε` attain its ends. -/
theorem interval_sharp {ε : ℝ} (he0 : 0 ≤ ε) (he1 : ε < 1) :
    (1 / Real.sqrt (2 * (1 + ε))) ^ 2 * (1 + ε) = 1 / 2 ∧
      (1 / Real.sqrt (2 * (1 - ε))) ^ 2 * (1 - ε) = 1 / 2 := by
  have p1 : (0 : ℝ) < 2 * (1 + ε) := by linarith
  have p2 : (0 : ℝ) < 2 * (1 - ε) := by linarith
  constructor
  · rw [div_pow, Real.sq_sqrt p1.le]; field_simp
  · rw [div_pow, Real.sq_sqrt p2.le]; field_simp

/-- Theorem 8 (i): the constitutive law reaches one half only at `x = 1` (`g = a₀`). -/
theorem constitutive_half_iff {x : ℝ} (hx : 0 ≤ x) : x / (x + 1) = 1 / 2 ↔ x = 1 := by
  have h : x + 1 ≠ 0 := by linarith
  constructor
  · intro e; field_simp at e; linarith
  · rintro rfl; norm_num

/-- Theorem 8 (ii): with the net-field rule's `μ = 1` (drainless, pure TetA) and the balance
plane's `μ_B = 1/2`, the two shares differ by exactly one half. -/
theorem structural_ne_constitutive : |(1 / 2 : ℝ) - 1| = 1 / 2 := by norm_num

/-- Theorem 8 (iii): for `x > 0` the TetB share `1/(1+x)` is below `1/x`. -/
theorem tetB_share_small {x : ℝ} (hx : 0 < x) : 1 - x / (x + 1) < 1 / x := by
  have h : 1 - x / (x + 1) = 1 / (x + 1) := by field_simp; ring
  rw [h]
  exact one_div_lt_one_div_of_lt hx (by linarith)

end GP2

#print axioms GP2.affine_share_diff
#print axioms GP2.affine_share_strictAntiOn
#print axioms GP2.affine_balance_unique
#print axioms GP2.partials
#print axioms GP2.shift_coefficient
#print axioms GP2.interval_sq
#print axioms GP2.interval_sqrt
#print axioms GP2.interval_sharp
#print axioms GP2.constitutive_half_iff
#print axioms GP2.structural_ne_constitutive
#print axioms GP2.tetB_share_small
