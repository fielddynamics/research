"""T18. Diamond against the other nets, at matched filling (diamond's 0.496) and contrast
(eps 11.56 spheres in air). Lonsdaleite uses the same bond length and sphere radius as diamond
(the two have the same atomic density, so the filling matches). Simple cubic and fcc use the
same volume per sphere as diamond, with the radius set for the same filling.
Plane waves scale with cell volume (800 per diamond primitive cell, as validated in T17).
The largest complete gap among the 10 lowest bands, on each lattice's standard path.
Pass (diamond singled out): diamond's gap at least twice the next largest."""
import sys, time
import numpy as np
from pwe import Crystal, spheres_eps, complete_gaps

EPS = 11.56
def radius_for(A, centres, f_target):
    lo, hi = 0.05, 0.6
    for _ in range(30):
        r = 0.5 * (lo + hi)
        f = (Crystal(A, spheres_eps(centres, r, 2.0, 1.0, A), grid=48).eps_r > 1.5).mean()
        lo, hi = (r, hi) if f < f_target else (lo, r)
    return 0.5 * (lo + hi)

cases = {}
# diamond (as T17)
A = [(0, .5, .5), (.5, 0, .5), (.5, .5, 0)]
X, U, L, G, W, K = (0, .5, .5), (0, .625, .375), (0, .5, 0), (0, 0, 0), (.25, .75, .5), (.375, .75, .375)
cases["diamond"] = (A, [np.full(3, .125), np.full(3, -.125)], 0.25, [X, U, L, G, X, W, K], 800)
# fcc, one sphere per primitive cell of volume 0.125 (cubic a = 0.5^(1/3))
af = 0.5 ** (1 / 3)
Af = [tuple(af * np.array(v)) for v in A]
cases["fcc"] = (Af, [np.zeros(3)], None, [X, U, L, G, X, W, K], 400)
# simple cubic, volume 0.125
As = [(.5, 0, 0), (0, .5, 0), (0, 0, .5)]
cases["simple cubic"] = (As, [np.zeros(3)], None, [(0, 0, 0), (.5, 0, 0), (.5, .5, 0), (0, 0, 0), (.5, .5, .5), (.5, 0, 0)], 400)
# lonsdaleite with diamond's bond length sqrt(3)/4 and radius 0.25
d = np.sqrt(3) / 4
ah = d * np.sqrt(8 / 3); ch = 8 * d / 3
Ah = [(ah, 0, 0), (ah / 2, ah * np.sqrt(3) / 2, 0), (0, 0, ch)]
fr = [(0, 0, 0), (0, 0, 3 / 8), (1 / 3, 1 / 3, .5), (1 / 3, 1 / 3, 7 / 8)]
cent = [np.array(f) @ np.array(Ah) for f in fr]
Bh = 2 * np.pi * np.linalg.inv(np.array(Ah)).T
Kpt = np.array([1 / 3, 2 / 3, 0]) @ Bh
assert abs(np.linalg.norm(Kpt) - 4 * np.pi / (3 * ah)) < 1e-9, "K point check"
Mpt = np.array([.5, 0, 0]) @ Bh
assert abs(np.linalg.norm(Mpt) - 2 * np.pi / (np.sqrt(3) * ah)) < 1e-9, "M point check"
hp = [(0, 0, 0), (.5, 0, 0), (1 / 3, 2 / 3, 0), (0, 0, 0), (0, 0, .5), (.5, 0, .5), (1 / 3, 2 / 3, .5), (0, 0, .5)]
cases["lonsdaleite"] = (Ah, cent, 0.25, hp, 1600)

f_diamond = None
out = {}
for name in sys.argv[1:] or ["diamond", "fcc", "simple cubic", "lonsdaleite"]:
    Av, cen, r, path, npw = cases[name]
    if r is None:
        r = radius_for(Av, cen, 0.4959)
    C = Crystal(Av, spheres_eps(cen, r, EPS, 1.0, Av), grid=64)
    f = (C.eps_r > 1).mean()
    t = time.time()
    bl = [C.bands(k, npw=npw, nbands=10) for k in C.path(path, per_seg=4)]
    gaps = complete_gaps(bl)
    best = max(gaps, key=lambda g: g[1]) if gaps else (None, 0.0, None, None)
    out[name] = best[1]
    print(f"{name:13s} r={r:.4f} filling {f:.4f}  gaps {[(g[0], round(100*g[1], 2)) for g in gaps]}  "
          f"largest {100*best[1]:.2f}% ({time.time()-t:.0f}s)")
    sys.stdout.flush()
if len(out) == 4:
    others = max(v for k, v in out.items() if k != "diamond")
    ok = out["diamond"] >= 2 * others
    print("\nT18", "PASS" if ok else "FAIL", f"- diamond {100*out['diamond']:.2f}%, next largest {100*others:.2f}% "
          "(criterion: diamond at least twice the next)")
