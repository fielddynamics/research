# Pushing the Pixel Λ System Further: Plan

*Field Dynamics Research, research folder, 2026-11-15. Status: plan, with criteria fixed before any script ran. Follows [`../pixel-lambda/`](../pixel-lambda/RESULTS.md).*

## The questions

The pixel is a Λ system. With shared corners (the cubic tiling), μ needs coupling amplitudes in the ratio $t_A : t_B = g : a_0$; with each pixel owning its corners, it needs $t_A^2 : t_B^2 = g : a_0$. Two things are open: which picture is GFD's, and why the TetB coupling is fixed at $a_0$. This study asks three questions.
- Can the energies tell TetA from TetB? If not, what can? This is the Gram-matrix proof's root-blind against root-resolving split, asked of the pixel.
- How does the TetA/TetB asymmetry appear in the tiling's waves?
- Does the repo's own horizon reading of $a_0$ explain the fixed TetB coupling? The repo takes $a_0 = cH/2\pi$ from horizon thermodynamics ([`GFD_COLES_NOTES.md`](../../../GFD_COLES_NOTES.md), [`EINSTEIN_TETA_PARTITION.md`](../../../EINSTEIN_TETA_PARTITION.md), [`research/g_from_topology/`](../../g_from_topology/)).

## Honesty note

R1 and R2 were derived while designing, so they are expected to pass. R3 is a check of a stated reading, and its outcome, including the factor of $2\pi$, is reported whatever it is.

## The tests

**R1. Energies are blind to the root; phases are not.**
- *Claim:*
  - For the isolated pixel, every energy depends on $t_A, t_B$ only through $t_A^2 + t_B^2$.
  - In the tiling, swapping $t_A \leftrightarrow t_B$ (exchange) leaves every band energy $E_\pm(k)$ unchanged exactly, and sends $F(k) \to F(k)^*$: it conjugates the Bloch phase.
  - So no energy measures which root carries more of the coupling; the eigenvector's phase does. This is the pixel's version of the Gram-matrix proof's split: the metric is blind to the root, the frame is not.
- *Pass:* exact.

**R2. Where the asymmetry appears in the tiling's waves.**
- *Claim:* $F(k) = (t_A + t_B)\,(4 - k^2/2 + O(k^4)) - \tfrac{i}{2}(t_A - t_B)\,k_xk_yk_z + O(k^5)$. So the only odd term at leading order is the parity character $k_xk_yk_z$, the $xyz$ Walsh function in momentum space, with coefficient $\propto t_A - t_B$. The ground band's phase is $\arg F = -(\sigma/8)\,k_xk_yk_z + O(k^5)$, with $\sigma = (t_A - t_B)/(t_A + t_B) = 2\mu - 1$, which with the tiling law is $(x-1)/(x+1)$.
- *Consequence:* this phase vanishes at the ring ($x = 1$, Letter 3's white ring), has opposite signs inside and outside it, and flips under exchange and under parity ($k \to -k$).
- *Pass:* exact series to $O(k^4)$ in the even part and $O(k^3)$ in the odd part.

**R3. The horizon reading of the coupling law.**
- *Setup:* in the tiling picture, take the coupling amplitudes proportional to temperatures. TetA: the Unruh temperature of the local acceleration, $T_U = \hbar g/(2\pi c k_B)$. TetB: the Gibbons–Hawking temperature of the cosmic horizon, $T_{GH} = \hbar H/(2\pi k_B)$.
- *Report:*
  1. What $x = t_A/t_B$ this gives, and so what $a_0$.
  2. Whether the equality $T_U = T_{GH}$ gives $a = cH$ or $cH/2\pi$, since the repo states $a_0 = cH/2\pi$ from that equality.
  3. The same in the isolated picture (squares).
  4. Numbers for $H_0 = 70$ km/s/Mpc against $a_0 = 1.2\times10^{-10}$ m/s².
- *Pass:* reported, not judged. No normalisation is adjusted to make a match.

## What would count as progress

R1 and R2 show where the root lives in the pixel lattice: not in any energy, but in a phase with the $xyz$ character that changes sign at the ring. R3 says whether the horizon temperatures supply the fixed TetB coupling with the right form, and states plainly any factor that is left over.
