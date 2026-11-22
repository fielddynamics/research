# The Mountain Scale in the SST: the Net-Field Rule From the Action

*Writing "a field object meets the NET Field as a whole, at its closure boundary" into the action · Gravity Field Dynamics (GFD) · Field Dynamics Research*

[![Lean proof](https://github.com/fielddynamics/research/actions/workflows/lean-sst-mountain-scale.yml/badge.svg)](https://github.com/fielddynamics/research/actions/workflows/lean-sst-mountain-scale.yml)

`SST` `net-field-rule` `field-object` `closure-boundary` `Jacobi-radius` `four-ports` `preferred-foliation` `action` `proof`

---

This folder holds a four-page proof, a script that checks it (25 checks), two 3D numerical solutions, and a Lean 4 formalisation (10 theorems). It closes the step that the [time-leg](../sst-covariant-time-leg/), [net-field rule](../net-field-rule/) and [khronon](../sst-khronon-preferred-frame/) proofs left open. It has been through two external reviews; the changes are listed below.

## The picture

A mountain stream looks flat close up; zoomed out, it runs down a mountain.

- **Inside a bound system** the host's field is a flat slope, and each body is a dimple with **no drain**: pure TetA.
- **Seen from outside**, the whole mountain shows, and the law acts on it.

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
   - **4π = kπ.** Each face of the envelope's tetrahedron covers π steradians, so exactly πGM passes through each face, at any radius.
   - **The faces read the ports.** Sampling a host field at the four face directions gives the clock rate exactly (the tide drops out) and the free fall, with a small *chiral* leak of the tide: + for TetA, − for TetB. **Both tetrahedra together, the stellated octahedron, read the ports exactly**: the leak cancels.
   - **No length in the rule.** Every sphere is set by its own mass and its host's tide, so the same rule applies at every level; only a₀, in the law's crossover, sets a scale. (A Weyl rescaling is not a symmetry of these equations; these are the scale statements that hold.)
9. **The action does not choose the edge (Theorem 6),** shown for a centred spherical system. The edge is a binding criterion, which mass belongs to which field object, not an energy minimum.

## The 3D check

![The tail read pointwise; none read by ownership](fig_demo.png)

- **One system:** read pointwise, the pull around the Sun beyond its own is the tail, a₀μ(x) (0.79, 0.70, 0.58 a₀). Read by ownership it is **0.000**.
- **Two systems whose spheres overlap, each containing the other's centre:** the pull beyond Newton for both stars is between −0.002 and −0.023 a₀, against +0.6 to +0.8 for a tail. What remains is the law acting on each star's field where it lies outside that star's own sphere, as it should.

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
| Pal 14's 8.9σ | Stated as the net-field analysis's figure; the literature is divided (Jordi 2009; Gentile 2010; Sollima 2012) |
| The Jacobi radius is a premise | Agreed: the data give a window, and choosing r_J within it is the binding premise |

## What it leaves open

- **The binding criterion** (which mass belongs to which field object). It is the premise; Theorem 6 shows, for a centred sphere, that energy cannot set it.
- **Ownership that changes in time** (mergers, stripping).
- **Theorem 6 for general shapes.**
- **Higher relativistic order.**
- **The twelve-contact count**, which is the framework's geometry. The four ports are derived here at the level of the action.

## Contents

| File | What it is |
|---|---|
| [`sst_mountain_scale.pdf`](sst_mountain_scale.pdf) | The proof (4 pages) |
| [`sst_mountain_scale.tex`](sst_mountain_scale.tex) | LaTeX source (IOP class, [`iopjournal.cls`](iopjournal.cls)) |
| [`verify_sst_mountain_scale.py`](verify_sst_mountain_scale.py), [`verify_output.txt`](verify_output.txt) | 25 checks: the split with overlapping spheres (1D, two laws), the matter equation, the four ports, the overlaps, a field-dependent radius, the edge, the 3D results, and nested envelopes and the faces |
| [`demo_ownership_3d.py`](demo_ownership_3d.py), [`demo_ownership_output.txt`](demo_ownership_output.txt) | The 3D ownership solutions, one system and two overlapping (about 10 minutes) |
| [`demo_mountain_scale.py`](demo_mountain_scale.py), [`demo_output.txt`](demo_output.txt) | The 3D solver and the pointwise reference (the tail); it also contains the earlier single-scale low-pass version |
| [`make_figure.py`](make_figure.py) | Draws [`fig_demo`](fig_demo.pdf) |
| [`lean/MountainScale.lean`](lean/MountainScale.lean) | Lean 4, 10 theorems, importing the [khronon](../sst-khronon-preferred-frame/lean/) formalisation |
| [`LEAN_AUDIT.md`](LEAN_AUDIT.md) | What the Lean proves and what is cited |

## Running the checks

```
python demo_mountain_scale.py > demo_output.txt
python demo_ownership_3d.py > demo_ownership_output.txt
python verify_sst_mountain_scale.py
cd lean && lake exe cache get && lake build
```
