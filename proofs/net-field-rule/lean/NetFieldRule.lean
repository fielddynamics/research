import TugOfWar
import ConstitutiveLaw
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.LinearAlgebra.Basis.Defs

/-!
# The Net-Field Rule: Where the Constitutive Law Acts

The algebra of the net-field rule of Gravity Field Dynamics. The constitutive law
`μ(x) = x/(x+1)` acts only on a field that has a drain (a galaxy's). A drainless field
(a star system, a binary, a star cluster) is TetA alone, Newton/GR with the bare `G`, and its
host reaches it only through free fall and the tide.

* `drained`, `gN`: the drained law `g_t = F(g_N)` and its inverse `g_N = g_t²/(g_t + a₀)`.
* `four_faces`: the four equivalent faces of "drainless" (linear, identity response, conserved
  flux, no TetB share) all vanish together, exactly at `μ = 1`; `dictionary` gives each as a
  function of `μ` alone.
* `subadditive`, `response_not_identity`: the drained law is never linear and never leaves a
  guest's `G` bare.
* `flux_exponent`, `involution`, `involution_singles_out`: the flux exponent is
  `s = 2(1 − μ)/(2 − μ)`, an involution of `μ`, which fails for the standard law.
* `tail_bounds`, `tail_forced`: a drain around every star leaves a pull between `μa₀` and `a₀`
  at every planet, and exchange symmetry plus the deep field force that tail for every law.
* `free_fall`, `com_free_fall`, `no_self_force`: the host's uniform field drops out; a sheet's
  own pointer cannot push it, for any host response.
* `sheet_vanishes_outside`, `sheet_continuous`: the rubber sheet's own term vanishes outside its
  edge (the shell theorem), so nothing is counted twice.
* `kepler_absorbs`: a host factor on `G` is invisible to orbits.
* `flat_tide`, `jacobi`: the tide of a flat rotation curve and the Jacobi edge.
* `sun_screening`: the Sun's TetB, screened, enclosed and bounded.

Numbers and data (Cassini, globular clusters, dwarfs, wide binaries, SPARC) are checked by the
script `verify_net_field_rule.py`.
-/

open Real Filter Topology

namespace NetFieldRule

/-- The drained law: the total pull `g_t` from the Newtonian pull `g`, `μ(g_t/a₀) g_t = g`. -/
noncomputable def drained (a g : ℝ) : ℝ := (g + √(g ^ 2 + 4 * g * a)) / 2

/-- The inverse of the drained law: `g_N = g_t²/(g_t + a₀) = μ(g_t/a₀) g_t`. -/
noncomputable def gN (a t : ℝ) : ℝ := t ^ 2 / (t + a)

/-- The share of the field carried by TetA, from the imported law. -/
noncomputable abbrev mu := ConstitutiveLaw.law

lemma sqrt_disc (a g : ℝ) (ha : 0 < a) (hg : 0 < g) :
    g < √(g ^ 2 + 4 * g * a) ∧ √(g ^ 2 + 4 * g * a) < g + 2 * a := by
  constructor
  · rw [show g = √(g ^ 2) from (Real.sqrt_sq hg.le).symm]
    rw [Real.sqrt_sq hg.le]
    exact Real.lt_sqrt_of_sq_lt (by nlinarith)
  · rw [Real.sqrt_lt' (by linarith)]
    nlinarith

/-- The drained law is the inverse of `g_N`, and `μ g_t = g`. -/
theorem drained_inverts (a g : ℝ) (ha : 0 < a) (hg : 0 < g) :
    gN a (drained a g) = g ∧ mu (drained a g / a) * drained a g = g := by
  have hs := Real.sq_sqrt (show 0 ≤ g ^ 2 + 4 * g * a by positivity)
  have ht : 0 < drained a g := by
    unfold drained; have := (sqrt_disc a g ha hg).1; linarith
  set s := √(g ^ 2 + 4 * g * a) with hsdef
  have key : drained a g ^ 2 = g * (drained a g + a) := by
    unfold drained; rw [← hsdef]; nlinarith [hs]
  refine ⟨?_, ?_⟩
  · unfold gN; rw [key]; field_simp
  · unfold mu ConstitutiveLaw.law
    rw [div_add_one ha.ne', div_div_div_cancel_right₀ ha.ne']
    rw [div_mul_eq_mul_div, ← sq, key]; field_simp

-- ============================================================================================
-- The dictionary and the four faces
-- ============================================================================================

/-- Every quantity of the rule is a rational function of `μ`. With `x > 0` and `m = μ(x)`:
`x = m/(1 − m)`; `y = x μ(x)` has `ν(y) = 1/2 + √(1/4 + 1/y) = 1/m` (the transverse response);
the parallel response `dg_t/dg_N` is `1/(m(2 − m))`; the log-degree of the law is `1/(2 − m)`. -/
theorem dictionary (x a : ℝ) (hx : 0 < x) (ha : 0 < a) :
    let m := mu x
    x = m / (1 - m) ∧
    1 / 2 + √(1 / 4 + 1 / (x * m)) = 1 / m ∧
    1 / ((x * a) ^ 2 + 2 * (x * a) * a) * (x * a + a) ^ 2 = 1 / (m * (2 - m)) ∧
    gN a (x * a) / ((x * a) * ((x * a) ^ 2 + 2 * (x * a) * a) / (x * a + a) ^ 2) = 1 / (2 - m) := by
  intro m
  have hx1 : x + 1 ≠ 0 := by positivity
  have hx2 : x + 2 ≠ 0 := by positivity
  have hx2' : 2 + x ≠ 0 := by positivity
  have hm : m = x / (x + 1) := rfl
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [hm]; field_simp; ring
  · have h : 1 / 4 + 1 / (x * m) = ((x + 2) / (2 * x)) ^ 2 := by
      rw [hm]; field_simp; ring
    rw [h, Real.sqrt_sq (by positivity), hm]; field_simp; ring
  · rw [hm]
    have e : 2 - x / (x + 1) = (x + 2) / (x + 1) := by field_simp; ring
    rw [e]; field_simp
  · unfold gN; rw [hm]
    have e : 2 - x / (x + 1) = (x + 2) / (x + 1) := by field_simp; ring
    rw [e]; field_simp

/-- The four faces of a drainless field vanish together, exactly at `μ = 1`: the law's degree
defect, the guest's response defect, the flux growth and the TetB share. -/
theorem four_faces (m : ℝ) (h0 : 0 < m) (h1 : m ≤ 1) :
    (1 - 1 / (2 - m) = 0 ↔ m = 1) ∧ (1 / m - 1 = 0 ↔ m = 1) ∧
    (2 * (1 - m) / (2 - m) = 0 ↔ m = 1) ∧ (1 - m = 0 ↔ m = 1) := by
  have h2 : (2 - m) ≠ 0 := by linarith
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [sub_eq_zero, eq_comm, div_eq_one_iff_eq h2]; constructor <;> intro h <;> linarith
  · rw [sub_eq_zero, div_eq_one_iff_eq h0.ne']; exact eq_comm
  · rw [div_eq_zero_iff]; constructor
    · rintro (h | h) <;> [linarith; exact absurd h h2]
    · intro h; left; rw [h]; ring
  · rw [sub_eq_zero, eq_comm]

/-- A drained field is never linear: two sources together pull less than the sum of each alone. -/
theorem subadditive (a b c : ℝ) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    drained a (b + c) < drained a b + drained a c := by
  unfold drained
  have hB := (sqrt_disc a b ha hb).1
  have hC := (sqrt_disc a c ha hc).1
  have key : √((b + c) ^ 2 + 4 * (b + c) * a) < √(b ^ 2 + 4 * b * a) + √(c ^ 2 + 4 * c * a) := by
    rw [Real.sqrt_lt' (by positivity)]
    have e1 := Real.sq_sqrt (show 0 ≤ b ^ 2 + 4 * b * a by positivity)
    have e2 := Real.sq_sqrt (show 0 ≤ c ^ 2 + 4 * c * a by positivity)
    nlinarith [mul_lt_mul'' hB hC hb.le hc.le]
  linarith

/-- A drained host never leaves a guest's `G` bare: at any finite field both responses exceed 1. -/
theorem response_not_identity (x : ℝ) (hx : 0 < x) :
    1 < 1 / mu x ∧ 1 < 1 / (mu x * (2 - mu x)) := by
  have hm0 : 0 < mu x := by unfold mu ConstitutiveLaw.law; positivity
  have hm1 : mu x < 1 := by
    unfold mu ConstitutiveLaw.law; rw [div_lt_one (by positivity)]; linarith
  constructor
  · rw [lt_div_iff₀ hm0]; linarith
  · rw [lt_div_iff₀ (by nlinarith)]; nlinarith

-- ============================================================================================
-- Flux: the drain as growth of flux across empty shells
-- ============================================================================================

/-- The derivative of the inverse law, and its log-degree `2 − μ`. -/
theorem gN_deriv (a t : ℝ) (ha : 0 < a) (ht : 0 < t) :
    HasDerivAt (gN a) ((t ^ 2 + 2 * t * a) / (t + a) ^ 2) t ∧
    t * ((t ^ 2 + 2 * t * a) / (t + a) ^ 2) / gN a t = 2 - mu (t / a) := by
  have hta : t + a ≠ 0 := by positivity
  constructor
  · have h := (hasDerivAt_pow 2 t).div ((hasDerivAt_id' t).add_const a) hta
    convert h using 1
    · funext s; simp [gN, Pi.div_apply]
    · field_simp; ring
  · unfold gN mu ConstitutiveLaw.law
    rw [div_add_one ha.ne', div_div_div_cancel_right₀ ha.ne']
    field_simp; ring

/-- The flux exponent `s = d ln(r² g_t)/d ln r` of a point mass is `2 − 2/(2 − μ)`, which is
`2(1 − μ)/(2 − μ)`: zero exactly without TetB share, one in the deep field. -/
theorem flux_exponent (m : ℝ) (hm : m < 2) :
    2 - 2 / (2 - m) = 2 * (1 - m) / (2 - m) ∧ (2 - 2 / (2 - m)) - 1 = -m / (2 - m) := by
  have h2 : (2 - m) ≠ 0 := by linarith
  constructor <;> field_simp <;> ring

/-- The map `f(u) = 2(1 − u)/(2 − u)` that sends `μ` to the flux exponent is an involution. -/
theorem involution (u : ℝ) (hu : u ≠ 2) :
    let f := fun w : ℝ => 2 * (1 - w) / (2 - w)
    f (f u) = u := by
  intro f
  have h2 : (2 - u) ≠ 0 := sub_ne_zero.mpr (Ne.symm hu)
  simp only [f]
  have h3 : 2 - 2 * (1 - u) / (2 - u) = 2 / (2 - u) := by field_simp; ring
  rw [h3]; field_simp; ring

/-- The involution singles out GFD's law: for the standard law (`n = 2`) the map
`u ↦ 2(1 − u²)/(2 − u²)` is not an involution. -/
theorem involution_singles_out :
    let f2 := fun w : ℝ => 2 * (1 - w ^ 2) / (2 - w ^ 2)
    f2 (f2 (3 / 10)) ≠ 3 / 10 := by
  intro f2; simp only [f2]; norm_num

-- ============================================================================================
-- A drain around every star is forced to fail
-- ============================================================================================

/-- Around a star under a drained field, the extra pull lies between `μ a₀` and `a₀`:
`a₀ g/(g + a₀) ≤ g_t − g < a₀`. It is a constant pull of nearly `a₀` at every planet. -/
theorem tail_bounds (a g : ℝ) (ha : 0 < a) (hg : 0 < g) :
    a * g / (g + a) ≤ drained a g - g ∧ drained a g - g < a := by
  obtain ⟨h1, h2⟩ := sqrt_disc a g ha hg
  have hs := Real.sq_sqrt (show 0 ≤ g ^ 2 + 4 * g * a by positivity)
  unfold drained
  constructor
  · rw [div_le_iff₀ (by positivity)]
    nlinarith
  · linarith

/-- Exchange symmetry plus the deep-field limit force the tail for every law:
`x(1 − μ(x)) = μ(1/x)/(1/x) → 1` as `x → ∞`. -/
theorem tail_forced (μ : ℝ → ℝ) (hX : TugOfWar.Exchange μ)
    (hdeep : Tendsto (fun u => μ u / u) (𝓝[>] 0) (𝓝 1)) :
    Tendsto (fun x => x * (1 - μ x)) atTop (𝓝 1) := by
  have h := hdeep.comp tendsto_inv_atTop_nhdsGT_zero
  refine h.congr' ?_
  filter_upwards [eventually_gt_atTop 0] with x hx
  simp only [Function.comp, div_inv_eq_mul]
  rw [hX x hx]; ring

-- ============================================================================================
-- The rubber sheet
-- ============================================================================================

/-- Free fall: a uniform host field `g_e` drops out of every relative acceleration. -/
theorem free_fall {V : Type*} [AddCommGroup V] (ai aj ge : V) :
    (aj + ge) - (ai + ge) = aj - ai := by abel

section Sheet
variable {V : Type*} [AddCommGroup V] [Module ℝ V]

/-- With pairwise antisymmetric internal forces, the centre of mass falls with the host:
`∑ mᵢ aᵢ = (∑ mᵢ) g_e`. -/
theorem com_free_fall {n : ℕ} (m : Fin n → ℝ) (a : Fin n → V) (F : Fin n → Fin n → V) (ge : V)
    (hF : ∀ i j, F i j = -F j i) (ha : ∀ i, m i • a i = (∑ j, F i j) + m i • ge) :
    ∑ i, m i • a i = (∑ i, m i) • ge := by
  have hS : ∑ i, ∑ j, F i j = 0 := by
    have h1 : ∑ i, ∑ j, F i j = -∑ i, ∑ j, F i j := by
      conv_lhs => rw [Finset.sum_comm]
      rw [← Finset.sum_neg_distrib]
      refine Finset.sum_congr rfl (fun y _ => ?_)
      rw [← Finset.sum_neg_distrib]
      exact Finset.sum_congr rfl (fun x _ => hF x y)
    have h2 : (2 : ℝ) • ∑ i, ∑ j, F i j = 0 := by
      rw [two_smul]; nth_rewrite 2 [h1]; abel
    exact (smul_eq_zero.mp h2).resolve_left two_ne_zero
  rw [Finset.sum_congr rfl (fun i _ => ha i), Finset.sum_add_distrib, hS, zero_add,
    Finset.sum_smul]

/-- No self-force: the sheet's own smoothed ball, a field `k (p − c)` linear about the centre of
mass `c`, passed through any linear host response `R`, exerts zero net force on the sheet. -/
theorem no_self_force {n : ℕ} (m : Fin n → ℝ) (p : Fin n → V) (c : V) (k : ℝ) (R : V →ₗ[ℝ] V)
    (hc : (∑ i, m i) • c = ∑ i, m i • p i) :
    ∑ i, m i • R (k • (p i - c)) = 0 := by
  have h0 : ∑ i, m i • (p i - c) = 0 := by
    simp_rw [smul_sub, Finset.sum_sub_distrib, ← Finset.sum_smul, hc, sub_self]
  calc ∑ i, m i • R (k • (p i - c)) = R (k • ∑ i, m i • (p i - c)) := by
        rw [Finset.smul_sum, map_sum]
        refine Finset.sum_congr rfl (fun i _ => ?_)
        rw [map_smul, map_smul, map_smul, smul_comm]
    _ = 0 := by rw [h0, smul_zero, map_zero]

end Sheet

/-- The field of a uniform ball of mass `M` and radius `l` (the pointer). -/
noncomputable def tophat (G M l r : ℝ) : ℝ := if r < l then G * M * r / l ^ 3 else G * M / r ^ 2

/-- The sheet's own term, the ball's field minus its pointer, vanishes outside the sheet's edge:
nothing is counted twice, and the host sees the sheet as one mass. -/
theorem sheet_vanishes_outside (G M l r : ℝ) (hr : l ≤ r) : G * M / r ^ 2 - tophat G M l r = 0 := by
  unfold tophat
  split_ifs with h
  · exact absurd h (not_lt.mpr hr)
  · ring

/-- The sheet's own term is continuous at the edge, and inside it is the ball minus a harmonic
term: `G M/r² − G M r/l³`. -/
theorem sheet_continuous (G M l : ℝ) (hl : 0 < l) :
    G * M / l ^ 2 - G * M * l / l ^ 3 = 0 ∧
    ∀ r, r < l → G * M / r ^ 2 - tophat G M l r = G * M / r ^ 2 - G * M * r / l ^ 3 := by
  refine ⟨by field_simp; ring, fun r hr => ?_⟩
  unfold tophat; simp [hr]

/-- A host factor on `G` is invisible to orbits: Kepler's period depends only on `G M`. -/
theorem kepler_absorbs (G M μ a : ℝ) :
    4 * π ^ 2 * a ^ 3 / ((G / μ) * M) = 4 * π ^ 2 * a ^ 3 / (G * (M / μ)) := by
  rw [div_mul_eq_mul_div, mul_div_assoc']

/-- The tide of a flat rotation curve, `Φ = v² ln R`: `Φ' = v²/R`, `Φ'' = −v²/R²`. -/
theorem flat_tide (v R : ℝ) (hR : 0 < R) :
    HasDerivAt (fun R => v ^ 2 * Real.log R) (v ^ 2 / R) R ∧
    HasDerivAt (fun R => v ^ 2 / R) (-(v ^ 2 / R ^ 2)) R := by
  constructor
  · have := (Real.hasDerivAt_log hR.ne').const_mul (v ^ 2)
    convert this using 1; field_simp
  · have := (hasDerivAt_inv hR.ne').const_mul (v ^ 2)
    convert this using 1
    · ext; simp [div_eq_mul_inv]
    · field_simp

/-- The Jacobi edge in a flat rotation curve: `κ² = R dΩ²/dR + 4Ω² = 2Ω²` for `Ω = v/R`, and at
`r_J³ = G M/(2Ω²)` the sheet's harmonic term is the tide's size, `G M/r_J³ = 2Ω²`. -/
theorem jacobi (v R GM rJ3 : ℝ) (hR : 0 < R) (hv : 0 < v) (hGM : 0 < GM)
    (hJ : rJ3 = GM / (2 * (v / R) ^ 2)) :
    HasDerivAt (fun R => (v / R) ^ 2) (-2 * v ^ 2 / R ^ 3) R ∧
    R * (-2 * v ^ 2 / R ^ 3) + 4 * (v / R) ^ 2 = 2 * (v / R) ^ 2 ∧
    GM / rJ3 = 2 * (v / R) ^ 2 := by
  refine ⟨?_, by field_simp; ring, ?_⟩
  · have h := ((hasDerivAt_pow 2 R).inv (by positivity)).const_mul (v ^ 2)
    convert h using 1
    · ext s; rw [div_pow, div_eq_mul_inv]; rfl
    · field_simp; ring
  · rw [hJ]; field_simp

-- ============================================================================================
-- The Sun's TetB: screened, enclosed and bounded
-- ============================================================================================

/-- The screening law is the TetA share: `x(1 − μ) = μ` and `1 − μ = 1/(1 + x)`. In a uniform
core the pull is `(4π/3) G ρ r`, and TetB dominates only inside `r_B = 3a₀/(4π G ρ)`. Read
pointwise, the screened TetB's extra flux at the surface is below `a₀ R²/G`. -/
theorem sun_screening (x G ρ a gs R : ℝ) (hx : 0 < x) (hG : 0 < G) (hρ : 0 < ρ) (ha : 0 < a)
    (hgs : 0 < gs) (hR : 0 < R) :
    x * (1 - mu x) = mu x ∧ 1 - mu x = 1 / (1 + x) ∧
    (4 / 3 * π * G * ρ * (3 * a / (4 * π * G * ρ)) = a) ∧
    (drained a gs - gs) * R ^ 2 / G < a * R ^ 2 / G := by
  have hx1 : x + 1 ≠ 0 := by positivity
  refine ⟨?_, ?_, ?_, ?_⟩
  · unfold mu ConstitutiveLaw.law; field_simp; ring
  · unfold mu ConstitutiveLaw.law; field_simp; ring
  · field_simp
  · have := (tail_bounds a gs ha hgs).2
    apply div_lt_div_of_pos_right _ hG
    exact mul_lt_mul_of_pos_right this (by positivity)

end NetFieldRule

#print axioms NetFieldRule.drained_inverts
#print axioms NetFieldRule.dictionary
#print axioms NetFieldRule.four_faces
#print axioms NetFieldRule.subadditive
#print axioms NetFieldRule.response_not_identity
#print axioms NetFieldRule.gN_deriv
#print axioms NetFieldRule.flux_exponent
#print axioms NetFieldRule.involution
#print axioms NetFieldRule.involution_singles_out
#print axioms NetFieldRule.tail_bounds
#print axioms NetFieldRule.tail_forced
#print axioms NetFieldRule.free_fall
#print axioms NetFieldRule.com_free_fall
#print axioms NetFieldRule.no_self_force
#print axioms NetFieldRule.sheet_vanishes_outside
#print axioms NetFieldRule.sheet_continuous
#print axioms NetFieldRule.kepler_absorbs
#print axioms NetFieldRule.flat_tide
#print axioms NetFieldRule.jacobi
#print axioms NetFieldRule.sun_screening
