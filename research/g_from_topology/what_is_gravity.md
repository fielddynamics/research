# What Is Gravity?

### An open question, set out from the archive's own results

*Field Dynamics Research · a synthesis of [`g_from_topology/`](./), [`universe-is-pixelated/`](../universe-is-pixelated/), [`photonic/`](../photonic/), [`field-closure/`](../field-closure/) and the tetrad letters*

---

## The question

The work in this archive answers three questions about gravity with unusual precision:

- **How strong it is.** $G = \tfrac{17}{13}\,\alpha^{21}\,\hbar c/m_e^2$, within 0.12% of the measured value at tree level and 12 parts per million with the one-loop factor $1 + \alpha/2\pi$.
- **What shape it has.** The connection has 64 components. General relativity keeps 40 and removes 24, and the constitutive law $\mu(x) = x/(1+x)$ shares the field between the two tetrahedral chambers at every radius.
- **How it travels.** At $c$, the same speed as light, as GW170817 confirmed.

A fourth question, **what gravity is**, has one answer running through the archive, first stated in the Distributed Field Processing papers I–III: **field closure requires a read.** A distributed field cannot settle unless each part reads what its neighbours are doing. Later work describes the parts of that one mechanism: what is read (the lattice), what does the reading (the sweep), what the read produces (settlement and registration), how general relativity sees the result (the connection) and the algebra the read runs on (the cube's Walsh–Hadamard spectrum).

This note follows the mechanism step by step and shows where each part of the archive enters. It proceeds in four stages: what any answer must account for; the mechanism, from closure to the field equation; what the archive itself still names as open; and what would decide it. It is written as an open question because, although each step is derived in the archive, the steps have not yet been joined into a single derivation of what gravity is.

**Conventions.** $K = 4$ is the number of tetrad legs and $D = 3$ the number of spatial dimensions; Paper VII writes them $k$ and $d$. The coupling polynomial is $f(K, s) = 1 + sK + K^2$, with values $f(+1) = 21$, $f(0) = 17$ and $f(-1) = 13$. TetA and TetB are the two tetrahedral chambers of the frame, and $\mu$ is the share of the field resolved through TetA. Quoted passages come from the files named at the head of each step; section and equation numbers refer to Paper VII unless stated otherwise.

---

## What any answer must account for

These results are established within the framework, by derivation, by computation or against measurement. Any account of what gravity is has to produce all of them.

| Result | Status | Where |
|---|---|---|
| $G = \tfrac{17}{13}\,\alpha^{21}\,\hbar c/m_e^2$; 0.12% at tree level, 12 ppm with $1 + \alpha/2\pi$ | Matches measurement; G itself is known to 22 ppm (CODATA 2022) | [`g_matrix_synthesis.md`](g_matrix_synthesis.md), [`synthesis_one_loop_G.md`](synthesis_one_loop_G.md) |
| Among 1,953 alternatives $(p/q)\,\alpha^n$ with $p, q \le 21$ and $n = 18$–24, only $17/13 \cdot \alpha^{21}$ lands within 0.12%, and only it lands within 22 ppm with the loop factor | Computed | [`look_elsewhere_G.py`](look_elsewhere_G.py) |
| The three values 21, 17, 13 are the traces of one graded operator, $\mathrm{Tr}(P_0 + sP_1 + P_2) = 1 + sK + K^2$, on blocks of size 1, 4 and 16 | Exact | [`g_matrix_synthesis.md`](g_matrix_synthesis.md) |
| The connection's 64 components split 40 + 24; the 24 carry the second root of the tetrad equation | Exact count; the identification is Letter 3's claim | [Letter 3 guide](../../FIELD_CLOSURE_OF_THE_TETRAD_FRAME.md) |
| $\mu(x) = x/(1+x)$ reproduces the radial acceleration relation with no free parameter | Matches 3,284 points in 164 SPARC galaxies with the same scatter as the empirical fit, 0.18 dex | Letter 3; the [SPARC letter](../../papers/letter-radial-acceleration-relation-sparc/) (Lelli et al. 2016; McGaugh et al. 2016) |
| The field equations run both ways: an observed rotation curve decodes to an effective mass, $M_{\text{dec}} = r v^4 / [G(a_0 r + v^2)]$, with no mass model and no halo. For the Milky Way and M33 the decoded mass lands near the baryonic mass, where $\Lambda$CDM needs three to five times more | Demonstrated on the Milky Way, M33 and NGC 3198 | [Decoding-mass letter](../../papers/letter-decoding-mass-from-rotation-curves/) |
| Gravity couples to everything equally, is only ever attractive, and travels at $c$ | Observed | Equivalence principle; GW170817 (Abbott et al. 2017) |
| The cube's eight corners carry every three-input Boolean operation; its spectrum factors as $H_8 = H_2 \otimes H_4$ | Established mathematics | [`universe-is-pixelated/`](../universe-is-pixelated/) |

---

## The mechanism, step by step

### 1. Closure requires a read

*[Paper I](../../papers/01-gravitational-constitutive-law/), [Paper II](../../papers/02-covariant-theory-without-dark-matter/), [Paper III](../../papers/03-unit-of-gravity/)*

Paper I starts from a requirement rather than a picture. A field that carries waves must have parts, and parts that couple at an interface must agree. "At each coupling interface, gradient information must be exchanged: the field on one side must 'read' what the field on the other side is doing. The coupling must then settle into a single consistent state across all interfaces simultaneously. This settlement process is what we call field closure." Settlement is atomic: either every coupling channel agrees, or the configuration is not settled.

Paper I writes the chain in one line: the field closure function at the closure boundary $\Sigma$ runs READ → SETTLE, and its output is the registered state $B^*_\Sigma$. Each term maps onto established physics. The complete field snapshot is the initial-data surface, settlement is relaxation to equilibrium, and the registered state is the field after settlement. Requiring settlement to be lossless and local gives the constitutive law $\mu(x) = x/(1+x)$ within the minimal single-channel saturating closure class.

Papers II and III give the read its extent and its size. Field closures are not isolated: their boundaries tile spacetime, and how they tile sets the acceleration scale, $a_0 = cH/2\pi$ (Paper II). The unit of that tiling, the tile, is set at the electron scale, the classical electron radius $r_e$ (Paper III).

Everything below elaborates this chain: what is read, what does the reading, what the reading produces, and how it is seen.

### 2. What is read: the lattice

*[`photonic/the-pixel-and-the-lattice.md`](../photonic/the-pixel-and-the-lattice.md), [`photonic/gfd_light_substrate_synthesis.md`](../photonic/gfd_light_substrate_synthesis.md), Paper VII §XI.A*

Each photon is a stellated octahedron, the pixel. Packed on their four faces, photons form the lattice, and the lattice is the gravitational field: "Gravity is the lattice itself." There is no flat space beneath it. Mass is a vortex in the lattice, a closure driven through the Field Origin into TetB and held there, and a gravity field is "a pocket of subspace that has closed" around it. Near matter, the strata along which light travels curve, which is lensing.

Paper VII names the two kinds of tile the read meets. The mesh of *unbound* envelopes, TetB chambers empty, is the long-range background, "the stage". *Bound* envelopes, TetB chambers occupied, are matter, "the actors". Because everything is made of the same packing, nothing can decouple from it, which is the equivalence principle.

### 3. What does the reading: the sweep

*[`read_sweep_synthesis.md`](read_sweep_synthesis.md), [`g_matrix_synthesis.md`](g_matrix_synthesis.md)*

The read-sweep note opens with exactly this question: "if G is a matrix read, what is doing the reading?" The substrate is stationary; what moves is a pattern of activation, as in a stadium wave. The read is a rotation through 64 sectors, and one rotation is one Compton period: one field closure. Paper VII states the same rate in its own terms, $f_{\text{closure}}/f_{\text{Compton}} = 2\pi/\alpha$ (§VI.A).

The 64 sectors carry three harmonic bands, of 1, $K = 4$ and $K^2 = 16$ cycles per rotation: the existence of the structure, its four directional channels and their sixteen couplings. That is $1 + K + K^2 = 21$ harmonics per rotation. Each level costs one factor of $\alpha$, and the factors multiply: the determinant identity $\det(\alpha^{I}) = \alpha^{\mathrm{Tr}\,I}$ applies one factor per eigenvalue of the graded operator, so the full read is attenuated by $\alpha^{21}$. With the tile set at $r_e$, $\alpha = r_e/\bar\lambda_C$ is the fraction of each quantum wavelength that the coupling structure occupies (Paper VII, §VI.A).

The same graded operator, read with $s = 0$ and $s = -1$, gives the prefactor. $17/13$ is derived twice, as coupling channels over structural elements (Paper VI, §8.3; [`FORMAL BRIDGING OF 17-13.md`](../../papers/06-gravitational-constant-from-topology/FORMAL%20BRIDGING%20OF%2017-13.md)) and as coupling capacity over spatial structure (Paper VII, Eq. 24). The numerator, $K^2 + 1 = 17$, is the Field Origin, where the face channels are absent: the 16 bimetric coupling channels plus the non-degenerate vertex itself. It is also the parity-even core that the metric couples through, since the sign representation carrying the parity-odd $K$ is absent from the Christoffel sector (Letter 2; the [algebraic pipeline](../../papers/algebraic-papers-a-b-c/algebraic_pipeline_of_reality.md)). The denominator, $DK + 1 = 13$, is TetB, the $K = 4$ face channels projected onto $D = 3$ spatial dimensions plus one for non-degeneracy. The three values are locked together, $f(0) = \tfrac12[f(+1) + f(-1)]$ (Eq. 23), and among 1,953 simple alternatives no other prefactor and exponent come close.

Electromagnetism and gravity are read to different depths, and Paper VII (§V.B) gives the reason. In ghost-free bimetric gravity, matter, including the electromagnetic field, couples to a single metric sector, so electromagnetism reaches only the first level and carries one factor of $\alpha$. Gravity is the interaction *between* the two sectors, through the Hassan–Rosen potential $V(\sqrt{g^{-1}f})$ (Hassan and Rosen 2012), so it must traverse all 21 levels. The ratio is $\alpha^{20} \approx 10^{-43}$.

### 4. What the read produces: settlement, registration and free fall

*[Paper VII](../../papers/07-dual-tetrad-topology-field-origin/v7/Dual_Tetrad_Gravity_And_The_Field_Origin.pdf) §II.B, §VII.A, §XI; [`field-closure/`](../field-closure/)*

Paper VII carries Paper I's chain through in full. "Through each face of the local tetrahedron, the field reads and reconciles the geometric state of neighboring regions" (§II.B). Its closure mechanism (§XI) has three steps: a *Full State Snapshot* reads the whole configuration at once, *Settlement* resolves it to the single state that satisfies every constraint in both metric sectors, and *Registration* records that state. The snapshot is the complete Cauchy data a well-posed initial-value problem needs, and settlement is the solution of the Hamiltonian and momentum constraints (the York–Lichnerowicz method).

Gravity is what the registered state looks like from one place to the next: "The gradients of the registered state $\nabla\ell(x)$ produce three manifestations of the same underlying process: gravitational acceleration, … gravitational lensing, … and time dilation." A body's trajectory is the sequence of its registered states. A body near a mass settles into the state of its neighbours, which differ slightly from one side to the other, and moving along that difference *is* the settling. General relativity treats free fall the same way, as motion with no force acting. In three dimensions the reconciliation around a mass spreads over a sphere, so it thins as $1/r^2$; the read-sweep note gives the same result as one sweep covering $4\pi = K\pi$ steradians.

Settlement also fixes how the field is shared. The coupling capacity at each point is either resolved or unresolved; resolution is driven by the field's intensity, $W_+ = \kappa\,x\,(1 - \varepsilon)$, and relaxation runs at $W_- = \kappa\,\varepsilon$. Detailed balance gives the resolved fraction $\varepsilon = x/(1+x) = \mu$, with the "1" as the processing capacity of the single Field Origin (§VII.A). That is the third independent route to the law, after lossless local closure (Paper I) and exchange symmetry (Letter 2).

### 5. How general relativity sees the read: the connection

*[Letter 3](../../papers/letter-3-field-closure-of-tetrad-frame/), [Einstein's equation as the TetA partition](../../EINSTEIN_TETA_PARTITION.md)*

In general relativity the gravitational field is the connection, the rule that relates one local frame to the next, which is the comparison between neighbouring registered states written in the language of geometry. It has 64 components, the $8 \times 8$ ordered transitions between the corners of neighbouring cubes. The torsion-free condition keeps the 40 that the metric can see and removes the 24 that carry the second root of the tetrad equation. That is why general relativity is exact where TetA carries the field, as in the solar system, and incomplete at galactic radii, where $\mu$ falls and TetB carries most of it. Restoring the 24 closes the field.

### 6. The algebra the read runs on: the cube

*[`universe-is-pixelated/`](../universe-is-pixelated/), [Paper C](../../papers/algebraic-papers-a-b-c/)*

The read is a transform with ±1 entries. The cube's eight corners form a universal Boolean operator, read by its Walsh–Hadamard spectrum, and the blocks of size 1, 4 and 16 in G's graded operator are the Hadamard matrices $H_1$, $H_4$ and $H_{16}$. The octahedral resonance node shows a coupled oscillator on those corners producing the whole spectrum in one oscillation.

The cube's spectrum factors as $H_8 = H_2 \otimes H_4$ (Paper C). $H_4$ is the frame within one tetrahedron; $H_2$ says which tetrahedron, and that is the cube's parity. General relativity keeps only the parity-even part, so it reads a single chamber. The full read needs $H_2$: both chambers, and with them $1 - \mu$. This is the bimetric fact of step 3 seen from the algebra. At $D = 3$ the counts coincide, $2 \times 4 = 8$ corners and $K^3 = 64 = 8 \times 8$, which is why the cube and the stellated octahedron can be read as one object.

### 7. Reading the read back from observation

*[Decoding-mass letter](../../papers/letter-decoding-mass-from-rotation-curves/)*

A star's orbit follows the total acceleration $g_t$, the field carried by both chambers, while the visible matter supplies only the TetA share, $g_s = \mu\,g_t$. The decoding-mass letter runs that relation backwards: from the measured rotation speeds alone, with no mass model, it returns the mass the field implies, $M_{\text{dec}}(r) = r\,v^4 / [G\,(a_0 r + v^2)]$. For the Milky Way at 25 kpc the decoded mass is about $6.6 \times 10^{10}\,M_\odot$, against $7.3 \times 10^{10}\,M_\odot$ in stars and gas, where $\Lambda$CDM needs about $2.3 \times 10^{11}\,M_\odot$.

**TetB can drive the rotation or brake it.** This is why predicting a rotation curve from the visible mass alone is not, by itself, a test of the framework. Such a prediction assumes a quiet interior, in which TetB neither adds to the field nor takes from it. A galaxy's second chamber behaves more like the drain of a water vortex. The drain can drive the flow, so the water circulates faster than the floating tracers alone would suggest, or it can hold the flow back. The tracers follow the rotation either way, so their speed alone does not say which.

The decode measures it. Comparing the decoded mass with the photometric mass at each radius, the ratio $R(r) = M_{\text{dec}}(r) / M_{\text{phot}}(r)$ reads the interior with no free parameter:

| $R(r)$ | The field compared with the visible matter | TetB's role |
|---|---|---|
| $> 1$ | Stronger than the baryons supply | Driving the rotation |
| $\approx 1$ | What the baryons supply | Quiet |
| $< 1$ | Weaker than the baryons supply | Braking the rotation |

The letter's mass difference, $\Delta M(r) = M_{\text{phot}}(r) - M_{\text{dec}}(r)$, is the same measurement written as a difference. The galaxies already decoded span the range. In M33 the decoded mass at 17 kpc, $1.38 \times 10^{10}\,M_\odot$, is roughly twice the visible mass: the outer disk is driven. In the Milky Way, $R \approx 0.9$ at 25 kpc: close to quiet. The lower outer speeds reported from Gaia DR3 (Jiao et al. 2023), about 181 km/s at 25.5 kpc, decode to about $5 \times 10^{10}\,M_\odot$, $R \approx 0.7$: the outer Milky Way braked, but still close to its baryons and nowhere near a halo. In the low-surface-brightness galaxy CamB the decoded mass falls below the visible mass across the observed range: braked. Because photometric masses themselves carry uncertainties of up to a factor of two, through the mass-to-light ratio, only departures larger than that are clear signals.

---

## The field equation, read term by term

Paper VII (§IX) writes the Poisson equation with every factor named:

$$\nabla^2\Phi = K\pi \cdot \frac{K^2 + 1}{DK + 1} \cdot G_{\text{bare}} \cdot \rho, \qquad G_{\text{bare}} = \alpha^{21}\,\frac{\hbar c}{m_e^2},$$

and the constitutive law weights the gradient in the full equation, $\nabla \cdot \big[\mu(|\nabla\Phi|/a_0)\,\nabla\Phi\big] = 4\pi G \rho$. Each term is one step of the mechanism:

| Term | Step | Reading |
|---|---|---|
| $\nabla\Phi$ | 4, 5 | The difference between neighbouring registered states |
| $K\pi = 4\pi$ | 3 | One full sweep: the solid angle, divided into four equal parts of $\pi$ steradians by the faces of a regular tetrahedron |
| $17/13$ | 3 | Coupling capacity at the Field Origin over the spatial structure of TetB |
| $G_{\text{bare}}$ | 1, 3 | The $\alpha^{21}$-deep read, set in units by the electron-scale tile |
| $\mu$ | 4, 6 | The share of each comparison resolved through TetA; below $a_0$, TetB carries most of it |
| $\rho$ | 2 | The density of bound envelopes |

The two kinds of term do different jobs. $G$ is built from all three structural states of the polynomial at once, 21 in the exponent and 17/13 in the prefactor, so it is a constant; in the covariant action it sits in the curvature term, $R/16\pi G$. The constitutive law $\mu(x)$ sits in the scalar sector, through $F(y)$, and describes how the response is shared between the two chambers at each acceleration.

In one sentence: **gravity is the gradient of what field closure registers, where closure requires a read, the read is a sweep through the stellated octahedron to depth $\alpha^{21}$, and the cube's parity brings in the second chamber.**

---

## What remains open

Two kinds of open point remain. The first is the one stated in the introduction: the mechanism above has not yet been written as a single derivation. The others are those the archive itself names.

### 1. The one physical input

Everything in G except one step is geometry and algebra. That step, as [`g_matrix_synthesis.md`](g_matrix_synthesis.md) states it, is that each coupling level attenuates by $\alpha$: the frame is built from null directions, and null means photonic. Step 3 gives the factor its physical meaning, $\alpha = r_e/\bar\lambda_C$, with the tile size of Paper III, and the G derivation lists it as its one physical assumption. The value of G supports the step strongly: changing the exponent by one changes G by a factor of 137, and the look-elsewhere test finds no rival.

### 2. The one-loop correction

The tree-level residual, 0.117%, is the Schwinger term $\alpha/2\pi = 0.116\%$, the same correction that shifts the electron's magnetic moment (Schwinger 1948); including it brings G to 12 ppm and moves the predicted Hubble constant from 70.21 to 70.29 km/s/Mpc (Paper VII, §X.B). [`synthesis_one_loop_G.md`](synthesis_one_loop_G.md) reads the factor structurally as $\tfrac{2}{17} \times \tfrac{17\alpha}{4\pi}$, the Field Origin impedance carried through one loop, and marks that reading as the subject of its own paper.

### 3. Lorentz invariance of the discrete picture

Any discrete picture of spacetime must respect Lorentz invariance, which Fermi observations of GRB 090510 constrain beyond 7.6 Planck energies (Vasileiou et al. 2013), and which GW170817 confirms for gravity to about one part in $10^{15}$ (Abbott et al. 2017). The pixelated README sets out why GFD's grid has no spacing to feel: propagation is closure, not motion across a mesh, and each cube is the local frame of its own event. It names the formal proof, that the Walsh structure of the frame keeps $\omega = ck$ exact, as the next step.

### 4. Beyond the electron

Paper VII closes by naming what its results do not yet address: how the non-linear coupling at the Field Origin produces the full spectrum of bound configurations beyond the electron, and how the field dynamics of the $K = 4$ topology connect to the gauge dynamics of the Standard Model, the strong and weak forces and the particle mass hierarchy.

The graviton belongs here too. Paper VII identifies the massless spin-2 mode of bimetric gravity with the unbound mesh and the massive mode, confined by its own coupling, with bound envelopes, Wheeler's geons (Wheeler 1955) realised as matter; the light-substrate notes describe the graviton as two stellated octahedra coupled at a face, and the quantum-gravity folder makes contact with Regge calculus and loop quantum gravity. How the quantised theory follows is open.

---

## What would decide it

Paper VII lists the framework's distinctive predictions, each of which can fail:

- **The massive graviton.** $\beta_n = (1, 0, 16, 0, 1)$ fixes the bimetric mass spectrum, which gravitational-wave dispersion measurements from LIGO, Virgo and KAGRA constrain directly.
- **An acceleration scale that changes with time.** $a_0$ is tied to the Hubble rate, so it was larger in the past. Rotation curves at redshift $z > 1$, from JWST and Euclid, test this; standard MOND assumes a constant $a_0$ (Milgrom 1983).
- **The value of $H$.** With $G$ and $m_e$ fixed, $H = 70.21$ km/s/Mpc at tree level and 70.29 at one loop, between the Planck and SH0ES values.

Two further measurements follow from this note:

- **A drive–brake map.** Running all 175 SPARC galaxies through the inverse pipeline would give $R(r) = M_{\text{dec}}/M_{\text{phot}}$ at every measured radius. Whether TetB drives or brakes, and how that depends on surface brightness, morphology and environment, is the measurement that would tell what the second chamber is doing, and it needs no free parameter.
- **The wide-binary tests**, beyond a few thousand AU from a star, where the external field of the Milky Way and the transition at $a_0$ both matter. The published analyses currently disagree (Chae 2023; Banik et al. 2024).

---

## Running the evidence

```bash
python look_elsewhere_G.py                                     # 17/13 alpha^21 against 1,953 alternatives
python ../universe-is-pixelated/verify_pixelated.py            # the cube, its spectrum and the value of G
python ../../papers/letter-3-field-closure-of-tetrad-frame/Supplementary/run_all_validations.py   # 40/24 and mu
```

---

## References

### Archive sources

- Nelson, S. (2026). *The Gravitational Constitutive Law (No Dark Matter Required)* (Paper I). [`papers/01-gravitational-constitutive-law/`](../../papers/01-gravitational-constitutive-law/).
- Nelson, S. (2026). *A Covariant Theory Without Dark Matter* (Paper II). [`papers/02-covariant-theory-without-dark-matter/`](../../papers/02-covariant-theory-without-dark-matter/).
- Nelson, S. (2026). *The Unit of Gravity: Deriving the Tile Size at Electron Scale* (Paper III). [`papers/03-unit-of-gravity/`](../../papers/03-unit-of-gravity/).
- Nelson, S. (2026). *Deriving the Gravitational Constant from Spacetime Topology* (Paper VI). [`papers/06-gravitational-constant-from-topology/`](../../papers/06-gravitational-constant-from-topology/); doi:10.5281/zenodo.18463038.
- Nelson, S. (2026). *Dual Tetrad Topology and the Field Origin: From Nuclear Decay to Galactic Dynamics* (Paper VII). [`papers/07-dual-tetrad-topology-field-origin/`](../../papers/07-dual-tetrad-topology-field-origin/).
- Nelson, S. (2026). *The Other Half of Gravity: Torsion and the Two-Chamber Structure of the Tetrad Frame* (Letter 2). [`papers/letter-2-other-half-of-gravity-torsion/`](../../papers/letter-2-other-half-of-gravity-torsion/).
- Nelson, S. (2026). *Gravity Field Dynamics: Field Closure of the Tetrad Frame* (Letter 3). [`papers/letter-3-field-closure-of-tetrad-frame/`](../../papers/letter-3-field-closure-of-tetrad-frame/).
- Nelson, S. (2026). *Decoding Mass from Observed Rotation Curves*. [`papers/letter-decoding-mass-from-rotation-curves/`](../../papers/letter-decoding-mass-from-rotation-curves/); doi:10.5281/zenodo.18721752.
- Nelson, S. (2026). *The Radial Acceleration Relation from a Zero-Parameter Covariant Action*. [`papers/letter-radial-acceleration-relation-sparc/`](../../papers/letter-radial-acceleration-relation-sparc/).
- Nelson, S. (2026). Papers A, B and C. [`papers/algebraic-papers-a-b-c/`](../../papers/algebraic-papers-a-b-c/).

### External

- Abbott, B. P. et al. (2017). Gravitational waves and gamma-rays from a binary neutron star merger: GW170817 and GRB 170817A. *Astrophys. J. Lett.* 848, L13.
- Banik, I. et al. (2024). Strong constraints on the gravitational law from Gaia DR3 wide binaries. *Mon. Not. R. Astron. Soc.* 527, 4573.
- Chae, K.-H. (2023). Breakdown of the Newton–Einstein standard gravity at low acceleration in internal dynamics of wide binary stars. *Astrophys. J.* 952, 128.
- Hassan, S. F. and Rosen, R. A. (2012). Bimetric gravity from ghost-free massive gravity. *J. High Energy Phys.* 2012(2), 126.
- Jiao, Y., Hammer, F., Flores, H., Wang, J. L. and Yang, Y. (2023). Detection of the Keplerian decline in the Milky Way rotation curve. *Astron. Astrophys.* 678, A208.
- Lelli, F., McGaugh, S. S. and Schombert, J. M. (2016). SPARC: mass models for 175 disk galaxies with Spitzer photometry at 3.6 μm and accurate rotation curves. *Astron. J.* 152, 157.
- McGaugh, S. S., Lelli, F. and Schombert, J. M. (2016). Radial acceleration relation in rotationally supported galaxies. *Phys. Rev. Lett.* 117, 201101.
- Milgrom, M. (1983). A modification of the Newtonian dynamics as a possible alternative to the hidden mass hypothesis. *Astrophys. J.* 270, 365.
- Mohr, P. J., Newell, D. B., Taylor, B. N. and Tiesinga, E. (2025). CODATA recommended values of the fundamental physical constants: 2022. *Rev. Mod. Phys.* 97, 025002.
- Schwinger, J. (1948). On quantum-electrodynamics and the magnetic moment of the electron. *Phys. Rev.* 73, 416.
- Vasileiou, V. et al. (2013). Constraints on Lorentz invariance violation from Fermi-Large Area Telescope observations of gamma-ray bursts. *Phys. Rev. D* 87, 122001.
- Wheeler, J. A. (1955). Geons. *Phys. Rev.* 97, 511.
