"""Vector plane-wave expansion for photonic bands (H-field formulation).

For Bloch vector k and reciprocal vectors G (|k+G| below a cutoff), the eigenproblem is
  sum_G' |k+G||k+G'| [eps^-1]_{GG'} [[e2.e2', -e2.e1'], [-e1.e2', e1.e1']] h_G' = (omega/c)^2 h_G
with e1, e2 unit vectors transverse to k+G. [eps^-1] is the inverse of the matrix eps(G - G')
(Ho, Chan and Soukoulis's choice). eps(G) comes from an FFT of eps(r) sampled on a grid over
the primitive cell, so overlapping spheres and rods are handled exactly at grid resolution.
Frequencies are returned as omega a / (2 pi c), with a the length unit of the lattice vectors.
"""
import numpy as np


class Crystal:
    def __init__(self, avecs, eps_fn, grid=64):
        self.A = np.array(avecs, float)                    # rows a_i
        self.B = 2 * np.pi * np.linalg.inv(self.A).T       # rows b_i
        s = np.arange(grid) / grid
        U = np.array(np.meshgrid(s, s, s, indexing="ij")).reshape(3, -1).T
        R = U @ self.A
        eps = eps_fn(R, U).reshape(grid, grid, grid)
        self.fill = None
        self.eps_r = eps
        self.epsG = np.fft.fftn(eps) / eps.size              # coefficient of exp(i G.r), G = m.B
        self.grid = grid

    def eps_coeff(self, dm):
        g = self.grid
        return self.epsG[dm[..., 0] % g, dm[..., 1] % g, dm[..., 2] % g]

    def gset(self, k, nmax, cutoff):
        r = np.arange(-nmax, nmax + 1)
        m = np.array(np.meshgrid(r, r, r, indexing="ij")).reshape(3, -1).T
        kg = k + m @ self.B
        keep = np.linalg.norm(kg, axis=1) <= cutoff
        return m[keep], kg[keep]

    def bands(self, k, npw=800, nbands=10, nmax=12):
        # choose a cutoff giving about npw plane waves at Gamma, reused for every k
        if not hasattr(self, "_cut") or self._cut[0] != npw:
            r = np.arange(-nmax, nmax + 1)
            m = np.array(np.meshgrid(r, r, r, indexing="ij")).reshape(3, -1).T
            norms = np.sort(np.linalg.norm(m @ self.B, axis=1))
            self._cut = (npw, norms[npw - 1] + 1e-9)
        m, kg = self.gset(np.asarray(k, float), nmax, self._cut[1])
        n = len(m)
        q = np.linalg.norm(kg, axis=1)
        zero = q < 1e-9
        khat = np.where(zero[:, None], np.array([[0, 0, 1.0]]), kg / np.where(zero, 1, q)[:, None])
        q = np.where(zero, 0.0, q)
        ref = np.where(np.abs(khat[:, 2:3]) < 0.9, np.array([[0, 0, 1.0]]), np.array([[1.0, 0, 0]]))
        e1 = np.cross(khat, ref); e1 /= np.linalg.norm(e1, axis=1)[:, None]
        e2 = np.cross(khat, e1)
        dm = m[:, None, :] - m[None, :, :]
        epsM = self.eps_coeff(dm)
        inv = np.linalg.inv(epsM)
        qq = q[:, None] * q[None, :]
        M = np.zeros((2 * n, 2 * n), complex)
        M[:n, :n] = qq * inv * (e2 @ e2.T)
        M[:n, n:] = -qq * inv * (e2 @ e1.T)
        M[n:, :n] = -qq * inv * (e1 @ e2.T)
        M[n:, n:] = qq * inv * (e1 @ e1.T)
        M = 0.5 * (M + M.conj().T)
        w2 = np.linalg.eigvalsh(M)[:nbands]
        return np.sqrt(np.clip(w2, 0, None)) / (2 * np.pi)

    def path(self, corners_frac, per_seg=4):
        pts = []
        for a, b in zip(corners_frac[:-1], corners_frac[1:]):
            for t in np.linspace(0, 1, per_seg + 1)[:-1]:
                pts.append((1 - t) * np.array(a) + t * np.array(b))
        pts.append(np.array(corners_frac[-1]))
        return [p @ self.B for p in pts]


def complete_gaps(bandlist):
    """For bands on a k-path: list of (lower band index (1-based), gap/midgap, bottom, top)."""
    W = np.array(bandlist)
    out = []
    for i in range(W.shape[1] - 1):
        lo, hi = W[:, i].max(), W[:, i + 1].min()
        if hi > lo:
            out.append((i + 1, 2 * (hi - lo) / (hi + lo), lo, hi))
    return out


def spheres_eps(centres, radius, eps_in, eps_out, A):
    """eps(r) for spheres (with periodic images) at the given Cartesian centres."""
    A = np.array(A, float)
    shifts = np.array([(i, j, k) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)]) @ A

    def f(R, U):
        inside = np.zeros(len(R), bool)
        for c in centres:
            for s in shifts:
                inside |= np.sum((R - c - s) ** 2, axis=1) <= radius ** 2
        return np.where(inside, eps_in, eps_out)
    return f


def rods_eps(segments, radius, eps_in, eps_out, A):
    """eps(r) for cylindrical rods (with periodic images) along the given Cartesian segments."""
    A = np.array(A, float)
    shifts = np.array([(i, j, k) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)]) @ A

    def f(R, U):
        inside = np.zeros(len(R), bool)
        for p0, p1 in segments:
            p0 = np.array(p0, float); d = np.array(p1, float) - p0; L2 = d @ d
            for s in shifts:
                w = R - p0 - s
                t = np.clip(w @ d / L2, 0, 1)
                inside |= np.sum((w - t[:, None] * d) ** 2, axis=1) <= radius ** 2
        return np.where(inside, eps_in, eps_out)
    return f
