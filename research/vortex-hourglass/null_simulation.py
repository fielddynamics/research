"""
Null simulation for the measured partition (T2, T3): galaxies that obey mu(x) exactly.

For every point of the 149 quality-cut SPARC galaxies, g_bar is SPARC's own Newtonian value and
g_obs is generated from mu(x) = x/(x+1) exactly (g_obs = (g_bar + sqrt(g_bar^2 + 4 g_bar a0))/2).
Measurement scatter is then added to g_obs only: each point's own velocity error (2 log10(1 + e/v),
capped at e/v = 0.5) and a per-galaxy offset of 0, 0.05 or 0.10 dex (distance, inclination).
The same binning (measured_partition.binned, cross_half) is run on the simulated data.

If the simulated "slip" and crossing match the measured ones, those features are what binning on a
noisy g_obs produces (the same error enters x = g_obs/a0 and mu_obs = g_bar/g_obs), and are not
evidence of a departure from mu(x).

Adapted from the independent review (2026-11-14). Usage: python null_simulation.py ROTMOD_DIR [RESULTS_DIR]
"""
from __future__ import annotations

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import measured_partition as mp  # noqa: E402

A0, KPC = 1.2e-10, 3.086e19


def main(rotmod_dir, res):
    D = mp.load(res)
    T = mp.load_thin_disk(D, rotmod_dir)
    ev = {}
    for g in T:
        a = np.loadtxt(os.path.join(rotmod_dir, f"{g}_rotmod.dat"), ndmin=2)
        gb = (np.abs(a[:, 3]) * a[:, 3] + 0.5 * a[:, 4] ** 2 + 0.7 * a[:, 5] ** 2) * 1e6 / (a[:, 0] * KPC)
        ev[g] = (a[:, 1], a[:, 2], gb)

    def run(sig_gal, seed):
        rng = np.random.default_rng(seed)
        LX, MU = [], []
        for v, e, gb in ev.values():
            ok = gb > 0
            gt = (gb + np.sqrt(gb ** 2 + 4 * gb * A0)) / 2
            lerr = 2 * np.log10(1 + np.clip(e / np.maximum(v, 1), 0, 0.5))
            go = gt * 10 ** (rng.normal(0, 1, len(gt)) * lerr + rng.normal(0, sig_gal))
            LX.append(np.log10(go[ok] / A0)); MU.append(gb[ok] / go[ok])
        lx, mu = np.concatenate(LX), np.concatenate(MU)
        s = (mu > 0) & (mu < 1)
        c2, m2, _, _ = mp.binned(lx[s], np.log10(mu[s] / (1 - mu[s])) - lx[s])
        c1, m1, _, _ = mp.binned(lx, mu)
        return mp.cross_half(lx, mu), dict(zip(np.round(c2, 2), m2)), dict(zip(np.round(c1, 2), np.abs(2 * m1 - 1)))

    print("Null model: mu(x) exact, scatter in g_obs only; 20 realisations each; medians shown")
    for sg in (0.0, 0.05, 0.10):
        xs, sl, gp = [], [], []
        for k in range(20):
            x0, d, gap = run(sg, k)
            xs.append(x0); sl.append(d); gp.append(gap)
        keys = sorted(set().union(*sl)); gk = sorted(set().union(*gp))
        print(f"  per-galaxy scatter {sg:.2f} dex: crossing x = {10 ** np.median(xs):.2f}")
        print("    slip log10(Omega/x): " + "  ".join(f"{k:+.2f}:{np.median([s[k] for s in sl if k in s]):+.3f}" for k in keys))
        print("    gap |2mu-1|:         " + "  ".join(f"{k:+.2f}:{np.median([s[k] for s in gp if k in s]):.2f}" for k in gk))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "decode_audit", "results_paper_mphot"))
