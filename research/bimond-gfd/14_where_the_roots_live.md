# 14 — Where the two roots live in the connection

*Research note, Field Dynamics Research, 2026-11-12. Status: deduction with checks, not a paper. Script: [`14_where_the_roots_live.py`](14_where_the_roots_live.py), 27 checks (numpy, sympy). Follows [note 13](13_connection_irreducibles.md).*

## The question

Letter 2 says that a torsion-free connection cannot distinguish TetA from TetB, and that the torsion is "the necessary carrier" of the distinction. Note 13 split the 64 connection components into pieces that no change of frame can mix. This note asks the next question: starting from the frame itself, where exactly does the difference between the two roots appear? It is answered by deduction, with each step checked.

Throughout, the two roots are frames $e$ and $\tilde e = L\,e$ on the same metric, with $L(x)$ a Lorentz transformation at each point. TetB is the case where $L$ is in the parity component ($\det L = -1$).

## Result 1: the covariant form of 64 = 40 + 24

At a point, a frame has $4 \times 16 = 64$ first derivatives $\partial_\mu e^a{}_\nu$. The script checks, for the identity frame and for a random frame, that these are, one to one:

$$\underbrace{\partial_\mu e^a{}_\nu}_{64} \;\longleftrightarrow\; \underbrace{\partial_\mu g_{\nu\rho}}_{40} \;\oplus\; \underbrace{T^a{}_{\mu\nu}}_{24}.$$

The 24 that the metric cannot see is exactly the set of local Lorentz changes of the frame, $\mathfrak{so}(1,3) \otimes V^* = 6 \times 4$.

**Why it matters for GFD.** This is the coordinate-free version of the 40/24 split of Letter 2 and the Gram paper. Note 13 showed that the index grid's diagonal 16 is not Lorentz-invariant. Here the split needs no grid:
- the 40 are the derivatives of the metric, which is the Gram product $e^T\eta e$ and so root-blind (Gram Lemma 1);
- the 24 are the torsion, the derivatives of the frame that the Gram product does not see. Result 2 shows that these carry the second root.

**Status: standard** in teleparallel geometry (the Weitzenböck connection). The GFD use is the reading: the 40/24 split is the derivative of the Gram map.

A companion check: "symmetric in the lower pair" (40, torsion-free) and "antisymmetric in the outer pair" (24, metric-compatible) meet only in zero and together span the 64. That is the fundamental theorem of Riemannian geometry, the uniqueness of the Levi-Civita connection, stated as linear algebra. Letter 2's Lemma rests on it.

## Result 2: the 40 is root-blind and the 24 carries the second root

Take the second root as the Gram paper defines it, $e^i{}_\mu \to -e^i{}_\mu$, that is $\tilde e = P e$ with $P = \mathrm{diag}(1,-1,-1,-1)$ on the frame index. The script checks, on a nontrivial (twisted and curved) frame:

- **The 40 are the same for both roots.** $\tilde e^T\eta\,\tilde e = e^T\eta\,e$, so the metric and all 40 of its derivatives agree. This is Gram Lemma 1 carried to the connection, and it is Letter 2's Lemma.
- **The 24 change with the root.** In its frame form, $T^a = de^a$, the torsion of the second root is $\tilde T^a = P^a{}_b\,T^b$: the spatial components reverse sign, exactly as the vielbein does. The torsion is rank 1 in the frame index, the parity-odd rank of Letter 2's argument, while the metric is rank 2 and even.

So, in the jet split of Result 1, the second root leaves the 40 fixed and acts on the 24. That is the 40 = TetA-blind / 24 = TetB identification of Letter 2, here without the index grid.

**A trap to avoid.** If the torsion is written with coordinate indices, $T^\lambda{}_{\mu\nu} = e_a{}^\lambda T^a{}_{\mu\nu}$, the inverse frame applies $P$ a second time and the sign cancels. The same happens to the frame's connection $\Gamma = e^{-1}\partial e$, which has one frame and one inverse frame, and to any relative-frame difference $L^{-1}\partial L$ (unchanged when $L \to PL$). This is the same cancellation that makes $g = e^T\eta e$ root-blind: a quantity contracted with the frame twice cannot see the root. The root has to be read where the frame index is left free, as in the Gram cross-coupling $M_1^T M_2$, or through the orientation. In coordinate form the axial torsion vector $a^\mu = \tfrac16\varepsilon^{\mu\nu\rho\sigma}T_{\nu\rho\sigma}$, built with $\varepsilon = \det(e)\,[\mu\nu\rho\sigma]$, still flips sign between the roots.

**Relative frames.** Two frames on one metric related by a position-dependent $L(x)$ have connections that differ by $N^\lambda{}_{\mu\nu} = (L^{-1}\partial_\mu L)^\lambda{}_\nu$. The script checks this for a general $L = R(f_1)\,B(f_2)$. Each $L^{-1}\partial_\mu L$ lies in $\mathfrak{so}(1,3)$, so $N$ is metric-compatible: it lies in the 24. Result 4 uses this.

The orientation reading agrees with the [bimetric proof](../../proofs/bimetric-two-potential-energy/), whose Lemma 1 gets $\alpha = -\beta$ from $\det(e)$.

## Result 3: which action terms see the root

Every first-order tetrad action term is a 4-form built from $e^a$, $T^a$ and $R^{ab}$, contracted with $\eta_{ab}$ or $\varepsilon_{abcd}$. Under a constant parity, $\eta_{ab}$ is invariant and each $\varepsilon$ contributes $\det P = -1$, which the script checks. Counting factors of $\varepsilon$ then sorts the terms:

| Term | Factors of $\varepsilon$ | Under the second root |
|---|---|---|
| Einstein–Hilbert (Palatini), $\varepsilon_{abcd}\,e^a e^b R^{cd}$ | 1 | flips sign |
| cosmological, $\varepsilon_{abcd}\,e^a e^b e^c e^d$ | 1 | flips sign |
| Euler, $\varepsilon_{abcd}\,R^{ab}R^{cd}$ | 1 | flips sign |
| Holst, $e_a e_b R^{ab}$ | 0 | unchanged |
| Nieh–Yan, $T^aT_a - e_a e_b R^{ab}$ | 0 | unchanged |
| Pontryagin, $R_{ab}R^{ab}$ | 0 | unchanged |

This settles target #2 from the earlier list. With equal couplings, the TetB root enters the Einstein–Hilbert term *and* the cosmological term with the opposite sign. The first is BIMOND's $\alpha = -\beta$. The second says a vacuum term written in tetrad form is also root-odd. The Holst term, which carries the Barbero–Immirzi parameter of loop quantum gravity, is the same for both roots.

**Status:** the transformation of $\eta$ and $\varepsilon$ is checked; the table follows by counting. It is standard representation theory; the GFD content is its reading as root-blind versus root-resolving.

## Result 4: what pushes slow matter, and what carries handedness

A slow particle moving on the connection of $Le$ instead of $e$ feels the extra acceleration $-N^i{}_{(00)}$. From Result 2:

$$-N^i{}_{(00)} = -(L^{-1}\partial_t L)^i{}_0 ,$$

the boost part of the time derivative: **the rate at which the relative rapidity changes**, that is, the relative acceleration of the two frames' time legs. Rotations, of any profile, and all spatial gradients give zero. The script checks four elementary relations at the origin:

| Relation between the two frames | Vector torsion | Axial torsion | Tensor torsion | Slow-motion force |
|---|---|---|---|---|
| twist: rotation about $z$ by $\theta = kz$ | 0 | yes | yes | 0 |
| spin: rotation about $z$ by $\theta = \omega t$ | 0 | yes | yes | 0 |
| boost along $x$, rapidity $\zeta = \omega t$ | yes | 0 | yes | $-\dot\zeta$ along $x$ |
| boost along $x$, rapidity $\zeta = kz$ | 0 | yes | yes | 0 |

This matches `research/bimetric-projection/probe_torsion_force.py`, which found that the vector and tensor parts can push a slow particle and the axial part cannot.

**Two consequences for GFD:**

1. **The force channel is the acceleration of the time leg.** If TetB acts on slow matter through torsion, it does so only through a relative boost changing in time. [`research/bimetric-projection/`](../bimetric-projection/) Part 2 reached the same channel from the other direction: its covariant form couples to $a_\mu$, the acceleration of the tetrad's time leg. The two routes agree on the channel; this is consistency, not a derivation of $\mu$.
2. **Handedness is force-free.** The relations that carry a sense of rotation (twist and spin) produce axial torsion and no slow-motion force. Open item 6 asks for brake and drive from the sense of the TetB spin. The kinematics cannot supply that directly. It needs a field equation that couples the axial channel, which knows the sense of rotation, to the vector channel, which moves matter. No such equation has been written.

## What this does not settle

- It does not say which connection matter follows. Result 4 assumes particles follow the frame's own connection (its autoparallels). In teleparallel-equivalent gravity they follow the Levi-Civita geodesics instead, and then a relative frame exerts no force at all.
- It does not supply the field equation asked for in consequence 2.
- Results 1 and 3 and the companion check are standard. The GFD-specific content is Result 2 (the covariant form of 40 = root-blind, 24 = TetB, and the coordinate-index trap), the action-term table read as root-blind versus root-resolving, and the two consequences of Result 4.
- No paper has been changed here.

*Correction, 2026-11-12. The first version of Result 2 said that the second root appears in none of the 64 connection components. That was wrong. It compared the torsion in coordinate components, where the inverse frame applies the parity twice and cancels the sign. In frame form the 24 change with the root, as Letter 2 states.*

## Run

```bash
python3 14_where_the_roots_live.py      # 27/27
```
