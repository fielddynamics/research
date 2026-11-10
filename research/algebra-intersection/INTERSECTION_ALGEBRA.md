# The Intersection Algebra

*The coupling polynomial, the constitutive law, the closure operator and the torsion sector as one modular group*

**Status:** derived and checked. Every claim below is tested by [`verify_intersection.py`](verify_intersection.py) (63/63 PASS), and so is the one hypothesis that turned out false.
**Depends on:** [`algebraic_pipeline_of_reality.md`](../../papers/algebraic-papers-a-b-c/algebraic_pipeline_of_reality.md), [`01.1_cyclotomic_algebra.md`](../exploratory/great-pyramid/pyramid_portal_research/01_framework_foundations/01.1_cyclotomic_algebra.md), [Appendix J](../exploratory/great-pyramid/pyramid_portal_research/99_appendices/J_closure_algebra_advancement.md), [`tbit_algebra.md`](../quantum%20compute/t-bit%20algebra/tbit_algebra.md), [`proofs/torsion-regular-representation`](../../proofs/torsion-regular-representation/)

---

## 0. Headline

The framework builds its algebra in five separate places:

| Layer | Object | Where it lives |
|---|---|---|
| Coupling polynomial | $f(K,s) = 1 + sK + K^2 \to 21, 17, 13$ | `llms.txt`, `01.1_cyclotomic_algebra.md` |
| Closure algebra | $\mathrm{Cl}(3,0)$, closure operator $\Omega$, axial half $\langle 1, I, d, Id\rangle$ | pipeline, Appendix J |
| t-bit gates | Möbius maps on $x$: $P(x) = 1/x$, $T_\lambda$, $D_\alpha$, $s(x) = (x-1)/(x+1)$ | `tbit_algebra.md` |
| Constitutive law | $\mu(x) = x/(x+1)$, $\mu(x) + \mu(1/x) = 1$ | `proofs/constitutive-law-exchange-symmetry` |
| Torsion sector | 24 components $\cong$ regular representation of $S_4$ | `proofs/torsion-regular-representation` |

They have been treated as parallel readings of one geometry. They are in fact **one group acting on one curve**:

$$\boxed{\;\mathrm{PSL}_2(\mathbb Z/4\mathbb Z) \;\cong\; S_4 \;=\; \langle\, S,\ ST,\ T \;\mid\; S^2 = (ST)^3 = T^4 = 1 \,\rangle \;=\; \Delta(2,3,4)\;}$$

| Generator (mod 4) | Order | Characteristic polynomial in $\mathrm{SL}_2(\mathbb Z)$ | Framework object |
|---|:-:|---|---|
| $S = \begin{psmallmatrix}0&-1\\1&0\end{psmallmatrix}$ | 2 | $\det(K - S) = K^2 + 1 = \Phi_4(K)$ | Field Origin, **17** |
| $ST$, $(ST)^2$ | 3 | $\Phi_6(K)$, $\Phi_3(K)$ | TetB **13**, TetA **21** |
| $T \sim L = \begin{psmallmatrix}1&0\\1&1\end{psmallmatrix}$ | **4 = K** | $(K-1)^2$ | the constitutive law $\mu(x) = x/(x+1)$ |

and the curve this group acts on, the level-4 modular curve $X(4)$, *is* the stellated octahedron:

| Points of $X(4)$ over $X(1)$ | Count | Stabiliser | Stellated octahedron |
|---|:-:|:-:|---|
| cusps (over $\infty$) $= \mathbb P^1(\mathbb Z/4)$ | 6 | $\mathbb Z_4$ | vertices of the octahedral core |
| elliptic points over $i$ | 12 | $\mathbb Z_2$ | edges |
| elliptic points over $\rho = e^{2\pi i/3}$ | 8 | $\mathbb Z_3$ | the 8 tips (cube corners), **2-coloured 4 + 4 into TetA and TetB** by the sign character of $S_4$ |
| generic fibre | 24 | 1 | a regular $S_4$-set, the same representation as the 24 torsion components |

Riemann–Hurwitz gives genus 0: $X(4)$ is a sphere tiled as an octahedron (Klein, 1878). That classical fact is not new. What is new is that the framework's objects, derived separately, line up with its pieces: the evaluation point $K = 4$ of the polynomial is the **level** of the modular curve, and it is also the **order** of the constitutive law.

---

## 1. The spinor norm form

Realise $\mathrm{Cl}(3,0)$ by Pauli matrices, with reversion $X \mapsto \tilde X$. Let $d = e_1 + e_2 + e_3$ and let

$$R = \tfrac12\,(1 - I d)$$

be the rotor for $120^\circ$ about the body diagonal. Then:

1. $\mathrm{Ad}_R$ is the closure operator: $R e_i \tilde R = e_{i+1}$. So $\Omega$ is not an extra structure. It is conjugation by an element of its own fixed (axial) subalgebra.
2. $R^3 = -1$ and $R^6 = 1$: $R$ has order 6 and $-R$ has order 3, while $I^2 = -1$ gives order 4.
3. Define the **spinor norm form** $\mathcal N_K(X) = (K - X)(K - X)^\sim$. Then

$$\mathcal N_K(-R) = \Phi_3(K),\qquad \mathcal N_K(I) = \Phi_4(K),\qquad \mathcal N_K(R) = \Phi_6(K),$$

each a scalar, so $21, 17, 13$ at $K = 4$. All three structural states are norms of $K$ minus the closure rotor, the pseudoscalar, or minus the rotor.

4. **Degree-2 exhaustion, read in the algebra.** For the order-12 element $\zeta_{12} = (d + I)/2$ of Appendix J, $\mathcal N_4(\zeta_{12})$ is *not* a scalar; a second norm is needed, giving $\Phi_{12}(4) = 241$. The states $s \in \{-1, 0, +1\}$ are exactly the roots of unity whose spinor norm is already a scalar.

5. **Pole splitting.** Over $\mathbb R$ the axial algebra splits as $\mathbb C \oplus \mathbb C$ through the idempotents $P_\pm = \tfrac12(1 \pm d/\sqrt3)$. These are the Bloch projectors onto the corners $(+,+,+)$ and $(-,-,-)$, one apex of each tetrahedron. The rotor projects to $R P_\pm = e^{\mp i\pi/3} P_\pm$: the two apices see complex-conjugate sixth roots of unity.

## 2. The spin-sheet theorem

For every unit quaternion (rotor) $q$ with real part $a$:

$$\frac{\mathcal N_K(q) + \mathcal N_K(-q)}{2} = K^2 + 1 = \Phi_4(K), \qquad \mathcal N_K(-q) - \mathcal N_K(q) = 4Ka.$$

With $|2a| = 1$ the difference is $2K = 8 = 2^D$, the framework's "range". The map $q \mapsto -q$ is the kernel of $\mathrm{Spin}(3) \to SO(3)$, and it sends $s \mapsto -s$, $\Phi_3 \leftrightarrow \Phi_6$.

**Reading.** 21 and 13 are the two sheets of the spin double cover over a single rotation, and 17 is the average over the fibre. A rotation in $SO(3)$, which is all the metric sees, cannot tell 21 from 13. It sees only their average, 17. This is the same statement as the scheme proof's "the metric sees only $(\det e)^2$", now in group language. The proof gives the identity $(21 + 13)/2 = 17$ (Eq. 10 in `llms.txt`) for every $K$, which explains why it holds.

## 3. The Möbius–Lorentz reading of the state map

1. $s(x) = (x-1)/(x+1) = \tanh\eta$ with $\eta = \tfrac12\ln x$. **The structural state $s$ is a velocity and $\ln x$ is a rapidity.**
2. The t-bit dilation gate $D_\alpha: x \mapsto \alpha x$ acts on $s$ by relativistic velocity addition, $s \mapsto (s_\alpha + s)/(1 + s_\alpha s)$. The exchange $P: x \mapsto 1/x$ is boost reversal, $s \mapsto -s$.
3. The logistic law $d\mu/d\ln x = \mu(1 - \mu)$ is $ds/d\eta = 1 - s^2$, the rapidity flow. TetA and TetB ($s = \pm 1$) are the two null limits and the Field Origin ($s = 0$) is the rest frame.
4. $f(K, s) = |K - e^{i\theta}|^2$ with $s = -2\cos\theta$. As $x$ runs over $(0,\infty)$, $e^{i\theta}$ traces the $60^\circ$ arc from $\zeta_6$ (TetB, $x \to 0$) through $i$ (Field Origin, $x = 1$) to $\zeta_3$ (TetA, $x \to \infty$). The galactic transition $g = a_0$ is the Gaussian point $i$. The whole constitutive law lives on one edge of the hexagon of sixth roots of unity.

> **Critical finding.** The normalisation route to the constitutive law (Eqs. 14–15 in `llms.txt`) is
> $$\mu = \frac{f(K,s) - f(K,-1)}{f(K,+1) - f(K,-1)} = \frac{1 + s}{2}\qquad\text{for every } K.$$
> $K$ cancels. On this route $\mu(x) = x/(x+1)$ follows from the Cayley map $s(x)$ alone, and the values 21, 17, 13 contribute nothing. This does not touch the exchange-symmetry proof, which stands on its own premises. But the polynomial route should not be cited as evidence that $\mu$ "knows" about $K = 4$.

## 4. The constitutive law is a modular matrix

- $\mu = L = \begin{psmallmatrix}1&0\\1&1\end{psmallmatrix} = P\,T\,P$, and $1 - \mu = P\,T$: $x \mapsto 1/(x+1)$.
- $L = S\,T^{-1}S^{-1}$: the constitutive law is conjugate to the cusp generator.
- $L^K = \begin{psmallmatrix}1&0\\K&1\end{psmallmatrix}$, so $L$ has order exactly $K = 4$ modulo 4. Composing the law $n$ times gives $x/(nx + 1)$.
- **Stern–Brocot.** The two integer gates $\{T: x \mapsto x + 1,\ L = \mu\}$, applied to the balanced state $x = 1$, reach every positive rational exactly once (checked to depth 10: 1023 words, 1023 distinct rationals, all reduced $p/q$ with $p + q \le 11$). In t-bit terms, the constitutive law and one threshold shift form a complete, non-redundant integer gate set, and $\mu(p/q) = p/(p+q)$ maps the Stern–Brocot tree onto the Farey tree.

## 5. A new uniqueness route to K = 4

The rotation group of the spherical triangle group $\Delta(2,3,K)$ has order $12K/(6 - K)$. The torsion sector has $K\binom K2$ components. Over the spherical range $2 \le K \le 5$:

$$\frac{12K}{6-K} = K\binom K2 \iff K(K-1)(6-K) = 24 \iff K = 4.$$

| $K$ | group | order | torsion count |
|:-:|---|:-:|:-:|
| 3 | tetrahedral $A_4$ | 12 | 9 |
| **4** | **octahedral $S_4$** | **24** | **24** |
| 5 | icosahedral $A_5$ | 60 | 50 |

So $K = 4$ is the only level at which the torsion sector can be the regular representation of the modular quotient. This is independent of $2(D+1) = 2^D$ and of the $K\binom K2 = K!$ argument in the torsion proof, although it agrees with both.

## 6. The squaring ladder explained

On the spin side, $(K - X)(K + X) = K^2 - X^2$. Squaring the element therefore corresponds to $K \mapsto K^2$, which gives the Sierpiński ladder of `01.1`:

$$\Phi_3(K^2) = \Phi_3(K)\,\Phi_6(K),\qquad \Phi_4(K^2) = \Phi_8(K),\qquad \Phi_6(K^2) = \Phi_{12}(K).$$

- **The next level's TetA is the product of this level's two sheets:** $273 = 21 \times 13$.
- The Field Origin column is the Fermat sequence: $17, 257, 65537$ (prime), then $F_5 = 4294967297 = 641 \times 6700417$ (composite). Any claim that the ladder stays prime is falsified at the fourth rung.

---

## 7. What failed, and what this does not show

**Hypothesis rejected: "the exchange $x \mapsto 1/x$ is the TetA ↔ TetB swap at level 4."** It is false. Reduced mod 4, $P$ is a **mirror**: orientation-reversing, of order 2, fixing the cusps $x = 1$ and $x = -1$, and preserving each tetrahedron. The swap is carried by:

- the central inversion $Z = \begin{psmallmatrix}1&2\\2&3\end{psmallmatrix}$ (the centre of $\mathrm{PGL}_2(\mathbb Z/4) \cong O_h$), which is spatial parity $v \mapsto -v$. This agrees with the scheme proof's "three is odd";
- the rotation $Z \cdot P$, a half-turn;
- the order-4 elements, including the constitutive law $L$ itself (whose square preserves the tetrahedra), and the six transpositions. In short, the sign character of $S_4$.

So the framework's two involutions, *exchange* ($\mu \leftrightarrow 1 - \mu$) and *spatial parity* (TetA ↔ TetB), are **different elements** of the octahedral group. Their product is a rotation. The documents currently use the two interchangeably, and this result says they should be kept apart.

**Coincidence rejected.** $\varphi(13) + \varphi(17) + \varphi(21) = 40$ equals the Christoffel count at $K = 4$, but at no other $K$ in $2, \dots, 29$, and nothing explains it. It is filtered out.

**Scope.**
- These are exact identities among standard objects: cyclotomic polynomials, $\mathrm{SL}_2(\mathbb Z)$, Klein's $X(4)$, Spin(3). The new part is the identification and the K-cancellation finding, not new number theory.
- "The torsion $S_4$ is the modular $S_4$" is an *identification*. Both are regular $S_4$-sets and so isomorphic as representations, but no map has been constructed from frame-leg permutations to $\mathrm{PSL}_2(\mathbb Z/4)$ that carries the 24 torsion components to the 24 sheets. Building that map is the next real step.
- Nothing here bears on $\alpha_G = \tfrac{17}{13}\alpha^{21}(1 + \alpha/2\pi)$, on $1/\alpha = 137 + 1/28$, or on the SPARC result. In particular the algebra does not single out $\alpha$ as the base or 21 as the exponent.

## 8. Open questions this opens

1. **Construct the equivariant map** from the torsion components $T^a{}_{[bc]}$ to the sheets of $X(4) \to X(1)$, compatible with the 40 / 24 split. If the 40 Christoffel components also have a natural home on $X(4)$, the Einstein / TetA partition becomes a statement about modular forms of level 4.
2. **The K = 5 hinge is icosahedral.** $\mathrm{PSL}_2(\mathbb Z/5) \cong A_5$ and $X(5)$ is the icosahedron. The "portal shell" at $K = 5$ (`01.4`, `03.1`) would carry icosahedral, not tetrahedral, symmetry, and its torsion count (50) is not the regular representation (60). This is a sharp test of that programme.
3. **Level-4 modular forms.** $\Gamma(4)$ is conjugate to $\Gamma_0(16)$, with $16 = K^2$ the curvature prefactor, whose forms include $\theta(\tau)^k$. If the 40 / 24 split has a modular reading, it should show up there.
4. **Exchange as a mirror.** Since $x \mapsto 1/x$ is orientation-reversing on $X(4)$, the exchange-symmetry premise of the constitutive-law proof is a reflection, not a rotation. Restate that proof with the mirror and parity kept distinct, and see whether any premise changes.

---

```bash
python research/algebra-intersection/verify_intersection.py     # 63/63 PASS
```
