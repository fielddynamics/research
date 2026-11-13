"""Figure 1 for 'The Null Directions of the Tetrad Frame Carry a Complete Boolean Basis'. Run: python make_figure.py"""
import itertools, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

BLUE, ORANGE, GOLD, INK, MUTED, GREY, GREEN, RED = "#2F7FD3", "#D2552B", "#C9962B", "#1b1f24", "#6b7280", "#e9ecef", "#1D9E75", "#C0392B"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "mathtext.fontset": "dejavusans"})
fig = plt.figure(figsize=(7.2, 8.6), dpi=300); fig.patch.set_facecolor("white")
pc = lambda x: bin(x).count("1")

# ---------------- (a) eight null directions = eight 3-bit words
fig.text(0.02, 0.985, "(a)  Eight null directions, eight 3-bit words", fontsize=10.5, weight="bold", color=INK, va="top")
ax = fig.add_axes([0.0, 0.60, 0.46, 0.37], projection="3d")
C = np.array(list(itertools.product((1, -1), repeat=3)))
TA = [c for c in C if np.prod(c) == 1]; TB = [c for c in C if np.prod(c) == -1]
def tet(V, col):
    faces = [[V[i] for i in f] for f in itertools.combinations(range(4), 3)]
    ax.add_collection3d(Poly3DCollection(faces, facecolor=col, alpha=0.16, edgecolor=col, linewidths=0.9))
tet(TA, BLUE); tet(TB, ORANGE)
for e in itertools.combinations(range(8), 2):
    a, b = C[e[0]], C[e[1]]
    if np.sum(a != b) == 1: ax.plot(*zip(a, b), color="#b8c0ca", lw=0.5)
for c in C:
    col = BLUE if np.prod(c) == 1 else ORANGE
    ax.plot([0, c[0]], [0, c[1]], [0, c[2]], color=col, lw=1.0, ls=(0, (2, 1.5)))
    ax.scatter(*c, color=col, s=16, depthshade=False)
    word = "".join(str((1 - x) // 2) for x in c)
    ax.text(*(1.22 * c), word, fontsize=7.5, color=col, ha="center", va="center", weight="bold")
ax.scatter([0], [0], [0], color=GOLD, s=14)
ax.view_init(elev=18, azim=-55); ax.set_box_aspect((1, 1, 1)); ax.axis("off")
fig.text(0.47, 0.935, "Letter 1: four isotropic directions on the sky\n"
         "are a regular tetrahedron. TetA (blue) and its\n"
         "antipode TetB (orange) are the eight points of\n"
         "the star, and each $k=(1,\\,v/\\sqrt{3})$ is a light ray.\n\n"
         "The signs of $v$ are three bits, so the eight null\n"
         "directions are the eight words $000,\\dots,111$, and\n"
         "TetA/TetB is their parity (even/odd).\n\n"
         "Functions on the eight directions $=$ the 256\n"
         "three-input Boolean functions.", fontsize=7.9, color=INK, va="top", linespacing=1.42)

# ---------------- (b) the 16 two-input gates on and off the null cone
fig.text(0.02, 0.585, "(b)  Two-input gates as 4-vectors: which are light rays?", fontsize=10.5, weight="bold", color=INK, va="top")
bx = fig.add_axes([0.02, 0.29, 0.96, 0.28]); bx.set_xlim(0, 100); bx.set_ylim(0, 36); bx.axis("off")
gates = [("AND", 0b1000, "real"), ("NOR", 0b0001, "real"), ("TRUE", 0b1111, "real"), ("FALSE", 0b0000, "zero"),
         ("a", 0b1100, "cx"), ("b", 0b1010, "cx"), ("NOT a", 0b0011, "cx"), ("NOT b", 0b0101, "cx"),
         ("a·¬b", 0b0100, "cx"), ("¬a·b", 0b0010, "cx"),
         ("XOR", 0b0110, "off"), ("XNOR", 0b1001, "off"), ("OR", 0b1110, "off"), ("NAND", 0b0111, "off"),
         ("a→b", 0b1011, "off"), ("b→a", 0b1101, "off")]
def tt(x0, y0, code, kind, name, c=2.6):
    X = [[code & 1, (code >> 1) & 1], [(code >> 2) & 1, (code >> 3) & 1]]     # X[a][b] = f(a, b): rows a = 0 (top), 1; cols b = 0, 1
    col = {"real": BLUE, "zero": MUTED, "cx": "#7FA8D9", "off": ORANGE}[kind]
    for i in range(2):
        for j in range(2):
            v = X[i][j]
            bx.add_patch(Rectangle((x0 + j * c, y0 + (1 - i) * c), 0.92 * c, 0.92 * c, fc=col if v else GREY, ec="none", alpha=1 if v else 1))
    bx.text(x0 + c, y0 - 1.3, name, ha="center", va="top", fontsize=7.2, color=INK)
# legend of the cell convention
bx.text(0.5, 35, "Truth table $X_{ab}=f(a,b)$ as a 2×2 matrix: $\\det X = t^2-x^2-y^2-z^2$ in the spinor reading.", fontsize=7.8, color=MUTED, va="top")
# null group box
bx.add_patch(FancyBboxPatch((0.5, 4.2), 62.5, 26.3, boxstyle="round,pad=0.3,rounding_size=1.2", fc="#f3f7fc", ec=BLUE, lw=0.9))
bx.text(1.8, 29.2, "On the null cone, $\\det X=0$: the 10 separable gates $f=g(a)\\,h(b)$", fontsize=8.4, color=BLUE, weight="bold", va="top")
xs = [3 + 6.1 * i for i in range(10)]
for (nm, code, kind), x in zip(gates[:10], xs):
    tt(x, 17.5, code, kind, nm)
bx.text(1.8, 12.6, "Dark blue: real light rays (AND along $-z$, NOR along $+z$, TRUE along $+x$).", fontsize=7.0, color=INK, va="top")
bx.text(1.8, 10.0, "Light blue: complex null vectors (real only in split signature). Grey: zero.", fontsize=7.0, color=INK, va="top")
bx.text(1.8, 7.2, "Universal: AND and NOT are null gates, and NOR alone gives all 256.", fontsize=7.4, color=GREEN, weight="bold", va="top")
# off-cone group
bx.add_patch(FancyBboxPatch((65.5, 4.2), 34, 26.3, boxstyle="round,pad=0.3,rounding_size=1.2", fc="#fdf4f0", ec=ORANGE, lw=0.9))
bx.text(66.8, 29.2, "Off the cone, $\\det X=\\pm1$: 6 gates", fontsize=8.4, color=ORANGE, weight="bold", va="top")
for (nm, code, kind), x in zip(gates[10:], [68 + 5.4 * i for i in range(6)]):
    tt(x, 17.5, code, kind, nm, c=2.3)
bx.text(66.8, 12.6, "Parity (XOR, XNOR), the TetA/TetB", fontsize=7.0, color=INK, va="top")
bx.text(66.8, 10.0, "split, lies off the cone.", fontsize=7.0, color=INK, va="top")
bx.text(66.8, 7.2, "Parity gates reach only 16 of 256.", fontsize=7.4, color=RED, weight="bold", va="top")

# ---------------- (c) H8 = S D S^T
fig.text(0.02, 0.27, "(c)  The Walsh read of the eight directions = AND table × π twist × AND table", fontsize=10.5, weight="bold", color=INK, va="top")
cx = fig.add_axes([0.02, 0.005, 0.96, 0.25]); cx.set_xlim(0, 100); cx.set_ylim(0, 30); cx.axis("off")
H = np.array([[(-1) ** pc(i & j) for j in range(8)] for i in range(8)])
S = np.array([[1 if (j & ~i) == 0 else 0 for j in range(8)] for i in range(8)])
Dg = np.diag([(-2) ** pc(x) for x in range(8)])
def grid(M, x0, y0, c, kind):
    for i in range(8):
        for j in range(8):
            v = M[i, j]; x, y = x0 + j * c, y0 + (7 - i) * c
            if v == 0: fc, a = GREY, 1
            elif kind == "S": fc, a = BLUE, (1 if i == j else 0.45)
            else: fc, a = (BLUE if v > 0 else ORANGE), min(1, 0.4 + 0.08 * abs(v))
            cx.add_patch(Rectangle((x, y), 0.9 * c, 0.9 * c, fc=fc, alpha=a, ec="none"))
c = 1.75; y0 = 7.5
grid(H, 1, y0, c, "H"); cx.text(1 + 4 * c, y0 + 8 * c + 1.0, "$H_8$", ha="center", fontsize=9.5, weight="bold", color=INK)
cx.text(1 + 4 * c, y0 - 1.0, "XOR table: the Walsh\ncharacters $(-1)^{|i\\wedge j|}$", ha="center", va="top", fontsize=7.2, color=MUTED)
cx.text(17.3, y0 + 4 * c, "=", fontsize=15, color=MUTED, ha="center", va="center")
grid(S, 19.5, y0, c, "S"); cx.text(19.5 + 4 * c, y0 + 8 * c + 1.0, "$S$", ha="center", fontsize=9.5, weight="bold", color=INK)
cx.text(19.5 + 4 * c, y0 - 1.0, "AND table: monomials\n$1,x,y,z,xy,\\dots,xyz$", ha="center", va="top", fontsize=7.2, color=MUTED)
cx.text(35.8, y0 + 4 * c, "×", fontsize=13, color=MUTED, ha="center", va="center")
grid(Dg, 38, y0, c, "D"); cx.text(38 + 4 * c, y0 + 8 * c + 1.0, "$(-2)^{|x|}$", ha="center", fontsize=9.5, weight="bold", color=INK)
cx.text(38 + 4 * c, y0 - 1.0, "$e^{(\\ln 2+i\\pi)|x|}$:\nthe $\\pi$ twist", ha="center", va="top", fontsize=7.2, color=MUTED)
cx.text(54.3, y0 + 4 * c, "×", fontsize=13, color=MUTED, ha="center", va="center")
grid(S.T, 56.5, y0, c, "S"); cx.text(56.5 + 4 * c, y0 + 8 * c + 1.0, "$S^{T}$", ha="center", fontsize=9.5, weight="bold", color=INK)
cx.text(56.5 + 4 * c, y0 - 1.0, "AND table\ntransposed", ha="center", va="top", fontsize=7.2, color=MUTED)
tx = 74.5
cx.text(tx, 26, "Gates generated", fontsize=9, weight="bold", color=INK)
for k_, (lab, val, col) in enumerate([("parity: XOR, NOT, 0, 1", "16", RED), ("AND, XOR, 1", "256", GREEN),
                                      ("AND, NOT (null gates)", "256", GREEN), ("NOR alone (a light ray)", "256", GREEN)]):
    y = 22 - 4.2 * k_
    cx.text(tx, y, lab, fontsize=7.6, color=INK); cx.text(tx + 25, y, val, fontsize=9, color=col, weight="bold", ha="right")
cx.text(tx, 5.2, "$S^2=I$ over GF(2): each function\nis a unique XOR of ANDs.", fontsize=7.2, color=MUTED, va="top")
fig.savefig("null_cone_boolean_figure.png", dpi=300, facecolor="white")
print("saved")
