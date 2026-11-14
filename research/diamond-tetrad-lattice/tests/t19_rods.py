"""T19. One root's legs against the full pixel, as dielectric rods (eps 11.56 in air).
The cubic tiling of pixels, cube side 1: centre (1/2,1/2,1/2), legs to the corners.
 - TetA only: rods from the centre along the 4 TetA legs (joined at the corners these are
   result 7's diamond nets of legs).
 - full pixel: rods along all 8 legs (both roots).
Rod radius 0.05 to 0.3 of the cube side. Simple-cubic path G-X-M-G-R-X, 1000 plane waves.
Pass (reported, not judged): gap/midgap against rod radius for both."""
import sys, time
import numpy as np
from pwe import Crystal, rods_eps, complete_gaps
A = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
c = np.full(3, .5)
TA = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]) / 2
legsA = [(c, c + v) for v in TA]
legsAll = legsA + [(c, c - v) for v in TA]
path = [(0, 0, 0), (.5, 0, 0), (.5, .5, 0), (0, 0, 0), (.5, .5, .5), (.5, 0, 0)]
radii = [float(v) for v in sys.argv[1].split(",")] if len(sys.argv) > 1 else [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
print("radius   TetA-only: filling, largest gap (bands)      full pixel: filling, largest gap (bands)")
for r in radii:
    row = []
    for segs in (legsA, legsAll):
        C = Crystal(A, rods_eps(segs, r, 11.56, 1.0, A), grid=64)
        bl = [C.bands(k, npw=1000, nbands=10) for k in C.path(path, per_seg=4)]
        g = complete_gaps(bl)
        b = max(g, key=lambda q: q[1]) if g else (None, 0.0)
        row.append(((C.eps_r > 1).mean(), b[1], b[0]))
    print(f" {r:.2f}    {row[0][0]:.3f}  {100*row[0][1]:7.3f}% ({row[0][2]})              "
          f"{row[1][0]:.3f}  {100*row[1][1]:7.3f}% ({row[1][2]})")
    sys.stdout.flush()
print("\nT19 PASS (reported) - gaps against rod radius for one root's legs and for the full pixel")
