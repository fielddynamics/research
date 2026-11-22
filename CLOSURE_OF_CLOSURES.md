# Closure of Closures

*How can gravity add up a universe without counting every grain of sand? Gravity Field Dynamics proposes that nature keeps its books the way a well-run organisation does: locally, once, and by reference.*

**Stephen Nelson** · Field Dynamics Research

---

Stand on a beach and drop a pebble. It falls because the Earth pulls on it. But strictly, according to Newton, the pebble is pulled by everything: the sand beneath your feet, the mountains on the horizon, the Moon, the Sun, the stars of the Milky Way, every galaxy out to the edge of what we can see. To work out the force on that one pebble, Newton's law says you should add up the pull of every particle in the universe, one at a time. There are roughly $10^{80}$ of them.

Nobody does that, of course. And, more interestingly, nature doesn't seem to either.

Newton himself found the first shortcut. He proved that a round planet pulls on things outside it exactly as if all its mass sat at a single point at its centre. You don't need to know where the mountains are, or how dense the core is. From outside, the whole Earth can be replaced by one number, its mass, at one place, its centre. The interior is *closed*: its details have been settled once and need never be reopened by anyone outside.

That small theorem hides a big idea. What if it is not a lucky property of spheres but the way gravity is organised at every scale?

## The bookkeeping problem

Consider a galaxy like our own. It holds something like a hundred billion stars. Most have planets, the planets have moons, and around them swarm asteroids and comets, each made of countless grains. If the galaxy's gravity had to account for every one of those pieces individually, the bookkeeping would be astronomical in the most literal sense.

A large company faces the same problem. Head office does not audit every receipt from every branch. Each branch closes its own books and sends up a summary. Head office works with the summaries, and the board works with head office's summary. Nobody reopens the branches' receipts, yet the totals come out right, because each summary carries exactly what the level above needs to know.

Gravity Field Dynamics, or GFD, proposes that gravity works like this. An asteroid settles its own internal field and closes. To the solar system it is no longer a heap of rock but a single entry, a *pointer*: here is a closed object, this is its mass, this is where it is. The solar system closes in turn, and to the galaxy it becomes one pointer. The galaxy closes, and to its cluster of galaxies it is one pointer.

```
Cosmic structure    works with the galaxies' summaries
  Galaxy            works with the star systems' summaries
    Star system     works with the planets' summaries
      Planet        internal mass already settled
```

At each level the same local rule does the work, and no level ever reaches down to redo the one below. GFD has always called this *distributed field processing*: the field is evaluated locally, in a mesh of domains that each settle their own accounts and talk to their neighbours only through their boundaries.

## Why it has to be this way

This is more than a convenience. It is a requirement.

If a larger closure had to reopen its members' internal accounts, then every time you went up a level you would have to recompute everything below it. A galaxy would have to re-derive every planet's interior; a cluster would have to re-derive every galaxy's. There would be no level at which the description simplifies, and no sense in which the same law applies at every scale, because each scale would be tangled up in all the ones beneath it.

So the idea can be written as a composition rule. If $\mathcal C(D)$ stands for the closed description of a region $D$, what its boundary tells the outside world, then closing two regions together should be the same as combining their closed descriptions:

$$\mathcal C(D_1 \cup D_2) = \mathcal M\big(\mathcal C(D_1),\, \mathcal C(D_2)\big).$$

Here $\mathcal M$ joins the descriptions across their shared boundary. Closure of closures equals closure of the whole, without reopening the interiors.

That is a strong kind of scale symmetry. It does not say every level looks the same; a star system and a galaxy have very different sizes, and the boundary of a closed system grows as the two-thirds power of its host's size, not in proportion. It says every level *follows the same rule*. The proofs call this being scale-universal. You might call it compositional.

In its general form, that composition rule is a proposal, not yet a theorem. But over the past weeks a series of proofs in the GFD research repository has turned several of its pieces into mathematics.

## What has been shown

**Closing in stages gives the same answer as closing all at once.** The mathematical tool for "closing" a region has a name, *balayage*, French for sweeping. You take the mass inside a closed surface and sweep it onto the surface itself, arranged so that the field outside is exactly unchanged. Newton's round planet is the simplest case: sweep the Earth onto its own surface and, from outside, nothing changes.

The key property is that sweeping nests. Sweep a planet onto its own boundary, then sweep that onto the star system's boundary, and you get exactly what you would have got by sweeping the planet straight onto the star system's boundary. In symbols, $B_k B_j = B_k$. This was proved in the [mountain-scale proof](proofs/sst-mountain-scale/) and checked by machine in the Lean proof assistant. It is the bookkeeping rule in mathematical form: a closed system's summary is all the level above ever needs, and the pointer is exact.

**The summary is a boundary record, not just a number.** Real objects are not perfect spheres. A comet is lumpy, a binary star is two bodies, a star system is a flattened swirl. A single mass at a single point is not, in general, enough to reproduce their outside field. The sweep keeps more: the whole arrangement of mass on the boundary. That record reproduces the outside field exactly, for any shape.

There is a natural way to see why this record, and nothing else, is what the outside world receives. If a closed system settles its interior with the least field energy consistent with what it shows at its boundary, the result is precisely the sweep. That is the classical Dirichlet principle, put to new use, and the boundary record plays the part of what GFD's first paper calls the object's *registered state*.

And at leading order the neighbours read that record through just four channels. A closed system meets the field around it through one timelike channel, its clock rate, and three spacelike ones, the three directions in which it falls. These are the four legs of GFD's tetrad, the four active ports of its geometry.

**Where the boundary sits.** A [companion proof](proofs/closure-surface/) asks where a closed system's surface actually lies. Picture the Sun on its orbit around the galaxy. Close in, the Sun's own pull dominates. Far out, the galaxy's tide, its tendency to stretch things apart, wins. In between, together with the effect of the orbit's turning, there are exactly two places where all the pulls cancel: two balance points, one toward the galactic centre and one away from it. The surface through those points is the boundary of the Sun's cell.

That surface does double duty. Defined purely from the field, it is also the surface that matter inside can never leave unless it gains enough energy. A planet or an inner comet stays in the Sun's cell for good. Matter with more energy can snap to a neighbouring cell, and the calculation shows it can only do so through the two balance points: they are the cell's doors.

For the Sun, the cell stretches about 1.44 parsecs (about 4.7 light years) toward and away from the galactic centre and about two-thirds of that along its orbit. Comets with orbits smaller than about 99,000 times the Earth–Sun distance are held for good, which is the scale astronomers usually quote for the outer edge of the Oort cloud. Alpha Centauri, 1.34 parsecs away, sits in its own cell. The two cells overlap, so each reads the other's field, but neither owns the other.

**The surroundings hold each cell in place.** Here is a detail that is easy to miss. Turn off the galaxy's tide in the calculation and the balance points slide away to infinity: there is no boundary at all. A cell exists only because of the field around it. A water vortex does the same. A whirlpool sitting in a still pond has no edge. Put it in a moving stream and a separating line appears, the boundary between the water that circles with the vortex and the water that flows past. In GFD's picture the surrounding medium is the mesh of unbound field cells through which the bound ones, the matter, move, and that mesh is what anchors each bound cell.

## Why it matters

The payoff is practical as well as conceptual, because it tells you where gravity's unusual behaviour should and should not appear.

Galaxies spin faster at their edges than their visible matter can explain. GFD accounts for this with a constitutive law, a rule for how the field responds that departs from Newton's when the pull becomes very weak. But that law must not act everywhere. If it acted on the Sun's own field, it would distort the orbits of the planets in a way the Cassini spacecraft, tracked at Saturn for thirteen years, has ruled out. The 2026 analysis of Cassini's data measures that distortion, a tiny stretching of the solar system along the direction of the galactic field, as $(1.6 \pm 1.8) \times 10^{-27}$ per second squared: consistent with zero.

Closure resolves the tension cleanly. Inside its cell the solar system has settled its own books: its gravity is Newton's, exactly. The galaxy's law acts on the galaxy's field, and it sees the Sun only as a summary on a boundary more than a parsec away. One of the proofs shows that this summary leaves no distortion at all inside the cell, even though the galaxy's field responds differently in different directions. What remains is the galaxy's ordinary tide, about a thousand times below what Cassini can detect.

The same reasoning makes a prediction that can be tested. Two stars orbiting each other widely, thousands of times farther apart than the Earth and Sun, can still lie well inside a shared cell. If they do, GFD says their motion around each other is Newtonian, and the speed at which they come apart has a sharp edge that can be calculated in advance from their masses, their separation and the galaxy's tide. Theories that strengthen gravity between such stars move that edge upward. Surveys of wide binaries from the Gaia satellite are already being argued over on exactly this point.

## What is not yet shown

It would be easy to overstate this, so let me be plain about the gaps.

The general composition rule above is still a proposal. What is proved is narrower. Closing in stages is exact for systems whose interiors follow Newton's law, the ones GFD calls drainless: planets, star systems, star clusters, binaries. A galaxy is different. Its interior has a drain, a central throat through which its field flows, and the constitutive law acts *inside* its accounting. A galaxy still closes, and to its cluster it is still a pointer, but exactly how its summary is composed, and even what mass that summary carries, has not been worked out.

Nor has the deepest step been taken: showing that GFD's underlying geometry, the dual tetrad, *requires* that a closed system registers its state at that balance-point surface, rather than this being assumed. The moment of snapping, when a piece of matter leaves one cell for the next, still has to be described as the discrete event it appears to be. And everything here is at the level of Newtonian gravity on a fixed slice of time; the full relativistic version, with surfaces that move, is still to come.

Those are the next problems. But the direction is clear. GFD was never meant to compute gravity by having every mass in the universe pull on every other mass, one pair at a time. It was meant to work the way the pebble on the beach suggests nature does: locally, once, and by reference. The new proofs suggest that this is not just a way of organising a calculation. It may be how gravity organises itself.

---

*The proofs referred to here are in the GFD research repository: the [mountain-scale proof](proofs/sst-mountain-scale/) (closing in stages, the boundary record, the four channels, the Cassini quadrupole) and the [closure-surface proof](proofs/closure-surface/) (where a cell's boundary sits, its doors and its anchoring). The idea of distributed field processing is introduced in [Einstein's TetA partition](EINSTEIN_TETA_PARTITION.md). For the larger story of why galaxies spin as they do, see [The Missing Mass](THE_MISSING_MASS.md).*
