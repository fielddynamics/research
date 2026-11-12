# 14 — Where the two roots live in the connection

*Research note, Field Dynamics Research, 2026-11-12. Status: deduction with checks, not a paper. Script: [`14_where_the_roots_live.py`](14_where_the_roots_live.py), 25 checks (numpy, sympy). Follows [note 13](13_connection_irreducibles.md).*

## The question

Letter 2 says that a torsion-free connection cannot distinguish TetA from TetB, and that the torsion is "the necessary carrier" of the distinction. Note 13 split the 64 connection components into pieces that no change of frame can mix. This note asks the next question: starting from the frame itself, where exactly does the difference between the two roots appear? It is answered by deduction, with each step checked.

Throughout, the two roots are frames $e$ and $\tilde e = L\,e$ on the same metric, with $L(x)$ a Lorentz transformation at each point. TetB is the case where $L$ is in the parity component ($\det L = -1$).

## Result 1: the covariant form of 64 = 40 + 24

At a point, a frame has $4 \times 16 = 64$ first derivatives $\partial_\mu e^a{}_\nu$. The script checks, for the identity frame and for a random frame, that these are, one to one:

$$\underbrace{\partial_\mu e^a{}_\nu}_{64} \;\longleftrightarrow\; \underbrace{\partial_\mu g_{\nu\rho}}_{40} \;\oplus\; \underbrace{T^a{}_{\mu\nu}}_{24}.$$

The 24 that the metric cannot see is exactly the set of local Lorentz changes of the frame, $\mathfrak{so}(1,3) \otimes V^* = 6 \times 4$.

**Why it matters for GFD.** This is the coordinate-free version of the split that the Gram paper draws on the index grid. Note 13 showed that the grid's diagonal 16 is not Lorentz-invariant. Here the split needs no grid:
- the 40 are the derivatives of the metric, which is the Gram product $e^T\eta e$ and so root-blind (Gram Lemma 1);
- the 24 are the derivatives of the frame that the Gram product does not see.

**Status: standard** in teleparallel geometry (the Weitzenböck connection). The GFD use is the reading: the 40/24 split is the derivative of the Gram map.

A companion check: "symmetric in the lower pair" (40, torsion-free) and "antisymmetric in the outer pair" (24, metric-compatible) meet only in zero and together span the 64. That is the fundamental theorem of Riemannian geometry, the uniqueness of the Levi-Civita connection, stated as linear algebra. Letter 2's Lemma rests on it.

## Result 2: the second root is not in any of the 64 components

Two frames on one metric, $e$ and $Le$, have connections that differ by

$$N^\lambda{}_{\mu\nu} = (L^{-1}\partial_\mu L)^\lambda{}_\nu .$$

The script checks this for a general $L = R(f_1)\,B(f_2)$ with arbitrary functions $f_1, f_2$ of all four coordinates. Each $L^{-1}\partial_\mu L$ lies in $\mathfrak{so}(1,3)$, so $N$ is metric-compatible: it lies in the 24.

The discrete part drops out. $L^{-1}\partial L$ is unchanged when $L$ is replaced by $PL$ with $P$ a constant parity. So:

- **For a constant parity, every one of the 64 connection components is the same for both roots.** The torsion tensor is the same too.
- **What changes is the orientation**, $\det(PL) = -\det L$. It enters only through the volume form $\varepsilon = \det(e)\,[\mu\nu\rho\sigma]$.
- Example: for a twisted frame, the axial torsion *vector* $a^\mu = \tfrac16\varepsilon^{\mu\nu\rho\sigma}T_{\nu\rho\sigma}$ flips sign between the roots, while the torsion tensor $T_{\nu\rho\sigma}$ does not.

**What this changes in the reading.** The torsion carries the *continuous* relation between two frames: how one turns or boosts relative to the other from point to point. The *discrete* root label, TetA or TetB, is carried by the orientation $\det e = \pm\sqrt{-g}$, which is a property of the frame, not of its derivatives. Letter 2's corollary, that torsion is the necessary carrier of the TetA/TetB distinction, is accurate only for roots related by a position-dependent transformation. For the global parity that defines TetB it is not: there the carrier is the orientation.

This agrees with the [bimetric proof](../../proofs/bimetric-two-potential-energy/). Its Lemma 1 gets $\alpha = -\beta$ from $\det(e)$, through the orientation, not from torsion.

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
- Results 1 and 3 and the companion check are standard. The GFD-specific content is the reading in Result 2 (the root lives in the orientation, not in the 64), the action-term table read as root-blind versus root-resolving, and the two consequences of Result 4.
- Results 2 and 3 bear on wording in Letter 2 (its corollary) and Letter 3. No paper has been changed here.

## Run

```bash
python3 14_where_the_roots_live.py      # 25/25
```
