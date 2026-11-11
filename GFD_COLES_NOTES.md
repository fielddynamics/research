# Gravity Field Dynamics — Coles Notes

*A condensed, LLM-oriented digest of every paper, letter, proof and manuscript in this repository, with the algebra written out. Companion to [`llms.txt`](llms.txt), which holds the rules and glossary; this file holds the content.*

Stephen Nelson · Field Dynamics Research · fielddynamics.org · Last updated 2026-11-11

---

## 0. How to read this file

- **Status tags.** Every result is tagged **[T]** theorem (proved, with a verification script), **[D]** derived (follows from the framework's stated assumptions), **[E]** exploratory (a numerical correspondence or extension, not yet a derivation), or **[O]** observational comparison.
- **Paper keys.** I–XIII are the numbered Zenodo series (Jan–Mar 2026). L1, L2, L3 are the tetrad letters. CL is the constitutive-law letter, RAR the radial-acceleration-relation letter, DEC the decoding-mass letter, GRAM the Gram-matrix manuscript, TF the Tully–Fisher manuscript, ESS the GFD Essentials primer, A/B/C the algebraic papers, FY the closed-form energy-functional note, P-xxx the formal proofs in [`proofs/`](proofs/).
- **The series evolved.** Papers I–VI use the older "Distributed Field Processing (DFP)" vocabulary (Field Object, NET Field, Coupling Ports, Field Chamber) and lower-case $k$. Later work uses $K = 4$, $D = 3$ and the tetrad equation as the starting point. Where an early paper and a later letter derive the same result differently, the later letter is the curated statement.

### Naming that must not be confused

| Term | Means | Does not mean |
|---|---|---|
| SST (scalar-tensor transition) | The full four-term covariant action (§3) | The quadratic $g_s = g_t^2/(a_0+g_t)$ |
| Spherical field equation | $g_s = g_t^2/(a_0 + g_t)$, the spherical, static limit of the action | "The SST" |
| Capacity function | $f(x) = (21x+13)/(x+1)$ | The field equation |
| TetA | The exterior: observable spacetime, where a galaxy's stars and gas orbit | — |
| TetB | The throat interior, reached only through the Field Origin; occupied in a galaxy | The deep field; reverse time |
| Deep field | The regime $x \ll 1$ of the exterior, toward a galaxy's rim, where the TetB share $1-\mu \to 1$ | TetB |
| $s$ | Discrete state label of $f(K,s)$: $+1$ TetA, $0$ Field Origin, $-1$ TetB | $\sigma(x)$ |
| $\sigma(x)$ | Share difference $(x-1)/(x+1) = \mu - (1-\mu)$, continuous | A state; $\sigma = 0$ ($x = 1$) is not the Field Origin |
| One-directional law | $x(1-\mu) = \mu$: matter sources the field, the field does not source itself; governs a galaxy's exterior | An "unbound galaxy" (galaxies are never unbound) |
| Bound law | $x(1-\mu)^2 = \mu$: each partner is source and response (nuclei) | — |

---

## 1. The structure in one paragraph

The metric is a Gram matrix of the tetrad, $g_{\mu\nu} = \eta_{ab} e^a{}_\mu e^b{}_\nu$. The equation is even in the spatial frame, so it has two parity-related roots. Drawn in space, one root is a regular tetrahedron (TetA) and the other its inversion (TetB); together they are the stellated octahedron inscribed in the cube, sharing a centre, the Field Origin. Counting on this object gives one polynomial, $f(K,s) = 1 + sK + K^2$, with values 21, 17, 13 at $K = 4$. The exchange symmetry between the two roots forces the interpolating function $\mu(x) = x/(x+1)$. Integrating it gives the AQUAL kinetic function $F(y)$, and with it a covariant action whose prefactors are $K^2$, $2^D$, $K$. In the spherical, static limit the action gives the relation tested on SPARC. General relativity is the $\mu = 1$ (all-TetA) case: its torsion-free condition keeps 40 of 64 connection components and discards the 24 that carry TetB.

---

## 2. Foundations: dimension, frame, polynomial

### 2.1 Dimension selection [T] (IX, P-hadamard)

$$2(d+1) = 2^d \;\Longrightarrow\; d = 3 \quad(\text{only positive integer root}),\qquad K = d+1 = 4,\quad D = 3.$$

Reading: a simplex in $d$ dimensions has $d+1$ vertices; a simplex and its parity image ($2(d+1)$ points) fill the $2^d$ corners of the cube only when $d = 3$. Check: $d=3$ gives $8 = 8$; $d = 2$ gives $6 \ne 4$; $d = 4$ gives $10 \ne 16$.

Early papers (III–V) reach $k = 4$ instead from the simplex theorem (a $d$-dimensional enclosure needs $d+1$ faces) and its recurrence in ADM (1 Hamiltonian + 3 momentum constraints), the tetrad (1 + 3 legs), LQG and Regge calculus (the tetrahedron), and LIGO's polarisations ($10 - 2k = 2$).

### 2.2 The tetrad's coordinate-space geometry [T] (L1, P-two-regions)

The four isotropic spatial directions of an orthonormal frame give four projections

$$v_1 = x+y+z,\quad v_2 = x-y-z,\quad v_3 = -x+y-z,\quad v_4 = -x-y+z,\qquad \textstyle\sum_i v_i = 0.$$

Of the $2^4 = 16$ sign combinations of the half-spaces $\pm v_i \le 1$, exactly two are bounded:

$$\text{TetA}: \max_i v_i \le 1, \qquad \text{TetB}: \max_i(-v_i) \le 1.$$

They interpenetrate as a stellated octahedron; the boundary splits into $4$ faces $\times$ $4$ sub-regions $= 16$ channels. No second frame is assumed: TetB is the second bounded region of a single tetrad.

**Scheme version (P-two-regions, 39 checks).** $g = e^T\eta e$ forces $(\det e)^2 = \det g/\det\eta$, so the solution scheme has exactly two components, one per root of $\det e$. Spatial parity maps one to the other (three is odd) and carries TetA onto TetB. The metric sees only $(\det e)^2$; restricting to $SO^+(1,3)$ keeps one root and discards the other.

### 2.3 The forced frame [T] (P-forced, GRAM, 27 + 32 checks)

Legs with the pattern of $\eta$ (every pair alike, equal magnitudes, distinct) are forced to a regular tetrahedron, unique up to $O(3)$, and only in three dimensions. Explicitly,

$$M_1 = \begin{pmatrix} +1&+1&-1&-1\\ +1&-1&+1&-1\\ +1&-1&-1&+1\end{pmatrix},\quad M_2 = -M_1,\quad G_{M_1M_1} = M_1^TM_1 = \begin{pmatrix}3&-1&-1&-1\\-1&3&-1&-1\\-1&-1&3&-1\\-1&-1&-1&3\end{pmatrix}.$$

Gram products: $G_{M_2M_2} = G_{M_1M_1}$ (root-blind self-coupling), $G_{M_1M_2} = -G_{M_1M_1}$ (sign-reversing cross-coupling); $G_{IJ} = D$ on the diagonal, $-1$ off it. Columns of $M_1$ are a tetrahedron, of $M_2$ its inverse, of $[M_1\ M_2]$ the stellated octahedron.

### 2.4 Hadamard kernel [T] (C, P-hadamard, 25 checks)

A regular simplex on cube corners $\{\pm1\}^D$, bordered by a row of ones, is a Hadamard matrix. The Walsh–Hadamard matrix of the 3-cube factorises $H_8 = H_2 \otimes H_4$ (parity $\otimes$ frame). The three non-constant rows of $H_4$ are the stellated octahedron's axes and the tetrad's face normals. Parity classes: TetA $\{(+++),(+--),(-+-),(--+)\}$, TetB $\{(---),(-++),(+-+),(++-)\}$.

### 2.5 The coupling polynomial [D] (VII, VIII, IX, A)

$$f(K,s) = 1 + sK + K^2,\qquad f(4,+1) = 21\ (\text{TetA}),\quad f(4,0) = 17\ (\text{Field Origin}),\quad f(4,-1) = 13\ (\text{TetB}).$$

Three levels: existence (1), the $K$ faces, the $K^2$ face-pair channels. Identities used throughout:

- $f(K,+1) = (K^3-1)/(K-1) = \Phi_3(K)$; $f(K,-1) = \Phi_6(K)$ (cyclotomic polynomials).
- $(f(+1) + f(-1))/2 = 17 = f(0)$; $f(+1) - f(-1) = 2K = 8$.
- $17/13 = (K^2+1)/(KD+1) = [1; 3, 4]$ as a continued fraction; $13 = 12$ edges $+ 1$ origin $= KD + 1$.

**As a trace [T] (A; research/aqual §13).** With $V = \mathbb R^4$ and $\tau$ the swap on $V\otimes V$ ($\operatorname{Tr}1 = 16$, $\operatorname{Tr}\tau = 4$),

$$f(K,s) = 1 + \operatorname{Tr}_{V\otimes V}(1 + s\tau),$$

the parity-weighted trace of the sector space $\Lambda^K V \oplus V \oplus (V\otimes V)$. The swap's eigenspaces are the symmetric 10 and antisymmetric 6, the same split GR meets in the tetrad (10 metric + 6 local Lorentz) and in each connection slice (10 Christoffel + 6 torsion). GR keeps the symmetric sector both times, which is why 13, 17, 21 never appear there: the parameter $s$ that weights the two sectors is fixed at one end.

---

## 3. The covariant action (the SST)

$$\boxed{S = \int d^4x\,\sqrt{-g}\left[\frac{R}{16\pi G} - \frac{a_0^2}{8\pi G}\,F(y) - \frac14 e^{-2\Phi/c^2}F_{\mu\nu}F^{\mu\nu} + \mathcal L_{\rm matter}\right],\qquad y = \frac{|\nabla\Phi|^2}{a_0^2}}$$

- **Prefactors [D]** (L3 supplement): $16 = K^2$, $8 = 2^D$, $4 = K$, a geometric sequence of ratio 2.
- **Electromagnetic term:** conformal coupling $e^{-2\Phi/c^2}$; $\gamma = 1$ follows from the connection structure, giving full light bending $\theta = (1+\gamma)\,2GM/(rc^2) = 4GM/(rc^2)$ (Paper I resolved the "half-lensing" problem of scalar theories this way).
- **Weak field:** $g_{00} = -(1+2\Phi/c^2)$, $g_{ij} = (1-2\Phi/c^2)\delta_{ij}$; GW speed equals $c$.
- **Split:** $\nabla^2\Phi_N = 4\pi G\rho$ (the 40-component Newtonian part) plus the scalar supplement $\nabla\cdot[(\mu - 1)\nabla\Phi] = 0$.
- **Open:** $\mathcal L_{\rm matter}$ is not specified in the papers. The source term $-\rho\Phi$ is what makes the scalar equation sourced (research/aqual docs note, check D1–D2).

### 3.1 The kinetic functional [T] (FY, P-aqual, 24 checks)

AQUAL requires $dF/dy = \mu(\sqrt y)$. For $\mu(x) = x/(x+1)$, with $u = \sqrt y$:

$$F(y) = \int_0^y \frac{\sqrt t}{\sqrt t+1}dt = 2\int_0^{\sqrt y}\frac{u^2}{u+1}du,\qquad \frac{u^2}{u+1} = (u-1) + \frac{1}{u+1},$$

$$\boxed{F(y) = y - 2\sqrt y + 2\ln(1+\sqrt y)},\qquad F'(y) = 1 - \frac1{\sqrt y} + \frac{1}{\sqrt y(1+\sqrt y)} = \frac{\sqrt y}{1+\sqrt y}.$$

- $F'' = 1/[2\sqrt y(1+\sqrt y)^2]$; $F(0) = 0$, $F \ge 0$.
- Newtonian limit $F \to y$; deep field $F \simeq \tfrac23 y^{3/2}$, which arises from the cancellation of all three terms (not from the log term alone).
- As a function of $\nabla\Phi$ the energy is $C^2$ and strictly convex, so the field equation is elliptic away from $\nabla\Phi = 0$ and solutions are unique for given boundary data.
- Paper I wrote the same object as $L(x) = \tfrac12x^2 - x + \ln(1+x)$ $(= F/2$ at $y = x^2)$.

### 3.2 Field equation and its spherical limit [D] (RAR, DEC, L3 suppl.)

Varying $\Phi$:

$$\nabla\cdot\left[\mu\!\left(\frac{|\nabla\Phi|}{a_0}\right)\nabla\Phi\right] = 4\pi G\rho.$$

Spherical symmetry plus Gauss's theorem: $\mu(g_t/a_0)\,g_t = g_s$ with $g_s = GM_{\rm bar}(r)/r^2$. Substituting $\mu = x/(x+1)$, $x = g_t/a_0$:

$$\boxed{g_s = \frac{g_t^2}{a_0 + g_t}}\ (\text{spherical field equation}),\qquad g_t = \frac{g_s + \sqrt{g_s^2 + 4g_sa_0}}{2}\ (\text{forward solver}).$$

- **BTFR:** for $g_t \ll a_0$, $g_t^2 = g_s a_0$, so $v^4 = GM_b a_0$ and $M_b = v_{\rm flat}^4/(Ga_0)$.
- **Mass decoder (DEC):** with $g_t = v^2/r$, $\;M_{\rm dec}(r) = \dfrac{r v^4}{G(a_0 r + v^2)} = \dfrac{r^2}{G}\,(g_t - a_0\mu)$, the total field minus its TetB share.
- **Interior activity (DEC):** $\Delta M_{\rm eff} = M_{\rm phot} - M_{\rm dec}$ is zero when the interior is quiet, positive or negative when the drain drives or brakes the flow. It is not the TetB share.
- **Stability [T]** (research/aqual): the kinetic coefficient is $2\mu > 0$ (no ghost); waves cross a static field at $c$ and travel along it at $c\sqrt{2-\mu}$; the Hessian eigenvalues are $\mu$ (twice) and $(x\mu)'$, and their ratio $(x\mu)'/\mu = 1 + (1-\mu)$ — the anisotropy is exactly the TetB share. $F$ is undefined for timelike gradients.

---

## 4. The constitutive law $\mu(x) = x/(x+1)$

Here $x = g/a_0$ and $\mu$ is the TetA share of the field; $1 - \mu = 1/(x+1)$ is the TetB share.

### 4.1 Exchange symmetry route [T] (CL route 3, P-exchange, 34 checks)

Exchanging TetA and TetB inverts $x$ about $a_0$ and swaps the shares:

$$\mu(1/x) = 1 - \mu(x).$$

On the odds ratio $\Omega = \mu/(1-\mu)$ this reads $\Omega(1/x) = 1/\Omega(x)$. With the endpoint $\mu(0) = 0$ and coupling of degree one in each variable, $\Omega(x) = x$, so

$$\frac{\mu}{1-\mu} = x \;\Longrightarrow\; \boxed{\mu(x) = \frac{x}{x+1}}.$$

Every premise is shown necessary. The capacity ratio between the two sectors equals the dimensionless acceleration.

### 4.2 Equilibrium (detailed balance) route [D] (I, CL route 2)

Single channel with fill $\varepsilon$: activation $W_+ = \kappa_+x(1-\varepsilon)$, relaxation $W_- = \kappa_-\varepsilon$. At equilibrium $Kx(1-\varepsilon) = \varepsilon$, so $\varepsilon = Kx/(1+Kx)$; absorbing $K$ into $a_0$ gives $\mu = x/(1+x)$. The fixed point is unique and globally attracting ($d\dot\varepsilon/d\varepsilon = -\kappa(x+1) < 0$). Paper I's postulates: lossless (no wakes, drag, hysteresis), locally evaluable, single channel; within this "MSC" class, the deep-MOND limit forces exponent $n = 1$.

### 4.3 Normalised capacity route [D] (VIII, IX)

$$f(4,\sigma(x)) = 17 + 4\sigma(x) = \frac{21x+13}{x+1},\qquad \mu(x) = \frac{f - 13}{21 - 13} = \frac18\cdot\frac{8x}{x+1} = \frac{x}{x+1}.$$

### 4.4 Algebraic route [T] (A)

The swap $\operatorname{Sym}^2V \leftrightarrow \Lambda^2V$ is represented by $x \mapsto x^{-1}$; within fractional-linear maps with the pure-sector endpoints, the unique solution is $x/(1+x)$, and the Cayley coordinate $(x-1)/(x+1)$ is $\sigma(x)$.

### 4.5 Properties

- Logistic: $x\,d\mu/dx = \mu(1-\mu)$; rate peaks at $1/4$ at $x = 1$.
- $\sigma(x) = \tanh(\tfrac12\ln x)$, and $\sigma(x_1x_2) = (\sigma_1+\sigma_2)/(1+\sigma_1\sigma_2)$ — shares compose like rapidities; odds multiply.
- Mean capacity: $\mu(x)+\mu(1/x) = 1 \Rightarrow \langle f\rangle = 17$ over any window symmetric in $\ln x$.
- Swap-operator form: $1 + \sigma\tau = 2[\mu P_{\rm sym} + (1-\mu)P_{\rm anti}]$, with $x = \lambda_{\rm sym}/\lambda_{\rm anti}$ and $1+\sigma\tau = \operatorname{sech}\theta\,e^{\theta\tau}$, $\theta = \tfrac12\ln x$. GR sits at $\mu = 1$.
- Dark-matter dictionary (L2): if $g_{\rm obs} = g_{\rm bar} + g_{\rm DM}$, then $g_{\rm DM}/g_{\rm bar} = (1-\mu)/\mu = 1/x$, so $M_{\rm DM}/M_{\rm bar} = 1/x$. "Dark matter" is the TetB share read through Newtonian analysis (Paper I: phantom density $\rho_{\rm ph}\propto r^{-2}$).

### 4.6 The law family and the bound law [D] (IX, XIII; research/aqual)

$x(1-\mu)^N = \mu$: $N = 1$ one-directional (galaxy exterior); $N = 2$ bound law (nuclei),

$$\mu_b(x) = \frac{(2x+1) - \sqrt{4x+1}}{2x},\qquad \mu_b(1) = \frac{3-\sqrt5}{2} = \frac1{\varphi^2},\qquad \mu_b(2) = \tfrac12.$$

- **The bound law is the exchange image of the source form.** In the source variable $z = x\mu$ the one-directional law is $z(1-\mu) = \mu^2$; applying $(z,\mu)\to(1/z, 1-\mu)$ gives $z(1-\mu)^2 = \mu$.
- Strong-field tail $1-\mu_b \simeq 1/\sqrt x$, so at $x = A^2$ the TetB share is $1/A$ (vs $1/(1+A^2)$ one-directionally).
- Bound logistic rate $x\mu' = \mu(1-\mu)/(1+\mu)$, peak $(\sqrt2-1)^2 \approx 0.172$ at $x = (1+\sqrt2)/2$.
- Hyperbolic form: with $\sinh\psi = 2\sqrt x$, $\mu_b = \tanh^2(\psi/2)$.
- Two operations generate the family $x^n(1-\mu)^m = \mu^k$: S (source variable) $(n,m,k)\to(n,m,k+n)$ and E (exchange) $(n,m,k)\to(n,k,m)$; $U = (1,1,1) \xrightarrow{S} (1,1,2) \xrightarrow{E} (1,2,1) = $ bound.

### 4.7 Point mass in one variable [T] (research/aqual §9)

With $r_M = \sqrt{GM/a_0}$ and $\sinh\psi = 2r/r_M$:

$$\frac{g_t}{a_0} = \operatorname{csch}^2\frac\psi2,\quad \mu = \operatorname{sech}^2\frac\psi2,\quad v^2 = \sqrt{GMa_0}\coth\frac\psi2,\quad \Phi + v^2 = \sqrt{GMa_0}\,\psi.$$

Unit source field ($g_s = a_0$) at $r = r_M$ where $\mu = 1/\varphi$; unit total field ($x = 1$) at $r = \sqrt2\,r_M$ where $\psi/2 = \ln(1+\sqrt2)$.

---

## 5. The connection: 64 = 40 + 24

### 5.1 Counting [T] (L2, L3, GRAM, 40/24 proof)

Per slice $\lambda$, $\Gamma^\lambda{}_{\mu\nu}$ has $K^2 = 16$ entries: $(K^2+K)/2 = 10$ symmetric, $(K^2-K)/2 = 6$ antisymmetric. Over $K$ slices:

$$\text{Christoffel } K\frac{K(K+1)}2 = 40,\qquad \text{torsion } K\frac{K(K-1)}2 = 24.$$

In polynomial form, per slice:

$$\text{kept} = \frac{f(K,+1)-1}{2} = 10,\qquad \text{discarded} = \frac{f(K,-1)-1}{2} = 6,$$

with difference $K$ and sum $K^2$. GRAM writes the index grid per slice as $6$ upper $+ 4$ diagonal $+ 6$ lower, so $24 + 16 + 24 = 64$, the torsion-free projection retaining $16 + 24 = 40$. The split is defined on the index grid, not on cube-corner pairs.

### 5.2 The torsion lemma [T] (L2)

A torsion-free connection cannot distinguish TetA from TetB; the torsion sector is the necessary carrier of the two-chamber distinction. $K/2 = 2 \Rightarrow K = 4$ selects the dimension at which this works.

### 5.3 Torsion is the regular representation of $S_4$ [T] (B, P-torsion, 36 checks)

At $K = 4$, $V\otimes\Lambda^2V^*$ (dimension $K^2(K-1)/2 = 24 = 4!$) carries the regular representation of $S_4$ acting on the four legs. The sign representation, the unique scalar parity detector, appears once in torsion and zero times in the Christoffel sector. Only $K = 2$ and $K = 4$ allow this.

### 5.4 Einstein's equation as the TetA partition [D] (L3)

The torsion-free condition keeps the $s = +1$ projection and discards the $s = -1$ projection. GR is the GFD field equation at $\mu = 1$. Restoring the 24 components gives the full 64-component connection, which $\mu(x)$ partitions spatially; the gap opened by releasing $\mu$ is the TetB share, conventionally attributed to dark matter. In a galaxy, the TetA share dominates the core and the TetB share the rim (the deep field), with the handover on the ring $x = 1$. TetB itself is the throat interior at the centre.

---

## 6. Galactic results

### 6.1 Radial acceleration relation [O] (RAR)

$$g_{\rm obs} = \tfrac12\left[g_{\rm bar} + \sqrt{g_{\rm bar}^2 + 4a_0g_{\rm bar}}\right],\qquad v_{\rm bar}^2 = v_{\rm gas}|v_{\rm gas}| + \Upsilon_d v_d^2 + \Upsilon_b v_b^2.$$

SPARC, $Q \le 2$: 164 galaxies, 3284 points, $\Upsilon_d = 0.5$, $\Upsilon_b = 0.7$, $a_0 = 1.2\times10^{-10}$ m/s². GFD: mean $-0.027$ dex, $\sigma = 0.181$ dex. McGaugh, Lelli & Schombert (2016) one-parameter fit: mean $-0.022$, $\sigma = 0.182$. $\Delta\sigma = 0.0003$ dex. **Caveat:** this is MOND's simple $\mu$; the RAR alone cannot distinguish GFD from that variant. Script: `papers/letter-radial-acceleration-relation-sparc/sparc_rar.py`.

### 6.2 Decoding mass [O] (DEC)

Observed $v(r)$ → $M_{\rm dec}(r)$ with only $G$ and $a_0$. Milky Way and M33 effective-mass profiles agree with independently inferred baryonic mass to within a factor of order unity, no halo. Analogy: a fluid vortex, whose surface tracers follow the flow but do not set the drain's power.

### 6.3 Milky Way rotation [O] (VII)

225 km/s predicted vs 229 km/s observed (1.6%), zero free parameters.

### 6.4 Tully–Fisher evolution [D/O] (II, X, TF)

$$a_0 = \frac{cH}{2\pi}\sqrt{\frac K\pi},\qquad v_{\rm flat}^4 = GMa_0 \;\Rightarrow\; \frac{v(z)}{v(0)} = \left[\frac{a_0(z)}{a_0(0)}\right]^{1/4}.$$

With Paper II's cosmological scaling $a_0 \propto H^{1-1/\pi}$, the exponent is $(1 - 1/\pi)/4 = 0.170$:

$$\frac{v(z)}{v(0)} = \left[\frac{H(z)}{H_0}\right]^{0.17},\qquad H(z) = H_0\sqrt{\Omega_m(1+z)^3 + \Omega_\Lambda}.$$

Predicts +21% at $z = 2$, $>1.3$ at $z > 3$ (ΛCDM: 1.0). Nine IFU measurements, $0 < z < 3$ (ratios 1.21 at $z = 2$, 1.29 at $z = 3$), fall within the band. Tests: JWST, ELT, Euclid at $z > 3$.

---

## 7. Cosmology and the acceleration scale

### 7.1 Horizon relation [D] (II)

$a_0 = cH_0/(2\pi)$ from horizon thermodynamics. At cosmic scales, closures tile with hexagonal contact geometry; averaging over the boundary ($\langle\theta\rangle$ of $\theta(d) = 2\cos^{-1}(d/2R)$) gives the factor $1/\pi$ and $a_0 \propto H^{1 - 1/\pi}$.

### 7.2 CMB enhancement [D/O] (II)

At recombination ($z = 1100$), $a_0$ was about 24,000 times larger, the field sits deep in the low-$x$ regime, and the enhancement is $1/\mu(x_{\rm rec}) = (1+x_{\rm rec})/x_{\rm rec} = 6.46$ against the ≈ 6.4 that Planck's peaks require (1%). Only this single factor is computed, not the full power spectrum. Paper II also lists consequences for the Planck lensing anomaly, JWST early galaxies and DESI's evolving dark energy.

### 7.3 The unit of gravity [E] (III, IV, V)

Two routes to the same length:

$$r_e = \frac{e^2}{4\pi\varepsilon_0 m_ec^2} = 2.818\ \text{fm (no gravity)},\qquad r_e = k\sqrt{\frac{Gm_e}{a_0}} = 2.82\ \text{fm (no EM)},$$

agreement 0.21%, unique to the electron (muon and proton fail by ~$10^3$). Equivalently $a_0 = 16\,Gm_e/r_e^2$, with $16 = k^2$ the isotropic tetrad channels ($4\times4$ components; measured ratio $a_0/(Gm_e/r_e^2) = 15.93$, 0.41%).

### 7.4 Hubble constant [E] (III, IV, companion, X, TF)

- MOND in flat space: $a_0 = cH/2\pi$ with the topological $a_0$ gives $H_{\rm flat} = 78.90$ km/s/Mpc.
- Projected through the tetrad: $H = H_{\rm flat}/\sqrt{k/\pi} = 69.92$ km/s/Mpc (GW170817: $70.0\pm12$).
- Port ratio $\sqrt{k/\pi} = 1.128$ converts the spherical envelope ($\pi$) to the tetrahedral chamber ($k$).
- Band: $(k/\pi)^{1/4} - 1 = \pm6.2\%$ → 65.9–74.6 km/s/Mpc, containing Planck, SH0ES and the other major methods.
- Bidirectional: observed $H$ recovers $m_e$ to 0.10% (IV) / 0.01% (companion).
- Paper X quotes $H_0 = 2\pi a_0/(c\sqrt{K/\pi}) = 70.21$; TF quotes 70.29; Paper VII 70.21. **Open:** three values from different routes; the two $a_0$–$H$ relations ($cH/2\pi$ vs $(cH/2\pi)\sqrt{4/\pi}$) differ by 1.128.

---

## 8. Constants from the integers [E] (VI, VII)

### 8.1 Newton's constant

$$G = \frac{17}{13}\,\alpha^{21}\,\frac{\hbar c}{m_e^2} = \frac{(d+1)^2+1}{d(d+1)+1}\,\alpha^{1+(d+1)+(d+1)^2}\,\frac{\hbar c}{m_e^2}$$

$= 1.3077 \times 1.338\times10^{-45}\times3.810\times10^{34} = 6.666\times10^{-11}$ m³ kg⁻¹ s⁻² (0.12% tree level; 0.001% with a one-loop Schwinger correction, research/g_from_topology). Exponent 21 = coupling depth; $\alpha^{20}\approx10^{-43}$ is the gravity/EM hierarchy. A 0.001% change in $\alpha$ shifts $G$ by 0.021%.

### 8.2 Fine-structure constant

$$\frac1\alpha = 2^d(k^2+1) + 1 + \frac{1}{k(k+d)} = 8\times17 + 1 + \frac1{28} = 137.0357\ (0.0002\%),$$

with $28 = V + E + F$ of the compound $= k(k+d)$, and $\alpha = r_e/\bar\lambda_C$.

### 8.3 Other structural readings (VI, VII)

- **Four roads to two tetrahedra (VI):** spinors need the SL(2,C) double cover; gravity's chiral split $A = A^+\oplus A^-$ (Ashtekar); ghost-free bimetric gravity needs two metrics (Hassan–Rosen); single-tetrahedron gravity is unstable (Alexander et al.). The stellated octahedron is the unique two-tetrahedra compound (Coxeter).
- **Spin:** 2 inward (TIME) faces of 8: $S = (2/8)\times2\hbar = \hbar/2$.
- **Neutron lifetime (VII):** beam–bottle discrepancy predicted 1.084% vs 1.081% observed.
- Paper VII also reads $E = mc^2$, the inverse-square law, $\lambda = h/p$ and $E^2 = (pc)^2 + (m_0c^2)^2$ from the structure. Treat these as interpretive.

---

## 9. Bimetric gravity [D] (VIII, XII)

Hassan–Rosen: $S = M_g^2\!\int\!\sqrt{-g}R_g + M_f^2\!\int\!\sqrt{-f}R_f + m^2M_g^2\!\int\!\sqrt{-g}\sum_{n=0}^4\beta_ne_n(S)$, $S = \sqrt{g^{-1}f}$ (vielbein form $S^a{}_b = (e^{-1}\tilde e)^a{}_b$), five free $\beta_n$.

GFD locks them:

$$\{\beta_0,\beta_1,\beta_2,\beta_3,\beta_4\} = \{1, 0, 16, 0, 1\},\qquad V(S) = e_0 + 16\,e_2 + e_4.$$

- $\beta_2 = 16 = \dim C\ell_{1,3} = \dim\operatorname{End}(\mathbb R^{1,3}) = K^2$.
- Odd terms vanish by metric exchange symmetry, $e_n(S^{-1}) = e_{4-n}(S)$, palindromic.
- Ghost freedom: the 4-form interaction is linear in the lapse ($dt\wedge dt = 0$, $\partial^2\mathcal L/\partial N^2 = 0$), so the potential lies in the ghost-free class by construction.
- The helicity-0 mode (Stückelberg $\varphi^\mu = x^\mu - \partial^\mu\pi/\Lambda_3^3$) gives Galileon terms whose static limit is AQUAL-like, $\mathcal P(\pi'/r) = GM/r^3$, matching $\mu(\sqrt y) = F'$.
- XII adds three theorems + three axioms, a term-by-term map of the two actions, and six concordance checks (expansion history, BBN, CMB enhancement, Vainshtein screening, Galileon hierarchy, mixing angle $\tan\theta = D/(V+E+F) = 3/28$, $\theta = 6.12°$; $\Delta\mu = 2/17 = 11.76\%$).

---

## 10. Nuclei [E] (XI, XIII)

### 10.1 Paper XI: packing and a one-line binding formula

$$\frac{\text{BE}}{A} = C\,[\,f(K, s_2(A^2)) - 17\,],\qquad f(K, s_2(A^2)) = 13 + 8\,\mu_2(A^2),\qquad C = \frac{m_ec^2\cdot17}{K} = 2.172\ \text{MeV},$$

where $\mu_2$ is the bound law. Ceiling $C(21 - 17) = m_ec^2\cdot17 = 8.687$ MeV. 82 isotopes He–Bi: $R^2 = 0.99$, mean error 3.9%, 98% within 10%.

**Magic numbers.** Tetrahedral numbers minus a Sierpiński gate:

$$T(n) = \frac{n(n+1)(n+2)}6,\quad G(n) = \begin{cases}0 & n < K\\ (n-1)n/2 & n\ge K\end{cases},\quad M(n) = 2[T(n) - G(n)] \Rightarrow \{2, 8, 20, 28, 50, 82, 126\}.$$

$K = 4$ is the unique integer in $2\le K\le10$ that gives all seven. Ceiling $M(n) \le K^K = 256$: no shell beyond the eighth, consistent with Bi-209 as the heaviest stable isotope.

### 10.2 Paper XIII: the bound law along a 64-step walk

Each nucleon $i$ contributes $\mu_b(i^2)$; with $\Sigma_A = \sum_{i\le A}\mu_b(i^2)$ and zinc ($A = K^D = 64$) as the anchor,

$$\frac BA(A) = \frac BA(\text{Zn})\,\frac{K^D}{A}\,\frac{\Sigma_A}{\Sigma_{K^D}}.$$

Shell ceilings $\mathrm{CEIL} = B_{\rm Zn} + B_{\rm bdy} - \mu_b(2)[B_{\rm Zn} - B_{\rm bdy}]$ with $\mu_b(2) = 1/2$; inverted curves $B_n^{\rm inv}(A) = \mathrm{CEIL}_n - B_{\rm local}(A - A_n)$; $B/A = \min(B_1, B_1^{\rm inv}, B_2^{\rm inv}, B_3^{\rm inv})$. Results: the seven magic numbers including the $20\to28$ gap without spin–orbit coupling, and $B/A$ from He to Pb at MAE ≈ 95 keV.

---

## 11. Other threads (shorter)

- **Paper V:** why four recurs across ADM, tetrads, LQG, Regge, LIGO — the simplex theorem; vocabulary bridge to the Field Chamber and its four Coupling Ports.
- **Paper IX:** the derivation chain $d = 3 \to$ stellated octahedron $\to (3+1) \to$ tetrad $\to \{\beta_n\} \to \Phi_3/\Phi_6 \to \mu \to S$; the $(3+1)$ split from face classification (2 TIME + 6 spatial faces). Also an isomorphism between the base-8 expansion of π and the topology **[E]**.
- **ESS:** primer for relativists: tetrads and non-degeneracy ($\det g = -(\det e)^2 \neq 0$) → four active channels → field closure → constitutive law → action → the inverse pipeline.
- **Exploratory programmes** (not part of the physics claims): the I Ching trigrams as cube vertices and the BBP π formula selected by the TIME axis; the Great Pyramid's King's Chamber at $z^*/h = 1 - 1/\sqrt2$; the oscillator Ising solver.

---

## 12. Open problems (stated in the README)

1. The RAR cannot separate GFD from MOND's simple function; discriminating tests are TF evolution, torsion, constants.
2. $a_0$ is empirical in the galactic test; two $a_0$–$H$ relations differ by 1.128.
3. $H_0$ appears as 69.92, 70.21, 70.29; the ±6% band does not yet discriminate Planck from SH0ES.
4. Clusters and the Bullet Cluster: qualitative only (VII); no lensing reconstruction.
5. CMB: one enhancement factor, no full power spectrum.
6. $\mathcal L_{\rm matter}$ unspecified.
7. Constants: numerical routes, subject to look-elsewhere effects.
8. No peer-reviewed publication yet.

---

## 13. Where to verify

| Claim | Script | Checks |
|---|---|---|
| RAR on SPARC | `papers/letter-radial-acceleration-relation-sparc/sparc_rar.py --from-csv supplementary/sparc_rar.csv` | σ = 0.181 |
| Two bounded regions | `proofs/tetrad-scheme-two-bounded-regions/` | 39 |
| Forced tetrahedral frame | `proofs/forced-tetrahedral-frame/` | 27 |
| Hadamard cube frame | `proofs/hadamard-cube-frame/` | 25 |
| Torsion = regular rep of $S_4$ | `proofs/torsion-regular-representation/` | 36 |
| Exchange symmetry → $\mu$ | `proofs/constitutive-law-exchange-symmetry/` | 34 |
| $F(y)$ closed form, convexity | `proofs/aqual-energy-functional/` | 24 |
| Gram theorems | `papers/gram-matrix-of-tetrad-equation/verify_gram_theorems.py` | 32 |
| Letters 1, 2, 3 | `papers/letter-*/…/Supplementary/run_all_validations.py` | 29, 52, 52 |
| TF evolution | `papers/tully-fisher-velocity-evolution/` | 64 |
| AQUAL algebra (§§4.5–4.7 here) | `research/aqual/verify_*.py` | 50, 48, 23 |
| Framework / constants | `research/gfd_enterprise_validation-v2.py`, `research/gfd_fundamental_constants.py` | 92, 36 |
