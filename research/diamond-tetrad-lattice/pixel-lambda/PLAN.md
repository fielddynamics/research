# The Pixel as a Λ System: Plan

*Field Dynamics Research, research folder, 2026-11-15. Status: plan, with criteria fixed before any script ran. Follows [`../self-consistent/`](../self-consistent/RESULTS.md).*

## The question

The self-consistent study found that μ comes out of a Λ system: the TetA end and the TetB end of a bond, both coupled to a common Field Origin state, with squared couplings in the ratio $g : a_0$.

The pixel has exactly this shape. The Field Origin at the cube's centre connects through 8 legs to 4 TetA corners and 4 TetB corners. This study asks:
- does the pixel, as a Λ system, give μ?
- what are its other states?
- does μ survive when pixels are joined into the cubic tiling, where each corner is shared by 8 pixels (result 7)?

## Model

Corner states at energy 0, the Field Origin at energy $\Delta$. Coupling $-t_A$ along each TetA leg and $-t_B$ along each TetB leg. "TetA share" means the fraction of the bonding energy, $\langle H_{\rm legs}\rangle$ of the lowest state, carried by the TetA legs. For an isolated pixel this equals the state's weight on the TetA corners. In the tiling, a corner is TetA for some pixels and TetB for others, so only the bonding-energy share is defined.

## Honesty note

These items were worked out while designing the plan, so they are expected to pass and are recorded as checks. The informative content is Q3 and Q4: whether μ survives the tiling, and which coupling law it then needs.

## The tests

**Q1. The isolated pixel is a Λ system.**
- *Claim:* the lowest state is the bright state, with TetA share exactly $t_A^2/(t_A^2 + t_B^2)$ for every $\Delta$ (by weight and by bonding energy). Seven states are dark, at zero energy and decoupled from the Field Origin. With $t_A^2 : t_B^2 = g : a_0$, the share is $\mu(g/a_0)$.
- *Pass:* exact (symbolic).

**Q2. The dark states, in the cube's Walsh basis.**
- *Claim:* the Field Origin couples only to the Walsh pair $\{1, xyz\}$ of the 8 corner functions. The other six, $x, y, z, xy, yz, zx$, are dark for any $t_A, t_B$, by symmetry. The seventh dark state is the $\{1, xyz\}$ combination orthogonal to the bright state. At the ring, $t_A = t_B$, the bright state is $1$ and that dark state is $xyz$, the parity character.
- *Pass:* exact.

**Q3. Joined pixels: the cubic tiling with shared corners.**
- *Setup:* a simple-cubic lattice of pixels, one Field Origin and one corner per cell. Each centre couples to its 8 corners, along 4 TetA legs ($t_A$) and 4 TetB legs ($t_B$) of that pixel. Bloch Hamiltonian $H(k) = \begin{pmatrix} \Delta & -F \\ -F^* & 0 \end{pmatrix}$, with $F(k) = t_A\sum_{\rm TetA} e^{ik\cdot v} + t_B\sum_{\rm TetB} e^{ik\cdot v}$.
- *Claim:* the ground state is at $k = 0$, and its TetA share is $t_A/(t_A + t_B)$: linear in the couplings, not squared. So μ needs $t_A : t_B = g : a_0$ in the tiling, against $t_A^2 : t_B^2 = g : a_0$ for an isolated pixel.
- *Pass:* exact at $k = 0$; numerically, the $k = 0$ state is the global minimum over the zone (grid of $40^3$) for several $t_A/t_B$ and $\Delta$.

**Q4. Which coupling law goes with which picture.**
- *Claim:*
  - A coupling amplitude proportional to the field ($t_A \propto g$, $t_B \propto a_0$; linear response) gives μ exactly in the tiling. For an isolated pixel it gives $g^2/(g^2 + a_0^2)$, which fails Tully–Fisher (S5's $n = 2$).
  - A squared coupling proportional to the field ($t_A^2 \propto g$) gives μ for an isolated pixel. In the tiling it gives $\sqrt x/(1 + \sqrt x)$, which fails Tully–Fisher (S5's $n = \tfrac12$).
- *Pass:* exact, with the deep-field exponents as in S5.
- *Means:* each coupling law pairs with exactly one picture. If the tiling is the right picture (corners shared, as the cubic lattice has them), then the remaining assumption becomes the most ordinary one available: the TetA coupling amplitude is proportional to the local field.

## What would count as success

Q1–Q2 make the Λ system literally the pixel, with its dark states named by the Walsh basis. Q3–Q4 settle whether μ survives the tiling, and which coupling law the cubic lattice requires.
