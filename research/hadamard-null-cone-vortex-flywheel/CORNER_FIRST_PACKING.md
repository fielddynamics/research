# Corner-first packing: the exact tetrahedral contact bound

> **Integration update.** The [unified synthesis](UNIFIED_HADAMARD_FIELD_DYNAMICS.md) relaxes rigid sphere tangency in an explicit overlapping diamond model, without changing the theorem below or treating the twelve second neighbours as eight.

**Status:** [T] geometric theorem under rigid, congruent, non-overlapping sphere assumptions; [E] application to GFD. This supersedes the interpretation that the four prescribed FCC links are aligned with the four regular Hadamard corner directions. It does not invalidate the FCC graph construction.

![Four active corner contacts and the four remaining contact regions](figures/23_corner_first_packing.svg)

## 1. Geometry first

One complete stellated octahedron is one field. Use cube corners $s_i\in\{(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)\}$ and unit vectors $n_i=s_i/\sqrt3$. The central sphere has radius $R=\sqrt3$ in cube coordinates. Equal-radius neighbours at $2s_i$ touch at $s_i$. The four directions satisfy

$$\sum_i n_i=0,\qquad \sum_i n_i n_i^T=\tfrac43 I,\qquad n_i\cdot n_j=-\tfrac13\quad(i\ne j).$$

## 2. Exact upper bound on additional equal-sphere contacts

Rescale the central radius to one. Any additional equal touching sphere has centre $2u$ with $\|u\|=1$. Non-overlap with each fixed neighbour requires $\|2u-2n_i\|\ge2$, equivalently $t_i=u\cdot n_i\le1/2$. Tight-frame closure implies $\sum_i t_i=0$ and $\sum_i t_i^2=4/3$.

Write $m=-\min_i t_i$. Necessarily $1/2<m\le1$: otherwise all four absolute values are at most $1/2$, contradicting their squared sum. Consider the compact polytope $\sum_i t_i=0$, $-m\le t_i\le1/2$. The convex squared norm reaches its maximum at a vertex. Every vertex has at least three coordinates at endpoints. For $1/2<m\le1$, three upper endpoints are impossible (the fourth would be $-3/2$), two lower endpoints are impossible (the other two sum to at most one), and three lower endpoints are impossible. The only vertex pattern, up to permutation, is

$$(-m,\tfrac12,\tfrac12,m-1).$$

It follows that $4/3\le m^2+1/2+(m-1)^2$, hence

$$m\ge m_* = \frac{1+\sqrt{2/3}}2\approx0.90824829.$$

Every additional direction therefore lies in one of four spherical caps centred at $-n_i$, with angular radius $\theta_*=\arccos m_*\approx24.74^\circ$. Two directions in the same cap are separated by at most $2\theta_*<60^\circ$ (since $m_*>\sqrt3/2$). Two equal touching neighbours need separation at least $60^\circ$. At most one additional sphere fits in each cap. The cap centres themselves provide a feasible configuration: the eight cube corners have minimum angular separation $\arccos(1/3)>60^\circ$.

**Theorem:** With four prescribed regular tetrahedral contacts, the maximum number of congruent, rigid, non-overlapping touching neighbours is exactly eight. The bound on cap radius is sharp: the vertex pattern above lies in the tight-frame image and reconstructs a unit vector $u=\frac34\sum_i t_i n_i$. This theorem is local and does not assume FCC, HCP, or global periodicity.

## 3. Consequences for the 12/4/8 hypothesis

- Eight exact equal contacts: four active corners and four complementary inactive contacts are geometrically possible. Activity itself remains a coupling premise.
- Twelve equal tangent contacts are possible in FCC, but no four form a regular tetrahedron (normalized pairwise dot products are in $\{-1,-1/2,0,1/2\}$). The earlier FCC graph result permits four links but not exact normal alignment.
- A diamond network gives four equal nearest neighbours exactly at tetrahedral directions and twelve *second* neighbours; these twelve are not tangent contacts.
- If spherical envelopes represent overlapping field closures rather than rigid material spheres, the non-overlap premise need not apply. One must define the neighbour relation independently (shared interface, overlap, or registered adjacency). If spheres differ in radius, the equal-radius theorem also need not apply. Neither option is proof of a 12/4/8 physical selection rule.

The eight internal vortices remain eight internal constituents of **each** field, not eight surrounding fields. Do not identify the external count with the internal face count.

## 4. Next research target

Derive external neighbour adjacency and transmission from field closure, rather than assuming the kissing number is the communication degree. If 12/4/8 is retained, identify explicitly which geometric assumption changes. Preserve $K=4$ as the internal regular tetrahedral frame and require reciprocity and conservation at the selected external interfaces. The result does not establish nuclear capture, the constitutive law, or the full SST action.

## Reproduction

`python verify_corner_first.py` checks the exact tight-frame algebra, polytope vertex bound, cap threshold and attaining construction. `python generate_corner_first_figure.py` regenerates the diagram. See [verification log](corner_first_verification_output.txt).
