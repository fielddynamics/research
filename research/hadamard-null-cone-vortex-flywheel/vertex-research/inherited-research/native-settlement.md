# The settlement observable of the eight-vortex flywheel: memory, conservation and junctions

*Gravity Field Dynamics · Field Dynamics Research · November 2026*

**Status.** Exact finite-dimensional theorems for the specified Stage VII and Stage IX Hamiltonians, together with a conditional shared-edge variational model. The verifier records 120 new assertions, including four numerical trajectory checks, and reruns 16 reconstruction checks. No new Lean proof, gravitational normalization or physical field action is claimed. Repository basis `d69739e984e5f1f8de5e4639d8fd0e7a2a8214b8`.

## 1. What is being settled?

The [native root grading](../core-native-grading/) provides a concrete realization of the old 21/17/13 polynomial. Its read space R consists of the 17 chamber-even amplitudes together with the four odd central-face amplitudes. This is a well-defined geometric read, but it is not an invariant space of the native flywheel. We therefore ask whether the native action independently selects a conserved read, and what the exact response of the discarded coordinates is. The [boundary register](../../CLOSURE_ENGINE_INTERNALS.md) and [unified action](../../../unified-closure-action/unification/UNIFIED_CLOSURE_ACTION.md) establish a separate static source-charge identity. We cannot assume that a count, an optical amplitude, a circulation moment and a physical rest energy are the same observable.

All eight stellation rings, the eight faces of the shared octahedron and the scalar/directional Origin coordinates are retained in the native models. The Stage VII witness has 33 coordinates and the Stage IX model has 36. No extra independently prescribed core oscillator is used.

## 2. The exact conservation obstruction

Write P for the orthogonal projector onto R and Q=I−P. For a Hermitian H and a solution of i dψ/dt=Hψ, the read occupation is ψ†Pψ and its derivative is i ψ†[H,P]ψ. Consequently read occupation is conserved for every initial state exactly when [H,P]=0. Both native models violate this condition.

A more general statement holds for any Hermitian quadratic observable M supported by the read, meaning M=PMP. If [H,M]=0, M annihilates Q and every H^k Q, so its range is contained in

$$K=(\operatorname{span}\{\operatorname{im}Q,H\operatorname{im}Q,H^2\operatorname{im}Q,\ldots\})^\perp.$$

Conversely K is H-invariant and its orthogonal projector is a conserved positive observable supported in R. Thus dim K is the largest possible rank of any conserved read-supported quadratic, even allowing arbitrary non-diagonal read weights. This argument does not assume the observable is positive; the projector attains the bound with positivity.

| Model | dim R | dim K | Read history hull | Dark dimension |
|---|---:|---:|---:|---:|
| Stage VII | 21 | 17 | 28 | 5 |
| Stage IX | 21 | 18 | 30 | 6 |

In Stage IX, K consists of the full even space plus the isolated odd uniform central mode. In Stage VII, it is the even space alone. These are exact ranks, not fitted cutoffs. Neither model supports a rank-21 conserved quadratic on the proposed read. This does not exclude a snapshot rather than a conserved quantity, or a driven or extended settlement model.

There is also a stronger identifiability obstruction. The invariant dark space is the orthogonal complement of span{R,HR,...}. In Stage IX it contains eigenvectors of energies 0 and 2, while in Stage VII it contains eigenvectors of energies 1/2 and 3/2. Normalize any two such vectors to unit norm. Their entire coherent R histories agree (both identically zero), but their Hamiltonian expectations differ. Even the complete ideal read history therefore cannot reconstruct the total H energy for arbitrary states. The same argument can be applied with a shared visible state and equal orthogonal dark norm, so the ambiguity is not restricted to zero observations. This is not a statement that those model energies are measured rest mass.

For a diagonal observable M=diag(m_i), [H,M]_{ij}=H_{ij}(m_j−m_i). The native nonzero coupling graph is connected. Hence the only diagonal conserved quadratic observables are multiples of total occupation. This is the global phase Noether charge of the stipulated complex-amplitude action, not an independently derived electric charge or mass. A site-resolved phase symmetry with links would require additional gauge data. The static boundary source-charge of the gravitational action is a different conservation identity, whose coupling to these amplitudes remains to be derived.

## 3. Exact memory of the odd central read

Let x=Pψ and y=Qψ. With A=PHP, D=QHQ and L=QHP restricted to their subspaces,

$$i\dot x=Ax+L^\dagger y,\qquad i\dot y=Lx+Dy.$$

Eliminating y gives the exact causal equation

$$i\dot x(t)=Ax(t)+L^\dagger e^{-iDt}y(0)-i\int_0^t L^\dagger e^{-iD(t-u)}L x(u)\,du.$$

The initial complement is an independent forcing term. Thus even with a known H, an instantaneous x is not a complete dynamical state. In the resolvent the projected operator is A+L†(z−D)^{-1}L. This identity follows from the original quadratic action, equivalently the two block equations, and is not a proposed phenomenological damping law.

The entire even sector is invariant. The memory of the 21-read lies in its four odd central modes. In Stage IX the odd scalar is isolated, while each odd vector direction has the same exact four-coordinate multiplicity block:

$$M=\begin{pmatrix}-2&2&-1&0\\1&1&1&0\\-4&4&-1&-1\\0&0&-8&0\end{pmatrix}.$$

The third coordinate is the central amplitude; the other three are the two outer amplitudes and the polar Origin. The block is self-adjoint in the positive Gram metric diag(block[[3,−1],[−1,3]],1,1/8). Direct elimination gives

$$\Sigma(z)=\frac{16(z^2-2)}{z(z^2+z-4)},\qquad G_{-,1}(z)=\frac{1}{z+1-\Sigma(z)}.$$

The memory has three uncancelled poles, at 0 and (−1±√17)/2, with respective residues 8 and 4∓12/√17, all positive. The first six moments are 16,−16,48,−112,304,−752; the 3×3 Hankel matrix from the first five has positive determinant. The zero-frequency pole of the eliminated block makes the projected core Green function vanish at z=0. A frequency-independent static replacement of the memory cannot capture this antiresonance. The zero pole is not a pole of the full projected response. The three triply replicated memory directions account for exactly the nine additional reachable amplitudes needed by the 21-read in Stage IX. The remaining six amplitudes are dark to that read.

![Native and conditional junction read dynamics](read_memory_dynamics.svg)

The plot starts in a normalized odd central vector and compares the unmodified Stage IX Hamiltonian with the conditional junction action of section 4. In both cases total norm is conserved, although the read occupation can become very small. Time and energies are dimensionless. This is not gravitational mass loss, a dissipative drain or a proof of a physical clock.

## 4. The geometry supplies a plausible variational origin for equal base and column bonds

The native primary tiles have 36 distinct geometric edges: 24 edges join two lateral tiles of one outer ring, and twelve octahedral edges each meet four tiles. Every geometric edge has squared length two in the normalized cube coordinates. Each four-tile edge meets two lateral tiles (the transpose pair X⁺_ij and X⁻_ji) and two central tiles (y⁺_i and y⁻_j). This is an actual junction of the two chamber surfaces, not four separate geometric edges. The 96 non-Origin native tile bonds are exactly the unordered pairs of incident tiles at these junctions. The proof verifies all 36 edges directly.

![The four-tile edge junction](shared_edge_junction.svg)

Suppose one shared complex edge variable q_e mediates the incident tile amplitudes ψ_i through the positive quadratic form

$$\mathcal E_e=\sum_{i\sim e}g_i|\psi_i-q_e|^2,\qquad g_i>0.$$

Stationarity in q_e gives q_e=Σg_iψ_i/Σg_i, and substitution gives the exact weighted clique Laplacian

$$\mathcal E_e^{\rm eff}=\frac{1}{\sum_i g_i}\sum_{i<j}g_i g_j|\psi_i-\psi_j|^2.$$

If the two lateral branches have conductance g_L and the two central branches have conductance g_C, the resulting existing bond types obey

$$d=-\frac{g_L^2}{2(g_L+g_C)},\quad k=-\frac{g_C^2}{2(g_L+g_C)},\quad b=a=-\frac{g_Lg_C}{2(g_L+g_C)},\qquad dk=b^2.$$

The equal base and column bonds are therefore a consequence of a common mediator with equal access within each branch family, not a separately adjusted equality. The branch assumption is an additional local constitutive premise. Tetrahedral symmetry alone does not force it, and the old Stage VII witness does not satisfy dk=b². No claim is made that a unique physical mediator is already derived from SST.

Equal conductances on all branches give off-diagonal hopping −g/2 at two-tile edges and −g/4 at four-tile edges. Taking g=4 merely sets the dimensionless tile coupling unit. It gives ring r=−2 and d=b=a=k=−1. The diagonal terms are also determined by the action: 7 on each lateral tile and 9 on each central tile. The tile-only constant mode is then in the kernel, in contrast to the native adjacency-only hopping. The tests retain the original scalar and polar Origin bonds separately, without claiming the junction action derives them or that the combined H is a positive mechanical energy.

This conditional action gives a counterexample to treating uniform pair hopping as the unique geometry-derived choice: the same surface has different junction valences, and eliminating identical branches automatically accounts for that distinction. Both the full junction Laplacian and its off-diagonal-only variant are tested. The latter is an algebraic diagnostic, not the result of eliminating the stated energy.

## 5. A robust thirteen for a class of junction models

When b=a, the uniform odd central amplitude decouples exactly from both lateral and Origin amplitudes and has energy e_c−3k. The actual graph reduces the odd vector sector to

$$M_- =\begin{pmatrix}e+2r&-r-d&b&0\\-d&e-r&-b&0\\4b&-4b&e_c+k&p\\0&0&8p&e_0\end{pmatrix},$$

where p is the polar Origin bond coefficient. For q=(0,0,1,0)^T, direct symbolic expansion gives

$$\det[q,M_-q,M_-^2q,M_-^3q]=-32b^2pr\big[d^2+dr+2r^2-(e-e_0)^2-r(e-e_0)\big].$$

Thus, whenever the displayed expression is nonzero, the four central odd inputs generate precisely one uniform scalar and four vector triplets: 13 amplitude directions. For e=e_0, the bracket is (d+r/2)^2+7r²/4, strictly positive if r≠0. The result is therefore robust over a parameter family rather than an isolated numerical choice. The explicit native and junction-action examples both have rank progression 4,7,10,13,13. The latter also has nonzero determinant with its derived site terms. All expressions are checked symbolically on the actual 36-coordinate graph.

But with the **same** four normalized even central inputs, both the native and the junction-action examples have reachability 12 rather than 17. The leading high-frequency spectral mass is four in each parity sector; the response is not a dimension count. This is a useful strengthening of the case for an odd-core rank of thirteen under the specified junction premise, not a derivation of 17/13 as a physical gravitational ratio.

## 6. The research programme now has a specific decision point

The 17 even amplitude inventory, the 17 circulation patterns, the abstract 21/17/13 trace grading and the conditional odd-core response rank are different objects. The native dynamics and the static boundary registration action do not yet identify them. It would be premature to use the trace ratio as a physical impedance or attenuation. The previous selective quadrupole reversal is not needed here.

The next action-level derivation should specify which boundary variables enter the local field action, and derive their conjugate charge using a common uniform shift. An interface link variable and a shared-edge mediator are plausible different degrees of freedom, not interchangeable. In particular, a physical field theory must explain (i) how a boundary read detects or excludes the dark energy inventory, (ii) why the junction branches obey the stated variational law, (iii) whether the frequency-dependent memory becomes a controlled static limit with an independently selected frequency or scale, and (iv) how the resulting source couples universally to the gravitational potential. The existing weak-field source and G normalization cannot be reinserted as though they had been derived from the microscopic flywheel.

The most immediate test is to introduce actual dynamical edge variables rather than instantaneous minimizers and derive their conservative response from a stated action. In the zero-inertia limit the clique expression must be recovered, and at finite inertia the mediator introduces its own poles. A common time or length scale, not a fit to 17/13, must select any effective approximation. This provides a falsifiable bridge to the next proof, with the dark-state obstruction as a required check.

## Reproduce

From this directory, with the previously integrated `../core-flywheel/` present, run `OPENBLAS_NUM_THREADS=1 python explore_settlement.py` (NumPy, SymPy, SciPy and Matplotlib). [Output](exploration_output.txt), [trajectory data](settlement_dynamics.csv). Both diagrams are included as SVG and PNG. This study makes no changes to the verified Proof 23 or the SST action.
