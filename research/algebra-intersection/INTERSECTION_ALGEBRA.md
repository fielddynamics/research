# The Intersection Algebra

*The coupling polynomial, the constitutive law, the closure operator and the torsion sector as one modular group*

**Status:** derived and checked. Part I is tested by [`verify_intersection.py`](verify_intersection.py) (63/63 PASS), Part II by [`verify_octahedral_connection.py`](verify_octahedral_connection.py) (48/48 PASS) and Part III, the cube, by [`verify_cube.py`](verify_cube.py) (38/38 PASS). **Part III corrects parts of Part II and §13; where they disagree, Part III stands.** The hypotheses that turned out false are tested too.
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

# Part I. One group

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

**Reading (corrected in §11 and §13).** The identity holds for any pair $\pm q$, so 17 is the average of 21 and 13 over the pair. But the group that actually separates 21 from 13 is the trace cover $\mathrm{SL}_2(\mathbb Z/4)$, not the spin cover $2O$. So "21 and 13 are the two spin sheets" is withdrawn. What remains is the norm identity and the fibre average. A rotation in $SO(3)$, which is all the metric sees, cannot tell 21 from 13. It sees only their average, 17. This is the same statement as the scheme proof's "the metric sees only $(\det e)^2$", now in group language. The proof gives the identity $(21 + 13)/2 = 17$ (Eq. 10 in `llms.txt`) for every $K$, which explains why it holds.

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

So the framework's two involutions, *exchange* ($\mu \leftrightarrow 1 - \mu$) and *spatial parity* (TetA ↔ TetB), are **different elements** of the octahedral group. Their product is a rotation. The constitutive-law proof's README identifies them ("The exchange is parity itself"), and this result says that in the level-4 model they are different. §13 sets out exactly what that does and does not affect.

**Coincidence rejected.** $\varphi(13) + \varphi(17) + \varphi(21) = 40$ equals the Christoffel count at $K = 4$, but at no other $K$ in $2, \dots, 29$, and nothing explains it. It is filtered out.

**Scope.**
- These are exact identities among standard objects: cyclotomic polynomials, $\mathrm{SL}_2(\mathbb Z)$, Klein's $X(4)$, Spin(3). The new part is the identification and the K-cancellation finding, not new number theory.
- "The torsion $S_4$ is the modular $S_4$": Part II (§9) now builds the explicit isomorphism and the explicit intertwiners. The 24 torsion components are *not* a free orbit (each basis tensor is fixed by a transposition). They are edge data on $X(4)$: $R[E] \oplus C^1$.
- Nothing here bears on $\alpha_G = \tfrac{17}{13}\alpha^{21}(1 + \alpha/2\pi)$, on $1/\alpha = 137 + 1/28$, or on the SPARC result. In particular the algebra does not single out $\alpha$ as the base or 21 as the exponent.

## 8. Open questions this opens

1. ~~Construct the equivariant map~~ Done in §9, for all 64 components.
2. **The K = 5 hinge is icosahedral.** $\mathrm{PSL}_2(\mathbb Z/5) \cong A_5$ and $X(5)$ is the icosahedron. The "portal shell" at $K = 5$ (`01.4`, `03.1`) would carry icosahedral, not tetrahedral, symmetry, and its torsion count (50) is not the regular representation (60). This is a sharp test of that programme.
3. **Level-4 modular forms.** $\Gamma(4)$ is conjugate to $\Gamma_0(16)$, with $16 = K^2$ the curvature prefactor, whose forms include $\theta(\tau)^k$. If the 40 / 24 split has a modular reading, it should show up there.
4. **Exchange as a mirror.** Since $x \mapsto 1/x$ is orientation-reversing on $X(4)$, the exchange-symmetry premise of the constitutive-law proof is a reflection, not a rotation. Restate that proof with the mirror and parity kept distinct, and see whether any premise changes.

---


---

# Part II. The connection lives on the octahedron

## 9. The 64 connection components as cochains on $X(4)$

**The isomorphism.** The cusps of $X(4)$ map to the six vertices $\pm e_i$ of the octahedron, and this carries $\mathrm{PSL}_2(\mathbb Z/4)$ onto the rotation group $O$ and $\mathrm{PGL}_2(\mathbb Z/4)$ onto $O_h$. The map is checked to be a homomorphism on all $48 \times 48$ pairs. The four tetrad legs are the four body diagonals, and $O$ permutes them as $S_4$. A rotation is odd on the legs exactly when it swaps the TetA and TetB tips.

**Theorem (octahedral decomposition of the connection).** As $S_4$-modules, with an explicit invertible intertwiner in each case:

| Sector | Count | Octahedral content |
|---|:-:|---|
| incident torsion $T^a{}_{[ab]}$ | 12 | $R[E]$, functions on the 12 edges |
| non-incident torsion $T^a{}_{[bc]}$ | 12 | $C^1$, **oriented 1-cochains** on the octahedron |
| Christoffel $\Gamma^a{}_{(bc)}$ | 40 | $R[D] \oplus 3R[E]$: the 4 body diagonals and three copies of the edges |
| **whole connection** | **64** | $R[D] \oplus 4R[E] \oplus C^1$ |

> **Scope (see Part III, §15).** This table is for the *abstract* $S_4$ of leg permutations, transported to the rotation group $O$. When the legs are taken as what they are, vectors to the TetA corners of the cube, the odd rotations send each leg to *minus* a leg, and the geometric action is this one tensored with $\mathrm{sgn}$, which exchanges $R[E]$ and $C^1$. The group that permutes the legs without signs is the tetrahedron's own group $T_d$, and §15 restates the theorem there.

So, for the abstract $S_4$, the torsion-free condition of general relativity keeps only orientation-blind data (diagonals and unoriented edges). The one oriented object in the connection, the 1-cochains $C^1$, lies entirely in the torsion. "General relativity is root-blind" now has a concrete form: **GR discards the orientation of the octahedron.**

**Hodge split.** $X(4)$ is a sphere, so $H^1 = 0$, and $C^1$ is exactly gradients from the cusps plus curls from the tips:

$$C^1 = \underbrace{d\,C^0}_{5\,=\,E + 3'} \;\oplus\; \underbrace{d^{T} C^2}_{7\,=\,\mathrm{sgn} + 3 + 3'},\qquad C^0 = 1 + E + 3',\quad C^2 = 1 + \mathrm{sgn} + 3 + 3'.$$

**The parity detector is a vortex.** Let $\chi = +1$ on the four TetA tips and $-1$ on the four TetB tips. Then the 1-cochain $\omega = d^{T}\chi$:

- spans the sign line of $C^1$. Pulled back through the intertwiner, it is *the* single sign-representation vector of the torsion, the one the torsion proof found;
- takes the value $\pm 2$ on every edge (adjacent tips always have opposite colours), so it is a uniform flow;
- is purely co-exact, orthogonal to every gradient, so it is not a potential flow;
- has circulation $+6$ around every TetA tip and $-6$ around every TetB tip.

The pipeline document's sentence "the torsion is the vortex" was a slogan. Here it is an exact statement for the abstract $S_4$: **the sign mode of the torsion corresponds to the curl of the TetA − TetB indicator on the level-4 curve.** Part III (§15) identifies the same mode, in the frame's own geometry, as the volume form $\varepsilon_{abcd}$ of TetA. It transforms by orientation ($\det$), and how it transforms under spatial inversion is fixed by the connection's three vector indices, not by the octahedron's antipodal map.

## 10. Where the t-bit states sit

The three axes of the octahedron are $\{0, 2\}$, $\{\infty, \tfrac12\}$ and $\{1, -1\}$.

- **The three t-bit logical states $x = 0$ (deep field), $x = 1$ (balanced) and $x = \infty$ (Newtonian) are the corners of one face, so they form a single tip of the stellated octahedron.** The antipodal tip, in the other tetrahedron, is the harmonic cross-ratio triple $\{-1, 2, \tfrac12\}$.
- The stabiliser of the tip $\{0, 1, \infty\}$ in $\mathrm{PGL}_2(\mathbb Z/4)$ is the anharmonic group $S_3 = \langle x \mapsto 1/x,\ x \mapsto 1 - x\rangle$, the classical symmetry group of the cross-ratio.
- The exchange $P$ is the mirror of that tip: it swaps $0$ and $\infty$ and fixes $1$. The constitutive law $L$ is the quarter-turn about the axis $\{0, 2\}$, the threshold shift $T$ is the quarter-turn about $\{\infty, \tfrac12\}$, and the Field Origin $x = 1$ lies on the third axis.

**Consequence for the framework (conditional; see §13).** *If* the t-bit line is read through the level-4 curve, the labels "$x = \infty$ pure TetA" and "$x = 0$ pure TetB" name two corners of the same tip, and the two tetrahedra are told apart by the harmonic points $\{-1, 2, \tfrac12\}$. Within the t-bit's own definitions ($\mu$ = TetA share) the labels are consistent. They conflict only with the level-4 picture.

## 11. The double cover that separates 21 from 13

The values 21 and 13 are the traces of the two lifts $\pm M$ of one element. The double cover that carries them is $\mathrm{SL}_2(\mathbb Z/4) \to S_4$, and its extension class can be identified exactly:

- Its element orders are $\{1{:}1,\ 2{:}7,\ 3{:}8,\ 4{:}24,\ 6{:}8\}$. So it is **not** the spin cover $2O$ (binary octahedral), **not** $\mathrm{GL}(2,3)$ and **not** split.
- The rule $\varphi(S) = \varphi(T) = i$ extends to a homomorphism $\varphi: \mathrm{SL}_2(\mathbb Z/4) \to \mu_4$ with $\varphi(-1) = -1$ and $\varphi^2 = \mathrm{sgn}$. Hence

$$\boxed{\;\mathrm{SL}_2(\mathbb Z/4) \;\cong\; \{(g, z) \in S_4 \times \mu_4 \;:\; z^2 = \operatorname{sgn} g\}\;}$$

- $\varphi$ is the multiplier system of $\eta(\tau)^6$ (weight 3), and $\varphi^2 = \mathrm{sgn}$ is that of $\eta(\tau)^{12}$. Both are checked numerically to 50 digits. **The TetA ↔ TetB sign character of $S_4$ is the multiplier of $\eta^{12}$.**

**Trace table.** Writing $s = -\operatorname{tr} M \bmod 4$:

| Class in $S_4$ | $s$ | Value |
|---|:-:|---|
| transpositions (edge half-turns) | 0 | $\Phi_4 = 17$, Field Origin |
| 3-cycles (rotations about the tips) | $\pm 1$ | $\Phi_3 = 21$ / $\Phi_6 = 13$ |
| identity, double transpositions, 4-cycles | 2 | $(K \mp 1)^2$, not elliptic |

The elliptic classes are exactly the three structural states, now read inside a finite group.

**Sign-twisted equivariance.** Over $A_4$ the cover splits, so each 3-cycle has a canonical order-3 lift (trace $-1$, value 21). Give each TetA tip the 21-lift of its $120^\circ$ rotation and each TetB tip the 13-lift. Then, for all 48 elements $h$ and all 8 tips $v$:

$$h\,\mathcal L(v)\,h^{-1} \;=\; \operatorname{sgn}(h)\,\mathcal L(h v), \qquad \mathcal L(-v) = -\mathcal L(v)^{-1}.$$

The 21/13 labelling is equivariant up to exactly one defect, the sign character, and that defect is $\varphi^2$, the $\eta^{12}$ multiplier. Spatial parity acts on the lifted states as $s \mapsto -s$.

## 12. What Part II changes

1. **Three different double covers of $S_4$ are in play, and they should be named separately.** They are $O_h = S_4 \times \mathbb Z_2$ (spatial parity, the scheme proof's two roots), $2O$ (spin) and $\mathrm{SL}_2(\mathbb Z/4)$ (the trace cover in which "21 or 13" is a property of the group element itself). They are pairwise non-isomorphic. The framework's own reading, that parity carries 21 to 13, is **consistent** with this: §11 checks that parity acts as $s \to -s$ on the lifted states. The reading that does not survive is mine, in §2: 21 and 13 are *not* the two sheets of the spin cover. See §13.
2. ~~Prediction-shaped consequence ("a scalar potential cannot excite the mode")~~ **Withdrawn.** On the cube's own cell complex, the Hodge dual of $\omega$ is $d\chi$, the *gradient* of the TetA − TetB indicator along the 12 cube edges, each of which runs from a TetA corner to a TetB corner. Whether the mode is a "curl" or a "gradient" depends on which of the two dual complexes you write it on, so it supports no physical prediction. The real discriminating test is in §16.
3. **Next step.** Level-4 forms with these multipliers ($\eta^6$, $\eta^{12}$, and $\eta(4\tau)^6 \in S_3(\Gamma_0(16))$ with $16 = K^2$) are the natural place to look for a modular reading of the 40 / 24 split.

## 13. Impact on existing framework claims, stated precisely

Two kinds of finding are here, and they must not be mixed up.

- **Firm.** Pure algebra, true whatever model you adopt.
- **Conditional.** True *if* the level-4 modular picture of Parts I–II is the right home for the framework's objects. The algebra of that picture is verified. That it is the *physical* picture is my proposal, not something proven.

| # | Framework claim (file) | Finding | Strength | What has to change | What is untouched |
|:-:|---|---|:-:|---|---|
| 1 | Normalisation of the coupling polynomial is a route to $\mu$: $\mu = (f(x) - 13)/8$ (`llms.txt` Eq. 13–15, listed among the "routes in the papers") | $(f - f_{-1})/(f_{+1} - f_{-1}) = (1+s)/2$ for **every** $K$. The route is the Cayley map $s(x)$ rewritten, and 21, 17, 13 cancel out | **Firm** | Stop counting it as an independent route, or as evidence that $\mu$ reflects $K = 4$. It is a relabelling of $s(x)$ | $\mu = x/(x+1)$ itself; the exchange-symmetry proof; the SPARC fit |
| 2 | "Swapping TetA and TetB is the map $x \to 1/x$" and "The exchange is parity itself" (`proofs/constitutive-law-exchange-symmetry/README.md`, lines 78–80) | *Revised in Part III.* At level 4, $x \to 1/x$ is a cube mirror with $(\det, \mathrm{swap}) = (-1, +1)$. It **does** flip orientation, the root of $\det e$, exactly as the scheme proof's criterion requires. It does **not** carry TetA onto TetB as a set; only the inversion $Z$ (or a quarter-turn) does that | **Conditional** | Line 80 is right if "parity" means orientation. Line 78 is the one that conflicts: swapping the root and swapping the tetrahedron are two different bits | The proof's logic and premise (X) |
| 3 | $x = \infty$ is "Pure TetA", $x = 0$ is "Pure TetB", $P$ "swaps TetA ↔ TetB" (`tbit_algebra.md` lines 48–50, 90; `Cube lattice/tbit_compute_node_algebra.md` lines 69–71, 133; `gfd_quantum_compute_algebra.md` lines 176–178) | In the cube, $0$, $1$ and $\infty$ are the centres of the three faces around one corner. Each is a point where a TetA edge crosses a TetB edge, so none belongs to one tetrahedron. $P$ is the diagonal mirror through that corner | **Conditional** | If the level-4 picture is adopted, the t-bit labels mean "$\mu \to 1$ / $\mu \to 0$" (shares), not "which tetrahedron" | The t-bit gate algebra as algebra |
| 4 | 21 and 13 are carried across by parity (scheme proof, TetA/TetB as the two roots) | **Consistent.** Parity acts on the lifted states as $s \to -s$ (§11) | — | Nothing | — |
| 4′ | *My* Part I §2: "21 and 13 are the two spin sheets" | **Wrong.** The cover that separates them is $\mathrm{SL}_2(\mathbb Z/4)$, which is not the spin cover $2O$ | **Firm** | Withdrawn (§2 now corrected) | The fibre-average identity $(21 + 13)/2 = 17$ |

**The decision this forces** (revised in Part III). Rows 2 and 3 come down to one question: does the exchange $\mu \leftrightarrow 1 - \mu$ swap only the root, or the root *and* the tetrahedron? In cube terms, is it the mirror (a bit SWAP) or the inversion (NOT on all three bits)? §16 gives the test that tells them apart. The earlier version of this paragraph used the octahedron's antipodal action on $\omega$, which is not how inversion acts on the connection, so its test was wrong and has been replaced.


---

# Part III. The stellated octahedron in its cube

The geometry is two tetrahedra inscribed in a cube $[-1,1]^3$: TetA on the four corners with sign product $+1$, TetB on the four with $-1$. In Walsh language these are the odd- and even-parity 3-bit addresses. Parts I–II used the octahedron and its 24 rotations. The cube has 48 symmetries, $O_h$, and the extra 24 are exactly where the framework's word "parity" splits apart.

## 14. The cube is the modular curve, cell by cell

The special points of $X(4)$ are the non-zero cells of the cube, $\{-1, 0, 1\}^3 \setminus 0$. Each kind of cell is an incidence of the two tetrahedra:

| Cube cell | Count | $X(4)$ point | Stabiliser | Where TetA and TetB meet | Value |
|---|:-:|---|:-:|---|:-:|
| face centre | 6 | cusp | $\mathbb Z_4$ | a TetA edge **crosses** a TetB edge (the two diagonals of that face) | level $K = 4$ |
| edge | 12 | over $i$ | $\mathbb Z_2$ | a TetA face **meets** a TetB face (the core octahedron's edges); the cube edge joins a TetA corner to a TetB corner | **17** |
| corner | 8 | over $\rho$ | $\mathbb Z_3$ | belongs to **one** tetrahedron | **21 / 13** |

This makes the framework's Rule 4 ("the Field Origin is where TetA and TetB meet") literal. The Field Origin value 17 sits on exactly the 12 cells where a face of one tetrahedron touches a face of the other. The tetrahedron-specific values 21 and 13 sit on the corners, which each belong to one tetrahedron. The 26 cells, $27 - 1$, are the ternary vectors, with the zero vector being the centre.

## 15. Two copies of S₄, and three kinds of "parity"

$O_h$ has three index-2 subgroups, each of order 24 and each containing $A_4$, and correspondingly three non-trivial characters:

| Subgroup | What it is | Kernel of | Relevance |
|---|---|---|---|
| $O$ | rotations | $\det$ | $= \mathrm{PSL}_2(\mathbb Z/4)$, the modular group |
| $T_d$ | symmetries of TetA alone | $\mathrm{swap}$ | **permutes the legs with no sign**: the torsion proof's $S_4$ |
| $T_h$ | pyritohedral | $\det\cdot\mathrm{swap}$ | contains the inversion $Z$ |

So **the modular $S_4$ and the torsion $S_4$ are different subgroups of the cube's symmetry**, isomorphic and sharing $A_4$. Every odd rotation in $O$ sends each TetA corner to *minus* a TetA corner. Representatives of the three non-trivial classes of $O_h / A_4 \cong \mathbb Z_2^2$:

| Element | In bits | $\det$ (orientation, the root of $\det e$) | swap (TetA ↔ TetB) | At level 4 |
|---|---|:-:|:-:|---|
| diagonal mirror, e.g. $x = y$ | SWAP two bits | $-1$ | $+1$ | the exchange $x \to 1/x$ |
| inversion $Z: v \to -v$ | NOT all three bits | $-1$ | $-1$ | the centre $Z$ of $\mathrm{PGL}_2(\mathbb Z/4)$ |
| quarter-turn about a face axis | — | $+1$ | $-1$ | the constitutive law $L$ |

The constitutive law equals mirror × inversion modulo $A_4$.

**Galois reading.** The stabiliser of the closure axis $(1,1,1)$ is $D_{3d}$ (order 12). It acts on the $\Omega$-fixed algebra $\mathbb Q[T_1, I] = \mathbb Q(\sqrt3, i) = \mathbb Q(\zeta_{12})$ by $T_1 \to \pm T_1$, $I \to \det \cdot I$, and $D_{3d}/C_3 \cong O_h/A_4 \cong \mathrm{Gal}(\mathbb Q(\zeta_{12})/\mathbb Q)$:

| Element | Galois element | Fixed quadratic field |
|---|:-:|---|
| quarter-turn (constitutive-law class) | $\sigma_5$ | $\mathbb Q(i)$, Gaussian: Field Origin, 17 |
| inversion $Z$ | $\sigma_7$ | $\mathbb Q(\omega)$, Eisenstein: 21 / 13 |
| mirror (exchange $x \to 1/x$) | $\sigma_{11}$ | $\mathbb Q(\sqrt3)$, real |

Equivalently, **orientation ($\det$) is the quadratic character of $\mathbb Q(i)$, TetA ↔ TetB is that of $\mathbb Q(\sqrt3)$, and $\det\cdot$swap is that of $\mathbb Q(\omega)$.**

**Correction to Appendix J, §3.** There $\sigma_5$ is listed as fixing $\mathbb Q(\sqrt{-3})$ and $\sigma_7$ as fixing $\mathbb Q(i)$. It is the other way round ($\sigma_a$ fixes $\mathbb Q(i)$ iff $a \equiv 1 \bmod 4$). J's "parity reversal" row, $\sigma_{11}$, is the mirror, not spatial inversion.

**The connection, legs as vectors to the TetA corners.**
- Inversion acts as $-1$ on all 64 components (three vector indices).
- Under all of $O_h$, the orientation character $\det$ occurs **once in the torsion and never in the Christoffel sector**. That is the torsion proof's result, now correctly placed: its "sign representation" is $\det$, the root of $\det e$.
- The single $\det$ mode is the **volume form of TetA**, $T^a{}_{[bc]} = \varepsilon_{abcd}$.
- The TetA ↔ TetB character occurs 4 times in the Christoffel sector and once in the torsion. These are the 5 tensors invariant under every leg permutation. So **GR is blind to orientation but not to which tetrahedron.**
- The frame-native form of Part II's theorem, under $T_d$ with its geometric action:

$$\text{torsion} = R[\text{TetA vertices}] \otimes C^1(\text{oriented TetA edges}), \qquad \text{Christoffel} = R[\text{TetA vertices}] \otimes \big(R[\text{TetA vertices}] \oplus R[\text{unoriented TetA edges}]\big),$$

where the six TetA edges are the cube's face diagonals through the six cusps. The torsion-free condition forgets the orientation of TetA's edges, and that is what "GR is root-blind" means in the cube.

## 16. The test: mirror or inversion

The exchange $\mu \leftrightarrow 1 - \mu$ flips the root in either reading. What differs is the TetA/TetB bit. On the connection:

| | axial (volume) torsion mode | 5 leg-permutation-invariant modes (4 Christoffel + vector-torsion trace) |
|---|:-:|:-:|
| exchange = mirror (level-4 reading) | flipped | **unchanged** |
| exchange = inversion | flipped | **flipped** |

The axial torsion cannot tell the readings apart; the permutation-invariant part of the connection can. Under the level-4 reading, the transition through $a_0$ reverses the handedness of the torsion while leaving every component that treats the four legs alike untouched. Under the inversion reading, it reverses those too.

**Unresolved and stated plainly.** In the Clifford model (§1), the closure rotor $R$ is a bivector exponential, so inversion fixes it and does *not* exchange $\mathcal N_K(-R) = 21$ with $\mathcal N_K(R) = 13$. In the modular model (§11), inversion acts as $s \to -s$. The two models of "21 versus 13" therefore disagree about spatial inversion. Settling which model the framework means is the next thing to fix, and the cube table of §15 is where to do it.

---

```bash
python research/algebra-intersection/verify_intersection.py            # Part I:  63/63 PASS
python research/algebra-intersection/verify_octahedral_connection.py   # Part II: 48/48 PASS
python research/algebra-intersection/verify_cube.py                    # Part III: 38/38 PASS
```
