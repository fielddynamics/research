import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Topology.Algebra.Order.Field
import Mathlib.Analysis.Normed.Group.Real
import Mathlib.Tactic.LinearCombination

/-!
# Lean 4 / Mathlib formalisation of
#   S. Nelson, "The Constitutive Law from Exchange Symmetry"

## How to referee this file
A Lean proof can only be wrong in its *statements*. Check these definitions against the paper:
* `rel a b c d x m := a·x·m + b·x + c·m + d = 0`: the bilinear relation of premise (A) with
  `x = x̃`, `m = μ`; non-degeneracy `ad − bc ≠ 0` is the irreducibility the lemma gives.
* A law is a function `μ` on `[0, ∞)` with `rel` and values in `[0, 1]`.
* `states a b μ`: the partition states realised on `[0, ∞]`: the values `μ x` for `x ≥ 0`, and at
  `x = ∞` the points of the projective closure in `x` (where `x(a m + b) + (c m + d) = 0` reads
  `a m + b = 0`) that lie in `[0, 1]`.
* (E) is `μ 0 = 0`; (X) is `∀ m ∈ states, 1 − m ∈ states`.
* `law x = x / (x + 1)`.

The field-degree statement of the lemma (`[K(x,y):K(x)] = m` via Gauss's lemma) is not
formalised; its use in the proof, that a bilinear relation is irreducible only if `ad − bc ≠ 0`
and is then solvable both ways, is (`lemma_bilinear`).
-/

open Filter Topology

namespace ConstitutiveLaw

/-- The bilinear relation `a x μ + b x + c μ + d = 0`. -/
def rel (a b c d x m : ℝ) : Prop := a * x * m + b * x + c * m + d = 0

/-- The partition states realised on `[0, ∞]`. -/
def states (a b : ℝ) (μ : ℝ → ℝ) : Set ℝ :=
  {m | ∃ x, 0 ≤ x ∧ μ x = m} ∪ {m | 0 ≤ m ∧ m ≤ 1 ∧ a * m + b = 0}

/-- The constitutive law `μ(x) = x / (x + 1)`. -/
noncomputable def law (x : ℝ) : ℝ := x / (x + 1)

/-! ## The lemma, in the form the proof uses -/

/-- **Lemma (bilinear case).** A relation of degree one in each variable factors into a polynomial
in `x` times one in `y` when `ad − bc = 0`, so irreducibility forces `ad − bc ≠ 0`; when
`ad − bc ≠ 0` each variable is a fractional linear function of the other. -/
theorem lemma_bilinear (a b c d : ℝ) :
    ((a ≠ 0 ∨ b ≠ 0) → (a ≠ 0 ∨ c ≠ 0) → a * d - b * c = 0 →
      a ≠ 0 ∧ ∃ t : ℝ, ∀ x y, a * x * y + b * x + c * y + d = (x + t) * (a * y + b)) ∧
    (a * d - b * c ≠ 0 →
      (∀ x y, a * x + c ≠ 0 → (rel a b c d x y ↔ y = -(b * x + d) / (a * x + c))) ∧
      (∀ x y, a * y + b ≠ 0 → (rel a b c d x y ↔ x = -(c * y + d) / (a * y + b))) ∧
      (∀ x, a * x + c = 0 → ¬ ∃ y, rel a b c d x y)) := by
  refine ⟨fun hx hy h => ?_, fun h => ⟨fun x y hxc => ?_, fun x y hyb => ?_, fun x hxc => ?_⟩⟩
  · have ha : a ≠ 0 := by
      intro ha; subst ha
      have hb : b ≠ 0 := hx.resolve_left (by simp)
      have hc : c ≠ 0 := hy.resolve_left (by simp)
      apply hb; have : b * c = 0 := by linarith
      rcases mul_eq_zero.mp this with h | h
      · exact h
      · exact absurd h hc
    refine ⟨ha, c / a, fun x y => ?_⟩
    have hd : d = b * c / a := by field_simp; linarith
    rw [hd]; field_simp; ring
  · rw [rel, eq_div_iff hxc]
    constructor <;> intro h' <;> linarith
  · rw [rel, eq_div_iff hyb]
    constructor <;> intro h' <;> linarith
  · rintro ⟨y, hy⟩
    rw [rel] at hy
    have e1 : (a * x + c) * y + (b * x + d) = 0 := by linarith
    rw [hxc, zero_mul, zero_add] at e1
    -- `a x = −c` and `b x = −d` give `ad − bc = 0`
    apply h
    have : a * (b * x + d) - b * (a * x + c) = a * d - b * c := by ring
    rw [e1, hxc] at this; linarith

/-! ## The unique law -/

/-- **Theorem.** Under (E), (X) and (A), the relation is `μ = kx/(kx + 1)` for a unique `k > 0`;
writing `x' = kx` (that is, `x' = g/a₀` with `a₀ = g_*/k`), `μ = x'/(x' + 1)`. -/
theorem unique_law (a b c d : ℝ) (hA : a * d - b * c ≠ 0) (μ : ℝ → ℝ)
    (hrel : ∀ x, 0 ≤ x → rel a b c d x (μ x))
    (hrange : ∀ x, 0 ≤ x → 0 ≤ μ x ∧ μ x ≤ 1)
    (hE : μ 0 = 0)
    (hX : ∀ m ∈ states a b μ, 1 - m ∈ states a b μ) :
    d = 0 ∧ a + b = 0 ∧ ∃ k : ℝ, 0 < k ∧ (∀ x, 0 ≤ x → μ x = law (k * x)) ∧
      ∀ k' : ℝ, 0 < k' → (∀ x, 0 ≤ x → μ x = law (k' * x)) → k' = k := by
  -- Step 1: d = 0, so bc ≠ 0
  have hd : d = 0 := by have := hrel 0 le_rfl; rw [rel, hE] at this; linarith
  subst hd
  have hbc : b * c ≠ 0 := by intro h; apply hA; linarith
  have hb : b ≠ 0 := left_ne_zero_of_mul hbc
  have hc : c ≠ 0 := right_ne_zero_of_mul hbc
  have hden : ∀ x, 0 ≤ x → a * x + c ≠ 0 := by
    intro x hx h
    have := hrel x hx
    rw [rel] at this
    have e : (a * x + c) * μ x + b * x = 0 := by linarith
    rw [h, zero_mul, zero_add] at e
    rcases mul_eq_zero.mp e with h1 | h1
    · exact hb h1
    · subst h1; simp at h; exact hc h
  have hμ : ∀ x, 0 ≤ x → μ x = -(b * x) / (a * x + c) := by
    intro x hx
    rw [eq_div_iff (hden x hx)]
    have := hrel x hx; rw [rel] at this; linarith
  -- 1 - μ (in odds form, `Ω = −bx/((a+b)x + c)`)
  have hm : ∀ x, 0 ≤ x → μ x * (a * x + c) = -(b * x) := fun x hx => by
    rw [hμ x hx, div_mul_cancel₀ _ (hden x hx)]
  have h1μ : ∀ x, 0 ≤ x → (1 - μ x) * (a * x + c) = (a + b) * x + c := by
    intro x hx; rw [sub_mul, one_mul, hm x hx]; ring
  -- Step 2: the state 1 is realised
  have h0 : (0 : ℝ) ∈ states a b μ := Or.inl ⟨0, le_rfl, hE⟩
  have h1 := hX 0 h0
  rw [sub_zero] at h1
  have hab : a + b = 0 := by
    rcases h1 with ⟨x₀, hx₀, hμ₀⟩ | ⟨-, -, h⟩
    · -- realised at a finite x₀: then (a + b) x₀ = −c, and the odds change sign
      by_contra hne
      have e := h1μ x₀ hx₀
      rw [hμ₀, sub_self, zero_mul] at e
      have hx₀pos : 0 < x₀ := by
        rcases hx₀.lt_or_eq with h | h
        · exact h
        · exfalso; subst h; apply hc; linarith [e]
      -- μ(1 − μ) ≥ 0 gives −b((a + b)x + c) ≥ 0 for every x > 0
      have hsign : ∀ x, 0 < x → 0 ≤ -b * ((a + b) * x + c) := by
        intro x hx
        have hr := hrange x hx.le
        have hprod : 0 ≤ μ x * ((1 - μ x) * (a * x + c) ^ 2) := by
          have : 0 ≤ μ x * (1 - μ x) := mul_nonneg hr.1 (by linarith [hr.2])
          have := mul_nonneg this (sq_nonneg (a * x + c))
          linarith [show μ x * (1 - μ x) * (a * x + c) ^ 2 =
            μ x * ((1 - μ x) * (a * x + c) ^ 2) by ring]
        have e2 : μ x * ((1 - μ x) * (a * x + c) ^ 2) =
            x * (-b * ((a + b) * x + c)) := by
          have h1' := h1μ x hx.le
          calc μ x * ((1 - μ x) * (a * x + c) ^ 2)
              = (μ x * (a * x + c)) * ((1 - μ x) * (a * x + c)) := by ring
            _ = x * (-b * ((a + b) * x + c)) := by rw [hm x hx.le, h1']; ring
        rw [e2] at hprod
        exact (mul_nonneg_iff_of_pos_left hx).mp hprod
      have hc' : c = -((a + b) * x₀) := by linarith
      have s1 := hsign (x₀ / 2) (by linarith)
      have s2 := hsign (2 * x₀) (by linarith)
      rw [hc'] at s1 s2
      have : b * (a + b) * x₀ = 0 := by nlinarith
      rcases mul_eq_zero.mp this with h | h
      · rcases mul_eq_zero.mp h with h | h
        · exact hb h
        · exact hne h
      · linarith
    · -- realised at x = ∞: a·1 + b = 0
      linarith
  -- Step 3: the scale
  set k := -b / c with hk
  have hlaw : ∀ x, 0 ≤ x → μ x = law (k * x) := by
    intro x hx
    rw [hμ x hx, law, hk]
    have ha : a = -b := by linarith
    rw [ha]
    have hx' : -b * x + c ≠ 0 := by have := hden x hx; rwa [ha] at this
    field_simp
  have hkpos : 0 < k := by
    by_contra hk0
    push Not at hk0
    have hk0' : k < 0 := lt_of_le_of_ne hk0 (by rw [hk]; exact div_ne_zero (neg_ne_zero.mpr hb) hc)
    -- at x = −1/(2k) > 0, μ = −1 < 0
    have hxpos : 0 ≤ -1 / (2 * k) := by
      apply div_nonneg_of_nonpos (by norm_num); linarith
    have hv := hlaw _ hxpos
    have hkne : k ≠ 0 := hk0'.ne
    have : law (k * (-1 / (2 * k))) = -1 := by
      rw [law, show k * (-1 / (2 * k)) = -1 / 2 by field_simp]; norm_num
    rw [this] at hv
    linarith [(hrange _ hxpos).1]
  refine ⟨rfl, hab, k, hkpos, hlaw, fun k' hk' hlaw' => ?_⟩
  have e := (hlaw' 1 zero_le_one).symm.trans (hlaw 1 zero_le_one)
  rw [law, law, mul_one, mul_one, div_eq_div_iff (by linarith) (by linarith)] at e
  linarith

/-! ## Consequences -/

/-- **Consequences.** The screening identity; `μ(0) = 0`; `μ(1) = ½`; `μ → 1` as `x → ∞` (the second
endpoint, derived); `μ(x) + μ(1/x) = 1`; the relation is carried to itself by
`(x, μ) → (1/x, 1 − μ)`; `μ` is strictly increasing, so the state exchanged with the one at `x`
sits exactly at `1/x`, an involution with fixed point `x = 1`. -/
theorem consequences :
    (∀ x, 0 ≤ x → x * (1 - law x) = law x) ∧ law 0 = 0 ∧ law 1 = 1 / 2 ∧
      Tendsto law atTop (𝓝 1) ∧
      (∀ x, 0 < x → law x + law (1 / x) = 1) ∧
      (∀ x m : ℝ, 0 < x → (x * (1 - m) = m ↔ (1 / x) * (1 - (1 - m)) = 1 - m)) ∧
      StrictMonoOn law (Set.Ici 0) ∧
      (∀ x y, 0 < x → 0 ≤ y → (law y = 1 - law x ↔ y = 1 / x)) ∧
      (∀ x : ℝ, x ≠ 0 → 1 / (1 / x) = x) ∧ (∀ x : ℝ, 0 < x → (1 / x = x ↔ x = 1)) := by
  have hpos : ∀ x : ℝ, 0 ≤ x → x + 1 ≠ 0 := fun x hx => by linarith
  have mono : StrictMonoOn law (Set.Ici 0) := by
    intro x hx y hy hxy
    simp only [Set.mem_Ici] at hx hy
    rw [law, law, div_lt_div_iff₀ (by linarith) (by linarith)]
    nlinarith
  have hcomp : ∀ x, 0 < x → law x + law (1 / x) = 1 := by
    intro x hx; rw [law, law]; field_simp; ring
  refine ⟨fun x hx => ?_, by simp [law], by norm_num [law], ?_, hcomp, fun x m hx => ?_, mono,
    fun x y hx hy => ?_, fun x hx => by field_simp, fun x hx => ?_⟩
  · rw [law]; field_simp [hpos x hx]; ring
  · have heq : (fun x : ℝ => 1 - (x + 1)⁻¹) =ᶠ[atTop] law := by
      filter_upwards [eventually_ge_atTop (0 : ℝ)] with x hx
      rw [law]; field_simp [hpos x hx]; ring
    have h1 : Tendsto (fun x : ℝ => x + 1) atTop atTop := tendsto_atTop_add_const_right _ 1 tendsto_id
    have h2 := (tendsto_const_nhds (x := (1 : ℝ))).sub (tendsto_inv_atTop_zero.comp h1)
    simp only [sub_zero] at h2
    exact h2.congr' heq
  · rw [sub_sub_cancel, one_div_mul_eq_div, div_eq_iff hx.ne']
    constructor <;> intro h <;> linarith
  · constructor
    · intro h
      have e : law y = law (1 / x) := by rw [h]; linarith [hcomp x hx]
      exact mono.injOn hy (by simp only [Set.mem_Ici]; positivity) e
    · rintro rfl; linarith [hcomp x hx]
  · constructor
    · intro h
      have h' := mul_one_div_cancel hx.ne'
      rw [h] at h'
      have : (x - 1) * (x + 1) = 0 := by nlinarith
      rcases mul_eq_zero.mp this with h' | h'
      · linarith
      · linarith
    · rintro rfl; norm_num

/-- **Parity form.** With `s = 2μ − 1`: `x(1 − s) = 1 + s`, `s(x) = (x − 1)/(x + 1)`, the exchange is
`(x, s) → (1/x, −s)`, and the normalised rank-one term of `f(K, s) = 1 + sK + K²` is `μ = (1 + s)/2`. -/
theorem parity_form :
    (∀ x, 0 ≤ x → 2 * law x - 1 = (x - 1) / (x + 1)) ∧
      (∀ x, 0 ≤ x → x * (1 - (2 * law x - 1)) = 1 + (2 * law x - 1)) ∧
      (∀ x, 0 < x → 2 * law (1 / x) - 1 = -(2 * law x - 1)) ∧
      (∀ K s : ℝ, K ≠ 0 →
        ((1 + s * K + K ^ 2) - (1 + (-1) * K + K ^ 2)) / (2 * K) = (1 + s) / 2) := by
  refine ⟨fun x hx => ?_, fun x hx => ?_, fun x hx => ?_, fun K s hK => ?_⟩
  · rw [law]; field_simp; ring
  · rw [law]; field_simp; ring
  · rw [law, law]; field_simp; ring
  · field_simp; ring

/-! ## Necessity of the premises -/

/-- **(E) is necessary.** `Ω = (x + ½)/(½x + 1)`: bilinear and non-degenerate, values in `[0,1]`,
closed under exchange, but `μ(0) = 1/3`. -/
theorem need_E :
    ∃ a b c d : ℝ, ∃ μ : ℝ → ℝ, a * d - b * c ≠ 0 ∧ (∀ x, 0 ≤ x → rel a b c d x (μ x)) ∧
      (∀ x, 0 ≤ x → 0 ≤ μ x ∧ μ x ≤ 1) ∧ (∀ m ∈ states a b μ, 1 - m ∈ states a b μ) ∧
      μ 0 ≠ 0 := by
  -- μ = (x + ½)/((3/2)(x + 1)): (3/2) x μ − x + (3/2) μ − ½ = 0
  let μ : ℝ → ℝ := fun x => (x + 1 / 2) / (3 / 2 * (x + 1))
  refine ⟨3 / 2, -1, 3 / 2, -1 / 2, μ, by norm_num, fun x hx => ?_, fun x hx => ⟨?_, ?_⟩, ?_, ?_⟩
  · simp only [rel, μ]; field_simp; ring
  · positivity
  · rw [div_le_one (by positivity)]; linarith
  · have hμinv : ∀ x, 0 < x → 1 - μ x = μ (1 / x) := by
      intro x hx; simp only [μ]; field_simp; ring
    rintro m (⟨x, hx, rfl⟩ | ⟨-, -, hm⟩)
    · rcases hx.lt_or_eq with hx | hx
      · exact Or.inl ⟨1 / x, by positivity, (hμinv x hx).symm⟩
      · subst hx; right; refine ⟨by norm_num [μ], by norm_num [μ], by norm_num [μ]⟩
    · have : m = 2 / 3 := by linarith
      subst this
      exact Or.inl ⟨0, le_rfl, by norm_num [μ]⟩
  · norm_num [μ]

/-- **(X) is necessary.** `Ω = x/(x + 1)`, i.e. `μ = x/(2x + 1)`: bilinear, non-degenerate, (E), values
in `[0, 1]`, but the state `0` has no exchanged state `1`. -/
theorem need_X :
    ∃ a b c d : ℝ, ∃ μ : ℝ → ℝ, a * d - b * c ≠ 0 ∧ (∀ x, 0 ≤ x → rel a b c d x (μ x)) ∧
      (∀ x, 0 ≤ x → 0 ≤ μ x ∧ μ x ≤ 1) ∧ μ 0 = 0 ∧
      ¬ (∀ m ∈ states a b μ, 1 - m ∈ states a b μ) := by
  let μ : ℝ → ℝ := fun x => x / (2 * x + 1)
  refine ⟨2, -1, 1, 0, μ, by norm_num, fun x hx => ?_, fun x hx => ⟨?_, ?_⟩, by simp [μ], ?_⟩
  · simp only [rel, μ]; field_simp; ring
  · positivity
  · rw [div_le_one (by positivity)]; linarith
  · intro h
    have := h 0 (Or.inl ⟨0, le_rfl, by simp [μ]⟩)
    rw [sub_zero] at this
    rcases this with ⟨x, hx, hx1⟩ | ⟨-, -, h2⟩
    · simp only [μ] at hx1
      rw [div_eq_one_iff_eq (by positivity)] at hx1; linarith
    · norm_num at h2

/-- The relation `xⁿ(1 − μ)ᵐ = μ`. -/
def relA (n m : ℕ) (x y : ℝ) : Prop := x ^ n * (1 - y) ^ m = y

/-- **(A) is necessary.** For every `n, m ≥ 1`, `xⁿ(1 − μ)ᵐ = μ` has exactly one root `μ ∈ [0, 1]`
for each `x ≥ 0`; the resulting law satisfies (E), runs from `0` to `1` (its states on `[0, ∞]` are
all of `[0, 1]`, so (X) holds); and for `(n, m) ≠ (1, 1)` it is not `x/(x + 1)` in any unit.
`(n, m) = (1, 2)` is the bound-state law. -/
theorem need_A (n m : ℕ) (hn : 1 ≤ n) (hm : 1 ≤ m) :
    ∃ μ : ℝ → ℝ, (∀ x, 0 ≤ x → relA n m x (μ x) ∧ 0 ≤ μ x ∧ μ x ≤ 1) ∧
      (∀ x y, 0 ≤ x → 0 ≤ y → y ≤ 1 → relA n m x y → y = μ x) ∧
      μ 0 = 0 ∧
      ({y | ∃ x, 0 ≤ x ∧ μ x = y} ∪ {1} = Set.Icc 0 1) ∧
      ((n, m) ≠ (1, 1) → ∀ k : ℝ, 0 < k → ∃ x, 0 ≤ x ∧ μ x ≠ law (k * x)) := by
  set F : ℝ → ℝ → ℝ := fun x y => x ^ n * (1 - y) ^ m - y with hF
  have hcont : ∀ x, Continuous (F x) := fun x => by
    simp only [hF]; fun_prop
  -- strictly decreasing in `y` on `[0, 1]`
  have hanti : ∀ x, 0 ≤ x → ∀ y₁ y₂, 0 ≤ y₁ → y₁ < y₂ → y₂ ≤ 1 → F x y₂ < F x y₁ := by
    intro x hx y₁ y₂ h1 h12 h2
    simp only [hF]
    have : (1 - y₂) ^ m ≤ (1 - y₁) ^ m := pow_le_pow_left₀ (by linarith) (by linarith) m
    have := mul_le_mul_of_nonneg_left this (pow_nonneg hx n)
    linarith
  have hexists : ∀ x, 0 ≤ x → ∃ y, 0 ≤ y ∧ y ≤ 1 ∧ F x y = 0 := by
    intro x hx
    have h0 : 0 ≤ F x 0 := by simp only [hF]; simp; positivity
    have h1 : F x 1 ≤ 0 := by simp only [hF]; simp [zero_pow (by omega : m ≠ 0)]
    obtain ⟨y, hy, hFy⟩ := intermediate_value_Icc' (zero_le_one' ℝ) (hcont x).continuousOn
      ⟨h1, h0⟩
    exact ⟨y, hy.1, hy.2, hFy⟩
  have huniq : ∀ x, 0 ≤ x → ∀ y₁ y₂, 0 ≤ y₁ → y₁ ≤ 1 → 0 ≤ y₂ → y₂ ≤ 1 →
      F x y₁ = 0 → F x y₂ = 0 → y₁ = y₂ := by
    intro x hx y₁ y₂ a1 b1 a2 b2 e1 e2
    rcases lt_trichotomy y₁ y₂ with h | h | h
    · have := hanti x hx y₁ y₂ a1 h b2; linarith
    · exact h
    · have := hanti x hx y₂ y₁ a2 h b1; linarith
  classical
  let μ : ℝ → ℝ := fun x => if hx : 0 ≤ x then (hexists x hx).choose else 0
  have hμ : ∀ x (hx : 0 ≤ x), 0 ≤ μ x ∧ μ x ≤ 1 ∧ F x (μ x) = 0 := by
    intro x hx; simp only [μ, hx, ↓reduceDIte]; exact (hexists x hx).choose_spec
  have hrelA : ∀ x y, relA n m x y ↔ F x y = 0 := fun x y => by
    simp only [relA, hF, sub_eq_zero]
  have hroot : ∀ x y, 0 ≤ x → 0 ≤ y → y ≤ 1 → relA n m x y → y = μ x := by
    intro x y hx h0 h1 hr
    exact huniq x hx y (μ x) h0 h1 (hμ x hx).1 (hμ x hx).2.1 ((hrelA x y).mp hr) (hμ x hx).2.2
  have hμ0 : μ 0 = 0 := by
    symm; apply hroot 0 0 le_rfl le_rfl zero_le_one
    simp [relA, zero_pow (by omega : n ≠ 0)]
  refine ⟨μ, fun x hx => ⟨(hrelA _ _).mpr (hμ x hx).2.2, (hμ x hx).1, (hμ x hx).2.1⟩, hroot, hμ0,
    ?_, ?_⟩
  · ext y
    simp only [Set.mem_union, Set.mem_ofPred_eq, Set.mem_singleton_iff, Set.mem_Icc]
    constructor
    · rintro (⟨x, hx, rfl⟩ | rfl)
      · exact ⟨(hμ x hx).1, (hμ x hx).2.1⟩
      · norm_num
    · rintro ⟨h0, h1⟩
      rcases h1.lt_or_eq with h1 | h1
      · left
        -- solve `xⁿ = y/(1 − y)ᵐ` for `x ≥ 0` by the intermediate value theorem
        set t := y / (1 - y) ^ m with ht
        have htnn : 0 ≤ t := div_nonneg h0 (pow_nonneg (by linarith) m)
        have hpow : t ≤ (t + 1) ^ n := by
          calc t ≤ t + 1 := by linarith
            _ = (t + 1) ^ 1 := (pow_one _).symm
            _ ≤ (t + 1) ^ n := pow_le_pow_right₀ (by linarith) hn
        obtain ⟨x, hx, hxt⟩ := intermediate_value_Icc (by linarith : (0 : ℝ) ≤ t + 1)
          (continuous_pow n).continuousOn
          ⟨show (0 : ℝ) ^ n ≤ t by rw [zero_pow (by omega)]; exact htnn, hpow⟩
        refine ⟨x, hx.1, (hroot x y hx.1 h0 h1.le ?_).symm⟩
        simp only [relA, hxt, ht]
        rw [div_mul_cancel₀ _ (pow_ne_zero m (by linarith))]
      · right; exact h1
  · intro hnm k hk
    by_contra hall
    push Not at hall
    obtain ⟨n', rfl⟩ : ∃ n', n = n' + 1 := ⟨n - 1, by omega⟩
    obtain ⟨m', rfl⟩ : ∃ m', m = m' + 1 := ⟨m - 1, by omega⟩
    -- on the law, the relation reads `x^{n−1} = k (kx + 1)^{m−1}`
    have key : ∀ x, 0 < x → x ^ n' = k * (k * x + 1) ^ m' := by
      intro x hx
      have hr := (hrelA _ _).mpr (hμ x hx.le).2.2
      rw [hall x hx.le, law] at hr
      simp only [relA] at hr
      have hu : 0 < k * x + 1 := by positivity
      have e1 : 1 - k * x / (k * x + 1) = 1 / (k * x + 1) := by field_simp; ring
      rw [e1, one_div, inv_pow, pow_succ, pow_succ] at hr
      have hu' : (k * x + 1) ≠ 0 := hu.ne'
      have hum : (k * x + 1) ^ m' ≠ 0 := pow_ne_zero _ hu'
      field_simp at hr
      linear_combination hr
    rcases Nat.eq_zero_or_pos n' with hn0 | hn0
    · -- n = 1, so m ≥ 2: compare x = 1/k and x = 2/k
      subst hn0
      have hm' : 1 ≤ m' := by
        by_contra h; apply hnm; have : m' = 0 := by omega
        subst this; rfl
      have e1 := key (1 / k) (by positivity)
      have e2 := key (2 / k) (by positivity)
      rw [show k * (1 / k) + 1 = 2 by field_simp; ring] at e1
      rw [show k * (2 / k) + 1 = 3 by field_simp; ring] at e2
      have : (2 : ℝ) ^ m' < 3 ^ m' := pow_lt_pow_left₀ (by norm_num) (by norm_num) (by omega)
      have := mul_lt_mul_of_pos_left this hk
      simp at e1 e2
      linarith
    · -- n ≥ 2: at a small x, x^{n−1} < k ≤ k (kx + 1)^{m−1}
      set x := min 1 k / 2 with hxdef
      have hx0 : 0 < x := by positivity
      have hx1 : x ≤ 1 := by have := min_le_left 1 k; linarith
      have hxk : x < k := by have := min_le_right 1 k; linarith
      have e := key x hx0
      have h1 : x ^ n' ≤ x := by
        calc x ^ n' ≤ x ^ 1 := pow_le_pow_of_le_one hx0.le hx1 hn0
          _ = x := pow_one x
      have h2 : 1 ≤ (k * x + 1) ^ m' := one_le_pow₀ (by nlinarith)
      nlinarith

/-- **Without (A) the exchange carries no content.** Any continuous `μ` on `[0, ∞)` with
`μ(0) = 0`, values in `[0, 1]` and `μ → 1` realises every state in `[0, 1)`, so with the state `1`
at `x = ∞` its states are all of `[0, 1]` and (E), (X) hold. -/
theorem no_content_without_A (μ : ℝ → ℝ) (hc : ContinuousOn μ (Set.Ici 0)) (h0 : μ 0 = 0)
    (hr : ∀ x, 0 ≤ x → 0 ≤ μ x ∧ μ x ≤ 1) (hlim : Tendsto μ atTop (𝓝 1)) :
    {y | ∃ x, 0 ≤ x ∧ μ x = y} ∪ {1} = Set.Icc 0 1 := by
  ext y
  simp only [Set.mem_union, Set.mem_ofPred_eq, Set.mem_singleton_iff, Set.mem_Icc]
  constructor
  · rintro (⟨x, hx, rfl⟩ | rfl)
    · exact hr x hx
    · norm_num
  · rintro ⟨hy0, hy1⟩
    rcases hy1.lt_or_eq with hy1 | hy1
    · left
      obtain ⟨X, hX⟩ := (hlim.eventually (lt_mem_nhds hy1)).exists_forall_of_atTop
      set X' := max X 0
      have hX' : y < μ X' := hX X' (le_max_left _ _)
      obtain ⟨x, hx, hxy⟩ := intermediate_value_Icc (le_max_right X 0)
        (hc.mono fun z hz => hz.1) ⟨by rw [h0]; exact hy0, hX'.le⟩
      exact ⟨x, hx.1, hxy⟩
    · right; exact hy1

#print axioms ConstitutiveLaw.lemma_bilinear
#print axioms ConstitutiveLaw.unique_law
#print axioms ConstitutiveLaw.consequences
#print axioms ConstitutiveLaw.parity_form
#print axioms ConstitutiveLaw.need_E
#print axioms ConstitutiveLaw.need_X
#print axioms ConstitutiveLaw.need_A
#print axioms ConstitutiveLaw.no_content_without_A

end ConstitutiveLaw
