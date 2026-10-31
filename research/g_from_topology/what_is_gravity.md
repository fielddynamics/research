# What Is Gravity?

### An open question, set out from the archive's own results

*Field Dynamics Research · a synthesis of the Distributed Field Processing papers I–III and VII, the tetrad letters, [`g_from_topology/`](./), [`photonic/`](../photonic/), [`field-closure/`](../field-closure/) and [`universe-is-pixelated/`](../universe-is-pixelated/)*

---

## In brief

A gravitational field is distributed: it has parts, and where parts meet they must agree. Agreement needs information, so each part has to *read* its neighbours before the field can settle into one consistent state. This is field closure, and it is where the Distributed Field Processing papers begin.

Gravity, on this account, is the gradient of what closure registers from one place to the next. Its strength is set by how deep the read must go, 21 levels at one factor of $\alpha$ each, which gives Newton's constant. Its shape is set by the two tetrahedral chambers the read must cover, which gives the constitutive law $\mu$ and the part of the field general relativity leaves out.

Every step of that account is derived somewhere in the archive. They have not yet been joined into one derivation, and that is why this note is written as an open question.

---

## The question

The work in this archive answers three questions about gravity with unusual precision:

- **How strong it is.** $G = \dfrac{K^2+1}{DK+1}\,\alpha^{1+K+K^2}\,\dfrac{\hbar c}{m_e^2} = \tfrac{17}{13}\,\alpha^{21}\,\hbar c/m_e^2$ with $K = 3+1$ and $D = 3$, within 0.12% of the measured value at tree level and 12 parts per million with the one-loop factor $1 + \alpha/2\pi$.
- **What shape it has.** The connection has 64 components. General relativity keeps 40 and removes 24, and the constitutive law $\mu(x) = x/(1+x)$ shares the field between the two tetrahedral chambers at every radius.
- **How it travels.** At $c$, the same speed as light, as GW170817 confirmed.

The fourth question, **what gravity is**, is the subject of this note. It follows one mechanism, field closure, in seven steps: why closure requires a read; what is read; what does the reading; what the read produces; how general relativity sees the result; the algebra the read runs on; and how the read can be measured back from observation. It then reads the field equation term by term against those steps, and ends with what the archive still names as open and what would decide it.

### Terms used

| Term | Meaning |
|---|---|
| $K = 3+1$, $D = 3$ | The number of tetrad legs, one per spacetime dimension, and the number of spatial dimensions. Paper VII writes them $k$ and $d$. |
| $f(K, s) = 1 + sK + K^2$ | The coupling polynomial: $f(+1) = 21$, $f(0) = 17$, $f(-1) = 13$ |
| TetA, TetB | The two tetrahedral chambers of the frame. General relativity describes TetA. |
| $\mu(x)$ | The share of the field resolved through TetA, at $x = g/a_0$ |
| Field Origin | The vertex where the two chambers couple, the $s = 0$ state of the polynomial |
| Field object | A body as gravity meets it: all its coupled fields, as one configuration |
| NET Field | Everything else, already merged into one local state at the body's position |
| Closure boundary $\Sigma$ | Where a field object and the NET Field meet and are reconciled |
| Registered state | The single consistent state that closure settles to; $\ell(x)$ is its local scale |

Quoted passages come from the sources named under each step. Section and equation numbers refer to Paper VII unless stated otherwise.

---

## What any answer must account for

These results are established within the framework, by derivation, by computation or against measurement. Any account of what gravity is has to produce all of them.

| Result | Status | Where |
|---|---|---|
| $G = \tfrac{17}{13}\,\alpha^{21}\,\hbar c/m_e^2$; 0.12% at tree level, 12 ppm with $1 + \alpha/2\pi$ | Matches measurement; G itself is known to 22 ppm (CODATA 2022) | [`g_matrix_synthesis.md`](g_matrix_synthesis.md), [`synthesis_one_loop_G.md`](synthesis_one_loop_G.md) |
| Among 1,953 alternatives $(p/q)\,\alpha^n$ with $p, q \le 21$ and $n = 18$–24, only $17/13 \cdot \alpha^{21}$ lands within 0.12%, and only it lands within 22 ppm with the loop factor | Computed | [`look_elsewhere_G.py`](look_elsewhere_G.py) |
| 21, 17 and 13 are the traces of one graded operator, $\mathrm{Tr}(P_0 + sP_1 + P_2) = 1 + sK + K^2$, on blocks of size 1, 4 and 16 | Exact | [`g_matrix_synthesis.md`](g_matrix_synthesis.md) |
| The connection's 64 components split 40 + 24; the 24 carry the second root of the tetrad equation | Exact count; the identification is Letter 3's claim | [Letter 3 guide](../../FIELD_CLOSURE_OF_THE_TETRAD_FRAME.md) |
| $\mu(x) = x/(1+x)$ reproduces the radial acceleration relation with no free parameter | Matches 3,284 points in 164 SPARC galaxies, with the same 0.18 dex scatter as the empirical fit | Letter 3; the [SPARC letter](../../papers/letter-radial-acceleration-relation-sparc/) (Lelli et al. 2016; McGaugh et al. 2016) |
| An observed rotation curve decodes to an effective mass, $M_{\text{dec}} = r v^4 / [G(a_0 r + v^2)]$, with no mass model and no halo; for the Milky Way and M33 it lands near the baryonic mass, where $\Lambda$CDM needs three to five times more | Demonstrated on the Milky Way, M33 and NGC 3198 | [Decoding-mass letter](../../papers/letter-decoding-mass-from-rotation-curves/) |
| Gravity couples to everything equally, only attracts, and travels at $c$ | Observed | Equivalence principle; GW170817 (Abbott et al. 2017) |
| The cube's eight corners carry every three-input Boolean operation; its spectrum factors as $H_8 = H_2 \otimes H_4$ | Established mathematics | [`universe-is-pixelated/`](../universe-is-pixelated/) |

---

## The mechanism, step by step

### 1. Closure requires a read

*[Paper I](../../papers/01-gravitational-constitutive-law/), [Paper II](../../papers/02-covariant-theory-without-dark-matter/), [Paper III](../../papers/03-unit-of-gravity/)*

**In short:** a field with parts must reconcile them, and reconciling them requires each part to read its neighbours.

Paper I starts from a requirement, not a picture. A field that carries waves must have parts, and parts that couple must agree; two incompatible geometries cannot coexist at one point. "At each coupling interface, gradient information must be exchanged: the field on one side must 'read' what the field on the other side is doing. The coupling must then settle into a single consistent state across all interfaces simultaneously. This settlement process is what we call field closure." Settlement is atomic: either every coupling channel agrees, or the configuration has not settled.

Paper I writes the whole chain in one line:

$$\text{field object} + \text{NET Field} \;\to\; \Sigma \;\to\; \text{READ} \to \text{SETTLE} \;\to\; B^*_\Sigma \;(\text{registered state}).$$

Each term has a standard counterpart: the complete snapshot is the initial-data surface, settlement is relaxation to equilibrium, and the registered state is the field once settled. Requiring settlement to be lossless and local gives the constitutive law $\mu(x) = x/(1+x)$, within the minimal single-channel saturating closure class.

Papers II and III give the read its extent and its unit. Closures are not isolated: their boundaries tile spacetime, and how they tile sets the acceleration scale $a_0 = cH/2\pi$ (Paper II). The tile itself is set at the electron scale, the classical electron radius $r_e$ (Paper III).

### 2. What is read: the lattice

*[`photonic/the-pixel-and-the-lattice.md`](../photonic/the-pixel-and-the-lattice.md), [`photonic/gfd_light_substrate_synthesis.md`](../photonic/gfd_light_substrate_synthesis.md), Paper VII §XI.A*

**In short:** the read runs over a lattice of stellated octahedra, and that lattice is the gravitational field.

Each photon is a stellated octahedron, the pixel. Packed on their four faces, photons form the lattice, and "Gravity is the lattice itself": there is no flat space beneath it. Mass is a vortex in the lattice, a closure driven through the Field Origin into TetB and held there, and a gravity field is "a pocket of subspace that has closed" around it. Near matter, the strata along which light travels curve, which is lensing.

The read meets two kinds of tile (Paper VII). The mesh of *unbound* envelopes, TetB chambers empty, is the long-range background, "the stage". *Bound* envelopes, TetB chambers occupied, are matter, "the actors". Because everything is made of the same packing, nothing can decouple from it, which is the equivalence principle.

### 3. What does the reading: the sweep

*[`read_sweep_synthesis.md`](read_sweep_synthesis.md), [`g_matrix_synthesis.md`](g_matrix_synthesis.md), Paper VI §8.3, Paper VII §V.B, §VI.A*

**In short:** a sweep reads the stellated octahedron to 21 levels, each costing one factor of $\alpha$, and that depth is Newton's constant.

The read-sweep note opens with the question this step answers: "if G is a matrix read, what is doing the reading?" The substrate is stationary; what moves is a pattern of activation, as in a stadium wave, where no one leaves their seat but the wave crosses the stadium. The read is a rotation through 64 sectors, and one rotation is one Compton period: one field closure. Paper VII gives the same rate in its own terms, $f_{\text{closure}}/f_{\text{Compton}} = 2\pi/\alpha$.

The 64 sectors carry three harmonic bands, of 1, $K = 4$ and $K^2 = 16$ cycles per rotation: the existence of the structure, its four directional channels and their sixteen couplings, $1 + K + K^2 = 21$ harmonics in all. Each level costs one factor of $\alpha$, and the factors multiply: the identity $\det(\alpha^{I}) = \alpha^{\mathrm{Tr}\,I}$ applies one factor per eigenvalue of the graded operator, so the full read is attenuated by $\alpha^{21}$. With the tile at $r_e$, $\alpha = r_e/\bar\lambda_C$ is the fraction of each quantum wavelength that the coupling structure occupies.

The same operator, read at the other two values of $s$, gives the prefactor. Each of the three values has a structural meaning:

| Value | Structure | Role in $G$ |
|---|---|---|
| $f(+1) = 21$ | Full TetA depth: scalar, 4 legs, 16 couplings | The exponent, $\alpha^{21}$ |
| $f(0) = K^2 + 1 = 17$ | The Field Origin, where the face channels are absent: 16 bimetric coupling channels plus the vertex | Numerator: coupling capacity |
| $f(-1) = DK + 1 = 13$ | TetB: the 4 face channels projected onto 3 spatial dimensions, plus one | Denominator: spatial structure |

Written in $K$ and $D$, with nothing but the dimension of spacetime in it, Newton's constant is

$$G = \frac{K^2 + 1}{DK + 1}\;\alpha^{\,1 + K + K^2}\;\frac{\hbar c}{m_e^2} = \frac{(3+1)^2 + 1}{3(3+1) + 1}\;\alpha^{\,1 + (3+1) + (3+1)^2}\;\frac{\hbar c}{m_e^2} = \frac{17}{13}\,\alpha^{21}\,\frac{\hbar c}{m_e^2}.$$

Neither the prefactor nor the exponent is adjustable; all three numbers follow from $K = 3+1$ and $D = 3$ (Eq. 24).

The ratio $17/13$ is derived twice, as coupling channels over structural elements (Paper VI, §8.3; [`FORMAL BRIDGING OF 17-13.md`](../../papers/06-gravitational-constant-from-topology/FORMAL%20BRIDGING%20OF%2017-13.md)) and as coupling capacity over spatial structure (Eq. 24). Letter 2 adds why the metric couples through 17: the sign representation carrying the parity-odd $K$ is absent from the Christoffel sector, so 17 is the parity-even core (see also the [algebraic pipeline](../../papers/algebraic-papers-a-b-c/algebraic_pipeline_of_reality.md)). The three values are locked together, $f(0) = \tfrac12[f(+1) + f(-1)]$ (Eq. 23), and among 1,953 simple alternatives no other prefactor and exponent come close.

The depth of the read also separates gravity from electromagnetism (§V.B). In ghost-free bimetric gravity, matter, including the electromagnetic field, couples to a single metric sector, so electromagnetism reaches only the first level and carries one factor of $\alpha$. Gravity is the interaction *between* the two sectors, through the Hassan–Rosen potential $V(\sqrt{g^{-1}f})$ (Hassan and Rosen 2012), so it must traverse all 21. The ratio is $\alpha^{20} \approx 10^{-43}$.

### 4. What the read produces: settlement, registration and motion

*[Paper I](../../papers/01-gravitational-constitutive-law/) §2.5; [Paper VII](../../papers/07-dual-tetrad-topology-field-origin/v7/Dual_Tetrad_Gravity_And_The_Field_Origin.pdf) §II.B, §VII.A, §XI*

**In short:** the read settles to one registered state; gravity is how that state changes from place to place, and motion is the sequence of registered states.

Paper VII carries Paper I's chain through in full. "Through each face of the local tetrahedron, the field reads and reconciles the geometric state of neighboring regions" (§II.B). The closure mechanism (§XI) has three steps:

1. **Full State Snapshot.** The whole configuration is read at once: the complete Cauchy data a well-posed initial-value problem needs.
2. **Settlement.** The snapshot is resolved to the single state that satisfies every constraint in both metric sectors: the solution of the Hamiltonian and momentum constraints (the York–Lichnerowicz method).
3. **Registration.** That state is recorded as $B^*_\Sigma$.

Gravity is how the registered state differs from one place to the next: "The gradients of the registered state $\nabla\ell(x)$ produce three manifestations of the same underlying process: gravitational acceleration, … gravitational lensing, … and time dilation."

Papers I and VII follow this through one running example, an asteroid in solar orbit. The asteroid is a field object, some $10^{33}$ coupled fields that the surrounding field meets as one configuration, as a chord is one sound rather than a list of notes. What it meets is the NET Field: the Sun, the planets and the galaxy already merged into one local state, as a boulder in a river feels only the current at its own position. At the closure boundary the two are read together, settled and registered. As the asteroid advances, the NET Field around it changes and closure runs again; its trajectory is the sequence of registered states. In Paper I's words, "The asteroid is not 'pulled' by a force at a distance. It is embedded in a field; that field couples to its field object… Gradients $\nabla\ell(x)$ determine motion." Because settlement is always complete, the asteroid leaves no constraint debris behind, and its own field follows it without lag.

Around a mass, the reconciliation spreads over a sphere in three dimensions, so it thins as $1/r^2$; the read-sweep note gives the same result as one sweep covering $4\pi = K\pi$ steradians.

Settlement also fixes how the field is shared between the chambers (§VII.A). The coupling capacity at each point is either resolved or unresolved. Resolution is driven by the field's intensity, $W_+ = \kappa\,x\,(1 - \varepsilon)$, and relaxation runs at $W_- = \kappa\,\varepsilon$. Detailed balance gives the resolved fraction $\varepsilon = x/(1+x) = \mu$, the "1" being the processing capacity of the single Field Origin. That is the third independent route to the law, after lossless local closure (Paper I) and exchange symmetry (Letter 2).

### 5. How general relativity sees the read: the connection

*[Letter 3](../../papers/letter-3-field-closure-of-tetrad-frame/), [Einstein's equation as the TetA partition](../../EINSTEIN_TETA_PARTITION.md)*

**In short:** general relativity describes the same comparison between neighbours, but keeps only the TetA part of it.

In general relativity the gravitational field is the connection, the rule that relates one local frame to the next: the comparison between neighbouring registered states, written in the language of geometry. It has 64 components, the $8 \times 8$ ordered transitions between the corners of neighbouring cubes. The torsion-free condition keeps the 40 that the metric can see and removes the 24 that carry the second root of the tetrad equation. General relativity is therefore exact where TetA carries the field, as in the solar system, and incomplete at galactic radii, where $\mu$ falls and TetB carries most of it. Restoring the 24 closes the field.

### 6. The algebra the read runs on: the cube

*[`universe-is-pixelated/`](../universe-is-pixelated/), [Paper C](../../papers/algebraic-papers-a-b-c/)*

**In short:** the read is a ±1 transform on the cube, and the cube's parity is what brings in the second chamber.

The cube's eight corners form a universal Boolean operator, read by its Walsh–Hadamard spectrum, and the blocks of size 1, 4 and 16 in G's graded operator are the Hadamard matrices $H_1$, $H_4$ and $H_{16}$. The octahedral resonance node shows a coupled oscillator on those corners producing the whole spectrum in one oscillation.

The spectrum factors as $H_8 = H_2 \otimes H_4$ (Paper C). $H_4$ is the frame within one tetrahedron; $H_2$ says which tetrahedron, and that is the cube's parity. General relativity keeps only the parity-even part, so it reads a single chamber. The full read needs $H_2$: both chambers, and with them $1 - \mu$. This is the bimetric result of step 3, seen from the algebra. At $D = 3$ the counts coincide, $2 \times 4 = 8$ corners and $K^3 = 64 = 8 \times 8$, which is why the cube and the stellated octahedron can be read as one object.

### 7. Measuring the read from observation

*[Decoding-mass letter](../../papers/letter-decoding-mass-from-rotation-curves/)*

**In short:** a rotation curve can be decoded into the mass the field implies, and comparing that with the visible mass shows what the second chamber is doing.

A star's orbit follows the total acceleration $g_t$, carried by both chambers, while the visible matter supplies only the TetA share, $g_s = \mu\,g_t$. The decoding-mass letter runs that relation backwards. From the measured rotation speeds alone, with no mass model, it returns the mass the field implies, $M_{\text{dec}}(r) = r\,v^4 / [G\,(a_0 r + v^2)]$.

This matters because TetB can drive the rotation or brake it. A galaxy's second chamber behaves like the drain of a water vortex: it can drive the flow, so the water circulates faster than the floating tracers alone would suggest, or hold it back. The tracers follow the rotation either way, so their speed alone does not say which. For the same reason, predicting a rotation curve from the visible mass alone is not, by itself, a test of the framework: it assumes a quiet interior, in which TetB neither adds to the field nor takes from it.

The decode measures it. The ratio of decoded to photometric mass at each radius, $R(r) = M_{\text{dec}}(r) / M_{\text{phot}}(r)$, reads the interior with no free parameter; the letter's mass difference, $\Delta M = M_{\text{phot}} - M_{\text{dec}}$, is the same measurement written as a difference.

| $R(r)$ | The field compared with the visible matter | TetB's role |
|---|---|---|
| $> 1$ | Stronger than the baryons supply | Driving the rotation |
| $\approx 1$ | What the baryons supply | Quiet |
| $< 1$ | Weaker than the baryons supply | Braking the rotation |

The galaxies decoded so far span the range:

| Galaxy | Radius | Decoded mass | $R$ | Reading |
|---|---|---|---|---|
| M33 | 17 kpc | $1.38 \times 10^{10}\,M_\odot$ | ≈ 2 | Driven |
| Milky Way | 25 kpc | $6.6 \times 10^{10}\,M_\odot$, against $7.3 \times 10^{10}$ in stars and gas | ≈ 0.9 | Close to quiet |
| Milky Way, Gaia DR3 speeds (Jiao et al. 2023; 181 km/s) | 25.5 kpc | ≈ $5 \times 10^{10}\,M_\odot$ | ≈ 0.7 | Braked, still near its baryons |
| CamB (low surface brightness) | Observed range | Below the visible mass | < 1 | Braked |

For comparison, $\Lambda$CDM needs about $2.3 \times 10^{11}\,M_\odot$ for the Milky Way at 25 kpc. Photometric masses carry uncertainties of up to a factor of two through the mass-to-light ratio, so only departures larger than that are clear signals.

---

## The field equation, read term by term

Paper VII (§IX) writes the Poisson equation with every factor named,

$$\nabla^2\Phi = K\pi \cdot \frac{K^2 + 1}{DK + 1} \cdot G_{\text{bare}} \cdot \rho, \qquad G_{\text{bare}} = \alpha^{21}\,\frac{\hbar c}{m_e^2},$$

and the constitutive law weights the gradient in the full equation, $\nabla \cdot \big[\mu(|\nabla\Phi|/a_0)\,\nabla\Phi\big] = 4\pi G \rho$. Each term belongs to a step of the mechanism:

| Term | Step | Meaning |
|---|---|---|
| $\nabla\Phi$ | 4, 5 | The difference between neighbouring registered states |
| $K\pi = 4\pi$ | 3 | One full sweep: the solid angle, divided into four parts of $\pi$ steradians by the faces of a regular tetrahedron |
| $17/13$ | 3 | Coupling capacity at the Field Origin over the spatial structure of TetB |
| $G_{\text{bare}}$ | 1, 3 | The $\alpha^{21}$-deep read, set in units by the electron-scale tile |
| $\mu$ | 4, 6 | The share of each comparison resolved through TetA; below $a_0$, TetB carries most of it |
| $\rho$ | 2 | The density of bound envelopes |

The two kinds of term do different jobs. $G$ is built from all three structural states at once, 21 in the exponent and 17/13 in the prefactor, so it is a constant; in the covariant action it sits in the curvature term, $R/16\pi G$. The constitutive law $\mu(x)$ sits in the scalar sector, through $F(y)$, and describes how the response is shared between the two chambers at each acceleration.

In one sentence: **gravity is the gradient of what field closure registers, where closure requires a read, the read is a sweep through the stellated octahedron to depth $\alpha^{21}$, and the cube's parity brings in the second chamber.**

---

## What remains open

The first open point is the one stated at the start: the seven steps above have not yet been written as a single derivation. The others are those the archive itself names.

### 1. The one physical input

Everything in G except one step is geometry and algebra. That step, as [`g_matrix_synthesis.md`](g_matrix_synthesis.md) states it, is that each coupling level attenuates by $\alpha$, because the frame is built from null directions and null means photonic. Step 3 gives the factor its physical meaning, $\alpha = r_e/\bar\lambda_C$, but the G derivation still lists it as its one physical assumption. The value of G supports it strongly: changing the exponent by one changes G by a factor of 137, and the look-elsewhere test finds no rival.

### 2. The one-loop correction

The tree-level residual, 0.117%, is the Schwinger term $\alpha/2\pi = 0.116\%$, the same correction that shifts the electron's magnetic moment (Schwinger 1948). Including it brings G to 12 ppm and moves the predicted Hubble constant from 70.21 to 70.29 km/s/Mpc (§X.B). [`synthesis_one_loop_G.md`](synthesis_one_loop_G.md) reads the factor structurally as $\tfrac{2}{17} \times \tfrac{17\alpha}{4\pi}$, the Field Origin impedance carried through one loop, and marks that reading as the subject of its own paper.

### 3. Lorentz invariance of the discrete picture

Any discrete picture of spacetime must respect Lorentz invariance. Fermi observations of GRB 090510 constrain violations beyond 7.6 Planck energies (Vasileiou et al. 2013), and GW170817 confirms that gravity travels at $c$ to about one part in $10^{15}$ (Abbott et al. 2017). The pixelated README sets out why GFD's grid has no spacing to feel: propagation is closure, not motion across a mesh, and each cube is the local frame of its own event. It names the formal proof, that the Walsh structure of the frame keeps $\omega = ck$ exact, as the next step.

### 4. Beyond the electron

Paper VII closes by naming what its results do not yet address: how the non-linear coupling at the Field Origin produces the full spectrum of bound configurations beyond the electron, and how the field dynamics of the $K = 4$ topology connect to the gauge dynamics of the Standard Model, the strong and weak forces and the particle mass hierarchy.

The graviton belongs here too. Paper VII identifies the massless spin-2 mode of bimetric gravity with the unbound mesh, and the massive mode, confined by its own coupling, with bound envelopes: Wheeler's geons (Wheeler 1955) realised as matter. The light-substrate notes describe the graviton as two stellated octahedra coupled at a face, and the quantum-gravity folder makes contact with Regge calculus and loop quantum gravity. How the quantised theory follows is open.

---

## What would decide it

Paper VII lists the framework's distinctive predictions, each of which can fail:

- **The massive graviton.** $\beta_n = (1, 0, 16, 0, 1)$ fixes the bimetric mass spectrum, which gravitational-wave dispersion measurements from LIGO, Virgo and KAGRA constrain directly.
- **An acceleration scale that changes with time.** $a_0$ is tied to the Hubble rate, so it was larger in the past. Rotation curves at redshift $z > 1$, from JWST and Euclid, test this; standard MOND assumes a constant $a_0$ (Milgrom 1983).
- **The value of $H$.** With $G$ and $m_e$ fixed, $H = 70.21$ km/s/Mpc at tree level and 70.29 at one loop, between the Planck and SH0ES values.

Two further measurements follow from this note:

- **A drive–brake map.** Running all 175 SPARC galaxies through the inverse pipeline would give $R(r)$ at every measured radius. How driving and braking depend on surface brightness, morphology and environment is the measurement that would show what the second chamber is doing, and it needs no free parameter.
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
