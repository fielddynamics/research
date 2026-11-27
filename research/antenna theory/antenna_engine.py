"""Finite model for resonant TetA-TetB coupling through a nonlinear Field Origin.

Two parts:

1. Sierpinski bookkeeping (exact integer/rational identities): the physical
   gasket keeps 3 of 4 children, the complete GFD ledger keeps all 4; edge
   halving gives the dyadic band ladder measured on Sierpinski antennas; the
   gasket is self-similar about its feed vertex (Hohlfeld-Cohen condition).

2. A three-mode vertex model, per band:  TetA mode a, Field Origin mode o,
   TetB mode b.

       i da/dt = wA a + g o
       i do/dt = wO o + chi |o|^2 o + g (a + b)
       i db/dt = wB b + g o

   There is no a-b term. TetA and TetB share no coordinates and no edge; any
   exchange between them has to pass through the vertex term. The vertex
   nonlinearity chi|o|^2 o is the cubic (Kerr/NLS) form that Hasimoto (1972)
   showed governs a thin vortex filament core under local induction.
   The model is lossless: total occupation |a|^2+|o|^2+|b|^2 is conserved.

Status: the bookkeeping is exact [T]; the vertex model is a conditional model
[D]; identifying its modes with GFD chambers is a hypothesis [H].
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import comb

import numpy as np

K, D = 4, 3

# ---------------------------------------------------------------------------
# Part 1: Sierpinski bookkeeping
# ---------------------------------------------------------------------------

def gasket_triangles(n: int) -> int:
    """Surviving triangles of a physical Sierpinski gasket after n steps."""
    return 3 ** n


def ledger_addresses(n: int) -> int:
    """Complete GFD Triforce ledger: the central (gate) child is kept."""
    return K ** n


def gasket_area(n: int) -> Fraction:
    return Fraction(3, 4) ** n


def edge_fraction(n: int) -> Fraction:
    return Fraction(1, 2) ** n


def band_ratio() -> int:
    """Scale factor between successive self-similar copies (edge halving).

    For a geometry-scaled resonance f ~ 1/edge this is the log-period of the
    band ladder, measured as ~2 on the Puente Sierpinski monopole."""
    return int(1 / edge_fraction(1))


def gate_depth_counts(depth: int = D) -> list[int]:
    """Number of ledger addresses that pass through the gate at exactly d
    of `depth` digits: C(depth, d) * 3^(depth-d)."""
    return [comb(depth, d) * 3 ** (depth - d) for d in range(depth + 1)]


def gasket_points(n: int) -> set[tuple[int, int]]:
    """Corner vertices of a level-n gasket in integer barycentric-free
    coordinates (Pascal-mod-2 lattice). Apex (feed) at (0, 0); row r has
    columns 0..r; a site is present iff C(r, c) is odd. Size 2^n rows."""
    rows = 2 ** n
    return {(r, c) for r in range(rows) for c in range(r + 1) if comb(r, c) % 2 == 1}


def self_similar_about_feed(n: int) -> bool:
    """Scaling by 2 about the feed apex maps the level-(n-1) gasket onto the
    level-n gasket's sites (the top sub-gasket is an exact half-scale copy).
    This is the origin-symmetric self-similarity that Hohlfeld and Cohen
    identified as required for frequency independence."""
    small = gasket_points(n - 1)
    big = gasket_points(n)
    top = {(r, c) for (r, c) in big if r < 2 ** (n - 1)}
    doubled = {(2 * r, 2 * c) for (r, c) in small}
    return top == small and doubled <= big


# ---------------------------------------------------------------------------
# Part 2: three-mode vertex model
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Vertex:
    g: float = 1.0          # chamber-to-vertex coupling
    wA: float = 0.0         # TetA band frequency (rotating frame)
    wB: float = 0.0         # TetB band frequency
    wO: float = 0.0         # Field Origin linear frequency
    chi: float = 0.0        # vertex (filament-core) nonlinearity

    def linear_matrix(self) -> np.ndarray:
        g = self.g
        return np.array([[self.wA, g, 0.0],
                         [g, self.wO, g],
                         [0.0, g, self.wB]], dtype=complex)


def adjacency(v: Vertex) -> np.ndarray:
    """Coupling graph of the model: A-O, O-B; no A-B edge."""
    h = v.linear_matrix()
    return (np.abs(h - np.diag(np.diag(h))) > 0).astype(int)


def _rhs(v: Vertex, y: np.ndarray) -> np.ndarray:
    a, o, b = y
    return -1j * np.array([
        v.wA * a + v.g * o,
        v.wO * o + v.chi * abs(o) ** 2 * o + v.g * (a + b),
        v.wB * b + v.g * o,
    ])


def evolve(v: Vertex, y0, t_end: float, dt: float = 1e-3) -> tuple[np.ndarray, np.ndarray]:
    """RK4 integration. Returns (times, states[3, n])."""
    n = int(round(t_end / dt))
    y = np.array(y0, dtype=complex)
    out = np.empty((3, n + 1), dtype=complex)
    out[:, 0] = y
    for k in range(n):
        k1 = _rhs(v, y)
        k2 = _rhs(v, y + 0.5 * dt * k1)
        k3 = _rhs(v, y + 0.5 * dt * k2)
        k4 = _rhs(v, y + dt * k3)
        y = y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        out[:, k + 1] = y
    return np.linspace(0, n * dt, n + 1), out


def evolve_linear_exact(v: Vertex, y0, times) -> np.ndarray:
    """Exact propagator exp(-iHt) for chi = 0."""
    assert v.chi == 0.0
    w, U = np.linalg.eigh(v.linear_matrix())
    c = U.conj().T @ np.asarray(y0, dtype=complex)
    return np.array([U @ (np.exp(-1j * w * t) * c) for t in np.atleast_1d(times)]).T


def symmetric_transfer_exact(g: float, t):
    """Closed form for wA = wO = wB, start in A:
    a = (1 + cos(sqrt2 g t))/2,  b = (cos(sqrt2 g t) - 1)/2,
    o = -i sin(sqrt2 g t)/sqrt2."""
    w = np.sqrt(2) * g * np.asarray(t)
    return (1 + np.cos(w)) / 2, -1j * np.sin(w) / np.sqrt(2), (np.cos(w) - 1) / 2


def effective_exchange(g: float, delta_O: float) -> float:
    """Dispersive (virtual-vertex) limit |delta_O| >> g: eliminating o gives an
    effective A-B coupling J = g^2 / delta_O (both chambers also shift by J)."""
    return g ** 2 / delta_O


def rabi_max_transfer(J: float, detuning: float) -> float:
    """Maximum B occupation for a two-mode exchange with coupling J and
    detuning: J^2 / (J^2 + (detuning/2)^2)."""
    return J ** 2 / (J ** 2 + (detuning / 2) ** 2)


def max_transfer(v: Vertex, amplitude: float = 1.0, t_end: float = 40.0, dt: float = 2e-3) -> float:
    """Peak fraction of the initial occupation reaching TetB, start in TetA."""
    _, y = evolve(v, [amplitude, 0, 0], t_end, dt)
    return float(np.max(np.abs(y[2]) ** 2) / amplitude ** 2)


def band_ladder(n_bands: int = D + 1, w0: float = 1.0, scale: float = 1.0) -> np.ndarray:
    """Self-similar band frequencies 2^n w0 (scale multiplies the whole
    ladder, i.e. a uniformly larger or smaller partner structure)."""
    return scale * w0 * band_ratio() ** np.arange(n_bands)


def multiband_transfer(scale_B: float, g: float = 0.05, delta_O: float = 1.0,
                       w0: float = 1.0) -> np.ndarray:
    """Per-band peak transfer for TetA ladder vs a TetB ladder scaled by
    scale_B, each band coupled through its own dispersive vertex (band-
    diagonal assumption). Uses the exact linear propagator."""
    wA = band_ladder(w0=w0)
    wB = band_ladder(w0=w0, scale=scale_B)
    res = []
    J = effective_exchange(g, delta_O)
    for a_n, b_n in zip(wA, wB):
        v = Vertex(g=g, wA=a_n, wB=b_n, wO=a_n + delta_O)
        T = np.pi / abs(J) * 4
        ts = np.linspace(0, T, 4000)
        y = evolve_linear_exact(v, [1, 0, 0], ts)
        res.append(float(np.max(np.abs(y[2]) ** 2)))
    return np.array(res)
