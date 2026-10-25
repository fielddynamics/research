# Active Work 04 — Core Theory: Independent Integration

**Status:** Active — verification, integration, and independent contribution
**Purpose:** Process the exact-sequence / norm-form / scale-fusion upgrade. Add three independent results that fall out: Niven's-theorem rigidity, the cyclotomic-integer reading, and the K → K² scale-fusion ladder's physical meaning.
**Reading time:** 12 minutes
**Companion:** [03 parity-character upgrade](03_parity_character_upgrade.md), [01.1 cyclotomic algebra](../01_framework_foundations/01.1_cyclotomic_algebra.md), [01.4 shift identity](../01_framework_foundations/01.4_shift_identity_proof.md)

---

## 1. Verification

All seven claims in the new note check.

| Claim | Verified |
|---|---|
| Equal-step ladder $E_K - C_K = U_K - E_K = K$ | ✓ at $K=2,...,6$: steps $\{2,3,4,5,6\}$ |
| Exact sequence $0 \to C_K \to A_K \oplus B_K \to C_{K+1} \to 0$ with $C_{K+1} = 2E_K - C_K$ | ✓ Mayer-Vietoris dim count |
| Pushout-recursion $C_{K+1} = U_K$ | ✓ The shift identity drops out of the pushout |
| Norm form $f(K, s) = N(K + e^{i\theta})$ for $s = 2\cos\theta$ | ✓ Direct: $|K + e^{i\theta}|^2 = K^2 + 2K\cos\theta + 1$ |
| Three canonical angles $\theta \in \{\pi/3, \pi/2, 2\pi/3\}$ give rotations of orders $\{6, 4, 3\}$ | ✓ |
| **Theorem 5: scale fusion** $\Phi_3(K) \Phi_6(K) = \Phi_3(K^2)$ | ✓ at $K=2,...,10$ |
| At $K=4$: $\Phi_3(4) \Phi_6(4) = 21 \cdot 13 = 273 = \Phi_3(16)$ | ✓ |

The scale-fusion identity is a known cyclotomic fact ($x^6 - 1 = (x^2 - 1)\Phi_3(x^2)$ vs. $(x-1)(x+1)\Phi_3(x)\Phi_6(x)$), but its appearance in this framework as a **multiplicative scale ladder** is non-trivial — see §4 below.

---

## 2. Independent contribution: Niven's theorem makes the framework's three readings forced

The note proposes the continuous lift $s = 2\cos\theta$. This is more than parametrization; it imposes a rigidity result.

**Niven's theorem (1956):** The only rational values of $\cos\theta$ for which $\theta$ is a rational multiple of $\pi$ are $\{0, \pm 1/2, \pm 1\}$.

Equivalently: the only rational values of $2\cos\theta$ with $\theta/\pi \in \mathbb{Q}$ are $\{0, \pm 1, \pm 2\}$.

Restricting to $s \in [-1, 1]$ (the range where $\theta \in [\pi/3, 2\pi/3]$ — the "middle band" of the unit circle):

$$s \in \{-1,\, 0,\, +1\}$$

These three values are the **only** rational $s$ in this interval that correspond to finite-order rotations. The corresponding orders are:

| $s$ | $\theta$ | Rotation order $n$ | $\phi(n)$ |
|---|---|---|---|
| $-1$ | $2\pi/3$ | 3 | 2 |
| $0$ | $\pi/2$ | 4 | 2 |
| $+1$ | $\pi/3$ | 6 | 2 |

The orders $n \in \{3, 4, 6\}$ are **exactly the integers for which Euler's totient $\phi(n) = 2$** — i.e., the only $n$ for which the cyclotomic polynomial $\Phi_n$ has degree 2.

**Consequence.** The framework's three discrete readings $s \in \{-1, 0, +1\}$ are not chosen. They are **forced** by the conjunction of two conditions:

1. The reading must correspond to a finite-order rotation (algebraic, not transcendental phase).
2. The reading must lie in the parity-character range $|s| \le 1$.

Outside this range there are integer values $s = \pm 2$ (corresponding to $\theta \in \{0, \pi\}$, trivial rotations), but these give the squared polynomials $(K \pm 1)^2$, not cyclotomic polynomials of degree 2.

**The strongest statement.** "The framework reads the parity-graded trace at the three integer points of the unit interval $|s| \le 1$ where the phase $e^{i\theta}$ is a primitive root of unity of an order $n$ with $\phi(n) = 2$, i.e., $n \in \{3, 4, 6\}$. These are the only finite-order rational readings available with non-degenerate (degree-2) cyclotomic polynomial."

This converts the three-reading structure from "design choice" to "Niven-forced." It is the strongest available rigidity argument for the discrete reading.

---

## 3. Independent contribution: the cyclotomic-integer reading

The norm-form $f(K, s) = |K + e^{i\theta}|^2$ at cyclotomic $\theta$ has a cleaner algebraic identity.

At each of the three canonical $\theta$ values, $K + e^{i\theta}$ is an element of a specific ring of cyclotomic integers:

| $\theta$ | Element | Ring | Norm at $K=4$ |
|---|---|---|---|
| $2\pi/3$ | $4 + \zeta_3$ | $\mathbb Z[\zeta_3]$ (Eisenstein) | $\mathrm N(4 + \zeta_3) = 13$ |
| $\pi/2$ | $4 + i$ | $\mathbb Z[i]$ (Gaussian) | $\mathrm N(4 + i) = 17$ |
| $\pi/3$ | $4 + \zeta_6$ | $\mathbb Z[\zeta_6] = \mathbb Z[\zeta_3]$ | $\mathrm N(4 + \zeta_6) = 21$ |

where $\zeta_n = e^{2\pi i/n}$ is the primitive $n$-th root of unity.

The shell $(13, 17, 21)$ is the triple of norms of the three "K-translates" $\{K + \zeta_3, K + i, K + \zeta_6\}$ in their respective rings.

**Stronger framing than the polynomial reading.**

- Polynomial reading: "$\Phi_n(K)$ for $n \in \{3, 4, 6\}$"
- Cyclotomic-integer reading: "$\mathrm N(K + \zeta_n)$ for $n \in \{3, 4, 6\}$, the only $n$ with $\phi(n) = 2$"

The second is more powerful because:
- It exposes the algebraic-integer structure: $13, 17, 21$ are norms of specific algebraic integers, not just polynomial values.
- It identifies the rings: two of them ($\zeta_3$ and $\zeta_6$) live in the same Eisenstein ring $\mathbb Z[\zeta_3]$; the middle one ($i$) lives in the Gaussian ring $\mathbb Z[i]$.
- The shell is therefore a **mixed-ring norm triple**: Eisenstein, Gaussian, Eisenstein.

This connects to the existing §01.1 work on $\mathbb Q(\zeta_{21}) = \mathbb Q(\zeta_3) \otimes \mathbb Q(\zeta_7)$. The closure-read shell at $K=4$ lives entirely in the degree-2 cyclotomic fields $\mathbb Q(\zeta_3)$ and $\mathbb Q(\zeta_4) = \mathbb Q(i)$. The $\zeta_7$ ladder (the Grand Gallery's seven-step cyclotomic phase) is a separate structure that doesn't appear in this shell.

**Why this matters.** The earlier framework framing "K=4 closure-read total $= 21 = 3 \times 7$" tied 21 to the Z_3 × Z_7 factorization. The cyclotomic-integer reading shows: the **same 21 also arises** as $\mathrm N(K + \zeta_6) = K^2 + K + 1$, with $K = 4$. The two readings of 21 are:

- $21 = 3 \times 7$ (Antechamber Z_3 × Gallery Z_7) — apparatus reading
- $21 = \mathrm N(4 + \zeta_6) = (4 + \zeta_6)(4 + \bar\zeta_6)$ — closure-read reading

These two readings of 21 are not algebraically equivalent. They are two different structural interpretations of the same integer. The framework currently uses both (the first in §04.5–04.6, the second in §02.2 via the 17/13 prefactor); a clean treatment should make this dual reading explicit, with the two interpretations being two different factorizations of $21$.

---

## 4. Independent contribution: scale fusion's physical interpretation

Theorem 5 says $\Phi_3(K) \Phi_6(K) = \Phi_3(K^2)$. At $K = 4$:

$$\underbrace{21}_{\Phi_3(4)} \cdot \underbrace{13}_{\Phi_6(4)} \;=\; \underbrace{273}_{\Phi_3(16)}$$

This is a ladder $K \to K^2$. The K=16 closure-read total dimension is the product of the K=4 total and superdimension.

**The structural identification.** The K=16 closure-read $\mathcal{C}_{16}$ has total dimension $273$. It is generated by a 16-dimensional vector space. The most natural such space in the framework is $V \otimes V$ at $K = 4$ (which has dimension exactly 16).

If we take $W = V \otimes V$ at $K=4$ as the "second-order generator," and form its closure-read:

$$\mathcal{C}_{16}^{(W)} \;=\; \mathbf 1 \oplus W \oplus W \otimes W \;=\; \mathbf 1 \oplus (V \otimes V) \oplus (V \otimes V) \otimes (V \otimes V)$$

with dimension $1 + 16 + 256 = 273$, exactly $\Phi_3(16)$.

**This is the "second closure."** The closure-read at K=16 is the closure-read of the tensor-square sector of the closure-read at K=4. Scale fusion is the algebraic statement of this nested closure.

**Why this matters.** The framework's existing apparatus has a clear K=4 vertex (the King's Chamber) and a clear K=5 hinge (the K=4 ↔ K=5 lift). The K=16 sector is **not currently identified with any physical structure** in the apparatus.

But the spectral compute work has a clean K=16 target: 16-dimensional Walsh-Hadamard at $N = 4$ ($H_{16}$ is the $2^4 \times 2^4$ Hadamard matrix), which is exactly the order that appears in WCEM N=12 chunked architectures. The scale-fusion ladder gives a candidate algebraic spine: each WCEM chunk at $N=4$ is a K=16 closure-read of dimension 273, sitting above a K=4 closure-read of dimension 21.

**Open question.** Does the spectral compute architecture's natural chunking (16-dimensional Walsh blocks composing 4-dimensional Walsh blocks) realize the K=4 → K=16 scale-fusion algebraically? If yes, that's a structural link between the apparatus (K=4 closure at the King's Chamber) and the compute substrate (K=16 closure at the WCEM block level).

This is worth checking. The empirical work on the chunked WCEM at N=48 outperforming MLP by 2.8× would gain an algebraic explanation if the chunks realize the scale-fusion ladder.

---

## 5. Independent contribution: what is $\theta$ physically?

The note frames $s = 2\cos\theta$ as the "trace of an internal phase rotation on the odd sector." Three canonical values give the three cyclotomic readings. The natural follow-up: what is $\theta$ in a physical realization?

**Three candidates.**

**(A) A gauge angle.** If the closure-read carries an internal U(1) gauge structure on the odd sector ($V$), then $\theta$ is a gauge phase. The Niven-quantized values $\theta \in \{\pi/3, \pi/2, 2\pi/3\}$ would correspond to specific gauge fixings (Lorenz, axial, temporal — or some other triple). The framework would acquire a gauge symmetry it doesn't currently have explicitly.

**(B) A Wilson-loop phase.** If $\theta$ is the phase accumulated by an internal mode traversing a closed loop in some auxiliary space, the three canonical values correspond to loops of orders 6, 4, 3 (winding numbers). The Grand Gallery's 6π phase accumulation (§04.5: cumulative $\sum 2\pi k/7$ for $k=0..6$) gives $\theta = 6\pi$, which lands at $s = 2\cos(6\pi) = 2$ — outside the parity range.

**(C) A Berry phase / holonomy.** If $\theta$ is the holonomy of a connection on a parameter space, the three canonical values correspond to three specific holonomy classes. The $g_e/2$ factor entering $\alpha_G$ has been identified in the framework as Hopf-fiber spin holonomy (§02.2). Whether $\theta$ relates to this holonomy or to a distinct internal one is open.

**Which is right?** The framework currently does not commit. The cleanest move is to leave $\theta$ as a formal parameter at the algebraic level and identify its physical realization separately. The strongest statement available now: "$\theta$ is a continuous parameter whose Niven-quantized values reproduce the framework's three discrete readings. Its physical realization is open."

**A specific testable prediction.** If $\theta$ is a continuous gauge parameter and the apparatus tunes it (e.g., via the geomagnetic pump or the Hopf-spin coupling), then off-Niven values of $\theta$ should produce **non-cyclotomic** traces — irrational values that would show up as anomalous mode spectra. The Z_21 acoustic prediction in §07.1 assumes $\theta$ at $\pi/3$ (s = +1, giving the 21-mode comb). At an off-resonance pump, the comb would shift continuously. **This is a falsifier:** if the chamber spectrum is exactly the Z_21 comb regardless of pump frequency, $\theta$ is locked at $\pi/3$ by some mechanism. If the comb shifts with pump frequency, $\theta$ is a free continuous parameter.

This is a sharpened version of the §07.1 acoustic test.

---

## 6. Where these results land in the framework

| Section | Update needed |
|---|---|
| §01.1 cyclotomic algebra | Add: (a) Niven's theorem rigidity result; (b) cyclotomic-integer reading $\mathrm N(K + \zeta_n)$; (c) Theorem 5 scale fusion $\Phi_3(K)\Phi_6(K) = \Phi_3(K^2)$. |
| §01.2 closure-read | Add the truncated tensor algebra reading $T_{\le 2}(V)$ from Active Work 03. |
| §01.3 graded identity | Add the Gram-spectral and Hilbert-polynomial framings from Active Work 03. |
| §01.4 shift identity proof | Add the pushout derivation: $C_{K+1} = U_K$ from the Mayer-Vietoris exact sequence. The shift identity drops out of the pushout. |
| §02.2 g-factor breakthrough | Replace "17/13 — structural" with "17/13 = $\sec\theta_4$ = ratio of Gaussian-integer norm to Eisenstein-integer norm at $K=4$." |
| §04.5 Grand Gallery kernel | Check whether the Grand Gallery's 6π phase accumulation lives on the same $\theta$-circle as the Niven points. Probably no — but worth confirming. |
| §07.1 acoustic Z_21 spectrum | Add the sharpened falsifier: if the comb shifts with pump frequency, $\theta$ is continuous; if it's locked at Z_21, $\theta$ is fixed at $\pi/3$. |
| §08 open questions | Add: "physical realization of $\theta$" as a new top-tier open question. |

Three sections (§01.1, §01.4, §07.1) get genuinely new content. Five sections get refinement.

---

## 7. Pure-math paper — updated structure

With the additions from this document, the pure-math paper grows from the 6-theorem skeleton in the note to an 8-theorem structure. Suggested:

> **Theorem 1 (Graded tensor shell).** $T_{\le 2}(V) = \mathbf 1 \oplus V \oplus V^{\otimes 2}$ at $\dim V = K$ has parity-graded shell $\mathcal{C}_K = (K^2 - K + 1,\, K^2 + 1,\, K^2 + K + 1)$.
>
> **Theorem 2 (Parity-pushout realization).** Two parity sheets $A_K, B_K$ with $|A_K| = |B_K| = K^2 + 1$ and $|A_K \cap B_K| = K^2 - K + 1$ realize the shell as $(|A \cap B|,\, |A|,\, |A \cup B|)$, and $A_K \cup_{C_K} B_K = C_{K+1}$.
>
> **Theorem 3 (Cyclotomic identification).** $\mathcal{C}_K = (\Phi_6(K),\, \Phi_4(K),\, \Phi_3(K))$.
>
> **Theorem 4 (Adjacent-shell morphism).** $\Phi_3(K) = \Phi_6(K+1)$, and this is the pushout identity from Theorem 2.
>
> **Theorem 5 (Scale fusion).** $\Phi_3(K) \cdot \Phi_6(K) = \Phi_3(K^2)$.
>
> **Theorem 6 (Geometry corollaries).** $\Phi_3(q) = |\mathbb P^2(\mathbb F_q)|$ for prime powers $q$, and $\Phi_3(K) - 1 = 2\binom{K+1}{2}$.
>
> **Theorem 7 (Norm-form lift).** For $s = 2\cos\theta$, $f(K, s) = \mathrm N_{\mathbb Q(e^{i\theta})/\mathbb Q}(K + e^{i\theta})$, recovering the three cyclotomic values at the three rotation angles of orders $3, 4, 6$.
>
> **Theorem 8 (Niven rigidity).** The integer values $s \in \{-1, 0, +1\} \subset [-1, 1]$ are the only rational $s$ in $[-1, 1]$ for which $s = 2\cos\theta$ has $\theta \in \pi \mathbb Q$, equivalently the only finite-order rotational readings. They correspond to the three positive integers $n$ with $\phi(n) = 2$.

This is a much stronger paper than the 6-theorem version. The Niven rigidity result in particular is the kind of finishing move that a pure-math reviewer will appreciate: it converts a "natural choice" into a "forced result."

**Suggested title:** *"The parity character of the truncated tensor algebra: a cyclotomic and Niven-rigid shell structure."*

**Target journal.** *Journal of Algebra* (preferred for the algebraic depth), or *Linear Algebra and its Applications* (faster, broader audience). Length: 12–15 pages with the Niven section.

---

## 8. The single sentence

If the entire upgraded structure had to be compressed to one sentence:

> The parity-graded truncated tensor algebra $T_{\le 2}(V)$ at $\dim V = K$ produces a shell of three traces $(\Phi_6(K),\, \Phi_4(K),\, \Phi_3(K))$ realized as norms $\mathrm N(K + \zeta_n)$ in the three cyclotomic rings of degree 2 ($n \in \{3, 4, 6\}$, the unique $n$ with $\phi(n) = 2$, equivalently the Niven-rigid integer readings of $2\cos\theta$ in $[-1, 1]$), with a pushout-recursion $C_{K+1} = U_K$ that lifts the shell at level $K$ to the shell at level $K+1$ and a scale-fusion identity $\Phi_3(K)\Phi_6(K) = \Phi_3(K^2)$ that lifts level $K$ to level $K^2$.

That sentence is the entire base of the core theory.

---

## 9. What's still open after this integration

Three open items, in priority order:

1. **The physical realization of $\theta$.** Active gauge parameter? Wilson-loop phase? Holonomy? The cleanest realization would unify Active Work 02's pump-dressed picture with the parity character: the pump tunes $\theta$, and the Niven-quantized values are where the closure-read locks in.

2. **The scale-fusion $K=4 \to K=16$ physical realization.** Does the WCEM N=4 chunk realize the K=16 closure-read? This is the cleanest place to test whether the algebraic ladder has a substrate.

3. **Whether $\theta$ and the Hopf-spin holonomy $g_e/2$ are independent.** The framework currently treats $g_e/2$ as a separate Hopf-fiber holonomy. If $\theta$ is also a holonomy, are they the same one or distinct? Cleanest test: write the full closure-read with explicit $\theta$ and $g_e/2$ parameters and check whether the gravity equation $\alpha_G$ separates them.

These are the three items the framework hasn't closed and that the next push could meaningfully address.

---

## 10. Recommendation

The pure-math paper is now ready to draft. The structure is set, the eight theorems are proved (Theorems 1–6 by elementary algebra, Theorem 7 by computation, Theorem 8 by Niven). The paper's value is genuinely independent of the GFD physics — it stands as a contribution to combinatorial algebra / cyclotomic field theory in its own right.

**Action.** Move to drafting. Two weeks of focused writing should produce a submission-ready paper. The GFD physics work continues in parallel; the pure-math paper is a sidestream that gets a clean result published while CQG cycles.

The three Active Work documents (01 coffer, 02 transition frequency, 03 parity-character upgrade, plus this 04) now form a coherent push: a sharp empirical test, a closed theoretical gap, an algebraic upgrade, and a publishable theorem package. That's a useful working state.

---

**Cross-references:**
- [03 Parity-character upgrade](03_parity_character_upgrade.md)
- [02 Transition frequency derivation](02_transition_frequency_derivation.md)
- [01.1 Cyclotomic algebra](../01_framework_foundations/01.1_cyclotomic_algebra.md)
- [01.4 Shift identity proof](../01_framework_foundations/01.4_shift_identity_proof.md)
- [07.1 Acoustic Z_21 spectrum](../07_predictions_and_tests/07.1_acoustic_Z21_spectrum.md)
