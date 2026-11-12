# 13 — The 64 connection components, split by symmetry

*Research note, Field Dynamics Research, 2026-11-12. Status: computation, not a paper. Script: [`13_connection_irreducibles.py`](13_connection_irreducibles.py), 25 checks (numpy, sympy).*

## The question

Open item 2 of this folder asks whether TetB lives in the torsion (24 components) or in the connection difference that BIMOND uses (40 components). In the slow-motion limit the two give the same force. This note asks whether they are the same object relativistically.

The method is to split the 64 components of a general connection difference $N_{abc}$ (first index lowered with $\eta$) into pieces that no change of frame can mix. Two symmetry groups are used:

- the **Lorentz group**, the symmetry of spacetime, which decides what is physical; and
- **$S_4$**, the permutations of the four tetrad legs, the symmetry of the [torsion proof](../../proofs/torsion-regular-representation/).

## Result 1: the seven pieces

Splitting by symmetry under exchange of indices gives the familiar $64 = 40 + 24$. Each half splits further.

| Sector | Piece | Dimension | Lorentz type $(j_1, j_2)$ |
|---|---|---|---|
| Symmetric 40 | fully symmetric, trace-free | 16 | $(\tfrac32, \tfrac32)$ |
| | fully symmetric, trace | 4 | vector $(\tfrac12, \tfrac12)$ |
| | mixed symmetry, trace-free | 16 | $(\tfrac32, \tfrac12) \oplus (\tfrac12, \tfrac32)$ |
| | mixed symmetry, trace | 4 | vector |
| Torsion 24 | mixed symmetry, trace-free (tensor) | 16 | $(\tfrac32, \tfrac12) \oplus (\tfrac12, \tfrac32)$ |
| | trace (vector) | 4 | vector |
| | fully antisymmetric (axial) | 4 | axial vector |

The script checks each piece's invariance under rotations and boosts and identifies its type from the two Lorentz Casimirs. The seven pieces span all 64.

**Status: standard.** The 40 is the space of *nonmetricity*, and its four pieces are the standard decomposition of metric-affine gravity (Hehl, McCrea, Mielke and Ne'eman, *Phys. Rep.* 258, 1995). The torsion pieces are the vector, axial and tensor parts already used in the [torsion proof](../../proofs/torsion-regular-representation/). What follows uses this split.

## Result 2: BIMOND and GFD sit in different halves of metric-affine geometry

BIMOND's $C = \Gamma - \hat\Gamma$ is the difference of two Levi-Civita connections. Measured with $\hat\Gamma$, the metric $g$ is not constant, so $C$ is a pure *nonmetricity* (disformation) tensor, in the symmetric 40. GFD's TetB, as placed by Letters 2 and 3, is *torsion*, in the 24.

A torsion acts on particles through its contorsion $K$, and a slow particle feels the part symmetric in the lower pair, $K^i{}_{(00)}$. The script shows:

- The map from torsion to the symmetric part of its contorsion has rank 20. Its kernel is exactly the axial 4. This is why axial torsion never pushes a slow particle, as `research/bimetric-projection/probe_torsion_force.py` found.
- Its image is exactly the mixed-symmetry 20 of the 40 (the 16 and its vector). It never reaches the fully symmetric 20.

Now take BIMOND's $C$ in a weak static field, $ds^2 = -(1+2\phi)\,dt^2 + (1-2\gamma\phi)\,d\mathbf x^2$. For every $\gamma$:

- it has no torsion part, as it must;
- it has a nonzero fully symmetric part. Exactly, $(C_{x00} + C_{0x0} + C_{00x})/3 = -g/3$, with no dependence on $\gamma$.

So **no torsion reproduces BIMOND's connection difference**, even in the weak field. The two agree on the slow-motion force, because torsion can set the $(i,0,0)$ slot to anything. But BIMOND's $C$ always carries a fully symmetric part that torsion cannot supply. It enters wherever the whole connection matters: light, moving matter, and the relativistic field equations.

**Consequence for open item 2.** The two placements of TetB are different theories, not two readings of one. A GFD with TetB in the torsion is not BIMOND. To reproduce BIMOND relativistically, GFD would need the nonmetricity sector, which no GFD paper uses. To keep TetB in the torsion, GFD needs its own covariant completion, of the kind sketched in `research/bimetric-projection/probe_ec_candidate.py`. The spin argument (open item 6) favours the torsion, because only the axial channel carries a sense of rotation. The axial piece, however, is exactly the one that exerts no slow-motion force.

## Result 3: what the index grid's 16 is, and is not

The [Gram paper](../../papers/gram-matrix-of-tetrad-equation/) splits each slice of $\Gamma^\lambda{}_{\mu\nu}$ into 6 upper + 4 diagonal + 6 lower entries, so $64 = 24 + 16 + 24$, with the diagonal 16 read as the shared, root-blind sector. The script checks how this grid behaves under the two symmetries:

| Subspace | Kept by leg permutations ($S_4$)? | Kept by rotations and boosts? |
|---|---|---|
| diagonal 16, $\Gamma^\lambda{}_{\mu\mu}$ | yes | no |
| upper-triangle 24 | no (a leg swap moves it to the lower triangle) | no |

The diagonal 16 shares no nonzero tensor with any of the seven Lorentz pieces. So:

- **The counts are exact**, and the swap of the two lower indices still exchanges the two triangles with the diagonal fixed. That is the property the [chiral-holonomy proof](../../proofs/chiral-holonomy-closed-frame/) uses, and it is unaffected.
- **"Sector" language depends on the coordinates.** A boost or a rotation mixes the diagonal 16 with the rest. Statements such as "Newton's pull $C^i{}_{00}$ sits in the shared 16" (row 7 of the dictionary in the README, and `probe_where_tetb_pushes.py`) are true in the static frame's coordinates. They do not describe a Lorentz-invariant sector.

## Result 4: the symmetric 40 under leg permutations

The [torsion proof](../../proofs/torsion-regular-representation/) shows that the torsion 24 is the regular representation of $S_4$. The script gives the companion decomposition of the symmetric 40 from its character:

| Subspace | Character on $e$, $(ab)$, $(ab)(cd)$, $(abc)$, $(abcd)$ | Decomposition |
|---|---|---|
| symmetric 40 | $(40, 8, 0, 1, 0)$ | $4\cdot\mathbf 1 \oplus 3\,[2,2] \oplus 7\,\mathrm{std} \oplus 3\,(\mathrm{sgn}\otimes\mathrm{std})$ |
| diagonal 16 | $(16, 4, 0, 1, 0)$ | $2\cdot\mathbf 1 \oplus [2,2] \oplus 3\,\mathrm{std} \oplus (\mathrm{sgn}\otimes\mathrm{std})$ |
| symmetric off-diagonal 24 | $(24, 4, 0, 0, 0)$ | $2\cdot\mathbf 1 \oplus 2\,[2,2] \oplus 4\,\mathrm{std} \oplus 2\,(\mathrm{sgn}\otimes\mathrm{std})$ |
| torsion 24 | $(24, 0, 0, 0, 0)$ | $\mathbf 1 \oplus \mathrm{sgn} \oplus 2\,[2,2] \oplus 3\,\mathrm{std} \oplus 3\,(\mathrm{sgn}\otimes\mathrm{std})$ (regular) |

The sign representation appears nowhere in the 40, consistent with Theorem 2 of the torsion proof. The two 24s of the index grid have the same dimension but are **not** the same representation of $S_4$: only the torsion 24 contains the sign response. In the grid's language, the retained TetA 24 and the discarded TetB 24 are equal in count, not mirror images under the symmetry of the legs.

## A related point, already in this folder

Script 07 (check F′) shows that a *constant* parity $P$ leaves the tetrad's (Weitzenböck) connection, and so its torsion, unchanged: $(Pe)^{-1}\partial(Pe) = e^{-1}\partial e$. Torsion distinguishes two frames only when the relation between them varies from point to point, as in the twist and spin examples of 07. Letter 2's proposition that "a torsionful connection depends on $e$ directly and is therefore root-resolving" should be read with this condition.

## What this does not settle

- It does not decide where TetB belongs. It shows that the choice matters relativistically and states what each choice commits GFD to.
- It does not test a covariant field equation for either placement.
- The decompositions in Result 1 are standard. The GFD-specific content is the comparison with BIMOND (Result 2), the status of the index grid (Result 3) and the $S_4$ decomposition of the 40 (Result 4).
- Results 3 and 4 bear on wording in the Gram paper, Letter 2 and Letter 3. No paper has been changed here.

## Run

```bash
python3 13_connection_irreducibles.py      # 25/25
```
