#!/usr/bin/env python3
"""Generate the figures embedded in the GP-1 ... GP-5 READMEs.

    python make_figures.py          # writes gp*/figures/*.svg

Every curve is computed here from the formulas proved and checked in the
proofs (nothing is hand-drawn). Static SVG on a white surface, so the figures
read the same in light and dark GitHub themes. Palette: the reference
categorical slots 1-3 (blue, orange, aqua), text in neutral inks.
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
S1, S2, S3, S4 = "#257de0", "#f47230", "#00b894", "#6a4ce2"   # blue, orange, aqua, violet
INK, INK2, GRID, SURF = "#191919", "#666666", "#e6e6e6", "#ffffff"

plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
    "axes.edgecolor": INK2, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.8, "axes.spines.top": False, "axes.spines.right": False,
    "lines.linewidth": 1.6, "font.size": 10, "axes.titlesize": 11, "axes.titleweight": "bold",
    "legend.frameon": False, "svg.fonttype": "path",
})


def save(fig, proof, name):
    out = HERE / proof / "figures"
    out.mkdir(exist_ok=True)
    fig.savefig(out / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)
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
    ax.fill([-1, 1, 0], [0, 0, 1], color="#f3f3f3", ec=INK2, lw=1.2)
    levels = [(1 - 2 ** (-1 / 3), "volume halved", S3), (U3, "section area halved (uniform flux)", S1), (0.5, "height halved", S2)]
    for lv, lab, col in levels:
        w = 1 - lv
        ax.plot([-w, w], [lv, lv], color=col, lw=2)
        ax.text(1.05 * w + 0.03, lv, f"u = {lv:.4f}  {lab}", va="center", color=INK, fontsize=9)
    ax.fill([-(1 - U3), 1 - U3, 0], [U3, U3, 1], color=S1, alpha=0.10)
    kc = 1692.55 / H_IN
    ax.plot([-0.08, 0.08], [kc, kc], color=INK, lw=3, solid_capstyle="butt")
    ax.annotate("King's Chamber floor (Petrie)\n1692.55 in = 0.29303 h", xy=(-0.08, kc), xytext=(-1.95, 0.40),
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
    ax.axvspan(1691.4, 1693.7, color="#f3f3f3", zorder=0)
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
             ("gravity budget, original (8πGρR_c)", 0.356, "#9c9c9c"),
             ("observed residual", 0.80, S2),
             ("height-reconstruction allowance", 2.05, "#9c9c9c")]
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
    ax.imshow(Mmask, cmap=matplotlib.colors.ListedColormap(["#f3f3f3", S1]), aspect="equal")
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
        ax.text(20.6, 0.85, lab, ha="right", fontsize=9)
    axs[2].set_xlabel("address offset d"); axs[2].set_xticks(range(0, 21, 7))
    axs[0].set_title("Complementary reconstruction of the exact 21-address selector", loc="left")
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


if __name__ == "__main__":
    for fn in (gp1, gp2, gp3, gp4, gp5):
        fn()
