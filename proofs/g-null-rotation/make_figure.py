"""Figure for 'G's Graded Operator Is a Null Rotation'. Run: python make_figure.py  (needs numpy, matplotlib)"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

GREEN, BLUE, ORANGE, INK, MUTED, POS, NEG = "#1D9E75", "#2F7FD3", "#D2552B", "#1b1f24", "#6b7280", "#2F7FD3", "#D2552B"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "mathtext.fontset": "dejavusans"})

def kron_pow(M, n):
    R = np.eye(1)
    for _ in range(n): R = np.kron(R, M)
    return R
A = np.array([[1, 0], [1, 1]])
S = [kron_pow(A, m) for m in (0, 2, 4)]

fig = plt.figure(figsize=(7.2, 9.2), dpi=300)
fig.patch.set_facecolor("white")

# ---------------- (a) the three Sierpinski blocks
ax = fig.add_axes([0.02, 0.555, 0.96, 0.435]); ax.set_xlim(0, 100); ax.set_ylim(0, 60); ax.axis("off")
ax.text(0, 59, "(a)  G's graded operator: three Sierpiński blocks", fontsize=10.5, weight="bold", color=INK, va="top")
ax.text(0, 55.2, "Light cells: Pascal's triangle mod 2, $S=e^{L}$.  Dark cells: the diagonal, the only part the trace, and so G, reads.",
        fontsize=7.8, color=MUTED, va="top")
def draw_block(M, x0, y0, cell, col, label, sub):
    n = M.shape[0]
    ax.add_patch(Rectangle((x0 - 0.6, y0 - 0.6), n * cell + 1.2, n * cell + 1.2, fill=False, ec=col, lw=1.1, ls=(0, (3, 2))))
    for i in range(n):
        for j in range(n):
            x, y = x0 + j * cell, y0 + (n - 1 - i) * cell
            if i == j:   fc, a = col, 1.0
            elif M[i, j]: fc, a = col, 0.30
            else:        fc, a = "#e9ecef", 1.0
            ax.add_patch(Rectangle((x + 0.06 * cell, y + 0.06 * cell), 0.88 * cell, 0.88 * cell, fc=fc, alpha=a, ec="none"))
    ax.text(x0 + n * cell / 2, y0 + n * cell + 1.6, label, ha="center", fontsize=10, color=col, weight="bold")
    ax.text(x0 + n * cell / 2, y0 - 2.2, sub, ha="center", fontsize=7.6, color=INK, linespacing=1.35, va="top")
Y0 = 12
draw_block(S[0], 3.4, Y0, 2.6, GREEN, "$P_0$", "$1\\times1$\ntrace 1\nfilled 1")
ax.text(9.6, Y0 + 1.3, "+", fontsize=15, color=MUTED, ha="center", va="center")
draw_block(S[1], 13.5, Y0, 2.6, BLUE, "$s\\cdot P_1$", "$4\\times4$ (2 bits)\ntrace 4, filled $9=3^2$\nchains $3+1$")
ax.text(28.4, Y0 + 1.3, "+", fontsize=15, color=MUTED, ha="center", va="center")
draw_block(S[2], 32.5, Y0, 2.2, ORANGE, "$P_2$", "$16\\times16$ (4 bits)\ntrace 16, filled $81=3^4$\nchains $5+3+3+3+1+1$")
bx = 72.5
ax.text(bx, 47, "What G reads", fontsize=9.5, weight="bold", color=INK)
ax.text(bx, 43.2, "$\\mathrm{Tr}\\,(P_0+sP_1+P_2)=1+4s+16$", fontsize=8.6, color=INK)
rows = [("TetA", "$s=+1$", "21", BLUE), ("Field Origin", "$s=0$", "17", INK), ("TetB", "$s=-1$", "13", ORANGE)]
for k, (nm, sv, v, c) in enumerate(rows):
    y = 38.6 - 4.0 * k
    ax.text(bx, y, nm, fontsize=8.5, color=INK); ax.text(bx + 12.5, y, sv, fontsize=8.5, color=MUTED); ax.text(bx + 21, y, v, fontsize=9.5, weight="bold", color=c)
ax.text(bx, 25.0, "$\\det\\,\\alpha^{M}=\\alpha^{\\mathrm{Tr}\\,M}$", fontsize=9, color=INK)
ax.text(bx, 20.8, "$G=\\frac{17}{13}\\,\\alpha^{21}\\,\\hbar c/m_e^{2}$", fontsize=9.5, color=INK, weight="bold")
ax.text(bx, 15.6, "Trace (diagonal): $1+4+16=21$", fontsize=7.8, color=GREEN)
ax.text(bx, 12.2, "Area (all filled): $1+9+81=91$", fontsize=7.8, color=NEG)
ax.text(bx, 9.0, "would miss G by $\\alpha^{70}\\approx10^{-150}$", fontsize=7.8, color=NEG)

# ---------------- (b) Hadamard factorisation on the 4-block
bx_ = fig.add_axes([0.02, 0.305, 0.96, 0.24]); bx_.set_xlim(0, 100); bx_.set_ylim(0, 31); bx_.axis("off")
bx_.text(0, 30.5, "(b)  The Walsh–Hadamard read on the 4-block factors through the Sierpiński block", fontsize=10.5, weight="bold", color=INK, va="top")
H4 = kron_pow(np.array([[1, 1], [1, -1]]), 2)
Dg = np.diag([(-2) ** bin(x).count("1") for x in range(4)])
def mat(M, x0, y0, cell, title, sub, kind):
    n = M.shape[0]
    for i in range(n):
        for j in range(n):
            v = M[i, j]; x, y = x0 + j * cell, y0 + (n - 1 - i) * cell
            if v == 0: fc, a = "#eef0f2", 1
            elif kind == "S": fc, a = BLUE, (1.0 if i == j else 0.35)
            else: fc, a = (POS if v > 0 else NEG), min(1, 0.35 + 0.16 * abs(v))
            bx_.add_patch(Rectangle((x + 0.05 * cell, y + 0.05 * cell), 0.9 * cell, 0.9 * cell, fc=fc, alpha=a, ec="none"))
            if v != 0: bx_.text(x + cell / 2, y + cell / 2, f"{int(v):+d}" if kind != "S" else "1", ha="center", va="center", fontsize=6.6, color="white", weight="bold")
    bx_.text(x0 + n * cell / 2, y0 + n * cell + 1.3, title, ha="center", fontsize=9, color=INK, weight="bold")
    bx_.text(x0 + n * cell / 2, y0 - 1.3, sub, ha="center", va="top", fontsize=7.2, color=MUTED, linespacing=1.3)
c, Yb = 3.1, 8.5
mat(H4, 1.5, Yb, c, "$H_4$", "Walsh–Hadamard read\n= rotation of space by $\\pi$", "H")
bx_.text(17.3, Yb + 6.2, "=", fontsize=15, color=MUTED, ha="center", va="center")
mat(S[1], 20.5, Yb, c, "$S=e^{L}$", "Sierpiński block\n= null rotation", "S")
bx_.text(36.6, Yb + 6.2, "×", fontsize=13, color=MUTED, ha="center", va="center")
mat(Dg, 39.8, Yb, c, "$(-2)^{\\mathrm{popcount}}$", "boost of rapidity $\\ln 2$\nwith a $\\pi$ twist", "D")
bx_.text(55.9, Yb + 6.2, "×", fontsize=13, color=MUTED, ha="center", va="center")
mat(S[1].T, 59.1, Yb, c, "$S^{T}=e^{L^{T}}$", "Sierpiński transposed\n= reverse null rotation", "S")
bx_.text(78.5, 23, "Graded character", fontsize=9, weight="bold", color=INK)
bx_.text(78.5, 19.4, "$1+s\\,\\chi+\\chi^{2}$,  $\\chi=|\\mathrm{Tr}\\,A|^{2}$", fontsize=8.2, color=INK)
bx_.text(78.5, 15.4, "null rotation: $\\chi=4=K$", fontsize=8.2, color=BLUE)
bx_.text(78.5, 12.4, "$\\to$ 21, 17, 13", fontsize=8.2, color=BLUE)
bx_.text(78.5, 8.4, "$\\pi$-rotation $H_4$: $\\chi=0$", fontsize=8.2, color=NEG)
bx_.text(78.5, 5.4, "$\\to$ 1, 1, 1", fontsize=8.2, color=NEG)

# ---------------- (c) the null rotation on the light cone, (t, x, z) slice (y is left fixed)
fig.text(0.02, 0.29, "(c)  The Sierpiński block is a null rotation: it fixes one light ray", fontsize=10.5, weight="bold", color=INK, va="top")
cx = fig.add_axes([0.0, 0.0, 0.50, 0.28], projection="3d")
sig = [np.eye(2), np.array([[0, 1], [1, 0]]), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]])]
def Lam(M): return np.real(np.array([[0.5 * np.trace(sig[m] @ M @ sig[n] @ M.conj().T) for n in range(4)] for m in range(4)]))
At = lambda a: np.array([[1.0, 0], [a, 1.0]])
th = np.linspace(0, 2 * np.pi, 80); hh = np.linspace(0, 1.25, 10)
T, Hh = np.meshgrid(th, hh)
cx.plot_surface(Hh * np.cos(T), Hh * np.sin(T), Hh, color="#d6dee8", alpha=0.22, linewidth=0)
cx.plot_wireframe(Hh * np.cos(T), Hh * np.sin(T), Hh, color="#a7b3c1", linewidth=0.25, rstride=3, cstride=8)
cx.plot(np.cos(th), np.sin(th), np.ones_like(th), color=MUTED, lw=0.8)          # the light rays at t = 1
cx.plot([0, 0], [0, -1.25], [0, 1.25], color=BLUE, lw=2.8)                       # fixed ray k: x = 0, z = -t
cx.text(-0.15, -1.6, 1.05, "fixed ray $k$", fontsize=7.5, color=BLUE, ha="right")
cx.scatter([0], [-1], [1], color=BLUE, s=22, zorder=10)
for phi in np.deg2rad([-40, 10, 60, 110, 160, 210]):
    v = np.array([1, np.cos(phi), 0.0, np.sin(phi)])
    pts = np.array([Lam(At(a)) @ v for a in np.tan(np.linspace(0, 1.52, 120))])
    pts = pts / pts[:, :1]
    cx.plot(pts[:, 1], pts[:, 3], np.ones(len(pts)), color=ORANGE, lw=1.5, alpha=0.9)
    cx.scatter([pts[0, 1]], [pts[0, 3]], [1], color=ORANGE, s=9)
    m = 25
    d = pts[m + 1] - pts[m]
    cx.quiver(pts[m, 1], pts[m, 3], 1, d[1], d[3], 0, length=0.25, normalize=True, color=ORANGE, arrow_length_ratio=0.9, lw=1.4)
cx.view_init(elev=28, azim=-62); cx.set_box_aspect((1, 1, 0.85)); cx.axis("off")
fig.text(0.50, 0.255,
         "Draw a 4-vector as the 2×2 matrix $X=(x_{ij})$, the\n"
         "two bits of the 4-block being its two spinor indices.\n"
         "Then $\\det X = t^2-x^2-y^2-z^2$, and $|00\\rangle$, $|11\\rangle$ are null.\n\n"
         "The Sierpiński block acts as $X\\to AXA^{T}$ with\n"
         "$A=[[1,0],[1,1]]$: a Lorentz transformation. It fixes\n"
         "the light ray $k=|11\\rangle$ (blue) and slides every other\n"
         "light ray around the circle toward it (orange).\n\n"
         "The 16-block splits as $16 = 10 + 6$, with\n"
         "$10 = 5+3+1+1$ (a metric) and $6 = 3+3$ (a 2-form).",
         fontsize=7.8, color=INK, va="top", linespacing=1.45)
fig.savefig("g_null_rotation_figure.png", dpi=300, facecolor="white")
print("saved")
