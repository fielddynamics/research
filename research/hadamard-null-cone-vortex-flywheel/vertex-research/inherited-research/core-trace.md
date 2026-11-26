# The seventeen core circulation modes and the 17/13 coupling ratio

*Gravity Field Dynamics · Field Dynamics Research · continuation of the eight-vortex core programme · 26 November 2026*

**Scope.** [T] Exact finite geometry, symmetry and linear algebra. [D] Consequences of the previously specified dimensionless Stage IX and refined Hamiltonians. [O] Physical selection of the core lattice, action, boundary functional and gravitational normalization. This note tests, rather than assumes, the identification of the core's 17 with the 17 of the coupling polynomial. It supersedes the conjecture that ordinary chamber inversion acts by reversing only the two visible quadrupole modes. It does not change SST or Proof 23.

## 1. The two occurrences of seventeen

The [root-exchange construction](../../../g_from_topology/read-and-rotation/ROOT_EXCHANGE_ON_THE_ADDRESS_TREE.md) uses the graded space $\mathbb R\oplus V\oplus(V\otimes V)$ with $\dim V=4$. Its abstract involution has 17 positive and 4 negative directions, yielding trace 13 on a **21-dimensional** space. Its positive space is $W=\mathbb R\oplus(V\otimes V)$.

Independently, the [core Hodge decomposition](../../../vortex-induced-triforce-refinement/core-hodge/) gives 17 cycle dimensions on the medial refinement of the eight-faced octahedral core. The stream values on 18 primal vertices determine the oriented face-dual currents, with one constant gauge direction. A five-dimensional visible component has a unique minimum squared-current lift; twelve independent midpoint stream differences remain invisible to the coarse edge read. These are available current patterns, not necessarily independent state amplitudes or excited vortices. The existing flywheel still comprises eight outer rings and a collective core; no new oscillator is introduced.

For dyadic depth n put m=2^n. The mesh has F=8m², E=12m² and V=4m²+2, so the cycle dimension is 4m²+1. The value 17 occurs at n=1 (secondary subdivision of the already central triangles), as opposed to 5, 65, 257 at the surrounding depths. The arithmetic agreement with 1+4² is exact at this depth, but it is not itself a physical selection theorem.

## 2. The physical symmetry of stream differences [T]

Let D be the oriented primal-edge difference matrix, with the edge orientation chosen consistently with the outward orientation of the core and its corresponding dual edge. Let U_g transport oriented dual currents and P_g permute primal stream vertices under a spatial isometry g. Direct orientation gives

    U_g D = det(g) D P_g.

An orientation-reversing transformation reverses the relation between an oriented surface edge and its dual. The extra determinant is therefore required, not chosen to obtain a desired trace. Since the kernel of D consists exactly of constants, the cycle character is

    χ_cycle(g) = det(g) (number of fixed primal vertices − 1).

The same formula applies to the coarse mesh. On the hidden midpoint functions, which vanish on all original vertices, there is no constant quotient. The minimum-norm visible lift is equivariant because the unit-edge metric is invariant under these isometries.

| Td permutation class | Refined core | Visible | Hidden | Abstract root-blind W |
|---|---:|---:|---:|---:|
| identity | 17 | 5 | 12 | 17 |
| transposition | -3 | -1 | -2 | 5 |
| double transposition | 1 | 1 | 0 | 1 |
| three-cycle | -1 | -1 | 0 | 2 |
| four-cycle | 1 | 1 | 0 | 1 |

In real A4 representations, write 1 for the trivial representation, E for the two-dimensional realification of the nontrivial complex characters, and T for the three-dimensional vector representation. The decompositions are

    core = 1 + 2E + 4T,
    W    = 3·1 + E + 4T,
    hidden = 1 + E + 3T,
    visible = E + T.

Their common subrepresentation has dimension 15, so an equivariant linear map has rank at most 15; this bound is attainable by matching the common summands. There is no equivariant linear isomorphism. In particular the two additional trivial coordinates of W cannot be identified with the extra E of the core. The twelve midpoint vertices carry a free transitive proper tetrahedral permutation action, explaining their regular representation. For improper symmetries the determinant twist matters.

## 3. Actual chamber inversion is not the trace-13 operator [T]

Spatial inversion g=-I sends each stream to minus its antipodal permutation. The 18 stream vertices form nine antipodal pairs; the one-dimensional constant gauge belongs to the negative sector. Thus actual inversion on the core has nine positive and eight negative dimensions, and trace one. On every dyadic refinement the antipodal action is free and the same reasoning gives trace one, although the dimension changes.

| Sector | Dimension | Inversion even | Inversion odd |
|---|---:|---:|---:|
| visible dipole | 3 | 3 | 0 |
| visible quadrupole | 2 | 0 | 2 |
| hidden midpoint cycles | 12 | 6 | 6 |
| total | 17 | 9 | 8 |

The hidden even part is 2T; the hidden odd part is 1+E+T. Thus the full physical-inversion-even circulation sector is 3T (dimension 9), and its odd sector is 1+2E+T (dimension 8). Exhaustive exact tests on the 48 signed coordinate permutations of the regular octahedron yield traces -7 (3 elements), -3 (6), -1 (8), 1 (30), 17 (identity). None gives 13. This rules out a single ordinary octahedral symmetry as the source of the desired denominator on this cycle space.

![Actual versus selective inversion](core_trace_comparison.svg)

## 4. A geometrically defined selective operator [T/D]

There is nevertheless an exact trace-13 operator. Let Pq project orthogonally onto the two visible quadrupole circulation directions, in the inherited unit-edge squared-current metric. The quadrupole lift comes from the even antipodal stream functions on the original six vertices after removing the constant. On the 17-dimensional cycle space define T = I - 2Pq. It is an involution of trace 13, preserves all hidden loops, and agrees with physical inversion on the visible lift. It differs from actual inversion on the six odd hidden directions; the difference has rank six. Equivalently, it reverses the quadrupole of the visible read without changing the internal residual. This is a symmetry-compatible *selective read*, not a spatial motion or a derived field evolution.

If a settlement operation preserved the hidden residual, preserved the visible dipole and inverted the visible quadrupole, its action on the cycle space would be this operator. These are additional physical premises, not implications of symmetry. The ratio of the full dimension to its trace is 17/13, but this calculation is distinct from the original 21-dimensional graded trace and does not explain why gravity should use a trace ratio rather than a resolvent, energy, or ordinary transport coefficient.

## 5. A dynamical selection rule for the established flywheel [T/D]

Let chamber inversion act on the complex site amplitudes by the permutation and centre-coordinate signs of Stage IX. The original H36 and the specified refined extension commute with this involution. Every pure parity state therefore retains its parity under the Hamiltonian. Although the state itself may acquire a minus sign, its bond current is bilinear, so its oriented current is inversion-even. The equivariant Hodge and visible projectors preserve this selection rule: the visible quadrupole cycle and the six hidden inversion-odd cycle directions vanish.

For a sum of even and odd amplitudes a+b, the current splits into J(a)+J(b)+Jcross(a,b), where the cross term is inversion-odd. Hence opposite-parity coherence is necessary for an odd current in the specified closed inversion-symmetric system, and can supply such a current; it is not sufficient for any prescribed pattern. A statistical incoherent mixture of the parity states would not give the cross term.

The Stage VII inversion-even sustained flywheel and the Stage IX odd collective excitation therefore do not, individually, exercise all 17 core cycle directions. This is not an absence of the core vortex: its visible dipole belongs to the even sector. The numerical Stage IX refinement at κ=4, with the same equal-child lift and an explicitly chosen tilted collective phase, gives the following peak norms over 161 samples on t∈[0,8]:

| Input | Visible quadrupole norm | Inversion-odd cycle norm |
|---|---:|---:|
| even | < 2e-15 | < 3e-15 |
| odd | < 1e-15 | < 3e-15 |
| coherent mixed | 0.0307853 | 0.1243574 |

These are dimensionless current norms, not measured stiffnesses or attenuation. The mixed state is a deliberately constructed test input, not a claim that the field generates it autonomously. The exact tests additionally verify the bilinear selection rule on integer-complex states and find explicit nonzero mixed-parity witnesses.

![Numerical parity selection](quadrupole_parity.svg)

## 6. Next physical test

The immediate objective is not to find another count of thirteen. Derive a boundary response from the native Hamiltonian and action that discriminates the visible dipole and quadrupole while tracking the hidden inversion-odd modes. In a linear model with inversion-symmetric H, their absence from a pure-parity current is exact, so a read that uses them requires an explanation of mixed-parity preparation, a state-dependent interaction, or a different observable. Compare actual projected response kernels, including their frequency dependence and metric, rather than fitting weights to 17/13. A physical connection between the core circulation and gravitational coupling must establish both the observable and the normalization independently. The selective involution gives a precise target and a counterexample to treating ordinary inversion as that target.

## Reproduce

`OPENBLAS_NUM_THREADS=1 python explore_core_trace.py` (NumPy, SciPy, SymPy, Matplotlib). The script imports the construction prefixes of the adjacent `core-hodge` and `core-flywheel` research; it does not run their full simulations. 196 fresh checks passed; 36 Hodge-prefix checks rerun, plus inherited geometry reconstruction checks. The exact symmetry tests use integer/rational matrices; the evolution uses numerical eigendecomposition. See [output](exploration_output.txt) and [CSV](parity_dynamics.csv). Upstream reviewed commit `d69739e984e5f1f8de5e4639d8fd0e7a2a8214b8`. No new physical constants, repository writes or Lean claims.
