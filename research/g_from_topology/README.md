# G from Topology

*Newton's constant as a read of the stellated octahedron · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`gravitational-constant` `fine-structure-constant` `hierarchy-problem` `coupling-polynomial` `stellated-octahedron` `gravity`

---

Gravity is weaker than electromagnetism by a factor of about $10^{43}$, and Newton's constant has been measured for more than two centuries without any theory predicting its value. This folder derives it from the same coupling polynomial that runs through the rest of the archive:

$$G = \frac{17}{13}\,\alpha^{21}\,\frac{\hbar c}{m_e^2}\left(1 + \frac{\alpha}{2\pi}\right).$$

- **21** $= 1 + K + K^2$ is the depth of the read: a scalar, the four legs of the tetrad and their sixteen couplings. Each level costs one factor of the fine-structure constant $\alpha$.
- **17/13** is the parity-even core that the metric couples through, $K^2 + 1 = 17$, over the TetB scaffold that carries it, $DK + 1 = 13$: coupling capacity over spatial structure (Paper VI, §8.3; Paper VII, Eq. 24).
- **$\hbar c/m_e^2$** sets the scale, through the electron, the smallest closed pattern.
- **$1 + \alpha/2\pi$** is the one-loop correction, the same Schwinger term that appears in the electron's magnetic moment.

At tree level the formula is within 0.12% of the measured value. With the one-loop factor it is within 12 parts per million, inside the 22 ppm uncertainty of G itself. Among 1,953 alternatives of the same form, $(p/q)\,\alpha^n$ with $p, q \le 21$ and $n = 18$–24, it is the only one that lands in either window.

The hierarchy follows in one line: electromagnetism couples through one level and gravity through twenty-one, so the ratio is $\alpha^{20} \approx 10^{-43}$.

## Reading order

1. [`g_matrix_synthesis.md`](g_matrix_synthesis.md), *G as a Matrix Read*. The derivation: the graded operator $I_s = P_0 + sP_1 + P_2$ on blocks of size 1, 4 and 16, its three traces 21, 17 and 13, and the identity $\det(\alpha^{I}) = \alpha^{\mathrm{Tr}\,I}$.
2. [`synthesis_one_loop_G.md`](synthesis_one_loop_G.md), *The One-Loop Correction to G*. The residual at tree level matches $\alpha/2\pi$, and a structural reading of that factor.
3. [`read_sweep_synthesis.md`](read_sweep_synthesis.md), *The Read Sweep*. A physical picture of what does the reading: 64 sectors, three harmonic bands of 1, 4 and 16, and light, gravity and matter as three patterns of one process.
4. [`what_is_gravity.md`](what_is_gravity.md), *What Is Gravity?* An open question. It sets the archive's five readings of gravity side by side (the lattice, the read sweep, closure settling, the connection and the pixel computing), shows how they fit into one synthesis, and lists what the archive itself names as open.

## What is derived, and what is assumed

| Step | Status |
|---|---|
| The traces 21, 17, 13 of the graded operator, and $\det(\alpha^{I}) = \alpha^{\mathrm{Tr}\,I}$ | Exact linear algebra |
| The value of G at tree level (0.12%) and one loop (12 ppm) | Matches measurement |
| Uniqueness of $17/13 \cdot \alpha^{21}$ among simple alternatives | Computed by [`look_elsewhere_G.py`](look_elsewhere_G.py) |
| Each coupling level attenuates by one factor of $\alpha$ | The single physical assumption: the frame is built from null directions, so its coupling is photonic |
| The prefactor $17/13 = (K^2+1)/(DK+1)$: the parity-even core the metric couples through, over the TetB scaffold | Derived in Paper VI §8.3 ([formal bridging note](../../papers/06-gravitational-constant-from-topology/FORMAL%20BRIDGING%20OF%2017-13.md)) and [Paper VII](../../papers/07-dual-tetrad-topology-field-origin/v7/Dual_Tetrad_Gravity_And_The_Field_Origin.pdf), Eq. (24); confirmed numerically by the look-elsewhere test |
| The decomposition of $\alpha/2\pi$ as $\tfrac{2}{17} \times \tfrac{17\alpha}{4\pi}$ | An interpretation of the residual |

## Running

```bash
python look_elsewhere_G.py
```

Standard library only. The value of G is also checked in [`universe-is-pixelated/verify_pixelated.py`](../universe-is-pixelated/verify_pixelated.py).

## Contents

| File | Contents |
|---|---|
| [`g_matrix_synthesis.md`](g_matrix_synthesis.md) | The derivation of G as three reads of one graded operator |
| [`synthesis_one_loop_G.md`](synthesis_one_loop_G.md) | The one-loop correction and its structural reading |
| [`read_sweep_synthesis.md`](read_sweep_synthesis.md) | The read sweep: what does the reading |
| [`what_is_gravity.md`](what_is_gravity.md) | What gravity is, framed as an open question |
| [`look_elsewhere_G.py`](look_elsewhere_G.py) | The look-elsewhere test for the prefactor and exponent |
| [`g_three_sierpinski_blocks.html`](g_three_sierpinski_blocks.html) | Diagram of G as three Sierpiński blocks, 1 + 4 + 16 |
| [`photonic_circle.jsx`](photonic_circle.jsx) | Interactive React component: the 64-sector read circle |

`g_matrix_synthesis.md`, `read_sweep_synthesis.md` and `photonic_circle.jsx` also appear, identical, in [`photonic/`](../photonic/).

## Related

- [`universe-is-pixelated/`](../universe-is-pixelated/): the cube as a Boolean computer, and G as an operator read on Walsh–Hadamard blocks
- [Paper VI](../../papers/06-gravitational-constant-from-topology/): *Deriving the Gravitational Constant from Spacetime Topology*
- [`docs/02-gravitation/04-g-from-topology.md`](../../docs/02-gravitation/04-g-from-topology.md): the documentation page
