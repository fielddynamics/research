# The Pixel as a Λ System: Results

*Run 2026-11-15 against [`PLAN.md`](PLAN.md), committed before any script ran. Outputs are in [`output/`](output/).*

## Answer in brief

**The pixel is a Λ system.** The Field Origin at the cube's centre couples through the 8 legs to 4 TetA and 4 TetB corners. That gives one bright state, whose TetA share is μ, and seven dark states, named exactly by the cube's Walsh functions.

**μ survives joining the pixels into the cubic tiling, but with a different coupling law.**
- **Isolated pixel:** μ needs the squared couplings in the ratio $g : a_0$.
- **Tiling with shared corners:** μ needs the coupling amplitudes themselves in the ratio $g : a_0$, that is, a TetA coupling proportional to the local field.

Each law gives Tully–Fisher in exactly one picture.

| Test | Verdict | Result |
|---|---|---|
| Q1 isolated pixel | **PASS** (expected) | The lowest state is the bright state, $E = (\Delta - \sqrt{\Delta^2 + 16(t_A^2 + t_B^2)})/2$, with TetA share exactly $t_A^2/(t_A^2 + t_B^2)$ by weight and by leg energy, for every $\Delta$. The Hamiltonian has rank 2, so seven states are dark at $E = 0$. With $t_A^2 : t_B^2 = g : a_0$ the share is $\mu(g/a_0)$. |
| Q2 dark states and Walsh | **PASS** (expected) | The Field Origin couples only to the Walsh pair $\{1, xyz\}$, with couplings $-4(t_A + t_B)$ and $-4(t_A - t_B)$. The six functions $x, y, z, xy, yz, xz$ are dark for any couplings. The seventh dark state is $\tfrac12(t_B - t_A)\,1 + \tfrac12(t_B + t_A)\,xyz$. At the ring, $t_A = t_B$, the bright state is $1$ and the seventh dark state is $xyz$, the parity character. |
| Q3 the tiling | **PASS** (expected) | In the simple-cubic tiling, with one Field Origin and one shared corner per cell, the ground state is at $k = 0$; this was confirmed as the global minimum over a $40^3$ zone grid for four sets of couplings. Its TetA leg-energy share is $t_A/(t_A + t_B)$, linear in the couplings. |
| Q4 coupling law against picture | **PASS** (expected) | *Amplitude ∝ field* ($t_A : t_B = g : a_0$): μ in the tiling; $x^2/(1+x^2)$ for an isolated pixel, giving $g \propto g_N^{1/3}$, no Tully–Fisher. *Squared ∝ field* ($t_A^2 : t_B^2 = g : a_0$): μ for an isolated pixel; $\sqrt x/(1 + \sqrt x)$ in the tiling, giving $g \propto g_N^{2/3}$, no Tully–Fisher. |

## What this adds

1. **The Λ system is the pixel itself.** No extra state is needed: the Field Origin is the cube's centre, and the two ends are the TetA and TetB corners.
2. **The dark states are the cube's Walsh functions.** Six are dark by symmetry, $x, y, z, xy, yz, xz$. The Field Origin couples only through $\{1, xyz\}$, and $xyz$ is the parity character that separates TetA from TetB. At the ring, the dark state is that character itself. This links the self-consistent result to T13, where the same $\{1, xyz\}$ pair formed the A₁ block.
3. **The remaining assumption depends on the picture, and in the cubic tiling it is the ordinary one.** With corners shared, as the cubic lattice has them, μ needs only that the TetA coupling amplitude be proportional to the local field while the TetB coupling stays at $a_0$. Linear response is the most ordinary coupling there is. The squared law of the self-consistent study belongs to isolated pixels.

## What is still assumed or open

- **Which picture is GFD's.** The two pictures differ in what a corner is. In the tiling, a corner is one state shared by the 8 cubes that meet there. In the isolated picture, each pixel has its own 8 corner states, even though corners coincide geometrically. The framework has to decide; the algebra only says which coupling law goes with each.
- **Why the TetB coupling is fixed at $a_0$.** Unchanged: this is the open question in either picture.
- **The share measure.** In the tiling the TetA share is defined by leg energy, because a shared corner is TetA for some pixels and TetB for others. For an isolated pixel, leg energy and weight agree (Q1).

## Notes on the run

Q1 and Q2 first failed on bugs in the test code, not on the claims, and were fixed before the verdicts above. Q1 compared sympy numbers inside a Python sum. Q2 had the sign of the expected dark state wrong: at the ring it is $+t\,xyz$. No criterion changed.
