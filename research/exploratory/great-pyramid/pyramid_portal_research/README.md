# The Giza Field-Resonator Programme

**Principal investigator:** Stephen Nelson, Field Dynamics Research
**Project:** The Great Pyramid as a field-coupled resonant structure, energised by a gilded capstone, analysed through the K=4↔K=5 vertex of Gravity Field Dynamics
**Framework:** Gravity Field Dynamics (GFD)
**Status:** Research programme. **Start with [`PROGRAMME.md`](PROGRAMME.md)**, the programme definition document: thesis, evidence base, prior work, pre-registered hypotheses H1–H9, work packages and phasing. The files below are its technical basis.

---

## Scope

This project documents the current understanding of the Great Pyramid of Giza as an engineered physics apparatus, derived from the Gravity Field Dynamics (GFD) framework's algebraic spine. The pyramid is treated as a cavity-QED-style boundary apparatus that operates on the always-on TetA/TetB interaction vertex of physics, with Earth's geomagnetic field as the pump.

The framework's load-bearing claim — that gravity is the incoherent statistical residue of a universal K=4↔K=5 hinge interaction, and that the Great Pyramid is a coherent-mode operator of the same interaction — is the throughline of every file in this project.

## Organization

Files are grouped into nine sections proceeding from framework foundations through apparatus engineering to predictions and open questions. Each section directory contains numbered subfiles whose order is the recommended reading order within that section.

```
pyramid_portal_research/
├── README.md                          [this file: index and reading guide]
├── PROGRAMME.md                       [programme definition: thesis, evidence, hypotheses, work packages]
├── FIELD_ORIGIN_KINGS_CHAMBER.md      [how the GFD Field Origin is realised at the King's Chamber]
├── 00_executive_summary.md            [one-document distillation of the theory]
├── 01_framework_foundations/          [the GFD algebraic spine]
├── 02_gravity_derivation/             [α_G = (17/13)α²¹(g_e/2) — the equation]
├── 03_portal_topology/                [K=4→K=5, Hopf, A_5, Σ(2,3,5), SU(2)_19]
├── 04_apparatus_engineering/          [chamber-by-chamber analysis]
├── 05_cavity_QED_operation/           [geomagnetic pump, strong coupling]
├── 06_master_equations/               [the operators in full]
├── 07_predictions_and_tests/          [falsifiable signatures]
├── 08_open_questions/                 [forks still requiring derivation]
└── 99_appendices/                     [notation, constants, references]
```

## Reading order

**For a working overview**, read in this order:
1. `PROGRAMME.md`, then `FIELD_ORIGIN_KINGS_CHAMBER.md`, then `00_executive_summary.md`
2. `01_framework_foundations/01.1_cyclotomic_algebra.md` and `01.4_shift_identity_proof.md`
3. `02_gravity_derivation/02.1_gravity_equation.md` and `02.2_g_factor_breakthrough.md`
4. `06_master_equations/06.1_universal_vertex_operator.md` and `06.2_portal_operator.md`
5. `05_cavity_QED_operation/05.3_strong_coupling_calculation.md`
6. `07_predictions_and_tests/` — pick any prediction file

**For deep theory**, read sections 01, 02, 03, 06 in full.

**For the apparatus**, read sections 04, 05.

**For experimental tests**, read sections 07, 08.

## File manifest

### Section 00 — Executive summary

| File | Content |
|---|---|
| `00_executive_summary.md` | Two-page distillation of the entire current understanding. Read first. |

### Section 01 — Framework foundations

| File | Content |
|---|---|
| `01.1_cyclotomic_algebra.md` | Φ_3, Φ_4, Φ_6 — the three degree-2 cyclotomic polynomials. The integers {13, 17, 21} at K=4. |
| `01.2_closure_read_representation.md` | C_K = Λ^K V ⊕ V ⊕ V⊗V from tetrad bilinearity. Dimensions {1, K, K²} = {1, 4, 16} → total 21 at K=4. |
| `01.3_graded_identity_operator.md` | I_s = P_0 + sP_1 + P_2 for s ∈ {+1, 0, -1}. Three-sweep spectral kernel. Det-trace identity. |
| `01.4_shift_identity_proof.md` | Φ_6(K+1) = Φ_3(K). The interlevel coupling ladder. 21 as the shared rung at K=4↔K=5. |
| `01.5_universal_vertex_reframe.md` | TetA/TetB exchange as background physics. Gravity = spontaneous emission. Portal = stimulated emission. |

### Section 02 — Gravity derivation

| File | Content |
|---|---|
| `02.1_gravity_equation.md` | α_G = (Φ_4(K)/Φ_6(K)) · α^Φ_3(K) · (g_e/2) at K=4. Reduced and matrix-read forms. |
| `02.2_g_factor_breakthrough.md` | Schwinger correction (1 + α/2π) identified as g_e/2 at one loop. No QED import; coupling. |
| `02.3_empirical_verification.md` | G predicted to −12.1 ppm with g_e/2 imported; integer-21 lock to 2.5×10⁻⁶. |
| `02.4_permutation_discrimination.md` | Six permutations of {21, 17, 13} test. (17/13, α^21) uniquely gives integer exponent. |

### Section 03 — Portal topology

| File | Content |
|---|---|
| `03.1_K4_to_K5_hinge.md` | Shell Hamiltonians H_K. The hinge operator J_4 = \|5,-⟩⟨4,+\|. Intertwiner H_5 J_4 = J_4 H_4 = 21 J_4. |
| `03.2_pentachoron_edge_network.md` | K_5^→ has 20 directed edges. α^20 from phase-closed edge product. 21 = 1 + 20. |
| `03.3_S3_hopf_bundle.md` | K=5 shell boundary is S³. Hopf fibration S¹ → S³ → S². g_e/2 as S¹ fiber holonomy. |
| `03.4_icosahedral_A5_structure.md` | 5 sub-tetrahedra of pentachoron. A_5 = icosahedral rotation group. Poincaré sphere Σ(2,3,5) = SU(2)/2I. |
| `03.5_SU2_19_chern_simons.md` | Identification of the apparatus's Chern-Simons level as k=19. Three independent landings. |
| `03.6_WRT_invariant_decomposition.md` | τ_21(Σ(2,3,5)) computed. CRT decomposition Q(ζ_21) = Q(ζ_3)⊗Q(ζ_7) matches apparatus Z_3 × Z_7. |

### Section 04 — Apparatus engineering

| File | Content |
|---|---|
| `04.1_subsystem_overview.md` | Full chamber-by-chamber table. Each subsystem mapped to algebraic function. |
| `04.2_kings_chamber_vertex.md` | All-granite chamber, 20 × 10 × 5√5 cubits; space diagonal √(20² + 10² + (5√5)²) = 25 = K² at K=5 (3-4-5 triangle). Feynman vertex. |
| `04.3_coffer_alpha_step.md` | V_coffer / V_KC ≈ α to 0.1% on Petrie data (floor-to-ceiling height; ±0.4%; 2.3% with wall height). Coffer = primitive Coulomb edge α (conjecture). |
| `04.4_relieving_chambers_pentachoron.md` | Five relieving chambers = 5 vertices of K_5. Inter-chamber Coulomb couplings = 20 directed edges. |
| `04.5_grand_gallery_kernel.md` | 7-corbel phase ramp. Cumulative phase = 21 units of 2π/7. Realizes three-sweep spectral kernel. |
| `04.6_antechamber_Z3_filter.md` | Three portcullis grooves. Z_3 character projector. |
| `04.7_shaft_address_triad.md` | K-shafts (N+S) and Q-shafts (N+S). Gram + chirality + phase triad address. K-Q interferometer reading. |
| `04.8_subsidiary_systems.md` | Descending passage, ascending passage, well shaft, subterranean chamber, Big Void. Function table. |

### Section 05 — Cavity-QED operation

| File | Content |
|---|---|
| `05.1_geomagnetic_pump.md` | Earth's B-field at Giza as the pump. Cardinal alignment as tuning. Pump Rabi frequency. |
| `05.2_material_specification.md` | Gold cap (diamagnetic, conductive, inert). Limestone bulk (dielectric). Granite cavity (high-Q). |
| `05.3_strong_coupling_calculation.md` | g√N/γ_cav ≈ 4 × 10⁷. Apparatus over-pumped by 7 orders of magnitude over threshold. |
| `05.4_purcell_modification.md` | Local α_G inside the chamber modified by cavity coupling. Anomalous local gravity prediction. |
| `05.5_field_flow_architecture.md` | How geomagnetic flux flows through cap → limestone → granite → KC vertex. |

### Section 06 — Master equations

| File | Content |
|---|---|
| `06.1_universal_vertex_operator.md` | V_univ(x) = α_G J_4(x) + g_NL R_x(a,b,c). The always-on vertex. |
| `06.2_portal_operator.md` | P_y←x = A_y† J_{4,y}† M(U,V) α_G J_{4,x} A_x. The full transfer operator. |
| `06.3_mirror_address_functional.md` | M(U,V) in Hopf, A_5, and Z_21 forms. The mirror-conjugation involution. |
| `06.4_two_mode_operation.md` | Gravity (spontaneous) vs portal (stimulated). Same α_G, different kernel. |

### Section 07 — Predictions and tests

| File | Content |
|---|---|
| `07.1_acoustic_Z21_spectrum.md` | 21-mode comb at the King's Chamber 21-band. Z_7 and Z_3 subgroup structure. Measurable. |
| `07.2_coffer_volume_test.md` | Status: 0.1% on Petrie measurements, convention-dependent. Refined-measurement protocol. |
| `07.3_relieving_chamber_volumes.md` | Naive prediction ∑V_i ≈ 81 c³ fails by ~10× on existing dimensions; needs a new formulation before WP1 measures the volumes. |
| `07.4_magnetic_shielding_test.md` | μ-metal in KC kills portal channel. Direct cavity-QED test. |
| `07.5_geomagnetic_storm_correlation.md` | K-index correlation with anomalous apparatus behavior. |
| `07.6_capstone_restoration.md` | Restoring gold cap restores full pump enhancement. |
| `07.7_reversal_archaeology.md` | Pyramid-style apparatus across geomagnetic reversal eras. |

### Section 08 — Open questions

| File | Content |
|---|---|
| `08.1_transition_frequency.md` | ω_{K4→K5} not yet derived. ℏω ~ m_e c² · α^21 conjectured. |
| `08.2_associator_nonlinearity.md` | g_NL coefficient not yet derived from closure-read algebra. |
| `08.3_mass_from_associator.md` | Conjecture: m_e from persistent axial associator residue. Highest-payoff calculation. |
| `08.4_energy_budget.md` | Energy source for portal transfer: pump, address, or TetB sheet? |

### Section 99 — Appendices

| File | Content |
|---|---|
| `A_notation.md` | Symbol glossary. |
| `B_numerical_constants.md` | α, m_e, ℏ, c, geomagnetic B at Giza, etc. |
| `C_cyclotomic_field_decomposition.md` | Q(ζ_21) = Q(ζ_3) ⊗ Q(ζ_7). Galois action. |
| `D_WRT_formula_derivation.md` | Lawrence-Rozansky-Hikami formula for τ_N(Σ(2,3,5)). |
| `E_petrie_measurements.md` | Primary apparatus measurements (Petrie 1883), with uncertainty bands. |

## Authoring conventions

1. **Math.** Inline math uses `$...$`. Display math uses `$$...$$`. LaTeX commands are standard.
2. **Boxed equations.** Use `\boxed{...}` for load-bearing statements. Sparingly.
3. **Cross-references.** Within-file: section headers. Across-file: relative paths from the project root.
4. **Numerical values.** Always cite source (CODATA, Petrie, framework derivation). No unsourced numbers.
5. **Status flags.** Each file's status line at top:
   - `Status: derived` (load-bearing, complete)
   - `Status: structural` (algebraically forced, awaits verification)
   - `Status: conjecture` (motivated, awaiting derivation)
   - `Status: open` (identified but not resolved)
6. **Reading time.** Each file estimated at top.

## Versioning

The single-document predecessor of this project is preserved at `99_appendices/Z_original_synthesis_v1.md`. New material developed in the project supersedes that document where they conflict; the original is kept for reference.

## Related framework documents

This project draws on the GFD framework's other documents. Where relevant, those are cited but not duplicated:

- **Letter 1, 2, 3** (CQG submissions): the core gravity derivation
- **Gram matrix proof v5** (`A Tetrahedral Realization Theorem for the Lorentz Tetrad`): the K=4 forcing
- **Supplementary spatial geometry of the Lorentz tetrad**: stellated octahedron, parity sectors
- **Core gravity framework** (`core_gravity_framework.md`): the minimal algebraic spine
- **Breakthrough g-factor coupling** (`breakthrough_g_factor_coupling.md`): identification of (1+α/2π) as g_e/2

This pyramid project is the engineering application of the same framework to one specific apparatus.

---

*Last updated: 2026-10-27*
