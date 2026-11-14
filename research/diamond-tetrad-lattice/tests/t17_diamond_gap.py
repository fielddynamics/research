"""T17. Reproduce the diamond photonic gap (solver validation).
Benchmark: the MPB tutorial's diamond lattice of dielectric spheres in air (eps 11.56,
r = 0.25 a, spheres at +-(1/8,1/8,1/8) a on an fcc lattice), with a complete gap between
bands 2 and 3 of 10.62% gap/midgap (0.3963 to 0.4408 c/a) on the path X-U-L-G-X-W-K.
This is the same structure Ho, Chan and Soukoulis (1990) introduced, with fully specified
parameters, so it is used as the reference.
Pass: a complete gap between bands 2 and 3, gap/midgap within 10% of 10.62%, converged
(doubling the plane waves changes it by less than the tolerance)."""
import sys, time
import numpy as np
from pwe import Crystal, spheres_eps, complete_gaps
A = [(0, .5, .5), (.5, 0, .5), (.5, .5, 0)]
eps = spheres_eps([np.full(3, .125), np.full(3, -.125)], 0.25, 11.56, 1.0, A)
C = Crystal(A, eps, grid=64)
print(f"filling fraction (grid): {(C.eps_r > 1).mean():.4f}")
X, U, L, G, W, K = (0, .5, .5), (0, .625, .375), (0, .5, 0), (0, 0, 0), (.25, .75, .5), (.375, .75, .375)
ks = C.path([X, U, L, G, X, W, K], per_seg=4)
res = {}
for npw in [int(a) for a in (sys.argv[1].split(",") if len(sys.argv) > 1 else ["400", "800", "1600"])]:
    t = time.time()
    bl = [C.bands(k, npw=npw, nbands=6) for k in ks]
    gaps = complete_gaps(bl)
    g23 = [g for g in gaps if g[0] == 2]
    res[npw] = g23[0][1] if g23 else 0.0
    print(f"npw {npw:5d}: gaps {[(g[0], round(100*g[1], 2), round(g[2], 4), round(g[3], 4)) for g in gaps]}  ({time.time()-t:.0f}s)")
    sys.stdout.flush()
best = res[max(res)]
keys = sorted(res)
conv = abs(res[keys[-1]] - res[keys[-2]]) if len(keys) > 1 else np.nan
ok = best > 0 and abs(best - 0.1062) <= 0.1 * 0.1062 and conv < 0.1 * 0.1062
print(f"\nT17", "PASS" if ok else "FAIL", f"- gap 2-3 = {100*best:.2f}% (benchmark 10.62%, tolerance +-1.06); "
      f"change on last doubling {100*conv:.2f} points")
