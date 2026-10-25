# Field Dynamics — Research Archive

**Gravity Field Dynamics (GFD)** · Stephen Nelson · [Field Dynamics Research](https://fielddynamics.org) · stephen@fielddynamics.org

This repository is the working research archive behind the Gravity Field Dynamics framework and the preprints published on Zenodo. It is published **as is**: derivation notes, synthesis documents, validation scripts, paper sources, interactive visualisations and exploratory experiments, in the state they were left at the end of each research session.

> **Read this first.** This is a lab notebook, not a software package. Folders were created as research threads opened, so naming is informal, some files exist in several versions (`(1)`, `-1`, `- Copy`, `v1`/`v2`), and a few threads were later superseded or abandoned. The published papers in [`papers/`](papers/) and the documentation in [`docs/`](docs/README.md) are the curated statements of the framework. Everything else is the trail that led there. The work is independent and has not been peer reviewed.

---

## Statement on open release

This programme has been carried out by a single independent investigator, Stephen Nelson of Field Dynamics Research. It has now reached a point where its open questions exceed what one researcher can responsibly pursue. The derivations require independent verification, the empirical comparisons call for scrutiny by specialists in each domain, and several lines of inquiry remain unresolved.

In the spirit of open science, the complete research record is therefore released here without restriction of access. That record comprises the published preprints, the manuscripts in preparation, the validation code and the working notes from which they were developed. It is offered not as a finished body of results but as a starting point for critical examination, replication and extension by the wider research community.

Engagement of every kind is welcome:

- independent checks of the mathematical derivations;
- re-analysis of the observational and experimental comparisons;
- identification of errors, gaps or unstated assumptions;
- collaboration on the open problems.

Negative results and well-founded criticism are regarded as contributions of equal value. Correspondence may be directed to stephen@fielddynamics.org, or raised as an issue on this repository.

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

For a guided explanation of each step, start with the [documentation](docs/README.md): Foundations, Gravitation, Fundamental Constants and Galactic Dynamics. [`llms.txt`](research/llms.txt) contains the full machine-readable derivation chain, symbol glossary and interpretation rules, and is the best single-file summary of the framework.

---

## Published papers (Zenodo)

Paper PDFs and their LaTeX sources live in [`papers/`](papers/). Two series were published: the numbered **Distributed Field Processing / GFD papers I–XIII** (January–March 2026) and the shorter **tetrad letters** (March 2026 onward). Each description below summarises the paper's own claim.

### Numbered series — Papers I–XIII (January–March 2026)

Papers I–V are single PDFs at the top of `papers/`; several dated revisions of each are kept, and the latest date is the final version. From Paper VI onward each paper has its own numbered folder with sources, revisions, validation scripts and supplementary material.

**I — The Gravitational Constitutive Law (No Dark Matter Required)**
[`2026-01_28_Nelson_DFP_Gravitational_Constitutive_Law.pdf`](papers/2026-01_28_Nelson_DFP_Gravitational_Constitutive_Law.pdf) — [doi:10.5281/zenodo.18332595](https://doi.org/10.5281/zenodo.18332595)
Asks why MOND's interpolating function has the form it does. From the requirement that gravitational field coupling be lossless and locally evaluable, it derives μ(x) = x/(1 + x) as the unique equilibrium solution instead of a curve-fit choice.

**II — A Covariant Theory Without Dark Matter**
[`2026-01_28_Nelson_DFPII_A_Covariant_Theory_Without_Dark_Matter.pdf`](papers/2026-01_28_Nelson_DFPII_A_Covariant_Theory_Without_Dark_Matter.pdf) — [doi:10.5281/zenodo.18360354](https://doi.org/10.5281/zenodo.18360354)
Extends Paper I to cosmological scales. Using a₀ = cH₀/2π and the geometry of tetrahedral closure packing, it derives a gravitational enhancement of 6.46 at recombination against the ≈ 6.4 that Planck's CMB peaks require, without cold dark matter.

**III — The Unit of Gravity**
[`2026-01_28_Nelson_DFPIII_The_Unit_Of_Gravity.pdf`](papers/2026-01_28_Nelson_DFPIII_The_Unit_Of_Gravity.pdf) — [doi:10.5281/zenodo.18362768](https://doi.org/10.5281/zenodo.18362768)
Asks what sets the size of the gravitational field tile. An electromagnetic route and a gravitational-topology route both land on ≈ 2.82 fm, the classical electron radius, which the paper identifies as the unit of gravity.

**IV — Resolving the Hubble Tension Through Tetrad Topology**
[`2026-01_28_Nelson_DFPIV_Resolving_The_Hubble_Tension_Through_Tetrad_Topology.pdf`](papers/2026-01_28_Nelson_DFPIV_Resolving_The_Hubble_Tension_Through_Tetrad_Topology.pdf) — [doi:10.5281/zenodo.18371849](https://doi.org/10.5281/zenodo.18371849)
Projects the flat-space MOND value H₀ = 78.9 km/s/Mpc through the k = 4 tetrad topology to obtain 69.92 km/s/Mpc, and runs the same chain in reverse to derive the electron mass from the measured Hubble constant.

**V — Field Closure and the Topology of Gravity**
[`2026-01_29_Nelson_DFPV_Field_Closure_And_The_Topology_Of_Gravity.pdf`](papers/2026-01_29_Nelson_DFPV_Field_Closure_And_The_Topology_Of_Gravity.pdf) — [doi:10.5281/zenodo.18419531](https://doi.org/10.5281/zenodo.18419531)
Explains why the number four recurs across ADM, tetrad gravity, Loop Quantum Gravity, Regge calculus and LIGO's two polarizations, via the simplex theorem, and connects the tetrahedron of those formalisms to the Field Chamber of this framework.

**VI — Deriving the Gravitational Constant from Spacetime Topology**
[`papers/06-gravitational-constant-from-topology/`](papers/06-gravitational-constant-from-topology/) — [doi:10.5281/zenodo.18463038](https://doi.org/10.5281/zenodo.18463038)
Argues that spinor theory, chiral gravity, ghost-free bimetric gravity and stability analysis all require two oppositely oriented tetrahedra, and from that dual-chamber structure derives Newton's constant with no adjustable parameters. Includes an arXiv-format build and `validation/run_all_validations.py`.

**VII — Dual Tetrad Topology and the Field Origin: From Nuclear Decay to Galactic Dynamics**
[`papers/07-dual-tetrad-topology-field-origin/`](papers/07-dual-tetrad-topology-field-origin/) <!-- Zenodo DOI -->
Derives the stellated octahedron as the minimal closure topology in 3+1 dimensions and builds a covariant scalar-tensor action from it, testing predictions from the neutron-lifetime beam–bottle discrepancy to Milky Way rotation. Revisions `v2`–`v7` are kept; `v7` is the latest.

**VIII — Gravity Field Dynamics and Bimetric Gravity**
[`papers/08-gfd-and-bimetric-gravity/`](papers/08-gfd-and-bimetric-gravity/) <!-- Zenodo DOI -->
Shows how the coupling polynomial fixes the five free Hassan–Rosen bimetric coefficients to {1, 0, 16, 0, 1}, while its continuous form gives the field equation f(x) = (21x + 13)/(x + 1) and the constitutive law.

**IX — Complete Field Closure from Stellated Octahedron Topology**
[`papers/09-complete-field-closure/`](papers/09-complete-field-closure/) <!-- Zenodo DOI -->
Derives both the topology and the closure condition of gravity from the single equation 2(d + 1) = 2^d, whose only solution d = 3 fixes K = 4 and produces the stellated octahedron and the 3+1 split. Comes with the largest test collection (`Tests/`, `supplementary/`).

**X — Two-Scale Kinematics from a Single Scalar-Tensor Transition**
[`papers/10-two-scale-kinematics-tully-fisher-h0/`](papers/10-two-scale-kinematics-tully-fisher-h0/) <!-- Zenodo DOI -->
Applies the same SST equation at galactic and cosmological scales to predict the redshift evolution of the baryonic Tully–Fisher relation to z = 3 and H₀ = 70.21 km/s/Mpc, with a ±6% band containing both the Planck and SH0ES values.

**XI — Nuclear Shell Structure and Binding Energies from Tetrahedral Packing at K = 4**
[`papers/11-nuclear-shells-tetrahedral-packing/`](papers/11-nuclear-shells-tetrahedral-packing/) <!-- Zenodo DOI -->
Gives a one-line binding-energy formula from the coupling polynomial, tested across the stable elements from hydrogen to bismuth, and a tetrahedral packing algebra that produces all seven nuclear magic numbers.

**XII — Dual Tetrad Covariance: The GFD Action and the Hassan–Rosen Potential as Two Projections of a Single Geometry**
[`papers/12-dual-tetrad-covariance-hassan-rosen/`](papers/12-dual-tetrad-covariance-hassan-rosen/) (source only) <!-- Zenodo DOI -->
Develops Paper VIII into a term-by-term correspondence between the two actions, locks the bimetric coefficients through three theorems and three axioms, and checks the result against six concordance tests (expansion history, BBN, CMB, Vainshtein screening, Galileon hierarchy, mixing angle).

**XIII — Nuclear Binding Energy from the Bidirectional Scalar-Tensor Transition**
[`papers/13-nuclear-binding-bidirectional-sst/`](papers/13-nuclear-binding-bidirectional-sst/) <!-- Zenodo DOI -->
Uses the SST quadratic, the same equation used for galaxy rotation curves, evaluated along a 64-step walk to reproduce the seven magic numbers (including the 20 → 28 gap without spin–orbit coupling) and binding energy per nucleon from helium to lead. The earlier draft is in `working-draft/`.

**Companion — Topological Field Closure: A Bidirectional Derivation of the Hubble Constant and the Electron Mass**
[`2026-01-26-Topological_Field_Closure_…pdf`](papers/2026-01-26-Topological_Field_Closure_A_Bidirectional_Derivation_of_the_Hubble_Constant_and_the_Electron_Mass.pdf) <!-- Zenodo DOI -->
A short paper presenting the Hubble-constant ↔ electron-mass link from Papers III–IV as a bidirectional test: forward from electron properties to H₀, and in reverse from H₀ to the electron mass.

### Tetrad letters — March 2026 onward

Short, self-contained letters that rebuild the framework from the tetrad equation alone. Each folder holds `letter.tex` / `letter.pdf`, a cover letter, supplementary proofs and, in most cases, a `run_all_validations.py` that checks every number in the letter.

**Letter 1 — The Coordinate-Space Geometry of the Tetrad Frame**
[`papers/letter-1-tetrad-frame-geometry/`](papers/letter-1-tetrad-frame-geometry/) <!-- Zenodo DOI -->
Takes the four half-space inequalities of a single orthonormal tetrad and shows that their 16 sign combinations give exactly two bounded regions, which together form a stellated octahedron. No second frame is assumed; every structural constant reduces to K = 4 and D = 3.

**Letter — The Gravitational Constitutive Law from the Tetrad Frame Geometry**
[`papers/letter-constitutive-law-tetrad-geometry/`](papers/letter-constitutive-law-tetrad-geometry/) <!-- Zenodo DOI -->
Derives the AQUAL interpolating function μ(x) = x/(x + 1) by three independent routes: the rank structure of the metric, equilibrium field closure, and the exchange symmetry between the tetrad's two bounded regions.

**Letter 2 — The Other Half of Gravity: Torsion and the Two-Chamber Structure of the Tetrad Frame**
[`papers/letter-2-other-half-of-gravity-torsion/`](papers/letter-2-other-half-of-gravity-torsion/) (`v1`, `v2`) <!-- Zenodo DOI -->
Proves that a torsion-free connection cannot tell the two tetrahedral chambers apart, so the 24 torsion components that general relativity discards are what carry the TetA/TetB distinction. The TetB field fraction comes out as 1/(x + 1).

**Letter 3 — Gravity Field Dynamics: Field Closure of the Tetrad Frame**
[`papers/letter-3-field-closure-of-tetrad-frame/`](papers/letter-3-field-closure-of-tetrad-frame/) <!-- Zenodo DOI -->
Shows that the torsion-free condition keeps the s = +1 projection of the coupling polynomial (40 components) and discards the s = −1 projection (24 components). Restoring them gives the full 64-component connection, which the constitutive law partitions spatially.

**Letter — The Radial Acceleration Relation from a Zero-Parameter Covariant Action**
[`papers/letter-radial-acceleration-relation-sparc/`](papers/letter-radial-acceleration-relation-sparc/) <!-- Zenodo DOI -->
Shows that the radial acceleration relation follows kinematically from the covariant action with F(y) written out explicitly, and tests it against the SPARC database (164 galaxies, 3284 points), reaching 0.181 dex scatter with no fitted parameters.

### Manuscripts in preparation (sources only)

**The Gram Matrix of the Tetrad Equation** — [`papers/gram-matrix-of-tetrad-equation/`](papers/gram-matrix-of-tetrad-equation/)
Treats the tetrad equation as a Gram matrix: its two sign-related solutions give a tetrahedron, its inverse and their stellated-octahedron compound, and the affine connection splits canonically as 24 + 16 + 24 = 64.

**Papers A, B and C** — [`papers/algebraic-papers-a-b-c/`](papers/algebraic-papers-a-b-c/)
- *A — An Algebraic Origin for the Simple AQUAL Interpolation Function* (`gfd_phase1_letter_final.tex`): derives μ(x) = x/(1 + x) from the reciprocal ℤ₂ structure of the tetrad-frame sector algebra, whose parity-weighted trace is f(K, s).
- *B — The Torsion Sector of the Tetrad Connection as the Regular Representation of S₄* (`gfd_paper_b_torsion_S4.tex`): shows that at K = 4 the 24-dimensional torsion sector carries the regular representation of S₄, and so contains the sign (parity) representation that the Christoffel sector lacks.
- *C — The Hadamard Sign Kernel of the Tetrahedral Frame* (`gfd_paper_c_hadamard_tetrad.tex`): identifies the 4 × 4 Hadamard matrix of signal processing, the sign skeleton of the isotropic tetrad and the axis structure of the stellated octahedron as one object.

**Closed-Form Energy Functional for the Simple Interpolating Function in AQUAL** — [`papers/closed-form-aqual-energy-functional/`](papers/closed-form-aqual-energy-functional/)
Gives the closed form F(y) = y − 2√y + 2 ln(1 + √y) for μ(x) = x/(x + 1), so the AQUAL action can be written explicitly instead of only through its derivative.

---

## Repository map

The repository has three top-level folders:

| Folder | Contents |
|---|---|
| [`papers/`](papers/) | The published and in-preparation papers (above) |
| [`docs/`](docs/README.md) | The framework documentation: 28 completed pages copied from the documentation site, as readable Markdown. The full site is available as a Flask app in the [fielddynamics/docs](https://github.com/fielddynamics/docs) repository |
| [`research/`](research/) | Every research thread, described in the tables below |

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
| [`antenna theory/`](<research/antenna theory/>) | Resonant coupling through the Field Origin |

### Exploratory work — [`research/exploratory/`](research/exploratory/)

These threads apply the framework's structures well outside conventional physics. They are kept apart from the main research record and are offered as exploration, not as results.

| Folder | Contents |
|---|---|
| [`great-pyramid/`](research/exploratory/great-pyramid/) | A structured compendium treating the Great Pyramid as a cavity apparatus, with its own README, ~35 working notes and a Python package with tests |
| [`i-ching/`](research/exploratory/i-ching/) | π base-8 closure walk on the stellated octahedron, read through I-Ching trigram structure; traversal and tetragram analyzers |

### Other notes

| Folder | Contents |
|---|---|
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
python papers/letter-1-tetrad-frame-geometry/Supplementary/run_all_validations.py
python "research/quantum compute/GFD oscillator v2/run_all.py"
```

Notes:

- Many paths contain spaces and parentheses; quote them in the shell.
- Scripts are generally meant to be run from their own folder.
- A few files under `research/exploratory/great-pyramid/field_origin_geometry/`, `research/exploratory/i-ching/` and `papers/09-complete-field-closure/Tests/` import `gravity_field_model` from the companion model repository (`dfp-gravity-field-model`) and will not run without it.
- Trained model weights (`*.pt`), zipped code bundles and LaTeX build artefacts (`.aux`, `.log`, `.out`) are committed as they were produced.

---

## Citing

Please cite the relevant Zenodo preprint for any result taken from this archive. For the framework as a whole, cite the latest letters above or the [documentation](docs/README.md).

## Licence

This repository is released under the [MIT License](LICENSE) © 2026 Stephen Nelson, Field Dynamics Research. The code, notes and paper sources may be used, modified and redistributed, provided the copyright and licence notice are retained. Papers deposited on Zenodo also carry the licence shown on their Zenodo records.

## Contact

Stephen Nelson — Field Dynamics Research
[fielddynamics.org](https://fielddynamics.org) · [documentation](docs/README.md) · stephen@fielddynamics.org
