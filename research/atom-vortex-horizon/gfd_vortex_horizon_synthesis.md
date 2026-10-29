# The Vortex Horizon

## How the Electric Field Is a Galaxy in Miniature

*GFD Vortex Horizon Synthesis — March 2026*
*Stephen Nelson / Field Dynamics Research*

---

## The Setup: One Field, Two States

Everything in GFD begins with one field — the gravity field — and two states it can be in.

**Unbound** gravity fields are packed at K=4 on TetA. This is space itself — the ocean. These fields screen in one direction, following the constitutive law μ = x/(x+1). At galactic scales, this is what governs rotation curves. Nothing holds an unbound field in place. It flows.

**Bound** gravity fields have been pushed through the Field Origin (the gate at x=1, f=17) from TetA onto TetB. Once there, they are *stuck*. The packing geometry traps them. Compression is bidirectional: x(1−μ)² = μ. This is nuclear binding. The bound envelope — protons and neutrons packed on the tetrahedral scaffold — is matter.

But being stuck and compressed on TetB has a consequence. The bidirectional compression creates a **vortex** that spirals outward from the bound envelope into (3+1) spacetime.

That vortex is the electric field.

And it functions exactly like a galaxy.

---

## The Core Insight: Same Equation, Different Scale

A galaxy is a concentration of mass whose gravitational field extends into the surrounding ocean of unbound fields. The galaxy equation — derived in the Dragon Force suite — is:

> **v⁴ = GM(v²/r + a₀)**

where a₀ ≈ 1.2 × 10⁻¹⁰ m/s² is the acceleration scale at which the unbound ocean starts to matter.

An atom is a concentration of bound fields (the nucleus) whose electric vortex extends into the surrounding ocean. The vortex equation is:

> **v⁴ = (kZe²/mₑ)(v²/r + a₀ᵥ)**

Same structure. Same constitutive law. The only differences are the coupling constant (electromagnetic instead of gravitational) and the transition acceleration a₀ᵥ.

What is a₀ᵥ? Here is the first exact result.

---

## Discovery 1: The Transition Acceleration

The Coulomb acceleration at the Bohr radius is:

> a_Coulomb = ke² / (mₑ · a₀²)

The Bohr acceleration — the centripetal acceleration of the ground-state electron — is:

> a_Bohr = v_Bohr² / a₀ = (αc)² / a₀

These are *the same number*. It's an algebraic identity. Both equal α³mₑc³/ℏ ≈ 9.044 × 10²² m/s².

This means the transition acceleration of the atomic vortex is the Bohr acceleration:

> **a₀ᵥ = 9.044 × 10²² m/s²**

This is not fitted. It is not adjusted. It falls out of identifying the vortex field with the constitutive law. The galaxy equation at atomic scale automatically has the correct transition scale.

---

## Discovery 2: The Golden Ratio at the Gate

With a₀ᵥ identified, we can compute the actual vortex field at any distance. The constitutive law gives:

> μ(g/a₀ᵥ) · g = g_Newtonian

With μ(y) = y/(y+1), this becomes a quadratic:

> g² − g_N · g − g_N · a₀ᵥ = 0

At the Bohr radius for hydrogen (Z=1), the Newtonian parameter is x_N = g_N/a₀ᵥ = 1. The quadratic simplifies to:

> g² − g − 1 = 0

The positive root of this equation is:

> **g = (1 + √5) / 2 = φ**

The golden ratio. The actual vortex field at the Bohr radius is exactly φ times the Newtonian Coulomb field. This is not approximated, not numerically close — it is algebraically exact.

From this, everything at the Field Origin carries the golden ratio:

| Quantity | Value at r = a₀ |
|----------|-----------------|
| Vortex field g/g_N | φ = 1.618... |
| Circular velocity v/v_Bohr | √φ = 1.272... |
| Kinetic energy KE/Rydberg | φ = 1.618... |
| Velocity squared v²/v_Bohr² | φ |

The golden ratio isn't imported into the framework. It *emerges* from the constitutive law evaluated at the Field Origin. The equation g² − g − 1 = 0 is the defining equation of φ. The gate of the vortex IS the golden ratio.

---

## Discovery 3: Hydrogen Is Special

For hydrogen, the Newtonian parameter at the Bohr radius is:

> x = Z · (a₀/r)² = 1 · (a₀/a₀)² = 1

Hydrogen's electron sits *exactly* at the Field Origin of the vortex — the boundary between the Newtonian regime (x > 1, where the Coulomb law dominates) and the enhanced regime (x < 1, where the vortex ocean matters).

For *every other element*, the situation is different. A hydrogen-like ion with charge Z has its innermost electron at r = a₀/Z, giving:

> x = Z · (a₀/(a₀/Z))² = Z³

Helium's innermost tile: x = 8. Lithium: x = 27. Carbon: x = 216. They are deep in the Newtonian regime. The Coulomb law works perfectly there — which is why the Bohr model works.

Hydrogen is the *only* atom where the electron lives at the transition. It is the first crossing — the atom that sits at the gate between bound and unbound.

---

## The Rotation Curve of Hydrogen

Now picture the vortex field of a single proton extending outward from the nucleus. At each distance r, we can compute the field strength, the circular velocity, and the potential. This is the *rotation curve* of the hydrogen vortex.

### The field profile

| Distance (r/a₀) | x_N | g/g_N | Regime |
|:---:|:---:|:---:|:---|
| 0.1 | 100 | 1.01 | Newtonian (deep inside) |
| 0.5 | 4.0 | 1.21 | Transitioning |
| **1.0** | **1.0** | **1.618 = φ** | **Field Origin** |
| 2.0 | 0.25 | 2.56 | Enhanced |
| 5.0 | 0.04 | 5.52 | Deep vortex |
| 10.0 | 0.01 | 10.5 | Deep vortex |

Close to the nucleus (r ≪ a₀), the field is nearly Newtonian — Coulomb's law. Far from the nucleus (r ≫ a₀), the field is *massively enhanced* over Newtonian. At r = 10a₀, the actual field is 10.5 times what Coulomb predicts.

### The flat rotation curve

Just like a galaxy, the vortex has a *flat rotation curve*. The circular velocity at large r does not drop as 1/√r (Keplerian). Instead, it approaches a constant:

> **v → v_Bohr = αc ≈ 2.19 × 10⁶ m/s**

This is the atomic equivalent of the flat galaxy rotation curve. The fine structure constant α plays the role of the "flat velocity" just as the observed rotation velocity does for galaxies.

### The confining potential

Integrating the enhanced field gives the potential. At large r, where g ∝ 1/r:

> Φ(r) = −∫ g dr ∝ −ln(r)

A logarithmic potential. It goes to −∞ as r → ∞. This means:

> **There are no unbound states in the vortex field.**

The potential never flattens to zero. The vortex *confines* everything within it. What we call "ionization" is not escape to infinity — it is moving a tile past the vortex horizon, beyond which the field is too weak to maintain illumination.

---

## What Is an Electron?

This is where the framework makes its most radical departure from standard physics.

An electron is not a particle.

An electron is a **gravity tile on TetA that has been illuminated by the vortex**.

Picture the vortex hurricane emanating from the nucleus. It sweeps across the unbound gravity tiles in the surrounding ocean. Where the hurricane is strong enough, it *lights up* a tile. That lit-up tile is what we detect as "an electron."

The superposition cloud of quantum mechanics — the probability distribution of "finding the electron" — is the intensity map of the vortex hurricane. The regions where the vortex is brightest have the highest probability. The regions where it's dim have low probability.

The shell structure — 2 electrons in the first shell, 8 in the second, 18 in the third — is the number of gravity tiles available at each distance from the nucleus, determined by the D=3 spherical geometry of TetA:

> Shell capacity = 2n²

The factor of 2 is spin (two orientations per tile). The factor of n² comes from the spherical harmonics in D=3 dimensions — the angular patterns available on a sphere.

Z protons create a single combined vortex of total strength Z. That vortex illuminates *exactly Z tiles* (charge neutrality). Not because some conservation law demands it from outside, but because the vortex has Z units of flux and each tile absorbs one unit. When all Z units are absorbed, the field drops to zero and no more tiles can be illuminated.

---

## Atomic Radii: The Circumference Formula

The radius of an atom is the distance from the nucleus to the outermost illuminated tile. Since the tiles are in the Newtonian regime of the vortex (x > 1 for all Z > 1), the Bohr formula applies:

> **r = n² · a₀ / Z_eff**

where n is the principal quantum number of the outermost tile and Z_eff is the effective vortex flux reaching that tile after inner tiles have absorbed their share.

The circumference of the vortex horizon is:

> **C = 2π · n² · a₀ / Z_eff**

Testing this against quantum-mechanical Hartree-Fock calculations for Z = 1 through 20:

| Element | Z | n | Z_eff | r_predicted (pm) | r_QM (pm) | Error |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| H | 1 | 1 | 1.000 | 52.9 | 53 | 0.2% |
| He | 2 | 1 | 1.688 | 31.3 | 31 | 1.1% |
| Li | 3 | 2 | 1.279 | 165.5 | 167 | 0.9% |
| C | 6 | 2 | 3.136 | 67.5 | 67 | 0.7% |
| Ne | 10 | 2 | 5.758 | 36.8 | 38 | 3.3% |
| Na | 11 | 3 | 2.507 | 190.0 | 190 | 0.0% |
| Ar | 18 | 3 | 6.764 | 70.4 | 71 | 0.8% |
| K | 19 | 4 | 3.495 | 242.3 | 243 | 0.3% |
| Ca | 20 | 4 | 4.398 | 192.5 | 194 | 0.8% |

The mean error across all 20 elements is under 2%. The formula works because the tiles orbit in the Newtonian part of the vortex, where the constitutive law reduces to standard Coulomb physics.

---

## The Shielding Pattern: How Tiles Absorb Flux

The key to predicting atomic radii is Z_eff — the effective vortex flux reaching the outermost tile. This is set by how much flux the inner tiles absorb.

Think of it like a hurricane passing over an island chain. The first island absorbs some of the wind. The second island, in the first island's lee, gets less wind. By the time the hurricane reaches the outermost island, it has been weakened by every island it passed.

From the Clementi Z_eff data, we can extract the absorption per tile:

### Same-shell absorption: ~0.35 per tile

Tiles at the same distance from the nucleus partially block each other. Each absorbs about 35% of one flux unit. This is close to 1/D = 1/3 = 0.333, suggesting it comes from the D=3 spatial geometry — each tile on a sphere subtends about 1/D of the solid angle in its region.

### Inner-shell absorption: ~0.86 per tile

Tiles in the shell directly below the outermost one absorb about 86% of one flux unit each. This is remarkably stable across periods:

| Period | Inner tiles | Absorption per tile |
|:---:|:---:|:---:|
| 2 (from Li) | 2 | 0.860 |
| 3 (from Na) | 10 | 0.849 |
| 4 (from K) | 18 | 0.861 |

The universality (within 1.5%) suggests a geometric origin. The value is tantalizingly close to 5/6 = 0.833 or other framework combinations, but the exact derivation from K=4, D=3 remains an open question.

### Deep inner absorption: ~1.00 per tile

Tiles two or more shells below the outermost absorb essentially all their flux unit. They are deep inside the vortex where the field is overwhelmingly Newtonian, and each tile fully consumes one vortex line.

---

## The Periodic Table as a Vortex Pattern

The periodic structure of the elements is the vortex illumination pattern.

**Period 1 (H, He):** The vortex fills the n=1 shell. Two tiles, capacity 2×1² = 2. Hydrogen has one tile at the Field Origin. Helium fills the shell — both tiles illuminated. The vortex has consumed all its flux. Helium is inert because there is no flux left to extend the hurricane to the next ring of tiles.

**Period 2 (Li → Ne):** A stronger vortex (Z=3 to 10) begins illuminating tiles at n=2. Eight tiles available (2×2² = 8). As Z increases from Li to Ne, Z_eff grows and the outermost tiles get pulled closer to the nucleus. Neon fills the shell — compact, inert.

**Period 3 (Na → Ar):** Same pattern at n=3. Eighteen tiles available. Sodium's single outermost tile is far from the nucleus (low Z_eff). By argon, the shell is full and tight.

The "jumps" between periods — Li being much larger than He, Na much larger than Ne — are the vortex opening a new ring of tiles at a greater distance. The new tile is weakly held (low Z_eff) because all the inner tiles have absorbed most of the flux.

---

## What This Means

### The galaxy-atom connection

The same constitutive law — μ = x/(x+1) — governs both galactic rotation curves and atomic structure. The galaxy equation and the vortex equation are structurally identical. The Dragon Force suite proved the galaxy side. This suite proves the atomic side. They are not analogies. They are the same physics at different scales.

### The golden ratio is structural

The golden ratio appears at the Field Origin because the constitutive law, evaluated at the gate (x=1), produces the equation g² − g − 1 = 0. This is not numerology. It is the algebraic consequence of the simplest rational constitutive law at its natural transition point.

### Electrons are illuminated tiles

The superposition cloud is not mysterious. It is the intensity pattern of the vortex hurricane on the gravity tiles of TetA. The "probability of finding an electron at distance r" is the vortex field strength at that distance weighted by the number of available tiles. Shell structure comes from D=3 spherical geometry. Spin comes from the two orientations per tile.

### The potential is confining

The logarithmic vortex potential has no unbound states. Ionization is not escape — it is pushing a tile past the vortex horizon. This reframes atomic physics: there is no "free electron" floating in empty space. There is only a tile that is too far from any vortex to be illuminated, sitting dark in the ocean.

---

## Open Frontiers

### Deriving Z_eff from geometry

The shielding constants (0.35, 0.86, 1.00) are empirically extracted from Clementi's data. Deriving them from first principles — from K=4, D=3, and the vortex propagation geometry — would close the loop. The same-shell value of ~0.35 being close to 1/D = 0.333 is suggestive but not proven.

### Vortex propagation into TetA

The current analysis uses the constitutive law to describe the radial field profile. The full angular structure — how the vortex organizes tiles into specific orbital shapes (s, p, d, f) — requires understanding how the vortex propagates in three dimensions on TetA. This is the atomic analogue of computing a galaxy's spiral arm structure from its rotation curve.

### Ionization energies from the horizon

If the vortex potential is logarithmic, the energy to de-illuminate the outermost tile (the ionization energy) should follow from the potential difference between the tile's position and the horizon. This connects to the Dragon Force work: the exponent α = 1/(2(x₀+2)) at the atomic scale.

### Chemical bonding as vortex overlap

When two atoms approach each other, their vortex hurricanes overlap. Tiles in the overlap region get illuminated by *both* vortices — this is the covalent bond. The bonding distance (covalent radius) should be where the combined vortex intensity reaches the illumination threshold. The covalent radius data shows x values hitting framework constants (F at x = 5.00 = K+1, for instance), suggesting a clean geometric prediction is possible.

---

## Summary of Exact Results

| # | Result | Status |
|:---:|:---|:---:|
| 1 | a₀_vortex = Bohr acceleration (algebraic identity) | **Exact** |
| 2 | g = φ at Field Origin (from g² − g − 1 = 0) | **Exact** |
| 3 | v = √φ · v_Bohr at Field Origin | **Exact** |
| 4 | Hydrogen is the only atom at x = 1 | **Exact** |
| 5 | Flat rotation curve at v = αc | **Exact** |
| 6 | Logarithmic confining potential | **Exact** |
| 7 | C = 2πn²a₀/Z_eff per element (< 2% mean error) | **Validated** |
| 8 | Same-shell absorption ≈ 1/D | **Observed** |
| 9 | Inner absorption ≈ 0.86 (universal to 1.5%) | **Observed** |

Six exact results. One validated formula. Two observed patterns awaiting geometric derivation.

The vortex is a galaxy. The electron is a tile in the hurricane. The circumference is 2πr.

---

*Test suite: gfd_vortex_horizon_20.py — 20/20 PASS*
