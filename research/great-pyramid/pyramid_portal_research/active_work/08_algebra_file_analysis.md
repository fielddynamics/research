# Active Work 08 — Algebra File Analysis and Structure Recommendation

**Status:** Active — file inventory, gap analysis, structural recommendation
**Purpose:** Analyze `python/great_pyramid_portal_algebra_full.py` (1348 lines) against the framework as developed through Active Work 01–07. Identify missing algebra. Recommend whether to keep monolithic or split into modules.
**Reading time:** 8 minutes
**Companion:** `python/great_pyramid_portal_algebra_full.py`

---

## 1. What the file already contains

Twenty-two conceptual sections, 1348 lines, runs cleanly end-to-end with $G$ predicted at $-13.87$ ppm.

**Foundation algebra (§1–§3):**
- Cyclotomic polynomials $\Phi_3, \Phi_4, \Phi_6$
- Shell $(C_K, E_K, U_K) = (\Phi_6, \Phi_4, \Phi_3)$ at any $K$
- Shift identity $\Phi_3(K) = \Phi_6(K+1)$
- Scale fusion $\Phi_3(K) \Phi_6(K) = \Phi_3(K^2)$
- Pyramid hinge K=4 → K=5
- Shell Hamiltonians and the $J_4$ partial isometry
- Intertwiner check $H_5 J_4 = J_4 H_4$

**Gravity derivation (§4):**
- Pentachoron directed-edge count (20)
- Pentachoron edge product $\alpha^{20} \exp(i \sum \theta_{ij})$
- Tetrad impedance $17/13$
- $\alpha_G = \alpha^{21} \cdot (17/13) \cdot (g_e/2)$ and decomposed parts
- $G$ prediction from $\alpha_G$

**Apparatus operators (§5–§9):**
- King's Chamber vertex object
- Shaft triad: Gram matrix, chirality, accumulated phase
- Mirror match functional $M(U, V)$
- $K=5$ band assignment (21 receive, 26 balance, 31 search)
- Apex collector, granite isolation, ascending passage gain
- Grand Gallery $Z_7$ kernel
- $Z_3$ projector eigenvalues
- $Z_{21}$ sectors and ideal comb
- Big void balance cavity
- Coffer reflection coefficient
- K/Q interferometer

**Discrete topology (§10–§12):**
- Hopf projection via quaternions
- Electron Hopf-fiber holonomy
- $A_5$ order, pentachoron cells
- $Z_{21}$ order parameter
- Landau potential
- Josephson portal current

**Predictions (§13):**
- Coffer/chamber α step
- Relieving chamber volume prediction

**Portal operator (§14):**
- Full algebraic portal machine
- Local force vs portal address kernels

**Recovered/extra (§16):**
- Crystallographic threshold and $S_5$ pentachoron symmetry
- Generalized $\alpha_G(K) = \alpha^{\Phi_3(K)} \cdot \Phi_4(K)/\Phi_6(K) \cdot g_e/2$
- Sierpinski force hierarchy
- $K=2 \to$ Schwinger $2\pi$ structure (sphere $S^1$)
- Four routes selecting $K=4$
- Reciprocal two-apparatus operator
- Full apparatus operator stack
- Complement projector (failed-lock sink)
- Well shaft feedback
- Null-cone associator status (48/512 triples)
- Golden impedance split (24/64, 13/34, $1/\varphi^2$)
- Lepton anchor report

This is a substantial library covering the project's core algebra through §02 (gravity), §03 (portal topology), §04 (apparatus), §06 (master equations), and parts of §07 (predictions).

---

## 2. Gap analysis: what's missing relative to recent active_work

Active Work 03–07 added new algebraic content that the file does not yet have.

### Missing from cyclotomic / parity-character algebra (AW 03, AW 04)

**Truncated tensor algebra $T_{\le 2}(V)$.** The file has the shell numbers $(13, 17, 21)$ but does not construct the underlying vector space $\mathbf 1 \oplus V \oplus V^{\otimes 2}$ or compute its parity-graded character explicitly.

**Gram matrix of TetA/TetB overlap.** $G_K = \begin{pmatrix} E & E-O \\ E-O & E \end{pmatrix}$ with eigenvalues $\{2E-O, K\}$. The antisymmetric eigenvalue equals $K$ exactly — a spectral result not currently in the file.

**Hilbert polynomial $H_K(t) = 1 + Kt + K^2 t^2$.** With $f_\pm(K) = H_K(\pm 1)$ and $f_0(K) = (H_K(1) + H_K(-1))/2$. This is the compactest algebraic statement of the entire shell.

**Parity-overlap angle $\theta_K = \arccos((E-O)/E)$.** At $K=4$: $\theta_4 = \arccos(13/17) \approx 40°$. The structural interpretation of $17/13$ as $\sec\theta_4$ (the secant of the parity-overlap angle between TetA and TetB) is not in the file.

**Norm-form lift $f(K, s) = |K + e^{i\theta}|^2$** for $s = 2\cos\theta$. Algebraic-integer norms of $(K + \zeta_n)$ in $\mathbb{Z}[\zeta_n]$ for $n \in \{3, 4, 6\}$.

**Niven's theorem rigidity check.** Verify that the three integer values $s \in \{-1, 0, +1\}$ are the only rational $s \in [-1, 1]$ for which $f(K, s)$ is a degree-2 cyclotomic polynomial.

### Missing from gravity / μ-partition algebra (AW 05, framework foundations)

**Constitutive law $\mu(x) = x/(x+1)$.** TetA share, TetB share, exchange under $x \leftrightarrow 1/x$.

**Logistic equation $x \frac{d\mu}{dx} = \mu(1-\mu)$.** The differential identity governing the partition.

**Born-rule map $\mu = (1+\cos\theta)/2$.** Connecting the parity-character angle to the gravitational partition.

**Three interior Niven readings.** $s \in \{-1, 0, +1\}$ ↔ $\mu \in \{1/4, 1/2, 3/4\}$ ↔ $x \in \{1/3, 1, 3\}$ ↔ sub-transition, MOND transition, super-transition.

**Permutation discrimination.** For each permutation of $\{21, 17, 13\}$ into (exponent, numerator, denominator), compute $\alpha^{\text{exp}} \cdot \text{num}/\text{den} \cdot g_e/2$ and verify that only $(17/13, \alpha^{21})$ gives an integer exponent against measured $G$.

**SST quadratic** $g^2/(g + a_0) = GM/r^2$ in the spherical static limit. AQUAL identity $\mu = dF/dy$.

### Missing from Maxwell algebra (AW 07)

**$V \otimes V$ decomposition.** $\dim \mathrm{Sym}^2 V = K(K+1)/2$, $\dim \Lambda^2 V = K(K-1)/2$. At $K=4$: $10 \oplus 6 = 16$.

**$F^{\mu\nu}$ as the 6 edges of $K_4$.** Construct the wedge basis, identify time-space edges with $E$ and space-space edges with $B$.

**Three perfect matchings of $K_4$.** Enumerate them; verify they give the self-dual / anti-self-dual decomposition.

**Self-dual / anti-self-dual decomposition.** $F_\pm^{(k)} = (E^k \pm i c B^k)/2$.

**Hodge star action** in 4D Lorentzian, $\ast\ast = -1$ on 2-forms.

**TetA/TetB dual Maxwell** structure: $F_e$ on TetA, $F_m = \ast F$ on TetB, Dirac quantization $e \cdot g = n\hbar c/2$.

**$\alpha^1$ Coulomb step** as the framework's primitive, with explicit identification that gravity's $\alpha^{21}$ is 21 such steps composed via three parity sweeps × seven non-trivial modes.

### Missing from cavity-QED / transition frequency (AW 02)

**$\omega_{K4 \to K5}$ bare carrier.** The framework's identification $\omega = \omega_C = m_e c^2/\hbar$ with per-vertex emission rate $\Gamma = \alpha_G \omega_C$.

**Strong-coupling cavity computation.** Verification that $g\sqrt N \gg \gamma_{\text{cav}}$ at the King's Chamber parameters.

### Missing from topology / WRT (project §03.5–§03.6)

**WRT invariant $\tau_{21}(\Sigma(2,3,5))$.** The Lawrence-Rozansky-Hikami formula evaluated at level 21 on the Poincaré homology sphere. The framework has a complete numerical computation in `/home/claude/cs_calc/` (transcript-referenced) giving $|\tau_{21}| = 8.0962$.

**SU(2)$_{19}$ Chern-Simons.** Level $k = 19$, $k+2 = 21$ representations, $c = 19/7$ central charge.

---

## 3. Recommendation: split the file

The current file works but has three structural problems:

1. **Mixed levels of abstraction.** Foundation algebra (cyclotomic shell, Gram matrix) sits next to apparatus-specific operators (apex collector, well shaft feedback). Reading the file requires holding the entire pyramid context to understand any single function.

2. **Single point of import.** Any code that needs only the cyclotomic shell pulls in the entire pyramid apparatus operators. For algorithmic re-use (e.g., a follow-up paper that uses only the parity-character algebra), this is friction.

3. **Hard to extend.** Adding the gap items from §2 to a 1348-line file would push it past 2000 lines. The recovered/extra block in §16 already shows the file's natural tendency to accrete.

Splitting along the same axes as the project's section structure gives clean separation, easy navigation, and matches the conceptual organization the team is already using.

**Proposed structure:**

```
python/
├── __init__.py              # re-exports the public API
├── constants.py             # ALPHA, G_E_OVER_2, HBAR, C_LIGHT, M_E, G_OBSERVED, TAU
├── cyclotomic.py            # foundation: Φ_n, shell, shift, scale fusion, Niven, norm-form, cyclotomic integers
├── closure_read.py          # T_≤2(V), parity-graded character, projectors, Gram matrix, sec(θ_K), Hilbert polynomial
├── hinge.py                 # K=4↔K=5: Hamiltonians, J_4, intertwiner check
├── gravity.py               # α_G derivation: pentachoron edges, tetrad impedance, four routes, permutation discrimination, G prediction
├── mu_partition.py          # constitutive law: μ(x), Born-rule map, three interior Niven readings, logistic, SST quadratic
├── electromagnetism.py      # F^μν in Λ²V: 6 edges, time/space split, perfect matchings, self/anti-self-dual, dual Maxwell
├── apparatus.py             # pyramid operators: KC vertex, shafts, addresses, mirror M, portal P, Grand Gallery, Z_3, Z_21, coffer, granite, big void, K/Q
├── topology.py              # Hopf/SU(2), A_5, pentachoron, WRT invariant of Σ(2,3,5), SU(2)_19 Chern-Simons
└── predictions.py           # coffer step, relieving chamber, Sierpinski hierarchy, K=2 Schwinger, lepton anchor
```

Ten Python modules + `__init__.py`. Each module is 100–250 lines, focused, importable independently.

**Tests** in a parallel `python/tests/` directory:
- `test_cyclotomic.py` — Φ identities at multiple $K$, shift identity, scale fusion, Niven check
- `test_closure_read.py` — Gram eigenvalues = $\{2E-O, K\}$, $\sec\theta_4 = 17/13$, $H_K(\pm 1)$
- `test_hinge.py` — intertwiner identity $H_5 J_4 = J_4 H_4$
- `test_gravity.py` — $G$ prediction at ppm-level, permutation discrimination uniqueness
- `test_mu_partition.py` — logistic equation, Born-rule round-trip, three interior Niven readings
- `test_electromagnetism.py` — perfect matchings count, self-dual / anti-self-dual decomposition
- `test_topology.py` — WRT invariant against the known $|τ_{21}| = 8.0962$

This makes regression testing tractable and gives reviewers a quick verification path.

---

## 4. Specific additions per module

In addition to the existing content, each new module gets specific additions from the gap list in §2.

### `cyclotomic.py` (additions)

- `niven_rigidity_check()` — verify $s \in \{-1, 0, +1\}$ are the only Niven integers in $[-1, 1]$ with degree-2 $\Phi_n$
- `norm_form_complex(K, theta)` — return $|K + e^{i\theta}|^2$
- `cyclotomic_integer_norm(K, n)` — return $|K + \zeta_n|^2$ for $n \in \{3, 4, 6\}$
- `hilbert_polynomial(K, t)` — return $1 + K t + K^2 t^2$
- `niven_partition_table(K)` — return the three interior Niven readings as a table with $s$, $\theta$, $n$, $\Phi_n(K)$

### `closure_read.py` (new module)

- `truncated_tensor_algebra(K)` — explicit construction of $\mathbf 1 \oplus V \oplus V^{\otimes 2}$
- `parity_projectors(K)` — $P_0, P_1, P_2$ on the three summands
- `graded_identity(K, s)` — $\mathbb{I}_s = P_0 + s P_1 + P_2$
- `gram_matrix_K(K)` — return $\begin{pmatrix} E & E-O \\ E-O & E \end{pmatrix}$
- `gram_eigenvalues(K)` — verify $\{2E-O, K\}$
- `parity_overlap_angle(K)` — return $\theta_K = \arccos((E-O)/E)$
- `sec_theta_K(K)` — return $\sec\theta_K = E/(E-O)$
- `verify_17_over_13_is_sec_theta_4()` — explicit check

### `mu_partition.py` (new module)

- `mu(x)` — $x/(x+1)$
- `tetA_share(x)`, `tetB_share(x)`
- `logistic_identity_check(x)` — verify $x \mu'(x) = \mu(1-\mu)$
- `born_rule_map(theta)` — return $\mu = (1+\cos\theta)/2$
- `inverse_born_rule(mu)` — return $\cos\theta = 2\mu - 1$
- `niven_partition_points()` — return the three interior Niven readings: $\{(s, \theta, \mu, x, \text{regime}, \Phi_n(4)) : s \in \{-1, 0, +1\}\}$
- `mond_transition_check()` — verify $s = 0 \leftrightarrow \mu = 1/2 \leftrightarrow x = 1$ (the MOND transition)
- `sst_quadratic(g, a_0, GM_over_r2)` — verify $g^2/(g + a_0) = GM/r^2$

### `electromagnetism.py` (new module)

- `vv_decomposition(K)` — return $\{\dim \mathrm{Sym}^2 = K(K+1)/2,\, \dim \Lambda^2 = K(K-1)/2,\, \text{total} = K^2\}$
- `tetrahedral_edges(K)` — enumerate the $\binom{K}{2}$ edges of $K_K$
- `F_mu_nu_basis()` — return the 6 wedge-basis elements at $K=4$ with $E$/$B$ identification
- `time_space_edges()` and `space_space_edges()` — return the 3+3 partition
- `perfect_matchings_K4()` — enumerate the three perfect matchings of $K_4$
- `self_dual_part(E_vec, B_vec, c)` — return $F_+^{(k)} = (E^k + icB^k)/2$
- `anti_self_dual_part(E_vec, B_vec, c)` — return $F_-^{(k)} = (E^k - icB^k)/2$
- `hodge_star_lorentzian_2form()` — return the action of $\ast$ on 2-forms with $\ast\ast = -1$
- `dirac_quantization(e_charge, g_charge, n)` — verify $e \cdot g = n \hbar c / 2$
- `coulomb_step()` — return $\alpha^1$, the framework's primitive
- `gravity_as_21_coulomb_steps()` — verify $\alpha_G \propto \alpha^{21}$ = $\alpha^7 \cdot \alpha^7 \cdot \alpha^7$

### `gravity.py` (additions)

- `permutation_discrimination()` — enumerate all six permutations of $\{21, 17, 13\}$ into (exponent, numerator, denominator); return the integer-exponent match
- `sst_static_spherical(g, a_0)` — algebraic version of $\mu(x) g = GM/r^2$
- `aqual_identity_check(y)` — verify $\mu = dF/dy$

### `topology.py` (additions)

- `wrt_invariant_sigma235(level)` — compute $\tau_k(\Sigma(2,3,5))$ at level $k$ using Lawrence-Rozansky-Hikami
- `wrt_at_level_21()` — return $|\tau_{21}| = 8.0962$ as a regression target
- `su2_chern_simons(k)` — return $(k+2, k+1, c = 3k/(k+2))$; verify $k=19$ gives $(21, 20, 19/7)$

---

## 5. Migration plan

If you go with the split:

**Phase 1 (1 session):** Set up `python/` as a package. Create `constants.py`, `cyclotomic.py`, `closure_read.py`, `hinge.py`, `gravity.py`, `apparatus.py`, `topology.py`, `predictions.py`, and `__init__.py` by moving content out of the monolith. Keep the monolith as `_legacy.py` for one cycle. Add `mu_partition.py` and `electromagnetism.py` as new files containing the AW 05 and AW 07 content from §4 above.

**Phase 2 (1 session):** Add `tests/` directory with regression tests against the existing monolith's outputs. Once all tests pass against the new structure, delete `_legacy.py`.

**Phase 3 (1 session):** Add the cyclotomic-integer reading, Niven rigidity, sec(θ_K), and the rest of the gap items from §2. Run all tests.

Total: three working sessions for a clean migration + 200–300 lines of new algebra added.

---

## 6. Alternative: keep monolithic + add new sections

If migration overhead is unwanted, the monolith can absorb the gap items from §2 in new sections §17–§22, putting it around 1800–2000 lines. This is workable but each new addition makes the file harder to navigate, and the conceptual coupling between (e.g.) cyclotomic algebra and apparatus operators stays opaque.

**Recommendation: split.** The framework has matured past the size where a single file is the best home. The split makes the algebra reusable, testable, and matches the project's already-modular markdown structure.

---

## 7. What goes into the project folder regardless

The file is now in place at `python/great_pyramid_portal_algebra_full.py` and runs end-to-end. It is a working artifact regardless of whether we split.

**Decision needed from Stephen:** split into modules (recommended, ~3 sessions of work) or absorb gap items into the monolith (faster but less clean)?

---

**Cross-references:**
- `python/great_pyramid_portal_algebra_full.py` (the file itself)
- All Active Work 01–07 (sources of gap items)
- Project §01 framework foundations through §07 predictions (the conceptual structure the split would mirror)
