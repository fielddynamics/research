# The root exchange on the address tree

*Abstract root-exchange traces, a projective addressing flag, and the limits of the physical identification · Gravity Field Dynamics (GFD) · Field Dynamics Research · November 2026*

`gravitational-constant` `coupling-polynomial` `root-exchange` `projective-plane` `closure-tree` `research`

---

## What this proves, and why it matters

GFD's Newton constant, graded [D] in `llms.txt` (premises: one factor of α per coupling level, and the combination rule, 21 as exponent and 17/13 as ratio, which `research/g_from_topology/` marks as proposed), is

$$G=\frac{17}{13}\,\alpha^{21}\,\frac{\hbar c}{m_e^2},$$

with 21, 17 and 13 the values of the coupling polynomial $f(K,s)=1+sK+K^2$ at TetA ($s=+1$), the Field Origin ($s=0$) and TetB ($s=-1$), for $K=4$.

The primary geometric candidate is the [recursive Triforce hierarchy](../../recursive-triforce-geometry/): four coupled face directions, each with four primary triangles and four medial children per primary triangle. Its maximal dyadic depth on the specified Flower lattice is two, conditional on using that fixed lattice. The resulting 64 paired addresses are not a second copy of the 64 corner pairs, nor 64 established independent degrees of freedom.

This note establishes distinct algebraic results:

1. On an abstract graded space $\mathbb C\oplus V\oplus(V\otimes V)$, leg reversal gives traces 21, 17, 13.
2. The time-diagonal axis and field conjugation select a pair of flags in $\mathrm{PG}(2,4)$, with strata 1, 4, 16. This is a result for the corner-pair representation, not a physical identification.
3. The corresponding frequency-adapted projective tree has invariant grades and a constructed involution with signs $+1,-1,+1$. Its determinant identity is conditional on this operator and attenuation law.
4. Cube inversion reverses four odd Walsh characters; it does not reverse time. Its induced action on an abstract graded tensor space gives the trace polynomial.
5. The actual recursive geometric tree is rotation-equivariant, but its pointing parity does not implement the proposed contrast grading. Its invariant dimension is 22; the corner-pair representation under spatial rotation has dimension 24. The two physical actions cannot be identified by relabelling.

Thus 17/13 is an exact ratio of abstract structural traces, not yet a derived physical stiffness, nor a result that forces the physical tree's settlement operator. The geometry, the computational representation and the dynamical read must be distinguished.

Status labels follow the read-and-rotation note: **[T]** exact algebra, **[O]** open.

## 1. The coupling polynomial is the root exchange [T]

Let $V$ be the $K$-dimensional leg space and $R=\mathbb C\oplus V\oplus(V\otimes V)$ the graded read space: the scalar, the four legs, the sixteen couplings. Its dimension is $1+K+K^2=21$.

The [read-and-rotation note](README.md) (Part D) defines the root exchange as $K\to-K$: TetB is TetA with the legs reversed. On $R$ that is the map $v\mapsto -v$ on each leg, so a block carrying $n$ legs picks up $(-1)^n$:

$$\Pi = P_0 - P_1 + P_2 .$$

$\Pi$ is an involution. Its $+1$ part is the scalar and the couplings, of dimension $E=1+K^2=17$. Its $-1$ part is the legs, of dimension $O=K=4$. These are the parity split $f=E+sO$ of the read-and-rotation note.

The graded identity $I_s=P_0+s\,P_1+P_2$ is then

$$\boxed{\,I_s=\frac{1+s}{2}\,\mathbb 1+\frac{1-s}{2}\,\Pi\,}$$

the identity at TetA, the root exchange at TetB, and their average, the projector onto the root-blind part, at the Field Origin. Taking traces gives the coupling polynomial for every $K$:

| State | Operator | Trace | Meaning |
|---|---|---|---|
| TetA, $s=+1$ | $\mathbb 1$ | 21 | dimension of the read space |
| Field Origin, $s=0$ | $(\mathbb 1+\Pi)/2$ | 17 | dimension of the root-blind part |
| TetB, $s=-1$ | $\Pi$ | 13 | trace of the root exchange |

$$\frac{17}{13}=\frac{\dim(\text{root-blind part})}{\operatorname{tr}(\text{root exchange})}=\frac{E}{E-O}.$$

In this abstract representation 17/13 is a ratio of traces/dimensions, not a flux-weighted statistic. That gravity uses this ratio is G's combination rule, which `research/g_from_topology/` marks as proposed; this note does not add to that premise.

**A second trace realization.** The unified closure notes use $C_s=1\oplus(I+s\tau)$ on $\mathbb C\oplus(V\otimes V)$, where $\tau$ swaps the legs. Since $\operatorname{tr}\tau=K$, $\operatorname{tr}C_s=f(K,s)$. This equality of traces does not identify operators of different dimensions, or identify either with physical pointing parity. The recursive geometry yields a precise $S_3$ obstruction to identifying pointing parity with tensor swap.

**Flux weights are a different functional.** The original weights 1/32 and 1/96 are an equal-child quadrature approximation, not the actual solid angles of second-level triangles. The corrected radial quadrature is given in [recursive Triforce geometry](../../recursive-triforce-geometry/). Neither structural trace nor quadrature by itself establishes the gravity source vertex.

## 2. Time-adapted projective flag [T]

The 64 ordered address pairs form $\mathbb F_4^3$, one $\mathbb F_4$ coordinate per spatial axis ([projective Walsh bridge](../../hadamard-null-cone-vortex-flywheel/PROJECTIVE_WALSH_G_BRIDGE.md)). The order-3 cycle on the ledger splits the 63 nonzero addresses into 21 orbits, the points of the projective plane $\mathrm{PG}(2,4)$.

Two symmetries act on this plane:
- the **closure rotation** $\sigma$: 120° about the time diagonal, which cycles the axes $x\to y\to z$;
- **conjugation** $\omega\leftrightarrow\bar\omega$, which exchanges the two orientations of the winding pair (vortex and antivortex).

Then:
- $\sigma$ fixes exactly three points. Only one of them, $(1,1,1)$, is also fixed by conjugation: the **time point**, the body diagonal.
- Exactly two $\sigma$-fixed lines pass through the time point, and conjugation swaps them: the **vortex line** and the **antivortex line**.
- Either line splits the 21 points into the time point, the 4 other points on the line, and the 16 points off it. Under the rotation, the 4 split as 1 fixed + 3 cycled, and the 16 as 1 fixed + five 3-cycles.

The orbit pattern matches the abstract tetrahedral leg and leg-pair permutation representations. This permits an abstract $C_3$ representation comparison, not an identification of the projective frequencies with actual face channels. Assigning the sign $-1$ to the four points of the line gives trace 13. This sign assignment is a defined projective operator; the physical identification is not established.

The same spatial rotation angle enters the characteristic polynomial $21=\det(K-R_{120^\circ})$ in Part A of the read-and-rotation note.

## 3. A time-adapted projective tree [T]

The closure tree reads the 64 addresses in three nested digits, coarse to fine, and its levels are spanned by Walsh characters. A function of the first digit alone is built from characters whose frequency lies along the first coordinate. So each tree level corresponds to a stratum of *frequencies*, and the tree's flag is set by which frequency directions its digits run along.

Compare two trees:

| | x-axis tree (current notes) | Time-adapted tree |
|---|---|---|
| Coarse frequency | $x$ axis | time point $(1,1,1)$ |
| First two frequencies span | the $x$–$y$ coordinate line | the vortex (or antivortex) line |
| Levels invariant under the closure rotation | no | yes |
| Constructed projective involution on the 1, 4, 16 invariant levels | mixed signs on the 4 and the 16 | exactly $+1$, $-1$, $+1$ |

For the time-adapted tree the result does not depend on the third basis direction: all 16 choices give the same tree. It holds identically for the vortex and the antivortex line.

For the constructed projective involution $\Pi_{\rm proj}$ the graded identity is $I_s=\tfrac{1+s}{2}\mathbb 1+\tfrac{1-s}{2}\Pi_{\rm proj}$. Consequently,

$$\det(\alpha^{I_s})=\alpha^{1+4s+16}:\quad\alpha^{21},\ \alpha^{17},\ \alpha^{13}.$$

This is a conditional determinant identity for that representation. The verifier defines the negative flag subspace; it does not derive that sign assignment from geometric chamber inversion on the physical tree.

## 4. Cube inversion on the Walsh leg space [T]

On the abstract four-leg space the sign reversal used in section 1 has a geometric realization in the odd cube Walsh characters.

The scheme proof's root exchange is spatial inversion, which maps TetA's corners $s_i$ onto TetB's corners $-s_i$. On functions on the cube's eight corners, inversion fixes the four even Walsh characters $1, xy, yz, zx$ and reverses the four odd ones $x, y, z, xyz$. So exactly $K=4$ modes flip:
- On TetA the odd characters $(xyz, x, y, z)$ are exactly the Triforce read's Hadamard legs $U=[1;s_i]/2$.
- On TetB the same characters are $-U$: inversion reverses all four legs.

So $K\to-K$ represents inversion on the chosen four odd leg characters, and its induced action on scalar $\oplus$ legs $\oplus$ leg pairs has signs $+1,-1,+1$ and trace 13. This does not establish the corresponding physical contrast operator.

The leg's "time" row is the chamber character $xyz$, which is $+1$ on TetA and $-1$ on TetB. It flips because it distinguishes the chambers, not because time reverses. The Triforce read's TetB dictionary $\operatorname{diag}(1,-1,-1,-1)\,U$ is the same leg block with that row renormalised to $+1$. This fits "TetB is not reverse time".

## 5. One recursive geometry; distinct computational representations [T/D]

The [recursive Triforce construction](../../recursive-triforce-geometry/) supplies the geometrically defined hierarchy: coupled face, medial tile, medial child. The central child is retained at both levels. Pairing complementary chamber faces defines 64 terminal addresses; it does not merge the physical chamber surfaces. The depth-two stopping criterion requires the existing fixed Flower lattice and remains conditional as physics.

| | Recursive geometric addresses | Ordered corner-pair representation |
|---|---|---|
| Address | face, primary tile, secondary tile | ordered pair of cube corners |
| Physical $120^\circ$ rotation | one fixed leaf, 21 three-cycles | four fixed pairs, 20 three-cycles |
| Invariant dimension | 22 | 24 |
| Physical relation | primary candidate geometry | computational representation; physical map open |

The physical rotation commutes with each prefix averaging projection. The prefix invariant dimensions at depths 0, 1, 2, 3 are 1, 2, 6, 22, so the invariant contrast dimensions are 1, 4, 16. This is not a proof that an invariant contrast belongs to one particular physical reader. The projective XOR cycle is another operation, not the spatial rotation. A rotation-equivariant bijection to ordered corner pairs is impossible.

The second-level pointing operator $Q=J\otimes J$, $J=\operatorname{diag}(-1,1,1,1)$, has the 10/6 split per face and structural trace 4. On the rotation-invariant leaf space it has 14 positive and 8 negative coordinates; it does not preserve the uniform-mean-zero contrast space. The compression has 13 positive unit, 7 negative unit and one $-1/4$ eigenvalue. It is not the projective involution. Nor can it be identified with connection swap under the full face symmetry: their signed reflection traces differ. The 40/24 match is combinatorial, not a proof of torsion.

## 6. What this does not settle

- **[O] Physical refinement:** derive the fixed lattice restriction, occupation of its maximal dyadic depth and the fine field dynamics from the existing action. The H36 tile model does not establish the secondary amplitudes.
- **[O] Physical settlement operator:** derive the actual chamber exchange and its action on contrast modes. Do not impose the projective sign grading or restore a second physical ledger merely to match dimensions.
- **[T/O] Representations:** the physical-rotation obstruction rules out a direct equivariant relabelling of ordered corner pairs. A different computational read can be investigated only with its explicit map and transformation law.
- **[O] Untouched premises.** Why each level attenuates by exactly α, why gravity takes the collective (determinant) read rather than a single channel, the drained/bound label from the drain, and the value of $a_0$ are all still open.

## Verification

[`verify_root_exchange_tree.py`](verify_root_exchange_tree.py) (NumPy, SymPy) checks the abstract trace, projective flag, prescribed sign operator, cube Walsh inversion and permutation-tree identities. Its [historical output](root_exchange_tree_output.txt) records 40 checks; it does not check autonomous physical exchange, attenuation or subchannel dynamics. See [recursive Triforce verification](../../recursive-triforce-geometry/) for the independent geometric and symmetry tests.
