# Test Results

*Run 2026-11-14 against the criteria fixed in [`../TEST_PLAN.md`](../TEST_PLAN.md). Failures are kept. Where a diagnostic was run after a failure, it is listed separately and does not change the verdict. Each test's full output is in [`output/`](output/).*

**Tally:** 14 pass (3 of them reported rather than judged), 5 fail (one, T06, predicted to fail), 1 not run (T15, not informative as designed).

| Test | Verdict | Key result |
|---|---|---|
| T01 isotropy | **PASS** | $\sum_a v_av_a^T = 4I$; the $O(k^2)$ term is exactly isotropic for diamond (and numerically for simple cubic and lonsdaleite). $k^4$ anisotropy (max−min)/mean: diamond 0.74, simple cubic 1.11, lonsdaleite 0.42. Diamond's exact $k^4$ term: $-(\sum k_i^4 + 6\sum_{i<j}k_i^2k_j^2)/6$. |
| T02 Green's function | **FAIL** | Shell spread 1.4% at $5d$ and 1.7% at $0.3L$ (criterion 1%). The $1/r$ law itself holds: fitted $A\pi = 1.0001$ (continuum $1/\pi$), shell means within $10^{-4}$. *Diagnostic:* in a box twice as large, the outer spread falls to 0.1%, so it was the box; the inner 1.4% at $5d$ is unchanged, so it is lattice graininess. Beyond $10d$ the spread is below 0.3%. |
| T03 nonlinear field | **FAIL** | Worst shell-mean error 2.0% at $5$–$7d$ (criterion 1% for $r > 5d$); deep field $v^4/[GMa_0(1+x)]$ off by 1.8%. *Diagnostic:* for $r \ge 8d$, within 0.5% across $x = 10^{-2}$ to $10^{2}$, and $v^4$ within 0.5%; doubling the box does not change the inner errors. The lattice with $\mu(x)$ on every bond reproduces $g_N = g^2/(g + a_0)$ and $v^4 \to GMa_0$ beyond about 8 bond lengths. |
| T04 stacking | **FAIL** | Linear: anisotropy along the stacking axis, lonsdaleite +0.10%, diamond +0.02% (criterion: lonsdaleite above 1%, diamond below 0.1%). Nonlinear (transition window): −0.70% and −0.76%, the same for both (the box). The field does not tell the two stackings apart beyond $10d$. |
| T05 Hellmann–Feynman | **PASS** | $\partial E/\partial V_3 = -\alpha_p$, $\partial E/\partial V_2 = -\alpha_c$, $\mu = (1 - \partial E/\partial V_3)/2$, exactly. |
| T06 bond vs AQUAL energy | **FAIL** (predicted) | Under the dictionary the bond energy is $-(g + a_0)/2$, so $dE/dg$ is constant, while the field equation needs $\mu g = g^2/(g + a_0)$, whose integral is $a_0^2F/2$. The dictionary fixes the shares, not the energy. |
| T07 two routes | **PASS** | Detailed balance's driving intensity $x$ is the bond's odds under $V_3/V_2 = (x-1)/(2\sqrt x)$; the Boltzmann gap is $\ln x = 2\,\mathrm{asinh}(V_3/V_2)$; exchange is $u \to -u$ in the bond and $\epsilon \to 1 - \epsilon$ in detailed balance. |
| T08 TetB as covalency | **PASS** | $(1-\mu)g = \tfrac12\alpha_c\sqrt{ga_0}$ exactly; $\approx g$ for $g \ll a_0$, $\to a_0$ for $g \gg a_0$. |
| T09 sp³ crystal | **FAIL** | At $V_1/V_2 = 0.25$ the crystal's TetA share differs from the single-bond $\mu(x)$ by up to 7.9% (near $x \approx 0.1$–$0.3$; criterion 2%). Within 2% only for $V_1/V_2 \lesssim 0.12$. *Diagnostic:* the crystal keeps the exchange symmetry exactly, share$(1/x) = 1 -$ share$(x)$; the deviation is zero at $x = 1$, grows as $V_1^2$, and pulls the share toward ½. |
| T10 Bloch shares | **PASS** (reported) | $f(0) = 4 = K$, band edge $\pm\sqrt{V_3^2 + 16t^2}$, exactly. In the s-band model the zone-mean share is pushed toward the ends (e.g. $x_\Gamma = 0.5$: $\mu = 0.333$, mean share 0.177), because $\lvert f\rvert < 4$ off $\Gamma$ and vanishes on the X–W lines. |
| T11 parity as polarity reversal | **PASS** | $\Sigma H(k;V_3)\Sigma = -H(k;-V_3)$; the bond-midpoint inversion maps $H(k;V_3)$ to $H(k;-V_3)$; symmetric spectrum at $V_3 = 0$. |
| T12 symmetry breaking | **PASS** | 48 symmetries at $V_3 = 0$ (diamond), 24 at $V_3 \ne 0$ (zincblende); the kept ones are $T_d$; the lost 24 are exactly the sublattice-swapping coset $-I\cdot T_d$. |
| T13 Walsh–Hadamard and the 64 entries | **PASS** | At $\Gamma$ the cube's 8×8 Walsh basis block-diagonalises the 8×8 (64-entry) sp³ cell Hamiltonian into four 2×2 blocks: $\{1, xyz\}$ (A₁) and $\{x, yz\}, \{y, xz\}, \{z, xy\}$ (T₂), each a TetA–TetB bond problem with the polarity off the diagonal. Not block-diagonal at X or L. |
| T14 pixel cosets | **PASS** | 48 symmetries of the stellated octahedron, 24 of one tetrahedron; the other 24 swap TetA and TetB and are $-I$ times tetrahedral ones. |
| T15 rotation and torsion | **NOT RUN** | Not informative as designed: on the lattice a bond's TetA and TetB readings are the same bond traversed both ways, so "equal and opposite" holds by definition. A real test needs a lattice tetrad and spin connection. |
| T16 hourglass on the net | **PASS** | Bond-midpoint inversion keeps the swirl, reverses the through-flow and reverses the discrete helicity ($\lvert H' + H\rvert/\lvert H\rvert = 3\times10^{-16}$). Structural: the inversion is a lattice symmetry. |
| T17 diamond photonic gap | **PASS** | Gap between bands 2 and 3 of 10.79% (benchmark 10.62%), converged to 0.02 points from 800 to 1600 plane waves. |
| T18 diamond vs other nets | **PASS** | At filling 0.496, $\epsilon = 11.56$: diamond 10.78%, lonsdaleite 1.14% (bands 4–5), fcc and simple cubic none. |
| T19 one root vs full pixel | **PASS** (reported) | Rods along the pixel legs in the cubic tiling: no complete gap at any radius 0.05–0.3, for one root's legs or for all eight (the one-root case only touches, below 0.0005%, at $r = 0.15$–$0.2$). |
| T20 length scale | **PASS** (reported) | $d \propto (ga_0)^{-1/4}$ exactly. A number needs the energy-per-acceleration constant $\kappa$, which the framework does not supply; with $\kappa = m_er_e$, $d(a_0) = \sqrt{3.22\,a_{\rm Bohr}\,c^2/a_0} \approx 3.6\times10^8$ m. No match is claimed. |

## What the run settles

1. **The lattice can carry GFD's field.** With $\mu(x)$ on every bond, the diamond net reproduces the spherical field equation and $v^4 \to GMa_0$ to within 0.5%, beyond about 8 bond lengths (T03 diagnostic), on an isotropic, Newtonian base (T01, T02). The fixed criteria failed only because they began at 5 bond lengths, where the lattice's graininess is 1–2%.
2. **The bond reading is exact for one bond and approximate for a crystal.** The TetA–TetB bond's algebra is $\mu(x)$, with exchange as parity (T05, T07, T08, T11, T12). In a crystal, coupling between bonds on one atom moves the share by order $(V_1/V_2)^2$ but keeps the exchange symmetry exactly (T09).
3. **The energy is still open.** The dictionary of result 9 gives the shares but not the field's energy (T06), and its absolute scale needs a constant the framework does not yet have (T20).
4. **Stacking matters for light, not for the field.** Diamond's photonic gap is roughly ten times lonsdaleite's (T18), but the two stackings give the same field beyond 10 bond lengths (T04). The cubic tiling's own leg structures, with two interlocking diamond nets, have no gap (T19).
5. **The 64 entries have a clean structure at Γ.** The Walsh–Hadamard basis splits the cell Hamiltonian into four TetA–TetB bonds (T13). This is a symmetry result; it does not by itself identify the 64 field-closure states.

## Corrections made during the run

These were bugs in the test code, fixed before the verdicts above; no criterion was changed.

- **Lonsdaleite basis:** the first version used fractional positions for a 120° cell in a 60° cell; caught by a bond-count check (`lattice.py`).
- **T03 deep-field measurement:** averaged $g$ over a wide shell and multiplied by its middle radius; replaced by a site-by-site $(gr)^2$.
- **T06 side check:** compared the AQUAL integral without allowing for an integration constant.
- **T12:** tried only two fixed centres, missing the nonsymmorphic operations (30 instead of 48); now tries every translation.
- **T18:** the hexagonal K point was wrong for a 60° basis; caught by a magnitude check.
- **T17 reference:** the plan named Ho, Chan and Soukoulis (1990), but their gap value for a fully specified structure was not retrieved, so the benchmark is the MPB documentation's diamond lattice of spheres (ε 11.56, r = 0.25a), the same structure, 10.62%.
- **T20 citation:** η = 3.22 is from Harrison's 1999 universal parameters, not the 1980 set.
