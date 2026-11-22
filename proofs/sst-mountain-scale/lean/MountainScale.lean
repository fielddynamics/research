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
* `ownership_split`, `ownership_blind_to_law`: the form the paper uses. Each system sweeps its
  own mass onto its own closure sphere, spheres may overlap, and the mountain `Φ − d` solves the plain
  law on the swept source while the systems' own fields `d` are the same for every law;
* `four_ports`: a field object meets the NET Field through one temporal channel (the lapse) and
  three spatial ones (its centre of mass), plus a tidal term;
* `faces_read_ports`, `nested_telescope` (Paper VII, Section IX): read at an envelope's four face
  directions, a host field gives its clock rate (plus the mean density inside) and free fall,
  with a chiral tidal leak that TetA and TetB carry with opposite signs and the stellated
  octahedron cancels; nested envelopes telescope;
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

-- ============================================================================================
-- The ownership form: each system sweeps its own mass onto its own closure sphere
-- ============================================================================================

/-- The ownership split. Let `d` be the systems' own interior fields, fixed by their own mass:
`K d = s − s̄`, where `s̄` is the source with every system's mass swept onto its own closure
sphere. If the field solves `K Φ + N (Φ − d) = s` (the law's term reads the mountain `Φ − d`), then
the mountain solves the plain law on the swept source, `K (Φ − d) + N (Φ − d) = s̄`, and the field is
the mountain plus `d`, whatever the law `N` is. Spheres may overlap: nothing here asks the systems'
regions to be disjoint. -/
theorem ownership_split (K : V →ₗ[ℝ] V) (N : V → V) (Φ d s sbar : V)
    (hd : K d = s - sbar) (heq : K Φ + N (Φ - d) = s) :
    K (Φ - d) + N (Φ - d) = sbar := by
  rw [map_sub, hd, sub_add_eq_add_sub, heq]; abel

/-- Two laws, same matter: the fields differ only in their mountains; the systems' own interior
fields `d` are shared. -/
theorem ownership_blind_to_law (K : V →ₗ[ℝ] V) (N₁ N₂ : V → V) (Φ₁ Φ₂ d s sbar : V)
    (hd : K d = s - sbar) (h₁ : K Φ₁ + N₁ (Φ₁ - d) = s) (h₂ : K Φ₂ + N₂ (Φ₂ - d) = s) :
    K (Φ₁ - d) + N₁ (Φ₁ - d) = sbar ∧ K (Φ₂ - d) + N₂ (Φ₂ - d) = sbar ∧
    Φ₁ - (Φ₁ - d) = Φ₂ - (Φ₂ - d) :=
  ⟨ownership_split K N₁ Φ₁ d s sbar hd h₁, ownership_split K N₂ Φ₂ d s sbar hd h₂, by abel⟩

/-- The four ports. A field object of point masses `m i` at `p i`, with its centre of mass at the
origin, in a NET Field `c₀ + b ⬝ x + q x` (`q` the tidal part): its interaction is `M c₀` (one
temporal channel, the lapse) plus the tidal part; the three spatial channels `b` act on its centre of
mass only, since the dipole term vanishes there. -/
theorem four_ports {n : ℕ} (m : Fin n → ℝ) (p : Fin n → Fin 3 → ℝ)
    (hcom : ∑ i, m i • p i = 0) (c₀ : ℝ) (b : Fin 3 → ℝ) (q : (Fin 3 → ℝ) → ℝ) :
    ∑ i, m i * (c₀ + b ⬝ᵥ p i + q (p i)) = (∑ i, m i) * c₀ + ∑ i, m i * q (p i) := by
  have hdip : ∑ i, m i * (b ⬝ᵥ p i) = 0 := by
    have : ∑ i, m i * (b ⬝ᵥ p i) = b ⬝ᵥ (∑ i, m i • p i) := by
      rw [dotProduct_sum]; congr 1; ext i; rw [dotProduct_smul, smul_eq_mul]
    rw [this, hcom, dotProduct_zero]
  simp only [mul_add, Finset.sum_add_distrib, hdip, Finset.sum_mul, add_zero]

-- ============================================================================================
-- The faces read the ports (Paper VII, Section IX)
-- ============================================================================================

/-- A host field near an envelope's centre: `c₀ + b ⬝ v + (1/2) vᵀ T v`, with `T` any symmetric
matrix, written in components. Inside an envelope the mountain need not be harmonic:
`tr T = 4πG (ρ_diffuse + ρ_TetB)` there. -/
noncomputable def hostField (c₀ b₁ b₂ b₃ t₁₁ t₁₂ t₁₃ t₂₂ t₂₃ t₃₃ : ℝ) (v₁ v₂ v₃ : ℝ) : ℝ :=
  c₀ + b₁ * v₁ + b₂ * v₂ + b₃ * v₃ +
    (t₁₁ * v₁ ^ 2 + t₂₂ * v₂ ^ 2 + t₃₃ * v₃ ^ 2 +
      2 * t₁₂ * v₁ * v₂ + 2 * t₁₃ * v₁ * v₃ + 2 * t₂₃ * v₂ * v₃) / 2

/-- Read at TetA's four face directions `(1,1,1), (1,−1,−1), (−1,1,−1), (−1,−1,1)`, the host
field's sum is `4c₀ + 2 tr T` (the temporal port, plus the mean density inside; the trace vanishes
only where the mountain is harmonic), and its face-weighted sum is `4b + 4(T₂₃, T₁₃, T₁₂)` (the three
spatial ports, with a chiral leak of the tide; the trace does not enter). TetB's directions are the
negatives: the same sum, and the leak with the opposite sign. Both together, the stellated
octahedron's eight cube corners, read `8c₀ + 4 tr T` and `8b`: the leak cancels. -/
theorem faces_read_ports (c₀ b₁ b₂ b₃ t₁₁ t₁₂ t₁₃ t₂₂ t₂₃ t₃₃ : ℝ) :
    let F := hostField c₀ b₁ b₂ b₃ t₁₁ t₁₂ t₁₃ t₂₂ t₂₃ t₃₃
    -- TetA
    F 1 1 1 + F 1 (-1) (-1) + F (-1) 1 (-1) + F (-1) (-1) 1 = 4 * c₀ + 2 * (t₁₁ + t₂₂ + t₃₃) ∧
    F 1 1 1 + F 1 (-1) (-1) - F (-1) 1 (-1) - F (-1) (-1) 1 = 4 * b₁ + 4 * t₂₃ ∧
    F 1 1 1 - F 1 (-1) (-1) + F (-1) 1 (-1) - F (-1) (-1) 1 = 4 * b₂ + 4 * t₁₃ ∧
    F 1 1 1 - F 1 (-1) (-1) - F (-1) 1 (-1) + F (-1) (-1) 1 = 4 * b₃ + 4 * t₁₂ ∧
    -- TetB
    F (-1) (-1) (-1) + F (-1) 1 1 + F 1 (-1) 1 + F 1 1 (-1) = 4 * c₀ + 2 * (t₁₁ + t₂₂ + t₃₃) ∧
    -(F (-1) (-1) (-1)) - F (-1) 1 1 + F 1 (-1) 1 + F 1 1 (-1) = 4 * b₁ - 4 * t₂₃ ∧
    -- the stellated octahedron: the leak cancels
    (F 1 1 1 + F 1 (-1) (-1) - F (-1) 1 (-1) - F (-1) (-1) 1) +
      (-(F (-1) (-1) (-1)) - F (-1) 1 1 + F 1 (-1) 1 + F 1 1 (-1)) = 8 * b₁ := by
  simp only [hostField]
  refine ⟨by ring, by ring, by ring, by ring, by ring, by ring, by ring⟩

/-- Nested envelopes telescope. If sweeping onto an inner envelope and then onto an outer one equals
sweeping straight onto the outer one (`Bₖ (Bⱼ ρ) = Bₖ ρ`), the system's own source is the inner
envelope's own source plus the shell-to-shell source, and the mountain sees only the outer shell. -/
theorem nested_telescope (Bj Bk : V →ₗ[ℝ] V) (ρ : V) (hnest : Bk (Bj ρ) = Bk ρ) :
    ρ - Bk ρ = (ρ - Bj ρ) + (Bj ρ - Bk (Bj ρ)) := by
  rw [hnest]; abel

end MountainScale

#print axioms MountainScale.mountain_split
#print axioms MountainScale.dimple_blind_to_law
#print axioms MountainScale.no_tail_in_dimple
#print axioms MountainScale.energy_split
#print axioms MountainScale.energy_blind_to_law
#print axioms MountainScale.ownership_split
#print axioms MountainScale.ownership_blind_to_law
#print axioms MountainScale.four_ports
#print axioms MountainScale.faces_read_ports
#print axioms MountainScale.nested_telescope
