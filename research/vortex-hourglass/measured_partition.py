"""
The red and blue discs, measured.

Letter 3's Figure 2 draws the two shares as surfaces of revolution: blue mu(x) (TetA) and red
1 - mu(x) (TetB), touching on the ring x = 1. Here the same surfaces are built from SPARC.

At every radius of the decode audit (version 2: the letter's pipeline and photometric mass),
  g_obs = v^2 / r          (smoothed velocity, as the letter decodes)
  g_bar = G M_phot / r^2   (the same spherical relation the decode uses)
  measured TetA share  mu_obs = g_bar / g_obs,   TetB share 1 - mu_obs
  measured roll ratio  Omega_obs = mu_obs / (1 - mu_obs)    (no slip at the measured radii)
Theory: mu(x) = x/(x+1), Omega = x, ring at x = 1.

Tests (exploratory; the forms are the theorem's own, nothing is fitted):
  T1  where the measured surfaces cross (median mu_obs = 1/2), against x = 1, with a bootstrap
      over galaxies;
  T2  the gap between the measured surfaces, |2 mu_obs - 1|, against |2 mu - 1| = |delta/omega_bar|;
  T3  the slip: median log10(Omega_obs / x) by x (zero everywhere if the chambers roll without slip
      at mu(x)). Note Delta = log10(M_dec/M_phot) = log10(mu(x)/mu_obs): Delta > 0 is a TetB share
      larger than mu predicts, Omega_obs < x.
Outputs a figure: theory and measured surfaces of revolution, and the shares against log10 x.

Usage: python measured_partition.py [RESULTS_DIR] [OUT_PNG] [ROTMOD_DIR for the thin-disk diagnostic]
"""
from __future__ import annotations

import csv
import os
import sys

import numpy as np

A0, KPC, MSUN, G = 1.2e-10, 3.086e19, 1.989e30, 6.674e-11
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(2026)
EDGES = np.arange(-1.5, 1.75, 0.25)


def load(res):
    S = {r["galaxy"]: r for r in csv.DictReader(open(os.path.join(res, "galaxy_summary.csv")))}
    q = {k for k, r in S.items() if int(r["Q"]) in (1, 2) and float(r["inc"]) >= 30 and int(r["n"]) >= 5}
    P = {}
    for r in csv.DictReader(open(os.path.join(res, "profiles.csv"))):
        if r["galaxy"] in q:
            P.setdefault(r["galaxy"], []).append(r)
    out = {}
    for g, rows in P.items():
        R = np.array([float(p["r_kpc"]) for p in rows]) * KPC
        v = np.array([float(p["v_smooth"]) for p in rows]) * 1e3
        gobs = v ** 2 / R
        gbar = G * np.array([float(p["M_phot"]) for p in rows]) * MSUN / R ** 2
        out[g] = dict(lx=np.log10(gobs / A0), mu=gbar / gobs, gas=float(S[g]["gas_share"]))
    return out


def binned(lx, y):
    cen, med, lo, hi = [], [], [], []
    for a, b in zip(EDGES[:-1], EDGES[1:]):
        s = (lx >= a) & (lx < b)
        if s.sum() >= 20:
            cen.append(0.5 * (a + b)); med.append(np.median(y[s]))
            lo.append(np.percentile(y[s], 16)); hi.append(np.percentile(y[s], 84))
    return np.array(cen), np.array(med), np.array(lo), np.array(hi)


def cross_half(lx, mu):
    cen, med, _, _ = binned(lx, mu)
    for i in range(len(med) - 1):
        if med[i] < 0.5 <= med[i + 1]:
            return cen[i] + (0.5 - med[i]) * (cen[i + 1] - cen[i]) / (med[i + 1] - med[i])
    return np.nan


def analyse(D, label):
    gal = sorted(D)
    lx = np.concatenate([D[g]["lx"] for g in gal]); mu = np.concatenate([D[g]["mu"] for g in gal])
    ok = (mu > 0) & (mu < 1)
    print(f"{label}: {len(gal)} galaxies, {len(mu)} points ({(~ok).sum()} with mu_obs outside (0,1), "
          f"kept for the median, excluded from Omega)")
    x0 = cross_half(lx, mu)
    boot = []
    for _ in range(2000):
        b = rng.choice(len(gal), len(gal))
        boot.append(cross_half(np.concatenate([D[gal[i]]["lx"] for i in b]), np.concatenate([D[gal[i]]["mu"] for i in b])))
    boot = np.array(boot); boot = boot[np.isfinite(boot)]
    lo, hi = np.percentile(boot, [2.5, 97.5])
    print(f"  T1 measured surfaces cross (median mu_obs = 1/2) at log10 x = {x0:+.2f} (x = {10 ** x0:.2f}); "
          f"95% interval x {10 ** lo:.2f}-{10 ** hi:.2f}; theory x = 1: {'inside' if lo <= 0 <= hi else 'outside'}")
    cen, med, _, _ = binned(lx, mu)
    th = 10 ** cen / (1 + 10 ** cen)
    print("  T2 gap |2mu-1|, measured (theory):  " + "  ".join(
        f"{c:+.2f}: {abs(2 * m - 1):.2f} ({abs(2 * t - 1):.2f})" for c, m, t in zip(cen, med, th)))
    slip = np.log10(mu[ok] / (1 - mu[ok])) - lx[ok]
    c2, m2, _, _ = binned(lx[ok], slip)
    print("  T3 slip median log10(Omega_obs / x):  " + "  ".join(f"{c:+.2f}: {m:+.3f}" for c, m in zip(c2, m2)))
    return lx, mu, cen, med


def figure(D, out_png, T=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    def series(DD):
        gal = sorted(DD)
        lx = np.concatenate([DD[g]["lx"] for g in gal]); mu = np.concatenate([DD[g]["mu"] for g in gal])
        cen, med, lo, hi = binned(lx, mu)
        n = np.array([((lx >= c - 0.125) & (lx < c + 0.125)).sum() for c in cen])
        k = n >= 100
        return cen[k], med[k], lo[k], hi[k], cross_half(lx, mu)

    sets = [("SPARC, the letter's photometric mass (spherical G M_phot/r^2)", series(D))]
    if T:
        sets.append(("SPARC, SPARC's own Newtonian g_bar (thin disks, HI maps)", series(T)))
    fig, axs = plt.subplots(len(sets) + 2, 1, figsize=(9, 3.1 * (len(sets) + 2)),
                            gridspec_kw=dict(height_ratios=[1] * (len(sets) + 1) + [1.4]))
    rr = np.linspace(0, 3, 300); xt = 10 ** (1.5 - rr); mt = xt / (1 + xt)
    panels = [("Theory (Letter 3): blue mu(x), red 1 - mu(x)", rr, mt, 1.5)]
    panels += [(lab + ": medians", 1.5 - c, m, 1.5 - x0) for lab, (c, m, lo, hi, x0) in sets]
    for ax, (title, r, m, ring) in zip(axs[:-1], panels):
        for sgn in (1, -1):
            ax.plot(sgn * r, m, color="#3b6fd1", lw=2.5)
            ax.plot(sgn * r, 1 - m, color="#d1514b", lw=2.5)
            ax.fill_between(sgn * r, m, 1 - m, color="0.85", alpha=0.6)
            ax.plot([sgn * ring], [0.5], "o", ms=9, mfc="white", mec="k")
            ax.axvline(sgn * 1.5, color="0.6", ls="--", lw=0.8)
        ax.set_title(title, fontsize=9)
        ax.set_xlim(-3.1, 3.1); ax.set_ylim(0, 1); ax.set_ylabel("share")
        ax.set_xticks([-3, -1.5, 0, 1.5, 3]); ax.set_xticklabels(["rim", "x = 1", "centre", "x = 1", "rim"])
    ax = axs[-1]
    xx = np.linspace(-1.6, 1.6, 300); m = 10 ** xx / (1 + 10 ** xx)
    ax.plot(xx, m, color="#3b6fd1", lw=2, label="theory mu(x)")
    ax.plot(xx, 1 - m, color="#d1514b", lw=2, label="theory 1 - mu(x)")
    for (lab, (c, md, lo, hi, x0)), mk in zip(sets, ("o", "s")):
        short = "letter's M_phot" if "letter" in lab else "SPARC g_bar"
        ax.plot(c, md, mk, color="#1f3f80", mfc="none" if mk == "o" else "#1f3f80", label=f"mu_obs, {short} (crossing x = {10 ** x0:.2f})")
        ax.plot(c, 1 - md, mk, color="#802520", mfc="none" if mk == "o" else "#802520")
    ax.axvline(0, color="0.5", ls="--", lw=0.8); ax.axhline(0.5, color="0.7", lw=0.6)
    ax.set_xlabel("log10 x   (x = g_obs/a0;  centre = high x at left, rim at right)")
    ax.set_ylabel("share"); ax.set_ylim(-0.05, 1.05); ax.set_xlim(1.6, -1.6); ax.legend(fontsize=7, loc="center right")
    fig.suptitle("Letter 3's red and blue discs: theory and SPARC (149 galaxies; white = where the shares meet; "
                 "dashed = x = 1; bins with >= 100 points)", fontsize=9)
    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
    print(f"\nFigure: {out_png}")


def load_thin_disk(D, rotmod_dir):
    """Diagnostic only: replace the spherical g_bar = G M_phot / r^2 by SPARC's thin-disk Newtonian
    g_bar = (|Vgas| Vgas + 0.5 Vdisk^2 + 0.7 Vbul^2) / r from the mass-model files."""
    import glob
    out = {}
    names = {os.path.basename(f)[:-len("_rotmod.dat")]: f for f in glob.glob(os.path.join(rotmod_dir, "*_rotmod.dat"))}
    for g, d in D.items():
        if g not in names:
            continue
        a = np.loadtxt(names[g], comments="#", ndmin=2)
        R = a[:, 0] * KPC
        gbar = (np.abs(a[:, 3]) * a[:, 3] + 0.5 * a[:, 4] ** 2 + 0.7 * a[:, 5] ** 2) * 1e6 / R
        if len(gbar) != len(d["lx"]):
            continue
        gobs = A0 * 10 ** d["lx"]
        out[g] = dict(lx=d["lx"], mu=gbar / gobs, gas=d["gas"])
    return out


def main(res, out_png, rotmod_dir=None):
    D = load(res)
    analyse(D, "all quality-cut")
    print()
    analyse({g: d for g, d in D.items() if d["gas"] < 0.5}, "not gas-dominated")
    if rotmod_dir:
        print("\nDIAGNOSTIC (not the letter's method): SPARC thin-disk g_bar instead of the spherical G M_phot / r^2")
        T = load_thin_disk(D, rotmod_dir)
        analyse(T, "all quality-cut, thin-disk g_bar")
        print()
        analyse({g: d for g, d in T.items() if d["gas"] < 0.5}, "not gas-dominated, thin-disk g_bar")
    else:
        T = None
    figure(D, out_png, T)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "decode_audit", "results_paper_mphot"),
         sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "measured_partition.png"),
         sys.argv[3] if len(sys.argv) > 3 else None)
