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

The metric is a Gram matrix of the tetrad, $`g_{\mu\nu} = \eta_{ab} e^a{}_\mu e^b{}_\nu`$. The equation is even in the spatial frame, so it has two parity-related roots. Drawn in space, one root is a regular tetrahedron (TetA) and the other its inversion (TetB); together they are the stellated octahedron inscribed in the cube, sharing a centre, the Field Origin. Counting on this object gives one polynomial, $f(K,s) = 1 + sK + K^2$, with values 21, 17, 13 at $K = 4$. The exchange symmetry between the two roots forces the interpolating function $\mu(x) = x/(x+1)$. Integrating it gives the AQUAL kinetic function $F(y)$, and with it a covariant action whose prefactors are $K^2$, $2^D$, $K$. In the spherical, static limit the action gives the relation tested on SPARC. General relativity is the $\mu = 1$ (all-TetA) case: its torsion-free condition keeps 40 of 64 connection components and discards the 24 that carry TetB.

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

(Checked by LP over all 16 patterns.) As a region, TetA $=\{\max v_i\le1\}$ has *outward* face normals $\propto(+++),(+--),(-+-),(--+)$ and therefore vertices at the opposite corners $(---),(-++),(+-+),(++-)$. Papers IX, GRAM and C instead name TetA by the vertex set $\{(+++),(+--),(-+-),(--+)\}$ ($xyz = +1$); that matches L1's region only if their "face normals" are read as *inward* normals (Paper C calls the same four vectors both TetA's vertices and its face normals). Same pair, flipped label. They interpenetrate as a stellated octahedron; the boundary splits into $4$ faces $\times$ $4$ sub-regions $= 16$ channels. No second frame is assumed: TetB is the second bounded region of a single tetrad.

**Scheme version (P-two-regions, 39 checks).** $g = e^T\eta e$ forces $(\det e)^2 = \det g/\det\eta$, so the solution scheme has exactly two components, one per root of $\det e$. Spatial parity maps one to the other (three is odd) and carries TetA onto TetB. The metric sees only $(\det e)^2$; restricting to $SO^+(1,3)$ keeps one root and discards the other.

### 2.3 The forced frame [T] (P-forced, GRAM, 27 + 32 checks)

Legs with the pattern of $\eta$ (every pair alike, equal magnitudes, distinct; the sign of $\eta_{00}$ is set aside, since a squared length cannot be negative — keeping it instead admits the observer's projection, three orthonormal legs and a null time leg) are forced to a regular tetrahedron, unique up to $O(3)$, and only in three dimensions. Explicitly,

$$M_1 = \begin{pmatrix} +1&+1&-1&-1\\ +1&-1&+1&-1\\ +1&-1&-1&+1\end{pmatrix},\quad M_2 = -M_1,\quad G_{M_1M_1} = M_1^TM_1 = \begin{pmatrix}3&-1&-1&-1\\-1&3&-1&-1\\-1&-1&3&-1\\-1&-1&-1&3\end{pmatrix}.$$

Gram products: $G_{M_2M_2} = G_{M_1M_1}$ (root-blind self-coupling), $G_{M_1M_2} = -G_{M_1M_1}$ (sign-reversing cross-coupling); $G_{IJ} = D$ on the diagonal, $-1$ off it. Columns of $M_1$ are a tetrahedron, of $M_2$ its inverse, of $[M_1\ M_2]$ the stellated octahedron.

### 2.4 Hadamard kernel [T] (C, P-hadamard, 25 checks)

A regular simplex on cube corners $\{\pm1\}^D$, bordered by a row of ones, is a Hadamard matrix. The Walsh–Hadamard matrix of the 3-cube factorises $H_8 = H_2 \otimes H_4$ (parity $\otimes$ frame). The three non-constant rows of $H_4$ are the stellated octahedron's axes and the tetrad's face normals. Parity classes (as face-normal sign patterns, cf. §2.2): TetA $\{(+++),(+--),(-+-),(--+)\}$, TetB $\{(---),(-++),(+-+),(++-)\}$.

### 2.5 The coupling polynomial [D] (VII, VIII, IX, A)

$$f(K,s) = 1 + sK + K^2,\qquad f(4,+1) = 21\ (\text{TetA}),\quad f(4,0) = 17\ (\text{Field Origin}),\quad f(4,-1) = 13\ (\text{TetB}).$$

Three levels: existence (1), the $K$ faces, the $K^2$ face-pair channels. Identities used throughout:

- $f(K,+1) = (K^3-1)/(K-1) = \Phi_3(K)$; $f(K,-1) = \Phi_6(K)$ (cyclotomic polynomials).
- $(f(+1) + f(-1))/2 = 17 = f(0)$; $f(+1) - f(-1) = 2K = 8$.
- $17/13 = (K^2+1)/(KD+1) = [1; 3, 4]$ as a continued fraction; $13 = 12$ edges $+ 1$ origin $= KD + 1$.

**As a trace [T] (A; research/aqual §13).** With $V = \mathbb R^4$ and $\tau$ the swap on $V\otimes V$ ($\mathrm{Tr}1 = 16$, $\mathrm{Tr}\tau = 4$),

$$f(K,s) = 1 + \mathrm{Tr}_{V\otimes V}(1 + s\tau),$$

the parity-weighted trace of the sector space $\Lambda^K V \oplus V \oplus (V\otimes V)$. The swap's eigenspaces are the symmetric 10 and antisymmetric 6, the same split GR meets in the tetrad (10 metric + 6 local Lorentz) and in each connection slice (10 Christoffel + 6 torsion). GR keeps the symmetric sector both times, which is why 13, 17, 21 never appear there: the parameter $s$ that weights the two sectors is fixed at one end.

---

## 3. The covariant action (the SST)

$$\boxed{S = \int d^4x\,\sqrt{-g}\left[\frac{R}{16\pi G} - \frac{a_0^2}{8\pi G}\,F(y) - \frac14 e^{-2\Phi/c^2}F_{\mu\nu}F^{\mu\nu} + \mathcal L_{\rm matter}\right],\qquad y = \frac{|\nabla\Phi|^2}{a_0^2}}$$

- **Prefactors [D]** (L3 supplement): $16 = K^2$, $8 = 2^D$, $4 = K$, a geometric sequence of ratio 2.
- **Lensing and $\gamma$ (L3 supplement §3):** the claim is $\gamma = 1$ at all accelerations, giving full light bending $\theta = (1+\gamma)\,2GM/(rc^2) = 4GM/(rc^2)$, because one potential $\Phi$ enters both $g_{00}$ and $g_{ij}$ ("the modification lives inside the connection, not beside it"), whereas AQUAL-in-GR with a separate scalar gets $\gamma = \mu(x)$. The single-potential weak-field metric is stated as an ansatz; the metric field equations of the action (including the scalar's stress–energy) are not solved in the note.
- **Electromagnetic term:** $-\tfrac14e^{-2\Phi/c^2}F_{\mu\nu}F^{\mu\nu}$. The supplement assigns it no lensing role (null rays are unaffected) and a cosmological one (a redshift dependence in EM scaling relations). **Unaddressed constraint:** with $\Phi$ the Newtonian potential, this term is a dilaton-type coupling, $\alpha_{\rm eff} = \alpha\,e^{2\Phi/c^2}$, i.e. $\delta\alpha/\alpha = k_\alpha\,\delta U/c^2$ with $|k_\alpha| = 2$. Clock and spectroscopy tests of $\alpha$'s dependence on the Sun's potential (annual $\delta U/c^2 \approx 3\times10^{-10}$) bound $|k_\alpha|$ at roughly $10^{-6}$–$10^{-7}$. None of the papers discusses this.
- **Weak field:** $g_{00} = -(1+2\Phi/c^2)$, $g_{ij} = (1-2\Phi/c^2)\delta_{ij}$; GW speed equals $c$.
- **Split (what GFD does *not* do):** the L3 supplement describes the scalar-tensor embedding as $\nabla^2\Phi_N = 4\pi G\rho$ (40 components) plus a scalar supplement $\nabla\cdot[(\mu - 1)\nabla\Phi] = 0$ carrying its own stress–energy, and attributes the $\gamma = \mu$ lensing deficit to that decomposition; GFD keeps the single equation $\nabla\cdot[\mu\nabla\Phi] = 4\pi G\rho$.
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

Every premise is shown necessary. The capacity ratio between the two sectors equals the dimensionless acceleration. The P-exchange version derives the exchange rather than assuming it: premises are (E) $\mu(0)=0$, (X) closure of the set of partition states under parity, and (A) a polynomial relation of degree one in each variable; a field-theory lemma (Gauss) makes it bilinear, and $x\to1/x$ with fixed point $a_0$ then follows. Premise (A) is where the one-directional law is chosen over the bound law: dropping it admits $x^n(1-\mu)^m = \mu$, and $(n,m) = (1,2)$ is the bound law. Without (A), any increasing $\mu$ from 0 to 1 satisfies (E) and (X).

### 4.2 Equilibrium (detailed balance) route [D] (I, CL route 2)

Single channel with fill $\varepsilon$: activation $W_+ = \kappa_+x(1-\varepsilon)$, relaxation $W_- = \kappa_-\varepsilon$. At equilibrium $Kx(1-\varepsilon) = \varepsilon$, so $\varepsilon = Kx/(1+Kx)$; absorbing $K$ into $a_0$ gives $\mu = x/(1+x)$. The fixed point is unique and globally attracting ($d\dot\varepsilon/d\varepsilon = -\kappa(x+1) < 0$). Paper I's postulates: lossless (no wakes, drag, hysteresis), locally evaluable, single channel; within this "MSC" class, the deep-MOND limit forces exponent $n = 1$.

### 4.3 Normalised capacity route [D] (VIII, IX)

$$f(4,\sigma(x)) = 17 + 4\sigma(x) = \frac{21x+13}{x+1},\qquad \mu(x) = \frac{f - 13}{21 - 13} = \frac18\cdot\frac{8x}{x+1} = \frac{x}{x+1}.$$

### 4.4 Algebraic route [T] (A)

(Paper A states the limit itself: $x^n/(1+x^n)$ satisfies the same exchange for every $n$; $n = 1$ is the fractional-linear member, i.e. the choice of $x$ as the odds.) The swap $\mathrm{Sym}^2V \leftrightarrow \Lambda^2V$ is represented by $x \mapsto x^{-1}$; within fractional-linear maps with the pure-sector endpoints, the unique solution is $x/(1+x)$, and the Cayley coordinate $(x-1)/(x+1)$ is $\sigma(x)$.

### 4.5 Properties

- Logistic: $x\,d\mu/dx = \mu(1-\mu)$; rate peaks at $1/4$ at $x = 1$.
- $\sigma(x) = \tanh(\tfrac12\ln x)$, and $\sigma(x_1x_2) = (\sigma_1+\sigma_2)/(1+\sigma_1\sigma_2)$ — shares compose like rapidities; odds multiply.
- Mean capacity: $\mu(x)+\mu(1/x) = 1 \Rightarrow \langle f\rangle = 17$ over any window symmetric in $\ln x$.
- Swap-operator form: $1 + \sigma\tau = 2[\mu P_{\rm sym} + (1-\mu)P_{\rm anti}]$, with $x = \lambda_{\rm sym}/\lambda_{\rm anti}$ and $1+\sigma\tau = \mathrm{sech}\theta\,e^{\theta\tau}$, $\theta = \tfrac12\ln x$. GR sits at $\mu = 1$.
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

$$\frac{g_t}{a_0} = \mathrm{csch}^2\frac\psi2,\quad \mu = \mathrm{sech}^2\frac\psi2,\quad v^2 = \sqrt{GMa_0}\coth\frac\psi2,\quad \Phi + v^2 = \sqrt{GMa_0}\,\psi.$$

Unit source field ($g_s = a_0$) at $r = r_M$ where $\mu = 1/\varphi$; unit total field ($x = 1$) at $r = \sqrt2\,r_M$ where $\psi/2 = \ln(1+\sqrt2)$.

---

## 5. The connection: 64 = 40 + 24

### 5.1 Counting [T] (L2, L3, GRAM, 40/24 proof)

Per slice $\lambda$, $`\Gamma^\lambda{}_{\mu\nu}`$ has $K^2 = 16$ entries: $(K^2+K)/2 = 10$ symmetric, $(K^2-K)/2 = 6$ antisymmetric. Over $K$ slices:

$$\text{Christoffel } K\frac{K(K+1)}2 = 40,\qquad \text{torsion } K\frac{K(K-1)}2 = 24.$$

In polynomial form, per slice:

$$\text{kept} = \frac{f(K,+1)-1}{2} = 10,\qquad \text{discarded} = \frac{f(K,-1)-1}{2} = 6,$$

with difference $K$ and sum $K^2$. (Counting note: the $K$ that separates 10 from 6 is the $K$ diagonal entries, which are all kept; the "$-1$" removed before halving is a single unit, although the L3 proof note describes it as standing for the diagonal. The identity $(f(K,\pm1)-1)/2 = (K^2\pm K)/2$ is exact either way.) GRAM writes the index grid per slice as $6$ upper $+ 4$ diagonal $+ 6$ lower, so $24 + 16 + 24 = 64$, the torsion-free projection retaining $16 + 24 = 40$. The split is defined on the index grid, not on cube-corner pairs.

### 5.2 The torsion lemma [T] (L2)

A torsion-free connection cannot distinguish TetA from TetB; the torsion sector is the necessary carrier of the two-chamber distinction. (The metric is bilinear in $e$, so parity $e^i\to-e^i$ leaves it fixed, and the Levi-Civita connection is built from the metric alone; this holds for any $K$.) Separately, the torsion count factorises as $K\cdot K(K-1)/2 = D\times2K$ (with $D = K-1$) only at $K = 4$ ($K/2 = 2$): $24 = 3\times8$, spatial dimension × coupling range.

### 5.3 Torsion is the regular representation of $S_4$ [T] (B, P-torsion, 36 checks)

At $K = 4$, $`V\otimes\Lambda^2V^*`$ (dimension $K^2(K-1)/2 = 24 = 4!$) carries the regular representation of $S_4$ acting on the four legs. The sign representation, the unique scalar parity detector, appears once in torsion and zero times in the Christoffel sector. Only $K = 2$ and $K = 4$ allow this. P-torsion gives the explicit generator $\xi = t_{0;01} + t_{0;23}$ (its 24 permutation images are a basis), two orbits of 12 (incident / non-incident), the sign irrep spanned by $\sum_d\varepsilon_{abcd}$, and, with indices lowered by $|\eta| = I$, vector ⊂ incident, axial ⊂ non-incident, tensor = $8 + 8$. Scope: the sign irrep detects odd *permutations of the legs*; spatial parity $\mathrm{diag}(1,-1,-1,-1)$ is not a leg permutation and is not described by these theorems, so the link to TetA/TetB root-blindness is by analogy (orientation character), not identity.

### 5.4 Einstein's equation as the TetA partition [D] (L3)

The torsion-free condition keeps the $s = +1$ projection and discards the $s = -1$ projection. GR is the GFD field equation at $\mu = 1$. Restoring the 24 components gives the full 64-component connection, which $\mu(x)$ partitions spatially; the gap opened by releasing $\mu$ is the TetB share, conventionally attributed to dark matter. In a galaxy, the TetA share dominates the core and the TetB share the rim (the deep field), with the handover on the ring $x = 1$. TetB itself is the throat interior at the centre.

**Local systems are TetA only** (as now stated in `EINSTEIN_TETA_PARTITION.md`). In a solar system, a binary or a star cluster, gravity between the bodies is the TetA connection, i.e. GR, exactly. Every body has its own TetB, but it is enclosed within the body: outside, gravity reports only the enclosed total (Gauss's law), so it is part of the body's measured GM and cannot be separated from TetA by any orbit. The TetB share is not a property of each mass. It belongs to the net field of the host galaxy, which is uniform across a bound system (to about $10^{-12}$ over the solar system) and cancels in the bodies' common free fall: the mountain stream, whose current presses on neighbouring rocks alike and appears only in the slope of the whole stream. A bound system enters the galaxy's net field as a single element, its total mass and position (the "pointer" picture). So $x$ is the galaxy's net field over $a_0$, and $\mu(x)$ is never applied to a star's own field. Applying it per mass would leave a TetB tail $1-\mu \approx 1/x$ around every star: a constant extra pull $\approx a_0$ at every planet and an external-field quadrupole $Q_2 \approx 4\times10^{-26}$ s⁻², both excluded (perihelia; Cassini, $Q_2 = (3\pm3)\times10^{-27}$ s⁻²); see `research/bimetric-projection/` Part 3. The surviving galactic tide at Saturn is about $10^{-18}$ m/s².

**In plain terms** (the summary at the top of `EINSTEIN_TETA_PARTITION.md`):

> **A galaxy is a vortex.** Picture water swirling down a drain. The visible stars are like leaves floating on the surface: they ride the flow and trace its shape, but they don't set its strength. What sets the strength is what's happening at the drain below.
>
> In GFD, gravity has two parts. **TetA** is the ordinary gravity of the matter you can see, the part Newton and Einstein describe. **TetB** is the flow through the galaxy's throat, the drain. Together they make the galaxy's **net field**, the gravity the stars actually feel.
>
> As in any vortex, the drain can work with the flow or against it. When TetB spins with the galaxy, it **drives** the rotation, and stars move faster than the visible matter alone would explain. When it spins against it, it **brakes** the rotation, and stars move slower. When it's quiet, the visible matter accounts for everything. The decoding-mass letter shows all three: M33 (drive), CamB (brake), and the Milky Way and NGC 3198 (close to quiet).
>
> **So why don't we see TetB in the solar system?** Every object has a TetB, the Sun included, but an object's TetB stays inside it. From outside, gravity can't tell what's going on inside a body; it only reports the total. So the Sun's TetB is already counted in the Sun's measured gravity, and the planets just feel "the Sun".
>
> Meanwhile, the whole solar system sits inside the galaxy's vortex like a pebble in a stream. Zoom in on the pebble and the water around it looks level: everything nearby is carried along together, so nothing changes between the planets. Zoom out to the whole galaxy and you see the stream running steeply downhill. The galaxy's TetB is real, but across something as small as the solar system it is perfectly flat.
>
> **That's why Einstein's gravity works so well locally and why galaxies look strange.** Up close, each body's TetB is hidden inside it and the galaxy's TetB is level. Only at the scale of a whole galaxy, where stars move through the vortex's TetB rather than past it, does the drive or brake show up.

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
- Bidirectional: observed $H$ recovers $m_e$ to 0.10% (IV). The companion PDF claims 0.01%, but its own eq. 5 at $H = 70$ gives −0.10%; its forward eq. pairs $a_0 = 1.225\times10^{-10}$ with 69.92, which belongs to $a_0 = 1.220\times10^{-10}$.
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

Hassan–Rosen: $S = M_g^2\!\int\!\sqrt{-g}R_g + M_f^2\!\int\!\sqrt{-f}R_f + m^2M_g^2\!\int\!\sqrt{-g}\sum_{n=0}^4\beta_ne_n(S)$, $S = \sqrt{g^{-1}f}$ (vielbein form $`S^a{}_b = (e^{-1}\tilde e)^a{}_b`$), five free $\beta_n$.

GFD locks them:

$$\{\beta_0,\beta_1,\beta_2,\beta_3,\beta_4\} = \{1, 0, 16, 0, 1\},\qquad V(S) = e_0 + 16\,e_2 + e_4.$$

- $\beta_2 = 16 = \dim C\ell_{1,3} = \dim\mathrm{End}(\mathbb R^{1,3}) = K^2$.
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

Shell ceilings $\mathrm{CEIL} = B_{\rm Zn} + B_{\rm bdy} - \mu_b(2)[B_{\rm Zn} - B_{\rm bdy}]$ with $\mu_b(2) = 1/2$; inverted curves $B_n^{\rm inv}(A) = \mathrm{CEIL}_n - B_{\rm local}(A - A_n)$; $B/A = \min(B_1, B_1^{\rm inv}, B_2^{\rm inv}, B_3^{\rm inv})$. Results: the seven magic numbers including the $20\to28$ gap without spin–orbit coupling, and $B/A$ from He to Pb at MAE ≈ 95 keV. One energy scale is calibrated (Zn-64, entered as 8.756 MeV; AME2020 gives 8.736), and the reflect-at-sector/min envelope is a construction, not derived from the action. XIII ends stability at Pb-208 (16 into the gate sector past 192); XI ends it at $K^K = 256$ / Bi-209.

---

## 11. Other threads (shorter)

- **Paper V:** why four recurs across ADM, tetrads, LQG, Regge, LIGO — the simplex theorem; vocabulary bridge to the Field Chamber and its four Coupling Ports.
- **Paper IX:** the derivation chain $d = 3 \to$ stellated octahedron $\to (3+1) \to$ tetrad $\to \{\beta_n\} \to \Phi_3/\Phi_6 \to \mu \to S$; the $(3+1)$ split from face classification (2 TIME + 6 spatial faces). Also an isomorphism between the base-8 expansion of π and the topology **[E]**.
- **ESS:** primer for relativists: tetrads and non-degeneracy ($\det g = -(\det e)^2 \neq 0$) → four active channels → field closure → constitutive law → action → the inverse pipeline.
- **Exploratory programmes** (not part of the physics claims): the I Ching trigrams as cube vertices and the BBP π formula selected by the TIME axis; the Great Pyramid's King's Chamber at $`z^*/h = 1 - 1/\sqrt2`$; the oscillator Ising solver.

---

## 12. Open problems and issues

### 12.0 Stated in the README

1. The RAR cannot separate GFD from MOND's simple function; discriminating tests are TF evolution, torsion, constants.
2. $a_0$ is empirical in the galactic test. Its link to $H$ ($a_0 = cH_{\rm flat}/2\pi$, $H_{\rm meas} = H_{\rm flat}/\sqrt{k/\pi}$) rests on the frame factor $\sqrt{k/\pi}$, which Paper IV calls a dimensional argument.
3. $H_0$ is quoted as 69.92 and 70.21 (the same formula with the empirical and the electron-derived $a_0$) and 70.29 (70.21 with the one-loop correction); the ±6.2% cage does not discriminate Planck from SH0ES.
4. Clusters and the Bullet Cluster: qualitative only (VII); no lensing reconstruction.
5. CMB: one enhancement factor, no full power spectrum.
6. $\mathcal L_{\rm matter}$ unspecified.
7. Constants: numerical routes, subject to look-elsewhere effects.
8. No peer-reviewed publication yet.

### 12.1 Found in the full paper-by-paper reading (Part II)

*Physics gaps, stated or implied by the papers themselves:*

9. **UV → IR bridge** (now computed: [`research/bimetric-projection/`](research/bimetric-projection/) — the locked decoupling limit has d = (49, 32, 16, 0), screening cubic $v(v^2+6v+6) = 2Q$, response a function of $M/r^3$ only and bounded by $g_{\rm tot}/g_N < 1.71$; it cannot give $\mu(x)$). No paper computes the match between the locked bimetric potential and the SST. In that match, the Galileon coefficients $c_k(\beta)$ give a quasi-static relation, and that relation would have to equal $\mu = x/(x+1)$. VIII and IX call this the open "checkable matching problem". XII and TF assert the equivalence without computing it.
10. **$\gamma = 1$.** This rests on a posited single-potential weak-field metric (L3 supplement §3). The metric field equations, which include the stress–energy of the $F(y)$ sector, are not solved. ESS gives the opposite account, in which the EM term supplies the lensing.
11. **EM coupling and $\alpha$.** With $\Phi$ the Newtonian potential, $-\tfrac14e^{-2\Phi/c^2}F^2$ implies $\alpha_{\rm eff}\propto e^{2\Phi/c^2}$, i.e. $|k_\alpha| = 2$. Laboratory bounds are about $10^{-6}$–$10^{-7}$. This is not discussed in any paper (§3).
12. **Graviton mass.** It is not predicted. The $\beta_n$ fix ratios; the overall $m^2$ (and $M_f/M_g$, set via $\theta$) remain (TF note).
13. **The exponent 0.17.** It has two stated mechanisms: $(1-1/\pi)/4$ from the tiling scaling (II), and disformal photon-path screening (X, TF). Neither paper shows the other's route.
14. **Nuclei.**
    - XI's single formula rises monotonically to 8.687 MeV, so it has no Fe peak and overshoots Pb/Bi by 9–10%.
    - XIII calibrates on Zn-64, entered as 8.756 MeV where AME2020 gives 8.736.
    - Its reflect-and-min envelope is constructed, not derived.
    - XI ends stability at $K^K = 256$ (Bi-209); XIII ends it at 192 + 16 (Pb-208).
15. **The decode deficit.** The sign of $\Delta M_{\rm eff}$ ("drives" vs "brakes") is not pinned down (DEC, ESS).

*Errata and internal inconsistencies (arithmetic checked here):*

16. XI: the uniqueness counterexamples are swapped. $K = 3$ misses 20, not 28; $K = 5$ misses 28, not 20. XI also gives the locked set as $\{1,0,K,0,1\}$ where it should be $K^2$.
17. Companion PDF: it pairs $a_0 = 1.225\times10^{-10}$ with $H = 69.92$, which needs 1.220. Its "0.01%" electron-mass round trip is −0.10% from its own eq. 5.
18. Paper X: it uses three $a_0$ values (1.2, 1.22, 1.225) for 68.8 / 78.9 / 70.21.
19. FY note: $+\rho\Phi$ in $\mathcal L$ gives the wrong sign of Poisson, and the abstract assigns the deep-field scaling to the log term alone.
20. TetA label: in L1, P-two-regions and Letter 2, TetA is the region with outward normals $(+++),\ldots$. In IX, GRAM and C, TetA is the solid with vertices $(+++),\ldots$. The pair is the same and the label is flipped (§2.2).
21. Paper C: its symmetry axes pass through cube face centres, not "opposite edge-midpoints of the cube".
22. RAR: the cached CSV has 163 galaxy names, not 164. XII cites 179 SPARC galaxies and X cites 175.
23. CMB factor: 6.46 (II) vs 6.44 (XII); comparator 6.40 (II) vs $6.36\pm0.10$ (XII).
24. The 40/24 proof note reads the subtracted "1" as the diagonal. There are $K$ diagonal entries, and they are the $+K$ that separates 10 from 6.
25. **Ghost citation (VII, VIII).** VII cites Alexander, Marcianò & Smolin, PRD 89, 065017 (2014) for "a single orientation produces a scalar ghost; two opposite chambers cancel it", and VIII for "BD-ghost cancellation by opposite orientations". The paper's abstract and introduction say the reverse. Its parity-symmetric bimetric phase (massless graviton + massive spin-2 + scalar ghost, following Speziale) is unstable, and its parity-broken chiral phase is stable. It does not discuss tetrad orientation. A reading consistent with GFD: the closed frame is parity-broken, because the chiral holonomy (L3 supplement) distinguishes the two senses of circulation, 135° versus 155.8° ([`research/bimond-gfd/10_chiral_holonomy_check.py`](research/bimond-gfd/10_chiral_holonomy_check.py)). That is an alignment of descriptions, not a stability proof. Hassan–Rosen's proof that the BD ghost is absent assumes positive kinetic terms for both metrics, so extending it to opposite orientations is open. Linearising at the Field Origin cannot settle this: $\mathcal M$ is non-analytic at zero field, and no quadratic theory exists there ([`research/bimond-gfd/`](research/bimond-gfd/), script 09).
26. **Chiral holonomy (L3 supplement).** The computation reproduces. Uniform transport gives the identity, which is the root-blind 40-component reading, as Letter 2's Lemma requires. Chiral transport winds on every cycle, and its two classes are the two senses of circulation, exchanged by parity. The note's TetB step $R(\hat n,-\theta)$ is exactly the transpose of the TetA step: the diagonal is shared and the triangles are exchanged. That is the Gram index grid's $24 + 16 + 24$, so the sign rule follows from the two-sector algebra ([`research/bimond-gfd/11_holonomy_robustness.py`](research/bimond-gfd/11_holonomy_robustness.py)). Erratum: exactly, $\cos\Theta = -4639/6561$ and $-5983/6561$ ($6561 = 3^8$), i.e. 134.996° and 155.770°, so "135° $= 3\pi/4$" is approximate. The cited script is not in the repository; the revised proof with its script is [`proofs/chiral-holonomy-closed-frame/`](proofs/chiral-holonomy-closed-frame/) (32 checks).

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
| BIMOND: $\alpha = -\beta$, $\mathcal M$ closed form, Legendre dual of $F$ | `proofs/bimetric-two-potential-energy/` | 39 |
| Chiral holonomy: uniform $= I$ (spinor $-1$), chiral angles exact, relabelling = reversal | `proofs/chiral-holonomy-closed-frame/` | 32 |
| BIMOND × GFD research (incl. chiral holonomy reproduced; connection irreducibles; where the roots live) | `research/bimond-gfd/run_all.py` | 130 |
| Gram theorems | `papers/gram-matrix-of-tetrad-equation/verify_gram_theorems.py` | 32 |
| Coupling algebra: the cube's symmetric couplings, two TetA–TetB channels, Gram/Walsh/Paper IX as elements, second root = odd leg relabelling; η as an element (time = grade 0), the connection's lower pair on the TetA–TetB links with the swap as parity | `research/coupling-algebra/verify_*.py`, `certify_first_principles.py` (exact, independent) | 50, 34, 52 |
| 64-Tetrahedron Grid: the 64 tetrahedra as (star, spike) pairs sorted by the coupling relations; grid = large star + 24 vector-link spikes; Galeffi's counts recomputed, Table 3 corrected (16 → 40); n×n×n photon composition: 4n(n²+1) captured, 24·C(n+1,3) expelled as copies of the regular rep of S4 (proved); pixel cubes force the lattice and closure at shared corners leaves only the global root choice (proved) | `research/stellated octahedron geometry/verify_64_tetrahedron_grid.py`, `verify_photon_composition.py`, `verify_pixel_tiling.py` (exact) | 24, 14, 9 |
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

**Architecture (DFP terms → standard).** Field closure = non-degenerate metric, $\det g \ne 0$; closure constraints = ADM constraints; the canonical chain is Field Object + NET Field → $\Sigma$ → field closure function FC$_\Sigma$ (READ, then SETTLE) → registered state $`B^*_\Sigma`$. Two empirical requirements: **lossless** (no wakes, drag, hysteresis, secular drift; "Full-State Snapshot") and **local** (no faster-than-$c$ coordination). Motivation for distributed structure: the Laplacian is a neighbour comparison, $\nabla^2\Phi = \lim_{\epsilon\to0}[\Phi(x+\epsilon)+\Phi(x-\epsilon)-2\Phi(x)]/\epsilon^2$; wave propagation (LIGO) needs parts. $k = 4$ from the simplex theorem and the 1 + 3 ADM constraints.

**Postulates.** P1 Newtonian correspondence, $\lim_{x\to\infty}\mu = 1$. P2 distributed field processing: finite encoding capacity, scale-invariant deep regime, $\lim_{x\to0}\mu/x = 1$ (from $g \propto (GMa_0)^{1/2}/r$, i.e. $g = \sqrt{g_Na_0}$). P3 single-channel capacity saturation.

**MSC class** (Minimal Single-Channel Saturating Closure): (i) one occupancy $\varepsilon\in[0,1]$; (ii) detailed balance $W_+ = W_-$; (iii) linear saturation $f(\varepsilon) = 1-\varepsilon$; (iv) monomial driving $x^n$; (v) $\mu \equiv \varepsilon$.

**Derivation (Lemmas A.1–A.5).** Rates $r_+ = \alpha x^n(1-\varepsilon)$, $r_- = \beta\varepsilon$ give $\varepsilon_{\rm eq} = x^n/(k + x^n)$, $k = \beta/\alpha$. P2 forces $n = 1$; $k$ is absorbed into $a_0$:

$$\boxed{\mu(x) = \frac{x}{1+x}}\qquad(\text{Theorem 1: unique within MSC, "a conditional theorem"}).$$

Stability: $\dot\varepsilon = \kappa x(1-\varepsilon) - \kappa\varepsilon$, slope $-\kappa(x+1) < 0$, unique globally attracting fixed point. Cross-check table: $n = 2$ gives $\mu/x\to0$ and $v\propto r^{1/6}$; $n = 1/2$ gives $\mu/x\to\infty$ and $v \propto r^{-1/6}$; only $n = 1$ gives flat curves and $v^4 \propto M$.

**Three convergent readings.** (1) the kinetics above; (2) flow $d\mu/d\ln x = \mu(1-\mu)$ (logistic; "variance of a coin flip", maximal at $\mu = \tfrac12$, $x = 1$; RG-like running between a UV fixed point $\mu = 1$ and IR $\mu = 0$); (3) Padé[1/1] uniqueness: $\mu = ax/(bx+c)$ with three constraints gives $a = b = c = 1$. Also the odds power law $\mu/(1-\mu) = Cx^k$ with P2 forcing $k = C = 1$, and the remark $\mu(x) + \mu(1/x) = 1$ ("asymptotic rigidity": the deep limit fixes the Newtonian approach $\mu \simeq 1 - 1/x$). Same form as the Langmuir isotherm and Michaelis–Menten kinetics.

**Action.** $S[\Phi] = \int d^3x\,[-(a_0^2/8\pi G)F(X) - \rho\Phi]$, $X = x^2$, $F'(X) = \mu(\sqrt X)$, giving $F(x^2) = x^2 - 2x + 2\ln(1+x)$; $F \to (2/3)x^3$ deep. A scalar Lagrangian $L(x) = \tfrac12x^2 - x + \ln(1+x)$ with $dL = x\mu\,dx$ (equal to $F/2$). Status table in the paper: the function is the Famaey–Binney (2005) "simple" form; the contribution is the mechanism. Gentile et al. (2011) found it gives population-synthesis M/L ratios.

**Galactic consequences.** BTFR $v^4 = GM_ba_0$ (theorem of the deep limit). Phantom density as an operator residual,

$$\rho_{\rm ph} = \frac{1}{4\pi G}\left[\nabla^2\Phi - \nabla\cdot(\mu\nabla\Phi)\right] = \frac{\nabla\cdot[(\mu-1)\mathbf g]}{4\pi G},\qquad \rho_{\rm ph}(r) = \frac{\sqrt{GM_ba_0}}{4\pi Gr^2}\ (\text{deep, outside the source}),$$

a singular isothermal sphere. Conserved flux $r^2\mu(g/a_0)g = GM$. External field effect inherited from AQUAL: if $g_{\rm ext}\gg a_0 \gg g_{\rm int}$ then $\mu\approx1$ (Crater II, NGC 1052-DF2/DF4 as discriminants). (Later reading, §5.4: a bound system much smaller than its host's field is pure TetA internally; the host's net field cancels in its free fall. Galaxies, including dwarfs, carry their own vortex TetB, possibly driven or braked as in DEC.)

**Processing boundary** $r_c = \sqrt{GM_b/a_0}$ (where $x = 1$, $\mu = \tfrac12$): Milky Way ($6\times10^{10}M_\odot$) ≈ 8 kpc; Sun ≈ 7000 AU; Sgr A* ≈ 0.06 pc; MW total ≈ 5 kpc (listed); rich cluster ≈ 150 kpc; a 33-billion-tonne asteroid ≈ 4300 km.

**Predictions.** Fast bars $\mathcal R \approx 1.0$–1.4 (no halo-wake friction: conservative, velocity-independent, constraint-slaved phantom) vs $\gtrsim 1.4$–2 for CDM; wide binaries: Newtonian return $\mu\to1-1/x$ (slow) vs standard $1 - 1/(2x^2)$ (fast) [superseded by §5.4: wide binaries are bound systems, so pure TetA, i.e. Newtonian]; EFE in satellites; baryon-only cluster lensing.

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

**Tetrad coupling $k^2 = 16$.** $`e^a{}_\mu`$ has $4\times4 = 16$ components; isotropy engages all of them, so the "topologically coupled" acceleration of mass $m$ at $r$ is $a_{\rm coupled} = k^2Gm/r^2 = 16\,Gm/r^2$.

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

**Closure = non-degeneracy.** Completeness $`e^a{}_\mu e_a{}^\nu = \delta_\mu^\nu`$ and $\det g = -(\det e)^2$, so $\det g\ne0 \iff \det e\ne0$. Tetrad gravity is first-order symmetric hyperbolic with characteristic speed $c$ (Buchman & Bardeen 2003): the "closure rate".

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
- ADM: $\mathcal H = \sqrt\gamma(R^{(3)} + K^2 - K_{ij}K^{ij}) - 16\pi G\sqrt\gamma\rho = 0$ and $`\mathcal H_i = -2\nabla_j[\sqrt\gamma(K^j{}_i - \delta^j_iK)] + 16\pi G\sqrt\gamma j_i = 0`$ (1 + 3).
- Tetrad completeness $`e^a{}_\mu e_a{}^\nu = \delta^\nu_\mu`$ (four legs, none redundant).
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

Compatibility: Deffayet–Mourad–Zahariade symmetric-vielbein condition $`g^{\mu\nu}E^A{}_\mu L^B{}_\nu = g^{\mu\nu}E^B{}_\mu L^A{}_\nu`$, equivalent to real $\sqrt{g^{-1}f}$.

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
- Uniqueness by constraints (LIGO, simplex, ghost-free bimetric) and by component counting in $H_{\rm int} = m^2\sqrt g\sum\beta_ne_n(\mathcal S)$: $e_0 = 1$, $e_1 = \mathrm{Tr}\mathcal S$ ($k$ terms), $e_2 = \tfrac12[(\mathrm{Tr}\mathcal S)^2 - \mathrm{Tr}\mathcal S^2]$ ($k^2$ terms).
- $f = (k^3-1)/(k-1) = 63/3 = 21$; unit coefficients (one existence condition, one connection per face, one entry per frame pair). Self-similarity: each face again carries 1 + 4 + 16.
- Three structural states $f = 1 + sk + k^2$: TetA ($+k$, 21, exponent), Field Origin (no face channels, 17, numerator), TetB ($-k$, 13, denominator). Only the odd term flips. Mean lock $(21+13)/2 = 17$, spacing $k$. $17 = k^2 + 1$ ("coupling capacity"), $13 = kd + 1$ ("spatial structure"), using $k^2 - k = kd$.
- **Proposition (identification).** Under a common coupling point, the symmetric-vielbein condition and compatible 3 + 1 splits, the stellated octahedron's coupled-face matrix $C_{ab}$ equals the Hassan–Rosen $`\mathcal S^a{}_b = (E^{-1})^a{}_\mu L^\mu{}_b`$. Five conditions: index (vierbein leg ↔ face, $a = 0$ the time face), operation, block split $1 + 3 + 3 + 9$ (lapse/shift + triad), $\sum_n\binom4n = 16$, existence ($\det e\ne0$).

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

**Mechanism (§11).** Field Object, Field Atom $A_\Phi$ (a geon-like soliton of the massive spin-2 mode, with a "Valence Horizon"), Full State Snapshot, Settlement, Registration $`B^*_\Sigma`$ (grounded in ADM, Israel junction conditions, York–Lichnerowicz, Dirac constraints; appendix). **Bound vs unbound is defined here:** an *unbound* gravity-field envelope has an empty TetB chamber (massless mode; the mesh, "the stage"); a *bound* envelope has an occupied TetB (massive mode; matter, "the actors"). Binding by stellar compression, up to electron capture $p + e^-\to n + \nu_e$; TOV balance; the Field Origin as the eye of a self-sustaining vortex. Chessboard picture: bound configurations sit only on mesh nodes where $\det e\ne0$.

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
2. *$\beta_2 = 16$, primary (geometric).* $e_2(S) = \tfrac12[(\mathrm{Tr}S)^2 - \mathrm{Tr}S^2]$ counts pairwise couplings; weighting it by the 16 boundary channels gives each channel unit weight.
3. *$\beta_2 = 16$, secondary (covariance).* $\dim C\ell_{1,3} = \sum_k\binom4k = 16 = \dim\mathrm{End}(\mathbb R^{1,3})$ = the components of $S$. Once the other terms are fixed, $e_2$ is the only free term and "must absorb" all 16; the paper words this as an interpretation ("we therefore interpret").
4. *Parity:* under $\lambda_i\to-\lambda_i$ the odd $e_1, e_3$ change sign (grade 1 and 3 reverse), so $\beta_1 = \beta_3 = 0$. *Exchange:* $g\leftrightarrow f$ sends $S\to S^{-1}$, so $\beta_0 = \beta_4$. *Normalisation:* $\beta_0 = 1$.
5. Result: $(\beta_0,\ldots,\beta_4) = (1,0,16,0,1)$, $V(S) = e_0 + 16e_2 + e_4$. Polynomial reading: the $1$ is bare existence ($\beta_0 = \beta_4$), $k^2 = 16$ is $\beta_2$, and no odd power gives $\beta_1 = \beta_3 = 0$.

**Ghost freedom.**
- ADM split: $e^0 = N\,dt + N_idx^i$. A 4-form contains exactly one $dt$, and $dt\wedge dt = 0$, so $\partial^2\mathcal L_{\rm int}/\partial N^2 = \partial^2\mathcal L_{\rm int}/\partial\tilde N^2 = 0$.
- The potential is in the Hassan–Rosen class, so the secondary constraint and the BD-ghost removal are inherited. The locked set is a point inside the ghost-free family.

**UV → IR bridge (EFT statement, explicitly not an identity of actions).**
- Stückelberg: $`\tilde e^{a}{}_{\mu}\to\tilde e^{a}{}_{\nu}(\varphi)\,\partial_{\mu}\varphi^{\nu}`$ with $\varphi^\mu = x^\mu - \partial^\mu\pi/\Lambda_3^3$, $\Lambda_3 = (m^2M_{\rm Pl})^{1/3}$.
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
  - $\mathrm{lcm}(3,4) = 12 = KD$.
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
  - The frame $`e^a{}_\mu`$ ($K$).
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

## Paper XIII — Nuclear Binding and Magic Numbers from the Bound Law (`13-nuclear-binding-bidirectional-sst`)

*MNRAS-format letter. Code: `github.com/field-dynamics/nuclear-binding` and `Supplementary/pipelines/` (30-test harness). Status: [E]. Magic numbers are exact arithmetic; the binding curve uses one calibration point plus a constructed envelope.*

**Framing (naming matches the later rules).**
- The four-term action is called the SST, and $g_s = g_t^2/(a_0+g_t)$ is its spherical, static field equation.
- In galaxies "matter sources the field and the field does not source itself" (one-directional). The galaxy itself is "a bound vortex whose interior is fed through its central drain".
- In a nucleus each nucleon is source and response at once.

**Bound law.**
- Self-consistency: the return share $(1-\mu)$, used as the effective source in the field equation, must give back $\mu$. That gives $x(1-\mu)^2 = \mu$, with root $\mu_b = [(2x+1) - \sqrt{4x+1}]/(2x)$.
- $\mu_b(2) = (5-3)/4 = \tfrac12$ is called "the bound-state field origin", the point where forward and return capacity split equally.
- This is the face-crossing/self-consistency motivation. research/aqual gives the exchange-image derivation (Part I §4.6).

**Walk.**
- $2(D+1) = 2^D \Rightarrow D = 3$, $K = 4$. Here $K$ is the branching factor and $D$ the depth.
- A Sierpiński triangle subdivided $D$ times at branching $K$ has $K^D = 64$ positions (4 faces × 4 channels × 4 sub-channels). The parent has $K = 4$ sectors, $4\times64 = 256$ in all. Face index 3 is the gate face.
- Nucleon $i$ sits at $x = i^2$; the stated reason is the Jacobian $dx = 2i\,di$.

**Magic numbers.**
- Same $T$, $G$, $M = 2(T - G)$ as XI. Here the 2 is "proton and neutron, or the two tetrahedra" (XI: two time-face orientations).
- The gate is the triangular number of side $n-1$ on the gate face. It first contributes at $n = K$: $G(4) = 6$ cuts shell 4 from 20 to 8.
- Capacities 2, 6, 12, 8, 22, 32, 44, i.e. the $20\to28$ gap without spin–orbit.

**Binding curve.**
- Rising branch: $\Sigma_A = \sum_{i\le A}\mu_b(i^2)$, $\Sigma_{64} = 59.928$ (recomputed 59.9278), and $B_1(A) = (B/A)_{\rm Zn}\,(64/A)\,(\Sigma_A/\Sigma_{64})$ with $(B/A)_{\rm Zn} = 8.756$ MeV.
- Each sector crossing (64 Zn, 128 Te, 192 Os) reflects the curve: $B^{\rm inv}_n = \mathrm{CEIL}_n - B_{\rm local}(A - A_n)$.
- $\mathrm{CEIL} = B_{\rm Zn} + B_{\rm bdy} - \mu_b(2)(B_{\rm Zn} - B_{\rm bdy})$, giving 17.512, 17.141 and 16.955 MeV.
  - Recomputed: $B_1(128) = 9.0034$, so $B_{\rm bdy} = 8.5086$, then 8.3849. All three ceilings reproduce.
- Prediction is $\min(B_1, B_1^{\rm inv}, B_2^{\rm inv}, B_3^{\rm inv})$.
- Stated fit: MAE 95 keV, $R^2 = 0.82$ He–Pb (sector 0: 97 keV, $R^2 = 0.90$; after 64: 36 keV, $R^2 = 0.96$). Te-128 within 14 keV.
- Recomputed spot checks against the paper's inputs:
  - C-12: −249 keV, as stated.
  - O-16 −221, Ca-40 −44, Fe-56 −97, Sn-120 −57, Pb-208 +239 keV.
  - He-4: −1.26 MeV. The paper notes $A<12$ has residuals of ≥ 200 keV.
- **Calibration value.** The paper and its pipelines use $B/A({\rm Zn\text{-}64}) = 8.756$ MeV. AME2020 gives 8.736 MeV, as listed in the repo's own `research/nuclear/gfd_nuclear_enterprise_20.py` and `research/bound-gravity-and-packing/…_20.py`. 8.756 is close to Zn-66 (8.760).
  - The 20 keV offset rescales the whole curve by 0.2%.
  - It also makes the "0 keV at Zn" statement true only for the input value.
  - Worth correcting at the source.
- **Free parameters.** The abstract says zero; the text says one energy scale "calibrated from a single element". The envelope (reflection at sector boundaries, the ceiling rule, the min) is a construction chosen in the paper, not derived from the action.

**Stability at lead.** Sectors 0–2 hold $3\times64 = 192$ positions; sector 3 is the gate. Pb-208 is 16 positions into the gate sector, and beyond it nuclei decay. (XI places the ceiling at $K^K = 256$ with Bi-209 as the last stable nucleus; the two letters choose different endpoints.)

**Limitations, as stated.** Few-body nuclei ($A<12$). Shell-closure fine structure is deferred to a "shell-by-shell decomposition".

## Companion — Topological Field Closure: A Bidirectional Derivation of the Hubble Constant and the Electron Mass

*Short PDF (DFP-era vocabulary, lower-case $k$). Zenodo 10.5281/zenodo.18371849, with a Python 3.6+ validation suite. Status: [E].*

**Argument.**
- *Simplex theorem.* The minimum enclosing polytope in $d$ dimensions has $d+1$ faces, so $k = 4$. The paper cites tetrahedral examples: CH₄, water, diamond, SiO₄.
- *Isotropic coupling.* All-to-all face coupling gives $k^2 = 16$, the only rotation-invariant count for tetrahedral topology. Test: $a_0/(Gm_e/r_e^2) = 15.93$ (with $a_0 = 1.22\times10^{-10}$; 0.41% from 16).
- *Horizon.* Unruh $T = \hbar a/2\pi k_Bc$ set equal to Gibbons–Hawking $T = \hbar H/2\pi k_Bc$ gives $a_0 = cH/2\pi$. This "flat" relation gives 78.9.
- *Geometric ratio.* $H_{\rm meas} = H_{\rm flat}/\sqrt{k/\pi} = 78.9/1.128 = 69.9$.
- *Forward.* $g_e = Gm_e/r_e^2 = 7.66\times10^{-12}$, so $a_0 = 16g_e = 1.225\times10^{-10}$ and $H = 2\pi k^2Gm_e/(r_e^2c\sqrt{k/\pi})$, stated as 69.92 (GW170817 70.0, 0.11%).
- *Reverse.* Since $r_e\propto1/m_e$, $Gm_e/r_e^2\propto m_e^3$, so $m_e = [H e^4\sqrt{k/\pi}/(2\pi k^2G(4\pi\varepsilon_0)^2c^3)]^{1/3}$. From $H = 70$ the paper states $9.11\times10^{-31}$ kg, "0.01% of CODATA".
- *Measurement cage.* $(k/\pi)^{1/4} = 1.062$ (±6.2%), described as the "geometric mean" of a 0–12.8% path correction. The range is 65.8–74.3. All seven listed methods (66.0 lensing, 67.4 Planck, 68.0 BAO, 70.0 GW, 72.5 TRGB, 73.0 SH0ES, 73.9 masers) fall inside. Chance probability is quoted as $0.12^7 = 3.6\times10^{-7}$.
- *Convergence test.* The mean of the seven, times 1.128, is 79.1 (recomputed 79.12). GW170817 alone gives 79.0.

**Arithmetic check.**
- *Forward.* With the paper's own $a_0 = 1.2250\times10^{-10}$ (recomputed from CODATA $G, m_e, r_e$), the formula gives $H = 70.21$, not 69.92. 69.92 is the value for $a_0 = 1.220\times10^{-10}$ (Paper IV's first evaluation). So the companion's eq. 3 and eq. 4 use different $a_0$.
- *Reverse.* Eq. 5 with $H = 70.0$ gives $m_e = 9.1002\times10^{-31}$ kg, which is −0.10% from CODATA. With $H = 69.92$ it gives −0.14%. The "0.01%" is not reproduced. The 0.10% figure (Paper IV's) is the one the algebra supports.
- *Probability.* The $3.6\times10^{-7}$ treats the seven measurements as independent and uniform on 50–150 km/s/Mpc. In practice they cluster around 70 by any account, so the number overstates the evidence.
- *Cage edges.* These check out: $69.92\times1.0623 = 74.28$ and $69.92/1.0623 = 65.82$.

## Letter 1 — The Coordinate-Space Geometry of the Tetrad Frame

*Letter. Supplementary material: `fig1_tetrad_frame.html`, `run_all_validations.py` (NumPy/SciPy), `supplementary_signature_to_frame.pdf` (the frame derived from the Lorentz signature), `supplementary_scheme_proof.pdf` (= P-two-regions). Status: [T]. The paper states that the result holds before any dynamics.*

**Claim.** One orthonormal tetrad, with no dual frame assumed, generates the stellated octahedron and its 16 boundary channels.

**Steps.**
1. *From signature to frame.* $(-,+,+,+)$ sends null directions to $S^2$ with $SO(3)$ symmetry. Asking that four directions on $S^2$ pick out no net direction forces the regular tetrahedral frame, with pairwise inner product $-1/3$ (proved in the supplement).
2. *Four planes.* $v_1..v_4$ as before, with TetA $=\{\max v_i\le1\}$. The $v_i$ are the spatial one-forms projected on the tetrahedral normals rather than on three orthogonal legs.
3. *Boundedness theorem.*
   - Choosing a sign per projection gives $2^4 = 16$ convex regions. The only relation among the $v_i$ is $v_1 + v_2 + v_3 + v_4 = 0$.
   - Bounded means the selected inward normals surround the origin.
   - All $+$ and all $-$ do. In any mixed choice the flipped normal is a positive combination of the others (e.g. $-v_4 = v_1+v_2+v_3$), so all four lie in one half-space and the region is unbounded.
   - So exactly two are bounded, TetA and TetB $=\{\max(-v_i)\le1\}$. Recomputed by linear programming over all 16 sign patterns: exactly $(++++)$ and $(----)$ are bounded.
4. *Intersection.* $|v_i|\le1$ for all $i$ gives six vertices $(\pm1,0,0),(0,\pm1,0),(0,0,\pm1)$ and twelve equal edges, i.e. the regular octahedron. The union is the stella octangula (Kepler 1619).
5. *Channels.* The opposing vertex cuts each coupled face into 3 exposed corners + 1 inverted core (the first Sierpiński level), giving $4\times4 = 16$ connected boundary regions. Whether deeper recursion matters is left open.

**Inventory.**

| Quantity | Formula | Value |
|---|---|---|
| Tetrahedra | — | 2 |
| Faces per tetrahedron | $K$ | 4 |
| Vertices | $2^D$ | 8 |
| Edges | $KD$ | 12 |
| Faces | $2K$ | 8 |
| Channels | $K^2$ | 16 |
| $V+E+F$ | $K(K+D)$ | 28 |

$V - E + F = 4 = 2\chi(S^2)$, two disjoint closed surfaces.

**Discussion points.**
- Each tetrahedron has one face whose normal has uniform sign and three with mixed signs. This 3 + 1 pattern mirrors $(-,+,+,+)$.
- The metric is quadratic in the tetrad, so the parity-related frames give the same $g_{\mu\nu}$. TetA and TetB are "distinct tetrad-level realisations of the same metric". This is the coordinate picture of P-two-regions' two scheme components.
- The geometry is independent of the action, so it sits in the local frame of any covariant tetrad theory.

**Labelling note (checked, applies across papers).**
- The region TetA $=\{\max v_i\le1\}$ has its *vertices* at $(+,+,-), (+,-,+), (-,+,+), (-,-,-)$, the even-popcount corners $\{6,5,3,0\}$. Its *face normals* $v_i$ point at the odd corners $\{7,4,2,1\}$.
- Paper IX's vertex table assigns the odd corners $\{1,2,4,7\}$ to TetA, which matches the normals, not the vertices, of this region.
- Both labellings name the same pair, and only the "which is A" convention differs. A reader matching vertex coordinates across papers should use the half-space definition.

## CL — The Gravitational Constitutive Law from the Tetrad Frame Geometry

*Letter, companion to L1. Supplementary Notes 1–3 hold the full routes. Status: [D]. It derives the form of $\mu$ and states that $a_0$ is an empirical input: "determining it … is the subject of ongoing work".*

**Problem.**
- AQUAL $\nabla\cdot[\mu(|\nabla\Phi|/a_0)\nabla\Phi] = 4\pi G\rho$ needs $\mu\to1$ for $x\gg1$ and $\mu\propto x$ for $x\to0$.
- Many forms satisfy both limits: simple $x/(1+x)$, standard $x/\sqrt{1+x^2}$, $1 - e^{-\sqrt x}$. Famaey & Binney (2005) prefer the simple form by fit.

**Route 1: graded structure of the metric.**
- From $\eta_{ab}$: $K = 4$ (size of the matrix), $D = 3$ (positive eigenvalues), and root count $n = 2$ (the tetrad equation is degree 2 in $e$).
- Closure $2(D+1) = 2^D = 8$.
- Ranks give dimensions: $\det e\ne0$ is rank 0 (1), $`e^a{}_\mu`$ rank 1 ($K$), $\eta_{ab}e^ae^b$ rank 2 ($K^2$). They add, giving $f = 21$.
- Parity sign $(-1)^r$ makes only rank 1 odd. Three structural components (TetA, octahedral core, TetB) give $s\in\{+1,0,-1\}$. Odd interpolation on three points gives $Ks$, so $f = 1 + sK + K^2$.
- A rational bijection of $\mathbb P^1$ is fractional-linear (Hartshorne). Three conditions give $s(x) = (x-1)/(x+1)$, then $\mu = (f-13)/8$.
- Here $s$ is defined as a three-state label and only *then* made continuous by the map. That is the step later notation writes as $\sigma(x)$.

**Route 2: equilibrium.**
- Let $\epsilon$ be the TetA fraction. Throughput to TetA is $\propto x^n(1-\epsilon)$, to TetB $\propto\epsilon$. Balance gives $\epsilon = \kappa x^n/(1+\kappa x^n)$.
- Deep-field $\mu/x\to$ const forces $n = 1$. This is an observational input (flat curves, BTFR).
- The rate ratio $\kappa$ (the letter writes it "$K$", which clashes with $K = 4$) is absorbed into $a_0$.
- So the route fixes the form, not the scale. It is globally attracting: the net rate has negative slope in $\epsilon$.

**Route 3: exchange symmetry (the cleanest).**
- Parity swaps the sectors and inverts $x$: $\mu(1/x) = 1 - \mu(x)$. With odds $\Omega = \mu/(1-\mu)$ this becomes $\Omega(1/x) = 1/\Omega(x)$, with $\Omega(0) = 0$ and $\Omega(\infty) = \infty$.
- Rational and bijective gives $\Omega = (ax+b)/(cx+d)$; $\Omega(0) = 0$ gives $b = 0$.
- The exchange condition gives $a^2x = (c+dx)(cx+d)$, so $cd = 0$ and $a^2 = c^2+d^2$ (checked).
- $d = 0$ makes $\Omega$ constant (excluded). $c = 0$ gives $a = \pm d$, and positivity picks $\Omega = x$.
- Hence $\mu = x/(1+x)$, with $\mu(1) = \tfrac12$ automatic.

**Why the three agree.** Each identifies the TetA:TetB odds with $x$.
- Route 1: $(f-13)/(21-f) = x$.
- Route 2: $\epsilon/(1-\epsilon) = x$.
- Route 3: $\Omega = x$.

**Consequences.**
- Complement symmetry is Route 3's premise, not a coincidence.
- BTFR: $\mu\approx x$ gives $v^4 = GMa_0$ in spherical symmetry.

**Note against later naming.**
- The letter's BTFR paragraph says the deep-field limit "corresponds to the TetB-dominated sector … is itself the TetB sector of the tetrad geometry". The later rule (and `research/aqual/README.md`, which cites these lines) is that the deep field is the exterior regime $x\ll1$, where the TetB *share* $1-\mu\to1$. TetB itself is the throat interior.
- The source `papers/letter-constitutive-law-tetrad-geometry/letter.tex` still carries the conflated wording.

## Letter 2 — The Other Half of Gravity: Torsion and the Two-Chamber Structure of the Tetrad Frame (v2)

*Letter, companion to L1. Supplementary: `supplementary_tetb_fraction.pdf` and `run_all_validations.py` (NumPy/SciPy/SymPy, 52/52 claims; §13 checks $P^T\eta P = \eta$ per sector, §14 checks the exchange → dark-ratio chain symbolically). Status: [T] for the lemma and counts, [D] for the partition reading.*

**Counts.** $`\Gamma^I{}_{JK}`$ has $K^3 = 64$ components. The lower-pair symmetric part has $K\cdot K(K+1)/2 = 40$ (Christoffel); the antisymmetric part has $K\cdot K(K-1)/2 = 24$ (torsion). Einstein (1915) set torsion to zero; Cartan (1922) and Hehl (1976) restore it and couple it to spin, giving the same vacuum predictions.

**Lemma, proposition, corollary.**
- *Lemma.* A torsion-free connection cannot distinguish TetA from TetB.
  - It is fixed by $g$ and $\partial g$ (fundamental theorem).
  - $g = \eta_{ab}e^ae^b$ is bilinear in $e$, so under $P: e^i\to-e^i$ both factors flip sign and $g$ is unchanged.
- *Proposition.* $\phi: e\mapsto\eta(e,e)$ is quadratic, so $e$ and $Pe$ lie in the same pre-image. The metric is root-blind; a torsionful connection depends on $e$ directly and resolves the root.
- *Corollary.*
  - Torsion is the necessary connection-level carrier of the TetA/TetB distinction.
  - Setting it to zero collapses the two chambers, and the interaction core with them, into one effective sector.
  - "Image-complete but root-blind."

**TetB fraction.**
- The response splits as $\mu$ (TetA) and $1-\mu$ (TetB). In the weak field the connection reduces to $\nabla\Phi$, so the split acts on $g$.
- Exchange gives $\Omega\to1/\Omega$, and a rational bijection forces $\Omega = x$ (as CL Route 3). So $\mu = x/(x+1)$ and $1-\mu = 1/(x+1)$.
- Torsion-free means $\mu = 1$. The missing share is $\Delta\mu(x) = 1/(x+1)$, which is ≈ 0 for $x\gg1$, ½ at $x = 1$, and ≈ 1 for $x\ll1$.

**Dark matter as the residual.**
- With $g_{\rm obs} = g_{\rm bar} + g_{\rm DM}$, $g_{\rm bar} = \mu g_{\rm obs}$ and $g_{\rm DM} = (1-\mu)g_{\rm obs}$, so $g_{\rm DM}/g_{\rm bar} = 1/x$.
- $M = gr^2/G$ shell by shell gives $M_{\rm DM}/M_{\rm bar} = 1/x$.
- **No cusp.** $g_{\rm DM} = g_{\rm obs}/(x+1) = a_0\,x/(x+1) < a_0$ (recomputed), so the phantom field saturates at $a_0$. This implies a finite central density, not an NFW cusp.

**Polynomial organisation (independent of the above).**
- Ranks 0, 1, 2 carry dimensions $1, K, K^2$. Only rank 1 is parity-odd, giving $f = 1 + sK + K^2$, with values 21/17/13 and $\Delta f = 2K = 8$.
- *Theorem.* With $D = K-1$, $K\cdot K(K-1)/2 = D\cdot2K$ iff $K = 4$ (divide through to $K/2 = 2$). So $24 = D\times\Delta f = 3\times8$.
- Counts table: $1, 4, 16, 10, 6, 64, 40, 24 = K^0, K, K^2, K(K\pm1)/2, K^3, K\cdot K(K\pm1)/2$.

**Discussion.**
- Einstein–Cartan keeps the 24 components. Here, keeping them keeps TetB and the full partition. "At the level of field magnitudes", Christoffel + contorsion ↔ $\mu$ + $(1-\mu)$.
- Logistic: $x\,d\mu/dx = \mu(1-\mu)$, i.e. $d\mu/dt = \mu(1-\mu)$ with $t = \ln x$.
- Strong-field tests (Solar System, pulsars, GW speed) are untouched because $\Delta\mu\to0$. (Later reading, §5.4: in a bound system the TetB share is exactly zero, not small; TetB is the host galaxy's net field.)
- Concordance at three levels from $2(D+1) = 2^D$: the stellated octahedron, $K^3 = K^D$, and $24 = D\times2K$.

**Notes.**
- The lemma is a statement about parity invariance of the metric and holds for any $K$. The "$K = 4$ only" statement belongs to the 24 = 3 × 8 factorisation (Part I §5.2 corrected to say so).
- The identification "the 24 torsion components carry the TetB share $1/(x+1)$" is made at the scalar-partition level, not by a calculation of a contorsion tensor in a galaxy.
- Symbol clash: this letter's $\Delta\mu = 1/(x+1)$ is not XII's $\Delta\mu = 2/17$ ("topological coupling impedance").

## Letter 3 — Field Closure of the Tetrad Frame (with `proof_polynomial_40_24` and `supplementary_covariant_completion`)

*Letter plus two supplementary notes. Supplementary files: `figure2_tetrad_partition.html` and `run_all_validations.py` (polynomial identity, partition, logistic identity, RAR, $F$ limits). Status: [T] for the counting, [D] for the identification and the action. The γ argument is [D] with an ansatz.*

**Letter: the torsion-free projection.**
- Per upper index $\lambda$ the lower pair is a $K\times K$ grid: $K$ diagonal entries and $(K^2-K)/2 = 6$ mirror pairs.
- Torsion-free keeps each pair's symmetric half and drops its antisymmetric half. Per slice that keeps $K + 6 = 10$ and drops 6; over $K$ slices, 40 kept and 24 dropped, 64 in all.
- In polynomial form, kept $= (f(K,+1)-1)/2$ and dropped $= (f(K,-1)-1)/2$.
- With TetA ↔ $s = +1$ and TetB ↔ $s = -1$ (from L2), "the 24 discarded components are the second root of the tetrad equation".
- The scheme has two components, so both roots satisfy the same equation and neither can be eliminated. Choosing an orientation is a projection, not a removal.
- **Field closure** means all $K^3$ connection components are active. This is distinct from Einstein's "complete field theory" and from geodesic completeness.
- Unlike Einstein–Cartan, where torsion is tied to spin and vanishes in vacuum, here torsion carries $1-\mu(x)$ and persists in vacuum: "kinematic, acceleration-dependent".

**Letter: the partition in space (Fig. 2).**
- The surfaces of revolution $\mu$ (blue, TetA) and $1-\mu$ (red, TetB) mirror each other and cross on the white ring $x = 1$.
- Centre ($x\gg1$): the TetA share dominates and the Christoffel sector suffices. Rim ($x\ll1$): the TetB share dominates.
- The "disk-and-bulge morphology" is said to emerge from the crossing and to need both roots. This is an interpretive reading of the plot of $\mu(x(r))$; no morphology is computed.
- $x\mu' = \mu(1-\mu)$ peaks at $\tfrac14$ on the ring. $\mu(1-\mu)$ is read as the continuous analogue of the $s = 0$ core.
- RAR: $g_{\rm bar} = \mu g_{\rm obs} = g_{\rm obs}^2/(g_{\rm obs}+a_0)$. Cites 0.057 dex intrinsic scatter over 175 galaxies (Li 2018).
- Consequences listed:
  - Bounded central phantom field, $< a_0$, so no cusp.
  - No new particles.
  - Solar System at $x\sim10^8$, where the TetB share is $\sim10^{-8}$. (Superseded, §5.4: the solar system is pure TetA; the per-mass $10^{-8}$ reading is excluded by perihelia and Cassini.)
- AeST (Skordis–Złośnik) adds fields; GFD restores connection content removed by a constraint.

**Proof note (40/24).** It is the same counting in seven steps (Steps 1–5 matrix counting, 6 polynomial identity, 7 interpretation).
- Surplus kept − dropped $= \Delta f/2 = K$ per slice and $K^2 = 16$ in total ("the asymmetry 40 vs 24 is the $K^2$ term"). Restored: $(K^2+K)/2 + (K^2-K)/2 = K^2$ per slice, $K^3$ in total.
- *Counting nuance.* Step 6 says the subtracted $K^0 = 1$ "maps to the diagonal entries". There are $K = 4$ diagonal entries, and they are inside the kept 10. The $\pm K$ difference between 10 and 6 is exactly those diagonals, while Step 7 attributes $\pm K$ to the off-diagonal pairs. The numerical identity is exact; the term-by-term reading does not match the grid count.

**Covariant-completion note.**
- *§1.* $F = 2\int_0^{\sqrt y}u^2/(u+1)\,du$ with $u^2/(u+1) = u - 1 + 1/(u+1)$, giving $y - 2\sqrt y + 2\ln(1+\sqrt y)$. The round trip $F' = \mu(\sqrt y)$ is checked.
  - Term map: $u\to y$ ($K^2$), $-1\to-2\sqrt y$ ($sK$), $1/(u+1)\to2\ln(1+\sqrt y)$ ($K^0$).
  - The remainder $1/(u+1) = 1-\mu$, so the log term integrates twice the TetB share.
  - Limits: $F/y\to1$; $F\to\tfrac23y^{3/2}$.
- *§2.* Prefactors are $16 = K^2$ (with $4\pi/K = \pi$ sr per face), $8 = 2^D$ and $4 = K$, a halving sequence. $\Phi$ "is not a new field": it is the Newtonian potential, with the torsion share carried implicitly inside $F$.
- *§3 (lensing).*
  - AQUAL-in-GR treats $(\mu-1)$ as a separate scalar with anisotropic stress, so $\gamma = \Psi/\Phi = \mu(x)$, and $\gamma\to0$ at the rim gives half the lensing (the reason for TeVeS).
  - GFD keeps one equation $\nabla\cdot[\mu\nabla\Phi] = 4\pi G\rho$ and one potential in $g_{00} = -(1+2\Phi/c^2)$, $g_{ij} = (1-2\Phi/c^2)\delta_{ij}$, so $\gamma = 1$ everywhere.
  - Table: GR (40 of 64, wrong rotation, $\gamma = 1$); AQUAL+φ (correct rotation, $\gamma = \mu$); GFD (64 of 64, correct rotation, $\gamma = 1$).
  - The single-potential metric is *posited*. The metric variation, which would include the stress–energy of the $F(y)$ term, is described but not carried out.
- *§3 (EM term).* It leaves null geodesics alone (conformal invariance of Maxwell in 4D). Its stated role is cosmological: $\Phi(z)$ modulates EM scaling relations.
  - Not discussed: as written it makes $\alpha_{\rm eff} = \alpha e^{2\Phi/c^2}$, a coupling $k_\alpha = 2$ of $\alpha$ to the gravitational potential. Laboratory bounds are $|k_\alpha|\lesssim10^{-6}$–$10^{-7}$ (Part I §3).
- *§4.*
  - The scalar variation gives $-(1/4\pi G)\nabla\cdot[\mu\nabla\Phi]$, set against $-\rho$; the prefactor $(a_0^2/8\pi G)(2/a_0^2) = 1/4\pi G$ checks.
  - Expanded: $\mu\nabla^2\Phi + \nabla\mu\cdot\nabla\Phi = 4\pi G\rho$.
  - Spherical case: $\mu(g_t/a_0)g_t = g_s$, so $g_s = g_t^2/(a_0+g_t)$.
  - PPN $\beta = \gamma = 1$. GW speed $c$ because the tensor sector is pure Einstein–Hilbert.

## RAR — The Radial Acceleration Relation from a Zero-Parameter Covariant Action

*Letter. Supplementary Proofs A (frame from the Lorentz tetrad, = P-forced), B (energy functional, = P-aqual/FY) and C (exchange symmetry, = P-exchange). Code: `sparc_rar.py`, with cached data in `supplementary/sparc_rar.csv`. Status: [O]. The paper states that "zero parameters" refers to $\mu$, not to $a_0$.*

**Chain.**
- Action (four terms) and $F(y)$.
- Varying with respect to $\Phi$ gives $\nabla\cdot[\mu\nabla\Phi] = 4\pi G\rho$. In the static weak field $e^{-2\Phi/c^2}\to1$ and the vector sector decouples.
- Gauss's theorem gives $\mu(g_t/a_0)g_t = g_{\rm bar}$, so $g_{\rm obs} = \tfrac12[g_{\rm bar} + \sqrt{g_{\rm bar}^2 + 4a_0g_{\rm bar}}]$.

**Data.**
- SPARC (176 galaxies), cut to $Q\le2$: stated as 164 galaxies and 3284 bins.
- Baryons: $v_{\rm bar}^2 = v_{\rm gas}|v_{\rm gas}| + 0.5v_d^2 + 0.7v_b^2$ (3.6 µm), with 1 (km/s)²/kpc $= 3.241\times10^{-14}$ m/s². $a_0 = 1.2\times10^{-10}$.
- Comparator: McGaugh+2016, $g_{\rm bar}/(1 - e^{-\sqrt{g_{\rm bar}/a_0}})$.

**Result, recomputed from the cached CSV.**

| Fit | Mean | σ | Median |
|---|---|---|---|
| GFD | −0.0269 | 0.1814 | −0.0165 |
| McGaugh | −0.0216 | 0.1817 | −0.0094 |

- This reproduces the table: $\Delta\sigma = 0.0003$ dex, and the 0.005 dex mean offset is comparable to $\sigma/\sqrt N\approx0.003$.
- The CSV holds 3284 points from **163** distinct galaxy names, not 164.
- The scatter of 0.18 dex vs Lelli+2017's 0.13 dex comes from the minimal pipeline: flat Υ, no inclination cut, no error weighting. It affects both curves equally.

**Scope, as stated.** The mean RAR tests only $\mu$, and any theory with the simple $\mu$ gives the same curve. The proposed discriminators are dwarf-spheroidal dispersions, galaxy–galaxy lensing and mergers, where the extra sectors switch on.

**Naming notes.**
- This letter calls $F_{\mu\nu}$ "the field strength of an auxiliary vector field" whose sector activates in time-dependent, non-axisymmetric or strong-field systems.
- The L3 covariant-completion note treats the same term as the electromagnetic coupling, with a cosmological role only. The two descriptions of the fourth term differ.

## DEC — Decoding Mass from Rotation Curves (MNRAS-format letter)

*Letter. Code: `generate_letter_figures.py`, `run_all_validations.py`; `supplemental_material.pdf` (§I has the field-closure postulates for $\mu$). Status: [O]. It is framed as "an axiomatic kinematic framework", with the full covariant derivation "presented separately".*

**Two equations, two constants.**
- Poisson $\nabla^2\Phi = 4\pi G\rho$ gives the source field $g_s$.
- The spherical limit of the four-term action gives $g_s = g_t^2/(a_0+g_t)$, or forward $g_t = \tfrac12[g_s + \sqrt{g_s^2 + 4g_sa_0}]$.
- Constants: $G$ (CODATA) and $a_0 = 1.2\times10^{-10}$ (Milgrom's standard value, not derived here).

**Inverse.**
- With $g_t = v^2/r$, $M_{\rm dec}(r) = r^2g_s/G = rv^4/[G(a_0r + v^2)]$ (checked).
- This is the *effective* mass: the mass-equivalent of the field an exterior observer sees, defined only over the measured radii. The paper states that it "is not assumed to be baryonic mass; comparison to baryonic mass is the diagnostic".

**Demonstrations.**
- *Milky Way* (McMillan 2017 baryons: Hernquist bulge 1.5×10¹⁰, scale 0.6 kpc; disk 4.57×10¹⁰, $R_d$ 2.2 kpc; gas 1.5×10¹⁰; total ~7.6×10¹⁰ M☉). At 25 kpc, $M_{\rm dec}\approx6.6\times10^{10}$ vs photometric 7.3×10¹⁰ vs ΛCDM 2.3×10¹¹. The 6.6×10¹⁰ corresponds to $v\approx196$ km/s (recomputed).
- *M33* (Corbelli 2000, ~7×10⁹ M☉ baryons). At 17 kpc, $M_{\rm dec} = 1.38\times10^{10}$ (needs $v\approx129$ km/s), i.e. about 2× the baryons, and 5.2× below ΛCDM's 7.2×10¹⁰.
- Footnote: at the last radii the decode sits 6.4σ (MW, ±32 km/s) and 17.2σ (M33, ±8 km/s) below the ΛCDM enclosed mass.
- Velocities are Gaussian-smoothed (width 6.2% of the radial span) before inversion. The round trip reproduces $v$ by construction.
- *Also shown:* CamB (Fig. 2), where the decode is *below* photometric, and NGC 3198 (Fig. 3, Begeman 1991), where the decode tracks the baryons.

**Interior topology and the deficit.**
- Ellis drainholes and Einstein–Rosen bridges allow an exterior field not fixed by the exterior matter. Such structures are placed at the centres of spiral galaxies.
- $\Delta M_{\rm eff} = M_{\rm phot} - M_{\rm dec}$ is a zero-parameter output, read as the drain's "power output". Vortex analogies: ping-pong balls, bathtub drain, jet engine, magnetic stirrer.
- "Quiet interior": decode = baryons. "Active interior": the interior "drives the field beyond what the exterior matter alone sustains".

**Notes.**
- *Sign of the deficit.* An interior that drives the field beyond the exterior matter would make $M_{\rm dec} > M_{\rm phot}$ ($\Delta M_{\rm eff}<0$). But the worked case, CamB, has $M_{\rm dec} < M_{\rm phot}$ ($\Delta M_{\rm eff}>0$) and is still described as "additional field strength sustained by the interior". The sign convention for "drives" versus "brakes" is not pinned down in the letter. Part I §3.2 records both signs as allowed.
- *Wording conflict.* The Framework paragraph says the inverse "returns the baryonic mass distribution that produces it", which conflicts with the later and more careful "not assumed to be baryonic mass".
- *Scope.* The abstract names the MW and M33; the body adds CamB and NGC 3198. "Factor of order unity" covers M33's factor of about 2.
- *Naming.* The letter calls the quadratic the "transition relation", and the summary/abstract framing calls the four-term action $S_{\rm ST}$. Under the naming rules the quadratic is the spherical field equation.

## GRAM — The Gram Matrix of the Tetrad Equation (supplementary manuscript)

*Supplementary note. Status: [T]. Every step is matrix arithmetic; the paper states that no dynamics are used.*

**Part I: three Gram products.**
- $M$ is the $D\times K$ spatial frame and $G = M^TM$. The equation is even in $M$, so $M_2 = -M_1$ is also a solution. Time reversal acts on the time leg, which is outside $M$.
- Products: $G_{11} = M_1^TM_1$, $G_{22}$, and $G_{12} = M_1^TM_2 = G_{21}$.
- Lemma 1 (root-blind): $G_{22} = G_{11}$.
- Lemma 2: $G_{12} = -G_{11}$, the only root-resolving product.
- Lemma 3: for $M_1$ with columns $(+,+,+), (+,-,-), (-,+,-), (-,-,+)$, $G_{II} = D = 3$ and $G_{I\ne J} = -1$.
- Lemma 4: all three are $O(D)$-invariant.
- Lemma 5: $G = (D+1)I - J$, with eigenvalues 0 (×1, eigenvector $(1,1,1,1)$, i.e. closure $\sum_IM_{aI} = 0$) and $D+1 = 4$ (×3). The trace 12 checks.

**Part II: geometry.**
- The columns of $M_1$ and $-M_1$ are disjoint and exhaust $\{\pm1\}^3$, the cube of side 2.
- Constant pairwise inner product makes each set a regular tetrahedron (Coxeter), and $S = [M_1\,|\,M_2]$ is the stellated octahedron.
- TetA is named as the columns of $M_1$ read as *vertices*.

**Part III: index grid.**
- Per slice, 6 strict upper + 4 diagonal + 6 strict lower, so the full connection is $24 + 16 + 24 = 64$.
- Torsion-free identifies lower with upper, keeping $16 + 24 = 40$. The Christoffel part depends only on $g$ (root-blind); the antisymmetric part carries Lemma 2's root-resolving content.

**Part IV: theorem.** The torsion-free connection keeps "the 16 shared + 24 TetA" and drops "24 TetB". So $16 + 24 = 40\ne64$: "a tetrahedron is not a stellated octahedron", and the torsion-free connection is a projection, not a rewrite.

**Notes.**
- *Labelling.* Read as vertices, the columns of $M_1$ are the odd-popcount corners, which agrees with Paper IX. In L1 the same four vectors are the *face normals* of the region TetA $=\{\max v_i\le1\}$, whose vertices are the even corners. So GRAM's TetA, as a solid, is L1's TetB region. The pair is the same and only the "A" label flips.
- *Upper vs lower.* Calling the strict upper triangle "TetA" and the strict lower "TetB" is a bookkeeping choice. What the torsion-free condition removes is the six antisymmetric combinations $\tfrac12(\Gamma_{\mu\nu} - \Gamma_{\nu\mu})$ per slice, which are not the lower-triangle entries themselves. The counts are unaffected.

## TF — Tully–Fisher Velocity Evolution from Dual-Tetrad Gravity (RevTeX manuscript, Feb 2026)

*Manuscript. Figure from GRAVIS (github.com/fielddynamics/gravis). Status: [O] comparison using [D]/[E] inputs. It is the longer sibling of Paper X.*

**Framework (older vocabulary).**
- *Waves and simplex.* LIGO waves imply local structure. The simplex theorem gives $k = 4$.
- *Faces.* Of the $k\cdot d = 12$ nearest-neighbour couplings, 4 are active faces and 8 are "topologically closed". Each face's two transverse deformation modes are read as the + and × polarisations.
- *Two chambers, four routes:* ghost stability, the SL(2,C) double cover, chirality (Ashtekar; Alexander–Marcianò–Smolin), and Hassan–Rosen.
- *Polynomial.* $f(k) = 1 + k + k^2 = 21$, read as vertex + faces + face pairs.
- *Constants and action.* $G = (17/13)\alpha^{21}\hbar c/m_e^2$, here with $13 = k^2 - k + 1$ (equal to $kd+1$ at $k = 4$). $a_0 = k^2Gm_e/r_e^2$. The action is the four-term SST, with the $e^{-2\Phi/c^2}$ factor called "the disformal coupling", whose 2 counts the two orientations.
- *Equivalence asserted.* The action is said to be equivalent to the bimetric completion with $\beta = (1,0,16,0,1)$. VIII and IX list the explicit match as open.

**Prediction.**
- $a_0 = (cH/2\pi)\sqrt{k/\pi}$. Its agreement with $k^2Gm_e/r_e^2$ "to within 0.3%" is reproduced: at $H = 70.0$ it gives $1.2214\times10^{-10}$ against $1.2250\times10^{-10}$.
- $v^4 = GMa_0$ gives a naive exponent of ¼. Photon-path screening through the disformal coupling, governed by $\sqrt{k/\pi}$ and $\mathcal F$, gives the stated 0.17. The derivation is cited, not shown.
- The table is identical to Paper X's (χ² = 0.34 for 8). Band ±6.2% from $(k/\pi)^{1/4}$, explained as "flat faces vs spherical curvature, correction $(k/\pi)^n$ with $n = ¼$ for velocity scatter".
- $H_0 = 70.29$: the tree-level 70.21 times the Schwinger one-loop factor carried through $G\to a_0\to H$. Band 66.2–74.7 (recomputed 66.17–74.67).
- Futures: $z = 4$ gives 1.36, $z = 5$ "≈ 40%" (recomputed 1.427). JWST NIRSpec and Euclid.

**Notes.**
- *Graviton mass.* The manuscript says GFD "predicts a specific mass for the massive graviton, determined by the five $\beta_n$". In Hassan–Rosen the graviton mass also scales with the overall $m^2$ in $m^2\sum\beta_ne_n$ (and with the Planck-mass ratio). Fixing the $\beta_n$ fixes ratios but not $m$, and no paper in the series gives $m$. So the mass is not yet predicted.
- *Coupling name.* $e^{-2\Phi/c^2}F_{\mu\nu}F^{\mu\nu}$ is a field-dependent factor on the Maxwell term. TF and ESS call it "disformal"; the L3 supplement calls it conformal and assigns it a different role. The documents disagree on what the term does (see Part I §3).

## ESS — GFD Essentials: Tetrads, Field Closure, and the Inverse Pipeline

*Primer for relativists, Feb 2026. Status: [D] summary; it cites Nelson 2026 (DEC) for the postulates.*

**Path in ten steps.**
1. GR uses tetrads, and LIGO shows local coupling (the wave equation's Laplacian compares neighbours).
2. Non-degeneracy, $\det e\ne0$, means four independent directions, hence a tetrahedral chamber. This is linked to ADM $1+3$ and to condensed-matter tetrahedral coordination.
3. Packing: of 12 sphere-packing contacts, 4 are open and 8 closed. The analogies are water's four H-bonds and Plateau's tetrahedral foam junctions (Taylor 1976).
4. A single orientation is ghost-unstable (Alexander 2014). Hassan–Rosen, spinors and chirality give two tetrahedra, the stellated octahedron, with the Field Origin at its centre.
5. Field closure is the ongoing enforcement of a closed, non-degenerate frame.
6. The postulates A1 (local closure), A2 (lossless transmission) and A3 (one scale $a_0$) give $\mu = x/(1+x)$. The 1 in the denominator comes from sector symmetry: $\mu(x) + \mu(1/x) = 1$ for $x/(n+x)$ only if $n = 1$.
7. The four-term action, with $F$ obtained by integration. Limits: $F\to y$; $F\to\tfrac23y^{3/2}$.
8. The spherical static limit gives "two field equations": Poisson $\nabla^2\Phi = 4\pi G\rho$ (source) and $g_s = g_t^2/(a_0+g_t)$ (response).
9. Inverse: $v\to g_t\to g_s\to M_{\rm dec} = rv^4/[G(a_0r + v^2)]$. This is "the spherical field equation and Poisson together, not Poisson alone" (Poisson alone would give $v^2r/G$).
10. $\Delta M_{\rm eff} = M_{\rm phot} - M_{\rm dec}$ is the drain's power output.

**Notes.**
- *Lensing.* ESS says the EM term "recovers the full gravitational lensing … without this term, lensing would be half". The L3 covariant-completion note says the opposite: $\gamma = 1$ comes from the single-potential connection structure, and the EM term has no lensing role. The later note is the more careful one, so Part I §3 follows it.
- *Symbol.* ESS writes Poisson with the same symbol $\Phi$ used for the total potential in the action. In the pipeline, Poisson defines the Newtonian source field $g_s$, so the $\Phi$ there is $\Phi_N$. Varying the action gives one equation, $\nabla\cdot[\mu\nabla\Phi] = 4\pi G\rho$, whose spherical form is the quadratic.
- *Naming.* The terminology matches the later rules: "spherical field equation of the scalar-tensor transition (SST) action".
- *Deficit sign.* ESS repeats DEC's deficit-sign ambiguity.

## Paper A — The Simple AQUAL Interpolation Law from the Tetrad Frame's Bilinear $\mathbb Z_2$ Sector

*Algebraic note. Status: [T]. Scope is stated narrowly: no covariant completion, no optical metric, no prediction of $G$. "No acceleration scale is smuggled in": $x$ is an algebraic odds variable until it is replaced by $|\nabla\Phi|/a_0$.*

**Sector space.**
- $V$ is the frame space, $K = \dim V = 4$, and $\det e\ne0$. The tetrad equation is bilinear in $e$. Read by frame degree it has three levels, $\mathcal C_K = \Lambda^KV\oplus V\oplus(V\otimes V)$, of dimensions $1 + K + K^2$.
- There is no rank-3 level: that would need trilinear dependence on $e$. Independently, $`\Gamma^a{}_{bc}`$ has only two lower indices, so it also stops at bilinear.
- Weighting $\Omega_s = I\oplus sI_V\oplus I$ gives the theorem $\mathrm{Tr}_{\mathcal C_K}\Omega_s = f(K,s) = 1 + sK + K^2$, i.e. 13/17/21 at $K = 4$.
  - The leading 1 is $\dim\Lambda^KV$.
  - $s = 0$ is the unpolarised average of the $s = \pm1$ reads, not a third eigenvalue.
- *Swap form.* $\tau(a\otimes b) = b\otimes a$ with $P_\pm = \tfrac12(I\pm\tau)$ and $\mathrm{Tr}\tau = K$, so $f = \dim\Lambda^KV + \mathrm{Tr}_{V\otimes V}(I + s\tau)$.
- *Connection.* $`\Gamma\in V\otimes V^*\otimes V^*`$ (the frame affine connection, not the spin connection) splits as $`V\otimes\mathrm{Sym}^2V^*`$ (40) $\oplus$ $`V\otimes\Lambda^2V^*`$ (24). Torsion is $`\Lambda^2V^*`$-valued, with $`T^a{}_{bc} = 2\Gamma^a{}_{[bc]}`$ in a coordinate basis.
- *Two gradings, four sectors.*

  | Parity, swap | Sector | Dimension |
  |---|---|---|
  | (+,+) | $\Lambda^KV\oplus\mathrm{Sym}^2V$ | 11 |
  | (+,−) | $\Lambda^2V$ | 6 |
  | (−,+) | $V$ | 4 |
  | (−,−) | — | 0 |

  Total 21.

**Occupation law.**
- Exchange $\mathrm{Sym}^2\leftrightarrow\Lambda^2$ acts as $x\mapsto1/x$, so $u(x) + u(1/x) = 1$, with $u(0) = 0$, $u(1) = \tfrac12$, $u(\infty) = 1$. Here $u$ is the symmetric-sector (Christoffel-side) fraction.
- A fractional-linear $u$ with these three values is $x/(1+x)$.
- *Stated caveat.* The family $x^n/(1+x^n)$ obeys the same exchange symmetry for every $n>0$. $n = 1$ is singled out by fractional-linearity, equivalently by taking $x$ to be the odds $u/(1-u)$ itself. The remark is explicit that given that identification, $u = x/(1+x)$ is just odds → probability. The content is the identification of the tetrad's bilinear $\mathbb Z_2$ split as the relevant partition.
- *Coordinates.* $s(x) = 2u - 1 = (x-1)/(x+1)$ is the Cayley coordinate; separately, it is the unique fractional-linear $s$ with $s(1/x) = -s(x)$, $s(1) = 0$, $s(0) = -1$, $s(\infty) = 1$. Then $f(K,s(x)) = f_- + 2Ku(x)$.
- *Density operator.* $\rho_x = uP_+ + (1-u)P_-$ satisfies $\rho_x + \rho_{1/x} = I$. The weighted count $N_K(x) = K^2(K-1)/2 + K^2u(x)$ satisfies $N_K(x) + N_K(1/x) = K^3 = 64$. This is called an algebraic identity, not a conservation law.

**Primitive.**
- $y = x^2$ and $F'(y) = u(\sqrt y)$, $F(0) = 0$, give $F = y - 2\sqrt y + 2\ln(1+\sqrt y)$, which is $C^1$ on $[0,\infty)$ and $C^\infty$ on $(0,\infty)$.
- $F\sim\tfrac23y^{3/2}$ from cancellation of the linear and quadratic orders. The Euler–Lagrange equation is understood weakly at critical points (Bekenstein–Milgrom).
- Realisation: $S_{\rm NR} = \int d^3x[-(a_0^2/8\pi G)F - \rho\Phi]$ gives $\nabla\cdot[u\nabla\Phi] = 4\pi G\rho$ (the sign is checked).

## Paper B — Torsion as the Regular Representation of $S_4$

*Algebraic note. Status: [T]. Recomputed: characters and both multiplicity decompositions.*

- *Action.* $S_4$ acts on the four frame labels before any metric (pre-$\eta$). The character counts fixed labels, and $`V^*\cong V`$ as $S_4$-modules.
- *Characters.* $\chi_{\Lambda^2V} = (\chi^2 - \chi(\sigma^2))/2$. On the classes (e, (12), (123), (1234), (12)(34)) of sizes (1, 6, 8, 6, 3):
  - $\chi_V = (4,2,1,0,0)$.
  - $\chi_{\Lambda^2} = (6,0,0,0,-2)$.
  - $\chi_{V\otimes\Lambda^2} = (24,0,0,0,0)$.
- *Theorem.* The torsion sector $`V\otimes\Lambda^2V^*`$ is the regular representation of $S_4$ ($\chi = |G|$ at $e$, 0 elsewhere). So it contains each irrep with multiplicity equal to its dimension: $1+1+4+9+9 = 24$. Recomputed: triv 1, sgn 1, $V_2$ 2, $V_3$ 3, $V_3\otimes$sgn 3.
- *Christoffel sector.* $V\otimes\mathrm{Sym}^2V$ has $\chi = (40,8,1,0,0)$ and decomposes as $4\cdot\mathbf1\oplus3V_2\oplus7V_3\oplus3(V_3\otimes\mathrm{sgn})$, with **zero** sign copies. Recomputed: confirmed.
- *Reading.* The sign irrep, the unique scalar detector of odd versus even leg permutations, lives only in torsion. This is a module-theoretic form of root-blindness.
- *Uniqueness.* $K^2(K-1)/2 = K!$ only for $K\in\{2,4\}$ (table $K = 1..6$).
- *Combinatorics.* $4\times6 = 24$ vertex–edge incidences of a tetrahedron, equal to $|S_4|$.
- *Stated limits.*
  - $\eta$ breaks $S_4$ to about $S_1\times S_3$.
  - How this relates to the Lorentz split $4 + 4 + 16$ is open.
  - The explicit isomorphism to $\mathbb R[S_4]$ is not constructed.

## Paper C — The Hadamard Kernel of the Tetrad Frame and the Stellated Octahedron

*Algebraic note. Status: [T].*

- *Parity split.* $p = xyz$ splits the cube into TetA ($p = +1$: $(+++), (+--), (-+-), (--+)$) and TetB ($p = -1$). Within a set the pairwise inner product is $-1$, so each set is a regular tetrahedron.
- *$H_4$.* The three balanced 2|2 partitions of four objects ($\binom42/2 = 3$) plus the constant row give $H_4$, with $H_4H_4^T = 4I$.
- *Theorem 1.* Reading the signs of the four normals $u_0..u_3$ along $x, y, z$ gives the three balanced partitions; adding the constant (temporal) row gives $H_4$.
- *Theorem 2 (parity-restricted Walsh kernel).* On $T_+$, $1\sim xyz$, $x\sim yz$, $y\sim xz$, $z\sim xy$. Eight Walsh characters collapse to four, $\{1,x,y,z\}$, whose values on $T_+$ form $H_4$.
  - Sylvester: $H_8\cong H_2\otimes H_4$, i.e. parity grading ⊗ frame read.
- *Tetrad.* The isotropic frame $`e^I{}_j = u_I^j/\sqrt3`$ has $H_4$ as its sign skeleton, with the time leg giving the constant row.
- *Uniqueness at $D = 3$.* Three facts hold together only there:
  - balanced partitions $= D$ only at $K = 4$ ($K = 3$ gives 3/2; $K = 5$ gives 5 ≠ 4);
  - $2(D+1) = 2^D$;
  - a Hadamard matrix of order $K>2$ needs $4\mid K$.
- *Open.* Whether the three appearances of 3 + 1 (Walsh modes, face signs, Lorentz signature) are one fact.
- **Notes.**
  - *Axes.* The text says the three axes connect "opposite edge-midpoints of the cube". The axes used ($x, y, z$) pass through the cube's face centres, which are the midpoints of opposite edges *of each tetrahedron*.
  - *Labelling.* Paper C calls $u_0..u_3$ both TetA's vertices and TetA's face normals. That is consistent only for inward normals, which is the source of the TetA/TetB label flip relative to L1 (Part I §2.2).

## FY — Closed-Form AQUAL Energy Functional for the Simple Interpolating Function

*Short note. Status: [T].*

- *Theorem.* $\mu = x/(x+1)$ with $F(0) = 0$ gives $F = y - 2\sqrt y + 2\ln(1+\sqrt y)$. Proof: $u = \sqrt t$, $u^2/(u+1) = (u-1) + 1/(u+1)$.
- *Check by differentiation in $u$.* $dF/du = 2u^2/(1+u)$, so $dF/dy = u/(1+u)$. This is regular at $u = 0$.
- *Limits.* $F\to y$; $F = \tfrac23y^{3/2} - \tfrac12y^2 + O(y^{5/2})$. The crossover is smooth, with no patching.
- *Novelty claim.* "No closed form for the corresponding $F(y)$ appears in the published literature". Not checked here.
- **Notes.**
  - *Abstract vs body.* The abstract says "the logarithm dominates at low acceleration and produces deep-MOND scaling, and the square root provides smooth crossover". The body (§5–6) correctly shows the deep-field $y^{3/2}$ arises only after the $\sqrt y$ and $y$ orders cancel among all three terms. The abstract's term-by-term roles do not hold.
  - *Sign.* The note writes $\mathcal L = -(a_0^2/8\pi G)F + \rho\Phi$. Varying that gives $\nabla\cdot[\mu\nabla\Phi] = -4\pi G\rho$. The stated field equation needs $-\rho\Phi$, as Paper A writes.

## The six formal proofs (`proofs/`)

*All six verification scripts were re-run: aqual 24/24, exchange 34/34, forced frame 27/27, Hadamard 25/25, scheme 39/39, torsion 36/36, 185 checks in all. Each proof lists its premises and shows them necessary by counterexample.*

**P-aqual — The Energy Functional of $\mu = x/(x+1)$.**
- $\mathcal L = -(a_0^2/8\pi G)F - \rho\Phi$.
- Thm 1: $F$ is the unique $C^1$ primitive with $F(0) = 0$.
- Cor 1 gives the convergent series:
  - $F = 2\sum_{k\ge3}(-1)^{k+1}y^{k/2}/k$ for $y\le1$;
  - $F = y - 2\sqrt y + \ln y + 2\sum_{k\ge1}(-1)^{k+1}y^{-k/2}/k$ for $y>1$.
- Deep field: $\nabla\cdot(|\nabla\Phi|\nabla\Phi) = 4\pi Ga_0\rho$.
- Thm 2:
  - With $W(q) = F(|q|^2)$, $W\in C^2$ and the Hessian is $2\mu(I - \hat q\hat q^T) + 2(x\mu)'\hat q\hat q^T$, with $2(x\mu)' = 2x(x+2)/(x+1)^2$.
  - So $W$ is strictly convex and $A(p) = \mu(|p|/a_0)p$ is strictly monotone.
  - $1 < (x\mu)'/\mu = (x+2)/(x+1)\le2$; the equation degenerates only at $\nabla\Phi = 0$.
- Cor 2: uniqueness for Dirichlet data on bounded domains. The whole-space case is not treated.

**P-exchange — The Constitutive Law from Exchange Symmetry.**
- Premises:
  - (E) $\mu(0) = 0$.
  - (X) Partition states are closed under parity. Parity fixes $|g|$, so if $\mu$ occurs then $1-\mu$ occurs.
  - (A) $P(\tilde x,\mu) = 0$ irreducible, of degree 1 in each variable. The degree in $\mu$ "counts the directions in which the coupling runs".
- Lemma (field degrees with Gauss): $y\in K(x)$ and $x\in K(y)$ iff $P = axy + bx + cy + d$ with $ad\ne bc$.
- Steps:
  1. Bilinearity gives $\Omega = \alpha\tilde x/(\gamma\tilde x + \delta)$.
  2. (X) requires a pole on $[0,\infty]$ without a sign change, so $\gamma = 0$.
  3. Setting the unit gives $\Omega = x$.
- The exchange $x\to1/x$ is *derived*, and $a_0$ is its fixed point (identified, not evaluated). $\mu(\infty) = 1$ and the complement symmetry are also derived.
- Parity form: $s = 2\mu - 1$ gives $x(1-s) = 1+s$, with exchange $(x,s)\to(1/x,-s)$.
- Necessity:
  - drop (E): $\Omega = (x+b)/(bx+1)$;
  - drop (X): $\mu(\infty)<1$;
  - drop (A): $x^n(1-\mu)^m = \mu$, irreducible by Eisenstein, where $(1,2)$ is the bound law;
  - without (A), any increasing $\mu$ works.
- Wording note: (A) is motivated by "the unbound field couples in one direction: matter sources the field, and the field does not source itself". "Unbound field" here means the field sourced one way. Under the naming rules this is the one-directional law that governs a galaxy's exterior, not an "unbound galaxy".

**P-forced — The Spatial Geometry of the Lorentz Tetrad.**
- Premises: (R) equal pairwise relation (the pattern of $\eta_{a\ne b} = 0$); (M) equal magnitude ($|\eta_{aa}| = 1$, so the sign of $\eta_{00}$ is set aside); (N) distinct legs; (D) $D = 3$.
- Rigidity lemma: equal Gram matrices of rank $D$ differ by a unique $Q\in O(D)$.
- Theorem: $G = c^2I - (c^2/3)(J-I)$ and closure $\sum v_a = 0$ are *derived*, giving the regular tetrahedron with angle $\arccos(-1/3)$, unique up to $O(3)$.
- Cor 2: $K$ legs can be realised iff $D\ge K-1$, and are forced iff $D = K-1$.
- Cor 3: parity $-I$ gives the disjoint second tetrahedron, and the eight points are the cube, i.e. the stella octangula.
- Necessity:
  - drop (R): a square;
  - drop (M): the observer's projection $v_0 = 0$, $v_i = c\hat e_i$, or $G_{aa} = (1,3,7,7)c^2$;
  - drop (N): $G = c^2J$;
  - drop (D): orthogonal legs in $\mathbb R^4$, and nothing in $\mathbb R^2$.
- The paper states that premise (M) is the decisive interpretive choice.

**P-hadamard — The Stellated Octahedron, the Cube and the Hadamard Matrix.**
- Thm 1: for a $D\times K$ sign matrix these are equivalent:
  - the columns are a cube simplex;
  - $M^TM = KI - J$;
  - $\hat H = \binom{\mathbf1^T}{M}$ is Hadamard;
  - $M\mathbf1 = 0$ and $MM^T = KI_D$ (no net direction, no preferred axis).
- Hadamard lemma: $4\mid n$ for $n>2$, so cube simplices exist only for $D = 1$ or $4\mid D+1$.
- Thm 2: $V\cup(-V) = Q_D$ iff $D = 3$, where they are the classes $x_1x_2x_3 = \pm1$. This is exactly what $2(D+1) = 2^D$ counts.
- Thm 3: in a stated ordering, $W_8 = H_2\otimes\hat H$ exactly, with $H_2$ as parity.
- Cor 2: the $K-1$ rows are all the equal-half splits only for $K = 2, 4$.

**P-two-regions — The Tetrad Scheme and the Two Bounded Regions.**
- The solution set of $g = e^T\eta e$ is the $O(1,3)$-orbit of one tetrad. The scheme $X_g\cong O(\eta)$.
- $(\det e)^2 = \det g/\det\eta = \kappa>0$, so $X_g = X_+\sqcup X_-$. Neither piece splits further, since $SO(4,\mathbb C)$ is connected.
- $P$ and $T$ (both det −1) exchange the pieces; $PT = -I$ does not. For a fixed future-pointing time leg the root is the orientation of the spatial legs, i.e. $O(3)$'s two components.
- $P = -I$ is canonical: it is the only det −1 element central in $O(3)$, and not a rotation leg by leg. The construction needs odd $D$.
- *Cautions stated.*
  - As unlabelled point sets the two tetrahedra are congruent (a 90° rotation maps one onto the other). They differ in leg order and occupied region.
  - The root ↔ tetrahedron identification needs future-pointing frames.
- Every metric-built quantity (Christoffels, curvature, Einstein tensor, EH action) is the same on both pieces. Keeping one piece is "a valid computational choice" ($SO^+(1,3)$), equivalent to adding $\det e = +\sqrt\kappa$.
- Each piece carries a 3 + 1 face split relative to the spatial legs: one uniform-sign normal ($(+++)$ or $(---)$) and three mixed.

**P-torsion — The Torsion Sector as the Regular Representation of $S_4$.**
- Lemma: the torsion basis $t_{a;bc}$ forms two orbits of 12, incident ($a\in\{b,c\}$) and non-incident. Both have stabiliser $\langle(23)\rangle$, acting by $\pm1$.
- Thm 1: the 24 images of $\xi = t_{0;01} + t_{0;23}$ are a basis, so $\mathbb R[S_4]\cong T$ explicitly. Also $T_{\rm inc} = \mathrm{Ind}_H\mathbf1$ and $T_{\rm non} = \mathrm{Ind}_H\varepsilon$.
- Thm 2: sgn occurs once in $T$ (spanned by $\sum_d\varepsilon_{abcd}$, in $T_{\rm non}$) and never in $C$. In $C$ every one of the four orbits has a stabiliser containing a transposition acting by +1.
- Thm 3, using $|\eta| = I$:
  - $T_v\cong V = \mathbf1\oplus\mathrm{std}$, inside the incident half.
  - $T_{ax}\cong\mathrm{sgn}\otimes V$, inside the non-incident half.
  - Each half of the tensor part is $[2,2]\oplus\mathrm{std}\oplus(\mathrm{sgn}\otimes\mathrm{std})$.
  - With the signed $\eta$ the axial part is not $S_4$-invariant.
- This answers Paper B's two open questions: the explicit isomorphism, and the relation to the Lorentz split $4 + 4 + 16$.
- Scope, as stated:
  - sgn$(\sigma) = \det P_\sigma$, the orientation character on leg permutations.
  - Spatial parity is not a leg permutation, and these theorems do not describe its action. So the link between the sign irrep and TetA/TetB root-blindness is by analogy, through orientation (Part I §5.3 updated).
