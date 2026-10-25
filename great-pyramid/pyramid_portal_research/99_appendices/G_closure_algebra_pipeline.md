# The Closure Algebra Pipeline: A Unified Algebraic System

**Author:** Stephen Nelson / Field Dynamics Research
**Date:** May 2026
**Companion to:** *Walsh-Spectral Compute Primitive: Algebraic and Engineering Synthesis*

---

## Spine

| Stage | Name | Object | Role |
|---|---|---|---|
| 1 | State law | $\oplus$ on $(\mathbb{Z}/2)^n$ | Boolean composition; cube as substrate |
| 2 | Orientation | Cocycle $\sigma(a, b)$ | Twists Walsh group algebra into Clifford |
| 3 | Closure | Operator $\Omega$, $\Omega^3 = 1$ | Order-3 cyclic action; terminates sweeps |
| 4 | Decomposition | $\mathcal{A}_3 = \langle 1, I \rangle \oplus \mathbb{Z}[\omega]^3$ | $\Omega$-eigenspace splitting |
| 5 | Coupling polynomial | $f(K, s) = 1 + sK + K^2$ | Trace of $K$-scaling on each channel |
| 6 | Operator algebra | Composition, sweep multiplication | Two distinct binary operations |
| 7 | Closure norm | $N_{\mathcal{A}}(F)$ | Number-theoretic complexity measure |
| 8 | Projective tower | $S(D, K) = |\mathbb{P}^{D-1}(\mathbb{F}_{K^2})|$ | Depth scaling = field extension tower |
| 9 | Hardware target | LUT-6 = $\mathcal{A}_3^{\otimes 2}$ | FPGA primitive realization |
| 10 | Dynamical realization | GFD oscillator Jacobian | Closure algebra in continuous time |

---

## Abstract

A closure algebra is a quadruple $\mathcal{A} = (A, \oplus, \sigma, \Omega)$ where $\oplus$ is a state law (Boolean group operation), $\sigma$ is an orientation cocycle (sign twist), and $\Omega$ is a closure operator (finite-order cyclic action). At dimension three, the unique such algebra is

$$\mathcal{A}_3 \;=\; \langle 1, I \rangle \;\oplus\; \mathbb{Z}[\omega]^3$$

a 2-dimensional Gaussian axial summand plus three Eisenstein-integer hexagonal channels, isomorphic as a graded vector space to the Clifford algebra $\mathrm{Cl}(3, 0)$. This document lays out the pipeline by which Walsh-spectral compute, Clifford geometry, Eisenstein number theory, and the GFD coupling polynomial $f(K, s) = 1 + sK + K^2$ are projections of one algebraic object. Each stage of the pipeline is defined precisely, and the GFD coupling polynomial appears as the trace of the $K$-scaling action on the three structural channels at the three discriminant-irreducible parities $s \in \{-1, 0, +1\}$.

---

# Part I: The Pipeline

## Stage 1 — State law: the cube as substrate

**Object.** The state space is the elementary abelian 2-group $G = (\mathbb{Z}/2)^n$, equivalently the cube $\{-1, +1\}^n$ under coordinate-wise multiplication.

**State law.** $\oplus$ is the group operation:
- On $\mathbb{F}_2^n$: bitwise XOR.
- On $\{-1,+1\}^n$: coordinate-wise multiplication.

**Walsh basis.** The characters $\chi_S : G \to \{-1, +1\}$ for $S \subseteq \{1, \ldots, n\}$:
$$\chi_S(x) = \prod_{i \in S} x_i.$$
There are $2^n$ characters, indexed by subsets $S$. They are an orthogonal basis for $\mathbb{R}[G]$ under the inner product $\langle f, g \rangle = \frac{1}{2^n} \sum_x f(x) g(x)$.

**FWHT.** The Fast Walsh-Hadamard Transform is the change-of-basis from the standard basis (delta functions at vertices) to the Walsh basis:
$$\widehat f(S) \;=\; \frac{1}{2^n} \sum_{x \in G} f(x) \chi_S(x).$$
Implementation: $\widehat f = \frac{1}{2^n} H_n f$ where $H_n$ is the Walsh-Hadamard matrix at order $2^n$.

**Bridge.** A *bridge* is a Walsh coefficient vector $b \in \mathbb{R}^{2^n}$. It defines an operator $T_b$ on $G$:
$$T_b(x) \;=\; \mathrm{sign}\!\left( \frac{1}{2^n} H_n \, \mathrm{diag}(b) \, H_n \, x \right).$$
This is the spectral kernel — the bridge IS the universal Boolean gate. Composition of bridges = multiplication of Walsh-diagonal operators followed by re-thresholding; collapses to a single LUT at compile time.

**At $n = 3$.** The cube has 8 vertices. Walsh basis splits by Hamming weight $|S|$ into 1 + 3 + 3 + 1 = 8 modes — the eventual $\mathrm{Cl}(3, 0)$ grading.

The state law alone gives Boolean computation. It does not yet have orientation or closure.

---

## Stage 2 — Orientation cocycle: Clifford emerges

**The problem.** The Walsh group algebra $\mathbb{R}[G]$ is commutative — it cannot be a Clifford algebra, which has $e_i e_j = -e_j e_i$ for $i \neq j$. To produce Clifford structure, the multiplication must be *twisted*.

**The cocycle.** A 2-cocycle $\sigma: G \times G \to \{\pm 1\}$ is a sign function satisfying the cocycle condition
$$\sigma(a, b) \, \sigma(a + b, c) \;=\; \sigma(a, b + c) \, \sigma(b, c).$$
The cocycle defines a twisted group algebra $\mathbb{R}[G]_\sigma$ with multiplication
$$e_a \cdot e_b \;=\; \sigma(a, b) \, e_{a + b}.$$
For the cube cocycle
$$\sigma(a, b) \;=\; (-1)^{\sum_{i > j} a_i b_j}$$
this twisted group algebra is precisely the Clifford algebra:
$$\mathbb{R}[(\mathbb{Z}/2)^n]_\sigma \;\cong\; \mathrm{Cl}(n, 0).$$

**At $n = 3$.** The 8 basis elements $\{e_a : a \in \mathbb{F}_2^3\}$ become the Clifford basis $\{1, e_1, e_2, e_3, e_{12}, e_{13}, e_{23}, e_{123}\}$, with grade given by Hamming weight $|a|$. The orientation cocycle realizes the Clifford anticommutation $e_i e_j = -e_j e_i$ exactly.

**Grade decomposition.**
| Grade $k$ | $\dim$ | Basis | Walsh $|S|$ |
|---|---|---|---|
| 0 (scalar) | 1 | $1$ | 0 |
| 1 (vector) | 3 | $e_1, e_2, e_3$ | 1 |
| 2 (bivector) | 3 | $e_{12}, e_{13}, e_{23}$ | 2 |
| 3 (pseudoscalar) | 1 | $I = e_{123}$ | 3 |

Total: $1 + 3 + 3 + 1 = 8 = 2^3$. The pseudoscalar $I$ satisfies $I^2 = -1$, making $\langle 1, I \rangle$ a copy of the complex numbers $\mathbb{C}$ inside Cl(3, 0).

The orientation cocycle alone gives geometry. It still lacks closure: the algebra is infinite-order in the sense that products of grade-1 elements can climb to all higher grades without termination.

---

## Stage 3 — Closure operator: Eisenstein action

**The closure operator.** Define $\Omega: \mathrm{Cl}(3, 0) \to \mathrm{Cl}(3, 0)$ as the order-3 algebra automorphism that cyclically permutes the three coordinate axes:
$$\Omega: e_1 \to e_2 \to e_3 \to e_1.$$
Extending multiplicatively: $\Omega(e_{12}) = e_{23}$, $\Omega(e_{23}) = e_{31}$, $\Omega(e_{31}) = e_{12}$. The scalar 1 and pseudoscalar $I = e_{123}$ are $\Omega$-fixed.

This is the rotation by $2\pi/3$ around the cube body diagonal $(1, 1, 1)$ — geometrically natural, algebraically fundamental.

**Order-3 closure.** $\Omega^3 = \mathrm{id}$. The minimal polynomial of $\Omega$ on Cl(3, 0) is
$$X^3 - 1 \;=\; (X - 1)(X^2 + X + 1) \;=\; \Phi_1(X) \cdot \Phi_3(X).$$
On the $\Omega$-fixed subspace, $\Omega$ acts as identity; on the complementary subspace, $\Omega$ acts with minimal polynomial $\Phi_3$ — i.e., as multiplication by a primitive cube root of unity.

**Eisenstein structure.** Because $\Phi_3(\Omega) = \Omega^2 + \Omega + 1 = 0$ on the non-fixed subspace, that subspace carries a natural $\mathbb{Z}[\omega]$-module structure where $\omega$ acts as $\Omega$.

**Closure-driven termination.** The 3-sweep recursion $S(D+1, K) = K^2 \cdot S(D, K) + 1$ terminates at depth 3 because $\Omega^3 = 1$: the third sweep returns to the starting orbit, contributing nothing new (Vote₃ = 0 in the dynamical synthesis).

The closure operator alone gives finite-order cyclic structure. Combined with the prior stages, it gives the full closure algebra.

---

## Stage 4 — The $\Omega$-eigenspace decomposition

**The decomposition.**
$$\mathcal{A}_3 \;=\; \underbrace{\langle 1, I \rangle}_{\Omega\text{-fixed, dim 2}} \;\oplus\; \underbrace{\mathbb{Z}[\omega]^3}_{\Omega\text{-cycled, dim 6}}$$
as a graded vector space (NOT as an algebra — the summands are not closed under Clifford multiplication; products mix them).

**Axial channel** $\langle 1, I \rangle$. Two real dimensions. Both basis elements $1$ and $I = e_{123}$ are fixed by $\Omega$ (the body-diagonal rotation leaves them invariant). Internally, $I^2 = -1$ makes $\langle 1, I \rangle$ a Gaussian field copy:
$$\langle 1, I \rangle \;\cong\; \mathbb{R}[X] / (X^2 + 1) \;\cong\; \mathbb{C}.$$

**Hexagonal channels** $\mathbb{Z}[\omega]^3$. Six real dimensions split as three complex (Eisenstein) channels:
$$z_k \;=\; e_k + \omega \cdot e_{(k+1)(k+2)}, \qquad k = 1, 2, 3$$
where indices are mod 3 (so $z_1 = e_1 + \omega e_{23}$, $z_2 = e_2 + \omega e_{31}$, $z_3 = e_3 + \omega e_{12}$). Each $z_k$ pairs a vector with its dual bivector via the cube root of unity $\omega = e^{2\pi i / 3}$.

**$\Omega$ action on hexagonal channels.** $\Omega$ cyclically permutes $z_1 \to z_2 \to z_3 \to z_1$. The triple $(z_1, z_2, z_3)$ is one $\Omega$-orbit of length 3, with $\Omega$ acting as a 3-cycle.

Each $z_k$ as a free $\mathbb{Z}[\omega]$-module of rank 1 carries Eisenstein arithmetic. Multiplication of $z_k$ by $\omega$ is exactly multiplication of $(e_k + \omega e_{(k+1)(k+2)})$ by $\omega$, giving $(\omega e_k + \omega^2 e_{(k+1)(k+2)})$ — a phase rotation.

**Why "$2 + 3\omega$".** The decomposition has 2 real-axial channels + 3 complex-Eisenstein channels. Real dimension count: $2 + 3 \times 2 = 8$, matching $\mathrm{Cl}(3, 0)$. The shorthand $2 + 3\omega$ records this.

**Geometric realization.** The body-diagonal projection of the cube (Part V §20 of the synthesis document) realizes this decomposition geometrically: 2 cube vertices project to the origin (axial) and 6 cube vertices form the hexagon (Eisenstein lattice fundamental cell, three pairs).

---

## Stage 5 — The GFD coupling polynomial

This is the bridge between the closure algebra paradigm and the GFD framework. The coupling polynomial $f(K, s) = 1 + sK + K^2$ is the trace of the $K$-scaling action on the structural channels of $\mathcal{A}_3$, evaluated at the three discriminant-irreducible parities.

### 5.1 Statement

For integer $s$ such that $s^2 < 4$ (i.e., $s \in \{-1, 0, +1\}$), the coupling polynomial $f(K, s) = 1 + sK + K^2$ evaluates to a degree-2 cyclotomic polynomial:
$$f(K, s) \;=\; \begin{cases} \Phi_3(K) = K^2 + K + 1 & s = +1 \\ \Phi_4(K) = K^2 + 1 & s = 0 \\ \Phi_6(K) = K^2 - K + 1 & s = -1 \end{cases}$$
These are the three (and only three) cyclotomic polynomials of degree 2 over $\mathbb{Q}$, corresponding to the three $n$ with $\varphi(n) = 2$, namely $n \in \{3, 4, 6\}$.

### 5.2 Each value is the norm in an imaginary quadratic ring

| $s$ | $f(K, s)$ | Cyclotomic | Field | Norm form |
|---|---|---|---|---|
| $+1$ | $K^2 + K + 1$ | $\Phi_3$ | $\mathbb{Q}(\omega)$ | $N_{\mathbb{Z}[\omega]/\mathbb{Z}}(K - \omega)$ |
| $0$ | $K^2 + 1$ | $\Phi_4$ | $\mathbb{Q}(i)$ | $N_{\mathbb{Z}[i]/\mathbb{Z}}(K - i)$ |
| $-1$ | $K^2 - K + 1$ | $\Phi_6$ | $\mathbb{Q}(\omega)$ | $N_{\mathbb{Z}[\omega]/\mathbb{Z}}(K + \omega)$ |

Verification:
- $(K - \omega)(K - \bar\omega) = K^2 - (\omega + \bar\omega) K + \omega \bar\omega = K^2 + K + 1$ since $\omega + \bar\omega = -1$ and $\omega \bar\omega = 1$. ✓
- $(K - i)(K + i) = K^2 + 1$. ✓
- $(K + \omega)(K + \bar\omega) = K^2 + (\omega + \bar\omega)K + \omega \bar\omega = K^2 - K + 1$. ✓

### 5.3 Each value is the trace on a structural channel

The closure-algebra channels of $\mathcal{A}_3$ each carry an imaginary-quadratic structure:
- **Axial $\langle 1, I \rangle$**: Gaussian, with $I^2 = -1$, ring $\mathbb{Z}[i]$.
- **Hexagonal $z_k$**: Eisenstein, with $\omega^3 = 1$, ring $\mathbb{Z}[\omega]$.

The $K$-scaling action on each channel has characteristic polynomial:

| Channel | Imaginary unit | Characteristic poly of $K$-scaling | Equals |
|---|---|---|---|
| Axial $\langle 1, I \rangle$ | $I$ ($I^2 = -1$) | $K^2 + 1$ | $f(K, 0)$ |
| Hexagonal "+" parity | $\omega$ ($\omega^2 + \omega + 1 = 0$) | $K^2 + K + 1$ | $f(K, +1)$ |
| Hexagonal "−" parity | $-\omega$ ($(-\omega)^2 - (-\omega) + 1 = 0$) | $K^2 - K + 1$ | $f(K, -1)$ |

So **the coupling polynomial $f(K, s)$ at the three forced values $s \in \{-1, 0, +1\}$ traces the $K$-scaling on the three structural channels of $\mathcal{A}_3$** — Gaussian axial, Eisenstein parity-even, Eisenstein parity-odd.

### 5.4 The discriminant constraint $s^2 < 4$ is forced by closure-algebra structure

The discriminant of $f(K, s)$ as a quadratic in $K$ is $\Delta_s = s^2 - 4$. For $f(K, s)$ to be irreducible over $\mathbb{Q}$ — equivalently, to be a cyclotomic polynomial generating an imaginary quadratic field — we need $\Delta_s < 0$:
$$s^2 < 4 \;\Longleftrightarrow\; s \in \{-1, 0, +1\}.$$
At $s = \pm 2$: $\Delta_s = 0$, $f$ becomes $(K \pm 1)^2$, reducible.
At $|s| \geq 3$: $\Delta_s > 0$, $f$ has real roots, splits over $\mathbb{Q}$.

The constraint $s^2 < 4$ is equivalent to $|s| \leq 1$, which is the *parity-tag constraint*: the rank-1 (vielbein) term carries a parity sign $s \in \{-1, +1\}$ or vanishes ($s = 0$). Higher integer values of $s$ would correspond to higher parity charge — which has no closure-algebra interpretation because the only imaginary quadratic structures available are Gaussian and Eisenstein.

### 5.5 The product structure recovers the 3-sweep operator space

$$f(K, +1) \cdot f(K, -1) \;=\; \Phi_3(K) \cdot \Phi_6(K) \;=\; \Phi_3(K^2) \;=\; K^4 + K^2 + 1 \;=\; S(3, K).$$
The TetA × TetB product equals the 3-sweep operator space, which is the projective plane point count $|\mathbb{P}^2(\mathbb{F}_{K^2})|$. **The coupling polynomial's parity values multiply to give the depth-3 closure algebra dimension.**

### 5.6 The range $\Delta f = 2K = 2^D$ at $D = 3$

$$f(K, +1) - f(K, -1) \;=\; 2K.$$
At $K = D + 1 = 4$: $\Delta f = 8 = 2^D$, recovering the cube-fill uniqueness equation as the parity span of the coupling polynomial. This is a third independent route to D=3 uniqueness: vertex-count ($2(D+1) = 2^D$), eigenspectrum ($\{1,D,D,1\} = \binom{D}{k}$), and now coupling polynomial range ($\Delta f = 2K = 2^D$).

### 5.7 Connection decomposition

The connection counts per face derive from the parity values:
$$\frac{f(K, +1) - 1}{2} \;=\; \frac{K^2 + K}{2} \;=\; \binom{K+1}{2} \;=\; 10 \text{ retained per face}$$
$$\frac{f(K, -1) - 1}{2} \;=\; \frac{K^2 - K}{2} \;=\; \binom{K}{2} \;=\; 6 \text{ discarded per face}$$

at $K = 4$. Multiplied by $K = 4$ faces: 40 retained Christoffel components, 24 discarded torsion components, total $K^3 = 64$. The 40 + 24 = 64 affine connection decomposition is recovered as the parity-resolved trace of $f$.

### 5.8 The unified statement

> **The GFD coupling polynomial $f(K, s) = 1 + sK + K^2$ is the trace of the $K$-scaling action on the closure algebra $\mathcal{A}_3 = \langle 1, I \rangle \oplus \mathbb{Z}[\omega]^3$, parameterized by parity $s$, with $s = 0$ tracing the Gaussian axial channel and $s = \pm 1$ tracing the Eisenstein hexagonal channels of opposite parity. The constraint $s^2 < 4$ enforced by polynomial irreducibility over $\mathbb{Q}$ exactly matches the parity-tag constraint on the rank-1 channel, picking out the three cyclotomic polynomials $\{\Phi_3, \Phi_4, \Phi_6\}$ that exhaust the degree-2 imaginary quadratic structures.**

---

## Stage 6 — Operator algebra: composition and sweep

### 6.1 Composition (bridge stacking)

The state-law product on bridges. Given bridges $b_1, b_2, \ldots, b_k \in \mathbb{R}^{2^n}$, the composed operator is
$$T_{b_1} \circ T_{b_2} \circ \cdots \circ T_{b_k}.$$
This is sequential application, with each layer being a Walsh-diagonal followed by sign threshold. At $n = 4$ ($N = 16$) or $n = 6$ ($N = 64$, LUT-6), the composed operator collapses to a single $N$-entry lookup table at compile time.

Composition is the *associative product* of the closure algebra. It corresponds to the multiplication in the spectral kernel.

### 6.2 Sweep multiplication

The closure-induced product. Given $a, b \in \mathcal{A}_3$, define
$$a \star b \;=\; \frac{1}{3}\big(a \cdot b \;+\; \Omega(a) \cdot \Omega(b) \;+\; \Omega^2(a) \cdot \Omega^2(b)\big).$$

**$\Omega$-invariance.** Under $\Omega$:
$$\Omega(a \star b) \;=\; \frac{1}{3}\big(\Omega(a)\Omega(b) + \Omega^2(a)\Omega^2(b) + a \cdot b\big) \;=\; a \star b.$$
So $a \star b$ is $\Omega$-invariant — it lies in the axial summand $\langle 1, I \rangle$ for any inputs.

**Interpretation.** Sweep multiplication averages the ordinary Clifford product over the three closure phases. The result is precisely the projection of $a \cdot b$ onto the $\Omega$-fixed subspace.

**On axial elements.** If $a, b \in \langle 1, I \rangle$ (so $\Omega(a) = a, \Omega(b) = b$), then $a \star b = ab$ — sweep multiplication reduces to ordinary multiplication on the axial channel.

**On hexagonal elements.** If $a = z_1, b = z_1$ (same channel), then
$$z_1 \star z_1 \;=\; \frac{1}{3}(z_1^2 + z_2^2 + z_3^2)$$
which is $\Omega$-symmetric and lives in the axial channel. This is the closure-algebraic analog of "sum of squares" — three Eisenstein squares averaging to a Gaussian-axial result.

**Why this matters.** Sweep multiplication is the natural product on closure algebras: it answers "what survives a full closure cycle" rather than "what is the Clifford product." It is the algebraic content of the 3-sweep recursion: each sweep applies $\Omega$ once, and after three sweeps the cycle closes.

---

## Stage 7 — Closure norm

### 7.1 Definition

For $F \in \mathcal{A}_3$ written in the decomposition basis as
$$F \;=\; a + bI + z_1 E_1 + z_2 E_2 + z_3 E_3$$
where $a, b \in \mathbb{Z}$ are the axial coordinates and $z_k \in \mathbb{Z}[\omega]$ are the Eisenstein hexagonal coordinates (with $E_k$ the $k$-th hexagonal channel basis), the *closure norm* is
$$N_{\mathcal{A}}(F) \;=\; \underbrace{a^2 + b^2}_{\text{Gaussian axial}} \;+\; \sum_{k=1}^{3} \underbrace{N_{\mathbb{Z}[\omega]/\mathbb{Z}}(z_k)}_{\text{Eisenstein hexagonal}}$$
where the Gaussian norm is $|a + bI|^2 = a^2 + b^2$ and the Eisenstein norm of $z = x + y\omega$ is $N(z) = x^2 - xy + y^2$.

### 7.2 Total norm formula

If $z_k = x_k + y_k \omega$:
$$N_{\mathcal{A}}(F) \;=\; (a^2 + b^2) \;+\; \sum_{k=1}^{3}(x_k^2 - x_k y_k + y_k^2).$$
Total: a polynomial in 8 integer variables $(a, b, x_1, y_1, x_2, y_2, x_3, y_3)$.

### 7.3 Number-theoretic interpretation

The closure norm of $F$ is an integer. Its prime factorization in $\mathbb{Z}$ encodes structural information:
- Primes ramifying in $\mathbb{Z}[i]$ (i.e., 2) appear from the axial part.
- Primes ramifying in $\mathbb{Z}[\omega]$ (i.e., 3) appear from the hexagonal part.
- Primes splitting in both (those $\equiv 1 \pmod{12}$) can come from either.
- Primes inert in both (those $\equiv 11, 17, 19, 23 \pmod{24}$) appear with even exponent.

This gives a number-theoretic classification of operators by their closure norm's prime factorization. Two operators with the same Eisenstein/Gaussian prime profile share structural properties.

### 7.4 Compute-complexity connection (conjecture)

The hypothesis to test: gates with low closure norm correspond to circuits with low complexity in some natural measure (NAND count, depth, or both). Specifically, *prime* operators in the closure norm should correspond to "irreducible" gates that cannot be factored into simpler compositions.

This is a research program, not a theorem. It would replace gate-counting by Eisenstein lattice arithmetic, turning circuit synthesis into a lattice-reduction problem over $\mathbb{Z}[\omega]^3$.

---

## Stage 8 — Projective tower: depth scaling

### 8.1 The Sierpinski recursion

The cumulative operator-space dimension at branching $K$ over $D$ self-similar Sierpinski sweeps is
$$S(D, K) \;=\; \sum_{k=0}^{D-1} K^{2k} \;=\; \frac{K^{2D} - 1}{K^2 - 1}.$$
Recursion: $S(D+1, K) = K^2 \cdot S(D, K) + 1$.

### 8.2 Projective plane identification

$$S(D, K) \;=\; \big|\mathbb{P}^{D-1}(\mathbb{F}_{K^2})\big|.$$
At $D = 3$, $K = 4$: $273 = |\mathbb{P}^2(\mathbb{F}_{16})|$.

### 8.3 Frobenius decomposition is the parity duality

In $\mathbb{P}^{D-1}(\mathbb{F}_{K^2})$, the Frobenius automorphism $\sigma: x \to x^K$ has fixed points $\mathbb{P}^{D-1}(\mathbb{F}_K)$. The decomposition
$$|\mathbb{P}^{D-1}(\mathbb{F}_{K^2})| \;=\; |\mathbb{P}^{D-1}(\mathbb{F}_K)| \;+\; 2 \cdot (\text{Galois-conjugate pairs})$$
maps onto the closure-algebra decomposition: the $\Omega$-fixed (real) points correspond to the axial channel; the Galois-conjugate pairs (Frobenius-twisted) correspond to the hexagonal channels.

At $D = 3, K = 4$: $273 = 21 + 252$, with 21 = $|\mathbb{P}^2(\mathbb{F}_4)|$ Frobenius-fixed and $252 = 2 \times 126$ as 126 Galois-conjugate pairs. The polynomial identity
$$\Phi_3(K^2) \;=\; \Phi_3(K) \cdot \Phi_6(K)$$
expresses this as: total points = ($\mathbb{F}_K$-points) × (per-point Galois twist factor $\Phi_6(K)$).

### 8.4 Cohomology relation as Vote_D = 0

The closure $h^D = 0$ in $H^*(\mathbb{CP}^{D-1}; \mathbb{Z}) = \mathbb{Z}[h]/(h^D)$ corresponds to Vote_D = 0 in the GFD oscillator dynamics. This is the Sierpinski recursion's termination condition:
$$\Omega^D = 1 \;\Longrightarrow\; h^D = 0 \;\Longrightarrow\; \text{Vote}_D = 0.$$
At $D = 3$, this terminates the universal Boolean gate's compute budget at exactly 273 dimensions.

---

## Stage 9 — Hardware compile target

### 9.1 LUT-6 as $\mathcal{A}_3^{\otimes 2}$

A standard FPGA LUT-6 stores 64 truth-table bits — algebraically a 6-cube Walsh vector. By tensor decomposition:
$$\text{LUT-6} \;=\; \mathrm{Cl}(3, 0) \otimes \mathrm{Cl}(3, 0) \;=\; \mathcal{A}_3^{\otimes 2}.$$
Each LUT-6 is two stellated-octahedron compute units tensored, equivalently two closure algebras at $D = 3$ paired.

The Walsh coefficient vector for a 6-bit Boolean operator is
$$b \;\in\; \mathbb{R}^{64} \;\cong\; (\mathbb{R}^8)^{\otimes 2} \;\cong\; \mathcal{A}_3^{\otimes 2}.$$
Bridge composition = LUT chaining = single-cycle BRAM read on FPGA.

### 9.2 Hexagonal addressing

The $\mathcal{A}_3$ decomposition $\langle 1, I \rangle \oplus \mathbb{Z}[\omega]^3$ suggests a *hexagonal* memory access pattern as the natural compile target for closure-algebra arithmetic. Each $\mathbb{Z}[\omega]$-channel can be addressed as a 2-dimensional Eisenstein-coordinate lookup; the axial channel as a Gaussian-coordinate lookup. Standard square-grid memory tiles do not match this structure; hexagonal memory tiles would.

### 9.3 Preflight margin discipline

The threshold step $\mathrm{sign}(\cdot)$ in the spectral kernel is robust as long as no element of the pre-threshold value is too close to zero. The closure-algebra interpretation: pre-threshold zero margins correspond to operators that are *boundary points* of the closure-norm lattice — operators whose Eisenstein/Gaussian decomposition has rank-degenerate components. Preflight checks at compile time flag these and exclude them.

---

## Stage 10 — Dynamical realization

### 10.1 GFD oscillator as closure algebra dynamics

The GFD oscillator's Jacobian at the fixed point IS a Walsh-diagonal operator on $\{-1, +1\}^3$ with $S_K \times \mathbb{Z}_2$ symmetry. Its eigenstructure $\{1, D, D, 1\}$ matches the Cl(3, 0) grade decomposition exactly, and its eigenvalue ratio $D = 1/\mathrm{Gram}$ realizes the closure-norm parity weighting between axial and hexagonal channels.

The 3+1 nested oscillator hierarchy realizes the depth-tower $S(D, K)$ for $D = 1, 2, 3, (4)$, with each level a complete $\mathcal{A}_3$ block. The cascade coupling (top-down 0.031→0.030→0.026, bottom-up 0.004→0.003→0.001, Vote₃ ≈ 0) is the projective-tower point count realized as continuous-time dynamics.

### 10.2 ε² selection rule

The one-directional grade-1 → grade-0 nonlinear vertex (with grade-0 → grade-1 exactly zero) is the **closure-algebra selection rule**: hexagonal-channel perturbations can source the axial channel (via sweep multiplication, which projects onto $\Omega$-fixed), but axial-channel perturbations cannot source hexagonal channels (no projection in that direction). This is the GR-style symmetry selection rule classically realized.

### 10.3 Heisenberg correspondence

The K=4 Heisenberg system at $J = 1/D = 1/3$ shares the $S_4$-irrep skeleton of $\mathcal{A}_3$ on the trivial and standard representations. The hook irrep $[2, 2]$ that appears in the quantum spectrum but not in the closure algebra is the genuinely-quantum entanglement sector — closure algebra is inherently classical.

---

# Part II: The Pipeline as One System

## The unified diagram

```
                      State space
                      G = (Z/2)^n
                          │
                          │  (Walsh basis)
                          ▼
    ┌──────────────── R[G] ─────────────────┐
    │     commutative group algebra          │
    │     bridges = coefficient vectors      │
    └────────────────────┬───────────────────┘
                         │
                         │  (orientation cocycle σ)
                         ▼
    ┌──────────── R[G]_σ ≅ Cl(n,0) ──────────┐
    │     graded by Hamming weight |S|       │
    │     {1, 3, 3, 1} at n=3 (binomial)     │
    └────────────────────┬───────────────────┘
                         │
                         │  (closure operator Ω, Ω³=1)
                         ▼
    ┌──── A_3 = ⟨1,I⟩ ⊕ Z[ω]³ ──────────────┐
    │     Ω-fixed: 2-dim Gaussian axial      │
    │     Ω-cycled: 3-dim Eisenstein hex.    │
    └────────────────────┬───────────────────┘
                         │
                         │  (K-scaling, parity s ∈ {-1, 0, +1})
                         ▼
    ┌──── f(K,s) = 1 + sK + K² ──────────────┐
    │     s=0:  Φ_4 = K²+1   (Gaussian)      │
    │     s=+1: Φ_3 = K²+K+1 (Eisenstein +)  │
    │     s=-1: Φ_6 = K²-K+1 (Eisenstein −)  │
    └────────────────────┬───────────────────┘
                         │
                         │  (depth tower D, Frobenius)
                         ▼
    ┌──── S(D,K) = |P^(D-1)(F_{K²})| ────────┐
    │     D=2: |P^1(F_16)| = 17  (impedance) │
    │     D=3: |P^2(F_16)| = 273 (operator)  │
    │     D=4: |P^3(F_16)| = 4369            │
    │     ... (Vote_D = 0 ⟺ h^D = 0)         │
    └────────────────────┬───────────────────┘
                         │
                         │  (LUT compile target)
                         ▼
              FPGA LUT-6 = A_3 ⊗ A_3
                         │
                         ▼
                  Physical realization:
              GFD oscillator (continuous time)
              FPGA spectral kernel (deterministic)
              Heisenberg K=4 system (quantum)
```

## The unified statement

> **A closure algebra is a quadruple $(A, \oplus, \sigma, \Omega)$ where $\oplus$ is a state law on an elementary abelian 2-group, $\sigma$ is an orientation cocycle (Clifford twist), and $\Omega$ is a finite-order closure operator. At dimension three, the unique closure algebra is $\mathcal{A}_3 = \langle 1, I \rangle \oplus \mathbb{Z}[\omega]^3$ — a 2-dimensional Gaussian axial summand plus three Eisenstein-integer hexagonal channels, isomorphic as a graded vector space to $\mathrm{Cl}(3, 0)$. The GFD coupling polynomial $f(K, s) = 1 + sK + K^2$ is the trace of the $K$-scaling action on these channels parameterized by parity $s$, with $s = 0$ tracing the Gaussian axial channel and $s = \pm 1$ tracing the Eisenstein hexagonal channels of opposite parity. The discriminant constraint $s^2 < 4$ enforced by polynomial irreducibility over $\mathbb{Q}$ exactly matches the parity-tag constraint, picking out the three cyclotomic polynomials $\{\Phi_3, \Phi_4, \Phi_6\}$ that exhaust the degree-2 imaginary-quadratic structures. Depth scaling realizes the cumulative operator space as the projective-plane tower $S(D, K) = |\mathbb{P}^{D-1}(\mathbb{F}_{K^2})|$. The GFD oscillator dynamics, the FPGA LUT-6 compile target, and the K=4 Heisenberg spin chain are three physical realizations of $\mathcal{A}_3$ — continuous-time, deterministic-classical, and quantum, respectively.**

---

# Part III: Rigorous Statements

## Theorem 1 — State law to Walsh basis

Let $G = (\mathbb{Z}/2)^n$. The complex-valued group algebra $\mathbb{C}[G]$ has a unique decomposition into 1-dimensional representations indexed by $\widehat G = \mathrm{Hom}(G, \mathbb{C}^*)$, which (for $G$ elementary abelian 2-group) is $\widehat G \cong G$. The corresponding basis change is the FWHT.

## Theorem 2 — Orientation cocycle gives Clifford

Let $\sigma : G \times G \to \{\pm 1\}$ be the cocycle $\sigma(a, b) = (-1)^{\sum_{i > j} a_i b_j}$. The twisted group algebra $\mathbb{R}[G]_\sigma$ with multiplication $e_a \cdot e_b = \sigma(a, b) e_{a+b}$ is isomorphic as an associative $\mathbb{R}$-algebra to $\mathrm{Cl}(n, 0)$.

*Sketch.* Verify the Clifford relations $e_i^2 = +1$ and $e_i e_j = -e_j e_i$ for $i \neq j$ from the cocycle. This is the standard construction (see Lounesto, *Clifford Algebras and Spinors*, 2nd ed., Cambridge 2001).

## Theorem 3 — Closure operator gives Eisenstein structure

Let $\Omega \in \mathrm{End}(\mathrm{Cl}(3, 0))$ be the algebra automorphism cyclically permuting $e_1 \to e_2 \to e_3$. Then $\Omega^3 = \mathrm{id}$, and the minimal polynomial of $\Omega$ on $\mathrm{Cl}(3, 0)$ factors as $X^3 - 1 = (X - 1)(X^2 + X + 1) = \Phi_1(X) \Phi_3(X)$. The $\Omega$-fixed subspace $V_1$ has dimension 2 (spanned by $1$ and $I$); the complement $V_3 \cong \mathbb{Z}[\omega]^3$ as a free $\mathbb{Z}[\omega]$-module of rank 3, carrying the action of $\omega$ via $\Omega$.

## Theorem 4 — The decomposition $\mathcal{A}_3 = \langle 1, I \rangle \oplus \mathbb{Z}[\omega]^3$

As a graded vector space (NOT subalgebra) decomposition under $\Omega$, with $\Omega$-fixed Gaussian axial (rank 2) and $\Omega$-cycled Eisenstein hexagonal (rank 3 over $\mathbb{Z}[\omega]$). Total real dimension $2 + 6 = 8 = \dim \mathrm{Cl}(3, 0)$.

## Theorem 5 — Coupling polynomial as norm trace

The polynomial $f(K, s) = 1 + sK + K^2$ at the discriminant-irreducible values $s \in \{-1, 0, +1\}$ equals the characteristic polynomial of $K$-scaling on the three structural channels of $\mathcal{A}_3$:
$$f(K, 0) = K^2 + 1 = N_{\mathbb{Z}[i]/\mathbb{Z}}(K - i) \quad \text{(axial)}$$
$$f(K, +1) = K^2 + K + 1 = N_{\mathbb{Z}[\omega]/\mathbb{Z}}(K - \omega) \quad \text{(hexagonal +)}$$
$$f(K, -1) = K^2 - K + 1 = N_{\mathbb{Z}[\omega]/\mathbb{Z}}(K + \omega) \quad \text{(hexagonal −)}$$
The product $f(K, +1) \cdot f(K, -1) = K^4 + K^2 + 1 = S(3, K)$ recovers the depth-3 closure algebra dimension.

## Theorem 6 — 3-sweep as projective plane

$$S(D, K) \;=\; \big|\mathbb{P}^{D-1}(\mathbb{F}_{K^2})\big| \;=\; \prod_{\substack{d \mid 2D \\ d > 2}} \Phi_d(K).$$
At $D = 3$, the divisor set is $\{3, 6\}$ uniquely producing the parity-conjugate cyclotomic pair $\Phi_3 \cdot \Phi_6$. The polynomial identity $\Phi_3(-K) = \Phi_3(K-1) = \Phi_6(K)$ holds because $\Phi_3$ has its symmetry axis exactly between consecutive integers — a property unique to $\Phi_3$ among cyclotomic polynomials.

## Theorem 7 — GFD oscillator as dynamical realization

The K=4 GFD oscillator's Jacobian at the dynamical fixed point is a Walsh-diagonal operator on $\mathcal{A}_3$ (8-dimensional state space) with $S_4 \times \mathbb{Z}_2$ symmetry. Its eigenvalue spectrum has degeneracy pattern $\{1, 3, 3, 1\}$ (= grade decomposition of $\mathrm{Cl}(3, 0)$) with ratio exactly $D = 3 = 1/\mathrm{Gram}$, invariant across all operating points and nesting depths. This is the closure algebra realized as continuous-time dynamics.

---

# Part IV: What the Pipeline Computes

## Worked example: a 3-bit Boolean function as closure algebra element

Take the Boolean function $f: \{-1,+1\}^3 \to \{-1,+1\}$ defined by the truth table $(+, +, -, +, -, +, +, -)$ on inputs ordered by $(x_1, x_2, x_3) = (---), (--+), (-+-), \ldots, (+++)$.

**Stage 1.** State law: this is a function on $G = (\mathbb{Z}/2)^3$, equivalently a $\pm 1$-valued vector in $\mathbb{R}^8$.

**Stage 1, Walsh expansion:** Compute the FWHT to get coefficients
$$\widehat f(S) \;=\; \frac{1}{8} \sum_x f(x) \chi_S(x).$$
Result: a coefficient vector $b \in \mathbb{R}^8$ indexed by $S \subseteq \{1, 2, 3\}$. (Specific values depend on the truth table — there are $2^8 = 256$ Boolean functions on 3 bits.)

**Stage 2.** Orientation: read the coefficient vector as a Clifford multivector,
$$F \;=\; \widehat f(\emptyset) + \widehat f(1) e_1 + \widehat f(2) e_2 + \widehat f(3) e_3 + \widehat f(12) e_{12} + \widehat f(13) e_{13} + \widehat f(23) e_{23} + \widehat f(123) e_{123}.$$

**Stage 3.** Closure: project onto the $\Omega$-eigenspace decomposition.
- Axial part: $a + b I = \widehat f(\emptyset) + \widehat f(123) I$.
- Hexagonal part: rewrite vectors and bivectors as
$$\sum_k \big(\widehat f(\{k\}) e_k + \widehat f(\{(k+1)(k+2)\}) e_{(k+1)(k+2)}\big).$$
Combine into Eisenstein form via $z_k = e_k + \omega e_{(k+1)(k+2)}$ (each $z_k$ a 1-dim $\mathbb{Z}[\omega]$-module).

**Stage 5.** Coupling polynomial trace: compute $f(K, s)$ at $K$ matching the operator's scaling characteristic.

**Stage 7.** Closure norm:
$$N_{\mathcal{A}}(F) \;=\; \widehat f(\emptyset)^2 + \widehat f(123)^2 + \sum_k N(z_k).$$
This integer characterizes the operator's complexity class.

**Stage 8.** Composition or sweep multiplication with another bridge; both produce a new closure-algebra element.

**Stage 9.** Compile to LUT: the bridge stack collapses to a 16-entry LUT (or 64-entry LUT-6 if the bridge is on 6 bits = $\mathcal{A}_3 \otimes \mathcal{A}_3$).

## Three views of the same operator

The Boolean function $f$, as a closure-algebra element, simultaneously is:
- A **Boolean gate** $T_b$ on 3 bits (via the spectral kernel).
- A **Clifford multivector** $F$ in $\mathrm{Cl}(3, 0)$.
- A **closure-algebra element** in $\mathcal{A}_3 = \langle 1, I \rangle \oplus \mathbb{Z}[\omega]^3$.
- A **point-labeling** of $\mathbb{P}^2(\mathbb{F}_{16})$ (via the projective-plane tower at $D = 3$).
- A **norm object** with $N_\mathcal{A}(F) \in \mathbb{Z}$.

These are not analogies. They are five projections of one algebraic object.

---

# Part V: Open Pipeline Extensions

1. **Higher-D closure algebras.** Define $\mathcal{A}_D$ for $D > 3$ — does the parity-shift collapse fail (as expected from Stage 5)? What replaces the Eisenstein-Gaussian dichotomy at $D = 4$? (Conjecture: at $D = 4$, the cyclotomic divisor set $\{4, 8\}$ gives $\Phi_4 \cdot \Phi_8$, a Gaussian-Fermat structure, not Eisenstein. Higher-D closure algebras are *not* simple analogs of $\mathcal{A}_3$ — they have different number-theoretic content.)

2. **Sweep multiplication algebra.** Develop the multiplication table of sweep $\star$ on the basis of $\mathcal{A}_3$. Determine whether $\star$ is associative (it generally won't be — averaging operations rarely are).

3. **Closure norm complexity classes.** Compute $N_\mathcal{A}$ for all 256 Boolean functions on 3 bits. Group by norm. Compare with circuit-complexity classes (NAND count, depth). Test the conjecture: low closure norm ↔ low complexity.

4. **Tensor product closure algebras.** $\mathcal{A}_3^{\otimes k}$ as a closure algebra at higher dimension. Each tensor copy contributes one Cl(3, 0) block. Decomposition into axial-tensor-axial, axial-tensor-hexagonal, hexagonal-tensor-hexagonal channels.

5. **Closure-algebra realization as quantum gates.** The K=4 Heisenberg system at $J = 1/3$ realizes the $S_4$-skeleton of $\mathcal{A}_3$. Identify which physical quantum systems realize the *full* closure algebra — including the closure operator $\Omega$ as an order-3 unitary.

6. **Generalized fine-structure constant.** $1/\alpha = 137 + 1/28$. With 137 prime and $\equiv 1 \pmod 6$, it splits in $\mathbb{Z}[\omega]$. Identify 137 in the closure-algebra hierarchy: at what depth $D$ and branching $K$ does 137 first appear as a prime factor of the closure norm of some natural operator?

---

# References

(See companion document for full bibliography. Primary closure-algebra references:)

- Lounesto, P. *Clifford Algebras and Spinors*. 2nd ed. Cambridge University Press, 2001. [Cl(n, 0) construction via cocycle-twisted group algebras.]
- Conway, J. H. and Smith, D. A. *On Quaternions and Octonions*. A K Peters, 2003. [Eisenstein integers, Hurwitz quaternions, octonion algebra.]
- Ireland, K. and Rosen, M. *A Classical Introduction to Modern Number Theory*. 2nd ed. Springer, 1990. [Cyclotomic fields, Eisenstein primes.]
- Hartshorne, R. *Algebraic Geometry*. Springer GTM 52, 1977. [Projective spaces over finite fields, Frobenius.]

---

*End of pipeline document. Three independent algebraic theorems define this pipeline: (a) the $\sigma$-twist Clifford correspondence (Lounesto, classical), (b) the $\Omega$-eigenspace Eisenstein decomposition (apparently new), and (c) the coupling-polynomial trace formula at parity-irreducible $s \in \{-1, 0, +1\}$ (apparently new). Together they unify Walsh computation, Clifford geometry, Eisenstein number theory, and GFD dynamics into one algebraic species — the closure algebra $\mathcal{A}_3$.*
