# Pixel Tiling and Closure

*Photons tile space as cubes, and closure fixes their chambers · Gravity Field Dynamics (GFD) · Field Dynamics Research*

*Note, 2026-11-12. Status: proved; the computations check every step. Run `python3 verify_pixel_tiling.py` (9 checks, exact).*

---

GFD reads the stellated octahedron as the photon, and the cube around it as the pixel of reality. In [the pixel and the lattice](../photonic/the-pixel-and-the-lattice.md), photons organise into a lattice, and that lattice is gravity, much as water molecules organise into ice. That note does not say which lattice. This note shows that the cube settles it, and that field closure then fixes the lattice's chamber labels up to a single global choice.

## 1. The cube settles the lattice

A photon's star fills exactly half its cube: 8 spikes and a core octahedron make 8 + 4 = 12 tetrahedron units of the cube's 24. The other half is 12 wedges, one along each cube edge, each a quarter of an octahedron.

Pixel cubes tile space on the simple cubic grid. Where four cubes meet around an edge, their four wedges close into one whole octahedron centred on that edge (check 1b):
- all 8 of its faces are spike faces;
- 2 faces come from each of the 4 surrounding photons.

So:
- **Photons fill space with nothing left over.** The space between stars is each cube's own empty half, completed by its neighbours.
- **The shared octahedra are owned jointly.** No single photon owns one; four photons hold it together. Each photon holds 12/4 = 3 of them, and space is half photons, half shared octahedra.
- **This is the lattice already modelled in this folder.** It is the 64-Tetrahedron Grid's lattice (the tetrahedral–octahedral honeycomb, Fuller's isotropic vector matrix). The 6 central octahedra of the 64-TG are the shared octahedra on the 6 interior edges of its 2×2×2 block.
- **No other packing keeps the cube.** Other packings of tetrahedra and octahedra, such as the hexagonal (gyrated) stacking or face-to-face chains, do not preserve the cube. If the pixel is the cube, the lattice is forced, as water's bond angle forces ice's hexagons.

## 2. Closure fixes the chambers

Each photon's star has two tetrahedra, and the photon assigns one to TetA and the other to TetB. Write σ_c ∈ {0, 1} for that choice in cube c.

At every lattice corner, 8 photons meet. Closure requires that where parts meet they agree (Paper I). Here that means every photon meeting at a corner must give it the same chamber.

**Theorem.** On any block of pixel cubes, these agreement conditions have exactly two solutions:

$$\sigma_c = |c| \bmod 2 \qquad\text{or}\qquad \sigma_c = |c| + 1 \bmod 2,$$

where |c| is the sum of the cube's integer coordinates.

**Proof.**
1. Cube c sees a corner p with local parity |p − c|. A neighbouring cube c + d sees the same corner with local parity |p − c − d|.
2. So agreement requires σ_c + σ_{c+d} ≡ |d| (mod 2).
3. Face neighbours alone (|d| = 1) force σ to alternate along every axis. That leaves σ_c = σ₀ + |c|, with σ₀ free.
4. This solution satisfies the conditions for edge and corner neighbours too, so it is consistent.

Checks 2a and 2e confirm this exactly for 2 to 5 photons per side.

**Consequences:**
- **Neighbouring photons alternate orientation.** The local labelling is a checkerboard (check 2b).
- **The whole lattice gets one consistent labelling.** Every lattice corner's chamber is its global parity, x + y + z mod 2 (check 2c). This is the labelling the 64-TG model uses.
- **One free bit remains, and it is global.** Exchanging TetA and TetB everywhere at once (check 2d) is the tetrad equation's choice between its two roots, M₁ or M₂ = −M₁. General relativity makes that choice by convention.

Once closure is required, no photon has any local freedom left in which chamber is which. The two-root structure appears for the whole lattice, not photon by photon.

**Remark (computed).** If the lattice closes on itself (periodic in all three directions), the labelling is consistent only for an even number of photons per side (check 2f).

## What this does and does not say

**Shown:**
- the cube forces the lattice;
- the space between photons is jointly held structure (the shared octahedra);
- closure at shared corners leaves exactly one global bit, which is the root choice.

**Not shown:**
- how a tile at the electron radius r_e sits in this lattice;
- what dynamics the lattice carries.

The composition results in [photon_composition.md](photon_composition.md) describe what larger blocks of this lattice contain. They do not yet say which block is the gravity tile.

## Related

- [README](README.md): the 64-TG model.
- [photon_composition.md](photon_composition.md): n×n×n photons composing a larger star.
- [the pixel and the lattice](../photonic/the-pixel-and-the-lattice.md) and [what is gravity](../g_from_topology/what_is_gravity.md): the framework's picture of photons organising into the gravity lattice.
- [`coupling-algebra/`](../coupling-algebra/): the two roots as parity on the cube.
