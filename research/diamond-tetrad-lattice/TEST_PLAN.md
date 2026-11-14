# Test Plan: Taking the Pixel Lattice Further

*Field Dynamics Research, research folder, 2026-11-14. Status: plan, written before any test is run. Each test's pass criterion is fixed here; a result that misses it is recorded as a failure, not re-tuned.*

The note ([`README.md`](README.md)) establishes that:
- the tetrad's roots tile as one stellated octahedron per cube;
- their legs form diamond nets;
- the sp³ hybrids are the bordered Hadamard matrix;
- a bond between a TetA site and a TetB site has exactly the algebra of $\mu(x)$.

These 20 tests ask whether the lattice can carry a field the way GFD needs, whether the bond reading survives beyond a single bond, and whether the photonic claim holds up.

**Rules**
- **Criteria are fixed in advance.** Each test states its pass criterion here and is reported as pass or fail against it.
- **One script per test,** `tests/tNN_name.py`, printing its own verdict, so that each can be rerun alone.
- **Exact where possible.** Use exact algebra (sympy) where the statement is exact. Use numerics with a stated tolerance otherwise.
- **No tuning.** Free parameters are named in the test and are not adjusted after seeing the result.
- **Readings stay readings.** A pass says the lattice *can* do something. It does not by itself say the vacuum *is* this lattice.

---

## A. Can the lattice carry a field?

A field theory on the lattice needs isotropy, a Newtonian limit, and the right nonlinearity. These come first, because if they fail, the rest is decoration.

**T01. Isotropy from the tight frame.**
- *Question:* does the diamond net give an isotropic Laplacian at long wavelength?
- *Method:* exact. Show $\sum_a v_a v_a^{T} = 4I_3$ for the TetA legs (a tight frame), so the $O(k^2)$ term of the lattice Laplacian is $\propto k^2$. Then compute the $O(k^4)$ anisotropy of the diamond Laplacian against simple cubic and lonsdaleite.
- *Pass:* $O(k^2)$ term exactly isotropic. Report the $k^4$ anisotropy coefficients for all three lattices.
- *Means:* a fail rules the diamond net out as a field carrier. The $k^4$ numbers tell how far below the lattice scale anisotropy would be visible.

**T02. Newtonian limit of the lattice Green's function.**
- *Question:* does a point source on the diamond net give $1/r$?
- *Method:* numerical. Solve the discrete Poisson equation for a unit source on a diamond net of at least $40^3$ conventional cells, with Dirichlet boundary, and fit $\phi(r) = A/r + B$ over shells.
- *Pass:* relative deviation from $A/r + B$ below 1% for $5 \le r/d \le 0.3\,L$ ($d$ the bond length), with no direction dependence above 1% on a shell.
- *Means:* a pass gives the Newtonian regime (the TetA-only, GR-like limit) on the lattice.

**T03. Nonlinear lattice field with the bond share on every bond.**
- *Question:* if each bond carries share $\mu(x)$ with local $x = |\nabla\phi|/a_0$, does a point mass give the spherical field equation $g_N = g^2/(g + a_0)$?
- *Method:* numerical. Solve $\nabla\cdot[\mu(|\nabla\phi|/a_0)\nabla\phi] = 4\pi G\rho$ on the diamond net, discretised bond by bond, by Newton iteration. Compare the radial $g(r)$ with the analytic quadratic.
- *Pass:* agreement within 1% for $r > 5d$, across $g/a_0$ from $10^{-2}$ to $10^{2}$. In the deep field, $v^4 \to G M a_0$ within 1%.
- *Means:* the central test. A pass shows the lattice plus the bond share reproduces GFD's spherical field equation and flat rotation curves. A fail locates where the discrete picture and the continuum law part.

**T04. Stacking sensitivity: diamond against lonsdaleite.**
- *Question:* does the parity root's choice of diamond matter physically?
- *Method:* repeat T02 and T03 on lonsdaleite, the stacking with the same Gram matrix (result 6).
- *Pass (diamond singled out):* lonsdaleite shows anisotropy above 1% along its hexagonal axis where diamond shows none above 0.1%.
- *Means:* a pass says the frame's choice, invisible to the metric, has an observable consequence on the lattice. A fail says the two stackings are equivalent at field level.

## B. Does the bond reading survive beyond one bond?

Result 9 is a single bond. These tests ask whether the share is still $\mu(x)$ when bonds are coupled into a crystal, and whether it is variationally consistent.

**T05. Hellmann–Feynman responses.**
- *Question:* are polarity and covalency the bond energy's responses, as $\mu = dF/dy$ is in AQUAL?
- *Method:* exact. With $E = -\sqrt{V_2^2 + V_3^2}$, check $\partial E/\partial V_3 = -\alpha_p$ and $\partial E/\partial V_2 = -\alpha_c$, so $\mu = (1 - \partial E/\partial V_3)/2$.
- *Pass:* exact identities.
- *Means:* writes $\mu$ as a derivative of an energy, the form a variational theory needs. It sets up T06.

**T06. Bond energy against the AQUAL energy.**
- *Question:* under the dictionary of result 9 ($V_3 = (g - a_0)/2$, $V_2 = \sqrt{g a_0}$), does the summed bond energy match the AQUAL Lagrangian $a_0^2 F(y)$ for $\mu = x/(1+x)$?
- *Method:* exact. The bond energy under the dictionary is $-(g + a_0)/2$, linear in $g$. Compare with $F(y) = y - 2\sqrt y + 2\ln(1 + \sqrt y)$, $y = x^2$.
- *Pass:* they agree up to terms that do not change the field equation.
- *Means:* the expected outcome is a fail, since one is linear and one is not. That is informative: it says the dictionary of result 9 fixes the shares but not the energy, so the energy must come from somewhere else. It guards against over-reading result 9.

**T07. Two routes to $\mu$.**
- *Question:* how does the quantum route (bond amplitudes, $\ln x = 2\,\mathrm{asinh}(V_3/V_2)$) relate to the repo's detailed-balance route (Boltzmann weights with gap $\ln x$)?
- *Method:* exact. Derive the map between the two "energies". Check it against [`supplementary_equilibrium_route.tex`](../../papers/letter-constitutive-law-tetrad-geometry/Supplementary/supplementary_equilibrium_route.tex).
- *Pass:* an explicit map exists under which both give the same $\mu(x)$ and the same exchange.
- *Means:* if both routes agree, $\mu$ has one meaning (a two-end share) reached two ways.

**T08. The TetB field as covalency.**
- *Question:* is the TetB part of the field, $(1-\mu)g$, the bond's covalent part?
- *Method:* exact. Check $(1-\mu)g = \tfrac12 \alpha_c\sqrt{g a_0}$, and its limits: $\approx g$ for $g \ll a_0$ and $\to a_0$ for $g \gg a_0$.
- *Pass:* exact identity and limits.
- *Means:* ties the "dark" share of the field to the bond's covalency. Purely algebraic, but it fixes the dictionary's reading of TetB.

**T09. The single bond against the full sp³ crystal.**
- *Question:* in a full diamond crystal, is the TetA-site weight of the occupied states still $\mu(x)$?
- *Method:* numerical. Harrison's 8-band sp³ tight-binding model on diamond, with the polar shift applied to the TetA and TetB hybrids. Integrate the occupied bands over the Brillouin zone, and compare the TetA-site weight with the single-bond $\mu(x)$, as the metallic coupling $V_1/V_2$ runs from 0 to 0.5.
- *Pass:* within 2% of $\mu(x)$ for $V_1/V_2 \le 0.25$ (the covalent regime of real group-IV crystals), across $10^{-2} \le x \le 10^{2}$.
- *Means:* a pass says the bond reading holds for a crystal, not just a molecule. The deviation as $V_1$ grows measures how much a lattice correction would modify $\mu$.

**T10. Share by Bloch mode.**
- *Question:* in the simplest two-sublattice model (one orbital per site), how does the TetA share vary with crystal momentum?
- *Method:* numerical. $H(k) = \begin{pmatrix} -V_3 & -t f(k) \\ -t f^*(k) & V_3 \end{pmatrix}$, $f(k) = \sum_a e^{ik\cdot v_a}$. Each mode has $x_k = (u_k + \sqrt{1 + u_k^2})^2$ with $u_k = V_3/(t|f(k)|)$. Compute the density-of-states-weighted mean share.
- *Pass (reported, not judged):* the mean share and its spread. Also check exactly that $f(0) = K = 4$ and that the band edge sits at $\pm\sqrt{V_3^2 + 16t^2}$.
- *Means:* shows how a lattice spreads one bond's $x$ into a range, and where $K = 4$ enters the spectrum.

## C. Symmetry

**T11. Parity as polarity reversal, at lattice level.**
- *Question:* does the bond-midpoint inversion send $V_3 \to -V_3$ across the whole crystal?
- *Method:* exact. With $\Sigma = \mathrm{diag}(1, -1)$ on the sublattices, check $\Sigma H(k; V_3)\Sigma = -H(k; -V_3)$, and that inversion maps $H(k; V_3)$ to $H(-k; -V_3)$ with sublattices swapped. At $V_3 = 0$ the spectrum is symmetric, $E \leftrightarrow -E$.
- *Pass:* exact identities.
- *Means:* lifts result 9.7 (exchange = swapping the ends) from one bond to the crystal.

**T12. Symmetry breaking when $x \ne 1$.**
- *Question:* does the polar bond reduce the symmetry from diamond to zincblende, as $x \ne 1$ should break the TetA/TetB exchange?
- *Method:* exact. Count the point operations, about a site and about a bond midpoint, that preserve the Hamiltonian: 48 for diamond (Fd-3m) at $V_3 = 0$, 24 for zincblende (F-43m) at $V_3 \ne 0$. Identify the lost coset as the parity coset.
- *Pass:* the counts are 48 and 24, and the lost coset is exactly the operations that swap the sublattices.
- *Means:* the ring at $x = 1$ is the point of extra symmetry, and the lost half is parity, matching Letter 3's equal-share point.

**T13. The 64 states and the 8×8 Walsh–Hadamard matrix.**
- *Question:* does the 8×8 sp³ Hamiltonian of a diamond primitive cell, with 64 matrix elements and 2 sites × 4 hybrids, block-diagonalise under the 8×8 Walsh–Hadamard matrix of the cube?
- *Method:* exact, at $\Gamma$ and at the X and L points. Transform by $H_8 = H_2 \otimes H_2 \otimes H_2$ with rows ordered by the cube's vertices, and record the block structure.
- *Pass:* block-diagonal at $\Gamma$, with blocks matching the irreps of $O_h$ (or $T_d$ when $V_3 \ne 0$).
- *Means:* a pass is the first concrete link between the 64 field-closure states and a lattice object. A fail says the 64 are not the cell's orbital space, and the search moves elsewhere.

**T14. The pixel's symmetry as cosets.**
- *Question:* is the pixel's symmetry the TetA symmetry plus a parity coset, as the Gram-matrix proof has it (Sym(S) = Sym(TetA) × {±I})?
- *Method:* exact. Enumerate the 48 symmetries of the stellated octahedron and the 24 of one tetrahedron. Check index 2, check that the nontrivial coset swaps TetA and TetB, and check that the coset is $-I$ times the tetrahedral group.
- *Pass:* exact.
- *Means:* confirms the tiling's TetA/TetB swap (result 7.3) is the same parity as in the proofs.

## D. Rotation, torsion and the vortex

**T15. Rotation as bond phases, and the axial torsion's sign.**
- *Question:* on the lattice, does a rotating frame give opposite axial "torsion" on TetA and TetB legs, as Proposition 3 of the Gram-matrix proof does in the continuum?
- *Method:* exact on a small periodic lattice. Model a uniform rotation $\Omega$ by Peierls phases $e^{i\theta_{ij}}$ on the bonds. Build the lattice analogue of the axial torsion from the phase circulation around the hexagon rings with the frame's orientation. Compare the TetA-leg and TetB-leg contributions.
- *Pass:* equal and opposite, reversing with $\Omega$, to machine precision.
- *Means:* puts Proposition 3 and the two-connection note's $\pm 2\Omega/3$ onto the lattice, the first lattice-level statement about chirality.

**T16. The hourglass lemma on the net.**
- *Question:* does the lattice version of a swirl plus through-flow have its helicity reversed by the bond-midpoint inversion, as the hourglass lemma says for the continuum?
- *Method:* numerical. Put a discrete vector field on the bonds, with an azimuthal swirl and an axial through-flow, compute the discrete helicity, apply the inversion, and recompute.
- *Pass:* helicity reverses sign, magnitude equal within $10^{-12}$; swirl kept, through-flow reversed.
- *Means:* links `research/vortex-hourglass/LEMMA.md` to the lattice.

## E. Is it photonic?

These test the claim that rests on the diamond structure's photonic band gap. They need a vector plane-wave solver (written in numpy, validated first).

**T17. Reproduce the diamond photonic gap.**
- *Question:* does the solver reproduce Ho, Chan and Soukoulis (1990)?
- *Method:* numerical. Vector plane-wave expansion of Maxwell's equations for dielectric spheres on a diamond lattice, at the paper's filling fraction and index contrast, with at least 1000 plane waves. Check convergence by doubling.
- *Pass:* a complete gap between bands 2 and 3, with gap-to-midgap ratio within 10% of the published value.
- *Means:* validates the solver. Nothing else in section E counts unless T17 passes.

**T18. Diamond against the other nets.**
- *Question:* is the complete gap special to diamond among the nets here?
- *Method:* as T17, for simple cubic, fcc and lonsdaleite at matched filling and contrast.
- *Pass (diamond singled out):* diamond's gap is at least twice the next largest.
- *Means:* tests whether "the parity root picks diamond" also picks the best photonic structure.

**T19. One root's legs against the full pixel.**
- *Question:* for rods along the pixel legs, which carries the gap: one root's legs (the diamond net, result 7) or all eight legs (both roots)?
- *Method:* as T17, with dielectric rods along the TetA legs only, then along all eight, over rod radii from 0.05 to 0.3 of the lattice constant.
- *Pass (reported, not judged):* gap-to-midgap ratio against rod radius for both.
- *Means:* tells how "both roots in one pixel" behaves photonically compared with "one root traced through the tiling".

## F. Calibration

**T20. Which energies would give $x = g/a_0$?**
- *Question:* result 9 requires a polar energy $(g - a_0)/2$ and a coupling $\sqrt{g a_0}$. In the bond-orbital model, $V_2 \propto \hbar^2/(m d^2)$ for bond length $d$. What bond length would $V_2 \propto \sqrt{g a_0}$ imply?
- *Method:* exact scaling, then numbers. Derive $d \propto (g a_0)^{-1/4}$. Evaluate $d$ at $g = a_0$, taking the framework's unit of gravity, the classical electron radius, as the reference length, with no other input.
- *Pass (reported, not judged):* the implied $d(g)$ and its value at the ring.
- *Means:* exploratory, and flagged as such. It turns the open question of result 9 into a concrete length scale the framework can check against its own units. No match is claimed in advance.

---

## Order

1. **T01, T02, T03.** If the lattice cannot carry the field, stop and record why.
2. **T05–T08 and T11–T14.** Exact and quick: they settle the algebra.
3. **T09, T10, T04.** The bond reading in a crystal, and stacking.
4. **T15, T16.** Rotation and the vortex.
5. **T17, then T18–T19.** Photonic, only after the solver passes T17.
6. **T20** last, as exploration.

Results go in `tests/RESULTS.md`, one line per test (pass/fail, key number, date), with failures kept.
