# From General Relativity to the Coupling Polynomial

## A Complete Derivation Chain in Nine Steps

**Stephen Nelson — Gravity Field Dynamics**

---

## Introduction

This document derives the gravitational coupling polynomial f(K, s) = 1 + Ks + K² from a single empirical input: that general relativity operates in 3+1 spacetime. The derivation proceeds in nine steps. Each step is either a theorem of mathematics, a geometric identity, or a direct reading of an equation already present in the standard literature. No free parameters are introduced at any step.

---

## Step 0 — The Starting Point

General relativity operates in 3+1 spacetime: three dimensions of space, one of time.

This is the single empirical input. It is not derived here. It is observed. Every measurement, every experiment, every human experience takes place in this arena. General relativity itself does not explain why — the Einstein field equations work in any number of dimensions. String theory entertains ten or eleven. The equations do not care.

We take 3+1 as given, and we ask: what follows?

What follows is derived entirely from this single observation. No additional physical input is introduced at any later step.

---

## Step 1 — The Simplex Theorem

The simplex theorem is pure geometry, known since antiquity and formalised long before Einstein.

In one dimension, you need two points to bracket an interval. In two dimensions, you need three points to enclose an area — that is a triangle. In three dimensions, you need four points (not lying in a plane) to enclose a volume — that is a tetrahedron. You cannot do it with fewer. Three points in three-dimensional space give you a flat triangle with no interior volume. It takes four to fence off a region. This is because four is the minimum number of points in three-dimensional space that do not all lie in a single plane — the necessary condition for enclosing volume.

The general statement is the **simplex theorem**: in *d* spatial dimensions, the minimum number of boundary faces required to enclose a region is *d* + 1.

For our three-dimensional space:

> **K = d + 1 = 3 + 1 = 4**

It is the geometric minimum for closure in three dimensions — the minimum needed to create an inside and an outside, the way a soap bubble must close completely to hold volume. Four faces. That is a tetrahedron.

---

## Step 2 — Independent Confirmation from General Relativity

Before moving on, it is worth pausing to notice that this number — four — appears independently across every major formalism in gravitational physics. Different research groups, working in different decades, for different purposes, all arrive at the same structural constant.

In the **ADM formalism**, there are four constraint equations: one Hamiltonian (energy) constraint and three momentum constraints. In **tetrad gravity**, there are four orthonormal basis vectors spanning the tangent space at each point. In **Loop Quantum Gravity**, the quantum tetrahedron has four faces. In **Regge calculus**, the fundamental building block is the 3-simplex, which has four vertices. In the **LIGO observation**, the two detected polarisation modes are consistent with 10 − 2K gravitational degrees of freedom, giving K = 4.

Five independent lines of physics. One number. The simplex theorem explains why: four is the minimum for three-dimensional closure, and every formalism that describes gravity in three spatial dimensions inherits this minimum.

None of these confirmations are required for what follows — the simplex theorem alone fixes K = 4. They are noted here because the convergence across independent formalisms is itself remarkable, and because it would be strange to proceed past so striking a pattern without acknowledging it.

---

## Step 3 — The Uniqueness Equation

Could the universe have had two spatial dimensions? Five? Eleven? Is three arbitrary, or is it forced?

To answer this, we need to connect the simplex from Step 1 to the coordinate structure of *d*-dimensional space. The coordinate cell in *d* dimensions is the hypercube, with 2^*d* vertices — one for each binary string of length *d*, representing every possible combination of "low" and "high" along each axis. Step 1 established that closure in *d*-dimensional space requires a simplex with *d* + 1 vertices. A single simplex cannot account for all the hypercube's vertices, since *d* + 1 < 2^*d* for all *d* ≥ 2. The minimum number of simplices that could partition the hypercube is therefore two — one for each orientation of the frame, just as a gravitational wave carries two polarisation modes. These are the two **polarisation simplices**. That two are sufficient is proved constructively in Step 4, which exhibits the partition. Two simplices contribute 2(*d* + 1) vertices. The hypercube provides 2^*d*. For the partition to be exact — every vertex assigned to one simplex or the other, with none left over and none missing — the equation is:

> **2(d + 1) = 2^d**

This equation has a direct physical meaning. It is the condition that the two polarisation simplices *completely tile* the coordinate space. If 2(*d* + 1) < 2^*d*, the two simplices cannot reach all the vertices of the coordinate cell — there are directions that neither polarisation can access. The geometry has gaps. If 2(*d* + 1) > 2^*d*, the simplices require more vertices than the coordinate cell provides — there is no consistent embedding. The geometry overflows. Only when 2(*d* + 1) = 2^*d* do the two polarisation simplices fill the coordinate cell exactly, with every direction accounted for and nothing wasted.

Now check it, dimension by dimension.

At *d* = 1: the left side gives 4, the right side gives 2. More simplex vertices than cube vertices. No fit.
At *d* = 2: left gives 6, right gives 4. Still too many. No fit.
At *d* = 3: left gives 8, right gives 8. **Exact match.**
At *d* = 4: left gives 10, right gives 16. Too few simplex vertices. No fit.
At *d* = 5: left gives 12, right gives 32. The gap only widens.

The left side grows linearly. The right side grows exponentially. They meet exactly once, at *d* = 3, and never again. It is an exact integer equation with a unique positive solution.

This single equation fixes both structural constants simultaneously:

> **D = 3** gives the spatial dimensions.
> **K = D + 1 = 4** gives the frame dimension.

Three is the unique number of spatial dimensions in which two polarisation simplices exactly partition the coordinate cell. In any other dimension, the geometry either has gaps or overflows. Only in three dimensions does everything fit.

---

## Step 4 — The Partition

At *d* = 3, the vertex counts match perfectly: 2(3 + 1) = 8 = 2³.

What does this mean geometrically? A cube in three dimensions has eight vertices. Each vertex can be labelled by a binary string of length three — its coordinates are either 0 or 1 along each axis. That gives eight labels: 000, 001, 010, 011, 100, 101, 110, 111.

Now partition these eight vertices by **binary parity**: count the number of 1s in each label. Vertices with an odd number of 1s go into one group; vertices with an even number go into the other.

Odd parity (odd popcount): 001, 010, 100, 111 — four vertices.
Even parity (even popcount): 000, 011, 101, 110 — four vertices.

Each group of four vertices, when connected, forms a **regular tetrahedron**. This is the unique partition of the cube's eight vertices into two groups of four that preserves the full symmetry of the cube. There are C(8,4) = 70 ways to split eight vertices into two groups of four, but only this one — the parity partition — produces two *regular* tetrahedra. All others yield irregular configurations that break the cube's rotational symmetry. No vertices are left over. None are shared. The assignment is completely determined by the binary encoding of the cube.

The two tetrahedra carry opposite spatial orientations — the parity map that defines them is spatial inversion through the centre of the cube. This is intrinsic to the binary partition, not an additional assumption.

Two tetrahedra. Eight vertices. One cube. Everything accounted for.

---

## Step 5 — The Structure

Two regular tetrahedra sharing all eight vertices of a cube and interlocking by parity form one geometric object: the **stellated octahedron** (also known as the stella octangula).

It is the unique geometry that realises the partition from Step 4. If you accept the cube, the binary labelling, and the parity partition — all of which are forced — then the stellated octahedron is the only structure that results.

Its combinatorial content, its *f*-vector, is:

> **8 vertices, 12 edges, 8 triangular faces**

(The total geometric element count of 8 + 12 + 8 = 28 becomes significant in other branches of the framework, but the present derivation depends only on the face type, not the total count. We note it here for completeness and move on.)

---

## Step 6 — The Face Type

The stellated octahedron inherits its faces from the tetrahedra that compose it. A tetrahedron is the 3-simplex. Its boundary consists of 2-simplices — that is, **triangles**. This is not a property specific to the stellated octahedron; it is a property of the simplex. The boundary of a *d*-simplex is always made of (*d* − 1)-simplices, and for *d* = 3, that means triangles.

Every face of the stellated octahedron is an equilateral triangle. No other face type is possible. A tetrahedron cannot have a square face for the same reason a triangle cannot have four vertices — it would require an additional vertex, producing a different simplex entirely. The triangular face is forced by the simplex structure of the tetrahedra from which the stellated octahedron is composed.

This matters enormously for what comes next, because the internal structure of the face determines the internal structure of the coupling.

---

## Step 7 — The Simplex Hierarchy of the Face

A triangle is the 2-simplex. Like every simplex, it has a hierarchy of boundary elements, running from dimension zero up to the dimension of the simplex itself. For the triangle, this hierarchy has exactly three levels:

**Level 0 — the 0-simplex: vertices.** A triangle has 3 vertices. These are points — zero-dimensional objects. They carry position but no extension.

**Level 1 — the 1-simplex: edges.** A triangle has 3 edges. These are line segments — one-dimensional objects. Each connects two vertices.

**Level 2 — the 2-simplex: the face itself.** The triangle has 1 face. This is the enclosed area — the two-dimensional object that all three vertices jointly define.

Three hierarchical levels: 0, 1, 2. It follows from the fact that the face is two-dimensional, and the simplex hierarchy runs from dimension 0 to dimension *d_face* = 2. That gives exactly *d_face* + 1 = 3 levels. There is no level 3, because there is no three-dimensional cell on the boundary of a three-dimensional object — the boundary is, by definition, one dimension lower than the interior. Any algebraic structure indexed by this hierarchy has exactly three levels to draw on — and no more.

(As an aside that becomes important in later work: this three-level structure is the same reason the Sierpiński triangle has three surviving sub-triangles at every iteration. Each sub-triangle is addressed by proximity to one of three vertices. The fourth central sub-triangle, the one removed, belongs to no vertex. Three vertices, three sub-triangles, three hierarchical levels. The number three is the vertex count of a triangle, which is the face type of a tetrahedron, which is the closure simplex in three spatial dimensions.)

---

## Step 8 — The Tetrad Equation Already Contains This Structure

Steps 1 through 7 established the geometry: the closure simplex is the tetrahedron, its faces are triangles, and each triangular face has a three-level simplex hierarchy. The next link in the chain is to show that this same three-level structure is already present — and has always been present — in the standard equation of tetrad gravity.

The equation appears in every textbook on the subject: Misner, Thorne and Wheeler (1973), Carroll (2004), Rovelli (2004). It is:

> **g_μν = η_ab e^a_μ e^b_ν**

It says the metric of spacetime is built from three ingredients. Let us examine each one — not its components (every relativist counts components), but its **structural type**. What kind of mathematical object is it? Specifically, what is its **rank** on the local frame space — the four-dimensional space indexed by the frame index *a*?

This is a different question from the standard one. When physicists ask "how many independent components does g_μν have?", the answer is ten — a symmetric 4×4 matrix. That is correct. But it is the answer to a question about degrees of freedom. The question here is about **rank-dimension**: for a tensor of rank *r* on a frame space of dimension K, the rank-dimension is K^*r*. It counts how many frame-direction combinations the object must be defined on — the size of the template itself, before any values are assigned. It does not depend on which entries happen to be zero or which symmetries have been imposed. A 4×4 matrix has rank-dimension 16 whether it is the identity matrix, the zero matrix, or the Minkowski metric — the template is the same in all three cases.

Now scan the ranks.

**Rank 0: The closure condition — det(e) ≠ 0.** A rank-0 object on frame space is a scalar: a single number with no free frame index. The tetrad must be non-degenerate — it must actually span the tangent space. This is the condition that the geometry *holds*, that the field *closes* rather than collapses into degeneracy. It is a single binary structural requirement.

A reader may object: "But det(e) is computed *from* e^a_μ — it is not a separate ingredient." The objection is natural, but consider a soap bubble. The closure of the film — the condition that it forms a bounded surface enclosing volume — is not a separate material added to the soap. It is produced by the film. Yet a soap film that does not close is a fundamentally different object: an open surface, not a bubble. Closure is structurally independent of the film's local properties in the precise sense that you can specify the film everywhere and still fail to have closure. The same is true here. One can write down a tetrad e^a_μ with all sixteen components specified and still have det(e) = 0 at a point. At that point the frame does not span the tangent space, the metric degenerates, and the equation g_μν = η_ab e^a_μ e^b_ν describes no geometry. The closure condition is not external to the equation — the left-hand side g_μν is a non-degenerate metric only when det(e) ≠ 0. It is the precondition for the equation to mean what it says. It contributes one structural element. In the tetrad formulation of the Einstein-Hilbert action, this condition appears explicitly: the Lagrangian is prefactored by e = det(e^a_μ), the scalar volume measure — a rank-0 object by construction.

> **Rank-dimension: K⁰ = 1.**

**Rank 1: The frame — e^a_μ.** A rank-1 object on frame space is a vector: one free frame index *a*, running over K values. The tetrad assigns a spacetime one-form to each of the K = 4 frame directions: one timelike leg and three spacelike legs. This is the frame — the set of directions that the local geometry provides.

> **Rank-dimension: K¹ = K = 4.**

**Rank 2: The coupling template — η_ab.** A rank-2 object on frame space is a matrix: two free frame indices *a* and *b*, each running over K values. The contraction η_ab e^a_μ e^b_ν evaluates one term for every ordered pair (*a*, *b*). There are K × K = 16 such pairs.

This is where the standard component count and the rank-dimension count diverge. The flat Minkowski metric η_ab assigns ±1 to the four diagonal pairs and zero to the twelve off-diagonal pairs. The twelve zeros are assignments of zero weight, not missing pairings — a Euclidean metric would assign +1 across the same sixteen slots, and a different signature would distribute the values differently. What is structurally invariant is the template: K × K frame-direction pairings that the coupling must be defined on.

> **Rank-dimension: K² = 16.**

The scan terminates at rank 2. No rank-3 object appears in g_μν = η_ab e^a_μ e^b_ν, in the tetrad action, or in the field equations of any metric or bimetric gravity theory. A rank-3 coupling would require three simultaneous free frame indices at each coupling event — a three-dimensional cell on the two-dimensional boundary of the tetrahedron. No such cell exists. The equation closes at rank 2, and the polynomial closes with it.

Now sum the occupied ranks by rank-dimension:

> **K⁰ + K¹ + K² = 1 + 4 + 16 = 21**

Three structural types. A scalar constraint, a vector frame, and a tensor coupling template. They scale as K⁰, K¹, and K². This sum is the total dimension of the graded tensor algebra ⊕_{r=0}^{2} V^{(r)} on the K-dimensional frame space — a standard construction in algebra and topology.

Now recall the simplex hierarchy from Step 7. The triangular face of the tetrahedron has three levels of boundary element: vertices (0-simplices), edges (1-simplices), and the face itself (2-simplex). Three levels, scaling as dimensions 0, 1, and 2.

The correspondence is exact. And it cannot be otherwise, because the tetrad *is* the simplex — that is what Steps 1 through 6 established. Here is the logical chain stated in plain sequence: the tetrad is the 3-simplex (Step 1). Its faces are triangles (Step 6). The simplex hierarchy of a triangle has three levels (Step 7). The tetrad equation has three structural types. The former is the geometric *reason* for the latter — not by analogy, but because the equation *describes* the simplex. They are the same object in two languages: one algebraic, one geometric.

The polynomial was written down in 1928, when Einstein introduced the tetrad formalism. It has been sitting inside the standard equation of tetrad gravity for a century. What was not previously noticed is that counting structural *types* rather than independent *components* yields the coupling polynomial directly.

---

## Step 9 — The Coupling Polynomial

Three terms. Three simplex levels. Three structural types in the tetrad equation. Each weighted by K raised to its rank-dimension. All that remains is to ask: how does a coupling variable enter, and where?

The two tetrahedra established in Steps 4 and 5 — TetA and TetB — carry opposite spatial orientations. That is what the binary parity partition means geometrically: the two tetrahedra are related by spatial inversion. If one is "right-handed," the other is "left-handed." Any coupling between them must therefore account for how each structural type transforms under spatial orientation reversal.

This is standard representation theory, the same classification used throughout quantum field theory to distinguish scalars from pseudoscalars and vectors from pseudovectors. Each tensor rank transforms according to its parity under spatial inversion:

**Rank 0 (scalar, K⁰ = 1):** A scalar has no spatial direction. It is invariant under orientation reversal. The closure condition — the field either holds or it does not — is the same regardless of which sector you observe from. It carries no sign change.

**Rank 1 (vector, K¹ = K):** A vector carries one spatial index. Under spatial orientation reversal, it picks up a factor of −1. The frame directions in TetB point oppositely to those in TetA. This is the only term that *distinguishes* one sector from the other.

**Rank 2 (tensor, K² = K²):** A rank-2 tensor carries two spatial indices. Under orientation reversal, each index contributes a sign flip, and (−1) × (−1) = +1. The coupling template is even under parity — it looks the same from both sectors.

Introduce a state parameter *s* that tracks the spatial orientation: *s* = +1 in the primary sector (TetA), *s* = −1 in the dual sector (TetB), and *s* = 0 at the point where both sectors meet and spatial extent collapses to zero. At this point the two frames point in opposite directions and cancel: the vector contribution vanishes, leaving only the orientation-independent terms — the scalar closure condition and the tensor coupling template. The value *s* = 0 is not a third parity eigenvalue — parity remains a two-state symmetry. It is the polynomial evaluated at the contact point where the parity-odd sector is absent; evaluating a polynomial at zero requires no additional justification. By the transformation rules just established, *s* can only appear on the rank-1 term — it is the only parity-odd term in the polynomial. The rank-0 and rank-2 terms are parity-even and therefore invariant. This is forced by the tensor character of each rank.

The polynomial is:

> ### **f(K, s) = 1 + Ks + K²**

At the unique value K = 4, in its three structural states:

> **f(4, +1) = 1 + 4 + 16 = 21** — the primary sector, full coupling.
> **f(4, 0) = 1 + 0 + 16 = 17** — the field origin, contact coupling.
> **f(4, −1) = 1 − 4 + 16 = 13** — the dual sector, reversed orientation.

These three integers are not independent. For any polynomial of the form 1 + Ks + K², evaluating at *s* = +1, 0, and −1 always produces three equally spaced values with spacing K. The middle value is the arithmetic mean of the outer two:

> **(21 + 13) / 2 = 17**

This is an algebraic identity. The three values form a single rigid object. Adjusting any one of them requires adjusting all three, because they are not three separate numbers — they are one polynomial evaluated at three points. If the field origin value were 18 instead of 17, the equal spacing would break, the primary-sector value 1 + K + K² would cease to equal the finite geometric series (K³ − 1)/(K − 1) for K = 4, and the connection between the polynomial and the dimension of space D = 3 would be severed.

There are zero free parameters remaining. The polynomial, the value of K, the placement of *s*, and the three evaluation integers are all determined by the chain.

---

## The Complete Chain

For reference, here is the full derivation compressed to a single logical sequence. Every arrow represents a theorem or geometric identity.

> **3+1 observation** → simplex theorem (K = d + 1 = 4)
> → uniqueness equation (d = 3 is the only solution to 2(d + 1) = 2^d)
> → binary parity partition (8 = 8, two groups of four, unique symmetric split)
> → stellated octahedron (unique realisation of the partition)
> → triangular faces (simplex inheritance from the tetrahedron)
> → three simplex levels per face (0-simplex, 1-simplex, 2-simplex)
> → three structural types in the tetrad equation (scalar, vector, tensor → K⁰, K¹, K²)
> → parity classification fixes *s* to the rank-1 term only
> → **f(K, s) = 1 + Ks + K²**

Nine steps. Zero free parameters. The polynomial is the terminal output. The stellated octahedron is the structure that forces it. The coupling variable *s* is locked to the single parity-odd rank by representation theory. The three evaluation integers 21, 17, and 13 are locked to each other by the arithmetic mean identity.

---

## What This Means

The coupling polynomial is the structural content of the tetrad equation, expressed in the language of the geometry that the tetrad equation describes. Each step in the derivation is either observational fact (Step 0), classical geometry (Steps 1, 4, 5, 6, 7), combinatorics (Step 3), pattern recognition across established physics (Step 2), a direct reading of a standard equation in general relativity (Step 8), or standard representation theory (Step 9).

No step depends on anything beyond what the previous step provides. No step introduces a free parameter. No step requires the reader to accept an unproven physical assumption. The chain runs from a single observed fact — three spatial dimensions — through nine forced links to a unique polynomial. Everything in between is mathematics.

The polynomial was always there. It was written in 1928 as g_μν = η_ab e^a_μ e^b_ν. It took a century to read it as 1 + K + K².

---

*Gravity Field Dynamics — docs.fielddynamics.org*
*Stephen Nelson*
