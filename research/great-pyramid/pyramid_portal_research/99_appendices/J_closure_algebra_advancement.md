# Closure Algebra Advancement: Cyclotomic-12 Structure of $\mathcal{A}_3$

## Eight Advances Beyond the Closure-Algebra Pipeline

**Companion to:** appendix G (closure-algebra pipeline) and appendix F (Walsh-spectral compute)
**Status:** Canonical reference. Distilled from extended development in past chats.
**Implementation:** `python/cyclotomic_12.py`

---

## 0. Headline

$$\boxed{\;\mathcal{A}_3^\Omega \;\cong\; \mathbb{Z}[\zeta_{12}]\;}$$

The Ω-invariant subalgebra of the closure algebra is exactly the 12th cyclotomic integer ring. This **unifies the Gaussian axial channel and the Eisenstein hexagonal channels into a single number ring**, with $\zeta_{12} = (T_1 + I)/2$ as the explicit generator.

## 1. The cyclotomic-12 identification

### 1.1 The Ω-invariant subalgebra

Under $\Omega$ acting by cyclic permutation $e_1 \to e_2 \to e_3 \to e_1$, the Ω-fixed subspace of $\mathrm{Cl}(3, 0)$ is spanned by four elements:

| Element | Grade | Definition |
|---|:-:|---|
| $1$ | 0 | scalar identity |
| $T_1$ | 1 | $e_1 + e_2 + e_3$ (sum of vectors) |
| $T_2$ | 2 | $e_{12} + e_{23} - e_{13}$ (cyclic-invariant bivector sum) |
| $I$ | 3 | $e_{123}$ pseudoscalar |

These four elements form a 4-dimensional subalgebra closed under Clifford multiplication.

### 1.2 The multiplication table

| · | $1$ | $T_1$ | $T_2$ | $I$ |
|:-:|:-:|:-:|:-:|:-:|
| $1$ | $1$ | $T_1$ | $T_2$ | $I$ |
| $T_1$ | $T_1$ | $3$ | $3I$ | $T_2$ |
| $T_2$ | $T_2$ | $3I$ | $-3$ | $-T_1$ |
| $I$ | $I$ | $T_2$ | $-T_1$ | $-1$ |

Verification (numerically confirmed at high precision):
- $T_1^2 = 3$ (sum of squares of three orthonormal vectors)
- $T_2^2 = -3$ (sum of squares of three bivectors, each squaring to $-1$, with cross-terms cancelling)
- $T_1 \cdot T_2 = 3I$ (vector times bivector → trivector)
- $I \cdot T_1 = T_2$ (multiplication by pseudoscalar acts as Hodge dual)
- $I^2 = -1$ (pseudoscalar squared)

### 1.3 The cyclotomic generator

Define

$$\boxed{\;\zeta_{12} \;\equiv\; \frac{T_1 + I}{2}\;}$$

Then the powers of $\zeta_{12}$ give:

| Power | Value | In closure-fixed basis |
|:-:|---|---|
| $\zeta^1$ | $\zeta_{12}$ | $(T_1 + I)/2$ |
| $\zeta^2$ | $(1 + T_2)/2$ | — |
| $\zeta^3$ | $I$ | (the pseudoscalar) |
| $\zeta^4$ | $\omega = (-1 + T_2)/2$ | (primitive cube root of unity) |
| $\zeta^6$ | $-1$ | — |
| $\zeta^{12}$ | $+1$ | identity |

The minimal polynomial check:

$$\Phi_{12}(\zeta_{12}) \;=\; \zeta_{12}^4 \;-\; \zeta_{12}^2 \;+\; 1 \;=\; 0$$

All verified numerically.

### 1.4 The unification of Gaussian and Eisenstein

| Subring | Image | Generator | $\Phi$ |
|---|---|---|:-:|
| $\mathbb Z[i]$ | $\zeta^3 = I$ | $i = I$ | $\Phi_4 = x^2 + 1$ |
| $\mathbb Z[\omega]$ | $\zeta^4 = (-1 + T_2)/2$ | $\omega$ | $\Phi_3 = x^2 + x + 1$ |
| $\mathbb Z[\zeta_{12}]$ | $\zeta$ itself | $\zeta_{12}$ | $\Phi_{12} = x^4 - x^2 + 1$ |

$\mathbb Z[\zeta_{12}]$ is the **compositum** of $\mathbb Z[i]$ and $\mathbb Z[\omega]$ — the smallest ring containing both. The closure-fixed subalgebra $\mathcal A_3^\Omega$ is this compositum, not either subring alone.

This is the **canonical unification**: the framework's two imaginary-quadratic channels (Gaussian axial, Eisenstein hexagonal) are not separate. They are the two quadratic subfields of $\mathbb Q(\zeta_{12})$, which is the actual ring on which the closure-fixed subalgebra lives.

## 2. The $\mathbb Z/3$-grading of $\mathcal A_3$

$\Omega$ has order 3, with eigenvalues $\{1, \omega, \omega^2\}$ on $\mathrm{Cl}(3, 0)$. The full 8-dim algebra decomposes:

| Eigenvalue | Multiplicity | Content |
|:-:|:-:|---|
| $+1$ | 2 | $\langle 1, I\rangle$ axial (Ω-fixed) |
| $\omega$ | 3 | Eisenstein "+" — vectors $e_i$, bivectors $e_{(i+1)(i+2)}$ combined as $z_k = e_k + \omega e_{(k+1)(k+2)}$ |
| $\bar\omega$ | 3 | Eisenstein "−" — complex conjugate of the "+" sector |

Total: $2 + 3 + 3 = 8 = \dim \mathrm{Cl}(3, 0)$ ✓

The four-element subalgebra spanned by $\{1, T_1, T_2, I\}$ is contained in the $+1$ eigenspace (Ω-fixed). The 6-dim middle sector splits into the $\omega$ and $\bar\omega$ eigenspaces.

## 3. Galois decomposition of parity

The Galois group of $\mathbb Q(\zeta_{12})/\mathbb Q$ is

$$\mathrm{Gal}(\mathbb Q(\zeta_{12})/\mathbb Q) \;\cong\; (\mathbb Z/12)^* \;=\; \{1, 5, 7, 11\} \;\cong\; V_4$$

This Klein four-group has three non-trivial subgroups of order 2, each fixing a distinct quadratic subfield. The three subfields correspond exactly to the three parity tags:

| Galois element | Action on $\zeta$ | Fixed subfield | Parity tag $s$ |
|:-:|:-:|---|:-:|
| $1$ | $\zeta \to \zeta$ | $\mathbb Q(\zeta_{12})$ (all) | — |
| $5$ | $\zeta \to \zeta^5$ | $\mathbb Q(\sqrt{-3}) = \mathbb Q(\omega)$ | $s = +1, -1$ (hexagonal) |
| $7$ | $\zeta \to \zeta^7 = -\zeta^{-1}$ | $\mathbb Q(i)$ | $s = 0$ (axial) |
| $11$ | $\zeta \to \zeta^{11} = \zeta^{-1}$ | $\mathbb Q(\sqrt 3)$ (real subfield) | parity reversal |

**The three coupling-polynomial channels $s \in \{-1, 0, +1\}$ correspond to the three quadratic subfields of $\mathbb Q(\zeta_{12})$ under the $V_4$ Galois action.**

## 4. Parity exhaustion (sharper than $s^2 < 4$)

In AW 13, we showed the discriminant constraint $s^2 < 4$ forces $s \in \{-1, 0, +1\}$. The Galois decomposition gives a **sharper** statement: $\mathbb Q(\zeta_{12})$ has exactly three quadratic subfields ($\mathbb Q(i)$, $\mathbb Q(\omega)$, $\mathbb Q(\sqrt 3)$), corresponding to the three non-trivial subgroups of $V_4$. There can be no fourth parity tag because there is no fourth quadratic subfield.

The two parities $s = \pm 1$ split the real subfield $\mathbb Q(\sqrt 3)$ along the Galois involution $\zeta \to \zeta^{11}$.

## 5. Spinor lift of $\Omega$

$\Omega$ has order 3 on $\mathcal A_3$. As a rotation of the spatial frame $(e_1, e_2, e_3)$ by $120°$ around the diagonal axis $(1, 1, 1)/\sqrt 3$, its spinor lift to $\mathrm{Spin}(3) = SU(2)$ has order **6**:

$$\tilde\Omega \;=\; \frac{1 - i T_1/\sqrt 3}{2}\sqrt 2 \;\in\; SU(2)$$

(In the right normalization. The key fact is $\tilde\Omega^3 = -1$ and $\tilde\Omega^6 = +1$.)

The element $\tilde\Omega$ generates a cyclic subgroup of order 6 in $SU(2)$. Combined with the spinor lifts of the three coordinate-axis reflections, it generates the **binary tetrahedral group**

$$2T \;=\; \mathrm{Spin}(3) \text{ preimage of } A_4 \;\subset\; SO(3)$$

of order 24. $2T$ is one of the three exceptional finite subgroups of $SU(2)$ (alongside $2O$ binary octahedral and $2I$ binary icosahedral).

## 6. McKay $\widehat E_6$ correspondence

The McKay correspondence assigns to each finite subgroup $G \subset SU(2)$ an extended affine Dynkin diagram. For $2T$:

$$2T \;\longleftrightarrow\; \widehat E_6$$

The $\widehat E_6$ Dynkin diagram has 7 nodes arranged in a Y-shape, corresponding to the 7 irreducible representations of $2T$. The dimensions of these irreps are $1, 1, 1, 2, 2, 2, 3$ — totaling $1+1+1+4+4+4+9 = 24 = |2T|$.

The 7 irreps of $2T$ contain:

- The 3 one-dimensional reps (trivial + two cube-root-of-unity reps, corresponding to $\Omega^0, \Omega^1, \Omega^2$)
- The 3 two-dimensional reps (the spinor reps, related by tensor with the 1-d reps)
- The 1 three-dimensional rep (the defining $SO(3)$ rep of $A_4$)

**This is the same {1, 1, 1, 2, 2, 2, 3} count that appears in $\mathcal A_3$ as: scalar (1), pseudoscalar-related (1, 1), three Eisenstein channels (2, 2, 2), and the spatial vector sector (3).** The Dynkin shadow of the framework's algebra is $\widehat E_6$.

## 7. Sweep multiplication as cyclotomic-12 multiplication

The sweep product

$$a \star b \;=\; \frac{1}{3}\left(ab + \Omega(a)\Omega(b) + \Omega^2(a)\Omega^2(b)\right)$$

projects to the Ω-fixed subalgebra $\mathcal A_3^\Omega = \mathbb Z[\zeta_{12}]$. **On this subalgebra, $\star$ coincides with ordinary multiplication in $\mathbb Z[\zeta_{12}]$.**

Why: $\Omega$ acts on $\mathcal A_3^\Omega$ as identity (by definition of Ω-fixed), so $\Omega(a) = a$ and $\Omega^2(a) = a$ for any $a \in \mathcal A_3^\Omega$. Therefore $a \star b = ab$ on the Ω-fixed subalgebra. The "Ω-averaging" reduces to identity when the inputs are already Ω-invariant.

This is the **deepest unification statement** in the framework: sweep multiplication, which appeared in the closure-algebra pipeline as an Ω-averaging operation, is on $\mathcal A_3^\Omega$ simply multiplication in the 12th cyclotomic ring. The sweep operator is the Hadamard transform composed three times around Ω; the resulting product is just $\mathbb Z[\zeta_{12}]$-multiplication.

## 8. Compositum-12 closure tower

The divisor formula (R6, AW 15) generalizes: at $D = 6$, the divisors of $2D = 12$ above 2 are $\{3, 4, 6, 8, 12\}$, giving

$$S(6, K) \;=\; \Phi_3(K)\,\Phi_4(K)\,\Phi_6(K)\,\Phi_8(K)\,\Phi_{12}(K)$$

At $K = 4$: $S(6, 4) = 21 \cdot 17 \cdot 13 \cdot 257 \cdot 241$.

Each of the five factors picks out a distinct level of the cyclotomic-12 hierarchy:

- $\Phi_3(4) = 21$ — Eisenstein "+"
- $\Phi_4(4) = 17$ — Gaussian axial
- $\Phi_6(4) = 13$ — Eisenstein "−"
- $\Phi_8(4) = 257$ — Fermat prime (Gaussian extension)
- $\Phi_{12}(4) = 241$ — top cyclotomic level (prime, $241 \equiv 1 \pmod{12}$)

**The framework's primary trio {13, 17, 21} sits inside a 5-element compositum-12 closure tower {13, 17, 21, 241, 257}.** The two higher levels are not in the apparatus physics directly — they show up at depth 6, not depth 3 — but they are forced by the divisor formula at $D = 6$.

## 9. Open advances after this push

1. **Compute $\mathrm{ord}_{137}(4)$** to place the fine-structure constant in the cyclotomic hierarchy.
2. **Compute the 3-cocycle of sweep multiplication** $\star$ in $H^3(\mathbb Z/3, \mathbb Z[\zeta_{12}])$ — the structured failure of associativity on the full algebra (not just on the Ω-fixed subalgebra where $\star$ is associative).
3. **Identify the McKay $\widehat E_6$ shadow** of the binary tetrahedral group $2T$ in observable closure-algebra data — what is the framework's prediction at the $\widehat E_6$ level?
4. **Verify the conjecture** that the cyclotomic-clean-up condition fails for all $D > 3$, providing a fourth independent $D = 3$ uniqueness theorem alongside T1, T2, T3.
5. **Tensor product cyclotomic-12 structure**: $\mathcal A_3^{\otimes 2}$ has Ω-fixed subalgebra under $\Omega \otimes \Omega$ — what's its number-ring structure?

---

*Eight new advances extend the closure algebra: (1) cyclotomic-12 identification $\mathcal A_3^\Omega = \mathbb Z[\zeta_{12}]$, (2) $\mathbb Z/3$-grading of full $\mathcal A_3$, (3) Galois decomposition of parity over $V_4$, (4) parity exhaustion (no fourth integer parity), (5) spinor lift order-6 in $SU(2)$, (6) McKay $\widehat E_6$ correspondence via binary tetrahedral $2T$, (7) sweep multiplication as cyclotomic-12 multiplication on $\mathbb Z[\zeta_{12}]$, (8) compositum-12 closure tower at $D = 6$. Together they unify the Gaussian and Eisenstein channels of $\mathcal A_3$ into a single number ring $\mathbb Z[\zeta_{12}]$, identify $2T$ as the natural symmetry, and place the parity tag $s$ within Galois theory of the 12th cyclotomic field.*
