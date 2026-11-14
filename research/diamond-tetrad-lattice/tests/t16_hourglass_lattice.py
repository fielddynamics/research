"""T16. The hourglass lemma on the diamond net.
A swirl (Omega z x rho) plus an axial through-flow (u_z = -W (1 - rho^2/R0^2), a drain) is put
on the bonds as b_ij = u(mid_ij).(r_j - r_i). Discrete operators: site velocity by the tight
frame (1/4) sum_a v_a b_a; vorticity at a site by least squares over its 12 hexagon rings
(circulation = omega . vector area). Helicity H = sum_s u_s . omega_s over a ball about a bond
midpoint m. Then the field is inverted through m, u'(r) = -u(2m - r), and everything recomputed.
Pass: helicity reverses (H' = -H to 1e-12 relative); swirl kept; through-flow reversed."""
import numpy as np
from lattice import diamond_grid

pts, lab, I, J, deg = diamond_grid(6)          # side 24
m = np.array([12.5, 12.5, 12.5])               # midpoint of the bond (12,12,12)-(13,13,13)
N = len(pts)
index = {tuple(p.astype(int)): i for i, p in enumerate(pts)}
assert (12, 12, 12) in index and (13, 13, 13) in index, "need a bond with midpoint m"
nbrs = [[] for _ in range(N)]
for i, j in zip(I, J):
    nbrs[i].append(j); nbrs[j].append(i)

def rings_at(s):
    """The hexagons through site s, each once, as an ordered cycle starting at s."""
    found = {}
    def walk(path):
        u = path[-1]
        for w in nbrs[u]:
            if len(path) == 6 and w == s:
                found.setdefault(frozenset(path), tuple(path))
            elif len(path) < 6 and w not in path:
                walk(path + [w])
    walk([s])
    return list(found.values())

R0, Om, W = 6.0, 0.7, 0.4
def u_field(r):
    d = r - m
    swirl = Om * np.stack([-d[..., 1], d[..., 0], np.zeros_like(d[..., 0])], -1)
    rho2 = d[..., 0]**2 + d[..., 1]**2
    axial = np.zeros_like(d); axial[..., 2] = -W * (1 - rho2 / R0**2)
    return swirl + axial, swirl, axial

def bond_values(field):
    mid = 0.5 * (pts[I] + pts[J])
    return np.sum(field(mid)[0] * (pts[J] - pts[I]), axis=1)

bval = {}
def setb(vals):
    bval.clear()
    for k, (i, j) in enumerate(zip(I, J)):
        bval[(i, j)] = vals[k]; bval[(j, i)] = -vals[k]

d_all = np.linalg.norm(pts - m, axis=1)
ball = np.where((d_all <= 7.0) & (deg == 4))[0]
ring_cache = {s: rings_at(s) for s in ball}
assert all(len(v) == 12 for v in ring_cache.values()), "12 hexagons per site"

def helicity():
    H = 0.0; us = {}
    for s in ball:
        u = sum((pts[j] - pts[s]) * bval[(s, j)] for j in nbrs[s]) / 4.0
        Arows, G = [], []
        for ring in ring_cache[s]:
            cyc = list(ring) + [ring[0]]
            G.append(sum(bval[(a, b)] for a, b in zip(cyc[:-1], cyc[1:])))
            Arows.append(0.5 * sum(np.cross(pts[a], pts[b]) for a, b in zip(cyc[:-1], cyc[1:])))
        w = np.linalg.lstsq(np.array(Arows), np.array(G), rcond=None)[0]
        H += u @ w; us[s] = u
    return H, us

setb(bond_values(u_field)); H, us = helicity()
inv_field = lambda r: tuple(-c for c in u_field(2 * m - r))
setb(bond_values(inv_field)); Hp, usp = helicity()
sigma = {s: index[tuple((2 * m - pts[s]).astype(int))] for s in ball}
assert all(sigma[s] in us for s in ball)
_, sw, ax = u_field(pts)
def parts(u, s):
    d = pts[s] - m; phi = np.array([-d[1], d[0], 0.0]); nphi = np.linalg.norm(phi)
    return (u @ phi / nphi if nphi > 1e-9 else 0.0), u[2]
sw_ok = all(abs(parts(usp[s], s)[0] - parts(us[sigma[s]], sigma[s])[0]) < 1e-9 for s in ball)
ax_ok = all(abs(parts(usp[s], s)[1] + parts(us[sigma[s]], sigma[s])[1]) < 1e-9 for s in ball)
rel = abs(Hp + H) / abs(H)
print(f"sites in the ball: {len(ball)}; helicity H = {H:.6f}, after inversion H' = {Hp:.6f}, |H'+H|/|H| = {rel:.1e}")
print("swirl kept (azimuthal part at s equals that at its image):", sw_ok)
print("through-flow reversed (axial part at s is minus that at its image):", ax_ok)
ok = rel < 1e-12 and sw_ok and ax_ok and abs(H) > 1e-6
print("\nT16", "PASS" if ok else "FAIL", "- on the diamond net the bond-midpoint inversion keeps the swirl, reverses the "
      "through-flow and reverses the helicity, as the hourglass lemma says")
