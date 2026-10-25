#!/usr/bin/env python3
"""
closure_core256.py

A research harness for the proposed closure-node architecture:

    ClosureNode3:
        8-state hypercube / stella-octangula / Eisenstein closure node.
        A3 = <1,I> ⊕ Z[omega]^3.

    SierpinskiTile64:
        64-state two-node tensor tile.
        A3 ⊗ A3 = 8 × 8 = 64.
        Equivalent to a 6-cube / LUT-6 style block.

    ClosureCore256:
        Four 64-state Sierpinski tiles.
        4 × 64 = 256.
        This matches the full atlas size of 3-input Boolean truth tables: 2^(2^3)=256.

The file includes tests for:

    - cube/stella-octangula parity split;
    - body-diagonal cube→hexagon projection;
    - Walsh round-trip for all 256 3-input Boolean gates;
    - Clifford cocycle relations;
    - Eisenstein Omega closure phase;
    - Sierpinski count identities;
    - K=4 coupling polynomial values 21,17,13;
    - 40/24 face decomposition;
    - 64 tile and 256 core decomposition.

This is a buildable computational architecture, not a physics proof.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import atan2, isclose, pi
from typing import Callable, Dict, List, Tuple

import json
import numpy as np


# =============================================================================
# Basic 3-cube / Walsh / Clifford utilities
# =============================================================================

N3 = 8
MASKS3 = list(range(8))


def cube_vertices_3() -> np.ndarray:
    """Return the 8 vertices of {-1,+1}^3 in lexicographic order."""
    return np.array(list(product([-1, 1], repeat=3)), dtype=int)


VERTICES3 = cube_vertices_3()


def parity3(vertex: np.ndarray) -> int:
    """TetA/TetB parity character x1*x2*x3."""
    return int(np.prod(vertex))


def mask_grade(mask: int) -> int:
    """Hamming weight / Clifford grade of a 3-bit mask."""
    return int(mask.bit_count())


def walsh_matrix_3(vertices: np.ndarray = VERTICES3) -> np.ndarray:
    """
    H[v, mask] = chi_mask(v) = product of selected coordinates.
    mask bit 0 -> x1, bit 1 -> x2, bit 2 -> x3.
    """
    H = np.empty((len(vertices), N3), dtype=int)
    for row, v in enumerate(vertices):
        for mask in MASKS3:
            val = 1
            for bit in range(3):
                if (mask >> bit) & 1:
                    val *= int(v[bit])
            H[row, mask] = val
    return H


H3 = walsh_matrix_3()


def truth_to_walsh3(truth: np.ndarray) -> np.ndarray:
    """Convert an 8-entry truth vector to normalized Walsh coefficients."""
    truth = np.asarray(truth, dtype=float)
    if truth.shape != (8,):
        raise ValueError("truth must have shape (8,)")
    return H3.T @ truth / 8.0


def walsh_to_truth3(coeffs: np.ndarray) -> np.ndarray:
    """Reconstruct function values from Walsh coefficients."""
    coeffs = np.asarray(coeffs, dtype=float)
    if coeffs.shape != (8,):
        raise ValueError("coeffs must have shape (8,)")
    return H3 @ coeffs


def sign_readout(values: np.ndarray, zero_value: int = 1) -> np.ndarray:
    """Threshold real values to {-1,+1}; exact zero defaults to +1."""
    values = np.asarray(values, dtype=float)
    if zero_value == 1:
        return np.where(values >= 0, 1, -1).astype(int)
    return np.where(values > 0, 1, -1).astype(int)


def truth_from_int(code: int) -> np.ndarray:
    """
    8-bit truth table code to {-1,+1} values in vertex order.
    bit=1 -> +1, bit=0 -> -1.
    """
    if not 0 <= code <= 255:
        raise ValueError("code must be in [0,255]")
    return np.array([1 if ((code >> i) & 1) else -1 for i in range(8)], dtype=int)


def int_from_truth(truth: np.ndarray) -> int:
    """Convert {-1,+1} truth table to 8-bit integer code."""
    truth = np.asarray(truth, dtype=int)
    code = 0
    for i, val in enumerate(truth):
        if val > 0:
            code |= (1 << i)
    return code


def clifford_cocycle_3(a: int, b: int) -> int:
    """
    Cocycle for Cl(3,0):
        e_a e_b = sigma(a,b) e_{a xor b}
    with sigma(a,b)=(-1)^{sum_{i>j} a_i b_j}.
    """
    exponent = 0
    for i in range(3):
        if not ((a >> i) & 1):
            continue
        for j in range(i):
            exponent += ((b >> j) & 1)
    return -1 if exponent % 2 else 1


def clifford_mul_basis_3(a: int, b: int) -> Tuple[int, int]:
    """Return (sign, mask) for e_a * e_b."""
    return clifford_cocycle_3(a, b), a ^ b


def clifford_product_3(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Clifford product of two Cl(3,0) multivectors in mask basis."""
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    if A.shape != (8,) or B.shape != (8,):
        raise ValueError("A and B must have shape (8,)")
    C = np.zeros(8, dtype=float)
    for a, av in enumerate(A):
        if av == 0:
            continue
        for b, bv in enumerate(B):
            if bv == 0:
                continue
            s, m = clifford_mul_basis_3(a, b)
            C[m] += s * av * bv
    return C


# =============================================================================
# Closure coordinates: <1,I> ⊕ Z[omega]^3
# =============================================================================

@dataclass(frozen=True)
class ClosureCoords3:
    """
    Closure coordinates for A3 = <1,I> ⊕ Z[omega]^3.

    Canonical mask order:
        0: 1
        1: e1
        2: e2
        3: e12
        4: e3
        5: e13
        6: e23
        7: I=e123

    Hodge pairing convention:
        *e1 = e23
        *e2 = e31 = -e13
        *e3 = e12

    Therefore:
        z1 = c_e1 + c_e23 omega
        z2 = c_e2 + c_e31 omega = c_e2 - c_e13 omega
        z3 = c_e3 + c_e12 omega
    """
    a: float
    b: float
    z1: Tuple[float, float]
    z2: Tuple[float, float]
    z3: Tuple[float, float]

    def as_vector(self) -> np.ndarray:
        c = np.zeros(8, dtype=float)
        c[0] = self.a
        c[7] = self.b

        x1, y1 = self.z1
        x2, y2 = self.z2
        x3, y3 = self.z3

        c[1] = x1       # e1
        c[6] = y1       # e23

        c[2] = x2       # e2
        c[5] = -y2      # e13 = -e31

        c[4] = x3       # e3
        c[3] = y3       # e12
        return c


def to_closure_coords3(coeffs: np.ndarray) -> ClosureCoords3:
    coeffs = np.asarray(coeffs, dtype=float)
    if coeffs.shape != (8,):
        raise ValueError("coeffs must have shape (8,)")
    return ClosureCoords3(
        a=float(coeffs[0]),
        b=float(coeffs[7]),
        z1=(float(coeffs[1]), float(coeffs[6])),
        z2=(float(coeffs[2]), float(-coeffs[5])),
        z3=(float(coeffs[4]), float(coeffs[3])),
    )


def eisenstein_omega_pair(pair: Tuple[float, float]) -> Tuple[float, float]:
    """
    Multiply x + y omega by omega, where omega^2 + omega + 1 = 0:

        omega*(x + y omega)
        = x omega + y omega^2
        = x omega + y(-1-omega)
        = -y + (x-y) omega.
    """
    x, y = pair
    return (-y, x - y)


def omega_phase3(coeffs: np.ndarray) -> np.ndarray:
    """Omega fixes axial coordinates and multiplies each z_k by omega."""
    cc = to_closure_coords3(coeffs)
    return ClosureCoords3(
        a=cc.a,
        b=cc.b,
        z1=eisenstein_omega_pair(cc.z1),
        z2=eisenstein_omega_pair(cc.z2),
        z3=eisenstein_omega_pair(cc.z3),
    ).as_vector()


def omega_power3(coeffs: np.ndarray, k: int) -> np.ndarray:
    out = np.asarray(coeffs, dtype=float).copy()
    for _ in range(k % 3):
        out = omega_phase3(out)
    return out


def closure_projection3(coeffs: np.ndarray) -> np.ndarray:
    """P_Omega = (I + Omega + Omega^2)/3."""
    coeffs = np.asarray(coeffs, dtype=float)
    return (coeffs + omega_power3(coeffs, 1) + omega_power3(coeffs, 2)) / 3.0


def sweep_product3(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Closure product: Clifford multiply, then project to Omega-invariants."""
    return closure_projection3(clifford_product_3(A, B))


def gaussian_norm(pair: Tuple[float, float]) -> float:
    x, y = pair
    return float(x * x + y * y)


def eisenstein_norm(pair: Tuple[float, float]) -> float:
    x, y = pair
    return float(x * x - x * y + y * y)


def closure_norm3(coeffs: np.ndarray) -> float:
    """Additive closure norm: Gaussian axial norm plus 3 Eisenstein norms."""
    cc = to_closure_coords3(coeffs)
    return float(
        gaussian_norm((cc.a, cc.b))
        + eisenstein_norm(cc.z1)
        + eisenstein_norm(cc.z2)
        + eisenstein_norm(cc.z3)
    )


def grade_energies3(coeffs: np.ndarray) -> Dict[int, float]:
    coeffs = np.asarray(coeffs, dtype=float)
    return {
        grade: float(sum(coeffs[m] ** 2 for m in MASKS3 if mask_grade(m) == grade))
        for grade in range(4)
    }


def closure_channel_norms3(coeffs: np.ndarray) -> Dict[str, float]:
    cc = to_closure_coords3(coeffs)
    return {
        "axial_gaussian": gaussian_norm((cc.a, cc.b)),
        "z1_eisenstein": eisenstein_norm(cc.z1),
        "z2_eisenstein": eisenstein_norm(cc.z2),
        "z3_eisenstein": eisenstein_norm(cc.z3),
    }


# =============================================================================
# Buildable objects
# =============================================================================

@dataclass
class ClosureNode3:
    """
    One 8-state closure node.

    Externally:
        a 3-bit / 3-sign input addresses one of 8 cube vertices.

    Internally:
        8 Walsh/Clifford coefficients organized as:
            <1,I> ⊕ Z[omega]^3.
    """
    coeffs: np.ndarray

    def __post_init__(self) -> None:
        self.coeffs = np.asarray(self.coeffs, dtype=float)
        if self.coeffs.shape != (8,):
            raise ValueError("ClosureNode3 coeffs must have shape (8,)")

    @classmethod
    def from_truth(cls, truth: np.ndarray) -> "ClosureNode3":
        return cls(truth_to_walsh3(truth))

    @classmethod
    def from_boolean_code(cls, code: int) -> "ClosureNode3":
        return cls.from_truth(truth_from_int(code))

    @classmethod
    def constant(cls, value: int = 1) -> "ClosureNode3":
        return cls.from_truth(np.full(8, 1 if value >= 0 else -1, dtype=int))

    def evaluate_score(self, x: Tuple[int, int, int]) -> float:
        x = np.asarray(x, dtype=int)
        if x.shape != (3,):
            raise ValueError("x must be a 3-tuple")
        features = np.array([np.prod(x[[bit for bit in range(3) if (mask >> bit) & 1]]) if mask else 1 for mask in MASKS3], dtype=float)
        return float(features @ self.coeffs)

    def evaluate_sign(self, x: Tuple[int, int, int]) -> int:
        return 1 if self.evaluate_score(x) >= 0 else -1

    def truth(self) -> np.ndarray:
        return sign_readout(walsh_to_truth3(self.coeffs))

    def closure_coords(self) -> ClosureCoords3:
        return to_closure_coords3(self.coeffs)

    def closure_norm(self) -> float:
        return closure_norm3(self.coeffs)

    def channel_norms(self) -> Dict[str, float]:
        return closure_channel_norms3(self.coeffs)


@dataclass
class SierpinskiTile64:
    """
    64-state two-node tensor tile.

        Tile64 = A3 ⊗ A3 = 8 × 8 = 64.

    This is the 6-cube / LUT-6 scale object.

    It has two simultaneous decompositions:

    1. Tensor-family decomposition:
        (axial + 3 hex families)^2 = 1 + 3 + 3 + 9 = 16 families.
        Each family is 2×2 = 4 real coefficients.
        Total = 16 × 4 = 64.

    2. K=4 face/rank-2 decomposition:
        4 faces × 16 rank-2 channels per face = 64.
        Per face: 16 = 10 symmetric + 6 exterior.
        Therefore: 64 = 40 symmetric + 24 exterior.
    """
    left: ClosureNode3
    right: ClosureNode3
    face_count: int = 4

    @property
    def coeffs64(self) -> np.ndarray:
        return np.kron(self.left.coeffs, self.right.coeffs)

    @property
    def state_count(self) -> int:
        return 64

    @property
    def tensor_family_count(self) -> int:
        return 16

    def tensor_family_dimensions(self) -> Dict[str, int]:
        dims = {}
        family_names = ["A", "Z1", "Z2", "Z3"]
        for f1 in family_names:
            for f2 in family_names:
                dims[f"{f1}⊗{f2}"] = 4  # each family is 2 real dims × 2 real dims
        return dims

    def tensor_family_summary(self) -> Dict[str, int]:
        dims = self.tensor_family_dimensions()
        axial_axial = dims["A⊗A"]
        axial_hex = sum(v for k, v in dims.items() if k.startswith("A⊗Z"))
        hex_axial = sum(v for k, v in dims.items() if "⊗A" in k and k.startswith("Z"))
        hex_hex = sum(v for k, v in dims.items() if k.startswith("Z") and "⊗Z" in k)
        return {
            "axial_axial": axial_axial,
            "axial_hex": axial_hex,
            "hex_axial": hex_axial,
            "hex_hex": hex_hex,
            "total": axial_axial + axial_hex + hex_axial + hex_hex,
        }

    def face_rank2_summary(self) -> Dict[str, int]:
        K = self.face_count
        sym_per_face = K * (K + 1) // 2
        ext_per_face = K * (K - 1) // 2
        rank2_per_face = K * K
        return {
            "faces": K,
            "rank2_per_face": rank2_per_face,
            "sym_per_face": sym_per_face,
            "ext_per_face": ext_per_face,
            "sym_total": K * sym_per_face,
            "ext_total": K * ext_per_face,
            "total": K * rank2_per_face,
        }


@dataclass
class ClosureCore256:
    """
    Four 64-state Sierpinski tiles.

        Core256 = 4 × Tile64 = 4 × (A3 ⊗ A3) = 256.

    This matches the full count of 3-input Boolean gates:
        2^(2^3) = 256.

    This object is architectural: it is the four-face K=4 lift of the 64-state
    tensor tile.
    """
    tiles: List[SierpinskiTile64]

    def __post_init__(self) -> None:
        if len(self.tiles) != 4:
            raise ValueError("ClosureCore256 requires exactly four SierpinskiTile64 tiles")

    @classmethod
    def default(cls) -> "ClosureCore256":
        # Use simple basis-like nodes for each tile so the core is concrete.
        nodes = [
            ClosureNode3.from_boolean_code(255),  # constant +1
            ClosureNode3.from_boolean_code(0),    # constant -1
            ClosureNode3(np.eye(8)[1]),           # e1 coefficient basis
            ClosureNode3(np.eye(8)[7]),           # parity/I basis
            ClosureNode3(np.eye(8)[2]),
            ClosureNode3(np.eye(8)[6]),
            ClosureNode3(np.eye(8)[4]),
            ClosureNode3(np.eye(8)[3]),
        ]
        tiles = [
            SierpinskiTile64(nodes[0], nodes[1]),
            SierpinskiTile64(nodes[2], nodes[3]),
            SierpinskiTile64(nodes[4], nodes[5]),
            SierpinskiTile64(nodes[6], nodes[7]),
        ]
        return cls(tiles)

    def architecture_summary(self) -> Dict[str, int]:
        tile_states = sum(tile.state_count for tile in self.tiles)
        face_summaries = [tile.face_rank2_summary() for tile in self.tiles]
        return {
            "tiles": len(self.tiles),
            "states_per_tile": 64,
            "total_states": tile_states,
            "boolean_3_input_gate_count": 2 ** (2 ** 3),
            "sym_per_tile": face_summaries[0]["sym_total"],
            "ext_per_tile": face_summaries[0]["ext_total"],
            "sym_total": sum(s["sym_total"] for s in face_summaries),
            "ext_total": sum(s["ext_total"] for s in face_summaries),
        }


# =============================================================================
# Coupling polynomial / Sierpinski helpers
# =============================================================================

def coupling_f(K: int, s: int) -> int:
    return K * K + s * K + 1


def sierpinski_S(D: int, K: int) -> int:
    return sum(K ** (2 * k) for k in range(D))


def projective_plane_q2_count(K: int) -> int:
    # |P^2(F_{K^2})| = K^4 + K^2 + 1
    return K**4 + K**2 + 1


def coupling_summary(K: int = 4) -> Dict[str, int]:
    f_plus = coupling_f(K, +1)
    f_zero = coupling_f(K, 0)
    f_minus = coupling_f(K, -1)
    return {
        "K": K,
        "f_plus": f_plus,
        "f_zero": f_zero,
        "f_minus": f_minus,
        "product_plus_minus": f_plus * f_minus,
        "S_3_K": sierpinski_S(3, K),
        "P2_F_K2": projective_plane_q2_count(K),
        "sym_per_face": (f_plus - 1) // 2,
        "ext_per_face": (f_minus - 1) // 2,
        "four_face_sym": K * ((f_plus - 1) // 2),
        "four_face_ext": K * ((f_minus - 1) // 2),
        "four_face_total": K * K * K,
    }


def boolean_gate_atlas() -> List[Dict[str, object]]:
    rows = []
    for code in range(256):
        truth = truth_from_int(code)
        coeffs = truth_to_walsh3(truth)
        rows.append(
            {
                "code": code,
                "truth": truth,
                "coeffs": coeffs,
                "closure_norm": closure_norm3(coeffs),
                "grade_energy": grade_energies3(coeffs),
                "channel_norms": closure_channel_norms3(coeffs),
            }
        )
    return rows


# =============================================================================
# Geometry: cube → hexagon projection
# =============================================================================

def body_diagonal_projection(vertices: np.ndarray = VERTICES3) -> np.ndarray:
    """
    Project vertices onto the plane perpendicular to the body diagonal (1,1,1).

    Returns 3D projected coordinates lying in the plane sum(x)=0.
    """
    d = np.array([1.0, 1.0, 1.0])
    d = d / np.linalg.norm(d)
    verts = vertices.astype(float)
    return verts - (verts @ d)[:, None] * d[None, :]


def hexagon_projection_summary() -> Dict[str, object]:
    P = body_diagonal_projection()
    radii = np.linalg.norm(P, axis=1)
    origin_count = int(np.sum(np.isclose(radii, 0.0)))
    nonzero = P[~np.isclose(radii, 0.0)]
    nonzero_radii = np.linalg.norm(nonzero, axis=1)

    # Build an orthonormal basis for the projection plane to compute angles.
    u = np.array([1.0, -1.0, 0.0])
    u = u / np.linalg.norm(u)
    v = np.cross(np.array([1.0, 1.0, 1.0]) / np.sqrt(3.0), u)
    coords2 = np.column_stack([nonzero @ u, nonzero @ v])
    angles = np.sort(np.mod(np.arctan2(coords2[:, 1], coords2[:, 0]), 2 * np.pi))
    diffs = np.diff(np.r_[angles, angles[0] + 2 * np.pi])

    return {
        "origin_count": origin_count,
        "nonzero_count": int(len(nonzero)),
        "nonzero_radius_squared_values": sorted(set(np.round(nonzero_radii ** 2, 12).tolist())),
        "angle_step_values_radians": sorted(set(np.round(diffs, 12).tolist())),
    }


# =============================================================================
# Tests
# =============================================================================

def run_tests(verbose: bool = True) -> Dict[str, object]:
    results = {}

    def check(condition: bool, name: str) -> None:
        if not condition:
            raise AssertionError(f"FAILED: {name}")
        if verbose:
            print(f"PASS: {name}")

    # Cube and stella-octangula parity split.
    check(VERTICES3.shape == (8, 3), "3-cube has 8 vertices")
    parities = np.array([parity3(v) for v in VERTICES3])
    check(int(np.sum(parities == 1)) == 4, "TetA parity +1 has 4 vertices")
    check(int(np.sum(parities == -1)) == 4, "TetB parity -1 has 4 vertices")

    for p in [+1, -1]:
        tetra = VERTICES3[parities == p]
        d2 = []
        for i in range(4):
            for j in range(i + 1, 4):
                d2.append(int(np.sum((tetra[i] - tetra[j]) ** 2)))
        check(set(d2) == {8}, f"parity {p:+d} vertices form a regular tetrahedron")

    # Cube -> hexagon projection.
    hex_summary = hexagon_projection_summary()
    check(hex_summary["origin_count"] == 2, "body-diagonal projection has 2 axial/core vertices")
    check(hex_summary["nonzero_count"] == 6, "body-diagonal projection has 6 hexagon vertices")
    check(hex_summary["nonzero_radius_squared_values"] == [round(8/3, 12)], "hexagon vertices have radius^2 = 8/3")
    check(len(hex_summary["angle_step_values_radians"]) == 1, "hexagon angular steps are equal")

    # Walsh.
    check(np.array_equal(H3.T @ H3, 8 * np.eye(8, dtype=int)), "Walsh matrix satisfies H^T H = 8I")
    for code in range(256):
        truth = truth_from_int(code)
        coeffs = truth_to_walsh3(truth)
        recon = walsh_to_truth3(coeffs)
        if not np.allclose(recon, truth):
            raise AssertionError(f"Walsh round trip failed for code {code}")
    check(True, "Walsh round trips all 256 three-input Boolean functions")

    # Clifford.
    vec_masks = [1, 2, 4]
    for m in vec_masks:
        s, out = clifford_mul_basis_3(m, m)
        check(s == 1 and out == 0, f"Clifford e_mask_{m} squares to +1")
    for i, a in enumerate(vec_masks):
        for b in vec_masks[i+1:]:
            s_ab, m_ab = clifford_mul_basis_3(a, b)
            s_ba, m_ba = clifford_mul_basis_3(b, a)
            check(m_ab == m_ba and s_ab == -s_ba, f"Clifford anti-commutation e_{a}e_{b}=-e_{b}e_{a}")

    # Closure coordinates and Omega.
    rng = np.random.default_rng(123)
    for _ in range(50):
        coeffs = rng.normal(size=8)
        check(np.allclose(to_closure_coords3(coeffs).as_vector(), coeffs), "closure coordinate round trip")
        check(np.allclose(omega_power3(coeffs, 3), coeffs), "Omega^3 = identity")
        check(isclose(closure_norm3(coeffs), closure_norm3(omega_phase3(coeffs)), rel_tol=1e-10, abs_tol=1e-10),
              "closure norm is Omega-invariant")

    for m in [1, 2, 3, 4, 5, 6]:
        coeffs = np.zeros(8)
        coeffs[m] = 1.0
        summed = coeffs + omega_power3(coeffs, 1) + omega_power3(coeffs, 2)
        check(np.allclose(summed, np.zeros(8)), f"Omega^2+Omega+1=0 on middle mask {m}")

    for _ in range(25):
        coeffs = rng.normal(size=8)
        P = closure_projection3(coeffs)
        check(np.allclose(closure_projection3(P), P), "closure projection is idempotent")
        check(np.allclose(P[[1,2,3,4,5,6]], 0.0), "closure projection kills middle grades")
        check(np.allclose(P[[0,7]], coeffs[[0,7]]), "closure projection preserves axial grades")

    # Coupling / Sierpinski.
    cs = coupling_summary(4)
    check(cs["f_plus"] == 21, "f(4,+1)=21")
    check(cs["f_zero"] == 17, "f(4,0)=17")
    check(cs["f_minus"] == 13, "f(4,-1)=13")
    check(cs["product_plus_minus"] == 273, "f(4,+1)f(4,-1)=273")
    check(cs["S_3_K"] == 273 and cs["P2_F_K2"] == 273, "S(3,4)=|P^2(F_16)|=273")
    check(cs["sym_per_face"] == 10 and cs["ext_per_face"] == 6, "per-face split is 10+6")
    check(cs["four_face_sym"] == 40 and cs["four_face_ext"] == 24, "four-face split is 40+24")
    check(cs["four_face_total"] == 64, "four-face rank-2 total is 64")

    # Tile and core.
    a = ClosureNode3.from_boolean_code(255)
    b = ClosureNode3.from_boolean_code(0)
    tile = SierpinskiTile64(a, b)
    check(tile.coeffs64.shape == (64,), "SierpinskiTile64 has 64 tensor coefficients")
    tf = tile.tensor_family_summary()
    check(tf["total"] == 64, "tensor family decomposition totals 64")
    check(tf["axial_axial"] == 4 and tf["axial_hex"] == 12 and tf["hex_axial"] == 12 and tf["hex_hex"] == 36,
          "tensor families decompose as 4+12+12+36")
    fr = tile.face_rank2_summary()
    check(fr["sym_total"] == 40 and fr["ext_total"] == 24 and fr["total"] == 64,
          "tile face/rank-2 split is 40+24=64")

    core = ClosureCore256.default()
    summary = core.architecture_summary()
    check(summary["total_states"] == 256, "ClosureCore256 has 256 total states")
    check(summary["boolean_3_input_gate_count"] == 256, "ClosureCore256 matches all 3-input Boolean gate count")
    check(summary["sym_total"] == 160 and summary["ext_total"] == 96, "four tiles give 160 symmetric + 96 exterior")

    # Boolean atlas.
    atlas = boolean_gate_atlas()
    norms = sorted(set(round(row["closure_norm"], 12) for row in atlas))
    norm_counts = {n: sum(1 for row in atlas if round(row["closure_norm"], 12) == n) for n in norms}
    check(len(atlas) == 256, "Boolean atlas has 256 gates")
    check(sum(norm_counts.values()) == 256, "closure norm buckets sum to 256")

    results["hexagon_projection"] = hex_summary
    results["coupling_summary_K4"] = cs
    results["tile_tensor_family_summary"] = tf
    results["tile_face_rank2_summary"] = fr
    results["core_summary"] = summary
    results["closure_norm_distribution"] = norm_counts

    if verbose:
        print("\n=== Coupling summary K=4 ===")
        print(json.dumps(cs, indent=2))
        print("\n=== Tile tensor family summary ===")
        print(json.dumps(tf, indent=2))
        print("\n=== Tile face/rank-2 summary ===")
        print(json.dumps(fr, indent=2))
        print("\n=== Core summary ===")
        print(json.dumps(summary, indent=2))
        print("\n=== Closure norm distribution across all 256 3-input gates ===")
        for n, count in norm_counts.items():
            print(f"  norm={n:g}: {count:3d} gates")

    return results


if __name__ == "__main__":
    run_tests(verbose=True)
