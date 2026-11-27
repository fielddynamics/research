import Mathlib

/-!
# GP-3 · Coupling signatures and the hinge (Lean 4 / Mathlib formalisation)

Exploratory Great Pyramid core framework, Gravity Field Dynamics.
Companion to `../README.md` and `../verify_gp3_signatures_hinge.py`.

`f K s = 1 + s K + K²` over `ℤ`.

What is formalised:

* `sig_plus_eq_cyclotomic`, `sig_zero_eq_cyclotomic`, `sig_minus_eq_cyclotomic` (Theorem 1): the three signatures are
  Mathlib's `cyclotomic 3`, `cyclotomic 4`, `cyclotomic 6` evaluated at `K`.
* `integer_s_in_open_interval` (Theorem 1): the integers `s` with `|s| < 2` are `-1, 0, 1`;
  `f_two`, `f_neg_two`: the endpoints `s = ±2` are the squares `(K ± 1)²`.
* `hinge` and `hinge_unique` (Theorem 2): `f K 1 = f (K+1) (-1)`, and for `K, K' ≥ 1`,
  `s, s' ∈ {-1,0,1}`, every coincidence `f K s = f K' s'` with `(K,s) ≠ (K',s')` is a hinge.
* `seventeen_unique` : `f K s = 17` only at `(K,s) = (4,0)` (for `K ≥ 1`, `s ∈ {-1,0,1}`).
* `coprime_plus_minus`, `coprime_zero_plus`, `coprime_zero_minus` (Theorem 3): pairwise coprime
  for every integer `K`; `midpoint`: `f K 1 + f K (-1) = 2 f K 0`.
* `fusion`, `fusion'`, `tower` (Theorem 4); `tower_pairwise_coprime`, `tower_head_coprime` (Theorem 4b:
  the whole fusion tower is pairwise coprime, for every integer `K`).
* `graded_trace` and `involution_multiplicities` (Theorem 6).

Not formalised (checked by the script): `φ(n) = 2 ↔ n ∈ {3,4,6}` and Niven's theorem (cited);
the finite-field enumerations of Theorem 5.
-/

namespace GP3

/-- The coupling polynomial. -/
def f (K s : ℤ) : ℤ := 1 + s * K + K ^ 2

open Polynomial in
theorem sig_plus_eq_cyclotomic (K : ℤ) : (cyclotomic 3 ℤ).eval K = f K 1 := by
  rw [Polynomial.cyclotomic_three]
  simp only [eval_add, eval_pow, eval_X, eval_one]
  unfold f; ring

open Polynomial in
theorem sig_zero_eq_cyclotomic (K : ℤ) : (cyclotomic 4 ℤ).eval K = f K 0 := by
  have h := Polynomial.cyclotomic_expand_eq_cyclotomic Nat.prime_two (dvd_refl 2) ℤ
  rw [Polynomial.cyclotomic_two] at h
  rw [show (4 : ℕ) = 2 * 2 from rfl, ← h]
  simp only [map_add, map_one, expand_X, eval_add, eval_pow, eval_X, eval_one]
  unfold f; ring

open Polynomial in
theorem sig_minus_eq_cyclotomic (K : ℤ) : (cyclotomic 6 ℤ).eval K = f K (-1) := by
  have h1 := Polynomial.cyclotomic_expand_eq_cyclotomic_mul Nat.prime_two
    (by norm_num : ¬ 2 ∣ 3) ℤ
  rw [Polynomial.cyclotomic_three] at h1
  have hX : (X ^ 2 + X + 1 : ℤ[X]) ≠ 0 := by
    intro h0
    have := congrArg (Polynomial.eval 0) h0
    simp at this
  have h6 : cyclotomic 6 ℤ = X ^ 2 - X + 1 := by
    apply mul_right_cancel₀ hX
    rw [show (6 : ℕ) = 3 * 2 from rfl, ← h1]
    simp only [map_add, map_pow, map_one, expand_X]
    ring
  rw [h6]
  simp only [eval_add, eval_sub, eval_pow, eval_X, eval_one]
  unfold f; ring

/-- The integers strictly inside `(-2, 2)`. -/
theorem integer_s_in_open_interval (s : ℤ) : |s| < 2 ↔ s = -1 ∨ s = 0 ∨ s = 1 := by
  constructor
  · intro h; rw [abs_lt] at h; omega
  · rintro (rfl | rfl | rfl) <;> norm_num

theorem f_two (K : ℤ) : f K 2 = (K + 1) ^ 2 := by unfold f; ring
theorem f_neg_two (K : ℤ) : f K (-2) = (K - 1) ^ 2 := by unfold f; ring

/-- The hinge identity. -/
theorem hinge (K : ℤ) : f K 1 = f (K + 1) (-1) := by unfold f; ring

lemma same_s {K K' s : ℤ} (hK : 1 ≤ K) (hK' : 1 ≤ K') (hs : -1 ≤ s)
    (h : f K s = f K' s) : K = K' := by
  simp only [f] at h
  have : (K - K') * (K + K' + s) = 0 := by linear_combination h
  rcases mul_eq_zero.mp this with h1 | h1
  · linarith
  · exfalso; linarith

lemma not_square_pronic {K n : ℤ} (hK : 0 ≤ K) (hn : 1 ≤ n) : K ^ 2 ≠ n ^ 2 + n := by
  intro h
  rcases le_or_gt K n with h1 | h1
  · nlinarith
  · have : n + 1 ≤ K := by omega
    nlinarith

lemma not_square_pronic' {K n : ℤ} (hK : 1 ≤ K) (hn : 1 ≤ n) : K ^ 2 ≠ n ^ 2 - n := by
  intro h
  rcases le_or_gt K (n - 1) with h1 | h1
  · nlinarith
  · have : n ≤ K := by omega
    nlinarith

lemma plus_minus {K K' : ℤ} (hK : 1 ≤ K) (hK' : 1 ≤ K') (h : f K 1 = f K' (-1)) :
    K' = K + 1 := by
  simp only [f] at h
  rcases le_or_gt K' K with h1 | h1
  · exfalso; nlinarith
  · rcases le_or_gt K' (K + 1) with h2 | h2
    · omega
    · exfalso
      have : K + 2 ≤ K' := by omega
      nlinarith

/-- Theorem 2: the hinge is the only coincidence between levels. -/
theorem hinge_unique {K K' s s' : ℤ} (hK : 1 ≤ K) (hK' : 1 ≤ K')
    (hs : s = -1 ∨ s = 0 ∨ s = 1) (hs' : s' = -1 ∨ s' = 0 ∨ s' = 1)
    (h : f K s = f K' s') :
    (K = K' ∧ s = s') ∨ (s = 1 ∧ s' = -1 ∧ K' = K + 1) ∨ (s = -1 ∧ s' = 1 ∧ K = K' + 1) := by
  rcases hs with rfl | rfl | rfl <;> rcases hs' with rfl | rfl | rfl
  · exact Or.inl ⟨same_s hK hK' (by norm_num) h, rfl⟩
  · -- f K (-1) = f K' 0 : K'^2 = K^2 - K
    exfalso; simp only [f] at h
    exact not_square_pronic' (K := K') (n := K) hK' hK (by linear_combination (-1 : ℤ) * h)
  · exact Or.inr (Or.inr ⟨rfl, rfl, plus_minus hK' hK h.symm⟩)
  · exfalso; simp only [f] at h
    exact not_square_pronic' (K := K) (n := K') hK hK' (by linear_combination h)
  · exact Or.inl ⟨same_s hK hK' (by norm_num) h, rfl⟩
  · exfalso; simp only [f] at h
    exact not_square_pronic (K := K) (n := K') (by linarith) hK' (by linear_combination h)
  · exact Or.inr (Or.inl ⟨rfl, rfl, plus_minus hK hK' h⟩)
  · exfalso; simp only [f] at h
    exact not_square_pronic (K := K') (n := K) (by linarith) hK (by linear_combination (-1 : ℤ) * h)
  · exact Or.inl ⟨same_s hK hK' (by norm_num) h, rfl⟩

/-- 17 belongs to `K = 4`, `s = 0` alone. -/
theorem seventeen_unique {K s : ℤ} (hK : 1 ≤ K) (hs : s = -1 ∨ s = 0 ∨ s = 1)
    (h : f K s = 17) : K = 4 ∧ s = 0 := by
  have h4 : f 4 0 = 17 := by norm_num [f]
  rcases hinge_unique hK (by norm_num : (1 : ℤ) ≤ 4) hs (Or.inr (Or.inl rfl)) (h.trans h4.symm)
    with ⟨h1, h2⟩ | ⟨_, h2, _⟩ | ⟨_, h2, _⟩
  · exact ⟨h1, h2⟩
  · norm_num at h2
  · norm_num at h2

/-- Theorem 3: `f K 1` and `f K (-1)` are coprime for every integer `K`. -/
theorem coprime_plus_minus (K : ℤ) : IsCoprime (f K 1) (f K (-1)) := by
  obtain ⟨t, ht⟩ := Int.even_mul_succ_self K
  refine ⟨f K 1 - 2 * t - (K + 1) * K + t * (K + 1), -t * (K + 1), ?_⟩
  simp only [f]
  linear_combination ht

theorem coprime_zero_plus (K : ℤ) : IsCoprime (f K 0) (f K 1) :=
  ⟨1 + K, -K, by simp only [f]; ring⟩

theorem coprime_zero_minus (K : ℤ) : IsCoprime (f K 0) (f K (-1)) :=
  ⟨1 - K, K, by simp only [f]; ring⟩

theorem gcd_one (K : ℤ) :
    Int.gcd (f K 1) (f K (-1)) = 1 ∧ Int.gcd (f K 0) (f K 1) = 1 ∧ Int.gcd (f K 0) (f K (-1)) = 1 :=
  ⟨Int.isCoprime_iff_gcd_eq_one.mp (coprime_plus_minus K),
   Int.isCoprime_iff_gcd_eq_one.mp (coprime_zero_plus K),
   Int.isCoprime_iff_gcd_eq_one.mp (coprime_zero_minus K)⟩

theorem midpoint (K : ℤ) : f K 1 + f K (-1) = 2 * f K 0 := by unfold f; ring

/-- Theorem 4: fusion. -/
theorem fusion (K : ℤ) : f K 1 * f K (-1) = f (K ^ 2) 1 := by unfold f; ring

theorem fusion' (K : ℤ) : f K 1 * f K (-1) = 1 + K ^ 2 * f K 0 := by unfold f; ring

/-- Theorem 4: the tower `f(K^(2^n), 1) = f(K,1) ∏_{j<n} f(K^(2^j), -1)`. -/
theorem tower (K : ℤ) (n : ℕ) :
    f (K ^ (2 ^ n)) 1 = f K 1 * ∏ j ∈ Finset.range n, f (K ^ (2 ^ j)) (-1) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Finset.prod_range_succ, ← mul_assoc, ← ih, fusion, ← pow_mul, ← pow_succ]

/-- Theorem 4b: every tower factor `B_j = f(K^(2^j), -1)` with `j < n` divides `A_n = f(K^(2^n), 1)`. -/
theorem tower_factor_dvd (K : ℤ) {j n : ℕ} (hj : j < n) :
    f (K ^ (2 ^ j)) (-1) ∣ f (K ^ (2 ^ n)) 1 := by
  rw [tower]
  exact Dvd.dvd.mul_left (Finset.dvd_prod_of_mem _ (Finset.mem_range.mpr hj)) _

/-- Theorem 4b: `A_0 = f(K, 1)` divides every `A_n`. -/
theorem tower_head_dvd (K : ℤ) (n : ℕ) : f K 1 ∣ f (K ^ (2 ^ n)) 1 := by
  rw [tower]; exact dvd_mul_right _ _

/-- Theorem 4b: the tower factors `B_j` and `B_n` (`j < n`) are coprime, for every integer `K`. -/
theorem tower_pairwise_coprime (K : ℤ) {j n : ℕ} (hj : j < n) :
    IsCoprime (f (K ^ (2 ^ j)) (-1)) (f (K ^ (2 ^ n)) (-1)) :=
  (coprime_plus_minus (K ^ (2 ^ n))).of_isCoprime_of_dvd_left (tower_factor_dvd K hj)

/-- Theorem 4b: the head `A_0` is coprime to every `B_n`. -/
theorem tower_head_coprime (K : ℤ) (n : ℕ) : IsCoprime (f K 1) (f (K ^ (2 ^ n)) (-1)) :=
  (coprime_plus_minus (K ^ (2 ^ n))).of_isCoprime_of_dvd_left (tower_head_dvd K n)


theorem tower_at_four :
    f 4 1 = 21 ∧ f 4 (-1) = 13 ∧ f 4 0 = 17 ∧ f 16 1 = 273 ∧ f 16 (-1) = 241 ∧
      f 256 1 = 65793 ∧ 21 * 13 * 241 = (65793 : ℤ) ∧ f 5 (-1) = 21 ∧ f 3 1 = 13 := by
  norm_num [f]

/-- Theorem 6: graded trace on `1 ⊕ V ⊕ V⊗V` (dimensions `1, K, K²`). -/
theorem graded_trace (K s : ℤ) : (1 : ℤ) + s * K + K ^ 2 = f K s := rfl

/-- Theorem 6: an involution with traces 21 (of `I`) and 13 (of `J`) has multiplicities (17, 4). -/
theorem involution_multiplicities {mp mm : ℤ} (h1 : mp + mm = 21) (h2 : mp - mm = 13) :
    mp = 17 ∧ mm = 4 := by
  constructor <;> omega

end GP3

#print axioms GP3.sig_plus_eq_cyclotomic
#print axioms GP3.sig_zero_eq_cyclotomic
#print axioms GP3.sig_minus_eq_cyclotomic
#print axioms GP3.integer_s_in_open_interval
#print axioms GP3.f_two
#print axioms GP3.f_neg_two
#print axioms GP3.hinge
#print axioms GP3.hinge_unique
#print axioms GP3.seventeen_unique
#print axioms GP3.coprime_plus_minus
#print axioms GP3.coprime_zero_plus
#print axioms GP3.coprime_zero_minus
#print axioms GP3.gcd_one
#print axioms GP3.midpoint
#print axioms GP3.fusion
#print axioms GP3.fusion'
#print axioms GP3.tower
#print axioms GP3.tower_factor_dvd
#print axioms GP3.tower_head_dvd
#print axioms GP3.tower_pairwise_coprime
#print axioms GP3.tower_head_coprime
#print axioms GP3.tower_at_four
#print axioms GP3.graded_trace
#print axioms GP3.involution_multiplicities
