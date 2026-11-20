import GramMatrixTetradEquation
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

/-!
# Lean 4 / Mathlib formalisation of
#   S. Nelson, "The Walsh Eigenmodes of the Cube, and What Field Closure Reads"

Builds on `GramMatrixTetradEquation` (and through it the forced frame, the half-space regions and
the tetrad scheme): TetA's corners are proved to be the columns of the forced frame `M`.

## How to referee this file
A Lean proof can only be wrong in its *statements*. Check these definitions against the paper:
* A corner is `s : C = Bool × Bool × Bool`, with coordinates `cx s, cy s, cz s ∈ {±1}`
  (`true ↦ +1`). `pt s` is the point `(cx, cy, cz) ∈ ℝ³`.
* A Walsh index is `S : C` read as a subset of `{x, y, z}` (`true` = member);
  `w S s = ∏_{d ∈ S} s_d`; `grade S = |S|`.
* `inA s` (Boolean): `s` is a TetA corner, `xyz = +1`.
* `flip m s`: the bit flip by the mask `m` (coordinate `d` is reversed iff `m_d`); `flipMat m` its
  permutation matrix. `adj`: the cube graph.
* An operator on the corners is `H : Matrix C C ℝ`; `H *ᵥ ψ` acts on amplitudes `ψ : C → ℝ`.
* `T_d` is `Td = Fin 6 × Fin 4`: an axis permutation `perm3 i` followed by an even sign-flip mask
  `masks j`; `act g` is its action on corners, `R g` its signed-permutation matrix on points
  (`pt_act`); `Td_complete` proves these are exactly the signed permutations keeping TetA.
* `IsInv H`: `H (g s) (g t) = H s t` for all `g`; `Hpar εA εB hAA hBB he hd` the six-parameter form
  (diagonal by chamber; same chamber: face diagonal; between: edge if distance 1, body diagonal
  if 3). `uA, uB, fA d, fB d`: the normalised chamber basis.
* `Heff`: the Schur complement `H_cc + H_cr (E − H_rr)⁻¹ H_rc` over any finite set of other sites.
* `gS`: the rotoreflection `(x, y, z) ↦ (−y, x, −z)`; `rot`: the quarter turn on functions;
  `psi = x + i y`; `J t ψ i j = 2 Im(ψ̄_j H_ji ψ_i)` with `H = t·adj`.
* `SA, SB`: chamber sums; `RA, RB`: frame readouts `Σ_{s ∈ chamber} φ(s) s`; `mu = SA/(SA + SB)`;
  `coef S φ = (1/8) Σ w_S φ` the node's Walsh coefficients; `mode θ = cos θ u_A + sin θ u_B`.

## What is not formalised
The fifteen-site whole cube itself and the numerical shares of Proposition 1 (the reduction to
`Heff` and its `T_d` form are proved for any finite set of other sites and any representation on
them); the octahedron's representation content in Corollary 1; the cited metric-kernel statement
of Theorem 3 (iii); the node's code runs in Theorem 4; and the cited bond-orbital dictionary of
Proposition 3 (iii). Over the corners `Hom_{T_d}` statements are proved in column form (the images
of the basis amplitudes), which is what a linear readout is.
-/

open Matrix Finset

namespace WalshEigenmodes

/-! ## Corners and Walsh functions -/

abbrev C := Bool × Bool × Bool

/-- The sign of a bit, `true ↦ +1`. -/
def sgn (b : Bool) : ℝ := if b then 1 else -1

def cx (s : C) : ℝ := sgn s.1
def cy (s : C) : ℝ := sgn s.2.1
def cz (s : C) : ℝ := sgn s.2.2

/-- The corner as a point of `ℝ³`. -/
def pt (s : C) : Fin 3 → ℝ := ![cx s, cy s, cz s]

/-- The Walsh function `w_S(s) = ∏_{d ∈ S} s_d`. -/
def w (S : C) (s : C) : ℝ :=
  (if S.1 then cx s else 1) * (if S.2.1 then cy s else 1) * (if S.2.2 then cz s else 1)

/-- The grade `|S|`. -/
def grade (S : C) : ℕ := (if S.1 then 1 else 0) + (if S.2.1 then 1 else 0) + (if S.2.2 then 1 else 0)

/-- The archive's names. -/
abbrev S1 : C := (false, false, false)
abbrev Sx : C := (true, false, false)
abbrev Sy : C := (false, true, false)
abbrev Sz : C := (false, false, true)
abbrev Syz : C := (false, true, true)
abbrev Sxz : C := (true, false, true)
abbrev Sxy : C := (true, true, false)
abbrev Sxyz : C := (true, true, true)

/-- TetA: the corners with `xyz = +1` (an odd number of `+1` coordinates). -/
def inA (s : C) : Bool := xor (xor s.1 s.2.1) s.2.2

/-- Sums over the eight corners, written out. -/
lemma sum_C (f : C → ℝ) : ∑ s, f s =
    f (true, true, true) + f (true, true, false) + f (true, false, true) + f (true, false, false) +
    f (false, true, true) + f (false, true, false) + f (false, false, true) +
    f (false, false, false) := by
  simp only [Fintype.sum_prod_type, Fintype.sum_bool]; ring

lemma w_xyz (s : C) : w Sxyz s = if inA s then 1 else -1 := by
  rcases s with ⟨a, b, c⟩; cases a <;> cases b <;> cases c <;> simp [w, cx, cy, cz, sgn, inA]

/-- **Orthogonality**: `w_S · w_T = 8 δ_{ST}`. -/
theorem walsh_orthogonal (S T : C) : ∑ s, w S s * w T s = if S = T then 8 else 0 := by
  rw [sum_C]
  rcases S with ⟨a, b, c⟩; rcases T with ⟨d, e, f⟩
  cases a <;> cases b <;> cases c <;> cases d <;> cases e <;> cases f <;>
    simp [w, cx, cy, cz, sgn] <;> norm_num

/-- **Completeness**: `∑_S w_S(s) w_S(t) = 8 δ_{st}`. -/
theorem walsh_complete (s t : C) : ∑ S, w S s * w S t = if s = t then 8 else 0 := by
  rw [sum_C]
  rcases s with ⟨a, b, c⟩; rcases t with ⟨d, e, f⟩
  cases a <;> cases b <;> cases c <;> cases d <;> cases e <;> cases f <;>
    simp [w, cx, cy, cz, sgn] <;> norm_num

/-- Every amplitude is its Walsh expansion: `ψ = ⅛ ∑_S (w_S·ψ) w_S`. -/
lemma walsh_expand (ψ : C → ℝ) : ψ = fun t => (1 / 8) * ∑ S, (∑ s, w S s * ψ s) * w S t := by
  funext t
  have : ∑ S, (∑ s, w S s * ψ s) * w S t = ∑ s, ψ s * ∑ S, w S s * w S t := by
    simp_rw [Finset.sum_mul, Finset.mul_sum]
    rw [Finset.sum_comm]
    exact Finset.sum_congr rfl fun s _ => Finset.sum_congr rfl fun S _ => by ring
  rw [this]
  simp_rw [walsh_complete]
  simp; ring

/-- Two operators that agree on every Walsh function are equal. -/
lemma walsh_ext {X Y : Matrix C C ℝ} (h : ∀ S, X *ᵥ w S = Y *ᵥ w S) : X = Y := by
  have hv : ∀ ψ : C → ℝ, X *ᵥ ψ = Y *ᵥ ψ := by
    intro ψ
    rw [walsh_expand ψ]
    have e : (fun t => (1 / 8 : ℝ) * ∑ S, (∑ s, w S s * ψ s) * w S t) =
        ∑ S, ((1 / 8 : ℝ) * ∑ s, w S s * ψ s) • w S := by
      funext t
      simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
      rw [Finset.mul_sum]
      exact Finset.sum_congr rfl fun S _ => by ring
    rw [e, mulVec_sum, mulVec_sum]
    simp only [mulVec_smul, h]
  ext s t
  have := congrFun (hv (Pi.single t 1)) s
  simpa [mulVec, dotProduct, Pi.single_apply] using this

/-! ## Theorem 1: the Walsh functions are the cube's eigenmodes -/

/-- The bit flip by the mask `m`. -/
def flip (m s : C) : C := (xor s.1 m.1, xor s.2.1 m.2.1, xor s.2.2 m.2.2)

/-- Its permutation matrix: `(flipMat m *ᵥ ψ)(s) = ψ(flip m s)`. -/
def flipMat (m : C) : Matrix C C ℝ := fun s t => if t = flip m s then 1 else 0

lemma flipMat_mulVec (m : C) (ψ : C → ℝ) : flipMat m *ᵥ ψ = fun s => ψ (flip m s) := by
  funext s; simp [flipMat, mulVec, dotProduct]

/-- The character of the bit flip `m` on `w_S`: `(−1)^{|S ∩ m|}`. -/
def chr (S m : C) : ℝ := w S (flip m (true, true, true))

lemma w_flip (S m s : C) : w S (flip m s) = chr S m * w S s := by
  rcases S with ⟨a, b, c⟩; rcases m with ⟨d, e, f⟩; rcases s with ⟨g, h, i⟩
  cases a <;> cases b <;> cases c <;> cases d <;> cases e <;> cases f <;> cases g <;> cases h <;>
    cases i <;> simp [w, chr, flip, cx, cy, cz, sgn]

/-- Different Walsh indices have different characters: some flip tells them apart. -/
lemma chr_separates {S T : C} (h : S ≠ T) : ∃ m, chr S m ≠ chr T m := by
  rcases S with ⟨a, b, c⟩; rcases T with ⟨d, e, f⟩
  refine ⟨if a = d then (if b = e then (false, false, true) else (false, true, false))
    else (true, false, false), ?_⟩
  cases a <;> cases b <;> cases c <;> cases d <;> cases e <;> cases f <;> simp at h ⊢ <;>
    simp [chr, w, flip, cx, cy, cz, sgn] <;> norm_num

/-- A joint eigenvector of every bit flip with the character of `w_S` is a multiple of `w_S`. -/
lemma joint_eigen {S : C} {v : C → ℝ} (h : ∀ m, (fun s => v (flip m s)) = chr S m • v) :
    v = (v (true, true, true) / w S (true, true, true)) • w S := by
  have hw : w S (true, true, true) ≠ 0 := by
    rcases S with ⟨a, b, c⟩; cases a <;> cases b <;> cases c <;> simp [w, cx, cy, cz, sgn]
  funext s
  -- `s = flip m (true,true,true)` for `m = flip s (true,true,true)` read as a mask
  have hs : s = flip (flip s (true, true, true)) (true, true, true) := by
    rcases s with ⟨a, b, c⟩; cases a <;> cases b <;> cases c <;> rfl
  have e1 := congrFun (h (flip s (true, true, true))) (true, true, true)
  have e2 := w_flip S (flip s (true, true, true)) (true, true, true)
  rw [← hs] at e1 e2
  simp only [Pi.smul_apply, smul_eq_mul] at e1 ⊢
  rw [e1, e2]; field_simp

/-- **Theorem 1.** `H` commutes with every bit flip iff every Walsh function is an eigenmode of
`H`; the eight eigenvalues are free (any `λ` is realised by exactly one such `H`). -/
theorem theorem1 (H : Matrix C C ℝ) :
    (∀ m, H * flipMat m = flipMat m * H) ↔ ∀ S, ∃ l : ℝ, H *ᵥ w S = l • w S := by
  constructor
  · intro hc S
    set v := H *ᵥ w S
    have h : ∀ m, (fun s => v (flip m s)) = chr S m • v := by
      intro m
      have e : flipMat m *ᵥ v = H *ᵥ (flipMat m *ᵥ w S) := by
        simp only [v, mulVec_mulVec, hc m]
      rw [flipMat_mulVec, flipMat_mulVec] at e
      rw [e]
      have : (fun s => w S (flip m s)) = chr S m • w S := by
        funext s; simp [w_flip]
      rw [this, mulVec_smul]
    exact ⟨_, joint_eigen h⟩
  · intro he m
    apply walsh_ext
    intro S
    obtain ⟨l, hl⟩ := he S
    have hf : flipMat m *ᵥ w S = chr S m • w S := by
      rw [flipMat_mulVec]; funext s; simp [w_flip]
    rw [← mulVec_mulVec, ← mulVec_mulVec, hf, mulVec_smul, hl, mulVec_smul, hf, smul_smul,
      smul_smul, mul_comm]

/-- The operator with Walsh eigenvalues `λ`: `H_λ = ⅛ ∑_S λ_S w_S w_Sᵀ`. -/
noncomputable def ofEigen (l : C → ℝ) : Matrix C C ℝ :=
  fun s t => (1 / 8) * ∑ S, l S * w S s * w S t

lemma ofEigen_mulVec (l : C → ℝ) (S : C) : ofEigen l *ᵥ w S = l S • w S := by
  funext s
  simp only [ofEigen, mulVec, dotProduct, Pi.smul_apply, smul_eq_mul]
  have : ∑ t, (1 / 8 * ∑ T, l T * w T s * w T t) * w S t =
      (1 / 8) * ∑ T, l T * w T s * ∑ t, w T t * w S t := by
    simp_rw [Finset.mul_sum, Finset.sum_mul]
    rw [Finset.sum_comm]
    exact Finset.sum_congr rfl fun T _ => Finset.sum_congr rfl fun t _ => by ring
  rw [this]
  simp_rw [walsh_orthogonal]
  simp
  ring

/-- **The eight eigenvalues are free**: every `λ : C → ℝ` is the Walsh spectrum of exactly one
operator commuting with the bit flips. -/
theorem eight_parameters (l : C → ℝ) :
    ∃! H : Matrix C C ℝ, ∀ S, H *ᵥ w S = l S • w S :=
  ⟨ofEigen l, ofEigen_mulVec l, fun H hH => walsh_ext fun S => by rw [hH, ofEigen_mulVec]⟩

/-- The cube graph: corners joined when they differ in exactly one coordinate. -/
def adj : Matrix C C ℝ := fun s t =>
  if (if s.1 = t.1 then 0 else 1) + (if s.2.1 = t.2.1 then 0 else 1) +
    (if s.2.2 = t.2.2 then 0 else 1) = (1 : ℕ) then 1 else 0

/-- **The cube graph's spectrum.** `A w_S = (3 − 2|S|) w_S` and `(3I − A) w_S = 2|S| w_S`. -/
theorem cube_graph (S : C) :
    adj *ᵥ w S = (3 - 2 * (grade S : ℝ)) • w S ∧
      ((3 : ℝ) • (1 : Matrix C C ℝ) - adj) *ᵥ w S = (2 * (grade S : ℝ)) • w S := by
  have hA : adj *ᵥ w S = (3 - 2 * (grade S : ℝ)) • w S := by
    funext s
    simp only [mulVec, dotProduct, Pi.smul_apply, smul_eq_mul]
    rw [sum_C]
    rcases S with ⟨a, b, c⟩; rcases s with ⟨d, e, f⟩
    cases a <;> cases b <;> cases c <;> cases d <;> cases e <;> cases f <;>
      simp [adj, w, grade, cx, cy, cz, sgn] <;> norm_num
  refine ⟨hA, ?_⟩
  rw [sub_mulVec, hA, smul_mulVec, one_mulVec, ← sub_smul]
  congr 1; ring

/-! ## The tetrahedral group `T_d` -/

/-- The coordinates of a corner as a function. -/
def toF (s : C) : Fin 3 → Bool := ![s.1, s.2.1, s.2.2]

/-- The six permutations of the axes (new axis `d` is old axis `perm3 i d`). -/
def perm3 : Fin 6 → Fin 3 → Fin 3 :=
  ![![0, 1, 2], ![1, 0, 2], ![2, 1, 0], ![0, 2, 1], ![1, 2, 0], ![2, 0, 1]]

/-- The four sign-flip masks with an even number of flips. -/
def masks : Fin 4 → C := ![(false, false, false), (true, true, false), (true, false, true),
  (false, true, true)]

/-- `T_d`: an axis permutation followed by an even number of sign flips (24 elements). -/
abbrev Td := Fin 6 × Fin 4

def permute (i : Fin 6) (s : C) : C := (toF s (perm3 i 0), toF s (perm3 i 1), toF s (perm3 i 2))

/-- The action of `g ∈ T_d` on corners. -/
def act (g : Td) (s : C) : C := flip (masks g.2) (permute g.1 s)

/-- Its matrix on points: `pt (g s) = R g *ᵥ pt s` (a signed permutation matrix). -/
def R (g : Td) : Matrix (Fin 3) (Fin 3) ℝ := fun d e =>
  if perm3 g.1 d = e then (if toF (masks g.2) d then -1 else 1) else 0

set_option maxHeartbeats 4000000 in
lemma pt_act (g : Td) (s : C) : pt (act g s) = R g *ᵥ pt s := by
  rcases g with ⟨i, j⟩; rcases s with ⟨a, b, c⟩
  funext d
  fin_cases i <;> fin_cases j <;> cases a <;> cases b <;> cases c <;> fin_cases d <;>
    simp [act, permute, flip, perm3, masks, toF, R, pt, cx, cy, cz, sgn, mulVec, dotProduct]

/-- `T_d` acts by bijections that keep TetA. -/
theorem Td_facts :
    (∀ g : Td, Function.Bijective (act g)) ∧ (∀ g : Td, ∀ s, inA (act g s) = inA s) ∧
      Fintype.card Td = 24 := by
  refine ⟨by decide, by decide, by simp⟩

/-- **`T_d` is exactly the signed permutations keeping TetA**: an axis permutation followed by the
flips `m` keeps TetA iff `m` flips an even number of axes. -/
theorem Td_complete (i : Fin 6) (m : C) :
    (∀ s, inA (flip m (permute i s)) = inA s) ↔ ∃ j, masks j = m := by
  revert i m; decide

/-- The inversion `−I` (all flips) exchanges TetA and TetB. -/
theorem inversion_exchanges (s : C) : inA (flip (true, true, true) s) = !inA s := by
  revert s; decide

/-- Corners differing in exactly `k` coordinates. -/
def dist (s t : C) : ℕ :=
  (if s.1 = t.1 then 0 else 1) + (if s.2.1 = t.2.1 then 0 else 1) + (if s.2.2 = t.2.2 then 0 else 1)

lemma dist_act (g : Td) (s t : C) : dist (act g s) (act g t) = dist s t := by
  revert g s t; decide

lemma act_eq_iff (g : Td) (s t : C) : act g s = act g t ↔ s = t := by
  revert g s t; decide

/-- Inside a chamber, distinct corners are face diagonals (distance 2); between chambers, cube
edges (1) or body diagonals (3). -/
lemma dist_chambers (s t : C) :
    (s ≠ t → inA s = inA t → dist s t = 2) ∧ (inA s ≠ inA t → dist s t = 1 ∨ dist s t = 3) := by
  revert s t; decide

/-! ## Theorem 2: the pairing of the grades -/

/-- The complementary Walsh index `S̄`. -/
def cmp (S : C) : C := (!S.1, !S.2.1, !S.2.2)

/-- **Theorem 2 (i).** Under `T_d`: `1` and `xyz` are invariant (`A_1`); the vector modes transform by
the signed permutation `R g` (a copy of `T_2`); the bivector modes are `xyz` times the vector modes
(the second copy); multiplication by `xyz` sends `w_S` to `w_{S̄}`, so grade `k` to grade `3 − k`, and
commutes with `T_d`. -/
theorem corners_under_Td :
    (∀ g : Td, ∀ s, w S1 (act g s) = w S1 s ∧ w Sxyz (act g s) = w Sxyz s) ∧
    (∀ g : Td, ∀ s, pt (act g s) = R g *ᵥ pt s) ∧
    (∀ s, w Syz s = w Sxyz s * w Sx s ∧ w Sxz s = w Sxyz s * w Sy s ∧ w Sxy s = w Sxyz s * w Sz s) ∧
    (∀ S s, w Sxyz s * w S s = w (cmp S) s) ∧ (∀ S, grade (cmp S) = 3 - grade S) ∧
    (∀ (g : Td) (φ : C → ℝ) s, w Sxyz (act g s) * φ (act g s) = w Sxyz s * φ (act g s)) := by
  have hx : ∀ g s, w Sxyz (act g s) = w Sxyz s := fun g s => by rw [w_xyz, w_xyz, Td_facts.2.1]
  refine ⟨fun g s => ⟨by simp [w], hx g s⟩, pt_act, fun s => ?_, fun S s => ?_, fun S => ?_,
    fun g φ s => by rw [hx]⟩
  · rcases s with ⟨a, b, c⟩
    cases a <;> cases b <;> cases c <;> simp [w, cx, cy, cz, sgn]
  · rcases S with ⟨a, b, c⟩; rcases s with ⟨d, e, f⟩
    cases a <;> cases b <;> cases c <;> cases d <;> cases e <;> cases f <;>
      simp [cmp, w, cx, cy, cz, sgn]
  · rcases S with ⟨a, b, c⟩
    cases a <;> cases b <;> cases c <;> simp [cmp, grade]

/-- The six-parameter `T_d`-invariant operator, Eq. (2). -/
def Hpar (eA eB hAA hBB he hd : ℝ) : Matrix C C ℝ := fun s t =>
  if s = t then (if inA s then eA else eB)
  else if inA s = inA t then (if inA s then hAA else hBB)
  else if dist s t = 1 then he else hd

/-- `T_d`-invariance of an operator. -/
def IsInv (H : Matrix C C ℝ) : Prop := ∀ g : Td, ∀ s t, H (act g s) (act g t) = H s t

/-- The permutation matrix of `g`: `(permMat g *ᵥ ψ)(s) = ψ(g s)`. -/
def permMat (g : Td) : Matrix C C ℝ := fun s t => if t = act g s then 1 else 0

/-- Invariance is commuting with the permutation representation. -/
lemma permMat_mul (g : Td) (H : Matrix C C ℝ) (s t : C) :
    (permMat g * H) s t = H (act g s) t := by
  simp [Matrix.mul_apply, permMat]

lemma mul_permMat_act (g : Td) (H : Matrix C C ℝ) (s u : C) :
    (H * permMat g) s (act g u) = H s u := by
  simp [Matrix.mul_apply, permMat, act_eq_iff]

theorem isInv_iff_commute (H : Matrix C C ℝ) :
    IsInv H ↔ ∀ g, H * permMat g = permMat g * H := by
  constructor
  · intro h g
    ext s t
    obtain ⟨u, rfl⟩ := (Td_facts.1 g).2 t
    rw [mul_permMat_act, permMat_mul, h g s u]
  · intro h g s t
    have := congrFun (congrFun (h g) s) (act g t)
    rw [mul_permMat_act, permMat_mul] at this
    exact this.symm

/-- **Theorem 2 (ii), invariance.** `Hpar` is symmetric and `T_d`-invariant. -/
theorem Hpar_inv (eA eB hAA hBB he hd : ℝ) :
    IsInv (Hpar eA eB hAA hBB he hd) ∧ (Hpar eA eB hAA hBB he hd)ᵀ = Hpar eA eB hAA hBB he hd := by
  refine ⟨fun g s t => ?_, ?_⟩
  · simp only [Hpar, act_eq_iff, Td_facts.2.1, dist_act]
  · ext s t
    simp only [transpose_apply]
    rcases s with ⟨a, b, c⟩; rcases t with ⟨d, e, f⟩
    cases a <;> cases b <;> cases c <;> cases d <;> cases e <;> cases f <;> simp [Hpar, inA, dist]

/-- A representative pair for each of the six orbits of `T_d` on unordered pairs of corners. -/
def rep (s t : C) : C × C :=
  if s = t then (if inA s then ((true, true, true), (true, true, true))
    else ((false, false, false), (false, false, false)))
  else if inA s = inA t then (if inA s then ((true, true, true), (true, false, false))
    else ((false, false, false), (false, true, true)))
  else if dist s t = 1 then ((true, true, true), (true, true, false))
  else ((true, true, true), (false, false, false))

/-- Every pair of corners is carried to or from its representative by some `g ∈ T_d`: the six
orbits are exhausted. -/
lemma rep_orbit : ∀ s t : C, ∃ g : Td,
    (act g (rep s t).1 = s ∧ act g (rep s t).2 = t) ∨ (act g (rep s t).1 = t ∧ act g (rep s t).2 = s) := by
  decide

/-- **Theorem 2 (ii), generality.** Every symmetric `T_d`-invariant operator is `Hpar` with its six
parameters read off one representative of each orbit. -/
theorem general_inv (H : Matrix C C ℝ) (hinv : IsInv H) (hs : Hᵀ = H) :
    H = Hpar (H (true, true, true) (true, true, true)) (H (false, false, false) (false, false, false))
      (H (true, true, true) (true, false, false)) (H (false, false, false) (false, true, true))
      (H (true, true, true) (true, true, false)) (H (true, true, true) (false, false, false)) := by
  have hsym : ∀ s t, H s t = H t s := fun s t => by
    have := congrFun (congrFun hs s) t; rw [transpose_apply] at this; exact this.symm
  ext s t
  have key : H s t = H (rep s t).1 (rep s t).2 := by
    obtain ⟨g, ⟨h1, h2⟩ | ⟨h1, h2⟩⟩ := rep_orbit s t
    · have := hinv g (rep s t).1 (rep s t).2; rw [h1, h2] at this; exact this
    · have := hinv g (rep s t).1 (rep s t).2; rw [h1, h2] at this; exact (hsym s t).trans this
  rw [key]
  unfold Hpar rep
  split_ifs <;> rfl

/-- The chamber basis: normalised indicators `u_A, u_B` and frame coordinates `f^d_A, f^d_B`. -/
noncomputable def uA (s : C) : ℝ := if inA s then 1 / 2 else 0
noncomputable def uB (s : C) : ℝ := if inA s then 0 else 1 / 2
noncomputable def fA (d : Fin 3) (s : C) : ℝ := if inA s then pt s d / 2 else 0
noncomputable def fB (d : Fin 3) (s : C) : ℝ := if inA s then 0 else pt s d / 2

/-- The Walsh functions in the chamber basis. -/
theorem walsh_in_chamber_basis :
    w S1 = 2 • (uA + uB) ∧ w Sxyz = 2 • (uA - uB) ∧
      w Sx = 2 • (fA 0 + fB 0) ∧ w Syz = 2 • (fA 0 - fB 0) ∧
      w Sy = 2 • (fA 1 + fB 1) ∧ w Sxz = 2 • (fA 1 - fB 1) ∧
      w Sz = 2 • (fA 2 + fB 2) ∧ w Sxy = 2 • (fA 2 - fB 2) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> funext s <;> rcases s with ⟨a, b, c⟩ <;>
    cases a <;> cases b <;> cases c <;>
    simp [w, uA, uB, fA, fB, inA, pt, cx, cy, cz, sgn] <;> norm_num

/-- **Theorem 2 (ii), the blocks, Eq. (2).** In the chamber basis `H` is
`[[α_A, β], [β, α_B]] ⊕ [[γ_A, δ], [δ, γ_B]]^{⊕3}`. -/
theorem blocks (eA eB hAA hBB he hd : ℝ) :
    let H := Hpar eA eB hAA hBB he hd
    H *ᵥ uA = (eA + 3 * hAA) • uA + (3 * he + hd) • uB ∧
      H *ᵥ uB = (3 * he + hd) • uA + (eB + 3 * hBB) • uB ∧
      ∀ d, H *ᵥ fA d = (eA - hAA) • fA d + (he - hd) • fB d ∧
        H *ᵥ fB d = (he - hd) • fA d + (eB - hBB) • fB d := by
  intro H
  refine ⟨?_, ?_, fun d => ⟨?_, ?_⟩⟩ <;> funext s <;>
    simp only [H, mulVec, dotProduct, Pi.add_apply, Pi.smul_apply, smul_eq_mul] <;> rw [sum_C] <;>
    rcases s with ⟨a, b, c⟩ <;> cases a <;> cases b <;> cases c <;> try fin_cases d
  all_goals simp [Hpar, uA, uB, fA, fB, inA, dist, pt, cx, cy, cz, sgn]
  all_goals ring

/-- **Theorem 2 (iii).** For the invariant `H`, every Walsh function is an eigenmode iff
`ε_A = ε_B` and `h_AA = h_BB`, iff `H` is invariant under the inversion `−I` as well (TetA and TetB
alike); then the eigenvalues are `α ± β` on `1, xyz` and `γ ± δ` on grades 1, 2. -/
theorem alike_iff (eA eB hAA hBB he hd : ℝ) :
    let H := Hpar eA eB hAA hBB he hd
    ((∀ S, ∃ l : ℝ, H *ᵥ w S = l • w S) ↔ eA = eB ∧ hAA = hBB) ∧
      ((∀ s t, H (flip (true, true, true) s) (flip (true, true, true) t) = H s t) ↔
        eA = eB ∧ hAA = hBB) ∧
      (eA = eB → hAA = hBB →
        H *ᵥ w S1 = (eA + 3 * hAA + (3 * he + hd)) • w S1 ∧
        H *ᵥ w Sxyz = (eA + 3 * hAA - (3 * he + hd)) • w Sxyz ∧
        H *ᵥ w Sx = (eA - hAA + (he - hd)) • w Sx ∧
        H *ᵥ w Syz = (eA - hAA - (he - hd)) • w Syz) := by
  intro H
  have ev : ∀ S : C, ∀ l : ℝ, H *ᵥ w S = l • w S → ∀ s, (H *ᵥ w S) s = l * w S s :=
    fun S l h s => by rw [h]; rfl
  have hmul : ∀ S s, (H *ᵥ w S) s = ∑ t, H s t * w S t := fun S s => rfl
  refine ⟨⟨fun h => ?_, fun ⟨h1, h2⟩ => ?_⟩, ⟨fun h => ?_, fun ⟨h1, h2⟩ => ?_⟩, fun h1 h2 => ?_⟩
  · obtain ⟨l1, hl1⟩ := h S1; obtain ⟨lx, hlx⟩ := h Sx
    have a1 := ev _ _ hl1 (true, true, true); have a2 := ev _ _ hl1 (false, false, false)
    have b1 := ev _ _ hlx (true, true, true); have b2 := ev _ _ hlx (true, true, false)
    simp only [hmul, sum_C] at a1 a2 b1 b2
    simp [H, Hpar, inA, dist, w, cx, sgn] at a1 a2 b1 b2
    constructor <;> linarith
  · subst h1; subst h2
    intro S
    rcases S with ⟨a, b, c⟩
    refine ⟨∑ t, Hpar eA eA hAA hAA he hd (true, true, true) t * w (a, b, c) t /
      w (a, b, c) (true, true, true), ?_⟩
    funext s
    simp only [hmul, Pi.smul_apply, smul_eq_mul, sum_C]
    rcases s with ⟨d, e, f⟩
    cases a <;> cases b <;> cases c <;> cases d <;> cases e <;> cases f <;>
      simp [H, Hpar, inA, dist, w, cx, cy, cz, sgn] <;> ring
  · have a1 := h (true, true, true) (true, true, true)
    have a2 := h (true, true, true) (true, false, false)
    simp [H, Hpar, flip, inA] at a1 a2
    exact ⟨a1.symm, a2.symm⟩
  · subst h1; subst h2
    intro s t
    simp only [H, Hpar]
    rcases s with ⟨a, b, c⟩; rcases t with ⟨d, e, f⟩
    cases a <;> cases b <;> cases c <;> cases d <;> cases e <;> cases f <;> simp [flip, inA, dist]
  · subst h1; subst h2
    refine ⟨?_, ?_, ?_, ?_⟩ <;> funext s <;> simp only [hmul, Pi.smul_apply, smul_eq_mul, sum_C] <;>
      rcases s with ⟨d, e, f⟩ <;> cases d <;> cases e <;> cases f <;>
      simp [H, Hpar, inA, dist, w, cx, cy, cz, sgn] <;> ring

/-- **Theorem 2 (iv), the mixing.** In a block `[[a, b], [b, c]]` the vector `(cos θ, sin θ)` is an
eigenvector iff `(a − c) sin 2θ = 2b cos 2θ` (Eq. (3)); its weight on the lower grade of the pair,
the component along `(1, 1)/√2`, is `(cos θ + sin θ)²/2`. -/
theorem mixing (a b c θ : ℝ) :
    ((∃ l : ℝ, a * Real.cos θ + b * Real.sin θ = l * Real.cos θ ∧
        b * Real.cos θ + c * Real.sin θ = l * Real.sin θ) ↔
      (a - c) * Real.sin (2 * θ) = 2 * b * Real.cos (2 * θ)) ∧
    ((Real.cos θ + Real.sin θ) / Real.sqrt 2) ^ 2 = (Real.cos θ + Real.sin θ) ^ 2 / 2 := by
  have hs := Real.sin_sq_add_cos_sq θ
  rw [Real.sin_two_mul, Real.cos_two_mul]
  refine ⟨⟨fun ⟨l, h1, h2⟩ => ?_, fun h => ?_⟩, ?_⟩
  · have : (a * Real.cos θ + b * Real.sin θ) * Real.sin θ =
        (b * Real.cos θ + c * Real.sin θ) * Real.cos θ := by rw [h1, h2]; ring
    linear_combination 2 * this - 2 * b * hs
  · refine ⟨a * Real.cos θ ^ 2 + 2 * b * Real.sin θ * Real.cos θ + c * Real.sin θ ^ 2, ?_, ?_⟩
    · linear_combination (-(a * Real.cos θ + b * Real.sin θ)) * hs + (Real.sin θ / 2) * h + b * Real.sin θ * hs
    · linear_combination (-(b * Real.cos θ + c * Real.sin θ)) * hs - (Real.cos θ / 2) * h - b * Real.cos θ * hs
  · rw [div_pow, Real.sq_sqrt (by norm_num)]

/-- **Theorem 2 (iv), the weight on the lower grade.** The chamber bases are orthonormal, and the
block mode `cos θ · u_A + sin θ · u_B` (resp. `cos θ · f^d_A + sin θ · f^d_B`) has component
`(cos θ + sin θ)/√2` along the normalised lower-grade mode `(u_A + u_B)/√2 ∝ 1`
(resp. `(f^d_A + f^d_B)/√2 ∝ s_d`), so weight `(cos θ + sin θ)²/2`. -/
theorem lower_grade_weight (θ : ℝ) (d : Fin 3) :
    (∑ s, uA s * uA s = 1 ∧ ∑ s, uB s * uB s = 1 ∧ ∑ s, uA s * uB s = 0) ∧
    (∑ s, fA d s * fA d s = 1 ∧ ∑ s, fB d s * fB d s = 1 ∧ ∑ s, fA d s * fB d s = 0) ∧
    (∑ s, (Real.cos θ * uA s + Real.sin θ * uB s) * ((uA s + uB s) / Real.sqrt 2)) ^ 2 =
      (Real.cos θ + Real.sin θ) ^ 2 / 2 ∧
    (∑ s, (Real.cos θ * fA d s + Real.sin θ * fB d s) * ((fA d s + fB d s) / Real.sqrt 2)) ^ 2 =
      (Real.cos θ + Real.sin θ) ^ 2 / 2 := by
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hs : Real.sqrt 2 ≠ 0 := by positivity
  refine ⟨⟨?_, ?_, ?_⟩, ⟨?_, ?_, ?_⟩, ?_, ?_⟩ <;> rw [sum_C] <;> fin_cases d
  all_goals simp [uA, uB, fA, fB, inA, pt, cx, cy, cz, sgn]
  all_goals first
    | (norm_num; done)
    | (rw [show ∀ u : ℝ, u ^ 2 = u * u from fun u => sq u]; field_simp; ring_nf; rw [h2]; ring)

/-! ## TetA is the forced frame -/

/-- TetA's corners in the order of the forced frame's columns. -/
def legA : Fin 4 → C := ![(true, true, true), (true, false, false), (false, true, false),
  (false, false, true)]

/-- **Link to the chain.** TetA's corners are exactly the four legs `Mcol a` of the forced frame. -/
theorem tetA_is_frame :
    (∀ a, pt (legA a) = ForcedTetrahedralFrame.Mcol a) ∧ Function.Injective legA ∧
      ∀ s, inA s = true ↔ ∃ a, legA a = s := by
  refine ⟨fun a => ?_, by decide, by decide⟩
  funext d
  fin_cases a <;> fin_cases d <;>
    simp [legA, pt, cx, cy, cz, sgn, ForcedTetrahedralFrame.Mcol, ForcedTetrahedralFrame.Mmat]

/-! ## Proposition 1 (ii): the whole cube, by the Schur complement -/

section WholeCube

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- The effective corner operator `H_eff(E) = H_cc + H_cr (E − H_rr)⁻¹ H_rc` obtained by
eliminating the remaining sites `ι` (for the paper, the Field Origin's seven sites). -/
noncomputable def Heff (Hcc : Matrix C C ℝ) (Hcr : Matrix C ι ℝ) (Hrc : Matrix ι C ℝ)
    (Hrr : Matrix ι ι ℝ) (E : ℝ) : Matrix C C ℝ :=
  Hcc + Hcr * (E • (1 : Matrix ι ι ℝ) - Hrr)⁻¹ * Hrc

variable (Hcc : Matrix C C ℝ) (Hcr : Matrix C ι ℝ) (Hrc : Matrix ι C ℝ) (Hrr : Matrix ι ι ℝ)
  (E : ℝ)

/-- **Proposition 1 (ii), the reduction.** When `E` is not an eigenvalue of `H_rr`, `(c, r)` is an
eigenmode of the whole block operator at `E` iff `H_eff(E) c = E c` and `r = (E − H_rr)⁻¹ H_rc c`. -/
theorem schur (hG : IsUnit (E • (1 : Matrix ι ι ℝ) - Hrr).det) (c : C → ℝ) (r : ι → ℝ) :
    (Hcc *ᵥ c + Hcr *ᵥ r = E • c ∧ Hrc *ᵥ c + Hrr *ᵥ r = E • r) ↔
      (r = (E • (1 : Matrix ι ι ℝ) - Hrr)⁻¹ *ᵥ (Hrc *ᵥ c) ∧ Heff Hcc Hcr Hrc Hrr E *ᵥ c = E • c) := by
  set G := E • (1 : Matrix ι ι ℝ) - Hrr with hGdef
  have hGr : ∀ r, G *ᵥ r = E • r - Hrr *ᵥ r := fun r => by
    rw [hGdef, sub_mulVec, smul_mulVec, one_mulVec]
  have hiff : ∀ r y, G *ᵥ r = y ↔ r = G⁻¹ *ᵥ y := fun r y =>
    ⟨fun h => by rw [← h, mulVec_mulVec, nonsing_inv_mul G hG, one_mulVec],
     fun h => by rw [h, mulVec_mulVec, mul_nonsing_inv G hG, one_mulVec]⟩
  have hH : Heff Hcc Hcr Hrc Hrr E *ᵥ c = Hcc *ᵥ c + Hcr *ᵥ (G⁻¹ *ᵥ (Hrc *ᵥ c)) := by
    rw [Heff, add_mulVec, mulVec_mulVec, mulVec_mulVec, Matrix.mul_assoc]
  constructor
  · rintro ⟨h1, h2⟩
    have hr : r = G⁻¹ *ᵥ (Hrc *ᵥ c) := (hiff _ _).1 (by rw [hGr, ← h2]; abel)
    exact ⟨hr, by rw [hH, ← hr, h1]⟩
  · rintro ⟨hr, he⟩
    refine ⟨by rw [hH, ← hr] at he; exact he, ?_⟩
    have := (hiff r _).2 hr
    rw [hGr] at this
    rw [← this]; abel

/-- **Proposition 1 (ii), the symmetry.** If every block intertwines the representations (`P` on the
corners, `Q` on the remaining sites), so does `H_eff(E)`. -/
theorem Heff_commute (hG : IsUnit (E • (1 : Matrix ι ι ℝ) - Hrr).det) (P : Matrix C C ℝ)
    (Q : Matrix ι ι ℝ) (h1 : Hcc * P = P * Hcc) (h2 : Hcr * Q = P * Hcr) (h3 : Hrc * P = Q * Hrc)
    (h4 : Hrr * Q = Q * Hrr) : Heff Hcc Hcr Hrc Hrr E * P = P * Heff Hcc Hcr Hrc Hrr E := by
  set G := E • (1 : Matrix ι ι ℝ) - Hrr with hGdef
  have hGQ : G * Q = Q * G := by
    rw [hGdef, Matrix.sub_mul, Matrix.mul_sub, h4, Matrix.smul_mul, Matrix.mul_smul, Matrix.one_mul,
      Matrix.mul_one]
  have hGiQ : G⁻¹ * Q = Q * G⁻¹ := by
    calc G⁻¹ * Q = G⁻¹ * Q * (G * G⁻¹) := by rw [mul_nonsing_inv G hG, Matrix.mul_one]
      _ = G⁻¹ * (Q * G) * G⁻¹ := by simp only [Matrix.mul_assoc]
      _ = G⁻¹ * (G * Q) * G⁻¹ := by rw [hGQ]
      _ = Q * G⁻¹ := by rw [← Matrix.mul_assoc G⁻¹ G Q, nonsing_inv_mul G hG, Matrix.one_mul]
  unfold Heff
  rw [← hGdef, Matrix.add_mul, Matrix.mul_add, h1]
  congr 1
  calc Hcr * G⁻¹ * Hrc * P = Hcr * G⁻¹ * (Hrc * P) := by simp only [Matrix.mul_assoc]
    _ = Hcr * (G⁻¹ * Q) * Hrc := by rw [h3]; simp only [Matrix.mul_assoc]
    _ = (Hcr * Q) * G⁻¹ * Hrc := by rw [hGiQ]; simp only [Matrix.mul_assoc]
    _ = P * (Hcr * G⁻¹ * Hrc) := by rw [h2]; simp only [Matrix.mul_assoc]

/-- `H_eff(E)` is symmetric when the whole operator is. -/
theorem Heff_symm (hcc : Hccᵀ = Hcc) (hcr : Hrcᵀ = Hcr) (hrr : Hrrᵀ = Hrr) :
    (Heff Hcc Hcr Hrc Hrr E)ᵀ = Heff Hcc Hcr Hrc Hrr E := by
  have hG : (E • (1 : Matrix ι ι ℝ) - Hrr)ᵀ = E • (1 : Matrix ι ι ℝ) - Hrr := by
    rw [transpose_sub, transpose_smul, transpose_one, hrr]
  have hcr' : Hcrᵀ = Hrc := by rw [← hcr, transpose_transpose]
  rw [Heff, transpose_add, transpose_mul, transpose_mul, transpose_nonsing_inv, hG, hcc, hcr, hcr',
    Matrix.mul_assoc]

/-- **Proposition 1 (ii).** For a symmetric whole-cube operator whose blocks are `T_d`-equivariant
(`permMat g` on the corners, any representation `Q g` on the other sites), the effective corner
operator at every `E` off the spectrum of `H_rr` has the six-parameter form `Hpar`, with
`E`-dependent entries: Theorem 2 then applies mode by mode. -/
theorem whole_cube (hG : IsUnit (E • (1 : Matrix ι ι ℝ) - Hrr).det) (Q : Td → Matrix ι ι ℝ)
    (h1 : ∀ g, Hcc * permMat g = permMat g * Hcc) (h2 : ∀ g, Hcr * Q g = permMat g * Hcr)
    (h3 : ∀ g, Hrc * permMat g = Q g * Hrc) (h4 : ∀ g, Hrr * Q g = Q g * Hrr)
    (hcc : Hccᵀ = Hcc) (hcr : Hrcᵀ = Hcr) (hrr : Hrrᵀ = Hrr) :
    let K := Heff Hcc Hcr Hrc Hrr E
    K = Hpar (K (true, true, true) (true, true, true)) (K (false, false, false) (false, false, false))
      (K (true, true, true) (true, false, false)) (K (false, false, false) (false, true, true))
      (K (true, true, true) (true, true, false)) (K (true, true, true) (false, false, false)) := by
  intro K
  refine general_inv K ((isInv_iff_commute K).2 fun g => ?_) (Heff_symm _ _ _ _ _ hcc hcr hrr)
  exact Heff_commute _ _ _ _ _ hG _ _ (h1 g) (h2 g) (h3 g) (h4 g)

end WholeCube

/-! ## Corollary 1: the vortices are made of `T_2` modes -/

/-- The rotoreflection `S_4` about `ẑ`: `(x, y, z) ↦ (−y, x, −z)`, an element of `T_d`. -/
def gS : Td := (1, 2)

lemma pt_gS (s : C) : pt (act gS s) = ![-(pt s 1), pt s 0, -(pt s 2)] := by
  rcases s with ⟨a, b, c⟩; funext d
  cases a <;> cases b <;> cases c <;> fin_cases d <;>
    simp [gS, act, permute, flip, perm3, masks, toF, pt, cx, cy, cz, sgn]

/-- `S` on the Walsh functions (`(Sf)(s) = f(S s)`): `+1` on `1, xyz`; `−1` on `z, xy`; and a
quarter turn on each of the pairs `(x, y)` and `(xz, yz)`. -/
theorem S_on_walsh (s : C) :
    w S1 (act gS s) = w S1 s ∧ w Sxyz (act gS s) = w Sxyz s ∧
      w Sz (act gS s) = -w Sz s ∧ w Sxy (act gS s) = -w Sxy s ∧
      w Sx (act gS s) = -w Sy s ∧ w Sy (act gS s) = w Sx s ∧
      w Sxz (act gS s) = w Syz s ∧ w Syz (act gS s) = -w Sxz s := by
  rcases s with ⟨a, b, c⟩
  cases a <;> cases b <;> cases c <;>
    simp [gS, act, permute, flip, perm3, masks, toF, w, cx, cy, cz, sgn]

/-- The winding vectors: `x + i y` and `xz − i yz` (one in each corner `T_2` copy) have `S`-eigenvalue
`+i`. -/
theorem winding_vectors (s : C) :
    ((w Sx (act gS s) : ℂ) + Complex.I * w Sy (act gS s)) =
        Complex.I * ((w Sx s : ℂ) + Complex.I * w Sy s) ∧
      ((w Sxz (act gS s) : ℂ) - Complex.I * w Syz (act gS s)) =
        Complex.I * ((w Sxz s : ℂ) - Complex.I * w Syz s) := by
  obtain ⟨-, -, -, -, h1, h2, h3, h4⟩ := S_on_walsh s
  rw [h1, h2, h3, h4]
  constructor <;> apply Complex.ext <;> simp

/-- **The orthogonality.** If `v ∘ g = λ v` and `f ∘ g = m f` with `m λ ≠ 1`, then `⟨f, v⟩ = 0`. -/
theorem eigen_orth (g : Td) (v : C → ℂ) (l : ℂ) (hv : ∀ s, v (act g s) = l * v s) (f : C → ℝ)
    (m : ℝ) (hf : ∀ s, f (act g s) = m * f s) (hne : (m : ℂ) * l ≠ 1) :
    ∑ s, (f s : ℂ) * v s = 0 := by
  have h := (Td_facts.1 g).sum_comp (fun s => (f s : ℂ) * v s)
  simp only [hf, hv, Complex.ofReal_mul] at h
  have h' : ((m : ℂ) * l - 1) * ∑ s, (f s : ℂ) * v s = 0 := by
    rw [sub_mul, one_mul, Finset.mul_sum, ← h, sub_eq_zero]
    exact Finset.sum_congr rfl fun s _ => by ring
  rcases mul_eq_zero.1 h' with h0 | h0
  · exact absurd (sub_eq_zero.1 h0) hne
  · exact h0

/-- **Corollary 1.** (a) For any `g ∈ T_d`, an eigenvector with eigenvalue `≠ 1` is orthogonal to the
constant mode and to the chamber sign `xyz`: these never wind. (b) An amplitude in the winding space
`V_{+i}` of `S` is orthogonal to `1, xyz, z, xy`, so its Walsh expansion uses only the `T_2` modes
`x, y, xz, yz`. -/
theorem vortex_T2 :
    (∀ g : Td, ∀ (v : C → ℂ) (l : ℂ), l ≠ 1 → (∀ s, v (act g s) = l * v s) →
      ∑ s, (w S1 s : ℂ) * v s = 0 ∧ ∑ s, (w Sxyz s : ℂ) * v s = 0) ∧
    (∀ v : C → ℂ, (∀ s, v (act gS s) = Complex.I * v s) →
      ∑ s, (w S1 s : ℂ) * v s = 0 ∧ ∑ s, (w Sxyz s : ℂ) * v s = 0 ∧
        ∑ s, (w Sz s : ℂ) * v s = 0 ∧ ∑ s, (w Sxy s : ℂ) * v s = 0) := by
  have h1 : ∀ g s, w S1 (act g s) = 1 * w S1 s := fun g s => by simp [w]
  have hxyz : ∀ g s, w Sxyz (act g s) = 1 * w Sxyz s := fun g s => by
    rw [w_xyz, w_xyz, Td_facts.2.1, one_mul]
  have hI : ∀ m : ℝ, m = 1 ∨ m = -1 → (m : ℂ) * Complex.I ≠ 1 := by
    rintro m (rfl | rfl) h <;> simpa using congrArg Complex.im h
  refine ⟨fun g v l hl hv => ⟨eigen_orth g v l hv _ 1 (h1 g) (by simpa using hl),
    eigen_orth g v l hv _ 1 (hxyz g) (by simpa using hl)⟩, fun v hv => ⟨?_, ?_, ?_, ?_⟩⟩
  · exact eigen_orth gS v _ hv _ 1 (h1 gS) (hI 1 (Or.inl rfl))
  · exact eigen_orth gS v _ hv _ 1 (hxyz gS) (hI 1 (Or.inl rfl))
  · exact eigen_orth gS v _ hv _ (-1) (fun s => by rw [(S_on_walsh s).2.2.1]; ring)
      (hI (-1) (Or.inr rfl))
  · exact eigen_orth gS v _ hv _ (-1) (fun s => by rw [(S_on_walsh s).2.2.2.1]; ring)
      (hI (-1) (Or.inr rfl))

/-! ## Proposition 2: two standing waves make a vortex -/

lemma sum_CC (f : C → ℂ) : ∑ s, f s =
    f (true, true, true) + f (true, true, false) + f (true, false, true) + f (true, false, false) +
    f (false, true, true) + f (false, true, false) + f (false, false, true) +
    f (false, false, false) := by
  simp only [Fintype.sum_prod_type, Fintype.sum_bool]; ring

/-- The vortex amplitude `ψ = x + i y`. -/
noncomputable def psi (s : C) : ℂ := (cx s : ℂ) + Complex.I * cy s

/-- The quarter turn `C_4` about `ẑ` on functions, `(C_4 f)(s) = f(rot s)`: it sends `x ↦ y`,
`y ↦ −x`. -/
def rot (s : C) : C := (s.2.1, !s.1, s.2.2)

/-- The current `J_{i→j} = 2 Im(ψ̄_j H_{ji} ψ_i)` for `H = t A`. -/
noncomputable def J (t : ℝ) (ψ : C → ℂ) (i j : C) : ℝ :=
  2 * ((starRingEnd ℂ) (ψ j) * ((t * adj j i : ℝ) : ℂ) * ψ i).im

/-- **Proposition 2.** For `H = tA`: `ψ = x + iy` is an eigenmode at the grade-1 energy `t`;
`C_4 ψ = −iψ`; `‖ψ‖² = 16`; the current through each of the four half-planes bounded by the `z` axis
(the two cube edges crossing it, in the right-handed sense) is `−8t`, that is `−t/2` per unit
norm; and a real standing wave carries no current on any edge. -/
theorem two_standing_waves (t : ℝ) :
    (∀ s, ∑ u, ((t * adj s u : ℝ) : ℂ) * psi u = (t : ℂ) * psi s) ∧
    (∀ s, psi (rot s) = -Complex.I * psi s) ∧
    ∑ s, Complex.normSq (psi s) = 16 ∧
    J t psi (true, false, true) (true, true, true) + J t psi (true, false, false) (true, true, false)
      = -8 * t ∧
    J t psi (true, true, true) (false, true, true) + J t psi (true, true, false) (false, true, false)
      = -8 * t ∧
    J t psi (false, true, true) (false, false, true) +
      J t psi (false, true, false) (false, false, false) = -8 * t ∧
    J t psi (false, false, true) (true, false, true) +
      J t psi (false, false, false) (true, false, false) = -8 * t ∧
    (∀ φ : C → ℝ, ∀ i j, J t (fun s => (φ s : ℂ)) i j = 0) := by
  refine ⟨fun s => ?_, fun s => ?_, ?_, ?_, ?_, ?_, ?_, fun φ i j => ?_⟩
  · rw [sum_CC]
    rcases s with ⟨a, b, c⟩
    cases a <;> cases b <;> cases c <;> apply Complex.ext <;> simp [adj, psi, cx, cy, sgn]
  · rcases s with ⟨a, b, c⟩
    cases a <;> cases b <;> cases c <;> apply Complex.ext <;> simp [rot, psi, cx, cy, sgn]
  · rw [sum_C]; simp [psi, cx, cy, sgn, Complex.normSq_apply]; norm_num
  all_goals first
    | (simp [J, adj, psi, cx, cy, sgn, Complex.mul_im, Complex.mul_re]; ring)
    | simp [J, Complex.mul_im, Complex.mul_re]

/-! ## Theorem 3: what closure and field closure read -/

/-- Chamber sums `S_A, S_B` and frame readouts `R_A, R_B` of an amplitude on the eight corners. -/
def SA (φ : C → ℝ) : ℝ := ∑ s, if inA s then φ s else 0
def SB (φ : C → ℝ) : ℝ := ∑ s, if inA s then 0 else φ s
def RA (φ : C → ℝ) : Fin 3 → ℝ := fun d => ∑ s, if inA s then φ s * pt s d else 0
def RB (φ : C → ℝ) : Fin 3 → ℝ := fun d => ∑ s, if inA s then 0 else φ s * pt s d

/-- `R_A` is the forced frame applied to TetA's four amplitudes: `R_A φ = M (φ ∘ legA)`. -/
theorem RA_eq_frame (φ : C → ℝ) :
    RA φ = ForcedTetrahedralFrame.Mmat *ᵥ (fun a => φ (legA a)) := by
  funext d
  simp only [RA, mulVec, dotProduct]
  rw [sum_C, Fin.sum_univ_four]
  fin_cases d <;> simp [legA, inA, pt, cx, cy, cz, sgn, ForcedTetrahedralFrame.Mmat]

lemma act_base : ∀ s : C, ∃ j : Fin 4,
    act (0, j) (if inA s then (true, true, true) else (false, false, false)) = s := by decide

lemma act_base_fixed : ∀ i : Fin 6, act (i, 0) (true, true, true) = (true, true, true) ∧
    act (i, 0) (false, false, false) = (false, false, false) := by decide

lemma fixed_const (v : Fin 3 → ℝ) (h1 : R (1, 0) *ᵥ v = v) (h2 : R (2, 0) *ᵥ v = v) :
    v = fun _ => v 0 := by
  have a1 := congrFun h1 0; have a2 := congrFun h2 0
  simp [R, perm3, masks, toF, mulVec, dotProduct] at a1 a2
  funext d; fin_cases d
  · rfl
  · simp [a1]
  · simp [a2]

/-- **Theorem 3 (i), (iv), frames.** A `T_d`-equivariant assignment of vectors to corners
(`m (g s) = R g m s`: the columns of an equivariant linear readout) is `a · pt` on TetA and `b · pt`
on TetB. Restricted to TetA this is (i): every equivariant map from TetA's amplitudes is a multiple
of `R_A`. -/
theorem frame_equivariant (m : C → Fin 3 → ℝ) (h : ∀ g s, m (act g s) = R g *ᵥ m s) :
    ∃ a b : ℝ, ∀ s, m s = (if inA s then a else b) • pt s := by
  have base : ∀ p : C, (p = (true, true, true) ∨ p = (false, false, false)) →
      m p = fun _ => m p 0 := fun p hp =>
    fixed_const _ (by rw [← h, (by rcases hp with rfl | rfl <;> decide : act (1, 0) p = p)])
      (by rw [← h, (by rcases hp with rfl | rfl <;> decide : act (2, 0) p = p)])
  refine ⟨m (true, true, true) 0, -m (false, false, false) 0, fun s => ?_⟩
  obtain ⟨j, hj⟩ := act_base s
  by_cases hs : inA s
  · simp only [hs, ↓reduceIte] at hj ⊢
    rw [← hj, h, pt_act, ← mulVec_smul, base _ (Or.inl rfl)]
    congr 1; funext d; fin_cases d <;> simp [pt, cx, cy, cz, sgn]
  · simp only [hs, ↓reduceIte, Bool.false_eq_true] at hj ⊢
    rw [← hj, h, pt_act, ← mulVec_smul, base _ (Or.inr rfl)]
    congr 1; funext d; fin_cases d <;> simp [pt, cx, cy, cz, sgn]

/-- **Theorem 3 (iv), scalars.** A `T_d`-invariant assignment of numbers to corners is constant on
each chamber. -/
theorem scalar_invariant (f : C → ℝ) (h : ∀ g s, f (act g s) = f s) :
    ∀ s, f s = if inA s then f (true, true, true) else f (false, false, false) := by
  intro s
  obtain ⟨j, hj⟩ := act_base s
  by_cases hs : inA s <;> simp only [hs] at hj ⊢ <;> rw [← hj, h] <;> simp

/-- **Theorem 3 (iv), every equivariant readout factors.** A linear readout `φ ↦ Σ φ(s) m(s)` with
equivariant columns is `a R_A + b R_B`; one with invariant scalar columns is `a S_A + b S_B`. -/
theorem readouts_factor :
    (∀ m : C → Fin 3 → ℝ, (∀ g s, m (act g s) = R g *ᵥ m s) →
      ∃ a b : ℝ, ∀ φ : C → ℝ, (fun d => ∑ s, φ s * m s d) = a • RA φ + b • RB φ) ∧
    (∀ f : C → ℝ, (∀ g s, f (act g s) = f s) →
      ∃ a b : ℝ, ∀ φ : C → ℝ, ∑ s, φ s * f s = a * SA φ + b * SB φ) := by
  refine ⟨fun m hm => ?_, fun f hf => ?_⟩
  · obtain ⟨a, b, hab⟩ := frame_equivariant m hm
    refine ⟨a, b, fun φ => funext fun d => ?_⟩
    simp only [hab, Pi.smul_apply, smul_eq_mul, Pi.add_apply, RA, RB, Finset.mul_sum]
    rw [← Finset.sum_add_distrib]
    exact Finset.sum_congr rfl fun s _ => by by_cases hs : inA s <;> simp [hs] <;> ring
  · refine ⟨f (true, true, true), f (false, false, false), fun φ => ?_⟩
    simp only [SA, SB, Finset.mul_sum]
    rw [← Finset.sum_add_distrib]
    exact Finset.sum_congr rfl fun s _ => by
      rw [scalar_invariant f hf s]; by_cases hs : inA s <;> simp [hs] <;> ring

/-- **Theorem 3 (ii), closure.** The frame is blind to the constant mode, `R_A(1) = Σ_a v_a = 0`;
it also follows from the orbit sum, since `T_d` fixes no nonzero vector. -/
theorem closure :
    RA (fun _ => 1) = 0 ∧ ∑ a, ForcedTetrahedralFrame.Mcol a = 0 ∧
      ∀ v : Fin 3 → ℝ, (∀ g : Td, R g *ᵥ v = v) → v = 0 := by
  refine ⟨?_, ?_, fun v hv => ?_⟩
  · funext d; simp only [RA]; rw [sum_C]; fin_cases d <;> simp [inA, pt, cx, cy, cz, sgn]
  · funext d; rw [Finset.sum_apply, Fin.sum_univ_four]
    fin_cases d <;> simp [ForcedTetrahedralFrame.Mcol, ForcedTetrahedralFrame.Mmat]
  · have a1 := congrFun (hv (0, 1)) 0; have a2 := congrFun (hv (0, 1)) 1
    have a3 := congrFun (hv (0, 2)) 2
    simp [R, perm3, masks, toF, mulVec, dotProduct] at a1 a2 a3
    funext d; fin_cases d <;> simp <;> linarith

lemma SA_expand (φ : C → ℝ) : SA φ = φ (true, true, true) + φ (true, false, false) +
    φ (false, true, false) + φ (false, false, true) := by
  simp only [SA]; rw [sum_C]; simp [inA]

lemma SB_expand (φ : C → ℝ) : SB φ = φ (false, false, false) + φ (false, true, true) +
    φ (true, false, true) + φ (true, true, false) := by
  simp only [SB]; rw [sum_C]; simp [inA]; ring

lemma RA_expand (φ : C → ℝ) : RA φ = ![
    φ (true, true, true) + φ (true, false, false) - φ (false, true, false) - φ (false, false, true),
    φ (true, true, true) - φ (true, false, false) + φ (false, true, false) - φ (false, false, true),
    φ (true, true, true) - φ (true, false, false) - φ (false, true, false) + φ (false, false, true)] := by
  funext d; simp only [RA]; rw [sum_C]; fin_cases d <;> simp [inA, pt, cx, cy, cz, sgn] <;> ring

lemma RB_expand (φ : C → ℝ) : RB φ = ![
    -φ (false, false, false) - φ (false, true, true) + φ (true, false, true) + φ (true, true, false),
    -φ (false, false, false) + φ (false, true, true) - φ (true, false, true) + φ (true, true, false),
    -φ (false, false, false) + φ (false, true, true) + φ (true, false, true) - φ (true, true, false)] := by
  funext d; simp only [RB]; rw [sum_C]; fin_cases d <;> simp [inA, pt, cx, cy, cz, sgn] <;> ring

/-- **Theorem 3 (ii), (iii).** `R_A` is injective on TetA's sum-zero amplitudes; `(S_A, R_A)` vanish
exactly on the amplitudes supported on TetB (rank 4 of 8); and on TetA, `w_S = w_{S̄}`. -/
theorem one_root :
    (∀ φ : C → ℝ, SA φ = 0 → RA φ = 0 → ∀ s, inA s = true → φ s = 0) ∧
    (∀ φ : C → ℝ, (SA φ = 0 ∧ RA φ = 0) ↔ ∀ s, inA s = true → φ s = 0) ∧
    (∀ S s, inA s = true → w S s = w (!S.1, !S.2.1, !S.2.2) s) := by
  have inj : ∀ φ : C → ℝ, SA φ = 0 → RA φ = 0 → ∀ s, inA s = true → φ s = 0 := by
    intro φ h0 hR s hs
    rw [SA_expand] at h0; rw [RA_expand] at hR
    have r0 := congrFun hR 0; have r1 := congrFun hR 1; have r2 := congrFun hR 2
    simp at r0 r1 r2
    rcases s with ⟨a, b, c⟩
    cases a <;> cases b <;> cases c <;> simp [inA] at hs <;> linarith
  refine ⟨inj, fun φ => ⟨fun ⟨h0, hR⟩ => inj φ h0 hR, fun h => ⟨?_, ?_⟩⟩, ?_⟩
  · rw [SA_expand]; simp [h, inA]
  · rw [RA_expand]; funext d; fin_cases d <;> simp [h, inA]
  · intro S s hs
    rcases S with ⟨a, b, c⟩; rcases s with ⟨d, e, f⟩
    cases a <;> cases b <;> cases c <;> cases d <;> cases e <;> cases f <;>
      simp [inA] at hs <;> simp [w, cx, cy, cz, sgn]

/-- **Theorem 3 (iv), field closure.** `(S_A, S_B, R_A, R_B)` is injective on all eight corners;
`S_A, S_B` read exactly `1` and `xyz`, `R_A, R_B` exactly the six `T_2` modes. -/
theorem field_closure :
    (∀ φ : C → ℝ, SA φ = 0 → SB φ = 0 → RA φ = 0 → RB φ = 0 → φ = 0) ∧
    (∀ S, grade S = 1 ∨ grade S = 2 → SA (w S) = 0 ∧ SB (w S) = 0) ∧
    (∀ S, grade S = 0 ∨ grade S = 3 → RA (w S) = 0 ∧ RB (w S) = 0) ∧
    SA (w S1) = 4 ∧ SB (w S1) = 4 ∧ SA (w Sxyz) = 4 ∧ SB (w Sxyz) = -4 ∧
    RA (w Sx) = ![4, 0, 0] ∧ RB (w Sx) = ![4, 0, 0] ∧ RA (w Syz) = ![4, 0, 0] ∧
      RB (w Syz) = ![-4, 0, 0] ∧
    RA (w Sy) = ![0, 4, 0] ∧ RB (w Sy) = ![0, 4, 0] ∧ RA (w Sxz) = ![0, 4, 0] ∧
      RB (w Sxz) = ![0, -4, 0] ∧
    RA (w Sz) = ![0, 0, 4] ∧ RB (w Sz) = ![0, 0, 4] ∧ RA (w Sxy) = ![0, 0, 4] ∧
      RB (w Sxy) = ![0, 0, -4] := by
  refine ⟨fun φ hA hB hRA hRB => funext fun s => ?_, fun S hS => ?_, fun S hS => ?_, ?_⟩
  · by_cases hs : inA s
    · exact (one_root.1 φ hA hRA s hs)
    · rw [SB_expand] at hB; rw [RB_expand] at hRB
      have r0 := congrFun hRB 0; have r1 := congrFun hRB 1; have r2 := congrFun hRB 2
      simp at r0 r1 r2
      rcases s with ⟨a, b, c⟩
      cases a <;> cases b <;> cases c <;> simp [inA] at hs <;> simp <;> linarith
  · rcases S with ⟨a, b, c⟩
    cases a <;> cases b <;> cases c <;> simp [grade] at hS <;>
      simp [SA_expand, SB_expand, w, cx, cy, cz, sgn]
  · rcases S with ⟨a, b, c⟩
    cases a <;> cases b <;> cases c <;> simp [grade] at hS <;>
      refine ⟨?_, ?_⟩ <;> simp only [RA_expand, RB_expand] <;> funext d <;> fin_cases d <;>
      simp [w, cx, cy, cz, sgn]
  · simp only [SA_expand, SB_expand, RA_expand, RB_expand]
    refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> simp [w, cx, cy, cz, sgn] <;> norm_num

/-- The TetA share `μ = S_A / (S_A + S_B)`. -/
noncomputable def mu (φ : C → ℝ) : ℝ := SA φ / (SA φ + SB φ)

/-- **`μ` needs both roots.** The TetA-supported amplitude and the constant amplitude have the same
TetA readouts but `μ = 1` and `μ = 1/2`. -/
theorem mu_needs_both :
    let φ1 : C → ℝ := fun s => if inA s then 1 else 0
    let φ2 : C → ℝ := fun _ => 1
    SA φ1 = SA φ2 ∧ RA φ1 = RA φ2 ∧ mu φ1 = 1 ∧ mu φ2 = 1 / 2 := by
  intro φ1 φ2
  refine ⟨?_, ?_, ?_, ?_⟩
  · simp [φ1, φ2, SA_expand, inA]
  · simp [φ1, φ2, RA_expand, inA]
  · simp [mu, φ1, SA_expand, SB_expand, inA]; norm_num
  · simp [mu, φ2, SA_expand, SB_expand]; norm_num

/-! ## Theorem 4: what the oscillator node's closure rule reads -/

/-- The node's Walsh coefficients `c_S = (1/8) Σ_k w_S(s_k) v_k`. -/
noncomputable def coef (S : C) (φ : C → ℝ) : ℝ := (1 / 8) * ∑ s, w S s * φ s

/-- **Theorem 4 (i).** `c_1 = (S_A + S_B)/8`, `c_xyz = (S_A − S_B)/8`, so the node's
`μ = (1 + c_xyz/c_1)/2` is the TetA share `S_A/(S_A + S_B)`; adding any `T_2` mode leaves it
unchanged. -/
theorem node_mu :
    (∀ φ, coef S1 φ = (SA φ + SB φ) / 8) ∧ (∀ φ, coef Sxyz φ = (SA φ - SB φ) / 8) ∧
    (∀ φ, SA φ + SB φ ≠ 0 → (1 + coef Sxyz φ / coef S1 φ) / 2 = mu φ) ∧
    (∀ φ S (c : ℝ), grade S = 1 ∨ grade S = 2 → mu (φ + c • w S) = mu φ) := by
  have h1 : ∀ φ, coef S1 φ = (SA φ + SB φ) / 8 := fun φ => by
    simp only [coef, SA_expand, SB_expand]; rw [sum_C]; simp [w]; ring
  have h2 : ∀ φ, coef Sxyz φ = (SA φ - SB φ) / 8 := fun φ => by
    simp only [coef, SA_expand, SB_expand]; rw [sum_C]; simp [w, cx, cy, cz, sgn]; ring
  refine ⟨h1, h2, fun φ hne => ?_, fun φ S c hS => ?_⟩
  · rw [h1, h2, mu]; field_simp; ring
  · have hA : SA (φ + c • w S) = SA φ := by
      have := (field_closure.2.1 S hS).1
      rw [SA_expand] at this ⊢; rw [SA_expand]; simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
      linear_combination c * this
    have hB : SB (φ + c • w S) = SB φ := by
      have := (field_closure.2.1 S hS).2
      rw [SB_expand] at this ⊢; rw [SB_expand]; simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
      linear_combination c * this
    rw [mu, mu, hA, hB]

/-- **Theorem 4 (ii).** Parseval, `Σ_k v_k² = 8 Σ_S c_S²`; under one common target the spread between
corners contracts by exactly `1 − κ` per step; and the carrier's spectrum is linear in a common
amplitude. -/
theorem node_rule :
    (∀ φ : C → ℝ, ∑ s, φ s ^ 2 = 8 * ∑ S, coef S φ ^ 2) ∧
    (∀ κ T ak aj : ℝ, (ak + κ * (T - ak)) - (aj + κ * (T - aj)) = (1 - κ) * (ak - aj)) ∧
    (∀ (a : ℝ) φ S, coef S (a • φ) = a * coef S φ) := by
  refine ⟨fun φ => ?_, fun κ T ak aj => by ring, fun a φ S => ?_⟩
  · rw [sum_C, sum_C]; simp [coef, sum_C, w, cx, cy, cz, sgn]; ring
  · simp only [coef, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
    exact Finset.sum_congr rfl fun s _ => by ring

/-- **Theorem 4 (iii).** The inward-coupling update `c ← c + κ sign(f b)(1 − |c|)` has the fixed
point `c = 1` whatever the signal; started off it, it moves. -/
theorem inward_fixed (κ σ : ℝ) : (1 : ℝ) + κ * σ * (1 - |(1 : ℝ)|) = 1 ∧
    (κ ≠ 0 → σ ≠ 0 → (1 / 2 : ℝ) + κ * σ * (1 - |(1 / 2 : ℝ)|) ≠ 1 / 2) := by
  refine ⟨by simp, fun hk hs => ?_⟩
  rw [abs_of_pos (by norm_num : (0 : ℝ) < 1 / 2)]
  intro h
  have : κ * σ * (1 / 2) = 0 := by linarith
  simp_all

/-! ## Proposition 3: `μ` and the mixing angle -/

/-- The mode `cos θ · u_A + sin θ · u_B` of the `A_1` block, and the antibonding partner. -/
noncomputable def mode (θ : ℝ) : C → ℝ := Real.cos θ • uA + Real.sin θ • uB
noncomputable def amode (θ : ℝ) : C → ℝ := (-Real.sin θ) • uA + Real.cos θ • uB

lemma SA_uAB (a b : ℝ) : SA (a • uA + b • uB) = 2 * a ∧ SB (a • uA + b • uB) = 2 * b := by
  constructor <;> simp [SA_expand, SB_expand, uA, uB, inA] <;> ring

/-- **Proposition 3, the shares.** For `0 < θ < π/2` the mode's chamber sums are `2 cos θ, 2 sin θ`,
its TetA share is `1/(1 + tan θ)`; the antibonding share `1/(1 − cot θ)` lies outside `[0, 1]`
(for `θ ≠ π/4`, i.e. `tan θ ≠ 1`, where it is undefined). -/
theorem shares (θ : ℝ) (h0 : 0 < θ) (h1 : θ < Real.pi / 2) :
    mu (mode θ) = 1 / (1 + Real.tan θ) ∧
      (Real.tan θ ≠ 1 → mu (amode θ) = 1 / (1 - Real.cos θ / Real.sin θ) ∧
        (mu (amode θ) < 0 ∨ 1 < mu (amode θ))) := by
  have hc : 0 < Real.cos θ := Real.cos_pos_of_mem_Ioo ⟨by linarith, h1⟩
  have hs : 0 < Real.sin θ := Real.sin_pos_of_pos_of_lt_pi h0 (by linarith [Real.pi_pos])
  have hm : mu (mode θ) = Real.cos θ / (Real.cos θ + Real.sin θ) := by
    rw [mu, mode, (SA_uAB _ _).1, (SA_uAB _ _).2]; field_simp
  have ha : mu (amode θ) = -Real.sin θ / (Real.cos θ - Real.sin θ) := by
    rw [mu, amode, (SA_uAB _ _).1, (SA_uAB _ _).2]
    rw [show 2 * -Real.sin θ + 2 * Real.cos θ = 2 * (Real.cos θ - Real.sin θ) by ring]
    rw [mul_div_mul_left _ _ (by norm_num : (2 : ℝ) ≠ 0)]
  refine ⟨?_, fun ht => ?_⟩
  · rw [hm, Real.tan_eq_sin_div_cos]; field_simp
  · have hne : Real.cos θ - Real.sin θ ≠ 0 := by
      intro h; apply ht; rw [Real.tan_eq_sin_div_cos, show Real.sin θ = Real.cos θ by linarith,
        div_self hc.ne']
    refine ⟨?_, ?_⟩
    · rw [ha]
      have : Real.sin θ - Real.cos θ ≠ 0 := fun h => hne (by linarith)
      field_simp
      ring
    · rw [ha]
      rcases lt_or_gt_of_ne hne with h | h
      · right; rw [lt_div_iff_of_neg h]; linarith
      · left; exact div_neg_of_neg_of_pos (by linarith) h

/-- **The mixing condition in `tan θ`.** For `cos θ ≠ 0`, Eq. (3) `(a − c) sin 2θ = 2b cos 2θ` is
`(a − c) tan θ = b (1 − tan² θ)`; for `a ≠ c`, `tan θ ≠ ±1` it is `b/(a − c) = tan θ/(1 − tan² θ)`. -/
theorem mixing_tan (a b c θ : ℝ) (hc : Real.cos θ ≠ 0) :
    ((a - c) * Real.sin (2 * θ) = 2 * b * Real.cos (2 * θ) ↔
      (a - c) * Real.tan θ = b * (1 - Real.tan θ ^ 2)) ∧
    (a ≠ c → 1 - Real.tan θ ^ 2 ≠ 0 →
      ((a - c) * Real.tan θ = b * (1 - Real.tan θ ^ 2) ↔
        b / (a - c) = Real.tan θ / (1 - Real.tan θ ^ 2))) := by
  have e : Real.cos (2 * θ) = Real.cos θ ^ 2 - Real.sin θ ^ 2 := by
    rw [Real.cos_two_mul]; linarith [Real.sin_sq_add_cos_sq θ]
  have key : (a - c) * Real.tan θ - b * (1 - Real.tan θ ^ 2) =
      ((a - c) * Real.sin (2 * θ) - 2 * b * Real.cos (2 * θ)) / (2 * Real.cos θ ^ 2) := by
    rw [Real.sin_two_mul, e, Real.tan_eq_sin_div_cos]; field_simp
  have hc2 : 2 * Real.cos θ ^ 2 ≠ 0 := by positivity
  refine ⟨⟨fun h => ?_, fun h => ?_⟩, fun hac h1 => ?_⟩
  · have : (a - c) * Real.tan θ - b * (1 - Real.tan θ ^ 2) = 0 := by rw [key, h, sub_self, zero_div]
    linarith
  · have h' : ((a - c) * Real.sin (2 * θ) - 2 * b * Real.cos (2 * θ)) / (2 * Real.cos θ ^ 2) = 0 := by
      rw [← key, h, sub_self]
    rcases div_eq_zero_iff.1 h' with h'' | h''
    · linarith
    · exact absurd h'' hc2
  · rw [div_eq_div_iff (sub_ne_zero.2 hac) h1]
    constructor <;> intro h <;> linarith

/-- **Proposition 3 (i), the linear reading.** With `T = tan θ > 0` and `x = g_t/a_0 > 0`: the share
`1/(1 + T)` is `x/(1 + x)` iff `T = 1/x`; equivalently (`T, x ≠ 1`) `T/(1 − T²) = x/(x² − 1)`. The
exchange `x ↦ 1/x` is `μ ↦ 1 − μ` and `θ ↦ π/2 − θ`. -/
theorem linear_reading (T x : ℝ) (hT : 0 < T) (hx : 0 < x) :
    (1 / (1 + T) = x / (1 + x) ↔ T = 1 / x) ∧
    (1 - T ^ 2 ≠ 0 → x ^ 2 - 1 ≠ 0 → (T / (1 - T ^ 2) = x / (x ^ 2 - 1) ↔ T = 1 / x)) ∧
    (1 / x) / (1 + 1 / x) = 1 - x / (1 + x) := by
  refine ⟨?_, fun h1 h2 => ?_, by field_simp; ring⟩
  · rw [div_eq_div_iff (by positivity) (by positivity), eq_div_iff hx.ne']
    constructor <;> intro h <;> linarith
  · rw [div_eq_div_iff h1 h2, eq_div_iff hx.ne']
    constructor
    · intro h
      have : (T * x - 1) * (x + T) = 0 := by linear_combination h
      rcases mul_eq_zero.1 this with h' | h'
      · linarith
      · linarith
    · intro h
      linear_combination (x + T) * h

/-- The exchange `θ ↦ π/2 − θ` inverts `tan θ`. -/
theorem exchange_angle (θ : ℝ) : Real.tan (Real.pi / 2 - θ) = (Real.tan θ)⁻¹ :=
  Real.tan_pi_div_two_sub θ

/-- **Proposition 3 (ii), the parts.** With `x = g_t/a_0`, the TetA part `μ g_t` is
`g_t²/(g_t + a_0)` and the TetB part `(1 − μ) g_t` is `g_t a_0/(g_t + a_0)`. -/
theorem parts (gt a0 : ℝ) (hg : 0 < gt) (ha : 0 < a0) :
    (gt / a0) / (1 + gt / a0) * gt = gt ^ 2 / (gt + a0) ∧
      (1 - (gt / a0) / (1 + gt / a0)) * gt = gt * a0 / (gt + a0) := by
  constructor <;> field_simp <;> ring

/-- **Proposition 3 (iii), the quadratic reading.** The weight share `1/(1 + T²)` is `x/(1 + x)` iff
`T = 1/√x`, and then `T/(1 − T²) = √x/(x − 1)` (`x ≠ 1`). -/
theorem quadratic_reading (T x : ℝ) (hT : 0 < T) (hx : 0 < x) :
    (1 / (1 + T ^ 2) = x / (1 + x) ↔ T = 1 / Real.sqrt x) ∧
    (x ≠ 1 → T = 1 / Real.sqrt x → T / (1 - T ^ 2) = Real.sqrt x / (x - 1)) := by
  have hr : 0 < Real.sqrt x := Real.sqrt_pos.2 hx
  have hrx : Real.sqrt x ^ 2 = x := Real.sq_sqrt hx.le
  have step : 1 / (1 + T ^ 2) = x / (1 + x) ↔ T ^ 2 * x = 1 := by
    rw [div_eq_div_iff (by positivity) (by positivity)]
    constructor <;> intro h <;> linarith
  refine ⟨step.trans ⟨fun h => ?_, fun h => ?_⟩, fun h1 h => ?_⟩
  · rw [eq_div_iff hr.ne']
    have : (T * Real.sqrt x - 1) * (T * Real.sqrt x + 1) = 0 := by
      linear_combination h + T ^ 2 * hrx
    rcases mul_eq_zero.1 this with h' | h'
    · linarith
    · nlinarith
  · rw [h, div_pow, hrx]; field_simp
  · rw [h]
    have hx1 : Real.sqrt x ^ 2 - 1 ≠ 0 := by rw [hrx]; exact sub_ne_zero.2 h1
    rw [show x - 1 = Real.sqrt x ^ 2 - 1 by rw [hrx]]
    generalize Real.sqrt x = r at hr hx1 ⊢
    field_simp

/-- The quadratic reading's share is the chamber weight: `cos²θ/(cos²θ + sin²θ) = 1/(1 + tan²θ)`. -/
theorem weight_share (θ : ℝ) (hc : Real.cos θ ≠ 0) :
    Real.cos θ ^ 2 / (Real.cos θ ^ 2 + Real.sin θ ^ 2) = 1 / (1 + Real.tan θ ^ 2) := by
  rw [Real.tan_eq_sin_div_cos]; field_simp

/-- **Proposition 3 (iv).** The two readings agree only at `x = 1`, where `μ = 1/2`. -/
theorem readings_agree (x : ℝ) (hx : 0 < x) :
    (1 / x = 1 / Real.sqrt x ↔ x = 1) ∧ (1 : ℝ) / (1 + 1) = 1 / 2 := by
  refine ⟨⟨fun h => ?_, fun h => by subst h; simp⟩, by norm_num⟩
  have hr : 0 < Real.sqrt x := Real.sqrt_pos.2 hx
  have hrx : Real.sqrt x ^ 2 = x := Real.sq_sqrt hx.le
  rw [div_eq_div_iff hx.ne' hr.ne', one_mul, one_mul] at h
  have : Real.sqrt x * (Real.sqrt x - 1) = 0 := by linear_combination hrx - h
  rcases mul_eq_zero.1 this with h' | h'
  · linarith
  · rw [← hrx, show Real.sqrt x = 1 by linarith]; norm_num

end WalshEigenmodes

/-! ## Axiom audit -/

#print axioms WalshEigenmodes.walsh_orthogonal
#print axioms WalshEigenmodes.walsh_complete
#print axioms WalshEigenmodes.theorem1
#print axioms WalshEigenmodes.eight_parameters
#print axioms WalshEigenmodes.cube_graph
#print axioms WalshEigenmodes.Td_facts
#print axioms WalshEigenmodes.Td_complete
#print axioms WalshEigenmodes.inversion_exchanges
#print axioms WalshEigenmodes.corners_under_Td
#print axioms WalshEigenmodes.isInv_iff_commute
#print axioms WalshEigenmodes.Hpar_inv
#print axioms WalshEigenmodes.general_inv
#print axioms WalshEigenmodes.walsh_in_chamber_basis
#print axioms WalshEigenmodes.blocks
#print axioms WalshEigenmodes.alike_iff
#print axioms WalshEigenmodes.mixing
#print axioms WalshEigenmodes.lower_grade_weight
#print axioms WalshEigenmodes.tetA_is_frame
#print axioms WalshEigenmodes.schur
#print axioms WalshEigenmodes.Heff_commute
#print axioms WalshEigenmodes.Heff_symm
#print axioms WalshEigenmodes.whole_cube
#print axioms WalshEigenmodes.S_on_walsh
#print axioms WalshEigenmodes.winding_vectors
#print axioms WalshEigenmodes.eigen_orth
#print axioms WalshEigenmodes.vortex_T2
#print axioms WalshEigenmodes.two_standing_waves
#print axioms WalshEigenmodes.RA_eq_frame
#print axioms WalshEigenmodes.frame_equivariant
#print axioms WalshEigenmodes.scalar_invariant
#print axioms WalshEigenmodes.readouts_factor
#print axioms WalshEigenmodes.closure
#print axioms WalshEigenmodes.one_root
#print axioms WalshEigenmodes.field_closure
#print axioms WalshEigenmodes.mu_needs_both
#print axioms WalshEigenmodes.node_mu
#print axioms WalshEigenmodes.node_rule
#print axioms WalshEigenmodes.inward_fixed
#print axioms WalshEigenmodes.shares
#print axioms WalshEigenmodes.mixing_tan
#print axioms WalshEigenmodes.linear_reading
#print axioms WalshEigenmodes.exchange_angle
#print axioms WalshEigenmodes.parts
#print axioms WalshEigenmodes.quadratic_reading
#print axioms WalshEigenmodes.weight_share
#print axioms WalshEigenmodes.readings_agree
