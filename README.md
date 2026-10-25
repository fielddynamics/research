# Field Dynamics — Research Archive

**Gravity Field Dynamics (GFD)** · Stephen Nelson · [Field Dynamics Research](https://fielddynamics.org) · stephen@fielddynamics.org

This repository is the working research archive behind the Gravity Field Dynamics framework and the preprints published on Zenodo. It is published **as is**: derivation notes, synthesis documents, validation scripts, paper sources, interactive visualisations and exploratory experiments, in the state they were left at the end of each research session.

> **Read this first.** This is a lab notebook, not a software package. Folders were created as research threads opened, so naming is informal, some files exist in several versions (`(1)`, `-1`, `- Copy`, `v1`/`v2`), and a few threads were later superseded or abandoned. The published papers in [`papers/`](papers/) and the documentation site at **[docs.fielddynamics.org](https://docs.fielddynamics.org/)** are the curated statements of the framework. Everything else is the trail that led there. The work is independent and has not been peer reviewed.

---

## The framework in one page

GFD proposes that the local gravitational frame has a definite interior geometry: the **stellated octahedron**, two interpenetrating tetrahedra of opposite orientation (**TetA** and **TetB**) sharing a common centre (the **Field Origin**). From that geometry it derives a covariant, zero-free-parameter theory of gravity that reproduces galactic rotation curves without dark matter, and it then follows the same structure into constants, particle masses, nuclear binding and atomic structure.

| Object | Statement |
|---|---|
| Dimension selection | `2(D + 1) = 2^D  ⇒  D = 3`, `K = D + 1 = 4` |
| Tetrad | `g_μν = η_ab e^a_μ e^b_ν` — the 2⁴ sign combinations of the spatial frame give exactly two bounded regions (TetA, TetB) |
| Coupling polynomial | `f(K, s) = 1 + sK + K²` → at K = 4: **21** (TetA, s = +1), **17** (origin, s = 0), **13** (TetB, s = −1) |
| Field equation | `f(x) = (21x + 13)/(x + 1)`, with `x = g_t / a₀` |
| Constitutive law | `μ(x) = (f(x) − 13)/8 = x/(x + 1)` — the "simple" AQUAL/MOND interpolating function, derived rather than fitted |
| Scalar–tensor transition (SST) | `g_s = g_t² / (a₀ + g_t)`, inverted as `g_t = (g_s + √(g_s² + 4 g_s a₀))/2` |
| Kinetic functional | `F(y) = y − 2√y + 2 ln(1 + √y)`, with `dF/dy = μ(√y)` |
| Covariant action | `S = ∫ d⁴x √−g [ R/16πG − (a₀²/8πG) F(y) − ¼ e^{−2Φ/c²} F_μν F^μν + L_m ]` — prefactors 16 = K², 8 = 2^D, 4 = K |
| Connection split | `K³ = 64 = 40 + 24`: GR's torsion-free condition keeps 40 Christoffel components and discards the 24 torsion components, which GFD identifies with TetB |
| Gravitational constant | `G = (17/13) α²¹ ħc / m_e²` |

[`llms.txt`](research/llms.txt) contains the full machine-readable derivation chain, symbol glossary and interpretation rules, and is the best single-file summary of the framework.

---

## Published papers (Zenodo)

Paper PDFs and their LaTeX sources live in [`papers/`](papers/). Two series were published: the numbered **Distributed Field Processing / GFD papers I–XIII** (January–March 2026) and the shorter **tetrad letters** (March 2026 onward).

### Numbered series — Papers I–XIII (January–March 2026)

Papers I–V are single PDFs at the top of `papers/`; several dated revisions of each are kept, and the latest date is the final version. From Paper VI onward each paper has its own folder with sources, revisions, validation scripts and supplementary material.

| # | Title | Where |
|---|---|---|
| I | Distributed Field Processing: The Gravitational Constitutive Law (No Dark Matter Required) | [`2026-01_28_Nelson_DFP_Gravitational_Constitutive_Law.pdf`](papers/2026-01_28_Nelson_DFP_Gravitational_Constitutive_Law.pdf) <!-- Zenodo DOI --> |
| II | A Covariant Theory Without Dark Matter | [`2026-01_28_Nelson_DFPII_A_Covariant_Theory_Without_Dark_Matter.pdf`](papers/2026-01_28_Nelson_DFPII_A_Covariant_Theory_Without_Dark_Matter.pdf) <!-- Zenodo DOI --> |
| III | The Unit of Gravity | [`2026-01_28_Nelson_DFPIII_The_Unit_Of_Gravity.pdf`](papers/2026-01_28_Nelson_DFPIII_The_Unit_Of_Gravity.pdf) <!-- Zenodo DOI --> |
| IV | Deriving Electron Mass from the Hubble Constant — Resolving the Hubble Tension Through Tetrad Topology | [`2026-01_28_Nelson_DFPIV_Resolving_The_Hubble_Tension_Through_Tetrad_Topology.pdf`](papers/2026-01_28_Nelson_DFPIV_Resolving_The_Hubble_Tension_Through_Tetrad_Topology.pdf) <!-- Zenodo DOI --> |
| V | Field Closure and the Topology of Gravity | [`2026-01_29_Nelson_DFPV_Field_Closure_And_The_Topology_Of_Gravity.pdf`](papers/2026-01_29_Nelson_DFPV_Field_Closure_And_The_Topology_Of_Gravity.pdf) — [Zenodo record 18419531](https://zenodo.org/records/18419531) |
| VI | Deriving the Gravitational Constant from Spacetime Topology — The Dual Tetrahedral Field Chambers | [`papers/Paper VI/`](<papers/Paper VI/>) (arXiv-format build in `ArXiv/`, `validation/run_all_validations.py`); earlier PDFs at the top of `papers/` <!-- Zenodo DOI --> |
| VII | Dual Tetrad Topology and the Field Origin: From Nuclear Decay to Galactic Dynamics | [`papers/Paper VII/`](<papers/Paper VII/>) (revisions `v2`–`v7`; `v7` is the latest) <!-- Zenodo DOI --> |
| VIII | Gravity Field Dynamics and Bimetric Gravity: Dual Tetrahedral Field Chambers as the Key to the General Parameters | [`papers/Paper VIII/`](<papers/Paper VIII/>) (`Nelson_2026_GFD_and_Bimetric_Gravity_v1_1.pdf`) <!-- Zenodo DOI --> |
| IX | Gravity Field Dynamics: Complete Field Closure from Stellated Octahedron Topology | [`papers/Paper IX/`](<papers/Paper IX/>) (with `Tests/`, `supplementary/` validation suites and I-Ching closure references) <!-- Zenodo DOI --> |
| X | Two-Scale Kinematics from a Single Scalar-Tensor Transition: Tully–Fisher Evolution and H₀ Without Free Parameters | [`papers/Paper X/`](<papers/Paper X/>) (`sst_two_scale_jcap.pdf`) <!-- Zenodo DOI --> |
| XI | Nuclear Shell Structure and Binding Energies from Tetrahedral Packing at K = 4 | [`papers/Paper XI/`](<papers/Paper XI/>) <!-- Zenodo DOI --> |
| XII | Dual Tetrad Covariance: The GFD Scalar-Tensor Action and the Hassan–Rosen Interaction Potential as Two Projections of a Single Geometry | [`papers/Paper XII/`](<papers/Paper XII/>) (source only) <!-- Zenodo DOI --> |
| XIII | Nuclear Binding Energy from the Bidirectional Scalar-Tensor Transition | [`papers/Paper XIII/`](<papers/Paper XIII/>) (working draft in [`Paper - chemistry-with-sst/`](<papers/Paper - chemistry-with-sst/>)) <!-- Zenodo DOI --> |
| — | Topological Field Closure: A Bidirectional Derivation of the Hubble Constant and the Electron Mass | [`2026-01-26-Topological_Field_Closure_…pdf`](papers/2026-01-26-Topological_Field_Closure_A_Bidirectional_Derivation_of_the_Hubble_Constant_and_the_Electron_Mass.pdf) <!-- Zenodo DOI --> |

### Letters — March 2026 onward

Short, self-contained letters that rebuild the framework from the tetrad equation alone, each with supplementary proofs and a `run_all_validations.py` that checks every number in the paper. Each folder holds `letter.tex` / `letter.pdf`, a cover letter, supplementary notes and the `iopjournal.cls` build.

| Letter | Title | Folder |
|---|---|---|
| 1 | The Coordinate-Space Geometry of the Tetrad Frame | [`papers/Paper Gravity-Simple/`](<papers/Paper Gravity-Simple/>) <!-- Zenodo DOI --> |
| — | The Gravitational Constitutive Law from the Tetrad Frame Geometry | [`papers/Paper Constitutive Law/`](<papers/Paper Constitutive Law/>) <!-- Zenodo DOI --> |
| 2 | The Other Half of Gravity: Torsion and the Two-Chamber Structure of the Tetrad Frame | [`papers/Paper - The other half of gravity/`](<papers/Paper - The other half of gravity/>) (v1, v2) <!-- Zenodo DOI --> |
| 3 | Gravity Field Dynamics: Field Closure of the Tetrad Frame | [`papers/Paper - holy shiznizzle it's a disc/`](<papers/Paper - holy shiznizzle it's a disc/>) <!-- Zenodo DOI --> |
| — | The Radial Acceleration Relation from a Zero-Parameter Covariant Action (SPARC: 164 galaxies, 3284 points) | [`papers/Paper - Sparc galaxy RAR with SST quadratic/`](<papers/Paper - Sparc galaxy RAR with SST quadratic/>) <!-- Zenodo DOI --> |

### Manuscripts in preparation (sources only)

| Title | Source |
|---|---|
| The Gram Matrix of the Tetrad Equation | [`papers/Paper - Lions and tigers and bears/`](<papers/Paper - Lions and tigers and bears/>) |
| An Algebraic Origin for the Simple AQUAL Interpolation Function | [`papers/Paper - u(x) with coupling poly/gfd_phase1_letter_final.tex`](<papers/Paper - u(x) with coupling poly/gfd_phase1_letter_final.tex>) |
| The Torsion Sector of the Tetrad Connection as the Regular Representation of S₄ | [`papers/Paper - u(x) with coupling poly/gfd_paper_b_torsion_S4.tex`](<papers/Paper - u(x) with coupling poly/gfd_paper_b_torsion_S4.tex>) |
| The Hadamard Sign Kernel of the Tetrahedral Frame | [`papers/Paper - u(x) with coupling poly/gfd_paper_c_hadamard_tetrad.tex`](<papers/Paper - u(x) with coupling poly/gfd_paper_c_hadamard_tetrad.tex>) |
| Closed-Form Energy Functional for the Simple Interpolating Function in AQUAL | [`papers/paper u(x) from aqual/`](<papers/paper u(x) from aqual/>) |

---

## Repository map

The repository has two top-level folders: [`papers/`](papers/) (above) and [`research/`](research/), which holds every research thread. The tables below describe the contents of `research/`.

Most research folders follow the same pattern: a **`*_synthesis.md`** that explains the result in prose, and a **Python suite** (often named `*_20.py`, `*_enterprise_*.py` or `*_validation.py`) that checks every claim numerically and prints PASS/FAIL. Read the synthesis first, then run the suite.

### Framework core ([`research/`](research/))

| File | What it is |
|---|---|
| [`llms.txt`](research/llms.txt) | Machine-readable specification of the framework: equations, dependency chain, glossary |
| [`gfd_algebra.py`](research/gfd_algebra.py) | Every algebraic object used in the RAR letter and its supplementary proofs, with self-checks |
| [`gfd_enterprise_validation-v2.py`](research/gfd_enterprise_validation-v2.py) | The main end-to-end validation: stellated octahedron from `2(D+1) = 2^D`, coupling polynomial, constitutive law, gauge structure (v1 kept for reference) |
| [`gfd_fundamental_constants.py`](research/gfd_fundamental_constants.py) | Capstone suite: G, α, θ_W, H₀ and field-equation prefactors derived from {K, D} |

### Gravity, galaxies and cosmology

| Folder | Contents |
|---|---|
| [`constitutive-law-u(x)/`](<research/constitutive-law-u(x)/>) | Constitutive law suites and TetA/TetB roulette visualisations |
| [`galaxy-rotation/`](research/galaxy-rotation/) | Rotation-curve pipeline, interior/exterior synthesis, mass decoding, vortex viewers |
| [`cdm/`](research/cdm/) | Translation of the cold-dark-matter halo into the TetB interior of the field |
| [`cmb/`](research/cmb/) | CMB gravitational enhancement, Compton-to-Hubble chain, velocity exponent |
| [`g_from_topology/`](research/g_from_topology/) | G as a matrix read; one-loop (Schwinger) correction to G |
| [`field-closure/`](research/field-closure/) | Derivation chain GR → coupling polynomial; why the closure walk produces π |
| [`bbp and pi field closure stepping/`](<research/bbp and pi field closure stepping/>) | The BBP π formula read as field closure |
| [`bound-gravity-and-packing/`](research/bound-gravity-and-packing/) | Gravity field packing, one field in two states |
| [`quantum gravity/`](<research/quantum gravity/>) | Contact with Regge / LQG / spin-foam programs; two-state Hilbert space of the octahedral core |
| [`deep-structure/`](research/deep-structure/) | Number-theoretic and topological structure of K = 4 |
| [`polynomial coupling fn/`](<research/polynomial coupling fn/>) | Structural analysis of `f(K, s)`, Sierpiński structure, prime sieve |
| [`faces/`](research/faces/) | "Enterprise Triforce" 40-test face-structure suite |
| [`hawking/`](research/hawking/) | Notes on information preservation |

### Particles, nuclei and atoms

| Folder | Contents |
|---|---|
| [`em/`](research/em/) | Electromagnetic sector: gauge structure S₄ → A₄ → V₄, coupling constants |
| [`mass-spectrum-particle-physics/`](research/mass-spectrum-particle-physics/) | Particle mass spectrum from A₄ → V₄ × Z₃ |
| [`proton/`](research/proton/) | Proton–electron mass ratio proof chain |
| [`photonic/`](research/photonic/) | Photon equations, "light substrate" suites and teaching notes |
| [`nuclear/`](research/nuclear/), [`nuclear-triforce/`](research/nuclear-triforce/) | Nuclear binding from the constitutive law; intersection with the face suite |
| [`matter/`](research/matter/) | Nuclear binding (Bethe–Weizsäcker coefficients, 3-scale model, Sierpiński walk), electron configurations, particle properties; includes the neural-network experiments (`sierpinski - nn breakthrough/`) that led to the closed-form binding formula |
| [`valance-shells-nailed/`](research/valance-shells-nailed/) | Electron configuration / Madelung rule from the coupling polynomial |
| [`atomic-properties/`](research/atomic-properties/), [`atom-vortex-horizon/`](research/atom-vortex-horizon/) | Overdetermined atomic predictions; the vortex horizon picture of the atom |

### Computation and signal processing

| Folder | Contents |
|---|---|
| [`quantum compute/`](<research/quantum compute/>) | The GFD oscillator (Kuramoto-type phase + amplitude dynamics) applied to Max-Cut, colouring, TSP, community detection and mazes; t-bit algebra; Walsh-bridge gate recognition; oscillator-based unsupervised learning. Subfolders `GFD oscillator v2/` and `Oscillator learning/` have their own READMEs |
| [`spectral/`](research/spectral/) | Walsh–Hadamard spectral kernel (PyTorch) |
| [`3 sweep understanding/`](<research/3 sweep understanding/>) | Closure-algebra pipeline and Walsh-spectral compute primitive syntheses |
| [`i-ching/`](research/i-ching/) | π base-8 closure walk on the stellated octahedron, traversal and tetragram analyzers |
| [`antenna theory/`](<research/antenna theory/>) | Resonant coupling through the Field Origin |

### Speculative and exploratory threads

These folders apply the framework well outside conventional physics and are kept for completeness. They should be read as exploration, not as results.

| Folder | Contents |
|---|---|
| [`great-pyramid/`](research/great-pyramid/) | A structured compendium treating the Great Pyramid as a cavity apparatus, with its own README, ~35 working notes and a Python package with tests |
| [`earth-365-days/`](research/earth-365-days/) | Note on the 365/360 relation |
| [`formalisms-tetrad/`](research/formalisms-tetrad/) | Literature-search notes on tetrahedral formalisms |
| [`temp/`](research/temp/) | Scratch work |

### External reference material

[`stellated octahedron geometry/On the 14-Octahedron Backbone of the Bimetric.pdf`](<research/stellated octahedron geometry/On the 14-Octahedron Backbone of the Bimetric.pdf>) is a third-party paper by Bruno R. Galeffi, kept as background reading. It is not part of the GFD work.

---

## Running the code

The scripts are standalone research code, not an installable package. Most need only Python 3 and NumPy; some use the extras below.

```bash
pip install numpy scipy mpmath matplotlib pytest
pip install torch        # spectral kernel, neural-network experiments, some oscillator work
```

Typical entry points:

```bash
python research/gfd_enterprise_validation-v2.py           # core framework validation
python research/gfd_fundamental_constants.py            # constants from {K, D}
python research/gfd_algebra.py                      # algebra self-checks (silent = pass)
python "papers/Paper Gravity-Simple/Supplementary/run_all_validations.py"
python "research/quantum compute/GFD oscillator v2/run_all.py"
cd research/great-pyramid/pyramid_portal_research/python && python -m pytest tests
```

Notes:

- Many paths contain spaces and parentheses; quote them in the shell.
- Scripts are generally meant to be run from their own folder.
- A few files under `research/great-pyramid/field_origin_geometry/`, `research/i-ching/` and `papers/Paper IX/Tests/` import `gravity_field_model` from the companion model repository (`dfp-gravity-field-model`) and will not run without it.
- Trained model weights (`*.pt`), zipped code bundles and LaTeX build artefacts (`.aux`, `.log`, `.out`) are committed as they were produced.

---

## Citing

Please cite the relevant Zenodo preprint for any result taken from this archive. For the framework as a whole, cite the latest letters above or the documentation at [docs.fielddynamics.org](https://docs.fielddynamics.org/).

No open-source licence file is included. For reuse beyond citation and reading, contact the author.

## Contact

Stephen Nelson — Field Dynamics Research
[fielddynamics.org](https://fielddynamics.org) · [docs.fielddynamics.org](https://docs.fielddynamics.org/) · stephen@fielddynamics.org
