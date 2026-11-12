# BIMOND × GFD

*Research folder, Field Dynamics Research, 2026-11-11. Status: working notes and checks, not a paper. Run `python3 run_all.py`: 78 checks pass, plus two data scripts (numpy, scipy, sympy).*

This folder lines up Milgrom's bimetric MOND (BIMOND; [arXiv:0912.0790](https://arxiv.org/pdf/0912.0790), [arXiv:1001.4444](https://arxiv.org/pdf/1001.4444), [arXiv:2208.10882](https://arxiv.org/pdf/2208.10882)) with the GFD algebra: the Coles notes, `research/gfd_algebra.py`, and `research/bimetric-projection/`. The question is whether BIMOND is a covariant home for the SST's physics.

## BIMOND in one paragraph

BIMOND has two metrics, g and ĝ. Matter couples to g and "twin matter" couples to ĝ. The action is

I = −(16πG)⁻¹ ∫ [β√g R + α√ĝ R̂ − 2(gĝ)^{1/4} f(κ) a₀² 𝓜(Υ/a₀²)] + I_M[g] + Î_M[ĝ]

- Υ is built from C = Γ − Γ̂, the difference of the two Levi-Civita connections.
- κ = (g/ĝ)^{1/4}.

Milgrom singles out the case α + β = 0 (β = 1). In it the nonrelativistic limit reduces to linear equations:

Δφ* = 4πG(ρ − ρ̂),  Δφ = 4πGρ + ∇·(𝓜′∇φ*),  φ* = φ − φ̂.

This is QUMOND, the two-potential form of MOND. Lensing is governed by the same potential as dynamics.

## Results

*The formal results of 01, 02 and 08 (the coupling sign, 𝓜 in closed form, Legendre duality and convexity) are written up as a proof: [`proofs/bimetric-two-potential-energy/`](../../proofs/bimetric-two-potential-energy/) (39 checks).*

**01 — The orientation of the second root gives α + β = 0** (`01_orientation_alpha_beta.py`).
- In tetrad form the Einstein–Hilbert term is the 4-form ∫ε_abcd eᵃ∧eᵇ∧Rᶜᵈ. Under the parity that maps TetA to TetB, ε picks up det P = −1, so S_EH[Pe] = −S_EH[e]. Proper Lorentz transformations leave it unchanged.
- TetA (det e > 0) and TetB (det ẽ < 0) with equal Planck mass therefore enter with opposite signs. That is exactly BIMOND's special case.
- Milgrom chooses this case. In GFD it follows from the orientation of the second root.

**02 — GFD's μ fixes BIMOND's free function** (`02_nr_limit_and_M.py`). I derived the nonrelativistic limit here for general (α, β):
- In spherical symmetry, g* = −(αg_s + βĝ_s)/(𝓜′(α+β) − αβ).
- φ* is Newtonian, independent of 𝓜, if and only if α + β = 0. In that case φ* is sourced by ρ − ρ̂.
- Requiring GFD's spherical law g_s = g_t²/(a₀ + g_t) gives:
  - 𝓜′(z) = −½ + √(¼ + z^{−1/2}), with z = |∇φ*|²/a₀². This meets BIMOND's two conditions: 𝓜′ → 0 at large z, and 𝓜′ ~ z^{−1/4} at small z.
  - In closed form, with u = |∇φ*|/a₀:

    𝓜(u) = ½√u (u+2)√(u+4) − u²/2 − 4 arsinh(√u/2),  𝓜(0) = 0.

  - Asymptotics: at small u, 𝓜 ≈ (4/3)u^{3/2} − u²/2 + …. At large u, 𝓜 = 2u − 2 ln u + 1 + o(1).
- The SST is the AQUAL form and BIMOND with α = −β is the QUMOND form of the same μ. They coincide in spherical symmetry. They differ by under 1% in the plane of a Miyamoto–Nagai disk (`research/bimetric-projection/probe_aqual_vs_two_potential.py`).

**03 — Dictionary, and what twin matter does** (`03_dictionary_and_twin_matter.py`).

| BIMOND (α = −β = −1) | GFD |
|---|---|
| φ* = φ − φ̂, the Newtonian potential of ρ − ρ̂ | TetA, the source field |
| ∇φ̂ = −𝓜′∇φ* (+ the twin's own Newtonian part); its magnitude is (1−μ)g_t ≤ a₀ | the TetB field (phantom), saturating at a₀ |
| φ, which matter and light follow | the TetA + TetB total (γ = 1) |
| twin matter ρ̂, a negative active mass for φ* | occupied TetB: the drain or throat |
| (∇φ)² − (∇φ̂)² = \|∇φ*\|² + 2∇φ*·∇φ̂ | the TetA–TetB cross-coupling, supplied by α = −β instead of being added by hand |
| C = Γ − Γ̂, symmetric in its lower indices | lives in the 40, not the torsion 24; its slow-motion component Cⁱ₀₀ = ∂ᵢφ* sits in the shared diagonal 16 |

- **Decoding theorem.** Apply the decoding-mass letter's inversion, M_dec = r²·[g_t²/(a₀ + g_t)]/G, to BIMOND–GFD. It returns M_dec = M − M̂ exactly, at every radius. So **ΔM_eff = M_phot − M_dec is the enclosed twin (occupied-TetB) mass.**

> **Brake-only is a BIMOND limitation, not a GFD prediction.** GFD treats both a brake and a drive as possible in galaxies.

  - **BIMOND.** Twin matter ρ̂ is a scalar density. With ρ̂ ≥ 0 the twin sector can only brake (M_dec < M_phot). A drive would need ρ̂ < 0.
  - **GFD.** TetB acts like a local vortex inside a net vortex, as in standard vortex dynamics. It brakes or drives depending on which way its spin points relative to the net TetA vortex spin, not on the sign of a density. Counter-rotating means brake; co-rotating means drive. Neither needs negative mass.
  - **The decoding-mass letter shows both cases** (`papers/letter-decoding-mass-from-rotation-curves/letter.tex`). The letter states that the decoded mass "may fall above or below the photometric value".
    - Brake: CamB, where M_dec falls below M_phot (Fig. 2).
    - Drive: M33, where M_dec = 1.38 × 10¹⁰ M☉ at 17 kpc against M_phot ≈ 7 × 10⁹ M☉.
    - Close to zero: the Milky Way (6.6 vs 7.3 × 10¹⁰ M☉) and NGC 3198, which track their baryons.
  - A scalar ρ̂ has no handedness, so BIMOND cannot represent GFD's drive. Spin direction needs an axial (gravitomagnetic) channel, the torsion 24, which is where GFD puts TetB (see open item 2).
  - Where M̂ > M, matter is repelled, matching Milgrom's "the twin's phantom mass repels both kinds".

**04 — Test of BIMOND's brake-only limit on SPARC** (`04_sparc_brake_only.py`). I took the per-galaxy median of log₁₀(M_dec/M_bar) over the outer half of each rotation curve.

| Sample | N | Median | Fraction above +0.1 dex | Fraction below −0.1 dex |
|---|---|---|---|---|
| All | 163 | −0.054 | 0.22 | 0.40 |
| Quality flag Q = 1, inclination ≥ 45° | 82 | −0.020 | 0.23 | 0.29 |

This tests BIMOND's scalar, brake-only version, not GFD. GFD allows both brakes and drives, so the fifth of galaxies sitting above +0.1 dex (driven, like M33) is consistent with GFD. Under scalar BIMOND they would need ρ̂ < 0. The distribution leans toward brakes. With a flat mass-to-light ratio and 0.18 dex scatter this is not yet a test. It needs fits with the stellar mass-to-light ratio and distance marginalised, and an isolation cut.

**05 — Local systems** (`05_local_systems.py`).
- BIMOND as written applies 𝓜′ to every source. Around the Sun that gives a constant a₀ pull at every planet, plus the external-field quadrupole Q₂ ≈ 4.8 × 10⁻²⁶ s⁻² (at g_e = 2.28 × 10⁻¹⁰). Cassini measures (3 ± 3) × 10⁻²⁷. Both are excluded.
- Under GFD's net-field rule (`EINSTEIN_TETA_PARTITION.md`), φ̂ is sourced by the galaxy's coarse-grained φ̄*:

  Δφ̂ = ∇·[𝓜′(|∇φ̄*|)∇φ̄*].

  - In the QUMOND form this is a one-line change, because the φ̂ equation is linear.
  - Inside a bound system φ̂ is then uniform, cancelling in free fall, apart from a tide of about 9 × 10⁻³¹ s⁻². That is about 1.3 × 10⁻¹⁸ m/s² at Saturn, roughly 10⁴ times below Cassini.
  - Between the bodies only φ* acts, i.e. Newton/GR (TetA) exactly.

**06 — Where the lock meets BIMOND** (`06_lock_meets_bimond.py`).
- κ = |det S|^{−1/2}, so BIMOND's f(κ) depends on S only through e₄(S) = det S. That is the volume channel: β₄ = 1 in the lock, and the pseudoscalar, on the TetB side of Cl⁺(1,3) ≅ Cl(3).
- At the GFD parity configuration (S = P, same metric), both interactions vanish:
  - BIMOND's, because C = 0 and 𝓜(0) = 0;
  - the locked Hassan–Rosen potential, because V(P) = 0.
  - Only matter and twin matter split the metrics.
- GFD's 𝓜 grows like 2u, so Milgrom's Λ ~ a₀²𝓜(∞) does not apply directly. The vacuum term would come from f(κ) or from the locked potential's floor (V₀ = 49 m², giving Λ_eff = 2a₀²/c⁴ in `research/bimetric-projection/`).

**07 — The algebra side by side** (`07_algebra_intersection.py`, 11 checks). This compares the identities in `research/gfd_algebra.py` with BIMOND's variables. The three potentials are φ* (TetA), φ̂ (TetB) and φ (the total).

| GFD algebra | BIMOND form | Status |
|---|---|---|
| Odds ratio Ω(x) = x (Proof C, Möbius uniqueness) | \|∇φ̂\| · \|∇φ\| = a₀ \|∇φ*\|: twin field × total field = a₀ × Newtonian field | exact; a rewrite of μ |
| Exchange symmetry μ(1/x) = 1 − μ(x) | the TetA and TetB shares of the total field swap under x → 1/x | exact |
| SST kinetic function F(y) (Proof B) | F and BIMOND's 𝓜 are exact Legendre duals: F(x²) + u² + 𝓜(u) = 2xu, with u = x²/(1+x). This is the AQUAL ↔ QUMOND duality in closed form. | exact (symbolic in 08, 50 digits in 07) |
| Logistic identity x μ′ = μ(1−μ) | g* ĝ / g², the product of the two shares | exact |
| 40 retained / 24 discarded (Letter 3) | BIMOND's C = Γ − Γ̂ has 4 × 10 = 40 components, exactly GFD's retained 40. The tetrad (Weitzenböck) difference of two frames has 4³ = 64 = 40 + 24. | count |
| TetB in the torsion 24 | Two frames that differ by a local rotation have the **same metric**, so BIMOND's C = 0: BIMOND cannot see the rotation. Their tetrad difference does carry axial torsion, and its sign follows the sense of rotation: a twist θ = kz gives a_t = −4k, and a spin θ = ωt gives a_z = 4ω. Reversing the rotation reverses the sign. | exact (sympy) |
| Parity P (TetA → TetB) | constant P gives zero tetrad difference, consistent with C = 0 and V(P) = 0 in 06 | exact |

**08 — Deriving 𝓜 the GFD way** (`08_deriving_M_the_gfd_way.py`, 9 checks, symbolic).

**Milgrom does not derive 𝓜.** BIMOND (0912.0790) calls it "an a priori unspecified function", says it should eventually come from a deeper theory, and fixes only its limits:
- 𝓜′ → 0 at high acceleration;
- 𝓜′ ≈ z^{−1/4} in the deep-MOND regime.

His papers do not mention a Legendre transform, and 2208.10882 again says 𝓜 is fixed by phenomenology. GFD supplies 𝓜 by the same route it used for F, integrating over the tetrad shares. Here x = g/a₀ is the total field, u = g*/a₀ is the TetA (Newtonian) field, and b = 1 − μ is the TetB share.

| Step | Result |
|---|---|
| Proof C: exchange symmetry and Möbius uniqueness | μ(x) = x/(1+x) |
| Split the total field into shares | TetA g* = μg; TetB ĝ = (1−μ)g = **a₀ μ(x)**; total x = u + μ(x) |
| Proof B (SST side): work done by TetA along the total field | F = 2∫(g*/a₀) dx = x² − 2x − 2 ln b |
| **BIMOND side: work done by TetB along the TetA field** | **𝓜 = 2∫(ĝ/a₀) du = 2x − 1 + 2b − b² + 2 ln b** |
| Consequences | 𝓜(0) = 0. 𝓜′(z) = 1/x = a₀/\|∇φ\|, the inverse odds ratio. The TetB logarithm enters F as +2 ln(1+x) and 𝓜 as −2 ln(1+x), and it cancels in the Legendre sum F + u² + 𝓜 = 2xu. |

Written in the TetB share b, 𝓜 is a polynomial plus one logarithm. That is simpler than the arsinh form in 02, which is the same function written in u. Read this way:
- F is what TetA does along the total field, and 𝓜 is what TetB does along the TetA field.
- The two are Legendre duals, and the TetB logarithm is the term they exchange.
- This gives 𝓜 the derivation Milgrom left open, within GFD's postulates. Once μ is given, integrating ν − 1 gives the same function by brute force. The added content is the route through μ's derivation and the reading of each term as a tetrad share.

**09 — Legendre duality at the level of the action** (`09_covariant_legendre_duality.py`, 14 checks). This tests whether the SST and BIMOND are one theory written two ways. It works with the SST's scalar sector, −(a₀²/8πG)F(X/a₀²) − ρΦ, where X = g^{μν}∂_μΦ∂_νΦ, on any metric. Gradients are taken to be spacelike, which is where F is defined. W*(p) = Q(|p|/2), where Q = y² + 𝓜 is the Legendre dual from the proof.

| Form | Lagrangian | What it is |
|---|---|---|
| SST (AQUAL) | −(a₀²/8πG) F − ρΦ | one scalar |
| First-order | (a₀²/8πG)[W*(p) − p·∂Φ/a₀] − ρΦ, with p an auxiliary covector | **exactly the SST.** Eliminating p returns F on any metric; p enters without derivatives. |
| Gradient | p = 2∂χ/a₀: (a₀²/8πG) Q(\|∂χ\|/a₀) − (1/4πG) ∂χ·∂Φ − ρΦ | **identically** −(1/8πG)[\|∂φ\|² − \|∂φ̂\|² − a₀²𝓜] − ρφ, with φ = Φ, φ* = χ, φ̂ = Φ − χ. This is Milgrom's BIMOND Lagrangian with β = 1, α = −1 (flat space and a curved static 3-metric checked symbolically). |

Results:
- **α = −β has a second, independent origin.** The Legendre pairing term −2∂χ·∂Φ completes the square to \|∂φ\|² − \|∂φ̂\|². The opposite sign is the sign of the duality itself, and it agrees with the tetrad orientation lemma.
- **The two forms differ by exactly one thing: which side carries the curl.**
  - In AQUAL the field ∂Φ is a gradient, and the flux p (that is, μ∇Φ) can have a curl.
  - In QUMOND/BIMOND the flux is the Newtonian gradient ∂φ*, and the field ν∇φ* has a curl, which is projected away.
  - With two point masses, the curl of ν(\|g_N\|)g_N is 10⁻²–10⁻¹ in units with G = a₀ = 1. With one mass it is zero, so the two coincide in spherical symmetry.
  - So BIMOND is the SST with the auxiliary flux required to be a gradient. That is one constraint, not a different theory. It matches the under-1% disk difference found in `research/bimetric-projection/probe_aqual_vs_two_potential.py`.
- **Two schemes meeting at a nonlinear Field Origin.**
  - The tetrad equation's scheme is two schemes, one per root, det e = ±√−g (see the [two bounded regions proof](../../proofs/tetrad-scheme-two-bounded-regions/)). TetA and TetB are two full sectors, two tetrads in GFD's Hassan–Rosen form (Paper VII), not one field with a sign chosen.
  - They meet at the Field Origin, the interaction vertex at S = I (the octahedral core), and the coupling there is nonlinear. The Hassan–Rosen potential V(S) = e₀ + 16e₂ + e₄ is nonlinear in S. In the two-potential form, 𝓜 has no Taylor expansion at zero field: 𝓜 ≈ (4/3)z^{3/4} and 𝓜′ ≈ z^{−1/4} → ∞.
  - The two proofs show the same thing from either side. At zero field the AQUAL Hessian goes to 0 (degenerate) and the two-potential Hessian goes to ∞ (singular). There is no quadratic, linear theory at the Field Origin.
  - So the diag(1, −1) kinetic matrix of the two-potential form records the orientation sign of the two sectors away from the vertex. It is not a ghost diagnosis. A ghost is defined by the quadratic (linearised) theory, and at the Field Origin that does not exist.
  - The opposite sign is the orientation that gives the two sectors opposite chirality (+θ for TetA, −θ for TetB). In the vortex-closure note (Letter 3 supplement), that chirality breaks the holonomy cancellation through the Field Origin and makes the field close as a vortex with an axis, which is the disk. The sign is what makes the vortex.
  - The first-order form (auxiliary flux) is a mathematically equivalent rewriting of the SST's scalar sector. It is not a claim that TetB lacks its own dynamics, which GFD's two-tetrad form gives it.

**Scope.** This is the scalar sector on a given metric. It is not a proof that the full SST, with its R and Maxwell terms, equals full two-metric BIMOND. BIMOND's second metric carries its own curvature term, whereas here φ̂ is a second scalar. The duality is exact for spacelike gradients. For timelike gradients F(y) is not defined, which is the standard open issue for AQUAL-type theories.

**10 — The chiral holonomy, reproduced** (`10_chiral_holonomy_check.py`, 6 checks). Letter 3's supplement [`supplementary_chiral_holonomy.tex`](../../papers/letter-3-field-closure-of-tetrad-frame/Supplementary/supplementary_chiral_holonomy.tex) proves by computation that transport through the eight null directions has two behaviours:
- **Uniform transport** (no chirality) gives identity holonomy on all twelve Hamiltonian cycles of the cube.
- **Chiral transport** (+θ from TetA, −θ from TetB) never does: 6 cycles give 135° and 6 give 155.8°.

The script the note cites isn't in the repository, so this reproduces it exactly. It adds one result: **the two angle classes are the two senses of circulation.** Each cycle gives 135° traversed one way and 155.8° traversed the other (exactly arccos(−4639/6561) and arccos(−5983/6561); see 11). So the closure through the Field Origin is chiral: its two senses of rotation are not equivalent. This is the framework's own evidence that the vortex is a parity-broken configuration, which bears on open item 3. It is kinematic (transport), not a stability result.

**11 — The holonomy read through GFD's two-sector algebra** (`11_holonomy_robustness.py`, 10 checks)

GFD already has the mathematics of the two sectors:
- **The Gram index grid** ([`papers/gram-matrix-of-tetrad-equation/`](../../papers/gram-matrix-of-tetrad-equation/)). Each K × K slice of the connection splits into 6 upper entries (TetA), 4 diagonal entries (shared) and 6 lower entries (TetB). Across four slices that is 64 = 24 + 16 + 24.
- **The cross-coupling sign reversal.** M₁ᵀM₂ = −M₁ᵀM₁ for M₂ = −M₁.
- **Letter 2's Lemma.** A torsion-free connection, which keeps 16 + 24 = 40, cannot distinguish TetA from TetB.

| Check | Result |
|---|---|
| The note's TetB step | R(n, −θ) is **exactly the transpose** of the TetA step R(n, θ). The diagonal is shared, and the upper and lower triangles are exchanged. That is the same exchange the Gram index grid assigns to TetA ↔ TetB. So the note's sign rule is the 24 + 16 + 24 structure, not an extra assumption. Transposing the TetB steps reproduces the note's transport on all twelve cycles. |
| Uniform transport | Every step is read as TetA, which is the root-blind, torsion-free projection. It gives the identity on every cycle, as Letter 2's Lemma requires. Keeping the TetB sector gives winding on every cycle. |
| Exact angles | cos Θ = −4639/6561 and −5983/6561, with 6561 = 3⁸, so Θ = 134.996° and 155.770°. The note's "135° (= 3π/4)" is close but not exact. |
| Parity | Swapping the TetA/TetB labels exchanges the two classes. The difference between the two senses of circulation is mirror-odd: a chirality. |
| For comparison: a GR-baseline model | TetA's Levi-Civita transport on every step, plus torsion as a small rotation of alternating sign, cancels exactly. That model imposes GR's projection on the TetB steps, so it reproduces the root-blind null result. It is not a test of the two-sector structure. |

So the chiral-holonomy proposition follows from GFD's own algebra. The TetB step is the TetA step with the two 24-component triangles exchanged and the shared 16 kept. The winding is what the full 24 + 16 + 24 connection does and the 40-component projection cannot.

**12 — Further algebra: the spinor lift and the share-weighted transport** (`12_spinor_lift_and_partition.py`, 9 checks)

| Check | Result |
|---|---|
| Spinor (SU(2)) lift, uniform transport | Uniform transport is the root-blind, all-TetA reading. In SO(3) it gives the identity, but in SU(2) it gives **exactly −1 on every cycle**: one circuit is a full 2π turn. Vectors return; spinors return with a minus sign, and two circuits are needed to bring them back. This is the 720° of the double cover, which Paper VII assigns to the two sheets, and it falls out of the root-blind transport itself. |
| Spinor lift, chiral transport | Half-traces exactly 31/81 and −17/81 for the two senses, consistent with the SO(3) values: 2(31/81)² − 1 = −4639/6561 and 2(17/81)² − 1 = −5983/6561. |
| Share-weighted steps | S = μR + (1 − μ)Rᵀ at a TetA source and μRᵀ + (1 − μ)R at a TetB source, where Rᵀ is the TetB step from 11. Exchange symmetry x → 1/x (μ → 1 − μ) turns each TetA step into the TetB step exactly. **So exchange symmetry acts as parity on the holonomy**: it swaps the two senses of circulation. |
| The ring x = 1 | With equal shares every step is symmetric: only the shared diagonal part survives. The two senses become equivalent and **the chirality vanishes**. The chirality is odd under x → 1/x, with opposite signs inside and outside the ring, and μ = 1 and μ = 0 recover the two chiral classes. |

Status. The spinor result is exact and needs no assumption beyond the transport of 10 and 11. The share-weighted steps are a construction here: the field partition μ applied to the transport. Two of its results follow from structure, not from fitting: exchange symmetry acting as parity, and chirality vanishing at the ring. The weighted products are not rotations (they contract, most strongly near the ring), so only their rotational part is compared.

## Is there a breakthrough?

Honest grading: two results stand out. Neither is yet a demonstrated breakthrough.

**1. GFD fixes BIMOND's two main free choices from geometry.** Milgrom's BIMOND picks the coupling ratio and the function 𝓜 by hand, and 𝓜 has been free since 2009.
- In GFD the coupling ratio follows from orientation (01): α = −β.
- 𝓜 follows from exchange symmetry and Möbius uniqueness, giving μ = x/(1+x), and then from Legendre duality with the SST's F. The closed form is in 02. 08 derives it directly as TetB work along the TetA field, and the duality is checked exactly in 07 and 08.

So in the nonrelativistic limit, BIMOND with α = −β is the SST written as a two-metric theory, with no free function. Still free: f(κ), which only enters through det S (06), and the value of a₀. This is the cleanest claim to put forward. It is only as strong as the GFD postulates behind it, namely exchange symmetry and the Aut(P¹) axiom. Note that μ = x/(1+x) is also MOND's well-known "simple" interpolating function.

**2. Spin blindness, which separates GFD from every metric bimetric theory.** Any theory built only from the two metrics cannot see a relative rotation of the two frames: BIMOND through C, and Hassan–Rosen through S. A tetrad theory sees it as axial torsion, with a sign set by handedness.
- This is the algebraic home for brake versus drive: counter-rotating versus co-rotating TetB.
- It gives a prediction that BIMOND does not make: the sign of ΔM_eff should correlate with relative rotation sense. Examples to test are counter-rotating gas or stellar components, and spin relative to the host galaxy's tidal field.

What is still missing is a field equation linking the axial torsion to ΔM_eff. Until that exists this is a kinematic statement, not a derived prediction, and the size of the effect is not computed.

**Not breakthroughs:**
- The odds-ratio identity and the logistic identity are rewrites of μ.
- The Legendre pairing is standard convex duality: AQUAL and QUMOND with ν the inverse of μ share their spherical solutions, and that is well known. What is new is the derivation route and the physical reading of 𝓜 (08), not the duality itself.
- The 40 = 40 match is a component count.

## What this gives GFD

A candidate covariant SST that already exists in the literature:

**BIMOND with α = −β (fixed by orientation), 𝓜 fixed by μ (closed form above), φ̂ sourced by the coarse-grained galactic field (the net-field rule), and twin matter as occupied TetB.**

In this candidate:
- Lensing and γ = 1 are inherited.
- The decoded-mass deficit is the TetB (twin) mass.
- Local systems are exactly GR.

## Open items

1. **Root-blindness only in vacuum.** In BIMOND the two metrics must differ once matter is present, or C = 0. GFD's "same metric for both roots" then holds only at the Field Origin, with no matter.
2. **Torsion vs connection difference.** BIMOND's MOND sector is C in the 40. GFD has placed TetB in the torsion 24. Both give the same 3-vector in the slow-motion limit (`research/bimetric-projection/probe_where_tetb_pushes.py`). The relativistic content differs. Brake vs drive by spin orientation (item 6) favours the torsion 24, because only an axial channel carries spin direction.
3. **Stability of the two-orientation structure.** α = −β gives the second sector a negative Einstein–Hilbert term, and that sign is the orientation of the second scheme. Any stability analysis has to be done in the nonlinear theory around real backgrounds, not by linearising at the Field Origin, where no quadratic theory exists (item above, script 09). Two points to check:
   - **Citation.** Paper VII cites Alexander, Marcianò & Smolin (2014) for "a single orientation produces a scalar ghost; two opposite chambers cancel it". That paper's abstract says the reverse: its parity-symmetric bimetric phase has a scalar ghost and is unstable, while its parity-broken (chiral) phase is stable. The citation should be checked against the paper's body before it is relied on. One reading consistent with GFD: the vortex is a parity-broken configuration. The chiral-holonomy proposition supports this kinematically: the two senses of circulation give different holonomies, 135° versus 155.8° (script 10). That would place the GFD vortex in the phase Alexander, Marcianò & Smolin find stable, but it is an alignment of descriptions, not a stability proof.
   - **Hassan–Rosen.** Their proof that the Boulware–Deser ghost is absent assumes both kinetic terms are positive. Extending it to opposite orientations is a claim of the framework, not yet a result.
   - **Milgrom (2014), [Gravitational waves in bimetric MOND](https://arxiv.org/abs/1308.5388v1), PRD 89, 024027.** In BIMOND's weak-field limit, the sum sector H⁺ behaves like linearised GR and carries GR's vacuum waves. The difference sector H⁻ "is fully nonlinear even for the weakest" fields and has no gauge freedom. That is the literature form of the Field Origin being nonlinear (script 09). The difference between the two sectors has no linear regime in which a standard ghost count applies.

   Milgrom's self-acceleration of mixed systems (F − F̂ = 0, not F + F̂ = 0) is also open.
4. **The net-field rule needs a covariant statement.** It has to say what coarse-graining scale defines φ̄*. Test D (`research/bimetric-projection/probe_testD_clusters_vs_dwarfs.py`) shows that star clusters must be coarse-grained out and dwarf galaxies kept. The criterion is galaxy (vortex) versus bound cluster, not a radius.
5. **Gravitational-wave speed** in BIMOND with two dynamical metrics is not checked here (GW170817).
6. **Brake and drive come from spin orientation.** In GFD the local TetB vortex brakes or drives against the net TetA vortex spin, depending on its relative handedness, as in standard vortex dynamics. BIMOND needs an axial (spin) twin sector to match this. A proper test of 04 should correlate the sign of ΔM_eff with spin orientation (for example, counter-rotating gas or stellar components, or spin relative to the host's tidal field), not just test a skew.
