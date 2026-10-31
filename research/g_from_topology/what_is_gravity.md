# What Is Gravity?

### An open question, set out from the archive's own results

*Field Dynamics Research · a synthesis of [`g_from_topology/`](./), [`universe-is-pixelated/`](../universe-is-pixelated/), [`photonic/`](../photonic/), [`field-closure/`](../field-closure/) and the tetrad letters*

---

## The question

The work in this archive answers three questions about gravity with unusual precision:

- **How strong it is.** $G = \tfrac{17}{13}\,\alpha^{21}\,\hbar c/m_e^2$, within 0.12% of the measured value at tree level and 12 parts per million with the one-loop factor $1 + \alpha/2\pi$.
- **What shape it has.** The connection has 64 components. General relativity keeps 40 and removes 24, and the constitutive law $\mu(x) = x/(x+1)$ shares the field between the two tetrahedral chambers at every radius.
- **How it travels.** At $c$, the same speed as light, as GW170817 confirmed.

It does not yet answer a fourth question in a single statement: **what gravity is.** Several answers have been written down in different folders, each drawn from a different part of the work. They are not obviously the same answer, and in places they pull against each other.

This note sets them side by side. It records what any answer must account for, the readings already in the archive, one candidate synthesis, and the tensions a complete answer would have to resolve. It is written as an open question, because that is what it is.

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

*What it explains well:* the equivalence principle (everything is made of the same packing, so nothing can decouple from it) and why gravity only attracts (the coupling polynomial increases monotonically with $s$).
*What it leaves open:* a uniform lattice exerts no force, so the lattice alone is spacetime rather than gravity's pull. The reading has to say what about the lattice produces attraction.

### 2. Gravity is the read sweep

*[`read_sweep_synthesis.md`](read_sweep_synthesis.md), [`g_matrix_synthesis.md`](g_matrix_synthesis.md)*

The substrate is stationary; what moves is a pattern of activation, as in a stadium wave. Light is a pattern that advances in a line. Matter is a pattern trapped at the boundary between the chambers. Gravity is a pattern that sweeps around 64 sectors in three harmonic bands of 1, 4 and 16, which gives 21 harmonics per rotation, each attenuated by $\alpha$. That is where $\alpha^{21}$ comes from.

*What it explains well:* the strength of gravity, and why it is weaker than electromagnetism by $\alpha^{20} \approx 10^{-43}$.
*What it leaves open:* a sweep describes a process at one place. It does not say how two places come to differ, which is what a force requires.

### 3. Gravity is closure settling

*[Paper I](../../papers/01-gravitational-constitutive-law/), [Paper VII](../../papers/07-dual-tetrad-topology-field-origin/v7/Dual_Tetrad_Gravity_And_The_Field_Origin.pdf), [`field-closure/`](../field-closure/)*

A field that carries waves must have parts, and parts that couple must reconcile. Where one field meets another, each side reads the other and the coupling settles into a single consistent state. Settlement is atomic: every channel agrees, or the field has not settled. Requiring that settlement to be lossless and local gives $\mu(x) = x/(x+1)$ within the minimal single-channel saturating closure class.

Paper VII carries this reading furthest. "Through each face of the local tetrahedron, the field reads and reconciles the geometric state of neighboring regions" (§II.B). Its closure mechanism (§XI) runs in three steps: a *Full State Snapshot* reads the whole configuration at once, *Settlement* resolves it to the single state that satisfies every constraint in both metric sectors, and *Registration* records that state. Then: "The gradients of the registered state $\nabla\ell(x)$ produce three manifestations of the same underlying process: gravitational acceleration, … gravitational lensing, … and time dilation." A body's trajectory is the sequence of its registered states. Paper VII grounds each step in established physics: the snapshot is the complete Cauchy data that a well-posed initial-value problem needs, and settlement is the solution of the Hamiltonian and momentum constraints (the York–Lichnerowicz method).

*What it explains well:* the constitutive law, why gravity is bookkeeping, and why acceleration, lensing and time dilation are one effect, not three.
*What it leaves open:* the registered field $\ell(x)$ is named but not built cell by cell, so its continuum limit has not been taken.

### 4. Gravity is the connection

*[Letter 3](../../papers/letter-3-field-closure-of-tetrad-frame/), [Einstein's equation as the TetA partition](../../EINSTEIN_TETA_PARTITION.md)*

In general relativity the gravitational field is the connection: the rule that relates one local frame to the next. It has 64 components. The torsion-free condition keeps the 40 that the metric can see and removes the 24 that carry the second root. Restoring them closes the field.

*What it explains well:* the shape of gravity, the 40/24 split, and why general relativity is exact in the solar system and incomplete at galactic radii.
*What it leaves open:* why the connection's strength is $\alpha^{21}$.

### 5. Gravity is the pixel computing

*[`universe-is-pixelated/`](../universe-is-pixelated/)*

The cube's eight corners form a universal Boolean operator, read by its Walsh–Hadamard spectrum. The octahedral resonance node shows a coupled oscillator on those corners producing the whole spectrum in one oscillation. On this reading, the null cone of every event is a computer, and a lattice of them is a computing medium.

*What it explains well:* why the same ±1 structures appear in the cube, the tetrad and G's graded operator. The blocks of size 1, 4 and 16 are the Hadamard matrices $H_1$, $H_4$ and $H_{16}$.
*What it leaves open:* which computation gravity is.

---

## A candidate synthesis: gravity as the difference between neighbouring reads

Each reading supplies a piece the others lack. One way to fit them together is this. Its core is not new: it is Paper VII's closure mechanism, in which gravity is the gradient of the registered state. What follows adds where that state's strength and completeness come from.

**A single read produces no force.** If every cell of the lattice read the same, nothing would move. A uniform gravitational potential exerts no force either; only its gradient does. Paper I's starting point is that the Laplacian at the heart of the field equation is a comparison between neighbours, $\Phi(x+\epsilon) + \Phi(x-\epsilon) - 2\Phi(x)$. The connection is by definition the rule relating one frame to the next, and its 64 components are the $8 \times 8$ ordered transitions between the corners of neighbouring cubes. On this view gravity lives in the transitions, not in the cells.

**The stellated octahedron sets the strength.** G's exponent, $21 = 1 + K + K^2$, counts the levels of the tetrad: a scalar, the four legs of one tetrahedron and their sixteen couplings. These blocks are built from $K = 4$, not from the cube's $2^3$. If each level costs one factor of $\alpha$, the exchange between neighbours is attenuated by $\alpha^{21}$, read at full TetA depth. The prefactor $17/13$ is the parity-even core that the metric couples through (17) over the TetB scaffold that carries it (13).

**The cube completes it.** The cube's spectrum factors as $H_8 = H_2 \otimes H_4$ (Paper C). $H_4$ is the frame within one tetrahedron; $H_2$ says which tetrahedron, and that is the cube's parity. General relativity keeps only the parity-even part, so it reads a single chamber. The full field needs $H_2$: both chambers, and with them $1 - \mu$. At $D = 3$ the two counts coincide, $2 \times 4 = 8$ corners and $K^3 = 64 = 8 \times 8$, which is why the cube and the stellated octahedron can be read as one object.

**Free fall is settling.** A mass is a trapped closure. The frames around it must reconcile with it, and in three dimensions that reconciliation thins out as $1/r^2$, because it spreads over a sphere of area $4\pi r^2$. A body placed in that region settles into the state of its neighbours, which differ slightly from one side to the other. On this reading, moving along that difference *is* the settling: nothing pushes. General relativity treats free fall the same way, as motion with no force acting.

**Gravity reads both chambers; electromagnetism reads one.** Paper VII (§V.B) gives the reason the two forces read to different depths. In ghost-free bimetric gravity, matter, including the electromagnetic field, couples to a single metric sector, so electromagnetism reaches only the first level and carries one factor of $\alpha$. Gravity is the interaction *between* the two sectors, through the potential $V(\sqrt{g^{-1}f})$, so it must traverse all 21 levels. The ratio is $\alpha^{20} \approx 10^{-43}$. Gravity's need for both chambers, which the cube's $H_2$ factor expresses, is the same fact seen from the bimetric side.

Observation shows the same thing. A star's orbit follows the total acceleration $g_t$, the field carried by both chambers, while the visible matter supplies only the TetA share, $g_s = \mu\,g_t$. The [decoding-mass letter](../../papers/letter-decoding-mass-from-rotation-curves/) runs that relation backwards: from the measured rotation speeds alone, with no mass model, it returns the mass that the field implies. For the Milky Way at 25 kpc the decoded mass is about $6.6 \times 10^{10}\,M_\odot$, against $7.3 \times 10^{10}\,M_\odot$ in stars and gas; $\Lambda$CDM needs about $2.3 \times 10^{11}\,M_\odot$. Even the lower outer speeds reported from Gaia DR3 (Jiao et al. 2023), about 181 km/s at 25.5 kpc, decode to about $5 \times 10^{10}\,M_\odot$: still close to the baryons, and nowhere near a halo. Read through both chambers, the rotation needs no unseen mass.

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

In one sentence: **gravity would be how far the closure of neighbouring frames differs, at a strength set by how deep the stellated octahedron must be read, and completed by the cube's parity, which brings in the second chamber.**

The mechanism is Paper VII's, and each ingredient is derived in the archive. What has not been derived is the continuum limit that would turn a cell-by-cell read into this equation.

---

## Tensions a complete answer must resolve

### 1. Why one factor of $\alpha$ per level?

Everything in G except one step is geometry and algebra. That step is the claim that each coupling level attenuates by $\alpha$. The value of G strongly supports it: changing the exponent by one changes G by a factor of 137, and the look-elsewhere test finds no rival.

Paper VII supplies the meaning of the factor (§VI.A). With the tile scale identified as the classical electron radius $r_e$, the fine-structure constant is the ratio of that scale to the quantum coherence length, $\alpha = r_e/\bar\lambda_C$: the fraction of each quantum wavelength that the coupling structure occupies. The same ratio appears in the rates, $f_{\text{closure}}/f_{\text{Compton}} = (c/r_e)/(m_e c^2/h) = 2\pi/\alpha$. Paper VII also explains why electromagnetism reads one level and gravity all 21 (the synthesis above).

What remains open is why the attenuation *compounds*, one factor per level, so that 21 levels give $\alpha^{21}$ rather than some other function of 21. Paper VII states the compounding; a derivation of it from the coupling of successive levels would close the last physical step in G.

### 2. A fixed depth and a sliding partition

G uses all three values of the polynomial at once, $21$ in the exponent and $17/13$ in the prefactor, and it is a constant. The partition slides: the continuous field equation $f(x) = (21x + 13)/(x + 1) = 13 + 8\mu(x)$ moves from 21 in strong fields to 13 in weak ones. If the strength of gravity were $\alpha$ raised to the local depth $f(x)$, weak-field gravity would be $\alpha^{-8} \approx 10^{17}$ times stronger than strong-field gravity, which is plainly not the case. So depth and partition must act in different ways.

Paper VII's second derivation of $\mu$ (§VII.A) suggests how. It treats the coupling capacity at each point as two-state: a *resolved* fraction $\varepsilon$ that tracks the Newtonian demand, and an *unresolved* fraction $1 - \varepsilon$. Resolution is driven by the field's intensity, $W_+ = \kappa\,x\,(1-\varepsilon)$, and relaxation runs at $W_- = \kappa\,\varepsilon$. Detailed balance, $W_+ = W_-$, gives $\varepsilon = x/(1+x) = \mu$, and the "1" in the denominator is the processing capacity of the single Field Origin, a bottleneck. On that reading the depth is the length of the path every exchange must travel, fixed at 21 levels, and so it fixes the constant; $\mu$ is the throughput, the fraction of the capacity resolved at the local intensity. Path length sets the strength; throughput sets the share. This separates the two roles cleanly. Deriving the rates, and showing that the saturation of the 16 + 4 channels below $a_0$ is exactly this two-state balance, would make it a result rather than a reading.

### 3. The prefactor is settled; the loop factor's reading is not

The prefactor $17/13$ is derived, in two papers. Paper VI (§8.3, and [`FORMAL BRIDGING OF 17-13.md`](../../papers/06-gravitational-constant-from-topology/FORMAL%20BRIDGING%20OF%2017-13.md)) writes it as $(D^2 + 1)/(dD + 1)$, "coupling channels versus structural elements". [Paper VII](../../papers/07-dual-tetrad-topology-field-origin/v7/Dual_Tetrad_Gravity_And_The_Field_Origin.pdf) derives it as *coupling capacity over spatial structure*, Eq. (24): the numerator, $f(0) = k^2 + 1 = 17$, is the Field Origin, where the face channels are absent, leaving the 16 bimetric coupling channels plus the non-degenerate coupling vertex itself; the denominator, $f(-1) = kd + 1 = 13$, is TetB, where each of the $k = 4$ face channels projects onto $d = 3$ spatial dimensions, giving 12 spatial components plus one for non-degeneracy. Paper VII also locks the three values together: $f(0) = \tfrac12\,[f(+1) + f(-1)]$, so 21, 17 and 13 are three equally spaced marks, and none can move without moving the others (Eq. 23). Letter 2 and the [algebraic pipeline](../../papers/algebraic-papers-a-b-c/algebraic_pipeline_of_reality.md) give the same choice its structural reason. The metric is parity-even, so it couples through the $s = 0$ read, the parity-even core, which is 17, not the full $s = +1$ read of 21: the sign representation, which carries the parity-odd $K$, is absent from the Christoffel sector. The TetB read, 13, is the scaffold that carries that coupling. The look-elsewhere test confirms numerically that no other simple prefactor competes.

What remains open is the one-loop factor's reading. [`synthesis_one_loop_G.md`](synthesis_one_loop_G.md) decomposes $\alpha/2\pi$ as $\tfrac{2}{17} \times \tfrac{17\alpha}{4\pi}$, which matches the residual exactly; that decomposition was found after the residual was known, so it is an interpretation still to be derived.

### 4. From read to gradient

Paper VII names the field: the registered state $B^*_\Sigma$, the settled potential $\Phi^*$, with local geometry $\ell(x)$, whose gradients are gravity, lensing and time dilation. It also identifies settlement with established constraint solving. What is missing is the construction: the read defined cell by cell on the lattice, and its continuum limit shown to give $\nabla \cdot (\mu \nabla\Phi) = 4\pi G\rho$, including the factor $k\pi$ and the weighting by $\mu$. Until that limit is taken, "force is the gradient of the registered read" is an interpretation of the equation, not a derivation of it.

### 5. A lattice without a preferred frame

Any discrete picture of spacetime must respect Lorentz invariance, which Fermi observations of GRB 090510 constrain beyond 7.6 Planck energies, and which GW170817 confirms for gravity to about one part in $10^{15}$. The pixelated README argues that propagation in GFD is closure, not motion across a mesh, so there is no grid spacing to feel. Showing formally that the lattice keeps the dispersion relation $\omega = ck$ exact is still to be done.

### 6. Lattice or connection? Settled by Paper VII

Reading 1 says gravity is the lattice; reading 4 says it is the connection. Paper VII (§XI.A) separates the two cleanly. The mesh of *unbound* gravity-field envelopes, TetB chambers empty, is the long-range background: "the stage". *Bound* envelopes, TetB chambers occupied, are matter: "the actors". Gravity is neither the stage nor the actors but the gradients of the registered state between them. The lattice is spacetime, and gravity is its non-uniformity, which is how general relativity separates the metric from its curvature.

### 7. The graviton

In Hassan–Rosen bimetric gravity the interaction splits the gravitational degrees of freedom into a massless spin-2 mode and a massive one. Paper VII identifies the massless mode with the unbound mesh and the massive mode, confined by its own non-linear coupling, with bound envelopes: Wheeler's geons, realised as matter. The light-substrate notes describe the graviton as two stellated octahedra coupled at a face, giving spin 2, and the quantum-gravity folder makes contact with Regge calculus and loop quantum gravity. Paper VII's fixed interaction coefficients, $\beta_n = (1, 0, 16, 0, 1)$, determine the massive mode's mass, so this part of the picture is testable now, through gravitational-wave dispersion. How the quantised theory follows remains open.

---

## What would decide it

- **A derivation of the compounding**, one factor of $\alpha = r_e/\bar\lambda_C$ per level, so that $\alpha^{21}$ follows rather than being stated.
- **The massive graviton.** Paper VII's $\beta_n = (1, 0, 16, 0, 1)$ fixes the bimetric mass spectrum, which gravitational-wave dispersion measurements from LIGO, Virgo and KAGRA constrain directly.
- **An acceleration scale that changes with time.** Paper VII ties $a_0$ to the Hubble rate, so $a_0$ was larger in the past. Rotation curves at redshift $z > 1$, from JWST and Euclid, test this; standard MOND assumes a constant $a_0$.
- **Decoded mass across catalogues.** Orbits follow the total acceleration $g_t$, carried by both chambers, not the TetA share alone, so the test of a rotation curve is the mass it decodes to. The field equations invert exactly, $M_{\text{dec}}(r) = r\,v^4 / \big[G\,(a_0 r + v^2)\big]$, and running every SPARC galaxy through that inverse would compare decoded mass with baryonic mass across 175 galaxies in one pass.
- **A continuum limit** of a cell-by-cell closure read that reproduces the modified Poisson equation, including the factor $4\pi$ and the weighting by $\mu$.
- **A derivation of the one-loop factor**, showing from the structure why the correction is the Schwinger term $\alpha/2\pi$.
- **An observation that separates the readings from plain MOND.** Every reading above reproduces the radial acceleration relation, because they share $\mu(x)$. Something unique to GFD would have to come from the restored torsion sector, which Letter 3 says persists in empty space, unlike Einstein–Cartan torsion. Identifying a measurable consequence of that is the most direct test available.
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
