# What Is Gravity?

### An open question, set out from the archive's own results

*Field Dynamics Research · a synthesis of [`g_from_topology/`](./), [`universe-is-pixelated/`](../universe-is-pixelated/), [`photonic/`](../photonic/), [`field-closure/`](../field-closure/) and the tetrad letters*

---

## The question

The work in this archive answers three questions about gravity with unusual precision:

- **How strong it is.** $G = \tfrac{17}{13}\,\alpha^{21}\,\hbar c/m_e^2$, within 0.12% of the measured value at tree level and 12 parts per million with the one-loop factor $1 + \alpha/2\pi$.
- **What shape it has.** The connection has 64 components. General relativity keeps 40 and removes 24, and the constitutive law $\mu(x) = x/(x+1)$ shares the field between the two tetrahedral chambers at every radius.
- **How it travels.** At $c$, the same speed as light, as GW170817 confirmed.

A fourth question, **what gravity is**, is answered in several places, each from a different side of the work: as a lattice, as a read, as closure settling, as a connection and as a computing medium.

This note sets those readings side by side and shows how they fit into one picture. It records what any answer must account for, what each reading contributes, the synthesis, and what the archive itself still names as open. It is written as an open question because the synthesis, though built entirely from derived pieces, has not yet been stated as one derivation.

---

## What any answer must account for

These results are established within the framework, by derivation, by computation or against measurement. Any account of what gravity is has to produce all of them.

| Result | Status | Where |
|---|---|---|
| $G = \tfrac{17}{13}\,\alpha^{21}\,\hbar c/m_e^2$; 0.12% at tree level, 12 ppm with $1 + \alpha/2\pi$ | Matches measurement; G itself is known to 22 ppm | [`g_matrix_synthesis.md`](g_matrix_synthesis.md), [`synthesis_one_loop_G.md`](synthesis_one_loop_G.md) |
| Among 1,953 alternatives $(p/q)\,\alpha^n$ with $p, q \le 21$ and $n = 18$–24, only $17/13 \cdot \alpha^{21}$ lands within 0.12%, and only it lands within 22 ppm with the loop factor | Computed | [`look_elsewhere_G.py`](look_elsewhere_G.py) |
| The three values 21, 17, 13 are the traces of one graded operator, $\mathrm{Tr}(P_0 + sP_1 + P_2) = 1 + sK + K^2$, on blocks of size 1, 4 and 16 | Exact | [`g_matrix_synthesis.md`](g_matrix_synthesis.md) |
| The connection's 64 components split 40 + 24; the 24 carry the second root of the tetrad equation | Exact count; the identification is Letter 3's claim | [Letter 3 guide](../../FIELD_CLOSURE_OF_THE_TETRAD_FRAME.md) |
| $\mu(x) = x/(x+1)$ reproduces the radial acceleration relation with no free parameter | Matches 175 galaxies | Letter 3; the SPARC letter |
| The field equations run both ways: an observed rotation curve decodes to an effective mass, $M_{\text{dec}} = r v^4 / [G(a_0 r + v^2)]$, with no mass model and no halo. For the Milky Way and M33 the decoded mass lands near the baryonic mass, where $\Lambda$CDM needs three to five times more | Demonstrated on the Milky Way, M33 and NGC 3198 | [Decoding-mass letter](../../papers/letter-decoding-mass-from-rotation-curves/) |
| Gravity couples to everything equally, is only ever attractive, and travels at $c$ | Observed | Equivalence principle; GW170817 |
| The cube's eight corners carry every three-input Boolean operation; its spectrum factors as $H_8 = H_2 \otimes H_4$ | Established mathematics | [`universe-is-pixelated/`](../universe-is-pixelated/) |

---

## Five readings already in the archive

### 1. Gravity is the lattice

*[`photonic/the-pixel-and-the-lattice.md`](../photonic/the-pixel-and-the-lattice.md), [`photonic/gfd_light_substrate_synthesis.md`](../photonic/gfd_light_substrate_synthesis.md)*

Each photon is a stellated octahedron, the pixel. When photons pack on their four faces, the packing is the gravitational field: "Gravity is the lattice itself." Remove the lattice and there is no flat space left behind, only nothing. Mass is a vortex in the lattice, a closure driven through the Field Origin into TetB and held there.

Mass organises the lattice around itself: a gravity field is "a pocket of subspace that has closed" around a mass concentration, and near matter the strata along which light travels curve, which is lensing.

*What it contributes:* the substrate, the equivalence principle (everything is made of the same packing, so nothing can decouple from it), and why gravity only attracts (the coupling polynomial increases monotonically with $s$).

### 2. Gravity is the read sweep

*[`read_sweep_synthesis.md`](read_sweep_synthesis.md), [`g_matrix_synthesis.md`](g_matrix_synthesis.md)*

The substrate is stationary; what moves is a pattern of activation, as in a stadium wave. Light is a pattern that advances in a line. Matter is a pattern trapped at the boundary between the chambers. Gravity is a pattern that sweeps around 64 sectors in three harmonic bands of 1, 4 and 16, which gives 21 harmonics per rotation, each attenuated by $\alpha$. That is where $\alpha^{21}$ comes from.

The same notes carry the sweep into the field equation: one full sweep covers $4\pi = K\pi$ steradians, the inverse-square law and Gauss's law follow from $D = 3$, and $\mu(x)$ is the fraction of the sweep that completes at a given field strength.

*What it contributes:* the strength of gravity, and why it is weaker than electromagnetism by $\alpha^{20} \approx 10^{-43}$.

### 3. Gravity is closure settling

*[Paper I](../../papers/01-gravitational-constitutive-law/), [Paper VII](../../papers/07-dual-tetrad-topology-field-origin/v7/Dual_Tetrad_Gravity_And_The_Field_Origin.pdf), [`field-closure/`](../field-closure/)*

A field that carries waves must have parts, and parts that couple must reconcile. Where one field meets another, each side reads the other and the coupling settles into a single consistent state. Settlement is atomic: every channel agrees, or the field has not settled. Requiring that settlement to be lossless and local gives $\mu(x) = x/(x+1)$ within the minimal single-channel saturating closure class.

Paper VII carries this reading furthest. "Through each face of the local tetrahedron, the field reads and reconciles the geometric state of neighboring regions" (§II.B). Its closure mechanism (§XI) runs in three steps: a *Full State Snapshot* reads the whole configuration at once, *Settlement* resolves it to the single state that satisfies every constraint in both metric sectors, and *Registration* records that state. Then: "The gradients of the registered state $\nabla\ell(x)$ produce three manifestations of the same underlying process: gravitational acceleration, … gravitational lensing, … and time dilation." A body's trajectory is the sequence of its registered states. Paper VII grounds each step in established physics: the snapshot is the complete Cauchy data that a well-posed initial-value problem needs, and settlement is the solution of the Hamiltonian and momentum constraints (the York–Lichnerowicz method). Paper VII also derives the constitutive law from settlement itself (§VII.A). The coupling capacity at each point is either resolved or unresolved; resolution is driven by the field's intensity, $W_+ = \kappa\,x\,(1 - \varepsilon)$, and relaxation runs at $W_- = \kappa\,\varepsilon$. Detailed balance gives the resolved fraction $\varepsilon = x/(1+x) = \mu$, with the "1" as the processing capacity of the single Field Origin. That makes three independent routes to the same law: lossless local closure (Paper I), exchange symmetry (Letter 2) and detailed balance (Paper VII).

*What it contributes:* the mechanism, the constitutive law, why gravity is bookkeeping, and why acceleration, lensing and time dilation are one effect, not three.

### 4. Gravity is the connection

*[Letter 3](../../papers/letter-3-field-closure-of-tetrad-frame/), [Einstein's equation as the TetA partition](../../EINSTEIN_TETA_PARTITION.md)*

In general relativity the gravitational field is the connection: the rule that relates one local frame to the next. It has 64 components. The torsion-free condition keeps the 40 that the metric can see and removes the 24 that carry the second root. Restoring them closes the field.

*What it contributes:* the shape of gravity, the 40/24 split, and why general relativity is exact in the solar system and incomplete at galactic radii.

### 5. Gravity is the pixel computing

*[`universe-is-pixelated/`](../universe-is-pixelated/)*

The cube's eight corners form a universal Boolean operator, read by its Walsh–Hadamard spectrum. The octahedral resonance node shows a coupled oscillator on those corners producing the whole spectrum in one oscillation. On this reading, the null cone of every event is a computer, and a lattice of them is a computing medium.

*What it contributes:* why the same ±1 structures appear in the cube, the tetrad and G's graded operator. The blocks of size 1, 4 and 16 are the Hadamard matrices $H_1$, $H_4$ and $H_{16}$.

---

## A candidate synthesis: gravity as the difference between neighbouring reads

Each reading supplies a piece of one picture. Its core is not new: it is Paper VII's closure mechanism, in which gravity is the gradient of the registered state. What follows adds where that state's strength and completeness come from.

**Gravity lives in the comparison between neighbours.** What a body responds to is the gradient of the potential, not its value. Paper I's starting point is that the Laplacian at the heart of the field equation is a comparison between neighbours, $\Phi(x+\epsilon) + \Phi(x-\epsilon) - 2\Phi(x)$. The connection is by definition the rule relating one frame to the next, and its 64 components are the $8 \times 8$ ordered transitions between the corners of neighbouring cubes. On this view gravity lives in the transitions, not in the cells.

**The stellated octahedron sets the strength.** G's exponent, $21 = 1 + K + K^2$, counts the levels of the tetrad: a scalar, the four legs of one tetrahedron and their sixteen couplings. These blocks are built from $K = 4$, not from the cube's $2^3$. Each level costs one factor of $\alpha$, and the factors multiply: the determinant identity $\det(\alpha^{I}) = \alpha^{\mathrm{Tr}\,I}$ applies one factor per eigenvalue of the graded operator, so the exchange between neighbours is attenuated by $\alpha^{21}$, read at full TetA depth. The prefactor $17/13$ is derived twice, as coupling channels over structural elements (Paper VI, §8.3; [`FORMAL BRIDGING OF 17-13.md`](../../papers/06-gravitational-constant-from-topology/FORMAL%20BRIDGING%20OF%2017-13.md)) and as coupling capacity over spatial structure ([Paper VII](../../papers/07-dual-tetrad-topology-field-origin/v7/Dual_Tetrad_Gravity_And_The_Field_Origin.pdf), Eq. 24). The numerator, $k^2 + 1 = 17$, is the Field Origin, where the face channels are absent: the 16 bimetric coupling channels plus the non-degenerate vertex itself. It is also the parity-even core that the metric couples through, since the sign representation carrying the parity-odd $k$ is absent from the Christoffel sector (Letter 2; the [algebraic pipeline](../../papers/algebraic-papers-a-b-c/algebraic_pipeline_of_reality.md)). The denominator, $kd + 1 = 13$, is TetB, the $k = 4$ face channels projected onto $d = 3$ spatial dimensions plus one for non-degeneracy. The three values are locked together, $f(0) = \tfrac12[f(+1) + f(-1)]$ (Paper VII, Eq. 23), and among 1,953 simple alternatives no other prefactor and exponent come close.

**The cube completes it.** The cube's spectrum factors as $H_8 = H_2 \otimes H_4$ (Paper C). $H_4$ is the frame within one tetrahedron; $H_2$ says which tetrahedron, and that is the cube's parity. General relativity keeps only the parity-even part, so it reads a single chamber. The full field needs $H_2$: both chambers, and with them $1 - \mu$. At $D = 3$ the two counts coincide, $2 \times 4 = 8$ corners and $K^3 = 64 = 8 \times 8$, which is why the cube and the stellated octahedron can be read as one object.

**Free fall is settling.** A mass is a trapped closure. The frames around it must reconcile with it, and in three dimensions that reconciliation thins out as $1/r^2$, because it spreads over a sphere of area $4\pi r^2$. A body placed in that region settles into the state of its neighbours, which differ slightly from one side to the other. On this reading, moving along that difference *is* the settling: nothing pushes. General relativity treats free fall the same way, as motion with no force acting.

**Gravity reads both chambers; electromagnetism reads one.** Paper VII (§V.B) gives the reason the two forces read to different depths. In ghost-free bimetric gravity, matter, including the electromagnetic field, couples to a single metric sector, so electromagnetism reaches only the first level and carries one factor of $\alpha$. Gravity is the interaction *between* the two sectors, through the potential $V(\sqrt{g^{-1}f})$, so it must traverse all 21 levels. The ratio is $\alpha^{20} \approx 10^{-43}$. Gravity's need for both chambers, which the cube's $H_2$ factor expresses, is the same fact seen from the bimetric side.

Observation shows the same thing. A star's orbit follows the total acceleration $g_t$, the field carried by both chambers, while the visible matter supplies only the TetA share, $g_s = \mu\,g_t$. The [decoding-mass letter](../../papers/letter-decoding-mass-from-rotation-curves/) runs that relation backwards: from the measured rotation speeds alone, with no mass model, it returns the mass the field implies, $M_{\text{dec}}(r) = r\,v^4 / [G\,(a_0 r + v^2)]$. For the Milky Way at 25 kpc the decoded mass is about $6.6 \times 10^{10}\,M_\odot$, against $7.3 \times 10^{10}\,M_\odot$ in stars and gas, where $\Lambda$CDM needs about $2.3 \times 10^{11}\,M_\odot$.

**TetB can drive the rotation or brake it.** This is why a forward prediction of rotation speed cannot settle the question on its own. Predicting a rotation curve from the visible mass assumes a quiet interior, in which TetB neither adds to the field nor takes from it. A galaxy's second chamber behaves more like the drain of a water vortex. The drain can drive the flow, so the water circulates faster than the floating tracers alone would suggest, or it can hold the flow back. The tracers follow the rotation either way, so their speed alone does not say which.

The decode measures it. Comparing the decoded mass with the photometric mass at each radius, the ratio $R(r) = M_{\text{dec}}(r) / M_{\text{phot}}(r)$ reads the interior with no free parameter:

| $R(r)$ | The field compared with the visible matter | TetB's role |
|---|---|---|
| $> 1$ | Stronger than the baryons supply | Driving the rotation |
| $\approx 1$ | What the baryons supply | Quiet |
| $< 1$ | Weaker than the baryons supply | Braking the rotation |

The letter's mass difference, $\Delta M(r) = M_{\text{phot}}(r) - M_{\text{dec}}(r)$, is the same measurement written as a difference. The galaxies already decoded span the range. In M33 the decoded mass at 17 kpc, $1.38 \times 10^{10}\,M_\odot$, is roughly twice the visible mass: the outer disk is driven. In the Milky Way, $R \approx 0.9$ at 25 kpc: close to quiet. The lower outer speeds reported from Gaia DR3 (Jiao et al. 2023), about 181 km/s at 25.5 kpc, decode to about $5 \times 10^{10}\,M_\odot$, $R \approx 0.7$: the outer Milky Way braked, but still close to its baryons and nowhere near a halo. In the low-surface-brightness galaxy CamB the decoded mass falls below the visible mass across the observed range: braked. Because photometric masses themselves carry uncertainties of up to a factor of two, through the mass-to-light ratio, only departures larger than that are clear signals.

The field equation can be read term by term in these words. Paper VII (§IX) writes the Poisson equation with every factor named:

$$\nabla^2\Phi = k\pi \cdot \frac{k^2 + 1}{kd + 1} \cdot G_{\text{bare}} \cdot \rho, \qquad G_{\text{bare}} = \alpha^{21}\,\frac{\hbar c}{m_e^2},$$

and the constitutive law weights the gradient in the full equation, $\nabla \cdot \big[\mu(|\nabla\Phi|/a_0)\,\nabla\Phi\big] = 4\pi G \rho$.

| Term | Reading |
|---|---|
| $\nabla\Phi$ | The difference between neighbouring registered states |
| $k\pi = 4\pi$ | The full solid angle, divided into four equal parts of $\pi$ steradians by the faces of a regular tetrahedron: a pure number, with no radius in it |
| $17/13$ | Coupling capacity at the Field Origin over the spatial structure of TetB |
| $G_{\text{bare}}$ | The $\alpha^{21}$-deep read, set in units by the electron |
| $\mu$ | The share of each comparison resolved through TetA; below $a_0$, TetB carries most of it |
| $\rho$ | The density of trapped closures |

The two kinds of term do different jobs. $G$ is built from all three structural states of the polynomial at once, 21 in the exponent and 17/13 in the prefactor, so it is a constant; in the covariant action it sits in the curvature term, $R/16\pi G$. The constitutive law $\mu(x)$ sits in the scalar sector, through $F(y)$, and describes how the response is shared between the two chambers at each acceleration.

In one sentence: **gravity is how far the closure of neighbouring frames differs, at a strength set by how deep the stellated octahedron must be read, and completed by the cube's parity, which brings in the second chamber.**

**The lattice is the stage; gravity is its gradients.** Paper VII (§XI.A) places the two descriptions. The mesh of *unbound* gravity-field envelopes, TetB chambers empty, is the long-range background: "the stage". *Bound* envelopes, TetB chambers occupied, are matter: "the actors". The lattice is the gravitational field, and what a body feels is the gradient of its registered state, as in general relativity the metric is the field and its curvature is what free-falling bodies feel.

The mechanism is Paper VII's, the strength is the G derivation, the shape is Letter 3, and the share is $\mu$: every piece is derived in the archive.

---

## What remains open

These are the open points the archive itself names.

### 1. The one physical input

Everything in G except one step is geometry and algebra. That step, as [`g_matrix_synthesis.md`](g_matrix_synthesis.md) states it, is that each coupling level attenuates by $\alpha$: the frame is built from null directions, and null means photonic. Paper VII gives the factor its meaning (§VI.A): with the tile scale identified as the classical electron radius $r_e$, $\alpha = r_e/\bar\lambda_C$ is the fraction of each quantum wavelength that the coupling structure occupies, and the same ratio appears in the rates, $f_{\text{closure}}/f_{\text{Compton}} = 2\pi/\alpha$. The value of G supports the step strongly: changing the exponent by one changes G by a factor of 137, and the look-elsewhere test finds no rival.

### 2. The one-loop correction

The tree-level residual, 0.117%, is the Schwinger term $\alpha/2\pi = 0.116\%$, the same correction that shifts the electron's magnetic moment; including it brings G to 12 ppm and moves the predicted Hubble constant from 70.21 to 70.29 km/s/Mpc (Paper VII, §X.B). [`synthesis_one_loop_G.md`](synthesis_one_loop_G.md) reads the factor structurally as $\tfrac{2}{17} \times \tfrac{17\alpha}{4\pi}$, the Field Origin impedance carried through one loop, and marks that reading as the subject of its own paper.

### 3. Lorentz invariance of the discrete picture

Any discrete picture of spacetime must respect Lorentz invariance, which Fermi observations of GRB 090510 constrain beyond 7.6 Planck energies, and which GW170817 confirms for gravity to about one part in $10^{15}$. The pixelated README sets out why GFD's grid has no spacing to feel: propagation is closure, not motion across a mesh, and each cube is the local frame of its own event. It names the formal proof, that the Walsh structure of the frame keeps $\omega = ck$ exact, as the next step.

### 4. Beyond the electron

Paper VII closes by naming what its results do not yet address: how the non-linear coupling at the Field Origin produces the full spectrum of bound configurations beyond the electron, and how the field dynamics of the $k = 4$ topology connect to the gauge dynamics of the Standard Model, the strong and weak forces and the particle mass hierarchy. The graviton belongs here too. Paper VII identifies the massless spin-2 mode of bimetric gravity with the unbound mesh and the massive mode, confined by its own coupling, with bound envelopes, Wheeler's geons realised as matter; the light-substrate notes describe the graviton as two stellated octahedra coupled at a face, and the quantum-gravity folder makes contact with Regge calculus and loop quantum gravity. How the quantised theory follows is open.

---

## What would decide it

Paper VII lists the framework's distinctive predictions, each of which can fail:

- **The massive graviton.** $\beta_n = (1, 0, 16, 0, 1)$ fixes the bimetric mass spectrum, which gravitational-wave dispersion measurements from LIGO, Virgo and KAGRA constrain directly.
- **An acceleration scale that changes with time.** $a_0$ is tied to the Hubble rate, so it was larger in the past. Rotation curves at redshift $z > 1$, from JWST and Euclid, test this; standard MOND assumes a constant $a_0$.
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

- Abbott, B. P. et al. (2017). Gravitational waves and gamma-rays from a binary neutron star merger: GW170817 and GRB 170817A. *Astrophys. J. Lett.* 848, L13.
- Banik, I. et al. (2024). Strong constraints on the gravitational law from Gaia DR3 wide binaries. *Mon. Not. R. Astron. Soc.* 527, 4573.
- Chae, K.-H. (2023). Breakdown of the Newton–Einstein standard gravity at low acceleration in internal dynamics of wide binary stars. *Astrophys. J.* 952, 128.
- Jiao, Y., Hammer, F., Flores, H., Wang, J. L. and Yang, Y. (2023). Detection of the Keplerian decline in the Milky Way rotation curve. *Astron. Astrophys.* 678, A208.
- Nelson, S. (2026). *Dual Tetrad Topology and the Field Origin: From Nuclear Decay to Galactic Dynamics* (Paper VII). [`papers/07-dual-tetrad-topology-field-origin/`](../../papers/07-dual-tetrad-topology-field-origin/).
- Tiesinga, E. et al. (2021). CODATA recommended values of the fundamental physical constants: 2018. *Rev. Mod. Phys.* 93, 025010.
- Vasileiou, V. et al. (2013). Constraints on Lorentz invariance violation from Fermi-Large Area Telescope observations of gamma-ray bursts. *Phys. Rev. D* 87, 122001.
