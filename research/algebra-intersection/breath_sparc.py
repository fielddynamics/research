"""
breath_sparc.py
===============

Computes pre-registration 3 (BREATH_SPARC_PREREG.md) exactly as registered.
"""
from __future__ import annotations

import csv
import os

import numpy as np

A0 = 1.2e-10
here = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(here, "..", "..", "papers", "letter-radial-acceleration-relation-sparc", "supplementary", "sparc_rar.csv")
rows = list(csv.DictReader(open(path)))
gbar = np.array([float(r["g_bar_ms2"]) for r in rows])
gobs = np.array([float(r["g_obs_ms2"]) for r in rows])
ngal = len({r["galaxy"] for r in rows})


def baseline(gb):
    return 0.5 * (gb + np.sqrt(gb * gb + 4 * gb * A0))


def breath(gb):
    """Exact solution of the registered equation mu(x) g_t = g_bar (x + 13/17)/(x + 1), x = g_t/a0.
    Multiplying out: g_t^2 - g_bar g_t - (13/17) g_bar a0 = 0."""
    gt = 0.5 * (gb + np.sqrt(gb * gb + 4 * (13 / 17) * gb * A0))
    x = gt / A0
    resid = (x / (x + 1)) * gt - gb * (x + 13 / 17) / (x + 1)
    assert np.all(np.abs(resid) <= 1e-12 * gb), "closed form does not satisfy the registered equation"
    return gt


def stats(pred):
    r = np.log10(gobs) - np.log10(pred)
    return r.mean(), r.std()


if __name__ == "__main__":
    print(f"data: {len(gbar)} points, {ngal} galaxies")
    mb, sb = stats(baseline(gbar))
    print(f"baseline (letter):  mean {mb:+.4f} dex, sigma {sb:.4f} dex   (letter: -0.027, 0.181)")
    mh, sh = stats(breath(gbar))
    print(f"H_breath:           mean {mh:+.4f} dex, sigma {sh:.4f} dex")
    d = sh - sb
    verdict = "SUPPORTED" if d < -0.002 else ("REJECTED" if d > 0.002 else "UNDECIDED")
    print(f"sigma_H - sigma_base = {d:+.4f} dex  ->  {verdict}")
    # where the two differ
    for lo, hi in ((1e-13, 1e-11), (1e-11, 1e-10), (1e-10, 1e-9), (1e-9, 1e-7)):
        m = (gbar >= lo) & (gbar < hi)
        if m.sum():
            rb = np.log10(gobs[m]) - np.log10(baseline(gbar[m]))
            rh = np.log10(gobs[m]) - np.log10(breath(gbar[m]))
            print(f"  g_bar in [{lo:.0e},{hi:.0e}): n={m.sum():4d}  mean resid base {rb.mean():+.3f}  breath {rh.mean():+.3f}")
