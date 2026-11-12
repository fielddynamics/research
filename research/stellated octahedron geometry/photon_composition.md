# Photon Composition

*How n×n×n photons build one larger stellated octahedron · Gravity Field Dynamics (GFD) · Field Dynamics Research*

*Note, 2026-11-12. Status: Results 1–4 are proved for every n and checked for n = 1–8. Result 5 is checked at two levels; Result 6 is exact at n = 2. The reading in the last section is interpretation. Run `python3 verify_photon_composition.py` (14 checks, exact). Open `photon_composition.html` to see every claim and recheck it for n = 1 to 5.*

---

GFD reads the stellated octahedron as the photon. Galeffi's 64-Tetrahedron Grid ([README](README.md)) is 8 photons in a 2×2×2 block, and it contains one stellated octahedron twice the size. This note asks what happens for any number of photons. Is the larger star simply made of the photons, or does composing them change something?

The answer: the larger star always forms and always has the photons' total volume, but it is not built from the same pieces. Part of the photons is pushed out. New space opens between photons and makes up exactly the lost volume. What is pushed out always has the symmetry of the 24 torsion components.

## Setup

- Place n×n×n photons in unit cubes. A photon is a core octahedron plus 8 tetrahedral spikes, one tip at each corner of its cube.
- The block contains one large stellated octahedron n times the photon: two big tetrahedra T⁺ and T⁻ on the block's corners. They meet in a central octahedron around the Field Origin.
- A spike is **captured** when it lies inside the large star and **expelled** otherwise.
- **Volume units:** small tetrahedron = 1, so an octahedron = 4, a photon = 8 + 4 = 12, and the large star = 12n³, the photons' total volume (a stellated octahedron fills half its cube).

All spikes, photon cores and the octahedra between photons together form the tetrahedral-octahedral honeycomb, and its only tetrahedra are the spikes. The faces of T⁺ and T⁻ lie on honeycomb planes, so every cell of the honeycomb is either inside the large star or outside it. No cell straddles the boundary.

## Results

### 1. Captured and expelled counts (proved)

Let t(N) be the number of honeycomb tetrahedra inside a tetrahedron of size N, with N small edges per side. Classically t(N) = C(N+2,3) + C(N,3) = N(N²+2)/3.

- Each big tetrahedron has size 2n, so it holds t(2n) spikes.
- Cutting a size-2n tetrahedron at its edge midpoints gives 4 corner tetrahedra of size n plus the central octahedron. So the octahedron holds t(2n) − 4t(n) spikes.
- By inclusion–exclusion, the large star captures

$$t(2n) + 4t(n) = \tfrac{4n(2n^2+1)}{3} + \tfrac{4n(n^2+2)}{3} = 4n(n^2+1)$$

  spikes and expels the rest:

$$8n^3 - 4n(n^2+1) = 4(n-1)n(n+1) = 24\binom{n+1}{3}.$$

| Photons per side n | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Captured | 8 | 40 | 120 | 272 | 520 |
| Expelled | 0 | 24 | 96 | 240 | 480 |

At n = 2 this gives the 64-TG's 40 and 24 (README, Result 2).

The same argument counts octahedra. The honeycomb holds C(N+1,3) octahedra in a tetrahedron of size N, so the large star contains C(2n+1,3) + 4C(n+1,3). These are the photon cores inside it plus the new cavities between photons.

### 2. The volume exchange (proved)

The large star is exactly filled by honeycomb cells, and its volume equals the photons' total volume. So:

> photons pushed out (expelled spikes + photon cores outside) = new cavities between photons, by volume.

| n | Spikes out | Cores out | New cavities | Exchange |
|---|---|---|---|---|
| 2 | 24 | 0 | 6 | 24 = 4·6 |
| 3 | 96 | 12 | 36 | 144 = 4·36 |
| 4 | 240 | 24 | 84 | 336 = 4·84 |

For large n the composite star is 1/3 spikes, 1/6 photon cores and 1/2 new space between photons. These are the classical proportions of the honeycomb.

### 3. Exact half and half off the diagonals (proved)

Call a spike **diagonal** when its photon's centre and its direction point along the same body diagonal through the Field Origin.

- **Count.** Each photon centred on a body diagonal contributes 2 diagonal spikes, or 8 for the central photon when n is odd. That makes 8n in all.
- **All captured.** In centred coordinates, take a photon at S = λD, with D a corner of T⁺. If λ ≥ 0 its spike lies in T⁺. If λ < 0 it lies in T⁻. The four face inequalities check directly.
- **Consequence.** Off the diagonals, the captured number is 4n(n²+1) − 8n = 4n(n²−1), which equals the expelled number. Off the diagonals, composition takes exactly half and expels exactly half.

At n = 2 there is also a pairing behind the split: each photon's own root exchange (spike f → opposite corner f̄) carries every captured off-diagonal spike to an expelled one. From n = 3 on that pairing fails, while the counts above still hold.

### 4. The expelled spikes carry torsion's symmetry (proved)

Suppose a rotation of the block maps a spike to itself.
- Every honeycomb tetrahedron lies in exactly one photon's cube, so the rotation fixes that photon's centre.
- It also fixes the spike's centroid, so it fixes the spike's direction.
- A nontrivial rotation fixing two such directions must be a 3-fold rotation about a body diagonal through both. So the spike is diagonal.

Every off-diagonal spike is therefore moved freely by the 24 rotations, and every expelled spike is off-diagonal (Result 3). So the expelled set is

> C(n+1,3) copies of the regular representation of S4 (rotations of the cube ≅ S4).

This is the symmetry of the 24 torsion components of the affine connection ([`proofs/torsion-regular-representation`](../../proofs/torsion-regular-representation/), Letter 2: the 24 are TetB). At n = 2 the expelled 24 are the coupling relation A₁: star and spike lie in opposite chambers.

**Limit:** the match is with the 24 only. The 40 captured at n = 2 do not carry the symmetry of the 40 Christoffel components. Their characters on the classes (e, transposition, double transposition, 3-cycle, 4-cycle) are (40, 0, 0, 4, 0) and (40, 8, 0, 1, 0).

### 5. The second level is again the coupling scheme (checked, n = 4)

Group 64 photons as 8 composites of 8. Label each spike by its composite C, its photon c and its own corner f. Whether it is captured depends only on the three Hamming relations (d(C,c), d(c,f), d(C,f)). So the anatomy of the composite of composites is still written in the cube's coupling relations, now on three labels.

### 6. At n = 2 the composite lays out the photon's metric (exact)

With the photon's frame vectors e_v (the cube corners, as in the Gram paper):

- **Tip position.** Every spike tip sits at (e_c + e_f)/2. Its squared distance from the Field Origin is

$$r^2 = 3 - d(c,f) = \tfrac{3 + e_c\cdot e_f}{2},$$

  which is a Gram entry of the photon. The coupling-algebra metric result reads the same relation as η(n_c, n_f) = −(2/3)·d(c,f).
- **Convergence.** Tips per point are 2^(3−r²): 8 at the Field Origin, then 4, 2, 1 outward.
- **Polarity.** The two polarities balance, 32 against 32.
- **Contact operator.** Two photons share 2^(3−d) tip points. As an element of the coupling algebra, Σ_d 2^(3−d) A_d has eigenvalue 3^(3−k) on Walsh grade k: 27, 9, 3, 1. The grade-0 mode, which is time in the metric result, is the strongest.

## Reading: composition toward a gravity field (interpretation)

The aim here is to sort what the results show from what they suggest.

- **Shown.** Photons always compose into a larger photon of the same total volume. Composition is an exchange: torsion-symmetric pieces leave, and new space between photons takes their place. Everything on the Field Origin's diagonals is kept. The larger star's handedness is read from which photon, not from the photons' own spikes. At n = 2 the composite's geometry is the photon's own metric laid out in space.
- **Suggested.** In bulk the photons' ± polarity cancels, and the same-sign grade-0 contact mode dominates. That fits the character of gravity (one sign, universal) as distinct from EM's ±. This is a reading, not a derivation.
- **Not shown.** Nothing here produces the value of G, the α²¹ suppression, or a 1/r falloff.
- **Coincidence (tagged).** At n = 4 (64 photons), 272 = 273 − 1 and 240 = 241 − 1 echo the level-2 values f(K², +1) and f(K², −1) of the G hierarchy. Both follow from the trivial identity x² ± x = x(x ± 1) and from 4n = n² at n = 4, so this is not evidence.

## Open

1. Is there a bijection behind the half-and-half split for every n, as root exchange gives at n = 2?
2. What is the rule, in terms of the three relations, for capture at the second level (Result 5)?
3. Does the contact operator's grade structure survive at larger n, and does it connect to the metric result beyond n = 2?

## Related

- [README](README.md): the 64-TG model and Galeffi's counts (`verify_64_tetrahedron_grid.py`).
- [`coupling-algebra/`](../coupling-algebra/): the relations A₀–A₃, Walsh grades, the metric as an element.
- [`proofs/torsion-regular-representation/`](../../proofs/torsion-regular-representation/): the 24 torsion components as the regular representation of S4.
