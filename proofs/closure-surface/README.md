# Where Closure Sits: the Field's Stagnation Surface and the Jacobi Surface

Every field object closes, locally, at every level: an asteroid is a pointer in the solar system's accounting, the solar system in the galaxy's ([mountain-scale proof](../sst-mountain-scale/)). This proof asks **where** an object's closure surface sits.

This folder holds a three-page proof, a script that checks it (16 checks), and a Lean 4 formalisation (8 theorems) that imports the mountain-scale formalisation.

## The picture

A bound object on a near-circular orbit, seen from the frame turning with it. Its own field, the host's tide and the orbit's turning add up to one effective potential, Φ_eff = −GM/r − ½Tx² + ½ν²z², with T = 4Ω² − κ².

- **The field alone defines a surface.** The combined field vanishes at exactly two points, the stagnation points on the host's radius at the Jacobi radius, r_J³ = GM/T. The level through them bounds the object: Σ_field.
- **Matter below the stagnation level stays in its cell.** The Coriolis force does no work, so the Jacobi energy is conserved, and matter below the stagnation level can never reach it. The surface it cannot leave, Σ_Jacobi, is Σ_field.
- **Matter above it can snap to a neighbouring cell,** and only through the two necks that open at the stagnation points: the doors.
- **The cell is anchored by its surroundings.** Without the host's tide there are no stagnation points and no boundary. In Paper VII's picture the unbound envelopes (TetB chambers empty) form the mesh, vorticing into TetB, and the bound cells, the matter, move through it; that surrounding flow is what anchors a bound cell.
- **A vortex does the same.** A point vortex in a strain stagnates at two points; its closed streamlines are bounded by the separatrix through them. An eddy carries the fluid inside its separatrix as one unit; a bound object carries what is inside its stagnation surface.

So the surface the field registers and the surface matter cannot leave are one surface. What remains a premise narrows to one geometric statement: **registration happens at the field's stagnation surface.**

## Results

1. **The stagnation surface (Theorem 1).** The field vanishes only at x = ±r_J; they are saddles; the level through them is E_c = −(3/2)GM/r_J.
2. **The surface matter cannot leave (Theorem 2).** 40 orbits below E_c, over forty host orbits each, stay in the cell (farthest 0.74 r_J). Above E_c, matter snaps to a neighbouring cell only through the necks: every one that left passed 1.05 r_J within 30° of the host's radius. The condition is sufficient, not necessary: just above E_c, 70% of prograde and 3% of retrograde orbits snap out in that time. Without the host's tide (T → 0) the boundary recedes to infinity: the surroundings anchor the cell.
3. **The vortex (Theorem 3).** Predicting 55 parcels' fates from the streamfunction alone agrees with integrating them in every case.
4. **Not a sphere (Theorem 4).** It reaches r_J along the host's radius, 2/3 r_J along the orbit and, for the Sun, 0.50 r_J out of the plane; its volume is that of a sphere of 0.64 r_J. The mountain-scale proof's sphere of radius r_J is an outer bound.
5. **The rule reproduces itself (Theorem 5).** T is the host field's own curvature in the turning frame (2Ω² for a flat curve, the deep law's mountain). Under ownership the members move in exactly Φ_eff, so ownership at the stagnation surface holds every member inside it.
6. **Tests (Proposition 6).**
   - **Planets:** Neptune is 3,300 times deeper than the stagnation level.
   - **Oort cloud:** Kepler orbits are held for good when a < r_J/3 = 99,000 AU, the scale usually quoted for the outer Oort cloud.
   - **α Centauri:** the surfaces overlap, but its energy relative to the Sun is far above the pair's stagnation level: each is its own cell.
   - **Wide binaries:** a pair is one cell when v/√(GM/s) < √(2 − 3s/r_J), an edge set before any velocity is inspected. Inside, its motion is Newtonian with G_N. A theory that strengthens gravity inside the pair moves the edge up.
   - **Palomar 14:** its surface (157 pc by 104 pc) holds its 26 pc body.

## What it leaves open

- **That registration happens at the stagnation surface,** from the dual-tetrad dynamics. This is now the single geometric premise.
- **The snap itself:** what happens to the registered state on both sides when matter changes cells, as a discrete event.
- **Eccentric orbits and a changing host,** where the surface breathes and ownership changes in time.
- **Beyond Hill's limit,** when the object is not small against its host's scale.
- **Orbits above E_c,** which the energy condition does not cover.
- **The drained level:** a galaxy's own closure surface in its group or cluster.

## Contents

| File | What it is |
|---|---|
| [`closure_surface.pdf`](closure_surface.pdf) | The proof (3 pages) |
| [`closure_surface.tex`](closure_surface.tex) | Its source |
| [`verify_closure_surface.py`](verify_closure_surface.py), [`verify_output.txt`](verify_output.txt) | 16 checks: the stagnation surface, anchoring, staying in the cell and snapping out, the vortex, the shape, self-consistency, five tests |
| [`lean/ClosureSurface.lean`](lean/ClosureSurface.lean) | Lean 4, 8 theorems, importing the [mountain-scale](../sst-mountain-scale/lean/) formalisation |
| [`LEAN_AUDIT.md`](LEAN_AUDIT.md) | What the Lean file proves and what it does not |
