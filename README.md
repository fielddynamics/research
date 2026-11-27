<div align="center">

# Gravity Field Dynamics

### Dual-tetrad geometry · Distributed Field Processing · Recursive field closure

**A research framework investigating gravity as a locally settled, geometrically closed field.**

[Field Dynamics Research](https://fielddynamics.org) · [Documentation](docs/README.md) · [Formal proofs](proofs/README.md) · [Research index](RESEARCH_INDEX.md)

[![Licence: MIT](https://img.shields.io/badge/licence-MIT-blue.svg)](LICENSE) [![Formal proofs](https://img.shields.io/badge/formal_proofs-26-2563eb.svg)](proofs/README.md) [![Lean 4](https://img.shields.io/badge/Lean_4-18_formalisations-7c3aed.svg)](proofs/README.md) [![Research status](https://img.shields.io/badge/status-preprints_·_letters_under_review-64748b.svg)](#status-and-known-limitations)

Stephen Nelson · [ORCID 0009-0008-6190-3269](https://orcid.org/0009-0008-6190-3269) · stephen@fielddynamics.org

</div>

---

Gravity Field Dynamics (GFD) begins with a question: **does the metric describe the entire gravitational structure of the tetrad from which it is constructed?**

The tetrad equation admits parity-related orientation sectors that produce the same metric. Under the spatial-realisation premises established in the repository, they form two interlocking tetrahedra: **TetA**, the observable spacetime sector, and **TetB**, the dual chamber, coupled through the **Field Origin**. GFD proposes that both participate in the gravitational field and that field objects settle their own internal accounting before registering with the surrounding NET Field.

This joins three research directions: the geometry of the tetrad, a constitutive law selected within a stated class of exchange-symmetric laws, and a distributed architecture for gravitational closure. From one measured scale, $a_0$, the framework derives the radial acceleration relation on SPARC with nothing fitted per galaxy, recovers Newton and general relativity exactly inside drainless star systems, decodes mass directly from rotation curves, and derives Newton's constant and the electron mass from the integers of its coupling polynomial.

![Framework overview: geometry, constitutive response, and distributed closure](diagrams/gfd-readme-architecture.svg)

> **Research status:** An open research framework. The repository holds 26 proof packages, 2,062 scripted checks and 18 Lean 4 formalisations, each stating its premises. The mathematics is machine-checked; TetB is the tetrad's second root, and the physical premises each result needs are stated and tested against data. The papers are preprints, and Tetrad Letters 1–3 are under review at *Classical and Quantum Gravity*.

## Results on SPARC

| Galaxies | Rotation-curve points | GFD residual scatter | Galaxy-specific gravitational fit parameters |
| :---: | :---: | :---: | :---: |
| **164** | **3,284** | **0.181 dex** | **0** |

![SPARC radial acceleration relation: GFD and the empirical fit, with residual distributions](papers/letter-radial-acceleration-relation-sparc/sparc_rar.png)

The figure compares the GFD spherical, static weak-field relation with the radial acceleration relation of McGaugh, Lelli & Schombert (2016). The dataset includes SPARC galaxies with quality flag Q ≤ 2. The baryonic inputs use the standard fixed stellar mass-to-light ratios of 0.5 for disks and 0.7 for bulges at 3.6 μm, and the shared empirical acceleration scale $a_0 \approx 1.2\times10^{-10}\ \mathrm{m\,s^{-2}}$.

| Relation | Mean residual | Scatter |
|---|---:|---:|
| GFD | −0.027 dex | 0.181 dex |
| McGaugh et al. empirical fit | −0.022 dex | 0.182 dex |

The GFD prediction uses the positive root of its spherical field equation:

$$g_{\rm obs}=\frac{g_{\rm bar}+\sqrt{g_{\rm bar}^2+4a_0g_{\rm bar}}}{2}.$$

The formula is exact in spherical symmetry; applying the algebraic relation to disk-galaxy rotation-curve components is the approximation used in this observational test, not a full three-dimensional solution for each galaxy.

![Stacked SPARC residuals for the GFD, standard MOND and bound laws](diagrams/gfd-readme-sparc-residuals.svg)

The stacked median residuals of the simple law remain within ±0.05 dex over the displayed bins. The standard MOND function and the bound law exhibit different residual shapes. Because $a_0$ is empirical in this comparison, the shape of the residuals, not their overall normalization, is the relevant comparison. GFD and simple-function MOND share the same algebraic RAR on SPARC. **The difference is that MOND chose this function to fit the data; GFD derives it from the tetrad**, and then says where it acts (drained fields only), which is where the two part ways: Cassini, globular clusters and wide binaries.

[Read the SPARC letter](papers/letter-radial-acceleration-relation-sparc/) · [Reproduce the figure](#verification) · [Full results and references](RESEARCH_INDEX.md#results-on-sparc)

---

## Start here

| Reading path | Entry point | Continue with |
|---|---|---|
| **The observational puzzle** | [The Other Root](THE_MISSING_MASS.md) | [SPARC results](#results-on-sparc) and [mass decoding](papers/letter-decoding-mass-from-rotation-curves/) |
| **Geometry and Einstein's equation** | [Einstein's Equation as the TetA Partition](EINSTEIN_TETA_PARTITION.md) | [The Twenty-Four That Were Set Aside](FIELD_CLOSURE_OF_THE_TETRAD_FRAME.md) |
| **Why TetB is the subspace** | [TetB Is the Subspace: Why 3+1 Spacetime Is TetA](TETB_THE_SUBSPACE.md) | [The Field Origin vertex: resonance and nonspatial transfer](research/hadamard-null-cone-vortex-flywheel/FIELD_ORIGIN_VERTEX.md) |
| **Local to cosmic closure** | [Closure of Closures](CLOSURE_OF_CLOSURES.md) | [Field Closure and Snapshot Accounting](FIELD_CLOSURE_AND_SNAPSHOT_ACCOUNTING.md) |
| **Mathematical architecture** | [Field Closure and Recursive Registration](FIELD_CLOSURE_AND_RECURSIVE_REGISTRATION.md) | [Read-Settle-Register bridge](research/read-settle-register-bridge/READ_SETTLE_REGISTER_BRIDGE.md) and [formal proof index](proofs/README.md) |
| **Full technical reference** | [GFD Coles Notes](GFD_COLES_NOTES.md) | [Machine-readable specification](llms.txt) and [complete research index](RESEARCH_INDEX.md) |

## What is GFD?

### 01 · The geometry: two chambers, one metric

<img src="docs/01-foundations/assets/stellated_octahedron.png" alt="Stellated octahedron, the compound of two interlocking tetrahedra" width="330" align="right">

The tetrad equation is quadratic in the frame:

$$g_{\mu\nu}=\eta_{ab}e^a{}_{\mu}e^b{}_{\nu}.$$

It fixes $(\det e)^2$, not the orientation sign. With a fixed future-pointing time leg, two spatial orientation sectors remain. The [forced-frame theorem](proofs/forced-tetrahedral-frame/) derives the regular tetrahedron under equal magnitude, equal relation, distinctness and three spatial dimensions. The [half-space proof](proofs/half-space-two-bounded-regions/) then establishes that exactly two of sixteen sign selections are bounded. Their compound is the stellated octahedron; the [scheme proof](proofs/tetrad-scheme-two-bounded-regions/) supplies a second route to the parity pair.

TetA is the observable exterior, TetB is the dual throat interior, and the Field Origin is their coupling region. **TetB is not an added assumption: it is the tetrad equation's second root.** General relativity keeps one root by the convention of restricting to $SO^+(1,3)$; GFD keeps both. TetB is not reverse time, and the galactic deep field is not TetB itself.

<br clear="right">

The structural parameters are $K=4$ (faces) and $D=3$ (spatial dimensions). The coupling polynomial organizes the three structural states:

$$f(K,s)=1+sK+K^2.$$

| TetA | Field Origin | TetB |
|:---:|:---:|:---:|
| $s=+1$ | $s=0$ | $s=-1$ |
| **21** | **17** | **13** |

The values count structural coupling channels in the framework; they are not particle counts. See the [geometry documentation](docs/README.md) and the [tetrad letters](#papers).

### 02 · The constitutive response: a closed partition

<img src="diagrams/gfd-capacity-curve.svg" alt="Continuous capacity from 13 through 17 to 21" width="390" align="right">

The [exchange-symmetry](proofs/constitutive-law-exchange-symmetry/) and [tug-of-war](proofs/constitutive-law-tug-of-war/) proofs select the simple constitutive law from exchange symmetry and the stated screening and degree-one conditions (equivalently, within the screening family, flat asymptotic rotation curves):

$$\mu(x)=\frac{x}{1+x},\qquad x=\frac{g_t}{a_0}.$$

$$\mu(1/x)=1-\mu(x).$$

In a quiet drained field, TetA's share is $\mu$ and TetB's is $1-\mu$, so the field splits as $g_t=\mu g_t+(1-\mu)g_t$, where the TetB part is exactly $(1-\mu)g_t=\mu a_0$: a tug of war in which TetA pulls with $g_t$ and TetB with $a_0$. At $x=1$ the shares are equal; the continuous capacity $f(x)=17+4(2\mu-1)=(21x+13)/(x+1)$ connects the polynomial states with the constitutive response.

<br clear="right">

The geometry selects the form of the law; the scale $a_0$ is tied to the electron through closure saturation, $a_0=K^2Gm_e/r_e^2$ ([constants](#derived-constants)).

### 03 · The connection: what the metric cannot distinguish

![The 64-component connection and its 40/24 projection](diagrams/gfd-connection-projection.svg)

The affine connection has $4^3=64$ components. Lower-index exchange decomposes it into 40 symmetric and 24 antisymmetric components. For a fixed metric, a metric-compatible connection differs from the Levi-Civita connection through its contorsion. The [Gram-matrix theorem](proofs/gram-matrix-tetrad-equation/) establishes root-blind self-coupling and relative-root cross-coupling; the orientation-dependent dual of torsion can distinguish orientation sectors. The [torsion representation](proofs/torsion-regular-representation/) identifies the regular representation of $S_4$ under the specified permutation action.

Letter 2 proves the 24 torsion components are TetB's carrier, while the 40 torsion-free components are root-blind: the metric and Christoffel connection cannot see which root they came from. That is why general relativity, built on the 40, is the TetA partition. The [Read-Settle-Register bridge](research/read-settle-register-bridge/READ_SETTLE_REGISTER_BRIDGE.md) builds the dynamical step from the Hadamard read of the cube to the SST's scalar sector through a registered torsion response (30 independent checks).

### 04 · Distributed Field Processing: how the field closes

Every **Field Object** participates in its local **NET Field** as a correlated whole. Paper I calls the complete read a **Full-State Snapshot**. Settlement establishes compatibility; **Field State Registration** records the result at the closure interface. A larger field processes the registered contributions of its constituent objects rather than reconstructing their settled interiors.

![The snapshot-accounting chain](diagrams/gfd-snapshot-accounting.svg)

The process is continuous and local, not a universe-wide clock or a sequence of global calculations. Fields may overlap, while ownership of each material contribution remains single-valued.

![Recursive composition from local Field Objects to stellar and galactic systems](diagrams/gfd-recursive-field-closure.svg)

This is **compositional scale invariance** (scale universality in the proofs): the same settlement, registration and composition principle applies at each level, not geometric self-similarity. The [mountain-scale proof](proofs/sst-mountain-scale/) establishes exterior-preserving Newtonian registration by balayage and the nesting identity $B_kB_j=B_k$ under its assumptions. General nonlinear composition of drained fields and relativistic moving interfaces remain open.

[Architecture: Snapshot Accounting](FIELD_CLOSURE_AND_SNAPSHOT_ACCOUNTING.md) · [Mathematics: Recursive Registration](FIELD_CLOSURE_AND_RECURSIVE_REGISTRATION.md)

### 05 · The net-field rule: where Einstein's description applies

![The host NET Field and the local Newtonian interior](diagrams/gfd-local-versus-host.svg)

This is what separates GFD from an interpolation function. **The drain belongs to a field, not to a body.** Every Field Object closes; the drain determines the internal response, not whether closure occurs. A galaxy has an open drain, and its NET Field follows the constitutive law. A star system has none: like a bowling ball on a rubber sheet sitting in the galaxy's net field, it is pure TetA, exactly Newton and general relativity with the bare $G$, every body's own TetB enclosed in its $GM$. The galaxy acts inside it only through free fall and its tide (about $10^{-18}$ m/s² at Saturn). A galaxy also closes and registers with its parent system.

The [net-field rule](proofs/net-field-rule/) proves this (Theorem + Lean, 122 checks): applying any exchange-symmetric law with flat rotation curves to a star's own field is forced to fail, leaving a pull toward $a_0$ at every planet that Cassini excludes, and globular clusters require the bare $G$ at more than $8\sigma$. The [mountain-scale construction](proofs/sst-mountain-scale/) separates owned interior residuals from the host field. The [closure-surface proof](proofs/closure-surface/) identifies the stagnation/Jacobi surface in the stated Hill model; the physical selection of that surface for registration is still a premise.

---

## The framework in one page

| Object | Equation or result |
|---|---|
| Dimension selection under the vertex-count premise | $2(D+1)=2^D\Rightarrow D=3$, $K=4$ for positive integral $D$ |
| Geometric closure | $g=e^T\eta e$, $\sum_a v_a=0$ |
| Coupling polynomial | $f(K,s)=1+sK+K^2$ |
| Connection partition | $K^3=64=40+24$ |
| Constitutive law | $\mu(x)=x/(x+1)$ |
| Continuous capacity | $f(x)=(21x+13)/(x+1)$ |
| Kinetic functional | $F(y)=y-2\sqrt y+2\ln(1+\sqrt y)$; $F'(y)=\mu(\sqrt y)$ |
| Covariant time-leg variable | $y=c^4a_\mu a^\mu/a_0^2$, $a^\mu=u^\nu\nabla_\nu u^\mu$ |
| Quasi-static drained field | $\nabla\cdot[\mu(|\nabla\Phi|/a_0)\nabla\Phi]=4\pi G\rho$ |
| Spherical field equation | $g_s=g_t^2/(a_0+g_t)$ |
| Baryonic Tully–Fisher | $v^4\to GMa_0$ in the isolated deep-field limit |
| Spherical mass decoder | $M_{\rm dec}=rv^4/[G(a_0r+v^2)]$ |
| Drive, quiet, brake | $M_{\rm dec}/M_{\rm phot}=(g_t+w)/(g_t+a_0)$; $w$ compared with $a_0$ |
| Recursive registration | $B_kB_j=B_k$ for nested Newtonian balayage |
| Jacobi radius | $r_J^3=GM/(4\Omega^2-\kappa^2)$ in the Hill model |

The **SST** names the four-term covariant action, not its spherical field equation. In the framework's notation it is

$$S=\int d^4x\,\sqrt{-g}\left[\frac{R}{16\pi G}-\frac{a_0^2}{8\pi G}F(y)-\frac14e^{-2\Phi/c^2}\mathcal F_{\mu\nu}\mathcal F^{\mu\nu}+\mathcal L_{\rm matter}\right].$$

Here $\mathcal F_{\mu\nu}$ denotes the electromagnetic field tensor, distinct from the kinetic function $F(y)$. The [quasi-static](proofs/sst-quasi-static-limit/) and [covariant time-leg](proofs/sst-covariant-time-leg/) proofs specify the effective scalar correction $F-y$ when the Einstein curvature term supplies the Newtonian contribution. The [mountain-scale proof](proofs/sst-mountain-scale/) develops the ownership-based static extension. See the [full action and equation dictionary](GFD_COLES_NOTES.md#3-the-covariant-action-the-sst) for the action as stated in the papers and the premises required for its reduction.

## Formal research programme

![The proof programme: geometry and response join in the distributed closure chain](diagrams/gfd-readme-proof-roadmap.svg)

<a id="all-results-and-their-status"></a>

The [proof index](proofs/README.md) links each theorem to its LaTeX source, PDF, verification script and, where present, Lean audit. Formally established mathematical results are distinguished from physical identifications, derived consequences and observations.

### Reading path: from the tetrad to the collective flywheel

**[Start with Proof 25 — Convergence of the Tetrad and Collective Flywheel Geometries](proofs/tetrad-flywheel-convergence/)** for a guided synthesis of the geometric foundations, the explicit common Gram matrix, the isometries joining the routes, and their exact assumptions. The reading paths below converge in that proof; they do not represent independent physical measurements.

| Reading order | Geometry branch | Circulation branch |
|---|---|---|
| 1. Foundations | [Letter 1](papers/letter-1-tetrad-frame-geometry/) · [Forced frame](proofs/forced-tetrahedral-frame/) | [Vortex proof](proofs/vortices-of-the-stellated-octahedron/) |
| 2. Construction | [Half-spaces](proofs/half-space-two-bounded-regions/) · [Tetrad scheme](proofs/tetrad-scheme-two-bounded-regions/) | [Sustained eight-ring flywheel](research/hadamard-null-cone-vortex-flywheel/SUSTAINED_TRIFORCE_FLYWHEEL.md) |
| 3. Common metric | [Gram matrix](proofs/gram-matrix-tetrad-equation/) · [Hadamard frame](proofs/hadamard-cube-frame/) | [Proof 24: Intrinsic flywheel geometry](proofs/flywheel-tetrad-geometry/) |
| 4. Convergence | [Proof 25: exact transport and intrinsic solids](proofs/tetrad-flywheel-convergence/) | [Proof 25: core incidence and current reconstruction](proofs/tetrad-flywheel-convergence/#theorem-5--core-geometry-incidence-and-collective-current) |
| 5. Downstream geometry | [Proof 23: recursive Triforce closure](proofs/recursive-triforce-closure/) | Physical geometry selection, covariant dynamics and settlement remain open. |
| 6. Closure response | [Proof 26: the read, the 21 directions and G](proofs/recursive-field-closure-response/) | [Proof 26: fixed geometry, changing vortex](proofs/recursive-field-closure-response/) |

[Focused convergence diagram](diagrams/gfd-tetrad-flywheel-convergence.svg) · [Visual guide and proof PDF](proofs/tetrad-flywheel-convergence/tetrad_flywheel_convergence.pdf)

### New: Proof 26 — what does a closing field have to read?

**[Proof 26: Gravity as the Response of Recursive Field Closure](proofs/recursive-field-closure-response/)** starts from one plain question. A field object closes its own accounting, but its neighbours' fields reach into it. Can it close without looking at them?

It can't. If the right settlement depends on the environment, a "blind" closure is impossible, and the object has to read *something* about its neighbours (Theorem 1). The rest of the proof follows that read and finds that it is surprisingly specific:

- **The read is three sweeps.** On the 64 addresses of the recursive Triforce, a complete, reversible read is the Walsh–Hadamard transform, and it factors into exactly three commuting four-way stages, one per level of the Sierpiński subdivision. Its inverse is a Sierpiński down-sweep, a weight, and a Sierpiński up-sweep.
- **Symmetry leaves 21 directions.** The tetrad's order-three rotation turns the four labels into the field F₄. What survives it is exactly 21 independent contrasts, in grades of 1, 4 and 16, which are the 21 points of the projective plane over F₄. That is the same 21 as in G's exponent.
- **Finished blocks disappear from the read but keep their mass.** A completed block contributes nothing to the contrasts and everything to the common record, so a parent field can hold a closed child as one pointer.
- **The response has G's shape.** If the read registers all 21 directions together, as one volume, the collective response is (17/13)·|t|⁴², where 17/13 is the coupling polynomial's own ratio f(4,0)/f(4,−1). With one factor of α per direction, |t|² = α, this is the tree-level formula below.
- **The cube stays fixed; the vortex moves.** Settlement doesn't change the geometry. It changes the vortex state, and the proof computes that response exactly on the inherited flywheel branch.

![Proof 26: fixed geometry, changing vortex](proofs/recursive-field-closure-response/figures/proof26_architecture.svg)

What it leaves open is stated just as plainly: why the native action reads the whole frame as a determinant, what sets the per-direction gain, and the long-wave source action. Proof 26 has 532 exact checks (plus 568 in an optional projective appendix), and its finite theorems are machine-checked in Lean 4 (36 theorems, standard axioms only). Its G conclusion is conditional on those three premises, which are stated, not formalised. [Proof](proofs/recursive-field-closure-response/proof26.pdf) · [Referee-style audit](proofs/recursive-field-closure-response/REFEREE_REVIEW.md) · [Revision notes](proofs/recursive-field-closure-response/REVISION_4.md) · [Background research](research/g_from_topology/updated-research/)

| Research pillar | Representative proof packages | Status and scope |
|---|---|---|
| Tetrad geometry | [Forced frame](proofs/forced-tetrahedral-frame/), [Half-spaces](proofs/half-space-two-bounded-regions/), [Scheme](proofs/tetrad-scheme-two-bounded-regions/), [Hadamard frame](proofs/hadamard-cube-frame/) | [T+L] under stated spatial-realisation premises |
| Connection & orientation | [Gram matrix](proofs/gram-matrix-tetrad-equation/), [Torsion representation](proofs/torsion-regular-representation/), [Chiral holonomy](proofs/chiral-holonomy-closed-frame/) | [T] (Gram: + Lean) the 24 torsion components are the only place a metric connection can tell the roots apart: TetB's carrier (Letter 2) |
| Constitutive response | [Exchange](proofs/constitutive-law-exchange-symmetry/), [Tug of war](proofs/constitutive-law-tug-of-war/), [AQUAL energy](proofs/aqual-energy-functional/) | [T+L] within specified classes |
| Local state readout | [Walsh modes](proofs/walsh-eigenmodes-of-the-cube/), [Vortices](proofs/vortices-of-the-stellated-octahedron/), [Proof 24](proofs/flywheel-tetrad-geometry/), [Proof 25](proofs/tetrad-flywheel-convergence/) | [T] finite-dimensional symmetric models and exact finite geometry; physical realization open |
| Field equations | [Quasi-static SST](proofs/sst-quasi-static-limit/), [Time leg](proofs/sst-covariant-time-leg/), [Preferred frame](proofs/sst-khronon-preferred-frame/) | [T/D] specified effective action and approximations |
| Distributed closure | [Net field](proofs/net-field-rule/), [Mountain scale](proofs/sst-mountain-scale/), [Closure surface](proofs/closure-surface/), [Proof 26](proofs/recursive-field-closure-response/) | [T+L/D] static ownership, nesting and Hill-model results; Proof 26 [T/D]: necessity of the read, the 21-direction Walsh read and conditional G response; general dynamics open |
| Extensions & structural algebra | [Bimetric energy](proofs/bimetric-two-potential-energy/), [Bimetric lock](proofs/bimetric-lock-constitutive-law/), [BBP ladder](proofs/bbp-coupling-polynomial-ladder/), [Null rotation](proofs/g-null-rotation/) | [T] scoped algebra; broader physical interpretations vary in status |

**Status key:** [T] mathematical theorem · [L] Lean formalisation · [D] derived under stated physical premises · [O] observational comparison · [E] exploratory research. The complete result-by-result status inventory is preserved in the [research index](RESEARCH_INDEX.md#all-results-and-their-status) and [Coles Notes](GFD_COLES_NOTES.md).

## Observational programme

| Test | Result or research target |
|---|---|
| Galactic RAR [D/O] | 164 SPARC galaxies, 3,284 points, 0.181 dex scatter with nothing fitted per galaxy, matching the best empirical fit; flat in stacked residuals where MOND's standard function is not. |
| Mass decoding [D/O] | The zero-parameter inverse pipeline decodes mass from velocity alone, $M_{\rm dec}=rv^4/[G(a_0r+v^2)]$. The area between the decoded and photometric mass curves measures what the interior TetB is doing: decoded above photometric is drive, below is brake, equal is quiet ($w$ above, below or equal to $a_0$). CamB brakes by 0.77 dex at 1.79 kpc; NGC 3198 tracks its baryons. [Letter](papers/letter-decoding-mass-from-rotation-curves/) |
| Solar system [T+L/O] | Drainless, so pure TetA with the bare $G$; Cassini excludes applying $\mu$ to the Sun's own field, and the ownership model gives no anomalous $Q_2$ at the calculated order. [Net-field rule](proofs/net-field-rule/) · [Mountain scale](proofs/sst-mountain-scale/) |
| Globular clusters [T/O] | Require the bare $G$ at more than $8\sigma$, as the net-field rule predicts for drainless fields. [Analysis](proofs/net-field-rule/) |
| Wide binaries [T] | Bound wide binaries are Newtonian to within $(s/r_J)^3$, with a speed edge $v/\sqrt{GM/s}<\sqrt{2-3s/r_J}$ set before any velocity is inspected. [Net-field rule](proofs/net-field-rule/) · [Closure surface](proofs/closure-surface/) |
| Lensing [T/D] | $\gamma=1$: the curvature term gives $\Psi=\Phi$, so lensing mass equals dynamical mass. [Proof](proofs/sst-quasi-static-limit/) |
| Redshift evolution [D/O] | Tully–Fisher velocities rise as $[H(z)/H_0]^{0.17}$, compared with nine IFU measurements to $z=3$. [Manuscript](papers/tully-fisher-velocity-evolution/) |

## Beyond galactic dynamics

The same geometry carries beyond galaxies: into the fundamental constants, cosmology, nuclei and computation.

| Programme | Entry point |
|---|---|
| Fundamental constants and the electron scale | [Newton's constant from topology](research/g_from_topology/), [Paper III](papers/03-unit-of-gravity/), [Paper VI](papers/06-gravitational-constant-from-topology/) |
| Cosmology and the horizon relation | [Paper II](papers/02-covariant-theory-without-dark-matter/), [Paper X](papers/10-two-scale-kinematics-tully-fisher-h0/) |
| Bimetric correspondence | [Bimetric lock and its limitations](proofs/bimetric-lock-constitutive-law/), [Bimetric research](research/bimond-gfd/) |
| Nuclear and atomic structure | [Paper XI](papers/11-nuclear-shells-tetrahedral-packing/), [Paper XIII](papers/13-nuclear-binding-bidirectional-sst/), [Atomic properties](research/atomic-properties/) |
| Spectral computation and photonic analogues | [Spectral kernel](research/spectral/), [Quantum compute](<research/quantum compute/>), [Research index](RESEARCH_INDEX.md#computation-and-signal-processing) |

<a id="derived-constants"></a>

**Derived constants.** Newton's constant follows from the integers of the coupling polynomial:

$$G=\frac{17}{13}\,\alpha^{21}\,\frac{\hbar c}{m_e^2}\left(1+\frac{\alpha}{2\pi}\right),$$

within 12 ppm of the measured value, inside G's own uncertainty, and unique among 1,953 alternatives of its form ([look-elsewhere test](research/g_from_topology/)). The electron mass follows from closure saturation, $a_0=K^2Gm_e/r_e^2$, to 0.1%, and the classical electron radius is the unit of gravity ([Paper III](papers/03-unit-of-gravity/)). G and $m_e$ are graded derived; their premises are one factor of $\alpha$ per coupling level and the combination rule (21 as exponent, 17/13 as ratio), which is still marked proposed. The structural reading of $\alpha$ and the Hubble-scale relation are graded exploratory. [Proof 26](proofs/recursive-field-closure-response/) works on the other side of this formula: how read and settlement produce it, with the exponent 21 appearing as the read's invariant directions.

---

## Verification

The repository is designed for independent examination. No proprietary solver is required for the core Python checks. The proof folders contain reproducible scripts, exact algebra where applicable and explicit Lean audits where available.

```bash
python -m pip install numpy scipy sympy mpmath matplotlib

# Reproduce the SPARC figure from the bundled data table.
cd papers/letter-radial-acceleration-relation-sparc
python sparc_rar.py --from-csv supplementary/sparc_rar.csv
```

For formal verification, select a proof marked **+ Lean** in the [proof index](proofs/README.md), follow its `README.md` and inspect its `LEAN_AUDIT.md`. A successful Lean build verifies the encoded statements, not the empirical validity of their physical premises.

| Repository-reported coverage | Count |
|---|---:|
| Formal proof packages | 26 |
| Scripted checks in those packages | 2,062 |
| Lean 4 formalisations | 18 |

[All verification commands and validation suites](RESEARCH_INDEX.md#verification) · [Companion computational model](https://github.com/fielddynamics/dfp-gravity-field-model)

## Status and known limitations

Every result states its premises, and the open problems are documented as openly as the results. The current frontier:

- **Geometry to dynamics:** the [Read-Settle-Register bridge](research/read-settle-register-bridge/READ_SETTLE_REGISTER_BRIDGE.md) gives a conditional route from the Hadamard read to the action; deriving its local rate law from a conservative coupled-oscillator Hamiltonian is the next step.
- **Closure:** the Newtonian registration theorem holds under specified ownership and settlement assumptions. The drain criterion, physical selection of the stagnation interface, drained-galaxy registration, moving interfaces and causal relativistic composition require further work.
- **Galactic tests:** the RAR alone does not separate GFD from simple-function MOND; the separating tests are where $\mu$ acts (drainless systems) and the drive/brake map across morphologies. Photometric inputs carry their own uncertainties.
- **Beyond leading order:** the covariant action (the SST) is complete, with every prefactor fixed. Matter is ordinary and minimally coupled, and its source term $-\rho\Phi$ follows from that coupling ([quasi-static proof](proofs/sst-quasi-static-limit/)), which is what the galactic results use. What remains is solving the metric equations beyond the established weak-field and quasi-static orders (strong fields, cosmological perturbations) and testing the electromagnetic coupling against clock and spectroscopy constraints.
- **Bimetric bridge:** the locked derivative-free Hassan–Rosen potential does not supply the required acceleration dependence; the negative result is documented, not concealed.
- **Cosmology:** a full CMB power spectrum has not yet been computed, and the Hubble-scale relation's ±6% band does not yet discriminate between the Planck and SH0ES values.

[Complete original limitations and status ledger](RESEARCH_INDEX.md#status-and-known-limitations) · [Open problems in Coles Notes](GFD_COLES_NOTES.md#12-open-problems-and-issues)

## Relation to prior work

GFD builds on MOND (Milgrom 1983), AQUAL (Bekenstein & Milgrom 1984), the simple function studied by Famaey & Binney (2005), the SPARC/RAR studies of Lelli, McGaugh & Schombert (2016), tetrad and torsion geometry, and the preferred-foliation dynamics of Blanchet & Marsat. The bimetric programme engages Hassan & Rosen (2012). Its intended contribution is a geometric selection of the response and a distributed field-closure architecture, not the discovery of the simple interpolation function itself.

[Prior work and bibliography](RESEARCH_INDEX.md#relation-to-prior-work)

## Papers

<a id="published-papers-zenodo"></a>

| Series | Focus | Sources |
|---|---|---|
| Papers I–III | Original DFP architecture, constitutive law, covariant extension and gravity unit | [I](papers/01-gravitational-constitutive-law/) · [II](papers/02-covariant-theory-without-dark-matter/) · [III](papers/03-unit-of-gravity/) |
| Papers IV–XIII | Topology, constants, closure, bimetric gravity, cosmology and nuclear extensions | [Complete numbered series](RESEARCH_INDEX.md#papers) |
| Tetrad Letters 1–3 | Geometry, orientation, torsion and the 40/24 connection split | [L1](papers/letter-1-tetrad-frame-geometry/) · [L2](papers/letter-2-other-half-of-gravity-torsion/) · [L3](papers/letter-3-field-closure-of-tetrad-frame/) |
| Constitutive-law letter | Independent algebraic and geometric routes | [Source](papers/letter-constitutive-law-tetrad-geometry/) |
| Observational letters | SPARC and mass decoding | [RAR](papers/letter-radial-acceleration-relation-sparc/) · [DEC](papers/letter-decoding-mass-from-rotation-curves/) |
| Technical manuscripts | Gram matrix, algebraic papers A/B/C, AQUAL, null cone and Tully–Fisher | [Manuscript inventory](RESEARCH_INDEX.md#manuscripts-in-preparation-sources-only) |

The [complete publication catalogue](RESEARCH_INDEX.md#papers) retains all paper descriptions, revision links and DOI references from the previous README. The [original README at the source commit](https://github.com/fielddynamics/research/blob/d8c2a2ef0e70d8fe9523e51f16fc81bff91245f8/README.md) is also available as a permanent reference.

## Repository map

| Location | Purpose |
|---|---|
| [`papers/`](papers/) | Preprints, LaTeX sources, supplementary material and revisions |
| [`proofs/`](proofs/README.md) | Curated mathematical proof packages and Lean audits |
| [`docs/`](docs/README.md) | Guided framework documentation |
| [`research/`](research/) | Research trail, numerical investigations, exploratory work and superseded approaches |
| [`diagrams/`](diagrams/) | Visual explanations of the framework and closure architecture |
| [`GFD_COLES_NOTES.md`](GFD_COLES_NOTES.md) | Condensed technical reference organized by topic and paper |
| [`llms.txt`](llms.txt) | Machine-readable ontology, terminology and dependency chain |
| [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md) | Detailed catalogue and original README, preserved in full |

## About the author

Stephen Nelson is an engineer whose work in enterprise and government systems, including encryption, motivated the original Distributed Field Processing question: how can a field close locally without leaving its configuration unaccounted for? Read [ABOUT.md](ABOUT.md) for the background to the research.

## Citing

Use the relevant Zenodo preprint for a specific result, or the repository's [CITATION.cff](CITATION.cff) for the framework as a whole. The [publication catalogue](RESEARCH_INDEX.md#papers) preserves the available DOI records.

## Licence

[MIT License](LICENSE) © 2026 Stephen Nelson, Field Dynamics Research. Zenodo papers also carry the licence recorded on their respective records.

## Contact

[Field Dynamics Research](https://fielddynamics.org) · [Documentation](docs/README.md) · stephen@fielddynamics.org · [Open an issue](https://github.com/fielddynamics/research/issues)

**Geometry establishes what closes. Snapshot accounting describes how it closes. Recursive registration describes how closure scales.**
