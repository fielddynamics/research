import NetFieldRule
import ConstitutiveLaw
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.Calculus.MeanValue

/-!
# The SST Khronon: Preferred-Frame Effects of the Time Leg

The algebra of the khronon sector of Gravity Field Dynamics. The SST, varied as the framework
varies it, has the field equations of Blanchet and Marsat's preferred-foliation theory with
`f = a₀²[F(y) − y]`, so that `f'(a) = 2a(μ − 1)` (the time-leg proof). Its preferred frame is a
foliation, the khronon. In Flanagan's slow-motion analysis of that theory the khronon's kinetic
matrix is built from `f'/2a` and `f''`, its density is the TetB share's phantom density, and its
stationary solutions are stable when `f' ≤ a f'' ≤ 0`.

* `bb_point`: Bonetti and Barausse's formulas at GFD's point `β = λ = 0`: `α₁ = −4α` is finite,
  `α₂` has a pole in `λ` with non-zero residue, and the khronon's sound speed vanishes; their
  expansion does not apply there.
* `stability_dictionary`: for any law with `f'(a) = 2a(μ(a/a₀) − 1)`, `−f''/2` is the derivative
  of the TetB share `x(1 − μ)`, and `a f'' − f'` is `2a·xμ'`. The stability conditions say that
  neither `μ` nor the TetB share decreases with the field.
* `share_eq_law`, `share_deriv`, `law_deriv`: for `μ = x/(x+1)` the TetB share in units of `a₀`
  is `μ` itself, so both conditions are the one condition `μ' = 1/(x+1)² > 0`.
* `gfd_stable`: GFD's `f'`, `f''` and `a f'' − f'` in closed form, with their signs, at every
  acceleration.
* `stability_forces_tail`, `no_constant_limit`: if `f'` does not increase and is negative somewhere,
  `f → −∞`, so a law stable at every acceleration cannot tend to a constant; `share_limit`: for GFD
  the TetB share tends to `a₀`.
* `standard_law_turns_over`: for `μ = x/√(1+x²)` the TetB share is smaller at `x = 10` than at
  `x = 1`, so the stability condition fails above `a₀`.
* `inertia_vanishes`: the khronon's inertia `(1 − μ)` and `(1 − μ)²` vanishes as the TetB share
  vanishes.
* `strong_field_not_pure`, `slope_and_dimple`: close up, the galaxy's field is a flat slope that
  drops out in free fall, and the Sun is a dimple with no drain (no TetB share); a stronger field
  never gives that, since the TetB share stays between 0 and `a₀`; the two views meet at the
  Jacobi radius, where the Sun's pull equals the tide.
* `density_exponent`, `oscillation_frequency`: around a point mass the khronon density is positive,
  and a khronon mode across the field oscillates at `ω² = [2/(2 − μ)]Ω² = −dg/dr`, between `Ω²`
  and `2Ω²`.

Numbers (solar-system estimates, the family scan) are checked by the script
`verify_sst_khronon_preferred_frame.py`.
-/

open Filter Topology ConstitutiveLaw

namespace KhrononPreferredFrame

/-- Bonetti–Barausse, Eqs. 14–16. -/
noncomputable def alpha1 (α β : ℝ) : ℝ := 4 * (α - 2 * β) / (β - 1)
noncomputable def alpha2 (α β l : ℝ) : ℝ :=
  (α - 2 * β) * (-β * (3 + β + 3 * l) - l + α * (1 + β + 2 * l)) /
    ((α - 2) * (β - 1) * (β + l))
noncomputable def cs2 (α β l : ℝ) : ℝ := (α - 2) * (β + l) / (α * (β - 1) * (2 + β + 3 * l))

/-- At `β = λ = 0` (no expansion or shear terms): `α₁ = −4α`; `λ·α₂` has the non-zero limit
`−α²/(α − 2)` as `λ → 0`, so `α₂` has a pole; and `c_s² = 0`. -/
theorem bb_point (α l : ℝ) (hα : α ≠ 0) (hα2 : α ≠ 2) (hl : l ≠ 0) :
    alpha1 α 0 = -4 * α ∧
    l * alpha2 α 0 l = α * (l - α - 2 * α * l) / (α - 2) ∧
    α * (0 - α - 2 * α * 0) / (α - 2) ≠ 0 ∧
    cs2 α 0 0 = 0 := by
  have h2 : α - 2 ≠ 0 := sub_ne_zero.mpr hα2
  refine ⟨?_, ?_, ?_, ?_⟩
  · unfold alpha1; ring
  · unfold alpha2
    simp only [mul_zero, zero_add, sub_zero, zero_mul, neg_zero, add_zero]
    field_simp; ring
  · have : α * (0 - α - 2 * α * 0) = -(α ^ 2) := by ring
    rw [this]; exact div_ne_zero (neg_ne_zero.mpr (pow_ne_zero 2 hα)) h2
  · unfold cs2; simp

/-- For any law `m`: the derivative of `f'(a) = 2a(m(a/a₀) − 1)` at `a = a₀x`, minus half of it is
the derivative of the TetB share `t(1 − m t)`, and `a f'' − f' = 2a·x m'`. -/
theorem stability_dictionary (m : ℝ → ℝ) (m' x a0 : ℝ) (ha : 0 < a0) (hm : HasDerivAt m m' x) :
    HasDerivAt (fun a => 2 * a * (m (a / a0) - 1)) (2 * (m x - 1) + 2 * x * m') (a0 * x) ∧
    HasDerivAt (fun t => t * (1 - m t)) ((1 - m x) - x * m') x ∧
    -(2 * (m x - 1) + 2 * x * m') / 2 = (1 - m x) - x * m' ∧
    a0 * x * (2 * (m x - 1) + 2 * x * m') - 2 * (a0 * x) * (m x - 1) = 2 * (a0 * x) * (x * m') := by
  have ha' : a0 ≠ 0 := ha.ne'
  have hx : a0 * x / a0 = x := by field_simp
  refine ⟨?_, ?_, by ring, by ring⟩
  · have hc : HasDerivAt (fun a => m (a / a0)) (m' * (1 / a0)) (a0 * x) := by
      have hm2 : HasDerivAt m m' (a0 * x / a0) := by rw [hx]; exact hm
      have hd : HasDerivAt (fun a : ℝ => a / a0) (1 / a0) (a0 * x) := (hasDerivAt_id _).div_const a0
      exact hm2.comp (a0 * x) hd
    have h := ((hasDerivAt_id' (a0 * x)).const_mul 2).mul (hc.sub_const 1)
    rw [hx] at h
    convert h using 1
    field_simp
  · have h := (hasDerivAt_id' x).mul ((hasDerivAt_const x (1 : ℝ)).sub hm)
    convert h using 1; simp only [Pi.sub_apply]; ring

theorem share_eq_law (x : ℝ) (hx : 0 ≤ x) : x * (1 - law x) = law x := by
  unfold law; have : x + 1 ≠ 0 := by linarith
  field_simp; ring

theorem law_deriv (x : ℝ) (hx : 0 ≤ x) : HasDerivAt law (1 / (x + 1) ^ 2) x := by
  have h1 : x + 1 ≠ 0 := by linarith
  have h := (hasDerivAt_id' x).div ((hasDerivAt_id' x).add_const 1) h1
  have e : law = fun t => t / (t + 1) := rfl
  rw [e]; convert h using 1; field_simp; ring

theorem share_deriv (x : ℝ) (hx : 0 ≤ x) :
    HasDerivAt (fun t => t * (1 - law t)) (1 / (x + 1) ^ 2) x := by
  have h1 : x + 1 ≠ 0 := by linarith
  have := ((stability_dictionary law (1 / (x + 1) ^ 2) x 1 one_pos (law_deriv x hx)).2.1)
  convert this using 1; unfold law; field_simp; ring

/-- GFD's `f` at `a = a₀x`: `f' = −2a₀μ`, `f''`'s value `−2/(x+1)²`, and `a f'' − f'` is
`2a₀x²/(x+1)²`; strictly negative, negative and positive for every `x > 0`. -/
theorem gfd_stable (x a0 : ℝ) (hx : 0 < x) (ha : 0 < a0) :
    2 * (a0 * x) * (law x - 1) = -2 * a0 * law x ∧
    2 * (law x - 1) + 2 * x * (1 / (x + 1) ^ 2) = -2 / (x + 1) ^ 2 ∧
    2 * (a0 * x) * (x * (1 / (x + 1) ^ 2)) = 2 * a0 * x ^ 2 / (x + 1) ^ 2 ∧
    -2 * a0 * law x < 0 ∧ -2 / (x + 1) ^ 2 < 0 ∧ 0 < 2 * a0 * x ^ 2 / (x + 1) ^ 2 := by
  have h1 : x + 1 ≠ 0 := by linarith
  have hl : 0 < law x := by unfold law; positivity
  refine ⟨?_, ?_, ?_, by nlinarith, ?_, by positivity⟩
  · unfold law; field_simp; ring
  · unfold law; field_simp; ring
  · field_simp
  · have : 0 < (x + 1) ^ 2 := by positivity
    exact div_neg_of_neg_of_pos (by norm_num) this

/-- Stability forces the tail: if `f'` is non-increasing on `[a₁, ∞)` and `f'(a₁) < 0`, then
`f → −∞`. -/
theorem stability_forces_tail (f f' : ℝ → ℝ) (a1 : ℝ)
    (hd : ∀ a, a1 ≤ a → HasDerivAt f (f' a) a)
    (hanti : AntitoneOn f' (Set.Ici a1)) (hneg : f' a1 < 0) :
    Tendsto f atTop atBot := by
  set k := -f' a1 with hk
  have hkpos : 0 < k := by linarith
  -- g(a) = f(a) + k a is non-increasing on [a₁, ∞)
  have hg : AntitoneOn (fun a => f a + k * a) (Set.Ici a1) := by
    apply antitoneOn_of_deriv_nonpos (convex_Ici a1)
    · intro a ha
      exact ((hd a ha).continuousAt.add (continuousAt_const.mul continuousAt_id)).continuousWithinAt
    · intro a ha
      rw [interior_Ici] at ha
      exact ((hd a (le_of_lt ha)).add ((hasDerivAt_id a).const_mul k)).differentiableAt.differentiableWithinAt
    · intro a ha
      rw [interior_Ici] at ha
      have h : HasDerivAt (fun y => f y + k * y) (f' a + k * 1) a :=
        (hd a (le_of_lt ha)).add ((hasDerivAt_id' a).const_mul k)
      rw [h.deriv]
      have : f' a ≤ f' a1 := hanti (Set.mem_Ici.mpr le_rfl) (Set.mem_Ici.mpr (le_of_lt ha)) (le_of_lt ha)
      simp only [mul_one]; linarith
  have hbound : ∀ a, a1 ≤ a → f a ≤ f a1 + k * a1 - k * a := by
    intro a ha
    have := hg ((Set.mem_Ici.mpr le_rfl)) ha ha
    simp only at this; linarith
  have hlin : Tendsto (fun a => f a1 + k * a1 - k * a) atTop atBot := by
    have : Tendsto (fun a => k * a) atTop atTop := tendsto_id.const_mul_atTop hkpos
    have hn : Tendsto (fun a => -(k * a)) atTop atBot := tendsto_neg_atTop_atBot.comp this
    exact (tendsto_atBot_add_const_left atTop (f a1 + k * a1) hn).congr (fun a => by ring)
  exact tendsto_atBot_mono' atTop (eventually_ge_atTop a1 |>.mono hbound) hlin

theorem no_constant_limit (f f' : ℝ → ℝ) (a1 : ℝ)
    (hd : ∀ a, a1 ≤ a → HasDerivAt f (f' a) a)
    (hanti : AntitoneOn f' (Set.Ici a1)) (hneg : f' a1 < 0) :
    ¬ ∃ L : ℝ, Tendsto f atTop (𝓝 L) := by
  rintro ⟨L, hL⟩
  have h := stability_forces_tail f f' a1 hd hanti hneg
  exact not_tendsto_nhds_of_tendsto_atBot h L hL

/-- For GFD the TetB share, in units of `a₀`, rises to 1: the tail tends to `a₀`. -/
theorem share_limit : Tendsto (fun x => x * (1 - law x)) atTop (𝓝 1) := by
  have h : ∀ x : ℝ, 0 ≤ x → x * (1 - law x) = 1 - 1 / (x + 1) := by
    intro x hx; rw [share_eq_law x hx]; unfold law
    have : x + 1 ≠ 0 := by linarith
    field_simp; ring
  have h2 : Tendsto (fun x : ℝ => 1 - 1 / (x + 1)) atTop (𝓝 1) := by
    have : Tendsto (fun x : ℝ => 1 / (x + 1)) atTop (𝓝 0) := by
      exact tendsto_const_nhds.div_atTop (tendsto_atTop_add_const_right _ 1 tendsto_id)
    simpa using (tendsto_const_nhds (x := (1 : ℝ))).sub this
  exact h2.congr' (eventually_ge_atTop 0 |>.mono fun x hx => (h x hx).symm)

/-- The 'standard' law `x/√(1+x²)`: its TetB share at `x = 10` is below its value at `x = 1`. -/
theorem standard_law_turns_over :
    (10 : ℝ) * (1 - 10 / Real.sqrt (1 + 10 ^ 2)) < 1 * (1 - 1 / Real.sqrt (1 + 1 ^ 2)) := by
  have s2 : Real.sqrt (1 + 1 ^ 2) = Real.sqrt 2 := by norm_num
  have s101 : Real.sqrt (1 + 10 ^ 2) = Real.sqrt 101 := by norm_num
  rw [s2, s101]
  have h2pos : 0 < Real.sqrt 2 := by positivity
  have h101pos : 0 < Real.sqrt 101 := by positivity
  have h2 : (4 : ℝ) / 3 < Real.sqrt 2 := by
    rw [show (4 : ℝ) / 3 = Real.sqrt ((4 / 3) ^ 2) by rw [Real.sqrt_sq]; norm_num]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  have h101 : Real.sqrt 101 < 400 / 39 := by
    rw [show (400 : ℝ) / 39 = Real.sqrt ((400 / 39) ^ 2) by rw [Real.sqrt_sq]; norm_num]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  have e1 : 1 / Real.sqrt 2 < 3 / 4 := by
    rw [div_lt_div_iff₀ h2pos (by norm_num)]; linarith
  have e2 : 39 / 40 < 10 / Real.sqrt 101 := by
    rw [div_lt_div_iff₀ (by norm_num) h101pos]; linarith
  linarith

/-- The khronon's inertia across and along the field, `(1 − μ)` and `(1 − μ)²`, vanishes where the
TetB share vanishes. -/
theorem inertia_vanishes :
    Tendsto (fun x => 1 - law x) atTop (𝓝 0) ∧ Tendsto (fun x => (1 - law x) ^ 2) atTop (𝓝 0) := by
  have h : Tendsto (fun x => 1 - law x) atTop (𝓝 0) := by
    have e : ∀ x : ℝ, 0 ≤ x → 1 - law x = 1 / (x + 1) := by
      intro x hx; unfold law; have : x + 1 ≠ 0 := by linarith
      field_simp; ring
    have : Tendsto (fun x : ℝ => 1 / (x + 1)) atTop (𝓝 0) := by
      exact tendsto_const_nhds.div_atTop (tendsto_atTop_add_const_right _ 1 tendsto_id)
    exact this.congr' (eventually_ge_atTop 0 |>.mono fun x hx => (e x hx).symm)
  exact ⟨h, by simpa using h.pow 2⟩

/-- Around a point mass, with `d ln x/d ln r = −2/(2 − μ)` and `x μ'/μ = 1 − μ`:
`d ln(r²μ)/d ln r = 2/(2 − μ) = 2 − s`, with `s` the net-field rule's flux exponent, and it is
positive, so the khronon density is positive. -/
theorem density_exponent (m : ℝ) (hm : m < 2) :
    2 + (1 - m) * (-2 / (2 - m)) = 2 / (2 - m) ∧
    2 / (2 - m) = 2 - 2 * (1 - m) / (2 - m) ∧ 0 < 2 / (2 - m) := by
  have h : 2 - m ≠ 0 := by linarith
  refine ⟨by field_simp; ring, ?_, div_pos (by norm_num) (by linarith)⟩
  have := (NetFieldRule.flux_exponent m hm).1
  linarith

/-- The khronon's frequency across the field around a point mass: `ρ_T0/h_⊥` with
`ρ_T0 = (a₀μ/4πGr)·2/(2 − μ)` and `h_⊥ = (1 − μ)/4πG` is `[2/(2 − μ)]·Ω²`, `Ω² = g/r = a₀x/r`;
it equals `−dg/dr`, and it lies strictly between `Ω²` and `2Ω²`. -/
theorem oscillation_frequency (x a0 G r : ℝ) (hx : 0 < x) (ha : 0 < a0) (hG : 0 < G) (hr : 0 < r) :
    (a0 * law x / (4 * Real.pi * G * r) * (2 / (2 - law x))) / ((1 - law x) / (4 * Real.pi * G))
      = 2 / (2 - law x) * (a0 * x / r) ∧
    -(a0 * (x / r) * (-2 / (2 - law x))) = 2 / (2 - law x) * (a0 * x / r) ∧
    a0 * x / r < 2 / (2 - law x) * (a0 * x / r) ∧ 2 / (2 - law x) * (a0 * x / r) < 2 * (a0 * x / r) := by
  have h1 : x + 1 ≠ 0 := by linarith
  have hl0 : 0 < law x := by unfold law; positivity
  have hl1 : law x < 1 := by unfold law; rw [div_lt_one (by linarith)]; linarith
  have h2 : 2 - law x ≠ 0 := by linarith
  have h3 : 1 - law x ≠ 0 := by linarith
  have hpi : 0 < Real.pi := Real.pi_pos
  have hO : 0 < a0 * x / r := by positivity
  have hs : law x / (1 - law x) = x := by
    have := share_eq_law x hx.le
    field_simp; linarith
  refine ⟨?_, by ring, ?_, ?_⟩
  · have : (a0 * law x / (4 * Real.pi * G * r) * (2 / (2 - law x))) / ((1 - law x) / (4 * Real.pi * G))
        = 2 / (2 - law x) * (a0 / r) * (law x / (1 - law x)) := by
      field_simp
    rw [this, hs]; ring
  · have : 1 < 2 / (2 - law x) := by rw [lt_div_iff₀ (by linarith)]; linarith
    nlinarith
  · have : 2 / (2 - law x) < 2 := by rw [div_lt_iff₀ (by linarith)]; nlinarith
    nlinarith

-- ============================================================================================
-- The flat slope and the mountain
-- ============================================================================================

/-- A stronger field never makes the field pure TetA: for every finite `x > 0` the TetB share, in
units of `a₀`, lies strictly between 0 and 1 (and tends to 1, `share_limit`). "No drain" is not
"strong field". -/
theorem strong_field_not_pure (x : ℝ) (hx : 0 < x) :
    0 < x * (1 - law x) ∧ x * (1 - law x) < 1 := by
  rw [share_eq_law x hx.le]; unfold law
  have h1 : 0 < x + 1 := by linarith
  exact ⟨div_pos hx h1, (div_lt_one h1).mpr (by linarith)⟩

/-- Close up: the Sun's own field is a drainless dimple, taken linearly (`μ = 1`), so its TetB
share is exactly zero; and the galaxy's field there is a flat slope `g_e`, which drops out of every
relative acceleration (the net-field rule's `free_fall`). At the edge, `r_J³ = GM/(2Ω²)`, the Sun's
pull equals the tide of a flat rotation curve: `GM/r_J² = 2Ω² r_J` (the net-field rule's `jacobi`). -/
theorem slope_and_dimple {V : Type*} [AddCommGroup V] (g : ℝ) (ai aj ge : V)
    (v R GM rJ : ℝ) (hR : 0 < R) (hv : 0 < v) (hGM : 0 < GM) (hrJ : 0 < rJ)
    (hJ : rJ ^ 3 = GM / (2 * (v / R) ^ 2)) :
    (1 - 1) * g = 0 ∧ (aj + ge) - (ai + ge) = aj - ai ∧ GM / rJ ^ 2 = 2 * (v / R) ^ 2 * rJ := by
  refine ⟨by ring, NetFieldRule.free_fall ai aj ge, ?_⟩
  have h := (NetFieldRule.jacobi v R GM (rJ ^ 3) hR hv hGM hJ).2.2
  have hr2 : rJ ^ 2 ≠ 0 := by positivity
  have hr3 : rJ ^ 3 ≠ 0 := by positivity
  rw [← h]; field_simp

end KhrononPreferredFrame

#print axioms KhrononPreferredFrame.bb_point
#print axioms KhrononPreferredFrame.stability_dictionary
#print axioms KhrononPreferredFrame.share_eq_law
#print axioms KhrononPreferredFrame.law_deriv
#print axioms KhrononPreferredFrame.share_deriv
#print axioms KhrononPreferredFrame.gfd_stable
#print axioms KhrononPreferredFrame.stability_forces_tail
#print axioms KhrononPreferredFrame.no_constant_limit
#print axioms KhrononPreferredFrame.share_limit
#print axioms KhrononPreferredFrame.standard_law_turns_over
#print axioms KhrononPreferredFrame.inertia_vanishes
#print axioms KhrononPreferredFrame.density_exponent
#print axioms KhrononPreferredFrame.oscillation_frequency
#print axioms KhrononPreferredFrame.strong_field_not_pure
#print axioms KhrononPreferredFrame.slope_and_dimple
