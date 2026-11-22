"""The galaxy is unchanged when the mountain scale is small against it: galaxy-only field at the Sun's position,
mountain reading vs pointwise, for ell = 3, 6, 12 (galaxy width 6). Uses the solver of demo_mountain_scale.py.
Run: python galaxy_scaling.py"""
import numpy as np
from demo_mountain_scale import blob, solve, grad, N, dx
rho_gal = blob(5000.0, 6.0, (0, 0, 0))
i0 = (N // 2 + int(24.0 / dx), N // 2, N // 2)
gp = np.sqrt(sum(c[i0] ** 2 for c in grad(solve(rho_gal, None)[0])))
for ell in (12.0, 6.0, 3.0):
    gm = np.sqrt(sum(c[i0] ** 2 for c in grad(solve(rho_gal, ell)[0])))
    print(f"ell = {ell:4.1f} (ell/width = {ell / 6:.1f}): galaxy field at the Sun {gm:.4f} vs pointwise {gp:.4f}, difference {abs(gm - gp) / gp:.1e}")
