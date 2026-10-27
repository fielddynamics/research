"""
Areal closure from the GFD action (01.7).

1. The GFD scalar sector  L = -(a0^2 / 8 pi G) F(y),  y = |grad Phi|^2 / a0^2,
   depends on Phi only through grad Phi, so it is invariant under the shift
   Phi -> Phi + c.  Its Noether current is

       J = -dL/d(grad Phi) = mu(|grad Phi| / a0) grad Phi / (4 pi G),

   carrying the constitutive law mu(x) = x/(x+1) (since dF/dy = mu(sqrt y)).
   (Verified symbolically in `noether_current_check`, if sympy is available.)

2. In a region free of sources for the driven closure field, div J = 0.  For
   the frustum of an apex body between the base and level z, the divergence
   theorem gives the closure balance

       Phi_base = Phi_section(z) + Phi_lateral(0..z).

3. GFD's odds ratio of the axial (continuing) share to the lateral
   (exchanged) share is Omega = mu / (1 - mu), so

       mu_B(z) = Phi_section(z) / Phi_base.

   For a uniform axial current this is A(z)/A(0): postulate P1 of 01.6.

This module integrates the fluxes numerically for a square pyramid and an
arbitrary current field J(x, y, z), so that P1 can be checked against any
computed field (for example, from the Phase 0 electromagnetic model).
"""

from __future__ import annotations

import math
from typing import Callable, Tuple

import numpy as np

Vector = Tuple[np.ndarray, np.ndarray, np.ndarray]
Field = Callable[[np.ndarray, np.ndarray, np.ndarray], Vector]

# Great Pyramid (Petrie 1883), inches
BASE_SIDE_IN = 9068.8
HEIGHT_IN = 5776.0


# ---------------------------------------------------------------------------
# Symbolic check of the Noether current
# ---------------------------------------------------------------------------

def noether_current_check() -> bool:
    """Return True if J = -dL/d(grad Phi) equals mu grad Phi / (4 pi G)."""
    import sympy as sp

    a0, G = sp.symbols("a0 G", positive=True)
    p = sp.symbols("p_x p_y p_z", real=True)
    y = sum(c ** 2 for c in p) / a0 ** 2
    u = sp.sqrt(y)
    F = y - 2 * u + 2 * sp.log(1 + u)
    L = -(a0 ** 2 / (8 * sp.pi * G)) * F
    x = sp.sqrt(sum(c ** 2 for c in p)) / a0
    mu = x / (x + 1)
    return all(sp.simplify(-sp.diff(L, c) - mu * c / (4 * sp.pi * G)) == 0 for c in p)


# ---------------------------------------------------------------------------
# Square pyramid geometry
# ---------------------------------------------------------------------------

def half_side(z: np.ndarray | float, b: float, h: float):
    """Half the side of the horizontal section at height z."""
    return 0.5 * b * (1.0 - np.asarray(z) / h)


def section_area(z: float, b: float, h: float) -> float:
    return (2.0 * half_side(z, b, h)) ** 2


def _gauss(n: int):
    return np.polynomial.legendre.leggauss(n)


def flux_through_section(J: Field, z: float, b: float, h: float, n: int = 48) -> float:
    """Upward flux of J through the horizontal section at height z."""
    s = float(half_side(z, b, h))
    if s == 0.0:
        return 0.0
    t, w = _gauss(n)
    X, Y = np.meshgrid(s * t, s * t, indexing="ij")
    W = np.outer(w, w) * s * s
    _, _, Jz = J(X, Y, np.full_like(X, z))
    return float(np.sum(W * Jz))


def flux_through_lateral(J: Field, z: float, b: float, h: float, n: int = 48) -> float:
    """Outward flux of J through the four lateral faces between 0 and z."""
    if z <= 0.0:
        return 0.0
    tz, wz = _gauss(n)
    zs = 0.5 * z * (tz + 1.0)
    wzs = 0.5 * z * wz
    ty, wy = _gauss(n)
    slope = b / (2.0 * h)          # -dX/dz for the face plane X(z)
    total = 0.0
    for zi, wzi in zip(zs, wzs):
        X = float(half_side(zi, b, h))
        ys = X * ty
        wys = X * wy
        # +x face: n dA = (1, 0, slope) dy dz
        Jx, _, Jz = J(np.full_like(ys, X), ys, np.full_like(ys, zi))
        total += wzi * np.sum(wys * (Jx + slope * Jz))
        # -x face: n dA = (-1, 0, slope)
        Jx, _, Jz = J(np.full_like(ys, -X), ys, np.full_like(ys, zi))
        total += wzi * np.sum(wys * (-Jx + slope * Jz))
        # +y face: n dA = (0, 1, slope)
        _, Jy, Jz = J(ys, np.full_like(ys, X), np.full_like(ys, zi))
        total += wzi * np.sum(wys * (Jy + slope * Jz))
        # -y face: n dA = (0, -1, slope)
        _, Jy, Jz = J(ys, np.full_like(ys, -X), np.full_like(ys, zi))
        total += wzi * np.sum(wys * (-Jy + slope * Jz))
    return float(total)


# ---------------------------------------------------------------------------
# Closure balance and local state
# ---------------------------------------------------------------------------

def closure_balance(J: Field, z: float, b: float = BASE_SIDE_IN, h: float = HEIGHT_IN):
    """Return (Phi_base, Phi_section, Phi_lateral, residual) for the frustum [0, z]."""
    phi_base = flux_through_section(J, 0.0, b, h)
    phi_sec = flux_through_section(J, z, b, h)
    phi_lat = flux_through_lateral(J, z, b, h)
    return phi_base, phi_sec, phi_lat, phi_base - phi_sec - phi_lat


def mu_B(J: Field, z: float, b: float = BASE_SIDE_IN, h: float = HEIGHT_IN) -> float:
    """Local closure fraction from fluxes: Phi_section(z) / Phi_base."""
    return flux_through_section(J, z, b, h) / flux_through_section(J, 0.0, b, h)


def odds_ratio(J: Field, z: float, b: float = BASE_SIDE_IN, h: float = HEIGHT_IN) -> float:
    """Omega = axial share / lateral share."""
    _, sec, lat, _ = closure_balance(J, z, b, h)
    return sec / lat


def balance_height(J: Field, b: float = BASE_SIDE_IN, h: float = HEIGHT_IN,
                   tol: float = 1e-9) -> float:
    """Height at which mu_B = 1/2 (bisection)."""
    lo, hi = 0.0, h * (1.0 - 1e-9)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mu_B(J, mid, b, h) > 0.5:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol * h:
            break
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------
# Example fields
# ---------------------------------------------------------------------------

def uniform_axial(j0: float = 1.0) -> Field:
    """Uniform axial current, J = j0 z_hat (divergence-free)."""
    def J(x, y, z):
        return np.zeros_like(x), np.zeros_like(x), np.full_like(x, j0)
    return J


def strained_axial(j0: float = 1.0, eps: float = 0.1, h: float = HEIGHT_IN) -> Field:
    """Divergence-free non-uniform current:
    J = j0 * (-eps x / (2h), -eps y / (2h), 1 + eps z / h)."""
    def J(x, y, z):
        return (-j0 * eps * x / (2 * h), -j0 * eps * y / (2 * h),
                j0 * (1.0 + eps * z / h))
    return J


def showcase() -> None:
    b, h = BASE_SIDE_IN, HEIGHT_IN
    print("Areal closure from the GFD action (01.7)")
    print("-" * 60)
    try:
        print(f"Noether current = mu grad Phi / 4 pi G : {noether_current_check()}")
    except ImportError:
        print("Noether current check skipped (sympy not installed)")
    zstar = h * (1 - 1 / math.sqrt(2))
    J = uniform_axial()
    base, sec, lat, res = closure_balance(J, zstar)
    print(f"Uniform field at z* = {zstar:.1f} in:")
    print(f"  Phi_base = {base:.6e}, Phi_sec = {sec:.6e}, Phi_lat = {lat:.6e}")
    print(f"  balance residual / Phi_base = {res / base:.2e}")
    print(f"  mu_B = {mu_B(J, zstar):.6f}, Omega = {odds_ratio(J, zstar):.6f}")
    print(f"  balance height = {balance_height(J):.2f} in (z* = {zstar:.2f})")
    for eps in (0.05, 0.1, 0.2):
        Js = strained_axial(eps=eps)
        zb = balance_height(Js)
        print(f"Strained field eps={eps:4.2f}: balance height {zb:.1f} in "
              f"({zb - zstar:+.1f} in from z*)")


if __name__ == "__main__":
    showcase()
