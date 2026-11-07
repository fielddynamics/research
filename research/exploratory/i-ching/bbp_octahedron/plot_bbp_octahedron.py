"""
Figure for BOOK_OF_CHANGES_AND_PI.md.

Panel A: the eight trigrams at the corners of the cube, the two Shuo Gua
families as the two tetrahedra, the TIME axis from Qian to Kun, and the four
corners the BBP formula uses, with their weights.

Panel B: four members of pi's family of base-16 formulas (Adamchik and Wagon,
w(r) = BBP + r * (8, -8, -4, -8, -2, -2, 1, 0)), shown corner by corner.
Only r = 0, the BBP formula, leaves both TIME corners empty.

    python plot_bbp_octahedron.py      # writes bbp_octahedron.png
"""
from fractions import Fraction
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

BLUE, ORANGE = "#2a78d6", "#eb6834"          # father's family (TetA), mother's family (TetB)
INK, INK2, MUTED, SURF = "#0b0b0b", "#52514e", "#b9b8b2", "#fcfcfb"

TRIGRAM = {  # (glyph, name, image); glyphs kept for reference, trigrams are drawn
   7: ("☰", "Qian", "Heaven"), 4: ("☳", "Zhen", "Thunder"), 2: ("☵", "Kan", "Water"),
           1: ("☶", "Gen", "Mountain"), 0: ("☷", "Kun", "Earth"), 3: ("☴", "Xun", "Wind"),
           5: ("☲", "Li", "Fire"), 6: ("☱", "Dui", "Lake")}
TETA = {7, 4, 2, 1}
BBP = {1: 4, 4: -2, 5: -1, 6: -1}           # by corner label (slot j -> corner j mod 8)
AW = {1: 8, 2: -8, 3: -4, 4: -8, 5: -2, 6: -2, 7: 1, 0: 0}


def draw_trigram(ax, v, cx, cy, w=0.42, gap=0.13, color=INK, lw=2.6):
    """Draw trigram v as three lines, bottom line first (bottom line = most significant bit)."""
    lines = [(v >> 2) & 1, (v >> 1) & 1, v & 1]          # bottom, middle, top
    for i, yang in enumerate(lines):
        y = cy + (i - 1) * gap
        if yang:
            ax.plot([cx - w / 2, cx + w / 2], [y, y], color=color, lw=lw, solid_capstyle="butt")
        else:
            ax.plot([cx - w / 2, cx - w * 0.08], [y, y], color=color, lw=lw, solid_capstyle="butt")
            ax.plot([cx + w * 0.08, cx + w / 2], [y, y], color=color, lw=lw, solid_capstyle="butt")


def minus(s):
    return s.replace("-", "\u2212")


def coords(v):  # bottom line = x (MSB), middle = y, top = z
    return ((v >> 2) & 1, (v >> 1) & 1, v & 1)


def project(c):  # simple oblique projection of the unit cube
    x, y, z = c
    return (x + 0.42 * y, z + 0.30 * y)


fig, (axA, axB) = plt.subplots(1, 2, figsize=(13.5, 5.6), gridspec_kw={"width_ratios": [1.1, 1]})
fig.patch.set_facecolor(SURF)

# ---------------- Panel A ----------------
axA.set_facecolor(SURF)
P = {v: project(coords(v)) for v in range(8)}
for a in range(8):                                  # cube edges
    for b in range(a + 1, 8):
        if bin(a ^ b).count("1") == 1:
            axA.plot(*zip(P[a], P[b]), color=MUTED, lw=1, zorder=1)
for fam, col in ((TETA, BLUE), (set(range(8)) - TETA, ORANGE)):   # tetrahedra
    vs = sorted(fam)
    for i in range(4):
        for j in range(i + 1, 4):
            axA.plot(*zip(P[vs[i]], P[vs[j]]), color=col, lw=2, alpha=0.9, zorder=2)
axA.plot(*zip(P[0], P[7]), color=INK2, lw=1.5, ls=(0, (4, 3)), zorder=3)  # TIME axis
mx, my = (P[0][0] + P[7][0]) / 2, (P[0][1] + P[7][1]) / 2
axA.plot(mx, my, "o", ms=5, color=INK2, zorder=4)
axA.annotate("Field Origin", (mx, my), xytext=(mx - 0.05, my - 0.30), fontsize=9, color=INK2,
             ha="center", arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8),
             bbox=dict(boxstyle="round,pad=0.15", fc=SURF, ec="none", alpha=0.9))
axA.annotate("TIME axis", P[7], xytext=(P[7][0] + 0.08, P[7][1] + 0.18), fontsize=9, color=INK2)

offsets = {7: (0.09, 0.05), 4: (0.09, -0.13), 2: (-0.09, 0.0), 1: (-0.10, 0.0),
           0: (-0.09, -0.12), 3: (-0.07, 0.10), 5: (0.11, 0.10), 6: (0.10, -0.10)}
for v in range(8):
    x, y = P[v]
    col = BLUE if v in TETA else ORANGE
    if v in BBP:
        axA.plot(x, y, "o", ms=19, mfc=SURF, mec=INK, mew=1.6, zorder=5)
    axA.plot(x, y, "o", ms=11, color=col, mec=SURF, mew=2, zorder=6)
    g, name, eng = TRIGRAM[v]
    dx, dy = offsets[v]
    ha = "left" if dx > 0 else "right"
    w = minus(f"\nweight {BBP[v]:+d}") if v in BBP else ""
    axA.text(x + dx, y + dy, f"{name} · {eng} ({v}){w}", fontsize=9.5, color=INK, ha=ha,
             va="center", zorder=7, linespacing=1.3,
             bbox=dict(boxstyle="round,pad=0.15", fc=SURF, ec="none", alpha=0.9))
axA.set_title("A   The trigrams are the stellated octahedron", loc="left", fontsize=12, color=INK,
              pad=12, fontweight="bold")
axA.text(0.0, -0.06, "Blue: the father's family (TetA).  Orange: the mother's family (TetB).\n"
         "Ringed: the four corners the BBP formula uses, two in each family.",
         transform=axA.transAxes, fontsize=9, color=INK2, va="top")
axA.set_aspect("equal")
axA.set_xlim(-0.85, 2.05)
axA.set_ylim(-0.45, 1.6)
axA.axis("off")

# ---------------- Panel B ----------------
axB.set_facecolor(SURF)
rows = [(Fraction(1), "r = 1"), (Fraction(-1, 4), "r = −1/4\n(the base −4 formula)"),
        (Fraction(-1, 2), "r = −1/2\n(four corners, split 3 + 1)"), (Fraction(0), "r = 0\nthe BBP formula")]
order = [0, 1, 2, 3, 4, 5, 6, 7]
for i, (r, lab) in enumerate(rows):
    yrow = len(rows) - 1 - i
    w = {v: Fraction(BBP.get(v, 0)) + r * AW[v] for v in range(8)}
    for k, v in enumerate(order):
        active = w[v] != 0
        col = (BLUE if v in TETA else ORANGE) if active else SURF
        axB.add_patch(Rectangle((k + 0.06, yrow + 0.08), 0.88, 0.84, facecolor=col,
                                edgecolor=MUTED if not active else SURF, lw=1.2, alpha=0.9 if active else 1))
        if active:
            txt = str(w[v]) if w[v].denominator == 1 else f"{w[v].numerator}/{w[v].denominator}"
            axB.text(k + 0.5, yrow + 0.5, minus(txt), ha="center", va="center",
                     fontsize=9.5 if len(txt) <= 3 else 8, color="white", fontweight="bold")
    axB.text(-0.15, yrow + 0.5, lab, ha="right", va="center", fontsize=9.5,
             color=INK, fontweight="bold" if r == 0 else "normal")
for k in (0, 7):                                     # TIME columns
    axB.add_patch(Rectangle((k + 0.02, -0.04), 0.96, len(rows) + 0.08, fill=False, ec=INK, lw=1.4, ls=(0, (4, 3))))
for k, v in enumerate(order):
    g, name, _ = TRIGRAM[v]
    draw_trigram(axB, v, k + 0.5, len(rows) + 0.42, w=0.5, gap=0.11, lw=2.2)
    axB.text(k + 0.5, len(rows) + 0.66, name, ha="center", va="bottom", fontsize=9.5, color=INK)
axB.text(0.5, -0.32, "TIME", ha="center", fontsize=8.5, color=INK2)
axB.text(7.5, -0.32, "TIME", ha="center", fontsize=8.5, color=INK2)
axB.set_xlim(-3.4, 8.1)
axB.set_ylim(-0.6, len(rows) + 1.1)
axB.axis("off")
axB.set_title("B   π's base-16 formulas, corner by corner", loc="left", fontsize=12, color=INK,
              pad=12, fontweight="bold")
axB.text(0.0, -0.06, "Each row is one formula for π; a filled cell is a corner the formula uses.\n"
         "Every formula of this kind is one of the rows w(r). Only r = 0 leaves both TIME corners empty.",
         transform=axB.transAxes, fontsize=9, color=INK2, va="top")

plt.tight_layout()
plt.savefig("bbp_octahedron.png", dpi=180, facecolor=SURF, bbox_inches="tight")
print("wrote bbp_octahedron.png")
