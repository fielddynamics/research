import Mathlib

/-!
# GP-4 · Registration and coherence (Lean 4 / Mathlib formalisation)

Exploratory Great Pyramid core framework, Gravity Field Dynamics.
Companion to `../README.md` and `../verify_gp4_registration_coherence.py`.

What is formalised:

* `abs_sin_nat_mul_le` : `|sin (n x)| ≤ n |sin x|` (the lemma of Theorem 3).
* `one_sub_cos_eq`     : `1 - cos y = 2 sin² (y/2)`.
* `one_sub_cos_nat_mul_le` : `1 - cos (n x) ≤ n² (1 - cos x)` (pointwise Theorem 3).
* `ensemble_bound` (Theorem 3): for any finite ensemble of phases `θᵢ` with weights `pᵢ ≥ 0`
  and any reference phase `φ`,
  `∑ pᵢ (1 - cos (n (θᵢ - φ))) ≤ n² ∑ pᵢ (1 - cos (θᵢ - φ))`.
  With `φ` the mean phase and `∑ pᵢ = 1` the right side is `n² (1 - C₁)`.
* `coprime_registration` (Theorem 4): in any field, `z³ = w³`, `z⁷ = w⁷`, `w ≠ 0` imply
  `z = w`: registration at the coprime orders 3 and 7 pins every phase to one value.
* `uniform_gon_harmonic` (Theorem 1): for a primitive `N`-th root `ζ`,
  `∑_{n<N} ζ^(d n) = N` if `N ∣ d` and `0` otherwise (the exact selector of Theorem 5).
* `mixture_coherence` (Theorem 2): the mixture `(1-t)·uniform N-gon + t·δ₀` has first harmonic
  `t` (for `N > 1`), while every atom is registered (`ζ^(nN) = 1`, `uniform_gon_registered`).
* `lock_minima` (Proposition 6): `cos (21 θ) = 1` at `θ = 2πn/21`.

Not formalised (checked by the script): the "only if" half of Theorem 1, the Parseval sidelobe
bound and the 14-character sum of Theorem 5.
-/

namespace GP4

open Real

/-- `|sin (n x)| ≤ n |sin x|`. -/
theorem abs_sin_nat_mul_le (n : ℕ) (x : ℝ) : |Real.sin (n * x)| ≤ n * |Real.sin x| := by
  induction n with
  | zero => simp
  | succ n ih =>
    have e : ((n + 1 : ℕ) : ℝ) * x = n * x + x := by push_cast; ring
    rw [e, Real.sin_add]
    have h1 : |Real.sin (n * x) * Real.cos x| ≤ |Real.sin (n * x)| := by
      rw [abs_mul]
      exact mul_le_of_le_one_right (abs_nonneg _) (Real.abs_cos_le_one x)
    have h2 : |Real.cos (n * x) * Real.sin x| ≤ |Real.sin x| := by
      rw [abs_mul]
      exact mul_le_of_le_one_left (abs_nonneg _) (Real.abs_cos_le_one _)
    calc |Real.sin (n * x) * Real.cos x + Real.cos (n * x) * Real.sin x|
        ≤ |Real.sin (n * x) * Real.cos x| + |Real.cos (n * x) * Real.sin x| := abs_add_le _ _
      _ ≤ n * |Real.sin x| + |Real.sin x| := by linarith
      _ = ((n + 1 : ℕ) : ℝ) * |Real.sin x| := by push_cast; ring

/-- `1 - cos y = 2 sin² (y/2)`. -/
theorem one_sub_cos_eq (y : ℝ) : 1 - Real.cos y = 2 * Real.sin (y / 2) ^ 2 := by
  have h := Real.cos_two_mul (y / 2)
  have h2 := Real.sin_sq_add_cos_sq (y / 2)
  rw [show 2 * (y / 2) = y by ring] at h
  linarith

/-- Pointwise form of Theorem 3. -/
theorem one_sub_cos_nat_mul_le (n : ℕ) (x : ℝ) :
    1 - Real.cos (n * x) ≤ (n : ℝ) ^ 2 * (1 - Real.cos x) := by
  rw [one_sub_cos_eq, one_sub_cos_eq]
  have h := abs_sin_nat_mul_le n (x / 2)
  have e : (n : ℝ) * x / 2 = n * (x / 2) := by ring
  rw [e]
  have hsq : Real.sin (n * (x / 2)) ^ 2 ≤ ((n : ℝ) * |Real.sin (x / 2)|) ^ 2 := by
    rw [← sq_abs]
    exact pow_le_pow_left₀ (abs_nonneg _) h 2
  have : ((n : ℝ) * |Real.sin (x / 2)|) ^ 2 = (n : ℝ) ^ 2 * Real.sin (x / 2) ^ 2 := by
    rw [mul_pow, sq_abs]
  nlinarith

/-- Theorem 3 for a finite ensemble: coherence implies registration. -/
theorem ensemble_bound {ι : Type*} (s : Finset ι) (p θ : ι → ℝ) (hp : ∀ i ∈ s, 0 ≤ p i)
    (n : ℕ) (φ : ℝ) :
    ∑ i ∈ s, p i * (1 - Real.cos (n * (θ i - φ))) ≤
      (n : ℝ) ^ 2 * ∑ i ∈ s, p i * (1 - Real.cos (θ i - φ)) := by
  rw [Finset.mul_sum]
  apply Finset.sum_le_sum
  intro i hi
  have := one_sub_cos_nat_mul_le n (θ i - φ)
  nlinarith [hp i hi]

/-- Theorem 4: registration at the coprime orders 3 and 7 forces a single phase. -/
theorem coprime_registration {F : Type*} [Field F] {z w : F} (hw : w ≠ 0)
    (h3 : z ^ 3 = w ^ 3) (h7 : z ^ 7 = w ^ 7) : z = w := by
  have ez : z ^ 7 = z * (z ^ 3) ^ 2 := by ring
  have ew : w ^ 7 = w * (w ^ 3) ^ 2 := by ring
  have hw3 : (w ^ 3) ^ 2 ≠ 0 := pow_ne_zero _ (pow_ne_zero _ hw)
  rw [ez, ew, h3] at h7
  exact mul_right_cancel₀ hw3 h7

/-- Theorem 1 / 5: the exact selector. -/
theorem uniform_gon_harmonic {R : Type*} [Field R] {ζ : R} {N : ℕ} (h : IsPrimitiveRoot ζ N)
    (d : ℕ) :
    ∑ k ∈ Finset.range N, ζ ^ (d * k) = if N ∣ d then (N : R) else 0 := by
  simp_rw [pow_mul]
  split_ifs with hd
  · have : ζ ^ d = 1 := (h.pow_eq_one_iff_dvd d).mpr hd
    simp [this]
  · have hne : ζ ^ d ≠ 1 := fun e => hd ((h.pow_eq_one_iff_dvd d).mp e)
    rw [geom_sum_eq hne]
    have : (ζ ^ d) ^ N = 1 := by rw [← pow_mul, mul_comm, pow_mul, h.pow_eq_one, one_pow]
    rw [this, sub_self, zero_div]

/-- Every atom of the (rotated) uniform `N`-gon is registered: `(ζ^n)^N = 1`. -/
theorem uniform_gon_registered {R : Type*} [CommMonoid R] {ζ : R} {N : ℕ}
    (h : IsPrimitiveRoot ζ N) (n : ℕ) : (ζ ^ n) ^ N = 1 := by
  rw [← pow_mul, mul_comm, pow_mul, h.pow_eq_one, one_pow]

/-- Theorem 2: the mixture `(1-t)·uniform + t·δ₀` has first harmonic `t` (for `N > 1`). -/
theorem mixture_coherence {R : Type*} [Field R] {ζ : R} {N : ℕ} (h : IsPrimitiveRoot ζ N)
    (hN : 1 < N) (t : R) :
    ∑ n ∈ Finset.range N, ((1 - t) / N + if n = 0 then t else 0) * ζ ^ n = t := by
  simp_rw [add_mul, Finset.sum_add_distrib, ← Finset.mul_sum]
  rw [h.geom_sum_eq_zero hN, mul_zero, zero_add]
  simp [Finset.sum_ite_eq', Finset.mem_range, show 0 < N by omega]

/-- Proposition 6: the 21 minima of `-cos (21 θ)`. -/
theorem lock_minima (n : ℤ) : Real.cos (21 * (2 * π * n / 21)) = 1 := by
  rw [show 21 * (2 * π * n / 21) = (n : ℝ) * (2 * π) by ring]
  exact Real.cos_int_mul_two_pi n

end GP4

#print axioms GP4.abs_sin_nat_mul_le
#print axioms GP4.one_sub_cos_eq
#print axioms GP4.one_sub_cos_nat_mul_le
#print axioms GP4.ensemble_bound
#print axioms GP4.coprime_registration
#print axioms GP4.uniform_gon_harmonic
#print axioms GP4.uniform_gon_registered
#print axioms GP4.mixture_coherence
#print axioms GP4.lock_minima
