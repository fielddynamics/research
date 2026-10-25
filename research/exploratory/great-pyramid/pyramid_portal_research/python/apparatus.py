"""
apparatus.py
============

Pyramid apparatus operators:

  - King's Chamber vertex
  - Shaft triad: directions, lengths, Gram matrix, chirality, phase
  - Address structures and the mirror match functional M(U, V)
  - Internal subsystem operators: apex collector, granite isolation,
    ascending passage, Grand Gallery Z_7 kernel, Z_3 projector,
    Z_21 sectors and comb, big void cavity, coffer reflection
  - K/Q interferometer
  - Universal vertex order parameter, Landau potential, Josephson current
  - Full portal machine and scalar reciprocal apparatus operator

References: project §04 apparatus engineering, §05 cavity-QED operation, §06
master equations; legacy §5-§9, §12, §14.
"""

from __future__ import annotations

import cmath
from dataclasses import dataclass
from itertools import permutations
from math import cos, exp, isclose, sin, sqrt
from typing import Dict, Iterable, List, Sequence, Tuple

from .constants import TAU
from .gravity import alpha_gravity


# =============================================================================
# Vector / triad utilities
# =============================================================================

Vector3 = Tuple[float, float, float]


def dot(a: Vector3, b: Vector3) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm(v: Vector3) -> float:
    return sqrt(dot(v, v))


def normalize(v: Vector3) -> Vector3:
    n = norm(v)
    if n == 0:
        raise ValueError("Cannot normalize zero vector.")
    return (v[0] / n, v[1] / n, v[2] / n)


def gram_matrix(triad: Sequence[Vector3]) -> Tuple[Tuple[float, float, float], ...]:
    """Gram matrix G_ij = u_i . u_j for a 3-vector triad (normalized)."""
    if len(triad) != 3:
        raise ValueError("Triad must have exactly 3 vectors.")
    u = [normalize(v) for v in triad]
    return tuple(tuple(dot(u[i], u[j]) for j in range(3)) for i in range(3))


def determinant_3(triad: Sequence[Vector3]) -> float:
    """Determinant of a 3-vector triad with vectors as columns."""
    if len(triad) != 3:
        raise ValueError("Triad must have exactly 3 vectors.")
    a, b, c = triad
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - b[0] * (a[1] * c[2] - a[2] * c[1])
        + c[0] * (a[1] * b[2] - a[2] * b[1])
    )


def chirality(triad: Sequence[Vector3], tol: float = 1e-12) -> int:
    """Signed chirality of the triad: +1 right-handed, -1 left-handed, 0 degenerate."""
    d = determinant_3([normalize(v) for v in triad])
    if d > tol:
        return 1
    if d < -tol:
        return -1
    return 0


def phase_closed(theta: float, tol: float = 1e-9) -> bool:
    """Check theta = 0 mod 2*pi."""
    m = theta % TAU
    return isclose(m, 0.0, abs_tol=tol) or isclose(m, TAU, abs_tol=tol)


# =============================================================================
# King's Chamber vertex
# =============================================================================

@dataclass(frozen=True)
class KingsChamberVertex:
    """
    Algebraic King's Chamber local vertex:
        V_KC(x) = J_4(x) * alpha_G

    Once the pentachoron phases close.
    """
    alpha_G: float
    band: int = 21
    source_state: str = "|4, +>"
    receiver_state: str = "|5, ->"

    def as_string(self) -> str:
        return (f"V_KC: {self.source_state} -> {self.receiver_state}, "
                f"band={self.band}, amplitude={self.alpha_G:.6e}")


def kings_chamber_vertex() -> KingsChamberVertex:
    return KingsChamberVertex(alpha_G=alpha_gravity())


def portal_scalar_amplitude(mirror_selector: float, alpha_G: float | None = None) -> float:
    """
    Scalar amplitude of the portal operator:
        P = alpha_G * J_4^dagger M J_4

    Here M is a scalar in [0, 1].
    """
    if alpha_G is None:
        alpha_G = alpha_gravity()
    return alpha_G * mirror_selector


# =============================================================================
# Shaft triad and address structure
# =============================================================================

@dataclass(frozen=True)
class ShaftKey:
    direction: Vector3
    length: float
    impedance: float
    omega: float
    phase: float
    band: int

    @property
    def wavenumber(self) -> float:
        # toy relation with c=1 natural units
        return self.omega

    @property
    def accumulated_phase(self) -> float:
        return self.phase + self.wavenumber * self.length


def triadic_phase(keys: Sequence[ShaftKey]) -> float:
    """Theta_U = sum_i (phi_i + k_i * ell_i)."""
    if len(keys) != 3:
        raise ValueError("Need exactly three shaft keys.")
    return sum(k.accumulated_phase for k in keys)


@dataclass(frozen=True)
class Address:
    triad: Tuple[Vector3, Vector3, Vector3]
    gram: Tuple[Tuple[float, float, float], ...]
    chirality: int
    phase: float
    band: int


def make_address(keys: Sequence[ShaftKey]) -> Address:
    triad = tuple(normalize(k.direction) for k in keys)
    return Address(
        triad=triad,  # type: ignore[arg-type]
        gram=gram_matrix(triad),
        chirality=chirality(triad),
        phase=triadic_phase(keys),
        band=keys[0].band,
    )


# =============================================================================
# Mirror match functional M(U, V)
# =============================================================================

def permute_gram(G: Tuple[Tuple[float, float, float], ...],
                 p: Tuple[int, int, int]) -> Tuple[Tuple[float, float, float], ...]:
    """Apply a vertex permutation to a Gram matrix: G' = P^T G P."""
    return tuple(tuple(G[p[i]][p[j]] for j in range(3)) for i in range(3))


def gram_distance(G1, G2) -> float:
    return sqrt(sum((G1[i][j] - G2[i][j]) ** 2 for i in range(3) for j in range(3)))


def mirror_match_functional(
    source: Address,
    target: Address,
    epsilon: float = 1e-6,
    phase_tolerance: float = 1e-6,
) -> float:
    """
    Mirror selector:
        M(U, V) = sum_P exp(-||G_U - P^T G_V P||^2 / eps^2)
                  * (1 - chi_U * chi_V) / 2
                  * delta_phase

    delta_phase is approximated as 1 if the phase difference closes mod 2*pi,
    else 0. Result is clamped to [0, 1].
    """
    chirality_factor = (1 - source.chirality * target.chirality) / 2
    if chirality_factor <= 0:
        return 0.0

    dphase = (source.phase - target.phase) % TAU
    phase_factor = 1.0 if phase_closed(dphase, tol=phase_tolerance) else 0.0
    if phase_factor == 0.0:
        return 0.0

    score = 0.0
    for p in permutations((0, 1, 2)):
        Gp = permute_gram(target.gram, p)
        d = gram_distance(source.gram, Gp)
        score += exp(-(d * d) / (epsilon * epsilon))

    return min(1.0, score * chirality_factor * phase_factor)


# =============================================================================
# Internal subsystem operators
# =============================================================================

def apex_top_collector(env_flux_derivative: float, capacitance: float, eta: float = 1.0) -> float:
    """Apex / gold-top field collector: T_top = eta * C_apex * dPhi_env/dt."""
    return eta * capacitance * env_flux_derivative


def granite_isolation(leak_gamma: float, wall_length: float) -> float:
    """Granite isolation / leakage suppression: I_granite = exp(-gamma_leak * L_wall)."""
    return exp(-leak_gamma * wall_length)


def ascending_passage_gain(gamma: float, length: float, phase_k: float) -> complex:
    """Ascending passage coherent 21-band injector: A_asc = exp(gamma L) exp(i k L)."""
    return exp(gamma * length) * cmath.exp(1j * phase_k * length)


def grand_gallery_z7_kernel(index_from_zero: bool = True) -> Dict[str, object]:
    """
    Grand Gallery Z_7 phase kernel.

    k = 0..6: sum k = 21, theta = (2*pi/7) * 21 = 6*pi = 0 mod 2*pi.
    k = 1..7: sum k = 28, theta = (2*pi/7) * 28 = 8*pi = 0 mod 2*pi.
    """
    from math import pi as _pi
    ks = range(0, 7) if index_from_zero else range(1, 8)
    s = sum(ks)
    theta = (TAU / 7) * s
    return {
        "index_sum": s,
        "theta_radians": theta,
        "theta_over_pi": theta / _pi,
        "closed": phase_closed(theta),
        "determinant_phase": cmath.exp(1j * theta),
    }


def z3_projector_eigenvalue(m: int) -> complex:
    """
    Z_3 closure projector eigenvalue for sector m:
        P_3 = (1/3)(1 + omega^m + omega^(2m)),  omega = exp(2*pi*i/3)

    Equals 1 for m = 0 mod 3, else 0.
    """
    omega = cmath.exp(TAU * 1j / 3)
    return (1 + omega ** m + omega ** (2 * m)) / 3


def z21_phase_sectors() -> List[complex]:
    """Twenty-one roots of unity."""
    return [cmath.exp(TAU * 1j * n / 21) for n in range(21)]


def z21_comb_frequencies(f0: float, ideal_equal_spacing: bool = True) -> List[float]:
    """
    Ideal Z_21 comb model: 21 character sectors at equal spacing.
    """
    if not ideal_equal_spacing:
        raise NotImplementedError("Nonuniform character-sector spectrum is model-dependent.")
    return [f0 + n * (f0 / 21) for n in range(21)]


def big_void_balance_cavity(omega: float, omega_26: float, gamma_26: float) -> complex:
    """
    Big Void / 26-band reservoir toy response:
        C_void = 1 / (omega_26^2 - omega^2 + i*omega*gamma_26)
    """
    return 1 / complex(omega_26 * omega_26 - omega * omega, omega * gamma_26)


def coffer_reflection_coefficient(Z_coffer: complex, Z_kc: complex) -> complex:
    """Coffer load reflection coefficient: Gamma = (Z_C - conj(Z_KC)) / (Z_C + Z_KC)."""
    return (Z_coffer - Z_kc.conjugate()) / (Z_coffer + Z_kc)


# =============================================================================
# K/Q interferometer
# =============================================================================

@dataclass(frozen=True)
class KQInterferometer:
    king_address: Address
    queen_address: Address

    @property
    def address_phase(self) -> float:
        """Theta_addr = Theta_K - Theta_Q (mod 2*pi)."""
        return (self.king_address.phase - self.queen_address.phase) % TAU

    @property
    def differential_chirality(self) -> Tuple[int, int]:
        return (self.king_address.chirality, self.queen_address.chirality)


def kq_phase_lock(
    kq: KQInterferometer,
    target_phase: float,
    tolerance: float = 1e-6,
) -> bool:
    """K/Q phase lock: Theta_K - Theta_Q - Theta_target = 0 mod 2*pi."""
    return phase_closed(kq.address_phase - target_phase, tol=tolerance)


# =============================================================================
# Universal vertex order parameter
# =============================================================================

def z21_order_parameter(theta_values: Iterable[float]) -> complex:
    """
    Omega_21 = average of exp(i * 21 * theta).

    Perfect Z_21 lock gives |Omega_21| = 1; incoherent phases tend toward 0.
    """
    vals = list(theta_values)
    if not vals:
        raise ValueError("Need at least one theta.")
    return sum(cmath.exp(1j * 21 * t) for t in vals) / len(vals)


def landau_z21_potential(rho: float, theta: float, a: float, b: float, h21: float) -> float:
    """Toy Landau potential: V = a*rho^2 + b*rho^4 - 2*h21*rho^21*cos(21*theta)."""
    return a * rho * rho + b * rho ** 4 - 2 * h21 * rho ** 21 * cos(21 * theta)


def josephson_portal_current(Ic: float, theta_x: float, theta_y: float, address_holonomy: float) -> float:
    """Josephson-style portal current: I = Ic * sin(21*(theta_x - theta_y) - A_xy)."""
    return Ic * sin(21 * (theta_x - theta_y) - address_holonomy)


# =============================================================================
# Portal machine and reciprocal apparatus operator
# =============================================================================

@dataclass(frozen=True)
class PortalMachine:
    """
    Bundled scalar/selector version of the full portal operator:
        P_{x->y} = A_y^dagger J_y^dagger M alpha_G J_x A_x
    """
    alpha_G: float
    mirror_selector: float
    source_apparatus_gain: complex = 1 + 0j
    receiver_apparatus_gain: complex = 1 + 0j

    @property
    def amplitude(self) -> complex:
        return (
            self.receiver_apparatus_gain.conjugate()
            * self.alpha_G
            * self.mirror_selector
            * self.source_apparatus_gain
        )


def local_force_kernel(alpha_G: float, r: float) -> float:
    """Local gravity-style mode: alpha_G / r."""
    if r <= 0:
        raise ValueError("r must be positive.")
    return alpha_G / r


def portal_address_kernel(alpha_G: float, mirror_selector: float) -> float:
    """Portal address mode: alpha_G * M(U, V)."""
    return alpha_G * mirror_selector


def reciprocal_two_apparatus_operator_scalar(
    source_gain: complex,
    receiver_gain: complex,
    mirror_selector: float,
    alphaG: float | None = None,
) -> complex:
    """
    Reciprocal two-apparatus transfer (scalar model):
        P_{y<-x} = A_y^dagger J_y^dagger M alpha_G J_x A_x
    """
    if alphaG is None:
        alphaG = alpha_gravity()
    return receiver_gain.conjugate() * mirror_selector * alphaG * source_gain


def apparatus_operator_stack(
    top: complex,
    asc: complex,
    plug_iso: complex,
    gallery: complex,
    z3_gate: complex,
    coffer_load: complex,
    granite: complex,
    kc_vertex: complex,
) -> complex:
    """
    Scalar version of the apparatus stack:
        A = I_granite * V_KC * Z_C * P_3 * L_7 * I_3 * A_asc * T_top
    """
    return granite * kc_vertex * coffer_load * z3_gate * gallery * plug_iso * asc * top


def complement_projector_mode(selected_21_component: float, total: float = 1.0) -> Dict[str, float]:
    """
    Descending / subterranean failed-lock sink as complement projector:
        Pi_perp = I - Pi_21
    """
    rejected = total - selected_21_component
    return {
        "accepted_21_channel": selected_21_component,
        "rejected_complement_channel": rejected,
    }


def well_shaft_feedback(beta: float, theta: float) -> complex:
    """Well-shaft / grotto feedback: W = beta * exp(i*theta)."""
    return beta * cmath.exp(1j * theta)
