# Lean audit: The Walsh Eigenmodes of the Cube, and What Field Closure Reads

| | |
|---|---|
| **Formalisation** | [`lean/WalshEigenmodes.lean`](lean/WalshEigenmodes.lean), 1158 lines, Lean 4.36.0 + Mathlib v4.36.0 |
| **Depends on** | [`../gram-matrix-tetrad-equation/lean/`](../gram-matrix-tetrad-equation/lean/), and through it the [forced tetrahedral frame](../forced-tetrahedral-frame/lean/) (`Mmat`, `Mcol`), the tetrad scheme and the half-space regions; imported, not copied |
| **Build** | 0 errors · 0 warnings · no `sorry` / `admit` / custom `axiom` / `native_decide` |
| **Axioms** | All 46 `#print axioms` checks report only `propext`, `Classical.choice`, `Quot.sound` |
| **Reproduce** | `cd lean && lake exe cache get && lake build` |
| **CI** | `.github/workflows/lean-walsh-eigenmodes.yml`, on every change to this proof or any proof it imports |

**Verdict.** Theorems 1–4, Corollary 1, Proposition 2, Proposition 3 and the reduction in Proposition 1 (ii) are proved. Two parts are not formalised: the fifteen-site model with its numerical shares, and the node's code runs (§3). Nothing in the note was found to be wrong. One edge case is made explicit: at $\theta = \pi/4$ the antibonding share $1/(1-\cot\theta)$ is undefined rather than outside $[0,1]$.

## 1. Definitions to check against the paper

| Lean | Paper |
|---|---|
| `C = Bool × Bool × Bool`; `cx, cy, cz` (`true ↦ +1`); `pt s ∈ ℝ³` | the eight corners $s \in \{\pm1\}^3$ |
| `w S s = ∏_{d∈S} s_d`, `S : C` read as a subset of `{x, y, z}`; `grade S = |S|`; `S1, Sx, …, Sxyz` | the Walsh functions $w_S$ and their grades |
| `inA s` | $s$ is a TetA corner, $xyz = +1$ |
| `flip m s`, `flipMat m` | the bit flips $F$ and their permutation matrices |
| `adj` | the cube graph $A$ (corners at Hamming distance 1) |
| `Td = Fin 6 × Fin 4`; `act g s` = axis permutation `perm3 i`, then the even sign-flip mask `masks j`; `R g` its signed-permutation matrix (`pt_act`) | $T_d$ and its action on the corners and on $\mathbb R^3$ |
| `IsInv H`: `H (g s) (g t) = H s t`; `permMat g` | $T_d$-invariance; `isInv_iff_commute` shows it is commuting with the permutation representation |
| `Hpar εA εB hAA hBB he hd` | Eq. (2)'s six parameters: by chamber on the diagonal, face diagonal inside a chamber, edge (distance 1) or body diagonal (distance 3) between |
| `uA, uB, fA d, fB d` | the normalised chamber basis $u_{A,B}$, $f^d_{A,B}$ |
| `Heff Hcc Hcr Hrc Hrr E` | $H_{\rm eff}(E) = H_{cc} + H_{cr}(E - H_{rr})^{-1}H_{rc}$, over **any** finite set of other sites |
| `gS` | the rotoreflection $S$: $(x, y, z) \mapsto (-y, x, -z)$; a function transforms as $f \mapsto f \circ S$ |
| `psi = x + i y`; `rot` | $\psi$ and the quarter turn $C_4$ ($x \mapsto y$, $y \mapsto -x$) |
| `J t ψ i j = 2 Im(ψ̄_j H_ji ψ_i)`, `H = t·adj` | the current $J_{i\to j}$ |
| `SA, SB`; `RA, RB`; `mu = SA/(SA+SB)` | the chamber sums $S_{A,B}$, the frame readouts $R_{A,B}\psi = \sum_{s\in\text{chamber}}\psi(s)\,s$, and $\mu$ |
| `coef S φ = (1/8) Σ w_S φ` | the node's Walsh coefficients $c_S$ |
| `mode θ`, `amode θ` | the bonding mode $\cos\theta\,u_A + \sin\theta\,u_B$ and its antibonding partner |

## 2. Statements

| Paper | Lean | Notes |
|---|---|---|
| Theorem 1 | `walsh_orthogonal`, `walsh_complete`, `theorem1`, `eight_parameters`, `cube_graph` | commuting with every bit flip ⟺ every $w_S$ is an eigenmode; exactly one $H$ for each choice of the 8 eigenvalues; $Aw_S = (3-2|S|)w_S$, $Lw_S = 2|S|w_S$ |
| $T_d$ | `Td_facts`, `Td_complete`, `inversion_exchanges` | 24 bijections keeping TetA; they are **exactly** the signed permutations keeping TetA; $-I$ exchanges the chambers |
| Theorem 2 (i) | `corners_under_Td` | $1$ and $xyz$ invariant; vectors transform by `R g`; bivectors $= xyz \cdot$ vectors; $xyz\,w_S = w_{\bar S}$, grade $k \mapsto 3-k$, equivariant |
| Theorem 2 (ii) | `Hpar_inv`, `general_inv`, `walsh_in_chamber_basis`, `blocks` | `Hpar` is symmetric and invariant; **every** symmetric invariant $H$ is `Hpar` (the orbits are exhausted by `rep_orbit`); the block entries $\alpha, \beta, \gamma, \delta$ and $1 \propto u_A + u_B$, …, $xyz \propto u_A - u_B$, $yz \propto f^x_A - f^x_B$ |
| Theorem 2 (iii) | `alike_iff` | every $w_S$ an eigenmode ⟺ $\epsilon_A = \epsilon_B$, $h_{AA} = h_{BB}$ ⟺ invariant under $-I$; eigenvalues $\alpha \pm \beta$, $\gamma \pm \delta$ |
| Theorem 2 (iv) | `mixing`, `mixing_tan`, `lower_grade_weight` | $(\cos\theta, \sin\theta)$ is an eigenvector ⟺ $(a-c)\sin2\theta = 2b\cos2\theta$, the form of Eq. (3) that needs no division; weight $(\cos\theta+\sin\theta)^2/2$ on the lower grade, with the chamber bases orthonormal |
| Proposition 1 (ii) | `schur`, `Heff_commute`, `Heff_symm`, `whole_cube` | the eigenproblem reduces to $H_{\rm eff}(E)c = Ec$ when $E \notin \mathrm{spec}\,H_{rr}$; $H_{\rm eff}$ inherits equivariance and symmetry, so it has the form of Eq. (2) at every such $E$ |
| Link to the chain | `tetA_is_frame`, `RA_eq_frame` | TetA's corners are the forced frame's legs `Mcol a`; $R_A\psi = M(\psi\vert_{\rm TetA})$ |
| Corollary 1 | `S_on_walsh`, `winding_vectors`, `eigen_orth`, `vortex_T2` | $S$ is $+1$ on $1, xyz$, $-1$ on $z, xy$ and a quarter turn on $(x, y)$ and on $(xz, yz)$; $x + iy$ and $xz - i\,yz$ have eigenvalue $+i$; any $T_d$ eigenvector with eigenvalue $\ne 1$ is orthogonal to $1$ and $xyz$; $V_{+i}$ on the corners lies in the $T_2$ modes |
| Proposition 2 | `two_standing_waves` | $tA\psi = t\psi$; $C_4\psi = -i\psi$; $\lVert\psi\rVert^2 = 16$; current $-8t$ through **each of the four** half-planes bounded by the $z$ axis; zero current for every real amplitude on every edge |
| Theorem 3 (i), (iv) | `frame_equivariant`, `scalar_invariant`, `readouts_factor` | equivariant columns are $a\,s$ on TetA and $b\,s$ on TetB; invariant scalars are constant on each chamber; every equivariant linear readout is $aR_A + bR_B$ or $aS_A + bS_B$ |
| Theorem 3 (ii) | `closure`, `one_root` | $R_A(1) = \sum_a$ `Mcol a` $= 0$; $T_d$ fixes no nonzero vector; $R_A$ injective on sum-zero amplitudes |
| Theorem 3 (iii) | `one_root` | $(S_A, R_A)$ vanish exactly on TetB-supported amplitudes (rank 4); $w_S = w_{\bar S}$ on TetA |
| Theorem 3 (iv) | `field_closure` | $(S_A, S_B, R_A, R_B)$ injective on all eight corners; $S$ reads exactly $1, xyz$, $R$ exactly the six $T_2$ modes, with every value given |
| $\mu$ needs both roots | `mu_needs_both` | equal TetA readouts, $\mu = 1$ and $\frac12$ |
| Theorem 4 (i) | `node_mu` | $c_1 = (S_A+S_B)/8$, $c_{xyz} = (S_A-S_B)/8$, $(1 + c_{xyz}/c_1)/2 = \mu$; adding any $T_2$ mode leaves $\mu$ unchanged |
| Theorem 4 (ii) | `node_rule` | Parseval $\sum v^2 = 8\sum c_S^2$; spread contracts by $1-\kappa$ under a common target; $c_S$ linear in a common amplitude |
| Theorem 4 (iii) | `inward_fixed` | $c = 1$ is fixed whatever the signal; from $c = \frac12$ it moves |
| Proposition 3, shares | `shares` | TetA share $1/(1+\tan\theta)$; antibonding $1/(1-\cot\theta)$, outside $[0,1]$ for $\tan\theta \ne 1$ |
| Proposition 3 (i) | `mixing_tan`, `linear_reading`, `exchange_angle` | $\mu = x/(1+x)$ ⟺ $\tan\theta = 1/x$ ⟺ $\tan\theta/(1-\tan^2\theta) = x/(x^2-1)$, which is $\beta/(\alpha_A - \alpha_B)$ by Eq. (3); $\mu(1/x) = 1-\mu(x)$; $\tan(\pi/2-\theta) = 1/\tan\theta$ |
| Proposition 3 (ii) | `parts` | $\mu g_t = g_t^2/(g_t+a_0)$, $(1-\mu)g_t = g_t a_0/(g_t+a_0)$ |
| Proposition 3 (iii) | `weight_share`, `quadratic_reading` | weight share $1/(1+\tan^2\theta) = x/(1+x)$ ⟺ $\tan\theta = 1/\sqrt x$; ratio $\sqrt x/(x-1)$ |
| Proposition 3 (iv) | `readings_agree` | $1/x = 1/\sqrt x$ ⟺ $x = 1$, where $\mu = \frac12$ |

## 3. Not formalised

- **The fifteen-site whole cube.** Proposition 1 (i), with its projectors, and the numerical grade-1 shares 0.83, 0.007 and 0.98 of (ii) are checked only by the script. Lean proves the reduction and its symmetry for any set of other sites and any representation on them, which is the step (ii) rests on.
- **The octahedron in Corollary 1.** The decomposition $4A_1 \oplus E \oplus 3T_2$ of the whole cube is cited. The corner half, that winding modes lie in the corner $T_2$ modes, is proved.
- **The metric kernel** in Theorem 3 (iii), that the metric cannot see grades 2 and 3, is cited from the coupling algebra.
- **The node's code** in Theorem 4: the 800-step runs of `octahedral_node.py`. The three properties they illustrate are proved as algebra.
- **The bond-orbital dictionary** $V_3/V_2 = (x-1)/(2\sqrt x)$ in Proposition 3 (iii) is cited; the ratio $\sqrt x/(x-1)$ it is read from is proved.

## 4. Notes for a referee

- **Hom statements in column form.** A linear readout of corner amplitudes is fixed by its values on the basis amplitudes, its columns. Equivariance is $m(gs) = R_g\,m(s)$. Theorem 3 (i) is `frame_equivariant` restricted to TetA. It is proved by stabilisers and orbits, not by Schur's lemma.
- **Orbits by enumeration.** Statements about the 24 elements and 64 corner pairs are decided by Lean's kernel (`decide`), not by `native_decide`.
- **Numbering** follows the PDF: Proposition 1 is the whole cube, Corollary 1 the vortices, Proposition 2 the cube vortex, Proposition 3 $\mu$ and the angle.
