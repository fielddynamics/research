# Paper VII: Notes for a Future Revision

*Dual Tetrad Topology and the Field Origin: From Nuclear Decay to Galactic Dynamics (v7, 108 pages)*

These notes come from a full reading of the v7 source, [`Dual_Tetrad_Gravity_And_The_Field_Origin.tex`](Dual_Tetrad_Gravity_And_The_Field_Origin.tex), and from running its validation script ([`python/run_all_validations.py`](python/run_all_validations.py), 21 of 21 pass). The published paper is unchanged. The notes record what later work in this archive strengthens, and what a revision should correct or reframe. Every numerical point is reproduced by [`revision_checks.py`](revision_checks.py).

Section numbers follow the compiled paper: II Why Gravity Has Topology, III The Dual Tetrahedron, IV The Coupling Polynomial, V Equations, VI The Fine-Structure Constant, VII Dark Matter and the Hubble Constant, VIII Covariant Completion, IX The Poisson Equation, X The Electron Mass, XI The Field Closure Mechanism, XII Discussion.

---

## What later work strengthens

1. **The prefactor 17/13 (§IV.D, Eq. 24).** Letter 2 adds the reason the metric couples through the Field Origin read. The metric is parity-even, and $s = 0$ isolates the parity-even core, because the sign representation that carries the parity-odd $k$ is absent from the Christoffel sector. A look-elsewhere test ([`research/g_from_topology/look_elsewhere_G.py`](../../../research/g_from_topology/look_elsewhere_G.py)) checks 1,953 alternatives of the form $(p/q)\,\alpha^n$ with $p, q \le 21$ and $n = 18$–24. Only $17/13 \cdot \alpha^{21}$ lands within the tree-level 0.12%, and it is also the only one within the 22 ppm uncertainty of $G$ once the one-loop factor is included. Both points would strengthen §V.A.
2. **The three states and the odd-parity step (§IV.D, §VIII.A).** Letter 3 shows that the torsion-free condition keeps $(f(k,+1)-1)/2 = 10$ and discards $(f(k,-1)-1)/2 = 6$ components per face, 40 + 24 in all. That gives the $s = \pm 1$ states, and the vanishing of the odd-order $\beta_1, \beta_3$, a concrete home in the connection.
3. **Three routes to $\mu(x) = x/(1+x)$.** Paper I (lossless, local closure), Letter 2 (exchange symmetry) and §VII.A here (detailed balance, with the "1" as the Field Origin's processing capacity) reach the same law. Cross-referencing them would make the constitutive law the best-supported link in the chain.
4. **The 28 is a $d = 3$ signature.** Corrected as in item 1 below, the identity $V + E + F = k(k + d)$ holds only at $d = 3$ among $d \ge 2$. It singles out three dimensions, alongside the tiling condition $2(d+1) = 2^d$.
5. **The closure mechanism (§XI).** The statement that gravitational acceleration, lensing and time dilation are the gradients of one registered state is the paper's clearest answer to what gravity is. [*What Is Gravity?*](../../../research/g_from_topology/what_is_gravity.md) builds on it, and a revision could bring it forward from §XI to the introduction.

---

## Corrections and reframings

### Mathematics and consistency

1. **$V + E + F = k(k + d)$ is stated for general $d$ (§III.D).** The paper says the identity holds "for the compound of two simplices in $d$ dimensions". Counting vertices, edges and 2-faces of two interlocking $d$-simplices, it holds at $d = 3$ (28 = 28) and trivially at $d = 1$, but fails elsewhere: $d = 2$ gives 14 against 15, and $d = 4$ gives 50 against 45. The correct statement is stronger: among $d \ge 2$, only $d = 3$ satisfies it.
2. **The Minkowski sign convention changes.** The tetrad equation in §II.B uses $\eta_{ab} = \mathrm{diag}(-1, +1, +1, +1)$; the component count in §IV.B uses $\mathrm{diag}(1, -1, -1, -1)$. Choose one.
3. **The tile scale.** §II.E and Result 7 identify the tile with the classical electron radius, $r_e = 2.818$ fm, and the mass–closure identity $m = \alpha\hbar/(rc)$ requires that value. The mass–energy subsection of §V.B instead says the tile has scale $r \sim h/(mc) \approx 2.4 \times 10^{-12}$ m, the Compton wavelength. That sentence should use $r_e$.
4. **Which sector is observed.** The vortex figure in §III.B labels TetA "our spacetime" and TetB "other spacetime". §IX calls $s = -1$ "the spatial projection, where we observe the field", and the 13 the "observable capacity". Letter 3, written later, treats TetA as the sector general relativity retains. One reading of the 13 should be used throughout.

### Evidence

5. **Route 2 and the $a_0$ check are one relation (§II.E, §IV.B, §VII.A).** "Route 2", $r_e = k\sqrt{Gm_e/a_0}$ (0.21%), the ratio check $a_0/(Gm_e/r_e^2) = 15.93$ (0.41%), and Eq. (a0), $a_0 = k^2 G m_e/r_e^2$, are the same equation rearranged. Since $a_0 \propto r^{-2}$, the 0.21% and the 0.41% are the same comparison. It should be counted once.
6. **How precisely $a_0$ is known.** The 0.41% agreement compares the derived value with $1.22 \times 10^{-10}$ m/s². The empirical value is $(1.20 \pm 0.02_{\text{stat}} \pm 0.24_{\text{sys}}) \times 10^{-10}$ m/s² (McGaugh, Lelli and Schombert 2016), so the measured scale is known to about 20%. The derived $a_0$ is consistent with it, but the comparison is not a 0.4% precision test.
7. **"Six independent accidents" (§XII.F).** The estimate that six sub-percent agreements would occur by chance with probability below $10^{-12}$ treats $\alpha$, $G$, $H$, $a_0$, $m_e$ and $\mu(x)$ as independent. $a_0$, $m_e$ and $H$ come from the same two-equation system ($a_0 = k^2 G m/r^2$ together with the horizon relation), and $\mu$ is a functional form rather than a number. The probability statement should be removed, or recomputed counting only the independent comparisons.
8. **The outer Milky Way (§VII.A, the rotation-curve figure and table).** The paper cites Jiao et al. (2023) in support of the flat rotation curve. That paper, titled *Detection of the Keplerian decline in the Milky Way rotation curve*, reports about 181 km/s at 25.5 kpc from Gaia DR3 and rejects a flat curve at 3σ. The 25 kpc data point in the figure, 200 ± 15 km/s, is Eilers et al. (2019). Paper VII predicts about 204 km/s there. Jiao et al. should be presented as a measurement in tension with the prediction, and as a sharp test, not as support.
9. **Wide binaries (§VIII.C).** The validation table cites Hernandez et al. (2022, 2023) for a velocity plateau. Banik et al. (2024) analyse Gaia DR3 wide binaries and find them consistent with Newtonian gravity. Both should be cited; the question is open.
10. **The Hubble tension paragraph (§VII.B).** "The SH0ES analysis calibrates distances using Newtonian gravity, which overestimates luminosity distances at low accelerations" does not describe the distance ladder, which rests on Cepheid and Type Ia supernova calibrations. The claim should be recast as a hypothesis about where a scale-dependent gravity would enter each analysis.
11. **The electron-mass precision (Result 7, §X.A).** The text gives 0.1%. The validation script reports 0.0005% for $m_e$ when $H$ is taken from the chain itself, and 0.10% when $m_e$ is recovered from the observed $H$. The text should say which comparison the 0.1% refers to.

### Attribution

12. **The integer 17.** §IV.E and §VI.B attribute 17 to Hassan and Kocic (2018) as the "Hamiltonian interaction space dimension". The count $16 + 1$, the frame-transition matrix components plus the existence condition, is this paper's construction built on Hassan–Rosen and Hassan–Kocic results. It is safer to present it that way.
13. **Bibliography.** The key `hoffman2000` points to a 1999 article (*J. Chem. Educ.* 76, 331).

---

## Running the checks

```bash
python revision_checks.py            # items 1, 5, 6 and 8 above
python python/run_all_validations.py # the paper's own 21 validations
```

## References

- Banik, I. et al. (2024). Strong constraints on the gravitational law from Gaia DR3 wide binaries. *Mon. Not. R. Astron. Soc.* 527, 4573.
- Eilers, A.-C., Hogg, D. W., Rix, H.-W. and Ness, M. K. (2019). The circular velocity curve of the Milky Way from 5 to 25 kpc. *Astrophys. J.* 871, 120.
- Jiao, Y., Hammer, F., Flores, H., Wang, J. L. and Yang, Y. (2023). Detection of the Keplerian decline in the Milky Way rotation curve. *Astron. Astrophys.* 678, A208.
- McGaugh, S. S., Lelli, F. and Schombert, J. M. (2016). Radial acceleration relation in rotationally supported galaxies. *Phys. Rev. Lett.* 117, 201101.
