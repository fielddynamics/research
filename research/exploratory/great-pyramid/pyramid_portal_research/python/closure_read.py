"""
closure_read.py
===============

Closure-read representation of the GFD framework at level K:

    C_K = Lambda^K V  oplus  V  oplus  (V tensor V)

Equivalently, the truncated tensor algebra T_<=2(V) = 1 oplus V oplus V tensor V
graded by tensor degree mod 2.

Exports:
  - Matrix utilities (diag, matmul, matrix_equal)
  - Shell Hamiltonian H_K = diag(Phi_6, Phi_4, Phi_3)
  - Truncated tensor algebra dimension breakdown
  - Parity projectors P_0, P_1, P_2 (dimensional traces)
  - Graded identity operator trace Tr(I_s) = 1 + s*K + K^2
  - Two-sheet Gram matrix and its eigenvalues {2E - O, K}
  - Parity-overlap angle theta_K and sec(theta_K)
  - Hilbert polynomial H_K(t) = 1 + K*t + K^2 * t^2
"""

from __future__ import annotations

from math import acos, cos, pi
from typing import Dict, List, Sequence, Tuple

from .cyclotomic import phi3, phi4, phi6, shell


# =============================================================================
# Type aliases and elementary matrix utilities
# =============================================================================

Matrix = List[List[float]]


def diag(values: Sequence[float]) -> Matrix:
    """Build a diagonal matrix from a sequence of values."""
    n = len(values)
    return [[values[i] if i == j else 0.0 for j in range(n)] for i in range(n)]


def matmul(A: Matrix, B: Matrix) -> Matrix:
    """Multiply two matrices A * B."""
    rows, mid, cols = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(mid)) for j in range(cols)]
            for i in range(rows)]


def matrix_equal(A: Matrix, B: Matrix, tol: float = 1e-12) -> bool:
    """Pointwise matrix equality within tolerance."""
    return all(abs(A[i][j] - B[i][j]) <= tol
               for i in range(len(A))
               for j in range(len(A[0])))


# =============================================================================
# Shell Hamiltonian
# =============================================================================

def shell_hamiltonian(K: int) -> Matrix:
    """
    H_K = diag(Phi_6(K), Phi_4(K), Phi_3(K))

    Basis order: |K, ->, |K, 0>, |K, +>
    (lower / neutral / upper cyclotomic readings).
    """
    sh = shell(K)
    return diag([sh.lower, sh.neutral, sh.upper])


# =============================================================================
# Truncated tensor algebra T_<=2(V)  [Active Work 03, 04]
# =============================================================================

def truncated_tensor_algebra(K: int) -> Dict[str, object]:
    """
    Dimension breakdown of the truncated tensor algebra T_<=2(V) at dim V = K:

        T_<=2(V) = 1 oplus V oplus (V tensor V)
                 = (Z/2-even: 1 oplus V tensor V)  oplus  (Z/2-odd: V)

    The shell C_K = (superdim, even-dim, total-dim) is the parity-graded
    character.
    """
    even = 1 + K * K
    odd = K
    return {
        "K": K,
        "dim_trivial":     1,
        "dim_V":           K,
        "dim_V_tensor_V":  K * K,
        "total_dimension": 1 + K + K * K,
        "even_dimension":  even,    # E_K = K^2 + 1
        "odd_dimension":   odd,     # O_K = K
        "superdimension":  even - odd,  # C_K = K^2 - K + 1
        "shell":           shell(K).tuple,
    }


def parity_projector_dimensions(K: int) -> Dict[str, int]:
    """
    Dimensions of the three canonical projectors on C_K:
        P_0 on Lambda^K V       (dim 1)
        P_1 on V                (dim K)
        P_2 on V tensor V       (dim K^2)
    """
    return {"P_0": 1, "P_1": K, "P_2": K * K}


def graded_identity_trace(K: int, s: int | float) -> int | float:
    """
    Trace of the graded identity I_s = P_0 + s*P_1 + P_2:
        Tr(I_s) = 1 + s*K + K^2

    At Niven integer s:
        s = +1  ->  Phi_3(K)
        s =  0  ->  Phi_4(K)
        s = -1  ->  Phi_6(K)
    """
    return 1 + s * K + K * K


# =============================================================================
# Two-sheet Gram matrix and parity-overlap angle  [Active Work 03]
# =============================================================================

def gram_matrix_K(K: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    TetA / TetB two-sheet incidence Gram:

        G_K = [[E,    E-O],
               [E-O,  E ]]

    with E = K^2 + 1 and O = K, equivalently
        G_K = [[Phi_4(K),  Phi_6(K)],
               [Phi_6(K),  Phi_4(K)]].
    """
    E = phi4(K)
    C = phi6(K)  # = E - O
    return ((E, C), (C, E))


def gram_eigenvalues(K: int) -> Dict[str, int]:
    """
    Eigenvalues of the two-sheet Gram matrix:

        symmetric eigenmode  ( (1,  1) / sqrt(2) ):  lambda_+ = 2E - O = E + Phi_3(K) - K^2
        antisymmetric eigenmode ( (1, -1) / sqrt(2) ):  lambda_- = O = K

    The antisymmetric eigenvalue equals K exactly. This is a spectral
    identification of K as the parity-antisymmetric charge of the overlap.
    """
    E = phi4(K)
    O = K
    return {
        "lambda_symmetric_2E_minus_O": 2 * E - O,    # at K=4: 2*17 - 4 = 30
        "lambda_antisymmetric_O":      O,            # at K=4: 4
        "trace_2E":                    2 * E,
        "det_E_squared_minus_C_squared": E * E - (E - O) ** 2,
    }


def parity_overlap_angle(K: int) -> float:
    """
    Parity-overlap angle between the TetA and TetB incidence vectors:

        cos(theta_K) = (E - O) / E = Phi_6(K) / Phi_4(K)

    At K=4: cos(theta_4) = 13/17, theta_4 = arccos(13/17) ≈ 40.00°.
    """
    return acos(phi6(K) / phi4(K))


def sec_theta_K(K: int) -> float:
    """
    Secant of the parity-overlap angle:
        sec(theta_K) = E / (E - O) = Phi_4(K) / Phi_6(K)

    At K=4: sec(theta_4) = 17/13. This is the algebraic origin of the tetrad
    impedance ratio in the gravity equation.
    """
    return phi4(K) / phi6(K)


def verify_17_over_13_is_sec_theta_4(tol: float = 1e-12) -> bool:
    """Explicit check: 17/13 = sec(theta_4) = sec(arccos(13/17))."""
    return abs(sec_theta_K(4) - 17.0 / 13.0) < tol


# =============================================================================
# Hilbert polynomial  [Active Work 03, 04]
# =============================================================================

def hilbert_polynomial(K: int, t: float) -> float:
    """
    Graded Hilbert polynomial of T_<=2(V):
        H_K(t) = 1 + K*t + K^2 * t^2

    Identities:
        H_K(+1) = Phi_3(K)   (total dimension)
        H_K(-1) = Phi_6(K)   (superdimension)
        (H_K(+1) + H_K(-1)) / 2 = Phi_4(K)   (even dimension)
    """
    return 1 + K * t + (K * K) * (t * t)


# =============================================================================
# Parity-sheet inclusion-exclusion reading  [AW 11 / field-origin synthesis]
# =============================================================================

def parity_sheet_inclusion_exclusion(K: int) -> Dict[str, int]:
    """
    TetA / TetB as parity sheets at level K. Each sheet has E_K = Phi_4(K)
    states; they share an overlap core of (E_K - O_K) = Phi_6(K); their
    union is E_K + O_K = Phi_3(K).

    At K=4:
        |A| = |B| = 17       (each parity sheet)
        |A ∩ B| = 13         (shared TetA/TetB core)
        |A ∪ B| = 21         (full closure)
        17 + 17 - 13 = 21    (inclusion-exclusion)
        21 = 13 + K + K      (parity decomposition: core + sheet-exclusive x 2)

    The 17/13 impedance is the ratio |sheet|/|core|, geometrically the
    secant of the overlap angle between the two parity-incidence vectors.
    """
    E_K = phi4(K)                # 17 at K=4 — each sheet's dimension
    O_K = K                      # 4 at K=4 — sheet-exclusive content
    core = E_K - O_K             # 13 at K=4 — shared overlap
    union = E_K + O_K            # 21 at K=4 — full closure
    return {
        'K': K,
        'sheet_A_size': E_K,
        'sheet_B_size': E_K,
        'intersection_size': core,
        'union_size': union,
        'sheet_minus_core': O_K,
        'inclusion_exclusion_holds': (E_K + E_K - core == union),
        'parity_decomposition_holds': (union == core + 2 * K),
        'impedance_Z_K': E_K / core,
    }


def parity_sheet_dot_products(K: int) -> Dict[str, int]:
    """
    Read (13, 17, 21) as Gram-matrix entries of two parity-incidence
    vectors A, B in the K-graded space:

        <A, A> = <B, B> = Phi_4(K)            (each sheet's self-overlap)
        <A, B> = Phi_4(K) - K = Phi_6(K)      (cross-sheet overlap)

    At K=4:
        <A, A> = <B, B> = 17
        <A, B> = 13
        cos(theta_K) = <A, B> / sqrt(<A, A> <B, B>) = 13/17
        sec(theta_K) = 17/13                 (overlap-impedance secant)
    """
    self_overlap = phi4(K)       # 17
    cross_overlap = phi6(K)      # 13
    return {
        'K': K,
        'A_dot_A': self_overlap,
        'B_dot_B': self_overlap,
        'A_dot_B': cross_overlap,
        'cos_theta_K': cross_overlap / self_overlap,  # 13/17
        'sec_theta_K': self_overlap / cross_overlap,  # 17/13
    }


def parity_overlap_angle_geometric(K: int) -> float:
    """
    The overlap angle theta_K between the two parity-incidence vectors,
    computed directly from the Gram-matrix dot products. Same value as
    parity_overlap_angle(K) but with the explicit geometric construction.
    """
    dots = parity_sheet_dot_products(K)
    cos_theta = dots['A_dot_B'] / dots['A_dot_A']
    return acos(cos_theta)
