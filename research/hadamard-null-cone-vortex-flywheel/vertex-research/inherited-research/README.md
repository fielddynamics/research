# Native vortex–torsion convergence

*Gravity Field Dynamics · Field Dynamics Research · research before Proof 26 · 26 November 2026*

**Status:** The original 581 exact assertions and eleven recovered research suites (2,121 named assertions) have been freshly rerun; the expanded cross-model suite adds 144 exact and 345 numerical assertions. See [coverage audit](VORTEX_MATH_COVERAGE.md) and [new results](CROSS_MODEL_FINDINGS.md). New research on the existing eight-vortex flywheel, with no additional dynamical state, coupling, or fitted constant. [T] denotes exact finite algebra, [D] consequences conditional on the published Stage VII model, [E] physical interpretation/selection still open. This is **not** Proof 26, a Lean certification, a derived Lorentz-covariant field theory, or an empirical identification of GFD with gravity. Repository basis: [`46e5ca1`](https://github.com/fielddynamics/research/tree/46e5ca1fef621f8fc4243a01324fe93342633354).

> **Repository note.** These notes record earlier research carried into the vertex work. Their own scripts, data files, figures and the `ALGEBRA.md`, `RESEARCH_GATES.md` and `SOURCES.md` companions were not included with them, so their assertion counts cannot be reproduced from this folder, and links to those files do not resolve. The vertex research's own verifiers, in the parent folder, are complete and rerun.

## The question

GFD proposes that TetA is the metric-visible chamber, TetB is the orientation-sensitive torsion chamber, and their eight constituent vortex rings form one collective engine. The primary vortex is the resulting circulation on the shared octahedron, not an additional oscillator. Letter 2 identified the connection partition 40+24; Letter 3 identified 24=8×3; Proofs 23–25 established the address dictionary and common geometry. Can we follow **actual currents**, rather than just matching numbers of components, into the antisymmetric connection slots?

The answer is more precise than a count. A natural signed dictionary exists for actual bonds of each chamber. Its totally antisymmetric part is supplied entirely by the outer ring currents, regardless of the choice of radial read. The core angular moment is proportional to its axial read with an exact time-dependent gain. This supplies a concrete mathematical candidate for the rotating torsion channel. A connection-valued transport/normalization still needs an independently justified physical law.

![From native bonds to torsion carriers](native_bond_dictionary.svg)

## Expanded cross-model investigation — read this first

The [cross-model findings](CROSS_MODEL_FINDINGS.md) independently reconstruct both original vortex graphs, verify the symbolic pixel secular polynomial and 4+6 Triforce winding decomposition, and test the existing Stage VII/IX solutions. They also establish a crucial new distinction:

- Each star's six normalized base/ring current records are a decomposable bivector. The Pfaffian vanishes exactly, so the actual single-chamber base-current map has generic differential rank 20 although the *formal* linear bond-to-slot dictionary is rank 24.
- The opposite-column read can attain rank 24, and the two-chamber parity-projected base read can also attain rank 24 on generic unconstrained states. Neither is uniquely selected by the dynamics.
- A core-dark A4 helicity state has a single-chamber spatial 3-form (pseudoscalar), distinct from the spatial axial vector in the collective triplet state. The parity-projected pseudoscalar measures chamber imbalance; equal occupations cancel it even if all eight rings circulate.
- These are exact current-to-tensor statements, not physical Cartan transport. They supply tests a derived connection must satisfy.

![Actual Stage VII axial and core current time series](axial_core_dynamics.svg)

The plot uses the full original dimensionless Hamiltonian. It is a numerical corroboration of the exact collective-sector laws, not a physical measurement. The [source coverage audit](VORTEX_MATH_COVERAGE.md) states exactly which older mathematical results were reconstructed, which tests reran, and which original verifiers still need execution in the full checkout.

## 1. What the earlier research already established

Read the [source register](SOURCES.md) before changing the model. It links the original torsion letters, chiral holonomy, two-connection research, Triforce tetrad read, archived core-hardening and sustained flywheel, Proofs 23–25, and the recovered native-grading/settlement studies. The detailed derivations here are in [ALGEBRA.md](ALGEBRA.md); [RESEARCH_GATES.md](RESEARCH_GATES.md) records the unresolved questions and proposed next calculations.

Three distinct objects must not be conflated:

- a scalar or complex tile amplitude (a field-state coordinate);
- a directed bond current (a bilinear observable of the existing amplitudes);
- a spacetime torsion tensor (the antisymmetric lower-index part of a connection, with units and transport law).

The first two already exist in the graph Hamiltonian. The third is the target of the proposed dictionary. No new store of energy or independent core oscillator is introduced.

## 2. Why scalar tiles are not yet the torsion tensor [T]

The 24 lateral tiles have labels `(h,i,j)`, chamber h=±, i≠j among four labels. Each chamber's 12 labels are a regular orbit of the proper tetrahedral group A4, but not of S4. The 24 torsion slots are `T^a_[bc]`, four choices for the upper label and six oriented pairs. Write the S4 irreducibles as A1,A2,E,T1,T2 (T2 is the polar triplet). The multiplicities are:

| Space | A1 | A2 | E | T1 | T2 | dimension |
|---|---:|---:|---:|---:|---:|---:|
| Both scalar tile arrays | 2 | 0 | 2 | 2 | 4 | 24 |
| Both outward-oriented ring bond arrays | 0 | 2 | 2 | 4 | 2 | 24 |
| Torsion regular representation | 1 | 1 | 2 | 3 | 3 | 24 |
| One ordinary + one sign-twisted ordered-pair array | 1 | 1 | 2 | 3 | 3 | 24 |

The maximum rank of a fixed S4-equivariant linear map from either of the first two spaces to torsion is 20, and the bound is attained. A4 permits an invertible map, with an explicit reflection sign defect. The twisted scalar-tile map mirrors Proof 23's incident/nonincident dictionary; its twist cannot simply be assigned to one physical chamber as an unexplained rule. This is why moving from tiles to actual *directed bonds* matters.

## 3. The native directed-bond dictionary [T]

Write X^h_ij for a lateral tile at apex i on original face j, and y^h_i for the central base of that stellation. In each chamber there are exactly twelve outer ring bonds and twelve tile-to-base bonds. Each is an actual edge of the published 33-site graph, independently verified from the exact triangle coordinates. Define a candidate connection read on one chamber:

```
T^i_ij := J(X_ij -> y_i)                 incident upper/lower labels
T^i_jk := J(X_ij -> X_ik), i,j,k distinct nonincident upper/lower labels
T^i_kj := -T^i_jk
```

For the incident case, extend by antisymmetry too. There is one representative for each of the 24 tensor slots. The incident bonds have a fixed lateral-to-central direction; the nonincident bonds reverse when j and k exchange. This is exactly the signed index action of torsion. No orientation sign is assigned by hand to one of the chambers. The resulting linear map from **formal bond records** to the 24 slots is a signed permutation, an isometry for the unit slot metric and equivariant for all 24 label permutations. This does not mean those records are independent dynamical degrees of freedom. The alternate actual bond `X^h_ij -> y^{-h}_j` gives a different incident read, with the same nonincident read.

Chamber inversion swaps the two arrays of label-oriented bond currents. Physical spatial parity on the tensor, expressed in the Hadamard time/spatial basis, has a 12+12 split. A full 48-to-24 read can be constructed by taking the even chamber combination into the parity-even target and the odd combination into the parity-odd target. This is onto and respects both actions; the orthogonal version has orthonormal rows. It is an admissible symmetry-consistent read, **not** uniquely selected by dynamics. In particular, physical inversion is not identical to lower-index exchange. The physical Stage VII solution has equal label-oriented current arrays; its outward ring means are opposite between chambers because outward orientation reverses.

## 4. The primary vortex and the axial carrier [T/D]

Retain the published collective phase and amplitudes, with no new variables:

```
q_i = s_i · z, Σq_i=0, ||z||=1, ρ=√3/8
X^±_ij = ρ(u q_i + v q_j), y^±_i = ρ w q_i, ψ_O=0
C = -i conj(z) × z
```

Define the totally antisymmetric 3-form part of the proposed tensor by cyclic antisymmetrization. Every incident slot has a repeated label, so it contributes zero. For every distinct triple i,j,k, the sum of the three ring currents cancels all symmetric bilinear terms. In the normalized Hadamard time/spatial basis the result, using the published r=−1 current convention, is

$$T_{[0ij]}=\epsilon_{ijk}\,\mathcal A_k,\qquad
\boxed{\mathcal A=\frac{|v|^2-2\operatorname{Re}(\bar u v)}{8}\,C.}$$

Here indices i,j,k in the displayed physical-frame formula are spatial, and the remaining all-spatial 3-form is zero. The coefficient uses a single chamber read, or the chamber **average** for the inversion-even state (the orthonormal paired read uses √2 times the average). This is an axial spatial carrier extracted from actual ring currents by the specified dictionary; it is not yet physical torsion in inverse length units.

The actual primary core has the independently established angular current

$$\mathcal L_c=-\frac{|w|^2}{6}\,C.$$

Therefore the new exact identity is

$$\boxed{|w|^2\mathcal A=-\frac34\bigl(|v|^2-2\operatorname{Re}(\bar u v)\bigr)\mathcal L_c.}$$

This is an undivided identity valid even when the core is empty. No independent axis or amplitude is assigned to the core. It follows from the same collective phase. The two reads are collinear with opposite signs when the coefficient is positive, in the stated orientation conventions. They are not universally equal as magnitudes: initially w=0 while the ring axial read is already nonzero. That is the distinction between the orientation carrier and the actual developed primary vortex. The centre point O is dark throughout this Stage VII solution, while the surrounding octahedral core circulates.

## 5. Persistence and what the full current read resolves [D]

Let m=u−v/3. The established empty-core trajectory has |v|≥73/77 and |m|≤2√22/99. It follows rigorously that

$$|v|^2-2\operatorname{Re}(\bar u v)\ge |v|(|v|/3-2|m|)>0.$$

The coefficient of C in the axial read has a uniform lower bound of approximately 0.01499173 (dimensionless), not claimed sharp. The established w(t)≠0 for all finite t>0 then makes both axial and actual core current nonzero when C≠0. The core can return arbitrarily close to zero by recurrence, and no physical dissipative drain or attractor follows. For a stationary row-closed branch, u=v/3, the axial read is simply |v|²C/24. The published stationary witness is normalized by √(75/77); the coefficient is then 75/(77×24), and its angular core moment is −(75/77)(16/225)C/6.

The 24 current records are not independent. For a fixed u,v,w and the collective ansatz, all currents are linear in the nine real Hermitian bilinears of z. The 12 ring currents in a chamber have rank 3 for real u/v and v≠0; for nonreal u/v they have rank 8 on that *linear bilinear space*: three axial and five traceless symmetric contributions. The isotropic bilinear is invisible. Ring means always see only the axial triplet, and the three bonds in each row are equal when u=v/3. The actual pure-state bilinears have rank-one constraints, so even these ranks are not physical degrees of freedom. In the stationary real-ratio state the entire proposed 24-slot tensor image has rank three. This is exactly what a collective engine should exhibit, rather than twenty-four independently excited vortices.

## 6. Which torsion carrier is selected? [T/E]

The time/spatial Hadamard map explicitly identifies the three allowed Td-equivariant axial embeddings in the 24-slot representation. Two are even under ordinary spatial inversion and are rotationally covariant; the third is a tetrahedrally anisotropic spatial tensor. The first two are

```
A(C)_{0ij}=ε_ijk C_k,
B(C)_{i0j}=ε_ijk C_k, B(C)_{ij0}=−ε_ijk C_k.
```

For a combination aA+bB, the pure 3-form projection is `(a−2b)/3 (A−B)`. The other independent even combination is mixed tensor torsion. The third allowed Td map uses the invariant cubic tensor of the reference tetrahedron; physical inversion eliminates it from a fixed linear map of an inversion-even C unless another inversion-odd input is supplied.

The native ring-plus-base and ring-plus-column reads both give **exactly the same axial projection** but different mixed-tensor components. This supplies a concrete nonuniqueness test. A coordinate tensor can always be converted into a unique metric-compatible contorsion by the standard inverse formula, once its units, coframe and physical interpretation are specified. It does not establish that the graph's Hamiltonian transports frames by that connection.

The axial triplet does not directly supply a static time-leg acceleration: all three candidate embeddings have `K^i_00=0`. The previously developed Read–Settle–Register model already gives an explicit separate nonaxial time-leg response. A future derivation must link these two responses of one engine, not add another oscillator or equate axial rotation with a static force.

## 7. Reproduce and continue

```
python -m pip install sympy
OPENBLAS_NUM_THREADS=1 python explore_vortex_torsion.py > verification_output.txt
```

The self-contained script constructs all finite group actions, explicit intertwiners, actual triangle adjacencies, Hadamard tensor transformation, axial/contorsion maps, and symbolic current identities. All 581 assertions use exact arithmetic. The checks include repeated group cases, not 581 independent theorems. For this expanded package, the original 581-check suite, eleven local inherited suites and the new cross-model suite were rerun. See the actual logs and the source coverage audit; the complete original vortex verifier was not rerun. The diagram is explanatory, not a physical simulation. No new Lean proof or live repository change is included.

**Next:** derive or constrain a tetrad-valued link transport from the native Hamiltonian/action that realizes the proposed bond read and yields the same tensor through Cartan closure. Determine what selects the incident/radial read, its units, and the coupling between axial and acceleration channels. See [Research gates](RESEARCH_GATES.md) for the exact acceptance criteria.
