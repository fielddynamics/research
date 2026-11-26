# Cross-model current constraints and vortex–torsion identifiability

*Continuation of the native vortex–torsion research; research only, not Proof 26. 26 November 2026.*

**Status.** The independent `cross_model_currents.py` suite passed 144 exact symbolic/rational and 345 numerical assertions. The original 581 exact assertions and eleven recovered suites (2,121 named assertions plus their repeated prefixes) were freshly rerun successfully. Numerical trajectories use explicit tolerances and are diagnostics, not proofs. Assertion totals overlap. No new physical coupling, degree of freedom, or field equation is introduced.

## 1. Why we re-open the older vortex proof

The original [Vortices of the Stellated Octahedron](https://github.com/fielddynamics/research/tree/46e5ca1fef621f8fc4243a01324fe93342633354/proofs/vortices-of-the-stellated-octahedron) covers all real symmetric Td-invariant Hamiltonians on two particular graphs, not just the symmetric Stage VII witness. It distinguishes stationary winding from actual nonzero conserved currents; its corrected sign is J(i→j) = −2 H_ij Im(conj(ψ_i) ψ_j). The new signed tensor read acts on the 33-site model, not directly on the 15-site model. We independently construct both graphs from the original coordinates, and then compare their results. The 15-site graph has 50 bonds and 4 site plus 6 bond orbits. The 33-site graph has 104 bonds and 5 site plus 10 bond orbits; the actual triangle-sharing edge set is exactly the Stage VII six-class graph. Its twelve outer transpose edges connect opposite chambers as labelled by apex; the geometrical description of a Field Origin coupling must not be used to delete those edges. Stage VII adds the premise of chamber-exchange symmetry and therefore has fewer independent weights than the original Td class. Stage IX extends the centre to four coordinates and uses a different witness. These models are not interchangeable.

### Pixel winding theorem: symbolic reproduction

For the quarter-turn rotoreflection S:(x,y,z)→(−y,x,−z), the primitive i-eigenspace is three-dimensional and vanishes at O and ±e_z. In the exact orbit basis the original matrix is an arrowhead with diagonal (Δ_f, ε_A, ε_B) and off-diagonal entries with squared magnitudes 2c_A² and 2c_B². Our independent reconstruction gives

`det(EI−H+) = (E−Δ_f)(E−ε_A)(E−ε_B) − 2c_A²(E−ε_B) − 2c_B²(E−ε_A)`.

For c_A c_B≠0 and distinct corner energies, the secular function is strictly increasing between the poles and ranges from −∞ to +∞ in each interval; there is one root in each. Neither corner pole is an eigenvalue, and the equatorial amplitude is nonzero. The octahedron edge weight h cancels from this polynomial, but the original *current* formula is `I=(E−Δ_f−2h)|ρ|²`. Thus a winding eigenstate can fail to circulate on an exceptional parameter set even with nonzero equatorial amplitude. When ε_A=ε_B a ring-dark eigenstate occurs. Conjugation reverses the current; a real standing-wave combination has none. Removing the octahedron leaves only origin-to-corner links with vanishing winding current; adding cube edges changes that conclusion. The current formula and genericity results are inherited from the revised original theorem, not independently rerun in its complete 81-check script. The new cross-model suite independently verifies the secular polynomial, winding dimension, axis zeros, and h-independence, not the full flux certificate. No canonical 24-slot read of the 15-site state is supplied; deriving one requires a map to the tile currents, not equating point and tile graphs by geometry alone.

### Triforce winding split: symbolic reproduction for every orbit parameter

The 120° leg permutation has ten three-cycles and three fixed sites. Its ω-eigenspace is ten-dimensional and dark on the chosen leg. The full T2 isotypic projector is

`P_T2 = (1/8) Σ_{p∈S4} (fix(p)−1) U_p`.

We construct all 15 site/bond orbit matrices and verify individually that each commutes with this projector and the leg rotation. Applying it to the winding basis gives rank six; the complementary projector gives rank four with support entirely on the lateral tiles. This re-establishes the W′ and W decomposition without assuming Stage VII symmetry. The original proof additionally supplies a doubled 2×2 spectral formula on W and generic nonzero current certificates on W′. Those results are relevant and retained as premises, not re-certified in full here. In particular one cannot infer that every state in a degenerate winding sector is a vortex or that every vortex excites the actual core. The full original 81-check verifier and its archived exact certificate suite remain to be rerun inside a complete repository checkout.

## 2. A new exact nonlinear constraint on the native base dictionary

For a fixed chamber h and apex i, the three lateral tiles X_ij (j≠i) and the central triangle y_i form a complete four-site graph K4. There are exactly six bonds: three lateral-ring and three base bonds. Define four complex numbers

`z_i=−ψ(y_i), z_j=ψ(X_ij) (j≠i)`.

The minus sign accounts for the chosen orientation X_ij→y_i, rather than y_i→X_ij. For nonzero real ring and base hoppings r,b define the normalized lower-pair skew array

`B^i_{jk}=T^i_{jk}/(-2 H_{jk}^{local})`,

where H_local=b when one lower index equals i and H_local=r otherwise. Then B^i_jk = Im(conj(z_j) z_k) = x_j y_k−x_k y_j for real x,y. In exterior algebra B^i=x∧y is a decomposable bivector. In four dimensions this is equivalent to the single quadratic relation

**Pf(B^i)=B^i_01 B^i_23−B^i_02 B^i_13+B^i_03 B^i_12=0.**

The identity is verified symbolically in all eight real coordinates. Conversely, any real 4×4 skew matrix of zero Pfaffian has rank at most 2, and if nonzero it has rank 2 and can be written x∧y (choose an orthonormal basis of its two-dimensional image and scale one basis vector). Thus this constraint completely describes the unconstrained instantaneous current image on one star for nonzero weights. This is a statement at an instant, before imposing norm, energy, stationary eigenstate or coupled evolution. It is not a claim about the number of independent propagating physical torsion components. For one star the nonzero simple-bivector cone is five-dimensional; at a real state its differential has rank at most three. At the zero bivector the cone is singular. The four stars within one chamber use disjoint coordinates, so the joint raw base-current map has generic real differential rank **20**, not 24. All four Pfaffian equations hold identically. Their product image (before the global state constraints) is exactly the product of four simple-bivector cones. Zero weights require an undivided polynomial relation or a separate zero-edge analysis; division is not allowed there.

### Why this changes the previous result

The signed bond-to-slot map in the first study is still an orthogonal rank-24 linear map on **formal independent records**. Its input is not a free 24-vector if it comes from a coherent wave. The raw current map from the actual amplitudes is nonlinear and generically rank 20. The new calculation resolves this distinction explicitly. A formal torsion slot tensor with normalized B_01=B_23=1 and all other components zero is allowed by antisymmetry but cannot be realized by this one-star current read (Pf=1). Replacing formal full rank by physical full rank would be an error.

## 3. Base, column and two-chamber reads are different mathematical objects

For the alternate incident read X_ij→y^-_j, the three incident bonds of one star involve three *different* opposite central sites, not the single base amplitude. Consequently the K4 wedge constraint cannot be imposed on those six records. On twelve explicit rational-amplitude Jacobians, eleven have rank 24 and one rank 23. One full-rank exact minor suffices to prove the generic local rank 24 for this particular nonzero witness and unconstrained complex-state domain: the minor is a nonzero polynomial in the real/imaginary amplitudes and its zero locus is proper. There is no claim that the column choice is physically better or unique. It is a mathematically inequivalent candidate read of the same graph. Both have identical full alternation because the incident indices repeat; they can differ in vector and mixed-tensor components. The tests explicitly check alternation for general amplitudes, not only the collective ansatz.

For the two-chamber parity read `R=P_even F(j_++j_-)/2+P_odd F(j_+−j_-)/2`, F is the normalized Hadamard tensor transport (including the signed dictionary in the slot ordering). Despite the four raw constraints on each chamber, the map to physical-parity slots is locally onto: all six rational-amplitude Jacobians have rank 24. This proves the generic rank for that fixed Hamiltonian by the same nonzero-minor argument. It does **not** establish global surjectivity under normalization, dynamics or a physically derived connection law. In a parity eigenstate of the wave, j_+=j_- in label-oriented coordinates (quadratic currents erase the overall sign), so the physical odd tensor read vanishes and the image is confined to the 12-dimensional even sector. A generic 24-output rank cannot be applied to the three-amplitude collective trajectory. The earlier stationary collective tensor rank three remains intact.

## 4. The old core-dark helicity is a decisive torsion test

The original Stage VI and later refinement studies constructed the A4/V4≅C3 character states. We independently reconstruct two vectors e_A,e_B, with unnormalized unit-modulus outer components and support in one chamber each, and zeros on all eight central triangles and the centre. Their norms squared are 12; both are orthogonal. For the Stage VII witness their exact restriction is

`H_hel = [[1,−1/2],[−1/2,1]]`.

This follows directly from the full 33×33 Hamiltonian and is verified exactly. Their symmetric combination and antisymmetric combination are stationary (energies 1/2, 3/2). They carry nonzero currents on all 24 ring bonds, yet the actual core currents are identically zero. The fully alternating single-chamber tensor read is a pure **spatial 3-form**, with coefficient T_[123]=2√3 for our unnormalized positive character, rather than the T_[0ij] spatial axial vector of the collective Stage VII branch. Conjugation reverses it. This is the sign/pseudoscalar line anticipated in the archived Hodge–Dirac analysis; it is not the same as a vector C.

For `ψ=α e_A+β e_B` with our unnormalized basis, the physical parity-projected 3-form coefficient is exactly

`T_[123] = √3 (|α|²−|β|²)`

using the chamber-average convention. Cross-phase terms cannot enter the ring-only read because each ring is supported within one chamber, so the identity verified for arbitrary real α,β extends to complex α,β. For normalized basis vectors e_A/√12 and e_B/√12, divide the coefficient by 12. For equal occupations the odd pseudoscalar cancels even though all eight rings can circulate; for unequal occupations it survives despite the core being entirely dark. From a normalized chamber-localized helicity input, the two-level evolution has occupations cos²(t/2), sin²(t/2), hence the signed pseudoscalar oscillates as cos(t) with zero core at every time. This exact example disallows a universal equality between the core angular moment and the entire totally antisymmetric tensor sector. The axial vector identity of the first study remains exact **on the stated collective triplet sector**. It must not be silently extended to all winding states. The scalar pseudoscalar and spatial axial vector are distinct under the selected observer and physical parity.

## 5. Time-dependent cross-model calculations

Stage VII uses the exact full 33-site graph, with the published r,d,b,a,k,o and on-site energy witness. At 65 dimensionless times, the numerical evolution agrees with the independently reduced 3×3 solution for the axial coefficient and core angular moment. Norm conservation is also checked at each sample. The graph amplitudes, not a prescribed torsion tensor, produce the currents.

![Same collective orientation, different magnitudes](axial_core_dynamics.svg)

The plot is generated from `stage_vii_axial_core.csv`; neither axis is calibrated to a physical spacetime scale. The initial core is empty and the outer axial read is nonzero. Later the two vectors are opposite in the fixed conventions, with distinct magnitudes. The exact all-time bounds are inherited from Stage VII and the closed algebra; numerical samples are not an all-time proof.

Stage IX uses the independently reconstructed H36 with all ordinary bonds −1 and the original direction-sensitive central coupling `−(1,s)`; the original scalar site plus three polar coordinates are the published extension, not invented in this study. At 25 times for each of the even and odd amplitude inputs, we check norm conservation, equal labelled chamber current reads in a parity eigenstate, and collinearity of the projected spatial axial read with the primary core moment. Collinearity includes possible zero reads and does not imply equality or persistent winding. The two weights, parity trajectories and scalar/polar centre must not be confused with Stage VII.

## 6. What would establish actual Cartan torsion?

All calculations above concern tensor-valued current observables. They establish precise representation, image and orientation identities, not a microscopic connection. A physical test must derive frame transport from the same native interaction. For a coframe e and spin connection ω, torsion is T^a=de^a+ω^a_b∧e^b. On an oriented infinitesimal loop, its translational closure defect is T evaluated on the area bivector; Lorentz rotation holonomy instead measures curvature. A pure gauge frame link can yield trivial transported closure even if the underlying complex wave circulates. The old chiral-holonomy proof calculates a prescribed rotational holonomy, not this translational closure defect. The previous diamond-lattice T15 test correctly rejected using U(1) bond reversal as evidence of frame torsion.

The next experiment should derive a single tetrad-valued link transport with coframe and spin connection from the native shared-edge interaction; compute its loop translation using actual paired Triforce paths, test the Cartan identities, then compare the resulting tensors to the candidate base/column reads, including the Pfaffian constraints, core-dark pseudoscalar and pure-triplet states. No arbitrary fit of the connection coefficients or independent oscillator is warranted. The current read's units, normalization and source law remain unresolved. Axial torsion alone gives no direct static time-leg acceleration; the already developed read–settle–register vector response is a separate response channel of the candidate engine, not evidence of its derivation from the rotating current.

## 7. Reproduction

`python explore_vortex_torsion.py`, `python cross_model_currents.py`, `python rerun_inherited.py`. Dependencies: SymPy, NumPy, SciPy, Matplotlib. See actual logs, `inherited_rerun.jsonl`, the source coverage audit and the original source register. The eleven inherited test copies have not been altered except for directory placement to satisfy original relative imports. They write outputs into their own local subfolders. No Lean build and no physical data fit were performed.
