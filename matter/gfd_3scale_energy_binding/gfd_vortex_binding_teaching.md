# The Gravity Vortex and Nuclear Binding
## A Teaching Guide to the Three-Scale Decomposition

**Stephen Nelson, Field Dynamics, March 2026**

---

## What This Document Teaches

This document explains the physical picture behind the GFD three-scale nuclear binding energy formula:

```
B/A = 27*a(A) + 27*b + 9*c(Z,A)
    = Face    + Chan  + Sub
```

The formula predicts nuclear binding energy per nucleon for any element from Z and A alone, with zero fitted parameters and 1.58% mean error across the periodic table. The document explains what the numbers mean physically, starting from the gravity vortex and working upward through nuclear packing, the electric field, and electron shell structure.

The key ideas in order:

1. The proton is a gravity vortex (the host)
2. Nuclear packing happens in the host's TetB (the basement)
3. Packing reverses the vortex, creating the electric field
4. Electrons are not particles but excitation patterns on surrounding gravity tiles
5. The three gate depths [27, 27, 9] correspond to what is visible from TetA
6. The gate coupling b = m_e / (F_ZERO - 1/2) is the energy per observable channel
7. The closure energy c(Z,A) sits at the vortex throat and absorbs all packing corrections

---

## Part 1: The Host

### The gravity vortex

Every proton is a single gravity field. In the GFD framework, a gravity field is a vortex in the field fabric, shaped like an hourglass. The vortex has two halves:

**TetA** is the upper half, the part that exists in our observable 3+1 spacetime. This is where we make measurements, detect particles, and observe electromagnetic interactions. When we look at a proton with our instruments, we are looking at TetA.

**TetB** is the lower half, the subspace beneath the vortex throat. This is the "basement" of the host field. It is real structure, it carries energy and geometry, but it is not directly observable from our spacetime. We see its effects only through what leaks through the throat.

The **vortex throat** (the field origin) is the narrowest point of the hourglass, where TetA meets TetB. This is where the coupling state s passes through zero, the gate threshold. The polynomial f(K,s) = 1 + Ks + K^2 evaluates to F_ZERO = 17 at the throat.

### The coupling polynomial at each level

The polynomial traces the full vortex structure as the coupling state s moves from -1 (deep in TetB) through 0 (the throat) to +1 (full coupling in TetA):

```
s = -1:  f = F_MINUS = 13    deep inside TetB
s =  0:  f = F_ZERO  = 17    the vortex throat (field origin)
s = +1:  f = F_PLUS  = 21    full coupling in our spacetime
```

The polynomial has three terms, each with a distinct role:

```
f(K,s) = 1   +   Ks   +   K^2
         |        |         |
       seed   propagation  interaction
```

The **seed** (1) is the ground state. It exists at all coupling levels. It is the irreducible identity of the field.

The **propagation** (Ks) carries the coupling state. It is antisymmetric: +K in TetA, -K in TetB. It is the dynamic content that distinguishes the two halves of the vortex.

The **interaction** (K^2 = 16) is the combinatorial content. It is symmetric: the same in both halves. It counts the number of pairwise interactions between K = 4 faces of the tetrahedron.

---

## Part 2: Nuclear Packing

### What happens in the basement

An unbound proton is a lone gravity vortex spiraling inward from TetA down through the throat into TetB. Nothing is packed in the basement. The vortex is one-directional: inward.

When other gravity fields enter the host's TetB, nuclear binding occurs. The additional fields (which we observe as neutrons and additional protons) pack into the basement of the host. This is nuclear structure. The packing follows the Sierpinski hierarchy of the coupling polynomial, with positions distributed across gate depths [27, 27, 9, 1] per shell of 64.

**The packing is not in our spacetime.** The nucleons are packed in TetB, the subspace of the host. This is why nuclear structure is so much smaller than atomic structure: the packing happens in the basement, not in the living room. The nuclear radius (~1 fm) is the TetA projection of TetB packing geometry.

### The vortex reversal

When the basement is empty, the vortex spirals inward. When the basement fills with packed fields, something changes: the packing creates pressure. The compression in TetB pushes outward through the throat.

This reversal is bidirectional. The inward gravity vortex still exists (gravity is always attractive), but now there is also an outward vortex driven by the TetB packing pressure. The outward vortex spirals from TetB through the throat into TetA, like a cyclone or tornado that has formed in the basement and is blowing upward into our spacetime.

**This outward vortex IS the electric field.** The electric field is not a separate force attached to the proton. It is the structural consequence of packing in TetB. A proton has an electric field because it has internal structure. The more packing (more nucleons bound), the more internal pressure, the stronger the outward vortex.

This is why the neutron has no net electric field: its internal packing configuration is balanced in a way that does not produce a net outward vortex. And it is why the electric field strength (the charge) is quantized: the packing pressure comes in discrete units of the coupling polynomial.

---

## Part 3: Electrons Are Not Particles

### The gravity tile excitation picture

The host proton sits in a fabric of gravity fields. Every point in space is a gravity tile, an unbound gravity vortex in its ground state. These tiles are the neighbours of the host.

When the outward electric vortex (driven by TetB packing pressure) reaches a neighbouring tile at a specific radius, it excites that tile. The tile lights up. The excitation energy is m_e = 0.511 MeV, which is the energy of one complete 2pi closure revolution of the vortex deposited into one tile.

**This excitation is what we detect as an electron.** There is no particle orbiting the nucleus. There is no little ball on a track. There is an outward vortex (electric field) painting excitation patterns onto the surrounding gravity tiles at specific radii. What we call "electron shells" are the radial boundaries where the vortex has enough energy to light up tiles.

### Why this explains electron shell structure

The outward vortex has radial structure set by the Sierpinski hierarchy. As it spirals outward from the throat, it passes through natural nodes determined by the coupling depth d = n + l:

- At depth d = 1: the first radial boundary (1s shell), lights up 2 tiles
- At depth d = 2: the next boundary (2s), lights up 2 more tiles
- At depth d = 3: two boundaries (2p and 3s), lights up 6 + 2 = 8 tiles
- And so on, following the Madelung (n+l) filling order

The filling order is not "electrons falling into orbitals." It is the vortex progressively reaching further radii as the packing pressure increases. Add more nucleons to TetB, the outward vortex gets stronger, it reaches further, it lights up more tiles at greater radii.

This is why the electron configuration follows from the same polynomial that gives binding energy. The polynomial describes the vortex. The vortex's inward structure (TetB packing) gives nuclear binding. The vortex's outward structure (electric field) gives electron shells. They are two readings of the same object.

---

## Part 4: The Three Closure Cycles

### What closure means

The coupling polynomial f(K,s) = 1 + Ks + K^2 must complete a full revolution for the field to close. "Closure" means the vortex returns to its starting state after traversing the polynomial through all coupling levels.

A complete closure revolution has the coupling state s trace a full cycle: from s = -1 (deep TetB) up through s = 0 (throat) to s = +1 (full TetA coupling), then back down through s = 0 to s = -1. This is one complete oscillation, one 2pi revolution.

### The three cycles

In D = 3 spatial dimensions, closure requires three complete cycles of the Sierpinski generator. Each cycle subdivides the tetrahedral structure one level deeper:

**Cycle 1** generates the face structure. One tetrahedron is subdivided into K = 4 sub-tetrahedra. This creates the 4 faces of the coupling.

**Cycle 2** generates the channel structure within each face. Each of the 4 sub-tetrahedra is itself subdivided into 4, giving 16 face-channel pairs.

**Cycle 3** generates the subchannel structure within each channel. Each of the 16 face-channel pairs subdivides into 4, giving 64 total positions.

At each cycle, the Sierpinski rule applies: subdivide into 4, remove the center. The removed center is the gate. The 64 positions distribute across gate depths [27, 27, 9, 1] depending on how many of the 3 cycles have their center removed.

### The closure energy

The energy of one complete 2pi closure revolution through all 3 cycles is the electron mass:

```
m_e = 0.51100 MeV
```

This is not a coincidence. The electron mass IS the closure energy. It is the energy cost of one complete revolution of the vortex through the polynomial. When the outward electric vortex deposits one revolution's worth of energy into a gravity tile, that tile becomes excited by exactly m_e. This is why the electron mass is what it is.

---

## Part 5: The Gate Coupling b

### Why b = m_e / (F_ZERO - 1/2)

The gate coupling b is the energy per structural channel visible from TetA per half-cycle of the closure revolution.

The full revolution traces the polynomial through two half-cycles:

**First half-cycle:** s goes from -1 to +1 (TetB to TetA). The polynomial's binding content at the endpoints is F+ - 1 = 20 channels (TetA) and F- - 1 = 12 channels (TetB). The propagation terms (+K and -K) cancel over the full revolution.

**Second half-cycle:** s goes from +1 back to -1 (TetA to TetB).

Over both half-cycles, the total structural content is:

```
F+ + F- = (1 + K + K^2) + (1 - K + K^2) = 2 + 2K^2 = 2 x F_ZERO = 34
```

The propagation terms cancel. What remains is twice the symmetric content.

But the identity seed "1" appears only once in the polynomial. It is the ground state. It sits at the vortex throat, shared between the two halves of the hourglass. The binding channels (the channels that actually carry nuclear energy) are:

```
2 x F_ZERO - 1 = 33
```

Per half-cycle, that is 33/2 = 16.5 effective channels.

### The TetA observation

From our spacetime (TetA), we observe only the top half of the hourglass. The packing is in TetB, but we measure the energy that leaks through the throat. The 16.5 channels per half-cycle are the channels visible from our side.

The gate coupling is therefore:

```
b = m_e / (F_ZERO - 1/2)
  = 0.51100 / 16.5
  = 0.03097 MeV
```

This is the closure energy per 2pi revolution, divided by the effective channel count visible from TetA, per half-cycle.

### Why the neural network got 0.0304

The neural network trained on measured binding energies (TetA observations). It found b ≈ 0.0304, which is close to m_e / F_ZERO = 0.03006 but rounded up by training noise. The NN implicitly divided by the full polynomial average (F_ZERO = 17 channels) instead of the TetA-visible count (16.5 channels). It did not know about the vortex geometry. It overcounted by half a channel because it treated the throat as fully accessible when in fact half the identity sits in TetB.

The corrected value b = 0.03097 improves the prediction from 1.72% to 1.58% MAPE. The improvement comes from properly accounting for the observation geometry: we live in TetA, not in the full vortex.

---

## Part 6: The Three-Scale Formula

### The 64 positions and their gate depths

Each shell of the Sierpinski walk has K^D = 64 positions. The three closure cycles create four gate depths:

```
gd=0: C(3,0) x 3^3 = 27 positions   no gate crossing in any cycle
gd=1: C(3,1) x 3^2 = 27 positions   gate crossing in exactly 1 of 3 cycles
gd=2: C(3,2) x 3^1 =  9 positions   gate crossing in exactly 2 of 3 cycles
gd=3: C(3,3) x 3^0 =  1 position    gate crossing in all 3 cycles (negligible)
```

The binomial expansion (3+1)^3 = 27 + 27 + 9 + 1 = 64 is the distribution of gate encounters across the three closure cycles. A position at gd=0 never encounters the gate (it sits in the "corner" of every Sierpinski subdivision). A position at gd=2 encounters the gate in two of three cycles (it sits in the "center" of two subdivisions).

### What each depth carries physically

**gd=0 (27 positions): Face -- the topology of the packing**

These positions never cross the gate. They are the fully spatial content of the walk. Their energy per position is:

```
a(A) = b x [3 + (9/K) x ln(1 + A/K^3)]
     = 0.03097 x [3 + 2.25 x ln(1 + A/64)]
```

This depends only on A, the total nucleon count. From TetA, we can count how many fields are packed in the host's basement. The topology of the packing (how many positions are filled) is visible as a bulk property. Face reads this count through the logarithmic walk fill.

The three constants in the formula are the three closure cycles (3), the closure-to-coupling ratio (9/K = 2.25), and the shell capacity (K^3 = 64).

Total: Face = 27 x a(A). Ranges from 2.6 MeV (Helium, A=4) to 5.3 MeV (Uranium, A=238).

**gd=1 (27 positions): Chan -- the throat coupling**

These positions cross the gate in exactly one of the three closure cycles. They are the generator content: the energy of one Sierpinski iteration passing through the gate once.

Their energy per position is b = 0.03097 MeV, the gate coupling constant. It is universal. It does not depend on Z or A. It is the same for Helium and Uranium. It is the energy cost of one channel of communication between TetB (where the packing is) and TetA (where we observe).

Total: Chan = 27 x b = 0.836 MeV. Constant everywhere.

**gd=2 (9 positions): Sub -- the closure at the throat**

These positions cross the gate in two of the three closure cycles. They sit at the vortex throat. They are the interface between TetA and TetB.

Their energy per position is c(Z,A), which starts from a ceiling and is reduced by the packing corrections:

```
c(Z,A) = c_max(A) - c_surf(A) - c_coul(Z,A) - c_asym(Z,A) + c_pair(Z,A)
```

Every correction enters at gd=2 because the throat is where TetB physics meets TetA observation:

- **c_surf** is the boundary of the packing region in TetB. Where the packing meets the wall of the host's TetB volume, closure is incomplete.

- **c_coul** is the proton charge radiating through the throat. The protons are packed in TetB, but their electromagnetic repulsion is the outward vortex that operates in TetA. The Coulomb term measures how much of TetB's charge content is visible from TetA.

- **c_asym** is the neutron-proton imbalance in the packing. When the TetB packing is asymmetric (N is not equal to Z), the closure at the throat is imperfect.

- **c_pair** is the spin-pairing bonus in the packing. Even-even configurations in TetB produce cleaner closure at the throat.

Total: Sub = 9 x c(Z,A). Ranges from 4.6 MeV (Carbon) to 1.9 MeV (Lead).

### The complete formula

```
B/A = 27 x a(A) + 27 x b + 9 x c(Z,A)
    = Face      + Chan    + Sub
```

This is the binding energy per nucleon as seen from TetA: the topological count (Face), the throat coupling (Chan), and the closure energy at the interface (Sub).

---

## Part 7: The Closure Coefficients

Each correction in the closure energy c(Z,A) has a structural coefficient derived from the polynomial and the gate attenuation eps = 2/F_ZERO = 2/17.

### The ceiling

```
c_max(A) = (Vol - Face - Chan) / 9
```

where Vol = F+ x D/(D+K) x sqrt(D) = 15.588 MeV is the volume energy. This is the maximum binding per closure position if the nucleus were infinite, symmetric, and uncharged. It decreases as A grows because Face takes a larger share.

### Surface: F_ZERO x (1 + eps^2)

The gate attenuation eps = 2/17 is the fractional energy loss per gate crossing. The gate is the removed center of the Sierpinski triangle. It operates once per closure cycle.

At the nuclear surface (the boundary of TetB packing), the closure positions experience additional gate exposure. The surface is a 2D manifold (codimension 1 in 3D space). Two transverse directions each contribute one gate crossing at rate eps, giving eps^2 = (2/17)^2 = 0.0138 total excess.

```
Surface coefficient = F_ZERO x (1 + eps^2) = 17 x 1.0138 = 17.235
```

This matches the standard Bethe-Weizsacker fitted value of 17.23 to 0.03%.

### Coulomb: b x (F+ + F-/K - 1)

The Coulomb coefficient combines the gate coupling b with the polynomial spread:

```
F+ + F-/K - 1 = 21 + 13/4 - 1 = 23.25
```

This is the full range of the polynomial (from deep field to full coupling), normalized by the branching factor at the deep end and minus the identity. Physically, it measures how much of the vortex's coupling range contributes to the charge interaction across the throat.

```
Coulomb coefficient = 0.03097 x 23.25 = 0.720
```

### Asymmetry: F+ + F-/K - 1

The same polynomial spread as Coulomb, but without the b factor:

```
Asymmetry coefficient = 23.25
```

This is a pure number. The asymmetry penalty is not an energy scale (that is set by the formula's geometry through (N-Z)^2/A^2) but a structural weight from the polynomial.

### Pairing: D x K

```
Pairing coefficient = 3 x 4 = 12
```

Exact. Spatial dimensions times branching factor. The pairing energy is the most discrete of the corrections: it depends only on whether Z and N are even or odd.

---

## Part 8: The Electric Field and Electron Shells

### From packing pressure to the outward vortex

When the host's TetB fills with packed gravity fields (nucleons), the packing pressure drives an outward vortex through the throat into TetA. This outward vortex IS the electric field.

The vortex has radial structure. As it spirals outward, it passes through natural boundaries set by the Sierpinski hierarchy. The coupling depth d = n + l determines the radius of each boundary:

- Deeper Sierpinski levels (higher l) bind more tightly to the host
- Higher principal numbers (higher n) reach further from the throat
- The total depth d = n + l sets the radial order

### Filling order as vortex illumination

The Madelung filling rule says: fill sub-shells in order of ascending d = n + l, with deeper Sierpinski (higher l) first within each d.

In the vortex picture, this means: as packing pressure increases (more nucleons in TetB), the outward vortex reaches further and further radii. At each new radius, it lights up the gravity tiles there. The order in which tiles light up follows the polynomial's energy ordering: the closure positions (highest energy per position, c > a > b) are excited first because they sit closest to the throat.

The sub-shell capacities come from the angular structure of the 3D vortex:

```
l=0 (s): 1 orientation x 2 (spin) = 2 tiles lit per boundary
l=1 (p): 3 orientations x 2        = 6 tiles
l=2 (d): 5 orientations x 2        = 10 tiles
l=3 (f): 7 orientations x 2        = 14 tiles
```

The total per shell pair: 2 + 6 + 10 + 14 = 32 = K^3/2. Half the walk positions carry the outward (electric) vortex structure. The other half carry the inward (gravity) vortex structure.

### Why there are no electron particles

The "electrons" are not objects. They are the gravity tiles at specific radii that are excited by the outward vortex. When we "remove an electron" (ionization), we are reducing the excitation at that radial boundary. When we "add an electron" (electron capture), we are increasing it.

The ionization energy of each shell corresponds to the vortex energy density at that radius. Inner shells (closer to the throat) have higher ionization energies because the vortex is stronger there. Outer shells are weaker.

The spin-1/2 behaviour of electrons is the same observation geometry as the gate coupling: from TetA, we see half the vortex revolution. One tile excitation appears to need 4pi to complete a full rotation because we only see the TetA half of the hourglass. The tile itself, as an unbound gravity field, has the full vortex structure, but our observation is limited to the TetA projection.

---

## Part 9: Putting It All Together

### The complete picture in one paragraph

A proton is a gravity vortex. Other gravity fields pack into its TetB (basement), creating nuclear binding. The packing pressure reverses the vortex direction, producing an outward electric field that illuminates surrounding gravity tiles as "electrons." The binding energy distributes across 64 walk positions at three gate depths: 27 spatial positions read the topology (Face), 27 generator positions carry the universal throat coupling (Chan), and 9 closure positions at the vortex throat absorb all composition-dependent corrections (Sub). The gate coupling b = m_e / 16.5 is the electron mass (one 2pi closure revolution) divided by the channels visible from TetA (the polynomial average minus the half-identity shared with TetB at the throat).

### The derivation chain

```
2(D+1) = 2^D  -->  K = 4, D = 3  (unique solution)
                     |
f(K,s) = 1 + Ks + K^2  -->  F+ = 21, F0 = 17, F- = 13
                     |
m_e = 0.51100 MeV  (closure energy per 2pi revolution)
                     |
b = m_e / (F0 - 1/2) = 0.03097  (energy per TetA-visible channel)
                     |
eps = 2/F0 = 2/17  (gate loss per crossing)
                     |
Five structural coefficients:
    Volume   = F+ x D/(D+K) x sqrt(D)     = 15.588
    Surface  = F0 x (1 + eps^2)            = 17.235
    Coulomb  = b x (F+ + F-/K - 1)        =  0.720
    Asymmetry = F+ + F-/K - 1             = 23.250
    Pairing  = D x K                       = 12
                     |
Three-scale prediction:
    a(A) = b x [3 + 2.25 x ln(1 + A/64)]
    c(Z,A) = c_max - surf/9 - coul/9 - asym/9 + pair/9
    B/A = 27a + 27b + 9c
                     |
Electron shells from the same polynomial:
    d = n + l, fill ascending, deeper l first
    118/118 elements correctly classified
```

### Performance

With b = 0.03097 (structural), on 78 core elements (Z = 6 to 83):

```
MAPE:       1.58%
Within 1%:  40/78 (51%)
Within 2%:  59/78 (76%)
Sub > 0:    78/78 (100%)
```

Zero fitted parameters. The only measured input is m_e.

---

## Part 10: Frequently Asked Questions

### If electrons are not particles, what are we detecting in experiments?

You are detecting the excitation state of gravity tiles at specific radii from the host. The excitation carries charge, angular momentum, and energy, all properties of the vortex at that radius. It responds to electromagnetic fields because it IS the electromagnetic field at that point. The "particle" description works as an effective model because the excitation is localized at a radial boundary and carries discrete quantum numbers. But there is no little ball.

### Why does the neutron not produce an electric field?

The neutron's internal packing configuration is balanced. Its TetB content produces equal outward pressure in all directions, resulting in no net outward vortex. It has internal structure (it is a bound gravity field with packing) but the packing does not create a directional cyclone. This is why the neutron has a magnetic moment (it has spinning internal structure) but no net charge (no directional outward vortex).

### Why is nuclear structure so much smaller than atomic structure?

Nuclear structure is the packing in TetB (the basement). Atomic structure is the outward vortex in TetA (our spacetime). The basement is compact. The living room is large. The ratio of nuclear to atomic radii (about 10^5) reflects the ratio of TetB packing density to TetA vortex extent.

### Why does the formula use the standard BW structure (volume, surface, Coulomb, asymmetry)?

Because the BW terms describe the geometry of TetB packing as seen from TetA. Volume is the total packing content. Surface is the packing boundary. Coulomb is the charge leaking through the throat. Asymmetry is the composition imbalance. These are not "liquid drop model assumptions." They are the natural decomposition of a packed TetB observed through a vortex throat. The GFD contribution is deriving the coefficients rather than fitting them.

### What is the gate physically?

The gate is the removed center of the Sierpinski triangle. At each closure cycle, the central sub-triangle is not filled. Physically, this is the vortex throat itself: the narrowest point of the hourglass, where the field transitions between TetA and TetB. The gate attenuation eps = 2/F_ZERO = 2/17 is the fraction of coupling that is lost at each passage through the throat. The "removed center" is not empty, it is the passage.

### Can this predict beyond Z = 83?

Yes. The formula extends to all elements through Oganesson (Z = 118) and beyond. The framework does not have a cutoff at Bismuth. The B/A prediction for superheavy elements uses the same formula with the same constants. The only degradation is data quality: for Z > 103, the experimental B/A values are themselves estimates from mass models.

---

## Files

| File | Purpose |
|------|---------|
| `gfd_3scale_binding.py` | Prediction script with full validation |
| `gfd_3scale_binding.csv` | Per-element results with closure breakdown |
| `gfd_3scale_binding_synthesis.md` | Technical synthesis (structural derivation) |

```bash
python gfd_3scale_binding.py              # full validation
python gfd_3scale_binding.py 26 56        # predict Iron-56
python gfd_3scale_binding.py 92 238       # predict Uranium-238
```

---

*Stephen Nelson, 2025-2026, Field Dynamics. CC BY 4.0.*
