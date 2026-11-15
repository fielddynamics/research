# Vortices in the Pixel: Theorem, Proof and Certificates

*Field Dynamics Research, research folder, 2026-11-15. Supersedes the statements in [`../pixel-vortex/PROOF.md`](../pixel-vortex/PROOF.md) and [`../triforce-vortex/PROOF.md`](../triforce-vortex/PROOF.md) where they differ; see the correction in §6.*

**How this is verified.** Every claim below is either proved by hand in this document or certified exactly by a computation that anyone can rerun. Three independent pieces of code do the checking:

| Script | Method | Result |
|---|---|---|
| [`certify_vortices.py`](certify_vortices.py) | Pure Python, exact arithmetic in $\mathbb Q(i)$ and $\mathbb Q(\omega)$ with fractions; no computer-algebra system; geometry, symmetry group and Hamiltonians built from scratch | 54/54, [output](certify_output.txt) |
| [`analyse_W.py`](analyse_W.py) | sympy, symbolic in all parameters | 5/5, [output](analyse_W_output.txt) |
| [`pixel_flux_closed_form.py`](pixel_flux_closed_form.py) | sympy, symbolic in all parameters | closed form confirmed, [output](pixel_flux_output.txt) |

The earlier scripts [`../pixel-vortex/verify_pixel_vortex.py`](../pixel-vortex/verify_pixel_vortex.py) (28/28) and [`../triforce-vortex/verify_triforce_vortex.py`](../triforce-vortex/verify_triforce_vortex.py) (15/15) give a further, separate implementation of Parts I–II.

---

## 1. Setting and definitions

**The two models.**

| | Pixel model $\mathcal P$ | Triforce model $\mathcal T$ |
|---|---|---|
| Sites | 15: the Field Origin $O$; the octahedron's 6 vertices (the cube's face centres); the cube's 8 corners (TetA: $xyz = +1$; TetB: $xyz = -1$) | 33: $O$; the 8 central tiles (medial triangles of the 8 tetrahedron faces, which are the octahedron's faces); the 24 outer tiles (3 per face). A tile's position is its centroid |
| Bonds | $O$ to each octahedron vertex and to each corner; each octahedron vertex to the 4 corners of its face | Two tiles that share an edge; each central tile to $O$ |

**The class of Hamiltonians.**
- $H$ is a real symmetric matrix on the sites, nonzero only on the diagonal and on bonds.
- $H$ is invariant under the tetrahedral group $T_d$ (24 elements, the symmetries that keep TetA and TetB). So TetA and TetB may be treated differently, which is the case whenever $x \neq 1$.
- Equivalently, $H$ has one free real parameter per $T_d$-orbit of sites and of bonds. $\mathcal P$ has 9 such orbits (4 site, 5 bond), and $\mathcal T$ has 15 (5 site, 10 bond). Every theorem below is stated for this whole class.

**Axes and their symmetries.**
- In $\mathcal P$, the axis is an octahedron axis $\hat z$. Its symmetry is the rotoreflection $S$: a quarter turn followed by a top–bottom flip, of order 4.
- In $\mathcal T$, the axis is a leg $\hat n = (1,1,1)/\sqrt3$. Its symmetry is the rotation $C$ by $120°$, of order 3.
- Both lie in $T_d$, so both commute with every $H$ in the class.

**Definitions.**
- **Winding state.** A vector $\psi$ with $S\psi = \lambda\psi$ (or $C\psi = \lambda\psi$), where $\lambda$ is a primitive root of unity: $\lambda = \pm i$ for $S$, and $\lambda = \omega^{\pm1} = e^{\pm 2\pi i/3}$ for $C$. Along every orbit of the symmetry, the phase of such a vector advances by $\arg\lambda^{-1}$ per step, so it winds exactly once per turn.
- **Bond current.** For a stationary state, $H\psi = E\psi$, the current on the bond $i \to j$ is $J_{ij} = 2\,\mathrm{Im}(\bar\psi_i H_{ij}\psi_j)$.
- **Circulating current $I(\psi)$.** The total current crossing a half-plane bounded by the axis, counted positive in the right-handed sense about the axis. By Lemma 2 it does not depend on which half-plane is used.
- **Vortex.** A stationary winding state with $I(\psi) \neq 0$.

## 2. General lemmas (proved by hand)

**Lemma 1 (current conservation).** If $H\psi = E\psi$ with $H$ real symmetric, then $\sum_j J_{ij} = 0$ at every site $i$.

*Proof.* $\sum_j J_{ij} = 2\,\mathrm{Im}\big(\bar\psi_i (H\psi)_i\big) - 2\,\mathrm{Im}\big(H_{ii}\lvert\psi_i\rvert^2\big) = 2\,\mathrm{Im}\big(E\lvert\psi_i\rvert^2\big) - 0 = 0$. ∎

**Lemma 2 (the axis is empty, so the circulating current is well defined).**
- Every winding state vanishes at every site on the axis.
- Hence, for a stationary winding state, the current crossing any half-plane bounded by the axis is the same for every such half-plane.

*Proof.* A site on the axis lies in an orbit of the symmetry whose length is less than its order ($O$ is fixed; in $\mathcal P$ the axial octahedron vertices form an orbit of length 2). On an orbit of length $\ell$, $\psi(x) = \lambda^\ell\psi(x)$ with $\lambda^\ell \neq 1$, so $\psi = 0$ there. Bonds touching an axis site therefore carry no current.

Take two half-planes and the region between them. By Lemma 1, the net current out of that region is zero. No current enters or leaves through the axis. So the current through the two half-planes is equal. ∎

*(Certificates: "axis sites lie in shorter orbits", "every winding vector vanishes on the axis", and C4, the flux is equal for three different half-planes in every case.)*

**Lemma 3 (antivortices).** If $\psi$ is a stationary winding state with eigenvalue $\lambda$, then $\bar\psi$ is a stationary winding state with eigenvalue $\bar\lambda$, at the same energy, and $I(\bar\psi) = -I(\psi)$.

*Proof.* $H$ is real, so $H\bar\psi = E\bar\psi$. The symmetry is a real permutation, so $S\bar\psi = \bar\lambda\bar\psi$. Finally $J_{ij}(\bar\psi) = 2\,\mathrm{Im}(\psi_i H_{ij}\bar\psi_j) = -J_{ij}(\psi)$. ∎ *(Certificate C7.)*

**Lemma 4 (existence).** $H$ preserves the winding space $V_\lambda$, so $V_\lambda$ has an orthonormal basis of stationary winding states. $\dim V_\lambda$ equals the number of full-length orbits: 3 in $\mathcal P$, 10 in $\mathcal T$.

*Proof.* $H$ commutes with the symmetry, so it preserves each eigenspace. The basis vectors of the orbits ($v[S^jx_0] = \lambda^{-j}$) span $V_\lambda$. ∎ *(Certificates: dimension, orthogonality, eigenvalue.)*

## 3. Theorem A: the pixel (all parameters, explicit exceptions)

In the basis (ring, TetA corners, TetB corners) of $V_{+i}$, every $H$ in the class acts as
$$H_+ = \begin{pmatrix}\Delta_f & a & b\\ \bar a & \epsilon_A & 0\\ \bar b & 0 & \epsilon_B\end{pmatrix},\qquad a = -c_A(1+i),\ \ b = -c_B(1+i).$$
Here $\Delta_f$ is the octahedron-vertex energy, $\epsilon_{A,B}$ are the corner energies, and $c_{A,B}$ are the octahedron-vertex-to-corner couplings.

**Theorem A.** Let $c_Ac_B \neq 0$ and $\epsilon_A \neq \epsilon_B$. Then:
1. **Three vortex energies.** There are exactly three stationary winding states with $\lambda = +i$, with distinct energies, the roots of $E - \Delta_f = \dfrac{2c_A^2}{E-\epsilon_A} + \dfrac{2c_B^2}{E-\epsilon_B}$. By Lemma 3 there are three antivortices.
2. **Corners locked to the ring.** Each state has ring amplitude $r \neq 0$, with the corners locked to it: $p = \bar a r/(E - \epsilon_A)$, $q = \bar b r/(E - \epsilon_B)$.
3. **The current in closed form.** The circulating current is $I = -\tfrac14(E - \Delta_f)\lvert r\rvert^2$.
4. **Every state circulates.** Each is a vortex, $I \neq 0$, unless $E = \Delta_f$. That happens only when $c_A^2(\Delta_f - \epsilon_B) + c_B^2(\Delta_f - \epsilon_A) = 0$.
5. **TetA = TetB.** At $\epsilon_A = \epsilon_B$, one of the three has $r = 0$ and $I = 0$.

*Proof.*
- **The ring row.** The ring row of $H_+w = Ew$ gives $ap + bq = (E - \Delta_f)r$, and the corner rows give the expressions for $p$ and $q$.
- **No energy equals a corner energy.** $\det(H_+ - E)$ equals $2c_A^2(\epsilon_A - \epsilon_B)$ at $E = \epsilon_A$ and $2c_B^2(\epsilon_B - \epsilon_A)$ at $E = \epsilon_B$, both nonzero. So $E \neq \epsilon_{A,B}$, and $r = 0$ would force $p = q = 0$.
- **Distinct roots.** The secular function is strictly increasing between its poles, so the three roots are distinct.
- **The current.** Substituting into the half-plane current gives $-r^2\,[c_A^2(E-\epsilon_B) + c_B^2(E-\epsilon_A)]\,/\,[2(E-\epsilon_A)(E-\epsilon_B)]$. The secular equation reduces this to $-\tfrac14(E-\Delta_f)r^2$, the same for all three half-planes tested ([`pixel_flux_closed_form.py`](pixel_flux_closed_form.py)).
- **Item 5.** At $\epsilon_A = \epsilon_B$, $E = \epsilon_A$ is a root with $r = 0$. ∎

*(Independent exact certificates at three random rational parameter points: C3 squarefree, C5 current nonzero, C6 ring turning. Also [`../pixel-vortex/verify_pixel_vortex.py`](../pixel-vortex/verify_pixel_vortex.py).)*

**Corollary A′ (the octahedron is what circulates).** Without the octahedron (9 sites: $O$ and the corners), winding states exist, but every bond touches $O$, where they vanish. So $I = 0$ for all of them: there are no vortices.

## 4. Theorem B: the Triforce (exact decomposition; generic statements certified)

**Theorem B.** In $\mathcal T$, with $\lambda = \omega$ about a leg:
1. **Existence, for all parameters.** $V_\omega$ has dimension 10. Every vector in it vanishes on the leg: at $O$ and at the two central tiles on the leg (Lemmas 2 and 4).
2. **An exact split, for all parameters.** $V_\omega = W \oplus W'$, an orthogonal sum of two subspaces, each preserved by every $H$ in the class.
   - $W$ (dimension 4) consists of winding vectors on outer tiles that no parameter couples to any central tile. It is a fixed subspace, the same for all $H$.
   - $W'$ (dimension 6) is its orthogonal complement.
3. **$W$: doubled energies, for all parameters.** $H$ acts on $W$ as two copies of the same $2\times2$ problem, so every energy on $W$ is doubled. On a doubled level, the circulating current is a $2\times2$ Hermitian form, with positive-definite Gram matrix. Whether every combination circulates depends on the parameters. Its determinant, reduced on the level, is $243\,t_3t_5^2t_7\,\ell(E)$, with $\ell$ linear in $E$. Over 40 random rational parameter points (78 levels, exact roots): 36 levels circulate in every combination, 40 contain a standing combination, and 2 lie exactly on the boundary between the two.
4. **$W'$: six vortices, generically.** For all parameters outside a proper algebraic subset of parameter space (a closed set of measure zero), $H$ on $W'$ has six distinct energies, and each of the six stationary states:
   - is a vortex, $I \neq 0$;
   - has nonzero weight on the three outer tiles of the star point at $(1,1,1)$, so its ring turns.

   By Lemma 3, the conjugates are six antivortices.

*Proof of 4 (exact certificate argument).*
- **Polynomials in the parameters.** $W$ is fixed, so in a fixed basis of $W'$, $A' = W'^\dagger H W'$ depends linearly on the parameters, and the Gram matrix $G$ is constant. So $p(x) = \det(xG - A')$, $f(x) = \mathrm{Tr}\big(K\,\mathrm{adj}(xG - A')\big)$ ($K$ the half-plane current form) and $g(x) = \mathrm{adj}(xG - A')_{\rm ring,ring}$ all have coefficients that are polynomials in the parameters.
- **Reduction to the roots.** For a simple root $E$ with eigenvector $y$, $\mathrm{adj}(EG - A') = \tfrac{p'(E)}{y^\dagger G y}\,yy^\dagger$. So $I(y)/\lVert y\rVert^2 = f(E)/p'(E)$, and the ring weight is $g(E)/p'(E)$.
- **Three resultants.** The claims hold wherever the three resultants $\mathrm{Res}(p, p')$, $\mathrm{Res}(p, f)$ and $\mathrm{Res}(p, g)$ are nonzero. Each is a polynomial in the parameters.
- **Certification.** `certify_vortices.py` shows, by exact gcd computations in $\mathbb Q(\omega)$, that all three are nonzero at three random rational parameter points. A polynomial that is nonzero at one point is not identically zero, so its zero set is a proper algebraic subset.
- **The current is well defined.** That the current is the same for three half-planes is certificate C4 ($p$ divides each difference). ∎

## 5. What is proved, and what is not

**Proved.**
- **Pixel (all Hamiltonians in the class).** About each octahedron axis there are exactly three vortices and three antivortices, with explicit exceptions. They circulate a current $I = -\tfrac14(E - \Delta_f)\lvert r\rvert^2$ through the octahedron, around an empty axis, with the corners locked to the octahedron's ring. Without the octahedron nothing circulates.
- **Triforce.** About each leg, the winding space splits exactly into $W'$ and $W$.
  - On $W'$, six vortices, generically. Each turns the star point's three outer tiles around an empty core that runs through the central tiles and the Field Origin.
  - On $W$, doubled levels whose circulation depends on the parameters.

**Not claimed.**
- That the GFD field occupies any of these states.
- That these tight-binding models are the field's dynamics. They are the most general $T_d$-invariant nearest-neighbour models on the stated graphs, and the theorems are about that class.
- That anything braids. The TetA and TetB strands about an octahedron axis are unlinked (linking number 0), and the leg axes meet at $O$.

## 6. Correction to the earlier Triforce proof

[`../triforce-vortex/PROOF.md`](../triforce-vortex/PROOF.md) said that every winding eigenstate circulates and turns the star point's ring, on the strength of 20 random numerical samples. The exact certificates show that this is true on $W'$, but not in general on $W$:
- $W$'s energies are doubled for every parameter set.
- Some of its stationary combinations carry no current, depending on the parameters.
- Numerical eigensolvers return one particular basis of a doubled level, which is why sampling missed this.

The earlier document now points here.
