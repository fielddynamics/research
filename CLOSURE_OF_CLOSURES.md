# Closure of Closures

*How can gravity close a universe without recounting every grain of sand in it? Gravity Field Dynamics proposes that nature keeps its books the way a well-run organisation does: locally, once, and by reference.*

**Stephen Nelson** · Field Dynamics Research

---

## The problem: you cannot recount the universe

Stand on a beach and drop a pebble. It falls because the Earth pulls on it. But strictly, according to Newton, the pebble is pulled by everything: the sand beneath your feet, the mountains on the horizon, the Moon, the Sun, the hundred billion stars of the Milky Way, every galaxy out to the edge of what we can see. To work out the force on that one pebble, Newton's law says you should add up the pull of every particle in the universe, one at a time. The observable universe holds something like $10^{80}$ protons and neutrons alone.

Now ask a bigger question. Not what pulls on one pebble, but how the universe as a whole settles its gravity: how every system, from an asteroid to a supercluster of galaxies, comes to a consistent field. Call that cosmic-scale closure.

Here is the problem. Suppose that each time a larger system closed, it had to reopen everything inside it.

A star system would have to recount every planet, every moon, every asteroid and every grain of rock in them. A galaxy, closing over its hundred billion star systems, would then have to recount every one of those, all the way down to the grains. A cluster of a thousand galaxies would recount every galaxy, and therefore every star, every planet and every grain, again. Each level up would carry the full weight of every level below it, and the work would compound with every step. Cosmic closure would never finish. Worse, there would be no level at which the description becomes simpler, so there would be no sense in which one rule applies at every scale: each scale would be tangled up in all of the ones beneath it.

You cannot have cosmic-wide closure if closing means re-accounting for everything.

So the requirement is this:

> **For cosmic-scale closure to work, a larger system must be able to close over already-closed smaller systems without reopening their internal gravitational accounting.**

Otherwise, every larger closure would require recalculating every constituent mass, and the framework would never achieve genuine scale invariance.

## Newton's hint

Newton himself found the first way out, though he did not put it in these terms. He proved that a spherically symmetric body, one built of uniform concentric layers, pulls on things outside it exactly as if all its mass sat at a single point at its centre. You don't need to know how dense the core is or how the layers are arranged. From outside, the Earth's interior has been settled once, and no one outside ever needs to reopen it.

A large company works the same way. Head office does not audit every receipt from every branch. Each branch closes its own books and sends up its result. Head office works with those results, and the board works with head office's. Nobody reopens a branch's receipts, yet the totals come out right, because each result carries exactly what the level above needs.

Gravity Field Dynamics, or GFD, proposes that this is not a lucky property of spherical bodies or a convenience of accountants. It is how gravity is organised at every scale.

## The recursive closure principle

Picture the hierarchy from the top down:

```
Cosmic closure          processes the galaxies' boundary contributions
  Galaxy closure        processes the stellar systems' boundaries
    Stellar closure     processes the planets' boundaries
      Planetary closure internal mass distribution already resolved
```

An asteroid settles its own internal field and closes. To the solar system it is no longer a heap of rock but a single entry, a *pointer*: here is a closed object, here is what it presents at its boundary. The solar system closes in turn, and to the galaxy it is one pointer. The galaxy closes, and to its cluster it is one pointer. No level ever reaches down to redo the one below.

Written as a rule: if $\mathcal C(D)$ is the closed field description of a region $D$, and $\mathcal M$ joins two descriptions across their shared boundary, then

$$\mathcal C(D_1 \cup D_2) = \mathcal M\big(\mathcal C(D_1),\, \mathcal C(D_2)\big).$$

The decisive statement is that **closing over closures is equivalent to closing over their complete interiors**, without reprocessing those interiors, for everything that can be observed from outside. Call it GFD's recursive closure theorem. In its general form it is still a proposal; parts of it have now been proved, as described below.

The regions in that rule are not tidy, non-overlapping boxes. Closed fields overlap; they must, or neighbours could never read each other. What composition respects is *ownership*, not the absence of overlap. Two closed field objects may occupy overlapping regions while keeping distinct registered states, and the larger closure takes in each object's owned contribution exactly once. It neither merges their interiors nor counts their mass twice.

And the universality belongs to the process of closure, not necessarily to what goes on inside every object. A drainless star system and a galaxy with a drain at its centre may follow different internal field equations, while obeying the same requirement to settle, register and compose. For the drainless, Newtonian case an exact nested construction already exists. Extending it to drained fields is the next mathematical step.

What has to be passed up is not simply a mass. A lumpy comet, a pair of stars or a flattened star system cannot in general be replaced by one number at one point and still produce the right field outside. What a closed system must hand to the level above is its *boundary information*: the field on its boundary and the flux through it, and, more completely, how its boundary responds when the field outside changes. That is what lets a closed system stay closed even when it is not round, when tides pull on it, and when the law that governs the larger system is not Newton's.

Closing does not mean that an object stops responding to its surroundings. Its registered state stays coupled to the surrounding NET Field. As that field changes, the object's boundary response changes with it, and a new compatible state is established. What closure removes is not interaction. It removes the need for a larger system to reconstruct the object's internal matter whenever the field around it changes. That matters most where environments change: galaxy encounters, mergers, tidal stripping.

## Compositional scale invariance

This gives scale invariance a different meaning from the one physicists usually give it.

The usual meaning is that nothing changes under rescaling: zoom in or out and the system, and the laws governing it, look the same. GFD does not require that. A galaxy is not a scaled-up solar system, and the boundary of a closed system does not even grow in proportion to its host; the proofs find it grows as the two-thirds power. What GFD requires is operational: the same rule of local settlement, registration and composition applies at every level, and each level works only with the closed results of the level below. A galaxy need not resemble a solar system. Both must be able to close their own field and present a registered state to the system around them. The proofs call this property scale-universal; compositional scale invariance is the same idea seen from the level of the whole.

## The original idea: distributed field processing

This is where the newest mathematics connects with GFD's oldest architectural idea.

GFD was never meant to calculate gravity by having every mass interact directly with every other mass across the universe. From the start it described gravity as evaluated locally, with the field's structure scaling up through a mesh of interacting domains: a galaxy domain with its own local field and closure, stellar domains inside it with theirs, planetary domains inside those, and boundary information exchanged between them. The framework calls this *distributed field processing*.

Seen this way, the recent proofs in the GFD research repository are not separate results. Each one supplies a mechanism that the original principle needed:

- **Distributed processing** is the organising principle: local field domains form a scalable mesh.
- **The closure surface** says where a bound domain's internal description can be replaced by an exterior description.
- **The mountain-scale construction** says how the internal Newtonian part and the external constitutive response are separated.
- **The net-field rule** says which field enters GFD's constitutive law at each level.

For example, the solar system's detailed internal field never has to be subjected, piece by piece, to the galaxy's constitutive law. Its influence is communicated through its boundary, and the galaxy processes the resulting total field.

The distinction is between gravitational influence and gravitational accounting. Gravity's influence reaches across enormous distances: the Milky Way's pull shapes the outermost comets of our solar system, and our galaxy and Andromeda are falling toward each other across two and a half million light years. But a field can influence distant systems without every distant system having to reconstruct its source. Each object settles its own field, registers what its exterior needs to know, and stays coupled to the surrounding NET Field through that registration. The next level works with those registered contributions and establishes its own closure. The process repeats from asteroids to planets, star systems, galaxies and clusters, and at no level does the larger system reopen a smaller one's internal accounting. Influence travels through the field, from domain to domain across their boundaries; the processing stays local.

A deeper consequence follows. A framework like this may not need a universal rule for selecting a scale at all: no single smoothing length laid over the whole universe to decide where one kind of gravity ends and another begins. It needs a local rule for ownership and interfaces, saying how each domain contributes to the domain around it. Every domain applies the same local prescription to its own density and its own boundary information:

$$\mathcal F_i = \mathcal L\big(\rho_i,\ \Phi\big|_{\partial D_i},\ \nabla\Phi\big|_{\partial D_i}\big).$$

The framework becomes scale-recursive rather than dependent on a globally chosen scale.

## What has been shown

Several mathematical pieces of the proposal have now been derived. Their algebraic cores are checked in the Lean proof assistant, and the geometric and numerical claims around them are tested by computation. Together they support a recursive construction for drainless systems. They do not yet establish the full closure principle for arbitrary fields.

**Closing in stages gives the same answer as closing all at once.** The tool for closing a region is called *balayage*, French for sweeping: you sweep the mass inside a closed surface onto the surface itself, arranged so that the field outside is exactly unchanged. Newton's round planet is the simplest case. The key property is that sweeping nests. Sweep a planet onto its own boundary, then sweep that onto the star system's boundary, and you get exactly what you would have got by sweeping the planet straight onto the star system's boundary. In symbols, $B_k B_j = B_k$. The [mountain-scale proof](proofs/sst-mountain-scale/) proves this, and it is checked by machine in the Lean proof assistant. It is the requirement above, in mathematical form: the larger closure never reopens the smaller one, and the pointer is exact.

**What is passed up is boundary information.** The sweep keeps the whole arrangement of mass on the boundary, not just its total, and that reproduces the outside field exactly for any shape. There is a natural reason this, and nothing else, is what the outside receives. If a closed system settles its interior with the least field energy consistent with what it shows at its boundary, the result is precisely the sweep. That is the classical Dirichlet principle, put to new use, and the boundary information plays the part of what GFD's first paper calls the object's *registered state*. At leading order the interaction is organised through four channels: one timelike, the object's clock rate, and three spacelike, the three directions in which it falls. These are the four legs of GFD's tetrad, the four active ports of its geometry. Finer tidal and shape information stays encoded in the boundary state: the four ports organise the coupling, but they do not reduce an arbitrary boundary field to four numbers.

**The closure surface is set by the field, locally.** A [companion proof](proofs/closure-surface/) asks where a closed system's boundary lies. Picture the Sun on its orbit around the galaxy. Close in, the Sun's own pull dominates. Far out, the galaxy's tide, its tendency to stretch things apart, wins. In between, together with the effect of the orbit's turning, there are exactly two places where all the pulls cancel: one toward the galactic centre and one away from it. In the frame that turns with the orbit, these are stagnation points of the combined field. The surface through them is the boundary of the Sun's cell. (The calculation is for a near-circular orbit in a steady host, with the cell small compared with the galaxy.) No global scale is needed to find it; it comes from the Sun's own mass and the field immediately around it.

That surface does double duty. Defined purely from the field, it is also the surface matter inside can never leave unless it gains enough energy. In this steady model a planet or an inner comet stays in the Sun's cell for good; in a changing galaxy the cell itself changes, and that case is still to be worked out. Matter with more energy can snap to a neighbouring cell, through the openings that appear around the two stagnation points when its energy allows: they are the cell's doors. For the Sun, the cell reaches about 1.44 parsecs (about 4.7 light years) toward and away from the galactic centre, and about two-thirds of that along its orbit. It holds comets whose orbits are smaller than about 99,000 times the Earth–Sun distance, the scale usually quoted for the outer edge of the Oort cloud. Alpha Centauri, 1.34 parsecs away, sits in its own cell. The two cells overlap, so each reads the other's field, but neither owns the other.

**The surroundings hold each cell in place.** Turn off the galaxy's tide in the calculation and the balance points slide away to infinity: there is no boundary at all. A cell exists only because of the field around it. A water vortex does the same. A whirlpool in a still pond has no edge. Put it in a moving stream and a separating line appears between the water that circles with the vortex and the water that flows past. In GFD's picture the surrounding medium is the mesh of unbound field cells through which the bound ones, the matter, move, and that mesh is what anchors each bound cell.

## Why it matters

Galaxies spin faster at their edges than their visible matter can explain. GFD accounts for this with a constitutive law, a rule for how the field responds, that departs from Newton's when the pull becomes very weak. But the law must not act everywhere. If it acted on the Sun's own field, it would distort the planets' orbits in a way the Cassini spacecraft, tracked at Saturn for thirteen years, has ruled out. The 2026 analysis of Cassini's data measures that distortion, a tiny stretching of the solar system along the direction of the galactic field, as $(1.6 \pm 1.8) \times 10^{-27}$ per second squared: consistent with zero.

Recursive closure resolves this cleanly. Inside its cell the solar system has settled its own books, and its gravity is Newton's. The galaxy's law acts on the galaxy's field and sees the Sun only as boundary information more than a parsec away. One of the proofs shows that this produces no anomalous distortion of that kind inside the cell, at the order calculated and for an idealised spherical cell. What remains is the galaxy's ordinary tide and smaller environmental terms, about a thousand times below what Cassini can detect.

The cell's boundary is not invisible. The potential is continuous across it, but its slope changes there, where the Newtonian field inside meets the galaxy's response outside. In the mountain-scale proof this appears as a thin effective layer on the boundary, the share of the Sun's field that the galaxy's second chamber, TetB, takes up. It is not a force on the planets, which sit deep inside; it is part of the interface accounting, more than a parsec away. Its full relativistic matching conditions are still to be derived.

The same reasoning makes a prediction. Two stars orbiting each other thousands of times farther apart than the Earth and the Sun can still share one closed cell. If they do, GFD says their motion around each other is Newtonian, and the speed at which they would come apart has a sharp edge, calculable in advance from their masses, their separation and the galaxy's tide. Theories that strengthen gravity between such stars move that edge upward. Surveys of wide binary stars from the Gaia satellite are already being argued over on exactly this point.

## What is not yet shown

The strongest way to put the idea is this: *GFD proposes that gravitational fields are processed locally on a recursively structured mesh, with dynamically determined closure surfaces mediating the field description between scales.*

Parts of that are now proved. The rest is the work ahead, and it is worth being plain about it.

Closing in stages is proved exactly for systems whose interiors follow Newton's law, the ones GFD calls drainless: planets, star systems, star clusters, binaries. A galaxy is different. Its interior has a drain, a central throat through which its field flows, and the constitutive law acts inside its own accounting. A galaxy still closes, and to its cluster it is still a pointer, but exactly what boundary information it passes up, including what mass that information carries, has not been worked out. That is where the composition rule has to be shown to hold when the law is not Newton's.

What remains to be demonstrated is that the recursive construction follows from GFD's full nonlinear and relativistic field equations, not only from the Newtonian cases established so far. The deepest step is also still to come: showing that GFD's underlying geometry, the dual tetrad, guarantees that closure information is sufficient and composable, and that a closed system registers its state at the balance-point surface rather than this being assumed. The moment of snapping, when matter leaves one cell for the next, still has to be described as the discrete event it appears to be. And everything here is Newtonian gravity on a fixed slice of time; the relativistic version, with moving boundaries, is ahead.

If those steps hold, cosmic-scale closure follows recursively, without reopening the internal accounting of a single smaller system. And the pebble on the beach would be telling us something true: gravity does not recount the universe. It closes it, one domain at a time.

---

*The proofs referred to here are in the GFD research repository: the [mountain-scale proof](proofs/sst-mountain-scale/) (closing in stages, boundary information, the four channels, the Cassini quadrupole) and the [closure-surface proof](proofs/closure-surface/) (where a cell's boundary sits, its doors and its anchoring). Distributed field processing is introduced in [Einstein's TetA partition](EINSTEIN_TETA_PARTITION.md). For the larger story of why galaxies spin as they do, see [The Missing Mass](THE_MISSING_MASS.md).*
