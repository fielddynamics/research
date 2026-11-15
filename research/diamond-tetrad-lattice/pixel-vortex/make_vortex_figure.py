"""Figure for PROOF.md and ../triforce-vortex/PROOF.md: the pixel's vortices, drawn from the proofs' own models.

Every arrow is a bond current J_{i->j} = 2 Im(psi_j* H_ji psi_i), the physical flow from i to j under i dpsi/dt = H psi, of an actual vortex eigenstate:
 - panels a, b: the 15-site pixel of pixel-vortex/PROOF.md (Field Origin, octahedron, corners),
   a vortex about the octahedron axis z, at one parameter set with TetA != TetB;
 - panel c: the 33-tile Triforce model of triforce-vortex/PROOF.md, a vortex about the leg (1,1,1).
The models are built by running the setup parts of the two verification scripts, so the figure uses
exactly the Hamiltonians that were proved about.
Run: python make_vortex_figure.py   (writes vortex_figure.png here and in ../triforce-vortex/)
"""
import contextlib
import io
import os
import shutil

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

HERE = os.path.dirname(os.path.abspath(__file__))
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"     # TetA, TetB, octahedron (validated palette)
INK, MUTED, GRID = "#1f2328", "#6b7280", "#c9ccd1"


def run_setup(path, stop_marker):
    """Execute a verification script up to (not including) stop_marker; return its namespace."""
    src = open(path).read().split(stop_marker)[0]
    ns = {"__name__": "setup"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, path, "exec"), ns)
    return ns


def currents(Hn, psi):
    out = []
    n = len(psi)
    for i in range(n):
        for j in range(i + 1, n):
            if Hn[i, j] != 0:
                J = 2 * np.imag(np.conj(psi[j]) * Hn[j, i] * psi[i])     # physical flow i -> j (i dpsi/dt = H psi)
                if abs(J) > 1e-12:
                    out.append((i, j, J) if J > 0 else (j, i, -J))   # arrow along the flow
    return out


# ---------------- the 15-site pixel: vortex about z ----------------
P = run_setup(os.path.join(HERE, "verify_pixel_vortex.py"), "# --- Theorem 2")
syms = [P["D"], P["Df"], P["eA"], P["eB"], P["tf"], P["tA"], P["tB"], P["cA"], P["cB"]]
vals = [0.0, 0.4, -0.5, 0.7, 1.0, 1.0, 0.8, 1.0, 0.7]          # TetA and TetB differ (x != 1)
Hn = np.array(P["H"].subs(dict(zip(syms, vals))).evalf(), dtype=float)
B = np.array(P["B"].evalf(), dtype=complex)
E, W = np.linalg.eigh(B.conj().T @ Hn @ B)
k = int(np.argmax([abs(W[0, m]) for m in range(3)]))         # the vortex with the most core motion
psi = B @ W[:, k]
sites = [np.array(s, float) for s in P["sites"]]
J15 = currents(Hn, psi)
amp15 = np.abs(psi)
kind15 = P["kind"]

# ---------------- the 33-tile Triforce model: vortex about the leg (1,1,1) ----------------
T = run_setup(os.path.join(HERE, "..", "triforce-vortex", "verify_triforce_vortex.py"), "# Theorem: stationary vortices")
tsyms = list(T["site_orb"].values()) + list(T["bond_orb"].values())
rng = np.random.default_rng(5)
tvals = rng.normal(size=len(tsyms)) * 0.4 + np.where(np.arange(len(tsyms)) < len(T["site_orb"]), 0.0, 1.0)
Ht = np.array(T["H"].subs(dict(zip(tsyms, tvals))).evalf(), dtype=float)
Pw = np.array(T["Pw"].evalf(), dtype=complex)
U, sv, _ = np.linalg.svd(Pw); Bw = U[:, :10]
Et, Wt = np.linalg.eigh(Bw.conj().T @ Ht @ Bw)
starA, nt = T["starA"], T["n"]
m = int(np.argmax([np.linalg.norm((Bw @ Wt[:, q])[starA]) for q in range(10)]))
psit = Bw @ Wt[:, m]
tpos = [np.array([float(c) for c in v]) for v in T["cent"]]
Jt = currents(Ht, psit)
tsites = T["sites"]

# ---------------- geometry ----------------
TA = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], float)
TB = -TA
OCT = np.array([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)], float)


def tet_edges(Tt):
    return [(Tt[a], Tt[b]) for a in range(4) for b in range(a + 1, 4)]


def oct_edges():
    return [(OCT[a], OCT[b]) for a in range(6) for b in range(a + 1, 6) if abs(np.dot(OCT[a], OCT[b])) < 1e-9]


def frame(ax, alpha=0.35):
    for a, b in tet_edges(TA):
        ax.plot(*zip(a, b), color=BLUE, lw=1.0, alpha=alpha)
    for a, b in tet_edges(TB):
        ax.plot(*zip(a, b), color=ORANGE, lw=1.0, alpha=alpha)
    for a, b in oct_edges():
        ax.plot(*zip(a, b), color=AQUA, lw=1.0, alpha=alpha + 0.15)


def style3d(ax, elev, azim):
    ax.view_init(elev=elev, azim=azim)
    ax.set_box_aspect((1, 1, 1))
    lim = 1.25
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim)
    ax.set_axis_off()


def arrows3d(ax, pts, J, color=INK, scale=None, shrink=0.18):
    Jmax = max(j for _, _, j in J)
    for i, j, val in J:
        a, b = pts[i], pts[j]
        d = b - a
        a2, d2 = a + shrink * d, (1 - 2 * shrink) * d
        w = 0.6 + 2.6 * val / Jmax
        ax.quiver(*a2, *d2, color=color, lw=w, arrow_length_ratio=0.28, alpha=0.95)


fig = plt.figure(figsize=(15.5, 5.6), dpi=170)
fig.patch.set_facecolor("white")

# ---- panel a: the pixel vortex in 3D ----
ax = fig.add_subplot(1, 2, 1, projection="3d")
frame(ax)
ax.plot([0, 0], [0, 0], [-1.25, 1.25], color=MUTED, lw=1.2, ls=(0, (4, 3)))
J15_draw = [(i, j, v) for i, j, v in J15]
arrows3d(ax, sites, J15_draw)
for idx, s in enumerate(sites):
    kd = kind15[idx]
    if kd == "O":
        ax.scatter(*s, s=60, facecolors="white", edgecolors=INK, linewidths=1.2, depthshade=False)
    elif kd == "F":
        on_axis = abs(s[0]) + abs(s[1]) < 1e-9
        ax.scatter(*s, s=40 + 260 * amp15[idx] / amp15.max(), color="white" if on_axis else AQUA,
                   edgecolors=AQUA, linewidths=1.2, depthshade=False)
    else:
        ax.scatter(*s, s=40 + 260 * amp15[idx] / amp15.max(), color=BLUE if kd == "A" else ORANGE,
                   edgecolors="white", linewidths=0.8, depthshade=False)
ax.text(0.08, 0.05, 1.32, "axis: empty core", color=MUTED, fontsize=8.5)
style3d(ax, 22, 35)
ax.set_title("a  Vortex about an octahedron axis\ncorners and the octahedron ring carry the current together",
             loc="left", fontsize=10.5, color=INK)

# ---- panel b: top view of the same vortex ----
ax2 = fig.add_subplot(1, 2, 2)
ax2.set_aspect("equal")
for a, b in tet_edges(TA):
    ax2.plot([a[0], b[0]], [a[1], b[1]], color=BLUE, lw=0.8, alpha=0.25)
for a, b in tet_edges(TB):
    ax2.plot([a[0], b[0]], [a[1], b[1]], color=ORANGE, lw=0.8, alpha=0.25)
Jmax = max(v for _, _, v in J15)
for i, j, v in J15:
    a, b = sites[i][:2], sites[j][:2]
    if np.linalg.norm(b - a) < 1e-9:
        continue
    d = b - a
    ax2.annotate("", xy=a + 0.82 * d, xytext=a + 0.18 * d,
                 arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.6 + 2.6 * v / Jmax, mutation_scale=11))
for idx, s in enumerate(sites):
    kd = kind15[idx]
    if kd in ("A", "B"):
        top = s[2] > 0
        ax2.scatter(s[0] * (1.0 if top else 0.93), s[1] * (1.0 if top else 0.93), s=40 + 260 * amp15[idx] / amp15.max(),
                    color=BLUE if kd == "A" else ORANGE, edgecolors=INK if top else "white", linewidths=0.9, zorder=3)
    elif kd == "F" and abs(s[0]) + abs(s[1]) > 1e-9:
        ax2.scatter(s[0], s[1], s=40 + 260 * amp15[idx] / amp15.max(), color=AQUA, edgecolors="white", zorder=3)
ax2.scatter(0, 0, s=70, facecolors="white", edgecolors=INK, linewidths=1.2, zorder=4)
ax2.text(0.0, -0.2, "axis and Field Origin:\nzero amplitude", color=MUTED, fontsize=8, ha="center", va="top")
th = np.linspace(0.15 * np.pi, 0.85 * np.pi, 60)
Lsign = np.sign(sum(v * np.cross(sites[i], sites[j])[2] for i, j, v in J15))
ax2.plot(1.33 * np.cos(th), 1.33 * np.sin(th), color=INK, lw=1.0)
end = (th[-1], th[-2]) if Lsign > 0 else (th[0], th[1])
ax2.annotate("", xy=(1.33 * np.cos(end[0]), 1.33 * np.sin(end[0])), xytext=(1.33 * np.cos(end[1]), 1.33 * np.sin(end[1])),
             arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.0, mutation_scale=12))
ax2.text(0, 1.42, "net circulation about the axis", ha="center", color=INK, fontsize=8.5)
ax2.text(1.12, -0.12, "octahedron\nring", color=INK, fontsize=8, ha="left", va="top")
ax2.set_xlim(-1.5, 1.6); ax2.set_ylim(-1.5, 1.6); ax2.axis("off")
ax2.set_title("b  The same vortex from above\nring and corners turn together; dark rim = upper corners",
              loc="left", fontsize=10.5, color=INK)

# ---- panel c: Triforce vortex about the leg, seen down the leg ----
leg = np.array([1, 1, 1.0]) / np.sqrt(3)
e1 = np.array([1, -1, 0.0]) / np.sqrt(2); e2 = np.cross(leg, e1)
proj = lambda v: np.array([np.dot(v, e1), np.dot(v, e2)])
keyB = T["key"](-T["TA"][0])
starB = [q for q in range(nt) if tsites[q][0] == "outer" and keyB in tsites[q][2]]
on_leg = [q for q in range(nt) if np.linalg.norm(np.cross(tpos[q], leg)) < 1e-9]
amp_t = np.abs(psit)
def end_circ(ring):
    return sum(v * np.dot(np.cross(tpos[a], tpos[b]), leg) for a, b, v in Jt if a in ring and b in ring)
cA_, cB_ = end_circ(starA), end_circ(starB)
ax3 = fig.add_axes([0.675, 0.16, 0.30, 0.62])
ax3.set_aspect("equal")
for q in starA:
    tri = np.array([proj(np.array([float(c) for c in v])) for v in tsites[q][2]])
    ax3.add_patch(plt.Polygon(tri, closed=True, facecolor=BLUE, alpha=0.2 + 0.5 * amp_t[q] / amp_t[starA].max(),
                              edgecolor="white", lw=1.5))
for q in on_leg:
    if tsites[q][0] == "central" and np.dot(tpos[q], leg) > 0:
        tri = np.array([proj(np.array([float(c) for c in v])) for v in tsites[q][2]])
        ax3.add_patch(plt.Polygon(tri, closed=True, fill=False, edgecolor=AQUA, lw=1.6, ls="--"))
ringA = [(a, b, v) for a, b, v in Jt if a in starA and b in starA]
vmax = max(v for _, _, v in ringA)
from matplotlib.patches import FancyArrowPatch
Rarc = 0.42
for a, b, v in ringA:
    ta, tb = np.arctan2(*proj(tpos[a])[::-1]), np.arctan2(*proj(tpos[b])[::-1])
    d = (tb - ta + np.pi) % (2 * np.pi) - np.pi          # shortest turn from tile a to tile b
    th = np.linspace(ta + 0.18 * d, ta + 0.82 * d, 40)
    ax3.plot(Rarc * np.cos(th[:-1]), Rarc * np.sin(th[:-1]), color=INK, lw=0.8 + 2.2 * v / vmax)
    ax3.add_patch(FancyArrowPatch((Rarc * np.cos(th[-2]), Rarc * np.sin(th[-2])), (Rarc * np.cos(th[-1]), Rarc * np.sin(th[-1])),
                                  arrowstyle="-|>", mutation_scale=15, color=INK, lw=0.8 + 2.2 * v / vmax))
for q in starA:
    u = proj(tpos[q]); u = u / np.linalg.norm(u)
    ax3.plot([0.12 * u[0], Rarc * u[0]], [0.12 * u[1], Rarc * u[1]], color="white", lw=0.8, alpha=0.8)
ax3.scatter(0, 0, s=80, facecolors="white", edgecolors=INK, linewidths=1.3, zorder=5)
ax3.annotate("the leg: zero amplitude", xy=(0, 0), xytext=(0.62, 0.05), color=INK, fontsize=8, va="center",
             arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
ax3.text(0.62, 0.62, "3 outer tiles of the\nTetA star point (1,1,1)", color=INK, fontsize=8.5)
ax3.text(-0.95, -0.72, "central tile beneath\n(dashed, zero amplitude)", color=AQUA, fontsize=8)
ax3.set_xlim(-1.05, 1.15); ax3.set_ylim(-0.95, 0.95); ax3.axis("off")
ax3.set_title("c  Triforce vortex about a leg, looking down the leg\nthe star point's three outer tiles circulate around an empty core",
              loc="left", fontsize=10.5, color=INK)
# side strip: the whole leg
axs = fig.add_axes([0.70, 0.10, 0.26, 0.08]); axs.axis("off"); axs.set_xlim(-1.15, 1.15); axs.set_ylim(-0.6, 0.6)
axs.plot([-1.1, 1.1], [0, 0], color=MUTED, lw=1.1, ls=(0, (4, 3)))
for xx, lab, col in ((1.0, "TetA point", BLUE), (0.33, "central tile", AQUA), (0.0, "Field Origin", INK),
                     (-0.33, "central tile", AQUA), (-1.0, "TetB point", ORANGE)):
    face = "white" if col != BLUE and col != ORANGE else col
    axs.scatter(xx, 0, s=40, facecolors=face, edgecolors=col, linewidths=1.3, zorder=3)
    axs.text(xx, -0.28, lab, ha="center", va="top", fontsize=7.5, color=INK)
for xx, cc, col in ((1.0, cA_, BLUE), (-1.0, cB_, ORANGE)):
    th = np.linspace(0, 2 * np.pi, 80)
    axs.plot(xx + 0.07 * np.cos(th), 0.32 * np.sin(th), color=col, lw=1.2)
    sgn = 1 if cc > 0 else -1
    axs.annotate("", xy=(xx + 0.07 * np.cos(sgn * 0.6), 0.32 * np.sin(sgn * 0.6)),
                 xytext=(xx + 0.07 * np.cos(0.0), 0.32 * np.sin(0.0)),
                 arrowprops=dict(arrowstyle="-|>", color=col, lw=1.0, mutation_scale=8))
axs.text(0, 0.42, "along the leg: both star points turn, the core between them is empty", ha="center", fontsize=7.5, color=MUTED)
print(f"circulation at the TetA end {cA_:+.4f}, at the TetB end {cB_:+.4f}")

# legend
from matplotlib.lines import Line2D
handles = [Line2D([], [], color=BLUE, marker="o", ls="-", lw=1, label="TetA"),
           Line2D([], [], color=ORANGE, marker="o", ls="-", lw=1, label="TetB"),
           Line2D([], [], color=AQUA, marker="o", ls="-", lw=1, label="octahedron (core)"),
           Line2D([], [], color=INK, lw=2, label="bond current J (width = size)"),
           Line2D([], [], color=MUTED, lw=1.2, ls=(0, (4, 3)), label="axis: zero amplitude")]
fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False, fontsize=9, labelcolor=INK)
fig.text(0.5, 0.005, "Arrows are the currents of exact vortex eigenstates of the proofs' models (marker size: amplitude). "
         "a, b: 15-site pixel, TetA and TetB parameters unequal. c: 33-tile Triforce model, ring currents of the two star points shown.",
         ha="center", fontsize=8, color=MUTED)
fig.subplots_adjust(left=0.01, right=0.66, top=0.86, bottom=0.1, wspace=0.05)
out = os.path.join(HERE, "vortex_figure.png")
fig.savefig(out, facecolor="white")
shutil.copy(out, os.path.join(HERE, "..", "triforce-vortex", "vortex_figure.png"))
print("wrote", out)
