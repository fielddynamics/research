#!/usr/bin/env python3
"""
SPARC Radial Acceleration Relation plot via Field Dynamics API.

Fetches the SPARC catalog, pulls rotation-curve data for each galaxy,
computes (g_bar, g_obs) per radial bin, and plots the RAR with the
GFD field equation prediction overlaid.

Conventions (SPARC standard):
    Upsilon_disk = 0.5   (M/L at 3.6 um)
    Upsilon_bul  = 0.7
    v_bar^2 = sign(v_gas)*v_gas^2  +  Y_d * v_disk^2  +  Y_b * v_bul^2
"""

import argparse
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote

import matplotlib.pyplot as plt
import numpy as np
import requests

API = "https://api.fielddynamics.org/v1/sparc"

# (km/s)^2 / kpc  ->  m/s^2
KMS2_PER_KPC_TO_MS2 = (1.0e3) ** 2 / 3.0857e19  # = 3.2408e-14

UPSILON_DISK = 0.5
UPSILON_BUL = 0.7

A0_MS2 = 1.2e-10  # MOND / GFD scale


# ---------- HTTP ----------------------------------------------------------

def fetch_catalog(session: requests.Session) -> list[dict]:
    r = session.get(f"{API}/catalog", timeout=30)
    r.raise_for_status()
    return r.json()["galaxies"]


def fetch_galaxy(session: requests.Session, name: str, retries: int = 3) -> dict | None:
    url = f"{API}/{quote(name)}"
    for attempt in range(retries):
        try:
            r = session.get(url, timeout=30)
            r.raise_for_status()
            return r.json()
        except Exception as e:  # noqa: BLE001
            if attempt == retries - 1:
                print(f"  FAIL {name}: {e}")
                return None


# ---------- RAR computation ----------------------------------------------

def compute_rar(g: dict) -> tuple[np.ndarray, np.ndarray]:
    d = g["data"]
    r  = np.asarray(d["radius_kpc"],  dtype=float)
    vo = np.asarray(d["v_obs_km_s"],  dtype=float)
    vg = np.asarray(d["v_gas_km_s"],  dtype=float)
    vd = np.asarray(d["v_disk_km_s"], dtype=float)
    vb = np.asarray(d["v_bul_km_s"],  dtype=float)

    # preserve gas sign (SPARC convention)
    v_bar2 = vg * np.abs(vg) + UPSILON_DISK * vd**2 + UPSILON_BUL * vb**2

    mask = (r > 0) & (vo > 0) & (v_bar2 > 0)
    r, vo2, vb2 = r[mask], vo[mask] ** 2, v_bar2[mask]

    g_obs = vo2 / r * KMS2_PER_KPC_TO_MS2
    g_bar = vb2 / r * KMS2_PER_KPC_TO_MS2
    return g_bar, g_obs


# ---------- theory curves ------------------------------------------------

def gfd_field_equation(g_bar: np.ndarray, a0: float = A0_MS2) -> np.ndarray:
    """GFD field equation in the spherical static limit.

    Solves  g_bar = g_obs^2 / (a0 + g_obs)  for g_obs.

    This is the GFD field equation (modified Poisson equation with
    mu = x/(x+1)) reduced via Gauss's theorem to an algebraic relation.
    mu is kinematic (forced by exchange symmetry of the tetrad equation's
    parity-related roots); the field equation is dynamic (from varying
    the covariant action).  Connected via the AQUAL identity  mu = dF/dy.
    """
    return 0.5 * (g_bar + np.sqrt(g_bar**2 + 4.0 * a0 * g_bar))


def mcgaugh_rar(g_bar: np.ndarray, g_dagger: float = A0_MS2) -> np.ndarray:
    """McGaugh+2016 empirical fit."""
    return g_bar / (1.0 - np.exp(-np.sqrt(g_bar / g_dagger)))


# ---------- main ---------------------------------------------------------

def main(quality_max: int = 2,
         workers: int = 16,
         out_png: str = "sparc_rar.png",
         out_csv: str = "sparc_rar.csv",
         from_csv: str | None = None):

    if from_csv:
        # Offline reproduction from the bundled (galaxy, g_bar, g_obs) table.
        rows = []
        with open(from_csv, newline="") as f:
            for r in csv.DictReader(f):
                rows.append((r["galaxy"], float(r["g_bar_ms2"]), float(r["g_obs_ms2"])))
        gb = np.array([r[1] for r in rows])
        go = np.array([r[2] for r in rows])
        galaxies = sorted({r[0] for r in rows})
        print(f"points: {len(gb)} from {len(galaxies)} galaxies (read from {from_csv})")
        return _analyse_and_plot(gb, go, galaxies, quality_max, out_png)

    sess = requests.Session()

    catalog = fetch_catalog(sess)
    names = [g["name"] for g in catalog if g["quality"] <= quality_max]
    print(f"catalog: {len(catalog)} total, {len(names)} with Q <= {quality_max}")

    galaxies: list[dict] = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(fetch_galaxy, sess, n): n for n in names}
        for i, fut in enumerate(as_completed(futs), 1):
            g = fut.result()
            if g is not None:
                galaxies.append(g)
            if i % 25 == 0 or i == len(names):
                print(f"  fetched {i}/{len(names)}")

    rows, all_gb, all_go = [], [], []
    for g in galaxies:
        try:
            gb, go = compute_rar(g)
        except Exception as e:  # noqa: BLE001
            print(f"  skip {g.get('name','?')}: {e}")
            continue
        all_gb.append(gb)
        all_go.append(go)
        for x, y in zip(gb, go):
            rows.append((g["name"], x, y))

    gb = np.concatenate(all_gb)
    go = np.concatenate(all_go)
    print(f"points: {len(gb)} from {len(galaxies)} galaxies")

    # CSV dump
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["galaxy", "g_bar_ms2", "g_obs_ms2"])
        w.writerows(rows)
    print(f"wrote {out_csv}")

    return _analyse_and_plot(gb, go, galaxies, quality_max, out_png)


def _analyse_and_plot(gb, go, galaxies, quality_max, out_png):

    # Residuals against both theory curves (dex)
    log_go  = np.log10(go)
    log_gfd = np.log10(gfd_field_equation(gb))
    log_mcg = np.log10(mcgaugh_rar(gb))
    res_gfd = log_go - log_gfd
    res_mcg = log_go - log_mcg

    # Plot: main RAR on left, residual histograms on right
    fig, (ax, ax_h) = plt.subplots(
        1, 2, figsize=(14, 7),
        gridspec_kw={"width_ratios": [1.15, 1]},
    )

    # --- left panel: RAR hexbin -----------------------------------------
    hb = ax.hexbin(np.log10(gb), log_go,
                   gridsize=60, cmap="viridis",
                   mincnt=1, bins="log")
    cb = fig.colorbar(hb, ax=ax, shrink=0.85)
    cb.set_label("log10 count")

    x = np.logspace(-13, -8, 400)
    ax.plot(np.log10(x), np.log10(x),
            "k--", lw=1, label="1:1 (Newton)")
    ax.plot(np.log10(x), np.log10(gfd_field_equation(x)),
            "r-",  lw=2,  label=r"GFD field equation  ($a_0=1.2\times10^{-10}$ m/s$^2$)")
    ax.plot(np.log10(x), np.log10(mcgaugh_rar(x)),
            "orange", ls=":", lw=1.5, label="McGaugh+2016 fit")

    ax.set_xlim(-13, -8)
    ax.set_ylim(-13, -8)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$\log_{10}\, g_{\rm bar}$  [m/s$^2$]")
    ax.set_ylabel(r"$\log_{10}\, g_{\rm obs}$  [m/s$^2$]")
    ax.set_title(f"SPARC RAR — {len(galaxies)} galaxies, {len(gb)} points (Q≤{quality_max})")
    ax.legend(loc="lower right", framealpha=0.9)
    ax.grid(alpha=0.3)

    # --- right panel: residual histogram --------------------------------
    bins = np.linspace(-1.0, 1.0, 61)

    ax_h.hist(res_gfd, bins=bins, histtype="stepfilled",
              color="red", alpha=0.35)
    ax_h.hist(res_gfd, bins=bins, histtype="step",
              color="red", lw=1.8, label="GFD field equation")

    ax_h.hist(res_mcg, bins=bins, histtype="stepfilled",
              color="orange", alpha=0.25)
    ax_h.hist(res_mcg, bins=bins, histtype="step",
              color="orange", lw=1.8, ls=":", label="McGaugh+2016")

    ax_h.axvline(0, color="k", lw=0.8)

    stats = [
        ("GFD",     res_gfd, "red"),
        ("McGaugh", res_mcg, "darkorange"),
    ]
    for i, (name, r, color) in enumerate(stats):
        ax_h.text(0.02, 0.96 - i * 0.06,
                  f"{name:<8} mean={r.mean():+.4f}   "
                  f"sigma={r.std():.4f}   "
                  f"median={np.median(r):+.4f}  dex",
                  transform=ax_h.transAxes,
                  color=color, fontsize=10, family="monospace",
                  fontweight="bold", verticalalignment="top")

    # zero-bias reference
    ax_h.set_xlabel(r"$\log_{10} g_{\rm obs} - \log_{10} g_{\rm theory}$   [dex]")
    ax_h.set_ylabel("count")
    ax_h.set_title("Residuals")
    ax_h.set_xlim(-1.0, 1.0)
    ax_h.legend(loc="upper right", framealpha=0.9)
    ax_h.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    print(f"wrote {out_png}")

    # print stats table for the record
    print()
    print(f"  {'theory':<10} {'mean':>10} {'sigma':>10} {'median':>10}  [dex]")
    for name, r, _ in stats:
        print(f"  {name:<10} {r.mean():>+10.4f} {r.std():>10.4f} {np.median(r):>+10.4f}")

    return fig, (ax, ax_h)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--quality-max", type=int, default=2,
                    help="keep galaxies with quality <= this (1=best, 3=worst)")
    ap.add_argument("--workers",     type=int, default=16)
    ap.add_argument("--out-png",     default="sparc_rar.png")
    ap.add_argument("--out-csv",     default="sparc_rar.csv")
    ap.add_argument("--from-csv",    default=None,
                    help="skip the API and reproduce offline from a saved table, "
                         "e.g. supplementary/sparc_rar.csv")
    # parse_known_args so Jupyter's  -f kernel.json  is ignored under %run
    args, _unknown = ap.parse_known_args()
    main(quality_max=args.quality_max,
         workers=args.workers,
         out_png=args.out_png,
         out_csv=args.out_csv,
         from_csv=args.from_csv)
