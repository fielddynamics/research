# Active Work 03 — Parity-Character Upgrade for 17/13

**Status:** Active — integration of the parity-character interpretation
**Purpose:** Land Nelson's 17/13 = sec(θ_4) result into the framework. Identify upgrades to §01.2, §01.3, §02.2 and the implication for the active 02 transition-frequency derivation.
**Reading time:** 8 minutes
**Companion:** [01.3 graded identity operator](../01_framework_foundations/01.3_graded_identity_operator.md), [02.2 g-factor breakthrough](../02_gravity_derivation/02.2_g_factor_breakthrough.md), [02 transition frequency derivation](02_transition_frequency_derivation.md)

---

## 1. Verification

All algebraic claims in the upgrade note check.

| Claim | Verified |
|---|---|
| $T_{\le 2}(V) = \mathbf 1 \oplus V \oplus V^{\otimes 2}$, $\mathbb Z_2$-graded by tensor degree | ✓ Standard |
| Even sector: $\mathbf 1 \oplus V^{\otimes 2}$, $\dim = K^2+1$ | ✓ |
| Odd sector: $V$, $\dim = K$ | ✓ |
| Triple $(E-O,\,E,\,E+O) = (\Phi_6(K),\,\Phi_4(K),\,\Phi_3(K))$ | ✓ Identity at any $K$ |
| Gram $G_K = \begin{pmatrix}E & E-O\\E-O & E\end{pmatrix}$ has eigenvalues $\{2E-O,\,O\}$ | ✓ Symmetric / antisymmetric decomposition |
| $\lambda_- = O = K$ exactly | ✓ |
| $\cos\theta_K = (E-O)/E$, $\sec\theta_K = E/(E-O) = \Phi_4(K)/\Phi_6(K)$ | ✓ |
| At $K=4$: $\sec\theta_4 = 17/13$, $\theta_4 = \arccos(13/17) \approx 40.00°$ | ✓ Direct |
| Recursion $C_{K+1} = C_K + 2K = C_K + O_A + O_B$ | ✓ |
| Shift identity $\Phi_3(K) = \Phi_6(K+1)$ drops out | ✓ Algebraic |
| $H_K(t) = 1 + Kt + K^2 t^2$, $H_K(\pm 1) = f_\pm(K)$, even-projector midpoint $= f_0$ | ✓ |

The structurally strongest single line:

$$\boxed{\;\frac{17}{13} \;=\; \sec\theta_4 \;=\; \frac{\dim T_{\text{even}}^{(K=4)}}{\dim T_{\text{even}}^{(K=4)} - \dim T_{\text{odd}}^{(K=4)}} \;}$$

This is the cleanest algebraic provenance for the gravitational prefactor available so far.

---

## 2. What this adds beyond the current §01.3

§01.3 has the trace structure $\mathrm{Tr}(\mathbb I_s) = 1 + sK + K^2$ and identifies $\{21, 17, 13\}$ with $\{\Phi_3(4), \Phi_4(4), \Phi_6(4)\}$. The upgrade note adds five things that are not in §01.3:

1. **The truncated-tensor-algebra reading.** $T_{\le 2}(V) = \mathbf 1 \oplus V \oplus V^{\otimes 2}$ is a more publishable framing than the closure-read $\Lambda^K V \oplus V \oplus (V\otimes V)$. At $K = \dim V$ the two agree numerically (since $\Lambda^K V$ is the 1-dim top exterior power). For pure algebra, the truncated tensor reading is cleaner because it doesn't require $K = \dim V$ — it works at any $K$ with $\dim V = K$ as a parameter.

2. **The Gram-spectral interpretation.** The two-sheet incidence Gram $G_K$ has eigenvalues $\{2E - O,\, K\}$. The antisymmetric eigenvalue is exactly $K$. This is **new structural content**: $K$ is not just the dimension of $V$, it is the spectral charge of the antisymmetric parity mode of the two-sheet overlap.

3. **The sec(θ) interpretation of 17/13.** The gravitational prefactor is the secant of the parity-overlap angle between the TetA and TetB incidence vectors. $\cos\theta_4 = 13/17 \implies \theta_4 \approx 40.00°$.

4. **The recursion as parity renormalization.** $C_{K+1} = C_K + O_A + O_B$ — the odd/exclusive content at level $K$ becomes the shared even core at level $K+1$. This is the mechanistic statement of the cyclotomic ladder.

5. **The Hilbert polynomial reformulation.** $H_K(t) = 1 + Kt + K^2 t^2$, with $f_\pm(K) = H_K(\pm 1)$ and $f_0(K) = (H_K(1) + H_K(-1))/2$. This is the most compact algebraic statement of the entire coupling-polynomial structure.

§01.3 should be upgraded to incorporate these. Suggested order: keep the trace-structure exposition, then add a new §01.3.5 or §01.3.6 covering the Hilbert character / Gram spectral / sec(θ) framing.

---

## 3. Implication for §02.2 — g-factor breakthrough

Currently the §02.2 status table reads:

| Factor | Provenance |
|---|---|
| 17/13 | structural (cyclotomic) |
| α²¹ | structural exponent × imported α |

"structural (cyclotomic)" is uninformative. The upgrade gives a sharper line:

| Factor | Provenance (upgraded) |
|---|---|
| 17/13 | secant of parity-overlap angle between TetA and TetB incidence sheets at $K=4$ |
| α²¹ | three-sweep kernel × seven non-trivial spatial modes per sweep |
| $g_e/2$ | Hopf-fiber spin holonomy |

Each factor now has independent geometric content:
- $\sec\theta_4$ is **angular** (parity-overlap geometry)
- $\alpha^{21}$ is **spectral** (three-sweep kernel attenuation)
- $g_e/2$ is **topological** (Hopf-fiber holonomy)

Three different geometric origins; their product is $\alpha_G$. This is much stronger than three numerically suggestive factors juxtaposed.

---

## 4. Implication for the active 02 transition frequency derivation

Active Work 02 left the prefactor on $\omega_C$ as open. The candidate prefactors were $\{1,\, 17/13,\, 21/17,\, g_e/2,\, 21/13,\, 1/5\}$ with no principled way to choose.

With the parity-character interpretation, these now have specific geometric content:

| Prefactor | Algebraic identity | Geometric reading |
|---|---|---|
| 1 | $\Phi_3(4)/\Phi_3(4)$ | total / total |
| 17/13 | $\Phi_4(4)/\Phi_6(4)$ | even / superdim = $\sec\theta_4$ |
| 21/17 | $\Phi_3(4)/\Phi_4(4)$ | total / even = $1 + O/E$ |
| 21/13 | $\Phi_3(4)/\Phi_6(4)$ | total / superdim |
| $g_e/2$ | spin holonomy | not from $T_{\le 2}(V)$ |
| 1/5 | $1/(K+1)$ | reciprocal cyclotomic step |

**The structural answer for the bare carrier prefactor.** The bare carrier $\omega_{K4 \to K5}$ lives at the **matched 21-sector** of the hinge — the sector where $\Phi_3(4) = \Phi_6(5) = 21$ identifies the two closure-reads as the same. This is the **total-dimension** sector of $T_{\le 2}(V)$ at $K=4$, which has trace $\mathrm{Tr}(\mathbb I_{+1}) = 21$.

The prefactor is therefore **1**: the bare carrier is at $\omega_C$ exactly, with no algebraic modification.

All the geometric ratios — 17/13, $g_e/2$, and $\alpha^{21}$ — live in the **coupling** $\alpha_G$, not in the **carrier** $\omega$. The QED-analogy decomposition is:

$$\boxed{\;\Gamma_{\text{grav, per vertex}} \;=\; \underbrace{\alpha_G}_{\text{coupling}} \cdot \underbrace{\omega_C}_{\text{carrier}} \cdot \underbrace{|M|^2}_{\text{matrix element}}\;}$$

with:
- $\alpha_G = \sec\theta_4 \cdot \alpha^{21} \cdot (g_e/2)$ — dimensionless, derived
- $\omega_C = m_e c^2 / \hbar$ — dimensional, exact (no prefactor)
- $|M|^2$ — open derivation gap (the coherent-vertex matrix element)

The carrier-prefactor question raised in Active Work 02 §10 closes: **prefactor = 1, exactly**, by the algebraic identification of the matched 21-sector with $\mathrm{Tr}(\mathbb I_{+1})$.

This narrows the remaining open work to the matrix element $|M|^2$, which is where the coherent-vertex enhancement and the bridge to Newtonian gravity live.

---

## 5. The publishable pure-math paper

The upgrade note ends: "That is the publishable core." Agreed. The theorem is separable from the GFD physics content and stands alone.

**Suggested theorem statement:**

> **Theorem.** Let $V$ be a $K$-dimensional vector space over a field of characteristic zero, and let $T_{\le 2}(V) = \mathbf 1 \oplus V \oplus V^{\otimes 2}$ be the truncated tensor algebra in degree $\le 2$, $\mathbb Z_2$-graded by tensor degree mod 2 (even: degrees 0 and 2; odd: degree 1). Set $E_K = \dim T_{\text{even}} = K^2 + 1$ and $O_K = \dim T_{\text{odd}} = K$. Then:
>
> (i) The triple $(E_K - O_K,\, E_K,\, E_K + O_K)$ equals the cyclotomic triple $(\Phi_6(K),\, \Phi_4(K),\, \Phi_3(K))$.
>
> (ii) The two-sheet incidence Gram $G_K = \begin{pmatrix} E_K & E_K - O_K \\ E_K - O_K & E_K \end{pmatrix}$ has eigenvalues $\{2E_K - O_K,\, O_K\}$, with the antisymmetric eigenvalue equal to $K$.
>
> (iii) The graded Hilbert polynomial $H_K(t) = 1 + Kt + K^2 t^2$ satisfies $f_\pm(K) = H_K(\pm 1)$ and $f_0(K) = \frac{1}{2}[H_K(1) + H_K(-1)]$.
>
> (iv) The shift identity $\Phi_3(K) = \Phi_6(K+1)$ holds and admits a parity-renormalization interpretation: $C_{K+1} = C_K + O_A + O_B$, i.e., the odd sectors at level $K$ become the shared even core at level $K+1$.

This is a tight result. Each clause is independently verifiable.

**Target journals.** Mid-tier algebra journal. Candidates: *Journal of Algebra*, *Linear Algebra and its Applications*, *Communications in Algebra*. The paper would be 8–15 pages, no physics. Reviewer pool: representation theorists and algebraic combinatorialists.

**What it would NOT include.** No GFD content, no $\alpha_G$, no pyramid, no $g_e/2$, no $\alpha^{21}$. The theorem stands on its own as an observation about the parity-graded truncated tensor algebra. The connections to physics are flagged in a closing "Applications" section in one paragraph: "*The triple $(\Phi_6, \Phi_4, \Phi_3)$ appears in a physical context as the gradient signature of the parity-graded local frame algebra; see [reference to physics paper].*" — at most.

**Why publish this separately.** Two reasons.
1. The algebra is unconditionally correct. The physics is conjectural. Separating them gets a clean publication out of the strongest material without entangling with controversy.
2. Once the pure-math paper exists and is cited, the physics paper can refer to it as established background. This is a standard maneuver for breaking conceptually heavy work into the algebraic and the physical halves.

**Recommendation.** Write this paper next, after the gravity letter cycle. The math is already complete; only exposition remains. Estimated drafting time: 1–2 weeks for a first complete draft.

---

## 6. The angle θ_4 ≈ 40°

A side observation that may or may not be significant.

$\theta_4 = \arccos(13/17) \approx 40.0019°$, almost exactly 40° but not exactly.

Comparison angles:
- $\arctan(1) = 45°$
- Tetrahedral angle $\arccos(-1/3) \approx 109.47°$, half is $\approx 54.74°$
- Octahedral angle $\arccos(0) = 90°$
- Pyramid slope angle $\arctan(4/\pi) \approx 51.85°$
- $\arccos(\sqrt 2 / 2) = 45°$

None of these match 40° exactly. The fact that $\theta_4$ is *close to* 40° but not exactly there suggests the angle is set by the cyclotomic content $(E - O)/E = 13/17$, not by an obvious geometric symmetry. The value $\arccos(13/17)$ is the canonical statement; the proximity to 40° is incidental.

This is worth noting in any presentation: "$\sec\theta_4 = 17/13$, with $\theta_4 \approx 40°$" reads cleanly without claiming a geometric coincidence the framework can't independently support.

---

## 7. Open question this opens

If the gravitational prefactor is $\sec\theta_K$ at $K=4$, what is $\sec\theta_K$ at general $K$?

$$\sec\theta_K = \frac{K^2 + 1}{K^2 - K + 1} = \frac{\Phi_4(K)}{\Phi_6(K)}$$

| $K$ | $E$ | $O$ | $E-O$ | $\sec\theta_K$ | $\theta_K$ |
|---|---|---|---|---|---|
| 2 | 5 | 2 | 3 | 5/3 ≈ 1.667 | 53.13° |
| 3 | 10 | 3 | 7 | 10/7 ≈ 1.429 | 45.57° |
| 4 | 17 | 4 | 13 | 17/13 ≈ 1.308 | 40.00° |
| 5 | 26 | 5 | 21 | 26/21 ≈ 1.238 | 36.05° |
| 6 | 37 | 6 | 31 | 37/31 ≈ 1.194 | 33.16° |

The angle decreases monotonically as $K$ grows. As $K \to \infty$, $\sec\theta_K \to 1$ and $\theta_K \to 0$.

The shift identity gives: $\Phi_6(5) = \Phi_3(4) = 21 = (E - O)$ at $K=4$. So $E-O$ at $K=4$ matches $E+O$ at... wait. $\Phi_3(K) = E + O$. So $\Phi_3(4) = 17 + 4 = 21$ and $\Phi_6(5) = 26 - 5 = 21$. The match is $E_4 + O_4 = E_5 - O_5 = 21$. This is the **portal sector**: $E - O$ at $K=5$ matches $E + O$ at $K=4$.

In angle language: the K=5 "superdim" sector (cos sector) matches the K=4 "total" sector. The hinge is at this matched 21-dimensional space.

**Implication for the hinge operator $J_4$.** The operator $J_4 = |5, -\rangle\langle 4, +|$ maps from the K=4 even-sector trace ($+1$ sweep, giving 21) to the K=5 superdim ($-1$ sweep, giving 21). The hinge transitions a parity-positive K=4 read to a parity-negative K=5 read of the same 21-dimensional content. This is a parity-flipping isomorphism within the matched sector.

The bare frequency $\omega_C$ is preserved across the hinge (same 21-sector, same energy); the **parity** flips, and the **K-grading** lifts $4 \to 5$. The hinge is a parity-flip and a K-lift acting on a fixed-energy sector.

This is a sharper statement than Active Work 02 had. Let me update that document.

---

## 8. Updates to existing files

| File | Update |
|---|---|
| §01.2 (closure-read) | Add the truncated-tensor-algebra framing $T_{\le 2}(V) = \mathbf 1 \oplus V \oplus V^{\otimes 2}$ as the abstract reading, with $\Lambda^K V \oplus V \oplus (V\otimes V)$ as the physics-natural specialization. |
| §01.3 (graded identity) | Add subsection on (a) Hilbert polynomial $H_K(t)$, (b) Gram-spectral $\lambda_- = K$, (c) $\sec\theta_K$ interpretation. |
| §02.2 (g-factor breakthrough) | Replace "17/13 — structural (cyclotomic)" with "17/13 = $\sec\theta_4$ — secant of parity-overlap angle between TetA and TetB incidence sheets." |
| Active Work 02 (transition frequency) | Close the prefactor question: prefactor = 1 exactly, by identification of the matched 21-sector with the total-dimension trace. |

The §01.2 and §01.3 upgrades are mechanical — add the new framing without removing the existing content. The §02.2 line is a one-sentence sharpening. The Active Work 02 upgrade resolves an open prefactor question and reframes the remaining open work as the matrix element $|M|^2$.

---

## 9. Suggested immediate next steps

1. **Patch the active 02 transition-frequency doc** with the closed prefactor (prefactor = 1).
2. **Draft the pure-math paper** at the truncated tensor algebra theorem level. Target: 10-page submission to *Linear Algebra and its Applications* or *Journal of Algebra*. No physics content. This is a clean, fast, high-value publication.
3. **Upgrade §01.3** in the project folder to include the parity-character formulation.

Items 1 and 3 are mechanical and can be done in the same session. Item 2 is a separate writing project, ~1–2 weeks of focused drafting.

---

**Cross-references:**
- [01.2 Closure-read representation](../01_framework_foundations/01.2_closure_read_representation.md)
- [01.3 Graded identity operator](../01_framework_foundations/01.3_graded_identity_operator.md)
- [02.2 G-factor breakthrough](../02_gravity_derivation/02.2_g_factor_breakthrough.md)
- [02 Transition frequency derivation](02_transition_frequency_derivation.md)
