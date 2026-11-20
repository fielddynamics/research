import ConstitutiveLaw
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.Convex.StrictConvexSpace
import Mathlib.Analysis.InnerProductSpace.Convex
import Mathlib.Analysis.Convex.Deriv
import Mathlib.Analysis.Calculus.Deriv.MeanValue

/-!
# Lean 4 / Mathlib formalisation of
#   S. Nelson, "The Energy Functional of the Constitutive Law μ(x) = x/(x+1)"

Builds on `ConstitutiveLaw`: `μ` is its `law x = x/(x + 1)`.

## How to referee this file
A Lean proof can only be wrong in its *statements*. Check these definitions against the paper:
* `F y = y − 2√y + 2 ln(1 + √y)`, Eq. (4); `g r = r² − 2r + 2 ln(1 + r)`, so `F (r²) = g r` for
  `r ≥ 0` (`F_sq`).
* `W q = F ‖q‖²` on any real inner product space `E` (the paper's `ℝ³` is
  `EuclideanSpace ℝ (Fin 3)`), with `q = ∇Φ/a₀`.
* `G q = 2μ(‖q‖) q`, the gradient of `W`; `A q = μ(‖q‖) q = ½ G q` is the field-equation flux in
  units `a₀ = 1`.
* `H q`: the Hessian, `2μ(x)·I + (2/((1+x)²x))·q qᵀ`, which is Eq. (6) rewritten.

## What is cited, not proved
Corollary 2's divergence-theorem step (integration by parts on a bounded domain); Lean proves its
pointwise heart, the strict monotonicity of `A` (`A_strictMono`). The series of Corollary 1 at
the single point `y = 1` (Abel's theorem); Lean proves it for `0 ≤ y < 1`, with a remainder bound
valid on all of `[0, ∞)`.
-/

open Real Filter Topology Set

namespace AqualEnergy

open ConstitutiveLaw (law)

/-- The kinetic function, Eq. (4). -/
noncomputable def F (y : ℝ) : ℝ := y - 2 * √y + 2 * log (1 + √y)

/-- Its radial form, `g r = F (r²)`. -/
noncomputable def g (r : ℝ) : ℝ := r ^ 2 - 2 * r + 2 * log (1 + r)

lemma F_sq {r : ℝ} (hr : 0 ≤ r) : F (r ^ 2) = g r := by
  simp [F, g, sqrt_sq hr]

lemma F_eq_g_sqrt {y : ℝ} (hy : 0 ≤ y) : F y = g (√y) := by
  rw [← F_sq (sqrt_nonneg y), sq_sqrt hy]

/-! ## Theorem 1: the kinetic function -/

lemma hasDerivAt_g {r : ℝ} (hr : -1 < r) : HasDerivAt g (2 * r ^ 2 / (1 + r)) r := by
  have h1 : 1 + r ≠ 0 := by linarith
  have hl : HasDerivAt (fun r => log (1 + r)) (1 / (1 + r)) r := by
    have := ((hasDerivAt_id r).const_add 1).log h1
    simpa using this
  have := (((hasDerivAt_pow 2 r).sub ((hasDerivAt_id r).const_mul 2)).add (hl.const_mul 2))
  convert this using 1
  · funext x; simp [g]
  · field_simp; ring

/-- `F' (y) = μ(√y)` for `y > 0`. -/
theorem hasDerivAt_F {y : ℝ} (hy : 0 < y) : HasDerivAt F (law (√y)) y := by
  have hs : HasDerivAt (fun y => √y) (1 / (2 * √y)) y := hasDerivAt_sqrt hy.ne'
  have hu : 0 < √y := sqrt_pos.mpr hy
  have h1 : 1 + √y ≠ 0 := by linarith
  have hl : HasDerivAt (fun y => log (1 + √y)) ((1 / (2 * √y)) / (1 + √y)) y :=
    (hs.const_add 1).log h1
  have := ((hasDerivAt_id y).sub (hs.const_mul 2)).add (hl.const_mul 2)
  convert this using 1
  · funext x; simp [F]
  · rw [law]; field_simp; ring

lemma continuous_F : Continuous F := by
  unfold F
  have hpos : ∀ y : ℝ, 1 + √y ≠ 0 := fun y => by linarith [sqrt_nonneg y]
  fun_prop (disch := exact hpos _)

/-- A function vanishing at `0` with nonnegative derivative on `(0, ∞)` is nonnegative on `[0, ∞)`. -/
lemma nonneg_of_deriv {h h' : ℝ → ℝ} (hc : ContinuousOn h (Ici 0))
    (hd : ∀ u, 0 < u → HasDerivAt h (h' u) u) (h0 : h 0 = 0) (hpos : ∀ u, 0 < u → 0 ≤ h' u) :
    ∀ u, 0 ≤ u → 0 ≤ h u := by
  intro u hu
  rcases hu.lt_or_eq with hu | hu
  · obtain ⟨c, hc', hcd⟩ := exists_hasDerivAt_eq_slope h h' hu
      (hc.mono Icc_subset_Ici_self) fun x hx => hd x hx.1
    rw [h0, sub_zero, sub_zero, eq_div_iff hu.ne'] at hcd
    rw [← hcd]; exact mul_nonneg (hpos c hc'.1) hu.le
  · rw [← hu, h0]

lemma continuousOn_g : ContinuousOn g (Ici 0) := by
  have : ∀ r ∈ Ici (0 : ℝ), 1 + r ≠ 0 := fun r hr => by simp at hr; linarith
  unfold g
  exact ((continuousOn_pow 2).sub (continuousOn_const.mul continuousOn_id)).add
    (continuousOn_const.mul ((continuousOn_const.add continuousOn_id).log this))

/-- **Bounds at low acceleration.** For `u ≥ 0`: `0 ≤ g u ≤ ⅔u³` and
`0 ≤ g u − ⅔u³ + ½u⁴ ≤ ⅖u⁵`, i.e. `F = ⅔ y^{3/2} − ½ y² + O(y^{5/2})`. -/
theorem g_bounds {u : ℝ} (hu : 0 ≤ u) :
    0 ≤ g u ∧ g u ≤ 2 / 3 * u ^ 3 ∧ 0 ≤ g u - 2 / 3 * u ^ 3 + u ^ 4 / 2 ∧
      g u - 2 / 3 * u ^ 3 + u ^ 4 / 2 ≤ 2 / 5 * u ^ 5 := by
  have hg0 : g 0 = 0 := by simp [g]
  have hd : ∀ u : ℝ, 0 < u → HasDerivAt g (2 * u ^ 2 / (1 + u)) u := fun u hu =>
    hasDerivAt_g (by linarith)
  have b0 : 0 ≤ g u :=
    nonneg_of_deriv continuousOn_g hd hg0 (fun u hu => by positivity) u hu
  -- ⅔u³ − g
  have b1 : 0 ≤ 2 / 3 * u ^ 3 - g u := by
    have hc : ContinuousOn (fun u : ℝ => 2 / 3 * u ^ 3 - g u) (Ici 0) :=
      (continuous_const.mul (continuous_pow 3)).continuousOn.sub continuousOn_g
    have hd' : ∀ u : ℝ, 0 < u →
        HasDerivAt (fun u : ℝ => 2 / 3 * u ^ 3 - g u) (2 * u ^ 3 / (1 + u)) u := by
      intro u hu
      have := ((hasDerivAt_pow 3 u).const_mul (2 / 3)).sub (hd u hu)
      convert this using 1; field_simp; ring
    exact nonneg_of_deriv hc hd' (by simp [hg0]) (fun u hu => by positivity) u hu
  -- g − ⅔u³ + ½u⁴
  have b2 : 0 ≤ g u - 2 / 3 * u ^ 3 + u ^ 4 / 2 := by
    have hc : ContinuousOn (fun u : ℝ => g u - 2 / 3 * u ^ 3 + u ^ 4 / 2) (Ici 0) :=
      (continuousOn_g.sub (continuous_const.mul (continuous_pow 3)).continuousOn).add
        ((continuous_pow 4).div_const 2).continuousOn
    have hd' : ∀ u : ℝ, 0 < u →
        HasDerivAt (fun u : ℝ => g u - 2 / 3 * u ^ 3 + u ^ 4 / 2) (2 * u ^ 4 / (1 + u)) u := by
      intro u hu
      have := ((hd u hu).sub ((hasDerivAt_pow 3 u).const_mul (2 / 3))).add
        ((hasDerivAt_pow 4 u).div_const 2)
      convert this using 1; field_simp; ring
    exact nonneg_of_deriv hc hd' (by simp [hg0]) (fun u hu => by positivity) u hu
  -- ⅖u⁵ − (g − ⅔u³ + ½u⁴)
  have b3 : 0 ≤ 2 / 5 * u ^ 5 - (g u - 2 / 3 * u ^ 3 + u ^ 4 / 2) := by
    have hc : ContinuousOn (fun u : ℝ => 2 / 5 * u ^ 5 - (g u - 2 / 3 * u ^ 3 + u ^ 4 / 2))
        (Ici 0) :=
      (continuous_const.mul (continuous_pow 5)).continuousOn.sub
        ((continuousOn_g.sub (continuous_const.mul (continuous_pow 3)).continuousOn).add
          ((continuous_pow 4).div_const 2).continuousOn)
    have hd' : ∀ u : ℝ, 0 < u →
        HasDerivAt (fun u : ℝ => 2 / 5 * u ^ 5 - (g u - 2 / 3 * u ^ 3 + u ^ 4 / 2))
          (2 * u ^ 5 / (1 + u)) u := by
      intro u hu
      have := ((hasDerivAt_pow 5 u).const_mul (2 / 5)).sub
        (((hd u hu).sub ((hasDerivAt_pow 3 u).const_mul (2 / 3))).add
          ((hasDerivAt_pow 4 u).div_const 2))
      convert this using 1; field_simp; ring
    exact nonneg_of_deriv hc hd' (by simp [hg0]) (fun u hu => by positivity) u hu
  exact ⟨b0, by linarith, b2, by linarith⟩

/-- **Theorem 1.** `F` is continuous on `[0, ∞)`, `F(0) = 0`, `F' = μ(√y)` for `y > 0`, the right
derivative at `0` is `μ(0) = 0`, and `F` is the unique such function. -/
theorem theorem1 :
    F 0 = 0 ∧ ContinuousOn F (Ici 0) ∧ (∀ y, 0 < y → HasDerivAt F (law (√y)) y) ∧
      HasDerivWithinAt F (law (√0)) (Ici 0) 0 ∧
      ∀ F₂ : ℝ → ℝ, F₂ 0 = 0 → ContinuousOn F₂ (Ici 0) →
        (∀ y, 0 < y → HasDerivAt F₂ (law (√y)) y) → ∀ y, 0 ≤ y → F₂ y = F y := by
  refine ⟨by simp [F], continuous_F.continuousOn, fun y hy => hasDerivAt_F hy, ?_, ?_⟩
  · -- `0 ≤ F y ≤ ⅔ y √y`
    rw [show law (√0) = 0 by simp [law]]
    rw [hasDerivWithinAt_iff_isLittleO]
    simp only [sub_zero, smul_zero, F, sqrt_zero, add_zero, log_one, mul_zero]
    rw [Asymptotics.isLittleO_iff]
    intro c hc
    have hev : ∀ᶠ y in 𝓝[Ici 0] (0 : ℝ), y ∈ Ici (0 : ℝ) ∧ √y ≤ 3 / 2 * c := by
      refine (eventually_mem_nhdsWithin (s := Ici (0 : ℝ))).and ?_
      have : ContinuousAt (fun y : ℝ => √y) 0 := continuous_sqrt.continuousAt
      have h := this.eventually (gt_mem_nhds (by rw [sqrt_zero]; positivity : √0 < 3 / 2 * c))
      exact Filter.Eventually.mono (nhdsWithin_le_nhds h) fun y hy => hy.le
    filter_upwards [hev] with y ⟨hy, hys⟩
    simp only [mem_Ici] at hy
    have hb := g_bounds (sqrt_nonneg y)
    have e : y - 2 * √y + 2 * log (1 + √y) = g (√y) := (F_eq_g_sqrt hy)
    rw [e, Real.norm_eq_abs, Real.norm_eq_abs, abs_of_nonneg hb.1, abs_of_nonneg hy]
    have : (√y) ^ 3 = y * √y := by rw [pow_succ, sq_sqrt hy]
    calc g (√y) ≤ 2 / 3 * √y ^ 3 := hb.2.1
      _ = 2 / 3 * √y * y := by rw [this]; ring
      _ ≤ 2 / 3 * (3 / 2 * c) * y := by gcongr
      _ = c * y := by ring
  · intro F₂ h0 hc hd y hy
    rcases hy.lt_or_eq with hy | hy
    · obtain ⟨c, hc', hcd⟩ := exists_hasDerivAt_eq_slope (fun y => F₂ y - F y) (fun _ => 0) hy
        ((hc.sub continuous_F.continuousOn).mono Icc_subset_Ici_self)
        fun x hx => ((hd x hx.1).sub (hasDerivAt_F hx.1)).congr_deriv (by ring)
      rw [eq_comm, div_eq_zero_iff] at hcd
      rcases hcd with h | h
      · simp [h0, show F 0 = 0 by simp [F]] at h; linarith
      · linarith
    · subst hy; simp [h0, F]

/-! ## Corollary 1: the two limits -/

/-- **Corollary 1, low acceleration.** For `0 ≤ y < 1`,
`F y = 2 Σ_{k ≥ 3} (−1)^{k+1} y^{k/2}/k` (here `k = n + 3`). -/
theorem series_small {y : ℝ} (hy : 0 ≤ y) (hy1 : y < 1) :
    HasSum (fun n : ℕ => 2 * ((-1) ^ n * √y ^ (n + 3) / (n + 3))) (F y) := by
  set u := √y with hu
  have hu0 : 0 ≤ u := sqrt_nonneg y
  have hu1 : u < 1 := by rw [hu, sqrt_lt' one_pos]; simpa using hy1
  have h := hasSum_pow_div_log_of_abs_lt_one (x := -u) (by rw [abs_neg, abs_of_nonneg hu0]; exact hu1)
  rw [sub_neg_eq_add] at h
  have h2 := (hasSum_nat_add_iff' 2).mpr h
  simp only [Finset.sum_range_succ, Finset.sum_range_zero] at h2
  have h3 := h2.mul_left (-2)
  rw [F_eq_g_sqrt hy, ← hu, g]
  convert h3 using 1
  · funext n
    push_cast
    rw [neg_pow]
    ring
  · norm_num; ring

/-- **Corollary 1, high acceleration.** For `y > 1`,
`F y = y − 2√y + ln y + 2 Σ_{k ≥ 1} (−1)^{k+1} y^{−k/2}/k`, and the remainder `F − (y − 2√y + ln y)`
lies in `(0, 2/√y]` for every `y > 0`. -/
theorem series_large :
    (∀ y : ℝ, 1 < y → HasSum (fun n : ℕ => 2 * ((-1) ^ n * (1 / √y) ^ (n + 1) / (n + 1)))
      (F y - (y - 2 * √y + log y))) ∧
    (∀ y : ℝ, 0 < y → 0 < F y - (y - 2 * √y + log y) ∧
      F y - (y - 2 * √y + log y) ≤ 2 / √y) := by
  have key : ∀ y : ℝ, 0 < y → F y - (y - 2 * √y + log y) = 2 * log (1 + 1 / √y) := by
    intro y hy
    have hu : 0 < √y := sqrt_pos.mpr hy
    have : log y = 2 * log (√y) := by
      rw [← log_rpow hu, show ((2 : ℝ)) = ((2 : ℕ) : ℝ) by norm_num, rpow_natCast, sq_sqrt hy.le]
    rw [F, this, show 1 + 1 / √y = (1 + √y) / √y by field_simp; ring,
      log_div (by positivity) hu.ne']
    ring
  refine ⟨fun y hy => ?_, fun y hy => ?_⟩
  · have hu : 1 < √y := by rw [lt_sqrt zero_le_one]; simpa using hy
    have hx : |-(1 / √y)| < 1 := by
      rw [abs_neg, abs_of_pos (by positivity), div_lt_one (by linarith)]; exact hu
    have h := hasSum_pow_div_log_of_abs_lt_one hx
    rw [sub_neg_eq_add] at h
    have h3 := h.mul_left (-2)
    rw [key y (by linarith)]
    convert h3 using 1
    · funext n; rw [neg_pow]; ring
    · ring
  · rw [key y hy]
    have hu : 0 < √y := sqrt_pos.mpr hy
    have hpos : 0 < 1 / √y := by positivity
    refine ⟨by have := log_pos (by linarith : (1 : ℝ) < 1 + 1 / √y); linarith, ?_⟩
    have := log_le_sub_one_of_pos (by positivity : (0 : ℝ) < 1 + 1 / √y)
    have e : 2 / √y = 2 * (1 / √y) := by ring
    rw [e]; linarith

/-! ## Theorem 2: convexity and ellipticity -/

section Vector

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- The energy density `W(q) = F(|q|²)`. -/
noncomputable def W (q : E) : ℝ := F (‖q‖ ^ 2)

/-- Its gradient `∇W(q) = 2μ(|q|) q`. -/
noncomputable def G (q : E) : E := (2 * law ‖q‖) • q

/-- The flux `A(q) = μ(|q|) q` of the field equation (units `a₀ = 1`). -/
noncomputable def A (q : E) : E := law ‖q‖ • q

/-- The Hessian at `q`, `2μ(x) I + (2/((1+x)² x)) q qᵀ`. -/
noncomputable def H (q : E) : E →L[ℝ] E :=
  (2 * law ‖q‖) • ContinuousLinearMap.id ℝ E +
    (2 / ((1 + ‖q‖) ^ 2 * ‖q‖)) • (innerSL ℝ q).smulRight q

omit [InnerProductSpace ℝ E] in
lemma W_eq (q : E) : W q = g ‖q‖ := F_sq (norm_nonneg q)

/-- **Theorem 2 (first derivative).** `W` is differentiable everywhere with gradient `G`. -/
theorem hasFDerivAt_W (q : E) : HasFDerivAt W (innerSL ℝ (G q)) q := by
  rcases eq_or_ne q 0 with rfl | hq
  · -- `|W q| ≤ ⅔|q|³`
    simp only [G, smul_zero, map_zero]
    rw [hasFDerivAt_iff_isLittleO_nhds_zero]
    simp only [zero_add, zero_apply, sub_zero, W, norm_zero]
    rw [show F (0 ^ 2) = 0 by simp [F]]
    rw [Asymptotics.isLittleO_iff]
    intro c hc
    have hev : ∀ᶠ h in 𝓝 (0 : E), ‖h‖ ≤ min 1 (3 / 2 * c) := by
      have : ContinuousAt (fun h : E => ‖h‖) 0 := continuous_norm.continuousAt
      have h := this.eventually (gt_mem_nhds
        (by rw [norm_zero]; positivity : ‖(0 : E)‖ < min 1 (3 / 2 * c)))
      exact h.mono fun y hy => hy.le
    filter_upwards [hev] with h hh
    rw [sub_zero, F_sq (norm_nonneg h), Real.norm_eq_abs]
    have hb := g_bounds (norm_nonneg h)
    rw [abs_of_nonneg hb.1]
    have h1 : ‖h‖ ≤ 1 := hh.trans (min_le_left _ _)
    have h2 : ‖h‖ ≤ 3 / 2 * c := hh.trans (min_le_right _ _)
    have hn := norm_nonneg h
    calc g ‖h‖ ≤ 2 / 3 * ‖h‖ ^ 3 := hb.2.1
      _ = 2 / 3 * ‖h‖ * ‖h‖ * ‖h‖ := by ring
      _ ≤ 2 / 3 * (3 / 2 * c) * 1 * ‖h‖ := by gcongr
      _ = c * ‖h‖ := by ring
  · have hpos : 0 < ‖q‖ ^ 2 := by positivity
    have h1 := (hasDerivAt_F hpos).comp_hasFDerivAt q (hasStrictFDerivAt_norm_sq q).hasFDerivAt
    have hW : (W : E → ℝ) = fun v => F (‖v‖ ^ 2) := rfl
    rw [hW]
    refine h1.congr_fderiv ?_
    ext v
    simp [G, sqrt_sq (norm_nonneg q)]
    ring

lemma hasDerivAt_c {r : ℝ} (hr : -1 < r) :
    HasDerivAt (fun r => 2 * law r) (2 / (1 + r) ^ 2) r := by
  have h1 : r + 1 ≠ 0 := by linarith
  have := ((hasDerivAt_id r).div ((hasDerivAt_id r).add_const 1) h1).const_mul 2
  convert this using 1
  · funext x; simp [law]
  · simp only [id]; ring

lemma hasFDerivAt_norm' {q : E} (hq : q ≠ 0) :
    HasFDerivAt (fun x : E => ‖x‖) ((1 / ‖q‖) • innerSL ℝ q) q := by
  have hpos : ‖q‖ ^ 2 ≠ 0 := by positivity
  have h := (hasStrictFDerivAt_norm_sq q).hasFDerivAt.sqrt hpos
  have e : (fun x : E => √(‖x‖ ^ 2)) = fun x => ‖x‖ := by
    funext x; exact sqrt_sq (norm_nonneg x)
  rw [e] at h
  convert h using 1
  rw [sqrt_sq (norm_nonneg q)]
  ext v
  simp
  field_simp

/-- **Theorem 2 (second derivative).** At `q ≠ 0` the gradient `G` has derivative `H q`; at `q = 0`
its derivative is `0`. -/
theorem hasFDerivAt_G {q : E} (hq : q ≠ 0) : HasFDerivAt G (H q) q := by
  have hn := hasFDerivAt_norm' hq
  have hc := (hasDerivAt_c (by linarith [norm_nonneg q] : -1 < ‖q‖)).comp_hasFDerivAt q hn
  have h := hc.smul (hasFDerivAt_id q)
  have hG : (G : E → E) = fun x => (2 * law ‖x‖) • id x := rfl
  rw [hG]
  refine h.congr_fderiv ?_
  have : ‖q‖ ≠ 0 := norm_ne_zero_iff.mpr hq
  ext v
  simp [H, smul_smul]
  field_simp

theorem hasFDerivAt_G_zero : HasFDerivAt (G : E → E) (0 : E →L[ℝ] E) (0 : E) := by
  rw [hasFDerivAt_iff_isLittleO_nhds_zero]
  simp only [zero_add, zero_apply, sub_zero, G, norm_zero, smul_zero]
  rw [Asymptotics.isLittleO_iff]
  intro c hc
  have hev : ∀ᶠ h in 𝓝 (0 : E), ‖h‖ ≤ c / 2 := by
    have : ContinuousAt (fun h : E => ‖h‖) 0 := continuous_norm.continuousAt
    have h := this.eventually (gt_mem_nhds (by rw [norm_zero]; positivity : ‖(0 : E)‖ < c / 2))
    exact h.mono fun y hy => hy.le
  filter_upwards [hev] with h hh
  rw [norm_smul, Real.norm_eq_abs]
  have hl : 0 ≤ law ‖h‖ := by unfold law; positivity
  have hl2 : law ‖h‖ ≤ ‖h‖ := by
    unfold law; rw [div_le_iff₀ (by positivity)]; nlinarith [norm_nonneg h]
  rw [abs_of_nonneg (by positivity)]
  calc 2 * law ‖h‖ * ‖h‖ ≤ 2 * ‖h‖ * ‖h‖ := by gcongr
    _ ≤ 2 * (c / 2) * ‖h‖ := by gcongr
    _ = c * ‖h‖ := by ring

/-- **The Hessian, Eq. (6).** Along `q` the eigenvalue is `2(xμ)' = 2x(x+2)/(x+1)²`; on `q^⊥` it is
`2μ = 2x/(1+x)`; both positive; their ratio `(x+2)/(x+1)` lies in `(1, 2]`; `(xμ)'` is the
derivative of `x μ(x)`; and `‖H q‖ ≤ 4|q|`, so the Hessian is continuous at `0` with value `0`. -/
theorem hessian {q : E} (hq : q ≠ 0) :
    H q q = (2 * ‖q‖ * (‖q‖ + 2) / (‖q‖ + 1) ^ 2) • q ∧
      (∀ v, inner ℝ q v = 0 → H q v = (2 * law ‖q‖) • v) ∧
      0 < 2 * law ‖q‖ ∧ 0 < 2 * ‖q‖ * (‖q‖ + 2) / (‖q‖ + 1) ^ 2 ∧
      (2 * ‖q‖ * (‖q‖ + 2) / (‖q‖ + 1) ^ 2) / (2 * law ‖q‖) = (‖q‖ + 2) / (‖q‖ + 1) ∧
      1 < (‖q‖ + 2) / (‖q‖ + 1) ∧ (‖q‖ + 2) / (‖q‖ + 1) ≤ 2 ∧
      HasDerivAt (fun x => x * law x) (‖q‖ * (‖q‖ + 2) / (‖q‖ + 1) ^ 2) ‖q‖ ∧
      ‖H q‖ ≤ 4 * ‖q‖ := by
  have hr : 0 < ‖q‖ := norm_pos_iff.mpr hq
  set r := ‖q‖ with hrdef
  have hlaw : law r = r / (r + 1) := rfl
  refine ⟨?_, fun v hv => ?_, ?_, by positivity, ?_, ?_, ?_, ?_, ?_⟩
  · simp only [H, add_apply, smul_apply,
      ContinuousLinearMap.id_apply, ContinuousLinearMap.smulRight_apply, innerSL_apply_apply,
      real_inner_self_eq_norm_sq, smul_smul, ← add_smul, ← hrdef]
    congr 1; rw [hlaw]; field_simp; ring
  · simp [H, hv]; rfl
  · rw [hlaw]; positivity
  · rw [hlaw]; field_simp
  · rw [lt_div_iff₀ (by linarith)]; linarith
  · rw [div_le_iff₀ (by linarith)]; linarith
  · have h1 : r + 1 ≠ 0 := by linarith
    have := (hasDerivAt_pow 2 r).div ((hasDerivAt_id' (x := r)).add_const 1) h1
    convert this using 1
    · funext x; simp only [law, Pi.div_apply]; ring
    · field_simp; ring
  · refine ContinuousLinearMap.opNorm_le_bound _ (by positivity) fun v => ?_
    simp only [H, add_apply, smul_apply,
      ContinuousLinearMap.id_apply, ContinuousLinearMap.smulRight_apply, innerSL_apply_apply]
    have hl : law r ≤ r := by rw [hlaw, div_le_iff₀ (by linarith)]; nlinarith
    have hl0 : 0 ≤ law r := by rw [hlaw]; positivity
    have hin : |inner ℝ q v| ≤ r * ‖v‖ := abs_real_inner_le_norm q v
    have hk : 0 ≤ 2 / ((1 + r) ^ 2 * r) := by positivity
    calc ‖(2 * law r) • v + (2 / ((1 + r) ^ 2 * r)) • (inner ℝ q v • q)‖
        ≤ ‖(2 * law r) • v‖ + ‖(2 / ((1 + r) ^ 2 * r)) • (inner ℝ q v • q)‖ := norm_add_le _ _
      _ = 2 * law r * ‖v‖ + 2 / ((1 + r) ^ 2 * r) * (|inner ℝ q v| * r) := by
          rw [norm_smul, norm_smul, norm_smul, Real.norm_eq_abs, Real.norm_eq_abs,
            Real.norm_eq_abs, abs_of_nonneg (by positivity), abs_of_nonneg hk]
      _ ≤ 2 * r * ‖v‖ + 2 / ((1 + r) ^ 2 * r) * (r * ‖v‖ * r) := by gcongr
      _ = 2 * r * ‖v‖ + 2 * r / (1 + r) ^ 2 * ‖v‖ := by field_simp
      _ ≤ 2 * r * ‖v‖ + 2 * r * ‖v‖ := by
          gcongr
          rw [div_le_iff₀ (by positivity)]
          nlinarith [mul_nonneg hr.le (by positivity : (0 : ℝ) ≤ 2 * r + r ^ 2)]
      _ = 4 * r * ‖v‖ := by ring

/-- `W` is smooth away from `q = 0`. -/
theorem contDiffAt_W {q : E} (hq : q ≠ 0) {n : WithTop ℕ∞} : ContDiffAt ℝ n W q := by
  have hy : 0 < ‖q‖ ^ 2 := by positivity
  have hF : ContDiffAt ℝ n F (‖q‖ ^ 2) := by
    unfold F
    have hs : ContDiffAt ℝ n (fun y : ℝ => √y) (‖q‖ ^ 2) := contDiffAt_sqrt hy.ne'
    have h1 : 1 + √(‖q‖ ^ 2) ≠ 0 := by positivity
    exact (contDiffAt_id.sub (contDiffAt_const.mul hs)).add
      (contDiffAt_const.mul ((contDiffAt_const.add hs).log h1))
  exact hF.comp q (contDiff_norm_sq ℝ).contDiffAt

/-- The gradient is smooth away from `0`. -/
lemma contDiffAt_G {q : E} (hq : q ≠ 0) {n : WithTop ℕ∞} : ContDiffAt ℝ n (G : E → E) q := by
  have hn : ContDiffAt ℝ n (fun x : E => ‖x‖) q := contDiffAt_norm ℝ hq
  have hlaw : ContDiffAt ℝ n law ‖q‖ := by
    have h1 : ‖q‖ + 1 ≠ 0 := by positivity
    exact contDiffAt_id.div (contDiffAt_id.add contDiffAt_const) h1
  exact (contDiffAt_const.mul (hlaw.comp q hn)).smul contDiffAt_id

lemma fderiv_G_norm_le (q : E) : ‖fderiv ℝ (G : E → E) q‖ ≤ 4 * ‖q‖ := by
  rcases eq_or_ne q 0 with rfl | hq
  · rw [hasFDerivAt_G_zero.fderiv]; simp
  · rw [(hasFDerivAt_G hq).fderiv]; exact (hessian hq).2.2.2.2.2.2.2.2

/-- **Theorem 2: `W ∈ C²`.** -/
theorem W_contDiff_two : ContDiff ℝ 2 (W : E → ℝ) := by
  have hdiffG : ∀ x : E, HasFDerivAt G (fderiv ℝ G x) x := by
    intro x
    rcases eq_or_ne x 0 with rfl | hx
    · exact hasFDerivAt_G_zero.differentiableAt.hasFDerivAt
    · exact (hasFDerivAt_G hx).differentiableAt.hasFDerivAt
  have hcont : Continuous (fderiv ℝ (G : E → E)) := by
    rw [continuous_iff_continuousAt]
    intro x
    rcases eq_or_ne x 0 with rfl | hx
    · rw [ContinuousAt, hasFDerivAt_G_zero.fderiv]
      apply squeeze_zero_norm' (a := fun q : E => 4 * ‖q‖)
      · exact Eventually.of_forall fun q => fderiv_G_norm_le q
      · have : Tendsto (fun q : E => 4 * ‖q‖) (𝓝 0) (𝓝 (4 * ‖(0 : E)‖)) :=
          (continuous_const.mul continuous_norm).tendsto 0
        simpa using this
      |> fun h => by simpa [tendsto_iff_norm_sub_tendsto_zero] using h
    · exact ((contDiffAt_G hx (n := 2)).fderiv_right (m := 1) (by norm_num)).continuousAt
  have hG1 : ContDiff ℝ 1 (G : E → E) :=
    contDiff_one_iff_hasFDerivAt.mpr ⟨fderiv ℝ G, hcont, hdiffG⟩
  have h2 : ContDiff ℝ 1 (fun q : E => innerSL ℝ (G q)) :=
    (innerSL ℝ : E →L[ℝ] E →L[ℝ] ℝ).contDiff.comp hG1
  exact contDiff_succ_iff_hasFDerivAt.mpr ⟨fun q => innerSL ℝ (G q), h2, hasFDerivAt_W⟩

/-- **Strict monotonicity of the flux.** `(A(p) − A(p'))·(p − p') > 0` for `p ≠ p'`: the pointwise
inequality behind uniqueness (Corollary 2). -/
theorem A_strictMono (p p' : E) (hne : p ≠ p') : 0 < inner ℝ (A p - A p') (p - p') := by
  set r := ‖p‖; set s := ‖p'‖
  have hr := norm_nonneg p; have hs := norm_nonneg p'
  set a := law r; set b := law s
  have ha : a = r / (r + 1) := rfl
  have hb : b = s / (s + 1) := rfl
  have ha0 : 0 ≤ a := by rw [ha]; positivity
  have hb0 : 0 ≤ b := by rw [hb]; positivity
  have hexp : inner ℝ (A p - A p') (p - p') = a * r ^ 2 + b * s ^ 2 - (a + b) * inner ℝ p p' := by
    simp only [A, inner_sub_left, inner_sub_right, inner_smul_left, real_inner_self_eq_norm_sq,
      real_inner_comm p p', RCLike.conj_to_real]
    ring
  have hin : inner ℝ p p' ≤ r * s := real_inner_le_norm p p'
  rw [hexp]
  rcases eq_or_ne r s with hrs | hrs
  · -- equal lengths: the expression is `a |p − p'|²`
    have hab : a = b := by rw [ha, hb, hrs]
    have hrpos : 0 < r := by
      rcases hr.lt_or_eq with h | h
      · exact h
      · exfalso; apply hne
        have h0 : p = 0 := norm_eq_zero.mp h.symm
        have hs0 : s = 0 := by rw [← hrs]; exact h.symm
        have h0' : p' = 0 := norm_eq_zero.mp hs0
        rw [h0, h0']
    have hapos : 0 < a := by rw [ha]; positivity
    have hd : 0 < ‖p - p'‖ ^ 2 := by have := sub_ne_zero.mpr hne; positivity
    have : ‖p - p'‖ ^ 2 = r ^ 2 + s ^ 2 - 2 * inner ℝ p p' := by
      rw [@norm_sub_sq_real]; ring
    rw [← hab]
    nlinarith
  · -- unequal lengths: at least `(r − s)²(r + s + rs)/((1 + r)(1 + s))`
    have hkey : a * r ^ 2 + b * s ^ 2 - (a + b) * (r * s) =
        (r - s) ^ 2 * (r + s + r * s) / ((1 + r) * (1 + s)) := by
      have h1r : 1 + r ≠ 0 := by positivity
      have h1s : 1 + s ≠ 0 := by positivity
      have h2r : r + 1 ≠ 0 := by positivity
      have h2s : s + 1 ≠ 0 := by positivity
      rw [ha, hb]; field_simp; ring
    have hpos : 0 < (r - s) ^ 2 * (r + s + r * s) / ((1 + r) * (1 + s)) := by
      have h1 : 0 < (r - s) ^ 2 := by have := sub_ne_zero.mpr hrs; positivity
      have h2 : 0 < r + s + r * s := by
        rcases hr.lt_or_eq with h | h
        · positivity
        · have : 0 < s := lt_of_le_of_ne hs (by rw [h]; exact hrs)
          positivity
      positivity
    nlinarith

lemma deriv_g {x : ℝ} (hx : 0 < x) : deriv g x = 2 * x ^ 2 / (1 + x) :=
  (hasDerivAt_g (by linarith)).deriv

lemma g_strictMonoOn : StrictMonoOn g (Ici 0) := by
  apply strictMonoOn_of_deriv_pos (convex_Ici 0) continuousOn_g
  intro x hx
  rw [interior_Ici, mem_Ioi] at hx
  rw [deriv_g hx]; positivity

lemma g_strictConvexOn : StrictConvexOn ℝ (Ici 0) g := by
  apply StrictMonoOn.strictConvexOn_of_deriv (convex_Ici 0) continuousOn_g
  rw [interior_Ici]
  intro x hx y hy hxy
  simp only [mem_Ioi] at hx hy
  rw [deriv_g hx, deriv_g hy, div_lt_div_iff₀ (by linarith) (by linarith)]
  nlinarith [mul_pos hx hy, mul_pos (mul_pos hx hy) (sub_pos.mpr hxy)]

/-- **Strict convexity of the energy density.** -/
theorem W_strictConvex : StrictConvexOn ℝ univ (W : E → ℝ) := by
  refine ⟨convex_univ, fun p _ p' _ hne a b ha hb hab => ?_⟩
  simp only [W_eq, smul_eq_mul]
  set r := ‖p‖; set s := ‖p'‖
  have hr := norm_nonneg p; have hs := norm_nonneg p'
  have ht : ‖a • p + b • p'‖ ≤ a * r + b * s := by
    calc ‖a • p + b • p'‖ ≤ ‖a • p‖ + ‖b • p'‖ := norm_add_le _ _
      _ = a * r + b * s := by
        rw [norm_smul, norm_smul, Real.norm_eq_abs, Real.norm_eq_abs, abs_of_pos ha,
          abs_of_pos hb]
  have hmono : g ‖a • p + b • p'‖ ≤ g (a * r + b * s) :=
    g_strictMonoOn.monotoneOn (norm_nonneg _) (by simp only [mem_Ici]; positivity) ht
  rcases eq_or_ne r s with hrs | hrs
  · have hlt : ‖a • p + b • p'‖ < r :=
      norm_combo_lt_of_ne le_rfl (by rw [hrs]) hne ha hb hab
    have := g_strictMonoOn (norm_nonneg _) (show r ∈ Ici (0 : ℝ) from hr) hlt
    rw [← hrs]
    calc g ‖a • p + b • p'‖ < g r := this
      _ = a * g r + b * g r := by rw [← add_mul, hab, one_mul]
  · have := g_strictConvexOn.2 (show r ∈ Ici (0 : ℝ) from hr) (show s ∈ Ici (0 : ℝ) from hs) hrs
      ha hb hab
    simp only [smul_eq_mul] at this
    exact lt_of_le_of_lt hmono this

end Vector

#print axioms AqualEnergy.theorem1
#print axioms AqualEnergy.g_bounds
#print axioms AqualEnergy.series_small
#print axioms AqualEnergy.series_large
#print axioms AqualEnergy.hasFDerivAt_W
#print axioms AqualEnergy.hasFDerivAt_G
#print axioms AqualEnergy.hasFDerivAt_G_zero
#print axioms AqualEnergy.hessian
#print axioms AqualEnergy.contDiffAt_W
#print axioms AqualEnergy.W_contDiff_two
#print axioms AqualEnergy.A_strictMono
#print axioms AqualEnergy.W_strictConvex

end AqualEnergy
