# The Intersection Algebra

*The coupling polynomial, the constitutive law, the closure operator and the torsion sector as one modular group*

**Status:** derived and checked. Part I is tested by [`verify_intersection.py`](verify_intersection.py) (63/63 PASS), Part II by [`verify_octahedral_connection.py`](verify_octahedral_connection.py) (48/48 PASS) and Part III, the cube, by [`verify_cube.py`](verify_cube.py) (38/38 PASS). Part IV, the cube as the computer of [`universe-is-pixelated/`](../universe-is-pixelated/), by [`verify_walsh.py`](verify_walsh.py) (26/26 PASS).

> **Read Part IV first.** Parts I–III modelled the exchange $x \to 1/x$ by reducing Möbius matrices mod 4. That model is algebraically correct but is **not** how the cube acts on a field. On the Boolean cube, where $x$ is the TetA : TetB mass ratio, the exchange *is* parity, XOR 111, exactly as the framework states (§17). The "conflicts" reported in §7, §10, §13 and §15–16 about exchange versus parity are therefore **retracted as artifacts of the mod-4 model**. The results that do not depend on that model still stand and are listed in §20. The hypotheses that turned out false are tested too.
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
| 2 | "Swapping TetA and TetB is the map $x \to 1/x$", "The exchange is parity itself" (constitutive-law README, lines 78–80) | **Retracted.** On the cube, $x$ = TetA mass / TetB mass and XOR 111 sends $x \to 1/x$ exactly (§17). The mod-4 "mirror" was an artifact of the model | — | Nothing | — |
| 3 | t-bit labels $x = \infty$ "Pure TetA", $x = 0$ "Pure TetB" | **Retracted.** On the cube, $x \to \infty$ is all mass in TetA and $x \to 0$ all mass in TetB, exactly as labelled | — | Nothing | — |
| 4 | 21 and 13 are carried across by parity (scheme proof, TetA/TetB as the two roots) | **Consistent.** Parity acts on the lifted states as $s \to -s$ (§11) | — | Nothing | — |
| 4′ | *My* Part I §2: "21 and 13 are the two spin sheets" | **Wrong.** The cover that separates them is $\mathrm{SL}_2(\mathbb Z/4)$, which is not the spin cover $2O$ | **Firm** | Withdrawn (§2 now corrected) | The fibre-average identity $(21 + 13)/2 = 17$ |

**Superseded by Part IV.** ~~The decision this forces~~ (revised in Part III). Rows 2 and 3 come down to one question: does the exchange $\mu \leftrightarrow 1 - \mu$ swap only the root, or the root *and* the tetrahedron? In cube terms, is it the mirror (a bit SWAP) or the inversion (NOT on all three bits)? §16 gives the test that tells them apart. The earlier version of this paragraph used the octahedron's antipodal action on $\omega$, which is not how inversion acts on the connection, so its test was wrong and has been replaced.


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

## 16. ~~The test: mirror or inversion~~ (superseded: on the cube the exchange is inversion, §17)

The exchange $\mu \leftrightarrow 1 - \mu$ flips the root in either reading. What differs is the TetA/TetB bit. On the connection:

| | axial (volume) torsion mode | 5 leg-permutation-invariant modes (4 Christoffel + vector-torsion trace) |
|---|:-:|:-:|
| exchange = mirror (level-4 reading) | flipped | **unchanged** |
| exchange = inversion | flipped | **flipped** |

The axial torsion cannot tell the readings apart; the permutation-invariant part of the connection can. Under the level-4 reading, the transition through $a_0$ reverses the handedness of the torsion while leaving every component that treats the four legs alike untouched. Under the inversion reading, it reverses those too.

**Unresolved and stated plainly.** In the Clifford model (§1), the closure rotor $R$ is a bivector exponential, so inversion fixes it and does *not* exchange $\mathcal N_K(-R) = 21$ with $\mathcal N_K(R) = 13$. In the modular model (§11), inversion acts as $s \to -s$. The two models of "21 versus 13" therefore disagree about spatial inversion. Settling which model the framework means is the next thing to fix, and the cube table of §15 is where to do it.

---

# Part IV. The cube as the computer

The cube here is the one of [`universe-is-pixelated/`](../universe-is-pixelated/README.md). Its corners are the 3-bit addresses, its harmonics are the Walsh functions $w_a(x) = (-1)^{\mathrm{popcount}(a \wedge x)}$, TetA and TetB are the odd- and even-parity corners, parity is $x \mapsto x \oplus 111$, and the octahedral node computes on it. A field on the pixel is a non-negative weight $p$ on the 8 corners with Walsh coefficients $c_a$.

## 17. The node reads out the constitutive law, and the exchange is parity

| Cube quantity | Framework quantity |
|---|---|
| $s = -c_{111}/c_{000}$, the normalised parity harmonic | the structural state $s$ |
| TetA share $= (1+s)/2$ | $\mu$, **exactly the node's readout** `mu = (1 + omega/c0)/2` (checked on 200 random node runs) |
| $x = $ TetA mass / TetB mass | the acceleration ratio $g/a_0$, so that $\mu = x/(x+1)$ |
| $s = \tanh(\tfrac12 \ln x)$ | the rapidity reading of §3 |
| $p(x) \to p(x \oplus 111)$ | sends $c_{111} \to -c_{111}$, so $s \to -s$, $\mu \to 1-\mu$ and $x \to 1/x$: **the exchange is Letter 2's parity** |

So the constitutive law is the chamber odds of the pixel, and the node already measures it. Two refinements, both exact:

- **Which operations exchange the chambers.** The XOR masks that flip the parity harmonic are exactly the four TetA addresses $\{001, 010, 100, 111\}$. Of these, only $111$ commutes with every permutation of the axes, so $111$ is the one that is spatial parity. Bit permutations (SWAP gates) keep every grade and never exchange the chambers. This is the cube-native form of §15's three labels: whether the chambers swap is the parity of the XOR mask, orientation is that parity times the sign of the bit permutation, and their product is the sign of the bit permutation alone.
- **Why the K-cancellation of §3 happens.** $\mu$ is a cube quantity, the TetA share, and the cube's even and odd sectors are the same size (4 and 4, the $H_2$ factor of $H_8 = H_2 \otimes H_4$). The coupling polynomial is a *frame* quantity. Normalising it onto the cube can only return the cube's share, which carries no $K$.

## 18. A new route to μ: maximum entropy on the pixel

Among all distributions on the 8 corners with a given parity harmonic, the one of largest entropy is the Gibbs state $p \propto e^{\eta\,w_A}$ ($w_A = +1$ on TetA, $-1$ on TetB). Its TetA share is

$$\mu = \frac{e^{\eta}}{e^{\eta} + e^{-\eta}} = \frac{x}{x+1}, \qquad x = e^{2\eta}.$$

The acceleration ratio is the exponential of the Lagrange multiplier on the parity harmonic, $\ln x = 2\eta$. The t-bit dilation gate $x \to \alpha x$ is a tilt $\eta \to \eta + \tfrac12\ln\alpha$, and the logistic law $d\mu/d\ln x = \mu(1-\mu)$ is the variance of $w_A$ in that Gibbs state, up to a factor of 4. This is an information-theoretic route to $\mu(x) = x/(x+1)$: *the least-committed field on the pixel, given only how much of it sits in TetA*. Its premise is that $g/a_0$ is the chamber odds. It is a fourth route, independent of the exchange-symmetry, Möbius and normalisation routes.

## 19. The three integers and the 64, read on the cube

**21, 17, 13 are graded dimensions.** Grade the frame's space $T^{\le 2}(V) = V^{\otimes 0} \oplus V \oplus V^{\otimes 2}$ (blocks $H_1, H_4, H_{16}$) by Letter 2's rule, with rank-one odd under parity. Then

$$\dim = 21,\qquad \dim_{\text{even}} = 17,\qquad \operatorname{sdim} = 13,$$

and $\mathrm{Tr}(I_s)$ at $s = +1, 0, -1$ is exactly these three: $I_{-1}$ *is* the parity operator, and its trace is the super-dimension. So the read of $G$ uses
- 17/13 = (root-blind dimension)/(super-dimension), and
- $\alpha^{21} = \alpha^{\dim}$.

The cube's own Walsh space, graded by XOR 111, has $(\dim, \dim_{\text{even}}, \operatorname{sdim}) = (8, 4, 0)$. The pixel is perfectly balanced; the frame is not, and its imbalance is 13.

**The 64.** The README notes $K^3 = (2^D)^2 = 64$: the connection's $4^3$ components equal the $8 \times 8$ corner transitions. The check asks *as what*:

| Symmetry | Connection $4^3$ ≅ transitions $8 \times 8$? |
|---|:-:|
| $E$ = TetB acting by XOR (order 4) | **yes**, both are 16 copies of the regular representation |
| $A_4$, the rotations of TetA | no |
| $T_d$, all of TetA's symmetry | no |

So the identification "the connection *is* the transitions" is canonical exactly over the cube's XOR action by TetB, the computing structure, and not over its rotations.

**The Eisenstein unit as a closure step.** Write a transition $(x, y)$ bitwise as $x + \omega y \in \mathbb F_4^3$, where $\mathbb F_4 = \mathbb Z[\omega]/2$ is the Eisenstein integers mod 2. Multiplication by $\omega$ is then

$$(x, y) \;\mapsto\; (y,\; x \oplus y),$$

a three-step closure: $x$, then $y$, then $x \oplus y$, and back, since $x \oplus y \oplus (x \oplus y) = 0$. It has order 3 and fixes only the trivial transition, so

$$64 = 1 + 3 \times 21,$$

and the 21 orbits are the closed XOR triangles of the cube: 14 genuine triangles (the 7 Fano lines, each in 2 orientations) and 7 out-and-back walks. Here $21 = \Phi_3(4)$ appears as a count of closures on the pixel, with the Eisenstein unit as the step. *Status: an exact identity.* It is the cube's $\mathbb F_4$-projective plane, $|PG(2,4)| = 21$. Whether the node's forward / backward / reconcile cycle realises this $\omega$-step is a question for the node, not yet a result.

## 20. What survives from Parts I–III

| Result | Status after Part IV |
|---|---|
| §3: the polynomial normalisation route to $\mu$ carries no $K$ | **Stands**, and is now explained (§17) |
| §4–5: $f(K,s) = \det(K - M)$ for the elliptic elements of $\mathrm{SL}_2(\mathbb Z)$; $\mu$ as the modular matrix $L$; the $(2,3,K)$ uniqueness route | Stand as algebra |
| §14: cube cells ↔ special points of $X(4)$; 17 on the cube's edges, where TetA meets TetB | Stands |
| §15: Appendix J's Galois table has $\sigma_5$ and $\sigma_7$ swapped | **Stands** (firm) |
| §15: the torsion's unique orientation mode is TetA's volume form $\varepsilon_{abcd}$, absent from the Christoffel sector | Stands |
| §2 "spin sheets"; §9–10 octahedral cochains and t-bit placement; §13 rows 2–3; §15–16 "exchange is a mirror" | **Retracted** or confined to the mod-4 model |

---

# Part V. A candidate mechanism for α²¹

*Read from [`g_three_sierpinski_blocks.html`](../g_from_topology/g_three_sierpinski_blocks.html) and [`tetb_64_walk_of_field_closure.html`](../field-closure/tetb_64_walk_of_field_closure.html). Checked by [`verify_closure_tree.py`](verify_closure_tree.py) (16/16).*

**Credit.** The construction of G from three Sierpiński blocks is the author's, in that diagram. The observations in §21 below (the blocks are tensor powers of $; the closure tree) are read off it. The junction rule of §22–23 is this document's hypothesis and is separate from the author's result.

**Note (Part VII):** the count 21 = (K³−1)/(K−1) is already in `g_matrix_synthesis.md`; only the cross-check of exponents in §23 is new here.

**Status: hypothesis.** It reproduces three of the archive's four α-exponents. It conflicts with the fourth (Λ), and the 17/13 prefactor rule does not carry over to it. Both failures are stated below.

## 21. Two facts in the diagrams

1. **G's blocks are the constitutive law.** The 4×4 and 16×16 Sierpiński blocks drawn for G are exactly $L^{\otimes 2}$ and $L^{\otimes 4}$, where $L = \begin{psmallmatrix}1&0\\1&1\end{psmallmatrix}$ is the Möbius matrix of $\mu(x) = x/(x+1)$ (§4). They are unipotent, so $\det(\alpha^{S}) = \alpha^{\mathrm{Tr}\,S} = \alpha^{1+4+16}$, the same 21 as the projector picture. The 1, 9, 81 filled cells are $3^{2k}$, from L's three non-zero entries.
2. **21 is the number of junctions in the closure tree.** The 64-channel walk (4 faces × 4 channels × 4 subchannels) is a complete 4-ary tree with 64 leaves. Such a tree has $1 + 4 + 16 = (K^D - 1)/(K - 1) = 21$ internal junctions. By depth: 17 at even depth and 4 at odd depth, so 21, 17 and 13 are "all junctions", "even-depth junctions" and "even minus odd".

## 22. The junction rule

> A coupling that completes a closure of $K^n$ channels, read $K$ at a time, carries one α per **junction** of the closure tree:
> $$\alpha^{J(n)}, \qquad J(n) = \frac{K^n - 1}{K - 1} = 1,\ 5,\ 21,\ 85,\ \dots$$

**Why all the junctions and not one path.** A single root-to-leaf path crosses only $D = 3$ junctions. The exponent counts all 21 because closure is atomic: every shared boundary must settle in the same snapshot (the author's note in the README). The amplitude is therefore a product over every junction, not over one path. At $n = D$ with $K = D + 1$, $J = ((D+1)^D - 1)/D$, so the exponent is fixed by $D$. It has three terms because the walk has three levels: face, channel, subchannel.

## 23. Tested against the archive

| Exponent used in the archive | Where | Junction rule |
|---|---|---|
| α¹ | electromagnetism | $J(1)$: one tetrahedron's 4 faces, one junction ✓ |
| α⁵ | $\eta_B = 29.4\,\alpha^5$, `baryogenesis.py` (justified there as $K_5 = K + 1$) | $J(2)$: a 16-channel closure ✓ |
| α²¹ | $G$ | $J(3)$: the 64-channel closure ✓ |
| α⁸⁵ | rejected for $G$ in `merkaba_engine.py` | $J(4)$: consistent, since $G$ is depth 3 |
| α⁵⁷ | $\Lambda = (9/5)\,\alpha^{57}$, `cosmological_constant.py` | **not a junction count: conflict** |

**What it changes.**
- The archive's three reasons for 21 do not agree. $1 + K + K^2$ levels and the surface truncation are compatible with the tree. "Three sweeps of α⁷" (`01.3`) is not: the tree splits 21 as $1 + 4 + 16$, not $7 + 7 + 7$, so one of the two readings has to go.
- The tree gives α¹, α⁵ and α²¹ one rule, where the archive currently has three unrelated justifications.

**Where it fails.**
- **Λ.** α⁵⁷ cannot be a single closure. Either Λ is a composite of closures, in which case the composition rule must be stated, or the junction rule is wrong.
- **The prefactor.** G's $17/13$ is (even-depth junctions)/(even − odd). The same rule at depth 2 gives $1/(1-4) = -1/3$, which is not $\eta_B$'s 29.4 and not even positive. So the tree explains the *exponent* but not the prefactor. The prefactor's derivation stays open, as `g_from_the_closure_climb.md` already says.
- **Look-elsewhere.** Two of the three matches (α¹ and α⁵) come with prefactors that were fitted (η_B's 29.4 was chosen in the archive), so they are weak evidence. The rule earns weight only if it is fixed now and used to predict an exponent the archive has not yet assigned.

**The test it proposes.** Any quantity the framework attributes to a complete closure of 256 channels must scale as α⁸⁵, and no quantity may carry an exponent outside $\{1, 5, 21, 85, \dots\}$ unless it is an explicit product of closures. Λ's α⁵⁷ is the first case to resolve.

---

# Part VI. The Sierpiński blocks, the three-sweep kernel and what reaches G

*Checked by [`verify_sweep_sierpinski.py`](verify_sweep_sierpinski.py) (10/10).*

## 24. The blocks are the triangular factors of a Hadamard sweep

The author's diagram builds G's operator as $S_0 \oplus s\,S_1 \oplus S_2$ with $S_k = L^{\otimes 2k}$ and $L = \begin{psmallmatrix}1&0\\1&1\end{psmallmatrix}$, the matrix of $\mu(x) = x/(x+1)$. The three-sweep kernel of [`spectral_kernel.py`](../spectral/spectral_kernel.py) is built from Walsh–Hadamard sweeps. The two are the same object, exactly:

$$H_2 = L\,\begin{pmatrix}1&0\\0&-2\end{pmatrix}L^{\mathsf T}, \qquad H_{2^n} = S_n\,D_n\,S_n^{\mathsf T},\quad D_n = \mathrm{diag}\big((-1)^{\mathrm{grade}}\,2^{\mathrm{grade}}\big).$$

A Hadamard sweep is a Sierpiński block, then the cube's parity grading (with weight $2^{\mathrm{grade}}$), then the transposed Sierpiński block. So the Sierpiński diagram and the three-sweep kernel are two factorisations of the same operator. In the diagram the parity grading appears as the $s$ on the middle block; in the sweep it sits in the diagonal factor $D_n$.

## 25. What actually reaches G

- **Through $\det(\alpha^A) = \alpha^{\mathrm{Tr}\,A}$, only the diagonal enters.** The Sierpiński blocks have unit diagonals, so their traces are 1, 4, 16. Identity blocks, or any unit lower-triangular blocks, give exactly the same $\alpha^{21}$ and $17/13$. The kernel says the same thing: a sweep with bridge $b$ has trace $\sum b$, so identity bridges on blocks 1, 4, 16 give 21, 17, 13. **The 5 + 65 off-diagonal filled cells never enter G.**
- **No off-diagonal-sensitive read gives 17/13.** The sum of entries, the Frobenius norm, $\mathrm{Tr}(S^{\mathsf T}S)$ and the below-diagonal count give 91/82/73 and 70/65/60, not 17/13. Every power $S^k$ is again unit lower-triangular, so $\mathrm{Tr}(S^k)$ returns 21, 17, 13 and nothing more.
- **The one-loop factor cannot come from the blocks.** Any read of integer blocks built from sums, products, traces and determinants is a polynomial in $\alpha$ with rational coefficients. $1/2\pi$ is transcendental. So $1 + \alpha/2\pi$, or $g_e/2$ as `gravity.py` writes it, must come from outside the blocks: from something with a circle in it.

## 26. What this means for "G comes from the diagram"

| Claim | Status |
|---|---|
| G's 21, 17, 13 are the traces of the three Sierpiński blocks, with $s$ on the middle one | **Exact** |
| The blocks are tensor powers of the constitutive law's matrix $L$ | **Exact, and new**: it ties G's operator to $\mu$ |
| The blocks are the triangular factors of the three-sweep Hadamard kernel, $H = SDS^{\mathsf T}$ | **Exact**: diagram and kernel are one operator |
| The Sierpiński *pattern* (the 9 and 81 filled cells) contributes to G | **No**, under the det–trace read. Identity blocks give the same number |
| The prefactor 17/13 or the one-loop factor come from the off-diagonal structure | **No**. 17/13 is diagonal, and $1/2\pi$ cannot come from integer blocks |

So the diagram is a correct and new *presentation*: one operator, built from the constitutive law, whose traces give G's integers. For the Sierpiński structure to *do* something, the read would have to be one that sees beyond the diagonal, and the number it gives would have to match G. The obvious places to look:
- the bridge $b$ of the three-sweep kernel, which can weight grades differently;
- the middle factor $D_n$, the one place parity and the weights $2^{\mathrm{grade}}$ enter.

Neither is done here.

---

# Part VII. Where the 2π of the one-loop factor comes from

*After reading all of [`g_from_topology/`](../g_from_topology/). Checked by [`verify_one_loop_fencepost.py`](verify_one_loop_fencepost.py) (6/6).*

**Correction to Part V.** The count $21 = (K^3 - 1)/(K - 1)$, i.e. $64 = 21 \times 3 + 1$, is already stated in [`g_matrix_synthesis.md`](../g_from_topology/g_matrix_synthesis.md) Part II. The closure-tree reading of §21–22 restates it as a tree and is not new. What remains of Part V is the comparison with the archive's other exponents (§23).

## 27. The identity

Part VI showed that the factor $1 + \alpha/2\pi$ cannot come from the integer blocks. It needs a circle. The archive already contains the circle, in two places:

- Paper VII: $f_{\text{closure}} = c/r_e$ and $f_{\text{Compton}} = m_e c^2/h$, so $f_{\text{closure}}/f_{\text{Compton}} = 2\pi/\alpha$.
- [`read_sweep_synthesis.md`](../g_from_topology/read_sweep_synthesis.md): one rotation of the read is one Compton period.

Together:

$$\frac{\alpha}{2\pi} \;=\; \frac{r_e}{\lambda_C} \;=\; \frac{f_{\text{Compton}}}{f_{\text{closure}}} \;=\; \frac1N, \qquad N = \frac{2\pi}{\alpha} \approx 861 \text{ closures per rotation},$$

$$1 + \frac{\alpha}{2\pi} \;=\; \frac{N+1}{N} \;=\; \frac{\lambda_C + r_e}{\lambda_C}.$$

**Reading (proposed).** One rotation of the read is $N$ closures. Read at their boundaries, $N$ intervals have $N + 1$ reads, a fencepost count. Equivalently, the read covers one Compton wavelength *plus one tile* $r_e$: the tile at the seam, which belongs to both the end of one rotation and the start of the next, is read once more. This matches the author's own requirement that a closure boundary is shared and must be read in the snapshot. On this reading:

- the $2\pi$ is the rotation of the read sweep;
- the $\alpha$ is the tile size over the reduced Compton wavelength, $r_e/\bar\lambda_C$;
- the "one loop" is one extra closure per rotation.

The closure-climb note already uses the same fencepost: its mean is taken over $n = 0, \ldots, 64$, which is 65 readings for 64 hexagrams.

**Status.** The identity is exact and uses only the archive's definitions. The fencepost reading is a proposal, as `synthesis_one_loop_G.md`'s $(2/17)(17\alpha)/4\pi$ is. Its advantage is that it says where both the $2\pi$ and the $\alpha$ come from, using quantities the framework has already defined, and it makes a different prediction at the next order.

## 28. A test the archive can already state

The archive uses two different completions of the factor, and a third is equally natural:

| Completion | Where | $G$ (CODATA 2018 inputs) | vs CODATA |
|---|---|---|---|
| $(N+1)/N = 1 + \alpha/2\pi$ exactly | `g_from_topology/` (fencepost: no $\alpha^2$ term) | $6.674219 \times 10^{-11}$ | −12.1 ppm |
| $g_e/2 = 1 + a_e$ | `pyramid_portal_research/python/gravity.py` (full QED anomaly) | $6.674207 \times 10^{-11}$ | −13.9 ppm |
| $N/(N-1)$ | fencepost counted the other way | $6.674228 \times 10^{-11}$ | −10.8 ppm |

They agree at first order and differ at second. $g_e/2 - (1 + \alpha/2\pi) = -1.76 \times 10^{-6}$, which is QED's two- and three-loop terms, $-0.3285\,(\alpha/\pi)^2 + 1.18\,(\alpha/\pi)^3$. The spread across all three is 3.1 ppm.

- **Now:** all three lie inside CODATA's 22 ppm, so G cannot yet choose.
- **What it means for the archive:** its two "one-loop" factors are different predictions. The [pre-registration](../g_from_topology/PREREGISTRATION.md) fixes $1 + \alpha/2\pi$, so `gravity.py`'s $g_e/2$ is a different formula and should not be cited as the same one.
- **The test:** a G measurement at about 1 ppm would decide whether the correction is a counting factor, with no $\alpha^2$ term, or QED's anomaly, with its $-0.328(\alpha/\pi)^2$. That is beyond current experiments (best single measurements are about 10 ppm), but it is a sharp statement for the pre-registration to carry.

---

# Part VIII. The loop factor from the snapshot principle

*After two failed pre-registered network models ([`NETWORK_MODEL_RESULT.md`](NETWORK_MODEL_RESULT.md)). Checked by [`verify_seam_average.py`](verify_seam_average.py) (7/7).*

**Why this is not a pre-registration.** A "loop model" could be built to give either $(N+1)/N$ (one extra read) or $N/(N-1)$ (a resummed loop). Nothing in the framework fixes which, so a registration would only encode the modeller's choice. What follows instead is a derivation from stated premises. The mathematics in it is a known theorem, so its result was known before it was computed. The blind test is experimental and is stated in §30.

## 29. Derivation

**Premises.**
- **P1.** One rotation of the read is one Compton wavelength (`read_sweep_synthesis.md`), and a closure tile has size $r_e$ (Papers III, VII). In tile units the rotation has length $N = \lambda_C / r_e = 2\pi/\alpha \approx 861.02$, which is **not an integer**.
- **P2.** Closure is atomic: it reads every tile the rotation **touches**. The tile cut by the seam is a shared boundary and must be in the snapshot. This is the author's requirement in the README and Paper I.
- **P3.** The rotation has no preferred phase relative to the tile lattice. Its offset is uniform over one tile (homogeneity of the lattice).
- **P4.** Tree-level G counts the ideal $N$ closures per rotation. The physical read counts the tiles actually touched, and the loop factor is the ratio of the two.

**Theorem** (geometric probability). A segment of length $N$ placed at a uniformly random offset on a lattice of unit tiles touches, on average, exactly $N + 1$ tiles, for every real $N$. With $N = n + f$, it touches $n + 1$ tiles with probability $1 - f$ and $n + 2$ with probability $f$, so the mean is $n + f + 1$. Monte Carlo at $N = 2\pi/\alpha$ over 2 million phases gives 862.0224 against 862.0226.

**Result.**

$$\frac{\mathbb E[\text{tiles read}]}{N} = \frac{N+1}{N} = 1 + \frac{\alpha}{2\pi} \qquad \text{exactly, at all orders.}$$

This gives the archive's one-loop factor a mechanism with every input already defined:
- the $2\pi$ is the rotation;
- the $\alpha$ is the tile over the wavelength;
- the "+1" is the seam tile that the snapshot must include.

The other counting rule, counting only tiles wholly inside the rotation, gives $N - 1$: a deficit, excluded by P2. A resummed $N/(N-1)$ needs a loop that premises P1–P4 do not contain.

## 30. What it predicts

Because the average is exact, the factor has **no $\alpha^2$ term**. That separates it from the two other completions in the archive:

| Completion | $G$ | vs seam average |
|---|---|---|
| Seam average, $(N+1)/N$ (this Part; equals the pre-registered $1 + \alpha/2\pi$) | $6.674219 \times 10^{-11}$ | — |
| QED anomaly, $1 + a_e$ (`pyramid_portal_research/python/gravity.py`) | $6.674207 \times 10^{-11}$ | −1.76 ppm |
| Resummed loop, $N/(N-1)$ | $6.674228 \times 10^{-11}$ | +1.35 ppm |

- **The test.** A determination of G at about 1 ppm decides between a counting correction, with no $\alpha^2$ term, and QED's anomaly, with $-0.328(\alpha/\pi)^2$. Current best measurements are about 10 ppm, so this is a target for the next generation of experiments, not a test available now.
- **What it settles inside the archive.** It supplies a mechanism for the factor the pre-registration already fixed, $1 + \alpha/2\pi$. It also says that `gravity.py`'s $g_e/2$ is a different and, on these premises, wrong completion.
- **What is still assumed.** P3, uniform phase, is the physical assumption that does the work. P4, that tree-level G counts exactly $N$ closures, is an identification, not a derivation. If either fails, so does the "exactly".

---

# Part IX. The prefactor 17/13 as a phase average

*Checked by [`verify_prefactor_exchange.py`](verify_prefactor_exchange.py) (6/6).*

## 31. The numerator is forced by exchange symmetry

[`g_from_the_closure_climb.md`](../g_from_topology/g_from_the_closure_climb.md) found that the closure's mean coupling depends on the measure: 17 per new hexagram, about 19.2 per step. So it proposed 17 only "per new reading". The dependence disappears under the framework's own exchange symmetry:

$$\langle f \rangle = \langle 1 + sK + K^2\rangle = 1 + K\langle s\rangle + K^2 = 1 + K^2 = 17 \quad\text{whenever the distribution of } s \text{ is symmetric under } s \to -s \;(x \leftrightarrow 1/x).$$

This holds for every symmetric measure. Uniform in $s$, uniform in $\mu$, uniform rapidity, log-normal in $x$ and the two-point TetA/TetB distribution all give 17. A one-way climb averaged per step is not symmetric, and it reproduces the note's ≈19.2 (19.4 here). The archive's own **breathing cycle** (`read_sweep_synthesis.md`: inhale 13 → 21, exhale 21 → 13) is symmetric, and averaged per step over a full breath it gives exactly 17 for any step measure. So the numerator does not need "per new reading". It needs only that a closure is the full breath, which the read-sweep note already says.

## 32. The denominator is the bound source

$\alpha_G = G m_e^2/\hbar c$ measures gravity relative to the electron, a bound pattern. The archive places bound matter in TetB: Paper VII has "bound envelopes, TetB chambers occupied, are matter", and `read_sweep_synthesis.md` describes matter as a read pattern reflected at the TetA/TetB boundary. TetB's capacity is $f(-1) = 13 = DK + 1$. So

$$\frac{17}{13} = \frac{\langle f\rangle_{\text{exchange-symmetric}}}{f(\text{bound source})}.$$

With the source placed elsewhere, the result misses badly: $17/21$ (TetA) is off by 38% and $17/17$ (origin) by 24%. Only TetB fits, at 12 ppm with the loop factor.

**Caveat on independence.** Paper VII's statement that matter sits in TetB was written after the G formula was known. It identifies the denominator but is not independent evidence for it.

## 33. What Parts VIII and IX together say about G

$$\alpha_G \;=\; \underbrace{\alpha^{21}}_{\text{atomic closure over } 1+4+16 \text{ levels}} \;\times\; \underbrace{\frac{\langle f\rangle}{f_{\text{source}}}}_{\text{phase average of the coupling}} \;\times\; \underbrace{\frac{\mathbb E[\text{tiles}]}{N}}_{\text{phase average of the seam}}$$

Both corrections to the bare $\alpha^{21}$ are **averages over a phase the read does not control**:
- the prefactor averages the coupling over the closure's position in its breath (exchange symmetric, so 17), relative to the source (13);
- the loop factor averages the seam over the rotation's position on the tile lattice ($N + 1$ tiles), relative to the ideal count ($N$).

**What this changes.** The archive's combination rule, "end as exponent, mean over start as prefactor", was one of 21 menu rules chosen after the fact. It is replaced by two principles the framework already states (exchange symmetry and matter in TetB) and one geometric theorem (the seam average).

**What it does not change, stated plainly.**
- The exponent's "one α per level" is still the framework's physical assumption.
- "Tree level counts N closures" (Part VIII, P4) is an identification.
- The TetB placement of the source is post hoc.

The formula is not more accurate than before: it is the same number. What has changed is that each of its parts now has a stated reason, and two parts have stated tests:
- **No α² term in the loop factor.** A ~1 ppm measurement of G would test it.
- **The exchange-symmetric mean.** Any other quantity the framework writes as "coupling relative to bound matter" must use $17/13$; one written relative to an *unbound* source must use $17/21$.

---

# Part X. One circle, and what the measured G says about the per-level factor

*Checked by [`verify_level_factor.py`](verify_level_factor.py) (8/8).*

## 34. The bound/unbound rule cannot be tested inside the archive

Part IX proposed that quantities taken relative to bound matter carry 17/13, and those relative to unbound sources carry 17/21. A search of the archive finds 17/13 only in G and in what follows from G: the Poisson prefactor $4\pi \cdot 17/13$, the Planck mass, $r_s$ and the docs that restate them. 17/21 appears nowhere. So the rule has no independent test inside the archive. It stands as a prediction for any future formula of that kind.

## 35. The whole formula on one circle

The read circle has circumference $\lambda_C$ (one rotation is one Compton period), so its radius is $\bar\lambda_C$. A tile of length $r_e$ on it subtends

$$\theta = \frac{r_e}{\bar\lambda_C} = \alpha \text{ radians}, \qquad N = \frac{2\pi}{\theta} \text{ tiles per turn},$$

and G becomes a function of this one geometric angle:

$$\alpha_G = \theta^{21}\cdot\frac{17}{13}\cdot\Big(1 + \frac{\theta}{2\pi}\Big).$$

Each of the 21 levels contributes the tile's **arc angle**. The seam contributes one extra tile **per full turn**.

## 36. The measured G already constrains the mechanism

Because the per-level factor is raised to the 21st power, any correction to it is amplified 21 times. With the prefactor and seam held fixed, CODATA's 22 ppm is therefore a per-level test at about 1 ppm:

| Per-level factor | Second-order term | z vs CODATA |
|---|---|---|
| **arc, θ** | 0 | **−0.54** |
| chord, 2 sin(θ/2) | −θ²/24 | −2.6 (excluded at 2σ) |
| sine, sin θ | −θ²/6 | −8.8 |
| tangent, tan θ | +θ²/3 | +16 |
| per-turn probability, θ/2π | — | −4 × 10⁴ |

| Seam factor (arc per level) | z |
|---|---|
| **per turn, 1 + θ/2π** | **−0.54** |
| per radian, 1 + θ | +272 |
| none | −52 |

At 2σ, a per-level factor of the form $\theta(1 + c\,\theta^2)$ needs $-0.029 < c < +0.051$, and any relative change per level must lie between −1.6 and +2.7 ppm.

**What this says.**
- **The levels count the arc in radians and the seam counts tiles per full turn.** That is two different measures on the same circle, and the data allow no other pairing.
- **A mechanism for "one α per level" must produce the arc exactly,** to about 2 ppm per level. Chord, sine and tangent readings are excluded.
- **The distinction is the familiar one between an angle and a probability.** A level contributes an angle (radian measure, $\hbar$). The seam contributes an expected count over a cycle ($h$, divided by $2\pi$). The formula's scale $\hbar c/m_e^2$ is already in radian measure, which is consistent with this.

**Caveat.** These are conditional constraints. They hold if 17/13 and the seam factor are exact. A per-level correction could be cancelled by an opposite change in the prefactor or the seam, so what the data fix is the combination. Within the formula as pre-registered, though, the per-level factor is pinned to the arc.

**The open question, now precise.** Why does a coupling level cost exactly one tile-angle, the arc subtended by $r_e$ on the read circle? Any proposed mechanism can be checked immediately against the table above, at the 2 ppm level per level, with no new experiment.

---

# Part XI. The per-level factor is the stellated octahedron's α

*From [`docs/03-fundamental-constants/01-fine-structure-constant-alpha.md`](../../docs/03-fundamental-constants/01-fine-structure-constant-alpha.md) and the mass page. Checked by [`verify_topological_alpha_in_G.py`](verify_topological_alpha_in_G.py) (9/9).*

## 37. Why one α per level: the docs' answer, joined to the read circle

The docs give the mechanism Part X asked for.
- **The count.** The stellated octahedron has $N = 1/\alpha = 1 + 8 \times 17 + 1/28 = 137 + 1/28$ interaction states: eight vertices each sampling the Field Origin depth 17, the global vertex, and one cycle through its 28 elements.
- **The share.** Closure's bandwidth $c/r$ is shared equally among them (the mass page: $mc^2 = \hbar c/(Nr)$).

So each level's read takes one state's share, $1/N = \alpha$.

This also resolves the radian-versus-turn split of Part X. Since $r_e = \alpha\bar\lambda_C$, the $N = 1/\alpha$ interaction states are exactly the **tiles in one radian** of the read circle, and $2\pi N$ is the tiles per turn. So:
- a level selects one of the octahedron's interaction states, the tiles per radian, giving $\alpha$;
- the seam adds one tile per full turn, giving $\alpha/2\pi$.

One circle, one stellated octahedron, two measures, each with a reason.

## 38. A test: does G use the measured α or the octahedron's α?

If the per-level factor is literally $1/N$ with $N = 137 + 1/28$, the framework can compute G with **no measured coupling at all**, using only $K$, $D$, $m_e$, $\hbar$ and $c$. The 2.1 ppm gap between $1/(137 + 1/28)$ and the measured α is amplified 21 times into **+44 ppm in G**.

| Version | G (×10⁻¹¹) | vs CODATA 2022 |
|---|---|---|
| measured α (pre-registered) | 6.674219 | −12 ppm, z = −0.54 |
| octahedron's α, $1/(137 + 1/28)$ | 6.674510 | +32 ppm, z = +1.40 |

Both lie inside CODATA's 2σ. Over all 16 measurements, with CODATA's expansion factor 3.9, the measured-α version is mildly preferred, Δχ² = 2.0, which does not decide. Inverted, CODATA's G implies a per-level $1/\alpha = 137.03592 \pm 0.00015$: the measured value is at +0.5σ and the octahedron's at −1.4σ.

**The two most precise measurements split along exactly this line.**

| Measurement | Uncertainty | z (measured α) | z (octahedron's α) | Implied 1/α per level |
|---|---|---|---|---|
| HUST 2018, time-of-swing | 11.7 ppm | **+0.45** | +4.19 | 137.036033 ± 0.000076 |
| HUST 2018, angular acceleration | 11.5 ppm | −3.44 | **+0.34** | 137.035740 ± 0.000075 |

The two HUST 2018 methods disagree with each other by 45 ppm, and that disagreement is unexplained in the literature. Each one sits on one version and more than 3σ from the other. The time-of-swing value implies the measured α to 0.45σ; the angular-acceleration value implies the octahedron's α to 0.35σ.

**Status, stated carefully.**
- **What it is:** an observation, not evidence. Sixteen measurements spread over hundreds of ppm, and two of them happening to land on two predictions 44 ppm apart could be chance. The octahedron's α is itself a 2 ppm-level formula, and the docs say its residual "will be addressed".
- **Why it is still useful:** it turns the framework's open question about α's next-order correction into something G can measure. A future G measurement at ≤ 10 ppm, or a resolution of the HUST discrepancy, decides whether gravity's 21 levels count the **measured** α or the **octahedron's** α. The two differ by 44 ppm.
- **The two outcomes:** if G settles near 6.67451, the per-level factor is purely topological and α's 2 ppm residual is an electromagnetic correction that gravity does not see. If G settles near 6.67422, gravity uses the full measured α.

## 39. Checked against data beyond CODATA 2022

**NIST 2026.** Schlamminger et al., *Metrologia* **63**, 025012 (April 2026), redetermined G with the BIPM torsion balance under a blind analysis: $G = 6.67387 \times 10^{-11}$, 57 ppm.

| Version | vs NIST 2026 |
|---|---|
| measured α, 6.674219 | +52 ppm, z = +0.92 |
| octahedron's α, 6.674510 | +96 ppm, z = +1.68 |

NIST lies below both. It mildly prefers the measured-α version, but excludes neither. NIST's value also sits about 250 ppm below the 2007 BIPM result it set out to replicate, which deepens the scatter rather than resolving it. **By [`PREREGISTRATION.md`](../g_from_topology/PREREGISTRATION.md) this is a cross-check, not a test:** it was published before the 9 November 2026 registration.

**A rival explanation of the HUST split.** Klein (*Class. Quantum Grav.* 2020, arXiv:1901.02604) argues that the HUST time-of-swing/feedback gap, and BIPM's internal gap, are removed by MOND corrections with one fitted interpolation function. Scarpa, Falomo and Treves (arXiv:2603.17770, 2026) find that the laboratory-tuned function differs from the galactic one. Under GFD's own $\mu(x) = x/(1+x)$, Earth's field as the external field gives $1 - \mu \approx 10^{-11}$: no laboratory effect at all. So Klein's mechanism is **not** GFD's, and if it is right, the HUST split has nothing to do with α. A second, conventional explanation also exists: the time-of-swing method depends on fibre anelasticity, which the feedback method avoids.

**Where this leaves Part XI.** The HUST split is unexplained, and it now has at least three candidate explanations:
1. fibre anelasticity (time-of-swing only);
2. a non-standard MOND function (Klein);
3. two different α's (this Part).

The data after CODATA (NIST 2026) lean slightly towards the measured α. The question in §38 stays open, and the next registered measurements will decide it.

---

# Part XII. "One α per level" as a theorem

*Checked by [`verify_exponent_theorem.py`](verify_exponent_theorem.py) (7/7).*

## 40. The theorem

**Premises.** Each is either the framework's own principle or a result of an earlier Part.
- **P1, self-similarity.** Every junction is the same unit: G's blocks are tensor powers of one matrix $L$ (the author's Sierpiński diagram). So every junction carries the same factor.
- **P2, the snapshot.** Nothing the read depends on may change while it settles (Paper I; the author's note in the README). So within one closure the coupling runs **one way, in read order**, and the network matrix is block-triangular in that order.
- **P3, calibration.** Electromagnetism is one junction, and its factor is $\alpha$, by the definition of $\alpha$ as the electromagnetic coupling.

**Lemma (triangular determinant).** If $M = D + E$ with $E$ strictly block-lower in read order, then $\det M = \det D$, the product of the junction factors, **for every choice of couplings $E$**. Checked on 200 random one-way couplings of arbitrary size, and on the registered tree read down only or up only.

**Theorem.** Under P1–P3, the closure amplitude is

$$\det\big[\alpha(B + E)\big] = \alpha^{\#\text{junctions}} = \alpha^{21},$$

**independently of how the levels are coupled**, provided the read is one-way.

This turns "one α per level" from an assumption into a consequence of the framework's own principles. It also explains why the result is so robust: the exponent cannot depend on the details of the inter-level coupling, because a causal (read-ordered) network's determinant never sees those details.

## 41. The converse explains the failed network, and the data bound it

**Back-reaction breaks the theorem.** The pre-registered network of Parts VI–VII had two-way edges: the response returns up the tree within the same closure. With back-reaction of relative strength $\varepsilon$, exactly,

$$\frac{\det}{\alpha^{21}} = (1 - \varepsilon)\,(1 - 4\varepsilon + 5\varepsilon^2 - 10\varepsilon^3) = 1 - 5\varepsilon + O(\varepsilon^2).$$

It is 1 at $\varepsilon = 0$ and **exactly 0 at $\varepsilon = 1$**: the registered symmetric network is the full-back-reaction limit, which is why it gave a zero TetA amplitude. The two negative results were not failures of the framework. They were the theorem's converse.

**The data bound back-reaction.** With the prefactor and loop factor fixed, the measured G gives the exponent as

$$n = 20.999998 \pm 0.000005,$$

and the closure amplitude may differ from $\alpha^{21}$ by at most −33 to +57 ppm (2σ). Hence:

$$|\varepsilon| < 1.1 \times 10^{-5} \quad\text{of the forward coupling.}$$

**Within one closure the read is one-way to one part in $10^5$.** The snapshot principle (P2), the framework's founding requirement, is the premise G measures most directly.

## 42. Which α, and what remains

- **P3 fixes the measured α.** The junction is calibrated by electromagnetism, so the theorem predicts the pre-registered $G = 6.674219 \times 10^{-11}$, not Part XI's octahedron-α value. If future G measurements land near 6.67451, it is P3 that fails: the junction would be calibrated by the bare state count $137 + 1/28$, not by the physical electromagnetic coupling.
- **What is now derived:**
  - the exponent, from P1–P3 (§40);
  - the loop factor, from P2 plus uniform phase (Part VIII);
  - the numerator 17, from exchange symmetry (Part IX).
- **What is still identified rather than derived:** the denominator 13 as the bound source in TetB.
- **What the conditional bound assumes.** The back-reaction bound holds with 17/13 and the loop factor exact, and for back-reaction along the closure tree. A different back-reaction pattern gives a different coefficient, but the same conclusion: any feedback at the $10^{-5}$ level would show up in G.

**The understanding gained, in one sentence.** Gravity is weaker than electromagnetism by $\alpha^{20}$ because a closure is a causal, one-way read through 21 identical junctions. The determinant of a causal network is the product of its junctions, so each junction contributes exactly the electromagnetic coupling, and the measured G confirms that the read has no back-reaction to one part in $10^5$.

---

# Part XIII. Gravity starts at 13

*The author's statement: 13 is where gravity starts; below it is the photonic matrix of light ([`photonic/`](../photonic/the-pixel-and-the-lattice.md)). Checked by [`verify_gravity_starts_at_13.py`](verify_gravity_starts_at_13.py) (7/7).*

## 43. What the framework's own equations say

The continuous capacity in [`the-pixel-and-the-lattice.md`](../photonic/the-pixel-and-the-lattice.md) is $f(x) = (21x + 13)/(x + 1)$. Exactly:

- $f(x) \to 13$ as $x \to 0$, the **field-free limit**, and $f(x) \to 21$ as $x \to \infty$.
- $f(x) - 13 = 8\,\mu(x)$. **Gravity's response is the capacity above 13.**
- For every field strength $x > 0$, $13 < f(x) < 21$, and $f$ rises strictly from 13 the moment any field is present.

So **13 is the capacity of the substrate with no gravitational field**: $\mu = 0$, nothing resolved through TetA. In the photonic notes' terms, that is the unorganised matrix of light, pixels not yet packed into a pocket. Every gravitational state lies strictly above it. Nothing gravitational lives at or below 13. The author's reading is exactly what the constitutive law says.

## 44. What it gives G

With gravity starting at 13, the prefactor has a single meaning:

$$\frac{17}{13} = \frac{\text{mean capacity of a closure}}{\text{capacity of the field-free substrate}}.$$

The numerator is the exchange-symmetric mean of a closure that breathes from the floor (Part IX). The denominator is the floor itself, the substrate in which every closure starts. G is a closure's average capacity measured **in units of the bare photonic matrix**.

The measured G confirms the reference point. Taking the reference at the floor gives 12 ppm; at the Field Origin, −24%; at the TetA ceiling, −38%.

**This replaces the "bound source in TetB" identification of Part IX.** That identification relied on Paper VII's statement about where matter sits. This one needs only the constitutive law's zero point, $f(0) = 13$. The two agree, since matter is light trapped below the gate, but the new reading is the cleaner one. It is a property of $f(x)$, not a claim about particles.

## 45. G, end to end

Each factor is now *(an average over a closure)* or *(a product over its junctions)*, relative to *the state at which the closure starts*:

$$\alpha_G \;=\; \underbrace{\alpha^{21}}_{\substack{\text{one-way read through 21 identical junctions,}\\ \text{each calibrated by electromagnetism (Part XII)}}} \times \underbrace{\frac{\langle f\rangle}{f(0)} = \frac{17}{13}}_{\substack{\text{mean capacity over the}\\ \text{field-free floor (IX, XIII)}}} \times \underbrace{\frac{\mathbb E[\text{tiles}]}{N} = 1 + \frac{\alpha}{2\pi}}_{\substack{\text{seam average over the}\\ \text{ideal count (VIII)}}}$$

| Ingredient | Premise | Status |
|---|---|---|
| $\alpha^{21}$ | self-similar junctions; one-way read (snapshot); EM calibration | theorem; back-reaction $< 10^{-5}$ by G |
| 17 | exchange symmetry of the breath | theorem |
| 13 | the closure starts from the field-free substrate, $f(0) = 13$ | read off the constitutive law; matches the author's photonic picture; only reference that fits G |
| $1 + \alpha/2\pi$ | atomic closure reads every touched tile; uniform phase | theorem; predicts no $\alpha^2$ term |

**What remains assumed, stated plainly.**
- Normalising by the closure's starting state follows Paper I's order (the read comes first, so the snapshot is taken at the start). That is the framework's principle applied once more, not an independent proof.
- The provenance cannot be settled from git. The photonic notes, Paper VII's TetB statements and the 17/13 formula entered the repository in a single import commit, so the agreement with the measured G is not a blind test. The blind tests are the ones already stated: no $\alpha^2$ term (~1 ppm), and measured α against the octahedron's α (~10 ppm).

---

# Part XIV. What follows from "gravity starts at 13"

*Checked by [`verify_closure_ladder.py`](verify_closure_ladder.py) (8/8); pre-registered test and DR4 prediction in [`BREATH_RESULT_AND_DR4_PREDICTION.md`](BREATH_RESULT_AND_DR4_PREDICTION.md).*

## 46. The closure ladder: why only electromagnetism and gravity

Apply Part XIII's reading to a closure of any depth $n$, with levels $1, K, \dots, K^{n-1}$ and odd levels flipped by parity:
- junctions: $J_n = (K^n - 1)/(K - 1)$;
- field-free floor: $F_n = (1 - (-K)^n)/(1 + K)$;
- symmetric mean: $E_n$, the sum of the even-level sizes;
- coupling: $\alpha_n = (E_n/F_n)\,\alpha^{J_n}$.

**Theorem.** The floor is positive **exactly when $n$ is odd**. If a closure needs a substrate beneath it (a positive floor, Part XIII), the allowed closures are:

| Depth | Coupling | |
|---|---|---|
| 1 | $1 \cdot \alpha^{1}$ | **electromagnetism**: prefactor exactly 1, as calibration requires |
| 2 | — | forbidden (floor −3) |
| 3 | $\tfrac{17}{13}\,\alpha^{21}$ | **gravity** |
| 4 | — | forbidden (floor −51) |
| 5 | $\tfrac{273}{205}\,\alpha^{341}$ | $\sim 10^{-729}$, physically empty |

So one rule gives both of the long-range couplings, electromagnetism and gravity, and **nothing in between**. For odd $n$ the prefactor is $(K^{n+1}-1)/\big((K-1)(K^n+1)\big)$, which gives 1 at $n = 1$ and 17/13 at $n = 3$, and tends to $4/3$.

Gravity's depth is $D = 3$ (face, channel, subchannel), and the theorem requires it to be odd. This is the same oddness that lets spatial parity change the tetrad's root (the scheme proof's "because three is odd").

**Conflicts, stated.** The archive's $\eta_B = 29.4\,\alpha^5$ uses the depth-2 exponent, and depth 2 is forbidden by this rule. Its $\Lambda \propto \alpha^{57}$ is not a ladder exponent either. Either those formulas need a different origin, such as a product of closures, or the floor rule is incomplete.

## 47. A second reading, tested: does the breath depend on the field?

The prefactor's 17 is the mean of a full breath, 13 → 21. Only a Newtonian field reaches 21. If, in a field $x$, the breath runs only up to $f(x)$, then $G_{\text{eff}}/G = (x + 13/17)/(x + 1)$. This is exactly equivalent to $a_0 \to \tfrac{13}{17}a_0$.

- **SPARC (pre-registered, 347f611): undecided.** σ is unchanged at 0.1814 dex. A rescaled $a_0$ is absorbed along the mass-to-light direction.
- **Gaia DR4 (registered here, before its 2 December 2026 release).** Using the archive's own solver: H_breath gives $R = 1.126$ (1.118–1.131), the registered GFD gives $R = 1.163$ (1.138–1.184), and Newton gives 1.000. The ranges do not overlap, so DR4 decides whether G's prefactor is a universal constant or runs with the local field.

## 48. What "gravity starts at 13" has produced

1. **A selection rule:** only odd-depth closures exist. Depth 1 is electromagnetism with prefactor exactly 1, depth 3 is gravity with 17/13, and there is no rung between them.
2. **Agreement with the constitutive law:** the field-free floor is $f(0) = 13$, and gravity is the excess $f - 13 = 8\mu$.
3. **Two internal conflicts flagged:** the archive's α⁵ for baryogenesis and α⁵⁷ for Λ do not fit the ladder.
4. **A falsifiable fork for Gaia DR4:** a universal breath ($R = 1.163$) against a field-set breath ($R = 1.126$).

---

```bash
python research/algebra-intersection/verify_intersection.py            # Part I:  63/63 PASS
python research/algebra-intersection/verify_octahedral_connection.py   # Part II: 48/48 PASS
python research/algebra-intersection/verify_cube.py                    # Part III: 38/38 PASS
python research/algebra-intersection/verify_walsh.py                   # Part IV: 26/26 PASS
python research/algebra-intersection/verify_closure_tree.py            # Part V:  16/16 PASS
python research/algebra-intersection/verify_sweep_sierpinski.py        # Part VI: 10/10 PASS
python research/algebra-intersection/verify_one_loop_fencepost.py      # Part VII: 6/6 PASS
python research/algebra-intersection/verify_seam_average.py           # Part VIII: 7/7 PASS
python research/algebra-intersection/verify_prefactor_exchange.py     # Part IX:  6/6 PASS
python research/algebra-intersection/verify_level_factor.py           # Part X:   8/8 PASS
python research/algebra-intersection/verify_topological_alpha_in_G.py # Part XI: 11/11 PASS
python research/algebra-intersection/verify_exponent_theorem.py       # Part XII:  7/7 PASS
python research/algebra-intersection/verify_gravity_starts_at_13.py  # Part XIII: 7/7 PASS
python research/algebra-intersection/verify_closure_ladder.py         # Part XIV:  8/8 PASS
python research/algebra-intersection/breath_sparc.py                  # pre-registration 3 (undecided)
python research/algebra-intersection/breath_wide_binaries.py          # H_breath DR4 prediction (needs scipy; ~2 min)
python research/algebra-intersection/network_model.py                 # registered network model (fails; see NETWORK_MODEL_RESULT.md)
```
