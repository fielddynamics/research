# Active Work 11 — The King's Chamber as Field-Origin Vertex

**Status:** Consolidation — pulls portal-resonance algebra into one statement and pins it to the implementation
**Purpose:** State, in one document, what the King's Chamber *is* algebraically, and tie each piece to the code
**Reading time:** 12 minutes
**Companion modules:** `python/portal_resonance.py` (579 lines, 58 tests), `python/closure_read.py` (extensions), `python/hinge.py` (extensions)
**Canonical source:** the field-origin synthesis (May 2026) that is the basis for this document; this AW is its implementation-bound translation

---

## 0. Headline

$$\boxed{\;\text{King's Chamber}\;=\;\text{coherent field-origin cavity where TetA/TetB parity overlap, 21-band hinge transfer, Coulomb-pentachoron attenuation, and associator source formation all intersect.}\;}$$

The intersection vertex itself is the K=5 pentachoron — a 4D, $S_5$-symmetric algebraic object. The King's Chamber is its engineered 3D focal point: the location where the always-on hinge $J_4(x)$ is isolated, phase-locked, and made coherent for one mode.

The local field-origin algebra has four ingredients:

$$\boxed{\;\mathcal V_{\text{origin}}(x)\;=\;\Psi_{AB}(x)\;+\;\lambda_e\,J_4(x)\;+\;g_R\,R_x\;+\;h_{21}\cos(21\theta_x)\;}$$

with $\lambda_e = \alpha^{21}\,(17/13)\,(g_e/2) = \alpha_G$. The four pieces are: cross-sheet order parameter, 21-band hinge, nonlinear associator source, and $\mathbb Z_{21}$ phase lock. Each is implemented as a discrete object in `portal_resonance.py`.

## 1. The local closure algebra

**Status:** derived

The minimal tensor closure of the K=4 frame is

$$T_{\le 2}(V) \;=\; \mathbf 1 \,\oplus\, V \,\oplus\, V^{\otimes 2}$$

with $\dim V = 4$, so $\dim T_{\le 2}(V) = 1 + 4 + 16 = 21$. Splitting by parity:

$$T_{\text{even}} = \mathbf 1 \oplus V^{\otimes 2} \quad (\dim 17),\qquad T_{\text{odd}} = V \quad (\dim 4)$$

The closure-read at $K=4$ produces the cyclotomic shell

$$\boxed{\;(\Phi_6(4),\,\Phi_4(4),\,\Phi_3(4))\;=\;(13,\,17,\,21)\;}$$

with the algebraic identification:

| Value | Polynomial | Reading |
|---|---|---|
| 13 | $\Phi_6(4)$ | TetA/TetB shared overlap core (superdimension) |
| 17 | $\Phi_4(4)$ | even sector, one parity sheet |
| 21 | $\Phi_3(4)$ | full closure, the sheet union |

The coupling polynomial $f(K,s) = K^2 + sK + 1$ at $K=4$ reads three states of the same local object:

$$f(4,-1) = 13,\qquad f(4,0) = 17,\qquad f(4,+1) = 21$$

with $s \in \{-1, 0, +1\}$ the parity signature. The three values are not separate quantities — they are *three readings of the same local cavity*.

**In code:** `closure_read.cyclotomic_shell_eigenvalues(4)` returns $(13,17,21)$; `closure_read.coupling_polynomial(4, s)` evaluates $f(4,s)$ for any signature.

## 2. Parity-sheet inclusion-exclusion

**Status:** derived (new in this consolidation)

The deeper reading of $(13,17,21)$ is set-theoretic. Let $A$ = TetA parity sheet, $B$ = TetB parity sheet. At $K=4$:

$$|A| = |B| = 17,\qquad |A \cap B| = 13,\qquad |A \cup B| = 21$$

so inclusion-exclusion gives

$$\boxed{\;|A| + |B| - |A \cap B| \;=\; 17 + 17 - 13 \;=\; 21\;}$$

Equivalently:

$$\boxed{\;21 = 13 + 4 + 4\;}$$

The 13 is the shared TetA/TetB core. The first 4 is TetA-exclusive parity content; the second 4 is TetB-exclusive. Together they sum to the full closure at the field origin.

**Consequence:** the intersection vertex *as a set* is the 13-core. The full active closure of the two sheets is the 21-band. These are distinct objects with distinct algebraic roles — the framework's parity sheets are set-valued, not abstract labels.

**In code:** `closure_read.parity_sheet_inclusion_exclusion(K)` returns $\{|A|, |B|, |A\cap B|, |A\cup B|\}$; verified at $K=4$ in `test_closure_read.py`.

## 3. The geometric realization of $17/13$

**Status:** derived (new in this consolidation)

The cyclotomic ratio $\Phi_4(4)/\Phi_6(4) = 17/13$ is not an abstract impedance — it is the *cosecant of an overlap angle*. Treat the parity-sheet incidence as inner products on a Euclidean realization:

$$\langle A, A\rangle = \langle B, B\rangle = 17,\qquad \langle A, B\rangle = 13$$

Then

$$\cos\theta_4 \;=\; \frac{\langle A, B\rangle}{\sqrt{\langle A,A\rangle\langle B,B\rangle}} \;=\; \frac{13}{17}$$

so

$$\boxed{\;\sec\theta_4 \;=\; \frac{17}{13}\;}$$

The framework's $17/13$ factor in $\alpha_G = \alpha^{21}(17/13)(g_e/2)$ is therefore *the geometric secant of the TetA/TetB overlap angle*. It is the impedance at the field-origin interface, with a concrete Euclidean meaning. The two parity sheets are at angle $\theta_4 = \arccos(13/17) \approx 40.0°$.

**In code:** `closure_read.parity_sheet_dot_products(K)` returns the three inner products; `closure_read.parity_overlap_angle_geometric(K)` returns $\theta_4$ and $\sec\theta_4$; verified in `test_closure_read.py`.

## 4. The 21-band shift identity

**Status:** derived (§01.4 in the project)

The cyclotomic shift identity is

$$\boxed{\;\Phi_3(K) \;=\; \Phi_6(K+1)\;}$$

so at $K = 4$:

$$\Phi_3(4) \;=\; \Phi_6(5) \;=\; 21$$

The K=4 full closure band coincides with the K=5 lower receive band. This is the algebraic basis for the K=4 → K=5 hinge: the band integer 21 is *simultaneously* TetA's full-closure exit and the pentachoron's lower-pole entry.

The two shell Hamiltonians:

$$H_4 = 13\Pi_{4,-} + 17\Pi_{4,0} + 21\Pi_{4,+}$$
$$H_5 = 21\Pi_{5,-} + 26\Pi_{5,0} + 31\Pi_{5,+}$$

share the integer 21 across their bands. **The hinge intertwines because the bands are equal.**

**In code:** `hinge.shell_hamiltonian(K)`, `hinge.shift_identity_check()`, both verified in `test_hinge.py`.

## 5. The hinge operator and its intertwiner

**Status:** derived (§03.1 in the project)

The rank-1 partial isometry

$$\boxed{\;J_4 \;=\; |5,-\rangle\langle 4,+|\;}$$

intertwines the two shell Hamiltonians:

$$\boxed{\;H_5 J_4 \;=\; J_4 H_4 \;=\; 21\,J_4\;}$$

Proof: $H_5 J_4 = \Phi_6(5)\,J_4 = 21\,J_4$ and $J_4 H_4 = J_4 \Phi_3(4) = 21\,J_4$. The eigenvalue 21 on both sides is the same integer from the shift identity. The hinge transfers the K=4 upper pole into the K=5 lower pole with no band mismatch.

**In code:** `hinge.j4_partial_isometry()` returns $J_4$ as a matrix; `hinge.interlevel_intertwiner_check()` verifies $H_5 J_4 = J_4 H_4$.

## 6. Five-fold sub-tetrahedron decomposition

**Status:** structural (new in this consolidation)

The K=5 pentachoron has $\binom{5}{4} = 5$ sub-tetrahedral cells, one for each excluded vertex. The hinge has a 5-fold multiplicity:

$$\boxed{\;J_4 \;=\; \sum_{v=1}^{5} J_4^{(v)}\,\pi_v\;}$$

where $\pi_v$ projects onto the sub-tetrahedron excluding vertex $v$, and $J_4^{(v)}$ is the hinge from that sub-tetrahedron's K=4 frame into the K=5 shell. This is the $S_5 \supset S_4$ branching, combinatorially forced.

**The 5 sub-tetrahedron choices correspond to the 5 relieving chambers** above the King's Chamber. The Hassan-Rosen palindromic structure $\{1, 0, 16, 0, 1\}$ is the apparatus realization: the central chamber is the peak ($16$), the immediate neighbors are zero, the outermost are unit-weight. This is a coupled cavity filter at the algebraic level — not a metaphor.

Which chamber is "electrically open" or "acoustically resonant" picks the active sub-tetrahedron. The apparatus has a genuine 5-state switch at the hinge level.

**In code:** `hinge.sub_tetrahedron_count()` returns 5; `hinge.s5_supset_s4_branching()` verifies $|S_5|/|S_4| = 5$; `hinge.hinge_sub_tetrahedron_decomposition()` returns the structural data on $J_4 = \sum_v J_4^{(v)}\pi_v$. The apparatus-dressed version is `portal_resonance.RelievingChamberSelector` / `portal_resonance.relieving_chamber_selector(v)`; the full info is in `portal_resonance.five_chamber_decomposition_info()`.

## 7. The cross-sheet order parameter

**Status:** structural

The local TetA/TetB coherence is measured by

$$\boxed{\;\Psi_{AB}(x) \;=\; \langle B, x|A, x\rangle\;}$$

In ordinary space, phases are incoherent and $\langle \Psi_{AB}\rangle \approx 0$. At a tuned vertex:

$$\boxed{\;\langle \Psi_{AB}\rangle_{\text{KC}} \;\neq\; 0\;}$$

The King's Chamber is a coherence cavity for the always-existing TetA/TetB exchange. The vacuum has $|\Psi_{AB}| = 0$; the King's Chamber drives $|\Psi_{AB}|$ to a finite value, then locks its phase.

**In code:** `portal_resonance.CrossSheetCoherence` dataclass; `portal_resonance.cross_sheet_order_parameter(amplitude, phase)`; `portal_resonance.vacuum_cross_sheet()` returns the zero-amplitude case; `portal_resonance.kings_chamber_cross_sheet(amplitude_magnitude, phase)` returns the apparatus-driven case. Tested in `TestCrossSheetCoherence`.

## 8. The $\mathbb Z_{21}$ phase lock

**Status:** structural (Landau potential analysis)

The $\mathbb Z_{21}$ order parameter is

$$\Omega_{21} \;=\; \langle e^{i\,21\,\theta}\rangle$$

with $\Omega_{21} = 0$ in the incoherent state and $\Omega_{21} = 1$ at full lock. The effective potential supporting this lock is

$$\boxed{\;V(\Psi) \;=\; a|\Psi|^2 + b|\Psi|^4 - h_{21}(\Psi^{21} + \bar\Psi^{21})\;}$$

Writing $\Psi = \rho e^{i\theta}$, the locking term is $-2 h_{21} \rho^{21}\cos(21\theta)$. The 21 minima are at

$$\boxed{\;\theta_n \;=\; \frac{2\pi n}{21}\;,\quad n = 0, 1, \dots, 20\;}$$

The King's Chamber drives the TetA/TetB order parameter into one of these 21 phase-locked states. Which $n$ is selected is set by the apparatus's address triad (Grand Gallery $\mathbb Z_7$ corbel index × antechamber $\mathbb Z_3$ filter = $\mathbb Z_{21}$).

**In code:** `portal_resonance.z21_landau_psi(psi, a, b, h21)`; `portal_resonance.z21_lock_minima(n_modes=21)` returns the 21 phase locations; `portal_resonance.z21_lock_strength(rho, h21)` computes the well depth. Tested in `TestZ21LandauLockPsi`.

## 9. The compact King's Chamber vertex

**Status:** derived (master equation form)

After phase closure on the pentachoron edge product ($\sum_{i \ne j} \theta_{ij} = 0 \bmod 2\pi$):

$$\prod_{i \ne j}^{5} \alpha e^{i\theta_{ij}} \;=\; \alpha^{20}$$

so the King's Chamber vertex equation in compact form is

$$\boxed{\;V_{\text{KC}}(x) \;=\; \lambda_e\,J_4(x) \;+\; g_R\,R_x\;}$$

with $\lambda_e = \alpha^{21}(17/13)(g_e/2)$. Two pieces: the linear hinge $\lambda_e J_4$ and the nonlinear associator source $g_R R$.

The full field-origin vertex equation adds the order parameter and the lock term:

$$\boxed{\;\mathcal V_{\text{origin}}(x) \;=\; \Psi_{AB}(x) \;+\; \lambda_e\,J_4(x) \;+\; g_R\,R_x \;+\; h_{21}\cos(21\theta_x)\;}$$

The four pieces correspond to: cross-sheet coherence (§7), 21-band transfer (§5), nonlinear closure source (§10), and $\mathbb Z_{21}$ phase lock (§8).

**In code:** `portal_resonance.FieldOriginVertex` dataclass; `portal_resonance.kings_chamber_vertex_compact(g_R=0.0)` returns the compact form; `portal_resonance.field_origin_vertex_equation(...)` returns the full 4-piece $\mathcal V_{\text{origin}}$. Tested in `TestKingsChamberCompact` and `TestFieldOriginVertexEquation`.

## 10. The associator: nonlinear source

**Status:** structural (from `01.5`); axial-landing theorem load-bearing

Define the closure product $a \star b = P_\Omega(ab)$ with $P_\Omega$ the closure-node projector. The associator is

$$R(a, b, c) \;=\; (a \star b) \star c - a \star (b \star c)$$

**Closure-node theorem:** $R(a, b, c) \in \langle 1, I\rangle$ — the associator lands axially, in the parity-invariant subspace.

This is the exact algebraic shape of a source/curvature output: middle-sector circulation produces axial closure defect. The local nonlinear vertex contribution is $g_R R_x$, and because $R_x \in \langle 1, I\rangle$, the nonlinear TetA/TetB exchange outputs an axial observable into TetA.

**That axial observable is what we call gravity / mass / source behavior.**

$$\boxed{\;\text{curvature is the axial residue of nonlinear TetA/TetB exchange.}\;}$$

The framework's `01.5` carries the full derivation; this AW treats the result as a load-bearing input.

**In code:** the associator landing is not directly computed here (it requires constructing the closure-node product $\star$ explicitly, which is open work); $g_R R_x$ appears as a parameter in `portal_resonance.field_origin_vertex_equation` and is stated as a theorem in the module docstring with reference to `01.5`.

## 11. The six matching conditions

**Status:** structural (consolidation of distributed conditions)

For the apparatus to lock the universal vertex into one coherent address, six matching conditions must hold simultaneously:

| # | Condition | Source | Algebraic test |
|:-:|---|---|---|
| 1 | **Band match** | shift identity | $\Phi_3(4) = \Phi_6(5) = 21$ (forced; not tunable) |
| 2 | **Phase match** | $\mathbb Z_{21}$ comb | $\theta_x = 2\pi n / 21$ (Grand Gallery + antechamber) |
| 3 | **Impedance match** | $\sec\theta_4$ | $17/13$ from parity-sheet overlap angle |
| 4 | **Address match** | mirror functional | $G_U = P^T G_V P$ on Gram matrices |
| 5 | **Chirality match** | mirror flip | $\chi_U = -\chi_V$ |
| 6 | **Strong-coupling** | cavity QED | $g\sqrt N / \gamma_{\text{cav}} > 1$ |

Four of these (1, 2, 3, 6) are verifiable from algebra alone given the apparatus parameters. Two (4, 5) require an external address triad — i.e., the existence of a mirror-matched second apparatus.

When all six hold, $\lambda_e \to \lambda_e \cdot Q_{\text{cavity}} \cdot \delta_{\text{phase}} \cdot \mathcal M$. The same weak universal coupling becomes coherent in one address; this is structurally identical to laser threshold.

**In code:** `portal_resonance.six_matching_conditions()` returns a list of dicts, one per condition, with `name`, `algebraic_form`, `verifiable_from_algebra`, and `source` fields; `portal_resonance.algebraic_match_count()` returns 4. Tested in `TestSixMatchingConditions`.

## 12. The pragmatic Lorentzian skeleton

**Status:** conjecture (pragmatic skeleton; full coupled-mode treatment deferred)

The portal resonance amplitude near a Z_{21} peak has the Lorentzian form

$$\boxed{\;\mathcal R_{\text{portal}}(\omega) \;=\; \frac{A^2}{(\omega - \omega_0)^2 + \gamma_{\text{eff}}^2}\;}$$

with effective linewidth

$$\boxed{\;\gamma_{\text{eff}} \;=\; \sqrt{\gamma_{\text{cav}}^2 + \Delta_{\text{addr}}^2 + \Delta_{\text{phase}}^2}\;}$$

The three contributions: $\gamma_{\text{cav}} \approx 7 \times 10^{-2}$ rad/s from cavity-Q loss (`05.3`), $\Delta_{\text{addr}}$ from mirror Gram mismatch, $\Delta_{\text{phase}}$ from $\mathbb Z_{21}$ deviation. On-resonance ($\omega = \omega_0$, all mismatches zero), the amplitude peaks at $A^2/\gamma_{\text{cav}}^2$.

This is a *skeleton*, not a derivation. A full coupled-mode treatment would replace the Lorentzian with the dressed Green's function of the multi-port apparatus operator $\mathsf A_x$. For the present consolidation, the Lorentzian gives the falsifiable lineshape that the §07.1 acoustic test should reveal.

**In code:** `portal_resonance.portal_resonance_lorentzian(omega, omega_0, A, gamma_eff)`; `portal_resonance.effective_linewidth(gamma_cav, delta_addr, delta_phase)`. Tested in `TestPortalLorentzian`.

## 13. Lock-strength compounding

**Status:** structural

The lock strength factor compounds the four apparatus dressings:

$$\boxed{\;\eta_{\text{lock}} \;=\; Q_{\text{cavity}} \cdot \delta_{\text{phase}} \cdot |\mathcal M|\;}$$

with $Q_{\text{cavity}} \sim 10^4$ (granite cavity at 110 Hz), $\delta_{\text{phase}} \in [0, 1]$ collapsing to 1 on $\mathbb Z_{21}$ lock and 0 off-lock, and $|\mathcal M| \in [0, 1]$ from the mirror functional. The effective coupling on-resonance is

$$\lambda_{\text{eff}} \;=\; \lambda_e \cdot \eta_{\text{lock}}$$

with $\lambda_e = \alpha_G \approx 1.75 \times 10^{-45}$. At full lock, $\eta_{\text{lock}} \sim 10^4$, giving $\lambda_{\text{eff}} \sim 10^{-41}$. The coupling is still tiny — but it is now *coherent in one address*, which is the operational distinction.

**In code:** `portal_resonance.lock_strength_factor(Q_cavity, delta_phase, mirror_match)`; `portal_resonance.effective_coupling(lambda_e, eta_lock)`. Tested in `TestLockStrengthCompound`.

## 14. What GR sees after projection

**Status:** structural (`§01.5`, `§06`, and AW 09)

The field-origin algebra lives *before* the GR projection. GR sees only the symmetric, local, torsion-free piece:

$$G_{\mu\nu}^{\text{GR}} \;=\; \Pi_{\text{GR}}\,\mathbb G_{\mu\nu}^{AB}$$

The full sector-valued Einstein tensor from AW 09 has six sectors:

$$\mathbb G_{\mu\nu}^{AB} \;=\; G_{\mu\nu}^{LC} + G_{\mu\nu}^{T} + G_{\mu\nu}^{P} + G_{\mu\nu}^{J} + G_{\mu\nu}^{R} + G_{\mu\nu}^{M}$$

The King's Chamber sector decomposition is dominated by three:

- $G_{\mu\nu}^{P} \sim \nabla_\mu \Psi_{AB}^* \nabla_\nu \Psi_{AB} - \tfrac12 g_{\mu\nu}|\nabla \Psi_{AB}|^2$ — parity tension
- $G_{\mu\nu}^{J} \sim \lambda_e [\mathcal J_\mu \mathcal J_\nu - \tfrac12 g_{\mu\nu}\mathcal J^2]$ — coherent 21-band transfer
- $G_{\mu\nu}^{R} \sim \mathcal R_{\mu\nu} - \tfrac12 g_{\mu\nu}\mathcal R$ — nonlinear closure source

After GR projection, $T$ and $M$ are killed; $P$ and $R$ are averaged into $T_{\mu\nu}$; $J$ is renormalized into $G$. The headline framework prediction $G = (17/13)\alpha^{21}(g_e/2)\hbar c / m_e^2$ at $-13.87$ ppm is what survives the projection.

**The King's Chamber algebra is deeper than the Einstein tensor.** It is the local origin of the parity / hinge / source structure that GR only sees after projection.

## 15. Falsifiability axis

**Status:** falsifiable

The framework's portal-resonance picture predicts at least four observables at the King's Chamber:

1. **21-mode acoustic comb** (`07.1`): 21 peaks below ~1 kHz, organized as 7 clusters of 3, with $\mathbb Z_3$ selection rule suppression.
2. **Vacuum Rabi splitting** (`05.3`): the 110 Hz acoustic mode splits into a doublet at separation $g\sqrt N \approx 2.65$ MHz collective coupling.
3. **$\mu$-metal shielding test** (`07.4`): magnetic shielding around the KC should observably reduce all apparatus signatures.
4. **K-index modulation** (`07.5`): geomagnetic storm response should produce transient Rabi oscillations and frequency shifts in the chamber's mode spectrum.

These are not consequences of a fitted theory — they are predictions of the algebraic framework with no free parameters. The 21-peak count is forced by $\Phi_3(4) = 21$. The 7-cluster grouping is forced by the Grand Gallery $\mathbb Z_7$. The Rabi splitting scale is forced by the strong-coupling calculation. A clean negative on any of these constrains the apparatus identification, not the algebraic spine.

## 16. Code map

Each algebraic piece in this document maps to a discrete object in the package:

| AW section | Algebra | Module / object |
|---|---|---|
| §1 | $(13, 17, 21)$ cyclotomic shell | `closure_read.cyclotomic_shell_eigenvalues(4)` |
| §2 | parity-sheet inclusion-exclusion | `closure_read.parity_sheet_inclusion_exclusion(K)` |
| §3 | $\sec\theta_4 = 17/13$ overlap angle | `closure_read.parity_sheet_dot_products(K)`, `closure_read.parity_overlap_angle_geometric(K)` |
| §4 | shift identity $\Phi_3(4) = \Phi_6(5) = 21$ | `hinge.shift_identity_check()` |
| §5 | $J_4 = \|5,-\rangle\langle 4,+\|$, $H_5 J_4 = J_4 H_4 = 21 J_4$ | `hinge.j4_partial_isometry()`, `hinge.interlevel_intertwiner_check()` |
| §6 | $J_4 = \sum_v J_4^{(v)}\pi_v$ over 5 sub-tetrahedra | `hinge.hinge_sub_tetrahedron_decomposition()`, `portal_resonance.RelievingChamberSelector`, `portal_resonance.five_chamber_decomposition_info()` |
| §7 | $\Psi_{AB}(x) = \langle B,x\|A,x\rangle$ | `portal_resonance.CrossSheetCoherence`, `portal_resonance.cross_sheet_order_parameter(...)`, `portal_resonance.vacuum_cross_sheet()`, `portal_resonance.kings_chamber_cross_sheet(...)` |
| §8 | $\mathbb Z_{21}$ Landau lock | `portal_resonance.z21_landau_psi(...)`, `portal_resonance.z21_lock_minima()`, `portal_resonance.z21_lock_strength(...)` |
| §9 | $\mathcal V_{\text{origin}}$ and $V_{\text{KC}}$ | `portal_resonance.FieldOriginVertex`, `portal_resonance.field_origin_vertex_equation(...)`, `portal_resonance.kings_chamber_vertex_compact(...)` |
| §11 | six matching conditions | `portal_resonance.six_matching_conditions()`, `portal_resonance.algebraic_match_count()` |
| §12 | Lorentzian skeleton | `portal_resonance.portal_resonance_lorentzian(...)`, `portal_resonance.effective_linewidth(...)` |
| §13 | lock-strength compounding | `portal_resonance.lock_strength_factor(...)`, `portal_resonance.effective_coupling(...)` |
| §summary | one-shot report and audit trail | `portal_resonance.field_origin_summary()`, `portal_resonance.showcase_portal_resonance()` |

Total: 579 lines in `portal_resonance.py`, 58 dedicated tests in `test_portal_resonance.py`, plus extensions to `closure_read.py` and `hinge.py` covered by additional tests. All 469 tests in the full suite pass in 0.49 s.

## 17. Status table

| Element | Status |
|---|---|
| $(13, 17, 21)$ closure | derived |
| inclusion-exclusion $17+17-13=21$ | derived (new) |
| $\sec\theta_4 = 17/13$ geometric realization | derived (new) |
| shift identity $\Phi_3(4) = \Phi_6(5) = 21$ | derived (`01.4`) |
| hinge $J_4$ and intertwiner | derived (`03.1`) |
| 5-fold $J_4 = \sum_v J_4^{(v)}\pi_v$ | structural (new) |
| $\Psi_{AB}(x)$ cross-sheet order parameter | structural |
| $\mathbb Z_{21}$ Landau lock | structural |
| compact and full vertex equations | derived (master equation form) |
| associator axial landing $R \in \langle 1, I\rangle$ | structural (`01.5`, theorem) |
| six matching conditions | structural (consolidation) |
| Lorentzian lineshape skeleton | conjecture (pragmatic) |
| lock-strength compounding | structural |
| GR projection chain | structural (`§01.5`, `§06`, AW 09) |
| 21-peak acoustic prediction | falsifiable (`07.1`) |
| Rabi splitting prediction | falsifiable (`05.3`) |

## 18. Headline

The King's Chamber is the place in physical space where the pentachoron's algebraic vertex is engineered into coherent operation. The intersection vertex is not a room — it is the K=5 pentachoron's $S_5$-symmetric 4D algebraic object. The chamber is the focal point where the universal hinge $J_4(x)$ becomes locally phase-coherent in one $\mathbb Z_{21}$ sector, dressed by the apparatus operator $\mathsf A_x$, and observable as a Lorentzian-broadened resonance at one of the 21 spectral peaks of the chamber's mode comb.

The field-origin algebra has four pieces. They are independent in mechanism (overlap, transfer, source, lock), they couple in the apparatus (cavity QED dresses each), and they compound on lock (six matching conditions). Each is now a discrete, tested object in the implementation.

---

**Cross-references:**
- `01_framework_foundations/01.4_shift_identity_proof.md` — the $\Phi_3(K) = \Phi_6(K+1)$ shift identity
- `01_framework_foundations/01.5_universal_vertex_reframe.md` — TetA/TetB exchange as universal, pyramid as tuner
- `03_portal_topology/03.1_K4_to_K5_hinge.md` — the bare hinge algebra
- `03_portal_topology/03.5_SU2_19_chern_simons.md` — the SU(2)₁₉ topological backbone
- `05_cavity_QED_operation/05.3_strong_coupling_calculation.md` — $g\sqrt N / \gamma_{\text{cav}} \approx 4 \times 10^7$
- `07_predictions_and_tests/07.1_acoustic_Z21_spectrum.md` — 21-mode comb prediction
- `active_work/09_curvature_sector_decomposition.md` — the six-sector $\mathbb G_{\mu\nu}^{AB}$ that the King's Chamber dominates
- Canonical source: the May 2026 field-origin synthesis document
- Implementation: `python/portal_resonance.py`, `python/tests/test_portal_resonance.py`, with extensions in `python/closure_read.py` and `python/hinge.py`
