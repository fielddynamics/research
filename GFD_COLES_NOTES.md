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

With Paper II's cosmological scaling $a_0 \propto H^{1-1/\pi}$, the exponent is $(1 - 1/\pi)/4 = 0.170$. (Paper X gives a different stated mechanism for the same 0.17: disformal screening of the photon path, governed by $\sqrt{K/\pi}$; it cites the derivation rather than showing it.)

$$\frac{v(z)}{v(0)} = \left[\frac{H(z)}{H_0}\right]^{0.17},\qquad H(z) = H_0\sqrt{\Omega_m(1+z)^3 + \Omega_\Lambda}.$$

Predicts +21% at $z = 2$, $>1.3$ at $z > 3$ (ΛCDM: 1.0). Nine IFU measurements, $0 < z < 3$ (ratios 1.21 at $z = 2$, 1.29 at $z = 3$), fall within the band. Tests: JWST, ELT, Euclid at $z > 3$.

---

## 7. Cosmology and the acceleration scale

### 7.1 Horizon relation [D] (II)

$a_0 = cH_0/(2\pi)$ from horizon thermodynamics. At cosmic scales, closures tile with hexagonal contact geometry; averaging over the boundary ($\langle\theta\rangle$ of $\theta(d) = 2\cos^{-1}(d/2R)$) gives the factor $1/\pi$ and $a_0 \propto H^{1 - 1/\pi}$.

### 7.2 CMB enhancement [D/O] (II)

Planck's target is $x = 0.185$ ($1.185/0.185 = 6.40$). The linear estimate $x = g_N/a_0$ gives 722, the self-consistent deep estimate $x = \sqrt{g_N/a_0}$ gives 28; the tiling suppression $(H_0/H)^{1/\pi} = 0.041$ at $z = 1100$ gives $a_0 = 1.05\times10^{-7}$ m/s², $x = 0.183$ and enhancement $1.183/0.183 = 6.46$ (+0.9%). Only this single factor is computed, not the full power spectrum. (Paper XII quotes $E = 6.44$ against $\Omega_m/\Omega_b = 6.36\pm0.10$; Planck 2018 central values give 6.39–6.40.) Paper II also lists consequences for the Planck lensing anomaly, JWST early galaxies and DESI's evolving dark energy.

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
- The single formula is $H = 2\pi a_0/(c\sqrt{k/\pi})$, i.e. $a_0 = (cH_{\rm meas}/2\pi)\sqrt{k/\pi} = cH_{\rm flat}/2\pi$. Paper IV evaluates it twice: $a_0 = 1.220\times10^{-10}$ (MOND empirical) gives **69.92**; $a_0 = 16Gm_e/r_e^2 = 1.225\times10^{-10}$ gives **70.21** (used in Papers VII and X). The 0.41% gap is the $16$ vs $15.93$ coupling test. **70.29** is the 70.21 value with the Schwinger one-loop factor $(1+\alpha/2\pi)$ carried through $G\to a_0\to H$ (Paper VII), and is the value the TF manuscript uses. Paper X quotes $a_0 = 1.2\times10^{-10}$ in its opening, 78.9 as the naive value (that is $a_0 = 1.22$) and 70.21 (that is 1.225): three inputs in one letter. Notes that write $a_0 = cH/2\pi$ with the *measured* $H$ (e.g. 1.086×10⁻¹⁰ at 70.21) mix the flat and measured frames.

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
- Odd terms vanish by orientation parity in VIII; XII, the more careful version, separates three theorems (exchange identity, pairing $\beta_0=\beta_4$, $\beta_1=\beta_3$, Hessian of $e_2$ at $I$ of rank 16 with spectrum $+3^1,+1^6,-1^9$) from three axioms ($\beta_1=\beta_3=0$ by symmetric closure, $\beta_0=1$, $\beta_2$ = Hessian rank), and states that generic ghost-free theories allow $\beta_1=\beta_3\ne0$ and that the data alone cannot pick $\beta_2 = 16$ over 15 or 17. Detail: VIII's wording is that odd terms vanish by orientation parity ($\lambda\to-\lambda$ flips $e_1, e_3$); metric exchange $S\to S^{-1}$, with $e_n(S^{-1}) = e_{4-n}(S)/e_4(S)$, pairs $\beta_0 = \beta_4$ (and $\beta_1 = \beta_3$); normalisation sets $\beta_0 = 1$. The proportional background $S = I$ is a stable minimum, $V''(I)>0$.
- Ghost freedom: the 4-form interaction is linear in the lapse ($dt\wedge dt = 0$, $\partial^2\mathcal L/\partial N^2 = 0$), so the potential lies in the ghost-free class by construction.
- The helicity-0 mode (Stückelberg $\varphi^\mu = x^\mu - \partial^\mu\pi/\Lambda_3^3$) gives Galileon terms with $c_k(\beta)$ fixed by the lock; their static limit is algebraic, $\mathcal P(\pi'/r) = GM/r^3$. **Open:** VIII frames the match of this relation to $\mu = x/(x+1)$ (hence $F$) as a checkable problem and does not compute it. VIII's own $N = 2$ label ("bimetric lock") differs from the later bound-law reading (§4.6).
- XII adds three theorems + three axioms, a term-by-term map of the two actions, and six concordance checks (expansion history, BBN, CMB enhancement, Vainshtein screening, Galileon hierarchy, mixing angle $\tan\theta = D/(V+E+F) = 3/28$, $\theta = 6.12°$; $\Delta\mu = 2/17 = 11.76\%$).

---

## 10. Nuclei [E] (XI, XIII)

### 10.1 Paper XI: packing and a one-line binding formula

$$\frac{\text{BE}}{A} = C\,[\,f(K, s_2(A^2)) - 17\,],\qquad f(K, s_2(A^2)) = 13 + 8\,\mu_2(A^2),\qquad C = \frac{m_ec^2\cdot17}{K} = 2.172\ \text{MeV},$$

where $\mu_2$ is the bound law. Ceiling $C(21 - 17) = m_ec^2\cdot17 = 8.687$ MeV. 82 isotopes He–Bi: $R^2 = 0.99$, mean error 3.9%, 98% within 10%.

**Magic numbers.** Tetrahedral numbers minus a Sierpiński gate:

$$T(n) = \frac{n(n+1)(n+2)}6,\quad G(n) = \begin{cases}0 & n < K\\ (n-1)n/2 & n\ge K\end{cases},\quad M(n) = 2[T(n) - G(n)] \Rightarrow \{2, 8, 20, 28, 50, 82, 126\}.$$

$K = 4$ is the unique integer in $2\le K\le10$ that gives all seven ($K = 3$ gives 14 in place of 20; $K = 5$ gives 40 in place of 28). The formula's $\mu_2(A^2)$ is monotonic, so BE/A rises toward its ceiling and has no Fe peak: about −4–5% in the middle, +6–10% at Pb/Bi, −31% at He-4. Ceiling $M(n) \le K^K = 256$: no shell beyond the eighth, consistent with Bi-209 as the heaviest stable isotope.

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
2. $a_0$ is empirical in the galactic test. Its link to $H$ ($a_0 = cH_{\rm flat}/2\pi$, $H_{\rm meas} = H_{\rm flat}/\sqrt{k/\pi}$) rests on the frame factor $\sqrt{k/\pi}$, which Paper IV calls a dimensional argument.
3. $H_0$ is quoted as 69.92 and 70.21 (the same formula with the empirical and the electron-derived $a_0$) and 70.29 (70.21 with the one-loop correction); the ±6.2% cage does not discriminate Planck from SH0ES.
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

---

# Part II — Paper by paper

*Each entry below was written after reading the full paper. Entries give the paper's own claims and algebra, its stated scope, and notes where it differs from later work. Part I above is the thematic summary; where an entry here corrects Part I, Part I has been updated.*

## Paper I — The Gravitational Constitutive Law (No Dark Matter Required)

*Jan 2026, v5 · doi:10.5281/zenodo.18332595 · DFP vocabulary · non-relativistic effective theory*

**Question.** AQUAL, $\nabla\cdot[\mu(|\nabla\Phi|/a_0)\nabla\Phi] = 4\pi G\rho$, fixes only the limits $\mu\to1$ ($x\to\infty$) and $\mu\to x$ ($x\to0$); the simple, standard $x/\sqrt{1+x^2}$ and infinitely many other forms fit both. Paper I derives $\mu$ from how a source (the *field object*) couples to its environment (the *NET Field*) at an interface (the *closure boundary* $\Sigma$).

**Architecture (DFP terms → standard).** Field closure = non-degenerate metric, $\det g \ne 0$; closure constraints = ADM constraints; the canonical chain is Field Object + NET Field → $\Sigma$ → field closure function FC$_\Sigma$ (READ, then SETTLE) → registered state $B^*_\Sigma$. Two empirical requirements: **lossless** (no wakes, drag, hysteresis, secular drift; "Full-State Snapshot") and **local** (no faster-than-$c$ coordination). Motivation for distributed structure: the Laplacian is a neighbour comparison, $\nabla^2\Phi = \lim_{\epsilon\to0}[\Phi(x+\epsilon)+\Phi(x-\epsilon)-2\Phi(x)]/\epsilon^2$; wave propagation (LIGO) needs parts. $k = 4$ from the simplex theorem and the 1 + 3 ADM constraints.

**Postulates.** P1 Newtonian correspondence, $\lim_{x\to\infty}\mu = 1$. P2 distributed field processing: finite encoding capacity, scale-invariant deep regime, $\lim_{x\to0}\mu/x = 1$ (from $g \propto (GMa_0)^{1/2}/r$, i.e. $g = \sqrt{g_Na_0}$). P3 single-channel capacity saturation.

**MSC class** (Minimal Single-Channel Saturating Closure): (i) one occupancy $\varepsilon\in[0,1]$; (ii) detailed balance $W_+ = W_-$; (iii) linear saturation $f(\varepsilon) = 1-\varepsilon$; (iv) monomial driving $x^n$; (v) $\mu \equiv \varepsilon$.

**Derivation (Lemmas A.1–A.5).** Rates $r_+ = \alpha x^n(1-\varepsilon)$, $r_- = \beta\varepsilon$ give $\varepsilon_{\rm eq} = x^n/(k + x^n)$, $k = \beta/\alpha$. P2 forces $n = 1$; $k$ is absorbed into $a_0$:

$$\boxed{\mu(x) = \frac{x}{1+x}}\qquad(\text{Theorem 1: unique within MSC, "a conditional theorem"}).$$

Stability: $\dot\varepsilon = \kappa x(1-\varepsilon) - \kappa\varepsilon$, slope $-\kappa(x+1) < 0$, unique globally attracting fixed point. Cross-check table: $n = 2$ gives $\mu/x\to0$ and $v\propto r^{1/6}$; $n = 1/2$ gives $\mu/x\to\infty$ and $v \propto r^{-1/6}$; only $n = 1$ gives flat curves and $v^4 \propto M$.

**Three convergent readings.** (1) the kinetics above; (2) flow $d\mu/d\ln x = \mu(1-\mu)$ (logistic; "variance of a coin flip", maximal at $\mu = \tfrac12$, $x = 1$; RG-like running between a UV fixed point $\mu = 1$ and IR $\mu = 0$); (3) Padé[1/1] uniqueness: $\mu = ax/(bx+c)$ with three constraints gives $a = b = c = 1$. Also the odds power law $\mu/(1-\mu) = Cx^k$ with P2 forcing $k = C = 1$, and the remark $\mu(x) + \mu(1/x) = 1$ ("asymptotic rigidity": the deep limit fixes the Newtonian approach $\mu \simeq 1 - 1/x$). Same form as the Langmuir isotherm and Michaelis–Menten kinetics.

**Action.** $S[\Phi] = \int d^3x\,[-(a_0^2/8\pi G)F(X) - \rho\Phi]$, $X = x^2$, $F'(X) = \mu(\sqrt X)$, giving $F(x^2) = x^2 - 2x + 2\ln(1+x)$; $F \to (2/3)x^3$ deep. A scalar Lagrangian $L(x) = \tfrac12x^2 - x + \ln(1+x)$ with $dL = x\mu\,dx$ (equal to $F/2$). Status table in the paper: the function is the Famaey–Binney (2005) "simple" form; the contribution is the mechanism. Gentile et al. (2011) found it gives population-synthesis M/L ratios.

**Galactic consequences.** BTFR $v^4 = GM_ba_0$ (theorem of the deep limit). Phantom density as an operator residual,

$$\rho_{\rm ph} = \frac{1}{4\pi G}\left[\nabla^2\Phi - \nabla\cdot(\mu\nabla\Phi)\right] = \frac{\nabla\cdot[(\mu-1)\mathbf g]}{4\pi G},\qquad \rho_{\rm ph}(r) = \frac{\sqrt{GM_ba_0}}{4\pi Gr^2}\ (\text{deep, outside the source}),$$

a singular isothermal sphere. Conserved flux $r^2\mu(g/a_0)g = GM$. External field effect inherited from AQUAL: if $g_{\rm ext}\gg a_0 \gg g_{\rm int}$ then $\mu\approx1$ (Crater II, NGC 1052-DF2/DF4 as discriminants).

**Processing boundary** $r_c = \sqrt{GM_b/a_0}$ (where $x = 1$, $\mu = \tfrac12$): Milky Way ($6\times10^{10}M_\odot$) ≈ 8 kpc; Sun ≈ 7000 AU; Sgr A* ≈ 0.06 pc; MW total ≈ 5 kpc (listed); rich cluster ≈ 150 kpc; a 33-billion-tonne asteroid ≈ 4300 km.

**Predictions.** Fast bars $\mathcal R \approx 1.0$–1.4 (no halo-wake friction: conservative, velocity-independent, constraint-slaved phantom) vs $\gtrsim 1.4$–2 for CDM; wide binaries: Newtonian return $\mu\to1-1/x$ (slow) vs standard $1 - 1/(2x^2)$ (fast); EFE in satellites; baryon-only cluster lensing.

**Relativistic extension (1PN only).** Postulate A4 (single-standard calibration, clocks and radar-ranged rods from one field $L$): $A = L^2$, $B = L^{-2}$, so $g_{00}\simeq-(1+2\Phi/c^2)$, $g_{ij}\simeq(1-2\Phi/c^2)\delta_{ij}$, $\Phi = \Psi$, $\gamma = 1$. Lensing by "two-sphere saturation": $\varepsilon = \varepsilon_0S$, $\mu_0\to\mu_0S$, $n = S = 1 + 2GM/(rc^2)$; Fermat's principle with $\int dz/(b^2+z^2)^{3/2} = 2/b^2$ gives $\theta = 4GM/(bc^2)$, resolving scalar "half-lensing". A covariant action $S = \tfrac{c^3}{16\pi G}\int\sqrt{-g}R - \tfrac{a_0^2}{8\pi G}\int\sqrt{-g}\tilde F(Y) + S_m$ is stated as future work.

**Bullet Cluster.** "Constraint, not refutation." Expanding $\rho_{\rm ph} = [(\mu-1)\nabla\cdot\mathbf g + (\nabla\mu)\cdot\mathbf g]/4\pi G$, with $d\mu/dx = 1/(1+x)^2$ and $|\nabla x|\sim2x/r$: compact sources give sharper residual peaks ("peaks + pedestal"), so lensing peaks can follow galaxies while gas gives a broad floor. A baryon-only AQUAL forward-model pipeline (Bullet, El Gordo, MACS J0025) is specified; success metrics are given; the computation is deferred.

**Scope stated by the paper.** $a_0$ is an empirical input; cosmology (CMB, BAO, LSS) and cluster profiles are not addressed (ΛCDM favoured there, per its own table); time-dependent dynamics need the covariant completion; uniqueness holds only within MSC.

## Paper II — A Covariant Theory Without Dark Matter

*Jan 2026, v4 · doi:10.5281/zenodo.18360354 · DFP vocabulary*

**Question.** Can Paper I's law explain the CMB, where Planck needs a gravitating-to-baryonic ratio $\Omega_m/\Omega_b = 1 + 5.36 = 6.36$ (target enhancement ≈ 6.4)?

**Saturation scale (§2).** Gibbons–Hawking temperature $T_{GH} = \hbar H/(2\pi k_Bc)$ and the Unruh relation $T = \hbar a/(2\pi ck_B)$ give a minimum resolvable acceleration

$$a_0 = \frac{cH}{2\pi}.$$

Inverted with $a_0 = 1.2\times10^{-10}$: $H_0 = 2.51\times10^{-18}\,\mathrm{s^{-1}} = 77.61$ km/s/Mpc, which the paper notes is 6–15% above Planck (67.4) and SH0ES (73.0) and leaves open. With $a_0 \propto H(z)$ unmodified, $a_0$ at $z = 1100$ would be $2.36\times10^4$ times today's.

**Action (§3).** "Constitutive Lagrangian" $F(y) = \tfrac12y - \sqrt y + \ln(1+\sqrt y)$ (half of the later $F$), from $dL/dx = x\mu(x)$, and

$$S = \int d^4x\sqrt{-g}\left[\frac{R}{16\pi G} - \frac{a_0^2}{8\pi G}F(y) - \frac14e^{-2\phi/c^2}F_{\mu\nu}F^{\mu\nu} + \mathcal L_{\rm matter}\right].$$

"Two-sphere coupling": photons see $\tilde g_{\mu\nu} = e^{-2\phi/c^2}g_{\mu\nu}$, $n\approx1+2\Phi/c^2$, $\theta = 4GM/(rc^2)$. Appendix A: $G_{\mu\nu} = 8\pi G(T^{\rm m} + T^\phi + T^{\rm EM})$, $T^\phi_{\mu\nu} = (a_0^2/4\pi G)[\mu\,\partial_\mu\phi\partial_\nu\phi - g_{\mu\nu}F]$, $\nabla_\mu(\mu\nabla^\mu\phi) = 4\pi G\rho$.

**Cosmological equations (§4).** Modified Poisson $\nabla^2\Phi = 4\pi Ga^2\rho\delta/\mu(x)$; growth $\ddot\delta + 2H\dot\delta - 4\pi G\rho\delta/\mu(x) = 0$; $1/\mu = (1+x)/x$ acts as "phantom dark matter".

**The CMB gap (§5).** Target $x = 0.185$ (since $1.185/0.185 = 6.40$). Linear estimate $x = g_N/a_0 \approx 0.0014$ → enhancement 722 (113× too large). Self-consistent deep-MOND $x = \sqrt{g_N/a_0} = \sqrt{4\pi G\rho\delta/(k a_0)} \approx 0.037$ → 28 (4.3× too large).

**Closure tiling (§6).** Closures pack tetrahedrally (hexagonal in 2D projection). Two circular boundaries of radius $R$ at separation $d$ share arc $\theta(d) = 2\cos^{-1}(d/2R)$. Fixed $d = R$: $\theta = 2\pi/3$, fraction $1/3$. Uniform $d\in[0,2R]$:

$$\langle\theta\rangle = \int_0^1 2\cos^{-1}u\,du = 2\left[u\cos^{-1}u - \sqrt{1-u^2}\right]_0^1 = 2,\qquad \frac{\langle\theta\rangle}{2\pi} = \frac1\pi .$$

Uniform weighting justified by microcanonical, scale-invariance ($n_s\approx0.965$), maximum-entropy and homogeneity arguments.

**Scaling law (§7).**

$$a_0(z) = \frac{cH(z)}{2\pi}\left(\frac{H_0}{H(z)}\right)^{1/\pi} \;\Rightarrow\; a_0 \propto H^{1-1/\pi},\quad 1 - \tfrac1\pi \approx 0.682 .$$

At $z = 1100$: $(1/23600)^{0.318} = 0.041$, $a_0 = 2.55\times10^{-6}\times0.041 = 1.05\times10^{-7}$ m/s², self-consistent $x = 0.183$, enhancement $1/\mu = 1.183/0.183 = 6.46$ vs 6.40 (+0.9%). The discrete exponent $1/3$ gives $x = 0.198$, 6.05 (−5.5%).

**Predictions (§8).** All from $a_0\propto H^{0.682}$:
- Tully–Fisher: $v(z)/v(0) = [a_0(z)/a_0(0)]^{1/4} = [H(z)/H_0]^{0.682/4} = [H(z)/H_0]^{0.17}$: +5% ($z = 0.5$), +10% (1), +21% (2), +30% (3). SINS reports ≈ +27% at $z\approx2$, inside the ±6.2% band of Paper V.
- DESI: $w_{\rm eff} = (F - yF')/(F + yF')$, said to approach −0.85 in the deep regime and 0 in the Newtonian.
- JWST early galaxies at $z = 10$: $a_0$ 9.5× higher; Jeans mass ratio $(\mu_{\rm DFP}/\mu_{\rm MOND})^{3/2}\approx0.03$, collapse time ratio ≈ 0.32.
- Planck lensing anomaly $A_L = 1.18\pm0.07$: $A_L \approx 1 + \langle E(z) - 1\rangle_{z\sim0.5-2}$ gives 1.15–1.20.
- Bullet Cluster infall velocity: $a_0(0.3)/a_0(0) \approx 1.10$; $1/\mu$ from 2 to 2.4 gives a 10% velocity boost (2700 → ~3000 km/s); phantom/baryon ratio rising with cluster redshift (1.10 at $z = 0.296$, 1.18 at 0.59, 1.26 at 0.87).
- Bidirectional BTFR worked example: $M = 10^{11}M_\odot$ → 200 km/s; $v = 150$ km/s → $3.2\times10^{10}M_\odot$.

**Scope stated.** No full CMB power spectrum (needs a Boltzmann code), no cluster dynamics, no quantum origin of the scale.

**Later revision.** Paper III onward keeps $a_0 = cH/2\pi$ only for flat space and introduces the factor $\sqrt{k/\pi}$; the H₀ value moves from 77.61 to 78.90 (flat) and 69.92 (measured).

## Paper III — The Unit of Gravity

*Jan 2026, v5 · doi:10.5281/zenodo.18362768 · DFP vocabulary*

**Question.** $k = 4$ is dimensionless and $a_0$ is an acceleration; what sets the *size* of the gravitational tile?

**Tetrad coupling $k^2 = 16$.** $e^a{}_\mu$ has $4\times4 = 16$ components; isotropy engages all of them, so the "topologically coupled" acceleration of mass $m$ at $r$ is $a_{\rm coupled} = k^2Gm/r^2 = 16\,Gm/r^2$.

**Crossover condition.** Setting $k^2Gm/r^2 = a_0$:

$$r = k\sqrt{\frac{Gm}{a_0}} .$$

**Two routes to 2.82 fm.**
- Route 1 (EM, no gravity): $U_{\rm EM} = e^2/(4\pi\varepsilon_0r) = m_ec^2 \Rightarrow r_e = e^2/(4\pi\varepsilon_0m_ec^2) = 2.818$ fm.
- Route 2 (gravity, no EM): $r_e = 4\sqrt{(6.674\times10^{-11})(9.109\times10^{-31})/(1.22\times10^{-10})} = 2.82$ fm.
- Agreement 0.21%. Unique to the electron: the muon misses by ~$10^3$, the proton by ~$10^7$. The electron is "a probe, not a cause".
- Equivalent statement: $a_0 = k^2Gm_e/r_e^2 = 16\,Gm_e/r_e^2$; measured $a_0/(Gm_e/r_e^2) = 15.93$ (0.41% from 16).
- Route 3 (from Paper IV): $r_e = k\sqrt{2\pi Gm_e/(cH)} = 2.82$ fm, i.e. Route 2 with $a_0 = cH/2\pi$.

**The two $a_0$ values and $\sqrt{k/\pi}$.**

$$a_0^{\rm cosmo} = \frac{cH}{2\pi} = 1.08\times10^{-10},\qquad a_0^{\rm geom} = k^2\frac{Gm_e}{r_e^2} = 1.22\times10^{-10},\qquad \frac{a_0^{\rm geom}}{a_0^{\rm cosmo}} = 1.130 \approx \sqrt{\frac4\pi} = 1.128\ (0.1\%).$$

Interpreted as the frame correction between flat tetrahedral closure ($k$) and the spherical horizon ($\pi$); the square root because $k/\pi$ compares area-like quantities.

**Hubble prediction.** $H = 2\pi a_0/c$ with $a_0 = 1.22\times10^{-10}$ gives 78.90 km/s/Mpc. Historical note in the paper: v1–v3 read this as the Hubble constant; after Paper IV it is $H_{\rm flat}$, and $H_{\rm measured} = 78.90/\sqrt{k/\pi} = 69.92$ (GW170817: $70.0\pm12$).

**Falsification criteria given.** Coupling ratio outside $16\pm1$; the two routes diverging by >1%; $\sqrt{k/\pi}$ failing by >1%; data requiring $k\ne4$. **Not claimed:** $r_e$ from pure topology, $m_e$ from first principles, MOND's correctness.

## Paper IV — Resolving the Hubble Tension Through Tetrad Topology

*Jan 2026 · doi:10.5281/zenodo.18371849 · arXiv-format source*

**Chain to $k = 4$.** GR + LIGO (gravity propagates) → wave equation → the Laplacian needs neighbours → coupling topology exists. Three routes to $k = 4$: four tetrad legs; four ADM constraints (one Hamiltonian, three momentum, read as the integrability conditions *for* the tetrad, closing under the Dirac algebra); LIGO's two polarisations, $10 - 2k = 2$. Uniqueness: $k\ge4$ (closure, simplex theorem) and $k\le4$ (more constraints leave $<2$ propagating modes or Boulware–Deser ghosts).

**Closure = non-degeneracy.** Completeness $e^a{}_\mu e_a{}^\nu = \delta_\mu^\nu$ and $\det g = -(\det e)^2$, so $\det g\ne0 \iff \det e\ne0$. Tetrad gravity is first-order symmetric hyperbolic with characteristic speed $c$ (Buchman & Bardeen 2003): the "closure rate".

**Acceleration scale.** Gibbons–Hawking $T = \hbar H/(2\pi k_B)$ = Unruh $T = \hbar a/(2\pi k_Bc)$ gives $a_0 = cH/2\pi = c/C_H$, the speed of light over the horizon *circumference*.

**Tile size.** $k^2Gm/r^2 = a_0 \Rightarrow r = k\sqrt{Gm/a_0} = k\sqrt{2\pi Gm/(cH)}$; for the electron 2.82 fm vs EM 2.818 fm (0.21%). Forward check: $a_0^{\rm pred} = 16\,Gm_e/r_e^2 = 16\times7.66\times10^{-12} = 1.225\times10^{-10}$ (0.4% from 1.22).

**Central result.**

$$\boxed{H = \frac{2\pi k^2}{c\sqrt{k/\pi}}\cdot\frac{Gm_e}{r_e^2}},\qquad H_{\rm measured} = \frac{H_{\rm flat}}{\sqrt{k/\pi}} .$$

| Route | $a_0$ (m/s²) | $H_{\rm flat}$ | $H_{\rm measured}$ |
|---|---|---|---|
| A: MOND empirical | $1.220\times10^{-10}$ | 78.90 | **69.92** |
| B: electron-derived $16Gm_e/r_e^2$ | $1.225\times10^{-10}$ | 79.22 | **70.21** |

The 0.41% A–B difference is exactly the $k^2 = 16$ vs 15.93 test. GW170817 ($70.0\pm12$) lies between (0.11% above A, 0.30% below B). **This is where 69.92 and 70.21 both come from**; they are the same formula with the two $a_0$ inputs.

**Frame correction.** $\sqrt{k/\pi} = 1.128$ compares the flat tetrahedral frame ($k$ faces) with the spherical horizon ($\pi$ in $4\pi R^2$); square root because $H = v/d$ depends on length and $k/\pi$ is area-like. The paper calls this "a dimensional argument, not a rigorous derivation from Regge calculus".

**Reverse (electron mass).** Since $r_e\propto1/m_e$, $Gm_e/r_e^2 \propto m_e^3$:

$$m_e = \left(\frac{H\,e^4\sqrt{k/\pi}}{2\pi k^2G(4\pi\varepsilon_0)^2c^3}\right)^{1/3} = 9.10\times10^{-31}\ \text{kg at } H = 70\ (0.10\%\text{ of CODATA}).$$

**Hubble tension.** Measurements traverse different fractions of the flat-to-curved correction (0 to 12.8%); the geometric mean of a factor running from 1 to $\sqrt{k/\pi}$ is $(k/\pi)^{1/4} = 1.062$, giving the cage $69.92/1.062 = 65.8$ to $69.92\times1.062 = 74.3$ km/s/Mpc. Planck 67.4 (−3.6%), BAO 68.0, GW170817 70.0, TRGB 72.5, SH0ES 73.0, masers 73.9 (+5.7%) all inside. Reverse test: the six values × 1.128 average 79.1 (0.27% from 78.90). A naive chance estimate $(0.12)^6\approx3\times10^{-6}$ is given with the caveat that shared systematics overstate it.

**Falsifiers.** Coupling ratio outside $16\pm1$; GW-siren $H$ converging outside $70\pm3$; a credible $H$ outside 65.8–74.3; the $m_e$ ↔ $H$ link breaking. **Limitations stated:** $m_e$ is an input; $a_0 = cH/2\pi$ is taken from horizon thermodynamics, not derived from $k$; $\sqrt{k/\pi}$ is dimensional.

## Paper V — Field Closure and the Topology of Gravity ("The Tetrahedral Bridge")

*Jan 2026 · doi:10.5281/zenodo.18419531 · DFP vocabulary; mostly interpretive*

**Textbook closures it collects.**
- ADM: $\mathcal H = \sqrt\gamma(R^{(3)} + K^2 - K_{ij}K^{ij}) - 16\pi G\sqrt\gamma\rho = 0$ and $\mathcal H_i = -2\nabla_j[\sqrt\gamma(K^j{}_i - \delta^j_iK)] + 16\pi G\sqrt\gamma j_i = 0$ (1 + 3).
- Tetrad completeness $e^a{}_\mu e_a{}^\nu = \delta^\nu_\mu$ (four legs, none redundant).
- LQG: a 4-valent spin-network node is a quantum tetrahedron (Rovelli & Vidotto); closure $\hat J_1+\hat J_2+\hat J_3+\hat J_4 = 0$, the quantum form of Minkowski's theorem $\sum_{f=1}^4A_f\hat n_f = 0$.
- Regge calculus: $S = \sum_hA_h\epsilon_h$ on simplicial complexes.
- LIGO: $10 - 2k = 2$. Simplex theorem: $d+1$ points enclose a $d$-region.

**Reinterpretation.** Constraints are read as four coupling channels ("Coupling Ports") through which a Field Object and the NET Field settle (READ, then SETTLE) at $\Sigma$; settlement is atomic, enabled by quantum co-location (both states share the same local conditions). Lossless supported by MICROSCOPE ($10^{-15}$ EP test). New terms: **Field Envelope** (spherical extent, signature $\pi$), **Coupling Boundary**, **Field Chamber** (the tetrahedral interior, signature $k = 4$), with an engine analogy (cylinder volume, ports, swept volume, combustion chamber, compression ratio).

**Port Ratio.** $\sqrt{k/\pi} = 1.128$, from (1) area-to-length conversion or (2) an effective aperture $r_{\rm eff} = \sqrt{A_{\rm open}/\pi} = \sqrt{k/\pi}$ for open area $\propto k$. Candidate mechanisms ranked: aperture-constrained propagation (coherent, achromatic) > mode-constrained propagation with periodic structure > bare boundary normalisation. Scatter: half the 12.8% correction ≈ 6.4%, vs the 6.2% cage of Paper IV.

**Scale.** Three routes: EM radius 2.818 fm; $k\sqrt{Gm_e/a_0} = 2.82$ fm; coupling test $a_0/(Gm_e/r_e^2) = 15.93\approx16$. Hubble chain: $a_0 = 16Gm_e/r_e^2 = 1.225\times10^{-10}$ → $H_{\rm flat} = 79.2$ → $79.2/1.128 = 70.2$ (the paper's boxed number is 69.92, the Route-A value).

**Interpretive claims.** The tetrahedron is "the bridge": the LQG quantum of space, the tetrad frame, the Regge simplex and the DFP Field Chamber are the same geometry. The 1 + 3 asymmetry (one Hamiltonian constraint across time, three momentum constraints within a slice) is read as the mechanism for a full-state read. The paper separates what is citable textbook fact (its Table 6) from what DFP adds (terminology, mechanism, Port Ratio, scale identification, $H$).

## Paper VI — Deriving the Gravitational Constant from Spacetime Topology

*Feb 2026 · doi:10.5281/zenodo.18463038 · arXiv/REVTeX source · "The Dual Tetrahedral Field Chambers"*

**Four roads to two tetrahedra** (the paper's literature synthesis):
1. *Stability.* For one tetrahedron with face fluxes $\Phi_i$ and $\sum\hat n_i = 0$, the net flux is $\vec F_{\rm net} = (\Phi_{\rm TIME} - \Phi_{\rm SPATIAL})\hat n_{\rm TIME} = \delta\phi\,\hat n_{\rm TIME}\ne0$; an oppositely oriented partner gives $\delta\phi(\hat n_A + \hat n_B) = 0$. Cited: Alexander, Marcianò & Smolin (2014), the parity-symmetric phase carries a scalar ghost and is unstable; parity breaking yields the massless graviton plus an SU(2) triplet of chirally coupled Yang–Mills fields.
2. *Double cover.* SL(2,C) covers SO(1,3) twice ($\pm s$); Geroch (1968): spinor structure ⟺ a global orthonormal tetrad. Two distinct closures need two distinct tetrahedra.
3. *Chirality.* Ashtekar's $A = A^+\oplus A^-$; one tetrahedron per handedness.
4. *Bimetric.* Hassan–Rosen $S = M_g^2\int\sqrt{-g}R[g] + M_f^2\int\sqrt{-f}R[f] + m^2\int\sqrt{-g}V(g,f)$, ghost-free with 7 DOF (2 massless + 5 massive); "one metric → one tetrahedron" (Paper V).

Compatibility: Deffayet–Mourad–Zahariade symmetric-vielbein condition $g^{\mu\nu}E^A{}_\mu L^B{}_\nu = g^{\mu\nu}E^B{}_\mu L^A{}_\nu$, equivalent to real $\sqrt{g^{-1}f}$.

**The stellated octahedron** (unique two-tetrahedra compound, Coxeter). Unit-cube binary labels, parity = bit sum mod 2: TetA (odd) $\{001, 010, 100, 111\}$, apex $V_7 = (1,1,1)$; TetB (even) $\{000, 011, 101, 110\}$, apex $V_0 = (0,0,0)$. Theorems:
- T1 antipodal apexes, $\hat r_7 + \hat r_0 = 0$;
- T2 coupling point $C = (V_0+V_7)/2 = (\tfrac12,\tfrac12,\tfrac12)$;
- T3–T4 TIME faces $A_7 = \{V_1,V_2,V_4\}$ (centroid $(\tfrac13,\tfrac13,\tfrac13)$) and $B_0 = \{V_3,V_5,V_6\}$ (centroid $(\tfrac23,\tfrac23,\tfrac23)$); compressions $\pm(\tfrac16,\tfrac16,\tfrac16)$ cancel at $C$;
- T5 the symmetric-vielbein condition holds at $C$ ($\sqrt{g^{-1}f}\to\mathbb 1$) and only there.

**Field Origin** defined as the octahedral core at $C$: where the chambers intersect, the compressions cancel, the vielbein condition holds and angular momentum transfers. Faces: per tetrahedron 1 TIME (inward) + 3 SPATIAL (outward), read as the 3 + 1 split; total 2 + 6 = 8.

**Spin (Theorem T6).** Ansatz: a full circuit of one tetrahedron carries $\hbar$ ($\hbar/4$ per face), so $L = \hbar + \hbar = 2\hbar$ (360° + 360° = 720°, matching the double cover):

$$S = \frac{N_{\rm TIME}}{N_{\rm total}}\,L = \frac28\cdot2\hbar = \frac\hbar2 .$$

**Newton's constant.** With $D = 3+1$:

$$G = \frac{(3+1)^2+1}{3(3+1)+1}\,\alpha^{1+(3+1)+(3+1)^2}\,\frac{\hbar c}{m_e^2} = 1.3077\times1.338\times10^{-45}\times3.810\times10^{34} = 6.666\times10^{-11}$$

vs $6.674\times10^{-11}$ (0.12%). Exponent terms: 1 (time), $D$ (spacetime), $D^2$ (dual-tetrahedra interaction). Hierarchy: gravity/EM $\sim\alpha^{1+D+D^2}/\alpha = \alpha^{D+D^2} = \alpha^{20}\approx10^{-43}$.

**Fine-structure constant (explicitly an empirical observation, "not a derivation").**

$$\frac1\alpha = 2^d(k^2+1) + 1 + \frac{1}{k(k+d)} = 8\cdot17 + 1 + \frac1{28} = 137.035714\ldots$$

vs CODATA 137.035999177 (0.00021%). $2^d = 8$ orthants; $k^2+1 = 17$ = 16 tetrad components + identity; $k(k+d) = 28$. The residual (~1/3500) is suggested to be QED-like.

**Scope.** $\alpha$, $\hbar$, $c$, $m_e$ are inputs; the spin result rests on the stated angular-momentum ansatz; the 17/13 prefactor is read as "coupling channels versus structural elements".

## Paper VII — Dual Tetrad Topology and the Field Origin: From Nuclear Decay to Galactic Dynamics

*Feb 2026, v7 (latest of v2–v7) · REVTeX source · the series' longest synthesis; introduces "dual tetrad gravity" (DTG)*

**Foundations (§§2–3).**
- Closure = non-degeneracy: $\det g = -(\det e)^2$; Barbieri (1998): the discrete closure $\sum\vec n_i = 0$ on four face normals defines a tetrahedron at each node. The binary existence condition is the $k^0 = 1$ term.
- $k = 4$ from both sides ($k\ge4$ simplex, $k\le4$ from $10 - 2k = 2$). $d = 3$ from three intersecting constraints: $2(d+1) = 2^d$ (two simplices' face count = dual-lattice vertices), Bertrand's theorem (closed orbits need $1/r^{d-1} = 1/r^2$), no hydrogen bound states for $d\ge4$.
- Scale: $r_e$ by the two routes; $\alpha = r_e/\bar\lambda_C$, $\bar\lambda_C = \hbar/(m_ec)$.
- Four roads to two tetrahedra (as Paper VI), plus Hassan–Kocic (2018): the two metrics need compatible 3 + 1 decompositions. The compound has $V + E + F = 8 + 12 + 8 = 28$ elements and inversion symmetry $\mathbf r\to-\mathbf r$ swapping TetA and TetB.
- **Field Origin** = the Hassan–Rosen interaction vertex, where both tetrads are evaluated at one point and $\tau_{\rm prop} = r/c = 0$ ("the neck of the hourglass"); it permits the atomic Full State Snapshot. Vortex picture: angular momentum flows through the Field Origin; Einstein–Cartan links spin and torsion.

**Spin, two routes.** (1) faces: $(2/8)\cdot2\hbar = \hbar/2$; (2) polynomial: $21 - 17 = 4$ TetA face channels and $17 - 13 = 4$ TetB; an observer sees one sector, $(4/8)\hbar = \hbar/2$. The quantum $\hbar$ per circuit is stated as an empirical input.

**28 three ways.** $V + E + F = 28 = k(k+d) = 4\times7$ = 7 bimetric propagating modes (2 massless + 5 massive) × 4 faces.

**The coupling polynomial (§4).**
- Three causal stages: EXIST ($k^0 = 1$, $\det e\ne0$), PROPAGATE ($k = 4$: a TetB vertex pierces a TetA face centre, cutting it into 3 + 1 sub-regions), INTERACT ($k^2 = 16$, the $4\times4$ frame-transition matrix). No $k^3$ term: a simplex boundary has only 0-, 1- and 2-cells.
- Uniqueness by constraints (LIGO, simplex, ghost-free bimetric) and by component counting in $H_{\rm int} = m^2\sqrt g\sum\beta_ne_n(\mathcal S)$: $e_0 = 1$, $e_1 = \operatorname{Tr}\mathcal S$ ($k$ terms), $e_2 = \tfrac12[(\operatorname{Tr}\mathcal S)^2 - \operatorname{Tr}\mathcal S^2]$ ($k^2$ terms).
- $f = (k^3-1)/(k-1) = 63/3 = 21$; unit coefficients (one existence condition, one connection per face, one entry per frame pair). Self-similarity: each face again carries 1 + 4 + 16.
- Three structural states $f = 1 + sk + k^2$: TetA ($+k$, 21, exponent), Field Origin (no face channels, 17, numerator), TetB ($-k$, 13, denominator). Only the odd term flips. Mean lock $(21+13)/2 = 17$, spacing $k$. $17 = k^2 + 1$ ("coupling capacity"), $13 = kd + 1$ ("spatial structure"), using $k^2 - k = kd$.
- **Proposition (identification).** Under a common coupling point, the symmetric-vielbein condition and compatible 3 + 1 splits, the stellated octahedron's coupled-face matrix $C_{ab}$ equals the Hassan–Rosen $\mathcal S^a{}_b = (E^{-1})^a{}_\mu L^\mu{}_b$. Five conditions: index (vierbein leg ↔ face, $a = 0$ the time face), operation, block split $1 + 3 + 3 + 9$ (lapse/shift + triad), $\sum_n\binom4n = 16$, existence ($\det e\ne0$).

**Results.**
1. $G = \frac{17}{13}\alpha^{21}\hbar c/m_e^2 = 6.666\times10^{-11}$ (0.12%); exponent 20 or 22 misses by ×137; extracted $n = 20.9998$. One loop: $G(1 + \alpha/2\pi)$ gives $6.6742\times10^{-11}$ vs $6.6743$ (0.001%).
2. $1/r^2$ from flux over $4\pi r^2$ in $d = 3$ (same for Newton and Coulomb; depth $\alpha^{21}$ vs $\alpha^1$).
3. $E = mc^2$: mass is closure energy at the Field Origin; $\omega_{\rm closure} = c/r$, $N$ states, $\omega_{\rm state} = c/(Nr)$, $mc^2 = \hbar c/(Nr)$ ⇒ $m = \hbar/(Nrc)$; with $N = 1/\alpha$, $m = \alpha\hbar/(rc)$ (the classical-radius relation). $c^2 = c_{\rm TetA}c_{\rm TetB}$ (dimensions, bilinear metric, exchange symmetry).
4. Hierarchy: EM couples to one sector ($\alpha^1$), gravity to both ($\alpha^{21}$): $\alpha^{20}\approx10^{-43}$.
5. $1/\alpha = 1 + 2k(k^2+1) + 1/[k(k+d)] = 137 + 1/28 = 137.0357$ (0.00021%). Integer part = 1 vertex + 8 vierbein legs × 17-dimensional interaction space; $2k^3 + 2k + 1 = 137 \Rightarrow k^3 + k = 68 \Rightarrow k = 4$. $k + d = 7$ = 12 configuration components − 4 diffeomorphisms − 1 ghost constraint. Rate check: $f_{\rm closure}/f_{\rm Compton} = (c/r_e)/(m_ec^2/h) = 2\pi/\alpha$ (an identity of the definitions).
6. $a_0 = k^2Gm_e/r_e^2 \approx 1.22\times10^{-10}$; $a_0 = (cH/2\pi)\sqrt{k/\pi}$; $H = 2\pi a_0/(c\sqrt{k/\pi}) = 70.21$; one loop gives **70.29** (the TF manuscript's value).
7. Electron mass: $a_0 = k^2Gm/r^2$ and $a_0 = (cH/2\pi)\sqrt{k/\pi}$ with $m = \alpha\hbar/(rc)$ give $r^3 = 2\pi^{3/2}k^{3/2}\alpha\hbar G/(c^2H)$, i.e. $r = [(3+1)^2\pi^{3/2}\alpha\hbar G/(c^2H)]^{1/3} = 2.82$ fm and $m = 9.11\times10^{-31}$ kg (0.1%).

**Galaxies (§7).** Detailed balance gives $\mu = x/(1+x)$; exchange $g\leftrightarrow f$ sends $x\to1/x$, and $\mu(x) + \mu(1/x) = 1$ holds for $x/(n+x)$ only if $n = 1$ (the "1" is the Field Origin). Newtonian-inferred dark fraction $1 - \mu = a_0/(g + a_0)$ (91% at $g = 0.1a_0$). Milky Way (7.5×10¹⁰ M☉: Hernquist bulge, exponential disk and gas), DTG vs standard-$\mu$ MOND vs Newton: 228/205/195 km/s at 5 kpc, **225**/200/179 at 8 kpc (obs. 229 ± 5), 208/191/126 at 20 kpc, 196/188/80 at 50 kpc (83% "dark"); reduced $\chi^2\approx1$ against seven datasets (Eilers, Jiao/Gaia DR3, Sofue). "Corrective lens" $M_{\rm actual} = M_{\rm inferred}\,g/(g + a_0)$. Clusters, Bullet Cluster and CMB are listed as known challenges.

**Covariant completion (§8).**
- Hassan–Rosen vielbein action $S_{\rm HR} = \int[e\,e\,e\,\Omega + \tilde e\,\tilde e\,\tilde e\,\tilde\Omega + m^2e\sum\beta_ne_n(e^{-1}\tilde e)]$. Fixing the $\beta_n$: (1) parity $e_n(-\lambda) = (-1)^ne_n$; (2) exchange $e_n(\mathcal S^{-1}) = e_{4-n}(\mathcal S)/e_4(\mathcal S)$ with $\mathcal S = I$ at the Field Origin, so $\beta_0 = \beta_4$, $\beta_1 = \beta_3$; (3) odd terms vanish at the symmetric point, $\beta_1e_1(I) + \beta_3e_3(I) = 8\beta_1 = 0$; (4) $\beta_0:\beta_2:\beta_4 = 1:k^2:1$. Result $V = e_0 + 16e_2 + e_4$ (weighted count $1 + 96 + 1 = 98$), testable through the massive-graviton spectrum.
- Scalar-tensor form $S_{\rm ST}$ (the four-term action; this is the SST). Term reading of $F$: $y$ ↔ $k^2$ (full interaction), $-2\sqrt y$ ↔ $k$ (face level; the sign echoes $s = -1$, the 2 counts two tetrahedra), $2\ln(1+\sqrt y)$ ↔ $k^0$ (the Field Origin floor). $e^{-2\Phi/c^2}$: the 2 counts two tetrahedra; $\gamma = 1$ (Cassini). Whether the scalar-tensor theory is the formal low-energy limit of the locked bimetric theory is stated as open.
- 14 tests + 1 check: $\gamma = 1$; $|v_{gw}/c - 1| < 10^{-15}$; neutron bound-decay probability 1.084% vs $1.081\pm0.03$% (SM ≈ 0.0004%), tied to the tetrahedral dihedral angle $\arccos(-1/3)$; MW 225 vs 229 ± 5; Gaia wide-binary plateau 0.39 vs $0.5\pm0.15$ km/s; Bullet offset $150\pm30$ kpc "consistent with gas displacement" (no simulation).

**Poisson and scale invariance (§9).** $k = 4$ is topological (immune to renormalisation); $4\pi = k\times\pi$ ($\pi$ steradians per face); $\nabla^2\Phi = k\pi\cdot\frac{k^2+1}{kd+1}G_{\rm bare}\rho = 16.493\,G_{\rm bare}\rho$, i.e. $G_{\rm eff} = (17/13)G_{\rm bare}$.

**Mechanism (§11).** Field Object, Field Atom $A_\Phi$ (a geon-like soliton of the massive spin-2 mode, with a "Valence Horizon"), Full State Snapshot, Settlement, Registration $B^*_\Sigma$ (grounded in ADM, Israel junction conditions, York–Lichnerowicz, Dirac constraints; appendix). **Bound vs unbound is defined here:** an *unbound* gravity-field envelope has an empty TetB chamber (massless mode; the mesh, "the stage"); a *bound* envelope has an occupied TetB (massive mode; matter, "the actors"). Binding by stellar compression, up to electron capture $p + e^-\to n + \nu_e$; TOV balance; the Field Origin as the eye of a self-sustaining vortex. Chessboard picture: bound configurations sit only on mesh nodes where $\det e\ne0$.

**Nuclear packing in TetB (heuristic, stated as not derived from the field equations).** He-4 first closed nucleus ($A = k$, 7.07 MeV/nucleon vs 2.83, 2.57 for $A = 3$); O-16 $= k^2$ tetrahedral α-clustering; α-ladder ¹²C, ¹⁶O, ²⁰Ne, ²⁴Mg, ²⁸Si; Be-8 ($2k$) unbound, $8.2\times10^{-17}$ s; ceiling $k^4 = 256$ (Fm-258 fissions, fragments near 128); binding peak near Fe-56.

**Summary claims.** Dependency chain $d = 3 \to k \to f \to \{21,17,13\} \to G, 1/\alpha, \beta_n$, spin, $1/r^2$, $E = mc^2$, $\alpha^{20} \to a_0, \mu \to H, m_e \to$ one-loop. Every integer named: 1 vertex, 4 faces, 8 vierbein legs, 13, 16 frame matrix, 17 interaction space, 21 depth, 28 elements, 137 breadth. Not addressed: strong and weak forces, the particle mass hierarchy, the cosmological constant.

## Paper VIII — Gravity Field Dynamics and Bimetric Gravity: Dual Tetrahedral Field Chambers as the Key to the General Parameters

*Letter. Companion: GFD Essentials; supplementary `fig1_dual_tetrahedral_field_chamber.html`, `run_all_validations.py`. Status of the main claims: [D] for the locked $\beta_n$ and the IR algebra; the UV→IR matching is stated as open.*

**Claim.** The five Hassan–Rosen coefficients are not free. One polynomial $f(k,s) = 1 + ks + k^2$ at $k = 4$ gives both the UV bimetric potential (its "static skeleton" at $s = 0$) and the IR constitutive law (its "dynamic body" as $s$ varies).

**Geometry made explicit (half-space form).**
- Face projections $v_1 = x+y+z$, $v_2 = x-y-z$, $v_3 = -x+y-z$, $v_4 = -x-y+z$.
- TetA: $\max_i v_i\le1$. TetB: $\max_i(-v_i)\le1$. The intersection is the central octahedron (the Field Origin); the union is the stellated octahedron.
- Fig. 1 samples $4\times10^6$ points against these inequalities, with no mesh. Each TetA face is cut by the piercing TetB vertex into 3 corners + 1 inverted core, giving $4\times4 = 16$ boundary channels.

**Locking the coefficients.**
1. *Basis is unique.* A derivative-free covariant scalar density built from tetrad one-forms is a 4-form, $\epsilon_{abcd}\,\tilde e^{a_1}\wedge\cdots\wedge\tilde e^{a_n}\wedge e^{a_{n+1}}\wedge\cdots\wedge e^{a_4} = e\,e_n(S)\,d^4x$, with $S = e^{-1}\tilde e$. So $V = \sum_{n=0}^4\beta_ne_n(S)$ is forced, not assumed.
2. *$\beta_2 = 16$, primary (geometric).* $e_2(S) = \tfrac12[(\operatorname{Tr}S)^2 - \operatorname{Tr}S^2]$ counts pairwise couplings; weighting it by the 16 boundary channels gives each channel unit weight.
3. *$\beta_2 = 16$, secondary (covariance).* $\dim C\ell_{1,3} = \sum_k\binom4k = 16 = \dim\operatorname{End}(\mathbb R^{1,3})$ = the components of $S$. Once the other terms are fixed, $e_2$ is the only free term and "must absorb" all 16; the paper words this as an interpretation ("we therefore interpret").
4. *Parity:* under $\lambda_i\to-\lambda_i$ the odd $e_1, e_3$ change sign (grade 1 and 3 reverse), so $\beta_1 = \beta_3 = 0$. *Exchange:* $g\leftrightarrow f$ sends $S\to S^{-1}$, so $\beta_0 = \beta_4$. *Normalisation:* $\beta_0 = 1$.
5. Result: $(\beta_0,\ldots,\beta_4) = (1,0,16,0,1)$, $V(S) = e_0 + 16e_2 + e_4$. Polynomial reading: the $1$ is bare existence ($\beta_0 = \beta_4$), $k^2 = 16$ is $\beta_2$, and no odd power gives $\beta_1 = \beta_3 = 0$.

**Ghost freedom.**
- ADM split: $e^0 = N\,dt + N_idx^i$. A 4-form contains exactly one $dt$, and $dt\wedge dt = 0$, so $\partial^2\mathcal L_{\rm int}/\partial N^2 = \partial^2\mathcal L_{\rm int}/\partial\tilde N^2 = 0$.
- The potential is in the Hassan–Rosen class, so the secondary constraint and the BD-ghost removal are inherited. The locked set is a point inside the ghost-free family.

**UV → IR bridge (EFT statement, explicitly not an identity of actions).**
- Stückelberg: $\tilde e^a{}_\mu\to\tilde e^a{}_\nu(\varphi)\partial_\mu\varphi^\nu$ with $\varphi^\mu = x^\mu - \partial^\mu\pi/\Lambda_3^3$, $\Lambda_3 = (m^2M_{\rm Pl})^{1/3}$.
- In the decoupling limit, $\mathcal L_\pi = c_2(\partial\pi)^2 + c_3(\partial\pi)^2[\Pi]/\Lambda_3^3 + c_4(\partial\pi)^2([\Pi]^2 - [\Pi^2])/\Lambda_3^6 + \cdots$, with $c_k(\beta)$ now fixed rather than tunable.
- The background $S = I$ is a stable minimum, $V''(I) > 0$. Matter drives the tetrads apart and switches on Vainshtein screening. In GFD language this is the node moving from $s = 0$ toward $s\to+1$.
- Static reduction is algebraic, $\mathcal P(\pi'/r) = GM(r)/r^3$.
- **Open (the paper's own words):** computing the quasi-static relation from the locked $c_k$ and showing it gives $\mu(x) = x/(x+1)$ "is the natural next step". Paper VIII frames it as a checkable matching problem; it does not do the calculation.

**IR algebra.**
- Conformal map $s(x) = (x-1)/(x+1)$, with $x\to0\Rightarrow s\to-1$, $x = 1\Rightarrow s = 0$, $x\to\infty\Rightarrow s\to+1$. It is called the unique Möbius map from $[0,\infty)$ onto $[-1,1]$ that fixes the transition point.
- $f(x) = 17 + 4s(x) = (21x+13)/(x+1)$, and $\mu = (f-13)/8 = x/(x+1)$.
- $F(y) = y - 2\sqrt y + 2\ln(1+\sqrt y)$ from $\mu(\sqrt y) = F'(y)$.
- "Stellated octahedron field equation": $\nabla\cdot\big[\tfrac{f(x)-13}{8}\nabla\Phi\big] = 4\pi G\rho$ (the AQUAL/MOND equation with $\mu$ written through $f$).

**$N$-metric family.**
- $x(1-\mu)^N = \mu$ with $\mu = (f-13)/8$ and $1-\mu = (21-f)/8$ gives $x = 8^{N-1}(f-13)/(21-f)^N$.
- $N = 1$: $x = (f-13)/(21-f)$, $\mu(1) = \tfrac12$.
- $N = 2$: $x = 8(f-13)/(21-f)^2$, $\mu = (\sqrt{1+4x}-1)/(\sqrt{1+4x}+1)$, which is the same function as Part I's $\mu_b$ (checked numerically), and $\mu(1) = 1/\varphi^2\approx0.382$.
- Proposed test: the two laws differ only near $x\sim1$.

**Notes against later work.**
- *$s$ vs $\sigma$.* Paper VIII lets the state label vary continuously, $s(x) = (x-1)/(x+1)$. Later naming keeps $s\in\{+1,0,-1\}$ as discrete states and calls the continuous quantity $\sigma(x)$. Paper VIII's "$s = 0$ at $x = 1$" is $\sigma = 0$ in later notation, and that point is not the Field Origin.
- *Deep field vs TetB.* Paper VIII says that in the deep-MOND regime the response "saturates at the geometric floor provided by the adjacent, inverted TetB subspace ($s\to-1$)". In the later reading this describes the TetB share $1-\mu\to1$ seen from the exterior (the deep field), not the field being in TetB.
- *What $N = 2$ means.* Paper VIII calls $N = 2$ "the Hassan–Rosen bimetric lock" and "the dual-tetrad interaction", and calls $N = 1$ the "effective single-metric SST" and "screened" limit. Later work (IX, XIII, research/aqual) reads $N = 1$ as the one-directional law for a galaxy's exterior and $N = 2$ as the bound law for nuclei. It derives $N = 2$ as the exchange image of the source form, not from counting metrics.
- *The SST action here has three terms.* It omits the $-\tfrac14e^{-2\Phi/c^2}F_{\mu\nu}F^{\mu\nu}$ term that the full SST has (§3). The name already means the action, as later naming requires.
- *What $e_2$ counts.* As a sum over $a<b$, $e_2$ has $\binom42 = 6$ principal $2\times2$ minors, so $e_2(I) = 6$ and $V(I) = 1 + 96 + 1 = 98$ (as Paper VII). The 16 is supplied by the channel count and the $\dim C\ell_{1,3}$ argument, not by the number of terms in $e_2$.

## Paper IX — Complete Field Closure from Stellated Octahedron Topology

*Letter. Companion to VIII (which carries the full $\beta_n$ derivation and the ghost-freedom proof). Validation: `run_all_validations.py`, 45 tests in 19 sections. Status: [T] for the combinatorics and algebra, [D] for the physics chain, [E] for the π section.*

**Thesis.** Every gravity formalism needs a *topology* (what the field is) and a *closure condition* (that the field extends through all of space). In GR, tetrad gravity, bimetric gravity and scalar–tensor theory both are inputs. In GFD both follow from $2(d+1) = 2^d$.

**Topology.**
1. *Uniqueness.* $2(d+1) = 2^d$ only at $d = 3$ (table $d = 1..5$; for $d\ge4$ the exponential side wins). So $K = d+1 = 4$ and $D = 3$. Euler check: $4 - 6 + 4 = 2$.
2. *Parity partition.*
   - Cube vertices are labelled by 3-bit addresses ($0\to-1$, $1\to+1$).
   - Odd popcount $\{1,2,4,7\}$ = TetA; even $\{0,3,5,6\}$ = TetB.
   - Within a class every pair is at Hamming distance 2, so each class is a regular tetrahedron with edge $2\sqrt2$. The two are vertex-, edge- and face-disjoint (the stella octangula).
   - Antipodal pairs sum to $7 = 111_2$. The four body diagonals meet at the centre, the Field Origin.
   - $12$ edges $+ 1$ origin $= 13 = KD+1$.
3. *(3+1) from faces.*
   - Per tetrahedron, three faces look outward and one inward. The inward face is opposite $V_7$ for TetA and opposite $V_0$ for TetB; these are the two time faces, and the other six are spatial. That gives $1 + 3$ per tetrahedron.
   - Time fraction $2/8 = 1/4$, so spin $= \tfrac14\cdot2\hbar = \hbar/2$.
4. *Tetrad = tetrahedron.*
   - The half-space construction ($v_i$, TetA $\max v_i\le1$, TetB $\max(-v_i)\le1$) is as in VIII.
   - Reading the signs of $v_i$ as bits gives TetA's normals at corners $\{7,4,2,1\}$ and their negatives at $\{0,3,5,6\}$. The binary stellated octahedron and the tetrad's dual tetrahedra are one object.

**Closure → coupling.**
- Medial-triangle subdivision: each TetA face splits into 4 similar triangles, and TetB's vertex sits at the centre. $K\times K = 16$ channels, organised hierarchically (4 faces × 4 sub-channels).
- $\beta_0 = \beta_4 = 1$ (exchange), $\beta_1 = \beta_3 = 0$ (orientation parity at the Field Origin), $\beta_2 = K^2 = 16 = \dim C\ell_{1,3} = 2^{D+1}$.
- Ghost freedom is cited to VIII. It is also said to "guarantee" a Vainshtein mechanism that recovers GR in strong fields.

**Polynomial algebra [T].**
- $f(4,\pm1,0) = 21, 13, 17$. Closure range $21 - 13 = 8 = 2K = 2^D$.
- $17/13 = 1 + 1/(3 + 1/4) = [1; D, K]$.
- Self-reciprocal: $k^2f(1/k,s) = f(k,s)$. Roots $k = (-s\pm\sqrt{s^2-4})/2$ are complex for $|s|\le1$, with $|r| = 1$.
- $f(k,+1) = \Phi_3(k)$, root phase $2\pi/3$. $f(k,-1) = \Phi_6(k)$, phase $\pi/3$. $s = 0$ gives roots $\pm i$. Sweeping $s\in[-1,1]$ moves the roots through one 60° hexagonal sector (checked: phases 60°, 90°, 120°).
- $\Phi_3\Phi_6 = k^4 + k^2 + 1$; at $k = 4$, $21\times13 = 273 = 256 + 16 + 1$.

**Action.**
- Möbius map $s(x) = (x-1)/(x+1)$, so $f(x) = (21x+13)/(x+1)$ and $\mu = (f-13)/8 = x/(x+1)$. "The factor 8 cancels" is read as the vertex count $2^D$ removing itself.
- $F(y) = y - 2\sqrt y + 2\ln(1+\sqrt y)$, with $F(0) = 0$.
- $S = \int\sqrt{-g}\,[R/16\pi G - (a_0^2/8\pi G)F + \mathcal L_m]$.
- Prefactors $16, 8, 4 = K^2, 2K, K$ (channels, vertices, faces), each half the previous.
- Constants table: $4 = K$, $8 = 2^D$, $12 = KD$, $13 = KD+1$, $16 = K^2$, $17 = K^2+1$, $21 = K^2+K+1$, $64 = K^D$ ("vertex-pair state space").

**$N$-metric family.**
- $x(1-\mu)^N = \mu$. $N = 2$ at $x = 1$ gives $\mu^2 - 3\mu + 1 = 0$, so $\mu = (3-\sqrt5)/2 = 1/\varphi^2$.
- Closed form $\mu_2 = (\sqrt{1+4x}-1)/(\sqrt{1+4x}+1)$. Both laws go to $\mu\to x$ for $x\ll1$ and $\mu\to1$ for $x\gg1$, and differ only near $x\approx1$.
- The family is described as "a discrete hierarchy indexed by closure depth".

**π section [E].**
- *Octal walk.* Take the octal digits of π ($3.11037552\ldots$) and walk the cube's vertices by cumulative sum mod 8 from vertex 0.
  - Checked on 12,000 digits: vertices first appear at steps 1, 2, 4, 5, 7, 8, 11, 15.
  - The time face $\{1,2,4\}$ completes at step 5, as stated.
  - Visit frequencies are uniform to within ±5%.
- *BBP formula.* $\pi = \sum16^{-k}[4/(8k+1) - 2/(8k+4) - 1/(8k+5) - 1/(8k+6)]$.
  - It has period $8 = 2^D$, four active terms ($K$) and base $16 = K^2 = 2^K$.
  - Its coefficients $\{4,-2,-1,-1\}$ sum to 0 and have magnitudes equal to the binary place values.
  - $\operatorname{lcm}(3,4) = 12 = KD$.
- *What the evidence supports.* The paper calls this "an algebraic isomorphism, not a numerical coincidence". The evidence is a match of small integers. Uniform visits under a cumulative-sum walk are expected of any digit sequence that behaves like a normal one. The tag stays [E].

**Chain and open items.**
- Chain: $d = 3\to$ stellated octahedron $\to(3+1)\to$ tetrad $\to\{\beta_n\}\to\Phi_3/\Phi_6\to\mu\to S_{\rm SST}$.
- Open, as the paper states them: (i) quantum gravity, where the closure frequency is ~$10^{20}$ Hz; (ii) the closed-form EFT match from the locked Galileons to $\mu$, as in VIII.

**Notes against later work.**
- As in VIII, $s$ is continuous here; in later notation it is $\sigma(x)$.
- The displayed action has three terms, but the text cites a "1/4" coupling, which belongs to the $-\tfrac14e^{-2\Phi/c^2}FF$ term of the full SST (§3). The 16 : 8 : 4 reading assumes that term.
- IX's "$N$ metric sectors" reading of $N = 2$ is superseded by the bound-law reading (§4.6).

## Paper X — One Equation, Two Scales: Tully–Fisher Evolution and the Hubble Constant (`sst_two_scale_jcap`)

*JCAP-format letter. Data served from api.fielddynamics.org. Status: [O] comparisons, using [D]/[E] inputs.*

**Framing.**
- Starts from the spherical field equation $g_s = g_t^2/(a_0+g_t)$ with $a_0 = 1.2\times10^{-10}$. Limits: $g_s\approx g_t$ (Newton); $g_t\approx\sqrt{g_sa_0}$ (deep field).
- States the naming explicitly: the four-term action (with $-\tfrac14e^{-2\Phi/c^2}FF$) *is* the SST, and the quadratic is its spherical, static field equation. Prefactors $16, 8, 4 = K^2, 2^D, K$. $F$ is the AQUAL functional for the simple $\mu$; the difference from AQUAL is the derivation, not the mathematics.
- The forward solver $g_t = \tfrac12[g_s + \sqrt{g_s^2 + 4g_sa_0}]$ is used directly; $\mu$ appears in no computation.
- SPARC (175 galaxies): RMS "comparable to MOND and ΛCDM" with zero parameters (cited, not re-shown).

**Prediction 1: Tully–Fisher evolution.**
- In the deep field, $g_t = \sqrt{g_sa_0}$ with $g_t = v^2/r$ and $g_s = GM/r^2$ gives $v^4 = GMa_0$ exactly.
- $a_0 = (cH/2\pi)\sqrt{K/\pi}$, so $a_0$ grows with $H(z)$. Naively, at fixed $M$, $v(z)/v(0) = [H(z)/H_0]^{1/4}$.
- **Exponent 0.17.** The stated mechanism: velocities are inferred from photons that crossed the scalar field. The disformal coupling changes the photon metric and "partially screens" the evolution, with the aperture factor $\sqrt{K/\pi} = 1.128$ setting the share absorbed. The full derivation is cited to nelson2025a.
- Prediction $v(z)/v(0) = [H(z)/H_0]^{0.17}$ with $H(z) = H_0\sqrt{0.3(1+z)^3 + 0.7}$.
- Recomputed: 1.026, 1.057, 1.090, 1.101, 1.154, 1.203, 1.222, 1.289 at $z$ = 0.3, 0.6, 0.9, 1.0, 1.5, 2.0, 2.2, 3.0; residuals ≤ 0.38σ; $\chi^2 = 0.339$ over 8 points. All reproduce the table.
- SINS BX442 ($z = 2.18$, +27%): GFD gives 1.220.
- Falsifier: $z = 4$ gives 1.363 (ΛCDM 1.0, naive ¼-power 1.58). Any $z>3$ value below the band or above 1.4 falsifies.

**Prediction 2: $H_0$.**
- $H_0 = 2\pi a_0/(c\sqrt{K/\pi}) = 70.21$.
- Band ±6.2% from $(K/\pi)^{1/4} = 1.0623$, applied linearly: 65.9–74.6. It contains Planck 67.4, TRGB 69.8, GW170817 70.0, SH0ES 73.04, megamasers 73.9 and TDCOSMO 74.2.
- Tension reframed: Planck's ΛCDM fit ignores the sub-$a_0$ enhancement (pulls low); SH0ES's Newtonian calibration in Cepheid-host outskirts pulls high. Stated as "may", not computed.

**Arithmetic check (inputs).**
- 70.21 needs $a_0 = 1.225\times10^{-10}$ (the $16Gm_e/r_e^2$ value). The opening's $a_0 = 1.2\times10^{-10}$ gives 68.78.
- The "naive $cH/2\pi$" 78.9 uses $a_0 = 1.22\times10^{-10}$; with 1.225 it is 79.2.
- So the letter mixes three $a_0$ inputs. The relation itself is unaffected; only the quoted numbers carry different $a_0$ (see §7.4).

**Notes against other papers.**
- Paper II obtains the same 0.17 as $(1-1/\pi)/4$ from the tiling scaling $a_0\propto H^{1-1/\pi}$. Paper X attributes it to disformal photon-path screening governed by $\sqrt{K/\pi}$.
- These are two different stated mechanisms for one number. Neither letter shows the other's route, and Part I §6.4 now records both.

## Paper XI — Nuclear Shell Structure and Binding Energies from Tetrahedral Packing at $K = 4$

*Letter. Supplementary material: a pure-Python 82-isotope validation script and an interactive periodic table. Status: [E] throughout. The paper separates "what is established" from "what is not".*

**Setup.**
- *Two tetrahedra, four ways* (as VI/VII): Hassan–Rosen; BD-ghost cancellation by opposite orientations; the $SL(2,\mathbb C)$ double cover; Ashtekar's self-dual/anti-self-dual split.
- *A new packing route.* Twelve FCC neighbours (Kepler, Hales) give twelve boundary planes, which sort into four groups of three sharing a normal. That makes a tetrahedron, and the opposite normals make the inverted one.
- *Roles.* TetA is outward and carries the massless mode ("the unbound gravitational field: spacetime itself, the ocean"). TetB is the bounded interior and carries the massive mode. The Field Origin is the Hassan–Rosen interaction vertex.
- *Three structural types.*
  - $\det e\ne0$ (1).
  - The frame $e^a{}_\mu$ ($K$).
  - A $K\times K$ coupling matrix ($K^2$). The text writes this as "a connection ($\eta_{ab}$)", but $\eta_{ab}$ is the Minkowski metric; elsewhere this level is the frame-transition matrix $S$.

**Binding formula.**
- Packing $A$ fields into a host's TetB cavity crosses the full Field Origin ($N = 2$ faces), so the bound law applies: $x(1-\mu)^2 = \mu$, $\mu_2 = [(2x+1) - \sqrt{4x+1}]/(2x)$.
- Nuclear map $s_2 = 2\mu_2 - 1$ with compression $x = A^2$.
- $\mathrm{BE}/A = C[f(K, s_2(A^2)) - 17] = C[8\mu_2(A^2) - 4]$, with $C = m_ec^2\cdot17/K = 2.1717$ MeV. The fitted value is 2.16 (0.54%).
- The range $f\in[13,21]$ maps to $\pm4C$. Zero binding falls at $f = 17$, i.e. $\mu_2 = \tfrac12$, i.e. $x = 2$.
- Asymptotic ceiling $4C = 17\,m_ec^2 = 8.687$ MeV; the Fe-56 peak is 8.790.
- Recomputed from the formula:

  | Nucleus | Formula (MeV) | Observed (MeV) | Error |
  |---|---|---|---|
  | He-4 | 4.853 | 7.074 | −31% (the stated outlier, "$A = K$ resonance") |
  | C-12 | 7.30 | 7.68 | −5.0% |
  | O-16 | 7.64 | 7.98 | −4.3% |
  | Ca-40 | 8.26 | 8.55 | −3.4% |
  | Fe-56 | 8.38 | 8.79 | −4.7% |
  | Sn-120 | 8.54 | 8.51 | +0.4% |
  | Pb-208 | 8.60 | 7.87 | +9.4% |
  | Bi-209 | 8.60 | 7.85 | +9.6% |

- Stated statistics on 82 isotopes: $R^2 = 0.991$ on total BE; mean |error| in BE/A 3.9% (3.5% without He-4); 79% within 5%, 98% within 10%; Bethe–Weizsäcker needs five fitted parameters.
- **Shape of the curve.** $\mu_2(A^2)$ is monotonic, so the formula rises toward 8.687 and has no maximum. The Fe peak and the decline toward Pb are not reproduced: light and middle nuclei are under-predicted by about 4–5%, heavy ones over-predicted by 6–10%.
- The paper attributes the heavy-end excess to Coulomb repulsion (∝ $Z^2$). It also reports that subtracting a standard Coulomb term worsens the fit, and records the effect as not yet separated.
- Deuterium is outside the tested set (the formula gives 1.90 vs 1.11).

**Magic numbers.**
- $T(n) = n(n+1)(n+2)/6$; gate $G(n) = 0$ for $n<K$, $(n-1)n/2$ for $n\ge K$ (Sierpiński: the central sub-triangle is removed at each level); $P = T - G$.
- $M(n) = 2P(n)$, where the 2 is two time-face orientations (spin).
- At $K = 4$: $M = 2, 8, 20, 28, 50, 82, 126, 184, 258$. Shell sizes are $S = 2, 6, 12, 8, 22, 32, 44, 58, 74$.
- $S_3 = 12 > S_4 = 8$ is presented as the spin–orbit inversion, "a theorem": below $K$ the sizes are $n(n+1)$, and at $n = K$ the size is $2K$; $DK = 12 > 2K = 8$ because $D>2$.
- **Uniqueness, recomputed for $K = 2..10$.** Only $K = 4$ contains all seven magic numbers.
  - The paper's two examples are swapped. $K = 3$ gives 2, 8, **14**, 28, …, so it misses **20**. $K = 5$ gives 2, 8, 20, **40**, 50, …, so it misses **28**.
  - $K$ enters only as the onset of gate exclusion. The gate $(n-1)n/2$ itself does not depend on $K$, so every $K\le n$ gives the same $M(n)$.

**Stability ceiling.**
- Nesting depth $K$ (3 + 1); address space $K^K = 256$.
- $M(8) = 184$ is allowed, which the paper links to the island of stability ($Z\approx114$, $N = 126$–184).
- $M(9) = 258$ exceeds 256 by 2 (the time faces).
- Bi-209 uses 81.6% of the space. Fm-258 ($A = M(9)$) fissions spontaneously, $t_{1/2}\approx370\ \mu$s.

**One polynomial, two scales.**
- $N$ counts the faces on the coupling path. $N = 1$ (galaxies): $s_1 = (x-1)/(x+1)$, $\mu_1 = x/(x+1)$, AQUAL $F$. $N = 2$ (nuclei): $f = 13 + 8\mu_2(A^2)$.
- This is the reading Part I uses: one-directional law for galaxies, bound law for nuclei. Here it is motivated by face crossings. research/aqual derives it instead as the exchange image of the source form.

**Small errata.**
- The text gives the locked bimetric set as $\{1, 0, K, 0, 1\}$; elsewhere (and correctly, $\beta_2 = K^2$) it is $\{1,0,16,0,1\}$.
- The abstract says "83 stable elements" but tests 82 isotopes (He-4 to Bi-209).

## Paper XII — Dual Tetrad Covariance: the GFD Scalar–Tensor Action and the Hassan–Rosen Potential as Two Projections of One Geometry (v9)

*REVTeX letter. Supplementary scripts: `gfd_structured_derivation.py` (the lock: theorems, axioms, counterexamples, impedance) and `gfd_bimetric_concordance.py` (six checks, integer scan, plots). Status: three [T] theorems, three axioms stated as postulates, and [O] concordance.*

**The GFD side.**
- The four-term action, with prefactors $16\pi G = K^2\pi G_{\rm eff}$, $8\pi G = 2^D\pi G_{\rm eff}$ and $1/4 = 1/K$.
- $\mu(\sqrt y) = F'(y)$. In the spherical, static limit the action gives $g_s = g_t^2/(a_0+g_t)$, read both ways, with decode $M_{\rm dec} = rv^4/[G(a_0r + v^2)]$.
- Observational status as listed:
  - 179 SPARC rotation curves via the decode formula (X says 175; RAR uses 164 at $Q\le2$).
  - CMB $E = 6.44$ vs $\Omega_m/\Omega_b = 6.36\pm0.10$ (0.8σ).
  - TF evolution, $\chi^2/{\rm dof} = 0.04$.
  - $H_0 = 70.21$ ± 6.2%.

**The Hassan–Rosen side.**
- $S = M_g^2\!\int\!\sqrt{-g}R_g + M_f^2\!\int\!\sqrt{-f}R_f + m^2M_g^2\!\int\!\sqrt{-g}\sum\beta_ne_n(S)$, with $S = \sqrt{g^{-1}f}$.
- Högås & Mörtsell (2025; DESI DR2 + Planck + ACT + SNe; seven-parameter MCMC): $\theta = 6.1^{+1.7}_{-2.1}$°, $H_0 = 69.0\pm0.4$.

**Dictionary.** TetA ↔ $e$, TetB ↔ $\tilde e$, stellated octahedron ↔ interaction domain, central octahedron ↔ proportional background, Field Origin ↔ $S = I$, and the $f$-vector $(8,12,8)$, 28 elements ↔ "five $\beta_n$ to be determined".

**The lock, with theorems kept separate from axioms.**
- **T1 (exchange identity).** $e_n(S^{-1}) = e_{4-n}(S)$ for $\det S = 1$ (Cayley–Hamilton; in general divide by $\det S$).
- **T2 (pairing).** If $V(S) = V(S^{-1})$ on the unimodular sector, then $\beta_0 = \beta_4$ and $\beta_1 = \beta_3$.
- **T3 (Hessian rank).** The Hessian of $e_2$ over the 16 entries at $S = I$, $\partial^2e_2/\partial S_{ij}\partial S_{kl} = \delta_{ij}\delta_{kl} - \delta_{il}\delta_{jk}$, has full rank 16 with spectrum $+3\,(\times1)$, $+1\,(\times6)$, $-1\,(\times9)$. Recomputed: confirmed. The form is indefinite but has no null directions.
- **A1 (symmetric lock).** A balanced closure at the origin excludes the pair $(e_1, e_3)$, which swaps under $S\to S^{-1}$ instead of mapping to itself. So $\beta_1 = \beta_3 = 0$. The paper says plainly that generic ghost-free theories allow $\beta_1 = \beta_3\ne0$, and that A1 selects a subclass.
- **A2 (normalisation).** $\beta_0 = K^0 = 1$, hence $\beta_4 = 1$.
- **A3 (quadratic completeness).** $\beta_2$ equals the Hessian multiplicity, 16. Three routes converge: variational (T3), combinatorial ($4\times4$ medial channels) and algebraic ($\dim C\ell(1,3)$). T3 fixes the rank. Setting the weight equal to the rank is the axiom.
- Counterexamples: drop A1 → $\{a,b,c,b,a\}$; drop A2 → $\{a,0,16,0,a\}$; drop A3 → $\{1,0,c,0,1\}$.
- Compared with VIII, the odd terms here come from an axiom (A1), not from orientation parity $\lambda\to-\lambda$. XII is the more careful statement.

**Six concordance checks.**
1. *Expansion.* The Bianchi bracket $\beta_1 + 2\beta_2y + \beta_3y^2 = 32y\ne0$ forces the finite branch, which is viable at $\theta = 6.1°$.
2. *BBN.* $\Delta N_{\rm eff} = 0.07 < 0.5$.
3. *CMB.* $E = 6.44$ vs $6.36\pm0.10$, stated as concordance with $\mu$, not a result of the $\beta_n$.
4. and 5. *Screening and Galileons.* $\beta_1 = \beta_3 = 0$ "kills the cubic and quintic Galileons"; the quartic survives with $c_3 = \tfrac32\beta_2 = 24$. This is stated, not derived, in the letter.
6. *Mixing angle.* $\tan\theta = D/(V+E+F) = 3/28$, $\theta = 6.1155°$ (recomputed), $0.016°$ from H–M's central value.
- *Integer scan, $\beta_2 = 1..30$.* Every value is viable at $\theta = 6.1°$, and the data cannot tell 15, 16 and 17 apart. The paper states that the selection of 16 is structural (A3), not observational.

**Term-by-term map.**

| GFD | Hassan–Rosen | Origin |
|---|---|---|
| $16\pi G$ | $\beta_2 = 16$ | $K^2$ |
| $8\pi G$ | scalar sector | $2^D$ |
| $1/4$ | $K$ faces | — |
| $\mu = x/(x+1)$ | $V = e_0 + 16e_2 + e_4$ | partition ↔ potential |
| $\tan\theta = 3/28$ | $\theta$ | — |
| $\Delta\mu = 2/17$ | boundary overhead | — |

- The scalar sector: $F$'s three terms ↔ $K^2$, $sK$, $K^0$. This is said to be "the same scalar content" as the Galileon sector with $c_3 = 24$; no calculation is given.
- **Topological coupling impedance.** $\Delta\mu = (\beta_0+\beta_4)/f(0) = 2/17 = 0.11765$, compared with $\tfrac12 - 1/\varphi^2 = 0.11803$, a 0.33% gap (recomputed). The $1/\varphi^2$ is attributed here to "quartic Galileon screening in the decoupling limit". Elsewhere it is $\mu_b(1)$ of the bound law.
- The text says the impedance sits at the vertex inside the vortex, and the exterior decode integrates over it.

**Notes against other papers.**
- *CMB numbers.* XII's 6.44 differs from Paper II's 6.46 (Part I §7.2). XII's comparator $6.36\pm0.10$ differs from Paper II's target 6.40 ($1.185/0.185$); Planck 2018 central values give 6.39–6.40.
- *Open matching.* XII claims the two actions "produce the same field content". The explicit match from Galileons to $\mu$ that VIII and IX list as open is still not computed here; the scalar-sector row is asserted.
