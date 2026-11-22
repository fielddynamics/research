"""Figures for 'The SST Khronon': the mountain, the slope and the dimple.

Figure 1 (fig_zoom.pdf): the Milky Way's potential seen at three zooms.
  (a) the whole mountain, 0-25 kpc, as seen from another galaxy;
  (b) +-1.5 Jacobi radii around the Sun: the mountain is a flat slope, and the Sun a thin dimple;
  (c) +-50 AU: only the Sun's dimple; the slope's tilt across it is invisible.
Figure 2 (fig_scales.pdf): which acceleration dominates at each distance from the Sun.

Model: flat rotation curve v = 220 km/s with a 2 kpc core, Sun at R0 = 8.2 kpc;
Omega = v/R0; tide of a flat curve 2 Omega^2 r; Jacobi radius r_J^3 = GM/(2 Omega^2).
Run: python make_figures.py"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# palette: categorical slots 1-4 of the validated reference palette, text inks, surface
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d9d8d4"
plt.rcParams.update({"font.size": 8, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.linewidth": 0.6, "lines.linewidth": 2.0, "font.family": "serif"})

GM, AU, PC, KPC = 1.32712e20, 1.495979e11, 3.0857e16, 3.0857e19
a0, v, R0, Rc = 1.2e-10, 2.2e5, 8.2 * KPC, 2.0 * KPC
Om = v / R0
gal = lambda R: 0.5 * v ** 2 * np.log(R ** 2 + Rc ** 2)                    # m^2/s^2
g_gal = v ** 2 * R0 / (R0 ** 2 + Rc ** 2)                                  # field at the Sun
rJ = (GM / (2 * Om ** 2)) ** (1 / 3)
KM2 = 1e6                                                                  # (km/s)^2

def clean(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color=GRID, linewidth=0.4)

# ---------------------------------------------------------------- Figure 1
fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.3))
# (a) the mountain
R = np.linspace(0.05, 25, 600) * KPC
ax = axs[0]
ax.plot(R / KPC, (gal(R) - gal(25 * KPC)) / KM2, color=ORANGE)
ax.axvline(R0 / KPC, color=INK2, linewidth=0.6, linestyle=":")
ax.plot([R0 / KPC], [(gal(R0) - gal(25 * KPC)) / KM2], "o", color=BLUE, markersize=4)
ax.annotate("Sun", (R0 / KPC, (gal(R0) - gal(25 * KPC)) / KM2), xytext=(10.5, -150), color=INK, fontsize=7,
            arrowprops=dict(arrowstyle="-", color=INK2, linewidth=0.5))
ax.set_xlabel("distance from galactic centre (kpc)")
ax.set_ylabel(r"potential (km/s)$^2$")
ax.set_title("(a) seen from afar: the mountain", fontsize=8, color=INK, loc="left")
clean(ax)
# (b) the slope, +-1.5 r_J
d = np.linspace(-1.5, 1.5, 4001) * rJ
slope = (gal(R0 + d) - gal(R0)) / KM2
dimple = -GM / np.maximum(np.abs(d), 200 * AU) / KM2
ax = axs[1]
ax.plot(d / PC, slope, color=ORANGE, label="galaxy: flat slope")
ax.plot(d / PC, slope + dimple, color=BLUE, linewidth=1.2, label="slope + Sun's dimple")
for s in (-1, 1):
    ax.axvline(s * rJ / PC, color=INK2, linewidth=0.6, linestyle=":")
ax.text(rJ / PC * 1.03, 11, r"$r_J$", color=INK2, fontsize=7)
curv = 0.5 * abs(v ** 2 * (Rc ** 2 - R0 ** 2) / (R0 ** 2 + Rc ** 2) ** 2) * rJ ** 2 / (g_gal * rJ)
ax.text(-1.45, 9.5, f"curvature across $r_J$:\n{curv:.0e} of the tilt", fontsize=6.5, color=INK2, va="top")
ax.set_ylim(-14, 14)
ax.set_xlabel("distance from the Sun (pc)")
ax.set_title("(b) zoom to $r_J$: a flat slope", fontsize=8, color=INK, loc="left")
ax.legend(frameon=False, fontsize=6.5, loc="lower right")
clean(ax)
# (c) the dimple, +-50 AU
d2 = np.linspace(-50, 50, 4001) * AU
ax = axs[2]
tilt = g_gal * d2 / KM2
ax.plot(d2 / AU, -GM / np.maximum(np.abs(d2), 0.3 * AU) / KM2 + tilt, color=BLUE)
ax.set_ylim(-900, 30)
ratio = g_gal * 50 * AU / (GM / (50 * AU))
ax.text(-49, -700, f"slope's tilt\nhere: {ratio:.0e}\nof the depth", fontsize=6.5, color=INK2)
ax.set_xlabel("distance from the Sun (AU)")
ax.set_title("(c) the planets: a dimple", fontsize=8, color=INK, loc="left")
clean(ax)
fig.tight_layout(w_pad=1.0)
fig.savefig("fig_zoom.pdf"); fig.savefig("fig_zoom.png", dpi=200)

# ---------------------------------------------------------------- Figure 2
r = np.logspace(np.log10(0.5 * AU), np.log10(30 * PC), 400)
fig, ax = plt.subplots(figsize=(3.4, 2.6))
ax.axvspan(r[0] / AU, rJ / AU, color="#f0efec", zorder=0)
ax.loglog(r / AU, GM / r ** 2, color=BLUE)
ax.loglog(r / AU, np.full_like(r, g_gal), color=ORANGE)
ax.loglog(r / AU, 2 * Om ** 2 * r, color=AQUA)
ax.loglog(r / AU, np.full_like(r, a0), color=YELLOW, linestyle=(0, (4, 2)), linewidth=1.6)
ax.axvline(rJ / AU, color=INK2, linewidth=0.6, linestyle=":")
ax.text(1.2, 2e-3, "Sun's pull (dimple)", color=INK, fontsize=6.5)
ax.text(1.2, 1.2e-9, "galaxy's slope: cancels in free fall", color=INK, fontsize=6.5)
ax.text(1.2, 8e-13, "tail if $\\mu$ read the dimple (excluded)", color=INK, fontsize=6.5)
ax.text(1.2, 3e-19, "tide", color=INK, fontsize=6.5)
ax.text(rJ / AU * 1.15, 1e-4, "$r_J$", color=INK2, fontsize=7)
ax.text(3, 4e-16, "inside: flat slope\n+ drainless dimple\n(pure TetA)", color=INK2, fontsize=6.5)
ax.text(rJ / AU * 1.3, 2e-20, "outside:\nthe mountain\n($\\mu$ acts)", color=INK2, fontsize=6.5)
ax.set_xlabel("distance from the Sun (AU)")
ax.set_ylabel("acceleration (m/s$^2$)")
ax.set_ylim(1e-20, 1e-1)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(color=GRID, linewidth=0.4, which="major")
fig.tight_layout()
fig.savefig("fig_scales.pdf"); fig.savefig("fig_scales.png", dpi=200)
print(f"r_J = {rJ / PC:.2f} pc = {rJ / AU:.3g} AU; g_gal = {g_gal:.3g} m/s^2; curvature/tilt across r_J = {curv:.1e}; "
      f"tilt/depth at 50 AU = {ratio:.1e}")
