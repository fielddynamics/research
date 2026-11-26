# The native root grading and core response of the eight-vortex flywheel

*Gravity Field Dynamics · Field Dynamics Research · November 2026*

**Status:** exact geometry and finite-dimensional algebra for the specified Stage VII and Stage IX models, not a physical derivation of Newton's constant. Based on `d69739e984e5f1f8de5e4639d8fd0e7a2a8214b8`. The Python verifier performs 208 new exact assertions and reruns the 16 reconstruction assertions. No Lean build or independent empirical verification is claimed.

## The question

The refined octahedral surface has seventeen independent divergence-free current patterns. The coupling polynomial also assigns seventeen to the Field Origin. Rather than prescribe a selective reversal that reproduces thirteen, we ask what the actual inversion symmetry and the original eight-vortex Hamiltonian establish on their own. The [core Hodge study](../../../vortex-induced-triforce-refinement/core-hodge/) determines the current space, while the [sustained flywheel](../../SUSTAINED_TRIFORCE_FLYWHEEL.md) and [unified synthesis](../../UNIFIED_HADAMARD_FIELD_DYNAMICS.md) supply the pre-existing amplitude dynamics. The three objects must not be conflated.

## 1. Exact geometric connection between the midpoint streams and leg pairs

Let the four tetrahedral sign vectors be $s_i$ with sum zero. The six octahedral vertices are $v_{ij}=(s_i+s_j)/2$ for unordered pairs $i\ne j$. They are the six axis points $\pm e_a$. The edge shared by the core faces with outward normals $s_i$ and $-s_j$ has midpoint $m_{ij}=(s_i-s_j)/4$, for $i\ne j$. Indeed its endpoints are $v_{ik},v_{il}$, where $k,l$ complement $i,j$. Thus all twelve new vertices have a canonical ordered-distinct-pair label, without choosing a basis by matching dimensions.

The divergence-free current space is the stream space modulo constants, with an orientation sign under improper transformations. The twelve hidden loop generators are the streams supported at the twelve new vertices. Under a leg permutation $g$ their action is $\operatorname{sgn}(g)$ times the permutation of ordered pairs. Under spatial inversion, $m_{ij}\mapsto m_{ji}$, while the stream sign reverses. Hence on this hidden basis physical inversion acts as **negative transposition**, $-\tau$, with six even and six odd modes. On the six old vertices it complements the unordered pair; the visible stream quotient has three even dipoles and two odd quadrupoles. The full cycle inversion has trace one, not thirteen.

The refined circulation character and the original abstract root-even character $1+V\otimes V$ for the five conjugacy classes (identity, transposition, double transposition, 3-cycle, 4-cycle) are respectively

$$\chi_C=(17,-3,1,-1,1),\qquad\chi_E=(17,5,1,2,1).$$

Over the complex numbers (or the corresponding real representations) the irreducible multiplicities in order trivial, sign, two-dimensional, standard three-dimensional, sign-twisted standard are $(0,1,2,1,3)$ and $(3,0,1,3,1)$. The maximum possible rank of an equivariant linear map is eight under $S_4$ and fifteen under $A_4$. This comparison complexifies the real current representation when comparing it to complex amplitude coefficients. No invertible symmetry-preserving identification exists. The 17 current dimensions remain a topological capacity, not necessarily realizable as independent stationary coherent currents.

## 2. The native even amplitude space is exactly the abstract root-even representation

Stage IX has 32 primary tile amplitudes and four Origin coordinates, while Stage VII has the same tile geometry and only the scalar Origin. Inversion pairs all 16 A tiles with their B partners, preserves the scalar coordinate and reverses the polar coordinates. Therefore Stage VII splits into 17 even and 16 odd amplitudes; Stage IX splits into 17 even and 19 odd amplitudes. In either model the even space is canonically the scalar Origin plus the even amplitude on each paired tile. Since the actual geometry labels a tile by its face and its central/lateral child, it carries precisely $1\oplus V\otimes V$ under the specified tetrahedral permutations. The verifier checks all 24 geometric actions on the explicit embedding, not just the character. The original [root-exchange algebra](../../../g_from_topology/read-and-rotation/ROOT_EXCHANGE_ON_THE_ADDRESS_TREE.md) therefore has a native realization of its even sector. It does not identify that sector with the 17 circulation modes.

## 3. A minimal geometric read, and why it is not the full engine

In the native model let $C_-$ denote the four-dimensional odd central-face amplitude space. The central faces are labeled by the four legs and their inversion partners, so $C_-$ is a copy of $V$ and inversion acts as $-I$. The smallest linear space containing the entire even sector and the amplitudes of all eight central faces is

$$\mathcal R=\mathcal H_+\oplus C_-.$$

Its dimension is 21 and its inversion trace is 13, with root-average rank 17. It realizes $1\oplus V\oplus(V\otimes V)$, with precisely the original root grading, under the full specified tetrahedral permutation action. Equivalently the read retains the even paired tile inventory and scalar Origin, plus the odd difference of each of the four central face pairs. This is an exact representation theorem **conditional on the stated read selection**. Retaining the three additional odd polar Origin coordinates would instead give dimension 24 and trace 10, so the 21-read cannot be called the complete native Origin read.

![Native root grading and its invariant hull](native_root_grading.svg)

The next test is autonomy. If $P$ is the orthogonal projection onto $\mathcal R$, native dynamics preserve the read for arbitrary states only if $(I-P)HP=0$. Exact rank sequences for $\mathcal R,H\mathcal R,\ldots$ are 21,25,28 in Stage VII and 21,24,27,30 in Stage IX, at which point they stabilize. Thus neither native model has autonomous 21-dimensional evolution on this read. A physical settlement law must justify projecting, retaining history, or including the additional dynamical coordinates. A trace is not a response coefficient.

## 4. A different native thirteen: the minimal odd-core response

Take the same input/output convention in both chambers: the normalized even or odd combinations of the four central face pairs. For a real symmetric Hamiltonian $H$ and port matrix $F$, the smallest invariant space containing the ports is the Krylov span of $F,HF,H^2F,\ldots$. By self-adjointness the complementary space is invisible to all coherent histories of the same ports. Exact ranks are

| Model | Full even | Full odd | Even core reachable | Odd core reachable | All core reachable |
|---|---:|---:|---:|---:|---:|
| Stage VII | 17 | 16 | 12 | 11 | 23 |
| Stage IX | 17 | 19 | 12 | 13 | 25 |

![Same-port core reachability](native_core_reachability.svg)

The thirteen in Stage IX is not imposed by a trace. The odd uniform central amplitude is a stationary scalar eigenmode of energy 3 because the equal base and column bonds cancel. The odd polar-vector reduction has four copies of the three-dimensional vector representation, and the central input is cyclic in its four-dimensional multiplicity block. Its exact Krylov determinant is -128. Consequently the odd core has a minimal dynamic realization of dimension $1+4\cdot3=13$.

This is a more substantive native occurrence of thirteen, but it is not yet the original trace denominator. If we use the identical read in both sectors, the comparison is 12 versus 13, not 17 versus 13. The latter would compare the entire even inventory with only the observable part of the odd inventory. No physical law yet justifies those asymmetric measures.

The odd uniform scalar block also shows why the count is not protected by symmetry. For existing ring, transpose, base, column and central couplings $r,d,b,a,k$ and site energies $e,e_c$, its matrix in the outer/central uniform amplitudes is

$$\begin{pmatrix}e+2r-d&b-a\\3(b-a)&e_c-3k\end{pmatrix}.$$

Changing the existing base bond strength while preserving all tetrahedral symmetries and inversion makes $b-a\ne0$. The odd scalar becomes a two-mode system and the tested odd-core rank becomes 14. This exact counterexample keeps the graph and all symmetries unchanged. The equality of base and column couplings requires independent dynamical justification if the physical count is to be thirteen.

## 5. Test the response, rather than replacing it by a dimension

For normalized central inputs and outputs the exact Stage IX core Green functions, with spectral parameter $z$, are

$$g_{+,0}=\frac{z(z+3)}{z^3+6z^2-11z-24},\quad g_{+,1}=\frac{(z-1)(z+2)}{z^3-7z+2},$$
$$g_{-,0}=\frac1{z-3},\quad g_{-,1}=\frac{z(z^2+z-4)}{z^4+2z^3-19z^2-4z+32}.$$

Subscript 0 denotes the scalar and 1 the triply degenerate vector sector. All denominators are uncancelled. The two traces $g_{+,0}+3g_{+,1}$ and $g_{-,0}+3g_{-,1}$ have distinct poles; both have leading asymptotic $4/z$, and their analytic static limits are -3 and -1/3 respectively. Although the full Hamiltonian has a dark zero eigenvalue, the core-projected response is regular there. No frequency-independent 17/13 proportionality follows. These are dimensionless native linear response functions, not the gravitational stiffness or the covariant SST response.

## 6. The actual core vortex does not occupy the entire cycle inventory

The two native Hamiltonians have inversion parity as an exact symmetry. A pure-parity coherent state has inversion-even bond currents. The only common energies of the parity blocks of Stage VII are 1/2 and 3/2; those of Stage IX are 0 and 2. Exact polynomial gcds establish this, and exact eigenspace nullspaces show that every state in each shared eigenspace has zero central amplitude. Therefore **every stationary eigenstate of either native model has an inversion-even central current**, even in the case of an accidental cross-parity degeneracy. After the Hodge projection its visible circulation lies in the three-dimensional dipole sector, never the two quadrupole modes. The known Stage VII sustained stationary triplet realizes all three dipole directions in the linear span of its actual bond currents; the Stage IX vector cyclicity gives the same existence argument using a real eigenbasis of its self-adjoint restriction. These results do not rule out mixed-parity time-dependent currents or fine-model hidden currents.

The earlier rotation-factor algebra also has a precise realization on the visible stream geometry. The proper 120-degree rotation acts on the traceless diagonal quadratic stream plane with eigenvalues $\omega,\bar\omega$. Its composition with inversion acts with eigenvalues $-\omega,-\bar\omega$. On the axial dipole plane the existing quarter-turn rotoreflection gives $i,-i$. The corresponding two-dimensional characteristic determinants at symbolic $K$ are $K^2+K+1$, $K^2-K+1$ and $K^2+1$. They recover 21,13,17 at $K=4$ as in the [read-and-rotation research](../../../g_from_topology/read-and-rotation/). However the odd quadrupole plane is absent from the native stationary core vortex; these factors are geometric spectral data, not a derivation of a physical ratio or determinant attenuation.

## 7. The next defensible research step

The exact native root grading is a better bridge than a prescribed selective quadrupole reversal. Before searching for gravity, derive the physical measurement and energy functional for the Origin. Test whether it retains the 21-read or some other observable, and derive the causal memory term induced by eliminating the native complement. Use the **same** source and output normalization in each parity sector unless the action independently requires otherwise. Determine why the base and column couplings should be equal, if that is claimed. A proposed 17/13 gravitational normalization must arise from that physical response rather than from the choice of dimension or spectral factor.

No new physical constants or free tuning parameters are introduced. The bond variation is an explicit counterexample, not a fit. The previous selective trace-13 construction should be retained only as a rejected candidate for ordinary inversion, not used as the foundation of a physical proof.

## Reproduce

Run `OPENBLAS_NUM_THREADS=1 python explore_native_grading.py` from this directory after the previously integrated `../core-flywheel/` study is present. Requires NumPy, SymPy, SciPy and Matplotlib. All 208 new checks use exact integer or rational algebra; the figures are explanatory. [Output](exploration_output.txt). SVG and PNG versions of both diagrams are included. This is research rather than a new Lean proof.
