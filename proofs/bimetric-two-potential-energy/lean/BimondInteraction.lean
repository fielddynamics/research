import AqualEnergy
import TetradScheme
import Mathlib.Analysis.SpecialFunctions.Arsinh
import Mathlib.Analysis.Calculus.Deriv.Inverse

/-!
# Lean 4 / Mathlib formalisation of
#   S. Nelson, "The Two-Potential Energy of Bimetric MOND (BIMOND)"

The nonrelativistic limit of Milgrom's bimetric MOND (BIMOND), with its two potentials `φ`
(matter) and `φ̂` (twin matter). Builds on `AqualEnergy` (the AQUAL kinetic function `g`, its
convexity), `ConstitutiveLaw` (`μ = law`) and `TetradScheme` (the two roots of the tetrad equation).

## How to referee this file
A Lean proof can only be wrong in its *statements*. Check these definitions against the paper:
* Theorem 1 is the algebra of the Euler–Lagrange equations (2): the divergence is any linear map
  `D`, `u = ∇φ`, `û = ∇φ̂`, `u − û = ∇φ*`, and `w = 𝓜'∇φ*` is a given field.
* `yOf x = x μ(x)`; `xOf y = (y + √(y² + 4y))/2`, its inverse; `nu y = ½ + √(¼ + 1/y)`, Eq. (6).
* `bOf x = 1/(1 + x)`; `Mx x = 2x − 1 + 2b − b² + 2 ln b`, Eq. (7), as a function of the total
  field `x`; `My y = Mx (xOf y)` in `y = |∇φ*|/a₀`; `Mz z = My √z` in BIMOND's argument `z = y²`.
* `Q y = y² + My y`, the kinetic function of Eq. (4).
* Units `a₀ = 1`.

## What is cited, not proved
Gauss's law in spherical symmetry (Proposition 1's first step) and the uniqueness of harmonic
functions with zero boundary values (Corollary 2's last step); the radial-Hessian formula for
`W(q) = Q(|q|)` (proved in `AqualEnergy` for its own `W`). The tetrad form of the action enters as
the pointwise density `det(e) R[g(e)]` for an arbitrary curvature operator `R`.
-/

open Real Filter Topology Set

namespace BimondInteraction

open ConstitutiveLaw (law)
open AqualEnergy (g)

/-! ## Theorem 1: the coupling ratio -/

section Coupling

variable {V S : Type*} [AddCommGroup V] [Module ℝ V] [AddCommGroup S] [Module ℝ S]

/-- **Theorem 1, the combination.** `α`·(first equation) − `β`·(second) eliminates `φ̂`:
`D[(αβ − (α+β)𝓜')∇φ*] = 4πG(αρ + βρ̂)`, with `c = 4πG`. -/
theorem combination (D : V →ₗ[ℝ] S) (α β c : ℝ) (u û w : V) (ρ ρh : S)
    (h1 : D (β • u - w) = c • ρ) (h2 : D (α • û + w) = -(c • ρh)) :
    D ((α * β) • (u - û) - (α + β) • w) = c • (α • ρ + β • ρh) := by
  have : (α * β) • (u - û) - (α + β) • w = α • (β • u - w) - β • (α • û + w) := by
    simp only [smul_sub, smul_add, smul_smul, add_smul]; abel_nf; simp only [mul_comm β α]; abel
  rw [this, map_sub, map_smul, map_smul, h1, h2]
  simp only [smul_neg, sub_neg_eq_add, smul_smul, smul_add, mul_comm α c, mul_comm β c]

/-- **Theorem 1, uniqueness of the combination.** In `λ`·(first) + `κ`·(second), `∇φ̂` enters with
coefficient `λβ + κα` (as `∇φ = ∇φ* + ∇φ̂`); it vanishes iff `(λ, κ)` is a multiple of `(α, −β)`. -/
theorem unique_combination (α β : ℝ) (hα : α ≠ 0) (lam kap : ℝ) :
    lam * β + kap * α = 0 ↔ ∃ t, lam = t * α ∧ kap = -(t * β) := by
  constructor
  · intro h; refine ⟨lam / α, by field_simp, ?_⟩
    field_simp; linarith
  · rintro ⟨t, rfl, rfl⟩; ring

/-- **Theorem 1, the condition.** For a nonconstant `𝓜'`, the coefficient `αβ − (α+β)𝓜'` is
constant iff `α + β = 0`. -/
theorem constant_iff (α β : ℝ) (m : ℝ → ℝ) (hm : ∃ z z', m z ≠ m z') :
    (∀ z z', α * β - (α + β) * m z = α * β - (α + β) * m z') ↔ α + β = 0 := by
  constructor
  · intro h
    obtain ⟨z, z', hzz⟩ := hm
    have := h z z'
    have : (α + β) * (m z - m z') = 0 := by linarith
    rcases mul_eq_zero.mp this with h | h
    · exact h
    · exact absurd (sub_eq_zero.mp h) hzz
  · intro h z z'; rw [h]; ring

/-- **Theorem 1, the system (Eq. (4)).** With `β = 1`, `α = −1`: `Δφ* = 4πG(ρ − ρ̂)` and
`Δφ = 4πGρ + ∇·(𝓜'∇φ*)`. -/
theorem qumond (D : V →ₗ[ℝ] S) (c : ℝ) (u û w : V) (ρ ρh : S)
    (h1 : D ((1 : ℝ) • u - w) = c • ρ) (h2 : D ((-1 : ℝ) • û + w) = -(c • ρh)) :
    D (u - û) = c • (ρ - ρh) ∧ D u = c • ρ + D w := by
  have h := combination D (-1) 1 c u û w ρ ρh h1 h2
  constructor
  · have e : ((-1 : ℝ) * 1) • (u - û) - (-1 + 1 : ℝ) • w = -(u - û) := by simp
    rw [e, map_neg, neg_one_smul, one_smul] at h
    rw [← neg_neg (D (u - û)), h, smul_add, smul_neg, smul_sub]; abel
  · rw [one_smul, map_sub] at h1
    rw [← h1]; abel

end Coupling

/-! ## Lemma 1: orientation -/

open Matrix

open TetradScheme (IsLorentz IsTetrad eta P Xminus kappa)

/-- **Lemma 1.** The tetrad Einstein–Hilbert density `det(e) R[g(e)]`, for any curvature operator `R`
of the metric field, changes by `det Λ` under a constant Lorentz `Λ`; under `P` it changes sign. -/
theorem lemma1 {X : Type*} (e : X → Matrix (Fin 4) (Fin 4) ℝ)
    (R : (X → Matrix (Fin 4) (Fin 4) ℝ) → X → ℝ) (Λ : Matrix (Fin 4) (Fin 4) ℝ)
    (hΛ : IsLorentz Λ) :
    (fun x => (Λ * e x).det * R (fun x => (Λ * e x)ᵀ * eta * (Λ * e x)) x) =
      fun x => Λ.det * ((e x).det * R (fun x => (e x)ᵀ * eta * e x) x) := by
  have hg : (fun x => (Λ * e x)ᵀ * eta * (Λ * e x)) = fun x => (e x)ᵀ * eta * e x := by
    funext x
    exact TetradScheme.lorentz_acts hΛ (rfl : IsTetrad ((e x)ᵀ * eta * e x) (e x))
  funext x; rw [hg, Matrix.det_mul]; ring

theorem lemma1_parity {X : Type*} (e : X → Matrix (Fin 4) (Fin 4) ℝ)
    (R : (X → Matrix (Fin 4) (Fin 4) ℝ) → X → ℝ) :
    (fun x => (P * e x).det * R (fun x => (P * e x)ᵀ * eta * (P * e x)) x) =
      fun x => -((e x).det * R (fun x => (e x)ᵀ * eta * e x) x) := by
  obtain ⟨hP, -, hdP, -⟩ := TetradScheme.P_T
  rw [lemma1 e R P hP]; funext x; rw [hdP]; ring

/-- **The second root enters with the opposite sign.** A frame on the root `det ê = −√(−det ĝ)`
gives `det(ê) R̂ = −√(−det ĝ) R̂`: in BIMOND's notation `α = −1` against `β = 1`. -/
theorem second_root_sign {gh eh : Matrix (Fin 4) (Fin 4) ℝ} (he : eh ∈ Xminus gh) (r : ℝ) :
    eh.det * r = -(√(-gh.det) * r) := by
  have hk : kappa gh = -gh.det := by
    rw [kappa, TetradScheme.det_etaR]; ring
  rw [he.2, hk]; ring

/-! ## The inverse partner -/

/-- `y = x μ(x)`. -/
noncomputable def yOf (x : ℝ) : ℝ := x * law x

/-- Its inverse, Eq. (6). -/
noncomputable def xOf (y : ℝ) : ℝ := (y + √(y ^ 2 + 4 * y)) / 2

/-- The inverse partner `ν(y) = ½ + √(¼ + 1/y)`, Eq. (6). -/
noncomputable def nu (y : ℝ) : ℝ := 1 / 2 + √(1 / 4 + 1 / y)

lemma yOf_eq {x : ℝ} (hx : 0 ≤ x) : yOf x = x ^ 2 / (1 + x) := by
  rw [yOf, law]; field_simp; ring

lemma yOf_nonneg {x : ℝ} (hx : 0 ≤ x) : 0 ≤ yOf x := by rw [yOf_eq hx]; positivity

lemma yOf_pos {x : ℝ} (hx : 0 < x) : 0 < yOf x := by rw [yOf_eq hx.le]; positivity

lemma xOf_nonneg {y : ℝ} (hy : 0 ≤ y) : 0 ≤ xOf y := by
  unfold xOf; positivity

lemma xOf_yOf {x : ℝ} (hx : 0 ≤ x) : xOf (yOf x) = x := by
  rw [yOf_eq hx, xOf]
  have h1 : 0 < 1 + x := by linarith
  have e : (x ^ 2 / (1 + x)) ^ 2 + 4 * (x ^ 2 / (1 + x)) = (x * (x + 2) / (1 + x)) ^ 2 := by
    field_simp; ring
  rw [e, sqrt_sq (by positivity)]
  field_simp; ring

lemma yOf_xOf {y : ℝ} (hy : 0 ≤ y) : yOf (xOf y) = y := by
  have hx := xOf_nonneg hy
  rw [yOf_eq hx]
  set s := √(y ^ 2 + 4 * y) with hs
  have hs0 : 0 ≤ s := sqrt_nonneg _
  have hs2 : s ^ 2 = y ^ 2 + 4 * y := sq_sqrt (by positivity)
  have h1 : 0 < 1 + xOf y := by linarith
  rw [div_eq_iff h1.ne', xOf, ← hs]
  nlinarith

/-- `x ↦ x μ(x)` is strictly increasing on `[0, ∞)`. -/
lemma yOf_strictMonoOn : StrictMonoOn yOf (Ici 0) := by
  intro a ha b hb hab
  simp only [mem_Ici] at ha hb
  rw [yOf_eq ha, yOf_eq hb, div_lt_div_iff₀ (by linarith) (by linarith)]
  nlinarith [mul_pos (by linarith : (0 : ℝ) < b - a) (by nlinarith : (0 : ℝ) < a + b + a * b)]

lemma nu_eq {y : ℝ} (hy : 0 < y) : nu y = xOf y / y := by
  rw [nu, xOf]
  have e : 1 / 4 + 1 / y = (y ^ 2 + 4 * y) / (2 * y) ^ 2 := by field_simp; ring
  rw [e, sqrt_div' _ (by positivity), sqrt_sq (by positivity)]
  field_simp

/-- **Proposition 1.** The AQUAL field in spherical symmetry is the unique `x ≥ 0` with
`μ(x) x = g_N`, namely `xOf g_N`; so BIMOND (whose total field is `(1 + 𝓜'(g_N²)) g_N`, by Gauss's
law, cited) realises `μ` iff `1 + 𝓜'(y²) = ν(y)` for all `y > 0`. -/
theorem prop1 :
    (∀ gN x : ℝ, 0 ≤ gN → 0 ≤ x → (law x * x = gN ↔ x = xOf gN)) ∧
      ∀ m : ℝ → ℝ, (∀ y : ℝ, 0 < y → (1 + m (y ^ 2)) * y = xOf y) ↔
        (∀ y : ℝ, 0 < y → 1 + m (y ^ 2) = nu y) := by
  refine ⟨fun gN x hg hx => ?_, fun m => ⟨fun h y hy => ?_, fun h y hy => ?_⟩⟩
  · rw [mul_comm, ← yOf]
    constructor
    · rintro rfl; exact (xOf_yOf hx).symm
    · rintro rfl; exact yOf_xOf hg
  · rw [nu_eq hy, ← h y hy]; field_simp
  · rw [h y hy, nu_eq hy]; field_simp

/-! ## Theorem 2: the interaction function -/

/-- `b = 1/(1 + x)`. -/
noncomputable def bOf (x : ℝ) : ℝ := 1 / (1 + x)

/-- `𝓜 = 2x − 1 + 2b − b² + 2 ln b`, Eq. (7), in the total field `x`. -/
noncomputable def Mx (x : ℝ) : ℝ := 2 * x - 1 + 2 * bOf x - bOf x ^ 2 + 2 * log (bOf x)

/-- `𝓜` in `y = |∇φ*|/a₀`. -/
noncomputable def My (y : ℝ) : ℝ := Mx (xOf y)

/-- `𝓜` in BIMOND's argument `z = y²`. -/
noncomputable def Mz (z : ℝ) : ℝ := My √z

/-- The kinetic function `Q(y) = y² + 𝓜` of Eq. (4). -/
noncomputable def Q (y : ℝ) : ℝ := y ^ 2 + My y

lemma log_bOf (x : ℝ) : log (bOf x) = -log (1 + x) := by
  rw [bOf, one_div, log_inv]

lemma Mx_zero : Mx 0 = 0 := by simp [Mx, bOf]; norm_num

lemma xOf_zero : xOf 0 = 0 := by simp [xOf]

lemma xOf_pos {y : ℝ} (hy : 0 < y) : 0 < xOf y := by
  unfold xOf; have := sqrt_nonneg (y ^ 2 + 4 * y); linarith

lemma continuous_xOf : Continuous xOf := by unfold xOf; fun_prop

lemma hasDerivAt_Mx {x : ℝ} (hx : -1 < x) :
    HasDerivAt Mx (2 * x ^ 2 * (x + 2) / (x + 1) ^ 3) x := by
  have h1 : 1 + x ≠ 0 := by linarith
  have hb : HasDerivAt bOf ((0 * (1 + x) - 1 * 1) / (1 + x) ^ 2) x :=
    (hasDerivAt_const x (1 : ℝ)).div ((hasDerivAt_id' (x := x)).const_add 1) h1
  have hbne : bOf x ≠ 0 := by rw [bOf]; positivity
  have := ((((hasDerivAt_id' (x := x)).const_mul 2).sub_const 1).add (hb.const_mul 2)).sub
    (hb.pow 2) |>.add ((hb.log hbne).const_mul 2)
  have h2 : x + 1 ≠ 0 := by linarith
  convert this using 1
  · funext y; simp [Mx]
  · simp only [bOf, show (2 : ℕ) - 1 = 1 from rfl, pow_one, Nat.cast_ofNat]
    field_simp; ring

lemma hasDerivAt_yOf {x : ℝ} (hx : -1 < x) : HasDerivAt yOf (x * (x + 2) / (x + 1) ^ 2) x := by
  have h1 : x + 1 ≠ 0 := by linarith
  have := (hasDerivAt_pow 2 x).div ((hasDerivAt_id' (x := x)).add_const 1) h1
  convert this using 1
  · funext y; simp only [yOf, law, Pi.div_apply]; ring
  · field_simp; ring

lemma hasDerivAt_xOf {y : ℝ} (hy : 0 < y) :
    HasDerivAt xOf ((xOf y * (xOf y + 2) / (xOf y + 1) ^ 2)⁻¹) y := by
  have hx := xOf_pos hy
  apply HasDerivAt.of_local_left_inverse continuous_xOf.continuousAt
    (hasDerivAt_yOf (by linarith)) (by positivity)
  filter_upwards [eventually_gt_nhds hy] with y' hy'
  exact yOf_xOf hy'.le

/-- `d𝓜/dy = 2(x − y) = 2μ(x)`, Eq. (9). -/
theorem hasDerivAt_My {y : ℝ} (hy : 0 < y) : HasDerivAt My (2 * (xOf y - y)) y := by
  have hx := xOf_pos hy
  have h := (hasDerivAt_Mx (by linarith : -1 < xOf y)).comp y (hasDerivAt_xOf hy)
  refine h.congr_deriv ?_
  have hyx : y = xOf y ^ 2 / (1 + xOf y) := by rw [← yOf_eq hx.le, yOf_xOf hy.le]
  set x := xOf y
  rw [hyx]; field_simp; ring

lemma two_x_sub_y {y : ℝ} (hy : 0 ≤ y) : 2 * (xOf y - y) = 2 * law (xOf y) := by
  have hx := xOf_nonneg hy
  have hy' := yOf_xOf hy
  set x := xOf y
  rw [← hy', yOf, law]; field_simp; ring

/-- `𝓜'(z) = ν(√z) − 1 = −½ + √(¼ + z^{−1/2})`. -/
theorem hasDerivAt_Mz {z : ℝ} (hz : 0 < z) : HasDerivAt Mz (nu √z - 1) z := by
  have hs : 0 < √z := sqrt_pos.mpr hz
  have h := (hasDerivAt_My hs).comp z (hasDerivAt_sqrt hz.ne')
  refine h.congr_deriv ?_
  rw [nu_eq hs]; field_simp

lemma continuousOn_Mx : ContinuousOn Mx (Ioi (-1)) := fun _ hx =>
  (hasDerivAt_Mx hx).continuousAt.continuousWithinAt

lemma continuous_on_comp {f : ℝ → ℝ} (hf : Continuous f) (hpos : ∀ z, 0 ≤ z → 0 ≤ f z) :
    ContinuousOn (fun z => Mx (f z)) (Ici 0) := fun z hz =>
  ((hasDerivAt_Mx (by linarith [hpos z hz] : -1 < f z)).continuousAt.comp
    hf.continuousAt).continuousWithinAt

lemma continuousOn_Mz : ContinuousOn Mz (Ici 0) :=
  continuous_on_comp (continuous_xOf.comp continuous_sqrt) fun z _ => xOf_nonneg (sqrt_nonneg z)

lemma continuousOn_My : ContinuousOn My (Ici 0) :=
  continuous_on_comp continuous_xOf fun _ hz => xOf_nonneg hz

lemma Mz_zero : Mz 0 = 0 := by simp [Mz, My, xOf_zero, Mx_zero]

/-- **Theorem 2.** `𝓜(0) = 0`, `𝓜` is continuous on `[0, ∞)`, `𝓜'(z) = −½ + √(¼ + 1/√z)`, so
`1 + 𝓜'(y²) = ν(y)`, and `𝓜` is the unique such function. Equivalent closed forms:
`x(2x² + 3x + 2)/(x + 1)² − 2 ln(1 + x)` and, in `y`, Eq. (8). -/
theorem theorem2 :
    Mz 0 = 0 ∧ ContinuousOn Mz (Ici 0) ∧
      (∀ z, 0 < z → HasDerivAt Mz (-1 / 2 + √(1 / 4 + 1 / √z)) z) ∧
      (∀ y, 0 < y → HasDerivAt Mz (nu y - 1) (y ^ 2)) ∧
      (∀ M₂ : ℝ → ℝ, M₂ 0 = 0 → ContinuousOn M₂ (Ici 0) →
        (∀ z, 0 < z → HasDerivAt M₂ (nu √z - 1) z) → ∀ z, 0 ≤ z → M₂ z = Mz z) ∧
      (∀ x, 0 ≤ x → Mx x = x * (2 * x ^ 2 + 3 * x + 2) / (x + 1) ^ 2 - 2 * log (1 + x)) ∧
      (∀ y, 0 ≤ y → My y = 1 / 2 * √y * (y + 2) * √(y + 4) - 1 / 2 * y ^ 2 -
        4 * arsinh (1 / 2 * √y)) := by
  refine ⟨Mz_zero, continuousOn_Mz, fun z hz => ?_, fun y hy => ?_, ?_, fun x hx => ?_,
    fun y hy => ?_⟩
  · exact (hasDerivAt_Mz hz).congr_deriv (by rw [nu]; ring)
  · exact (hasDerivAt_Mz (by positivity)).congr_deriv (by rw [sqrt_sq hy.le])
  · intro M₂ h0 hc hd z hz
    rcases hz.lt_or_eq with hz | hz
    · obtain ⟨c, hc', hcd⟩ := exists_hasDerivAt_eq_slope (fun z => M₂ z - Mz z) (fun _ => 0) hz
        ((hc.sub continuousOn_Mz).mono Icc_subset_Ici_self)
        fun x hx => ((hd x hx.1).sub (hasDerivAt_Mz hx.1)).congr_deriv (by ring)
      rw [eq_comm, div_eq_zero_iff] at hcd
      rcases hcd with h | h
      · simp [h0, Mz_zero] at h; linarith
      · linarith
    · subst hz; rw [h0, Mz_zero]
  · rw [Mx, log_bOf, bOf]; field_simp; ring
  · -- in `x = xOf y`: `√y √(y+4) = 2x − y`, and `(√y/2 + √(1 + y/4))² = 1 + x`
    show Mx (xOf y) = _
    have hx := xOf_nonneg hy
    have hyx : y = xOf y ^ 2 / (1 + xOf y) := by rw [← yOf_eq hx, yOf_xOf hy]
    have hxdef : xOf y = (y + √(y ^ 2 + 4 * y)) / 2 := rfl
    set x := xOf y
    have hs : √y * √(y + 4) = 2 * x - y := by
      rw [← sqrt_mul hy, show y * (y + 4) = y ^ 2 + 4 * y by ring, hxdef]; ring
    have hsq : (1 / 2 * √y + √(1 + (1 / 2 * √y) ^ 2)) ^ 2 = 1 + x := by
      have h1 : (1 / 2 * √y) ^ 2 = y / 4 := by rw [mul_pow, sq_sqrt hy]; ring
      rw [h1]
      have h2 : √y * √(1 + y / 4) = (2 * x - y) / 2 := by
        rw [← hs, show y + 4 = 4 * (1 + y / 4) by ring, sqrt_mul (by norm_num),
          show √(4 : ℝ) = 2 by rw [show (4 : ℝ) = 2 ^ 2 by norm_num, sqrt_sq (by norm_num)]]
        ring
      have h3 : √(1 + y / 4) ^ 2 = 1 + y / 4 := sq_sqrt (by positivity)
      nlinarith [sq_sqrt hy]
    have harsinh : 4 * arsinh (1 / 2 * √y) = 2 * log (1 + x) := by
      rw [arsinh, ← hsq, log_pow]; push_cast; ring
    rw [harsinh, Mx, log_bOf, bOf, mul_assoc (1 / 2 * √y), mul_comm (y + 2),
      ← mul_assoc, mul_assoc (1 / 2), hs]
    rw [hyx]
    field_simp
    ring

/-! ## Corollary 1: the two limits -/

lemma sqrt_bounds {v : ℝ} (hv : 0 ≤ v) :
    1 + v / 2 - v ^ 2 / 8 ≤ √(1 + v) ∧ √(1 + v) ≤ 1 + v / 2 := by
  constructor
  · by_cases h : 1 + v / 2 - v ^ 2 / 8 ≤ 0
    · exact h.trans (sqrt_nonneg _)
    · push Not at h
      have hv6 : v < 6 := by nlinarith
      rw [show 1 + v / 2 - v ^ 2 / 8 = √((1 + v / 2 - v ^ 2 / 8) ^ 2) from
        (sqrt_sq h.le).symm]
      exact sqrt_le_sqrt (by nlinarith [mul_nonneg (pow_nonneg hv 3) (by linarith : (0:ℝ) ≤ 8 - v)])
  · rw [show 1 + v / 2 = √((1 + v / 2) ^ 2) from (sqrt_sq (by positivity)).symm]
    exact sqrt_le_sqrt (by nlinarith)

/-- **Corollary 1, the derivative.** `𝓜'(z) → 0` as `z → ∞`; and with `z = t⁴`,
`𝓜'(z) = 1/t − ½ + t/8 + r` with `−t³/128 ≤ r ≤ 0`, i.e. `z^{−1/4} − ½ + ⅛ z^{1/4} + O(z^{3/4})`. -/
theorem cor1_derivative :
    Tendsto (fun z : ℝ => -1 / 2 + √(1 / 4 + 1 / √z)) atTop (𝓝 0) ∧
      ∀ t : ℝ, 0 < t → -(t ^ 3 / 128) ≤ (nu (t ^ 2) - 1) - (1 / t - 1 / 2 + t / 8) ∧
        (nu (t ^ 2) - 1) - (1 / t - 1 / 2 + t / 8) ≤ 0 := by
  refine ⟨?_, fun t ht => ?_⟩
  · have h0 : Tendsto (fun z : ℝ => 1 / √z) atTop (𝓝 0) := by
      have := (continuous_sqrt.tendsto 0).comp tendsto_inv_atTop_zero
      rw [sqrt_zero] at this
      refine this.congr fun z => ?_
      simp [Function.comp, sqrt_inv]
    have h1 := ((continuous_sqrt.tendsto (1 / 4 + 0)).comp (h0.const_add (1 / 4))).const_add
      (-1 / 2)
    have hq : √(1 / 4 + 0 : ℝ) = 1 / 2 := by
      rw [add_zero, show (1 / 4 : ℝ) = (1 / 2) ^ 2 by norm_num, sqrt_sq (by norm_num)]
    rw [hq, show (-1 / 2 + 1 / 2 : ℝ) = 0 by norm_num] at h1
    exact h1
  · have e : √(1 / 4 + 1 / t ^ 2) = √(1 + t ^ 2 / 4) / t := by
      rw [show 1 / 4 + 1 / t ^ 2 = (1 + t ^ 2 / 4) / t ^ 2 by field_simp; ring,
        sqrt_div' _ (by positivity), sqrt_sq ht.le]
    have hb := sqrt_bounds (v := t ^ 2 / 4) (by positivity)
    set r := √(1 + t ^ 2 / 4)
    have key : (nu (t ^ 2) - 1) - (1 / t - 1 / 2 + t / 8) = (r - 1 - t ^ 2 / 8) / t := by
      rw [nu, e]; field_simp; ring
    rw [key]
    constructor
    · rw [le_div_iff₀ ht]; nlinarith
    · exact div_nonpos_of_nonpos_of_nonneg (by nlinarith) ht.le

lemma xOf_sq {u : ℝ} (hu : 0 ≤ u) : xOf (u ^ 2) = u ^ 2 / 2 + u * √(1 + u ^ 2 / 4) := by
  rw [xOf, show (u ^ 2) ^ 2 + 4 * u ^ 2 = (2 * u) ^ 2 * (1 + u ^ 2 / 4) by ring,
    sqrt_mul (sq_nonneg _), sqrt_sq (by linarith)]
  ring

lemma hasDerivAt_My_sq {u : ℝ} (hu : 0 < u) :
    HasDerivAt (fun u => My (u ^ 2)) (4 * u ^ 2 * √(1 + u ^ 2 / 4) - 2 * u ^ 3) u := by
  have h := (hasDerivAt_My (by positivity : 0 < u ^ 2)).comp u (hasDerivAt_pow 2 u)
  refine h.congr_deriv ?_
  rw [xOf_sq hu.le]; simp; ring

/-- **Corollary 1, low acceleration.** `𝓜 = (4/3) y^{3/2} − ½ y² + ⅒ y^{5/2} + O(y^{7/2})` (the
paper's `O(y³)`, sharpened): with `y = u²`, `−u⁷/224 ≤ 𝓜 − (4/3 u³ − ½u⁴ + ⅒u⁵) ≤ 0` for every
`u ≥ 0`. -/
theorem cor1_small {u : ℝ} (hu : 0 ≤ u) :
    -(u ^ 7 / 224) ≤ My (u ^ 2) - (4 / 3 * u ^ 3 - 1 / 2 * u ^ 4 + 1 / 10 * u ^ 5) ∧
      My (u ^ 2) - (4 / 3 * u ^ 3 - 1 / 2 * u ^ 4 + 1 / 10 * u ^ 5) ≤ 0 := by
  have hc : ContinuousOn (fun u : ℝ => My (u ^ 2)) (Ici 0) :=
    continuousOn_My.comp (continuous_pow 2).continuousOn fun u _ => by
      simp only [mem_Ici]; positivity
  have hpoly : ∀ u : ℝ, HasDerivAt (fun u : ℝ => 4 / 3 * u ^ 3 - 1 / 2 * u ^ 4 + 1 / 10 * u ^ 5)
      (4 * u ^ 2 - 2 * u ^ 3 + u ^ 4 / 2) u := fun u => by
    have := (((hasDerivAt_pow 3 u).const_mul (4 / 3)).sub ((hasDerivAt_pow 4 u).const_mul (1 / 2))).add
      ((hasDerivAt_pow 5 u).const_mul (1 / 10))
    convert this using 1; push_cast; ring
  have hpc : Continuous fun u : ℝ => 4 / 3 * u ^ 3 - 1 / 2 * u ^ 4 + 1 / 10 * u ^ 5 := by fun_prop
  have hr : ∀ u : ℝ, 0 ≤ u → -(u ^ 4 / 128) ≤ √(1 + u ^ 2 / 4) - 1 - u ^ 2 / 8 ∧
      √(1 + u ^ 2 / 4) - 1 - u ^ 2 / 8 ≤ 0 := fun u hu => by
    have := sqrt_bounds (v := u ^ 2 / 4) (by positivity)
    constructor <;> nlinarith [this.1, this.2]
  constructor
  · set H : ℝ → ℝ := fun u => My (u ^ 2) - (4 / 3 * u ^ 3 - 1 / 2 * u ^ 4 + 1 / 10 * u ^ 5) +
      u ^ 7 / 224 with hH
    set H' : ℝ → ℝ := fun u => 4 * u ^ 2 * √(1 + u ^ 2 / 4) - 2 * u ^ 3 -
      (4 * u ^ 2 - 2 * u ^ 3 + u ^ 4 / 2) + 7 * u ^ 6 / 224 with hH'
    have hHc : ContinuousOn H (Ici 0) :=
      (hc.sub hpc.continuousOn).add ((continuous_pow 7).div_const 224).continuousOn
    have hHd : ∀ u : ℝ, 0 < u → HasDerivAt H (H' u) u := fun u hu =>
      ((hasDerivAt_My_sq hu).sub (hpoly u)).add ((hasDerivAt_pow 7 u).div_const 224)
        |>.congr_deriv (by simp only [hH']; push_cast; ring)
    have hH0 : H 0 = 0 := by simp [hH, My, xOf_zero, Mx_zero]
    have hHpos : ∀ u : ℝ, 0 < u → 0 ≤ H' u := fun u hu => by
      have h := (hr u hu.le).1
      simp only [hH']
      nlinarith [mul_le_mul_of_nonneg_left h (by positivity : (0 : ℝ) ≤ 4 * u ^ 2)]
    have := AqualEnergy.nonneg_of_deriv hHc hHd hH0 hHpos u hu
    simp only [hH] at this
    linarith
  · set H : ℝ → ℝ := fun u => (4 / 3 * u ^ 3 - 1 / 2 * u ^ 4 + 1 / 10 * u ^ 5) - My (u ^ 2)
      with hH
    set H' : ℝ → ℝ := fun u => (4 * u ^ 2 - 2 * u ^ 3 + u ^ 4 / 2) -
      (4 * u ^ 2 * √(1 + u ^ 2 / 4) - 2 * u ^ 3) with hH'
    have hHc : ContinuousOn H (Ici 0) := hpc.continuousOn.sub hc
    have hHd : ∀ u : ℝ, 0 < u → HasDerivAt H (H' u) u := fun u hu =>
      (hpoly u).sub (hasDerivAt_My_sq hu)
    have hH0 : H 0 = 0 := by simp [hH, My, xOf_zero, Mx_zero]
    have hHpos : ∀ u : ℝ, 0 < u → 0 ≤ H' u := fun u hu => by
      have h := (hr u hu.le).2
      simp only [hH']
      nlinarith [mul_le_mul_of_nonneg_left h (by positivity : (0 : ℝ) ≤ 4 * u ^ 2)]
    have := AqualEnergy.nonneg_of_deriv hHc hHd hH0 hHpos u hu
    simp only [hH] at this
    linarith

/-- The exact form at high acceleration: `𝓜 − 2y + 2 ln y = 1 − b² + 4 ln(1 − b)`, with `b y = (1 − b)²`. -/
lemma My_large_exact {y : ℝ} (hy : 0 < y) :
    My y - 2 * y + 2 * log y = 1 - bOf (xOf y) ^ 2 + 4 * log (1 - bOf (xOf y)) ∧
      bOf (xOf y) * y = (1 - bOf (xOf y)) ^ 2 ∧ 0 < bOf (xOf y) ∧ bOf (xOf y) < 1 := by
  have hx := xOf_pos hy
  have hyx : y = xOf y ^ 2 / (1 + xOf y) := by rw [← yOf_eq hx.le, yOf_xOf hy.le]
  set x := xOf y
  have hb : bOf x = 1 / (1 + x) := rfl
  have hby : bOf x * y = (1 - bOf x) ^ 2 := by rw [hb, hyx]; field_simp; ring
  have hb0 : 0 < bOf x := by rw [hb]; positivity
  have hb1 : bOf x < 1 := by rw [hb, div_lt_one (by linarith)]; linarith
  refine ⟨?_, hby, hb0, hb1⟩
  have hlog : 2 * log (bOf x) + 2 * log y = 4 * log (1 - bOf x) := by
    rw [mul_comm 2 (log (bOf x)), mul_comm 2 (log y), ← add_mul, ← log_mul hb0.ne' hy.ne', hby,
      log_pow]; push_cast; ring
  have hxy : 2 * x - 2 * y = 2 - 2 * bOf x := by rw [hyx, hb]; field_simp; ring
  show Mx x - 2 * y + 2 * log y = _
  rw [Mx]; linarith

/-- **Corollary 1, high acceleration.** `𝓜 = 2y − 2 ln y + 1 − 4/y + 5/y² + O(y^{−3})`: for every
`y ≥ 2` the remainder is at most `40/y³` in absolute value. -/
theorem cor1_large {y : ℝ} (hy : 2 ≤ y) :
    |My y - (2 * y - 2 * log y + 1 - 4 / y + 5 / y ^ 2)| ≤ 40 / y ^ 3 := by
  have hy0 : 0 < y := by linarith
  obtain ⟨hex, hby, hb0, hb1⟩ := My_large_exact hy0
  set b := bOf (xOf y)
  set w := 1 / y with hw
  have hwy : w * y = 1 := by rw [hw]; field_simp
  have hw0 : 0 < w := by positivity
  have hw2 : w ≤ 1 / 2 := by rw [hw, div_le_div_iff₀ hy0 (by norm_num)]; linarith
  have hbw : b = (1 - b) ^ 2 * w := by
    have := congrArg (· * w) hby; rw [mul_assoc, mul_comm y w, hwy] at this
    linarith
  have hbw' : b ≤ w := by
    rw [hbw]; nlinarith [sq_nonneg b]
  have hlow : w - 2 * w ^ 2 ≤ b := by
    rw [hbw]
    have : (1 - w) ^ 2 ≤ (1 - b) ^ 2 := by nlinarith
    nlinarith [mul_le_mul_of_nonneg_right this hw0.le]
  have hup : b ≤ w - 2 * w ^ 2 + 5 * w ^ 3 := by
    have h1 : 1 - b ≤ 1 - w + 2 * w ^ 2 := by linarith
    have h2 : (1 - b) ^ 2 ≤ (1 - w + 2 * w ^ 2) ^ 2 := by
      apply pow_le_pow_left₀ (by linarith) h1
    rw [hbw]
    nlinarith [mul_le_mul_of_nonneg_right h2 hw0.le, pow_pos hw0 4,
      mul_nonneg (pow_pos hw0 4).le (by linarith : (0 : ℝ) ≤ 1 - w)]
  -- the logarithm to second order
  have hR : |(b + b ^ 2 / 2) + log (1 - b)| ≤ 2 * b ^ 3 := by
    have h := Real.abs_log_sub_add_sum_range_le (x := b) (by rw [abs_of_pos hb0]; exact hb1) 2
    simp only [Finset.sum_range_succ, Finset.sum_range_zero] at h
    norm_num at h
    rw [abs_of_pos hb0] at h
    have hb2 : b ≤ 1 / 2 := hbw'.trans hw2
    calc _ ≤ b ^ 3 / (1 - b) := by convert h using 2
      _ ≤ 2 * b ^ 3 := by rw [div_le_iff₀ (by linarith)]; nlinarith [pow_pos hb0 3]
  have hb3 : b ^ 3 ≤ w ^ 3 := pow_le_pow_left₀ hb0.le hbw' 3
  have hsplit : My y - (2 * y - 2 * log y + 1 - 4 / y + 5 / y ^ 2) =
      3 * ((w - b) * (w + b)) - 4 * (b - w + 2 * w ^ 2) + 4 * ((b + b ^ 2 / 2) + log (1 - b)) := by
    have e1 : 4 / y = 4 * w := by rw [hw]; ring
    have e2 : 5 / y ^ 2 = 5 * w ^ 2 := by rw [hw]; field_simp
    rw [e1, e2]; linarith [hex]
  have hA0 : 0 ≤ (w - b) * (w + b) := mul_nonneg (by linarith) (by linarith)
  have hA1 : (w - b) * (w + b) ≤ 4 * w ^ 3 := by
    nlinarith [mul_le_mul (show w - b ≤ 2 * w ^ 2 by linarith) (show w + b ≤ 2 * w by linarith)
      (by linarith) (by positivity)]
  have e3 : 40 / y ^ 3 = 40 * w ^ 3 := by rw [hw]; field_simp
  rw [hsplit, e3, abs_le]
  obtain ⟨hR1, hR2⟩ := abs_le.mp hR
  constructor <;> nlinarith

/-! ## Theorem 3: Legendre duality -/

lemma hasDerivAt_Q {y : ℝ} (hy : 0 < y) : HasDerivAt Q (2 * xOf y) y :=
  ((hasDerivAt_pow 2 y).add (hasDerivAt_My hy)).congr_deriv (by push_cast; ring)

lemma Q_yOf {x : ℝ} (hx : 0 ≤ x) : Q (yOf x) = yOf x ^ 2 + Mx x := by
  rw [Q, My, xOf_yOf hx]

lemma continuousOn_g : ContinuousOn g (Ici 0) := AqualEnergy.continuousOn_g

/-- **Theorem 3.** At `y = xμ(x)`: `g(x) + Q(y) = 2xy`, `g'(x) = 2y`, `Q'(y) = 2x`, and
`Q(y) = max_{x' ≥ 0} [2x'y − g(x')]`, attained only at `x' = x`. In `b`, `g = x² − 2x − 2 ln b` and the
logarithms cancel in `g + 𝓜`. The twin field is `|∇φ̂| = μ(x) < 1` (units `a₀`). -/
theorem theorem3 {x : ℝ} (hx : 0 ≤ x) :
    g x + Q (yOf x) = 2 * x * yOf x ∧ HasDerivAt g (2 * yOf x) x ∧
      (0 < x → HasDerivAt Q (2 * x) (yOf x)) ∧
      (∀ x', 0 ≤ x' → 2 * x' * yOf x - g x' ≤ Q (yOf x) ∧
        (2 * x' * yOf x - g x' = Q (yOf x) ↔ x' = x)) ∧
      g x = x ^ 2 - 2 * x - 2 * log (bOf x) ∧
      g x + Mx x = x ^ 2 - 1 + 2 * bOf x - bOf x ^ 2 ∧
      x - yOf x = law x ∧ law x < 1 := by
  have h1 : 0 < 1 + x := by linarith
  have hid : g x + Q (yOf x) = 2 * x * yOf x := by
    rw [Q_yOf hx, AqualEnergy.g, Mx, log_bOf, bOf, yOf_eq hx]; field_simp; ring
  have hgd : ∀ t : ℝ, -1 < t → HasDerivAt g (2 * yOf t) t := fun t ht =>
    (AqualEnergy.hasDerivAt_g ht).congr_deriv (by
      rw [yOf, law, add_comm t 1]; field_simp)
  refine ⟨hid, hgd x (by linarith), fun hx0 => ?_, fun x' hx' => ?_, ?_, ?_, ?_, ?_⟩
  · have := hasDerivAt_Q (yOf_pos hx0)
    rwa [xOf_yOf hx] at this
  · -- `h t = g t − 2 t y` is minimised exactly at `t = x`
    set y := yOf x
    have hgc : ContinuousOn g (Icc (min x x') (max x x')) :=
      continuousOn_g.mono fun t ht => by simp only [mem_Ici]; exact le_trans (le_min hx hx') ht.1
    have hmin : x' ≠ x → g x - 2 * x * y < g x' - 2 * x' * y := by
      intro hne
      rcases lt_or_gt_of_ne hne with hlt | hlt
      · obtain ⟨c, hc, hcd⟩ := exists_hasDerivAt_eq_slope (fun t => g t - 2 * t * y)
          (fun t => 2 * yOf t - 2 * y) hlt
          ((hgc.mono (Icc_subset_Icc (min_le_right _ _) (le_max_left _ _))).sub (by fun_prop))
          fun t ht => ((hgd t (by linarith [ht.1])).sub
            (((hasDerivAt_id' (x := t)).const_mul 2).mul_const y)).congr_deriv (by ring)
        have hy : yOf c < y := yOf_strictMonoOn (by simp only [mem_Ici]; linarith [hc.1])
          (show x ∈ Ici (0 : ℝ) from hx) hc.2
        rw [eq_div_iff (by linarith)] at hcd
        nlinarith [hc.2]
      · obtain ⟨c, hc, hcd⟩ := exists_hasDerivAt_eq_slope (fun t => g t - 2 * t * y)
          (fun t => 2 * yOf t - 2 * y) hlt
          ((hgc.mono (Icc_subset_Icc (min_le_left _ _) (le_max_right _ _))).sub (by fun_prop))
          fun t ht => ((hgd t (by linarith [ht.1])).sub
            (((hasDerivAt_id' (x := t)).const_mul 2).mul_const y)).congr_deriv (by ring)
        have hy : y < yOf c := yOf_strictMonoOn (show x ∈ Ici (0 : ℝ) from hx)
          (by simp only [mem_Ici]; linarith [hc.1]) hc.1
        rw [eq_div_iff (by linarith)] at hcd
        nlinarith [hc.1]
    have hQ : Q y = 2 * x * y - g x := by linarith [hid]
    refine ⟨?_, ⟨fun h => ?_, fun h => by rw [h, hQ]⟩⟩
    · by_cases hne : x' = x
      · rw [hne, hQ]
      · have := hmin hne; rw [hQ]; linarith
    · by_contra hne
      have := hmin hne; rw [hQ] at h; linarith
  · rw [AqualEnergy.g, log_bOf]; ring
  · rw [AqualEnergy.g, Mx, log_bOf]; ring
  · rw [yOf, law]; field_simp; ring
  · rw [law, div_lt_one (by linarith)]; linarith

/-! ## Corollary 2: convexity -/

lemma xOf_strictMonoOn : StrictMonoOn xOf (Ici 0) := by
  intro a ha b hb hab
  by_contra h
  push Not at h
  have := yOf_strictMonoOn.monotoneOn (xOf_nonneg hb) (xOf_nonneg ha) h
  rw [yOf_xOf ha, yOf_xOf hb] at this
  linarith

lemma continuousOn_Q : ContinuousOn Q (Ici 0) :=
  (continuous_pow 2).continuousOn.add continuousOn_My

lemma Q_strictMonoOn : StrictMonoOn Q (Ici 0) := by
  apply strictMonoOn_of_deriv_pos (convex_Ici 0) continuousOn_Q
  intro y hy
  rw [interior_Ici, mem_Ioi] at hy
  rw [(hasDerivAt_Q hy).deriv]; have := xOf_pos hy; linarith

lemma Q_strictConvexOn : StrictConvexOn ℝ (Ici 0) Q := by
  apply StrictMonoOn.strictConvexOn_of_deriv (convex_Ici 0) continuousOn_Q
  rw [interior_Ici]
  intro a ha b hb hab
  simp only [mem_Ioi] at ha hb
  rw [(hasDerivAt_Q ha).deriv, (hasDerivAt_Q hb).deriv]
  have := xOf_strictMonoOn (show a ∈ Ici (0 : ℝ) from ha.le) (show b ∈ Ici (0 : ℝ) from hb.le) hab
  linarith

/-- A radial function `φ(|q|)` with `φ` strictly convex and strictly increasing on `[0, ∞)` is
strictly convex. -/
theorem radial_strictConvex {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {φ : ℝ → ℝ} (hconv : StrictConvexOn ℝ (Ici 0) φ) (hmono : StrictMonoOn φ (Ici 0)) :
    StrictConvexOn ℝ univ (fun q : E => φ ‖q‖) := by
  refine ⟨convex_univ, fun p _ p' _ hne a b ha hb hab => ?_⟩
  simp only [smul_eq_mul]
  have hr := norm_nonneg p; have hs := norm_nonneg p'
  have ht : ‖a • p + b • p'‖ ≤ a * ‖p‖ + b * ‖p'‖ := by
    calc ‖a • p + b • p'‖ ≤ ‖a • p‖ + ‖b • p'‖ := norm_add_le _ _
      _ = a * ‖p‖ + b * ‖p'‖ := by
        rw [norm_smul, norm_smul, Real.norm_eq_abs, Real.norm_eq_abs, abs_of_pos ha,
          abs_of_pos hb]
  have hm : φ ‖a • p + b • p'‖ ≤ φ (a * ‖p‖ + b * ‖p'‖) :=
    hmono.monotoneOn (norm_nonneg _) (by simp only [mem_Ici]; positivity) ht
  rcases eq_or_ne ‖p‖ ‖p'‖ with hrs | hrs
  · have hlt : ‖a • p + b • p'‖ < ‖p‖ := norm_combo_lt_of_ne le_rfl hrs.ge hne ha hb hab
    have := hmono (norm_nonneg _) (show ‖p‖ ∈ Ici (0 : ℝ) from hr) hlt
    rw [← hrs]
    calc φ ‖a • p + b • p'‖ < φ ‖p‖ := this
      _ = a * φ ‖p‖ + b * φ ‖p‖ := by rw [← add_mul, hab, one_mul]
  · have := hconv.2 (show ‖p‖ ∈ Ici (0 : ℝ) from hr) (show ‖p'‖ ∈ Ici (0 : ℝ) from hs) hrs ha hb hab
    simp only [smul_eq_mul] at this
    exact lt_of_le_of_lt hm this

/-- **Corollary 2.** `W(q) = Q(|q|)` is strictly convex (on any real inner product space). With
`x = xOf y`, `y > 0`: the radial eigenvalues are `Q'/y = 2ν` and `Q'' = 2(x+1)²/(x(x+2))`, both
positive, with ratio `(x+1)/(x+2) ∈ [½, 1)`, the reciprocal of the AQUAL ratio `(x+2)/(x+1)`. -/
theorem cor2 :
    (∀ {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E],
      StrictConvexOn ℝ univ (fun q : E => Q ‖q‖)) ∧
      ∀ y : ℝ, 0 < y →
        HasDerivAt (fun y => 2 * xOf y) (2 * (xOf y + 1) ^ 2 / (xOf y * (xOf y + 2))) y ∧
        2 * xOf y / y = 2 * nu y ∧ 0 < 2 * nu y ∧
        0 < 2 * (xOf y + 1) ^ 2 / (xOf y * (xOf y + 2)) ∧
        (2 * (xOf y + 1) ^ 2 / (xOf y * (xOf y + 2))) / (2 * xOf y / y) =
          (xOf y + 1) / (xOf y + 2) ∧
        1 / 2 ≤ (xOf y + 1) / (xOf y + 2) ∧ (xOf y + 1) / (xOf y + 2) < 1 ∧
        (xOf y + 1) / (xOf y + 2) * ((xOf y + 2) / (xOf y + 1)) = 1 := by
  refine ⟨fun {E} _ _ => radial_strictConvex Q_strictConvexOn Q_strictMonoOn, fun y hy => ?_⟩
  have hx := xOf_pos hy
  have hyx : y = xOf y ^ 2 / (1 + xOf y) := by rw [← yOf_eq hx.le, yOf_xOf hy.le]
  have hnu := nu_eq hy
  have hd : HasDerivAt (fun y => 2 * xOf y) (2 * (xOf y + 1) ^ 2 / (xOf y * (xOf y + 2))) y :=
    ((hasDerivAt_xOf hy).const_mul 2).congr_deriv (by field_simp)
  set x := xOf y
  refine ⟨hd, by rw [hnu]; ring,
    by rw [hnu]; positivity, by positivity, ?_, ?_, ?_, ?_⟩
  · rw [hyx]; field_simp; ring
  · rw [le_div_iff₀ (by linarith)]; linarith
  · rw [div_lt_one (by linarith)]; linarith
  · field_simp

#print axioms BimondInteraction.combination
#print axioms BimondInteraction.unique_combination
#print axioms BimondInteraction.constant_iff
#print axioms BimondInteraction.qumond
#print axioms BimondInteraction.lemma1
#print axioms BimondInteraction.lemma1_parity
#print axioms BimondInteraction.second_root_sign
#print axioms BimondInteraction.prop1
#print axioms BimondInteraction.hasDerivAt_My
#print axioms BimondInteraction.theorem2
#print axioms BimondInteraction.cor1_derivative
#print axioms BimondInteraction.cor1_small
#print axioms BimondInteraction.cor1_large
#print axioms BimondInteraction.theorem3
#print axioms BimondInteraction.radial_strictConvex
#print axioms BimondInteraction.cor2

end BimondInteraction
