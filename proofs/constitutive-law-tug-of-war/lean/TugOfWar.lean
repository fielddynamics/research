import WalshEigenmodes
import ConstitutiveLaw
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.Calculus.Deriv.Pow

/-!
# The Constitutive Law as a Tug of War

A formalisation of `proofs/constitutive-law-tug-of-war/constitutive_law_tug_of_war.tex`.

The constitutive law `μ(x) = x/(x + 1)`, `x = g/a₀`, is read as TetA's share of a tug of war in
which TetA pulls with the local field `g` and TetB pulls with `a₀`. The file proves:

* **Lemma 1 (two teams).** On the cube, a `T_d`-symmetric state holds one value on each chamber;
  its TetA share is `w_A/(w_A + w_B)`, the rope position `c_xyz/c₁` is `(w_A − w_B)/(w_A + w_B)`,
  the inversion swaps the teams, and the vortex (`T₂`) modes cannot move the rope. This is read
  from `WalshEigenmodes`.
* **Theorem 1.** A law obeying the screening relation `xⁿ(1 − μ)ᵐ = μᵖ` is exchange-symmetric
  exactly when `m = p`, and then its odds are the power `x^(n/p)`.
* **Theorem 2.** For the power-law family `μ_k = x^k/(1 + x^k)`, `k = 1` is equivalent to the two
  strengths being accelerations (`μ (g + a₀) = g`) and to flat rotation curves in the deep field;
  `k = 1` gives the Tully–Fisher relation and is `ConstitutiveLaw.law`.
* **Proposition 1.** The bound-state law `x(1 − μ)² = μ`, the standard function and the exponential
  function all break the exchange.
* **Proposition 2.** One Field Origin node between the teams is their weighted average; the cap
  `(1 − μ) g = μ a₀ < a₀`; the exchange on pulls is `g ↦ a₀²/g`.
* **Theorem 3.** The decoding-mass ratio is `M_dec/M_phot = (g + w)/(g + a₀)`, with `w` TetB's
  measured strength; quiet, drive and brake are `w = a₀`, `w > a₀`, `w < a₀`.
* **Proposition 3.** The Burgers vortex balances inflow, stretching and diffusion exactly, and the
  Lamb–Oseen vortex diffuses exactly when there is no drain.

## Not formalised
The counterexample of Proposition 1 (a), whose MOND limits need asymptotic analysis; the
degree-one characterisation (iv) of Theorem 2 (proved in `ConstitutiveLaw.unique_law` in the form
the letter uses); the numerical rotation curves and the Burgers peak radius; and the explicit
cube-with-centre model (its reduction is `WalshEigenmodes.whole_cube`). The script
`verify_constitutive_law_tug_of_war.py` checks all of them.
-/

open Real

namespace TugOfWar

open WalshEigenmodes

/-! ## Lemma 1: the cube forces two teams -/

/-- The tug-of-war state: TetA's four corners hold `wA`, TetB's hold `wB`. -/
noncomputable def teams (wA wB : ℝ) : C → ℝ := fun s => if inA s then wA else wB

lemma SA_teams (wA wB : ℝ) : SA (teams wA wB) = 4 * wA := by
  rw [SA_expand]; simp [teams, inA]; ring

lemma SB_teams (wA wB : ℝ) : SB (teams wA wB) = 4 * wB := by
  rw [SB_expand]; simp [teams, inA]; ring

/-- **Lemma 1.** (i) Every `T_d`-symmetric corner state is a `teams` state. (ii) Its TetA share is
`w_A/(w_A + w_B)`. (iii) The rope position `s = c_xyz/c₁` is `(w_A − w_B)/(w_A + w_B) = 2μ − 1`.
(iv) The inversion `−I` swaps the teams. (v) Adding any `T₂` (vortex) mode leaves `μ` unchanged. -/
theorem lemma1 :
    (∀ f : C → ℝ, (∀ g s, f (act g s) = f s) →
      f = teams (f (true, true, true)) (f (false, false, false))) ∧
    (∀ wA wB : ℝ, 0 < wA + wB → mu (teams wA wB) = wA / (wA + wB)) ∧
    (∀ wA wB : ℝ, 0 < wA + wB →
      coef Sxyz (teams wA wB) / coef S1 (teams wA wB) = (wA - wB) / (wA + wB) ∧
      coef Sxyz (teams wA wB) / coef S1 (teams wA wB) = 2 * mu (teams wA wB) - 1) ∧
    (∀ wA wB : ℝ, (fun s => teams wA wB (flip (true, true, true) s)) = teams wB wA) ∧
    (∀ (φ : C → ℝ) S (c : ℝ), grade S = 1 ∨ grade S = 2 → mu (φ + c • w S) = mu φ) := by
  have hmu : ∀ wA wB : ℝ, 0 < wA + wB → mu (teams wA wB) = wA / (wA + wB) := by
    intro wA wB h
    rw [mu, SA_teams, SB_teams, show 4 * wA + 4 * wB = 4 * (wA + wB) by ring,
      mul_div_mul_left _ _ (by norm_num : (4 : ℝ) ≠ 0)]
  refine ⟨fun f h => funext fun s => ?_, hmu, fun wA wB h => ?_, fun wA wB => funext fun s => ?_,
    node_mu.2.2.2⟩
  · rw [scalar_invariant f h s]; rfl
  · have h1 := node_mu.1 (teams wA wB); have h2 := node_mu.2.1 (teams wA wB)
    rw [SA_teams, SB_teams] at h1 h2
    have hs : coef Sxyz (teams wA wB) / coef S1 (teams wA wB) = (wA - wB) / (wA + wB) := by
      rw [h1, h2, div_div_div_cancel_right₀ (by norm_num : (8 : ℝ) ≠ 0),
        show 4 * wA - 4 * wB = 4 * (wA - wB) by ring, show 4 * wA + 4 * wB = 4 * (wA + wB) by ring,
        mul_div_mul_left _ _ (by norm_num : (4 : ℝ) ≠ 0)]
    refine ⟨hs, ?_⟩
    rw [hs, hmu wA wB h]; field_simp; ring
  · simp only [teams, inversion_exchanges]
    cases inA s <;> simp

/-- **The tug of war on the cube.** TetA's corners at `g`, TetB's at `a₀`: the share is the law. -/
theorem cube_tug_of_war (g a0 : ℝ) (hg : 0 < g) (ha : 0 < a0) :
    mu (teams g a0) = g / (g + a0) ∧ mu (teams g a0) = ConstitutiveLaw.law (g / a0) := by
  have h := lemma1.2.1 g a0 (by linarith)
  refine ⟨h, ?_⟩
  rw [h, ConstitutiveLaw.law]; field_simp

/-! ## Theorem 1: exchange turns screening into a power law -/

/-- The screening relation `xⁿ (1 − μ)ᵐ = μᵖ` on `x > 0`. -/
def Screens (n m p : ℝ) (μ : ℝ → ℝ) : Prop :=
  ∀ x, 0 < x → x ^ n * (1 - μ x) ^ m = μ x ^ p

/-- The exchange `μ(1/x) = 1 − μ(x)`. -/
def Exchange (μ : ℝ → ℝ) : Prop := ∀ x, 0 < x → μ x⁻¹ = 1 - μ x

/-- The power-law family `μ_k(x) = x^k/(1 + x^k)`. -/
noncomputable def muk (k x : ℝ) : ℝ := x ^ k / (1 + x ^ k)

/-- The exchange puts the even split at `x = 1`. -/
lemma exchange_half (μ : ℝ → ℝ) (h : Exchange μ) : μ 1 = 1 / 2 := by
  have := h 1 one_pos; rw [inv_one] at this; linarith

/-- Every member of the family is exchange-symmetric. -/
lemma muk_exchange (k : ℝ) : Exchange (muk k) := by
  intro x hx
  have hk : 0 < x ^ k := rpow_pos_of_pos hx k
  rw [muk, muk, inv_rpow hx.le]
  field_simp
  ring

/-- **Theorem 1.** Let `μ` take values in `(0, 1)` on `x > 0` and obey the screening relation
with `n, p > 0`. Then `μ` is exchange-symmetric if and only if `m = p`; and when `m = p`, `μ` is
the power law `μ_{n/p}`: its odds are `μ/(1 − μ) = x^(n/p)`. -/
theorem theorem1 (n m p : ℝ) (hp : 0 < p) (μ : ℝ → ℝ)
    (hr : ∀ x, 0 < x → 0 < μ x ∧ μ x < 1) (hs : Screens n m p μ) :
    (Exchange μ ↔ m = p) ∧
      (m = p → ∀ x, 0 < x → μ x / (1 - μ x) = x ^ (n / p) ∧ μ x = muk (n / p) x) := by
  have power : m = p → ∀ x, 0 < x → μ x / (1 - μ x) = x ^ (n / p) ∧ μ x = muk (n / p) x := by
    rintro rfl x hx
    obtain ⟨h0, h1⟩ := hr x hx
    have h1' : 0 < 1 - μ x := by linarith
    have hodds : (μ x / (1 - μ x)) ^ m = x ^ n := by
      rw [div_rpow h0.le h1'.le, ← hs x hx]
      field_simp
    have hO : μ x / (1 - μ x) = x ^ (n / m) := by
      have := congrArg (fun y => y ^ m⁻¹) hodds
      rw [rpow_rpow_inv (div_pos h0 h1').le hp.ne', ← rpow_mul hx.le] at this
      rwa [div_eq_mul_inv]
    refine ⟨hO, ?_⟩
    have hk : 0 < x ^ (n / m) := rpow_pos_of_pos hx _
    rw [muk, ← hO]
    field_simp
    ring
  refine ⟨⟨fun hX => ?_, fun hmp => ?_⟩, power⟩
  · have h1 := exchange_half μ hX
    have := hs 1 one_pos
    rw [one_rpow, one_mul, h1, show (1 : ℝ) - 1 / 2 = 1 / 2 by norm_num] at this
    have hl := congrArg Real.log this
    rw [Real.log_rpow (by norm_num), Real.log_rpow (by norm_num)] at hl
    have hlog : Real.log (1 / 2 : ℝ) ≠ 0 := by
      rw [one_div, Real.log_inv]; exact neg_ne_zero.2 (Real.log_pos (by norm_num)).ne'
    exact mul_right_cancel₀ hlog hl
  · intro x hx
    rw [(power hmp x⁻¹ (inv_pos.2 hx)).2, (power hmp x hx).2]
    exact muk_exchange _ x hx

/-! ## Theorem 2: what fixes the power -/

/-- **Theorem 2 (i) ⟺ (ii).** The two strengths add up in the units of the field,
`μ_k(g/a₀)·(g + a₀) = g` for every pull, exactly when `k = 1`. -/
theorem strengths_are_accelerations (k a0 : ℝ) (ha : 0 < a0) :
    (∀ g, 0 < g → muk k (g / a0) * (g + a0) = g) ↔ k = 1 := by
  constructor
  · intro h
    have h2 := h (2 * a0) (by linarith)
    rw [show 2 * a0 / a0 = (2 : ℝ) by field_simp, muk] at h2
    have hk : 0 < (2 : ℝ) ^ k := rpow_pos_of_pos (by norm_num) k
    have h22 : (2 : ℝ) ^ k = 2 := by
      field_simp at h2; nlinarith
    have hl := congrArg Real.log h22
    rw [Real.log_rpow (by norm_num)] at hl
    have : Real.log 2 ≠ 0 := (Real.log_pos (by norm_num)).ne'
    calc k = k * Real.log 2 / Real.log 2 := by field_simp
      _ = 1 := by rw [hl, div_self this]
  · rintro rfl g hg
    rw [muk, rpow_one]
    field_simp
    ring

/-- The deep-field pull: `g^(k+1) = GM a₀^k / r²`, i.e. `μ ≈ x^k` with `μ g = GM/r²`. -/
noncomputable def gdeep (k GM a0 r : ℝ) : ℝ := (GM * a0 ^ k * r ^ (-2 : ℝ)) ^ (1 / (k + 1))

/-- **Theorem 2 (iii).** In the deep field the law `μ = x^k` gives `x^k g = GM/r²`, and the circular
speed obeys `v² = g r = (GM a₀^k)^(1/(k+1)) r^((k−1)/(k+1))`: the rotation curve is flat exactly
when `k = 1`, and then `v⁴ = GM a₀` (Tully–Fisher). -/
theorem deep_field (k GM a0 : ℝ) (hk : 0 < k) (hGM : 0 < GM) (ha : 0 < a0) :
    (∀ r, 0 < r → (gdeep k GM a0 r / a0) ^ k * gdeep k GM a0 r = GM * r ^ (-2 : ℝ)) ∧
    (∀ r, 0 < r → gdeep k GM a0 r * r = (GM * a0 ^ k) ^ (1 / (k + 1)) * r ^ ((k - 1) / (k + 1))) ∧
    ((∀ r₁ r₂, 0 < r₁ → 0 < r₂ → gdeep k GM a0 r₁ * r₁ = gdeep k GM a0 r₂ * r₂) ↔ k = 1) ∧
    (k = 1 → ∀ r, 0 < r → (gdeep k GM a0 r * r) ^ 2 = GM * a0) := by
  have hA : 0 < GM * a0 ^ k := mul_pos hGM (rpow_pos_of_pos ha k)
  have hk1 : k + 1 ≠ 0 := by linarith
  have speed : ∀ r, 0 < r →
      gdeep k GM a0 r * r = (GM * a0 ^ k) ^ (1 / (k + 1)) * r ^ ((k - 1) / (k + 1)) := by
    intro r hr
    rw [gdeep, mul_rpow hA.le (rpow_pos_of_pos hr _).le, ← rpow_mul hr.le, mul_assoc]
    congr 1
    rw [← rpow_add_one hr.ne']
    congr 1
    field_simp
    ring
  refine ⟨fun r hr => ?_, speed, ⟨fun h => ?_, ?_⟩, ?_⟩
  · have hg : 0 < gdeep k GM a0 r := rpow_pos_of_pos (mul_pos hA (rpow_pos_of_pos hr _)) _
    rw [div_rpow hg.le ha.le, div_mul_eq_mul_div, ← rpow_add_one hg.ne', gdeep, ← rpow_mul
      (mul_pos hA (rpow_pos_of_pos hr _)).le, show 1 / (k + 1) * (k + 1) = 1 by field_simp, rpow_one]
    field_simp
  · have h12 := h 1 2 one_pos (by norm_num)
    rw [speed 1 one_pos, speed 2 (by norm_num), one_rpow, mul_one] at h12
    have hc : 0 < (GM * a0 ^ k) ^ (1 / (k + 1)) := rpow_pos_of_pos hA _
    have h2 : (2 : ℝ) ^ ((k - 1) / (k + 1)) = 1 := by
      have := h12.symm; field_simp at this ⊢; nlinarith [rpow_pos_of_pos (by norm_num : (0:ℝ) < 2) ((k - 1) / (k + 1))]
    have hl := congrArg Real.log h2
    rw [Real.log_rpow (by norm_num), Real.log_one] at hl
    have : (k - 1) / (k + 1) = 0 := by
      rcases mul_eq_zero.1 hl with h | h
      · exact h
      · exact absurd h (Real.log_pos (by norm_num)).ne'
    rw [div_eq_zero_iff] at this
    rcases this with h | h
    · linarith
    · exact absurd h hk1
  · rintro rfl r₁ r₂ h₁ h₂
    rw [speed r₁ h₁, speed r₂ h₂]
    norm_num
  · rintro rfl r hr
    have hA' : 0 < GM * a0 := mul_pos hGM ha
    rw [speed r hr]
    norm_num
    rw [← rpow_natCast, ← rpow_mul hA'.le]
    norm_num

/-- `k = 1` is the constitutive law of the AQUAL and BIMOND formalisations. -/
theorem muk_one (x : ℝ) : muk 1 x = ConstitutiveLaw.law x := by
  rw [muk, rpow_one, ConstitutiveLaw.law, add_comm]

/-! ## Proposition 1: the premises are necessary -/

/-- **Proposition 1.** (b) Unequal screening powers break the exchange: the bound-state law
`x(1 − μ)² = μ` is not exchange-symmetric, and at `x = 1` its root is `(3 − √5)/2 = 1/φ²`, not
`1/2`. (d) The standard function `x/√(1 + x²)` and the exponential function `1 − e^(−x)` break the
exchange, since they miss `1/2` at `x = 1`. (c) is Theorem 2: `k ≠ 1` is not flat. -/
theorem necessity :
    (∀ μ : ℝ → ℝ, (∀ x, 0 < x → 0 < μ x ∧ μ x < 1) → Screens 1 2 1 μ → ¬ Exchange μ) ∧
    ((1 - (3 - Real.sqrt 5) / 2) ^ 2 = (3 - Real.sqrt 5) / 2 ∧ (3 - Real.sqrt 5) / 2 ≠ 1 / 2) ∧
    (∀ μ : ℝ → ℝ, (∀ x, 0 < x → μ x = x / Real.sqrt (1 + x ^ 2)) → ¬ Exchange μ) ∧
    (∀ μ : ℝ → ℝ, (∀ x, 0 < x → μ x = 1 - Real.exp (-x)) → ¬ Exchange μ) := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  refine ⟨fun μ hr hs hX => ?_, ⟨by nlinarith, fun h => ?_⟩, fun μ hμ hX => ?_, fun μ hμ hX => ?_⟩
  · have := ((theorem1 1 2 1 one_pos μ hr hs).1).1 hX
    norm_num at this
  · have : Real.sqrt 5 = 2 := by linarith
    nlinarith
  · have h1 := exchange_half μ hX
    rw [hμ 1 one_pos] at h1
    norm_num at h1
    have : Real.sqrt 2 = 2 := by
      have hs : 0 < Real.sqrt 2 := Real.sqrt_pos.2 (by norm_num)
      field_simp at h1; linarith
    nlinarith [Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num)]
  · have h1 := exchange_half μ hX
    rw [hμ 1 one_pos] at h1
    have he : Real.exp (-1) = 1 / 2 := by linarith
    have : Real.exp 1 = 2 := by
      rw [Real.exp_neg, inv_eq_iff_eq_inv] at he; rw [he]; norm_num
    linarith [Real.add_one_lt_exp (one_ne_zero : (1 : ℝ) ≠ 0)]

/-! ## Proposition 2: one node between the teams, and the cap -/

/-- **Proposition 2.** (i) A single Field Origin node between the teams, in balance
`c_A (V_A − V_O) + c_B (V_B − V_O) = 0`, sits at their strength-weighted average, and eliminating it
leaves the series link `c_A c_B/(c_A + c_B)`. (ii) Each team carries `μ` times its own strength:
`g = μ g + μ a₀`, TetB carries `(1 − μ) g = μ a₀ < a₀`, rising with `g`; missing over visible is
`a₀/g`. (iii) A dilation-covariant swap of pulls is `g ↦ c/g`, and its one fixed pull is `√c`. -/
theorem prop2 :
    (∀ cA cB VA VB VO : ℝ, 0 < cA + cB →
      (cA * (VA - VO) + cB * (VB - VO) = 0 ↔ VO = (cA * VA + cB * VB) / (cA + cB))) ∧
    (∀ cA cB : ℝ, 0 < cA + cB → cA - cA * cA / (cA + cB) = cA * cB / (cA + cB)) ∧
    (∀ g a0 : ℝ, 0 < g → 0 < a0 →
      let μ := g / (g + a0)
      g = μ * g + μ * a0 ∧ (1 - μ) * g = μ * a0 ∧ (1 - μ) * g < a0 ∧ (1 - μ) / μ = a0 / g) ∧
    (∀ a0 : ℝ, 0 < a0 → StrictMonoOn (fun g => g * a0 / (g + a0)) (Set.Ioi 0)) ∧
    (∀ E : ℝ → ℝ, (∀ l g, 0 < l → 0 < g → E (l * g) = E g / l) →
      (∀ g, 0 < g → E g = E 1 / g) ∧ (0 < E 1 → ∀ g, 0 < g → (E g = g ↔ g = Real.sqrt (E 1)))) := by
  refine ⟨fun cA cB VA VB VO h => ?_, fun cA cB h => ?_, fun g a0 hg ha => ?_, fun a0 ha => ?_,
    fun E hE => ?_⟩
  · rw [eq_div_iff h.ne']
    constructor <;> intro h' <;> linarith
  · field_simp; ring
  · intro μ
    have hs : 0 < g + a0 := by linarith
    refine ⟨?_, ?_, ?_, ?_⟩
    · simp only [μ]; field_simp
    · simp only [μ]; field_simp; ring
    · simp only [μ]; rw [show (1 - g / (g + a0)) * g = a0 * (g / (g + a0)) by field_simp; ring]
      have : g / (g + a0) < 1 := (div_lt_one hs).2 (by linarith)
      nlinarith
    · simp only [μ]; field_simp; ring
  · intro g₁ h₁ g₂ h₂ h
    simp only [Set.mem_Ioi] at h₁ h₂
    simp only
    rw [div_lt_div_iff₀ (by linarith) (by linarith)]
    nlinarith [mul_pos (mul_pos ha ha) (sub_pos.2 h)]
  · have hinv : ∀ g, 0 < g → E g = E 1 / g := fun g hg => by
      have := hE g 1 hg one_pos; rw [mul_one] at this; exact this
    refine ⟨hinv, fun h1 g hg => ?_⟩
    rw [hinv g hg, div_eq_iff hg.ne']
    constructor
    · intro h; rw [eq_comm, ← Real.sqrt_sq hg.le]; congr 1; rw [h]; ring
    · intro h; rw [h, ← sq, Real.sq_sqrt h1.le]

/-! ## Theorem 3: decoding mass, quiet, drive and brake -/

/-- TetB's measured strength: the `a₀` that would make the measured share the quiet one. -/
noncomputable def strength (g gbar : ℝ) : ℝ := g * (g - gbar) / gbar

/-- The decoded over the photometric mass, `μ(g/a₀) g / g_bar`. -/
noncomputable def ratio (g gbar a0 : ℝ) : ℝ := ConstitutiveLaw.law (g / a0) * g / gbar

/-- **Theorem 3.** At a radius with total pull `g`, visible pull `g_bar` and TetB's measured strength
`w`: `M_dec/M_phot = (g + w)/(g + a₀)` and `ΔM/M_phot = (w − a₀)/(g + a₀)`. The decode is **quiet**
(`= 1`) exactly when `w = a₀`, i.e. when `g_bar = μ g`; it shows **drive** (`> 1`) exactly when
`w > a₀`, i.e. when TetB pulls more than `μ a₀`; and **brake** (`< 1`) exactly when `w < a₀`. -/
theorem decode (g gbar a0 : ℝ) (hg : 0 < g) (hb : 0 < gbar) (ha : 0 < a0) :
    let w := strength g gbar
    let μ := ConstitutiveLaw.law (g / a0)
    ratio g gbar a0 = (g + w) / (g + a0) ∧ ratio g gbar a0 - 1 = (w - a0) / (g + a0) ∧
    (ratio g gbar a0 = 1 ↔ w = a0) ∧ (ratio g gbar a0 = 1 ↔ gbar = μ * g) ∧
    (1 < ratio g gbar a0 ↔ a0 < w) ∧ (1 < ratio g gbar a0 ↔ μ * a0 < g - gbar) ∧
    (ratio g gbar a0 < 1 ↔ w < a0) ∧ (ratio g gbar a0 < 1 ↔ g - gbar < μ * a0) := by
  intro w μ
  have hs : 0 < g + a0 := by linarith
  have hμ : μ = g / (g + a0) := by simp only [μ, ConstitutiveLaw.law]; field_simp
  have hr : ratio g gbar a0 = (g + w) / (g + a0) := by
    simp only [ratio, w, strength, ConstitutiveLaw.law]; field_simp; ring
  have hr1 : ratio g gbar a0 - 1 = (w - a0) / (g + a0) := by rw [hr]; field_simp; ring
  -- TetB's pull against its quiet pull
  have hpull : g - gbar - μ * a0 = gbar / g * (w - a0) * μ := by
    rw [hμ]; simp only [w, strength]; field_simp; ring
  have hpos : 0 < gbar / g * μ := by rw [hμ]; positivity
  have hc : g - gbar - μ * a0 = gbar / g * μ * (w - a0) := by rw [hpull]; ring
  have hq : μ * a0 = (1 - μ) * g := by rw [hμ]; field_simp; ring
  refine ⟨hr, hr1, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · rw [← sub_eq_zero, hr1, div_eq_zero_iff, sub_eq_zero]; simp [hs.ne']
  · rw [← sub_eq_zero, hr1, div_eq_zero_iff, sub_eq_zero]
    simp only [hs.ne', or_false]
    constructor
    · intro h; rw [h, sub_self, mul_zero] at hc; linarith [hq]
    · intro h
      have : gbar / g * μ * (w - a0) = 0 := by rw [← hc, h]; linarith [hq]
      rcases mul_eq_zero.1 this with h' | h'
      · exact absurd h' hpos.ne'
      · linarith
  · rw [← sub_pos, hr1, div_pos_iff_of_pos_right hs, sub_pos]
  · constructor
    · intro h
      have : 0 < w - a0 := by
        have := (show 0 < ratio g gbar a0 - 1 by linarith); rw [hr1] at this
        exact (div_pos_iff_of_pos_right hs).1 this
      nlinarith [mul_pos hpos this]
    · intro h
      have hw : 0 < w - a0 := by
        by_contra hn; push Not at hn
        nlinarith [mul_nonpos_of_nonneg_of_nonpos hpos.le hn]
      have : 0 < ratio g gbar a0 - 1 := by rw [hr1]; exact div_pos hw hs
      linarith
  · rw [← sub_neg, hr1, div_neg_iff]
    constructor
    · rintro (⟨-, h⟩ | ⟨h, -⟩) <;> linarith
    · intro h; right; exact ⟨by linarith, hs⟩
  · constructor
    · intro h
      have : w - a0 < 0 := by
        have := (show ratio g gbar a0 - 1 < 0 by linarith); rw [hr1] at this
        rcases div_neg_iff.1 this with ⟨-, h'⟩ | ⟨h', -⟩
        · linarith
        · exact h'
      nlinarith [mul_neg_of_pos_of_neg hpos this]
    · intro h
      have hw : w - a0 < 0 := by
        by_contra hn; push Not at hn
        nlinarith [mul_nonneg hpos.le hn]
      have : ratio g gbar a0 - 1 < 0 := by rw [hr1]; exact div_neg_of_neg_of_pos hw hs
      linarith

/-- The decode is the decoding-mass letter's `M_dec = r v⁴ / (G (a₀ r + v²))`. -/
theorem letter_decode (G a0 v r : ℝ) (hG : 0 < G) (ha : 0 < a0) (hv : 0 < v) (hr : 0 < r) :
    ConstitutiveLaw.law (v ^ 2 / r / a0) * (v ^ 2 / r) * r ^ 2 / G = r * v ^ 4 / (G * (a0 * r + v ^ 2)) := by
  rw [ConstitutiveLaw.law]; field_simp; ring

/-! ## Proposition 3: the vortex -/

/-- The Burgers vorticity profile `ω(r) = exp(−β r²)` and its first two derivatives. -/
noncomputable def om (β r : ℝ) : ℝ := Real.exp (-β * r ^ 2)
noncomputable def om1 (β r : ℝ) : ℝ := -2 * β * r * Real.exp (-β * r ^ 2)
noncomputable def om2 (β r : ℝ) : ℝ := (-2 * β + 4 * β ^ 2 * r ^ 2) * Real.exp (-β * r ^ 2)

lemma hasDerivAt_om (β r : ℝ) : HasDerivAt (om β) (om1 β r) r := by
  have h : HasDerivAt (fun r => -β * r ^ 2) (-β * (2 * r)) r := by
    simpa using (hasDerivAt_pow 2 r).const_mul (-β)
  show HasDerivAt (fun r => Real.exp (-β * r ^ 2)) (-2 * β * r * Real.exp (-β * r ^ 2)) r
  convert h.exp using 1
  ring

lemma hasDerivAt_om1 (β r : ℝ) : HasDerivAt (om1 β) (om2 β r) r := by
  have hl : HasDerivAt (fun r => -2 * β * r) (-2 * β) r := by
    simpa using (hasDerivAt_id r).const_mul (-2 * β)
  have h := hl.mul (hasDerivAt_om β r)
  convert h using 1
  · funext r; simp only [om1, om, Pi.mul_apply]
  · simp only [om2, om1, om]; ring

/-- **Proposition 3 (i), the Burgers vortex.** With inflow `u_r = −α r/2`, axial outflow `α z` and
`β = α/(4ν)`, the vorticity `ω = exp(−β r²)` is steady: inward advection balances stretching and
diffusion exactly, `u_r ω' = α ω + ν (ω'' + ω'/r)`. -/
theorem burgers (α ν r : ℝ) (hν : 0 < ν) (hr : r ≠ 0) :
    HasDerivAt (om (α / (4 * ν))) (om1 (α / (4 * ν)) r) r ∧
    HasDerivAt (om1 (α / (4 * ν))) (om2 (α / (4 * ν)) r) r ∧
    (-α * r / 2) * om1 (α / (4 * ν)) r =
      α * om (α / (4 * ν)) r + ν * (om2 (α / (4 * ν)) r + om1 (α / (4 * ν)) r / r) := by
  refine ⟨hasDerivAt_om _ r, hasDerivAt_om1 _ r, ?_⟩
  simp only [om, om1, om2]
  field_simp
  ring

/-- The Lamb–Oseen vorticity `(Γ/(4πν t)) exp(−r²/(4ν t))`, and its derivatives in `t` and `r`. -/
noncomputable def lo (Γ ν r t : ℝ) : ℝ := Γ / (4 * Real.pi * ν * t) * Real.exp (-r ^ 2 / (4 * ν * t))

/-- **Proposition 3 (ii), the Lamb–Oseen vortex.** With no drain the same circulation diffuses:
`∂_t ω = ν (∂²_r ω + ∂_r ω / r)`, with the three derivatives given explicitly. -/
theorem lamb_oseen (Γ ν r t : ℝ) (hν : 0 < ν) (ht : 0 < t) (hr : r ≠ 0) :
    let β := 1 / (4 * ν * t)
    let A := Γ / (4 * Real.pi * ν * t)
    HasDerivAt (fun t => lo Γ ν r t)
      (Γ / (4 * Real.pi * ν) * Real.exp (-r ^ 2 / (4 * ν * t)) * (r ^ 2 / (4 * ν * t ^ 3) - 1 / t ^ 2)) t ∧
    (∀ s, lo Γ ν s t = A * om β s) ∧
    Γ / (4 * Real.pi * ν) * Real.exp (-r ^ 2 / (4 * ν * t)) * (r ^ 2 / (4 * ν * t ^ 3) - 1 / t ^ 2) =
      ν * (A * om2 β r + A * om1 β r / r) := by
  intro β A
  have hπ : 0 < Real.pi := Real.pi_pos
  refine ⟨?_, fun s => ?_, ?_⟩
  · have h1 : HasDerivAt (fun t : ℝ => Γ / (4 * Real.pi * ν) * t⁻¹) (Γ / (4 * Real.pi * ν) * -(t ^ 2)⁻¹) t :=
      (hasDerivAt_inv ht.ne').const_mul _
    have h2 : HasDerivAt (fun t : ℝ => -r ^ 2 / (4 * ν) * t⁻¹) (-r ^ 2 / (4 * ν) * -(t ^ 2)⁻¹) t :=
      (hasDerivAt_inv ht.ne').const_mul _
    have h := h1.mul h2.exp
    convert h using 1
    · funext t; simp only [lo]
      by_cases h0 : t = 0
      · subst h0; simp
      · congr 1
        · field_simp
        · congr 1; field_simp
    · rw [show -r ^ 2 / (4 * ν) * t⁻¹ = -r ^ 2 / (4 * ν * t) by field_simp]
      field_simp; ring
  · simp only [lo, A, om, β]; congr 2; field_simp
  · simp only [A, om1, om2, β]
    rw [show -(1 / (4 * ν * t)) * r ^ 2 = -r ^ 2 / (4 * ν * t) by field_simp]
    field_simp
    ring

end TugOfWar

/-! ## Axiom audit -/

#print axioms TugOfWar.lemma1
#print axioms TugOfWar.cube_tug_of_war
#print axioms TugOfWar.theorem1
#print axioms TugOfWar.strengths_are_accelerations
#print axioms TugOfWar.deep_field
#print axioms TugOfWar.muk_one
#print axioms TugOfWar.necessity
#print axioms TugOfWar.prop2
#print axioms TugOfWar.decode
#print axioms TugOfWar.letter_decode
#print axioms TugOfWar.burgers
#print axioms TugOfWar.lamb_oseen
