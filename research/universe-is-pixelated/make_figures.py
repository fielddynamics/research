"""Figures for 'The Universe Is Pixelated'. Run: python make_figures.py"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

BLUE, ORANGE, GOLD, INK, MUTED = "#2a78d6", "#eb6834", "#eda100", "#1f1f1e", "#8a8984"
pc = lambda v: bin(v).count("1")
# Paper IX convention: bit = 1 -> +1, bit = 0 -> -1; address bits (x, y, z)
def coord(v): return np.array([1 if (v >> (2 - i)) & 1 else -1 for i in range(3)], float)
A = [v for v in range(8) if pc(v) % 2 == 1]   # TetA {1,2,4,7}
B = [v for v in range(8) if pc(v) % 2 == 0]   # TetB {0,3,5,6}

# ---------- Figure 1: stellated octahedron in the cube ----------
fig = plt.figure(figsize=(7, 7)); ax = fig.add_subplot(111, projection="3d")
for a in range(8):
    for b in range(a + 1, 8):
        if pc(a ^ b) == 1:
            p, q = coord(a), coord(b); ax.plot(*zip(p, q), color=MUTED, lw=1.0)
def tet_faces(vs):
    P = [coord(v) for v in vs]
    return [[P[i] for i in range(4) if i != k] for k in range(4)]
for vs, col in ((A, BLUE), (B, ORANGE)):
    ax.add_collection3d(Poly3DCollection(tet_faces(vs), facecolor=col, edgecolor="white", lw=1.2, alpha=0.28))
octa = [np.array(v, float) for v in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]]
of = []
for sx in (1,-1):
    for sy in (1,-1):
        for sz in (1,-1):
            of.append([np.array([sx,0,0.]), np.array([0,sy,0.]), np.array([0,0,sz*1.])])
ax.add_collection3d(Poly3DCollection(of, facecolor=GOLD, edgecolor=GOLD, lw=0.6, alpha=0.55))
for i,p in enumerate(octa):
    for q in octa[i+1:]:
        if abs(p@q) < 1e-9: ax.plot(*zip(p, q), color="#b07800", lw=1.6, zorder=10)
for v in range(8):
    p = coord(v) * 1.13
    ax.text(*p, format(v, "03b"), color=BLUE if v in A else ORANGE, fontsize=12, ha="center", va="center", weight="bold",
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85), zorder=20)
ax.set_box_aspect((1,1,1)); ax.set_axis_off(); ax.view_init(elev=22, azim=-58)
ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2); ax.set_zlim(-1.2,1.2)
fig.text(0.5, 0.06, "Odd-parity corners (blue) form TetA; even-parity corners (orange) form TetB.\nTheir overlap is the octahedron (gold), whose six vertices sit at the cube's face centres.",
         ha="center", fontsize=10, color=INK)
fig.savefig("stellated_octahedron_in_cube.png", dpi=160, bbox_inches="tight", facecolor="white"); plt.close(fig)

# ---------- Figure 2: the cube's Walsh-Hadamard spectrum ----------
H = np.array([[(-1) ** pc(a & x) for x in range(8)] for a in range(8)])
order = [0, 1, 2, 4, 3, 5, 6, 7]          # rows sorted by grade (number of 1s)
fig, ax = plt.subplots(figsize=(8.6, 6.4))
for r, a in enumerate(order):
    for c in range(8):
        val = H[a, c]
        ax.add_patch(plt.Rectangle((c, 7 - r), 0.94, 0.94, color=INK if val > 0 else "#f1f0ec"))
for c in range(8):
    ax.text(c + 0.47, 8.25, format(c, "03b"), ha="center", fontsize=10, color=BLUE if c in A else ORANGE, weight="bold")
ax.text(4, 8.85, "cube corner (input address)", ha="center", fontsize=10, color=INK)
eig = {0: 3, 1: 1, 2: -1, 3: -3}
for r, a in enumerate(order):
    col = BLUE if a in A else ORANGE
    ax.text(-0.2, 7 - r + 0.47, f"w{format(a,'03b')}", ha="right", va="center", fontsize=10, color=col, weight="bold")
    ax.text(8.25, 7 - r + 0.47, f"grade {pc(a)}   eigenvalue {eig[pc(a)]:+d}", va="center", fontsize=9.5, color=INK)
ax.add_patch(plt.Rectangle((-0.04, -0.04), 8.02, 1.02, fill=False, ec=GOLD, lw=2.5))
ax.text(4, -0.55, "Bottom row w111 = (-1)^(x+y+z): +1 on TetB, -1 on TetA. The parity function is the stellated octahedron.",
        ha="center", fontsize=9.5, color=INK)
ax.set_xlim(-1.6, 12.6); ax.set_ylim(-0.9, 9.2); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("The eight Walsh functions of the cube (dark = +1, light = -1)", fontsize=12, color=INK, pad=4)
fig.savefig("cube_walsh_spectrum.png", dpi=160, bbox_inches="tight", facecolor="white"); plt.close(fig)
print("written")
