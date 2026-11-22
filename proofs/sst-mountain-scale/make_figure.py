"""Figure for 'The Mountain Scale in the SST': the extra pull around the Sun in the 3D solutions, read pointwise
(the tail, a0 mu(x); demo_output.txt) and by ownership (no tail; demo_ownership_output.txt). Run: python make_figure.py"""
import re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d9d8d4"
plt.rcParams.update({"font.size": 8, "font.family": "serif", "axes.edgecolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.linewidth": 0.6})
txt = open("demo_output.txt").read()
rows = re.findall(r"(mountain|pointwise)\s+r = (\d+): extra pull toward the Sun = ([+-][0-9.]+) a0 \(Sun's own Newtonian pull ([0-9.]+)", txt)
fig, ax = plt.subplots(figsize=(3.4, 2.4))
r = [int(a) for n, a, v, o in rows if n == "pointwise"]; v = [float(v) for n, a, v, o in rows if n == "pointwise"]
ax.plot(r, v, "o-", color=ORANGE, linewidth=2, markersize=5)
own = open("demo_ownership_output.txt").read()
ro = re.findall(r"ownership r = (\d+): extra pull toward the Sun = ([+-][0-9.]+)", own)
ax.plot([int(a) for a, b in ro], [float(b) for a, b in ro], "o-", color=BLUE, linewidth=2, markersize=5)
rr = np.array(r); oo = np.array([float(o) for n, a, v, o in rows if n == "pointwise"])
ax.plot(rr, oo / (1 + oo), color=INK2, linewidth=1, linestyle=(0, (3, 2)))
ax.text(2.1, 0.86, "read pointwise: the tail", color=INK, fontsize=7)
ax.text(4.7, 0.58, "$a_0\\mu(x)$", color=INK2, fontsize=7)
ax.text(2.1, 0.08, "read by ownership: no tail", color=INK, fontsize=7)
ax.set_xlabel("distance from the Sun (box units; sphere $R = 10$)")
ax.set_ylabel("extra pull toward the Sun ($a_0$)")
ax.set_ylim(0, 1.0)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(color=GRID, linewidth=0.4)
fig.tight_layout()
fig.savefig("fig_demo.pdf"); fig.savefig("fig_demo.png", dpi=200)
