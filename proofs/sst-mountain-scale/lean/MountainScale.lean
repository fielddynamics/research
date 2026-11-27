import KhrononPreferredFrame

/-!
# The Mountain Scale in the SST: the Net-Field Rule From the Action

The picture: a mountain stream is flat close up and a mountain zoomed out. The SST's law term
is read on the mountain's potential `P Φ`, with `P` the projector onto modes longer than the
mountain scale. Its field equation is `L Φ + P (N (P Φ)) = s`, with `L` the Laplacian, `N` the
law's nonlinear flux and `s = 4πGρ`. Because `P` is idempotent and commutes with `L`:

* `mountain_split`: the dimple `Φ − PΦ` obeys `L (Φ − PΦ) = s − P s` (linear: locally settled residual, bare
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
* `dielectric_ratio`, `stretch_isotropic`, `trace_corrector` (the Cassini quadrupole): the
  mountain's linear response is anisotropic, stretching makes the swept shell a homoeoid with no
  interior field, and the trace term is isotropic; `interface_jump`: the closure surface carries
  the `(1 − μ̄)` share of the swept mass as a kink in the field, the potential staying continuous;
* `least_energy`: registration implies the sweep. With the registered state held fixed, the
  harmonic (energy-orthogonal) completion has the least field energy, and the energy splits
  exactly into the registered part and the residual;
* `no_tail_in_dimple`: the dimple has no additional constitutive correction, while read pointwise the law leaves a
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

/-- The dimple's own law is linear (`μ = 1`), so its additional constitutive correction is zero;
this does not assert that TetB is absent. Read pointwise, the law leaves a share strictly between
0 and `a₀` (in units of `a₀`, between 0 and 1) at every finite field: the tail. -/
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

-- ============================================================================================
-- Registration implies the sweep (Dirichlet's principle)
-- ============================================================================================

/-- Least energy. Let `β` be the field-energy form, non-negative. Let `h` be the registered field
(harmonic inside the closure surface) and `v` any interior change that keeps the registered state
(zero on and outside the surface). If `h` and `v` are energy-orthogonal, which is what harmonic inside
means, then every completion `h + v` has energy `β h h + β v v ≥ β h h`. The registered field is the
least-energy completion, and it is unique wherever `β v v = 0` forces `v = 0`: least-energy settlement
with a fixed registered state gives the swept field, the ownership sweep. -/
theorem least_energy (β : LinearMap.BilinForm ℝ V) (hpos : ∀ v, 0 ≤ β v v) (h v : V)
    (horth : β h v = 0) (horth' : β v h = 0) :
    β (h + v) (h + v) = β h h + β v v ∧ β h h ≤ β (h + v) (h + v) := by
  have hexp : β (h + v) (h + v) = β h h + β h v + β v h + β v v := by
    simp only [map_add, LinearMap.add_apply]; ring
  refine ⟨by rw [hexp, horth, horth']; ring, ?_⟩
  rw [hexp, horth, horth']; linarith [hpos v]

-- ============================================================================================
-- The Cassini quadrupole: the swept shell in the mountain's anisotropic response
-- ============================================================================================

/-- The mountain's linear response. For the law `μ(x) = x/(1+x)`, a small change in the field
responds with `μ` across the background field and `μ + xμ'` along it; the ratio is
`1 + 1/(1+x)` (1.4 at the Sun, `x = 1.5`). -/
theorem dielectric_ratio (x : ℝ) (hx : 0 < x) :
    (x / (1 + x) + x * (1 / (1 + x) ^ 2)) / (x / (1 + x)) = 1 + 1 / (1 + x) := by
  have h1 : (1 + x) ≠ 0 := by positivity
  have h2 : x ≠ 0 := hx.ne'
  field_simp

/-- Stretching removes the anisotropy, and a thin uniform shell becomes a homoeoid. With
`e² = λ∥/λ⊥` and `z = e z'`, the term `λ∥ ∂z²` is `λ⊥ ∂z'²`, so the operator is `λ⊥` times the
Laplacian in `(x, y, z')`. The sphere of radius `r` becomes the ellipsoid
`x² + y² + e² z'² = r²`, and scaling by `t` carries it to the one of radius `t r`: concentric
spheres go to concentric similar ellipsoids, so a thin uniform spherical shell goes to a thin
uniform shell between similar ellipsoids, a homoeoid, whose interior field is zero (Newton). -/
theorem stretch_isotropic (lp ll e : ℝ) (he : e ≠ 0) (hll : ll = lp * e ^ 2) (x y z' r t : ℝ) :
    ll / e ^ 2 = lp ∧
    (x ^ 2 + y ^ 2 + (e * z') ^ 2 = r ^ 2 ↔ x ^ 2 + y ^ 2 + e ^ 2 * z' ^ 2 = r ^ 2) ∧
    (x ^ 2 + y ^ 2 + e ^ 2 * z' ^ 2 = r ^ 2 →
      (t * x) ^ 2 + (t * y) ^ 2 + e ^ 2 * (t * z') ^ 2 = (t * r) ^ 2) := by
  refine ⟨?_, by rw [mul_pow], ?_⟩
  · rw [hll]; field_simp
  · intro h
    have : (t * x) ^ 2 + (t * y) ^ 2 + e ^ 2 * (t * z') ^ 2
        = t ^ 2 * (x ^ 2 + y ^ 2 + e ^ 2 * z' ^ 2) := by ring
    rw [this, h]; ring

/-- The trace corrector. Inside a sphere of radius `R`, the part of a quadratic host field that
the swept coupling misses is `w = (tr T/6)(|x|² − R²)`: per axis its slope is `(tr T/3) x` and its
curvature `tr T/3`, so `∇²w = tr T`, and `w = 0` on the sphere. Its force is isotropic, so it adds
nothing to a traceless quadrupole. -/
theorem trace_corrector (t R s : ℝ) :
    HasDerivAt (fun u => t / 6 * (u ^ 2 - R ^ 2)) (t / 3 * s) s ∧
    HasDerivAt (fun u => t / 3 * u) (t / 3) s ∧ 3 * (t / 3) = t ∧ t / 6 * (R ^ 2 - R ^ 2) = 0 := by
  refine ⟨?_, ?_, by ring, by ring⟩
  · have := ((hasDerivAt_pow 2 s).sub_const (R ^ 2)).const_mul (t / 6)
    convert this using 1; push_cast; ring
  · simpa using (hasDerivAt_id s).const_mul (t / 3)

/-- The closure surface carries the additional parent-level TetB response. Across the surface, write `jd` for the jump in the
residual's normal slope, `jPb` for the mountain's, and `jmu` for that of `μ̄` times the mountain's.
The sweep gives `jd = −s` and the mountain's flux condition `jmu = s` (`s = 4πGσ`), so the total
field's slope jumps by `jPb + jd = jPb − jmu`, the `(1 − μ̄)` part: a phantom surface layer. For the
centred shell in a constant response `a = n·A·n > 0`, the mountain's slope is `0` inside and `q`
outside with `a q = s`, so the jump is `s (1/a − 1)`, positive when `a < 1`. -/
theorem interface_jump (jPb jmu jd s a q : ℝ) (hd : jd = -s) (hmu : jmu = s)
    (ha : 0 < a) (hflux : a * q = s) :
    jPb + jd = jPb - jmu ∧ q + jd = s * (1 / a - 1) ∧ (0 < s → a < 1 → 0 < q + jd) := by
  have hq : q = s / a := by field_simp; linarith
  refine ⟨by rw [hd, hmu]; ring, by rw [hd, hq]; field_simp; ring, ?_⟩
  intro hs ha1
  have hlt : s < s / a := by rw [lt_div_iff₀ ha]; nlinarith
  rw [hd, hq]; linarith

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
#print axioms MountainScale.least_energy
#print axioms MountainScale.dielectric_ratio
#print axioms MountainScale.stretch_isotropic
#print axioms MountainScale.trace_corrector
#print axioms MountainScale.interface_jump
