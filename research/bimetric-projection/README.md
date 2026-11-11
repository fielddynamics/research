# Does the locked bimetric potential project onto μ(x) = x/(x+1)?

*Working note, Field Dynamics Research, 2026-11-11. Status: computation, not a paper. Verification: `python3 verify_bimetric_projection.py` (23/23 checks pass, about 50 s; numpy, scipy, sympy).*

## Question

Papers VIII, IX, XII and the Tully–Fisher manuscript state that the Hassan–Rosen (HR) bimetric theory with the locked coefficients β = (1, 0, 16, 0, 1) and the GFD scalar–tensor action (the SST) are "two projections of one geometry". At galactic scales, the locked bimetric theory should then reduce to the constitutive law μ(x) = x/(x+1), with x = g/a₀. Paper VIII states that this match is an open, checkable problem. This note does the check in the standard way: the decoupling limit and the static, spherically symmetric weak field.

## Result in one paragraph

The locked bimetric theory does not reduce to μ(x) = x/(x+1). Around a static mass, its static weak-field response is fixed by one combination, M_enc/r³. It never depends on M_enc/r², which is the combination an acceleration law g/a₀ needs. The extra force it adds is bounded: g_tot/g_N stays between 1 and 4/3 in the linear regime, and below 1.71 on any solution branch. There is no regime in which g_tot/g_N grows without bound as g_N → 0, which is what μ(x) → x (the deep field and flat rotation curves) requires. The lock does fix several things exactly: the background, the Fierz–Pauli mass, the absence of the irreducible quartic mixing, and a screening cubic with integer coefficients. But the potential has no derivatives, and its helicity-0 sector is Galileon/Vainshtein. That structure cannot produce an acceleration-scale law. So the SST's F(y) cannot be a projection of this potential. If the two are one theory, the a₀ physics has to come from a sector Hassan–Rosen does not have.

## What was computed

**A. Variation of the potential.** By finite differences on random g, f and β:

  ∂(√−g Σβₙeₙ(X))/∂g_{μν} = ½√−g Σₙ(−1)ⁿβₙ (Yₙ(X) g⁻¹)^{μν}, with X = √(g⁻¹f) and Yₙ(X) = Σₖ(−1)ᵏ eₖ(X) X^{n−k}.

This is the standard HR equation of motion, checked rather than assumed.

**B. Background and spectrum of the locked set.**
- A proportional background f = c²g requires α²(1+48c²) = c² + 48, with α = M_f/M_g. So c² = (48 − α²)/(48α² − 1), which is real for 1/48 < α² < 48.
- The effective cosmological constant is Λ_g = m²(1 + 48c²), i.e. 49m² at c = 1. Flat space is not a solution: the locked set always carries a cosmological term of order the graviton mass scale.
- By direct quadratic expansion, the mass term has exactly the Fierz–Pauli form, with β₁c + 2β₂c² + β₃c³ = 32c². So m_FP² = 32m²c²(1 + 1/(α²c²)).
- Higuchi bound: m_FP²/H² − 2 = 4606c²/((c²+48)(48c²+1)) > 0 for every c. The bound is satisfied on every proportional background and approached only as c → 0 or ∞. The maximum, m_FP²/H² = 3.918, is at c = 1.

**C. The GFD parity configuration.**
- GFD's two chambers are the two roots e and Pe of the *same* metric, with P = diag(1, −1, −1, −1). In vielbein form that is S = e⁻¹ẽ = P with f = g.
- Then e_n(P) = (1, −2, 0, 2, −1), so V(P) = β₀ − β₄ = 0. The locked potential vanishes exactly there.
- Its stress at S = P is diag(49, −15, −15, −15), which is not of cosmological-constant form. So "TetB = second HR tetrad" with f = g is not a vacuum solution.
- In other words, GFD's TetA/TetB (two roots of one metric) and HR's e, ẽ (two different metrics) are different objects. The dictionary in Paper XII (TetA ↔ e, TetB ↔ ẽ, Field Origin ↔ S = I) mixes them.

**D. Decoupling-limit coefficients.**
- With Stückelberg fields, f → (η − Π)² and Π = ∂∂π/Λ₃³, Λ₃³ = m²M_Pl. The h–π mixing tensor expands in the identically conserved basis as
  Σₙ(−1)ⁿβₙYₙ(1 − Π) = Σₖ dₖ Yₖ(Π),
  with d₀ = β₀+3β₁+3β₂+β₃, d₁ = β₁+2β₂+β₃, d₂ = β₂+β₃, d₃ = β₃.
- For the locked set, (d₀, d₁, d₂, d₃) = (49, 32, 16, 0).
- d₁ = 32 is the Fierz–Pauli combination again, a consistency check.
- d₃ = 0 removes the irreducible h·X⁽³⁾ mixing, and with it the λ⁵ term below.
- d₂ = 16 ≠ 0, so the cubic Galileon term is present. Paper XII says β₁ = β₃ = 0 "kills the cubic and quintic Galileon interactions". The quintic part is right and the cubic part is not.

**E. Static spherical solution.** I used the decoupling-limit Lagrangian −½hEh + h^{μν}Σₖaₖ X⁽ᵏ⁾_{μν}(∂∂π) + h_{μν}T^{μν}/(2M), with isotropic h₀₀ = A(r), h_ij = B(r)δ_ij and π(r). Steps:
- Reduced the action and took the Euler–Lagrange equations. All three are total derivatives, so their first integrals are exact.
- Eliminating A′ and B′ leaves an algebraic equation for λ = π′/r:

  (3/2)a₁²λ − (3a₁a₂ + a₃q/4M)λ² + (a₂² + 2a₁a₃/3)λ³ − (a₃²/6)λ⁵ + a₁q/(4M) = 0, with q = M_enc/(4πr³).

- The force on matter is g_tot/g_N = 1 − 2Ma₁λ/q + (2/3)Ma₃λ³/q.
- Neither equation contains r except through q. **The response depends on the enclosed mass only through M_enc/r³.**
- The linear regime gives g_tot/g_N = 4/3 exactly (vDVZ), for every mass and radius.

**F. The locked screening equation.**
- With a₃ = 0, write λ = −sq/(2Ma₁), so that g_tot/g_N = 1 + s, and let Q = a₂q/(Ma₁²). The π-equation becomes Q²s³ + 6Qs² + 6s − 2 = 0, or with v = Qs:

  **v(v² + 6v + 6) = 2Q.**

- At Q → 0, s = 1/3 (the 4/3 force). As Q → +∞, s ≈ 2^{1/3}Q^{−2/3} → 0 (screened to GR).
- For Q < 0, the branch connected to infinity ends at Q* = 2 − 2√2 ≈ −0.828, where s = 1/√2. Inside that point only a disconnected, screened branch exists.
- With the overall sign fixed by requiring a non-tachyonic Fierz–Pauli mass, a₂/a₁² ∝ −d₂/d₁², so the locked set sits on the Q < 0 side.
- On every branch, s ≤ 1/√2, so g_tot/g_N < 1.71.

## Why no projection of this sector can give μ(x)

1. **Wrong variable.** μ(x) is a function of g/a₀ ∝ M_enc/r². The bimetric static response is a function of Q ∝ M_enc/(M_Pl Λ₃³ r³). The two transition radii scale differently with mass: r_V ∝ M^{1/3} and r_M = √(GM/a₀) ∝ M^{1/2}. No change of variable maps one into the other for all masses.
2. **Bounded enhancement.** A flat rotation curve needs g_tot/g_N ≈ √(a₀/g_N) → ∞ in the deep field. Here g_tot/g_N ≤ 4/3 in the linear regime and < 1.71 on any branch. In bimetric (as opposed to massive) gravity the massive mode carries only part of the coupling, which can only lower this bound.
3. **Where galaxies sit.** With m ~ H₀/c, r_V is roughly 260 kpc at 10¹⁰ M☉ and 560 kpc at 10¹¹ M☉, against r_M ≈ 3.4 and 11 kpc. Galaxies lie deep inside r_V, where Vainshtein screening returns them to GR. There, μ_eff → 1, not x/(1+x).
4. **The N-family claim.** Papers VIII and IX state that x(1−μ)^N = μ "arises from the Vainshtein screening equation" with N counting metrics. The actual locked screening equation is v(v² + 6v + 6) = 2Q, in a density variable. It is not of that form, and with N = 2 it does not turn into the bound law.

## What survives, and what this points to

- **The lock does fix things in the bimetric sector.** It sets the background (Λ = m²(1+48c²)), the Fierz–Pauli mass (m_FP² ∝ 32c²) and the Higuchi-safe spectrum. It removes the irreducible mixing (d₃ = 0) and gives the integer screening cubic v(v² + 6v + 6) = 2Q. These are genuine, testable consequences of {1, 0, 16, 0, 1}, so the lock is not empty. But they are bimetric facts at the scale of the Hubble rate and the graviton mass, not galaxy-scale μ(x).
- **μ(x) needs a first-derivative, acceleration-scale kinetic term.** That term is F(|∇Φ|²/a₀²) in the SST itself. Its deep limit F ∝ y^{3/2} is a k-essence/AQUAL structure, which a potential with no derivatives cannot generate in the decoupling limit.
- **The natural place to look next is a coupling between the two connections, not the two metrics.** Milgrom's BIMOND (Phys. Rev. D 80, 123536, 2009) obtains MOND from two metrics coupled through the connection difference C = Γ − Γ̂. That is a tensor in V⊗V*⊗V*, with K³ = 64 components splitting 40 + 24, exactly the space Letters 2 and 3 and Paper B work in.
  - One caution, from part C: GFD's two roots share one metric, so their Levi-Civita connections are identical and C = 0.
  - A GFD version would therefore have to use the torsion (24) sector as the second connection. That fits L2/L3's claim that torsion carries the TetB share.
  - Whether that coupling, with F fixed by the lock, gives exactly μ = x/(1+x) is the next calculation.

## Limits of this note

- The decoupling limit was taken around flat space. The locked set's d₀ = 49 tadpole really sits on a de Sitter background with H ~ m. At galactic radii its corrections are of order H²r², which is negligible.
- The full bimetric decoupling limit, with a dynamical f-fluctuation, was not computed. The massive-gravity (frozen-f) limit was used. The linear bimetric force is the standard massless plus weighted massive superposition, which keeps the enhancement bounded by 4/3.
- The sign that places the locked set at Q < 0 follows from the conventions stated in part F. The conclusion does not depend on it: the response is a function of M/r³ and is bounded on either sign.

---

## Part 2 (later the same day): the relation that does work

*Probe scripts, all passing: `probe_sst_vs_locked_hr.py`, `probe_gradient_leg.py`, `probe_log_and_stueckelberg.py`, `probe_cube_clifford_mond.py`, `probe_mu_as_field.py`, `probe_orientation_and_covariant.py`. Supporting runs: `probe_projections.py`, `probe_torsion_force.py`, `probe_aqual_vs_two_potential.py`, `probe_local_mixing.py`, `probe_tetb_auxiliary.py`, `probe_ec_candidate.py`.*

Part 1's conclusion is right about the standard construction and wrong as a general verdict. The locked potential reproduces the SST once the second frame is tied to the acceleration rather than to the curvature of a reference field.

**Why the standard construction gives density and GFD gives acceleration.** Standard bimetric gravity builds the second frame from reference fields, ẽ = dφ.
- For φⁱ = xⁱh(r), the eigenvalues are tied: (rh)′ radially and h on the two transverse axes. In the decoupling limit that puts ∂∂π, a second derivative, into S, so the response depends on density, M/r³.
- GFD needs S = diag(1, 1, 1, |∇Φ|/a₀). That means h = 1 with (rh)′ ≠ 1, which no reference-field pullback can give.

**The cube and Clifford structure of the lock.**
- *On the cube of spatial leg flips, S = diag(1, ±1, ±1, ±1):*
  - V vanishes on all four TetB transitions.
  - On TetA it is 98 at (+,+,+) and −30 at the three mixed vertices. That is V = 2(1 + K²(x+y+z)) on Paper C's TetA modes.
- *In the even Clifford algebra Cl⁺(1,3) ≅ Cl(3), whose 8 blades are the cube's vertices,* the locked weights split 49 | 49 two ways:
  - by parity: TetA = scalar + 3 rotations, TetB = 3 boosts + volume;
  - by face, along any single axis.
- *The gradient leg:* the rank-one deformation along the acceleration axis gives V = 49(1 + λ). That is the face split along that axis.
  - The face share λ/(1+λ) is μ = x/(1+x), with n = 1 from the palindrome.
  - β₂ = 16 only sets the 49s; it cancels from μ.

**The SST as a function of the locked potential.** Let w = V/V₀ = 1 + |∇Φ|/a₀. Then:
- F(y) = y − 2D(w), with D(w) = w − 1 − ln w (equivalently −4 KL(𝒩(0,w)‖𝒩(0,1))).
- On this family, V/V(I) = det[(I+S)/2], so the log term is the log-volume of the midpoint (Field-Origin) frame.

**The share as a field (auxiliary).**
- *Uniform split of all four legs.* Writing e_A = μe, e_B = (1−μ)e turns the locked potential into a binomial average. Its stationary point sits at μ = ½, so this split cannot give MOND.
- *Acceleration leg.* With u = ln(V/V₀):

  E(u; y) = (1 − V₀/V)·y − 2(sinh u − u)

  - Its stationary point is V/V₀ = 1 + |∇Φ|/a₀.
  - At that point the coupling equals μ and the value equals F(y).
  - The potential is the orientation-odd sum −Σ_{s=±1} s·φ(su), with φ(z) = e^z − 1 − z. That is the odd channel, like sK in f(K,s).
  - The orientation-even sum Σ_s φ(su) is the equation of state.

**A covariant form.** Let a_μ be the acceleration of the tetrad's time leg, the boost direction.
- Take the second frame equal to the first except along a_μ, with ratio |a|/a₀. This gives V = 49(1 + |a|/a₀) for any direction of a.
- In the static weak field the extra sector depends only on g₀₀. So Ψ = Φ (γ = 1, full lensing), and the Φ-equation is g_s = g_t²/(a₀ + g_t).
- A homogeneous cosmology has a = 0. That puts V at its floor, V₀ = 49, a pure vacuum term.

**Open.**
- The time leg's acceleration defines a preferred frame. The preferred-frame parameters α₁ and α₂ need computing.
- In an isolated strong field the simple μ leaves a constant extra pull of a₀. The external-field effect still has to be computed against solar-system bounds.
- The meV-scale origin of the log term (a Gaussian sector on the midpoint frame) is a hypothesis.

---

## Part 3: the solar system, and the matter coupling that GFD needs

*Scripts: `probe_efe_solar_system.py`, `probe_net_galactic_field.py`.*

**The local-source reading fails.** Suppose every mass sources the SST scalar through its own local gradient. Then every isolated mass carries a saturated TetB field, B = (1−μ)g → a₀. Around the Sun this gives two effects, and both are ruled out:
- *A constant extra pull of 1.2 × 10⁻¹⁰ m/s² at every planet.* Perihelion analyses exclude it: Iorio 2008, arXiv:0711.2791.
- *An external-field quadrupole of Q₂ ≈ 4.0 × 10⁻²⁶ s⁻².* Cassini measures (3 ± 3) × 10⁻²⁷ (Hees et al. 2014, arXiv:1402.6950).

Exchange symmetry plus the deep-field limit forces 1 − μ ≈ 1/x at large x. Every such μ I tested stays above the Cassini bound.

**The coarse-grained reading adopted here.** The papers leave 𝓛_matter unspecified. The reading is:
- the SST scalar is sourced by the galaxy's coarse-grained density ρ̄;
- x = |∇Φ̄|/a₀ is built from the galaxy's net field;
- bound subsystems (a star with its planets) gravitate internally through the metric, i.e. GR.

What a local solar system then feels is the galaxy's net field. Its uniform part, g_e ≈ 2.3 × 10⁻¹⁰ m/s² (x ≈ 1.9), is removed by free fall, so only the galactic tide is left. That tide is about 1 × 10⁻³⁰ s⁻², giving 1.6 × 10⁻¹⁸ m/s² at Saturn, roughly 8000 times below the Cassini bound. There is no a₀ monopole and no Sun-centred quadrupole.

Galactic predictions are unchanged. With the McMillan-type baryons, the SST rotation curve in the plane is 240 km/s at 8.2 kpc. That number is sensitive to the gas-disk scale assumed here (7 kpc); Paper VII quotes 225 km/s, against an observed 229 ± 5. The curve continues at 220 km/s at 15 kpc, 207 at 25 kpc and 197 at 50 kpc.

**What this commits GFD to.**
- A precise definition of a bound subsystem. A natural scale is √(Gm/a₀), about 7000 AU for the Sun.
- Wide binaries, star clusters and the Oort cloud are Newtonian internally. This conflicts with Paper VII's claimed wide-binary plateau.
- The external-field effect acts between galaxies, through ρ̄.
