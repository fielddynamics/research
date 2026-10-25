# Active Work 05 — Niven's Theorem and the μ(x) Partition

**Status:** Active — structural unification
**Purpose:** Identify the Niven-theorem connection between the parity-character algebra and the GFD gravitational partition $\mu(x) = x/(x+1)$.
**Reading time:** 8 minutes
**Companion:** [04 core theory integration](04_core_theory_integration.md), [03 parity-character upgrade](03_parity_character_upgrade.md), constitutive law / TetA-TetB partition (framework foundations)

---

## 1. Result

The framework's three closure-read parity readings $s \in \{-1, 0, +1\}$ are exactly the three Niven points in the unit interval $|s| \le 1$ at which the polynomial $f(K, s) = K^2 + s K + 1$ is a non-degenerate (degree-2) cyclotomic norm form. Under the Born-rule map $\mu = (1+\cos\theta)/2$, these three readings correspond to three specific values of the gravitational partition $\mu \in \{1/4, 1/2, 3/4\}$, with the middle reading sitting at the MOND transition $g = a_0$ by parity-even = exchange-invariance.

The framework's parity-character algebra and the GFD μ-partition physics are the same structure under this identification.

---

## 2. The Born-rule identification

The GFD partition is a two-occupancy Bernoulli split with exchange symmetry $\mu \leftrightarrow 1 - \mu$ under $x \leftrightarrow 1/x$:

$$\mu(x) = \frac{x}{x+1}, \qquad 1 - \mu(x) = \frac{1}{x+1}, \qquad \frac{\mu}{1-\mu} = x = g/a_0$$

The natural angle-parametrization of a two-occupancy partition is the Born rule:

$$\boxed{\;\mu \;=\; \cos^2(\theta/2) \;=\; \frac{1 + \cos\theta}{2}, \qquad x \;=\; \cot^2(\theta/2) \;=\; \frac{1+\cos\theta}{1-\cos\theta}\;}$$

This has the right symmetry: $\theta \to \pi - \theta$ sends $\cos\theta \to -\cos\theta$, which sends $\mu \to 1-\mu$. The TetA $\leftrightarrow$ TetB exchange is the half-turn $\theta \to \pi - \theta$ on the unit circle.

With the parity-character variable $s = 2\cos\theta$:

$$\mu \;=\; \frac{2 + s}{4}, \qquad x \;=\; \frac{2 + s}{2 - s}$$

---

## 3. Niven's theorem on the unit interval

Niven's theorem: the only rational values of $\cos\theta$ at $\theta \in \pi \mathbb Q$ are $\{0, \pm 1/2, \pm 1\}$, equivalently $2\cos\theta \in \{0, \pm 1, \pm 2\}$.

Restricted to the interval $|s| \le 1$ — where the cyclotomic polynomial $\Phi_n(K)$ associated with the rotation has degree exactly 2 — the integer values are exactly $s \in \{-1, 0, +1\}$. The corresponding rotation orders are $n \in \{3, 4, 6\}$, the only positive integers with $\phi(n) = 2$.

| $s$ | $\cos\theta$ | $\theta$ | Order $n$ | $\Phi_n(K)$ at $K=4$ | $\mu$ | $x = g/a_0$ | Regime |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| $-1$ | $-1/2$ | $2\pi/3$ | $3$ | $\Phi_6(K) = 13$ | $1/4$ | $1/3$ | sub-transition |
| $0$ | $0$ | $\pi/2$ | $4$ | $\Phi_4(K) = 17$ | $1/2$ | $1$ | **MOND transition ($g = a_0$)** |
| $+1$ | $+1/2$ | $\pi/3$ | $6$ | $\Phi_3(K) = 21$ | $3/4$ | $3$ | super-transition |

These three readings are precisely the framework's three closure-read parity traces. Under the Born-rule map, they correspond to three specific gravitational regimes within the open partition interval $\mu \in (0, 1)$.

The gravitational asymptotes $\mu \to 0$ (deep MOND, $x \to 0$) and $\mu \to 1$ (Newtonian, $x \to \infty$) are real physical limits of the partition but are not framework algebraic readings — they sit outside the unit interval where the parity character is non-degenerate, and the closure-read structure does not produce a trace there.

---

## 4. The middle reading sits at the MOND transition

The $s = 0$ trace is the parity-even reading: $\mathrm{Tr}(\mathbb{I}_0) = 17 = \Phi_4(4)$ at $K=4$.

By construction, the parity-even operator is invariant under the exchange $\theta \to \pi - \theta$ (equivalently, $\cos\theta \to -\cos\theta$), so its eigenvalue trace lies at the fixed point of the exchange symmetry. Under the Born-rule map, this fixed point is $\mu = 1/2$, which is $x = 1$, i.e., $g = a_0$ — **the MOND transition**, the Field Origin in framework language.

This identification is structurally forced. The Field Origin's role as the symmetric anchor of TetA/TetB is the algebraic statement that the parity-even trace lies at the partition's exchange-invariant midpoint. Once the Born-rule identification is in place, the location of the middle reading is not a coincidence to be matched but a consequence of exchange symmetry.

---

## 5. The 17/13 ratio reads transition-to-sub-transition

The gravity equation contains the factor $17/13 = \sec\theta_4 = \Phi_4(4)/\Phi_6(4)$. In Niven-partition language:

$$\frac{17}{13} \;=\; \frac{\text{trace at } \mu = 1/2}{\text{trace at } \mu = 1/4}$$

The numerator sits at the MOND transition ($g = a_0$). The denominator sits at the sub-transition ($g = a_0/3$, $\mu = 1/4$). The gravity equation embeds this specific ratio.

The §02.4 permutation discrimination argument established empirically that of the six permutations of $\{21, 17, 13\}$ into $\{\text{exponent, numerator, denominator}\}$, only $(17/13, \alpha^{21})$ gives an integer exponent against measured $G$. The next-best permutation is off by $\sim 10^{-2}$, four orders of magnitude worse.

The Niven-partition reading **explains** the empirically-forced permutation: the chosen ratio reads the parity-symmetric center over the parity-antisymmetric companion (transition over sub-transition), and the chosen exponent reads the parity-positive sweep (super-transition). Each factor in $\alpha_G$ now has a specific Niven-point identification.

---

## 6. The gravity equation in Niven-partition language

Combining §3–§5, the gravity equation:

$$\alpha_G \;=\; \frac{17}{13} \cdot \alpha^{21} \cdot \frac{g_e}{2}$$

has a Niven-partition reading:

$$\alpha_G \;=\; \underbrace{\frac{\text{Tr at MOND transition}}{\text{Tr at sub-transition}}}_{17/13 \,=\, \sec\theta_4} \cdot \underbrace{\alpha^{\text{Tr at super-transition}}}_{\alpha^{21}} \cdot \underbrace{\frac{g_e}{2}}_{\text{Hopf-spin holonomy}}$$

In words: gravity is the trace ratio between the **transition** ($\mu = 1/2$) and **sub-transition** ($\mu = 1/4$) Niven points, attenuated by $\alpha$ raised to the **super-transition** trace ($\mu = 3/4$), modulated by the Hopf-fiber spin holonomy ($g_e/2$).

Three of the four input factors have specific Niven-point identifications in the partition. The fourth ($g_e/2$) sits outside the closure-read parity character; it is the separate Hopf-bundle topological contribution.

This is a substantial reframing. The previous reading was "$(17/13)$ structural ratio × $\alpha^{21}$ three-sweep kernel × $g_e/2$ spin holonomy" — three factors with independent provenance. The Niven-partition reading is: "gravity is the structure encoded by the three interior Niven points of the TetA/TetB partition, each contributing one of the three coupling factors."

---

## 7. Why the asymptotic regimes look like clean theories

The two gravitational asymptotes correspond to limits where the closure-read parity character becomes invisible:

- $\mu \to 1$ ($x \to \infty$, $g \gg a_0$): Newtonian limit. The partition has fully resolved to TetA; there is no two-sheet structure to read; the parity character degenerates. **GR is the asymptotic theory at this limit.**
- $\mu \to 0$ ($x \to 0$, $g \ll a_0$): deep MOND limit. The partition has fully resolved to TetB; same loss of parity character. **Deep MOND is the asymptotic theory at this limit.**

The framework's algebraic content is accessible only on the **open** partition interval $\mu \in (0, 1)$, where both sheets contribute and the parity character is non-degenerate. The three interior Niven points are where this content has its discrete cyclotomic structure.

This is consistent with the historical success of GR (at $\mu \approx 1$) and MOND (at $\mu \approx 0$) as stand-alone theories: each operates in a regime where the GFD closure-read structure is invisible, so each looks complete on its own. The framework's algebraic content lives in the intermediate regimes near and around the MOND transition $g = a_0$ — the band where the three interior Niven points sit.

---

## 8. New testable lines

Two falsifiable predictions follow.

**Look for $\Phi_6(4) = 13$ signatures at $g \approx a_0/3 \approx 4 \times 10^{-11}$ m/s².**

This is the sub-transition Niven point. SPARC galaxy outskirts (and similarly low-acceleration regions in cluster physics) sample exactly this regime. The framework predicts that the parity superdimension trace ($13$ at $K=4$) has a distinguished algebraic role at this acceleration.

**Look for $\Phi_3(4) = 21$ signatures at $g \approx 3 a_0 \approx 3.6 \times 10^{-10}$ m/s².**

The super-transition Niven point. This is the locus where the three-sweep kernel attenuation $\alpha^{21}$ is structurally read in $\alpha_G$. Laboratory torsion balances or low-acceleration probes at this scale would test the framework's identification of $\Phi_3(4) = 21$ as the algebraic content at this regime.

Neither test currently has a dedicated experiment. They are testable predictions the unification makes available.

---

## 9. Framework updates

| Section | Update |
|---|---|
| §01.1 cyclotomic algebra | Add the Born-rule identification mapping the three Niven readings to three partition values $\mu \in \{1/4, 1/2, 3/4\}$. Note: restricted to $|s| \le 1$, where $\Phi_n$ has degree 2. |
| §01.3 graded identity operator | Add: the parity-even reading ($s=0$, trace $17$) is structurally forced to sit at $\mu = 1/2$ by exchange-invariance. |
| §02.2 g-factor breakthrough | Replace "17/13 = structural (cyclotomic)" with the partition reading: trace ratio between the MOND transition and sub-transition Niven points. |
| §02.4 permutation discrimination | The empirically-forced permutation now has a physical interpretation in partition language. Add. |

---

## 10. Open thread

The Born-rule identification $\mu = (1+\cos\theta)/2$ is structurally clean — right exchange symmetry, right interior count, middle reading lands exactly at $g = a_0$ — but it is not currently derived from a deeper framework primitive. The case for it is structural alignment, not first-principles construction.

**The next move that would make this airtight.** Derive the angle $\theta$ as a specific physical parameter — a gauge phase, Wilson-loop holonomy, or internal connection — that simultaneously parametrizes the closure-read parity character AND the TetA/TetB partition. If $\theta$ can be identified with a real geometric quantity in GFD, the Born-rule map is forced; if not, the map remains a structural identification.

This is a single open derivation. It is in scope for a future framework push.

---

**Cross-references:**
- [04 Core theory integration](04_core_theory_integration.md)
- [03 Parity-character upgrade](03_parity_character_upgrade.md)
- [02.4 Permutation discrimination](../02_gravity_derivation/02.4_permutation_discrimination.md)
- [01.3 Graded identity operator](../01_framework_foundations/01.3_graded_identity_operator.md)
