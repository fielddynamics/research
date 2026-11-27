#!/usr/bin/env python3
"""Generate the figures embedded in the GP-1 ... GP-8 READMEs.

    python make_figures.py          # writes gp*/figures/*.svg

Every curve is computed here from the formulas proved and checked in the
proofs (nothing is hand-drawn). Static SVG in the repository's dark diagram
style (navy gradient #102237 -> #162f43, border #496075, light inks; the
palette of diagrams/closure-hinge.svg), so the figures match the existing
diagrams in both GitHub themes.
Requires numpy, scipy, matplotlib.
"""
import math
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from scipy.linalg import expm  # noqa: E402

HERE = Path(__file__).resolve().parent
S1, S2, S3, S4 = "#78bdf0", "#d6a15e", "#59d4b5", "#f0cf7d"   # sky, amber, teal, gold (repo diagram accents)
INK, INK2, GRID, SURF = "#eef5fb", "#b7c9d7", "#26435a", "#13283d"
PANEL, MUTED, EDGE = "#1b3a52", "#6f8699", "#496075"
BG0, BG1 = "#102237", "#162f43"

plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": "none", "savefig.facecolor": SURF,
    "axes.edgecolor": INK2, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.8, "axes.spines.top": False, "axes.spines.right": False,
    "lines.linewidth": 1.6, "font.size": 10, "axes.titlesize": 11, "axes.titleweight": "bold",
    "axes.titlecolor": INK, "legend.labelcolor": INK, "legend.frameon": False, "svg.fonttype": "path",
    "font.family": "DejaVu Sans",
})


def _dress(path):
    """Replace matplotlib's flat figure background with the repository's
    diagram frame: navy gradient, rounded corners, #496075 border."""
    import re
    svg = path.read_text()
    w = float(re.search(r'width="([\d.]+)pt"', svg).group(1))
    h = float(re.search(r'height="([\d.]+)pt"', svg).group(1))
    frame = (f'<defs><linearGradient id="gpbg" x2="1" y2="1"><stop stop-color="{BG0}"/>'
             f'<stop offset="1" stop-color="{BG1}"/></linearGradient></defs>'
             f'<rect x="0.75" y="0.75" width="{w - 1.5:.2f}" height="{h - 1.5:.2f}" rx="12" '
             f'fill="url(#gpbg)" stroke="{EDGE}" stroke-width="1.2"/>')
    svg, n = re.subn(r'<g id="patch_1">\s*<path d="[^"]*"\s*style="fill: {0}"\s*/>\s*</g>'.format(SURF), frame, svg, count=1)
    assert n == 1, path
    path.write_text(svg)


def save(fig, proof, name):
    out = HERE / proof / "figures"
    out.mkdir(exist_ok=True)
    path = out / f"{name}.svg"
    fig.savefig(path, bbox_inches="tight", pad_inches=0.22)
    plt.close(fig)
    _dress(path)
    print(f"  {proof}/figures/{name}.svg")


U3 = 1 - 1 / math.sqrt(2)
H_IN = 5776.0

# ---------------------------------------------------------------------------
# GP-1
# ---------------------------------------------------------------------------
def gp1():
    P = "gp1-half-section-balance-plane"
    # 1. meridional section with the three halving levels
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.grid(False)
    ax.fill([-1, 1, 0], [0, 0, 1], color=PANEL, ec=INK2, lw=1.2)
    levels = [(1 - 2 ** (-1 / 3), "volume halved", S3), (U3, "section area halved (uniform flux)", S1), (0.5, "height halved", S2)]
    for lv, lab, col in levels:
        w = 1 - lv
        ax.plot([-w, w], [lv, lv], color=col, lw=2)
        ax.text(1.05 * w + 0.03, lv, f"u = {lv:.4f}  {lab}", va="center", color=INK, fontsize=9)
    ax.fill([-(1 - U3), 1 - U3, 0], [U3, U3, 1], color=S1, alpha=0.10)
    kc = 1692.55 / H_IN
    ax.plot([-0.08, 0.08], [kc, kc], color=INK, lw=3, solid_capstyle="butt")
    ax.annotate("King's Chamber floor (Petrie)\n1692.55 in = 0.29303 h", xy=(-0.08, kc), xytext=(-1.95, 0.66),
                fontsize=9, color=INK, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
    ax.text(0, 0.80, "area above\nthe blue level = 1/2", ha="center", fontsize=9, color=S1)
    ax.set_xlim(-2.0, 2.4); ax.set_ylim(-0.03, 1.05); ax.set_yticks([0, 0.25, 0.5, 0.75, 1]); ax.set_xticks([])
    ax.set_ylabel("fractional height u = z/h"); ax.spines["bottom"].set_visible(False)
    ax.set_title("Three distinct halving levels of one cone (D = 3)", loc="left")
    save(fig, P, "fig1_halving_levels")

    # 2. horizontal vs meridional halving across dimension
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    D = np.arange(2, 9)
    ax.plot(D, 1 - 2.0 ** (-1 / (D - 1)), "o-", color=S1, ms=6, label="horizontal sections halved")
    ax.plot(D, [U3] * len(D), "s--", color=S2, ms=6, label="meridional section halved")
    ax.annotate("coincide only at D = 3", xy=(3, U3), xytext=(4.2, 0.42), fontsize=9,
                arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
    ax.text(8.1, 1 - 2 ** (-1 / 7), "horizontal", color=S1, va="center", fontsize=9)
    ax.text(8.1, U3, "meridional", color=S2, va="center", fontsize=9)
    ax.set_xlim(1.8, 9.2); ax.set_xlabel("dimension D"); ax.set_ylabel("balance level u*")
    ax.set_title("Balance level u* = 1 - 2^(-1/(D-1)) against the meridional level", loc="left")
    ax.legend(loc="upper right")
    save(fig, P, "fig2_dimension")

    # 3. survey comparison with allowance intervals
    fig, ax = plt.subplots(figsize=(7.2, 2.8))
    pred, dpred = U3 * H_IN, U3 * 7.0
    rows = [("geometric target 0.292893 h", pred, dpred, S1),
            ("King's Chamber floor (range + 0.6)", 1692.55, 1.75, S2),
            ("Phase 0 model half-flux plane", 1692.55 - 0.82 + 0.0, 0.0, S3)]
    for i, (lab, c, d, col) in enumerate(rows):
        y = 2 - i
        if d:
            ax.plot([c - d, c + d], [y, y], color=col, lw=6, alpha=0.35, solid_capstyle="round")
        ax.plot([c], [y], "o", color=col, ms=8)
        ax.text(1686.4, y, lab, va="center", ha="left", fontsize=9)
    ax.axvspan(1691.4, 1693.7, color=PANEL, zorder=0)
    ax.set_yticks([]); ax.set_xlim(1686.3, 1696.5); ax.set_ylim(-0.6, 2.6)
    ax.set_xlabel("height above pavement (in)")
    ax.set_title("Residual +0.80 in inside a combined allowance of ±3.80 in", loc="left")
    save(fig, P, "fig3_survey")

    # 4. graded structural trace
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    u = np.linspace(0, 1, 400)
    ax.plot(u, 13 + 8 * (1 - u) ** 2, color=S1, lw=2)
    for uu, val, lab, dy in [(0, 21, "base: Tr = 21 (A_B = I)", -0.6), (U3, 17, "balance: Tr = 17 (A_B = P_even)", 0.4), (1, 13, "apex: Tr = 13 (A_B = J)", 1.1)]:
        ax.plot([uu], [val], "o", color=S1, ms=7)
        ax.text(uu + (0.03 if uu < 1 else -0.03), val + dy, lab, ha="left" if uu < 1 else "right", fontsize=9)
    ax.set_ylim(12.3, 21.8)
    ax.axvline(U3, color=INK2, lw=0.8, ls=":")
    ax.set_xlabel("fractional height u"); ax.set_ylabel("Tr A_B(u) = 13 + 8 mu_B")
    ax.set_title("Graded structural operator: a conditional labelling, not a derivation", loc="left")
    save(fig, P, "fig4_graded_trace")


# ---------------------------------------------------------------------------
# GP-2
# ---------------------------------------------------------------------------
def gp2():
    P = "gp2-balance-plane-robustness"
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 3.6))
    u = np.linspace(0.002, 0.995, 800)
    for bv, col in [(-3, S2), (0, S1), (3, S3)]:
        a1.plot(u, (1 - u) ** 2 * (1 + bv * u), color=col, label=f"b = {bv:+d}")
    a1.axhline(0.5, color=INK2, lw=0.8, ls=":")
    a1.set_ylim(-1.2, 1.6); a1.set_xlabel("u"); a1.set_ylabel("g_b(u) = (1-u)^2 (1 + b u)")
    a1.set_title("Signed share; each crosses 1/2 once", loc="left"); a1.legend(loc="upper right")
    B = (1 / (2 * (1 - u) ** 2) - 1) / u
    a2.plot(u, B, color=S1, lw=2)
    a2.set_ylim(-20, 20); a2.set_xlabel("balance level u*"); a2.set_ylabel("b = B(u*)")
    a2.axvline(U3, color=INK2, lw=0.8, ls=":"); a2.text(U3 + 0.02, -17, "u* = 0.2929 at b = 0", fontsize=9)
    a2.set_title("B is an increasing bijection (0,1) → ℝ", loc="left")
    fig.tight_layout(); save(fig, P, "fig1_all_b_uniqueness")

    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    e = np.linspace(0, 0.45, 300)
    lo, hi = 1 - 1 / np.sqrt(2 * (1 - e)), 1 - 1 / np.sqrt(2 * (1 + e))
    ax.fill_between(e, lo, hi, color=S1, alpha=0.15, lw=0)
    ax.plot(e, lo, color=S1); ax.plot(e, hi, color=S1)
    ax.plot(e, U3 - e / (2 * math.sqrt(2)), color=S2, ls="--"); ax.plot(e, U3 + e / (2 * math.sqrt(2)), color=S2, ls="--")
    ax.text(0.452, hi[-1], "upper (attained by r_+)", fontsize=9, va="center")
    ax.text(0.452, lo[-1], "lower (attained by r_-, eps < 1/2)", fontsize=9, va="center")
    ax.text(0.05, 0.40, "dashed: first order ±eps/(2√2)", color=S2, fontsize=9)
    ax.set_xlabel("fractional non-uniformity eps"); ax.set_ylabel("allowed balance level u*")
    ax.set_xlim(0, 0.62); ax.set_title("Sharp, asymmetric interval for any bounded non-uniformity", loc="left")
    save(fig, P, "fig2_interval")

    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    items = [("Earth's gradient (exact solid angle)", 0.0276, S3),
             ("gravity budget, refined (4πGρR_eq)", 0.163, S1),
             ("gravity budget, original (8πGρR_c)", 0.356, MUTED),
             ("observed residual", 0.80, S2),
             ("height-reconstruction allowance", 2.05, MUTED)]
    for i, (lab, v, col) in enumerate(items[::-1]):
        ax.barh(i, v, color=col, height=0.55)
        ax.text(v + 0.03, i, f"{v:.3g} in", va="center", fontsize=9)
    ax.set_yticks(range(len(items))); ax.set_yticklabels([x[0] for x in items[::-1]])
    ax.set_xlabel("shift of the balance level (in)"); ax.set_xlim(0, 2.5); ax.grid(axis="y", visible=False)
    ax.set_title("Gravity cannot account for the residual; the survey can", loc="left")
    save(fig, P, "fig3_gravity_budget")


# ---------------------------------------------------------------------------
# GP-3
# ---------------------------------------------------------------------------
def gp3():
    P = "gp3-coupling-signatures-and-hinge"
    f = lambda K, s: 1 + s * K + K * K
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    Ks = range(1, 7)
    for s, col, lab in [(-1, S2, "s = -1 (TetB-type, Φ6)"), (0, S3, "s = 0 (Field-Origin-type, Φ4)"), (1, S1, "s = +1 (TetA-type, Φ3)")]:
        ax.plot(list(Ks), [f(K, s) for K in Ks], "o", color=col, ms=7, label=lab)
    for K in range(1, 6):
        ax.plot([K, K + 1], [f(K, 1), f(K + 1, -1)], color=INK2, lw=1, ls="--")
    for K in Ks:
        ax.text(K + 0.08, f(K, 0), str(f(K, 0)), fontsize=8, va="center", color=INK2)
    ax.annotate("hinge 21 = f(4,+1) = f(5,−1)", xy=(4.5, 21), xytext=(1.2, 30), fontsize=9,
                arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
    ax.annotate("17 = f(4,0): occurs nowhere else", xy=(4, 17), xytext=(4.6, 9), fontsize=9,
                arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
    ax.set_xlabel("level K"); ax.set_ylabel("f(K, s) = 1 + sK + K²")
    ax.set_title("The only coincidences between levels are the hinges (dashed)", loc="left")
    ax.legend(loc="upper left", fontsize=9)
    save(fig, P, "fig1_ladder_hinge")

    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    da, db = [2, 3, 2], [2, 3, 2]
    labs_a = ["K: 13"] * da[0] + ["K: 17"] * da[1] + ["K: 21"] * da[2]
    labs_b = ["K+1: 21"] * db[0] + ["K+1: 26"] * db[1] + ["K+1: 31"] * db[2]
    Mmask = np.zeros((sum(db), sum(da)))
    Mmask[:db[0], da[0] + da[1]:] = 1
    ax.imshow(Mmask, cmap=matplotlib.colors.ListedColormap([PANEL, S1]), aspect="equal")
    ax.set_xticks(range(sum(da))); ax.set_xticklabels(labs_a, rotation=60, fontsize=8)
    ax.set_yticks(range(sum(db))); ax.set_yticklabels(labs_b, fontsize=8)
    ax.grid(False)
    for x in np.arange(-0.5, sum(da), 1):
        ax.axvline(x, color=SURF, lw=2)
    for y in np.arange(-0.5, sum(db), 1):
        ax.axhline(y, color=SURF, lw=2)
    ax.set_xlabel("source eigenspaces (K = 4: 13, 17, 21)"); ax.set_ylabel("target eigenspaces (K = 5)")
    ax.set_title("Allowed entries of every intertwiner T: one block", loc="left")
    save(fig, P, "fig2_intertwiner_block")

    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    K = 4
    names = ["A₀ = 21", "B₀ = 13", "B₁ = 241", "B₂ = 65281", "B₃"]
    vals = [f(K, 1), f(K, -1), f(K ** 2, -1), f(K ** 4, -1), f(K ** 8, -1)]
    ax.bar(range(5), np.log10(vals), color=[S1, S2, S2, S2, S2], width=0.55)
    for i, v in enumerate(vals):
        ax.text(i, math.log10(v) + 0.15, f"{v:,}" if v < 1e7 else f"{v:.3e}", ha="center", fontsize=8)
    ax.set_xticks(range(5)); ax.set_xticklabels(names); ax.set_ylabel("log10 of factor")
    ax.set_title("Fusion tower f(4^(2^n), +1) = A₀ B₀ B₁ … : every factor pairwise coprime", loc="left")
    ax.grid(axis="x", visible=False)
    save(fig, P, "fig3_tower")


# ---------------------------------------------------------------------------
# GP-4
# ---------------------------------------------------------------------------
def gp4():
    P = "gp4-registration-and-coherence"
    rng = np.random.default_rng(3)
    fig, axs = plt.subplots(1, 3, figsize=(9.4, 3.4), subplot_kw=dict(projection="polar"))
    sets = [("disordered", rng.uniform(0, 2 * np.pi, 210)),
            ("registered (21-gon)", np.repeat(2 * np.pi * np.arange(21) / 21, 10) + rng.normal(0, 0.02, 210)),
            ("coherent", rng.normal(0.6, 0.05, 210))]
    for ax, (title, th) in zip(axs, sets):
        C1 = abs(np.exp(1j * th).mean()); C21 = abs(np.exp(21j * th).mean())
        ax.scatter(th, np.ones_like(th) + rng.normal(0, 0.03, th.size), s=8, color=S1, alpha=0.6, lw=0)
        ax.set_ylim(0, 1.25); ax.set_yticks([]); ax.set_xticklabels([])
        ax.set_title(f"{title}\nC₁ = {C1:.2f}   C₂₁ = {C21:.2f}", fontsize=10)
    fig.tight_layout(); save(fig, P, "fig1_ensembles")

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.6))
    c1 = np.linspace(0.995, 1, 300)
    a1.fill_between(c1, np.maximum(0, 1 - 441 * (1 - c1)), 1, color=S1, alpha=0.15, lw=0)
    a1.plot(c1, np.maximum(0, 1 - 441 * (1 - c1)), color=S1)
    a1.axhline(0.5, color=INK2, lw=0.8, ls=":"); a1.axvline(1 - 1 / 882, color=INK2, lw=0.8, ls=":")
    a1.text(0.9951, 0.55, "C₁ ≥ 1 − 1/882 ⇒ C₂₁ ≥ 1/2", fontsize=9)
    a1.set_xlabel("coherence C₁"); a1.set_ylabel("guaranteed C₂₁")
    a1.set_title("Coherence forces registration (N² bound)", loc="left")
    r = np.linspace(0.85, 1, 300)
    a2.plot(r, np.maximum(0, 1 - 9 * (1 - r)), color=S2, lw=2)
    a2.plot([0.99], [0.91], "o", color=S2, ms=7); a2.text(0.905, 0.60, "99% per stage\n⇒ C₁ ≥ 91%", fontsize=9)
    a2.set_xlabel("registration per stage, C₃ = C₇ = r"); a2.set_ylabel("guaranteed coherence C₁")
    a2.set_title("Approximate coprime locking (3 and 7)", loc="left")
    fig.tight_layout(); save(fig, P, "fig2_bounds")

    N = 21; d = np.arange(N)
    F14 = np.array([sum(np.exp(2j * np.pi * k * x / N) for k in range(N) if k % 3) for x in d]).real / 14
    F7 = np.array([sum(np.exp(2j * np.pi * k * x / N) for k in range(0, N, 3)) for x in d]).real / 7
    F21 = 2 / 3 * F14 + 1 / 3 * F7
    fig, axs = plt.subplots(3, 1, figsize=(7.2, 5.2), sharex=True)
    for ax, F, col, lab in [(axs[0], F14, S2, "F₁₄: 14 characters k ≢ 0 (mod 3)"),
                            (axs[1], F7, S3, "F₇: 7 characters k ≡ 0 (mod 3)"),
                            (axs[2], F21, S1, "(2/3) F₁₄ + (1/3) F₇ = δ")]:
        ax.vlines(d, 0, F, color=col, lw=2); ax.plot(d, F, "o", color=col, ms=5)
        ax.axhline(0, color=INK2, lw=0.8); ax.set_ylim(-0.7, 1.15); ax.set_ylabel("F(d)")
        ax.set_title(lab, loc="right", fontsize=9, fontweight="normal", color=INK2)
    axs[2].set_xlabel("address offset d"); axs[2].set_xticks(range(0, 21, 7))
    fig.suptitle("Complementary reconstruction of the exact 21-address selector", x=0.02, ha="left",
                 fontsize=11, fontweight="bold", color=INK)
    fig.tight_layout(); save(fig, P, "fig3_characters")


# ---------------------------------------------------------------------------
# GP-5
# ---------------------------------------------------------------------------
def gp5():
    P = "gp5-two-site-transfer-bound"
    k = 1.0
    t = np.linspace(0, 2 * math.pi, 600)
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    for D, col in [(0.0, S1), (1.5, S2), (4.0, S3)]:
        Om = math.sqrt(D * D + 4 * k * k)
        ax.plot(t, 4 * k * k / (D * D + 4 * k * k) * np.sin(Om * t / 2) ** 2, color=col, label=f"Δ = {D:g} k")
    ax.plot(t, np.sin(np.minimum(k * t, math.pi / 2)) ** 2, color=INK, lw=1.2, ls="--", label="budget bound sin²(min(∫|κ|, π/2))")
    ax.set_xlabel("t (units of 1/|κ|)"); ax.set_ylabel("transfer P(t)"); ax.set_ylim(0, 1.08)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=9)
    ax.set_title("Detuning lowers the peak; no drive beats the coupling budget", loc="left")
    save(fig, P, "fig1_transfer_budget")

    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    tt = np.linspace(0, 8, 800)
    for g, col in [(0.0, S1), (0.3, S2), (1.0, S3)]:
        ax.plot(tt, np.exp(-g * tt) * np.sin(k * tt) ** 2, color=col, label=f"γ = {g:g} k")
        to = math.atan(2 * k / g) / k if g else math.pi / (2 * k)
        ax.plot([to], [math.exp(-g * to) * math.sin(k * to) ** 2], "o", color=col, ms=7)
    ax.set_xlabel("t (units of 1/k)"); ax.set_ylabel("P_γ(t) = e^(−γt) sin²(kt)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize=9)
    ax.set_title("Equal loss: optimum at t_opt = arctan(2k/γ)/k (dots)", loc="left")
    save(fig, P, "fig2_loss_optimum")

    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    Pm = np.linspace(0, 1, 400)
    ax.plot(Pm, np.arcsin(np.sqrt(Pm)), color=S1, lw=2)
    ax.fill_between(Pm, np.arcsin(np.sqrt(Pm)), math.pi / 2 + 0.2, color=S1, alpha=0.12, lw=0)
    ax.text(0.15, 1.35, "allowed region for ∫₀ᵀ |κ| dt", fontsize=9)
    ax.set_xlabel("measured transfer probability P"); ax.set_ylabel("required ∫₀ᵀ |κ| dt")
    ax.set_title("Inverse bound: a measured transfer requires ∫|κ| ≥ arcsin √P", loc="left")
    save(fig, P, "fig3_inverse_bound")

    gx, gy, wB = 0.05, 0.07, 1.0
    H3 = np.array([[0, 0, gx], [0, 0, gy], [gx, gy, wB]])
    kap = gx * gy / (0 - wB); dx, dy = gx * gx / -wB, gy * gy / -wB
    Heff = np.array([[dx, kap], [kap, dy]])
    T = np.linspace(0, 2.2 * math.pi / abs(kap), 900)
    full = [abs((expm(-1j * H3 * s) @ np.array([1, 0, 0]))[1]) ** 2 for s in T]
    eff = [abs((expm(-1j * Heff * s) @ np.array([1, 0]))[1]) ** 2 for s in T]
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.plot(T, full, color=S1, lw=2, label="exact 3-mode (x, y, intermediate B)")
    ax.plot(T, eff, color=S2, lw=1.4, ls="--", label="dispersive 2-mode: κ = g_x g_y/(ω−ω_B) + shifts")
    ax.set_xlabel("t"); ax.set_ylabel("transfer x → y"); ax.legend(loc="upper right", fontsize=9)
    ax.set_ylim(0, 1.1)
    ax.set_title("A coupling induced through an intermediate sector (Schur complement)", loc="left")
    save(fig, P, "fig4_induced_coupling")


# ---------------------------------------------------------------------------
# GP-6, GP-7, GP-8
# ---------------------------------------------------------------------------
from itertools import product  # noqa: E402
from matplotlib.patches import Polygon, Rectangle, FancyArrowPatch  # noqa: E402

STONE = "#2c3f4f"   # stone fill on the navy surface


def gp6():
    P = "gp6-structural-boundary-response"
    u0 = U3
    fig, ax = plt.subplots(figsize=(8.6, 4.6)); ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-1.2, 2.45); ax.set_ylim(-0.22, 1.12)
    ax.add_patch(Polygon([(-1, 0), (1, 0), (0, 1)], closed=True, fc=STONE, ec=S2, lw=1.8))
    a = 1 - u0
    ax.add_patch(Polygon([(-1, 0), (1, 0), (a, u0), (-a, u0)], closed=True, fc=S1, alpha=0.18, lw=0))
    ax.plot([-a, a], [u0, u0], color=S3, lw=2.5)
    ax.text(0, 0.62, "upper volume\n35.36%", ha="center", va="center", fontsize=10)
    ax.text(0, 0.10, "lower volume 64.64%", ha="center", fontsize=10)
    ax.annotate("half-section plane\nA/A₀ = 1/2", xy=(a, u0), xytext=(1.12, 0.50),
                arrowprops=dict(arrowstyle="-", color=S3, lw=0.9), color=S3, fontsize=10)
    for x in (-0.65, -0.3, 0.3, 0.65):
        ax.annotate("", xy=(x, 0.02), xytext=(x, -0.17), arrowprops=dict(arrowstyle="->", color=S1, lw=1.6))
    ax.text(1.12, 0.10, "equal outgoing flux:\n2 F_z = F_0 + M(z)", fontsize=10, color=INK)
    ax.set_title("Sourced boundary accounting", loc="left")
    save(fig, P, "fig1_sourced_closure")

    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    x = np.logspace(-3, 4, 500)
    ax.semilogx(x, x / (1 + x), color=S1, lw=2, label="transverse  μ")
    ax.semilogx(x, 1 - 1 / (1 + x) ** 2, color=S3, lw=2, label="longitudinal  μ + xμ′")
    ax.axvline(1, ls=":", color=INK2, lw=0.8)
    ax.set_xlabel("background field ratio x = |∇Φ|/a₀"); ax.set_ylabel("response eigenvalue"); ax.set_ylim(0, 1.05)
    ax.legend(loc="lower right"); ax.set_title("Constitutive response (where the interpolating law applies)", loc="left")
    save(fig, P, "fig2_response_tensor")

    fig, ax = plt.subplots(figsize=(8.0, 3.4)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 3)
    yy = 0.5 + 2.1 * u0
    for i, (name, col) in enumerate([("virtual boundary", INK2), ("solid body", S2), ("chambered body", S3)]):
        c = 1.7 + 3.3 * i
        ax.add_patch(Polygon([(c - 1.15, 0.5), (c + 1.15, 0.5), (c, 2.6)], closed=True,
                             fc="none" if i == 0 else STONE, ec=col, ls="--" if i == 0 else "-", lw=1.8))
        ax.plot([c - 1.15 * (1 - u0), c + 1.15 * (1 - u0)], [yy, yy], color=S3, lw=2)
        ax.text(c, 0.12, name, ha="center", fontweight="bold", fontsize=10)
        if i == 2:
            ax.add_patch(Rectangle((c - 0.25, yy), 0.5, 0.19, fc=BG0, ec=S3, lw=1.2))
    ax.set_title("A geometric cut is not a material interface", loc="left")
    save(fig, P, "fig3_virtual_solid_chambered")


def gp7():
    P = "gp7-chamber-spectral-selection"
    L, W, Hh = np.array([412.24, 206.12, 230.09]) * 0.0254
    cs = 343.0
    ideal = np.array([L, L / 2, L * np.sqrt(5) / 4]); actual = np.array([L, W, Hh])
    freq = lambda n, d: cs / 2 * np.linalg.norm(np.array(n) / d)
    fig, ax = plt.subplots(figsize=(8.0, 4.0))
    modes = [n for n in product(range(9), repeat=3) if any(n) and freq(n, actual) <= 120]
    cols = [S1, S3, S2]
    for n in modes:
        k = sum(v > 0 for v in n)
        ax.vlines(freq(n, actual), k - 0.29, k + 0.29, color=cols[k - 1], lw=1.4)
    counts = [sum(sum(v > 0 for v in n) == k for n in modes) for k in (1, 2, 3)]
    ax.set_yticks([1, 2, 3]); ax.set_yticklabels([f"axial ({counts[0]})", f"tangential ({counts[1]})", f"oblique ({counts[2]})"])
    ax.set_xlabel("ideal rigid-wall acoustic frequency (Hz)"); ax.set_xlim(0, 122); ax.set_ylim(0.45, 3.55)
    ax.grid(axis="y", visible=False)
    ax.set_title(f"The complete King's Chamber mode spectrum to 120 Hz: {len(modes)} modes (c = 343 m/s)", loc="left")
    save(fig, P, "fig1_complete_mode_spectrum")

    pairs = [((2, 2, 1), (4, 1, 1)), ((2, 2, 2), (4, 1, 2)), ((3, 1, 3), (5, 1, 2))]
    fig, ax = plt.subplots(figsize=(8.0, 3.6))
    for i, (a, b) in enumerate(pairs):
        fi = freq(a, ideal)
        sh = (np.array([freq(a, actual), freq(b, actual)]) - fi) * 1000
        ax.plot(sh, [i, i], color=MUTED, lw=2)
        ax.scatter(sh, [i, i], color=[S1, S3], s=60, zorder=3)
        ax.text(max(sh) + 4, i, f"split {abs(sh[0] - sh[1]):.1f} mHz", va="center", fontsize=9)
    ax.axvline(0, ls=":", color=INK2, lw=0.8)
    ax.set_yticks(range(3)); ax.set_yticklabels([f"{a} / {b}" for a, b in pairs]); ax.invert_yaxis()
    ax.set_xlabel("shift from the ideal 20 : 10 : 5√5 pair frequency (mHz)"); ax.set_xlim(-5, 195)
    ax.grid(axis="y", visible=False)
    ax.set_title("Which ideal degeneracies survive the surveyed geometry?", loc="left")
    save(fig, P, "fig2_degeneracy_splitting")

    fig, axes = plt.subplots(1, 3, figsize=(9.0, 3.0))
    X, Y = np.meshgrid(np.linspace(0, 1, 150), np.linspace(0, 1, 90))
    for ax, n in zip(axes, [(1, 0), (2, 1), (3, 2)]):
        Z = np.cos(n[0] * np.pi * X) * np.cos(n[1] * np.pi * Y)
        ax.imshow(Z, extent=(0, 2, 0, 1), origin="lower", cmap="RdBu_r", vmin=-1, vmax=1)
        ax.set_title(f"mode ({n[0]}, {n[1]}, 0)", fontsize=10); ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
        ax.set_xlabel(f"x parity {'even' if n[0] % 2 == 0 else 'odd'} · y parity {'even' if n[1] % 2 == 0 else 'odd'}", fontsize=9)
    fig.suptitle("Mode parity is fixed by the rectangular shape", x=0.02, ha="left", fontsize=11, fontweight="bold", color=INK)
    fig.tight_layout(); save(fig, P, "fig3_mode_parity")


def gp8():
    P = "gp8-reciprocal-resonator-matching"
    fig, ax = plt.subplots(figsize=(8.0, 3.6)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 4)
    for cx, name in [(1.7, "terminal A"), (8.3, "terminal B")]:
        ax.add_patch(Polygon([(cx - 1.15, 1), (cx + 1.15, 1), (cx, 3.3)], closed=True, fc=STONE, ec=S2, lw=1.8))
        ax.add_patch(Rectangle((cx - 0.22, 1.66), 0.44, 0.19, fc=S3, ec=BG0))
        ax.text(cx, 0.62, name, ha="center", fontsize=10, fontweight="bold")
    for y, col in [(2.2, S1), (1.65, S3)]:
        ax.add_patch(FancyArrowPatch((2.95, y), (7.05, y), arrowstyle="<->", mutation_scale=14, color=col, lw=1.8))
    ax.text(5, 2.6, "specified reciprocal field", ha="center", fontsize=10)
    ax.text(5, 1.1, "G(ω; x, y) = G(ω; y, x)", ha="center", fontsize=10)
    ax.text(5, 0.2, "matching selects a response; propagation supplies the channel", ha="center", color=INK2, fontsize=9)
    ax.set_title("Two resonators coupled through a physical field", loc="left")
    save(fig, P, "fig1_reciprocal_channel")

    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    d = np.logspace(0, 5, 400)
    ax.loglog(d, 1 / d, color=S1, lw=2, label="amplitude ∝ 1/R")
    ax.loglog(d, 1 / d ** 2, color=S3, lw=2, label="intensity ∝ 1/R²")
    ax.set_xlabel("distance / reference distance"); ax.set_ylabel("relative free-space response")
    ax.legend(loc="lower left"); ax.grid(True, which="both", alpha=0.6)
    ax.set_title("Conventional propagation baseline", loc="left")
    save(fig, P, "fig2_range_baseline")

    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    u = np.linspace(0, 2, 500)
    for D, col in [(0, S3), (2, S1), (6, S2)]:
        Om = np.sqrt(D ** 2 + 4)
        ax.plot(u, 4 / (D ** 2 + 4) * np.sin(Om * u * np.pi / 2) ** 2, color=col, lw=1.8, label=f"|Δ|/|κ| = {D}")
    ax.set_xlabel("normalised time |κ|t/π"); ax.set_ylabel("transfer probability"); ax.set_ylim(0, 1.05)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3)
    ax.set_title("GP-5 applied to a calibrated coherent coupling", loc="left")
    save(fig, P, "fig3_transfer_detuning")


if __name__ == "__main__":
    for fn in (gp1, gp2, gp3, gp4, gp5, gp6, gp7, gp8):
        fn()
