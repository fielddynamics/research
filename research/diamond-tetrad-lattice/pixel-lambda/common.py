"""The pixel: Field Origin O (index 0), TetA corners v_a (1-4), TetB corners -v_a (5-8)."""
import sympy as sp
LEGS = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
VERTS = LEGS + [tuple(-c for c in v) for v in LEGS]


def pixel_H(tA, tB, D):
    H = sp.zeros(9)
    H[0, 0] = D
    for i in range(1, 9):
        t = tA if i <= 4 else tB
        H[0, i] = H[i, 0] = -t
    return H


def leg_energy_share(psi, tA, tB):
    """Fraction of the legs' energy <H_legs> carried by the TetA legs (real psi)."""
    eA = sum(-tA * 2 * psi[0] * psi[i] for i in range(1, 5))
    eB = sum(-tB * 2 * psi[0] * psi[i] for i in range(5, 9))
    return sp.simplify(eA / (eA + eB))
