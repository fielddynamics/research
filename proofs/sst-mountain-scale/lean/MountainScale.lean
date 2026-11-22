import KhrononPreferredFrame

/-!
# The Mountain Scale in the SST: the Net-Field Rule From the Action

The picture: a mountain stream is flat close up and a mountain zoomed out. The SST's law term
is read on the mountain's potential `P Φ`, with `P` the projector onto modes longer than the
mountain scale. Its field equation is `L Φ + P (N (P Φ)) = s`, with `L` the Laplacian, `N` the
law's nonlinear flux and `s = 4πGρ`. Because `P` is idempotent and commutes with `L`:

* `mountain_split`: the dimple `Φ − PΦ` obeys `L (Φ − PΦ) = s − P s` (linear: pure TetA, bare
  `G`), and the mountain obeys `P (L (PΦ) + P N(PΦ)) = P s` (the law at the mountain's scale);
* `dimple_blind_to_law`: if `L` is injective, the dimple is the same for every law `N`;
* `energy_split`, `energy_blind_to_law`: the same, needing only that `P` be idempotent and
  self-adjoint in the field-energy product; it need not commute with the Laplacian. This covers
  the sweeping projector, with a different Jacobi radius for each bound system;
* `no_tail_in_dimple`: the dimple's TetB share is zero, while read pointwise the law leaves a
  share strictly between 0 and `a₀` at every finite field (`strong_field_not_pure`).

The projector's properties on a curved leaf, the 1D and 3D solutions, and the numbers for the
mountain scale (Sun, Pal 14, Pal 4) are checked by `verify_sst_mountain_scale.py` and
`demo_mountain_scale.py`.
-/

namespace MountainScale

variable {V : Type*} [AddCommGroup V] [Module ℝ V]

/-- The exact split of the mountain-scale field equation. -/
theorem mountain_split (L P : V →ₗ[ℝ] V) (N : V → V) (Φ s : V)
    (hP : P ∘ₗ P = P) (hc : L ∘ₗ P = P ∘ₗ L) (heq : L Φ + P (N (P Φ)) = s) :
    L (Φ - P Φ) = s - P s ∧ P (L (P Φ) + P (N (P Φ))) = P s := by
  have hPP : ∀ v, P (P v) = P v := fun v => by
    have := LinearMap.congr_fun hP v; simpa using this
  have hLP : ∀ v, L (P v) = P (L v) := fun v => by
    have := LinearMap.congr_fun hc v; simpa using this
  constructor
  · rw [← heq, map_sub, hLP, map_add, hPP]; abel
  · rw [← heq, map_add, map_add, hLP, hPP, hPP]

/-- The dimple does not see the law: two laws, same source, same dimple. -/
theorem dimple_blind_to_law (L P : V →ₗ[ℝ] V) (N₁ N₂ : V → V) (Φ₁ Φ₂ s : V)
    (hP : P ∘ₗ P = P) (hc : L ∘ₗ P = P ∘ₗ L) (hL : Function.Injective L)
    (h₁ : L Φ₁ + P (N₁ (P Φ₁)) = s) (h₂ : L Φ₂ + P (N₂ (P Φ₂)) = s) :
    Φ₁ - P Φ₁ = Φ₂ - P Φ₂ := by
  apply hL
  rw [(mountain_split L P N₁ Φ₁ s hP hc h₁).1, (mountain_split L P N₂ Φ₂ s hP hc h₂).1]

/-- The dimple's own law is linear (`μ = 1`), so its TetB share is zero; read pointwise, the
law leaves a share strictly between 0 and `a₀` (in units of `a₀`, between 0 and 1) at every
finite field: the tail. -/
theorem no_tail_in_dimple (g x : ℝ) (hx : 0 < x) :
    (1 - 1) * g = 0 ∧ 0 < x * (1 - ConstitutiveLaw.law x) ∧ x * (1 - ConstitutiveLaw.law x) < 1 :=
  ⟨by ring, KhrononPreferredFrame.strong_field_not_pure x hx⟩

/-- The split needs less than commuting with the Laplacian. Let `K` be the (invertible) field-energy
operator, `−∇²`, and `P` a projector that is self-adjoint in the energy product, written as
`K (P v) = Pᵀ (K v)` with `Pᵀ` its ordinary adjoint. Then from the field equation
`K Φ + Pᵀ (N (P Φ)) = s` the dimple is `Φ − PΦ = K⁻¹s − P (K⁻¹s)`: fixed by the source alone. The
sweeping projector (each system's mass swept onto its own Jacobi surface) is of this kind and
does not commute with `K`. -/
theorem energy_split (K : V ≃ₗ[ℝ] V) (P Pt : V →ₗ[ℝ] V) (N : V → V) (Φ s : V)
    (hP : P ∘ₗ P = P) (hadj : ∀ v, K (P v) = Pt (K v)) (heq : K Φ + Pt (N (P Φ)) = s) :
    Φ - P Φ = K.symm s - P (K.symm s) := by
  have hPP : ∀ v, P (P v) = P v := fun v => by
    have := LinearMap.congr_fun hP v; simpa using this
  have hinv : ∀ w, K.symm (Pt w) = P (K.symm w) := fun w => by
    apply K.injective; rw [LinearEquiv.apply_symm_apply, hadj, LinearEquiv.apply_symm_apply]
  have hΦ : Φ = K.symm s - P (K.symm (N (P Φ))) := by
    rw [← heq, map_add, LinearEquiv.symm_apply_apply, hinv]; abel
  rw [hΦ]
  simp only [map_sub, hPP]
  abel

/-- With the energy-orthogonal projector, too, the dimple does not see the law. -/
theorem energy_blind_to_law (K : V ≃ₗ[ℝ] V) (P Pt : V →ₗ[ℝ] V) (N₁ N₂ : V → V) (Φ₁ Φ₂ s : V)
    (hP : P ∘ₗ P = P) (hadj : ∀ v, K (P v) = Pt (K v))
    (h₁ : K Φ₁ + Pt (N₁ (P Φ₁)) = s) (h₂ : K Φ₂ + Pt (N₂ (P Φ₂)) = s) :
    Φ₁ - P Φ₁ = Φ₂ - P Φ₂ := by
  rw [energy_split K P Pt N₁ Φ₁ s hP hadj h₁, energy_split K P Pt N₂ Φ₂ s hP hadj h₂]

end MountainScale

#print axioms MountainScale.mountain_split
#print axioms MountainScale.dimple_blind_to_law
#print axioms MountainScale.no_tail_in_dimple
#print axioms MountainScale.energy_split
#print axioms MountainScale.energy_blind_to_law
