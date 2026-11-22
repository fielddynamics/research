"""3D check of the ownership form of the mountain-scale action.

Each bound system sweeps ITS OWN mass onto its own closure sphere (Jacobi sphere); spheres may overlap and contain
other systems. The mountain is the total field minus each system's own interior field, Phi_bar = Phi - sum_k d_k,
and it obeys the plain law on the swept density:  div[mu grad Phi_bar] = 4 pi G (rho_host + sum_k swept shell_k).
Each d_k = Newton(rho_k) - Newton(shell_k) is the system's own interior field: zero outside its sphere, linear.

Runs: (1) one system (the 'Sun') against the pointwise reading; (2) two systems whose spheres overlap and each contain
the other's mass. Units 4 pi G = a0 = 1. Uses the solver of demo_mountain_scale.py. About 10 minutes.
Run: python demo_ownership_3d.py > demo_ownership_output.txt"""
import numpy as np
from demo_mountain_scale import blob, solve, grad, inv_lap, X, Y, Z, dx

def shell(m, R, c, w=0.7):
    r = np.sqrt((X - c[0]) ** 2 + (Y - c[1]) ** 2 + (Z - c[2]) ** 2)
    s = np.exp(-(r - R) ** 2 / (2 * w ** 2)); return m * s / (s.sum() * dx ** 3)

def radial_in(g, c, R):
    rx, ry, rz = X - c[0], Y - c[1], Z - c[2]; rr = np.sqrt(rx ** 2 + ry ** 2 + rz ** 2) + 1e-12
    v = sum(g[i] * comp / rr for i, comp in enumerate((rx, ry, rz)))
    sh = (rr > R - 0.5) & (rr < R + 0.5)
    return np.mean(v[sh])

sun, cA, RA = 300.0, (24.0, 0.0, 0.0), 10.0
starB, cB, RB = 200.0, (31.0, 0.0, 0.0), 9.0           # 7 apart: each sphere contains the other's centre
rho_gal = blob(5000.0, 6.0, (0, 0, 0))
rho_A, rho_B = blob(sun, 1.0, cA), blob(starB, 1.0, cB)
sh_A, sh_B = shell(sun, RA, cA), shell(starB, RB, cB)
d_A, d_B = inv_lap(rho_A - sh_A), inv_lap(rho_B - sh_B)
rr_A = np.sqrt((X - cA[0]) ** 2 + (Y - cA[1]) ** 2 + (Z - cA[2]) ** 2)
rr_B = np.sqrt((X - cB[0]) ** 2 + (Y - cB[1]) ** 2 + (Z - cB[2]) ** 2)
print(f"own interior field vanishes outside its sphere: Sun {np.abs(d_A[rr_A > RA + 3]).max() / np.abs(d_A).max():.1e}, "
      f"star B {np.abs(d_B[rr_B > RB + 3]).max() / np.abs(d_B).max():.1e}")
Pg, rg = solve(rho_gal, None)                                   # galaxy alone
gG = grad(Pg)
gNA, gNB = grad(inv_lap(rho_A)), grad(inv_lap(rho_B))
# (1) one system, ownership reading
Pm, r1 = solve(rho_gal + sh_A, None)
gT = grad(Pm + d_A)
print(f"[one system] mountain residual {r1:.1e}")
for R in (2.0, 3.0, 4.0, 6.0):
    extra = -radial_in([gT[i] - gG[i] - gNA[i] for i in range(3)], cA, R)
    print(f"  ownership r = {R:.0f}: extra pull toward the Sun = {extra:+.3f} a0")
# (2) two systems with overlapping spheres
Pm2, r2 = solve(rho_gal + sh_A + sh_B, None)
gT2 = grad(Pm2 + d_A + d_B)
print(f"[two systems, overlapping spheres] mountain residual {r2:.1e}")
for R in (2.0, 3.0, 4.0):
    extra = -radial_in([gT2[i] - gG[i] - gNA[i] - gNB[i] for i in range(3)], cA, R)
    print(f"  around the Sun r = {R:.0f}: extra pull beyond Newton (Sun + star B) and the galaxy = {extra:+.3f} a0")
for R in (2.0, 3.0):
    extra = -radial_in([gT2[i] - gG[i] - gNA[i] - gNB[i] for i in range(3)], cB, R)
    print(f"  around star B r = {R:.0f}: extra pull beyond Newton (Sun + star B) and the galaxy = {extra:+.3f} a0")
