# The Universe Is Pixelated

*The cube, its Walsh spectrum, and the light cone · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`walsh-hadamard-transform` `boolean-functions` `stellated-octahedron` `digital-physics` `discrete-spacetime` `tetrad` `light-cone` `gravitational-constant`

---

Every image on a screen is made of pixels. Each pixel is a small square that is either lit or not, and the picture exists only in their arrangement. Up close there are no curves at all, only steps. Step back and smooth curves appear.

Mathematics has two ways of building a signal out of simple pieces. Fourier analysis uses smooth waves, sines and cosines, and is the natural language of anything continuous. Walsh analysis uses square waves that take only the values +1 and −1, and is the natural language of anything built from on/off states. Fourier is the language of a violin string. Walsh is the language of a screen.

This folder asks which of the two belongs to the local structure of spacetime. In GFD, that structure is the stellated octahedron sitting inside a cube. The cube is a binary object: its eight corners are the eight three-bit addresses, 000 to 111. Its natural harmonics are therefore Walsh functions, not sine waves. The question is what that means.

![The stellated octahedron inside a cube, with binary corner addresses](stellated_octahedron_in_cube.png)

## A shape with a long history

The stellated octahedron has fascinated geometers for five centuries.

- **The Renaissance.** Luca Pacioli included it in *De Divina Proportione* (1509), illustrated by Leonardo da Vinci, under the name *octocedron elevatum*, the "elevated octahedron." Pacioli described it as 24 equal triangles enclosing an inner octahedron "visible only to the imagination." Wenzel Jamnitzer engraved it again in *Perspectiva Corporum Regularium* (1568). It had already appeared in stone three centuries earlier, carved into the Sahib Ata caravanserai in Anatolia.
- **Kepler.** Johannes Kepler named it the *stella octangula*, the eight-pointed star, in *Harmonices Mundi* (1619). There he introduced stellation, the extension of a polyhedron's faces until they meet again. Kepler had spent his career looking for the geometry beneath the cosmos. In *Mysterium Cosmographicum* (1596) he nested the Platonic solids between the orbits of the planets, and in *De Nive Sexangula* (1611) he asked why every snowflake has six points.

Part of the appeal was Platonic. In the *Timaeus*, Plato assigned his solids to the elements: the tetrahedron to fire, the octahedron to air, the cube to earth. The stellated octahedron holds all three at once. Two tetrahedra interpenetrate, an octahedron sits at their heart where they overlap, and the cube encloses them, its eight corners exactly the eight points of the star. For anyone who believed the world was built from geometry, this was a single figure in which several of the elements locked together.

It is also the simplest possible compound of regular solids: two copies of the most basic polyhedron, related by a reflection through the centre. Letter 1 shows that this is precisely the shape the tetrad of general relativity draws in space.

## The cube is a binary computer

Give each axis of the cube one bit: 0 for one side, 1 for the other. Each corner then has a three-bit address, from 000 to 111. Figure 1 colours them by parity, the number of 1s in the address:

- the four corners with an odd number of 1s (001, 010, 100, 111) form one regular tetrahedron, **TetA**;
- the four with an even number (000, 011, 101, 110) form the other, **TetB**.

**How the Walsh values are produced.** A Walsh function is labelled by an address $a$, just like a corner. Its value at corner $x$ is

$$w_a(x) = (-1)^{\,\mathrm{popcount}(a \,\mathrm{AND}\, x)} .$$

Take the bits that $a$ and $x$ share, count them, and return +1 if the count is even and −1 if it is odd. For example, $w_{011}$ at corner $110$: the shared bit is the middle one, a count of 1, so the value is −1.

Doing this for all eight labels and all eight corners gives an $8 \times 8$ table of ±1 entries, the **Walsh–Hadamard matrix**. It is built from the $2 \times 2$ block $\begin{smallmatrix}1&1\\1&-1\end{smallmatrix}$ by repeated tensor products, $H_8 = H_2 \otimes H_2 \otimes H_2$, one factor per axis (Sylvester 1867). Its rows are mutually orthogonal, and they are the eight harmonics of the cube.

![The eight Walsh functions of the cube](cube_walsh_spectrum.png)

**How many operations?** Your understanding is right about the number, with one adjustment about the inputs. The cube has **3 inputs**, one bit per axis. Those 3 bits give $2^3 = 8$ corners, which are the 8 rows of a truth table. A Boolean operation assigns an output bit to each corner, so there are

$$2^{2^3} = 2^8 = 256$$

distinct operations on the cube. These are all the three-input logic gates there are. (With 8 independent inputs there would be $2^{256}$.) Each of the 256 has a Walsh spectrum of 8 integers, and every spectrum has the same total power: the squares of its 8 values sum to 64 (Parseval's theorem). Sixteen of the 256 are the Walsh functions themselves and their negatives. Every other operation is a mixture of them.

## The stellated octahedron is in the spectrum

Three exact facts tie the shape in Figure 1 to the matrix in Figure 2.

**1. The last Walsh function draws the star.** The highest harmonic, $w_{111}(x) = (-1)^{x_1 + x_2 + x_3}$, is the parity function. It is +1 on every corner of TetB and −1 on every corner of TetA. The split of the cube into two tetrahedra is not an extra construction. It is one row of the Walsh–Hadamard matrix.

**2. The cube's own vibrations split the same way.** Treat the cube's twelve edges as a network and ask for its natural modes, the eigenvectors of the graph. They are exactly the eight Walsh functions, with eigenvalues $3 - 2 \times \text{grade}$, where the grade is the number of 1s in the label: $+3, +1, -1, -3$, with multiplicities $1, 3, 3, 1$.

The cube graph is bipartite: every edge joins a TetA corner to a TetB corner, and no edge stays inside one tetrahedron. Multiplying any mode by the parity function $w_{111}$ turns eigenvalue $\lambda$ into $-\lambda$. Because the cube's frequency labels are themselves cube corners, the frequencies sort into the same two tetrahedra: the even-grade labels (eigenvalues $+3$ and $-1$) are the TetB addresses, and the odd-grade labels (eigenvalues $+1$ and $-3$) are the TetA addresses. The stellated octahedron appears on both sides of the transform.

**3. A tetrahedron transforms into the diagonal.** TetB is a subgroup of the cube under XOR, and TetA is its other half (its coset). The Walsh transform of TetA's indicator has only two nonzero values, at $w_{000}$ and $w_{111}$. Conversely, the transform of the body diagonal $\{000, 111\}$ is nonzero only on the four TetB addresses.

In frequency space, then, a tetrahedron becomes the line from 000 to 111, and that line becomes a tetrahedron. In Paper IX this diagonal is special: it passes through the Field Origin and joins the two **time faces**, TetA's face opposite 111 and TetB's opposite 000. The spectral dual of the stellated octahedron is the axis that carries time.

**And the tetrad is a Hadamard matrix.** Take the $4 \times 4$ Hadamard matrix and drop its first column of 1s. The four rows that remain are

$$(1,1,1),\quad (1,-1,-1),\quad (-1,1,-1),\quad (-1,-1,1),$$

which are exactly the four tetrad directions $v_1, \dots, v_4$ of Letter 1. They sum to zero, the closure condition, and meet at the tetrahedral angle, $\cos\theta = -1/3$. It is a classical result that a regular simplex can be placed on the corners of a cube precisely when a Hadamard matrix of the next order exists. In three dimensions that order is 4. The tetrad of general relativity, written in ±1 form, is a Hadamard matrix.

## The octahedron and the light cone

Letter 1's supplement starts from the light cone. In a frame with signature $(-,+,+,+)$, every light ray through a point corresponds to a direction on a sphere, the celestial sphere $S^2$. The tetrad's four directions are four such directions, chosen so that none is preferred. They are null directions: directions of light.

Now look at the gold octahedron at the centre of Figure 1. It is the region where $|v_i| \le 1$ for all four directions at once, the overlap of TetA and TetB. Its eight faces point to the eight corners of the cube, which are exactly the eight directions $\pm v_1, \dots, \pm v_4$ of the two tetrads. **The octahedron is the solid bounded by the eight null directions.** It is the sphere of light rays, made discrete: eight facets instead of a smooth sphere, one facet for each null direction the frame contains.

GFD's photonic notes take the next step. They propose that **the photon is the stellated octahedron itself**: the whole figure, both chambers, TetA and TetB, coupled through the Field Origin, with the octahedral core where they overlap. The eight null directions that bound the core are the eight points of the star, so the photon's geometry is the geometry of its own directions of travel. On this reading light is the pixel of spacetime, and that gravity is many such pixels organised into a lattice (see [`photonic/`](../photonic/the-pixel-and-the-lattice.md)). The visualisations below were made in that spirit. Eight cones converge on the centre, one along each of the eight null directions, through the faces of the octahedron. The ten-cone version adds a pair along a single axis.

![Convergent vortex visualisations: eight cones converging on the centre through the faces of the octahedron, and the ten-cone variant](convergent_vortex.png)

*Left: the convergent octahedral vortex, eight cones meeting at the Field Origin inside the octahedron. Centre and right: the ten-cone variant inside the stellated octahedron, seen from two angles.*

## Why "pixelated"

The choice between Fourier and Walsh is not a matter of taste. It is set by symmetry.

Sine waves are the natural harmonics of continuous symmetry: a line, a circle, a string that can be shifted by any amount. Walsh functions are the natural harmonics of binary symmetry: a space of switches that can be flipped (Walsh 1923). Engineers learned this in practice. Hadamard transforms were among the first methods for compressing digital images (Pratt, Kane and Andrews 1969), and single-pixel cameras today reconstruct whole images from a sequence of Hadamard patterns (Duarte et al. 2008).

The argument of this folder follows from that:

1. **The local frame is a cube with binary corners.** The tetrad's directions are the corners of a cube (Letter 1), labelled by three bits (Paper IX).
2. **The harmonics of a binary cube are Walsh functions.** This is a theorem: the Walsh functions are the characters of the group of three-bit strings.
3. **The stellated octahedron is built into that spectrum.** It is the parity harmonic, it is the bipartition of the cube's modes, and its transform is the time axis.
4. **The stellated octahedron is built from the eight null directions.** Its eight points lie along them, and its octahedral core is bounded by them. On GFD's reading, the stellated octahedron is the photon.
5. **So, at the scale of the frame, the field is spectrally pixelated.** Its natural basis is a set of on/off patterns, not smooth waves.

Smoothness does not disappear. It emerges at scale, the way a curve emerges from pixels when you step back. The [field closure walk](../field-closure/) is an example inside GFD: binary steps around the cube's eight corners assemble a series that converges to π, the circle recovered from switches.

The idea of a discrete universe has a long lineage in physics: Konrad Zuse's *Rechnender Raum* ("Calculating Space," 1969), John Wheeler's "it from bit" (1990), and the discrete spectra of area and volume in loop quantum gravity (Rovelli and Smolin 1995). GFD's version is specific. The pixel is not a point on a grid but a frame: the cube, its two tetrahedra, and the eight null directions between them.

## G as an operator read

The same habit of thought, build a structured operator and then read it, appears in GFD's derivation of Newton's constant ([`g_from_topology/`](../g_from_topology/g_matrix_synthesis.md)).

**In the spectral kernel** ([`spectral/`](../spectral/spectral_kernel.py)), any Boolean gate is computed in one step. Build the Hadamard matrix $H$ from popcount parity, multiply the gate's coefficient vector by $H$, and read the sign of the result. The operator is fixed by the cube; the gate is a reading of it.

**For G**, GFD builds a graded operator on the $1 + 4 + 16 = 21$ dimensional space of the tetrad equation's scalar, vector and tensor parts:

$$I_s = P_0 + s\,P_1 + P_2, \qquad \mathrm{Tr}(I_s) = 1 + sK + K^2 = f(K,s) \in \{21, 17, 13\} .$$

It then reads it with two standard linear-algebra operations. The trace gives the ratio $17/13$. The determinant identity $\det(\alpha^{I}) = \alpha^{\mathrm{Tr}\,I}$ gives the attenuation $\alpha^{21}$, one factor of the fine-structure constant per coupling level. Together:

$$G = \frac{\mathrm{Tr}(I_0)}{\mathrm{Tr}(I_{-1})}\;\det\!\big(\alpha^{I_{+1}}\big)\;\frac{\hbar c}{m_e^2} = \frac{17}{13}\,\alpha^{21}\,\frac{\hbar c}{m_e^2}.$$

That is $6.6665 \times 10^{-11}$ at tree level, and $6.6742 \times 10^{-11}$ with the one-loop Schwinger factor $1 + \alpha/2\pi$, against the measured $6.6743 \times 10^{-11}$.

The two constructions are built the same way. The Hadamard matrix is a tensor power of one small block, $H_2^{\otimes 3}$. GFD's graded space is a sum of tensor powers of the four-dimensional frame, $V^{\otimes 0} \oplus V^{\otimes 1} \oplus V^{\otimes 2}$. The gradings differ: the cube's Walsh functions grade as $1, 3, 3, 1$ by bit count, while the tetrad's ranks grade as $1, 4, 16$. In both cases, though, the physics is a reading of a ±1-structured operator assembled from the geometry of the frame.

## What is established, and what is proposed

| Statement | Status |
|---|---|
| The Walsh functions are the harmonics of the binary cube; there are 256 three-input operations, each with an 8-value spectrum of total power 64 | Established mathematics |
| The parity harmonic splits the cube into the two tetrahedra; the cube's modes split the same way; a tetrahedron and the body diagonal are Walsh duals | Established mathematics |
| The tetrad directions are Hadamard rows, and the octahedron is bounded by the eight directions of the two tetrads | Established mathematics |
| The tetrad directions are null directions, and the cube is the local frame of spacetime | Derived in Letter 1 and Paper IX |
| $G = (17/13)\,\alpha^{21}\,\hbar c/m_e^2$ as a trace-and-determinant read | GFD derivation, matching measurement to 0.001% at one loop |
| The stellated octahedron is the photon; spacetime is spectrally pixelated at the scale of the frame | GFD proposal |

Every mathematical statement in the first three rows, and the value of G, is checked by [`verify_pixelated.py`](verify_pixelated.py).

**The open question that matters most.** Any discrete picture of spacetime has to respect Lorentz invariance, which has been tested to extraordinary precision. Fermi observations of gamma-ray bursts push any linear energy-dependent delay in the arrival of photons beyond the Planck energy (Vasileiou et al. 2013). A naive grid of points would fail that test. GFD's pixel is not a grid of points: it is a frame attached to every event, built from null directions, and it is Lorentz-covariant by construction. Showing that its Walsh-type structure leaves the propagation of light unchanged at observable energies is the test this proposal has to pass.

## Contents

| File | Contents |
|---|---|
| [`README.md`](README.md) | This overview |
| [`verify_pixelated.py`](verify_pixelated.py) | 26 checks: the Walsh–Hadamard matrix, the stellated octahedron in the spectrum, Hadamard rows as the tetrad, the octahedron's null faces, the 256 operations, and G |
| [`make_figures.py`](make_figures.py) | Generates the cube and spectrum figures |
| [`stellated_octahedron_in_cube.png`](stellated_octahedron_in_cube.png) | Figure 1: the stellated octahedron in the cube, with binary addresses |
| [`cube_walsh_spectrum.png`](cube_walsh_spectrum.png) | Figure 2: the eight Walsh functions of the cube |
| [`convergent_vortex.png`](convergent_vortex.png) | Figure 3: convergent vortex visualisations |

```bash
pip install numpy matplotlib
python verify_pixelated.py     # 26 passed, 0 failed
python make_figures.py         # regenerates Figures 1 and 2
```

## Related work

- **Letter 1**, [*The Coordinate-Space Geometry of the Tetrad Frame*](../../papers/letter-1-tetrad-frame-geometry/): the tetrad's four planes and the two bounded tetrahedra; the supplement derives the frame from the light cone.
- **Paper IX**, [*Complete Field Closure from Stellated Octahedron Topology*](../exploratory/i-ching/Nelson_2026_GFD_Complete_Field_Closure_from_Stellated_Octahedron_Topology.pdf): binary addresses, the parity partition and the time faces.
- [`g_from_topology/`](../g_from_topology/): G as a matrix read.
- [`spectral/`](../spectral/) and [`quantum compute/`](../quantum%20compute/): the Walsh–Hadamard kernel and the oscillator work built on it.
- [`photonic/`](../photonic/): the photon as the stellated octahedron, the pixel of spacetime.
- [`field-closure/`](../field-closure/): the closure walk, and π from binary steps.

---

*A screen shows smooth images built from square pixels. The proposal here is that spacetime may do the same, and that the pixel has been hiding in plain sight inside the tetrad for a century.*

---

## References

- Duarte, M. F. et al. (2008). Single-pixel imaging via compressive sampling. *IEEE Signal Process. Mag.* 25(2), 83.
- Jamnitzer, W. (1568). *Perspectiva Corporum Regularium*. Nuremberg.
- Kepler, J. (1596). *Mysterium Cosmographicum*. Tübingen.
- Kepler, J. (1611). *Strena seu de Nive Sexangula*. Frankfurt.
- Kepler, J. (1619). *Harmonices Mundi*. Linz.
- O'Donnell, R. (2014). *Analysis of Boolean Functions*. Cambridge University Press.
- Pacioli, L. (1509). *De Divina Proportione*, illustrated by Leonardo da Vinci. Venice.
- Pratt, W. K., Kane, J. and Andrews, H. C. (1969). Hadamard transform image coding. *Proc. IEEE* 57, 58.
- Rovelli, C. and Smolin, L. (1995). Discreteness of area and volume in quantum gravity. *Nucl. Phys. B* 442, 593.
- Sylvester, J. J. (1867). Thoughts on inverse orthogonal matrices. *Phil. Mag.* 34, 461.
- Vasileiou, V. et al. (2013). Constraints on Lorentz invariance violation from Fermi-LAT observations of gamma-ray bursts. *Phys. Rev. D* 87, 122001.
- Walsh, J. L. (1923). A closed set of normal orthogonal functions. *Amer. J. Math.* 45, 5.
- Wheeler, J. A. (1990). Information, physics, quantum: the search for links. In W. Zurek (ed.), *Complexity, Entropy, and the Physics of Information*. Addison-Wesley.
- Zuse, K. (1969). *Rechnender Raum*. Vieweg.
- History of the stellated octahedron: [Wikipedia, "Stellated octahedron"](https://en.wikipedia.org/wiki/Stellated_octahedron); [Matemáticas Visuales, "Stella octangula (adapted from Leonardo da Vinci)"](https://www.matematicasvisuales.com/english/html/history/leonardo/stellatedoctahedron.html).
