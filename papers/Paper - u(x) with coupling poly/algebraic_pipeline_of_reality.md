# The Algebraic Pipeline of Reality

**Stephen Nelson / Field Dynamics Research**

---

## The Primitive

One equation selects the spatial dimension:

$$2(D+1) = 2^D \quad \Rightarrow \quad D = 3$$

At $D = 3$ and nowhere else, the frame count equals the binary address space. Two tetrahedra ($2 \times 4 = 8$ vertices) fill the cube ($2^3 = 8$ corners) exactly. The geometric primitive is complete: every fundamental shape is present simultaneously on 8 vertices.

| Shape | How it appears |
|:---|:---|
| Sphere $S^2$ | Envelope — all 8 vertices at radius $\sqrt{3}$ |
| Cube | The $\mathbb{Z}_2^3$ Walsh domain — 8 vertices, 12 edges, 6 faces |
| Tetrahedron A | Even-parity 4 vertices |
| Tetrahedron B | Odd-parity 4 vertices |
| Stellated octahedron | The compound of TetA + TetB |
| Octahedral core | Their intersection — 6 vertices, 12 edges, 8 faces |

One vertex set. Every platonic solid present. White light.

---

## The Algebra

The cube $\{±1\}^3$ carries three algebraic structures, layered by successive enrichment:

**Layer 1 — Walsh (computation).** The group algebra $\mathbb{R}[\mathbb{Z}_2^3]$ is commutative. The Walsh-Hadamard transform is its Fourier analysis. Every Boolean function on 3 bits is a Walsh coefficient vector. This is the substrate of computation.

**Layer 2 — Clifford (geometry).** The cocycle twist $\sigma(a,b) = (-1)^{\sum_{i>j} a_i b_j}$ turns the commutative Walsh algebra into $\text{Cl}(3,0)$. The anticommutation $e_i e_j = -e_j e_i$ is the orientation. Grade decomposition: $1 + 3 + 3 + 1 = 8$. This is the substrate of geometry.

**Layer 3 — Eisenstein (number theory).** The closure operator $\Omega: e_1 \to e_2 \to e_3 \to e_1$ (rotation by $2\pi/3$ around the body diagonal) has order 3. It splits $\text{Cl}(3,0)$ into:

$$\mathcal{A}_3 = \underbrace{\langle 1, I \rangle}_{\text{Gaussian axial}} \oplus \underbrace{\mathbb{Z}[\omega]^3}_{\text{Eisenstein hexagonal}}$$

The closure algebra. Dimension $2 + 6 = 8$. The coupling polynomial

$$f(K,s) = 1 + sK + K^2$$

is the norm form of $K$-scaling on the three cyclotomic channels:

$$\Phi_3(K) = K^2+K+1 = 21, \quad \Phi_4(K) = K^2+1 = 17, \quad \Phi_6(K) = K^2-K+1 = 13$$

---

## The Connection

At $K = D+1 = 4$, the connection $\Gamma^a{}_{bc}$ has $K^3 = 64$ components. The 64 is also $\mathcal{A}_3 \otimes \mathcal{A}_3 = 8 \times 8$. The connection IS the tensor square of the closure algebra.

The lower index pair decomposes:

$$64 = \underbrace{24}_{\text{TetA (off-diag sym)}} + \underbrace{16}_{\text{shared core (diagonal)}} + \underbrace{24}_{\text{TetB (off-diag anti = torsion)}}$$

GR lumps shared + TetA = $16 + 24 = 40$ (Christoffel). Discards TetB = $24$ (torsion).

The torsion sector is $V \otimes \Lambda^2 V^*$. Each component $T^a{}_{[bc]}$ is indexed by 1 of 4 faces and 1 of 6 edges. The anatomy of a tetrahedron: $4 \times 6 = 24$.

At $K=4$ and only $K=4$: $24 = 4! = |S_4|$. The torsion sector is the regular representation of the frame permutation group. It contains every irreducible $S_4$-representation at full multiplicity. The sign representation (the scalar parity detector) lives exclusively in the torsion. The Christoffel sector has zero copies. Root-blindness.

---

## The Partition

The swap involution $\tau(a \otimes b) = b \otimes a$ splits $V \otimes V$ into $\text{Sym}^2 V \oplus \Lambda^2 V$. The sector exchange $x \mapsto 1/x$ imposes:

$$u(x) + u(1/x) = 1, \quad u(0) = 0, \quad u(1) = \tfrac{1}{2}, \quad u(\infty) = 1$$

The unique fractional-linear solution:

$$\boxed{u(x) = \frac{x}{1+x}}$$

This is the reciprocal partition law. TetA carries weight $u$. TetB carries weight $1-u$. The shared core mediates.

The AQUAL primitive follows by integration:

$$F(y) = y - 2\sqrt{y} + 2\ln(1+\sqrt{y})$$

Three terms. Three sectors. Two exact cancellations produce the deep-MOND exponent:

$$F \sim \tfrac{2}{3}y^{3/2} \quad \Rightarrow \quad v^4 = GMa_0$$

The baryonic Tully-Fisher relation. Not fitted. Forced by sector cancellation.

---

## The Vortex

The occupation law has a derivative:

$$\frac{du}{d(\ln x)} = u(1-u)$$

The logistic equation. Not a model. A corollary. Every term is algebraic:

- $u$ = TetA fraction (symmetric sector)
- $1-u$ = TetB fraction (torsion sector)
- $u(1-u)$ = their product = octahedral core activity
- Maximum at $x = 1$ ($g = a_0$): core fully active, $u(1-u) = 1/4$

The field can only transition where the core is active. At $x \gg 1$: core dormant, partition frozen, pure GR. At $x \ll 1$: core dormant, partition frozen, pure torsion. At $x = 1$: peak vorticity.

The torsion factorises as $24 = 8 \times 3$ exclusively at $K = 4$. Eight null directions (the stellated octahedron's 8 vertices) times three rotation planes ($D = 3$ spatial). The eight faces of the stellated octahedron braid through the octahedral core. The braiding generates torsion. The torsion IS the vortex.

Eight spiral arms. Four TetA (blue). Four TetB (gold). Interleaved. The galaxy is the projection of the stellated octahedron's braiding onto the disk.

---

## The Gravitational Constant

The three trace reads:

$$\text{Tr}(\mathbb{I}_{+1}) = 21, \quad \text{Tr}(\mathbb{I}_0) = 17, \quad \text{Tr}(\mathbb{I}_{-1}) = 13$$

The metric is parity-even: it sees the $s = 0$ read (17), not the full $s = +1$ read (21). The sign representation is absent from the Christoffel sector, so the parity-odd contribution ($K = 4$) is invisible to the metric.

The determinant-trace identity $\det(\alpha^A) = \alpha^{\text{Tr}(A)}$ gives:

$$\alpha_G = \frac{17}{13}\,\alpha^{21}\left(1 + \frac{\alpha}{2\pi}\right) = 1.75179 \times 10^{-45}$$

Measured: $1.75181 \times 10^{-45}$. Agreement at 12 ppm. Zero free parameters.

---

## The Substrate

The closure algebra $\mathcal{A}_3$ realises as hardware. $\mathcal{A}_3 \otimes \mathcal{A}_3 = 64$ states fits a single LUT-6 on an FPGA. The pi-walk accumulates Walsh coefficients over 332 ticks (subchannel closure). The 5-vote XOR coupling preserves operator identity under neighbor coupling. The stellated octahedron is a programmable Boolean processor.

---

## The Complete Chain

$$D = 3$$
$$\downarrow$$
$$2(D+1) = 2^D \quad \text{(uniqueness)}$$
$$\downarrow$$
$$\text{cube } \mathbb{Z}_2^3 \xrightarrow{\sigma} \text{Cl}(3,0) \xrightarrow{\Omega} \mathcal{A}_3 = \langle 1,I \rangle \oplus \mathbb{Z}[\omega]^3$$
$$\downarrow$$
$$f(K,s) = 1 + sK + K^2 \quad \to \quad 21, 17, 13$$
$$\downarrow$$
$$64 = 24 + 16 + 24 \quad \text{(two tetrahedra + shared core)}$$
$$\downarrow$$
$$\text{torsion} \cong \mathbb{R}[S_4] \quad \text{(sign rep only in torsion)}$$
$$\downarrow$$
$$u(x) = \frac{x}{1+x} \quad \text{(reciprocal partition law)}$$
$$\downarrow$$
$$F(y) = y - 2\sqrt{y} + 2\ln(1+\sqrt{y}) \quad \to \quad v^4 = GMa_0$$
$$\downarrow$$
$$\frac{du}{d(\ln x)} = u(1-u) \quad \text{(vortex = logistic transition)}$$
$$\downarrow$$
$$24 = 8 \times 3 \quad \text{(8 arms × 3 planes = galaxy)}$$
$$\downarrow$$
$$\alpha_G = \frac{17}{13}\alpha^{21} \quad \text{(gravity from the trace polynomial)}$$

One input: $D = 3$.

One primitive: the cube with its two tetrahedra.

One algebra: $\mathcal{A}_3$.

Everything else is a projection.
