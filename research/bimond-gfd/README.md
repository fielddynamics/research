# BIMOND × GFD

*Research folder, Field Dynamics Research, 2026-11-11. Status: working notes and checks, not a paper. Run `python3 run_all.py`: 19 checks pass, plus two data scripts (numpy, scipy, sympy).*

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
  - With ρ̂ ≥ 0, an isolated galaxy can only be braked. CamB is a brake.
  - A drive (M_dec > M_phot) needs the environment (the host's net field) or ρ̂ < 0.
  - Where M̂ > M, matter is repelled, matching Milgrom's "the twin's phantom mass repels both kinds".

**04 — Test of "brake only" on SPARC** (`04_sparc_brake_only.py`). I took the per-galaxy median of log₁₀(M_dec/M_bar) over the outer half of each rotation curve.

| Sample | N | Median | Fraction above +0.1 dex | Fraction below −0.1 dex |
|---|---|---|---|---|
| All | 163 | −0.054 | 0.22 | 0.40 |
| Quality flag Q = 1, inclination ≥ 45° | 82 | −0.020 | 0.23 | 0.29 |

The distribution leans toward brakes, but about a fifth of galaxies sit above +0.1 dex. With a flat mass-to-light ratio and 0.18 dex scatter this is not yet a test. It needs fits with the stellar mass-to-light ratio and distance marginalised, and an isolation cut.

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

## What this gives GFD

A candidate covariant SST that already exists in the literature:

**BIMOND with α = −β (fixed by orientation), 𝓜 fixed by μ (closed form above), φ̂ sourced by the coarse-grained galactic field (the net-field rule), and twin matter as occupied TetB.**

In this candidate:
- Lensing and γ = 1 are inherited.
- The decoded-mass deficit is the TetB (twin) mass.
- Local systems are exactly GR.

## Open items

1. **Root-blindness only in vacuum.** In BIMOND the two metrics must differ once matter is present, or C = 0. GFD's "same metric for both roots" then holds only at the Field Origin, with no matter.
2. **Torsion vs connection difference.** BIMOND's MOND sector is C in the 40. GFD has placed TetB in the torsion 24. Both give the same 3-vector in the slow-motion limit (`research/bimetric-projection/probe_where_tetb_pushes.py`). The relativistic content differs, and GFD has to choose.
3. **Ghosts.** α = −β gives the twin sector a negative Einstein–Hilbert term. Ghost stability, and Milgrom's self-acceleration of mixed systems (F − F̂ = 0, not F + F̂ = 0), are open.
4. **The net-field rule needs a covariant statement.** It has to say what coarse-graining scale defines φ̄*. Test D (`research/bimetric-projection/probe_testD_clusters_vs_dwarfs.py`) shows that star clusters must be coarse-grained out and dwarf galaxies kept. The criterion is galaxy (vortex) versus bound cluster, not a radius.
5. **Gravitational-wave speed** in BIMOND with two dynamical metrics is not checked here (GW170817).
6. **Drives.** Under "brake only", any isolated galaxy with M_dec > M_phot beyond the errors needs ρ̂ < 0 or an environmental origin. Test 04 has to be redone properly.
