# The Algebraic Pipeline of Reality

**Stephen Nelson / Field Dynamics Research**

---

## The Primitive

One equation selects the spatial dimension:

$$2(D+1) = 2^D \quad \Rightarrow \quad D = 3$$

At $D = 3$ and nowhere else, the frame count equals the binary address space. Two tetrahedra ($2 \times 4 = 8$ vertices) fill the cube ($2^3 = 8$ corners) exactly. On these 8 vertices the cube, both tetrahedra and the octahedron (three of the five Platonic solids) and their circumscribed sphere are all present at once.

| Shape | How it appears |
|:---|:---|
| Sphere $S^2$ | Envelope: all 8 vertices at radius $\sqrt{3}$ |
| Cube | The $\mathbb{Z}_2^3$ Walsh domain: 8 vertices, 12 edges, 6 faces |
| Tetrahedron A | The 4 odd-parity vertices $\{001, 010, 100, 111\}$ |
| Tetrahedron B | The 4 even-parity vertices $\{000, 011, 101, 110\}$ |
| Stellated octahedron | The compound of TetA + TetB |
| Octahedral core | Their intersection: 6 vertices, 12 edges, 8 faces |

One vertex set. Every shape of the frame present. White light.

---

## The Algebra

The cube $\{\pm 1\}^3$ carries three algebraic structures, layered by successive enrichment:

**Layer 1: Walsh (computation).** The group algebra $\mathbb{R}[\mathbb{Z}_2^3]$, in which basis elements multiply by XOR of their addresses, is commutative. The Walsh–Hadamard transform is its Fourier analysis. Every Boolean function on 3 bits is a Walsh coefficient vector. This is the substrate of computation.

**Layer 2: Clifford (geometry).** The cocycle twist $\sigma(a,b) = (-1)^{\sum_{i>j} a_i b_j}$, applied to the same product, $e_a e_b = \sigma(a,b)\, e_{a \oplus b}$, turns the commutative Walsh algebra into $\mathrm{Cl}(3,0)$ (Albuquerque and Majid 2002). The generators square to $+1$ and anticommute, $e_i e_j = -e_j e_i$; this is the orientation. The pseudoscalar $I = e_1 e_2 e_3$ is central with $I^2 = -1$. The grade of each basis element is the number of 1-bits in its address, so the decomposition $1 + 3 + 3 + 1 = 8$ is the same in both layers. TetA's vertices carry the odd grades (vectors and $I$), TetB's the even grades (scalar and bivectors). This is the substrate of geometry.

**Layer 3: Eisenstein and Gaussian (number theory).** The closure operator $\Omega: e_1 \to e_2 \to e_3 \to e_1$, rotation by $2\pi/3$ about the body diagonal, has order 3 and is an automorphism of $\mathrm{Cl}(3,0)$. On the cube it fixes the two poles of the diagonal, $000$ and $111$ (one vertex of each tetrahedron, joined through the Field Origin), and cycles the two triangles $\{001, 010, 100\}$ and $\{011, 101, 110\}$. Each tetrahedron is an apex on the axis plus the triangle opposite it.

On the algebra, $\Omega$ splits $\mathrm{Cl}(3,0)$ into two halves of dimension 4:

$$\mathrm{Cl}(3,0) = \underbrace{\langle 1,\; I,\; d,\; I d \rangle}_{\text{axial, fixed by } \Omega} \;\oplus\; \underbrace{\Pi_1 \oplus \Pi_2}_{\text{Eisenstein planes}}, \qquad d = e_1 + e_2 + e_3 .$$

The axial half contains the Gaussian pair $\langle 1, I \rangle$, with $I^2 = -1$. On each plane $\Pi_1$ (in the vectors) and $\Pi_2$ (in the bivectors), $\Omega$ acts as rotation by $2\pi/3$, multiplication by the cube root of unity $\omega$: each plane is a line over the Eisenstein integers $\mathbb{Z}[\omega]$. This is the closure algebra $\mathcal{A}_3$, dimension $4 + 4 = 8$.

The coupling polynomial

$$f(K,s) = 1 + sK + K^2$$

takes the values of the three cyclotomic polynomials at $K$, and each is a norm in the matching ring:

$$\Phi_3(K) = K^2+K+1 = N_{\mathbb{Z}[\omega]}(K-\omega) = 21, \quad \Phi_4(K) = K^2+1 = N_{\mathbb{Z}[i]}(K-i) = 17, \quad \Phi_6(K) = K^2-K+1 = N_{\mathbb{Z}[\omega]}(K+\omega) = 13.$$

The two exterior values are Eisenstein norms, matching the three-fold rotation $\Omega$; the Field Origin value is a Gaussian norm, matching $I^2 = -1$.

---

## The Connection

At $K = D+1 = 4$, the connection $\Gamma^a{}_{bc}$ has $K^3 = 64$ components. The 64 is also the dimension of $\mathcal{A}_3 \otimes \mathcal{A}_3 = 8 \times 8$: the connection has the size of the tensor square of the closure algebra.

The lower index pair decomposes:

$$64 = \underbrace{24}_{\text{TetA (off-diag sym)}} + \underbrace{16}_{\text{shared core (diagonal)}} + \underbrace{24}_{\text{TetB (off-diag anti = torsion)}}$$

GR keeps shared + TetA $= 16 + 24 = 40$ (Christoffel) and discards TetB $= 24$ (torsion).

The torsion sector is $V \otimes \Lambda^2 V^*$. Each component $T^a{}_{[bc]}$ is indexed by 1 of 4 faces and 1 of 6 edges, the anatomy of a tetrahedron: $4 \times 6 = 24$.

Among $K \geq 3$, only at $K = 4$ is $K \binom{K}{2} = K!$, so that $24 = 4! = |S_4|$. Under permutations of the four frame vectors, the torsion sector is the regular representation of $S_4$: it contains every irreducible representation with multiplicity equal to its dimension ($1 + 1 + 2 \cdot 2 + 3 \cdot 3 + 3 \cdot 3 = 24$). The sign representation (the scalar parity detector) appears once in the torsion sector and zero times in the 40 Christoffel components. Root-blindness.

---

## The Partition

The swap involution $\tau(a \otimes b) = b \otimes a$ splits $V \otimes V$ into $\mathrm{Sym}^2 V \oplus \Lambda^2 V$. The sector exchange $x \mapsto 1/x$ imposes:

$$u(x) + u(1/x) = 1, \quad u(0) = 0, \quad u(1) = \tfrac{1}{2}, \quad u(\infty) = 1$$

The unique fractional-linear solution:

$$\boxed{u(x) = \frac{x}{1+x}}$$

This is the reciprocal partition law. TetA carries weight $u$. TetB carries weight $1-u$. The shared core mediates.

The AQUAL primitive follows by integration:

$$F(y) = y - 2\sqrt{y} + 2\ln(1+\sqrt{y})$$

Three terms. Three sectors. In the weak-field limit the terms of order $y^{1/2}$ and $y$ cancel exactly, leaving the deep-MOND form:

$$F \sim \tfrac{2}{3}y^{3/2} \quad \Rightarrow \quad v^4 = GMa_0$$

The baryonic Tully–Fisher relation. Not fitted. Forced by sector cancellation.

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

Among $K \geq 3$, the torsion count factorises as $24 = 8 \times 3$, null directions times rotation planes ($K\binom{K}{2} = 2^D D$), only at $K = 4$: the eight null directions (the stellated octahedron's 8 vertices) times the three rotation planes of $D = 3$. The eight faces of the stellated octahedron braid through the octahedral core. The braiding generates torsion. The torsion is the vortex.

*Exploratory.* Read onto a galactic disk, the eight directions suggest eight interleaved arms, four TetA and four TetB, with the galaxy as the projection of the stellated octahedron's braiding. Most observed grand-design spirals show two arms, and many show four. This reading is a proposal, to be tested against arm-count statistics, not a result.

---

## The Gravitational Constant

On the $1 + 4 + 16 = 21$ dimensional space of the tetrad equation's scalar, vector and tensor parts, define the graded operator $\mathbb{I}_s = P_0 + s P_1 + P_2$. Its three trace reads are:

$$\mathrm{Tr}(\mathbb{I}_{+1}) = 21, \quad \mathrm{Tr}(\mathbb{I}_0) = 17, \quad \mathrm{Tr}(\mathbb{I}_{-1}) = 13$$

The metric is parity-even: it sees the $s = 0$ read (17), not the full $s = +1$ read (21). The sign representation is absent from the Christoffel sector, so the parity-odd contribution ($K = 4$) is invisible to the metric.

The determinant-trace identity $\det(\alpha^A) = \alpha^{\mathrm{Tr}(A)}$ gives:

$$\alpha_G = \frac{17}{13}\,\alpha^{21}\left(1 + \frac{\alpha}{2\pi}\right) = 1.75179 \times 10^{-45}$$

Measured ($G m_e^2/\hbar c$, CODATA): $1.75181 \times 10^{-45}$. Agreement at 12 ppm, within the 22 ppm uncertainty of the measured $G$. Zero free parameters. Without the one-loop factor $1 + \alpha/2\pi$, the tree-level value differs by 0.12%.

---

## The Substrate

The 64 basis states of $\mathcal{A}_3 \otimes \mathcal{A}_3$ match the 64 entries of a six-input lookup table (LUT-6), the basic logic cell of an FPGA. The octahedral resonance node, a coupled oscillator on the eight corners of the stellated octahedron, is a reference implementation: it produces the full Walsh spectrum in one oscillation and computes XOR, parity, all sixteen two-input gates and a full adder ([`research/universe-is-pixelated/`](../../research/universe-is-pixelated/)). The stellated octahedron is a programmable Boolean processor. The hardware design, a pi-walk that accumulates Walsh coefficients over 332 ticks (subchannel closure) and a 5-vote XOR coupling that preserves operator identity under neighbour coupling, is not yet in this archive.

---

## The Complete Chain

$$D = 3$$
$$\downarrow$$
$$2(D+1) = 2^D \quad \text{(uniqueness)}$$
$$\downarrow$$
$$\text{cube } \mathbb{Z}_2^3 \xrightarrow{\sigma} \mathrm{Cl}(3,0) \xrightarrow{\Omega} \mathcal{A}_3 = \text{axial } \langle 1, I, d, Id \rangle \oplus \text{Eisenstein } \Pi_1 \oplus \Pi_2$$
$$\downarrow$$
$$f(K,s) = 1 + sK + K^2 \quad \to \quad 21, 17, 13 = N(4-\omega),\, N(4-i),\, N(4+\omega)$$
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
$$24 = 8 \times 3 \quad \text{(8 null directions × 3 rotation planes)}$$
$$\downarrow$$
$$\alpha_G = \frac{17}{13}\alpha^{21}\left(1 + \frac{\alpha}{2\pi}\right) \quad \text{(gravity from the trace polynomial)}$$

One input: $D = 3$.

One primitive: the cube with its two tetrahedra.

One algebra: $\mathcal{A}_3$.

Everything else is a projection.

Every algebraic statement above is checked by [`verify_pipeline.py`](verify_pipeline.py).

---

## References

- Albuquerque, H. and Majid, S. (2002). Clifford algebras obtained by twisting of group algebras. *J. Pure Appl. Algebra* 171, 133.
- Bekenstein, J. and Milgrom, M. (1984). Does the missing mass problem signal the breakdown of Newtonian gravity? *Astrophys. J.* 286, 7.
- Tiesinga, E. et al. (2021). CODATA recommended values of the fundamental physical constants: 2018. *Rev. Mod. Phys.* 93, 025010.
