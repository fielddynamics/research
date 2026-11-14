"""Shared lattice builders for the T-tests.

Units: TetA legs are (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1), so the bond
length is sqrt(3) and the diamond conventional cell has side 4.
"""
import itertools

import numpy as np
import scipy.sparse as sps

TETA = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], dtype=float)
TETB = -TETA
BOND = np.sqrt(3.0)


def diamond_box(n):
    """Diamond sites in the cube [0, 4n)^3, with sublattice labels (+1 TetA, -1 TetB)."""
    rng = range(0, 4 * n)
    pts, lab = [], []
    for p in itertools.product(rng, repeat=3):
        if all(c % 2 == 0 for c in p) and sum(p) % 4 == 0:
            pts.append(p); lab.append(1)
        elif all(c % 2 for c in p) and sum(p) % 4 == 3:
            pts.append(p); lab.append(-1)
    return np.array(pts, float), np.array(lab)


def lonsdaleite_box(nx, ny, nz):
    """Lonsdaleite (hexagonal diamond) with bond length sqrt(3), every site 4-bonded
    in a regular tetrahedron. Returns positions and sublattice labels (+1/-1 by
    which way the c-axis bond points)."""
    d = BOND
    a = d * np.sqrt(8.0 / 3.0)
    c = 8.0 * d / 3.0
    a1 = np.array([a, 0, 0]); a2 = np.array([a / 2, a * np.sqrt(3) / 2, 0]); a3 = np.array([0, 0, c])
    basis = [  # wurtzite-type positions for a 60-degree cell, u = 3/8
        (np.array([0.0, 0.0, 0.0]), 1), (np.array([0.0, 0.0, 3 / 8]), -1),
        (np.array([1 / 3, 1 / 3, 0.5]), 1), (np.array([1 / 3, 1 / 3, 0.5 + 3 / 8]), -1)]
    pts, lab = [], []
    for i, j, k in itertools.product(range(nx), range(ny), range(nz)):
        for f, l in basis:
            r = (i + f[0]) * a1 + (j + f[1]) * a2 + (k + f[2]) * a3
            pts.append(r); lab.append(l)
    return np.array(pts), np.array(lab)


def bonds(pts, cutoff=BOND * 1.01):
    """All pairs closer than the cutoff (the 4 nearest neighbours), by grid hashing."""
    h = cutoff
    keys = np.floor(pts / h).astype(int)
    table = {}
    for idx, k in enumerate(map(tuple, keys)):
        table.setdefault(k, []).append(idx)
    I, J = [], []
    for idx, k in enumerate(map(tuple, keys)):
        for dk in itertools.product((-1, 0, 1), repeat=3):
            for jdx in table.get((k[0] + dk[0], k[1] + dk[1], k[2] + dk[2]), ()):
                if jdx > idx and np.sum((pts[jdx] - pts[idx]) ** 2) < cutoff ** 2:
                    I.append(idx); J.append(jdx)
    return np.array(I), np.array(J)


def laplacian(npts, I, J, w=None):
    """Weighted graph Laplacian with Dirichlet zero outside: sum_j w_ij (phi_i - phi_j),
    plus w = 1 for each missing neighbour (a bond to the zero boundary)."""
    if w is None:
        w = np.ones(len(I))
    A = sps.coo_matrix((np.r_[w, w], (np.r_[I, J], np.r_[J, I])), shape=(npts, npts)).tocsr()
    deg = np.asarray(A.sum(1)).ravel()
    return A, deg


def site_gradients(pts, lab, I, J, phi):
    """Gradient at each fully bonded site from its 4 bonds, using the tight frame
    sum_a v_a v_a^T = 4 I: grad = (1/4) sum_a v_a (phi_nb - phi_site)/|v|^2 * |v|^2 ... with
    |v|^2 = 3: grad = (1/4) * sum_a v_a dphi_a / 1 where dphi_a = phi(r + v_a) - phi(r),
    exact for linear phi since sum_a v_a v_a^T = 4I."""
    n = len(pts)
    g = np.zeros((n, 3)); cnt = np.zeros(n)
    dv = pts[J] - pts[I]
    dphi = phi[J] - phi[I]
    np.add.at(g, I, dv * dphi[:, None]); np.add.at(cnt, I, 1)
    np.add.at(g, J, dv * dphi[:, None]); np.add.at(cnt, J, 1)   # (-dv)(-dphi) = dv dphi
    full = cnt == 4
    return g / 4.0, full


def diamond_grid(n):
    """Fast diamond in the cube [0, 4n)^3: positions, labels, and bond list (A index, B index),
    built by index arithmetic. Bonds leaving the box are returned as counts per site."""
    L = 4 * n
    g = np.indices((L, L, L)).reshape(3, -1).T
    even = np.all(g % 2 == 0, axis=1) & (g.sum(1) % 4 == 0)
    odd = np.all(g % 2 == 1, axis=1) & (g.sum(1) % 4 == 3)
    sel = even | odd
    pts = g[sel]
    lab = np.where(even[sel], 1, -1)
    index = -np.ones((L, L, L), dtype=np.int64)
    index[pts[:, 0], pts[:, 1], pts[:, 2]] = np.arange(len(pts))
    A = np.where(lab == 1)[0]
    I, J = [], []
    for v in TETA.astype(int):
        q = pts[A] + v
        inside = np.all((q >= 0) & (q < L), axis=1)
        jj = index[q[inside, 0], q[inside, 1], q[inside, 2]]
        assert np.all(jj >= 0)
        I.append(A[inside]); J.append(jj)
    I = np.concatenate(I); J = np.concatenate(J)
    deg = np.bincount(np.r_[I, J], minlength=len(pts))
    return pts.astype(float), lab, I, J, deg
