"""
Axisymmetric solver for the GFD field equation (the scalar-sector Euler-Lagrange equation of the action):

    div[ mu(|grad Phi| / a0) grad Phi ] = 4 pi G rho,      mu(x) = x / (1 + x)

for a point mass M in a uniform external field g_e (along +z: Phi -> g_e z far away).
Units: G M = 1, a0 = 1, so lengths are in r_M = sqrt(G M / a0) and accelerations in a0.

Finite volume on a sinh-stretched (R, z) grid, Picard iteration on mu, sparse direct solve.
Dirichlet boundary from the analytic far field:
  g_e > 0 : Phi = g_e z - 1 / (mu_e sqrt(1+L_e) sqrt(R^2 + z^2/(1+L_e)))     (linearised EFE regime)
  g_e = 0 : the exact isolated spherical solution.
"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.interpolate import RegularGridInterpolator
from scipy.integrate import quad

mu = lambda x: x / (1.0 + x)
mu_safe = lambda x: x / (1.0 + x) + 1e-10      # floor guards exact zeros of the gradient only


def g_isolated(r):
    """Exact spherical solution of mu(g) g = g_N with g_N = 1/r^2."""
    gN = 1.0 / r ** 2
    return 0.5 * (gN + np.sqrt(gN ** 2 + 4 * gN))


class Solver:
    def __init__(self, g_e, A=0.004, Rmax=300.0, NR=240, NZ=481, eps=0.015):
        self.g_e = g_e
        u = np.linspace(0, np.arcsinh(Rmax / A), NR + 1)
        self.R = A * np.sinh(u)
        v = np.linspace(-np.arcsinh(Rmax / A), np.arcsinh(Rmax / A), NZ)
        self.z = A * np.sinh(v)
        self.NR, self.NZ = NR, NZ
        R, z = self.R, self.z
        # control-volume faces
        Rf = np.concatenate([[0.0], 0.5 * (R[1:] + R[:-1]), [R[-1]]])
        zf = np.concatenate([[z[0]], 0.5 * (z[1:] + z[:-1]), [z[-1]]])
        self.Rf, self.zf = Rf, zf
        self.ring = np.pi * (Rf[1:] ** 2 - Rf[:-1] ** 2)          # annulus area per R node
        self.dz = zf[1:] - zf[:-1]
        RR, ZZ = np.meshgrid(R, z, indexing="ij")
        self.RR, self.ZZ = RR, ZZ
        # source: uniform sphere of radius eps, normalised so that integral of 4 pi G rho dV = 4 pi
        vol = self.ring[:, None] * self.dz[None, :]
        inside = (RR ** 2 + ZZ ** 2) < eps ** 2
        w = vol * inside
        self.S = 4 * np.pi * w / w.sum()
        self.Phi = self.boundary(RR, ZZ)

    def boundary(self, R, z):
        if self.g_e > 0:
            xe = self.g_e
            me, Le = mu(xe), 1.0 / (1.0 + xe)
            return self.g_e * z - 1.0 / (me * np.sqrt(1 + Le) * np.sqrt(R ** 2 + z ** 2 / (1 + Le) + 1e-12))
        r = np.sqrt(R ** 2 + z ** 2) + 1e-12
        # Phi(r) = int_1^r g dr  (exact isolated solution, additive constant irrelevant)
        rr = np.geomspace(1e-6, 1e4, 6000)
        gg = g_isolated(rr)
        Pc = np.concatenate([[0.0], np.cumsum(0.5 * (gg[1:] + gg[:-1]) * np.diff(rr))])
        P1 = np.interp(1.0, rr, Pc)
        return np.interp(r, rr, Pc) - P1

    def grad(self, Phi):
        dR = np.gradient(Phi, self.R, axis=0, edge_order=2)
        dZ = np.gradient(Phi, self.z, axis=1, edge_order=2)
        dR[0, :] = 0.0
        return dR, dZ

    def iterate(self, max_iter=80, tol=1e-7, relax=0.6, verbose=False):
        R, z, NR, NZ = self.R, self.z, self.NR, self.NZ
        nI, nJ = NR, NZ - 2                      # unknowns: i = 0..NR-1, j = 1..NZ-2
        idx = lambda i, j: i * nJ + (j - 1)
        Phi = self.Phi.copy()
        bnd = self.boundary(self.RR, self.ZZ)
        Phi[NR, :] = bnd[NR, :]; Phi[:, 0] = bnd[:, 0]; Phi[:, -1] = bnd[:, -1]
        for it in range(max_iter):
            dR, dZ = self.grad(Phi)
            # face mus
            gRf = (Phi[1:, :] - Phi[:-1, :]) / (R[1:] - R[:-1])[:, None]         # R-faces i+1/2
            zR = 0.5 * (dZ[1:, :] + dZ[:-1, :])
            muR = mu_safe(np.sqrt(gRf ** 2 + zR ** 2))
            gZf = (Phi[:, 1:] - Phi[:, :-1]) / (z[1:] - z[:-1])[None, :]         # z-faces j+1/2
            rZ = 0.5 * (dR[:, 1:] + dR[:, :-1])
            muZ = mu_safe(np.sqrt(gZf ** 2 + rZ ** 2))
            rows, cols, vals = [], [], []
            b = np.zeros(nI * nJ)
            for i in range(nI):
                Rp = self.Rf[i + 1]; Rm = self.Rf[i]
                for j in range(1, NZ - 1):
                    p = idx(i, j); diag = 0.0
                    # east (i+1)
                    aE = 2 * np.pi * Rp * self.dz[j] * muR[i, j] / (R[i + 1] - R[i])
                    diag -= aE
                    if i + 1 < NR: rows.append(p); cols.append(idx(i + 1, j)); vals.append(aE)
                    else: b[p] -= aE * Phi[i + 1, j]
                    # west (i-1)
                    if i > 0:
                        aW = 2 * np.pi * Rm * self.dz[j] * muR[i - 1, j] / (R[i] - R[i - 1])
                        diag -= aW; rows.append(p); cols.append(idx(i - 1, j)); vals.append(aW)
                    # north (j+1), south (j-1)
                    aN = self.ring[i] * muZ[i, j] / (z[j + 1] - z[j]); diag -= aN
                    if j + 1 < NZ - 1: rows.append(p); cols.append(idx(i, j + 1)); vals.append(aN)
                    else: b[p] -= aN * Phi[i, j + 1]
                    aS = self.ring[i] * muZ[i, j - 1] / (z[j] - z[j - 1]); diag -= aS
                    if j - 1 > 0: rows.append(p); cols.append(idx(i, j - 1)); vals.append(aS)
                    else: b[p] -= aS * Phi[i, j - 1]
                    rows.append(p); cols.append(p); vals.append(diag)
                    b[p] += self.S[i, j]
            Amat = sp.csr_matrix((vals, (rows, cols)), shape=(nI * nJ, nI * nJ))
            sol = spla.spsolve(Amat.tocsc(), b)
            new = Phi.copy()
            new[:NR, 1:NZ - 1] = sol.reshape(nI, nJ)
            change = np.max(np.abs(new - Phi)[: NR, 1:-1]) / (np.max(np.abs(Phi)) + 1e-30)
            Phi = relax * new + (1 - relax) * Phi
            if verbose: print(f"  iter {it:2d}  max change {change:.2e}")
            if change < tol: break
        self.Phi = Phi
        dR, dZ = self.grad(Phi)
        self._iR = RegularGridInterpolator((R, z), dR)
        self._iZ = RegularGridInterpolator((R, z), dZ)
        return it, change

    def internal_radial(self, s, n_theta=64):
        """Orientation-averaged inward radial internal acceleration at radius s
        (the uniform external field removed). Gauss-Legendre in cos(theta)."""
        c, w = np.polynomial.legendre.leggauss(n_theta)
        th = np.arccos(c)
        pts = np.stack([s * np.sin(th), s * np.cos(th)], axis=1)
        dR, dZ = self._iR(pts), self._iZ(pts) - self.g_e
        gr = np.sin(th) * dR + np.cos(th) * dZ          # = d Phi_int / d r  (> 0 means attraction)
        return 0.5 * np.sum(w * gr), gr, th
