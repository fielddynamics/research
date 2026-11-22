# The Mountain Scale in the SST: the Net-Field Rule From the Action

*Writing "a field object meets the NET Field as a whole, at its closure boundary" into the action · Gravity Field Dynamics (GFD) · Field Dynamics Research*

[![Lean proof](https://github.com/fielddynamics/research/actions/workflows/lean-sst-mountain-scale.yml/badge.svg)](https://github.com/fielddynamics/research/actions/workflows/lean-sst-mountain-scale.yml)

`SST` `net-field-rule` `field-object` `closure-boundary` `Jacobi-radius` `four-ports` `preferred-foliation` `action` `proof`

---

This folder holds a seven-page proof, a script that checks it (36 checks), two 3D numerical solutions, and a Lean 4 formalisation (15 theorems). It closes the step that the [time-leg](../sst-covariant-time-leg/), [net-field rule](../net-field-rule/) and [khronon](../sst-khronon-preferred-frame/) proofs left open. It has been through four external reviews; the changes are listed below.

## The picture

A mountain stream looks flat close up; zoomed out, it runs down a mountain.

- **Inside a bound system** the host's field is a flat slope, and each body is a dimple with **no drain**: pure TetA.
- **Seen from outside**, the whole mountain shows, and the law acts on it.
- **Every object closes, locally, at every level.** An asteroid closes, and the solar system's accounting holds a pointer to it; the solar system closes, and the galaxy holds a pointer to it; a galaxy closes, and its cluster holds a pointer to it. The drain decides only what the interior contains: none means pure TetA, a drain means the law acts inside.

## GFD already says how a body meets the mountain

- **Paper I (§2.2–2.3):** a field object (an asteroid, a star, a cluster) is one correlated whole. The NET Field couples to it **as a whole, never to its parts**, at its closure boundary Σ.
- **Paper II (§6):** closure boundaries are spheres, and they **overlap**.
- **Paper IV and the face-structure notes:** each field unit meets its neighbours through **four** interfaces, three spatial and one temporal. In close packing a chamber has twelve contacts, of which the four face-to-face ones are the active ports.

So **fields overlap**, and neighbours read each other. What is single-valued is **ownership**: which field object a piece of mass belongs to.

## What this proof does

1. **The ownership sweep.** Each bound system sweeps **its own mass** onto its own closure sphere, its Jacobi sphere, r_J³ = GM/(4Ω² − κ²).
   - Sweeping a mass onto a sphere leaves its field outside the sphere exactly unchanged, for any shape of system.
   - The spheres may overlap and contain other systems: each one sweeps only what it owns.
2. **The action** reads the curvature term (all of Newton and Einstein) at every point, and the law's term on the **mountain**: the total field minus each system's own interior field.
3. **The split is exact (Theorem 1):**
   - the mountain obeys the **plain law** (not a projected one) on the density with every system's mass on its own sphere;
   - each system's own field is **Newtonian with the bare G**, zero outside its sphere, and the same whatever the law is.
4. **The four ports (Theorem 2).** At leading order a field object meets the NET Field through exactly four channels:
   - one temporal: its clock rate, the lapse;
   - three spatial: its free fall.

   That is the tetrad's 1 + 3 legs. The next channel, the tide, needs the object's size and is suppressed by (s/r_J)³ (3 × 10⁻¹⁴ at Saturn).
5. **What follows (Theorem 3):**
   - no tail;
   - neighbours keep their full Newtonian pull on each other;
   - the Sun's own matter feels one extra tide-sized term (about 2 × 10⁻¹⁹ m/s² at Saturn), from the galaxy's TetB density inside its sphere.
6. **The overlaps are real (Proposition 4).**
   - α Centauri, 1.34 pc away, has a 1.81 pc sphere; the Sun's is 1.44 pc. Each contains the other's centre.
   - In the solar neighbourhood the spheres fill about 60% of space, above the threshold at which overlapping spheres join up across space.
   - So merging overlapping regions would turn the whole disc Newtonian. Ownership merges nothing.
7. **A field-dependent radius (Theorem 5)** only nudges the mountain (by 2 × 10⁻³ in the test). Each system's own field stays Newtonian by construction.
8. **Nested envelopes and the faces (Theorem 7, Paper VII §IX).** Section IX says every system, atom, star or galaxy, closes its own envelope with the same k = 4 structure and the same Poisson equation. In the action this is exact:
   - **Nesting telescopes.** Sweeping onto the star's envelope and then onto the system's equals sweeping straight onto the system's, so each level is its own Poisson field with the same 4πG, and inner envelopes are invisible above their level.
   - **4π = kπ.** Each face of the envelope's tetrahedron covers π steradians. The total flux is 4πGM for any object (Gauss). Per face it is πGM for a centred, round mass; for an asymmetric object (an oblong asteroid) the faces differ by its dipole (zero if the sphere is centred on its centre of mass) and part of its quadrupole, suppressed by (s/R)², about 10⁻⁸ for the planets in the Sun's sphere. The four ports describe the coupling structure, not four equal fluxes.
   - **The faces read the ports.** Sampling a host field at the four face directions gives the clock rate exactly (the tide drops out) and the free fall, with a small *chiral* leak of the tide: + for TetA, − for TetB. **Both tetrahedra together, the stellated octahedron, read the ports exactly**: the leak cancels.
   - **Scale-universal, not scale-invariant.** The same rule applies at every level, but the hierarchy is not self-similar: in a flat host, stretching the host by λ stretches a closure radius by λ^(2/3), and a₀ sets a scale in the law's crossover. (A Weyl rescaling is not a symmetry of these equations.)
9. **Registration implies the sweep (Theorem 8).** Paper I: at the closure boundary, settlement records a unique registered state B*_Σ. Take that state as the object's potential on its boundary, and add one premise: settlement fills the interior with the *least field energy* compatible with it. Then the interior field is harmonic and unique, and it is exactly the field of the object's mass swept onto the boundary, the ownership sweep. The energy splits exactly: own field = registered field + residual. For a mass off-centre the swept density is the Poisson kernel and the interior is the Kelvin image field (checked to 10⁻⁹ in 3D). So registration ⇒ sweep ⇒ split; what remains open is why field closure selects least-energy settlement, and where each closure surface sits.
10. **The action does not choose the edge (Theorem 6),** shown for a centred spherical system. Every object closes; where its surface sits is set by the dynamics, not by an energy minimum.

## The 3D check

![The tail read pointwise; none read by ownership](fig_demo.png)

- **One system:** read pointwise, the pull around the Sun beyond its own is the tail, a₀μ(x) (0.79, 0.70, 0.58 a₀). Read by ownership it is **0.000**.
- **Two systems whose spheres overlap, each containing the other's centre:** the pull beyond Newton for both stars is between −0.002 and −0.023 a₀, against +0.6 to +0.8 for a tail. What remains is the law acting on each star's field where it lies outside that star's own sphere, as it should.

## The Cassini quadrupole (Theorem 9)

In AQUAL the Sun's own field enters the law, and the Galactic field makes the result anisotropic: the planets feel a quadrupole, Q₂. Cassini excluded the standard laws, and the 2026 bound is Q₂ = (1.6 ± 1.8) × 10⁻²⁷ s⁻² (Park et al., PRD 114, 024066). Under ownership the Sun's own field never enters the law; the law sees only its mass, swept onto its 1.44 pc sphere.

- The mountain's linear response is anisotropic: along the Galactic field it is 1 + 1/(1+x) times the response across it, 1.4 at the Sun.
- Stretching coordinates along the field removes the anisotropy and turns the uniform swept shell into a homoeoid (a thin uniform shell between similar ellipsoids). A homoeoid has no field inside (Newton). Check: 9 × 10⁻⁹ GM/r_J³, against 3 × 10⁻² for a non-homoeoid control.
- What remains is the Galactic tide, GM/r_J³ = 4Ω² − κ² = 1.5 × 10⁻³⁰ s⁻² (present in GR too), and the trace term, (tr T/3)x, which is isotropic.
- **Prediction: no anomalous Q₂ at this order; residuals below about 10⁻³⁰ s⁻², a thousand times under the bound.** The same law read pointwise is AQUAL with the simple law, which Cassini excludes. This is for the centred spherical shell in a constant linear response; a non-spherical surface is bounded, not computed.
- A second proof, by the Green function: for any constant positive-definite response the kernel is even and falls off as 1/r, so a uniform shell's potential is constant inside.
- **The closure surface carries the TetB share (9(d)).** The potential is continuous; its slope kinks by [n·(1 − μ̄)∇Φ̄], a phantom surface layer, the (1 − μ̄) share of the swept mass, already in the field equation. For the Sun: 1.28 × 10⁻¹⁴ m/s² along the Galactic field, 4.48 × 10⁻¹⁴ across it. Inside, the Sun's field is Newtonian; outside, the law reads it, 1.2–1.7× stronger. A closed eddy has the same structure: a vortex sheet at its edge in the frictionless limit (Sadovskii), smoothed by viscosity into a thin layer. The relativistic junction conditions at the surface are not checked.

## Reviews, and what changed

| Review point | Response |
|---|---|
| A scale that varies from place to place breaks the spectral projector | Replaced: there is no projector on the field now, only each system's own interior field removed |
| Real Jacobi spheres overlap (α Cen) | Allowed: ownership, not space, decides what each system sweeps. Merging regions would join one Newtonian region across the disc (shown) |
| The split must survive a field-dependent projector | Each system's own field is Newtonian by construction for any radius; a field-dependent radius only changes the mountain's equation (Theorem 5) |
| Non-spherical systems | Outside its sphere a system's field is exact for any shape; inside, its own multipoles enter the mountain, suppressed by (s/r_J)³ |
| Theorem on the edge was stronger than its proof | Now stated for a centred spherical system only |
| Check C2 was `True` | Removed; every check computes something |
| The 3D demo used a different projector | The 3D runs now use the ownership sweep itself, with one system and with two overlapping |
| The mountain obeyed a projected law | It now obeys the plain law |
| Theorem 7(b) claimed equal flux πGM through every face, for any shape (third review) | Corrected: the total is 4πGM; per face, πGM plus the object's dipole and part of its quadrupole, measured (29% through the nearest face for a mass 0.1R off-centre) |
| Scale invariance (third review) | Now "scale-universal": the closure radius scales as λ^(2/3) in a flat host |
| The four-port count 1 + 3 is generic for any smooth potential (third review) | Agreed and stated; the tetrahedral content is how the faces read the ports and the chiral cancellation |
| Which level owns a planet's mass (third review) | Every object closes, locally, at every level: the asteroid is a pointer in the solar system's accounting, the solar system in the galaxy's, the galaxy in its cluster's. Nested sweeps telescope, so the pointer is exact. The drain decides only what the interior contains: drainless means pure TetA (Newtonian), drained means the law acts inside. The drained level (a galaxy as a pointer in its cluster) is not treated here |
| Assumptions, constants and the matter test (third review) | Assumptions listed; G is Newton's G_N (Paper VII's (17/13)G_bare); the matter test compares forces, not potentials |
| The matter variation was incomplete (fourth review) | With the sweep varied, the extra force is tide-sized (B1). With the sphere centred on the centre of mass, its motion gives every member the same acceleration, (∂S/∂c)m_i/M: it moves the system as a whole and drops out of internal motion (~7 × 10⁻¹⁵ m/s² for the Sun). A constrained variational formulation is still open |
| Inside an envelope the mountain is not harmonic (fourth review) | Agreed: the face sum is 4c₀ + (2/3)R² tr T, tr T = 4πG(ρ_diffuse + ρ_TetB); the chiral cancellation is unaffected (Lean updated) |
| Units in the action; Newtonian vs constitutive flux; "no tail" (fourth review) | c⁴ restored; the conserved flux for the mountain is ∮μ∇Φ̄·dA; "no tail" now means no pointwise self-tail, with the small environment-dependent terms sized |
| Energy reading of Theorem 6; space-filling wording; real Jacobi surfaces (fourth review) | Now "the action does not select a finite radius"; η = 0.63 is the reduced density, covering 47%; sweeping works onto any closed surface, so the true anisotropic Jacobi surface can be used |
| Pal 14's 8.9σ | Stated as the net-field analysis's figure; the literature is divided (Jordi 2009; Gentile 2010; Sollima 2012) |
| Fifth review: connections to potential theory | Adopted: telescoping is the strong Markov property of balayage (a mathematical equivalence, not a mechanism); the anisotropic response and trace corrector give Theorem 9. Not adopted: a two-radius reconstruction that cancels the trace term, because the trace is the local density the scalar port reads. A boundary (Dirichlet-to-Neumann) action is noted as a route for the full variation |
| Sixth and seventh reviews: the anisotropic shell and the interface | The Green-function proof added as a second proof of 9(b). The interface jump is real and is now Theorem 9(d): a kink with the potential continuous, a phantom surface layer already in the field equation, not an inconsistency. The khronon reading is stated as an interpretation; the Israel junction conditions and energy across a moving surface are listed as open. The vortex analogue is a vortex sheet (a jump in the field's slope), not a vorticity jump, which is one derivative higher |
| The Jacobi radius is a premise | Agreed: the data give a window, and choosing r_J within it is the premise of where the surface sits |

## What it leaves open

- **Least-energy settlement** (Theorem 8's premise) as a consequence of field closure in the dual-tetrad dynamics.
- **Where each closure surface sits** (here the Jacobi radius). It is the premise; Theorem 6 shows, for a centred sphere, that energy cannot set it. The [closure-surface proof](../closure-surface/) shows the field's stagnation surface and the orbits' trapping surface are one surface, and narrows the premise to registration at that surface.
- **The drained level:** a galaxy as a pointer in its cluster, with the law acting inside its own accounting, and what mass its pointer carries.
- **Ownership that changes in time** (mergers, stripping), and energy across a moving closure surface.
- **The junction conditions** at the closure surface, which must come from the action.
- **Theorem 6 for general shapes**, and the exact non-spherical closure surface in Theorem 9 (bounded, not computed).
- **Higher relativistic order.**
- **The twelve-contact count**, which is the framework's geometry. The four ports are derived here at the level of the action.

## Contents

| File | What it is |
|---|---|
| [`sst_mountain_scale.pdf`](sst_mountain_scale.pdf) | The proof (7 pages) |
| [`sst_mountain_scale.tex`](sst_mountain_scale.tex) | LaTeX source (IOP class, [`iopjournal.cls`](iopjournal.cls)) |
| [`verify_sst_mountain_scale.py`](verify_sst_mountain_scale.py), [`verify_output.txt`](verify_output.txt) | 36 checks: the split with overlapping spheres (1D, two laws), the matter equation, the four ports, the overlaps, a field-dependent radius, the edge, the 3D results, nested envelopes and the faces, registration ⇒ sweep, the Cassini quadrupole, and the closure-surface kink |
| [`demo_ownership_3d.py`](demo_ownership_3d.py), [`demo_ownership_output.txt`](demo_ownership_output.txt) | The 3D ownership solutions, one system and two overlapping (about 10 minutes) |
| [`demo_mountain_scale.py`](demo_mountain_scale.py), [`demo_output.txt`](demo_output.txt) | The 3D solver and the pointwise reference (the tail); it also contains the earlier single-scale low-pass version |
| [`make_figure.py`](make_figure.py) | Draws [`fig_demo`](fig_demo.pdf) |
| [`lean/MountainScale.lean`](lean/MountainScale.lean) | Lean 4, 15 theorems, importing the [khronon](../sst-khronon-preferred-frame/lean/) formalisation |
| [`LEAN_AUDIT.md`](LEAN_AUDIT.md) | What the Lean proves and what is cited |

## Running the checks

```
python demo_mountain_scale.py > demo_output.txt
python demo_ownership_3d.py > demo_ownership_output.txt
python verify_sst_mountain_scale.py
cd lean && lake exe cache get && lake build
```
