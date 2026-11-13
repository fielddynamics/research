"""Figure: Tully-Fisher velocity evolution with measurement uncertainties.
GFD prediction v(z)/v(0) = [H(z)/H0]^0.17 with its +/-6.2% band, LCDM (no evolution),
a0 proportional to H (exponent 1/4) for reference, and the nine IFU measurements with 1-sigma errors.
Lower panel: residuals in units of each measurement's sigma.
Run: python make_tf_figure.py   ->  tf-evolution-errors.png, tf-evolution-errors.pdf"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

Om, OL = 0.30, 0.70
H = lambda z: np.sqrt(Om * (1 + z) ** 3 + OL)
gfd = lambda z: H(z) ** 0.17
band = (4 / np.pi) ** 0.25           # +/-6.2% topological band

# z, v(z)/v(0), sigma, survey, marker
data = [
    (0.0, 1.00, 0.02, "Local calibration", "o"),
    (0.3, 1.04, 0.05, "Kassin+ 2007 (DEEP2)", "s"),
    (0.6, 1.06, 0.06, "Puech+ 2008 (IMAGES)", "D"),
    (0.9, 1.10, 0.07, "Kassin+ 2007 (DEEP2)", "s"),
    (1.0, 1.10, 0.06, "Miller+ 2011 (DEEP2)", "^"),
    (1.5, 1.13, 0.08, "Übler+ 2017 (KMOS$^{3D}$)", "v"),
    (2.0, 1.21, 0.09, "Cresci+ 2009 (SINS)", "p"),
    (2.2, 1.26, 0.10, "Straatman+ 2017 (ZFIRE)", "h"),
    (3.0, 1.29, 0.12, "Übler+ 2017 (KMOS$^{3D}$)", "v"),
]

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["DejaVu Serif"], "mathtext.fontset": "dejavuserif",
    "font.size": 10, "axes.linewidth": 0.8, "xtick.direction": "in", "ytick.direction": "in",
    "xtick.top": True, "ytick.right": True, "xtick.minor.visible": True, "ytick.minor.visible": True,
})
C_GFD, C_BAND, C_DATA, C_LCDM, C_ALT = "#1f4e9c", "#c9d8f0", "#b2470f", "#333333", "#8a8a8a"

fig, (ax, axr) = plt.subplots(2, 1, figsize=(9.6, 6.2), sharex=True,
                              gridspec_kw={"height_ratios": [3.2, 1], "hspace": 0.06})
zz = np.linspace(0, 4.2, 400)
ax.fill_between(zz, gfd(zz) / band, gfd(zz) * band, color=C_BAND, alpha=0.75, lw=0, zorder=1)
ax.plot(zz, gfd(zz), color=C_GFD, lw=2.0, zorder=3)
ax.plot(zz, H(zz) ** 0.25, color=C_ALT, lw=1.1, ls=(0, (1, 1.6)), zorder=2)
ax.axhline(1.0, color=C_LCDM, lw=1.1, ls="--", zorder=2)

seen = {}
for z, v, s, lab, m in data:
    h = ax.errorbar(z, v, yerr=s, fmt=m, ms=6, mfc=C_DATA, mec="white", mew=0.7, ecolor=C_DATA,
                    elinewidth=1.1, capsize=3, capthick=1.1, zorder=5)
    seen.setdefault(lab, h)
    axr.errorbar(z, (v - gfd(z)) / s, yerr=1, fmt=m, ms=5, mfc=C_DATA, mec="white", mew=0.6,
                 ecolor=C_DATA, elinewidth=1.0, capsize=2.5, zorder=5)
# SINS BX442: single galaxy, quoted without an uncertainty in the source table
ax.plot(2.18, 1.27, marker="*", ms=12, mfc="#2e8b57", mec="white", mew=0.6, ls="none", zorder=6)
ax.annotate("BX442 (single galaxy)", (2.18, 1.27), xytext=(2.45, 1.15), fontsize=8, color="#2e8b57",
            arrowprops=dict(arrowstyle="-", color="#2e8b57", lw=0.7))

ax.set_xlim(-0.1, 4.2); ax.set_ylim(0.9, 1.55)
ax.set_ylabel(r"$v(z)\,/\,v(0)$  at fixed baryonic mass")
ax.text(0.015, 0.975, r"GFD:  $v(z)/v(0) = [H(z)/H_0]^{0.17}$" "\n" r"$\Omega_m = 0.30,\ \Omega_\Lambda = 0.70$",
        transform=ax.transAxes, va="top", fontsize=9)

# chi-square summary (8 points beyond the local anchor)
pts = [(z, v, s) for z, v, s, *_ in data if z > 0]
chi = lambda f: sum(((v - f(z)) / s) ** 2 for z, v, s in pts)
ax.text(0.985, 0.03,
        "$\\chi^2$ (8 points, $z>0$)\n"
        f"GFD, exponent 0.17:  {chi(gfd):.2f}\n"
        f"$a_0\\propto H$, exponent 1/4:  {chi(lambda z: H(z)**0.25):.2f}\n"
        f"No evolution ($\\Lambda$CDM):  {chi(lambda z: 1.0):.2f}",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=8,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#bbbbbb", lw=0.6))

model_handles = [
    Line2D([], [], color=C_GFD, lw=2.0, label="GFD prediction"),
    plt.Rectangle((0, 0), 1, 1, fc=C_BAND, ec="none", label=r"GFD band $\pm6.2\%$, $(4/\pi)^{1/4}$"),
    Line2D([], [], color=C_ALT, lw=1.1, ls=(0, (1, 1.6)), label=r"$a_0 \propto H$ (exponent 1/4)"),
    Line2D([], [], color=C_LCDM, lw=1.1, ls="--", label=r"$\Lambda$CDM / constant $a_0$"),
]
leg1 = ax.legend(handles=model_handles, loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=8, frameon=False,
                 title="Models", title_fontsize=8.5, alignment="left")
ax.add_artist(leg1)
data_handles = [Line2D([], [], marker=h.lines[0].get_marker(), ls="none", mfc=C_DATA, mec="white", ms=6, label=l)
                for l, h in seen.items()]
data_handles.append(Line2D([], [], marker="*", ls="none", mfc="#2e8b57", mec="white", ms=10, label="SINS BX442 (no $\\sigma$ quoted)"))
ax.legend(handles=data_handles, loc="upper left", bbox_to_anchor=(1.02, 0.55), fontsize=8, frameon=False,
          title=r"IFU measurements ($\pm1\sigma$)", title_fontsize=8.5, handletextpad=0.4, alignment="left")

axr.axhspan(-1, 1, color="#eeeeee", zorder=0)
axr.axhline(0, color=C_GFD, lw=1.2)
axr.set_ylim(-2.2, 2.2); axr.set_yticks([-2, -1, 0, 1, 2])
axr.set_ylabel(r"(obs $-$ GFD)$/\sigma$", fontsize=9)
axr.set_xlabel("Redshift $z$")

fig.align_ylabels([ax, axr])
fig.savefig("tf-evolution-errors.png", dpi=300, bbox_inches="tight")
fig.savefig("tf-evolution-errors.pdf", bbox_inches="tight")
print("chi2:", round(chi(gfd), 2), round(chi(lambda z: H(z)**0.25), 2), round(chi(lambda z: 1.0), 2))
