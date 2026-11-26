# The root exchange on the address tree

*Why 17/13 needs no weighting, and which way the closure tree must be read · Gravity Field Dynamics (GFD) · Field Dynamics Research · November 2026*

`gravitational-constant` `coupling-polynomial` `root-exchange` `projective-plane` `closure-tree` `research`

---

## What this proves, and why it matters

GFD's Newton constant is

$$G=\frac{17}{13}\,\alpha^{21}\,\frac{\hbar c}{m_e^2},$$

with 21, 17 and 13 the values of the coupling polynomial $f(K,s)=1+sK+K^2$ at TetA ($s=+1$), the Field Origin ($s=0$) and TetB ($s=-1$), for $K=4$.

The [unified closure research](../../unified-closure-action/) builds a 64-address closure tree whose three levels carry 1, 4 and 16 invariant contrast modes. Attenuating each level gives $\alpha\cdot\alpha^4\cdot\alpha^{16}=\alpha^{21}$. But that work had to *choose* which level plays the part of the legs, the term $sK$, and it called that choice a free "flag". If the choice is free, then 17 and 13 on the tree are a convention, and 17/13 is not geometry.

This note shows the choice is not free. Five results:

1. **The coupling polynomial is the root exchange.** On the graded read space, the graded identity is a mix of the identity and the root exchange, so 21 is the dimension, 13 is the exchange's trace, and 17 is the dimension of its root-blind part. Nothing is weighted.
2. **The closure rotation fixes the legs.** In the projective plane over $\mathbb F_4$ that the tree lives on, the 120° rotation about the time diagonal, together with the vortex/antivortex conjugation, selects one point and one line through it. That flag splits the 21 points as 1 + 4 + 16, with the same rotation pattern as the tetrad's scalar, four legs and sixteen leg pairs.
3. **Read along the time diagonal, the tree is the polynomial.** With the tree's digits aligned to that flag, every tree level is invariant under the closure rotation, and the root exchange acts as exactly $+1,-1,+1$ on its 1, 4 and 16 levels. Read along the x-axis, as the unified closure notes currently do, neither holds.
4. **The exchange is the cube's inversion.** Inversion reverses exactly four Walsh modes of the cube, and on TetA they are the Triforce read's four Hadamard legs. So $K\to-K$ is derived from the geometry, not assumed, and it is not a time reversal.
5. **The physical tree needs no flag.** Two different 64-address ledgers are in use. On the physical one (face, tile, subchannel) the closure rotation permutes the tiles exactly and the tree's readers are scalar, legs and leg pairs by construction. The flag problem belongs only to the corner-pair ledger, where the time flag of results 2 and 3 resolves it.

So 17/13 on the tree is forced by the rotation and the root exchange. The only thing left to choose is the handedness, vortex or antivortex, and both give identical numbers.

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

A trace counts each state once. That is why no weighting enters: 17/13 is a count, not a flux.

**The swap realization is the same thing.** The unified closure notes use $C_s=1\oplus(I+s\tau)$ on $\mathbb C\oplus(V\otimes V)$, where $\tau$ swaps the two legs of a pair. Its trace is $1+K^2+s\operatorname{tr}\tau$, and $\operatorname{tr}\tau=K$, because the swap fixes exactly the $K$ self-pairs $e_i\otimes e_i$. Those self-pairs are the legs embedded in the couplings. So $\operatorname{tr}C_s=f(K,s)$ too.

**Flux weights are a different functional.** The solid-angle weights (1/32 and 1/96) register how much mass a field carries, $w^Tx$. They are not a trace. Giving the self-pairs the central Triforce tile's flux share produces 9/17, but that mixes the mass register with the coupling count. G reads the count.

## 2. The closure rotation fixes the legs [T]

The 64 ordered address pairs form $\mathbb F_4^3$, one $\mathbb F_4$ coordinate per spatial axis ([projective Walsh bridge](../../hadamard-null-cone-vortex-flywheel/PROJECTIVE_WALSH_G_BRIDGE.md)). The order-3 cycle on the ledger splits the 63 nonzero addresses into 21 orbits, the points of the projective plane $\mathrm{PG}(2,4)$.

Two symmetries act on this plane:
- the **closure rotation** $\sigma$: 120° about the time diagonal, which cycles the axes $x\to y\to z$;
- **conjugation** $\omega\leftrightarrow\bar\omega$, which exchanges the two orientations of the winding pair (vortex and antivortex).

Then:
- $\sigma$ fixes exactly three points. Only one of them, $(1,1,1)$, is also fixed by conjugation: the **time point**, the body diagonal.
- Exactly two $\sigma$-fixed lines pass through the time point, and conjugation swaps them: the **vortex line** and the **antivortex line**.
- Either line splits the 21 points into the time point, the 4 other points on the line, and the 16 points off it. Under the rotation, the 4 split as 1 fixed + 3 cycled, and the 16 as 1 fixed + five 3-cycles.

That is exactly how the same rotation acts on the tetrad: of the four legs, one lies on the axis and three are cycled; of the sixteen leg pairs, one is fixed and fifteen fall into five 3-cycles. So the flag set by the time axis and a winding orientation reproduces scalar + legs + couplings, rotation pattern included. Its root exchange, $-1$ on the 4 points of the line, has trace $1-4+16=13$.

This is the same 120° rotation whose characteristic polynomial gives $21=\det(K-R_{120^\circ})$ in Part A of the read-and-rotation note.

## 3. Read along the time diagonal, the tree is the polynomial [T]

The closure tree reads the 64 addresses in three nested digits, coarse to fine, and its levels are spanned by Walsh characters. A function of the first digit alone is built from characters whose frequency lies along the first coordinate. So each tree level corresponds to a stratum of *frequencies*, and the tree's flag is set by which frequency directions its digits run along.

Compare two trees:

| | x-axis tree (current notes) | Time-adapted tree |
|---|---|---|
| Coarse frequency | $x$ axis | time point $(1,1,1)$ |
| First two frequencies span | the $x$–$y$ coordinate line | the vortex (or antivortex) line |
| Levels invariant under the closure rotation | no | yes |
| Root exchange on the 1, 4, 16 invariant levels | mixed signs on the 4 and the 16 | exactly $+1$, $-1$, $+1$ |

For the time-adapted tree the result does not depend on the third basis direction: all 16 choices give the same tree. It holds identically for the vortex and the antivortex line.

So on the time-adapted tree the graded identity is literally $I_s=\tfrac{1+s}{2}\mathbb 1+\tfrac{1-s}{2}\Pi$ acting on the three contrast levels, and the three stage determinants are

$$\det\!\big(\alpha^{I_s}\big)=\alpha^{\,1}\cdot\alpha^{\,4s}\cdot\alpha^{16}=\alpha^{f(K,s)}:\quad\alpha^{21},\ \alpha^{17},\ \alpha^{13}.$$

The tree, the coupling polynomial and the root exchange are one structure.

## 4. The exchange is the cube's inversion [T]

Section 1 used the read-and-rotation definition, $K\to-K$. It follows from the geometry.

The scheme proof's root exchange is spatial inversion, which maps TetA's corners $s_i$ onto TetB's corners $-s_i$. On functions on the cube's eight corners, inversion fixes the four even Walsh characters $1, xy, yz, zx$ and reverses the four odd ones $x, y, z, xyz$. So exactly $K=4$ modes flip:
- On TetA the odd characters $(xyz, x, y, z)$ are exactly the Triforce read's Hadamard legs $U=[1;s_i]/2$.
- On TetB the same characters are $-U$: inversion reverses all four legs.

So $K\to-K$ is inversion acting on the legs, and on scalar ⊕ legs ⊕ leg pairs it gives $+1,-1,+1$ and trace 13.

The leg's "time" row is the chamber character $xyz$, which is $+1$ on TetA and $-1$ on TetB. It flips because it distinguishes the chambers, not because time reverses. The Triforce read's TetB dictionary $\operatorname{diag}(1,-1,-1,-1)\,U$ is the same leg block with that row renormalised to $+1$. This fits "TetB is not reverse time".

## 5. Two ledgers share the number 64 [T]

The research uses two different 64-address ledgers. Keeping them apart removes the flag problem from the physical one.

| | Tile ledger | Pair ledger |
|---|---|---|
| Source | [Triforce tetrad read](../../hadamard-null-cone-vortex-flywheel/TRIFORCE_TETRAD_READ.md), [three sub-reads](../../hadamard-null-cone-vortex-flywheel/THREE_SUBREAD_CLOSURE.md) §1 | [projective Walsh bridge](../../hadamard-null-cone-vortex-flywheel/PROJECTIVE_WALSH_G_BRIDGE.md), the π walk |
| Address | face $i$, tile $(i,j)$ at vertex $j$, subchannel | ordered pair of cube corners $(u,v)$ |
| Digit alphabet | the four legs | a bit pair along one spatial axis, read as $\mathbb F_4$ |
| Closure rotation | permutes the legs: $(i,j)\to(\pi i,\pi j)$ | cycles the axes $x\to y\to z$ |

**On the tile ledger no flag is needed.** The 120° rotation about $s_0=(1,1,1)$ fixes leg 0 and cycles legs 1, 2 and 3. It carries tile $(i,j)$ exactly onto tile $(\pi i,\pi j)$. Every level of the face → tile → subchannel tree commutes with it. The invariant contrasts are 1, 4 and 16, one per reader: the root, the four face readers and the sixteen tile readers. The readers carry 0, 1 and 2 leg indices, so the tree's nodes are scalar ⊕ legs ⊕ leg pairs, and the middle level is the faces.

**On the pair ledger the flag must be the time flag** (sections 2 and 3). There the closure rotation moves digits between levels unless the tree is read along the time diagonal. The three-sub-read note's §3 applies this ledger's axis pairing to the tree's digits. That is what produced the free flag.

## 6. What this does not settle

- **[O] The exchange on the tile ledger, level by level.** Section 4 fixes the exchange on legs, and section 5 shows the tile tree's readers carry 0, 1 and 2 leg indices. What remains is an explicit operator on the dual-chamber tile ledger (TetA ⊕ TetB) showing the contrast levels pick up exactly $+1,-1,+1$. [Recursive Triforce geometry](../../recursive-triforce-geometry/) now gives the subchannel a geometry, as the second medial subdivision of each tile. It also shows that *pointing parity* (up versus down triangles) is not that operator: on the invariant sector it does not reproduce the 1/4/16 grading.
- **[T] No equivariant map between the two ledgers.** [Recursive Triforce geometry](../../recursive-triforce-geometry/) shows the closure rotation has 22 invariant dimensions on the tile tree and 24 on the corner pairs, so no rotation-equivariant bijection exists. The corner-pair ledger is a computational representation, not a second physical ledger.
- **[O] Untouched premises.** Why each level attenuates by exactly α, why gravity takes the collective (determinant) read rather than a single channel, the drained/bound label from the drain, and the value of $a_0$ are all still open.

## Verification

[`verify_root_exchange_tree.py`](verify_root_exchange_tree.py) (NumPy, SymPy) checks every statement above exactly: 40 checks, all passing ([output](root_exchange_tree_output.txt)). It rebuilds the projective plane, the pair-ledger trees, the Walsh characters, the cube inversion and the Triforce tile tree from scratch, and tests every choice of the third basis direction for both handedness choices.
