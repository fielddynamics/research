import ForcedTetrahedralFrame
import Mathlib.Analysis.Convex.Basic
import Mathlib.Analysis.Normed.Group.Bounded
import Mathlib.Analysis.Normed.Group.Constructions
import Mathlib.Analysis.Normed.Group.Real

/-!
# Lean 4 / Mathlib formalisation of
#   S. Nelson, "The Sixteen Half-Space Regions of the Tetrad Frame"
#   (Route 1 of Letter 1, "The Coordinate-Space Geometry of the Tetrad Frame")

Builds on `ForcedTetrahedralFrame`: the four normals are the columns of its matrix `M`
(`Mcol`), the forced tetrahedral frame.

## How to referee this file
A Lean proof can only be wrong in its *statements*. Check these definitions against the paper:
* `proj a p = n_a · p` with `n_a = Mcol a`; `proj_formulas` shows these are the paper's
  `v₁ = x+y+z`, `v₂ = x−y−z`, `v₃ = −x+y−z`, `v₄ = −x−y+z`.
* `region s = {p | ∀ a, σ_a v_a(p) ≤ 1}` with `σ_a = +1` if `s a = true`, `−1` if `false`:
  one half-space per projection, `2⁴ = 16` selections.
* `TetA = region (all true) = {max v_a ≤ 1}`, `TetB = region (all false) = {max (−v_a) ≤ 1}`.
* *Bounded* is Mathlib's `Bornology.IsBounded` (for the sup norm on `ℝ³`, equivalently any norm).
* `face a`, `core a`, `corner a b`, `channel a b`: the faces of TetA and their four pieces.

Headline results: `proj_sum`, `proj_relations` (the sole relation), `classification`
(bounded iff all signs agree), `exactly_two_bounded`, `TetA_eq_hull`, `TetB_eq_hull`,
`inter_eq_octahedron`, `octahedron_regular`, `inter_eq_hull_octVert`, `interpenetration`, `channels`, `inventory`,
`three_plus_one`.
-/

open Matrix Finset Bornology

namespace HalfSpaceTwoBoundedRegions

open ForcedTetrahedralFrame (Mcol Mmat MtM_apply)

/-- The projection `v_a(p) = n_a · p` along the `a`-th tetrahedral direction. -/
def proj (a : Fin 4) (p : Fin 3 → ℝ) : ℝ := Mcol a ⬝ᵥ p

lemma proj_formulas (p : Fin 3 → ℝ) :
    proj 0 p = p 0 + p 1 + p 2 ∧ proj 1 p = p 0 - p 1 - p 2 ∧
      proj 2 p = -p 0 + p 1 - p 2 ∧ proj 3 p = -p 0 - p 1 + p 2 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [proj, Mcol, Mmat, dotProduct, Fin.sum_univ_three] <;> ring

lemma proj_add (a : Fin 4) (x y : Fin 3 → ℝ) : proj a (x + y) = proj a x + proj a y := by
  simp [proj, dotProduct_add]

lemma proj_smul (a : Fin 4) (t : ℝ) (x : Fin 3 → ℝ) : proj a (t • x) = t * proj a x := by
  simp [proj, dotProduct_smul]

lemma proj_neg (a : Fin 4) (x : Fin 3 → ℝ) : proj a (-x) = -proj a x := by
  simp [proj, dotProduct_neg]

/-- `n_b · n_a`: `3` on the diagonal, `−1` off it. -/
lemma proj_Mcol (a b : Fin 4) : proj b (Mcol a) = if b = a then 3 else -1 := by
  rw [← MtM_apply, Matrix.mul_apply]; simp [proj, Mcol, dotProduct]

/-- **The linear relation** `v₁ + v₂ + v₃ + v₄ = 0`, at every point. -/
theorem proj_sum (p : Fin 3 → ℝ) : ∑ a, proj a p = 0 := by
  obtain ⟨h0, h1, h2, h3⟩ := proj_formulas p
  rw [Fin.sum_univ_four, h0, h1, h2, h3]; ring

/-- **The sole relation.** A linear combination of the four projections vanishes everywhere iff
all its coefficients are equal. -/
theorem proj_relations (l : Fin 4 → ℝ) :
    (∀ p, ∑ a, l a * proj a p = 0) ↔ ∀ a b, l a = l b := by
  constructor
  · intro h
    have e : ∀ i : Fin 3, ∑ a, l a * Mcol a i = 0 := by
      intro i
      have := h (Pi.single i 1)
      simpa [proj, dotProduct, Pi.single_apply] using this
    have e0 := e 0; have e1 := e 1; have e2 := e 2
    simp [Fin.sum_univ_four, Mcol, Mmat] at e0 e1 e2
    intro a b
    fin_cases a <;> fin_cases b <;> simp <;> linarith
  · intro h p
    have : ∀ a, l a = l 0 := fun a => h a 0
    simp only [this, ← Finset.mul_sum, proj_sum, mul_zero]

/-- Recovering a point from its projections. -/
lemma coords_of_proj (p : Fin 3 → ℝ) :
    p 0 = (proj 0 p + proj 1 p) / 2 ∧ p 1 = (proj 0 p + proj 2 p) / 2 ∧
      p 2 = (proj 0 p + proj 3 p) / 2 := by
  obtain ⟨h0, h1, h2, h3⟩ := proj_formulas p
  refine ⟨?_, ?_, ?_⟩ <;> rw [h0] <;> [rw [h1]; rw [h2]; rw [h3]] <;> ring

lemma abs_proj_le (a : Fin 4) (p : Fin 3 → ℝ) : |proj a p| ≤ |p 0| + |p 1| + |p 2| := by
  obtain ⟨h0, h1, h2, h3⟩ := proj_formulas p
  have := le_abs_self (p 0); have := le_abs_self (p 1); have := le_abs_self (p 2)
  have := neg_abs_le (p 0); have := neg_abs_le (p 1); have := neg_abs_le (p 2)
  rw [abs_le]
  fin_cases a <;> simp only [Fin.zero_eta, Fin.mk_one, Fin.reduceFinMk, h0, h1, h2, h3] <;>
    constructor <;> linarith

/-! ## The sixteen regions -/

/-- The sign `σ_a`: `+1` keeps `v_a ≤ 1`, `−1` flips it to `−v_a ≤ 1`. -/
def sgn (s : Fin 4 → Bool) (a : Fin 4) : ℝ := if s a then 1 else -1

/-- The region selected by `s`: one half-space per projection. -/
def region (s : Fin 4 → Bool) : Set (Fin 3 → ℝ) := {p | ∀ a, sgn s a * proj a p ≤ 1}

def TetA : Set (Fin 3 → ℝ) := region fun _ => true
def TetB : Set (Fin 3 → ℝ) := region fun _ => false

lemma mem_TetA (p : Fin 3 → ℝ) : p ∈ TetA ↔ ∀ a, proj a p ≤ 1 := by
  simp [TetA, region, sgn]

lemma mem_TetB (p : Fin 3 → ℝ) : p ∈ TetB ↔ ∀ a, -proj a p ≤ 1 := by
  simp [TetB, region, sgn]

lemma sixteen : Fintype.card (Fin 4 → Bool) = 16 := by simp

/-- Bounded by coordinates. -/
lemma isBounded_of_coord {S : Set (Fin 3 → ℝ)} (C : ℝ) (hC : 0 ≤ C)
    (h : ∀ p ∈ S, ∀ i, |p i| ≤ C) : IsBounded S := by
  refine (isBounded_iff_forall_norm_le (s := S)).mpr ⟨C, fun p hp => ?_⟩
  refine (pi_norm_le_iff_of_nonneg hC).mpr fun i => ?_
  rw [Real.norm_eq_abs]; exact h p hp i

lemma coord_of_isBounded {S : Set (Fin 3 → ℝ)} (h : IsBounded S) :
    ∃ C, ∀ p ∈ S, ∀ i, |p i| ≤ C := by
  obtain ⟨C, hC⟩ := (isBounded_iff_forall_norm_le (s := S)).mp h
  exact ⟨C, fun p hp i => by
    have := norm_le_pi_norm p i
    rw [Real.norm_eq_abs] at this
    exact this.trans (hC p hp)⟩

/-- TetA and TetB are bounded: the inward normals close (`Σ v_a = 0`), so each `v_a ≥ −3`. -/
theorem TetA_bounded : IsBounded TetA := by
  refine isBounded_of_coord 3 (by norm_num) fun p hp => ?_
  rw [mem_TetA] at hp
  have hs := proj_sum p
  rw [Fin.sum_univ_four] at hs
  have h0 := hp 0; have h1 := hp 1; have h2 := hp 2; have h3 := hp 3
  obtain ⟨c0, c1, c2⟩ := coords_of_proj p
  intro i; rw [abs_le]
  fin_cases i <;> simp only [Fin.zero_eta, Fin.mk_one, Fin.reduceFinMk, c0, c1, c2] <;>
    constructor <;> linarith

theorem TetB_bounded : IsBounded TetB := by
  refine isBounded_of_coord 3 (by norm_num) fun p hp => ?_
  rw [mem_TetB] at hp
  have hs := proj_sum p
  rw [Fin.sum_univ_four] at hs
  have h0 := hp 0; have h1 := hp 1; have h2 := hp 2; have h3 := hp 3
  obtain ⟨c0, c1, c2⟩ := coords_of_proj p
  intro i; rw [abs_le]
  fin_cases i <;> simp only [Fin.zero_eta, Fin.mk_one, Fin.reduceFinMk, c0, c1, c2] <;>
    constructor <;> linarith

/-- For a mixed selection with kept set `S`, the direction `d = −Σ_{b∈S} n_b` has
`σ_c v_c(d) ≤ −1` for every `c`, so the ray `t d` stays in the region. -/
lemma mixed_direction (s : Fin 4 → Bool) (hT : ∃ a, s a = true) (hF : ∃ b, s b = false) (c : Fin 4) :
    sgn s c * proj c (-∑ b ∈ Finset.univ.filter (fun b => s b = true), Mcol b) ≤ -1 := by
  set S := Finset.univ.filter (fun b => s b = true) with hS
  have hsum : proj c (∑ b ∈ S, Mcol b) = (if s c = true then 4 else 0) - S.card := by
    have : proj c (∑ b ∈ S, Mcol b) = ∑ b ∈ S, proj c (Mcol b) := by
      simp only [proj, dotProduct_sum]
    rw [this]
    have e : ∀ b, proj c (Mcol b) = -1 + if c = b then 4 else 0 := by
      intro b; rw [proj_Mcol]; split_ifs <;> norm_num
    simp only [e, Finset.sum_add_distrib, Finset.sum_const, nsmul_eq_mul, mul_neg, mul_one,
      Finset.sum_ite_eq, hS, Finset.mem_filter, Finset.mem_univ, true_and]
    split_ifs <;> ring
  obtain ⟨a, ha⟩ := hT; obtain ⟨b, hb⟩ := hF
  have hcard1 : 1 ≤ S.card := Finset.card_pos.mpr ⟨a, by simp [hS, ha]⟩
  have hcard3 : S.card ≤ 3 := by
    have : S ⊆ Finset.univ.erase b := by
      intro x hx; simp only [hS, Finset.mem_filter] at hx
      exact Finset.mem_erase.mpr ⟨fun h => by rw [h, hb] at hx; exact absurd hx.2 (by simp),
        Finset.mem_univ _⟩
    have := Finset.card_le_card this
    simpa using this
  have h1 : (1 : ℝ) ≤ S.card := by exact_mod_cast hcard1
  have h3 : (S.card : ℝ) ≤ 3 := by exact_mod_cast hcard3
  rw [proj_neg, hsum]
  by_cases hc : s c = true
  · have hsg : sgn s c = 1 := by simp [sgn, hc]
    rw [hsg]; simp only [hc, ite_true]; linarith
  · have hsg : sgn s c = -1 := by simp [sgn, hc]
    rw [hsg, ite_eq_right_of_eq_false _ _ (eq_false hc)]; linarith

/-- Every mixed selection is unbounded. -/
theorem mixed_unbounded (s : Fin 4 → Bool) (hT : ∃ a, s a = true) (hF : ∃ b, s b = false) :
    ¬ IsBounded (region s) := by
  intro hB
  obtain ⟨C, hC⟩ := coord_of_isBounded hB
  set d := -∑ b ∈ Finset.univ.filter (fun b => s b = true), Mcol b with hd
  have hmem : ∀ t : ℝ, 0 ≤ t → t • d ∈ region s := by
    intro t ht c
    rw [proj_smul, ← mul_assoc, mul_comm (sgn s c) t, mul_assoc]
    have := mixed_direction s hT hF c
    nlinarith
  obtain ⟨a, ha⟩ := hT
  have hda : sgn s a * proj a d ≤ -1 := mixed_direction s ⟨a, ha⟩ hF a
  have hsa : sgn s a = 1 := by simp [sgn, ha]
  rw [hsa, one_mul] at hda
  set t := 3 * |C| + 1 with ht
  have htpos : 0 ≤ t := by positivity
  have hp := hC _ (hmem t htpos)
  have hb : |proj a (t • d)| ≤ 3 * C := by
    have := abs_proj_le a (t • d)
    linarith [hp 0, hp 1, hp 2]
  rw [proj_smul, abs_mul, abs_of_nonneg htpos] at hb
  have : 1 ≤ |proj a d| := by rw [abs_of_neg (by linarith)]; linarith
  nlinarith [le_abs_self C]

/-- **Classification.** A region is bounded iff all four signs agree: TetA or TetB. -/
theorem classification (s : Fin 4 → Bool) :
    IsBounded (region s) ↔ (∀ a, s a = true) ∨ (∀ a, s a = false) := by
  constructor
  · intro hB
    by_contra hne
    push Not at hne
    obtain ⟨⟨a, ha⟩, ⟨b, hb⟩⟩ := hne
    exact mixed_unbounded s ⟨b, by simpa using hb⟩ ⟨a, by simpa using ha⟩ hB
  · rintro (h | h)
    · have : s = fun _ => true := funext h
      rw [this]; exact TetA_bounded
    · have : s = fun _ => false := funext h
      rw [this]; exact TetB_bounded

open Classical in
/-- **Exactly two of the sixteen regions are bounded**, and they are TetA and TetB. -/
theorem exactly_two_bounded :
    (Finset.univ.filter fun s : Fin 4 → Bool => IsBounded (region s)) =
      ({fun _ => true, fun _ => false} : Finset (Fin 4 → Bool)) ∧
    (Finset.univ.filter fun s : Fin 4 → Bool => IsBounded (region s)).card = 2 := by
  have h : (Finset.univ.filter fun s : Fin 4 → Bool => IsBounded (region s)) =
      ({fun _ => true, fun _ => false} : Finset (Fin 4 → Bool)) := by
    ext s
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, classification, Finset.mem_insert,
      Finset.mem_singleton]
    constructor
    · rintro (h | h)
      · left; exact funext h
      · right; exact funext h
    · rintro (rfl | rfl)
      · left; intro; rfl
      · right; intro; rfl
  refine ⟨h, ?_⟩
  rw [h, Finset.card_pair]
  intro heq
  have := congrFun heq 0
  simp at this

/-! ## TetA and TetB as tetrahedra -/

lemma reconstruct (p : Fin 3 → ℝ) :
    p = ∑ a, ((1 - proj a p) / 4) • (-Mcol a) := by
  obtain ⟨h0, h1, h2, h3⟩ := proj_formulas p
  funext i
  simp only [Finset.sum_apply, Pi.smul_apply, Pi.neg_apply, smul_eq_mul, Fin.sum_univ_four, h0,
    h1, h2, h3]
  fin_cases i <;> simp [Mcol, Mmat] <;> ring

lemma reconstructB (p : Fin 3 → ℝ) :
    p = ∑ a, ((1 + proj a p) / 4) • Mcol a := by
  obtain ⟨h0, h1, h2, h3⟩ := proj_formulas p
  funext i
  simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Fin.sum_univ_four, h0, h1, h2, h3]
  fin_cases i <;> simp [Mcol, Mmat] <;> ring

lemma proj_sum_smul (b : Fin 4) (w : Fin 4 → ℝ) (u : Fin 4 → Fin 3 → ℝ) :
    proj b (∑ a, w a • u a) = ∑ a, w a * proj b (u a) := by
  simp only [proj, dotProduct_sum, dotProduct_smul, smul_eq_mul]

/-- **TetA is the tetrahedron with vertices `−n_a`** (the parity image of the forced frame):
its points are exactly the convex combinations of the four vertices. -/
theorem TetA_eq_hull :
    TetA = {p | ∃ w : Fin 4 → ℝ, (∀ a, 0 ≤ w a) ∧ ∑ a, w a = 1 ∧ p = ∑ a, w a • (-Mcol a)} := by
  ext p
  rw [mem_TetA]
  constructor
  · intro hp
    refine ⟨fun a => (1 - proj a p) / 4, fun a => by linarith [hp a], ?_, reconstruct p⟩
    have hs := proj_sum p
    rw [Fin.sum_univ_four] at hs ⊢; linarith
  · rintro ⟨w, hw, hsum, rfl⟩ b
    rw [proj_sum_smul]
    simp only [proj_neg, proj_Mcol]
    rw [Fin.sum_univ_four] at hsum ⊢
    have := hw 0; have := hw 1; have := hw 2; have := hw 3
    fin_cases b <;> simp <;> linarith

/-- **TetB is the tetrahedron with vertices `n_a`**, the columns of the forced frame `M`. -/
theorem TetB_eq_hull :
    TetB = {p | ∃ w : Fin 4 → ℝ, (∀ a, 0 ≤ w a) ∧ ∑ a, w a = 1 ∧ p = ∑ a, w a • Mcol a} := by
  ext p
  rw [mem_TetB]
  constructor
  · intro hp
    refine ⟨fun a => (1 + proj a p) / 4, fun a => by linarith [hp a], ?_, reconstructB p⟩
    have hs := proj_sum p
    rw [Fin.sum_univ_four] at hs ⊢; linarith
  · rintro ⟨w, hw, hsum, rfl⟩ b
    rw [proj_sum_smul]
    simp only [proj_Mcol]
    rw [Fin.sum_univ_four] at hsum ⊢
    have := hw 0; have := hw 1; have := hw 2; have := hw 3
    fin_cases b <;> simp <;> linarith

/-- TetB is the image of TetA under spatial parity `p → −p`. -/
theorem TetB_eq_neg_TetA : TetB = {p | -p ∈ TetA} := by
  ext p; simp [mem_TetA, mem_TetB, proj_neg]

/-! ## Interpenetration and the octahedral core -/

/-- **Interpenetration.** Each vertex `n_a` of TetB lies beyond exactly one face of TetA, the face
`v_a = 1`, and each vertex `−n_a` of TetA beyond exactly one face of TetB. -/
theorem interpenetration (a b : Fin 4) :
    (1 < proj b (Mcol a) ↔ b = a) ∧ (1 < -proj b (-Mcol a) ↔ b = a) := by
  rw [proj_neg, neg_neg, proj_Mcol]
  by_cases h : b = a <;> simp [h]

/-- **The intersection** `TetA ∩ TetB = {|v_a| ≤ 1 for all a} = {|x| + |y| + |z| ≤ 1}`. -/
theorem inter_eq_octahedron :
    TetA ∩ TetB = {p | ∀ a, |proj a p| ≤ 1} ∧
      TetA ∩ TetB = {p | |p 0| + |p 1| + |p 2| ≤ 1} := by
  have h1 : TetA ∩ TetB = {p | ∀ a, |proj a p| ≤ 1} := by
    ext p
    simp only [Set.mem_inter_iff, mem_TetA, mem_TetB, Set.mem_ofPred_eq, abs_le]
    constructor
    · rintro ⟨hA, hB⟩ a; exact ⟨by linarith [hB a], hA a⟩
    · intro h; exact ⟨fun a => (h a).2, fun a => by linarith [(h a).1]⟩
  refine ⟨h1, ?_⟩
  rw [h1]
  ext p
  simp only [Set.mem_ofPred_eq]
  constructor
  · intro h
    obtain ⟨h0, h1, h2, h3⟩ := proj_formulas p
    have a0 := abs_le.mp (h 0); have a1 := abs_le.mp (h 1)
    have a2 := abs_le.mp (h 2); have a3 := abs_le.mp (h 3)
    rw [h0] at a0; rw [h1] at a1; rw [h2] at a2; rw [h3] at a3
    rcases abs_cases (p 0) with ⟨e0, _⟩ | ⟨e0, _⟩ <;>
    rcases abs_cases (p 1) with ⟨e1, _⟩ | ⟨e1, _⟩ <;>
    rcases abs_cases (p 2) with ⟨e2, _⟩ | ⟨e2, _⟩ <;>
    rw [e0, e1, e2] <;> linarith [a0.1, a0.2, a1.1, a1.2, a2.1, a2.2, a3.1, a3.2]
  · intro h a
    exact (abs_proj_le a p).trans h

/-- The octahedron's six vertices `±ê_j`. -/
def octVert (u : Fin 3 × Bool) : Fin 3 → ℝ := (if u.2 then (1 : ℝ) else -1) • Pi.single u.1 1

/-- **The octahedron is regular**: its six vertices lie in `TetA ∩ TetB` on its boundary, and the
twelve edges (pairs of non-opposite vertices) all have squared length `2`. -/
theorem octahedron_regular :
    (∀ u, octVert u ∈ TetA ∩ TetB ∧ |octVert u 0| + |octVert u 1| + |octVert u 2| = 1) ∧
    (∀ u v : Fin 3 × Bool, u.1 ≠ v.1 →
      (octVert u - octVert v) ⬝ᵥ (octVert u - octVert v) = 2) ∧
    (Finset.univ.filter fun e : (Fin 3 × Bool) × (Fin 3 × Bool) => e.1.1 ≠ e.2.1).card = 2 * 12 := by
  refine ⟨fun u => ?_, fun u v huv => ?_, by decide⟩
  · rw [(inter_eq_octahedron).2]
    obtain ⟨j, b⟩ := u
    fin_cases j <;> cases b <;> simp [octVert]
  · obtain ⟨j, b⟩ := u; obtain ⟨k, c⟩ := v
    simp only at huv
    fin_cases j <;> fin_cases k <;> cases b <;> cases c <;> simp_all [octVert, dotProduct,
      Fin.sum_univ_three, Pi.single_apply] <;> norm_num

lemma max_split (x : ℝ) : max x 0 - max (-x) 0 = x ∧ max x 0 + max (-x) 0 = |x| := by
  rcases le_total 0 x with h | h
  · rw [max_eq_left h, max_eq_right (by linarith), abs_of_nonneg h]; constructor <;> ring
  · rw [max_eq_right h, max_eq_left (by linarith), abs_of_nonpos h]; constructor <;> ring

lemma sum_octVert (w : Fin 3 × Bool → ℝ) (i : Fin 3) :
    (∑ u, w u • octVert u) i = w (i, true) - w (i, false) := by
  simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Fintype.sum_prod_type,
    Fintype.sum_bool, octVert, Fin.sum_univ_three]
  fin_cases i <;> simp <;> ring

/-- **The octahedron is the convex hull of its six vertices** `±ê_j`. -/
theorem inter_eq_hull_octVert :
    TetA ∩ TetB =
      {p | ∃ w : Fin 3 × Bool → ℝ, (∀ u, 0 ≤ w u) ∧ ∑ u, w u = 1 ∧ p = ∑ u, w u • octVert u} := by
  rw [(inter_eq_octahedron).2]
  ext p
  simp only [Set.mem_ofPred_eq]
  constructor
  · intro hp
    set r := 1 - (|p 0| + |p 1| + |p 2|) with hr
    refine ⟨fun u => (if u.2 then max (p u.1) 0 else max (-p u.1) 0) +
      (if u.1 = 0 then r / 2 else 0), fun u => ?_, ?_, ?_⟩
    · have : 0 ≤ r := by linarith
      positivity
    · simp only [Fintype.sum_prod_type, Fintype.sum_bool, Fin.sum_univ_three, ite_true]
      have := (max_split (p 0)).2; have := (max_split (p 1)).2; have := (max_split (p 2)).2
      simp; linarith
    · funext i
      rw [sum_octVert]
      simp only [Bool.false_eq_true, ite_true, ite_false]
      have := (max_split (p i)).1
      linarith
  · rintro ⟨w, hw, hsum, rfl⟩
    simp only [sum_octVert]
    have e : ∀ i, |w (i, true) - w (i, false)| ≤ w (i, true) + w (i, false) := fun i => by
      rw [abs_le]; constructor <;> linarith [hw (i, true), hw (i, false)]
    simp only [Fintype.sum_prod_type, Fintype.sum_bool, Fin.sum_univ_three] at hsum
    linarith [e 0, e 1, e 2]

/-! ## The sixteen boundary channels -/

/-- Face `a` of TetA: the points of TetA with `v_a = 1`. -/
def face (a : Fin 4) : Set (Fin 3 → ℝ) := {p | p ∈ TetA ∧ proj a p = 1}

/-- The central core of face `a`: the part inside TetB. -/
def core (a : Fin 4) : Set (Fin 3 → ℝ) := face a ∩ TetB

/-- Corner `b` of face `a`: the part beyond TetB's face `−v_b = 1`. -/
def corner (a b : Fin 4) : Set (Fin 3 → ℝ) := {p | p ∈ face a ∧ 1 < -proj b p}

/-- Channel `(a, b)`: the core of face `a` if `b = a`, otherwise its corner `b`. -/
def channel (a b : Fin 4) : Set (Fin 3 → ℝ) := if b = a then core a else corner a b

lemma convex_halfspace_le (a : Fin 4) (σ : ℝ) : Convex ℝ {p : Fin 3 → ℝ | σ * proj a p ≤ 1} := by
  intro x hx y hy s t hs ht hst
  simp only [Set.mem_ofPred_eq, proj_add, proj_smul] at hx hy ⊢
  nlinarith

lemma convex_face (a : Fin 4) : Convex ℝ (face a) := by
  intro x hx y hy s t hs ht hst
  simp only [face, Set.mem_ofPred_eq, mem_TetA, proj_add, proj_smul] at hx hy ⊢
  refine ⟨fun c => ?_, by rw [hx.2, hy.2]; linarith⟩
  nlinarith [hx.1 c, hy.1 c]

/-- **The sixteen channels.** For each face `a` of TetA: the face is the union of its four
channels (one core, three corners), the channels are pairwise disjoint, each is non-empty, and
each is convex. With four faces this gives `4 × 4 = 16` channels. -/
theorem channels :
    (∀ a, face a = ⋃ b, channel a b) ∧
    (∀ a b c, b ≠ c → Disjoint (channel a b) (channel a c)) ∧
    (∀ a b, (channel a b).Nonempty) ∧
    (∀ a b, Convex ℝ (channel a b)) ∧
    Fintype.card (Fin 4 × Fin 4) = 16 := by
  refine ⟨fun a => ?_, fun a b c hbc => ?_, fun a b => ?_, fun a b => ?_, by simp⟩
  · ext p
    simp only [Set.mem_iUnion]
    constructor
    · intro hp
      by_cases hB : p ∈ TetB
      · exact ⟨a, by simp [channel, core, hp, hB]⟩
      · rw [mem_TetB] at hB; push Not at hB
        obtain ⟨b, hb⟩ := hB
        have hba : b ≠ a := by
          intro h; rw [h, hp.2] at hb; norm_num at hb
        exact ⟨b, by simp [channel, hba, corner, hp, hb]⟩
    · rintro ⟨b, hb⟩
      by_cases h : b = a
      · simp only [channel, h, ite_true, core] at hb; exact hb.1
      · simp only [channel, h, ite_false, corner] at hb; exact hb.1
  · rw [Set.disjoint_left]
    intro p hpb hpc
    have hface : p ∈ face a := by
      unfold channel at hpb; split_ifs at hpb
      · exact hpb.1
      · exact hpb.1
    have hA := (mem_TetA p).mp hface.1
    have hs := proj_sum p
    rw [Fin.sum_univ_four] at hs
    have ha := hface.2
    unfold channel at hpb hpc
    split_ifs at hpb hpc with h1 h2 h2
    · exact hbc (h1.trans h2.symm)
    · have := (mem_TetB p).mp hpb.2 c; linarith [hpc.2]
    · have := (mem_TetB p).mp hpc.2 b; linarith [hpb.2]
    · have hb := hpb.2; have hc := hpc.2
      have a0 := hA 0; have a1 := hA 1; have a2 := hA 2; have a3 := hA 3
      clear hpb hpc hface
      fin_cases a <;> fin_cases b <;> fin_cases c <;> simp at * <;> linarith
  · by_cases h : b = a
    · refine ⟨(1 / 3 : ℝ) • Mcol a, ?_⟩
      simp only [channel, h, ite_true, core, face, Set.mem_inter_iff, Set.mem_ofPred_eq,
        mem_TetA, mem_TetB, proj_smul, proj_Mcol]
      refine ⟨⟨fun c => ?_, by simp⟩, fun c => ?_⟩ <;> split_ifs <;> norm_num
    · refine ⟨-Mcol b, ?_⟩
      simp only [channel, h, ite_false, corner, face, Set.mem_ofPred_eq, mem_TetA, proj_neg,
        proj_Mcol]
      refine ⟨⟨fun c => ?_, by simp [Ne.symm h]⟩, by simp⟩
      split_ifs <;> norm_num
  · unfold channel
    split_ifs
    · have hB : TetB = ⋂ c, {p : Fin 3 → ℝ | (-1) * proj c p ≤ 1} := by
        ext p; simp [mem_TetB]
      rw [core, hB]
      exact (convex_face a).inter (convex_iInter fun c => convex_halfspace_le c (-1))
    · intro x hx y hy s t hs ht hst
      simp only [corner, Set.mem_ofPred_eq] at hx hy ⊢
      refine ⟨convex_face a hx.1 hy.1 hs ht hst, ?_⟩
      rw [proj_add, proj_smul, proj_smul]
      have h2 : t * 1 ≤ t * (-proj b y) := mul_le_mul_of_nonneg_left hy.2.le ht
      rcases hs.lt_or_eq with hs' | hs'
      · have h3 : s * 1 < s * (-proj b x) := mul_lt_mul_of_pos_left hx.2 hs'
        linarith
      · subst hs'
        have ht1 : t = 1 := by linarith
        subst ht1
        linarith [hy.2]

/-! ## Structural inventory -/

open Classical in
/-- **Structural inventory.** The two tetrahedra have `2^D = 8` distinct vertices, `K × D = 12`
edges and `2K = 8` faces; with `K² = 16` channels, `V + E + F = K(K+D) = 28` and
`V − E + F = 4`, twice the Euler characteristic of a sphere. -/
theorem inventory :
    let vA : Finset (Fin 3 → ℝ) := Finset.univ.image fun a => -Mcol a
    let vB : Finset (Fin 3 → ℝ) := Finset.univ.image Mcol
    vA.card = 4 ∧ vB.card = 4 ∧ Disjoint vA vB ∧ (vA ∪ vB).card = 2 ^ 3 ∧
      (vA.powersetCard 2 ∪ vB.powersetCard 2).card = 4 * 3 ∧
      (vA.powersetCard 3 ∪ vB.powersetCard 3).card = 2 * 4 ∧
      Fintype.card (Fin 4 × Fin 4) = 4 ^ 2 ∧
      8 + 12 + 8 = 4 * (4 + 3) ∧ (8 : ℤ) - 12 + 8 = 2 * 2 := by
  intro vA vB
  have hinjB : Function.Injective Mcol := by
    intro a b h
    have := proj_Mcol a b
    rw [h, proj_Mcol] at this
    by_contra hne
    simp [Ne.symm hne] at this; norm_num at this
  have hinjA : Function.Injective fun a => -Mcol a := fun a b h => hinjB (neg_injective h)
  have hcA : vA.card = 4 := by
    simp only [vA]; rw [Finset.card_image_of_injective _ hinjA]; simp
  have hcB : vB.card = 4 := by
    simp only [vB]; rw [Finset.card_image_of_injective _ hinjB]; simp
  have hdisj : Disjoint vA vB := by
    rw [Finset.disjoint_left]
    intro x hx hx'
    simp only [vA, vB, Finset.mem_image, Finset.mem_univ, true_and] at hx hx'
    obtain ⟨a, rfl⟩ := hx; obtain ⟨b, hb⟩ := hx'
    have := proj_Mcol b a
    rw [hb, proj_neg, proj_Mcol] at this
    split_ifs at this <;> norm_num at this
  have hpow : ∀ k, Disjoint (vA.powersetCard k) (vB.powersetCard k) ∨ k = 0 := by
    intro k
    by_cases hk : k = 0
    · right; exact hk
    · left
      rw [Finset.disjoint_left]
      intro S hSA hSB
      rw [Finset.mem_powersetCard] at hSA hSB
      obtain ⟨x, hx⟩ : S.Nonempty := Finset.card_pos.mp (by omega)
      exact Finset.disjoint_left.mp hdisj (hSA.1 hx) (hSB.1 hx)
  refine ⟨hcA, hcB, hdisj, ?_, ?_, ?_, by simp, by norm_num, by norm_num⟩
  · rw [Finset.card_union_of_disjoint hdisj, hcA, hcB]; norm_num
  · rcases hpow 2 with h | h
    · rw [Finset.card_union_of_disjoint h, Finset.card_powersetCard, Finset.card_powersetCard,
        hcA, hcB]; rfl
    · norm_num at h
  · rcases hpow 3 with h | h
    · rw [Finset.card_union_of_disjoint h, Finset.card_powersetCard, Finset.card_powersetCard,
        hcA, hcB]; rfl
    · norm_num at h

/-- **The 3 + 1 pattern.** Of TetA's four face normals `n_a`, one has uniform signs `(+,+,+)` and
three have mixed signs; TetB's normals `−n_a` carry the same pattern with `(−,−,−)`. -/
theorem three_plus_one :
    (∀ i, Mcol 0 i = 1) ∧ (∀ a, a ≠ 0 → ∃ i j, Mcol a i ≠ Mcol a j) ∧
      (∀ i, (-Mcol 0) i = -1) := by
  refine ⟨fun i => ?_, fun a ha => ?_, fun i => ?_⟩
  · fin_cases i <;> simp [Mcol, Mmat]
  · fin_cases a
    · exact absurd rfl ha
    · exact ⟨0, 1, by simp [Mcol, Mmat]; norm_num⟩
    · exact ⟨0, 1, by simp [Mcol, Mmat]; norm_num⟩
    · exact ⟨0, 2, by simp [Mcol, Mmat]; norm_num⟩
  · fin_cases i <;> simp [Mcol, Mmat]

#print axioms HalfSpaceTwoBoundedRegions.proj_sum
#print axioms HalfSpaceTwoBoundedRegions.proj_relations
#print axioms HalfSpaceTwoBoundedRegions.classification
#print axioms HalfSpaceTwoBoundedRegions.exactly_two_bounded
#print axioms HalfSpaceTwoBoundedRegions.TetA_eq_hull
#print axioms HalfSpaceTwoBoundedRegions.TetB_eq_hull
#print axioms HalfSpaceTwoBoundedRegions.TetB_eq_neg_TetA
#print axioms HalfSpaceTwoBoundedRegions.interpenetration
#print axioms HalfSpaceTwoBoundedRegions.inter_eq_octahedron
#print axioms HalfSpaceTwoBoundedRegions.octahedron_regular
#print axioms HalfSpaceTwoBoundedRegions.inter_eq_hull_octVert
#print axioms HalfSpaceTwoBoundedRegions.channels
#print axioms HalfSpaceTwoBoundedRegions.inventory
#print axioms HalfSpaceTwoBoundedRegions.three_plus_one

end HalfSpaceTwoBoundedRegions
