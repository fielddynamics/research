"""Figure for tiled_cube_affine_connection.tex, drawn from the same exact geometry as the checks.
(a) One face of TetA (opposite v_1), pierced by the TetB corner -v_1 and cut into its four channels.
(b) The shared octahedron on the cube edge from v_2 to -v_1, with the four cubes that hold it, one along each leg.
Run: python3 make_figure.py   (writes tiled_cube_figure.png)
"""
import itertools
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

A = [s for s in itertools.product((1, -1), repeat=3) if s[0] * s[1] * s[2] == 1]   # TetA corners = the legs v_a
v1 = (1, 1, 1); v2, v3, v4 = [a for a in A if a != v1]
mid = lambda p, q: tuple((x + y) / 2 for x, y in zip(p, q))
add = lambda *us: tuple(sum(u[i] for u in us) for i in range(3))
sc = lambda e, u: tuple(e * x for x in u)
neg = lambda u: sc(-1, u)

CORE, CORNER, OCTA, TETB = "#4c72b0", "#dd8452", "#c9c9c9", "#c44e52"

def cube_edges(c, ax, **kw):
    for p, q in itertools.combinations(itertools.product((-1, 1), repeat=3), 2):
        if sum(a != b for a, b in zip(p, q)) == 1:
            P, Q = add(c, p), add(c, q)
            ax.plot(*zip(P, Q), **kw)

def tri(ax, pts, color, alpha=0.85):
    ax.add_collection3d(Poly3DCollection([pts], facecolor=color, edgecolor="k", linewidth=0.8, alpha=alpha))

def setup(ax, lim, elev, azim):
    ax.set_xlim(*lim); ax.set_ylim(*lim); ax.set_zlim(*lim)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=elev, azim=azim); ax.set_axis_off()

fig = plt.figure(figsize=(7.2, 3.6))

# (a) the four channels of one face
ax = fig.add_subplot(1, 2, 1, projection="3d")
cube_edges((0, 0, 0), ax, color="0.75", linewidth=0.6)
f = [v2, v3, v4]
core = [mid(p, q) for p, q in itertools.combinations(f, 2)]
tri(ax, core, CORE)
for p in f:
    tri(ax, [p] + [mid(p, q) for q in f if q != p], CORNER)
b = neg(v1)
for c in core:                                   # TetB's spike at -v_1 stands on the core
    ax.plot(*zip(b, c), color=TETB, linewidth=1.0, linestyle="--")
ax.scatter(*b, color=TETB, s=25)
ax.text(*add(b, (0.0, 0.0, 0.3)), r"$-v_1$ (TetB)", color=TETB, fontsize=8, ha="right")
for p, name in zip(f, (r"$v_2$", r"$v_3$", r"$v_4$")):
    ax.text(*add(p, sc(0.18, p)), name, fontsize=8)
ax.text2D(0.02, 0.95, "(a) one face of TetA: core + 3 corner channels", transform=ax.transAxes, fontsize=8)
setup(ax, (-1.3, 1.3), 8, -20)

# (b) the shared octahedron of corner channel mu = 2 and its four cubes
ax = fig.add_subplot(1, 2, 2, projection="3d")
e = mid(v2, neg(v1))                             # cube-edge midpoint (v_2 - v_1)/2
q, r = v3, v4
cubes = {r"$\nu=1$ (own)": (0, 0, 0), r"$\nu=2$": add(v2, neg(v1)),
         r"$\nu=3$": add(neg(v1), neg(q)), r"$\nu=4$": add(neg(v1), neg(r))}
for name, c in cubes.items():
    cube_edges(c, ax, color="0.7", linewidth=0.5)
    away = tuple(0 if i == 0 else 1.25 * (c[i] - e[i]) for i in range(3))      # push the label off the edge
    ax.text(*add(e, away), name, fontsize=7, ha="center")
octv = [tuple(e[i] + (d if i == k else 0) for i in range(3)) for k in range(3) for d in (1, -1)]
for t in itertools.combinations(octv, 3):
    if all(sum((x - y) ** 2 for x, y in zip(P, Q)) == 2 for P, Q in itertools.combinations(t, 2)):
        tri(ax, list(t), OCTA, alpha=0.35)
tri(ax, [v2, mid(v2, q), mid(v2, r)], CORNER, alpha=0.95)
ax.plot(*zip(v2, neg(v1)), color="k", linewidth=1.4)
ax.text(*add(v2, (0.1, 0.1, 0.15)), r"$v_2$", fontsize=8)
ax.text(*add(neg(v1), (0.1, 0.1, -0.35)), r"$-v_1$", color=TETB, fontsize=8)
ax.text2D(0.02, 0.95, "(b) a corner channel's octahedron, held by 4 cubes", transform=ax.transAxes, fontsize=8)
setup(ax, (-3.4, 1.6), 22, 40)

fig.tight_layout()
fig.savefig("tiled_cube_figure.png", dpi=220)
print("wrote tiled_cube_figure.png")
