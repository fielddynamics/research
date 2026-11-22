# Closure of Closures

*How can gravity close a universe without recounting every grain of sand in it? Gravity Field Dynamics proposes that nature keeps its books the way a well-run organisation does: locally, once, and by reference.*

**Stephen Nelson** · Field Dynamics Research

---

## The problem: you cannot recount the universe

Stand on a beach and drop a pebble. It falls because the Earth pulls on it. But strictly, according to Newton, the pebble is pulled by everything: the sand beneath your feet, the mountains on the horizon, the Moon, the Sun, the hundred billion stars of the Milky Way, every galaxy out to the edge of what we can see. To work out the force on that one pebble, Newton's law says you should add up the pull of every particle in the universe, one at a time. There are roughly $10^{80}$ of them.

Now ask a bigger question. Not what pulls on one pebble, but how the universe as a whole settles its gravity: how every system, from an asteroid to a supercluster of galaxies, comes to a consistent field. Call that cosmic-scale closure.

Here is the problem. Suppose that each time a larger system closed, it had to reopen everything inside it.

A star system would have to recount every planet, every moon, every asteroid and every grain of rock in them. A galaxy, closing over its hundred billion star systems, would then have to recount every one of those, all the way down to the grains. A cluster of a thousand galaxies would recount every galaxy, and therefore every star, every planet and every grain, again. Each level up would carry the full weight of every level below it, and the work would compound with every step. Cosmic closure would never finish. Worse, there would be no level at which the description becomes simpler, so there would be no sense in which one rule applies at every scale: each scale would be tangled up in all of the ones beneath it.

You cannot have cosmic-wide closure if closing means re-accounting for everything.

So the requirement is this:

> **For cosmic-scale closure to work, a larger system must be able to close over already-closed smaller systems without reopening their internal gravitational accounting.**

Otherwise, every larger closure would require recalculating every constituent mass, and the framework would never achieve genuine scale invariance.

## Newton's hint

Newton himself found the first way out, though he did not put it in these terms. He proved that a round planet pulls on things outside it exactly as if all its mass sat at a single point at its centre. You don't need to know where the mountains are, or how dense the core is. From outside, the Earth's interior has been settled once, and no one outside ever needs to reopen it.

A large company works the same way. Head office does not audit every receipt from every branch. Each branch closes its own books and sends up its result. Head office works with those results, and the board works with head office's. Nobody reopens a branch's receipts, yet the totals come out right, because each result carries exactly what the level above needs.

Gravity Field Dynamics, or GFD, proposes that this is not a lucky property of spheres or a convenience of accountants. It is how gravity is organised at every scale.

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

What has to be passed up is not simply a mass. A lumpy comet, a pair of stars or a flattened star system cannot in general be replaced by one number at one point and still produce the right field outside. What a closed system must hand to the level above is its *boundary information*: the field on its boundary and the flux through it, and, more completely, how its boundary responds when the field outside changes. That is what lets a closed system stay closed even when it is not round, when tides pull on it, and when the law that governs the larger system is not Newton's.

## A stronger kind of scale invariance

This gives scale invariance a stronger meaning than physicists usually give it.

The usual meaning is that the same equations hold at different distances. The meaning here is compositional: the same physical rules apply at every level, and each level works only with the closed results of the level below. A galaxy is not a scaled-up solar system, and a cluster is not a scaled-up galaxy. What is the same at every level is the rule that closes them, and the fact that each closure can be built from closures without reopening them.

There is also an important distinction between influence and processing. Gravity's influence reaches across enormous distances. The Milky Way's pull shapes the outermost comets of our solar system, and our galaxy and Andromeda are falling toward each other across two and a half million light years. But long-range influence does not require all-to-all processing. The influence travels through the field, from domain to domain across their boundaries. The processing stays local to each domain and its interfaces.

## The original idea: distributed field processing

This is where the newest mathematics connects with GFD's oldest architectural idea.

GFD was never meant to calculate gravity by having every mass interact directly with every other mass across the universe. From the start it described gravity as evaluated locally, with the field's structure scaling up through a mesh of interacting domains: a galaxy domain with its own local field and closure, stellar domains inside it with theirs, planetary domains inside those, and boundary information exchanged between them. The framework calls this *distributed field processing*.

Seen this way, the recent proofs in the GFD research repository are not separate results. Each one supplies a mechanism that the original principle needed:

- **Distributed processing** is the organising principle: local field domains form a scalable mesh.
- **The closure surface** says where a bound domain's internal description can be replaced by an exterior description.
- **The mountain-scale construction** says how the internal Newtonian part and the external constitutive response are separated.
- **The net-field rule** says which field enters GFD's constitutive law at each level.

For example, the solar system's detailed internal field never has to be subjected, piece by piece, to the galaxy's constitutive law. Its influence is communicated through its boundary, and the galaxy processes the resulting total field.

A deeper consequence follows. A framework like this may not need a universal rule for selecting a scale at all: no single smoothing length laid over the whole universe to decide where one kind of gravity ends and another begins. It needs a local rule for ownership and interfaces, saying how each domain contributes to the domain around it. Every domain applies the same local prescription to its own density and its own boundary information:

$$\mathcal F_i = \mathcal L\big(\rho_i,\ \Phi\big|_{\partial D_i},\ \nabla\Phi\big|_{\partial D_i}\big).$$

The framework becomes scale-recursive rather than dependent on a globally chosen scale.

## What has been shown

Four pieces of this are now mathematics rather than intention.

**Closing in stages gives the same answer as closing all at once.** The tool for closing a region is called *balayage*, French for sweeping: you sweep the mass inside a closed surface onto the surface itself, arranged so that the field outside is exactly unchanged. Newton's round planet is the simplest case. The key property is that sweeping nests. Sweep a planet onto its own boundary, then sweep that onto the star system's boundary, and you get exactly what you would have got by sweeping the planet straight onto the star system's boundary. In symbols, $B_k B_j = B_k$. The [mountain-scale proof](proofs/sst-mountain-scale/) proves this, and it is checked by machine in the Lean proof assistant. It is the requirement above, in mathematical form: the larger closure never reopens the smaller one, and the pointer is exact.

**What is passed up is boundary information.** The sweep keeps the whole arrangement of mass on the boundary, not just its total, and that reproduces the outside field exactly for any shape. There is a natural reason this, and nothing else, is what the outside receives. If a closed system settles its interior with the least field energy consistent with what it shows at its boundary, the result is precisely the sweep. That is the classical Dirichlet principle, put to new use, and the boundary information plays the part of what GFD's first paper calls the object's *registered state*. At leading order the neighbours read it through just four channels: one timelike, the object's clock rate, and three spacelike, the three directions in which it falls. These are the four legs of GFD's tetrad, the four active ports of its geometry.

**The closure surface is set by the field, locally.** A [companion proof](proofs/closure-surface/) asks where a closed system's boundary lies. Picture the Sun on its orbit around the galaxy. Close in, the Sun's own pull dominates. Far out, the galaxy's tide, its tendency to stretch things apart, wins. In between, together with the effect of the orbit's turning, there are exactly two places where all the pulls cancel: one toward the galactic centre and one away from it. The surface through those two balance points is the boundary of the Sun's cell. No global scale is needed to find it; it comes from the Sun's own mass and the field immediately around it.

That surface does double duty. Defined purely from the field, it is also the surface matter inside can never leave unless it gains enough energy. A planet or an inner comet stays in the Sun's cell for good. Matter with more energy can snap to a neighbouring cell, and only through the two balance points: they are the cell's doors. For the Sun, the cell reaches about 1.44 parsecs (about 4.7 light years) toward and away from the galactic centre, and about two-thirds of that along its orbit. It holds comets whose orbits are smaller than about 99,000 times the Earth–Sun distance, the scale usually quoted for the outer edge of the Oort cloud. Alpha Centauri, 1.34 parsecs away, sits in its own cell. The two cells overlap, so each reads the other's field, but neither owns the other.

**The surroundings hold each cell in place.** Turn off the galaxy's tide in the calculation and the balance points slide away to infinity: there is no boundary at all. A cell exists only because of the field around it. A water vortex does the same. A whirlpool in a still pond has no edge. Put it in a moving stream and a separating line appears between the water that circles with the vortex and the water that flows past. In GFD's picture the surrounding medium is the mesh of unbound field cells through which the bound ones, the matter, move, and that mesh is what anchors each bound cell.

## Why it matters

Galaxies spin faster at their edges than their visible matter can explain. GFD accounts for this with a constitutive law, a rule for how the field responds, that departs from Newton's when the pull becomes very weak. But the law must not act everywhere. If it acted on the Sun's own field, it would distort the planets' orbits in a way the Cassini spacecraft, tracked at Saturn for thirteen years, has ruled out. The 2026 analysis of Cassini's data measures that distortion, a tiny stretching of the solar system along the direction of the galactic field, as $(1.6 \pm 1.8) \times 10^{-27}$ per second squared: consistent with zero.

Recursive closure resolves this cleanly. Inside its cell the solar system has settled its own books, and its gravity is Newton's. The galaxy's law acts on the galaxy's field and sees the Sun only as boundary information more than a parsec away. One of the proofs shows that this leaves no distortion at all inside the cell. What remains is the galaxy's ordinary tide, about a thousand times below what Cassini can detect.

The same reasoning makes a prediction. Two stars orbiting each other thousands of times farther apart than the Earth and the Sun can still share one closed cell. If they do, GFD says their motion around each other is Newtonian, and the speed at which they would come apart has a sharp edge, calculable in advance from their masses, their separation and the galaxy's tide. Theories that strengthen gravity between such stars move that edge upward. Surveys of wide binary stars from the Gaia satellite are already being argued over on exactly this point.

## What is not yet shown

The strongest way to put the idea is this: *GFD proposes that gravitational fields are processed locally on a recursively structured mesh, with dynamically determined closure surfaces mediating the field description between scales.*

Parts of that are now proved. The rest is the work ahead, and it is worth being plain about it.

Closing in stages is proved exactly for systems whose interiors follow Newton's law, the ones GFD calls drainless: planets, star systems, star clusters, binaries. A galaxy is different. Its interior has a drain, a central throat through which its field flows, and the constitutive law acts inside its own accounting. A galaxy still closes, and to its cluster it is still a pointer, but exactly what boundary information it passes up, including what mass that information carries, has not been worked out. That is where the composition rule has to be shown to hold when the law is not Newton's.

The deepest step is also still to come: showing that GFD's underlying geometry, the dual tetrad, guarantees that closure information is sufficient and composable, and that a closed system registers its state at the balance-point surface rather than this being assumed. The moment of snapping, when matter leaves one cell for the next, still has to be described as the discrete event it appears to be. And everything here is Newtonian gravity on a fixed slice of time; the relativistic version, with moving boundaries, is ahead.

If those steps hold, cosmic-scale closure follows recursively, without reopening the internal accounting of a single smaller system. And the pebble on the beach would be telling us something true: gravity does not recount the universe. It closes it, one domain at a time.

---

*The proofs referred to here are in the GFD research repository: the [mountain-scale proof](proofs/sst-mountain-scale/) (closing in stages, boundary information, the four channels, the Cassini quadrupole) and the [closure-surface proof](proofs/closure-surface/) (where a cell's boundary sits, its doors and its anchoring). Distributed field processing is introduced in [Einstein's TetA partition](EINSTEIN_TETA_PARTITION.md). For the larger story of why galaxies spin as they do, see [The Missing Mass](THE_MISSING_MASS.md).*
