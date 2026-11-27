"""Recreate all figures (PNG + SVG) and the output ledgers from antenna_engine."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import antenna_engine as ae

HERE = Path(__file__).resolve().parent
FIG = HERE / "figures"
OUT = HERE / "outputs"
FIG.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

CA, CO, CB, INK = "#2a6fdb", "#d1495b", "#3a9d5d", "#333333"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})


def save(fig, name):
    for ext in ("png", "svg"):
        fig.savefig(FIG / f"{name}.{ext}", dpi=160, bbox_inches="tight")
    plt.close(fig)


# 01 coupling graph -------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 4))
ax.set_xlim(0, 10); ax.set_ylim(-0.5, 4.5); ax.axis("off")
for n in range(4):
    y = 3.6 - n * 1.1
    ax.add_patch(plt.Circle((1.5, y), 0.32, color=CA))
    ax.text(1.5, y, f"A{n}", ha="center", va="center", color="white", weight="bold")
    ax.text(0.4, y, f"{2**n}ω₀", ha="center", va="center", color=INK)
    ax.add_patch(plt.Circle((8.5, y), 0.32, color=CB))
    ax.text(8.5, y, f"B{n}", ha="center", va="center", color="white", weight="bold")
    ax.text(9.6, y, f"{2**n}ω₀", ha="center", va="center", color=INK)
    ax.plot([1.85, 4.55], [y, 1.95], color=INK, lw=1)
    ax.plot([5.45, 8.15], [1.95, y], color=INK, lw=1)
ax.add_patch(plt.Circle((5, 1.95), 0.5, color=CO))
ax.text(5, 1.95, "FO", ha="center", va="center", color="white", weight="bold")
ax.text(5, 1.05, "nonlinear vertex\nχ|o|²o (vortex core)", ha="center", va="top", fontsize=9)
ax.text(1.5, 4.35, "TetA spiral", ha="center", color=CA, weight="bold")
ax.text(8.5, 4.35, "TetB spiral", ha="center", color=CB, weight="bold")
ax.annotate("", xy=(7.6, 3.95), xytext=(2.4, 3.95),
            arrowprops=dict(arrowstyle="-", ls="--", color="#aaaaaa"))
ax.text(5, 4.1, "no A–B edge, no shared coordinate", ha="center", color="#888888", fontsize=9)
save(fig, "01_coupling_graph")

# 02 symmetric exact transfer --------------------------------------------
ts = np.linspace(0, 9, 600)
a, o, b = ae.symmetric_transfer_exact(1.0, ts)
fig, ax = plt.subplots(figsize=(7, 3.2))
ax.plot(ts, np.abs(a) ** 2, color=CA, label="TetA |a|²")
ax.plot(ts, np.abs(o) ** 2, color=CO, label="Field Origin |o|²")
ax.plot(ts, np.abs(b) ** 2, color=CB, label="TetB |b|²")
ax.axvline(np.pi / np.sqrt(2), color="#999", ls=":")
ax.set_xlabel("g t"); ax.set_ylabel("occupation"); ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.18))
ax.set_title("Resonant vertex: complete exchange at gt = π/√2", fontsize=10, pad=24)
save(fig, "02_resonant_exchange")

# 03 dispersive exchange --------------------------------------------------
v = ae.Vertex(g=0.1, wO=2.0)
ts = np.linspace(0, 700, 3000)
y = ae.evolve_linear_exact(v, [1, 0, 0], ts)
fig, ax = plt.subplots(figsize=(7, 3.2))
ax.plot(ts, np.abs(y[0]) ** 2, color=CA, label="TetA")
ax.plot(ts, np.abs(y[2]) ** 2, color=CB, label="TetB")
ax.plot(ts, np.abs(y[1]) ** 2, color=CO, label="Field Origin")
ax.set_xlabel("t (g = 0.1, origin detuned Δ = 2)"); ax.set_ylabel("occupation")
ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.18))
ax.set_title("Virtual vertex: full exchange, origin peak ≤ 1%", fontsize=10, pad=24)
save(fig, "03_virtual_vertex")

# 04 detuning selection ---------------------------------------------------
J = ae.effective_exchange(0.1, 2.0)
ds = np.linspace(-0.05, 0.05, 41)
tsd = np.linspace(0, 800, 8001)
num = [np.max(np.abs(ae.evolve_linear_exact(ae.Vertex(g=0.1, wO=2.0, wB=d), [1, 0, 0], tsd)[2]) ** 2) for d in ds]
dd = np.linspace(-0.05, 0.05, 400)
fig, ax = plt.subplots(figsize=(6.5, 3.2))
ax.plot(dd, [ae.rabi_max_transfer(J, d) for d in dd], color=INK, label="J²/(J²+(δ/2)²)")
ax.plot(ds, num, "o", color=CB, ms=4, label="three-mode model")
ax.set_xlabel("TetB detuning δ"); ax.set_ylabel("peak TetB occupation")
ax.legend(frameon=False); ax.set_title("Only matched modes exchange", fontsize=10)
save(fig, "04_detuning_selection")

# 05 nonlinear vertex share ----------------------------------------------
Ns = [0.01, 0.5, 1, 2, 4, 8, 16, 32, 64]
shares, halves = [], []
for N in Ns:
    t, yy = ae.evolve(ae.Vertex(g=1, chi=1.0), [np.sqrt(N), 0, 0], 120.0, 2e-3)
    fb = np.abs(yy[2]) ** 2 / N
    shares.append(np.max(np.abs(yy[1]) ** 2) / N)
    halves.append(t[np.argmax(fb >= 0.5)])
fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
ax[0].semilogx(Ns, shares, "o-", color=CO); ax[0].set_xlabel("inventory N"); ax[0].set_ylabel("peak Field Origin share")
ax[0].set_title("Vertex self-detunes", fontsize=10)
ax[1].semilogx(Ns, halves, "o-", color=CB); ax[1].set_xlabel("inventory N"); ax[1].set_ylabel("time to 50% in TetB")
ax[1].set_title("Exchange slows but still completes", fontsize=10)
save(fig, "05_nonlinear_vertex")
with open(OUT / "nonlinear_vertex.csv", "w") as f:
    f.write("N,peak_origin_share,t_half_transfer\n")
    for N, s, h in zip(Ns, shares, halves):
        f.write(f"{N},{s:.6f},{h:.4f}\n")

# 06 gasket vs ledger and band ladder ------------------------------------
fig, ax = plt.subplots(1, 3, figsize=(11, 3.4), gridspec_kw={"width_ratios": [1.1, 1.1, 1]})
for k, n in enumerate([3, 4]):
    pts = ae.gasket_points(n)
    xs = [c - r / 2 for r, c in pts]; ys = [-r for r, c in pts]
    ax[k].scatter(xs, ys, s=8 if n == 4 else 18, color=CA)
    ax[k].scatter([0], [0], s=60, color=CO, zorder=3)
    ax[k].set_aspect("equal"); ax[k].axis("off")
    ax[k].set_title(f"gasket level {n}: {3**n} sites\n(feed = red, self-similar about it)", fontsize=9)
lv = np.arange(5)
ax[2].semilogy(lv, [ae.gasket_triangles(n) for n in lv], "o-", color=CA, label="gasket 3ⁿ")
ax[2].semilogy(lv, [ae.ledger_addresses(n) for n in lv], "s-", color=CO, label="GFD ledger 4ⁿ")
ax[2].semilogy(lv, ae.band_ladder(5), "^-", color=CB, label="band 2ⁿω₀")
ax[2].set_xlabel("level n"); ax[2].legend(frameon=False, fontsize=8)
save(fig, "06_gasket_ledger_bands")

with open(OUT / "gasket_ledger.csv", "w") as f:
    f.write("level,gasket_3^n,ledger_4^n,area_(3/4)^n,edge_(1/2)^n,band_2^n\n")
    for n in range(6):
        f.write(f"{n},{ae.gasket_triangles(n)},{ae.ledger_addresses(n)},{ae.gasket_area(n)},{ae.edge_fraction(n)},{2**n}\n")
print("figures and outputs written")
