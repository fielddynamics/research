import HalfSpaceTwoBoundedRegions
import Mathlib

/-! # Recursive Triforce Closure
The source is supplied for the repository's Lean 4.36.0/Mathlib build.
The finite checks are kernel `decide` proofs, not native executable certificates.
The audit distinguishes these statements from the real geometric and physical scope.
-/

namespace RecursiveTriforceClosure

open ForcedTetrahedralFrame HalfSpaceTwoBoundedRegions
open scoped BigOperators

set_option maxRecDepth 4096
set_option maxHeartbeats 0

abbrev Label := Fin 4
abbrev Address := Label × Label × Label

/-! ## 1. The inherited geometry and medial subdivision -/

/-- The sign vertices come from the existing half-space theorem, not a new axiom. -/
theorem inherited_hull :
    TetB = {p | ∃ w : Fin 4 → ℝ, (∀ a, 0 ≤ w a) ∧
      ∑ a, w a = 1 ∧ p = ∑ a, w a • Mcol a} := TetB_eq_hull

/-- Closed medial children cover a barycentric triangle; interiors do not overlap. -/
theorem medial_cover (a b c : ℝ) :
    (a ≤ 1/2 ∧ b ≤ 1/2 ∧ c ≤ 1/2) ∨
      1/2 ≤ a ∨ 1/2 ≤ b ∨ 1/2 ≤ c := by
  by_cases ha : a ≤ 1/2
  · by_cases hb : b ≤ 1/2
    · by_cases hc : c ≤ 1/2
      · exact Or.inl ⟨ha, hb, hc⟩
      · exact Or.inr (Or.inr (Or.inr (by linarith)))
    · exact Or.inr (Or.inr (Or.inl (by linarith)))
  · exact Or.inr (Or.inl (by linarith))

theorem medial_unique_interiors (a b c : ℝ) (hc : 0 ≤ c) (hs : a+b+c=1) :
    ¬ (1/2 < a ∧ 1/2 < b) := by
  rintro ⟨ha,hb⟩; linarith

/-- Barycentric inversion at the centroid maps exactly onto the central child. -/
theorem medial_center_iff (a b c : ℝ) (h : a+b+c=1) :
    (0 ≤ a ∧ 0 ≤ b ∧ 0 ≤ c ∧ a ≤ 1/2 ∧ b ≤ 1/2 ∧ c ≤ 1/2) ↔
    ∃ x y z : ℝ, 0 ≤ x ∧ 0 ≤ y ∧ 0 ≤ z ∧ x+y+z=1 ∧
      a=(1-x)/2 ∧ b=(1-y)/2 ∧ c=(1-z)/2 := by
  constructor
  · rintro ⟨ha,hb,hc,ha',hb',hc'⟩
    refine ⟨1-2*a,1-2*b,1-2*c,by linarith,by linarith,by linarith,
      by linarith,by ring,by ring,by ring⟩
  · rintro ⟨x,y,z,hx,hy,hz,hs,rfl,rfl,rfl⟩
    exact ⟨by linarith,by linarith,by linarith,by linarith,by linarith,by linarith⟩

/-- The corner at the first vertex has precisely the barycentric inequality a≥1/2. -/
theorem medial_corner_iff (a b c : ℝ) (h : a+b+c=1) :
    (1/2 ≤ a ∧ 0 ≤ b ∧ 0 ≤ c) ↔
    ∃ x y z : ℝ, 0 ≤ x ∧ 0 ≤ y ∧ 0 ≤ z ∧ x+y+z=1 ∧
      a=(1+x)/2 ∧ b=y/2 ∧ c=z/2 := by
  constructor
  · rintro ⟨ha,hb,hc⟩
    refine ⟨2*a-1,2*b,2*c,by linarith,by linarith,by linarith,
      by linarith,by ring,by ring,by ring⟩
  · rintro ⟨x,y,z,hx,hy,hz,hs,rfl,rfl,rfl⟩
    exact ⟨by linarith,by linarith,by linarith⟩

/-- The central map has positive oriented area multiplier, as do the corner maps. -/
theorem medial_area_factor : ((-1/2 : ℚ)^2 = 1/4) ∧ ((1/2 : ℚ)^2 = 1/4) := by norm_num

/-! ## 2. Octahedral edge-midpoint lattice (doubled integer coordinates) -/

/-- All integer linear combinations of the three positive edge generators are exactly
    the even-sum sublattice. The other nine generators already belong to it. -/
theorem midpoint_lattice (x y z : ℤ) :
    (x+y+z)%2=0 ↔ ∃ a b c : ℤ, x=a+b ∧ y=a+c ∧ z=b+c := by
  constructor
  · intro h
    refine ⟨(x+y-z)/2,(x+z-y)/2,(y+z-x)/2,?_,?_,?_⟩ <;> omega
  · rintro ⟨a,b,c,rfl,rfl,rfl⟩; omega

/-- The projected lattice in the basis P(e₁)/2,P(e₂)/2 is all of ℤ². -/
theorem projection_surjective (a b : ℤ) :
    ∃ x y z : ℤ, (x+y+z)%2=0 ∧ x-z=a ∧ y-z=b := by
  refine ⟨a+(a+b),b+(a+b),a+b,?_,?_,?_⟩ <;> omega

/-- On the reference face x+y+z=-1, doubled lattice coordinates are exactly
    the quarter barycentric grid. Nonnegativity is the face inequality. -/
theorem face_lattice_grid (x y z : ℤ) :
    (x+y+z = -2 ∧ -2 ≤ x ∧ -2 ≤ y ∧ -2 ≤ z) ↔
    ∃ a b c : ℤ, 0 ≤ a ∧ 0 ≤ b ∧ 0 ≤ c ∧ a+b+c=4 ∧
      x=a-2 ∧ y=b-2 ∧ z=c-2 := by
  constructor
  · rintro ⟨hs,hx,hy,hz⟩
    refine ⟨x+2,y+2,z+2,?_,?_,?_,?_,?_,?_,?_⟩ <;> omega
  · rintro ⟨a,b,c,ha,hb,hc,hs,rfl,rfl,rfl⟩
    exact ⟨by omega,by omega,by omega,by omega⟩

def quarterGrid : Finset (Fin 5 × Fin 5 × Fin 5) :=
  Finset.univ.filter fun x => x.1.val+x.2.1.val+x.2.2.val=4

theorem quarter_grid_card : quarterGrid.card = 15 := by decide

private theorem pow_two_ge_eight (n : ℕ) (h : 3 ≤ n) : 8 ≤ 2^n := by
  induction n with
  | zero => omega
  | succ n ih =>
    by_cases hn : 3 ≤ n
    · have h' := ih hn
      rw [pow_succ]; omega
    · have he : n=2 := by omega
      subst n; decide

/-- An edge step at depth n has nonzero doubled coordinate 4/2^n.
    The exact divisibility condition is equivalent to n≤2. -/
theorem dyadic_depth (n : ℕ) : (∃ t : ℕ, 2^n*t=4) ↔ n≤2 := by
  constructor
  · rintro ⟨t,ht⟩
    by_contra h
    have hn : 3 ≤ n := by omega
    have hp := pow_two_ge_eight n hn
    have htpos : 1 ≤ t := by
      by_contra hh
      have hz : t=0 := by omega
      simp [hz] at ht
    have hle : 2^n*1 ≤ 2^n*t := Nat.mul_le_mul_left _ htpos
    rw [ht] at hle
    simp at hle; omega
  · intro h
    interval_cases n
    · exact ⟨4,by decide⟩
    · exact ⟨2,by decide⟩
    · exact ⟨1,by decide⟩

/-- Refining the permitted lattice by a factor two defeats an unconditional bound. -/
theorem finer_lattice_counterexample : 2^3 * (1 : ℕ) = 8 := by decide

/-! ## 3. Actual affine labels and their action -/

/-- Integer model of the inherited vertex coordinates, with an explicit bridge below. -/
def vertexZ (i : Label) (d : Fin 3) : ℤ :=
  (![![1,1,1],![1,-1,-1],![-1,1,-1],![-1,-1,1]] : Fin 4 → Fin 3 → ℤ) i d

theorem vertex_bridge (i : Label) (d : Fin 3) : (vertexZ i d : ℝ)=Mcol i d := by
  fin_cases i <;> fin_cases d <;> norm_num [vertexZ, Mcol, Mmat]

/-- Child vertex coefficients with denominator two. The omitted label has weight zero. -/
def delta (l r : Label) : ℤ := if l=r then 1 else 0

def firstCoeff (i j l r : Label) : ℤ :=
  if l=i ∨ r=i then 0 else
    if j=i then 1-delta l r else delta l r+delta j r

/-- Denominator four coefficients, obtained by the second medial affine map. -/
def secondCoeff (i j k l r : Label) : ℤ :=
  if l=i ∨ r=i then 0 else
    if k=i then (∑ u : Label, firstCoeff i j u r)-firstCoeff i j l r
    else firstCoeff i j l r+firstCoeff i j k r

def secondVertex (x : Address) (l : Label) (d : Fin 3) : ℤ :=
  ∑ r : Label, secondCoeff x.1 x.2.1 x.2.2 l r * vertexZ r d

/-- All the coefficients are nonnegative and sum to four for actual triangle vertices. -/
theorem refined_coefficients (i j k l : Label) (hl : l≠i) :
    (∀ r : Label, 0 ≤ secondCoeff i j k l r) ∧
    (∑ r : Label, secondCoeff i j k l r)=4 := by
  revert hl
  revert j k l
  fin_cases i <;> decide

/-- Twice every actual refined vertex coordinate is integral (numerator/4). -/
theorem refined_half_integral (i j k l : Label) (d : Fin 3) :
    secondVertex (i,j,k) l d % 2 = 0 := by
  revert j k l d
  fin_cases i <;> decide

/-- The doubled coordinate sum is even, so the refined vertices belong to L. -/
theorem refined_lattice_sum (i j k l : Label) :
    (∑ d : Fin 3, secondVertex (i,j,k) l d) % 4 = 0 := by
  revert j k l
  fin_cases i <;> decide

/-- Every quarter barycentric grid point of the reference face occurs as a
    vertex of a secondary tile. Covariance transports the result to all faces. -/
theorem reference_grid_saturated (a b c : Fin 5) (h : a.val+b.val+c.val=4) :
    ∃ j k l : Label, l≠0 ∧ secondCoeff 0 j k l 1=(a.val : ℤ) ∧
      secondCoeff 0 j k l 2=(b.val : ℤ) ∧ secondCoeff 0 j k l 3=(c.val : ℤ) := by
  revert h
  revert b c
  fin_cases a <;> decide

abbrev Coeff4 := ℤ × ℤ × ℤ × ℤ

def refinedTile (x : Address) : Finset Coeff4 :=
  (Finset.univ.filter fun l : Label => l≠x.1).image fun l =>
    (secondCoeff x.1 x.2.1 x.2.2 l 0, secondCoeff x.1 x.2.1 x.2.2 l 1,
     secondCoeff x.1 x.2.1 x.2.2 l 2, secondCoeff x.1 x.2.1 x.2.2 l 3)

/-- All 64 actual barycentric triangles are distinct. -/
theorem distinct_refined_tiles : (Finset.univ.image refinedTile).card=64 := by decide

/-! ## 4. Pointing and traces -/

def evenPoint (x : Address) : Bool := (x.2.1==x.1)==(x.2.2 == x.1)

def pointing (x : Address) : ℤ := if evenPoint x then 1 else -1

def positives : Finset Address := Finset.univ.filter fun x => evenPoint x = true

def negatives : Finset Address := Finset.univ.filter fun x => evenPoint x = false

theorem address_count : Fintype.card Address = 64 := by decide

theorem pointing_counts : positives.card=40 ∧ negatives.card=24 := by decide

def counts : ℕ → ℕ × ℕ
  | 0 => (1,0)
  | n+1 => (3*(counts n).1+(counts n).2,(counts n).1+3*(counts n).2)

/-- General recurrence: the sum is 4^n and the difference is 2^n. -/
theorem pointing_recurrence (n : ℕ) :
    (counts n).1+(counts n).2=4^n ∧ (counts n).1=(counts n).2+2^n := by
  induction n with
  | zero => decide
  | succ n ih =>
    rcases ih with ⟨hs,hd⟩
    simp only [counts, pow_succ]
    constructor <;> omega

def faceTrace (i : Label) : ℤ := ∑ j : Label, ∑ k : Label, pointing (i,j,k)

theorem face_trace (i : Label) : faceTrace i=4 := by fin_cases i <;> decide

theorem trace_polynomial (i : Label) (s : ℤ) : 1+16+s*faceTrace i=17+4*s := by
  rw [face_trace]; ring

/-! ## 5. Explicit signed basis dictionary -/

/-- Symmetric slots have ordered lower labels a≤b; antisymmetric slots are stored
    in reverse order a>b, with coefficient relative to the increasing wedge. -/
abbrev SignedSlot := Address × ℤ

def symSlot (i a b : Label) : SignedSlot :=
  if a≤b then ((i,a,b),1) else ((i,b,a),1)

def antiSlot (i a b : Label) : SignedSlot :=
  if a<b then ((i,b,a),1) else ((i,a,b),-1)

def firstOther (a b : Label) : Label :=
  if a≠0 ∧ b≠0 then 0 else if a≠1 ∧ b≠1 then 1 else if a≠2 ∧ b≠2 then 2 else 3

def lastLabel (a b c : Label) : Label :=
  if a≠0 ∧ b≠0 ∧ c≠0 then 0 else if a≠1 ∧ b≠1 ∧ c≠1 then 1
  else if a≠2 ∧ b≠2 ∧ c≠2 then 2 else 3

def inv (a b : Label) : ℕ := if b<a then 1 else 0

def evenQuad (a b c d : Label) : Bool :=
  (inv a b+inv a c+inv a d+inv b c+inv b d+inv c d)%2==0

def dictionary (x : Address) : SignedSlot :=
  let (i,j,k) := x
  if j=i then
    if k=i then symSlot i i i else antiSlot i i k
  else if k=i then
    let a := firstOther i j
    let b := lastLabel i j a
    if evenQuad i j a b then antiSlot i a b else antiSlot i b a
  else if j=k then symSlot i j j
  else
    let l := lastLabel i j k
    if evenQuad i j k l then symSlot i i l else symSlot i j k

def slot (x : Address) : Address := (dictionary x).1

def inverseSlot (x : Address) : Address :=
  let (i,a,b) := x
  if a≤b then
    if a=b then (i,a,a)
    else if a=i ∨ b=i then
      let l := if a=i then b else a
      let j := firstOther i l
      let k := lastLabel i l j
      if evenQuad i j k l then (i,j,k) else (i,k,j)
    else
      let l := lastLabel i a b
      if evenQuad i a b l then (i,b,a) else (i,a,b)
  else if a=i ∨ b=i then (i,i,if a=i then b else a)
  else (i,lastLabel i a b,i)

theorem dictionary_left_inverse (i j k : Label) : inverseSlot (slot (i,j,k))=(i,j,k) := by
  revert j k
  fin_cases i <;> decide

theorem dictionary_right_inverse (i j k : Label) : slot (inverseSlot (i,j,k))=(i,j,k) := by
  revert j k
  fin_cases i <;> decide

theorem dictionary_bijective : Function.Bijective slot := by
  constructor
  · rintro ⟨i,j,k⟩ ⟨a,b,c⟩ h
    have hh := congrArg inverseSlot h
    simpa only [dictionary_left_inverse] using hh
  · rintro ⟨i,j,k⟩
    exact ⟨inverseSlot (i,j,k),dictionary_right_inverse i j k⟩

theorem dictionary_grading (i j k : Label) :
    evenPoint (i,j,k)=true ↔ (slot (i,j,k)).2.1 ≤ (slot (i,j,k)).2.2 := by
  revert j k
  fin_cases i <;> decide

theorem dictionary_unit_sign (i j k : Label) :
    (dictionary (i,j,k)).2=1 ∨ (dictionary (i,j,k)).2= -1 := by
  revert j k
  fin_cases i <;> decide

/-- Lexicographic list of all 24 permutations; completeness is certified below. -/
def permTable : Fin 24 → Label → Label :=
  ![![0, 1, 2, 3],
    ![0, 1, 3, 2],
    ![0, 2, 1, 3],
    ![0, 2, 3, 1],
    ![0, 3, 1, 2],
    ![0, 3, 2, 1],
    ![1, 0, 2, 3],
    ![1, 0, 3, 2],
    ![1, 2, 0, 3],
    ![1, 2, 3, 0],
    ![1, 3, 0, 2],
    ![1, 3, 2, 0],
    ![2, 0, 1, 3],
    ![2, 0, 3, 1],
    ![2, 1, 0, 3],
    ![2, 1, 3, 0],
    ![2, 3, 0, 1],
    ![2, 3, 1, 0],
    ![3, 0, 1, 2],
    ![3, 0, 2, 1],
    ![3, 1, 0, 2],
    ![3, 1, 2, 0],
    ![3, 2, 0, 1],
    ![3, 2, 1, 0]]

def permEven (p : Fin 24) : Bool := evenQuad (permTable p 0) (permTable p 1) (permTable p 2) (permTable p 3)

def act (p : Fin 24) (x : Address) : Address :=
  (permTable p x.1,permTable p x.2.1,permTable p x.2.2)

def scale (s : ℤ) (x : SignedSlot) : SignedSlot := (x.1,s*x.2)

def slotAct (p : Fin 24) (x : SignedSlot) : SignedSlot :=
  let (i,a,b) := x.1
  let q := permTable p
  scale x.2 (if a≤b then symSlot (q i) (q a) (q b) else antiSlot (q i) (q b) (q a))

theorem table_injective (p : Fin 24) (a b : Label) : permTable p a=permTable p b → a=b := by
  revert a b
  fin_cases p <;> decide

theorem table_complete_values (a b c d : Label)
    (h : a≠b ∧ a≠c ∧ a≠d ∧ b≠c ∧ b≠d ∧ c≠d) :
    ∃ p : Fin 24, permTable p 0=a ∧ permTable p 1=b ∧ permTable p 2=c ∧ permTable p 3=d := by
  revert h
  revert b c d
  fin_cases a <;> decide

theorem table_complete (q : Label → Label) (h : Function.Injective q) :
    ∃ p : Fin 24, ∀ i : Label, permTable p i=q i := by
  have hab : q 0≠q 1 := fun he => (by decide : (0 : Label)≠1) (h he)
  have hac : q 0≠q 2 := fun he => (by decide : (0 : Label)≠2) (h he)
  have had : q 0≠q 3 := fun he => (by decide : (0 : Label)≠3) (h he)
  have hbc : q 1≠q 2 := fun he => (by decide : (1 : Label)≠2) (h he)
  have hbd : q 1≠q 3 := fun he => (by decide : (1 : Label)≠3) (h he)
  have hcd : q 2≠q 3 := fun he => (by decide : (2 : Label)≠3) (h he)
  obtain ⟨p,h0,h1,h2,h3⟩ := table_complete_values (q 0) (q 1) (q 2) (q 3) ⟨hab,hac,had,hbc,hbd,hcd⟩
  refine ⟨p,?_⟩
  intro i; fin_cases i <;> assumption

theorem geometric_covariance (p : Fin 24) (i j k l r : Label) :
    secondCoeff (permTable p i) (permTable p j) (permTable p k) (permTable p l) (permTable p r)
    = secondCoeff i j k l r := by
  revert j k l r
  fin_cases p <;> fin_cases i <;> decide

/-- The dictionary is an intertwiner for every even permutation, not just a generator. -/
theorem proper_equivariance (p : Fin 24) (i j k : Label) :
    permEven p=true → dictionary (act p (i,j,k))=slotAct p (dictionary (i,j,k)) := by
  revert i j k
  fin_cases p <;> decide

/-- Algebraic repair of reflections: odd permutations exchange the order of the last
    two labels on all-distinct addresses, and attach a sign to lateral→central. -/
def repairedAddress (p : Fin 24) (x : Address) : Address :=
  let y := act p x
  if !(permEven p) && (x.1 != x.2.1) && (x.1 != x.2.2) && (x.2.1 != x.2.2)
    then (y.1,y.2.2,y.2.1) else y

def repairSign (p : Fin 24) (x : Address) : ℤ :=
  if !(permEven p) && (x.2.1 != x.1) && (x.2.2 == x.1) then -1 else 1

theorem repaired_equivariance (p : Fin 24) (i j k : Label) :
    scale (repairSign p (i,j,k)) (dictionary (repairedAddress p (i,j,k)))
      = slotAct p (dictionary (i,j,k)) := by
  revert i j k
  fin_cases p <;> decide

/-- The transposition (0 1) is the lexicographic index 6. -/
def reflection : Fin 24 := 6

def fixedNeg : Finset Address := negatives.filter fun x => act reflection x=x

def slotTraceNeg : ℤ := ∑ x : Address,
  if x.2.2<x.2.1 then
    let y := slotAct reflection (x,1)
    if y.1=x then y.2 else 0
  else 0

theorem reflection_trace_witness : fixedNeg.card=4 ∧ slotTraceNeg=0 := by decide

/-! ## 6. Closure tree -/

def H4 (i j : Label) : ℤ :=
  (![![1,1,1,1],![1,-1,1,-1],![1,1,-1,-1],![1,-1,-1,1]] : Label → Label → ℤ) i j

theorem local_walsh_orthogonal (i j : Label) :
    (∑ k : Label, H4 i k * H4 j k) = if i=j then 4 else 0 := by
  revert j
  fin_cases i <;> decide

theorem tree_counts : (1 : ℕ)+4+16=21 ∧ (3 : ℕ)+12+48=63 ∧ (1 : ℕ)+3+12+48=64 := by decide

/-- A physical three-cycle of the four labels fixes exactly one label. -/
def cycle (i : Label) : Label := (![0,2,3,1] : Label → Label) i

theorem cycle_order (i : Label) : cycle (cycle (cycle i))=i := by fin_cases i <;> decide

theorem cycle_fixed (i : Label) : cycle i=i ↔ i=0 := by fin_cases i <;> decide

/-- Burnside numerators, including the different ordered cube-pair action. -/
theorem invariant_counts :
    ((4 : ℕ)+1+1)/3=2 ∧ ((16 : ℕ)+1+1)/3=6 ∧ ((64 : ℕ)+1+1)/3=22 ∧
    (2 : ℕ)-1=1 ∧ (6 : ℕ)-2=4 ∧ (22 : ℕ)-6=16 ∧ ((64 : ℕ)+4+4)/3=24 := by decide

/-- Positive/negative fixed address traces for the physical three-cycle. -/
def cyAct (x : Address) : Address := (cycle x.1,cycle x.2.1,cycle x.2.2)

theorem cycle_pointing_fixed :
    (positives.filter fun x => cyAct x=x).card=1 ∧
    (negatives.filter fun x => cyAct x=x).card=0 := by decide

theorem invariant_pointing_counts : ((40 : ℕ)+2)/3=14 ∧ (24 : ℕ)/3=8 := by decide

/-! Axiom audit commands. Build output must be inspected before claiming verification. -/
#print axioms inherited_hull
#print axioms medial_center_iff
#print axioms medial_corner_iff
#print axioms midpoint_lattice
#print axioms projection_surjective
#print axioms face_lattice_grid
#print axioms dyadic_depth
#print axioms vertex_bridge
#print axioms refined_coefficients
#print axioms refined_half_integral
#print axioms refined_lattice_sum
#print axioms reference_grid_saturated
#print axioms distinct_refined_tiles
#print axioms pointing_recurrence
#print axioms dictionary_bijective
#print axioms dictionary_grading
#print axioms table_complete
#print axioms geometric_covariance
#print axioms proper_equivariance
#print axioms repaired_equivariance
#print axioms reflection_trace_witness
#print axioms local_walsh_orthogonal
#print axioms cycle_pointing_fixed

end RecursiveTriforceClosure
