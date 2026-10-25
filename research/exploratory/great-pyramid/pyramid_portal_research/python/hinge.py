"""
hinge.py
========

The K=4 <-> K=5 portal hinge of the framework:

    Phi_3(4) = 21 = Phi_6(5)

Identifies the shared 21-dimensional sector across the cyclotomic shift,
realized as a partial isometry J_4 = |5, -><4, +| with intertwining identity
H_5 J_4 = J_4 H_4 = 21 J_4.

References: project §03.1, §06.1; legacy §2-§3.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .closure_read import Matrix, matmul, matrix_equal, shell_hamiltonian
from .cyclotomic import Shell, shell


# =============================================================================
# The K=4 / K=5 hinge object
# =============================================================================

@dataclass(frozen=True)
class PyramidHinge:
    """Algebraic description of the K=4 -> K=5 portal hinge."""
    source_K: int
    receiver_K: int
    source_shell: Shell
    receiver_shell: Shell
    shared_band: int
    identity_holds: bool

    @property
    def statement(self) -> str:
        return (
            f"K={self.source_K} upper band {self.source_shell.upper} "
            f"= K={self.receiver_K} lower band {self.receiver_shell.lower}"
        )


def pyramid_k4_k5_hinge() -> PyramidHinge:
    """The canonical K=4 -> K=5 pyramid hinge."""
    source = shell(4)
    receiver = shell(5)
    return PyramidHinge(
        source_K=4,
        receiver_K=5,
        source_shell=source,
        receiver_shell=receiver,
        shared_band=source.upper,
        identity_holds=(source.upper == receiver.lower),
    )


# =============================================================================
# The J_4 partial isometry
# =============================================================================

def j4_partial_isometry() -> Matrix:
    """
    J_4 = |5, -><4, +|

    In a 3x3 representation mapping H_4 -> H_5 with both bases ordered
    [-, 0, +], J_4 has a 1 at row |5, -> = 0 and column |4, +> = 2.
    """
    J = [[0.0, 0.0, 0.0] for _ in range(3)]
    J[0][2] = 1.0
    return J


def interlevel_intertwiner_check() -> Dict[str, object]:
    """
    Intertwining identity:
        H_5 J_4 = J_4 H_4

    Both sides equal 21 * J_4 by the shift identity Phi_3(4) = Phi_6(5).
    """
    H4 = shell_hamiltonian(4)
    H5 = shell_hamiltonian(5)
    J4 = j4_partial_isometry()
    left = matmul(H5, J4)
    right = matmul(J4, H4)
    return {"H5J4": left, "J4H4": right, "holds": matrix_equal(left, right)}


# =============================================================================
# K=5 band assignment
# =============================================================================

def k5_band_assignment() -> Dict[str, Dict[str, object]]:
    """
    Functional assignment of the three K=5 bands in the apparatus reading.

        Phi_6(5) = 21  — receives K=4 upper-emission band
        Phi_4(5) = 26  — balance / reference
        Phi_3(5) = 31  — upper search / output pole
    """
    sh = shell(5)
    return {
        "lower_receive": {
            "band": sh.lower,
            "symbol": "Phi_6(5)",
            "function": "receives K=4 upper emission band",
        },
        "midpoint_balance": {
            "band": sh.neutral,
            "symbol": "Phi_4(5)",
            "function": "balance / reference / stabilization",
        },
        "upper_search": {
            "band": sh.upper,
            "symbol": "Phi_3(5)",
            "function": "upper search / output pole",
        },
    }


# =============================================================================
# Five-fold hinge decomposition on the K_5 sub-tetrahedra  [§03.1]
# =============================================================================

def sub_tetrahedron_count() -> int:
    """
    The pentachoron K_5 has C(5,4) = 5 sub-tetrahedral cells, one per
    excluded vertex. This forces a 5-fold multiplicity on the hinge J_4.
    """
    return 5


def s5_supset_s4_branching() -> Dict[str, int]:
    """
    The S_5 / S_4 branching index. S_5 (pentachoron symmetry) has 120
    elements; S_4 (any single sub-tetrahedron's symmetry) has 24.
    The index [S_5 : S_4] = 5 is exactly the sub-tetrahedron count.
    """
    s5_order = 120
    s4_order = 24
    return {
        'S5_order': s5_order,
        'S4_order': s4_order,
        'index_S5_over_S4': s5_order // s4_order,
        'sub_tetrahedron_count': sub_tetrahedron_count(),
        'indices_agree': (s5_order // s4_order == sub_tetrahedron_count()),
    }


def hinge_sub_tetrahedron_decomposition() -> Dict[str, object]:
    """
    Five-fold decomposition of the hinge:

        J_4 = sum_{v=1}^{5}  J_4^{(v)}  pi_v

    where pi_v projects onto the sub-tetrahedron excluding vertex v
    (one of the 5 K=4 tetrahedra inside K_5), and J_4^{(v)} is the
    hinge from that sub-tetrahedron into the K=5 shell.

    Engineering correspondence (5 relieving chambers above the King's
    Chamber): each relieving chamber realizes one J_4^{(v)} projection.
    Which chamber is electrically open / acoustically resonant picks
    the active sub-tetrahedron. The apparatus has a genuine 5-state
    switch at the hinge level.

    This function returns the structural data; the operators themselves
    live in the apparatus-dressed reading (portal_resonance module).
    """
    return {
        'multiplicity': sub_tetrahedron_count(),
        'decomposition': 'J_4 = sum_v J_4^{(v)} pi_v',
        'index_set': list(range(1, 6)),  # vertices 1..5 of K_5
        'projector_basis': [f'pi_{v} = projection onto K_5 \\ {{v}}'
                            for v in range(1, 6)],
        'physical_realization': '5 relieving chambers above the King\'s Chamber',
        'group_theory_basis': 's5_supset_s4_branching',
    }
