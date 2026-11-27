import Mathlib

/-!
# GP-1 · The half-section theorem (Lean 4 / Mathlib formalisation)

Exploratory Great Pyramid core framework, Gravity Field Dynamics.
Companion to `../README.md` and `../verify_gp1_half_section.py`.

What is formalised (the algebraic content of Theorems 3–5 and Proposition 6):

* `share_strictAntiOn`  : `u ↦ (1-u)^n` is strictly decreasing on `[0,1]` (n ≥ 1).
* `balance_unique`      : at most one level in `[0,1]` has `(1-u)^n = 1/2`.
* `balance_level_rpow`  : that level is `u = 1 - (1/2)^(1/n)`, for every `n ≥ 1` (Theorem 3).
* `balance_level_D3`    : in `D = 3` (`n = 2`), `(1-u)^2 = 1/2 ↔ u = 1 - 1/√2` on `[0,1]`.
* `halvings_coincide_iff` : the horizontal halving `(1-u)^(D-1) = 1/2` and the meridional halving
                            `(1-u)^2 = 1/2` hold at a common level iff `D - 1 = 2` (Theorem 4).
* `canonical_levels_ordered` : volume level < area level < height level (Theorem 5).
* `volume_above_area_plane` : at the area level the volume fraction above is `(1/√2)^3 = √2/4`.
* `labelling` (Proposition 6) : `f_B = 13 + 8 μ_B` reads 21, 17, 13 at `μ_B = 1, 1/2, 0`.

Not formalised (checked by the script): the measure-theoretic section scaling of Theorem 1 and
the divergence-theorem flux balance of Theorem 2; the Petrie comparison (an observation).
-/

namespace GP1

open Real

/-- The structural share of a uniform current at fractional height `u`, in dimension `n + 1`. -/
noncomputable def share (n : ℕ) (u : ℝ) : ℝ := (1 - u) ^ n

/-- The share is strictly decreasing on `[0,1]`. -/
theorem share_strictAntiOn (n : ℕ) (hn : n ≠ 0) :
    StrictAntiOn (share n) (Set.Icc (0 : ℝ) 1) := by
  intro u hu v hv huv
  simp only [share]
  have h1 : 0 ≤ 1 - v := by linarith [hv.2]
  have h2 : 1 - v < 1 - u := by linarith
  exact pow_lt_pow_left₀ h2 h1 hn

/-- Uniqueness of the balance level. -/
theorem balance_unique (n : ℕ) (hn : n ≠ 0) {u v : ℝ}
    (hu : u ∈ Set.Icc (0 : ℝ) 1) (hv : v ∈ Set.Icc (0 : ℝ) 1)
    (h1 : share n u = 1 / 2) (h2 : share n v = 1 / 2) : u = v :=
  (share_strictAntiOn n hn).injOn hu hv (h1.trans h2.symm)

/-- The balance level in dimension `n + 1` is `1 - (1/2)^(1/n)` (Theorem 3). -/
theorem balance_level_rpow (n : ℕ) (hn : n ≠ 0) :
    share n (1 - (1 / 2 : ℝ) ^ ((n : ℝ)⁻¹)) = 1 / 2 := by
  simp only [share, sub_sub_cancel]
  exact Real.rpow_inv_natCast_pow (by norm_num) hn

/-- The balance level lies in `[0,1]`. -/
theorem balance_level_mem (n : ℕ) :
    1 - (1 / 2 : ℝ) ^ ((n : ℝ)⁻¹) ∈ Set.Icc (0 : ℝ) 1 := by
  have h0 : 0 ≤ (1 / 2 : ℝ) ^ ((n : ℝ)⁻¹) := Real.rpow_nonneg (by norm_num) _
  have h1 : (1 / 2 : ℝ) ^ ((n : ℝ)⁻¹) ≤ 1 :=
    Real.rpow_le_one (by norm_num) (by norm_num) (by positivity)
  constructor <;> linarith

/-- `D = 3`: the balance level is `1 - 1/√2`. -/
theorem balance_level_D3 {u : ℝ} (hu : u ∈ Set.Icc (0 : ℝ) 1) :
    (1 - u) ^ 2 = 1 / 2 ↔ u = 1 - 1 / Real.sqrt 2 := by
  have hs : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hspos : 0 < Real.sqrt 2 := by positivity
  constructor
  · intro h
    have ht : 0 ≤ 1 - u := by linarith [hu.2]
    -- (1-u) and 1/√2 are both nonnegative square roots of 1/2
    have hq : (1 / Real.sqrt 2) ^ 2 = 1 / 2 := by rw [div_pow, hs]; norm_num
    have : 1 - u = 1 / Real.sqrt 2 := by
      have hnn : 0 ≤ 1 / Real.sqrt 2 := by positivity
      nlinarith [sq_nonneg (1 - u - 1 / Real.sqrt 2), sq_nonneg (1 - u + 1 / Real.sqrt 2)]
    linarith
  · intro h
    rw [h, sub_sub_cancel, div_pow, hs]; norm_num

/-- Horizontal and meridional halvings coincide iff the section exponent is `2`, i.e. `D = 3`
(Theorem 4). Here `m = D - 1` is the exponent of the horizontal sections. -/
theorem halvings_coincide_iff (m : ℕ) :
    (∃ u ∈ Set.Icc (0 : ℝ) 1, (1 - u) ^ m = 1 / 2 ∧ (1 - u) ^ 2 = 1 / 2) ↔ m = 2 := by
  constructor
  · rintro ⟨u, hu, hm, h2⟩
    set t := 1 - u with ht
    have t0 : 0 ≤ t := by linarith [hu.2]
    have tpos : 0 < t := by
      rcases t0.lt_or_eq with h | h
      · exact h
      · rw [← h] at h2; norm_num at h2
    have t1 : t < 1 := by nlinarith
    rcases lt_trichotomy m 2 with hlt | heq | hgt
    · interval_cases m
      · norm_num at hm
      · -- t = 1/2 contradicts t^2 = 1/2
        rw [pow_one] at hm; rw [hm] at h2; norm_num at h2
    · exact heq
    · exfalso
      obtain ⟨k, rfl⟩ : ∃ k, m = k + 3 := ⟨m - 3, by omega⟩
      have hk : t ^ (k + 1) < 1 := pow_lt_one₀ t0 t1 (by omega)
      have : t ^ (k + 3) = t ^ 2 * t ^ (k + 1) := by ring
      rw [this, h2] at hm
      nlinarith
  · rintro rfl
    refine ⟨1 - 1 / Real.sqrt 2, ?_, ?_, ?_⟩
    · have hs : 1 < Real.sqrt 2 := by
        rw [show (1 : ℝ) = Real.sqrt 1 by simp]
        exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
      have hpos : 0 < 1 / Real.sqrt 2 := by positivity
      have hle : 1 / Real.sqrt 2 ≤ 1 := by
        rw [div_le_one (by positivity)]; linarith
      constructor <;> linarith
    all_goals
      rw [sub_sub_cancel, div_pow, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]; norm_num

/-- The three canonical halving levels are ordered: with `t₂² = 1/2` and `t₃³ = 1/2`
(the remaining fractions `1 - u` at the area and volume levels), `1/2 < t₂ < t₃`,
i.e. `u_volume < u_area < u_height = 1/2` (Theorem 5). -/
theorem canonical_levels_ordered {t₂ t₃ : ℝ} (h2 : 0 < t₂) (h3 : 0 < t₃)
    (e2 : t₂ ^ 2 = 1 / 2) (e3 : t₃ ^ 3 = 1 / 2) :
    1 - t₃ < 1 - t₂ ∧ 1 - t₂ < 1 / 2 := by
  have half : 1 / 2 < t₂ := by nlinarith
  have t2lt1 : t₂ < 1 := by nlinarith
  have key : t₂ < t₃ := by
    by_contra hc
    have hc : t₃ ≤ t₂ := not_lt.mp hc
    have : t₃ ^ 3 ≤ t₂ ^ 3 := pow_le_pow_left₀ h3.le hc 3
    have : t₂ ^ 3 = t₂ / 2 := by rw [pow_succ, e2]; ring
    nlinarith
  constructor <;> linarith

/-- At the area-balance level the volume fraction above is `(1/√2)^3 = √2/4 < 1/2`. -/
theorem volume_above_area_plane :
    (1 / Real.sqrt 2) ^ 3 = Real.sqrt 2 / 4 ∧ Real.sqrt 2 / 4 < 1 / 2 := by
  have hs : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hspos : 0 < Real.sqrt 2 := by positivity
  constructor
  · field_simp
    nlinarith
  · have : Real.sqrt 2 < 2 := by nlinarith
    linarith

/-- Proposition 6: the capacity labelling `f_B = 13 + 8 μ_B` (a labelling, not a derivation). -/
theorem labelling :
    (13 + 8 * (1 : ℝ) = 21) ∧ (13 + 8 * (1 / 2 : ℝ) = 17) ∧ (13 + 8 * (0 : ℝ) = 13) ∧
      ∀ μ : ℝ, 17 + 4 * (2 * μ - 1) = 13 + 8 * μ := by
  refine ⟨by norm_num, by norm_num, by norm_num, fun μ => by ring⟩

end GP1

#print axioms GP1.share_strictAntiOn
#print axioms GP1.balance_unique
#print axioms GP1.balance_level_rpow
#print axioms GP1.balance_level_mem
#print axioms GP1.balance_level_D3
#print axioms GP1.halvings_coincide_iff
#print axioms GP1.canonical_levels_ordered
#print axioms GP1.volume_above_area_plane
#print axioms GP1.labelling
